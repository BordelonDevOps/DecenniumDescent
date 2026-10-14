# Actual live control/pulse transaction candidate — 36 integration methods

This continues the nine-family conference and approved 22-method payment/output bridge. The original 76-method foundation is preserved byte-for-byte under its approved hash. The CURRENT foundation file has a small explicit extension below, so its old approval does not cover this current version. All 36 new + 76 foundation + 22 bridge checks pass.

Please inspect the actual code for consequential defects in this bounded integration. Give concrete counterexamples, then a bounded disposition. This is NOT a request to close full Time Loop, all control sources, complete cards, or the whole game. All seven major integrations remain counted as missing. No class/catalog status is promoted.

Implemented: canonical existing holders are joined to the original preflight/commit transaction, exact source registry, same-object restoration (frozen SpeedRecord is a value in its canonical BoundEffect), immutable source metadata, concentration alias/callback staleness, original outside-clock retirement without catch-up, current RP/RC/BA facade, iteration history, authentic regular-start windows, target-start Hemostasis, current parent pulse receipts for Bloom/contact, once-evaluated paid native starts.

Known remaining dependencies, not presented as complete: full source sibling effects (save/lifecycle/aura/floor/etc.), application-source legality/target predicates, original-clock construction, outside-initiative round-ledger import, actual final HP/Ki/Conviction application and caps, parent replacement/retirement/restoration, device/stasis/copy/physical/form parents, Omen Reader setup, extra turns, movement/entry receipts, mutation reserves, shared multi-parent FirstContactLedger. Missing supplied adapters reject explicitly where represented. A BoundEffect is the selected component's binding, not evidence that the whole source card has been executed. The host still owns action/source transactions.

All active timed sources captured at the initiative-start boundary must already exist and have outside-origin schedules. Later encounter-created sources can retire on rewind but cannot acquire snapshot membership. Native ability records are persistent preexisting capabilities; restore produces no native start.

Specific points to check: source/target start authority; candidate's recipient claimed view versus conserved iteration-round history; parent activity after missed upkeep; old event receipt reuse; preservation of original costs; stale-plan coverage; malformed source holder admission. One test fixture originally tried two Song pulses in the same numbered round; it now advances a genuine complete round before the later pulse rather than clearing the target budget. Original helper behavior was unchanged.

The real-source clock policies were settled in the preceding conference. If the implementation has a defect, identify it; if a source parent needs more actual data, distinguish that missing adapter from a new rule question. Please do not infer an approval of deferred pieces from passing checks.

## Foundation extension diff

