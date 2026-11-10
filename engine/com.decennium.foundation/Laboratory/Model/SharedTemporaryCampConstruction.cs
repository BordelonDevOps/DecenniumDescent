#if DECENNIUM_TEST_ONLY && (UNITY_EDITOR || DEVELOPMENT_BUILD || HEADLESS_TESTS)
using System;
using System.Globalization;
using System.Linq;
using System.Security.Cryptography;
using System.Text;

namespace Decennium.Foundation.Laboratory
{
    /// <summary>One fingerprinted TEST_ONLY two-person camp build at the selected FL-07 site.
    /// Enabling the profile seeds physical fixture lots only; it grants no skill or purchase.</summary>
    public sealed class TestOnlyExpeditionCampConstructionFixture
    {
        public const string SkillId = "survival";
        public const string TentProfileId = "adventuring-gear.tent-two-person";
        public const string PackProfileId = "expedition.temporary-fitting-pack";
        public const string TentLotId = "TEST_ONLY.camp.two-person-tent";
        public const string PackLotId = "TEST_ONLY.camp.fitting-pack";
        public const long FixtureMassPounds = 20;
        public const long RequiredWorkSeconds = 480 * 60;
        private readonly string[] assistantIds;
        public int RouteTier { get; }
        public string LeadId { get; }
        public string[] AssistantIds => (string[])assistantIds.Clone();
        public CharacterAbility Ability { get; }
        public string Fingerprint { get; }

        public TestOnlyExpeditionCampConstructionFixture(int routeTier, string leadId,
            string[] assistantIds, CharacterAbility ability)
        {
            var assistants = assistantIds ?? Array.Empty<string>();
            if (routeTier < 1 || routeTier > 6 || !Validation.ValidId(leadId)
                || assistants.Length > 3 || assistants.Any(x => !Validation.ValidId(x))
                || assistants.Contains(leadId, StringComparer.Ordinal)
                || assistants.Distinct(StringComparer.Ordinal).Count() != assistants.Length
                || ability != CharacterAbility.Strength && ability != CharacterAbility.Wisdom)
                throw new ArgumentException("Invalid TEST_ONLY Temporary Camp construction profile.");
            RouteTier = routeTier; LeadId = leadId; this.assistantIds = (string[])assistants.Clone(); Ability = ability;
            Fingerprint = "TEST_ONLY.camp-build-v1-" + Hash(Canonical);
        }

        internal string Canonical => string.Join("|", new[] { "MGT-03", "FL-07", "FL-03", "schema70-v1",
            "fixed-two-person-temporary-camp", routeTierInvariant, LeadId, SkillId, ((int)Ability).ToString(CultureInfo.InvariantCulture),
            string.Join(",", assistantIds), TentLotId, PackLotId, FixtureMassPounds.ToString(CultureInfo.InvariantCulture),
            RequiredWorkSeconds.ToString(CultureInfo.InvariantCulture), "no-price-debit", "durable-installation-claims" });
        private string routeTierInvariant => RouteTier.ToString(CultureInfo.InvariantCulture);
        internal string BindFingerprint(string prior) => "TEST_ONLY.camp-construction-v1-" + Hash(prior + "|" + Fingerprint);

        private static string Hash(string value)
        {
            using (var sha = SHA256.Create())
                return string.Concat(sha.ComputeHash(Encoding.UTF8.GetBytes(value))
                    .Select(x => x.ToString("x2", CultureInfo.InvariantCulture)));
        }
    }

    public sealed partial class TestOnlySharedWorldPolicy
    {
        private TestOnlyExpeditionCampConstructionFixture expeditionCampConstructionProfile;

        public TestOnlySharedWorldPolicy EnableExpeditionCampConstruction(
            TestOnlyExpeditionCampConstructionFixture fixture)
        {
            if (initializationStarted) throw new InvalidOperationException("World initialization has already started.");
            if (fixture == null || expeditionCampConstructionProfile != null)
                throw new ArgumentException("Supply one explicit temporary-camp construction fixture.");
            if (expeditionCampSiteProfile == null || expeditionPressureProfile == null || routeTravelFixture == null)
                throw new InvalidOperationException("TemporaryCampConstructionRequiresCampSitePressureAndRoute");
            if (fixture.LeadId != expeditionPressureProfile.MemberId)
                throw new ArgumentException("Temporary Camp lead must be the authored expedition member.");
            expeditionCampConstructionProfile = fixture;
            ContentFingerprint = fixture.BindFingerprint(ContentFingerprint);
            return this;
        }

