# GPT completed Time Loop world-state source conference

ChatGPT said:

The source has two layers that must both remain visible. The original Boon V promise is very broad: reset the entire combat encounter to its beginning state, while allies retain knowledge. The reviewed operational card then deliberately narrows that into an initiative-start transaction over recorded participants while explicitly conserving per-rest/daily resources, physical consumables, inventory/loot ownership, and the Time Loop use itself. 
Pasted text
 
Pasted text

The following is therefore a NEW finite world-transaction bridge implementing that promise. It is not map-wide time travel and it does not turn the existing participant helper into a generic rollback engine. The existing helper is expressly incomplete for equipment, environment, body duplication and clock rebasing. 
Pasted text

1. Encounter participants and the world boundary
Participant roster

At initiative-start snapshot, freeze a finite participantRoster.

A participant is any physical combat entity the encounter authority has already registered as belonging to that encounter, regardless of whether the players know about it.

Include:

visible combatants;
hidden/unrevealed combatants already present;
off-board or concealed reinforcements already designated as part of this encounter, using their actual staging/off-board state;
mounts and independent pets participating in combat;
pre-existing summons/companions that are already participating;
controlled enemies already participating;
combat-capable persistent assets whose mutable state matters independently, such as an existing companion/drone/turret where its reviewed source treats it as an entity.

Do not automatically include:

every creature on the map;
bystanders not designated as encounter participants;
arbitrary objects;
later unscheduled arrivals.
Later arrivals

A creature designated at snapshot as an off-board reinforcement is already a participant and rewinds to its snapshot staging state.

A genuinely new/unregistered creature that enters later is a nonparticipant external entity. It is not rewound.

If such an external entity can remain in its current state without obstructing the atomic restore, Time Loop may still resolve.

If its current position/body/environment makes the snapshot restoration impossible without teleporting, damaging or rewinding that nonparticipant, Time Loop is unavailable at that activation and remains unspent.

Post-snapshot summons

A creature genuinely created after the snapshot by a participant is not added to the immutable snapshot roster. It is tracked as a temporal child of its creation source.

On rewind:

that post-snapshot creature ends/is removed;
its creation cost/use/RP remains spent;
its loot/death/reward events remain historically recorded;
it does not become a second copy when the original timeline is discarded.
Environment

Doors, walls, hazards and similar things are not creature participants. They belong to a finite environmentAnchorRegistry, discussed under question 3.

This is the necessary bounded interpretation of “entire combat”: the complete registered encounter state, not the entire surrounding world. That is a NEW narrowing necessary to avoid map-wide rollback.

2. Bodies, corpses and reconstructed identities

The already-reviewed temporal contract establishes that Time Loop is not resurrection: a creature alive at snapshot can return from a later death, while a creature dead at snapshot remains dead. 
Pasted text

Each snapshot participant therefore needs:

immutable character/creature identity;
canonical body identity;
immutable physical origin;
current anatomy record;
any body-lineage/derivative identities.
Restore rule

Time Loop restores one canonical physical expression of that identity to its snapshot state.

If the participant later:

died;
became a corpse;
was turned into an object;
was raised as an undead derivative;
had its corpse consumed by another effect;
acquired a separately reconstructed body;

then all later physical expressions that derive from the same snapshot body/identity are reconciled to one restored snapshot body.

There is never:

restored living body + old corpse;
restored creature + raised corpse-creature;
two reconstructed bodies;
a second soul.
Derived-body collapse — NEW conservation bridge

A post-snapshot body, undead, corpse-object or body-derived material that cannot coexist with the restored snapshot identity is a temporal derivative, not independent loot.

It is retired when its source body is restored.

That is the necessary exception to the general inventory-preservation rule: otherwise restoring the source body would physically duplicate its matter.

However, consumed finite resources used to create/manipulate the derivative remain spent.

Example:

B dies after snapshot.
B's corpse is consumed to create undead U.
Necromancer pays a limited use.
Time Loop fires.

Result:

