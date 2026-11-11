# Worked examples: market evidence is a starting point

These are actual public API responses collected on 2026-11-11, preserved with their retrieval times. They are historical examples, not current prices, live research, or favorable selections. Re-run the helper for fresh observations. No model was run to generate the JSON packets; the interpretations below were written from the stated evidence.

## PEPE: observations without a complete selection case

**Asset:** Ethereum `0x6982508145454Ce325dDbE47a25d4ec3d2311933`.

**Evidence:** [saved packet](pepe-market-snapshot.json), retrieved at `2026-11-11T02:43:29.870239Z` from this [exact-address endpoint](https://api.dexscreener.com/token-pairs/v1/ethereum/0x6982508145454Ce325dDbE47a25d4ec3d2311933). The provider returned 30 exact-base-token pairs. That is provider coverage, not an assertion that every pool was found.

One returned pool, `0xA43fe16908251ee70EF74718545e4FE6C5cCEc9f`, reported a base-token USD price of `0.000005466`, 1-hour USD volume of `159166.08`, and 19 buy transactions / 41 sell transactions in that hour. These observations concern that pool and window. They don't establish unique buyers, flow ownership, or a price trend. The packet has no original market observation timestamp; its retrieval time isn't one.

**An appropriately bounded read:** This packet establishes provider-reported trading observations for the specified base contract. It does not establish a new reason to select this asset now. Its website/social fields are leads; it has no independently checked holder distribution, permission checks, fee receipts, current catalyst, or closed candle history. Market stage and any favorable selection remain unassessed from this packet alone. Research the original narrative and its connection to this asset, then compare its current case with alternatives and material counterevidence.

**An unsupported leap:** Describing 19 buys as 19 independent investors, reading one rolling hour as a bottom or breakout, or using the listed website to declare affiliation and security verified.

Try:

> Use the meme-research skill to assess this saved evidence as of its retrieval time. Separate observed facts from what still needs research. Do not use later prices or invent a favorable selection. For a fresh assessment instead, collect fresh evidence and keep its date separate.

## WORTHLESS: an empty result isn't a negative verdict

**Asset:** Solana `HSTcEvAwhpYW17x8MhsqQwEe7KAXd3V1VgCh7mifd2qd`.

**Evidence:** [saved packet](worthless-market-snapshot.json), retrieved at `2026-11-11T02:42:42.261102Z` from this [exact-mint endpoint](https://api.dexscreener.com/token-pairs/v1/solana/HSTcEvAwhpYW17x8MhsqQwEe7KAXd3V1VgCh7mifd2qd). The response was an empty list.

**An appropriately bounded read:** This provider returned no pool observations for the request. Price, liquidity, and current activity are unknown from this packet. It doesn't establish that the token has no market, is abandoned, or is fraudulent. A fresh read needs other exact-mint sources; missing coverage can't be replaced with another same-name token's data.

**An unsupported leap:** Turning absent prices into zero, or silently switching to a same-name contract that has a more attractive market chart.

The skill's job is to investigate these gaps with the user's available sources, then deliver the strongest conclusion the evidence actually supports. The collector's job is simply to preserve observations and their limits.
