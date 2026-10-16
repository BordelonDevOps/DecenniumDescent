# Devices, Totems and companion commands

**REVIEWED / reference-VALIDATED: 132 targeted checks and 1,200 reconfiguration states.** This is the lifecycle and shared-command overlay for 74 supplied Tinker/Shaman passages and three frozen shared paragraphs. It does not certify all effects on those cards, all companions, or the whole game.

The [source register](DEVICE_LIFECYCLE_SOURCE_BINDINGS.md) preserves all exact procedures and hashes. The [source check](DEVICE_LIFECYCLE_SOURCE_VALIDATION.json) and [behavior check](DEVICE_LIFECYCLE_PLAYTEST_VALIDATION.json) cover this bounded package. The other 157 passages in the wider companion inventory are still open. Original sources and the frozen class guide remain unchanged.

The original names, costs, targets, rolls, damage, class gates and frequencies control. A label such as “device,” “deployed” or “support command” below is a classification, not an added ability. **NEW** marks an integration decision explicitly discussed with the notebook.

## At the table

Keep one card/token for each active device, Totem or companion. Record its current HP, expiry, occupied capacity, spent ammunition/uses and protected disablement. A persistent Anacite Drone also retains an ownership identity across reconstruction.

When a device reaches 0 HP, release its active slot and record what destroyed it. A destroyed Drone remains a recoverable machine. Standard summoned companions disappear. Totems stop their aura immediately. Expiry, dismissal, replacement and loss of concentration end effects without producing destruction rewards.

Repair is not reconstruction. Field Repair and Repair Pulse cannot bring a destroyed machine back. Snap Rebuild and the Drone's ten-minute repair can do so under their exact costs, ranges and limits. Snap must still fit the original slot footprint and beat the original expiry.

All companions belonging to one character share one Bonus Action command and one damaging companion action per numbered round. Separate tokens, multiclass companions, an extra Action or an extra turn do not reset those limits.

## Lifecycle and persistent state

Primary state is deployed, retracted, destroyed, expired, ended or replaced. Protected disablement is a separate flag. A disabled Drone can be retracted or destroyed; neither action clears the flag. An active entity functions only while deployed, before its expiry, above 0 HP if it has HP, available in its owner's configuration, and not disabled.

**NEW:** administrative ending releases capacity without destruction, refunds or salvage. Earlier destruction debris can remain after the original timer, but cannot be Snap Rebuilt at or after that timer. Inert remnants do not acquire collision, cover, terrain or repair rights without a source.

The Drone has an asset identity for ownership and configuration and an instance identity for the current physical incarnation. Ordinary repair, retraction, redeployment, Snap and Reconfiguration preserve that instance. A genuinely new paid deployment or explicit long-rest Drone rebuild uses a new instance.

Protected disablement belongs to the persistent Drone asset. A long-rest rebuild can therefore produce a full-HP Drone that remains disabled. The printed automatic clearance is a completed **short rest**; a long rest is not silently substituted for that marker.

## Commands, Reactions and damage allowances

| Event | Shared BA command | Shared damaging action | Other payment |
| --- | --- | --- | --- |
| Attack command | Spent | Spent | Printed costs |
| Support-only command | Spent | Available | Printed costs |
| Gadget Sync shot | Unchanged | Spent | Trigger and 1 RP |
| Decoy Dummy destruction damage | Unchanged | Spent if available | Automatic engine trigger |
| Default follow/move/Dodge | Unchanged | Unchanged | No attack granted |
| Emergency Protocols, Protective Programming, Magnetic Wall | Unchanged | Unchanged | Owner's printed Reaction |
| Volatile Components / Cinderflame destruction burst | Unchanged | Unchanged | Their own predicates and limits |

Gadget Sync after support may use the still-unspent damaging allowance. Gadget Sync first leaves a later BA support command available. Neither sequence grants a second damaging activation. Rocket Tower's two-target shot is one activation; Advanced Turret Bay does not command both turrets together.

**NEW scope clarification:** engine[6]'s damaging-trigger limit applies to its deployable profiles, including Decoy. It does not impose that limit on separately printed Volatile Components or Cinderflame. A suppressed Decoy trigger grants no damage and is not banked. An off-turn Decoy trigger still uses the current numbered-round allowance. Tinker BA commands also require their narrower regular-turn eligibility. Other timing/trigger legality is checked by the caller.

