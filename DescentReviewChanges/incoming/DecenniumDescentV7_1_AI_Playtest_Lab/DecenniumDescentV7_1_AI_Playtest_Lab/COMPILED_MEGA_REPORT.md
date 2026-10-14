# Decennium Descent V7.1 — Compiled Mega Report

**Date:** 2026-08-06  
**Run root:** `C:\Github\Descent assets\DecenniumDescent-main\DescentReviewChanges\incoming\DecenniumDescentV7_1_AI_Playtest_Lab\DecenniumDescentV7_1_AI_Playtest_Lab`  
**Status:** Partial suite compile (packs 01-04 GAP). **Post-pack-11-14 mega refresh** (`npm run test:ai:compile` / `compile_all_results.py`: 20 pack slots, 1941 JSON). **No ReviewBible/main promotion. No silent canon rewrites.**

Auto index also at: `playtests/ai-mega-suite/AI_PLAYTEST_MASTER_REPORT.md` (1941 JSON files; compile refreshed 2026-08-06 after packs 11-14).

---

## 1. Executive findings

1. **Encounter budget bands are ordered but soft mid-tier.** Packs 07/08 show global difficulty order held (routine ≫ catastrophic), yet routine/standard often collapse to ~100% win after L5, while L1 standard is far deadlier (~42% WR). Chassis needs level-scaled budget review before class-balance claims.
2. **Objective-step RULES_HALT cluster (Pack 08).** Gameplay Loop canon says objectives/terrain/surprise/hazards each bump effective difficulty one step “unless already included.” Scenario matrices label bands while sims add objective mechanics separately → double-count / under-count ambiguity. Highest-priority rules clarification.
3. **Rest Debt / ExpeditionTracker conflict (Packs 05/17).** UI `/3` counter vs canon two-Watch Rest Debt window — repeated RULES_HALT. Authoritative clock must be named for live play.
4. **Release gate FAIL on Windows encoding (Pack 18), not proven spoiler leak.** `validate_public_canon.py` fails decoding UTF-8 JSON under cp1252; `validate_gameplay_loop.py` can fail on arrow Unicode print. Magic + class validators PASS. Fix tooling UTF-8 before treating as content regression.
5. **Packs 01–04 not re-run this wave.** Coverage deferred to successor packs (06 combat, 11–13 loop, 14 seasonal). Prior V7 kits evidence still historical, not this lab’s raw JSON.

## 2. Evidence quality and test volume

| Kind | Evidence |
|------|----------|
| Executable baselines | 00: 72 combat / 60 expedition / 5 economy rows; 500 runs/combat fixture |
| Monte Carlo chassis | 07: 38k combats; 08 budgets; 11 attrition; 12 cargo; 13 Haven; 14 seasonal; 16 fuzz |
| Dice-level | 06: 133 pack result files (roll transcripts + meta) |
| Usability / GM | 05, 17 agentic prompt batteries |
| Regression gate | 18 against validators + baselines |
| Raw JSON (suite compile) | **1941** |
| Finding records / rules halts (index) | ~887 / ~1036 (many duplicates across seeds) |

AI narration is **not** numerical evidence. Chassis proxies ≠ full class builds.

## 3. Mathematical chassis

- Hit rates ~0.50–0.63 across levels (readable d20).
- Mean WR by labeled difficulty (Pack 07): routine 1.00 · standard 0.92 · hard 0.74 · severe 0.24 · catastrophic 0.03.
- Suspected: `standard_off_band`, `band_collapse`, `level_curve_instability` (early deadly / mid soft / L20 hard re-tightens).

## 4–6. Action economy, class balance, feats/spells

- Pack **06** dice-level runs completed (primary tactical evidence).
- Packs **09 / 10 / 15** completed with executable stress scanners (5 / 5 / 9 result files) — exploit hypotheses logged in pack reports; do not promote without human confirmation.
- Packs **01** (class balance narrative) **GAP** this run.

## 7–8. Encounter budgets & boss/control

- Pack **08:** objective-step RULES_HALT; adjacent budget bands often non-distinct at high severity wipe floors.
- Pack **15:** boss/control/PvP stress artifacts present; Director-only outputs must stay sealed.

## 9–12. Expedition, cargo, Haven, seasonal

