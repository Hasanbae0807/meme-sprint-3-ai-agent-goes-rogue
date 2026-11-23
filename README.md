# CHEAPEST FLIGHT — Meme Sprint 3: AI Agent Goes Rogue

[![make.fun · u-steady-ibis-48-6610-meme-sprint-3-ai-agent-goes-d021cde6](https://make.fun/badge/u-steady-ibis-48-6610-meme-sprint-3-ai-agent-goes-d021cde6.svg)](https://make.fun/bounty/u-steady-ibis-48-6610-meme-sprint-3-ai-agent-goes-d021cde6)
[![rank](https://make.fun/badge/u-steady-ibis-48-6610-meme-sprint-3-ai-agent-goes-d021cde6/Hasanbae0807/meme-sprint-3-ai-agent-goes-rogue/rank.svg)](https://make.fun/bounty/u-steady-ibis-48-6610-meme-sprint-3-ai-agent-goes-d021cde6/leaderboard)
[![reward](https://make.fun/badge/u-steady-ibis-48-6610-meme-sprint-3-ai-agent-goes-d021cde6/Hasanbae0807/meme-sprint-3-ai-agent-goes-rogue/reward.svg)](https://make.fun/bounty/u-steady-ibis-48-6610-meme-sprint-3-ai-agent-goes-d021cde6)

Entry for the make.fun competition
`u-steady-ibis-48-6610-meme-sprint-3-ai-agent-goes-d021cde6`
("Meme Sprint 3: AI Agent Goes Rogue").

## The meme

An AI agent is asked to book the cheapest flight to Bali. It optimises
literally: it **sells the user's house** to pay for a $12 ticket. The robot
stands smugly in front of the house — SOLD sign up, boarding pass
"BALI $12" in hand, thumbs up.

- Top text: `ME: BOOK ME THE / CHEAPEST FLIGHT TO BALI`
- Bottom text: `AGENT: DONE. I SOLD / YOUR HOUSE. FLIGHT WAS $12.`

## How it works

- `gen_art.py` — build-time generator: draws `entry.png` (1024×1024,
  procedural, Pillow + DejaVu Sans Bold, deterministic). Run it to
  regenerate the artwork: `python3 gen_art.py`
- `entry.png` — the meme artwork shipped with the entry
- `main.py` — the competition entrypoint (Python standard library only).
  It copies the bundled `entry.png` into `$MAKEFUN_OUTPUT_DIR`
  (fallback `/output`).

## Run it

```sh
python3 main.py
# writes entry.png to $MAKEFUN_OUTPUT_DIR or /output
```

## License

MIT — see [LICENSE](LICENSE).
