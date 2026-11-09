#if DECENNIUM_TEST_ONLY && (UNITY_EDITOR || DEVELOPMENT_BUILD || HEADLESS_TESTS)
using System;
using System.Globalization;
using System.Linq;
using System.Security.Cryptography;
using System.Text;

namespace Decennium.Foundation.Laboratory
{
    /// <summary>Authored TEST_ONLY recreation location. Its safety/eligibility flags are independent
    /// of the Long Rest SafeBerth and QualifyingRestEligible facts.</summary>
    public sealed class TestOnlyMoraleRestSiteFact
    {
        public string Id { get; }
        public string ActivityId { get; }
        public int X { get; }
        public int Y { get; }
        public bool SafeRecreation { get; }
        public bool MoraleRestEligible { get; }

        public TestOnlyMoraleRestSiteFact(string id, string activityId, int x, int y,
            bool safeRecreation, bool moraleRestEligible)
        {
            if (!Validation.ValidId(id) || !Validation.ValidId(activityId) || x < 0 || y < 0)
                throw new ArgumentException("Invalid TEST_ONLY Morale Rest site fact.");
            Id = id; ActivityId = activityId; X = x; Y = y;
            SafeRecreation = safeRecreation; MoraleRestEligible = moraleRestEligible;
        }

        internal string Canonical => Id + "|activity=" + ActivityId + "|" + X.ToString(CultureInfo.InvariantCulture)
            + "|" + Y.ToString(CultureInfo.InvariantCulture) + "|safe=" + (SafeRecreation ? "1" : "0")
            + "|eligible=" + (MoraleRestEligible ? "1" : "0");
    }

    /// <summary>Finite TEST_ONLY admission, activity, and site facts for the source-marked NEW Morale
    /// Rest endpoint. The profile does not grant recovery or production authority.</summary>
    public sealed class TestOnlyMoraleRestProfile
    {
        public const string SourceId = "campaign.morale-rest";
        public const string TrackId = "expedition.strain";
        public const string SourceRevision = "46a4d52728ee6956f0bebcb5d2103ffd5bc67ba4";
        public const string StrainBlob = "7005aaf9558f0ce4f445ffe982dfa9b6f36c8ee4";
        public const string ExpeditionBookBlob = "466871fc128dc5f06043a874da2b9c1d94ed80a5";
        private readonly string[] eligibleActors;
        private readonly TestOnlyMoraleRestSiteFact[] sites;

        public System.Collections.Generic.IReadOnlyList<string> EligibleActors => Array.AsReadOnly(eligibleActors);
        public System.Collections.Generic.IReadOnlyList<TestOnlyMoraleRestSiteFact> Sites => Array.AsReadOnly(sites);

        public TestOnlyMoraleRestProfile(
            System.Collections.Generic.IEnumerable<string> eligibleActors = null,
            System.Collections.Generic.IEnumerable<TestOnlyMoraleRestSiteFact> sites = null)
        {
            this.eligibleActors = (eligibleActors ?? new[] { TestOnlyPolicy.ActorId })
                .OrderBy(x => x, StringComparer.Ordinal).ToArray();
            this.sites = (sites ?? new[] { new TestOnlyMoraleRestSiteFact(
                "TEST_ONLY.safe-recreation", "TEST_ONLY.campfire-recreation", 0, 0, true, true) })
                .OrderBy(x => x?.Id, StringComparer.Ordinal).ToArray();
            if (this.eligibleActors.Length == 0 || this.eligibleActors.Any(x => !Validation.ValidId(x))
                || this.eligibleActors.Distinct(StringComparer.Ordinal).Count() != this.eligibleActors.Length
                || this.sites.Length == 0 || this.sites.Any(x => x == null)
                || this.sites.Select(x => x.Id).Distinct(StringComparer.Ordinal).Count() != this.sites.Length
                || !this.sites.Any(x => x.SafeRecreation && x.MoraleRestEligible)
                || this.sites.Where(x => x.SafeRecreation && x.MoraleRestEligible)
                    .Select(x => x.X + "," + x.Y).Distinct(StringComparer.Ordinal).Count()
                    != this.sites.Count(x => x.SafeRecreation && x.MoraleRestEligible))
                throw new ArgumentException("Invalid finite TEST_ONLY Morale Rest profile.");
        }

        internal string CanonicalKey => "morale-rest-v1|source=" + SourceId + "|track=" + TrackId
            + "|book=" + ExpeditionBookBlob + "|strain=" + StrainBlob + "|revision=" + SourceRevision
            + "|continuous-seconds=14400|max-beneficial-per-24h=1|no-work-travel-sleep-short-rest=1"
            + "|no-long-rest-overlap=1|eligible=" + string.Join(";", eligibleActors)
            + "|sites=" + string.Join(";", sites.Select(x => x.Canonical));

        internal bool IncludesActor(string actor) => eligibleActors.Contains(actor, StringComparer.Ordinal);
        internal TestOnlyMoraleRestSiteFact Site(string id) => sites.SingleOrDefault(x => x.Id == id);

        internal string ValidateBindings(Snapshot s, TestOnlyRestDebtProfile restDebt)
            => restDebt != null && eligibleActors.All(actor => restDebt.IncludesActor(actor)
                && s.Actors.Any(x => x.Id == actor) && s.Lives.Any(x => x.ActorId == actor))
                ? null : "MoraleRestProfileActorMissing";

        internal static string BindFingerprint(string prior, TestOnlyMoraleRestProfile profile)
        {
            using (var sha = SHA256.Create())
                return "TEST_ONLY.morale-rest-v1-" + string.Concat(sha.ComputeHash(
                    Encoding.UTF8.GetBytes(prior + "|" + profile.CanonicalKey))
                    .Select(b => b.ToString("x2", CultureInfo.InvariantCulture)));
        }
    }

