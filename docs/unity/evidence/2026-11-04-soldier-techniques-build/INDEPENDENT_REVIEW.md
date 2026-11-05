# Schema29 Soldier tactical techniques — independent review

**Final review result:** no remaining actionable issue found in the read-only re-review of the corrected schema29 increment.

## Review scope

Two independent read-only passes reviewed attack-time effect capture/consumption, effect application/replacement/expiry, Recharge across the shared schedule, schema/version gates, initialization, source fingerprinting and the fixed ally roster. No tests were run and no files were edited by the reviewers.

## Findings and corrections

The second pass identified five issues, all corrected and re-reviewed:

1. **Schema28 restore compatibility.** The default Soldier build had started selecting schema29 and changing the content fingerprint. The existing constructor now remains schema28 with its original two-actor schedule and fingerprint. `SoldierCharacterBuildFixture.ForTacticalTechniques(...)` explicitly opts into schema29 and its source fingerprint.
2. **Ally actors treated as hostile.** The recorded alliance now excludes the companion from close-hostile ranged disadvantage, close-hostile Overwatch disadvantage, ordinary opportunity attacks against the other ally, and proximity-based implicit combat entry.
3. **Effect history validation accepted shifted or inconsistent records.** Validation now requires the exact next future owner/target slot; joins a consumed effect to the same attack revision, an attack before its expiry marker, and—when it is Covering Fire—a qualifying recorded ally target; and requires each successful card hit to have exactly one persisted rider.
4. **One-second ordinary handling could cross a tactical deadline without processing expiry.** Such inventory handling now fails closed when its one-second cost crosses a tactical-effect deadline, consistent with the existing timed-boundary guard.
5. **New Unity package files lacked metadata.** All four schema29 C# assets now have unique `.meta` siblings.

## Verification limits

The reviewers inspected source and persistence code but did not restore a historical schema28 save, execute schema29 state transitions, compare schema28 golden bytes, or run tests. The independent review does not replace those checks. Current evidence records a successful shared C# compile and a successful static package-structure validation; neither is Unity Editor compilation or gameplay validation.
