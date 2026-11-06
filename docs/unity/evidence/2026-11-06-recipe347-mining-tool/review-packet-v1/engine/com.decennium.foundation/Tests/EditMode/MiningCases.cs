#if DECENNIUM_TEST_ONLY && (UNITY_EDITOR || HEADLESS_TESTS)
using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text;
using Decennium.Foundation.Laboratory;

namespace Decennium.Foundation.Tests
{
    public static partial class FoundationCases
    {
        private const string MiningWorker = SharedMiningFixture.OwnerId;

        private static Command MiningCommand(Simulation simulation,CommandKind kind,string target="",MiningSelectionRequest selection=null,
            string actor=MiningWorker,string commandId=null)
        {
            var state=simulation.Capture();
            return new Command(commandId??"mining.command."+(state.Revision+1),actor,state.Revision,kind,target,miningSelection:selection);
        }

        private static void MiningCommit(Simulation simulation,Command command)
        {
            var result=simulation.Execute(TestOnlySharedWorldPolicy.Host(),command);
            Require(result.Outcome==Outcome.Committed,command.Kind+" rejected: "+result.Code);
        }

        private static MiningSelectionRequest MiningSelection(params string[] categories)
            =>new MiningSelectionRequest(SharedMiningFixture.DepositVersionId,categories,MiningAbilityChoice.Wisdom);

        private static int MiningModifier(Snapshot state)
        {
            var worker=state.Characters.Single(x=>x.ActorId==MiningWorker);
            var training=state.SkillTraining.SingleOrDefault(x=>x.ActorId==MiningWorker&&x.SkillId=="mining-tools");
            return checked(PlaytestCharacters.AbilityModifier(worker.Abilities[4])
                +(training==null?0:PlaytestCharacters.ProficiencyBonus(worker.Levels.Count)*(training.ProficiencyRank==2?2:1)));
        }

        private static int MiningHurryFlagOffset(byte[] bytes)
        {
            byte[] text=Encoding.UTF8.GetBytes(SharedMiningFixture.DepositId);
            byte[] needle=BitConverter.GetBytes(text.Length).Concat(text).ToArray();
            int offset=-1;
            for(int i=0;i<=bytes.Length-needle.Length;i++) {
                bool match=true;for(int j=0;j<needle.Length;j++)if(bytes[i+j]!=needle[j]){match=false;break;}
                if(match){offset=i;break;}
            }
            if(offset<0)throw new Exception("Mining deposit was not found in encoded fixture.");
            using(var stream=new MemoryStream(bytes,false))using(var reader=new BinaryReader(stream,Encoding.UTF8,true)) {
                stream.Position=offset;
                void SkipText(){int length=reader.ReadInt32();if(length<0||length>512)throw new Exception("Invalid encoded mining text.");stream.Position+=length;}
                SkipText();SkipText();SkipText();SkipText();reader.ReadInt32();reader.ReadInt32();
                SkipText();SkipText();SkipText();SkipText();
                byte hasDc=reader.ReadByte();if(hasDc>1)throw new Exception("Invalid encoded DC presence flag.");
                if(hasDc==1)reader.ReadInt32();
                return checked((int)stream.Position);
            }
        }

        private static uint MiningSeedFor(TaskDegree degree,int modifier,bool disadvantage=false,int dc=12)
        {
            for(uint seed=1;seed<1000000;seed++)
                if(PlaytestRolls.TaskCheck(PlaytestDice.RollD20(seed,disadvantageSources:disadvantage?1:0).Natural,modifier,dc).Degree==degree)
                    return seed;
            throw new Exception("No deterministic mining check seed for "+degree+".");
        }

        private static MiningDepositFixtureContent AuthoredMiningDeposit(string key,string material,int tier,int x,int y,
            RuleQuantity mass,RuleQuantity volume,long value)
        {
            string depositId="TEST_ONLY.mining."+key+".deposit",versionId=depositId+".v1",siteId="TEST_ONLY.mining."+key+".site";
            string categoryId="TEST_ONLY.mining."+key+".category",unitId="TEST_ONLY.mining."+key+".unit";
            string toolsId="TEST_ONLY.mining."+key+".tools",pickId="TEST_ONLY.mining."+key+".pick";
            string receiverId="TEST_ONLY.mining."+key+".receiver",surfaceId="TEST_ONLY.mining."+key+".surface";
            var deposit=new MiningDepositRecord(depositId,versionId,siteId,MiningWorker,x,y,toolsId,pickId,receiverId,surfaceId);
            var category=new MiningCategoryRecord(categoryId,depositId,material,tier,true,new[]{unitId});
            var unit=new MiningMaterialUnitRecord(unitId,depositId,categoryId,mass,volume,value,MiningUnitCondition.Intact,MiningUnitStatus.Available);
            var physical=new[]{
                new PortableEquipmentRecord(unitId,"TEST_ONLY.mining.raw-unit",MiningWorker,MiningWorker,"",PortablePlacement.Ground,
                    PortableLinkKind.InventoryLot,unitId,PortableMassBasis.GenericPounds,mass,null,groundX:x,groundY:y),
                MiningFixtureItem(toolsId,"TEST_ONLY.mining.screen-and-tray",MiningWorker,x,y,new RuleQuantity(3)),
                MiningFixtureItem(pickId,"TEST_ONLY.mining-pick",MiningWorker,x,y,new RuleQuantity(10)),
                new PortableEquipmentRecord(receiverId,"TEST_ONLY.mining.receiver."+key,MiningWorker,MiningWorker,"",PortablePlacement.Ground,
                    PortableLinkKind.None,"",PortableMassBasis.Fixed,new RuleQuantity(2),new RuleQuantity(2),capacityPounds:new RuleQuantity(50),
                    capacityCubicFeet:new RuleQuantity(2),open:true,fitRuleId:"TEST_ONLY.mining.fit."+key,fitMemberIds:new[]{unitId},groundX:x,groundY:y)};
            var surface=new ObjectStructureRecord(surfaceId,"TEST_ONLY.mining.work-surface."+key,MiningWorker,MiningWorker,siteId,
                ObjectMaterial.Stone,100,100,0,new RuleQuantity(20));
            return new MiningDepositFixtureContent(deposit,new[]{category},new[]{unit},physical,new[]{surface});
        }

        private static PortableEquipmentRecord MiningFixtureItem(string id,string profile,string owner,int x,int y,RuleQuantity mass)
            =>new PortableEquipmentRecord(id,profile,owner,owner,"",PortablePlacement.Ground,PortableLinkKind.None,"",PortableMassBasis.Fixed,
                mass,mass,groundX:x,groundY:y);

        private sealed class MiningToolScenario
        {
            public SharedMiningFixture Fixture;
            public MiningDepositFixtureContent Content;
            public MiningToolCandidateProfileRecord Profile;
            public string TargetId,DamagedId,ReserveId,TargetCategoryId,DamagedCategoryId,ReserveCategoryId,ToolItemId;
        }

