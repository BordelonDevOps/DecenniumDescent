#if DECENNIUM_TEST_ONLY && (UNITY_EDITOR || DEVELOPMENT_BUILD || HEADLESS_TESTS)
using System;
using System.Globalization;
using System.Linq;
using System.Security.Cryptography;
using System.Text;

namespace Decennium.Foundation.Laboratory
{
    /// <summary>One explicitly authored TEST_ONLY staffed Haven-care service. Its finite identity,
    /// admitted patients, availability and physical coverage are bound into the snapshot fingerprint.</summary>
    public sealed class TestOnlyHavenCareProfile
    {
        public const string SourceRevision = "46a4d52728ee6956f0bebcb5d2103ffd5bc67ba4";
        public const string StrainBlob = "7005aaf9558f0ce4f445ffe982dfa9b6f36c8ee4";
        public const string ExpeditionBookBlob = "466871fc128dc5f06043a874da2b9c1d94ed80a5";
        public const long CareSeconds = 24 * 60 * 60;
        public RuleQuantity FoodRequired => new RuleQuantity(2);
        public RuleQuantity WaterRequired => new RuleQuantity(8);
        public int PatientCapacity => 1;
        public string ProviderId { get; }
        public string ServiceId { get; }
        public string SiteId { get; }
        public bool CanDeliverReviewedCare { get; }
        public RuleTime AvailableFrom { get; }
        public RuleTime AvailableUntil { get; }
        public int SiteX { get; }
        public int SiteY { get; }
        private readonly string[] admittedPatients;
        public System.Collections.Generic.IReadOnlyList<string> AdmittedPatients
            => Array.AsReadOnly(admittedPatients);

        public TestOnlyHavenCareProfile(
            System.Collections.Generic.IEnumerable<string> admittedPatients = null,
            string providerId = "TEST_ONLY.haven-provider",
            string serviceId = "TEST_ONLY.haven-care-service",
            string siteId = "TEST_ONLY.haven-care-site",
            bool canDeliverReviewedCare = true,
            RuleTime? availableFrom = null,
            RuleTime? availableUntil = null,
            int siteX = 0,
            int siteY = 0)
        {
            this.admittedPatients = (admittedPatients ?? new[] { TestOnlyPolicy.ActorId })
                .OrderBy(x => x, StringComparer.Ordinal).ToArray();
            ProviderId = providerId; ServiceId = serviceId; SiteId = siteId;
            CanDeliverReviewedCare = canDeliverReviewedCare;
            AvailableFrom = availableFrom ?? default(RuleTime);
            AvailableUntil = availableUntil ?? new RuleTime(31536000, 1);
            SiteX = siteX; SiteY = siteY;
            if (!Validation.ValidId(ProviderId) || !Validation.ValidId(ServiceId) || !Validation.ValidId(SiteId)
                || this.admittedPatients.Length == 0 || this.admittedPatients.Length > Snapshot.MaxActors
                || this.admittedPatients.Any(x => !Validation.ValidId(x))
                || this.admittedPatients.Distinct(StringComparer.Ordinal).Count() != this.admittedPatients.Length
                || AvailableFrom < default(RuleTime) || AvailableUntil <= AvailableFrom)
                throw new ArgumentException("Invalid finite TEST_ONLY Haven-care service.");
        }

        internal string CanonicalKey => "haven-care-v1|source-revision=" + SourceRevision
            + "|strain=" + StrainBlob + "|book=" + ExpeditionBookBlob
            + "|provider=" + ProviderId + "|service=" + ServiceId + "|site=" + SiteId
            + "|can-deliver-reviewed-care=" + (CanDeliverReviewedCare ? "1" : "0")
            + "|availability=" + AvailableFrom.Numerator.ToString(CultureInfo.InvariantCulture) + "/"
            + AvailableFrom.Denominator.ToString(CultureInfo.InvariantCulture) + ".."
            + AvailableUntil.Numerator.ToString(CultureInfo.InvariantCulture) + "/"
            + AvailableUntil.Denominator.ToString(CultureInfo.InvariantCulture)
            + "|capacity=1|site-cell=" + SiteX.ToString(CultureInfo.InvariantCulture) + ","
            + SiteY.ToString(CultureInfo.InvariantCulture) + "|duration-seconds=" + CareSeconds.ToString(CultureInfo.InvariantCulture)
            + "|food-lb=2|water-pints=8|window=half-open|patients=" + string.Join(";", admittedPatients);

