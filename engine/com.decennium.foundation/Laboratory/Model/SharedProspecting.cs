#if DECENNIUM_TEST_ONLY && (UNITY_EDITOR || DEVELOPMENT_BUILD || HEADLESS_TESTS)
using System;
using System.Globalization;
using System.Linq;
using System.Security.Cryptography;
using System.Text;

namespace Decennium.Foundation.Laboratory
{
    /// <summary>TEST_ONLY authored patch and all content versions that a trusted world event may expose.</summary>
    public sealed class ProspectingPatchFixtureContent
    {
        private readonly ProspectingExposureProfile[] exposures;
        private readonly ProspectingObservationProfile[] observations;
        private readonly PortableEquipmentRecord[] implements;
        public ProspectingPatchRecord Patch { get; }
        public string InitialExposureId { get; }
        public ProspectingExposureProfile[] Exposures => exposures.ToArray();
        public ProspectingObservationProfile[] Observations => observations.ToArray();
        public PortableEquipmentRecord[] Implements => implements.ToArray();

        public ProspectingPatchFixtureContent(ProspectingPatchRecord patch, string initialExposureId,
            ProspectingExposureProfile[] exposures, ProspectingObservationProfile[] observations,
            PortableEquipmentRecord[] implements = null)
        {
            if (patch == null || !Validation.ValidId(initialExposureId) || exposures == null || exposures.Length < 1
                || observations == null || exposures.Any(x => x == null) || observations.Any(x => x == null))
                throw new ArgumentException("Invalid prospecting patch content.");
            var items = implements ?? Array.Empty<PortableEquipmentRecord>();
            if (items.Any(x => x == null) || exposures.Any(x => x.PatchId != patch.Id)
                || exposures.Select(x => x.Id).Distinct(StringComparer.Ordinal).Count() != exposures.Length
                || observations.Select(x => x.Id).Distinct(StringComparer.Ordinal).Count() != observations.Length
                || items.Select(x => x.Id).Distinct(StringComparer.Ordinal).Count() != items.Length
                || !exposures.Any(x => x.Id == initialExposureId)
                || exposures.SelectMany(x => x.RequiredImplementIds).Any(id => !items.Any(x => x.Id == id))
                || exposures.SelectMany(x => x.FindingIds).Any(id => !observations.Any(x => x.Id == id)))
                throw new ArgumentException("Prospecting content references do not resolve.");
            Patch = patch; InitialExposureId = initialExposureId;
            this.exposures = exposures.OrderBy(x => x.Id, StringComparer.Ordinal).ToArray();
            this.observations = observations.OrderBy(x => x.Id, StringComparer.Ordinal).ToArray();
            this.implements = items.OrderBy(x => x.Id, StringComparer.Ordinal).ToArray();
        }

        internal string Key => Patch.Id + "|" + Patch.OwnerId + "|" + Patch.SiteId + "|" + Patch.X + "," + Patch.Y + "|"
            + InitialExposureId + "|" + string.Join("||", exposures.Select(ExposureKey)) + "|"
            + string.Join("||", observations.Select(ObservationKey)) + "|" + string.Join("||", implements.Select(PortableItemKey));

        private static string ExposureKey(ProspectingExposureProfile x)
            => string.Join("|", new[]{x.Id,x.PatchId,x.AreaSquareFeet.ToString(CultureInfo.InvariantCulture),x.Exposed.ToString(),
                x.Accessible.ToString(),((int)x.Signs).ToString(CultureInfo.InvariantCulture),((int)x.Method).ToString(CultureInfo.InvariantCulture),
                x.RequiredHands.ToString(CultureInfo.InvariantCulture),x.HazardDeclarationId,string.Join(",",x.RequiredImplementIds),string.Join(",",x.FindingIds)});

        private static string ObservationKey(ProspectingObservationProfile x)
            => string.Join("|", new[]{x.Id,((int)x.Kind).ToString(CultureInfo.InvariantCulture),x.ObservableFact});

