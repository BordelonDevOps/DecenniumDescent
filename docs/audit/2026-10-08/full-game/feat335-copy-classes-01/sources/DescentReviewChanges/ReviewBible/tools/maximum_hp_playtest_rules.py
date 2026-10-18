"""Proposed58-source maximumHP/threshold primitives; exact review pending.

Base maximum excludes the represented ledger bonuses/reductions and systemic
factors. Caller owns legal sources, acquisition, target/control/equipment state,
level updates, real event snapshots, actions and rest completion.
"""
from dataclasses import dataclass,field,replace
from fractions import Fraction
from spell_playtest_rules import integer,SpellRuleError
from strain_playtest_rules import combined_maximum_hp,apply_effective_maximum
from control_playtest_rules import ClockMarker,clock_marker,require_deadline

MONK={
 'monk.hero.iron-fist-master.ribcrusher-strike':1,
 'monk.hero.iron-fist-master.bone-breaking-strike':2,
 'monk.hero.way-of-shadow.deathless-silence':4,
}
BONUS_GROUPS={
 'warrior.supplement.flesh-warden':'flesh-warden',
 'wizard.engine[10]':'wizard-conjuration',
 'wizard.engine[24]':'flesh-ascendant',
 'wizard.hero.necromancer.flesh-ascendant':'flesh-ascendant',
 'feat:familiar_bond':'familiar-bond',
 'feat:tenacity':'tenacity',
 'feat:tough':'tough',
 'feat:tough_as_nails':'tough-as-nails',
 'feat:dark_fortitude':'dark-fortitude',
}

def identity(value):
    if not isinstance(value,str) or not value:raise SpellRuleError('Nonempty identity required')
    return value

def source_amount(source,*,scale=1,modifier=1,character_level=1,warrior_level=1,
                  wizard_level=1,acquisition_level=None,conjuration_creation_level=None):
    """Freeze trauma/application amounts; refresh dynamic bonuses on legal level changes.

    Conjuration uses a stored creating-Wizard level; Tough uses acquisition level.
    Companion base statistics and feat acquisition/retraining are separate.
    """
    if source in MONK:
        integer(scale,'S',1,4);integer(modifier,'M',1)
        return MONK[source]*scale+modifier
    if source=='warrior.supplement.flesh-warden':
        return 2*integer(warrior_level,'Warrior level',1,20)
    if source=='wizard.engine[10]':
        return integer(conjuration_creation_level,'creating Wizard level snapshot',1,20)
    if source in ('wizard.engine[24]','wizard.hero.necromancer.flesh-ascendant'):
        return 2*integer(wizard_level,'current controlling Wizard level',1,20)
    integer(character_level,'current character level',1,20)
    if source=='feat:tough':
        return 2*integer(acquisition_level,'feat acquisition level snapshot',1,character_level)
    if source in ('feat:tenacity','feat:familiar_bond'):return character_level
    if source in ('feat:tough_as_nails','feat:dark_fortitude'):return 2*character_level
    raise SpellRuleError('Unreviewed maximumHP source')

@dataclass(frozen=True)
class MaxHpRecord:
    application_id: str
    source: str
    owner: str
    target: str
    amount: int
    starts: ClockMarker=field(default_factory=lambda:ClockMarker(0))
    expires: ClockMarker | None=None
    present: bool=True
    suppressed: bool=False
    ends_on_completed_rest: bool=False
    ended_reason: str | None=None

    def __post_init__(self):
        for x in (self.application_id,self.owner,self.target):identity(x)
        if self.source not in MONK and self.source not in BONUS_GROUPS:
            raise SpellRuleError('Unreviewed maximumHP modifier source')
        integer(self.amount,'source maximumHP modifier magnitude',0)
        require_deadline(self.starts)
        if self.expires is not None:
            require_deadline(self.expires)
            if self.expires<=self.starts:raise SpellRuleError('Expiry must follow application')
        if self.ends_on_completed_rest and self.source not in MONK:
            raise SpellRuleError('Only supplied Monk trauma uses this rest endpoint')
        if self.source in MONK and self.expires is None and not self.ends_on_completed_rest:
            raise SpellRuleError('Monk trauma needs its rest or explicit earlier endpoint')

    def operative(self,now):
        now=clock_marker(now)
        return self.present and not self.suppressed and self.starts<=now and (self.expires is None or now<self.expires)

    @property
    def group(self):
        return 'monk-trauma-global' if self.source in MONK else BONUS_GROUPS[self.source]

