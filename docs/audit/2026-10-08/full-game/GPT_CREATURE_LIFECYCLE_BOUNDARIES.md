# GPT creature lifecycle boundary reconciliation

Complete response to CODEX_CREATURE_LIFECYCLE_BOUNDARIES.md;100 source roles plus5 frozen supports, source-audited/draftable, not implemented closure.

The conflicts can be reconciled without adding new abilities or importing unsupplied creature rules. The following should control implementation.

## 1. Reflective Companion and the hard-denial guard

The correction is necessary: `mirrorsage.base.charm-creature` / `mirrorsage.engine[4]` were **not** part of the previously closed 219-source control register.

Apply the frozen hard-denial rule directly.

**NEW source-specific integration — Reflective Companion compulsion:**

On the initial failed save:

- apply the printed Charmed relation and concentration/duration;
- register the creature as the temporary Reflective Companion;
- this does **not** itself spend the hard-denial allowance.

While the effect remains active, the Mirrorsage may use the shared BA companion command to force **one Action total** from that creature if that Mirrorsage/target hard-denial allowance is still unused.

When that forced Action actually replaces the creature's normal Action:

- spend the Mirrorsage→target hard-denial allowance;
- it may use only the permitted ordinary attack, capped at `S d6`;
- the command may include source-legal accompanying movement for that one forced command;
- unique powers remain unavailable.

After that hard allowance has been spent:

- no further forced attack;
- no forced Dodge;
- no forced movement;
- no other commanded Action;
- no invented soft fallback.

The remaining effect is only the actual printed Charmed relationship, repeat-save procedure, companion-slot relationship, and other explicitly printed soft effects. The creature otherwise acts with its own agency subject to Charmed.

If a queued forced Action never actually occurs because the charm ends first, the hard-denial allowance is **not** consumed.

This brings Reflective Companion under the same character/target/encounter hard-denial ceiling without pretending it was previously source-reviewed.

---

## 2. Command issuance versus resolution

### Ordinary standard/Mage/Wizard companions

Use an attached companion phase.

During the owner's **regular turn**:

1. owner chooses the companion;
2. spends the BA;
3. selects the printed command/mode and currently legal target information;
4. records the command.

After the owner's regular turn finishes, that companion receives **one attached companion phase immediately after the owner**.

During that phase it:

- performs its permitted commanded movement;
- resolves its one commanded action.

It does not gain an independent additional turn.

At resolution, recheck:

- companion still exists;
- it is capable of acting;
- target remains legal;
- required range/LOE remains legal.

If intervening state makes resolution impossible, the command is lost without refund. No replacement command is granted.

Once validly issued, later owner incapacitation/removal does not by itself revoke the order unless:

- the companion/effect depended on concentration/source survival; or
- another exact source ends it.

Owner removal/reordering never changes previously registered virtual companion markers.

Uncommanded companions use only the printed defensive move/Dodge behavior.

### Reflective Companion

It does **not** receive this attached companion phase because it is the original creature and retains its own initiative.

A valid BA command instead reserves its **next future regular Action slot**.

If its regular turn is still upcoming in the current numbered round, the forced Action resolves there.

If its regular turn already occurred, it queues to its next regular turn, provided the control still exists.

It never receives a duplicate turn.

**NEW reservation rule:** a queued offensive Reflective command reserves the owner-wide offensive-companion allowance for the numbered round in which that target Action will resolve. Another companion cannot consume that reserved offensive allowance first.

If the charm ends before resolution:

- reservation clears;
- command payment remains spent;
- hard-denial allowance remains unused because no Action was actually taken.

Repeat saves occur at the creature's actual regular turn end.

---

## 3. Mirror-origin Echo targeting and timing

Confirm the targeting rule.

The Mirrorsage must still satisfy the frozen targeting requirement:

> perceive the target, be otherwise eligible to target it, and obey applicable source restrictions.

“Perceive” is not automatically “see.” Valid nonvisual senses can qualify where the general rules permit them.

The Beast grants **no remote sensory feed**.

For a Beast-origin Echo:

- range is measured from the Beast;
- line of effect is measured from the Beast;
- owner still needs ordinary legal target perception.

### Echo execution timing

