"""Bounded Cleric/Oracle/Paladin/Soldier lifecycle reference, not a runtime.

Share CreatureWorld (physical bodies), Wallet, CommandLedger, HardDenialLedger,
ExtraActionClock and IncomingAttacks across all abilities. The caller certifies
source access, placement/targets/agency, exact deadlines, recharge/reset scopes,
ordinary rolls/defenses and native creature zero-HP handling. A true legality
flag is an assertion of those checks, never an authorization invented here.
"""
from dataclasses import dataclass, field
from copy import deepcopy
from creature_lifecycle_playtest_rules import Creature, CreatureWorld, Corpse, require, HardDenialLedger
from device_lifecycle_playtest_rules import Wallet, CommandLedger
from combat_playtest_rules import ExtraActionClock
from control_playtest_rules import ClockMarker, clock_marker, require_deadline
from spell_playtest_rules import SpellRuleError, integer
from redirection_playtest_rules import identity

CHOIR='cleric.hero.cultist.rite-of-the-crimson-choir'
RITUAL='cleric.hero.cultist.ritual-of-undeath'
UNBOUND='oracle.supplement.bones.ledger-unbound'
LEDGER='oracle.supplement.bones.ledger-s-command'
TURRET='soldier.hero.artillerist.turret-deployment'
PALISADE='soldier.arch.palisade-deployment'
QUICK='soldier.base.quick-deploy'
ZONES=frozenset(('soldier.hero.artillerist.bubble-of-discipline',
                'soldier.arch.fortify-zone','soldier.hero.champion.wall-of-aegis'))


@dataclass(frozen=True)
class Stats:
    owner: str
    source_class: str
    level: int
    pb: int
    scale: int
    modifier: int
    attack: int
    dc: int
    constitution: int=0
    dexterity: int=0
    charisma: int=0

    def __post_init__(self):
        identity(self.owner)
        require(self.source_class in ('cleric','oracle','paladin','soldier'),'Wrong source class')
        integer(self.level,'class level',1,20);integer(self.pb,'PB',1)
        integer(self.scale,'S',1,4);integer(self.modifier,'M',1)
        for v in (self.attack,self.dc,self.constitution,self.dexterity,self.charisma):
            require(type(v) is int,'Actual modifier must be an integer')


def deadline(now,expiry,seconds):
    now=clock_marker(now);require_deadline(expiry)
    require(now<expiry and expiry.seconds-now.seconds<=seconds,'Invalid printed deadline')


@dataclass
class Points:
    """Adapter to the canonical class resource balance (Conviction or RC)."""
    owner: str
    resource: str
    value: int

    def validate(self,owner,resource,cost):
        require((self.owner,self.resource)==(owner,resource),'Wrong resource ledger')
        integer(self.value,'class resource',0);integer(cost,'class resource cost',0)
        require(self.value>=cost,'Insufficient class resource')


@dataclass
class RemainingCreature(Creature):
    position: object=None
    explosion_settled: bool=False
    local_modes: dict=field(default_factory=dict)

    def attack_profile(self,stats):
        self.verify_stats(stats)
        out={'sourceOwner':self.source_owner,'sourceClass':self.source_class,
             'attack':stats.attack,'saves':stats.pb,'saveDC':stats.dc,
             'range':5,'mode':'melee','damageType':'necrotic','attackerOwnResourcePool':False}
        if self.profile=='choir':out['damage']=(1,6,stats.scale)
        elif self.profile=='thrall':out['damage']=(stats.scale,6,0)
        elif self.profile=='bone-servant':out['damage']=(1,8,stats.scale)
        elif self.profile=='soldier-turret':
            out.update(attack=stats.pb+stats.dexterity,range=60,mode='ranged',
                       damage=(1,6,stats.modifier),damageType='piercing')
        else:raise SpellRuleError('Unregistered remaining companion profile')
        return out


