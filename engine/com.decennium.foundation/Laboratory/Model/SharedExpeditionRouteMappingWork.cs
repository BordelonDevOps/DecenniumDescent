#if DECENNIUM_TEST_ONLY && (UNITY_EDITOR || DEVELOPMENT_BUILD || HEADLESS_TESTS)
using System;
using System.Globalization;
using System.Linq;
using System.Security.Cryptography;
using System.Text;

namespace Decennium.Foundation.Laboratory
{
    public sealed class TestOnlyRouteMappingTaskProfile
    {
        public string RouteId { get; }
        public int Tier { get; }
        public int Dc => StandardDc(Tier);

        public TestOnlyRouteMappingTaskProfile(string routeId, int tier)
        {
            if (!Validation.ValidId(routeId) || tier < 1 || tier > 6)
                throw new ArgumentException("Invalid route-tier Map Route task profile.");
            RouteId = routeId; Tier = tier;
        }

        private static int StandardDc(int tier)
        {
            switch (tier)
            {
                case 1: return 12;
                case 2: return 13;
                case 3: return 15;
                case 4: return 16;
                case 5: return 18;
                case 6: return 19;
                default: throw new ArgumentOutOfRangeException(nameof(tier));
            }
        }

        internal string Canonical => RouteId + "|tier=" + Tier.ToString(CultureInfo.InvariantCulture)
            + "|dc=" + Dc.ToString(CultureInfo.InvariantCulture);
    }

    /// <summary>TEST_ONLY character-sheet training fact used by the route-work scenario.</summary>
    public sealed class TestOnlyRouteMappingSkillFact
    {
        public string ActorId { get; }
        public int ProficiencyRank { get; }
        public TestOnlyRouteMappingSkillFact(string actorId, int proficiencyRank)
        {
            if (!Validation.ValidId(actorId) || proficiencyRank < 0 || proficiencyRank > 2)
                throw new ArgumentException("Invalid TEST_ONLY Survival training fact.");
            ActorId = actorId; ProficiencyRank = proficiencyRank;
        }
        internal string Canonical => ActorId + "|survival|" + ProficiencyRank.ToString(CultureInfo.InvariantCulture);
    }

    /// <summary>Explicit stationary Map Route prototype profile. Tier and Survival training are
    /// finite TEST_ONLY content; this fixture does not change the physical route or authorize passage.</summary>
    public sealed class TestOnlyExpeditionRouteMappingWorkFixture
    {
        private const string PlayerBookSha256 = "4c58b9f7063e562b785b8db6006699d3c4f68edd0e697d06db69662ba9b7e480";
        private readonly TestOnlyRouteMappingTaskProfile[] tasks;
        private readonly TestOnlyRouteMappingSkillFact[] skills;
        public string RouteFingerprint { get; }
        public string Fingerprint { get; }
        public System.Collections.Generic.IReadOnlyList<TestOnlyRouteMappingTaskProfile> Tasks { get; }
        public System.Collections.Generic.IReadOnlyList<TestOnlyRouteMappingSkillFact> Skills { get; }
        public const int RequiredWorkSeconds = 480 * 60;
        public const string SkillId = "survival";
        public const int WisdomAbilityIndex = 4;

        public TestOnlyExpeditionRouteMappingWorkFixture(TestOnlyExpeditionRouteFixture routes,
            System.Collections.Generic.IEnumerable<TestOnlyRouteMappingTaskProfile> tasks,
            System.Collections.Generic.IEnumerable<TestOnlyRouteMappingSkillFact> skills = null)
        {
            if (routes == null || tasks == null) throw new ArgumentNullException(routes == null ? nameof(routes) : nameof(tasks));
            this.tasks = tasks.ToArray();
            this.skills = (skills ?? Array.Empty<TestOnlyRouteMappingSkillFact>()).ToArray();
            if (this.tasks.Length < 1 || this.tasks.Length > ExpeditionRouteMappingWorkValidation.MaxAttempts
                || this.tasks.Any(x => x == null) || this.tasks.Select(x => x.RouteId).Distinct(StringComparer.Ordinal).Count() != this.tasks.Length
                || this.tasks.Any(x => routes.Routes.All(route => route.Id != x.RouteId))
                || this.skills.Any(x => x == null) || this.skills.Select(x => x.ActorId).Distinct(StringComparer.Ordinal).Count() != this.skills.Length)
                throw new ArgumentException("Invalid finite Map Route work fixture.");
            RouteFingerprint = routes.Fingerprint;
            Array.Sort(this.tasks, (a, b) => StringComparer.Ordinal.Compare(a.RouteId, b.RouteId));
            Array.Sort(this.skills, (a, b) => StringComparer.Ordinal.Compare(a.ActorId, b.ActorId));
            Tasks = Array.AsReadOnly(this.tasks); Skills = Array.AsReadOnly(this.skills);
            string key = "ex58-exact-2026-10-11|FL-02/03/10|player-book-sha256=" + PlayerBookSha256
                + "|prototype-stationary-map-route-v1|wisdom-survival|route-tier-standard-dc|480-active-minutes"
                + "|trained-assistant-plus-one-max-three|success-one-critical-two|failed-retry-full-work"
                + "|test-party-alliance=actor+companion"
                + "|stationary-route-mouth-radius-one-test-cell|mapping-does-not-establish-passage-feasibility|" + RouteFingerprint + "|"
                + string.Join(";", this.tasks.Select(x => x.Canonical)) + "|"
                + string.Join(";", this.skills.Select(x => x.Canonical));
            using (var sha = SHA256.Create()) Fingerprint = "TEST_ONLY.route-map-work-v1-"
                + string.Concat(sha.ComputeHash(Encoding.UTF8.GetBytes(key)).Select(b => b.ToString("x2", CultureInfo.InvariantCulture)));
        }

