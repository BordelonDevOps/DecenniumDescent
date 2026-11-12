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
        private static void RequireSameCommandResult(CommandResult expected, CommandResult actual)
        {
            Require(expected.Outcome == actual.Outcome && expected.Code == actual.Code
                && expected.Revision == actual.Revision && expected.IsSuspended == actual.IsSuspended
                && expected.TacticalDecisionAt == actual.TacticalDecisionAt && expected.ReachedClock == actual.ReachedClock,
                "Strict replay and verified prefix produced different public command results.");
        }

        private static void AddVerifiedCommandCases(Dictionary<string, Action> cases)
        {
            cases.Add("int03_verified_prefix_owned_atomic_and_corrupt_restore_rejected", () =>
            {
                var policy = BatchPolicy();
                var initial = policy.Initial();
                var fast = new Simulation(policy, initial, ExecutionProfile.Laboratory, CommandVerification.VerifiedPrefix);
                var reference = new Simulation(BatchPolicy(), initial, ExecutionProfile.Laboratory);
                var external = initial.Copy();
                var peer = new Simulation(policy, external, ExecutionProfile.Laboratory, CommandVerification.VerifiedPrefix);
                external.Actors[0].X++;
                external.RandomState++;
                var grant = new Authority("TEST_ONLY.p1-host", new[] { PlanHero }, canAdvanceClock: true);
                var revoked = new Authority("TEST_ONLY.p1-host", Array.Empty<string>());
                var opening = new Command("p1.opening", PlanHero, 0, CommandKind.BeginWorldStep, "walk", 1, 0);
                var advance = new Command("p1.advance", PlanHero, 1, CommandKind.AdvanceClock, x: 2, y: 1);
                var codec = new SnapshotCodec();
                var checkpointField = typeof(Simulation).GetField("checkpoint", BindingFlags.Instance | BindingFlags.NonPublic);
                var originField = typeof(Simulation).GetField("verificationOrigin", BindingFlags.Instance | BindingFlags.NonPublic);
                var firstCheckpoint = (IVerifiedCommandCheckpoint)checkpointField.GetValue(fast);
                var origin = (VerifiedSimulationOrigin)originField.GetValue(fast);
                var original = Bytes(fast);
                Require(Bytes(peer).SequenceEqual(original), "The external constructor input could mutate the owned root.");

                var disposable = fast.Capture();
                disposable.Actors[0].X++;
                disposable.Objects = Array.Empty<ObjectState>();
                disposable.RandomState++;
                Require(Bytes(fast).SequenceEqual(original), "A caller capture mutated the live predecessor.");

                RequireSameCommandResult(reference.Execute(revoked, opening), fast.Execute(revoked, opening));
                var rejected = new Command("p1.invalid-step", PlanHero, 0, CommandKind.BeginWorldStep, "walk", 4, 0);
                RequireSameCommandResult(reference.Execute(grant, rejected), fast.Execute(grant, rejected));
                Require(Bytes(fast).SequenceEqual(original) && ReferenceEquals(checkpointField.GetValue(fast), firstCheckpoint),
                    "An ordinary denial advanced the verified prefix.");

                checkpointField.SetValue(fast, checkpointField.GetValue(peer));
                var foreign = checkpointField.GetValue(fast);
                Require(fast.Execute(grant, opening).Code == "InvalidResult" && Bytes(fast).SequenceEqual(original)
                    && ReferenceEquals(checkpointField.GetValue(fast), foreign),
                    "The transaction accepted or silently resealed another session's checkpoint.");
                checkpointField.SetValue(fast, firstCheckpoint);

                var committed = reference.Execute(grant, opening);
                Require(committed.Outcome == Outcome.Committed, "The strict reference could not start the ordinary traversal.");
                var falseCandidate = reference.Capture();
                uint random = falseCandidate.RandomState;
                RandomV1.Next(ref random);
                falseCandidate.RandomState = random;
                var receipt = falseCandidate.Receipts.Single();
                var mismatch = firstCheckpoint.VerifyNext(origin, fast.Capture(), falseCandidate, receipt, out var successor);
                Require(mismatch == "InvalidSharedWorldReplay" && successor == null
                    && Bytes(fast).SequenceEqual(original) && ReferenceEquals(checkpointField.GetValue(fast), firstCheckpoint),
                    "An encodable but false candidate produced a successor checkpoint.");
                var differentPredecessor = fast.Capture();
                differentPredecessor.RandomState = random;
                Require(firstCheckpoint.VerifyNext(origin, differentPredecessor, reference.Capture(), receipt, out successor)
                    == "InvalidVerifiedPrefixBytes" && successor == null, "A different predecessor was silently resealed.");

                var encodedForgery = codec.Encode(falseCandidate);
                Throws<ArgumentException>(() => new Simulation(BatchPolicy(), codec.Decode(encodedForgery),
                    ExecutionProfile.Laboratory, CommandVerification.VerifiedPrefix));
                Throws<ArgumentException>(() => new Simulation(BatchPolicy(), codec.Decode(encodedForgery), ExecutionProfile.Laboratory));
                var forgedHistory = reference.Capture();
                string originalFingerprint = forgedHistory.Receipts[0].Fingerprint;
                forgedHistory.Receipts[0].Fingerprint = originalFingerprint.Replace("|walk|0|1|0", "|walk|0|0|1");
                Require(forgedHistory.Receipts[0].Fingerprint != originalFingerprint
                    && CommandHistory.Read(forgedHistory.Receipts[0]).Y == 1, "The receipt control was not a plausible command.");
                var encodedHistoryForgery = codec.Encode(forgedHistory);
                Throws<ArgumentException>(() => new Simulation(BatchPolicy(), codec.Decode(encodedHistoryForgery),
                    ExecutionProfile.Laboratory, CommandVerification.VerifiedPrefix));
                Throws<ArgumentException>(() => new Simulation(BatchPolicy(), codec.Decode(encodedHistoryForgery), ExecutionProfile.Laboratory));
                Throws<InvalidOperationException>(() => policy.EnableDodgeAction());
                Throws<InvalidOperationException>(() => new Simulation(BatchPolicy(), initial,
                    ExecutionProfile.Release, CommandVerification.VerifiedPrefix));
                var otherPolicy = new TestOnlyPolicy();
                Throws<ArgumentException>(() => new Simulation(otherPolicy, otherPolicy.Initial(),
                    ExecutionProfile.Laboratory, CommandVerification.VerifiedPrefix));

                RequireSameCommandResult(committed, fast.Execute(grant, opening));
                var afterFirst = Bytes(fast);
                var afterCheckpoint = checkpointField.GetValue(fast);
                Require(!ReferenceEquals(afterCheckpoint, firstCheckpoint) && afterFirst.SequenceEqual(Bytes(reference)),
                    "The valid command did not advance the owned state and checkpoint together.");
                var conflict = new Command(opening.Id, PlanHero, 0, CommandKind.BeginWorldStep, "walk", 0, 1);
                var stale = new Command("p1.stale", PlanHero, 0, CommandKind.AdvanceClock, x: 1, y: 1);
                RequireSameCommandResult(reference.Execute(grant, opening), fast.Execute(grant, opening));
                RequireSameCommandResult(reference.Execute(revoked, opening), fast.Execute(revoked, opening));
                RequireSameCommandResult(reference.Execute(grant, conflict), fast.Execute(grant, conflict));
                RequireSameCommandResult(reference.Execute(grant, stale), fast.Execute(grant, stale));
                Require(Bytes(fast).SequenceEqual(afterFirst) && ReferenceEquals(checkpointField.GetValue(fast), afterCheckpoint),
                    "Retry handling changed the committed state or checkpoint.");

                var restored = new Simulation(BatchPolicy(), codec.Decode(afterFirst), ExecutionProfile.Laboratory,
                    CommandVerification.VerifiedPrefix);
                var advanced = reference.Execute(grant, advance);
                Require(advanced.Outcome == Outcome.Committed, "The strict reference did not finish the actual paid step.");
                RequireSameCommandResult(advanced, fast.Execute(grant, advance));
                RequireSameCommandResult(advanced, restored.Execute(grant, advance));
                Require(Bytes(reference).SequenceEqual(Bytes(fast)) && Bytes(fast).SequenceEqual(Bytes(restored)),
                    "Restoring into a new owned checkpoint changed the ordinary continuation.");
            });

            cases.Add("int03_verified_prefix_preserves_receipt_capacity_and_duplicate", () =>
            {
                var policy = BatchPolicy();
                var fast = new Simulation(policy, policy.Initial(), ExecutionProfile.Laboratory, CommandVerification.VerifiedPrefix);
                var grant = new Authority("TEST_ONLY.p1-capacity", new[] { PlanHero }, canAdvanceClock: true);
                Command last = null;
                for (int i = 0; i < 512; i++) {
                    last = new Command("p1.capacity." + i, PlanHero, i, CommandKind.AdvanceClock, x: 1, y: 1);
                    var result = fast.Execute(grant, last);
                    Require(result.Outcome == Outcome.Committed, "The live history failed before capacity: " + result.Code);
                }
                var reference = new Simulation(BatchPolicy(), fast.Capture(), ExecutionProfile.Laboratory);
                var before = Bytes(fast);
                var excess = new Command("p1.capacity.excess", PlanHero, 512, CommandKind.AdvanceClock, x: 1, y: 1);
                var expected = reference.Execute(grant, excess);
                Require(expected.Code == "SessionCapacityReached", "The reference did not reach the existing receipt limit.");
                RequireSameCommandResult(expected, fast.Execute(grant, excess));
                RequireSameCommandResult(reference.Execute(grant, last), fast.Execute(grant, last));
                Require(Bytes(reference).SequenceEqual(before) && Bytes(fast).SequenceEqual(before),
                    "Capacity rejection or duplicate changed the existing history.");
            });
        }
    }
}
#endif