        internal bool IncludesPatient(string actorId) => admittedPatients.Contains(actorId, StringComparer.Ordinal);

        internal string ValidateBindings(Snapshot s, TestOnlyDailyProvisioningProfile provisioning,
            TestOnlyRestDebtProfile restDebt, TestOnlyExpeditionStrainRecoveryProfile recovery,
            TestOnlyMoraleRestProfile morale)
            => provisioning != null && restDebt != null && recovery != null && morale != null
                && admittedPatients.All(actor => s.Actors.Any(x => x.Id == actor)
                    && s.Lives.Any(x => x.ActorId == actor)
                    && provisioning.Roster.Contains(actor, StringComparer.Ordinal)
                    && restDebt.IncludesActor(actor) && morale.IncludesActor(actor))
                ? null : "HavenCarePatientNotRegistered";

        internal static string BindFingerprint(string prior, TestOnlyHavenCareProfile profile)
        {
            using (var sha = SHA256.Create())
                return "TEST_ONLY.haven-care-v1-" + string.Concat(sha.ComputeHash(
                    Encoding.UTF8.GetBytes(prior + "|" + profile.CanonicalKey))
                    .Select(b => b.ToString("x2", CultureInfo.InvariantCulture)));
        }
    }

    public sealed partial class TestOnlySharedWorldPolicy
    {
        private TestOnlyHavenCareProfile havenCareProfile;

        /// <summary>Selects bounded schema66 TEST_ONLY Haven care after the shared clock,
        /// provisioning, Rest Debt, Strain recovery and Morale authorities.</summary>
        public TestOnlySharedWorldPolicy EnableHavenCare(TestOnlyHavenCareProfile profile = null)
        {
            if (initializationStarted) throw new InvalidOperationException("Haven-care profile must be selected before Initial().");
            if (moraleRestProfile == null || strainRecoveryProfile == null || restDebtProfile == null || dailyProvisioning == null)
                throw new InvalidOperationException("Haven care requires provisioning, Rest Debt, Strain recovery and Morale profiles.");
            if (legacyStrainRecoverySemantics)
                throw new InvalidOperationException("Haven care requires typed schema65 Strain recovery semantics.");
            if (havenCareProfile != null) throw new InvalidOperationException("Haven-care profile is already selected.");
            havenCareProfile = profile ?? new TestOnlyHavenCareProfile();
            string error = havenCareProfile.ValidateBindings(bodies.Initial(), dailyProvisioning,
                restDebtProfile, strainRecoveryProfile, moraleRestProfile);
            if (error != null) throw new ArgumentException(error, nameof(profile));
            ContentFingerprint = TestOnlyHavenCareProfile.BindFingerprint(ContentFingerprint, havenCareProfile);
            return this;
        }

        private void InitializeHavenCare(Snapshot s)
        {
            if (havenCareProfile == null) return;
            if (s.SchemaVersion != Snapshot.HavenCareSchema)
                throw new InvalidOperationException("HavenCareRequiresSchema66");
            string error = havenCareProfile.ValidateBindings(s, dailyProvisioning,
                restDebtProfile, strainRecoveryProfile, moraleRestProfile);
            if (error != null) throw new InvalidOperationException(error);
            s.ExpeditionHavenCareIntervals = Array.Empty<ExpeditionHavenCareIntervalRecord>();
            s.ExpeditionHavenCareAssessments = Array.Empty<ExpeditionHavenCareAssessmentRecord>();
        }

        private bool IsHavenCareCommand(CommandKind kind)
            => kind == CommandKind.BeginHavenCare || kind == CommandKind.InterruptHavenCare;

        private ExpeditionHavenCareIntervalRecord ActiveHavenCare(Snapshot s, string actorId)
            => havenCareProfile == null ? null : s.ExpeditionHavenCareIntervals.SingleOrDefault(x =>
                x.ActorId == actorId && x.Status == HavenCareIntervalStatus.Active);

        private bool HasActiveHavenCare(Snapshot s)
            => havenCareProfile != null && s.ExpeditionHavenCareIntervals.Any(x => x.Status == HavenCareIntervalStatus.Active);

