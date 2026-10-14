"""Candidate Time Loop transaction kernel; NOT a complete/approved Time Loop.

The twelve notebook decisions are in GPT_TEMPORAL_WORLD_BOUNDARIES.md. This
module implements bounded foundational adapters, not the seven outstanding
lifecycle/form/control integrations. No ordinary class overlay enables it.

Input is the canonical host scene, including outsiders. Existing LifeState,
Wallet, BufferLedger and HealingCommitLedger identities are retained. A plan
contains explicit field writes, never a deepcopy of the live object graph or
arbitrary callbacks. Unknown fields and unsupported state stop preflight.
"""
from copy import deepcopy
from dataclasses import dataclass, field, fields, replace
from fractions import Fraction
import json

from core_playtest_rules import LifeState
from control_playtest_rules import ClockMarker, SpeedRecord, clock_marker
from device_lifecycle_playtest_rules import Wallet
from form_temphp_playtest_rules import BufferGrant, BufferLedger
from healing_playtest_rules import HealingCommitLedger, SoulBind
from maximum_hp_playtest_rules import MaxHpRecord, effective_maximum
from spell_playtest_rules import SpellRuleError, integer

SOURCE = 'oracle.supplement.spiral-touched.spiral-touched-boon-v'
STATUS = 'CANDIDATE / foundational adapters only / independent review pending'
REQUIRED_ADAPTERS = (
    'scheduler', 'core-life', 'buffers', 'one-shot-healing', 'soul-identity',
    'transformations', 'druid', 'creatures', 'devices', 'remaining-lifecycle',
    'feats', 'control-pulses', 'inventory-provenance', 'geometry', 'rewards',
    'external-dependencies', 'memory',
)
IMPLEMENTED_ADAPTERS = frozenset((
    'scheduler', 'core-life', 'buffers', 'one-shot-healing', 'soul-identity',
    'inventory-provenance', 'geometry', 'rewards', 'external-dependencies',
    'memory',
))


def require(ok, message):
    if not ok:
        raise SpellRuleError(message)


def ident(value):
    require(isinstance(value, str) and bool(value), 'Nonempty canonical ID required')
    return value


def shape(value, cls):
    """No subclass/extra dynamic field may silently enter an accepted adapter."""
    require(type(value) is cls, 'Unsupported holder type: ' + type(value).__name__)
    require(set(vars(value)) == {f.name for f in fields(cls)},
            'Unclassified fields on ' + cls.__name__)


def data(value):
    """Copy only explicit data leaves; forbid cross-world aliases/callbacks."""
    if value is None or type(value) in (str, int, bool, Fraction):
        return value
    if type(value) in (tuple, list, set, frozenset):
        return type(value)(data(x) for x in value)
    if type(value) is dict:
        return {data(k): data(v) for k, v in value.items()}
    if type(value) in DATA_TYPES:
        shape(value, type(value))
        # Reconstruct typed data, never copy a world/controller/callback.
        return type(value)(**{f.name: data(getattr(value, f.name)) for f in fields(value)})
    raise SpellRuleError('Unclassified temporal payload: ' + type(value).__name__)


@dataclass
class FieldWrite:
    holder: object
    name: str
    before: object
    after: object


class Transaction:
    """Single-thread reference compare-and-swap; no callbacks during commit.

    Host must hold its scene lock from preflight through commit. Every watched
    attribute is rechecked so a rest, inventory change or combat event makes a
    prepared plan stale. Container contents are replaced, holder identities stay.
    """
    def __init__(self):
        self.watches = {}
        self.writes = {}
        self.shapes = []
        self.bindings = []
        self.registries = []
        self.labels = {}
        self.used = False

    def watch_shape(self, holder):
        self.shapes.append((holder, type(holder), frozenset(vars(holder))))

    def watch_binding(self, holder, name):
        self.bindings.append((holder, name, getattr(holder, name)))

    def watch_registry(self, registry):
        self.registries.append((registry, {k: id(v) for k, v in registry.items()}))

    def watch(self, holder, name):
        key = id(holder), name
        if key not in self.watches:
            self.watches[key] = holder, name, data(getattr(holder, name))
        return data(self.watches[key][2])

    def write(self, holder, name, after):
        key = id(holder), name
        require(key not in self.writes, 'Conflicting adapters write the same field')
        before = self.watch(holder, name)
        self.writes[key] = FieldWrite(holder, name, before, data(after))

    def audit_rows(self):
        return tuple({'holder': self.labels[id(v.holder)], 'field': v.name,
                      'before': data(v.before), 'after': data(v.after)} for v in self.writes.values())

    def commit(self):
        require(not self.used, 'Temporal transaction already committed')
        for holder, kind, keys in self.shapes:
            require(type(holder) is kind and frozenset(vars(holder)) == keys, 'Temporal holder schema changed')
        for holder, name, bound in self.bindings:
            require(getattr(holder, name) is bound, 'Canonical temporal binding changed')
        for registry, before in self.registries:
            require({k: id(v) for k, v in registry.items()} == before, 'Canonical actor registry changed')
        for holder, name, before in self.watches.values():
            require(data(getattr(holder, name)) == before, 'Stale temporal plan; re-run preflight')
        applied = []
        try:
            for change in self.writes.values():
                # Only exact known, ordinary Python data holders are writable.
                setattr(change.holder, change.name, data(change.after))
                applied.append(change)
        except Exception:
            for change in reversed(applied):
                setattr(change.holder, change.name, data(change.before))
            raise
        self.used = True


@dataclass(frozen=True)
class RoundId:
    encounter: str
    iteration: int
    number: int

    def token(self):
        return json.dumps([self.encounter, self.iteration, self.number], separators=(',', ':'))


@dataclass(frozen=True)
class TurnId:
    encounter: str
    iteration: int
    actor: str
    ordinal: int
    kind: str = 'regular'

    def token(self):
        return json.dumps([self.encounter, self.iteration, self.actor, self.ordinal, self.kind],
                          separators=(',', ':'))


