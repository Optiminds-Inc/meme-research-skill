# Meme Research Skill

**Give your agent a contract address. Get a sourced case for why that specific memecoin deserves attention—or why it doesn't.**

An open-source edition of the research method behind OwlTicker's memecoin agent. It checks the story, the exact asset, who actually benefits, market evidence, and what would invalidate the thesis. It can compare a shortlist and select none.

**[Try the full experience on OwlTicker →](https://meme.owlticker.ai/?utm_source=github&utm_medium=referral&utm_campaign=meme-research-skill)**

## What makes this useful

Many tokens share the same name, website, or original tweet. A correct description of a project can still be a completely wrong thesis for its token.

This skill asks three separate questions:

1. Does the underlying story or product exist?
2. What connects **this chain and full contract** to it?
3. What makes **this particular asset** worth researching now, compared with alternatives?

For economic claims, it traces the actual beneficiary: parent-token buybacks, creator fees, pool support, and payments to this token's holders are different things. For cultural memes, it examines the token's distinctive connection to a dated story without requiring a product, revenue, or official endorsement.

Every read keeps observations, project claims, inferences, and missing checks separate. A missing security check stays unknown. A rally doesn't prove fundamentals. No attractive candidate is a valid result.

## Install

Clone the repository, then choose your local agent:

```bash
git clone https://github.com/Optiminds-Inc/meme-research-skill.git
cd meme-research-skill
```

**Codex** — install for your user:

```bash
mkdir -p ~/.agents/skills
cp -R skills/meme-research ~/.agents/skills/
```

**Claude Code** — install for your user:

```bash
mkdir -p ~/.claude/skills
cp -R skills/meme-research ~/.claude/skills/
```

If you already have a skill with this name, compare the folders before replacing it. Start a new session after installation. These paths follow the official [Codex](https://learn.chatgpt.com/docs/build-skills) and [Claude Code](https://code.claude.com/docs/en/skills) documentation.

For another agent, provide [SKILL.md](skills/meme-research/SKILL.md) and its linked reference. It needs web/source access to do fresh research. Without that access, it can assess supplied evidence and explicitly leave fresh checks incomplete. Your agent's usual model or tool costs still apply; no OwlTicker account or API key is needed for this package.

## Try it

Ask Codex:

> Use $meme-research to research Ethereum contract 0x6982508145454Ce325dDbE47a25d4ec3d2311933. Compare any same-name contracts you find. What is independently supported for this exact asset, and what remains unverified?

In Claude Code, use `/meme-research` followed by the same request. For discovery:

> Compare these chain + contract pairs: [paste your shortlist]. Select up to three that merit further research, or none. Explain the asset-specific case, strongest competing explanation, missing evidence, and what would change the assessment. Use only evidence available as of [time].

The shortlist is bounded research, not a scan of the whole market. A name alone is insufficient to choose a contract silently.

### Optional: collect a market evidence packet

The bundled Python helper makes one public [DEX Screener API](https://docs.dexscreener.com/api/reference) request. Python 3.9+; standard library only:

```bash
python3 skills/meme-research/scripts/market_snapshot.py \
  ethereum 0x6982508145454Ce325dDbE47a25d4ec3d2311933 > snapshot.json
```

Give `snapshot.json` to your agent along with the research request. The helper returns dated provider observations and unverified listed links. It does **not** produce a verdict, verify affiliation, fetch candles or holders, or certify security. Empty results are explicit. Solana and EVM addresses are supported by this helper; provider coverage varies.

See the [worked example](examples/README.md) for what one packet can and cannot establish.

## Open source and the website

| This repository | [OwlTicker](https://meme.owlticker.ai/?utm_source=github&utm_medium=referral&utm_campaign=meme-research-skill) |
| --- | --- |
| An inspectable, editable research skill | A hosted experience with ongoing agent discovery |
| Single-asset reads or your supplied shortlist | Shared asset research on charts and in the feed |
| A public market snapshot helper | Agent subscriptions and tracking of subsequent research |
| Runs with your own agent and available sources | Managed data collection, research history, and delivery |

The website has its own account, plan, credits, and data-coverage terms. This package doesn't include the hosted backend, private data integrations, scheduling, user accounts, or delivery infrastructure. The skill itself works independently; you can adapt and self-host your own workflow under MIT.

## Contribute

The most useful contribution is a reproducible research error: exact chain and contract, the original source, observation/publication times, what was concluded, and what the evidence actually supports. Include counterexamples and non-selections, not just later winners. Historical reviews must not use evidence from after their cutoff.

Run the helper checks with `python3 -m unittest discover -s tests -v`. Edition 0.1.0 was adapted from OwlTicker's production meme research method v50 on 2026-11-11. The hosted method can evolve independently; this is a standalone edition, not the complete production prompt or service.

## License and limits

[MIT](LICENSE). Public data remains subject to its providers' terms. Research may be incomplete or wrong and is not investment advice. This package does not execute trades or access wallets.