@dataclass
class Structure:
    instance_id: str
    owner: str
    kind: str
    maximum_hp: int
    hp: int
    expiry: ClockMarker | None=None
    area_resistance: bool=False
    state: str='intact'
    ac: int=12

    def active(self,now):
        return self.state=='intact' and self.hp>0 and (self.expiry is None or clock_marker(now)<self.expiry)


@dataclass
class Supplies:
    owner: str
    kits: int=2
    field_supplies: int=0
    spare_parts: int=0
    deployments: dict=field(default_factory=dict)
    repaired: set=field(default_factory=set)

    def validate(self,owner):
        require(self.owner==owner,'Wrong material inventory')
        integer(self.kits,'carried kits',0,2)
        integer(self.field_supplies,'actual field supply uses',0)
        integer(self.spare_parts,'actual spare-part uses',0)

    def completed_rest(self,*,completed,carpentry):
        self.validate(self.owner)
        require(completed and carpentry,'Actual completed long rest and carpentry tools required')
        self.kits=2


@dataclass
class IncomingAttacks:
    """Canonical post-hit/pre-consequence windows, keyed by real attack identity."""
    closed: set=field(default_factory=set)

    def validate(self,attack_id,*,successful_single_target_hit,pre_consequences,legal):
        identity(attack_id)
        require(successful_single_target_hit and pre_consequences and legal,'No legal interception window')
        require(attack_id not in self.closed,'Attack already intercepted/resolved')

    def commit(self,attack_id,target):
        self.closed.add(attack_id)
        return {'attackId':attack_id,'zeroAssignmentTarget':target,'oracleDamage':0,
                'oracleOnHit':False,'newAttackRoll':False,'transferredDamage':False,
                'damageEvent':False,'resourceEvent':False,'duplicateBody':False,
                'nativeZeroLifecycleRequired':True}


@dataclass
class ExistingUndeadBuff:
    owner: str
    members: frozenset
    expiry: ClockMarker
    first_damage: set=field(default_factory=set)

    def operative(self,target,now,*,controlled):
        return controlled and target in self.members and clock_marker(now)<self.expiry

    def attack_bonus(self,target,now,scale,*,controlled,commanded):
        integer(scale,'S',1,4)
        return scale if commanded and self.operative(target,now,controlled=controlled) else 0

    def first_damage_offer(self,target,now,round_number,*,controlled,qualifying):
        integer(round_number,'numbered round',1)
        key=(target,round_number)
        if not qualifying or not self.operative(target,now,controlled=controlled) or key in self.first_damage:return 0
        self.first_damage.add(key)
        return 1  # Consume before strongest-only arbitration, even if another DR wins.


