"""Check identity, evidence gaps, and provider failure behavior without network calls."""

import contextlib
import importlib.util
import io
from pathlib import Path
import unittest
from unittest.mock import patch
from urllib.error import HTTPError


SCRIPT = Path(__file__).resolve().parents[1] / "skills/meme-research/scripts/market_snapshot.py"
SPEC = importlib.util.spec_from_file_location("market_snapshot", SCRIPT)
snapshot = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(snapshot)
MINT = "HSTcEvAwhpYW17x8MhsqQwEe7KAXd3V1VgCh7mifd2qd"
EVM = "0x" + "aB" * 20


def packet(chain, address, pairs):
    return snapshot.build_packet(chain, address, pairs, "https://example.test/source", "2026-11-11T00:00:00Z")


class EvidencePacketTests(unittest.TestCase):
    def test_same_ticker_does_not_match_different_mint(self):
        result = packet("solana", MINT, [{
            "chainId": "solana",
            "baseToken": {"address": "other", "symbol": "WORTHLESS"},
        }])
        self.assertEqual(result["providerPairs"], [])
        self.assertEqual(result["status"], "no_base_pair_observations")

    def test_quote_match_cannot_borrow_base_price(self):
        result = packet("solana", MINT, [{
            "chainId": "solana", "baseToken": {"address": "other"},
            "quoteToken": {"address": MINT}, "priceUsd": "100",
        }])
        self.assertEqual(result["providerPairs"], [])
        self.assertEqual(result["coverage"]["excludedQuotePairs"], 1)

    def test_chain_must_match_even_when_evm_address_matches(self):
        result = packet("base", EVM, [{
            "chainId": "ethereum", "baseToken": {"address": EVM},
        }])
        self.assertEqual(result["coverage"]["excludedOtherPairs"], 1)

    def test_solana_case_is_significant(self):
        self.assertFalse(snapshot.same_address("solana", MINT, MINT.lower()))

    def test_evm_checksum_case_is_not_significant(self):
        result = packet("base", EVM, [{"chainId": "base", "baseToken": {"address": EVM.lower()}}])
        self.assertEqual(len(result["providerPairs"]), 1)

    def test_missing_measurements_stay_missing_and_clocks_are_separate(self):
        raw = {"chainId": "solana", "baseToken": {"address": MINT}, "priceUsd": None}
        result = packet("solana", MINT, [raw])
        self.assertIsNone(result["providerObservedAt"])
        self.assertIsNone(result["providerPairs"][0]["priceUsd"])
        self.assertNotIn("liquidity", result["providerPairs"][0])
        self.assertEqual(result["retrievedAt"], "2026-11-11T00:00:00Z")

    def test_empty_response_is_coverage_gap(self):
        result = packet("solana", MINT, [])
        self.assertEqual(result["status"], "no_base_pair_observations")
        self.assertEqual(result["coverage"]["receivedPairs"], 0)
        self.assertTrue(result["limitations"])

    def test_unexpected_response_fails_instead_of_looking_empty(self):
        for response in ({"error": "rate limit"}, None, [None], ["pair"]):
            with self.subTest(response=response), self.assertRaises(ValueError):
                packet("solana", MINT, response)

    def test_bad_address_and_chain_fail_before_network(self):
        for chain, address in [("solana", "WORTHLESS"), ("base", "0x123"), ("../../x", EVM)]:
            with self.subTest(chain=chain), self.assertRaises(ValueError):
                snapshot.fetch_packet(chain, address)

    def test_http_failure_is_nonzero_with_no_json_stdout(self):
        error = HTTPError("https://example.test", 429, "Too Many Requests", {}, None)
        stdout, stderr = io.StringIO(), io.StringIO()
        with patch("sys.argv", ["market_snapshot.py", "solana", MINT]), \
             patch.object(snapshot, "fetch_packet", side_effect=error), \
             contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            self.assertEqual(snapshot.main(), 1)
        self.assertEqual(stdout.getvalue(), "")
        self.assertIn("429", stderr.getvalue())


if __name__ == "__main__":
    unittest.main()
