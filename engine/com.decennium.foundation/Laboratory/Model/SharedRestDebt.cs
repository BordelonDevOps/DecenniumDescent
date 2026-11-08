#if DECENNIUM_TEST_ONLY && (UNITY_EDITOR || DEVELOPMENT_BUILD || HEADLESS_TESTS)
using System;
using System.Collections.Generic;
using System.Globalization;
using System.Linq;
using System.Numerics;
using System.Security.Cryptography;
using System.Text;

namespace Decennium.Foundation.Laboratory
{
    /// <summary>Explicit fixture fact for a location that can host a qualifying Rest. Safety and
    /// qualification are authored fields; no location name is interpreted as a safety rule.</summary>
    public sealed class TestOnlyRestSiteFact
    {
        public string Id { get; }
        public int X { get; }
        public int Y { get; }
        public bool SafeBerth { get; }
        public bool QualifyingRestEligible { get; }

        public TestOnlyRestSiteFact(string id, int x, int y, bool safeBerth, bool qualifyingRestEligible)
        {
            if (!Validation.ValidId(id) || x < 0 || y < 0)
                throw new ArgumentException("Invalid TEST_ONLY Rest site fact.");
            Id = id; X = x; Y = y; SafeBerth = safeBerth; QualifyingRestEligible = qualifyingRestEligible;
        }

        internal string Canonical => Id + "|" + X.ToString(CultureInfo.InvariantCulture) + "|"
            + Y.ToString(CultureInfo.InvariantCulture) + "|safe=" + (SafeBerth ? "1" : "0")
            + "|qualifying=" + (QualifyingRestEligible ? "1" : "0");
    }

    /// <summary>Finite, fingerprinted safe-berth and actual-Rest facts for the MGT-03 prototype.
    /// It does not classify recovery or provide Long Rest benefits.</summary>
    public sealed class TestOnlyRestDebtProfile
    {
        public const string SourceId = "campaign.rest-debt";
        public const string TrackId = "expedition.strain";
        private readonly string[] eligibleActors;
        private readonly TestOnlyRestSiteFact[] sites;
        public IReadOnlyList<string> EligibleActors => Array.AsReadOnly(eligibleActors);
        public IReadOnlyList<TestOnlyRestSiteFact> Sites => Array.AsReadOnly(sites);

        public TestOnlyRestDebtProfile(IEnumerable<string> eligibleActors = null,
            IEnumerable<TestOnlyRestSiteFact> sites = null)
        {
            this.eligibleActors = (eligibleActors ?? new[] { TestOnlyPolicy.ActorId, TestOnlyPolicy.CompanionId })
                .OrderBy(x => x, StringComparer.Ordinal).ToArray();
            this.sites = (sites ?? new[] { new TestOnlyRestSiteFact("TEST_ONLY.safe-berth", 0, 0, true, true) })
                .OrderBy(x => x?.Id, StringComparer.Ordinal).ToArray();
            if (this.eligibleActors.Length == 0 || this.eligibleActors.Any(x => !Validation.ValidId(x))
                || this.eligibleActors.Distinct(StringComparer.Ordinal).Count() != this.eligibleActors.Length
                || this.sites.Length == 0 || this.sites.Any(x => x == null)
                || this.sites.Select(x => x.Id).Distinct(StringComparer.Ordinal).Count() != this.sites.Length
                || this.sites.Where(x => x.SafeBerth && x.QualifyingRestEligible)
                    .Select(x => x.X + "," + x.Y).Distinct(StringComparer.Ordinal).Count() != this.sites.Count(x => x.SafeBerth && x.QualifyingRestEligible))
                throw new ArgumentException("Invalid finite TEST_ONLY Rest Debt profile.");
        }

