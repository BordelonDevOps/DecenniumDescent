# Resume the actual Time Loop kernel review: 52-test revision

Thank you for explaining the scope to the owner. The prior review did not produce a completed findings/approval response before that question. Please now complete the independent review of the actual updated code below. The owner authorized us to keep developing together. No whole-game approval or GitHub push is requested here.

While you reviewed, my own audit added six regressions and repaired physical root identity restoration, immutable provenance validation, per-restore before/after audit frames, the single canonical completed-rest epoch, current external max-HP record precedence and the original world-clock boundary. The original 46-test submitted packet remains preserved; THIS complete 52-test revision supersedes it for implementation review. All 52 tests pass locally.

Please report concrete reproducible defects and required repairs in the ADMITTED bounded fixture scope. Check conservation, atomic commit, stale-plan detection, same-ID one-shots, physical derivatives/outsiders, memory and scope claims. In particular check if a malformed or still-unclassified active record can silently get through this kernel. Do not claim full Time Loop closure: seven integrations remain explicitly unimplemented and playable_plan always rejects. Distinguish issues in this kernel from those openly missing integrations.

If there are no blockers within that limited scope, say so explicitly while keeping the full Time Loop and whole-game gates open. If blockers exist, give counterexamples so I can implement targeted repairs.


## tools/temporal_playtest_rules.py

```
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
from control_playtest_rules import ClockMarker, clock_marker
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

    def round_id(self):
        return RoundId(self.encounter, self.iteration, self.round)

    def begin_event(self, event_id):
        ident(event_id)
        require(self.atomic_event is None and event_id not in self.completed_events,
                'One new complete atomic event at a time')
        self.atomic_event = event_id

    def finish_event(self, event_id):
        require(self.atomic_event == event_id, 'Finish the current event completely')
        self.atomic_event = None
        self.last_completed_event = event_id
        self.completed_events.add(event_id)

    def regular_start(self, actor, wallet, now):
        shape(wallet, Wallet)
        require(self.atomic_event is None and actor in self.initiative, 'Legal regular-start boundary required')
        marker = clock_marker(now)
        require(marker >= self.now, 'Elapsed time never rewinds')
        self.now = marker
        self.global_regular += 1
        self.turn_ordinal += 1
        self.debts.discard(actor)
        wallet.reaction = True
        return TurnId(self.encounter, self.iteration, actor, self.turn_ordinal)


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
        require(record.expires is not None, 'Agony has an absolute original deadline')
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


DATA_TYPES = frozenset((
    ClockMarker, LifeState, MaxHpRecord, BufferGrant, SoulBind, RoundId, TurnId,
    RewardOpportunityKey, OneShot, MaximumContext, SoulRecord, SoulIdentity,
    PhysicalRecord, Pose, EnvironmentAnchor, ExternalDependency, ExternalEffect,
    BufferPolicy, Snapshot, TemporalHistory,
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

    def _validate_holders(self):
        shape(self.scheduler, Scheduler)
        for holder, cls in ((self.souls, SoulIdentity), (self.inventory, Inventory),
                            (self.geometry, Geometry), (self.rewards, RewardLedger),
                            (self.external, ExternalState), (self.memory, Memory), (self.history, TemporalHistory)):
            shape(holder, cls)
        require(not self.integrations, 'Unsupported active integrations: ' + ', '.join(self.integrations))
        require(set(self.wallets) == set(self.lives) == set(self.maxima),
                'Canonical scene registries must name the same actors, including outsiders')
        for actor in self.lives:
            ident(actor)
            shape(self.lives[actor], LifeState)
            shape(self.wallets[actor], Wallet)
            shape(self.maxima[actor], MaximumContext)
        require(type(self.buffers) is BufferLedger, 'One canonical BufferLedger required')
        require(set(vars(self.buffers)) <= {'grants', 'active', 'rest_epochs', 'damage_events',
                                         'absorptions', 'form_instances', 'spell_anatomies', 'ordinary_cast_events'},
                'Unclassified BufferLedger field')
        require(not self.buffers.form_instances and not self.buffers.spell_anatomies,
                'Form/transformation adapter required')
        require(all(p['finished'] for p in self.buffers.absorptions.values()), 'Mid-packet buffer absorption')
        require(type(self.healing) is TemporalHealingCommitLedger, 'One canonical temporal healing ledger required')
        require(set(vars(self.healing)) == {'iteration', 'records', 'consumption_history',
                    'committed_event_ids', 'consumed_reducer_ids'}, 'Unclassified healing ledger state')
        require(self.healing.iteration == self.scheduler.iteration, 'Healing/scheduler iteration mismatch')
        require(self.geometry.movement_model == 'finite-level-ground', 'Geometry source adapter required')
        for name, minimum in (('iteration', 0), ('round', 1), ('cursor', 0), ('global_regular', 0), ('turn_ordinal', 0)):
            integer(getattr(self.scheduler, name), 'scheduler '+name, minimum)
        shape(self.scheduler.now, ClockMarker)
        for row in self.inventory.physical.values():
            shape(row, PhysicalRecord)
            require(row.kind in ('root', 'inventory', 'temporal-entity'), 'Unknown physical record kind')
        require(all(a in self.lives for a in self.buffers.active), 'Unclassified shield target body')

    def capture(self, roster, environment=()):
        self._validate_holders()
        s = self.scheduler
        require(self._snapshot is None, 'Immutable initiative snapshot already exists')
        require(s.iteration == 0 and s.round == 1 and s.cursor == 0 and s.turn_ordinal == 0,
                'Capture only at original initiative boundary')
        require(s.atomic_event is None and not s.completed_events and not s.queued,
                'Snapshot boundary contains unresolved/prior encounter work')
        roster, environment = frozenset(roster), frozenset(environment)
        require(roster and roster <= self.lives.keys(), 'Every participant must have a canonical body')
        require(len(s.initiative) == len(set(s.initiative)) and set(s.initiative) == roster,
                'Explicit finite initiative roster required')
        require(environment <= self.geometry.anchors.keys(), 'Register each rewindable environment anchor')
        require(roster <= self.geometry.poses.keys(), 'Snapshot body placements are incomplete')
        require(roster <= self.souls.living | set(self.souls.deaths), 'Canonical body/life identity required')
        require(roster <= self.inventory.physical.keys(), 'Immutable physical roots required')
        require(all(self.inventory.physical[x].kind == 'root' for x in roster), 'Participant root provenance required')
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
            data(s.now), s.global_regular, data(self.inventory.physical))
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
        tx.watch(self, 'integrations')
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
        for actor in snap.roster:
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
        anchors = data(g.anchors)
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
        for dep in snap.dependencies:
            shape(dep, ExternalDependency)
            require(dep.caster not in snap.roster, 'Full participant concentration needs transformation adapter')
            require(self.external.concentration.get(dep.caster) == dep.concentration_id,
                    'External concentration ended or was replaced')
        for effect in self.external.effects.values():
            shape(effect, ExternalEffect)
            if effect.target in snap.roster:
                require(effect.owner not in snap.roster and effect.kind == 'maximum-hp'
                        and type(effect.record) is MaxHpRecord,
                        'External anatomy/control/suppression source adapter required')
                require((effect.identity, effect.owner, effect.target) ==
                        (effect.record.application_id, effect.record.owner, effect.record.target),
                        'External maximum source identity mismatch')

        new_iteration = s.iteration + 1
        tx.write(s, 'iteration', new_iteration)
        tx.write(s, 'round', 1)
        tx.write(s, 'cursor', 0)
        tx.write(s, 'turn_ordinal', 0)
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
            rows = [data(r) for r in context.records if r.owner not in snap.roster or not r.source.startswith('monk.')]
            for r in snap.maxima[actor].records:
                if r.owner in snap.roster and r.source.startswith('monk.'):
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
        for actor in snap.roster:
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
        frame = {'iterationDiscarded': s.iteration, 'iterationCreated': new_iteration,
                 'oracle': oracle, 'afterEvent': s.last_completed_event, 'atWorldMarker': s.now,
                 'changes': tx.audit_rows()}
        tx.write(self.history, 'frames', self.history.frames + (frame,))
        return tx

```


