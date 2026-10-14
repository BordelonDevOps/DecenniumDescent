# GPT completed twelve Time Loop boundary decisions

ChatGPT said:

The attachment resolves several ambiguities from the first Time Loop conference. The largest correction is that logical combat time can rewind without rewinding elapsed world time. That means some encounter permissions receive fresh iteration-qualified turn/round identities, while explicit elapsed-time records such as Soul Bind, Agony, the promoted transformation spells, and persistent resource ledgers keep their real deadlines/history. The original Boon V still promises an encounter reset and ally memory, while the reviewed card explicitly conserves per-rest resources, consumables, loot ownership, and its own use. 
Pasted text

Reward opportunity identity — conserve the opportunity, not the death event. Use a permanent key such as RewardOpportunityKey(encounterOriginId, immutableRewardSourceId, opportunityKind, opportunitySlotId). immutableRewardSourceId is normally the original participant/body/environment anchor that owns the reward opportunity; opportunityKind distinguishes XP, treasure, harvest, quest-credit, etc.; opportunitySlotId distinguishes multiple genuinely separate source-authorized rewards from the same entity, such as independently defined harvest slots. Claim state is conserved across every Time Loop iteration. Killing the same snapshot foe again with a fresh deathEventId therefore creates a new combat event but not a new XP/treasure/harvest entitlement. If the first discarded timeline already claimed the opportunity, the re-kill yields no second claim. A genuinely independent reward requires a genuinely different immutable source/opportunity authorized by its source, not merely a new iteration, event ID, corpse, transformation, or regenerated body. Post-snapshot generated summons/created farming bodies remain subject to the existing no-farm rules and do not acquire a reward opportunity merely because they exist. This is a NEW conservation bridge required by the source's “no duplicate XP, treasure or consumables” promise. 
Pasted text

Restored one-shot effects — preserve root identity and historical audit, but give each timeline its own consumption view. Canonical effectId never changes. Historical eventIds and historical consumption records are never deleted. Add a separate TemporalConsumptionKey = (effectId, timelineIterationId) or equivalent temporal generation. At snapshot, record whether the one-shot permission/rider was available or already consumed. On rewind into a new iteration:

snapshot-unconsumed → same effectId, available in the new iteration view;
snapshot-consumed → same effectId, still consumed;
consumption that occurred only in a discarded later iteration remains in audit history but does not mark the restored snapshot view consumed.

This applies to Agony's next-heal reducer, linked buffer riders, marks, form riders and equivalent one-shot state. It is privileged temporal restoration: no new offer, cast, entry trigger, source cost, or new effect ID occurs. Any finite cost needed to use the restored permission must still be paid from the current conserved resource state.

HealingCommitLedger.committed_event_ids stays globally historical. consumed_reducer_ids cannot remain the sole source of present availability when Time Loop is active; either the ledger must accept a composite temporal consumption token or TemporalWorld must supply an iteration-qualified application token while separately retaining the canonical effectId. Blindly deleting old consumption is wrong, and blindly carrying it forward is also wrong. 
Pasted text
 The same principle applies to generic one-shot state holders already present in the control/healing modules. 
Pasted text

Reaction debt — preserve every outstanding Time Loop Reaction debt, not merely the newest Oracle's. Maintain TimeLoopReactionDebt[oracleId]. Committing Time Loop creates that Oracle's debt. A later Time Loop restores snapshot Action/Reaction budgets and then overlays all debts still outstanding. Oracle A therefore remains unable to use another Reaction if Oracle B loops before A reaches the canonical Reaction refresh. A debt clears only when that Oracle experiences the same real scheduler event that ordinarily refreshes their Reaction — for this interface, the owner's next actual normal regular-start Reaction refresh. A debt already legitimately cleared before a later loop remains cleared; Time Loop does not resurrect old debt. Extra Actions do not clear it, and the rewind itself does not clear it. This is a NEW overlay required to keep the 1/LR Reaction expenditure conserved while still rewinding encounter action state. 
Pasted text

Logical turns versus world time — fresh iteration-qualified combat windows, conserved elapsed-time clocks. Introduce:

IterationRoundId = (encounterId, iterationId, roundNumber)
IterationTurnId = (encounterId, iterationId, actorId, turnOrdinal/type)
a separate monotonic global/world regular-marker sequence for actual clock systems.

