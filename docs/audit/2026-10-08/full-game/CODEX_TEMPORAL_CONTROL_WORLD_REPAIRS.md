# Live control/pulse repairs — 44 methods pass

Your completed five findings are preserved verbatim in GPT_TEMPORAL_CONTROL_WORLD_FINDINGS.md. All five and the Eternal Bloom correction are repaired. I also added Crown Restored to the concentration-required set: no exact exemption exists in the supplied evidence; its alias explicitly incorporates oracle.engine[26]. Please review the concrete repairs and give a bounded disposition or another reproducible defect. This does not ask for full nine-family, full Time Loop, whole-game, balance, or GitHub closure.

1. Child entry checks now clone/advance the actual pulse parent to current time, rejecting a stale unobserved missed-upkeep parent without applying any child effect or mutating the parent. Both already-ended and unobserved-ended cases are tested.
2. Capture rejects participant claims already in the active RecipientLedger. Outsider-only claims are conserved. Tests that formerly had an unsupported preinitiative numeric-round claim now use a first pulse with no eligible output targets; no target budget is cleared to make them pass. A direct import-rejection test proves capture has no state/cost changes. Original outside-round mapping remains unimplemented.
3. TemporalControlWorld now REQUIRES outputs=<the host's existing ConservedPulseOutputs> as an explicit constructor argument; there is no fallback that silently creates another ledger. It registers/reuses the same actual PulseSeries in that guard, verifies all guard registrations are represented, delegates resolve_pulse for Ki/Conviction profiles to guard.resolve, watches the guard schema/bindings/consumed/events, and writes missed-opportunity reconciliation into guard.consumed. The approved guard file is unchanged. Tests resolve first via the old guard then via the world after a real restore, and reverse the paths; the same Ki allowance cannot recur. Host obligations remain one canonical guard per world and final atomic capped resource application, as with the other canonical holder contracts.
4. Speed suppressed=True is rejected without the missing provenance adapter, including at capture and after a previously unsuppressed snapshot. No unknown suppression Boolean is rewound.
5. tx.watch_shape(self.concentration) now rejects newly added live concentration state after preflight. The actual counterexample is tested.
6. Eternal Bloom and Crown Restored require exact current concentration. Tests explicitly reject both without it. Existing fixtures use real ConcentrationLedger entries/callbacks.

44 integration methods pass. The 76 foundation and 22 payment/output regressions still pass; the foundation extension remains exactly hash 45ad6ab7d2b26baf7bc56a8377d82398781175d5a81c7562b3dedeb40f28d577, submitted with its full diff in the preceding packet. The approved payment/output helper remains hash 835a108a80e5ad8c5d030dbf7d927e0491bc944eb2697d71f2504fd2e0b1df12. The complete revised module, complete tests, unchanged guard and current status guide follow so composition can be assessed directly.

No original source changed, no scope count promoted, no whole-game push performed. All seven larger integrations remain incomplete; full source sibling/lifecycle execution, external round import, final HP/Ki/Conviction mutation, entry/movement/extra-turn/mutation/device/form parents, shared multi-parent contacts, and source-specific eligibility remain separately required.


## tools/temporal_control_world.py

