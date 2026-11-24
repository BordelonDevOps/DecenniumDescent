#if DECENNIUM_TEST_ONLY && (UNITY_EDITOR || HEADLESS_TESTS)
using System;
using System.Collections.Generic;
using System.Linq;
using System.Reflection;
using Decennium.Foundation.Laboratory;

namespace Decennium.Foundation.Tests
{
    public static partial class FoundationCases
    {
        // Labelled infrastructure probes use private access; no production context factory is added.
        private static NativeReadContextV1 ProbeReadContext(Simulation simulation, Snapshot snapshot)
            => (NativeReadContextV1)typeof(Simulation).GetMethod("CurrentReadContextV1", BindingFlags.Instance | BindingFlags.NonPublic)
                .Invoke(simulation, new object[] { snapshot });

        private sealed class ProjectionProbe : IReadStateProjectionV1
        {
            public ReadStateStampV1 Stamp { get; }
            internal ProjectionProbe(ReadStateStampV1 stamp) { Stamp = stamp; }
        }

        private sealed class OneReadStampProjection : IReadStateProjectionV1
        {
            private readonly ReadStateStampV1 stamp;
            internal int Reads;
            internal OneReadStampProjection(ReadStateStampV1 stamp) { this.stamp = stamp; }
            public ReadStateStampV1 Stamp => ++Reads == 1 ? stamp
                : throw new InvalidOperationException("A provider getter ran outside guarded publication.");
        }

        private sealed class ProjectionProbePolicy : ICommandPolicy, IReadStateProjectionPolicyV1
        {
            private readonly TestOnlyPolicy native = new TestOnlyPolicy();
            internal int Publications;
            internal Func<ReadStateStampV1, Snapshot, IReadStateProjectionV1> Create;
            public string ContentFingerprint => native.ContentFingerprint;
            public bool TestOnly => true;
            public Snapshot Initial() => native.Initial();
            public string ValidateState(Snapshot state) => native.ValidateState(state);
            public string Resolve(Snapshot state, Command command) => native.Resolve(state, command);
            public IReadStateProjectionV1 CreateReadProjection(ReadStateStampV1 stamp, Snapshot state)
            {
                Publications++;
                return Create == null ? new ProjectionProbe(stamp) : Create(stamp, state);
            }
        }

