#if DECENNIUM_TEST_ONLY && (UNITY_EDITOR || DEVELOPMENT_BUILD || HEADLESS_TESTS)
using System;
using System.Globalization;
using System.Linq;
using System.Security.Cryptography;
using System.Text;

namespace Decennium.Foundation.Laboratory
{
    public sealed partial class TestOnlySharedWorldPolicy
    {
        private bool harvestPreservationEnabled;

        /// <summary>Build the explicit schema74 TEST_ONLY witness over the existing finite harvest fixture.
        /// The two-interval workload is harness scaffolding so it remains unfinished at the first
        /// sourced preservation boundary; it is not a crafting duration.</summary>
        public static TestOnlySharedWorldPolicy WithHarvestPreservation(SharedHarvestFixture harvest=null,uint seed=1)
        {
            var policy=WithHarvest(harvest??new SharedHarvestFixture(),seed);
            policy.harvestPreservationEnabled=true;
            using(var sha=SHA256.Create())policy.ContentFingerprint="TEST_ONLY.mgt05a-v1-"
                +string.Concat(sha.ComputeHash(Encoding.UTF8.GetBytes(policy.ContentFingerprint
                    +"|harvest-preservation-derived-v1|fresh-only-reservation-work-adapter-v1|fixture-work=two-age-intervals"
                    +"|portable-identities=TEST_ONLY.harvest-tray:item,prototype.generic-pound-lot:mass-pound;volume=unknown"))
                    .Select(x=>x.ToString("x2",CultureInfo.InvariantCulture)));
            return policy;
        }

        internal static PortableStorageProfileRecord[] PreservationPortableProfiles()=>new[]{
            new PortableStorageProfileRecord("TEST_ONLY.harvest-tray","item",null),
            new PortableStorageProfileRecord("prototype.generic-pound-lot",SharedHarvestFixture.MaterialUnit,null)
        };

        internal static void InitializePreservationPortableProfiles(Snapshot s)
        {
            if(s.SchemaVersion!=Snapshot.HarvestPreservationSchema)
                throw new ArgumentException("Harvest preservation portable profiles require schema74.");
            s.PortableStorageProfiles=PreservationPortableProfiles();
        }

        internal static string ValidatePreservationPortableProfiles(Snapshot s)
        {
            if(s.SchemaVersion!=Snapshot.HarvestPreservationSchema||!s.TestOnly||s.PortableStorageProfiles==null
                ||s.PortableStorageProfiles.Length!=2)return "HarvestPreservationPortableProfileMismatch";
            var tray=s.PortableStorageProfiles.SingleOrDefault(x=>x.ProfileId=="TEST_ONLY.harvest-tray");
            var pounds=s.PortableStorageProfiles.SingleOrDefault(x=>x.ProfileId=="prototype.generic-pound-lot");
            if(tray==null||tray.QuantityUnitId!="item"||tray.PackedVolumePerUnitCubicFeet.HasValue||tray.MassPerUnitLb.HasValue
                ||tray.AllowedContainedProfileIds.Count!=0||pounds==null
                ||pounds.QuantityUnitId!=SharedHarvestFixture.MaterialUnit||pounds.PackedVolumePerUnitCubicFeet.HasValue
                ||pounds.MassPerUnitLb.HasValue||pounds.AllowedContainedProfileIds.Count!=0)
                return "HarvestPreservationPortableProfileMismatch";
            return null;
        }

        private static bool HarvestRequirementWorkCommand(CommandKind kind)
            =>kind==CommandKind.StartHarvestRequirementWork||kind==CommandKind.PauseHarvestRequirementWork
                ||kind==CommandKind.ResumeHarvestRequirementWork;

        private static HarvestRequirementWorkRecord ReplaceHarvestRequirementWork(Snapshot s,HarvestRequirementWorkRecord value)
        {
            s.HarvestRequirementWorks=s.HarvestRequirementWorks.Select(x=>x.Id==value.Id?value:x).ToArray();
            return value;
        }

        private static RuleTime AddHarvestRequirementTime(RuleTime first,RuleTime second)
        {
            var sum=new RuleQuantity(first.Numerator,first.Denominator)+new RuleQuantity(second.Numerator,second.Denominator);
            return new RuleTime(sum.Numerator,sum.Denominator);
        }

        private static RuleTime SubtractHarvestRequirementTime(RuleTime first,RuleTime second)
        {
            var difference=new RuleQuantity(first.Numerator,first.Denominator)-new RuleQuantity(second.Numerator,second.Denominator);
            return new RuleTime(difference.Numerator,difference.Denominator);
        }

        private RuleTime HarvestRequirementDuration(Snapshot s,string lotId)
        {
            if(!HarvestPreservationRules.TryProject(s,lotId,out var view))throw new ArgumentException("Unknown harvest preservation lineage.");
            var unit=s.HarvestUnits.Single(x=>x.Id==view.HarvestUnitId);
            return new RuleTime(checked(unit.PreservationIntervalSeconds*2L));
        }