        internal string CanonicalKey => "rest-debt-v1|source=" + SourceId + "|track=" + TrackId
            + "|origin=0|watch-seconds=28800|daily-watches=3|default-slot=evening|owed-deadline-watches=2"
            + "|same-boundary=unpaid-deadline-before-missed-rest-v1|eligible="
            + string.Join(";", eligibleActors) + "|sites=" + string.Join(";", sites.Select(x => x.Canonical));

        internal bool IncludesActor(string actor) => eligibleActors.Contains(actor, StringComparer.Ordinal);
        internal TestOnlyRestSiteFact Site(string id) => sites.SingleOrDefault(x => x.Id == id);

        internal string ValidateBindings(Snapshot s, TestOnlyDailyProvisioningProfile provisioning)
            => provisioning != null && eligibleActors.All(actor => provisioning.Roster.Contains(actor)
                && s.Actors.Any(x => x.Id == actor) && s.Lives.Any(x => x.ActorId == actor))
                ? null : "RestDebtProfileActorMissing";

        internal static string BindFingerprint(string prior, TestOnlyRestDebtProfile profile)
        {
            using (var sha = SHA256.Create())
                return "TEST_ONLY.rest-debt-v1-" + string.Concat(sha.ComputeHash(
                    Encoding.UTF8.GetBytes(prior + "|" + profile.CanonicalKey))
                    .Select(b => b.ToString("x2", CultureInfo.InvariantCulture)));
        }
    }

    public sealed partial class TestOnlySharedWorldPolicy
    {
        private const long RestWatchSeconds = 8 * 60 * 60;
        private TestOnlyRestDebtProfile restDebtProfile;

        /// <summary>Selects the schema63 TEST_ONLY Rest Watch/Rest Debt rules over the fixed
        /// schema62 daily profile. Call after EnableDailyProvisioning and before Initial().</summary>
        public TestOnlySharedWorldPolicy EnableRestDebt(TestOnlyRestDebtProfile profile = null)
        {
            if (initializationStarted) throw new InvalidOperationException("Rest Debt profile must be selected before Initial().");
            if (dailyProvisioning == null) throw new InvalidOperationException("Rest Debt requires the fixed daily provisioning profile.");
            if (restDebtProfile != null) throw new InvalidOperationException("Rest Debt profile is already selected.");
            restDebtProfile = profile ?? new TestOnlyRestDebtProfile();
            ContentFingerprint = TestOnlyRestDebtProfile.BindFingerprint(ContentFingerprint, restDebtProfile);
            return this;
        }

        private void InitializeRestDebt(Snapshot s)
        {
            if (restDebtProfile == null) return;
            string error = restDebtProfile.ValidateBindings(s, dailyProvisioning);
            if (error != null) throw new InvalidOperationException(error);
            int expectedSchema = strainRecoveryProfile != null ? Snapshot.ExpeditionStrainRecoverySchema : Snapshot.RestDebtSchema;
            if (s.SchemaVersion != expectedSchema || s.RuleClock != dailyProvisioning.CanonicalDayOrigin)
                throw new InvalidOperationException("RestDebtRequiresCanonicalInitialProfile");
            s.RestWatchSchedules = Array.Empty<RestWatchScheduleRecord>();
            s.RestIntervals = Array.Empty<RestIntervalRecord>();
            s.RestWatchOutcomes = Array.Empty<RestWatchOutcomeRecord>();
            s.RestDebtEvents = Array.Empty<RestDebtEventRecord>();
        }

        private bool IsRestDebtCommand(CommandKind kind)
            => kind == CommandKind.ScheduleRestWatch || kind == CommandKind.BeginRest || kind == CommandKind.InterruptRest;

        private bool IsActorResting(Snapshot s, string actor)
            => restDebtProfile != null && s.RestIntervals.Any(x => x.ActorId == actor && x.Status == RestIntervalStatus.Active);

        private string RestingActorCommandFailure(Snapshot s, Command c)
            => IsActorResting(s, c.Actor) && c.Kind != CommandKind.AdvanceClock && !IsRestDebtCommand(c.Kind)
                ? "ActorCurrentlyResting" : null;

