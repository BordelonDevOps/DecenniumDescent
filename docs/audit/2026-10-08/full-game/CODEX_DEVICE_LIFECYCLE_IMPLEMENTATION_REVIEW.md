# Exact device lifecycle implementation review

Codex → Calibration Review. Please review the exact candidate against all 74 supplied class source roles and three frozen shared paragraphs. Source cards, books and frozen class guide are unchanged. Reply under 15,000 characters and identify concrete defects before disposition.

Current verification: 104 targeted adversarial checks and 1,200 reconfiguration-state cases pass. Source integrity separately verifies 74+3. This bounded package covers life/deployment state, protected disablement, repair/reconstruction, original material identity, slot replacement and Echo dependencies, command/damage budgets, creation/dynamic stats and Magnetic Wall's newly bound transfer. Other effects on the same cards and the other 157 lifecycle candidates remain open.

Important caller boundaries are explicit, not completion claims: actual source access/class gates, known eligible profiles, range/space/LOS, actual rolls and damage defenses, source recharge/encounter/rest calendar and use keys, authoritative owner wallet/command ledger, standard movement/collision, concentration/pulse propagation, module riders and remaining individual card effects. Placement validates state/capacity/payment but receives already source/geometry-legal entities and costs. This is a rules reference for tabletop and later engine implementation, not a full video game.

Please check especially:

1. First actual destruction locks the instance's only material/opportunity set. Snap and ten-minute Drone reconstruction consume that material and cannot manufacture another first-event entitlement. Fresh explicit LR Drone incarnation is a new instance but carries asset disablement. The two ten-minute procedures remain separate.
2. Efficient Recycling now matches your correction: friendly/accidental destruction can qualify; sacrifice/copy and noResourceGeneration block. Salvage and Reaper keep distinct hostile/actual-enemy-hit predicates.
3. Magnetic Wall branch is not an attack hit, so a Wall destroyed purely by transferred enemy damage is enemy-caused for Volatile/Salvage but does NOT satisfy Scrap Reaper's stricter enemy-hit source wording. Confirm this consequence, or give the exact intended source override; none has been silently added.
4. Off-turn automatic Decoy damage uses the owner numbered-round damage allowance without a BA. Only Tinker BA commands impose regular-turn eligibility in the helper; Gadget Sync still needs its actual printed trigger checked by caller. No passive Cinder/Volatile charge against command allowance.
5. noDeathTriggers now blocks Cinder/Volatile destruction bursts. The Reaper helper currently enforces hostile enemy-hit/no-sacrifice/copy/friendly/secondary and no-self-replacement predicates. Does inherited noDeathTriggers also bar Reaper's Reaction while leaving later active Salvage distinct? Does any exact source forbid that active material transformation too? Avoid widening noResourceGeneration to all transformations.
6. Scrapling no-self-replacement is enforced for Salvage/Reaper, but is not broadened to an unrelated Volatile exclusion beyond its printed friendly/copy/sacrifice/secondary bans. Is a first genuine enemy destruction of a Salvage Scrapling allowed to use separately owned Volatile, subject to no-chain flags? Also clarify Recycling of that new Scrapling under its exact deployment payment provenance if needed.
7. The bounded helper models positive-HP repairs and preserves tempHP/module/ammo/effect clocks. Normal damage consumes tempHP before object death. LR Drone rebuild clears old timed effects and gives zero tempHP; source-authorized long-rest use resets remain a separate canonical rest operation. Confirm whether source-effect clocks need further retention across LR instance replacement.
8. Check the source aliases/stat/capacity table and anti-loop implications rather than granting blanket full-card closure. Guide has NEW integration labels; no new named abilities.

If correct, explicitly dispose of the 74 supplied lifecycle/command roles plus3 shared paragraphs and state remaining scope. If anything needs correction, return the smallest exact counterexample.


## docs/mechanics/DEVICE_LIFECYCLE_PLAYTEST.md

# Devices, Totems and companion commands

**Implemented candidate; exact GPT implementation review pending.** This is the lifecycle and shared-command overlay for 74 supplied Tinker/Shaman passages and three frozen shared paragraphs. It does not certify all effects on those cards, all companions, or the whole game.

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
| Named standard elemental | 2L; Harmony makes 3L | 12 + PB | Creation |
| Elemental Chorus package | 4L; Harmony makes 5L total | 12 + PB | Creation |
| Salvage / Reaper Scrapling | L | 12 | Creation |
| Restoration Field | No HP-bearing anchor | None | Slot effect |

A legitimate temporary actual INT change updates Drone AC, maximum HP and its current PB+INT attack bonus. Increased maximum supplies capacity without healing. Decreased maximum clamps current HP without damage or destruction. Finite created profiles keep their creation statistics.

Harmony adds HP at creation and one source turn of duration, capped at four. It does not heal an existing summon. Chorus is one shared package represented by four spirits. Echo's 10-foot radius and half aura numbers do not halve its durability.

Machines/Totem objects have no organic Wounds, Stable state or death saves. Legal temporary HP is a separate buffer. The Drone's printed poison/psychic and Charmed immunities do not imply every condition immunity. Totems have their own printed poison/psychic and condition immunities. “Vulnerable to ordinary weapon and other damage” means susceptible in this source wording, not an invented numerical doubling.

The reference's damage method receives an amount after all legally applicable defenses. Condition eligibility, object immunities, attack rolls, saves and exact riders remain caller work. A Shaman elemental is a creature companion, not automatically a machine.

## Repair, reconstruction and disabling

| Procedure | Eligible target and change | Payment / limit |
| --- | --- | --- |
| Field Repair | Functional damaged machine; or protected-disabled living machine, even at full HP. Restores rolled S d8+M up to max and clears protected disablement | Action, 1 RP, printed Recharge 2 |
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

At Tinker 13, choose two basic Drones with one module each or one Drone with two distinct modules during the printed configuration procedure. No more than two. **NEW:** withdrawing the excess Drone into an unavailable/retracted configuration causes no destruction or salvage.

Totem capacity is one, then two at Shaman 13. **NEW generalization:** an ordinary new Totem placed at capacity replaces a chosen active Totem, including at capacity one. Echo needs a separate free capacity; creating Echo alone never evicts another Totem.

**NEW dependent Echo rule:** ending, replacing, destroying or expiring the parent ends its Echo and releases both capacities. That Echo ending is administrative, not its own destruction. Ending only Echo leaves the parent. Echo shares the parent's remaining duration, concentration and upkeep.

Preflight ownership, source use, space/range, action, resources and capacity before payment or ending anything. Determine all dependent releases first. A valid parent replacement can free room for the new parent plus a separately paid Echo. If Echo cannot fit, its optional creation is unavailable; the caller can submit an ordinary parent-only placement instead. Failure of a submitted combined transaction changes nothing.

All active Totems share their concentration burden. Losing it ends their effects and dependent Echoes without destruction rewards. Totem movement follows its printed BA, 15-foot move through an open route within the printed range; it retains expiry, concentration, recipient ledgers and pulse schedule. Movement grants no entry heal.

## Destruction, debris and source-specific opportunities

Record the instance, original hostile cause, actual enemy hit versus transferred damage, deliberate sacrifice, copy, friendly damage, secondary explosion and inherited branch flags at destruction.

**NEW anti-loop integration:** the first actual destruction of an instance establishes its only object-linked opportunity and material set. Nonqualifying and declined opportunities are closed for that instance. Snap does not create another set. A second physical destruction still ends the rebuilt device but cannot supply another harvest, Volatile opportunity or material record.

Recycling, Salvage, Reaper and Snap share the usable original material. The first successful consumer spends it. Volatile does not consume material. A source-qualified Volatile can therefore precede one legal material consumer. Declining Volatile on Device A does not spend the owner's round allowance for Device B.

| Source | Important predicate |
| --- | --- |
| Efficient Recycling | Your destroyed non-copy device; not deliberate sacrifice; debris within reach, after combat for one minute, 1/short rest. Refund at most min(1 RP, actual deployment RP). Enemy cause is **not required**. |
| Scrap Salvage | Enemy-destroyed qualifying material; Action+1 RP, 1/encounter; one slot-using Scrapling at printed location |
| Scrap Reaper | Qualifying destroyed enemy-hit device/material within 30 feet; Reaction+2 RP, 1/short rest; printed short-lived Scrapling uses **no deployable slot** |
| Volatile Components | First enemy-caused device destruction; excludes deliberate sacrifice, copy, friendly damage and secondary explosion; enemy within 5 feet; once per owner/round |
| Snap | Original destroyed instance/material, original footprint free and original expiry not reached |

Scraplings cannot spawn their own replacement. Reaper still uses the later BA command and damaging-action budget for its detonation. Its absent slot cost is not inferred from the separate Salvage card.

Inherited noResourceGeneration blocks Recycling refunds. It does not automatically prohibit all non-resource transformations. Inherited noRetaliation blocks a destruction explosion such as Volatile. No-death-trigger restrictions continue into death riders. Source-specific exclusions still apply to each consumer.

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

This reference does not create a complete runtime transaction manager, movement/collision system, all damage riders, every condition interaction, all 157 remaining companion candidates or a video game. It supplies the same decisions in tabletop prose and a precise checked model for later implementation.

## Discussion evidence

Saved in docs/audit/2026-10-08/full-game:

- GPT_DEVICE_LIFECYCLE_FIRST_REVIEW.md: complete initial 74-source classification.
- GPT_DEVICE_LIFECYCLE_BOUNDARIES.md: state, identity, repair, capacity, commands and Field corrections; controls over conflicting initial proposals.
- GPT_DEVICE_LIFECYCLE_PREDICATES.md: Recycling correction, first-actual-destruction anti-loop rule, distinct ten-minute procedures and persistent disablement.
- CODEX_DEVICE_LIFECYCLE_IMPLEMENTATION_REVIEW.md: exact candidate and tests submitted for disposition.


## tools/device_lifecycle_playtest_rules.py

"""Bounded device/Totem lifecycle reference; exact source roles are registered.

The caller owns source access, range/space/LOS, legal targets, recharge/rest
calendar, rolls, concentration scheduling and geometry. Wallets and command
ledgers MUST be canonical for the owner, not a new copy for each ability.
Expiry markers are original source-authorized deadlines. These primitives do
not implement every effect on the 74 supplied cards or a complete game engine.
"""
from dataclasses import dataclass, field
from copy import deepcopy
from control_playtest_rules import ClockMarker, clock_marker, require_deadline
from spell_playtest_rules import SpellRuleError, integer
from redirection_playtest_rules import DeviceState, device_damage, identity

MACHINE_KINDS=frozenset({'drone','device','salvage','reaper'})
OBJECT_KINDS=MACHINE_KINDS|{'totem','echo'}
PRIMARY=frozenset({'deployed','retracted','destroyed','expired','ended','replaced'})


@dataclass
class Wallet:
    rp: int=0
    actions: int=1
    bonus_action: bool=True
    reaction: bool=True
    used: set=field(default_factory=set)

    def validate(self,rp=0,action=None,use_key=None):
        integer(rp,'RP cost',0)
        integer(self.rp,'available RP',0)
        if action not in (None,'action','bonus','reaction'):
            raise SpellRuleError('Unknown action payment')
        if self.rp<rp:raise SpellRuleError('Insufficient RP')
        if action=='action' and self.actions<1:raise SpellRuleError('No Action')
        if action=='bonus' and not self.bonus_action:raise SpellRuleError('No Bonus Action')
        if action=='reaction' and not self.reaction:raise SpellRuleError('No Reaction')
        if use_key is not None:
            identity(use_key)
            if use_key in self.used:raise SpellRuleError('Source use already spent in this scope')

    def pay(self,rp=0,action=None,use_key=None):
        self.validate(rp,action,use_key)
        self.rp-=rp
        if action=='action':self.actions-=1
        if action=='bonus':self.bonus_action=False
        if action=='reaction':self.reaction=False
        if use_key is not None:self.used.add(use_key)


@dataclass
class CommandLedger:
    """Owner-wide numbered-round ledger, including multiclass companions."""
    owner: str
    rounds: dict=field(default_factory=dict)

    def activate(self,round_number,mode,wallet,*,rp=0,tinker=False,regular=True):
        integer(round_number,'numbered round',1)
        if mode not in ('support','attack','gadget-sync','decoy'):
            raise SpellRuleError('Not a shared command mode')
        if tinker and mode in ('support','attack') and not regular:
            raise SpellRuleError('Tinker command/trigger requires supplied regular-turn eligibility')
        command=mode in ('support','attack')
        damaging=mode!='support'
        entry=self.rounds.get(round_number,{'command':False,'damage':False})
        if command and entry['command']:raise SpellRuleError('Round companion command spent')
        if damaging and entry['damage']:raise SpellRuleError('Round companion damage spent')
        # Gadget Sync costs exactly 1 RP; Decoy is a passive engine trigger.
        if mode=='gadget-sync' and rp!=1:raise SpellRuleError('Gadget Sync costs 1 RP')
        if mode=='decoy' and rp!=0:raise SpellRuleError('Decoy trigger has no RP cost')
        wallet.validate(rp,'bonus' if command else None)
        wallet.pay(rp,'bonus' if command else None)
        self.rounds[round_number]={
            'command':entry['command'] or command,
            'damage':entry['damage'] or damaging}
        return {'commandSpent':command,'damagingActivationSpent':damaging}


@dataclass
class Entity:
    instance_id: str
    owner: str
    source_id: str
    kind: str
    maximum_hp: int | None
    hp: int | None
    ac: int | None
    expiry: ClockMarker | None=None
    slot_kind: str | None=None
    slot_count: int=0
    asset_id: str | None=None
    state: str='deployed'
    disabled: bool=False
    disabled_reason: str | None=None
    temp_hp: int=0
    parent_id: str | None=None
    concentration: str | None=None
    paid_deployment_rp: int=0
    modules: tuple=()
    ammunition: dict=field(default_factory=dict)
    spent_uses: set=field(default_factory=set)
    effects: dict=field(default_factory=dict)
    destruction_history: list=field(default_factory=list)
    material_event: str | None=None
    damaging_profile: bool=False
    attack_bonus: int | None=None
    unavailable: bool=False
    superseded: bool=False

    def __post_init__(self):
        identity(self.instance_id);identity(self.owner);identity(self.source_id)
        if self.kind not in OBJECT_KINDS|{'field','elemental','chorus'}:
            raise SpellRuleError('Unknown lifecycle kind')
        if self.state not in PRIMARY:raise SpellRuleError('Unknown lifecycle state')
        integer(self.slot_count,'slot footprint',0,2)
        integer(self.paid_deployment_rp,'actually paid deployment RP',0)
        integer(self.temp_hp,'legal temp HP',0)
        if bool(self.slot_kind)!=bool(self.slot_count):
            raise SpellRuleError('A slot kind needs a positive footprint')
        if self.expiry is not None:require_deadline(self.expiry)
        if self.kind=='field':
            if any(v is not None for v in (self.hp,self.maximum_hp,self.ac)):
                raise SpellRuleError('Restoration Field has no HP-bearing anchor')
            if self.temp_hp:raise SpellRuleError('No temp HP on an objectless field')
        else:
            integer(self.maximum_hp,'maximum HP',1)
            integer(self.hp,'HP',0,self.maximum_hp)
            integer(self.ac,'AC',0)
            if (self.hp==0)!=(self.state=='destroyed'):
                raise SpellRuleError('Zero HP is the destroyed state')
        if self.kind=='drone' and (not self.asset_id or self.slot_count):
            raise SpellRuleError('Persistent Drone needs an asset and no deployable slot')
        if self.kind=='echo' and not self.parent_id:
            raise SpellRuleError('Echo needs its original parent')

    def active(self,now):
        return self.state=='deployed' and not self.unavailable and (
            self.expiry is None or clock_marker(now)<self.expiry)

    def functional(self,now):
        return self.active(now) and not self.disabled and (self.hp is None or self.hp>0)

    def machine_target(self,now,*,allow_disabled=False):
        return self.kind in MACHINE_KINDS and self.active(now) and self.hp>0 and (
            allow_disabled or not self.disabled)


@dataclass
class Destruction:
    event_id: str
    instance_id: str
    enemy_caused: bool
    enemy_hit: bool
    deliberate_sacrifice: bool
    copied: bool
    friendly_damage: bool
    secondary_explosion: bool
    flags: frozenset
    hostile_source: str | None
    first_for_instance: bool
    material_available: bool
    material_consumer: str | None=None
    volatile_settled: bool=False
    no_replacement: bool=False
    cinder_settled: bool=False

    def hostile_qualifies(self):
        return self.first_for_instance and self.enemy_caused and not (
            self.deliberate_sacrifice or self.copied or self.friendly_damage or
            self.secondary_explosion)


def profile_stats(kind,level,pb,*,intelligence=0,modifier=1,expertise=False,harmony=False):
    """Creation stats. Helpers' kind labels are aliases, not additional abilities."""
    integer(level,'class level',1,20);integer(pb,'proficiency bonus',1)
    integer(intelligence,'actual INT modifier',-10,20);integer(modifier,'M',1)
    if kind=='drone':return {'hp':max(1,5+intelligence+level),'ac':13+intelligence,'attack':pb+intelligence}
    if kind=='device':return {'hp':2*level+(modifier if expertise else 0),'ac':12+pb+int(expertise)}
    if kind in ('totem','echo'):return {'hp':2*level,'ac':12+pb}
    if kind=='elemental':return {'hp':(3 if harmony else 2)*level,'ac':12+pb}
    if kind=='chorus':return {'hp':(5 if harmony else 4)*level,'ac':12+pb}
    if kind in ('salvage','reaper'):return {'hp':level,'ac':12}
    if kind=='field':return {'hp':None,'ac':None}
    raise SpellRuleError('No supplied creation profile')


def deployable_capacity(level):
    integer(level,'Tinker level',1,20)
    return 3 if level>=17 else 2 if level>=13 else 1 if level>=6 else 0


def totem_capacity(level):
    integer(level,'Shaman level',1,20)
    return 2 if level>=13 else 1


def turret_bay_offer(free_slots):
    integer(free_slots,'free slots',0)
    if not free_slots:raise SpellRuleError('No slot for Advanced Turret Bay')
    count=min(2,free_slots)
    return count,2*count


