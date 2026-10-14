# GPT remaining turn-end phase finding

Captured from the visible rendered Calibration Review reply.

I found one remaining concrete timing defect. The four previously identified defects are fixed, and the binding-role cleanup is sound, but I would not mark this bounded package REVIEWED until this clock issue is corrected. The candidate otherwise reports the expected 123 interface checks, 9,393 Speed invariants, and exact 219-source/binding validation. 
Pasted text

Remaining material defect: ordinary turn-end expiries are still phase-0

The new ClockMarker correctly fixes effects created and expiring during the same end-turn timestamp:

application/resolution phase 10;
expiry phase 20;
later event phase 30. 
Pasted text

But ordinary end of next turn, source-next-end, target-next-end, and bare hostile N-round deadlines are still represented elsewhere as bare integer timestamps. clock_marker(9) becomes:

ClockMarker(9, 0)

Meanwhile a normal end-turn effect-resolution query would be something like:

ClockMarker(9, 10).

SpeedRecord.operative() then evaluates:

(9,10) < (9,0) == false

so the effect is already expired before the end-turn resolution phase. 
Pasted text

That conflicts with the combat ordering we already established: effects ending at the end of a turn expire after that turn's end-triggered effects, damage, saves, and maintenance.

Exact fix

All turn-end endpoint constructors/callers should normalize to:

ClockMarker(deadlineSeconds, END_EFFECT_EXPIRY)

for:

target next regular end;
source next regular end;
Nth future target regular end;
any explicit “until end of X's turn” endpoint;
Balanced Elements' computed following_target_end.

Turn-start expiries should remain an earlier phase, because the combat procedure explicitly expires start-ending effects before the rest of start-turn processing.

Absolute elapsed-time deadlines can remain phase 0 unless the source ties them to a turn event.

So for example:

Plain text
target-next-end = ClockMarker(9, 20)

Then:

at (9,10) → still active;
at (9,20) → expires;
at (9,30) → gone.
Tests to add

At minimum:

ordinary target-next-end -10 slow is operative at (9,10);
expires at (9,20);
absent at (9,30);
source-next-end behaves identically;
bare hostile 2-round target-end deadline gets phase 20;
Balanced Elements receives/returns a phase-20 following-target endpoint, not bare integer 9;
a stronger record expiring at target-end remains the effective record through phase 10, then exposes the weaker record at phase 20.

Your current phased tests prove the current-turn bridge, but not the ordinary future-end case. 
Pasted text

The four prior fixes otherwise pass review

Guiding Star: the pre-roll/post-roll split is now correct. begin_ally_attack() supplies and consumes +2 before the attack roll, while a mark-specific token binds later hit resolution; duplicate/foreign tokens reject, suppression does not spend the initial entitlement, and a miss preserves the separate hit rider. 
Pasted text

Fallback slowed metadata: the missing Oracle/Paladin fallback records are now tagged conditionally, while Spiral Opens correctly separates the player Speed-0 branch from NPC Forced Echo. 
Pasted text

Stars Revelation Mastery: STATE → HOOK is correct. The actual Guiding Bolt remains the possible applicator, while Mastery modifies/authorizes the enhanced slow only when that option was selected. 
Pasted text

Modifier/reference roles: the Flask wrapper no longer pretends to apply Burn only; Arch Elemental Mastery uses modifier links; ordinary Ray of Frost/Frost Arrow have the narrow reviewed elemental classification; Fusion records its NEW missing endpoint bridge; Cascade preserves source-clock wording. 
Pasted text

Carrion Conductor's cross-owner corpse-family lock also remains correct, as does the separation between cures of present Staggered records and active-effect eligibility hooks.

Disposition

IN REVIEW — one material clock normalization remains.

After future turn-end deadlines are represented as phase-aware end-expiry markers and those lifecycle tests pass, I would close the following exact scope as REVIEWED / reference-VALIDATED:

The supplied 219-source control-state interface package: source-qualified Speed arbitration and refresh/suppression; supplied control/mark/restraint clocks and rider consumption; Staggered classification/removal; reviewed elemental-control membership and Balanced Elements interface; selected curse/disease reader/removal interfaces; Moment's Pause initiative-delay interface; Hypermutation Speed floors; and the 219 supplied application/modifier/reference bindings.

That still would not close DD16/DD18, complete card execution, disease/curse catalogs, death/replacement/resurrection, unsupplied object/tether durability, or the all-source semantic remainder.