        private RuleTime WatchStart(long day, RestWatchSlot slot)
            => new RuleTime(checked(day * 86400 + (long)slot * RestWatchSeconds));

        private RuleTime WatchEnd(long day, RestWatchSlot slot)
            => WatchStart(day, slot).AddSeconds(RestWatchSeconds);

        private RestWatchSlot ScheduledRestWatch(Snapshot s, string actor, long day)
        {
            var change = s.RestWatchSchedules.Where(x => x.ActorId == actor && x.DayOrdinal == day)
                .OrderByDescending(x => x.At).ThenByDescending(x => x.Revision).ThenByDescending(x => x.Id, StringComparer.Ordinal)
                .FirstOrDefault();
            return change?.Slot ?? RestWatchSlot.Evening;
        }

        private sealed class RestDebtProjection
        {
            public string EpisodeId;
            public RuleTime Deadline;
            public bool Owed => EpisodeId != "";
        }

        private static RestDebtProjection DebtFor(Snapshot s, string actor)
        {
            var latest = s.RestDebtEvents.Where(x => x.ActorId == actor).OrderBy(x => x.At).ThenBy(x => x.Revision)
                .ThenBy(x => x.EventSequence).ThenBy(x => x.Id, StringComparer.Ordinal).LastOrDefault();
            return latest == null || latest.Kind == RestDebtEventKind.Cleared
                ? new RestDebtProjection { EpisodeId = "", Deadline = default }
                : new RestDebtProjection { EpisodeId = latest.EpisodeId, Deadline = latest.DeadlineAfter };
        }

        private RuleTime? NextRestDebtBoundary(Snapshot s)
        {
            if (restDebtProfile == null) return null;
            RuleTime? next = null;
            foreach (var interval in s.RestIntervals.Where(x => x.Status == RestIntervalStatus.Active))
                if (!next.HasValue || interval.ScheduledEnd < next.Value) next = interval.ScheduledEnd;

            long currentDay = checked((long)(s.RuleClock.Numerator / ((BigInteger)s.RuleClock.Denominator * 86400)));
            foreach (string actor in restDebtProfile.EligibleActors)
            {
                for (long day = currentDay; day <= checked(currentDay + 1); day++)
                {
                    RuleTime end = WatchEnd(day, ScheduledRestWatch(s, actor, day));
                    if (end > s.RuleClock && (!next.HasValue || end < next.Value)) next = end;
                }
                var debt = DebtFor(s, actor);
                if (debt.Owed && debt.Deadline > s.RuleClock && (!next.HasValue || debt.Deadline < next.Value))
                    next = debt.Deadline;
            }
            return next;
        }