        internal TestOnlyRouteMappingTaskProfile Find(string routeId)
            => tasks.SingleOrDefault(x => x.RouteId == routeId);

        internal string ValidateRoutes(TestOnlyExpeditionRouteFixture routes)
            => routes != null && routes.Fingerprint == RouteFingerprint
                && tasks.All(x => routes.Routes.Any(route => route.Id == x.RouteId))
                ? null : "RouteMappingWorkFixtureMismatch";

        internal string ValidateBindings(Snapshot s)
        {
            if (s == null || skills.Any(x => !s.Actors.Any(a => a.Id == x.ActorId))) return "RouteMappingSkillActorMissing";
            return null;
        }

        internal void Initialize(Snapshot s)
        {
            if (!s.TacticalAllies.Any(x => x.Includes(TestOnlyPolicy.ActorId)
                    && x.Other(TestOnlyPolicy.ActorId) == TestOnlyPolicy.CompanionId))
                s.TacticalAllies = s.TacticalAllies.Concat(new[] {
                    new TacticalAllyRecord(TestOnlyPolicy.ActorId, TestOnlyPolicy.CompanionId) }).ToArray();
            var fixtureActors = new System.Collections.Generic.HashSet<string>(skills.Select(x => x.ActorId), StringComparer.Ordinal);
            s.SkillTraining = s.SkillTraining.Where(x => x.SkillId != SkillId || !fixtureActors.Contains(x.ActorId))
                .Concat(skills.Where(x => x.ProficiencyRank > 0)
                    .Select(x => new SkillTrainingRecord(x.ActorId, SkillId, x.ProficiencyRank))).ToArray();
        }
    }

    public sealed partial class TestOnlySharedWorldPolicy
    {
        private TestOnlyExpeditionRouteMappingWorkFixture routeMappingWorkFixture;

        /// <summary>Opts this TEST_ONLY world into executable stationary Map Route work/check state.
        /// The physical route remains available to unrelated travelers; work reservations cover only participants.</summary>
        public TestOnlySharedWorldPolicy EnableRouteMappingWork(TestOnlyExpeditionRouteMappingWorkFixture fixture)
        {
            if (initializationStarted) throw new InvalidOperationException("World initialization has already started.");
            if (routeTravelFixture == null || fixture == null || routeMappingFixture != null || routeMappingWorkFixture != null
                || routeReconnaissanceFixture != null && dailyProvisioning == null
                || readyActionEnabled || cacheExcavationEnabled || dodgeActionEnabled || huntingTrapFixture != null)
                throw new ArgumentException("Map Route work requires one route profile and an unlayered route-work TEST_ONLY profile.");
            string error = fixture.ValidateRoutes(routeTravelFixture);
            if (error != null) throw new ArgumentException(error, nameof(fixture));
            routeMappingWorkFixture = fixture;
            using (var sha = SHA256.Create()) ContentFingerprint = "TEST_ONLY.route-map-work-v1-"
                + string.Concat(sha.ComputeHash(Encoding.UTF8.GetBytes(ContentFingerprint + "|" + fixture.Fingerprint))
                    .Select(b => b.ToString("x2", CultureInfo.InvariantCulture)));
            return this;
        }

        private static bool RouteMappingWorkCommand(CommandKind kind)
            => kind == CommandKind.StartRouteMappingWork || kind == CommandKind.PauseRouteMappingWork
                || kind == CommandKind.ResumeRouteMappingWork;

        private bool RouteMappingWorkSelected(Snapshot s)
            => routeMappingWorkFixture != null && (s.SchemaVersion == Snapshot.RouteMappingWorkSchema
                || expeditionCampConstructionProfile != null
                    && s.SchemaVersion == Snapshot.TemporaryCampConstructionSchema
                || portableStorageFixture != null && expeditionCampConstructionProfile != null
                    && s.SchemaVersion == Snapshot.PortableStorageSchema
                || dailyProvisioning != null && s.SchemaVersion == Snapshot.DailyProvisioningSchema
                || characterAdvancement!=null&&characterAdvancement.LevelFourAdvancementEnabled
                    &&s.SchemaVersion==Snapshot.SharedCharacterAdvancementSchema);

