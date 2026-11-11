#!/usr/bin/env python3
"""Collect exact-base-token market observations without making a research verdict."""

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from urllib.error import HTTPError, URLError
from urllib.parse import quote
from urllib.request import Request, urlopen


LIMITATIONS = [
    "retrievedAt is the collector's UTC time, not the provider's market observation time.",
    "Pairs are provider-reported observations, not independently verified on-chain state.",
    "Only exact-chain, exact-base-token matches are returned; priceUsd prices the base asset.",
    "Rolling-window values are not OHLC history, unique traders, or proof of independent demand.",
    "Listed websites and socials are untrusted leads, not verified affiliation or endorsement.",
    "Market cap and displayed liquidity are not invested capital or executable exit proceeds.",
    "Identity, holders, control, security, revenue and execution receipts were not checked.",
    "Provider pool coverage may be incomplete; an empty response does not prove no market exists.",
]


def validate_identity(chain, address):
    if not re.fullmatch(r"[a-z0-9][a-z0-9-]{0,49}", chain):
        raise ValueError("chain must be a lowercase DEX Screener chain ID")
    if chain == "solana":
        if not re.fullmatch(r"[1-9A-HJ-NP-Za-km-z]{32,44}", address):
            raise ValueError("Solana address must be a full base58 mint (32–44 characters)")
    elif not re.fullmatch(r"0x[0-9a-fA-F]{40}", address):
        raise ValueError("this helper supports Solana mints or full 0x EVM addresses")


def same_address(chain, left, right):
    if not isinstance(left, str) or not isinstance(right, str):
        return False
    return left == right if chain == "solana" else left.lower() == right.lower()


def build_packet(chain, address, pairs, source_url, retrieved_at):
    validate_identity(chain, address)
    if not isinstance(pairs, list) or any(not isinstance(pair, dict) for pair in pairs):
        raise ValueError("unexpected provider response: expected a list of pair objects")
    matches = []
    quote_matches = 0
    excluded = 0
    for pair in pairs:
        if pair.get("chainId") != chain:
            excluded += 1
            continue
        base = pair.get("baseToken") or {}
        quoted = pair.get("quoteToken") or {}
        if not isinstance(base, dict) or not isinstance(quoted, dict):
            raise ValueError("unexpected provider response: invalid token identity")
        if same_address(chain, base.get("address"), address):
            matches.append(pair)
        elif same_address(chain, quoted.get("address"), address):
            quote_matches += 1
        else:
            excluded += 1
    return {
        "schemaVersion": 1,
        "identity": {"chain": chain, "address": address},
        "source": {"provider": "DEX Screener", "url": source_url},
        "retrievedAt": retrieved_at,
        "providerObservedAt": None,
        "status": "observations_available" if matches else "no_base_pair_observations",
        "coverage": {
            "receivedPairs": len(pairs),
            "includedBasePairs": len(matches),
            "excludedQuotePairs": quote_matches,
            "excludedOtherPairs": excluded,
        },
        "limitations": list(LIMITATIONS),
        "providerPairs": matches,
    }


def fetch_packet(chain, address):
    validate_identity(chain, address)
    source_url = "https://api.dexscreener.com/token-pairs/v1/{}/{}".format(
        quote(chain, safe=""), quote(address, safe="")
    )
    request = Request(source_url, headers={
        "Accept": "application/json",
        "User-Agent": "owlticker-meme-research/0.1.0",
    })
    with urlopen(request, timeout=20) as response:
        pairs = json.load(response)
    retrieved_at = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    return build_packet(chain, address, pairs, source_url, retrieved_at)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("chain", help="DEX Screener chain ID, e.g. solana, ethereum or base")
    parser.add_argument("address", help="full Solana mint or EVM contract address")
    args = parser.parse_args()
    try:
        packet = fetch_packet(args.chain, args.address)
    except HTTPError as error:
        print("Market snapshot failed: provider returned HTTP {}".format(error.code), file=sys.stderr)
        return 1
    except (ValueError, URLError, TimeoutError, OSError) as error:
        print("Market snapshot failed: {}".format(error), file=sys.stderr)
        return 1
    print(json.dumps(packet, ensure_ascii=False, indent=2, allow_nan=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