```
"""Source-qualified live control/pulse state in the temporal transaction.

Implementation candidate. Parent adapters not supplied here remain admission
requirements; this module does not claim full Time Loop or full-card execution.
"""
from dataclasses import dataclass, fields, MISSING
from control_playtest_rules import (ClockMarker, SpeedRecord, GuidingStarMark,
    WrathfulBrand, OneShotRider, PerTurnReflection)
from healing_pulse_playtest_rules import (PulseSeries, RecipientLedger, BloomReserve,
    FirstContactLedger, NativeOccurrenceLedger, PROFILES, NATIVE_COSTS)
from transformation_spell_playtest_rules import ConcentrationLedger
from temporal_playtest_rules import data, ident, require, shape
from temporal_control_playtest_rules import ConservedPulseOutputs, INDEPENDENT_OUTPUTS
from spell_playtest_rules import integer, SpellRuleError


# Exact source/component policies; no prefix or duration-length inference.
# A paired child can have an earlier source-parent ending as well.
CONTROL_POLICIES = {
    ('ray-of-frost','ordinary.ray-of-frost.slow'):('speed','target-end'),
    ('frost-arrow','ordinary.frost-arrow.slow'):('speed','target-end'),
    ('monk.hero.way-of-shadow.nerve-strike','monk.nerve-strike.speed-zero'):('speed','target-end'),
    ('soldier.arch.suppression-fire','soldier.suppression-fire.slow'):('speed','owner-end'),
    ('dragoon.hero.drake-rider.elemental-lance','dragoon.elemental-lance.cold-slow'):('speed','owner-end'),
    ('mage.base.elemental-bolt','mage.cold-focus.flat'):('speed','target-end'),
    ('mage.base.cold.cold','mage.cold-focus.flat'):('speed','target-end'),
    ('mage.base.cold.cold','mage.cold-focus.glacier'):('speed','target-end'),
    ('mage.arch.elemental-surge','mage.cold-focus.flat'):('speed','target-end'),
    ('oracle.supplement.stars.guiding-bolt','oracle.guiding-bolt.star-mark'):('guiding','target-end'),
    ('oracle.supplement.flame.wrathful-brand','oracle.wrathful-brand'):('brand','owner-end'),
    ('dragoon.hero.drake-rider.drake-mark','dragoon.drake-mark'):('rider:hit','owner-end'),
    ('soldier.hero.tyrant.marked-for-death','soldier.marked-for-death'):('rider:hit','owner-start'),
    ('thief.hero.shadowblade.vein-cutter','thief.vein-cutter.attack-damage-penalty'):('rider:hit','target-end'),
    ('thief.hero.blackguard.crippling-lash','thief.crippling-lash.weapon-hit-damage-penalty'):('rider:hit','target-end'),
    ('cleric.hero.priest.balanced-scales','cleric.balanced-scales.mark'):('rider:damage','owner-start'),
    ('oracle.supplement.dream.slumber-glimpse','oracle.slumber-glimpse.attack-bonus'):('rider:attack','target-end'),
    ('paladin.supplement.oath-of-vengeance.mark-of-retribution','paladin.vengeance-mark.retribution'):('rider:hit','owner-end'),
    ('tinker.engine[3]','tinker.target-scanner.mark'):('rider:attack','owner-start'),
    ('cleric.hero.priest.divine-judgment','cleric.divine-judgment.mark'):('reflection','target-end'),
}

PULSE_SOURCES = {
    'sacred-chant':'cleric.base.sacred-chant', 'sacrament':'cleric.arch.sacrament',
    'dark-sacrament':'cleric.hero.cultist.dark-sacrament',
    'healing-briar':'ranger.hero.warder.healing-briar',
    'circle-of-harmony':'monk.hero.enlightened-master.circle-of-harmony',
    'renewal':'shaman.engine[1]', 'renewal-extended':'shaman.engine[1]',
    'restoration-field':'tinker.hero.artificer.restoration-field',
    'desecrated-ground':'paladin.supplement.oathbreaker-shared.desecrated-ground',
    'lifewell':'crimson-agent.hero.bloodweaver.lifewell',
    'unfinished-chorus':'oracle.supplement.bones.unfinished-chorus',
    'song-of-mending':'oracle.supplement.life.song-of-mending',
    'enhanced-song':'oracle.supplement.life.song-of-mending',
    'transcendent-meditation':'monk.hero.enlightened-master.transcendent-meditation',
    'eternal-bloom':'oracle.supplement.life.eternal-bloom',
    'wound-eater-iv':'oracle.supplement.wound-eater.wound-eater-boon-iv',
    'hemostasis':'crimson-agent.hero.bloodweaver.hemostasis',
    'cellular-reconstruction':'warrior.hero.ironskin.cellular-reconstruction',
    'cleric-echoes':'cleric.base.echoes.echoes',
    'resonant-seed':'oracle.supplement.life.resonant-seed',
    'garden':'oracle.supplement.life.garden-of-restoration',
    'burning-blood-v':'oracle.supplement.burning-blood.burning-blood-boon-v',
    'crown-restored':'oracle.supplement.flame.crown-restored',
    'nano-aegis':'tinker.hero.artificer.nano-aegis-drone',
}
CONCENTRATION_PROFILES = frozenset(('sacred-chant','sacrament','dark-sacrament',
    'healing-briar','circle-of-harmony','renewal','renewal-extended','restoration-field',
    'desecrated-ground','lifewell','unfinished-chorus','song-of-mending','enhanced-song',
    'transcendent-meditation','resonant-seed','garden','burning-blood-v','wound-eater-iv',
    'eternal-bloom','crown-restored'))
PARENT_PROFILES = frozenset(('renewal','renewal-extended','nano-aegis',
                            'cellular-reconstruction','cleric-echoes'))
HOLDER_TYPES = {'speed':SpeedRecord,'guiding':GuidingStarMark,'brand':WrathfulBrand,
    'rider':OneShotRider,'reflection':PerTurnReflection,'pulse':PulseSeries,
    'bloom':BloomReserve,'contact':FirstContactLedger,'native':NativeOccurrenceLedger}
IMMUTABLE_FIELDS = {
    'speed':('application_id','owner','target','group','profile','mode','amount','floor','expires','slowed_hook'),
    'guiding':('owner','target','expires','s','_identity'),
    'brand':('owner','target','expires'), 'rider':('trigger_kind',),
    'reflection':('cleric_level',),
    'pulse':('instance_id','profile_name','activation','future_starts','roster','maintenance_ends','expires','opens'),
    'bloom':('roster_missing','shares'), 'contact':('profiles',), 'native':(),
}


@dataclass
class BoundEffect:
    identity: str
    family: str
    source: str
    component: str
    owner: str
    targets: tuple
    holder: object
    origin: str
    deadline: ClockMarker | None
    concentration_id: str | None = None
    parent_id: str | None = None
    dependencies: tuple = ()


class TemporalRecipientLedger(RecipientLedger):
    """Existing PulseSeries reads claimed directly, so keep its active view.

The additional history uses iteration-qualified round tokens and is conserved.
Only the temporal adapter restores claimed; an ordinary commit never clears it.
"""
    def __init__(self, scheduler):
        super().__init__()
        self.scheduler=scheduler
        self.history=set()

    def check(self,domain,targets,round_number):
        require(round_number==self.scheduler.round,'Recipient round is not the current canonical round')
        super().check(domain,targets,round_number)

    def commit(self,domain,targets,round_number):
        super().commit(domain,targets,round_number)
        if domain:
            self.history.update((domain,t,self.scheduler.round_id().token()) for t in targets)


def payload(holder):
    """Explicit fields only; canonical ledger/profile references stay live."""
    names={f.name for f in fields(type(holder))}|set(vars(holder))
    if type(holder) is PulseSeries:names-={'ledger','profile'}
    return {k:data(getattr(holder,k)) for k in names}


def plain_clone(holder, values):
    """Pure data projection for advance(); never calls a cast/entry constructor."""
    candidate=object.__new__(type(holder))
    for key,value in values.items():object.__setattr__(candidate,key,data(value))
    if type(holder) is PulseSeries:
        candidate.ledger=holder.ledger
        candidate.profile=holder.profile
    return candidate


class TemporalControlWorld:
    def __init__(self, scheduler, *, outputs, concentration=None):
        require(type(outputs) is ConservedPulseOutputs and outputs.kernel.scheduler is scheduler,
                'Supply the existing canonical independent-output guard for this host')
        self.scheduler=scheduler
        self.outputs=outputs
        self.concentration=concentration if concentration is not None else ConcentrationLedger()
        self.recipients=TemporalRecipientLedger(scheduler)
        self.records={}
        self.canonical={}
        self.active=set()
        self.events={}
        self.native_evaluations={}

    def register(self, record):
        shape(record,BoundEffect)
        ident(record.identity)
        require(record.identity not in self.records,'Canonical control identity already registered')
        require(record.family in HOLDER_TYPES,'Unsupported temporal control family')
        require(type(record.holder) is HOLDER_TYPES[record.family],'Control holder type mismatch')
        if record.family=='pulse' and record.holder.profile_name in INDEPENDENT_OUTPUTS:
            if record.identity in self.outputs.series:
                h,owner,_=self.outputs._binding(record.identity)
                require(h is record.holder and owner==record.owner
                        and self.outputs.series[record.identity][2]==record.source,
                        'Existing independent-output binding differs')
            else:self.outputs.register(record.holder,record.owner,record.source)
        self.records[record.identity]=record
        self.canonical[record.identity]=record if record.family=='speed' else record.holder
        self.active.add(record.identity)

    def _validate_record(self, kernel, record):
        shape(record,BoundEffect)
        h=record.holder
        require(record.family in HOLDER_TYPES and type(h) is HOLDER_TYPES[record.family],
                'Unsupported live control holder')
        expected_canonical=record if record.family=='speed' else h
        require(self.canonical.get(record.identity) is expected_canonical,'Canonical effect holder was replaced')
        require(record.owner in kernel.lives and set(record.targets)<=kernel.lives.keys(),
                'Control source/target not in canonical scene')
        require(type(record.targets) is tuple and len(record.targets)==len(set(record.targets)),
                'Distinct canonical effect targets required')
        require(record.origin in ('outside','encounter'),'Explicit source origin required')
        require(record.deadline is None or type(record.deadline) is ClockMarker,'Explicit source deadline required')
        expected={f.name for f in fields(type(h))}
        required={f.name for f in fields(type(h)) if f.init or f.default_factory is not MISSING}
        if record.family=='pulse':expected|={'profile','opens'}
        if record.family=='bloom':expected|={'shares'}
        required|=expected-{f.name for f in fields(type(h))}
        require(required<=set(vars(h))<=expected,'Unclassified control/pulse holder fields')
        require(not record.dependencies,'Required physical/device/form/source parent adapter missing')
        if record.family in ('speed','guiding','brand','rider','reflection'):
            policy=CONTROL_POLICIES.get((record.source,record.component))
            require(policy is not None,'Exact temporal control source policy missing')
            require(policy[0].split(':')[0]==record.family,'Source component/holder mismatch')
            require(len(record.targets)==1,'One target for this control holder')
            if record.family=='rider':
                require(h.trigger_kind==policy[0].split(':')[1],'Source rider trigger mismatch')
            if hasattr(h,'owner'):require(h.owner==record.owner,'Control owner mismatch')
            if hasattr(h,'target'):require(h.target==record.targets[0],'Control target mismatch')
            if hasattr(h,'expires'):require(h.expires==record.deadline,'Control source deadline mismatch')
            require(record.deadline is not None,'Parent/clock source adapter required')
            if record.family=='speed':require(h.application_id==record.identity,'Speed application identity mismatch')
            if record.family=='speed':
                require(h.suppressed is False,'Speed suppression provenance adapter required')
                choices={('flat',10,0)}
                if record.source=='monk.hero.way-of-shadow.nerve-strike':choices={('zero',0,0)}
                elif record.source=='dragoon.hero.drake-rider.elemental-lance':choices={('flat',5,0)}
                elif record.component=='mage.cold-focus.flat':choices={('flat',10,0),('flat',15,0)}
                elif record.component=='mage.cold-focus.glacier':choices={('half',0,0),('half-minus',5,0)}
                require((h.mode,h.amount,h.floor) in choices and h.slowed_hook is True,
                        'Unreviewed source Speed profile/magnitude')
            if record.family=='guiding':
                require(not h._pending,'Mid-roll Guiding Star state blocks Time Loop')
                ident(h._identity);integer(h._next_token,'historical attack token',0)
            if record.family=='reflection':require(record.concentration_id is not None,'Divine Judgment concentration required')
        elif record.family=='pulse':
            require(h.instance_id==record.identity and PULSE_SOURCES.get(h.profile_name)==record.source,
                    'Pulse source/profile/application mismatch')
            require(h.profile is PROFILES[h.profile_name] and h.ledger is self.recipients,
                    'Pulse must use its canonical profile and shared recipient ledger')
            require(h.profile_name not in PARENT_PROFILES,'Full device/stasis/copy parent adapter required')
            require(h.expires==record.deadline,'Pulse deadline identity mismatch')
            require(len(h.states)==h.profile.count and set(h.states)<=
                    {'pending','funded','committed','lost','closed'},'Malformed pulse opportunity state')
            require(set(h.roster)<=set(record.targets),'Pulse fixed roster/target mismatch')
            if h.profile_name=='hemostasis':
                require(len(record.targets)==1 and h.roster==record.targets,'Hemostasis requires its one actual target')
            projected=PulseSeries(h.instance_id,h.profile_name,h.activation,h.future_starts,self.recipients,
                                  h.roster,h.maintenance_ends,h.expires)
            require(projected.opens==h.opens,'Pulse schedule differs from source construction')
            if h.profile_name in CONCENTRATION_PROFILES:
                require(record.concentration_id is not None,'Source concentration required')
        elif record.family in ('bloom','contact'):
            require(record.parent_id in self.records,'Exact pulse parent required')
            parent=self.records[record.parent_id]
            require(parent.family=='pulse' and parent.owner==record.owner,'Wrong pulse parent identity')
            require(set(record.targets)<=set(parent.targets),'Child recipients differ from actual parent')
            if record.family=='bloom':
                require(record.source==PULSE_SOURCES['eternal-bloom'] and parent.holder.profile_name=='eternal-bloom',
                        'Bloom requires its actual Eternal Bloom parent')
                require(set(h.roster_missing)==set(parent.holder.roster),'Bloom immutable roster mismatch')
                from healing_pulse_playtest_rules import installments
                require(h.shares=={t:installments(n) for t,n in h.roster_missing.items()},'Bloom shares were changed')
                require(h.consumed==set(range(len(h.consumed))) and len(h.consumed)<=3,'Bloom consumption order invalid')
            else:
                profile=h.profiles.get(record.parent_id)
                require(set(h.profiles)=={record.parent_id} and profile in ('garden','enhanced-garden','resonant-seed'),
                        'Contact parent/profile missing or shared cross-parent state requires adapter')
                require(parent.holder.profile_name==('garden' if profile=='enhanced-garden' else profile),
                        'Contact profile differs from parent')
                require(record.source==parent.source,'Contact source identity mismatch')
        else:
            require(record.source in ('cleric.hero.saint.aura-of-grace','ranger.hero.warder.living-pulse',
                    'thief.hero.blackguard.exsanguinate'),'Native mutation reserve/movement adapter required')
            require(record.targets==(record.owner,) and record.deadline is None,'Native ability is not a timed pulse')
        if record.concentration_id is not None and record.identity in self.active:
            current=self.concentration.current.get(record.owner)
            require(current is not None and current[0]==record.concentration_id,
                    'Exact current concentration parent missing; restoration adapter required')
        if record.parent_id is not None:
            require(record.parent_id!=record.identity and record.parent_id in self.records,'Missing/cyclic parent')

    def validate(self,kernel):
        require(set(vars(self))=={'scheduler','concentration','recipients','records','canonical',
                'active','events','native_evaluations','outputs'},'Unclassified control world state')
        require(self.scheduler is kernel.scheduler,'Control scheduler alias differs')
        require(type(self.outputs) is ConservedPulseOutputs and self.outputs.kernel is kernel
                and set(vars(self.outputs))=={'kernel','series','consumed','events'},
                'Canonical independent-output guard/schema required')
        expected_outputs={key for key,r in self.records.items() if r.family=='pulse'
                          and r.holder.profile_name in INDEPENDENT_OUTPUTS}
        require(set(self.outputs.series)==expected_outputs,'Undisclosed independent-output source')
        for key in expected_outputs:
            h,owner,_=self.outputs._binding(key)
            require(h is self.records[key].holder and owner==self.records[key].owner,
                    'Independent-output guard and live world must share canonical holders')
        require(type(self.concentration) is ConcentrationLedger and set(vars(self.concentration))=={'current'},
                'Canonical concentration ledger required')
        require(type(self.recipients) is TemporalRecipientLedger and self.recipients.scheduler is kernel.scheduler,
                'Canonical temporal recipient ledger required')
        require(set(vars(self.recipients))=={'claimed','scheduler','history'},'Recipient schema changed')
        require(set(self.records)==set(self.canonical) and self.active<=self.records.keys(),'Control registry incomplete')
        require(len({id(r.holder) for r in self.records.values()})==len(self.records),'Shared control holder needs one canonical record')
        for key,r in self.records.items():
            require(key==r.identity,'Control registry/application mismatch')
            self._validate_record(kernel,r)
            seen={key};parent=r.parent_id
            while parent is not None:
                require(parent not in seen and parent in self.records,'Missing/cyclic source parent')
                seen.add(parent);parent=self.records[parent].parent_id
        hemostasis=[r.targets[0] for r in self.records.values() if r.identity in self.active
                    and r.family=='pulse' and r.holder.profile_name=='hemostasis'
                    and r.holder.ended_at is None]
        require(len(hemostasis)==len(set(hemostasis)),'Only one active Hemostasis per target')

    def capture_payload(self,kernel,roster):
        self.validate(kernel)
        require(not any(claim[1] in roster for claim in self.recipients.claimed),
                'Outside-initiative recipient round import adapter required')
        for r in self.records.values():
            require(r.family=='native' or r.origin=='outside',
                    'No supplied active control source is created at the immutable initiative boundary')
        return {'records':{key:{'metadata':{k:data(v) for k,v in vars(r).items() if k!='holder'},
                               'fields':payload(r.holder)} for key,r in self.records.items()},
                'active':data(self.active),'recipientClaims':data(self.recipients.claimed)}

    def watch(self,tx):
        tx.labels[id(self)]='control-world'
        tx.watch_shape(self)
        for name in ('scheduler','concentration','recipients','records','canonical','outputs'):
            tx.watch_binding(self,name)
        tx.watch_registry(self.records);tx.watch_registry(self.canonical)
        for name in ('active','events','native_evaluations'):tx.watch(self,name)
        tx.watch_shape(self.concentration)
        tx.watch_binding(self.concentration,'current');tx.watch_registry(self.concentration.current)
        tx.labels[id(self.outputs)]='control-independent-outputs'
        tx.watch_shape(self.outputs);tx.watch_binding(self.outputs,'kernel')
        tx.watch_binding(self.outputs,'series');tx.watch_registry(self.outputs.series)
        tx.watch(self.outputs,'consumed');tx.watch(self.outputs,'events')
        tx.labels[id(self.recipients)]='control-recipients'
        tx.watch_shape(self.recipients);tx.watch_binding(self.recipients,'scheduler')
        tx.watch(self.recipients,'claimed');tx.watch(self.recipients,'history')
        for key,r in self.records.items():
            tx.labels[id(r)]='control-binding:'+key
            tx.labels[id(r.holder)]='control-holder:'+key
            tx.watch_shape(r);tx.watch_binding(r,'holder');tx.watch_shape(r.holder)
            for name in vars(r):
                if name!='holder':tx.watch(r,name)
            for name in vars(r.holder):
                if r.family=='pulse' and name in ('ledger','profile'):tx.watch_binding(r.holder,name)
                else:tx.watch(r.holder,name)

    def stage_restore(self,kernel,tx,saved,roster,new_iteration):
        self.validate(kernel)
        now=kernel.scheduler.now
        require(set(saved['records'])<=self.records.keys(),'Snapshot effect object disappeared')
        desired=set(self.active)
        missed_outputs=set()
        def restored_active(key):
            record=self.records[key]
            old=saved['records'].get(key)
            if old is None or key not in saved['active']:return False
            if record.deadline is not None and now>=record.deadline:return False
            if record.parent_id is not None and not restored_active(record.parent_id):return False
            if record.family=='pulse':
                clone=plain_clone(record.holder,old['fields'])
                clone.advance(now)
                if clone.ended_at is not None:return False
            return True
        for key,r in self.records.items():
            touches=r.owner in roster or bool(set(r.targets)&roster)
            if not touches:continue
            require(r.owner in roster and set(r.targets)<=roster,'External control overlay/recipient adapter required')
            old=saved['records'].get(key)
            if old is not None:
                require(old['metadata']=={k:data(v) for k,v in vars(r).items() if k!='holder'},
                        'Immutable source provenance or deadline changed')
                require(all(getattr(r.holder,name)==old['fields'][name] for name in IMMUTABLE_FIELDS[r.family]),
                        'Immutable source effect parameters changed')
            active=restored_active(key)
            if r.concentration_id is not None:
                current=self.concentration.current.get(r.owner)
                if active:
                    require(current is not None and current[0]==r.concentration_id,
                            'Snapshot concentration ended; actual parent restoration adapter required')
                elif current is not None and current[0]==r.concentration_id:
                    raise SpellRuleError('Concentration retirement requires its source parent adapter')
            if r.family=='native':
                require(old is not None,'New persistent native ability is a progression divergence')
                continue  # Native occurrence and expenditure histories never rewind.
            candidate=payload(r.holder) if old is None else data(old['fields'])
            if r.family=='guiding':
                require(old is None or candidate['_identity']==r.holder._identity,'Canonical mark identity changed')
                candidate['_next_token']=max(candidate['_next_token'],r.holder._next_token)
                candidate['_pending']=set()
            if r.family=='reflection':candidate['used_turn_ids']=data(r.holder.used_turn_ids)
            if r.family=='pulse':
                # Outside-origin real clock remains fixed. Purely retire missed
                # opportunities; advance() performs no healing, payment or pulse.
                clone=plain_clone(r.holder,candidate)
                clone.advance(now)
                candidate=payload(clone)
                active &= clone.ended_at is None
                if r.holder.profile_name in ('transcendent-meditation','sacred-chant'):
                    idx=1 if r.holder.profile_name=='transcendent-meditation' else 2
                    component='Ki' if idx==1 else 'Conviction'
                    # A missed actual clock occurrence is not banked. Reaching
                    # the original due marker alone performs no resource grant.
                    if candidate['states'][idx]=='lost' and now>r.holder.opens[idx]:
                        missed_outputs.add((key,idx,component))
            if not active:
                desired.discard(key)
                if 'active' in candidate:candidate['active']=False
                if 'available' in candidate:candidate['available']=False
                if r.family=='pulse':
                    candidate['states']=['lost' if x in ('pending','funded') else x for x in candidate['states']]
                    candidate['ended_at']=candidate['ended_at'] or now
                    candidate['ended_reason']=candidate['ended_reason'] or 'temporal-retired'
            else:desired.add(key)
            if r.family=='speed':
                tx.write(r,'holder',SpeedRecord(**candidate))
                # Frozen records are values; mutable source holders retain identity.
            else:
                for name,value in candidate.items():tx.write(r.holder,name,value)
        # A frozen SpeedRecord is a value owned by its canonical BoundEffect.
        # Its binding replacement is watched/committed atomically above.
        tx.write(self,'active',desired)
        restored_claims={claim for claim in self.recipients.claimed if claim[1] not in roster}
        restored_claims|={claim for claim in saved['recipientClaims'] if claim[1] in roster}
        tx.write(self.recipients,'claimed',restored_claims)
        tx.write(self.outputs,'consumed',self.outputs.consumed|missed_outputs)

    def _event(self,kernel,identity,event_id):
        self.validate(kernel);ident(event_id)
        require(event_id not in self.events and event_id not in self.outputs.events,'Control event replay')
        require(identity in self.active,'Control source is inactive')
        r=self.records[identity]
        require(r.deadline is None or kernel.scheduler.now<r.deadline,'Control source expired')
        parent_id=r.parent_id
        while parent_id is not None:
            parent=self.records[parent_id]
            require(parent_id in self.active and (parent.deadline is None or kernel.scheduler.now<parent.deadline),
                    'Control parent is inactive or expired')
            require(parent.family!='pulse' or parent.holder.ended_at is None,'Pulse parent ended')
            if parent.family=='pulse':
                projected=plain_clone(parent.holder,payload(parent.holder))
                projected.advance(kernel.scheduler.now)
                require(projected.ended_at is None,'Pulse parent has missed upkeep or expired')
            parent_id=parent.parent_id
        return r

    @staticmethod
    def _regular(kernel, actor, *, start=False):
        turn=kernel.scheduler.active_regular
        require(turn is not None and turn.actor==actor and turn.kind=='regular'
                and turn.encounter==kernel.scheduler.encounter and turn.iteration==kernel.scheduler.iteration,
                'Authentic current regular turn required')
        if start:require(kernel.scheduler.turn_phase=='start','Regular-start event window is closed')
        return turn

    def native_occurrence(self,kernel,identity,event_id,*,eligible,opted_in):
        r=self._event(kernel,identity,event_id)
        require(r.family=='native','Native ability required')
        require(type(eligible) is bool and type(opted_in) is bool,'Explicit native eligibility/choice required')
        turn=self._regular(kernel,r.owner,start=True)
        key=(r.source,r.owner,turn.token())
        require(key not in self.native_evaluations,'Native start opportunity already evaluated')
        from temporal_control_playtest_rules import CanonicalPulseWallet
        wallet=CanonicalPulseWallet(kernel,r.owner)
        result='ineligible' if not eligible else 'declined' if not opted_in else 'unaffordable' if wallet.rp<1 else 'occurred'
        if result=='occurred':
            wallet.spend(1);r.holder.consumed.add(key)
        self.native_evaluations[key]=result
        self.events[event_id]={'identity':identity,'iteration':turn.iteration,'turn':turn.token(),'result':result}
        return result=='occurred'

    def reflect(self,kernel,identity,event_id,*,positive_damage_event,actual_damage_dealt):
        r=self._event(kernel,identity,event_id)
        require(r.family=='reflection','Divine Judgment reflection record required')
        turn=self._regular(kernel,r.targets[0])
        result=r.holder.reflect(target_turn_id=turn.token(),positive_damage_event=positive_damage_event,
            actual_damage_dealt=actual_damage_dealt,on_target_turn=True)
        self.events[event_id]={'identity':identity,'iteration':turn.iteration,'turn':turn.token(),'result':result}
        return result

    def consume_bloom(self,kernel,identity,event_id,index,*,eligible_targets,pulse_event):
        r=self._event(kernel,identity,event_id)
        require(r.family=='bloom','Eternal Bloom reserve required')
        self._regular(kernel,r.owner,start=True)
        parent=self.records[r.parent_id].holder
        integer(index,'Bloom installment',0,2)
        require(parent.states[index]=='committed' and parent.opens[index]==kernel.scheduler.now,
                'Bloom installment requires its actual parent pulse occurrence')
        receipt=self.events.get(pulse_event,{})
        output=receipt.get('result') or {}
        require(receipt.get('identity')==r.parent_id and receipt.get('iteration')==kernel.scheduler.iteration
                and receipt.get('at')==kernel.scheduler.now and receipt.get('pulse')==index
                and set(eligible_targets)<=set(output.get('outputTargets',())),
                'Bloom installment requires a current unsuppressed parent pulse receipt')
        result=r.holder.consume(index,eligible_targets=eligible_targets)
        self.events[event_id]={'identity':identity,'iteration':kernel.scheduler.iteration,'installment':index,'result':data(result)}
        return result

    def contact(self,kernel,identity,event_id,target,*,event,eligible=True,pulse_event=None):
        r=self._event(kernel,identity,event_id)
        require(r.family=='contact' and target in r.targets,'Actual contact parent/recipient required')
        profile=r.holder.profiles[r.parent_id]
        require(event in (('entry','start') if profile=='garden' else ('pulse',)),
                'Source does not allow this contact event')
        require(event!='entry','Actual movement/entry receipt adapter required')
        if event=='start':self._regular(kernel,target,start=True)
        if event=='pulse':
            receipt=self.events.get(pulse_event,{})
            output=receipt.get('result') or {}
            require(receipt.get('identity')==r.parent_id and receipt.get('iteration')==kernel.scheduler.iteration
                    and receipt.get('at')==kernel.scheduler.now
                    and target in output.get('outputTargets',()),
                    'No current actual source pulse for this recipient')
        result=r.holder.claim(r.parent_id,target,event=event,eligible=eligible)
        self.events[event_id]={'identity':identity,'iteration':kernel.scheduler.iteration,'target':target,'event':event,'consumed':result}
        return result

    def resolve_pulse(self,kernel,identity,event_id,index,targets,*,upkeep_legal=True,whole_effect_suppressed=False):
        r=self._event(kernel,identity,event_id)
        require(r.family=='pulse','PulseSeries required')
        h=r.holder
        actor=r.targets[0] if h.profile_name=='hemostasis' else r.owner
        self._regular(kernel,actor,start=h.profile.mode in ('sequence','delayed-sequence'))
        targets=tuple(targets)
        require(set(targets)<=set(r.targets),'Declared recipient outside canonical source targets')
        from temporal_control_playtest_rules import CanonicalPulseWallet
        if h.profile_name in INDEPENDENT_OUTPUTS:
            result=self.outputs.resolve(identity,index,kernel.scheduler.now,targets,event_id=event_id,
                round_number=kernel.scheduler.round,real_encounter=True,upkeep_legal=upkeep_legal,
                whole_effect_suppressed=whole_effect_suppressed)
        else:
            result=h.resolve(index,kernel.scheduler.now,targets,CanonicalPulseWallet(kernel,r.owner),
                round_number=kernel.scheduler.round,upkeep_legal=upkeep_legal,
                whole_effect_suppressed=whole_effect_suppressed)
        self.events[event_id]={'identity':identity,'iteration':kernel.scheduler.iteration,'at':kernel.scheduler.now,
                              'pulse':index,'result':data(result)}
        return result

    def fund_window(self,kernel,identity,event_id,index,*,upkeep_legal=True):
        r=self._event(kernel,identity,event_id)
        require(r.family=='pulse','PulseSeries required');self._regular(kernel,r.owner,start=True)
        from temporal_control_playtest_rules import CanonicalPulseWallet
        r.holder.fund(index,kernel.scheduler.now,CanonicalPulseWallet(kernel,r.owner),upkeep_legal=upkeep_legal)
        self.events[event_id]={'identity':identity,'iteration':kernel.scheduler.iteration,'at':kernel.scheduler.now,'funded':index}

    def target_start(self,kernel,identity,event_id,target,*,eligible=True,whole_effect_suppressed=False):
        r=self._event(kernel,identity,event_id)
        require(r.family=='pulse' and target in r.targets,'Pulse parent/target required')
        self._regular(kernel,target,start=True)
        result=r.holder.target_start(target,kernel.scheduler.now,round_number=kernel.scheduler.round,
            eligible=eligible,whole_effect_suppressed=whole_effect_suppressed)
        self.events[event_id]={'identity':identity,'iteration':kernel.scheduler.iteration,'at':kernel.scheduler.now,
                              'result':data(result)}
        return result

    def trigger_rider(self,kernel,identity,event_id,**source_arguments):
        r=self._event(kernel,identity,event_id)
        require(r.family=='rider','OneShotRider required')
        result=r.holder.trigger(**source_arguments)
        self.events[event_id]={'identity':identity,'iteration':kernel.scheduler.iteration,'consumed':result}
        return result

```

