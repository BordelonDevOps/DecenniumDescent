"""Reviewed bounded39-source damage sharing plus2 supporting Tinker engines.

Magnetic Wall is a separately reviewed74+3 lifecycle-package supplement.

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
