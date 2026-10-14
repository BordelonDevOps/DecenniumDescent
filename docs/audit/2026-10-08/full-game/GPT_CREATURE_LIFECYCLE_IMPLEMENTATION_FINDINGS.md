# GPT creature implementation findings

Complete visible reply to browser-submitted CODEX_CREATURE_LIFECYCLE_IMPLEMENTATION_COMPACT.md. One correction required; not closure.

ChatGPT said:

The 105 targeted checks and 2,800 Ranger conversion states are meaningful evidence, and the submitted scope is correctly bounded rather than claiming whole-class completion. Source integrity is also separately reported as 100 exact class records plus 5 frozen supports. 
Pasted text
 
Pasted text

I find one concrete semantic blocker before REVIEWED / reference-VALIDATED. I do not find another blocker in the command ledger, Auto-Raise, Mage elite, Mirror-origin Echo, Reflective reservation, Druid dependency, or Wizard no-acquisition boundaries.

Blocker: resurrected Ranger Beast still exists as an available corpse

The tabletop guide has the right intended rule: the Ranger Beast is a real animal, leaves an ordinary surviving corpse on death, can later be independently resurrected, and then requires a new full bond ritual. 
Pasted text
 
Pasted text

The implementation correctly creates a real corpse on the Beast's first death:

Python
if c.life_kind=='ranger':
    c.state='dead'
    ...
    self.register_corpse(Corpse('body:'+ident,ident,'beast'))

Pasted text

However, when the same animal is subsequently independently resurrected and rebound, bond_ranger(... resurrected=True) replaces the dead Creature with a living one but never changes the existing Corpse.available state. 
Pasted text

Corpse currently defines available=True as the live corpse-eligibility state. 
Pasted text

So this sequence is presently possible:

Beast dies → body:animal.available == True → actual resurrection → full rebond ritual → animal is alive again → body:animal.available is still True.

That is semantically impossible and matters even though Beast bodies cannot feed Corpse Harvest. Corpse Gateway is part of this exact source packet and targets a visible corpse without consuming or altering it. A living resurrected animal cannot simultaneously remain a legal corpse anchor. 
Pasted text

Smallest correction

Keep the same physical body identity; do not create another corpse record.

Add an explicit physical-body state, ideally something like:

body_state = living | corpse | consumed/removed

or, minimally, make available represent “currently exists as a corpse.”

On accepted independent resurrection:

Plain text
same body identity
corpse.available = False
corpse is no longer a legal corpse target

On a later genuine Ranger Beast death where the body survives:

Plain text
reuse the same body record
corpse.available = True
do not create a fragment/new body ID

If the body was actually destroyed/consumed by some future legal source, do not reactivate it without that source explicitly reconstructing the body.

This preserves the anti-fragment decision while correctly distinguishing:

same physical body identity ≠ currently a corpse.

Required regression:

Plain text
death1 -> body:animal available
independent resurrection + rebond -> same record, unavailable as corpse
death2 with surviving body -> same record becomes available again
number of body identities remains 1

That correction does not require solving the broader corpse-cleanup system.

Command/attached-phase model: accepted

I find the attached command implementation consistent with the agreed model.

Ordinary command issuance commits the BA/offensive allowance and resolves once in the attached phase; invalid resolution receives no refund. Mage/Wizard regular-turn restrictions are represented in this packet's command procedure. Ghoul Lash produces two actual attack rolls inside one command/offensive allowance. 
Pasted text

The Auto-Raise design is also coherent:

first qualifying trigger automatically reserves;
reservations count toward cap;
corpse is not frozen;
failed resolution still spends the round opportunity;
killer destruction does not cancel;
creation-round action bar is absolute;
attached-phase checkpoint is non-turn bookkeeping;
closed checkpoint cannot produce an orphan reservation.

The guide captures that model accurately. 
Pasted text

I find no correction needed there.

Reflective Companion: accepted

The implementation now correctly treats Reflective Companion as a new bounded integration rather than pretending it belonged to the earlier 219-source control closure.

It has:

initial Charm without hard-denial expenditure;
one pending forced Action maximum;
issuance-round BA;
future-resolution-round offensive reservation;
hard-denial expenditure only upon actual Action replacement;
cancellation when Charm/capability/legality/hard allowance fails;
no invented fallback;
no duplicate attached turn.

The reservation/cancellation code matches those decisions. 
Pasted text

No blocker remains there.

Mirror-origin Echo: accepted

The implementation correctly treats the Beast as an origin rather than caster.

Preflight happens before mutation, and successful use spends:

owner's Action;
shared BA command;
RP;
record;
release cap;
Beast local round option.

It deliberately leaves the offensive companion allowance unused because the resulting effect remains the Mirrorsage's spell. 
Pasted text

This matches the guide's immediate-owner-Action procedure and permits the specifically reviewed extra-own-turn case only when genuine Action/BA/caps still exist. 
Pasted text

No correction needed.

Mage/Wizard identity and return: accepted

The implementation cleanly preserves:

original source owner versus controller;
dynamic Mage elite maximums;
same-asset Soulbound return;
source-specific minimum-1 half-HP return;
history/recharge/use preservation;
completed-LR full return without independently granting rest resets;
Wizard elite schema/cap without Wizard create/bind/return API.

The absence of Wizard elite acquisition remains a genuine evidence gap rather than an invented ability, which is the correct disposition.

Druid dependencies: accepted

The implementation correctly distinguishes:

independent Base Swarm Summoning;
Carrion form-dependent swarm;
Broodmother form-dependent pair;
Master of Vermin's profile substitution.

Ending a form does not silently kill an unrelated paid concentration summon. The source-instance dependency model is appropriate. 
Pasted text

Nonblocking engine-hardening note

SourceStats currently accepts M=0 and does not cap S at 4:

Python
integer(self.scale,'S',1)
integer(self.modifier,'M',0)

Pasted text

Under the stated integration contract, the caller supplies canonical stats, so I am not treating this as a blocker for this bounded source review. For the eventual production/video-game rules kernel, I would tighten it to the already-established global invariants (S 1–4 and M >= 1) so malformed callers cannot create impossible companion statistics.

Disposition

Current status should remain:

IMPLEMENTED CANDIDATE — one exact lifecycle correction required.

After the Ranger resurrection/body-state correction and a regression covering death → resurrection → second death using the same physical body identity, I see no other semantic blocker in the supplied implementation.

At that point the appropriate closure is:

REVIEWED / reference-VALIDATED — selected lifecycle, identity, companion-command, Auto-Raise, corpse-consumption, Mage elite return, Ranger Beast, Mirror Beast/Reflective Companion, Mirror-origin Echo, and Druid summon-dependency interfaces for the supplied 100 source roles + 5 frozen supporting paragraphs.

That closure must continue to exclude full Druid forms, full temporary-HP systems, all complete card effects, Wizard elite acquisition/return, general corpse decay/cleanup, natural Beast rest/Hit Dice, keen-sense specifics, remaining companion families, full condition/on-hit execution, balance, human testing, and the complete runtime/video game.