        private static bool HavenCareAllowsPatientCommand(CommandKind kind)
            => kind == CommandKind.AdvanceClock || kind == CommandKind.ScheduleRestWatch
                || kind == CommandKind.BeginRest || kind == CommandKind.InterruptRest
                || kind == CommandKind.BeginMoraleRest || kind == CommandKind.InterruptMoraleRest
                || kind == CommandKind.DispatchConditionEvent
                || kind == CommandKind.PortionInventory || kind == CommandKind.HandleInventory
                || kind == CommandKind.HandleVessel || kind == CommandKind.StartIntake
                || kind == CommandKind.InterruptIntake || kind == CommandKind.StartWaterFill
                || kind == CommandKind.PauseWaterFill || kind == CommandKind.ResumeWaterFill
                || kind == CommandKind.CancelWaterFill || kind == CommandKind.OpenPortableContainer
                || kind == CommandKind.ClosePortableContainer;

        private string HavenCareActorCommandFailure(Snapshot s, Command c)
        {
            if (ActiveHavenCare(s, c.Actor) != null && !HavenCareAllowsPatientCommand(c.Kind))
                return "ActorCurrentlyInHavenCare";
            return null;
        }

        private bool IsHavenCarePatient(Snapshot s, string actorId)
            => havenCareProfile != null && havenCareProfile.IncludesPatient(actorId)
                && ActiveHavenCare(s, actorId) != null;

        private void InterruptActiveHavenCare(Snapshot s, string commandId, long commandRevision,
            long applyRevision, string actorId = null)
        {
            foreach (var interval in s.ExpeditionHavenCareIntervals.Where(x =>
                    x.Status == HavenCareIntervalStatus.Active
                    && (actorId == null || x.ActorId == actorId))
                .OrderBy(x => x.ActorId, StringComparer.Ordinal).ThenBy(x => x.Id, StringComparer.Ordinal).ToArray())
                s.ExpeditionHavenCareIntervals = s.ExpeditionHavenCareIntervals.Select(x => x.Id == interval.Id
                    ? x.With(s.RuleClock, HavenCareIntervalStatus.Interrupted, commandId,
                        commandRevision, applyRevision) : x).ToArray();
        }

        private string AssessHavenCareCommand(Snapshot s, Command c,
            out ExpeditionHavenCareIntervalRecord active)
        {
            active = null;
            if (havenCareProfile == null || s.SchemaVersion != Snapshot.HavenCareSchema)
                return "HavenCareNotSelected";
            if (!havenCareProfile.IncludesPatient(c.Actor)) return "HavenCarePatientNotAdmitted";
            if (c.X != 0 || c.Y != 0 || c.Inventory != null || c.Combat != null || c.Advancement != null
                || c.Ranged != null || c.OverwatchRider != OverwatchRider.None || c.SuppressionFire != null
                || c.DefensiveFormation != null || c.ExpeditionAssignment != null || c.HarvestSelection != null
                || c.MiningSelection != null || c.ProspectingExposure != null || c.RouteMappingWork != null)
                return "InvalidHavenCareCommandPayload";
            if (s.InventoryCombat || s.Encounter != null && !ResolvedConflict(s))
                return "HavenCareUnavailableDuringCombat";
            if (c.Kind == CommandKind.BeginHavenCare)
            {
                if (c.Target != havenCareProfile.ServiceId) return "HavenCareServiceNotRegistered";
                if (!havenCareProfile.CanDeliverReviewedCare) return "HavenCareServiceNotQualified";
                if (s.Lives.Single(x => x.ActorId == c.Actor).Dead) return "HavenCarePatientIsDead";
                if (s.RuleClock < havenCareProfile.AvailableFrom) return "HavenCareServiceUnavailable";
                RuleTime scheduledEnd = s.RuleClock.AddSeconds(TestOnlyHavenCareProfile.CareSeconds);
                if (scheduledEnd > havenCareProfile.AvailableUntil) return "HavenCareServiceUnavailable";
                if (HasActiveHavenCare(s)) return "HavenCareServiceSlotOccupied";
                var position = WorldPositionResolver.Position(s, c.Actor);
                if (position.X != new RuleQuantity(havenCareProfile.SiteX)
                    || position.Y != new RuleQuantity(havenCareProfile.SiteY)
                    || s.WorldTraversals.Any(x => x.ActorId == c.Actor)
                    || s.RouteTravels.Any(x => x.TravelerId == c.Actor && x.Status == ExpeditionRouteTravelStatus.Moving))
                    return "HavenCarePatientNotAtServiceSite";
                if (WorldActivityValidation.HasActiveLabor(s, c.Actor, s.RuleClock, scheduledEnd)
                    || s.ExpeditionAssignments.Any(x => x.WorkerId == c.Actor && x.Open)
                    || OrdinaryInventory.Busy(s, c.Actor))
                    return "HavenCarePatientHasIncompatibleActivity";
                if (s.ExpeditionHavenCareIntervals.Length >= ExpeditionProvisioningValidation.MaxHavenCareIntervals)
                    return "HavenCareIntervalHistoryCapacityReached";
                return null;
            }
            if (c.Kind == CommandKind.InterruptHavenCare)
            {
                if (!Validation.ValidId(c.Target)) return "InvalidHavenCareInterval";
                active = ActiveHavenCare(s, c.Actor);
                return active != null && active.Id == c.Target ? null : "NoActiveHavenCare";
            }
            return "InvalidHavenCareCommand";
        }