This requires a narrow source-specific exception to the ordinary attached companion phase.

**NEW Mirror-origin execution rule:**

The Echo Release resolves as the **Mirrorsage's Action during the Mirrorsage's own turn**, because:

- it remains the owner's spell/release;
- the owner supplies the Action;
- the owner owns Dissonance/Refrain/concentration/release cap.

The required BA companion command authorizes use of the Beast as origin but does **not** delay the spell into a separate Beast action.

Therefore:

1. validate Beast active/eligible;
2. validate record/release cap;
3. validate owner perception;
4. validate range/LOE from Beast's **current position**;
5. validate Action, BA, RP;
6. commit all costs;
7. resolve immediately.

The Echo-origin command grants **no additional Beast movement before the release**. It also gives no later commanded attack/action that round.

If the transaction fails before commitment, nothing is spent. Ordinary miss/save/outcome after commitment gives no refund.

---

## 4. Echo versus offensive companion allowance

A Beast-origin Echo does **not** consume the owner-wide offensive companion allowance.

Reason:

- BA companion command is spent;
- but the resulting damage/control is the **Mirrorsage's spell**, not a companion attack/control action.

This applies to both damaging and support Echoes.

Therefore, after Beast-origin Echo:

- shared BA companion command is spent;
- shared offensive companion allowance may remain unused.

A later triggered Gadget Sync may use that unused offensive allowance if all of Gadget Sync's own trigger/cost requirements are satisfied.

There still cannot be another BA companion command.

Radiant Mirror Beast retains its source-local lock:

> attack **or** paid heal **or** Echo origin that round.

That local lock applies regardless of whether the owner has another explicit triggered companion effect.

---

## 5. Ghoul Lash

Confirmed.

“TWO copies of its normal damaging attack” means:

> **two actual independently resolved attack rolls** using that minion's ordinary printed attack profile.

Each attack independently:

- rolls to hit;
- can hit or miss;
- can naturally crit under the ordinary attack rules;
- resolves its own damage.

They are not numerical damage copies of one stored attack event.

Ghoul Lash is the expressly priced exception granting two attacks inside:

- one BA command;
- one offensive companion allowance.

It does not create two commands.

Auto-Raise remains once per owner/round, so even if both attacks kill eligible creatures, at most one Auto-Raise opportunity occurs.

The frozen numerical-copy prohibition must not erase this explicit source behavior.

---

## 6. Auto-Raise queue and failure

First correction: engine[20] is written as an automatic trigger, not a “may.”

There is therefore **no voluntary decline of an otherwise qualifying first kill**.

The first qualifying killing blow that round automatically attempts reservation.

### Trigger

At the killing blow:

1. killer must be owner's standard undead;
2. body must presently satisfy creature-type eligibility;
3. owner has not used/reserved Auto-Raise this numbered round;
4. active standard minions + reserved slot must be below 3;
5. reserve corpse ID;
6. reserve one standard-minion capacity;
7. snapshot killer's mechanical minion type.

This spends that round's Auto-Raise opportunity.

If the later raise fails, the opportunity remains spent.

### Creation-round bar

The resulting minion **cannot act at all during its creation numbered round**.

That includes:

- no voluntary movement;
- no Dodge;
- no support action;
- no attack/control;
- no Reaction.

Passive defenses, conditions and expiry clocks still exist.

### End-turn resolution

At the current regular turn's end:

- finish immediate death/destruction responses;
- process already-due end damage/save events in stable application order;
- then process queued Auto-Raise reservations in stable application order;
- then perform ordinary end-ending expiries.

The reservation does **not** freeze the corpse.

If another legal earlier event consumes/removes it, Auto-Raise fails.

If killer is destroyed/expired before resolution, the already-created reservation remains valid.

If capacity somehow becomes unavailable despite the reservation, do not exceed cap; resolution fails.

### Kill during end processing

If the qualifying killing blow occurs during the ordinary due-damage/trigger portion of that same end marker, it may enter the still-open Auto-Raise queue and resolve at the Auto-Raise checkpoint.

A purely administrative event occurring only **after** that checkpoint does not reopen the finished turn-end queue.

No dismissal is automatically performed to manufacture capacity.

---

## 7. Standard-undead duration and source removal

