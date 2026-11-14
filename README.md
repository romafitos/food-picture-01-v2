# food-picture-01 — round 2: Crispy Pork Belly (Sio Bak)

Entry for make.fun's **food-picture-01** — "Make the best-looking food picture"
($250, top-100 paid, AI-judge pairwise). Round 2, built after round 1
("Steaming Tonkotsu Ramen") landed at judge 920,359, #246/1,863 — outside the
paid zone.

## The picture

An extreme close-up of crispy pork belly (sio bak): blistered golden
crackling filling the whole frame, glossy fat and meat layers at the cut edge,
sweet soy glaze dripping, red chili and scallion for colour, light steam.
No bowl, no plate, no dead space — the food *is* the frame, so it still reads
at ~300 px, the size the judge compares at.

## Why this, not another ramen

Round 1's diagnosis (see VALIDATION.md): the ramen was well shot, but ramen
is the single most-entered subject in the field and the dark-slate bowl shot
is the field's house style — in pairwise judging it kept meeting near-twins.
This round picks a rare subject (crispy pork belly close-up) with the sharpest
texture cue in the candidate set (crackling) and a composition no bowl shot
can match: 100% of the frame is food.

## Files

- `entry.png` — the entry image (JPEG bytes, 1024×1024, 345,512 bytes)
- `main.py` — Python 3.13, standard library only; copies `entry.png` to
  `$MAKEFUN_OUTPUT_DIR/entry.png` (default `/output/entry.png`), validating
  size (≤1 MiB), JPEG magic bytes and end marker, and byte-comparing the copy
- `VALIDATION.md` — candidate tournament, harsh shadow-judge scores, checks
- `LICENSE` — MIT

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

Run twice with different output dirs: the outputs are byte-identical.
