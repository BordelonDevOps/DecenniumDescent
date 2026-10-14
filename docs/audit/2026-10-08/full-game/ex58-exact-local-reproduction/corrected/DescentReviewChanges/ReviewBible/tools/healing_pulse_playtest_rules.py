"""Bounded pulse clocks/budgets. Source legality, actions and HP pipeline stay separate.

REVIEWED in the supplied100+6-source scope. Callers supply original virtual clock markers, canonical wallet
and shared target ledger. These helpers never cast, heal, repair, create a
companion, or infer permission to maintain a suppressed/incapacitated effect.
"""
from dataclasses import dataclass,field
from spell_playtest_rules import integer,SpellRuleError
from control_playtest_rules import ClockMarker,require_deadline


@dataclass
class PulseWallet:
    rp:int=0
    rc:int=0
    bonus_action:bool=True
    def spend(self,amount,currency='RP',*,bonus_action=False):
        integer(self.rp,'RP',0);integer(self.rc,'RC',0)
        integer(amount,'pulse cost',0)
        if currency not in ('RP','RC'):raise SpellRuleError('Unknown pulse currency')
        attr=currency.lower()
        if getattr(self,attr)<amount or (bonus_action and not self.bonus_action):
            raise SpellRuleError('Required pulse resource/action unavailable')
        setattr(self,attr,getattr(self,attr)-amount)
        if bonus_action:self.bonus_action=False


@dataclass
class RecipientLedger:
    claimed:set=field(default_factory=set)
    def check(self,domain,targets,round_number):
        integer(round_number,'numbered round',1)
        if domain and any((domain,t,round_number) in self.claimed for t in targets):
            raise SpellRuleError('Target already received this domain this numbered round')
    def commit(self,domain,targets,round_number):
        self.check(domain,targets,round_number)
        if domain:self.claimed.update((domain,t,round_number) for t in targets)


@dataclass(frozen=True)
class PulseProfile:
    mode:str
    count:int
    initial:bool=True
    later_cost:int=0
    currency:str='RP'
    fixed:bool=False
    target_cap:int=3
    round_domain:str=''
    maintenance_bonus_action:bool=True


PROFILES={
    'sacred-chant':PulseProfile('maintenance',3,target_cap=0),
    'sacrament':PulseProfile('maintenance',3,later_cost=1,target_cap=6),
    'dark-sacrament':PulseProfile('maintenance',3,later_cost=1,target_cap=6),
    'healing-briar':PulseProfile('maintenance',3,later_cost=1),
    'circle-of-harmony':PulseProfile('maintenance',3,later_cost=1,round_domain='named-circle'),
    'renewal':PulseProfile('maintenance',3,later_cost=1,round_domain='instance'),
    'renewal-extended':PulseProfile('maintenance',4,later_cost=1,round_domain='instance'),
    'restoration-field':PulseProfile('maintenance',3,later_cost=1,round_domain='instance'),
    'desecrated-ground':PulseProfile('maintenance',3,later_cost=1),
    'lifewell':PulseProfile('maintenance',3,initial=False,later_cost=1,fixed=True),
    'unfinished-chorus':PulseProfile('maintenance',2,later_cost=1,currency='RC',fixed=True,target_cap=6,round_domain='instance',maintenance_bonus_action=False),
    'song-of-mending':PulseProfile('sequence',2,later_cost=1,currency='RC',fixed=True,round_domain='instance'),
    'enhanced-song':PulseProfile('sequence',3,later_cost=1,currency='RC',fixed=True,round_domain='instance'),
    'transcendent-meditation':PulseProfile('sequence',3,fixed=True,target_cap=4),
    'eternal-bloom':PulseProfile('sequence',3,fixed=True,round_domain='instance'),
    'wound-eater-iv':PulseProfile('delayed-sequence',3,later_cost=1,currency='RC',fixed=True,round_domain='instance'),
    'hemostasis':PulseProfile('delayed-sequence',3,fixed=True,target_cap=1),
    'cellular-reconstruction':PulseProfile('delayed-sequence',1,fixed=True,target_cap=1),
    'cleric-echoes':PulseProfile('delayed-sequence',1,fixed=True,target_cap=1),
    'resonant-seed':PulseProfile('window',3,later_cost=1,currency='RC',fixed=True,target_cap=6,round_domain='instance'),
    'garden':PulseProfile('window',3,later_cost=1,currency='RC',fixed=True,target_cap=6,round_domain='instance'),
    'burning-blood-v':PulseProfile('window',3,later_cost=1,currency='RC',fixed=True,target_cap=6,round_domain='instance'),
    'crown-restored':PulseProfile('window',3,fixed=True,round_domain='instance'),
    'nano-aegis':PulseProfile('command',3,initial=False,later_cost=1,target_cap=1),
}


