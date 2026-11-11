#if DECENNIUM_TEST_ONLY && (UNITY_EDITOR || DEVELOPMENT_BUILD || HEADLESS_TESTS)
using System;
using System.Collections.Generic;
using System.Globalization;
using System.Linq;
using System.Security.Cryptography;
using System.Text;

namespace Decennium.Foundation.Laboratory
{
    public sealed class TestOnlyNextCharterPlanProfile
    {
        public const string VersionId = "TEST_ONLY.haven-approach-plan.v1";
        public const string PlannerId = TestOnlyPolicy.ActorId;
        public NextCharterPlanTerms Terms { get; }
        public bool MandateAuthorized { get; }
        public bool EvidenceAccessible { get; }
        public bool DeskPermitted { get; }
        public bool WritingFacilitiesAvailable { get; }
        public bool? ApproachAccess { get; }
        public bool ReserveWaterStartsCarried { get; }

        public TestOnlyNextCharterPlanProfile(bool mandateAuthorized = true, bool evidenceAccessible = true, bool deskPermitted = true,
            bool writingFacilitiesAvailable = true, bool? approachAccess = true, bool duplicateWaterSource = false,
            int validFrom = 0, int authorizationUntil = 48000, bool reserveWaterStartsCarried = false)
        {
            MandateAuthorized = mandateAuthorized;
            EvidenceAccessible = evidenceAccessible;
            DeskPermitted = deskPermitted;
            WritingFacilitiesAvailable = writingFacilitiesAvailable;
            ApproachAccess = approachAccess;
            ReserveWaterStartsCarried = reserveWaterStartsCarried;
            Terms = new NextCharterPlanTerms(VersionId, TestOnlyExpeditionBillProfile.EpisodeId,
                TestOnlyExpeditionBillProfile.CharterVersionId, PlannerId, "TEST_ONLY.next-charter-plan-mandate.v1",
                "TEST_ONLY.next-charter-plan-evidence-access.v1", TestOnlyHavenAppraisalProfile.DeskId,
                "TEST_ONLY.local-approach-accessibility-check.v1", TestOnlyPolicy.CompanionId,
                TestOnlyHavenAppraisalProfile.SiteX, TestOnlyHavenAppraisalProfile.SiteY, 3, 3,
                PortableKitFixture.Rations, PortableKitFixture.Water, PortableKitFixture.Skin,
                duplicateWaterSource ? PortableKitFixture.Water : TestOnlyInventoryPolicy.WaterId,
                duplicateWaterSource ? PortableKitFixture.Skin : TestOnlyFillingPolicy.ActorSkinId,
                new RuleTime(validFrom), new RuleTime(authorizationUntil));
        }

        internal string Key => string.Join("|", "FL19-FL26-46a4d52728ee6956f0bebcb5d2103ffd5bc67ba4", Terms.BindingKey,
            MandateAuthorized, EvidenceAccessible, DeskPermitted, WritingFacilitiesAvailable, ApproachAccess, ReserveWaterStartsCarried,
            "self-service-no-fee", "own-stock-carried-proposal-only", "unresolved-hazards-and-wider-obligations");
    }

    public sealed partial class TestOnlySharedWorldPolicy
    {
        private TestOnlyNextCharterPlanProfile nextCharterPlanProfile;

        public TestOnlySharedWorldPolicy EnableNextCharterPlan(TestOnlyNextCharterPlanProfile profile)
        {
            if (profile == null) throw new ArgumentNullException(nameof(profile));
            if (initializationStarted || nextCharterPlanProfile != null || SelectedSchema != Snapshot.ExpeditionEpisodeCloseSchema)
                throw new InvalidOperationException("Select one prospective plan on the accepted episode-close host before initialization.");
            nextCharterPlanProfile = profile;
            using (var sha = SHA256.Create())
                ContentFingerprint = "TEST_ONLY.next-charter-plan-v1-" + string.Concat(sha.ComputeHash(
                    Encoding.UTF8.GetBytes(ContentFingerprint + "|" + profile.Key)).Select(x => x.ToString("x2", CultureInfo.InvariantCulture)));
            return this;
        }

        private static bool IsNextCharterPlanCommand(CommandKind kind)
            => kind == CommandKind.StartNextCharterPlan || kind == CommandKind.PauseNextCharterPlan || kind == CommandKind.ResumeNextCharterPlan
                || kind == CommandKind.CancelNextCharterPlan || kind == CommandKind.FinalizeNextCharterPlan || kind == CommandKind.InspectNextCharterPlan;

