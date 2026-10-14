# Redirection exact final disposition

Codex → Calibration Review. Please reply below12,000 characters. All three findings are corrected; please inspect the EXACT current helper/tests/guide below and either close this bounded39-source interface with2supportingTinker engines or identify concrete remaining defects.

1. Stage precedence: guide now states premitigation offers first, mandatory priority only WITHIN a stage, pretransferlocksallrootbranches, no speculative defense/preventionpreview. Tested Bloodbond blocking laterautomaticAegis.
2. Guardiannewcounter returns ONLY source's noFreeAttackGeneration/noActionGeneration. Incoming noResource/noHealing/noReflection is not inherited; newregressionprovesit.
3. Palmnewforce root has NOinventedflags. Normalconsumereligibilitypreserved; noattack/meleeidentityblocksrecursivePalm. Regressionchangedaccordingly.
4. FinalStandguideexplicitlystates BOTHtempHP and resistall-through-allynextend. Helper only numerictempHP; caller createsresistrecord.
5. Two local source-contract safeguards: Paladinledger rejects non-Paladin/nonregisteredsource; native self-absorptionriders cannotborrowdamage fromBurdenShared's OTHER recipients. Addedregressions. This narrowsinvalidhelperinputs; allprinted costs/ranges/cadence remaincallerowned.

Validation94checks/186conservationstatesPASS. Exact39sourceobjects plus2supportingenginepassages preserved. Firstcandidate8886 count superseded by current report; the original88checks were expanded by6.

No whole-game defense order, full companion/repair lifecycle, general trigger/action engine, character ownership, numerical balance or publication claim. After boundedclosure, the next prepared exactconference is51class+7feat maximumHP records, includingstat modifiers,thresholds and exclusions.


## Exact tools/redirection_playtest_rules.py