        private string ResolveRestDebtCommand(Snapshot s, Command c)
        {
            int expectedSchema = strainRecoveryProfile != null ? Snapshot.ExpeditionStrainRecoverySchema : Snapshot.RestDebtSchema;
            if (restDebtProfile == null || s.SchemaVersion != expectedSchema) return "RestDebtNotSelected";
            if (!restDebtProfile.IncludesActor(c.Actor)) return "RestDebtActorNotRegistered";
            if (c.Inventory != null || c.Combat != null || c.Advancement != null || c.Ranged != null
                || c.OverwatchRider != OverwatchRider.None || c.SuppressionFire != null || c.DefensiveFormation != null
                || c.ExpeditionAssignment != null || c.HarvestSelection != null || c.MiningSelection != null
                || c.ProspectingExposure != null || c.RouteMappingWork != null)
                return "InvalidRestDebtCommandPayload";
            if (c.Kind == CommandKind.ScheduleRestWatch)
            {
                const string prefix = "day.";
                if (c.Target == null || !c.Target.StartsWith(prefix, StringComparison.Ordinal)
                    || !long.TryParse(c.Target.Substring(prefix.Length), NumberStyles.None, CultureInfo.InvariantCulture, out long day)
                    || day < 0 || c.Y != 0 || c.X < 0 || c.X > (int)RestWatchSlot.Evening
                    || s.RestWatchSchedules.Length >= ExpeditionProvisioningValidation.MaxRestWatchSchedules)
                    return "InvalidRestWatchSchedule";
                var slot = (RestWatchSlot)c.X;
                if (WatchStart(day, slot) < s.RuleClock) return "RestWatchChangeNotProspective";
                RuleTime dayStart = new RuleTime(checked(day * 86400));
                RuleTime dayEnd = dayStart.AddSeconds(86400);
                bool assignedEarlier = s.ExpeditionAssignments.Any(x => x.WorkerId == c.Actor
                        && x.AssignedAt >= dayStart && x.AssignedAt < dayEnd && x.AssignedAt <= s.RuleClock)
                    || s.Work.WorkerIntervals.Any(x => x.WorkerId == c.Actor && x.Start >= dayStart
                        && x.Start < dayEnd && x.Start <= s.RuleClock);
                if (assignedEarlier) return "RestWatchChangeAfterFirstAssignment";
                string id = "rest.schedule." + c.Actor + ".day." + day.ToString(CultureInfo.InvariantCulture)
                    + ".r" + (s.Revision + 1).ToString(CultureInfo.InvariantCulture);
                s.RestWatchSchedules = s.RestWatchSchedules.Concat(new[] { new RestWatchScheduleRecord(id,
                    c.Actor, day, slot, s.RuleClock, s.Revision + 1) }).ToArray();
                return null;
            }
            if (c.X != 0 || c.Y != 0) return "InvalidRestCommandCoordinates";
            if (s.InventoryCombat) return "RestUnavailableDuringTacticalCombat";
            if (c.Kind == CommandKind.BeginRest)
            {
                if (c.Target == null) return "InvalidRestSite";
                var site = restDebtProfile.Site(c.Target);
                if (site == null || !site.SafeBerth || !site.QualifyingRestEligible) return "RestSiteNotQualified";
                var position = WorldPositionResolver.Position(s, c.Actor);
                if (position.X != new RuleQuantity(site.X) || position.Y != new RuleQuantity(site.Y))
                    return "ActorNotAtRestSite";
                if (IsActorResting(s, c.Actor)) return "ActorAlreadyResting";
                RuleTime end = s.RuleClock.AddSeconds(RestWatchSeconds);
                if (WorldActivityValidation.HasActiveLabor(s, c.Actor, s.RuleClock, end)
                    || s.WorldTraversals.Any(x => x.ActorId == c.Actor)
                    || s.RouteTravels.Any(x => x.TravelerId == c.Actor && x.Status == ExpeditionRouteTravelStatus.Moving)
                    || s.ExpeditionAssignments.Any(x => x.WorkerId == c.Actor && x.Open))
                    return "RestConflictsWithAssignedActivity";
                if (s.RestIntervals.Length >= ExpeditionProvisioningValidation.MaxRestIntervals) return "RestIntervalHistoryCapacityReached";
                string id = "rest.interval." + c.Actor + ".r" + (s.Revision + 1).ToString(CultureInfo.InvariantCulture);
                s.RestIntervals = s.RestIntervals.Concat(new[] { new RestIntervalRecord(id, c.Actor, site.Id,
                    s.RuleClock, end, null, RestIntervalStatus.Active, s.Revision + 1) }).ToArray();
                return null;
            }
            if (c.Kind == CommandKind.InterruptRest)
            {
                var interval = s.RestIntervals.SingleOrDefault(x => x.Id == c.Target && x.ActorId == c.Actor);
                if (interval == null) return "UnknownRestInterval";
                if (interval.Status != RestIntervalStatus.Active) return "RestIntervalNotActive";
                if (s.RuleClock >= interval.ScheduledEnd) return "RestAlreadyComplete";
                s.RestIntervals = s.RestIntervals.Select(x => x.Id == interval.Id
                    ? new RestIntervalRecord(x.Id, x.ActorId, x.SiteId, x.StartedAt, x.ScheduledEnd,
                        s.RuleClock, RestIntervalStatus.Interrupted, s.Revision + 1) : x).ToArray();
                return null;
            }
            return "InvalidRestDebtCommand";
        }

