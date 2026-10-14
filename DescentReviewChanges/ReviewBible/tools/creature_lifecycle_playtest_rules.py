"""Reviewed bounded creature lifecycle reference; selected100+5 roles only.

Callers own source access, acquisition/consent gates, legal geometry, rolls,
conditions, concentration, ordinary class resources and canonical clocks.
Boolean legality inputs certify those checks; these helpers do not infer them.
Use ONE world, owner wallet/CommandLedger, encounter hard-denial set and Echo
ledger across all sources. No method grants Wizard elite acquisition or return.
No full class card, organic life procedure or complete scheduler is implemented.
"""
from dataclasses import dataclass, field
from copy import deepcopy
from control_playtest_rules import ClockMarker, clock_marker, require_deadline
from spell_playtest_rules import SpellRuleError, integer
from redirection_playtest_rules import identity
from device_lifecycle_playtest_rules import Wallet, CommandLedger
from maximum_hp_playtest_rules import effective_maximum


def require(value,message):
    if not value:raise SpellRuleError(message)


@dataclass(frozen=True)
class SourceStats:
    owner: str
    source_class: str
    level: int
    pb: int
    modifier: int
    scale: int
    attack: int
    dc: int
    wisdom: int=0

    def __post_init__(self):
        identity(self.owner)
        require(self.source_class in ('druid','mage','mirrorsage','ranger','wizard'),'Unsupported source class')
        integer(self.level,'class level',1,20);integer(self.pb,'PB',1)
        integer(self.scale,'S',1,4);integer(self.modifier,'M',1)
        for v in (self.attack,self.dc,self.wisdom):
            require(isinstance(v,int) and not isinstance(v,bool),'Integer stat required')


STANDARD_UNDEAD={
    'skeleton':(14,6,2,30,30,'1d6+S'),
    'zombie':(12,10,3,20,5,'1d8+S'),
    'goblin-thrall':(13,8,2,30,5,'1d6+S')}
ELITES={
    'boneflayer':(14,12,2,30,60,'2d6+S'),
    'dreadblade':(16,16,3,30,5,'1d8+S'),
    'wraithbound':(14,10,2,40,5,'1d8+S')}
FINITE_SOURCES={
    'druid.base.rotshaper.swarm-summoning':('swarm',0,'action',600,'short'),
    'druid.hero.rotshaper.carrion-rat-king':('swarm',0,'action',60,'form'),
    'druid.hero.rotshaper.insect-broodmother':('swarm',0,None,60,'form'),
    'mage.arch.conjure-elemental-familiar':('familiar',4,'action',600,'long'),
    'mirrorsage.base.mirror-beast-summon':('mirror',2,'action',60,'recharge'),
    'mirrorsage.hero.light-weaver.radiant-mirror-beast':('radiant',4,'action',None,'recharge'),
    'mirrorsage.hero.shattered-one.shattered-mirror-beast':('shattered',4,'action',None,'recharge')}


