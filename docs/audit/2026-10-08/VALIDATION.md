# Validation record — 2026-10-08

| Check | Observed result | Limit |
|---|---|---|
| Whole original folder after relocation | 225,276 original files present with original sizes; no errors | Asset/dependency bytes were not individually hashed. |
| Original project bytes after all original-file repairs | 10,423 exact originals at current paths; 7 exact originals in pre-edit backups; 0 missing | Covers all 10,430 original project files. See [final preservation check](final_preservation_check.json). |
| DOCX/XLSX/ZIP package CRC | 219 package files / 98 distinct packages, no errors | Package integrity, not rendered layout review. |
| ZIP-member comparison | 6,811 members; 39 distinct contents without a loose-project byte match | Preserved and indexed; no archive deletion. |
| Main TypeScript | `tsc --noEmit --incremental false`, exit 0 | Type check only; no production build or browser workflow certification. |
| ReviewBible TypeScript | Same check with ReviewBible `tsconfig.json`, exit 0 | Type correctness does not resolve gameplay-state bugs. |
| ReviewBible gameplay validator | PASS | Existing structural assertions and selected boundary checks. |
| ReviewBible extraction parity | 8 worked cases and 672 combinations PASS; public/runtime JSON identical | Validates extraction coefficients and cap placement, not whole-game balance. |
| Frozen V7.2 public-canon validator | PASS: bestiary 65, tiers ≤6, public crafting | Applies to the lab. Main/ReviewBible still require deliberate runtime-boundary reconciliation. |
| New navigation | 51 local links checked, none missing at initial finalization | Later-added proposal links also checked separately. |

The frozen V7.2 lab was read and validated without rewriting its reports. Validators that write outputs were not run in the frozen lab. Original Word books were not edited or newly rendered in this pass. Copied Quickstart Word bytes are unchanged from the lab.

No human playtest, production deployment, numerical balance approval or full publication-layout review was performed. The readiness checklist records these outstanding tasks explicitly.
