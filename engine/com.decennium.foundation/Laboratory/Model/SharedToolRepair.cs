#if DECENNIUM_TEST_ONLY && (UNITY_EDITOR || DEVELOPMENT_BUILD || HEADLESS_TESTS)
using System;
using System.Collections.Generic;
using System.Globalization;
using System.Linq;
using System.Security.Cryptography;
using System.Text;

namespace Decennium.Foundation.Laboratory
{
    /// <summary>One authored wooden-case repair: separate ordinary Carpenter's tools, DEX task,
    /// two compatible 12gp5sp material allotments at the plot, and two legal work Watches.
    /// The shared bench has two compatible work areas for copying and physical repair by different
    /// workers; a spill affects both. Training, recoverable case and intact implements are supplied facts.</summary>
    public sealed class SharedRepairFixture
    {
        public const string Toolkit = "repair.carpenter-kit", Materials = "repair.case-materials";
        public bool Trained { get; }
        public bool UsableToolkit { get; }
        public bool RecoverableBody { get; }
        public bool IntactImplements { get; }
        public bool Accessible { get; }
        public int SiteX { get; }
        public int SiteY { get; }
        public SharedRepairFixture(bool trained = true, bool usableToolkit = true, bool recoverableBody = true, bool intactImplements = true,
            bool accessible = true, int siteX = 3, int siteY = 3)
        {
            if(siteX<0)throw new ArgumentOutOfRangeException(nameof(siteX),"Repair site coordinates must be nonnegative.");
            if(siteY<0)throw new ArgumentOutOfRangeException(nameof(siteY),"Repair site coordinates must be nonnegative.");
            Trained = trained; UsableToolkit = usableToolkit; RecoverableBody = recoverableBody; IntactImplements = intactImplements;
            Accessible = accessible; SiteX=siteX;SiteY=siteY;
        }
        internal string Key => "case-repair-v1|two-material-allotments1250cp|carpenter8gp6lbHP5|iron-bearing-tools|DEX-PB-once-DC10|retain-repair-work|first-labor-debit|two-watches|shared-bench-two-compatible-copy-repair-workareas|copy-independent-of-alchemy-kit|sourced-injury-check-penalties|"
            + Trained + "|" + UsableToolkit + "|" + RecoverableBody + "|" + IntactImplements + "|" + Accessible
            + (SiteX==3&&SiteY==3?"":"|site="+SiteX.ToString(CultureInfo.InvariantCulture)+","+SiteY.ToString(CultureInfo.InvariantCulture));
    }
    public sealed partial class TestOnlySharedWorldPolicy
    {
        private readonly SharedRepairFixture repair;
        public IEnumerable<string> RequiredInventoryOwners(Snapshot s, Command c)
        {
            if(IsProspectingCommand(c)&&c.Kind!=CommandKind.RecordProspectingExposure) {
                string patchId=c.Kind==CommandKind.StartProspecting?c.Target
                    :s.ProspectingAttempts.SingleOrDefault(x=>x.Id==c.Target)?.PatchId;
                var patch=s.ProspectingPatches.SingleOrDefault(x=>x.Id==patchId);
                var exposureId=c.Kind==CommandKind.StartProspecting?patch?.CurrentExposureId
                    :s.ProspectingAttempts.SingleOrDefault(x=>x.Id==c.Target)?.ExposureId;
                var exposure=s.ProspectingExposures.SingleOrDefault(x=>x.Id==exposureId);
                if(patch==null||exposure==null)return Array.Empty<string>();
                return new[]{patch.OwnerId}.Concat(exposure.RequiredImplementIds
                    .Select(id=>s.PortableEquipment.SingleOrDefault(x=>x.Id==id)?.OwnerId))
                    .Where(x=>x!=null).Distinct(StringComparer.Ordinal).ToArray();
            }
            if(IsMiningCommand(c)) {
                string depositId=c.Kind==CommandKind.StartMining?c.Target:s.MiningAttempts.SingleOrDefault(x=>x.Id==c.Target)?.DepositId;
                var deposit=s.MiningDeposits.SingleOrDefault(x=>x.Id==depositId);
                if(deposit==null)return Array.Empty<string>();
                string[] unitIds=c.Kind==CommandKind.StartMining
                    ?s.MiningCategories.Where(x=>x.DepositId==deposit.Id&&(c.MiningSelection?.CategoryIds??Array.Empty<string>()).Contains(x.Id,StringComparer.Ordinal)).SelectMany(x=>x.UnitIds).ToArray()
                    :s.MiningAttempts.SingleOrDefault(x=>x.Id==c.Target)?.SelectedUnitIds??Array.Empty<string>();
                return new[]{deposit.OwnerId,s.PortableEquipment.SingleOrDefault(x=>x.Id==deposit.MiningToolsId)?.OwnerId,
                    s.PortableEquipment.SingleOrDefault(x=>x.Id==deposit.PickId)?.OwnerId,
                    s.PortableEquipment.SingleOrDefault(x=>x.Id==deposit.ReceiverId)?.OwnerId,
                    s.Structures.SingleOrDefault(x=>x.Id==deposit.WorkSurfaceId)?.OwnerId}
                    .Concat(s.InventoryLots.Where(x=>unitIds.Contains(x.LotId,StringComparer.Ordinal)).Select(x=>x.OwnerId))
                    .Where(x=>x!=null).Distinct(StringComparer.Ordinal).ToArray();
            }
            if(IsHarvestCommand(c)) {
                string manifestId=c.Kind==CommandKind.StartHarvest
                    ?s.HarvestCategories.SingleOrDefault(x=>x.Id==c.Target)?.ManifestId
                    :s.HarvestAttempts.SingleOrDefault(x=>x.Id==c.Target)?.ManifestId;
                var manifest=s.HarvestManifests.SingleOrDefault(x=>x.Id==manifestId);
                if(manifest==null)return Array.Empty<string>();
                var donor=s.HarvestDonors.SingleOrDefault(x=>x.CreatureId==manifest.CreatureId);
                return new[]{donor?.OwnerId,s.PortableEquipment.SingleOrDefault(x=>x.Id==manifest.ToolkitId)?.OwnerId,
                    s.PortableEquipment.SingleOrDefault(x=>x.Id==manifest.KnifeId)?.OwnerId,
                    s.PortableEquipment.SingleOrDefault(x=>x.Id==manifest.ContainerId)?.OwnerId,
                    s.Structures.SingleOrDefault(x=>x.Id==manifest.WorkSurfaceId)?.OwnerId}
                    .Where(x=>x!=null).Distinct(StringComparer.Ordinal).ToArray();
            }
            if(IsOrdinaryReceptacleCommand(s,c)) {
                var lockState=s.OrdinaryReceptacleLocks.SingleOrDefault(x=>x.Id==c.Target);
                if(lockState==null)return Array.Empty<string>();
                string credentialId=c.X==(int)OrdinaryReceptacleInteraction.UnlockWithKey?lockState.KeyItemId
                    :c.X==(int)OrdinaryReceptacleInteraction.PickWithTools?lockState.ToolsItemId
                    :c.X==(int)OrdinaryReceptacleInteraction.Interrupt
                        ?s.OrdinaryReceptacleAttempts.SingleOrDefault(x=>x.LockId==lockState.Id&&x.ActorId==c.Actor
                            &&x.Status==OrdinaryReceptacleAttemptStatus.Working)?.CredentialItemId:"";
                return new[]{lockState.OwnerId}.Concat(PortableEquipmentRules.Owners(s,credentialId)).Distinct(StringComparer.Ordinal).ToArray();
            }
            if(c.Kind==CommandKind.AttackRepeatingCrossbow||c.Kind==CommandKind.ReloadRepeatingCrossbow
                ||c.Kind==CommandKind.WarningShot||c.Kind==CommandKind.CoveringFire) {
                var weapon=s.RepeatingCrossbows.FirstOrDefault(x=>x.Id==c.Ranged?.WeaponId);
                var lot=c.Kind==CommandKind.ReloadRepeatingCrossbow?s.AmmunitionLots.FirstOrDefault(x=>x.Id==c.Ranged?.AmmoLotId):null;
                return new[]{weapon?.OwnerId,lot?.OwnerId}.Where(x=>x!=null).Distinct(StringComparer.Ordinal).ToArray();
            }
            if(PortableCommand(c.Kind))return PortableEquipmentRules.Owners(s,c.Target);
            if(IsSupplyCacheCommand(c)) {
                var cache=s.SupplyCaches.SingleOrDefault(x=>x.Id==c.Target);
                if(cache==null)return Array.Empty<string>();
                SupplyCacheEquipmentRecord item=null;
                if(c.X==(int)SupplyCacheInteraction.UnlockWithKey||c.X==(int)SupplyCacheInteraction.PickWithTools) {
                    var kind=c.X==(int)SupplyCacheInteraction.UnlockWithKey?SupplyCacheEquipmentKind.Key:SupplyCacheEquipmentKind.ThievesTools;
                    item=s.SupplyCacheEquipment.SingleOrDefault(x=>x.Kind==kind&&x.LocationId==c.Actor&&x.CustodianId==c.Actor);
                } else if(c.X==(int)SupplyCacheInteraction.Interrupt) {
                    var active=s.SupplyCacheAttempts.SingleOrDefault(x=>x.CacheId==cache.Id&&x.ActorId==c.Actor&&x.Status==SupplyCacheAttemptStatus.Working);
                    if(active!=null)item=s.SupplyCacheEquipment.SingleOrDefault(x=>x.Id==active.EquipmentId);
                }
                return item==null?new[]{cache.OwnerId}:new[]{cache.OwnerId,item.OwnerId}.Distinct(StringComparer.Ordinal).ToArray();
            }
            if(ManufacturingCommand(c.Kind))return ManufacturingOwners(s,c);
            var assignment=c.Kind==CommandKind.StartExpeditionWork
                ?s.ExpeditionAssignments.SingleOrDefault(x=>x.Id==c.Target&&x.WorkerId==c.Actor):null;
            if(assignment?.Procedure==ExpeditionWorkProcedure.FishingTrapRetrieval)
                return PortableEquipmentRules.Owners(s,assignment.TargetId);
            if(assignment?.Procedure==ExpeditionWorkProcedure.CacheExcavation) {
                var site=s.BuriedCacheSites.SingleOrDefault(x=>x.CacheId==assignment.TargetId);
                return PortableEquipmentRules.Owners(s,site?.ShovelId);
            }
            if(CacheExcavationCommand(c)) {
                var work=s.CacheExcavations.SingleOrDefault(x=>x.Id==c.Target&&x.WorkerId==c.Actor);
                return PortableEquipmentRules.Owners(s,work?.ShovelId);
            }
            bool assignedRepair=assignment?.Procedure==ExpeditionWorkProcedure.ToolRepair;
            if (repair == null || !assignedRepair&&c.Kind != CommandKind.StartToolRepair && c.Kind != CommandKind.ResumeToolRepair) return Array.Empty<string>();
            var job = c.Kind == CommandKind.ResumeToolRepair ? s.RepairWork.SingleOrDefault(x => x.Id == c.Target) : null;
            if (c.Kind == CommandKind.ResumeToolRepair && job == null) return Array.Empty<string>();
            string target = assignedRepair?assignment.TargetId:job?.TargetId ?? c.Target;
            string toolkit = job?.ToolkitId ?? SharedRepairFixture.Toolkit, materials = job?.MaterialsId ?? RepairMaterialsLotId;
            return s.Structures.Where(x => x.Id == target || x.Id == toolkit).Select(x => x.OwnerId)
                .Concat(s.InventoryLots.Where(x => x.LotId == materials).Select(x => x.OwnerId)).Distinct(StringComparer.Ordinal).ToArray();
        }
        private static bool TargetInActiveRepair(Snapshot s, string target) => s.RepairWork.Any(x => x.TargetId == target && x.Status == RepairWorkStatus.Working);
        private static bool ResearchUsesRepairTarget(FormulaWorkRecord job, string target) => target == SharedCraftingFixture.ToolId && job.Kind == FormulaWorkKind.Research && job.Status == FormulaWorkStatus.Working;
        private static void AcquireRepairAccess(Snapshot s, string target)
        {
            foreach(var job in s.ManufacturingOrders.Where(x=>x.Status==ManufacturingStatus.Working).ToArray())PauseManufacturing(s,job);
            foreach (var job in s.FormulaWork.Where(x => ResearchUsesRepairTarget(x,target)).ToArray()) PauseFormula(s, job);
            foreach (var incident in s.CraftingIncidents.Where(x => x.ToolId == target && x.Result == 2 && x.Workers.Count != 0).ToArray()) {
                var paused = incident.WithWork(s.RuleClock, incident.Labor, Array.Empty<string>());
                PutIncident(s, paused); BookRemedy(s, paused);
            }
        }
        private static bool RepairWorkerBusy(Snapshot s, string actor, string target)
        {
            var transferable = s.FormulaWork.Where(x => ResearchUsesRepairTarget(x,target)).Select(x => x.Id)
                .Concat(s.CraftingIncidents.Where(x => x.ToolId == target && x.Result == 2 && x.Workers.Count != 0).Select(RemedyJobId)).ToArray();
            return s.Work.WorkerIntervals.Any(x => x.WorkerId == actor && x.Start <= s.RuleClock && x.End > s.RuleClock && !transferable.Contains(x.JobId))
                || WorldActivityProjection.CurrentWork(s).Any(x => x.ActorId == actor && !transferable.Contains(x.Id));
        }
        private static string RepairFingerprint(string prior, SharedRepairFixture facts)
        {
            using (var sha = SHA256.Create()) return "TEST_ONLY.repair-v1-" + string.Concat(sha.ComputeHash(Encoding.UTF8.GetBytes(prior + "|" + facts.Key)).Select(x => x.ToString("x2", CultureInfo.InvariantCulture)));
        }
        private void InitializeRepair(Snapshot s)
        {
            if (repair == null) return;
            s.Structures = s.Structures.Concat(new[] { new ObjectStructureRecord(SharedRepairFixture.Toolkit, "tools.carpenter-s-tools", TestOnlyPolicy.CompanionId,
                TestOnlyPolicy.CompanionId, RepairSiteLocationId, ObjectMaterial.IronSteel, 5, repair.UsableToolkit ? 5 : 0, 800, new RuleQuantity(6)) }).ToArray();
            s.Work = new WorkLedger(s.Work.Lots.Concat(new[] { new ResourceLot(RepairMaterialsLotId, "case-repair-allotment-1250cp", 2, RepairSiteLocationId, TestOnlyPolicy.CompanionId) }), s.Work.WorkerIntervals, s.Work.Reservations);
            s.InventoryLots = s.InventoryLots.Concat(new[] { new InventoryLotRecord(RepairMaterialsLotId, "", TestOnlyPolicy.CompanionId, new RuleQuantity(2), default, NutritionKind.None, null, InventoryAccess.Ground) }).ToArray();
        }
        private static bool RepairCommand(CommandKind kind) => kind == CommandKind.StartToolRepair || kind == CommandKind.PauseToolRepair || kind == CommandKind.ResumeToolRepair || kind == CommandKind.CancelToolRepair;
        private static void PutRepair(Snapshot s, RepairWorkRecord job) => s.RepairWork = s.RepairWork.Select(x => x.Id == job.Id ? job : x).ToArray();
        private static RepairWorkRecord ChangeRepair(Snapshot s, RepairWorkRecord job, RepairWorkStatus status, ActiveWorkProgress work = null, int first = 0, int second = 0, int natural = 0)
            => new RepairWorkRecord(job.Id, job.WorkerId, job.TargetId, job.ToolkitId, job.MaterialsId, status, job.StartedAt, s.RuleClock, work ?? job.Work, first, second, natural);
        private string RepairAccess(Snapshot s, string actor, string targetId, bool requireWindow = true)
        {
            if (!IsRepairWorker(actor) || !repair.Trained) return "RepairTrainingMissing";
            var target = s.Structures.SingleOrDefault(x => x.Id == targetId); var kit = s.Structures.SingleOrDefault(x => x.Id == SharedRepairFixture.Toolkit);
            if (target == null || target.Id != SharedCraftingFixture.ToolId || !repair.RecoverableBody || !repair.IntactImplements) return "RepairTargetUnsupported";
            if (kit == null || kit.Broken) return "RepairToolkitUnavailable";
            if (!repair.Accessible || target.LocationId != RepairSiteLocationId || kit.LocationId != RepairSiteLocationId
                || s.Work.Lots.Single(x => x.Id == RepairMaterialsLotId).LocationId != RepairSiteLocationId) return "RepairAccessUnavailable";
            if (CraftingRestrictions.StationUseBlocked(s, RepairSiteLocationId)) return "RepairStationUnavailable";
            if (!CapableWorker(s, actor) || View(s, actor).BlocksSight || AvailableHands(s, actor) < 1) return "RepairWorkerIncapable";
            var body = s.Actors.Single(x => x.Id == actor);
            if (s.WorldTraversals.Any(x => x.ActorId == actor)
                || !WorldSpatialQueries.WithinRange(body.X, body.Y, RepairSiteX, RepairSiteY, 1)) return "RepairStationOutOfReach";
            if (s.InventoryCombat && s.WorldSchedule.Order.Contains(actor)) return "RepairParticipantInCombat";
            if (requireWindow && !ResearchWindowEnd(s.RuleClock).HasValue) return "RepairWorkWindowClosed";
            return null;
        }
        private static void BookRepair(Snapshot s, RepairWorkRecord job)
        {
            var end = CampGreens.Add(s.RuleClock, job.Work.Remaining); var window = ResearchWindowEnd(s.RuleClock).Value; if (window < end) end = window;
            string id = job.Id + ".labor." + (s.Revision + 1).ToString(CultureInfo.InvariantCulture);
            s.Work = s.Work.Reserve(job.Id, new[] { new WorkerInterval(id, job.Id, job.WorkerId, s.RuleClock, end) }, Array.Empty<ResourceReservation>());
        }
        private static void PauseRepair(Snapshot s, RepairWorkRecord job)
        {
            if (job.Status != RepairWorkStatus.Working) return;
            s.Work = s.Work.CancelFutureWork(job.Id, s.RuleClock); PutRepair(s, ChangeRepair(s, job, RepairWorkStatus.Paused, job.Work.Interrupt(false)));
        }
        private void PauseIncompatibleRepairs(Snapshot s)
        {
            if (repair == null) return;
            foreach (var job in s.RepairWork.Where(x => x.Status == RepairWorkStatus.Working).ToArray())
                if (RepairAccess(s, job.WorkerId, job.TargetId, false) != null) PauseRepair(s, job);
        }
        private static RuleTime? NextRepairBoundary(Snapshot s)
        {
            var ends = s.RepairWork.Where(x => x.Status == RepairWorkStatus.Working).Select(x => s.Work.WorkerIntervals.Single(w => w.JobId == x.Id && w.Start <= s.RuleClock && w.End > s.RuleClock).End).ToArray();
            return ends.Length == 0 ? (RuleTime?)null : ends.Min();
        }
        private static void CreditRepairWork(Snapshot s, RuleTime elapsed, ICollection<string> ready)
        {
            foreach (var job in s.RepairWork.Where(x => x.Status == RepairWorkStatus.Working).ToArray()) {
                if (job.Work.Labor == default) s.Work = s.Work.Consume(job.Id, job.Id + ".materials");
                var progress = job.Work.Credit(elapsed); var status = RepairWorkStatus.Working;
                if (progress.Complete) { status = RepairWorkStatus.AwaitingCheck; ready.Add(job.Id); }
                else if (!s.Work.WorkerIntervals.Any(w => w.JobId == job.Id && w.Start <= s.RuleClock && w.End > s.RuleClock)) status = RepairWorkStatus.Paused;
                PutRepair(s, ChangeRepair(s, job, status, progress));
            }
        }
        private static void FinishRepair(Snapshot s, RepairWorkRecord job)
        {
            var character = s.Characters.Single(x => x.ActorId == job.WorkerId);
            var facts = CharacterRuleFacts.From(character);
            int modifier = facts.AbilityModifier(CharacterAbility.Dexterity) + facts.ProficiencyBonus;
            modifier += PlaytestLife.AbilityCheckInjuryPenalty(ActorLifeRules.Read(s.Lives.Single(x => x.ActorId == job.WorkerId)), 1, toolCheck: true);
            var roll = PlaytestDice.RollD20(s.RandomState, disadvantageSources: View(s, job.WorkerId).Has(ConditionKind.Poisoned) ? 1 : 0); s.RandomState = roll.NextRandomState;
            bool success = ObjectStructureRules.RepairSucceeds(roll.Natural, modifier);
            if (success) s.Structures = s.Structures.Select(x => x.Id == job.TargetId ? x.WithHp(x.MaximumHp) : x).ToArray();
            PutRepair(s, ChangeRepair(s, job, success ? RepairWorkStatus.Success : RepairWorkStatus.Failure, first: roll.First, second: roll.Second ?? 0, natural: roll.Natural));
        }
        private string ResolveRepair(Snapshot s, Command c)
        {
            string assessment = AssessRepairCommand(s, c, out var current); if (assessment != null) return assessment;
            if (c.Kind == CommandKind.StartToolRepair) {
                var target = s.Structures.Single(x => x.Id == c.Target);
                string id = "repair.work." + (s.Revision + 1).ToString(CultureInfo.InvariantCulture);
                var job = new RepairWorkRecord(id, c.Actor, c.Target, SharedRepairFixture.Toolkit, RepairMaterialsLotId, RepairWorkStatus.Working, s.RuleClock, s.RuleClock,
                    new ActiveWorkProgress(new[] { ObjectStructureRules.RepairLabor(target) }));
                s.Work = s.Work.Reserve(id, Array.Empty<WorkerInterval>(), new[] { new ResourceReservation(id + ".materials", id, job.MaterialsId, 1) });
                AcquireRepairAccess(s,c.Target);BookRepair(s, job); s.RepairWork = s.RepairWork.Concat(new[] { job }).ToArray(); return null;
            }
            if (c.Kind == CommandKind.PauseToolRepair) {
                PauseRepair(s, current); return null;
            }
            if (c.Kind == CommandKind.CancelToolRepair) {
                s.Work = s.Work.CancelFutureWork(current.Id, s.RuleClock);
                if (current.Work.Labor == default) s.Work = s.Work.Release(current.Id, current.Id + ".materials");
                PutRepair(s, ChangeRepair(s, current, RepairWorkStatus.Cancelled)); return null;
            }
            if (c.Kind == CommandKind.ResumeToolRepair) {
                AcquireRepairAccess(s,current.TargetId);
                if (current.Status == RepairWorkStatus.AwaitingCheck) { FinishRepair(s, current); return null; }
                BookRepair(s, current); PutRepair(s, ChangeRepair(s, current, RepairWorkStatus.Working)); return null;
            }
            return "InvalidRepairRequest";
        }
    }
}
#endif
