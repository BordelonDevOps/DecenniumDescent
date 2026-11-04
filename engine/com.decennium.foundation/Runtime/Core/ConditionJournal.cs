using System;
using System.Collections.Generic;
using System.Linq;

namespace Decennium.Foundation
{
    /// <summary>Serializable time and phase, without selecting a gameplay ordering policy.</summary>
    public readonly struct ConditionStamp : IComparable<ConditionStamp>, IEquatable<ConditionStamp>
    {
        public RuleTime Time { get; }
        public int Phase { get; }
        public ConditionStamp(RuleTime time, int phase = 0)
        { if (phase < 0) throw new ArgumentOutOfRangeException(nameof(phase)); Time = time; Phase = phase; }
        public int CompareTo(ConditionStamp other)
        { int value = Time.CompareTo(other.Time); return value == 0 ? Phase.CompareTo(other.Phase) : value; }
        public bool Equals(ConditionStamp other) => Time == other.Time && Phase == other.Phase;
        public override bool Equals(object obj) => obj is ConditionStamp other && Equals(other);
        public override int GetHashCode() => unchecked(Time.GetHashCode() * 397 ^ Phase);
    }

    /// <summary>Structural source data. The selected rules interpreter validates condition names,
    /// admission, component semantics and source eligibility; this record grants no authority.</summary>
    public sealed class ConditionApplicationData
    {
        public string Id { get; }
        public string Owner { get; }
        public string Source { get; }
        public string Kind { get; }
        public ConditionStamp? Expires { get; }
        public string EndingMethod { get; }
        public bool GenericCureAllowed { get; }
        public bool? InheritedCureAllowed { get; }
        public int? ApplyingDc { get; }
        public long? Magnitude { get; }
        public ConditionApplicationData(string id, string owner, string source, string kind,
            ConditionStamp? expires, string endingMethod, bool genericCureAllowed,
            int? applyingDc = null, long? magnitude = null, bool? inheritedCureAllowed = null)
        {
            foreach (string value in new[] { id, owner, source, kind, endingMethod }) ConditionJournal.RequireId(value);
            if (applyingDc < 0 || magnitude < 0) throw new ArgumentException("Negative condition source value.");
            Id = id; Owner = owner; Source = source; Kind = kind; Expires = expires; EndingMethod = endingMethod;
            GenericCureAllowed = genericCureAllowed; ApplyingDc = applyingDc; Magnitude = magnitude; InheritedCureAllowed = inheritedCureAllowed;
        }
    }

    public sealed class ConditionImmunityData
    {
        public string Id { get; }
        public string Owner { get; }
        public string Source { get; }
        public IReadOnlyList<string> Kinds { get; }
        public ConditionStamp? Expires { get; }
        public string EndingMethod { get; }
        public ConditionImmunityData(string id, string owner, string source, IEnumerable<string> kinds,
            ConditionStamp? expires, string endingMethod)
        {
            foreach (string value in new[] { id, owner, source, endingMethod }) ConditionJournal.RequireId(value);
            if (kinds == null) throw new ArgumentNullException(nameof(kinds));
            var copy = kinds.Take(15).ToArray();
            if (copy.Length == 0 || copy.Length > 14 || copy.Distinct(StringComparer.Ordinal).Count() != copy.Length)
                throw new ArgumentException("Invalid named condition immunity set.");
            foreach (string kind in copy) ConditionJournal.RequireId(kind);
            Id = id; Owner = owner; Source = source; Kinds = Array.AsReadOnly(copy.OrderBy(x => x, StringComparer.Ordinal).ToArray());
            Expires = expires; EndingMethod = endingMethod;
        }
    }

    public enum ConditionOperationKind { Apply, GrantImmunity, Suppress, EndApplication, EndImmunity, Cure, Advance }

