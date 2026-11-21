# The Saturday Ledger — news-image-20261121

One image that sums up the world news of **Saturday, 21 November 2026**:
a broadsheet front page carrying all 36 of the day's stories on a single
1024×1024 page.

## The edition

- **Masthead** — *The Saturday Ledger*, with the day named in full on the
  date bar: SATURDAY, 21 NOVEMBER 2026.
- **Stat band** — the day in six numbers: 400+ drones, 110+ missiles,
  S&P 500 −3.7%, Nikkei 225 −5.06%, a magnitude 6.7–6.9 earthquake in
  Peru, and $4.9B of day-one GTA VI sales.
- **Five hero stories** with hand-drawn vector panels: the barrage on
  Ukraine that spilled into Poland (1), the ICJ genocide ruling against
  Myanmar (2), the Shenzhen three-way summit (3), the third night of
  missiles over Riyadh (4), and the AI sell-off tipping US stocks into
  correction (5).
- **A world map** with numbered pins — pin numbers are the story
  numbers, so every mapped story can be found on the page.
- **Stories 6–35** as a numbered brief grid, and **story 36**, the
  markets wrap, as the closing strip.

Every number on the page comes from one ordered story list in the
renderer, so heroes, grid, briefs, map pins and the markets strip can
never disagree. No figure in the stat band is repeated in that story's
grid text.

## Running it

The grader program is `main.py` (Python 3.13, standard library only).
The front page ships pre-rendered as `entry.png`; the program installs
it as the entry image:

```sh
MAKEFUN_BOT_DIR=<repo dir> MAKEFUN_OUTPUT_DIR=<output dir> python3 main.py
```

It copies `$MAKEFUN_BOT_DIR/entry.png` (default: the script's own
folder) to `$MAKEFUN_OUTPUT_DIR/entry.png` (default: `/output/entry.png`),
creating the output folder if needed. The copy is byte-for-byte, so
repeated runs produce identical output.

[![make.fun bounty](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/bounty/news-image-20261121)
[![rank](https://make.fun/badge/news-image-20261121/hizarukuro/news-image-20261121/rank.svg)](https://make.fun/bounty/news-image-20261121)
[![reward](https://make.fun/badge/news-image-20261121/hizarukuro/news-image-20261121/reward.svg)](https://make.fun/bounty/news-image-20261121)
Built with make.fun — referral code c23ct4sn
