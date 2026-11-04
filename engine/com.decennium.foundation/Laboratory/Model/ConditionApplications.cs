#if DECENNIUM_TEST_ONLY && (UNITY_EDITOR || DEVELOPMENT_BUILD || HEADLESS_TESTS)
using System;
using System.Collections.Generic;
using System.Linq;

namespace Decennium.Foundation.Laboratory
{
    // Generic non-track identities admitted by this lifecycle. Relationship conditions,
    // periodic damage, Staggered's episode rider and inactive Resonance Burn are separate.
    public enum ConditionKind
    {
        Blinded, Corrupted, Dazed, Deafened, Incapacitated, Invisible, Paralyzed,
        Petrified, Poisoned, Prone, Restrained, Silenced, Stunned, Unconscious
    }

    /// <summary>A legally selected source component, not permission to inflict it. The caller
    /// supplies its actual endpoint and cure eligibility after source exceptions and caps.</summary>
    public sealed class ConditionApplication
    {
        public string Id { get; }
        public string Owner { get; }
        public string Source { get; }
        public string Target { get; }
        public ConditionKind Kind { get; }
        public EffectClockMarker Starts { get; }
        public EffectClockMarker? Expires { get; }
        public string EndingMethod { get; }
        public bool GenericCureAllowed { get; }
        public bool InheritedIncapacitatedCureAllowed { get; }
        public int? ApplyingDc { get; }
        public long? Magnitude { get; }

        public ConditionApplication(string id, string owner, string source, string target, ConditionKind kind,
            EffectClockMarker starts, EffectClockMarker? expires, string endingMethod, bool genericCureAllowed,
            int? applyingDc = null, long? magnitude = null, bool? inheritedIncapacitatedCureAllowed = null)
        {
            foreach (string value in new[] { id, owner, source, target, endingMethod }) ConditionIdentity.Require(value);
            ConditionIdentity.Kind(kind);
            if (expires.HasValue && expires.Value.CompareTo(starts) <= 0 || applyingDc < 0 || magnitude < 0)
                throw new ArgumentException("Invalid condition endpoint or magnitude.");
            if (inheritedIncapacitatedCureAllowed.HasValue && !ConditionIdentity.InheritsIncapacitated(kind))
                throw new ArgumentException("This condition has no inherited Incapacitated component.");
            Id = id; Owner = owner; Source = source; Target = target; Kind = kind;
            Starts = starts; Expires = expires; EndingMethod = endingMethod; GenericCureAllowed = genericCureAllowed;
            ApplyingDc = applyingDc; Magnitude = magnitude;
            InheritedIncapacitatedCureAllowed = ConditionIdentity.InheritsIncapacitated(kind)
                && (inheritedIncapacitatedCureAllowed ?? genericCureAllowed);
        }
    }

    /// <summary>Named condition immunity only. Damage defenses and source-specific poison/disease
    /// interfaces must not be inserted as if they were named condition immunity.</summary>
    public sealed class ConditionImmunity
    {
        public string Id { get; }
        public string Owner { get; }
        public string Source { get; }
        public string Target { get; }
        public IReadOnlyList<ConditionKind> Kinds { get; }
        public EffectClockMarker Starts { get; }
        public EffectClockMarker? Expires { get; }
        public string EndingMethod { get; }

        public ConditionImmunity(string id, string owner, string source, string target,
            IEnumerable<ConditionKind> kinds, EffectClockMarker starts, EffectClockMarker? expires, string endingMethod)
        {
            foreach (string value in new[] { id, owner, source, target, endingMethod }) ConditionIdentity.Require(value);
            if (kinds == null) throw new ArgumentNullException(nameof(kinds));
            var copy = kinds.ToArray();
            if (copy.Length == 0 || copy.Length > 14 || copy.Distinct().Count() != copy.Length)
                throw new ArgumentException("Invalid named immunity set.");
            foreach (var kind in copy) ConditionIdentity.Kind(kind);
            if (expires.HasValue && expires.Value.CompareTo(starts) <= 0)
                throw new ArgumentException("Immunity expiry must follow application.");
            Id = id; Owner = owner; Source = source; Target = target;
            Kinds = Array.AsReadOnly(copy.OrderBy(x => x).ToArray());
            Starts = starts; Expires = expires; EndingMethod = endingMethod;
        }
    }

