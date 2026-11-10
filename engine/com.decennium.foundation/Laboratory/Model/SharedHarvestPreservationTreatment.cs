#if DECENNIUM_TEST_ONLY && (UNITY_EDITOR || DEVELOPMENT_BUILD || HEADLESS_TESTS)
using System;
using System.Globalization;
using System.Linq;
using System.Numerics;

namespace Decennium.Foundation.Laboratory
{
    internal static class HarvestPreservationTreatmentFixture
    {
        internal const string SkillId="cooking";
        internal const string ToolId="TEST_ONLY.preservation.cooks-utensils";
        internal const string ToolProfileId="TEST_ONLY.cooking-utensils";
        internal const string ContainerId="TEST_ONLY.preservation.sealable-vessel";
        internal const string ContainerProfileId="TEST_ONLY.preservation-vessel";
        internal const string SupplyLotId="TEST_ONLY.preservation.supply-half-pound";
        internal const string FitRuleId="TEST_ONLY.preservation-vessel-fit-v1";
        internal const string ContainerMassBinding="fixture-container-1lb";
        internal const string ContainerCapacityBinding="fixture-capacity-10lb";
        internal const string ToolMassBinding="unmodeled-source-mass";

        internal static void Initialize(Snapshot s,string worker,string site,int siteX,int siteY,string fishLotId)
        {
            if(s.SchemaVersion!=Snapshot.HarvestPreservationTreatmentSchema||!s.TestOnly
                ||!s.WorldSchedule.Order.Contains(worker)||s.PortableEquipment.Any(x=>x.Id==ContainerId||x.Id==ToolId||x.Id==SupplyLotId)
                ||s.Work.Lots.Any(x=>x.Id==SupplyLotId)||s.InventoryLots.Any(x=>x.LotId==SupplyLotId))
                throw new ArgumentException("MGT-05B requires a clean schema75 TEST_ONLY harvest profile.");

            var training=s.SkillTraining.SingleOrDefault(x=>x.ActorId==worker&&x.SkillId==SkillId);
            if(training!=null&&training.ProficiencyRank!=1)
                throw new ArgumentException("MGT-05B fixture binds Cooking proficiency rank1.");
            if(training==null)s.SkillTraining=s.SkillTraining.Concat(new[]{new SkillTrainingRecord(worker,SkillId,1)}).ToArray();

            RuleQuantity supplies=HarvestPreservationTreatmentValidation.SupplyAmount;
            s.Work=new WorkLedger(s.Work.Lots.Concat(new[]{new ResourceLot(SupplyLotId,SharedHarvestFixture.MaterialUnit,
                supplies,worker,worker)}),s.Work.WorkerIntervals,s.Work.Reservations);
            s.InventoryLots=s.InventoryLots.Concat(new[]{new InventoryLotRecord(SupplyLotId,"",worker,supplies,s.RuleClock,
                NutritionKind.None,null,InventoryAccess.Ready)}).ToArray();
            PortableEquipmentRules.RegisterInventoryLot(s,SupplyLotId,worker,worker);

            // The vessel's mass, load, capacity and authored exact-fit membership are synthetic
            // fixture facts. They are not production equipment catalogue entries.
            s.PortableEquipment=s.PortableEquipment.Concat(new[]{
                new PortableEquipmentRecord(ToolId,ToolProfileId,worker,worker,"",PortablePlacement.Ground,
                    PortableLinkKind.None,"",PortableMassBasis.Unmodeled,null,null,groundX:siteX,groundY:siteY),
                new PortableEquipmentRecord(ContainerId,ContainerProfileId,worker,worker,"",PortablePlacement.Ground,
                    PortableLinkKind.None,"",PortableMassBasis.Fixed,new RuleQuantity(1),new RuleQuantity(1),
                    capacityPounds:new RuleQuantity(10),capacityCubicFeet:new RuleQuantity(1),open:true,
                    fitRuleId:FitRuleId,fitMemberIds:new[]{fishLotId,SupplyLotId},groundX:siteX,groundY:siteY)
            }).ToArray();
            PortableEquipmentRules.SynchronizeLinks(s);
        }

