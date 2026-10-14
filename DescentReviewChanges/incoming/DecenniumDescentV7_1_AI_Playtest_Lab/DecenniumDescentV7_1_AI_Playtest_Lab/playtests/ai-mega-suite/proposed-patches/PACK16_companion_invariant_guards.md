# Proposed patch — Pack 16: companion invariant guards (DRAFT)

**Status:** proposed companion/code validators only — no rulebook number changes  
**Evidence:** Pack 16 — 100k transitions; failures are adversarial illegal-state catches

## Guards to add (companion / state write)

1. **Expedition roster:** reject `partySize > expedition.maximumRoster` (12).
2. **Additional Action Slot:** hard cap of **one** extra action from AAS sources per turn.
3. **Public depth boundary:** public seasonal/map state must not claim depth &gt; Sixth Gate (Director-only beyond).

## Tests

Re-run `tools/run_pack_16.py` after guards; expect FUZZ-EXPEDITION / FUZZ-ACTIONS / FUZZ-SEASONAL adversarial branches to fail closed (reject) rather than accept illegal states.