    public sealed partial class TestOnlySharedWorldPolicy
    {
        private const long MoraleRestSeconds = 4 * 60 * 60;
        private TestOnlyMoraleRestProfile moraleRestProfile;

        /// <summary>Selects the additive schema65 TEST_ONLY Morale Rest endpoint after the shared
        /// daily provisioning, Rest Debt, and schema64 Strain recovery profiles.</summary>
        public TestOnlySharedWorldPolicy EnableMoraleRest(TestOnlyMoraleRestProfile profile = null)
        {
            if (initializationStarted) throw new InvalidOperationException("Morale Rest profile must be selected before Initial().");
            if (strainRecoveryProfile == null || restDebtProfile == null || dailyProvisioning == null)
                throw new InvalidOperationException("Morale Rest requires daily provisioning, Rest Debt, and Expedition Strain recovery.");
            if (legacyStrainRecoverySemantics)
                throw new InvalidOperationException("Morale Rest requires typed schema65 Strain recovery semantics.");
            if (moraleRestProfile != null) throw new InvalidOperationException("Morale Rest profile is already selected.");
            moraleRestProfile = profile ?? new TestOnlyMoraleRestProfile();
            string error = moraleRestProfile.ValidateBindings(bodies.Initial(), restDebtProfile);
            if (error != null) throw new ArgumentException(error, nameof(profile));
            ContentFingerprint = TestOnlyMoraleRestProfile.BindFingerprint(ContentFingerprint, moraleRestProfile);
            return this;
        }

        private void InitializeMoraleRest(Snapshot s)
        {
            if (moraleRestProfile == null) return;
            if (s.SchemaVersion != Snapshot.MoraleRestSchema)
                throw new InvalidOperationException("MoraleRestRequiresSchema65");
            string error = moraleRestProfile.ValidateBindings(s, restDebtProfile);
            if (error != null) throw new InvalidOperationException(error);
            s.ExpeditionMoraleRestIntervals = Array.Empty<ExpeditionMoraleRestIntervalRecord>();
            s.ExpeditionMoraleRestBenefits = Array.Empty<ExpeditionMoraleRestBenefitRecord>();
        }

        private bool IsMoraleRestCommand(CommandKind kind)
            => kind == CommandKind.BeginMoraleRest || kind == CommandKind.InterruptMoraleRest;

        private ExpeditionMoraleRestIntervalRecord ActiveMoraleRest(Snapshot s, string actor)
            => moraleRestProfile == null ? null : s.ExpeditionMoraleRestIntervals.SingleOrDefault(x =>
                x.ActorId == actor && x.Status == MoraleRestIntervalStatus.Active);

        private bool HasActiveMoraleRest(Snapshot s)
            => moraleRestProfile != null && s.ExpeditionMoraleRestIntervals.Any(x => x.Status == MoraleRestIntervalStatus.Active);

        private string MoraleRestingActorCommandFailure(Snapshot s, Command c)
            => ActiveMoraleRest(s, c.Actor) != null && c.Kind != CommandKind.AdvanceClock
                && c.Kind != CommandKind.InterruptMoraleRest ? "ActorCurrentlyInMoraleRest" : null;

        private string AssessMoraleRestCommand(Snapshot s, Command c, out TestOnlyMoraleRestSiteFact site,
            out ExpeditionMoraleRestIntervalRecord active)
        {
            site = null; active = null;
            if (moraleRestProfile == null || s.SchemaVersion != Snapshot.MoraleRestSchema)
                return "MoraleRestNotSelected";
            if (!moraleRestProfile.IncludesActor(c.Actor)) return "MoraleRestActorNotRegistered";
            if (c.X != 0 || c.Y != 0 || c.Inventory != null || c.Combat != null || c.Advancement != null
                || c.Ranged != null || c.OverwatchRider != OverwatchRider.None || c.SuppressionFire != null
                || c.DefensiveFormation != null || c.ExpeditionAssignment != null || c.HarvestSelection != null
                || c.MiningSelection != null || c.ProspectingExposure != null || c.RouteMappingWork != null)
                return "InvalidMoraleRestCommandPayload";
            if (s.InventoryCombat || s.Encounter != null) return "MoraleRestUnavailableDuringCombat";
            if (c.Kind == CommandKind.BeginMoraleRest)
            {
                if (!CanVoluntarilyRecreate(s, c.Actor)) return "MoraleRestParticipantCannotChoose";
                if (!Validation.ValidId(c.Target)) return "InvalidMoraleRestSite";
                site = moraleRestProfile.Site(c.Target);
                if (site == null || !site.SafeRecreation || !site.MoraleRestEligible)
                    return "MoraleRestSiteNotQualified";
                var body = WorldPositionResolver.Position(s, c.Actor);
                if (body.X != new RuleQuantity(site.X) || body.Y != new RuleQuantity(site.Y))
                    return "ActorNotAtMoraleRestSite";
                if (ActiveMoraleRest(s, c.Actor) != null) return "ActorAlreadyInMoraleRest";
                RuleTime end = s.RuleClock.AddSeconds(MoraleRestSeconds);
                if (s.RestIntervals.Any(x => x.ActorId == c.Actor && x.Status == RestIntervalStatus.Active
                        && x.StartedAt < end && s.RuleClock < x.ScheduledEnd))
                    return "MoraleRestConflictsWithLongRest";
                if (s.ExpeditionMoraleRestIntervals.Any(x => x.ActorId == c.Actor
                        && x.Status == MoraleRestIntervalStatus.Active && x.StartedAt < end && s.RuleClock < x.ScheduledEnd))
                    return "MoraleRestConflictsWithActiveRecreation";
                if (WorldActivityValidation.HasActiveLabor(s, c.Actor, s.RuleClock, end)
                    || s.WorldTraversals.Any(x => x.ActorId == c.Actor)
                    || s.RouteTravels.Any(x => x.TravelerId == c.Actor && x.Status == ExpeditionRouteTravelStatus.Moving)
                    || s.ExpeditionAssignments.Any(x => x.WorkerId == c.Actor && x.Open)
                    || OrdinaryInventory.Busy(s, c.Actor))
                    return "MoraleRestConflictsWithAssignedActivity";
                if (s.ExpeditionMoraleRestIntervals.Length >= ExpeditionProvisioningValidation.MaxMoraleRestIntervals)
                    return "MoraleRestIntervalHistoryCapacityReached";
                return null;
            }
            if (c.Kind == CommandKind.InterruptMoraleRest)
            {
                if (!Validation.ValidId(c.Target)) return "InvalidMoraleRestInterval";
                active = ActiveMoraleRest(s, c.Actor);
                return active != null && active.Id == c.Target ? null : "NoActiveMoraleRest";
            }
            return "InvalidMoraleRestCommand";
        }

