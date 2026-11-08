#if DECENNIUM_TEST_ONLY && (UNITY_EDITOR || DEVELOPMENT_BUILD || HEADLESS_TESTS)
using System;
using System.Globalization;
using System.Linq;

namespace Decennium.Foundation.Laboratory
{
    public sealed partial class TestOnlySharedWorldPolicy
    {
        private const int CampGreensSiteX = 3, CampGreensSiteY = 3;
        private static void PutExpeditionAssignment(Snapshot s, ExpeditionWorkAssignmentRecord value)
            => s.ExpeditionAssignments = s.ExpeditionAssignments.Select(x => x.Id == value.Id ? value : x).ToArray();

        private bool AssignmentSite(Snapshot s, ExpeditionWorkProcedure procedure, string targetId, string destinationId,
            MiningSelectionRequest miningSelection, string existingAssignmentId,
            out int siteX, out int siteY, out string error)
        {
            siteX = siteY = 0; error = null;
            if (procedure == ExpeditionWorkProcedure.ToolRepair)
            {
                if (destinationId != "" || repair == null || targetId != SharedCraftingFixture.ToolId
                    || !s.Structures.Any(x => x.Id == targetId)) { error = "UnknownToolRepairAssignmentTarget"; return false; }
                siteX = RepairSiteX; siteY = RepairSiteY; return true;
            }
            if (procedure == ExpeditionWorkProcedure.FishingTrapRetrieval)
            {
                if (!PhysicalFishingEnabled) { error = "FishingTrapAssignmentUnsupported"; return false; }
                var trap = s.FishingTraps.SingleOrDefault(x => x.TrapId == targetId);
                var receiver = s.FishingReceiveLocations.SingleOrDefault(x => x.Id == destinationId);
                if (trap == null || receiver == null || trap.SiteId != receiver.SiteId)
                { error = "UnknownFishingTrapAssignmentTarget"; return false; }
                siteX = trap.X; siteY = trap.Y; return true;
            }
            if (procedure == ExpeditionWorkProcedure.MiningExtraction)
            {
                if (miningFixture==null||s.SchemaVersion<Snapshot.MiningExpeditionAssignmentSchema)
                { error="MiningAssignmentUnsupported"; return false; }
                var deposit=s.MiningDeposits.SingleOrDefault(x=>x.Id==targetId);
                if (deposit==null||destinationId!=""||miningSelection==null
                    ||miningSelection.DepositVersionId!=deposit.VersionId)
                { error="UnknownMiningAssignmentTarget"; return false; }
                siteX=deposit.SiteX;siteY=deposit.SiteY;return true;
            }
            if (procedure == ExpeditionWorkProcedure.CacheExcavation)
            {
                if (!CacheExcavationSelected(s)) { error = "CacheExcavationNotSelected"; return false; }
                var site = BuriedCacheSite(s, targetId);
                if (site == null || destinationId != "") { error = "UnknownBuriedCacheSite"; return false; }
                if (!site.Buried) { error = "CacheAlreadyExposed"; return false; }
                siteX = site.X; siteY = site.Y; return true;
            }
            if (ExpeditionWorkProcedureRules.TryGetCropWork(procedure, out var cropKind))
            {
                if (!cropAssignmentsEnabled || destinationId != "")
                { error = "CampGreensAssignmentUnsupported"; return false; }
                var plot = s.CropPlots.SingleOrDefault(x => x.Id == TestOnlyCropPolicy.PlotId);
                if (plot == null) { error = "CampGreensPlotUnavailable"; return false; }
                if (cropKind == CropWorkKind.Plant)
                {
                    if (s.Crops.Any(x => x.Id == targetId)
                        || s.ExpeditionAssignments.Any(x => x.Procedure == ExpeditionWorkProcedure.CropPlanting
                            && x.Id != existingAssignmentId && x.TargetId == targetId
                            && x.Status != ExpeditionAssignmentStatus.Cancelled))
                    { error = "CropBatchAlreadyExistsOrAssigned"; return false; }
                }
                else
                {
                    var crop = s.Crops.SingleOrDefault(x => x.Id == targetId);
                    var expectedStage = cropKind == CropWorkKind.Tend ? CropStage.Growing : CropStage.Mature;
                    if (crop == null || crop.PlotId != plot.Id || crop.Stage != expectedStage)
                    { error = cropKind == CropWorkKind.Tend ? "CropNotTendable" : "CropNotHarvestable"; return false; }
                }
                // The existing TEST_ONLY Camp Greens plot is authored at this world tile;
                // CropPlotRecord itself remains content identity/suitability, not geometry.
                siteX = CampGreensSiteX; siteY = CampGreensSiteY; return true;
            }
            error = "UnknownExpeditionWorkProcedure"; return false;
        }

        private static void SyncExpeditionAssignments(Snapshot s, string workerId = null)
        {
            foreach (var assignment in s.ExpeditionAssignments.Where(x => x.Open
                && (workerId == null || x.WorkerId == workerId)).ToArray())
            {
                var actor = s.Actors.Single(x => x.Id == assignment.WorkerId);
                bool ready = actor.X == assignment.SiteX && actor.Y == assignment.SiteY
                    && !s.WorldTraversals.Any(x => x.ActorId == actor.Id);
                var status = ready ? ExpeditionAssignmentStatus.Ready : ExpeditionAssignmentStatus.Travelling;
                if (assignment.Status != status) PutExpeditionAssignment(s, assignment.With(status, s.RuleClock));
            }
        }

