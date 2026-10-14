# Form and buffer implementation correction

Codex → Calibration Review. Your complete review found one blocker: Earth Warden's recharge only progressed on regular turn indices. I replaced that dependency with an explicit owner recharge clock spanning initiative and actual elapsed downtime. The full current helper and regression suite are attached below.

OwnerRechargeClock keeps one tick ordinal, current time, next due six-second owner marker and initiative/outside mode. Actual regular starts may consume due ticks; outside elapsed time consumes the same marker sequence. Leaving/entering initiative preserves its phase. A regular start at a boundary already consumed by downtime cannot tick twice. Extra turns, time reversal and an elapsed parallel clock inside initiative are rejected. Slam readiness is source-scoped tick ordinal+2. Shift/revert/reentry does not advance it. Actual short/long rests now accept their actual completion time and advance the outside clock, rather than merely clearing recharge on rest.

Regression evidence: use Slam, leave initiative, six seconds remains blocked; twelve seconds succeeds; actual short and long rest time makes it ready; same-time form reentry does not; extra turns do not; entering initiative at an already counted boundary does not double-tick; early reordered starts cannot manufacture time. Caller remains responsible for canonical regular marker timestamps, processing actual form/effect expiry and all existing calendar transitions. This is a bounded clock adapter, not a second combat scheduler.

I also found and corrected one identity collision risk: form IDs had been unique only within each DruidState. Two owners could therefore choose the same ID, which a shared CreatureWorld dependency cleanup would mistake for one parent. The shared BufferLedger now reserves every form instance ID globally, including forms with no entry shield. Collisions fail before paying or ending old forms. Ended IDs remain reserved. Tests cover two actual owners and unpaid rejection.

The suite now passes163 contract checks and1,053 arbitration/damage scenarios. All175+5 source integrity checks and Druid metadata still pass. The frozen shared class-rules hash remains adb2f4752b45dc70ce792a675bb30dda362aab5056588061bcde3ba31c4c8a81. No original card/book/spell has changed.

Please review these exact corrections and state whether any blocker remains to closing the previously described SELECTED form/buffer reference scope. Do not promote the nine named deferred components, item/anatomy or natural-weapon gaps, other feat clauses, the full runtime, human balance or the whole game. All remain explicit follow-up work. The next five-spell source conference is prepared but has not been submitted or adopted.