        private string ResolveMoraleRestCommand(Snapshot s, Command c)
        {
            string error = AssessMoraleRestCommand(s, c, out var site, out var active);
            if (error != null) return error;
            long revision = s.Revision + 1;
            if (c.Kind == CommandKind.BeginMoraleRest)
            {
                string id = "morale.interval." + c.Actor + ".r" + revision.ToString(CultureInfo.InvariantCulture);
                s.ExpeditionMoraleRestIntervals = s.ExpeditionMoraleRestIntervals.Concat(new[] {
                    new ExpeditionMoraleRestIntervalRecord(id, c.Actor, site.Id, site.ActivityId,
                        s.RuleClock, s.RuleClock.AddSeconds(MoraleRestSeconds), null,
                        MoraleRestIntervalStatus.Active, c.Id, revision)
                }).ToArray();
                return null;
            }
            s.ExpeditionMoraleRestIntervals = s.ExpeditionMoraleRestIntervals.Select(x => x.Id == active.Id
                ? x.With(s.RuleClock, MoraleRestIntervalStatus.Interrupted, c.Id, revision) : x).ToArray();
            return null;
        }

        private CommandQueryResult QueryMoraleRestCommand(Snapshot s, Command c)
        {
            string error = AssessMoraleRestCommand(s, c, out _, out _);
            return new CommandQueryResult(true, error == null, error ?? "Available", s.Revision);
        }

        private System.Collections.Generic.IEnumerable<Command> DiscoverMoraleRestCommands(Snapshot s, string actor)
        {
            if (moraleRestProfile == null || !moraleRestProfile.IncludesActor(actor)) return Array.Empty<Command>();
            var active = ActiveMoraleRest(s, actor);
            if (active != null)
                return new[] { new Command("option." + s.Revision.ToString(CultureInfo.InvariantCulture)
                    + ".morale.interrupt", actor, s.Revision, CommandKind.InterruptMoraleRest, active.Id) };
            var body = s.Actors.SingleOrDefault(x => x.Id == actor);
            if (body == null) return Array.Empty<Command>();
            return moraleRestProfile.Sites.Where(x => x.SafeRecreation && x.MoraleRestEligible
                    && body.X == x.X && body.Y == x.Y)
                .OrderBy(x => x.Id, StringComparer.Ordinal)
                .Select((x, i) => new Command("option." + s.Revision.ToString(CultureInfo.InvariantCulture)
                    + ".morale.begin." + i.ToString(CultureInfo.InvariantCulture), actor, s.Revision,
                    CommandKind.BeginMoraleRest, x.Id)).ToArray();
        }

        private RuleTime? NextMoraleRestBoundary(Snapshot s)
        {
            if (moraleRestProfile == null) return null;
            var ends = s.ExpeditionMoraleRestIntervals.Where(x => x.Status == MoraleRestIntervalStatus.Active
                    && x.ScheduledEnd > s.RuleClock).Select(x => x.ScheduledEnd).ToArray();
            return ends.Length == 0 ? (RuleTime?)null : ends.Min();
        }

        private bool CanVoluntarilyRecreate(Snapshot s, string actorId)
        {
            var life = s.Lives.SingleOrDefault(x => x.ActorId == actorId);
            return life != null && !life.Dead && life.Hp > 0
                && ExpeditionStrainRules.Project(s, actorId, s.RuleClock, s.Revision + 1).Level < 5
                && !TestOnlyClubAttackPolicy.ConditionsFor(s, actorId).View().Has(ConditionKind.Incapacitated);
        }

        private string InterruptMoraleRestOnIncapacity(Snapshot s, Command initiating)
        {
            if (moraleRestProfile == null) return null;
            var incapable = s.ExpeditionMoraleRestIntervals.Where(x => x.Status == MoraleRestIntervalStatus.Active
                    && !CanVoluntarilyRecreate(s, x.ActorId))
                .OrderBy(x => x.ActorId, StringComparer.Ordinal).ThenBy(x => x.Id, StringComparer.Ordinal).ToArray();
            foreach (var interval in incapable)
            {
                if (initiating == null) return "MoraleRestInterruptionCommandMissing";
                s.ExpeditionMoraleRestIntervals = s.ExpeditionMoraleRestIntervals.Select(x => x.Id == interval.Id
                    ? x.With(s.RuleClock, MoraleRestIntervalStatus.Interrupted, initiating.Id, s.Revision + 1) : x).ToArray();
            }
            return null;
        }