        private static NextCharterPlanRecord OpenNextCharterPlan(Snapshot state) => state.NextCharterPlans.SingleOrDefault(x => x.Open);

        private IEnumerable<Command> DiscoverNextCharterPlan(Snapshot state, string actor)
        {
            if (nextCharterPlanProfile == null || actor != TestOnlyNextCharterPlanProfile.PlannerId || state.ExpeditionEpisodeClose == null)
                yield break;
            Command Option(CommandKind kind, string target) => new Command("option."
                + state.Revision.ToString(CultureInfo.InvariantCulture) + ".next-charter." + kind, actor, state.Revision, kind, target);
            var complete = state.NextCharterPlans.SingleOrDefault(x => x.Report != null);
            if (complete != null) {
                yield return Option(CommandKind.InspectNextCharterPlan, complete.Id);
                yield break;
            }
            var job = OpenNextCharterPlan(state);
            if (job == null) {
                yield return Option(CommandKind.StartNextCharterPlan, nextCharterPlanProfile.Terms.VersionId);
                yield break;
            }
            yield return Option(CommandKind.CancelNextCharterPlan, job.Id);
            switch (job.Status) {
                case NextCharterPlanStatus.Working: yield return Option(CommandKind.PauseNextCharterPlan, job.Id); break;
                case NextCharterPlanStatus.Paused: yield return Option(CommandKind.ResumeNextCharterPlan, job.Id); break;
                case NextCharterPlanStatus.PendingCompletion: yield return Option(CommandKind.FinalizeNextCharterPlan, job.Id); break;
            }
        }

        private string NextCharterPlanBasisFailure(Snapshot state, NextCharterPlanRecord previous, out long passageRevision)
        {
            passageRevision = 0;
            var terms = nextCharterPlanProfile.Terms;
            if (!nextCharterPlanProfile.MandateAuthorized) return "NextCharterPlanningMandateMissing";
            if (!nextCharterPlanProfile.EvidenceAccessible) return "NextCharterPlanningEvidenceUnavailable";
            if (!terms.DistinctWaterSources) return "NextCharterPlanningWaterSourcesNotDistinct";
            var close = state.ExpeditionEpisodeClose;
            if (close == null || close.EpisodeId != terms.EpisodeId || close.CharterVersionId != terms.CharterVersionId)
                return "NextCharterPlanningCloseRequired";
            if (!close.Members.Any(x => x.ActorId == terms.PassageWitnessId)) return "NextCharterPlanningPassageEvidenceMissing";
            if (previous != null && (previous.Terms.BindingKey != terms.BindingKey || previous.PriorCloseRevision != close.CloseRevision))
                return "NextCharterPlanningBasisChanged";
            passageRevision = previous?.PassageRevision ?? FindPlanningPassage(state, terms, close.SourceRevision);
            return passageRevision == 0 ? "NextCharterPlanningPassageEvidenceMissing" : null;
        }

        private long FindPlanningPassage(Snapshot state, NextCharterPlanTerms terms, long throughRevision)
        {
            // Verify a completed prior crossing from the traversal itself, since the close may occur elsewhere.
            var replay = Initial();
            foreach (var receipt in state.Receipts.Where(x => x.Revision <= throughRevision).OrderBy(x => x.Revision)) {
                var traversal = replay.WorldTraversals.SingleOrDefault(x => x.ActorId == terms.PassageWitnessId && !x.Running
                    && x.FromX == terms.StageX && x.FromY == terms.StageY && x.ToX == terms.ApproachX && x.ToY == terms.ApproachY);
                var command = CommandHistory.Read(receipt);
                if (command.ExpectedRevision != replay.Revision || Resolve(replay, command) != null) return 0;
                replay.Revision = receipt.Revision;
                replay.Receipts = replay.Receipts.Append(receipt).ToArray();
                if (traversal != null && !replay.WorldTraversals.Any(x => x.ActorId == traversal.ActorId)
                    && AtSalePosition(replay, traversal.ActorId, traversal.ToX, traversal.ToY)) {
                    var passage = CommandHistory.Read(replay.Receipts.Single(x => x.Revision == traversal.StartedRevision));
                    if (passage.Kind == CommandKind.BeginWorldStep && passage.Target == "walk" && passage.Actor == traversal.ActorId)
                        return traversal.StartedRevision;
                }
            }
            return 0;
        }