class Lifecycle:
    def __init__(self,capacities):
        """capacities maps (owner, slot kind) to current legal capacity."""
        self.capacities=dict(capacities)
        for v in self.capacities.values():integer(v,'capacity',0)
        self.entities={}
        self.destructions={}
        self.volatile_rounds=set()

    def entity(self,ident):
        if ident not in self.entities:raise SpellRuleError('Unknown entity')
        return self.entities[ident]

    def closure(self,ident):
        result={ident}
        for child in self.entities.values():
            if child.parent_id==ident:result|=self.closure(child.instance_id)
        return result

    def occupied(self,owner,slot_kind,now,excluding=frozenset()):
        return sum(e.slot_count for e in self.entities.values()
                   if e.owner==owner and e.slot_kind==slot_kind and e.active(now)
                   and e.instance_id not in excluding)

    def free(self,owner,slot_kind,now,excluding=frozenset()):
        return self.capacities.get((owner,slot_kind),0)-self.occupied(owner,slot_kind,now,excluding)

    def end(self,ident,reason='ended'):
        if reason not in ('expired','ended','replaced'):raise SpellRuleError('Not an administrative ending')
        ended=[]
        for key in self.closure(ident):
            e=self.entity(key)
            if e.state in ('deployed','retracted'):
                e.state=reason;ended.append(key)
        return tuple(sorted(ended))

    def advance(self,now):
        now=clock_marker(now)
        for e in tuple(self.entities.values()):
            if e.expiry is not None and now>=e.expiry and e.state in ('deployed','retracted'):
                self.end(e.instance_id,'expired')
        # Destroyed debris retains destruction state and original expiry.

    def place(self,entities,now,wallet,*,rp,action='action',replace_id=None,use_key=None):
        """Atomic, caller-preflighted placement, including optional paid Echo.

        Passed entities have already validated source profiles, placement/range,
        original deadlines, source action/cost and owner Drone asset capacity.
        Only ordinary Totem placement may replace; Echo alone never evicts.
        """
        now=clock_marker(now);entities=tuple(entities)
        if not entities:raise SpellRuleError('No entities to place')
        if len({e.instance_id for e in entities})!=len(entities):raise SpellRuleError('Duplicate new identity')
        if any(e.instance_id in self.entities or not e.active(now) for e in entities):
            raise SpellRuleError('Placement needs fresh active instances')
        owners={e.owner for e in entities}
        if len(owners)!=1:raise SpellRuleError('One owner per placement')
        excluded=set()
        if replace_id is not None:
            old=self.entity(replace_id)
            if old.owner not in owners or old.kind not in ('totem','echo') or not old.active(now):
                raise SpellRuleError('Replacement requires own active Totem')
            if not any(e.kind=='totem' for e in entities):
                raise SpellRuleError('Echo alone cannot replace another Totem')
            excluded=self.closure(replace_id)
        known={**self.entities,**{e.instance_id:e for e in entities}}
        for e in entities:
            if e.kind=='echo':
                parent=known.get(e.parent_id)
                if not parent or parent.kind!='totem' or parent.owner!=e.owner or not parent.active(now):
                    raise SpellRuleError('Echo needs a live ordinary parent Totem')
                if parent.instance_id in excluded or e.expiry!=parent.expiry or e.concentration!=parent.concentration:
                    raise SpellRuleError('Echo shares parent expiry/concentration and cannot outlive replacement')
        additions={}
        for e in entities:
            if e.slot_count:
                key=e.owner,e.slot_kind
                additions[key]=additions.get(key,0)+e.slot_count
        for (owner,kind),count in additions.items():
            if count>self.free(owner,kind,now,excluded):raise SpellRuleError('Insufficient compatible capacity')
        wallet.validate(rp,action,use_key)
        wallet.pay(rp,action,use_key)
        if replace_id is not None:self.end(replace_id,'replaced')
        self.entities.update({e.instance_id:e for e in entities})
        return tuple(e.instance_id for e in entities)

    def end_concentration(self,owner,group):
        ended=set()
        for e in self.entities.values():
            if e.owner==owner and e.concentration==group:ended.update(self.end(e.instance_id))
        return tuple(sorted(ended))

    def retract(self,ident):
        e=self.entity(ident)
        if e.kind!='drone' or e.state!='deployed':raise SpellRuleError('Only a deployed Drone retracts')
        e.state='retracted'

    def redeploy(self,ident,now):
        e=self.entity(ident)
        if e.kind!='drone' or e.state!='retracted' or e.unavailable:
            raise SpellRuleError('Drone is not available for redeployment')
        if e.expiry is not None and clock_marker(now)>=e.expiry:raise SpellRuleError('Expired')
        e.state='deployed'

    def disable(self,ident,now,wallet,*,dissonance,amount,use_key):
        e=self.entity(ident);integer(dissonance,'current Dissonance',0);integer(amount,'routed amount',1,2)
        if not e.machine_target(now) or amount>dissonance:
            raise SpellRuleError('Need an active functional device and enough Dissonance')
        wallet.pay(0,'bonus',identity(use_key))
        self.set_disabled(e,True)
        return dissonance-amount

    def set_disabled(self,entity,value):
        # Persistent Drone asset state follows all recorded incarnations.
        for e in self.entities.values():
            if e is entity or (entity.asset_id is not None and e.owner==entity.owner and e.asset_id==entity.asset_id):
                e.disabled=value;e.disabled_reason='tinker.engine[7]' if value else None

    def tools_clear_disable(self,ident,wallet):
        """After a distinct completed 10-minute tools procedure; no reconstruction."""
        e=self.entity(ident)
        if e.kind not in MACHINE_KINDS or not e.disabled or e.superseded:
            raise SpellRuleError('A current protected-disabled machine is required')
        wallet.pay(1)
        self.set_disabled(e,False)

    def completed_short_rest(self,owner):
        for e in self.entities.values():
            if e.owner==owner:e.disabled=False;e.disabled_reason=None

    def field_repair(self,ident,now,wallet,rolled_amount):
        e=self.entity(ident);integer(rolled_amount,'S d8+M rolled repair',0)
        if not e.machine_target(now,allow_disabled=True) or (e.hp==e.maximum_hp and not e.disabled):
            raise SpellRuleError('Need damaged or protected-disabled living machine')
        wallet.pay(1,'action')
        gain=min(rolled_amount,e.maximum_hp-e.hp)
        e.hp+=gain;self.set_disabled(e,False)
        return gain

    def repair_pulse(self,idents,now,wallet,*,use_key,ac_deadline):
        require_deadline(ac_deadline)
        ids=tuple(idents)
        if not 1<=len(ids)<=3 or len(set(ids))!=len(ids):raise SpellRuleError('Choose 1 to 3 distinct devices')
        if ac_deadline<=clock_marker(now):raise SpellRuleError('AC bonus needs next-start deadline')
        entities=[self.entity(i) for i in ids]
        if any(not e.machine_target(now) for e in entities):raise SpellRuleError('Functional devices only')
        wallet.pay(3,'action',identity(use_key))
        result={}
        for e in entities:
            gain=min(e.maximum_hp//2,e.maximum_hp-e.hp);e.hp+=gain
            e.effects['repair-pulse-ac']={'amount':1,'deadline':ac_deadline}
            result[e.instance_id]=gain
        return result

    def damage(self,ident,now,amount,*,event_id,enemy_caused=False,enemy_hit=False,
               deliberate_sacrifice=False,copied=False,friendly_damage=False,
               secondary_explosion=False,flags=frozenset(),hostile_source=None):
        """Receives resolved damage after legal defenses; preserves branch flags."""
        e=self.entity(ident);identity(event_id)
        if event_id in self.destructions:raise SpellRuleError('Destruction event identity already used')
        if not e.active(now) or e.hp is None:raise SpellRuleError('Not an active HP-bearing target')
        if enemy_hit and not enemy_caused:raise SpellRuleError('Enemy-hit attribution requires enemy cause')
        after,result=device_damage(DeviceState(e.maximum_hp,e.hp,e.temp_hp,False,e.disabled),amount)
        e.hp=after.hp;e.temp_hp=after.temp_hp
        if not after.destroyed:return result,None
        e.state='destroyed'
        first=not e.destruction_history
        material=first and e.kind in MACHINE_KINDS
        d=Destruction(event_id,ident,enemy_caused,enemy_hit,deliberate_sacrifice,copied,
                      friendly_damage,secondary_explosion,frozenset(flags),hostile_source,
                      first,material,no_replacement=e.kind in ('salvage','reaper'))
        self.destructions[event_id]=d;e.destruction_history.append(event_id)
        if material:e.material_event=event_id
        for child in tuple(self.entities.values()):
            if child.parent_id==ident:self.end(child.instance_id)
        # Elementals disappear; the immutable cause record remains for Cinderflame.
        return {**result,'disappeared':e.kind in ('elemental','chorus')},d

    def material(self,ident):
        e=self.entity(ident)
        d=self.destructions.get(e.material_event)
        if e.state!='destroyed' or d is None or not d.material_available:
            raise SpellRuleError('No unused material from this destroyed instance')
        return e,d

    def consume_material(self,ident,consumer):
        e,d=self.material(ident)
        identity(consumer);d.material_available=False;d.material_consumer=consumer
        return e,d

    def reconstruct(self,ident,now,wallet,*,method,use_key):
        e,d=self.material(ident)
        if e.kind not in ('device','drone'):raise SpellRuleError('No reconstruction permission for this kind')
        if e.expiry is not None and clock_marker(now)>=e.expiry:raise SpellRuleError('Original deadline has passed')
        if e.unavailable:raise SpellRuleError('Drone asset is unavailable in current configuration')
        if method not in ('snap','drone-ten-minute'):raise SpellRuleError('Unknown reconstruction source')
        if method=='drone-ten-minute' and e.kind!='drone':raise SpellRuleError('Ten-minute rebuild is Drone-only')
        if e.slot_count>self.free(e.owner,e.slot_kind,now):raise SpellRuleError('Original slot footprint unavailable')
        wallet.validate(2 if method=='snap' else 1,'bonus' if method=='snap' else None,identity(use_key))
        wallet.pay(2 if method=='snap' else 1,'bonus' if method=='snap' else None,use_key)
        self.consume_material(ident,method)
        e.hp=max(1,e.maximum_hp//2);e.state='deployed'
        return e.hp

    def recycling(self,ident,wallet,*,use_key):
        e,d=self.material(ident)
        # Exact source excludes sacrifice/copy, but does not require enemy cause.
        if d.deliberate_sacrifice or d.copied or 'noResourceGeneration' in d.flags:
            raise SpellRuleError('Recycling source/branch excludes this debris')
        wallet.validate(0,None,identity(use_key))
        self.consume_material(ident,'recycling')
        wallet.pay(0,None,use_key)
        refund=min(1,e.paid_deployment_rp);wallet.rp+=refund
        return refund

    def salvage(self,ident,new_entity,now,wallet,*,reaper=False,use_key):
        e,d=self.material(ident)
        if not d.hostile_qualifies() or d.no_replacement or (reaper and not d.enemy_hit):
            raise SpellRuleError('Debris fails printed hostile destruction predicate')
        kind='reaper' if reaper else 'salvage'
        if new_entity.kind!=kind or new_entity.owner!=e.owner:
            raise SpellRuleError('Wrong resulting Scrapling')
        if new_entity.slot_count!=(0 if reaper else 1):
            raise SpellRuleError('Only Salvage Scrapling occupies a deployable slot')
        # place performs every capacity/payment validation before any mutation.
        self.place((new_entity,),now,wallet,rp=2 if reaper else 1,
                   action='reaction' if reaper else 'action',use_key=identity(use_key))
        self.consume_material(ident,'reaper' if reaper else 'salvage')
        return new_entity.instance_id

    def settle_volatile(self,event_id,round_number,*,chosen,enemy_in_range,scale):
        d=self.destructions[event_id];e=self.entity(d.instance_id)
        integer(round_number,'numbered round',1);integer(scale,'S',1,4)
        if d.volatile_settled:raise SpellRuleError('Object destruction opportunity already settled')
        eligible=(e.kind in MACHINE_KINDS and d.hostile_qualifies() and enemy_in_range
                  and not (d.flags&{'noRetaliation','noDamageTriggers','noDeathTriggers'})
                  and (e.owner,round_number) not in self.volatile_rounds)
        d.volatile_settled=True
        if not chosen or not eligible:return 0
        self.volatile_rounds.add((e.owner,round_number))
        return scale  # Caller attaches printed no-other-procs/resources flags.

    def cinder_destruction(self,event_id):
        d=self.destructions[event_id];e=self.entity(d.instance_id)
        if e.source_id!='shaman.hero.theurgist.summon-cinderflame' or not d.first_for_instance or d.cinder_settled:
            raise SpellRuleError('Not a fresh Cinderflame destruction')
        d.cinder_settled=True
        if d.flags&{'noRetaliation','noDamageTriggers','noDeathTriggers'}:return None
        return {'sourceId':e.source_id,'maximumEnemyTargets':3,
                'flags':frozenset({'noDeathTriggers','noResourceGeneration'})}

    def injection_cost(self,ident,now,modifier):
        e=self.entity(ident);integer(modifier,'M direct HP cost',1)
        if e.kind!='device' or not e.machine_target(now) or e.hp<=modifier:
            raise SpellRuleError('Volatile Injection must leave a legal device above zero')
        e.hp-=modifier  # Neither damage nor a temp-HP payment.
        return e.hp

    def reconfigure(self,ident,now,wallet,*,source_id,new_maximum,new_ac,known,
                    nonhealing,slot_count,damaging_profile):
        e=self.entity(ident);identity(source_id)
        integer(new_maximum,'new profile maximum HP',1);integer(new_ac,'new profile AC',0)
        if e.kind!='device' or not e.functional(now) or not known or not nonhealing:
            raise SpellRuleError('Functional device and known nonhealing destination required')
        if slot_count!=e.slot_count:raise SpellRuleError('Slot footprint cannot change')
        wallet.pay(1,'action')
        e.hp=min(new_maximum,max(1,e.hp*new_maximum//e.maximum_hp))
        e.maximum_hp=new_maximum;e.ac=new_ac;e.source_id=source_id
        e.damaging_profile=damaging_profile
        # Effects retain their original clocks. Caller reevaluates predicates;
        # an inapplicable Overcharge is not refunded or banked into a later use.
        return e.hp

    def recompute_drone(self,ident,*,level,pb,intelligence):
        e=self.entity(ident)
        if e.kind!='drone':raise SpellRuleError('Dynamic owner stats apply only to Drone')
        stats=profile_stats('drone',level,pb,intelligence=intelligence)
        e.maximum_hp=stats['hp'];e.hp=min(e.hp,e.maximum_hp)
        e.ac=stats['ac'];e.attack_bonus=stats['attack']
        return stats

    def long_rest_drone(self,ident,new_instance_id):
        """Source-authorized full rebuild; caller verifies completed long rest."""
        e=self.entity(ident);identity(new_instance_id)
        if e.kind!='drone' or e.state!='destroyed' or e.unavailable:
            raise SpellRuleError('Destroyed owned Drone required')
        if new_instance_id in self.entities:raise SpellRuleError('Fresh deployment identity required')
        new=deepcopy(e);new.instance_id=new_instance_id;new.state='deployed'
        new.hp=new.maximum_hp;new.temp_hp=0;new.destruction_history=[]
        new.material_event=None;new.paid_deployment_rp=0
        # Retained modules/asset and protected disable; no fabricated source-use
        # reset. Canonical long-rest reset rules are separate caller operations.
        new.effects={};e.unavailable=True;e.superseded=True
        if e.material_event:
            d=self.destructions[e.material_event]
            d.material_available=False
            if d.material_consumer is None:d.material_consumer='long-rest-rebuild'
        self.entities[new_instance_id]=new
        return new

    def configure_drones(self,owner,*,level,mode,modules_by_asset):
        """Completed-LR choice; no destruction/reward on excess asset withdrawal."""
        integer(level,'Tinker level',1,20)
        if mode not in ('single','dual'):raise SpellRuleError('Choose single or dual Drone')
        if mode=='dual' and level<13:raise SpellRuleError('Dual Drone requires level 13')
        expected=2 if mode=='dual' else 1
        if len(modules_by_asset)!=expected:raise SpellRuleError('Wrong number of configured assets')
        for asset,mods in modules_by_asset.items():
            identity(asset)
            if len(set(mods))!=len(mods) or len(mods)>(1 if mode=='dual' or level<13 else 2):
                raise SpellRuleError('Module configuration exceeds source limits')
        owned={e.asset_id for e in self.entities.values() if e.owner==owner and e.kind=='drone'}
        if not set(modules_by_asset)<=owned:raise SpellRuleError('Must configure owned assets')
        for e in self.entities.values():
            if e.owner==owner and e.kind=='drone' and not e.superseded:
                e.unavailable=e.asset_id not in modules_by_asset
                if e.unavailable and e.state=='deployed':e.state='retracted'
                if not e.unavailable:e.modules=tuple(modules_by_asset[e.asset_id])


def magnetic_wall_intercept(board,wall_id,root,now,wallet,*,scale,modifier,
                            ranged_weapon_hit,ally_within_five,wall_in_line):
    """Owner's Reaction; source/ally ownership and geometry established by caller."""
    e=board.entity(wall_id)
    if e.source_id!='tinker.hero.artificer.magnetic-wall' or not e.functional(now):
        raise SpellRuleError('Functional Magnetic Wall required')
    b=root.pending(root.original_id)
    if not b.attack_hit or not ranged_weapon_hit or not ally_within_five or not wall_in_line:
        raise SpellRuleError('Printed ranged weapon hit/ally/wall geometry not met')
    from redirection_playtest_rules import transfer_limit
    amount=transfer_limit(e.source_id,b.amount,scale=scale,modifier=modifier)
    wallet.validate(0,'reaction')
    operation=root.transfer(e.source_id,e.owner,{wall_id:amount},scale=scale,modifier=modifier)
    wallet.pay(0,'reaction')
    return operation['recipientBranchIds'][0]


def resolve_entity_branch(board,root,branch_id,now,*,enemy_caused=False,
                          enemy_hit=False,hostile_source=None,friendly_damage=False,
                          secondary_explosion=False,copied=False):
    """Bridge sealed/defended damage into HP and persistent destruction history.

    Transferred damage is not an attack hit. Its enemy-caused attribution may
    still permit Volatile/Recycling; enemy-hit-only predicates remain separate.
    """
    b=root.pending(branch_id);e=board.entity(b.target)
    if not e.active(now) or e.hp is None:raise SpellRuleError('No active HP-bearing recipient')
    if enemy_hit and (not enemy_caused or not b.attack_hit):
        raise SpellRuleError('Enemy-hit predicate needs an actual enemy attack hit on this object')
    event_id=branch_id+'/destruction'
    if event_id in board.destructions:raise SpellRuleError('Repeated destruction identity')
    _,event=root.resolve_device(branch_id,DeviceState(e.maximum_hp,e.hp,e.temp_hp,False,e.disabled))
    _,destruction=board.damage(b.target,now,b.amount,event_id=event_id,
        enemy_caused=enemy_caused,enemy_hit=enemy_hit,hostile_source=hostile_source,
        friendly_damage=friendly_damage,secondary_explosion=secondary_explosion,
        copied=copied,flags=b.flags)
    return event,destruction


## tools/validate_device_lifecycle_playtests.py

"""Adversarial tests for reviewed boundaries, not full-card execution."""
from pathlib import Path
from copy import deepcopy
import json
from device_lifecycle_playtest_rules import *
from redirection_playtest_rules import DamageRoot
ROOT=Path(__file__).resolve().parents[1]


def main():
    checks=[]
    def check(name,actual,expected):
        assert actual==expected,(name,actual,expected)
        checks.append({'name':name,'result':'PASS'})
    def rejects(name,fn):
        try:fn()
        except SpellRuleError:checks.append({'name':name,'result':'PASS'})
        else:raise AssertionError(name)
    def board(slots=2,totems=2):
        return Lifecycle({('owner','deployable'):slots,('owner','totem'):totems})
    def entity(ident='e',kind='device',maximum=20,**kw):
        slots={'device':('deployable',1),'salvage':('deployable',1),
               'totem':('totem',1),'echo':('totem',1),'field':('deployable',1)}
        sk,sc=slots.get(kind,(None,0))
        args=dict(instance_id=ident,owner='owner',source_id='tinker.engine[6]',
                  kind=kind,maximum_hp=maximum,hp=maximum,ac=14,
                  expiry=ClockMarker(18),slot_kind=sk,slot_count=sc,paid_deployment_rp=2)
        if kind=='drone':args.update(asset_id='asset-'+ident,expiry=None,source_id='tinker.engine[1]',paid_deployment_rp=0)
        if kind=='field':args.update(maximum_hp=None,hp=None,ac=None,source_id='tinker.hero.artificer.restoration-field')
        if kind in ('totem','echo'):args.update(concentration='all-totems',source_id='shaman.engine[0]')
        args.update(kw)
        return Entity(**args)
    def put(b,e):
        b.place((e,),ClockMarker(0),Wallet(100),rp=0,action=None)
        return e
    def kill(b,e,event='death',**kw):
        return b.damage(e.instance_id,ClockMarker(1),999,event_id=event,**kw)[1]

    b=board();e=put(b,entity(kind='drone'));w=Wallet(5)
    remaining=b.disable('e',0,w,dissonance=3,amount=2,use_key='route/sr1')
    check('Routing consumes BA and Dissonance but not RP',(remaining,w.rp,w.bonus_action),(1,5,False))
    b.retract('e');b.redeploy('e',0)
    check('Retraction/redeployment preserves protected disablement',(e.state,e.disabled),('deployed',True))
    d=kill(b,e,enemy_caused=True);b.reconstruct('e',2,Wallet(5),method='snap',use_key='snap/enc1')
    check('Snap returns positive HP but preserves disable',(e.hp,e.disabled,e.state),(10,True,'deployed'))
    check('Snap consumes first-event debris',(d.material_available,d.material_consumer),(False,'snap'))
    b.field_repair('e',2,Wallet(1),20)
    check('Field Repair clears disable and heals up to maximum',(e.disabled,e.hp),(False,20))
    b.set_disabled(e,True);w=Wallet(1)
    check('Full-HP disabled Field Repair is legal',b.field_repair('e',2,w,12),0)
    check('Full-HP clear still costs Action and RP',(w.actions,w.rp),(0,0))
    rejects('Full-HP enabled Field Repair invalid',lambda:b.field_repair('e',2,Wallet(1),10))

    b=board();e=put(b,entity(kind='drone',disabled=True))
    kill(b,e);b.completed_short_rest('owner')
    check('Short rest clears flag only',(e.hp,e.state,e.disabled),(0,'destroyed',False))
    rejects('Field Repair cannot revive destroyed Drone',lambda:b.field_repair('e',2,Wallet(2),20))
    b.set_disabled(e,True);b.tools_clear_disable('e',Wallet(1))
    check('Separate tools procedure clears flag without reconstruction',(e.disabled,e.hp),(False,0))
    b.set_disabled(e,True);b.reconstruct('e',2,Wallet(1),method='drone-ten-minute',use_key='drone/sr1')
    check('Drone ten-minute reconstruction does not merge disable-clear',(e.hp,e.disabled),(10,True))

    b=board(1);e=put(b,entity());kill(b,e,enemy_caused=True)
    check('Destruction releases active slot',b.free('owner','deployable',2),1)
    blocker=put(b,entity('block'));w=Wallet(4)
    rejects('Snap cannot evict occupied slot',lambda:b.reconstruct('e',2,w,method='snap',use_key='snap/enc1'))
    check('Failed Snap leaves wallet and debris intact',(w.rp,w.bonus_action,b.material('e')[1].material_available),(4,True,True))
    b.end('block');b.reconstruct('e',2,w,method='snap',use_key='snap/enc1')
    check('Snap reacquires same slot footprint',b.free('owner','deployable',2),0)
    e.ammunition={'rocket':1};e.spent_uses={'used'};e.modules=('offense',)
    d2=kill(b,e,'death2',enemy_caused=True)
    check('Second physical death creates no second material',(d2.first_for_instance,d2.material_available),(False,False))
    check('Second physical death cannot cause Volatile',b.settle_volatile('death2',2,chosen=True,enemy_in_range=True,scale=2),0)
    rejects('Second death has no Snap material',lambda:b.reconstruct('e',3,Wallet(4),method='snap',use_key='snap/enc2'))

    b=board();e=put(b,entity());kill(b,e,friendly_damage=True)
    w=Wallet(0);check('Friendly/accidental destruction can recycle',b.recycling('e',w,use_key='recycle/sr1'),1)
    check('Recycling refunds no more than deployment RP',w.rp,1)
    rejects('Consumed Recycling debris cannot Snap',lambda:b.reconstruct('e',2,Wallet(4),method='snap',use_key='snap/enc1'))
    rejects('Consumed debris cannot recycle twice',lambda:b.recycling('e',Wallet(),use_key='recycle/sr2'))
    b=board();e=put(b,entity(paid_deployment_rp=0));kill(b,e)
    check('Free deployment gets zero refund',b.recycling('e',Wallet(),use_key='recycle/sr1'),0)
    b=board();e=put(b,entity());kill(b,e,flags={'noResourceGeneration'})
    rejects('Inherited noResourceGeneration blocks Recycling',lambda:b.recycling('e',Wallet(),use_key='recycle/sr1'))
    check('Rejected refund does not consume debris',b.material('e')[1].material_available,True)

    b=board();e=put(b,entity());kill(b,e,enemy_caused=True,enemy_hit=True);b.advance(30)
    rejects('Snap illegal exactly at expiry',lambda:b.reconstruct('e',18,Wallet(3),method='snap',use_key='snap/enc1'))
    check('Earlier destroyed debris remains after expiry',b.material('e')[1].material_available,True)
    check('Recycling can use expired-deployment debris',b.recycling('e',Wallet(),use_key='recycle/sr1'),1)
    b=board();e=put(b,entity());b.advance(18)
    check('Ordinary expiry no destruction/debris',(e.state,len(b.destructions),e.material_event),('expired',0,None))

    b=board();e=put(b,entity(kind='drone',disabled=True))
    e.modules=('support',);e.spent_uses={'existing'};kill(b,e)
    b.recycling('e',Wallet(),use_key='recycle/sr1')
    new=b.long_rest_drone('e','new')
    check('LR after consumed Drone debris is fresh instance',(new.asset_id,new.instance_id,new.hp,new.destruction_history),(e.asset_id,'new',20,[]))
    check('LR rebuild preserves asset disable and module',(new.disabled,new.modules,new.spent_uses),(True,('support',),{'existing'}))
    check('Old incarnation superseded without reuse',(e.superseded,e.unavailable),(True,True))
    b.field_repair('new',2,Wallet(1),3)
    check('Asset flag clear follows historical and current instances',(e.disabled,new.disabled),(False,False))
    d=kill(b,new,'newdeath',enemy_caused=True)
    check('Fresh LR incarnation receives own first death',d.first_for_instance,True)

    b=board();e=put(b,entity(maximum=1));kill(b,e)
    check('Max1 Snap reconstruction has viability minimum',b.reconstruct('e',2,Wallet(2),method='snap',use_key='snap/enc1'),1)
    result=b.repair_pulse(('e',),2,Wallet(3),use_key='repair/sr1',ac_deadline=ClockMarker(6))
    check('Functional max1 Repair Pulse rounds half to zero',result,{'e':0})
    b.set_disabled(e,True)
    rejects('Repair Pulse has no protected-disable clearance',lambda:b.repair_pulse(('e',),2,Wallet(3),use_key='repair/sr2',ac_deadline=ClockMarker(6)))

    b=board();e=put(b,entity());e.hp=1;e.temp_hp=4;e.ammunition={'rocket':1};e.spent_uses={'trap'}
    e.effects['overcharge']={'deadline':ClockMarker(6),'requires':'damaging-activation'}
    b.reconfigure('e',2,Wallet(1),source_id='tinker.arch.deploy-net-trap',new_maximum=2,new_ac=15,known=True,nonhealing=True,slot_count=1,damaging_profile=False)
    check('Reconfiguration fractional minimum does not destroy',(e.hp,e.maximum_hp,len(e.destruction_history)),(1,2,0))
    check('Reconfiguration preserves clocks/temp/ammo/uses',(e.expiry,e.temp_hp,e.ammunition,e.spent_uses,e.effects['overcharge']['deadline']),(ClockMarker(18),4,{'rocket':1},{'trap'},ClockMarker(6)))
    rejects('Reconfiguration cannot gain slot footprint',lambda:b.reconfigure('e',2,Wallet(1),source_id='profile',new_maximum=10,new_ac=14,known=True,nonhealing=True,slot_count=2,damaging_profile=True))
    rejects('Reconfiguration cannot become healing profile',lambda:b.reconfigure('e',2,Wallet(1),source_id='profile',new_maximum=10,new_ac=14,known=True,nonhealing=False,slot_count=1,damaging_profile=False))
    b.set_disabled(e,True)
    rejects('Disabled device cannot reconfigure to escape flag',lambda:b.reconfigure('e',2,Wallet(1),source_id='profile',new_maximum=10,new_ac=14,known=True,nonhealing=True,slot_count=1,damaging_profile=False))

    b=board();e=put(b,entity(kind='drone',maximum=10));e.hp=7
    b.recompute_drone('e',level=3,pb=2,intelligence=4)
    check('Temporary actual INT updates Drone capacity/AC/attack without heal',(e.maximum_hp,e.hp,e.ac,e.attack_bonus),(12,7,17,6))
    b.recompute_drone('e',level=3,pb=2,intelligence=-3)
    check('INT decrease clamps HP without destruction',(e.maximum_hp,e.hp,e.ac,e.attack_bonus,len(e.destruction_history)),(5,5,10,-1,0))
    check('Ordinary deployable Expertise snapshot',profile_stats('device',10,4,modifier=3,expertise=True),{'hp':23,'ac':17})
    check('Harmony named elemental 3L',profile_stats('elemental',10,4,harmony=True)['hp'],30)
    check('Harmony Chorus one package 5L',profile_stats('chorus',10,4,harmony=True)['hp'],50)
    check('Echo keeps ordinary Totem object stats',profile_stats('echo',10,4),{'hp':20,'ac':16})
    check('Deployable capacity gates',[deployable_capacity(v) for v in (5,6,12,13,16,17)], [0,1,1,2,2,3])
    check('Turret Bay slot/cost fallback',(turret_bay_offer(1),turret_bay_offer(3)),((1,2),(2,4)))
    rejects('Turret Bay no free slot is illegal',lambda:turret_bay_offer(0))

    b=board();p=entity('parent','totem');echo=entity('echo','echo',parent_id='parent')
    b.place((p,echo),0,Wallet(6),rp=6)
    w=Wallet(1);np=entity('np','totem');ne=entity('ne','echo',parent_id='np')
    rejects('Unaffordable replacement leaves parent+Echo',lambda:b.place((np,ne),1,w,rp=6,replace_id='parent'))
    check('Failed placement atomically preserves old board/wallet',(p.state,echo.state,w.rp),('deployed','deployed',1))
    b.place((np,ne),1,Wallet(6),rp=6,replace_id='parent')
    check('Parent replacement frees both for paid parent+Echo',(p.state,echo.state,np.state,ne.state,len(b.destructions)),('replaced','replaced','deployed','deployed',0))
    ep=entity('ep','totem')
    b.place((ep,),1,Wallet(2),rp=2,replace_id='ne')
    check('Replacing Echo alone leaves parent',(np.state,ne.state),('deployed','replaced'))
    rejects('Echo cannot itself replace another Totem',lambda:b.place((entity('bad','echo',parent_id='np'),),1,Wallet(2),rp=2,replace_id='ep'))
    b.end_concentration('owner','all-totems')
    check('Concentration ends all active Totems, no debris',(b.occupied('owner','totem',2),len(b.destructions)),(0,0))
    b=board();p=entity('p','totem');ch=entity('ch','echo',parent_id='p')
    b.place((p,ch),0,Wallet(6),rp=6);kill(b,p)
    check('Parent destruction ends Echo administratively',(p.state,ch.state,len(b.destructions)),('destroyed','ended',1))
    b=board(totems=1);old=put(b,entity('old','totem'))
    b.place((entity('new','totem'),),0,Wallet(2),rp=2,replace_id='old')
    check('Capacity1 replaces prior ordinary Totem',old.state,'replaced')

    ledger=CommandLedger('owner');w=Wallet(4)
    ledger.activate(1,'support',w)
    ledger.activate(1,'gadget-sync',w,rp=1)
    check('Support then Sync uses BA and one damage',(w.rp,w.bonus_action,ledger.rounds[1]),(3,False,{'command':True,'damage':True}))
    rejects('Extra turn does not reset owner round command',lambda:ledger.activate(1,'attack',Wallet(4)))
    ledger=CommandLedger('owner');w=Wallet(4)
    ledger.activate(1,'gadget-sync',w,rp=1);ledger.activate(1,'support',w)
    check('Sync first leaves later legal support BA',ledger.rounds[1],{'command':True,'damage':True})
    ledger=CommandLedger('owner');w=Wallet(4)
    ledger.activate(1,'decoy',w,tinker=True,regular=False)
    check('Off-turn Decoy uses damage allowance, no BA',ledger.rounds[1],{'command':False,'damage':True})
    rejects('Decoy first blocks turret damage later',lambda:ledger.activate(1,'attack',w,tinker=True))
    ledger.activate(1,'support',w,tinker=True)
    rejects('Tinker BA cannot use extra-turn permission',lambda:CommandLedger('owner').activate(2,'attack',Wallet(),tinker=True,regular=False))
    ledger=CommandLedger('owner');w=Wallet(0)
    rejects('Unfunded Sync does not claim allowance',lambda:ledger.activate(1,'gadget-sync',w,rp=1))
    check('Failed command leaves ledger untouched',ledger.rounds,{})

    b=board(1);e=put(b,entity());d=kill(b,e,enemy_caused=True,enemy_hit=True);put(b,entity('occupant'))
    reaper=entity('reaper','reaper',expiry=ClockMarker(6,20))
    b.salvage('e',reaper,2,Wallet(2),reaper=True,use_key='reaper/sr1')
    check('Reaper succeeds with no deployable capacity',(reaper.slot_count,b.free('owner','deployable',2)),(0,0))
    check('Reaper consumes source material',d.material_consumer,'reaper')
    b=board(1);e=put(b,entity());d=kill(b,e,enemy_caused=True);put(b,entity('occupant'));w=Wallet(1)
    rejects('Salvage requires free slot before payment/debris',lambda:b.salvage('e',entity('scrap','salvage'),2,w,use_key='salvage/enc1'))
    check('Failed Salvage preserves material and RP',(d.material_available,w.rp),(True,1))
    b.end('occupant');b.salvage('e',entity('scrap','salvage'),2,w,use_key='salvage/enc1')
    s=b.entity('scrap');kill(b,s,'scrapdeath',enemy_caused=True,enemy_hit=True)
    rejects('Scrapling cannot spawn own replacement',lambda:b.salvage('scrap',entity('chain','reaper'),3,Wallet(2),reaper=True,use_key='reaper/sr2'))

    b=board();e=put(b,entity());kill(b,e,enemy_caused=True,flags={'noRetaliation'})
    check('Emergency provenance blocks Volatile despite enemy cause',b.settle_volatile('death',1,chosen=True,enemy_in_range=True,scale=2),0)
    check('NoRetaliation alone does not block debris',b.material('e')[1].material_available,True)
    b=board();e=put(b,entity());kill(b,e,enemy_caused=True)
    check('Declining own opportunity gives no damage',b.settle_volatile('death',1,chosen=False,enemy_in_range=True,scale=2),0)
    check('Decline does not spend owner round allowance',b.volatile_rounds,set())
    other=put(b,entity('other'));kill(b,other,'otherdeath',enemy_caused=True)
    check('Other device may use owner Volatile after decline',b.settle_volatile('otherdeath',1,chosen=True,enemy_in_range=True,scale=2),2)
    rejects('Settled opportunity cannot replay',lambda:b.settle_volatile('otherdeath',2,chosen=True,enemy_in_range=True,scale=2))
    b=board();e=put(b,entity());e.hp=3;e.temp_hp=10
    check('Injection spends direct normal HP',b.injection_cost('e',1,2),1)
    check('Injection leaves tempHP and death history unchanged',(e.temp_hp,len(e.destruction_history)),(10,0))
    rejects('Injection must leave positive HP',lambda:b.injection_cost('e',1,1))

    b=board();f=put(b,entity('f','field'))
    rejects('Objectless Field cannot take machine damage',lambda:b.damage('f',1,2,event_id='x'))
    rejects('Objectless Field cannot receive Field Repair',lambda:b.field_repair('f',1,Wallet(1),2))
    rejects('Objectless Field cannot route Dissonance',lambda:b.disable('f',1,Wallet(),dissonance=2,amount=1,use_key='route/sr1'))
    check('Objectless Field still occupies a slot',b.occupied('owner','deployable',1),1)
    b.end('f');check('Field ending releases slot with no debris',(b.occupied('owner','deployable',1),len(b.destructions)),(0,0))
    b=board();c=put(b,entity('c','elemental',source_id='shaman.hero.theurgist.summon-cinderflame'))
    result,d=b.damage('c',1,999,event_id='cdeath')
    check('Cinder disappears but records destruction',result['disappeared'],True)
    check('Cinder death burst independent of command ledger',b.cinder_destruction('cdeath')['maximumEnemyTargets'],3)
    rejects('Cinder burst resolves once',lambda:b.cinder_destruction('cdeath'))
    b=board();c=put(b,entity('c','elemental',source_id='shaman.hero.theurgist.summon-cinderflame'));b.end('c')
    check('Cinder dismissal no death burst event',len(b.destructions),0)

    b=board();wall=put(b,entity('wall',maximum=3,source_id='tinker.hero.artificer.magnetic-wall',temp_hp=1))
    r=DamageRoot('shot','ally',12,'piercing',attack_hit=True,critical=True);r.defend(r.original_id,flat_reductions=(2,))
    w=Wallet()
    bid=magnetic_wall_intercept(b,'wall',r,1,w,scale=2,modifier=2,ranged_weapon_hit=True,ally_within_five=True,wall_in_line=True)
    check('Magnetic Wall fixed post-defense transfer',(r.branch(r.original_id).amount,r.branch(bid).amount,w.reaction),(6,4,False))
    check('Wall branch exact flags/no attack riders',(r.branch(bid).flags,r.branch(bid).attack_hit,r.branch(bid).critical),(frozenset({'noSecondMitigation','noRetransfer'}),False,False))
    rejects('Wall branch cannot get second mitigation',lambda:r.prevent(bid,1,'extra'))
    event,d=resolve_entity_branch(b,r,bid,1,enemy_caused=True,hostile_source='enemy')
    check('Wall temp then HP destruction, hostile not sacrifice',(wall.hp,wall.temp_hp,d.enemy_caused,d.deliberate_sacrifice),(0,0,True,False))
    check('Transferred damage not an enemy attack hit on wall',d.enemy_hit,False)
    check('Magnetic destruction can trigger Volatile',b.settle_volatile(d.event_id,1,chosen=True,enemy_in_range=True,scale=2),2)
    check('Magnetic destruction keeps useful debris',d.material_available,True)
    b=board();wall=put(b,entity('wall',source_id='tinker.hero.artificer.magnetic-wall'))
    r=DamageRoot('wrong','ally',10,'fire');r.defend(r.original_id);w=Wallet()
    rejects('Magnetic Wall rejects non-hit without spending Reaction',lambda:magnetic_wall_intercept(b,'wall',r,1,w,scale=1,modifier=2,ranged_weapon_hit=False,ally_within_five=True,wall_in_line=True))
    check('Invalid wall reaction preserves root and Reaction',(r.operation,w.reaction),(None,True))

    b=board();d1=put(b,entity('d1','drone'));d2=put(b,entity('d2','drone'))
    b.configure_drones('owner',level=13,mode='single',modules_by_asset={d1.asset_id:('a','b')})
    check('Single two-module configuration withdraws second without death',(d2.state,d2.unavailable,len(b.destructions)),('retracted',True,0))
    b.configure_drones('owner',level=13,mode='dual',modules_by_asset={d1.asset_id:('a',),d2.asset_id:('b',)})
    b.redeploy('d2',1)
    check('Returning owned second Drone keeps identity',(d2.instance_id,d2.state,d2.unavailable),('d2','deployed',False))
    rejects('Dual cannot have two modules per Drone',lambda:b.configure_drones('owner',level=13,mode='dual',modules_by_asset={d1.asset_id:('a','b'),d2.asset_id:('a',)}))
    rejects('Single two modules must be distinct',lambda:b.configure_drones('owner',level=13,mode='single',modules_by_asset={d1.asset_id:('a','a')}))

    states=0
    for old_max in range(1,25):
        for old_hp in range(1,old_max+1):
            for new_max in (1,2,7,24):
                b=board();e=put(b,entity(maximum=old_max));e.hp=old_hp
                b.reconfigure('e',1,Wallet(1),source_id='tinker.engine[6]',new_maximum=new_max,new_ac=14,known=True,nonhealing=True,slot_count=1,damaging_profile=True)
                assert 1<=e.hp<=new_max and e.state=='deployed' and not e.destruction_history
                assert e.hp==max(1,old_hp*new_max//old_max)
                states+=1
    result={'result':'PASS','status':'IMPLEMENTED; GPT exact review pending',
            'scope':'74 class-source lifecycle roles plus3 frozen shared paragraphs; no full-card/game completeness claim',
            'checkCount':len(checks),'reconfigurationStates':states,'checks':checks}
    (ROOT/'docs/mechanics/DEVICE_LIFECYCLE_PLAYTEST_VALIDATION.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(f'PASS {len(checks)} device lifecycle checks and {states} reconfiguration states.')


if __name__=='__main__':main()


## docs/mechanics/DEVICE_LIFECYCLE_PLAYTEST_VALIDATION.json

{
  "result": "PASS",
  "status": "IMPLEMENTED; GPT exact review pending",
  "scope": "74 class-source lifecycle roles plus3 frozen shared paragraphs; no full-card/game completeness claim",
  "checkCount": 104,
  "reconfigurationStates": 1200,
  "checks": [
    {
      "name": "Routing consumes BA and Dissonance but not RP",
      "result": "PASS"
    },
    {
      "name": "Retraction/redeployment preserves protected disablement",
      "result": "PASS"
    },
    {
      "name": "Snap returns positive HP but preserves disable",
      "result": "PASS"
    },
    {
      "name": "Snap consumes first-event debris",
      "result": "PASS"
    },
    {
      "name": "Field Repair clears disable and heals up to maximum",
      "result": "PASS"
    },
    {
      "name": "Full-HP disabled Field Repair is legal",
      "result": "PASS"
    },
    {
      "name": "Full-HP clear still costs Action and RP",
      "result": "PASS"
    },
    {
      "name": "Full-HP enabled Field Repair invalid",
      "result": "PASS"
    },
    {
      "name": "Short rest clears flag only",
      "result": "PASS"
    },
    {
      "name": "Field Repair cannot revive destroyed Drone",
      "result": "PASS"
    },
    {
      "name": "Separate tools procedure clears flag without reconstruction",
      "result": "PASS"
    },
    {
      "name": "Drone ten-minute reconstruction does not merge disable-clear",
      "result": "PASS"
    },
    {
      "name": "Destruction releases active slot",
      "result": "PASS"
    },
    {
      "name": "Snap cannot evict occupied slot",
      "result": "PASS"
    },
    {
      "name": "Failed Snap leaves wallet and debris intact",
      "result": "PASS"
    },
    {
      "name": "Snap reacquires same slot footprint",
      "result": "PASS"
    },
    {
      "name": "Second physical death creates no second material",
      "result": "PASS"
    },
    {
      "name": "Second physical death cannot cause Volatile",
      "result": "PASS"
    },
    {
      "name": "Second death has no Snap material",
      "result": "PASS"
    },
    {
      "name": "Friendly/accidental destruction can recycle",
      "result": "PASS"
    },
    {
      "name": "Recycling refunds no more than deployment RP",
      "result": "PASS"
    },
    {
      "name": "Consumed Recycling debris cannot Snap",
      "result": "PASS"
    },
    {
      "name": "Consumed debris cannot recycle twice",
      "result": "PASS"
    },
    {
      "name": "Free deployment gets zero refund",
      "result": "PASS"
    },
    {
      "name": "Inherited noResourceGeneration blocks Recycling",
      "result": "PASS"
    },
    {
      "name": "Rejected refund does not consume debris",
      "result": "PASS"
    },
    {
      "name": "Snap illegal exactly at expiry",
      "result": "PASS"
    },
    {
      "name": "Earlier destroyed debris remains after expiry",
      "result": "PASS"
    },
    {
      "name": "Recycling can use expired-deployment debris",
      "result": "PASS"
    },
    {
      "name": "Ordinary expiry no destruction/debris",
      "result": "PASS"
    },
    {
      "name": "LR after consumed Drone debris is fresh instance",
      "result": "PASS"
    },
    {
      "name": "LR rebuild preserves asset disable and module",
      "result": "PASS"
    },
    {
      "name": "Old incarnation superseded without reuse",
      "result": "PASS"
    },
    {
      "name": "Asset flag clear follows historical and current instances",
      "result": "PASS"
    },
    {
      "name": "Fresh LR incarnation receives own first death",
      "result": "PASS"
    },
    {
      "name": "Max1 Snap reconstruction has viability minimum",
      "result": "PASS"
    },
    {
      "name": "Functional max1 Repair Pulse rounds half to zero",
      "result": "PASS"
    },
    {
      "name": "Repair Pulse has no protected-disable clearance",
      "result": "PASS"
    },
    {
      "name": "Reconfiguration fractional minimum does not destroy",
      "result": "PASS"
    },
    {
      "name": "Reconfiguration preserves clocks/temp/ammo/uses",
      "result": "PASS"
    },
    {
      "name": "Reconfiguration cannot gain slot footprint",
      "result": "PASS"
    },
    {
      "name": "Reconfiguration cannot become healing profile",
      "result": "PASS"
    },
    {
      "name": "Disabled device cannot reconfigure to escape flag",
      "result": "PASS"
    },
    {
      "name": "Temporary actual INT updates Drone capacity/AC/attack without heal",
      "result": "PASS"
    },
    {
      "name": "INT decrease clamps HP without destruction",
      "result": "PASS"
    },
    {
      "name": "Ordinary deployable Expertise snapshot",
      "result": "PASS"
    },
    {
      "name": "Harmony named elemental 3L",
      "result": "PASS"
    },
    {
      "name": "Harmony Chorus one package 5L",
      "result": "PASS"
    },
    {
      "name": "Echo keeps ordinary Totem object stats",
      "result": "PASS"
    },
    {
      "name": "Deployable capacity gates",
      "result": "PASS"
    },
    {
      "name": "Turret Bay slot/cost fallback",
      "result": "PASS"
    },
    {
      "name": "Turret Bay no free slot is illegal",
      "result": "PASS"
    },
    {
      "name": "Unaffordable replacement leaves parent+Echo",
      "result": "PASS"
    },
    {
      "name": "Failed placement atomically preserves old board/wallet",
      "result": "PASS"
    },
    {
      "name": "Parent replacement frees both for paid parent+Echo",
      "result": "PASS"
    },
    {
      "name": "Replacing Echo alone leaves parent",
      "result": "PASS"
    },
    {
      "name": "Echo cannot itself replace another Totem",
      "result": "PASS"
    },
    {
      "name": "Concentration ends all active Totems, no debris",
      "result": "PASS"
    },
    {
      "name": "Parent destruction ends Echo administratively",
      "result": "PASS"
    },
    {
      "name": "Capacity1 replaces prior ordinary Totem",
      "result": "PASS"
    },
    {
      "name": "Support then Sync uses BA and one damage",
      "result": "PASS"
    },
    {
      "name": "Extra turn does not reset owner round command",
      "result": "PASS"
    },
    {
      "name": "Sync first leaves later legal support BA",
      "result": "PASS"
    },
    {
      "name": "Off-turn Decoy uses damage allowance, no BA",
      "result": "PASS"
    },
    {
      "name": "Decoy first blocks turret damage later",
      "result": "PASS"
    },
    {
      "name": "Tinker BA cannot use extra-turn permission",
      "result": "PASS"
    },
    {
      "name": "Unfunded Sync does not claim allowance",
      "result": "PASS"
    },
    {
      "name": "Failed command leaves ledger untouched",
      "result": "PASS"
    },
    {
      "name": "Reaper succeeds with no deployable capacity",
      "result": "PASS"
    },
    {
      "name": "Reaper consumes source material",
      "result": "PASS"
    },
    {
      "name": "Salvage requires free slot before payment/debris",
      "result": "PASS"
    },
    {
      "name": "Failed Salvage preserves material and RP",
      "result": "PASS"
    },
    {
      "name": "Scrapling cannot spawn own replacement",
      "result": "PASS"
    },
    {
      "name": "Emergency provenance blocks Volatile despite enemy cause",
      "result": "PASS"
    },
    {
      "name": "NoRetaliation alone does not block debris",
      "result": "PASS"
    },
    {
      "name": "Declining own opportunity gives no damage",
      "result": "PASS"
    },
    {
      "name": "Decline does not spend owner round allowance",
      "result": "PASS"
    },
    {
      "name": "Other device may use owner Volatile after decline",
      "result": "PASS"
    },
    {
      "name": "Settled opportunity cannot replay",
      "result": "PASS"
    },
    {
      "name": "Injection spends direct normal HP",
      "result": "PASS"
    },
    {
      "name": "Injection leaves tempHP and death history unchanged",
      "result": "PASS"
    },
    {
      "name": "Injection must leave positive HP",
      "result": "PASS"
    },
    {
      "name": "Objectless Field cannot take machine damage",
      "result": "PASS"
    },
    {
      "name": "Objectless Field cannot receive Field Repair",
      "result": "PASS"
    },
    {
      "name": "Objectless Field cannot route Dissonance",
      "result": "PASS"
    },
    {
      "name": "Objectless Field still occupies a slot",
      "result": "PASS"
    },
    {
      "name": "Field ending releases slot with no debris",
      "result": "PASS"
    },
    {
      "name": "Cinder disappears but records destruction",
      "result": "PASS"
    },
    {
      "name": "Cinder death burst independent of command ledger",
      "result": "PASS"
    },
    {
      "name": "Cinder burst resolves once",
      "result": "PASS"
    },
    {
      "name": "Cinder dismissal no death burst event",
      "result": "PASS"
    },
    {
      "name": "Magnetic Wall fixed post-defense transfer",
      "result": "PASS"
    },
    {
      "name": "Wall branch exact flags/no attack riders",
      "result": "PASS"
    },
    {
      "name": "Wall branch cannot get second mitigation",
      "result": "PASS"
    },
    {
      "name": "Wall temp then HP destruction, hostile not sacrifice",
      "result": "PASS"
    },
    {
      "name": "Transferred damage not an enemy attack hit on wall",
      "result": "PASS"
    },
    {
      "name": "Magnetic destruction can trigger Volatile",
      "result": "PASS"
    },
    {
      "name": "Magnetic destruction keeps useful debris",
      "result": "PASS"
    },
    {
      "name": "Magnetic Wall rejects non-hit without spending Reaction",
      "result": "PASS"
    },
    {
      "name": "Invalid wall reaction preserves root and Reaction",
      "result": "PASS"
    },
    {
      "name": "Single two-module configuration withdraws second without death",
      "result": "PASS"
    },
    {
      "name": "Returning owned second Drone keeps identity",
      "result": "PASS"
    },
    {
      "name": "Dual cannot have two modules per Drone",
      "result": "PASS"
    },
    {
      "name": "Single two modules must be distinct",
      "result": "PASS"
    }
  ]
}


## docs/mechanics/DEVICE_LIFECYCLE_SOURCE_VALIDATION.json

{
  "status": "PASS",
  "exactClassPassages": 74,
  "exactSharedParagraphs": 3,
  "scope": "Source equality and provenance of prepared conference; no semantics reviewed yet.",
  "issues": []
}


## Full current source roles

{
  "status": "IMPLEMENTED CANDIDATE; exact lifecycle/command review pending",
  "scope": "74 supplied Tinker/Shaman source roles plus3 shared paragraphs. Includes73 lexical candidates and MagneticWall semantic supplement; no full class or companion-system completion claim.",
  "bindings": [
    {
      "bindingId": "shaman.engine[0]",
      "sourceKind": "class-engine",
      "sourcePath": "data/public/class_playtests/shaman.json",
      "sourceId": 0,
      "sourceSha256": "7e562f123d46ba4396acf88e741004b1b09e622a105670522c0db07aa6d94996",
      "candidateOrigin": "Lexical candidate inventory",
      "sourceProcedure": {
        "text": "Wisdom is the class ability. Choose Elemental Affinity automatically at 1: Fire, Ice, Air or Earth. Spellcasting/RP remain separate from Totem objects and flasks. Totem capacity 1, rises 2 at 13; any third replaces one of your existing totems. A totem is a visible Tiny magical object: AC 12+PB, HP 2 L, immobile, immune to poison/psychic/conditions, vulnerable to ordinary weapon and other damage. At 0 HP its aura ends. A new totem appears within 30 ft; cannot occupy a creature's space, serve as a bridge, trap a creature without a save or move through walls."
      },
      "status": "SOURCE-AUDITED / DRAFTABLE; exact implementation review pending",
      "classification": "TOTEM_LIFECYCLE/CAPACITY",
      "operationalOverrides": [
        "Current lifecycle/command role is defined in DEVICE_LIFECYCLE_PLAYTEST.md. Boundary and predicate replies supersede conflicting initial proposals. Full card effects are not certified.",
        "Shared owner command/damage ledgers, source-qualified life states, original expiry, slot footprint, protected-disable and destruction provenance apply only where the source role calls for them."
      ],
      "reviewEvidence": [
        "GPT_DEVICE_LIFECYCLE_FIRST_REVIEW.md",
        "GPT_DEVICE_LIFECYCLE_BOUNDARIES.md",
        "GPT_DEVICE_LIFECYCLE_PREDICATES.md"
      ],
      "openIssues": [
        "Exact implementation review pending; other effects and wider companion completeness remain outside this bounded role."
      ]
    },
    {
      "bindingId": "shaman.engine[1]",
      "sourceKind": "class-engine",
      "sourcePath": "data/public/class_playtests/shaman.json",
      "sourceId": 1,
      "sourceSha256": "2a2a89b4f440277a59743d2dc2936f2a625be9557882f5796fa8fb71d4b76d80",
      "candidateOrigin": "Lexical candidate inventory",
      "sourceProcedure": {
        "text": "Totem Casting is Action 2 RP, duration 3 of your turns, 15 ft aura. Choose Flame, Stone, Frost, Spirit or Renewal. Benefits require an ally/target in the aura, maximum 3 creatures benefiting per pulse/round chosen by you. Flame adds 1 fire to an ally's first direct weapon hit per round; on critical that target Burns 1d4 next turn. Stone reduces damage by 1 and gives enemies-1 to STR checks to shove. Frost: enemy first entering/starting each round makes CON save or Speed-10 ft until end its turn. Spirit: first necrotic/hex damage per target per round adds 1. Renewal: on start and each of next 2 turns with Bonus Action+1 RP maintenance, up to 3 allies regain 2 HP. Thus Renewal total cost 4 RP for 3 pulses; no free healing on entry. All totems share one concentration burden; losing it ends all. Other concentration effects replace them. Non-Renewal auras need no Bonus Action upkeep. Multiple same-name/stat auras do not stack."
      },
      "status": "SOURCE-AUDITED / DRAFTABLE; exact implementation review pending",
      "classification": "TOTEM_ENGINE/UPKEEP",
      "operationalOverrides": [
        "Current lifecycle/command role is defined in DEVICE_LIFECYCLE_PLAYTEST.md. Boundary and predicate replies supersede conflicting initial proposals. Full card effects are not certified.",
        "Shared owner command/damage ledgers, source-qualified life states, original expiry, slot footprint, protected-disable and destruction provenance apply only where the source role calls for them."
      ],
      "reviewEvidence": [
        "GPT_DEVICE_LIFECYCLE_FIRST_REVIEW.md",
        "GPT_DEVICE_LIFECYCLE_BOUNDARIES.md",
        "GPT_DEVICE_LIFECYCLE_PREDICATES.md"
      ],
      "openIssues": [
        "Exact implementation review pending; other effects and wider companion completeness remain outside this bounded role."
      ]
    },
    {
      "bindingId": "shaman.engine[2]",
      "sourceKind": "class-engine",
      "sourcePath": "data/public/class_playtests/shaman.json",
      "sourceId": 2,
      "sourceSha256": "673d1b3887e874041180d1c813ee02efa51962dbc07a33844853a708b1468a5a",
      "candidateOrigin": "Lexical candidate inventory",
      "sourceProcedure": {
        "text": "On your turn you may spend Bonus Action to move one totem up to 15 ft along unobstructed ground, remaining within 60 ft. This competes with healing maintenance, companion commands and advanced flasks. Moving an aura over a creature cannot trigger its once/round effect repeatedly. Totem destruction creates no resource return. Once per round, the first ordinary spell cast while inside your own active totem aura generates 1 less Dissonance, minimum 0; no RP reduction."
      },
      "status": "SOURCE-AUDITED / DRAFTABLE; exact implementation review pending",
      "classification": "TOTEM_MOVE/BA_GUARD",
      "operationalOverrides": [
        "Current lifecycle/command role is defined in DEVICE_LIFECYCLE_PLAYTEST.md. Boundary and predicate replies supersede conflicting initial proposals. Full card effects are not certified.",
        "Shared owner command/damage ledgers, source-qualified life states, original expiry, slot footprint, protected-disable and destruction provenance apply only where the source role calls for them."
      ],
      "reviewEvidence": [
        "GPT_DEVICE_LIFECYCLE_FIRST_REVIEW.md",
        "GPT_DEVICE_LIFECYCLE_BOUNDARIES.md",
        "GPT_DEVICE_LIFECYCLE_PREDICATES.md"
      ],
      "openIssues": [
        "Exact implementation review pending; other effects and wider companion completeness remain outside this bounded role."
      ]
    },
    {
      "bindingId": "shaman.engine[5]",
      "sourceKind": "class-engine",
      "sourcePath": "data/public/class_playtests/shaman.json",
      "sourceId": 5,
      "sourceSha256": "e52ff035f378a5a8443bb9756f6c99b712a221581ad4def15b78be95ca9df429",
      "candidateOrigin": "Lexical candidate inventory",
      "sourceProcedure": {
        "text": "Choose Fire/Ice/Air/Earth bonuses through affinity card; Ember/Cold/Shock damage are fire/cold/lightning, Earth uses bludgeoning. Summoned elemental spirits use one standard companion each, maximum one normally; Elemental Chorus expressly summons a package of 4 but all share one Bonus Action command and a printed combined pulse. Companions cannot generate RP, trigger flask refunds or create corpse/kill farms."
      },
      "status": "SOURCE-AUDITED / DRAFTABLE; exact implementation review pending",
      "classification": "COMPANION_ENGINE",
      "operationalOverrides": [
        "Current lifecycle/command role is defined in DEVICE_LIFECYCLE_PLAYTEST.md. Boundary and predicate replies supersede conflicting initial proposals. Full card effects are not certified.",
        "Shared owner command/damage ledgers, source-qualified life states, original expiry, slot footprint, protected-disable and destruction provenance apply only where the source role calls for them."
      ],
      "reviewEvidence": [
        "GPT_DEVICE_LIFECYCLE_FIRST_REVIEW.md",
        "GPT_DEVICE_LIFECYCLE_BOUNDARIES.md",
        "GPT_DEVICE_LIFECYCLE_PREDICATES.md"
      ],
      "openIssues": [
        "Exact implementation review pending; other effects and wider companion completeness remain outside this bounded role."
      ]
    },
    {
      "bindingId": "shaman.engine[6]",
      "sourceKind": "class-engine",
      "sourcePath": "data/public/class_playtests/shaman.json",
      "sourceId": 6,
      "sourceSha256": "d1730f0e5af3cebe4d5e6d67824b97a1d6a5bd7c33316a7387f772bdc6188caf",
      "candidateOrigin": "Lexical candidate inventory",
      "sourceProcedure": {
        "text": "Bloodcaller at Hero 10 transforms permanently into Hagraven, with the player choosing this class path and its stated loss of ordinary Shaman spellcasting. It does NOT lose its RP reservoir: printed Hagraven/Totem techniques still pay RP, but it cannot cast ordinary Shaman spells or advanced magical flasks. It retains prior totem/technique selections. The change is a class choice, not permission for involuntary player-character conversion; ancestry identity and player control remain. At long rest it can prepare mundane flasks only if Base Flask Use is known."
      },
      "status": "SOURCE-AUDITED / DRAFTABLE; exact implementation review pending",
      "classification": "CLASS_EXCLUSION",
      "operationalOverrides": [
        "Current lifecycle/command role is defined in DEVICE_LIFECYCLE_PLAYTEST.md. Boundary and predicate replies supersede conflicting initial proposals. Full card effects are not certified.",
        "Shared owner command/damage ledgers, source-qualified life states, original expiry, slot footprint, protected-disable and destruction provenance apply only where the source role calls for them."
      ],
      "reviewEvidence": [
        "GPT_DEVICE_LIFECYCLE_FIRST_REVIEW.md",
        "GPT_DEVICE_LIFECYCLE_BOUNDARIES.md",
        "GPT_DEVICE_LIFECYCLE_PREDICATES.md"
      ],
      "openIssues": [
        "Exact implementation review pending; other effects and wider companion completeness remain outside this bounded role."
      ]
    },
    {
      "bindingId": "shaman.base.totem-casting",
      "sourceKind": "class-card",
      "sourcePath": "data/public/class_playtests/shaman.json",
      "sourceId": "shaman.base.totem-casting",
      "sourceSha256": "9c40be7a051134453ef6940a3cb64473df490359731255e8e7f7e9b829109449",
      "candidateOrigin": "Lexical candidate inventory",
      "sourceProcedure": {
        "name": "Totem Casting",
        "activation": "Action",
        "cost": "2 RP; Renewal upkeep 1 RP+Bonus Action",
        "rangeAndTarget": "One totem within 30 ft with 15 ft aura",
        "duration": "3 of your turns",
        "frequency": "Capacity 1, 2 at 13",
        "effect": "Place one Flame/Stone/Frost/Spirit/Renewal totem using the engine's exact profile. All your totems share concentration. Respect 3 creature aura/pulse limit; same-stat bonuses do not stack. Replacing a totem ends it without refund."
      },
      "status": "SOURCE-AUDITED / DRAFTABLE; exact implementation review pending",
      "classification": "TOTEM_DEPLOY",
      "operationalOverrides": [
        "Current lifecycle/command role is defined in DEVICE_LIFECYCLE_PLAYTEST.md. Boundary and predicate replies supersede conflicting initial proposals. Full card effects are not certified.",
        "Shared owner command/damage ledgers, source-qualified life states, original expiry, slot footprint, protected-disable and destruction provenance apply only where the source role calls for them."
      ],
      "reviewEvidence": [
        "GPT_DEVICE_LIFECYCLE_FIRST_REVIEW.md",
        "GPT_DEVICE_LIFECYCLE_BOUNDARIES.md",
        "GPT_DEVICE_LIFECYCLE_PREDICATES.md"
      ],
      "openIssues": [
        "Exact implementation review pending; other effects and wider companion completeness remain outside this bounded role."
      ]
    },
    {
      "bindingId": "shaman.base.spirit-shock",
      "sourceKind": "class-card",
      "sourcePath": "data/public/class_playtests/shaman.json",
      "sourceId": "shaman.base.spirit-shock",
      "sourceSha256": "4f60fb72993176568e693ec766dbc647323f6188bb3282d533db8ea75582ced0",
      "candidateOrigin": "Lexical candidate inventory",
      "sourceProcedure": {
        "name": "Spirit Shock",
        "activation": "Action",
        "cost": "2 RP",
        "rangeAndTarget": "One enemy within 60 ft",
        "duration": "Instant",
        "frequency": "Recharge 2",
        "effect": "Target makes DEX save: S d8 affinity damage, half on success. Affinity rider applies once; this printed technique is not an ordinary spell, cannot Overcast and does not generate a flask or totem."
      },
      "status": "SOURCE-AUDITED / DRAFTABLE; exact implementation review pending",
      "classification": "EXCLUSION",
      "operationalOverrides": [
        "Current lifecycle/command role is defined in DEVICE_LIFECYCLE_PLAYTEST.md. Boundary and predicate replies supersede conflicting initial proposals. Full card effects are not certified.",
        "Shared owner command/damage ledgers, source-qualified life states, original expiry, slot footprint, protected-disable and destruction provenance apply only where the source role calls for them."
      ],
      "reviewEvidence": [
        "GPT_DEVICE_LIFECYCLE_FIRST_REVIEW.md",
        "GPT_DEVICE_LIFECYCLE_BOUNDARIES.md",
        "GPT_DEVICE_LIFECYCLE_PREDICATES.md"
      ],
      "openIssues": [
        "Exact implementation review pending; other effects and wider companion completeness remain outside this bounded role."
      ]
    },
    {
      "bindingId": "shaman.arch.extended-totem-duration",
      "sourceKind": "class-card",
      "sourcePath": "data/public/class_playtests/shaman.json",
      "sourceId": "shaman.arch.extended-totem-duration",
      "sourceSha256": "d3e1a07ab47f089ce66a98f3ef5083eb604f55174892955836175df7c94724bb",
      "candidateOrigin": "Lexical candidate inventory",
      "sourceProcedure": {
        "name": "Extended Totem Duration",
        "activation": "Passive",
        "cost": "0; full upkeep for extra Renewal pulse",
        "rangeAndTarget": "One of your totems",
        "duration": "Maximum 4 of your turns",
        "frequency": "Continuous",
        "effect": "Totems last 1 extra turn. Renewal may have a fourth pulse only if you pay Bonus Action+1 RP on that turn; no fifth pulse and no automatic free healing. Concentration still required."
      },
      "status": "SOURCE-AUDITED / DRAFTABLE; exact implementation review pending",
      "classification": "TOTEM_DURATION",
      "operationalOverrides": [
        "Current lifecycle/command role is defined in DEVICE_LIFECYCLE_PLAYTEST.md. Boundary and predicate replies supersede conflicting initial proposals. Full card effects are not certified.",
        "Shared owner command/damage ledgers, source-qualified life states, original expiry, slot footprint, protected-disable and destruction provenance apply only where the source role calls for them."
      ],
      "reviewEvidence": [
        "GPT_DEVICE_LIFECYCLE_FIRST_REVIEW.md",
        "GPT_DEVICE_LIFECYCLE_BOUNDARIES.md",
        "GPT_DEVICE_LIFECYCLE_PREDICATES.md"
      ],
      "openIssues": [
        "Exact implementation review pending; other effects and wider companion completeness remain outside this bounded role."
      ]
    },
    {
      "bindingId": "shaman.arch.spirit-cache",
      "sourceKind": "class-card",
      "sourcePath": "data/public/class_playtests/shaman.json",
      "sourceId": "shaman.arch.spirit-cache",
      "sourceSha256": "9a84d6cf21f387bfc7fc32c7e9e7344aa7449da4abd8e24b96e76710e18249ce",
      "candidateOrigin": "Lexical candidate inventory",
      "sourceProcedure": {
        "name": "Spirit Cache",
        "activation": "Triggered",
        "cost": "1 short-rest use",
        "rangeAndTarget": "One flask/to-tem effect you directly used",
        "duration": "Stored until encounter end",
        "frequency": "1/short rest",
        "effect": "Store its profile, not an active copy. On a later turn use normal Action/Bonus Action and pay all RP and a new flask unit or full totem cost to repeat it. Add 1d6 to one numerical damage/heal amount; no copy of refund/limited use."
      },
      "status": "SOURCE-AUDITED / DRAFTABLE; exact implementation review pending",
      "classification": "PROFILE_REPEAT",
      "operationalOverrides": [
        "Current lifecycle/command role is defined in DEVICE_LIFECYCLE_PLAYTEST.md. Boundary and predicate replies supersede conflicting initial proposals. Full card effects are not certified.",
        "Shared owner command/damage ledgers, source-qualified life states, original expiry, slot footprint, protected-disable and destruction provenance apply only where the source role calls for them."
      ],
      "reviewEvidence": [
        "GPT_DEVICE_LIFECYCLE_FIRST_REVIEW.md",
        "GPT_DEVICE_LIFECYCLE_BOUNDARIES.md",
        "GPT_DEVICE_LIFECYCLE_PREDICATES.md"
      ],
      "openIssues": [
        "Exact implementation review pending; other effects and wider companion completeness remain outside this bounded role."
      ]
    },
    {
      "bindingId": "shaman.arch.totem-pulse",
      "sourceKind": "class-card",
      "sourcePath": "data/public/class_playtests/shaman.json",
      "sourceId": "shaman.arch.totem-pulse",
      "sourceSha256": "da88a2c237b85efcd2b52a63b65f8a2decafbdc6671d11820ab72f859f0c0ce6",
      "candidateOrigin": "Lexical candidate inventory",
      "sourceProcedure": {
        "name": "Totem Pulse",
        "activation": "Passive",
        "cost": "1 RP optional",
        "rangeAndTarget": "Up to 3 creatures inside newly placed non-healing totem",
        "duration": "Instant",
        "frequency": "Once/turn",
        "effect": "On placement pay 1 RP: allies gain M temporary HP OR enemies make DEX save for S affinity damage, half on success. No immediate second Renewal healing pulse, no repeat from moving the totem."
      },
      "status": "SOURCE-AUDITED / DRAFTABLE; exact implementation review pending",
      "classification": "PLACEMENT_RIDER",
      "operationalOverrides": [
        "Current lifecycle/command role is defined in DEVICE_LIFECYCLE_PLAYTEST.md. Boundary and predicate replies supersede conflicting initial proposals. Full card effects are not certified.",
        "Shared owner command/damage ledgers, source-qualified life states, original expiry, slot footprint, protected-disable and destruction provenance apply only where the source role calls for them."
      ],
      "reviewEvidence": [
        "GPT_DEVICE_LIFECYCLE_FIRST_REVIEW.md",
        "GPT_DEVICE_LIFECYCLE_BOUNDARIES.md",
        "GPT_DEVICE_LIFECYCLE_PREDICATES.md"
      ],
      "openIssues": [
        "Exact implementation review pending; other effects and wider companion completeness remain outside this bounded role."
      ]
    },
    {
      "bindingId": "shaman.arch.spirit-saturation",
      "sourceKind": "class-card",
      "sourcePath": "data/public/class_playtests/shaman.json",
      "sourceId": "shaman.arch.spirit-saturation",
      "sourceSha256": "e25c049b60111d478b8844f935bfdf3b1f6068d80100de6a8c2d702a9723f543",
      "candidateOrigin": "Lexical candidate inventory",
      "sourceProcedure": {
        "name": "Spirit Saturation",
        "activation": "Triggered",
        "cost": "1 long-rest use",
        "rangeAndTarget": "One non-Renewal totem you place",
        "duration": "Normal duration",
        "frequency": "1/long rest",
        "effect": "Waive its 2 RP placement cost once. Still use Action, concentration, capacity and any added costs. Cannot create a healing totem or be cached/refunded to generate more free casts."
      },
      "status": "SOURCE-AUDITED / DRAFTABLE; exact implementation review pending",
      "classification": "COST_MODIFIER",
      "operationalOverrides": [
        "Current lifecycle/command role is defined in DEVICE_LIFECYCLE_PLAYTEST.md. Boundary and predicate replies supersede conflicting initial proposals. Full card effects are not certified.",
        "Shared owner command/damage ledgers, source-qualified life states, original expiry, slot footprint, protected-disable and destruction provenance apply only where the source role calls for them."
      ],
      "reviewEvidence": [
        "GPT_DEVICE_LIFECYCLE_FIRST_REVIEW.md",
        "GPT_DEVICE_LIFECYCLE_BOUNDARIES.md",
        "GPT_DEVICE_LIFECYCLE_PREDICATES.md"
      ],
      "openIssues": [
        "Exact implementation review pending; other effects and wider companion completeness remain outside this bounded role."
      ]
    },
    {
      "bindingId": "shaman.arch.elemental-channeling",
      "sourceKind": "class-card",
      "sourcePath": "data/public/class_playtests/shaman.json",
      "sourceId": "shaman.arch.elemental-channeling",
      "sourceSha256": "66b91020be5c1c09376f4bcca08c8d632f5c6931604418e30684dce88e09e445",
      "candidateOrigin": "Lexical candidate inventory",
      "sourceProcedure": {
        "name": "Elemental Channeling",
        "activation": "Bonus Action",
        "cost": "2 RP",
        "rangeAndTarget": "Self",
        "duration": "Concentration, 3 of your turns",
        "frequency": "Recharge 3",
        "effect": "Embody affinity: gain+10 ft Speed and once/turn add 1d4 affinity damage to a weapon hit. Fire/cold/lightning/bludgeoning by affinity. This concentration replaces your totem burden, so it is a tactical alternative."
      },
      "status": "SOURCE-AUDITED / DRAFTABLE; exact implementation review pending",
      "classification": "CONCENTRATION_REPLACEMENT",
      "operationalOverrides": [
        "Current lifecycle/command role is defined in DEVICE_LIFECYCLE_PLAYTEST.md. Boundary and predicate replies supersede conflicting initial proposals. Full card effects are not certified.",
        "Shared owner command/damage ledgers, source-qualified life states, original expiry, slot footprint, protected-disable and destruction provenance apply only where the source role calls for them."
      ],
      "reviewEvidence": [
        "GPT_DEVICE_LIFECYCLE_FIRST_REVIEW.md",
        "GPT_DEVICE_LIFECYCLE_BOUNDARIES.md",
        "GPT_DEVICE_LIFECYCLE_PREDICATES.md"
      ],
      "openIssues": [
        "Exact implementation review pending; other effects and wider companion completeness remain outside this bounded role."
      ]
    },
    {
      "bindingId": "shaman.arch.ancestral-guardian",
      "sourceKind": "class-card",
      "sourcePath": "data/public/class_playtests/shaman.json",
      "sourceId": "shaman.arch.ancestral-guardian",
      "sourceSha256": "2017eae94ed31d166adb032bf4a724b44206a006fbf7fc23ec6eb0e6fa5aae8e",
      "candidateOrigin": "Lexical candidate inventory",
      "sourceProcedure": {
        "name": "Ancestral Guardian",
        "activation": "Reaction",
        "cost": "2 RP",
        "rangeAndTarget": "Ally within 30 ft being damaged",
        "duration": "One damage instance",
        "frequency": "Recharge 3",
        "effect": "A guardian prevents S d8+M damage, minimum 0. It then vanishes and creates no companion action, corpse or refund. Cannot prevent sacrifice/trauma or redirect prevented damage into another trigger."
      },
      "status": "SOURCE-AUDITED / DRAFTABLE; exact implementation review pending",
      "classification": "EXCLUSION/PREVENTION",
      "operationalOverrides": [
        "Current lifecycle/command role is defined in DEVICE_LIFECYCLE_PLAYTEST.md. Boundary and predicate replies supersede conflicting initial proposals. Full card effects are not certified.",
        "Shared owner command/damage ledgers, source-qualified life states, original expiry, slot footprint, protected-disable and destruction provenance apply only where the source role calls for them."
      ],
      "reviewEvidence": [
        "GPT_DEVICE_LIFECYCLE_FIRST_REVIEW.md",
        "GPT_DEVICE_LIFECYCLE_BOUNDARIES.md",
        "GPT_DEVICE_LIFECYCLE_PREDICATES.md"
      ],
      "openIssues": [
        "Exact implementation review pending; other effects and wider companion completeness remain outside this bounded role."
      ]
    },
    {
      "bindingId": "shaman.arch.elemental-surge",
      "sourceKind": "class-card",
      "sourcePath": "data/public/class_playtests/shaman.json",
      "sourceId": "shaman.arch.elemental-surge",
      "sourceSha256": "b0edce0be3a43bb6aaac85f2c17c99bf67778f375e2fa2fbc5b1251e14915633",
      "candidateOrigin": "Lexical candidate inventory",
      "sourceProcedure": {
        "name": "Elemental Surge",
        "activation": "Bonus Action",
        "cost": "2 RP",
        "rangeAndTarget": "One active totem within 60 ft",
        "duration": "Until start next turn",
        "frequency": "Recharge 3",
        "effect": "Choose one: aura radius+5 ft OR numerical flat benefit improves by 1. Renewal instead adds M HP to its next paid pulse, once, without adding a pulse. Same-name/stat stacking rules remain."
      },
      "status": "SOURCE-AUDITED / DRAFTABLE; exact implementation review pending",
      "classification": "TOTEM_MODIFIER",
      "operationalOverrides": [
        "Current lifecycle/command role is defined in DEVICE_LIFECYCLE_PLAYTEST.md. Boundary and predicate replies supersede conflicting initial proposals. Full card effects are not certified.",
        "Shared owner command/damage ledgers, source-qualified life states, original expiry, slot footprint, protected-disable and destruction provenance apply only where the source role calls for them."
      ],
      "reviewEvidence": [
        "GPT_DEVICE_LIFECYCLE_FIRST_REVIEW.md",
        "GPT_DEVICE_LIFECYCLE_BOUNDARIES.md",
        "GPT_DEVICE_LIFECYCLE_PREDICATES.md"
      ],
      "openIssues": [
        "Exact implementation review pending; other effects and wider companion completeness remain outside this bounded role."
      ]
    },
    {
      "bindingId": "shaman.hero.theurgist.echo-totem",
      "sourceKind": "class-card",
      "sourcePath": "data/public/class_playtests/shaman.json",
      "sourceId": "shaman.hero.theurgist.echo-totem",
      "sourceSha256": "20874e77366801074f6dc417c26450a1957dab6d55ca77ba083e370fec3fa92b",
      "candidateOrigin": "Lexical candidate inventory",
      "sourceProcedure": {
        "name": "Echo Totem",
        "activation": "Triggered",
        "cost": "1 additional RP",
        "rangeAndTarget": "Adjacent empty space within 5 ft of newly placed totem",
        "duration": "Same remaining duration",
        "frequency": "Once/placement",
        "effect": "Create a weak echo anchor of that totem. It counts toward capacity; if no space in capacity, cannot create it. Its radius 10 ft and numerical bonuses/healing are half, rounded down. Shared concentration/upkeep and same-name nonstacking prevent double healing."
      },
      "status": "SOURCE-AUDITED / DRAFTABLE; exact implementation review pending",
      "classification": "TOTEM_CHILD/CAPACITY",
      "operationalOverrides": [
        "Current lifecycle/command role is defined in DEVICE_LIFECYCLE_PLAYTEST.md. Boundary and predicate replies supersede conflicting initial proposals. Full card effects are not certified.",
        "Shared owner command/damage ledgers, source-qualified life states, original expiry, slot footprint, protected-disable and destruction provenance apply only where the source role calls for them."
      ],
      "reviewEvidence": [
        "GPT_DEVICE_LIFECYCLE_FIRST_REVIEW.md",
        "GPT_DEVICE_LIFECYCLE_BOUNDARIES.md",
        "GPT_DEVICE_LIFECYCLE_PREDICATES.md"
      ],
      "openIssues": [
        "Exact implementation review pending; other effects and wider companion completeness remain outside this bounded role."
      ]
    },
    {
      "bindingId": "shaman.hero.theurgist.elemental-harmony",
      "sourceKind": "class-card",
      "sourcePath": "data/public/class_playtests/shaman.json",
      "sourceId": "shaman.hero.theurgist.elemental-harmony",
      "sourceSha256": "d888897e75f58e90c484e854a9686be7b3a4fddb44bd65235cde7ac1980a94e2",
      "candidateOrigin": "Lexical candidate inventory",
      "sourceProcedure": {
        "name": "Elemental Harmony",
        "activation": "Passive",
        "cost": "0",
        "rangeAndTarget": "Your summoned elemental",
        "duration": "Summon duration",
        "frequency": "Continuous",
        "effect": "Add class level to its maximum/current HP on creation and 1 turn duration, maximum 4 turns for class summons. Cannot extend once/day Chorus beyond 4 turns or restore an existing creature's lost HP."
      },
      "status": "SOURCE-AUDITED / DRAFTABLE; exact implementation review pending",
      "classification": "SUMMON_CREATION_MOD",
      "operationalOverrides": [
        "Current lifecycle/command role is defined in DEVICE_LIFECYCLE_PLAYTEST.md. Boundary and predicate replies supersede conflicting initial proposals. Full card effects are not certified.",
        "Shared owner command/damage ledgers, source-qualified life states, original expiry, slot footprint, protected-disable and destruction provenance apply only where the source role calls for them."
      ],
      "reviewEvidence": [
        "GPT_DEVICE_LIFECYCLE_FIRST_REVIEW.md",
        "GPT_DEVICE_LIFECYCLE_BOUNDARIES.md",
        "GPT_DEVICE_LIFECYCLE_PREDICATES.md"
      ],
      "openIssues": [
        "Exact implementation review pending; other effects and wider companion completeness remain outside this bounded role."
      ]
    },
    {
      "bindingId": "shaman.hero.theurgist.spiritual-resonance",
      "sourceKind": "class-card",
      "sourcePath": "data/public/class_playtests/shaman.json",
      "sourceId": "shaman.hero.theurgist.spiritual-resonance",
      "sourceSha256": "8f882cdc7c007d25afc734df7d5d303dea4b7473853191f501c720ea6c8667bb",
      "candidateOrigin": "Lexical candidate inventory",
      "sourceProcedure": {
        "name": "Spiritual Resonance",
        "activation": "Passive",
        "cost": "0",
        "rangeAndTarget": "Two of your active totems within 10 ft of one another",
        "duration": "While placement condition holds",
        "frequency": "Continuous",
        "effect": "Their aura radii increase 5 ft. No extra targets or extra pulses and overlapping same-name benefits do not stack. One totem and its echo still use normal capacity."
      },
      "status": "SOURCE-AUDITED / DRAFTABLE; exact implementation review pending",
      "classification": "TOTEM_RADIUS_MOD",
      "operationalOverrides": [
        "Current lifecycle/command role is defined in DEVICE_LIFECYCLE_PLAYTEST.md. Boundary and predicate replies supersede conflicting initial proposals. Full card effects are not certified.",
        "Shared owner command/damage ledgers, source-qualified life states, original expiry, slot footprint, protected-disable and destruction provenance apply only where the source role calls for them."
      ],
      "reviewEvidence": [
        "GPT_DEVICE_LIFECYCLE_FIRST_REVIEW.md",
        "GPT_DEVICE_LIFECYCLE_BOUNDARIES.md",
        "GPT_DEVICE_LIFECYCLE_PREDICATES.md"
      ],
      "openIssues": [
        "Exact implementation review pending; other effects and wider companion completeness remain outside this bounded role."
      ]
    },
    {
      "bindingId": "shaman.hero.theurgist.summon-ice-wisp",
      "sourceKind": "class-card",
      "sourcePath": "data/public/class_playtests/shaman.json",
      "sourceId": "shaman.hero.theurgist.summon-ice-wisp",
      "sourceSha256": "61bdd76cc7b08db81abaeb59e356d8a02a36c2492153824a7c47b05a8970baa7",
      "candidateOrigin": "Lexical candidate inventory",
      "sourceProcedure": {
        "name": "Summon Ice Wisp",
        "activation": "Action",
        "cost": "4 RP",
        "rangeAndTarget": "One spirit in empty space within 30 ft",
        "duration": "Concentration, 3 of your turns",
        "frequency": "Recharge 4",
        "effect": "Summon standard Ice Wisp with fly 30 ft. Commanded attack deals cold; on hit target STR save or Speed 0 until end its next turn. No whole-turn freezing, bonus independent spells or multiple companion attacks."
      },
      "status": "SOURCE-AUDITED / DRAFTABLE; exact implementation review pending",
      "classification": "STANDARD_COMPANION",
      "operationalOverrides": [
        "Current lifecycle/command role is defined in DEVICE_LIFECYCLE_PLAYTEST.md. Boundary and predicate replies supersede conflicting initial proposals. Full card effects are not certified.",
        "Shared owner command/damage ledgers, source-qualified life states, original expiry, slot footprint, protected-disable and destruction provenance apply only where the source role calls for them."
      ],
      "reviewEvidence": [
        "GPT_DEVICE_LIFECYCLE_FIRST_REVIEW.md",
        "GPT_DEVICE_LIFECYCLE_BOUNDARIES.md",
        "GPT_DEVICE_LIFECYCLE_PREDICATES.md"
      ],
      "openIssues": [
        "Exact implementation review pending; other effects and wider companion completeness remain outside this bounded role."
      ]
    },
    {
      "bindingId": "shaman.hero.theurgist.summon-airling",
      "sourceKind": "class-card",
      "sourcePath": "data/public/class_playtests/shaman.json",
      "sourceId": "shaman.hero.theurgist.summon-airling",
      "sourceSha256": "2fba80f5a7bd4148ebe4caafb68b9c72b95b16e1bae50ced90aeac61974b15b5",
      "candidateOrigin": "Lexical candidate inventory",
      "sourceProcedure": {
        "name": "Summon Airling",
        "activation": "Action",
        "cost": "4 RP",
        "rangeAndTarget": "One spirit within 30 ft",
        "duration": "Concentration, 3 of your turns",
        "frequency": "Recharge 4",
        "effect": "Summon standard Airling with fly 40 ft. Commanded attack deals lightning; on hit target CON save or loses Reactions until end its next turn. Failure by 10 also Stunned, subject to the shared hard-denial guard across all the Shaman’s features. Companion Stun counts as the Shaman’s denial; if the target already suffered that denial this encounter, only damage and Reaction loss resolve. One shared companion command."
      },
      "status": "SOURCE-AUDITED / DRAFTABLE; exact implementation review pending",
      "classification": "STANDARD_COMPANION",
      "operationalOverrides": [
        "Current lifecycle/command role is defined in DEVICE_LIFECYCLE_PLAYTEST.md. Boundary and predicate replies supersede conflicting initial proposals. Full card effects are not certified.",
        "Shared owner command/damage ledgers, source-qualified life states, original expiry, slot footprint, protected-disable and destruction provenance apply only where the source role calls for them."
      ],
      "reviewEvidence": [
        "GPT_DEVICE_LIFECYCLE_FIRST_REVIEW.md",
        "GPT_DEVICE_LIFECYCLE_BOUNDARIES.md",
        "GPT_DEVICE_LIFECYCLE_PREDICATES.md"
      ],
      "openIssues": [
        "Exact implementation review pending; other effects and wider companion completeness remain outside this bounded role."
      ]
    },
    {
      "bindingId": "shaman.hero.theurgist.summon-cinderflame",
      "sourceKind": "class-card",
      "sourcePath": "data/public/class_playtests/shaman.json",
      "sourceId": "shaman.hero.theurgist.summon-cinderflame",
      "sourceSha256": "f4422bf6b56fe62a9c13837fb6728fad8bd76836897d6c291001372a858291f4",
      "candidateOrigin": "Lexical candidate inventory",
      "sourceProcedure": {
        "name": "Summon Cinderflame",
        "activation": "Action",
        "cost": "4 RP",
        "rangeAndTarget": "One spirit within 30 ft",
        "duration": "Concentration, 3 of your turns",
        "frequency": "Recharge 4",
        "effect": "Summon standard Cinderflame. Commanded hit deals fire plus Burn 1d4 next target turn. On destruction only (not dismissal), up to 3 enemies within 5 ft make DEX save for S d4 fire, half. Explosion creates no further death/resource triggers."
      },
      "status": "SOURCE-AUDITED / DRAFTABLE; exact implementation review pending",
      "classification": "STANDARD_COMPANION/DEATH_RIDER",
      "operationalOverrides": [
        "Current lifecycle/command role is defined in DEVICE_LIFECYCLE_PLAYTEST.md. Boundary and predicate replies supersede conflicting initial proposals. Full card effects are not certified.",
        "Shared owner command/damage ledgers, source-qualified life states, original expiry, slot footprint, protected-disable and destruction provenance apply only where the source role calls for them."
      ],
      "reviewEvidence": [
        "GPT_DEVICE_LIFECYCLE_FIRST_REVIEW.md",
        "GPT_DEVICE_LIFECYCLE_BOUNDARIES.md",
        "GPT_DEVICE_LIFECYCLE_PREDICATES.md"
      ],
      "openIssues": [
        "Exact implementation review pending; other effects and wider companion completeness remain outside this bounded role."
      ]
    },
    {
      "bindingId": "shaman.hero.theurgist.summon-stonekin",
      "sourceKind": "class-card",
      "sourcePath": "data/public/class_playtests/shaman.json",
      "sourceId": "shaman.hero.theurgist.summon-stonekin",
      "sourceSha256": "ae54b5237330899f28393edf638503f69691fb1b685e21128d9a60d0b668e7ef",
      "candidateOrigin": "Lexical candidate inventory",
      "sourceProcedure": {
        "name": "Summon Stonekin",
        "activation": "Action",
        "cost": "4 RP",
        "rangeAndTarget": "One spirit within 30 ft",
        "duration": "Concentration, 3 of your turns",
        "frequency": "Recharge 4",
        "effect": "Summon standard Stonekin. Command chooses bludgeoning attack with STR save or Prone on hit, OR gives up to 3 adjacent allies reduction 2 until start next turn. No simultaneous attack and protection command."
      },
      "status": "SOURCE-AUDITED / DRAFTABLE; exact implementation review pending",
      "classification": "STANDARD_COMPANION/COMMAND_MODE",
      "operationalOverrides": [
        "Current lifecycle/command role is defined in DEVICE_LIFECYCLE_PLAYTEST.md. Boundary and predicate replies supersede conflicting initial proposals. Full card effects are not certified.",
        "Shared owner command/damage ledgers, source-qualified life states, original expiry, slot footprint, protected-disable and destruction provenance apply only where the source role calls for them."
      ],
      "reviewEvidence": [
        "GPT_DEVICE_LIFECYCLE_FIRST_REVIEW.md",
        "GPT_DEVICE_LIFECYCLE_BOUNDARIES.md",
        "GPT_DEVICE_LIFECYCLE_PREDICATES.md"
      ],
      "openIssues": [
        "Exact implementation review pending; other effects and wider companion completeness remain outside this bounded role."
      ]
    },
    {
      "bindingId": "shaman.hero.theurgist.elemental-chorus",
      "sourceKind": "class-card",
      "sourcePath": "data/public/class_playtests/shaman.json",
      "sourceId": "shaman.hero.theurgist.elemental-chorus",
      "sourceSha256": "9b3fc059fd54655db96ffe05b822859aa9b0019583161c412efeac74dc29d366",
      "candidateOrigin": "Lexical candidate inventory",
      "sourceProcedure": {
        "name": "Elemental Chorus",
        "activation": "Action",
        "cost": "8 RP; 1 long-rest use",
        "rangeAndTarget": "Four spirits in 10 ft-radius zone within 30 ft",
        "duration": "Concentration, 3 of your turns",
        "frequency": "1/long rest",
        "effect": "Summon a single Chorus package: four visible spirits share HP 4 L, AC 12+PB, immobile. Bonus Action command pulses up to 3 enemies: DEX save S d6 chosen affinity damage half; one failed target Speed-10 ft until end next turn. Four spirits do not make four separate attacks."
      },
      "status": "SOURCE-AUDITED / DRAFTABLE; exact implementation review pending",
      "classification": "PACKAGE_COMPANION",
      "operationalOverrides": [
        "Current lifecycle/command role is defined in DEVICE_LIFECYCLE_PLAYTEST.md. Boundary and predicate replies supersede conflicting initial proposals. Full card effects are not certified.",
        "Shared owner command/damage ledgers, source-qualified life states, original expiry, slot footprint, protected-disable and destruction provenance apply only where the source role calls for them."
      ],
      "reviewEvidence": [
        "GPT_DEVICE_LIFECYCLE_FIRST_REVIEW.md",
        "GPT_DEVICE_LIFECYCLE_BOUNDARIES.md",
        "GPT_DEVICE_LIFECYCLE_PREDICATES.md"
      ],
      "openIssues": [
        "Exact implementation review pending; other effects and wider companion completeness remain outside this bounded role."
      ]
    },
    {
      "bindingId": "shaman.hero.soothsayer.divining-totem",
      "sourceKind": "class-card",
      "sourcePath": "data/public/class_playtests/shaman.json",
      "sourceId": "shaman.hero.soothsayer.divining-totem",
      "sourceSha256": "479ef4e10c712a39ee1f39c2cae77a668e2c1af6c30f601b91cecee894325d9a",
      "candidateOrigin": "Lexical candidate inventory",
      "sourceProcedure": {
        "name": "Divining Totem",
        "activation": "Action",
        "cost": "3 RP",
        "rangeAndTarget": "One divining totem within 30 ft; observed enemy in aura",
        "duration": "3 of your turns",
        "frequency": "Capacity and concentration as totems",
        "effect": "Each own-turn start choose one visible enemy in 15 ft aura. First ally attack against it before your next turn gains+1 to hit; first attack it makes has-1. Predicts immediate intent, not guaranteed future actions; totem has ordinary object stats."
      },
      "status": "SOURCE-AUDITED / DRAFTABLE; exact implementation review pending",
      "classification": "TOTEM",
      "operationalOverrides": [
        "Current lifecycle/command role is defined in DEVICE_LIFECYCLE_PLAYTEST.md. Boundary and predicate replies supersede conflicting initial proposals. Full card effects are not certified.",
        "Shared owner command/damage ledgers, source-qualified life states, original expiry, slot footprint, protected-disable and destruction provenance apply only where the source role calls for them."
      ],
      "reviewEvidence": [
        "GPT_DEVICE_LIFECYCLE_FIRST_REVIEW.md",
        "GPT_DEVICE_LIFECYCLE_BOUNDARIES.md",
        "GPT_DEVICE_LIFECYCLE_PREDICATES.md"
      ],
      "openIssues": [
        "Exact implementation review pending; other effects and wider companion completeness remain outside this bounded role."
      ]
    },
    {
      "bindingId": "shaman.hero.soothsayer.omen-loop",
      "sourceKind": "class-card",
      "sourcePath": "data/public/class_playtests/shaman.json",
      "sourceId": "shaman.hero.soothsayer.omen-loop",
      "sourceSha256": "a9340726d7e8a9a7b15ef4e6d16ea9e3480f0b388f592977b5ccd6398d313fa4",
      "candidateOrigin": "Lexical candidate inventory",
      "sourceProcedure": {
        "name": "Omen Loop",
        "activation": "Action",
        "cost": "Normal RP+2 RP; fresh flask if required; 1 long-rest use",
        "rangeAndTarget": "Your own qualifying effect used within previous 2 turns",
        "duration": "Normal effect duration",
        "frequency": "1/long rest",
        "effect": "Repeat one non-Finale, non-resource-restoring class flask/totem effect with normal targets and full costs. It replaces the current Action; cannot repeat another repeat, regain per-rest uses or exceed totem capacity. If effect required a flask, consume one now."
      },
      "status": "SOURCE-AUDITED / DRAFTABLE; exact implementation review pending",
      "classification": "REPEAT/DEPLOY",
      "operationalOverrides": [
        "Current lifecycle/command role is defined in DEVICE_LIFECYCLE_PLAYTEST.md. Boundary and predicate replies supersede conflicting initial proposals. Full card effects are not certified.",
        "Shared owner command/damage ledgers, source-qualified life states, original expiry, slot footprint, protected-disable and destruction provenance apply only where the source role calls for them."
      ],
      "reviewEvidence": [
        "GPT_DEVICE_LIFECYCLE_FIRST_REVIEW.md",
        "GPT_DEVICE_LIFECYCLE_BOUNDARIES.md",
        "GPT_DEVICE_LIFECYCLE_PREDICATES.md"
      ],
      "openIssues": [
        "Exact implementation review pending; other effects and wider companion completeness remain outside this bounded role."
      ]
    },
    {
      "bindingId": "shaman.hero.bloodcaller.hagraven-form",
      "sourceKind": "class-card",
      "sourcePath": "data/public/class_playtests/shaman.json",
      "sourceId": "shaman.hero.bloodcaller.hagraven-form",
      "sourceSha256": "245cd9850522e7c414f7f5aac754dd19a5313febc095e7baec549af40194ea39",
      "candidateOrigin": "Lexical candidate inventory",
      "sourceProcedure": {
        "name": "Hagraven Form",
        "activation": "Passive",
        "cost": "0",
        "rangeAndTarget": "Self",
        "duration": "Permanent while Bloodcaller",
        "frequency": "Automatic on Hero entry",
        "effect": "Become Hagraven: retain player control/mental stats, light-armor use and ordinary movement; claws are finesse 1d6 slashing, darkvision 60 ft and poison resistance. Lose ordinary Shaman spellcasting/advanced magical flasks; retain RP for printed techniques and totems. No free flight or hidden monster stat block."
      },
      "status": "SOURCE-AUDITED / DRAFTABLE; exact implementation review pending",
      "classification": "EXCLUSION",
      "operationalOverrides": [
        "Current lifecycle/command role is defined in DEVICE_LIFECYCLE_PLAYTEST.md. Boundary and predicate replies supersede conflicting initial proposals. Full card effects are not certified.",
        "Shared owner command/damage ledgers, source-qualified life states, original expiry, slot footprint, protected-disable and destruction provenance apply only where the source role calls for them."
      ],
      "reviewEvidence": [
        "GPT_DEVICE_LIFECYCLE_FIRST_REVIEW.md",
        "GPT_DEVICE_LIFECYCLE_BOUNDARIES.md",
        "GPT_DEVICE_LIFECYCLE_PREDICATES.md"
      ],
      "openIssues": [
        "Exact implementation review pending; other effects and wider companion completeness remain outside this bounded role."
      ]
    },
    {
      "bindingId": "shaman.hero.bloodcaller.blood-feast",
      "sourceKind": "class-card",
      "sourcePath": "data/public/class_playtests/shaman.json",
      "sourceId": "shaman.hero.bloodcaller.blood-feast",
      "sourceSha256": "30b3df4c4300374344e5639bdbe04d81fb1a631d5b5c2a5722c0f016a4bb13b3",
      "candidateOrigin": "Lexical candidate inventory",
      "sourceProcedure": {
        "name": "Blood Feast",
        "activation": "Triggered",
        "cost": "1 RP",
        "rangeAndTarget": "Self at start regular turn; hostile bleeding creature within 10 ft",
        "duration": "Instant",
        "frequency": "Once/turn",
        "effect": "Pay 1 RP to regain M HP. Bleeding allies, summons or staged captives cannot qualify. No healing while Downed; secondary heal creates no damage/resource triggers."
      },
      "status": "SOURCE-AUDITED / DRAFTABLE; exact implementation review pending",
      "classification": "EXCLUSION",
      "operationalOverrides": [
        "Current lifecycle/command role is defined in DEVICE_LIFECYCLE_PLAYTEST.md. Boundary and predicate replies supersede conflicting initial proposals. Full card effects are not certified.",
        "Shared owner command/damage ledgers, source-qualified life states, original expiry, slot footprint, protected-disable and destruction provenance apply only where the source role calls for them."
      ],
      "reviewEvidence": [
        "GPT_DEVICE_LIFECYCLE_FIRST_REVIEW.md",
        "GPT_DEVICE_LIFECYCLE_BOUNDARIES.md",
        "GPT_DEVICE_LIFECYCLE_PREDICATES.md"
      ],
      "openIssues": [
        "Exact implementation review pending; other effects and wider companion completeness remain outside this bounded role."
      ]
    },
    {
      "bindingId": "shaman.hero.bloodcaller.blight-totem",
      "sourceKind": "class-card",
      "sourcePath": "data/public/class_playtests/shaman.json",
      "sourceId": "shaman.hero.bloodcaller.blight-totem",
      "sourceSha256": "56bd3dd7b141931dda883f3728d30221c8e34ba30347d55c87fe66dc2f338805",
      "candidateOrigin": "Lexical candidate inventory",
      "sourceProcedure": {
        "name": "Blight Totem",
        "activation": "Action",
        "cost": "3 RP",
        "rangeAndTarget": "Totem within 30 ft; 15 ft aura affecting all creatures",
        "duration": "3 of your turns",
        "frequency": "Ordinary totem capacity/concentration",
        "effect": "HP healing received inside aura is halved, rounding down, including allies and you. Nonstacking with another healing reduction; temporary HP unaffected. This totem has standard object stats and grants no free damage/healing."
      },
      "status": "SOURCE-AUDITED / DRAFTABLE; exact implementation review pending",
      "classification": "TOTEM",
      "operationalOverrides": [
        "Current lifecycle/command role is defined in DEVICE_LIFECYCLE_PLAYTEST.md. Boundary and predicate replies supersede conflicting initial proposals. Full card effects are not certified.",
        "Shared owner command/damage ledgers, source-qualified life states, original expiry, slot footprint, protected-disable and destruction provenance apply only where the source role calls for them."
      ],
      "reviewEvidence": [
        "GPT_DEVICE_LIFECYCLE_FIRST_REVIEW.md",
        "GPT_DEVICE_LIFECYCLE_BOUNDARIES.md",
        "GPT_DEVICE_LIFECYCLE_PREDICATES.md"
      ],
      "openIssues": [
        "Exact implementation review pending; other effects and wider companion completeness remain outside this bounded role."
      ]
    },
    {
      "bindingId": "shaman.supplement.elder-spirit-accord-new-hero-capstone",
      "sourceKind": "class-card",
      "sourcePath": "data/public/class_playtests/shaman.json",
      "sourceId": "shaman.supplement.elder-spirit-accord-new-hero-capstone",
      "sourceSha256": "14135567a903c049f854953b8feb74893959b5f92c58123af008a3d8e67eac70",
      "candidateOrigin": "Lexical candidate inventory",
      "sourceProcedure": {
        "name": "Elder Spirit Accord — new Hero capstone",
        "activation": "Triggered",
        "cost": "1 long-rest use",
        "rangeAndTarget": "Your chosen Hero ultimate",
        "duration": "One activation",
        "frequency": "1/long rest",
        "effect": "When starting Elemental Chorus, Omen Loop or Bloodroot Trail, reduce its RP cost by 3, minimum 1, and add M to one damage/healing roll from that use. You must know that ability and still spend its own limited use. If you do not know it, instead reduce one known Hero technique's RP cost by 3, minimum 1. No extra duration, flask, totem, command or repeated cast."
      },
      "status": "SOURCE-AUDITED / DRAFTABLE; exact implementation review pending",
      "classification": "COST/ROLL_MOD",
      "operationalOverrides": [
        "Current lifecycle/command role is defined in DEVICE_LIFECYCLE_PLAYTEST.md. Boundary and predicate replies supersede conflicting initial proposals. Full card effects are not certified.",
        "Shared owner command/damage ledgers, source-qualified life states, original expiry, slot footprint, protected-disable and destruction provenance apply only where the source role calls for them."
      ],
      "reviewEvidence": [
        "GPT_DEVICE_LIFECYCLE_FIRST_REVIEW.md",
        "GPT_DEVICE_LIFECYCLE_BOUNDARIES.md",
        "GPT_DEVICE_LIFECYCLE_PREDICATES.md"
      ],
      "openIssues": [
        "Exact implementation review pending; other effects and wider companion completeness remain outside this bounded role."
      ]
    },
    {
      "bindingId": "tinker.engine[0]",
      "sourceKind": "class-engine",
      "sourcePath": "data/public/class_playtests/tinker.json",
      "sourceId": 0,
      "sourceSha256": "ace8078ceabd7544eecdbaf7bc0583a2e9fc54d6c224ee449ccab1c370965582",
      "candidateOrigin": "Lexical candidate inventory",
      "sourceProcedure": {
        "text": "Intelligence governs class DC/M, device attacks use PB+INT; Dexterity governs personal ranged weapons. Hit Die d8, light armor, shortbows/crossbows/simple weapons, tinkers tools and alchemist supplies. Technology is fictional equipment. Ordinary Tinker spells use RP/Dissonance; mundane bombs/devices with printed RP fuel costs are class techniques and do not separately count as spell casts."
      },
      "status": "SOURCE-AUDITED / DRAFTABLE; exact implementation review pending",
      "classification": "DEVICE_BASE",
      "operationalOverrides": [
        "Current lifecycle/command role is defined in DEVICE_LIFECYCLE_PLAYTEST.md. Boundary and predicate replies supersede conflicting initial proposals. Full card effects are not certified.",
        "Shared owner command/damage ledgers, source-qualified life states, original expiry, slot footprint, protected-disable and destruction provenance apply only where the source role calls for them."
      ],
      "reviewEvidence": [
        "GPT_DEVICE_LIFECYCLE_FIRST_REVIEW.md",
        "GPT_DEVICE_LIFECYCLE_BOUNDARIES.md",
        "GPT_DEVICE_LIFECYCLE_PREDICATES.md"
      ],
      "openIssues": [
        "Exact implementation review pending; other effects and wider companion completeness remain outside this bounded role."
      ]
    },
    {
      "bindingId": "tinker.engine[1]",
      "sourceKind": "class-engine",
      "sourcePath": "data/public/class_playtests/tinker.json",
      "sourceId": 1,
      "sourceSha256": "58f25de4d57c94d78536bc487deabc2d878e86224dfe9f544a029d4b79e51986",
      "candidateOrigin": "Lexical candidate inventory",
      "sourceProcedure": {
        "text": "At 1 automatically own one Anacite Drone: AC 13+INT modifier, HP 5+INT modifier+class level (minimum 1), flight 30 ft, ranged bolt 60 ft attack PB+INT for 1d6 piercing. Bonus Action commands one move and one attack or named module action; otherwise it Dodges and may follow you. On bolt hit roll d4; on 4 target CON save or cannot take Reactions through end next turn (Shock, no automatic Stun). All drones/turrets/scraplings share ONE damaging action per Bonus Action command per regular turn unless a card explicitly supplies a priced extra attack. No autonomous barrage. Drone is a construct, not immune to all conditions; poison/psychic immunity, no charm. Carry/retract it in 1 minute; no pocket extra world or passenger flight."
      },
      "status": "SOURCE-AUDITED / DRAFTABLE; exact implementation review pending",
      "classification": "DRONE/CMD_ENGINE",
      "operationalOverrides": [
        "Current lifecycle/command role is defined in DEVICE_LIFECYCLE_PLAYTEST.md. Boundary and predicate replies supersede conflicting initial proposals. Full card effects are not certified.",
        "Shared owner command/damage ledgers, source-qualified life states, original expiry, slot footprint, protected-disable and destruction provenance apply only where the source role calls for them."
      ],
      "reviewEvidence": [
        "GPT_DEVICE_LIFECYCLE_FIRST_REVIEW.md",
        "GPT_DEVICE_LIFECYCLE_BOUNDARIES.md",
        "GPT_DEVICE_LIFECYCLE_PREDICATES.md"
      ],
      "openIssues": [
        "Exact implementation review pending; other effects and wider companion completeness remain outside this bounded role."
      ]
    },
    {
      "bindingId": "tinker.engine[2]",
      "sourceKind": "class-engine",
      "sourcePath": "data/public/class_playtests/tinker.json",
      "sourceId": 2,
      "sourceSha256": "fc21b2a2fbc8af0dc175d90e8d8be5d9a90480a1c8aab1ec23d7aa0d6eebd01a",
      "candidateOrigin": "Lexical candidate inventory",
      "sourceProcedure": {
        "text": "A destroyed drone remains 0 HP until repaired for 1 RP and 10 minutes with tools to half HP, once/short rest, or rebuilt during long rest to full. Ordinary repairing does not recharge devices, grant organic healing or trigger destruction bonuses. At 13 Dual Drone Protocols automatically chooses on each long rest either 2 basic drones each with one module, or one drone with 2 distinct modules. Still one command budget. Never more than 2 drones."
      },
      "status": "SOURCE-AUDITED / DRAFTABLE; exact implementation review pending",
      "classification": "DRONE_REPAIR/CAP",
      "operationalOverrides": [
        "Current lifecycle/command role is defined in DEVICE_LIFECYCLE_PLAYTEST.md. Boundary and predicate replies supersede conflicting initial proposals. Full card effects are not certified.",
        "Shared owner command/damage ledgers, source-qualified life states, original expiry, slot footprint, protected-disable and destruction provenance apply only where the source role calls for them."
      ],
      "reviewEvidence": [
        "GPT_DEVICE_LIFECYCLE_FIRST_REVIEW.md",
        "GPT_DEVICE_LIFECYCLE_BOUNDARIES.md",
        "GPT_DEVICE_LIFECYCLE_PREDICATES.md"
      ],
      "openIssues": [
        "Exact implementation review pending; other effects and wider companion completeness remain outside this bounded role."
      ]
    },
    {
      "bindingId": "tinker.engine[3]",
      "sourceKind": "class-engine",
      "sourcePath": "data/public/class_playtests/tinker.json",
      "sourceId": 3,
      "sourceSha256": "48ef29ba2043a595ab801397a269579864b2865bee7ef1b72353944421604669",
      "candidateOrigin": "Lexical candidate inventory",
      "sourceProcedure": {
        "text": "At 5 automatically gain one module slot; change module during long rest. Offensive: Burn Injector first bolt hit/turn causes 1d4 fire next 2 target turns; Poison Vents d4=4 on hit CON save or-1 attack rolls until end next turn; Concussive Bolt d4=4 on hit CON save or Stunned until end next turn, once/target/encounter shared denial guard and 1/short-rest successful Stun. Defensive: Target Taunter command action once/encounter WIS save one foe 30 ft or disadvantage attacking others until end next turn; Energy Shield command gives adjacent ally+2 AC until start next turn; Smoke Cloud command once/encounter creates 5 ft radius opaque smoke centered drone until start next turn. Support: Ammo Dispenser adjacent allies first ranged hit/turn+1 damage; Target Scanner command mark 1 visible foe 60 ft first ally attack before start next turn+1 hit; Tether Grappler command once/encounter pulls 1 willing ally 15 ft within 30 ft without opportunity attacks along open route."
      },
      "status": "SOURCE-AUDITED / DRAFTABLE; exact implementation review pending",
      "classification": "MODULE_ENGINE",
      "operationalOverrides": [
        "Current lifecycle/command role is defined in DEVICE_LIFECYCLE_PLAYTEST.md. Boundary and predicate replies supersede conflicting initial proposals. Full card effects are not certified.",
        "Shared owner command/damage ledgers, source-qualified life states, original expiry, slot footprint, protected-disable and destruction provenance apply only where the source role calls for them."
      ],
      "reviewEvidence": [
        "GPT_DEVICE_LIFECYCLE_FIRST_REVIEW.md",
        "GPT_DEVICE_LIFECYCLE_BOUNDARIES.md",
        "GPT_DEVICE_LIFECYCLE_PREDICATES.md"
      ],
      "openIssues": [
        "Exact implementation review pending; other effects and wider companion completeness remain outside this bounded role."
      ]
    },
    {
      "bindingId": "tinker.engine[5]",
      "sourceKind": "class-engine",
      "sourcePath": "data/public/class_playtests/tinker.json",
      "sourceId": 5,
      "sourceSha256": "b9ca3f83e895390256fad13f18df8d32b813c79017cc3d6c236a30444bd566b4",
      "candidateOrigin": "Lexical candidate inventory",
      "sourceProcedure": {
        "text": "Advanced bomb profiles replace basic rider: Thermobaric fire pushes 5 ft on failed STR save after damage; Cryo cold on failed DEX also Speed 0 until end next turn and d2=2 ignores 1 flat DR against this bomb; Shock lightning CON instead DEX, failure prevents verbal spellcasting until end next turn (construct instead loses Reactions), shared hard-denial guard; Glue no damage, 15 ft square difficult terrain 3 rounds and entering/starting DEX save or Speed-15 ft until end turn, once per creature/round. Overload Core destroys one commanded drone within 30 ft as part Action bomb, DEX save 2d6 lightning and no Reactions until end next turn on failure, half damage on success. Consumes stock/allowance; no further destruction proc."
      },
      "status": "SOURCE-AUDITED / DRAFTABLE; exact implementation review pending",
      "classification": "BOMB/SACRIFICE",
      "operationalOverrides": [
        "Current lifecycle/command role is defined in DEVICE_LIFECYCLE_PLAYTEST.md. Boundary and predicate replies supersede conflicting initial proposals. Full card effects are not certified.",
        "Shared owner command/damage ledgers, source-qualified life states, original expiry, slot footprint, protected-disable and destruction provenance apply only where the source role calls for them."
      ],
      "reviewEvidence": [
        "GPT_DEVICE_LIFECYCLE_FIRST_REVIEW.md",
        "GPT_DEVICE_LIFECYCLE_BOUNDARIES.md",
        "GPT_DEVICE_LIFECYCLE_PREDICATES.md"
      ],
      "openIssues": [
        "Exact implementation review pending; other effects and wider companion completeness remain outside this bounded role."
      ]
    },
    {
      "bindingId": "tinker.engine[6]",
      "sourceKind": "class-engine",
      "sourcePath": "data/public/class_playtests/tinker.json",
      "sourceId": 6,
      "sourceSha256": "84965457980b9a985ee4fa4022a0ad0f9b9977760f0e28b93342dc03d005a356",
      "candidateOrigin": "Lexical candidate inventory",
      "sourceProcedure": {
        "text": "Deployable slots start 1 at 6, 2 at 13, 3 at 17, separate from drone cap. Deploy Action 2 RP within 15 ft, fixed ground, AC 12+PB HP 2 L, duration 3 rounds, concentration not required; destroyed do not refund fuel. All share command budget. Sentry and Net require their cards. Additional engine profiles unlocked 6: Rocket Tower commanded attack 60 ft target DEX save S d6 fire/half success to up to 2 creatures within 5 ft, maximum 3 shots; Decoy Dummy one foe 30 ft WIS save when deployed or disadvantage on next attack against others, destruction S fire to one adjacent enemy no chain; Blast Wall 10-by 5 ft blocks LOS and movement, climb cost 10 ft. Net Trap one enemy entry STR save or Restrained, end turn repeat/Action escape DC, 3 round max then ends. One only fires when commanded except nonattack trap/decoy trigger; command budget limits damaging triggers too."
      },
      "status": "SOURCE-AUDITED / DRAFTABLE; exact implementation review pending",
      "classification": "DEPLOYABLE_ENGINE/CAP",
      "operationalOverrides": [
        "Current lifecycle/command role is defined in DEVICE_LIFECYCLE_PLAYTEST.md. Boundary and predicate replies supersede conflicting initial proposals. Full card effects are not certified.",
        "Shared owner command/damage ledgers, source-qualified life states, original expiry, slot footprint, protected-disable and destruction provenance apply only where the source role calls for them."
      ],
      "reviewEvidence": [
        "GPT_DEVICE_LIFECYCLE_FIRST_REVIEW.md",
        "GPT_DEVICE_LIFECYCLE_BOUNDARIES.md",
        "GPT_DEVICE_LIFECYCLE_PREDICATES.md"
      ],
      "openIssues": [
        "Exact implementation review pending; other effects and wider companion completeness remain outside this bounded role."
      ]
    },
    {
      "bindingId": "tinker.engine[7]",
      "sourceKind": "class-engine",
      "sourcePath": "data/public/class_playtests/tinker.json",
      "sourceId": 7,
      "sourceSha256": "9429949777c5be914254699b4403f903a1e617504b801672deaff80b2f0ae0d4",
      "candidateOrigin": "Lexical candidate inventory",
      "sourceProcedure": {
        "text": "Base 1–2, Mechanist Arch 3–9, then Artificer/Techsmith/Warmachine Hero 10–20. Upgrade Slot 5 is automatic; Sentry and Net minimum 6, Remote Detonation 9. There is no source automatic Arch capstone. Mech Overdrive 20 is automatic: once/long rest when deploying choose one device whose duration becomes encounter end (maximum 1 minute), still command dependent, slot limited and destructible. No infinite pulses: healing effects keep original pulse cap and all per-use costs remain. Protected magic interface: once per short rest, as a Bonus Action route up to 2 current Dissonance into one of your active devices within 30 ft. Reduce Dissonance by that amount; the device is disabled and cannot move, attack, emit an aura or trigger effects until repaired or your next completed short rest. Its duration keeps ticking. Repair with an Action and 1 RP using Field Repair, or with 10 minutes and 1 RP using tinkers tools. No RP is created and no Refrain counter resets."
      },
      "status": "SOURCE-AUDITED / DRAFTABLE; exact implementation review pending",
      "classification": "DISABLE/DURATION_GUARD",
      "operationalOverrides": [
        "Current lifecycle/command role is defined in DEVICE_LIFECYCLE_PLAYTEST.md. Boundary and predicate replies supersede conflicting initial proposals. Full card effects are not certified.",
        "Shared owner command/damage ledgers, source-qualified life states, original expiry, slot footprint, protected-disable and destruction provenance apply only where the source role calls for them."
      ],
      "reviewEvidence": [
        "GPT_DEVICE_LIFECYCLE_FIRST_REVIEW.md",
        "GPT_DEVICE_LIFECYCLE_BOUNDARIES.md",
        "GPT_DEVICE_LIFECYCLE_PREDICATES.md"
      ],
      "openIssues": [
        "Exact implementation review pending; other effects and wider companion completeness remain outside this bounded role."
      ]
    },
    {
      "bindingId": "tinker.base.mechanical-aptitude",
      "sourceKind": "class-card",
      "sourcePath": "data/public/class_playtests/tinker.json",
      "sourceId": "tinker.base.mechanical-aptitude",
      "sourceSha256": "a29ef8484546a634482ff8e23ca42ab743ee3c336da424ae2bd0f43b9de85025",
      "candidateOrigin": "Lexical candidate inventory",
      "sourceProcedure": {
        "name": "Mechanical Aptitude",
        "activation": "Passive",
        "cost": "0",
        "rangeAndTarget": "Mechanical devices you examine",
        "duration": "While using tools",
        "frequency": "Continuous",
        "effect": "Advantage on checks to understand, repair or disable mechanisms. Requires appropriate access and tools; no automatic control of enemy constructs."
      },
      "status": "SOURCE-AUDITED / DRAFTABLE; exact implementation review pending",
      "classification": "ACCESS_CHECK",
      "operationalOverrides": [
        "Current lifecycle/command role is defined in DEVICE_LIFECYCLE_PLAYTEST.md. Boundary and predicate replies supersede conflicting initial proposals. Full card effects are not certified.",
        "Shared owner command/damage ledgers, source-qualified life states, original expiry, slot footprint, protected-disable and destruction provenance apply only where the source role calls for them."
      ],
      "reviewEvidence": [
        "GPT_DEVICE_LIFECYCLE_FIRST_REVIEW.md",
        "GPT_DEVICE_LIFECYCLE_BOUNDARIES.md",
        "GPT_DEVICE_LIFECYCLE_PREDICATES.md"
      ],
      "openIssues": [
        "Exact implementation review pending; other effects and wider companion completeness remain outside this bounded role."
      ]
    },
    {
      "bindingId": "tinker.base.explosive-handling",
      "sourceKind": "class-card",
      "sourcePath": "data/public/class_playtests/tinker.json",
      "sourceId": "tinker.base.explosive-handling",
      "sourceSha256": "874e32986d9d3c0186dbd7bef7f232e035bd9818c8cdf2d14693c7e4aa8c8b71",
      "candidateOrigin": "Lexical candidate inventory",
      "sourceProcedure": {
        "name": "Explosive Handling",
        "activation": "Passive",
        "cost": "One bomb and encounter allowance",
        "rangeAndTarget": "Your bomb throw",
        "duration": "Instant",
        "frequency": "Once/own turn",
        "effect": "Throw a known prepared bomb as Bonus Action instead of Action. Removes ordinary accidental misfire, not Warmachine risk or enemy defenses. Cannot command a device with the same Bonus Action."
      },
      "status": "SOURCE-AUDITED / DRAFTABLE; exact implementation review pending",
      "classification": "BA_ECONOMY",
      "operationalOverrides": [
        "Current lifecycle/command role is defined in DEVICE_LIFECYCLE_PLAYTEST.md. Boundary and predicate replies supersede conflicting initial proposals. Full card effects are not certified.",
        "Shared owner command/damage ledgers, source-qualified life states, original expiry, slot footprint, protected-disable and destruction provenance apply only where the source role calls for them."
      ],
      "reviewEvidence": [
        "GPT_DEVICE_LIFECYCLE_FIRST_REVIEW.md",
        "GPT_DEVICE_LIFECYCLE_BOUNDARIES.md",
        "GPT_DEVICE_LIFECYCLE_PREDICATES.md"
      ],
      "openIssues": [
        "Exact implementation review pending; other effects and wider companion completeness remain outside this bounded role."
      ]
    },
    {
      "bindingId": "tinker.base.quick-fingers",
      "sourceKind": "class-card",
      "sourcePath": "data/public/class_playtests/tinker.json",
      "sourceId": "tinker.base.quick-fingers",
      "sourceSha256": "f5971b6b7ae9f754ee2f67caf99f4189305214c5c58a2bd5446bce35e0f72ae0",
      "candidateOrigin": "Lexical candidate inventory",
      "sourceProcedure": {
        "name": "Quick Fingers",
        "activation": "Bonus Action",
        "cost": "0",
        "rangeAndTarget": "One noncombat mechanism touched",
        "duration": "One manipulation",
        "frequency": "Once/turn",
        "effect": "Open unlocked latch, operate simple switch or retrieve a carried gadget. Does not activate damaging/healing devices, disarm a trap, reload every weapon or add another Bonus Action."
      },
      "status": "SOURCE-AUDITED / DRAFTABLE; exact implementation review pending",
      "classification": "EXCLUSION",
      "operationalOverrides": [
        "Current lifecycle/command role is defined in DEVICE_LIFECYCLE_PLAYTEST.md. Boundary and predicate replies supersede conflicting initial proposals. Full card effects are not certified.",
        "Shared owner command/damage ledgers, source-qualified life states, original expiry, slot footprint, protected-disable and destruction provenance apply only where the source role calls for them."
      ],
      "reviewEvidence": [
        "GPT_DEVICE_LIFECYCLE_FIRST_REVIEW.md",
        "GPT_DEVICE_LIFECYCLE_BOUNDARIES.md",
        "GPT_DEVICE_LIFECYCLE_PREDICATES.md"
      ],
      "openIssues": [
        "Exact implementation review pending; other effects and wider companion completeness remain outside this bounded role."
      ]
    },
    {
      "bindingId": "tinker.base.deploy-anacite-drone",
      "sourceKind": "class-card",
      "sourcePath": "data/public/class_playtests/tinker.json",
      "sourceId": "tinker.base.deploy-anacite-drone",
      "sourceSha256": "4cab6cd7930c7cf40df1b28e17efe1d360b1a92b470781ba3a020fd3491ce1aa",
      "candidateOrigin": "Lexical candidate inventory",
      "sourceProcedure": {
        "name": "Deploy Anacite Drone",
        "activation": "Action",
        "cost": "0 if functional; repairs as engine",
        "rangeAndTarget": "Your carried drone within 5 ft",
        "duration": "Until retracted/destroyed",
        "frequency": "One deployment per drone",
        "effect": "Drone is automatic class engine. Selecting this card instead upgrades deployment to Bonus Action and permits 5 ft free initial placement. No free attacks, repair or extra drone."
      },
      "status": "SOURCE-AUDITED / DRAFTABLE; exact implementation review pending",
      "classification": "DRONE_DEPLOY/RETRACT",
      "operationalOverrides": [
        "Current lifecycle/command role is defined in DEVICE_LIFECYCLE_PLAYTEST.md. Boundary and predicate replies supersede conflicting initial proposals. Full card effects are not certified.",
        "Shared owner command/damage ledgers, source-qualified life states, original expiry, slot footprint, protected-disable and destruction provenance apply only where the source role calls for them."
      ],
      "reviewEvidence": [
        "GPT_DEVICE_LIFECYCLE_FIRST_REVIEW.md",
        "GPT_DEVICE_LIFECYCLE_BOUNDARIES.md",
        "GPT_DEVICE_LIFECYCLE_PREDICATES.md"
      ],
      "openIssues": [
        "Exact implementation review pending; other effects and wider companion completeness remain outside this bounded role."
      ]
    },
    {
      "bindingId": "tinker.base.field-repair",
      "sourceKind": "class-card",
      "sourcePath": "data/public/class_playtests/tinker.json",
      "sourceId": "tinker.base.field-repair",
      "sourceSha256": "612a9f00b4e33a8bfc77c3f83ff1e1d839fa1237e8d20e65b703bea1431b6d7f",
      "candidateOrigin": "Lexical candidate inventory",
      "sourceProcedure": {
        "name": "Field Repair",
        "activation": "Action",
        "cost": "1 RP",
        "rangeAndTarget": "One construct/device touched",
        "duration": "Instant",
        "frequency": "Recharge 2",
        "effect": "Restore S d8+M HP, up to maximum, to functional damaged machine. Cannot revive destroyed objects, heal organic allies, reset duration or recharge limited uses. If the target is disabled by the Tinker’s protected Dissonance-routing feature, Field Repair also clears that disabled state. It does not reset duration, recharge, ammunition or per-rest uses."
      },
      "status": "SOURCE-AUDITED / DRAFTABLE; exact implementation review pending",
      "classification": "FUNCTIONAL_REPAIR/DISABLE_CLEAR",
      "operationalOverrides": [
        "Current lifecycle/command role is defined in DEVICE_LIFECYCLE_PLAYTEST.md. Boundary and predicate replies supersede conflicting initial proposals. Full card effects are not certified.",
        "Shared owner command/damage ledgers, source-qualified life states, original expiry, slot footprint, protected-disable and destruction provenance apply only where the source role calls for them."
      ],
      "reviewEvidence": [
        "GPT_DEVICE_LIFECYCLE_FIRST_REVIEW.md",
        "GPT_DEVICE_LIFECYCLE_BOUNDARIES.md",
        "GPT_DEVICE_LIFECYCLE_PREDICATES.md"
      ],
      "openIssues": [
        "Exact implementation review pending; other effects and wider companion completeness remain outside this bounded role."
      ]
    },
    {
      "bindingId": "tinker.base.analyze-weakness",
      "sourceKind": "class-card",
      "sourcePath": "data/public/class_playtests/tinker.json",
      "sourceId": "tinker.base.analyze-weakness",
      "sourceSha256": "0ae1995f4bba4c1503d9f5e8385d537a5b3f6b35f2e2bb11c3db0ce56935109c",
      "candidateOrigin": "Lexical candidate inventory",
      "sourceProcedure": {
        "name": "Analyze Weakness",
        "activation": "Bonus Action",
        "cost": "0",
        "rangeAndTarget": "Visible target within 60 ft",
        "duration": "Until end next turn",
        "frequency": "Recharge 3",
        "effect": "Identify one visibly demonstrated damage resistance. Your next bomb/device damage against it ignores 2 flat DR, not resistance/immunity. No invented weakness or automatic secret knowledge."
      },
      "status": "SOURCE-AUDITED / DRAFTABLE; exact implementation review pending",
      "classification": "DAMAGE_MOD",
      "operationalOverrides": [
        "Current lifecycle/command role is defined in DEVICE_LIFECYCLE_PLAYTEST.md. Boundary and predicate replies supersede conflicting initial proposals. Full card effects are not certified.",
        "Shared owner command/damage ledgers, source-qualified life states, original expiry, slot footprint, protected-disable and destruction provenance apply only where the source role calls for them."
      ],
      "reviewEvidence": [
        "GPT_DEVICE_LIFECYCLE_FIRST_REVIEW.md",
        "GPT_DEVICE_LIFECYCLE_BOUNDARIES.md",
        "GPT_DEVICE_LIFECYCLE_PREDICATES.md"
      ],
      "openIssues": [
        "Exact implementation review pending; other effects and wider companion completeness remain outside this bounded role."
      ]
    },
    {
      "bindingId": "tinker.base.jury-rig",
      "sourceKind": "class-card",
      "sourcePath": "data/public/class_playtests/tinker.json",
      "sourceId": "tinker.base.jury-rig",
      "sourceSha256": "ffbbe9b3e96242efb89dc141ed4d12e2e452d3919d2c6421ea8c5c18996659cf",
      "candidateOrigin": "Lexical candidate inventory",
      "sourceProcedure": {
        "name": "Jury-rig",
        "activation": "Action",
        "cost": "1 RP",
        "rangeAndTarget": "One willing ally weapon/device touched",
        "duration": "3 rounds",
        "frequency": "Recharge 3",
        "effect": "Choose+1 first attack roll/turn or+5 ft device movement. One modification per item, no stack. Does not change weapon category, spell function, summon limit or command budget."
      },
      "status": "SOURCE-AUDITED / DRAFTABLE; exact implementation review pending",
      "classification": "DEVICE_MOD",
      "operationalOverrides": [
        "Current lifecycle/command role is defined in DEVICE_LIFECYCLE_PLAYTEST.md. Boundary and predicate replies supersede conflicting initial proposals. Full card effects are not certified.",
        "Shared owner command/damage ledgers, source-qualified life states, original expiry, slot footprint, protected-disable and destruction provenance apply only where the source role calls for them."
      ],
      "reviewEvidence": [
        "GPT_DEVICE_LIFECYCLE_FIRST_REVIEW.md",
        "GPT_DEVICE_LIFECYCLE_BOUNDARIES.md",
        "GPT_DEVICE_LIFECYCLE_PREDICATES.md"
      ],
      "openIssues": [
        "Exact implementation review pending; other effects and wider companion completeness remain outside this bounded role."
      ]
    },
    {
      "bindingId": "tinker.arch.enhanced-drone-control",
      "sourceKind": "class-card",
      "sourcePath": "data/public/class_playtests/tinker.json",
      "sourceId": "tinker.arch.enhanced-drone-control",
      "sourceSha256": "49f2b89302f9a23883dc5235d782acb7191dc5f67a9a871f21f28cf3b831ae10",
      "candidateOrigin": "Lexical candidate inventory",
      "sourceProcedure": {
        "name": "Enhanced Drone Control",
        "activation": "Passive",
        "cost": "0",
        "rangeAndTarget": "Your drones",
        "duration": "While active",
        "frequency": "Continuous",
        "effect": "Gain+1 attack roll and can follow simple move/dodge commands while within 120 ft. Attacks still require your Bonus Action and line of effect; no independent turn."
      },
      "status": "SOURCE-AUDITED / DRAFTABLE; exact implementation review pending",
      "classification": "CMD_RANGE/MOD",
      "operationalOverrides": [
        "Current lifecycle/command role is defined in DEVICE_LIFECYCLE_PLAYTEST.md. Boundary and predicate replies supersede conflicting initial proposals. Full card effects are not certified.",
        "Shared owner command/damage ledgers, source-qualified life states, original expiry, slot footprint, protected-disable and destruction provenance apply only where the source role calls for them."
      ],
      "reviewEvidence": [
        "GPT_DEVICE_LIFECYCLE_FIRST_REVIEW.md",
        "GPT_DEVICE_LIFECYCLE_BOUNDARIES.md",
        "GPT_DEVICE_LIFECYCLE_PREDICATES.md"
      ],
      "openIssues": [
        "Exact implementation review pending; other effects and wider companion completeness remain outside this bounded role."
      ]
    },
    {
      "bindingId": "tinker.arch.pet-upgrade-slot",
      "sourceKind": "class-card",
      "sourcePath": "data/public/class_playtests/tinker.json",
      "sourceId": "tinker.arch.pet-upgrade-slot",
      "sourceSha256": "c9c6dce75dcb5b9a9ecf7cbc9d7c8b7c3b238e58a1404acedd16538c91151a82",
      "candidateOrigin": "Lexical candidate inventory",
      "sourceProcedure": {
        "name": "Pet Upgrade Slot",
        "activation": "Long rest choice",
        "cost": "0",
        "rangeAndTarget": "One drone module slot",
        "duration": "Until next reconfiguration",
        "frequency": "Automatic engine at 5",
        "effect": "Choose one of 9 bounded modules in engine. This automatic unlock is not a selected skill. At 13 use Dual Drone Protocols, still shared command budget."
      },
      "status": "SOURCE-AUDITED / DRAFTABLE; exact implementation review pending",
      "classification": "DRONE_CONFIGURATION",
      "operationalOverrides": [
        "Current lifecycle/command role is defined in DEVICE_LIFECYCLE_PLAYTEST.md. Boundary and predicate replies supersede conflicting initial proposals. Full card effects are not certified.",
        "Shared owner command/damage ledgers, source-qualified life states, original expiry, slot footprint, protected-disable and destruction provenance apply only where the source role calls for them."
      ],
      "reviewEvidence": [
        "GPT_DEVICE_LIFECYCLE_FIRST_REVIEW.md",
        "GPT_DEVICE_LIFECYCLE_BOUNDARIES.md",
        "GPT_DEVICE_LIFECYCLE_PREDICATES.md"
      ],
      "openIssues": [
        "Exact implementation review pending; other effects and wider companion completeness remain outside this bounded role."
      ]
    },
    {
      "bindingId": "tinker.arch.deployable-expertise",
      "sourceKind": "class-card",
      "sourcePath": "data/public/class_playtests/tinker.json",
      "sourceId": "tinker.arch.deployable-expertise",
      "sourceSha256": "4f63c35881564989abeaf3c37286af4f79c52d22f983f667d09ab22dcbf1ee58",
      "candidateOrigin": "Lexical candidate inventory",
      "sourceProcedure": {
        "name": "Deployable Expertise",
        "activation": "Passive",
        "cost": "0",
        "rangeAndTarget": "Your deployables",
        "duration": "While deployed",
        "frequency": "Continuous",
        "effect": "Gain M maximum/initial HP and+1 AC. Does not heal existing damage when moved or grant additional slots. Drones excluded unless another card says otherwise."
      },
      "status": "SOURCE-AUDITED / DRAFTABLE; exact implementation review pending",
      "classification": "MAX_HP/AC_MOD",
      "operationalOverrides": [
        "Current lifecycle/command role is defined in DEVICE_LIFECYCLE_PLAYTEST.md. Boundary and predicate replies supersede conflicting initial proposals. Full card effects are not certified.",
        "Shared owner command/damage ledgers, source-qualified life states, original expiry, slot footprint, protected-disable and destruction provenance apply only where the source role calls for them."
      ],
      "reviewEvidence": [
        "GPT_DEVICE_LIFECYCLE_FIRST_REVIEW.md",
        "GPT_DEVICE_LIFECYCLE_BOUNDARIES.md",
        "GPT_DEVICE_LIFECYCLE_PREDICATES.md"
      ],
      "openIssues": [
        "Exact implementation review pending; other effects and wider companion completeness remain outside this bounded role."
      ]
    },
    {
      "bindingId": "tinker.arch.remote-detonation",
      "sourceKind": "class-card",
      "sourcePath": "data/public/class_playtests/tinker.json",
      "sourceId": "tinker.arch.remote-detonation",
      "sourceSha256": "064953c7220b0c9cdb495093993946ddf911f41d0b24ca834999dbc1c4a3e7f1",
      "candidateOrigin": "Lexical candidate inventory",
      "sourceProcedure": {
        "name": "Remote Detonation",
        "activation": "Bonus Action",
        "cost": "1 RP; sacrifice one device",
        "rangeAndTarget": "Device within 60 ft, 10 ft radius up to 3 creatures",
        "duration": "Instant",
        "frequency": "Recharge 3",
        "effect": "Destroy your device; DEX save 2 S d6 force, half success. Failed save also no Reactions until end next turn. Cannot trigger Volatile Components/Scrap Reaper or another destruction/copy chain; no resource refund."
      },
      "status": "SOURCE-AUDITED / DRAFTABLE; exact implementation review pending",
      "classification": "SACRIFICE",
      "operationalOverrides": [
        "Current lifecycle/command role is defined in DEVICE_LIFECYCLE_PLAYTEST.md. Boundary and predicate replies supersede conflicting initial proposals. Full card effects are not certified.",
        "Shared owner command/damage ledgers, source-qualified life states, original expiry, slot footprint, protected-disable and destruction provenance apply only where the source role calls for them."
      ],
      "reviewEvidence": [
        "GPT_DEVICE_LIFECYCLE_FIRST_REVIEW.md",
        "GPT_DEVICE_LIFECYCLE_BOUNDARIES.md",
        "GPT_DEVICE_LIFECYCLE_PREDICATES.md"
      ],
      "openIssues": [
        "Exact implementation review pending; other effects and wider companion completeness remain outside this bounded role."
      ]
    },
    {
      "bindingId": "tinker.arch.deploy-sentry-turret",
      "sourceKind": "class-card",
      "sourcePath": "data/public/class_playtests/tinker.json",
      "sourceId": "tinker.arch.deploy-sentry-turret",
      "sourceSha256": "f062d05fde2b92c4fb4bd83c889ac75be59f72027bf58ff7dcd469dceee03c14",
      "candidateOrigin": "Lexical candidate inventory",
      "sourceProcedure": {
        "name": "Deploy Sentry Turret",
        "activation": "Action",
        "cost": "2 RP; one slot",
        "rangeAndTarget": "Empty ground within 15 ft",
        "duration": "3 rounds",
        "frequency": "Recharge 2",
        "effect": "Deploy Sentry engine profile: commanded attack range 25 ft PB+INT for 1d6 piercing. No auto fire, extra Bonus Action or shared budget exception. Durability AC 12+PB HP 2 L before upgrades."
      },
      "status": "SOURCE-AUDITED / DRAFTABLE; exact implementation review pending",
      "classification": "DEPLOYABLE",
      "operationalOverrides": [
        "Current lifecycle/command role is defined in DEVICE_LIFECYCLE_PLAYTEST.md. Boundary and predicate replies supersede conflicting initial proposals. Full card effects are not certified.",
        "Shared owner command/damage ledgers, source-qualified life states, original expiry, slot footprint, protected-disable and destruction provenance apply only where the source role calls for them."
      ],
      "reviewEvidence": [
        "GPT_DEVICE_LIFECYCLE_FIRST_REVIEW.md",
        "GPT_DEVICE_LIFECYCLE_BOUNDARIES.md",
        "GPT_DEVICE_LIFECYCLE_PREDICATES.md"
      ],
      "openIssues": [
        "Exact implementation review pending; other effects and wider companion completeness remain outside this bounded role."
      ]
    },
    {
      "bindingId": "tinker.arch.deploy-net-trap",
      "sourceKind": "class-card",
      "sourcePath": "data/public/class_playtests/tinker.json",
      "sourceId": "tinker.arch.deploy-net-trap",
      "sourceSha256": "441a83ffad99028dd74608c352ea1e03fc65b118d636fcf0f6c474d652c7d28a",
      "candidateOrigin": "Lexical candidate inventory",
      "sourceProcedure": {
        "name": "Deploy Net Trap",
        "activation": "Action",
        "cost": "2 RP; one slot",
        "rangeAndTarget": "One 5 ft square within 15 ft",
        "duration": "3 rounds or trigger",
        "frequency": "Recharge 2",
        "effect": "Deploy visible Net Trap. First enemy entry STR save or Restrained, repeat end turn or Action escape against DC. Target Huge+instead speed-10 ft. No damage or continued rearming; ends after one creature escapes."
      },
      "status": "SOURCE-AUDITED / DRAFTABLE; exact implementation review pending",
      "classification": "DEPLOYABLE/TRIGGER",
      "operationalOverrides": [
        "Current lifecycle/command role is defined in DEVICE_LIFECYCLE_PLAYTEST.md. Boundary and predicate replies supersede conflicting initial proposals. Full card effects are not certified.",
        "Shared owner command/damage ledgers, source-qualified life states, original expiry, slot footprint, protected-disable and destruction provenance apply only where the source role calls for them."
      ],
      "reviewEvidence": [
        "GPT_DEVICE_LIFECYCLE_FIRST_REVIEW.md",
        "GPT_DEVICE_LIFECYCLE_BOUNDARIES.md",
        "GPT_DEVICE_LIFECYCLE_PREDICATES.md"
      ],
      "openIssues": [
        "Exact implementation review pending; other effects and wider companion completeness remain outside this bounded role."
      ]
    },
    {
      "bindingId": "tinker.arch.overcharge",
      "sourceKind": "class-card",
      "sourcePath": "data/public/class_playtests/tinker.json",
      "sourceId": "tinker.arch.overcharge",
      "sourceSha256": "31a25f25fc9de809817bd0e24b84d4af770ff341f4a94db510df13964bc4c339",
      "candidateOrigin": "Lexical candidate inventory",
      "sourceProcedure": {
        "name": "Overcharge",
        "activation": "Bonus Action",
        "cost": "1 RP",
        "rangeAndTarget": "One device within 30 ft",
        "duration": "Until end next turn",
        "frequency": "Recharge 3",
        "effect": "Next damaging activation adds S d6 to one target. One pending overcharge, no stacking, does not command device or grant attack. If device expires first cost lost."
      },
      "status": "SOURCE-AUDITED / DRAFTABLE; exact implementation review pending",
      "classification": "PENDING_DAMAGE_MOD",
      "operationalOverrides": [
        "Current lifecycle/command role is defined in DEVICE_LIFECYCLE_PLAYTEST.md. Boundary and predicate replies supersede conflicting initial proposals. Full card effects are not certified.",
        "Shared owner command/damage ledgers, source-qualified life states, original expiry, slot footprint, protected-disable and destruction provenance apply only where the source role calls for them."
      ],
      "reviewEvidence": [
        "GPT_DEVICE_LIFECYCLE_FIRST_REVIEW.md",
        "GPT_DEVICE_LIFECYCLE_BOUNDARIES.md",
        "GPT_DEVICE_LIFECYCLE_PREDICATES.md"
      ],
      "openIssues": [
        "Exact implementation review pending; other effects and wider companion completeness remain outside this bounded role."
      ]
    },
    {
      "bindingId": "tinker.arch.recalibrate",
      "sourceKind": "class-card",
      "sourcePath": "data/public/class_playtests/tinker.json",
      "sourceId": "tinker.arch.recalibrate",
      "sourceSha256": "538b89c0ad6f430c91e03b8a16f9e20ac1fa5c88e7a94cf3a2f5f12cb78aa6ca",
      "candidateOrigin": "Lexical candidate inventory",
      "sourceProcedure": {
        "name": "Recalibrate",
        "activation": "Bonus Action",
        "cost": "0",
        "rangeAndTarget": "One drone; one visible enemy 60 ft",
        "duration": "Until end next turn",
        "frequency": "Recharge 2",
        "effect": "Drone's next attack against chosen enemy has advantage. Still needs separate command; no automatic shot, enemy type wide permanent buff or crit conversion."
      },
      "status": "SOURCE-AUDITED / DRAFTABLE; exact implementation review pending",
      "classification": "PENDING_ATTACK_MOD",
      "operationalOverrides": [
        "Current lifecycle/command role is defined in DEVICE_LIFECYCLE_PLAYTEST.md. Boundary and predicate replies supersede conflicting initial proposals. Full card effects are not certified.",
        "Shared owner command/damage ledgers, source-qualified life states, original expiry, slot footprint, protected-disable and destruction provenance apply only where the source role calls for them."
      ],
      "reviewEvidence": [
        "GPT_DEVICE_LIFECYCLE_FIRST_REVIEW.md",
        "GPT_DEVICE_LIFECYCLE_BOUNDARIES.md",
        "GPT_DEVICE_LIFECYCLE_PREDICATES.md"
      ],
      "openIssues": [
        "Exact implementation review pending; other effects and wider companion completeness remain outside this bounded role."
      ]
    },
    {
      "bindingId": "tinker.arch.emergency-protocols",
      "sourceKind": "class-card",
      "sourcePath": "data/public/class_playtests/tinker.json",
      "sourceId": "tinker.arch.emergency-protocols",
      "sourceSha256": "ac7d27cd219c8e7e7ee81ba88425c48850dbac9861ea85a06d715ab99ad905ff",
      "candidateOrigin": "Lexical candidate inventory",
      "sourceProcedure": {
        "name": "Emergency Protocols",
        "activation": "Reaction",
        "cost": "1 encounter use",
        "rangeAndTarget": "Drone within 10 ft when attack hits you",
        "duration": "One hit",
        "frequency": "1/encounter",
        "effect": "Drone intercepts: reduce damage to you by S+M and takes same amount unmitigated. It must be active/conscious. Does not redirect again or trigger retaliation loops."
      },
      "status": "SOURCE-AUDITED / DRAFTABLE; exact implementation review pending",
      "classification": "POST_DEFENSE_TRANSFER",
      "operationalOverrides": [
        "Current lifecycle/command role is defined in DEVICE_LIFECYCLE_PLAYTEST.md. Boundary and predicate replies supersede conflicting initial proposals. Full card effects are not certified.",
        "Shared owner command/damage ledgers, source-qualified life states, original expiry, slot footprint, protected-disable and destruction provenance apply only where the source role calls for them."
      ],
      "reviewEvidence": [
        "GPT_DEVICE_LIFECYCLE_FIRST_REVIEW.md",
        "GPT_DEVICE_LIFECYCLE_BOUNDARIES.md",
        "GPT_DEVICE_LIFECYCLE_PREDICATES.md"
      ],
      "openIssues": [
        "Exact implementation review pending; other effects and wider companion completeness remain outside this bounded role."
      ]
    },
    {
      "bindingId": "tinker.hero.artificer.protective-programming",
      "sourceKind": "class-card",
      "sourcePath": "data/public/class_playtests/tinker.json",
      "sourceId": "tinker.hero.artificer.protective-programming",
      "sourceSha256": "e76aac51eaced741048fcaefeed7ca204d63230910195d42fde9ebe7f59888d1",
      "candidateOrigin": "Lexical candidate inventory",
      "sourceProcedure": {
        "name": "Protective Programming",
        "activation": "Reaction",
        "cost": "1 RP",
        "rangeAndTarget": "Drone adjacent to ally hit by attack",
        "duration": "One hit",
        "frequency": "Once/round",
        "effect": "Drone grants ally S+M temporary HP before hit resolves. No heal or reversal of hit; max one protected ally, normal temporary HP nonstacking."
      },
      "status": "SOURCE-AUDITED / DRAFTABLE; exact implementation review pending",
      "classification": "DEFENSIVE_REACTION",
      "operationalOverrides": [
        "Current lifecycle/command role is defined in DEVICE_LIFECYCLE_PLAYTEST.md. Boundary and predicate replies supersede conflicting initial proposals. Full card effects are not certified.",
        "Shared owner command/damage ledgers, source-qualified life states, original expiry, slot footprint, protected-disable and destruction provenance apply only where the source role calls for them."
      ],
      "reviewEvidence": [
        "GPT_DEVICE_LIFECYCLE_FIRST_REVIEW.md",
        "GPT_DEVICE_LIFECYCLE_BOUNDARIES.md",
        "GPT_DEVICE_LIFECYCLE_PREDICATES.md"
      ],
      "openIssues": [
        "Exact implementation review pending; other effects and wider companion completeness remain outside this bounded role."
      ]
    },
    {
      "bindingId": "tinker.hero.artificer.efficient-power-cells",
      "sourceKind": "class-card",
      "sourcePath": "data/public/class_playtests/tinker.json",
      "sourceId": "tinker.hero.artificer.efficient-power-cells",
      "sourceSha256": "c9738585ed8fae504de1ec5a0603fbea55a31fbcc5c4711838d7c7a252736c44",
      "candidateOrigin": "Lexical candidate inventory",
      "sourceProcedure": {
        "name": "Efficient Power Cells",
        "activation": "Passive",
        "cost": "0",
        "rangeAndTarget": "Your nonhealing deployables",
        "duration": "Deployment",
        "frequency": "Continuous",
        "effect": "A 3 round device lasts 4 rounds (50%rounded down). Healing pulse count unchanged, no extra ammunition or free commands. Does not extend spell concentration."
      },
      "status": "SOURCE-AUDITED / DRAFTABLE; exact implementation review pending",
      "classification": "DURATION_MOD",
      "operationalOverrides": [
        "Current lifecycle/command role is defined in DEVICE_LIFECYCLE_PLAYTEST.md. Boundary and predicate replies supersede conflicting initial proposals. Full card effects are not certified.",
        "Shared owner command/damage ledgers, source-qualified life states, original expiry, slot footprint, protected-disable and destruction provenance apply only where the source role calls for them."
      ],
      "reviewEvidence": [
        "GPT_DEVICE_LIFECYCLE_FIRST_REVIEW.md",
        "GPT_DEVICE_LIFECYCLE_BOUNDARIES.md",
        "GPT_DEVICE_LIFECYCLE_PREDICATES.md"
      ],
      "openIssues": [
        "Exact implementation review pending; other effects and wider companion completeness remain outside this bounded role."
      ]
    },
    {
      "bindingId": "tinker.hero.artificer.nano-aegis-drone",
      "sourceKind": "class-card",
      "sourcePath": "data/public/class_playtests/tinker.json",
      "sourceId": "tinker.hero.artificer.nano-aegis-drone",
      "sourceSha256": "a3117289c319bbe6ef18ae9437975f46db8da26795fd3f271cb54b443b93ee01",
      "candidateOrigin": "Lexical candidate inventory",
      "sourceProcedure": {
        "name": "Nano-Aegis Drone",
        "activation": "Action",
        "cost": "2 RP",
        "rangeAndTarget": "Your drone within 15 ft",
        "duration": "3 rounds",
        "frequency": "Recharge 4",
        "effect": "Replace bolts with support mode. Each Bonus Action command pay 1 RP choose one ally 30 ft to heal S d6+M or grant 2 S+Mtemp HP. Maximum 3 pulses; organic healing explicit exception, no attack during mode."
      },
      "status": "SOURCE-AUDITED / DRAFTABLE; exact implementation review pending",
      "classification": "SUPPORT_COMMAND",
      "operationalOverrides": [
        "Current lifecycle/command role is defined in DEVICE_LIFECYCLE_PLAYTEST.md. Boundary and predicate replies supersede conflicting initial proposals. Full card effects are not certified.",
        "Shared owner command/damage ledgers, source-qualified life states, original expiry, slot footprint, protected-disable and destruction provenance apply only where the source role calls for them."
      ],
      "reviewEvidence": [
        "GPT_DEVICE_LIFECYCLE_FIRST_REVIEW.md",
        "GPT_DEVICE_LIFECYCLE_BOUNDARIES.md",
        "GPT_DEVICE_LIFECYCLE_PREDICATES.md"
      ],
      "openIssues": [
        "Exact implementation review pending; other effects and wider companion completeness remain outside this bounded role."
      ]
    },
    {
      "bindingId": "tinker.hero.artificer.repair-pulse",
      "sourceKind": "class-card",
      "sourcePath": "data/public/class_playtests/tinker.json",
      "sourceId": "tinker.hero.artificer.repair-pulse",
      "sourceSha256": "bfea8b20493f349c4de02c639c7acb4842d61e734d7798ddad412422bfb81593",
      "candidateOrigin": "Lexical candidate inventory",
      "sourceProcedure": {
        "name": "Repair Pulse",
        "activation": "Action",
        "cost": "3 RP",
        "rangeAndTarget": "Upto 3 friendly devices within 30 ft",
        "duration": "Instant; AC until start next turn",
        "frequency": "1/short rest",
        "effect": "Restore each half its maximum HP rounded down and+1 AC. Functional devices only; no construct resurrection, organic HP, resource or use resets."
      },
      "status": "SOURCE-AUDITED / DRAFTABLE; exact implementation review pending",
      "classification": "FUNCTIONAL_DEVICE_REPAIR",
      "operationalOverrides": [
        "Current lifecycle/command role is defined in DEVICE_LIFECYCLE_PLAYTEST.md. Boundary and predicate replies supersede conflicting initial proposals. Full card effects are not certified.",
        "Shared owner command/damage ledgers, source-qualified life states, original expiry, slot footprint, protected-disable and destruction provenance apply only where the source role calls for them."
      ],
      "reviewEvidence": [
        "GPT_DEVICE_LIFECYCLE_FIRST_REVIEW.md",
        "GPT_DEVICE_LIFECYCLE_BOUNDARIES.md",
        "GPT_DEVICE_LIFECYCLE_PREDICATES.md"
      ],
      "openIssues": [
        "Exact implementation review pending; other effects and wider companion completeness remain outside this bounded role."
      ]
    },
    {
      "bindingId": "tinker.hero.artificer.restoration-field",
      "sourceKind": "class-card",
      "sourcePath": "data/public/class_playtests/tinker.json",
      "sourceId": "tinker.hero.artificer.restoration-field",
      "sourceSha256": "a791259766db2192f9effe98f8946304ee8ef85d4ff243faa87c04665bf96ffa",
      "candidateOrigin": "Lexical candidate inventory",
      "sourceProcedure": {
        "name": "Restoration Field",
        "activation": "Action",
        "cost": "3 RP start; 1 RP maintenance; one slot",
        "rangeAndTarget": "10 ft radius within 30 ft",
        "duration": "Maximum 3 pulses",
        "frequency": "Recharge 4",
        "effect": "Concentration. Initial and paid Bonus Action pulse heals up to 3 living allies/devices S d6 HP. Devices must not be destroyed. Same creature once/round, no extra autonomous healing or longer Efficient Cells."
      },
      "status": "SOURCE-AUDITED / DRAFTABLE; exact implementation review pending",
      "classification": "SLOT_EFFECT/HEALING_ZONE; no physical anchor",
      "operationalOverrides": [
        "Current lifecycle/command role is defined in DEVICE_LIFECYCLE_PLAYTEST.md. Boundary and predicate replies supersede conflicting initial proposals. Full card effects are not certified.",
        "Shared owner command/damage ledgers, source-qualified life states, original expiry, slot footprint, protected-disable and destruction provenance apply only where the source role calls for them.",
        "No imported object HP/AC, machine targeting, disable routing, reconstruction or debris."
      ],
      "reviewEvidence": [
        "GPT_DEVICE_LIFECYCLE_FIRST_REVIEW.md",
        "GPT_DEVICE_LIFECYCLE_BOUNDARIES.md",
        "GPT_DEVICE_LIFECYCLE_PREDICATES.md"
      ],
      "openIssues": [
        "Exact implementation review pending; other effects and wider companion completeness remain outside this bounded role."
      ]
    },
    {
      "bindingId": "tinker.hero.artificer.overload-suppression",
      "sourceKind": "class-card",
      "sourcePath": "data/public/class_playtests/tinker.json",
      "sourceId": "tinker.hero.artificer.overload-suppression",
      "sourceSha256": "ed1f05201b49d5737cf112f42770553d20cbeb035e6cbb947cd0ddb407be7d22",
      "candidateOrigin": "Lexical candidate inventory",
      "sourceProcedure": {
        "name": "Overload Suppression",
        "activation": "Action",
        "cost": "3 RP",
        "rangeAndTarget": "One enemy construct/device within 30 ft",
        "duration": "Until end next target turn",
        "frequency": "1/short rest",
        "effect": "CON save or fails its next Reaction and has disadvantage on attacks. On failure by 5 also Stunned, shared hard-denial guard. No automatic permanent deactivation, hacking allegiance or ignoring boss immunity."
      },
      "status": "SOURCE-AUDITED / DRAFTABLE; exact implementation review pending",
      "classification": "ENEMY_DEVICE_CONTROL",
      "operationalOverrides": [
        "Current lifecycle/command role is defined in DEVICE_LIFECYCLE_PLAYTEST.md. Boundary and predicate replies supersede conflicting initial proposals. Full card effects are not certified.",
        "Shared owner command/damage ledgers, source-qualified life states, original expiry, slot footprint, protected-disable and destruction provenance apply only where the source role calls for them."
      ],
      "reviewEvidence": [
        "GPT_DEVICE_LIFECYCLE_FIRST_REVIEW.md",
        "GPT_DEVICE_LIFECYCLE_BOUNDARIES.md",
        "GPT_DEVICE_LIFECYCLE_PREDICATES.md"
      ],
      "openIssues": [
        "Exact implementation review pending; other effects and wider companion completeness remain outside this bounded role."
      ]
    },
    {
      "bindingId": "tinker.hero.techsmith.automated-field-kit",
      "sourceKind": "class-card",
      "sourcePath": "data/public/class_playtests/tinker.json",
      "sourceId": "tinker.hero.techsmith.automated-field-kit",
      "sourceSha256": "1476c580f48bc38fc72776460853c72ab1455b2a24fab7ae38d105ac1103a8b5",
      "candidateOrigin": "Lexical candidate inventory",
      "sourceProcedure": {
        "name": "Automated Field Kit",
        "activation": "Passive",
        "cost": "0",
        "rangeAndTarget": "Self",
        "duration": "While known",
        "frequency": "Continuous",
        "effect": "Bomb stock cap/refill+1; encounter allowance unchanged. Reduce deployable card recharge by 1 minimum 1, on setting counter only. Never refresh rest uses or trigger repeated counter reductions."
      },
      "status": "SOURCE-AUDITED / DRAFTABLE; exact implementation review pending",
      "classification": "RECHARGE/STOCK_MOD",
      "operationalOverrides": [
        "Current lifecycle/command role is defined in DEVICE_LIFECYCLE_PLAYTEST.md. Boundary and predicate replies supersede conflicting initial proposals. Full card effects are not certified.",
        "Shared owner command/damage ledgers, source-qualified life states, original expiry, slot footprint, protected-disable and destruction provenance apply only where the source role calls for them."
      ],
      "reviewEvidence": [
        "GPT_DEVICE_LIFECYCLE_FIRST_REVIEW.md",
        "GPT_DEVICE_LIFECYCLE_BOUNDARIES.md",
        "GPT_DEVICE_LIFECYCLE_PREDICATES.md"
      ],
      "openIssues": [
        "Exact implementation review pending; other effects and wider companion completeness remain outside this bounded role."
      ]
    },
    {
      "bindingId": "tinker.hero.techsmith.enhanced-targeting",
      "sourceKind": "class-card",
      "sourcePath": "data/public/class_playtests/tinker.json",
      "sourceId": "tinker.hero.techsmith.enhanced-targeting",
      "sourceSha256": "39eb03fb7bf030235829e1fd532d165194bdf0e7981e05c64b96db0ab84e471a",
      "candidateOrigin": "Lexical candidate inventory",
      "sourceProcedure": {
        "name": "Enhanced Targeting",
        "activation": "Passive",
        "cost": "0",
        "rangeAndTarget": "Your turret attacks",
        "duration": "While active",
        "frequency": "Continuous",
        "effect": "Gain+1 to hit. Does not stack with Enhanced Drone Control if profile ever counts both, and does not impose save penalties."
      },
      "status": "SOURCE-AUDITED / DRAFTABLE; exact implementation review pending",
      "classification": "ATTACK_MOD",
      "operationalOverrides": [
        "Current lifecycle/command role is defined in DEVICE_LIFECYCLE_PLAYTEST.md. Boundary and predicate replies supersede conflicting initial proposals. Full card effects are not certified.",
        "Shared owner command/damage ledgers, source-qualified life states, original expiry, slot footprint, protected-disable and destruction provenance apply only where the source role calls for them."
      ],
      "reviewEvidence": [
        "GPT_DEVICE_LIFECYCLE_FIRST_REVIEW.md",
        "GPT_DEVICE_LIFECYCLE_BOUNDARIES.md",
        "GPT_DEVICE_LIFECYCLE_PREDICATES.md"
      ],
      "openIssues": [
        "Exact implementation review pending; other effects and wider companion completeness remain outside this bounded role."
      ]
    },
    {
      "bindingId": "tinker.hero.techsmith.efficient-recycling",
      "sourceKind": "class-card",
      "sourcePath": "data/public/class_playtests/tinker.json",
      "sourceId": "tinker.hero.techsmith.efficient-recycling",
      "sourceSha256": "22bd682461f3d9b31bf30da64cff23c86d4af3a3d5b19426da23ea7bb0e2009c",
      "candidateOrigin": "Lexical candidate inventory",
      "sourceProcedure": {
        "name": "Efficient Recycling",
        "activation": "Triggered",
        "cost": "One destroyed device remains",
        "rangeAndTarget": "Your destroyed device within reach",
        "duration": "After combat 1 minute",
        "frequency": "1/short rest",
        "effect": "Recover 1 RP spent on deploying it, never more than its actual paid cost. Deliberate sacrifice or copy does not qualify. Consume usable debris; no repeated salvage from same object."
      },
      "status": "SOURCE-AUDITED / DRAFTABLE; exact implementation review pending",
      "classification": "DEBRIS_CONSUMER/REFUND",
      "operationalOverrides": [
        "Current lifecycle/command role is defined in DEVICE_LIFECYCLE_PLAYTEST.md. Boundary and predicate replies supersede conflicting initial proposals. Full card effects are not certified.",
        "Shared owner command/damage ledgers, source-qualified life states, original expiry, slot footprint, protected-disable and destruction provenance apply only where the source role calls for them.",
        "Enemy destruction is not required; friendly/accidental qualifies if not deliberate sacrifice/copy and noResourceGeneration absent."
      ],
      "reviewEvidence": [
        "GPT_DEVICE_LIFECYCLE_FIRST_REVIEW.md",
        "GPT_DEVICE_LIFECYCLE_BOUNDARIES.md",
        "GPT_DEVICE_LIFECYCLE_PREDICATES.md"
      ],
      "openIssues": [
        "Exact implementation review pending; other effects and wider companion completeness remain outside this bounded role."
      ]
    },
    {
      "bindingId": "tinker.hero.techsmith.technical-mastery",
      "sourceKind": "class-card",
      "sourcePath": "data/public/class_playtests/tinker.json",
      "sourceId": "tinker.hero.techsmith.technical-mastery",
      "sourceSha256": "3a4d62af52179da3430c9fa28c1ea84dfbb27f435dc8eb81ef9764e8d157eca1",
      "candidateOrigin": "Lexical candidate inventory",
      "sourceProcedure": {
        "name": "Technical Mastery",
        "activation": "Triggered",
        "cost": "1 RP",
        "rangeAndTarget": "Your damaging device activation",
        "duration": "One target",
        "frequency": "Once/own turn",
        "effect": "After damage rolld 10; on 10 you may pay 1 RP to add half its unmodified damage dice total rounded down to one target. No second activation, commands, procs, resources or healing duplication."
      },
      "status": "SOURCE-AUDITED / DRAFTABLE; exact implementation review pending",
      "classification": "DAMAGE_COPY",
      "operationalOverrides": [
        "Current lifecycle/command role is defined in DEVICE_LIFECYCLE_PLAYTEST.md. Boundary and predicate replies supersede conflicting initial proposals. Full card effects are not certified.",
        "Shared owner command/damage ledgers, source-qualified life states, original expiry, slot footprint, protected-disable and destruction provenance apply only where the source role calls for them."
      ],
      "reviewEvidence": [
        "GPT_DEVICE_LIFECYCLE_FIRST_REVIEW.md",
        "GPT_DEVICE_LIFECYCLE_BOUNDARIES.md",
        "GPT_DEVICE_LIFECYCLE_PREDICATES.md"
      ],
      "openIssues": [
        "Exact implementation review pending; other effects and wider companion completeness remain outside this bounded role."
      ]
    },
    {
      "bindingId": "tinker.hero.techsmith.advanced-turret-bay",
      "sourceKind": "class-card",
      "sourcePath": "data/public/class_playtests/tinker.json",
      "sourceId": "tinker.hero.techsmith.advanced-turret-bay",
      "sourceSha256": "be608930afc67316f33a22f98076bd16c77acb0bf5b87d8278743ef4da7b5a86",
      "candidateOrigin": "Lexical candidate inventory",
      "sourceProcedure": {
        "name": "Advanced Turret Bay",
        "activation": "Action",
        "cost": "4 RP; two slots",
        "rangeAndTarget": "Two empty ground spaces within 15 ft",
        "duration": "3 rounds",
        "frequency": "Recharge 4",
        "effect": "Requires 2 available slots (normally 13); if only one, deploy one for 2 RP. Sniper command attack 90 ft S d6 piercing; Burst command DEX save S d4 piercing to 2 targets within 5 ftat 30 ft. One commanded turret per Bonus Action, not both automatically."
      },
      "status": "SOURCE-AUDITED / DRAFTABLE; exact implementation review pending",
      "classification": "MULTI_DEPLOYABLE",
      "operationalOverrides": [
        "Current lifecycle/command role is defined in DEVICE_LIFECYCLE_PLAYTEST.md. Boundary and predicate replies supersede conflicting initial proposals. Full card effects are not certified.",
        "Shared owner command/damage ledgers, source-qualified life states, original expiry, slot footprint, protected-disable and destruction provenance apply only where the source role calls for them."
      ],
      "reviewEvidence": [
        "GPT_DEVICE_LIFECYCLE_FIRST_REVIEW.md",
        "GPT_DEVICE_LIFECYCLE_BOUNDARIES.md",
        "GPT_DEVICE_LIFECYCLE_PREDICATES.md"
      ],
      "openIssues": [
        "Exact implementation review pending; other effects and wider companion completeness remain outside this bounded role."
      ]
    },
    {
      "bindingId": "tinker.hero.techsmith.gadget-sync-protocol",
      "sourceKind": "class-card",
      "sourcePath": "data/public/class_playtests/tinker.json",
      "sourceId": "tinker.hero.techsmith.gadget-sync-protocol",
      "sourceSha256": "4faccb7a8c195b8d598bc99c1639b1c1c021fd69a95f3f082f8305e9f80ea3c5",
      "candidateOrigin": "Lexical candidate inventory",
      "sourceProcedure": {
        "name": "Gadget Sync Protocol",
        "activation": "Triggered",
        "cost": "1 RP",
        "rangeAndTarget": "One turret within 60 ft after your bomb throw",
        "duration": "One attack",
        "frequency": "Once/own turn",
        "effect": "Turret makes one ordinary shot at surviving bomb target. Replaces its normal commanded damaging action for that turn; cannot combine with another device attack from Bonus Action. No chains or additional bombs."
      },
      "status": "SOURCE-AUDITED / DRAFTABLE; exact implementation review pending",
      "classification": "TRIGGERED_DEVICE_ATTACK",
      "operationalOverrides": [
        "Current lifecycle/command role is defined in DEVICE_LIFECYCLE_PLAYTEST.md. Boundary and predicate replies supersede conflicting initial proposals. Full card effects are not certified.",
        "Shared owner command/damage ledgers, source-qualified life states, original expiry, slot footprint, protected-disable and destruction provenance apply only where the source role calls for them."
      ],
      "reviewEvidence": [
        "GPT_DEVICE_LIFECYCLE_FIRST_REVIEW.md",
        "GPT_DEVICE_LIFECYCLE_BOUNDARIES.md",
        "GPT_DEVICE_LIFECYCLE_PREDICATES.md"
      ],
      "openIssues": [
        "Exact implementation review pending; other effects and wider companion completeness remain outside this bounded role."
      ]
    },
    {
      "bindingId": "tinker.hero.techsmith.snap-rebuild",
      "sourceKind": "class-card",
      "sourcePath": "data/public/class_playtests/tinker.json",
      "sourceId": "tinker.hero.techsmith.snap-rebuild",
      "sourceSha256": "0a8d445d6a86fd84b5dc4587562eb1eab093cd81ae114f10be850ad8f512cd11",
      "candidateOrigin": "Lexical candidate inventory",
      "sourceProcedure": {
        "name": "Snap Rebuild",
        "activation": "Bonus Action",
        "cost": "2 RP; 1 encounter use",
        "rangeAndTarget": "One destroyed device/drone within 15 ft",
        "duration": "Remaining original duration",
        "frequency": "1/encounter",
        "effect": "Restore half its maximum HP. Uses original slot and original expiry; expired devices ineligible. Does not reset limited uses, modules, Overdrive, destruction triggers or bomb stock."
      },
      "status": "SOURCE-AUDITED / DRAFTABLE; exact implementation review pending",
      "classification": "DESTROYED_RECONSTRUCTION",
      "operationalOverrides": [
        "Current lifecycle/command role is defined in DEVICE_LIFECYCLE_PLAYTEST.md. Boundary and predicate replies supersede conflicting initial proposals. Full card effects are not certified.",
        "Shared owner command/damage ledgers, source-qualified life states, original expiry, slot footprint, protected-disable and destruction provenance apply only where the source role calls for them."
      ],
      "reviewEvidence": [
        "GPT_DEVICE_LIFECYCLE_FIRST_REVIEW.md",
        "GPT_DEVICE_LIFECYCLE_BOUNDARIES.md",
        "GPT_DEVICE_LIFECYCLE_PREDICATES.md"
      ],
      "openIssues": [
        "Exact implementation review pending; other effects and wider companion completeness remain outside this bounded role."
      ]
    },
    {
      "bindingId": "tinker.hero.techsmith.reconfiguration",
      "sourceKind": "class-card",
      "sourcePath": "data/public/class_playtests/tinker.json",
      "sourceId": "tinker.hero.techsmith.reconfiguration",
      "sourceSha256": "b002ce1fcf72933c9ee498d43d32bcc0f93e2476240fa85d4715ca7deae0ff74",
      "candidateOrigin": "Lexical candidate inventory",
      "sourceProcedure": {
        "name": "Reconfiguration",
        "activation": "Action",
        "cost": "1 RP",
        "rangeAndTarget": "One deployed device within 15 ft",
        "duration": "Remaining duration",
        "frequency": "Recharge 3",
        "effect": "Change between known nonhealing profiles using same HP fraction, slot, expiry and spent uses. Cannot turn a 1 slot device into two, refill ammo, reset trap, create fresh death trigger or morph drone into free bomb."
      },
      "status": "SOURCE-AUDITED / DRAFTABLE; exact implementation review pending",
      "classification": "PROFILE_CHANGE",
      "operationalOverrides": [
        "Current lifecycle/command role is defined in DEVICE_LIFECYCLE_PLAYTEST.md. Boundary and predicate replies supersede conflicting initial proposals. Full card effects are not certified.",
        "Shared owner command/damage ledgers, source-qualified life states, original expiry, slot footprint, protected-disable and destruction provenance apply only where the source role calls for them."
      ],
      "reviewEvidence": [
        "GPT_DEVICE_LIFECYCLE_FIRST_REVIEW.md",
        "GPT_DEVICE_LIFECYCLE_BOUNDARIES.md",
        "GPT_DEVICE_LIFECYCLE_PREDICATES.md"
      ],
      "openIssues": [
        "Exact implementation review pending; other effects and wider companion completeness remain outside this bounded role."
      ]
    },
    {
      "bindingId": "tinker.hero.warmachine.malfunction-field",
      "sourceKind": "class-card",
      "sourcePath": "data/public/class_playtests/tinker.json",
      "sourceId": "tinker.hero.warmachine.malfunction-field",
      "sourceSha256": "940d686ea7fd142c68776c809029c5d2df478293ba2899f969932970eebca10d",
      "candidateOrigin": "Lexical candidate inventory",
      "sourceProcedure": {
        "name": "Malfunction Field",
        "activation": "Passive",
        "cost": "0",
        "rangeAndTarget": "Enemy within 5 ft of your device",
        "duration": "While device active",
        "frequency": "Once/round total",
        "effect": "First spell attack by one enemy has disadvantage. Multiple devices do not multiply effect; area/spell-saves unchanged. Does not create antimagic zone."
      },
      "status": "SOURCE-AUDITED / DRAFTABLE; exact implementation review pending",
      "classification": "PASSIVE_DEVICE_AURA",
      "operationalOverrides": [
        "Current lifecycle/command role is defined in DEVICE_LIFECYCLE_PLAYTEST.md. Boundary and predicate replies supersede conflicting initial proposals. Full card effects are not certified.",
        "Shared owner command/damage ledgers, source-qualified life states, original expiry, slot footprint, protected-disable and destruction provenance apply only where the source role calls for them."
      ],
      "reviewEvidence": [
        "GPT_DEVICE_LIFECYCLE_FIRST_REVIEW.md",
        "GPT_DEVICE_LIFECYCLE_BOUNDARIES.md",
        "GPT_DEVICE_LIFECYCLE_PREDICATES.md"
      ],
      "openIssues": [
        "Exact implementation review pending; other effects and wider companion completeness remain outside this bounded role."
      ]
    },
    {
      "bindingId": "tinker.hero.warmachine.volatile-components",
      "sourceKind": "class-card",
      "sourcePath": "data/public/class_playtests/tinker.json",
      "sourceId": "tinker.hero.warmachine.volatile-components",
      "sourceSha256": "05634b00666a14dfccefe6f95b99a382f386e6a7ed7c044c31a011477753bc37",
      "candidateOrigin": "Lexical candidate inventory",
      "sourceProcedure": {
        "name": "Volatile Components",
        "activation": "Triggered",
        "cost": "0",
        "rangeAndTarget": "One device destroyed by enemy; one enemy within 5 ft",
        "duration": "Instant",
        "frequency": "Once/round",
        "effect": "Deal S fire to that enemy. Deliberate sacrifices, copied objects, friendly damage and secondary explosions cannot trigger. No other procs/resources from damage."
      },
      "status": "SOURCE-AUDITED / DRAFTABLE; exact implementation review pending",
      "classification": "HOSTILE_DESTRUCTION_TRIGGER",
      "operationalOverrides": [
        "Current lifecycle/command role is defined in DEVICE_LIFECYCLE_PLAYTEST.md. Boundary and predicate replies supersede conflicting initial proposals. Full card effects are not certified.",
        "Shared owner command/damage ledgers, source-qualified life states, original expiry, slot footprint, protected-disable and destruction provenance apply only where the source role calls for them."
      ],
      "reviewEvidence": [
        "GPT_DEVICE_LIFECYCLE_FIRST_REVIEW.md",
        "GPT_DEVICE_LIFECYCLE_BOUNDARIES.md",
        "GPT_DEVICE_LIFECYCLE_PREDICATES.md"
      ],
      "openIssues": [
        "Exact implementation review pending; other effects and wider companion completeness remain outside this bounded role."
      ]
    },
    {
      "bindingId": "tinker.hero.warmachine.scrap-salvage",
      "sourceKind": "class-card",
      "sourcePath": "data/public/class_playtests/tinker.json",
      "sourceId": "tinker.hero.warmachine.scrap-salvage",
      "sourceSha256": "5e43e97602bbba6b5807b0bb63f56064083e8acc7c24926eca21e7579aa4a521",
      "candidateOrigin": "Lexical candidate inventory",
      "sourceProcedure": {
        "name": "Scrap Salvage",
        "activation": "Action",
        "cost": "1 RP; enemy-destroyed device debris",
        "rangeAndTarget": "Empty space within 5 ft of debris",
        "duration": "3 rounds",
        "frequency": "1/encounter",
        "effect": "Create one Scrapling AC 12 HP L Speed 20 ft, commanded melee attack PB+INT for 1d6 bludgeoning. Counts as deployable slot/shared command. Consumed debris cannot be salvaged again; cannot spawn its own replacement."
      },
      "status": "SOURCE-AUDITED / DRAFTABLE; exact implementation review pending",
      "classification": "DEBRIS_CONSUMER/COMPANION",
      "operationalOverrides": [
        "Current lifecycle/command role is defined in DEVICE_LIFECYCLE_PLAYTEST.md. Boundary and predicate replies supersede conflicting initial proposals. Full card effects are not certified.",
        "Shared owner command/damage ledgers, source-qualified life states, original expiry, slot footprint, protected-disable and destruction provenance apply only where the source role calls for them."
      ],
      "reviewEvidence": [
        "GPT_DEVICE_LIFECYCLE_FIRST_REVIEW.md",
        "GPT_DEVICE_LIFECYCLE_BOUNDARIES.md",
        "GPT_DEVICE_LIFECYCLE_PREDICATES.md"
      ],
      "openIssues": [
        "Exact implementation review pending; other effects and wider companion completeness remain outside this bounded role."
      ]
    },
    {
      "bindingId": "tinker.hero.warmachine.boomcore-drone",
      "sourceKind": "class-card",
      "sourcePath": "data/public/class_playtests/tinker.json",
      "sourceId": "tinker.hero.warmachine.boomcore-drone",
      "sourceSha256": "3ad4684e03c3b3a02bb2204eab11082be1c7d7f92f04ec65261299f97fb3571b",
      "candidateOrigin": "Lexical candidate inventory",
      "sourceProcedure": {
        "name": "Boomcore Drone",
        "activation": "Bonus Action",
        "cost": "2 RP",
        "rangeAndTarget": "One drone within 30 ft",
        "duration": "3 rounds",
        "frequency": "Recharge 4",
        "effect": "Commanded bolts add 1d6 fire and on hit STR save or push 5 ft. Still one command and normal attack budget; no free activation attack or unlimited stacking."
      },
      "status": "SOURCE-AUDITED / DRAFTABLE; exact implementation review pending",
      "classification": "DRONE_ATTACK_MOD",
      "operationalOverrides": [
        "Current lifecycle/command role is defined in DEVICE_LIFECYCLE_PLAYTEST.md. Boundary and predicate replies supersede conflicting initial proposals. Full card effects are not certified.",
        "Shared owner command/damage ledgers, source-qualified life states, original expiry, slot footprint, protected-disable and destruction provenance apply only where the source role calls for them."
      ],
      "reviewEvidence": [
        "GPT_DEVICE_LIFECYCLE_FIRST_REVIEW.md",
        "GPT_DEVICE_LIFECYCLE_BOUNDARIES.md",
        "GPT_DEVICE_LIFECYCLE_PREDICATES.md"
      ],
      "openIssues": [
        "Exact implementation review pending; other effects and wider companion completeness remain outside this bounded role."
      ]
    },
    {
      "bindingId": "tinker.hero.warmachine.scrap-reaper",
      "sourceKind": "class-card",
      "sourcePath": "data/public/class_playtests/tinker.json",
      "sourceId": "tinker.hero.warmachine.scrap-reaper",
      "sourceSha256": "136ff6f663a889e441bd405548be1d826807ab93ee75e55500487ccd6c9f0e55",
      "candidateOrigin": "Lexical candidate inventory",
      "sourceProcedure": {
        "name": "Scrap Reaper",
        "activation": "Reaction",
        "cost": "2 RP; one destroyed enemy-hit device",
        "rangeAndTarget": "Debris within 30 ft",
        "duration": "Until end next turn",
        "frequency": "1/short rest",
        "effect": "Create one Scrapling Speed 30, AC 12 HP L; next Bonus Action command moves and detonates within 5 ft one enemy for 2 S d6 fire DEX half. Uses one command budget and ends. No chain from deliberate sacrifice or its own death."
      },
      "status": "SOURCE-AUDITED / DRAFTABLE; exact implementation review pending",
      "classification": "DEBRIS_CONSUMER/TEMP_COMPANION",
      "operationalOverrides": [
        "Current lifecycle/command role is defined in DEVICE_LIFECYCLE_PLAYTEST.md. Boundary and predicate replies supersede conflicting initial proposals. Full card effects are not certified.",
        "Shared owner command/damage ledgers, source-qualified life states, original expiry, slot footprint, protected-disable and destruction provenance apply only where the source role calls for them.",
        "No invented deployable-slot requirement; shared command still applies; exact enemy-hit predicate retained."
      ],
      "reviewEvidence": [
        "GPT_DEVICE_LIFECYCLE_FIRST_REVIEW.md",
        "GPT_DEVICE_LIFECYCLE_BOUNDARIES.md",
        "GPT_DEVICE_LIFECYCLE_PREDICATES.md"
      ],
      "openIssues": [
        "Exact implementation review pending; other effects and wider companion completeness remain outside this bounded role."
      ]
    },
    {
      "bindingId": "tinker.hero.warmachine.volatile-injection",
      "sourceKind": "class-card",
      "sourcePath": "data/public/class_playtests/tinker.json",
      "sourceId": "tinker.hero.warmachine.volatile-injection",
      "sourceSha256": "f9cd77012a09b377a8aeb76487cc0a19a0276773e5d8567507ecf6f681913f7d",
      "candidateOrigin": "Lexical candidate inventory",
      "sourceProcedure": {
        "name": "Volatile Injection",
        "activation": "Bonus Action",
        "cost": "1 RP; device loses MHP",
        "rangeAndTarget": "One functional device within 30 ft",
        "duration": "Until end next turn",
        "frequency": "Recharge 3",
        "effect": "Must have strictly more HP than cost. Its next damaging activation adds S d6 to one target; cannot combine with Overcharge, damage cannot be refunded by same activation. No resources gained from self damage."
      },
      "status": "SOURCE-AUDITED / DRAFTABLE; exact implementation review pending",
      "classification": "DIRECT_DEVICE_HP_COST",
      "operationalOverrides": [
        "Current lifecycle/command role is defined in DEVICE_LIFECYCLE_PLAYTEST.md. Boundary and predicate replies supersede conflicting initial proposals. Full card effects are not certified.",
        "Shared owner command/damage ledgers, source-qualified life states, original expiry, slot footprint, protected-disable and destruction provenance apply only where the source role calls for them."
      ],
      "reviewEvidence": [
        "GPT_DEVICE_LIFECYCLE_FIRST_REVIEW.md",
        "GPT_DEVICE_LIFECYCLE_BOUNDARIES.md",
        "GPT_DEVICE_LIFECYCLE_PREDICATES.md"
      ],
      "openIssues": [
        "Exact implementation review pending; other effects and wider companion completeness remain outside this bounded role."
      ]
    },
    {
      "bindingId": "tinker.hero.warmachine.catastrophic-overload",
      "sourceKind": "class-card",
      "sourcePath": "data/public/class_playtests/tinker.json",
      "sourceId": "tinker.hero.warmachine.catastrophic-overload",
      "sourceSha256": "6b3fe321c4ef6257dc8315fb1e5345989a7cb874e95503b5179701b82abbee24",
      "candidateOrigin": "Lexical candidate inventory",
      "sourceProcedure": {
        "name": "Catastrophic Overload",
        "activation": "Action",
        "cost": "4 RP; sacrifice one device",
        "rangeAndTarget": "10 ft radius about device within 60 ft",
        "duration": "Instant",
        "frequency": "1/long rest",
        "effect": "All creatures including allies DEX save, 3 S d6 fire plus 3 S d6 force on failure, half success. No critical hit, additional destruction proc, salvage, automatic stun or copied damage. Device ends before blast; no Safety exclusion."
      },
      "status": "SOURCE-AUDITED / DRAFTABLE; exact implementation review pending",
      "classification": "SACRIFICE",
      "operationalOverrides": [
        "Current lifecycle/command role is defined in DEVICE_LIFECYCLE_PLAYTEST.md. Boundary and predicate replies supersede conflicting initial proposals. Full card effects are not certified.",
        "Shared owner command/damage ledgers, source-qualified life states, original expiry, slot footprint, protected-disable and destruction provenance apply only where the source role calls for them."
      ],
      "reviewEvidence": [
        "GPT_DEVICE_LIFECYCLE_FIRST_REVIEW.md",
        "GPT_DEVICE_LIFECYCLE_BOUNDARIES.md",
        "GPT_DEVICE_LIFECYCLE_PREDICATES.md"
      ],
      "openIssues": [
        "Exact implementation review pending; other effects and wider companion completeness remain outside this bounded role."
      ]
    },
    {
      "bindingId": "tinker.supplement.mech-overdrive",
      "sourceKind": "class-card",
      "sourcePath": "data/public/class_playtests/tinker.json",
      "sourceId": "tinker.supplement.mech-overdrive",
      "sourceSha256": "0a3d5549a68c395cdfa364bac06f334436af7ac848ca5fed71a0a9bc141aec73",
      "candidateOrigin": "Lexical candidate inventory",
      "sourceProcedure": {
        "name": "Mech Overdrive",
        "activation": "Triggered on deploying a device",
        "cost": "1 long-rest use plus original deployment cost",
        "rangeAndTarget": "One of your newly deployed devices",
        "duration": "Until encounter end, maximum 1 minute",
        "frequency": "1/long rest; automatic Hero capstone",
        "effect": "Source-derived level 20 feature: extend device duration only. It still occupies its slot, requires normal commands and payments, and is destructible. Healing devices keep maximum 3 pulses; bombs, spent uses and expended charges never refill. Does not create permanent equipment."
      },
      "status": "SOURCE-AUDITED / DRAFTABLE; exact implementation review pending",
      "classification": "DURATION_MOD",
      "operationalOverrides": [
        "Current lifecycle/command role is defined in DEVICE_LIFECYCLE_PLAYTEST.md. Boundary and predicate replies supersede conflicting initial proposals. Full card effects are not certified.",
        "Shared owner command/damage ledgers, source-qualified life states, original expiry, slot footprint, protected-disable and destruction provenance apply only where the source role calls for them."
      ],
      "reviewEvidence": [
        "GPT_DEVICE_LIFECYCLE_FIRST_REVIEW.md",
        "GPT_DEVICE_LIFECYCLE_BOUNDARIES.md",
        "GPT_DEVICE_LIFECYCLE_PREDICATES.md"
      ],
      "openIssues": [
        "Exact implementation review pending; other effects and wider companion completeness remain outside this bounded role."
      ]
    },
    {
      "bindingId": "tinker.hero.artificer.magnetic-wall",
      "sourceKind": "class-card",
      "sourcePath": "data/public/class_playtests/tinker.json",
      "sourceId": "tinker.hero.artificer.magnetic-wall",
      "sourceSha256": "b4c888d3665e64fad8aaaa616790d651ecd1f36f68907d2ce52449cedbbd5beb",
      "candidateOrigin": "Semantic supplement: operational wall interception text lacks lexical device/deploy/redirect terms.",
      "sourceProcedure": {
        "name": "Magnetic Wall",
        "activation": "Action",
        "cost": "3 RP; one slot",
        "rangeAndTarget": "10-by 5 ft wall within 15 ft",
        "duration": "3 rounds",
        "frequency": "Recharge 4",
        "effect": "AC 12+PB HP 2 L, blocks LOS/movement. Reaction when ranged weapon hit ally within 5 ft of wall reduce its damage by S+M and wall takes reduction amount. Requires line between attack and wall; no automatic all-shot absorption."
      },
      "status": "SOURCE-AUDITED / DRAFTABLE; exact implementation review pending",
      "classification": "DEPLOYABLE/INTERCEPTION",
      "operationalOverrides": [
        "Current lifecycle/command role is defined in DEVICE_LIFECYCLE_PLAYTEST.md. Boundary and predicate replies supersede conflicting initial proposals. Full card effects are not certified.",
        "Shared owner command/damage ledgers, source-qualified life states, original expiry, slot footprint, protected-disable and destruction provenance apply only where the source role calls for them."
      ],
      "reviewEvidence": [
        "GPT_DEVICE_LIFECYCLE_FIRST_REVIEW.md",
        "GPT_DEVICE_LIFECYCLE_BOUNDARIES.md",
        "GPT_DEVICE_LIFECYCLE_PREDICATES.md"
      ],
      "openIssues": [
        "Exact implementation review pending; other effects and wider companion completeness remain outside this bounded role."
      ]
    }
  ]
}

## Source inventory supporting records

{
  "status": "UNREVIEWED_SOURCE_CANDIDATES",
  "scope": "73 lexical Tinker/Shaman passages plus MagneticWall semantic supplement:74 exact passages;3 frozen shared-rule paragraphs. Other157 future lifecycle candidates stay separate.",
  "supportingSources": [
    {
      "sourcePath": "docs/mechanics/CLASS_PLAYTEST_RULES.md",
      "paragraphPrefix": "Where a class card calls for a",
      "text": "Where a class card calls for a **standard companion** without a more specific profile, use: Small or Medium; AC 12+floor(PB/2); HP 2 L; walking Speed 30 ft; saves equal owner's PB; one melee or ranged attack (reach 5 ft/range 30 ft) at owner's class attack bonus, damage S d6 of the printed type. It has no independent class features, resources, loot, death triggers or extra turns. All companions belonging to one character share one Bonus Action command and **one damaging attack/action total per round** unless a specifically priced feature grants more. Without a command they move and Dodge. Act immediately after owner. A standard companion lasts 1 minute, disappears at 0 HP and cannot be healed for free by dismissing/resummoning. The creation cost must be paid again. Creature-specific stat blocks override this profile only where explicitly printed.",
      "fullFileSha256": "adb2f4752b45dc70ce792a675bb30dda362aab5056588061bcde3ba31c4c8a81"
    },
    {
      "sourcePath": "docs/mechanics/CLASS_PLAYTEST_RULES.md",
      "paragraphPrefix": "One regular Action,",
      "text": "One regular Action, one Bonus Action if a feature permits it, normal movement and one Reaction between starts of your turns. A free trigger costs no Action only if expressly stated. All grants share **one extra full Action per creature per round**. An extra Action cannot grant another Action, recharge itself, or start another extra-Action grant. It supplies no extra Bonus Action or Reaction. A card granting additional attacks is not permission to repeat all class riders on every hit: obey each rider's frequency.",
      "fullFileSha256": "adb2f4752b45dc70ce792a675bb30dda362aab5056588061bcde3ba31c4c8a81"
    },
    {
      "sourcePath": "docs/mechanics/CLASS_PLAYTEST_RULES.md",
      "paragraphPrefix": "No damage/healing copy",
      "text": "No damage/healing copy repeats the source's costs, procs, resource generation, critical bonus dice, buffs, actions, cooldown resets or duration. Compute fractions once, capped at 100% of one stored source unless an explicit card states a separately priced higher amount. Copies still cause ordinary damage consequences, concentration checks and death. A copy cannot copy another copy. A target/source record must refer to an actual resolved event, not merely a known ability name.",
      "fullFileSha256": "adb2f4752b45dc70ce792a675bb30dda362aab5056588061bcde3ba31c4c8a81"
    }
  ]
}

## Magnetic Wall new profile added alongside original redirection profiles

"""Reviewed bounded39-source damage sharing plus2 supporting Tinker engines.

Callers establish ownership, actions/costs, target legality, range, willingness,
active effects, printed cadence and damage type. One root is ONE original
recipient packet, not an entire multi-target cast. Each area recipient gets a
separate root under its shared cast/roll identity. No full combat scheduler.
"""
from dataclasses import dataclass,field,replace
from core_playtest_rules import attack_roll
from spell_playtest_rules import integer,SpellRuleError
from healing_playtest_rules import survival_damage_event
from control_playtest_rules import clock_marker,require_deadline

P='paladin.supplement.'
CROWN=P+'oath-of-the-martyr-king.crown-undying'
FINAL=P+'oath-of-the-chain.final-stand'
BURDEN=P+'oath-of-the-martyr-king.burden-shared'
PALADIN_BASE=frozenset({'noSecondMitigation','noRetransfer','noReflection','noResourceGeneration'})
POST=frozenset({'noSecondMitigation','noRetransfer'})

@dataclass(frozen=True)
class TransferProfile:
    phase: str
    formula: str
    flags: frozenset
    blocked_resources: frozenset=frozenset()
    automatic: bool=False
    max_recipients: int=1

PROFILES={
 'crimson-agent.hero.bloodweaver.bloodbond':TransferProfile('raw','quarter',frozenset({'noRetransfer'})),
 'crimson-agent.hero.bloodweaver.veinlock-tether':TransferProfile('raw','scale-mod',frozenset({'noRetransfer'})),
 'monk.hero.enlightened-master.shared-breath':TransferProfile('defended','scale-mod',POST),
 'oracle.supplement.life.life-linked':TransferProfile('defended','half-chosen',POST|frozenset({
     'noReflection','noResourceGeneration','noPassiveTriggers','noConditionTriggers',
     'noActionGeneration','noCopyGeneration','noRecoveryGeneration','noRetaliation'})),
 'paladin.base.protective-stance':TransferProfile('defended','scale-mod-fixed',PALADIN_BASE|{'noDamageTriggers'}),
 P+'oath-of-the-chain.chainbound-smite':TransferProfile('defended','cha-min3',PALADIN_BASE),
 P+'oath-of-the-chain.linked-ward':TransferProfile('defended','twice-cha-min2',PALADIN_BASE),
 P+'oath-of-the-chain.martyr-s-share':TransferProfile('defended','half',PALADIN_BASE),
 FINAL:TransferProfile('defended','all',PALADIN_BASE,automatic=True),
 P+'oath-of-the-martyr-king.king-s-smite':TransferProfile('defended','five',PALADIN_BASE),
 P+'oath-of-the-martyr-king.aura-of-the-crown':TransferProfile('defended','mod',PALADIN_BASE),
 P+'oath-of-the-martyr-king.crown-of-embers':TransferProfile('defended','level-mod',PALADIN_BASE),
 BURDEN:TransferProfile('defended','level-mod',PALADIN_BASE|{'noHealingGeneration'},max_recipients=2),
 CROWN:TransferProfile('defended','level-mod',PALADIN_BASE),
 'soldier.hero.champion.selfless-guardian':TransferProfile('defended','scale-mod',POST|{'noRetaliation'}),
 'tinker.arch.emergency-protocols':TransferProfile('defended','scale-mod-fixed',POST|{'noRetaliation'}),
 # Separately source-audited lifecycle supplement; not part of the original39.
 'tinker.hero.artificer.magnetic-wall':TransferProfile('defended','scale-mod-fixed',POST),
 'warrior.hero.wardborn.guardian-tissue':TransferProfile('defended','third',POST,frozenset({'BT'})),
 'warrior.hero.wardborn.aegis-incarnate':TransferProfile('defended','half',POST,frozenset({'BT'}),automatic=True),
}

def identity(value):
    if not isinstance(value,str) or not value:raise SpellRuleError('Nonempty identity required')
    return value

def transfer_limit(source,available,*,scale=1,modifier=1,level=1,charisma=0):
    """Maximum; fixed fractions/all/fixed reductions require exactly this amount."""
    if source not in PROFILES:raise SpellRuleError('Source is not a supplied damage transfer')
    integer(available,'available damage',0);integer(scale,'S',1,4)
    integer(modifier,'M',1);integer(level,'level',1,20);integer(charisma,'actual CHA modifier',-10,20)
    f=PROFILES[source].formula
    caps={'quarter':available//4,'third':available//3,'half':available//2,
          'half-chosen':available//2,'all':available,'scale-mod':scale+modifier,
          'scale-mod-fixed':scale+modifier,'level-mod':level+modifier,
          'cha-min3':max(3,charisma),'twice-cha-min2':max(2,2*charisma),'five':5,'mod':modifier}
    return min(available,caps[f])

@dataclass(frozen=True)
class Branch:
    branch_id: str
    target: str
    amount: int
    stage: str='raw'
    transferred: bool=False
    attack_hit: bool=False
    critical: bool=False
    failed_save: bool=False
    melee_attack: bool=False
    flags: frozenset=frozenset()
    blocked_resources: frozenset=frozenset()
    prevention_ids: frozenset=frozenset()

@dataclass
class PaladinRoundLedger:
    owner: str
    round_number: int
    events: dict=field(default_factory=dict)
    crown_heal_used: dict=field(default_factory=dict)
    settled_heals: set=field(default_factory=set)

    def __post_init__(self):
        identity(self.owner);integer(self.round_number,'numbered round',1)

    def validate(self,root_id,source,amount,*,crown_active,level,modifier):
        identity(root_id);integer(amount,'positive transferred amount',1)
        if source not in PROFILES or not source.startswith('paladin.'):
            raise SpellRuleError('Paladin ledger accepts only supplied Paladin transfer sources')
        integer(level,'Paladin level',1,20);integer(modifier,'M',1)
        if root_id in self.events:raise SpellRuleError('This owner already redirected that damage root')
        if len(self.events)>= (2 if crown_active else 1):
            raise SpellRuleError('Shared Paladin round allowance exhausted')
        if source==CROWN:
            if not crown_active:raise SpellRuleError('Crown is not active')
            spent=sum(x['amount'] for x in self.events.values() if x['source']==CROWN)
            if spent+amount>level+modifier:raise SpellRuleError('Crown round transferred amount exhausted')
        elif any(x['source']!=CROWN for x in self.events.values()):
            raise SpellRuleError('Only one ordinary Paladin redirection per round')

    def record(self,root_id,source,amount,ally,**options):
        self.validate(root_id,source,amount,**options)
        self.events[root_id]={'source':source,'amount':amount,'ally':identity(ally)}

    def crown_heal(self,root_id,actual_damage,*,scale,modifier):
        """Commit nominal source entitlement BEFORE target healing restrictions.

        Blocked healing spends the nominal cap. A duplicate settlement is an
        error, not another heal. Caller applies ordinary pipeline and explicit
        no-copy/no-redirection-chain flags to this source-native result.
        """
        integer(actual_damage,'final Paladin branch actual damage',0)
        integer(scale,'S',1,4);integer(modifier,'M',1)
        entry=self.events.get(root_id)
        if not entry or entry['source']!=CROWN:raise SpellRuleError('Not a Crown event')
        if root_id in self.settled_heals:raise SpellRuleError('Crown event already settled')
        if actual_damage>entry['amount']:raise SpellRuleError('Numeric damage exceeds transferred amount')
        ally=entry['ally'];used=self.crown_heal_used.get(ally,0)
        amount=min(actual_damage//2,max(0,scale+modifier-used))
        self.crown_heal_used[ally]=used+amount;self.settled_heals.add(root_id)
        return amount

class DamageRoot:
    def __init__(self,root_id,target,amount,damage_type,*,attack_hit=False,critical=False,
                 failed_save=False,melee_attack=False,inherited_flags=frozenset(),blocked_resources=frozenset()):
        self.root_id=identity(root_id);identity(target);identity(damage_type)
        integer(amount,'finalized attack/save/critical raw damage',0)
        if critical and not attack_hit:raise SpellRuleError('Critical requires an actual attack hit')
        if melee_attack and not attack_hit:raise SpellRuleError('Melee damage requires an actual hit')
        self.damage_type=damage_type;self.rolled_packet=amount
        self.original_id=root_id+'/original'
        self.branches={self.original_id:Branch(self.original_id,target,amount,
            attack_hit=attack_hit,critical=critical,failed_save=failed_save,melee_attack=melee_attack,
            flags=frozenset(inherited_flags),blocked_resources=frozenset(blocked_resources))}
        self.operation=None;self.resolved={}

    def branch(self,branch_id):
        if branch_id not in self.branches:raise SpellRuleError('Unknown branch')
        return self.branches[branch_id]

    def pending(self,branch_id):
        b=self.branch(branch_id)
        if branch_id in self.resolved:raise SpellRuleError('Branch already resolved')
        return b

    def defend(self,branch_id,*,flat_reductions=(),resistant=False,immune=False):
        b=self.pending(branch_id)
        if b.stage!='raw':raise SpellRuleError('Ordinary defenses apply once to a raw branch')
        for v in flat_reductions:integer(v,'flat class reduction',0)
        value=max(0,b.amount-max(flat_reductions,default=0))
        value=0 if immune else value//2 if resistant else value
        self.branches[branch_id]=replace(b,amount=value,stage='defended')
        return value

    def prevent(self,branch_id,amount,application_id):
        b=self.pending(branch_id);integer(amount,'eligible prevention amount',0);identity(application_id)
        if b.stage!='defended' or 'noSecondMitigation' in b.flags:
            raise SpellRuleError('Prevention requires a legally reducible defended branch')
        if application_id in b.prevention_ids:raise SpellRuleError('One prevention application per branch')
        stopped=min(amount,b.amount)
        self.branches[branch_id]=replace(b,amount=b.amount-stopped,
            prevention_ids=b.prevention_ids|{application_id})
        return stopped

    def transfer(self,source,owner,allocations,*,scale=1,modifier=1,level=1,charisma=0,
                 paladin_ledger=None,crown_active=False):
        """One selected legal operation. Entire validation precedes mutation.

        allocations maps DISTINCT willing legal recipients to positive amounts.
        Caller selects mandatory offers before optional offers AT THE SAME stage.
        Raw-stage offers precede post-defense offers; no defense/pool preview.
        Zero automatic shares simply produce no operation; optional0 is illegal.
        """
        identity(owner)
        if source not in PROFILES:raise SpellRuleError('Not a supplied damage-transfer source')
        p=PROFILES[source];b=self.pending(self.original_id)
        if self.operation:raise SpellRuleError('One transfer operation per original-recipient root')
        if b.stage!=p.phase:raise SpellRuleError('Transfer at wrong defense stage')
        cap=transfer_limit(source,b.amount,scale=scale,modifier=modifier,level=level,charisma=charisma)
        if not allocations:
            if p.automatic and cap==0:return None
            raise SpellRuleError('Optional transfer requires a positive amount')
        if len(allocations)>p.max_recipients:raise SpellRuleError('Too many transferred recipients')
        for target,amount in allocations.items():
            identity(target);integer(amount,'recipient transfer',1)
            if target==b.target:raise SpellRuleError('Cannot transfer to original damage target')
        total=sum(allocations.values())
        if total>cap:raise SpellRuleError('Transfer exceeds available/source amount')
        if p.formula in ('quarter','third','half','all','scale-mod-fixed') and total!=cap:
            raise SpellRuleError('Printed fixed amount cannot be arbitrarily lowered')
        is_paladin=source.startswith('paladin.')
        if is_paladin:
            if paladin_ledger is None or paladin_ledger.owner!=owner:
                raise SpellRuleError('Use the source owner Paladin round ledger')
            paladin_ledger.validate(self.root_id,source,total,crown_active=crown_active,level=level,modifier=modifier)
        stage='raw' if p.phase=='raw' else 'sealed'
        children={self.root_id+'/transfer/'+str(i):Branch(self.root_id+'/transfer/'+str(i),
            target,amount,stage=stage,transferred=True,flags=b.flags|p.flags,
            blocked_resources=b.blocked_resources|p.blocked_resources)
            for i,(target,amount) in enumerate(allocations.items(),1)}
        # No operation below this point can fail validation.
        if is_paladin:
            paladin_ledger.record(self.root_id,source,total,b.target,crown_active=crown_active,level=level,modifier=modifier)
        self.branches[self.original_id]=replace(b,amount=b.amount-total,stage=stage)
        self.branches.update(children)
        self.operation={'source':source,'owner':owner,'amount':total,'recipientBranchIds':tuple(children)}
        return self.operation

    def resolve_living(self,branch_id,state,**life_options):
        b=self.pending(branch_id)
        if b.stage not in ('defended','sealed'):raise SpellRuleError('Resolve defenses before life state')
        if 'critical' in life_options:raise SpellRuleError('Critical identity is owned by damage branch')
        if b.transferred and any(life_options.get(k) for k in ('maiming','knockout','melee')):
            raise SpellRuleError('Original attack riders do not accompany transferred damage')
        after,event=survival_damage_event(state,b.amount,critical=b.critical,**life_options)
        event={**event,'rootDamageEventId':self.root_id,'branchId':branch_id,'targetId':b.target,
               'damageType':self.damage_type,'attackHit':b.attack_hit,'criticalHit':b.critical,
               'failedOriginalSave':b.failed_save,'transferred':b.transferred,
               'concentrationDamage':b.amount,'flags':sorted(b.flags)}
        self.resolved[branch_id]=event
        return after,event

    def resolve_device(self,branch_id,state):
        b=self.pending(branch_id)
        if b.stage not in ('defended','sealed'):raise SpellRuleError('Resolve defenses before device state')
        after,event=device_damage(state,b.amount)
        event={**event,'rootDamageEventId':self.root_id,'branchId':branch_id,'targetId':b.target,
               'damageType':self.damage_type,'attackHit':b.attack_hit,'criticalHit':b.critical,
               'failedOriginalSave':b.failed_save,'transferred':b.transferred,'flags':sorted(b.flags)}
        self.resolved[branch_id]=event
        return after,event

    def total(self,consumer='physical',*,resource=None,qualified_targets=None):
        """Caller still verifies initiating-source and target-specific predicates."""
        if set(self.resolved)!=set(self.branches):raise SpellRuleError('All terminal branches must resolve first')
        return sum(event['actualDamageDealt'] for bid,event in self.resolved.items()
                   if (qualified_targets is None or self.branches[bid].target in qualified_targets)
                   and permits_consumer(self.branches[bid],consumer,resource=resource))

def permits_consumer(branch,consumer,*,resource=None):
    flags=branch.flags
    if consumer=='physical':return True
    kinds={'damage','healing','recovery','resource','retaliation','reflection','passive','condition','action','copy','attack-hit','free-attack'}
    if consumer not in kinds:raise SpellRuleError('Unknown damage consumer')
    if 'noDamageTriggers' in flags:return False
    if consumer=='attack-hit':return branch.attack_hit
    if consumer=='resource':
        identity(resource)
        if 'noResourceGeneration' in flags or resource in branch.blocked_resources:return False
    mapping={'healing':{'noHealingGeneration','noRecoveryGeneration'},
             'recovery':{'noRecoveryGeneration'},'reflection':{'noReflection','noRetaliation'},
             'retaliation':{'noRetaliation'},'passive':{'noPassiveTriggers'},
             'condition':{'noConditionTriggers'},'action':{'noActionGeneration'},
             'copy':{'noCopyGeneration'},'free-attack':{'noFreeAttackGeneration'}}
    return not (flags & mapping.get(consumer,set()))

@dataclass(frozen=True)
class DeviceState:
    maximum_hp: int
    hp: int
    temp_hp: int=0
    destroyed: bool=False
    disabled: bool=False
    def __post_init__(self):
        integer(self.maximum_hp,'device maximum HP',1);integer(self.hp,'device HP',0,self.maximum_hp)
        integer(self.temp_hp,'legally granted device tempHP',0)
        if self.destroyed!=(self.hp==0):raise SpellRuleError('A0HP device is destroyed')

def device_damage(state,amount):
    """Tinker device damage only; no organic Wounds/death saves or repair rights."""
    integer(amount,'device resolved damage',0)
    if state.destroyed:raise SpellRuleError('Already destroyed device is not a functional damage recipient')
    absorbed=min(state.temp_hp,amount);loss=min(state.hp,amount-absorbed);hp=state.hp-loss
    return replace(state,hp=hp,temp_hp=state.temp_hp-absorbed,destroyed=hp==0),{
        'resolvedDamage':amount,'positiveDamageEvent':amount>0,'tempAbsorbed':absorbed,
        'actualHpDamage':loss,'actualDamageDealt':absorbed+loss,'destroyedNow':hp==0,
        'woundSaves':0,'deathFailuresAdded':0}

@dataclass
class BloomPool:
    application_id: str
    target: str
    remaining: int
    expires: object
    ended: bool=False
    rider_deadline: object=None
    def __post_init__(self):
        identity(self.application_id);identity(self.target);integer(self.remaining,'Bloom capacity',1)
        require_deadline(self.expires)

    def end(self,now,*,target_next_end):
        now=clock_marker(now);require_deadline(target_next_end)
        if target_next_end<=now:raise SpellRuleError('Ending rider needs a future target-next-end')
        if self.ended:return False
        self.ended=True;self.rider_deadline=target_next_end
        return True

    def absorb(self,root,branch_id,now,*,target_next_end,suppressed=False):
        b=root.pending(branch_id);now=clock_marker(now);require_deadline(target_next_end)
        if b.target!=self.target:raise SpellRuleError('Bloom belongs to a different recipient')
        if self.ended:return 0
        if now>=self.expires:
            # Caller supplies the target end AFTER actual expiry, not late polling.
            self.end(self.expires,target_next_end=target_next_end);return 0
        if target_next_end<=now:raise SpellRuleError('Ending rider needs a future target-next-end')
        if suppressed:return 0
        # prevent validates before either root/pool mutates.
        prevented=root.prevent(branch_id,self.remaining,self.application_id)
        self.remaining-=prevented
        if self.remaining==0:self.end(now,target_next_end=target_next_end)
        return prevented

@dataclass
class AttackRetarget:
    attack_id: str
    intended_target: str
    current_target: str=None
    retargeted: bool=False
    resolved: bool=False
    counter_used: bool=False
    def __post_init__(self):
        identity(self.attack_id);identity(self.intended_target)
        self.current_target=self.intended_target
    def retarget(self,guardian):
        identity(guardian)
        if self.resolved or self.retargeted:raise SpellRuleError('Attack can retarget only once before hit resolution')
        if guardian==self.current_target:raise SpellRuleError('Retarget requires a different creature')
        self.current_target=guardian;self.retargeted=True
    def resolve(self,natural,modifier,armor_class,critical_threshold=20):
        if self.resolved:raise SpellRuleError('Original attack roll resolves once')
        result=attack_roll(natural,modifier,armor_class,critical_threshold)
        self.resolved=True
        return {**result,'targetId':self.current_target,'attackId':self.attack_id}

    def guardian_counter(self,*,triggering_attack_fully_resolved,in_reach,actor_can_attack,
                         parent_flags=frozenset()):
        """Single free counter after full damage/rider resolution, on hit OR miss.

        False eligibility consumes this response opportunity, not a new attack.
        Caller attaches returned flags to the NEW counterattack and its damage.
        """
        if not self.retargeted or not self.resolved or not triggering_attack_fully_resolved:
            raise SpellRuleError('Guardian counter waits for its retargeted attack to finish')
        if self.counter_used:raise SpellRuleError('Guardian counter opportunity already settled')
        self.counter_used=True
        if not in_reach or not actor_can_attack or 'noFreeAttackGeneration' in parent_flags:return None
        # This NEW attack inherits no unrelated resource/healing/reflection bans.
        return frozenset({'noFreeAttackGeneration','noActionGeneration'})

def redirecting_palm(root,branch_id,monk_level,attacker_id,*,second_enemy_id=None,new_root_id=None):
    """Caller owns Reaction/Ki/range. Distinct second enemy required for counter."""
    b=root.pending(branch_id);integer(monk_level,'Monk level',1,20);identity(attacker_id)
    if not b.attack_hit or not b.melee_attack or b.amount<=0:raise SpellRuleError('Palm requires positive melee-hit damage')
    if second_enemy_id is not None:
        identity(second_enemy_id);identity(new_root_id)
        if second_enemy_id in (b.target,attacker_id):raise SpellRuleError('Palm needs a distinct second enemy')
        if new_root_id==root.root_id:raise SpellRuleError('Counter is a NEW root')
    prevented=root.prevent(branch_id,b.amount//2,'monk.arch.tortoise.redirecting-palm')
    if not prevented or second_enemy_id is None:return None
    return DamageRoot(new_root_id,second_enemy_id,min(prevented,monk_level),'force')

def native_transfer_temp_hp(root,branch_id,*,source,scale,modifier,level,reduced_to_zero=False):
    """Caller establishes actual rider ownership, bond and zero-crossing predicate."""
    integer(scale,'S',1,4);integer(modifier,'M',1);integer(level,'level',1,20)
    if not root.operation or branch_id not in root.operation['recipientBranchIds'] or branch_id not in root.resolved:
        raise SpellRuleError('Rider requires a completed transferred branch')
    if root.branch(branch_id).target!=root.operation['owner']:
        raise SpellRuleError('These riders require damage absorbed by the redirecting owner')
    value=root.resolved[branch_id]['actualDamageDealt']
    if source==P+'oath-of-the-chain.unbroken-covenant':return min(value//2,scale+modifier)
    if source==P+'oath-of-the-chain.linked-ward':
        if root.operation['source']!=source:raise SpellRuleError('Linked Ward rider belongs to its own transfer')
        return min(value,level+modifier) if reduced_to_zero else 0
    if source==FINAL:
        if root.operation['source']!=source:raise SpellRuleError('Final Stand rider belongs to its own transfer')
        return level if reduced_to_zero else 0
    raise SpellRuleError('No supplied native transfer tempHP rider')

