# Completed independent review of the 52-test temporal kernel

ChatGPT said:

The 52-test revision fixes the six issues described in the packet, but I still find six concrete blockers inside the admitted foundational scope. These are not complaints about the seven integrations that are openly deferred.

The good news is that the core transaction pattern itself is substantially sound: preflight is non-mutating, stale-plan comparisons are broad, rollback-on-write-failure is present, world time is not assigned backward by the restore, reward opportunities survive iterations, same-ID Agony consumption uses iteration-qualified views, and the audit frame is separated from character memory. 
Pasted text

1. Reaction debt can be cleared by a fake regular start

Scheduler.regular_start() only requires:

no atomic event; and
actor in self.initiative.

It never verifies that this actor is actually the next actor at the initiative cursor. It also doesn't advance or validate the cursor. 
Pasted text

Reproducer
A loops.
B loops before A's legitimate refresh.
Debts = {A, B} and restored cursor is 0.
Suppose initiative is A, B, Foe.
Call regular_start('B', ...) immediately.

That succeeds even though A's regular turn should occur first. B's debt disappears and B's Reaction becomes available early.

Calling the same actor repeatedly can likewise manufacture global_regular increments.

Required repair

Either make this reference scheduler actually enforce initiative progression, or require an authoritative regular-start token/certificate that cannot be produced by an arbitrary caller.

At minimum:

Plain text
require(actor == initiative[cursor])

with canonical cursor/round advancement, separately distinguishing genuine extra turns.

If the host owns progression instead, regular_start() must receive and validate an authoritative actualRegularStartId; membership in the initiative tuple is insufficient.

This is a blocker because Reaction-debt conservation is claimed as implemented, not one of the seven missing domains. 
Pasted text

2. Environment geometry can be restored while its physical object remains destroyed

The physical and geometry adapters are not yet atomic with respect to registered environment anchors.

_physical_plan() snapshots physical history, but at restore only participant roots get their snapshot survives state restored:

Plain text
for actor in snap.roster:
    physical[actor] = ...survives=snapshot...

Environment roots do not. 
Pasted text
 
Pasted text

Meanwhile _geometry_plan() always restores snapshot environment anchors. 
Pasted text

Reproducer A

Snapshot has wall W:

PhysicalRecord('W', kind='root', survives=True)
environment anchor W blocks squares.

After snapshot:

wall is destroyed;
physical['W'].survives=False;
wall's blocking cells disappear.

Time Loop:

geometry restores the blocking wall;
physical record remains survives=False.

The world now has a wall geometrically present and physically destroyed.

Reproducer B

After snapshot, participant creates temporal wall W2:

PhysicalRecord(kind='temporal-entity', roots=...)
corresponding geometry.anchors['W2'].

_physical_plan() correctly schedules W2 for retirement, but _geometry_plan() filters retired poses, not retired anchors. W2 becomes survives=False while its wall cells remain active.

Required repair

Registered rewindable environment anchors need explicit physical identity binding.

For the current bounded model:

require each physical environment anchor to have a matching canonical PhysicalRecord;
validate anchor key == anchor identity;
restore snapshot environment-root existence consistently with geometry;
filter anchors by retire, just as poses are filtered;
reject nonphysical/hazard anchors unless they have a separate explicit source policy.

This is an admitted inventory-provenance + geometry defect, not RemainingWorld work.

3. New post-snapshot external concentration dependencies can be silently ignored

The kernel correctly verifies the snapshot dependencies:

Plain text
for dep in snap.dependencies:
    require(current concentration == snapshot concentration)

but it never reconciles new current self.external.dependencies added after snapshot. 
Pasted text

Reproducer
Snapshot has no outside concentration dependency on B.
After snapshot, outsider casts a persistent concentration effect on B.
Host records:
external.concentration['outside']='cast-new'
external.dependencies += ExternalDependency('new-effect','b','outside','cast-new')
No supported ExternalEffect adapter exists for that effect.
Time Loop preflight passes.

The participant is restored while the current external dependency is simply ignored. Depending on what that effect did, this can erase its consequences without ending the outsider's concentration, exactly the state split we said must never occur.

Required repair

Compare current external dependencies against the snapshot/dependency adapters.

For every current external dependency targeting a restored participant:

exact supported reconciliation exists → preserve/overlay it;
otherwise → preflight failure.

Similarly, a snapshot dependency that has disappeared as a live dependency cannot be accepted merely because the caster's concentration ID happens to have the same string.

The live effect/dependency relationship must remain authoritative.

4. Maximum-HP temporal policy is inferred from "monk." string prefixes

This is the largest source-policy hole.

The code currently treats:

Plain text
owner in roster AND source.startswith('monk.')

as the definition of a rewindable internal max-HP record. Everything else is treated as current/conserved unless supplied as an external effect. 
Pasted text

That is not source-qualified enough.

Reproducer A: unknown participant effect survives incorrectly

After snapshot, participant A gains:

Plain text
MaxHpRecord(
    application_id='new-buff',
    source='some.participant.temporary.maxhp',
    owner='a',
    target='a',
    ...
)

No progression-signature change occurs.

The record isn't monk.*, so Time Loop silently preserves it even if it is encounter-local and should disappear.

Reproducer B: unrelated Monk record rewinds incorrectly

A valid permanent/passive Monk max-HP record whose source begins monk. is automatically treated as temporal trauma and can be reconstructed from snapshot.

There is no evidence that every Monk-owned max-HP record has that policy.

Required repair

Replace prefix inference with an explicit source-policy table/adapter:

Plain text
application/source → {
    REWIND_TO_SNAPSHOT,
    CONSERVE_CURRENT,
    WORLD_ABSOLUTE,
    REST_BOUND,
    UNSUPPORTED
}

Only the exact reviewed trauma sources should receive the existing special reconciliation. Unknown participant-owned MaxHpRecords targeting roster members must make that snapshot unavailable.

The guide currently claims a narrower rule—“snapshot internal Monk trauma may restore”—than the code actually enforces. 
Pasted text

5. BufferLedger validation allows a malformed canonical ledger to pass

Because BufferLedger is not validated with shape(), the current test is only:

Plain text
set(vars(buffers)) <= allowed_fields

Pasted text

That detects extra fields but permits missing required fields.

Reproducer A

Delete:

Plain text
del buffers.damage_events

With no code path needing that field during this fixture, _validate_holders() can still pass because the remaining keys are a subset of the allowlist.

Time Loop commits against a malformed canonical BufferLedger.

Reproducer B

Create an internally inconsistent active mapping:

Plain text
buffers.active['a'] = 'shield'
buffers.grants['shield'].target = 'b'

If the projected temp-HP values happen to be arranged to satisfy the numeric check, there is no explicit invariant requiring:

active-key target == grant target;
active grant state == "active";
active grant has positive remaining HP;
grant ID exists exactly once as the active identity.
Required repair

Require the canonical minimum field set, with only explicitly supported optional fields such as lazily-created ordinary_cast_events.

Also validate active-ledger invariants before capture and before plan construction.

This is exactly the kind of malformed active state that the kernel says it rejects, so it belongs in this review rather than a future integration.

6. A source-illegal pending Soul Bind can be captured and restored

The Soul identity adapter preserves absolute deadlines correctly, but it doesn't validate that a pending Soul Bind is actually attached to a living dying creature at 0 HP.

The current restoration condition for a non-bound record is effectively only:

Plain text
target in living

plus deadline. 
Pasted text

Reproducer

Before capture:

B is living at 25/30 HP;
create participant-owned:
SoulRecord(... SoulBind('b','pending',60)).

Capture accepts it.

After an event, Time Loop restores B to 25 HP and restores the pending Soul Bind, because B is in the living set and the deadline hasn't expired.

But the reviewed Soul Bind source permits pending state only on a living dying 0-HP target; positive HP should already have ended that tether.

Required repair

Validate SoulRecord invariants both at snapshot and preflight:

Pending

target living;
target HP == 0;
target not Stable;
target not Dead;
no death-instance binding;
bind identity matches target.

Bound

target Dead;
death_instance exists;
it exactly matches the canonical current death instance.

Also validate dictionary/application identity consistency.

If the current source state violates those predicates, the snapshot is incomplete/unavailable rather than serializing an impossible Soul Bind state.

Things I do not consider blockers here

Several important areas look correct within the admitted scope:

transaction construction itself is non-mutating and commit has compare-and-swap stale checks plus rollback on write failure; 
Pasted text
all previous Time Loop Reaction debts are overlaid during a later rewind—the defect is only in proving when they may be cleared; 
Pasted text
world elapsed time is not rewound by the transaction;
reward claims use immutable opportunities rather than fresh death IDs;
same-ID Agony restoration properly separates canonical identity, historical consumption and iteration-qualified availability;
Stable deadlines are not rebased and resolved/expired recovery is conservatively rejected;
restored HP is recomputed against current maximum and Critical's healing ceiling is not misused;
transferred ordinary inventory remains current;
surviving transferable/mixed derivatives conservatively block;
direct outsider overlap, support loss and reachable-area enclosure are checked;
snapshot-alliance memory and cumulative retained memory are bounded correctly;
audit frames are engine history and don't leak into character memory;
playable_plan() remains hard-gated and the documentation accurately says seven integrations are still missing. 
Pasted text
Disposition

So I would record the 52-test revision as:

IMPLEMENTED FOUNDATIONAL CANDIDATE — six bounded-kernel blockers remain. Full Time Loop remains unavailable.

I would fix these before adding the seven larger integrations, particularly #1 scheduler legitimacy, #2 environment/physical atomicity, and #3 current external-dependency reconciliation, because those are foundational assumptions the later adapters will rely on.

This does not reopen the already reviewed spells/feats, does not constitute Time Loop closure, and does not satisfy the later whole-game flow/GitHub gate.