        private static MiningToolScenario Recipe347MiningScenario(bool includeToolItem=true,bool broken=false,
            bool missingPrimary=false,bool suppressed=false,bool melded=false,bool misplaced=false)
        {
            const string key="recipe347";
            string depositId="TEST_ONLY.mining."+key+".deposit",versionId=depositId+".v1",siteId="TEST_ONLY.mining."+key+".site";
            string targetCategoryId="TEST_ONLY.mining."+key+".target-category";
            string damagedCategoryId="TEST_ONLY.mining."+key+".damaged-category";
            string reserveCategoryId="TEST_ONLY.mining."+key+".reserve-category";
            string targetId="TEST_ONLY.mining."+key+".target";
            string damagedId="TEST_ONLY.mining."+key+".damaged";
            string reserveId="TEST_ONLY.mining."+key+".reserve";
            string toolsId="TEST_ONLY.mining."+key+".ordinary-tools",pickId="TEST_ONLY.mining."+key+".pick";
            string receiverId="TEST_ONLY.mining."+key+".receiver",surfaceId="TEST_ONLY.mining."+key+".surface";
            string toolItemId="TEST_ONLY.mining."+key+".candidate-item",structureId="TEST_ONLY.mining."+key+".candidate-structure";
            int x=3,y=3;var owner=MiningWorker;
            var deposit=new MiningDepositRecord(depositId,versionId,siteId,owner,x,y,toolsId,pickId,receiverId,surfaceId);
            var categories=new[]{
                new MiningCategoryRecord(targetCategoryId,depositId,"TEST_ONLY.mineral.recipe347-target",1,true,new[]{targetId}),
                new MiningCategoryRecord(damagedCategoryId,depositId,"TEST_ONLY.mineral.recipe347-damaged",1,true,new[]{damagedId}),
                new MiningCategoryRecord(reserveCategoryId,depositId,"TEST_ONLY.mineral.recipe347-reserve",1,true,new[]{reserveId})};
            var units=new[]{
                new MiningMaterialUnitRecord(targetId,depositId,targetCategoryId,new RuleQuantity(1,2),new RuleQuantity(1,100),30,
                    MiningUnitCondition.Intact,MiningUnitStatus.Available),
                new MiningMaterialUnitRecord(damagedId,depositId,damagedCategoryId,new RuleQuantity(1,2),new RuleQuantity(1,100),10,
                    MiningUnitCondition.DamagedPotentiallyRecoverable,MiningUnitStatus.Available),
                new MiningMaterialUnitRecord(reserveId,depositId,reserveCategoryId,new RuleQuantity(1,2),new RuleQuantity(1,100),5,
                    MiningUnitCondition.Intact,MiningUnitStatus.Available)};
            PortableEquipmentRecord unitItem(MiningMaterialUnitRecord unit)=>new PortableEquipmentRecord(unit.Id,"TEST_ONLY.mining.raw-unit",
                owner,owner,"",PortablePlacement.Ground,PortableLinkKind.InventoryLot,unit.Id,PortableMassBasis.GenericPounds,
                unit.MassPounds,null,groundX:x,groundY:y);
            var physicalItems=new List<PortableEquipmentRecord>{
                unitItem(units[0]),unitItem(units[1]),unitItem(units[2]),
                MiningFixtureItem(toolsId,"TEST_ONLY.mining.screen-and-tray",owner,x,y,new RuleQuantity(3)),
                MiningFixtureItem(pickId,"TEST_ONLY.mining-pick",owner,x,y,new RuleQuantity(10)),
                new PortableEquipmentRecord(receiverId,"TEST_ONLY.mining.recipe347-receiver",owner,owner,"",PortablePlacement.Ground,
                    PortableLinkKind.None,"",PortableMassBasis.Fixed,new RuleQuantity(2),new RuleQuantity(2),
                    capacityPounds:new RuleQuantity(50),capacityCubicFeet:new RuleQuantity(2),open:true,
                    fitRuleId:"TEST_ONLY.mining.recipe347-fit",fitMemberIds:units.Select(z=>z.Id).ToArray(),groundX:x,groundY:y)};
            var surface=new ObjectStructureRecord(surfaceId,"TEST_ONLY.mining.recipe347-surface",owner,owner,siteId,
                ObjectMaterial.Stone,100,100,0,new RuleQuantity(20));
            var content=new MiningDepositFixtureContent(deposit,categories,units,physicalItems.ToArray(),new[]{surface});
            var preparation=new MineralPreparationProfileRecord("TEST_ONLY.mining.recipe347-preparation",targetId,
                new RuleQuantity(1,10),"TEST_ONLY.mining.recipe347-dressed","TEST_ONLY.mining.recipe347-gangue");
            var profile=new MiningToolCandidateProfileRecord("TEST_ONLY.mining.recipe347-profile",depositId,toolItemId,
                "TEST_ONLY.mining.recipe347-tool",structureId,"TEST_ONLY.mining.recipe347-structure",preparation.Id,targetId,reserveId);
            string[] missing=missingPrimary?new[]{profile.RequiredMemberIds[0]}:Array.Empty<string>();
            var instance=new MiningToolInstanceStateRecord(profile.Id,toolItemId,missing,suppressed,melded);
            var structure=new ObjectStructureRecord(structureId,profile.StructureProfileId,owner,owner,siteId,ObjectMaterial.WoodLeather,
                MiningToolCandidateProfileRecord.MaximumHp,broken?0:MiningToolCandidateProfileRecord.MaximumHp,0,
                MiningToolCandidateProfileRecord.EmptyMassPounds);
            var candidateItems=includeToolItem?new[]{new PortableEquipmentRecord(toolItemId,profile.ToolItemProfileId,owner,owner,"",
                PortablePlacement.Ground,PortableLinkKind.None,"",PortableMassBasis.Fixed,MiningToolCandidateProfileRecord.EmptyMassPounds,
                MiningToolCandidateProfileRecord.EmptyMassPounds,groundX:misplaced?x+2:x,groundY:y)}:Array.Empty<PortableEquipmentRecord>();
            var fixture=new SharedMiningFixture(new[]{content},mineralPreparationProfiles:new[]{preparation},
                miningToolCandidateProfiles:new[]{profile},miningToolInstanceStates:new[]{instance},miningToolStructures:new[]{structure},
                miningToolItems:candidateItems);
            return new MiningToolScenario{Fixture=fixture,Content=content,Profile=profile,TargetId=targetId,DamagedId=damagedId,
                ReserveId=reserveId,TargetCategoryId=targetCategoryId,DamagedCategoryId=damagedCategoryId,
                ReserveCategoryId=reserveCategoryId,ToolItemId=toolItemId};
        }

