# Daily Provisioning and Expedition Strain — TEST_ONLY Contract

**Date:** 2026-11-08

**Scope:** First fixed-roster daily provisioning profile for the MGT-03 C# simulation increment.
**Authority:** TEST_ONLY implementation completion. This document does not promote the provisional campaign overlay into Core or release authority.

## Pinned source requirements

- `DescentReviewChanges/ReviewBible/docs/mechanics/expedition/EXPEDITION_PLAYER_BOOK.md`, source revision `46a4d52728ee6956f0bebcb5d2103ffd5bc67ba4`, blob `466871fc128dc5f06043a874da2b9c1d94ed80a5`: FL-03 one elapsed campaign clock, eight-hour Watches; FL-04 actual recipient/lot consumption, ordinary Small/Medium daily demand of 2 lb edible food and 8 pints potable water, one total Expedition Strain per recipient/day for any food/water shortfall, and settlement at canonical 24-hour endpoints. The epoch is not stated.
- `DescentReviewChanges/ReviewBible/docs/mechanics/STRAIN_PLAYTEST.md`, same revision, blob `7005aaf9558f0ce4f445ffe982dfa9b6f36c8ee4`: source-qualified `expedition.strain` points and cumulative level effects; level 1 initiative/Expedition-check penalty, level 2 speed/attack/save penalties, level 3 Expedition-check disadvantage and Dash restriction, level 4 effective maximum HP factor, level 5 incapacitation/movement restrictions, and level 6 endpoint. The campaign overlay remains provisional. The level-6 deterministic endpoint and recoverable collapse text are explicitly labeled NEW interpretations in the candidate.
- Existing authority: `RuleClock` is the shared rational elapsed clock; `IntakeRecord` identifies actor, lot, reservation and interval; `WorkLedger` reservation `ConsumedAmount` is the consumed quantity authority; `WorldScheduleRecord.Origin` is an initiative calendar anchor and is not a provisioning epoch; `ActorCharacterRecord`, `ActorLifeRecord`, conditions, movement, commands, RNG and receipts remain their existing authorities.

## Codex/GPT consensus

The source leaves two procedures unspecified. After review in **Unity Rules Engine Development**, GPT proposed a bounded TEST_ONLY completion; Codex concurred; GPT confirmed there was no blocker and that MGT-03 remains the next mapped module.

1. **Day origin:** `CanonicalDayOrigin = RuleTime.Zero` belongs to immutable, fingerprinted provisioning-profile content. It is distinct from `WorldSchedule.Origin`; no duplicate mutable snapshot field is needed for this fixed profile. Restore must resolve the exact bound profile. Day `n` is `[origin + n×86,400s, origin + (n+1)×86,400s)`. Watches divide the day into three consecutive eight-hour intervals. Encounter entry/exit, assignments, travel, saving/loading and Haven transitions do not reset it.
2. **Settlement:** accrue actual intake through each endpoint, then persist once-only actor/day settlement with causal consumption evidence. Intake spanning midnight contributes its actual portions to both days. Later commands at the same timestamp cannot satisfy a closed day. Every admitted clock advance settles every crossed endpoint, including multi-day advances. A profile enrolls its fixed roster at origin; it must not retroactively assess unsupported historical days.
3. **Roster and checks:** the initial profile has a fixed roster from origin; mid-day enrollment and changing diets remain gated. The explicit, versioned Expedition-check registry initially contains only stationary Map Route completion checks and route-reconnaissance completion checks. Location, assignment, skill, or use of a generic `TaskCheck` does not imply membership. Other procedures (including repair, mining, harvesting, research, Hide/Search and treatment) remain unaffected absent an explicit versioned addition. Apply level 1's −1 once and level 3's one disadvantage source to registered checks. Initiative, attacks and saves retain their separate printed scopes.
4. **Level 6:** preserve the candidate's NEW/provisional authority. Ordinary provisioning shortfalls do not qualify for recoverable collapse; the ordinary endpoint applies. This implementation does not promote the new collapse interpretation.

### GPT's actual confirmation

> “Confirmed. Codex/GPT consensus is reached on this exact TEST_ONLY contract. I see no blocker.”
>
> “Day origin: `CanonicalDayOrigin = RuleTime.Zero` belongs to immutable, fingerprinted provisioning-profile content. It is distinct from `WorldSchedule.Origin`; no duplicate mutable snapshot field is needed. Restore must resolve the exact bound profile.”
>
> “Settlement: use the stated half-open day intervals and persist once-only recipient/day settlement with causal consumption evidence. Late same-time intake cannot alter a closed day.”
>
> “Enrollment: the fixed roster starts at the origin. ‘No retroactive settlement’ excludes activating this policy over unsupported historical saves; an admitted clock advance must still settle every endpoint it crosses, including multi-day advances.”
>
> “Check classification: the versioned registry initially contains only stationary Map Route and route-reconnaissance completion checks. Other procedures remain unaffected by the expedition-check modifier. Initiative, attack and save penalties retain their separate scopes.”
>
> “Level 6: preserve the candidate's NEW/provisional authority. Ordinary provisioning shortfalls do not qualify for recoverable collapse.”
>
> “MGT-03 daily provisioning and executable Expedition Strain remains the selected next module. Record this concurrence, implement the agreed scope, and provide the commit and verifiable acceptance evidence here for review before moving to the next module.”