        private string ProcessMoraleRestBoundary(Snapshot s, Command initiating)
        {
            if (moraleRestProfile == null) return null;
            var due = s.ExpeditionMoraleRestIntervals.Where(x => x.Status == MoraleRestIntervalStatus.Active
                    && x.ScheduledEnd == s.RuleClock)
                .OrderBy(x => x.ActorId, StringComparer.Ordinal).ThenBy(x => x.Id, StringComparer.Ordinal).ToArray();
            foreach (var interval in due)
            {
                if (initiating == null) return "MoraleRestCompletionCommandMissing";
                if (!CanVoluntarilyRecreate(s, interval.ActorId))
                {
                    s.ExpeditionMoraleRestIntervals = s.ExpeditionMoraleRestIntervals.Select(x => x.Id == interval.Id
                        ? x.With(s.RuleClock, MoraleRestIntervalStatus.Interrupted, initiating.Id, s.Revision + 1) : x).ToArray();
                    continue;
                }
                long revision = s.Revision + 1;
                var completed = interval.With(interval.ScheduledEnd, MoraleRestIntervalStatus.Completed,
                    initiating.Id, revision);
                s.ExpeditionMoraleRestIntervals = s.ExpeditionMoraleRestIntervals.Select(x => x.Id == interval.Id
                    ? completed : x).ToArray();
                var lastBenefit = s.ExpeditionMoraleRestBenefits.Where(x => x.ActorId == interval.ActorId)
                    .OrderByDescending(x => x.CompletedAt).ThenByDescending(x => x.Revision).FirstOrDefault();
                if (lastBenefit != null && interval.ScheduledEnd < lastBenefit.CompletedAt.AddSeconds(24 * 60 * 60))
                    continue;
                if (s.ExpeditionMoraleRestBenefits.Length >= ExpeditionProvisioningValidation.MaxMoraleRestBenefits)
                    return "MoraleRestBenefitHistoryCapacityReached";

                string[] points = EligibleRecoveryPointsWithoutDebt(s, interval.ActorId, interval.ScheduledEnd, revision);
                string offerId = "";
                if (points.Length != 0)
                {
                    if (s.ExpeditionStrainRecoveryOffers.Length >= ExpeditionProvisioningValidation.MaxStrainRecoveryOffers)
                        return "ExpeditionStrainRecoveryOfferHistoryCapacityReached";
                    offerId = "strain.recovery.offer.r" + revision.ToString(CultureInfo.InvariantCulture)
                        + ".n" + s.ExpeditionStrainRecoveryOffers.Length.ToString(CultureInfo.InvariantCulture);
                }
                string benefitId = "morale.benefit.r" + revision.ToString(CultureInfo.InvariantCulture)
                    + ".n" + s.ExpeditionMoraleRestBenefits.Length.ToString(CultureInfo.InvariantCulture);
                var benefit = new ExpeditionMoraleRestBenefitRecord(benefitId, interval.ActorId,
                    interval.Id, offerId, interval.ScheduledEnd, revision);
                s.ExpeditionMoraleRestBenefits = s.ExpeditionMoraleRestBenefits.Concat(new[] { benefit }).ToArray();
                if (offerId != "")
                {
                    var offer = new ExpeditionStrainRecoveryOfferRecord(offerId, interval.ActorId,
                        ExpeditionRecoveryKind.MoraleRest, benefitId, interval.Id, initiating.Id,
                        interval.ScheduledEnd, revision, points);
                    s.ExpeditionStrainRecoveryOffers = s.ExpeditionStrainRecoveryOffers.Concat(new[] { offer }).ToArray();
                }
            }
            return null;
        }