        private static void AddMiningCases(Dictionary<string,Action> cases,string directory)
        {
            var host=TestOnlySharedWorldPolicy.Host();
            cases.Add("recipe347_mining_tool_applies_check_reserve_and_integrated_dressing_through_shared_extraction",()=>{
                var scenario=Recipe347MiningScenario();var selection=new MiningSelectionRequest(scenario.Content.Deposit.VersionId,
                    new[]{scenario.TargetCategoryId,scenario.DamagedCategoryId},MiningAbilityChoice.Wisdom,false,"",scenario.DamagedId);
                var unseeded=TestOnlySharedWorldPolicy.WithMining(scenario.Fixture);
                int baseModifier=MiningModifier(unseeded.Initial());
                var initial=unseeded.Initial();
                Require(initial.SchemaVersion==Snapshot.MiningToolCandidateSchema
                    &&MiningToolCandidateRules.PhysicallyEligible(initial,scenario.Profile,
                        initial.MiningToolInstanceStates.Single(x=>x.ProfileId==scenario.Profile.Id),MiningWorker,
                        new[]{scenario.TargetId,scenario.DamagedId,scenario.ReserveId}),
                    "The authored recipe-347 body and three actual candidate units were not physically eligible.");
                uint seed=MiningSeedFor(TaskDegree.CriticalSuccess,baseModifier+MiningToolCandidateProfileRecord.CheckBonus,dc:12);
                var policy=TestOnlySharedWorldPolicy.WithMining(scenario.Fixture,seed);var simulation=World(policy);
                var start=MiningCommand(simulation,CommandKind.StartMining,scenario.Content.Deposit.Id,selection);
                MiningCommit(simulation,start);
                var booked=simulation.Capture();var use=booked.MiningToolUses.Single();var bookedAttempt=booked.MiningAttempts.Single();
                Require(bookedAttempt.DurationSeconds==2400&&bookedAttempt.SetupSeconds==200&&bookedAttempt.RemovalSeconds==2000
                    &&bookedAttempt.SortingSeconds==200&&use.PreparedUnitId==scenario.TargetId&&use.ReservedUnitId==scenario.ReserveId
                    &&booked.Work.Reservations.Single(x=>x.Id==MiningIds.ToolReserveReservation(use.MiningAttemptId)).Status==ReservationStatus.Reserved,
                    "The candidate changed the full extraction schedule or failed to bind the prepared baseline and distinct preclaimed reserve.");
                WorldAdvance(simulation,1800);
                var duringPreparation=simulation.Capture();use=duringPreparation.MiningToolUses.Single();
                Require(duringPreparation.MiningAttempts.Single().WorkDone==new RuleTime(1800)
                    &&use.ToolWorkDone==new RuleTime(1600)&&use.PreparationWorkDone==new RuleTime(200)
                    &&!use.PreparationCompletedAt.HasValue,
                    "Candidate participation or the final 600-second preparation interval was not credited from actual removal work.");
                byte[] partialSave=new SnapshotCodec().Encode(duringPreparation);
                simulation=new Simulation(policy,new SnapshotCodec().Decode(partialSave),ExecutionProfile.Laboratory);
                Require(partialSave.SequenceEqual(new SnapshotCodec().Encode(simulation.Capture())),
                    "A mid-preparation save changed the mining tool participation or reservation records.");
                WorldAdvance(simulation,400);
                var split=simulation.Capture();use=split.MiningToolUses.Single();
                var preparedUnit=split.MiningUnits.Single(x=>x.Id==scenario.TargetId);
                var retained=split.InventoryLots.Single(x=>x.LotId==use.RetainedLotId);
                var gangue=split.InventoryLots.Single(x=>x.LotId==use.GangueLotId);
                Require(split.RuleClock==new RuleTime(2200)&&split.MiningAttempts.Single().WorkDone==new RuleTime(2200)
                    &&use.ToolWorkDone==new RuleTime(2000)&&use.PreparationWorkDone==new RuleTime(600)
                    &&use.PreparationCompletedAt==new RuleTime(2200)&&split.Work.Lots.Single(x=>x.Id==scenario.TargetId).Amount==default(RuleQuantity)
                    &&retained.ParentId==scenario.TargetId&&retained.CreatedAmount==new RuleQuantity(2,5)
                    &&gangue.ParentId==scenario.TargetId&&gangue.CreatedAmount==new RuleQuantity(1,10)
                    &&retained.CreatedAmount+gangue.CreatedAmount==preparedUnit.MassPounds,
                    "The preparation split did not occur atomically at the end of removal or conserve source mass.");
                WorldAdvance(simulation,200);
                var completed=simulation.Capture();var attempt=completed.MiningAttempts.Single();use=completed.MiningToolUses.Single();
                var target=completed.MiningUnits.Single(x=>x.Id==scenario.TargetId);
                var recoveredDamaged=completed.MiningUnits.Single(x=>x.Id==scenario.DamagedId);
                var reserve=completed.MiningUnits.Single(x=>x.Id==scenario.ReserveId);
                var received=completed.Work.Lots.Single(x=>x.Id==use.RetainedLotId);
                var discarded=completed.Work.Lots.Single(x=>x.Id==use.GangueLotId);
                var body=completed.PortableEquipment.Single(x=>x.Id==scenario.TargetId);
                Require(attempt.DurationSeconds==2400&&attempt.SetupSeconds==200&&attempt.RemovalSeconds==2000
                    &&attempt.SortingSeconds==200&&attempt.Status==MiningAttemptStatus.CriticalSuccess
                    &&attempt.CheckModifier==baseModifier+MiningToolCandidateProfileRecord.CheckBonus
                    &&target.Status==MiningUnitStatus.Extracted&&target.ReceivedLotId==use.RetainedLotId
                    &&recoveredDamaged.Status==MiningUnitStatus.Extracted&&recoveredDamaged.ReceivedLotId==scenario.DamagedId
                    &&reserve.Status==MiningUnitStatus.Extracted&&reserve.ReceivedLotId==scenario.ReserveId
                    &&!attempt.SelectedUnitIds.Contains(scenario.ReserveId,StringComparer.Ordinal)
                    &&use.CheckBonusApplied&&use.CriticalReserveAwardedUnitId==scenario.ReserveId&&use.DressedBenefitAwarded
                    &&received.Amount==new RuleQuantity(2,5)&&received.LocationId==scenario.Content.Deposit.ReceiverId
                    &&discarded.Amount==new RuleQuantity(1,10)&&discarded.LocationId=="ground.3.3"
                    &&body.ProfileId=="TEST_ONLY.mining.recipe347-dressed"&&body.ParentId==scenario.Content.Deposit.ReceiverId
                    &&reserve.MassPounds+recoveredDamaged.MassPounds+received.Amount+discarded.Amount==new RuleQuantity(3,2)
                    &&completed.Work.Reservations.Single(x=>x.Id==MiningIds.ToolReserveReservation(attempt.Id)).Status==ReservationStatus.Released,
                    "Critical Success did not apply the +2 check, one distinct reserve, dressed retained unit and separate damaged recovery.");
                byte[] finishedSave=new SnapshotCodec().Encode(completed);
                simulation=new Simulation(policy,new SnapshotCodec().Decode(finishedSave),ExecutionProfile.Laboratory);
                Require(finishedSave.SequenceEqual(new SnapshotCodec().Encode(simulation.Capture())),
                    "Completed recipe-347 mining effects changed through save/restore.");
                var duplicate=simulation.Execute(host,start);
                Require(duplicate.Outcome==Outcome.Duplicate&&finishedSave.SequenceEqual(new SnapshotCodec().Encode(simulation.Capture())),
                    "Replaying recipe-347 mining repeated an extraction, reserve, or physical split.");
            });

            cases.Add("recipe347_failed_extraction_preserves_unawarded_prepared_mass_and_releases_reserve",()=>{
                var scenario=Recipe347MiningScenario();var selection=new MiningSelectionRequest(scenario.Content.Deposit.VersionId,
                    new[]{scenario.TargetCategoryId,scenario.DamagedCategoryId},MiningAbilityChoice.Wisdom,false,"",scenario.DamagedId);
                var unseeded=TestOnlySharedWorldPolicy.WithMining(scenario.Fixture);int baseModifier=MiningModifier(unseeded.Initial());
                uint seed=MiningSeedFor(TaskDegree.Failure,baseModifier+MiningToolCandidateProfileRecord.CheckBonus,dc:12);
                var policy=TestOnlySharedWorldPolicy.WithMining(scenario.Fixture,seed);var simulation=World(policy);
                MiningCommit(simulation,MiningCommand(simulation,CommandKind.StartMining,scenario.Content.Deposit.Id,selection));
                WorldAdvance(simulation,2200);
                var beforeCheck=simulation.Capture();var use=beforeCheck.MiningToolUses.Single();
                Require(use.PreparationCompletedAt==new RuleTime(2200)&&beforeCheck.MiningUnits.Single(x=>x.Id==scenario.TargetId).Status==MiningUnitStatus.Available,
                    "Preparation was not committed before the still-pending extraction check.");
                WorldAdvance(simulation,200);
                var result=simulation.Capture();var attempt=result.MiningAttempts.Single();use=result.MiningToolUses.Single();
                var target=result.MiningUnits.Single(x=>x.Id==scenario.TargetId);var reserve=result.MiningUnits.Single(x=>x.Id==scenario.ReserveId);
                var retained=result.Work.Lots.Single(x=>x.Id==use.RetainedLotId);var gangue=result.Work.Lots.Single(x=>x.Id==use.GangueLotId);
                Require(attempt.Status==MiningAttemptStatus.Failure
                    &&attempt.CheckModifier==baseModifier+MiningToolCandidateProfileRecord.CheckBonus&&use.CheckBonusApplied
                    &&!use.DressedBenefitAwarded&&use.CriticalReserveAwardedUnitId==""
                    &&target.Status==MiningUnitStatus.Ruined&&reserve.Status==MiningUnitStatus.Available
                    &&retained.Amount==new RuleQuantity(2,5)&&retained.LocationId=="ground.3.3"
                    &&gangue.Amount==new RuleQuantity(1,10)&&gangue.LocationId=="ground.3.3"
                    &&result.Work.Lots.Single(x=>x.Id==scenario.TargetId).Amount==default(RuleQuantity)
                    &&result.Work.Reservations.Single(x=>x.Id==MiningIds.ToolReserveReservation(attempt.Id)).Status==ReservationStatus.Released,
                    "Ordinary failure awarded output or destroyed the independently completed physical split/reserve claim.");
            });

            cases.Add("recipe347_ineligible_candidate_has_no_effect_and_falls_back_to_base_mining",()=>{
                var ineligible=new[]{Recipe347MiningScenario(broken:true),Recipe347MiningScenario(missingPrimary:true),
                    Recipe347MiningScenario(suppressed:true),Recipe347MiningScenario(melded:true),
                    Recipe347MiningScenario(misplaced:true),Recipe347MiningScenario(includeToolItem:false)};
                foreach(var scenario in ineligible) {
                    var state=TestOnlySharedWorldPolicy.WithMining(scenario.Fixture).Initial();
                    var instance=state.MiningToolInstanceStates.Single(x=>x.ProfileId==scenario.Profile.Id);
                    Require(!MiningToolCandidateRules.PhysicallyEligible(state,scenario.Profile,instance,MiningWorker,
                        new[]{scenario.TargetId,scenario.DamagedId,scenario.ReserveId}),
                        "An incomplete, damaged, suppressed, melded, inaccessible or missing candidate body qualified.");
                }
                var fallback=ineligible[1];var selection=new MiningSelectionRequest(fallback.Content.Deposit.VersionId,
                    new[]{fallback.TargetCategoryId,fallback.DamagedCategoryId},MiningAbilityChoice.Wisdom,false,"",fallback.DamagedId);
                var unseeded=TestOnlySharedWorldPolicy.WithMining(fallback.Fixture);int baseModifier=MiningModifier(unseeded.Initial());
                uint seed=MiningSeedFor(TaskDegree.Success,baseModifier,dc:12);
                var policy=TestOnlySharedWorldPolicy.WithMining(fallback.Fixture,seed);var simulation=World(policy);
                MiningCommit(simulation,MiningCommand(simulation,CommandKind.StartMining,fallback.Content.Deposit.Id,selection));
                Require(simulation.Capture().MiningToolUses.Length==0,
                    "An ineligible recipe-347 body registered candidate effects or claims.");
                WorldAdvance(simulation,2400);
                var result=simulation.Capture();var attempt=result.MiningAttempts.Single();
                Require(attempt.Status==MiningAttemptStatus.Success&&attempt.CheckModifier==baseModifier
                    &&result.MiningToolUses.Length==0
                    &&result.MiningUnits.Single(x=>x.Id==fallback.TargetId).Status==MiningUnitStatus.Extracted
                    &&result.Work.Lots.Single(x=>x.Id==fallback.TargetId).Amount==new RuleQuantity(1,2),
                    "Ordinary shared extraction failed when recipe-347 candidate benefits were physically unavailable.");
            });

            cases.Add("mineral_preparation_conserves_measured_mass_and_resumes_after_save",()=>{
                var profile=new MineralPreparationProfileRecord("TEST_ONLY.mining.preparation.iron",SharedMiningFixture.UnitA,
                    new RuleQuantity(1,10),"TEST_ONLY.mining.dressed-iron","TEST_ONLY.mining.gangue");
                var fixture=new SharedMiningFixture(mineralPreparationProfiles:new[]{profile});
                var unseeded=TestOnlySharedWorldPolicy.WithMining(fixture);
                uint seed=MiningSeedFor(TaskDegree.Success,MiningModifier(unseeded.Initial()));
                var policy=TestOnlySharedWorldPolicy.WithMining(fixture,seed);
                var simulation=World(policy);
                Require(simulation.Capture().SchemaVersion==Snapshot.MineralPreparationSchema,
                    "The explicit dressing profile did not select schema48.");
                RejectUnchanged(simulation,host,new Command("mineral.preparation.before-extraction",MiningWorker,
                    simulation.Capture().Revision,CommandKind.StartMineralPreparation,SharedMiningFixture.UnitA),
                    "MineralPreparationRequiresExtractedUnit");
                RejectUnchanged(simulation,host,new Command("mineral.preparation.unprofiled-unit",MiningWorker,
                    simulation.Capture().Revision,CommandKind.StartMineralPreparation,SharedMiningFixture.UnitB),
                    "MineralPreparationProfileUnavailable");

                MiningCommit(simulation,MiningCommand(simulation,CommandKind.StartMining,SharedMiningFixture.DepositId,
                    MiningSelection(SharedMiningFixture.CategoryA)));
                WorldAdvance(simulation,1800);
                var mined=simulation.Capture();var unitBefore=mined.MiningUnits.Single(x=>x.Id==SharedMiningFixture.UnitA);
                Require(unitBefore.Status==MiningUnitStatus.Extracted,"The dressing scenario did not first extract its ordinary unit.");
                var discovered=simulation.DiscoverCommands(host,MiningWorker).Single(x=>x.Command.Kind==CommandKind.StartMineralPreparation);
                Require(discovered.Query.Admissible&&discovered.Query.Costs.Any(x=>x.Kind=="work-seconds"
                    &&x.Amount==MineralPreparationValidation.WorkSeconds),"The full ten-minute no-roll task was not admitted and costed.");
                MiningCommit(simulation,discovered.Command);
                WorldAdvance(simulation,200);
                var partial=simulation.Capture();var working=partial.MineralPreparationAttempts.Single();
                Require(working.Status==MineralPreparationStatus.Working&&working.WorkDone==new RuleTime(200)
                    &&partial.Work.Reservations.Single(x=>x.Id==working.ReservationId).RemainingAmount==unitBefore.MassPounds,
                    "Partial dressing did not retain its complete input reservation and exact work credit.");
                byte[] workingSave=new SnapshotCodec().Encode(partial);
                simulation=new Simulation(policy,new SnapshotCodec().Decode(workingSave),ExecutionProfile.Laboratory);
                Require(workingSave.SequenceEqual(new SnapshotCodec().Encode(simulation.Capture())),
                    "A save during dressing changed its exact work or reservation state.");
                var pause=simulation.DiscoverCommands(host,MiningWorker).Single(x=>x.Command.Kind==CommandKind.PauseMineralPreparation);
                Require(pause.Query.Admissible,"The active dressing procedure did not expose its pause control.");
                MiningCommit(simulation,pause.Command);
                var paused=simulation.Capture().MineralPreparationAttempts.Single();
                Require(paused.Status==MineralPreparationStatus.Paused&&paused.WorkDone==new RuleTime(200)
                    &&simulation.Capture().Work.Reservations.Single(x=>x.Id==paused.ReservationId).RemainingAmount==unitBefore.MassPounds,
                    "Pausing dressing refunded progress or released its input reservation.");
                var pausedView=WorldActivityProjection.OpenProcedures(simulation.Capture(),simulation.DiscoverCommands(host,MiningWorker))
                    .Single(x=>x.Id==paused.Id);
                Require(pausedView.Kind==WorldProcedureKind.MineralPreparation&&pausedView.AvailableCommands.Any(x=>x.Command.Kind==CommandKind.ResumeMineralPreparation),
                    "The persisted paused procedure did not expose its resume control.");
                byte[] pausedSave=new SnapshotCodec().Encode(simulation.Capture());
                simulation=new Simulation(policy,new SnapshotCodec().Decode(pausedSave),ExecutionProfile.Laboratory);
                var resume=simulation.DiscoverCommands(host,MiningWorker).Single(x=>x.Command.Kind==CommandKind.ResumeMineralPreparation);
                Require(resume.Query.Admissible,"The saved preparation job could not resume with its reserved input.");
                MiningCommit(simulation,resume.Command);
                uint randomBeforeCompletion=simulation.Capture().RandomState;
                WorldAdvance(simulation,400);
                var completed=simulation.Capture();var attempt=completed.MineralPreparationAttempts.Single();
                var retained=completed.InventoryLots.Single(x=>x.LotId==attempt.RetainedLotId);
                var retainedLot=completed.Work.Lots.Single(x=>x.Id==attempt.RetainedLotId);
                var gangue=completed.InventoryLots.Single(x=>x.LotId==attempt.GangueLotId);
                var gangueLot=completed.Work.Lots.Single(x=>x.Id==attempt.GangueLotId);
                var body=completed.PortableEquipment.Single(x=>x.Id==SharedMiningFixture.UnitA);
                var gangueBody=completed.PortableEquipment.Single(x=>x.Id==attempt.GangueLotId);
                var unitAfter=completed.MiningUnits.Single(x=>x.Id==SharedMiningFixture.UnitA);
                Require(attempt.Status==MineralPreparationStatus.Complete&&attempt.WorkDone==new RuleTime(600)
                    &&attempt.InputMassPounds==new RuleQuantity(1)&&attempt.GangueWastePounds==new RuleQuantity(1,10)
                    &&attempt.RetainedMassPounds==new RuleQuantity(9,10)
                    &&attempt.InputMassPounds==attempt.GangueWastePounds+attempt.RetainedMassPounds
                    &&completed.Work.Lots.Single(x=>x.Id==SharedMiningFixture.UnitA).Amount==default(RuleQuantity)
                    &&retained.ParentId==SharedMiningFixture.UnitA&&retained.CreatedAmount==new RuleQuantity(9,10)
                    &&retainedLot.Amount==new RuleQuantity(9,10)&&retainedLot.LocationId==SharedMiningFixture.ReceiverId
                    &&retained.Access==InventoryAccess.Stowed&&gangue.ParentId==SharedMiningFixture.UnitA
                    &&gangue.CreatedAmount==new RuleQuantity(1,10)&&gangueLot.Amount==new RuleQuantity(1,10)
                    &&gangueLot.LocationId=="ground.3.3"&&gangue.Access==InventoryAccess.Ground
                    &&body.ProfileId==profile.DressedItemProfileId&&body.LinkedId==attempt.RetainedLotId
                    &&body.ParentId==SharedMiningFixture.ReceiverId&&body.Placement==PortablePlacement.Contained
                    &&gangueBody.ProfileId==profile.GangueItemProfileId&&gangueBody.Placement==PortablePlacement.Ground
                    &&gangueBody.GroundX==3&&gangueBody.GroundY==3
                    &&unitAfter.Status==unitBefore.Status&&unitAfter.MassPounds==unitBefore.MassPounds
                    &&unitAfter.ValueCopper==unitBefore.ValueCopper&&unitAfter.Condition==unitBefore.Condition
                    &&unitAfter.CategoryId==unitBefore.CategoryId&&completed.RandomState==randomBeforeCompletion,
                    "Dressing changed the wrong source facts, lost lineage/custody, failed the measured mass split, or consumed RNG.");
                byte[] finishedSave=new SnapshotCodec().Encode(completed);
                simulation=new Simulation(policy,new SnapshotCodec().Decode(finishedSave),ExecutionProfile.Laboratory);
                Require(finishedSave.SequenceEqual(new SnapshotCodec().Encode(simulation.Capture())),
                    "Completed dressing and its retained/waste lineage changed through save/restore.");
                var duplicate=simulation.Execute(host,discovered.Command);
                Require(duplicate.Outcome==Outcome.Duplicate&&finishedSave.SequenceEqual(new SnapshotCodec().Encode(simulation.Capture())),
                    "Replaying the completed dressing command repeated inventory settlement.");
            });

            cases.Add("mining_uses_wisdom_score_and_check_modifier_not_intelligence",()=>{
                var fixture=new SharedMiningFixture(intelligence:8,wisdom:18);var unseeded=TestOnlySharedWorldPolicy.WithMining(fixture);
                uint seed=MiningSeedFor(TaskDegree.Success,MiningModifier(unseeded.Initial()));
                var policy=TestOnlySharedWorldPolicy.WithMining(fixture,seed);var simulation=World(policy);
                MiningCommit(simulation,MiningCommand(simulation,CommandKind.StartMining,SharedMiningFixture.DepositId,MiningSelection(SharedMiningFixture.CategoryA)));
                Require(simulation.Capture().MiningAttempts.Single().AbilityModifier==4,"Mining mapped Wisdom to a different ability score than index 4.");
                WorldAdvance(simulation,1800);var attempt=simulation.Capture().MiningAttempts.Single();
                Require(attempt.Status==MiningAttemptStatus.Success&&attempt.CheckModifier==4+attempt.ProficiencyBonus,
                    "Resolved check modifier did not use Wisdom 18 instead of Intelligence 8.");
            });

            cases.Add("mining_timed_inventory_handling_credits_parallel_work_and_guards_completion_boundary",()=>{
                var policy=TestOnlySharedWorldPolicy.WithMining(new SharedMiningFixture());var simulation=World(policy);
                MiningCommit(simulation,MiningCommand(simulation,CommandKind.StartMining,SharedMiningFixture.DepositId,MiningSelection(SharedMiningFixture.CategoryA)));
                var handle=new Command("mining.parallel-handling",TestOnlyPolicy.ActorId,simulation.Capture().Revision,
                    CommandKind.HandleInventory,TestOnlyInventoryPolicy.FoodId,inventory:new InventoryRequest(new RuleQuantity(1),handling:HandlingKind.Stow));
                var handled=simulation.Execute(host,handle);
                Require(handled.Outcome==Outcome.Committed&&simulation.Capture().RuleClock==new RuleTime(1)
                    &&simulation.Capture().MiningAttempts.Single().WorkDone==new RuleTime(1),
                    "One-second inventory handling did not credit the parallel mining job on the shared clock.");

                simulation=World(policy);MiningCommit(simulation,MiningCommand(simulation,CommandKind.StartMining,SharedMiningFixture.DepositId,MiningSelection(SharedMiningFixture.CategoryA)));
                WorldAdvance(simulation,1799);
                var boundaryHandle=new Command("mining.boundary-handling",TestOnlyPolicy.ActorId,simulation.Capture().Revision,
                    CommandKind.HandleInventory,TestOnlyInventoryPolicy.FoodId,inventory:new InventoryRequest(new RuleQuantity(1),handling:HandlingKind.Stow));
                RejectUnchanged(simulation,host,boundaryHandle,"TimedHandlingBoundaryUnsupported");
                WorldAdvance(simulation,1);
                var attempt=simulation.Capture().MiningAttempts.Single();
                Require(attempt.Status==MiningAttemptStatus.Success||attempt.Status==MiningAttemptStatus.CriticalSuccess
                    ||attempt.Status==MiningAttemptStatus.Failure||attempt.Status==MiningAttemptStatus.CriticalFailure,
                    "The exact completion boundary did not resolve its check after timed handling was rejected: "+attempt.Status+".");
            });

            cases.Add("mining_codec_rejects_noncanonical_boolean_flags",()=>{
                byte[] bytes=new SnapshotCodec().Encode(TestOnlySharedWorldPolicy.WithMining(new SharedMiningFixture()).Initial());
                int flag=MiningHurryFlagOffset(bytes);Require(bytes[flag]==0,"Fixture hurry flag was not encoded as false.");
                bytes[flag]=2;Resign(bytes);Throws<InvalidDataException>(()=>new SnapshotCodec().Decode(bytes));
            });

            cases.Add("mining_duration_and_stage_plan_preserve_exposed_parcel_scope",()=>{
                Require(MiningExtractionRules.DurationSeconds(2,2,false)==3600
                    &&MiningExtractionRules.DurationSeconds(2,1,false)==1800
                    &&MiningExtractionRules.DurationSeconds(2,1,true)==900
                    &&MiningExtractionRules.TierDc(1)==12&&MiningExtractionRules.TierDc(2)==13
                    &&MiningExtractionRules.TierDc(3)==15&&MiningExtractionRules.TierDc(4)==16
                    &&MiningExtractionRules.TierDc(5)==18&&MiningExtractionRules.TierDc(6)==19,
                    "Exposed-node duration, hurry rounding, or tier DC changed.");
                MiningExtractionRules.StagePlan(1800,out int setup,out int removal,out int sorting);
                Require(setup==150&&removal==1500&&sorting==150&&setup+removal+sorting==1800,
                    "The provisional 1:10:1 stage plan did not preserve total active work.");
                Throws<ArgumentOutOfRangeException>(()=>MiningExtractionRules.DurationSeconds(0,1,false));
                Throws<ArgumentOutOfRangeException>(()=>MiningExtractionRules.TierDc(0));
            });

            cases.Add("mining_partial_selection_commits_then_pauses_saves_resumes_and_receives_once",()=>{
                var unseeded=TestOnlySharedWorldPolicy.WithMining(new SharedMiningFixture());
                uint seed=MiningSeedFor(TaskDegree.Success,MiningModifier(unseeded.Initial()));
                var policy=TestOnlySharedWorldPolicy.WithMining(new SharedMiningFixture(),seed);
                var simulation=World(policy);var initial=simulation.Capture();
                var discovered=simulation.DiscoverCommands(host,MiningWorker).Single(x=>x.Command.Kind==CommandKind.StartMining
                    &&x.Command.Target==SharedMiningFixture.DepositId
                    &&x.Command.MiningSelection.CategoryIds.SequenceEqual(new[]{SharedMiningFixture.CategoryA}));
                Require(discovered.Query.Admissible&&discovered.Query.Costs.Any(x=>x.Kind=="work-seconds"&&x.Amount==1800)
                    &&discovered.Query.Costs.Any(x=>x.Kind=="finite-source-unit"&&x.ResourceId==SharedMiningFixture.UnitA)
                    &&Bytes(simulation).SequenceEqual(new SnapshotCodec().Encode(initial)),
                    "Mining command discovery did not report its shared-clock and finite-stock costs without mutation.");
                var start=MiningCommand(simulation,CommandKind.StartMining,SharedMiningFixture.DepositId,MiningSelection(SharedMiningFixture.CategoryA));
                MiningCommit(simulation,start);
                var attempt=simulation.Capture().MiningAttempts.Single();
                Require(attempt.Status==MiningAttemptStatus.Working&&attempt.DurationSeconds==1800
                    &&attempt.SetupSeconds==150&&attempt.RemovalSeconds==1500&&attempt.SortingSeconds==150
                    &&attempt.CheckDc==12&&simulation.Capture().RandomState==initial.RandomState
                    &&simulation.Capture().Work.Reservations.Count(x=>x.JobId==attempt.Id)==1,
                    "Starting extraction rolled early, reserved an inexact selection, or used an incorrect task profile.");
                var reconstructed=CommandHistory.Read(simulation.Capture().Receipts.Single(x=>x.Id==start.Id));
                Require(reconstructed.MiningSelection!=null&&reconstructed.MiningSelection.CategoryIds.SequenceEqual(new[]{SharedMiningFixture.CategoryA}),
                    "The persisted start receipt could not reconstruct the selected deposit version and category.");

                WorldAdvance(simulation,150);attempt=simulation.Capture().MiningAttempts.Single();
                Require(attempt.WorkDone==new RuleTime(150)&&!attempt.CommittedAt.HasValue
                    &&MiningExtractionRules.Stage(attempt)==MiningWorkStage.Removal
                    &&simulation.Capture().MiningUnits.Single(x=>x.Id==SharedMiningFixture.UnitB).Status==MiningUnitStatus.Available,
                    "Setup completion committed selection before positive extraction work.");
                WorldAdvance(simulation,1);attempt=simulation.Capture().MiningAttempts.Single();
                Require(attempt.CommittedAt==new RuleTime(150)
                    &&simulation.Capture().MiningUnits.Single(x=>x.Id==SharedMiningFixture.UnitB).Status==MiningUnitStatus.Forfeited,
                    "The first positive removal second did not commit partial selection (work="+attempt.WorkDone+", committed="
                    +(attempt.CommittedAt.HasValue?attempt.CommittedAt.Value.ToString():"none")+", status="+attempt.Status+", unselected="
                    +simulation.Capture().MiningUnits.Single(x=>x.Id==SharedMiningFixture.UnitB).Status+").");
                WorldAdvance(simulation,869);
                MiningCommit(simulation,MiningCommand(simulation,CommandKind.PauseMining,attempt.Id));
                var paused=simulation.Capture().MiningAttempts.Single();
                Require(paused.Status==MiningAttemptStatus.Paused&&paused.WorkDone==new RuleTime(1020)
                    &&!simulation.Capture().Work.WorkerIntervals.Any(x=>x.JobId==attempt.Id&&x.Start<=simulation.Capture().RuleClock&&x.End>simulation.Capture().RuleClock),
                    "Pause failed to preserve exact seventeen-minute labor and release the active interval.");
                string path=Path.Combine(directory,"mining-paused.bin");new FileSaveStore().Save(path,simulation.Capture());
                simulation=new Simulation(policy,new FileSaveStore().Load(path),ExecutionProfile.Laboratory);
                Require(new SnapshotCodec().Encode(simulation.Capture()).SequenceEqual(new SnapshotCodec().Encode(new SnapshotCodec().Decode(new SnapshotCodec().Encode(simulation.Capture())))),
                    "Paused mining state did not roundtrip canonically.");
                MiningCommit(simulation,MiningCommand(simulation,CommandKind.ResumeMining,attempt.Id));
                WorldAdvance(simulation,780);
                var state=simulation.Capture();attempt=state.MiningAttempts.Single();
                var unit=state.MiningUnits.Single(x=>x.Id==SharedMiningFixture.UnitA);
                var received=state.InventoryLots.Single(x=>x.LotId==unit.Id);
                var body=state.PortableEquipment.Single(x=>x.Id==unit.Id);
                var lot=state.Work.Lots.Single(x=>x.Id==unit.Id);
                var expectedRoll=PlaytestDice.RollD20(initial.RandomState);
                Require(attempt.Status==MiningAttemptStatus.Success&&attempt.Degree==MiningCheckDegree.Success
                    &&attempt.WorkDone==new RuleTime(1800)&&attempt.ResolvedAt==new RuleTime(1800)
                    &&attempt.FirstDie==expectedRoll.First&&attempt.SecondDie==0&&attempt.Natural==expectedRoll.Natural
                    &&attempt.RandomBefore==initial.RandomState&&attempt.RandomAfter==expectedRoll.NextRandomState
                    &&unit.Status==MiningUnitStatus.Extracted&&unit.ReceivedLotId==unit.Id
                    &&unit.ReceivedContainerId==SharedMiningFixture.ReceiverId
                    &&lot.Amount==unit.MassPounds&&lot.LocationId==SharedMiningFixture.ReceiverId
                    &&received.OwnerId==MiningWorker&&received.FreshUntil==null&&received.Nutrition==NutritionKind.None
                    &&received.Access==InventoryAccess.Stowed&&body.Placement==PortablePlacement.Contained
                    &&body.ParentId==SharedMiningFixture.ReceiverId
                    &&state.MiningUnits.Single(x=>x.Id==SharedMiningFixture.UnitB).Status==MiningUnitStatus.Forfeited
                    &&state.Work.Reservations.Where(x=>x.JobId==attempt.Id).All(x=>x.Status==ReservationStatus.Released),
                    "Successful extraction did not deliver exactly the selected physical unit into the receiver with its provenance and claims settled.");
                var saved=new SnapshotCodec().Encode(state);
                simulation=new Simulation(policy,new SnapshotCodec().Decode(saved),ExecutionProfile.Laboratory);
                Require(saved.SequenceEqual(new SnapshotCodec().Encode(simulation.Capture())),"Resolved mining audit or physical output changed through save/restore.");
                var duplicate=simulation.Execute(host,start);
                Require(duplicate.Outcome==Outcome.Duplicate&&saved.SequenceEqual(new SnapshotCodec().Encode(simulation.Capture())),
                    "Replayed mining start repeated or changed the completed extraction.");
                RejectUnchanged(simulation,host,MiningCommand(simulation,CommandKind.StartMining,SharedMiningFixture.DepositId,
                    MiningSelection(SharedMiningFixture.CategoryA)),"MiningDepositClaimClosed");
            });

            cases.Add("mining_critical_success_recovers_one_authored_damaged_unit",()=>{
                var fixture=new SharedMiningFixture(unitBCondition:MiningUnitCondition.DamagedPotentiallyRecoverable);
                var unseeded=TestOnlySharedWorldPolicy.WithMining(fixture);
                uint seed=MiningSeedFor(TaskDegree.CriticalSuccess,MiningModifier(unseeded.Initial()));
                var policy=TestOnlySharedWorldPolicy.WithMining(fixture,seed);var simulation=World(policy);
                MiningCommit(simulation,MiningCommand(simulation,CommandKind.StartMining,SharedMiningFixture.DepositId,
                    MiningSelection(SharedMiningFixture.CategoryA,SharedMiningFixture.CategoryB)));
                WorldAdvance(simulation,3600);var state=simulation.Capture();
                Require(state.MiningAttempts.Single().Status==MiningAttemptStatus.CriticalSuccess
                    &&state.MiningUnits.All(x=>x.Status==MiningUnitStatus.Extracted)
                    &&state.MiningUnits.Single(x=>x.Id==SharedMiningFixture.UnitB).Condition==MiningUnitCondition.DamagedPotentiallyRecoverable
                    &&state.Conditions.All(x=>ConditionHistory.Restore(x).Ledger.Now.Time==state.RuleClock&&x.Operations.Count<8),
                    "Critical success did not add the one fixture-authored recoverable damaged unit while preserving its condition record.");
            });

            cases.Add("mining_failure_ruins_the_highest_value_selected_unit",()=>{
                var unseeded=TestOnlySharedWorldPolicy.WithMining(new SharedMiningFixture());
                uint seed=MiningSeedFor(TaskDegree.Failure,MiningModifier(unseeded.Initial()));
                var policy=TestOnlySharedWorldPolicy.WithMining(new SharedMiningFixture(),seed);var simulation=World(policy);
                MiningCommit(simulation,MiningCommand(simulation,CommandKind.StartMining,SharedMiningFixture.DepositId,
                    MiningSelection(SharedMiningFixture.CategoryA,SharedMiningFixture.CategoryB)));
                WorldAdvance(simulation,3600);var state=simulation.Capture();
                Require(state.MiningAttempts.Single().Status==MiningAttemptStatus.Failure
                    &&state.MiningUnits.Single(x=>x.Id==SharedMiningFixture.UnitB).Status==MiningUnitStatus.Ruined
                    &&state.MiningUnits.Single(x=>x.Id==SharedMiningFixture.UnitA).Status==MiningUnitStatus.Spent
                    &&state.InventoryLots.Where(x=>x.LotId==SharedMiningFixture.UnitA||x.LotId==SharedMiningFixture.UnitB)
                        .All(x=>x.Access==InventoryAccess.Ground)
                    &&state.PortableEquipment.Where(x=>x.Id==SharedMiningFixture.UnitA||x.Id==SharedMiningFixture.UnitB)
                        .All(x=>x.Placement==PortablePlacement.Ground),
                    "Failure did not ruin only the highest-value selected unit or award no output.");
            });

            cases.Add("mining_critical_failure_records_bludgeoning_accident_and_applies_life_damage",()=>{
                var unseeded=TestOnlySharedWorldPolicy.WithMining(new SharedMiningFixture());
                uint seed=MiningSeedFor(TaskDegree.CriticalFailure,MiningModifier(unseeded.Initial()));
                var policy=TestOnlySharedWorldPolicy.WithMining(new SharedMiningFixture(),seed);var simulation=World(policy);
                var before=simulation.Capture();
                MiningCommit(simulation,MiningCommand(simulation,CommandKind.StartMining,SharedMiningFixture.DepositId,
                    MiningSelection(SharedMiningFixture.CategoryA)));
                WorldAdvance(simulation,1800);var state=simulation.Capture();
                var attempt=state.MiningAttempts.Single();var priorLife=ActorLifeRules.Read(before.Lives.Single(x=>x.ActorId==MiningWorker));
                var life=ActorLifeRules.Read(state.Lives.Single(x=>x.ActorId==MiningWorker));
                Require(attempt.Status==MiningAttemptStatus.CriticalFailure&&attempt.D4Rolled>=1&&attempt.D4Rolled<=4
                    &&attempt.AccidentDamageType=="bludgeoning"&&attempt.DamageApplied>0&&life.Hp==priorLife.Hp-attempt.DamageApplied
                    &&state.MiningUnits.Single(x=>x.Id==SharedMiningFixture.UnitA).Status==MiningUnitStatus.Ruined
                    &&state.MiningUnits.Single(x=>x.Id==SharedMiningFixture.UnitB).Status==MiningUnitStatus.Forfeited,
                    "Critical failure did not record and apply the authored absent-hazard bludgeoning accident or settle finite stock.");
            });

            cases.Add("mining_shared_resolver_handles_distinct_authored_deposits_through_save_and_replay",()=>{
                var profiles=new[]{
                    AuthoredMiningDeposit("slate","TEST_ONLY.mineral.slate",1,3,3,new RuleQuantity(1),RuleQuantity.FromFraction(1,30),12),
                    AuthoredMiningDeposit("cobalt","TEST_ONLY.mineral.cobalt",5,4,3,new RuleQuantity(2),RuleQuantity.FromFraction(1,8),95)};
                foreach(var content in profiles) {
                    var fixture=new SharedMiningFixture(new[]{content});
                    var unseeded=TestOnlySharedWorldPolicy.WithMining(fixture);
                    int dc=MiningExtractionRules.TierDc(content.Categories.Single().Tier);
                    uint seed=MiningSeedFor(TaskDegree.Success,MiningModifier(unseeded.Initial()),dc:dc);
                    var policy=TestOnlySharedWorldPolicy.WithMining(fixture,seed);
                    var simulation=World(policy);var initial=simulation.Capture();
                    var category=content.Categories.Single();
                    var selection=new MiningSelectionRequest(content.Deposit.VersionId,new[]{category.Id},MiningAbilityChoice.Wisdom);
                    var start=MiningCommand(simulation,CommandKind.StartMining,content.Deposit.Id,selection);
                    var discovered=simulation.DiscoverCommands(host,MiningWorker).Single(x=>x.Command.Kind==CommandKind.StartMining
                        &&x.Command.Target==content.Deposit.Id&&x.Command.MiningSelection.CategoryIds.SequenceEqual(new[]{category.Id}));
                    Require(discovered.Query.Admissible&&discovered.Query.Costs.Any(x=>x.Kind=="work-seconds"&&x.Amount==3600),
                        "Authored mining content was not admitted through the shared assessment path.");
                    MiningCommit(simulation,start);WorldAdvance(simulation,3600);
                    var state=simulation.Capture();var attempt=state.MiningAttempts.Single();var unit=state.MiningUnits.Single();
                    Require(attempt.DepositId==content.Deposit.Id&&attempt.CheckDc==dc&&attempt.Status==MiningAttemptStatus.Success
                        &&unit.Id==content.Units.Single().Id&&unit.Status==MiningUnitStatus.Extracted
                        &&unit.ReceivedContainerId==content.Deposit.ReceiverId
                        &&state.Work.Lots.Single(x=>x.Id==unit.Id).LocationId==content.Deposit.ReceiverId
                        &&state.PortableEquipment.Single(x=>x.Id==content.Deposit.ReceiverId).FitRuleId.StartsWith("TEST_ONLY.mining.fit.",StringComparison.Ordinal),
                        "Shared mining resolution ignored authored tier, physical receiver or extracted-unit identity.");
                    byte[] saved=new SnapshotCodec().Encode(state);
                    simulation=new Simulation(policy,new SnapshotCodec().Decode(saved),ExecutionProfile.Laboratory);
                    Require(saved.SequenceEqual(new SnapshotCodec().Encode(simulation.Capture())),"Distinct authored mining state changed through save/restore.");
                    var duplicate=simulation.Execute(host,start);
                    Require(duplicate.Outcome==Outcome.Duplicate&&saved.SequenceEqual(new SnapshotCodec().Encode(simulation.Capture())),
                        "Replaying a distinct authored mining command repeated or changed settlement.");
                }
            });

            cases.Add("mining_rejects_missing_access_and_unapproved_hurry_without_cost",()=>{
                foreach(var fixture in new[]{new SharedMiningFixture(hasMiningTools:false),new SharedMiningFixture(hasPick:false),
                    new SharedMiningFixture(hasReceiver:false),new SharedMiningFixture(hasWorkSurface:false)}) {
                    var simulation=World(TestOnlySharedWorldPolicy.WithMining(fixture));
                    string expected=!fixture.HasMiningTools?"MiningToolsUnavailable":!fixture.HasPick?"MiningPickUnavailable":
                        !fixture.HasWorkSurface?"MiningWorkSurfaceUnavailable":"MiningReceiverUnavailable";
                    RejectUnchanged(simulation,host,MiningCommand(simulation,CommandKind.StartMining,SharedMiningFixture.DepositId,
                        MiningSelection(SharedMiningFixture.CategoryA)),expected);
                }
                var hurried=World(TestOnlySharedWorldPolicy.WithMining(new SharedMiningFixture()));
                var hurrySelection=new MiningSelectionRequest(SharedMiningFixture.DepositVersionId,new[]{SharedMiningFixture.CategoryA},
                    MiningAbilityChoice.Wisdom,true);
                RejectUnchanged(hurried,host,MiningCommand(hurried,CommandKind.StartMining,SharedMiningFixture.DepositId,hurrySelection),"MiningHurryNotFeasible");
            });
        }
    }
}
#endif