**NEW standard-raised lifecycle integration:** an Auto-Raised standard undead uses the same standard raised-minion endpoint as Corpse Harvest:

> until destroyed, dismissed, or the owner's next completed long rest.

It is not a frozen-standard-companion one-minute summon.

Corpse Harvest and Auto-Raise share the same three-standard-minion population.

No supplied source says owner:

- incapacitation;
- unconsciousness;
- death

automatically ends already-existing standard undead.

Do not invent such an ending.

If the owner cannot command them, they follow the supplied uncommanded defensive behavior until some actual source endpoint removes them.

A reservation occupies capacity but does not lock the corpse against another legal consumer.

An expiring/destroyed killer does not cancel an already-triggered reservation.

Raised/summoned remains never become a new eligible corpse-farming source under the anti-farm rules.

---

## 8. Ranger Beast injury, corpse and rebinding

Correct: acquisition is **not** missing.

The supplied card already gives:

- Ritual;
- 4 RP;
- 1 hour;
- touch;
- willing/tamed eligible Beast;
- 1/long rest.

Only the campaign process of finding/taming/willingness is outside this lifecycle procedure.

### Zero HP

The earlier ruling remains explicitly **NEW Ranger-specific integration**:

> a bonded Beast reaching 0 HP dies immediately as a companion.

This is not a generic law for all living creatures.

Because this is a real bonded Beast rather than a conjured token, it leaves its ordinary real corpse unless the actual cause/source destroys/removes the body.

Death ends the Beast Companion bond.

If some separately legal resurrection later restores that same animal:

- it returns according to that resurrection source;
- it is no longer automatically the bonded Beast;
- a new full Beast Companion ritual is required;
- that rebond cannot occur until the actual completed-long-rest requirement has been satisfied.

No free animal and no free rebond healing.

### Initial wounded-state conversion

Use a deterministic **NEW profile-conversion rule**.

For the actual living Beast immediately before bonding, record:

`oldCurrentHP / oldMaximumHP`

Then create the bounded Beast maximum:

`newMax = max(1, 2 × Ranger level + actual WIS modifier)`

and set:

`newCurrent = max(1, floor(newMax × oldCurrentHP / oldMaximumHP))`

for a living eligible Beast.

Thus:

- previously healthy Beast → full bounded HP;
- wounded Beast → proportionally wounded;
- bonding itself is **not healing**;
- no healing trigger occurs;
- conditions, disease, poison, injury provenance and other legal ongoing state remain.

This is profile conversion, not importing the creature's old combat stat block.

A wounded bonded Beast cannot be rebonded/resummoned merely to reset the ratio.

---

## 9. Mage elite destruction and return

Destroyed Mage Lich elites remain owned bound assets and continue occupying:

- their one-of-each identity;
- the maximum-three elite asset cap.

Destruction cannot permit binding a duplicate Boneflayer/Dreadblade/Wraithbound.

Soulbound Ritual returns the **same asset and same companion instance identity**.

It preserves:

- command/offensive ledgers;
- spent independent uses;
- recharge clocks;
- still-applicable ongoing effect records;
- identity/provenance.

It changes only what the card expressly changes:

- destroyed → returned;
- HP → half current legal maximum;
- gain printed temporary HP.

### Half maximum at max 1

Do not import the machine-reconstruction rule.

Adopt a distinct, explicitly labeled ruling:

**NEW Soulbound viability rule:** because the source says “Return” the elite, returned HP is:

`max(1, floor(currentMaximumHP / 2))`.

This is specific to this living/undead return permission.

Completed-LR full return likewise restores the same bound asset to its current legal maximum. It creates no new elite identity.

Any recharge/rest-use reset comes only from the canonical completed-long-rest system, not from the HP return itself.

---

## 10. Wraithbound markers and invisibility

Use one owner-linked **companion regular marker** immediately after the owner's original regular turn.

That marker controls:

- companion recharge ticks;
- previous/next companion-turn references;
- Wraithbound invisibility eligibility.

Extra turns do not create another marker.

Initiative reordering/removal does not restart the virtual sequence.

### Invisibility

Read both sentences together.

Wraithbound loses invisibility when it either:

- attacks; **or**
- imposes control.