U ends;
B's same body returns to snapshot state;
the limited use remains spent;
no extra corpse remains;
no new death/resurrection trigger occurs.
Already dead at snapshot

If B was dead at snapshot:

B returns dead;
snapshot corpse/body condition returns;
Time Loop does not turn that state into resurrection.
3. Atomic positions and environmental restoration
Finite environment boundary

At initiative snapshot, register every mutable encounter anchor whose state can materially alter:

participant occupancy;
movement;
line of effect;
legal targeting;
environmental damage/hazard state.

Examples:

doors;
destructible walls;
encounter barriers;
traps;
terrain hazards;
movable encounter machinery;
pre-existing Palisades/deployables if their source model makes them world objects rather than creature participants.

Do not snapshot the whole map.

Each anchor gets a world-unique identity and explicit rewind policy.

Atomic restoration plan

Before Time Loop costs anything, construct the entire destination state:

every participant snapshot position and footprint;
snapshot anatomy/size;
every rewindable environment anchor;
every post-snapshot temporal child scheduled for removal;
every external nonparticipant that remains unchanged.

All destination occupancy must be mutually legal simultaneously.

No sequential “move A, then see if B fits.”

Terrain

For registered encounter anchors:

destroyed after snapshot → restore snapshot anchor state;
altered after snapshot → restore snapshot state;
created after snapshot by a participant encounter effect → remove it if it did not exist at snapshot.

Physical costs used to create those post-snapshot structures remain spent.

Nonparticipant obstruction

If a nonparticipant or nonrewindable external structure currently occupies a required snapshot space and no existing geometry rule allows the states to coexist:

preflight fails; Time Loop is unavailable and unspent.

No:

nearest-space teleport;
forced relocation;
crushing damage;
wall traversal.

This uses the same conservative geometry philosophy already established for mandatory transformation reversion. 
Pasted text

4. Restored state versus conserved expenditures

Use two independent ledgers.

A. Rewindable encounter state

Restore to the initiative snapshot:

participant position/footprint;
life/death state;
HP/current maximum relationship as recorded;
active temp-HP grant identity and remaining amount;
death-save counters/Stable state;
Wounds and linked Injuries;
Core/custom conditions;
Revelation Charges;
per-encounter uses;
encounter hard-denial source/target histories;
encounter per-target immunity/history allowances;
encounter recharge/cooldown counters;
current anatomy/form state;
encounter-relative attached effects;
snapshot Soul Bind state;
initiative order and encounter cursor;
per-round Action/Reaction/command/offense/extra-Action budgets to their snapshot state, subject to the Time Loop activation overlay described below.

The existing reviewed contract expressly names position, life, conditions, RC, per-encounter uses and Soul Bind. 
Pasted text

B. Conserved history/resources

Never rewind:

world elapsed time;
long-rest/short-rest epochs;
weekly clocks;
Time Loop uses;
RP;
Ki;
Conviction;
Blood Gauge;
device stock;
ammunition/physical consumables;
healing reserves;
Mutation reserves;
Lifeleech Recovery Reserve;
Soul Charges;
kit uses;
rations/materials;
spell/resource payments;
short-/long-rest/daily uses;
loot ownership;
XP/treasure entitlements;
anti-farm/reward histories;
unique event IDs;
unique form/cast/grant IDs;
current physical item existence;
currently consumed/destroyed/lost-item history.

Those explicit exclusions are already part of the reviewed source-derived card. 
Pasted text

Specific class examples

Ranger bond: bond identity is conserved; snapshot Beast participant state can rewind. A spent rebond/rest resource does not.

Mage elite: same elite asset identity returns to its snapshot combat state if it was a participant. A later Soulbound/return/LR use remains spent.

Wizard raised undead: if already present at snapshot, restore the same undead identity/state. If raised afterward, remove it on rewind; raising costs remain spent.

Mirror entities/slots: restore snapshot encounter records/slot occupancy; don't refund external resource costs.

Druid: restore the exact existing FormInstanceID and form-dependent state from snapshot. Do not create a new Shift. Buffer Reserve, Form Surges and rest-based Shift resources remain at their current conserved values. A snapshot temp-HP amount may be restored because temp HP is explicitly named, but no Reserve refund occurs.

