#if DECENNIUM_TEST_ONLY && (UNITY_EDITOR || DEVELOPMENT_BUILD || HEADLESS_TESTS)
using System;
using System.Collections.Generic;
using System.Globalization;
using System.Linq;

namespace Decennium.Foundation.Laboratory
{
    /// <summary>Content registration connecting one controlled worker, one existing work
    /// procedure, and one authored physical site. It grants no skill, item, ownership, or
    /// procedure access; the selected handler still validates those facts at start.</summary>
    public sealed class ExpeditionAssignmentBinding
    {
        public string WorkerId { get; }
        public ExpeditionWorkProcedure Procedure { get; }
        public string SiteId { get; }
        public int X { get; }
        public int Y { get; }

        public ExpeditionAssignmentBinding(string workerId, ExpeditionWorkProcedure procedure, string siteId, int x, int y)
        {
            if (!Validation.ValidId(workerId) || !Enum.IsDefined(typeof(ExpeditionWorkProcedure), procedure)
                || !Validation.ValidId(siteId) || x < 0 || y < 0)
                throw new ArgumentException("Invalid expedition assignment binding.");
            WorkerId = workerId; Procedure = procedure; SiteId = siteId; X = x; Y = y;
        }

        internal string Canonical => WorkerId + "|" + ((int)Procedure).ToString(CultureInfo.InvariantCulture)
            + "|" + SiteId + "|" + X.ToString(CultureInfo.InvariantCulture) + "|" + Y.ToString(CultureInfo.InvariantCulture);
    }

    /// <summary>Immutable TEST_ONLY worker/site registrations for the existing assignment
    /// dispatcher. Physical records and procedure handlers remain authoritative.</summary>
    public sealed class SharedExpeditionAssignmentProfile
    {
        private readonly ExpeditionAssignmentBinding[] bindings;
        private readonly string[] workers;
        public string Id { get; }
        public IReadOnlyList<ExpeditionAssignmentBinding> Bindings { get; }
        public IReadOnlyList<string> WorkerIds { get; }

        public SharedExpeditionAssignmentProfile(string id, IEnumerable<ExpeditionAssignmentBinding> bindings)
        {
            this.bindings = (bindings ?? Array.Empty<ExpeditionAssignmentBinding>()).OrderBy(x => x?.Canonical, StringComparer.Ordinal).ToArray();
            if (!Validation.ValidId(id) || this.bindings.Length < 1 || this.bindings.Any(x => x == null)
                || this.bindings.Select(x => x.WorkerId + "|" + x.Procedure + "|" + x.SiteId)
                    .Distinct(StringComparer.Ordinal).Count() != this.bindings.Length
                || this.bindings.GroupBy(x => ((int)x.Procedure).ToString(CultureInfo.InvariantCulture) + "|" + x.SiteId, StringComparer.Ordinal)
                    .Any(g => g.Select(x => x.X + "," + x.Y).Distinct(StringComparer.Ordinal).Count() != 1))
                throw new ArgumentException("Invalid expedition assignment profile.");
            Id = id;
            workers = this.bindings.Select(x => x.WorkerId).Distinct(StringComparer.Ordinal).OrderBy(x => x, StringComparer.Ordinal).ToArray();
            Bindings = Array.AsReadOnly(this.bindings);
            WorkerIds = Array.AsReadOnly(workers);
        }

        internal bool Allows(string workerId, ExpeditionWorkProcedure procedure, string siteId, int x, int y)
            => bindings.Any(b => b.WorkerId == workerId && b.Procedure == procedure && b.SiteId == siteId && b.X == x && b.Y == y);

        internal bool HasSite(ExpeditionWorkProcedure procedure, string siteId, int x, int y)
            => bindings.Any(b => b.Procedure == procedure && b.SiteId == siteId && b.X == x && b.Y == y);

        internal string Fingerprint(string prior)
        {
            if (string.IsNullOrEmpty(prior)) throw new ArgumentException("Missing prior content fingerprint.");
            string value = "shared-expedition-assignment-profile-v1|" + Id + "|"
                + string.Join(";", bindings.Select(x => x.Canonical).OrderBy(x => x, StringComparer.Ordinal));
            using (var hash = System.Security.Cryptography.SHA256.Create())
                return "TEST_ONLY.assign-bind-v1-" + string.Concat(hash.ComputeHash(
                    System.Text.Encoding.UTF8.GetBytes(prior + "|" + value))
                    .Select(x => x.ToString("x2", CultureInfo.InvariantCulture)));
        }
    }