        private void InitializeRouteMappingWork(Snapshot s)
        {
            if (routeMappingWorkFixture == null) return;
            string error = routeMappingWorkFixture.ValidateBindings(s);
            if (error != null) throw new InvalidOperationException(error);
            routeMappingWorkFixture.Initialize(s);
        }

        private static void PutRouteMappingWork(Snapshot s, ExpeditionRouteMappingWorkAttemptRecord attempt)
            => s.RouteMappingWorkAttempts = s.RouteMappingWorkAttempts.Select(x => x.Id == attempt.Id ? attempt : x).ToArray();

        private string RouteMappingWorkerFailure(Snapshot s, string actorId, TestOnlyExpeditionRoute route,
            ExpeditionRouteMappingWorkAttemptRecord current)
        {
            if (s.InventoryCombat) return "RouteMappingWorkDuringTacticalControl";
            var actor = s.Actors.SingleOrDefault(x => x.Id == actorId);
            long distance = actor == null ? long.MaxValue : WorldSpatialQueries.CardinalDistance(actor.X, actor.Y, route.FromX, route.FromY);
            if (actor == null || distance > 1 || s.WorldTraversals.Any(x => x.ActorId == actorId)
                || s.RouteTravels.Any(x => x.TravelerId == actorId && x.Status != ExpeditionRouteTravelStatus.SegmentComplete))
                return "RouteMappingWorkerNotAtSite";
            if (!CapableWorker(s, actorId)) return "RouteMappingWorkerIncapable";
            RuleTime horizon = CampGreens.Add(s.RuleClock, new RuleTime(1));
            if (s.Work.WorkerIntervals.Any(x => x.WorkerId == actorId && x.JobId != current?.Id
                    && x.Start < horizon && x.End > s.RuleClock)
                || WorldActivityProjection.CurrentWork(s).Any(x => x.ActorId == actorId && x.Id != current?.Id))
                return "RouteMappingWorkerBusy";
            return null;
        }

        private string AssessRouteMappingWork(Snapshot s, Command c, out TestOnlyExpeditionRoute route,
            out ExpeditionRouteMappingWorkAttemptRecord current, out TestOnlyRouteMappingTaskProfile task)
        {
            route = null; current = null; task = null;
            if (!RouteMappingWorkSelected(s) || routeTravelFixture == null) return "RouteMappingWorkNotSelected";
            if (s.InventoryCombat) return "RouteMappingWorkDuringTacticalControl";
            if (s.RouteMappingResults.Length != 0) return "SyntheticRouteMappingResultsNotAllowed";
            if (c.Inventory != null || c.Combat != null || c.Advancement != null || c.Ranged != null
                || c.OverwatchRider != OverwatchRider.None || c.SuppressionFire != null || c.DefensiveFormation != null
                || c.ExpeditionAssignment != null || c.HarvestSelection != null || c.MiningSelection != null
                || c.ProspectingExposure != null || c.X != 0 || c.Y != 0) return "InvalidRouteMappingWorkRequest";
            if (c.Kind == CommandKind.StartRouteMappingWork)
            {
                if (c.Target == "" || c.RouteMappingWork == null) return "InvalidRouteMappingWorkRequest";
                route = routeTravelFixture.Find(c.Target);
                if (route == null) return "UnknownRoute";
                string requestedRouteId = route.Id;
                task = routeMappingWorkFixture.Find(route.Id);
                if (task == null) return "RouteMappingTaskUnavailable";
                if (s.RouteMappingWorkAttempts.Length >= ExpeditionRouteMappingWorkValidation.MaxAttempts)
                    return "RouteMappingWorkHistoryCapacityReached";
                if (s.RouteMappingWorkAttempts.Any(x => x.RouteId == requestedRouteId
                    && x.Status != ExpeditionRouteMappingWorkStatus.Resolved))
                    return "RouteMappingTaskAlreadyOpen";
                if (c.RouteMappingWork.AssistantIds.Contains(c.Actor, StringComparer.Ordinal))
                    return "RouteMappingLeadCannotAssist";
                var team = new[] { c.Actor }.Concat(c.RouteMappingWork.AssistantIds).ToArray();
                foreach (string actorId in team)
                {
                    string failure = RouteMappingWorkerFailure(s, actorId, route, null);
                    if (failure != null) return failure;
                }
                foreach (string assistantId in c.RouteMappingWork.AssistantIds)
                {
                    if (!CharacterSkillTrainingFacts.IsTrained(s, assistantId,
                        TestOnlyExpeditionRouteMappingWorkFixture.SkillId)) return "RouteMappingAssistantNotTrained";
                }
                RuleTime end = CampGreens.Add(s.RuleClock, new RuleTime(TestOnlyExpeditionRouteMappingWorkFixture.RequiredWorkSeconds));
                foreach (string actorId in team)
                    if (s.Work.WorkerIntervals.Any(x => x.WorkerId == actorId && x.Start < end && x.End > s.RuleClock))
                        return "RouteMappingWorkerBusy";
                return null;
            }
            if (c.Target == "" || c.RouteMappingWork != null) return "InvalidRouteMappingWorkRequest";
            current = s.RouteMappingWorkAttempts.SingleOrDefault(x => x.Id == c.Target && x.LeadId == c.Actor);
            if (current == null) return "UnknownRouteMappingWork";
            route = routeTravelFixture.Find(current.RouteId);
            task = route == null ? null : routeMappingWorkFixture.Find(route.Id);
            if (route == null || task == null) return "RouteMappingDefinitionMissing";
            if (c.Kind == CommandKind.PauseRouteMappingWork)
                return current.Status == ExpeditionRouteMappingWorkStatus.Working ? null : "RouteMappingWorkNotWorking";
            if (c.Kind != CommandKind.ResumeRouteMappingWork) return "InvalidRouteMappingWorkRequest";
            if (current.Status == ExpeditionRouteMappingWorkStatus.AwaitingCheck)
                return RouteMappingWorkerFailure(s, current.LeadId, route, current);
            if (current.Status != ExpeditionRouteMappingWorkStatus.Paused) return "RouteMappingWorkNotPaused";
            foreach (string actorId in new[] { current.LeadId }.Concat(current.AssistantIds))
            {
                string failure = RouteMappingWorkerFailure(s, actorId, route, current);
                if (failure != null) return failure;
            }
            RuleTime remaining = CampGreens.Subtract(current.WorkRequired, current.WorkDone);
            RuleTime endAt = CampGreens.Add(s.RuleClock, remaining);
            string currentId = current.Id;
            foreach (string actorId in new[] { current.LeadId }.Concat(current.AssistantIds))
                if (s.Work.WorkerIntervals.Any(x => x.WorkerId == actorId && x.JobId != currentId
                    && x.Start < endAt && x.End > s.RuleClock)) return "RouteMappingWorkerBusy";
            return null;
        }

