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
        self.spell_anatomies={}

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
        self.ticks=0;self.last_regular=0;self.anchored=False

    def _time(self,now):
        marker=clock_marker(now);require(marker>=self.now,'Recharge time cannot move backward')
        return marker

    def _anchor(self,marker):
        if not self.anchored:
            self.next_tick=marker.seconds+6;self.anchored=True

    def regular_start(self,index,now,*,actual_regular_marker):
        marker=self._time(now);integer(index,'actual regular marker',1)
        require(self.mode=='initiative' and actual_regular_marker and index>self.last_regular,
                'New actual regular initiative marker required')
        self._anchor(marker)
        self.last_regular=index;self.now=marker
        if marker.seconds>=self.next_tick:
            self.ticks+=1;self.next_tick=marker.seconds+6

    def leave_initiative(self,now):
        marker=self._time(now);require(self.mode=='initiative','Already outside initiative')
        self._anchor(marker)
        self.now=marker;self.mode='outside'

    def advance_outside(self,now):
        marker=self._time(now);require(self.mode=='outside','Elapsed ticks only outside initiative')
        self._anchor(marker)
        if marker.seconds>=self.next_tick:
            count=int((marker.seconds-self.next_tick)//6)+1
            self.ticks+=count;self.next_tick+=6*count
        self.now=marker

    def enter_initiative(self,now):
        self.advance_outside(now);self.mode='initiative'

    def use(self,now):
        marker=self._time(now)
        self._anchor(marker)
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
        require(self.owner not in self.buffers.spell_anatomies,
                'End active spell anatomy through its legal procedure before Druid Shapeshift')
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