        internal static string Validate(Snapshot s,string worker,string site,int siteX,int siteY,string fishLotId)
        {
            if(s.SchemaVersion!=Snapshot.HarvestPreservationTreatmentSchema||!s.TestOnly
                ||s.SkillTraining.Count(x=>x.ActorId==worker&&x.SkillId==SkillId&&x.ProficiencyRank==1)!=1
                ||s.SkillTraining.Any(x=>x.ActorId==worker&&x.SkillId==SkillId&&x.ProficiencyRank!=1))
                return "HarvestTreatmentCookingBindingMismatch";
            var supply=s.InventoryLots.SingleOrDefault(x=>x.LotId==SupplyLotId);
            var supplyLot=s.Work.Lots.SingleOrDefault(x=>x.Id==SupplyLotId);
            var physicalSupply=s.PortableEquipment.SingleOrDefault(x=>x.Id==SupplyLotId&&x.LinkedId==SupplyLotId
                &&x.LinkKind==PortableLinkKind.InventoryLot&&x.MassBasis==PortableMassBasis.GenericPounds);
            var tool=s.PortableEquipment.SingleOrDefault(x=>x.Id==ToolId);
            var container=s.PortableEquipment.SingleOrDefault(x=>x.Id==ContainerId);
            bool supplyInsideTreatmentVessel=physicalSupply!=null&&physicalSupply.ParentId==ContainerId;
            bool supplyCustodyMatchesPhysical=physicalSupply!=null&&supplyLot!=null
                &&supplyLot.CustodianId==physicalSupply.CustodianId
                &&(supplyInsideTreatmentVessel
                    ?container!=null&&physicalSupply.Placement==PortablePlacement.Contained
                        &&physicalSupply.CustodianId==container.CustodianId
                    :physicalSupply.ParentId==""&&physicalSupply.CustodianId==worker);
            if(supply==null||supplyLot==null||physicalSupply==null||supply.OwnerId!=worker
                ||physicalSupply.OwnerId!=worker||!supplyCustodyMatchesPhysical
                ||supply.CreatedAmount!=HarvestPreservationTreatmentValidation.SupplyAmount||supply.Nutrition!=NutritionKind.None
                ||supply.FreshUntil.HasValue||supplyLot.UnitId!=SharedHarvestFixture.MaterialUnit
                ||supplyLot.Amount>HarvestPreservationTreatmentValidation.SupplyAmount
                ||tool==null||tool.ProfileId!=ToolProfileId||tool.OwnerId!=worker||tool.MassBasis!=PortableMassBasis.Unmodeled
                ||tool.SourceWeightLb.HasValue||tool.OperationalWeightLb.HasValue
                ||container==null||container.ProfileId!=ContainerProfileId||container.OwnerId!=worker
                ||container.MassBasis!=PortableMassBasis.Fixed||container.SourceWeightLb!=new RuleQuantity(1)
                ||container.OperationalWeightLb!=new RuleQuantity(1)||container.CapacityPounds!=new RuleQuantity(10)
                ||container.CapacityCubicFeet!=new RuleQuantity(1)||container.FitRuleId!=FitRuleId
                ||!container.FitMemberIds.OrderBy(x=>x,StringComparer.Ordinal)
                    .SequenceEqual(new[]{fishLotId,SupplyLotId}.OrderBy(x=>x,StringComparer.Ordinal)))
                return "HarvestTreatmentPhysicalFixtureMismatch";
            if(s.HarvestPreservationTreatmentAttempts.Any(x=>x.WorkerId!=worker||x.SkillId!=SkillId
                ||x.ToolId!=ToolId||x.ContainerId!=ContainerId||x.SupplyLotId!=SupplyLotId))
                return "HarvestTreatmentAttemptFixtureMismatch";
            RuleQuantity expectedSupply=s.HarvestPreservationTreatmentAttempts.Any(x=>
                x.Status!=HarvestPreservationTreatmentStatus.Working)?default:HarvestPreservationTreatmentValidation.SupplyAmount;
            if(supplyLot.Amount!=expectedSupply)return "HarvestTreatmentSupplySettlementMismatch";
            return null;
        }
    }