def distinct_targets(values,cap):
    values=tuple(values)
    if any(not isinstance(v,str) or not v for v in values) or len(values)!=len(set(values)) or len(values)>cap:
        raise SpellRuleError('Invalid, duplicate or excessive declared recipients')
    return values


@dataclass
class PulseSeries:
    instance_id:str
    profile_name:str
    activation:ClockMarker
    future_starts:tuple
    ledger:RecipientLedger
    roster:tuple=()
    # For maintenance: activation turn end, then one end for each later turn.
    maintenance_ends:tuple=()
    # Override only for an actual source-authorized duration extension, never cap.
    expires:ClockMarker|None=None
    states:list=field(init=False)
    declarations:dict=field(default_factory=dict,init=False)
    applications:set=field(default_factory=set,init=False)
    ended_at:ClockMarker|None=field(default=None,init=False)
    ended_reason:str|None=field(default=None,init=False)

    def __post_init__(self):
        if not self.instance_id or self.profile_name not in PROFILES:raise SpellRuleError('Unknown pulse instance/profile')
        self.profile=PROFILES[self.profile_name]
        require_deadline(self.activation)
        self.future_starts=tuple(require_deadline(v) for v in self.future_starts)
        needed=self.profile.count if self.profile.mode!='command' else 3
        if len(self.future_starts)!=needed or any(a>=b for a,b in zip((self.activation,)+self.future_starts,self.future_starts)):
            raise SpellRuleError('Supply strictly ordered original virtual future markers')
        self.roster=distinct_targets(self.roster,self.profile.target_cap)
        if not self.profile.fixed and self.roster:raise SpellRuleError('Repicked source has no fixed roster')
        if self.profile.mode=='maintenance':
            self.maintenance_ends=tuple(require_deadline(v) for v in self.maintenance_ends)
            opens=(self.activation,)+self.future_starts[:-1]
            if len(self.maintenance_ends)!=self.profile.count or any(not (a<b<c) for a,b,c in zip(opens,self.maintenance_ends,self.future_starts)):
                raise SpellRuleError('Supply each actual source-turn maintenance deadline')
        elif self.maintenance_ends:raise SpellRuleError('Unexpected maintenance turn ends')
        if self.expires is not None:require_deadline(self.expires)
        if self.profile.mode=='delayed-sequence':
            if self.expires is not None:raise SpellRuleError('Explicit delayed sequence ends after final opportunity')
            self.opens=self.future_starts
        elif self.profile.mode=='command':
            self.opens=()
            self.expires=self.expires or self.future_starts[-1]
        else:
            self.opens=(self.activation,)+self.future_starts[:-1]
            self.expires=self.expires or self.future_starts[-1]
        if self.expires is not None and self.expires<=self.activation:raise SpellRuleError('Invalid effect expiry')
        self.states=['pending']*self.profile.count
        if self.profile.mode=='window':
            # Initial activation funds first window; printed Final funds all.
            self.states[0]='funded'
            if self.profile.later_cost==0:self.states=['funded']*self.profile.count

    def domain(self):
        if self.profile.round_domain=='named-circle':return 'named:Circle of Harmony'
        return 'pulse:'+self.instance_id if self.profile.round_domain=='instance' else ''

    def end(self,at,reason):
        require_deadline(at)
        if self.ended_at is None:
            self.ended_at=at;self.ended_reason=reason
            self.states=['lost' if s in ('pending','funded') else s for s in self.states]

    def advance(self,now):
        """Retire missed markers; never perform catch-up healing or refund costs."""
        require_deadline(now)
        if now<self.activation:raise SpellRuleError('Cannot observe before activation')
        if self.ended_at is not None:return
        mode=self.profile.mode
        if mode=='command':
            if now>=self.expires:self.end(self.expires,'duration')
            return
        observation_limit=min(now,self.expires) if self.expires is not None else now
        if mode=='window':
            for i,status in enumerate(self.states):
                if status=='funded' and now>=self.future_starts[i]:self.states[i]='closed'
        for i,status in enumerate(self.states):
            if status!='pending':continue
            if mode=='maintenance':
                deadline=self.maintenance_ends[i]
                missed=observation_limit>=deadline
            else:
                deadline=self.opens[i];missed=observation_limit>deadline
            if not missed:continue
            self.states[i]='lost'
            if mode in ('maintenance','window') or (mode=='sequence' and i>0 and self.profile.later_cost) or (mode=='delayed-sequence' and i>0 and self.profile.later_cost):
                self.end(deadline,'missed upkeep');return
        if mode=='delayed-sequence' and all(s!='pending' for s in self.states):
            self.end(self.opens[-1],'sequence exhausted')
        elif self.expires is not None and now>=self.expires:self.end(self.expires,'duration')

    def _targets(self,targets):
        targets=distinct_targets(targets,self.profile.target_cap)
        if self.profile.fixed and not set(targets)<=set(self.roster):raise SpellRuleError('Recipient was not fixed at activation')
        return targets

    def resolve(self,index,now,targets,wallet,*,round_number,regular=True,
                upkeep_legal=True,whole_effect_suppressed=False):
        """Commit one non-window opportunity before HP outcomes.

        Caller supplies already legal declared recipients, source-specific
        ally/enemy subcaps, and source eligibility. HP blocks/fullHP are NOT
        whole-effect suppression. Whole suppression consumes clock/opportunity
        but grants no target benefit/independent component.
        """
        integer(index,'pulse index',0,self.profile.count-1)
        self.advance(now)
        if self.ended_at is not None:raise SpellRuleError('Effect ended')
        mode=self.profile.mode
        if mode in ('window','command'):raise SpellRuleError('Use the correct window/command method')
        if not regular:raise SpellRuleError('Not a regular pulse/maintenance')
        if self.states[index]!='pending':raise SpellRuleError('Opportunity already consumed')
        if any(s=='pending' for s in self.states[:index]):raise SpellRuleError('Earlier opportunity unresolved')
        exact_paid=mode in ('sequence','delayed-sequence') and index>0 and self.profile.later_cost>0
        if not upkeep_legal:
            if exact_paid and now==self.opens[index]:self.end(now,'illegal due upkeep')
            raise SpellRuleError('Not legal upkeep in current source state')
        initial_included=index==0 and self.profile.initial and mode!='delayed-sequence'
        if mode=='maintenance' and not initial_included:
            if not self.opens[index]<=now<self.maintenance_ends[index]:raise SpellRuleError('Outside maintenance window')
            needs_ba=self.profile.maintenance_bonus_action
        else:
            if now!=self.opens[index]:raise SpellRuleError('Not the exact registered due marker')
            needs_ba=False
        chosen=self._targets(targets)
        output=() if whole_effect_suppressed else chosen
        self.ledger.check(self.domain(),output,round_number)
        cost=0 if initial_included or (mode=='delayed-sequence' and index==0) else self.profile.later_cost
        try:wallet.spend(cost,self.profile.currency,bonus_action=needs_ba)
        except SpellRuleError:
            if exact_paid:self.end(now,'unpaid due pulse')
            raise
        self.ledger.commit(self.domain(),output,round_number)
        self.states[index]='committed';self.declarations[index]=chosen
        result={'pulseId':f'{self.instance_id}:{index}','occurred':True,'declaredTargets':chosen,
                'outputTargets':output,'cost':cost,'bonusActionSpent':needs_ba,
                'independentKi':1 if self.profile_name=='transcendent-meditation' and index==1 and not whole_effect_suppressed else 0}
        if mode=='delayed-sequence' and index==self.profile.count-1:self.end(now,'sequence exhausted')
        return result

    def fund(self,index,now,wallet,*,regular=True,upkeep_legal=True):
        integer(index,'window index',0,self.profile.count-1)
        self.advance(now)
        if self.ended_at is not None or self.profile.mode!='window':raise SpellRuleError('Not an active window effect')
        if not regular or now!=self.opens[index] or self.states[index]!='pending':
            raise SpellRuleError('Window funding is due once at its original source marker')
        if not upkeep_legal:
            self.end(now,'illegal due upkeep')
            raise SpellRuleError('Required window upkeep is illegal')
        try:wallet.spend(self.profile.later_cost,self.profile.currency)
        except SpellRuleError:
            self.end(now,'unpaid due window')
            raise
        self.states[index]='funded'

    def target_start(self,target,now,*,round_number,regular=True,eligible=True,
                     whole_effect_suppressed=False):
        self.advance(now)
        if self.ended_at is not None or self.profile.mode!='window':return None
        if not regular or not eligible:return None
        self._targets((target,))
        index=next((i for i in range(self.profile.count) if self.opens[i]<=now<self.future_starts[i]),None)
        if index is None or self.states[index]!='funded':return None
        if (index,target) in self.applications:return None
        integer(round_number,'numbered round',1)
        self.applications.add((index,target))
        if (self.domain(),target,round_number) in self.ledger.claimed:return None
        # A suppressed occurrence is lost; it does not deliver a named benefit.
        if not whole_effect_suppressed:self.ledger.commit(self.domain(),(target,),round_number)
        return {'pulseId':f'{self.instance_id}:{index}:{target}','occurred':True,
                'outputTargets':() if whole_effect_suppressed else (target,)}

    def command(self,now,target,wallet,*,option,command_legal=True):
        self.advance(now)
        if self.ended_at is not None or self.profile.mode!='command':raise SpellRuleError('Not an active command mode')
        if option not in ('heal','temporary-hp') or not command_legal:raise SpellRuleError('Illegal support command')
        self._targets((target,))
        try:index=self.states.index('pending')
        except ValueError:raise SpellRuleError('Command pulse cap exhausted') from None
        wallet.spend(1,'RP',bonus_action=True)
        self.states[index]='committed';self.declarations[index]=(target,)
        return {'pulseId':f'{self.instance_id}:{index}','option':option,'target':target}