        private string NextCharterPlannerFailure(Snapshot state)
        {
            var terms = nextCharterPlanProfile.Terms;
            var desk = state.Structures.SingleOrDefault(x => x.Id == terms.DeskId);
            if (!nextCharterPlanProfile.DeskPermitted || !nextCharterPlanProfile.WritingFacilitiesAvailable || desk == null
                || desk.ProfileId != AppraisalDeskStructure || desk.LocationId != AppraisalGround || desk.Broken)
                return "NextCharterPlanningDeskUnavailable";
            if (CraftingRestrictions.StationUseBlocked(state, desk.Id)) return "NextCharterPlanningDeskUseBlocked";
            if (state.InventoryCombat || state.Encounter != null && !ResolvedConflict(state) || PendingCalendarChoice(state))
                return "NextCharterPlanningCombatUnavailable";
            if (!CapableWorker(state, terms.PlannerId) || View(state, terms.PlannerId).BlocksSight || AvailableHands(state, terms.PlannerId) < 1)
                return "NextCharterPlanningWorkerIncapable";
            return AtSalePosition(state, terms.PlannerId, terms.StageX, terms.StageY) ? null : "NextCharterPlanningWorkerNotAtDesk";
        }

        private string AssessNextCharterPlanCommand(Snapshot state, Command command, out NextCharterPlanRecord job, out long passageRevision,
            out NextCharterPlanObservation observation)
        {
            job = null;
            passageRevision = 0;
            observation = null;
            if (nextCharterPlanProfile == null || state.SchemaVersion != Snapshot.NextCharterPlanSchema) return "NextCharterPlanningNotSelected";
            if (command.Actor != TestOnlyNextCharterPlanProfile.PlannerId) return "NextCharterPlanningWorkerUnauthorized";
            if (command.X != 0 || command.Y != 0 || command.Inventory != null || command.Combat != null || command.Advancement != null
                || command.Ranged != null || command.OverwatchRider != OverwatchRider.None || command.SuppressionFire != null
                || command.DefensiveFormation != null || command.ExpeditionAssignment != null || command.HarvestSelection != null
                || command.MiningSelection != null || command.ProspectingExposure != null || command.RouteMappingWork != null)
                return "InvalidNextCharterPlanningPayload";
            if (command.Kind == CommandKind.InspectNextCharterPlan) {
                job = state.NextCharterPlans.SingleOrDefault(x => x.Id == command.Target && x.Report != null);
                if (job == null) return "NextCharterPlanningReportMissing";
                string invalid = NextCharterPlanBasisFailure(state, job, out passageRevision);
                if (invalid == null) observation = ObserveNextCharterPlan(state, state.Revision);
                return invalid;
            }

            var terms = nextCharterPlanProfile.Terms;
            job = OpenNextCharterPlan(state);
            if (command.Kind == CommandKind.StartNextCharterPlan) {
                if (command.Target != terms.VersionId) return "NextCharterPlanningDefinitionUnknown";
                if (job != null) return "NextCharterPlanningSlotOccupied";
                if (state.NextCharterPlans.Any(x => x.Report != null)) return "NextCharterPlanningAlreadyCompleted";
                if (state.NextCharterPlans.Length >= NextCharterPlanValidation.MaxAttempts) return "NextCharterPlanningHistoryCapacityReached";
            } else {
                if (job == null || command.Target != job.Id) return "NextCharterPlanningWorkNotOpen";
                if (command.Kind == CommandKind.CancelNextCharterPlan) return null;
                if (command.Kind == CommandKind.PauseNextCharterPlan)
                    return job.Status == NextCharterPlanStatus.Working ? null : "NextCharterPlanningWorkNotRunning";
                if (command.Kind == CommandKind.ResumeNextCharterPlan && job.Status != NextCharterPlanStatus.Paused)
                    return "NextCharterPlanningWorkNotPaused";
                if (command.Kind == CommandKind.FinalizeNextCharterPlan && job.Status != NextCharterPlanStatus.PendingCompletion)
                    return "NextCharterPlanningWorkIncomplete";
            }

            string failure = NextCharterPlanBasisFailure(state, job, out passageRevision);
            if (failure != null) return failure;
            var end = CampGreens.Add(state.RuleClock, job?.Work.Remaining ?? new RuleTime(NextCharterPlanRecord.RequiredSeconds));
            if (!terms.AuthorizedAt(state.RuleClock) || end >= terms.AuthorizationUntil) return "NextCharterPlanningAuthorizationWindow";
            failure = NextCharterPlannerFailure(state);
            if (failure != null) return failure;
            if (end > state.RuleClock && IsOffCalendarActivity(state, command.Actor)) {
                var activity = ActivityInterval(state, command.Actor);
                if (activity.Action == WorldActionCommitment.Dash
                    || activity.Action == WorldActionCommitment.ActiveLabor && !CanContinueActivityLabor(state, command.Actor))
                    return "OffCalendarActionAlreadySpent";
            }
            if (WorkerHasIncompatibleLabor(state, command.Actor, end)) return "NextCharterPlanningWorkerBusy";
            observation = ObserveNextCharterPlan(state, state.Revision);
            return null;
        }

