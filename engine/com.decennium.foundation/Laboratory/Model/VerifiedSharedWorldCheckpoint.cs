#if DECENNIUM_TEST_ONLY && (UNITY_EDITOR || DEVELOPMENT_BUILD || HEADLESS_TESTS)
using System;
using System.Linq;

namespace Decennium.Foundation.Laboratory
{
    public sealed partial class TestOnlySharedWorldPolicy : IVerifiedCommandPolicy
    {
        IVerifiedCommandCheckpoint IVerifiedCommandPolicy.Seal(VerifiedSimulationOrigin origin)
        {
            var state = origin?.Capture();
            if (!connectedRecipe4Batch || !initializationStarted || state?.TestOnly != true
                || state.ContentFingerprint != ContentFingerprint || state.WireSchemaVersion != Snapshot.ConnectedRecipe4BatchSchema)
                return null;
            return new VerifiedSharedWorldCheckpoint(this, origin, state.Revision, new SnapshotCodec().Encode(state));
        }

        private sealed class VerifiedSharedWorldCheckpoint : IVerifiedCommandCheckpoint
        {
            private readonly TestOnlySharedWorldPolicy policy;
            private readonly VerifiedSimulationOrigin owner;
            private readonly long revision;
            private readonly string fingerprint;
            private readonly byte[] canonicalPredecessor;

            internal VerifiedSharedWorldCheckpoint(TestOnlySharedWorldPolicy policy, VerifiedSimulationOrigin owner,
                long revision, byte[] canonicalPredecessor)
            {
                this.policy = policy;
                this.owner = owner;
                this.revision = revision;
                fingerprint = policy.ContentFingerprint;
                this.canonicalPredecessor = canonicalPredecessor;
            }

            public string VerifyNext(VerifiedSimulationOrigin origin, Snapshot predecessor, Snapshot candidate,
                CommandReceipt submittedReceipt, out IVerifiedCommandCheckpoint successor)
            {
                successor = null;
                if (!ReferenceEquals(owner, origin) || policy.ContentFingerprint != fingerprint
                    || predecessor.Revision != revision || predecessor.ContentFingerprint != fingerprint
                    || !predecessor.TestOnly || predecessor.WireSchemaVersion != Snapshot.ConnectedRecipe4BatchSchema)
                    return "InvalidVerifiedPrefixOwner";
                if (candidate.Revision != revision + 1 || candidate.ContentFingerprint != fingerprint || !candidate.TestOnly
                    || candidate.WireSchemaVersion != predecessor.WireSchemaVersion || candidate.SchemaVersion != predecessor.SchemaVersion
                    || candidate.Receipts.Length != predecessor.Receipts.Length + 1 || submittedReceipt.Revision != candidate.Revision
                    || !SameReceipt(candidate.Receipts[candidate.Receipts.Length - 1], submittedReceipt))
                    return "InvalidVerifiedSuccessorReceipt";
                for (int i = 0; i < predecessor.Receipts.Length; i++)
                    if (!SameReceipt(candidate.Receipts[i], predecessor.Receipts[i])) return "InvalidVerifiedSuccessorReceipt";

                byte[] nextBytes = null;
                string failure = policy.ValidateState(candidate,
                    () => VerifyCanonicalTransition(predecessor, candidate, submittedReceipt, out nextBytes));
                if (failure != null) return failure;
                successor = new VerifiedSharedWorldCheckpoint(policy, owner, candidate.Revision, nextBytes);
                return null;
            }

            private string VerifyCanonicalTransition(Snapshot predecessor, Snapshot candidate, CommandReceipt submittedReceipt,
                out byte[] nextBytes)
            {
                nextBytes = null;
                var codec = new SnapshotCodec();
                if (!codec.Encode(predecessor).SequenceEqual(canonicalPredecessor)) return "InvalidVerifiedPrefixBytes";

                // Independently decode the sealed bytes. No references from the tentative
                // resolver result participate in reconstructing the next rule state.
                var replay = codec.Decode(canonicalPredecessor);
                if (!policy.ReplayReceipt(replay, submittedReceipt)) return "InvalidSharedWorldHistory";
                var reconstructed = codec.Encode(replay);
                if (!codec.Encode(candidate).SequenceEqual(reconstructed)) return "InvalidSharedWorldReplay";
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