def installments(reserve,count=3):
    integer(reserve,'recorded missing HP',0);integer(count,'installment count',1)
    base,remainder=divmod(reserve,count)
    return tuple(base+int(i<remainder) for i in range(count))


def renewal_branch_bases(*,parent_active,parent_covers,echo_active,echo_covers):
    """Preview legal source bases, then caller applies/compares healing branches.

    This supplied Renewal has flat2 base. Echo half occurs here, before target
    modifiers; both anchors share ONE PulseSeries and its three-recipient cap.
    No parent-destruction relationship is inferred.
    """
    result={}
    if parent_active and parent_covers:result['parent']=2
    if echo_active and echo_covers:result['echo']=1
    return result


@dataclass
class BloomReserve:
    roster_missing:dict
    consumed:set=field(default_factory=set)
    def __post_init__(self):
        distinct_targets(self.roster_missing,3)
        self.shares={target:installments(value) for target,value in self.roster_missing.items()}
    def consume(self,index,*,eligible_targets):
        integer(index,'Bloom installment',0,2)
        if index in self.consumed:raise SpellRuleError('Installment already consumed')
        if self.consumed!=set(range(index)):raise SpellRuleError('Consume every scheduled installment in order')
        eligible=set(eligible_targets)
        if not eligible<=set(self.shares):raise SpellRuleError('Bloom cannot add new entrants')
        self.consumed.add(index)
        return {target:parts[index] for target,parts in self.shares.items() if target in eligible}