    public sealed partial class TestOnlySharedWorldPolicy
    {
        private static bool HarvestPreservationTreatmentCommand(CommandKind kind)
            =>kind==CommandKind.StartHarvestPreservationTreatment;

        private static bool PortableInside(Snapshot s,string ancestorId,string itemId)
        {
            var current=s.PortableEquipment.SingleOrDefault(x=>x.Id==itemId);
            var seen=new System.Collections.Generic.HashSet<string>(StringComparer.Ordinal);
            while(current!=null) {
                if(current.Id==ancestorId)return true;
                if(current.ParentId==""||!seen.Add(current.ParentId))return false;
                current=s.PortableEquipment.SingleOrDefault(x=>x.Id==current.ParentId);
            }
            return false;
        }

        private string HarvestPreservationTreatmentPortableHandlingFailure(Snapshot s,Command c)
        {
            if(!harvestPreservationTreatmentEnabled)return null;
            var item=s.PortableEquipment.SingleOrDefault(x=>x.Id==c.Target);if(item==null)return null;
            var active=s.HarvestPreservationTreatmentAttempts.Where(x=>x.Status==HarvestPreservationTreatmentStatus.Success
                &&x.CompletedAt.HasValue&&x.CompletedAt.Value<=s.RuleClock
                &&s.RuleClock<x.CompletedAt.Value.AddSeconds(HarvestPreservationTreatmentValidation.ProtectionSeconds))
                .FirstOrDefault(x=>PortableInside(s,x.ContainerId,item.Id));
            if(active!=null) {
                bool wholeVesselMove=item.Id==active.ContainerId&&!item.Open
                    &&c.Kind==CommandKind.HandlePortableEquipment&&c.Inventory!=null
                    &&(c.Inventory.Handling==HandlingKind.Pickup||c.Inventory.Handling==HandlingKind.Drop
                        ||c.Inventory.Handling==HandlingKind.Retrieve||c.Inventory.Handling==HandlingKind.Stow
                        ||c.Inventory.Handling==HandlingKind.Handover);
                if(!wholeVesselMove)return "HarvestTreatmentProtectionActive";
            }
            var working=s.HarvestPreservationTreatmentAttempts.SingleOrDefault(x=>x.Status==HarvestPreservationTreatmentStatus.Working
                &&(x.ContainerId==item.Id||x.InventoryLotId==item.Id||x.SupplyLotId==item.Id||x.ToolId==item.Id
                    ||PortableInside(s,x.ContainerId,item.Id)));
            return working==null?null:"HarvestTreatmentInputsInUse";
        }

        private void InitializeHarvestPreservationTreatmentFixture(Snapshot s)
        {
            if(!harvestPreservationTreatmentEnabled)return;
            HarvestPreservationTreatmentFixture.Initialize(s,TestOnlyPolicy.ActorId,HarvestSiteId,HarvestSiteX,HarvestSiteY,
                HarvestFiniteLotId);
        }

        private string ValidateHarvestPreservationTreatmentFixture(Snapshot s)
            =>!harvestPreservationTreatmentEnabled?s.HarvestPreservationTreatmentAttempts.Length==0?null:"HarvestTreatmentFixtureNotSelected"
                :HarvestPreservationTreatmentFixture.Validate(s,TestOnlyPolicy.ActorId,HarvestSiteId,HarvestSiteX,HarvestSiteY,
                    HarvestFiniteLotId);

