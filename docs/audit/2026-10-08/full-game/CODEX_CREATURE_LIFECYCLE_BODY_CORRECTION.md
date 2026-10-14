# Creature physical-body correction — exact final disposition request

Codex → Calibration Review. Your complete105-check implementation review is saved as GPT_CREATURE_LIFECYCLE_IMPLEMENTATION_FINDINGS.md. I corrected the single Ranger body-state blocker and also applied your nonblocking canonical-stat invariant suggestion. Please review these exact corrections against the already-supplied100+5 source set and return an explicit bounded disposition below8,000 characters.

Current verification:121 targeted checks and2,800 Ranger conversion states. Existing device132/1,200 tests and creature source-integrity100+5 remain passing. No original source card/frozen paragraph changed. Every previously accepted command, Auto-Raise, Mirror, Mage and Druid boundary remains as reviewed.

The correction separates one physical body identity from current corpse eligibility:
- Corpse.body_state is living/corpse/consumed/removed; available is a derived read-only property true ONLY for corpse state.
- record_ranger_resurrection is a notification of an ALREADY legally resolved independent source, not a new resurrection ability. It requires actual restoredHP/max and source legality, sets the known body living immediately, makes the real animal unbonded, and restores no bond/uses/rest eligibility.
- Rebond of the same identity now requires that recorded unbonded state and exact current HP ratio; a dead corpse cannot be treated as a living animal through a boolean alone.
- First death registers one body; later genuine death reuses it. Body destruction records removed. Actual consumed/removed bodies cannot return unless the independent source explicitly reconstructs that body. Historical consumed_by provenance remains historical, not current eligibility.
- Added the required death1→resurrection→rebond→death2 test with exactly one identical body record. Also tested eligibility invalidation BEFORE rebond, consumed/removed-body rejection, source-authorized reconstruction, no free post-death rest bypass, malformed HP-ratio rejection and duplicate resurrection rejection.
- S now enforces1–4; M enforces>=1. Ranger continues to use its separate actual WIS modifier, including negatives.

The guide is updated and every full-effect/open-evidence exclusion is retained. Please confirm selected100+5 closure if this resolves the blocker; otherwise give the smallest remaining counterexample. Do not close full forms/tempHP/cards, Wizard elite acquisition/return, global corpse cleanup, Beast rest/HitDice/keen-sense specifics, other companion families, balance/human testing or complete runtime.