"""Bounded39-source damage sharing, proposed for exact notebook review.

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


## Exact tools/validate_redirection_playtests.py

from pathlib import Path
import json
from copy import deepcopy
from redirection_playtest_rules import *
from core_playtest_rules import LifeState
from healing_playtest_rules import healing_packet
from control_playtest_rules import absolute_deadline,turn_end_deadline
ROOT=Path(__file__).resolve().parents[1]
BB='crimson-agent.hero.bloodweaver.bloodbond'
VT='crimson-agent.hero.bloodweaver.veinlock-tether'
BREATH='monk.hero.enlightened-master.shared-breath'
TISSUE='warrior.hero.wardborn.guardian-tissue'
AEGIS='warrior.hero.wardborn.aegis-incarnate'
STANCE='paladin.base.protective-stance'
EMERGENCY='tinker.arch.emergency-protocols'

def main():
    checks=[]
    def check(name,actual,expected):
        assert actual==expected,(name,actual,expected);checks.append(name)
    def rejects(name,fn):
        try:fn()
        except SpellRuleError:checks.append(name)
        else:raise AssertionError(name)
    def raw(name,amount=20,**kw):return DamageRoot(name,'ally',amount,'fire',**kw)
    def defended(name,amount=20,**kw):
        r=raw(name,amount,**kw);r.defend(r.original_id);return r
    def living_all(r,states=None,**kw):
        states=states or {}
        for bid,b in r.branches.items():
            if b.stage=='raw':r.defend(bid)
            r.resolve_living(bid,states.get(b.target,LifeState(100,100)),**kw)
    r=raw('pre',40,attack_hit=True,critical=True)
    r.transfer(BB,'agent',{'agent':10})
    ids=list(r.branches);r.defend(ids[0],resistant=True);r.defend(ids[1],resistant=True)
    check('Quarter sharing precedes both recipients resistance',[b.amount for b in r.branches.values()],[15,5])
    check('Transferred portion loses attack-critical identity',(r.branch(ids[1]).attack_hit,r.branch(ids[1]).critical),(False,False))
    check('Original portion preserves hit and critical identity',(r.branch(ids[0]).attack_hit,r.branch(ids[0]).critical),(True,True))
    rejects('Pretransfer locks retained original against later transfer',lambda:r.transfer(BREATH,'monk',{'monk':1}))
    rejects('Quarter reaction cannot arbitrarily choose smaller share',lambda:raw('bad-quarter',40).transfer(BB,'agent',{'agent':5}))
    a=raw('pre-dr',40);a.transfer(BB,'agent',{'agent':10})
    a.defend(a.original_id,flat_reductions=(12,5),resistant=True)
    check('Strongest original flat reduction applies to retained share only',a.branch(a.original_id).amount,9)
    a.defend('pre-dr/transfer/1',flat_reductions=(2,),resistant=True)
    a.prevent('pre-dr/transfer/1',3,'guardian')
    check('Premitigation transfer accepts recipient defenses and pure prevention',a.branch('pre-dr/transfer/1').amount,1)
    r=raw('post',30);r.defend(r.original_id,flat_reductions=(5,3),resistant=True)
    check('Flat strongest then resistance floor',r.branch(r.original_id).amount,12)
    r.transfer(BREATH,'monk',{'monk':5},scale=2,modifier=3)
    check('Postdefense split conserves remaining amount',[b.amount for b in r.branches.values()],[7,5])
    child='post/transfer/1'
    rejects('Postdefense child cannot defend again',lambda:r.defend(child,immune=True))
    rejects('Postdefense child cannot use further pure prevention',lambda:r.prevent(child,5,'bloom'))
    rejects('Postsplit original cannot use late pure prevention',lambda:r.prevent(r.original_id,1,'late'))
    after,event=r.resolve_living(child,LifeState(20,20,temp_hp=5))
    check('Unmitigated transfer still consumes temporary HP',(after.hp,after.temp_hp,event['actualDamageDealt']),(20,0,5))
    check('TemporaryHP absorption does not erase concentration packet',event['concentrationDamage'],5)
    rejects('Root totals await every terminal branch',lambda:r.total())
    r.resolve_living(r.original_id,LifeState(20,20))
    check('Physical total counts final recipients only',r.total(),12)
    rejects('Final branch cannot resolve twice',lambda:r.resolve_living(child,after))
    r=defended('critical',6,attack_hit=True,critical=True)
    r.transfer(BREATH,'monk',{'monk':6},scale=3,modifier=3)
    after,event=r.resolve_living('critical/transfer/1',LifeState(20,0))
    check('Transferred critical damage causes one death failure',(after.death_failures,event['criticalHit']),(1,False))
    after,event=r.resolve_living(r.original_id,LifeState(20,20))
    check('Full transfer retains original hit without positive damage',(event['attackHit'],event['positiveDamageEvent']),(True,False))
    r=defended('aegis',50)
    r.transfer(AEGIS,'warrior',{'warrior':25})
    after,event=r.resolve_living('aegis/transfer/1',LifeState(10,2),ritual_ward=True)
    check('Aegis still transfers lethal packet but Ward can prevent death',(after.dead,after.hp,event['instantDeath'],event['wardUsed']),(False,1,True,True))
    check('Survival replacement does not overcount actualHP damage',event['actualDamageDealt'],1)
    r=defended('wounds',12);r.transfer(BREATH,'monk',{'monk':7},scale=3,modifier=4)
    after,event=r.resolve_living('wounds/transfer/1',LifeState(20,5),wound_natural=20)
    check('Ordinary transfer dropping positiveHP to0 invokes Wound save',(after.hp,event['woundSaves']),(0,1))
    rejects('Caller cannot replace the branch critical identity',
            lambda:r.resolve_living(r.original_id,LifeState(20,20),critical=True))
    r=defended('no-riders',10);r.transfer(BREATH,'monk',{'monk':3},modifier=2)
    rejects('Transferred branch rejects attack maiming rider',lambda:r.resolve_living('no-riders/transfer/1',LifeState(20,20),maiming=True))
    ledger=PaladinRoundLedger('paladin',1)
    r=defended('stance-small',3,attack_hit=True)
    r.transfer(STANCE,'paladin',{'paladin':3},scale=4,modifier=4,paladin_ledger=ledger)
    check('Protective Stance cannot create nonexistent excess damage',r.operation['amount'],3)
    check('Shared Paladin ledger records one operation',len(ledger.events),1)
    r2=defended('second',5);snapshot=deepcopy(r2.branches)
    rejects('Second ordinary Paladin event rejected',lambda:r2.transfer(STANCE,'paladin',{'paladin':2},paladin_ledger=ledger))
    check('Failed shared allowance leaves root unchanged',r2.branches,snapshot)
    check('Failed shared allowance does not add ledger event',len(ledger.events),1)
    r3=defended('other-owner',5)
    r3.transfer(STANCE,'other-paladin',{'other-paladin':2},paladin_ledger=PaladinRoundLedger('other-paladin',1))
    check('Different Paladin keeps independent round allowance',r3.operation['owner'],'other-paladin')
    rejects('Different owner cannot transfer already split root',lambda:r3.transfer(BREATH,'monk',{'monk':1}))
    r=defended('zero-auto',1)
    check('Automatic rounded0 share creates no operation',r.transfer(AEGIS,'warrior',{}),None)
    check('Automatic0 leaves root unclaimed',r.operation,None)
    rejects('Optional0 transfer cannot activate',lambda:defended('zero-opt',5).transfer(BREATH,'monk',{}))
    r=defended('multi',12);ledger=PaladinRoundLedger('paladin',2)
    r.transfer(BURDEN,'paladin',{'friend-A':3,'friend-B':5},level=10,modifier=2,paladin_ledger=ledger)
    check('Burden is one multi-recipient operation',[b.amount for b in r.branches.values()],[4,3,5])
    living_all(r)
    check('Burden physical total includes all branches',r.total(),12)
    check('Burden healing consumer excludes prohibited branches',r.total('healing'),4)
    check('Burden resource consumer excludes prohibited branches',r.total('resource',resource='RP'),4)
    check('Source target predicate still filters final recipients',r.total(qualified_targets={'ally'}),4)
    rejects('Native self-absorption rider cannot use damage sent to another ally',
            lambda:native_transfer_temp_hp(r,'multi/transfer/1',source=P+'oath-of-the-chain.unbroken-covenant',scale=2,modifier=2,level=10))
    rejects('Paladin ledger cannot accept unrelated transfer source',
            lambda:PaladinRoundLedger('paladin',3).record('not-paladin',BREATH,2,'ally',crown_active=False,level=10,modifier=2))
    r=defended('flags',9);r.transfer(TISSUE,'warrior',{'warrior':3})
    living_all(r)
    check('Warrior transfer bans BT only',r.total('resource',resource='BT'),6)
    check('Warrior transfer does not invent universal resource ban',r.total('resource',resource='Ki'),9)
    r=defended('pal-flags',8);ledger=PaladinRoundLedger('paladin',3)
    r.transfer(P+'oath-of-the-martyr-king.king-s-smite','paladin',{'paladin':5},paladin_ledger=ledger)
    living_all(r)
    check('Paladin reflection ban does not suppress all retaliation',(r.total('reflection'),r.total('retaliation')),(3,8))
    check('Paladin generic engine does not forbid healing generation',r.total('healing'),8)
    r=defended('native',8);ledger=PaladinRoundLedger('paladin',4)
    r.transfer(STANCE,'paladin',{'paladin':6},scale=2,modifier=4,paladin_ledger=ledger)
    living_all(r)
    check('Protective Stance suppresses generic damage-generated healing',r.total('healing'),2)
    check('Unbroken Covenant triggers on redirection despite noDamageTriggers',
          native_transfer_temp_hp(r,'native/transfer/1',source=P+'oath-of-the-chain.unbroken-covenant',scale=2,modifier=4,level=10),3)
    check('Unrelated later healing of recipient remains legal',healing_packet(LifeState(20,10),5)['actualHpGained'],5)
    ledger=PaladinRoundLedger('paladin',5)
    opts=dict(crown_active=True,level=10,modifier=2)
    ledger.record('c1',CROWN,6,'same-ally',**opts)
    ledger.record('c2',CROWN,6,'same-ally',**opts)
    check('Crown permits two different events for same selected ally',len(ledger.events),2)
    check('Crown healing floors per event then uses cumulative cap',
          (ledger.crown_heal('c1',5,scale=2,modifier=2),ledger.crown_heal('c2',6,scale=2,modifier=2)),(2,2))
    rejects('Crown third event rejected',lambda:ledger.record('c3',CROWN,1,'ally',**opts))
    rejects('Crown heal cannot be settled twice',lambda:ledger.crown_heal('c1',5,scale=2,modifier=2))
    ledger=PaladinRoundLedger('paladin',6)
    ledger.record('earlier',STANCE,2,'ally',crown_active=False,level=10,modifier=2)
    ledger.record('later',CROWN,8,'ally',**opts)
    check('Midround Crown activation preserves previous ordinary use',len(ledger.events),2)
    rejects('Crown activation cannot reset shared event history',lambda:ledger.record('extra',CROWN,1,'ally',**opts))
    ledger=PaladinRoundLedger('paladin',7)
    ledger.record('c-first',CROWN,2,'ally',**opts)
    ledger.record('o-second',STANCE,2,'ally',**opts)
    check('One Crown plus one ordinary allowed with Crown active in either order',len(ledger.events),2)
    ledger=PaladinRoundLedger('paladin',8)
    ledger.record('amount',CROWN,11,'ally',**opts)
    rejects('Crown amount cap independent of remaining event slot',lambda:ledger.record('too-much',CROWN,2,'ally',**opts))
    check('Failed amount cap leaves one event',len(ledger.events),1)
    ledger=PaladinRoundLedger('paladin',9)
    ledger.record('blocked',CROWN,8,'ally',**opts)
    nominal=ledger.crown_heal('blocked',8,scale=2,modifier=2)
    check('Blocked Crown heal yields0actual',healing_packet(LifeState(20,1),nominal,hp_gain_prohibited=True)['actualHpGained'],0)
    check('Blocked Crown healing consumes nominal cap',ledger.crown_heal_used['ally'],4)
    ledger=PaladinRoundLedger('paladin',10)
    r=defended('final-first',5);r.transfer(FINAL,'paladin',{'paladin':5},paladin_ledger=ledger)
    rejects('Final Stand constrained to one shared event that round',lambda:defended('final-second',4).transfer(FINAL,'paladin',{'paladin':4},paladin_ledger=ledger))
    check('Final Stand is an automatic profile',PROFILES[FINAL].automatic,True)
    r=defended('bloom-first',6);pool=BloomPool('bloom','ally',15,absolute_deadline(60))
    pool.absorb(r,r.original_id,0,target_next_end=turn_end_deadline(6))
    check('Bloom pool persists across small packet',(pool.remaining,pool.ended),(9,False))
    r=defended('bloom-second',12);pool.absorb(r,r.original_id,1,target_next_end=turn_end_deadline(6))
    check('Bloom depletion leaves remainder and starts rider',(r.branch(r.original_id).amount,pool.remaining,pool.ended,pool.rider_deadline),(3,0,True,turn_end_deadline(6)))
    pool=BloomPool('suppressed','ally',5,absolute_deadline(60));r=defended('suppressed',5)
    check('Suppression neither consumes nor ends Bloom',pool.absorb(r,r.original_id,2,target_next_end=turn_end_deadline(6),suppressed=True),0)
    check('Suppressed Bloom retains full capacity',(pool.remaining,pool.ended),(5,False))
    pool.absorb(r,r.original_id,70,target_next_end=turn_end_deadline(66),suppressed=True)
    check('Late observation preserves expiry-based rider deadline',(pool.ended,pool.rider_deadline),(True,turn_end_deadline(66)))
    pool=BloomPool('skip','monk',8,absolute_deadline(60));r=defended('skip-bloom',10)
    r.transfer(BREATH,'monk',{'monk':4},modifier=3)
    rejects('Unmitigated transfer cannot spend recipient Bloom',lambda:pool.absorb(r,'skip-bloom/transfer/1',1,target_next_end=turn_end_deadline(6)))
    check('Rejected Bloom attempt preserves finite pool',pool.remaining,8)
    attack=AttackRetarget('attack','ally');attack.retarget('guardian')
    check('Guardian uses original roll against own AC',attack.resolve(12,4,19)['hit'],False)
    rejects('Attack cannot bounce to another Guardian',lambda:attack.retarget('second-guardian'))
    rejects('Original attack cannot reroll on retarget',lambda:attack.resolve(20,4,19))
    rejects('Counter must wait for full original attack resolution',lambda:attack.guardian_counter(triggering_attack_fully_resolved=False,in_reach=True,actor_can_attack=True))
    flags=attack.guardian_counter(triggering_attack_fully_resolved=True,in_reach=True,actor_can_attack=True)
    check('Missed incoming attack still permits single legal counter','noFreeAttackGeneration' in flags,True)
    rejects('Counter opportunity cannot replay',lambda:attack.guardian_counter(triggering_attack_fully_resolved=True,in_reach=True,actor_can_attack=True))
    attack2=AttackRetarget('counter-parent','ally');attack2.retarget('guardian');attack2.resolve(10,5,12)
    check('A free counter cannot manufacture another free counter',
          attack2.guardian_counter(triggering_attack_fully_resolved=True,in_reach=True,actor_can_attack=True,parent_flags=flags),None)
    attack3=AttackRetarget('unrelated-flags','ally');attack3.retarget('guardian');attack3.resolve(12,4,18)
    counter_flags=attack3.guardian_counter(triggering_attack_fully_resolved=True,in_reach=True,actor_can_attack=True,
                                         parent_flags=frozenset({'noResourceGeneration','noHealingGeneration','noReflection'}))
    check('New Guardian attack drops unrelated incoming restrictions',
          counter_flags,frozenset({'noFreeAttackGeneration','noActionGeneration'}))
    attack=AttackRetarget('retarget-then-transfer','ally');attack.retarget('guardian')
    result=attack.resolve(20,3,20)
    r=DamageRoot('after-retarget',result['targetId'],10,'slashing',attack_hit=result['hit'],critical=result['critical'])
    r.defend(r.original_id);r.transfer(BREATH,'monk',{'monk':4},modifier=3)
    check('Attack retarget leaves later transfer opportunity intact',r.operation['amount'],4)
    r=defended('palm',9,attack_hit=True,melee_attack=True)
    counter=redirecting_palm(r,r.original_id,3,'attacker',second_enemy_id='second',new_root_id='palm-counter')
    check('Palm prevents floorhalf and caps separate force packet',(r.branch(r.original_id).amount,counter.rolled_packet),(5,3))
    counter.defend(counter.original_id,resistant=True)
    check('Palm force counter accepts new recipient defenses',counter.branch(counter.original_id).amount,1)
    check('Palm counter is not an attack hit',counter.branch(counter.original_id).attack_hit,False)
    check('Palm new force root has no invented consumer bans',
          [permits_consumer(counter.branch(counter.original_id),c) for c in ('free-attack','copy','action','healing')],[True]*4)
    rejects('Palm force packet cannot recursively qualify as a melee attack',
            lambda:redirecting_palm(counter,counter.original_id,3,'second'))
    r=defended('palm-no-second',9,attack_hit=True,melee_attack=True)
    check('Palm reduction remains without a second enemy',redirecting_palm(r,r.original_id,3,'attacker'),None)
    check('Palm still reduced original damage',r.branch(r.original_id).amount,5)
    r=defended('palm-bad',9,attack_hit=True,melee_attack=True)
    rejects('Palm cannot send force back to original attacker',lambda:redirecting_palm(r,r.original_id,3,'attacker',second_enemy_id='attacker',new_root_id='bad-counter'))
    check('Invalid counter target does not consume prevention',r.branch(r.original_id).amount,9)
    rejects('Ranged attack cannot activate Palm',lambda:redirecting_palm(defended('palm-ranged',9,attack_hit=True),'palm-ranged/original',3,'attacker'))
    r=defended('drone',10,attack_hit=True);r.transfer(EMERGENCY,'tinker',{'drone':6},scale=2,modifier=4)
    after,event=r.resolve_device('drone/transfer/1',DeviceState(10,3,temp_hp=1))
    check('Emergency drone destruction uses device consequences',(after.hp,after.destroyed,event['actualDamageDealt'],event['woundSaves'],event['deathFailuresAdded']),(0,True,4,0,0))
    check('Device transfer does not manufacture an enemy attack hit',event['attackHit'],False)
    check('Emergency drone transfer suppresses retaliation consumer',permits_consumer(r.branch('drone/transfer/1'),'retaliation'),False)
    rejects('Destroyed drone cannot receive another functional packet',lambda:device_damage(after,1))
    rejects('False positiveHP destroyed device rejected',lambda:DeviceState(10,1,destroyed=True))
    r=raw('stage-precedence',20)
    r.transfer(BB,'agent',{'agent':5})
    r.defend(r.original_id)
    rejects('Earlier raw transfer preempts later mandatory Aegis',lambda:r.transfer(AEGIS,'warrior',{'warrior':7}))
    check('Stage arbitration never consumes hypothetical defender prevention',r.branch(r.original_id).amount,15)
    # Independent conservation/oracle formula coverage, including floor boundaries.
    states=0
    for amount in range(0,65):
      for source,denom in ((BB,4),(TISSUE,3),(AEGIS,2)):
       chosen=amount//denom
       check_amount=transfer_limit(source,amount)
       assert check_amount==chosen
       if not chosen:continue
       r=raw('matrix',amount) if source==BB else defended('matrix',amount)
       r.transfer(source,'protector',{'protector':chosen})
       assert sum(b.amount for b in r.branches.values())==amount
       living_all(r)
       assert r.total()==amount
       states+=1
    report={'status':'PASS','reviewStatus':'IN_REVIEW; exact implementation pending',
            'scope':'Bounded39-source stage, branch flags, transfer arithmetic, per-owner Paladin/Crown budget, retarget, finite Bloom/Palm and Tinker damage interface. Not full feature execution, all-source defense order, device repair lifecycle or balance.',
            'checkCount':len(checks),'conservationStates':states,'checks':checks}
    (ROOT/'docs/mechanics/REDIRECTION_PLAYTEST_VALIDATION.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(f'PASS {len(checks)} redirection checks and {states} transfer conservation states; review pending.')
if __name__=='__main__':main()


## Exact docs/mechanics/REDIRECTION_PLAYTEST_VALIDATION.json

{
  "status": "PASS",
  "reviewStatus": "IN_REVIEW; exact implementation pending",
  "scope": "Bounded39-source stage, branch flags, transfer arithmetic, per-owner Paladin/Crown budget, retarget, finite Bloom/Palm and Tinker damage interface. Not full feature execution, all-source defense order, device repair lifecycle or balance.",
  "checkCount": 94,
  "conservationStates": 186,
  "checks": [
    "Quarter sharing precedes both recipients resistance",
    "Transferred portion loses attack-critical identity",
    "Original portion preserves hit and critical identity",
    "Pretransfer locks retained original against later transfer",
    "Quarter reaction cannot arbitrarily choose smaller share",
    "Strongest original flat reduction applies to retained share only",
    "Premitigation transfer accepts recipient defenses and pure prevention",
    "Flat strongest then resistance floor",
    "Postdefense split conserves remaining amount",
    "Postdefense child cannot defend again",
    "Postdefense child cannot use further pure prevention",
    "Postsplit original cannot use late pure prevention",
    "Unmitigated transfer still consumes temporary HP",
    "TemporaryHP absorption does not erase concentration packet",
    "Root totals await every terminal branch",
    "Physical total counts final recipients only",
    "Final branch cannot resolve twice",
    "Transferred critical damage causes one death failure",
    "Full transfer retains original hit without positive damage",
    "Aegis still transfers lethal packet but Ward can prevent death",
    "Survival replacement does not overcount actualHP damage",
    "Ordinary transfer dropping positiveHP to0 invokes Wound save",
    "Caller cannot replace the branch critical identity",
    "Transferred branch rejects attack maiming rider",
    "Protective Stance cannot create nonexistent excess damage",
    "Shared Paladin ledger records one operation",
    "Second ordinary Paladin event rejected",
    "Failed shared allowance leaves root unchanged",
    "Failed shared allowance does not add ledger event",
    "Different Paladin keeps independent round allowance",
    "Different owner cannot transfer already split root",
    "Automatic rounded0 share creates no operation",
    "Automatic0 leaves root unclaimed",
    "Optional0 transfer cannot activate",
    "Burden is one multi-recipient operation",
    "Burden physical total includes all branches",
    "Burden healing consumer excludes prohibited branches",
    "Burden resource consumer excludes prohibited branches",
    "Source target predicate still filters final recipients",
    "Native self-absorption rider cannot use damage sent to another ally",
    "Paladin ledger cannot accept unrelated transfer source",
    "Warrior transfer bans BT only",
    "Warrior transfer does not invent universal resource ban",
    "Paladin reflection ban does not suppress all retaliation",
    "Paladin generic engine does not forbid healing generation",
    "Protective Stance suppresses generic damage-generated healing",
    "Unbroken Covenant triggers on redirection despite noDamageTriggers",
    "Unrelated later healing of recipient remains legal",
    "Crown permits two different events for same selected ally",
    "Crown healing floors per event then uses cumulative cap",
    "Crown third event rejected",
    "Crown heal cannot be settled twice",
    "Midround Crown activation preserves previous ordinary use",
    "Crown activation cannot reset shared event history",
    "One Crown plus one ordinary allowed with Crown active in either order",
    "Crown amount cap independent of remaining event slot",
    "Failed amount cap leaves one event",
    "Blocked Crown heal yields0actual",
    "Blocked Crown healing consumes nominal cap",
    "Final Stand constrained to one shared event that round",
    "Final Stand is an automatic profile",
    "Bloom pool persists across small packet",
    "Bloom depletion leaves remainder and starts rider",
    "Suppression neither consumes nor ends Bloom",
    "Suppressed Bloom retains full capacity",
    "Late observation preserves expiry-based rider deadline",
    "Unmitigated transfer cannot spend recipient Bloom",
    "Rejected Bloom attempt preserves finite pool",
    "Guardian uses original roll against own AC",
    "Attack cannot bounce to another Guardian",
    "Original attack cannot reroll on retarget",
    "Counter must wait for full original attack resolution",
    "Missed incoming attack still permits single legal counter",
    "Counter opportunity cannot replay",
    "A free counter cannot manufacture another free counter",
    "New Guardian attack drops unrelated incoming restrictions",
    "Attack retarget leaves later transfer opportunity intact",
    "Palm prevents floorhalf and caps separate force packet",
    "Palm force counter accepts new recipient defenses",
    "Palm counter is not an attack hit",
    "Palm new force root has no invented consumer bans",
    "Palm force packet cannot recursively qualify as a melee attack",
    "Palm reduction remains without a second enemy",
    "Palm still reduced original damage",
    "Palm cannot send force back to original attacker",
    "Invalid counter target does not consume prevention",
    "Ranged attack cannot activate Palm",
    "Emergency drone destruction uses device consequences",
    "Device transfer does not manufacture an enemy attack hit",
    "Emergency drone transfer suppresses retaliation consumer",
    "Destroyed drone cannot receive another functional packet",
    "False positiveHP destroyed device rejected",
    "Earlier raw transfer preempts later mandatory Aegis",
    "Stage arbitration never consumes hypothetical defender prevention"
  ]
}


## Exact docs/mechanics/REDIRECTION_SOURCE_VALIDATION.json

{
  "status": "PASS",
  "exactRecords": 39,
  "supportingEnginePassages": 2,
  "scope": "Original source equality, hashes and complete individual classification; not proof of semantic completion.",
  "issues": []
}


## Exact docs/mechanics/DAMAGE_SHARING_PLAYTEST.md

# Damage sharing, prevention and interception

**IN REVIEW —39 exact source passages and two supporting Tinker engine passages.** This candidate implements the supplied damage-sharing interface. It does not establish every item/spell defense, companion lifecycle, all-source attack chain or numerical balance. Original source cards remain unchanged.

Read the [source register](REDIRECTION_SOURCE_BINDINGS.md), [source checks](REDIRECTION_SOURCE_VALIDATION.json), [reference checks](REDIRECTION_PLAYTEST_VALIDATION.json), [first notebook proposal](../../../../docs/audit/2026-10-08/full-game/GPT_REDIRECTION_FIRST_REVIEW_PARTIAL.md) and [complete corrections](../../../../docs/audit/2026-10-08/full-game/GPT_REDIRECTION_BOUNDARIES.md). Later corrections supersede the retained first proposal.

## Resolve the kind of protection first

Guardian Pulse changes the target of an attack before comparing its original roll with AC. The Guardian becomes the actual hit/miss and on-hit-rider target. One attack can be retargeted once. Multiple offers are chosen by the original intended target; only the selected Guardian spends its Reaction/use. After the incoming attack fully resolves, a surviving, eligible Guardian may make the printed counterattack against an attacker in reach whether the original attack hit or missed. This free attack cannot grant another free attack or Action. Retargeting does not spend the later damage-transfer opportunity.

Bloodbond and Veinlock Tether divide the finalized raw damage before either recipient's mitigation. Attack/save success, save-halving and critical dice have already determined that amount. Bloodbond transfers one quarter, rounded down; Veinlock instead chooses up to S+M. Each recipient applies its own eligible defenses once to its own share.

Other supplied damage transfers divide damage after the original target's defenses and legal pure prevention, before temporary HP. Their transferred portions keep damage type and skip another DR/resistance/immunity/prevention stage. Temporary HP, applicable HP floors, would-die replacements, Wounds, concentration and ordinary life consequences still apply. “Unmitigated damage” does not mean “death cannot be prevented.”

Pure prevention removes damage without creating a second recipient. Elemental Absorption adds its resistance during ordinary defenses. Aura of Bonds and Crown reductions use the strongest applicable class flat reduction, then resistance/immunity. Finite/reactive prevention such as Bloom and Ancestral Guardian follows those defenses before post-defense transfer and temporary HP. Verify additional item/spell sources before treating this as universal defense ordering.

Redirecting Palm prevents half the Monk's post-defense damage, rounded down. The Monk keeps the remainder. A second enemy distinct from the triggering melee attacker, within5feet, can receive new force damage equal to the prevented amount, capped at Monk level. That new damage gets its own defenses; it is not a transferred attack or critical hit. With no second enemy, the Monk still receives the reduction.

Direct HP payments from Blood Sacrifice, Flesh-to-RP, Profane Exchange and Channel Life stay outside the damage sequence. They bypass temporary HP, obey their own legal minimum HP and do not create damage/Wound/resource triggers from paying the cost. Healing-recipient substitution and excess-healing conversion also remain distinct operations.

## One transfer operation and exact amounts

A root here means one original recipient's damage packet. A shared area cast has a separate root for each original recipient, under the same cast/roll identity.

One such root accepts one damage-sharing operation across all owners. A pre-mitigation split locks both its retained original portion and transferred portions against later transfer. Burden Shared can divide one operation among up to two other explicitly willing recipients. It does not create two redirection events. No transferred recipient may be the original damage target.

**New stage-precedence integration:** consider pre-mitigation offers before applying defenses, and post-defense offers afterward. Within the same stage, select eligible positive mandatory/automatic protection before optional offers; competing mandatory claims are chosen by the original damage target. A legally chosen Bloodbond/Veinlock operation can therefore preempt later Aegis/Final Stand because that root is already claimed. Do not preview or consume defenses/Bloom to decide a later-stage preference. The helper accepts an already selected legal operation; it does not select Reactions or schedule automatic offers.

Optional transfer requires a positive chosen amount and available damage. Zero transfer cannot spend an optional Reaction/resource/use. A mandatory rounded-zero share does nothing and spends no transfer allowance. An independently legal prevention component can still occur.

| Source | Transferred amount |
|---|---|
| Bloodbond | floor(raw damage/4), fixed |
| Veinlock Tether / Shared Breath / Selfless Guardian | chosen up to S+M |
| Protective Stance / Emergency Protocols | min(S+M, available damage), fixed |
| Life Linked | chosen up to floor(available damage/2) |
| Guardian Tissue | floor(available damage/3), fixed |
| Aegis Incarnate / Martyr's Share | floor(available damage/2), fixed |
| Chainbound Smite | chosen up to max(3, actual CHA modifier) |
| Linked Ward | chosen up to max(2, twice actual CHA modifier) |
| King's Smite protection | chosen up to5 |
| Aura of the Crown | chosen up to M |
| Crown of Embers / Burden Shared | chosen up to level+M |
| Crown Undying | chosen up to remaining level+M round allowance |
| Final Stand | all available damage, subject to shared allowance |

Every amount is capped by the available packet at its source's stage. Fixed fractions/fixed protection cannot voluntarily choose a smaller amount. Original actions, range, willingness, costs, active-state requirements, cadence and source-specific use limits still apply.

## Hit identity and final damage accounting

The original damage target retains its original hit, failed-save, critical and on-hit-rider identity even if all damage is transferred. A rider that requires positive damage must recheck the actual remaining packet. A transferred recipient was not hit by that attack and did not fail its save; it receives no attached poison/control/maiming/knockout rider merely because damage moved.

Accordingly, transferred damage from a critical attack gives an already0HP recipient the ordinary one damage failure, not two critical-hit failures. Concentration still sees the transferred recipient's resolved packet even if temporary HP absorbs all of it.

Use the [reviewed life-state interface](HEALING_DEATH_PLAYTEST.md) after resolving each final recipient. Numeric actual damage is temporary HP absorbed plus actual normal HP lost, excluding overkill and damage prevented by an HP floor. Sum each terminal recipient once. Do not also count the unsplit parent or unrelated counterdamage.

Physical root totals include every recipient. A healing/resource/reflection consumer sums only branches permitted for that consumer and qualifying for its own source's target predicate. For example, a meaningful-hostile-only drain does not automatically count damage transferred onto a friendly protector. Check all applicable flags for a compound trigger, such as a passive healing proc.

## Source-specific restrictions

All transfers prohibit another transfer. All supplied post-defense transfers prohibit another mitigation/prevention stage. Further restrictions differ:

| Source family | Additional restrictions on transferred damage |
|---|---|
| Paladin engine | No reflection or resource generation; does not universally prohibit other retaliation or healing |
| Protective Stance | Also no generic damage-trigger chains |
| Burden Shared | Also no derived healing |
| Oracle Life Linked | No reflection, resource/RC, passive, condition, action or copy generation; no recovery or retaliation |
| Guardian Tissue / Aegis | No BT generation; no invented ban on every other resource |
| Shared Breath | No additional generic trigger prohibition |
| Selfless Guardian / Emergency Protocols | No retaliation chain |
| Bloodbond / Veinlock | Each recipient still has its one defense stage; no additional blanket prohibition |

A no-derived-healing flag does not prevent unrelated later healing of the recipient.

The source's explicit redirection riders remain narrowly available. Unbroken Covenant triggers on the redirection operation, even when Protective Stance prohibits generic damage triggers; use half the final protector actual damage, capped at S+M. These self-absorption riders require damage actually transferred to the redirecting owner, not to another ally under Burden Shared. Linked Ward's own transfer granting temporary HP on reducing the Paladin to0 uses final actual damage, capped at level+M. Final Stand also gives the protected ally temporary HP equal to Paladin level and resistance to all damage through that ally's next turn end; the numeric helper handles only temporary HP, and the caller must create the resistance record. None grants a generic permission to ignore other source restrictions. Temporary HP still uses the larger remaining amount and does not stack.

## Paladin round ledger

Track each Paladin owner's numbered-round events. Ordinarily, one redirection event is available, using exactly one Paladin redirection feature. Final Stand is automatic on the first eligible positive post-defense packet while its allowance remains; the Paladin cannot save it for a later hit. Its “all damage” text does not override the explicit engine ceiling. It may redirect again in a later numbered round if still active before its source-next-start deadline.

Crown Undying can raise the owner's total to two different damage events, with at most one ordinary/non-Crown feature. The additional permission belongs to Crown Undying. A prior ordinary redirection remains recorded if Crown activates later in the same round; only one further Crown event is then possible. Reapplication does not clear history.

The two Crown events may protect the same selected ally. Sum Crown-transferred amounts against level+M per round. Its heal is floor(final Paladin branch actual damage/2) for each event, then capped by the remaining S+M per protected ally that round. Commit that nominal source entitlement before target healing restrictions; blocked or capped healing refunds no event, transfer amount or healing entitlement. The heal cannot heal the Paladin or start another redirection/heal-copy chain.

## Bloom and devices

Bloom Ward is a finite10+Oracle-level prevention pool across packets. Apply its legal prevention after ordinary defenses. Subtract only the prevented amount. The bloom ends on depletion, its1minute expiry, or actual legal removal. Suppression alone does not end it. Ending grants the printed +1 Frightened-save rider through the target's next end. A late clock observation must retain the endpoint calculated from the actual expiry, not create a fresh duration. An unmitigated transferred branch cannot consume this prevention pool.

Emergency Protocols requires an active/conscious drone within its printed range. The transfer occurs after the Tinker's defenses and before temporary HP. The drone receives the bounded transferred amount without mitigation; legally granted temporary HP can absorb it. At0HP the drone is destroyed and receives no organic Wound or death-save procedure.

Tinker engine[2] retains the destroyed drone at0 until its explicit repair/rebuild procedure. Ordinary functional repair cannot reconstruct a destroyed drone or reset ammunition, uses, duration or command budget. This package's device helper only resolves damage/destruction; it does not implement reconstruction or grant a destruction reward. The broader companion/device lifecycle remains open.

## Reference boundary

The helper validates arithmetic, stages, branch identity, replay protection and round entitlements. Callers establish legal sources, target relationships, exact source cadence, action/resource payment, clock endpoints and source-native riders. No helper imports card ownership merely from a string identifier. The source register preserves every exact original procedure alongside the overlay.

Guardian Pulse's new counterattack carries its explicit no-further-free-attack/no-Action limits, without inheriting unrelated incoming healing/resource/reflection restrictions. Palm's force damage has no invented copy/action/resource prohibition; each downstream source determines eligibility. It cannot trigger another Palm because it is not a melee attack.

Validation currently covers94 targeted checks and186 conservation states. Full-game completion, human balance and all-source combat/device execution remain separate unfinished work.