## tools/validate_temporal_control_world.py

```
"""Live-object integration regressions, not whole-game/Time Loop approval."""
from dataclasses import replace
from copy import deepcopy
from pathlib import Path
import hashlib
import json
import unittest

from validate_temporal_playtests import scene,event,history
from temporal_playtest_rules import ClockMarker,SpellRuleError
from temporal_control_world import (TemporalControlWorld,BoundEffect,TemporalRecipientLedger,
    GuidingStarMark,WrathfulBrand,OneShotRider,SpeedRecord,PerTurnReflection,
    PulseSeries,BloomReserve,FirstContactLedger,NativeOccurrenceLedger,payload,PULSE_SOURCES,CONCENTRATION_PROFILES)
from temporal_control_playtest_rules import CanonicalPulseWallet,ConservedPulseOutputs


def world():
    w=scene(capture=False);c=TemporalControlWorld(w.scheduler,outputs=ConservedPulseOutputs(w))
    w.integrations['control-pulses']=c
    return w,c


def attach(c,family,holder,source,component,*,identity='effect',owner='a',targets=('b',),
           deadline=ClockMarker(30),parent=None,concentration=None,origin='outside'):
    record=BoundEffect(identity,family,source,component,owner,targets,holder,origin,deadline,
                       concentration_id=concentration,parent_id=parent)
    c.register(record);return record


def star(c,**kw):
    return attach(c,'guiding',GuidingStarMark('a','b',ClockMarker(30),3),
        'oracle.supplement.stars.guiding-bolt','oracle.guiding-bolt.star-mark',**kw)


def capture(w):w.capture(('a','b','foe'))


def whole_state(w,c):
    # Assertion-only copy; production never deepcopies the live scene.
    return deepcopy((history(w),c.active,c.events,c.native_evaluations,c.outputs.consumed,c.outputs.events,
        {k:payload(r.holder) for k,r in c.records.items()},c.recipients.claimed,c.recipients.history))


class ControlTransactionTests(unittest.TestCase):
    def test_star_same_object_entitlements_restore_tokens_do_not_rewind(self):
        w,c=world();r=star(c);capture(w);h=r.holder
        token=h.begin_ally_attack(actor='foe',ally_of_owner=True,now=1)['attackToken']
        h.resolve_ally_attack(token,hit=True,now=1)
        event(w,now=2);before=whole_state(w,c);plan=w.kernel_plan('a')
        self.assertEqual(whole_state(w,c),before);plan.commit()
        self.assertIs(r.holder,h);self.assertTrue(h.active and h.attack_bonus_available and h.hit_rider_available)
        self.assertEqual(h._next_token,1)
        next_token=h.begin_ally_attack(actor='foe',ally_of_owner=True,now=3)['attackToken']
        self.assertNotEqual(next_token,token)
        with self.assertRaises(SpellRuleError):h.resolve_ally_attack(token,hit=True,now=3)

    def test_pending_attack_blocks_atomic_restore_without_cost(self):
        w,c=world();r=star(c);capture(w)
        r.holder.begin_ally_attack(actor='foe',ally_of_owner=True,now=1);event(w,now=2)
        before=whole_state(w,c)
        with self.assertRaisesRegex(SpellRuleError,'Mid-roll'):w.kernel_plan('a')
        self.assertEqual(whole_state(w,c),before)

    def test_brand_independent_entitlements_restore_in_place(self):
        w,c=world();h=WrathfulBrand('a','b',ClockMarker(30),ally_rider_available=False)
        attach(c,'brand',h,'oracle.supplement.flame.wrathful-brand','oracle.wrathful-brand')
        capture(w);h.trigger(actor='a',ally_of_owner=True,now=1,resolved_damage=4,direct_attack_hit=True,base_dice_total=8)
        event(w,now=2);w.kernel_plan('a').commit()
        self.assertTrue(h.owner_rider_available);self.assertFalse(h.ally_rider_available)

    def test_rider_actual_consumption_rewinds_history_remains(self):
        w,c=world();h=OneShotRider('hit')
        attach(c,'rider',h,'thief.hero.blackguard.crippling-lash','thief.crippling-lash.weapon-hit-damage-penalty')
        capture(w)
        self.assertTrue(c.trigger_rider(w,'effect','hit-one',qualifying=True,hit=True))
        event(w,now=2);w.kernel_plan('a').commit()
        self.assertTrue(h.available);self.assertIn('hit-one',c.events)
        with self.assertRaisesRegex(SpellRuleError,'replay'):c.trigger_rider(w,'effect','hit-one',qualifying=True,hit=True)

    def test_frozen_speed_value_updates_canonical_binding_atomically(self):
        w,c=world();h=SpeedRecord('effect','a','b','ray','ordinary','flat',10,expires=ClockMarker(30))
        r=attach(c,'speed',h,'ray-of-frost','ordinary.ray-of-frost.slow');capture(w)
        r.holder=replace(h,active=False)
        event(w,now=2);w.kernel_plan('a').commit()
        self.assertTrue(r.holder.active);self.assertIs(c.canonical['effect'],r)
        self.assertEqual(r.holder.application_id,'effect');c.validate(w)

    def test_world_expired_control_does_not_return(self):
        w,c=world();r=star(c);capture(w);event(w,now=31);w.kernel_plan('a').commit()
        self.assertNotIn('effect',c.active);self.assertFalse(r.holder.active)

    def test_unknown_speed_suppression_blocks_capture_and_restore(self):
        for initially_suppressed in (False,True):
            with self.subTest(initially_suppressed=initially_suppressed):
                w,c=world();h=SpeedRecord('effect','a','b','ray','ordinary','flat',10,
                                        expires=ClockMarker(30),suppressed=initially_suppressed)
                r=attach(c,'speed',h,'ray-of-frost','ordinary.ray-of-frost.slow')
                if initially_suppressed:
                    with self.assertRaisesRegex(SpellRuleError,'suppression provenance'):capture(w)
                else:
                    capture(w);r.holder=replace(h,suppressed=True);event(w,now=2)
                    before=whole_state(w,c)
                    with self.assertRaisesRegex(SpellRuleError,'suppression provenance'):w.kernel_plan('a')
                    self.assertEqual(whole_state(w,c),before)

    def test_added_concentration_schema_makes_prepared_plan_stale(self):
        w,c=world();star(c);capture(w);event(w,now=2);plan=w.kernel_plan('a')
        c.concentration.new_temporal_state={'unknown':True};before=whole_state(w,c)
        with self.assertRaises(SpellRuleError):plan.commit()
        self.assertEqual(whole_state(w,c),before)

    def test_post_snapshot_rider_retires_and_payment_stays_spent(self):
        w,c=world();capture(w);w.wallets['a'].rp-=2
        h=OneShotRider('hit');attach(c,'rider',h,'dragoon.hero.drake-rider.drake-mark','dragoon.drake-mark',origin='encounter')
        event(w,now=2);w.kernel_plan('a').commit()
        self.assertNotIn('effect',c.active);self.assertFalse(h.available);self.assertEqual(w.wallets['a'].rp,8)

    def test_unknown_or_mismatched_sources_block_admission(self):
        for change in ('source','component','holder','origin','extra'):
            with self.subTest(change=change):
                w,c=world();r=star(c)
                if change=='source':r.source='future'
                elif change=='component':r.component='future'
                elif change=='holder':r.holder=GuidingStarMark('a','b',ClockMarker(30),3)
                elif change=='origin':r.origin='encounter'
                else:r.holder.unclassified=True
                with self.assertRaises(SpellRuleError):capture(w)
                self.assertIsNone(w._snapshot)

    def test_stale_control_plan_rejects_before_any_core_write(self):
        for change in ('entitlement','record','registry','ledger'):
            with self.subTest(change=change):
                w,c=world();r=star(c);capture(w);event(w,now=2);plan=w.kernel_plan('a')
                if change=='entitlement':r.holder.active=False
                elif change=='record':r.deadline=ClockMarker(40)
                elif change=='registry':c.active.clear()
                else:c.recipients.claimed.add(('x','a',1))
                before=whole_state(w,c)
                with self.assertRaises(SpellRuleError):plan.commit()
                self.assertEqual(whole_state(w,c),before)

    def test_adapter_added_after_snapshot_blocks(self):
        w=scene();c=TemporalControlWorld(w.scheduler,outputs=ConservedPulseOutputs(w));w.integrations['control-pulses']=c
        event(w)
        with self.assertRaisesRegex(SpellRuleError,'adapter set changed'):w.kernel_plan('a')

    def test_external_target_is_not_silently_rewound(self):
        w=scene(capture=False,outsider=True);c=TemporalControlWorld(w.scheduler,outputs=ConservedPulseOutputs(w));w.integrations['control-pulses']=c
        h=GuidingStarMark('a','outside',ClockMarker(30),3)
        attach(c,'guiding',h,'oracle.supplement.stars.guiding-bolt','oracle.guiding-bolt.star-mark',targets=('outside',))
        capture(w);event(w,now=2)
        with self.assertRaisesRegex(SpellRuleError,'External control'):w.kernel_plan('a')


def pulse(c,profile,*,owner='a',identity='pulse',roster=('b',),concentration=None):
    mode_kwargs={}
    from healing_pulse_playtest_rules import PROFILES
    p=PROFILES[profile]
    if concentration is None:concentration=profile in CONCENTRATION_PROFILES
    starts=tuple(ClockMarker(6*(i+1)) for i in range(p.count))
    if p.mode=='maintenance':mode_kwargs['maintenance_ends']=tuple(ClockMarker(5+6*i,20) for i in range(p.count))
    h=PulseSeries(identity,profile,ClockMarker(0),starts,c.recipients,
                  roster=roster if p.fixed else (),**mode_kwargs)
    if concentration:c.concentration.start_committed(owner,identity,lambda reason: c.active.discard(identity))
    r=attach(c,'pulse',h,PULSE_SOURCES[profile],profile,identity=identity,owner=owner,targets=roster,
             deadline=h.expires,concentration=identity if concentration else None)
    return r


class PulseTransactionTests(unittest.TestCase):
    def test_preinitiative_recipient_claim_requires_import_adapter(self):
        w,c=world();c.recipients.commit('named:Circle of Harmony',('b',),1)
        before=whole_state(w,c)
        with self.assertRaisesRegex(SpellRuleError,'round import adapter'):capture(w)
        self.assertIsNone(w._snapshot);self.assertEqual(whole_state(w,c),before)

    def test_independent_output_is_shared_across_old_and_new_paths(self):
        for original_path in ('guard','world'):
            with self.subTest(original_path=original_path):
                w,c=world();r=pulse(c,'transcendent-meditation');guard=c.outputs
                guard.resolve('pulse',0,ClockMarker(0),('b',),event_id='initial',round_number=1,real_encounter=True)
                capture(w);w.regular_start('a',6)
                if original_path=='guard':
                    first=guard.resolve('pulse',1,ClockMarker(6),('b',),event_id='old-pulse',round_number=1,real_encounter=True)
                else:first=c.resolve_pulse(w,'pulse','old-pulse',1,('b',))
                self.assertEqual(first['independentKi'],1)
                event(w,now=6);w.kernel_plan('b').commit();w.regular_start('a',6)
                if original_path=='guard':second=c.resolve_pulse(w,'pulse','new-pulse',1,('b',))
                else:
                    second=guard.resolve('pulse',1,ClockMarker(6),('b',),event_id='new-pulse',round_number=1,real_encounter=True)
                self.assertEqual(second['independentKi'],0)
                self.assertEqual(guard.consumed,{('pulse',1,'Ki')})
                self.assertIs(c.outputs,guard)

    def test_guard_events_and_state_make_preflight_stale(self):
        for field in ('consumed','events','schema','binding'):
            with self.subTest(field=field):
                w,c=world();pulse(c,'transcendent-meditation');capture(w);event(w,now=2);plan=w.kernel_plan('a')
                if field=='consumed':c.outputs.consumed.add(('pulse',1,'Ki'))
                elif field=='events':c.outputs.events['outside-path']={'used':True}
                elif field=='schema':c.outputs.unknown=True
                else:c.outputs.series['pulse']=tuple(list(c.outputs.series['pulse']))
                before=whole_state(w,c)
                with self.assertRaises(SpellRuleError):plan.commit()
                self.assertEqual(whole_state(w,c),before)

    def test_existing_guard_registration_is_used_without_new_ledger(self):
        w,c=world();guard=c.outputs
        h=PulseSeries('pulse','transcendent-meditation',ClockMarker(0),
                      tuple(ClockMarker(t) for t in (6,12,18)),c.recipients,roster=('b',))
        guard.register(h,'a',PULSE_SOURCES['transcendent-meditation'])
        c.concentration.start_committed('a','pulse',lambda reason:c.active.discard('pulse'))
        attach(c,'pulse',h,PULSE_SOURCES['transcendent-meditation'],'transcendent-meditation',identity='pulse',
               concentration='pulse',deadline=h.expires)
        capture(w);self.assertIs(c.outputs,guard);self.assertIs(guard.series['pulse'][0],h)

    def test_oracle_finals_still_require_concentration(self):
        for profile in ('eternal-bloom','crown-restored'):
            with self.subTest(profile=profile):
                w,c=world();pulse(c,profile,concentration=False)
                with self.assertRaisesRegex(SpellRuleError,'Source concentration required'):capture(w)

    def test_live_resolution_uses_real_wallet_and_authenticated_start(self):
        w,c=world();r=pulse(c,'song-of-mending',concentration=True)
        r.holder.resolve(0,ClockMarker(0),(),CanonicalPulseWallet(w,'a'),round_number=1)
        capture(w)
        for actor,now in (('a',1),('b',2),('foe',3)):
            turn=w.regular_start(actor,now);w.scheduler.regular_end(turn,now)
        w.regular_start('a',6)
        result=c.resolve_pulse(w,'pulse','actual-song',1,('b',))
        self.assertEqual(result['outputTargets'],('b',));self.assertEqual(w.scheduler.rc['a'],4)
        self.assertIn('actual-song',c.events)

    def test_hemostasis_uses_target_start_not_owner_start(self):
        w,c=world();pulse(c,'hemostasis');capture(w)
        with self.assertRaises(SpellRuleError):c.resolve_pulse(w,'pulse','fake',0,('b',))
        ta=w.regular_start('a',6)
        with self.assertRaises(SpellRuleError):c.resolve_pulse(w,'pulse','wrong-owner',0,('b',))
        w.scheduler.regular_end(ta,6);w.regular_start('b',6)
        result=c.resolve_pulse(w,'pulse','target-start',0,('b',))
        self.assertEqual(result['outputTargets'],('b',))
        self.assertEqual(w.wallets['a'].rp,10)

    def test_hemostasis_duplicate_target_is_not_admitted(self):
        w,c=world();pulse(c,'hemostasis');pulse(c,'hemostasis',identity='duplicate')
        with self.assertRaisesRegex(SpellRuleError,'one active Hemostasis'):capture(w)

    def test_bloom_requires_fresh_current_iteration_parent_receipt(self):
        w,c=world();p=pulse(c,'eternal-bloom');h=BloomReserve({'b':10})
        attach(c,'bloom',h,PULSE_SOURCES['eternal-bloom'],'installments',identity='reserve',deadline=ClockMarker(18),parent='pulse')
        p.holder.resolve(0,ClockMarker(0),(),CanonicalPulseWallet(w,'a'),round_number=1)
        h.consume(0,eligible_targets=());capture(w)
        for actor,now in (('a',1),('b',2),('foe',3)):
            turn=w.regular_start(actor,now);w.scheduler.regular_end(turn,now)
        w.regular_start('a',6);c.resolve_pulse(w,'pulse','bloom-pulse',1,('b',))
        with self.assertRaisesRegex(SpellRuleError,'receipt'):
            c.consume_bloom(w,'reserve','forged',1,eligible_targets=('b',),pulse_event='absent')
        self.assertEqual(c.consume_bloom(w,'reserve','share',1,eligible_targets=('b',),pulse_event='bloom-pulse'),{'b':3})
        event(w,now=6);w.kernel_plan('b').commit();w.regular_start('a',6)
        with self.assertRaisesRegex(SpellRuleError,'actual parent pulse|receipt'):
            c.consume_bloom(w,'reserve','old-iteration',1,eligible_targets=('b',),pulse_event='bloom-pulse')

    def test_ended_parent_cannot_leave_contact_live(self):
        w,c=world();p=pulse(c,'garden',concentration=True);h=FirstContactLedger({'pulse':'garden'})
        attach(c,'contact',h,PULSE_SOURCES['garden'],'first-contact',identity='cure',deadline=ClockMarker(18),parent='pulse')
        capture(w);p.holder.end(ClockMarker(1),'test-ended');ta=w.regular_start('a',1)
        w.scheduler.regular_end(ta,1);w.regular_start('b',2)
        with self.assertRaisesRegex(SpellRuleError,'parent ended'):c.contact(w,'cure','bad-contact','b',event='start')
        self.assertEqual(h.consumed,set())

    def test_unobserved_missed_parent_upkeep_cannot_authorize_contact(self):
        w,c=world();p=pulse(c,'garden');h=FirstContactLedger({'pulse':'garden'})
        attach(c,'contact',h,PULSE_SOURCES['garden'],'first-contact',identity='cure',deadline=ClockMarker(18),parent='pulse')
        capture(w);ta=w.regular_start('a',7);w.scheduler.regular_end(ta,7);w.regular_start('b',7)
        self.assertIsNone(p.holder.ended_at)
        before=whole_state(w,c)
        with self.assertRaisesRegex(SpellRuleError,'missed upkeep'):
            c.contact(w,'cure','stale-parent','b',event='start')
        self.assertEqual(whole_state(w,c),before)

    def test_contact_pulse_needs_fresh_unsuppressed_parent_receipt(self):
        w,c=world();pulse(c,'resonant-seed',concentration=True);h=FirstContactLedger({'pulse':'resonant-seed'})
        attach(c,'contact',h,PULSE_SOURCES['resonant-seed'],'first-contact',identity='cure',deadline=ClockMarker(18),parent='pulse')
        capture(w);ta=w.regular_start('a',1);w.scheduler.regular_end(ta,1);w.regular_start('b',2)
        with self.assertRaises(SpellRuleError):c.contact(w,'cure','no-pulse','b',event='pulse')
        c.target_start(w,'pulse','seed-start','b',whole_effect_suppressed=True)
        with self.assertRaises(SpellRuleError):c.contact(w,'cure','suppressed','b',event='pulse',pulse_event='seed-start')
        self.assertEqual(h.consumed,set())

    def test_unrelated_outsider_recipient_budget_is_conserved(self):
        w=scene(capture=False,outsider=True);c=TemporalControlWorld(w.scheduler,outputs=ConservedPulseOutputs(w));w.integrations['control-pulses']=c
        capture(w);c.recipients.commit('named:Circle of Harmony',('outside',),1)
        event(w,now=2);w.kernel_plan('a').commit()
        self.assertIn(('named:Circle of Harmony','outside',1),c.recipients.claimed)

    def test_bloom_cannot_change_both_capture_and_recomputed_shares(self):
        w,c=world();pulse(c,'eternal-bloom');h=BloomReserve({'b':10})
        attach(c,'bloom',h,PULSE_SOURCES['eternal-bloom'],'installments',identity='reserve',deadline=ClockMarker(18),parent='pulse')
        capture(w);h.roster_missing={'b':99};h.shares={'b':(33,33,33)};event(w,now=2)
        with self.assertRaisesRegex(SpellRuleError,'parameters changed'):w.kernel_plan('a')

    def test_real_pulse_series_restores_in_place_without_cast_or_heal(self):
        w,c=world();r=pulse(c,'transcendent-meditation',concentration=True);h=r.holder
        h.resolve(0,ClockMarker(0),('b',),CanonicalPulseWallet(w,'a'),round_number=1)
        capture(w);h.end(ClockMarker(1),'temporary-test-state');event(w,now=2)
        old_life=w.lives['b'].hp;w.kernel_plan('a').commit()
        self.assertIs(r.holder,h);self.assertIs(h.ledger,c.recipients)
        self.assertEqual(h.states,['committed','pending','pending']);self.assertIsNone(h.ended_at)
        self.assertEqual(w.lives['b'].hp,old_life);self.assertEqual(h.future_starts,(ClockMarker(6),ClockMarker(12),ClockMarker(18)))

    def test_missed_original_due_pulse_is_lost_not_rebased(self):
        w,c=world();r=pulse(c,'hemostasis');capture(w);event(w,now=7)
        w.kernel_plan('a').commit()
        self.assertEqual(r.holder.states,['lost','pending','pending'])
        self.assertEqual(r.holder.opens[0],ClockMarker(6))

    def test_all_expired_outside_pulses_retire(self):
        w,c=world();r=pulse(c,'hemostasis');capture(w);event(w,now=20);w.kernel_plan('a').commit()
        self.assertNotIn('pulse',c.active);self.assertEqual(r.holder.states,['lost']*3)

    def test_missing_actual_concentration_blocks_without_mutation(self):
        w,c=world();r=pulse(c,'transcendent-meditation',concentration=True);capture(w)
        c.concentration.end('a','lost');event(w,now=2);before=whole_state(w,c)
        with self.assertRaisesRegex(SpellRuleError,'concentration'):w.kernel_plan('a')
        self.assertEqual(whole_state(w,c),before)

    def test_replaced_concentration_after_preflight_makes_plan_stale(self):
        w,c=world();pulse(c,'transcendent-meditation',concentration=True);capture(w);event(w,now=2)
        plan=w.kernel_plan('a');c.concentration.current['a']=('pulse',lambda reason:None)
        before=whole_state(w,c)
        with self.assertRaises(SpellRuleError):plan.commit()
        self.assertEqual(whole_state(w,c),before)

    def test_snapshot_fixed_roster_cannot_change(self):
        w,c=world();r=pulse(c,'eternal-bloom');capture(w);r.holder.roster=('a',);event(w,now=2)
        with self.assertRaisesRegex(SpellRuleError,'roster'):w.kernel_plan('a')

    def test_shared_recipient_current_view_rewinds_history_does_not(self):
        w,c=world();capture(w);c.recipients.commit('named:Circle of Harmony',('b',),1)
        old=set(c.recipients.history);event(w,now=2);w.kernel_plan('a').commit()
        self.assertEqual(c.recipients.claimed,set());self.assertEqual(c.recipients.history,old)
        c.recipients.commit('named:Circle of Harmony',('b',),1)
        self.assertEqual(len(c.recipients.history),2)
        with self.assertRaises(SpellRuleError):c.recipients.commit('named:Circle of Harmony',('b',),1)

    def test_bloom_original_shares_and_snapshot_consumption_restore(self):
        w,c=world();p=pulse(c,'eternal-bloom');h=BloomReserve({'b':10});h.consume(0,eligible_targets=('b',))
        attach(c,'bloom',h,PULSE_SOURCES['eternal-bloom'],'installments',identity='reserve',
               deadline=ClockMarker(18),parent='pulse')
        capture(w);h.consume(1,eligible_targets=('b',));event(w,now=2);w.kernel_plan('a').commit()
        self.assertEqual(h.consumed,{0});self.assertEqual(h.shares,{'b':(4,3,3)})

    def test_bloom_changed_original_missing_hp_rejected(self):
        w,c=world();pulse(c,'eternal-bloom');h=BloomReserve({'b':10})
        attach(c,'bloom',h,PULSE_SOURCES['eternal-bloom'],'installments',identity='reserve',deadline=ClockMarker(18),parent='pulse')
        capture(w);h.roster_missing['b']=100;event(w,now=2)
        with self.assertRaisesRegex(SpellRuleError,'shares'):w.kernel_plan('a')

    def test_contact_consumption_restores_without_contact_event(self):
        w,c=world();pulse(c,'garden',concentration=True);h=FirstContactLedger({'pulse':'garden'})
        attach(c,'contact',h,PULSE_SOURCES['garden'],'first-contact',identity='cure',deadline=ClockMarker(18),parent='pulse')
        capture(w);h.claim('pulse','b',event='start');event(w,now=2);w.kernel_plan('a').commit()
        self.assertEqual(h.consumed,set());self.assertEqual(c.events,{})

    def test_parent_device_without_actual_adapter_rejected(self):
        w,c=world();pulse(c,'nano-aegis')
        with self.assertRaisesRegex(SpellRuleError,'parent adapter'):capture(w)

    def test_ended_concentration_callback_still_targets_same_restored_source(self):
        w,c=world();pulse(c,'transcendent-meditation',concentration=True);capture(w)
        event(w,now=2);w.kernel_plan('a').commit();c.concentration.end('a','later end')
        self.assertNotIn('pulse',c.active)


class NativeAndReflectionTests(unittest.TestCase):
    def native(self,c):
        return attach(c,'native',NativeOccurrenceLedger(),'cleric.hero.saint.aura-of-grace','regular-heal',
                      identity='native',targets=('a',),deadline=None)

    def test_native_declined_ineligible_or_unaffordable_cannot_retry_start(self):
        for eligible,opted,rp in ((True,False,10),(False,True,10),(True,True,0)):
            with self.subTest(case=(eligible,opted,rp)):
                w,c=world();self.native(c);capture(w);w.wallets['a'].rp=rp;w.regular_start('a',1)
                self.assertFalse(c.native_occurrence(w,'native','first',eligible=eligible,opted_in=opted))
                w.wallets['a'].rp=10
                with self.assertRaisesRegex(SpellRuleError,'already evaluated'):
                    c.native_occurrence(w,'native','retry',eligible=True,opted_in=True)

    def test_native_new_iteration_can_pay_again_but_old_rp_stays_spent(self):
        w,c=world();r=self.native(c);capture(w);w.regular_start('a',1)
        self.assertTrue(c.native_occurrence(w,'native','heal-1',eligible=True,opted_in=True))
        event(w,now=2);w.kernel_plan('b').commit()
        self.assertEqual(w.wallets['a'].rp,9);self.assertEqual(len(r.holder.consumed),1)
        w.regular_start('a',3);self.assertTrue(c.native_occurrence(w,'native','heal-2',eligible=True,opted_in=True))
        self.assertEqual(w.wallets['a'].rp,8);self.assertEqual(len(r.holder.consumed),2)

    def test_native_has_no_restore_tick_and_no_late_turn_retry(self):
        w,c=world();self.native(c);capture(w);event(w,now=2);w.kernel_plan('a').commit()
        self.assertEqual(c.native_evaluations,{})
        with self.assertRaisesRegex(SpellRuleError,'regular turn'):c.native_occurrence(w,'native','fake',eligible=True,opted_in=True)
        w.regular_start('a',3);w.scheduler.begin_event('action');w.scheduler.finish_event('action')
        with self.assertRaisesRegex(SpellRuleError,'window is closed'):c.native_occurrence(w,'native','late',eligible=True,opted_in=True)

    def test_rapid_coagulation_requires_real_movement_adapter(self):
        w,c=world();r=self.native(c);r.source='warrior.supplement.rapid-coagulation'
        with self.assertRaisesRegex(SpellRuleError,'movement adapter'):capture(w)

    def test_reflection_uses_real_target_turn_and_preserves_history(self):
        w,c=world();h=PerTurnReflection(10)
        c.concentration.start_committed('a','judgment',lambda reason:None)
        attach(c,'reflection',h,'cleric.hero.priest.divine-judgment','cleric.divine-judgment.mark',concentration='judgment')
        capture(w);ta=w.regular_start('a',1)
        with self.assertRaises(SpellRuleError):c.reflect(w,'effect','off-turn',positive_damage_event=True,actual_damage_dealt=8)
        w.scheduler.regular_end(ta,1);w.regular_start('b',2)
        self.assertEqual(c.reflect(w,'effect','damage-1',positive_damage_event=True,actual_damage_dealt=8),4)
        self.assertEqual(c.reflect(w,'effect','damage-2',positive_damage_event=True,actual_damage_dealt=8),0)
        event(w,now=3);w.kernel_plan('a').commit();self.assertEqual(len(h.used_turn_ids),1)
        ta=w.regular_start('a',4);w.scheduler.regular_end(ta,4);w.regular_start('b',5)
        self.assertEqual(c.reflect(w,'effect','damage-3',positive_damage_event=True,actual_damage_dealt=8),4)
        self.assertEqual(len(h.used_turn_ids),2)


if __name__=='__main__':
    suite=unittest.TestSuite(unittest.defaultTestLoader.loadTestsFromTestCase(c) for c in
                            (ControlTransactionTests,PulseTransactionTests,NativeAndReflectionTests))
    result=unittest.TextTestRunner(verbosity=2).run(suite)
    root=Path(__file__).resolve().parents[1]
    report={'status':'PASS' if result.wasSuccessful() else 'FAIL','methods':result.testsRun,
        'failures':len(result.failures),'errors':len(result.errors),'fullTimeLoopOperational':False,
        'scope':'Live control/pulse transaction candidate; exact admitted source policies; parent/entry/mutation adapters remain',
        'hashes':{p:hashlib.sha256((root/p).read_bytes()).hexdigest() for p in
                  ('tools/temporal_playtest_rules.py','tools/temporal_control_world.py')}}
    (root/'docs/mechanics/TEMPORAL_CONTROL_WORLD_VALIDATION.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    raise SystemExit(0 if result.wasSuccessful() else 1)

```