        private string ValidateMoraleRestState(Snapshot s)
        {
            if (moraleRestProfile == null)
                return s.SchemaVersion != Snapshot.MoraleRestSchema && s.ExpeditionMoraleRestIntervals.Length == 0
                    && s.ExpeditionMoraleRestBenefits.Length == 0 ? null : "MoraleRestProfileMissing";
            if (s.SchemaVersion != Snapshot.MoraleRestSchema || !s.TestOnly || s.ContentFingerprint != ContentFingerprint
                || moraleRestProfile.ValidateBindings(s, restDebtProfile) != null)
                return "MoraleRestProfileMismatch";

            if (s.ExpeditionMoraleRestIntervals.Length > ExpeditionProvisioningValidation.MaxMoraleRestIntervals
                || s.ExpeditionMoraleRestBenefits.Length > ExpeditionProvisioningValidation.MaxMoraleRestBenefits
                || s.ExpeditionMoraleRestIntervals.Select(x => x.Id).Distinct(StringComparer.Ordinal).Count()
                    != s.ExpeditionMoraleRestIntervals.Length
                || s.ExpeditionMoraleRestIntervals.Any(x => Math.Max(x.StartRevision, x.EndRevision) > s.Revision
                    || x.StartedAt > s.RuleClock || x.EndedAt.HasValue && x.EndedAt.Value > s.RuleClock
                    || !moraleRestProfile.IncludesActor(x.ActorId)
                    || !s.Receipts.Any(r => r.Id == x.StartCommandId && r.Revision == x.StartRevision)
                    || x.Status == MoraleRestIntervalStatus.Active && (x.ScheduledEnd <= s.RuleClock
                        || x.EndedAt.HasValue || x.EndCommandId != "" || x.EndRevision != 0)
                    || x.Status == MoraleRestIntervalStatus.Completed && x.EndedAt != x.ScheduledEnd
                    || x.Status == MoraleRestIntervalStatus.Interrupted && (!x.EndedAt.HasValue
                        || x.EndedAt.Value > x.ScheduledEnd)
                    || x.EndCommandId != "" && !s.Receipts.Any(r => r.Id == x.EndCommandId && r.Revision == x.EndRevision)))
                return "InvalidMoraleRestIntervalHistory";

            foreach (var interval in s.ExpeditionMoraleRestIntervals)
            {
                var site = moraleRestProfile.Site(interval.SiteId);
                if (site == null || !site.SafeRecreation || !site.MoraleRestEligible || site.ActivityId != interval.ActivityId
                    || interval.ScheduledEnd != interval.StartedAt.AddSeconds(MoraleRestSeconds)
                    || !s.Receipts.Any(r => r.Id == interval.StartCommandId && r.Revision == interval.StartRevision
                        && CommandHistory.Read(r).Kind == CommandKind.BeginMoraleRest))
                    return "MoraleRestIntervalProfileMismatch";
                if (interval.Status == MoraleRestIntervalStatus.Completed
                    && !s.Receipts.Any(r => r.Id == interval.EndCommandId && r.Revision == interval.EndRevision))
                    return "MoraleRestCompletionCommandMissing";
                if (interval.Status == MoraleRestIntervalStatus.Interrupted
                    && !s.Receipts.Any(r => r.Id == interval.EndCommandId && r.Revision == interval.EndRevision
                        && (CommandHistory.Read(r).Kind == CommandKind.InterruptMoraleRest
                            && interval.EndedAt.Value < interval.ScheduledEnd
                            || CommandHistory.Read(r).Kind == CommandKind.AdvanceClock
                                && interval.EndedAt.Value <= interval.ScheduledEnd)))
                    return "MoraleRestInterruptCommandMissing";
                if (s.RestIntervals.Any(x => x.ActorId == interval.ActorId
                    && x.StartedAt < (interval.EndedAt ?? interval.ScheduledEnd)
                    && interval.StartedAt < (x.EndedAt ?? x.ScheduledEnd))
                    || s.ExpeditionMoraleRestIntervals.Any(x => x.Id != interval.Id && x.ActorId == interval.ActorId
                        && x.StartedAt < (interval.EndedAt ?? interval.ScheduledEnd)
                        && interval.StartedAt < (x.EndedAt ?? x.ScheduledEnd)))
                    return "MoraleRestIntervalOverlap";
            }

            if (s.ExpeditionMoraleRestBenefits.Select(x => x.Id).Distinct(StringComparer.Ordinal).Count()
                    != s.ExpeditionMoraleRestBenefits.Length
                || s.ExpeditionMoraleRestBenefits.Select(x => x.IntervalId).Distinct(StringComparer.Ordinal).Count()
                    != s.ExpeditionMoraleRestBenefits.Length
                || s.ExpeditionMoraleRestBenefits.Any(x => x.Revision > s.Revision || x.CompletedAt > s.RuleClock
                    || !moraleRestProfile.IncludesActor(x.ActorId)))
                return "InvalidMoraleRestBenefitHistory";
            foreach (var group in s.ExpeditionMoraleRestBenefits.GroupBy(x => x.ActorId, StringComparer.Ordinal))
            {
                var ordered = group.OrderBy(x => x.CompletedAt).ThenBy(x => x.Revision).ToArray();
                for (int i = 0; i < ordered.Length; i++)
                {
                    var benefit = ordered[i];
                    var interval = s.ExpeditionMoraleRestIntervals.SingleOrDefault(x => x.Id == benefit.IntervalId);
                    if (interval == null || interval.ActorId != benefit.ActorId
                        || interval.Status != MoraleRestIntervalStatus.Completed || interval.EndedAt != benefit.CompletedAt
                        || interval.EndRevision > benefit.Revision)
                        return "MoraleRestBenefitIntervalMismatch";
                    if (i > 0 && benefit.CompletedAt < ordered[i - 1].CompletedAt.AddSeconds(24 * 60 * 60))
                        return "MoraleRestBenefitLimitExceeded";
                    var offer = s.ExpeditionStrainRecoveryOffers.SingleOrDefault(x =>
                        x.RecoveryKind == ExpeditionRecoveryKind.MoraleRest && x.RecoveryCompletionId == benefit.Id);
                    if (benefit.RecoveryOfferId == "" ? offer != null
                        : offer == null || offer.Id != benefit.RecoveryOfferId || offer.ActorId != benefit.ActorId
                            || offer.CompletedAt != benefit.CompletedAt)
                        return "MoraleRestBenefitOfferMismatch";
                }
            }
            foreach (var group in s.ExpeditionMoraleRestIntervals.Where(x => x.Status == MoraleRestIntervalStatus.Completed)
                .GroupBy(x => x.ActorId, StringComparer.Ordinal))
            {
                RuleTime? last = null;
                foreach (var interval in group.OrderBy(x => x.EndedAt).ThenBy(x => x.EndRevision))
                {
                    bool shouldConsume = !last.HasValue || interval.EndedAt.Value >= last.Value.AddSeconds(24 * 60 * 60);
                    var benefit = s.ExpeditionMoraleRestBenefits.SingleOrDefault(x => x.IntervalId == interval.Id);
                    if (shouldConsume != (benefit != null)) return "MoraleRestAllowanceCompletionMismatch";
                    if (benefit != null) last = benefit.CompletedAt;
                }
            }
            return null;
        }