The first clause explicitly requires neither to have occurred since the prior companion turn.

The narrower second sentence describing attack does not erase “imposed control” from the eligibility predicate.

After either event, it cannot regain this source invisibility until the appropriate end of its next regular companion marker and only if the predicate is then satisfied.

A tick from a previously-created persistent effect is not automatically a new attack or command by the companion.

No supplied Wraithbound feature here creates such a persistent control effect.

Boneflayer Grave Miasma ticks therefore do not affect Wraithbound's invisibility clock.

### Uncommanded behavior

If the owner cannot issue a command, a still-existing companion may perform only its supplied defensive movement/Dodge behavior, subject to its own conditions.

This grants:

- no damaging/control action;
- no additional Reaction;
- no class trigger;
- no resources.

No generic companion Reaction is created by this packet.

---

## 11. Druid swarm dependencies

Confirmed.

### Base Swarm Summoning

Independent spell/class summon:

- concentration;
- 10 minutes;
- 1/short rest.

Changing Druid form does **not** end it merely because a form changed.

Engine[3] ends **old-form features/summons**, not unrelated preexisting summons.

### Carrion Rat King

Its form-created swarm:

- printed 1 minute;
- ends earlier if the form ends/changes;
- replaces the previous **form swarm**, not Base Swarm Summoning.

### Broodmother

The two spawned swarms use the bounded standard companion profile.

Therefore their lifetime is:

`min(standard companion 1 minute, remaining Broodmother form duration)`.

The explicit “both end with form” is an earlier ending condition, not permission to exceed the standard one-minute companion lifetime.

Both share one combined damaging command as printed.

### Master of Vermin

A substituted swarm created by a paid summoning spell inherits:

- that spell's duration;
- that spell's concentration;
- that spell's creature count.

The form only substitutes the profile.

Changing form does not automatically end that independently sourced spell summon.

Different swarm source instances can coexist when their actual concentration/cap rules permit. Dependency is tracked per source instance, not by creature name “swarm.”

---

## 12. Wizard elites and genuine evidence gaps

Your source check is correct.

For this bounded package:

### Wizard standard undead

Creation exists:

- Corpse Harvest;
- Auto-Raise.

Profiles/cap exist:

- engine[19];
- engine[20].

Ghoul Lash command exception exists.

### Wizard elites

Profiles/caps exist:

- engine[21];
- engine[22];
- engine[23].

But there is **no supplied operational Wizard elite acquisition procedure** giving:

- Action/time;
- RP cost;
- binding target;
- eligibility;
- creation timing;
- replacement after death.

There is also no supplied Wizard elite return procedure.

Therefore the implementation may define:

- profile schema;
- cap validation;
- command behavior;
- maximum-HP modifiers;

but must expose **no public create/bind/return operation** for Wizard elites yet.

`command-undeath` remains separate unfinished spell evidence and cannot fill this hole.

Mage's similarly named elites do not donate their acquisition/return procedure to Wizard.

### Not genuine gaps

These are already supplied and should not be marked missing:

- Ranger Beast ritual/action/cost/time/frequency;
- Mage Familiar creation/dismissal/duration;
- Mage Lich elite unlock and long-rest return;
- Soulbound Ritual;
- Corpse Harvest standard-minion creation;
- Auto-Raise trigger;
- Mirror Beast summon;
- Reflective Companion application procedure, subject to the new hard-denial integration above;
- Druid Base Swarm Summoning.

### Genuine future evidence still useful

Still open:

- general living-companion natural rest/Hit Dice recovery;
- global corpse cleanup/decay/removal timing;
- exact Ranger keen-sense choice/definition if a separate source exists;
- Wizard elite binding and return source;
- wider form/temp-HP cards;
- broader companion families.

## Implementation disposition

These reconciliations are ready to be written as the **100-source creature lifecycle implementation overlay**, now using the original three shared paragraphs plus the two additional frozen targeting/hard-denial paragraphs as supporting evidence.

Status remains:

> **SOURCE-AUDITED / DRAFTABLE — implementation pending.**

Nothing here closes the five classes, the broader form/temp-HP systems, Wizard elite acquisition, general corpse cleanup, natural companion-rest rules, balance, or the complete runtime.
