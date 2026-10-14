# FEAT335-CADENCE-CHECK-01 — controlling narrow addendum

**Decision: correct the overbroad local default. Eleven unqualified-turn rows and Overrun require local cadence-key corrections; the other 26 requested feat rows retain their keys. No feat approval or status change follows.**

## Inspection and source binding

I verified the submitted archive at **243,342 bytes**, SHA-256 `5d67cc24ab7ce5274f6a055a60616143d5d605b3dfdfdb9b1c4f4e7910f1ffe9`, and every one of the **12 payloads** listed in its actual root `PACKAGE_MANIFEST.json`. The ZIP has 13 entries including that manifest.

I read REQUEST.txt, all **38 cadence-bearing rows' complete current operative procedures**, their descriptors, both supplied local scripts, the controlling FS-06 and related shared clauses, and the included combat/class/temporal timing guides and TEX/resource-reference text. Those 38 rows contain **40 cadence records** because Eldritch Combat and Quickened Thought each have two. The other 139 descriptor rows were preserved/compared mechanically, not semantically re-audited. Referenced reports and dependencies outside this small archive were not silently retrieved or certified as current.

## FCD-01 — existing source distinction; NEW minimal default

The reviewed Combat guide explicitly defines a regular turn as the normal initiative slot and states **“An extra turn is distinct.”** Its no-refresh sentence protects **“the regular-turn allowances defined here,”** not every unqualified turn-triggered rider. CLASS_PLAYTEST_RULES.md's matching restrictions concern recharge and the extra-full-Action guard. The TEX addendum aligns that recharge summary; it did not convert every per-turn feat into a regular-turn feat. FS-06 explicitly defaults **“your turn”** allowances to the owner's regular interval and expressly preserves own/any/round predicates; it supplied no equivalent generic sentence for unqualified **“once per turn.”**

Tactical Flanker explicitly says **“that actual turn.”** Overrun says **“that turn's subsequent ordinary movement”** and **“each distinct creature may be challenged once that turn.”** In the opposite direction, Savage Attacker expressly retains **“Own and off-turn regular-turn allowances”** and Eldritch Combat **“one embedded cast per actual regular creature turn.”** The temporal control guide likewise demonstrates an explicitly actual-turn source that can qualify in a separately authenticated extra turn, without refreshing its regular save/expiry clocks. This is evidence that the clock categories are distinct, not permission to enable the unfinished temporal ability.

**Ruling:** for otherwise unqualified once-per-turn feat clauses, use each genuine actual creature turn, including a genuinely separately sourced extra turn. This is not an owner-regular-interval cap. To make the missing generic default explicit, adopt the following as **NEW minimal feat-scope authoring**, not recovered historical wording. The specific Tactical Flanker/Overrun readings and the Savage/Eldritch exceptions are retained source interpretations.

### Exact FS-06 addition

Append the following two paragraphs after the existing complete `FS-06` wording. In this packet the exact target is `DescentReviewChanges/ReviewBible/data/public/feat_candidates/exact_01/shared_rules.json#/rules/5/wording`, guarded by rule ID `FS-06` and the supplied original string/hash. Propagate identically to the actual current internal shared-rule mirror and shared manuscript; these two counterparts are not present in this small packet, so no unseen path or hash is certified.

NEW FEAT335-CADENCE-CHECK-01 completion, limited to feat procedures governed by FS-06: an otherwise unqualified "once per turn" allowance is once for that feat owner during each genuine actual creature turn in which its exact trigger legally occurs, whether that turn belongs to the owner or another creature. A separately sourced and actually occurring extra turn has a distinct actual-turn identity and can supply a distinct opportunity for that unqualified allowance; this rule grants no extra turn. Another Action, Bonus Action, attack, Reaction, nested event, target or resumed segment of the same actual turn does not create another turn identity. Returning to or replaying an already recorded turn retains that turn's spent claim. Actual body, movement, attack, casting, payment, causal-root and recipient restrictions still govern independently.