@dataclass
class Creature:
    instance_id: str
    source_owner: str
    controller: str
    source_class: str
    source_id: str
    profile: str
    life_kind: str
    base_maximum: int
    maximum_hp: int
    hp: int
    ac: int
    speed: int
    expiry: ClockMarker | None=None
    concentration: str | None=None
    parent_form: str | None=None
    command_group: str | None=None
    asset_id: str | None=None
    state: str='active'
    temp_hp: int=0
    temp_expiry: ClockMarker | None=None
    blocked_round: int | None=None
    focus: str | None=None
    movement_mode: str='walk'
    keen_sense: str | None=None
    effects: dict=field(default_factory=dict)
    spent_uses: set=field(default_factory=set)
    recharges: dict=field(default_factory=dict)
    max_hp_records: list=field(default_factory=list)
    round_options: set=field(default_factory=set)
    appearance: str | None=None
    movement_overrides: dict=field(default_factory=dict)
    death_count: int=0
    invisible: bool=False
    invis_resume_marker: int=0
    last_marker: int=0

    def __post_init__(self):
        for v in (self.instance_id,self.source_owner,self.controller,self.source_id):identity(v)
        require(self.life_kind in ('finite','ranger','mage-elite','wizard-standard'),'Unsupported lifecycle; Wizard elite creation absent')
        integer(self.maximum_hp,'max HP',1);integer(self.base_maximum,'base max HP',1)
        integer(self.hp,'HP',0,self.maximum_hp);integer(self.temp_hp,'temp HP',0)
        if self.expiry is not None:require_deadline(self.expiry)
        if self.temp_expiry is not None:require_deadline(self.temp_expiry)
        require(self.state in ('active','unbonded','ended','dead','destroyed'),'Unknown life state')

    def active(self,now):
        return self.state=='active' and self.hp>0 and (self.expiry is None or clock_marker(now)<self.expiry)

    def can_act(self,now,round_number):
        return self.active(now) and self.blocked_round!=round_number

    def verify_stats(self,stats):
        require((stats.owner,stats.source_class)==(self.source_owner,self.source_class),'Stats must follow original source owner/class')

    def refresh_maximum(self,stats,now=0):
        self.verify_stats(stats)
        base=self.base_maximum
        if self.life_kind=='ranger':
            base=max(1,2*stats.level+stats.wisdom)
            self.ac=12+stats.pb//2
        elif self.life_kind=='mage-elite':
            _,fixed,mult,_,_,_=ELITES[self.profile];base=fixed+mult*stats.level
        self.base_maximum=base
        self.maximum_hp=effective_maximum(base,self.max_hp_records,target=self.instance_id,now=now)['effectiveMaximum']
        self.hp=min(self.hp,self.maximum_hp)
        return self.maximum_hp

    def attack_profile(self,stats):
        self.verify_stats(stats)
        out={'sourceOwner':self.source_owner,'sourceClass':self.source_class,'attack':stats.attack,
             'saveDC':stats.dc,'scale':stats.scale,'saves':stats.pb,'resourceEligible':False}
        if self.profile in ELITES or self.profile in STANDARD_UNDEAD:
            row=(ELITES|STANDARD_UNDEAD)[self.profile]
            out.update(range=row[4],damage=row[5],damageType='necrotic')
        elif self.profile=='familiar':
            out.update(range=30,damage='S d4',damageType=self.focus,saves='current source-owner saves')
        else:
            out.update(range=5,damage='S d6',damageType='source chosen normal attack')
            if self.source_class in ('druid','ranger'):
                out['attack']=stats.pb+stats.wisdom
            if self.profile=='swarm':out['damageType']='piercing'
        return out

    def regular_end(self,marker_index,*,regular=True):
        """Original owner-linked marker only; never attached checkpoint/extra turn."""
        integer(marker_index,'regular companion marker index',1)
        require(regular and marker_index>self.last_marker,'Marker cannot repeat/reset or come from extra turn')
        self.last_marker=marker_index
        if self.profile=='wraithbound' and self.state=='active' and marker_index>=self.invis_resume_marker:
            self.invisible=True

    def offense_event(self,marker_index):
        if self.profile=='wraithbound':
            self.invisible=False
            self.invis_resume_marker=max(self.invis_resume_marker,marker_index+1)


@dataclass
class Corpse:
    """One physical body identity, with current corpse eligibility kept separate."""
    body_id: str
    creature_id: str
    creature_type: str
    goblinoid: bool=False
    real_original: bool=True
    body_state: str='corpse'
    consumed_by: str | None=None

    def __post_init__(self):
        identity(self.body_id);identity(self.creature_id)
        require(self.body_state in ('living','corpse','consumed','removed'),'Unknown physical body state')

    @property
    def available(self):return self.body_state=='corpse'

    def eligible(self,profile,*,pact=False):
        return self.available and self.real_original and (
            self.creature_type=='humanoid' or (pact and self.creature_type=='fiend')) and (
            profile!='goblin-thrall' or self.goblinoid)


@dataclass
class RaiseReservation:
    order_id: str
    owner: str
    corpse_id: str
    profile: str
    round_number: int
    checkpoint_id: str
    pact: bool


@dataclass
class AttachedOrder:
    order_id: str
    owner: str
    creatures: tuple
    mode: str
    round_number: int
    attacks: int=1
    settled: bool=False


@dataclass
class HardDenialLedger:
    """Adapter over the canonical ALL-feature (encounter, character, target) set."""
    used: set=field(default_factory=set)

    def available(self,encounter,owner,target):
        for v in (encounter,owner,target):identity(v)
        return (encounter,owner,target) not in self.used

    def spend(self,encounter,owner,target):
        require(self.available(encounter,owner,target),'Shared hard-denial allowance spent')
        self.used.add((encounter,owner,target))