        private void InitializeExpeditionCampConstruction(Snapshot s)
        {
            if (expeditionCampConstructionProfile == null) return;
            var site = s.ExpeditionCampSites.Single(x => x.Id == expeditionCampSiteProfile.Id);
            string location = PortableEquipmentValidation.GroundLocation(new PortableEquipmentRecord(
                TestOnlyExpeditionCampConstructionFixture.TentLotId,
                TestOnlyExpeditionCampConstructionFixture.TentProfileId,
                expeditionCampConstructionProfile.LeadId, expeditionCampConstructionProfile.LeadId, "",
                PortablePlacement.Ground, PortableLinkKind.None, "", PortableMassBasis.Fixed,
                new RuleQuantity(TestOnlyExpeditionCampConstructionFixture.FixtureMassPounds),
                new RuleQuantity(TestOnlyExpeditionCampConstructionFixture.FixtureMassPounds),
                groundX: site.RouteX, groundY: site.RouteY));
            string owner = expeditionCampConstructionProfile.LeadId;
            var tent = new ResourceLot(TestOnlyExpeditionCampConstructionFixture.TentLotId, "mass-pound",
                new RuleQuantity(TestOnlyExpeditionCampConstructionFixture.FixtureMassPounds), location, owner);
            var pack = new ResourceLot(TestOnlyExpeditionCampConstructionFixture.PackLotId, "mass-pound",
                new RuleQuantity(TestOnlyExpeditionCampConstructionFixture.FixtureMassPounds), location, owner);
            s.Work = new WorkLedger(s.Work.Lots.Concat(new[] { tent, pack }), s.Work.WorkerIntervals, s.Work.Reservations);
            s.InventoryLots = s.InventoryLots.Concat(new[] {
                new InventoryLotRecord(tent.Id, "", owner, tent.Amount, s.RuleClock, NutritionKind.None, null, InventoryAccess.Ground),
                new InventoryLotRecord(pack.Id, "", owner, pack.Amount, s.RuleClock, NutritionKind.None, null, InventoryAccess.Ground)
            }).ToArray();
            s.PortableEquipment = s.PortableEquipment.Concat(new[] {
                ConstructionItem(tent.Id, TestOnlyExpeditionCampConstructionFixture.TentProfileId, owner,
                    site.RouteX, site.RouteY, false),
                ConstructionItem(pack.Id, TestOnlyExpeditionCampConstructionFixture.PackProfileId, owner,
                    site.RouteX, site.RouteY, true)
            }).ToArray();
            s.TemporaryCampConstructionAttempts = Array.Empty<TemporaryCampConstructionAttemptRecord>();
            s.TemporaryCampInstallations = Array.Empty<TemporaryCampInstallationRecord>();
        }

        private static PortableEquipmentRecord ConstructionItem(string id, string profile, string owner,
            int x, int y, bool fittingPack)
            => new PortableEquipmentRecord(id, profile, owner, owner, "", PortablePlacement.Ground,
                PortableLinkKind.InventoryLot, id, PortableMassBasis.GenericPounds,
                new RuleQuantity(TestOnlyExpeditionCampConstructionFixture.FixtureMassPounds),
                null,
                capacityPounds: fittingPack ? new RuleQuantity(200) : (RuleQuantity?)null,
                capacityCubicFeet: fittingPack ? new RuleQuantity(20) : (RuleQuantity?)null,
                groundX: x, groundY: y);

        private static string GroundSiteLocation(int x, int y) => "ground." + x.ToString(CultureInfo.InvariantCulture) + "." + y.ToString(CultureInfo.InvariantCulture);