## tools/creature_lifecycle_playtest_rules.py
"""Bounded creature lifecycle candidate. Exact implementation review pending.

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

    def fresh(self,ident):
        identity(ident)
        require(ident not in self.creatures,'Creature identity already exists')

    def register_corpse(self,corpse):
        require(corpse.body_id not in self.corpses,'Body identity already registered')
        require(not any(c.creature_id==corpse.creature_id for c in self.corpses.values()),'Fragments/repeated death are not new bodies')
        require(corpse.real_original,'Summoned/copied/raised remains are not corpse fuel')
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


## tools/validate_creature_lifecycle_playtests.py
"""Adversarial state transitions for bounded creature lifecycle interfaces."""
from pathlib import Path
from dataclasses import replace
from copy import deepcopy
import json
from creature_lifecycle_playtest_rules import *
from maximum_hp_playtest_rules import MaxHpRecord
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
    def stats(cls='wizard',owner='owner',level=10):
        return SourceStats(owner,cls,level,4,3,2,7,15,wisdom=3)
    def summon(world,profile='mirror',ident='pet',cls='mirrorsage',**kw):
        sources={'mirror':'mirrorsage.base.mirror-beast-summon','familiar':'mage.arch.conjure-elemental-familiar',
                 'radiant':'mirrorsage.hero.light-weaver.radiant-mirror-beast','swarm':'druid.base.rotshaper.swarm-summoning'}
        args=dict(use_key='summon:'+ident,legal=True,ledger=CommandLedger('owner'))
        if profile=='familiar':args['focus']='fire'
        if profile in ('swarm','radiant'):args['concentration']='conc:'+ident
        args.update(kw)
        return world.summon(sources[profile],(ident,),stats(cls),0,ClockMarker(18),Wallet(20),**args)[0]
    def corpse(world,ident,kind='humanoid',**kw):
        c=Corpse(ident,'original:'+ident,kind,**kw);world.register_corpse(c);return c
    def harvest(world,ident='s',body='body',profile='skeleton',**kw):
        corpse(world,body)
        return world.harvest(ident,body,profile,stats(),Wallet(10),use_key='harvest:'+ident,legal=True,**kw)
    def ranger(world,ident='animal',**kw):
        args=dict(use_key='bond:'+ident,old_hp=7,old_maximum=20,movement_mode='fly',speed=40,keen_sense='smell',
                  legal=True,effects={'disease':'original','injury':'old-scar'})
        args.update(kw)
        return world.bond_ranger(ident,stats('ranger'),Wallet(10),**args)
    def lich(world):return world.unlock_lich(stats('mage'),{p:p for p in ELITES},successful_transformation=True)

    b=CreatureWorld();c=summon(b,mirrorcall=True)
    check('Mirrorcall adjusts creation HP/speed',(c.hp,c.maximum_hp,c.ac,c.speed),(23,23,14,35))
    c.hp=9;c.effects['marked']='persists';c.spent_uses.add('old');c.recharges['x']=6
    b.shift_appearance('pet',1,Wallet(1),method='mirror-shift',appearance='stored bat',movement='climb',use_key='shift1',legal=True)
    check('Appearance never imports anatomy or heals',(c.hp,c.effects,c.spent_uses,c.recharges,c.movement_overrides),(9,{'marked':'persists'},{'old'},{'x':6},{'shift':{'climb':30}}))
    rejects('Mirror Shift cannot grant flight',lambda:b.shift_appearance('pet',1,Wallet(1),method='mirror-shift',appearance='bat',movement='fly',use_key='shift2',legal=True))
    old=deepcopy(c);w=Wallet(1)
    rejects('Insufficient RP cannot dismiss prior Beast',lambda:b.summon('mirrorsage.base.mirror-beast-summon',('new',),stats('mirrorsage'),1,ClockMarker(60),w,use_key='new',legal=True,ledger=CommandLedger('owner')))
    check('Rejected replacement preserves old creature/payment',(c,w.rp),(old,1))
    b.damage('pet',99,2)
    check('Finite zero ends without organic states/corpse',(c.state,len(b.corpses)),('ended',0))
    rejects('Finite corpse cannot be relabeled real',lambda:b.register_corpse(Corpse('fake','pet','humanoid')))
    rejects('Healing cannot resummon ended creature',lambda:b.heal('pet',8,3,legal=True))
    b=CreatureWorld();f=summon(b,'familiar',cls='mage')
    check('Familiar finite profile',(f.hp,f.ac,f.focus,f.effects),(18,16,'fire',{'resistance':'fire'}))
    f.hp=4;f.refresh_maximum(stats('mage',level=20))
    check('Finite base stats remain creation snapshot',(f.hp,f.maximum_hp,f.ac),(4,18,16))
    check('Familiar attacks use current source-owner stats',f.attack_profile(replace(stats('mage'),attack=11))['attack'],11)
    rejects('Temporary controller cannot overwrite stat owner',lambda:f.attack_profile(stats('mage',owner='dominator')))
    f2=summon(b,'familiar','f2','mage',focus='lightning')
    check('New familiar replaces old and uses chosen Focus',(f.state,f2.focus,f2.movement_overrides),('ended','lightning',{'fly':30}))
    b.expire(18,{})
    check('Duration ending produces no corpse',(f2.state,b.corpses),('ended',{}))

    b=CreatureWorld();sw=summon(b,'swarm',cls='druid')
    pair=b.summon('druid.hero.rotshaper.insect-broodmother',('a','b'),stats('druid'),0,ClockMarker(50),Wallet(),
                  use_key='brood/form1',legal=True,parent_form='form1',form_surge_paid=True)
    check('Brood two bodies share one command identity',(len(pair),pair[0].command_group==pair[1].command_group),(2,True))
    ledger=CommandLedger('owner');o=b.command('pair',('a','b'),'attack',1,0,Wallet(),ledger,regular=True,legal=True,capable=True)
    check('Brood pair gets one combined attack',b.resolve_command('pair',1,attached_phase=True,legal=True,capable=True)['attackRolls'],1)
    b.end_dependency(form='form1')
    check('Form end preserves independent Base Swarm',(pair[0].state,pair[1].state,sw.state),('ended','ended','active'))
    b.end_dependency(concentration='conc:pet')
    check('Actual concentration ends independent Swarm',sw.state,'ended')
    sub=paid_swarm_substitution(paid_count=1,duration=ClockMarker(90),concentration='paidspell',form_id='vermin')
    check('Master of Vermin preserves paid spell dependency',(sub['count'],sub['expiry'],sub['parentForm'],sub['additionalCasts']),(1,ClockMarker(90),None,0))
    rejects('Form swarm cannot exceed one minute',lambda:b.summon('druid.hero.rotshaper.carrion-rat-king',('rat',),stats('druid'),0,ClockMarker(61),Wallet(),use_key='rat',legal=True,parent_form='rat-form',form_surge_paid=True))
    rejects('No unpaid Form Surge',lambda:b.summon('druid.hero.rotshaper.insect-broodmother',('x','y'),stats('druid'),0,ClockMarker(60),Wallet(),use_key='brood',legal=True,parent_form='form',form_surge_paid=False))

    b=CreatureWorld();r=ranger(b)
    check('Wounded initial bond is proportional and preserves state',(r.hp,r.maximum_hp,r.effects),(8,23,{'disease':'original','injury':'old-scar'}))
    check('Retained movement is one legal capped mode',(r.movement_mode,r.speed,r.keen_sense),('fly',40,'smell'))
    rejects('Wounded Beast cannot rebond for healing',lambda:ranger(b,'new'))
    r.refresh_maximum(replace(stats('ranger'),level=20,wisdom=4,pb=6))
    check('Ranger growth adds capacity only',(r.hp,r.maximum_hp,r.ac),(8,44,15))
    r.refresh_maximum(replace(stats('ranger'),level=1,wisdom=-5,pb=2))
    check('Actual negative WIS not minimum M',(r.hp,r.maximum_hp,r.ac),(1,1,13))
    outcome=b.damage('animal',1,1)
    check('Ranger zero is actual death without Wound/save',(outcome['state'],outcome['woundRoll'],outcome['deathSave'],len(b.corpses)),('dead',False,False,1))
    rejects('No rebond before completed long rest',lambda:ranger(b,'next'))
    b.completed_long_rest('owner',stats('ranger'),100)
    check('Long rest alone does not resurrect Beast',r.state,'dead')
    rejects('Same animal requires independently legal resurrection',lambda:ranger(b,'animal'))
    body=b.corpses['body:animal'];body_identity=id(body)
    b.record_ranger_resurrection('animal',legal=True,restored_hp=2,restored_maximum=20)
    check('Accepted resurrection immediately removes corpse eligibility before rebond',(r.state,body.available,body.body_state),('unbonded',False,'living'))
    rejects('Living resurrected body cannot be consumed as a corpse',lambda:b.consume_body('body:animal','corpse spell'))
    rejects('Rebond cannot invent healthier post-resurrection ratio',lambda:ranger(b,'animal',resurrected=True,old_hp=20,old_maximum=20,use_key='bond/lr2'))
    r2=ranger(b,'animal',resurrected=True,old_hp=2,old_maximum=20,use_key='bond/lr2')
    check('Resurrected real identity requires full wounded ritual',(r2.instance_id,r2.hp),('animal',2))
    check('Rebond keeps one living body record',(id(body)==body_identity,body.available,len(b.corpses)),(True,False,1))
    b.damage('animal',99,101)
    check('Second genuine death reactivates SAME physical corpse',(id(b.corpses['body:animal'])==body_identity,body.available,body.body_state,len(b.corpses),r2.death_count),(True,True,'corpse',1,2))
    rejects('No duplicated corpse fragments',lambda:b.register_corpse(Corpse('fragment','animal','beast')))
    b.consume_body('body:animal','actual future legal consumer')
    before=deepcopy((body,r2))
    rejects('Ordinary resurrection cannot recreate a consumed body',lambda:b.record_ranger_resurrection('animal',legal=True,restored_hp=1,restored_maximum=20))
    check('Rejected missing-body return is atomic',(body,r2),before)
    b.record_ranger_resurrection('animal',legal=True,restored_hp=1,restored_maximum=20,body_reconstructed=True)
    check('Explicit independent source reconstruction retains physical identity/provenance',(id(body)==body_identity,body.available,body.consumed_by),(True,False,'actual future legal consumer'))
    rejects('Actual resurrection alone does not bypass after-death rest requirement',lambda:ranger(b,'animal',resurrected=True,old_hp=1,old_maximum=20,use_key='bond/lr3'))
    b=CreatureWorld();r=ranger(b);b.damage('animal',99,1,body_survives=False)
    check('Body-destroying death retains unavailable original body identity',(b.corpses['body:animal'].body_state,b.corpses['body:animal'].available),('removed',False))
    rejects('Removed body cannot spontaneously return',lambda:b.record_ranger_resurrection('animal',legal=True,restored_hp=1,restored_maximum=20))
    rejects('Notification cannot itself grant resurrection permission',lambda:b.record_ranger_resurrection('animal',legal=False,restored_hp=1,restored_maximum=20,body_reconstructed=True))
    b.record_ranger_resurrection('animal',legal=True,restored_hp=1,restored_maximum=20,body_reconstructed=True)
    check('Explicit source reconstruction of removed body makes it living not corpse',(r.state,b.corpses['body:animal'].available),('unbonded',False))
    rejects('Duplicate resurrection event cannot refill living animal',lambda:b.record_ranger_resurrection('animal',legal=True,restored_hp=20,restored_maximum=20,body_reconstructed=True))
    rejects('Canonical S cannot exceed4',lambda:replace(stats(),scale=5))
    rejects('Canonical M cannot be0',lambda:replace(stats(),modifier=0))

    b=CreatureWorld();els=lich(b);e=b.creatures['boneflayer']
    e.hp=1;e.spent_uses.add('fear/enc');e.recharges['fear']=12;e.effects['curse']='still applies'
    e.refresh_maximum(stats('mage',level=20))
    check('Elite dynamic capacity does not heal',(e.hp,e.maximum_hp),(1,52))
    b.damage('boneflayer',5,1)
    check('Destroyed elite remains same asset without corpse',(e.state,e.asset_id,len(b.corpses)),('destroyed','boneflayer',0))
    rejects('Destroyed elites still block duplicate unlock',lambda:lich(b))
    oldid=id(e);w=Wallet(5)
    b.soulbound('boneflayer',stats('mage',level=20),w,2,use_key='ritual/lr1',legal=True)
    check('Soulbound restores same identity at half current max',(id(e)==oldid,e.hp,e.temp_hp,e.temp_expiry),(True,26,5,ClockMarker(62)))
    check('Soulbound preserves independent history',(e.spent_uses,e.recharges,e.effects),({'fear/enc'},{'fear':12},{'curse':'still applies'}))
    check('Soulbound pays Action/RP/use',(w.actions,w.rp,w.used),(0,0,{'ritual/lr1'}))
    e.hp=1;b.damage('boneflayer',5,3)
    b.completed_long_rest('owner',stats('mage',level=20),100)
    check('Completed LR returns same elite full without independent reset',(id(e)==oldid,e.hp,e.spent_uses,e.recharges),(True,52,{'fear/enc'},{'fear':12}))
    rejects('Wizard elite cannot use Mage constructor',lambda:CreatureWorld().unlock_lich(stats('wizard'),{p:p for p in ELITES},successful_transformation=True))
    check('Wizard supplied profile remains inspectable',elite_profile('dreadblade',stats())['maximumHP'],46)
    rejects('Cross-class duplicate elite identities invalid',lambda:validate_elite_assets([('owner','boneflayer','mage-bone'),('owner','boneflayer','wizard-bone')]))
    e=b.creatures['wraithbound'];e.offense_event(1)
    check('Wraith attack/control immediately ends invisibility',e.invisible,False)
    e.regular_end(1);check('Wraith remains visible at current marker end',e.invisible,False)
    e.regular_end(2);check('Wraith returns at next proper marker',e.invisible,True)
    rejects('Extra turn cannot supply companion marker',lambda:e.regular_end(3,regular=False))
    rejects('Initiative reordering cannot replay old marker',lambda:e.regular_end(1))

    b=CreatureWorld();s=harvest(b)
    check('Harvest consumes body and uses snapshot stats',(b.corpses['body'].available,s.hp,s.ac),(False,26,14))
    s.hp=3;s.refresh_maximum(stats(level=20))
    check('Standard undead base does not grow with level',(s.hp,s.maximum_hp),(3,26))
    corpse(b,'kill1');b.auto_raise_trigger('s','kill1',1,'attached1','raise1')
    check('Auto-Raise immediately reserves one capacity',b.standard_count('owner'),2)
    harvest(b,'s2','body2')
    corpse(b,'body3');w=Wallet(4)
    rejects('Reserved third slot prevents fourth manual raise',lambda:b.harvest('s3','body3','skeleton',stats(),w,use_key='h3',legal=True))
    check('Over-cap failure preserves payment/body',(w.rp,b.corpses['body3'].available),(4,True))
    b.damage('s',999,2)
    raised=b.auto_raise_checkpoint('attached1',{'owner':stats()},{'raise1':('raised',True,())},2)[0]
    check('Killer destruction does not cancel reserved raise',(raised.profile,raised.blocked_round,raised.state),('skeleton',1,'active'))
    check('New minion cannot even defensive-move/Dodge',b.uncommanded('raised',2,1,capable=True),())
    rejects('Creation-round attack forbidden',lambda:b.command('newattack',('raised',),'attack',1,2,Wallet(),CommandLedger('owner'),regular=True,legal=True,capable=True))
    check('Next numbered round permits defensive behavior',b.uncommanded('raised',2,2,capable=True),('defensive-move','dodge'))
    corpse(b,'later');check('After-checkpoint kill creates no orphan reservation',b.auto_raise_trigger('raised','later',2,'attached1','late'),None)
    check('After-checkpoint rejected trigger leaves later round unused',('owner',2) in b.auto_used,False)
    rejects('Closed checkpoint cannot reopen',lambda:b.auto_raise_checkpoint('attached1',{},{}))
    b.completed_long_rest('owner',stats(),100)
    check('Auto-Raised and harvested standard minions end at LR',(raised.state,b.creatures['s2'].state),('ended','ended'))
    check('No consumed body returns on ending',b.corpses['kill1'].available,False)

    b=CreatureWorld();s=harvest(b);corpse(b,'kill');b.auto_raise_trigger('s','kill',1,'end','r')
    b.consume_body('kill','another legal corpse consumer')
    check('Reservation does not freeze corpse',b.auto_raise_checkpoint('end',{'owner':stats()},{'r':('new',True,())}),())
    check('Failed raise consumes round opportunity and releases slot',(b.auto_used,b.standard_count('owner')),({('owner',1)},1))
    corpse(b,'later');check('Later kill cannot replace failed opportunity',b.auto_raise_trigger('s','later',1,'end2','r2'),None)
    b=CreatureWorld();s=harvest(b)
    corpse(b,'fiend','fiend');check('No Pact means Fiend ineligible',b.auto_raise_trigger('s','fiend',1,'end','r'),None)
    check('Pact enables Fiend Skeleton raise',b.auto_raise_trigger('s','fiend',1,'end','r',pact=True).profile,'skeleton')
    conj=MaxHpRecord('conj','wizard.engine[10]','owner','raised',10)
    rejects('Auto-Raise cannot gain new Conjuration snapshot',lambda:b.auto_raise_checkpoint('end',{'owner':stats()},{'r':('raised',True,(conj,))}))
    check('Invalid modifier preflight preserves reservation/checkpoint',('r' in b.reservations,'end' in b.closed_checkpoints),(True,False))
    b.auto_raise_checkpoint('end',{'owner':stats()},{'r':('raised',True,())})
    b=CreatureWorld();corpse(b,'gob',goblinoid=True)
    g=b.harvest('g','gob','goblin-thrall',stats(),Wallet(4),use_key='h',legal=True)
    corpse(b,'human');check('Goblin Thrall cannot convert ordinary Humanoid',b.auto_raise_trigger('g','human',1,'end','r'),None)
    corpse(b,'devil','fiend');check('Pact does not bypass goblinoid predicate',b.auto_raise_trigger('g','devil',1,'end','r',pact=True),None)
    corpse(b,'gob2',goblinoid=True);check('First qualifying goblinoid kill auto-reserves',b.auto_raise_trigger('g','gob2',1,'end','r').profile,'goblin-thrall')

    b=CreatureWorld();s=harvest(b);ledger=CommandLedger('owner');w=Wallet(2)
    b.command('lash',('s',),'attack',1,0,w,ledger,regular=True,legal=True,capable=True,ghoul_lash=True,adjacent_controlled_undead=True)
    check('Ghoul Lash pays one command plus2RP',(w.rp,w.bonus_action,ledger.rounds[1]),(0,False,{'command':True,'damage':True}))
    check('Ghoul Lash resolves two actual rolls',b.resolve_command('lash',1,attached_phase=True,legal=True,capable=True)['attackRolls'],2)
    rejects('Command cannot resolve twice',lambda:b.resolve_command('lash',1,attached_phase=True,legal=True,capable=True))
    rejects('No Gadget Sync after paid companion offense',lambda:ledger.activate(1,'gadget-sync',Wallet(1),rp=1))
    b=CreatureWorld();lich(b);ledger=CommandLedger('owner');w=Wallet()
    b.command('fear',('boneflayer',),'control',1,0,w,ledger,regular=True,legal=True,capable=True)
    rejects('Non-damaging Mage fear also blocks Gadget Sync',lambda:ledger.activate(1,'gadget-sync',Wallet(1),rp=1))
    check('Invalid resolution loses committed command',b.resolve_command('fear',1,attached_phase=True,legal=False,capable=True)['resolved'],False)
    check('Invalid later target gives no BA refund',w.bonus_action,False)
    rejects('Ordinary command cannot issue on extra turn',lambda:b.command('extra',('boneflayer',),'attack',2,2,Wallet(),CommandLedger('owner'),regular=False,legal=True,capable=True))
    check('Uncommanded living elite has no independent offense',b.uncommanded('boneflayer',1,1,capable=True),('defensive-move','dodge'))

    b=CreatureWorld();c=summon(b,'radiant');ledger=CommandLedger('owner');echoes=EchoLedger('owner',{'rec'});w=Wallet(5)
    before=deepcopy((w,ledger,echoes,c))
    rejects('Echo needs own legal perception/origin before all payment',lambda:b.echo_from_beast('pet',stats('mirrorsage'),1,1,'rec',2,w,ledger,echoes,own_turn=True,legal=False))
    check('Invalid Echo is atomic',(w,ledger,echoes,c),before)
    out=b.echo_from_beast('pet',stats('mirrorsage'),1,1,'rec',2,w,ledger,echoes,own_turn=True,legal=True)
    check('Beast Echo is immediate owner Action with no free movement',(out['resolves'],out['extraBeastMovement'],out['caster']),('immediate owner Action',False,'owner'))
    check('Echo consumes Action BA record and release cap',(w.actions,w.bonus_action,w.rp,echoes.records,echoes.released_rounds),(0,False,3,set(),{1}))
    check('Echo leaves offensive allowance unused',ledger.rounds[1]['damage'],False)
    ledger.activate(1,'gadget-sync',w,rp=1)
    check('Legal later Gadget Sync uses remaining offense',(w.rp,ledger.rounds[1]['damage']),(2,True))
    rejects('Radiant cannot heal after same-round Echo',lambda:b.command('heal',('pet',),'radiant-heal',1,1,Wallet(1),CommandLedger('owner'),regular=True,legal=True,capable=True))
    echoes.records.add('rec2');w=Wallet(2,actions=1,bonus_action=False)
    rejects('Extra Action alone cannot pay Echo BA',lambda:b.echo_from_beast('pet',stats('mirrorsage'),2,2,'rec2',2,w,ledger,echoes,own_turn=True,legal=True))
    check('Missing BA preserves record/RP',(echoes.records,w.rp),({'rec2'},2))
    b.echo_from_beast('pet',stats('mirrorsage'),2,2,'rec2',2,Wallet(2),ledger,echoes,own_turn=True,legal=True)
    check('Actual extra own turn with real BA may Echo',2 in echoes.released_rounds,True)

    b=CreatureWorld();c=summon(b);ledger=CommandLedger('owner');hard=HardDenialLedger();w=Wallet(3)
    bond=b.apply_reflective('owner','original-enemy','charm',ClockMarker(18),'conc',w,ledger,use_key='charm/lr',legal=True,failed_save=True)
    check('Reflective replaces Beast without damaging original target',(c.state,bond.target_id,hard.used),('ended','original-enemy',set()))
    resolution=bond.queue(1,1,'force',Wallet(),ledger,hard,'enc',target_turn_upcoming=False,capable=True,legal=True)
    check('After target already acted queues next round',resolution,2)
    check('BA issue round and offense next round are distinct',(ledger.rounds[1],ledger.reservations),({'command':True,'damage':False},{2:'force'}))
    rejects('Future reservation blocks device offense',lambda:ledger.activate(2,'gadget-sync',Wallet(1),rp=1))
    w=Wallet();before=deepcopy(w)
    rejects('Second pending order fails before payment',lambda:bond.queue(2,2,'force2',w,ledger,hard,'enc',target_turn_upcoming=True,capable=True,legal=True))
    check('Second-order rejection keeps new BA',w,before)
    hard.spend('enc','owner','original-enemy')
    check('Other feature spending hard guard cancels reservation',bond.revalidate_pending(2,ledger,hard,capable=True,legal=True),False)
    check('Canceled order releases offense but not original BA',(ledger.reservations,ledger.rounds[1]['command'],bond.pending),({},True,None))
    rejects('Spent hard guard grants no fallback command',lambda:bond.queue(2,2,'force2',Wallet(),ledger,hard,'enc',target_turn_upcoming=True,capable=True,legal=True))
    check('Charm relation can remain after hard denial spent',bond.operative(2),True)
    b=CreatureWorld();ledger=CommandLedger('owner');hard=HardDenialLedger()
    bond=b.apply_reflective('owner','enemy','charm',ClockMarker(18),'conc',Wallet(3),ledger,use_key='charm/lr',legal=True,failed_save=True)
    bond.queue(0,1,'force',Wallet(),ledger,hard,'enc',target_turn_upcoming=True,capable=True,legal=True)
    rejects('Forced action cannot use a duplicate/extra turn',lambda:bond.resolve(1,1,ledger,hard,actual_regular_action_slot=False,capable=True,legal=True))
    out=bond.resolve(1,1,ledger,hard,actual_regular_action_slot=True,capable=True,legal=True)
    check('One forced normal Action commits hard guard',(out['replacesNormalAction'],out['extraTurn'],hard.used),(True,False,{('enc','owner','enemy')}))
    rejects('Same Charm never grants second forced Action',lambda:bond.queue(2,2,'again',Wallet(),ledger,hard,'enc2',target_turn_upcoming=True,capable=True,legal=True))
    b=CreatureWorld();ledger=CommandLedger('owner');hard=HardDenialLedger()
    bond=b.apply_reflective('owner','enemy','charm',ClockMarker(18),'conc',Wallet(3),ledger,use_key='charm/lr',legal=True,failed_save=True)
    bond.queue(0,1,'force',Wallet(),ledger,hard,'enc',target_turn_upcoming=False,capable=True,legal=True)
    b.end_dependency(concentration='conc',ledger=ledger)
    check('Concentration ending cancels future reservation without hard spend',(bond.active,ledger.reservations,hard.used),(False,{},set()))
    b=CreatureWorld();ledger=CommandLedger('owner');hard=HardDenialLedger()
    bond=b.apply_reflective('owner','enemy','charm',ClockMarker(18),'conc',Wallet(3),ledger,use_key='charm/lr',legal=True,failed_save=True)
    bond.queue(0,1,'force',Wallet(),ledger,hard,'enc',target_turn_upcoming=False,capable=True,legal=True)
    summon(b,ledger=ledger)
    check('Mirror replacement cancels Charm order without killing target',(bond.active,ledger.reservations,hard.used),(False,{},set()))

    states=0
    for level in range(1,21):
        for wisdom in (-5,-1,0,3,5):
            for old_max in (1,7,20):
                for hp in range(1,old_max+1):
                    b=CreatureWorld();st=replace(stats('ranger',level=level),wisdom=wisdom)
                    c=b.bond_ranger('animal',st,Wallet(4),use_key='bond',old_hp=hp,old_maximum=old_max,
                                    movement_mode='walk',speed=30,keen_sense='smell',legal=True)
                    mx=max(1,2*level+wisdom)
                    assert c.hp==max(1,mx*hp//old_max) and 1<=c.hp<=mx
                    before=c.hp;c.refresh_maximum(replace(st,level=20,wisdom=5))
                    assert c.hp==before
                    states+=1
    disposition=json.loads((ROOT/'data/playtest/creature_lifecycle_bindings.json').read_text(encoding='utf-8'))
    result={'result':'PASS','status':disposition['status'],'reviewClosure':disposition.get('reviewClosure'),
            'scope':'100 source roles plus5 frozen supports; selected lifecycle boundaries only, not complete cards/runtime',
            'checkCount':len(checks),'rangerConversionStates':states,'checks':checks}
    (ROOT/'docs/mechanics/CREATURE_LIFECYCLE_PLAYTEST_VALIDATION.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(f'PASS {len(checks)} creature lifecycle checks and {states} Ranger conversion states.')


if __name__=='__main__':main()


## docs/mechanics/CREATURE_LIFECYCLE_PLAYTEST.md
# Creature companions: life, commands and identity

**Implemented candidate; exact GPT implementation review pending.** This overlay discusses 100 exact passages from Druid, Mage, Mirrorsage, Ranger and Wizard, supported by five frozen common paragraphs. It closes no full class, form, temporary-HP system or complete runtime by itself. [Source register](CREATURE_LIFECYCLE_SOURCE_BINDINGS.md), [source integrity](CREATURE_LIFECYCLE_SOURCE_VALIDATION.json), [behavior checks](CREATURE_LIFECYCLE_PLAYTEST_VALIDATION.json).

The original class cards and frozen class guide remain intact. The notebook's first classification, boundary reconciliation and event-model decisions are preserved in the audit folder. Where the historical first reply differs from the later boundary replies, the later explicit resolution controls. In particular, Auto-Raise is automatic, its new minion cannot act at all in the creation round, and Mirrorsage Charm was not in the older 219-source control closure.

## At the table

Keep one companion command and one offensive companion allowance per owner per numbered round, including multiclass companions and devices. A normal command costs your Bonus Action. A damaging companion action, or Mage/Wizard control action, spends the offensive allowance. A pure support command spends only the command. The earlier device ledger's internal field named `damage` now represents this shared offensive allowance; its public behavior remains compatible with existing device checks.

Issue ordinary commands during your regular turn. The selected companion moves and performs its command immediately after your whole turn, in an attached phase. It receives no extra independent turn. If it or its target becomes ineligible before execution, the command fails without refund. Your later incapacity or removal alone does not cancel an issued command; actual concentration/source ending can. Uncommanded companions can move defensively and Dodge, subject to their conditions; this grants no generic Reaction or autonomous attack/control.

Use the owner's original regular companion markers for recharge and previous/next-turn references. Extra turns, initiative changes and removal do not restart those markers. The attached phase's event-resolution checkpoint is distinct: it refreshes no Reaction, recharge, Action, death save or regular duration clock.

## Different kinds of creature life

| Creature | HP and 0 HP | Return and identity |
|---|---|---|
| Finite standard summons, Druid swarms, Mage Familiar, Mirror Beasts | HP-only bounded layer; at 0 disappear/end | No corpse, resource or free resummon; a new summon pays its actual source costs |
| Ranger Beast | HP-only; **NEW** immediate death at 0, no Wound checks, Stable or death saves | Actual animal and ordinary surviving corpse; death ends bond. No automatic resurrection or rebond |
| Mage Lich elite | Destroyed bound asset at 0; no usable corpse/resources | Same unique asset remains owned. Soulbound or actual completed LR can return it |
| Wizard standard undead | Destroyed at 0; consumed body never returns as new fuel | Ends on destruction, dismissal or owner's next completed LR, including Auto-Raised minions |
| Wizard elite | Supplied profile/cap only in this package | Binding/acquisition and return procedure are still missing; no create/bind/return API |
| Reflective Companion | Original creature's HP and life rules | Temporary control relation; no copied body, reset, new statistics or duplicate turn |
| Druid form | Same character's HP/life rules | Full forms and Buffer Reserve remain a separate open interface |

Companion healing restores legal normal HP only. It does not reset identity, duration, recharge, actions, source uses, effects or command budgets. Ranger's “heal normally” supplies no Hit Dice pool or automatic rest healing. The HP-only layer is specific to this reviewed companion chassis, not generic law for all animals/NPCs. Existing animal conditions, disease, poison, explicit injuries and timed effects survive bonding.

## Stats and ownership

**NEW:** finite created creatures snapshot base HP and AC at creation. Attacks, saves, class DC and S use the current values of the original source owner at resolution. Keep source owner, current controller, source class and creation source separate. A temporary controller does not donate their class levels, PB or attack bonus. The implementation rejects stats belonging to another owner/class; it provides no unrestricted transfer/rebinding operation.

Standard profile: AC 12 + floor(PB/2), HP 2L, Speed 30, owner PB for saves, one class attack for S d6 with printed melee/ranged mode. Druid swarm uses current PB+WIS, piercing and its printed tiny-gap movement. Familiar snapshots AC 12+PB and HP 5+Mage level+M; its current source-owner Mage attack fires a 30-foot Elemental Dart for S d4. Focus is fixed at creation: Lightning adds Fly30, Fire/Cold their matching resistance. Changing Focus neither morphs nor refills it. One Familiar; replacement ends the prior one.

Ranger maximum is **NEW dynamic** max(1, 2×current Ranger level + actual WIS modifier), not M. Current PB updates its standard AC/saves/attack. Persistent Mage elite maxima use current source-owner Mage level; fixed AC stays fixed. Capacity growth never heals; shrink clamps HP without damage. Wizard elite profiles use the same names with their own original Wizard source statistics if a future legitimate binding source establishes them.

The [reviewed maximum-HP ledger](MAXIMUM_HP_PLAYTEST.md) supplies source-qualified modifiers. Conjuration is the original creating Wizard level snapshot and requires actual Wizard spell creation. Corpse Harvest qualifies only with actual access; Auto-Raise is not a spell and grants no new Conjuration snapshot. Flesh Ascendant is the explicit dynamic eligible-current-controller exception; engine and card are one effect, not two bonuses. Creation starts at full final legal maximum unless the actual source enters damaged; later added capacity never fills HP. Callers update dynamic modifier records from their real sources.

## Ranger's persistent bond

Use the printed one-hour ritual, touch, 4 RP and one long-rest use. The animal must already be willing/tamed, noncorrupted, INT below7 and CR no greater than Ranger level. The helper does not invent finding/taming rules. Keep one chosen movement mode, capped40 feet, and the original keen-sense identity; no monster stat block, boss powers or free special actions. Exact keen-sense selection definitions remain an evidence gap.

**NEW initial conversion:** for a living animal, new HP = max(1, floor(new maximum × old current HP / old maximum)). A wounded animal stays proportionally wounded. This is profile conversion, not healing or damage. A living bound Beast cannot be rebonded to refill HP. On death, ordinary legal resurrection may restore the same animal under its own source, but it remains unbonded. A new full ritual also requires an actual completed long rest after bond death.

Physical body identity is separate from current corpse eligibility. Keep one record whose state is living, corpse, consumed or removed. Accepting an already-resolved, independently legal resurrection immediately marks that same body living and unavailable as a corpse, before any rebond. Corpse Gateway cannot use it while living. A later genuine death with a surviving body makes that same record a corpse again; no fragment/new body identity is generated. A consumed/removed body requires explicit reconstruction by the actual resurrection source before it can return. The notification helper grants no resurrection ability, payment exemption or automatic bond. Rebond uses the actual post-resurrection HP ratio and preserves death history; it cannot claim a healthier ratio. Full global corpse decay/cleanup remains open.

## Mage Lich assets and elite commands

An actual successful Lich transformation unlocks Boneflayer, Dreadblade and Wraithbound. Readiness and informed retirement-risk consent are source guards; this lifecycle helper does not perform that irreversible ritual. **NEW shared identity:** across Mage/Wizard, one owner can have at most one of each named elite and three total. Destroyed assets still occupy those identities. Any future external Wizard binding must validate against the same asset register; the current helper offers only its profile schema.

| Elite | Profile | Source-native actions/riders |
|---|---|---|
| Boneflayer | AC14, HP12+2L, Speed30; ranged60, 2d6+S necrotic | Fear Pulse replaces attack, enemies10 feet WIS or Frightened through target-next-end, recharge3. Grave Miasma replaces attack: radius10 point30 until next owner-start, enemies entry/start1d6 once, recharge3 |
| Dreadblade | AC16, HP16+3L, Speed30; melee5, 1d8+S necrotic | Concentrating hit target immediately saves with disadvantage; natural20 applies printed −1 attack Weakened until target-next-end. Advantage against forced movement |
| Wraithbound | AC14, HP10+2L, Fly40/hover; melee5, 1d8+S necrotic | Natural20 CON or Stunned until target-next-end under shared character→target hard-denial guard |

Rolls, chosen enemy geometry, recharge payments, exact condition applications and canonical hard-guard sharing remain caller/source responsibilities. This helper returns attack profiles and bounded lifecycle/command transitions; it does not silently execute every on-hit effect.

**NEW Miasma integration:** creation spends one offensive command. Its native finite entry/start damage needs no second command and does not spend next round's offense. Retain no-resource/no-recursion flags. An old zone tick is not a new companion turn or attack.

Wraithbound loses source invisibility on attack **or control**. It can regain it at the end of its next original regular companion marker if the predicate remains satisfied. A current-marker end cannot immediately restore it. The actual offense event must notify its marker state. Core Invisible still does not grant unknown location, sight through walls or automatic target legality.

Soulbound requires the destroyed own bound elite within30 or its inert token, legal empty space30, Action, 5 RP and one LR use. Return the same asset/instance at **NEW source-specific** max(1, floor(current maximum/2)), plus S+M temp HP for60 seconds under normal temp-HP rules. Do not copy machine reconstruction permissions. Preserve spent uses, recharge clocks, command history and still-applicable effects. Completed LR returns those same Mage assets at full current HP unless an actual campaign consequence prevents it. Rest-use/recharge resets come only from the canonical rest system; a return itself grants none. Natural effect expiries must still be processed.

## Wizard corpses, standard minions and Auto-Raise

Corpse Harvest costs Action+4 RP, recharge2, legal corpse/space30. Humanoids qualify; actual Infernal Pact also permits Fiends. Skeleton: AC14, HP6+2WizardL, Speed30, ranged30 1d6+S necrotic. Zombie: AC12, HP10+3L, Speed20, melee5 1d8+S. Goblin Thrall: AC13, HP8+2L, Speed30, melee5 1d6+S; requires a goblinoid body even with Pact.

All standard minions and reserved Auto-Raise slots share a cap of3. Manually dismiss an existing standard minion before attempting a fourth; failed creation spends nothing and does not consume the body. Harvest consumes the original body. Summoned, raised, copied, illusory or fragmented remains provide no new corpse fuel. Corpse Gateway uses a legal body without consuming it; it does not grant raising permission. Global corpse decay/removal rules remain open.

Ghoul Lash uses the shared BA command and2 RP with another controlled undead within5 at issuance. Its chosen standard minion makes **two independently rolled normal attacks**, not numerical damage copies. Each can miss/hit/crit. This remains one command and one offensive allowance, with at most one Auto-Raise opportunity.

**NEW queue integration, preserving the printed automatic trigger:** the first qualifying personal killing blow by a standard minion automatically reserves the body, one capacity slot and the killer's mechanical minion type. It spends the owner's round opportunity immediately. Ineligible kills do not spend it; a qualifying trigger cannot voluntarily be declined. Body reservation does not prevent another legal consumer from taking the body first. A destroyed/expired killer does not cancel an already-created reservation.

Resolve after immediate death responses and already-due end damage/saves, before ordinary expiry cleanup, in stable application order. An ordinary attached attack has its own `attachedCompanionEnd` queue checkpoint after its consequences, in the same numbered round. That checkpoint is not a second regular turn marker. Kills before the checkpoint closes may reserve. A later administrative kill cannot reopen it, roll forward or leave an orphan queue; its unused opportunity remains unused unless another independently valid trigger occurs before another legally open checkpoint.

At resolution, still-eligible body, legal space and cap permit creation; otherwise release the reservation but retain the spent round use. Auto-Raise costs no Action or RP. The newborn cannot voluntarily move, Dodge, support, attack, control or react in its creation numbered round. Passive defenses/conditions/expiry continue. It ends at destruction, dismissal or next completed owner LR. Owner unconsciousness/death alone does not invent a new ending.

## Mirror Beast, Reflective Companion and Echo origin

One Mirror Beast **or** Reflective Companion slot. Summoning a Beast replaces the old body/control relation administratively; it never kills the real previously controlled target. Mirrorcall adds M max/current HP at creation and5 Speed. Advanced Mirrorcall spends BA once/encounter for appearance plus its printed swim/climb adjustment; Mirror Shift spends BA+1 RP/recharge2 for swim30 or climb30. Neither heals, restores uses, releases Echoes, grants flight/anatomy, or refreshes duration. Corrupted and Shattered on-hit dice/splash retain their exact once-round source qualifiers; full damage-event execution remains in the later copy/trigger work. Luminant Bond supplies only its printed local WIS-save/Invisible advantage interface, with ordinary cover/targeting intact.

Ordinary Beast: Action2 RP, empty space15, one minute, recharge3. Radiant/Shattered: Action4 RP, empty space15, concentration3 of the owner's regular turns, recharge4. Actual scheduler supplies the precise three-turn endpoint. Radiant chooses attack, BA+1 RP heal S d4 to living ally5, or paid Echo origin, once per numbered round. The healing pipeline resolves rolls/modifiers before the lifecycle HP gain; no invented resurrection.

**NEW Mirror-origin exception:** your Echo resolves immediately as your Action during your own turn, including a real extra own turn if real Action, BA and unused shared caps exist. An extra Action alone supplies no BA. Preflight active Beast, actual record, release cap, owner target perception, current Beast range/LOE, Action, BA and RP before any spend. The Beast grants no remote sensory feed or free preceding movement. You own record consumption, Dissonance, Refrain, concentration and spell damage. BA command is spent; offensive companion allowance is not. A later independently legal Gadget Sync may spend it. No second BA command or second local Beast option appears.

Charm Creature remains Action3 RP, one LR use, WIS save, target INT<=6 within30, concentration at most3 rounds, no PC/boss without actual encounter permission. Repeat save at target's actual turn end and when harmed by your side. No suicide, compelled beliefs or permanent allegiance. Original identity/HP/conditions/effects/stat provenance/initiative remain unchanged. A successful save spends cast costs but does not replace an existing Beast. Source-specific save/Charm immunity and permitted target/route checks remain caller responsibilities.

**NEW hard-denial reconciliation:** initial Charm applies the actual Charmed relation and slot without spending hard denial. While active, one BA may queue at most one pending forced ordinary Action, never unique powers; ordinary attack damage capped S d6. Queue to the next future regular target Action: this round if upcoming, next round if already passed. Pay BA in issue round; reserve offensive allowance in the resolution round. The target receives no duplicate attached turn.

At the designated Action slot, revalidate Charm, capability, legal order and the shared character→target→encounter hard guard. Valid execution replaces that Action and spends both hard guard and offense. If Charm ends, target becomes incapable, legality fails or another same-character feature spends hard denial, cancel and release unused offense; retain BA/costs and do not spend an additional hard denial. Call the pending-order revalidation when those facts change, not only at the future turn. Once a forced Action has occurred, this effect permits no further forced attack, Dodge, movement or replacement Action. Actual Charmed restrictions/repeat saves remain; no new fallback is invented.

## Druid summon dependencies

Base Swarm Summoning: Action, one SR use, space30, concentration10 minutes; independent of form. Carrion Rat King: Action, actual Form Surge, once per shift, one standard swarm for at most60 seconds and only while its parent form remains; replacement affects its old form swarm, not independent Base Swarm. Broodmother: on entry actual Form Surge creates two adjacent bodies with one combined commanded attack; end at the earlier of60 seconds or parent form end. Form change ends those children, not unrelated paid summons.

Master of Vermin substitutes the paid summoning spell's profile while preserving its actual count, duration and concentration. No extra casts, creatures or command budget. Its independently paid spell creatures do not inherit a form-ending dependency solely from that substitution. Full forms, reserve arithmetic, per-form special actions and temporary-HP effects remain open.

## Reference boundaries and next work

The helper requires certified source access, legal target/space/range/LOE/perception, ordinary condition capability, real paid Form Surge, canonical action wallets/use scopes, actual concentration/clock endpoints and actual completed rest events. These are explicit inputs, not guessed by creature names. A fresh wallet/ledger per ability is invalid integration. Recharge/frequency keys represent already validated canonical scopes; caller must not mint a new key to bypass them.

Open: Wizard elite binding/return, real Beast natural rest and keen-sense details, global corpse cleanup, broader companion families, full forms/tempHP, complete damage/copy/proc execution, ordinary spell and content catalogs, human balance and complete runtime. Classification of incidental source passages is not closure of their complete effects.


## docs/mechanics/CREATURE_LIFECYCLE_PLAYTEST_VALIDATION.json
{
  "result": "PASS",
  "status": "IMPLEMENTED CANDIDATE; exact selected-interface review pending; incidental form/tempHP effects deferred",
  "reviewClosure": null,
  "scope": "100 source roles plus5 frozen supports; selected lifecycle boundaries only, not complete cards/runtime",
  "checkCount": 121,
  "rangerConversionStates": 2800,
  "checks": [
    {
      "name": "Mirrorcall adjusts creation HP/speed",
      "result": "PASS"
    },
    {
      "name": "Appearance never imports anatomy or heals",
      "result": "PASS"
    },
    {
      "name": "Mirror Shift cannot grant flight",
      "result": "PASS"
    },
    {
      "name": "Insufficient RP cannot dismiss prior Beast",
      "result": "PASS"
    },
    {
      "name": "Rejected replacement preserves old creature/payment",
      "result": "PASS"
    },
    {
      "name": "Finite zero ends without organic states/corpse",
      "result": "PASS"
    },
    {
      "name": "Finite corpse cannot be relabeled real",
      "result": "PASS"
    },
    {
      "name": "Healing cannot resummon ended creature",
      "result": "PASS"
    },
    {
      "name": "Familiar finite profile",
      "result": "PASS"
    },
    {
      "name": "Finite base stats remain creation snapshot",
      "result": "PASS"
    },
    {
      "name": "Familiar attacks use current source-owner stats",
      "result": "PASS"
    },
    {
      "name": "Temporary controller cannot overwrite stat owner",
      "result": "PASS"
    },
    {
      "name": "New familiar replaces old and uses chosen Focus",
      "result": "PASS"
    },
    {
      "name": "Duration ending produces no corpse",
      "result": "PASS"
    },
    {
      "name": "Brood two bodies share one command identity",
      "result": "PASS"
    },
    {
      "name": "Brood pair gets one combined attack",
      "result": "PASS"
    },
    {
      "name": "Form end preserves independent Base Swarm",
      "result": "PASS"
    },
    {
      "name": "Actual concentration ends independent Swarm",
      "result": "PASS"
    },
    {
      "name": "Master of Vermin preserves paid spell dependency",
      "result": "PASS"
    },
    {
      "name": "Form swarm cannot exceed one minute",
      "result": "PASS"
    },
    {
      "name": "No unpaid Form Surge",
      "result": "PASS"
    },
    {
      "name": "Wounded initial bond is proportional and preserves state",
      "result": "PASS"
    },
    {
      "name": "Retained movement is one legal capped mode",
      "result": "PASS"
    },
    {
      "name": "Wounded Beast cannot rebond for healing",
      "result": "PASS"
    },
    {
      "name": "Ranger growth adds capacity only",
      "result": "PASS"
    },
    {
      "name": "Actual negative WIS not minimum M",
      "result": "PASS"
    },
    {
      "name": "Ranger zero is actual death without Wound/save",
      "result": "PASS"
    },
    {
      "name": "No rebond before completed long rest",
      "result": "PASS"
    },
    {
      "name": "Long rest alone does not resurrect Beast",
      "result": "PASS"
    },
    {
      "name": "Same animal requires independently legal resurrection",
      "result": "PASS"
    },
    {
      "name": "Accepted resurrection immediately removes corpse eligibility before rebond",
      "result": "PASS"
    },
    {
      "name": "Living resurrected body cannot be consumed as a corpse",
      "result": "PASS"
    },
    {
      "name": "Rebond cannot invent healthier post-resurrection ratio",
      "result": "PASS"
    },
    {
      "name": "Resurrected real identity requires full wounded ritual",
      "result": "PASS"
    },
    {
      "name": "Rebond keeps one living body record",
      "result": "PASS"
    },
    {
      "name": "Second genuine death reactivates SAME physical corpse",
      "result": "PASS"
    },
    {
      "name": "No duplicated corpse fragments",
      "result": "PASS"
    },
    {
      "name": "Ordinary resurrection cannot recreate a consumed body",
      "result": "PASS"
    },
    {
      "name": "Rejected missing-body return is atomic",
      "result": "PASS"
    },
    {
      "name": "Explicit independent source reconstruction retains physical identity/provenance",
      "result": "PASS"
    },
    {
      "name": "Actual resurrection alone does not bypass after-death rest requirement",
      "result": "PASS"
    },
    {
      "name": "Body-destroying death retains unavailable original body identity",
      "result": "PASS"
    },
    {
      "name": "Removed body cannot spontaneously return",
      "result": "PASS"
    },
    {
      "name": "Notification cannot itself grant resurrection permission",
      "result": "PASS"
    },
    {
      "name": "Explicit source reconstruction of removed body makes it living not corpse",
      "result": "PASS"
    },
    {
      "name": "Duplicate resurrection event cannot refill living animal",
      "result": "PASS"
    },
    {
      "name": "Canonical S cannot exceed4",
      "result": "PASS"
    },
    {
      "name": "Canonical M cannot be0",
      "result": "PASS"
    },
    {
      "name": "Elite dynamic capacity does not heal",
      "result": "PASS"
    },
    {
      "name": "Destroyed elite remains same asset without corpse",
      "result": "PASS"
    },
    {
      "name": "Destroyed elites still block duplicate unlock",
      "result": "PASS"
    },
    {
      "name": "Soulbound restores same identity at half current max",
      "result": "PASS"
    },
    {
      "name": "Soulbound preserves independent history",
      "result": "PASS"
    },
    {
      "name": "Soulbound pays Action/RP/use",
      "result": "PASS"
    },
    {
      "name": "Completed LR returns same elite full without independent reset",
      "result": "PASS"
    },
    {
      "name": "Wizard elite cannot use Mage constructor",
      "result": "PASS"
    },
    {
      "name": "Wizard supplied profile remains inspectable",
      "result": "PASS"
    },
    {
      "name": "Cross-class duplicate elite identities invalid",
      "result": "PASS"
    },
    {
      "name": "Wraith attack/control immediately ends invisibility",
      "result": "PASS"
    },
    {
      "name": "Wraith remains visible at current marker end",
      "result": "PASS"
    },
    {
      "name": "Wraith returns at next proper marker",
      "result": "PASS"
    },
    {
      "name": "Extra turn cannot supply companion marker",
      "result": "PASS"
    },
    {
      "name": "Initiative reordering cannot replay old marker",
      "result": "PASS"
    },
    {
      "name": "Harvest consumes body and uses snapshot stats",
      "result": "PASS"
    },
    {
      "name": "Standard undead base does not grow with level",
      "result": "PASS"
    },
    {
      "name": "Auto-Raise immediately reserves one capacity",
      "result": "PASS"
    },
    {
      "name": "Reserved third slot prevents fourth manual raise",
      "result": "PASS"
    },
    {
      "name": "Over-cap failure preserves payment/body",
      "result": "PASS"
    },
    {
      "name": "Killer destruction does not cancel reserved raise",
      "result": "PASS"
    },
    {
      "name": "New minion cannot even defensive-move/Dodge",
      "result": "PASS"
    },
    {
      "name": "Creation-round attack forbidden",
      "result": "PASS"
    },
    {
      "name": "Next numbered round permits defensive behavior",
      "result": "PASS"
    },
    {
      "name": "After-checkpoint kill creates no orphan reservation",
      "result": "PASS"
    },
    {
      "name": "After-checkpoint rejected trigger leaves later round unused",
      "result": "PASS"
    },
    {
      "name": "Closed checkpoint cannot reopen",
      "result": "PASS"
    },
    {
      "name": "Auto-Raised and harvested standard minions end at LR",
      "result": "PASS"
    },
    {
      "name": "No consumed body returns on ending",
      "result": "PASS"
    },
    {
      "name": "Reservation does not freeze corpse",
      "result": "PASS"
    },
    {
      "name": "Failed raise consumes round opportunity and releases slot",
      "result": "PASS"
    },
    {
      "name": "Later kill cannot replace failed opportunity",
      "result": "PASS"
    },
    {
      "name": "No Pact means Fiend ineligible",
      "result": "PASS"
    },
    {
      "name": "Pact enables Fiend Skeleton raise",
      "result": "PASS"
    },
    {
      "name": "Auto-Raise cannot gain new Conjuration snapshot",
      "result": "PASS"
    },
    {
      "name": "Invalid modifier preflight preserves reservation/checkpoint",
      "result": "PASS"
    },
    {
      "name": "Goblin Thrall cannot convert ordinary Humanoid",
      "result": "PASS"
    },
    {
      "name": "Pact does not bypass goblinoid predicate",
      "result": "PASS"
    },
    {
      "name": "First qualifying goblinoid kill auto-reserves",
      "result": "PASS"
    },
    {
      "name": "Ghoul Lash pays one command plus2RP",
      "result": "PASS"
    },
    {
      "name": "Ghoul Lash resolves two actual rolls",
      "result": "PASS"
    },
    {
      "name": "Command cannot resolve twice",
      "result": "PASS"
    },
    {
      "name": "No Gadget Sync after paid companion offense",
      "result": "PASS"
    },
    {
      "name": "Non-damaging Mage fear also blocks Gadget Sync",
      "result": "PASS"
    },
    {
      "name": "Invalid resolution loses committed command",
      "result": "PASS"
    },
    {
      "name": "Invalid later target gives no BA refund",
      "result": "PASS"
    },
    {
      "name": "Ordinary command cannot issue on extra turn",
      "result": "PASS"
    },
    {
      "name": "Uncommanded living elite has no independent offense",
      "result": "PASS"
    },
    {
      "name": "Echo needs own legal perception/origin before all payment",
      "result": "PASS"
    },
    {
      "name": "Invalid Echo is atomic",
      "result": "PASS"
    },
    {
      "name": "Beast Echo is immediate owner Action with no free movement",
      "result": "PASS"
    },
    {
      "name": "Echo consumes Action BA record and release cap",
      "result": "PASS"
    },
    {
      "name": "Echo leaves offensive allowance unused",
      "result": "PASS"
    },
    {
      "name": "Legal later Gadget Sync uses remaining offense",
      "result": "PASS"
    },
    {
      "name": "Radiant cannot heal after same-round Echo",
      "result": "PASS"
    },
    {
      "name": "Extra Action alone cannot pay Echo BA",
      "result": "PASS"
    },
    {
      "name": "Missing BA preserves record/RP",
      "result": "PASS"
    },
    {
      "name": "Actual extra own turn with real BA may Echo",
      "result": "PASS"
    },
    {
      "name": "Reflective replaces Beast without damaging original target",
      "result": "PASS"
    },
    {
      "name": "After target already acted queues next round",
      "result": "PASS"
    },
    {
      "name": "BA issue round and offense next round are distinct",
      "result": "PASS"
    },
    {
      "name": "Future reservation blocks device offense",
      "result": "PASS"
    },
    {
      "name": "Second pending order fails before payment",
      "result": "PASS"
    },
    {
      "name": "Second-order rejection keeps new BA",
      "result": "PASS"
    },
    {
      "name": "Other feature spending hard guard cancels reservation",
      "result": "PASS"
    },
    {
      "name": "Canceled order releases offense but not original BA",
      "result": "PASS"
    },
    {
      "name": "Spent hard guard grants no fallback command",
      "result": "PASS"
    },
    {
      "name": "Charm relation can remain after hard denial spent",
      "result": "PASS"
    },
    {
      "name": "Forced action cannot use a duplicate/extra turn",
      "result": "PASS"
    },
    {
      "name": "One forced normal Action commits hard guard",
      "result": "PASS"
    },
    {
      "name": "Same Charm never grants second forced Action",
      "result": "PASS"
    },
    {
      "name": "Concentration ending cancels future reservation without hard spend",
      "result": "PASS"
    },
    {
      "name": "Mirror replacement cancels Charm order without killing target",
      "result": "PASS"
    }
  ]
}


## docs/mechanics/CREATURE_LIFECYCLE_SOURCE_VALIDATION.json
{
  "result": "PASS",
  "exactClassRecords": 100,
  "originalInventoryCandidates": 83,
  "semanticSupplements": 17,
  "frozenSharedParagraphs": 5,
  "scope": "Exact source equality/hash only; not classification or semantic approval.",
  "issues": []
}

