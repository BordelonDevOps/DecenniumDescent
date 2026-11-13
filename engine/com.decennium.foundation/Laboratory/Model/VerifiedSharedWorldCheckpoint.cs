#if DECENNIUM_TEST_ONLY && (UNITY_EDITOR || DEVELOPMENT_BUILD || HEADLESS_TESTS)
using System;
using System.Linq;

namespace Decennium.Foundation.Laboratory
{
    public sealed partial class TestOnlySharedWorldPolicy : IVerifiedCommandPolicy, IVerifiedSimulationConstruction
    {
        private bool verifiedPlanningPassage;

        internal TestOnlySharedWorldPolicy EnableVerifiedPlanningPassage()
        {
            if (initializationStarted || !connectedRecipe4Batch || nextCharterPlanProfile == null)
                throw new InvalidOperationException("Select verified charter passage before starting the connected expedition.");
            verifiedPlanningPassage = true;
            return this;
        }

        bool IVerifiedSimulationConstruction.SupportsVerifiedConstruction => verifiedPlanningPassage;

        private int VerifiedExpeditionWireSchema => connectedStowedVial ? Snapshot.ConnectedStowedVialSchema
            : connectedCarriedVial ? Snapshot.ConnectedCarriedVialSchema : Snapshot.ConnectedRecipe4BatchSchema;

        Func<VerifiedSimulationOrigin, IVerifiedCommandCheckpoint> IVerifiedSimulationConstruction.ValidateForConstruction(Snapshot state)
        {
            if (!verifiedPlanningPassage || !initializationStarted || state?.TestOnly != true
                || state.ContentFingerprint != ContentFingerprint || state.WireSchemaVersion != VerifiedExpeditionWireSchema)
                throw new ArgumentException("Verified construction is unavailable for this selected content.");
            var known = new PlanningPassage(ContentFingerprint, nextCharterPlanProfile.Terms.BindingKey);
            byte[] canonical = null;
            PlanningPassage? passage = null;
            string failure = ValidateState(state, () => ReconstructCanonicalHistory(state, known, out canonical, out passage));
            if (failure != null) throw new ArgumentException(failure);
            if (canonical == null || !passage.HasValue)
                throw new ArgumentException("Verified construction did not complete history validation.");
            return origin => {
                var owned = origin?.Capture();
                if (owned == null || !passage.Value.Covers(owned, nextCharterPlanProfile.Terms, owned.Revision)
                    || !new SnapshotCodec().Encode(owned).SequenceEqual(canonical)) return null;
                return new VerifiedSharedWorldCheckpoint(this, origin, owned.Revision, canonical, passage);
            };
        }

        IVerifiedCommandCheckpoint IVerifiedCommandPolicy.Seal(VerifiedSimulationOrigin origin)
        {
            var state = origin?.Capture();
            if (!connectedRecipe4Batch || !initializationStarted || state?.TestOnly != true
                || state.ContentFingerprint != ContentFingerprint || state.WireSchemaVersion != VerifiedExpeditionWireSchema)
                return null;
            var codec = new SnapshotCodec();
            byte[] canonical = codec.Encode(state);
            PlanningPassage? passage = null;
            if (verifiedPlanningPassage) {
                var replay = Initial();
                replay.SchemaVersion = state.SchemaVersion;
                var known = new PlanningPassage(ContentFingerprint, nextCharterPlanProfile.Terms.BindingKey);
                foreach (var receipt in state.Receipts.OrderBy(x => x.Revision)) {
                    var traversal = known.PendingCrossing(replay, nextCharterPlanProfile.Terms);
                    if (!ReplayReceipt(replay, receipt)) return null;
                    known = known.Advance(replay, traversal, receipt);
                    if (known.Found) break;
                }
                // Construction already replayed and compared the full owned origin.
                // The first crossing cannot be replaced by any subsequent receipt.
                passage = known.ThroughValidatedOrigin(state.Revision);
            }
            return new VerifiedSharedWorldCheckpoint(this, origin, state.Revision, canonical, passage);
        }

        private readonly struct PlanningPassage
        {
            private readonly string fingerprint;
            private readonly string termsBinding;
            private readonly long throughRevision;
            private readonly CommandReceipt start;
            private readonly CommandReceipt completion;

            internal PlanningPassage(string fingerprint, string termsBinding, long throughRevision = 0,
                CommandReceipt start = null, CommandReceipt completion = null)
            {
                this.fingerprint = fingerprint;
                this.termsBinding = termsBinding;
                this.throughRevision = throughRevision;
                this.start = start;
                this.completion = completion;
            }

            internal bool Covers(Snapshot state, NextCharterPlanTerms terms, long cutoff)
                => state.ContentFingerprint == fingerprint && terms.BindingKey == termsBinding
                    && state.Revision == throughRevision && cutoff <= throughRevision;

            internal long StartThrough(long cutoff)
                => completion != null && completion.Revision <= cutoff ? start.Revision : 0;

            internal bool Found => start != null;

            internal PlanningPassage ThroughValidatedOrigin(long revision)
                => new PlanningPassage(fingerprint, termsBinding, revision, start, completion);

            internal WorldTraversalRecord PendingCrossing(Snapshot state, NextCharterPlanTerms terms)
                => start == null ? PendingPlanningCrossing(state, terms) : null;

            internal PlanningPassage Advance(Snapshot state, WorldTraversalRecord traversal, CommandReceipt receipt)
            {
                var crossing = CompletedPlanningCrossing(state, traversal);
                return new PlanningPassage(fingerprint, termsBinding, receipt.Revision, start ?? crossing?.Copy(),
                    completion ?? (crossing == null ? null : receipt.Copy()));
            }
        }