        private static string PortableItemKey(PortableEquipmentRecord x)
            => string.Join("|", new[]{x.Id,x.ProfileId,x.OwnerId,x.CustodianId,x.ParentId,x.LinkedId,x.FitRuleId,
                ((int)x.Placement).ToString(CultureInfo.InvariantCulture),((int)x.LinkKind).ToString(CultureInfo.InvariantCulture),
                ((int)x.MassBasis).ToString(CultureInfo.InvariantCulture),x.SourceWeightLb?.ToString()??"-",
                x.OperationalWeightLb?.ToString()??"-",x.PrintedLoad?.ToString()??"-",x.CapacityPounds?.ToString()??"-",
                x.CapacityCubicFeet?.ToString()??"-",x.Wearable.ToString(),x.Open.ToString(),x.GroundX.ToString(CultureInfo.InvariantCulture),
                x.GroundY.ToString(CultureInfo.InvariantCulture),x.HeldHands.ToString(CultureInfo.InvariantCulture),string.Join(",",x.FitMemberIds)});
    }

    public sealed class SharedProspectingFixture
    {
        private readonly ProspectingPatchFixtureContent[] patches;
        private readonly string[] workers;
        public bool Trained { get; }
        public int? Wisdom { get; }
        public ProspectingPatchFixtureContent[] Patches => patches.ToArray();
        public string[] Workers => workers.ToArray();
        internal string Key => "TEST_ONLY.prospecting-v1|" + Trained + "|" + (Wisdom?.ToString(CultureInfo.InvariantCulture) ?? "-")
            + "|" + string.Join("||", patches.Select(x => x.Key)) + "|" + string.Join(",", workers);

        public SharedProspectingFixture(ProspectingPatchFixtureContent[] patches, bool trained = true,
            string[] workers = null, int? wisdom = null)
        {
            if (patches == null || patches.Length < 1 || patches.Length > ProspectingValidation.MaxRecords || patches.Any(x => x == null)
                || patches.Select(x => x.Patch.Id).Distinct(StringComparer.Ordinal).Count() != patches.Length
                || patches.Select(x => x.Patch.X.ToString(CultureInfo.InvariantCulture) + "," + x.Patch.Y.ToString(CultureInfo.InvariantCulture))
                    .Distinct(StringComparer.Ordinal).Count() != patches.Length
                || patches.SelectMany(x => x.Exposures).Select(x => x.Id).Distinct(StringComparer.Ordinal).Count()
                    != patches.Sum(x => x.Exposures.Length)
                || patches.SelectMany(x => x.Observations).Select(x => x.Id).Distinct(StringComparer.Ordinal).Count()
                    != patches.Sum(x => x.Observations.Length)
                || patches.SelectMany(x => x.Implements).Select(x => x.Id).Distinct(StringComparer.Ordinal).Count()
                    != patches.Sum(x => x.Implements.Length)
                || wisdom.HasValue && (wisdom.Value < 1 || wisdom.Value > 30))
                throw new ArgumentException("Invalid authored prospecting fixture.", nameof(patches));
            var actorIds = workers ?? new[] { TestOnlyPolicy.CompanionId };
            if (actorIds.Length < 1 || actorIds.Any(x => !Validation.ValidId(x))
                || actorIds.Distinct(StringComparer.Ordinal).Count() != actorIds.Length)
                throw new ArgumentException("Invalid prospecting workers.", nameof(workers));
            this.patches = patches.OrderBy(x => x.Patch.Id, StringComparer.Ordinal).ToArray();
            this.workers = actorIds.OrderBy(x => x, StringComparer.Ordinal).ToArray();
            Trained = trained; Wisdom = wisdom;
        }

        public static ProspectingPatchFixtureContent Patch(string key, int x, int y, ProspectingSignSeverity signs,
            ProspectingObservationProfile[] observations, int areaSquareFeet = 100,
            ProspectingMethodKind method = ProspectingMethodKind.VisualInspection, int requiredHands = 0,
            string[] requiredImplementIds = null, PortableEquipmentRecord[] implements = null)
        {
            if (!Validation.ValidId(key) || x < 0 || y < 0) throw new ArgumentException("Invalid prospecting patch helper input.");
            string owner = TestOnlyPolicy.CompanionId;
            string patchId = "TEST_ONLY.prospecting." + key + ".patch";
            string exposureId = "TEST_ONLY.prospecting." + key + ".exposure.v1";
            var profile = new ProspectingExposureProfile(exposureId, patchId, areaSquareFeet, true, true, signs,
                method, requiredHands, "TEST_ONLY.prospecting.hazard.none", requiredImplementIds ?? Array.Empty<string>(),
                observations.Select(o => o.Id).ToArray());
            var patch = new ProspectingPatchRecord(patchId, owner, "TEST_ONLY.prospecting." + key + ".site", x, y, exposureId);
            return new ProspectingPatchFixtureContent(patch, exposureId, new[] { profile }, observations, implements);
        }
    }