The new iteration's round 1 is immediately playable after atomic restoration; the engine does not wait six world seconds before anyone can act, and the rewind itself triggers no start-of-turn/periodic tick.

Encounter-logical once-per-turn/round rules receive fresh identities in the new iteration:

Necrotic Affinity's once-per-turn melee die can qualify on a genuine new iteration turn;
Empowered Summoning's first rolled damage in round 1 can qualify under the new IterationRoundId;
command/offense budgets restart from their snapshot encounter state;
Lifeleech may qualify again for an ongoing spell root that actually existed at snapshot because the new round-window ID is different, but its finite Recovery Reserve remains spent/current.

Old events remain historical and cannot be replayed for rewards/resources.

Important correction to my first Time Loop draft: continuous recharge clocks are not automatically “per-encounter uses.” The reviewed Druid OwnerRechargeClock spans initiative and downtime and must remain conserved. Its ticks, phase and due marker are not reset merely because encounter labels restart. The first post-loop regular turn is a new logical turn, but the Druid recharge clock receives the next real scheduler marker and may tick only under its already-reviewed clock rules; Time Loop creates no free recharge tick at the rewind instant. The frozen class rules distinguish regular-turn Recharge from encounter declarations and six-second outside-combat ticking. 
Pasted text
 
Pasted text

Per-source clock policy — use the following explicit table, not duration-length inference.

Source/state	Temporal policy
Pending living Soul Bind, 60s	WORLD_ABSOLUTE. Preserve original expiry; never rebase. If already expired at rewind, it does not become pending again.
Bound-dead Soul Bind, 24h	WORLD_ABSOLUTE, death-instance bound. If the associated post-snapshot death is undone, that later bound record becomes historical/inactive. A bound record already present at snapshot keeps its original expiry.
Necrotic Affinity death seal, 24h	WORLD_ABSOLUTE, exact death-instance. Undoing that post-snapshot death closes the seal's active applicability; dead-at-snapshot seals keep original expiry.
Agony healing suppression, 60s	WORLD_ABSOLUTE + snapshot one-shot state. If snapshot-unconsumed and still before original expiry, it may be available in the new temporal consumption view. If expired, it does not return.
Chef potent food, 24h or owner's next LR	WORLD_ABSOLUTE AND REST_EPOCH. Physical food/inventory is conserved. Consumed/discarded food never returns.
Chef/Inspiring recipient-family entitlement	CONSERVED REST_EPOCH HISTORY. Never rewound. An offer already received in the same real LR epoch remains spent across loops.
Blood Ritual self default-LR shield	SNAPSHOT THP + REST_EPOCH. Restore snapshot amount only if the original grant remains valid in the current real recipient epoch. No new grant/ritual occurs.
Blood Ritual curse/disease rider	SNAPSHOT ONE-SHOT + REST_EPOCH. Consumption can rewind to snapshot state via temporal generation, but the real LR epoch never rewinds.
Blood Ritual ally 1h shield	SNAPSHOT THP + WORLD_ABSOLUTE. Restore remaining snapshot THP only while the original one-hour endpoint is still in the future.
Field Medic default-LR shield	SNAPSHOT THP + REST_EPOCH.
Empowered Summoning creation shield	SNAPSHOT THP + REST_EPOCH + ENTITY DEPENDENCY. Same summon lineage only; no new creation event.
Soul Cage 2d8 shield	SNAPSHOT THP + REST_EPOCH. Charges remain conserved/spent.
Core Stable d4-hour recovery	WORLD_ABSOLUTE. Never schedule the same recovery event twice. If its deadline already resolved in discarded history, restoring Stable/HP state cannot retrigger that resolved recovery.
Druid form duration	WORLD_ABSOLUTE source duration, not reset merely because combat rewinds. Restore the same form instance only if its actual source endpoint is still valid. Dependent form effects cannot outlive an invalid form.
Polymorph/Mass/Shapechange	WORLD_ABSOLUTE 60-second endpoint, as already promoted. Do not rebase.
True Polymorph shaping	WORLD_ABSOLUTE stabilization checkpoint. A record that has legitimately passed its checkpoint cannot be de-stabilized by Time Loop.
Permanent True Polymorph	PERMANENT record, subject to current external suppression/identity reconciliation.
Per-rest/daily/weekly resets	CONSERVED REST/WORLD EPOCH. Never rewound.
Explicit “next regular turn” effects	ITERATION_LOGICAL marker policy when that exact source is reviewed as turn-relative, not because it happens to be ~6 seconds.