        private string ValidateTemporaryCampConstructionFixtureState(Snapshot s)
        {
            if (expeditionCampConstructionProfile == null)
                return s.TemporaryCampConstructionAttempts.Length + s.TemporaryCampInstallations.Length == 0
                    ? null : "TemporaryCampConstructionFixtureMissing";
            if ((s.SchemaVersion != Snapshot.TemporaryCampConstructionSchema
                    && !(portableStorageFixture != null && s.SchemaVersion == Snapshot.PortableStorageSchema)
                    && !(recipe347Fixture != null && s.SchemaVersion == Snapshot.Recipe347Schema))
                || s.ExpeditionCampSites.Length != 1 || expeditionCampSiteProfile == null
                || expeditionCampSiteProfile.Id != s.ExpeditionCampSites[0].Id)
                return "TemporaryCampConstructionProfileMismatch";
            var profile = expeditionCampConstructionProfile;
            var site = s.ExpeditionCampSites.Single();
            if (site.RouteId != routeTravelFixture.Find(site.RouteId)?.Id
                || site.RouteFingerprint != routeTravelFixture.Fingerprint
                || site.ProfileFingerprint != expeditionCampSiteProfile.Fingerprint
                || site.FootprintWidthFeet != 20 || site.FootprintHeightFeet != 20
                || !site.LegalAccess || !site.Stable || !site.Drainage || !site.WeatherProtection
                || !site.InhabitantSpace || !site.GearSpace)
                return "TemporaryCampConstructionSiteUnsuitable";
            var expected = new[] { TestOnlyExpeditionCampConstructionFixture.TentLotId,
                TestOnlyExpeditionCampConstructionFixture.PackLotId };
            foreach (string id in expected)
            {
                var lot = s.Work.Lots.SingleOrDefault(x => x.Id == id);
                var provenance = s.InventoryLots.SingleOrDefault(x => x.LotId == id);
                var item = s.PortableEquipment.SingleOrDefault(x => x.Id == id);
                bool installed = s.TemporaryCampInstallations.Any(x => x.LotId == id);
                bool activelyClaimed = s.Work.Reservations.Any(x => x.LotId == id && x.RemainingAmount != default);
                bool mayMoveUnclaimed = !activelyClaimed && !installed;
                bool atAuthoredSite = lot != null && item != null
                    && lot.LocationId == GroundSiteLocation(site.RouteX, site.RouteY)
                    && lot.CustodianId == profile.LeadId
                    && item.Placement == PortablePlacement.Ground
                    && item.GroundX == site.RouteX && item.GroundY == site.RouteY
                    && item.CustodianId == profile.LeadId;
                string expectedLocation = item == null ? "" : item.ParentId != "" ? item.ParentId
                    : item.Placement == PortablePlacement.Ground ? PortableEquipmentValidation.GroundLocation(item)
                    : item.CustodianId;
                string expectedProfile = id == TestOnlyExpeditionCampConstructionFixture.TentLotId
                    ? TestOnlyExpeditionCampConstructionFixture.TentProfileId
                    : TestOnlyExpeditionCampConstructionFixture.PackProfileId;
                if (lot == null || lot.UnitId != "mass-pound" || lot.Amount != new RuleQuantity(20)
                    || provenance == null || provenance.ParentId != "" || provenance.OwnerId != profile.LeadId
                    || provenance.CreatedAmount != new RuleQuantity(20) || provenance.Nutrition != NutritionKind.None
                    || !(atAuthoredSite || mayMoveUnclaimed)
                    || lot.LocationId != expectedLocation || item == null || lot.CustodianId != item.CustodianId
                    || item == null || item.LinkKind != PortableLinkKind.InventoryLot || item.LinkedId != id
                    || item.ProfileId != expectedProfile || item.OwnerId != profile.LeadId
                    || item.MassBasis != PortableMassBasis.GenericPounds || item.SourceWeightLb != new RuleQuantity(20)
                    || item.OperationalWeightLb.HasValue) return "TemporaryCampFixtureLotMismatch";
            }
            var fittingPack = s.PortableEquipment.Single(x => x.Id == TestOnlyExpeditionCampConstructionFixture.PackLotId);
            if (fittingPack.CapacityPounds != new RuleQuantity(200) || fittingPack.CapacityCubicFeet != new RuleQuantity(20))
                return "TemporaryCampFittingPackCapacityMismatch";
            if (s.TemporaryCampConstructionAttempts.Any(x => x.SiteId != site.Id || x.RouteId != site.RouteId
                || x.RouteTier != profile.RouteTier || x.ProfileFingerprint != profile.Fingerprint
                || x.LeadId != profile.LeadId || x.SkillId != TestOnlyExpeditionCampConstructionFixture.SkillId
                || x.Ability != profile.Ability || x.TentLotId != TestOnlyExpeditionCampConstructionFixture.TentLotId
                || x.PackLotId != TestOnlyExpeditionCampConstructionFixture.PackLotId
                || !x.AssistantIds.SequenceEqual(profile.AssistantIds, StringComparer.Ordinal)
                || x.WorkRequired != new RuleTime(TestOnlyExpeditionCampConstructionFixture.RequiredWorkSeconds)))
                return "TemporaryCampConstructionAttemptProfileMismatch";
            foreach (var attempt in s.TemporaryCampConstructionAttempts.Where(x => x.Check != null))
            {
                string error = ValidateTemporaryCampConstructionCheck(s, attempt);
                if (error != null) return error;
            }
            foreach (var attempt in s.TemporaryCampConstructionAttempts.Where(x => x.Status == TemporaryCampConstructionStatus.Working))
            {
                var crew = new[] { attempt.LeadId }.Concat(attempt.AssistantIds).ToArray();
                RuleTime end = CampGreens.Add(s.RuleClock, CampGreens.Subtract(attempt.WorkRequired, attempt.WorkDone));
                if (crew.Any(id => !s.Work.WorkerIntervals.Any(w => w.JobId == attempt.Id && w.WorkerId == id
                    && w.Start <= s.RuleClock && w.End == end))) return "TemporaryCampConstructionWorkerBookingsMismatch";
            }
            return null;
        }