@dataclass
class Scheduler:
    encounter: str
    initiative: tuple
    iteration: int = 0
    round: int = 1
    cursor: int = 0
    now: ClockMarker = field(default_factory=lambda: ClockMarker(0))
    global_regular: int = 0
    turn_ordinal: int = 0
    atomic_event: str | None = None
    last_completed_event: str | None = None
    completed_events: set = field(default_factory=set)
    debts: set = field(default_factory=set)
    loop_uses: set = field(default_factory=set)
    rc: dict = field(default_factory=dict)
    encounter_uses: dict = field(default_factory=dict)
    queued: dict = field(default_factory=dict)
    active_regular: TurnId | None = None
    turn_phase: str = 'between'

    def round_id(self):
        return RoundId(self.encounter, self.iteration, self.round)

    def begin_event(self, event_id, *, phase='body'):
        ident(event_id)
        require(self.atomic_event is None and event_id not in self.completed_events,
                'One new complete atomic event at a time')
        require(phase in ('start','body'),'Unsupported combat event phase')
        if phase=='start':
            require(self.active_regular is not None and self.turn_phase=='start',
                    'Not an authenticated regular-start event window')
        elif self.active_regular is not None:
            self.turn_phase='body'
        self.atomic_event = event_id

    def finish_event(self, event_id):
        require(self.atomic_event == event_id, 'Finish the current event completely')
        self.atomic_event = None
        self.last_completed_event = event_id
        self.completed_events.add(event_id)

    def _regular_start(self, actor, wallet, now):
        """Internal mutation; public callers use TemporalKernel.regular_start."""
        shape(wallet, Wallet)
        require(self.atomic_event is None and self.active_regular is None,
                'Regular turn already active or atomic event unresolved')
        require(0 <= self.cursor < len(self.initiative) and actor == self.initiative[self.cursor],
                'Actor is not next at the canonical initiative cursor')
        marker = clock_marker(now)
        require(marker >= self.now, 'Elapsed time never rewinds')
        self.now = marker
        self.global_regular += 1
        self.turn_ordinal += 1
        self.debts.discard(actor)
        wallet.reaction = True
        self.active_regular = TurnId(self.encounter, self.iteration, actor, self.turn_ordinal)
        self.turn_phase='start'
        return self.active_regular

    def regular_end(self, turn_id, now):
        require(self.atomic_event is None and self.active_regular == turn_id and turn_id is not None,
                'Only the actual active regular turn may end')
        marker = clock_marker(now)
        require(marker >= self.now, 'Elapsed time never rewinds')
        self.now = marker
        self.active_regular = None
        self.turn_phase='between'
        self.cursor += 1
        if self.cursor == len(self.initiative):
            self.cursor = 0
            self.round += 1


@dataclass(frozen=True)
class RewardOpportunityKey:
    encounter_origin: str
    source: str
    kind: str
    slot: str


@dataclass
class RewardLedger:
    opportunities: set = field(default_factory=set)
    claims: dict = field(default_factory=dict)

    def claim(self, opportunity, claim_event):
        shape(opportunity, RewardOpportunityKey)
        ident(claim_event)
        require(opportunity in self.opportunities, 'No source-authorized reward opportunity')
        require(opportunity not in self.claims, 'Reward opportunity already claimed in world history')
        require(claim_event not in self.claims.values(), 'Reward claim event already used')
        self.claims[opportunity] = claim_event


@dataclass(frozen=True)
class OneShot:
    effect_id: str
    source_id: str
    owner: str
    target: str
    available: bool
    expires: ClockMarker | None = None
    rest_epoch: int | None = None


class TemporalHealingCommitLedger(HealingCommitLedger):
    """Canonical IDs returned to FeatWorld; generation tokens stay in history.

    Instantiate this as the world's ONE HealingCommitLedger before registering
    effects; pass that same instance to FeatWorld. Existing reviewed helpers call
    commit() normally. No deletion of historical event or consumption evidence.
    The active one-shot registry is explicit; unsupported source IDs are rejected.
    """
    def __init__(self):
        super().__init__()
        self.iteration = 0
        self.records = {}
        self.consumption_history = set()

    def register(self, record):
        shape(record, OneShot)
        require(record.source_id == 'feat:soul_cage:agony', 'One-shot source adapter still required')
        require(record.expires is not None and record.rest_epoch is None, 'Agony has only its absolute original deadline')
        require(type(record.available) is bool, 'One-shot availability must be boolean')
        for value in (record.effect_id, record.owner, record.target):
            ident(value)
        require(record.effect_id not in self.records, 'Canonical effect already registered')
        self.records[record.effect_id] = data(record)

    def commit(self, event_id, packet):
        ident(event_id)
        require(event_id not in self.committed_event_ids, 'Healing event already committed')
        canonical = set(packet['nextHealingCandidates'])
        require(canonical <= self.records.keys(), 'Unregistered one-shot source in healing packet')
        require(all(self.records[x].available for x in canonical), 'One-shot already consumed in this iteration')
        tokens = {(x, self.iteration) for x in canonical}
        require(not tokens & self.consumed_reducer_ids, 'Temporal consumption replay')
        self.committed_event_ids.add(event_id)
        self.consumed_reducer_ids.update(tokens)
        self.consumption_history.update((x, self.iteration, event_id) for x in canonical)
        for x in canonical:
            self.records[x] = replace(self.records[x], available=False)
        return canonical


@dataclass
class MaximumContext:
    # Recomputed by the host from CURRENT legal progression and equipment.
    base: int
    records: tuple = ()
    expedition: int = 0
    exhaustion: int = 0
    progression_signature: tuple = ()


@dataclass(frozen=True)
class SoulRecord:
    application_id: str
    owner: str
    target: str
    bind: SoulBind
    death_instance: str | None = None


@dataclass
class SoulIdentity:
    binds: dict = field(default_factory=dict)
    deaths: dict = field(default_factory=dict)
    living: set = field(default_factory=set)
    remains: dict = field(default_factory=dict)
    return_history: set = field(default_factory=set)
    resolved_stable: set = field(default_factory=set)
    stable_event_ids: dict = field(default_factory=dict)