class RemainingWorld:
    def __init__(self,physical_world):
        self.physical=physical_world
        self.structures={};self.orders={};self.choirs={};self.choir_healing={}
        self.hit_events=set();self.unbound_buffs={};self.synergy_turns=set()

    def fresh(self,ident):
        self.physical.fresh(ident)
        require(ident not in self.structures,'Object identity already exists')

    def create(self,ident,stats,source,profile,hp,ac,speed,expiry,**kwargs):
        return RemainingCreature(ident,stats.owner,stats.owner,stats.source_class,source,profile,
                                 'finite',hp,hp,hp,ac,speed,expiry=expiry,**kwargs)

    def choir(self,application,ids,positions,stats,now,expiry,wallet,conviction,*,use_key,legal,concentration):
        identity(application);require(application not in self.choirs,'Application reused')
        require(stats.source_class=='cleric' and legal and concentration,'Choir source/placement/concentration required')
        require(len(ids)==len(set(ids))==len(positions)==4,'Exactly four unique legal bodies required')
        deadline(now,expiry,18)
        for ident in ids:self.fresh(ident)
        identity(use_key);wallet.validate(8,'action',use_key);conviction.validate(stats.owner,'Conviction',5)
        cs=[self.create(i,stats,CHOIR,'choir',10,14,30,expiry,concentration=concentration,
                        command_group=application,position=deepcopy(p)) for i,p in zip(ids,positions)]
        wallet.pay(8,'action',use_key);conviction.value-=5
        self.choirs[application]=tuple(ids)
        for c in cs:self.physical.creatures[c.instance_id]=c
        return tuple(cs)

    def thrall(self,ident,body_id,stats,now,expiry,wallet,conviction,*,use_key,legal,death_age_seconds):
        require(stats.source_class=='cleric' and legal,'Corpse Servant exact source gates required')
        integer(death_age_seconds,'actual corpse age seconds',0,60)
        self.fresh(ident);deadline(now,expiry,18);identity(use_key)
        body=self.physical.corpses[body_id]
        require(body.real_original and body.available and body.creature_type=='humanoid','Real available humanoid body required')
        wallet.validate(6,'action',use_key);conviction.validate(stats.owner,'Conviction',3)
        c=self.create(ident,stats,RITUAL,'thrall',10,13,30,expiry)
        wallet.pay(6,'action',use_key);conviction.value-=3
        self.physical.consume_body(body_id,ident);self.physical.creatures[ident]=c
        return c

    def unbound(self,application,ids,body_ids,existing_ids,stats,now,expiry,wallet,*,use_key,legal,existing_control_certified):
        identity(application);require(application not in self.unbound_buffs,'Application reused')
        require(stats.source_class=='oracle' and legal and existing_control_certified,'Exact Unbound/body/control gates required')
        require(len(ids)==len(body_ids)<=3 and len(set(ids))==len(ids) and len(set(body_ids))==len(body_ids),'Unique bodies/instances, up to three')
        require(len(existing_ids)<=3 and len(set(existing_ids))==len(existing_ids) and not set(ids)&set(existing_ids),'Snapshot existing undead before creation')
        for ident in existing_ids:identity(ident)
        for ident in ids:self.fresh(ident)
        for ident in body_ids:
            body=self.physical.corpses[ident]
            require(body.real_original and body.available,'Real available nonsummoned body required')
        deadline(now,expiry,18);identity(use_key);wallet.validate(0,'action',use_key)
        cs=[self.create(i,stats,UNBOUND,'bone-servant',1,12+stats.pb//2,30,expiry) for i in ids]
        buff=ExistingUndeadBuff(stats.owner,frozenset(existing_ids),expiry)
        wallet.pay(0,'action',use_key)
        for body_id,c in zip(body_ids,cs):
            self.physical.consume_body(body_id,c.instance_id);self.physical.creatures[c.instance_id]=c
        self.unbound_buffs[application]=buff
        return tuple(cs),buff

    def turrets(self,ids,stats,now,expiry,wallet,*,use_key,legal):
        require(stats.source_class=='soldier' and legal,'Exact Turret source/placement gates required')
        require(1<=len(ids)<=2 and len(set(ids))==len(ids),'Choose one or two legal turrets for this use')
        for ident in ids:self.fresh(ident)
        deadline(now,expiry,18);identity(use_key);wallet.validate(0,'action',use_key)
        cs=[self.create(i,stats,TURRET,'soldier-turret',2*stats.level,12+stats.pb,0,expiry) for i in ids]
        wallet.pay(0,'action',use_key)
        for c in cs:self.physical.creatures[c.instance_id]=c
        return tuple(cs)

    def command(self,order_id,ids,round_number,now,wallet,ledger,*,regular,legal,capable):
        identity(order_id);require(order_id not in self.orders,'Order identity reused')
        require(regular and legal and capable,'Original regular-turn issuance and legal capable actors required')
        require(ids and len(set(ids))==len(ids),'Unique commanded identities required')
        cs=[self.physical.creatures[i] for i in ids]
        require(all(isinstance(c,RemainingCreature) and c.controller==ledger.owner and c.can_act(now,round_number) for c in cs),'Own active selected creatures required')
        if len(cs)>1:
            require(len(cs)<=4 and all(c.profile=='choir' and c.command_group==cs[0].command_group for c in cs),'Only one Choir permits grouped attacks')
        for c in cs:
            require(c.profile!='bone-servant' or round_number not in c.local_modes,'Servant local attack/sacrifice choice spent')
        ledger.activate(round_number,'attack',wallet)
        for c in cs:
            if c.profile=='bone-servant':c.local_modes[round_number]='ATTACK_RESERVED'
        self.orders[order_id]={'owner':ledger.owner,'ids':tuple(ids),'round':round_number,'settled':False}

    def resolve_command(self,order_id,round_number,now,*,attached_phase,valid_ids):
        o=self.orders[order_id]
        require(attached_phase and round_number==o['round'] and not o['settled'],'Exactly once in designated attached phase')
        require(set(valid_ids)<=set(o['ids']),'Only commanded actors may execute')
        o['settled']=True
        live=[i for i in o['ids'] if i in valid_ids and self.physical.creatures[i].controller==o['owner']
              and self.physical.creatures[i].can_act(now,round_number)]
        o['executed']=tuple(live)
        return {'attackers':live,'attackRolls':len(live),'extraTurns':0,'refund':False}

    def choir_hit(self,event_id,order_id,fanatic_id,round_number,*,hit,healing_permitted,current_hp,maximum_hp):
        identity(event_id);o=self.orders[order_id]
        require(o['settled'] and round_number==o['round'] and fanatic_id in o.get('executed',()),'Must follow the actual commanded attack')
        c=self.physical.creatures[fanatic_id];require(c.profile=='choir','Choir only')
        key=(order_id,fanatic_id)
        require(event_id not in self.hit_events and key not in self.hit_events,'Attack result already settled')
        integer(maximum_hp,'maximum HP',1);integer(current_hp,'current HP',0,maximum_hp)
        self.hit_events.update((event_id,key))
        cap_key=(o['owner'],round_number);used=self.choir_healing.get(cap_key,0)
        gained=int(bool(hit and healing_permitted and used<4 and current_hp<maximum_hp))
        self.choir_healing[cap_key]=used+gained
        return {'hp':current_hp+gained,'healed':gained,'woundsRemoved':0}

    def burst(self,c,*,suppressed=False):
        require(c.profile=='choir','Only Choir explodes')
        if c.explosion_settled:return None
        c.explosion_settled=True
        if suppressed:return None
        return {'sourceId':CHOIR,'sourceOwner':c.source_owner,
                'fanatic':c.instance_id,'position':deepcopy(c.position),'radius':5,'targets':'legal enemies',
                'damage':'1d6 necrotic','save':'DEX half','healing':False,'commandDebit':False,
                'choirHealingEligible':False,'fanaticBodyResourceEligible':False,
                'explosionOpportunityGenerated':False,'fanaticCorpse':False}

    def damage(self,ident,amount,now,*,suppress_zero_explosion=False):
        """Actual damage after defenses, before this body's existing temp HP."""
        c=self.physical.creatures[ident]
        require(isinstance(c,RemainingCreature) and c.active(now),'Active selected finite body required')
        integer(amount,'post-defense damage',0)
        absorbed=min(amount,c.temp_hp);c.temp_hp-=absorbed;c.hp=max(0,c.hp-(amount-absorbed))
        burst=None
        if c.hp==0:
            c.state='ended'
            if c.profile=='choir':burst=self.burst(c,suppressed=suppress_zero_explosion)
        return {'burst':burst,'corpse':False,'woundRoll':False}

    def end_choir(self,application,now,*,concentration_ended=False):
        cs=[self.physical.creatures[i] for i in self.choirs[application]]
        require(concentration_ended or all(clock_marker(now)>=c.expiry for c in cs),'Actual concentration or deadline ending required')
        # Snapshot descriptors before effects can alter positions or end another body.
        survivors=[c for c in cs if c.state=='active' and c.hp>0]
        events=[self.burst(c) for c in survivors]
        for c in survivors:c.state='ended'
        return [e for e in events if e is not None]

    def expire(self,now):
        events=[]
        for application,ids in self.choirs.items():
            if clock_marker(now)>=self.physical.creatures[ids[0]].expiry:
                events+=self.end_choir(application,now)
        for c in self.physical.creatures.values():
            if isinstance(c,RemainingCreature) and c.profile!='choir' and c.state=='active' and clock_marker(now)>=c.expiry:c.state='ended'
        for s in self.structures.values():
            if s.expiry and clock_marker(now)>=s.expiry and s.state=='intact':s.state='expired'
        return events

    def sacrifice(self,ident,round_number,now,wallet,windows,attack_id,*,owner,legal,successful_single_target_hit,pre_consequences):
        c=self.physical.creatures[ident]
        require(isinstance(c,RemainingCreature) and c.profile=='bone-servant' and c.active(now),'Living Unbound servant required')
        require(c.controller==c.source_owner==owner,'Original Oracle must currently control its own servant')
        integer(round_number,'numbered round',1)
        require(round_number not in c.local_modes,'This servant already reserved attack/sacrifice')
        windows.validate(attack_id,successful_single_target_hit=successful_single_target_hit,pre_consequences=pre_consequences,legal=legal)
        wallet.validate(0,'reaction')
        wallet.pay(action='reaction');c.local_modes[round_number]='SACRIFICED';c.hp=0;c.state='ended'
        return windows.commit(attack_id,ident)

    def palisade(self,ident,stats,supplies,wallet,encounter,*,legal):
        require(stats.source_class=='soldier' and stats.level>=5 and legal,'Palisade access/material/ground requirements')
        self.fresh(ident);identity(encounter);supplies.validate(stats.owner)
        cap=2 if stats.level>=13 else 1
        count=sum(s.owner==stats.owner and s.kind=='palisade' and s.state=='intact' for s in self.structures.values())
        require(count<cap and supplies.deployments.get(encounter,0)<cap and supplies.kits>0,'Intact cap, encounter allowance or kit exhausted')
        wallet.validate(0,'action');maximum=max(1,5+stats.constitution)*(2 if stats.level>=13 else 1)
        s=Structure(ident,stats.owner,'palisade',maximum,maximum,area_resistance=stats.level>=13)
        wallet.pay(action='action');supplies.kits-=1;supplies.deployments[encounter]=supplies.deployments.get(encounter,0)+1
        self.structures[ident]=s
        self.physical.noncorpse_identities.add(ident)
        return s

    def quick_deploy(self,ident,stats,supplies,now,expiry,wallet,*,use_key,legal):
        require(stats.source_class=='soldier' and legal,'Legal Quick Deploy required')
        self.fresh(ident);supplies.validate(stats.owner);require(supplies.field_supplies>0,'Actual carried field supplies required')
        deadline(now,expiry,18);identity(use_key);wallet.validate(0,'action',use_key)
        s=Structure(ident,stats.owner,'quick',5,5,expiry)
        wallet.pay(0,'action',use_key);supplies.field_supplies-=1
        for old in self.structures.values():
            if old.owner==stats.owner and old.kind=='quick' and old.state=='intact':old.state='replaced'
        self.structures[ident]=s
        self.physical.noncorpse_identities.add(ident)
        return s

    def structure_damage(self,ident,amount,now):
        """Caller already applied actual object defenses, including area resistance."""
        s=self.structures[ident];require(s.active(now),'Intact object required');integer(amount,'post-defense damage',0)
        s.hp=max(0,s.hp-amount)
        if s.hp==0:s.state='destroyed'
        return {'hp':s.hp,'state':s.state,'salvage':0,'kitRefund':0}

    def repair(self,ident,stats,supplies,wallet,encounter,now,*,legal):
        s=self.structures[ident];supplies.validate(stats.owner)
        require(stats.source_class=='soldier' and s.owner==stats.owner and s.kind=='palisade' and s.active(now) and legal,'Own legal positive-HP Palisade required')
        require(s.hp<s.maximum_hp and encounter not in supplies.repaired and supplies.spare_parts>0,'Repair requires damage, unused encounter use and actual spare parts')
        wallet.validate(0,'action');gain=min(stats.modifier,s.maximum_hp-s.hp)
        wallet.pay(action='action');supplies.spare_parts-=1;supplies.repaired.add(encounter);s.hp+=gain
        return gain

    def dismantle(self,ident,supplies,now,*,completed_seconds,legal):
        s=self.structures[ident];supplies.validate(s.owner)
        require(legal and completed_seconds>=60 and s.kind=='palisade' and s.active(now),'Actual one-minute dismantling of intact Palisade required')
        s.state='dismantled';before=supplies.kits;supplies.kits=min(2,before+1)
        return supplies.kits-before

    def palisade_benefits(self,ident,owner,now,*,adjacent,brace_geometry):
        s=self.structures[ident]
        valid=s.owner==owner and s.kind=='palisade' and s.active(now) and adjacent
        return {'holdAC':int(valid),'holdSaves':int(valid),'braceFlatDR':2 if valid and brace_geometry else 0}

    def synergy(self,ident,stats,now,turn_id,*,adjacent,own_ranged_weapon_hit):
        identity(turn_id);s=self.structures[ident];key=(stats.owner,turn_id)
        require(stats.source_class=='soldier' and s.owner==stats.owner and s.kind=='palisade' and s.active(now) and adjacent and own_ranged_weapon_hit,'Actual own ranged weapon hit beside own intact Palisade required')
        require(key not in self.synergy_turns,'Palisade Synergy already used this own turn')
        self.synergy_turns.add(key);return stats.scale


@dataclass
class LedgerControl:
    owner: str
    application_id: str
    expiry: ClockMarker
    targets: dict
    interception_used: bool=False
    pending: dict=field(default_factory=dict)
    order_ids: set=field(default_factory=set)
    first_damage: set=field(default_factory=set)

    @classmethod
    def apply(cls,application,stats,now,expiry,target_results,wallet,rc,*,legal,mastery=False):
        """target_results maps eligible target ID to actual failed/waived initial save.
        Caller checks nonlegendary undead, CR<=floor(L/2), range20, agency.
        Successful saves still consume the cast's Action and2 RC.
        """
        identity(application);require(stats.source_class=='oracle' and legal,'Exact Ledger source/target gates')
        require(1<=len(target_results)<=(3 if mastery else 2),'One to printed target maximum')
        for t,result in target_results.items():identity(t);require(type(result) is bool,'Resolved save result required')
        deadline(now,expiry,12);wallet.validate(0,'action');rc.validate(stats.owner,'RC',2)
        wallet.pay(action='action');rc.value-=2
        return cls(stats.owner,application,expiry,{t:{'active':True,'last_end':0,'soft_until':None} for t,v in target_results.items() if v})

    def operative(self,target,now,controlled):
        return controlled and target in self.targets and self.targets[target]['active'] and clock_marker(now)<self.expiry

    def issue(self,target,order_id,now,round_number,wallet,commands,hard,encounter,*,regular,willing,controlled,capable,legal,extra_clock=None,granted_by_extra_action=False,target_turn_upcoming=True):
        identity(order_id);require(order_id not in self.order_ids and target not in self.pending,'Duplicate order or pending target')
        require(commands.owner==self.owner,'Wrong canonical command ledger')
        require(regular and capable and legal and self.operative(target,now,controlled),'Legal original regular-turn order required')
        if willing:
            require(isinstance(extra_clock,ExtraActionClock) and not granted_by_extra_action and round_number not in extra_clock.spent_rounds,'Canonical target extra-Action allowance required')
            commands.validate(round_number,'attack',wallet)
            extra_clock.spend(round_number);commands.activate(round_number,'attack',wallet);resolution=round_number
        else:
            require(hard.available(encounter,self.owner,target),'Shared hard denial spent')
            resolution=round_number if target_turn_upcoming else round_number+1
            commands.reserve(round_number,resolution,order_id,wallet)
        self.order_ids.add(order_id)
        self.pending[target]={'id':order_id,'round':resolution,'willing':willing,'encounter':encounter}
        return resolution

    def cancel(self,target,commands):
        require(commands.owner==self.owner,'Wrong command ledger')
        o=self.pending.pop(target,None)
        if o and not o['willing']:commands.settle(o['round'],o['id'],executed=False)

    def resolve(self,target,now,round_number,commands,hard,*,attached_phase=False,actual_regular_action_slot=False,willing,controlled,capable,legal):
        require(commands.owner==self.owner and target in self.pending,'Matching pending order required')
        o=self.pending[target];require(round_number==o['round'],'Wrong resolution round')
        require(attached_phase if o['willing'] else actual_regular_action_slot,'Wrong action checkpoint')
        valid=self.operative(target,now,controlled) and capable and legal
        if o['willing']:valid=valid and willing
        else:valid=valid and hard.available(o['encounter'],self.owner,target)
        if not o['willing']:
            commands.settle(round_number,o['id'],executed=bool(valid))
            if valid:hard.spend(o['encounter'],self.owner,target)
        del self.pending[target]
        return {'attackRolls':int(bool(valid)),'replacesNormalAction':bool(valid and not o['willing']),
                'extraAction':bool(valid and o['willing']),'extraTurn':False,'sourceStats':'original creature',
                'damageCap':'S d8+M','monsterMultiattack':False,'resourceRiders':False}

    def revalidate(self,target,now,commands,hard,*,willing,controlled,capable,legal):
        o=self.pending.get(target)
        if not o:return False
        valid=self.operative(target,now,controlled) and capable and legal
        valid=valid and (willing if o['willing'] else hard.available(o['encounter'],self.owner,target))
        if not valid:self.cancel(target,commands)
        return bool(valid)

    def regular_end(self,target,now,marker,commands,hard,encounter,*,failed_save,regular,controlled):
        t=self.targets[target];integer(marker,'target original regular-end index',1)
        require(regular and marker>t['last_end'],'Extra/repeated end cannot tick target')
        t['last_end']=marker;t['soft_until']=None
        if not self.operative(target,now,controlled) or not failed_save:
            t['active']=False;self.cancel(target,commands);return None
        if not hard.available(encounter,self.owner,target):
            t['soft_until']=marker+1
            return {'noReactions':True,'speed':0,'untilRegularEnd':marker+1,'orEarlier':self.expiry}
        return None

    def first_damage_offer(self,target,now,round_number,*,controlled,qualifying):
        integer(round_number,'numbered round',1);key=(target,round_number)
        if not qualifying or not self.operative(target,now,controlled) or key in self.first_damage:return 0
        self.first_damage.add(key);return 1

    def intercept(self,target,now,windows,attack_id,*,controlled,expendable,native_zero_legal,successful_single_target_hit,pre_consequences):
        require(self.operative(target,now,controlled) and expendable and native_zero_legal and not self.interception_used,'Legal expendable controlled undead and unused application required')
        windows.validate(attack_id,successful_single_target_hit=successful_single_target_hit,pre_consequences=pre_consequences,legal=True)
        self.interception_used=True
        # Return a zero-assignment instruction; caller executes native death prevention/lifecycle.
        return windows.commit(attack_id,target)


@dataclass(frozen=True)
class WeaponProfile:
    attack: int
    dice: tuple  # tuple of (count,sides), ordinary base only
    flat: int
    damage_type: str
    range_feet: int

    def __post_init__(self):
        require(type(self.attack) is int and type(self.flat) is int,'Recorded numeric attack/base modifier required')
        identity(self.damage_type);integer(self.range_feet,'actual ordinary weapon range',1)
        for count,sides in self.dice:integer(count,'dice count',1);integer(sides,'die sides',2)

    def capped_damage(self,scale,modifier):
        integer(scale,'S',1,4);integer(modifier,'M',1)
        if sum(n*s for n,s in self.dice)+self.flat>8*scale+modifier:return (((scale,8),),modifier)
        return self.dice,self.flat


def ledger_attack_profile(profile,stats):
    require(isinstance(profile,WeaponProfile) and stats.source_class=='oracle','Actual permitted native ordinary attack and Oracle stats required')
    dice,flat=profile.capped_damage(stats.scale,stats.modifier)
    return {'attack':profile.attack,'dice':dice,'flat':flat,'damageType':profile.damage_type,
            'range':profile.range_feet,'ordinaryCrit':True,'multiattack':False,'resourceRiders':False}


@dataclass
class FallenEchoes:
    deaths: set=field(default_factory=set)
    uses: set=field(default_factory=set)

    def record_death(self,owner,ally,encounter,*,actual_allied_death_in_aura):
        for v in (owner,ally,encounter):identity(v)
        require(actual_allied_death_in_aura,'Must be actual allied death in aura, not finite disappearance')
        self.deaths.add((owner,ally,encounter))

    def invoke(self,ally,encounter,rest_epoch,mode,stats,round_number,wallet,commands,*,legal,own_turn,profile=None,guard_expiry=None):
        require(stats.source_class=='paladin' and commands.owner==stats.owner and legal and own_turn,'Actual own Action and exact legal Echo target/source required')
        identity(rest_epoch);require((stats.owner,ally,encounter) in self.deaths,'Recorded qualifying death required')
        key=(stats.owner,ally,rest_epoch);require(key not in self.uses,'Same fallen ally already used this long rest')
        require(mode in ('strike','guard'),'Choose exactly one Echo mode')
        wallet.validate(10,'action')
        if mode=='strike':
            require(isinstance(profile,WeaponProfile),'Recorded ordinary weapon profile required')
            commands.validate(round_number,'decoy',wallet)
            dice,flat=profile.capped_damage(stats.scale,stats.modifier)
            result={'attack':min(profile.attack,stats.pb+stats.charisma),'dice':dice,'flat':flat,
                    'damageType':profile.damage_type,'range':profile.range_feet,'ordinaryCrit':True}
        else:
            require_deadline(guard_expiry)
            result={'acBonus':2,'expires':guard_expiry}
        wallet.pay(10,'action');self.uses.add(key)
        if mode=='strike':commands.activate(round_number,'decoy',wallet)
        result.update(targetable=False,corpse=False,resurrection=False,extraTurn=False,resourceRiders=False)
        return result


@dataclass
class SpiritScout:
    owner: str
    mode: str
    expiry: ClockMarker
    state: str='outbound'
    delivered_message: bool=False
    observations: list=field(default_factory=list)

    @classmethod
    def summon(cls,stats,mode,now,expiry,wallet,*,use_key,legal_timed_route):
        require(stats.source_class=='oracle' and legal_timed_route,'Source/route/plane/barrier/timing certification required')
        require(mode in ('observe','inquiry','message'),'One assigned task required')
        deadline(now,expiry,600);identity(use_key);wallet.validate(0,'action',use_key)
        wallet.pay(0,'action',use_key);return cls(stats.owner,mode,expiry)

    def arrive_and_perform(self,now,observations,*,legal_direct_observations,willing_spirits=True):
        require(self.state=='outbound' and clock_marker(now)<self.expiry,'Live outbound task required')
        require(legal_direct_observations and (self.mode!='inquiry' or willing_spirits),'Ordinary direct observations or willing spirit inquiry only')
        self.observations=list(observations);self.delivered_message=self.mode=='message';self.state='returning'

    def return_report(self,now,*,actually_returned):
        require(self.state=='returning' and actually_returned,'Actual return required; no remote report')
        if clock_marker(now)>=self.expiry:
            self.state='expired';return []
        self.state='ended';return list(self.observations)

    def expire(self,now):
        if clock_marker(now)>=self.expiry and self.state in ('outbound','returning'):self.state='expired'
        return {'state':self.state,'remoteReport':None,'messageAlreadyDelivered':self.delivered_message}