    public sealed class ProspectingObservedFact
    {
        public string ActorId { get; }
        public string PatchId { get; }
        public string ExposureId { get; }
        public string FindingId { get; }
        public ProspectingObservationKind Kind { get; }
        public string ObservableFact { get; }
        public RuleTime LearnedAt { get; }
        internal ProspectingObservedFact(string actorId, string patchId, string exposureId,
            ProspectingObservationProfile profile, RuleTime learnedAt)
        { ActorId=actorId;PatchId=patchId;ExposureId=exposureId;FindingId=profile.Id;Kind=profile.Kind;ObservableFact=profile.ObservableFact;LearnedAt=learnedAt; }
    }

    public sealed partial class TestOnlySharedWorldPolicy
    {
        private SharedProspectingFixture prospectingFixture;

        public static TestOnlySharedWorldPolicy WithProspecting(SharedProspectingFixture fixture, uint seed = 1)
        {
            if (fixture == null) throw new ArgumentNullException(nameof(fixture));
            var policy = new TestOnlySharedWorldPolicy(new SharedCombatFixture(seed: seed), walkingSpeed: 30);
            policy.prospectingFixture = fixture;
            using (var sha = SHA256.Create())
                policy.ContentFingerprint = "TEST_ONLY.prospecting-v1-" + string.Concat(sha.ComputeHash(Encoding.UTF8.GetBytes(
                    policy.ContentFingerprint + "|" + fixture.Key + "|seed=" + seed.ToString(CultureInfo.InvariantCulture)))
                    .Select(x => x.ToString("x2", CultureInfo.InvariantCulture)));
            return policy;
        }

        private string[] ProspectingWorkerIds => prospectingFixture?.Workers ?? Array.Empty<string>();
        private bool IsProspectingWorker(string id) => ProspectingWorkerIds.Contains(id, StringComparer.Ordinal);

        private void InitializeProspecting(Snapshot s)
        {
            if (prospectingFixture == null) return;
            if (prospectingFixture.Wisdom.HasValue) {
                s.Characters = s.Characters.Select(x => {
                    if (!ProspectingWorkerIds.Contains(x.ActorId, StringComparer.Ordinal)) return x;
                    int[] abilities = x.Abilities.ToArray(); abilities[4] = prospectingFixture.Wisdom.Value;
                    return new ActorCharacterRecord(x.ActorId, x.ProfileId, abilities, x.Levels);
                }).ToArray();
            }
            if (prospectingFixture.Trained) s.SkillTraining = s.SkillTraining.Concat(ProspectingWorkerIds
                .Where(id => !s.SkillTraining.Any(x => x.ActorId == id && x.SkillId == "mining-tools"))
                .Select(id => new SkillTrainingRecord(id, "mining-tools", 1))).ToArray();
            var contents = prospectingFixture.Patches;
            s.ProspectingPatches = contents.Select(x => x.Patch).ToArray();
            s.ProspectingExposures = contents.SelectMany(x => x.Exposures.Where(e => e.Id == x.InitialExposureId)
                .Select(e => ProspectingExposureRecord.FromProfile(e, "", "authored.initial", s.RuleClock))).ToArray();
            s.PortableEquipment = s.PortableEquipment.Concat(contents.SelectMany(x => x.Implements)).ToArray();
        }

        public System.Collections.Generic.IReadOnlyList<ProspectingObservedFact> ObservationsFor(Snapshot snapshot, string actorId)
        {
            if (snapshot == null || !Validation.ValidId(actorId)) throw new ArgumentException("Invalid prospecting observation query.");
            if (prospectingFixture == null || snapshot.ContentFingerprint != ContentFingerprint) return Array.Empty<ProspectingObservedFact>();
            var known = snapshot.ProspectingAttempts.Where(x => x.ActorId == actorId
                    && (x.Status == ProspectingAttemptStatus.Success || x.Status == ProspectingAttemptStatus.CriticalSuccess))
                .SelectMany(x => x.FindingIds.Select(id => new { Attempt = x, Id = id })).ToArray();
            var observations = prospectingFixture.Patches.SelectMany(x => x.Observations).ToDictionary(x => x.Id, StringComparer.Ordinal);
            return Array.AsReadOnly(known.Select(x => new ProspectingObservedFact(actorId, x.Attempt.PatchId, x.Attempt.ExposureId,
                observations[x.Id], x.Attempt.ResolvedAt.Value)).ToArray());
        }