If a WORLD_ABSOLUTE record's deadline already resolved, Time Loop may restore surrounding participant state but must not replay that world event. Historical resolution identity stays conserved. If restoring the containing state would require the expired event to fire again to become legal, the source adapter must supply a specific reconciliation; otherwise snapshot preflight fails. This is especially important for Stable recovery and similar delayed resolutions. Soul Bind already has explicit finite pending/bound states rather than an encounter-relative clock. 
Pasted text
 The promoted transformation package likewise uses absolute 60-second checkpoints and conserved underlying identity. 
Pasted text

Maximum HP/current inventory — snapshot HP is restored against the legal maximum that exists now. Snapshot maximumHP is evidence, not blindly authoritative. Procedure:

restore snapshot life/death/Wounds and rewindable max-HP modifiers;
retain current conserved level, ability scores, feats, permanent progression, current physical inventory/ownership and current nonrewindable external modifiers;
recompute effectiveMaximum using the already-reviewed max-HP rules;
assign restoredHP = min(snapshotHP, currentEffectiveMaximum).

If the current legal maximum is lower because gear was destroyed/transferred or another conserved source disappeared, clamp snapshot HP downward. That clamp is temporal normalization — not damage, healing, Wound generation, resource generation or a damage event.

If the current maximum is higher, do not scale or raise HP; restore the numeric snapshot HP unless another exact Time Loop field says otherwise.

The Critical healing ceiling does not cap this assignment because Time Loop restoration is not ordinary healing. Restore snapshot Wounds independently, then use the legal max-HP recomputation.

XP, level, ASI and feat acquisition are conserved progression and do not rewind. Reward-opportunity conservation prevents obtaining the same reward twice. A mid-encounter progression change that changes the participant schema/source set is an explicit structural divergence: unless there is a reviewed temporal adapter for that progression event, Time Loop preflight fails rather than manufacturing initial per-encounter state for a newly acquired feature. 
Pasted text
 The existing LifeState holder contains current/max HP but that field list itself is not permission to deepcopy stale maximum HP. 
Pasted text

Off-scene concentration and external effects — dependency closure does not make an external caster a rewind participant. Define two roles:

FullParticipant: body/HP/position/state may rewind.
ExternalDependency: only its current source/effect/concentration references may be consulted.

A nonparticipant caster included only because a participant snapshot effect depends on it does not have their body, HP, position, memory, resource state or concentration slot rewound.

For a snapshot effect dependent on external concentration:

if the exact same external concentration record is still active and compatible, the participant can reference it;
if that external caster ended/replaced concentration after the snapshot, Time Loop cannot silently recreate the old slot/effect;
unless the effect source explicitly survives independently, that dependency makes restoration impossible and preflight fails.

A persistent effect applied after snapshot by an unrelated nonparticipant is conserved as a current external record. Restore the participant's rewindable baseline, then overlay/reconcile the external effect. Do not erase it merely because it wasn't in the snapshot. If it changes anatomy, maximum HP, control, suppression or placement in a way that cannot coexist with the proposed restored state, preflight fails. Never silently end or rewrite the unrelated caster's concentration. 
Pasted text

Physical derivatives — use a transitive provenance graph and distinguish reversible entities from conserved inventory. Every physical derivative that can intersect restoration needs:

immutable root physical IDs;
derivation event/root;
whether it is a surviving discrete entity/item;
current owner/controller;
independent ingredients/material roots.

Retire automatically only a post-snapshot TEMPORAL_DERIVATIVE_ENTITY whose whole physical identity derives from a rewindable participant/environment root and whose source is inside the temporal closure — e.g. a raised corpse-body, temporary body-object, encounter-created structure. Its creation resource remains spent. Current control alone does not create a second physical entitlement.

Do not silently retire conserved transferable inventory/loot. If a corpse part harvested after snapshot still exists as an item — especially if transferred/sold to a nonparticipant — restoring the complete snapshot body would duplicate physical matter while removing the item would violate conserved loot ownership. Unless an exact adapter can reconcile it without changing conserved ownership, preflight fails.