        private sealed class VerifiedSharedWorldCheckpoint : IVerifiedCommandCheckpoint, IVerifiedCommandResolution
        {
            private readonly TestOnlySharedWorldPolicy policy;
            private readonly VerifiedSimulationOrigin owner;
            private readonly long revision;
            private readonly string fingerprint;
            private readonly byte[] canonicalPredecessor;
            private readonly PlanningPassage? passage;

            internal VerifiedSharedWorldCheckpoint(TestOnlySharedWorldPolicy policy, VerifiedSimulationOrigin owner,
                long revision, byte[] canonicalPredecessor, PlanningPassage? passage)
            {
                this.policy = policy;
                this.owner = owner;
                this.revision = revision;
                fingerprint = policy.ContentFingerprint;
                this.canonicalPredecessor = canonicalPredecessor;
                this.passage = passage;
            }

            public bool Resolves(Command command)
                => passage.HasValue && (command.Kind == CommandKind.StartNextCharterPlan || command.Kind == CommandKind.AdvanceClock);

            public string ResolveNext(VerifiedSimulationOrigin origin, Snapshot predecessor, Snapshot candidate, Command command)
            {
                if (!Resolves(command))
                    return policy.Resolve(candidate, command);
                string failure = VerifyOwner(origin, predecessor);
                if (failure != null) return failure;
                var codec = new SnapshotCodec();
                if (!codec.Encode(predecessor).SequenceEqual(canonicalPredecessor)
                    || !codec.Encode(candidate).SequenceEqual(canonicalPredecessor))
                    return "InvalidVerifiedPrefixBytes";
                return policy.Resolve(candidate, command, passage, verifiedExecution: true);
            }

            private string VerifyOwner(VerifiedSimulationOrigin origin, Snapshot predecessor)
                => !ReferenceEquals(owner, origin) || policy.ContentFingerprint != fingerprint
                    || predecessor.Revision != revision || predecessor.ContentFingerprint != fingerprint
                    || !predecessor.TestOnly || predecessor.WireSchemaVersion != policy.VerifiedExpeditionWireSchema
                    || passage.HasValue && !passage.Value.Covers(predecessor, policy.nextCharterPlanProfile.Terms, revision)
                    ? "InvalidVerifiedPrefixOwner" : null;

            public string VerifyNext(VerifiedSimulationOrigin origin, Snapshot predecessor, Snapshot candidate,
                CommandReceipt submittedReceipt, out IVerifiedCommandCheckpoint successor)
            {
                successor = null;
                string ownerFailure = VerifyOwner(origin, predecessor);
                if (ownerFailure != null) return ownerFailure;
                if (candidate.Revision != revision + 1 || candidate.ContentFingerprint != fingerprint || !candidate.TestOnly
                    || candidate.WireSchemaVersion != predecessor.WireSchemaVersion || candidate.SchemaVersion != predecessor.SchemaVersion
                    || candidate.Receipts.Length != predecessor.Receipts.Length + 1 || submittedReceipt.Revision != candidate.Revision
                    || !SameReceipt(candidate.Receipts[candidate.Receipts.Length - 1], submittedReceipt))
                    return "InvalidVerifiedSuccessorReceipt";
                for (int i = 0; i < predecessor.Receipts.Length; i++)
                    if (!SameReceipt(candidate.Receipts[i], predecessor.Receipts[i])) return "InvalidVerifiedSuccessorReceipt";

                byte[] nextBytes = null;
                PlanningPassage? nextPassage = null;
                string failure = policy.ValidateState(candidate,
                    () => VerifyCanonicalTransition(predecessor, candidate, submittedReceipt, out nextBytes, out nextPassage));
                if (failure != null) return failure;
                successor = new VerifiedSharedWorldCheckpoint(policy, owner, candidate.Revision, nextBytes, nextPassage);
                return null;
            }

            private string VerifyCanonicalTransition(Snapshot predecessor, Snapshot candidate, CommandReceipt submittedReceipt,
                out byte[] nextBytes, out PlanningPassage? nextPassage)
            {
                nextBytes = null;
                nextPassage = null;
                var codec = new SnapshotCodec();
                if (!codec.Encode(predecessor).SequenceEqual(canonicalPredecessor)) return "InvalidVerifiedPrefixBytes";

                // Independently decode the sealed bytes. No references from the tentative
                // resolver result participate in reconstructing the next rule state.
                var replay = codec.Decode(canonicalPredecessor);
                var traversal = passage?.PendingCrossing(replay, policy.nextCharterPlanProfile.Terms);
                if (!policy.ReplayReceipt(replay, submittedReceipt, passage, verifiedExecution: true)) return "InvalidSharedWorldHistory";
                var reconstructed = codec.Encode(replay);
                if (!codec.Encode(candidate).SequenceEqual(reconstructed)) return "InvalidSharedWorldReplay";
                nextPassage = passage?.Advance(replay, traversal, submittedReceipt);
                nextBytes = reconstructed;
                return null;
            }

            private static bool SameReceipt(CommandReceipt first, CommandReceipt second)
                => first.Revision == second.Revision && first.Id == second.Id
                    && first.Principal == second.Principal && first.Fingerprint == second.Fingerprint;
        }
    }
}
#endif