        private string ValidateTemporaryCampConstructionCheck(Snapshot s, TemporaryCampConstructionAttemptRecord attempt)
        {
            var check = attempt.Check;
            var receipt = s.Receipts.SingleOrDefault(x => x.Id == check.CommandId);
            if (receipt == null || receipt.Revision != check.AppliedRevision
                || check.AssistantBonus != attempt.AssistantIds.Count || check.Dc != TemporaryCampConstructionValidation.TierDc(attempt.RouteTier))
                return "TemporaryCampConstructionCheckBindingMismatch";
            if (check.LinkedInjuriesAtCheck.Any(x => !Enum.IsDefined(typeof(Injury), x)))
                return "TemporaryCampConstructionInjuryEvidenceInvalid";
            var journal = s.Conditions.SingleOrDefault(x => x.Target == attempt.LeadId);
            if (journal == null || check.ConditionOperationCount > journal.Operations.Count) return "TemporaryCampConstructionConditionsMissing";
            var historical = new ConditionJournal(journal.PolicyId, journal.Target, journal.Origin,
                journal.Operations.Take(check.ConditionOperationCount));
            var conditionLedger = ConditionHistory.Restore(historical).Ledger;
            if (conditionLedger.Now.CompareTo(new EffectClockMarker(check.At)) < 0)
                conditionLedger = conditionLedger.AdvanceTo(new EffectClockMarker(check.At)).State;
            bool disadvantage = conditionLedger.View().Has(ConditionKind.Poisoned)
                || ExpeditionStrainRules.Project(s, attempt.LeadId, check.At, check.AppliedRevision).ExpeditionCheckDisadvantage;
            var facts = CharacterStateFacts.ForActor(s, attempt.LeadId, attempt.SkillId);
            var character = CharacterAdvancementRules.AtRevision(s, attempt.LeadId, check.AppliedRevision - 1);
            var modifier = AbilityCheckRules.Derive(character, facts.Training, attempt.Ability);
            int injury = PlaytestLife.AbilityCheckInjuryPenalty(new LifeState(1, 1,
                wounds: check.LinkedInjuriesAtCheck.Select(x => (Injury)x)), (int)attempt.Ability);
            int strain = ExpeditionStrainRules.Project(s, attempt.LeadId, check.At, check.AppliedRevision).ExpeditionCheckModifier;
            var roll = RuleDice.RollD20(check.RandomBefore, disadvantageSources: disadvantage ? 1 : 0);
            var outcome = RuleResolution.TaskCheck(check.Natural, check.LeadModifier + check.AssistantBonus, check.Dc);
            var result = outcome.Degree == RuleTaskDegree.CriticalFailure ? TemporaryCampConstructionResult.CriticalFailure
                : outcome.Degree == RuleTaskDegree.Failure ? TemporaryCampConstructionResult.Failure
                : outcome.Degree == RuleTaskDegree.Success ? TemporaryCampConstructionResult.Success
                : TemporaryCampConstructionResult.CriticalSuccess;
            return modifier.Total + injury + strain != check.LeadModifier || injury != check.InjuryPenalty
                || strain != check.StrainModifier || modifier.ProficiencyRank != check.ProficiencyRank
                || modifier.ProficiencyBonus != check.ProficiencyBonus || disadvantage != check.Disadvantage
                || outcome.Total != check.Total || result != check.Result || roll.First != check.FirstRoll
                || roll.Second.GetValueOrDefault() != check.SecondRoll || roll.Natural != check.Natural
                || roll.NextRandomState != check.RandomAfter || roll.WordsConsumed != check.WordsConsumed
                ? "TemporaryCampConstructionCheckReplayMismatch" : null;
        }

        private static bool IsTemporaryCampConstructionCommand(CommandKind kind)
            => kind == CommandKind.StartTemporaryCampConstruction || kind == CommandKind.PauseTemporaryCampConstruction
                || kind == CommandKind.ResumeTemporaryCampConstruction || kind == CommandKind.ResolveTemporaryCampConstruction;

