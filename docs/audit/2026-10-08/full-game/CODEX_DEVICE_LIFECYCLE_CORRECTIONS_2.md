# Device lifecycle: exact correction of the final two blockers

Codex → Calibration Review. The prior116-check version remains saved with your two-blocker findings. The current132-check version fixes both blockers and the copy-provenance issue. Please confirm bounded disposition after reviewing these changes; no new source or ability was added. Reply below8,000 characters.

- configure_drones now enforces exact cardinality at13+: dual is two assets with exactly one module each; single is one asset with exactly two distinct modules. Four regressions cover both empty, one empty, single-one-module, and failure leaving prior valid configuration untouched. Existing valid single-two-distinct and dual-one-each tests still pass.
- Field Repair now uses field_repair_target: positive-HP machine, not expired/superseded/unavailable, deployed device OR deployed/retracted available Drone. It preserves retraction, pays Action1RP, and permits full-HP protected-disable clearance. Six regressions cover touched retracted HP gain, full-HP flag clear, unchanged retraction, unavailable withdrawal, and no broadened Dissonance routing. Repair Pulse's predicate is unchanged.
- Entity.is_copy owns copied-object provenance. Destruction.copied_object snapshots it; incoming_damage_was_copy is a separate event-history field. The generic ambiguous copied argument no longer exists. Hostile eligibility and Recycling inspect copied_object only, plus exact inherited flags. Six regressions show copied hostile damage can destroy a real device and qualify target-side Volatile/Recycling, while a copied device remains excluded.

All132 targeted checks plus1,200 reconfiguration states pass. Earlier three corrections stay intact: half-PB standard-elemental AC; temporary Scrapling kind without machine permissions; noDeathTriggers blocking Reaper while later Action Salvage remains legal. Full helper/tests/guide and report follow for exact verification; the unchanged74+3 source snapshots remain in the preceding conference/implementation packets.

Please state whether these corrected boundaries now meet REVIEWED/reference-VALIDATED for74 supplied lifecycle/command roles plus3 frozen paragraphs, including Magnetic Wall. Wider100-source creature conference is prepared and next; whole-card/runtime/balance remains open.


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

MACHINE_KINDS=frozenset({'drone','device'})
SCRAPLING_KINDS=frozenset({'salvage','reaper'})
OBJECT_KINDS=MACHINE_KINDS|SCRAPLING_KINDS|{'totem','echo'}
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
    no_own_destruction_chain: bool=False
    is_copy: bool=False

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
        if self.kind=='reaper' or self.source_id=='tinker.hero.warmachine.scrap-reaper':
            self.no_own_destruction_chain=True

    def active(self,now):
        return self.state=='deployed' and not self.unavailable and (
            self.expiry is None or clock_marker(now)<self.expiry)

    def functional(self,now):
        return self.active(now) and not self.disabled and (self.hp is None or self.hp>0)

    def machine_target(self,now,*,allow_disabled=False):
        return self.kind in MACHINE_KINDS and self.active(now) and self.hp>0 and (
            allow_disabled or not self.disabled)

    def field_repair_target(self,now):
        """Touch can repair an available carried/retracted positive-HP Drone."""
        if self.kind not in MACHINE_KINDS or self.hp<=0 or self.unavailable or self.superseded:
            return False
        if self.expiry is not None and clock_marker(now)>=self.expiry:return False
        return self.state=='deployed' or (self.kind=='drone' and self.state=='retracted')


@dataclass
class Destruction:
    event_id: str
    instance_id: str
    enemy_caused: bool
    enemy_hit: bool
    deliberate_sacrifice: bool
    copied_object: bool
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
    no_own_destruction_chain: bool=False
    incoming_damage_was_copy: bool=False

    def hostile_qualifies(self):
        return self.first_for_instance and self.enemy_caused and not (
            self.deliberate_sacrifice or self.copied_object or self.friendly_damage or
            self.secondary_explosion or self.no_own_destruction_chain)