        private string OpenSchema65SecureRestOffers(Snapshot s, Command initiating)
        {
            var completed = s.RestIntervals.Where(x => x.Status == RestIntervalStatus.Completed
                    && x.EndedAt == s.RuleClock && strainRecoveryProfile.IsSecure(x.SiteId))
                .OrderBy(x => x.ActorId, StringComparer.Ordinal).ThenBy(x => x.Id, StringComparer.Ordinal).ToArray();
            foreach (var interval in completed)
            {
                if (s.ExpeditionBeneficialRests.Any(x => x.RestIntervalId == interval.Id)
                    || s.ExpeditionStrainRecoveryOffers.Any(x => x.RecoveryKind == ExpeditionRecoveryKind.SecureLongRest
                        && x.ActivityIntervalId == interval.Id)) continue;
                var last = LastBeneficialRest(s, interval.ActorId, interval.EndedAt.Value, s.Revision + 1);
                if (last.HasValue && interval.EndedAt.Value < last.Value.AddSeconds(24 * 60 * 60)) continue;
                if (RestDebtOwedAt(s, interval.ActorId, interval.EndedAt.Value, s.Revision + 1)) continue;
                if (s.ExpeditionBeneficialRests.Length >= ExpeditionProvisioningValidation.MaxBeneficialRests)
                    return "ExpeditionBeneficialRestHistoryCapacityReached";
                string[] points = EligibleRecoveryPoints(s, interval.ActorId, interval.EndedAt.Value, s.Revision + 1);
                string offerId = "";
                if (points.Length != 0)
                {
                    if (initiating == null) return "StrainRecoveryInitiatingCommandMissing";
                    if (s.ExpeditionStrainRecoveryOffers.Length >= ExpeditionProvisioningValidation.MaxStrainRecoveryOffers)
                        return "ExpeditionStrainRecoveryOfferHistoryCapacityReached";
                    offerId = "strain.recovery.offer.r" + (s.Revision + 1).ToString(CultureInfo.InvariantCulture)
                        + ".n" + s.ExpeditionStrainRecoveryOffers.Length.ToString(CultureInfo.InvariantCulture);
                }
                string benefitId = "strain.benefit.r" + (s.Revision + 1).ToString(CultureInfo.InvariantCulture)
                    + ".n" + s.ExpeditionBeneficialRests.Length.ToString(CultureInfo.InvariantCulture);
                var benefit = new ExpeditionBeneficialRestRecord(benefitId, interval.ActorId, offerId,
                    interval.Id, interval.EndedAt.Value, s.Revision + 1);
                s.ExpeditionBeneficialRests = s.ExpeditionBeneficialRests.Concat(new[] { benefit }).ToArray();
                if (offerId != "")
                {
                    var offer = new ExpeditionStrainRecoveryOfferRecord(offerId, interval.ActorId,
                        ExpeditionRecoveryKind.SecureLongRest, benefitId, interval.Id, initiating.Id,
                        interval.EndedAt.Value, s.Revision + 1, points);
                    s.ExpeditionStrainRecoveryOffers = s.ExpeditionStrainRecoveryOffers.Concat(new[] { offer }).ToArray();
                }
            }
            return null;
        }

        private string AssessSchema65RecoveryChoice(Snapshot s, Command c,
            out ExpeditionStrainRecoveryOfferRecord offer, out ExpeditionStrainGainRecord gain)
        {
            offer = null; gain = null;
            if (c.X != 0 || c.Y != 0 || c.Target == "" || c.Inventory != null || c.Combat != null
                || c.Advancement != null || c.Ranged != null || c.OverwatchRider != OverwatchRider.None
                || c.SuppressionFire != null || c.DefensiveFormation != null || c.ExpeditionAssignment != null
                || c.HarvestSelection != null || c.MiningSelection != null || c.ProspectingExposure != null
                || c.RouteMappingWork != null)
                return "InvalidStrainRecoveryChoicePayload";
            offer = PendingRecoveryOffer(s, c.Actor);
            if (offer == null) return "NoPendingStrainRecoveryChoice";
            if (!offer.PointIds.Contains(c.Target, StringComparer.Ordinal)) return "StrainRecoveryPointNotOffered";
            if (s.RuleClock != offer.CompletedAt) return "StrainRecoveryOfferClockChanged";
            if (ProvisioningBlockActive(s, c.Actor, offer.CompletedAt)) return "ProvisioningBlockPreventsStrainRecovery";
            var selectedOffer = offer;

            ExpeditionStrainGainRecord[] eligible;
            if (offer.RecoveryKind == ExpeditionRecoveryKind.SecureLongRest)
            {
                var interval = s.RestIntervals.SingleOrDefault(x => x.Id == selectedOffer.ActivityIntervalId
                    && x.ActorId == c.Actor && x.Status == RestIntervalStatus.Completed
                    && x.EndedAt == selectedOffer.CompletedAt && x.ScheduledEnd == selectedOffer.CompletedAt);
                var site = interval == null ? null : restDebtProfile.Site(interval.SiteId);
                var benefit = s.ExpeditionBeneficialRests.SingleOrDefault(x => x.Id == selectedOffer.RecoveryCompletionId
                    && x.RestIntervalId == selectedOffer.ActivityIntervalId && x.ActorId == c.Actor
                    && x.CompletedAt == selectedOffer.CompletedAt && x.RecoveryOfferId == selectedOffer.Id);
                if (interval == null || site == null || !strainRecoveryProfile.IsSecure(interval.SiteId)
                    || !site.SafeBerth || !site.QualifyingRestEligible || benefit == null
                    || RestDebtOwedAt(s, c.Actor, selectedOffer.CompletedAt, s.Revision + 1))
                    return "StrainRecoveryRestNoLongerSecure";
                var last = LastBeneficialRest(s, c.Actor, selectedOffer.CompletedAt, s.Revision + 1, interval.Id);
                if (last.HasValue && selectedOffer.CompletedAt < last.Value.AddSeconds(24 * 60 * 60))
                    return "BeneficialLongRestLimitNotElapsed";
                eligible = ExpeditionStrainRulesEligible(s, c.Actor, selectedOffer.CompletedAt, s.Revision + 1, true);
            }
            else if (offer.RecoveryKind == ExpeditionRecoveryKind.MoraleRest)
            {
                var interval = s.ExpeditionMoraleRestIntervals.SingleOrDefault(x => x.Id == selectedOffer.ActivityIntervalId
                    && x.ActorId == c.Actor && x.Status == MoraleRestIntervalStatus.Completed
                    && x.EndedAt == selectedOffer.CompletedAt);
                var site = interval == null ? null : moraleRestProfile.Site(interval.SiteId);
                var benefit = s.ExpeditionMoraleRestBenefits.SingleOrDefault(x => x.Id == selectedOffer.RecoveryCompletionId
                    && x.IntervalId == selectedOffer.ActivityIntervalId && x.ActorId == c.Actor
                    && x.CompletedAt == selectedOffer.CompletedAt && x.RecoveryOfferId == selectedOffer.Id);
                if (interval == null || site == null || !site.SafeRecreation || !site.MoraleRestEligible
                    || site.ActivityId != interval.ActivityId || benefit == null)
                    return "MoraleRestCompletionNoLongerEligible";
                var last = s.ExpeditionMoraleRestBenefits.Where(x => x.ActorId == c.Actor
                        && x.IntervalId != interval.Id && x.CompletedAt <= selectedOffer.CompletedAt)
                    .Select(x => (RuleTime?)x.CompletedAt).OrderByDescending(x => x).FirstOrDefault();
                if (last.HasValue && selectedOffer.CompletedAt < last.Value.AddSeconds(24 * 60 * 60))
                    return "MoraleRestLimitNotElapsed";
                eligible = ExpeditionStrainRulesEligible(s, c.Actor, selectedOffer.CompletedAt, s.Revision + 1, false);
            }
            else return "UnknownStrainRecoveryKind";

            if (!eligible.Any(x => x.PointId == c.Target)) return "StrainRecoveryPointNotEligible";
            gain = eligible.Single(x => x.PointId == c.Target);
            return null;
        }

