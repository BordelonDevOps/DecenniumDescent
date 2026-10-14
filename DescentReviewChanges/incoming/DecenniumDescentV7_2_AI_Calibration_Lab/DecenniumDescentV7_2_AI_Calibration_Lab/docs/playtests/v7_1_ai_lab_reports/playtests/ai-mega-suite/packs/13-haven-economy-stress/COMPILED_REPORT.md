# Haven Economy Stress Test — Compiled Report

**Pack:** `13-haven-economy-stress`  
**Evidence:** Level A (executable sale/tax/share/Heat/debt/assay/reputation formulas from Gameplay Loop v1.1)  
**Canon:** No edits.  
**Volume:** 43 cell JSONs; 5k–10k runs per cell as matrixed

## Primary question

Do appraisal, provenance, taxes, shares, wages, debt, insurance, reminting, Heat, reputation, and market demand produce understandable and non-exploitable outcomes?

**Verdict:** Core sale stack (provenance×demand×condition×urgency − taxes − sponsor share − wages) is intelligible and non-exploitable at formula level. Gaps: counterfeit seizure fraction, faction access gates, insurance not numeric in JSON.

## Scenario results

### HAVEN-CHARTER (10k runs × sponsor × party)

| Sponsor | Share | P4 lossRate | P6 lossRate | P12 lossRate | P6 mean trueProfit |
|---|---:|---:|---:|---:|---:|
| self | 0.00 | 0.29 | 0.32 | 0.39 | ~1615 |
| guild | 0.20 | 0.33 | 0.36 | 0.43 | ~1185 |
| bank | 0.30 | 0.35 | 0.38 | 0.47 | ~1023 |
| noble | 0.35 | 0.35 | 0.39 | 0.49 | ~889 |
| sovereign | 0.45 | 0.39 | 0.44 | 0.51 | ~679 |

Larger parties raise loss rate via wages — charter size is an economic decision, not free power.

### HAVEN-MARKET

Demand multipliers: glutted 0.75 → strategic 1.5 (**2.00×** spread). Deterministic and readable.

### HAVEN-COIN

Assay DCs/fees executable. **RULES_HALT:** counterfeit seizure/forfeiture fraction unspecified (sim 50% proxy).

### HAVEN-HEAT

| Start Heat | Complication rate | ≈Heat/6 |
|---:|---:|---:|
| 0 | 0.08 | 0.00 |
| 1 | 0.17 | 0.17 |
| 2 | 0.26 | 0.33 |
| 3 | 0.38 | 0.50 |
| 4 | 0.53 | 0.67 |
| 5 | 0.72 | 0.83 |
| 6 | 0.88 | 1.00 |

Rates track 1d6≤Heat but sit below naive Heat/6 when random bribes apply (floorWhileActive=1). H0≠0 rate is an artifact of bribing at Heat 0 hitting the floor — document that bribes should not be offered at Heat 0, or floor applies only while Heat was already >0.

### HAVEN-DEBT

| Term | Mean interest frac | Default rate |
|---|---:|---:|
| short | 0.055 | 0.039 |
| medium | 0.257 | 0.107 |
| long | 0.618 | 0.397 |

Interest cap 0.10/Opening clamps abusive rates (**DEBT-INTEREST-OVER-CAP**).

### HAVEN-FACTION

Labels −5…+5 applied; access gates inferred (**FACTION-ACCESS-THRESHOLDS** halt).

## Confirmed defects / gaps

1. Missing numeric counterfeit forfeiture.
2. Missing tabulated reputation→license/desk gates.
3. Insurance premiums not present as formulas in havenEconomy JSON.
4. Bribe floor interaction at Heat 0 needs clarification.

## Proposed follow-up

See suite proposed-patches file.

## Evidence limitations

No agentic faction negotiation; settlement math only. Labor status tags not fully simulated beyond wage rates.