        private string ProcessRestDebtBoundary(Snapshot s)
        {
            if (restDebtProfile == null) return null;
            long revision = s.Revision + 1;
            foreach (var active in s.RestIntervals.Where(x => x.Status == RestIntervalStatus.Active
                && x.ScheduledEnd == s.RuleClock).OrderBy(x => x.ActorId, StringComparer.Ordinal).ToArray())
                s.RestIntervals = s.RestIntervals.Select(x => x.Id == active.Id
                    ? new RestIntervalRecord(x.Id, x.ActorId, x.SiteId, x.StartedAt, x.ScheduledEnd,
                        s.RuleClock, RestIntervalStatus.Completed, revision) : x).ToArray();

            foreach (string actor in restDebtProfile.EligibleActors.OrderBy(x => x, StringComparer.Ordinal))
            {
                foreach (var interval in s.RestIntervals.Where(x => x.ActorId == actor && x.Status == RestIntervalStatus.Completed
                    && x.EndedAt == s.RuleClock).OrderBy(x => x.Id, StringComparer.Ordinal).ToArray())
                {
                    var debt = DebtFor(s, actor);
                    if (!debt.Owed) continue;
                    if (s.RestDebtEvents.Length >= ExpeditionProvisioningValidation.MaxRestDebtEvents) return "RestDebtHistoryCapacityReached";
                    string id = NextDebtEventId(s, actor, revision);
                    AppendDebtEvent(s, new RestDebtEventRecord(id, actor, RestDebtEventKind.Cleared,
                        s.RuleClock, revision, NextDebtEventSequence(s, actor, revision), debt.EpisodeId,
                        interval.Id, debt.Deadline, default, ""));
                }
            }

            var missed = new System.Collections.Generic.List<RestWatchOutcomeRecord>();
            if (s.RuleClock.Denominator == 1 && s.RuleClock.Numerator > 0 && s.RuleClock.Numerator % RestWatchSeconds == 0)
            {
                long ordinal = s.RuleClock.Numerator / RestWatchSeconds - 1;
                long day = ordinal / 3;
                var slot = (RestWatchSlot)(ordinal % 3);
                foreach (string actor in restDebtProfile.EligibleActors.OrderBy(x => x, StringComparer.Ordinal))
                {
                    if (ScheduledRestWatch(s, actor, day) != slot) continue;
                    if (s.RestWatchOutcomes.Any(x => x.ActorId == actor && x.DayOrdinal == day))
                        return "RestWatchOutcomeAlreadyExists";
                    if (s.RestWatchOutcomes.Length >= ExpeditionProvisioningValidation.MaxRestWatchOutcomes)
                        return "RestWatchOutcomeHistoryCapacityReached";
                    var rest = s.RestIntervals.SingleOrDefault(x => x.ActorId == actor && x.Status == RestIntervalStatus.Completed
                        && x.StartedAt == WatchStart(day, slot) && x.ScheduledEnd == s.RuleClock
                        && IsQualifiedSite(s, x.SiteId));
                    string id = "rest.watch." + actor + ".day." + day.ToString(CultureInfo.InvariantCulture);
                    var outcome = new RestWatchOutcomeRecord(id, actor, day, slot, WatchStart(day, slot),
                        s.RuleClock, rest == null ? RestWatchOutcomeKind.Missed : RestWatchOutcomeKind.Rested,
                        rest?.Id ?? "", revision);
                    s.RestWatchOutcomes = s.RestWatchOutcomes.Concat(new[] { outcome }).ToArray();
                    if (rest == null) missed.Add(outcome);
                }
            }

            // Resolve existing deadlines before evaluating a newly missed Watch at the same instant.
            // A completed qualifying Rest was already allowed to clear the debt above.
            foreach (string actor in restDebtProfile.EligibleActors.OrderBy(x => x, StringComparer.Ordinal))
            {
                var debt = DebtFor(s, actor);
                if (!debt.Owed || debt.Deadline != s.RuleClock) continue;
                if (s.RestDebtEvents.Any(x => x.ActorId == actor && x.EpisodeId == debt.EpisodeId
                    && x.Kind == RestDebtEventKind.UnpaidDeadline && x.At == s.RuleClock)) continue;
                if (s.RestDebtEvents.Length >= ExpeditionProvisioningValidation.MaxRestDebtEvents) return "RestDebtHistoryCapacityReached";
                if (s.ExpeditionStrainGains.Length >= ExpeditionProvisioningValidation.MaxStrainGains)
                    return "ExpeditionStrainHistoryCapacityReached";
                string id = NextDebtEventId(s, actor, revision);
                var gain = CreateRestDebtGain(s, actor, ExpeditionStrainCauseKind.RestDebtDeadline, id, revision);
                AppendDebtEvent(s, new RestDebtEventRecord(id, actor, RestDebtEventKind.UnpaidDeadline,
                    s.RuleClock, revision, NextDebtEventSequence(s, actor, revision), debt.EpisodeId,
                    debt.EpisodeId, debt.Deadline, debt.Deadline, gain.Id));
                AppendStrainGain(s, gain);
            }

            foreach (var outcome in missed.OrderBy(x => x.ActorId, StringComparer.Ordinal))
            {
                var debt = DebtFor(s, outcome.ActorId);
                if (s.RestDebtEvents.Length >= ExpeditionProvisioningValidation.MaxRestDebtEvents) return "RestDebtHistoryCapacityReached";
                string id = NextDebtEventId(s, outcome.ActorId, revision);
                if (!debt.Owed)
                {
                    string episodeId = id + ".episode";
                    AppendDebtEvent(s, new RestDebtEventRecord(id, outcome.ActorId, RestDebtEventKind.Opened,
                        s.RuleClock, revision, NextDebtEventSequence(s, outcome.ActorId, revision), episodeId,
                        outcome.Id, default, s.RuleClock.AddSeconds(2 * RestWatchSeconds), ""));
                }
                else
                {
                    if (s.ExpeditionStrainGains.Length >= ExpeditionProvisioningValidation.MaxStrainGains)
                        return "ExpeditionStrainHistoryCapacityReached";
                    var gain = CreateRestDebtGain(s, outcome.ActorId,
                        ExpeditionStrainCauseKind.RestMissedWhileIndebted, id, revision);
                    AppendDebtEvent(s, new RestDebtEventRecord(id, outcome.ActorId, RestDebtEventKind.MissedWhileIndebted,
                        s.RuleClock, revision, NextDebtEventSequence(s, outcome.ActorId, revision), debt.EpisodeId,
                        outcome.Id, debt.Deadline, s.RuleClock.AddSeconds(2 * RestWatchSeconds), gain.Id));
                    AppendStrainGain(s, gain);
                }
            }
            return null;
        }