        private string ResolveRouteMappingWork(Snapshot s, Command c)
        {
            string failure = AssessRouteMappingWork(s, c, out var route, out var current, out var task);
            if (failure != null) return failure;
            if (c.Kind == CommandKind.StartRouteMappingWork)
            {
                string id = "route.map.work." + (s.Revision + 1).ToString(CultureInfo.InvariantCulture);
                var attempt = new ExpeditionRouteMappingWorkAttemptRecord(id, route.Id, c.Actor,
                    c.RouteMappingWork.AssistantIds, s.Revision + 1, s.RuleClock, s.RuleClock, default,
                    new RuleTime(TestOnlyExpeditionRouteMappingWorkFixture.RequiredWorkSeconds),
                    ExpeditionRouteMappingWorkStatus.Working);
                BookRouteMappingWork(s, attempt);
                s.RouteMappingWorkAttempts = s.RouteMappingWorkAttempts.Concat(new[] { attempt }).ToArray();
                return null;
            }
            if (c.Kind == CommandKind.PauseRouteMappingWork) PauseRouteMappingWork(s, current);
            else if (current.Status == ExpeditionRouteMappingWorkStatus.AwaitingCheck)
                FinishRouteMappingWorkCheck(s, current, c.Id, s.Revision + 1);
            else
            {
                var resumed = current.WithWork(s.RuleClock, current.WorkDone, ExpeditionRouteMappingWorkStatus.Working);
                BookRouteMappingWork(s, resumed);
                PutRouteMappingWork(s, resumed);
            }
            return null;
        }

        private CommandQueryResult QueryRouteMappingWork(Snapshot s, Command c)
        {
            string error = AssessRouteMappingWork(s, c, out _, out var current, out _);
            long cost = error != null || c.Kind == CommandKind.PauseRouteMappingWork
                || current?.Status == ExpeditionRouteMappingWorkStatus.AwaitingCheck ? 0
                : c.Kind == CommandKind.StartRouteMappingWork ? TestOnlyExpeditionRouteMappingWorkFixture.RequiredWorkSeconds
                : CampGreens.Subtract(current.WorkRequired, current.WorkDone).Numerator;
            var costs = error == null && cost > 0
                ? new[] { new CommandCost("active-work-seconds", c.Target, cost) }
                : Array.Empty<CommandCost>();
            return new CommandQueryResult(true, error == null, error ?? "Available", s.Revision, costs);
        }

