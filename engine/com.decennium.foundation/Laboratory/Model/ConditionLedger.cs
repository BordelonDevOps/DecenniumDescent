#if DECENNIUM_TEST_ONLY && (UNITY_EDITOR || DEVELOPMENT_BUILD || HEADLESS_TESTS)
using System;
using System.Collections.Generic;
using System.Linq;

namespace Decennium.Foundation.Laboratory
{
    public enum ConditionConsequenceKind { DropHeldItems, FallProne, EndConcentration }
    public sealed class ConditionConsequence
    {
        public ConditionConsequenceKind Kind { get; }
        public string Target { get; }
        public string Cause { get; }
        public EffectClockMarker At { get; }
        internal ConditionConsequence(ConditionConsequenceKind kind, string target, string cause, EffectClockMarker at)
        { Kind = kind; Target = target; Cause = cause; At = at; }
    }

    public sealed class ResolvedConditionComponent
    {
        public string ApplicationId { get; }
        public ConditionKind Kind { get; }
        public bool Inherited { get; }
        internal ResolvedConditionComponent(string applicationId, ConditionKind kind, bool inherited)
        { ApplicationId = applicationId; Kind = kind; Inherited = inherited; }
    }

    public sealed class ConditionView
    {
        public IReadOnlyList<ResolvedConditionComponent> Components { get; }
        public ConditionClauses Clauses { get; }
        internal ConditionView(IEnumerable<ResolvedConditionComponent> components)
        {
            Components = Array.AsReadOnly(components.ToArray());
            var clauses = new List<ConditionClause>();
            foreach (var kind in Components.Select(x => x.Kind).Distinct())
                if (Enum.TryParse(kind.ToString(), out ConditionClause clause)) clauses.Add(clause);
            Clauses = ConditionClauses.FromResolved(clauses);
        }
        public bool Has(ConditionKind kind) { ConditionIdentity.Kind(kind); return Components.Any(x => x.Kind == kind); }
        public IReadOnlyList<string> Sources(ConditionKind kind)
        { ConditionIdentity.Kind(kind); return Array.AsReadOnly(Components.Where(x => x.Kind == kind).Select(x => x.ApplicationId).ToArray()); }
        public bool BlocksSight => Has(ConditionKind.Blinded);
        public bool BlocksHearing => Has(ConditionKind.Deafened);
        public bool Unaware => Has(ConditionKind.Petrified) || Has(ConditionKind.Unconscious);
        public bool BlocksSpeech => Has(ConditionKind.Paralyzed) || Has(ConditionKind.Petrified) || Has(ConditionKind.Unconscious);
        public bool SpeechOnlyFaltering => Has(ConditionKind.Stunned);
        public bool BlocksAudibleFeatures => BlocksSpeech || Has(ConditionKind.Silenced);
        public bool AutomaticStrengthDexterityFailure => Has(ConditionKind.Paralyzed) || Has(ConditionKind.Petrified)
            || Has(ConditionKind.Stunned) || Has(ConditionKind.Unconscious);
        public long HealingPotential(long amount, HpRestorationKind kind = HpRestorationKind.HealingEffect)
            => PlaytestConditions.HpRestorationAmount(amount, Has(ConditionKind.Corrupted), kind);
        // These are condition/life constraints, not grants of actions, valid targets or perception.
        // External named immunity cannot override this host's zero-HP/death rules.
        public ConditionPermissions PermissionsForLife(LifeState life, long actionsTaken = 0, long speedSpent = 0)
        {
            if (life == null) throw new ArgumentNullException(nameof(life));
            var result = PlaytestConditions.Permissions(Clauses, actionsTaken, speedSpent);
            return life.Dead || life.Hp == 0 ? new ConditionPermissions(false, false, false, false, false, false, false) : result;
        }
    }

    /// <summary>Pure result. A host must commit State and its consequences together exactly once;
    /// calling this helper does not authorize a command, alter inventory or own concentration.</summary>
    public sealed class ConditionTransition
    {
        public ConditionLedger State { get; }
        public bool ApplicationPrevented { get; }
        public IReadOnlyList<ConditionConsequence> Consequences { get; }
        internal ConditionTransition(ConditionLedger state, IEnumerable<ConditionConsequence> consequences, bool prevented = false)
        { State = state; ApplicationPrevented = prevented; Consequences = Array.AsReadOnly(consequences.ToArray()); }
    }