        private bool IsProspectingCommand(Command c) => prospectingFixture != null && (c.Kind == CommandKind.StartProspecting
            || c.Kind == CommandKind.PauseProspecting || c.Kind == CommandKind.ResumeProspecting
            || c.Kind == CommandKind.RecordProspectingExposure);

        private static void PutProspectingAttempt(Snapshot s, ProspectingAttemptRecord value)
            => s.ProspectingAttempts = s.ProspectingAttempts.Select(x => x.Id == value.Id ? value : x).ToArray();

        private static RuleTime AddProspectingTime(RuleTime a, RuleTime b)
            => RuleTime.FromFraction((System.Numerics.BigInteger)a.Numerator * b.Denominator
                + (System.Numerics.BigInteger)b.Numerator * a.Denominator, (System.Numerics.BigInteger)a.Denominator * b.Denominator);
        private static RuleTime SubtractProspectingTime(RuleTime a, RuleTime b)
            => RuleTime.FromFraction((System.Numerics.BigInteger)a.Numerator * b.Denominator
                - (System.Numerics.BigInteger)b.Numerator * a.Denominator, (System.Numerics.BigInteger)a.Denominator * b.Denominator);

        private ProspectingPatchFixtureContent ProspectingContent(string patchId)
            => prospectingFixture?.Patches.SingleOrDefault(x => x.Patch.Id == patchId);
        private ProspectingExposureProfile ProspectingProfile(string exposureId)
            => prospectingFixture?.Patches.SelectMany(x => x.Exposures).SingleOrDefault(x => x.Id == exposureId);
        private ProspectingObservationProfile ProspectingObservation(string id)
            => prospectingFixture?.Patches.SelectMany(x => x.Observations).SingleOrDefault(x => x.Id == id);

        private bool ProspectingExposureDiffers(ProspectingExposureRecord oldExposure, ProspectingExposureProfile next)
        {
            if (oldExposure.AreaSquareFeet != next.AreaSquareFeet || oldExposure.Exposed != next.Exposed
                || oldExposure.Accessible != next.Accessible || oldExposure.Signs != next.Signs || oldExposure.Method != next.Method
                || oldExposure.HazardDeclarationId != next.HazardDeclarationId)
                return true;
            // Identity changes alone do not authorize a retry. Compare the player-observable facts,
            // not profile IDs, so a rename cannot manufacture new evidence.
            string[] oldFacts = oldExposure.FindingIds.Select(id => ProspectingObservation(id)).Where(x => x != null)
                .Select(x => ((int)x.Kind).ToString(CultureInfo.InvariantCulture) + "|" + x.ObservableFact)
                .OrderBy(x => x, StringComparer.Ordinal).ToArray();
            string[] nextFacts = next.FindingIds.Select(id => ProspectingObservation(id)).Where(x => x != null)
                .Select(x => ((int)x.Kind).ToString(CultureInfo.InvariantCulture) + "|" + x.ObservableFact)
                .OrderBy(x => x, StringComparer.Ordinal).ToArray();
            if (!oldFacts.SequenceEqual(nextFacts)) return true;
            return false;
        }