    /// <summary>An ordered component operation, not an authorized gameplay command or its receipt.</summary>
    public sealed class ConditionOperation
    {
        public string Id { get; }
        public ConditionStamp At { get; }
        public ConditionOperationKind Kind { get; }
        public ConditionApplicationData Application { get; }
        public ConditionImmunityData Immunity { get; }
        public string Subject { get; }
        public string Reason { get; }
        public bool Suppressed { get; }
        private ConditionOperation(string id, ConditionStamp at, ConditionOperationKind kind,
            ConditionApplicationData application = null, ConditionImmunityData immunity = null,
            string subject = "", string reason = "", bool suppressed = false)
        {
            ConditionJournal.RequireId(id);
            Id = id; At = at; Kind = kind; Application = application; Immunity = immunity;
            Subject = subject; Reason = reason; Suppressed = suppressed;
        }
        public static ConditionOperation Apply(string id, ConditionStamp at, ConditionApplicationData application, string proneId = "")
        {
            if (application == null) throw new ArgumentNullException(nameof(application));
            if (proneId != "") ConditionJournal.RequireId(proneId);
            Endpoint(at, application.Expires);
            return new ConditionOperation(id, at, ConditionOperationKind.Apply, application: application, subject: proneId);
        }
        public static ConditionOperation Grant(string id, ConditionStamp at, ConditionImmunityData immunity)
        {
            if (immunity == null) throw new ArgumentNullException(nameof(immunity));
            Endpoint(at, immunity.Expires);
            return new ConditionOperation(id, at, ConditionOperationKind.GrantImmunity, immunity: immunity);
        }
        public static ConditionOperation Suppress(string id, ConditionStamp at, string applicationId, bool suppressed)
        {
            ConditionJournal.RequireId(applicationId);
            return new ConditionOperation(id, at, ConditionOperationKind.Suppress, subject: applicationId, suppressed: suppressed);
        }
        public static ConditionOperation End(string id, ConditionStamp at, string applicationId, string reason)
        {
            ConditionJournal.RequireId(applicationId); ConditionJournal.RequireId(reason);
            return new ConditionOperation(id, at, ConditionOperationKind.EndApplication, subject: applicationId, reason: reason);
        }
        public static ConditionOperation EndGrant(string id, ConditionStamp at, string immunityId, string reason)
        {
            ConditionJournal.RequireId(immunityId); ConditionJournal.RequireId(reason);
            return new ConditionOperation(id, at, ConditionOperationKind.EndImmunity, subject: immunityId, reason: reason);
        }
        public static ConditionOperation Cure(string id, ConditionStamp at, string conditionKind)
        {
            ConditionJournal.RequireId(conditionKind);
            return new ConditionOperation(id, at, ConditionOperationKind.Cure, subject: conditionKind);
        }
        public static ConditionOperation Advance(string id, ConditionStamp destination)
            => new ConditionOperation(id, destination, ConditionOperationKind.Advance);
        private static void Endpoint(ConditionStamp starts, ConditionStamp? expires)
        { if (expires.HasValue && expires.Value.CompareTo(starts) <= 0) throw new ArgumentException("Endpoint must follow application."); }
    }

    /// <summary>Bounded component history. A full host must bind this to its command receipts,
    /// actual sources and world consequences. Neither this record nor its checksum authenticates them.</summary>
    public sealed class ConditionJournal
    {
        public const int MaxOperations = 512;
        public string PolicyId { get; }
        public string Target { get; }
        public ConditionStamp Origin { get; }
        public ConditionStamp Now => Operations.Count == 0 ? Origin : Operations[Operations.Count - 1].At;
        public IReadOnlyList<ConditionOperation> Operations { get; }
        public ConditionJournal(string policyId, string target, ConditionStamp origin = default,
            IEnumerable<ConditionOperation> operations = null)
        {
            RequireId(policyId); RequireId(target);
            var copy = (operations ?? Array.Empty<ConditionOperation>()).Take(MaxOperations + 1).ToArray();
            if (copy.Length > MaxOperations) throw new ArgumentException("Condition operation capacity reached.");
            var seen = new HashSet<string>(StringComparer.Ordinal); var now = origin;
            foreach (var operation in copy) {
                if (operation == null || !seen.Add(operation.Id)) throw new ArgumentException("Invalid or duplicate condition operation.");
                if (operation.At.CompareTo(now) < 0 || operation.Kind != ConditionOperationKind.Advance && !operation.At.Equals(now))
                    throw new ArgumentException("Only explicit Advance may change the condition clock.");
                now = operation.At;
            }
            PolicyId = policyId; Target = target; Origin = origin; Operations = Array.AsReadOnly(copy);
        }
        public ConditionJournal Append(ConditionOperation operation)
        {
            if (Operations.Count == MaxOperations) throw new InvalidOperationException("Condition operation capacity reached.");
            return new ConditionJournal(PolicyId, Target, Origin, Operations.Concat(new[] { operation }));
        }
        internal static void RequireId(string value)
        { if (!Validation.ValidId(value)) throw new ArgumentException("Invalid condition journal identity."); }
    }
}