        private static RuleTime? NextHarvestRequirementWorkBoundary(Snapshot s)
        {
            RuleTime? next=null;
            foreach(var job in s.HarvestRequirementWorks.Where(x=>x.Status==HarvestRequirementWorkStatus.Working)) {
                var interval=s.Work.WorkerIntervals.Single(w=>w.JobId==job.Id&&w.Start<=s.RuleClock&&w.End>s.RuleClock);
                if(!next.HasValue||interval.End<next.Value)next=interval.End;
                if(!HarvestPreservationRules.TryProject(s,job.InventoryLotId,out var view))
                    throw new InvalidOperationException("Harvest requirement lineage disappeared.");
                var unit=s.HarvestUnits.Single(x=>x.Id==view.HarvestUnitId);
                RuleTime boundary=unit.OriginAt.AddSeconds(unit.PreservationIntervalSeconds);
                if(boundary>s.RuleClock&&(!next.HasValue||boundary<next.Value))next=boundary;
            }
            return next;
        }

        private string AssessHarvestRequirementWork(Snapshot s,Command c,out HarvestRequirementWorkRecord current,
            out HarvestPreservationView preservation)
        {
            current=null;preservation=null;
            if(!harvestPreservationEnabled||s.SchemaVersion!=Snapshot.HarvestPreservationSchema)return "HarvestRequirementWorkNotSelected";
            bool start=c.Kind==CommandKind.StartHarvestRequirementWork;
            if((start?c.Inventory==null:c.Inventory!=null)||c.Target==""||c.X!=0||c.Y!=0
                ||c.Combat!=null||c.Advancement!=null||c.Ranged!=null||c.OverwatchRider!=OverwatchRider.None
                ||c.SuppressionFire!=null||c.DefensiveFormation!=null||c.ExpeditionAssignment!=null
                ||c.HarvestSelection!=null||c.MiningSelection!=null||c.ProspectingExposure!=null||c.RouteMappingWork!=null)
                return "InvalidHarvestRequirementWorkCommand";
            if(s.InventoryCombat)return "HarvestRequirementWorkDuringCombatUnsupported";
            if(start) {
                if(c.Inventory.Amount==default||c.Inventory.Destination!=""||c.Inventory.Handling!=HandlingKind.Pickup)
                    return "InvalidHarvestRequirementInput";
                if(s.HarvestRequirementWorks.Any(x=>x.Status==HarvestRequirementWorkStatus.Working
                    ||x.Status==HarvestRequirementWorkStatus.Paused))return "HarvestRequirementWorkAlreadyOpen";
                if(!HarvestPreservationRules.TryProject(s,c.Target,out preservation))return "HarvestRequirementNeedsHarvestedMass";
                if(preservation.State!=HarvestPreservationState.Fresh)return "FreshIngredientRequired";
                var item=s.InventoryLots.Single(x=>x.LotId==c.Target);
                var physical=s.PortableEquipment.Single(x=>x.Id==item.LotId&&x.LinkKind==PortableLinkKind.InventoryLot
                    &&x.LinkedId==item.LotId&&x.MassBasis==PortableMassBasis.GenericPounds);
                if(!PortableEquipmentRules.Accessible(s,c.Actor,physical))return "InventoryOutOfReach";
                if(!CapableWorker(s,c.Actor))return "HarvestRequirementWorkerIncapable";
                if(OrdinaryInventory.Busy(s,c.Actor))return "WorkerBusy";
                if(c.Inventory.Amount>s.Work.AvailableAmount(c.Target))return "InventoryQuantityUnavailable";
                return null;
            }
            current=s.HarvestRequirementWorks.SingleOrDefault(x=>x.Id==c.Target&&x.WorkerId==c.Actor);
            if(current==null)return "UnknownHarvestRequirementWork";
            if(c.Kind==CommandKind.PauseHarvestRequirementWork) {
                if(current.Status!=HarvestRequirementWorkStatus.Working)return "HarvestRequirementWorkNotWorking";
                return null;
            }
            if(current.Status!=HarvestRequirementWorkStatus.Paused)return "HarvestRequirementWorkNotPaused";
            if(!HarvestPreservationRules.TryProject(s,current.InventoryLotId,out preservation))return "HarvestRequirementNeedsHarvestedMass";
            if(preservation.State!=HarvestPreservationState.Fresh)return "FreshIngredientRequired";
            string currentLotId=current.InventoryLotId;
            var bound=s.PortableEquipment.Single(x=>x.Id==currentLotId&&x.LinkKind==PortableLinkKind.InventoryLot
                &&x.LinkedId==currentLotId&&x.MassBasis==PortableMassBasis.GenericPounds);
            if(!PortableEquipmentRules.Accessible(s,c.Actor,bound))return "InventoryOutOfReach";
            if(!CapableWorker(s,c.Actor))return "HarvestRequirementWorkerIncapable";
            if(OrdinaryInventory.Busy(s,c.Actor))return "WorkerBusy";
            string reservationId=current.ReservationId;
            var claim=s.Work.Reservations.Single(x=>x.Id==reservationId);
            if(claim.RemainingAmount!=current.RequiredAmount)return "HarvestRequirementReservationUnavailable";
            return null;
        }