## tools/temporal_control_playtest_rules.py

```
"""Temporal control/pulse integration under construction, not full Time Loop.

This first bridge lets the existing pulse helper spend the canonical RP, RC and
Bonus Action. It owns no second resource pool and changes no source timing.
Remaining source policies require their actual notebook conference and review.
"""
from device_lifecycle_playtest_rules import Wallet
from healing_pulse_playtest_rules import PulseSeries, PROFILES
from spell_playtest_rules import integer
from temporal_playtest_rules import Scheduler, TemporalKernel, ident, require, shape


class CanonicalPulseWallet:
    """Duck-typed spend interface used by the reviewed PulseSeries helper.

Bind once to a known host actor. Every spend verifies that its scene, scheduler,
registry and Wallet aliases still designate those same canonical objects. RC
comes from Scheduler.rc, the encounter resource explicitly restored by the
kernel; RP/used-history remain on the real Wallet. There is no local balance.
"""
    def __init__(self, kernel, actor):
        require(isinstance(kernel, TemporalKernel), 'Canonical temporal host required')
        ident(actor)
        require(actor in kernel.wallets and actor in kernel.lives, 'Canonical pulse actor required')
        self.kernel = kernel
        self.actor = actor
        self._scheduler = kernel.scheduler
        self._registry = kernel.wallets
        self._wallet = kernel.wallets[actor]
        self._validate()

    def _validate(self):
        require(self.kernel.scheduler is self._scheduler and self.kernel.wallets is self._registry
                and self._registry.get(self.actor) is self._wallet,
                'Canonical pulse binding changed')
        require(self.actor in self.kernel.lives, 'Canonical pulse actor disappeared')
        require(len({id(w) for w in self._registry.values()}) == len(self._registry),
                'Pulse actors cannot share one Wallet')
        shape(self._scheduler, Scheduler)
        shape(self._wallet, Wallet)
        integer(self._wallet.rp, 'canonical RP', 0)
        require(type(self._wallet.bonus_action) is bool, 'Canonical Bonus Action must be boolean')
        require(type(self._scheduler.rc) is dict, 'Canonical RC registry required')

    @property
    def rp(self):
        self._validate()
        return self._wallet.rp

    @property
    def rc(self):
        self._validate()
        value = self._scheduler.rc.get(self.actor, 0)
        return integer(value, 'canonical RC', 0)

    @property
    def bonus_action(self):
        self._validate()
        return self._wallet.bonus_action

    def spend(self, amount, currency='RP', *, bonus_action=False):
        self._validate()
        integer(amount, 'pulse cost', 0)
        require(currency in ('RP', 'RC'), 'Unknown pulse currency')
        require(type(bonus_action) is bool, 'Explicit Bonus Action cost required')
        balance = self.rp if currency == 'RP' else self.rc
        require(balance >= amount, 'Required pulse resource unavailable')
        require(not bonus_action or self._wallet.bonus_action, 'Required pulse Bonus Action unavailable')
        # All checks precede mutation. Reference host holds its scene/event lock.
        if currency == 'RP':
            self._wallet.rp -= amount
        elif amount:
            self._scheduler.rc[self.actor] = balance - amount
        if bonus_action:
            self._wallet.bonus_action = False


# Zero-based pulse indexes. These keys identify conserved source opportunities,
# not new resource pools. Source acquisition/parent eligibility stay with host.
INDEPENDENT_OUTPUTS = {
    'transcendent-meditation': ('monk.hero.enlightened-master.transcendent-meditation',1,'Ki'),
    'sacred-chant': ('cleric.base.sacred-chant',2,'Conviction'),
}


class ConservedPulseOutputs:
    """Guard actual resolved outputs through the existing PulseSeries method.

This is the resolution boundary only. It does not restore series, validate their
parent concentration, or authorize a due marker. The eventual temporal source
adapter must provide those. It retains one canonical series object per identity
and never grants the same instance/index resource twice, even across iterations.

Returned allowances must be applied once in the host's same atomic event to its
real resource holder with the printed cap. This guard owns no Ki or Conviction.
Missed/expired clock events still require the source-clock adapter; no method
here fabricates an occurrence from an old committed state or a supplied receipt.
"""
    def __init__(self, kernel):
        require(isinstance(kernel, TemporalKernel),'Canonical temporal host required')
        self.kernel = kernel
        self.series = {}
        self.consumed = set()
        self.events = {}

    def register(self, series, owner, source_id):
        require(type(series) is PulseSeries, 'Canonical PulseSeries required')
        require(series.profile_name in INDEPENDENT_OUTPUTS,'Unsupported independent-output source')
        expected = INDEPENDENT_OUTPUTS[series.profile_name][0]
        require(source_id == expected,'Independent-output source/profile mismatch')
        ident(series.instance_id)
        require(series.instance_id not in self.series,'Canonical pulse identity already registered')
        CanonicalPulseWallet(self.kernel,owner)
        self.series[series.instance_id] = (series,owner,source_id,series.profile_name)

    def _binding(self, instance):
        require(instance in self.series,'Unknown independent-output instance')
        series,owner,source_id,profile = self.series[instance]
        require(type(series) is PulseSeries and series.instance_id == instance
                and series.profile_name == profile and series.profile == PROFILES[profile]
                and source_id == INDEPENDENT_OUTPUTS[profile][0],
                'Independent-output canonical binding changed')
        return series,owner,profile

    def resolve(self, instance, index, now, targets, *, event_id, round_number,
                real_encounter, regular=True, upkeep_legal=True,
                whole_effect_suppressed=False):
        ident(event_id)
        require(event_id not in self.events,'Independent-output event replay')
        require(type(real_encounter) is bool and type(whole_effect_suppressed) is bool,
                'Explicit encounter and suppression state required')
        series,owner,profile = self._binding(instance)
        wallet = CanonicalPulseWallet(self.kernel,owner)
        # This call actually resolves a pending opportunity; reading a historical
        # series state or passing a copied result is not sufficient.
        result = series.resolve(index,now,targets,wallet,round_number=round_number,
            regular=regular,upkeep_legal=upkeep_legal,
            whole_effect_suppressed=whole_effect_suppressed)
        _,output_index,resource = INDEPENDENT_OUTPUTS[profile]
        key = (instance,index,resource)
        allowance = 0
        if index == output_index:
            first = key not in self.consumed
            self.consumed.add(key)  # Suppressed/capped occurrences never bank.
            allowance = int(first and not whole_effect_suppressed
                            and (profile != 'sacred-chant' or real_encounter))
        # Replace the old helper's unguarded Ki flag rather than returning two
        # independently usable authorizations for the same resource component.
        result['independentKi'] = allowance if resource == 'Ki' else 0
        result['independentConviction'] = allowance if resource == 'Conviction' else 0
        result['resourceOwner'] = owner
        result['occurrenceId'] = event_id
        result['iteration'] = self.kernel.scheduler.iteration
        self.events[event_id] = {'instance':instance,'index':index,
            'iteration':self.kernel.scheduler.iteration,'resource':resource,
            'allowance':allowance,'wholeSuppressed':whole_effect_suppressed}
        return result

```

