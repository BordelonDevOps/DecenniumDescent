# Pulse implementation corrections and exact final disposition

Codex → Calibration Review. Please replyunder12,000characters withremainingconcretedefects orboundeddisposition.

Your exactimplementationreview was preserved separatelyfrom thelaternotebook provenance instruction. Implemented requiredfixes:

- Sequence/delayedsequence laterpaidmarker: iflegalwalletpaymentfails, effectendsatdue marker beforeanytargetledger/declarationcommit. Song/EnhancedSong/WoundEater cannotretrywithnewRCatsamemarker.
- Exactpaidmarker withupkeep_legal=False nowendsatthatduemarker. Oraclefund alsoendswhenactualrequiredsourceupkeepisillegal.
- regular=False onextra-turnattemptrejectswithoutendingattheactualsame pendingmarker; by-turn-endmaintenance failed early payment remainspendinguntildueend.
- Addedreplay, illegalupkeep, extrasourcecall andsuppressedCircle sharedbenefitledger regressions.
- EnhancedGarden entitlement nowlabeled NEWsource-specificmasteryintegration, asapproved; UnfinishedChorustwopulse/noBAandEchoRenewalvsBlightarbitrationdistinctionretained.

Current89targetedchecks+301reservepartitionsPASS. Addedexplicitprovenancemap:24scheduleprofiles+6nativeprofiles+3contactvariants=33alllinkedtoactualsupplied100+6sourceIDs. No newability/spellnamesorcontentintroduced. Internalshortlabelsarealiases, notadditionalcards. Originalsourceobjects/frozenclassguide remainunchanged. All priorcallerboundariesremain: actualinitialcosts, acquisition, source/target/sidecaplegality, originalvirtualmarkers, canonicalwallet/actioneconomy, objectlifeandcompanioncommandbudgets, andactualhealingpipeline/independentcomponentresolution.

Full correctedhelper/tests/guide/reports/mappings below. Original100sourcebindingtexts areunchanged fromexactpacket; sourceintegrityPASS100+6. Pleasecloseonlythe supplied scheduling/roleinterfaceifappropriate, leavingfullcards/companionlife/770unfinishedspells/othercatalogs/wholegameopen.

Nextpreparedreview:74device/Totem passages (73lexicalTinker/Shaman + explicitMagneticWallsemanticaddition) plus3frozenguidesources. MagneticWallwasnotinprior39redirectionset andwasmissedbyfuture230lexicalpattern; itisnowcapturedandhashverified explicitly. Noassumptionthatlexicalcountsmeantcompleteness.


## tools/healing_pulse_playtest_rules.py