        private ExpeditionStrainGainRecord[] ExpeditionStrainRulesEligible(Snapshot s, string actorId,
            RuleTime at, long revision, bool requireNoDebt)
        {
            if (strainRecoveryProfile == null || !restDebtProfile.IncludesActor(actorId)
                || ProvisioningBlockActive(s, actorId, at)
                || requireNoDebt && RestDebtOwedAt(s, actorId, at, revision)
                || ExpeditionStrainRules.Project(s, actorId, at, revision).Level >= 6)
                return Array.Empty<ExpeditionStrainGainRecord>();
            return s.ExpeditionStrainGains.Where(g => g.ActorId == actorId && g.PointId != ""
                    && g.AddedAmount == 1 && g.OrdinaryRemovable == true
                    && ExpeditionStrainRules.RecoveryGateMet(s, g, at, revision)
                    && ExpeditionStrainRules.IsActivePoint(s, actorId, g.PointId, at, revision))
                .OrderBy(g => g.PointId, StringComparer.Ordinal).ToArray();
        }

        private string ResolveSchema65RecoveryChoice(Snapshot s, Command c)
        {
            string failure = AssessSchema65RecoveryChoice(s, c, out var offer, out var gain);
            if (failure != null) return failure;
            if (s.ExpeditionStrainRemovals.Length >= ExpeditionProvisioningValidation.MaxStrainRemovals)
                return "ExpeditionStrainRecoveryHistoryCapacityReached";
            long revision = s.Revision + 1;
            int sequence = ExpeditionStrainRules.NextGainSequence(s, c.Actor, revision);
            string removalId = "strain.removal.r" + revision.ToString(CultureInfo.InvariantCulture)
                + ".n" + s.ExpeditionStrainRemovals.Length.ToString(CultureInfo.InvariantCulture);
            var removal = new ExpeditionStrainRemovalRecord(removalId, c.Actor, gain.PointId, gain.Id,
                offer.RecoveryKind, offer.RecoveryCompletionId, offer.CompletedAt, revision, sequence);
            var previous = ExpeditionStrainRules.Current(s, c.Actor);
            s.ExpeditionStrainRemovals = s.ExpeditionStrainRemovals.Concat(new[] { removal }).ToArray();
            s.ExpeditionStrainRecoveryOffers = s.ExpeditionStrainRecoveryOffers.Select(x => x.Id == offer.Id
                ? new ExpeditionStrainRecoveryOfferRecord(x.Id, x.ActorId, x.RecoveryKind, x.RecoveryCompletionId,
                    x.ActivityIntervalId, x.InitiatingCommandId, x.CompletedAt, x.Revision, x.PointIds,
                    c.Target, revision) : x).ToArray();
            var current = ExpeditionStrainRules.Project(s, c.Actor, s.RuleClock, revision);
            if (current.Level != previous.Level - 1) return "StrainRecoveryProjectionMismatch";
            if (previous.Level >= 3 && current.Level < 3)
                s.ExpeditionDashLocks = s.ExpeditionDashLocks.Where(x => x.ActorId != c.Actor).ToArray();
            return HasPendingRecoveryOffer(s) || ManufacturingChoicePending(s) ? null : ResumeManufacturingAdvance(s, c);
        }