        private string ValidateProspectingFixtureState(Snapshot s)
        {
            if (prospectingFixture == null)
                return s.ProspectingPatches.Length + s.ProspectingExposures.Length + s.ProspectingAttempts.Length == 0
                    ? null : "ProspectingFixtureNotSelected";
            var authored = prospectingFixture.Patches;
            if ((s.SchemaVersion != Snapshot.ProspectingSchema&&!(dodgeActionEnabled&&s.SchemaVersion==Snapshot.DodgeSchema)) || s.ProspectingPatches.Length != authored.Length
                || !s.ProspectingPatches.OrderBy(x=>x.Id,StringComparer.Ordinal).Zip(authored.OrderBy(x=>x.Patch.Id,StringComparer.Ordinal),
                    (a,b)=>a.Id==b.Patch.Id&&a.OwnerId==b.Patch.OwnerId&&a.SiteId==b.Patch.SiteId&&a.X==b.Patch.X&&a.Y==b.Patch.Y).All(x=>x)
                || s.PortableEquipment.Count(x=>authored.SelectMany(p=>p.Implements).Any(i=>i.Id==x.Id))!=authored.Sum(x=>x.Implements.Length)
                || s.ProspectingAttempts.Any(x=>!ProspectingWorkerIds.Contains(x.ActorId,StringComparer.Ordinal)))
                return "InvalidProspectingFixture";
            foreach(var content in authored) {
                if(!s.ProspectingExposures.Any(x=>x.Id==content.InitialExposureId&&x.PatchId==content.Patch.Id
                    &&x.ParentExposureId==""&&x.ChangeCauseId=="authored.initial"))return "InvalidProspectingInitialExposure";
                foreach(var exposure in s.ProspectingExposures.Where(x=>x.PatchId==content.Patch.Id)) {
                    var profile=content.Exposures.SingleOrDefault(x=>x.Id==exposure.Id);
                    if(profile==null||profile.AreaSquareFeet!=exposure.AreaSquareFeet||profile.Exposed!=exposure.Exposed
                        ||profile.Accessible!=exposure.Accessible||profile.Signs!=exposure.Signs||profile.Method!=exposure.Method
                        ||profile.RequiredHands!=exposure.RequiredHands||profile.HazardDeclarationId!=exposure.HazardDeclarationId
                        ||!profile.RequiredImplementIds.SequenceEqual(exposure.RequiredImplementIds)
                        ||!profile.FindingIds.SequenceEqual(exposure.FindingIds))return "InvalidProspectingExposureContent";
                }
            }
            int expectedSkillCount=prospectingFixture.Trained?ProspectingWorkerIds.Length:0;
            var skillRecords=s.SkillTraining.Where(x=>x.SkillId=="mining-tools").ToArray();
            if(skillRecords.Length!=expectedSkillCount||skillRecords.Any(x=>!ProspectingWorkerIds.Contains(x.ActorId,StringComparer.Ordinal)||x.ProficiencyRank!=1))
                return "InvalidProspectingSkillProfile";
            return null;
        }

        private bool ProspectingAccess(Snapshot s, string actorId, ProspectingPatchRecord patch,
            ProspectingExposureRecord exposure, string exceptJob = "")
        {
            if (prospectingFixture == null) return false;
            if (!exposure.Exposed || !exposure.Accessible) return false;
            if (s.InventoryCombat && s.WorldSchedule.Order.Contains(actorId)) return false;
            if (!IsProspectingWorker(actorId) || !CapableWorker(s, actorId) || s.WorldTraversals.Any(x => x.ActorId == actorId)) return false;
            if (s.Work.WorkerIntervals.Any(x => x.WorkerId == actorId && x.JobId != exceptJob && x.Start <= s.RuleClock && x.End > s.RuleClock)
                || WorldActivityProjection.CurrentWork(s).Any(x => x.ActorId == actorId && x.Id != exceptJob)) return false;
            var worker = s.Actors.Single(x => x.Id == actorId);
            if (!WorldSpatialQueries.WithinCardinalRange(worker.X, worker.Y, patch.X, patch.Y, 1)
                || AvailableHands(s, actorId) < exposure.RequiredHands) return false;
            foreach (string itemId in exposure.RequiredImplementIds) {
                var item = s.PortableEquipment.SingleOrDefault(x => x.Id == itemId);
                if (item == null || item.OwnerId != patch.OwnerId || !PortableEquipmentRules.Accessible(s, actorId, item)) return false;
                if (item.Placement == PortablePlacement.Ground && (item.GroundX != patch.X || item.GroundY != patch.Y)) return false;
            }
            return true;
        }

        private sealed class ProspectingAssessment
        {
            public ProspectingPatchRecord Patch;
            public ProspectingExposureRecord Exposure;
            public ProspectingAttemptRecord Current;
            public ProspectingExposureProfile NextExposure;
            public int WisdomModifier, ProficiencyRank, ProficiencyBonus, CheckDc;
        }