Nano Aegis uses a support command for each printed BA+1RP output; it cannot attack with that command. Its reviewed maximum of three outputs remains. Duration extensions do not restore ammo, uses or healing pulses.

## Durability and immunities

| Profile | Maximum / initial HP | AC | Stat timing |
| --- | --- | --- | --- |
| Anacite Drone | max(1, 5 + actual INT modifier + Tinker level) | 13 + actual INT modifier | Current actual owner values |
| Ordinary HP-bearing deployable | 2 × Tinker level | 12 + PB | NEW creation snapshot |
| Deployable Expertise on eligible object | Add M maximum/initial HP | Add 1 | Creation; excludes Drones |
| Totem, including Echo | 2 × Shaman level | 12 + PB | NEW placement snapshot |
| Named standard elemental | 2L; Harmony makes 3L | 12 + floor(PB/2) | Creation |
| Elemental Chorus package | 4L; Harmony makes 5L total | 12 + PB | Creation |
| Salvage / Reaper Scrapling | L | 12 | Creation |
| Restoration Field | No HP-bearing anchor | None | Slot effect |

A legitimate temporary actual INT change updates Drone AC, maximum HP and its current PB+INT attack bonus. Increased maximum supplies capacity without healing. Decreased maximum clamps current HP without damage or destruction. Finite created profiles keep their creation statistics.

Harmony adds HP at creation and one source turn of duration, capped at four. It does not heal an existing summon. Chorus is one shared package represented by four spirits. Echo's 10-foot radius and half aura numbers do not halve its durability.

Machines/Totem objects have no organic Wounds, Stable state or death saves. Legal temporary HP is a separate buffer. The Drone's printed poison/psychic and Charmed immunities do not imply every condition immunity. Totems have their own printed poison/psychic and condition immunities. “Vulnerable to ordinary weapon and other damage” means susceptible in this source wording, not an invented numerical doubling.

The reference's damage method receives an amount after all legally applicable defenses. Condition eligibility, object immunities, attack rolls, saves and exact riders remain caller work. A Shaman elemental is a creature companion, not automatically a machine.

Scraplings are temporary companions with their printed stats and shared command rules. Neither supplied Scrapling source establishes generic machine/device targeting. Salvage's slot cost does not grant that category. They disappear at zero HP and do not thereby gain Field Repair, Repair Pulse, protected-disable routing, Recycling, Volatile Components, Snap or other device-only permissions.

## Repair, reconstruction and disabling

| Procedure | Eligible target and change | Payment / limit |
| --- | --- | --- |
| Field Repair | Touched damaged machine with positive HP; or protected-disabled positive-HP machine, even at full HP. An available carried/retracted Drone qualifies. Restores rolled S d8+M up to max and clears protected disablement | Action, 1 RP, printed Recharge 2 |
| Repair Pulse | Up to three functional friendly devices; restores floor(maxHP/2), applies printed +1 AC until next source start. Does not clear protected disablement | Action, 3 RP, 1/short rest |
| Drone ten-minute reconstruction | Destroyed owned Drone with available original material; restores max(1, floor(maxHP/2)); preserves protected disablement | 10 minutes, 1 RP, 1/short rest |
| Snap Rebuild | Destroyed device/Drone, legal material, original free compatible slot footprint and remaining duration; restores max(1, floor(maxHP/2)); preserves disablement | BA, 2 RP, 1/encounter |
| Disable-clear tools procedure | Clears only protected-disable flag, including on a destroyed persistent machine; restores no HP | Separate 10 minutes, 1 RP, tinker's tools |
| Completed short rest | Clears protected disablement only | Actual completed short-rest marker |
| Long-rest Drone rebuild | Full HP, fresh physical instance for owned asset, even after old material consumed; preserves uncleared asset disablement | Actual source-authorized completed long rest |

**NEW machine viability arithmetic:** explicit half-maximum reconstruction has minimum 1 HP. Repair Pulse on a functional max-1-HP machine still restores floor(1/2) = 0.

The two ten-minute procedures are distinct rights. Reconstructing a disabled, destroyed Drone does not also buy disable clearance. Reconstruction is not a generic cleanse and does not reset ammunition, modules, spent uses, Overdrive history or unexpired legal effects. Normally damage has already consumed temp HP before destruction; this package adds no destroyed-machine temp-HP grant.