def effective_maximum(base,records,*,target,now=0,expedition=0,exhaustion=0):
    """Source-supported groups only; global Monk strongest, distinct bonuses additive."""
    integer(base,'base maximum excluding this ledger and systemic factors',1);identity(target)
    rows=tuple(records)
    if len({r.application_id for r in rows})!=len(rows):raise SpellRuleError('Duplicate application identity')
    active=[r for r in rows if r.target==target and r.operative(now)]
    groups={}
    for r in active:
        old=groups.get(r.group)
        if old is None or (-r.amount,r.starts,r.application_id)<(-old.amount,old.starts,old.application_id):
            groups[r.group]=r
    bonuses=sum(r.amount for r in groups.values() if r.source not in MONK)
    trauma=groups['monk-trauma-global'].amount if 'monk-trauma-global' in groups else 0
    pre=max(1,base+bonuses-trauma)
    maximum=combined_maximum_hp(pre,expedition=expedition,exhaustion=exhaustion)
    return {'effectiveMaximum':maximum,'baseMaximum':base,'additiveBonuses':bonuses,
            'monkTraumaReduction':trauma,'preSystemicMaximum':pre,
            'selectedApplications':{group:r.application_id for group,r in groups.items()}}

def update_maximum(life,base,records,**options):
    report=effective_maximum(base,records,**options)
    out=apply_effective_maximum(life,report['effectiveMaximum'])
    return out,{**report,'capacityClamp':life.hp-out.hp,'actualHpDamage':0,
                'actualHpGained':0,'woundSaves':0,'deathFailuresAdded':0}

def complete_target_rest(records,target,*,completed,rest_type):
    identity(target)
    if rest_type not in ('short','long'):raise SpellRuleError('Use a completed short or long rest')
    return tuple(replace(r,present=False,ended_reason='completed-target-'+rest_type+'-rest')
                 if completed and r.target==target and r.ends_on_completed_rest and r.present
                 else r for r in records)

def threshold(hp,maximum,*,fraction=Fraction(1,2),relation='below'):
    integer(maximum,'effective maximum',1);integer(hp,'current normalHP',0,maximum)
    if not isinstance(fraction,Fraction) or not 0<=fraction<=1:
        raise SpellRuleError('Threshold requires an exact fraction from0 through1')
    left=hp*fraction.denominator;right=maximum*fraction.numerator
    if relation=='below':return left<right
    if relation=='at-or-below':return left<=right
    if relation=='above':return left>right
    if relation=='at-or-above':return left>=right
    raise SpellRuleError('Unknown threshold relation')

@dataclass(frozen=True)
class HpEventSnapshot:
    event_id: str
    before_hp: int
    after_hp: int
    effective_maximum: int
    kind: str
    def __post_init__(self):
        identity(self.event_id);integer(self.effective_maximum,'event effective maximum',1)
        integer(self.before_hp,'before HP',0,self.effective_maximum)
        integer(self.after_hp,'after HP',0,self.effective_maximum)
        if self.kind not in ('damage','direct-hp-loss','healing','capacity-change'):
            raise SpellRuleError('Unreviewed HP transition kind')
        if self.kind in ('damage','direct-hp-loss') and self.after_hp>self.before_hp:
            raise SpellRuleError('Damage/loss snapshot cannot show net healing')
        if self.kind=='healing' and self.after_hp<self.before_hp:
            raise SpellRuleError('Healing snapshot cannot show net HP loss')

    def falls_across(self,*,fraction=Fraction(1,4),inclusive=True):
        relation='at-or-below' if inclusive else 'below'
        return (self.kind in ('damage','direct-hp-loss') and self.after_hp<self.before_hp
                and not threshold(self.before_hp,self.effective_maximum,fraction=fraction,relation=relation)
                and threshold(self.after_hp,self.effective_maximum,fraction=fraction,relation=relation))

    def healed_above_half(self):
        return self.kind=='healing' and self.after_hp>self.before_hp and threshold(self.after_hp,self.effective_maximum,relation='above')

    def damage_left_below_half(self):
        # "Had reduced it below" is a stored damage predicate, not a later stat test.
        return self.kind=='damage' and self.after_hp<self.before_hp and threshold(self.after_hp,self.effective_maximum)

def pain_empowerment(hp,maximum):
    integer(maximum,'effective maximum',1);integer(hp,'current HP',0,maximum)
    return min(5,10*(maximum-hp)//maximum)

def percentage_amount(maximum,denominator,*,source_minimum=0):
    """Pure amount only. Minimum must come from printed source/viable revival bridge."""
    integer(maximum,'effective maximum',1);integer(denominator,'percentage denominator',1)
    integer(source_minimum,'explicit source minimum',0)
    return max(source_minimum,maximum//denominator)
