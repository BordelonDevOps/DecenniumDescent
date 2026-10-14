# Time Loop parent conference: concentration, spell anatomy and Druid

The previous 50+76+22 bounded live-control checkpoint is recorded exactly as approved. Full Time Loop still has seven incomplete integration domains. Here is the actual current source code for the next parent integrations; it is evidence, not a claim they are implemented. No original source, catalog status, or global rule is being changed. The human already authorized GitHub push after our final whole-game flow agreement; that condition has not yet been met and does not need renewed human permission.

Please settle the following concrete cases together, using the twelve existing conservation decisions. Distinguish already-implied interpretations from any new provisional decision. Correct these proposed interpretations where necessary. Implementation review will follow separately.

1. **Participant concentration restoration.** A participant's snapshot Polymorph (absolute deadline still future) ended after initiative because of concentration failure. Proposed: restore that exact original cast/link and canonical end callback without a new cast/save/payment/start event, provided all dependent targets/gear/geometry are reconcilable. If that participant now concentrates on a different post-snapshot source, its entire source closure must retire without refund; unsupported or protected outsider consequences reject the rewind. Outsider casters' slots remain strictly current. Is that the intended full adapter beyond the exact-still-current restriction of the approved control bridge?

2. **Mixed-roster concentration.** Snapshot Mass Polymorph reaches one participant and one nonparticipant. Proposed: participant state may rewind while the nonparticipant's current link/state remains unchanged; only if a complete proposed shared cast/slot can maintain both. If reconstructing or retiring the parent's callback would end, revive, reapply or alter the outsider effect, reject. No synthetic half-cast and no replay of saves. Confirm or specify a simpler always-reject boundary for the first complete parent adapter.

3. **True Polymorph stabilization.** Snapshot link was shaping; the exact current link legitimately reached its original 60-second checkpoint and is permanent. Proposed: conserve permanent status and lack of concentration, restore compatible participant encounter state/geometry/gear, keep the same lineage/enrollment, and do not re-run checkpoint. What if that newly permanent link was then legitimately dispelled or replaced: can the old snapshot restore it as permanent, or must that historical world resolution make it unavailable? Please resolve the actual latter case rather than inferring from a current link.state label.

4. **Druid paid same-instance renewal.** Snapshot at t=599 has form F with deadline600. At t=600 the owner legally pays a shift and renews F to1200 (natural_endpoint updates the same instance). Rewind occurs at t=601 before round4. Proposed: conserve the actual paid renewal and F's current valid1200 endpoint, without refunding its shift; do not rebase to now+600 or reinstate expired600. A new form ID never inherits that extension. Confirm the exact endpoint when the same F subsequently ended before the rewind, and whether an explicit historical renewal receipt is required.

5. **Druid form-local and global expenditures.** A snapshot-unspent per-form special may regain its local permission, while current Form Surges, shifts, reserve, rest_uses, recharges and recharge-clock ticks stay spent/current. Snapshot-spent stays spent. A restored Broodmother never reopens its actual entry-only spawn window. Rest/attunement changes require exact current eligibility; absent a rest/progression adapter reject structural divergence. Confirm this separation, especially that a current exhausted global payment cannot be bypassed by restoring a local flag.

6. **Druid entry and dependent shields.** Restore exact original form and eligible snapshot entry-buffer grant/remaining amount without calling shift(), offering a new buffer or decrementing reserve again. Example: Bear entered with20, snapshot buffer12, spent8 more and reverted; valid F can restore12 and current reserve remains spent. Invalid/expired F cannot support its entry shield. Mooncursed Howl uses recipient LR rather than form dependency in current helper; it follows its original independent grant lifetime. Confirm both. All other active shield sources still require explicit policies.

7. **Recharge bridge and authentic markers.** Proposed: one existing OwnerRechargeClock per actual Druid, preserve all its fields and recharges. kernel.regular_start supplies its monotonic global_regular to DruidState.regular_start exactly once, only for that owner's genuine start. A first post-loop start at unchanged world seconds advances marker identity but does not manufacture a six-second tick. Restore calls no clock method. A prepared plan watches every clock/finite field and rejects if a real tick/rest occurs before commit. Initiative entry/exit still use the same ordinary clock. Confirm.

8. **Shapechange and hostile repeat windows.** Current TransformationWorld uses numeric regular_index and round_number. Proposed source wrapper uses authenticated iteration-qualified turn/round windows for once/later-regular-turn switches and damage repeat saves, preserving historical event IDs. Absolute deadline remains unchanged; no save at restore. Clarify 'later than original casting turn' for an outside-origin snapshot Shapechange in new iteration round1, and a restored hostile link whose first HP-damage save was consumed only after snapshot.

9. **Druid cadence.** shift() clears refrain and rememberedSpell only on actual entry. Temporal restoration must not call it. Are the participant's snapshot refrain/rememberedSpell/dissonance independently rewindable encounter state, or conserved finite class economy? The current Druid adapter shares a canonical cadence dict; the complete class-cadence adapter is not present. Proposed initial parent implementation rejects any scene requiring changes to that cadence until its source-specific policy exists, rather than inventing a reset. Please identify the policy or required source evidence.

10. **Expired forms and current external effects.** If snapshot Druid/temporary spell form has expired at current world time without a valid same-instance extension, proposal is to reject when restoring that snapshot's anatomy requires replaying the expired endpoint; do not silently grant a fresh form or drop the form while restoring dependent movement/gear/shields. Existing external suppression is preserved only through exact canonical records and simultaneous legal geometry. Is any supported normalization to base anatomy already authorized, or should these cases remain unavailable pending a specific reconciliation?

Source limitations to preserve: current DruidState does not own gear or a body HP copy. TransformationWorld.Body.life must alias Core life; its buffers/concentration must be the same objects as other adapters. The first full implementation must not invent a separate form world, calendar, concentration pool, HP pool or persistent slot map. Complete creature/physical/device dependencies still require their adapters; empty registries do not prove scene completeness.


## Exact current file: tools/form_temphp_playtest_rules.py
SHA-256: `97566962d3eddeca5966b4b58bbb3a5e53dc34d529afb5de033d4358397e2151`

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

```

## Exact current file: tools/transformation_spell_playtest_rules.py
SHA-256: `91697863f6d19043787e17f19b4c127e6c32de32ad3867393566212533081d39`

```python
"""Five-spell reference adapter. CANDIDATE: independent review pending.

Not a complete combat engine. Caller supplies canonical cast/access/geometry
legality, current caster statistics, actual save results, original-turn markers,
and already-finalized HP outcomes. One world/ledger per game; do not copy HP or
command ledgers. All preflight occurs before payment, then concentration ends,
then counters/saves resolve. Nothing here grants a class feature or source use.
"""
from dataclasses import dataclass, field
from copy import deepcopy
from itertools import combinations, product
from pathlib import Path
import json

from spell_playtest_rules import SpellRuleError, integer
from form_temphp_playtest_rules import BufferLedger, BufferGrant, require
from redirection_playtest_rules import identity
from device_lifecycle_playtest_rules import Wallet, CommandLedger

PROFILES={p['id']:p for p in json.loads((Path(__file__).resolve().parents[1]/'data/playtest/spell_form_profiles.json').read_text(encoding='utf-8'))['profiles']}
SPELLS={'polymorph':4,'shapechange':9,'true-polymorph':9,'mass-polymorph':9}
SIZES=('Tiny','Small','Medium','Large','Huge','Gargantuan')
TEMPLATES=frozenset({'barrier/slab','ramp/wedge','open-container','static-furniture','simple-one-piece-tool'})


@dataclass(frozen=True)
class CastStats:
    owner: str
    source_class: str
    attack: int
    dc: int
    pb: int
    modifier: int

    def __post_init__(self):
        identity(self.owner);identity(self.source_class)
        require(type(self.attack) is int,'Actual signed spell attack required')
        integer(self.dc,'spell DC',1);integer(self.pb,'PB',2,6)
        integer(self.modifier,'M=max(1, casting modifier)',1)


@dataclass(frozen=True)
class CastPrice:
    spell_id: str
    rank: int
    base_paid: int
    other_paid: int
    quote: dict=field(compare=False)

    @classmethod
    def from_quote(cls,quote,*,actual_base_paid=None,exact_reduction_authorized=False):
        """Consume canonical quote_cast result; exact class discounts are external.

        This does not establish known/prepared access or grant a discount. Those
        gates must already have passed in the caller's source-qualified preflight.
        Refrain/Dissonance/trauma follow quote plus the canonical class interface.
        """
        base=integer(quote['baseRpCost'],'quoted base RP',0)
        extra=integer(quote['additionalRpCost'],'quoted additional RP',0)
        surcharge=integer(quote['surcharge'],'quoted surcharge',0)
        require(quote['cost']==base+extra+surcharge,'Inconsistent canonical quote')
        paid=base if actual_base_paid is None else integer(actual_base_paid,'actual base paid',0,base)
        require(paid==base or exact_reduction_authorized,'Exact base reduction authority required')
        identity(quote['spellId']);integer(quote['rank'],'rank',0,9)
        return cls(quote['spellId'],quote['rank'],paid,extra+surcharge,deepcopy(quote))

    @property
    def total(self):return self.base_paid+self.other_paid


def harmonic_bulwark(ledger,stats,price,wallet,grant_id,target,conversion,now,*,legal,countered=False):
    """Commit everything before countering/arbitration; return cadence quote.

    Exact free-copy permissions need their own source adapter. This method is a
    fresh paid cast and will not mint an offer with zero credited RP.
    """
    require(isinstance(ledger,BufferLedger) and isinstance(stats,CastStats),'Canonical state required')
    require(legal and price.spell_id=='harmonic-bulwark' and price.rank==3,'Legal Harmonic Bulwark cast required')
    integer(conversion,'conversion X',0,stats.pb)
    credited=price.base_paid+conversion
    require(credited>0,'Zero credited RP cannot create a fresh shield')
    if not hasattr(ledger,'ordinary_cast_events'):ledger.ordinary_cast_events=set()
    require(grant_id not in ledger.ordinary_cast_events,'Cast identity already committed, including countered casts')
    grant=BufferGrant(grant_id,'ordinary-spell:harmonic-bulwark',stats.owner,target,5*credited,
                      rest_epoch=ledger.rest_epochs.get(target,0))
    ledger.validate_offer(grant,now)
    wallet.validate(rp=price.total+conversion,action='action')
    wallet.pay(rp=price.total+conversion,action='action')
    ledger.ordinary_cast_events.add(grant_id)
    return {'paidRP':price.total+conversion,'creditedRP':credited,'cadenceQuote':deepcopy(price.quote),
            'offer':None if countered else ledger.offer(grant,now),'countered':bool(countered)}


class ConcentrationLedger:
    """One ledger shared by ALL concentration spells, including other adapters.

    Each entry's end callback must be total/nonthrowing after valid preflight.
    Starting after payment always destroys the former entry, even if the new
    spell is countered or every target saves. Call end on actual concentration
    failure/incapacitation or a legal voluntary release.
    """
    def __init__(self):self.current={}

    def end(self,owner,reason):
        old=self.current.pop(owner,None)
        if old:old[1](reason)
        return old[0] if old else None

    def start_committed(self,owner,cast_id,on_end):
        old=self.end(owner,'new-concentration')
        self.current[owner]=(cast_id,on_end)
        return old

    def detach(self,owner,cast_id):
        if self.current.get(owner,(None,))[0]==cast_id:del self.current[owner]


