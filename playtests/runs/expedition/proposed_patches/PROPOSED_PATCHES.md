# Proposed patches — Pack 02 Expedition / Extraction
**Status:** proposals only — NOT applied to canon.
**Evidence base:** deterministic multi-iteration sims per SCENARIO_MATRIX.csv; bible = `GAMEPLAY_LOOP_BIBLE_v1_EXTRACT.txt`.
**Assumption:** Pack 01 combat results not ready (0 JSON); class balance not used beyond tier DC checks.

## P2-01 — Define Extraction Test spacing
- **Issue:** Bible §16 says test at every major route transition; no numeric spacing.
- **Evidence:** All scenarios required a Director ruling (sim used every 4 Progress).
- **Proposal:** Add table: Mapped segment = 1 test per Length/2 Progress; Unknown/Sketched = every 3 Progress; always on Severe complication.

## P2-02 — Attention Pressure cadence
- **Issue:** §7 lists Attention-tagged artifact as Pressure increase condition without per-Watch vs once-while-carried clarity.
- **Evidence:** EXP-HAVEN-RUN / EXP-CASUALTY Pressure peaks sensitive to interpretation.
- **Proposal:** Increase once when first carried into a Watch, then only again if re-exposed after concealment OR on complication.

## P2-03 — Profitability charter metric
- **Issue:** 'Return profitable' / 8,000 gp objectives ambiguous vs sponsor shares and wages (§17).
- **Evidence:** EXP-T1 avg profit -382.9; EXP-HAVEN-RUN objective rate 0.0%.
- **Proposal:** Charter fields: `gross_target`, `net_after_sponsor_target`, `profit_after_wages_target` — pick one as primary.

## P2-04 — Forage output cap
- **Issue:** Tier I Forage can erase Supply abort pressure on Mapped Risk 1.
- **Proposal:** Cap Forage at `tier_biome_rating` units; Critical Success needed to exceed; Failure risks exposure Pressure.

## P2-05 — Rest-debt for evening camp workers
- **Issue:** Camp example has 3 workers skip Rest; §5 Strain rule needs explicit same-day vs next-day timing.
- **Proposal:** Workers who skip Evening Rest must take Morning Rest next day or gain 1 Strain at next day-boundary.

## P2-06 — Companion SOURCE_MANIFEST gaps
- **Issue:** `GAMEPLAY_LOOP_CANON.md`, `gameplay-loop.json`, `ExpeditionTracker.tsx` not on main.
- **Proposal:** Promote bible → canon + JSON + tracker UI under owner order; until then keep extract as pending-review SoT for playtests.

## P2-07 — Sample company Combat band
- **Issue:** Pack roster Combat=3 vs optimal 4–6; EXP-CASUALTY collapses Escort capacity.
- **Proposal:** Adjust worked example / pack roster to 4 Combat OR document 3-Combat professional company as supported variant.
