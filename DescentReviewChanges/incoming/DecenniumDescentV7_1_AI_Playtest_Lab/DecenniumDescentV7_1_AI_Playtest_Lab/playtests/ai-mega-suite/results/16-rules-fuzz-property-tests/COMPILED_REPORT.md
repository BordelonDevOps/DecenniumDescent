# Rules Fuzz and Property Tests — Compiled Report

**Pack:** `16-rules-fuzz-property-tests`  
**Evidence level:** A (executable property / invariant fuzz)  
**Seed:** `71600`  
**Source hash (Gameplay Loop v1.1):** `2f3167ff71e5c9ad99278e3d72bce48298bb71b3b9d623e430eea2851bd76ab8`  
**Outcome:** FAIL on adversarial illegal-state detection scenarios; PASS on clamped resource/haven paths  
**Total transitions:** **100,000** (matrix minimum met)

## Test volume

| Scenario | Runs | Failures | Outcome |
|---|---:|---:|---|
| FUZZ-ACTIONS | 25,000 | 522 | FAIL |
| FUZZ-RESOURCES | 25,000 | 0 | PASS |
| FUZZ-EXPEDITION | 25,000 | 4,968 | FAIL |
| FUZZ-HAVEN | 15,000 | 0 | PASS |
| FUZZ-SEASONAL | 10,000 | 279 | FAIL |

## Source and fixture hashes

- Public Gameplay Loop v1.1 and `src/data/gameplay-loop.json` **match** on `encounterMath`, `opening` (2400/1200), and `expedition.maximumRoster` (12). No source-parity RULES_HALT.

## Results by scenario

1. **FUZZ-ACTIONS:** Encoded clamps hold for normal generation. Adversarial branch constructs &gt;1 Additional Action Slot states (**522** catches) — invariant flags them; companion must hard-reject.
2. **FUZZ-RESOURCES:** RP/Dissonance/HP clamps held for 25k transitions (null breach).
3. **FUZZ-EXPEDITION:** **4,968** `roster_over_max` catches when generator proposes party &gt;12. Pressure/Supply/Strain/Progress bounds held after clamp. Confirms roster cap must be enforced at charter UI / state write.
4. **FUZZ-HAVEN:** Sale formula non-negative/finite; sponsor shares in [0,1]; settlement step list present — 0 breaches.
5. **FUZZ-SEASONAL:** **279** `public_depth_leak` catches when public state claims depth &gt; Sixth Gate. Inheritance/rep clamps otherwise held.

## Rules halts

Total: **0** (parity clean). Coverage limitation noted: fuzz encodes a subset of prose rules.

## Confirmed defects (enforcement gaps)

1. **Expedition roster &gt;12** can be constructed — needs write-time rejection (`maximumRoster: 12`).
2. **Additional Action Slot overflow** can be constructed — needs action-economy hard cap.
3. **Public depth beyond Sixth Gate** can appear in public seasonal state — needs public/Director boundary guard.

## Suspected defects

None beyond enforcement gaps above (failures are intentional adversarial detections, not arithmetic NaNs).

## Null findings

- Haven settlement math and resource meters did not produce impossible values under clamp.
- Opening horn 2400/1200 consistent across public + src JSON.

## Proposed follow-up

- Companion validators for roster, AAS, and public depth (proposed patches).
- Expand fuzz to real class resource IDs from `class-core-mechanics.js` in a later wave (still patches only until approved).

## Evidence limitations

- Does **not** prove all prose rules are represented.
- Adversarial counts measure detector sensitivity, not table frequency.
