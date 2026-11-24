using System;

namespace Decennium.Foundation
{
    /// <summary>Trusted policy capability. Called only after authoritative state validation.</summary>
    public interface IReadStateProjectionPolicyV1
    {
        IReadStateProjectionV1 CreateReadProjection(ReadStateStampV1 stamp, Snapshot detachedValidatedCurrent);
    }

    public interface IReadStateProjectionV1
    {
        ReadStateStampV1 Stamp { get; }
    }

    internal sealed class ReadStateOwnerV1
    {
        internal ReadStateStampV1 Current;
    }

    /// <summary>Unserialized identity of one owning simulation generation; never a gameplay grant.</summary>
    public sealed class ReadStateStampV1
    {
        private readonly ReadStateOwnerV1 owner;
        private readonly ICommandPolicy policy;
        public long Revision { get; }
        public int SchemaVersion { get; }
        public int WireSchemaVersion { get; }
        public RuleTime RuleClock { get; }
        public string ContentFingerprint { get; }
        public bool TestOnly { get; }

        internal ReadStateStampV1(ReadStateOwnerV1 owner, ICommandPolicy policy, Snapshot state)
        {
            this.owner = owner;
            this.policy = policy;
            Revision = state.Revision;
            SchemaVersion = state.SchemaVersion;
            WireSchemaVersion = state.WireSchemaVersion;
            RuleClock = state.RuleClock;
            ContentFingerprint = state.ContentFingerprint;
            TestOnly = state.TestOnly;
        }

        internal bool IsCurrent => ReferenceEquals(owner.Current, this);

        internal bool Matches(ReadStateOwnerV1 expectedOwner, ICommandPolicy expectedPolicy, Snapshot state)
            => IsCurrent && ReferenceEquals(owner, expectedOwner) && ReferenceEquals(policy, expectedPolicy)
                && state != null && Revision == state.Revision && SchemaVersion == state.SchemaVersion
                && WireSchemaVersion == state.WireSchemaVersion && RuleClock == state.RuleClock
                && ContentFingerprint == state.ContentFingerprint && TestOnly == state.TestOnly;
    }

    /// <summary>One trusted observation, bound to the exact detached snapshot passed to its policy.</summary>
    public sealed class NativeReadContextV1
    {
        private readonly Snapshot snapshot;
        private readonly VerifiedSimulationOrigin verificationOrigin;
        public ReadStateStampV1 Stamp { get; }
        public IReadStateProjectionV1 Projection { get; }

        internal NativeReadContextV1(ReadStateStampV1 stamp, IReadStateProjectionV1 projection, Snapshot snapshot,
            VerifiedSimulationOrigin verificationOrigin)
        {
            Stamp = stamp;
            Projection = projection;
            this.snapshot = snapshot;
            this.verificationOrigin = verificationOrigin;
        }

        public bool IsBoundTo(VerifiedSimulationOrigin origin, Snapshot candidate)
            => origin != null && ReferenceEquals(verificationOrigin, origin) && IsBoundTo(candidate);

        public bool IsBoundTo(Snapshot candidate)
            => ReferenceEquals(snapshot, candidate) && Stamp != null && Stamp.IsCurrent && Projection != null
                && candidate.Revision == Stamp.Revision && candidate.SchemaVersion == Stamp.SchemaVersion
                && candidate.WireSchemaVersion == Stamp.WireSchemaVersion && candidate.RuleClock == Stamp.RuleClock
                && candidate.ContentFingerprint == Stamp.ContentFingerprint && candidate.TestOnly == Stamp.TestOnly;
    }

    public sealed partial class Simulation
    {
        private readonly ReadStateOwnerV1 readStateOwnerV1 = new ReadStateOwnerV1();
        private ReadStatePublicationV1 readStateV1;
        private bool preparingReadStateV1;

        private sealed class ReadStatePublicationV1
        {
            internal readonly ReadStateStampV1 Stamp;
            internal readonly IReadStateProjectionV1 Projection;
            internal ReadStatePublicationV1(ReadStateStampV1 stamp, IReadStateProjectionV1 projection)
            { Stamp = stamp; Projection = projection; }
        }

        private void RequireOwnerEntryV1(bool insideOwningRead = false)
        {
            if (preparingReadStateV1)
                throw new InvalidOperationException("A read projection provider cannot reenter its owning simulation.");
            if (!insideOwningRead) NativeReadInspectionV1.RequireExecution(NativeReadOperationV1.OwnerReentry);
        }

        private ReadStatePublicationV1 PrepareReadStateV1(Snapshot validatedCurrent)
        {
            var stamp = new ReadStateStampV1(readStateOwnerV1, policy, validatedCurrent);
            IReadStateProjectionV1 projection = null;
            preparingReadStateV1 = true;
            try {
                if (policy is IReadStateProjectionPolicyV1 provider) {
                    var proposed = provider.CreateReadProjection(stamp, validatedCurrent.Copy());
                    if (proposed != null && ReferenceEquals(proposed.Stamp, stamp)) projection = proposed;
                }
            }
            catch (Exception) {
                // Derived detail cannot reject an already validated command or authenticated restore.
                // The new generation stays unavailable; no previous projection or lazy repair is used.
                projection = null;
            }
            finally { preparingReadStateV1 = false; }
            return new ReadStatePublicationV1(stamp, projection);
        }

        private NativeReadContextV1 CurrentReadContextV1(Snapshot captured)
        {
            RequireOwnerEntryV1(insideOwningRead: true);
            var current = readStateV1;
            if (current == null || current.Projection == null
                || !current.Stamp.Matches(readStateOwnerV1, policy, state)
                || !current.Stamp.Matches(readStateOwnerV1, policy, captured)) return null;
            // The stamp/projection pair was accepted once inside guarded preparation. Never
            // execute a policy-defined property getter again merely to inspect that pair.
            return new NativeReadContextV1(current.Stamp, current.Projection, captured, verificationOrigin);
        }
    }
}