        private bool IsQualifiedSite(Snapshot s, string siteId)
        {
            var fact = restDebtProfile?.Site(siteId);
            return fact != null && fact.SafeBerth && fact.QualifyingRestEligible;
        }

        private static int NextDebtEventSequence(Snapshot s, string actor, long revision)
            => s.RestDebtEvents.Where(x => x.ActorId == actor && x.Revision == revision)
                .Select(x => x.EventSequence).DefaultIfEmpty(-1).Max() + 1;

        private static string NextDebtEventId(Snapshot s, string actor, long revision)
            => "rest.debt." + actor + ".r" + revision.ToString(CultureInfo.InvariantCulture)
                + ".e" + NextDebtEventSequence(s, actor, revision).ToString(CultureInfo.InvariantCulture);

        private static void AppendDebtEvent(Snapshot s, RestDebtEventRecord value)
            => s.RestDebtEvents = s.RestDebtEvents.Concat(new[] { value }).ToArray();

        private static void AppendStrainGain(Snapshot s, ExpeditionStrainGainRecord value)
            => s.ExpeditionStrainGains = s.ExpeditionStrainGains.Concat(new[] { value }).ToArray();

        private static ExpeditionStrainGainRecord CreateRestDebtGain(Snapshot s, string actor,
            ExpeditionStrainCauseKind causeKind, string causeId, long revision)
        {
            if (s.ExpeditionStrainGains.Length >= ExpeditionProvisioningValidation.MaxStrainGains)
                throw new InvalidOperationException("ExpeditionStrainHistoryCapacityReached");
            int level = ExpeditionStrainRules.Project(s, actor, s.RuleClock, revision).Level;
            int added = Math.Min(1, 6 - level);
            var endpoint = level >= 5 ? ExpeditionStrainEndpoint.OrdinaryDeath : ExpeditionStrainEndpoint.None;
            string id = causeId + ".gain";
            var gain = new ExpeditionStrainGainRecord(id, added > 0 ? id + ".point" : "", causeKind,
                causeId, ExpeditionStrainRules.NextGainSequence(s, actor, revision), actor,
                TestOnlyRestDebtProfile.SourceId, TestOnlyRestDebtProfile.TrackId, s.RuleClock,
                revision, level, 1, added, null, null, endpoint);
            if (endpoint == ExpeditionStrainEndpoint.OrdinaryDeath && !s.Lives.Single(x => x.ActorId == actor).Dead)
            {
                var before = s.Lives.Single(x => x.ActorId == actor);
                var priorLife = ActorLifeRules.Read(before);
                var after = new LifeState(priorLife.MaximumHp, 0, priorLife.TemporaryHp, priorLife.Wounds,
                    stable: false, dead: true, deathSuccesses: before.DeathSuccesses,
                    deathFailures: before.DeathFailures, usesDeathSaves: before.UsesDeathSaves,
                    lastDeathTurn: before.LastDeathTurn);
                TestOnlyClubAttackPolicy.ApplyLife(s, before, after);
            }
            return gain;
        }