def profile_stats(kind,level,pb,*,intelligence=0,modifier=1,expertise=False,harmony=False):
    """Creation stats. Helpers' kind labels are aliases, not additional abilities."""
    integer(level,'class level',1,20);integer(pb,'proficiency bonus',1)
    integer(intelligence,'actual INT modifier',-10,20);integer(modifier,'M',1)
    if kind=='drone':return {'hp':max(1,5+intelligence+level),'ac':13+intelligence,'attack':pb+intelligence}
    if kind=='device':return {'hp':2*level+(modifier if expertise else 0),'ac':12+pb+int(expertise)}
    if kind in ('totem','echo'):return {'hp':2*level,'ac':12+pb}
    if kind=='elemental':return {'hp':(3 if harmony else 2)*level,'ac':12+pb//2}
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
        if not e.field_repair_target(now) or (e.hp==e.maximum_hp and not e.disabled):
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
               deliberate_sacrifice=False,incoming_damage_was_copy=False,friendly_damage=False,
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
        material=first and e.kind in MACHINE_KINDS and not e.no_own_destruction_chain
        d=Destruction(event_id,ident,enemy_caused,enemy_hit,deliberate_sacrifice,e.is_copy,
                      friendly_damage,secondary_explosion,frozenset(flags),hostile_source,
                      first,material,no_replacement=e.kind in SCRAPLING_KINDS,
                      no_own_destruction_chain=e.no_own_destruction_chain,
                      incoming_damage_was_copy=incoming_damage_was_copy)
        self.destructions[event_id]=d;e.destruction_history.append(event_id)
        if material:e.material_event=event_id
        for child in tuple(self.entities.values()):
            if child.parent_id==ident:self.end(child.instance_id)
        # Elementals disappear; the immutable cause record remains for Cinderflame.
        return {**result,'disappeared':e.kind in SCRAPLING_KINDS|{'elemental','chorus'}},d

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
        if d.deliberate_sacrifice or d.copied_object or d.no_own_destruction_chain or 'noResourceGeneration' in d.flags:
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
        if reaper and 'noDeathTriggers' in d.flags:
            raise SpellRuleError('Inherited noDeathTriggers blocks Scrap Reaper')
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
        # All packet-supplied timed effects expire during a completed LR. This
        # is NOT permission to erase a future permanent/LR-surviving effect.
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
            if level>=13 and len(mods)!=(1 if mode=='dual' else 2):
                raise SpellRuleError('Dual Protocol requires exact one-per-dual or two-distinct-on-single modules')
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
                          secondary_explosion=False,incoming_damage_was_copy=False):
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
        incoming_damage_was_copy=incoming_damage_was_copy,flags=b.flags)
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
    b.retract('e');e.hp=5;w=Wallet(1)
    check('Touched retracted Drone accepts Field Repair',b.field_repair('e',2,w,8),8)
    check('Retracted repair neither redeploys nor resets payment',(e.hp,e.state,w.rp,w.actions),(13,'retracted',0,0))
    e.hp=e.maximum_hp;b.set_disabled(e,True)
    check('Full-HP retracted Drone may clear disable by touch',b.field_repair('e',2,Wallet(1),5),0)
    check('Touch clearing preserves retraction',(e.state,e.disabled),('retracted',False))
    rejects('Retracted Drone still cannot route Dissonance',lambda:b.disable('e',2,Wallet(),dissonance=2,amount=1,use_key='route/sr2'))
    e.unavailable=True;e.hp=5
    rejects('Withdrawn unavailable Drone not eligible in current configuration',lambda:b.field_repair('e',2,Wallet(1),5))

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
    b=board();e=put(b,entity());d=kill(b,e,enemy_caused=True,incoming_damage_was_copy=True)
    check('Real object and copied incoming damage stay distinct',(d.copied_object,d.incoming_damage_was_copy),(False,True))
    check('Copied incoming damage retains ordinary target-side destruction',b.settle_volatile('death',1,chosen=True,enemy_in_range=True,scale=2),2)
    check('Copy damage alone does not prohibit later Recycling',b.recycling('e',Wallet(),use_key='recycle/sr1'),1)
    b=board();e=put(b,entity(is_copy=True));d=kill(b,e,enemy_caused=True)
    check('Copied object exclusion comes from entity record',(d.copied_object,d.incoming_damage_was_copy),(True,False))
    check('Copied object does not qualify Volatile',b.settle_volatile('death',1,chosen=True,enemy_in_range=True,scale=2),0)
    rejects('Copied object cannot recycle',lambda:b.recycling('e',Wallet(),use_key='recycle/sr1'))

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
    check('Standard elementals use frozen half-PB AC',[profile_stats('elemental',10,pb)['ac'] for pb in range(2,7)],[13,13,14,14,15])
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
    check('Scrapling destruction grants no generic device material',b.destructions['scrapdeath'].material_available,False)
    check('Scrapling is not a Volatile device',b.settle_volatile('scrapdeath',1,chosen=True,enemy_in_range=True,scale=2),0)
    rejects('Scrapling is not a Recycling device',lambda:b.recycling('scrap',Wallet(),use_key='recycle/sr1'))
    rejects('Scrapling is not a Snap device',lambda:b.reconstruct('scrap',3,Wallet(2),method='snap',use_key='snap/enc1'))
    b=board();s=put(b,entity('s','salvage'));s.hp=5
    rejects('Slot-using Scrapling is not a Field Repair machine',lambda:b.field_repair('s',1,Wallet(1),5))
    rejects('Scrapling is not a Repair Pulse device',lambda:b.repair_pulse(('s',),1,Wallet(3),use_key='repair/sr1',ac_deadline=ClockMarker(6)))
    rejects('Scrapling cannot route protected Dissonance',lambda:b.disable('s',1,Wallet(),dissonance=2,amount=1,use_key='route/sr1'))
    b=board();e=put(b,entity());d=kill(b,e,enemy_caused=True,enemy_hit=True,flags={'noDeathTriggers','noResourceGeneration'})
    w=Wallet(2)
    rejects('noDeathTriggers rejects Reaction Reaper',lambda:b.salvage('e',entity('r','reaper'),2,w,reaper=True,use_key='reaper/sr1'))
    check('Blocked Reaper preserves Reaction RP and material',(w.rp,w.reaction,d.material_available),(2,True,True))
    b.salvage('e',entity('s','salvage'),2,w,use_key='salvage/enc1')
    check('Later Action Salvage not blocked by noDeath/noResource flags',(w.rp,d.material_consumer),(1,'salvage'))
    b=board();r=put(b,entity('r','reaper'))
    result,d=b.damage('r',1,999,event_id='rdeath',enemy_caused=True,enemy_hit=True)
    check('Reaper disappears retaining hard no-own-death-chain',(result['disappeared'],d.no_own_destruction_chain,d.material_available),(True,True,False))

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
    rejects('Dual Protocol rejects both empty modules',lambda:b.configure_drones('owner',level=13,mode='dual',modules_by_asset={d1.asset_id:(),d2.asset_id:()}))
    rejects('Dual Protocol rejects one empty Drone',lambda:b.configure_drones('owner',level=13,mode='dual',modules_by_asset={d1.asset_id:(),d2.asset_id:('a',)}))
    rejects('Single level13 Protocol requires exactly two modules',lambda:b.configure_drones('owner',level=13,mode='single',modules_by_asset={d1.asset_id:('a',)}))
    check('Rejected module cardinalities preserve prior valid dual modules',(d1.modules,d2.modules),(('a',),('b',)))

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


