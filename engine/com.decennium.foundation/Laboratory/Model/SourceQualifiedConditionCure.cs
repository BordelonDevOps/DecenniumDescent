#if DECENNIUM_TEST_ONLY && (UNITY_EDITOR || DEVELOPMENT_BUILD || HEADLESS_TESTS)
using System;
using System.Collections.Generic;
using System.Collections.ObjectModel;
using System.Linq;

namespace Decennium.Foundation.Laboratory
{
    /// <summary>Trusted producer boundary, never a command payload. A future gameplay
    /// producer must add a factory that validates its real trigger, ownership, recipient,
    /// choice and payment before issuing a context. No gameplay factory is admitted here.</summary>
    internal sealed class ConditionCureInvocation
    {
        internal const string DetachedAuthority = "TEST_ONLY.detached-condition-cure.v1";
        internal string Id { get; }
        internal string SourceId { get; }
        internal string SourceRevision { get; }
        internal string ApplyingActor { get; }
        internal string Target { get; }
        internal ConditionStamp At { get; }
        internal ReadOnlyCollection<ConditionKind> AllowedKinds { get; }
        internal bool TestOnly { get; }

        private ConditionCureInvocation(string id, string source, string sourceRevision, string actor,
            string target, ConditionStamp at, IEnumerable<ConditionKind> allowedKinds, bool testOnly)
        {
            foreach (string value in new[] { id, source, sourceRevision, actor, target }) ConditionIdentity.Require(value);
            var kinds = allowedKinds?.ToArray();
            if (kinds == null || kinds.Length == 0 || kinds.Length > 15 || kinds.Distinct().Count() != kinds.Length)
                throw new ArgumentException("A qualified source must name its permitted cure choices.");
            foreach (var kind in kinds) ConditionIdentity.Kind(kind);
            Id = id; SourceId = source; SourceRevision = sourceRevision; ApplyingActor = actor;
            Target = target; At = at; AllowedKinds = Array.AsReadOnly(kinds); TestOnly = testOnly;
        }

        // Explicit detached component authority. These facts cannot qualify a connected
        // source, and the current gameplay profile rejects any Frightened cure operation.
        internal static ConditionCureInvocation ForDetachedTest(string authority, string id, string source,
            string sourceRevision, string actor, string target, ConditionStamp at, ConditionKind[] allowedKinds)
        {
            if (authority != DetachedAuthority || id == null || !id.StartsWith("TEST_ONLY.", StringComparison.Ordinal)
                || source == null || !source.StartsWith("TEST_ONLY.", StringComparison.Ordinal)
                || sourceRevision == null || !sourceRevision.StartsWith("TEST_ONLY.", StringComparison.Ordinal))
                throw new ArgumentException("Detached cure invocation requires explicit TEST_ONLY authority and provenance.");
            return new ConditionCureInvocation(id, source, sourceRevision, actor, target, at, allowedKinds, true);
        }
    }

    /// <summary>One source-qualified component settlement. Its returned journal is still
    /// staged: the future producer must commit it with its own receipt and other effects.</summary>
    internal sealed class ConditionCureSettlement
    {
        internal ConditionCureInvocation Invocation { get; }
        internal ConditionKind Kind { get; }
        internal ConditionHistoryTransition Transition { get; }
        internal ReadOnlyCollection<string> EndedApplications { get; }
        internal ConditionCureSettlement(ConditionCureInvocation invocation, ConditionKind kind,
            ConditionHistoryTransition transition, IEnumerable<string> ended)
        { Invocation = invocation; Kind = kind; Transition = transition; EndedApplications = Array.AsReadOnly(ended.ToArray()); }
    }

    internal static class SourceQualifiedConditionCure
    {
        internal static ConditionCureSettlement Settle(ConditionHistory history, ConditionCureInvocation invocation,
            string target, ConditionKind kind)
        {
            if (history == null || invocation == null) throw new ArgumentNullException("A qualified invocation and target history are required.");
            ConditionIdentity.Kind(kind);
            if (target != history.Journal.Target || target != invocation.Target || !history.Journal.Now.Equals(invocation.At)
                || !invocation.AllowedKinds.Contains(kind))
                throw new ArgumentException("Cure target, time or choice does not match the qualified invocation.");
            string operation = invocation.Id + ".cure";
            var transition = history.Append(ConditionOperation.Cure(operation, invocation.At, kind.ToString()));
            var before = history.Ledger.Applications.ToDictionary(x => x.Id, StringComparer.Ordinal);
            var ended = transition.State.Ledger.Applications.Where(x => x.EndedAt.HasValue && !before[x.Id].EndedAt.HasValue)
                .Select(x => x.Id).OrderBy(x => x, StringComparer.Ordinal);
            return new ConditionCureSettlement(invocation, kind, transition, ended);
        }
    }
}
#endif