        private string ValidateRestDebtState(Snapshot s)
        {
            if (restDebtProfile == null)
                return s.RestWatchSchedules.Length == 0 && s.RestIntervals.Length == 0
                    && s.RestWatchOutcomes.Length == 0 && s.RestDebtEvents.Length == 0
                    && s.ExpeditionStrainGains.All(x => x.CauseKind == ExpeditionStrainCauseKind.DailyProvisioning)
                    ? null : "RestDebtProfileMissing";
            int expectedSchema = strainRecoveryProfile != null ? Snapshot.ExpeditionStrainRecoverySchema : Snapshot.RestDebtSchema;
            if (s.SchemaVersion != expectedSchema || s.ContentFingerprint != ContentFingerprint
                || restDebtProfile.ValidateBindings(s, dailyProvisioning) != null)
                return "RestDebtProfileMismatch";

            foreach (var schedule in s.RestWatchSchedules)
            {
                if (!restDebtProfile.IncludesActor(schedule.ActorId) || schedule.Revision > s.Revision
                    || schedule.At > s.RuleClock || schedule.At > WatchStart(schedule.DayOrdinal, schedule.Slot))
                    return "RestWatchScheduleProfileMismatch";
            }
            foreach (var interval in s.RestIntervals)
            {
                if (!restDebtProfile.IncludesActor(interval.ActorId) || interval.Revision > s.Revision
                    || interval.StartedAt > s.RuleClock || interval.EndedAt.HasValue && interval.EndedAt.Value > s.RuleClock
                    || !IsQualifiedSite(s, interval.SiteId)) return "RestIntervalProfileMismatch";
            }
            foreach (var outcome in s.RestWatchOutcomes)
            {
                if (!restDebtProfile.IncludesActor(outcome.ActorId) || outcome.Revision > s.Revision
                    || outcome.Slot != ScheduledRestWatchAt(s, outcome.ActorId, outcome.DayOrdinal, outcome.Start)
                    || outcome.Start != WatchStart(outcome.DayOrdinal, outcome.Slot)
                    || outcome.End != WatchEnd(outcome.DayOrdinal, outcome.Slot))
                    return "RestWatchOutcomeProfileMismatch";
            }

            long maxDay = checked((long)(s.RuleClock.Numerator / ((BigInteger)s.RuleClock.Denominator * 86400)));
            if (maxDay > ExpeditionProvisioningValidation.MaxRestWatchOutcomes / restDebtProfile.EligibleActors.Count + 1)
                return "RestWatchHistoryCapacityReached";
            var expectedKeys = new System.Collections.Generic.HashSet<string>(StringComparer.Ordinal);
            foreach (string actor in restDebtProfile.EligibleActors)
                for (long day = 0; day <= maxDay; day++)
                {
                    RestWatchSlot slot = ScheduledRestWatch(s, actor, day);
                    if (WatchEnd(day, slot) <= s.RuleClock)
                        expectedKeys.Add(actor + "|" + day.ToString(CultureInfo.InvariantCulture) + "|" + (int)slot);
                }
            var actualKeys = s.RestWatchOutcomes.Select(x => x.ActorId + "|" + x.DayOrdinal.ToString(CultureInfo.InvariantCulture)
                + "|" + (int)x.Slot).ToArray();
            if (expectedKeys.Count != actualKeys.Length || expectedKeys.Except(actualKeys, StringComparer.Ordinal).Any())
                return "RestWatchOutcomeCoverageMismatch";

            foreach (var gain in s.ExpeditionStrainGains.Where(x => x.CauseKind != ExpeditionStrainCauseKind.DailyProvisioning))
            {
                if (gain.SourceId != TestOnlyRestDebtProfile.SourceId || gain.TrackId != TestOnlyRestDebtProfile.TrackId
                    || gain.AttemptedAmount != 1 || gain.OrdinaryRemovable.HasValue || gain.RemovalGateMet.HasValue)
                    return "RestDebtStrainBindingMismatch";
                int level = ExpeditionStrainRules.PriorLevel(s, gain);
                int added = Math.Min(1, 6 - level);
                var endpoint = level >= 5 ? ExpeditionStrainEndpoint.OrdinaryDeath : ExpeditionStrainEndpoint.None;
                if (gain.LevelBefore != level || gain.AddedAmount != added || gain.Endpoint != endpoint)
                    return "RestDebtStrainHistoryMismatch";
            }
            return null;
        }

        private RestWatchSlot ScheduledRestWatchAt(Snapshot s, string actor, long day, RuleTime at)
        {
            var change = s.RestWatchSchedules.Where(x => x.ActorId == actor && x.DayOrdinal == day && x.At <= at)
                .OrderByDescending(x => x.At).ThenByDescending(x => x.Revision).ThenByDescending(x => x.Id, StringComparer.Ordinal)
                .FirstOrDefault();
            return change?.Slot ?? RestWatchSlot.Evening;
        }

        private CommandQueryResult QueryRestDebtCommand(Snapshot s, Command c)
        {
            if (restDebtProfile == null)
                return new CommandQueryResult(false, false, "UnsupportedOperation", s.Revision);
            string failure = ResolveRestDebtCommand(s, c);
            var costs = failure == null && c.Kind == CommandKind.BeginRest
                ? new[] { new CommandCost("rest-seconds", "", RestWatchSeconds) }
                : Array.Empty<CommandCost>();
            return new CommandQueryResult(true, failure == null, failure ?? "Available", s.Revision, costs);
        }
    }
}
#endif