@dataclass(frozen=True)
class PhysicalRecord:
    identity: str
    kind: str  # inventory, temporal-entity, root
    owner: str | None
    roots: tuple = ()
    created_iteration: int = -1
    survives: bool = True
    source_owner: str | None = None
    external_binding: str | None = None
    persistent_enrollment: str | None = None


@dataclass
class Inventory:
    physical: dict = field(default_factory=dict)
    # Quantity/stock/history never restore. Each discrete transferable item also
    # has a PhysicalRecord so derivatives cannot hide behind a stack quantity.
    quantities: dict = field(default_factory=dict)
    expenditure_events: set = field(default_factory=set)


@dataclass(frozen=True)
class Pose:
    anchor: tuple
    offsets: frozenset = frozenset({(0, 0)})

    def cells(self):
        require(len(self.anchor) == 2 and all(type(x) is int for x in self.anchor), '2D integer anchor required')
        require(bool(self.offsets) and (0, 0) in self.offsets, 'Nonempty anchor footprint required')
        require(all(len(v) == 2 and all(type(n) is int for n in v) for v in self.offsets),
                'Explicit integer footprint offsets required')
        return frozenset((self.anchor[0] + x, self.anchor[1] + y) for x, y in self.offsets)


@dataclass(frozen=True)
class EnvironmentAnchor:
    identity: str
    blocked: frozenset = frozenset()
    support: frozenset = frozenset()


@dataclass
class Geometry:
    cells: frozenset
    fixed_support: frozenset
    poses: dict = field(default_factory=dict)
    anchors: dict = field(default_factory=dict)
    # This bounded adapter supports a finite orthogonal level ground plane.
    # Flying/elevation/portals/forced growth require additional reviewed adapters.
    movement_model: str = 'finite-level-ground'


@dataclass(frozen=True)
class ExternalDependency:
    effect_id: str
    target: str
    caster: str
    concentration_id: str


@dataclass(frozen=True)
class ExternalEffect:
    identity: str
    owner: str
    target: str
    kind: str
    record: MaxHpRecord | None = None


@dataclass
class ExternalState:
    # Values are exact current concentration IDs projected from the canonical
    # ledger. A live callback bridge is still part of the transformation adapter.
    concentration: dict = field(default_factory=dict)
    dependencies: tuple = ()
    effects: dict = field(default_factory=dict)


@dataclass
class Memory:
    known: dict = field(default_factory=dict)
    perceived: dict = field(default_factory=dict)
    retained: dict = field(default_factory=dict)
    alliances: dict = field(default_factory=dict)


@dataclass
class TemporalHistory:
    # Director/engine audit only. Never passed to character memory.
    frames: tuple = ()


@dataclass(frozen=True)
class BufferPolicy:
    source: str
    lifetime: str


# Explicit reviewed time policies, never inferred from a numeric duration.
BUFFER_POLICIES = {
    'feat:chef': BufferPolicy('feat:chef', 'rest'),
    'feat:inspiring_leader': BufferPolicy('feat:inspiring_leader', 'rest'),
    'feat:field_medic': BufferPolicy('feat:field_medic', 'rest'),
    'feat:soul_cage': BufferPolicy('feat:soul_cage', 'rest'),
    'feat:empowered_summoning': BufferPolicy('feat:empowered_summoning', 'rest-entity'),
    'feat:blood_ritual': BufferPolicy('feat:blood_ritual', 'blood-self-or-ally'),
}


MAXIMUM_POLICIES = {
    'monk.hero.iron-fist-master.ribcrusher-strike': 'snapshot-trauma',
    'monk.hero.iron-fist-master.bone-breaking-strike': 'snapshot-trauma',
    'monk.hero.way-of-shadow.deathless-silence': 'snapshot-trauma',
    'feat:tough': 'conserved-progression',
    'feat:tough_as_nails': 'conserved-progression',
    'feat:tenacity': 'conserved-progression',
    'feat:dark_fortitude': 'conserved-progression',
}


@dataclass(frozen=True)
class Snapshot:
    encounter: str
    roster: frozenset
    environment: frozenset
    initiative: tuple
    wallets: dict
    rc: dict
    encounter_uses: dict
    life: dict
    maxima: dict
    grants: dict
    active_grants: dict
    one_shots: dict
    souls: SoulIdentity
    physical_ids: frozenset
    poses: dict
    anchors: dict
    dependencies: tuple
    known: dict
    alliances: dict
    manifest: tuple
    captured_at: ClockMarker
    global_regular: int
    physical_baseline: dict
    adapter_payloads: dict = field(default_factory=dict)


DATA_TYPES = frozenset((
    ClockMarker, LifeState, MaxHpRecord, BufferGrant, SoulBind, RoundId, TurnId,
    RewardOpportunityKey, OneShot, MaximumContext, SoulRecord, SoulIdentity,
    PhysicalRecord, Pose, EnvironmentAnchor, ExternalDependency, ExternalEffect,
    BufferPolicy, Snapshot, TemporalHistory, SpeedRecord,
))