Palisade: a snapshot wall may restore its snapshot structural state. A kit consumed after snapshot stays consumed. A post-snapshot wall disappears while its kit remains spent.

Tinker: snapshot device identity/state can restore if registered; device stock/ammo/material reserve does not. A post-snapshot deployable can disappear without refunding the stock that created it.

5. Effect identity and clocks

This needs explicit clock classes. Do not blindly deepcopy absolute timestamps.

Every snapshotted effect must declare one of:

ENCOUNTER_RELATIVE

The effect belongs to the encounter timeline.

On rewind, restore:

the same effect ID;
same source ID;
same dependency relationships;
the remaining duration it had at the snapshot.

Rebase that remaining duration from the new iteration start.

This is not a fresh application and fires no:

cast trigger;
entry trigger;
healing trigger;
summon trigger;
resource-generation trigger.

Examples appropriate for this class:

temporary Polymorph/Shapechange/Mass links existing at snapshot;
True Polymorph shaping existing at snapshot;
short combat conditions;
next-regular-turn effects;
encounter-local command/effect deadlines.

For marker-based effects, restore the snapshot marker relationship rather than manufacturing an absolute timestamp.

A “until owner's next regular turn” shield active at snapshot again ends at the corresponding next regular turn in the new iteration.

WORLD_ABSOLUTE

The world clock does not rewind.

Keep the original absolute endpoint.

If it has already expired by the time Time Loop resolves, it does not come back active.

Examples:

24-hour Necrotic Affinity seals;
post-death 24-hour Soul Bind;
multi-hour/day effects whose source clearly lives outside the encounter clock.
REST_EPOCH

Use the current real rest epoch. Never roll it back.

Examples:

default temp-HP long-rest lifetime;
Blood Ritual next-LR rider;
Chef family/rest entitlements.
PERMANENT

No expiry exists. Restore the snapshot record only if the identity itself is rewindable.

Mandatory source adapter

No duration is assigned to one of these categories merely from its numeric length.

Every effect type must have an explicit temporalClockClass.

Unknown class = incomplete snapshot.

That prevents a generic Time Loop adapter from silently deciding whether a 1-minute or 24-hour source means combat-relative or world-relative.

Promoted transformation interface

For participant-owned transformation records existing at snapshot:

temporary Polymorph/Mass/Shapechange: ENCOUNTER_RELATIVE;
True shaping: ENCOUNTER_RELATIVE;
permanent True: PERMANENT.

Thus a True Polymorph that was still shaping at snapshot but stabilized in the discarded timeline returns to the same shaping record, with its snapshot remaining duration.

Suppression state also restores to its snapshot value.

No new object-companion slot is created: snapshot sponsorship/control/slot occupancy is restored as identity state.

The transformation rules already require one physical identity and prohibit hidden former forms. 
Pasted text

6. Concentration

Concentration is part of snapshot encounter state only when its owner is inside the temporal participant/dependency closure.

Snapshot concentration

Store:

concentration owner;
concentration record ID;
source ID;
linked effect IDs;
clock classification;
target/dependency IDs.

If a participant caster had concentration at snapshot and later:

lost it;
failed a concentration save;
began another concentration spell;

Time Loop restores the snapshot concentration record.

But:

RP paid for later spells stays spent;
post-snapshot spell records are ended/removed;
no cast/entry triggers fire;
the restored concentration is the old identity, not a new cast.
Absent nonparticipant caster

Time Loop must not silently overwrite the concentration slot of an unrelated off-scene creature.

Therefore a concentration-dependent snapshot effect whose caster is not inside the temporal dependency closure makes the snapshot nonrestorable unless an exact source says the effect can persist/restored independently of the caster.

The safe implementation is:

every mutable external concentration source required to reconstruct participant state must be captured in the snapshot dependency closure, otherwise Time Loop is unavailable for that encounter.

That is a NEW completeness requirement.

Independently ongoing external effects