## tools/validate_temporal_playtests.py

```
"""Adversarial tests for the unpromoted temporal transaction kernel."""
from copy import deepcopy
from dataclasses import replace
from pathlib import Path
from fractions import Fraction
import hashlib
import json
import unittest

from temporal_playtest_rules import (
    TemporalKernel, Scheduler, Wallet, LifeState, MaximumContext, SoulIdentity,
    Inventory, PhysicalRecord, Geometry, Pose, EnvironmentAnchor, Memory,
    BufferGrant, ClockMarker, OneShot, RewardOpportunityKey, SpellRuleError,
    ExternalDependency, ExternalEffect, MaxHpRecord, SoulBind, SoulRecord,
    RoundId, TurnId,
)
from healing_playtest_rules import HealingReduction, healing_packet


def scene(*, capture=True, outsider=False):
    actors = ['a', 'b', 'foe'] + (['outside'] if outsider else [])
    lives = {a: LifeState(30, 25) for a in actors}
    wallets = {a: Wallet(rp=10) for a in actors}
    maxima = {a: MaximumContext(30, progression_signature=('level:20',)) for a in actors}
    souls = SoulIdentity(living=set(actors))
    inventory = Inventory(physical={a: PhysicalRecord(a, 'root', a) for a in actors})
    cells = frozenset((x, y) for x in range(20) for y in range(5))
    geometry = Geometry(cells, cells, {a: Pose((1+3*i, 2)) for i, a in enumerate(actors)})
    memory = Memory(known={a: {'start:'+a} for a in actors},
                    alliances={'a': {'a', 'b'}, 'b': {'b'}})
    scheduler = Scheduler('encounter-1', ('a', 'b', 'foe'), rc={'a': 5, 'b': 3})
    w = TemporalKernel(scheduler, wallets, lives, maxima, souls=souls,
                       inventory=inventory, geometry=geometry, memory=memory)
    if capture:
        w.capture(('a', 'b', 'foe'))
    return w


def event(w, name='attack-1', now=12):
    w.scheduler.now = ClockMarker(now)
    w.scheduler.begin_event(name)
    w.scheduler.finish_event(name)


def history(w):
    return deepcopy({
        'scheduler': vars(w.scheduler), 'wallets': {a:vars(v) for a,v in w.wallets.items()},
        'lives': {a:vars(v) for a,v in w.lives.items()}, 'buffers':vars(w.buffers),
        'healing':vars(w.healing), 'souls':vars(w.souls), 'inventory':vars(w.inventory),
        'geometry':vars(w.geometry), 'memory':vars(w.memory), 'rewards':vars(w.rewards),
        'external':vars(w.external), 'maxima':{a:vars(v) for a,v in w.maxima.items()}, 'history':vars(w.history),
    })


class TemporalTests(unittest.TestCase):
    def blocked(self, w, match, oracle='a'):
        before = history(w)
        with self.assertRaisesRegex(SpellRuleError, match):
            w.kernel_plan(oracle)
        self.assertEqual(history(w), before, 'Failed preflight mutated canonical state/cost')

    def test_full_time_loop_remains_gated(self):
        w = scene()
        self.assertFalse(w.support_report()['fullTimeLoopOperational'])
        self.assertEqual(len(w.support_report()['missing']), 7)
        with self.assertRaisesRegex(SpellRuleError, 'unavailable'):
            w.playable_plan('a')

    def test_atomic_restore_preserves_resources_and_object_aliases(self):
        w = scene()
        life, wallet, buffer = w.lives['a'], w.wallets['a'], w.buffers
        life.hp = 3
        life.wounds = (1,)
        wallet.rp = 2
        wallet.actions = 0
        wallet.used.add('daily-spent')
        w.scheduler.rc['a'] = 0
        w.scheduler.encounter_uses['a'] = {'encounter-spent'}
        w.geometry.poses['a'] = Pose((2, 3))
        event(w)
        before = history(w)
        plan = w.kernel_plan('a')
        self.assertEqual(history(w), before)
        plan.commit()
        self.assertIs(w.lives['a'], life)
        self.assertIs(w.wallets['a'], wallet)
        self.assertIs(w.buffers, buffer)
        self.assertEqual((life.hp, life.wounds, wallet.rp, wallet.actions), (25, (), 2, 1))
        self.assertEqual(wallet.used, {'daily-spent'})
        self.assertFalse(wallet.reaction)
        self.assertEqual(w.scheduler.rc['a'], 5)
        self.assertEqual(w.scheduler.encounter_uses['a'], set())
        self.assertEqual(w.geometry.poses['a'].anchor, (1, 2))
        self.assertEqual(w.scheduler.now, ClockMarker(12))
        self.assertEqual(w.scheduler.iteration, 1)
        with self.assertRaisesRegex(SpellRuleError, 'already committed'):
            plan.commit()

    def test_all_oracle_debts_survive_later_loop(self):
        w = scene()
        event(w)
        w.kernel_plan('a').commit()
        event(w, 'attack-2', 13)
        w.kernel_plan('b').commit()
        self.assertEqual(w.scheduler.debts, {'a', 'b'})
        self.assertFalse(w.wallets['a'].reaction)
        self.assertFalse(w.wallets['b'].reaction)
        self.assertEqual(w.scheduler.loop_uses, {('a', 0), ('b', 0)})

    def test_actual_regular_refresh_clears_only_owner_debt(self):
        w = scene()
        event(w)
        w.kernel_plan('a').commit()
        w.scheduler.regular_start('a', w.wallets['a'], 13)
        self.assertTrue(w.wallets['a'].reaction)
        self.assertNotIn('a', w.scheduler.debts)
        event(w, 'attack-2', 13)
        w.kernel_plan('b').commit()
        self.assertTrue(w.wallets['a'].reaction)
        self.assertEqual(w.scheduler.global_regular, 1)
        self.assertEqual(w.scheduler.debts, {'b'})

    def test_same_owner_long_rest_use_does_not_return(self):
        w = scene()
        event(w)
        w.kernel_plan('a').commit()
        w.scheduler.regular_start('a', w.wallets['a'], 13)
        event(w, 'attack-2', 13)
        self.blocked(w, 'already spent')

    def test_round_and_turn_keys_are_iteration_qualified(self):
        w = scene()
        before = w.scheduler.round_id().token()
        event(w)
        w.kernel_plan('a').commit()
        self.assertNotEqual(before, w.scheduler.round_id().token())
        self.assertNotEqual(TurnId('e', 0, 'a', 1).token(), TurnId('e', 1, 'a', 1).token())
        self.assertNotEqual(TurnId('e', 0, 'a', 1).token(), TurnId('e', 0, 'a', 1, 'extra').token())

    def test_timing_failures_spend_nothing(self):
        for kind in ('no-event', 'mid-event', 'late-round', 'queue'):
            with self.subTest(kind=kind):
                w = scene()
                if kind != 'no-event':
                    event(w)
                if kind == 'mid-event':
                    w.scheduler.begin_event('pending')
                if kind == 'late-round':
                    w.scheduler.round = 4
                if kind == 'queue':
                    w.scheduler.queued['command'] = {'owner': 'a'}
                self.blocked(w, 'resolved|round four|Queued')

    def test_stale_plan_detects_each_conserved_mutation(self):
        changes = (
            lambda w: setattr(w.wallets['a'], 'rp', 1),
            lambda w: w.inventory.quantities.update(potion=0),
            lambda w: w.buffers.rest_epochs.update(a=1),
            lambda w: w.rewards.claims.update(other='claim'),
            lambda w: w.memory.perceived.update(a={'new information'}),
        )
        for change in changes:
            w = scene(); event(w)
            plan = w.kernel_plan('a'); change(w); before = history(w)
            with self.assertRaisesRegex(SpellRuleError, 'Stale'):
                plan.commit()
            self.assertEqual(history(w), before)

    def test_stale_plan_detects_replaced_canonical_binding(self):
        w = scene(); event(w)
        plan = w.kernel_plan('a')
        w.wallets['a'] = deepcopy(w.wallets['a'])
        with self.assertRaisesRegex(SpellRuleError, 'registry changed'):
            plan.commit()
        self.assertFalse(w.scheduler.loop_uses)

    def test_stale_plan_detects_new_unknown_field(self):
        w = scene(); event(w)
        plan = w.kernel_plan('a')
        w.lives['a'].new_effect = 'unclassified'
        with self.assertRaisesRegex(SpellRuleError, 'schema changed'):
            plan.commit()
        self.assertFalse(w.scheduler.loop_uses)

    def test_maximum_hp_clamps_without_healing_critical_ceiling(self):
        w = scene(capture=False)
        w.lives['a'] = LifeState(30, 30, wounds=(1, 2, 3))
        w.capture(('a', 'b', 'foe'))
        w.maxima['a'].base = 20
        w.lives['a'].hp = 2
        event(w)
        w.kernel_plan('a').commit()
        self.assertEqual((w.lives['a'].maximum_hp, w.lives['a'].hp), (20, 20))
        self.assertEqual(w.lives['a'].wounds, (1, 2, 3))
        self.assertFalse(w.healing.committed_event_ids)
        self.assertFalse(w.buffers.damage_events)

    def test_larger_current_maximum_does_not_increase_snapshot_hp(self):
        w = scene(); w.maxima['a'].base = 100; event(w)
        w.kernel_plan('a').commit()
        self.assertEqual((w.lives['a'].maximum_hp, w.lives['a'].hp), (100, 25))

    def test_structural_progression_divergence_fails(self):
        w = scene(); w.maxima['a'].progression_signature += ('new-feat',); event(w)
        self.blocked(w, 'Progression')

    def test_rest_ended_monk_trauma_does_not_return(self):
        w = scene(capture=False)
        trauma = MaxHpRecord('trauma', 'monk.hero.iron-fist-master.ribcrusher-strike',
                             'b', 'a', 5, ends_on_completed_rest=True)
        w.maxima['a'].records = (trauma,)
        w.lives['a'] = LifeState(25, 20)
        w.capture(('a', 'b', 'foe'))
        w.maxima['a'].records = (replace(trauma, present=False, ended_reason='completed-target-short-rest'),)
        event(w); w.kernel_plan('a').commit()
        self.assertEqual(w.lives['a'].maximum_hp, 30)

    def test_stable_resolved_or_expired_event_never_replays(self):
        for resolved, now in ((True, 12), (False, 3600)):
            w = scene(capture=False)
            w.lives['b'] = LifeState(30, 0, stable=True, stable_until_seconds=3600)
            w.souls.stable_event_ids['b'] = 'recovery-1'
            w.capture(('a', 'b', 'foe'))
            if resolved:
                w.souls.resolved_stable.add('recovery-1')
            event(w, now=now)
            self.blocked(w, 'Stable')

    def test_valid_stable_deadline_is_not_rebased(self):
        w = scene(capture=False)
        w.lives['b'] = LifeState(30, 0, stable=True, stable_until_seconds=3600)
        w.souls.stable_event_ids['b'] = 'recovery-1'
        w.capture(('a', 'b', 'foe'))
        event(w); w.kernel_plan('a').commit()
        self.assertEqual(w.lives['b'].stable_until_seconds, 3600)

    def test_same_body_returns_without_revival_event(self):
        w = scene()
        w.lives['b'] = LifeState(30, 0, dead=True)
        w.souls.living.remove('b'); w.souls.deaths['b'] = 'death-1'
        w.souls.remains['b'] = {'corpse': 'body-b'}
        event(w); w.kernel_plan('a').commit()
        self.assertFalse(w.lives['b'].dead)
        self.assertEqual(w.lives['b'].hp, 25)
        self.assertNotIn('b', w.souls.deaths)
        self.assertNotIn('b', w.souls.remains)
        self.assertEqual(w.souls.return_history, set())

    def test_soul_bind_keeps_original_deadline(self):
        for now, present in ((12, True), (60, False)):
            w = scene(capture=False)
            w.lives['b'] = LifeState(30, 0)
            w.souls.binds['bind'] = SoulRecord('bind', 'foe', 'b', SoulBind('b', 'pending', 60))
            w.capture(('a', 'b', 'foe')); event(w, now=now)
            w.kernel_plan('a').commit()
            self.assertEqual('bind' in w.souls.binds, present)
            if present:
                self.assertEqual(w.souls.binds['bind'].bind.expires, 60)

    def test_post_snapshot_death_bind_becomes_inactive(self):
        w = scene()
        w.lives['b'] = LifeState(30, 0, dead=True)
        w.souls.living.remove('b'); w.souls.deaths['b'] = 'death-1'
        w.souls.binds['bind'] = SoulRecord('bind', 'foe', 'b', SoulBind('b', 'bound', 86400), 'death-1')
        event(w); w.kernel_plan('a').commit()
        self.assertFalse(w.souls.binds)

    def test_default_buffer_restores_same_id_remaining_not_new_offer(self):
        w = scene(capture=False)
        w.buffers.offer(BufferGrant('shield', 'feat:chef', 'b', 'a', 8, rest_epoch=0))
        w.lives['a'].temp_hp = 8
        w.capture(('a', 'b', 'foe'))
        w.buffers.grants['shield'].remaining = 2
        w.lives['a'].temp_hp = 2
        w.buffers.damage_events.add(('a', 'damage-old'))
        event(w); w.kernel_plan('a').commit()
        self.assertEqual((w.buffers.amount('a'), w.lives['a'].temp_hp), (8, 8))
        self.assertEqual(set(w.buffers.grants), {'shield'})
        self.assertEqual(w.buffers.damage_events, {('a', 'damage-old')})

    def test_buffer_real_rest_invalidates_snapshot_grant(self):
        w = scene(capture=False)
        w.buffers.offer(BufferGrant('shield', 'feat:chef', 'b', 'a', 8, rest_epoch=0))
        w.lives['a'].temp_hp = 8
        w.capture(('a', 'b', 'foe'))
        w.buffers.completed_long_rest('a', 1)
        w.lives['a'].temp_hp = 0
        event(w); w.kernel_plan('a').commit()
        self.assertEqual((w.buffers.amount('a'), w.lives['a'].temp_hp), (0, 0))

    def test_blood_ally_absolute_buffer_expired_does_not_return(self):
        w = scene(capture=False)
        w.buffers.offer(BufferGrant('blood', 'feat:blood_ritual', 'a', 'b', 8, expiry=ClockMarker(3600)))
        w.lives['b'].temp_hp = 8
        w.capture(('a', 'b', 'foe')); event(w, now=3600)
        w.kernel_plan('a').commit()
        self.assertEqual(w.lives['b'].temp_hp, 0)

    def test_unknown_buffer_source_is_unavailable(self):
        w = scene(capture=False)
        w.buffers.offer(BufferGrant('x', 'future-source', 'a', 'a', 8, rest_epoch=0))
        w.lives['a'].temp_hp = 8
        with self.assertRaisesRegex(SpellRuleError, 'No temporal source policy'):
            w.capture(('a', 'b', 'foe'))
        self.assertIsNone(w._snapshot)

    def test_external_late_buffer_not_silently_erased(self):
        w = scene(outsider=True)
        w.buffers.offer(BufferGrant('shield', 'feat:chef', 'outside', 'a', 8, rest_epoch=0))
        w.lives['a'].temp_hp = 8
        event(w); self.blocked(w, 'external buffer')

    def test_one_shot_same_id_new_consumption_view_preserves_audit(self):
        w = scene(capture=False)
        shot = OneShot('agony-1', 'feat:soul_cage:agony', 'a', 'foe', True, ClockMarker(60))
        w.healing.register(shot)
        w.capture(('a', 'b', 'foe'))
        reduction = HealingReduction('agony-1', 'agony', 'factor', Fraction(1, 2), next_healing=True)
        packet = healing_packet(w.lives['foe'], 8, reductions=(reduction,))
        w.healing.commit('heal-1', packet)
        event(w); w.kernel_plan('a').commit()
        self.assertTrue(w.healing.records['agony-1'].available)
        self.assertEqual(w.healing.commit('heal-2', packet), {'agony-1'})
        self.assertEqual(w.healing.consumed_reducer_ids, {('agony-1', 0), ('agony-1', 1)})
        self.assertEqual(w.healing.committed_event_ids, {'heal-1', 'heal-2'})
        with self.assertRaisesRegex(SpellRuleError, 'already committed'):
            w.healing.commit('heal-1', packet)

    def test_snapshot_consumed_one_shot_stays_consumed(self):
        w = scene(capture=False)
        w.healing.register(OneShot('agony-1', 'feat:soul_cage:agony', 'a', 'foe', False, ClockMarker(60)))
        w.capture(('a', 'b', 'foe')); event(w)
        w.kernel_plan('a').commit()
        self.assertFalse(w.healing.records['agony-1'].available)
        with self.assertRaisesRegex(SpellRuleError, 'already consumed'):
            w.healing.commit('heal-1', {'nextHealingCandidates': ['agony-1']})

    def test_expired_one_shot_stays_unavailable(self):
        w = scene(capture=False)
        w.healing.register(OneShot('agony-1', 'feat:soul_cage:agony', 'a', 'foe', True, ClockMarker(60)))
        w.capture(('a', 'b', 'foe')); event(w, now=60)
        w.kernel_plan('a').commit()
        self.assertFalse(w.healing.records['agony-1'].available)

    def test_reward_opportunity_not_fresh_death_event(self):
        w = scene()
        key = RewardOpportunityKey('encounter-1', 'foe', 'xp', 'defeat')
        w.rewards.opportunities.add(key); w.rewards.claim(key, 'death-1')
        event(w); w.kernel_plan('a').commit()
        with self.assertRaisesRegex(SpellRuleError, 'already claimed'):
            w.rewards.claim(key, 'death-2')
        other = RewardOpportunityKey('encounter-1', 'foe', 'harvest', 'gland')
        w.rewards.opportunities.add(other); w.rewards.claim(other, 'harvest-1')
        self.assertEqual(len(w.rewards.claims), 2)

    def test_immutable_snapshot_cannot_be_recaptured(self):
        w = scene()
        with self.assertRaisesRegex(SpellRuleError, 'already exists'):
            w.capture(('a', 'b', 'foe'))

    def test_snapshot_returned_copy_cannot_change_original(self):
        w = scene(capture=False)
        returned = w.capture(('a', 'b', 'foe'))
        returned.life['a'].hp = 1
        event(w); w.kernel_plan('a').commit()
        self.assertEqual(w.lives['a'].hp, 25)

    def test_physical_derivative_entity_retires_cost_conserved(self):
        w = scene()
        w.inventory.physical['raised'] = PhysicalRecord('raised', 'temporal-entity', 'a', ('foe',), 0,
                                                        source_owner='a')
        w.geometry.poses['raised'] = Pose((17, 2))
        w.inventory.quantities['onyx'] = 0
        w.inventory.expenditure_events.add('raise-cost')
        event(w); w.kernel_plan('a').commit()
        self.assertFalse(w.inventory.physical['raised'].survives)
        self.assertNotIn('raised', w.geometry.poses)
        self.assertEqual(w.inventory.quantities['onyx'], 0)
        self.assertEqual(w.inventory.expenditure_events, {'raise-cost'})

    def test_transitive_surviving_inventory_derivative_blocks(self):
        w = scene()
        w.inventory.physical['harvest'] = PhysicalRecord('harvest', 'inventory', 'a', ('foe',), 0, False)
        w.inventory.physical['sale'] = PhysicalRecord('sale', 'inventory', 'outside', ('harvest',), 0)
        event(w); self.blocked(w, 'transferable derivative')

    def test_mixed_roots_and_external_asset_slot_block(self):
        for mode in ('mixed', 'binding', 'enrollment'):
            w = scene()
            w.inventory.physical['ore'] = PhysicalRecord('ore', 'root', 'outside')
            w.inventory.physical['new'] = PhysicalRecord('new', 'temporal-entity', 'a',
                ('foe', 'ore') if mode == 'mixed' else ('foe',), 0, source_owner='a',
                external_binding='slot' if mode == 'binding' else None,
                persistent_enrollment='asset' if mode == 'enrollment' else None)
            event(w); self.blocked(w, 'Mixed|external source slot')

    def test_consumed_derivative_remains_consumed(self):
        w = scene()
        w.inventory.physical['used'] = PhysicalRecord('used', 'inventory', 'a', ('foe',), 0, False)
        event(w); w.kernel_plan('a').commit()
        self.assertFalse(w.inventory.physical['used'].survives)

    def test_transferred_original_item_ownership_is_conserved(self):
        w = scene(capture=False)
        w.inventory.physical['sword'] = PhysicalRecord('sword', 'inventory', 'a')
        w.capture(('a', 'b', 'foe'))
        w.inventory.physical['sword'] = replace(w.inventory.physical['sword'], owner='outside')
        event(w); w.kernel_plan('a').commit()
        self.assertEqual(w.inventory.physical['sword'].owner, 'outside')

    def test_provenance_cycle_blocks(self):
        w = scene()
        w.inventory.physical['x'] = PhysicalRecord('x', 'inventory', 'a', ('y',))
        w.inventory.physical['y'] = PhysicalRecord('y', 'inventory', 'a', ('x',))
        event(w); self.blocked(w, 'cycle')

    def test_snapshot_pose_overlap_with_outsider_blocks(self):
        w = scene(outsider=True)
        w.geometry.poses['outside'] = Pose((1, 2))
        w.geometry.poses['a'] = Pose((0, 0))
        event(w); self.blocked(w, 'overlap')

    def test_atomic_participant_exchange_is_legal(self):
        w = scene()
        w.geometry.poses['a'], w.geometry.poses['b'] = w.geometry.poses['b'], w.geometry.poses['a']
        event(w); w.kernel_plan('a').commit()
        self.assertEqual(w.geometry.poses['a'].anchor, (1, 2))
        self.assertEqual(w.geometry.poses['b'].anchor, (4, 2))

    def test_environment_cannot_enclose_outsider_without_cell_overlap(self):
        w = scene(capture=False, outsider=True)
        wall = EnvironmentAnchor('wall', blocked=frozenset((12, y) for y in range(5)))
        w.geometry.anchors['wall'] = wall
        w.inventory.physical['wall'] = PhysicalRecord('wall', 'root', None)
        w.capture(('a', 'b', 'foe'), ('wall',))
        w.geometry.anchors['wall'] = replace(wall, blocked=frozenset())
        event(w); self.blocked(w, 'restricts a protected outsider')

    def test_environment_cannot_remove_external_support(self):
        w = scene(capture=False, outsider=True)
        w.geometry.fixed_support -= {(10, 2)}
        w.geometry.poses['outside'] = Pose((11, 2))
        floor = EnvironmentAnchor('floor')
        w.geometry.anchors['floor'] = floor
        w.inventory.physical['floor'] = PhysicalRecord('floor', 'root', None)
        w.capture(('a', 'b', 'foe'), ('floor',))
        w.geometry.anchors['floor'] = replace(floor, support=frozenset({(10, 2)}))
        w.geometry.poses['outside'] = Pose((10, 2))
        event(w); self.blocked(w, 'lost support')

    def test_external_concentration_not_recreated_or_changed(self):
        w = scene(capture=False, outsider=True)
        w.external.concentration['outside'] = 'cast-original'
        w.external.dependencies = (ExternalDependency('effect', 'b', 'outside', 'cast-original'),)
        w.capture(('a', 'b', 'foe'))
        w.lives['outside'].hp = 5
        event(w); w.kernel_plan('a').commit()
        self.assertEqual(w.external.concentration['outside'], 'cast-original')
        self.assertEqual(w.lives['outside'].hp, 5)
        event(w, 'attack-2', 13)
        w.external.concentration['outside'] = 'cast-new'
        self.blocked(w, 'External concentration', oracle='b')

    def test_external_new_maximum_modifier_overlays_snapshot(self):
        w = scene(outsider=True)
        modifier = MaxHpRecord('external-trauma', 'monk.hero.iron-fist-master.ribcrusher-strike',
                               'outside', 'a', 9, ends_on_completed_rest=True)
        w.external.effects['external-trauma'] = ExternalEffect('external-trauma', 'outside', 'a',
                                                              'maximum-hp', modifier)
        event(w); w.kernel_plan('a').commit()
        self.assertEqual(w.lives['a'].maximum_hp, 21)
        self.assertEqual(w.lives['a'].hp, 21)

    def test_external_unknown_anatomy_blocks(self):
        w = scene(outsider=True)
        w.external.effects['new-form'] = ExternalEffect('new-form', 'outside', 'a', 'anatomy')
        event(w); self.blocked(w, 'External anatomy')

    def test_memory_only_snapshot_allies_and_observed_facts(self):
        w = scene()
        w.memory.perceived = {'a': {'saw trap'}, 'b': {'heard warning'}, 'foe': {'saw attack'}}
        w.memory.known['foe'].add('saw attack')
        w.memory.alliances['a'] = {'foe'}
        event(w); w.kernel_plan('a').commit()
        self.assertIn('saw trap', w.memory.known['a'])
        self.assertIn('heard warning', w.memory.known['b'])
        self.assertNotIn('saw attack', w.memory.known['foe'])
        self.assertNotIn('heard warning', w.memory.known['a'])
        self.assertNotIn('secret stats', set.union(*w.memory.known.values()))

    def test_retained_memory_is_cumulative_across_different_oracles(self):
        w = scene()
        w.memory.perceived = {'a': {'first'}, 'b': {'first-b'}}
        event(w); w.kernel_plan('a').commit()
        w.memory.perceived = {'a': {'second-a'}, 'b': {'second-b'}}
        event(w, 'attack-2', 13); w.kernel_plan('b').commit()
        self.assertIn('first', w.memory.known['a'])
        self.assertNotIn('second-a', w.memory.known['a'])
        self.assertTrue({'first-b', 'second-b'} <= w.memory.known['b'])

    def test_unsupported_holder_and_dynamic_state_fail(self):
        w = scene(); w.integrations['DruidState'] = object(); event(w)
        self.blocked(w, 'Unsupported active')
        w = scene(); w.buffers.new_refill = 10; event(w)
        self.blocked(w, 'Unclassified')

    def test_discarded_death_and_grant_records_remain_in_audit(self):
        w = scene()
        w.lives['b'] = LifeState(30, 0, dead=True)
        w.souls.living.remove('b'); w.souls.deaths['b'] = 'death-1'
        event(w); w.kernel_plan('a').commit()
        frame = w.history.frames[0]
        change = next(x for x in frame['changes'] if x['holder'] == 'souls' and x['field'] == 'deaths')
        self.assertEqual(change['before']['b'], 'death-1')
        self.assertNotIn('b', change['after'])
        self.assertNotIn('death-1', w.memory.known['a'])

    def test_destroyed_participant_root_restores_same_physical_identity(self):
        w = scene()
        w.inventory.physical['b'] = replace(w.inventory.physical['b'], survives=False)
        w.lives['b'] = LifeState(30, 0, dead=True)
        w.souls.living.remove('b'); w.souls.deaths['b'] = 'death-1'
        event(w); w.kernel_plan('a').commit()
        self.assertTrue(w.inventory.physical['b'].survives)
        self.assertFalse(w.lives['b'].dead)
        self.assertEqual(set(w.inventory.physical), {'a', 'b', 'foe'})

    def test_deleted_or_reused_physical_history_rejects(self):
        for kind in ('removed', 'reused', 'ownership'):
            w = scene()
            if kind == 'removed':
                del w.inventory.physical['b']
            elif kind == 'reused':
                w.inventory.physical['b'] = replace(w.inventory.physical['b'], roots=('foe',))
            else:
                w.inventory.physical['b'] = replace(w.inventory.physical['b'], owner='outside')
            event(w); self.blocked(w, 'Physical history|provenance changed|ownership')

    def test_one_canonical_rest_epoch_controls_loop_use(self):
        w = scene(); event(w); w.kernel_plan('a').commit()
        w.buffers.completed_long_rest('a', 1)
        w.scheduler.regular_start('a', w.wallets['a'], 13)
        event(w, 'event-after-real-rest', 13)
        w.kernel_plan('a').commit()
        self.assertEqual(w.scheduler.loop_uses, {('a', 0), ('a', 1)})

    def test_external_current_record_replaces_stale_same_id_projection(self):
        w = scene(outsider=True)
        old = MaxHpRecord('external-trauma', 'monk.hero.iron-fist-master.ribcrusher-strike',
                          'outside', 'a', 3, ends_on_completed_rest=True)
        w.maxima['a'].records = (old,)
        new = replace(old, amount=10)
        w.external.effects['external-trauma'] = ExternalEffect('external-trauma', 'outside', 'a', 'maximum-hp', new)
        event(w); w.kernel_plan('a').commit()
        self.assertEqual(w.lives['a'].maximum_hp, 20)

    def test_world_marker_never_moves_before_snapshot(self):
        w = scene(capture=False)
        w.scheduler.now = ClockMarker(20)
        w.capture(('a', 'b', 'foe'))
        event(w, now=10)
        self.blocked(w, 'moved backward')


def main():
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(TemporalTests)
    result = unittest.TextTestRunner(verbosity=1).run(suite)
    root = Path(__file__).resolve().parents[1]
    report = {
        'status': 'PASS' if result.wasSuccessful() else 'FAIL',
        'scope': 'Unpromoted foundational temporal kernel only; seven integrations and actual notebook review remain',
        'testMethods': result.testsRun,
        'failures': len(result.failures), 'errors': len(result.errors),
        'fullTimeLoopOperational': False,
        'helperSha256': hashlib.sha256((root/'tools/temporal_playtest_rules.py').read_bytes()).hexdigest(),
    }
    (root/'docs/mechanics/TEMPORAL_KERNEL_VALIDATION.json').write_text(json.dumps(report, indent=2)+'\n', encoding='utf-8')
    print(json.dumps(report))
    raise SystemExit(0 if result.wasSuccessful() else 1)


if __name__ == '__main__':
    main()

```