        private static void AddAdmittedReadContextCases(Dictionary<string, Action> cases)
        {
            cases.Add("int05_read_context_owner_generation_and_failure_isolation", () => {
                var policy = new ProjectionProbePolicy();
                var sim = new Simulation(policy, policy.Initial(), ExecutionProfile.Laboratory);
                var first = sim.Capture(); var context = ProbeReadContext(sim, first);
                Require(context != null && context.IsBoundTo(first) && !context.IsBoundTo(first.Copy()),
                    "Context was missing or transferable to an equal detached snapshot.");
                Require(typeof(ReadStateStampV1).GetConstructors().Length == 0
                    && typeof(NativeReadContextV1).GetConstructors().Length == 0, "A public context/stamp constructor escaped.");
                var other = new Simulation(policy, policy.Initial(), ExecutionProfile.Laboratory);
                var otherState = other.Capture(); var otherContext = ProbeReadContext(other, otherState);
                Require(!ReferenceEquals(context.Stamp, otherContext.Stamp) && !context.IsBoundTo(otherState), "Owner identity was transferable.");
                int count = policy.Publications;
                RejectUnchanged(sim, TestOnlyPolicy.Host(), new Command("denied", TestOnlyPolicy.ActorId, 0, CommandKind.Move, x:1), "Blocked");
                Require(policy.Publications == count && context.IsBoundTo(first), "Rejection replaced or repaired the projection.");
                Require(sim.Execute(TestOnlyPolicy.Host(), Open()).Outcome == Outcome.Committed, "Native interaction failed.");
                Require(!context.IsBoundTo(first) && policy.Publications == count+1, "Commit retained an earlier generation.");
                var second = sim.Capture(); var next = ProbeReadContext(sim, second); var bytes = Bytes(sim);
                Require(sim.Execute(TestOnlyPolicy.Host(), Open()).Outcome == Outcome.Duplicate && bytes.SequenceEqual(Bytes(sim))
                    && next.IsBoundTo(second) && policy.Publications == count+1, "Duplicate republished or changed state.");

                policy.Create = (stamp, copy) => { copy.Actors[0].X = 999; throw new InvalidOperationException("derived failure"); };
                var move = new Command("next", TestOnlyPolicy.ActorId, 1, CommandKind.Move, x:-1);
                Require(sim.Execute(TestOnlyPolicy.Host(), move).Outcome == Outcome.Committed && sim.Capture().Revision == 2
                    && sim.Capture().Actors.Single(x => x.Id == TestOnlyPolicy.ActorId).X == 0,
                    "Derived failure altered or rejected validated gameplay.");
                Require(!next.IsBoundTo(second) && ProbeReadContext(sim, sim.Capture()) == null, "Failure reused stale detail.");
                count = policy.Publications; bytes = Bytes(sim);
                Require(sim.Execute(TestOnlyPolicy.Host(), move).Outcome == Outcome.Duplicate
                    && bytes.SequenceEqual(Bytes(sim)) && policy.Publications == count, "Unavailable detail triggered retry repair.");

                policy.Create = (stamp, copy) => new ProjectionProbe(otherContext.Stamp);
                var foreign = new Simulation(policy, policy.Initial(), ExecutionProfile.Laboratory);
                Require(ProbeReadContext(foreign, foreign.Capture()) == null, "Foreign generation was accepted.");
                policy.Create = (stamp, copy) => { sim.Capture(); return new ProjectionProbe(stamp); };
                var reverse = new Command("reverse", TestOnlyPolicy.ActorId, 2, CommandKind.Move, x:1);
                Require(sim.Execute(TestOnlyPolicy.Host(), reverse).Outcome == Outcome.Committed
                    && ProbeReadContext(sim, sim.Capture()) == null, "Provider reentry was permitted or invalidated committed gameplay.");
                OneReadStampProjection once = null;
                policy.Create = (stamp, copy) => once = new OneReadStampProjection(stamp);
                Require(sim.Execute(TestOnlyPolicy.Host(), new Command("after-reentry", TestOnlyPolicy.ActorId, 3, CommandKind.Move, x:-1)).Outcome
                    == Outcome.Committed, "Publication guard did not reset after reentry failed.");
                var current = sim.Capture(); var frozen = ProbeReadContext(sim, current);
                Require(frozen != null && frozen.IsBoundTo(current) && frozen.IsBoundTo(current) && once.Reads == 1,
                    "An accepted provider getter escaped guarded preparation during a read.");
            });

            cases.Add("int05_materialized_conditions_strict_lookup_and_scope_cleanup", () => {
                var actor = TestOnlyPolicy.ActorId;
                var policy = new TestOnlySharedWorldPolicy(conditions: new ConditionCombatFixture(new[] { CCApply("int05-poison", "Poisoned", actor) }));
                var sim = World(policy); CCDispatch(sim, "int05-poison", actor);
                var snapshot = sim.Capture(); var bytes = Bytes(sim); var context = ProbeReadContext(sim, snapshot);
                var expected = TestOnlyClubAttackPolicy.ConditionsFor(snapshot, actor);
                var scope = typeof(ConditionHistory).Assembly.GetType("Decennium.Foundation.Laboratory.ConditionResolutionScope");
                var enter = scope.GetMethod("EnterRead", BindingFlags.Static | BindingFlags.NonPublic);
                Require(context != null, "Shared-world condition projection was not published.");
                using ((IDisposable)enter.Invoke(null, new object[] { context, snapshot })) {
                    var actual = TestOnlyClubAttackPolicy.ConditionsFor(snapshot, actor);
                    Require(actual.Now.Equals(expected.Now) && actual.View().Has(ConditionKind.Poisoned)
                        && ReferenceEquals(actual, TestOnlyClubAttackPolicy.ConditionsFor(snapshot, actor)), "Read did not reuse materialized native ledger.");
                    Throws<InvalidOperationException>(() => TestOnlyClubAttackPolicy.ConditionsFor(snapshot.Copy(), actor));
                    Throws<InvalidOperationException>(() => ConditionHistory.Restore(snapshot.Conditions.Single(x => x.Target == actor)));
                    Throws<InvalidOperationException>(() => actual.AdvanceTo(actual.Now));
                    Throws<InvalidOperationException>(() => actual.Cure(ConditionKind.Poisoned));
                }
                Require(ConditionHistory.Restore(snapshot.Conditions.Single(x => x.Target == actor)).Ledger.View().Has(ConditionKind.Poisoned)
                    && bytes.SequenceEqual(Bytes(sim)), "Strict scope escaped its lifetime or changed canonical state.");
                var outer = (IDisposable)enter.Invoke(null, new object[] { context, snapshot });
                var inner = (IDisposable)enter.Invoke(null, new object[] { context, snapshot });
                try {
                    Throws<InvalidOperationException>(() => outer.Dispose());
                    Throws<InvalidOperationException>(() => ConditionHistory.Restore(snapshot.Conditions.Single(x => x.Target == actor)));
                    inner.Dispose();
                    Throws<InvalidOperationException>(() => ConditionHistory.Restore(snapshot.Conditions.Single(x => x.Target == actor)));
                    outer.Dispose();
                    inner.Dispose(); // A retired inner frame must not reinstall its retired parent.
                    Require(ConditionHistory.Restore(snapshot.Conditions.Single(x => x.Target == actor)).Ledger.View().Has(ConditionKind.Poisoned),
                        "Repeated strict disposal contaminated a later legacy observation.");
                }
                finally { inner.Dispose(); outer.Dispose(); }
            });

            cases.Add("int05_private_canonical_comparison_preserves_validated_codec", () => {
                var sim = World(); var snapshot = sim.Capture(); var codec = new SnapshotCodec(); var bytes = codec.Encode(snapshot);
                var method = typeof(SnapshotCodec).GetMethod("MatchesValidatedPredecessor", BindingFlags.Instance | BindingFlags.NonPublic);
                Require(method != null && (bool)method.Invoke(codec, new object[] { snapshot, bytes }), "Private comparison disagrees with validated bytes.");
                var altered = snapshot.Copy(); altered.RandomState ^= 1;
                Require(!(bool)method.Invoke(codec, new object[] { altered, bytes }), "Opaque stored RNG bytes were ignored.");
                var invalid = snapshot.Copy(); invalid.Actors[0].Id = "";
                Throws<ArgumentException>(() => codec.Encode(invalid));
                Require(bytes.SequenceEqual(codec.Encode(snapshot)), "Comparison mutated source or expected bytes.");
            });
        }
    }
}
#endif
