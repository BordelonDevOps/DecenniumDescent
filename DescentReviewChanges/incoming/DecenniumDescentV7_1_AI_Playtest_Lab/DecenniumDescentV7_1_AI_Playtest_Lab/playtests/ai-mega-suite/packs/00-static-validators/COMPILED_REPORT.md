# 00 Static Validators — Compiled Report

Outcome: FAIL

- python tools/validate_magic_system.py → rc=0
  - stdout: PASS spells=848 placements=936 varied_acquisition=619 classes=17
- node --no-warnings tools/validate_class_abilities.mjs → rc=0
  - stdout: PASS classes=17 core=17 feats=335 oaths=10 mysteries=10 curses=10
- python tools/validate_public_canon.py → rc=1
  - stdout: FAIL public-canon-boundary
floor-encounters.json invalid: 'charmap' codec can't decode byte 0x9d in position 1373: character maps to <undefined>
bestiary_data_full.json invalid: 'charmap' codec can't decode byte 0x9d in position 170921: character maps to <undefined>
- python tools/validate_gameplay_loop.py → rc=0
  - stdout: Gameplay loop validation: PASS â€” complete preparation â†’ descent â†’ extraction â†’ Haven â†’ seasonal loop