    /// <summary>One target's immutable, bounded generic condition lifecycle. Source eligibility,
    /// targeting, costs, DC construction and actual cure/ending events are adjudicated by the caller.
    /// No refresh, periodic damage, source relationship or track behavior is inferred from a name.</summary>
    public sealed class ConditionLedger
    {
        public const int MaxApplications = 128, MaxImmunities = 64;
        public string Target { get; }
        public EffectClockMarker Now { get; }
        public IReadOnlyList<ConditionInstance> Applications { get; }
        public IReadOnlyList<ConditionImmunityInstance> Immunities { get; }
        public ConditionLedger(string target, EffectClockMarker now = default)
            : this(target, now, Array.Empty<ConditionInstance>(), Array.Empty<ConditionImmunityInstance>()) { }
        private ConditionLedger(string target, EffectClockMarker now, IEnumerable<ConditionInstance> applications,
            IEnumerable<ConditionImmunityInstance> immunities)
        {
            ConditionIdentity.Require(target); Target = target; Now = now;
            Applications = Array.AsReadOnly(applications.ToArray()); Immunities = Array.AsReadOnly(immunities.ToArray());
        }
        private ConditionLedger Copy(IEnumerable<ConditionInstance> applications = null,
            IEnumerable<ConditionImmunityInstance> immunities = null, EffectClockMarker? now = null)
            => new ConditionLedger(Target, now ?? Now, applications ?? Applications, immunities ?? Immunities);
        private void NewId(string id)
        {
            ConditionIdentity.Require(id);
            if (Applications.Any(x => x.Id == id) || Immunities.Any(x => x.Grant.Id == id))
                throw new ArgumentException("Application identity already exists, including ended history.");
        }
        private bool NamedImmunity(ConditionKind kind) => Immunities.Any(x => x.Present(Now) && x.Grant.Kinds.Contains(kind));
        private bool OperativeRoot(ConditionInstance instance) => instance.Present(Now) && !instance.Suppressed
            && !NamedImmunity(instance.Application.Kind);
        public bool ImmuneTo(ConditionKind kind)
        {
            ConditionIdentity.Kind(kind);
            return ImmunitySources(kind).Count != 0;
        }
        public IReadOnlyList<string> ImmunitySources(ConditionKind kind)
        {
            ConditionIdentity.Kind(kind);
            var ids = Immunities.Where(x => x.Present(Now) && x.Grant.Kinds.Contains(kind)).Select(x => x.Grant.Id);
            if (kind == ConditionKind.Poisoned)
                ids = ids.Concat(Applications.Where(x => x.Application.Kind == ConditionKind.Petrified && OperativeRoot(x)).Select(x => x.Id));
            return Array.AsReadOnly(ids.ToArray());
        }
        public ConditionView View()
        {
            var components = new List<ResolvedConditionComponent>();
            foreach (var instance in Applications) {
                var kind = instance.Application.Kind;
                if (!instance.Present(Now) || instance.Suppressed || ImmuneTo(kind)) continue;
                components.Add(new ResolvedConditionComponent(instance.Id, kind, false));
                if (ConditionIdentity.InheritsIncapacitated(kind) && !instance.IncapacitatedComponentEnded && !instance.IncapacitatedPreventedAtAdmission
                    && !ImmuneTo(ConditionKind.Incapacitated))
                    components.Add(new ResolvedConditionComponent(instance.Id, ConditionKind.Incapacitated, true));
            }
            return new ConditionView(components);
        }
        private ConditionTransition Transition(ConditionLedger next, string cause,
            IEnumerable<ConditionConsequence> onset = null)
        {
            var events = onset?.ToList() ?? new List<ConditionConsequence>();
            if (!View().Has(ConditionKind.Incapacitated) && next.View().Has(ConditionKind.Incapacitated))
                events.Add(new ConditionConsequence(ConditionConsequenceKind.EndConcentration, Target, cause, next.Now));
            return new ConditionTransition(next, events);
        }
        public ConditionTransition Apply(ConditionApplication application, string proneConsequenceId = "")
        {
            if (application == null) throw new ArgumentNullException(nameof(application));
            if (application.Target != Target || !application.Starts.Equals(Now))
                throw new ArgumentException("Apply only to this target at the current marker.");
            NewId(application.Id);
            bool unconscious = application.Kind == ConditionKind.Unconscious;
            if (unconscious) {
                NewId(proneConsequenceId);
                if (proneConsequenceId == application.Id) throw new ArgumentException("Onset needs a separate identity.");
            } else if (proneConsequenceId != "") throw new ArgumentException("Only Unconscious has this onset record.");
            if (ImmuneTo(application.Kind)) return new ConditionTransition(this, Array.Empty<ConditionConsequence>(), true);
            bool pronePrevented = unconscious && ImmuneTo(ConditionKind.Prone);
            int count = unconscious && !pronePrevented ? 2 : 1;
            if (Applications.Count + count > MaxApplications) throw new InvalidOperationException("Condition history capacity reached.");
            var records = Applications.ToList();
            bool incapacitatedPrevented = ConditionIdentity.InheritsIncapacitated(application.Kind) && ImmuneTo(ConditionKind.Incapacitated);
            records.Add(new ConditionInstance(application, pronePrevented: pronePrevented, incapacitatedPrevented: incapacitatedPrevented));
            var onset = new List<ConditionConsequence>();
            if (application.Kind == ConditionKind.Prone)
                onset.Add(new ConditionConsequence(ConditionConsequenceKind.FallProne, Target, application.Id, Now));
            if (unconscious) {
                onset.Add(new ConditionConsequence(ConditionConsequenceKind.DropHeldItems, Target, application.Id, Now));
                if (!pronePrevented) {
                    var prone = new ConditionApplication(proneConsequenceId, application.Owner, application.Source, Target,
                        ConditionKind.Prone, Now, null, "stand-or-explicit-cure", true);
                    records.Add(new ConditionInstance(prone, application.Id));
                    onset.Add(new ConditionConsequence(ConditionConsequenceKind.FallProne, Target, application.Id, Now));
                }
            }
            return Transition(Copy(applications: records), application.Id, onset);
        }
        public ConditionTransition GrantImmunity(ConditionImmunity immunity)
        {
            if (immunity == null) throw new ArgumentNullException(nameof(immunity));
            if (immunity.Target != Target || !immunity.Starts.Equals(Now))
                throw new ArgumentException("Grant immunity only to this target at the current marker.");
            NewId(immunity.Id);
            if (Immunities.Count == MaxImmunities) throw new InvalidOperationException("Immunity history capacity reached.");
            return Transition(Copy(immunities: Immunities.Concat(new[] { new ConditionImmunityInstance(immunity) })), immunity.Id);
        }
        private ConditionInstance PresentInstance(string id)
        {
            ConditionIdentity.Require(id);
            return Applications.SingleOrDefault(x => x.Id == id && x.Present(Now))
                ?? throw new ArgumentException("A present, unexpired condition application is required.");
        }
        public ConditionTransition SuppressApplication(string id, bool suppressed)
        {
            var instance = PresentInstance(id);
            return Transition(Copy(applications: Applications.Select(x => x == instance ? x.WithSuppression(suppressed) : x)), id);
        }
        public ConditionTransition EndApplication(string id, string reason)
        {
            ConditionIdentity.Require(reason); var instance = PresentInstance(id);
            return Transition(Copy(applications: Applications.Select(x => x == instance ? x.End(Now, reason) : x)), id);
        }
        public ConditionTransition EndImmunity(string id, string reason)
        {
            ConditionIdentity.Require(id); ConditionIdentity.Require(reason);
            var instance = Immunities.SingleOrDefault(x => x.Grant.Id == id && x.Present(Now))
                ?? throw new ArgumentException("A present immunity grant is required.");
            return Transition(Copy(immunities: Immunities.Select(x => x == instance ? x.End(Now, reason) : x)), id);
        }
        public ConditionTransition Cure(ConditionKind kind)
        {
            ConditionIdentity.Kind(kind);
            var next = Applications.Select(instance => {
                if (!instance.Present(Now)) return instance;
                if (instance.Application.Kind == kind && instance.Application.GenericCureAllowed) return instance.End(Now, "generic-condition-cure");
                if (kind == ConditionKind.Incapacitated && instance.Application.InheritedIncapacitatedCureAllowed
                    && !instance.IncapacitatedComponentEnded && !instance.IncapacitatedPreventedAtAdmission)
                    return instance.EndIncapacitated(Now);
                return instance;
            });
            return Transition(Copy(applications: next), "generic-condition-cure");
        }
        public ConditionTransition AdvanceTo(EffectClockMarker destination)
        {
            if (destination.CompareTo(Now) < 0) throw new ArgumentException("The condition clock cannot move backward.");
            var deadlines = Applications.Where(x => !x.EndedAt.HasValue).Select(x => x.Application.Expires)
                .Concat(Immunities.Where(x => !x.EndedAt.HasValue).Select(x => x.Grant.Expires))
                .Where(x => x.HasValue && x.Value.CompareTo(Now) > 0 && x.Value.CompareTo(destination) <= 0)
                .Select(x => x.Value).Distinct().OrderBy(x => x).ToArray();
            var state = this; var events = new List<ConditionConsequence>();
            foreach (var marker in deadlines) {
                var next = state.Copy(now: marker,
                    applications: state.Applications.Select(x => !x.EndedAt.HasValue && x.Application.Expires.HasValue
                        && x.Application.Expires.Value.Equals(marker) ? x.End(marker, "expired") : x),
                    immunities: state.Immunities.Select(x => !x.EndedAt.HasValue && x.Grant.Expires.HasValue
                        && x.Grant.Expires.Value.Equals(marker) ? x.End(marker, "expired") : x));
                var change = state.Transition(next, "expiry"); events.AddRange(change.Consequences); state = change.State;
            }
            return new ConditionTransition(state.Copy(now: destination), events);
        }
    }
}
#endif