For a mixed crafted item containing both root-derived matter and unrelated ingredients, generic TemporalWorld may not uncraft it. If a source-specific provenance adapter can safely separate/reconcile the root contribution, use that; otherwise preflight fails. Unrelated ingredients/payments remain spent either way.

If the root-derived material was already actually consumed and no independent physical derivative survives, do not refund or recreate that consumed item; the body may still be restored because the consumed resource remains spent rather than surviving as a duplicate object.

A derivative under a nonparticipant's control may be retired only when the derivative itself is a registered rewindable entity and its removal does not mutate that nonparticipant's unrelated body/resources/source slot. If its external binding/source would also need alteration, preflight fails.

Environment restoration has the same external-protection rule: even without literal cell overlap, restoring/removing a wall/floor/door may not drop, crush, enclose, trap, forcibly move or otherwise change a nonparticipant's physical state. Any such consequence blocks preflight. The verified geometry only authorizes existing movement/space rules, including squeezing one size smaller; it does not supply a generic involuntary-growth/overlap solution. 
Pasted text
 
Pasted text

Persistent assets — conserve enrollment; rewind encounter state only for the same still-valid asset identity. Add a distinction:

PersistentAssetEnrollment: bond/elite/pet/asset/slot membership — conserved unless the exact source says it is encounter-only.
EncounterAssetState: HP, position, temporary state, encounter conditions/deployment posture — rewindable when the same asset remains enrolled.
AssetFiniteResources: charges/ammo/rest uses/materials — conserved.

Examples:

Ranger Beast: if the current bond still points to the snapshot Beast, restore its encounter state. If a later legal rebond changed the enrolled Beast, do not undo that bond. The old snapshot Beast may only be restored as an ordinary physical participant if its identity still legally exists; it does not regain the bond for free.
Mage elite/persistent pet: same rule: current persistent enrollment wins; encounter state rewinds only for that asset.
True Polymorph object-creature sponsor slot: current slot occupancy/sponsor validity must reconcile. If snapshot restoration would require restoring an old object-creature while a different current persistent occupant legally owns the same slot, do not double the slot or overwrite the new persistent identity. If the current occupant is itself a fully reversible post-snapshot temporal derivative that can lawfully return to its underlying state, the source adapter may free it; otherwise preflight fails.
Wizard raised undead/corpse lineage: use the physical-provenance rules from #8. Snapshot undead can rewind only without cloning/reusing a corpse lineage now committed elsewhere.
Mirror/device slots: source adapter distinguishes encounter-local deployed state from persistent reserved asset identity/capacity; do not generically copy a slot map.

This is a NEW source-aware reconciliation rule. The existing lifecycle packages already separate asset IDs, controllers, slots, corpse identities, command groups, stock, destruction and rebuild histories; Time Loop must use those semantics rather than overwrite them with a generic snapshot. 
Pasted text
 
Pasted text

Gear on restored forms — restore meld membership only for items that still legally exist with that identity; preserve later external gear separately. For a snapshot form/transformation:

restoredMeldSet = snapshotMeldSet ∩ currentExistingItems ∩ itemsStillOwned/HeldByParticipant
transferred/lost/destroyed/consumed items never reappear;
an item currently owned by somebody else stays there;
later-acquired external gear that is compatible with the restored anatomy remains external and usable; it does not become part of the old meld set;
incompatible current external gear is dropped atomically under the already-reviewed transformation placement rule, with no new form-entry/recapture hook.

All drop placements must be included in Time Loop preflight. If the item cannot occupy the participant's restored anchor or an already-authorized legal adjacent drop location without changing a protected nonparticipant/environment state, Time Loop is unavailable/unspent.

Restoring the anatomy does not fire:

form entry;
spell cast;
meld recapture;
resource reset;
buffer grant;
summon/deploy hooks.

Suppression is reconciled in two layers. Restore the rewindable snapshot source record, then apply current conserved external suppression such as ongoing antimagic. Snapshot “unsuppressed” cannot bypass an antimagic field that currently exists outside the temporal rollback. Conversely, a rewindable suppression source that existed at snapshot may restore if its source is itself in scope. Any resulting root/form anatomy placement must already pass preflight. This follows the promoted transformation rule that melded gear is identity-conserved and suppression does not recapture it. 
Pasted text