Routing Dissonance is the engine[7] BA, once/short rest, up to two current Dissonance into an active device within 30 feet. It creates no RP, does not reset Refrain, and blocks movement, attacks, auras and triggers while the device's timer continues.

## Capacity, placement and dependent Totems

Deployable slots are zero before the engine's class gate, one at Tinker 6, two at 13 and three at 17. Advanced Turret Bay uses two available slots for 4 RP, or its one-slot/2-RP fallback; zero free slots is illegal. Drones use separate persistent ownership capacity, not deployable slots.

At Tinker 13, choose exactly two basic Drones with exactly one module each or exactly one Drone with exactly two distinct modules during the printed configuration procedure. No more than two. Earlier module acquisition remains governed by its own class gates. **NEW:** withdrawing the excess Drone into an unavailable/retracted configuration causes no destruction or salvage.

Totem capacity is one, then two at Shaman 13. **NEW generalization:** an ordinary new Totem placed at capacity replaces a chosen active Totem, including at capacity one. Echo needs a separate free capacity; creating Echo alone never evicts another Totem.

**NEW dependent Echo rule:** ending, replacing, destroying or expiring the parent ends its Echo and releases both capacities. That Echo ending is administrative, not its own destruction. Ending only Echo leaves the parent. Echo shares the parent's remaining duration, concentration and upkeep.

Preflight ownership, source use, space/range, action, resources and capacity before payment or ending anything. Determine all dependent releases first. A valid parent replacement can free room for the new parent plus a separately paid Echo. If Echo cannot fit, its optional creation is unavailable; the caller can submit an ordinary parent-only placement instead. Failure of a submitted combined transaction changes nothing.

All active Totems share their concentration burden. Losing it ends their effects and dependent Echoes without destruction rewards. Totem movement follows its printed BA, 15-foot move through an open route within the printed range; it retains expiry, concentration, recipient ledgers and pulse schedule. Movement grants no entry heal.

## Destruction, debris and source-specific opportunities

Record the instance, original hostile cause, actual enemy hit versus transferred damage, deliberate sacrifice, whether the object itself is a copy, friendly damage, secondary explosion and inherited branch flags at destruction. Separately record whether incoming damage was copied. A real device destroyed by copied damage still has ordinary destruction consequences; only that damage's actual restriction flags suppress them. “Copied object” exclusions do not mean “any object damaged by a copy.”

**NEW anti-loop integration:** the first actual destruction of an instance establishes its only object-linked opportunity and material set. Nonqualifying and declined opportunities are closed for that instance. Snap does not create another set. A second physical destruction still ends the rebuilt device but cannot supply another harvest, Volatile opportunity or material record.

Recycling, Salvage, Reaper and Snap share the usable original material. The first successful consumer spends it. Volatile does not consume material. A source-qualified Volatile can therefore precede one legal material consumer. Declining Volatile on Device A does not spend the owner's round allowance for Device B.

| Source | Important predicate |
| --- | --- |
| Efficient Recycling | Your destroyed non-copy device; not deliberate sacrifice; debris within reach, after combat for one minute, 1/short rest. Refund at most min(1 RP, actual deployment RP). Enemy cause is **not required**. |
| Scrap Salvage | Enemy-destroyed qualifying material; Action+1 RP, 1/encounter; one slot-using Scrapling at printed location |
| Scrap Reaper | Qualifying destroyed enemy-hit device/material within 30 feet; Reaction+2 RP, 1/short rest; printed short-lived Scrapling uses **no deployable slot** |
| Volatile Components | First enemy-caused device destruction; excludes deliberate sacrifice, copy, friendly damage and secondary explosion; enemy within 5 feet; once per owner/round |
| Snap | Original destroyed instance/material, original footprint free and original expiry not reached |

Scraplings cannot spawn their own replacement. Reaper still uses the later BA command and damaging-action budget for its detonation. Its absent slot cost is not inferred from the separate Salvage card. Reaper also carries its source's broader no-own-destruction-chain property; a later type ruling must not silently remove that protection.

Inherited noResourceGeneration blocks Recycling refunds. It does not automatically prohibit all non-resource transformations. Inherited noRetaliation blocks a destruction explosion such as Volatile. Inherited noDeathTriggers blocks Volatile, Cinder's destruction burst and Reaper's destruction-triggered Reaction. It does not automatically prohibit the later Action-based Scrap Salvage or ordinary Recycling. Source-specific exclusions still apply to each consumer.

