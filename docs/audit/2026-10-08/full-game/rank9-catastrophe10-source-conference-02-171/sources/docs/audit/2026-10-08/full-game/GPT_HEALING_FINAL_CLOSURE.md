# Bounded healing/death closure

Captured from completed Calibration Review reply.

I do not find another concrete defect inside the submitted bounded healing/death interface.

The two previous blockers are corrected in a way that matches the prior conferences, and the additional Spellform/ExcessLedger fixes are sound. This package can now receive bounded REVIEWED / reference-VALIDATED closure. The six ordinary spell objects may also move into the operational playtest overlay as operational-playtest drafts; that is not canon promotion.

Bounded healing/death disposition

REVIEWED / reference-VALIDATED for the submitted 153-source healing/death interface package.

The evidence now includes:

164 selected healing/death checks PASS
120 unchanged Core damage parity states PASS
150 control checks PASS
9,393 Speed invariant states PASS
98 custom-condition checks PASS
153 exact source integrity records PASS
original class/book/spell source objects unchanged. 
Pasted text
Blocked natural-20 recovery is now correct

death_save_with_survival() no longer independently interprets the prohibited natural-20 case. It delegates to the previously reviewed death_save_with_hp_prohibition() behavior and then layers only the new survival interfaces around it. 
Pasted text

The regression test now requires exactly the established result:

HP 0;
Stable;
successes/failures cleared;
d4-hour recovery deadline established;
regular-turn death-save marker preserved;
no Ritual Ward use spent. 
Pasted text

That removes the prior internal contradiction.

Passive Reserve regeneration exclusion is correct

excess_conversion_eligible() explicitly excludes:

Bloodthick Node;
Rapid Coagulation;
Regenerative Mutation;
Bio-Stabilizer as Bloodthick's modifier,

unless some future source expressly creates an exception. 
Pasted text

The tests correctly establish the intended distinction:

passive Reserve regeneration at full/Critical HP: actual gain 0, Reserve spend 0, conversion 0;
ordinary paid healing at full HP can still provide legitimate excess when its converter is otherwise legal. 
Pasted text

That solves the free-radiant-damage exploit without globally disabling overhealing mechanics.

Spiral III + Ward is correct

The phase remains when Spiral III's later fatal Wound is successfully replaced by an independent Ward. Since the creature never actually becomes Dead, the phase's death-ending condition never occurs. The Ward does not reset or extend the phase or refund Spiral's use. 
Pasted text

Spellform expiry correction is also sound

The Mage expiry's added failure now creates a pending death first and offers an eligible would-die replacement before Dead is finalized. A blocked-HP Ward properly produces Stable 0 and the normal recovery deadline. 
Pasted text
 
Pasted text

ExcessLedger rejected allocations are transactional

The revised ordering validates an over-allocation before setting internal-priority state, so a rejected conversion does not partially mutate the ledger. The added tests cover both quantity and priority-state preservation. 
Pasted text
 
Pasted text

I find the rest of the submitted interface internally consistent with the decisions already made: frozen damage metrics, floor/Wound ordering, Ritual Ward, direct death, zero-HP acting permissions, False Life V, Fate-Bound rerolls, two-pass healing, reducer commitment, Channel Life excess restrictions, causal healing ledgers, lethal-track collapse, resurrection history, identity deduplication, Soul Bind and suppressed-record cures. The guide accurately limits Time Loop to a participant snapshot interface rather than pretending the world/topology problem is solved. 
Pasted text

Six ordinary spells

All six may now be promoted from their inactive candidate file into the operational playtest overlay.

Their validator confirms:

all six complete operational objects are present;
preserved source identity and classAccess;
preserved ranks;
preserved minimum class levels;
preserved RP costs;
420 class/level access boundaries PASS;
none is currently active in the existing catalog yet. 
Pasted text

Individual dispositions:

Spell	Disposition
Stitch Fate	REVIEWED / reference-VALIDATED → approve operational-playtest promotion. Living dying-0 only; failure removal or direct 1-HP recovery; blocked recovery uses Stable-0 bridge.
Death Ward	REVIEWED / reference-VALIDATED → approve promotion. Positive-to-zero 1-HP prevention only; distinct from Ritual Death Ward.
Resurrection	REVIEWED / reference-VALIDATED → approve promotion. 8-hour NEW playtest window, viable remains, willing identity, 1 HP, persistent consequences retained.
Mass Resurrection Denial	REVIEWED / reference-VALIDATED → approve promotion. NEW 20-ft corpse-local concentration zone resolves the source's otherwise unusable instantaneous/ongoing conflict.
True Resurrection	REVIEWED / reference-VALIDATED → approve promotion. 7-day NEW window, body or bodyless formation mode, identity deduplication, actual soul/identity blocks retained.
Soul Bind	REVIEWED / reference-VALIDATED → approve promotion. Dying living target, CHA save, 60-second pending tether, 24-hour post-death identity block, no concentration, exact expiry and removal boundaries.

Their preserved access/rank/RP records are explicitly verified spell-by-spell in the submitted validation. 
Pasted text

For status tracking, I would record them after Codex promotion as:

Operational playtest drafts — REVIEWED / reference-VALIDATED. Not canon. Not human-balance-certified.

Exact closure statement

Healing/death bounded interface package: CLOSED as REVIEWED / reference-VALIDATED for the 153 supplied source records and selected reference interfaces. The six individually reviewed ordinary spell candidates are approved for promotion into the operational playtest overlay.

This does not close DD24, the remaining 131 tracked semantic matches, full Time Loop/environment/equipment/topology behavior, broader body/soul cosmology, numerical balance, human playtesting, or the game as a whole. 
Pasted text