```diff
--- reviewed-foundation
+++ current-extension
@@ -15,7 +15,7 @@
 import json
 
 from core_playtest_rules import LifeState
-from control_playtest_rules import ClockMarker, clock_marker
+from control_playtest_rules import ClockMarker, SpeedRecord, clock_marker
 from device_lifecycle_playtest_rules import Wallet
 from form_temphp_playtest_rules import BufferGrant, BufferLedger
 from healing_playtest_rules import HealingCommitLedger, SoulBind
@@ -183,14 +183,21 @@
     encounter_uses: dict = field(default_factory=dict)
     queued: dict = field(default_factory=dict)
     active_regular: TurnId | None = None
+    turn_phase: str = 'between'
 
     def round_id(self):
         return RoundId(self.encounter, self.iteration, self.round)
 
-    def begin_event(self, event_id):
+    def begin_event(self, event_id, *, phase='body'):
         ident(event_id)
         require(self.atomic_event is None and event_id not in self.completed_events,
                 'One new complete atomic event at a time')
+        require(phase in ('start','body'),'Unsupported combat event phase')
+        if phase=='start':
+            require(self.active_regular is not None and self.turn_phase=='start',
+                    'Not an authenticated regular-start event window')
+        elif self.active_regular is not None:
+            self.turn_phase='body'
         self.atomic_event = event_id
 
     def finish_event(self, event_id):
@@ -214,6 +221,7 @@
         self.debts.discard(actor)
         wallet.reaction = True
         self.active_regular = TurnId(self.encounter, self.iteration, actor, self.turn_ordinal)
+        self.turn_phase='start'
         return self.active_regular
 
     def regular_end(self, turn_id, now):
@@ -223,6 +231,7 @@
         require(marker >= self.now, 'Elapsed time never rewinds')
         self.now = marker
         self.active_regular = None
+        self.turn_phase='between'
         self.cursor += 1
         if self.cursor == len(self.initiative):
             self.cursor = 0
@@ -478,13 +487,14 @@
     captured_at: ClockMarker
     global_regular: int
     physical_baseline: dict
+    adapter_payloads: dict = field(default_factory=dict)
 
 
 DATA_TYPES = frozenset((
     ClockMarker, LifeState, MaxHpRecord, BufferGrant, SoulBind, RoundId, TurnId,
     RewardOpportunityKey, OneShot, MaximumContext, SoulRecord, SoulIdentity,
     PhysicalRecord, Pose, EnvironmentAnchor, ExternalDependency, ExternalEffect,
-    BufferPolicy, Snapshot, TemporalHistory,
+    BufferPolicy, Snapshot, TemporalHistory, SpeedRecord,
 ))
 
 
@@ -540,7 +550,8 @@
                             (self.geometry, Geometry), (self.rewards, RewardLedger),
                             (self.external, ExternalState), (self.memory, Memory), (self.history, TemporalHistory)):
             shape(holder, cls)
-        require(not self.integrations, 'Unsupported active integrations: ' + ', '.join(self.integrations))
+        for adapter in self._adapters().values():
+            adapter.validate(self)
         require(set(self.wallets) == set(self.lives) == set(self.maxima),
                 'Canonical scene registries must name the same actors, including outsiders')
         for registry in (self.wallets, self.lives, self.maxima):
@@ -568,6 +579,7 @@
         for name, minimum in (('iteration', 0), ('round', 1), ('cursor', 0), ('global_regular', 0), ('turn_ordinal', 0)):
             integer(getattr(self.scheduler, name), 'scheduler '+name, minimum)
         shape(self.scheduler.now, ClockMarker)
+        require(self.scheduler.turn_phase in ('between','start','body'),'Unclassified scheduler phase')
         for row in self.inventory.physical.values():
             shape(row, PhysicalRecord)
             require(row.kind in ('root', 'inventory', 'temporal-entity'), 'Unknown physical record kind')
@@ -621,6 +633,16 @@
                         (effect.record.application_id, effect.record.owner, effect.record.target),
                         'External maximum record identity mismatch')
 
+    def _adapters(self):
+        """Exact implemented adapter classes only; no completeness boolean."""
+        from temporal_control_world import TemporalControlWorld
+        require(type(self.integrations) is dict, 'Canonical integration registry required')
+        require(set(self.integrations) <= {'control-pulses'},
+                'Unsupported active integrations: ' + ', '.join(self.integrations))
+        for name, adapter in self.integrations.items():
+            require(type(adapter) is TemporalControlWorld, 'Unsupported control/pulse adapter type')
+        return self.integrations
+
     def _validate_one_shots(self):
         ledger = self.healing
         require(type(ledger.records) is dict, 'Canonical one-shot registry must be a dictionary')
@@ -700,7 +722,8 @@
             {a: data(self.geometry.poses[a]) for a in roster},
             {a: data(self.geometry.anchors[a]) for a in environment}, data(self.external.dependencies),
             data(self.memory.known), data(self.memory.alliances), tuple(sorted(self.lives)),
-            data(s.now), s.global_regular, data(self.inventory.physical))
+            data(s.now), s.global_regular, data(self.inventory.physical),
+            {name: adapter.capture_payload(self, roster) for name,adapter in self._adapters().items()})
         # Verify even an unchanged restoration before accepting the snapshot.
         self._geometry_plan(candidate, set())
         self._snapshot = candidate
@@ -731,7 +754,9 @@
                      'souls', 'inventory', 'geometry', 'rewards', 'external', 'memory', 'integrations', 'history'):
             tx.watch_binding(self, name)
             tx.labels[id(getattr(self, name))] = name
-        tx.watch(self, 'integrations')
+        tx.watch_registry(self.integrations)
+        for adapter in self._adapters().values():
+            adapter.watch(tx)
         for holder in (self.scheduler, self.souls, self.inventory, self.geometry,
                        self.rewards, self.external, self.memory, self.buffers, self.healing, self.history):
             tx.watch_shape(holder)
@@ -909,6 +934,7 @@
         tx.write(s, 'cursor', 0)
         tx.write(s, 'turn_ordinal', 0)
         tx.write(s, 'active_regular', None)
+        tx.write(s, 'turn_phase', 'between')
         tx.write(s, 'initiative', snap.initiative)
         tx.write(s, 'debts', s.debts | {oracle})
         tx.write(s, 'loop_uses', s.loop_uses | {(oracle, epoch)})
@@ -1036,6 +1062,9 @@
         tx.write(self.memory, 'retained', retained)
         tx.write(self.memory, 'known', known)
         tx.write(self.memory, 'perceived', {a: v for a, v in self.memory.perceived.items() if a not in snap.roster})
+        require(set(snap.adapter_payloads) == set(self.integrations), 'Temporal adapter set changed since snapshot')
+        for name,adapter in self._adapters().items():
+            adapter.stage_restore(self, tx, snap.adapter_payloads[name], snap.roster, new_iteration)
         frame = {'iterationDiscarded': s.iteration, 'iterationCreated': new_iteration,
                  'oracle': oracle, 'afterEvent': s.last_completed_event, 'atWorldMarker': s.now,
                  'changes': tx.audit_rows()}

```

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
    'transcendent-meditation','resonant-seed','garden','burning-blood-v','wound-eater-iv'))
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
    def __init__(self, scheduler, *, concentration=None):
        self.scheduler=scheduler
        self.concentration=concentration if concentration is not None else ConcentrationLedger()
        self.recipients=TemporalRecipientLedger(scheduler)
        self.records={}
        self.canonical={}
        self.active=set()
        self.events={}
        self.native_evaluations={}
        self.independent_consumed=set()

    def register(self, record):
        shape(record,BoundEffect)
        ident(record.identity)
        require(record.identity not in self.records,'Canonical control identity already registered')
        require(record.family in HOLDER_TYPES,'Unsupported temporal control family')
        require(type(record.holder) is HOLDER_TYPES[record.family],'Control holder type mismatch')
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
                'active','events','native_evaluations','independent_consumed'},'Unclassified control world state')
        require(self.scheduler is kernel.scheduler,'Control scheduler alias differs')
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
        for r in self.records.values():
            require(r.family=='native' or r.origin=='outside',
                    'No supplied active control source is created at the immutable initiative boundary')
        return {'records':{key:{'metadata':{k:data(v) for k,v in vars(r).items() if k!='holder'},
                               'fields':payload(r.holder)} for key,r in self.records.items()},
                'active':data(self.active),'recipientClaims':data(self.recipients.claimed)}

    def watch(self,tx):
        tx.labels[id(self)]='control-world'
        tx.watch_shape(self)
        for name in ('scheduler','concentration','recipients','records','canonical'):
            tx.watch_binding(self,name)
        tx.watch_registry(self.records);tx.watch_registry(self.canonical)
        for name in ('active','events','native_evaluations','independent_consumed'):tx.watch(self,name)
        tx.watch_binding(self.concentration,'current');tx.watch_registry(self.concentration.current)
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
        tx.write(self,'independent_consumed',self.independent_consumed|missed_outputs)

    def _event(self,kernel,identity,event_id):
        self.validate(kernel);ident(event_id)
        require(event_id not in self.events,'Control event replay')
        require(identity in self.active,'Control source is inactive')
        r=self.records[identity]
        require(r.deadline is None or kernel.scheduler.now<r.deadline,'Control source expired')
        parent_id=r.parent_id
        while parent_id is not None:
            parent=self.records[parent_id]
            require(parent_id in self.active and (parent.deadline is None or kernel.scheduler.now<parent.deadline),
                    'Control parent is inactive or expired')
            require(parent.family!='pulse' or parent.holder.ended_at is None,'Pulse parent ended')
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
        from temporal_control_playtest_rules import CanonicalPulseWallet, INDEPENDENT_OUTPUTS
        result=h.resolve(index,kernel.scheduler.now,targets,CanonicalPulseWallet(kernel,r.owner),
            round_number=kernel.scheduler.round,upkeep_legal=upkeep_legal,
            whole_effect_suppressed=whole_effect_suppressed)
        output=INDEPENDENT_OUTPUTS.get(h.profile_name)
        if output is not None:
            _,output_index,component=output
            key=(identity,index,component)
            allowance=0
            if index==output_index:
                allowance=int(key not in self.independent_consumed and not whole_effect_suppressed)
                self.independent_consumed.add(key)
            result['independentKi']=allowance if component=='Ki' else 0
            result['independentConviction']=allowance if component=='Conviction' else 0
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
    PulseSeries,BloomReserve,FirstContactLedger,NativeOccurrenceLedger,payload,PULSE_SOURCES)