        private void BookNextCharterPlan(Snapshot state, NextCharterPlanRecord job)
        {
            string intervalId = job.Id + ".labor." + (state.Revision + 1).ToString(CultureInfo.InvariantCulture);
            state.Work = state.Work.Reserve(job.Id, new[] { new WorkerInterval(intervalId, job.Id, job.WorkerId,
                state.RuleClock, CampGreens.Add(state.RuleClock, job.Work.Remaining)) }, Array.Empty<ResourceReservation>());
            CommitActivityLabor(state, job.WorkerId, job.Id);
        }

        private static void PutNextCharterPlan(Snapshot state, NextCharterPlanRecord job)
            => state.NextCharterPlans = state.NextCharterPlans.Select(x => x.Id == job.Id ? job : x).ToArray();

        private static void StopNextCharterPlan(Snapshot state, NextCharterPlanRecord job, NextCharterPlanStatus status, string reason)
        {
            state.Work = state.Work.CancelFutureWork(job.Id, state.RuleClock);
            PutNextCharterPlan(state, job.With(state, job.Work.Labor, status, reason));
        }

        private void CompleteNextCharterPlan(Snapshot state, NextCharterPlanRecord job)
            => PutNextCharterPlan(state, job.With(state, job.Work.Labor, NextCharterPlanStatus.CompletedConditional,
                "NextCharterPlanningCompletedConditional", ObserveNextCharterPlan(state, state.Revision + 1)));

        private string ResolveNextCharterPlan(Snapshot state, Command command)
        {
            string failure = AssessNextCharterPlanCommand(state, command, out var job, out long passageRevision, out _);
            if (failure != null) return failure;
            switch (command.Kind) {
                case CommandKind.StartNextCharterPlan:
                    long revision = state.Revision + 1;
                    job = new NextCharterPlanRecord("next-charter.plan." + revision.ToString(CultureInfo.InvariantCulture),
                        nextCharterPlanProfile.Terms, state.ExpeditionEpisodeClose.CloseRevision, passageRevision, revision,
                        revision, state.RuleClock, state.RuleClock, default, NextCharterPlanStatus.Working, "NextCharterPlanningAdmitted");
                    state.NextCharterPlans = state.NextCharterPlans.Append(job).ToArray();
                    BookNextCharterPlan(state, job);
                    break;
                case CommandKind.PauseNextCharterPlan:
                    StopNextCharterPlan(state, job, NextCharterPlanStatus.Paused, "NextCharterPlanningPausedByWorker");
                    break;
                case CommandKind.ResumeNextCharterPlan:
                    BookNextCharterPlan(state, job);
                    PutNextCharterPlan(state, job.With(state, job.Work.Labor, NextCharterPlanStatus.Working, "NextCharterPlanningResumed"));
                    break;
                case CommandKind.FinalizeNextCharterPlan:
                    CompleteNextCharterPlan(state, job);
                    break;
                case CommandKind.CancelNextCharterPlan:
                    StopNextCharterPlan(state, job, NextCharterPlanStatus.Cancelled, "NextCharterPlanningCancelled");
                    break;
                case CommandKind.InspectNextCharterPlan:
                    return "NextCharterPlanningReadOnly";
            }
            return null;
        }

