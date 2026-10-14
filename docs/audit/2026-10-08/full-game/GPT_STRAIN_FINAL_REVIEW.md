# GPT exact Strain review and bounded disposition

Captured from the visible rendered reply.

The implemented Strain package is internally coherent and can close at its bounded namespace/recovery scope. I do not see a material contradiction in the supplied state transitions or tests.

The corrected source placement is right: Expedition Strain 2 carries both Speed -10 and -1 attacks/saves; level 3 adds expedition-check disadvantage and the Dash restriction. The guide now preserves that correctly. 
Pasted text

1. Dash endpoint — confirmed

The implementation now matches the intended rule:

Dash during the creature's own current regular turn excludes that current turn-end marker.
Dash at 1, current end 3 → lock endpoint 9.
Off-turn Dash at 4, preserved regular-end phase 3 → endpoint 9.
Out-of-initiative Dash at 4 → absolute endpoint 10.
Transitioning into/out of initiative does not re-anchor the existing endpoint. 
Pasted text

That fixes the earlier imprecise “strictly after Dash” wording. The important rule is now the next eligible regular-turn end, excluding the current in-progress regular turn when the Dash occurred during that turn.

2. RestHistory scope — confirmed

The implementation correctly distinguishes:

completion of an activity interval;
eligibility for a beneficial rest reward;
Rest Debt discharge;
Expedition Strain reduction;
Serum Strain recovery.

A safe qualifying Rest Watch can clear Rest Debt even when the 24-hour Long-Rest reward cap prevents another beneficial Long Rest, without resetting benefit clocks or Short-Rest counts. The Haven-care window can contain separately completed, non-overlapping sleep/recreation activities, while the helper does not pretend to provide supplies, active care, or inventory. 
Pasted text

The chronological-completion requirement is important and correctly reflected by the helper: contained Morale/Rest intervals must be processed when they finish, and the enclosing Haven window completes afterward.

3. Level-6 gain/collapse/death handling — confirmed

expedition_gain() correctly:

evaluates a positive unprevented gain whenever existing points + attempted gain reaches/exceeds 6;
stores no seventh point;
defaults to the Dead state;
permits explicit nonlethal collapse only when the triggering source says so;
allows a later ordinary gain against a living collapsed level-6 creature to kill it despite the storage cap;
leaves an independently dying 0-HP state intact under nonlethal collapse;
refuses to treat a gain as resurrection. 
Pasted text

Likewise, ordinary recovery never touches LifeState; maximum-HP recalculation cannot revive, heal, reset death counters, or create damage/Wound triggers. That boundary is sound.

One future cross-system question remains, but it is not a blocker here: an actual resurrection performed while the character still carries six Expedition Strain points will need the resurrection pass to specify whether that resurrection must first reduce/bypass the lethal track state. This helper correctly does not invent that rule.

4. Point recovery metadata — confirmed

The point-level model is appropriate:

ordinary_removable
removal_gate_met
source identity
unique point identity.

Long/Morale recovery removes a selected eligible point. Haven removes all eligible ordinary points. Blocked points remain. Lowering a collapsed character below six clears only the Expedition-collapse state, not unrelated Unconscious or life-state effects. 
Pasted text

No recovery replay issue is apparent in the supplied tests.

5. Namespace bindings — confirmed, with one scope wording nuance

The source registry functioning as a namespace reference rather than an effect trigger is correct. Binding Serum Tolerance to warrior.serum-strain does not grant immunity or modify the track by itself. Unknown/ambiguous references are rejected by bind_strain(), and exact source references are being hash-checked. 
Pasted text

A minor wording precision: expedition_gain() itself accepts a caller-supplied source_id; it does not internally call bind_strain(). That is fine because the package explicitly says callers establish source legality, but documentation should continue saying namespace lookup rejects unknown sources, not that every low-level transition helper independently validates the source registry.

This is editorial/scope clarity, not a mechanical defect.

6. Penalty projection — confirmed

track_penalties() correctly keeps the independent tracks separate:

Expedition 2 attack -1.
Expedition 2 save -1.
Serum 3 adds another save -1.
Serum and Expedition flat Speed reductions coexist before Exhaustion halving.
Expedition 5 reports Incapacitated and tactical-movement prohibition without rewriting actual Speed to zero.
slow travel is exposed as one 1/2 multiplier for the later travel system rather than repeatedly applying it internally. 
Pasted text

The maximum-HP helper also correctly multiplies rational factors and floors once, with the Critical Wound healing ceiling remaining downstream.

One small documentation correction

The level-6 source says “death or permanent collapse.” The current playtest makes its nonlethal collapse recoverable through qualifying Haven care/explicit treatment. That was an intentional authored resolution, but the guide should keep emphasizing that this is a NEW operational replacement for the otherwise non-executable source phrase, rather than implying that “permanent collapse” itself sourced a recoverable state.

The current “NEW deterministic interpretation” label largely does this already; I would simply preserve that wording in any player-facing condensation.

Bounded disposition

warrior.serum-strain / expedition.strain namespace, selected penalties, gain/cap transitions, Dash lock, maximum-HP interaction, and generic recovery bookkeeping: CLOSED as REVIEWED and reference-VALIDATED within the declared scope.

Evidence reported in the candidate:

101 total checks
71 transition checks
30 exact namespace/source checks
4,949 maximum-HP invariant states
source integrity over the supplied Warrior engines/cards, campaign sections, and Core passages. 
Pasted text

This does not close the wider Expedition/travel/rest systems, class resource semantics, all future Strain references, resurrection interaction, DD16 custom-state coverage, or human balance.