    public sealed class ConditionInstance
    {
        public ConditionApplication Application { get; }
        public string Id => Application.Id;
        public string ParentApplicationId { get; }
        public bool Suppressed { get; }
        public EffectClockMarker? EndedAt { get; }
        public string EndedReason { get; }
        public bool IncapacitatedPreventedAtAdmission { get; }
        public EffectClockMarker? IncapacitatedComponentEndedAt { get; }
        public bool IncapacitatedComponentEnded => IncapacitatedComponentEndedAt.HasValue;
        public bool ProneOnsetPrevented { get; }
        public bool DropHeldOnsetIssued => Application.Kind == ConditionKind.Unconscious;
        public bool ProneOnsetIssued => DropHeldOnsetIssued && !ProneOnsetPrevented
            || Application.Kind == ConditionKind.Prone && ParentApplicationId == "";

        internal ConditionInstance(ConditionApplication application, string parent = "", bool suppressed = false,
            EffectClockMarker? ended = null, string reason = null, EffectClockMarker? componentEnded = null,
            bool pronePrevented = false, bool incapacitatedPrevented = false)
        {
            Application = application; ParentApplicationId = parent; Suppressed = suppressed;
            EndedAt = ended; EndedReason = reason; IncapacitatedComponentEndedAt = componentEnded;
            ProneOnsetPrevented = pronePrevented; IncapacitatedPreventedAtAdmission = incapacitatedPrevented;
        }
        public bool Present(EffectClockMarker at) => Application.Starts.CompareTo(at) <= 0
            && (!EndedAt.HasValue || at.CompareTo(EndedAt.Value) < 0)
            && (!Application.Expires.HasValue || at.CompareTo(Application.Expires.Value) < 0);
        internal ConditionInstance WithSuppression(bool value) => new ConditionInstance(Application, ParentApplicationId,
            value, EndedAt, EndedReason, IncapacitatedComponentEndedAt, ProneOnsetPrevented, IncapacitatedPreventedAtAdmission);
        internal ConditionInstance End(EffectClockMarker at, string reason) => new ConditionInstance(Application, ParentApplicationId,
            Suppressed, at, reason, IncapacitatedComponentEndedAt, ProneOnsetPrevented, IncapacitatedPreventedAtAdmission);
        internal ConditionInstance EndIncapacitated(EffectClockMarker at) => new ConditionInstance(Application, ParentApplicationId,
            Suppressed, EndedAt, EndedReason, at, ProneOnsetPrevented, IncapacitatedPreventedAtAdmission);
    }

    public sealed class ConditionImmunityInstance
    {
        public ConditionImmunity Grant { get; }
        public EffectClockMarker? EndedAt { get; }
        public string EndedReason { get; }
        internal ConditionImmunityInstance(ConditionImmunity grant, EffectClockMarker? ended = null, string reason = null)
        { Grant = grant; EndedAt = ended; EndedReason = reason; }
        public bool Present(EffectClockMarker at) => Grant.Starts.CompareTo(at) <= 0
            && (!EndedAt.HasValue || at.CompareTo(EndedAt.Value) < 0)
            && (!Grant.Expires.HasValue || at.CompareTo(Grant.Expires.Value) < 0);
        internal ConditionImmunityInstance End(EffectClockMarker at, string reason) => new ConditionImmunityInstance(Grant, at, reason);
    }

    internal static class ConditionIdentity
    {
        internal static void Require(string id)
        { if (!Validation.ValidId(id)) throw new ArgumentException("A stable condition identity is required."); }
        internal static void Kind(ConditionKind kind)
        { if (!Enum.IsDefined(typeof(ConditionKind), kind)) throw new ArgumentException("Unsupported condition identity."); }
        internal static bool InheritsIncapacitated(ConditionKind kind) => kind == ConditionKind.Paralyzed
            || kind == ConditionKind.Petrified || kind == ConditionKind.Stunned || kind == ConditionKind.Unconscious;
    }
}
#endif