A nonconcentration effect sourced by an absent nonparticipant may continue according to its actual world-time record. Time Loop does not fabricate another source instance.

7. Per-encounter histories, commands and event identity

Yes: the phrase per-encounter uses includes the actual encounter-scoped ledgers necessary to reproduce initiative-start combat state.

Restore:

once/encounter uses;
per-target hard-denial allowance;
per-target encounter immunity/history;
encounter damage-history gates;
recharge counters;
original-turn/round action-budget state;
companion command/offense budgets;
universal extra-Action allowance.

The broader class suite defines these encounter/round ceilings independently. 
Pasted text

But event history is not erased

Every event that occurred in a discarded iteration remains in a historical event registry.

Never reuse its event ID.

The new timeline gets:

encounterId + iterationId + freshEventId

This prevents:

double XP;
double loot;
Soul Charge corpse rescans;
copied healing replay;
duplicated resource triggers;
death-reward farming.

Restoring a per-encounter use means the feature may be used again under its source rules, but the new use creates a new event identity and must still pay every conserved cost.

8. Reaction timing, multiple Oracles and initiative restart

The original only says Reaction before round 4, so exact timing is a NEW bridge. 
Pasted text

Use this:

Legal trigger window

Time Loop can be declared after one actual atomic combat event has completely resolved and before the next event begins, while the encounter is still before round 4.

Examples of completed event boundaries:

attack resolution;
damage packet;
save/effect resolution;
movement event;
command resolution;
condition application.

It does not interrupt halfway through:

a damage packet;
an attack;
a command;
a multi-stage healing transaction.

This ensures there is no half-resolved state to roll back.

Preflight

Before spending anything:

valid immutable initiative-start snapshot exists;
current round < 4;
Oracle actually owns Boon V;
Oracle has Reaction available;
Oracle's Time Loop LR entitlement is available;
no atomic event is currently unresolved;
identity/body/equipment/environment restoration plan is complete;
placement plan is legal;
all effect clock classes/dependencies are known.

Failure here:

Time Loop is unavailable and unspent.

Commit

After a valid plan exists:

spend Oracle's Reaction;
spend that Oracle's 1/LR Time Loop use;
allocate a new timelineIterationId;
mark both expenditures in the conserved ledger.

Only then apply the atomic restore.

Cleanup

Post-snapshot queued commands, attacks, zones, summons and delayed events belonging only to the discarded timeline are canceled/retired as appropriate.

Their already-paid conserved costs remain paid.

Restart

Restore:

initiative order;
round = 1;
initiative cursor = snapshot cursor immediately before the first regular turn.

Do not restore global elapsed world time.

Reaction debt overlay

Although action economy rewinds, the Reaction used to invoke Time Loop does not become free again.

After snapshot restoration, overlay:

TimeLoopReactionSpent[Oracle] = true

until that Oracle reaches the next legitimate Reaction-refresh point under normal initiative.

This explicitly satisfies the supplied two-Oracle acceptance scenario. 
Pasted text

Multiple Oracles

Multiple eligible Oracles may each Time Loop the same encounter.

Each always rewinds to the original immutable initiative-start snapshot, not the previous loop's start.

Every Oracle's actual LR use remains spent across all later loops.

A previously used Oracle cannot regain their use from another Oracle's rollback.

9. Allies, control and retained knowledge

Memory is not ordinary participant state. It is a conserved temporal-memory overlay.

Memory eligibility

At the initiative snapshot, record:

memoryEligible = participant allied with this Oracle at snapshot

This avoids allegiance manipulation after combat begins.

Therefore:

snapshot ally later dominated/turned hostile → still receives retained timeline memory after rewind;
enemy later Charmed/controlled into an ally → does not retroactively gain Boon V memory entitlement.

The rewind separately restores snapshot control/allegiance state.

What knowledge is retained

An eligible ally retains only information the character actually:

perceived;
experienced;
learned in the discarded timeline.

They do not gain:

Director-only information;
knowledge of hidden actors they never perceived;
unknown stats;
unseen events merely because the engine snapshot contains them.