        private string AssessTemporaryCampConstruction(Snapshot s, Command c,
            out TemporaryCampConstructionAttemptRecord attempt)
        {
            attempt = null;
            if (expeditionCampConstructionProfile == null
                || s.SchemaVersion != Snapshot.TemporaryCampConstructionSchema
                    && !(portableStorageFixture != null && s.SchemaVersion == Snapshot.PortableStorageSchema)
                    && !(recipe347Fixture != null && s.SchemaVersion == Snapshot.Recipe347Schema))
                return "TemporaryCampConstructionNotSelected";
            if (c.Inventory != null || c.Combat != null || c.Advancement != null || c.Ranged != null
                || c.SuppressionFire != null || c.DefensiveFormation != null || c.ExpeditionAssignment != null
                || c.HarvestSelection != null || c.MiningSelection != null || c.ProspectingExposure != null
                || c.RouteMappingWork != null || c.OverwatchRider != OverwatchRider.None || c.X != 0 || c.Y != 0
                || c.Target == "") return "InvalidTemporaryCampConstructionCommand";
            var profile = expeditionCampConstructionProfile;
            if (c.Actor != profile.LeadId) return "TemporaryCampConstructionLeadRequired";
            if (c.Kind == CommandKind.StartTemporaryCampConstruction)
            {
                if (c.Target != expeditionCampSiteProfile.Id || s.TemporaryCampConstructionAttempts.Length >= TemporaryCampConstructionValidation.MaxAttempts)
                    return c.Target != expeditionCampSiteProfile.Id ? "UnknownTemporaryCampSite" : "TemporaryCampConstructionHistoryFull";
                if (TemporaryCampConstructionValidation.HasTemporaryCamp(s, c.Target)) return "TemporaryCampAlreadyInstalled";
                if (s.TemporaryCampConstructionAttempts.Any(x => x.Status != TemporaryCampConstructionStatus.Resolved))
                    return "TemporaryCampConstructionAlreadyOpen";
                var site = s.ExpeditionCampSites.SingleOrDefault(x => x.Id == c.Target);
                if (site == null || !site.SupportsUse || !site.LegalAccess || !site.Stable || !site.Drainage
                    || !site.WeatherProtection || !site.InhabitantSpace || !site.GearSpace
                    || site.FootprintWidthFeet != 20 || site.FootprintHeightFeet != 20)
                    return "TemporaryCampSiteUnsuitable";
                string checkpoint = CampCheckpointFailure(s, site);
                if (checkpoint != null) return checkpoint;
                foreach (string actorId in new[] { profile.LeadId }.Concat(profile.AssistantIds))
                {
                    string workerFailure = TemporaryCampConstructionWorkerFailure(s, actorId, null);
                    if (workerFailure != null) return workerFailure;
                    if (!CharacterSkillTrainingFacts.IsTrained(s, actorId, TestOnlyExpeditionCampConstructionFixture.SkillId))
                        return actorId == profile.LeadId ? "TemporaryCampLeadNeedsSurvivalTraining" : "TemporaryCampAssistantNeedsSurvivalTraining";
                }
                if (s.ExpeditionCampActivities.Any(x => x.Active && x.Kind == ExpeditionCampActivityKind.LyingLow
                    && x.CohortId == site.CohortId)) return "TemporaryCampConstructionConflictsWithLyingLow";
                RuleTime end = CampGreens.Add(s.RuleClock, new RuleTime(TestOnlyExpeditionCampConstructionFixture.RequiredWorkSeconds));
                foreach (string actorId in new[] { profile.LeadId }.Concat(profile.AssistantIds))
                    if (s.Work.WorkerIntervals.Any(x => x.WorkerId == actorId && x.Start < end && x.End > s.RuleClock))
                        return "TemporaryCampConstructionWorkerBusy";
                foreach (var id in new[] { TestOnlyExpeditionCampConstructionFixture.TentLotId,
                    TestOnlyExpeditionCampConstructionFixture.PackLotId })
                {
                    var lot = s.Work.Lots.SingleOrDefault(x => x.Id == id);
                    if (lot == null || lot.UnitId != "mass-pound" || lot.Amount != new RuleQuantity(20)
                        || lot.LocationId != GroundSiteLocation(site.RouteX, site.RouteY)
                        || lot.CustodianId != profile.LeadId || s.Work.AvailableAmount(id) != new RuleQuantity(20))
                        return "TemporaryCampFixtureUnavailable";
                }
                return null;
            }
            attempt = s.TemporaryCampConstructionAttempts.SingleOrDefault(x => x.Id == c.Target && x.LeadId == c.Actor);
            if (attempt == null) return "UnknownTemporaryCampConstruction";
            var currentAttempt = attempt;
            if (c.Kind == CommandKind.PauseTemporaryCampConstruction)
                return currentAttempt.Status == TemporaryCampConstructionStatus.Working ? null : "TemporaryCampConstructionNotWorking";
            if (c.Kind == CommandKind.ResumeTemporaryCampConstruction)
            {
                if (currentAttempt.Status != TemporaryCampConstructionStatus.Paused) return "TemporaryCampConstructionNotPaused";
                var site = s.ExpeditionCampSites.Single(x => x.Id == currentAttempt.SiteId);
                string checkpoint = CampCheckpointFailure(s, site);
                if (checkpoint != null) return checkpoint;
                foreach (string actorId in new[] { currentAttempt.LeadId }.Concat(currentAttempt.AssistantIds))
                {
                    string workerFailure = TemporaryCampConstructionWorkerFailure(s, actorId, currentAttempt);
                    if (workerFailure != null) return workerFailure;
                    if (!CharacterSkillTrainingFacts.IsTrained(s, actorId, currentAttempt.SkillId)) return "TemporaryCampCrewQualificationChanged";
                }
                if (s.ExpeditionCampActivities.Any(x => x.Active && x.Kind == ExpeditionCampActivityKind.LyingLow
                    && x.CohortId == site.CohortId)) return "TemporaryCampConstructionConflictsWithLyingLow";
                RuleTime end = CampGreens.Add(s.RuleClock, CampGreens.Subtract(currentAttempt.WorkRequired, currentAttempt.WorkDone));
                foreach (string actorId in new[] { currentAttempt.LeadId }.Concat(currentAttempt.AssistantIds))
                    if (s.Work.WorkerIntervals.Any(x => x.WorkerId == actorId && x.JobId != currentAttempt.Id
                        && x.Start < end && x.End > s.RuleClock)) return "TemporaryCampConstructionWorkerBusy";
                foreach (string id in new[] { currentAttempt.TentLotId, currentAttempt.PackLotId })
                    if (s.Work.AvailableAmount(id) != default(RuleQuantity)) return "TemporaryCampFixtureClaimMissing";
                return null;
            }
            if (c.Kind == CommandKind.ResolveTemporaryCampConstruction)
            {
                if (currentAttempt.Status != TemporaryCampConstructionStatus.AwaitingCheck) return "TemporaryCampConstructionCheckNotReady";
                var site = s.ExpeditionCampSites.Single(x => x.Id == currentAttempt.SiteId);
                string checkpoint = CampCheckpointFailure(s, site);
                if (checkpoint != null) return checkpoint;
                if (!CapableWorker(s, currentAttempt.LeadId)) return "TemporaryCampLeadIncapable";
                return CharacterSkillTrainingFacts.IsTrained(s, currentAttempt.LeadId, currentAttempt.SkillId)
                    ? null : "TemporaryCampLeadNeedsSurvivalTraining";
            }
            return "InvalidTemporaryCampConstructionCommand";
        }