@dataclass(frozen=True)
class PhysicalOrigin:
    identity: str
    kind: str
    size: str
    type_tags: frozenset=frozenset()
    mass: int | None=None
    value: int | None=None

    def __post_init__(self):
        identity(self.identity);require(self.kind in ('creature','object'),'Immutable origin kind required')
        require(self.size in SIZES,'Actual original size required')
        if self.mass is not None:integer(self.mass,'recorded origin mass',1)
        if self.value is not None:integer(self.value,'documented original value',0)


@dataclass
class Body:
    """Single underlying physical identity. No transformation HP field exists.

    life is the actual mutable/canonical character or structural ledger object;
    the adapter never heals, reconstructs or replaces it. Origin is immutable.
    Gear IDs and availability represent real items, not inventory creation.
    """
    origin: PhysicalOrigin
    life: object
    size: str
    mass: int | None=None
    equipment: set=field(default_factory=set)
    melded: set=field(default_factory=set)
    lost_items: set=field(default_factory=set)
    destroyed: bool=False
    anatomy: str | None=None
    slot_sponsor: str | None=None
    controller: str | None=None
    placement_pending: bool=False
    placement_conflict: bool=False

    @property
    def identity(self):return self.origin.identity


@dataclass(frozen=True)
class Selection:
    target: str
    profile: str | None
    willing: bool
    # Geometry caller supplies occupied cells at the post-concentration-save
    # stage; every possible unchanged/transformed shape must individually fit.
    original_cells: frozenset
    transformed_cells: frozenset
    legal: bool
    object_template: str | None=None
    object_size: str | None=None
    object_mass: int | None=None
    object_value: int | None=None
    object_input_eligible: bool=False
    mundane_output_certified: bool=False


@dataclass
class Link:
    identity: str
    cast_id: str
    target: str
    profile: str | None
    willing: bool
    deadline: int
    state: str='shaping'
    object_template: str | None=None
    object_size: str | None=None
    object_mass: int | None=None
    last_switch: int | None=None
    suppressed: bool=False


@dataclass
class Cast:
    identity: str
    spell_id: str
    caster: str
    rank: int
    stats: CastStats
    casting_regular_index: int
    links: list=field(default_factory=list)
    state: str='committed'


def validate_mass_space(selections):
    require(1<=len(selections)<=10 and len({s.target for s in selections})==len(selections),
            'Choose1..10 distinct physical targets')
    for s in selections:
        require(s.legal and s.original_cells and s.transformed_cells,'Both possible footprints must individually fit')
    for a,b in combinations(selections,2):
        for aa,bb in product((a.original_cells,a.transformed_cells),(b.original_cells,b.transformed_cells)):
            require(aa.isdisjoint(bb),'Independent Mass outcomes could overlap')