"""Bounded pulse clocks/budgets. Source legality, actions and HP pipeline stay separate.

IN REVIEW. Callers supply the original virtual clock markers, canonical wallet
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


## tools/validate_healing_pulse_playtests.py

"""Adversarial scheduling/budget checks; does not certify full source execution."""
from pathlib import Path
import json
from healing_pulse_playtest_rules import *
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
    def series(profile,ident='effect',roster=(),ledger=None,activation=None,expires=None):
        p=PROFILES[profile];n=p.count if p.mode!='command' else 3
        starts=tuple(ClockMarker(6*(i+1)) for i in range(n))
        ends=tuple(ClockMarker(6*i,20) for i in range(n)) if p.mode=='maintenance' else ()
        return PulseSeries(ident,profile,activation or ClockMarker(0,5),starts,
                           ledger or RecipientLedger(),roster,ends,expires)
    w=PulseWallet(rp=8);briar=series('healing-briar')
    a=briar.resolve(0,ClockMarker(0,5),('a','b'),w,round_number=1)
    check('Initial Briar included without BA/additionalRP',(a['cost'],w.rp,w.bonus_action),(0,8,True))
    a=briar.resolve(1,ClockMarker(6,10),('c',),w,round_number=2)
    check('Later Briar repicks before outcomes and pays BA1RP',(a['declaredTargets'],w.rp,w.bonus_action),(('c',),7,False))
    rejects('Cannot replay paid pulse',lambda:briar.resolve(1,ClockMarker(6,11),('d',),w,round_number=2))
    check('Replay never charges again',w.rp,7)
    briar.advance(ClockMarker(12,20))
    check('Missed upkeep ends at due turn end',(briar.ended_at,briar.ended_reason),(ClockMarker(12,20),'missed upkeep'))
    rejects('Cannot resume missed upkeep',lambda:briar.resolve(2,ClockMarker(18,10),('a',),PulseWallet(rp=4),round_number=4))
    lw=series('lifewell',roster=('a','b'));w=PulseWallet(rp=8)
    a=lw.resolve(0,ClockMarker(0,10),('a',),w,round_number=1)
    check('Lifewell first pulse already costs BA1RP',(w.rp,w.bonus_action,a['cost']),(7,False,1))
    rejects('Lifewell cannot replace fixed target',lambda:lw.resolve(1,ClockMarker(6,10),('new',),PulseWallet(rp=4),round_number=2))
    absent=series('lifewell',roster=('a',));absent.advance(ClockMarker(0,20))
    check('No Lifewell first BA ends at activation turn end',absent.ended_at,ClockMarker(0,20))
    b=series('dark-sacrament');w=PulseWallet(rp=3)
    b.resolve(0,ClockMarker(0,5),('ally','enemy'),w,round_number=1)
    b.resolve(1,ClockMarker(6,10),(),w,round_number=2)
    check('Empty legal DarkSacrament pulse maintains with BA1RP',(w.rp,w.bonus_action,b.states[1]),(2,False,'committed'))
    b=series('restoration-field');w=PulseWallet(rp=4)
    b.resolve(0,ClockMarker(0,5),('full','decayed'),w,round_number=1)
    b.resolve(1,ClockMarker(6,10),('full','decayed'),w,round_number=2)
    check('Full/Decay outcomes cannot refund committed Field',(w.rp,b.declarations[1]),(3,('full','decayed')))
    b=series('renewal-extended');w=PulseWallet(rp=5)
    b.resolve(0,ClockMarker(0,5),('a',),w,round_number=1)
    for i in (1,2,3):
        w.bonus_action=True;b.resolve(i,ClockMarker(i*6,10),('a',),w,round_number=i+1)
    check('Extended Renewal fourth requires total3upkeepRP',w.rp,2)
    rejects('Extended Renewal never fifth',lambda:b.resolve(4,ClockMarker(24,10),('a',),w,round_number=5))
    b.advance(ClockMarker(24));check('Extended Renewal expires startturn5',b.ended_at,ClockMarker(24))
    circles=RecipientLedger()
    c1=series('circle-of-harmony','c1',ledger=circles)
    c2=series('circle-of-harmony','c2',ledger=circles)
    c1.resolve(0,ClockMarker(0,5),('a',),PulseWallet(),round_number=1)
    rejects('Circle named cap crosses owner instances',lambda:c2.resolve(0,ClockMarker(0,5),('a',),PulseWallet(),round_number=1))
    c2.resolve(0,ClockMarker(0,5),('b',),PulseWallet(),round_number=1)
    check('Other legal Circle target still available',c2.declarations[0],('b',))
    common=RecipientLedger()
    f1=series('restoration-field','f1',ledger=common);f2=series('restoration-field','f2',ledger=common)
    for f in (f1,f2):f.resolve(0,ClockMarker(0,5),('a',),PulseWallet(),round_number=1)
    check('Independent Field instances may each affect same target',len(common.claimed),2)
    ren1=series('renewal','r1',ledger=common);ren2=series('renewal','r2',ledger=common,activation=ClockMarker(0,6))
    ren1.resolve(0,ClockMarker(0,5),('a',),PulseWallet(),round_number=1)
    ren2.resolve(0,ClockMarker(0,6),('a',),PulseWallet(),round_number=1)
    check('Separate Renewal scheduled moments not global round banned',len(common.claimed),4)
    song=series('song-of-mending',roster=('a',));w=PulseWallet(rc=1)
    song.resolve(0,ClockMarker(0,5),('a',),w,round_number=1)
    song.resolve(1,ClockMarker(6),('a',),w,round_number=2)
    check('Song second pulse consumes1RC withoutBA',(w.rc,w.bonus_action),(0,True))
    song=series('enhanced-song',roster=('a',));w=PulseWallet(rc=2)
    for i,at in enumerate(song.opens):song.resolve(i,at,('a',),w,round_number=i+1)
    check('EnhancedSong both laterpulses cost2RC',w.rc,0)
    meditation=series('transcendent-meditation',roster=('owner','a'))
    meditation.resolve(0,ClockMarker(0,5),('owner','a'),PulseWallet(),round_number=1)
    event=meditation.resolve(1,ClockMarker(6),('owner','a'),PulseWallet(),round_number=2)
    check('Meditation independentKi even when callerblocksallHP',event['independentKi'],1)
    meditation=series('transcendent-meditation',roster=('owner',))
    meditation.resolve(0,ClockMarker(0,5),('owner',),PulseWallet(),round_number=1)
    event=meditation.resolve(1,ClockMarker(6),('owner',),PulseWallet(),round_number=2,whole_effect_suppressed=True)
    check('EntireMeditation suppressed losesHPoutputsandKi',(event['outputTargets'],event['independentKi']),((),0))
    wound=series('wound-eater-iv',roster=('e',));w=PulseWallet(rc=2)
    rejects('WoundEater no activation drain',lambda:wound.resolve(0,ClockMarker(0,5),('e',),w,round_number=1))
    for i,at in enumerate(wound.opens):event=wound.resolve(i,at,('e',),w,round_number=i+2)
    check('Delayedthirdpulse resolves BEFOREsequenceends',(wound.states,w.rc,wound.ended_at),(['committed']*3,0,ClockMarker(18)))
    hemo=series('hemostasis',roster=('a',))
    for i,at in enumerate(hemo.opens):hemo.resolve(i,at,('a',),PulseWallet(),round_number=i+2)
    check('Hemostasis includes exactlythirdtargetstart',hemo.states,['committed']*3)
    hemo=series('hemostasis',roster=('a',))
    hemo.advance(ClockMarker(7))
    check('Lateobservation missesfirsttick withoutcatchup',hemo.states,['lost','pending','pending'])
    hemo.resolve(1,ClockMarker(12),('a',),PulseWallet(),round_number=3)
    check('Later prepaidtickstillresolves',hemo.states[1],'committed')
    g=series('garden',roster=('a','owner'));w=PulseWallet(rc=2)
    event=g.target_start('a',ClockMarker(3),round_number=1)
    check('Activation-funded Garden window permitsone targetstart',event['outputTargets'],('a',))
    check('Samewindow replay blocked',g.target_start('a',ClockMarker(3),round_number=1),None)
    g.fund(1,ClockMarker(6),w)
    check('Newwindow cannot bypass numberedround',g.target_start('a',ClockMarker(6,1),round_number=1),None)
    g.fund(2,ClockMarker(12),w)
    check('Newround eligible Garden pulse',g.target_start('a',ClockMarker(15),round_number=3)['outputTargets'],('a',))
    check('Garden pays perwindow notperrecipient',w.rc,0)
    check('Garden expires beforeownerthirdfuturestart',g.target_start('owner',ClockMarker(18),round_number=4),None)
    g=series('garden',roster=('a',));g.advance(ClockMarker(7))
    check('Missedfunding ends atoriginalduemarker',g.ended_at,ClockMarker(6))
    g=series('garden',roster=('a',))
    rejects('Unpayableduewindowrejects',lambda:g.fund(1,ClockMarker(6),PulseWallet()))
    check('Unpayableduewindowends immediately',g.ended_at,ClockMarker(6))
    crown=series('crown-restored',roster=('owner',))
    got=[]
    for n in (1,2,3):
        if crown.target_start('owner',ClockMarker(6*n),round_number=n+1):got.append(n)
    check('CrownselfBAcast can onlyreceive2 beforeexpiry',got,[1,2])
    crown=series('crown-restored',roster=('a',))
    rejects('Crowncannotaddunselectedentrants',lambda:crown.target_start('new',ClockMarker(3),round_number=1))
    check('Extra targetturn creates no pulse',crown.target_start('a',ClockMarker(3),round_number=1,regular=False),None)
    crown.target_start('a',ClockMarker(3),round_number=1,whole_effect_suppressed=True)
    check('Suppressed occurrence cannotcatchup',crown.target_start('a',ClockMarker(4),round_number=1),None)
    reserve=BloomReserve({'a':10,'b':1})
    check('Bloom remainder toearlierinstallments',reserve.shares,{'a':(4,3,3),'b':(1,0,0)})
    check('Bloom first declaredreserve',reserve.consume(0,eligible_targets=('a','b')),{'a':4,'b':1})
    check('Outside target loses middleinstallment',reserve.consume(1,eligible_targets=()),{})
    check('Reentry gets thirdonly, no accumulatedmissing',reserve.consume(2,eligible_targets=('a',)),{'a':3})
    rejects('Bloom installment cannotreplay',lambda:reserve.consume(2,eligible_targets=('a',)))
    rejects('Bloom cannotnewroster',lambda:BloomReserve({'a':10}).consume(0,eligible_targets=('new',)))
    contacts=FirstContactLedger({'g':'garden','s':'resonant-seed','eg':'enhanced-garden'})
    check('Gardenentrycure independent ofHP',contacts.claim('g','a',event='entry'),True)
    check('Gardenlaterpulse cannotdoublecure',contacts.claim('g','a',event='pulse'),False)
    check('Seedentry is notfirstpulse',contacts.claim('s','a',event='entry'),False)
    check('Seedfirstpulse cure evenHPblocked',contacts.claim('s','a',event='pulse'),True)
    check('EnhancedGardenexplicitfirstpulsetiming',contacts.claim('eg','a',event='entry'),False)
    nano=series('nano-aegis');w=PulseWallet(rp=4)
    check('Nano noinitialheal',nano.states,['pending']*3)
    nano.advance(ClockMarker(6))
    check('SkippingNano commanddoesnotend',nano.ended_at,None)
    for i in (1,2,3):
        w.bonus_action=True;nano.command(ClockMarker(6,i),'a',w,option='heal')
    check('Nano printedcap independent ofcallercommandceiling',w.rp,1)
    rejects('Nano4thpulseprohibited',lambda:nano.command(ClockMarker(12),'a',w,option='heal'))
    nano=series('nano-aegis');w=PulseWallet(rp=2,bonus_action=False)
    rejects('ExtraActionalone cannotpayrequiredBA',lambda:nano.command(ClockMarker(6),'a',w,option='temporary-hp'))
    check('RejectedNano command noRPcharged',w.rp,2)
    nano=series('nano-aegis',expires=ClockMarker(60));w=PulseWallet(rp=4)
    for i in (1,2,3):
        w.bonus_action=True;nano.command(ClockMarker(i*12),'a',w,option='heal')
    rejects('Overdrivecannotcreate4thhealingpulse',lambda:nano.command(ClockMarker(48),'a',w,option='heal'))
    native=NativeOccurrenceLedger();w=PulseWallet(rp=10)
    for i in range(5):native.commit('aura-of-grace','cleric',ClockMarker(6*i),w)
    check('Nativefivepaidregularpulses',(len(native.consumed),w.rp),(5,5))
    check('Nativereplaynofee',native.commit('aura-of-grace','cleric',ClockMarker(24),w),False)
    check('Nativeextraturnnofee',native.commit('aura-of-grace','cleric',ClockMarker(25),w,regular=False),False)
    rejects('Unknownsourceprofile',lambda:PulseSeries('x','invented',ClockMarker(0),(),RecipientLedger()))
    shifted=PulseSeries('phase','song-of-mending',ClockMarker(2),(ClockMarker(6),ClockMarker(12)),RecipientLedger(),('a',))
    shifted.resolve(0,ClockMarker(2),('a',),PulseWallet(rc=1),round_number=1)
    check('Existingvirtualphase retainsnext6 notactivationplus6',shifted.opens[1],ClockMarker(6))
    early=series('song-of-mending',roster=('a',),expires=ClockMarker(4))
    early.resolve(0,ClockMarker(0,5),('a',),PulseWallet(),round_number=1)
    early.advance(ClockMarker(20))
    check('Actual earlierexpiry notoverwrittenbylatermissedupkeep',early.ended_at,ClockMarker(4))
    unpaid=series('lifewell',roster=('a',));w=PulseWallet(rp=0)
    rejects('UnpayableBApulse chargesnoaction',lambda:unpaid.resolve(0,ClockMarker(0,10),('a',),w,round_number=1))
    check('UnpayableBApulse remainsunspent untildeadline',(w.bonus_action,unpaid.states[0]),(True,'pending'))
    check('Echoonly active anchor yieldssourcebase1',renewal_branch_bases(parent_active=False,parent_covers=True,echo_active=True,echo_covers=True),{'echo':1})
    check('Overlap suppliesalternativebases neveradds',renewal_branch_bases(parent_active=True,parent_covers=True,echo_active=True,echo_covers=True),{'parent':2,'echo':1})
    renewal=series('renewal')
    rejects('ParentplusEcho do notcreate6targetbudget',lambda:renewal.resolve(0,ClockMarker(0,5),('a','b','c','d'),PulseWallet(),round_number=1))
    check('Rejectedexcessrecipientsdoesnotconsumepulse',renewal.states[0],'pending')
    chorus=series('unfinished-chorus',roster=('enemy','ally'));w=PulseWallet(rc=1)
    chorus.resolve(0,ClockMarker(0,5),('enemy','ally'),w,round_number=1)
    chorus.resolve(1,ClockMarker(6,10),('enemy','ally'),w,round_number=2)
    check('Choruslaterownturnpulse1RC no inventedBA',(w.rc,w.bonus_action),(0,True))
    for profile in ('song-of-mending','enhanced-song','wound-eater-iv'):
        s=series(profile,roster=('a',));w=PulseWallet()
        s.resolve(0,s.opens[0],('a',),w,round_number=1)
        due=s.opens[1]
        rejects(profile+' unpaid exactdue rejects',lambda:s.resolve(1,due,('a',),w,round_number=2))
        check(profile+' unpaid exactdue ends immediately',(s.ended_at,w.rc,s.declarations.get(1)),(due,0,None))
        rejects(profile+' cannotretry same marker afteracquiringRC',lambda:s.resolve(1,due,('a',),PulseWallet(rc=1),round_number=2))
    s=series('song-of-mending',roster=('a',))
    s.resolve(0,s.opens[0],('a',),PulseWallet(),round_number=1)
    rejects('IllegalSongdueupkeep rejects',lambda:s.resolve(1,s.opens[1],('a',),PulseWallet(rc=1),round_number=2,upkeep_legal=False))
    check('IllegalSongdueupkeep endsatmarker',s.ended_at,s.opens[1])
    s=series('garden',roster=('a',));w=PulseWallet(rc=2)
    rejects('IllegalGardenduefunding rejects',lambda:s.fund(1,ClockMarker(6),w,upkeep_legal=False))
    check('IllegalGardenduefunding endswithoutpayment',(s.ended_at,w.rc),(ClockMarker(6),2))
    s=series('garden',roster=('a',))
    rejects('Extra-turnfundattempt rejects',lambda:s.fund(1,ClockMarker(6),PulseWallet(rc=2),regular=False))
    check('Extraturndoesnotitselfterminatependingrealmarker',s.ended_at,None)
    s.fund(1,ClockMarker(6),PulseWallet(rc=1))
    check('Actualregularfunding remainslegal afterextraattempt',s.states[1],'funded')
    shared=RecipientLedger()
    s1=series('circle-of-harmony','suppressed-circle',ledger=shared)
    s2=series('circle-of-harmony','operative-circle',ledger=shared)
    event=s1.resolve(0,s1.opens[0],('a',),PulseWallet(),round_number=1,whole_effect_suppressed=True)
    check('SuppressedCircle consumesownpulse withoutnamedbenefit',(s1.states[0],event['outputTargets'],len(shared.claimed)),('committed',(),0))
    s2.resolve(0,s2.opens[0],('a',),PulseWallet(),round_number=1)
    check('OtheroperativeCircle canbenefit sametargetround',len(shared.claimed),1)
    states=0
    for reserve_value in range(301):
        parts=installments(reserve_value)
        assert len(parts)==3 and sum(parts)==reserve_value and max(parts)-min(parts)<=1 and tuple(sorted(parts,reverse=True))==parts
        states+=1
    report={'status':'PASS','reviewStatus':'IN_REVIEW','checkCount':len(checks),'reservePartitionStates':states,
            'scope':'Bounded source/target pulse clocks, resource/action commitments, fixed/repicked targets, named/instance round budgets, reserves and contact entitlements. Caller owns actual target eligibility, subgroup caps, canonical action economy, anchor/device lifecycle and healing outputs.','checks':checks}
    (ROOT/'docs/mechanics/HEALING_PULSE_PLAYTEST_VALIDATION.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(f'PASS{len(checks)} pulse checks;{states} reserve partition states. Exact review pending.')
if __name__=='__main__':main()


## docs/mechanics/HEALING_PULSE_PLAYTEST.md

# Healing pulses, sustained zones and upkeep

**IN REVIEW.** The100 source candidates have individual discussion roles in the [source register](HEALING_PULSE_SOURCE_BINDINGS.md); many are guards, one-time effects or already reviewed modifiers. The [boundary conference](../../../../docs/audit/2026-10-08/full-game/GPT_HEALING_PULSE_BOUNDARIES.md) corrects the first proposals. Original cards, books and the frozen class guide remain unchanged.

This overlay defines the supplied recurring-healing schedules. Each legal healing application still uses the [healing interface](HEALING_DEATH_PLAYTEST.md). Resource cost, pulse occurrence, actual HP restored and independent cure/resource components are different events.

Every internal schedule, native recurrence and cure-variant label has an [explicit source mapping](../../data/playtest/healing_pulse_profiles.json), checked by the [profile provenance report](HEALING_PULSE_PROFILE_PROVENANCE.json). These labels add no new spells or abilities. New integration decisions remain labeled separately from preserved source text.

## Keep the original clock

Use the original source or target regular-turn markers. Extra turns do not advance periodic healing, refill opportunities, generate upkeep, or reset these deadlines. Leaving/reentering initiative, reordering and source removal do not restart clocks.

Outside initiative preserve existing virtual markers. For activation at second2 with source starts0/6/12/18, later starts are6/12, not8/14. Establish one coherent six-second virtual schedule only when none exists. Bare outside-initiative round durations still use their separately reviewed absolute deadline; do not run both timing models for one component.

Ordinary start-expiry precedes start triggers. Explicit finite sequences own their printed due opportunities: Hemostasis's third target-start tick and Wound Eater IV's third source-start tick resolve before their sequence ends. A three-round target-start aura instead expires at its normal source deadline even if a creature received fewer than three pulses.

## Source schedules

Activation costs below are paid before the series exists; quoted later costs never refund an activation, limited use, BG, Ki, slot or Conviction.

| Source | First opportunity | Later opportunities and cost | End |
|---|---|---|---|
| Lifewell | Action4RP + all BG (at least3) establishes it; first same-turn heal still needs BA+1RP | Next2 regular source turns, each BA+1RP; fixed≤3 allies | Missed maintenance: that source turn end; otherwise startturn4 |
| Healing Briar | Action4RP includes first heal | Next2 regular turns BA+1RP; repick≤3 living allies in fixed natural-ground zone | Same |
| Circle of Harmony | Action2Ki+3RP includes first heal | Next2 regular turns BA+1RP; repick≤3 living allies in fixed zone | Same |
| Restoration Field | Action3RP + slot includes first heal | Next2 regular turns BA+1RP; repick≤3 living allies/functional devices | Same; this exact lifetime is a labeled default integration |
| Renewal Totem | Action2RP includes first heal | Next2 regular turns BA+1RP; repick≤3 allies | Same; Extended Totem adds one paid fourth turn and expires startturn5 |
| Sacred Chant | Action1RP includes nonhealing pulse1 | Next2 regular turns BA,0RP | Same; printed Conviction only, no invented healing |
| Sacrament / Dark Sacrament | Printed Action/Conviction/RP includes first pulse | Next2 regular turns BA+1RP, supplied by Cleric engine5 | Same; up to3 allies and3 qualifying enemies separately |
| Desecrated Ground | Action7RP includes first damage pulse | Next2 regular turns BA+1RP,≤3 enemies | Same; no healing output |
| Song of Mending | Action3RC includes pulse1, fixed≤3 allies | Source-next-regular-start pulse2 costs1RC; Enhanced adds second-later-start pulse3 for another1RC | Unpaid due pulse ends immediately; normal2/3-round duration otherwise |
| Unfinished Chorus | Action3RC includes first source-turn drain | One later regular source-turn drain costs1RC, no invented upkeep action; choose from the fixed zone set | Two-round deadline; missed upkeep ends that source turn |
| Transcendent Meditation | Action3Ki+4RP/short-rest use includes pulse1 | Next2 source regular starts, prepaid, fixed self+≤3 allies | Normal3-source-turn duration; concentration required |
| Eternal Bloom | Final Action/long-rest use; activation installment1 | Next2 source regular starts; prepaid installments2/3 | Normal3-round duration; no extraRC |
| Wound Eater IV | BA2RC establishes aura; first drain at next source regular start | Following2 source starts cost1RC each | After third pulse; unpaid later pulse ends at its due marker |
| Hemostasis | Pay printed additional1RP with eligible application | Next3 target regular starts, prepaid | After third opportunity |
| Cellular Reconstruction / Cleric Echoes | Printed activation/trigger stores one delayed event | Next source regular start, prepaid | After that opportunity; full stasis/copy rules are separately owned |
| Nano-Aegis Drone | Action2RP enters support mode; no immediate heal | Each legal BA command costs1RP; choose heal OR temporaryHP; at most3 total | Three-round mode; skipping command does not end mode |

All listed concentration requirements remain. Starting replacement concentration or becoming Incapacitated ends those effects immediately. An effect with no concentration requirement does not gain one merely because it is in this table. Incapacity still prevents required actions. A suppressed maintenance activation is illegal if the actual suppression says so; output suppression alone need not prevent an otherwise legal payment.

For ordinary paid three-pulse effects, maintenance must occur by the end of the corresponding regular source turn. Missing it ends the effect at that turn's end, with no later resumption. Lifewell also checks its activation turn. Paying early for a future turn is not permitted. A legal empty pulse can maintain a source that permits up toN targets; it consumes its cost and opportunity.

Song, Enhanced Song, Wound Eater IV and Oracle funded windows require later payment at their exact registered due marker. If that payment is unavailable or the upkeep is illegal then, the effect ends immediately at that marker. Later resources cannot retry it at the same marker. An early failed attempt at ordinary turn-window maintenance instead leaves that opportunity pending until its actual turn-end deadline. An extra-turn call is not a due regular marker and grants no payment, opportunity or automatic termination.

**Worked Lifewell example:** starting with12RP and3BG, activation plus first BA pulse spends5RP and all3BG, leaving7RP. Turn2 maintenance leaves6RP; turn3 leaves5RP. Losing the turn2 maintenance ends Lifewell that turn; neither the daily use nor first payments return.

## Oracle target-start windows

Garden, Resonant Seed and Burning Blood V have activation-funded window1. At each of the next two original source regular starts, pay1RC once to fund the next window, or end the effect. No upkeep action is invented. Each window ends at the following source regular start. Their persistent zones require concentration and fixed sets of at most3 allies and3 enemies, as applicable to each source.

Burning Blood V is a Curse Boon, separately gained alongside the Mystery Final; it receives no Final payment exemption. Its enemy-start damage does not turn its once-on-your-turn self-healing trigger into a heal on every enemy turn.

Crown Restored is a Final: its finite windows are prepaid, with no generic extraRC. Its fixed ally set contains at most3 including the Oracle if selected. A BA self-cast after that turn's start can give the Oracle only2 subsequent self-start heals before startturn4 expiry. Maximum3 per creature is a cap, not a promise.

Evaluate target-start effects on that target's original regular marker while it is eligible and inside the live zone. Both the funded window and numbered-round budget must be available. Entry/reentry or moving a Totem does not create entry healing. An ally that missed a start while outside loses that opportunity; it does not bank healing.

Oracle zone benefits use one fixed set across healing, floors, immunity and other aura benefits unless a source explicitly separates sets. Eternal Bloom's chosen≤3 living allies must be inside at activation; new entrants gain no reserve, floor or necrotic immunity. Selected targets regain applicable continuous benefits on legal reentry while the source remains active.

## Targets, payments and separate budgets

Declare legal recipients before rolling or learning outcomes. Fixed targets cannot be replaced. For repicked sources, select a new legal set for each pulse before its outcomes. Loss of eligibility after declaration skips that application without replacing it or refunding payment.

Commit the legal upkeep action/resource and opportunity before HP resolution. Full HP, Decay and zero actual healing do not refund costs, restore a pulse, or allow a replacement target. Healing prohibition does not automatically suppress an independent printed cure. All source target restrictions, ally/enemy subcaps and clear line of effect remain caller responsibilities.

| Budget | Domain |
|---|---|
| Circle of Harmony | NEW global named effect + target + numbered round, across owners |
| Restoration Field | Field instance + target + numbered round |
| Oracle engine26 | Zone instance + target + numbered round, plus one application per funded window |
| Renewal + its Echo | One parent-family instance, one pulse ID, one up-to3 recipient budget and target/round ledger |
| Separate Renewal instances | No invented global once/round ceiling; simultaneous same-opportunity overlap uses the strongest legal branch |
| Nano-Aegis | Printed max3 commands per mode; caller enforces the applicable shared companion command limit |

A paid pulse at a distinct scheduled time from another independent Renewal can heal in the same round. Same-opportunity overlapping Renewal auras never add together.

Parent/Echo Renewal shares one upkeep payment, concentration and opportunity. From legal coverage, parent source base is2 and Echo source base is1. Construct the separate legal branches with correct modifier placement, select the stronger preview, then commit one healing application. Never add both or halve the already modified parent final heal. This is a source-specific new scheduling/arbitration integration; the existing Blight Totem reduction comparison is a different rule.

The scheduler takes each anchor's active/coverage state from the future object lifecycle. Parent destruction does not yet authorize this package to destroy or preserve its Echo. Both anchors never supply a six-target budget.

## Finite installments and independent components

Eternal Bloom records each chosen ally's missingHP at activation. Divide into3 integer installments; assign remainder to earlier pulses:10 becomes4/3/3,1 becomes1/0/0. At each scheduled opportunity consume the next installment. Outside, dead or suppressed targets lose it. Returning later never recovers the lost share, and new damage never grows the original reserve.

Bloom's once-per-selected-ally 1HP floor is separately tracked by the already reviewed survival interface. It neither consumes nor replenishes installments. The target must still be eligible and inside; full healing prohibition does not turn prevention into healing.

Garden gives a first-entry-or-start cure opportunity independent of HP gain. Seed's cure belongs to its first healing pulse, not entry. **New source-specific mastery integration, confirmed in exact review:** Enhanced Garden replaces this with its printed first-pulse cure-both opportunity, using one entitlement rather than granting both an entry cure and a second enhanced cure.

Transcendent Meditation's second pulse supplies its printed1Ki even if every HP gain is blocked. Suppressing the whole effect also suppresses Ki for that occurrence; suppressing only healing does not. No missed independent component is banked.

Hemostasis and other prepaid effects preserve each target/source clock. A late observation records missed opportunities without performing catch-up recovery.

Hemostasis permits only one such healing effect per target. Creating a separate series does not authorize stacking a second instance; the caller enforces active-effect eligibility. For Unfinished Chorus the fixed zone roster remains≤3 allies/3 enemies, but a drain chooses only one eligible enemy and one healing destination (self or one eligible ally) per pulse.

## Native recurrence and device limits

Aura of Grace, Living Pulse and Thief Exsanguinate retain their optional1RP regular-start heal and their printed eligibility gates. Regenerative Mutation, Bloodthick Node and Rapid Coagulation retain their real-encounter, mutation and movement gates and spend Mutation Recovery Reserve per actual HP restored. Bio-Stabilizer modifies Bloodthick; it is not another pulse.

These native effects have no generic three-pulse ceiling. Extra turns provide no new periodic recovery tick. Explicit restrictions on Downed, Incapacitated, enemy proximity or natural terrain remain source-specific.

Efficient Power Cells extends eligible nonhealing deployments only. Mech Overdrive extends eligible device duration, never healing capacity, charges, ammunition or resource recovery. A disabled device's duration continues. Whether it can accept a support command or maintenance depends on the actual disabled-state rule; the scheduler grants no permission.

## Reference boundary

The reference helper accepts already paid legal activation, exact original clock markers, a canonical wallet/action state and a shared recipient ledger. It does not itself pay initial BG/Conviction/Ki, enforce acquisition, choose targets, roll/heal, compute Echo final previews, implement object destruction, or execute the entire companion command engine.

Profile target caps of6 for mixed Oracle/Cleric effects mean3 allies plus3 eligible enemies, not6 of one side. The caller must validate these subcaps before creating a fixed roster or committing recipients. The helper's generic recipient count does not grant broader targeting.

Source-qualified independent components and remaining guard/exclusion records retain their separate guides. The supplied100 class passages and the negative scan of78 operational spell drafts do not cover770 unfinished spells or unsupplied items/monsters.


## docs/mechanics/HEALING_PULSE_PLAYTEST_VALIDATION.json

{
  "status": "PASS",
  "reviewStatus": "IN_REVIEW",
  "checkCount": 89,
  "reservePartitionStates": 301,
  "scope": "Bounded source/target pulse clocks, resource/action commitments, fixed/repicked targets, named/instance round budgets, reserves and contact entitlements. Caller owns actual target eligibility, subgroup caps, canonical action economy, anchor/device lifecycle and healing outputs.",
  "checks": [
    {
      "name": "Initial Briar included without BA/additionalRP",
      "result": "PASS"
    },
    {
      "name": "Later Briar repicks before outcomes and pays BA1RP",
      "result": "PASS"
    },
    {
      "name": "Cannot replay paid pulse",
      "result": "PASS"
    },
    {
      "name": "Replay never charges again",
      "result": "PASS"
    },
    {
      "name": "Missed upkeep ends at due turn end",
      "result": "PASS"
    },
    {
      "name": "Cannot resume missed upkeep",
      "result": "PASS"
    },
    {
      "name": "Lifewell first pulse already costs BA1RP",
      "result": "PASS"
    },
    {
      "name": "Lifewell cannot replace fixed target",
      "result": "PASS"
    },
    {
      "name": "No Lifewell first BA ends at activation turn end",
      "result": "PASS"
    },
    {
      "name": "Empty legal DarkSacrament pulse maintains with BA1RP",
      "result": "PASS"
    },
    {
      "name": "Full/Decay outcomes cannot refund committed Field",
      "result": "PASS"
    },
    {
      "name": "Extended Renewal fourth requires total3upkeepRP",
      "result": "PASS"
    },
    {
      "name": "Extended Renewal never fifth",
      "result": "PASS"
    },
    {
      "name": "Extended Renewal expires startturn5",
      "result": "PASS"
    },
    {
      "name": "Circle named cap crosses owner instances",
      "result": "PASS"
    },
    {
      "name": "Other legal Circle target still available",
      "result": "PASS"
    },
    {
      "name": "Independent Field instances may each affect same target",
      "result": "PASS"
    },
    {
      "name": "Separate Renewal scheduled moments not global round banned",
      "result": "PASS"
    },
    {
      "name": "Song second pulse consumes1RC withoutBA",
      "result": "PASS"
    },
    {
      "name": "EnhancedSong both laterpulses cost2RC",
      "result": "PASS"
    },
    {
      "name": "Meditation independentKi even when callerblocksallHP",
      "result": "PASS"
    },
    {
      "name": "EntireMeditation suppressed losesHPoutputsandKi",
      "result": "PASS"
    },
    {
      "name": "WoundEater no activation drain",
      "result": "PASS"
    },
    {
      "name": "Delayedthirdpulse resolves BEFOREsequenceends",
      "result": "PASS"
    },
    {
      "name": "Hemostasis includes exactlythirdtargetstart",
      "result": "PASS"
    },
    {
      "name": "Lateobservation missesfirsttick withoutcatchup",
      "result": "PASS"
    },
    {
      "name": "Later prepaidtickstillresolves",
      "result": "PASS"
    },
    {
      "name": "Activation-funded Garden window permitsone targetstart",
      "result": "PASS"
    },
    {
      "name": "Samewindow replay blocked",
      "result": "PASS"
    },
    {
      "name": "Newwindow cannot bypass numberedround",
      "result": "PASS"
    },
    {
      "name": "Newround eligible Garden pulse",
      "result": "PASS"
    },
    {
      "name": "Garden pays perwindow notperrecipient",
      "result": "PASS"
    },
    {
      "name": "Garden expires beforeownerthirdfuturestart",
      "result": "PASS"
    },
    {
      "name": "Missedfunding ends atoriginalduemarker",
      "result": "PASS"
    },
    {
      "name": "Unpayableduewindowrejects",
      "result": "PASS"
    },
    {
      "name": "Unpayableduewindowends immediately",
      "result": "PASS"
    },
    {
      "name": "CrownselfBAcast can onlyreceive2 beforeexpiry",
      "result": "PASS"
    },
    {
      "name": "Crowncannotaddunselectedentrants",
      "result": "PASS"
    },
    {
      "name": "Extra targetturn creates no pulse",
      "result": "PASS"
    },
    {
      "name": "Suppressed occurrence cannotcatchup",
      "result": "PASS"
    },
    {
      "name": "Bloom remainder toearlierinstallments",
      "result": "PASS"
    },
    {
      "name": "Bloom first declaredreserve",
      "result": "PASS"
    },
    {
      "name": "Outside target loses middleinstallment",
      "result": "PASS"
    },
    {
      "name": "Reentry gets thirdonly, no accumulatedmissing",
      "result": "PASS"
    },
    {
      "name": "Bloom installment cannotreplay",
      "result": "PASS"
    },
    {
      "name": "Bloom cannotnewroster",
      "result": "PASS"
    },
    {
      "name": "Gardenentrycure independent ofHP",
      "result": "PASS"
    },
    {
      "name": "Gardenlaterpulse cannotdoublecure",
      "result": "PASS"
    },
    {
      "name": "Seedentry is notfirstpulse",
      "result": "PASS"
    },
    {
      "name": "Seedfirstpulse cure evenHPblocked",
      "result": "PASS"
    },
    {
      "name": "EnhancedGardenexplicitfirstpulsetiming",
      "result": "PASS"
    },
    {
      "name": "Nano noinitialheal",
      "result": "PASS"
    },
    {
      "name": "SkippingNano commanddoesnotend",
      "result": "PASS"
    },
    {
      "name": "Nano printedcap independent ofcallercommandceiling",
      "result": "PASS"
    },
    {
      "name": "Nano4thpulseprohibited",
      "result": "PASS"
    },
    {
      "name": "ExtraActionalone cannotpayrequiredBA",
      "result": "PASS"
    },
    {
      "name": "RejectedNano command noRPcharged",
      "result": "PASS"
    },
    {
      "name": "Overdrivecannotcreate4thhealingpulse",
      "result": "PASS"
    },
    {
      "name": "Nativefivepaidregularpulses",
      "result": "PASS"
    },
    {
      "name": "Nativereplaynofee",
      "result": "PASS"
    },
    {
      "name": "Nativeextraturnnofee",
      "result": "PASS"
    },
    {
      "name": "Unknownsourceprofile",
      "result": "PASS"
    },
    {
      "name": "Existingvirtualphase retainsnext6 notactivationplus6",
      "result": "PASS"
    },
    {
      "name": "Actual earlierexpiry notoverwrittenbylatermissedupkeep",
      "result": "PASS"
    },
    {
      "name": "UnpayableBApulse chargesnoaction",
      "result": "PASS"
    },
    {
      "name": "UnpayableBApulse remainsunspent untildeadline",
      "result": "PASS"
    },
    {
      "name": "Echoonly active anchor yieldssourcebase1",
      "result": "PASS"
    },
    {
      "name": "Overlap suppliesalternativebases neveradds",
      "result": "PASS"
    },
    {
      "name": "ParentplusEcho do notcreate6targetbudget",
      "result": "PASS"
    },
    {
      "name": "Rejectedexcessrecipientsdoesnotconsumepulse",
      "result": "PASS"
    },
    {
      "name": "Choruslaterownturnpulse1RC no inventedBA",
      "result": "PASS"
    },
    {
      "name": "song-of-mending unpaid exactdue rejects",
      "result": "PASS"
    },
    {
      "name": "song-of-mending unpaid exactdue ends immediately",
      "result": "PASS"
    },
    {
      "name": "song-of-mending cannotretry same marker afteracquiringRC",
      "result": "PASS"
    },
    {
      "name": "enhanced-song unpaid exactdue rejects",
      "result": "PASS"
    },
    {
      "name": "enhanced-song unpaid exactdue ends immediately",
      "result": "PASS"
    },
    {
      "name": "enhanced-song cannotretry same marker afteracquiringRC",
      "result": "PASS"
    },
    {
      "name": "wound-eater-iv unpaid exactdue rejects",
      "result": "PASS"
    },
    {
      "name": "wound-eater-iv unpaid exactdue ends immediately",
      "result": "PASS"
    },
    {
      "name": "wound-eater-iv cannotretry same marker afteracquiringRC",
      "result": "PASS"
    },
    {
      "name": "IllegalSongdueupkeep rejects",
      "result": "PASS"
    },
    {
      "name": "IllegalSongdueupkeep endsatmarker",
      "result": "PASS"
    },
    {
      "name": "IllegalGardenduefunding rejects",
      "result": "PASS"
    },
    {
      "name": "IllegalGardenduefunding endswithoutpayment",
      "result": "PASS"
    },
    {
      "name": "Extra-turnfundattempt rejects",
      "result": "PASS"
    },
    {
      "name": "Extraturndoesnotitselfterminatependingrealmarker",
      "result": "PASS"
    },
    {
      "name": "Actualregularfunding remainslegal afterextraattempt",
      "result": "PASS"
    },
    {
      "name": "SuppressedCircle consumesownpulse withoutnamedbenefit",
      "result": "PASS"
    },
    {
      "name": "OtheroperativeCircle canbenefit sametargetround",
      "result": "PASS"
    }
  ]
}


## data/playtest/healing_pulse_profiles.json

{
  "status": "EXACT_SOURCE_LINKS; scheduling overlay under review",
  "scope": "Internal helper profile labels map to existing supplied source IDs. These are not additional spells, abilities, feat choices or class cards.",
  "reviewEvidence": [
    "GPT_HEALING_PULSE_FIRST_REVIEW.md",
    "GPT_HEALING_PULSE_BOUNDARIES.md",
    "GPT_HEALING_PULSE_IMPLEMENTATION_FINDINGS.md"
  ],
  "profiles": {
    "sacred-chant": [
      "cleric.base.sacred-chant"
    ],
    "sacrament": [
      "cleric.arch.sacrament",
      "cleric.engine[5]"
    ],
    "dark-sacrament": [
      "cleric.hero.cultist.dark-sacrament",
      "cleric.engine[5]"
    ],
    "healing-briar": [
      "ranger.hero.warder.healing-briar"
    ],
    "circle-of-harmony": [
      "monk.hero.enlightened-master.circle-of-harmony"
    ],
    "renewal": [
      "shaman.engine[1]",
      "shaman.hero.theurgist.echo-totem"
    ],
    "renewal-extended": [
      "shaman.engine[1]",
      "shaman.arch.extended-totem-duration",
      "shaman.hero.theurgist.echo-totem"
    ],
    "restoration-field": [
      "tinker.hero.artificer.restoration-field"
    ],
    "desecrated-ground": [
      "paladin.supplement.oathbreaker-shared.desecrated-ground",
      "paladin.engine[11]"
    ],
    "lifewell": [
      "crimson-agent.hero.bloodweaver.lifewell"
    ],
    "unfinished-chorus": [
      "oracle.supplement.bones.unfinished-chorus",
      "oracle.engine[26]"
    ],
    "song-of-mending": [
      "oracle.supplement.life.song-of-mending",
      "oracle.engine[26]"
    ],
    "enhanced-song": [
      "oracle.supplement.life.song-of-mending",
      "oracle.supplement.life.life-revelation-mastery",
      "oracle.engine[26]"
    ],
    "transcendent-meditation": [
      "monk.hero.enlightened-master.transcendent-meditation"
    ],
    "eternal-bloom": [
      "oracle.supplement.life.eternal-bloom",
      "oracle.engine[26]"
    ],
    "wound-eater-iv": [
      "oracle.supplement.wound-eater.wound-eater-boon-iv",
      "oracle.engine[26]"
    ],
    "hemostasis": [
      "crimson-agent.hero.bloodweaver.hemostasis"
    ],
    "cellular-reconstruction": [
      "warrior.hero.ironskin.cellular-reconstruction"
    ],
    "cleric-echoes": [
      "cleric.base.echoes.echoes"
    ],
    "resonant-seed": [
      "oracle.supplement.life.resonant-seed",
      "oracle.engine[26]"
    ],
    "garden": [
      "oracle.supplement.life.garden-of-restoration",
      "oracle.engine[26]"
    ],
    "burning-blood-v": [
      "oracle.supplement.burning-blood.burning-blood-boon-v",
      "oracle.engine[26]",
      "oracle.engine[17]"
    ],
    "crown-restored": [
      "oracle.supplement.flame.crown-restored",
      "oracle.engine[26]"
    ],
    "nano-aegis": [
      "tinker.hero.artificer.nano-aegis-drone"
    ]
  },
  "nativeRecurrences": {
    "aura-of-grace": [
      "cleric.hero.saint.aura-of-grace"
    ],
    "living-pulse": [
      "ranger.hero.warder.living-pulse"
    ],
    "thief-exsanguinate": [
      "thief.hero.blackguard.exsanguinate"
    ],
    "regenerative-mutation": [
      "warrior.hero.ironskin.regenerative-mutation"
    ],
    "bloodthick-node": [
      "warrior.supplement.bloodthick-node"
    ],
    "rapid-coagulation": [
      "warrior.supplement.rapid-coagulation"
    ]
  },
  "contactVariants": {
    "garden": [
      "oracle.supplement.life.garden-of-restoration"
    ],
    "enhanced-garden": [
      "oracle.supplement.life.garden-of-restoration",
      "oracle.supplement.life.life-revelation-mastery"
    ],
    "resonant-seed": [
      "oracle.supplement.life.resonant-seed"
    ]
  }
}


## docs/mechanics/HEALING_PULSE_PROFILE_PROVENANCE.json

{
  "status": "PASS",
  "linkedProfiles": 33,
  "scope": "Every current scheduling/native/contact profile maps to exact supplied sources. This validates provenance, not balance or unsupplied card acquisition.",
  "checks": [
    {
      "category": "profiles",
      "profile": "sacred-chant",
      "sourceIds": [
        "cleric.base.sacred-chant"
      ],
      "result": "PASS"
    },
    {
      "category": "profiles",
      "profile": "sacrament",
      "sourceIds": [
        "cleric.arch.sacrament",
        "cleric.engine[5]"
      ],
      "result": "PASS"
    },
    {
      "category": "profiles",
      "profile": "dark-sacrament",
      "sourceIds": [
        "cleric.hero.cultist.dark-sacrament",
        "cleric.engine[5]"
      ],
      "result": "PASS"
    },
    {
      "category": "profiles",
      "profile": "healing-briar",
      "sourceIds": [
        "ranger.hero.warder.healing-briar"
      ],
      "result": "PASS"
    },
    {
      "category": "profiles",
      "profile": "circle-of-harmony",
      "sourceIds": [
        "monk.hero.enlightened-master.circle-of-harmony"
      ],
      "result": "PASS"
    },
    {
      "category": "profiles",
      "profile": "renewal",
      "sourceIds": [
        "shaman.engine[1]",
        "shaman.hero.theurgist.echo-totem"
      ],
      "result": "PASS"
    },
    {
      "category": "profiles",
      "profile": "renewal-extended",
      "sourceIds": [
        "shaman.engine[1]",
        "shaman.arch.extended-totem-duration",
        "shaman.hero.theurgist.echo-totem"
      ],
      "result": "PASS"
    },
    {
      "category": "profiles",
      "profile": "restoration-field",
      "sourceIds": [
        "tinker.hero.artificer.restoration-field"
      ],
      "result": "PASS"
    },
    {
      "category": "profiles",
      "profile": "desecrated-ground",
      "sourceIds": [
        "paladin.supplement.oathbreaker-shared.desecrated-ground",
        "paladin.engine[11]"
      ],
      "result": "PASS"
    },
    {
      "category": "profiles",
      "profile": "lifewell",
      "sourceIds": [
        "crimson-agent.hero.bloodweaver.lifewell"
      ],
      "result": "PASS"
    },
    {
      "category": "profiles",
      "profile": "unfinished-chorus",
      "sourceIds": [
        "oracle.supplement.bones.unfinished-chorus",
        "oracle.engine[26]"
      ],
      "result": "PASS"
    },
    {
      "category": "profiles",
      "profile": "song-of-mending",
      "sourceIds": [
        "oracle.supplement.life.song-of-mending",
        "oracle.engine[26]"
      ],
      "result": "PASS"
    },
    {
      "category": "profiles",
      "profile": "enhanced-song",
      "sourceIds": [
        "oracle.supplement.life.song-of-mending",
        "oracle.supplement.life.life-revelation-mastery",
        "oracle.engine[26]"
      ],
      "result": "PASS"
    },
    {
      "category": "profiles",
      "profile": "transcendent-meditation",
      "sourceIds": [
        "monk.hero.enlightened-master.transcendent-meditation"
      ],
      "result": "PASS"
    },
    {
      "category": "profiles",
      "profile": "eternal-bloom",
      "sourceIds": [
        "oracle.supplement.life.eternal-bloom",
        "oracle.engine[26]"
      ],
      "result": "PASS"
    },
    {
      "category": "profiles",
      "profile": "wound-eater-iv",
      "sourceIds": [
        "oracle.supplement.wound-eater.wound-eater-boon-iv",
        "oracle.engine[26]"
      ],
      "result": "PASS"
    },
    {
      "category": "profiles",
      "profile": "hemostasis",
      "sourceIds": [
        "crimson-agent.hero.bloodweaver.hemostasis"
      ],
      "result": "PASS"
    },
    {
      "category": "profiles",
      "profile": "cellular-reconstruction",
      "sourceIds": [
        "warrior.hero.ironskin.cellular-reconstruction"
      ],
      "result": "PASS"
    },
    {
      "category": "profiles",
      "profile": "cleric-echoes",
      "sourceIds": [
        "cleric.base.echoes.echoes"
      ],
      "result": "PASS"
    },
    {
      "category": "profiles",
      "profile": "resonant-seed",
      "sourceIds": [
        "oracle.supplement.life.resonant-seed",
        "oracle.engine[26]"
      ],
      "result": "PASS"
    },
    {
      "category": "profiles",
      "profile": "garden",
      "sourceIds": [
        "oracle.supplement.life.garden-of-restoration",
        "oracle.engine[26]"
      ],
      "result": "PASS"
    },
    {
      "category": "profiles",
      "profile": "burning-blood-v",
      "sourceIds": [
        "oracle.supplement.burning-blood.burning-blood-boon-v",
        "oracle.engine[26]",
        "oracle.engine[17]"
      ],
      "result": "PASS"
    },
    {
      "category": "profiles",
      "profile": "crown-restored",
      "sourceIds": [
        "oracle.supplement.flame.crown-restored",
        "oracle.engine[26]"
      ],
      "result": "PASS"
    },
    {
      "category": "profiles",
      "profile": "nano-aegis",
      "sourceIds": [
        "tinker.hero.artificer.nano-aegis-drone"
      ],
      "result": "PASS"
    },
    {
      "category": "nativeRecurrences",
      "profile": "aura-of-grace",
      "sourceIds": [
        "cleric.hero.saint.aura-of-grace"
      ],
      "result": "PASS"
    },
    {
      "category": "nativeRecurrences",
      "profile": "living-pulse",
      "sourceIds": [
        "ranger.hero.warder.living-pulse"
      ],
      "result": "PASS"
    },
    {
      "category": "nativeRecurrences",
      "profile": "thief-exsanguinate",
      "sourceIds": [
        "thief.hero.blackguard.exsanguinate"
      ],
      "result": "PASS"
    },
    {
      "category": "nativeRecurrences",
      "profile": "regenerative-mutation",
      "sourceIds": [
        "warrior.hero.ironskin.regenerative-mutation"
      ],
      "result": "PASS"
    },
    {
      "category": "nativeRecurrences",
      "profile": "bloodthick-node",
      "sourceIds": [
        "warrior.supplement.bloodthick-node"
      ],
      "result": "PASS"
    },
    {
      "category": "nativeRecurrences",
      "profile": "rapid-coagulation",
      "sourceIds": [
        "warrior.supplement.rapid-coagulation"
      ],
      "result": "PASS"
    },
    {
      "category": "contactVariants",
      "profile": "garden",
      "sourceIds": [
        "oracle.supplement.life.garden-of-restoration"
      ],
      "result": "PASS"
    },
    {
      "category": "contactVariants",
      "profile": "enhanced-garden",
      "sourceIds": [
        "oracle.supplement.life.garden-of-restoration",
        "oracle.supplement.life.life-revelation-mastery"
      ],
      "result": "PASS"
    },
    {
      "category": "contactVariants",
      "profile": "resonant-seed",
      "sourceIds": [
        "oracle.supplement.life.resonant-seed"
      ],
      "result": "PASS"
    }
  ]
}


## docs/mechanics/HEALING_PULSE_SOURCE_VALIDATION.json

{
  "status": "PASS",
  "exactRecords": 100,
  "scope": "100 exact class candidate passages, including guards and exclusions. Source integrity only, not complete game zone coverage.",
  "issues": []
}


## docs/mechanics/HEALING_PULSE_SUPPORT_VALIDATION.json

{
  "status": "PASS",
  "exactSupportingRecords": 6,
  "scope": "Exact supplemental source equality and hashes, including frozen full shared class guide hash.",
  "issues": []
}

