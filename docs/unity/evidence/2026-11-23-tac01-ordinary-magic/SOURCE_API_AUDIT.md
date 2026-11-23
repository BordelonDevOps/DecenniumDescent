# Ordinary magical activity: preimplementation source/API audit

Baseline: Engine `cf02edf6154f79e6d3a7bc80f54dad4b122bde34`; accepted runtime `3c5135ae0d664d79528fff1f2676fae2198beb28`. Owner resumed the full C# goal on 2026-11-23. **CAL-01–05 remain open. No runtime design is approved by this audit.**

## Confirmed source and integration constraints

- Original ReviewBible `CLASS_PLAYTEST_RULES.md` lines15/17/47–49 separates ordinary allowances, recharge, spell strain and idle/Grounding reduction. Regular no-magic turns lose1 Dissonance; paid Grounding substitutes PB, never both; encounter closure resets nothing.
- `COMBAT_ACTION_PLAYTEST.md` lines29/47–66 retains regular initiative slots, original effect markers and event ordering.
- Shared-world decisions explicitly put slot End at the next actor Start. TAC-08 approved P4 line70 applies idle/Grounding there. The successor needs an explicit prospective amendment; omission of a zero-Dissonance End record is not evidence of an open interval.
- Cleric source Radiance is once per owner turn; protected vent is once per regular turn and requires real spending of at least2 Conviction. A mode/epoch/accounting segment must not manufacture another entitlement.
- A paid outside Consecrate at s+3 retains future owner-Start recharge s+6/+12/+18 and absolute outside expiry s+21. Activity accounting must not move either deadline. Arcane Ward retains its actual next-owner-Start deadline.

## Actual seams that prevent a guard-only fix

1. `SharedSpellCasting.CurrentCastingTurn` binds a normal owner Start or exact carried admission. `CastingActionFailure` requires the owning processed slot. Activity, cast and focus records/validators restrict historical own-action timestamps; some constructors forbid carried identities.
2. `NextCastingBoundary` and `SettleCastingTime` currently settle at epoch.Start(local+1). Strain reconstruction independently verifies every End. Zero Dissonance/no activity allows sparse omission, not extra legal time.
3. `SharedRadiance.OwnTurnFailure`, the paid cure factory and `ClericSettlementValidation` impose their own owner-slot/frequency checks. Invocation uses both Radiance and casting gates. Widening only the front-end command would fail downstream validation.
4. Consecration zone/recharge, Invocation and Radiance records require real nonnegative owner-Start identities. Current Bishop codec does not carry an admission field. New versioned representations must preserve actual carried provenance; no future Start may be substituted.
5. Arcane Ward currently derives expiry from localStart+rosterCount; a carried -1 cannot use that expression. Sanctuary also uses `SpellTurnIdentity` for once-per-attacker-interval caching, so a broad reinterpretation would affect unrelated behavior.
6. Ground/Aura healing intermediates are command-bound; preserve base Rite → Ground → Radiance → Aura and actual capped values.
7. `PostRecoveryOldEndsSettled` and `FerryOldEndsSettled` require completed old actor slots and, where needed, corresponding casting End records. A new pending outside accounting interval must receive an explicit transition disposition; do not silently bypass the complete admission contract.
8. Encounter admission copies actual spending into carried `WorldIntervalRecord` entries before processing the actual new actor0 Start. Current ownership comes from `WorldTiming.ForActor`, not any retained older epoch.
9. Real closure uses `AdvanceTo` to finish the outgoing tactical slot before setting InventoryCombat=false and retaining the closed encounter. This creates the important already-settled-End transition case.
10. The main `AdvanceTo` scheduler calls `SettleCastingTime` before inventory/condition work and subsequent interval/life/epoch refresh. The direct ordinary handling path also invokes settlement before refresh. Both paths and sparse advancement must obey the new contract exactly.

## Required adverse timeline resolutions

| Situation | Why the contract must decide it |
| --- | --- |
| Dissonance3 at s; idle old End s+2 makes2; magical Consecrate s+3 | Adding magic to the settled old identity contradicts its history. Undoing reduction is prohibited. |
| Dissonance0 yields no End row | Legality cannot depend on a sparse-history optimization. |
| Idle reduction3→2 already happened; Grounding later with PB2 | Applying another full PB would grant both idle and Grounding for the same accounting entitlement. A paid-but-unspecified result is also unacceptable. |
| New epoch origin4, actual owner Start6, carried Action available at5 | This has no new local owner Start. Preserve admission and old allowance origin; no made-up future identity. |
| Genuine entry after old slot End but before old next owner Start | Pending accounting, transferred allowances and original deadlines must reconcile without reset, lost activity or duplicate reduction. |
| Effect/rest/condition/work/refresh ties | Specify one ordering through both scheduler paths and demonstrate whole-versus-partitioned equivalence. |

## Independent review

Existing reviewer `/root/review_consecration` independently inspected the pinned source and current implementations under development brief §14. It confirmed these constraints and downstream couplings, and identified outside accounting tied to the real allowance interval as a possible investigation direction, **not a complete or approved policy**. Its specific unresolved issue is the suffix after a tactical End has already settled. No files, builds, gameplay tests, pushes or approval were produced by that review.

Actual GPT consultation is in Unity Rules Engine Development Part3, request `0c58c61a-7c35-4fea-a802-1af85053af00`. Retain its actual response and resolve the complete amendment before runtime edits. Existing acceptances and 49 workstreams/120 dependencies/100 completion obligations remain authoritative.