Player characters retain their own remembered experience.

Agency

Memory does not prescribe behavior.

The source expressly says retained knowledge allows allies to make different choices. 
Pasted text

No engine rule may:

replay a previous choice automatically;
force a different choice;
force a spell/attack target;
compel an NPC/player decision because it occurred previously.

Temporal memory from earlier completed loops is itself conserved and is not erased by a later Oracle loop.

10. Snapshot completeness and diagnostics

Do not use:

completeSnapshot = true

as the sole gate.

Use a structured validator.

Proposed finite snapshot schema
Plain text
TemporalEncounterSnapshot
  schemaVersion
  encounterId
  snapshotId
  snapshotWorldTime
  snapshotIteration = 0

  initiative
    order[]
    cursor = BEFORE_FIRST_REGULAR_TURN
    round = 1
    regularMarkerState
    rechargePhaseState

  participantRoster[]
    participantId
    canonicalBodyId
    immutableOriginId
    participationKind
      combatant
      hidden-combatant
      staged-reinforcement
      companion
      mount
      controlled-creature
      combat-asset
      temporal-dependency
    snapshotControllerId
    snapshotAllegiance
    memoryEligibleByOracle{}
    playerKnowledgeMaskRef

  participantState[participantId]
    position
    footprint
    life
      alive/dead/stable
      currentHP
      maximumHP
      tempGrantId
      tempHPRemaining
      deathSuccesses
      deathFailures
      wounds[]
      linkedInjuries[]
    conditions[]
      conditionId
      sourceId
      effectRecordId
    revelationCharges
    perEncounterUses{}
    encounterLedgers
      hardDenial
      perTargetImmunities
      damageHistory
      rechargeCounters
      commandBudget
      offenseBudget
      extraActionBudget
    soulBindState
    anatomy
      anatomyRecordId
      sourceRecordId
      formOrTransformId
      suppressionState
      sponsorId
      controllerId
      dependencyIds[]
      snapshotMeldItemIds[]
    concentrationRecordId
    persistentAssetRefs[]

  effectRecords[effectId]
    sourceId
    sourceOwnerId
    targetIds[]
    stateAtSnapshot
    clockClass
      ENCOUNTER_RELATIVE
      WORLD_ABSOLUTE
      REST_EPOCH
      PERMANENT
    remainingEncounterDurationAtSnapshot
    absoluteDeadline
    markerDeadline
    dependencyIds[]
    riderState

  environmentAnchors[anchorId]
    anchorKind
    position/footprint
    state
    HP/durability if applicable
    provenanceRoot
    rewindable = true
    derivativeIds[]

  physicalIdentityGraph
    bodyId -> derivativeBodyIds[]
    anchorId -> derivativeObjectIds[]
    creationRoots[]

  inventoryReferences
    itemIds[]
    snapshotHolderRefs
    snapshotMeldRefs
    # diagnostic only — current conserved inventory wins

  conservationLedgerRefs
    restEpochLedger
    finiteResourceLedger
    physicalInventoryLedger
    lootOwnershipLedger
    rewardEntitlementLedger
    historicalEventIdLedger
    worldUniqueIdentityRegistry

  dependencyClosure
    concentrationSources[]
    controllers[]
    requiredExternalRecords[]

  diagnostics
    missingParticipantFields[]
    unknownClockPolicies[]
    unresolvedBodyLineages[]
    unresolvedEnvironmentAnchors[]
    unresolvedDependencies[]
    duplicatePhysicalClaims[]
    illegalSnapshotOccupancy[]
    sourceAdaptersMissing[]
Snapshot creation rule

At initiative start:

enumerate roster/dependencies;
capture participant states;
capture environment anchors;
capture effect records and clock classes;
capture identity graph;
bind references to conserved ledgers;
run diagnostic validation.

If any required entry is unresolved:

Boon V is marked snapshotUnavailable for that encounter.

Its use is not spent because the source expressly says incomplete snapshot makes the option unavailable/unspent. 
Pasted text