This completion does not replace an expressly regular-turn allowance or FS-06's existing default owner-regular-interval allowance for "your turn". In particular, Savage Attacker retains its stated own/off-turn regular-turn allowances, and Eldritch Combat retains its expressly regular-creature-turn shared embedded-cast cap plus its owner-regular-interval ordinary-append cap. Overrun's per-creature challenge limit belongs to the actual turn containing its qualifying Dash and subsequent movement; another Dash in that same turn does not renew it. Quickened Thought keeps its expressly any-later-actual-turn release window and the shared one-free-stored-release-per-owner/numbered-round cap, not a new bank at each turn. Per-round, encounter, underlying-roll/cast, recipient-rest and source-defined duration/deadline histories are not reset by an extra turn. Outside initiative retain the governed six-second procedure without inventing a turn from each action or counting an initiative transition twice. Source-specific temporal restoration remains separately governed; this completion supplies no rewind or unsupported extra-turn adapter.

## FCD-02 — exact local descriptor/builder changes

The exact replacements, with old values and input hashes, are in `EXACT_CADENCE_CORRECTIONS.json`. They contain **15 guarded operations**: one FS-06 append, two builder declaration replacements and twelve complete `laterEventCadences` value replacements. These are not fifteen new rules.

**Eleven IDs:** `bladedancer`, `break_line`, `bull_rush`, `crippling_strike`, `crusher`, `piercer`, `punishing_blow`, `slasher`, `tactical_flanker`, `unstoppable_force`, `precision_strike`.

For their one existing cadence record, retain `family`, `maximum: 1`, `scope: ["owner"]` and no-acquisition-claim initialization. Replace `epoch` with:

> genuine actual creature-turn identity (regular or separately authorized extra turn)

Replace `detail` with the exact full text in the operations file. It expressly limits only the turn-limited clause and preserves separate critical-hit/per-event clauses. The feat owner spends the allowance; the **turn containing the event** supplies the epoch. Neither the recipient nor active actor becomes the feat owner.

**Overrun:** retain `family: "overrun.challenge"`, `maximum: 1`, `scope: ["owner", "recipient"]` and initialization. Replace `epoch` with:

> actual turn containing the qualifying Dash and subsequent movement

Its replacement detail retains one challenge per actual recipient, no renewal from another Dash in the same turn, and a new qualifying Dash/real movement prerequisite in a distinct extra turn. No extra Action, movement budget or permission to enter a creature is granted by the key.

Remove Savage Attacker from the builder's generic unqualified-turn group and give it an explicit separate declaration retaining its **identical existing regular-interval descriptor**. This is a builder separation, not a change to that row's result. Leave the generic `EpochClaims` algorithm unchanged: it already distinguishes whichever authentic epoch is supplied. A new string or `extraTurn=true` is not evidence of an actual extra turn.

## FCD-03 — retain the other 26 requested rows

All 38 complete before/after mappings and source-procedure hashes are in `CADENCE_38_REGISTER.json`. The 26 retained IDs are:

`cleave`, `combatExpertise`, `combat_reflexes`, `combat_slide`, `crushing_advance`, `efficient_caster`, `energy_sink`, `fast_talker`, `lucky`, `mana_burn`, `savage_attacker`, `shield_bash`, `target_mark`, `whirlwind_striker`, `wilderness_chef`, `arcane_adaptation`, `arcane_calculus`, `conjure_flora`, `curse_weaving`, `eldritch_combat`, `eldritch_echo`, `mimicry`, `primal_instinct`, `quickened_thought`, `spell_reflection`, `trapsetter`.

The important distinctions are:

- **Savage Attacker:** its whole-pool reroll keeps the explicit regular-creature-turn allowance, including legal off-turn use. A linked extra turn does not create another regular allowance. Piercer's separate unqualified-turn reroll now has its own actual-turn opportunity; keep Savage-before-Piercer ordering.
- **Eldritch Combat:** both modes share the existing regular-creature-turn embedded-cast cap. Ordinary append additionally retains its owner-regular-interval cap; the off-turn branch still needs its real SR use and exact hit/cast requirements. An extra turn does not reset either regular cap. This is not a reason to convert that explicit exception to the new generic default.
- **Quickened Thought:** owner+real-encounter for the first-initiative bank is correct; it is an immediate source event, not an unspent permission that can be invoked later after a missed window. Its valid held cantrip can release on any later actual turn, including a separately legitimate extra turn, only between completed events. The release still shares one `freeStoredRelease` per owner/numbered round with Arcane Calculus and the same single Ready/concentration slot. Its separate BA-conversion SR/LR use is not this bank. Arcane Calculus keeps its narrower next-own-regular-turn release window.
- **Owner/recipient:** Mana Burn is recipient-wide across all owners; Curse Weaving is owner+recipient; Wilderness Chef follows the eater's beneficial-LR epoch independently of the cook's preparation use. Target Mark and Primal Instinct retain their actual instance/recipient identities and existing consumption rules. Hard-denial keys use the actual source character, recipient and encounter, not a new trap/custodian.
- **Do not overextend a key:** these descriptors are partial projections. Tactical Flanker's one-die-per-hit across owners, hard-denial actual-application gate, source-specific trigger windows and independent costs still need their own existing predicates. Their omission from the generic identity-algebra helper is not proof they were executed, or a new permission to omit them in the full procedure.

I found **no further concrete owner/recipient/epoch error in the other 26 mappings within this requested scope**. This is not a new 335-row acquisition verdict or validation of every use-time consequence.

## Finite verification and fulfillment

`FINITE_CADENCE_EXPECTATIONS.json` supplies twelve bounded authored acceptance groups covering the actual-turn default, multiple events and resumed turns, off-turn owner identity, movement predicates, Tactical Flanker, Savage/Piercer, uncapped sibling riders, Overrun, Eldritch Combat, regular-own-turn exceptions, Quickened Thought, global/cast/roll/recipient histories and unchanged clock boundaries. They are **authored expectations**, not gameplay-runtime passes.

I executed `check_cadence_addendum.py` against this exact ZIP: **381 checks passed, zero failed** — 45 integrity, 136 static, 179 preservation and 21 extracted-key-algebra comparisons. It executes the supplied original/amended CADENCE declarations and the supplied `EpochClaims` class only, with conditional supplied epoch/event facts. It does **not** execute `assemble()` against absent repository inputs, BoundAllowance/FiniteFeatUse, the turn scheduler, complete attacks/spells/Ready/rests, temporal restoration or real campaign authentication. Large successful compared values are stored as canonical-JSON fingerprints after actual deep-snapshot equality; failed values would remain fully disclosed.

Reproduce with Python standard library:

```text
python check_cadence_addendum.py /path/to/DD_FEAT335_Cadence_Check_01.zip /path/to/new_report.json
```

For local fulfillment, preserve this submitted archive and current pre-edit descendants; apply the listed exact changes, propagate the identical FS-06 addition to its real mirrors, and regenerate only the affected derived cadence/source bindings. Record actual new shared-rule/builder hashes in current descriptor `sourceBindings` entries 5 and 8; preserve old bindings in the old report/archive rather than claiming an old test covered new bytes. Keep the same 177 entries, 38 cadence-bearing IDs and 40 cadence records. Verify unchanged complete feat procedures, original objects, finite allowances, permanent choices, history and all approval/selection flags. Record the finite source-based expectations and actual executed-check scope separately.

**These finite edits and a version-bound fulfillment receipt resolve this narrow cadence question without another generic conference or unchanged 335-feat resubmission.** They grant no feat promotion, full acquisition/use approval, runtime selection, actual extra turn, human balance, whole-game agreement, source deletion or cosmology review. All previously fulfilled scopes carry forward. Delivery remains actual final joint whole-game flow agreement → already-authorized commit/push → verified remote commit → careful cosmology review and preservation-based cleanup in their agreed phases.