class TemporalKernel:
    """Development kernel. Full Time Loop activation remains unimplemented.

    Call capture() exactly at initiative start. Roster/environment freeze once.
    kernel_plan() is for admitted development fixtures only. Host must disclose
    every active holder through integrations; unimplemented holders reject.
    playable_plan() is intentionally gated until all seventeen adapters exist.
    """
    def __init__(self, scheduler, wallets, lives, maxima, *, buffers=None,
                 healing=None, souls=None, inventory=None, geometry=None,
                 rewards=None, external=None, memory=None, integrations=None, history=None):
        self.scheduler = scheduler
        self.wallets = wallets
        self.lives = lives
        self.maxima = maxima
        self.buffers = buffers if buffers is not None else BufferLedger()
        self.healing = healing if healing is not None else TemporalHealingCommitLedger()
        self.souls = souls if souls is not None else SoulIdentity()
        self.inventory = inventory if inventory is not None else Inventory()
        self.geometry = geometry
        self.rewards = rewards if rewards is not None else RewardLedger()
        self.external = external if external is not None else ExternalState()
        self.memory = memory if memory is not None else Memory()
        self.integrations = integrations if integrations is not None else {}
        self.history = history if history is not None else TemporalHistory()
        self._snapshot = None

    def support_report(self):
        return {'status': STATUS, 'implemented': sorted(IMPLEMENTED_ADAPTERS),
                'missing': sorted(set(REQUIRED_ADAPTERS) - IMPLEMENTED_ADAPTERS),
                'fullTimeLoopOperational': False}

    def playable_plan(self, oracle):
        raise SpellRuleError('Full Time Loop unavailable: seven source integrations and independent review remain')

    def regular_start(self, actor, now):
        """The public boundary obtains the actor's canonical wallet itself.

        No wallet argument is accepted. The underscore scheduler mutator is an
        internal implementation detail, not another public event-entry API.
        """
        require(actor in self.wallets, 'No canonical wallet for the actor')
        require(len({id(v) for v in self.wallets.values()}) == len(self.wallets),
                'Distinct actors cannot alias the same canonical wallet')
        return self.scheduler._regular_start(actor, self.wallets[actor], now)

    def _validate_holders(self):
        shape(self.scheduler, Scheduler)
        for holder, cls in ((self.souls, SoulIdentity), (self.inventory, Inventory),
                            (self.geometry, Geometry), (self.rewards, RewardLedger),
                            (self.external, ExternalState), (self.memory, Memory), (self.history, TemporalHistory)):
            shape(holder, cls)
        for adapter in self._adapters().values():
            adapter.validate(self)
        require(set(self.wallets) == set(self.lives) == set(self.maxima),
                'Canonical scene registries must name the same actors, including outsiders')
        for registry in (self.wallets, self.lives, self.maxima):
            require(len({id(v) for v in registry.values()}) == len(registry),
                    'Distinct actors cannot alias one canonical holder')
        for actor in self.lives:
            ident(actor)
            shape(self.lives[actor], LifeState)
            shape(self.wallets[actor], Wallet)
            shape(self.maxima[actor], MaximumContext)
        require(type(self.buffers) is BufferLedger, 'One canonical BufferLedger required')
        required = {'grants', 'active', 'rest_epochs', 'damage_events', 'absorptions', 'form_instances', 'spell_anatomies'}
        actual = set(vars(self.buffers))
        require(required <= actual <= required | {'ordinary_cast_events'},
                'Unclassified or missing required BufferLedger field')
        require(not self.buffers.form_instances and not self.buffers.spell_anatomies,
                'Form/transformation adapter required')
        require(all(p['finished'] for p in self.buffers.absorptions.values()), 'Mid-packet buffer absorption')
        require(type(self.healing) is TemporalHealingCommitLedger, 'One canonical temporal healing ledger required')
        require(set(vars(self.healing)) == {'iteration', 'records', 'consumption_history',
                    'committed_event_ids', 'consumed_reducer_ids'}, 'Unclassified healing ledger state')
        require(self.healing.iteration == self.scheduler.iteration, 'Healing/scheduler iteration mismatch')
        self._validate_one_shots()
        require(self.geometry.movement_model == 'finite-level-ground', 'Geometry source adapter required')
        for name, minimum in (('iteration', 0), ('round', 1), ('cursor', 0), ('global_regular', 0), ('turn_ordinal', 0)):
            integer(getattr(self.scheduler, name), 'scheduler '+name, minimum)
        shape(self.scheduler.now, ClockMarker)
        require(self.scheduler.turn_phase in ('between','start','body'),'Unclassified scheduler phase')
        for row in self.inventory.physical.values():
            shape(row, PhysicalRecord)
            require(row.kind in ('root', 'inventory', 'temporal-entity'), 'Unknown physical record kind')
        require(all(a in self.lives for a in self.buffers.active), 'Unclassified shield target body')
        active_ids = tuple(self.buffers.active.values())
        require(len(active_ids) == len(set(active_ids)), 'One shield grant cannot be active for multiple targets')
        for key, grant in self.buffers.grants.items():
            shape(grant, BufferGrant)
            require(key == grant.grant_id, 'Buffer grant identity mismatch')
            if grant.state == 'active':
                require(self.buffers.active.get(grant.target) == key and grant.remaining > 0,
                        'Active grant missing from the canonical target map')
        for target, grant_id in self.buffers.active.items():
            grant = self.buffers.grants.get(grant_id)
            require(grant is not None and grant.target == target and grant.state == 'active' and grant.remaining > 0,
                    'Malformed active shield target/state/amount')
        for key, anchor in self.geometry.anchors.items():
            shape(anchor, EnvironmentAnchor)
            physical = self.inventory.physical.get(key)
            require(key == anchor.identity and physical is not None and physical.identity == key,
                    'Environment anchor lacks its exact physical identity')
            require(physical.kind in ('root', 'temporal-entity'), 'Nonphysical hazard/transferable anchor needs an adapter')
            require(physical.survives or not (anchor.blocked or anchor.support),
                    'Destroyed environment anchor still contributes geometry')
        for key, record in self.souls.binds.items():
            shape(record, SoulRecord)
            shape(record.bind, SoulBind)
            require(key == record.application_id and record.bind.identity == record.target,
                    'Soul Bind application/target identity mismatch')
            require(record.target in self.lives, 'Soul Bind target is not a canonical scene body')
            if self.scheduler.now.seconds >= record.bind.expires:
                continue  # Expired audit record is inactive and will not restore.
            life = self.lives[record.target]
            if record.bind.stage == 'pending':
                require(record.target in self.souls.living and life.hp == 0 and not life.stable
                        and not life.dead and record.death_instance is None,
                        'Pending Soul Bind requires a living dying zero-HP target')
            else:
                require(life.dead and record.death_instance is not None
                        and self.souls.deaths.get(record.target) == record.death_instance,
                        'Bound Soul Bind requires the exact current dead instance')
        for context in self.maxima.values():
            for record in context.records:
                self._maximum_policy(record)
        for key, effect in self.external.effects.items():
            shape(effect, ExternalEffect)
            require(key == effect.identity, 'External effect dictionary/application identity mismatch')
            if effect.kind == 'maximum-hp':
                shape(effect.record, MaxHpRecord)
                require((key, effect.owner, effect.target) ==
                        (effect.record.application_id, effect.record.owner, effect.record.target),
                        'External maximum record identity mismatch')

    def _adapters(self):
        """Exact implemented adapter classes only; no completeness boolean."""
        from temporal_control_world import TemporalControlWorld
        require(type(self.integrations) is dict, 'Canonical integration registry required')
        require(set(self.integrations) <= {'control-pulses'},
                'Unsupported active integrations: ' + ', '.join(self.integrations))
        for name, adapter in self.integrations.items():
            require(type(adapter) is TemporalControlWorld, 'Unsupported control/pulse adapter type')
        return self.integrations

    def _validate_one_shots(self):
        ledger = self.healing
        require(type(ledger.records) is dict, 'Canonical one-shot registry must be a dictionary')
        for key, record in ledger.records.items():
            shape(record, OneShot)
            require(key == record.effect_id, 'One-shot dictionary/effect identity mismatch')
            require(record.source_id == 'feat:soul_cage:agony', 'Unsupported live one-shot source')
            require(type(record.expires) is ClockMarker and record.rest_epoch is None,
                    'Agony requires only its original absolute deadline')
            require(record.owner in self.lives and record.target in self.lives,
                    'One-shot owner and target require canonical scene identities')
            ident(record.effect_id)
            require(type(record.available) is bool, 'One-shot availability must be boolean')
            require(not record.available or (record.effect_id, ledger.iteration) not in ledger.consumed_reducer_ids,
                    'One-shot is both available and consumed in this iteration')
        require(all(type(x) is set for x in (ledger.committed_event_ids, ledger.consumed_reducer_ids,
                                             ledger.consumption_history)), 'Canonical consumption histories must be sets')
        for event_id in ledger.committed_event_ids:
            ident(event_id)
        for token in ledger.consumed_reducer_ids:
            require(type(token) is tuple and len(token) == 2, 'Malformed temporal consumption token')
            ident(token[0]); integer(token[1], 'consumption iteration', 0, ledger.iteration)
        observed = set()
        for entry in ledger.consumption_history:
            require(type(entry) is tuple and len(entry) == 3, 'Malformed consumption audit entry')
            effect_id, generation, event_id = entry
            ident(effect_id); ident(event_id); integer(generation, 'consumption iteration', 0, ledger.iteration)
            token = effect_id, generation
            require(token in ledger.consumed_reducer_ids and event_id in ledger.committed_event_ids,
                    'Consumption history is missing its committed event/token')
            require(token not in observed, 'One temporal permission has multiple consumption events')
            observed.add(token)
        require(observed == ledger.consumed_reducer_ids, 'Consumption token is missing historical evidence')

    @staticmethod
    def _maximum_policy(record):
        shape(record, MaxHpRecord)
        require(record.source in MAXIMUM_POLICIES,
                'No temporal maximum-HP source policy: ' + record.source)
        policy = MAXIMUM_POLICIES[record.source]
        if policy == 'conserved-progression':
            require(record.expires is None and not record.ends_on_completed_rest,
                    'Permanent progression maximum-HP source has an unsupported temporary endpoint')
        return policy

    def capture(self, roster, environment=()):
        self._validate_holders()
        s = self.scheduler
        require(self._snapshot is None, 'Immutable initiative snapshot already exists')
        require(s.iteration == 0 and s.round == 1 and s.cursor == 0 and s.turn_ordinal == 0,
                'Capture only at original initiative boundary')
        require(s.atomic_event is None and not s.completed_events and not s.queued,
                'Snapshot boundary contains unresolved/prior encounter work')
        require(s.active_regular is None, 'Snapshot cannot be captured during an active regular turn')
        roster, environment = frozenset(roster), frozenset(environment)
        require(roster and roster <= self.lives.keys(), 'Every participant must have a canonical body')
        require(len(s.initiative) == len(set(s.initiative)) and set(s.initiative) == roster,
                'Explicit finite initiative roster required')
        require(environment <= self.geometry.anchors.keys(), 'Register each rewindable environment anchor')
        require(roster <= self.geometry.poses.keys(), 'Snapshot body placements are incomplete')
        require(roster <= self.souls.living | set(self.souls.deaths), 'Canonical body/life identity required')
        require(roster <= self.inventory.physical.keys(), 'Immutable physical roots required')
        require(environment <= self.inventory.physical.keys(), 'Environment physical roots are incomplete')
        require(all(self.inventory.physical[x].kind == 'root' for x in roster), 'Participant root provenance required')
        require(all(self.inventory.physical[x].kind == 'root' and self.inventory.physical[x].survives
                    for x in environment), 'Snapshot environment requires existing physical roots')
        for actor in roster:
            require(self.lives[actor].temp_hp == self.buffers.amount(actor), 'Temporary HP projection differs')
            require(self.lives[actor].dead == (actor in self.souls.deaths), 'Death-instance/life mismatch')
        self._buffer_policies(roster)
        candidate = Snapshot(s.encounter, roster, environment, tuple(s.initiative),
            {a: {k: data(getattr(self.wallets[a], k)) for k in ('actions', 'bonus_action', 'reaction')}
             for a in roster}, data(s.rc), data(s.encounter_uses),
            {a: data(self.lives[a]) for a in roster}, {a: data(self.maxima[a]) for a in roster},
            data(self.buffers.grants), data(self.buffers.active), data(self.healing.records),
            data(self.souls), frozenset(self.inventory.physical),
            {a: data(self.geometry.poses[a]) for a in roster},
            {a: data(self.geometry.anchors[a]) for a in environment}, data(self.external.dependencies),
            data(self.memory.known), data(self.memory.alliances), tuple(sorted(self.lives)),
            data(s.now), s.global_regular, data(self.inventory.physical),
            {name: adapter.capture_payload(self, roster) for name,adapter in self._adapters().items()})
        # Verify even an unchanged restoration before accepting the snapshot.
        self._geometry_plan(candidate, set())
        self._snapshot = candidate
        return data(self._snapshot)

    def _buffer_policies(self, roster):
        for grant_id in self.buffers.active.values():
            g = self.buffers.grants[grant_id]
            shape(g, BufferGrant)
            if g.target not in roster:
                continue
            require(g.source_id in BUFFER_POLICIES, 'No temporal source policy for ' + g.source_id)
            p = BUFFER_POLICIES[g.source_id].lifetime
            require(not g.riders, 'Linked buffer rider adapter still required')
            if p in ('rest', 'rest-entity'):
                require(g.expiry is None and g.rest_epoch is not None, 'Expected original rest-bound grant')
                require(bool(g.dependencies) == (p == 'rest-entity'), 'Unexpected buffer dependency')
            elif g.owner == g.target:
                require(g.expiry is None and g.rest_epoch is not None and not g.dependencies,
                        'Blood self shield uses original recipient rest epoch')
            else:
                require(g.expiry is not None and g.rest_epoch is None and not g.dependencies,
                        'Blood ally shield uses original world deadline')

    def _watch(self, tx):
        tx.watch(self, '_snapshot')
        for name in ('scheduler', 'wallets', 'lives', 'maxima', 'buffers', 'healing',
                     'souls', 'inventory', 'geometry', 'rewards', 'external', 'memory', 'integrations', 'history'):
            tx.watch_binding(self, name)
            tx.labels[id(getattr(self, name))] = name
        tx.watch_registry(self.integrations)
        for adapter in self._adapters().values():
            adapter.watch(tx)
        for holder in (self.scheduler, self.souls, self.inventory, self.geometry,
                       self.rewards, self.external, self.memory, self.buffers, self.healing, self.history):
            tx.watch_shape(holder)
            for name in vars(holder):
                tx.watch(holder, name)
        for domain, registry in (('life', self.lives), ('wallet', self.wallets), ('maximum', self.maxima)):
            tx.watch_registry(registry)
            for actor, holder in registry.items():
                tx.labels[id(holder)] = domain+':'+actor
                tx.watch_shape(holder)
                for name in vars(holder):
                    tx.watch(holder, name)

    def _physical_plan(self, snap):
        rows = self.inventory.physical
        require(all(k == v.identity for k, v in rows.items()), 'Physical identity mismatch')
        require(snap.physical_ids <= rows.keys(), 'Physical history/identity was removed')
        for key, before in snap.physical_baseline.items():
            current = rows[key]
            require((before.kind, before.roots, before.source_owner) ==
                    (current.kind, current.roots, current.source_owner),
                    'Immutable physical provenance changed or reused an identity')
        for actor in snap.roster | snap.environment:
            before, current = snap.physical_baseline[actor], rows[actor]
            require(before.survives, 'Snapshot physical body must actually exist')
            require((before.owner, before.external_binding, before.persistent_enrollment) ==
                    (current.owner, current.external_binding, current.persistent_enrollment),
                    'Participant body ownership/enrollment changed; source adapter required')
        roots_in_scope = set(snap.roster | snap.environment)
        retire = set()

        def roots(identity, seen):
            require(identity not in seen, 'Physical provenance cycle')
            require(identity in rows, 'Missing provenance root: ' + identity)
            row = rows[identity]
            shape(row, PhysicalRecord)
            if not row.roots:
                return {identity}
            result = set()
            for parent in row.roots:
                result |= roots(parent, seen | {identity})
            return result

        for identity, row in rows.items():
            rootset = roots(identity, set())
            if not row.survives or identity in snap.physical_ids or not rootset & roots_in_scope:
                continue
            require(row.kind == 'temporal-entity', 'Surviving transferable derivative blocks restoration')
            require(rootset <= roots_in_scope, 'Mixed physical roots require a source adapter')
            require(row.source_owner in snap.roster, 'Derivative source outside temporal closure')
            require(row.external_binding is None and row.persistent_enrollment is None,
                    'Cannot rewrite an external source slot or persistent enrollment')
            retire.add(identity)
        return retire

    @staticmethod
    def _space(geometry, anchors):
        blocked = frozenset().union(*(a.blocked for a in anchors.values()))
        support = geometry.fixed_support | frozenset().union(*(a.support for a in anchors.values()))
        require(blocked <= geometry.cells and support <= geometry.cells, 'Environment outside finite boundary')
        return blocked, support

    @staticmethod
    def _reachable(geometry, pose, blocked, support):
        def legal(anchor):
            cells = replace(pose, anchor=anchor).cells()
            return cells <= geometry.cells and cells <= support and not cells & blocked
        require(legal(pose.anchor), 'Body cannot occupy its current/restored footprint')
        visited, todo = {pose.anchor}, [pose.anchor]
        while todo:
            x, y = todo.pop()
            for p in ((x-1, y), (x+1, y), (x, y-1), (x, y+1)):
                if p not in visited and legal(p):
                    visited.add(p)
                    todo.append(p)
        return visited

    def _geometry_plan(self, snap, retire):
        g = self.geometry
        poses = {k: data(v) for k, v in g.poses.items() if k not in retire}
        poses.update(data(snap.poses))
        anchors = {k: data(v) for k, v in g.anchors.items() if k not in retire}
        anchors.update(data(snap.anchors))
        before_blocked, before_support = self._space(g, g.anchors)
        blocked, support = self._space(g, anchors)
        occupied = set()
        for actor, pose in poses.items():
            cells = pose.cells()
            require(cells <= g.cells and cells <= support and not cells & blocked,
                    'Illegal restored footprint or lost support')
            require(not cells & occupied, 'Atomic restored footprints overlap')
            occupied |= cells
            if actor not in snap.roster:
                # Conservative: retain every ground location previously reachable
                # by the outsider, so an environment restore cannot trap/enclose it.
                before = self._reachable(g, pose, before_blocked, before_support)
                after = self._reachable(g, pose, blocked, support)
                require(before <= after, 'Environment restoration restricts a protected outsider')
        return poses, anchors

    def kernel_plan(self, oracle):
        """Build a pure development-fixture plan; no live cost/state changes."""
        self._validate_holders()
        snap = self._snapshot
        require(snap is not None, 'No immutable complete initiative snapshot')
        s = self.scheduler
        require(tuple(sorted(self.lives)) == snap.manifest, 'Actor registry changed; source adapter required')
        require(s.encounter == snap.encounter and oracle in snap.roster, 'Wrong encounter or Oracle')
        require(s.now >= snap.captured_at and s.global_regular >= snap.global_regular,
                'World clock or actual regular history moved backward')
        require(s.atomic_event is None and s.last_completed_event in s.completed_events,
                'Time Loop requires a fully resolved atomic combat event')
        require(s.round < 4, 'Time Loop must occur before round four')
        require(self.wallets[oracle].reaction and oracle not in s.debts, 'No available Oracle Reaction')
        epoch = self.buffers.rest_epochs.get(oracle, 0)
        require((oracle, epoch) not in s.loop_uses, 'Time Loop already spent this actual long-rest epoch')
        require(not s.queued, 'Queued source adapter required; cannot silently erase unknown work')
        for actor in snap.roster:
            require(self.maxima[actor].progression_signature == snap.maxima[actor].progression_signature,
                    'Progression changed structural source set; exact adapter required')
        self._buffer_policies(snap.roster)
        for actor, grant_id in self.buffers.active.items():
            if actor in snap.roster:
                require(self.buffers.grants[grant_id].owner in snap.roster,
                        'Current external buffer must not be silently erased')
        require(all(r.target not in snap.roster or r.owner in snap.roster
                    for r in self.souls.binds.values()), 'Current external Soul Bind needs its exact adapter')
        require(all(r.target not in snap.roster or r.owner in snap.roster
                    for r in self.healing.records.values()), 'Current external one-shot needs its exact adapter')
        tx = Transaction()
        self._watch(tx)
        retire = self._physical_plan(snap)
        poses, anchors = self._geometry_plan(snap, retire)
        current_dependencies = {}
        for dep in self.external.dependencies:
            shape(dep, ExternalDependency)
            require(dep.effect_id not in current_dependencies, 'Duplicate external dependency identity')
            current_dependencies[dep.effect_id] = dep
        snapshot_dependencies = {dep.effect_id: dep for dep in snap.dependencies}
        require(len(snapshot_dependencies) == len(snap.dependencies), 'Duplicate snapshot dependency identity')
        for dep in snap.dependencies:
            shape(dep, ExternalDependency)
            if dep.target not in snap.roster:
                continue
            require(dep.caster not in snap.roster, 'Full participant concentration needs transformation adapter')
            require(current_dependencies.get(dep.effect_id) == dep,
                    'Snapshot external dependency disappeared or changed')
            require(self.external.concentration.get(dep.caster) == dep.concentration_id,
                    'External concentration ended or was replaced')
        for dep in self.external.dependencies:
            if dep.target not in snap.roster:
                continue
            require(self.external.concentration.get(dep.caster) == dep.concentration_id,
                    'Current external concentration/dependency mismatch')
            if dep.effect_id not in snapshot_dependencies:
                effect = self.external.effects.get(dep.effect_id)
                require(effect is not None and effect.kind == 'maximum-hp'
                        and effect.identity == dep.effect_id
                        and (effect.owner, effect.target) == (dep.caster, dep.target),
                        'New external dependency lacks a supported overlay')
        for effect in self.external.effects.values():
            shape(effect, ExternalEffect)
            if effect.target in snap.roster:
                require(effect.owner not in snap.roster and effect.kind == 'maximum-hp'
                        and type(effect.record) is MaxHpRecord,
                        'External anatomy/control/suppression source adapter required')
                require((effect.identity, effect.owner, effect.target) ==
                        (effect.record.application_id, effect.record.owner, effect.record.target),
                        'External maximum source identity mismatch')
                self._maximum_policy(effect.record)

        new_iteration = s.iteration + 1
        tx.write(s, 'iteration', new_iteration)
        tx.write(s, 'round', 1)
        tx.write(s, 'cursor', 0)
        tx.write(s, 'turn_ordinal', 0)
        tx.write(s, 'active_regular', None)
        tx.write(s, 'turn_phase', 'between')
        tx.write(s, 'initiative', snap.initiative)
        tx.write(s, 'debts', s.debts | {oracle})
        tx.write(s, 'loop_uses', s.loop_uses | {(oracle, epoch)})
        tx.write(s, 'rc', {**s.rc, **{a: snap.rc.get(a, 0) for a in snap.roster}})
        tx.write(s, 'encounter_uses', {**s.encounter_uses,
                    **{a: data(snap.encounter_uses.get(a, set())) for a in snap.roster}})
        # Prevent a second loop from treating the rewind as a new completed event.
        tx.write(s, 'last_completed_event', None)
        for actor in snap.roster:
            wallet = self.wallets[actor]
            for name, value in snap.wallets[actor].items():
                if name == 'reaction' and actor in s.debts | {oracle}:
                    value = False
                tx.write(wallet, name, value)
            # rp and used remain the current canonical finite-resource histories.

        active = {a: v for a, v in self.buffers.active.items() if a not in snap.roster}
        grants = data(self.buffers.grants)
        for actor in snap.roster:
            old = grants.get(self.buffers.active.get(actor))
            if old is not None:
                old.state = 'temporal-discarded'
                old.remaining = 0
                old.riders.clear()
            gid = snap.active_grants.get(actor)
            if gid is None:
                continue
            saved = data(snap.grants[gid])
            require(saved.owner in snap.roster, 'External buffer arbitration adapter required')
            valid = (saved.expiry is None or s.now < saved.expiry)
            valid &= (saved.rest_epoch is None or
                      saved.rest_epoch == self.buffers.rest_epochs.get(actor, 0))
            valid &= all(d in snap.roster and not snap.life[d].dead for d in saved.dependencies)
            if valid:
                saved.state = 'active'
                grants[gid] = saved
                active[actor] = gid
        tx.write(self.buffers, 'grants', grants)
        tx.write(self.buffers, 'active', active)

        deaths = {a: d for a, d in self.souls.deaths.items() if a not in snap.roster}
        deaths.update({a: d for a, d in snap.souls.deaths.items() if a in snap.roster})
        living = (self.souls.living - snap.roster) | (snap.souls.living & snap.roster)
        restored_stable_ids = {a: v for a, v in self.souls.stable_event_ids.items() if a not in snap.roster}
        for actor in snap.roster:
            current, old = self.lives[actor], snap.life[actor]
            context = self.maxima[actor]
            # Conserved current passive/progression/gear sources coexist with
            # rewindable Monk trauma. Rest-ended trauma never returns.
            current_by_id = {r.application_id: r for r in context.records}
            rows = [data(r) for r in context.records if r.owner not in snap.roster
                    or self._maximum_policy(r) == 'conserved-progression']
            for r in snap.maxima[actor].records:
                if r.owner in snap.roster and self._maximum_policy(r) == 'snapshot-trauma':
                    cur = current_by_id.get(r.application_id)
                    ended_by_rest = cur is not None and (cur.ended_reason or '').startswith('completed-target-')
                    if not ended_by_rest:
                        rows.append(data(r))
            for effect in self.external.effects.values():
                if effect.target == actor:
                    rows = [r for r in rows if r.application_id != effect.record.application_id]
                    rows.append(data(effect.record))
            maximum = effective_maximum(context.base, rows, target=actor, now=s.now,
                        expedition=context.expedition, exhaustion=context.exhaustion)['effectiveMaximum']
            restored = replace(old, maximum_hp=maximum, hp=min(old.hp, maximum),
                        temp_hp=grants[active[actor]].remaining if actor in active else 0,
                        last_death_turn=current.last_death_turn)
            if restored.stable:
                event = snap.souls.stable_event_ids.get(actor)
                require(event is not None and event not in self.souls.resolved_stable,
                        'Stable recovery already resolved or lacks a unique event')
                require(restored.stable_until_seconds is not None and s.now.seconds < restored.stable_until_seconds,
                        'Expired Stable recovery needs an explicit reconciliation adapter')
                restored_stable_ids[actor] = event
            for f in fields(LifeState):
                tx.write(current, f.name, getattr(restored, f.name))
            tx.write(context, 'records', tuple(rows))
        tx.write(self.souls, 'deaths', deaths)
        tx.write(self.souls, 'living', living)
        tx.write(self.souls, 'stable_event_ids', restored_stable_ids)
        remains = {k: v for k, v in self.souls.remains.items() if k not in snap.roster}
        remains.update({k: v for k, v in snap.souls.remains.items() if k in snap.roster})
        tx.write(self.souls, 'remains', remains)
        binds = {k: v for k, v in self.souls.binds.items() if v.target not in snap.roster}
        for key, record in snap.souls.binds.items():
            if record.target not in snap.roster:
                continue
            require(record.owner in snap.roster, 'External soul effect needs its exact adapter')
            if s.now.seconds >= record.bind.expires:
                continue
            if record.bind.stage == 'bound':
                if deaths.get(record.target) != record.death_instance:
                    continue
            elif record.target not in living:
                continue
            binds[key] = data(record)
        tx.write(self.souls, 'binds', binds)

        shots = {k: v for k, v in self.healing.records.items() if v.target not in snap.roster}
        for key, record in snap.one_shots.items():
            if record.target not in snap.roster:
                continue
            require(record.owner in snap.roster, 'External one-shot effect needs its exact adapter')
            valid = record.expires is None or s.now < record.expires
            valid &= record.rest_epoch is None or record.rest_epoch == self.buffers.rest_epochs.get(record.target, 0)
            shots[key] = replace(record, available=record.available and valid)
        tx.write(self.healing, 'records', shots)
        tx.write(self.healing, 'iteration', new_iteration)
        # committed_event_ids, consumed_reducer_ids and consumption_history stay.

        physical = data(self.inventory.physical)
        for actor in snap.roster | snap.environment:
            physical[actor] = replace(physical[actor], survives=snap.physical_baseline[actor].survives)
        for identity in retire:
            physical[identity] = replace(physical[identity], survives=False)
        tx.write(self.inventory, 'physical', physical)
        tx.write(self.geometry, 'poses', poses)
        tx.write(self.geometry, 'anchors', anchors)
        eligible = (set(snap.alliances.get(oracle, set())) | {oracle}) & snap.roster
        retained, known = data(self.memory.retained), data(self.memory.known)
        for actor in eligible:
            retained.setdefault(actor, set()).update(self.memory.perceived.get(actor, set()))
        for actor in snap.roster:
            known[actor] = set(snap.known.get(actor, set())) | retained.get(actor, set())
        tx.write(self.memory, 'retained', retained)
        tx.write(self.memory, 'known', known)
        tx.write(self.memory, 'perceived', {a: v for a, v in self.memory.perceived.items() if a not in snap.roster})
        require(set(snap.adapter_payloads) == set(self.integrations), 'Temporal adapter set changed since snapshot')
        for name,adapter in self._adapters().items():
            adapter.stage_restore(self, tx, snap.adapter_payloads[name], snap.roster, new_iteration)
        frame = {'iterationDiscarded': s.iteration, 'iterationCreated': new_iteration,
                 'oracle': oracle, 'afterEvent': s.last_completed_event, 'atWorldMarker': s.now,
                 'changes': tx.audit_rows()}
        tx.write(self.history, 'frames', self.history.frames + (frame,))
        return tx