    public sealed partial class TestOnlySharedWorldPolicy
    {
        private const int CampGreensSiteX = 3, CampGreensSiteY = 3;
        private SharedExpeditionAssignmentProfile assignmentBindingProfile;

        /// <summary>Selects explicit worker/site pairings for the existing TEST_ONLY assignment
        /// handlers. Call after selecting those handlers and before Initial().</summary>
        public TestOnlySharedWorldPolicy EnableExpeditionAssignmentBindings(SharedExpeditionAssignmentProfile profile)
        {
            if (initializationStarted) throw new InvalidOperationException("Assignment bindings must be selected before Initial().");
            if (profile == null) throw new ArgumentNullException(nameof(profile));
            if (assignmentBindingProfile != null) throw new InvalidOperationException("Assignment bindings are already selected.");
            if (!expeditionAssignmentsEnabled) EnableExpeditionAssignments();
            assignmentBindingProfile = profile;
            var cropWorkers = profile.Bindings.Where(x => ExpeditionWorkProcedureRules.TryGetCropWork(x.Procedure, out _))
                .Select(x => x.WorkerId).Concat(new[] { TestOnlyPolicy.CompanionId })
                .Distinct(StringComparer.Ordinal).OrderBy(x => x, StringComparer.Ordinal).ToArray();
            if (cropWorkers.Length > 1) {
                var cropPolicy = new TestOnlyCropPolicy(workerIds: cropWorkers);
                inventory = new TestOnlyFillingPolicy(movableVessels: true, cropPolicy: cropPolicy);
                bodies.ConfigureCropWorkers(cropWorkers);
            }
            ContentFingerprint = profile.Fingerprint(ContentFingerprint);
            return this;
        }

        private static void PutExpeditionAssignment(Snapshot s, ExpeditionWorkAssignmentRecord value)
            => s.ExpeditionAssignments = s.ExpeditionAssignments.Select(x => x.Id == value.Id ? value : x).ToArray();

