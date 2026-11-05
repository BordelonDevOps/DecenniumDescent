#if DECENNIUM_TEST_ONLY && (UNITY_EDITOR || DEVELOPMENT_BUILD || HEADLESS_TESTS)
using System;
using System.Globalization;
using System.Linq;

namespace Decennium.Foundation.Laboratory
{
    public sealed partial class TestOnlySharedWorldPolicy
    {
        private static void PutExpeditionAssignment(Snapshot s, ExpeditionWorkAssignmentRecord value)
            => s.ExpeditionAssignments = s.ExpeditionAssignments.Select(x => x.Id == value.Id ? value : x).ToArray();

        private bool AssignmentSite(Snapshot s, ExpeditionWorkProcedure procedure, string targetId, string destinationId,
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
            if (!expeditionAssignmentsEnabled || s.SchemaVersion != Snapshot.ExpeditionAssignmentSchema)
                return "ExpeditionAssignmentsNotSelected";
            if (s.InventoryCombat) return "WorkAssignmentRequiresExploration";
            if (c.Kind == CommandKind.AssignExpeditionWork)
            {
                var request = c.ExpeditionAssignment;
                if (request == null) return "InvalidExpeditionAssignmentRequest";
                if (!ExpeditionAssignmentValidation.HasCapacity(s))
                    return "ExpeditionAssignmentCapacityReached";
                if (s.ExpeditionAssignments.Any(x => x.Open && x.WorkerId == c.Actor)) return "WorkerAlreadyAssigned";
                if (!AssignmentSite(s, request.Procedure, request.TargetId, request.DestinationId,
                    out int siteX, out int siteY, out string siteError)) return siteError;
                string id = "expedition.assignment." + (s.Revision + 1).ToString(CultureInfo.InvariantCulture);
                var actor = s.Actors.Single(x => x.Id == c.Actor);
                var status = actor.X == siteX && actor.Y == siteY && !s.WorldTraversals.Any(x => x.ActorId == c.Actor)
                    ? ExpeditionAssignmentStatus.Ready : ExpeditionAssignmentStatus.Travelling;
                s.ExpeditionAssignments = s.ExpeditionAssignments.Concat(new[] { new ExpeditionWorkAssignmentRecord(id,
                    c.Actor, request.Procedure, request.TargetId, request.DestinationId, siteX, siteY, s.RuleClock,
                    s.RuleClock, status) }).ToArray();
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
            if (!AssignmentSite(s, current.Procedure, current.TargetId, current.DestinationId,
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
            else
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
            PutExpeditionAssignment(s, current.With(ExpeditionAssignmentStatus.Started, s.RuleClock, workId));
            return null;
        }
    }
}
#endif