        private static void BookRouteMappingWork(Snapshot s, ExpeditionRouteMappingWorkAttemptRecord attempt)
        {
            RuleTime end = CampGreens.Add(s.RuleClock, CampGreens.Subtract(attempt.WorkRequired, attempt.WorkDone));
            string[] workers = new[] { attempt.LeadId }.Concat(attempt.AssistantIds).ToArray();
            string booking = (s.Revision + 1).ToString(CultureInfo.InvariantCulture);
            var intervals = workers.Select(id => new WorkerInterval(attempt.Id + ".labor." + id + "." + booking, attempt.Id,
                id, s.RuleClock, end)).ToArray();
            s.Work = s.Work.Reserve(attempt.Id, intervals, Array.Empty<ResourceReservation>());
        }

        private static void PauseRouteMappingWork(Snapshot s, ExpeditionRouteMappingWorkAttemptRecord attempt)
        {
            s.Work = s.Work.CancelFutureWork(attempt.Id, s.RuleClock);
            PutRouteMappingWork(s, attempt.WithWork(s.RuleClock, attempt.WorkDone, ExpeditionRouteMappingWorkStatus.Paused));
        }

        private void PauseIncompatibleRouteMappingWork(Snapshot s)
        {
            if (!RouteMappingWorkSelected(s)) return;
            foreach (var attempt in s.RouteMappingWorkAttempts.Where(x => x.Status == ExpeditionRouteMappingWorkStatus.Working).ToArray())
            {
                var route = routeTravelFixture.Find(attempt.RouteId);
                if (route == null || new[] { attempt.LeadId }.Concat(attempt.AssistantIds)
                    .Any(id => RouteMappingWorkerFailure(s, id, route, attempt) != null))
                    PauseRouteMappingWork(s, attempt);
            }
        }

        private RuleTime? NextRouteMappingWorkBoundary(Snapshot s)
        {
            if (!RouteMappingWorkSelected(s)) return null;
            var ends = s.RouteMappingWorkAttempts.Where(x => x.Status == ExpeditionRouteMappingWorkStatus.Working)
                .SelectMany(x => s.Work.WorkerIntervals.Where(w => w.JobId == x.Id && w.Start <= s.RuleClock && w.End > s.RuleClock)
                    .Select(w => w.End)).ToArray();
            return ends.Length == 0 ? (RuleTime?)null : ends.Min();
        }

        private void CreditRouteMappingWork(Snapshot s, RuleTime elapsed, Command initiating,
            System.Collections.Generic.ICollection<string> readyChecks = null)
        {
            if (!RouteMappingWorkSelected(s)) return;
            foreach (var attempt in s.RouteMappingWorkAttempts.Where(x => x.Status == ExpeditionRouteMappingWorkStatus.Working).ToArray())
            {
                string[] workers = new[] { attempt.LeadId }.Concat(attempt.AssistantIds).ToArray();
                if (workers.Any(id => !s.Work.WorkerIntervals.Any(w => w.JobId == attempt.Id && w.WorkerId == id
                    && w.Start <= attempt.UpdatedAt && w.End >= s.RuleClock)))
                    throw new InvalidOperationException("Map Route work interval is not reserved for every participant.");
                RuleTime progress = CampGreens.Add(attempt.WorkDone, elapsed);
                if (progress < attempt.WorkRequired)
                {
                    PutRouteMappingWork(s, attempt.WithWork(s.RuleClock, progress, ExpeditionRouteMappingWorkStatus.Working));
                    continue;
                }
                if (progress != attempt.WorkRequired)
                    throw new InvalidOperationException("Map Route task crossed its completion boundary without its command.");
                PutRouteMappingWork(s, attempt.AwaitCheck(s.RuleClock));
                readyChecks?.Add(attempt.Id);
            }
        }

        private static bool RouteMappingCheckDisadvantage(Snapshot s, string actorId, RuleTime at,
            long revision, int conditionOperationCount)
        {
            var journal = s.Conditions.Single(x => x.Target == actorId);
            var stamp = new ConditionStamp(at);
            if (conditionOperationCount < 0 || conditionOperationCount > journal.Operations.Count)
                throw new ArgumentException("Map Route condition evidence is outside the recorded history.");
            var operations = journal.Operations.Take(conditionOperationCount).ToArray();
            if (operations.Any(x => x.At.CompareTo(stamp) > 0))
                throw new ArgumentException("Map Route condition evidence includes a future operation.");
            var historicalJournal = new ConditionJournal(journal.PolicyId, journal.Target, journal.Origin,
                operations);
            var ledger = ConditionHistory.Restore(historicalJournal).Ledger;
            var marker = new EffectClockMarker(at);
            if (ledger.Now.CompareTo(marker) < 0) ledger = ledger.AdvanceTo(marker).State;
            return ledger.View().Has(ConditionKind.Poisoned)
                || ExpeditionStrainRules.Project(s, actorId, at, revision).ExpeditionCheckDisadvantage;
        }