        private string ResolveHavenCareCommand(Snapshot s, Command c)
        {
            string failure = AssessHavenCareCommand(s, c, out var active);
            if (failure != null) return failure;
            long revision = s.Revision + 1;
            if (c.Kind == CommandKind.BeginHavenCare)
            {
                string id = "haven.care.interval." + c.Actor + ".r" + revision.ToString(CultureInfo.InvariantCulture);
                s.ExpeditionHavenCareIntervals = s.ExpeditionHavenCareIntervals.Concat(new[] {
                    new ExpeditionHavenCareIntervalRecord(id, c.Actor, havenCareProfile.ProviderId,
                        havenCareProfile.ServiceId, havenCareProfile.SiteId, s.RuleClock,
                        s.RuleClock.AddSeconds(TestOnlyHavenCareProfile.CareSeconds), null,
                        HavenCareIntervalStatus.Active, c.Id, revision)
                }).ToArray();
                return null;
            }
            s.ExpeditionHavenCareIntervals = s.ExpeditionHavenCareIntervals.Select(x => x.Id == active.Id
                ? x.With(s.RuleClock, HavenCareIntervalStatus.Interrupted, c.Id, revision, revision) : x).ToArray();
            return null;
        }

        private CommandQueryResult QueryHavenCareCommand(Snapshot s, Command c)
        {
            string error = AssessHavenCareCommand(s, c, out _);
            return new CommandQueryResult(true, error == null, error ?? "Available", s.Revision);
        }

        private System.Collections.Generic.IEnumerable<Command> DiscoverHavenCareCommands(Snapshot s, string actorId)
        {
            if (havenCareProfile == null || !havenCareProfile.IncludesPatient(actorId))
                return Array.Empty<Command>();
            var active = ActiveHavenCare(s, actorId);
            if (active != null)
                return new[] { new Command("option." + s.Revision.ToString(CultureInfo.InvariantCulture)
                    + ".haven-care.interrupt", actorId, s.Revision, CommandKind.InterruptHavenCare, active.Id) };
            var body = s.Actors.SingleOrDefault(x => x.Id == actorId);
            if (body == null || WorldPositionResolver.Position(s, actorId).X != new RuleQuantity(havenCareProfile.SiteX)
                || WorldPositionResolver.Position(s, actorId).Y != new RuleQuantity(havenCareProfile.SiteY))
                return Array.Empty<Command>();
            var begin = new Command("option." + s.Revision.ToString(CultureInfo.InvariantCulture)
                + ".haven-care.begin", actorId, s.Revision, CommandKind.BeginHavenCare, havenCareProfile.ServiceId);
            return AssessHavenCareCommand(s, begin, out _) == null
                ? new[] { begin } : Array.Empty<Command>();
        }

        private RuleTime? NextHavenCareBoundary(Snapshot s)
        {
            if (havenCareProfile == null) return null;
            var ends = s.ExpeditionHavenCareIntervals.Where(x => x.Status == HavenCareIntervalStatus.Active
                    && x.ScheduledEnd > s.RuleClock)
                .Select(x => (RuleTime?)x.ScheduledEnd).ToArray();
            return ends.Length == 0 ? (RuleTime?)null : ends.Min();
        }

