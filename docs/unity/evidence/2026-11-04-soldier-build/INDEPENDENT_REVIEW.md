# Schema28 Soldier build independent review

**Result:** No remaining actionable defect found by read-only review.

**Scope reviewed:** schema28 persistence/version gates; Soldier loadout fixture validation; build and Shield Trained source bindings; regular-start stationarity reset; Shield Trained's limited repeating-crossbow attack hand exception; starter stock replacement; shared AC, speed, saving-throw, damage-reduction, and movement integrations.

**Findings verified:**

- The selected Soldier build and shield-stationarity records are required where expected, and schema27/28 fixture keys bind to the current decision document Git blob and SHA-256.
- Shield Trained's exception does not provide generic hand availability. Reload still requires an actually available hand.
- Replaced inherited ration, water, and actor-waterskin records are removed through guarded initialization; the retained companion waterskin remains represented.
- Stationarity resets at the actor's regular start, and the bounded shared integrations reviewed are consistent with the documented fixture limits.

**Limitations:** This was a source review, not a runtime execution. No tests were run, historical save bytes were not compared, and Unity import/compilation and gameplay were not evaluated. The compile-only result is recorded separately in [COMPILE_RESULTS.json](COMPILE_RESULTS.json).