        private void FinishRouteMappingWorkCheck(Snapshot s, ExpeditionRouteMappingWorkAttemptRecord attempt,
            string commandId, long appliedRevision)
        {
            if (attempt.Status != ExpeditionRouteMappingWorkStatus.AwaitingCheck || attempt.Check != null
                || attempt.WorkDone != attempt.WorkRequired)
                throw new InvalidOperationException("Map Route check is not awaiting resolution.");
            var route = routeTravelFixture.Find(attempt.RouteId);
            var task = route == null ? null : routeMappingWorkFixture.Find(route.Id);
            var leadFailure = route == null ? "RouteMappingDefinitionMissing"
                : RouteMappingWorkerFailure(s, attempt.LeadId, route, attempt);
            if (task == null || leadFailure != null) throw new InvalidOperationException(leadFailure ?? "RouteMappingDefinitionMissing");
            var actorFacts = CharacterStateFacts.ForActor(s, attempt.LeadId, TestOnlyExpeditionRouteMappingWorkFixture.SkillId);
            var modifier = actorFacts.DeriveCheck(CharacterAbility.Wisdom);
            int leadModifier = checked(modifier.TotalWithInjury(actorFacts)
                + ExpeditionStrainRules.Project(s, attempt.LeadId, s.RuleClock, appliedRevision).ExpeditionCheckModifier);
            int assistantBonus = attempt.AssistantIds.Length;
            int conditionOperationCount = s.Conditions.Single(x => x.Target == attempt.LeadId).Operations.Count;
            bool disadvantage = RouteMappingCheckDisadvantage(s, attempt.LeadId, s.RuleClock, appliedRevision, conditionOperationCount);
            uint before = s.RandomState;
            RuleD20Roll roll = RuleDice.RollD20(before, disadvantageSources: disadvantage ? 1 : 0);
            var outcome = RuleResolution.TaskCheck(roll.Natural, checked(leadModifier + assistantBonus), task.Dc);
            ExpeditionRouteMappingResultDegree degree = outcome.Degree == RuleTaskDegree.CriticalFailure
                ? ExpeditionRouteMappingResultDegree.CriticalFailure
                : outcome.Degree == RuleTaskDegree.Failure ? ExpeditionRouteMappingResultDegree.Failure
                : outcome.Degree == RuleTaskDegree.Success ? ExpeditionRouteMappingResultDegree.Success
                : ExpeditionRouteMappingResultDegree.CriticalSuccess;
            s.RandomState = roll.NextRandomState;
            var knowledge = ExpeditionRouteMappingRules.Current(s, route.Id, route.Mapping);
            var updated = ExpeditionRouteMappingRules.Apply(knowledge, route.Risk, degree, out int marksGranted);
            var check = new ExpeditionRouteMappingWorkCheckRecord(commandId, appliedRevision, s.RuleClock,
                leadModifier, modifier.ProficiencyRank, modifier.ProficiencyBonus, assistantBonus, task.Dc,
                conditionOperationCount,
                disadvantage, roll.First, roll.Second ?? 0, roll.Natural, outcome.Total, degree,
                before, roll.NextRandomState, roll.WordsConsumed, knowledge.Mapping, updated.Mapping,
                knowledge.UnspentMarks, marksGranted, updated.UnspentMarks,
                s.SchemaVersion>=Snapshot.SharedCharacterAdvancementSchema?actorFacts.Life.LinkedInjuries.ToArray():null);
            PutRouteMappingWork(s, attempt.Resolve(s.RuleClock, check));
        }

        private void ResolveReadyRouteMappingWorkChecks(Snapshot s,
            System.Collections.Generic.IEnumerable<string> attemptIds, Command initiating)
        {
            if (initiating == null || attemptIds == null) return;
            foreach (string id in attemptIds.Distinct(StringComparer.Ordinal))
            {
                var attempt = s.RouteMappingWorkAttempts.SingleOrDefault(x => x.Id == id);
                if (attempt == null || attempt.Status != ExpeditionRouteMappingWorkStatus.AwaitingCheck) continue;
                var route = routeTravelFixture.Find(attempt.RouteId);
                if (route != null && RouteMappingWorkerFailure(s, attempt.LeadId, route, attempt) == null)
                    FinishRouteMappingWorkCheck(s, attempt, initiating.Id, s.Revision + 1);
            }
        }