        private string ProcessHavenCareBoundary(Snapshot s, Command initiating,
            ManufacturingAdvanceRecord continuation = null)
        {
            if (havenCareProfile == null) return null;
            var active = s.ExpeditionHavenCareIntervals.Where(x => x.Status == HavenCareIntervalStatus.Active)
                .OrderBy(x => x.ActorId, StringComparer.Ordinal).ThenBy(x => x.Id, StringComparer.Ordinal).ToArray();
            if (s.InventoryCombat || s.Encounter != null && !ResolvedConflict(s))
            {
                if (active.Length != 0 && initiating == null) return "HavenCareBoundaryCommandMissing";
                if (active.Length != 0) InterruptActiveHavenCare(s,
                    continuation?.CommandId ?? initiating.Id,
                    continuation?.CommandRevision ?? s.Revision + 1, s.Revision + 1);
                return null;
            }
            foreach (var interval in active)
            {
                if (initiating == null) return "HavenCareBoundaryCommandMissing";
                var position = WorldPositionResolver.Position(s, interval.ActorId);
                bool dead = s.Lives.Single(x => x.ActorId == interval.ActorId).Dead;
                bool siteStillQualified = interval.ProviderId == havenCareProfile.ProviderId
                    && interval.ServiceId == havenCareProfile.ServiceId && interval.SiteId == havenCareProfile.SiteId
                    && havenCareProfile.CanDeliverReviewedCare
                    && position.X == new RuleQuantity(havenCareProfile.SiteX)
                    && position.Y == new RuleQuantity(havenCareProfile.SiteY);
                if (dead || !siteStillQualified)
                {
                    string commandId = continuation?.CommandId ?? initiating.Id;
                    long commandRevision = continuation?.CommandRevision ?? s.Revision + 1;
                    s.ExpeditionHavenCareIntervals = s.ExpeditionHavenCareIntervals.Select(x => x.Id == interval.Id
                        ? x.With(s.RuleClock, HavenCareIntervalStatus.Interrupted, commandId,
                            commandRevision, s.Revision + 1) : x).ToArray();
                    continue;
                }
                if (interval.ScheduledEnd < s.RuleClock) return "HavenCareCompletionBoundaryMissed";
                if (interval.ScheduledEnd != s.RuleClock) continue;

                long revision = s.Revision + 1;
                string command = continuation?.CommandId ?? initiating.Id;
                long commandRevisionAtBoundary = continuation?.CommandRevision ?? revision;
                var completed = interval.With(interval.ScheduledEnd, HavenCareIntervalStatus.Completed,
                    command, commandRevisionAtBoundary, revision);
                s.ExpeditionHavenCareIntervals = s.ExpeditionHavenCareIntervals.Select(x => x.Id == interval.Id
                    ? completed : x).ToArray();

                var support = HavenCareSupport(s, interval.ActorId, interval.StartedAt, interval.ScheduledEnd);
                bool supportQualified = support.Food >= havenCareProfile.FoodRequired
                    && support.Water >= havenCareProfile.WaterRequired;
                bool provisioningBlocked = ProvisioningBlockActive(s, interval.ActorId, interval.ScheduledEnd);
                string[] points = supportQualified && !provisioningBlocked
                    ? EligibleHavenCarePoints(s, interval.ActorId, interval.ScheduledEnd, revision)
                        .Select(x => x.PointId).OrderBy(x => x, StringComparer.Ordinal).ToArray()
                    : Array.Empty<string>();
                string assessmentId = "haven.care.completion.r" + revision.ToString(CultureInfo.InvariantCulture)
                    + ".n" + s.ExpeditionHavenCareAssessments.Length.ToString(CultureInfo.InvariantCulture);
                var assessment = new ExpeditionHavenCareAssessmentRecord(assessmentId, interval.Id,
                    interval.ActorId, interval.ScheduledEnd, revision, support.Food, support.Water,
                    supportQualified, provisioningBlocked, support.IntakeIds, points);
                s.ExpeditionHavenCareAssessments = s.ExpeditionHavenCareAssessments.Concat(new[] { assessment }).ToArray();
                if (points.Length == 0) continue;
                if (s.ExpeditionStrainRemovals.Length + points.Length > ExpeditionProvisioningValidation.MaxStrainRemovals)
                    return "ExpeditionStrainRecoveryHistoryCapacityReached";

                int sequence = ExpeditionStrainRules.NextGainSequence(s, interval.ActorId, revision);
                string[] ids = points.Select((pointId, i) => "strain.removal.r"
                    + revision.ToString(CultureInfo.InvariantCulture) + ".n"
                    + (s.ExpeditionStrainRemovals.Length + i).ToString(CultureInfo.InvariantCulture)).ToArray();
                var removals = points.Select((pointId, i) => {
                    var gain = s.ExpeditionStrainGains.Single(x => x.ActorId == interval.ActorId && x.PointId == pointId);
                    return new ExpeditionStrainRemovalRecord(ids[i], interval.ActorId, pointId, gain.Id,
                        ExpeditionRecoveryKind.HavenCare, assessment.Id, interval.ScheduledEnd,
                        revision, checked(sequence + i));
                }).ToArray();
                var before = ExpeditionStrainRules.Current(s, interval.ActorId);
                s.ExpeditionStrainRemovals = s.ExpeditionStrainRemovals.Concat(removals).ToArray();
                var after = ExpeditionStrainRules.Project(s, interval.ActorId, interval.ScheduledEnd, revision);
                if (after.Level != before.Level - points.Length) return "HavenCareStrainProjectionMismatch";
                if (before.Level >= 3 && after.Level < 3)
                    s.ExpeditionDashLocks = s.ExpeditionDashLocks.Where(x => x.ActorId != interval.ActorId).ToArray();
            }
            return null;
        }

