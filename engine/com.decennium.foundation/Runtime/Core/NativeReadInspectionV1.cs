using System;
using System.Linq;

namespace Decennium.Foundation
{
    public enum NativeReadOperationV1
    {
        OwnerReentry, RandomDraw, SnapshotValidation, PolicyValidation, Resolver,
        HistoryReplay, ConditionLifecycle, DeadlineAdvancement, ResourceReservation
    }

    /// <summary>Synchronous per-call instrumentation. It cannot grant read authority and
    /// contains no gameplay failure or last-result state.</summary>
    public sealed class NativeReadInspectionV1 : IDisposable
    {
        internal const int OperationCount = 9;
        [ThreadStatic] private static NativeReadInspectionV1 current;
        private readonly NativeReadInspectionV1 previous;
        private readonly int[] attempts = new int[OperationCount];
        private bool disposed;
        private NativeReadInspectionV1() { previous = current; current = this; }
        internal static NativeReadInspectionV1 Enter() => new NativeReadInspectionV1();
        internal int[] Attempts() => (int[])attempts.Clone();
        internal bool HasViolation => attempts.Any(x => x != 0);
        public static void RequireExecution(NativeReadOperationV1 operation)
        {
            if (current == null) return;
            for (var scope = current; scope != null; scope = scope.previous) scope.attempts[(int)operation]++;
            throw new InvalidOperationException("An execution-only operation was attempted during a V1 read.");
        }
        public void Dispose()
        {
            if (disposed) return;
            if (!ReferenceEquals(current, this)) throw new InvalidOperationException("Read inspections must unwind in nesting order.");
            disposed = true; current = previous;
        }
    }
}