        private string ValidateRouteMappingWorkState(Snapshot s)
        {
            if (routeMappingWorkFixture == null)
                return s.RouteMappingWorkAttempts.Length == 0 && s.SchemaVersion != Snapshot.RouteMappingWorkSchema
                    ? null : "RouteMappingWorkFixtureMissing";
            if (!RouteMappingWorkSelected(s) || routeTravelFixture == null
                || routeMappingWorkFixture.ValidateRoutes(routeTravelFixture) != null
                || routeMappingWorkFixture.ValidateBindings(s) != null || s.RouteMappingResults.Length != 0)
                return "RouteMappingWorkSchemaOrFixtureMismatch";
            foreach (var attempt in s.RouteMappingWorkAttempts)
            {
                var route = routeTravelFixture.Find(attempt.RouteId);
                var task = route == null ? null : routeMappingWorkFixture.Find(route.Id);
                var startReceipt = s.Receipts.SingleOrDefault(x => x.Revision == attempt.StartedRevision);
                if (route == null || task == null || attempt.WorkRequired != new RuleTime(TestOnlyExpeditionRouteMappingWorkFixture.RequiredWorkSeconds)
                    || startReceipt == null) return "InvalidRouteMappingWorkEvidence";
                Command start;
                try { start = CommandHistory.Read(startReceipt); }
                catch (ArgumentException) { return "InvalidRouteMappingWorkStartCommand"; }
                if (start.Kind != CommandKind.StartRouteMappingWork || start.Actor != attempt.LeadId
                    || start.Target != route.Id || start.RouteMappingWork == null
                    || !start.RouteMappingWork.AssistantIds.SequenceEqual(attempt.AssistantIds)
                    || attempt.StartedAt > s.RuleClock) return "InvalidRouteMappingWorkStartCommand";
                if (attempt.Check != null)
                {
                    var check = attempt.Check;
                    var checkReceipt = s.Receipts.SingleOrDefault(x => x.Revision == check.AppliedRevision);
                    if (checkReceipt == null) return "InvalidRouteMappingWorkCheckCommand";
                    Command checkCommand;
                    try { checkCommand = CommandHistory.Read(checkReceipt); }
                    catch (ArgumentException) { return "InvalidRouteMappingWorkCheckCommand"; }
                    var conditionJournal = s.Conditions.Single(x => x.Target == attempt.LeadId);
                    if (check.ConditionOperationCount < 0
                        || check.ConditionOperationCount > conditionJournal.Operations.Count
                        || conditionJournal.Operations.Take(check.ConditionOperationCount)
                            .Any(x => x.At.CompareTo(new ConditionStamp(check.At)) > 0))
                        return "InvalidRouteMappingWorkConditionEvidence";
                    bool expectedDisadvantage = RouteMappingCheckDisadvantage(s, attempt.LeadId, check.At,
                        check.AppliedRevision, check.ConditionOperationCount);
                    RuleD20Roll replayedRoll = RuleDice.RollD20(check.RandomBefore,
                        disadvantageSources: check.Disadvantage ? 1 : 0);
                    if (checkReceipt.Id != check.CommandId || checkCommand.ExpectedRevision + 1 != check.AppliedRevision
                        || check.At < attempt.StartedAt || !expectedDisadvantage.Equals(check.Disadvantage)
                        || replayedRoll.Selection != (check.Disadvantage ? RuleD20Selection.Disadvantage : RuleD20Selection.Normal)
                        || replayedRoll.First != check.FirstRoll || replayedRoll.Second.GetValueOrDefault() != check.SecondRoll
                        || replayedRoll.Natural != check.Natural || replayedRoll.NextRandomState != check.RandomAfter
                        || replayedRoll.WordsConsumed != check.WordsConsumed)
                        return "InvalidRouteMappingWorkRandomEvidence";
                    var actorFacts = CharacterStateFacts.ForActor(s, attempt.LeadId, TestOnlyExpeditionRouteMappingWorkFixture.SkillId);
                    var historicalCharacter=s.SchemaVersion>=Snapshot.SharedCharacterAdvancementSchema
                        ?CharacterAdvancementRules.AtRevision(s,attempt.LeadId,check.AppliedRevision-1):actorFacts.Character;
                    var training=actorFacts.Training;
                    var modifier=AbilityCheckRules.Derive(historicalCharacter,training,CharacterAbility.Wisdom);
                    int injuryPenalty=s.SchemaVersion>=Snapshot.SharedCharacterAdvancementSchema
                        ?PlaytestLife.AbilityCheckInjuryPenalty(new LifeState(1,1,
                            wounds:check.LinkedInjuriesAtCheck.Select(x=>(Injury)x)),(int)CharacterAbility.Wisdom)
                        :actorFacts.InjuryPenalty(CharacterAbility.Wisdom);
                    int leadModifier=checked(modifier.Total+injuryPenalty
                        +ExpeditionStrainRules.Project(s,attempt.LeadId,check.At,check.AppliedRevision).ExpeditionCheckModifier);
                    var expected = RuleResolution.TaskCheck(check.Natural, checked(leadModifier + attempt.AssistantIds.Length), task.Dc);
                    ExpeditionRouteMappingResultDegree degree = expected.Degree == RuleTaskDegree.CriticalFailure
                        ? ExpeditionRouteMappingResultDegree.CriticalFailure
                        : expected.Degree == RuleTaskDegree.Failure ? ExpeditionRouteMappingResultDegree.Failure
                        : expected.Degree == RuleTaskDegree.Success ? ExpeditionRouteMappingResultDegree.Success
                        : ExpeditionRouteMappingResultDegree.CriticalSuccess;
                    var prior = s.RouteMappingWorkAttempts.Where(x => x.RouteId == route.Id && x.Check != null
                        && x.Check.AppliedRevision < check.AppliedRevision).OrderBy(x => x.Check.AppliedRevision).LastOrDefault();
                    var knowledge = prior == null ? new ExpeditionRouteMappingKnowledge(route.Mapping, 0)
                        : new ExpeditionRouteMappingKnowledge(prior.Check.MappingAfter, prior.Check.MarksAfter);
                    var result = ExpeditionRouteMappingRules.Apply(knowledge, route.Risk, degree, out int marks);
                    if (s.SchemaVersion>=Snapshot.SharedCharacterAdvancementSchema&&check.LinkedInjuriesAtCheck.Count>3)
                        return "InvalidRouteMappingWorkInjuryEvidence";
                    if (check.LeadModifier != leadModifier || check.ProficiencyRank != modifier.ProficiencyRank
                        || check.ProficiencyBonus != modifier.ProficiencyBonus || check.AssistantBonus != attempt.AssistantIds.Length
                        || check.Dc != task.Dc || check.Total != expected.Total || check.Degree != degree
                        || check.MappingBefore != knowledge.Mapping || check.MarksBefore != knowledge.UnspentMarks
                        || check.MappingAfter != result.Mapping || check.MarksGranted != marks || check.MarksAfter != result.UnspentMarks)
                        return "InvalidRouteMappingWorkCheck";
                }
                string[] team = new[] { attempt.LeadId }.Concat(attempt.AssistantIds).ToArray();
                var intervals = s.Work.WorkerIntervals.Where(x => x.JobId == attempt.Id).ToArray();
                if (intervals.Length == 0 && attempt.Status == ExpeditionRouteMappingWorkStatus.Paused
                    && attempt.WorkDone == default && attempt.Check == null) continue;
                if (intervals.Length == 0 || team.Any(actor => !intervals.Any(x => x.WorkerId == actor))
                    || intervals.Any(x => !team.Contains(x.WorkerId, StringComparer.Ordinal)))
                    return "InvalidRouteMappingWorkReservations";
                RuleTime credited = default;
                var leadIntervals = intervals.Where(x => x.WorkerId == attempt.LeadId).OrderBy(x => x.Start).ToArray();
                if (team.Any(worker => intervals.Count(x => x.WorkerId == worker) != leadIntervals.Length))
                    return "InvalidRouteMappingWorkTeamReservation";
                foreach (var interval in leadIntervals)
                {
                    RuleTime end = interval.End < s.RuleClock ? interval.End : s.RuleClock;
                    if (end > interval.Start) credited = CampGreens.Add(credited, CampGreens.Subtract(end, interval.Start));
                    if (team.Any(worker => !intervals.Any(other => other.WorkerId == worker
                        && other.Start == interval.Start && other.End == interval.End)))
                        return "InvalidRouteMappingWorkTeamReservation";
                }
                if (credited != attempt.WorkDone
                    || attempt.Status == ExpeditionRouteMappingWorkStatus.AwaitingCheck
                        && (leadIntervals.Length == 0 || leadIntervals[leadIntervals.Length - 1].End != attempt.UpdatedAt)
                    || attempt.Status == ExpeditionRouteMappingWorkStatus.Resolved
                        && (leadIntervals.Length == 0 || leadIntervals[leadIntervals.Length - 1].End > attempt.Check.At))
                    return "InvalidRouteMappingWorkProgressEvidence";
                var activePerWorker = team.ToDictionary(worker => worker,
                    worker => intervals.Count(x => x.WorkerId == worker && x.Start <= s.RuleClock && x.End > s.RuleClock),
                    StringComparer.Ordinal);
                bool working = attempt.Status == ExpeditionRouteMappingWorkStatus.Working;
                RuleTime expectedEnd = CampGreens.Add(s.RuleClock, CampGreens.Subtract(attempt.WorkRequired, attempt.WorkDone));
                if (activePerWorker.Values.Any(count => count != (working ? 1 : 0))
                    || working && team.Any(worker => !intervals.Any(x => x.WorkerId == worker
                        && x.Start <= s.RuleClock && x.End == expectedEnd)))
                    return "InvalidRouteMappingWorkReservationStatus";
            }
            return null;
        }
    }
}
#endif