        private static bool Later(RuleTime left, RuleTime right) => left > right;

        private static RuleTime Minimum(RuleTime left, RuleTime right) => left < right ? left : right;

        private (RuleQuantity Food, RuleQuantity Water, string[] IntakeIds) HavenCareSupport(
            Snapshot s, string actorId, RuleTime start, RuleTime end)
        {
            RuleQuantity food = default, water = default;
            var intakeIds = new System.Collections.Generic.List<string>();
            foreach (var intake in s.Intakes.Where(x => x.ActorId == actorId)
                .OrderBy(x => x.StartedAt).ThenBy(x => x.Id, StringComparer.Ordinal))
            {
                var lot = s.InventoryLots.SingleOrDefault(x => x.LotId == intake.LotId);
                if (lot == null || lot.Nutrition != NutritionKind.FoodPounds
                    && lot.Nutrition != NutritionKind.WaterPints) continue;
                var reservation = s.Work.Reservations.SingleOrDefault(x => x.Id == intake.ReservationId);
                if (reservation == null) continue;
                RuleTime overlapStart = intake.StartedAt > start ? intake.StartedAt : start;
                RuleTime intakeEnd = intake.EndedAt ?? end;
                RuleTime overlapEnd = Minimum(Minimum(intakeEnd, end), lot.FreshUntil ?? end);
                if (overlapEnd <= overlapStart) continue;
                long rate = OrdinaryInventory.SecondsPerUnit(lot.Nutrition);
                RuleQuantity elapsedInWindow = OrdinaryInventory.Quantity(CampGreens.Subtract(overlapEnd, overlapStart), rate);
                RuleTime priorEnd = Minimum(Minimum(overlapStart, intakeEnd), lot.FreshUntil ?? overlapStart);
                RuleQuantity elapsedBeforeWindow = priorEnd <= intake.StartedAt ? default(RuleQuantity)
                    : OrdinaryInventory.Quantity(CampGreens.Subtract(priorEnd, intake.StartedAt), rate);
                RuleQuantity unconsumedBefore = reservation.ConsumedAmount > elapsedBeforeWindow
                    ? reservation.ConsumedAmount - elapsedBeforeWindow : default(RuleQuantity);
                RuleQuantity amount = elapsedInWindow < unconsumedBefore ? elapsedInWindow : unconsumedBefore;
                if (amount <= default(RuleQuantity)) continue;
                if (lot.Nutrition == NutritionKind.FoodPounds) food += amount;
                else water += amount;
                intakeIds.Add(intake.Id);
            }
            return (food, water, intakeIds.OrderBy(x => x, StringComparer.Ordinal).Distinct(StringComparer.Ordinal).ToArray());
        }

        private ExpeditionStrainGainRecord[] EligibleHavenCarePoints(Snapshot s, string actorId,
            RuleTime at, long revision)
        {
            if (strainRecoveryProfile == null || !havenCareProfile.IncludesPatient(actorId)
                || ProvisioningBlockActive(s, actorId, at)
                || s.Lives.Single(x => x.ActorId == actorId).Dead
                || ExpeditionStrainRules.Project(s, actorId, at, revision).Level >= 6)
                return Array.Empty<ExpeditionStrainGainRecord>();
            return s.ExpeditionStrainGains.Where(g => g.ActorId == actorId && g.PointId != ""
                    && g.AddedAmount == 1 && g.OrdinaryRemovable == true
                    && ExpeditionStrainRules.RecoveryGateMet(s, g, at, revision)
                    && ExpeditionStrainRules.IsActivePoint(s, actorId, g.PointId, at, revision))
                .OrderBy(g => g.PointId, StringComparer.Ordinal).ToArray();
        }