## docs/mechanics/TEMPORAL_CONTROL_WORLD_VALIDATION.json

```
{
  "status": "PASS",
  "methods": 44,
  "failures": 0,
  "errors": 0,
  "fullTimeLoopOperational": false,
  "scope": "Live control/pulse transaction candidate; exact admitted source policies; parent/entry/mutation adapters remain",
  "hashes": {
    "tools/temporal_playtest_rules.py": "45ad6ab7d2b26baf7bc56a8377d82398781175d5a81c7562b3dedeb40f28d577",
    "tools/temporal_control_world.py": "8c5ccaa8b961c069254385a24a1ccd33864422fdc06fb8b8698fff91b4214fb9"
  }
}

```

## docs/mechanics/TEMPORAL_CONTROL_PLAYTEST.md

```
# Time Loop: control and healing-pulse integration

**Source policies discussed; implementation in progress. Full Time Loop remains unavailable.**

The [actual nine-part conference](../../../../docs/audit/2026-10-08/full-game/GPT_TEMPORAL_CONTROL_PULSE_BOUNDARIES.md) supplements the [twelve world-conservation decisions](../../../../docs/audit/2026-10-08/full-game/GPT_TEMPORAL_WORLD_BOUNDARIES.md). The existing [control](CONTROL_STATES_PLAYTEST.md) and [pulse](HEALING_PULSE_PLAYTEST.md) guides continue to own ordinary source behavior. No original card was changed.

## Agreed temporal behavior

| State | Temporal rule |
| --- | --- |
| Explicit source/target regular endpoints | Restore remaining logical progress with authentic new-iteration regular markers. World elapsed time does not move backward, and restoration creates no marker event. |
| Current actual-turn endings | Remain attached to the actual application turn. The initiative-start snapshot has no active turn; a pending in-turn attachment there is invalid. Outside-turn +6-second endpoints retain their absolute deadline. |
| Outside-origin pulse schedules | Keep their original virtual markers and absolute deadlines. Entering initiative or using Time Loop does not restart them. Origin must be recorded explicitly. |
| Speed records | Same application, exact source/component/profile and valid endpoint. Do not reapply or refresh. Current external suppression remains authoritative. Aura, net, form, serum and creature children require their actual parent adapters. Hypermutation's floor is systemic parent state, not a hostile slow. |
| Guiding Bolt's Star mark | Restore its two separate entitlements. Keep the same mark identity and monotonic attack-token history; pending attacks block capture and preflight. |
| Wrathful Brand | Restore the separate owner/ally riders and snapshot timed parent. No new damage, healing or save event occurs at restore. |
| One-shot riders | Use exact parent/application/source/component identities and a finite trigger table. Vein Cutter consumes on its qualifying attack hit; Crippling Lash specifically requires a weapon hit. Omen Reader's once/encounter attack adjustment is distinct from the resulting timed star-ash. |
| Divine Judgment reflection | Retain historical actual-turn consumption. A genuinely new iteration turn can qualify, including a separately authenticated extra turn. Ordinary repeat saves and expiry still use regular markers. |
| PulseSeries | Restore snapshot pending/funded/consumed state under the same valid parent and fixed roster. No cast pulse or consumed-at-snapshot opportunity replays. A later pending paid pulse pays its current printed cost when actually due. |
| Recipient budgets | Retain history with domain, target and iteration-round identity. Circle of Harmony remains shared across owners in the same iteration-round. |
| Eternal Bloom | Preserve the original missing-HP capture and shares. Restore only snapshot installment availability; retain old consumption history. Do not grow the reserve from later damage. Its survival floor is separate. |
| First-contact cures | Restore snapshot instance/recipient entitlements. Garden uses entry/start; Enhanced Garden and Seed use their reviewed pulse event. Restore itself is none of these events. Real-rest recipient histories remain conserved. |
| Native healing | One evaluated opportunity at a genuine regular start during a real encounter. Decline, ineligibility or unavailable payment loses that start opportunity. Extra turns and downtime create no tick. A new iteration can supply a new genuine start, with current RP/reserves. |

**Resource-output conservation:** Transcendent Meditation's second pulse can supply1Ki only once for the same effect instance. Sacred Chant's third pulse can supply1Conviction only once for that instance. Reaching the occurrence while capped or while the whole effect is suppressed still consumes that resource opportunity. Healing may later replay under an authorized restored source without generating the same resource again. A never-reached opportunity remains eligible. Restoration itself grants neither resource.

For example, a Monk receives the second pulse's1Ki, then spends it. Rewinding to a snapshot where that pulse was pending can permit its healing again when legally due, but it cannot return that same1Ki. Sacred Chant uses the same conservation rule for Conviction.

The immutable snapshot is at initiative start. A source first created afterward is not silently added to that snapshot. An origin label cannot manufacture preexisting pulse state. Any logical-clock restoration must demonstrate that the actual source instance was already present in the captured state.

The conference's maintenance wording is read with its express instruction not to reopen ordinary mechanics: an early failed ordinary turn-window payment remains pending until the source's real turn-end deadline. Exact-due paid sequences/windows end immediately on failed upkeep. The notebook explicitly [confirmed this distinction and immutable snapshot membership](../../../../docs/audit/2026-10-08/full-game/GPT_TEMPORAL_PULSE_BRIDGE_CLOSURE.md). No currently supplied pulse profile needs a fabricated at-initiative creation exception; native passive abilities instead await their future genuine regular-start events.

## Current code and checks

`tools/temporal_control_playtest_rules.py` currently implements two limited bridges:

- `CanonicalPulseWallet` lets existing pulse helpers spend the real actor Wallet's RP/Bonus Action and the canonical Scheduler's RC. It owns no duplicate balances and rejects changed aliases before spending.
- `ConservedPulseOutputs` wraps actual `PulseSeries.resolve()` calls for the two resource-producing profiles. It retains unique occurrence IDs and conserved instance/index/component opportunities; it replaces the helper's raw Ki flag with the guarded allowance. Suppressed or capped resolved occurrences cannot be banked. Sacred Chant cannot generate Conviction outside a real encounter.

The returned resource allowance must be applied once by the host in the same atomic event, subject to the actual resource cap. These helpers do not themselves own, increment or restore Ki/Conviction. Source acquisition, legal recipients, actual parent concentration and authenticated due-event scheduling remain host/source-adapter responsibilities. The output guard cannot certify them.

[Validation](TEMPORAL_CONTROL_VALIDATION.json):22 focused methods pass. They exercise the actual existing maintenance, Song, Meditation, Chant and native payment interfaces, plus duplicate output, cap, suppression, early/duplicate occurrence and canonical-alias cases. A replay test deliberately resets only an isolated series view; it demonstrates the output guard, not a complete Time Loop source restoration. The [actual independent review](../../../../docs/audit/2026-10-08/full-game/GPT_TEMPORAL_PULSE_BRIDGE_CLOSURE.md) approves only these payment/resolved-output bridges. The [review manifest](TEMPORAL_PULSE_BRIDGE_REVIEW_STATUS.json) binds that approval to the exact unchanged helper. The validation JSON retains its original submitted pre-review scope label as evidence; the separate review manifest records the later disposition.

## Still required

The new `tools/temporal_control_world.py` candidate joins actual existing effect holders to the foundation's atomic restore transaction. Its 44 integration methods pass, alongside the 76 foundation and 22 payment/output methods. **The actual notebook review returned five defects and an Oracle concentration omission; their repairs await independent confirmation.** It restores selected same-object fields, watches aliases and current concentration callbacks, preserves original outside-origin pulse clocks, and uses authenticated regular-start phases. Hemostasis uses the target's start; other admitted sequences use the source's. Bloom installments and pulse-triggered contacts require current parent occurrence receipts. Native optional healing records an evaluated start even when declined, ineligible or unaffordable.

The repaired world requires the host's existing `ConservedPulseOutputs` guard as an explicit constructor argument. It delegates resource-producing pulses to that same guard and watches its canonical bindings, consumption and event history in the restore transaction. There is no second independent-output ledger. Child operations reject a parent whose clock projection reveals missed upkeep. Capture rejects participant recipient-round claims until a real outside-round import adapter exists. Unclassified Speed suppression blocks capture/restore. Prepared plans also watch the concentration object's complete schema. Eternal Bloom and Crown Restored require concentration through the existing `oracle.engine[26]` zone rule; prepaid Final pulses do not waive that requirement.

This is still bounded component code. Exact supplied source/target schedules and source eligibility remain host inputs; original outside-initiative round-ledger import is not implemented. The new integration does not execute complete cards or apply HP/Ki/Conviction output to final life/resource holders. It admits only the explicit control policy rows and three paid native sources. Omen Reader, extra turns, movement/entry receipts, mutation reserves, shared multi-parent contact holders, device/stasis/copy parents and complete source sibling lifecycles remain unsupported. Missing or ended required concentration rejects restoration. Parent retirement/restoration beyond the existing exact callback is not implemented.

All nine-family restoration remains in progress. No supported-adapter count or ordinary catalog status has been promoted. Required work includes complete source clock/parent adapters, final resource/output application, complete shared recipient history across initiative boundaries, and the outstanding lifecycles above. [Candidate validation](TEMPORAL_CONTROL_WORLD_VALIDATION.json) is engineering evidence, not full Time Loop approval.

Rapid Coagulation additionally needs the canonical previous-turn movement baseline from the initiative snapshot. It remains unsupported until that state exists. Net Bolt, Totem/Echo, Nano-Aegis, auras and other dependent sources remain unavailable to Time Loop without their physical/device/parent adapters. The seven major integrations and final whole-game/GitHub gate remain open.

```