        private static RuleTime? NextCharterPlanBoundary(Snapshot state)
        {
            var job = OpenNextCharterPlan(state);
            if (job == null) return null;
            return job.Status == NextCharterPlanStatus.Working
                ? state.Work.WorkerIntervals.Single(x => x.JobId == job.Id && x.End > state.RuleClock).End
                : job.Terms.AuthorizationUntil;
        }

        private static void CreditNextCharterPlan(Snapshot state, RuleTime elapsed)
        {
            var job = OpenNextCharterPlan(state);
            if (job?.Status != NextCharterPlanStatus.Working) return;
            var work = job.Work.Credit(elapsed);
            PutNextCharterPlan(state, job.With(state, work.Labor, work.Complete ? NextCharterPlanStatus.PendingCompletion
                : NextCharterPlanStatus.Working, work.Complete ? "NextCharterPlanningCompletionDue" : "NextCharterPlanningLaborCredited"));
        }

        private void ReconcileNextCharterPlan(Snapshot state)
        {
            var job = OpenNextCharterPlan(state);
            if (job == null) return;
            if (state.RuleClock >= job.Terms.AuthorizationUntil) {
                StopNextCharterPlan(state, job, NextCharterPlanStatus.Expired, "NextCharterPlanningAuthorizationExpired");
                return;
            }
            string invalid = NextCharterPlanBasisFailure(state, job, out _);
            if (invalid != null) {
                StopNextCharterPlan(state, job, NextCharterPlanStatus.Invalidated, invalid);
                return;
            }
            if (job.Status == NextCharterPlanStatus.Working) {
                string obstruction = NextCharterPlannerFailure(state);
                if (obstruction != null) StopNextCharterPlan(state, job, NextCharterPlanStatus.Paused, obstruction);
            }
        }

        private void FinishDueNextCharterPlan(Snapshot state)
        {
            ReconcileNextCharterPlan(state);
            var job = OpenNextCharterPlan(state);
            if (job?.Status != NextCharterPlanStatus.PendingCompletion || job.Reason != "NextCharterPlanningCompletionDue") return;
            string obstruction = NextCharterPlannerFailure(state);
            if (obstruction == null && WorkerHasIncompatibleLabor(state, job.WorkerId, state.RuleClock))
                obstruction = "NextCharterPlanningWorkerBusy";
            if (obstruction == null) CompleteNextCharterPlan(state, job);
            else PutNextCharterPlan(state, job.With(state, job.Work.Labor, NextCharterPlanStatus.PendingCompletion, obstruction));
        }

        private NextCharterPlanObservation ObserveNextCharterPlan(Snapshot state, long revision)
        {
            var terms = nextCharterPlanProfile.Terms;
            string scout = terms.ScoutId;
            bool walkable = WorldWalkable(state, terms.StageX, terms.StageY) && WorldWalkable(state, terms.ApproachX, terms.ApproachY);
            bool occupied = WorldSpatialQueries.Occupied(state, scout, terms.StageX, terms.StageY)
                || WorldSpatialQueries.Occupied(state, scout, terms.ApproachX, terms.ApproachY);
            bool pathReserved = RoutePathReserved(state, scout, terms.StageX, terms.StageY)
                || RoutePathReserved(state, scout, terms.ApproachX, terms.ApproachY);
            bool tactical = state.InventoryCombat || PendingCalendarChoice(state)
                || WorldStepWouldStartEncounter(state, scout, terms.StageX, terms.StageY, terms.ApproachX, terms.ApproachY);
            bool scoutCapable = CapableWorker(state, scout) && Permissions(state, scout).VoluntarySpeed && Speed(state, scout) > 0;

            var burden = PortableEquipmentRules.CarriedBurden(state, scout);
            var limits = PlaytestCarrying.Limits(CarrierSize.Medium, 10);
            bool? burdened = burden.Load.HasValue ? PlaytestCarrying.IsBurdened(burden.Load.Value, limits.Load) : (bool?)null;
            var cohort = state.ExpeditionPressureCohorts.SingleOrDefault(x => x.Members.Contains(scout));
            int? pressure = cohort != null ? ExpeditionPressureRules.Current(state, cohort.Id) : (int?)null;
            int? strain = dailyProvisioning != null || state.ExpeditionStrainGains.Any(x => x.ActorId == scout)
                ? ExpeditionStrainRules.Current(state, scout).Level : (int?)null;
            bool? restDebt = restDebtProfile != null || state.RestDebtEvents.Any(x => x.ActorId == scout)
                ? DebtFor(state, scout).Owed : (bool?)null;
            var supplies = new[] {
                ObserveNextCharterSupply(state, scout, terms.RationRoot, "", terms.IntendedFood + terms.ReserveFood),
                ObserveNextCharterSupply(state, scout, terms.WaterRoot, terms.WaterVessel, terms.WaterPerVessel),
                ObserveNextCharterSupply(state, scout, terms.ReserveWaterRoot, terms.ReserveWaterVessel, terms.WaterPerVessel)
            };
            return new NextCharterPlanObservation(state.RuleClock, revision, walkable, occupied, pathReserved, tactical,
                nextCharterPlanProfile.ApproachAccess, scoutCapable, AtSalePosition(state, scout, terms.StageX, terms.StageY),
                burden.Pounds, burden.Load, PlaytestCarrying.CanCarry(limits, burden), burdened, pressure, strain, restDebt, supplies);
        }

