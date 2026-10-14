# Haven Economy and Social Report

Playtest harness: `run_haven_playtest.py` · Pack `03-haven-economy-social` · 10 scenarios x 12 agents · ≥20 seeds + 5 narratives each.
Sources: pending-review Gameplay Loop Bible extract; `src/data/haven.json`; `src/data/reputation.js`; `data/public/Decennium_Descent_Core_Systems_Data_v2_Known_Descent.json`; `data/crafting/Decennium_Descent_Crafting_Bible_v4.json`.
**No canon files were edited.**

## Transaction math
- Sale formula verified: Final Value = Base x Provenance x Demand x Condition x Urgency (Loop extract section 17).
- Worked example seed matches: 4500 x 1.0 x 1.25 x 0.5 x 1.1 = **3094 gp**.
- Tax rate **unpublished**; settlements used example residual ≈ **6.2702%**.
- Mean appraisal misprice |believed-true| across 20 seeds: **587.1 gp**.

## Sponsor comparison
- Gp-only best counts: `{'self_funded': 19, 'noble_temple': 1}` (dominant=False).
- Multifactor best counts: `{'sovereign': 2, 'self_funded': 17, 'noble_temple': 1}` (dominant=False).
- Finding: self-funded wins naive treasury math; priced non-gp benefits are required to keep the five-row table meaningful.

## Market exploits
- Shaved/counterfeit coin without remint fees -> face-value soft exploit (procedure gap).
- Smuggle beats legal in **0%** seeds under assumed risk model; domination requires ignoring catch/standing.
- Trafficking consequence-free rate **30%** when evidence fails - not closed.
- No infinite legal brew/substance profit vs rare artifact extraction at published list prices.

## Legal and faction consequences
- Haven resolution order (quarantine -> ... -> standing) is clear in bible extract.
- Standing scale conflict: Loop **-5..+5** vs `reputation.js` coarse tiers.
- Blackmail / illegal sale modeled with standing hits; consensual sex work kept distinct from trafficking.

## Labor and trafficking safeguards
- Chain Market is named as political conflict in `haven.json`, but **numeric** wage/debt/emancipation/prosecution procedures are missing.
- Emancipation rate under test assumptions: **15%**; rescue **20%**.
- Safeguards exist as narrative districts + inspection order; not yet as closed mechanical loops.

## Brewing and substance findings
- Core Systems: prices, dependence DCs, legality, crash effects - usable.
- Market premiums, rehab, brew COGS, licenses - **Director gaps**.
- Substance/brew side loops do not obsolete extraction.

## Recommended changes
See `proposed_patches/PROPOSED_PATCHES.md` (proposals only).

## Market shock
- Mean Tier II glut collapse: **55%**.
- Deeper extraction still relevant: **100%** of seeds.