        private bool AssignmentSite(Snapshot s, ExpeditionWorkProcedure procedure, string targetId, string destinationId,
            MiningSelectionRequest miningSelection, string existingAssignmentId,
            out string siteId, out int siteX, out int siteY, out string error)
        {
            siteId = ""; siteX = siteY = 0; error = null;
            if (procedure == ExpeditionWorkProcedure.ToolRepair)
            {
                if (destinationId != "" || repair == null || targetId != SharedCraftingFixture.ToolId
                    || !s.Structures.Any(x => x.Id == targetId)) { error = "UnknownToolRepairAssignmentTarget"; return false; }
                siteId = RepairSiteLocationId; siteX = RepairSiteX; siteY = RepairSiteY; return true;
            }
            if (procedure == ExpeditionWorkProcedure.FishingTrapRetrieval)
            {
                if (!PhysicalFishingEnabled) { error = "FishingTrapAssignmentUnsupported"; return false; }
                var trap = s.FishingTraps.SingleOrDefault(x => x.TrapId == targetId);
                var receiver = s.FishingReceiveLocations.SingleOrDefault(x => x.Id == destinationId);
                if (trap == null || receiver == null || trap.SiteId != receiver.SiteId)
                { error = "UnknownFishingTrapAssignmentTarget"; return false; }
                siteId = trap.SiteId; siteX = trap.X; siteY = trap.Y; return true;
            }
            if (procedure == ExpeditionWorkProcedure.MiningExtraction)
            {
                if (miningFixture==null||s.SchemaVersion<Snapshot.MiningExpeditionAssignmentSchema)
                { error="MiningAssignmentUnsupported"; return false; }
                var deposit=s.MiningDeposits.SingleOrDefault(x=>x.Id==targetId);
                if (deposit==null||destinationId!=""||miningSelection==null
                    ||miningSelection.DepositVersionId!=deposit.VersionId)
                { error="UnknownMiningAssignmentTarget"; return false; }
                siteId=deposit.SiteId;siteX=deposit.SiteX;siteY=deposit.SiteY;return true;
            }
            if (procedure == ExpeditionWorkProcedure.CacheExcavation)
            {
                if (!CacheExcavationSelected(s)) { error = "CacheExcavationNotSelected"; return false; }
                var site = BuriedCacheSite(s, targetId);
                if (site == null || destinationId != "") { error = "UnknownBuriedCacheSite"; return false; }
                if (!site.Buried) { error = "CacheAlreadyExposed"; return false; }
                siteId = site.CacheId; siteX = site.X; siteY = site.Y; return true;
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
                // CropPlotRecord remains content identity/suitability, not geometry. The
                // registered fixture binding supplies its authored tile and must agree with
                // the existing Camp Greens/inventory access model.
                string plotId = plot.Id;
                siteId = plotId;
                var binding = assignmentBindingProfile?.Bindings.FirstOrDefault(x => x.Procedure == procedure && x.SiteId == plotId);
                siteX = binding?.X ?? CampGreensSiteX; siteY = binding?.Y ?? CampGreensSiteY; return true;
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
                    out string siteId, out int siteX, out int siteY, out string siteError)) return siteError;
                if (assignmentBindingProfile != null && !assignmentBindingProfile.Allows(c.Actor, request.Procedure, siteId, siteX, siteY))
                    return assignmentBindingProfile.WorkerIds.Contains(c.Actor, StringComparer.Ordinal)
                        ? "ExpeditionAssignmentSiteNotRegistered" : "ExpeditionAssignmentWorkerNotRegistered";
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
                out string siteIdNow, out int siteXNow, out int siteYNow, out string currentSiteError)) return currentSiteError;
            if (siteXNow != current.SiteX || siteYNow != current.SiteY) return "ExpeditionAssignmentSiteChanged";
            if (assignmentBindingProfile != null && !assignmentBindingProfile.Allows(c.Actor, current.Procedure, siteIdNow, siteXNow, siteYNow))
                return "ExpeditionAssignmentSiteNotRegistered";

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

        private string ValidateExpeditionAssignmentBindings(Snapshot s)
        {
            if (assignmentBindingProfile == null) return null;
            foreach (var binding in assignmentBindingProfile.Bindings)
            {
                if (!s.Actors.Any(a => a.Id == binding.WorkerId)) return "ExpeditionAssignmentWorkerNotControlled";
                bool physical = false;
                if (ExpeditionWorkProcedureRules.TryGetCropWork(binding.Procedure, out _))
                    physical = binding.SiteId == TestOnlyCropPolicy.PlotId && binding.X == CampGreensSiteX
                        && binding.Y == CampGreensSiteY && s.CropPlots.Any(p => p.Id == binding.SiteId);
                else if (binding.Procedure == ExpeditionWorkProcedure.MiningExtraction)
                    physical = miningFixture != null && miningFixture.Deposits.Any(x => x.Deposit.SiteId == binding.SiteId
                        && x.Deposit.SiteX == binding.X && x.Deposit.SiteY == binding.Y)
                        && s.MiningDeposits.Any(x => x.SiteId == binding.SiteId && x.SiteX == binding.X && x.SiteY == binding.Y);
                else if (binding.Procedure == ExpeditionWorkProcedure.ToolRepair)
                {
                    var target = s.Structures.SingleOrDefault(x => x.Id == SharedCraftingFixture.ToolId);
                    var toolkit = s.Structures.SingleOrDefault(x => x.Id == SharedRepairFixture.Toolkit);
                    var materials = s.Work.Lots.SingleOrDefault(x => x.Id == RepairMaterialsLotId);
                    physical = repair != null && binding.SiteId == RepairSiteLocationId
                        && binding.X == RepairSiteX && binding.Y == RepairSiteY
                        && target?.LocationId == binding.SiteId && toolkit?.LocationId == binding.SiteId
                        && materials?.LocationId == binding.SiteId;
                }
                else
                    return "ExpeditionAssignmentProcedureBindingUnsupported";
                if (!physical) return "ExpeditionAssignmentSiteNotRegistered";
            }
            foreach (var assignment in s.ExpeditionAssignments)
            {
                string siteId;
                if (ExpeditionWorkProcedureRules.TryGetCropWork(assignment.Procedure, out _)) siteId = TestOnlyCropPolicy.PlotId;
                else if (assignment.Procedure == ExpeditionWorkProcedure.MiningExtraction)
                    siteId = s.MiningDeposits.SingleOrDefault(x => x.Id == assignment.TargetId)?.SiteId ?? "";
                else if (assignment.Procedure == ExpeditionWorkProcedure.ToolRepair)
                {
                    var target = s.Structures.SingleOrDefault(x => x.Id == assignment.TargetId);
                    if (repair == null || assignment.TargetId != SharedCraftingFixture.ToolId || assignment.DestinationId != ""
                        || target?.LocationId != RepairSiteLocationId) return "ExpeditionAssignmentBindingMismatch";
                    siteId = target.LocationId;
                }
                else return "ExpeditionAssignmentProcedureBindingUnsupported";
                if (siteId == "" || !assignmentBindingProfile.Allows(assignment.WorkerId, assignment.Procedure,
                    siteId, assignment.SiteX, assignment.SiteY)) return "ExpeditionAssignmentBindingMismatch";
            }
            return null;
        }
    }
}
#endif