Memory and PvP — supernatural character memory is Oracle/alliance-specific; human player knowledge is not engine state. For each Time Loop activation define:
TemporalMemoryEligible(invokingOracle, character) = character == invokingOracle OR character was an ally of that Oracle at the immutable encounter snapshot.

Because the shared rules treat “ally” as including self unless explicitly excluded, the Oracle retains their own discarded-timeline memory. 
Pasted text

A player-character enemy in a PvP encounter who was not the invoking Oracle's snapshot ally does not receive supernatural in-character memory from that Time Loop, even though the human player obviously remembers what happened at the table. The engine cannot erase human knowledge, but it does not mark the character as knowing facts they were not source-eligible to retain.

Memory is cumulative across loops:

Oracle A's eligible allies keep memories from A's discarded iteration;
later Oracle B can grant additional retained memories to B's own snapshot-allied set;
later allegiance/control changes do not retroactively alter either eligibility set.

Each eligible character retains only facts that character actually perceived, experienced or was told. Hidden roster entries, unrevealed enemies, Director-only information, unseen rolls and unobserved actions do not leak from the snapshot serializer into character knowledge.

Memory never dictates behavior. No previous choice is replayed, and no player or NPC is forced to “correct” the timeline. The original source specifically frames memory as enabling different choices. 
Pasted text

Minimum TemporalWorld adapters and additional source evidence. character-storage.js should not be used as the canonical world rollback mechanism. The attached inventory correctly shows that state is distributed across many real holders and that field existence alone does not establish rewind semantics. 
Pasted text

The minimum implementation adapters I would require before calling the authored Time Loop reference complete are:

initiative/iteration scheduler adapter: round/turn identities, Reaction debts, command/offense/extra-Action budgets, global regular-marker/recharge phase;
Core life/max-HP/Stable adapter;
BufferLedger adapter for grant identity, remaining THP, dependency/rider state and rest-epoch validity;
temporal one-shot/HealingCommit adapter for historical audit versus iteration consumption view;
SoulBind/revival/identity-return adapter;
ConcentrationLedger + TransformationWorld adapter;
DruidState/FormInstance/OwnerRechargeClock adapter;
CreatureWorld/corpse/body-lineage/persistent-asset adapter;
device Lifecycle/Entity/Destruction/CommandLedger adapter;
RemainingWorld structures/Choir/Undeath/Palisade/Ledger-control adapter;
FeatWorld adapter for Soul Charges, Lifeleech reserve/histories, Necrotic seals, Agony, recipient-family/rest histories and summon lineages;
healing-pulse/control-state adapter for active marks, one-shot riders and pulse-series state;
physical inventory/provenance adapter;
environment-anchor/geometry adapter;
reward-opportunity ledger;
external dependency/concentration adapter;
temporal-memory/perception overlay.

No additional class cards are required before writing the framework and adapters for the already-reviewed lifecycle, Druid/form, transformation, healing/death, device/remaining-lifecycle and eight-feat packages. Their reviewed packages already supply the source semantics needed for those domains.

However, snapshot completeness must reject any active state-holder whose exact source cannot yet be mapped to a temporal policy. The first likely families needing exact source evidence if their existing review packets do not already provide a source-ID mapping are:

SpeedRecord
GuidingStarMark
WrathfulBrand
generic OneShotRider
PerTurnReflection
PulseSeries
BloomReserve
FirstContactLedger
NativeOccurrenceLedger

Their holders do not, by themselves, prove whether a record is world-absolute, turn-relative, per-encounter, rest-bound, or consumable. If the existing control/pulse review source registry already maps those instances to exact source IDs and lifecycle rules, use that registry and no new class-card packet is necessary. If it does not, those exact source records are the next evidence I would request before permitting such an instance in a “complete” Time Loop snapshot. The same rule applies to any future unsupported source: it makes that specific snapshot unavailable rather than opting in through an unchecked boolean. 
Pasted text
 
Pasted text

These decisions leave Time Loop at:

SOURCE-DISCUSSED / IMPLEMENTATION-READY — twelve concrete world-conservation boundaries reconciled; actual TemporalWorld code, adapters and adversarial validation still require independent review.

This does not satisfy the owner's final project gate. Even after Time Loop receives its own bounded closure, there is still no authorized GitHub push until the final joint whole-game flow review confirms the authored game flows correctly as a whole. 
Pasted text