from temporal_control_playtest_rules import CanonicalPulseWallet


def world():
    w=scene(capture=False);c=TemporalControlWorld(w.scheduler)
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
    return deepcopy((history(w),c.active,c.events,c.native_evaluations,c.independent_consumed,
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
        w=scene();c=TemporalControlWorld(w.scheduler);w.integrations['control-pulses']=c
        event(w)
        with self.assertRaisesRegex(SpellRuleError,'adapter set changed'):w.kernel_plan('a')

    def test_external_target_is_not_silently_rewound(self):
        w=scene(capture=False,outsider=True);c=TemporalControlWorld(w.scheduler);w.integrations['control-pulses']=c
        h=GuidingStarMark('a','outside',ClockMarker(30),3)
        attach(c,'guiding',h,'oracle.supplement.stars.guiding-bolt','oracle.guiding-bolt.star-mark',targets=('outside',))
        capture(w);event(w,now=2)
        with self.assertRaisesRegex(SpellRuleError,'External control'):w.kernel_plan('a')


def pulse(c,profile,*,owner='a',identity='pulse',roster=('b',),concentration=False):
    mode_kwargs={}
    from healing_pulse_playtest_rules import PROFILES
    p=PROFILES[profile]
    starts=tuple(ClockMarker(6*(i+1)) for i in range(p.count))
    if p.mode=='maintenance':mode_kwargs['maintenance_ends']=tuple(ClockMarker(5+6*i,20) for i in range(p.count))
    h=PulseSeries(identity,profile,ClockMarker(0),starts,c.recipients,
                  roster=roster if p.fixed else (),**mode_kwargs)
    if concentration:c.concentration.start_committed(owner,identity,lambda reason: c.active.discard(identity))
    r=attach(c,'pulse',h,PULSE_SOURCES[profile],profile,identity=identity,owner=owner,targets=roster,
             deadline=h.expires,concentration=identity if concentration else None)
    return r


class PulseTransactionTests(unittest.TestCase):
    def test_live_resolution_uses_real_wallet_and_authenticated_start(self):
        w,c=world();r=pulse(c,'song-of-mending',concentration=True)
        r.holder.resolve(0,ClockMarker(0),('b',),CanonicalPulseWallet(w,'a'),round_number=1)
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
        p.holder.resolve(0,ClockMarker(0),('b',),CanonicalPulseWallet(w,'a'),round_number=1)
        h.consume(0,eligible_targets=('b',));capture(w)
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

    def test_contact_pulse_needs_fresh_unsuppressed_parent_receipt(self):
        w,c=world();pulse(c,'resonant-seed',concentration=True);h=FirstContactLedger({'pulse':'resonant-seed'})
        attach(c,'contact',h,PULSE_SOURCES['resonant-seed'],'first-contact',identity='cure',deadline=ClockMarker(18),parent='pulse')
        capture(w);ta=w.regular_start('a',1);w.scheduler.regular_end(ta,1);w.regular_start('b',2)
        with self.assertRaises(SpellRuleError):c.contact(w,'cure','no-pulse','b',event='pulse')
        c.target_start(w,'pulse','seed-start','b',whole_effect_suppressed=True)
        with self.assertRaises(SpellRuleError):c.contact(w,'cure','suppressed','b',event='pulse',pulse_event='seed-start')
        self.assertEqual(h.consumed,set())

    def test_unrelated_outsider_recipient_budget_is_conserved(self):
        w=scene(capture=False,outsider=True);c=TemporalControlWorld(w.scheduler);w.integrations['control-pulses']=c
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

## docs/mechanics/TEMPORAL_CONTROL_WORLD_VALIDATION.json

```
{
  "status": "PASS",
  "methods": 36,
  "failures": 0,
  "errors": 0,
  "fullTimeLoopOperational": false,
  "scope": "Live control/pulse transaction candidate; exact admitted source policies; parent/entry/mutation adapters remain",
  "hashes": {
    "tools/temporal_playtest_rules.py": "45ad6ab7d2b26baf7bc56a8377d82398781175d5a81c7562b3dedeb40f28d577",
    "tools/temporal_control_world.py": "22940d643cf51c4694c50d7652728db2521c47b3051dcf345e42984307ee1eba"
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

The new `tools/temporal_control_world.py` candidate joins actual existing effect holders to the foundation's atomic restore transaction. Its 36 integration methods pass, alongside the 76 foundation and 22 payment/output methods. **This candidate awaits actual notebook review.** It restores selected same-object fields, watches aliases and current concentration callbacks, preserves original outside-origin pulse clocks, and uses authenticated regular-start phases. Hemostasis uses the target's start; other admitted sequences use the source's. Bloom installments and pulse-triggered contacts require current parent occurrence receipts. Native optional healing records an evaluated start even when declined, ineligible or unaffordable.

This is still bounded component code. Exact supplied source/target schedules and source eligibility remain host inputs; original outside-initiative round-ledger import is not implemented. The new integration does not execute complete cards or apply HP/Ki/Conviction output to final life/resource holders. It admits only the explicit control policy rows and three paid native sources. Omen Reader, extra turns, movement/entry receipts, mutation reserves, shared multi-parent contact holders, device/stasis/copy parents and complete source sibling lifecycles remain unsupported. Missing or ended required concentration rejects restoration. Parent retirement/restoration beyond the existing exact callback is not implemented.

All nine-family restoration remains in progress. No supported-adapter count or ordinary catalog status has been promoted. Required work includes complete source clock/parent adapters, final resource/output application, complete shared recipient history across initiative boundaries, and the outstanding lifecycles above. [Candidate validation](TEMPORAL_CONTROL_WORLD_VALIDATION.json) is engineering evidence, not full Time Loop approval.

Rapid Coagulation additionally needs the canonical previous-turn movement baseline from the initiative snapshot. It remains unsupported until that state exists. Net Bolt, Totem/Echo, Nano-Aegis, auras and other dependent sources remain unavailable to Time Loop without their physical/device/parent adapters. The seven major integrations and final whole-game/GitHub gate remain open.

```