Cinderflame's qualifying destruction event is captured before its standard-companion disappearance. Its printed burst may then resolve, with the printed three-enemy cap, save, damage and no further death/resource triggers. Dismissal, expiry and concentration ending are not destruction.

Volatile Injection spends M **normal** device HP and requires current HP strictly greater than M. Temp HP cannot pay it. It is not damage or a qualifying destruction event. Deliberate sacrifice sources retain their express no-proc/salvage/copy/refund exclusions.

## Magnetic Wall and existing damage sharing

**NEW source binding and timing integration:** when the printed ranged weapon hit, ally distance and wall-line predicates hold, the owner's Reaction transfers exactly min(remaining defended damage, S+M) to the functional Wall after the ally's ordinary defenses/prevention and before temp HP.

The transfer retains damage type. The Wall branch carries noSecondMitigation and noRetransfer. It receives no second AC roll, critical, attack-hit rider or second mitigation pass. Legal Wall temp HP then normal HP absorb it; reaching zero destroys it and releases its slot.

Enemy damage intercepted this way remains enemy-caused. Choosing the Reaction is not deliberate sacrifice. A Wall destroyed this way may qualify Volatile and a source-qualified material consumer. Transferred damage is not itself an attack hit on the Wall; enemy-hit-only Reaper qualification remains distinct.

Emergency Protocols retains its existing additional noRetaliation flag. Enemy attribution and ordinary debris survive, but destroying the Drone cannot bypass that flag to trigger Volatile. This new Magnetic Wall binding supplements the earlier 39-source redirection package; it was not part of that package's original count.

## Reconfiguration and implementation boundaries

Reconfiguration requires a functional deployed device and a known eligible nonhealing destination. **NEW arithmetic:** newHP = max(1, floor(oldHP × newMaxHP / oldMaxHP)), capped at new max. Preserve instance, slot footprint, expiry, ammunition, spent uses, destruction history and effect clocks. This conversion is neither damage nor healing.

Pending modifiers only apply when their own predicate remains true. Overcharge grants no free command; a profile unable to use it does not refund it or reset its deadline. Exact source access, profile legality and pending-modifier application remain caller responsibilities.

Restoration Field is a slot-using concentration effect with its already-reviewed healing scheduler. Its source supplies no HP, AC or physical anchor. It cannot be attacked as a fabricated machine, repaired, Snap Rebuilt, Remote Detonated, used for Volatile Injection/salvage or targeted by protected Dissonance routing merely because it consumes a slot.

The implementation stores authoritative owner/instance/material identifiers, original ClockMarkers, canonical command ledgers, atomic RP/action payments and explicit source-scoped use keys. The caller must provide the same real owner wallet and ledger across abilities, unique use-scope keys tied to the real rest/encounter calendar, legal source actions and costs, actual targets/geometry, source profiles and class gates. It must also propagate these life states to the pulse/concentration engine.

All timed device effects supplied here expire during a completed long rest, explaining the fresh Drone instance's empty timed-effect list and zero tempHP. This is not a generic reconstruction cleanse: a future permanent or long-rest-surviving source effect must retain its own clock and rules.

This reference does not create a complete runtime transaction manager, movement/collision system, all damage riders, every condition interaction, all 157 remaining companion candidates or a video game. It supplies the same decisions in tabletop prose and a precise checked model for later implementation.

## Discussion evidence

Saved in docs/audit/2026-10-08/full-game:

- GPT_DEVICE_LIFECYCLE_FIRST_REVIEW.md: complete initial 74-source classification.
- GPT_DEVICE_LIFECYCLE_BOUNDARIES.md: state, identity, repair, capacity, commands and Field corrections; controls over conflicting initial proposals.
- GPT_DEVICE_LIFECYCLE_PREDICATES.md: Recycling correction, first-actual-destruction anti-loop rule, distinct ten-minute procedures and persistent disablement.
- CODEX_DEVICE_LIFECYCLE_IMPLEMENTATION_REVIEW.md: exact candidate and tests submitted for disposition.

[Final notebook disposition](../../../../docs/audit/2026-10-08/full-game/GPT_DEVICE_LIFECYCLE_FINAL_CLOSURE.md) closes only this supplied 74+3 interface. Human balance and whole-game completion remain separate.