        private string TemporaryCampConstructionWorkerFailure(Snapshot s, string actorId,
            TemporaryCampConstructionAttemptRecord current)
        {
            if (s.InventoryCombat) return "TemporaryCampConstructionDuringTacticalControl";
            if (!CapableWorker(s, actorId)) return "TemporaryCampConstructionWorkerIncapable";
            if (s.WorldTraversals.Any(x => x.ActorId == actorId)) return "TemporaryCampConstructionWorkerTraversing";
            var site = s.ExpeditionCampSites.SingleOrDefault(x => x.Id == expeditionCampSiteProfile.Id);
            if (site == null) return "TemporaryCampConstructionSiteMissing";
            var actor = s.Actors.Single(x => x.Id == actorId);
            var position = WorldPositionResolver.Position(s, actorId);
            long distance = WorldSpatialQueries.CardinalDistance(actor.X, actor.Y, site.RouteX, site.RouteY);
            if (actorId == expeditionCampConstructionProfile.LeadId)
            {
                string checkpoint = CampCheckpointFailure(s, site);
                if (checkpoint != null) return checkpoint;
            }
            else if (distance > 1 || position.X != new RuleQuantity(actor.X)
                || position.Y != new RuleQuantity(actor.Y))
                return "TemporaryCampConstructionWorkerNotAtSite";
            if (s.Work.WorkerIntervals.Any(x => x.WorkerId == actorId && x.JobId != current?.Id
                && x.Start <= s.RuleClock && x.End > s.RuleClock)
                || WorldActivityProjection.CurrentWork(s).Any(x => x.ActorId == actorId && x.Id != current?.Id))
                return "TemporaryCampConstructionWorkerBusy";
            if (s.RestIntervals.Any(x => x.ActorId == actorId && x.Status == RestIntervalStatus.Active
                && x.StartedAt <= s.RuleClock && x.ScheduledEnd > s.RuleClock))
                return "TemporaryCampConstructionConflictsWithRest";
            return null;
        }

        private static void PutTemporaryCampConstruction(Snapshot s, TemporaryCampConstructionAttemptRecord attempt)
            => s.TemporaryCampConstructionAttempts = s.TemporaryCampConstructionAttempts.Select(x => x.Id == attempt.Id ? attempt : x).ToArray();

        private void BookTemporaryCampConstruction(Snapshot s, TemporaryCampConstructionAttemptRecord attempt)
        {
            RuleTime remaining = CampGreens.Subtract(attempt.WorkRequired, attempt.WorkDone);
            RuleTime end = CampGreens.Add(s.RuleClock, remaining);
            string[] workers = new[] { attempt.LeadId }.Concat(attempt.AssistantIds).ToArray();
            string stamp = (s.Revision + 1).ToString(CultureInfo.InvariantCulture);
            var intervals = workers.Select(id => new WorkerInterval(attempt.Id + ".labor." + id + "." + stamp,
                attempt.Id, id, s.RuleClock, end)).ToArray();
            var materials = attempt.WorkDone == default(RuleTime) && attempt.StartedAt == s.RuleClock
                && !s.Work.Reservations.Any(x => x.JobId == attempt.Id)
                ? new[] {
                    new ResourceReservation(attempt.Id + ".claim.tent", attempt.Id, attempt.TentLotId, new RuleQuantity(20)),
                    new ResourceReservation(attempt.Id + ".claim.pack", attempt.Id, attempt.PackLotId, new RuleQuantity(20))
                } : Array.Empty<ResourceReservation>();
            s.Work = s.Work.Reserve(attempt.Id, intervals, materials);
        }

        private static void PauseTemporaryCampConstruction(Snapshot s, TemporaryCampConstructionAttemptRecord attempt)
        {
            s.Work = s.Work.CancelFutureWork(attempt.Id, s.RuleClock);
            PutTemporaryCampConstruction(s, attempt.WithProgress(s.RuleClock, attempt.WorkDone,
                TemporaryCampConstructionStatus.Paused));
        }

        private static void PauseTemporaryCampConstructionForActor(Snapshot s, string actorId)
        {
            foreach (var attempt in s.TemporaryCampConstructionAttempts.Where(x => x.Status == TemporaryCampConstructionStatus.Working
                && (x.LeadId == actorId || x.AssistantIds.Contains(actorId, StringComparer.Ordinal))).ToArray())
                PauseTemporaryCampConstruction(s, attempt);
        }

        private void PauseIncompatibleTemporaryCampConstruction(Snapshot s)
        {
            if (expeditionCampConstructionProfile == null) return;
            foreach (var attempt in s.TemporaryCampConstructionAttempts.Where(x => x.Status == TemporaryCampConstructionStatus.Working).ToArray())
                if (s.InventoryCombat || new[] { attempt.LeadId }.Concat(attempt.AssistantIds)
                    .Any(id => TemporaryCampConstructionWorkerFailure(s, id, attempt) != null))
                    PauseTemporaryCampConstruction(s, attempt);
        }

        private RuleTime? NextTemporaryCampConstructionBoundary(Snapshot s)
        {
            if (expeditionCampConstructionProfile == null) return null;
            var ends = s.TemporaryCampConstructionAttempts.Where(x => x.Status == TemporaryCampConstructionStatus.Working)
                .SelectMany(x => s.Work.WorkerIntervals.Where(w => w.JobId == x.Id && w.Start <= s.RuleClock && w.End > s.RuleClock)
                    .Select(w => w.End)).ToArray();
            return ends.Length == 0 ? (RuleTime?)null : ends.Min();
        }