class TransformationWorld:
    """Bounded anatomy/concentration bridge; no hidden previous-form stack."""
    def __init__(self,buffers,concentration):
        require(isinstance(buffers,BufferLedger) and isinstance(concentration,ConcentrationLedger),'Canonical shared ledgers required')
        self.buffers=buffers;self.concentration=concentration
        self.bodies={};self.casts={};self.links={};self.slots={};self.druids={}
        self.damage_rounds=set();self.damage_events=set();self.regular_ends=set();self.commands={}
        self.events=[]
        # Shared with the Druid admission bridge, including suppressed records.
        if not hasattr(buffers,'spell_anatomies'):buffers.spell_anatomies={}

    def add_body(self,body,*,druid=None):
        require(isinstance(body,Body) and body.identity not in self.bodies,'Register each physical identity once')
        require(body.size in SIZES and body.life is not None,'Actual anatomy and HP ledger required')
        require(not body.anatomy and not body.melded and not body.slot_sponsor,'Register at original anatomy, or restore complete serialized world')
        self.bodies[body.identity]=body
        if druid is not None:
            require(druid.owner==body.identity and druid.buffers is self.buffers,'Druid must share world and owner')
            self.druids[body.identity]=druid

    def current(self,target):
        body=self.bodies[target]
        return self.links.get(body.anatomy)

    def _current_creature(self,body):
        link=self.current(body.identity)
        if link and not link.suppressed:return link.profile is not None
        return body.origin.kind=='creature'

    def _validate_selection(self,spell_id,rank,s,caster):
        identity(s.target);require(s.target in self.bodies,'Known physical target required')
        b=self.bodies[s.target];old=self.current(s.target)
        require(s.legal and not b.destroyed,'Legal live physical target required')
        require(s.original_cells and s.transformed_cells,'Both individually legal footprints required')
        ends_own_concentration=bool(old and old.state=='shaping' and self.casts[old.cast_id].caster==caster)
        active_transformed_object=bool(old and old.profile is None and self.casts[old.cast_id].spell_id=='true-polymorph')
        # Validate target anatomy after the mandatory end of own concentration.
        creature=b.origin.kind=='creature' if ends_own_concentration else self._current_creature(b)
        if spell_id!='true-polymorph':require(creature,'This spell requires creature anatomy')
        if spell_id=='shapechange':require(s.target==caster and s.willing,'Shapechange is self only')
        if old and not ends_own_concentration:
            if old.state=='permanent':
                require(spell_id=='true-polymorph','Permanent True anatomy requires a new True Polymorph')
            else:require(rank>=self.casts[old.cast_id].rank,'New rank cannot replace higher-rank anatomy')
        if s.profile is not None:
            require(s.profile in PROFILES,'Unknown finite spell profile')
            p=PROFILES[s.profile]
            require(spell_id not in ('polymorph','mass-polymorph') or p['tier']=='R4','R9 profile unavailable')
            require(b.origin.kind!='object' or s.profile!='spellform.humanoid','Object origin cannot gain humanoid profile')
        else:
            require(spell_id=='true-polymorph' and (not (creature or b.origin.kind=='creature') or s.willing),
                    'Object output requires True and willingness of a retained creature-origin person')
            require(s.object_template in TEMPLATES and s.mundane_output_certified,'Bounded inert mundane template required')
            input_size=b.origin.size if ends_own_concentration else b.size
            input_mass=b.origin.mass if ends_own_concentration else b.mass
            require(s.object_size in SIZES[:4] and abs(SIZES.index(s.object_size)-SIZES.index(input_size))<=1,'Object output size illegal')
            require(input_mass is not None and b.origin.mass is not None,'Canonical current/origin mass required')
            integer(s.object_mass,'output mass',1,min(input_mass,b.origin.mass))
            if b.origin.kind=='object':
                require(b.origin.value is not None,'Original documented value required')
                integer(s.object_value,'output value',0,b.origin.value)
            else:require(s.object_value==0,'Creature body has no independent recoverable/sale value')
        if not creature:
            require(spell_id=='true-polymorph' and (active_transformed_object or s.object_input_eligible),
                    'Fresh outside objects require eligibility; an active True object record uses legal replacement')
        if b.origin.kind=='object' and s.profile is not None:
            sponsor=caster if ends_own_concentration else b.slot_sponsor or caster
            occupant=self.slots.get(sponsor)
            occupied_link=self.current(occupant) if occupant is not None else None
            freed_by_commit=bool(occupied_link and occupied_link.state=='shaping' and self.casts[occupied_link.cast_id].caster==caster)
            require(occupant in (None,b.identity) or freed_by_commit,'Original caster object-creature slot occupied')
        return b

    def cast(self,cast_id,spell_id,stats,price,wallet,selections,now,regular_index,*,legal,resolve_save,countered=False):
        """resolve_save(target, DC) executes only AFTER committed payment.

        It returns True on success (or an exact legendary defense); False on
        failure. Caller must provide a nonthrowing authoritative resolver. All
        actual die rolls/target condition legality remain in the combat engine.
        """
        identity(cast_id);integer(now,'cast timestamp',0);integer(regular_index,'original regular index',0)
        require(legal and spell_id in SPELLS and price.spell_id==spell_id and price.rank==SPELLS[spell_id],'Legal canonical quote/access required')
        require(cast_id not in self.casts and cast_id not in self.buffers.form_instances,'Cast identity already used')
        require(len(selections)==1 or spell_id=='mass-polymorph','Single-target spell')
        if spell_id=='mass-polymorph':validate_mass_space(selections)
        else:require(len(selections)==1,'Exactly one target required')
        for s in selections:
            self._validate_selection(spell_id,price.rank,s,stats.owner)
            require(cast_id+':'+s.target not in self.buffers.form_instances,'World form/link identity already used')
        wallet.validate(rp=price.total,action='action')
        # All potentially invalid requests rejected above. No refunds below.
        wallet.pay(rp=price.total,action='action')
        record=Cast(cast_id,spell_id,stats.owner,price.rank,stats,regular_index)
        self.casts[cast_id]=record;self.buffers.form_instances.add(cast_id)
        self.concentration.start_committed(stats.owner,cast_id,lambda reason:self._end_cast(cast_id,reason))
        if countered:
            record.state='countered';self.concentration.detach(stats.owner,cast_id)
            return {'castId':cast_id,'links':[],'paidRP':price.total,'countered':True,'cadenceQuote':deepcopy(price.quote)}
        successful=[]
        for s in selections:
            body=self.bodies[s.target]
            # Object anatomy never strips a retained creature-origin person's
            # save. Object-origin creature targets retain normal current-form saves.
            needs_save=(self._current_creature(body) or body.origin.kind=='creature') and not s.willing
            if not needs_save or not resolve_save(s.target,stats.dc):successful.append(s)
        # Choices are fixed before rolling; no sequential geometry re-evaluation.
        for s in successful:self._apply(record,s,now)
        record.state='active' if record.links else 'no-target-links'
        if not record.links:self.concentration.detach(stats.owner,cast_id)
        return {'castId':cast_id,'links':list(record.links),'paidRP':price.total,'countered':False,'cadenceQuote':deepcopy(price.quote)}

    def _apply(self,record,s,now):
        b=self.bodies[s.target]
        old=self.current(s.target)
        if old:self._end_link(old,'replaced',continuous=True)
        druid=self.druids.get(s.target)
        if druid and druid.current:druid._end('spell-transformation')
        link_id=record.identity+':'+s.target
        link=Link(link_id,record.identity,s.target,s.profile,s.willing,now+60,
                  object_template=s.object_template,object_size=s.object_size,object_mass=s.object_mass)
        self.links[link_id]=link;record.links.append(link_id);self.buffers.form_instances.add(link_id)
        b.anatomy=link_id
        self.buffers.spell_anatomies[b.identity]=link_id
        b.placement_pending=False;b.placement_conflict=False
        # Close-and-recapture: old record restores still-existing meld items,
        # then this new record captures them without an intervening action window.
        b.melded.update(b.equipment);b.equipment.clear()
        b.size=PROFILES[s.profile]['size'] if s.profile else s.object_size
        if s.profile is None:b.mass=s.object_mass
        if b.origin.kind=='object' and s.profile:
            if b.slot_sponsor is None:b.slot_sponsor=record.caster;b.controller=record.caster
            self.slots[b.slot_sponsor]=b.identity
        elif b.slot_sponsor:self._release_slot(b)

    def _release_slot(self,b):
        if b.slot_sponsor and self.slots.get(b.slot_sponsor)==b.identity:del self.slots[b.slot_sponsor]
        b.slot_sponsor=None

    def _end_link(self,link,reason,*,continuous=False):
        if link.state not in ('shaping','permanent'):return
        b=self.bodies[link.target];record=self.casts[link.cast_id]
        link.state=reason
        if b.anatomy==link.identity:b.anatomy=None
        if self.buffers.spell_anatomies.get(b.identity)==link.identity:
            del self.buffers.spell_anatomies[b.identity]
        self.buffers.end_dependency(link.identity)
        b.equipment.update(b.melded-b.lost_items);b.melded.clear()
        b.size=b.origin.size;b.mass=b.origin.mass
        if not continuous:self._release_slot(b)
        if not continuous:
            b.placement_pending=True
            self.events.append({'target':b.identity,'reason':reason,'sameSpatialAnchor':True,
                                'placementCheckRequired':True,'noHealingOrAutomaticMovement':True})
        if not any(self.links[i].state=='shaping' for i in record.links):
            self.concentration.detach(record.caster,record.identity)

    def _end_cast(self,cast_id,reason):
        record=self.casts[cast_id]
        for ident in record.links:
            link=self.links[ident]
            if link.state=='shaping':self._end_link(link,reason)
        record.state=reason

    def _active(self,target,now,*,allow_boundary=False,allow_suppressed=False):
        link=self.current(target)
        require(link is not None and link.state in ('shaping','permanent'),'No operative spell anatomy')
        require(allow_suppressed or not link.suppressed,'Anatomy is currently suppressed')
        if link.state=='shaping':
            require(now<=link.deadline if allow_boundary else now<link.deadline,'Resolve actual60-second checkpoint first')
        return link

    def repeat_save(self,target,stats,now,*,trigger,event_or_turn,round_number=None,normal_hp_damage=0,success):
        link=self._active(target,now,allow_boundary=True,allow_suppressed=True);record=self.casts[link.cast_id]
        require(link.state=='shaping' and not link.willing and link.profile is not None,'No hostile repeat-save permission')
        require(stats.owner==record.caster,'Original caster statistics required')
        identity(event_or_turn)
        if trigger=='regular-end':
            key=(target,event_or_turn)
            require(key not in self.regular_ends,'Original regular endpoint already handled')
            self.regular_ends.add(key)
        elif trigger=='damage':
            integer(normal_hp_damage,'actual normal HP damage',1);integer(round_number,'numbered round',1)
            key=(target,round_number)
            require(key not in self.damage_rounds,'First positive HP damage repeat already used this round')
            require((target,event_or_turn) not in self.damage_events,'Damage event already processed')
            self.damage_rounds.add(key)
            self.damage_events.add((target,event_or_turn))
        else:raise SpellRuleError('Only actual original regular end or first positive normal-HP damage')
        dc=record.stats.dc if record.spell_id=='true-polymorph' else stats.dc
        if success:self._end_link(link,'repeat-save')
        return {'dc':dc,'ended':bool(success),'target':target}

    def checkpoint(self,now,*,started_packets_and_due_saves_finished):
        integer(now,'absolute checkpoint',0)
        require(started_packets_and_due_saves_finished,'Finish packets and due repeat saves before checkpoint')
        result=[]
        for link in self.links.values():
            if link.state!='shaping' or now<link.deadline:continue
            record=self.casts[link.cast_id]
            if record.spell_id=='true-polymorph':
                link.state='permanent';self.concentration.detach(record.caster,record.identity)
                result.append({'link':link.identity,'state':'permanent'})
            else:
                self._end_link(link,'expired');result.append({'link':link.identity,'state':'expired'})
        return result

    def reject(self,target,now,wallet,*,actual_regular_turn,legal):
        link=self._active(target,now,allow_suppressed=True);record=self.casts[link.cast_id];b=self.bodies[target]
        action_capable=(not link.suppressed and link.profile is not None) or (link.suppressed and b.origin.kind=='creature')
        require(link.state=='shaping' and link.willing and b.origin.kind=='creature' and action_capable and legal and actual_regular_turn,
                'Only a willing temporary creature-origin recipient with expressed action-capable anatomy may reject')
        require(record.spell_id!='shapechange','Shapechange uses ordinary concentration release')
        wallet.validate(action='action');wallet.pay(action='action');self._end_link(link,'willing-rejection')

    def finalize_damage_state(self,target,*,actual_hp,incapacitated,dead,destroyed=False,unsupported=False):
        """After Core damage and ALL same-packet replacement/prevention. No reroll."""
        integer(actual_hp,'actual final HP',0);b=self.bodies[target];link=self.current(target)
        recorded_hp=b.life.get('hp') if isinstance(b.life,dict) else b.life.hp
        require(recorded_hp==actual_hp,'Project the actual finalized canonical HP ledger before anatomy cleanup')
        if b.origin.kind=='object' and actual_hp==0:
            b.destroyed=True
            if link:self._end_link(link,'physical-destruction')
        elif destroyed:
            b.destroyed=True
            if link and link.state=='shaping':self._end_link(link,'physical-destruction')
        elif link and link.state=='shaping' and (actual_hp==0 or incapacitated or dead):self._end_link(link,'forced-reversion')
        return {'sameHPLedger':b.life,'beginOrdinaryFall':bool(unsupported),'secondDamageResolution':False}

    def check_reversion_placement(self,target,*,fits_at_current_anchor):
        b=self.bodies[target]
        require(b.placement_pending,'No pending root-anatomy placement check')
        b.placement_pending=False;b.placement_conflict=not fits_at_current_anchor
        return {'placementConflict':b.placement_conflict,'sameSpatialAnchor':True,
                'requiresCanonicalGeometryResolution':b.placement_conflict,'automaticDamage':0,'automaticRelocation':False}

    def clear_geometry_conflict(self,target,*,canonical_resolution_completed):
        require(canonical_resolution_completed,'Actual canonical geometry resolution required')
        self.bodies[target].placement_pending=False;self.bodies[target].placement_conflict=False

    def dispel(self,target,*,legal):
        require(legal and self.current(target) is not None,'Actual successful dispel required')
        self._end_link(self.current(target),'dispelled')

    def set_suppressed(self,target,now,*,suppressed,legal):
        link=self._active(target,now,allow_suppressed=True);b=self.bodies[target]
        require(legal and link.suppressed!=suppressed,'Actual changed antimagic state required')
        link.suppressed=bool(suppressed)
        b.size=b.origin.size if suppressed else PROFILES[link.profile]['size'] if link.profile else link.object_size
        b.mass=b.origin.mass if suppressed or link.profile else link.object_mass
        # No gear recapture, slot release, benefit entry, HP change or clock reset.
        b.placement_pending=True
        return {'sameRecord':link.identity,'deadline':link.deadline,'placementCheckRequired':True,
                'sameMeldSet':frozenset(b.melded),'slotSponsor':b.slot_sponsor}

    def _stats_for(self,link,stats):
        record=self.casts[link.cast_id]
        require(isinstance(stats,CastStats) and stats.owner==record.caster,'Use original caster statistics')
        return record.stats if record.spell_id=='true-polymorph' else stats

    def profile(self,target,stats,now,form_normal_ac,*,ac_components_certified):
        link=self._active(target,now);b=self.bodies[target]
        require(not b.placement_pending and not b.placement_conflict,'Resolve physical placement before movement/targeting')
        integer(form_normal_ac,'operative form normal AC',0)
        require(ac_components_certified,'Exclude melded armor/shield; certify compatible passives/external equipment')
        types=sorted(b.origin.type_tags) if b.origin.kind=='creature' else ['transformed-object']
        if link.profile is None:
            return {'ac':12,'size':link.object_size,'movement':{},'speech':False,'hands':False,
                    'ordinarySenses':False,'actions':False,'bonusActions':False,'reactions':False,
                    'actionlessObjectAnatomy':True,'appliesIncapacitated':False,'targetKind':'object',
                    'originTypeTags':types,'grantedResistances':[],'sameHPLedger':b.life}
        p=deepcopy(PROFILES[link.profile]);mode=p['ac']['mode'];amount=p['ac']['amount']
        p['ac']=form_normal_ac if mode=='normal' else max(form_normal_ac,amount) if mode=='floor' else amount
        provider=self._stats_for(link,stats)
        p['attack'].update({'attack':provider.attack,'modifier':provider.modifier,'reachFeet':5,
                            'attacker':target,'statProvider':provider.owner,'spellcast':False,
                            'directCasterSpellDamage':False,'sourceSpell':self.casts[link.cast_id].spell_id,
                            'sourceLink':link.identity})
        p.update({'targetKind':'creature','typeTags':types,'sameHPLedger':b.life,'ordinarySenses':True,
                  'grantsSpecialSenses':False,'grantsResources':False,'grantsMultiattack':False})
        if b.origin.kind=='object':p.update({'saves':provider.pb,'ordinaryChecks':0,'soul':False,
            'wounds':False,'deathSaves':False,'resurrection':False,'ordinaryHealing':False,
            'companionPhase':'attached','uncommanded':['move','Dodge']})
        return p

    def healing_target_eligible(self,target,*,native_eligible):
        b=self.bodies[target]
        return bool(native_eligible and not b.destroyed and b.origin.kind=='creature' and self._current_creature(b))

    def acquire_external_gear(self,target,item_id,now,*,compatible_and_equipped):
        link=self._active(target,now);b=self.bodies[target];identity(item_id)
        require(link.profile is not None and PROFILES[link.profile]['hands'] and compatible_and_equipped,
                'Actual compatible external equipment required')
        require(item_id not in b.melded and item_id not in b.equipment and item_id not in b.lost_items,'Item identity unavailable/already recorded')
        b.equipment.add(item_id)

    def mark_item_lost(self,target,item_id,*,actual_loss):
        require(actual_loss,'Actual destroyed/consumed/lost item event required')
        b=self.bodies[target];require(item_id in b.melded or item_id in b.equipment,'Unknown held/melded item')
        b.equipment.discard(item_id);b.melded.discard(item_id);b.lost_items.add(item_id)

    def switch_shapechange(self,target,profile,now,regular_index,wallet,*,original_regular_turn,legal,retained_gear,drop_placement_legal,unsupported=False):
        link=self._active(target,now);record=self.casts[link.cast_id];b=self.bodies[target]
        require(record.spell_id=='shapechange' and record.caster==target,'Only actual self Shapechange may switch')
        require(original_regular_turn and regular_index>record.casting_regular_index and regular_index!=link.last_switch,
                'Switch once on a later original regular turn only')
        require(profile in PROFILES and profile!=link.profile and legal,'Different legal finite profile required')
        require(b.origin.kind!='object' or profile!='spellform.humanoid','Object-origin humanoid prohibited')
        keep=set(retained_gear)
        require(keep<=b.equipment and (not keep or PROFILES[profile]['hands']),'Only certified anatomy-compatible external gear may remain')
        dropped=b.equipment-keep
        require(not dropped or drop_placement_legal,'Resolve legal current/nearest adjacent item placement before switch')
        wallet.validate(action='bonus');wallet.pay(action='bonus')
        b.equipment=keep;link.profile=profile;link.last_switch=regular_index;b.size=PROFILES[profile]['size']
        return {'sameRecord':link.identity,'droppedItemIds':sorted(dropped),'spellcast':False,'paidRP':0,
                'refrainEvent':False,'beginOrdinaryFall':bool(unsupported and not PROFILES[profile]['movement'].get('fly'))}

    def attack(self,target,stats,now,wallet,*,legal):
        link=self._active(target,now);b=self.bodies[target]
        require(legal and b.origin.kind=='creature' and link.profile is not None,'Legal subject natural attack required; object companions use command adapter')
        require(not b.placement_pending and not b.placement_conflict,'Unresolved placement cannot authorize targeting')
        provider=self._stats_for(link,stats)
        wallet.validate(action='action');wallet.pay(action='action')
        return self._attack_packet(link,provider)

    def _attack_packet(self,link,provider):
        attack=deepcopy(PROFILES[link.profile]['attack'])
        attack.update({'reachFeet':5,'attacker':link.target,'statProvider':provider.owner,'attack':provider.attack,
                       'modifier':provider.modifier,'sourceSpell':self.casts[link.cast_id].spell_id,
                       'sourceLink':link.identity,'spellcast':False,'directCasterSpellDamage':False,
                       'importsMultiattack':False,'weaponOnlyFeaturesAuthorized':False})
        return attack

    def command(self,target,order_id,now,round_number,ledger,wallet,*,mode,legal,distance,owner_perceives):
        link=self._active(target,now);b=self.bodies[target];identity(order_id)
        require(b.origin.kind=='object' and link.profile is not None and b.slot_sponsor is not None,'Active object-origin creature required')
        require(isinstance(ledger,CommandLedger) and ledger.owner==b.controller,'Current controller canonical shared command ledger required')
        require(not b.placement_pending and not b.placement_conflict,'Resolve placement before issuing a command')
        require(legal and owner_perceives and 0<=distance<=60,'Actual60-foot command legality required')
        require(mode in ('support','attack','control') and order_id not in self.commands,'Fresh supported command required')
        ledger.activate(round_number,mode,wallet)
        self.commands[order_id]={'target':target,'link':link.identity,'controller':b.controller,'mode':mode,'resolved':False}
        return {'orderId':order_id,'phase':'attached','independentTurn':False}

    def resolve_command(self,order_id,stats,now,*,attached_phase,still_legal):
        order=self.commands.get(order_id)
        require(order is not None and not order['resolved'] and attached_phase,'Actual unresolved attached command required')
        b=self.bodies[order['target']];link=self.current(b.identity)
        order['resolved']=True
        if (not still_legal or not link or link.identity!=order['link'] or link.suppressed
            or b.controller!=order['controller'] or b.destroyed or b.placement_pending or b.placement_conflict
            or (link.state=='shaping' and now>=link.deadline)):
            return {'executed':False,'refunded':False}
        self._active(b.identity,now)
        if order['mode']=='attack':return {'executed':True,'attack':self._attack_packet(link,self._stats_for(link,stats))}
        return {'executed':True,'mode':order['mode'],'damageAuthorized':False,'profileGrantsNoExtraControlPower':True}

    def uncommanded(self,target,now):
        link=self._active(target,now);b=self.bodies[target]
        require(b.origin.kind=='object' and link.profile is not None,'Actual object companion required')
        return {'options':['move','Dodge'],'damageAuthorized':False,'independentTurn':False}