## Exact original Oracle source evidence

```json
[
  {
    "bindingId": "oracle.engine[26]",
    "sourceKind": "class-engine",
    "sourcePath": "data/public/class_playtests/oracle.json",
    "sourceId": 26,
    "sourceSha256": "dd6003b655e77deb78cbdc17b83837c51b1f4798eb77d546cbd9b865cdf725b2",
    "sourceProcedure": {
      "text": "Oracle zone default: choose at most three allies and three enemies for each pulse or aura benefit, fixed at activation unless the card names fewer. Persistent damaging/healing zones require concentration and at most three pulses. Pay 1 RC before each pulse after the first, or end the effect; once-per-long-rest Finals include their printed pulses in that limited use. One pulse can affect a creature only once per round. Passive personal resistance and a single-target temporary buff are not zones."
    },
    "status": "REVIEWED / reference-VALIDATED: supplied scheduling or guard/exclusion role only",
    "classification": "G/TW",
    "operationalOverrides": [
      "FIRST PROPOSAL; read later source corrections before implementing: Generic Oracle persistent-zone schedule: fixed sets, concentration, \u22643 funded windows.",
      "BOUNDARY CORRECTION controls: shared missed-maintenance termination; Song later1RC/concentration; BurningBloodV notFinal; original virtual markers; capped fixed Oracle sets; separate named/instance budgets; exact delayed final ticks. See HEALING_PULSE_PLAYTEST.md for current candidate; exact review pending.",
      "Final89-check/301-state guide controls. Exact paid due markers end immediately on illegal/unavailable upkeep; turn-window maintenance retains its deadline. EnhancedGarden replaces entry cure with first-pulse entitlement. Internal aliases add no abilities."
    ],
    "reviewEvidence": [
      "GPT_HEALING_PULSE_FIRST_REVIEW.md",
      "GPT_HEALING_PULSE_BOUNDARIES.md",
      "GPT_HEALING_PULSE_IMPLEMENTATION_FINDINGS.md",
      "GPT_HEALING_PULSE_FINAL_CLOSURE.md"
    ],
    "openIssues": [
      "Other card components, full companion commands, object lifecycle and unsupplied catalogs remain open. Each-fixed-target effects must resolve for every currently eligible fixed target."
    ]
  },
  {
    "bindingId": "oracle.supplement.flame.crown-restored",
    "sourceKind": "class-card",
    "sourcePath": "data/public/class_playtests/oracle.json",
    "sourceId": "oracle.supplement.flame.crown-restored",
    "sourceSha256": "354e4fb2b53a1b46b121c1edc36df4e364f0dbf66931fa7bdb453e68d6f3ab8f",
    "sourceProcedure": {
      "name": "Crown Restored",
      "activation": "Bonus Action",
      "cost": "0 RC",
      "rangeAndTarget": "Self and allies within 5 tiles",
      "duration": "3 rounds",
      "frequency": "1/long rest",
      "effect": "Manifest the Crown for 3 rounds. Once on each of your turns add 2 fire damage to one damaging attack or Revelation. At the start of each living ally's turn within 5 tiles, including yours, that ally regains 1d6 HP, at most three pulses per creature from this Final and never above maximum HP. Once per round you may activate one known Tier I Flame Revelation for 0 RC using its normal action type. Free Revelations cannot recursively restore additional RC beyond the normal once-per-round Prophecy Trigger cap."
    },
    "status": "REVIEWED / reference-VALIDATED: supplied scheduling or guard/exclusion role only",
    "classification": "FI/TW",
    "operationalOverrides": [
      "FIRST PROPOSAL; read later source corrections before implementing: Limited Final target-start pulses, max3/creature; no generic upkeep.",
      "BOUNDARY CORRECTION controls: shared missed-maintenance termination; Song later1RC/concentration; BurningBloodV notFinal; original virtual markers; capped fixed Oracle sets; separate named/instance budgets; exact delayed final ticks. See HEALING_PULSE_PLAYTEST.md for current candidate; exact review pending.",
      "Final89-check/301-state guide controls. Exact paid due markers end immediately on illegal/unavailable upkeep; turn-window maintenance retains its deadline. EnhancedGarden replaces entry cure with first-pulse entitlement. Internal aliases add no abilities."
    ],
    "reviewEvidence": [
      "GPT_HEALING_PULSE_FIRST_REVIEW.md",
      "GPT_HEALING_PULSE_BOUNDARIES.md",
      "GPT_HEALING_PULSE_IMPLEMENTATION_FINDINGS.md",
      "GPT_HEALING_PULSE_FINAL_CLOSURE.md"
    ],
    "openIssues": [
      "Other card components, full companion commands, object lifecycle and unsupplied catalogs remain open. Each-fixed-target effects must resolve for every currently eligible fixed target."
    ]
  },
  {
    "bindingId": "oracle.supplement.life.eternal-bloom",
    "sourceKind": "class-card",
    "sourcePath": "data/public/class_playtests/oracle.json",
    "sourceId": "oracle.supplement.life.eternal-bloom",
    "sourceSha256": "3d97cb828d42d1ec6f4f674e4328a37f916f47c15513a4e357cff80a706f7d02",
    "sourceProcedure": {
      "name": "Eternal Bloom",
      "activation": "Action",
      "cost": "0 RC",
      "rangeAndTarget": "5-tile-radius fixed sanctuary centered within 5 tiles",
      "duration": "3 rounds",
      "frequency": "1/long rest",
      "effect": "When Eternal Bloom appears, record each living ally's missing HP while it is inside the zone. Divide that recorded missing HP into three healing installments as evenly as possible, with any remainder assigned to earlier pulses. On activation and at the start of each of your next two regular turns, each qualifying ally still inside regains its next installment; later damage does not increase this reserve. Once per ally during the Bloom, when damage would reduce it to 0 HP without instant death, it remains at 1 HP instead. Allies in the zone have necrotic immunity for the 3 rounds. When the Bloom ends, petals create light obscurement in the zone until the start of your next turn. It removes no Wounds and does not resurrect."
    },
    "status": "REVIEWED / reference-VALIDATED: supplied scheduling or guard/exclusion role only",
    "classification": "FI",
    "operationalOverrides": [
      "FIRST PROPOSAL; read later source corrections before implementing: Three fixed reserve installments; activation + next2 source starts; no upkeep.",
      "BOUNDARY CORRECTION controls: shared missed-maintenance termination; Song later1RC/concentration; BurningBloodV notFinal; original virtual markers; capped fixed Oracle sets; separate named/instance budgets; exact delayed final ticks. See HEALING_PULSE_PLAYTEST.md for current candidate; exact review pending.",
      "Final89-check/301-state guide controls. Exact paid due markers end immediately on illegal/unavailable upkeep; turn-window maintenance retains its deadline. EnhancedGarden replaces entry cure with first-pulse entitlement. Internal aliases add no abilities."
    ],
    "reviewEvidence": [
      "GPT_HEALING_PULSE_FIRST_REVIEW.md",
      "GPT_HEALING_PULSE_BOUNDARIES.md",
      "GPT_HEALING_PULSE_IMPLEMENTATION_FINDINGS.md",
      "GPT_HEALING_PULSE_FINAL_CLOSURE.md"
    ],
    "openIssues": [
      "Other card components, full companion commands, object lifecycle and unsupplied catalogs remain open. Each-fixed-target effects must resolve for every currently eligible fixed target."
    ]
  }
]
```
