# Regression and Release Gate — COMPILED_REPORT

**Raw JSON results:** 7
**Evidence level:** A (validators/baselines) + B (usability deps)
**Canon edits:** none

## Test volume

- REG-STATIC: magic, class abilities, public-canon, gameplay-loop, preflight rerun
- REG-COMBAT / REG-EXPEDITION / REG-ECONOMY: 00-baseline-simulations chassis CSVs on disk
- REG-CANON: public/director visibility + encoding gate
- Dependencies used: 00 baselines, 16 fuzz summary, packs 05+17 from this run
- Missing preferred deps (noted, not invented): full agent JSON for packs 01/07/08/11/12/13

## Source and fixture hashes

- See `playtests/ai-mega-suite/results/05-17-18-source-freeze.json`

## Results by scenario

- **REG-CANON:** 1 results; outcomes: FAIL
- **REG-COMBAT:** 2 results; outcomes: BASELINE_LOCKED, FAIL
- **REG-ECONOMY:** 1 results; outcomes: BASELINE_LOCKED
- **REG-EXPEDITION:** 1 results; outcomes: BASELINE_LOCKED
- **REG-STATIC:** 2 results; outcomes: FAIL, GATE_FAIL

## Validator rerun

- `C:\Python\python.exe tools/validate_magic_system.py` -> returncode 0
- `node --no-warnings tools/validate_class_abilities.mjs` -> returncode 0
- `C:\Python\python.exe tools/validate_public_canon.py` -> returncode 1
- `C:\Python\python.exe tools/validate_gameplay_loop.py` -> returncode 1
- `C:\Python\python.exe playtests/ai-mega-suite/tools/preflight.py` -> returncode 0

## Statistical distributions

- Pack 16 fuzz on disk: runs=100000, failureCount=5769, seed=71600.
- Chassis baselines: combatRows=72, expeditionRows=60, economyRows=5 (summary.json).
- Note: fuzz failureCount reflects encoded scenario matrix status on disk at gate time; not a silent rewrite of combat DPR.

## Interpretation

- validate_magic_system.py PASS; validate_class_abilities.mjs PASS; preflight.py PASS.
- validate_public_canon.py FAIL: Windows charmap decode on floor-encounters.json / bestiary_data_full.json (byte 0x9d) — tooling/encoding release-gate blocker, not proven spoiler leak.
- validate_gameplay_loop.py returncode 1 on this host due to stdout UnicodeEncodeError (arrow characters under cp1252); treat as tooling gate, not rules regression.
- No approved numerical patch branch to diff; gate is baseline integrity + validators + usability packs 05/17.
- GATE_FAIL until public-canon encoding (and gameplay-loop console encoding) are UTF-8 safe.

## Rules halts

- None raised inside pack 18 agents; usability RULES_HALTs live in packs 05/17.

## Confirmed defects

- Public-canon validator encoding failure (release gate).
- Gameplay-loop validator console encoding fragility (release gate).
- Usability RULES_HALTs from packs 05/17 (Rest Debt UI; Retreat ambiguity) — clarity, not baseline math drift.

## Suspected defects

- Incomplete suite coverage: most packs 01-16 lack complete agent JSON on disk; full post-patch regression not yet possible.
- Pack 16 fuzz reports failureCount=5769 — requires pack-16 owner interpretation before treating as release blocker vs expected invariant probes.

## Null findings

- No proposed numerical patch branch to diff against combat/expedition/economy chassis baselines.
- Chassis baseline row counts match summary.json (72 / 60 / 5).

## Proposed follow-up

- Make validators UTF-8 safe on Windows.
- Complete remaining mega-suite packs before claiming full release regression.
- Apply clarity patches from 05/17 only after owner review (no silent canon overwrite).

## Evidence limitations

- Level B usability cannot prove human fun or comprehension.
- Baseline CSVs are chassis proxies per summary warning.