@dataclass
class FirstContactLedger:
    profiles:dict
    consumed:set=field(default_factory=set)
    def __post_init__(self):
        if any(source not in ('garden','enhanced-garden','resonant-seed') for source in self.profiles.values()):
            raise SpellRuleError('Unknown cure contact source')
    def claim(self,instance,target,*,event,eligible=True):
        if instance not in self.profiles:raise SpellRuleError('Unknown contact instance')
        source=self.profiles[instance]
        if event not in ('entry','pulse','start'):raise SpellRuleError('Unknown contact event')
        if not eligible or (source=='resonant-seed' and event!='pulse') or (source=='enhanced-garden' and event!='pulse'):
            return False
        key=(instance,target)
        if key in self.consumed:return False
        self.consumed.add(key)
        return True


NATIVE_COSTS={'aura-of-grace':1,'living-pulse':1,'thief-exsanguinate':1,
              'regenerative-mutation':0,'bloodthick-node':0,'rapid-coagulation':0}


@dataclass
class NativeOccurrenceLedger:
    consumed:set=field(default_factory=set)
    def commit(self,source,owner,marker,wallet,*,regular=True,eligible=True):
        if source not in NATIVE_COSTS:raise SpellRuleError('Unknown native recurrence source')
        require_deadline(marker)
        if not owner:raise SpellRuleError('Native pulse needs owner identity')
        key=(source,owner,marker)
        if not regular or not eligible or key in self.consumed:return False
        wallet.spend(NATIVE_COSTS[source])
        self.consumed.add(key)
        return True