        private static HarvestPreservationTreatmentAttemptRecord ReplaceHarvestPreservationTreatment(
            Snapshot s,HarvestPreservationTreatmentAttemptRecord value)
        {
            s.HarvestPreservationTreatmentAttempts=s.HarvestPreservationTreatmentAttempts.Select(x=>x.Id==value.Id?value:x).ToArray();
            return value;
        }

        private static RuleTime? NextHarvestPreservationTreatmentBoundary(Snapshot s)
        {
            RuleTime? next=null;
            foreach(var attempt in s.HarvestPreservationTreatmentAttempts.Where(x=>x.Status==HarvestPreservationTreatmentStatus.Working)) {
                var interval=s.Work.WorkerIntervals.Single(w=>w.JobId==attempt.Id&&w.Start<=s.RuleClock&&w.End>s.RuleClock);
                if(!next.HasValue||interval.End<next.Value)next=interval.End;
            }
            return next;
        }

        private string AssessHarvestPreservationTreatment(Snapshot s,Command c,
            out HarvestPreservationTreatmentAttemptRecord current,out HarvestPreservationView preservation)
        {
            current=null;preservation=null;
            if(!harvestPreservationTreatmentEnabled||s.SchemaVersion!=Snapshot.HarvestPreservationTreatmentSchema)
                return "HarvestPreservationTreatmentNotSelected";
            if(c.Kind!=CommandKind.StartHarvestPreservationTreatment||c.Inventory==null||c.Target==""
                ||c.Inventory.Amount==default||c.Inventory.Destination!=""||c.Inventory.Handling!=HandlingKind.Pickup
                ||c.X!=0||c.Y!=0||c.Combat!=null||c.Advancement!=null||c.Ranged!=null
                ||c.OverwatchRider!=OverwatchRider.None||c.SuppressionFire!=null||c.DefensiveFormation!=null
                ||c.ExpeditionAssignment!=null||c.HarvestSelection!=null||c.MiningSelection!=null
                ||c.ProspectingExposure!=null||c.RouteMappingWork!=null)
                return "InvalidHarvestPreservationTreatmentCommand";
            if(s.InventoryCombat)return "HarvestTreatmentDuringCombatUnsupported";
            if(s.HarvestPreservationTreatmentAttempts.Length!=0)return "HarvestTreatmentAlreadyAttempted";
            if(!s.WorldSchedule.Order.Contains(c.Actor))return "HarvestTreatmentRequiresScheduledWorker";
            if(c.Actor!=TestOnlyPolicy.ActorId)return "HarvestTreatmentWorkerUnsupported";
            var training=s.SkillTraining.SingleOrDefault(x=>x.ActorId==c.Actor&&x.SkillId==HarvestPreservationTreatmentFixture.SkillId);
            if(training==null||training.ProficiencyRank!=1)return "HarvestTreatmentCookingTrainingRequired";
            if(!HarvestPreservationRules.TryProject(s,c.Target,out preservation))return "HarvestTreatmentNeedsHarvestedMass";
            if(preservation.State==HarvestPreservationState.Spoiled)return "HarvestTreatmentCannotRescueSpoiledMaterial";
            var target=s.InventoryLots.Single(x=>x.LotId==c.Target);
            var resource=s.Work.Lots.Single(x=>x.Id==c.Target);
            if(resource.UnitId!=SharedHarvestFixture.MaterialUnit||resource.Amount<=default(RuleQuantity)
                ||resource.Amount>new RuleQuantity(10)||c.Inventory.Amount!=resource.Amount
                ||s.Work.AvailableAmount(c.Target)!=resource.Amount)
                return "HarvestTreatmentRequiresWholeAvailableLotUnderTenPounds";
            RuleTime finish=s.RuleClock.AddSeconds(HarvestPreservationTreatmentValidation.WorkSeconds);
            if(!HarvestPreservationRules.TryProjectAt(s,c.Target,finish,out var atFinish)
                ||atFinish.State==HarvestPreservationState.Spoiled)
                return "HarvestTreatmentCannotFinishBeforeSpoilage";

            var targetPhysical=s.PortableEquipment.SingleOrDefault(x=>x.Id==target.LotId&&x.LinkKind==PortableLinkKind.InventoryLot
                &&x.LinkedId==target.LotId&&x.MassBasis==PortableMassBasis.GenericPounds);
            var supply=s.PortableEquipment.SingleOrDefault(x=>x.Id==HarvestPreservationTreatmentFixture.SupplyLotId
                &&x.LinkKind==PortableLinkKind.InventoryLot&&x.LinkedId==HarvestPreservationTreatmentFixture.SupplyLotId
                &&x.MassBasis==PortableMassBasis.GenericPounds);
            var container=s.PortableEquipment.SingleOrDefault(x=>x.Id==HarvestPreservationTreatmentFixture.ContainerId);
            var tool=s.PortableEquipment.SingleOrDefault(x=>x.Id==HarvestPreservationTreatmentFixture.ToolId);
            if(targetPhysical==null||supply==null||container==null||tool==null||!container.Open
                ||targetPhysical.ParentId!=container.Id||supply.ParentId!=container.Id
                ||!PortableEquipmentValidation.FitsAuthoredMember(s,container,targetPhysical)
                ||!PortableEquipmentValidation.FitsAuthoredMember(s,container,supply)
                ||!container.CapacityPounds.HasValue
                ||PortableEquipmentValidation.Mass(s,targetPhysical)+PortableEquipmentValidation.Mass(s,supply)>container.CapacityPounds.Value)
                return "HarvestTreatmentContainerFitNotEstablished";
            if(s.Work.AvailableAmount(HarvestPreservationTreatmentFixture.SupplyLotId)
                !=HarvestPreservationTreatmentValidation.SupplyAmount)return "HarvestTreatmentSupplyUnavailable";
            if(!PortableEquipmentRules.Accessible(s,c.Actor,targetPhysical)
                ||!PortableEquipmentRules.Accessible(s,c.Actor,supply)
                ||!PortableEquipmentRules.Accessible(s,c.Actor,container)
                ||!PortableEquipmentRules.Accessible(s,c.Actor,tool))return "HarvestTreatmentEquipmentOutOfReach";
            if(PortableEquipmentRules.HasPendingClaim(s,targetPhysical)||PortableEquipmentRules.HasPendingClaim(s,supply)
                ||PortableEquipmentRules.HasPendingClaim(s,container)||PortableEquipmentRules.HasPendingClaim(s,tool))
                return "HarvestTreatmentEquipmentAlreadyReserved";
            if(OrdinaryInventory.Busy(s,c.Actor)||!CapableWorker(s,c.Actor))return "HarvestTreatmentWorkerUnavailable";
            var check=AbilityCheckRules.Derive(s,c.Actor,HarvestPreservationTreatmentFixture.SkillId,CharacterAbility.Wisdom);
            if(check.ProficiencyRank!=1)return "HarvestTreatmentCookingTrainingRequired";
            current=null;
            return null;
        }