        private string AssessProspectingCommand(Snapshot s, Command c, out ProspectingAssessment facts)
        {
            facts = null;
            if (prospectingFixture == null || s.SchemaVersion < Snapshot.ProspectingSchema) return "ProspectingNotSelected";
            if (c.Inventory != null || c.Combat != null || c.Advancement != null || c.Ranged != null || c.HarvestSelection != null
                || c.MiningSelection != null || c.OverwatchRider != OverwatchRider.None || c.SuppressionFire != null
                || c.DefensiveFormation != null || c.ExpeditionAssignment != null || c.X != 0 || c.Y != 0)
                return "InvalidProspectingCommand";
            if (PendingCalendarChoice(s)) return "TacticalChoicePending";
            if (c.Kind == CommandKind.RecordProspectingExposure) {
                var patch = s.ProspectingPatches.SingleOrDefault(x => x.Id == c.Target);
                var profile = c.ProspectingExposure == null ? null : ProspectingProfile(c.ProspectingExposure.ExposureId);
                if (patch == null) return "UnknownProspectingPatch";
                if (profile == null || profile.PatchId != patch.Id) return "UnknownProspectingExposure";
                var prior = s.ProspectingExposures.Single(x => x.Id == patch.CurrentExposureId);
                if (s.ProspectingExposures.Any(x => x.Id == profile.Id)) return "ProspectingExposureAlreadyRecorded";
                if (profile.HazardDeclarationId != "TEST_ONLY.prospecting.hazard.none") return "ProspectingHazardProfileUnsupported";
                if (!ProspectingExposureDiffers(prior, profile)) return "ProspectingEvidenceUnchanged";
                facts = new ProspectingAssessment { Patch = patch, Exposure = prior, NextExposure = profile };
                return null;
            }
            if (c.ProspectingExposure != null) return "InvalidProspectingCommand";
            if (c.Kind == CommandKind.StartProspecting) {
                var patch = s.ProspectingPatches.SingleOrDefault(x => x.Id == c.Target);
                if (patch == null) return "UnknownProspectingPatch";
                var exposure = s.ProspectingExposures.Single(x => x.Id == patch.CurrentExposureId);
                if (!exposure.Exposed || !exposure.Accessible) return "ProspectingEvidenceUnavailable";
                if (exposure.HazardDeclarationId != "TEST_ONLY.prospecting.hazard.none") return "ProspectingHazardProfileUnsupported";
                if (s.ProspectingAttempts.Any(x => x.ExposureId == exposure.Id)) return "ProspectingOpportunityAlreadyAttempted";
                if (s.ProspectingAttempts.Any(x => x.PatchId == patch.Id && (x.Status == ProspectingAttemptStatus.Working
                    || x.Status == ProspectingAttemptStatus.Paused || x.Status == ProspectingAttemptStatus.AwaitingCheck)))
                    return "ProspectingPatchBusy";
                if (IsOffCalendarActivity(s, c.Actor) && StartsOrResumesActivityWork(c)) {
                    var activity = ActivityInterval(s, c.Actor);
                    if (activity.Action == WorldActionCommitment.Dash || activity.Action == WorldActionCommitment.ActiveLabor
                        && !CanContinueActivityLabor(s, c.Actor)) return "OffCalendarActionAlreadySpent";
                }
                if (!ProspectingAccess(s, c.Actor, patch, exposure)) return "ProspectingAccessUnavailable";
                var character = s.Characters.Single(x => x.ActorId == c.Actor);
                var training = s.SkillTraining.SingleOrDefault(x => x.ActorId == c.Actor && x.SkillId == "mining-tools");
                var check = AbilityCheckRules.Derive(character, training, 4);
                facts = new ProspectingAssessment { Patch = patch, Exposure = exposure,
                    WisdomModifier = check.AbilityModifier, ProficiencyRank = check.ProficiencyRank,
                    ProficiencyBonus = check.ProficiencyBonus, CheckDc = ProspectingValidation.Difficulty(exposure.Signs) };
                return null;
            }
            var current = s.ProspectingAttempts.SingleOrDefault(x => x.Id == c.Target && x.ActorId == c.Actor);
            if (current == null) return "UnknownProspectingAttempt";
            var currentPatch = s.ProspectingPatches.Single(x => x.Id == current.PatchId);
            var currentExposure = s.ProspectingExposures.Single(x => x.Id == current.ExposureId);
            if (c.Kind == CommandKind.PauseProspecting) {
                if (current.Status != ProspectingAttemptStatus.Working) return "ProspectingNotWorking";
                facts = new ProspectingAssessment { Current = current, Patch = currentPatch, Exposure = currentExposure };
                return null;
            }
            if (c.Kind != CommandKind.ResumeProspecting) return "InvalidProspectingCommand";
            if (current.Status != ProspectingAttemptStatus.Paused && current.Status != ProspectingAttemptStatus.AwaitingCheck)
                return "ProspectingNotPaused";
            if (!ProspectingAccess(s, c.Actor, currentPatch, currentExposure, current.Id)) return "ProspectingAccessUnavailable";
            facts = new ProspectingAssessment { Current = current, Patch = currentPatch, Exposure = currentExposure };
            return null;
        }