@dataclass
class ReflectiveBond:
    owner: str
    target_id: str
    effect_id: str
    expiry: ClockMarker
    concentration: str
    active: bool=True
    forced_action_used: bool=False
    pending: dict | None=None

    def operative(self,now):return self.active and clock_marker(now)<self.expiry

    def cancel(self,ledger):
        require(ledger.owner==self.owner,'Wrong command ledger')
        if self.pending:
            ledger.settle(self.pending['round'],self.pending['id'],executed=False)
            self.pending=None

    def revalidate_pending(self,now,ledger,hard,*,capable,legal):
        if not self.pending:return False
        valid=(self.operative(now) and capable and legal and
               hard.available(self.pending['encounter'],self.owner,self.target_id))
        if not valid:self.cancel(ledger)
        return bool(valid)

    def end(self,ledger):
        self.cancel(ledger);self.active=False

    def queue(self,now,round_number,order_id,wallet,ledger,hard,encounter,*,target_turn_upcoming,capable,legal):
        identity(order_id)
        require(ledger.owner==self.owner,'Wrong command ledger')
        require(self.operative(now) and capable and legal,'No legal forced order')
        require(not self.pending and not self.forced_action_used,'One pending and one total forced Action')
        require(hard.available(encounter,self.owner,self.target_id),'Hard denial already spent')
        resolution=round_number if target_turn_upcoming else round_number+1
        ledger.reserve(round_number,resolution,order_id,wallet)
        self.pending={'id':order_id,'round':resolution,'encounter':encounter}
        return resolution

    def resolve(self,now,round_number,ledger,hard,*,actual_regular_action_slot,capable,legal):
        require(ledger.owner==self.owner and self.pending is not None,'No matching pending order')
        order=self.pending
        require(actual_regular_action_slot and round_number==order['round'],'Must replace designated future regular Action')
        valid=(self.operative(now) and capable and legal and
               hard.available(order['encounter'],self.owner,self.target_id))
        ledger.settle(round_number,order['id'],executed=valid)
        self.pending=None
        if valid:
            hard.spend(order['encounter'],self.owner,self.target_id);self.forced_action_used=True
        return {'replacesNormalAction':bool(valid),'attackRolls':1 if valid else 0,
                'damageCap':'S d6','uniquePowers':False,'extraTurn':False}


@dataclass
class EchoLedger:
    """Use the owner's canonical record/release sets, shared with every Echo path."""
    owner: str
    records: set=field(default_factory=set)
    released_rounds: set=field(default_factory=set)


