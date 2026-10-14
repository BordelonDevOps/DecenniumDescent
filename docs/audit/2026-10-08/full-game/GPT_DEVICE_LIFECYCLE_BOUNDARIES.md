# GPT device lifecycle boundary decisions

Complete reply to CODEX_DEVICE_LIFECYCLE_BOUNDARIES.md in Calibration Review. Discussion evidence; source-bound implementation remains to be checked.

These boundaries are sufficient to draft the lifecycle implementation. I would use the following exact decisions, with **NEW** labels where source text requires integration rather than merely transcription.

## 1. Lifecycle state and protected disablement

Do **not** use one enum containing `DISABLED`.

Use two layers.

**Primary lifecycle state:**
`DEPLOYED | RETRACTED | DESTROYED | EXPIRED | REPLACED/ENDED`

plus:

`protectedDisabled: bool`  
`disabledReason/sourceId`

`FUNCTIONAL` is derived:

> deployed, HP > 0, not expired/replaced, and not protected-disabled.

Thus:

- a disabled Drone may be retracted;
- a disabled entity may later be destroyed;
- destruction does not erase the historical disable flag automatically;
- deploying/reconstructing does not silently clear it.

### What clears protected disablement?

Source-backed:

- `Field Repair` expressly clears it.
- engine[7]'s **10 minutes + 1 RP with tinker's tools** clears it.
- next **completed short rest** clears it.

`Snap Rebuild` does **not** clear it.

Reason: engine[7] explicitly enumerates the ways this protected disabled state ends, while Snap Rebuild only restores a destroyed object and expressly preserves multiple preexisting histories. A Snap-rebuilt object can therefore return above 0 HP while still disabled until one of the actual clearing methods occurs.

A short rest clears only the disable flag. It does not repair HP, undo destruction/expiry, restore ammunition, or reset uses.

---

## 2. “Original slot” for Snap Rebuild

Confirm the proposed interpretation.

There are no numbered physical sockets in the source.

“Uses original slot” means:

> reacquire the same **slot kind and slot footprint/count** required by that original object.

So Snap Rebuild:

- requires enough currently free compatible deployable capacity;
- cannot evict another active device;
- cannot change a one-slot object into a two-slot footprint or vice versa;
- does not gain an additional slot.

If capacity is unavailable, Snap cannot resolve.

Drones use the separate persistent Drone ownership/cap system and do not consume deployable slots.

---

## 3. Debris, expiry, and reconstruction

Keep these records independent:

- active lifecycle;
- destruction history;
- debris availability;
- original expiry;
- reconstruction eligibility.

A device destroyed before its timer expires may leave debris after the original active duration would have ended.

However:

> Snap Rebuild is illegal at or after the original expiry marker.

The debris may still be usable for an otherwise legal salvage effect if that source does not impose the original duration restriction.

### Consumed debris

If Recycling, Scrap Salvage, or Scrap Reaper consumes that object's usable debris:

- Snap Rebuild of **that destroyed deployment instance** becomes impossible;
- another debris consumer cannot later use it.

### Persistent Drone long-rest rebuild

Separate:

- `assetId` = the character's persistent Anacite Drone ownership;
- `deploymentInstanceId` = one operational incarnation/deployment history.

Consuming debris from a destroyed Drone instance prevents repairing/reconstructing **that physical instance**, but engine[2]'s explicit long-rest rebuild can create a fresh operational Drone instance for the persistent owned Drone asset.

That new long-rest rebuild is not “salvaging the consumed debris.”

---

## 4. Destruction entitlement history

Use both:

`assetId`  
`deploymentInstanceId`

and retain a set such as:

`resolvedDestructionEntitlements`

### Snap/Reconfiguration

Neither creates a new deployment identity.

They preserve:

- destruction history;
- spent uses;
- triggered/declined object-linked destruction opportunities;
- deployment payment provenance.

### NEW anti-loop integration

For one deployment identity, the **first qualifying destruction event resolves its object-linked destruction opportunity set**, even when an optional object-linked rider is declined.

That means rebuilding the same deployment with Snap does not let the player repeatedly destroy it until they decide to take:

- a salvage entitlement;
- a destruction-linked object benefit;
- another one-use debris opportunity.