        private string ResolveExpeditionAssignment(Snapshot s, Command c)
        {
            if (!expeditionAssignmentsEnabled || s.SchemaVersion < Snapshot.ExpeditionAssignmentSchema)
                return "ExpeditionAssignmentsNotSelected";
            if (s.InventoryCombat) return "WorkAssignmentRequiresExploration";
            if (c.Kind == CommandKind.AssignExpeditionWork)
            {
                var request = c.ExpeditionAssignment;
                if (request == null) return "InvalidExpeditionAssignmentRequest";
                if (!ExpeditionAssignmentValidation.HasCapacity(s))
                    return "ExpeditionAssignmentCapacityReached";
                if (s.ExpeditionAssignments.Any(x => x.Open && x.WorkerId == c.Actor)) return "WorkerAlreadyAssigned";
                if (!AssignmentSite(s, request.Procedure, request.TargetId, request.DestinationId,request.MiningSelection,"",
                    out int siteX, out int siteY, out string siteError)) return siteError;
                string id = "expedition.assignment." + (s.Revision + 1).ToString(CultureInfo.InvariantCulture);
                var actor = s.Actors.Single(x => x.Id == c.Actor);
                var status = actor.X == siteX && actor.Y == siteY && !s.WorldTraversals.Any(x => x.ActorId == c.Actor)
                    ? ExpeditionAssignmentStatus.Ready : ExpeditionAssignmentStatus.Travelling;
                s.ExpeditionAssignments = s.ExpeditionAssignments.Concat(new[] { new ExpeditionWorkAssignmentRecord(id,
                    c.Actor, request.Procedure, request.TargetId, request.DestinationId, siteX, siteY, s.RuleClock,
                    s.RuleClock, status, miningSelection:request.MiningSelection) }).ToArray();
                return null;
            }

            var current = s.ExpeditionAssignments.SingleOrDefault(x => x.Id == c.Target && x.WorkerId == c.Actor);
            if (current == null) return "UnknownExpeditionAssignment";
            if (c.Kind == CommandKind.CancelExpeditionWork)
            {
                if (!current.Open) return "ExpeditionAssignmentClosed";
                PutExpeditionAssignment(s, current.With(ExpeditionAssignmentStatus.Cancelled, s.RuleClock));
                return null;
            }
            if (c.Kind != CommandKind.StartExpeditionWork) return "InvalidExpeditionAssignmentCommand";
            if (current.Status != ExpeditionAssignmentStatus.Ready) return "ExpeditionAssignmentNotReady";
            var worker = s.Actors.Single(x => x.Id == c.Actor);
            if (worker.X != current.SiteX || worker.Y != current.SiteY || s.WorldTraversals.Any(x => x.ActorId == c.Actor))
                return "ExpeditionAssignmentNotAtSite";
            if (!AssignmentSite(s, current.Procedure, current.TargetId, current.DestinationId,current.MiningSelection,current.Id,
                out int siteXNow, out int siteYNow, out string currentSiteError)) return currentSiteError;
            if (siteXNow != current.SiteX || siteYNow != current.SiteY) return "ExpeditionAssignmentSiteChanged";

            string error;
            string workId;
            if (current.Procedure == ExpeditionWorkProcedure.ToolRepair)
            {
                int priorCount = s.RepairWork.Length;
                error = ResolveRepair(s, new Command(c.Id, c.Actor, c.ExpectedRevision, CommandKind.StartToolRepair, current.TargetId));
                if (error != null) return error;
                var job = s.RepairWork.Skip(priorCount).SingleOrDefault();
                if (job == null) return "AssignmentProcedureDidNotCreateRepair";
                workId = job.Id;
            }
            else if(current.Procedure==ExpeditionWorkProcedure.FishingTrapRetrieval)
            {
                int priorCount = s.FishingTrapRetrievals.Length;
                var delegated = new Command(c.Id, c.Actor, c.ExpectedRevision, CommandKind.Interact, current.TargetId,
                    (int)FishingTrapInteraction.Retrieve, inventory: new InventoryRequest(default, current.DestinationId, HandlingKind.Retrieve));
                error = ResolveFishingTrap(s, delegated);
                if (error != null) return error;
                var job = s.FishingTrapRetrievals.Skip(priorCount).SingleOrDefault();
                if (job == null) return "AssignmentProcedureDidNotCreateTrapRetrieval";
                workId = job.Id;
            }
            else if (current.Procedure == ExpeditionWorkProcedure.CacheExcavation)
            {
                error = StartCacheExcavation(s, current, out workId);
                if (error != null) return error;
            }
            else if (ExpeditionWorkProcedureRules.TryGetCropWork(current.Procedure, out var cropKind))
            {
                CommandKind kind = cropKind == CropWorkKind.Plant ? CommandKind.PlantCrop
                    : cropKind == CropWorkKind.Tend ? CommandKind.TendCrop : CommandKind.HarvestCrop;
                error = Resolve(s, new Command(c.Id, c.Actor, c.ExpectedRevision, kind, current.TargetId));
                if (error != null) return error;
                var task = s.Crops.Single(x => x.Id == current.TargetId).Tasks.SingleOrDefault(x =>
                    x.WorkerId == current.WorkerId && x.Kind == cropKind && x.Status == CropWorkStatus.Working);
                if (task == null) return "AssignmentProcedureDidNotCreateCropWork";
                workId = task.Id;
            }
            else
            {
                int priorCount=s.MiningAttempts.Length;
                error=ResolveMining(s,new Command(c.Id,c.Actor,c.ExpectedRevision,CommandKind.StartMining,current.TargetId,
                    miningSelection:current.MiningSelection));
                if(error!=null)return error;
                var job=s.MiningAttempts.Skip(priorCount).SingleOrDefault();
                if(job==null)return "AssignmentProcedureDidNotCreateMiningAttempt";
                workId=job.Id;
            }
            PutExpeditionAssignment(s, current.With(ExpeditionAssignmentStatus.Started, s.RuleClock, workId));
            return null;
        }
    }
}
#endif