## docs/mechanics/DEVICE_LIFECYCLE_PLAYTEST_VALIDATION.json

{
  "result": "PASS",
  "status": "IMPLEMENTED; GPT exact review pending",
  "scope": "74 class-source lifecycle roles plus3 frozen shared paragraphs; no full-card/game completeness claim",
  "checkCount": 132,
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
      "name": "Touched retracted Drone accepts Field Repair",
      "result": "PASS"
    },
    {
      "name": "Retracted repair neither redeploys nor resets payment",
      "result": "PASS"
    },
    {
      "name": "Full-HP retracted Drone may clear disable by touch",
      "result": "PASS"
    },
    {
      "name": "Touch clearing preserves retraction",
      "result": "PASS"
    },
    {
      "name": "Retracted Drone still cannot route Dissonance",
      "result": "PASS"
    },
    {
      "name": "Withdrawn unavailable Drone not eligible in current configuration",
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
      "name": "Real object and copied incoming damage stay distinct",
      "result": "PASS"
    },
    {
      "name": "Copied incoming damage retains ordinary target-side destruction",
      "result": "PASS"
    },
    {
      "name": "Copy damage alone does not prohibit later Recycling",
      "result": "PASS"
    },
    {
      "name": "Copied object exclusion comes from entity record",
      "result": "PASS"
    },
    {
      "name": "Copied object does not qualify Volatile",
      "result": "PASS"
    },
    {
      "name": "Copied object cannot recycle",
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
      "name": "Standard elementals use frozen half-PB AC",
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
      "name": "Scrapling destruction grants no generic device material",
      "result": "PASS"
    },
    {
      "name": "Scrapling is not a Volatile device",
      "result": "PASS"
    },
    {
      "name": "Scrapling is not a Recycling device",
      "result": "PASS"
    },
    {
      "name": "Scrapling is not a Snap device",
      "result": "PASS"
    },
    {
      "name": "Slot-using Scrapling is not a Field Repair machine",
      "result": "PASS"
    },
    {
      "name": "Scrapling is not a Repair Pulse device",
      "result": "PASS"
    },
    {
      "name": "Scrapling cannot route protected Dissonance",
      "result": "PASS"
    },
    {
      "name": "noDeathTriggers rejects Reaction Reaper",
      "result": "PASS"
    },
    {
      "name": "Blocked Reaper preserves Reaction RP and material",
      "result": "PASS"
    },
    {
      "name": "Later Action Salvage not blocked by noDeath/noResource flags",
      "result": "PASS"
    },
    {
      "name": "Reaper disappears retaining hard no-own-death-chain",
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
    },
    {
      "name": "Dual Protocol rejects both empty modules",
      "result": "PASS"
    },
    {
      "name": "Dual Protocol rejects one empty Drone",
      "result": "PASS"
    },
    {
      "name": "Single level13 Protocol requires exactly two modules",
      "result": "PASS"
    },
    {
      "name": "Rejected module cardinalities preserve prior valid dual modules",
      "result": "PASS"
    }
  ]
}