        private static NextCharterSupplyObservation ObserveNextCharterSupply(Snapshot state, string scout, string root, string vesselId,
            RuleQuantity required)
        {
            var vessel = vesselId == "" ? null : state.Vessels.Single(x => x.Id == vesselId);
            var vesselItem = vessel == null ? null : state.PortableEquipment.SingleOrDefault(x =>
                x.LinkKind == PortableLinkKind.WaterVessel && x.LinkedId == vessel.Id);
            var capacity = vessel == null ? (RuleQuantity?)null : WaterFilling.Capacity(vessel.Profile);
            bool suitableVessel = vessel != null && capacity.Value >= required && WaterFilling.Contents(state, vesselId) <= capacity.Value;
            bool vesselCarried = vessel != null && vessel.CustodianId == scout && (vesselItem == null
                ? vessel.LocationId == scout : PortableEquipmentRules.IsCarriedBy(state, scout, vesselItem));
            bool vesselAccess = vessel != null && WaterFilling.OpeningsAvailable(state, "", vesselId) && (vesselItem == null
                ? WaterFilling.Accessible(state, scout, vessel) : PortableEquipmentRules.Accessible(state, scout, vesselItem));
            var family = InventoryValidation.FamilyAt(state, root, state.RuleClock);
            var observed = state.InventoryLots.Where(x => family.Contains(x.LotId)).Select(item => {
                var lot = state.Work.Lots.Single(x => x.Id == item.LotId);
                var portable = state.PortableEquipment.SingleOrDefault(x => x.LinkKind == PortableLinkKind.InventoryLot && x.LinkedId == lot.Id);
                bool owned = item.OwnerId == scout && (vessel == null || vessel.OwnerId == scout);
                bool custody = lot.CustodianId == scout && (vessel == null || vessel.CustodianId == scout);
                bool inBoundVessel = vessel != null && lot.LocationId == vesselId && WaterFilling.SourceVessel(state, lot.Id) == vesselId;
                bool carried = vessel == null
                    ? portable == null ? lot.LocationId == scout : PortableEquipmentRules.IsCarriedBy(state, scout, portable)
                    : vesselCarried && inBoundVessel;
                bool suitable = vessel == null
                    ? item.Nutrition == NutritionKind.FoodPounds && lot.UnitId == TestOnlyInventoryPolicy.FoodUnit && OrdinaryInventory.Fresh(state, item)
                    : item.Nutrition == NutritionKind.WaterPints && lot.UnitId == TestOnlyInventoryPolicy.WaterUnit && suitableVessel && inBoundVessel;
                bool accessible = vessel == null
                    ? portable == null ? TestOnlyInventoryPolicy.Accessible(state, scout, item, lot) : PortableEquipmentRules.Accessible(state, scout, portable)
                    : vesselAccess && inBoundVessel;
                bool ready = carried && accessible && (vessel == null ? item.Access == InventoryAccess.Ready && lot.LocationId == scout
                    : WaterFilling.ReadyForIntake(state, scout, item, lot));
                return new NextCharterStockObservation(lot.Id, item.OwnerId, lot.CustodianId, lot.LocationId,
                    lot.Amount, state.Work.AvailableAmount(lot.Id), owned, custody, carried, suitable, accessible, ready);
            });
            return new NextCharterSupplyObservation(root, vesselId, capacity, vessel?.OwnerId ?? "", vessel?.CustodianId ?? "",
                vessel?.LocationId ?? "", required, observed);
        }
    }
}
#endif