## tools/form_temphp_playtest_rules.py
SHA256 c38a5c347597e27d2fdf9f1d9f7ddf6df17f64aa7a0c99fa93f967f00cdae299
```python
"""Bounded form/buffer reference, implementation review PENDING.

Caller owns actual source access, costs, targets, range, rolls, condition and
calendar legality. Use ONE BufferLedger per world and one DruidState per owner.
No scalar temp-HP copies may independently create/spend shields. Explicit clock
markers and completed-rest epochs come from the canonical scheduler.
"""
from dataclasses import dataclass, field, replace
from copy import deepcopy
from pathlib import Path
import json
from control_playtest_rules import ClockMarker, clock_marker, require_deadline
from spell_playtest_rules import SpellRuleError, integer
from redirection_playtest_rules import identity
from device_lifecycle_playtest_rules import Wallet
from core_playtest_rules import damage_event


def require(value, message):
    if not value: raise SpellRuleError(message)


@dataclass
class BufferGrant:
    grant_id: str
    source_id: str
    owner: str
    target: str
    remaining: int
    expiry: ClockMarker | None = None
    # None means an explicitly fixed/source-dependent lifetime, not default LR.
    rest_epoch: int | None = None
    dependencies: tuple = ()
    riders: set = field(default_factory=set)
    state: str = 'pending'

    def __post_init__(self):
        for v in (self.grant_id,self.source_id,self.owner,self.target): identity(v)
        integer(self.remaining,'offered temporary HP',0)
        if self.expiry is not None: require_deadline(self.expiry)
        if self.rest_epoch is not None: integer(self.rest_epoch,'recipient LR epoch',0)
        require(self.expiry is not None or self.rest_epoch is not None or self.dependencies,
                'Declare explicit expiry/dependency or default recipient LR epoch')
        for dep in self.dependencies: identity(dep)
        require(self.riders <= {'bloodshield-reaction','overflowing-cleanse'},'Unknown linked rider')
        if 'bloodshield-reaction' in self.riders:
            require(self.source_id=='crimson-agent.arch.veinweave-bloodshield','Wrong Bloodshield source')
        if 'overflowing-cleanse' in self.riders:
            require(self.source_id=='oracle.supplement.life.overflowing-light' and self.expiry is not None,
                    'Overflowing Light requires its explicit two-round endpoint')


class BufferLedger:
    """Grant identities persist after ending; no hidden shield or replay refill.

    expire() must run at actual scheduler deadlines. Side effects are returned
    as instructions; this helper never decides eligible conditions or cleanses
    automatically. A projection into Core is checked and reconciled atomically.
    """
    def __init__(self):
        self.grants={}; self.active={}; self.rest_epochs={}; self.damage_events=set()
        self.absorptions={}
        self.form_instances=set()

    def amount(self,target):
        ident=self.active.get(target)
        return self.grants[ident].remaining if ident else 0

    def current(self,target):
        ident=self.active.get(target)
        return self.grants.get(ident)

    def validate_offer(self,grant,now):
        require(isinstance(grant,BufferGrant) and grant.state=='pending','Supply a new uncommitted grant')
        require(grant.grant_id not in self.grants,'Grant identity already processed')
        marker=clock_marker(now)
        if grant.expiry is not None: require(marker<grant.expiry,'Grant deadline already passed')
        if grant.rest_epoch is not None:
            require(grant.rest_epoch==self.rest_epochs.get(grant.target,0),'Stale recipient rest epoch')
        current=self.current(grant.target)
        if current and current.expiry is not None:
            require(marker<current.expiry,'Resolve existing scheduled expiry before offering a new grant')

    def offer(self,grant,now=0):
        """Caller pays the legal source BEFORE this nonstack comparison.

        No current reviewed source overrides equal-retains-existing. Noble's
        paired Smite components are merged BEFORE calling this method once.
        """
        self.validate_offer(grant,now)
        g=deepcopy(grant)
        if not g.remaining:
            return {'accepted':False,'amount':0,'grantId':None}
        self.grants[g.grant_id]=g
        current=self.current(g.target)
        if current and current.remaining>=g.remaining:
            g.state='rejected'; return {'accepted':False,'amount':g.remaining,'grantId':None}
        if current: self.end(g.target,'replaced')
        g.state='active'; self.active[g.target]=g.grant_id
        return {'accepted':True,'amount':g.remaining,'grantId':g.grant_id}

    def end(self,target,reason,*,now=None):
        require(reason in ('replaced','depleted','natural-expiry','long-rest','dependency-ended','body-ended'),
                'Unknown buffer ending')
        g=self.current(target)
        if g is None:return []
        if reason=='natural-expiry':
            require(now is not None and g.expiry is not None and clock_marker(now)>=g.expiry,
                    'Natural expiry requires the actual fixed deadline')
        events=[]
        if reason=='natural-expiry' and g.remaining>0 and 'overflowing-cleanse' in g.riders:
            events.append({'sourceId':g.source_id,'grantId':g.grant_id,'target':target,
                           'chooseUpTo':1,'eligibleConditions':('Frightened','Poisoned','Staggered')})
        g.state=reason; g.remaining=0; g.riders.clear(); del self.active[target]
        return events

    def expire(self,now):
        marker=clock_marker(now); events=[]
        for target in list(self.active):
            g=self.current(target)
            if g.expiry is not None and marker>=g.expiry: events+=self.end(target,'natural-expiry',now=marker)
        return events

    def end_dependency(self,dependency):
        identity(dependency)
        for target in list(self.active):
            if dependency in self.current(target).dependencies:self.end(target,'dependency-ended')

    def completed_long_rest(self,target,epoch):
        integer(epoch,'new recipient LR epoch',1)
        require(epoch==self.rest_epochs.get(target,0)+1,'Process each actual completed LR exactly once')
        g=self.current(target)
        if g and g.rest_epoch is not None:self.end(target,'long-rest')
        self.rest_epochs[target]=epoch

    def consume_linked_reaction(self,target,grant_id,wallet,*,legal):
        g=self.current(target)
        require(legal and g is not None and g.grant_id==grant_id and 'bloodshield-reaction' in g.riders,
                'No current legal Bloodshield permission')
        wallet.validate(action='reaction'); wallet.pay(action='reaction')
        g.riders.remove('bloodshield-reaction')
        return {'sourceId':g.source_id,'grantId':g.grant_id,'reactionSpent':True}

    def core_damage(self,target,event_id,state,resolved_damage,*,now=0,**core_options):
        """Already defended packet, exactly one Core HP/Wound/death resolution.

        Returned life state is authoritative. Source-specific same-packet
        replacements remain the caller's existing Core/death adapter obligation;
        finalize Druid reversion only AFTER those settle the actual state.
        """
        identity(event_id); key=(target,event_id)
        require(key not in self.damage_events,'Damage event already resolved for this character')
        require(state.temp_hp==self.amount(target),'Core temporary-HP projection differs from grant ledger')
        current=self.current(target)
        require(current is None or current.expiry is None or clock_marker(now)<current.expiry,
                'Resolve scheduled shield expiry before damage')
        result,events=damage_event(state,resolved_damage,**core_options)
        self.damage_events.add(key)
        g=self.current(target)
        if g:
            g.remaining=result.temp_hp
            if not g.remaining:self.end(target,'depleted')
        return result,events

    def necrotic_affinity(self,target,event_id,post_defense_damage,wallet,expiry,*,legal):
        """Reaction at post-defense/after-resistance stage, BEFORE old buffer.

        Caller verifies spell/supernatural necrotic origin and actual access.
        Use returned remainingDamage in the canonical packet, then finish below.
        """
        identity(target); identity(event_id); require_deadline(expiry)
        integer(post_defense_damage,'post-defense necrotic damage',1)
        key=(target,event_id)
        require(legal and key not in self.absorptions and key not in self.damage_events,
                'Legal pending unique necrotic event required')
        wallet.validate(action='reaction'); wallet.pay(action='reaction')
        absorbed=post_defense_damage//2
        self.absorptions[key]={'amount':absorbed,'expiry':expiry,'finished':False}
        return {'prevented':absorbed,'remainingDamage':post_defense_damage-absorbed,
                'isHealing':False,'isTransfer':False}

    def finish_necrotic_affinity(self,target,event_id,grant_id,now,*,living_holder):
        key=(target,event_id); pending=self.absorptions.get(key)
        require(pending is not None and not pending['finished'] and key in self.damage_events,
                'Finish once after canonical damage has actually resolved')
        grant=None
        if pending['amount'] and living_holder:
            grant=BufferGrant(grant_id,'feat:necrotic_affinity',target,target,pending['amount'],expiry=pending['expiry'])
            self.validate_offer(grant,now)
        pending['finished']=True
        return self.offer(grant,now) if grant else None


def blood_ritual_offers(level):
    integer(level,'character level',1,20)
    return {'self':2*level,'eachEligibleAlly':level,'allyLifetimeSeconds':3600}


def post_event_buffer_amount(source_id,actual_amount,*,eligible,scale=None,modifier=None):
    """Only these already-resolved causal amounts; never rolled/raw damage.

    Necrotic Affinity uses its separate staged adapter above.
    """
    integer(actual_amount,'actual causal amount',0)
    require(eligible,'Actual source trigger/anti-farm/target legality required')
    if source_id in ('paladin.supplement.oath-of-the-martyr-king.king-s-smite',
                     'paladin.supplement.oath-of-the-martyr-king.noble-bearing'):
        integer(scale,'S',1,4);integer(modifier,'M',1)
        return min(actual_amount//2,scale+modifier)
    if source_id=='v6-trait:soul-drain':return actual_amount
    raise SpellRuleError('Use the source-specific established amount adapter')


def one_character_area_targets(position_hits):
    """Input is already-filtered legal positions for ONE area/event.

    Each pair is (canonical character identity, representation identity).
    Independent attack/event calls are deliberately not coalesced together.
    """
    result=[]
    for character,position in position_hits:
        identity(character); identity(position)
        if character not in result:result.append(character)
    return result


def spirit_walk_position_eligible(*,is_spirit,is_attack,physical_target_required,native_eligible):
    return bool(native_eligible and (not is_spirit or (not is_attack and not physical_target_required)))


@dataclass(frozen=True)
class DruidStats:
    owner: str
    level: int
    pb: int
    wisdom: int
    scale: int
    modifier: int

    def __post_init__(self):
        identity(self.owner);integer(self.level,'Druid level',1,20);integer(self.pb,'PB',1)
        integer(self.scale,'S',1,4);integer(self.modifier,'M',1)
        require(isinstance(self.wisdom,int) and not isinstance(self.wisdom,bool),'Actual signed WIS required')


@dataclass
class FormInstance:
    instance_id: str
    source_id: str
    variant: str | None
    expiry: ClockMarker
    large: bool=False
    spent: set=field(default_factory=set)
    state: str='active'
    entry_open: bool=False


PROFILES=json.loads((Path(__file__).resolve().parents[1]/'data/playtest/druid_form_profiles.json').read_text(encoding='utf-8'))['profiles']
ARCH_IDS=frozenset(k for k,v in PROFILES.items() if v['archAttunement'])
CIRCLES=frozenset(('Land','Moon','Storm','Thorns','Winterfang','Rotshaper','Ashen Grove'))


def shift_capacity(level):
    integer(level,'Druid level',1,20)
    return 2+sum(level>=gate for gate in (4,7,10,13,16,19))


class OwnerRechargeClock:
    """One owner timeline, shared by regular starts and downtime.

    The canonical six-second owner-marker phase survives initiative transitions.
    Reordering/extra turns cannot create earlier ticks. The scheduler must supply
    every actual regular start while in initiative. Outside, elapsed intervals
    consume the same next-due marker, never an additional parallel clock.
    """
    def __init__(self):
        self.mode='initiative';self.now=ClockMarker(0);self.next_tick=6
        self.ticks=0;self.last_regular=0

    def _time(self,now):
        marker=clock_marker(now);require(marker>=self.now,'Recharge time cannot move backward')
        return marker

    def regular_start(self,index,now,*,actual_regular_marker):
        marker=self._time(now);integer(index,'actual regular marker',1)
        require(self.mode=='initiative' and actual_regular_marker and index>self.last_regular,
                'New actual regular initiative marker required')
        self.last_regular=index;self.now=marker
        if marker.seconds>=self.next_tick:
            self.ticks+=1;self.next_tick=marker.seconds+6

    def leave_initiative(self,now):
        marker=self._time(now);require(self.mode=='initiative','Already outside initiative')
        self.now=marker;self.mode='outside'

    def advance_outside(self,now):
        marker=self._time(now);require(self.mode=='outside','Elapsed ticks only outside initiative')
        if marker.seconds>=self.next_tick:
            count=int((marker.seconds-self.next_tick)//6)+1
            self.ticks+=count;self.next_tick+=6*count
        self.now=marker

    def enter_initiative(self,now):
        self.advance_outside(now);self.mode='initiative'

    def use(self,now):
        marker=self._time(now)
        if self.mode=='outside':self.advance_outside(marker)
        else:self.now=marker
        # The cast/action does not tick or reset an existing owner's phase.
        return self.ticks


class DruidState:
    """Same-body forms and shared finite reserves; no HP or condition copy.

    The owner-wide class cadence dictionary is mutated only for real entries.
    creatures, when supplied, is the SAME CreatureWorld used by companion rules.
    Caller ends other exact form-dependent effect records from returned IDs.
    A canonical calendar owns regular marker indices and actual rest completion.
    """
    def __init__(self,stats,circle,buffers,cadence,*,attuned=(),creatures=None):
        require(circle in CIRCLES or (circle is None and stats.level==1),'Choose legal Druid Circle')
        require(isinstance(buffers,BufferLedger),'Canonical buffer ledger required')
        require(set(cadence)>= {'refrain','rememberedSpell','dissonance'},'Canonical class cadence required')
        self.owner=stats.owner;self.circle=circle;self.buffers=buffers;self.cadence=cadence
        self.creatures=creatures;self.current=None;self.instances={}
        self.long_epoch=0;self.short_epoch=0;self.regular_index=0;self.recharges={}
        self.recharge_clock=OwnerRechargeClock()
        self.rest_uses={};self.attuned=()
        self._validate_attunement(stats,attuned)
        self._refill(stats,attuned)

    def _stats(self,stats):
        require(isinstance(stats,DruidStats) and stats.owner==self.owner,'Use current original-owner Druid stats')

    def _validate_attunement(self,stats,attuned):
        require(len(attuned)==len(set(attuned)) and len(attuned)<=2 and set(attuned)<=ARCH_IDS,
                'Choose at most two distinct supplied Arch forms')
        require(stats.level>=11 or not attuned,'Arch attunement starts at11')

    def _refill(self,stats,attuned):
        self.shifts=shift_capacity(stats.level);self.buffer_capacity=2*stats.level+stats.modifier
        self.reserve=self.buffer_capacity;self.surges=stats.pb;self.surge_capacity=stats.pb
        self.attuned=tuple(attuned);self.rest_uses={}

    def completed_long_rest(self,stats,epoch,*,attuned,actual_completed,now):
        self._stats(stats);self._validate_attunement(stats,attuned)
        require(actual_completed and epoch==self.long_epoch+1,'Actual next completed owner LR required')
        self.recharge_clock.advance_outside(now)
        self.long_epoch=epoch;self.short_epoch+=1;self._refill(stats,attuned)
        # Receiving default buffers is a separate recipient-calendar operation.
        # Form instances/local flags and independent clocks are NOT refreshed.

    def completed_short_rest(self,epoch,*,actual_completed,now):
        require(actual_completed and epoch==self.short_epoch+1,'Actual next completed SR required')
        self.recharge_clock.advance_outside(now)
        self.short_epoch=epoch
        self.rest_uses={k:v for k,v in self.rest_uses.items() if not k.startswith('short:')}

    def regular_start(self,index,now,*,actual_regular_marker):
        integer(index,'canonical regular marker',1)
        require(actual_regular_marker and index>self.regular_index,'No extra-turn/repeated recharge tick')
        self.recharge_clock.regular_start(index,now,actual_regular_marker=actual_regular_marker)
        self.regular_index=index

    def _active(self,now):
        require(self.current is not None and self.current.state=='active' and clock_marker(now)<self.current.expiry,
                'Resolve form endpoint before acting')
        return self.current

    def _legal_profile(self,stats,source_id,variant,large):
        self._stats(stats);require(source_id in PROFILES,'Only supplied bounded Druid forms')
        p=PROFILES[source_id]
        require(stats.level>=p['minimumLevel'],'Form level gate not met')
        require(p['circle'] is None or p['circle']==self.circle,'Wrong Circle')
        require(not p['archAttunement'] or source_id in self.attuned,'Form is not long-rest attuned')
        require(not large or p['mayLarge'],'This form does not permit Large size')
        if source_id.endswith('elemental-shapeshifting'):
            require(variant in ('air','earth','fire','water'),'Choose actual Elemental subtype')
        elif source_id.endswith('master-of-vermin'):
            require(variant in ('ground','bats'),'Choose actual Vermin subtype')
        else:require(variant is None,'This form has no independently changeable subtype')
        return p

    def shift(self,stats,source_id,instance_id,now,wallet,*,legal,variant=None,large=False,
              spawn=False,spawn_legal=False):
        p=self._legal_profile(stats,source_id,variant,large);marker=clock_marker(now)
        identity(instance_id)
        require(instance_id not in self.buffers.form_instances,'Form instance identity already used anywhere in this world')
        require(legal,'Actual movement/space/capability/source preflight failed')
        if self.current:
            old=self._active(marker)
            require((old.source_id,old.variant)!=(source_id,variant),'Early identical-form requests are unpaid and rejected')
        require(stats.level==20 or self.shifts>0,'No shift use')
        elemental=source_id.endswith('elemental-shapeshifting')
        require(not elemental or self.rest_uses.get('long:elemental',0)<2,'Elemental uses exhausted')
        wallet.validate(action='bonus')
        amount=min(p['entryBuffer'],self.reserve)
        grant=BufferGrant(instance_id+':entry',source_id,self.owner,self.owner,amount,dependencies=(instance_id,)) if amount else None
        if grant:self.buffers.validate_offer(grant,marker)
        wallet.pay(action='bonus')
        if stats.level<20:self.shifts-=1
        if elemental:self.rest_uses['long:elemental']=self.rest_uses.get('long:elemental',0)+1
        old_id=self._end('changed')
        form=FormInstance(instance_id,source_id,variant,ClockMarker(marker.seconds+600,marker.phase),large)
        self.current=form;self.instances[instance_id]=form
        self.buffers.form_instances.add(instance_id)
        self.cadence['refrain']=0;self.cadence['rememberedSpell']=None
        self.reserve-=amount
        offered=self.buffers.offer(grant,marker) if grant else None
        spawn_payment=None
        if source_id.endswith('insect-broodmother'):
            form.entry_open=True
            if spawn and spawn_legal and self.surges>0:
                spawn_payment=self.special(stats,now,wallet,'spawn',legal=True)
            form.entry_open=False
        return {'formInstance':instance_id,'endedDependency':old_id,'entryBuffer':offered,
                'spawnPayment':spawn_payment,'optionalSpawnWindowClosed':True}

    def _end(self,reason):
        if self.current is None:return None
        f=self.current;f.state=reason;self.current=None
        self.buffers.end_dependency(f.instance_id)
        if self.creatures is not None:self.creatures.end_dependency(form=f.instance_id)
        return f.instance_id

    def revert(self,now,wallet,*,legal):
        self._active(now);require(legal,'Actual voluntary reversion must be legal')
        wallet.validate(action='bonus');wallet.pay(action='bonus')
        return self._end('voluntary-reversion')

    def natural_endpoint(self,stats,now,*,renew):
        self._stats(stats);marker=clock_marker(now);f=self.current
        require(f is not None and f.state=='active' and marker==f.expiry,'Process actual form endpoint exactly')
        if not renew:return {'endedDependency':self._end('expired')}
        require(stats.level==20 or self.shifts>0,'No shift use for renewal')
        if stats.level<20:self.shifts-=1
        f.expiry=ClockMarker(f.expiry.seconds+600,f.expiry.phase)
        return {'renewedSameInstance':f.instance_id,'expiry':f.expiry}

    def finalize_damage_state(self,*,actual_hp,incapacitated,dead,unsupported):
        integer(actual_hp,'actual final HP',0)
        if self.current is None:return None
        if actual_hp==0 or incapacitated or dead:
            ident=self._end('forced-reversion')
            return {'endedDependency':ident,'beginOrdinaryFall':bool(unsupported),'secondDamageResolution':False}
        return None

    def profile(self,stats,now,form_normal_ac,*,ac_components_certified):
        self._stats(stats);f=self._active(now);integer(form_normal_ac,'operative form normal AC',0)
        require(ac_components_certified,'Exclude melded armor/shield/unclassified item bonuses first')
        p=deepcopy(PROFILES[f.source_id]);mode=p['ac']['mode'];n=p['ac']['amount']
        p['ac']=max(form_normal_ac,n) if mode=='floor' else form_normal_ac+n if mode=='add' else n if mode=='fixed' else form_normal_ac
        p['size']='Large' if f.large else p['size'];p['formInstance']=f.instance_id
        p['attack']['attack']=stats.pb+stats.wisdom;p['saveDC']=8+stats.pb+stats.wisdom
        p['attack']['magicalAgainstPhysicalDefenses']=p['attack']['intrinsicallyMagical'] or (self.circle=='Moon' and stats.level>=6)
        if f.variant in ('air','earth','fire','water'):
            p['attack']['damageType']={'air':'lightning','earth':'bludgeoning','fire':'fire','water':'cold'}[f.variant]
            p['elementalSubtype']=f.variant
            p['movement'].update({'air':{'fly':60},'earth':{'burrowLooseSoil':20},'fire':{},'water':{'swim':60}}[f.variant])
        if f.variant in ('ground','bats'):
            p['physicalResistance']=f.variant=='ground'
            if f.variant=='bats':p['movement']['fly']=30
        p['mayCastDruidSpells']=stats.level>=18
        p['materialComponents']='At20 waive noncostly unconsumed only; otherwise no access to melded materials'
        return p

    def attack(self,stats,now,wallet,*,legal):
        self._stats(stats);f=self._active(now);require(legal,'Actual natural attack target/capability required')
        wallet.validate(action='action');wallet.pay(action='action')
        attack=deepcopy(PROFILES[f.source_id]['attack'])
        if f.variant in ('air','earth','fire','water'):
            attack['damageType']={'air':'lightning','earth':'bludgeoning','fire':'fire','water':'cold'}[f.variant]
        return {'sourceId':f.source_id,'formInstance':f.instance_id,
                'profile':attack,'attack':stats.pb+stats.wisdom,
                'WIS':stats.wisdom,'S':stats.scale,'saveDC':8+stats.pb+stats.wisdom,
                'magicalAgainstPhysicalDefenses':attack['intrinsicallyMagical'] or (self.circle=='Moon' and stats.level>=6),
                'circleFormsFirstHitBonus':stats.scale if self.circle=='Moon' and stats.level>=2 else 0,
                'circleFormsFrequency':'First actual natural-form hit on own turn only; canonical hit ledger required',
                'exactRiders':PROFILES[f.source_id]['sourceProcedure']['effect'],
                'unrelatedWeaponProcAuthorized':False}

    def special(self,stats,now,wallet,special_id,*,legal):
        self._stats(stats);f=self._active(now);p=PROFILES[f.source_id]
        require(special_id in p['specials'] and legal,'Actual printed special and all gates required')
        q=p['specials'][special_id]
        # Canonical clock progress is independent of whether this ability is used.
        ticks=self.recharge_clock.use(now)
        if special_id=='spawn':require(f.entry_open,'Brood spawn requires the actual entry window')
        if q['payment']=='surge':
            require(special_id not in f.spent and self.surges>0,'Local special or global Form Surge exhausted')
        elif q['payment']=='recharge2':
            require(ticks>=self.recharges.get(f.source_id,0),'Slam source recharge still active across shifts')
        else:
            kind='short:' if q['payment']=='short-rest' else 'long:'
            require(self.rest_uses.get(kind+f.source_id,0)==0,'Shared per-rest special already spent')
        wallet.validate(action=q['action']);wallet.pay(action=q['action'])
        if q['payment']=='surge':f.spent.add(special_id);self.surges-=1
        elif q['payment']=='recharge2':self.recharges[f.source_id]=ticks+2
        else:self.rest_uses[kind+f.source_id]=1
        return {'sourceId':f.source_id,'formInstance':f.instance_id,'specialId':special_id,
                'sourceProcedure':deepcopy(p['sourceProcedure']),'refundOnFailure':False,
                'createsExtraAttack':False,'formSurgePaid':q['payment']=='surge'}

    def mooncursed_howl(self,stats,now,wallet,recipients,shared_roll,grant_ids,*,legal):
        f=self._active(now)
        require(f.source_id=='druid.hero.moon.mooncursed','Requires actual Mooncursed form')
        require(1<=len(recipients)<=3 and len(recipients)==len(set(recipients))==len(grant_ids),
                'Select and order one to three distinct legal allies before rolling')
        require(len(set(grant_ids))==len(grant_ids),'Distinct offered grant IDs')
        integer(shared_roll,'shared 2d8',2,16)
        grants=[];reserve=self.reserve
        for target,ident in zip(recipients,grant_ids):
            identity(target);identity(ident);amount=min(shared_roll,reserve);reserve-=amount
            g=BufferGrant(ident,f.source_id,self.owner,target,amount,
                          rest_epoch=self.buffers.rest_epochs.get(target,0)) if amount else None
            if g:self.buffers.validate_offer(g,now)
            grants.append(g)
        self.special(stats,now,wallet,'howl',legal=legal)
        self.reserve=reserve
        return [self.buffers.offer(g,now) if g else None for g in grants]

```