```

## All26 actual Druid source profiles: costs, entry buffers and specials

```json
{
  "druid.base.wolf-form-striker": {
    "sourceId": "druid.base.wolf-form-striker",
    "sourceSha256": "7f886ec4aad2d5dc08b8eb79ac0ab2b2b83064449c2dd44a7a1ca73453864576",
    "sourceProcedure": {
      "id": "druid.base.wolf-form-striker",
      "name": "Wolf Form (Striker)",
      "className": "Druid",
      "band": "Base",
      "path": null,
      "sourceKind": "form",
      "minimumClassLevel": 1,
      "acquisition": "automatic",
      "activation": "Action attack; passive form traits",
      "cost": "One shift to enter",
      "rangeAndTarget": "Self; bite 5 ft",
      "duration": "While in Wolf",
      "frequency": "One bite/Action",
      "effect": "Speed 40 ft; advantage on hearing/smell Perception. Bite 1d8 piercing+WIS; target STR save against Druid DC or Prone, once/target/round. All damage remains your own HP.",
      "spellRank": null
    },
    "minimumLevel": 1,
    "circle": null,
    "archAttunement": false,
    "entryBuffer": 0,
    "specials": {}
  },
  "druid.base.bear-form-tank": {
    "sourceId": "druid.base.bear-form-tank",
    "sourceSha256": "d62efe277f4dfe0f210af41e3bb70eca6646d24f7501fa709a0269b5c4d349b7",
    "sourceProcedure": {
      "id": "druid.base.bear-form-tank",
      "name": "Bear Form (Tank)",
      "className": "Druid",
      "band": "Base",
      "path": null,
      "sourceKind": "form",
      "minimumClassLevel": 1,
      "acquisition": "automatic",
      "activation": "Action attack; passive form traits",
      "cost": "One shift; buffer drawn from reserve",
      "rangeAndTarget": "Self; claw 5 ft",
      "duration": "While in Bear",
      "frequency": "One claw/Action",
      "effect": "Gain up to 20 temporary HP from reserve; AC max(normal, 14). Claw 2d6 slashing+WIS+1. Buffer disappears on reversion and cannot be refilled through free shifting.",
      "spellRank": null
    },
    "minimumLevel": 1,
    "circle": null,
    "archAttunement": false,
    "entryBuffer": 20,
    "specials": {}
  },
  "druid.base.hawk-form-scout": {
    "sourceId": "druid.base.hawk-form-scout",
    "sourceSha256": "4534b24051e4e8540c7c4138f95d729e014a25be5cc554e72e25d10c0c9653b8",
    "sourceProcedure": {
      "id": "druid.base.hawk-form-scout",
      "name": "Hawk Form (Scout)",
      "className": "Druid",
      "band": "Base",
      "path": null,
      "sourceKind": "form",
      "minimumClassLevel": 1,
      "acquisition": "automatic",
      "activation": "Action attack; passive form traits",
      "cost": "One shift",
      "rangeAndTarget": "Self; talon 5 ft",
      "duration": "While in Hawk",
      "frequency": "One talon/Action",
      "effect": "Tiny, flight 60 ft, walking 10 ft, advantage on sight Perception. Talon 1d4 slashing+WIS; advantage if you descended at least 10 ft immediately before attack. No carrying Medium allies or casting spells before 18.",
      "spellRank": null
    },
    "minimumLevel": 1,
    "circle": null,
    "archAttunement": false,
    "entryBuffer": 0,
    "specials": {}
  },
  "druid.base.boar-form-brawler": {
    "sourceId": "druid.base.boar-form-brawler",
    "sourceSha256": "d1288f0ae961f47cdaf529e43a8f37b48873aa800032377dc8506c26c58710ec",
    "sourceProcedure": {
      "id": "druid.base.boar-form-brawler",
      "name": "Boar Form (Brawler)",
      "className": "Druid",
      "band": "Base",
      "path": null,
      "sourceKind": "form",
      "minimumClassLevel": 1,
      "acquisition": "automatic",
      "activation": "Action attack; passive form traits",
      "cost": "One shift",
      "rangeAndTarget": "Self; tusk 5 ft",
      "duration": "While in Boar",
      "frequency": "One tusk/Action",
      "effect": "Resistance to slashing. Tusk 1d6 piercing+WIS. After moving 10 ft directly toward target, first hit/turn adds 1d6 and STR save or push 5 ft; no repeated charges from forced movement.",
      "spellRank": null
    },
    "minimumLevel": 1,
    "circle": null,
    "archAttunement": false,
    "entryBuffer": 0,
    "specials": {}
  },
  "druid.base.panther-form-stealth": {
    "sourceId": "druid.base.panther-form-stealth",
    "sourceSha256": "8daa235b54a30f029be0ab4ec9285f0787742efb78cd905b848ebcb572158396",
    "sourceProcedure": {
      "id": "druid.base.panther-form-stealth",
      "name": "Panther Form (Stealth)",
      "className": "Druid",
      "band": "Base",
      "path": null,
      "sourceKind": "form",
      "minimumClassLevel": 1,
      "acquisition": "automatic",
      "activation": "Action attack; passive form traits",
      "cost": "One shift",
      "rangeAndTarget": "Self; claw 5 ft",
      "duration": "While in Panther",
      "frequency": "One claw/Action",
      "effect": "Speed 40 ft, darkvision 60 ft, +4 Stealth. Claw 2d4 slashing+WIS; after 20 ft straight approach hit, STR save or Grappled. Escape Action against Druid DC; ends on separation/reversion. Only one held target, no free Restrained.",
      "spellRank": null
    },
    "minimumLevel": 1,
    "circle": null,
    "archAttunement": false,
    "entryBuffer": 0,
    "specials": {}
  },
  "druid.arch.dire-wolf": {
    "sourceId": "druid.arch.dire-wolf",
    "sourceSha256": "b384946f0b86e1ad7b0b45561e0b50f3468f65d7bc8c4e90ff363194486b7987",
    "sourceProcedure": {
      "id": "druid.arch.dire-wolf",
      "name": "Dire Wolf",
      "className": "Druid",
      "band": "Arch",
      "path": null,
      "sourceKind": "form",
      "minimumClassLevel": 11,
      "acquisition": "automatic",
      "activation": "Action attack or Howl",
      "cost": "One shift; Howl 1 Form Surge",
      "rangeAndTarget": "Self; bite 5 ft; Howl 30 ft",
      "duration": "Form 10 minutes; fear up to 3 rounds",
      "frequency": "Howl 1/shift and finite reserve",
      "effect": "Arch attunement required. Speed 40 ft, bite 2d6 piercing+WIS; advantage when active ally threatens target 5 ft. Howl Action up to 3 enemies WIS save or Frightened, repeat end each turn, maximum 3 rounds. No free bite with Howl.",
      "spellRank": null
    },
    "minimumLevel": 11,
    "circle": null,
    "archAttunement": true,
    "entryBuffer": 0,
    "specials": {
      "howl": {
        "action": "action",
        "payment": "surge"
      }
    }
  },
  "druid.arch.earth-warden-dire-bear": {
    "sourceId": "druid.arch.earth-warden-dire-bear",
    "sourceSha256": "8ceb2cb1ea880743953a06d50a1c0e098eba154298b3755a7efa689556e18af6",
    "sourceProcedure": {
      "id": "druid.arch.earth-warden-dire-bear",
      "name": "Earth Warden (Dire Bear)",
      "className": "Druid",
      "band": "Arch",
      "path": null,
      "sourceKind": "form",
      "minimumClassLevel": 11,
      "acquisition": "automatic",
      "activation": "Action Slam",
      "cost": "One shift; buffer reserve",
      "rangeAndTarget": "Self; 10 ft radius up to 3 creatures",
      "duration": "While in Earth Warden",
      "frequency": "Slam recharge 2",
      "effect": "Arch attunement required. Gain up to 30 temp HP from reserve, nonmagical physical resistance. Slam DEX save 2d6 bludgeoning+WIS and Prone on failure, half damage no Prone success. Ordinary claw 1d8+WIS when Slam unavailable.",
      "spellRank": null
    },
    "minimumLevel": 11,
    "circle": null,
    "archAttunement": true,
    "entryBuffer": 30,
    "specials": {
      "slam": {
        "action": "action",
        "payment": "recharge2"
      }
    }
  },
  "druid.arch.sky-serpent": {
    "sourceId": "druid.arch.sky-serpent",
    "sourceSha256": "fb02c57b9530f327172b8a1c001f8528f4a4086e4659d954e713c7946468c708",
    "sourceProcedure": {
      "id": "druid.arch.sky-serpent",
      "name": "Sky Serpent",
      "className": "Druid",
      "band": "Arch",
      "path": null,
      "sourceKind": "form",
      "minimumClassLevel": 11,
      "acquisition": "automatic",
      "activation": "Action bite; passive traits",
      "cost": "One shift",
      "rangeAndTarget": "Self; bite 5 ft",
      "duration": "While in Sky Serpent",
      "frequency": "One bite/Action",
      "effect": "Arch attunement required. Flight 80 ft with hover, +2 DEX saves. Bite 2d8 lightning+WIS. Once/shift may spend 1 Form Surge to add 1d4 against wet target; no repeated electrical propagation.",
      "spellRank": null
    },
    "minimumLevel": 11,
    "circle": null,
    "archAttunement": true,
    "entryBuffer": 0,
    "specials": {
      "wet": {
        "action": null,
        "payment": "surge"
      }
    }
  },
  "druid.arch.ironhorn-ram": {
    "sourceId": "druid.arch.ironhorn-ram",
    "sourceSha256": "08721f755db519afdb198be9a11f8df1b8e2062022c4b2ed7428f552af5d2b9d",
    "sourceProcedure": {
      "id": "druid.arch.ironhorn-ram",
      "name": "Ironhorn Ram",
      "className": "Druid",
      "band": "Arch",
      "path": null,
      "sourceKind": "form",
      "minimumClassLevel": 11,
      "acquisition": "automatic",
      "activation": "Action ram; passive traits",
      "cost": "One shift",
      "rangeAndTarget": "Self; ram 5 ft",
      "duration": "While in Ironhorn Ram",
      "frequency": "One ram/Action",
      "effect": "Arch attunement required. AC max(normal, 17), immune Prone. Ram 1d8+WIS bludgeoning; after 20 ft straight approach first hit/turn adds 3d6, STR against Druid DC or push 10 ft. No bonus against same target more than once/round.",
      "spellRank": null
    },
    "minimumLevel": 11,
    "circle": null,
    "archAttunement": true,
    "entryBuffer": 0,
    "specials": {}
  },
  "druid.arch.shadow-lynx": {
    "sourceId": "druid.arch.shadow-lynx",
    "sourceSha256": "a0a1750c467c1afc4289e067406f9488b165c86971105261790ad671c238de64",
    "sourceProcedure": {
      "id": "druid.arch.shadow-lynx",
      "name": "Shadow Lynx",
      "className": "Druid",
      "band": "Arch",
      "path": null,
      "sourceKind": "form",
      "minimumClassLevel": 11,
      "acquisition": "automatic",
      "activation": "Reaction Blink; Action claw",
      "cost": "One shift; Blink 1 Form Surge",
      "rangeAndTarget": "Self; claw 5 ft",
      "duration": "Blink instant; form 10 minutes",
      "frequency": "Blink 1/shift and finite reserve",
      "effect": "Arch attunement required. Claw 2d4+WIS magical slashing; +2 Stealth while motionless. When attack would hit, Reaction teleport 30 ft to visible empty space, causing triggering attack to miss if you leave its reach/range. Next claw before end next turn advantage. No blanket immunity to magical damage.",
      "spellRank": null
    },
    "minimumLevel": 11,
    "circle": null,
    "archAttunement": true,
    "entryBuffer": 0,
    "specials": {
      "blink": {
        "action": "reaction",
        "payment": "surge"
      }
    }
  },
  "druid.hero.land.blight-elk": {
    "sourceId": "druid.hero.land.blight-elk",
    "sourceSha256": "359c36eac3bfd49ee16f5a309642ef6aec0c3f0486f37991c610895c861231fe",
    "sourceProcedure": {
      "id": "druid.hero.land.blight-elk",
      "name": "Blight Elk",
      "className": "Druid",
      "band": "Hero",
      "path": "Land",
      "sourceKind": "form",
      "minimumClassLevel": 10,
      "acquisition": "automatic",
      "activation": "Action antlers; passive aura",
      "cost": "One shift",
      "rangeAndTarget": "Land Hero; 5 ft aura",
      "duration": "While in Blight Elk",
      "frequency": "Aura once/enemy/round, max 3 enemies",
      "effect": "Antlers 2d8+WIS piercing. Enemy starting within 5 ft CON save or 1d4 poison. Wither unattended mundane vegetation within 5 ft cosmetically; tainted water is visibly foul and harmless after 10 minutes. No mass contamination or permanent resource fabrication.",
      "spellRank": null
    },
    "minimumLevel": 10,
    "circle": "Land",
    "archAttunement": false,
    "entryBuffer": 0,
    "specials": {}
  },
  "druid.hero.land.tanglemaw": {
    "sourceId": "druid.hero.land.tanglemaw",
    "sourceSha256": "b916c4ba9ccc394e5cf2eb6cbc02344c0e211daec1698938f6d2403aaab415ab",
    "sourceProcedure": {
      "id": "druid.hero.land.tanglemaw",
      "name": "Tanglemaw",
      "className": "Druid",
      "band": "Hero",
      "path": "Land",
      "sourceKind": "form",
      "minimumClassLevel": 10,
      "acquisition": "automatic",
      "activation": "Action bite; passive traits",
      "cost": "One shift",
      "rangeAndTarget": "Land Hero; bite 5 ft; sense 30 ft",
      "duration": "While in Tanglemaw",
      "frequency": "Retaliation once/round",
      "effect": "Bite 2d6+WIS piercing, STR save or Restrained until end next turn, escape Action against DC. Thorny Body deals 1d4 piercing to one melee attacker after hit; no reflections. Sense ground-contact locations 30 ft on same connected surface, not identities through stone walls.",
      "spellRank": null
    },
    "minimumLevel": 10,
    "circle": "Land",
    "archAttunement": false,
    "entryBuffer": 0,
    "specials": {}
  },
  "druid.hero.moon.beastlord-alpha-animal-hybrid": {
    "sourceId": "druid.hero.moon.beastlord-alpha-animal-hybrid",
    "sourceSha256": "0c08e78f8f2d4d467d2ef31331896514dc61775ed3397fa5357eba633d87fb5a",
    "sourceProcedure": {
      "id": "druid.hero.moon.beastlord-alpha-animal-hybrid",
      "name": "Beastlord (Alpha Animal Hybrid)",
      "className": "Druid",
      "band": "Hero",
      "path": "Moon",
      "sourceKind": "form",
      "minimumClassLevel": 10,
      "acquisition": "automatic",
      "activation": "Action bite or Howl",
      "cost": "One shift; Howl 1 Form Surge",
      "rangeAndTarget": "Moon Hero; bite 5 ft/Howl 15 ft",
      "duration": "While in Beastlord; fear 1 turn",
      "frequency": "Howl 1/shift and finite reserve",
      "effect": "Bite 2d6+WIS piercing; first hit/turn adds 1d4 of one chosen fire/cold/lightning, not all three. Up to 2 beast allies 30 ft gain+1 first attack/turn. Howl Action up to 3 enemies WIS save or Frightened until end next turn.",
      "spellRank": null
    },
    "minimumLevel": 10,
    "circle": "Moon",
    "archAttunement": false,
    "entryBuffer": 0,
    "specials": {
      "howl": {
        "action": "action",
        "payment": "surge"
      }
    }
  },
  "druid.hero.moon.mooncursed": {
    "sourceId": "druid.hero.moon.mooncursed",
    "sourceSha256": "ce968a8db6c8ebac99dc9d8d7ef4f99c949e173df8eed26e5dd75a8175bd3054",
    "sourceProcedure": {
      "id": "druid.hero.moon.mooncursed",
      "name": "Mooncursed",
      "className": "Druid",
      "band": "Hero",
      "path": "Moon",
      "sourceKind": "form",
      "minimumClassLevel": 10,
      "acquisition": "automatic",
      "activation": "Action bite or Howl",
      "cost": "One shift; Howl 1 Form Surge",
      "rangeAndTarget": "Moon Hero; bite 5 ft/Howl 30 ft",
      "duration": "While in Mooncursed",
      "frequency": "Howl 1/shift and finite reserve",
      "effect": "Resistance to nonmagical physical damage except silver; other types unchanged. Bite 2d6+WIS piercing, +1d8 once/turn under real full moon. Howl Action choose up to 3 allies gain 2d8 temp HP total roll, or 3 enemies WIS save or Frightened through end next turn. Temp HP draws from Buffer Reserve per recipient.",
      "spellRank": null
    },
    "minimumLevel": 10,
    "circle": "Moon",
    "archAttunement": false,
    "entryBuffer": 0,
    "specials": {
      "howl": {
        "action": "action",
        "payment": "surge"
      }
    }
  },
  "druid.hero.moon.elemental-shapeshifting": {
    "sourceId": "druid.hero.moon.elemental-shapeshifting",
    "sourceSha256": "1d9ad7f20980737543dc037fc1318a7462e3995e17afec48de94312ac3f5c0b7",
    "sourceProcedure": {
      "id": "druid.hero.moon.elemental-shapeshifting",
      "name": "Elemental Shapeshifting",
      "className": "Druid",
      "band": "Hero",
      "path": "Moon",
      "sourceKind": "form",
      "minimumClassLevel": 14,
      "acquisition": "automatic",
      "activation": "Bonus Action",
      "cost": "One shift and one elemental use",
      "rangeAndTarget": "Moon Circle self",
      "duration": "10 minutes",
      "frequency": "2/long rest",
      "effect": "Choose bounded elemental form: AC 16, natural attack 2d8+WIS chosen element, one/Action. Air flight 60 lightning resistance; Earth burrow 20 through loose soil physical DR 2; Fire fire resistance and melee attacker 1d4 fire once/round; Water swim 60 water breathing cold resistance. Retain own HP/abilities, no external stat blocks.",
      "spellRank": null
    },
    "minimumLevel": 14,
    "circle": "Moon",
    "archAttunement": false,
    "entryBuffer": 0,
    "specials": {}
  },
  "druid.hero.storm.tempest-raptor": {
    "sourceId": "druid.hero.storm.tempest-raptor",
    "sourceSha256": "0f6b5667a0e9f772174a0e56e8b9f4ef174fd16d47d2bb7a6fe6ff148f8683ad",
    "sourceProcedure": {
      "id": "druid.hero.storm.tempest-raptor",
      "name": "Tempest Raptor",
      "className": "Druid",
      "band": "Hero",
      "path": "Storm",
      "sourceKind": "form",
      "minimumClassLevel": 10,
      "acquisition": "automatic",
      "activation": "Action claw; passive traits",
      "cost": "One shift",
      "rangeAndTarget": "Storm Hero; claw 5 ft",
      "duration": "While in Tempest Raptor",
      "frequency": "One claw/Action; retaliation once/round",
      "effect": "Flight 60 ft, advantage on saves against wind/lightning while airborne. Claw 2d6+WIS lightning; wet target adds 1d4 once/shift for 1 Form Surge. After melee hit on you, attacker takes 1d6 lightning once/round; no repeated disarm chains.",
      "spellRank": null
    },
    "minimumLevel": 10,
    "circle": "Storm",
    "archAttunement": false,
    "entryBuffer": 0,
    "specials": {
      "wet": {
        "action": null,
        "payment": "surge"
      }
    }
  },
  "druid.hero.storm.thunderhorn-stag": {
    "sourceId": "druid.hero.storm.thunderhorn-stag",
    "sourceSha256": "80904406e241853bf23018ba3194ea3b49941321ceaf05b417ce9cca3be8526a",
    "sourceProcedure": {
      "id": "druid.hero.storm.thunderhorn-stag",
      "name": "Thunderhorn Stag",
      "className": "Druid",
      "band": "Hero",
      "path": "Storm",
      "sourceKind": "form",
      "minimumClassLevel": 10,
      "acquisition": "automatic",
      "activation": "Action antlers or Thunder Step",
      "cost": "One shift; Step 1 Form Surge",
      "rangeAndTarget": "Storm Hero; antlers 5 ft; teleport 30 ft",
      "duration": "While in Thunderhorn Stag",
      "frequency": "Step 1/shift and finite reserve",
      "effect": "Antlers 1d8+WIS piercing; after 20 ft approach first hit/turn also 2d8 thunder and CON save or Deafened through end next turn. Step Action teleport 30 ft, departure 10 ft radius up to 3 creatures CON save 2d8 thunder, half success. Sense natural storm approach 24 hours, no exact prediction of magical weather.",
      "spellRank": null
    },
    "minimumLevel": 10,
    "circle": "Storm",
    "archAttunement": false,
    "entryBuffer": 0,
    "specials": {
      "step": {
        "action": "action",
        "payment": "surge"
      }
    }
  },
  "druid.hero.thorns.blight-elk": {
    "sourceId": "druid.hero.thorns.blight-elk",
    "sourceSha256": "f9db8ef944e9bfe024c3fb740c2efb6f4240b0938b1db4e098f4ce540e2e22dc",
    "sourceProcedure": {
      "id": "druid.hero.thorns.blight-elk",
      "name": "Blight Elk",
      "className": "Druid",
      "band": "Hero",
      "path": "Thorns",
      "sourceKind": "form",
      "minimumClassLevel": 10,
      "acquisition": "automatic",
      "activation": "Action antlers; passive aura",
      "cost": "One shift",
      "rangeAndTarget": "Thorns Hero; 5 ft aura",
      "duration": "While in Blight Elk",
      "frequency": "Aura once/enemy/round, max 3 enemies",
      "effect": "Antlers 2d8+WIS piercing, +1d4 poison once/turn against Poisoned. Enemies starting 5 ft CON save or 1d4 poison. Ground 10 ft around you is difficult terrain for enemies, no lasting thorns after movement/reversion.",
      "spellRank": null
    },
    "minimumLevel": 10,
    "circle": "Thorns",
    "archAttunement": false,
    "entryBuffer": 0,
    "specials": {}
  },
  "druid.hero.thorns.tanglemaw": {
    "sourceId": "druid.hero.thorns.tanglemaw",
    "sourceSha256": "daff5c2781baba250c2131a002539a6f80d7a7a2884ebaaed94b81d541d90e08",
    "sourceProcedure": {
      "id": "druid.hero.thorns.tanglemaw",
      "name": "Tanglemaw",
      "className": "Druid",
      "band": "Hero",
      "path": "Thorns",
      "sourceKind": "form",
      "minimumClassLevel": 10,
      "acquisition": "automatic",
      "activation": "Action bite; passive traits",
      "cost": "One shift",
      "rangeAndTarget": "Thorns Hero; bite 5 ft; sense 30 ft",
      "duration": "While in Tanglemaw",
      "frequency": "Retaliation once/round",
      "effect": "Bite 2d6+WIS piercing, STR save or Restrained through end next turn, Action escape DC. One melee attacker/round takes 1d4 piercing; one creature restrained by your bite takes 1d4 at start turn. Ground sense 30 ft same surface and advantage against Prone; no wall-penetrating identification.",
      "spellRank": null
    },
    "minimumLevel": 10,
    "circle": "Thorns",
    "archAttunement": false,
    "entryBuffer": 0,
    "specials": {}
  },
  "druid.hero.winterfang.snow-leopard": {
    "sourceId": "druid.hero.winterfang.snow-leopard",
    "sourceSha256": "45a815d53f107787811abec352814026ffae437e83a0891e5bf3a8f21f262755",
    "sourceProcedure": {
      "id": "druid.hero.winterfang.snow-leopard",
      "name": "Snow Leopard",
      "className": "Druid",
      "band": "Hero",
      "path": "Winterfang",
      "sourceKind": "form",
      "minimumClassLevel": 10,
      "acquisition": "automatic",
      "activation": "Action claw; passive traits",
      "cost": "One shift",
      "rangeAndTarget": "Winterfang Hero; claw 5 ft",
      "duration": "While in Snow Leopard",
      "frequency": "One claw/Action",
      "effect": "Claw 2d6+WIS cold, +1d4 once/turn against slowed foe. +5 Stealth on ice/snow and advantage on legal Hide there; source+10 reduced provisionally. Ignore ordinary ice/snow movement penalties, not magical restraining ice.",
      "spellRank": null
    },
    "minimumLevel": 10,
    "circle": "Winterfang",
    "archAttunement": false,
    "entryBuffer": 0,
    "specials": {}
  },
  "druid.hero.winterfang.frost-wyrmling": {
    "sourceId": "druid.hero.winterfang.frost-wyrmling",
    "sourceSha256": "be5a32836802126e195e59a8de64ea3c1e7ec3d8926ca051284bf326d39f526f",
    "sourceProcedure": {
      "id": "druid.hero.winterfang.frost-wyrmling",
      "name": "Frost Wyrmling",
      "className": "Druid",
      "band": "Hero",
      "path": "Winterfang",
      "sourceKind": "form",
      "minimumClassLevel": 10,
      "acquisition": "automatic",
      "activation": "Action breath or claw",
      "cost": "One shift; breath one short-rest use",
      "rangeAndTarget": "Winterfang Hero; 30 ft cone up to 3 creatures",
      "duration": "While in Frost Wyrmling",
      "frequency": "Breath 1/short rest, shared across shifts",
      "effect": "AC normal+2, cold immunity. Claw 1d8+WIS cold. Breath 4d6 cold DEX half. One breath target may have cold resistance ignored once/shift for 1 Form Surge; immunity remains. No general physical resistance from cold terrain in this draft.",
      "spellRank": null
    },
    "minimumLevel": 10,
    "circle": "Winterfang",
    "archAttunement": false,
    "entryBuffer": 0,
    "specials": {
      "breath": {
        "action": "action",
        "payment": "short-rest"
      },
      "ignore-cold-resistance": {
        "action": null,
        "payment": "surge"
      }
    }
  },
  "druid.hero.rotshaper.carrion-rat-king": {
    "sourceId": "druid.hero.rotshaper.carrion-rat-king",
    "sourceSha256": "66cae86b4ff384703f2aef8cc07dfd610085034b0922e02a461f86e74f20cc66",
    "sourceProcedure": {
      "id": "druid.hero.rotshaper.carrion-rat-king",
      "name": "Carrion Rat King",
      "className": "Druid",
      "band": "Hero",
      "path": "Rotshaper",
      "sourceKind": "form",
      "minimumClassLevel": 10,
      "acquisition": "automatic",
      "activation": "Action bite or summon",
      "cost": "One shift; summon 1 Form Surge",
      "rangeAndTarget": "Rotshaper Hero; bite 5 ft/swarm 30 ft",
      "duration": "While in Carrion Rat King",
      "frequency": "Summon 1/shift and finite reserve",
      "effect": "Bite 1d8+WIS piercing+2d6 poison; CON save or Poisoned through end next turn. Immune disease/Poisoned, not poison damage. Summon Action creates one bounded engine swarm 1 minute, same command budget; replaces previous form swarm.",
      "spellRank": null
    },
    "minimumLevel": 10,
    "circle": "Rotshaper",
    "archAttunement": false,
    "entryBuffer": 0,
    "specials": {
      "summon": {
        "action": "action",
        "payment": "surge"
      }
    }
  },
  "druid.hero.rotshaper.insect-broodmother": {
    "sourceId": "druid.hero.rotshaper.insect-broodmother",
    "sourceSha256": "52edbedf9bfbdf8057259f3758ebfd144820c93a27c2170fd34e4d6f70297d82",
    "sourceProcedure": {
      "id": "druid.hero.rotshaper.insect-broodmother",
      "name": "Insect Broodmother",
      "className": "Druid",
      "band": "Hero",
      "path": "Rotshaper",
      "sourceKind": "form",
      "minimumClassLevel": 10,
      "acquisition": "automatic",
      "activation": "Action bite; passive traits",
      "cost": "One shift; spawning 1 Form Surge",
      "rangeAndTarget": "Rotshaper Hero; up to 2 swarms adjacent",
      "duration": "While in Insect Broodmother",
      "frequency": "Spawn once/shift and finite reserve",
      "effect": "AC normal+3, climb 30 walls/ceilings, bite 1d8+WIS piercing. On entry optional spend surge spawn 2 bounded shared profile swarms, both end with form, combined one commanded attack/turn. Once/shift for another Form Surge turn one crit against you into normal hit; no infinite insects.",
      "spellRank": null
    },
    "minimumLevel": 10,
    "circle": "Rotshaper",
    "archAttunement": false,
    "entryBuffer": 0,
    "specials": {
      "spawn": {
        "action": null,
        "payment": "surge"
      },
      "negate-critical": {
        "action": null,
        "payment": "surge"
      }
    }
  },
  "druid.hero.rotshaper.master-of-vermin": {
    "sourceId": "druid.hero.rotshaper.master-of-vermin",
    "sourceSha256": "762dc5ac770d66998e89219fad3ca15abc6f5bb3755316d4bb388d76682283b5",
    "sourceProcedure": {
      "id": "druid.hero.rotshaper.master-of-vermin",
      "name": "Master of Vermin",
      "className": "Druid",
      "band": "Hero",
      "path": "Rotshaper",
      "sourceKind": "form",
      "minimumClassLevel": 14,
      "acquisition": "automatic",
      "activation": "Bonus Action",
      "cost": "One shift",
      "rangeAndTarget": "Rotshaper Circle self",
      "duration": "10 minutes",
      "frequency": "Normal shift limit",
      "effect": "Swarm form: own HP/AC, physical resistance, Speed 30, fit Tinygaps, natural attack S d6+WIS piercing. No flight unless choosing bats (flight 30), which forfeits physical resistance. Replacing a summoning spell's beast with swarm uses same single companion budget and paid spell, never multiplied dice/creatures.",
      "spellRank": null
    },
    "minimumLevel": 14,
    "circle": "Rotshaper",
    "archAttunement": false,
    "entryBuffer": 0,
    "specials": {}
  },
  "druid.hero.ashen-grove.charbear": {
    "sourceId": "druid.hero.ashen-grove.charbear",
    "sourceSha256": "aea389ba9868189c5ee1db218d3623978ad55bab07d432188912cba18493e50d",
    "sourceProcedure": {
      "id": "druid.hero.ashen-grove.charbear",
      "name": "Charbear",
      "className": "Druid",
      "band": "Hero",
      "path": "Ashen Grove",
      "sourceKind": "form",
      "minimumClassLevel": 10,
      "acquisition": "automatic",
      "activation": "Action claw or Smoke",
      "cost": "One shift; Smoke 1 Form Surge",
      "rangeAndTarget": "Ashen Hero; claw 5 ft/aura 5 ft/smoke 10 ft",
      "duration": "While in Charbear; smoke 3 rounds",
      "frequency": "Smoke 1/shift; aura/retaliation caps",
      "effect": "Claw 2d8+WIS fire; first hit/turn Burn 1d4 next turn. Up to 3 enemies starting 5 ft CON save or 1d6 fire. Smoke Action opaque 10 ft radius sphere centered fixed point you occupy, concentration 3 rounds; all vision blocked, no poison in this draft. Wind 20 mph disperses.",
      "spellRank": null
    },
    "minimumLevel": 10,
    "circle": "Ashen Grove",
    "archAttunement": false,
    "entryBuffer": 0,
    "specials": {
      "smoke": {
        "action": "action",
        "payment": "surge"
      }
    }
  },
  "druid.hero.ashen-grove.blazewood-stag": {
    "sourceId": "druid.hero.ashen-grove.blazewood-stag",
    "sourceSha256": "17a078d0e7095877419b9b0626f73d0c24c578be8a18c568ce2b1f89695ed07f",
    "sourceProcedure": {
      "id": "druid.hero.ashen-grove.blazewood-stag",
      "name": "Blazewood Stag",
      "className": "Druid",
      "band": "Hero",
      "path": "Ashen Grove",
      "sourceKind": "form",
      "minimumClassLevel": 10,
      "acquisition": "automatic",
      "activation": "Action antlers or Conflagration",
      "cost": "One shift; blast one long-rest use",
      "rangeAndTarget": "Ashen Hero; antlers 5 ft/blast 10 ft",
      "duration": "While in Blazewood Stag",
      "frequency": "Blast 1/long rest across shifts",
      "effect": "Antlers 1d8+WIS piercing; 20 ft charge adds 2d6 fire once/turn. Leave up to 3 fire tiles/turn, last until start next turn, DEX save or 1d8 fire once/creature/round. Blast Action 6d6 fire DEX half up to 3 creatures 10 ft, not free on reversion.",
      "spellRank": null
    },
    "minimumLevel": 10,
    "circle": "Ashen Grove",
    "archAttunement": false,
    "entryBuffer": 0,
    "specials": {
      "blast": {
        "action": "action",
        "payment": "long-rest"
      }
    }
  }
}
```

## Existing twelve decisions (actual notebook reply)

# GPT completed twelve Time Loop boundary decisions

ChatGPT said:

The attachment resolves several ambiguities from the first Time Loop conference. The largest correction is that logical combat time can rewind without rewinding elapsed world time. That means some encounter permissions receive fresh iteration-qualified turn/round identities, while explicit elapsed-time records such as Soul Bind, Agony, the promoted transformation spells, and persistent resource ledgers keep their real deadlines/history. The original Boon V still promises an encounter reset and ally memory, while the reviewed card explicitly conserves per-rest resources, consumables, loot ownership, and its own use. 
Pasted text

Reward opportunity identity — conserve the opportunity, not the death event. Use a permanent key such as RewardOpportunityKey(encounterOriginId, immutableRewardSourceId, opportunityKind, opportunitySlotId). immutableRewardSourceId is normally the original participant/body/environment anchor that owns the reward opportunity; opportunityKind distinguishes XP, treasure, harvest, quest-credit, etc.; opportunitySlotId distinguishes multiple genuinely separate source-authorized rewards from the same entity, such as independently defined harvest slots. Claim state is conserved across every Time Loop iteration. Killing the same snapshot foe again with a fresh deathEventId therefore creates a new combat event but not a new XP/treasure/harvest entitlement. If the first discarded timeline already claimed the opportunity, the re-kill yields no second claim. A genuinely independent reward requires a genuinely different immutable source/opportunity authorized by its source, not merely a new iteration, event ID, corpse, transformation, or regenerated body. Post-snapshot generated summons/created farming bodies remain subject to the existing no-farm rules and do not acquire a reward opportunity merely because they exist. This is a NEW conservation bridge required by the source's “no duplicate XP, treasure or consumables” promise. 
Pasted text

Restored one-shot effects — preserve root identity and historical audit, but give each timeline its own consumption view. Canonical effectId never changes. Historical eventIds and historical consumption records are never deleted. Add a separate TemporalConsumptionKey = (effectId, timelineIterationId) or equivalent temporal generation. At snapshot, record whether the one-shot permission/rider was available or already consumed. On rewind into a new iteration:

snapshot-unconsumed → same effectId, available in the new iteration view;
snapshot-consumed → same effectId, still consumed;
consumption that occurred only in a discarded later iteration remains in audit history but does not mark the restored snapshot view consumed.

This applies to Agony's next-heal reducer, linked buffer riders, marks, form riders and equivalent one-shot state. It is privileged temporal restoration: no new offer, cast, entry trigger, source cost, or new effect ID occurs. Any finite cost needed to use the restored permission must still be paid from the current conserved resource state.

HealingCommitLedger.committed_event_ids stays globally historical. consumed_reducer_ids cannot remain the sole source of present availability when Time Loop is active; either the ledger must accept a composite temporal consumption token or TemporalWorld must supply an iteration-qualified application token while separately retaining the canonical effectId. Blindly deleting old consumption is wrong, and blindly carrying it forward is also wrong. 
Pasted text
 The same principle applies to generic one-shot state holders already present in the control/healing modules. 
Pasted text

Reaction debt — preserve every outstanding Time Loop Reaction debt, not merely the newest Oracle's. Maintain TimeLoopReactionDebt[oracleId]. Committing Time Loop creates that Oracle's debt. A later Time Loop restores snapshot Action/Reaction budgets and then overlays all debts still outstanding. Oracle A therefore remains unable to use another Reaction if Oracle B loops before A reaches the canonical Reaction refresh. A debt clears only when that Oracle experiences the same real scheduler event that ordinarily refreshes their Reaction — for this interface, the owner's next actual normal regular-start Reaction refresh. A debt already legitimately cleared before a later loop remains cleared; Time Loop does not resurrect old debt. Extra Actions do not clear it, and the rewind itself does not clear it. This is a NEW overlay required to keep the 1/LR Reaction expenditure conserved while still rewinding encounter action state. 
Pasted text

Logical turns versus world time — fresh iteration-qualified combat windows, conserved elapsed-time clocks. Introduce:

IterationRoundId = (encounterId, iterationId, roundNumber)
IterationTurnId = (encounterId, iterationId, actorId, turnOrdinal/type)
a separate monotonic global/world regular-marker sequence for actual clock systems.

The new iteration's round 1 is immediately playable after atomic restoration; the engine does not wait six world seconds before anyone can act, and the rewind itself triggers no start-of-turn/periodic tick.

Encounter-logical once-per-turn/round rules receive fresh identities in the new iteration:

Necrotic Affinity's once-per-turn melee die can qualify on a genuine new iteration turn;
Empowered Summoning's first rolled damage in round 1 can qualify under the new IterationRoundId;
command/offense budgets restart from their snapshot encounter state;
Lifeleech may qualify again for an ongoing spell root that actually existed at snapshot because the new round-window ID is different, but its finite Recovery Reserve remains spent/current.

Old events remain historical and cannot be replayed for rewards/resources.

Important correction to my first Time Loop draft: continuous recharge clocks are not automatically “per-encounter uses.” The reviewed Druid OwnerRechargeClock spans initiative and downtime and must remain conserved. Its ticks, phase and due marker are not reset merely because encounter labels restart. The first post-loop regular turn is a new logical turn, but the Druid recharge clock receives the next real scheduler marker and may tick only under its already-reviewed clock rules; Time Loop creates no free recharge tick at the rewind instant. The frozen class rules distinguish regular-turn Recharge from encounter declarations and six-second outside-combat ticking. 
Pasted text
 
Pasted text

Per-source clock policy — use the following explicit table, not duration-length inference.

Source/state	Temporal policy
Pending living Soul Bind, 60s	WORLD_ABSOLUTE. Preserve original expiry; never rebase. If already expired at rewind, it does not become pending again.
Bound-dead Soul Bind, 24h	WORLD_ABSOLUTE, death-instance bound. If the associated post-snapshot death is undone, that later bound record becomes historical/inactive. A bound record already present at snapshot keeps its original expiry.
Necrotic Affinity death seal, 24h	WORLD_ABSOLUTE, exact death-instance. Undoing that post-snapshot death closes the seal's active applicability; dead-at-snapshot seals keep original expiry.
Agony healing suppression, 60s	WORLD_ABSOLUTE + snapshot one-shot state. If snapshot-unconsumed and still before original expiry, it may be available in the new temporal consumption view. If expired, it does not return.
Chef potent food, 24h or owner's next LR	WORLD_ABSOLUTE AND REST_EPOCH. Physical food/inventory is conserved. Consumed/discarded food never returns.
Chef/Inspiring recipient-family entitlement	CONSERVED REST_EPOCH HISTORY. Never rewound. An offer already received in the same real LR epoch remains spent across loops.
Blood Ritual self default-LR shield	SNAPSHOT THP + REST_EPOCH. Restore snapshot amount only if the original grant remains valid in the current real recipient epoch. No new grant/ritual occurs.
Blood Ritual curse/disease rider	SNAPSHOT ONE-SHOT + REST_EPOCH. Consumption can rewind to snapshot state via temporal generation, but the real LR epoch never rewinds.
Blood Ritual ally 1h shield	SNAPSHOT THP + WORLD_ABSOLUTE. Restore remaining snapshot THP only while the original one-hour endpoint is still in the future.
Field Medic default-LR shield	SNAPSHOT THP + REST_EPOCH.
Empowered Summoning creation shield	SNAPSHOT THP + REST_EPOCH + ENTITY DEPENDENCY. Same summon lineage only; no new creation event.
Soul Cage 2d8 shield	SNAPSHOT THP + REST_EPOCH. Charges remain conserved/spent.
Core Stable d4-hour recovery	WORLD_ABSOLUTE. Never schedule the same recovery event twice. If its deadline already resolved in discarded history, restoring Stable/HP state cannot retrigger that resolved recovery.
Druid form duration	WORLD_ABSOLUTE source duration, not reset merely because combat rewinds. Restore the same form instance only if its actual source endpoint is still valid. Dependent form effects cannot outlive an invalid form.
Polymorph/Mass/Shapechange	WORLD_ABSOLUTE 60-second endpoint, as already promoted. Do not rebase.
True Polymorph shaping	WORLD_ABSOLUTE stabilization checkpoint. A record that has legitimately passed its checkpoint cannot be de-stabilized by Time Loop.
Permanent True Polymorph	PERMANENT record, subject to current external suppression/identity reconciliation.
Per-rest/daily/weekly resets	CONSERVED REST/WORLD EPOCH. Never rewound.
Explicit “next regular turn” effects	ITERATION_LOGICAL marker policy when that exact source is reviewed as turn-relative, not because it happens to be ~6 seconds.

If a WORLD_ABSOLUTE record's deadline already resolved, Time Loop may restore surrounding participant state but must not replay that world event. Historical resolution identity stays conserved. If restoring the containing state would require the expired event to fire again to become legal, the source adapter must supply a specific reconciliation; otherwise snapshot preflight fails. This is especially important for Stable recovery and similar delayed resolutions. Soul Bind already has explicit finite pending/bound states rather than an encounter-relative clock. 
Pasted text
 The promoted transformation package likewise uses absolute 60-second checkpoints and conserved underlying identity. 
Pasted text

Maximum HP/current inventory — snapshot HP is restored against the legal maximum that exists now. Snapshot maximumHP is evidence, not blindly authoritative. Procedure:

restore snapshot life/death/Wounds and rewindable max-HP modifiers;
retain current conserved level, ability scores, feats, permanent progression, current physical inventory/ownership and current nonrewindable external modifiers;
recompute effectiveMaximum using the already-reviewed max-HP rules;
assign restoredHP = min(snapshotHP, currentEffectiveMaximum).

If the current legal maximum is lower because gear was destroyed/transferred or another conserved source disappeared, clamp snapshot HP downward. That clamp is temporal normalization — not damage, healing, Wound generation, resource generation or a damage event.

If the current maximum is higher, do not scale or raise HP; restore the numeric snapshot HP unless another exact Time Loop field says otherwise.

The Critical healing ceiling does not cap this assignment because Time Loop restoration is not ordinary healing. Restore snapshot Wounds independently, then use the legal max-HP recomputation.

XP, level, ASI and feat acquisition are conserved progression and do not rewind. Reward-opportunity conservation prevents obtaining the same reward twice. A mid-encounter progression change that changes the participant schema/source set is an explicit structural divergence: unless there is a reviewed temporal adapter for that progression event, Time Loop preflight fails rather than manufacturing initial per-encounter state for a newly acquired feature. 
Pasted text
 The existing LifeState holder contains current/max HP but that field list itself is not permission to deepcopy stale maximum HP. 
Pasted text

Off-scene concentration and external effects — dependency closure does not make an external caster a rewind participant. Define two roles:

FullParticipant: body/HP/position/state may rewind.
ExternalDependency: only its current source/effect/concentration references may be consulted.

A nonparticipant caster included only because a participant snapshot effect depends on it does not have their body, HP, position, memory, resource state or concentration slot rewound.

For a snapshot effect dependent on external concentration:

if the exact same external concentration record is still active and compatible, the participant can reference it;
if that external caster ended/replaced concentration after the snapshot, Time Loop cannot silently recreate the old slot/effect;
unless the effect source explicitly survives independently, that dependency makes restoration impossible and preflight fails.

A persistent effect applied after snapshot by an unrelated nonparticipant is conserved as a current external record. Restore the participant's rewindable baseline, then overlay/reconcile the external effect. Do not erase it merely because it wasn't in the snapshot. If it changes anatomy, maximum HP, control, suppression or placement in a way that cannot coexist with the proposed restored state, preflight fails. Never silently end or rewrite the unrelated caster's concentration. 
Pasted text

Physical derivatives — use a transitive provenance graph and distinguish reversible entities from conserved inventory. Every physical derivative that can intersect restoration needs:

immutable root physical IDs;
derivation event/root;
whether it is a surviving discrete entity/item;
current owner/controller;
independent ingredients/material roots.

Retire automatically only a post-snapshot TEMPORAL_DERIVATIVE_ENTITY whose whole physical identity derives from a rewindable participant/environment root and whose source is inside the temporal closure — e.g. a raised corpse-body, temporary body-object, encounter-created structure. Its creation resource remains spent. Current control alone does not create a second physical entitlement.

Do not silently retire conserved transferable inventory/loot. If a corpse part harvested after snapshot still exists as an item — especially if transferred/sold to a nonparticipant — restoring the complete snapshot body would duplicate physical matter while removing the item would violate conserved loot ownership. Unless an exact adapter can reconcile it without changing conserved ownership, preflight fails.

For a mixed crafted item containing both root-derived matter and unrelated ingredients, generic TemporalWorld may not uncraft it. If a source-specific provenance adapter can safely separate/reconcile the root contribution, use that; otherwise preflight fails. Unrelated ingredients/payments remain spent either way.

If the root-derived material was already actually consumed and no independent physical derivative survives, do not refund or recreate that consumed item; the body may still be restored because the consumed resource remains spent rather than surviving as a duplicate object.

A derivative under a nonparticipant's control may be retired only when the derivative itself is a registered rewindable entity and its removal does not mutate that nonparticipant's unrelated body/resources/source slot. If its external binding/source would also need alteration, preflight fails.

Environment restoration has the same external-protection rule: even without literal cell overlap, restoring/removing a wall/floor/door may not drop, crush, enclose, trap, forcibly move or otherwise change a nonparticipant's physical state. Any such consequence blocks preflight. The verified geometry only authorizes existing movement/space rules, including squeezing one size smaller; it does not supply a generic involuntary-growth/overlap solution. 
Pasted text
 
Pasted text

Persistent assets — conserve enrollment; rewind encounter state only for the same still-valid asset identity. Add a distinction:

PersistentAssetEnrollment: bond/elite/pet/asset/slot membership — conserved unless the exact source says it is encounter-only.
EncounterAssetState: HP, position, temporary state, encounter conditions/deployment posture — rewindable when the same asset remains enrolled.
AssetFiniteResources: charges/ammo/rest uses/materials — conserved.

Examples:

Ranger Beast: if the current bond still points to the snapshot Beast, restore its encounter state. If a later legal rebond changed the enrolled Beast, do not undo that bond. The old snapshot Beast may only be restored as an ordinary physical participant if its identity still legally exists; it does not regain the bond for free.
Mage elite/persistent pet: same rule: current persistent enrollment wins; encounter state rewinds only for that asset.
True Polymorph object-creature sponsor slot: current slot occupancy/sponsor validity must reconcile. If snapshot restoration would require restoring an old object-creature while a different current persistent occupant legally owns the same slot, do not double the slot or overwrite the new persistent identity. If the current occupant is itself a fully reversible post-snapshot temporal derivative that can lawfully return to its underlying state, the source adapter may free it; otherwise preflight fails.
Wizard raised undead/corpse lineage: use the physical-provenance rules from #8. Snapshot undead can rewind only without cloning/reusing a corpse lineage now committed elsewhere.
Mirror/device slots: source adapter distinguishes encounter-local deployed state from persistent reserved asset identity/capacity; do not generically copy a slot map.

This is a NEW source-aware reconciliation rule. The existing lifecycle packages already separate asset IDs, controllers, slots, corpse identities, command groups, stock, destruction and rebuild histories; Time Loop must use those semantics rather than overwrite them with a generic snapshot. 
Pasted text
 
Pasted text

Gear on restored forms — restore meld membership only for items that still legally exist with that identity; preserve later external gear separately. For a snapshot form/transformation:

restoredMeldSet = snapshotMeldSet ∩ currentExistingItems ∩ itemsStillOwned/HeldByParticipant
transferred/lost/destroyed/consumed items never reappear;
an item currently owned by somebody else stays there;
later-acquired external gear that is compatible with the restored anatomy remains external and usable; it does not become part of the old meld set;
incompatible current external gear is dropped atomically under the already-reviewed transformation placement rule, with no new form-entry/recapture hook.

All drop placements must be included in Time Loop preflight. If the item cannot occupy the participant's restored anchor or an already-authorized legal adjacent drop location without changing a protected nonparticipant/environment state, Time Loop is unavailable/unspent.

Restoring the anatomy does not fire:

form entry;
spell cast;
meld recapture;
resource reset;
buffer grant;
summon/deploy hooks.

Suppression is reconciled in two layers. Restore the rewindable snapshot source record, then apply current conserved external suppression such as ongoing antimagic. Snapshot “unsuppressed” cannot bypass an antimagic field that currently exists outside the temporal rollback. Conversely, a rewindable suppression source that existed at snapshot may restore if its source is itself in scope. Any resulting root/form anatomy placement must already pass preflight. This follows the promoted transformation rule that melded gear is identity-conserved and suppression does not recapture it. 
Pasted text

Memory and PvP — supernatural character memory is Oracle/alliance-specific; human player knowledge is not engine state. For each Time Loop activation define:
TemporalMemoryEligible(invokingOracle, character) = character == invokingOracle OR character was an ally of that Oracle at the immutable encounter snapshot.

Because the shared rules treat “ally” as including self unless explicitly excluded, the Oracle retains their own discarded-timeline memory. 
Pasted text

A player-character enemy in a PvP encounter who was not the invoking Oracle's snapshot ally does not receive supernatural in-character memory from that Time Loop, even though the human player obviously remembers what happened at the table. The engine cannot erase human knowledge, but it does not mark the character as knowing facts they were not source-eligible to retain.

Memory is cumulative across loops:

Oracle A's eligible allies keep memories from A's discarded iteration;
later Oracle B can grant additional retained memories to B's own snapshot-allied set;
later allegiance/control changes do not retroactively alter either eligibility set.

Each eligible character retains only facts that character actually perceived, experienced or was told. Hidden roster entries, unrevealed enemies, Director-only information, unseen rolls and unobserved actions do not leak from the snapshot serializer into character knowledge.

Memory never dictates behavior. No previous choice is replayed, and no player or NPC is forced to “correct” the timeline. The original source specifically frames memory as enabling different choices. 
Pasted text

Minimum TemporalWorld adapters and additional source evidence. character-storage.js should not be used as the canonical world rollback mechanism. The attached inventory correctly shows that state is distributed across many real holders and that field existence alone does not establish rewind semantics. 
Pasted text

The minimum implementation adapters I would require before calling the authored Time Loop reference complete are:

initiative/iteration scheduler adapter: round/turn identities, Reaction debts, command/offense/extra-Action budgets, global regular-marker/recharge phase;
Core life/max-HP/Stable adapter;
BufferLedger adapter for grant identity, remaining THP, dependency/rider state and rest-epoch validity;
temporal one-shot/HealingCommit adapter for historical audit versus iteration consumption view;
SoulBind/revival/identity-return adapter;
ConcentrationLedger + TransformationWorld adapter;
DruidState/FormInstance/OwnerRechargeClock adapter;
CreatureWorld/corpse/body-lineage/persistent-asset adapter;
device Lifecycle/Entity/Destruction/CommandLedger adapter;
RemainingWorld structures/Choir/Undeath/Palisade/Ledger-control adapter;
FeatWorld adapter for Soul Charges, Lifeleech reserve/histories, Necrotic seals, Agony, recipient-family/rest histories and summon lineages;
healing-pulse/control-state adapter for active marks, one-shot riders and pulse-series state;
physical inventory/provenance adapter;
environment-anchor/geometry adapter;
reward-opportunity ledger;
external dependency/concentration adapter;
temporal-memory/perception overlay.

No additional class cards are required before writing the framework and adapters for the already-reviewed lifecycle, Druid/form, transformation, healing/death, device/remaining-lifecycle and eight-feat packages. Their reviewed packages already supply the source semantics needed for those domains.

However, snapshot completeness must reject any active state-holder whose exact source cannot yet be mapped to a temporal policy. The first likely families needing exact source evidence if their existing review packets do not already provide a source-ID mapping are:

SpeedRecord
GuidingStarMark
WrathfulBrand
generic OneShotRider
PerTurnReflection
PulseSeries
BloomReserve
FirstContactLedger
NativeOccurrenceLedger

Their holders do not, by themselves, prove whether a record is world-absolute, turn-relative, per-encounter, rest-bound, or consumable. If the existing control/pulse review source registry already maps those instances to exact source IDs and lifecycle rules, use that registry and no new class-card packet is necessary. If it does not, those exact source records are the next evidence I would request before permitting such an instance in a “complete” Time Loop snapshot. The same rule applies to any future unsupported source: it makes that specific snapshot unavailable rather than opting in through an unchecked boolean. 
Pasted text
 
Pasted text

These decisions leave Time Loop at:

SOURCE-DISCUSSED / IMPLEMENTATION-READY — twelve concrete world-conservation boundaries reconciled; actual TemporalWorld code, adapters and adversarial validation still require independent review.

This does not satisfy the owner's final project gate. Even after Time Loop receives its own bounded closure, there is still no authorized GitHub push until the final joint whole-game flow review confirms the authored game flows correctly as a whole. 
Pasted text