        private string ResolveHarvestPreservationTreatment(Snapshot s,Command c)
        {
            string error=AssessHarvestPreservationTreatment(s,c,out _,out _);if(error!=null)return error;
            string id="harvest.preservation."+(s.Revision+1).ToString(CultureInfo.InvariantCulture);
            string targetReservation=id+".target",supplyReservation=id+".supply";
            RuleTime end=s.RuleClock.AddSeconds(HarvestPreservationTreatmentValidation.WorkSeconds);
            var work=new ActiveWorkProgress(new[]{new RuleTime(HarvestPreservationTreatmentValidation.WorkSeconds)});
            s.Work=s.Work.Reserve(id,new[]{new WorkerInterval(id+".labor",id,c.Actor,s.RuleClock,end)},new[]{
                new ResourceReservation(targetReservation,id,c.Target,c.Inventory.Amount),
                new ResourceReservation(supplyReservation,id,HarvestPreservationTreatmentFixture.SupplyLotId,
                    HarvestPreservationTreatmentValidation.SupplyAmount)
            });
            var attempt=new HarvestPreservationTreatmentAttemptRecord(id,c.Actor,HarvestPreservationTreatmentFixture.SkillId,
                c.Target,c.Inventory.Amount,HarvestPreservationTreatmentFixture.ContainerId,
                HarvestPreservationTreatmentFixture.ToolId,HarvestPreservationTreatmentFixture.SupplyLotId,
                targetReservation,supplyReservation,s.RuleClock,s.RuleClock,work,HarvestPreservationTreatmentStatus.Working);
            s.HarvestPreservationTreatmentAttempts=s.HarvestPreservationTreatmentAttempts.Concat(new[]{attempt}).ToArray();
            return null;
        }