        private void BookProspecting(Snapshot s, ProspectingAttemptRecord attempt)
        {
            RuleTime remaining = SubtractProspectingTime(new RuleTime(ProspectingValidation.WorkSeconds), attempt.WorkDone);
            RuleTime end = AddProspectingTime(s.RuleClock, remaining);
            int interval = s.Work.WorkerIntervals.Count(x => x.JobId == attempt.Id);
            string id = attempt.Id + ".labor." + interval.ToString(CultureInfo.InvariantCulture);
            s.Work = s.Work.Reserve(attempt.Id, new[] { new WorkerInterval(id, attempt.Id, attempt.ActorId, s.RuleClock, end) },
                Array.Empty<ResourceReservation>());
        }

        private void PauseIncompatibleProspecting(Snapshot s)
        {
            if (prospectingFixture == null) return;
            foreach (var attempt in s.ProspectingAttempts.Where(x => x.Status == ProspectingAttemptStatus.Working).ToArray()) {
                var patch = s.ProspectingPatches.Single(x => x.Id == attempt.PatchId);
                var exposure = s.ProspectingExposures.Single(x => x.Id == attempt.ExposureId);
                if (!ProspectingAccess(s, attempt.ActorId, patch, exposure, attempt.Id)) {
                    s.Work = s.Work.CancelFutureWork(attempt.Id, s.RuleClock);
                    PutProspectingAttempt(s, attempt.WithWork(s.RuleClock, attempt.WorkDone, ProspectingAttemptStatus.Paused));
                }
            }
        }

        private static RuleTime? NextProspectingBoundary(Snapshot s)
        {
            var ends = s.ProspectingAttempts.Where(x => x.Status == ProspectingAttemptStatus.Working)
                .Select(x => s.Work.WorkerIntervals.Single(w => w.JobId == x.Id && w.Start <= s.RuleClock && w.End > s.RuleClock).End).ToArray();
            return ends.Length == 0 ? (RuleTime?)null : ends.Min();
        }

        private void CreditProspectingWork(Snapshot s, RuleTime elapsed)
        {
            foreach (var attempt in s.ProspectingAttempts.Where(x => x.Status == ProspectingAttemptStatus.Working).ToArray()) {
                if (!s.Work.WorkerIntervals.Any(w => w.JobId == attempt.Id && w.Start <= attempt.UpdatedAt && w.End >= s.RuleClock)) continue;
                RuleTime work = AddProspectingTime(attempt.WorkDone, elapsed);
                PutProspectingAttempt(s, work >= new RuleTime(ProspectingValidation.WorkSeconds)
                    ? attempt.WithWork(s.RuleClock, new RuleTime(ProspectingValidation.WorkSeconds), ProspectingAttemptStatus.AwaitingCheck)
                    : attempt.WithWork(s.RuleClock, work, ProspectingAttemptStatus.Working));
            }
        }

        private void ResolveReadyProspecting(Snapshot s)
        {
            var ready = s.ProspectingAttempts.Where(x => x.Status == ProspectingAttemptStatus.AwaitingCheck).ToArray();
            foreach (var attempt in ready) {
                var patch = s.ProspectingPatches.Single(x => x.Id == attempt.PatchId);
                var exposure = s.ProspectingExposures.Single(x => x.Id == attempt.ExposureId);
                if (ProspectingAccess(s, attempt.ActorId, patch, exposure, attempt.Id)) FinishProspectingCheck(s, attempt, exposure);
            }
        }