        private void BookHarvestRequirementWork(Snapshot s,HarvestRequirementWorkRecord job)
        {
            RuleTime end=AddHarvestRequirementTime(s.RuleClock,job.Work.Remaining);
            string intervalId=job.Id+".labor."+(s.Revision+1).ToString(CultureInfo.InvariantCulture);
            s.Work=s.Work.Reserve(job.Id,new[]{new WorkerInterval(intervalId,job.Id,job.WorkerId,s.RuleClock,end)},Array.Empty<ResourceReservation>());
        }

        private void PauseHarvestRequirementWork(Snapshot s,HarvestRequirementWorkRecord job,
            HarvestRequirementWorkStatus status,HarvestRequirementPauseReason reason,ActiveWorkProgress progress=null)
        {
            if(job.Status!=HarvestRequirementWorkStatus.Working)return;
            s.Work=s.Work.CancelFutureWork(job.Id,s.RuleClock);
            ReplaceHarvestRequirementWork(s,job.With(s.RuleClock,progress??job.Work,status,reason));
        }

        private void PauseIncompatibleHarvestRequirementWork(Snapshot s)
        {
            if(!harvestPreservationEnabled)return;
            foreach(var job in s.HarvestRequirementWorks.Where(x=>x.Status==HarvestRequirementWorkStatus.Working).ToArray())
                if(!CapableWorker(s,job.WorkerId))PauseHarvestRequirementWork(s,job,
                    HarvestRequirementWorkStatus.Paused,HarvestRequirementPauseReason.WorkerUnavailable);
        }

        private void CreditHarvestRequirementWork(Snapshot s,RuleTime elapsed)
        {
            if(!harvestPreservationEnabled||elapsed==default)return;
            RuleTime start=SubtractHarvestRequirementTime(s.RuleClock,elapsed);
            foreach(var job in s.HarvestRequirementWorks.Where(x=>x.Status==HarvestRequirementWorkStatus.Working).ToArray()) {
                if(!s.Work.WorkerIntervals.Any(w=>w.JobId==job.Id&&w.Start<=start&&w.End>=s.RuleClock))continue;
                if(!HarvestPreservationRules.TryProject(s,job.InventoryLotId,out var view))
                    throw new InvalidOperationException("Harvest requirement lineage disappeared during work.");
                var unit=s.HarvestUnits.Single(x=>x.Id==view.HarvestUnitId);
                RuleTime boundary=unit.OriginAt.AddSeconds(unit.PreservationIntervalSeconds);
                if(start>=boundary||s.RuleClock>boundary)
                    throw new InvalidOperationException("Fresh-required work crossed its scheduled preservation boundary.");
                ActiveWorkProgress progress=job.Work.Credit(elapsed);
                if(s.RuleClock==boundary)
                    PauseHarvestRequirementWork(s,job,HarvestRequirementWorkStatus.Paused,
                        HarvestRequirementPauseReason.IngredientNotFresh,progress);
                else ReplaceHarvestRequirementWork(s,job.With(s.RuleClock,progress,HarvestRequirementWorkStatus.Working,
                    HarvestRequirementPauseReason.None));
            }
        }

        private string ResolveHarvestRequirementWork(Snapshot s,Command c)
        {
            string failure=AssessHarvestRequirementWork(s,c,out var current,out var preservation);
            if(failure!=null)return failure;
            if(c.Kind==CommandKind.StartHarvestRequirementWork) {
                string id="harvest.requirement."+(s.Revision+1).ToString(CultureInfo.InvariantCulture);
                string reservation=id+".ingredient";
                var progress=new ActiveWorkProgress(new[]{HarvestRequirementDuration(s,c.Target)});
                current=new HarvestRequirementWorkRecord(id,c.Actor,c.Target,reservation,c.Inventory.Amount,
                    HarvestIngredientRequirement.Fresh,HarvestRequirementWorkStatus.Working,
                    HarvestRequirementPauseReason.None,s.RuleClock,s.RuleClock,progress);
                s.Work=s.Work.Reserve(id,Array.Empty<WorkerInterval>(),new[]{new ResourceReservation(reservation,id,c.Target,c.Inventory.Amount)});
                BookHarvestRequirementWork(s,current);
                s.HarvestRequirementWorks=s.HarvestRequirementWorks.Concat(new[]{current}).ToArray();
                return null;
            }
            if(c.Kind==CommandKind.PauseHarvestRequirementWork) {
                PauseHarvestRequirementWork(s,current,HarvestRequirementWorkStatus.Paused,
                    HarvestRequirementPauseReason.Explicit);return null;
            }
            BookHarvestRequirementWork(s,current);
            ReplaceHarvestRequirementWork(s,current.With(s.RuleClock,current.Work,
                HarvestRequirementWorkStatus.Working,HarvestRequirementPauseReason.None));
            return null;
        }
    }
}
#endif