## tools/validate_form_temphp_playtests.py
SHA256 6f2fe213e57176443450ec4dbdc9f3296ad3d47452f019790e0a8d609c874904
```python
"""Adversarial contract checks, not full card/rider or human balance tests."""
from pathlib import Path
import json
from copy import deepcopy
from dataclasses import replace
from form_temphp_playtest_rules import *
from core_playtest_rules import LifeState
from creature_lifecycle_playtest_rules import CreatureWorld, Creature

checks=0
def check(value,label):
    global checks
    assert value,label
    checks+=1
def rejects(fn,label):
    try:fn()
    except SpellRuleError:check(True,label)
    else:raise AssertionError(label)

def grant(ident,amount,*,source='test',target='d',expiry=None,rest=0,deps=(),riders=()):
    return BufferGrant(ident,source,'d',target,amount,expiry,rest,deps,set(riders))

def state(level=20,circle='Moon',*,attuned=(),creatures=None):
    stats=DruidStats('d',level,6,4,4,4)
    ledger=BufferLedger(); cadence={'refrain':3,'rememberedSpell':'test-spell','dissonance':9}
    return stats,DruidState(stats,circle,ledger,cadence,attuned=attuned,creatures=creatures)

def main():
    global checks
    b=BufferLedger()
    b.offer(grant('old',8,expiry=ClockMarker(30),rest=None))
    b.offer(grant('small',7,expiry=ClockMarker(100),rest=None))
    check(b.current('d').grant_id=='old','Smaller grant cannot refresh')
    b.offer(grant('tie',8,expiry=ClockMarker(100),rest=None))
    check(b.current('d').expiry==ClockMarker(30),'Tie retains original deadline')
    rejects(lambda:b.offer(grant('tie',50)),'Rejected ID cannot later refill')
    b.offer(grant('bigger',9))
    check(b.grants['old'].state=='replaced' and b.amount('d')==9,'Only one active grant')
    b.end('d','depleted');check(b.amount('d')==0,'Old grant never reappears')
    b.offer(grant('zero',0));check('zero' not in b.grants,'Zero creates no grant identity')
    b.offer(grant('default',4));b.completed_long_rest('d',1)
    check(b.amount('d')==0,'Default ends at actual recipient LR')
    rejects(lambda:b.completed_long_rest('d',1),'No repeated rest reset')
    rejects(lambda:b.offer(grant('stale',5,rest=0)),'Stale recipient epoch rejected')
    b.offer(grant('fixed',5,expiry=ClockMarker(100),rest=None),50)
    b.completed_long_rest('d',2);check(b.amount('d')==5,'Explicit lifetime may outlast LR')
    b.expire(100);check(b.amount('d')==0,'Exact fixed endpoint')

    blood='crimson-agent.arch.veinweave-bloodshield'
    b=BufferLedger();b.offer(grant('unrelated',10))
    b.offer(grant('rejected-blood',10,source=blood,riders=('bloodshield-reaction',)))
    w=Wallet();rejects(lambda:b.consume_linked_reaction('d','rejected-blood',w,legal=True),'Rejected shield has no permission')
    check(w.reaction,'Invalid permission does not pay Reaction')
    b.offer(grant('blood',12,source=blood,riders=('bloodshield-reaction',)))
    b.consume_linked_reaction('d','blood',w,legal=True)
    check(not w.reaction and not b.current('d').riders,'One current linked Reaction')
    rejects(lambda:b.consume_linked_reaction('d','blood',Wallet(),legal=True),'No repeated linked use')
    b.offer(grant('blood2',13,source=blood,riders=('bloodshield-reaction',)))
    b.offer(grant('other',14));rejects(lambda:b.consume_linked_reaction('d','blood2',Wallet(),legal=True),'Replacement removes linked use')

    overflow='oracle.supplement.life.overflowing-light'
    for reason in ('replaced','depleted','dependency-ended','body-ended','long-rest'):
        b=BufferLedger();b.offer(grant('ol',3,source=overflow,expiry=ClockMarker(12),rest=None,riders=('overflowing-cleanse',)))
        check(not b.end('d',reason),'No false natural-expiry cleanse: '+reason)
        check(not b.expire(12),'No delayed cleanse after '+reason)
    b=BufferLedger();b.offer(grant('ol',3,source=overflow,expiry=ClockMarker(12),rest=None,riders=('overflowing-cleanse',)))
    rejects(lambda:b.end('d','natural-expiry',now=11),'Cannot fabricate early natural expiry')
    rejects(lambda:b.core_damage('d','late',LifeState(20,20,3),1,now=12),'Expired buffer cannot protect late event')
    check(not b.expire(11),'No early cleanse');events=b.expire(12)
    check(len(events)==1 and events[0]['chooseUpTo']==1,'One optional actual eligible cleanse')
    check(not b.expire(13),'No repeat cleanse')

    b=BufferLedger();b.offer(grant('program',10,source='tinker.hero.artificer.protective-programming',rest=None,deps=('hit1',)))
    life,events=b.core_damage('d','hit1',LifeState(20,20,10),3)
    check(life.hp==20 and life.temp_hp==7 and events['tempAbsorbed']==3,'Shield before one hit')
    b.end_dependency('hit1');check(b.amount('d')==0,'Programming remainder ends after that hit')
    b=BufferLedger();b.offer(grant('larger',20));b.offer(grant('program',10,rest=None,deps=('hit1',)))
    b.end_dependency('hit1');check(b.amount('d')==20,'Rejected one-hit shield cannot end winner')

    b=BufferLedger();b.offer(grant('shield',6))
    original=LifeState(30,8,6,wounds=(None,),stable=False,death_successes=0)
    out,e=b.core_damage('d','damage',original,4)
    check(out.hp==8 and out.wounds==(None,) and b.amount('d')==2,'THP mitigates without healing/Wound removal')
    check(original.temp_hp==6,'Core input immutable')
    rejects(lambda:b.core_damage('d','damage',out,4),'No duplicate canonical damage')
    rejects(lambda:b.core_damage('d','other',replace(out,temp_hp=100),4),'Divergent scalar HP projection rejected')
    b=BufferLedger();b.offer(grant('dying',10))
    out,e=b.core_damage('d','dmg',LifeState(20,0,10,death_failures=1),5)
    check(out.hp==0 and not out.stable and out.death_failures==1,'Buffer cannot stabilize/reset dying')

    b=BufferLedger();b.offer(grant('old',3));w=Wallet()
    q=b.necrotic_affinity('d','necro',9,w,ClockMarker(12),legal=True)
    check(q['prevented']==4 and q['remainingDamage']==5 and not w.reaction,'After-resistance half prevention')
    out,e=b.core_damage('d','necro',LifeState(20,20,3),q['remainingDamage'])
    check(out.hp==18 and e['tempAbsorbed']==3,'Old shield protects remainder only')
    b.finish_necrotic_affinity('d','necro','new',0,living_holder=True)
    check(b.amount('d')==4 and out.hp==18,'New shield only after damage')
    rejects(lambda:b.necrotic_affinity('d','necro',9,Wallet(),ClockMarker(12),legal=True),'No repeat absorption')
    rejects(lambda:b.finish_necrotic_affinity('d','necro','new2',0,living_holder=True),'No repeat post-packet grant')
    b=BufferLedger();b.necrotic_affinity('d','one',1,Wallet(),ClockMarker(12),legal=True)
    b.core_damage('d','one',LifeState(20,20),1)
    check(b.finish_necrotic_affinity('d','one','no-grant',0,living_holder=True) is None and not b.grants,'One damage can pay without zero grant')
    b=BufferLedger();q=b.necrotic_affinity('d','fatal',100,Wallet(),ClockMarker(12),legal=True)
    out,e=b.core_damage('d','fatal',LifeState(20,1),q['remainingDamage'])
    check(out.dead,'Test actual instant death')
    b.finish_necrotic_affinity('d','fatal','corpse',0,living_holder=False)
    check(not b.grants,'No post-event corpse shield')

    check(blood_ritual_offers(7)=={'self':14,'eachEligibleAlly':7,'allyLifetimeSeconds':3600},'Blood Ritual uses own offer not winner')
    check(post_event_buffer_amount('paladin.supplement.oath-of-the-martyr-king.king-s-smite',99,eligible=True,scale=2,modifier=3)==5,'Smite actual half and cap')
    rejects(lambda:post_event_buffer_amount('v6-trait:soul-drain',8,eligible=False),'Actual ancestry anti-farm gate')
    check(one_character_area_targets([('d','body'),('d','spirit'),('ally','body2')])==['d','ally'],'One area deduplicates same body identity')
    check(not spirit_walk_position_eligible(is_spirit=True,is_attack=True,physical_target_required=False,native_eligible=True),'Spirit never attack target')
    check(not spirit_walk_position_eligible(is_spirit=True,is_attack=False,physical_target_required=True,native_eligible=True),'Physical-required effect excluded')
    check(spirit_walk_position_eligible(is_spirit=True,is_attack=False,physical_target_required=False,native_eligible=True),'Legal nonphysical area exposure')

    bear='druid.base.bear-form-tank';wolf='druid.base.wolf-form-striker';hawk='druid.base.hawk-form-scout'
    stats,d=state(10);d.buffers.offer(grant('large-shield',50));w=Wallet()
    entered=d.shift(stats,bear,'bear1',0,w,legal=True)
    check(d.shifts==4 and d.reserve==4 and not w.bonus_action,'Entry pays full20 reserve and shift/BA')
    check(d.buffers.current('d').grant_id=='large-shield','Failed comparison still consumes reserve')
    check(d.cadence=={'refrain':0,'rememberedSpell':None,'dissonance':9},'Only Refrain clears')
    before=(d.reserve,d.shifts);w=Wallet()
    rejects(lambda:d.shift(stats,bear,'repeat',1,w,legal=True),'Early identical form rejected')
    check(before==(d.reserve,d.shifts) and w.bonus_action,'Illegal identical shift costs nothing')
    d.cadence['refrain']=2;d.cadence['rememberedSpell']='again'
    d.natural_endpoint(stats,600,renew=True)
    check(d.current.instance_id=='bear1' and d.reserve==4 and d.shifts==3,'Renew same instance without refill')
    check(d.cadence['refrain']==2 and d.current.expiry==ClockMarker(1200),'Renew does not clear Refrain')
    rejects(lambda:d.natural_endpoint(stats,700,renew=True),'No early renew')
    d.revert(601,Wallet(),legal=True)
    check(d.cadence['refrain']==2 and d.shifts==3 and d.buffers.amount('d')==50,'Revert preserves unrelated shield and cadence')
    d.shift(stats,bear,'bear2',602,Wallet(),legal=True)
    check(d.reserve==0,'New entry only remaining reserve offered')
    d.revert(603,Wallet(),legal=True);d.shift(stats,bear,'bear3',604,Wallet(),legal=True)
    check(d.reserve==0 and 'bear3:entry' not in d.buffers.grants,'Zero-reserve form still legal, no grant')
    rejects(lambda:d.shift(stats,wolf,'illegal',605,Wallet(),legal=False),'Illegal geometry does not mutate')

    stats,d=state(20);d.shift(stats,bear,'f',0,Wallet(),legal=True)
    check(d.shifts==8 and d.reserve==24,'Level20 free shifts do not refill finite benefits')
    d.natural_endpoint(stats,600,renew=True)
    check(d.reserve==24 and d.current.instance_id=='f','Level20 renewal preserves exact grant')
    check(d.finalize_damage_state(actual_hp=1,incapacitated=False,dead=False,unsupported=False) is None,'Actual instead1 retains form')
    result=d.finalize_damage_state(actual_hp=0,incapacitated=False,dead=False,unsupported=True)
    check(result['beginOrdinaryFall'] and not result['secondDamageResolution'] and not d.buffers.amount('d'),'Forced end/fall no second HP pool')
    stats,d=state();d.shift(stats,hawk,'h',0,Wallet(),legal=True)
    p=d.profile(stats,1,12,ac_components_certified=True)
    check(p['size']=='Tiny' and p['movement']=={'walk':10,'fly':60} and not p['canSpeak'],'Exact Hawk profile')
    check(p['mayCastDruidSpells'],'Beast Spells uses actual18 gate')
    rejects(lambda:d.profile(stats,1,20,ac_components_certified=False),'No unclassified melded AC')

    # Exact-source profile gates and an ordinary Action for all26 bodies.
    for index,(ident,p) in enumerate(PROFILES.items()):
        stats,d=state(20,p['circle'] or 'Moon',attuned=(ident,) if p['archAttunement'] else ())
        variant='air' if ident.endswith('elemental-shapeshifting') else 'ground' if ident.endswith('master-of-vermin') else None
        d.shift(stats,ident,'form'+str(index),0,Wallet(),legal=True,variant=variant)
        profile=d.profile(stats,0,12,ac_components_certified=True)
        check(profile['sourceId']==ident and profile['attack']['attack']==10,'Actual source profile '+ident)
        w=Wallet();attack=d.attack(stats,0,w,legal=True)
        check(w.actions==0 and not attack['unrelatedWeaponProcAuthorized'],'One natural Action '+ident)
    stats,d=state(10,'Moon')
    rejects(lambda:d.shift(stats,'druid.arch.dire-wolf','x',0,Wallet(),legal=True),'Arch level11 gate')
    stats,d=state(20,'Moon')
    rejects(lambda:d.shift(stats,'druid.arch.dire-wolf','x',0,Wallet(),legal=True),'Attunement required')
    rejects(lambda:d.shift(stats,'druid.hero.storm.tempest-raptor','x',0,Wallet(),legal=True),'No cross-Circle Hero form')

    moon='druid.hero.moon.mooncursed';stats,d=state();d.shift(stats,moon,'moon',0,Wallet(),legal=True)
    d.reserve=9;d.buffers.offer(grant('ally-big',20,target='a'))
    out=d.mooncursed_howl(stats,1,Wallet(),['a','b','c'],12,['a1','b1','c1'],legal=True)
    check(d.reserve==0 and out[0]['amount']==9 and not out[0]['accepted'] and out[1:]==[None,None],'Sequential9/0/0, rejected offer still pays')
    check(d.surges==5 and 'howl' in d.current.spent,'One shared mode opportunity')
    rejects(lambda:d.special(stats,1,Wallet(),'howl',legal=True),'Enemy mode cannot reuse same Howl')
    d.shift(stats,wolf,'w',2,Wallet(),legal=True);d.shift(stats,moon,'moon2',3,Wallet(),legal=True)
    d.mooncursed_howl(stats,3,Wallet(),['b'],5,['empty'],legal=True)
    check(d.surges==4 and 'empty' not in d.buffers.grants,'Exhausted legal Howl pays but creates no zero grant')
    stats,d=state();d.shift(stats,moon,'moon',0,Wallet(),legal=True)
    d.mooncursed_howl(stats,1,Wallet(),['a'],8,['ally'],legal=True)
    d.revert(2,Wallet(),legal=True);check(d.buffers.amount('a')==8,'Mooncursed ally shield survives reversion')
    d.buffers.completed_long_rest('a',1);check(d.buffers.amount('a')==0,'Mooncursed uses recipient default lifetime')

    earth='druid.arch.earth-warden-dire-bear';stats,d=state(attuned=(earth,));d.regular_start(1,0,actual_regular_marker=True)
    d.shift(stats,earth,'earth',0,Wallet(),legal=True);d.special(stats,0,Wallet(),'slam',legal=True)
    d.shift(stats,wolf,'wolf',1,Wallet(),legal=True);d.shift(stats,earth,'earth2',2,Wallet(),legal=True)
    rejects(lambda:d.special(stats,2,Wallet(),'slam',legal=True),'Slam recharge survives shifts')
    rejects(lambda:d.regular_start(2,6,actual_regular_marker=False),'Extra turn cannot tick recharge')
    d.regular_start(2,6,actual_regular_marker=True);rejects(lambda:d.special(stats,6,Wallet(),'slam',legal=True),'Recharge2 not ready next start')
    d.regular_start(3,12,actual_regular_marker=True);d.special(stats,12,Wallet(),'slam',legal=True)
    check(d.recharges[earth]==4,'Slam ready at second later regular start')

    frost='druid.hero.winterfang.frost-wyrmling';stats,d=state(circle='Winterfang')
    d.shift(stats,frost,'frost',0,Wallet(),legal=True);d.special(stats,0,Wallet(),'breath',legal=True)
    d.shift(stats,wolf,'wolf',1,Wallet(),legal=True);d.shift(stats,frost,'frost2',2,Wallet(),legal=True)
    rejects(lambda:d.special(stats,2,Wallet(),'breath',legal=True),'Breath remains spent across new instances')
    d.revert(3,Wallet(),legal=True);d.recharge_clock.leave_initiative(3)
    d.completed_short_rest(1,actual_completed=True,now=3603)
    d.shift(stats,frost,'frost3',3603,Wallet(),legal=True);d.special(stats,3603,Wallet(),'breath',legal=True)
    check(d.rest_uses['short:'+frost]==1,'Actual SR restores source use only')
    rejects(lambda:d.completed_short_rest(1,actual_completed=True,now=3603),'No fabricated repeated SR')

    elemental='druid.hero.moon.elemental-shapeshifting';stats,d=state()
    d.shift(stats,elemental,'air',0,Wallet(),legal=True,variant='air')
    d.natural_endpoint(stats,600,renew=True)
    check(d.rest_uses['long:elemental']==1,'Same Elemental renew does not pay entry use')
    d.shift(stats,elemental,'water',601,Wallet(),legal=True,variant='water')
    check(d.attack(stats,601,Wallet(),legal=True)['profile']['damageType']=='cold','Subtype identity sets actual damage')
    rejects(lambda:d.shift(stats,elemental,'fire',602,Wallet(),legal=True,variant='fire'),'Two Elemental entries remain finite at20')
    d.revert(603,Wallet(),legal=True);d.recharge_clock.leave_initiative(603)
    d.completed_long_rest(stats,1,attuned=(),actual_completed=True,now=29403)
    check(d.reserve==44 and d.surges==6 and d.instances['water'].state=='voluntary-reversion','Actual LR refills reserve without recreating ended form')

    brood='druid.hero.rotshaper.insect-broodmother';world=CreatureWorld();stats,d=state(circle='Rotshaper',creatures=world)
    out=d.shift(stats,brood,'brood',0,Wallet(),legal=True,spawn=True,spawn_legal=False)
    check(out['spawnPayment'] is None and d.surges==6,'Invalid optional spawn does not undo form or pay')
    rejects(lambda:d.special(stats,1,Wallet(),'spawn',legal=True),'No later spawn window')
    d.special(stats,1,Wallet(),'negate-critical',legal=True)
    check(d.surges==5,'Separate crit-negation still available')
    d.shift(stats,wolf,'wolf',2,Wallet(),legal=True)
    out=d.shift(stats,brood,'brood2',3,Wallet(),legal=True,spawn=True,spawn_legal=True)
    check(out['spawnPayment']['formSurgePaid'] and d.surges==4,'Valid entry spawn pays exactly one Surge')
    c=Creature('swarm','d','d','druid',brood,'swarm','finite',20,20,20,15,30,expiry=ClockMarker(63),parent_form='brood2')
    independent=replace(c,instance_id='independent',parent_form=None)
    world.creatures['swarm']=c;world.creatures['independent']=independent
    d.natural_endpoint(stats,603,renew=True)
    check(c.expiry==ClockMarker(63),'Renewal never extends independent creature deadline')
    d.revert(604,Wallet(),legal=True)
    check(c.state=='ended' and independent.state=='active','Parent ending only removes its own dependent swarm')

    # The same owner recharge clock continues outside combat and through rest.
    stats,d=state(attuned=(earth,));d.regular_start(1,0,actual_regular_marker=True)
    d.shift(stats,earth,'clock-earth',0,Wallet(),legal=True);d.special(stats,0,Wallet(),'slam',legal=True)
    d.recharge_clock.leave_initiative(0);d.recharge_clock.advance_outside(6)
    rejects(lambda:d.special(stats,6,Wallet(),'slam',legal=True),'Only one downtime tick after6 seconds')
    d.recharge_clock.advance_outside(12);d.special(stats,12,Wallet(),'slam',legal=True)
    check(d.recharges[earth]==4,'Twelve actual downtime seconds mature Recharge2')
    d.recharge_clock.enter_initiative(18);ticks=d.recharge_clock.ticks
    d.regular_start(2,18,actual_regular_marker=True)
    check(d.recharge_clock.ticks==ticks,'Initiative entry cannot double-count same due tick')
    d.regular_start(3,19,actual_regular_marker=True)
    check(d.recharge_clock.ticks==ticks,'Reordered start before canonical interval cannot fabricate tick')
    rejects(lambda:d.recharge_clock.advance_outside(24),'No parallel elapsed clock inside initiative')
    rejects(lambda:d.recharge_clock.leave_initiative(17),'No recharge time reversal')
    d.regular_start(4,24,actual_regular_marker=True);d.special(stats,24,Wallet(),'slam',legal=True)
    d.revert(25,Wallet(),legal=True);d.recharge_clock.leave_initiative(25)
    d.completed_short_rest(1,actual_completed=True,now=3625)
    d.shift(stats,earth,'after-sr',3625,Wallet(),legal=True);d.special(stats,3625,Wallet(),'slam',legal=True)
    check(d.recharges[earth]==d.recharge_clock.ticks+2,'Real SR elapsed time matured previous recharge')
    d.revert(3626,Wallet(),legal=True)
    d.completed_long_rest(stats,1,attuned=(earth,),actual_completed=True,now=32426)
    d.shift(stats,earth,'after-lr',32426,Wallet(),legal=True);d.special(stats,32426,Wallet(),'slam',legal=True)
    check(d.recharges[earth]==d.recharge_clock.ticks+2,'Real LR elapsed time matured previous recharge')

    # Global instance IDs prevent another owner's form cleanup touching summons.
    stats,d=state();d.shift(stats,wolf,'shared-name',0,Wallet(),legal=True)
    other_stats=DruidStats('other',20,6,4,4,4)
    other=DruidState(other_stats,'Moon',d.buffers,{'refrain':0,'rememberedSpell':None,'dissonance':0})
    w=Wallet();rejects(lambda:other.shift(other_stats,wolf,'shared-name',0,w,legal=True),'Cross-owner form ID collision rejected')
    check(w.bonus_action and other.current is None,'Collision preflight is unpaid and atomic')
    other.shift(other_stats,wolf,'other-unique',0,w,legal=True)
    check(other.current.instance_id=='other-unique' and d.current.instance_id=='shared-name','Two actual owners retain distinct form identities')

    # Enumerate competing values and damage: winner never stacks and conservation.
    scenarios=0
    for old in range(9):
        for new in range(9):
            for damage in range(13):
                b=BufferLedger()
                if old:b.offer(grant('old',old))
                b.offer(grant('new',new))
                winner=max(old,new)
                out,e=b.core_damage('d','packet',LifeState(100,100,winner),damage)
                assert b.amount('d')==max(0,winner-damage)
                assert out.hp==100-max(0,damage-winner)
                if old and old>=new and damage<old:assert b.current('d').grant_id=='old'
                scenarios+=1
    check(scenarios==1053,'Arbitration/damage conservation scenarios')
    report={'status':'PASS','checks':checks,'arbitrationDamageScenarios':scenarios,
            'formProfiles':len(PROFILES),'reviewStatus':'IMPLEMENTED; GPT implementation review pending',
            'scope':'Selected grant/form interface only; not full source cards, item/weapon taxonomy, full runtime or human balance.'}
    out=Path(__file__).resolve().parents[1]/'docs/mechanics/FORM_TEMP_HP_PLAYTEST_VALIDATION.json'
    out.write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(report))
if __name__=='__main__':main()

```

## Validation
```json
{
  "status": "PASS",
  "checks": 163,
  "arbitrationDamageScenarios": 1053,
  "formProfiles": 26,
  "reviewStatus": "IMPLEMENTED; GPT implementation review pending",
  "scope": "Selected grant/form interface only; not full source cards, item/weapon taxonomy, full runtime or human balance."
}
```