        private void CreditHarvestPreservationTreatment(Snapshot s,RuleTime elapsed)
        {
            if(!harvestPreservationTreatmentEnabled||elapsed==default)return;
            var previousValue=new RuleQuantity(s.RuleClock.Numerator,s.RuleClock.Denominator)
                -new RuleQuantity(elapsed.Numerator,elapsed.Denominator);
            RuleTime previous=new RuleTime(previousValue.Numerator,previousValue.Denominator);
            foreach(var attempt in s.HarvestPreservationTreatmentAttempts
                .Where(x=>x.Status==HarvestPreservationTreatmentStatus.Working).ToArray()) {
                var interval=s.Work.WorkerIntervals.Single(x=>x.JobId==attempt.Id);
                if(interval.Start>previous||interval.End<s.RuleClock)continue;
                if(elapsed>attempt.Work.Remaining)throw new InvalidOperationException("Harvest treatment work crossed its terminal boundary.");
                var progress=attempt.Work.Credit(elapsed);
                if(!progress.Complete) {
                    ReplaceHarvestPreservationTreatment(s,attempt.WithProgress(s.RuleClock,progress));
                    continue;
                }
                if(!HarvestPreservationRules.TryProjectAt(s,attempt.InventoryLotId,s.RuleClock,out var atFinish)
                    ||atFinish.State==HarvestPreservationState.Spoiled)
                    throw new InvalidOperationException("Harvest treatment reached its deadline after the material Spoiled.");
                var modifier=AbilityCheckRules.Derive(s,attempt.WorkerId,attempt.SkillId,CharacterAbility.Wisdom);
                uint randomBefore=s.RandomState;RuleD20Roll roll=RuleDice.RollD20(randomBefore);
                RuleTaskCheckResult outcome=RuleResolution.TaskCheck(roll.Natural,modifier.Total,
                    HarvestPreservationTreatmentValidation.DifficultyClass);
                s.RandomState=roll.NextRandomState;
                var status=outcome.Degree==RuleTaskDegree.Success||outcome.Degree==RuleTaskDegree.CriticalSuccess
                    ?HarvestPreservationTreatmentStatus.Success:HarvestPreservationTreatmentStatus.Failure;
                s.Work=s.Work.Consume(attempt.Id,attempt.SupplyReservationId);
                s.Work=s.Work.Release(attempt.Id,attempt.TargetReservationId);
                if(status==HarvestPreservationTreatmentStatus.Success) {
                    var container=s.PortableEquipment.Single(x=>x.Id==attempt.ContainerId);
                    if(!container.Open)throw new InvalidOperationException("Preservation vessel lost its open treatment state.");
                    s.PortableEquipment=s.PortableEquipment.Select(x=>x.Id==container.Id?x.With(open:false):x).ToArray();
                }
                ReplaceHarvestPreservationTreatment(s,attempt.Complete(s.RuleClock,progress,status,
                    modifier.AbilityModifier,modifier.ProficiencyRank,modifier.ProficiencyBonus,roll.Natural,
                    (HarvestPreservationTreatmentDegree)((int)outcome.Degree+1),randomBefore,roll.NextRandomState,roll.WordsConsumed));
            }
        }
    }
}
#endif