## docs/mechanics/TEMPORAL_KERNEL_PLAYTEST.md

```
# Time Loop: foundational transaction candidate

**Status: implementation candidate, independent review pending. Full Time Loop remains unavailable.**

This implements a bounded part of `oracle.supplement.spiral-touched.spiral-touched-boon-v`. It does not change the original source, enable the ability in the playable class catalog, or close the full temporal interface. The notebook's twelve decisions are the authority for this candidate: [boundary conference](../../../../docs/audit/2026-10-08/full-game/GPT_TEMPORAL_WORLD_BOUNDARIES.md).

## What is implemented

The reference restores an immutable initiative-start snapshot through a preflighted transaction. It handles a finite development scene containing canonical Core life states, action wallets, selected feat shields, a temporal healing-consumption ledger, explicit Soul Bind/death identities, physical provenance, finite level-ground geometry, reward opportunities, external dependency records and character memory. The existing shared `LifeState`, `Wallet` and `BufferLedger` objects retain their identities. Spent resources and historical event records remain current.

The restore is permitted only after a complete atomic combat event, before round four, with an available Reaction and an unspent actual long-rest use. It never interrupts a damage, healing or command transaction. Preflight checks all registered state, source policies, physical dependencies and placements before charging anything. A prepared plan becomes stale if the registered world changes before commit. The single-thread reference requires the host scene lock through preflight and commit. Each committed restore also retains an engine/Director audit frame with the previous and resulting field values; that audit is never a source of character memory. The existing canonical BufferLedger completed-rest epoch also governs Time Loop's own long-rest use; there is no independent rest counter to diverge.

At commit, encounter initiative and the snapshot's Action/Bonus Action/Reaction allowances, RC and declared per-encounter uses return. Every outstanding Oracle Time Loop Reaction debt overlays the restored budgets. Only the owner's actual normal regular-start refresh clears that owner's debt. The new iteration has fresh round/turn identities; the rewind itself creates no turn start, pulse or recharge tick. Elapsed world time, real regular-marker count, RP and finite-use history remain unchanged.

## Conservation checks

| State | Bounded behavior |
| --- | --- |
| Core HP and Wounds | Restore numeric snapshot HP against the current legal maximum. A lower maximum clamps HP without damage or healing; a higher maximum does not increase snapshot HP. Critical Wound healing ceilings do not limit temporal assignment. |
| Maximum HP | Use the existing maximum-HP calculation. Current passive progression/gear and external sources remain. Snapshot internal Monk trauma may restore, except actual rest-ended records. Structural progression changes reject the fixture without a dedicated adapter. The host must supply current legal base/stat values. |
| Stable recovery | Preserve its original world deadline and event identity. An already resolved or expired recovery cannot replay; this kernel rejects such restoration rather than inventing a recovery rule. |
| Temporary HP | Restore the same grant ID and original snapshot amount only while its source's deadline/rest epoch/entity dependency remains valid. Supported IDs are Chef, Inspiring Leader, Field Medic, Soul Cage, Empowered Summoning and Blood Ritual. Unknown sources and linked riders reject the scene. |
| One-shot healing reduction | Keep canonical effect ID and all past events. Consumption keys include the iteration. Snapshot-available Agony can be available in a new iteration before its original expiry; snapshot-consumed or expired Agony remains unavailable. |
| Soul Bind | Original absolute deadline, exact death instance for bound-dead records. Undoing a later death removes that later active bind. No revival event or source cost is manufactured. |
| Rewards | A claim belongs to encounter origin, immutable reward source, opportunity kind and source-defined slot. Another death event or iteration cannot make another claim. |
| Physical derivatives | Traverse immutable provenance transitively. A wholly in-scope, reversible temporal entity can retire; its costs stay spent. Surviving harvested inventory, mixed material roots, external source slots or persistent enrollment conflicts block the restore. Already consumed material remains consumed. |
| Outsiders | Keep body state, inventory ownership, resource history and concentration records. A snapshot dependency on replaced external concentration blocks. Unimplemented external anatomy/control/suppression overlays also block. |
| Environment | Plan all participant positions simultaneously. Reject overlap, loss of support, and restrictions to a protected outsider's previously reachable ground area. This is deliberately limited to a finite orthogonal level ground plane, not flying, elevation, portals or mandatory growth. |
| Memory | The invoking Oracle and their immutable snapshot allies retain only facts individually perceived, experienced or received. Retained memories accumulate across loops. Enemy player characters receive no special knowledge; no hidden roster or Director facts enter memory automatically. |

## Required integrations still missing

The minimum seventeen-domain review is not complete. Seven major integrations are unimplemented: actual concentration/transformation callbacks; Druid form and conserved recharge clocks; creature lifecycle/corpse/persistent assets; device lifecycle/stock/commands; remaining structures, Choir and control lifecycles; the complete FeatWorld; and source-qualified control/healing pulses. Even the implemented foundational domains are bounded by the input policies above. For example, the external concentration map is a dependency projection, not the callback-bearing live concentration adapter.

`TemporalKernel.support_report()` reports that limit. `playable_plan()` always rejects until the full implementation and independent review exist. `kernel_plan()` is a development fixture interface, not a replacement for the complete Oracle feature. The host must disclose every active integration. A supplied unsupported holder rejects preflight; an empty registration is not a certificate that a real game scene is complete.

`TemporalHealingCommitLedger` can be passed as the one canonical healing ledger to existing helpers. Its canonical return IDs preserve `FeatWorld.commit_healing` removal semantics, while its historical consumption tokens are iteration-qualified. Agony creation/refresh/removal still needs the full feat adapter to synchronize active records; this kernel does not claim that synchronization exists.

## Validation and next review

Run `tools/validate_temporal_playtests.py`. The current suite contains 52 adversarial test methods, including stale-plan rejection, alias preservation, absolute expiry, dual-Oracle debts, reward replay, transitive physical derivatives, outsider enclosure without overlap and memory eligibility. [Validation report](TEMPORAL_KERNEL_VALIDATION.json) records the tested helper hash. The initial 46-test packet is preserved separately. A subsequent owner question in the notebook received a scope explanation, not an implementation disposition. The updated 52-test candidate therefore still requires actual independent findings.

Next, independently review this actual code and its narrow claims, repair defects, then add the seven missing integrations and exact source policies. Do not remove the Time Loop deferred status based on these tests. The final joint whole-game flow review and authorized GitHub push remain later gates.

```


## docs/mechanics/TEMPORAL_KERNEL_VALIDATION.json

```
{
  "status": "PASS",
  "scope": "Unpromoted foundational temporal kernel only; seven integrations and actual notebook review remain",
  "testMethods": 52,
  "failures": 0,
  "errors": 0,
  "fullTimeLoopOperational": false,
  "helperSha256": "682bb64b0b1804051b7c9cc74e0da552c16c35b680c5d53f69cc835c52a08e34"
}

```