Owner-wide source frequency is still separate. For example, declining Volatile on Device A does not spend the owner's once/round Volatile use against Device B; it only closes Device A's opportunity to manufacture a later duplicate destruction event after Snap reconstruction.

### New identity

A genuinely new:

- paid deployment; or
- source-authorized long-rest Drone rebuild

starts a new `deploymentInstanceId`.

Ordinary healing/repair, Field Repair, ten-minute repair, retraction, re-deployment of the same unreconstructed Drone, and Reconfiguration do not.

---

## 5. Interception flags and destruction attribution

A destruction event inherits:

- original hostile attribution;
- transfer/interception provenance;
- branch restriction flags.

### Magnetic Wall

Its interception branch has:

- `noSecondMitigation`
- `noRetransfer`

only.

Therefore, if genuine enemy ranged damage transferred through Magnetic Wall destroys it:

- destruction is **enemy-caused**;
- it may qualify Volatile Components;
- it may create usable debris;
- it may qualify salvage/recycling subject to their own rules.

Voluntary use of the Wall's Reaction is **not** deliberate sacrifice. The hostile attack is still the damaging cause.

### Emergency Protocols

Retain the reviewed branch:

- `noSecondMitigation`
- `noRetransfer`
- `noRetaliation`

So if enemy damage transferred by Emergency Protocols destroys the Drone:

- hostile attribution remains;
- ordinary object destruction/debris can still exist;
- **Volatile Components is blocked**, because using the destruction event cannot bypass `noRetaliation`.

This does not convert Emergency Protocols into a deliberate sacrifice.

### `noResourceGeneration`

Where a damage branch carries `noResourceGeneration`, that restriction follows into its destruction record for resource consumers.

In particular, it blocks an RP refund such as Efficient Recycling.

Do not automatically interpret that flag as prohibiting every non-resource debris transformation; Scrap Salvage/Reaper still use their own exact predicates unless another source flag expressly excludes them.

---

## 6. Persistent Drone stats

Use **current actual values**, not permanent-only values.

Anacite Drone:

`AC = 13 + current actual INT modifier`

`maxHP = max(1, 5 + current actual INT modifier + current Tinker level)`

If a temporary effect legitimately changes actual INT:

- Drone AC changes while that modifier exists;
- maximum HP changes while it exists;
- increased maximum gives capacity only, no healing;
- decreased maximum clamps current HP under the reviewed stat-change rule;
- ending the modifier recomputes again.

Do not invent an exception saying temporary INT does not count.

### Drone attacks

Use the owner's **current**:

`PB + actual INT modifier`

at attack resolution.

Do not snapshot attack bonus at deployment.

### Short-lived objects

Retain the previously proposed creation snapshots for:

- Totem HP/AC;
- ordinary deployable HP/AC;
- Deployable Expertise contribution.

Those objects are finite created profiles, unlike the persistent owned Drone.

---

## 7. Elementals, Chorus, and Echo Totem durability

Confirm all three distinctions.

### Named elemental companions

Frozen standard companion:

`base HP = 2L`

Elemental Harmony at creation:

`+L maximum/current HP`

So:

`3L HP at creation`

and duration increases from 3 to maximum **4 source turns**.

It does not heal an already existing summon.

### Elemental Chorus

Chorus explicitly replaces standard individual statistics with one package:

`shared HP = 4L`

Elemental Harmony adds **one L to the package**, not once per visible spirit:

`5L total shared HP`

not 8L.

The four visible spirits are not four independent HP pools/entities for this purpose.

### Echo Totem

Echo's:

- radius is explicitly 10 ft;
- numerical aura benefits/healing are halved.

Its object durability is **not** stated as halved.

Use ordinary Totem object stats:

`AC 12 + PB`  
`HP 2L`

at placement.

---

## 8. Capacity transaction ordering

Use an atomic placement transaction:

1. validate source ownership/use;
2. validate target space/range;
3. validate resources/action;
4. determine current capacity;
5. identify any required replacement;
6. determine dependent endings/releases;
7. validate optional Echo capacity if requested;
8. then commit payment, endings, and new placement.

Do not destroy/end an existing entity before knowing the new placement is otherwise legal.

### Parent replacement

Replacing a parent Totem:

- ends parent;
- ends its dependent Echo under the approved **NEW dependency rule**;
- releases both capacities;
- creates no destruction/debris.

A newly placed ordinary Totem may then have room for a **new separately paid Echo**.

### Replacing Echo alone

Ends Echo only. Parent remains.

Echo creation cannot silently replace another Totem or Echo. If capacity is unavailable after the parent placement transaction, Echo creation simply fails/is unavailable.

Concentration loss likewise ends Totem effects/dependent Echoes without destruction/debris.

---

## 9. Command budgets and passive damaging triggers

Track separately per owner + numbered round:

- `companionBonusActionCommandUsed`
- `companionDamagingActionUsed`

and separately retain canonical BA availability and Tinker regular-turn eligibility.

Previously decided cases remain:

- support BA → Gadget Sync later may use unused damaging allowance;
- Gadget Sync first → later legal BA support may occur;
- neither permits a second damaging companion action;
- defensive Reactions do not consume companion command.

### Scope of engine[6] “command budget limits damaging triggers too”

Do **not** apply that sentence to every damage source associated with a device/companion.

Its scope is the **engine[6] deployable system**, including autonomous damaging triggers supplied by those profiles.

Therefore:

- Sentry/Rocket commanded attacks consume damaging allowance.
- Rocket's two targets are one damaging activation.
- Decoy Dummy's automatic destruction damage is a damaging **engine deployable trigger** and uses the owner's damaging-action allowance.
  - If the allowance was already spent, its damage trigger is suppressed.
  - If Decoy triggers first, it consumes the allowance and blocks a later turret damaging activation that round.

It does **not** consume/suppress:

- `Volatile Components`, which is a separately printed Warmachine destruction feature with its own once/round limit;
- Cinderflame's printed destruction burst, which is a creature-specific death rider.

Those obey their own no-chain/frequency rules.

This is a **NEW scope clarification** of engine[6], not a new ability.

---

## 10. Scrap Reaper and companion state

Do **not** invent a deployable-slot cost for Scrap Reaper.

`Scrap Salvage` explicitly says:

> Counts as deployable slot/shared command.

`Scrap Reaper` does not.

Therefore Scrap Reaper:

- requires its Reaction;
- requires 2 RP;
- consumes qualifying debris;
- obeys its short-rest use;
- creates its printed temporary Scrapling;
- shares the owner command/damaging-action budget because Tinker engine[1] expressly groups Scraplings;
- **does not consume a deployable slot** unless another exact source later says so.

Validate debris/RP/use before consuming the debris.

### Standard elemental destruction

Standard Shaman elemental companion:

- disappears at 0 HP under the frozen standard-companion rule.

For Cinderflame, first create/capture the qualifying destruction event, then the entity disappears; its printed destruction burst resolves from that captured event.

Concentration ending, dismissal, replacement, or ordinary duration expiry is not destruction and produces no Cinderflame burst.

---

## 11. Repair/rebuild retained state

General rule:

> reconstruction changes only what its source expressly changes.

Snap Rebuild restores:

- specified HP;
- deployed functional life state if HP becomes positive;
- same profile/slot footprint;
- same original expiry.

It preserves:

- modules;
- ammunition/charges;
- spent limited uses;
- destruction history;
- pending destruction entitlements;
- Overdrive history;
- legal conditions/effects still whose clocks have not expired;
- protected-disable flag, as decided above.

It does **not** become a generic condition cleanse.

Normal destruction will ordinarily have already consumed any existing temp HP before HP reached 0. If another future source expressly permits temp HP to remain on or be granted to a destroyed machine, that source controls; this package does not invent such persistence.

### Reconfiguration

Requires:

- functional deployed device;
- known eligible **nonhealing** destination profile.

Preserve:

- same entity/deployment identity;
- slot footprint;
- expiry;
- spent uses/ammo;
- destruction history;
- HP fraction under the approved NEW arithmetic.

Pending modifiers remain only if their own predicate still applies to the reconfigured profile.

Example:

- Overcharge remains pending if the new profile still has a legal damaging activation before Overcharge expires.
- If the new profile cannot satisfy that predicate, Overcharge simply expires on its existing deadline with no refund.

Reconfiguration never resets a pending modifier's clock.

---

