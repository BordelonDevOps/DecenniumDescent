# Cargo and Extraction Risk Calibration — Compiled Report

**Pack:** `12-cargo-extraction-risk`  
**Evidence:** Level A (seeded route/cargo Monte Carlo on Gameplay Loop v1.1)  
**Canon:** No edits.  
**Volume:** 150 cell result JSONs; matrix runs 2500–5000 per cell

## Primary question

Do Load, capacity, Extraction Class, Attention, Mapping, and cargo priorities create rational tradeoffs without making profit arbitrary?

**Verdict:** Yes on retention vs EC — retained load fraction falls as EC rises; Unknown routes cut Haven rate. Profit remains noisy but ordered; Attention cargo is not “free.”

## Scenario coverage

| Scenario | Cells | Mean havenRate | Mean retainedLoadFrac | Mean trueProfit |
|---|---:|---:|---:|---:|
| CARGO-LIGHT (EC0–2) | 36 | 1.00 | 0.81 | ~20 |
| CARGO-RARE (EC3–4) | 24 | 1.00 | 0.68 | ~151 |
| CARGO-ATTENTION (EC4–6) | 36 | 1.00 | 0.54 | ~433 |
| CARGO-CASUALTY (EC2–4) | 36 | 1.00 | 0.69 | ~89 |
| CARGO-UNKNOWN (EC3–5) | 18 | 0.83 | 0.62 | ~419 |

## EC retention curve (evidence A)

| EC | Mean retained load fraction | Notes |
|---:|---:|---|
| 0 | 0.836 | Ordinary goods |
| 1 | 0.807 | Common salvage |
| 2 | 0.777 | Uncommon/fragile |
| 3 | ~0.73–0.79 | Rare/volatile |
| 4 | ~0.55–0.63 | Strategic / Attention |
| 5–6 | ~0.50–0.54 | Epic/legendary Attention |

Monotonic decline supports rational cargo-class tradeoffs.

## Rules halts

- **EXTRACTION-CARGO-DC-MODS** (all scenarios)
- **UNKNOWN-PROGRESS-ZERO** (CARGO-UNKNOWN)

## Confirmed findings

1. Higher Extraction Class ⇒ lower retained fraction and higher absolute profit when extraction succeeds (risk/reward present).
2. Unknown mapping is the only scenario with material Haven failure (~17% miss).
3. Casualty runs retain ~69% load on average — Living priority helps but crit-fail multi-lot dumps still bite.

## Suspected defects

- HavenRate≈1.0 on Mapped Attention runs may understate Attention Pressure in full agentic play (Pack 02 historically hit P6 often).
- Profit P10–P90 spreads exist; not collapsed to a single arbitrary value.

## Proposed follow-up

Numeric cargo DC modifier table; Attention cadence already clearer in v1.1 JSON than V7 bible — keep and cross-link.

## Evidence limitations

Extraction Class DC bump is a proxy. Priority dumping uses lowest priority first on failure — matches intent, not full Quartermaster UI.