Restoration/conservation table
Domain	Time Loop treatment
Position/footprint	Restore snapshot
Alive/dead/HP/death counters	Restore snapshot
Temp HP amount/grant identity	Restore snapshot
Wounds/linked Injuries	Restore snapshot
Conditions	Restore snapshot
Revelation Charges	Restore snapshot
Per-encounter uses	Restore snapshot
Hard-denial/per-target encounter ledgers	Restore snapshot
Initiative round/cursor	Restore snapshot start
Command/offense/extra-Action budgets	Restore snapshot, then apply Time Loop Reaction debt
Snapshot anatomy/form	Restore same record/ID
Snapshot concentration	Restore if dependency closure permits
Encounter-relative clocks	Rebase snapshot remaining duration
World-absolute clocks	Do not rewind
Rest epochs	Do not rewind
RP/Ki/Conviction/Blood Gauge	Do not rewind
Device stock/ammo	Do not rewind
Healing/Mutation/Lifeleech reserves	Do not rewind
Soul Charges	Do not rewind
Physical consumables/kits/materials	Do not rewind
Equipment existence/ownership	Do not rewind
Time Loop use	Remains spent
Other SR/LR/daily/weekly uses	Remain spent
XP/loot/treasure entitlement	Do not rewind
Historical event IDs	Do not rewind/reuse
Snapshot environment anchors	Restore
Post-snapshot encounter-generated terrain/entities	Remove, costs remain spent
External nonparticipants	Leave unchanged
Temporal body derivatives	Collapse to preserve one physical identity
Subjective ally memory	Conserved/additive
Concrete scenario resolutions
Two eligible Oracles loop the same encounter

Oracle A loops.

A's LR use and Reaction remain spent.
Encounter returns to original snapshot.

Later Oracle B loops.

B's LR use and Reaction become spent.
A's use remains spent.
Both rewind to the same original initiative snapshot.
Any temporal memories already granted remain.

No loop refreshes either Oracle's per-rest entitlement.

Participant dies, corpse is raised or transformed

Restore the participant's same snapshot body identity.

Retire:

corpse derivative;
raised-undead derivative;
post-snapshot replacement body;
incompatible body-object derivative.

No second corpse/body survives.

All actual RP, kits, corpse-resource payments or limited uses spent creating those derivatives remain spent.

Nonparticipant stands in old square

If it can legally coexist with the atomic snapshot placement, leave it alone.

If not:

activation preflight fails; no Reaction or Time Loop use is spent.

No teleport/damage is invented.

Snapshot form ended and gear changed

Restore the same form/transformation record ID.

Do not recreate its snapshot equipment.

Reconcile its meld set against current conserved inventory:

same existing item still lawfully held by that identity → may remeld according to the source's snapshot anatomy;
transferred item → stays with current owner;
consumed/destroyed/lost item → remains absent;
dropped external item → stays where it actually exists.

No normal form-entry hooks run.

Snapshot True Polymorph record

If shaping at snapshot:

restore same shaping ID;
same origin/sponsor/controller;
same suppression state;
same snapshot remaining encounter-relative duration.

If permanent at snapshot:

restore same permanent record.

No second object-companion slot or new body is created.

Active spell now past its former timestamp

If its clockClass=ENCOUNTER_RELATIVE, restore its snapshot remaining duration.

If WORLD_ABSOLUTE, keep the old deadline; if already expired, it does not revive.

This is why every effect requires explicit clock classification.

Later summon, device destruction, kit/RP spends

Post-snapshot summon:

disappears;
creation cost remains spent.

Snapshot device later destroyed:

same device entity/state may rewind;
stock/ammo/material reserve stays current.

Kit use:

stays consumed.

RP:

stays spent.

Round command/offense state:

rewinds to snapshot encounter budget.
Soul Charges, Lifeleech, seals, Agony

Soul Charges: current amount is conserved.

Soul body/LR entitlement histories: conserved, preventing death farming.

Lifeleech Recovery Reserve: current spent amount is conserved.

Lifeleech root/window event histories: historical discarded event IDs stay reserved; new timeline uses new event IDs.