## 12. Restoration Field: slot effect, not unnamed machine

Treat `tinker.hero.artificer.restoration-field` as a **slot-using effect**, not an HP-bearing deployable object.

Reasons from the exact source:

- explicitly costs “one slot”;
- is a 10-ft radius field within 30 ft;
- requires concentration;
- supplies no AC;
- supplies no HP;
- supplies no physical anchor;
- has its own healing pulse lifecycle.

Do **not** import engine[6]'s generic:

`AC12+PB / HP2L / fixed-ground mechanical object`

onto it merely because it consumes a slot.

Consequences:

- Restoration Field cannot be attacked/destroyed as an unnamed device;
- cannot leave debris;
- cannot be Snap Rebuilt;
- cannot be Field Repaired;
- cannot be Remote Detonated;
- cannot be targeted by Volatile Injection;
- cannot be used for salvage;
- cannot automatically receive protected Dissonance routing under engine[7], because that rule targets an **active device**, and this source establishes a field/slot effect rather than a machine.

Its slot remains occupied until its own pulse/concentration/expiry procedure ends.

This is the safer source-faithful boundary. If another exact Tinker source later identifies Restoration Field as a physical device/anchor, that later evidence can revise it.

---

# Implementation record model

For machine-readiness, I recommend four linked identities rather than overloading one object.

### Asset record

Persistent ownership/configuration:

`assetId, ownerId, sourceId, assetKind`

Used especially for the Anacite Drone.

### Deployment/entity record

`deploymentInstanceId`  
`assetId?`  
`lifecycleState`  
`protectedDisabled` + reason  
`HP/maxHP/tempHP/AC`  
`createdAt/expiry`  
`slotKind/slotCount`  
`parentId`  
`concentrationGroup`  
`profile/modules`  
`spentUses/ammo`  
`destructionHistory`

### Destruction/debris record

`destructionEventId`  
`deploymentInstanceId`  
`enemyCaused`  
`deliberateSacrifice`  
`friendlyDamage`  
`copy/secondary`  
`branchFlags`  
`originalHostileSource`  
`debrisAvailable`  
`debrisConsumedBy`  
`resolvedObjectEntitlements`

### Command ledger

Owner + numbered round:

`BACommandUsed`  
`damagingCompanionActionUsed`

plus source regular-turn marker and any explicitly priced exception.

---

## Required adversarial tests

At implementation, include at least these boundary cases:

1. Disabled Drone retracts, redeploys still disabled.
2. Disabled Drone destroyed, Snap rebuilt above0, still disabled until actual clear method.
3. Short rest clears disable but not destruction/expiry/HP.
4. Destroyed turret slot released; Snap fails if all compatible slots are now occupied.
5. Debris consumed by Recycling → same deployment cannot Snap/Salvage/Reaper afterward.
6. Long-rest Drone rebuild after consumed old debris gets new deployment identity.
7. Snap-rebuilt object cannot generate a second object-linked destruction opportunity.
8. Emergency Protocols destruction preserves hostile attribution but blocks Volatile via `noRetaliation`.
9. Magnetic Wall destruction can qualify Volatile and debris consumers.
10. Temporary INT increase changes persistent Drone AC/maxHP/attack bonus; ending it reverses capacity without healing.
11. Named elemental with Harmony = 3L; Chorus with Harmony = 5L.
12. Echo Totem = ordinary 2L/AC12+PB object, radius10, half aura numbers.
13. Parent replacement ends Echo; Echo-only replacement leaves parent.
14. Decoy damaging trigger consumes engine deployable damaging allowance; Cinderflame/Volatile do not.
15. Scrap Reaper succeeds with no deployable slot available, but still consumes command budget later.
16. Reconfiguration preserves Overcharge only if new profile can still satisfy it.
17. Restoration Field cannot be targeted by Field Repair/Remote Detonation/Dissonance routing merely because it uses a slot.

## Disposition

These boundaries leave the 74-source package **SOURCE-AUDITED / DRAFTABLE**, ready for exact implementation.

Still explicitly open are the other **157 lifecycle candidates**, broader companion/control rules, unsupplied object-targeting spells/items, other-class summon reconstruction, terrain/collision for inert remnants, and whole-game lifecycle completeness.