class CreatureWorld:
    def __init__(self):
        self.creatures={};self.corpses={};self.reflective={}
        self.reservations={};self.auto_used=set();self.closed_checkpoints=set()
        self.orders={};self.completed_rests={};self.ranger_deaths={}
        self.noncorpse_identities=set()  # Exact external created-object integrations.

    def fresh(self,ident):
        identity(ident)
        require(ident not in self.creatures and ident not in self.noncorpse_identities,'Creature/object identity already exists')

    def register_corpse(self,corpse):
        require(corpse.body_id not in self.corpses,'Body identity already registered')
        require(not any(c.creature_id==corpse.creature_id for c in self.corpses.values()),'Fragments/repeated death are not new bodies')
        require(corpse.real_original,'Summoned/copied/raised remains are not corpse fuel')
        require(corpse.creature_id not in self.noncorpse_identities,'Known created object cannot become real body fuel')
        known=self.creatures.get(corpse.creature_id)
        require(known is None or known.life_kind=='ranger','Known created companion cannot become real body fuel')
        self.corpses[corpse.body_id]=corpse

    def consume_body(self,body_id,consumer):
        identity(consumer);corpse=self.corpses[body_id]
        require(corpse.available,'Body already consumed')
        corpse.body_state='consumed';corpse.consumed_by=consumer

    def standard_count(self,owner):
        return sum(c.source_owner==owner and c.life_kind=='wizard-standard' and c.state=='active'
                   for c in self.creatures.values())+sum(r.owner==owner for r in self.reservations.values())

    def _end_mirror_slot(self,owner,ledger):
        for c in self.creatures.values():
            if c.source_owner==owner and c.profile in ('mirror','radiant','shattered') and c.state=='active':c.state='ended'
        bond=self.reflective.get(owner)
        if bond:bond.end(ledger)

    def summon(self,source,ids,stats,now,expiry,wallet,*,use_key,legal,concentration=None,
               parent_form=None,form_surge_paid=False,focus=None,mirrorcall=False,ledger=None,records=()):
        require(source in FINITE_SOURCES,'Only supplied summon procedures may create finite creatures')
        require(legal and source.split('.')[0]==stats.source_class,'Caller must validate exact access/placement/clock')
        profile,rp,action,seconds,_=FINITE_SOURCES[source]
        now=clock_marker(now);require_deadline(expiry)
        require(expiry>now,'Expired summon')
        if seconds is not None:require(expiry.seconds-now.seconds<=seconds,'Duration exceeds printed bound')
        count=2 if source.endswith('insect-broodmother') else 1
        require(len(ids)==count and len(set(ids))==count,'Wrong source body count')
        for ident in ids:self.fresh(ident)
        if profile in ('radiant','shattered') or source.endswith('swarm-summoning'):
            require(bool(concentration),'Printed concentration required')
        form_source=source.endswith(('carrion-rat-king','insect-broodmother'))
        if form_source:require(parent_form and form_surge_paid,'Actual current form and paid Form Surge required')
        else:require(parent_form is None,'Independent summon must not inherit a form dependency')
        if profile=='familiar':require(focus in ('fire','cold','lightning'),'Choose actual current Focus')
        if profile in ('mirror','radiant','shattered'):
            require(ledger is not None and ledger.owner==stats.owner,'Canonical mirror command ledger required')
        require(use_key is not None,'Canonical source frequency/recharge key required')
        wallet.validate(rp,action,use_key)
        created=[]
        for ident in ids:
            hp=2*stats.level;ac=12+stats.pb//2;speed=30
            if profile=='familiar':hp=5+stats.level+stats.modifier;ac=12+stats.pb
            if profile in ('mirror','radiant','shattered') and mirrorcall:hp+=stats.modifier;speed+=5
            maximum=effective_maximum(hp,records,target=ident,now=now)['effectiveMaximum']
            c=Creature(ident,stats.owner,stats.owner,stats.source_class,source,profile,'finite',hp,maximum,maximum,ac,speed,
                       expiry=expiry,concentration=concentration,parent_form=parent_form,
                       command_group=(parent_form if count==2 else None),focus=focus,
                       max_hp_records=list(records))
            if profile=='familiar':
                if focus=='lightning':c.movement_overrides['fly']=30
                else:c.effects['resistance']=focus
            created.append(c)
        wallet.pay(rp,action,use_key)
        if profile=='familiar':
            for c in self.creatures.values():
                if c.source_owner==stats.owner and c.profile=='familiar' and c.state=='active':c.state='ended'
        if profile in ('mirror','radiant','shattered'):self._end_mirror_slot(stats.owner,ledger)
        if source.endswith('carrion-rat-king'):
            for c in self.creatures.values():
                if c.source_owner==stats.owner and c.source_id==source and c.state=='active':c.state='ended'
        for c in created:self.creatures[c.instance_id]=c
        return tuple(created)

    def end_dependency(self,*,form=None,concentration=None,ledger=None):
        require(bool(form)!=bool(concentration),'End one actual dependency')
        for b in self.reflective.values():
            if concentration and b.concentration==concentration and b.active:
                require(ledger is not None and ledger.owner==b.owner,'Canonical ledger needed to release queued compulsion')
        for c in self.creatures.values():
            if c.state=='active' and ((form and c.parent_form==form) or (concentration and c.concentration==concentration)):
                c.state='ended'
        for b in self.reflective.values():
            if concentration and b.concentration==concentration and b.active:
                require(ledger is not None and ledger.owner==b.owner,'Canonical ledger needed to release queued compulsion')
                b.end(ledger)

    def expire(self,now,ledgers):
        for b in self.reflective.values():
            if b.active and clock_marker(now)>=b.expiry:
                require(b.owner in ledgers and ledgers[b.owner].owner==b.owner,'Canonical expiration ledger required')
        for c in self.creatures.values():
            if c.expiry is not None and clock_marker(now)>=c.expiry and c.state=='active':c.state='ended'
            if c.temp_expiry is not None and clock_marker(now)>=c.temp_expiry:c.temp_hp=0;c.temp_expiry=None
        for b in self.reflective.values():
            if b.active and clock_marker(now)>=b.expiry:b.end(ledgers[b.owner])

    def damage(self,ident,amount,now,*,body_survives=True):
        """Post-defense/pre-tempHP amount, already legally targeted; HP-only layer."""
        c=self.creatures[ident];integer(amount,'post-defense damage',0)
        require(c.active(now),'Inactive creature cannot receive this live damage packet')
        if c.temp_expiry is not None and clock_marker(now)>=c.temp_expiry:c.temp_hp=0;c.temp_expiry=None
        absorbed=min(c.temp_hp,amount);c.temp_hp-=absorbed
        loss=min(c.hp,amount-absorbed);c.hp-=loss
        if c.hp==0:
            c.death_count+=1;c.temp_hp=0
            if c.life_kind=='ranger':
                c.state='dead';self.ranger_deaths[c.source_owner]=self.completed_rests.get(c.source_owner,0)
                body=next((x for x in self.corpses.values() if x.creature_id==ident),None)
                if body is None:
                    self.register_corpse(Corpse('body:'+ident,ident,'beast',body_state='corpse' if body_survives else 'removed'))
                elif body.body_state=='living':
                    body.body_state='corpse' if body_survives else 'removed'
                # A consumed/removed body cannot reappear merely from another event.
            elif c.life_kind in ('mage-elite','wizard-standard'):c.state='destroyed'
            else:c.state='ended'
        return {'hpLost':loss,'tempHPAbsorbed':absorbed,'state':c.state,'woundRoll':False,
                'deathSave':False,'resourceEligible':False,'corpseCreated':c.life_kind=='ranger' and c.hp==0 and
                any(x.creature_id==ident and x.available for x in self.corpses.values())}

    def heal(self,ident,amount,now,*,legal):
        """Already-resolved legal normal HP restoration; no rest/HD entitlement."""
        integer(amount,'resolved HP restoration',0);c=self.creatures[ident]
        require(legal and c.active(now),'Healing cannot restore destroyed/dead/ended creature')
        gain=min(amount,c.maximum_hp-c.hp);c.hp+=gain;return gain

    def record_ranger_resurrection(self,ident,*,legal,restored_hp,restored_maximum,body_reconstructed=False,effects=None):
        """Accept an already-resolved independent legal resurrection, NOT grant one.

        Caller owns the actual source, costs, time/body/condition eligibility and
        its restored stats/effects. This immediately invalidates the corpse even
        before any future ritual. Missing-body return requires explicit source
        reconstruction. It neither restores a bond nor refreshes rests/uses.
        """
        c=self.creatures[ident]
        require(legal and c.life_kind=='ranger' and c.state=='dead','Actual independent dead Beast resurrection required')
        integer(restored_maximum,'source-restored maximum HP',1)
        integer(restored_hp,'source-restored current HP',1,restored_maximum)
        body=next((x for x in self.corpses.values() if x.creature_id==ident),None)
        require(body is not None,'Known original body identity required')
        require(body.available or (body_reconstructed and body.body_state in ('consumed','removed')),
                'Consumed/removed body requires actual source-authorized reconstruction')
        body.body_state='living'  # consumed_by remains historical provenance, not current eligibility.
        c.state='unbonded';c.hp=restored_hp;c.maximum_hp=restored_maximum;c.base_maximum=restored_maximum
        if effects is not None:c.effects=deepcopy(effects)
        return c

    def bond_ranger(self,ident,stats,wallet,*,use_key,old_hp,old_maximum,movement_mode,speed,keen_sense,
                    legal,effects=None,resurrected=False):
        require(stats.source_class=='ranger' and legal,'Actual eligible willing/tamed noncorrupted Beast: touch, INT<7, CR<=level, one hour')
        integer(old_maximum,'original max HP',1);integer(old_hp,'living original HP',1,old_maximum)
        integer(speed,'retained movement speed',0,40);identity(movement_mode);identity(keen_sense)
        require(not any(c.source_owner==stats.owner and c.life_kind=='ranger' and c.state=='active' for c in self.creatures.values()),'Cannot rebind living wounded companion')
        require(self.completed_rests.get(stats.owner,0)>self.ranger_deaths.get(stats.owner,-1),'Complete an actual long rest after bond death')
        prior=self.creatures.get(ident)
        if prior:
            require(resurrected and prior.life_kind=='ranger' and prior.state=='unbonded','Record actual independent resurrection before new ritual')
            require((old_hp,old_maximum)==(prior.hp,prior.maximum_hp),'Use actual current post-resurrection HP ratio')
        else:self.fresh(ident)
        body=next((x for x in self.corpses.values() if x.creature_id==ident),None)
        require(body is None or body.body_state=='living','A corpse cannot be bonded as a living Beast')
        require(use_key is not None,'Bond requires canonical long-rest use key')
        wallet.validate(4,None,use_key)
        maximum=max(1,2*stats.level+stats.wisdom)
        state=deepcopy(effects if effects is not None else (prior.effects if prior else {}))
        c=Creature(ident,stats.owner,stats.owner,'ranger','ranger.hero.warder.beast-companion','beast','ranger',
                   maximum,maximum,max(1,maximum*old_hp//old_maximum),12+stats.pb//2,speed,
                   movement_mode=movement_mode,keen_sense=keen_sense,effects=state,
                   death_count=prior.death_count if prior else 0)
        wallet.pay(4,None,use_key);self.creatures[ident]=c
        return c

    def unlock_lich(self,stats,ids,*,successful_transformation,records=()):
        require(stats.source_class=='mage' and successful_transformation,'Actual successful consented transformation required; helper does not perform ritual')
        require(set(ids)==set(ELITES) and len(set(ids.values()))==3,'Exactly three unique bound assets')
        for ident in ids.values():self.fresh(ident)
        require(not any(c.source_owner==stats.owner and c.profile in ELITES for c in self.creatures.values()),'Named elite identity already owned, even if destroyed')
        created=[]
        for profile,ident in ids.items():
            ac,fixed,mult,speed,_,_=ELITES[profile];base=fixed+mult*stats.level
            maximum=effective_maximum(base,records,target=ident)['effectiveMaximum']
            c=Creature(ident,stats.owner,stats.owner,'mage','mage.engine[11]',profile,'mage-elite',base,maximum,maximum,ac,speed,
                       asset_id=ident,max_hp_records=list(records),invisible=profile=='wraithbound',
                       movement_mode='fly-hover' if profile=='wraithbound' else 'walk')
            created.append(c)
        for c in created:self.creatures[c.instance_id]=c
        return tuple(created)

    def soulbound(self,ident,stats,wallet,now,*,use_key,legal):
        c=self.creatures[ident];c.verify_stats(stats)
        require(c.life_kind=='mage-elite' and c.state=='destroyed' and legal,'Destroyed own bound Mage elite/token and empty space30 required')
        require(use_key is not None,'Soulbound requires canonical long-rest use key')
        wallet.validate(5,'action',use_key)
        c.refresh_maximum(stats,now);wallet.pay(5,'action',use_key)
        c.state='active';c.hp=max(1,c.maximum_hp//2)
        c.temp_hp=max(c.temp_hp,stats.scale+stats.modifier)
        c.temp_expiry=ClockMarker(clock_marker(now).seconds+60)
        return c

    def completed_long_rest(self,owner,stats,now,*,return_prevented=False):
        require(stats.owner==owner,'Rest stats owner mismatch')
        for c in self.creatures.values():
            if c.source_owner==owner and c.life_kind=='mage-elite' and not return_prevented:c.verify_stats(stats)
        self.completed_rests[owner]=self.completed_rests.get(owner,0)+1
        for c in self.creatures.values():
            if c.source_owner!=owner:continue
            if c.life_kind=='wizard-standard' and c.state=='active':c.state='ended'
            if c.life_kind=='mage-elite' and not return_prevented:
                c.refresh_maximum(stats,now);c.hp=c.maximum_hp;c.state='active'
        # Canonical rest system, not this HP return, resets source uses/recharges.

    def _new_standard(self,ident,owner,profile,stats,*,source,records=(),blocked_round=None,now=0):
        self.fresh(ident);require(stats.owner==owner and stats.source_class=='wizard','Original Wizard statistics required')
        require(profile in STANDARD_UNDEAD,'Unknown standard undead')
        ac,fixed,mult,speed,_,_=STANDARD_UNDEAD[profile];base=fixed+mult*stats.level
        maximum=effective_maximum(base,records,target=ident,now=now)['effectiveMaximum']
        return Creature(ident,owner,owner,'wizard',source,profile,'wizard-standard',base,maximum,maximum,ac,speed,
                        max_hp_records=list(records),blocked_round=blocked_round)

    def harvest(self,ident,body_id,profile,stats,wallet,*,use_key,legal,pact=False,records=(),now=0):
        self.fresh(ident);require(profile in STANDARD_UNDEAD,'Unknown raised profile')
        require(legal and self.corpses[body_id].eligible(profile,pact=pact),'Eligible accessible real body30 and placement required')
        require(self.standard_count(stats.owner)<3,'Dismiss a standard minion before exceeding cap; reservations count')
        require(use_key is not None,'Harvest recharge key required');wallet.validate(4,'action',use_key)
        c=self._new_standard(ident,stats.owner,profile,stats,source='wizard.hero.necromancer.corpse-harvest',records=records,now=now)
        wallet.pay(4,'action',use_key);self.consume_body(body_id,ident);self.creatures[ident]=c
        return c

    def dismiss(self,ident):
        c=self.creatures[ident]
        require(c.life_kind in ('finite','wizard-standard'),'No generic persistent asset dismissal/rebinding')
        require(c.state=='active','Already ended');c.state='ended'

    def auto_raise_trigger(self,killer_id,body_id,round_number,checkpoint_id,order_id,*,pact=False,personal_killing_blow=True):
        integer(round_number,'numbered round',1);identity(checkpoint_id);identity(order_id)
        c=self.creatures[killer_id];require(order_id not in self.reservations,'Duplicate raise reservation')
        require(c.life_kind=='wizard-standard','Only standard undead can originate Auto-Raise')
        # Actual immediate trigger may already have destroyed the killer; snapshot identity survives.
        key=(c.source_owner,round_number)
        body=self.corpses[body_id]
        if (checkpoint_id in self.closed_checkpoints or key in self.auto_used or not personal_killing_blow
            or not body.eligible(c.profile,pact=pact) or self.standard_count(c.source_owner)>=3):return None
        require(not any(r.corpse_id==body_id for r in self.reservations.values()),'This corpse already reserved')
        r=RaiseReservation(order_id,c.source_owner,body_id,c.profile,round_number,checkpoint_id,pact)
        self.reservations[order_id]=r;self.auto_used.add(key);return r

    def auto_raise_checkpoint(self,checkpoint_id,stats_by_owner,placements,now=0):
        """After immediate/due damage, before expiry. Attached checkpoint is NOT a turn.

        placements maps reservation ID to (fresh minion ID, legal placement,
        max-HP records). Auto-Raise records must exclude new Conjuration grants.
        Missing/illegal placements fail the already-spent round opportunity.
        """
        identity(checkpoint_id);require(checkpoint_id not in self.closed_checkpoints,'Checkpoint already closed')
        due=[r for r in self.reservations.values() if r.checkpoint_id==checkpoint_id]
        planned=[];used_ids=set()
        for r in due:
            supplied=placements.get(r.order_id)
            c=None
            if supplied is not None:
                ident,legal,records=supplied
                if legal and self.corpses[r.corpse_id].eligible(r.profile,pact=r.pact) and self.standard_count(r.owner)<=3:
                    self.fresh(ident);require(ident not in used_ids,'Duplicate future instance identity')
                    require(not any(record.source=='wizard.engine[10]' for record in records),'Auto-Raise grants no new spell creation snapshot')
                    used_ids.add(ident)
                    c=self._new_standard(ident,r.owner,r.profile,stats_by_owner[r.owner],source='wizard.engine[20]',
                                         records=records,blocked_round=r.round_number,now=now)
            planned.append((r,c))
        self.closed_checkpoints.add(checkpoint_id)
        for r,c in planned:
            del self.reservations[r.order_id]
            if c:self.consume_body(r.corpse_id,c.instance_id);self.creatures[c.instance_id]=c
        return tuple(c for _,c in planned if c)

    def command(self,order_id,ids,mode,round_number,now,wallet,ledger,*,regular,legal,capable,
                ghoul_lash=False,adjacent_controlled_undead=False):
        identity(order_id);require(order_id not in self.orders,'Order identity already used')
        require(regular and legal and capable,'Attached ordinary command requires regular turn and legal capable actor/target')
        require(ids and len(set(ids))==len(ids),'Unique commanded body identities required')
        cs=[self.creatures[i] for i in ids]
        require(all(c.controller==ledger.owner and c.can_act(now,round_number) for c in cs),'Cannot command unavailable/creation-round creature or wrong owner')
        if len(cs)>1:
            require(len(cs)==2 and cs[0].command_group and all(c.command_group==cs[0].command_group for c in cs),'Only Broodmother combined pair command')
        require(mode in ('attack','control','support','radiant-heal'),'Unsupported command mode')
        if mode=='control':require(len(cs)==1 and cs[0].profile=='boneflayer','Only supplied Boneflayer control action here')
        if mode=='radiant-heal':require(len(cs)==1 and cs[0].profile=='radiant','Paid healing is Radiant Beast only')
        require(not any(round_number in c.round_options for c in cs if c.profile in ('mirror','radiant','shattered')),'Mirror option already used')
        if ghoul_lash:
            require(mode=='attack' and len(cs)==1 and cs[0].life_kind=='wizard-standard' and adjacent_controlled_undead,'Ghoul Lash requires own standard and adjacent controlled undead')
        rp=2 if ghoul_lash else (1 if mode=='radiant-heal' else 0)
        ledger.activate(round_number,'support' if mode in ('support','radiant-heal') else mode,wallet,rp=rp)
        for c in cs:
            if c.profile in ('mirror','radiant','shattered'):c.round_options.add(round_number)
        order=AttachedOrder(order_id,ledger.owner,tuple(ids),mode,round_number,2 if ghoul_lash else 1)
        self.orders[order_id]=order;return order

    def resolve_command(self,order_id,now,*,attached_phase,legal,capable):
        o=self.orders[order_id];require(not o.settled and attached_phase,'Resolve once in actual attached phase')
        o.settled=True
        valid=legal and capable and all(self.creatures[i].can_act(now,o.round_number) for i in o.creatures)
        return {'resolved':bool(valid),'attackRolls':o.attacks if valid and o.mode=='attack' else 0,
                'combinedBodies':o.creatures,'extraTurns':0,'refund':False,'mode':o.mode}

    def uncommanded(self,ident,now,round_number,*,capable):
        c=self.creatures[ident]
        return ('defensive-move','dodge') if capable and c.can_act(now,round_number) else ()

    def apply_reflective(self,owner,target_id,effect_id,expiry,concentration,wallet,ledger,*,use_key,legal,failed_save):
        for v in (owner,target_id,effect_id,concentration):identity(v)
        require_deadline(expiry);require(ledger.owner==owner and legal,'Exact INT<=6, target exclusions, save, source and geometry required')
        require(use_key is not None,'Charm requires long-rest use key');wallet.validate(3,'action',use_key)
        wallet.pay(3,'action',use_key)
        if not failed_save:return None
        self._end_mirror_slot(owner,ledger)
        bond=ReflectiveBond(owner,target_id,effect_id,expiry,concentration);self.reflective[owner]=bond
        # Original creature HP, identity, effects, initiative and stats are never copied/mutated.
        return bond

    def echo_from_beast(self,ident,stats,now,round_number,record_id,rp,wallet,commands,echoes,*,own_turn,legal):
        c=self.creatures[ident];c.verify_stats(stats)
        require(commands.owner==echoes.owner==c.controller,'Canonical owner command and Echo ledgers required')
        require(own_turn and legal and c.can_act(now,round_number) and c.profile in ('mirror','radiant','shattered'),'Legal current Beast origin and owner perception required')
        require(round_number not in c.round_options and round_number not in echoes.released_rounds,'Round Beast/release option spent')
        require(record_id in echoes.records,'Actual record required');integer(rp,'normal paid Echo cost',2)
        wallet.validate(rp,'action');commands.validate(round_number,'support',wallet,rp=rp)
        commands.activate(round_number,'support',wallet,rp=rp);wallet.pay(action='action')
        echoes.records.remove(record_id);echoes.released_rounds.add(round_number);c.round_options.add(round_number)
        return {'caster':stats.owner,'origin':ident,'resolves':'immediate owner Action','extraBeastMovement':False,
                'offensiveCompanionAllowanceSpent':False,'strainOwner':stats.owner,'concentrationOwner':stats.owner}

    def shift_appearance(self,ident,now,wallet,*,method,appearance,movement,use_key,legal):
        c=self.creatures[ident]
        require(c.active(now) and c.profile in ('mirror','radiant','shattered') and legal,'Active own Mirror Beast and actual stored appearance required')
        require(method in ('advanced-mirrorcall','mirror-shift') and movement in ('swim','climb'),'Source permits swim/climb only')
        identity(appearance);require(use_key is not None,'Source frequency key required')
        wallet.validate(1 if method=='mirror-shift' else 0,'bonus',use_key)
        wallet.pay(1 if method=='mirror-shift' else 0,'bonus',use_key)
        c.appearance=appearance
        if method=='mirror-shift':c.movement_overrides['shift']={movement:30}
        else:c.movement_overrides['advanced']={movement:10}
        return c


def elite_profile(profile,stats):
    """Schema only, including Wizard. Does NOT grant binding/creation/return."""
    require(profile in ELITES and stats.source_class in ('mage','wizard'),'Eligible elite profile source required')
    ac,fixed,mult,speed,reach,damage=ELITES[profile]
    return {'profile':profile,'ac':ac,'maximumHP':fixed+mult*stats.level,'speed':speed,
            'range':reach,'damage':damage,'attack':stats.attack,'dc':stats.dc,
            'statOwner':stats.owner,'sourceClass':stats.source_class}


def validate_elite_assets(assets):
    """All external Mage/Wizard bindings must share this owner/name identity cap."""
    seen=set();counts={}
    for owner,profile,asset_id in assets:
        identity(owner);identity(asset_id);require(profile in ELITES,'Unknown elite identity')
        require((owner,profile) not in seen,'Duplicate named elite across source classes')
        seen.add((owner,profile));counts[owner]=counts.get(owner,0)+1
        require(counts[owner]<=3,'Elite asset cap exceeded')
    return True


def paid_swarm_substitution(*,paid_count,duration,concentration,form_id):
    """Master of Vermin profile substitution only; no creation/resource API."""
    integer(paid_count,'actual paid spell count',1);require_deadline(duration);identity(form_id)
    return {'profile':'swarm','count':paid_count,'expiry':duration,'concentration':concentration,
            'parentForm':None,'additionalCasts':0,'extraCommandAllowance':0}
