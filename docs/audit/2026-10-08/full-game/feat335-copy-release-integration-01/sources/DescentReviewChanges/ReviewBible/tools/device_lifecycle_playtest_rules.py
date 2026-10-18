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
    reservations: dict=field(default_factory=dict)

    def validate(self,round_number,mode,wallet,*,rp=0,tinker=False,regular=True):
        integer(round_number,'numbered round',1)
        if mode not in ('support','attack','control','gadget-sync','decoy'):
            raise SpellRuleError('Not a shared command mode')
        command=mode in ('support','attack','control')
        offensive=mode!='support'
        if tinker and command and not regular:
            raise SpellRuleError('Tinker command requires a regular turn')
        entry=self.rounds.get(round_number,{'command':False,'damage':False})
        if command and entry['command']:raise SpellRuleError('Round companion command spent')
        if offensive and (entry['damage'] or round_number in self.reservations):
            raise SpellRuleError('Round companion offense spent or reserved')
        if mode=='gadget-sync' and rp!=1:raise SpellRuleError('Gadget Sync costs 1 RP')
        if mode=='decoy' and rp!=0:raise SpellRuleError('Decoy trigger has no RP cost')
        wallet.validate(rp,'bonus' if command else None)
        return command,offensive,entry

    def reserve(self,issuance_round,resolution_round,order_id,wallet):
        """Reflective order pays current BA, reserves future offense atomically."""
        identity(order_id)
        integer(resolution_round,'resolution round',issuance_round)
        command,_,entry=self.validate(issuance_round,'support',wallet)
        future=self.rounds.get(resolution_round,{'command':False,'damage':False})
        if future['damage'] or resolution_round in self.reservations or order_id in self.reservations.values():
            raise SpellRuleError('Future offense already committed or duplicate order')
        wallet.pay(action='bonus')
        self.rounds[issuance_round]={'command':True,'damage':entry['damage']}
        self.reservations[resolution_round]=order_id

    def settle(self,resolution_round,order_id,*,executed):
        if self.reservations.get(resolution_round)!=order_id:
            raise SpellRuleError('No matching offensive reservation')
        del self.reservations[resolution_round]
        if executed:
            entry=self.rounds.setdefault(resolution_round,{'command':False,'damage':False})
            entry['damage']=True

    def activate(self,round_number,mode,wallet,*,rp=0,tinker=False,regular=True):
        command,damaging,entry=self.validate(round_number,mode,wallet,rp=rp,tinker=tinker,regular=regular)
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