        private string ValidateHavenCareState(Snapshot s)
        {
            if (havenCareProfile == null)
                return s.SchemaVersion != Snapshot.HavenCareSchema
                    && s.ExpeditionHavenCareIntervals.Length == 0
                    && s.ExpeditionHavenCareAssessments.Length == 0
                    && s.ExpeditionStrainRemovals.All(x => x.RecoveryKind != ExpeditionRecoveryKind.HavenCare)
                    ? null : "HavenCareProfileMissing";
            if (s.SchemaVersion != Snapshot.HavenCareSchema || !s.TestOnly
                || s.ContentFingerprint != ContentFingerprint
                || havenCareProfile.ValidateBindings(s, dailyProvisioning, restDebtProfile,
                    strainRecoveryProfile, moraleRestProfile) != null)
                return "HavenCareProfileMismatch";
            if (s.ExpeditionHavenCareIntervals.Any(x => x.ProviderId != havenCareProfile.ProviderId
                    || x.ServiceId != havenCareProfile.ServiceId || x.SiteId != havenCareProfile.SiteId
                    || !havenCareProfile.IncludesPatient(x.ActorId)
                    || !havenCareProfile.CanDeliverReviewedCare
                    || x.StartedAt < havenCareProfile.AvailableFrom
                    || x.ScheduledEnd > havenCareProfile.AvailableUntil)
                || s.ExpeditionHavenCareIntervals.Any(x => x.Status == HavenCareIntervalStatus.Active
                    && (s.InventoryCombat || s.Encounter != null && !ResolvedConflict(s)
                        || s.Lives.Single(y => y.ActorId == x.ActorId).Dead
                        || WorldPositionResolver.Position(s, x.ActorId).X != new RuleQuantity(havenCareProfile.SiteX)
                        || WorldPositionResolver.Position(s, x.ActorId).Y != new RuleQuantity(havenCareProfile.SiteY)
                        || s.WorldTraversals.Any(y => y.ActorId == x.ActorId)
                        || s.RouteTravels.Any(y => y.TravelerId == x.ActorId && y.Status == ExpeditionRouteTravelStatus.Moving))))
                return "HavenCareIntervalProfileMismatch";

            foreach (var assessment in s.ExpeditionHavenCareAssessments)
            {
                var interval = s.ExpeditionHavenCareIntervals.Single(x => x.Id == assessment.IntervalId);
                var support = HavenCareSupport(s, interval.ActorId, interval.StartedAt, interval.ScheduledEnd);
                bool qualified = support.Food >= havenCareProfile.FoodRequired
                    && support.Water >= havenCareProfile.WaterRequired;
                bool blocked = ProvisioningBlockActive(s, interval.ActorId, interval.ScheduledEnd);
                // The assessment records eligibility immediately before its own atomic removal
                // batch. Reconstruct that state so replay validation does not hide the points
                // that this assessment itself removed.
                var beforeAssessmentBatch = s.Copy();
                beforeAssessmentBatch.ExpeditionStrainRemovals = s.ExpeditionStrainRemovals
                    .Where(x => x.RecoveryCompletionId != assessment.Id).ToArray();
                string[] eligible = qualified && !blocked
                    ? EligibleHavenCarePoints(beforeAssessmentBatch, interval.ActorId,
                        interval.ScheduledEnd, assessment.Revision)
                        .Select(x => x.PointId).OrderBy(x => x, StringComparer.Ordinal).ToArray()
                    : Array.Empty<string>();
                if (support.Food != assessment.FoodConsumed || support.Water != assessment.WaterConsumed
                    || qualified != assessment.SupportQualified || blocked != assessment.ProvisioningBlockActive
                    || !support.IntakeIds.SequenceEqual(assessment.IntakeIds, StringComparer.Ordinal)
                    || !eligible.SequenceEqual(assessment.EligiblePointIds, StringComparer.Ordinal))
                    return "HavenCareAssessmentEvidenceMismatch";
            }
            return null;
        }
    }
}
#endif