        private void CreditTemporaryCampConstruction(Snapshot s, RuleTime elapsed,
            System.Collections.Generic.ICollection<string> ready)
        {
            if (expeditionCampConstructionProfile == null || elapsed == default(RuleTime)) return;
            RuleTime end = s.RuleClock; RuleTime start = CampGreens.Subtract(end, elapsed);
            foreach (var attempt in s.TemporaryCampConstructionAttempts.Where(x => x.Status == TemporaryCampConstructionStatus.Working).ToArray())
            {
                var crew = new[] { attempt.LeadId }.Concat(attempt.AssistantIds).ToArray();
                bool covered = crew.All(id => s.Work.WorkerIntervals.Any(w => w.JobId == attempt.Id && w.WorkerId == id
                    && w.Start <= start && w.End >= end));
                if (!covered) continue;
                RuleTime done = CampGreens.Add(attempt.WorkDone, elapsed);
                if (done > attempt.WorkRequired) done = attempt.WorkRequired;
                if (done == attempt.WorkRequired)
                {
                    PutTemporaryCampConstruction(s, attempt.WithProgress(end, done, TemporaryCampConstructionStatus.AwaitingCheck));
                    ready.Add(attempt.Id);
                }
                else PutTemporaryCampConstruction(s, attempt.WithProgress(end, done, TemporaryCampConstructionStatus.Working));
            }
        }

        private void ResolveReadyTemporaryCampChecks(Snapshot s, System.Collections.Generic.IEnumerable<string> ids,
            Command initiating)
        {
            if (initiating == null || ids == null) return;
            foreach (string id in ids.Distinct(StringComparer.Ordinal))
            {
                var attempt = s.TemporaryCampConstructionAttempts.SingleOrDefault(x => x.Id == id
                    && x.Status == TemporaryCampConstructionStatus.AwaitingCheck);
                if (attempt == null || !CapableWorker(s, attempt.LeadId)) continue;
                ResolveTemporaryCampConstructionCheck(s, attempt, initiating.Id, s.Revision + 1);
            }
        }

        private void ResolveTemporaryCampConstructionCheck(Snapshot s,
            TemporaryCampConstructionAttemptRecord attempt, string commandId, long appliedRevision)
        {
            var facts = CharacterStateFacts.ForActor(s, attempt.LeadId, attempt.SkillId);
            var character = CharacterAdvancementRules.AtRevision(s, attempt.LeadId, appliedRevision - 1);
            var modifier = AbilityCheckRules.Derive(character, facts.Training, attempt.Ability);
            int injury = PlaytestLife.AbilityCheckInjuryPenalty(ActorLifeRules.Read(facts.Life), (int)attempt.Ability);
            int strain = ExpeditionStrainRules.Project(s, attempt.LeadId, s.RuleClock, appliedRevision).ExpeditionCheckModifier;
            int leadModifier = checked(modifier.Total + injury + strain);
            int conditionOperations = s.Conditions.Single(x => x.Target == attempt.LeadId).Operations.Count;
            var journal = s.Conditions.Single(x => x.Target == attempt.LeadId);
            var historical = new ConditionJournal(journal.PolicyId, journal.Target, journal.Origin,
                journal.Operations.Take(conditionOperations));
            var conditionLedger = ConditionHistory.Restore(historical).Ledger;
            if (conditionLedger.Now.CompareTo(new EffectClockMarker(s.RuleClock)) < 0)
                conditionLedger = conditionLedger.AdvanceTo(new EffectClockMarker(s.RuleClock)).State;
            bool disadvantage = conditionLedger.View().Has(ConditionKind.Poisoned)
                || ExpeditionStrainRules.Project(s, attempt.LeadId, s.RuleClock, appliedRevision).ExpeditionCheckDisadvantage;
            uint before = s.RandomState;
            RuleD20Roll roll = RuleDice.RollD20(before, disadvantageSources: disadvantage ? 1 : 0);
            int assistantBonus = attempt.AssistantIds.Count;
            var outcome = RuleResolution.TaskCheck(roll.Natural, checked(leadModifier + assistantBonus),
                TemporaryCampConstructionValidation.TierDc(attempt.RouteTier));
            var result = outcome.Degree == RuleTaskDegree.CriticalFailure ? TemporaryCampConstructionResult.CriticalFailure
                : outcome.Degree == RuleTaskDegree.Failure ? TemporaryCampConstructionResult.Failure
                : outcome.Degree == RuleTaskDegree.Success ? TemporaryCampConstructionResult.Success
                : TemporaryCampConstructionResult.CriticalSuccess;
            int[] injuries = facts.Life.LinkedInjuries.ToArray();
            var check = new TemporaryCampConstructionCheckRecord(commandId, appliedRevision, s.RuleClock,
                leadModifier, modifier.ProficiencyRank, modifier.ProficiencyBonus, injury, strain, assistantBonus,
                TemporaryCampConstructionValidation.TierDc(attempt.RouteTier), conditionOperations, disadvantage,
                injuries, roll.First, roll.Second.GetValueOrDefault(), roll.Natural, checked((int)outcome.Total),
                result, before, roll.NextRandomState, checked((int)roll.WordsConsumed));
            s.RandomState = roll.NextRandomState;
            var resolved = attempt.WithCheck(check);
            PutTemporaryCampConstruction(s, resolved);
            if (result >= TemporaryCampConstructionResult.Success)
            {
                s.TemporaryCampInstallations = s.TemporaryCampInstallations.Concat(new[] {
                    new TemporaryCampInstallationRecord(resolved.Id + ".install.tent", resolved.Id, resolved.SiteId,
                        resolved.TentLotId, TemporaryCampFixtureKind.TwoPersonTent, s.RuleClock, appliedRevision),
                    new TemporaryCampInstallationRecord(resolved.Id + ".install.pack", resolved.Id, resolved.SiteId,
                        resolved.PackLotId, TemporaryCampFixtureKind.FittingPack, s.RuleClock, appliedRevision)
                }).ToArray();
            }
            else
            {
                foreach (var claim in s.Work.Reservations.Where(x => x.JobId == resolved.Id && x.RemainingAmount != default).ToArray())
                    s.Work = s.Work.Release(resolved.Id, claim.Id);
            }
        }

