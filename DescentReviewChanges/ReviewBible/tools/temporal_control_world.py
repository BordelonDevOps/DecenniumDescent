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
COMPONENTS={'bloom':'installments','contact':'first-contact','native':'regular-heal'}
COLLECTION_FIELDS={
    'guiding':{'_pending':set},'reflection':{'used_turn_ids':set},
    'pulse':{'states':list,'declarations':dict,'applications':set,'roster':tuple,
             'future_starts':tuple,'maintenance_ends':tuple,'opens':tuple},
    'bloom':{'roster_missing':dict,'shares':dict,'consumed':set},
    'contact':{'profiles':dict,'consumed':set},'native':{'consumed':set},
}
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
        # Retain actual slot/callback references so snapshot identity tokens
        # cannot be recycled after a slot is detached or replaced.
        self.concentration_pins={}
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
        if record.concentration_id is not None:
            slot=self.concentration.current.get(record.owner)
            require(type(slot) is tuple and len(slot)==2 and slot[0]==record.concentration_id
                    and callable(slot[1]),'Register actual concentration before its component')
            self.concentration_pins[id(slot)]=slot
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
        for name,kind in COLLECTION_FIELDS.get(record.family,{}).items():
            require(type(getattr(h,name)) is kind,'Malformed control holder collection: '+name)
        for name in ('active','available','suppressed','attack_bonus_available','hit_rider_available',
                     'owner_rider_available','ally_rider_available','slowed_hook'):
            if hasattr(h,name):require(type(getattr(h,name)) is bool,'Malformed control Boolean: '+name)
        if record.family in COMPONENTS:
            require(record.component==COMPONENTS[record.family],'Exact temporal component policy missing')
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
            require(record.component==h.profile_name,'Exact temporal pulse component policy missing')
            require(h.instance_id==record.identity and PULSE_SOURCES.get(h.profile_name)==record.source,
                    'Pulse source/profile/application mismatch')
            require(h.profile is PROFILES[h.profile_name] and h.ledger is self.recipients,
                    'Pulse must use its canonical profile and shared recipient ledger')
            require(h.profile_name not in PARENT_PROFILES,'Full device/stasis/copy parent adapter required')
            require(h.expires==record.deadline,'Pulse deadline identity mismatch')
            require(len(h.states)==h.profile.count and set(h.states)<=
                    {'pending','funded','committed','lost','closed'},'Malformed pulse opportunity state')
            require(h.profile.mode=='window' or not {'funded','closed'}&set(h.states),
                    'Pulse opportunity state belongs to another mode')
            require(h.ended_at is None or type(h.ended_at) is ClockMarker,'Malformed pulse end marker')
            require((h.ended_at is None)==(h.ended_reason is None),'Pulse ending fields disagree')
            if h.ended_reason is not None:ident(h.ended_reason)
            for index,targets in h.declarations.items():
                integer(index,'declared pulse index',0,h.profile.count-1)
                require(type(targets) is tuple and set(targets)<=set(record.targets)
                        and len(targets)==len(set(targets)) and h.states[index]=='committed',
                        'Malformed pulse declaration')
            for application in h.applications:
                require(type(application) is tuple and len(application)==2 and h.profile.mode=='window',
                        'Malformed pulse application')
                integer(application[0],'pulse application index',0,h.profile.count-1)
                require(application[1] in record.targets,'Unknown pulse application recipient')
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
            require(self.concentration_pins.get(id(current)) is current,
                    'Current concentration binding identity was replaced')
        if record.parent_id is not None:
            require(record.parent_id!=record.identity and record.parent_id in self.records,'Missing/cyclic parent')

    def validate(self,kernel):
        require(set(vars(self))=={'scheduler','concentration','recipients','records','canonical',
                'active','events','native_evaluations','outputs','concentration_pins'},'Unclassified control world state')
        require(self.scheduler is kernel.scheduler,'Control scheduler alias differs')
        for name,kind in (('records',dict),('canonical',dict),('active',set),('events',dict),('native_evaluations',dict)):
            require(type(getattr(self,name)) is kind,'Malformed control world collection: '+name)
        require(type(self.outputs) is ConservedPulseOutputs and self.outputs.kernel is kernel
                and set(vars(self.outputs))=={'kernel','series','consumed','events'},
                'Canonical independent-output guard/schema required')
        require(type(self.outputs.series) is dict and type(self.outputs.consumed) is set
                and type(self.outputs.events) is dict,'Malformed independent-output collections')
        expected_outputs={key for key,r in self.records.items() if r.family=='pulse'
                          and r.holder.profile_name in INDEPENDENT_OUTPUTS}
        require(set(self.outputs.series)==expected_outputs,'Undisclosed independent-output source')
        for key in expected_outputs:
            h,owner,_=self.outputs._binding(key)
            require(h is self.records[key].holder and owner==self.records[key].owner,
                    'Independent-output guard and live world must share canonical holders')
        require(type(self.concentration) is ConcentrationLedger and set(vars(self.concentration))=={'current'},
                'Canonical concentration ledger required')
        require(type(self.concentration.current) is dict,'Malformed concentration registry')
        require(type(self.concentration_pins) is dict,'Malformed concentration identity pins')
        for token,slot in self.concentration_pins.items():
            require(token==id(slot) and type(slot) is tuple and len(slot)==2 and callable(slot[1]),
                    'Malformed retained concentration identity')
        for owner,slot in self.concentration.current.items():
            ident(owner)
            require(type(slot) is tuple and len(slot)==2 and callable(slot[1]),'Malformed concentration slot')
            ident(slot[0])
        require(type(self.recipients) is TemporalRecipientLedger and self.recipients.scheduler is kernel.scheduler,
                'Canonical temporal recipient ledger required')
        require(set(vars(self.recipients))=={'claimed','scheduler','history'},'Recipient schema changed')
        require(type(self.recipients.claimed) is set and type(self.recipients.history) is set,
                'Malformed recipient collections')
        for claim in self.recipients.claimed:
            require(type(claim) is tuple and len(claim)==3,'Malformed active recipient claim')
            ident(claim[0]);ident(claim[1]);integer(claim[2],'recipient round',1)
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
            if r.family=='pulse' and r.identity in self.active:
                require(r.holder.activation<=kernel.scheduler.now,'Pulse did not exist at initiative snapshot')
                require(r.deadline is None or kernel.scheduler.now<r.deadline,'Pulse expired before snapshot')
                projected=plain_clone(r.holder,payload(r.holder));projected.advance(kernel.scheduler.now)
                require(projected.ended_at is None,'Pulse already ended or missed upkeep before snapshot')
        return {'records':{key:{'metadata':{k:data(v) for k,v in vars(r).items() if k!='holder'},
                               'fields':payload(r.holder)} for key,r in self.records.items()},
                'active':data(self.active),'recipientClaims':data(self.recipients.claimed),
                'concentrationBindings':{key:(r.owner,r.concentration_id,
                    id(self.concentration.current[r.owner]),id(self.concentration.current[r.owner][1]))
                    for key,r in self.records.items() if key in self.active and r.concentration_id is not None}}

    def watch(self,tx):
        tx.labels[id(self)]='control-world'
        tx.watch_shape(self)
        for name in ('scheduler','concentration','recipients','records','canonical','outputs'):
            tx.watch_binding(self,name)
        tx.watch_registry(self.records);tx.watch_registry(self.canonical)
        for name in ('active','events','native_evaluations'):tx.watch(self,name)
        tx.watch_shape(self.concentration)
        tx.watch_binding(self.concentration,'current');tx.watch_registry(self.concentration.current)
        tx.watch_binding(self,'concentration_pins');tx.watch_registry(self.concentration_pins)
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
        for key,(owner,concentration_id,slot_token,callback_token) in saved['concentrationBindings'].items():
            current=self.concentration.current.get(owner)
            require(current is not None and current[0]==concentration_id and id(current)==slot_token
                    and id(current[1])==callback_token and self.concentration_pins.get(slot_token) is current,
                    'Snapshot concentration binding identity changed; parent adapter required')
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
            if r.family=='bloom':
                parent=self.records[r.parent_id].holder
                candidate['consumed']|={i for i,at in enumerate(parent.opens) if at<now}
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
        candidate=plain_clone(r.holder,payload(r.holder))
        candidate.consumed|={i for i,at in enumerate(parent.opens) if at<kernel.scheduler.now}
        result=candidate.consume(index,eligible_targets=eligible_targets)
        r.holder.consumed=candidate.consumed
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