Necrotic Affinity seal created by a death that Time Loop undoes: that death instance is closed/archived because the death no longer exists. It does not remain an active blocker on the living restored participant.

A seal already attached to a participant who was dead at the snapshot returns according to its snapshot record and its WORLD_ABSOLUTE deadline.

Agony suppression: if active at snapshot and classified encounter-relative, restore its same family record and snapshot remaining duration. If applied only after snapshot, remove it; the 2 Soul Charges spent remain spent.

Dead at snapshot with Soul Bind

Participant stays dead.

Restore the snapshot Soul Bind state exactly.

This is not resurrection and does not generate a new corpse, soul or death event.

The reviewed temporal participant interface already singles out Soul Bind snapshot state. 
Pasted text

Knowledge

Snapshot allies remember what they actually perceived in every discarded timeline.

Control/allegiance rewinds to snapshot state.

No player choice is replayed automatically.

Preflight → commit → restore → cleanup

The executable transaction should be:

Snapshot phase at initiative

Build immutable snapshot.
Validate schema/dependency closure.
If incomplete, mark Time Loop unavailable for encounter.

Activation preflight

Verify owner/source/Reaction/LR use/round gate.
Verify atomic event boundary.
Build complete restoration plan.
Resolve identity lineage conflicts.
Validate environment/position plan.
Validate effect clock classifications.
Validate concentration dependency closure.
Confirm all world-unique IDs still refer to the expected records.

No mutation yet.

Commit

Spend Reaction.
Spend Time Loop LR use.
Allocate new iteration ID.
Persist those expenditures to conservation ledger.

Atomic restore

retire post-snapshot temporal children/derivatives;
restore environment anchors;
restore participant bodies/life/anatomy;
reconcile equipment against current inventory;
restore conditions/temp grants/effect records;
restore RC/per-encounter ledgers;
restore valid concentration records;
restore positions simultaneously;
restore initiative start state.

Post-restore overlays

reapply conserved finite-resource state;
reapply current inventory/ownership;
apply Time Loop Reaction-spent overlay;
close invalid post-snapshot death-bound records;
retain historical event/reward ledgers;
add temporal memories to eligible allies.

After a successfully validated plan, the actual restore procedure should be designed as total/nonthrowing. An implementation mismatch after commit is an engine error, not an in-world partial Time Loop.

Source evidence still required before implementation closure

This conference can specify the transaction, but several adapters still need exact source/runtime evidence rather than generic assumptions:

Canonical encounter registry: exact host API for hidden actors, staged reinforcements and later arrivals.
Geometry/environment serialization: authoritative encounter-region anchors, destructible terrain and occupancy conflict handling.
Physical identity lineage: corpse derivatives, undead raising, body reconstruction, harvested body materials and anchor-derived salvage.
Equipment/inventory provenance: authoritative ownership, consumption, destruction, drop and meld history.
Per-source temporal clock classification: especially long-lived zones, externally sourced concentration, Soul Bind pending vs bound states, Agony suppression, explicit hour/day effects and similar records.
Class-specific asset serializers: Ranger Beast/bonds, Mage elites, Wizard raised undead, Mirrorsage records, Soldier Palisades, Tinker persistent/deployable assets and any source whose state isn't already represented by shared ledgers.
Initiative/Reaction scheduler: atomic event boundaries, round restart and Reaction refresh semantics.
Environment-created derivative objects: exact handling of salvage/body-derived items so restoration never duplicates matter.
Knowledge/perception records: enough host evidence to distinguish what each ally actually perceived from Director-only state.

Those are required adapters/evidence, not reasons to invent new content.

Conference disposition

The Time Loop world transaction is now:

SOURCE-DISCUSSED / DRAFTABLE — finite world-state transaction specified; implementation and independent validation pending.

The original promise remains intact within a finite interpretation: the registered combat encounter returns to its initiative-start state, allies retain subjective memory, and the explicitly conserved expenditures/history do not rewind. The remaining work is executable serialization and source-specific adapters, not a license for arbitrary map-wide rollback or resource duplication.