        private string ValidateSchema65StrainRecoveryState(Snapshot s)
        {
            if (strainRecoveryProfile == null || s.SchemaVersion != Snapshot.MoraleRestSchema || !s.TestOnly
                || s.ContentFingerprint != ContentFingerprint || strainRecoveryProfile.ValidateBindings(restDebtProfile) != null)
                return "StrainRecoveryProfileMismatch";
            foreach (var benefit in s.ExpeditionBeneficialRests)
            {
                var interval = s.RestIntervals.SingleOrDefault(x => x.Id == benefit.RestIntervalId);
                if (interval == null || !strainRecoveryProfile.IsSecure(interval.SiteId)
                    || !restDebtProfile.IncludesActor(benefit.ActorId)
                    || RestDebtOwedAt(s, benefit.ActorId, benefit.CompletedAt, benefit.Revision))
                    return "StrainRecoveryBenefitProfileMismatch";
                var last = LastBeneficialRest(s, benefit.ActorId, benefit.CompletedAt, benefit.Revision, interval.Id);
                if (last.HasValue && benefit.CompletedAt < last.Value.AddSeconds(24 * 60 * 60))
                    return "StrainRecoveryBenefitExceedsBeneficialRestLimit";
            }
            foreach (var offer in s.ExpeditionStrainRecoveryOffers)
            {
                if (!restDebtProfile.IncludesActor(offer.ActorId)
                    || ProvisioningBlockActive(s, offer.ActorId, offer.CompletedAt))
                    return "StrainRecoveryOfferProfileMismatch";
                ExpeditionStrainGainRecord[] eligible;
                if (offer.RecoveryKind == ExpeditionRecoveryKind.SecureLongRest)
                {
                    var interval = s.RestIntervals.SingleOrDefault(x => x.Id == offer.ActivityIntervalId
                        && x.ActorId == offer.ActorId && x.Status == RestIntervalStatus.Completed
                        && x.EndedAt == offer.CompletedAt);
                    var site = interval == null ? null : restDebtProfile.Site(interval.SiteId);
                    var benefit = s.ExpeditionBeneficialRests.SingleOrDefault(x => x.Id == offer.RecoveryCompletionId
                        && x.RestIntervalId == offer.ActivityIntervalId && x.ActorId == offer.ActorId
                        && x.CompletedAt == offer.CompletedAt && x.RecoveryOfferId == offer.Id);
                    if (interval == null || site == null || !strainRecoveryProfile.IsSecure(interval.SiteId)
                        || !site.SafeBerth || !site.QualifyingRestEligible || benefit == null
                        || RestDebtOwedAt(s, offer.ActorId, offer.CompletedAt, offer.Revision))
                        return "StrainRecoveryOfferProfileMismatch";
                    eligible = ExpeditionStrainRulesEligible(s, offer.ActorId, offer.CompletedAt, offer.Revision, true);
                }
                else if (offer.RecoveryKind == ExpeditionRecoveryKind.MoraleRest)
                {
                    var interval = s.ExpeditionMoraleRestIntervals.SingleOrDefault(x => x.Id == offer.ActivityIntervalId
                        && x.ActorId == offer.ActorId && x.Status == MoraleRestIntervalStatus.Completed
                        && x.EndedAt == offer.CompletedAt);
                    var site = interval == null ? null : moraleRestProfile.Site(interval.SiteId);
                    var benefit = s.ExpeditionMoraleRestBenefits.SingleOrDefault(x => x.Id == offer.RecoveryCompletionId
                        && x.IntervalId == offer.ActivityIntervalId && x.ActorId == offer.ActorId
                        && x.CompletedAt == offer.CompletedAt && x.RecoveryOfferId == offer.Id);
                    if (interval == null || site == null || !site.SafeRecreation || !site.MoraleRestEligible
                        || site.ActivityId != interval.ActivityId || benefit == null)
                        return "MoraleRestOfferProfileMismatch";
                    eligible = ExpeditionStrainRulesEligible(s, offer.ActorId, offer.CompletedAt, offer.Revision, false);
                }
                else return "UnknownStrainRecoveryKind";
                if (eligible.Select(x => x.PointId).Except(offer.PointIds, StringComparer.Ordinal).Any()
                    || offer.PointIds.Except(eligible.Select(x => x.PointId), StringComparer.Ordinal).Any())
                    return "StrainRecoveryOfferContainsIneligiblePoint";
                var lastLongRest = LastBeneficialRest(s, offer.ActorId, offer.CompletedAt, offer.Revision,
                    offer.RecoveryKind == ExpeditionRecoveryKind.SecureLongRest ? offer.ActivityIntervalId : "");
                if (offer.RecoveryKind == ExpeditionRecoveryKind.SecureLongRest && lastLongRest.HasValue
                    && offer.CompletedAt < lastLongRest.Value.AddSeconds(24 * 60 * 60))
                    return "StrainRecoveryOfferExceedsBeneficialRestLimit";
                if (offer.RecoveryKind == ExpeditionRecoveryKind.MoraleRest)
                {
                    var prior = s.ExpeditionMoraleRestBenefits.Where(x => x.ActorId == offer.ActorId
                            && x.IntervalId != offer.ActivityIntervalId && x.CompletedAt <= offer.CompletedAt
                            && x.Revision <= offer.Revision)
                        .Select(x => (RuleTime?)x.CompletedAt).OrderByDescending(x => x).FirstOrDefault();
                    if (prior.HasValue && offer.CompletedAt < prior.Value.AddSeconds(24 * 60 * 60))
                        return "MoraleRestOfferExceedsBenefitLimit";
                }
            }
            return null;
        }
    }
}
#endif