        private string ResolveTemporaryCampConstruction(Snapshot s, Command c)
        {
            string error = AssessTemporaryCampConstruction(s, c, out var attempt);
            if (error != null) return error;
            if (c.Kind == CommandKind.StartTemporaryCampConstruction)
            {
                var profile = expeditionCampConstructionProfile;
                string id = "camp-build." + (s.Revision + 1).ToString(CultureInfo.InvariantCulture);
                var created = new TemporaryCampConstructionAttemptRecord(id, expeditionCampSiteProfile.Id,
                    expeditionCampSiteProfile.RouteId, profile.RouteTier, profile.Fingerprint, profile.LeadId,
                    TestOnlyExpeditionCampConstructionFixture.SkillId, profile.Ability,
                    TestOnlyExpeditionCampConstructionFixture.TentLotId,
                    TestOnlyExpeditionCampConstructionFixture.PackLotId, profile.AssistantIds, s.Revision + 1,
                    s.RuleClock, s.RuleClock, new RuleTime(TestOnlyExpeditionCampConstructionFixture.RequiredWorkSeconds),
                    default, TemporaryCampConstructionStatus.Working);
                BookTemporaryCampConstruction(s, created);
                s.TemporaryCampConstructionAttempts = s.TemporaryCampConstructionAttempts.Concat(new[] { created }).ToArray();
                return null;
            }
            if (c.Kind == CommandKind.PauseTemporaryCampConstruction)
                PauseTemporaryCampConstruction(s, attempt);
            else if (c.Kind == CommandKind.ResumeTemporaryCampConstruction)
            {
                var resumed = attempt.WithProgress(s.RuleClock, attempt.WorkDone, TemporaryCampConstructionStatus.Working);
                BookTemporaryCampConstruction(s, resumed);
                PutTemporaryCampConstruction(s, resumed);
            }
            else ResolveTemporaryCampConstructionCheck(s, attempt, c.Id, s.Revision + 1);
            return null;
        }

        private CommandQueryResult QueryTemporaryCampConstruction(Snapshot s, Command c)
        {
            string error = AssessTemporaryCampConstruction(s.Copy(), c, out var attempt);
            RuleTime remaining = error == null && attempt != null
                ? CampGreens.Subtract(attempt.WorkRequired, attempt.WorkDone) : default;
            long cost = error != null || c.Kind == CommandKind.PauseTemporaryCampConstruction
                || c.Kind == CommandKind.ResolveTemporaryCampConstruction ? 0
                : c.Kind == CommandKind.StartTemporaryCampConstruction ? TestOnlyExpeditionCampConstructionFixture.RequiredWorkSeconds
                : remaining.Denominator == 1 ? remaining.Numerator : 0;
            var costs = error == null && cost > 0
                ? new[] { new CommandCost("active-work-seconds", c.Target, cost) }
                : Array.Empty<CommandCost>();
            return new CommandQueryResult(true, error == null, error ?? "Available", s.Revision, costs);
        }

        private System.Collections.Generic.IEnumerable<Command> DiscoverTemporaryCampConstructionCommands(Snapshot s, string actor)
        {
            var profile = expeditionCampConstructionProfile;
            if (profile == null || actor != profile.LeadId || s.InventoryCombat) yield break;
            var active = s.TemporaryCampConstructionAttempts.SingleOrDefault(x => x.Status != TemporaryCampConstructionStatus.Resolved);
            string prefix = "option." + s.Revision.ToString(CultureInfo.InvariantCulture) + ".camp-build.";
            if (active == null)
                yield return new Command(prefix + "start", actor, s.Revision, CommandKind.StartTemporaryCampConstruction,
                    expeditionCampSiteProfile.Id);
            else if (active.Status == TemporaryCampConstructionStatus.Working)
                yield return new Command(prefix + "pause", actor, s.Revision, CommandKind.PauseTemporaryCampConstruction, active.Id);
            else if (active.Status == TemporaryCampConstructionStatus.Paused)
                yield return new Command(prefix + "resume", actor, s.Revision, CommandKind.ResumeTemporaryCampConstruction, active.Id);
            else if (active.Status == TemporaryCampConstructionStatus.AwaitingCheck)
                yield return new Command(prefix + "resolve", actor, s.Revision, CommandKind.ResolveTemporaryCampConstruction, active.Id);
        }
    }
}
#endif