        private void FinishProspectingCheck(Snapshot s, ProspectingAttemptRecord prior, ProspectingExposureRecord exposure)
        {
            int injury = PlaytestLife.AbilityCheckInjuryPenalty(ActorLifeRules.Read(s.Lives.Single(x => x.ActorId == prior.ActorId)), 4, toolCheck: true);
            int modifier = checked(prior.WisdomModifier + prior.ProficiencyBonus + injury);
            int disadvantage = (prior.ProficiencyRank == 0 ? 1 : 0)
                + (TestOnlyClubAttackPolicy.ConditionsFor(s, prior.ActorId).View().Has(ConditionKind.Poisoned) ? 1 : 0);
            uint before = s.RandomState;
            var roll = PlaytestDice.RollD20(before, disadvantageSources: disadvantage);
            var check = PlaytestRolls.TaskCheck(roll.Natural, modifier, prior.CheckDc);
            s.RandomState = roll.NextRandomState;
            ProspectingAttemptStatus status = check.Degree == TaskDegree.CriticalSuccess ? ProspectingAttemptStatus.CriticalSuccess
                : check.Degree == TaskDegree.Success ? ProspectingAttemptStatus.Success
                : check.Degree == TaskDegree.Failure ? ProspectingAttemptStatus.Failure : ProspectingAttemptStatus.CriticalFailure;
            string[] findings = status == ProspectingAttemptStatus.Success || status == ProspectingAttemptStatus.CriticalSuccess
                ? exposure.FindingIds : Array.Empty<string>();
            var degree = check.Degree == TaskDegree.CriticalSuccess ? MiningCheckDegree.CriticalSuccess
                : check.Degree == TaskDegree.Success ? MiningCheckDegree.Success
                : check.Degree == TaskDegree.Failure ? MiningCheckDegree.Failure : MiningCheckDegree.CriticalFailure;
            PutProspectingAttempt(s, prior.WithResult(s.RuleClock, status, degree,
                roll.Selection == D20Selection.Normal ? MiningDiceSelection.Normal : MiningDiceSelection.Disadvantage,
                roll.First, roll.Second ?? 0, roll.Natural, modifier, before, roll.NextRandomState, roll.WordsConsumed, findings));
        }

        private string ResolveProspecting(Snapshot s, Command c)
        {
            string error = AssessProspectingCommand(s, c, out var facts);
            if (error != null) return error;
            if (c.Kind == CommandKind.RecordProspectingExposure) {
                var prior = facts.Exposure;
                var exposure = ProspectingExposureRecord.FromProfile(facts.NextExposure, prior.Id, c.ProspectingExposure.CauseId, s.RuleClock);
                s.ProspectingExposures = s.ProspectingExposures.Concat(new[] { exposure }).ToArray();
                s.ProspectingPatches = s.ProspectingPatches.Select(x => x.Id == facts.Patch.Id ? x.WithCurrentExposure(exposure.Id) : x).ToArray();
                foreach (var attempt in s.ProspectingAttempts.Where(x => x.PatchId == facts.Patch.Id
                    && (x.Status == ProspectingAttemptStatus.Working || x.Status == ProspectingAttemptStatus.Paused
                        || x.Status == ProspectingAttemptStatus.AwaitingCheck)).ToArray()) {
                    s.Work = s.Work.CancelFutureWork(attempt.Id, s.RuleClock);
                    PutProspectingAttempt(s, attempt.Invalidate(s.RuleClock, c.ProspectingExposure.CauseId));
                }
                return null;
            }
            if (c.Kind == CommandKind.StartProspecting) {
                string id = "prospecting." + (s.Revision + 1).ToString(CultureInfo.InvariantCulture);
                var attempt = new ProspectingAttemptRecord(id, c.Actor, facts.Patch.Id, facts.Exposure.Id,
                    facts.Exposure.Id + ".method", s.RuleClock, s.RuleClock, default, ProspectingAttemptStatus.Working,
                    facts.WisdomModifier, facts.ProficiencyRank, facts.ProficiencyBonus, facts.CheckDc, null, null,
                    MiningCheckDegree.None, MiningDiceSelection.None, 0, 0, 0, 0, 0, 0, 0, "", Array.Empty<string>());
                BookProspecting(s, attempt);
                s.ProspectingAttempts = s.ProspectingAttempts.Concat(new[] { attempt }).ToArray();
                return null;
            }
            var current = facts.Current;
            if (c.Kind == CommandKind.PauseProspecting) {
                s.Work = s.Work.CancelFutureWork(current.Id, s.RuleClock);
                PutProspectingAttempt(s, current.WithWork(s.RuleClock, current.WorkDone, ProspectingAttemptStatus.Paused));
                return null;
            }
            if (current.Status == ProspectingAttemptStatus.AwaitingCheck) {
                FinishProspectingCheck(s, current, facts.Exposure);
                return null;
            }
            BookProspecting(s, current);
            PutProspectingAttempt(s, current.WithWork(s.RuleClock, current.WorkDone, ProspectingAttemptStatus.Working));
            return null;
        }
    }
}
#endif