- **11** attrition MC: 198 results + COMPILED_REPORT.
- **12** cargo/extraction: 150 results.
- **13** Haven economy stress: 43 results.
- **14** seasonal cycle: 67 results.
- Track gross vs net vs true profit separately (per batch guide); see pack reports for seed ledgers.

## 13. Readability / GM readiness

- **05** + **17** DONE. Human agenda must confirm turn speed, cognitive load, and fun — AI personas prove friction, not enjoyment.
- Missing public one-page Quickstart sheet noted as RULES_HALT in Pack 17.

## 14. Rules halts and contradictions (deduped themes)

| Theme | Packs | Note |
|-------|-------|------|
| Encounter objective difficulty step | 08 | Clarify include-vs-bump |
| Rest Debt clock UI vs §5 | 05, 17 | Pick authoritative clock |
| Retreat Escape stacking same round | 17 | §12 ambiguous |
| Public Quickstart sheet | 17 | Not found |
| Windows UTF-8 validators | 00, 18 | Tooling, not canon rewrite |

## 15. Confirmed defects (lab environment)

- Public-canon validator **FAIL** under Windows default encoding on `floor-encounters.json` / `bestiary_data_full.json`.
- Pack 18 **GATE_FAIL** until UTF-8-safe validators.

## 16. Suspected defects (need human / fuller class sims)

- Mid-level budget softness and L1 deadliness (07/08).
- Objective-step ambiguity (08).
- Rest Debt / Retreat Escape clarity (17).
- Class-specific dominance: insufficient without Pack 01 + deeper Pack 06 class personas.

## 17. Proposed changes (confidence-ranked — patches only)

Place any approved drafts under `playtests/ai-mega-suite/proposed-patches/`. **Do not edit canon in-lab.**

1. **High:** Clarify GAMEPLAY_LOOP objective/terrain difficulty step accounting.
2. **High:** Align ExpeditionTracker Rest Debt with canon §5 (or document UI as house).
3. **High:** Force UTF-8 in validator file IO / console (lab tooling).
4. **Med:** Level-scale encounter budgets so standard≠routine at L5–15.
5. **Med:** Publish or locate public Quickstart one-pager.
6. **Low until Pack 01/06 deep pass:** class numerical retunes.

## 18. Human GM playtest agenda

1. Table: L1 standard + L5 standard same party — confirm early spike / mid soft feel.
2. Director prep: one cargo objective fight — does difficulty step feel double-counted?
3. Watch Rest Debt assignment forgetfulness — which clock do you use?
4. Time-to-first-combat for new players without Quickstart sheet.
5. One Haven settlement with taxes/Heat — verify companion vs book.

---

## Pack completion matrix

| Pack | Status |
|------|--------|
| 00-baseline-simulations | DONE |
| 00-static-validators | DONE (PARTIAL validators: encoding FAIL) |
| 01-combat-class-balance | **GAP** |
| 02-expedition-extraction | **GAP** |
| 03-haven-economy-social | **GAP** |
| 04-seasonal-decennial-persistence | **GAP** |
| 05-readability-speed-onboarding | DONE |
| 06-dice-level-combat-validation | DONE |
| 07-statistical-combat-calibration | DONE |
| 08-encounter-budget-calibration | DONE |
| 09-feat-spell-ability-interactions | DONE |
| 10-progression-multiclass-exploit | DONE |
| 11-expedition-attrition-monte-carlo | DONE |
| 12-cargo-extraction-risk | DONE |
| 13-haven-economy-stress | DONE |
| 14-seasonal-cycle-simulation | DONE |
| 15-boss-control-pvp | DONE |
| 16-rules-fuzz-property-tests | DONE |
| 17-gm-readiness-usability | DONE |
| 18-regression-release-gate | DONE (GATE_FAIL env) |

**Completed this run:** 00×2, 05–18 (16 content packs + 2 prep) = **18 tracker rows DONE**; **4 GAPs** (01–04).

## Artifacts

- Master auto-index: `playtests/ai-mega-suite/AI_PLAYTEST_MASTER_REPORT.md`
- Per-pack: `playtests/ai-mega-suite/packs/<id>/COMPILED_REPORT.md`
- Raw: `playtests/ai-mega-suite/results/` and `packs/*/results/`
- Status: `playtests/ai-mega-suite/RUN_STATUS.md`
- Zip: `C:\Users\cbord\Downloads\DD_V7_1_AI_Lab_Reports.zip`