### Initiative integration clarification (2026-11-08)

The selected host uses an authored fixed initiative order and has no executable initiative-roll command or initiative-resolution record. GPT confirmed: “An authored initiative order is not an initiative roll.” The implementation adds a pure, source-qualified initiative modifier projection (0 below Expedition Strain 1, −1 from level 1 onward) but does not draw RNG, alter the schedule, or connect it to a nonexistent roll. Acceptance verifies this projection and proves Strain gains preserve the established order through save/restore and deterministic replay. Initiative rolling and application remain explicitly unsupported. Attack and saving-throw penalties must execute through the existing paths.

GPT also resolved the point-recovery metadata: supply-shortfall points are `ordinaryRemovable=true` and `removalGateMet=false` at creation. FL-04 says the unsupported day blocks Strain removal. A later day, new supply, or completed rest does not automatically clear this gate; a sufficient provisioning plan must actually be available and maintained. This does not block gains or their effects. Keep the daily settlements because the restriction applies to the recipient's removal eligibility, not only this point; recovery remains outside MGT-03.

## Module responsibilities and authoritative records

- Boundary processing uses `RuleClock` and the profile's immutable epoch; it must not reset or substitute the initiative calendar.
- Physical food/water remain in `WorkLedger` lots. Consumption and provenance remain in `InventoryLotRecord`, `IntakeRecord`, and reservation ledgers. New settlement records are an attributed accounting result, not inventory.
- New source-qualified Strain points and actor/day settlements are persisted with the smallest new schema increment; existing character facts, life facts, conditions, movement, RNG and command receipts remain authoritative for their own domains.
- `TEST_ONLY` content and its roster/demand profile remain isolated in the Laboratory host and fingerprint. Production rules are not inferred from this profile.

## Acceptance criteria

1. Pin and validate the two source snapshots and this GPT consensus. Existing saves at schemas 1–61 retain their byte layout and restore semantics; provisioning activates only through the exact new profile, with no back-assessment of historical time.
2. Consume exact ordinary food/water lots progressively and attribute quantity by intersection of the recorded intake interval with each half-open day. Use the existing rates and `WorkLedger` quantities; do not debit stock twice.
3. At every crossed endpoint, once per enrolled recipient and day, persist required amounts, actual credited food/water, and causal intake/lot/reservation evidence. Food and water deficits together create only one daily source-qualified point. Same-time later intake cannot rewrite settlement. Repeated settlement rejects or is idempotently recognized without adding points twice.
4. Reuse one shared policy projection for cumulative Expedition Strain. Demonstrate registered check modifiers, distinct attack/save penalties, speed/Dash and action permissions, effective HP ceiling, and the source's ordinary level-6 death endpoint in the admitted host. Verify the initiative projection returns 0 below level 1 and −1 from level 1 onward, leaves an established order unchanged across save/restore/replay, and consumes no RNG or other state. Report initiative rolling/application as unsupported. Serum Strain and Core Exhaustion remain independent.
5. Runnable connected scenario: use the shared clock while the lead explores and a companion performs management work; two fixed recipients consume actual lots, one fully supported and one short; include intake spanning the boundary, a save just before it, whole versus split/restored advances, multiple-day catch-up, late same-time intake, duplicate-settlement rejection, registered Map Route/recon checks, an unregistered procedure check, and consequences through each reached level. Snapshot state and command replay must match exactly across equivalent paths.
6. Compile with warnings as errors; run relevant full and focused regressions, package validation, source-binding audit and historical-save fixtures. Retain logs/results/hashes. Unity import/runtime checks remain deferred.

## Explicit limitations and open dependencies

- This profile models only its fixed enrolled TEST_ONLY roster and authored ordinary 2 lb / 8 pint daily demand. It adds no `Size`, diet, membership or advancement fact to `ActorCharacterRecord`.
- Mid-day joins/leaves, size or form change, special diets, mounts, Haven/home support, oil/sundries logistics, rest benefits/debt/recovery, Strain removal, other Strain sources, generic Expedition-check membership, and production promotion remain outside this module.
- The candidate's NEW recoverable-collapse interpretation, resurrection while at level 6, and human balance are not implemented or promoted here.
- Unity gameplay integration, scenes, Play Mode and builds remain deferred.
