#if DECENNIUM_TEST_ONLY && (UNITY_EDITOR || HEADLESS_TESTS)
using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using Decennium.Foundation.Laboratory;

namespace Decennium.Foundation.Tests
{
    public static partial class FoundationCases
    {
        private static TestOnlySharedWorldPolicy ManufacturePolicy(uint seed=1,SharedManufacturingFixture facts=null,SharedCraftingFixture crafting=null,ConditionCombatFixture conditions=null)
            =>new TestOnlySharedWorldPolicy(new SharedCombatFixture(seed:seed),new SharedResearchFixture(),crafting??new SharedCraftingFixture(),new SharedRepairFixture(),facts??new SharedManufacturingFixture(),conditions:conditions);
        private static Command ManufactureCommand(Simulation s,CommandKind kind=CommandKind.StartManufacturing,string target=SharedResearchFixture.Recipe,int x=0,int y=0)
            =>new Command("manufacturing."+(s.Capture().Revision+1),TestOnlyPolicy.CompanionId,s.Capture().Revision,kind,target,x,y);
        private static ManufacturingOrderRecord Order(Simulation s)=>s.Capture().ManufacturingOrders.Last();
        private static void LearnManufacturing(Simulation s){ResearchStart(s,copy:true);WorldAdvance(s,3600);}
        private static void ManufactureStart(Simulation s,int set=0,int extra=0)=>WorldCommit(s,ManufactureCommand(s,x:set,y:extra));
        private static void ManufactureControl(Simulation s,CommandKind kind)=>WorldCommit(s,ManufactureCommand(s,kind,Order(s).Id));
        private static void ManufactureChoice(Simulation s,CraftQualityChoice choice=CraftQualityChoice.FullYield,int catalyst=-1)=>WorldCommit(s,ManufactureCommand(s,CommandKind.ResolveManufacturingQuality,Order(s).Id,(int)choice,catalyst+1));
        private static RuleQuantity Material(Simulation s,int component,int set=0)=>s.Capture().Work.Lots.Single(x=>x.Id==SharedManufacturingFixture.Lot(set,component)).Amount;
        private static uint ManufacturingMishapSeed(int result){for(uint seed=1;seed<1000000;seed++){var d20=PlaytestDice.RollD20(seed);if(d20.Natural==1&&DiceStream.Draw(d20.NextRandomState,6).Value+1==result)return seed;}throw new Exception("No mishap seed.");}
        private static Command DoseCommand(Simulation s,string dose,string recipient=TestOnlyPolicy.ActorId,string actor=TestOnlyPolicy.ActorId)
            =>new Command("dose."+(s.Capture().Revision+1),actor,s.Capture().Revision,CommandKind.UseAlchemyDose,dose,inventory:new InventoryRequest(new RuleQuantity(1),recipient));
        private static void AddManufacturingCases(Dictionary<string,Action> cases,string directory)
        {
            const string worker=TestOnlyPolicy.CompanionId,hero=TestOnlyPolicy.ActorId;var host=TestOnlySharedWorldPolicy.Host();
            cases.Add("manufacturing_native_mishap_identity_cannot_collide_with_supplied_occurrence",()=>{
                var s=World(ManufacturePolicy(ManufacturingMishapSeed(3),crafting:new SharedCraftingFixture(events:new[]{new CraftingMishapFact("manufacture.order.4.mishap",3)})));
                CraftEvent(s,"manufacture.order.4.mishap");LearnManufacturing(s);ManufactureStart(s);Require(Order(s).Id=="manufacture.order.4","Fixture revision changed.");WorldAdvance(s,14400);
                Require(Order(s).Status==ManufacturingStatus.Complete&&s.Capture().CraftingIncidents.Length==2&&Order(s).MishapIncidentId=="manufacture.order.4.mishap.1"
                    &&s.Capture().Structures.Single(x=>x.Id==SharedCraftingFixture.ToolId).Hp==3,"Public incident identity blocked native completion or replaced earlier damage.");
            });
            cases.Add("manufacturing_suspended_status_is_scoped_to_actual_principal_receipt",()=>{
                var s=World(ManufacturePolicy(SeedForDeath(16)));var other=new Authority("other.host",new[]{hero},true);
                var earlier=new Command("same-id",hero,0,CommandKind.AdvanceClock,"",1,1);Require(s.Execute(other,earlier).Outcome==Outcome.Committed,"Earlier principal advance rejected.");
                LearnManufacturing(s);ManufactureStart(s,extra:2);var initiating=new Command("same-id",hero,s.Capture().Revision,CommandKind.AdvanceClock,"",14400,1);
                Require(s.Execute(host,initiating).IsSuspended&&!s.Execute(other,earlier).IsSuspended&&s.Execute(host,initiating).IsSuspended,"Another principal's old receipt borrowed suspended status.");
            });
            cases.Add("manufacturing_native_mishap_preserves_future_authored_occurrence_identity",()=>{
                const string id="manufacture.order.3.mishap";
                var s=World(ManufacturePolicy(ManufacturingMishapSeed(3),crafting:new SharedCraftingFixture(events:new[]{new CraftingMishapFact(id,3,at:T(18001))})));
                LearnManufacturing(s);ManufactureStart(s);WorldAdvance(s,14400);
                Require(Order(s).MishapIncidentId==id+".1","Generated incident claimed future source identity.");WorldAdvance(s,1);CraftEvent(s,id);
                Require(s.Capture().CraftingIncidents.Length==2&&s.Capture().Structures.Single(x=>x.Id==SharedCraftingFixture.ToolId).Hp==3,"Native outcome made future source fact unreachable.");
            });
            cases.Add("manufacturing_specialty_boundary_fails_closed_without_silent_level10_bonus",()=>{
                Throws<ArgumentException>(()=>new SharedManufacturingFixture(level:10));
                var s=World(ManufacturePolicy(SeedForDeath(6),new SharedManufacturingFixture(level:9,xp:18)));LearnManufacturing(s);ManufactureStart(s);WorldAdvance(s,14400);
                Require(s.Capture().Trades.Single().Level==10&&s.Capture().Trades.Single().Xp==3,"Legitimate advancement failed at specialty boundary.");
                RejectUnchanged(s,host,ManufactureCommand(s,x:1),"ManufacturingSpecialtyNotImplemented");
            });
            cases.Add("manufacturing_strict_codec_rejects_noncanonical_booleans_with_valid_checksum",()=>{
                var s=World(ManufacturePolicy(SeedForDeath(16)));LearnManufacturing(s);ManufactureStart(s,extra:2);WorldAdvance(s,14400);
                byte[] component;using(var stream=new MemoryStream()){using(var w=new BinaryWriter(stream,System.Text.Encoding.UTF8,true))
                    typeof(SnapshotCodec).Assembly.GetType("Decennium.Foundation.ManufacturingCodec").GetMethod("Write").Invoke(null,new object[]{w,s.Capture()});component=stream.ToArray();}
                var positions=new List<int>{0,17};using(var r=new BinaryReader(new MemoryStream(component))){
                    void SkipText(){int n=r.ReadInt32();r.BaseStream.Position+=n;}
                    r.BaseStream.Position=18;SkipText();r.BaseStream.Position+=8;SkipText();r.BaseStream.Position+=4;
                    Require(r.ReadInt32()==1,"Expected one serialized order.");SkipText();SkipText();SkipText();r.BaseStream.Position+=8;positions.Add((int)r.BaseStream.Position);
                    r.BaseStream.Position+=5;int phases=r.ReadInt32();r.BaseStream.Position+=phases*16+4+16+16+16+16;positions.Add((int)r.BaseStream.Position);
                }
                var whole=Bytes(s);int offset=whole.Length-32-component.Length;Require(whole.Skip(offset).Take(component.Length).SequenceEqual(component),"Could not locate exact serialized manufacturing component.");
                foreach(int position in positions){var corrupt=whole.ToArray();corrupt[offset+position]=2;using(var sha=System.Security.Cryptography.SHA256.Create()){var hash=sha.ComputeHash(corrupt,0,corrupt.Length-32);Array.Copy(hash,0,corrupt,corrupt.Length-32,32);}
                    Throws<InvalidDataException>(()=>new SnapshotCodec().Decode(corrupt));}
            });
            cases.Add("manufacturing_capacity_keeps_one_receipt_for_quality_settlement",()=>{
                var s=World(ManufacturePolicy(SeedForDeath(16)));LearnManufacturing(s);ManufactureStart(s,extra:2);
                // Construct lawful scheduler receipts, then require one complete independent
                // canonical replay. Avoid replaying all earlier padding after every fixture step.
                var padded=s.Capture();var policy=ManufacturePolicy(SeedForDeath(16));
                while(padded.Revision<510){
                    var c=new Command("padding."+(padded.Revision+1),hero,padded.Revision,CommandKind.AdvanceClock,"",1,1);
                    Require(policy.Resolve(padded,c)==null,"Lawful padding command rejected.");
                    var receipt=new CommandReceipt{Principal=host.Principal,Id=c.Id,Revision=++padded.Revision,Fingerprint=FormattableString.Invariant($"{(int)c.Kind}|{c.Actor}||{c.ExpectedRevision}|1|1")};
                    Require(c.MatchesReceipt(receipt),"Padding receipt did not match exact command.");padded.Receipts=padded.Receipts.Concat(new[]{receipt}).ToArray();
                }
                s=new Simulation(policy,padded,ExecutionProfile.Laboratory);
                var at510=s.Capture();WorldAdvance(s,checked((int)Order(s).Work.Remaining.Numerator));
                Require(s.Capture().Revision==511&&Order(s).Status==ManufacturingStatus.AwaitingChoice,"Penultimate receipt did not retain settlement room.");ManufactureChoice(s,catalyst:0);
                Require(s.Capture().Revision==512&&Order(s).Status==ManufacturingStatus.Complete&&!s.Capture().ManufacturingOrders.Any(x=>x.Open),"Last legal receipt could not settle frozen output.");
                var blocked=new Simulation(ManufacturePolicy(SeedForDeath(16)),at510,ExecutionProfile.Laboratory);WorldAdvance(blocked,1);byte[] before=Bytes(blocked);
                var result=blocked.Execute(host,IC(blocked,CommandKind.AdvanceClock,x:checked((int)Order(blocked).Work.Remaining.Numerator),y:1));
                Require(result.Outcome==Outcome.Rejected&&Bytes(blocked).SequenceEqual(before)&&blocked.Capture().ManufacturingAdvance==null,"Full receipt history committed unresolvable choice.");
            });
            cases.Add("manufacturing_active_tool_excludes_recalibration_in_both_acquisition_orders",()=>{
                var facts=new SharedCraftingFixture(heroProficient:true,events:new[]{new CraftingMishapFact("calibrate",2)});var s=World(ManufacturePolicy(crafting:facts));CraftEvent(s,"calibrate");LearnManufacturing(s);HeroToWorkshop(s);ManufactureStart(s);WorldAdvance(s,100);
                RejectUnchanged(s,host,CraftCommand(s,"calibrate",CommandKind.StartCraftRemedy,hero),"CraftRemedyWorkerIneligible");Require(Order(s).Work.Partial==T(100),"Rejected calibration lost manufacturing phase.");
                ManufactureControl(s,CommandKind.PauseManufacturing);Remedy(s,"calibrate",hero);
                RejectUnchanged(s,host,ManufactureCommand(s,CommandKind.ResumeManufacturing,Order(s).Id),"ManufacturingToolInCalibration");
            });
            cases.Add("manufacturing_mid_tactical_slot_quality_continuation_finishes_original_end_once",()=>{
                var p=ManufacturePolicy(SeedForDeath(16));var s=World(p);LearnManufacturing(s);WorldAdvance(s,1);ManufactureStart(s,extra:2);WorldAdvance(s,14398);BeginEncounter(s);
                if(!s.Capture().Stances.Any(x=>x.TurnOrdinal==s.Capture().Encounter.TurnOrdinal))WorldCommit(s,Tac(s,CommandKind.SelectCombatStance,stance:(int)CombatStance.Guarded));
                ConnectedEnd(s); //17999 ->18000; still one active second short.
                WorldCommit(s,Tac(s,CommandKind.SelectCombatStance,stance:(int)CombatStance.Guarded));var end=Tac(s,CommandKind.EndRegularTurn);var result=s.Execute(host,end);
                Require(result.IsSuspended&&s.Capture().RuleClock==T(18001)&&s.Capture().ManufacturingAdvance.Target==T(18003)&&s.Capture().ManufacturingAdvance.OutgoingSlotId==end.Target,"Remote completion rounded, dropped or duplicated outgoing slot.");
                int prior=s.Capture().Encounter.TurnOrdinal;
                Require(s.Capture().Encounter.CurrentActor!=worker,"Fixture unexpectedly made the remote manufacturing owner the active tactical actor.");
                var choice=s.DiscoverCommands(host,worker).Single(x=>x.Command.Kind==CommandKind.ResolveManufacturingQuality
                    &&x.Command.Target==Order(s).Id&&x.Command.X==(int)CraftQualityChoice.FullYield&&x.Command.Y==1);
                byte[] beforeChoice=Bytes(s);var preview=s.QueryCommand(host,choice.Command);
                Require(choice.Query.Admissible&&preview.Supported&&preview.Admissible&&preview.Costs.Count==0&&Bytes(s).SequenceEqual(beforeChoice),
                    "Off-turn order owner did not receive a pure admissible quality choice without extra costs.");
                WorldCommit(s,choice.Command);
                Require(s.Capture().RuleClock==T(18003)&&s.Capture().Encounter.TurnOrdinal==prior+1&&!s.Execute(host,end).IsSuspended,"Settlement did not finish same original outgoing slot once.");
            });
            cases.Add("manufacturing_quality_uses_six_native_bands_without_natural20_shift",()=>{
                Require(ManufacturingRules.Quality(1,100,8)==CraftQuality.Mishap&&ManufacturingRules.Quality(20,-20,8)==CraftQuality.Failed,"Natural-die crafting overrides drifted.");
                foreach(var row in new[]{(-10,CraftQuality.Mishap),(-9,CraftQuality.Failed),(-5,CraftQuality.Failed),(-4,CraftQuality.Flawed),(-1,CraftQuality.Flawed),(0,CraftQuality.Standard),(4,CraftQuality.Standard),(5,CraftQuality.Exceptional),(9,CraftQuality.Exceptional),(10,CraftQuality.Masterwork)})
                    Require(ManufacturingRules.Quality(10,row.Item1,10)==row.Item2,"Wrong native band.");
                Require(ManufacturingRules.Yield(CraftQuality.Masterwork,1000000000,CraftQualityChoice.FullYield)==1500000000,"Representable large yield overflowed.");
            });
            cases.Add("manufacturing_source_training_take_ten_recovery_and_trade_arithmetic",()=>{
                Require(ManufacturingRules.Eligible(1,4,true,false,false)&&!ManufacturingRules.Eligible(1,5,true,true,true)&&!ManufacturingRules.Eligible(5,5,false,true,true)
                    &&ManufacturingRules.CanTakeTen(10,5,true,true,false)&&!ManufacturingRules.CanTakeTen(10,5,true,true,true),"Trade or take-ten gate drifted.");
                Require(ManufacturingRules.FailureRecovery(new RuleQuantity(5),true,false,false)==new RuleQuantity(1)&&ManufacturingRules.FailureRecovery(new RuleQuantity(5),true,false,true)==new RuleQuantity(5,4)
                    &&ManufacturingRules.FailureRecovery(new RuleQuantity(5),true,true,true)==default,"Recovery ignored units/catalyst flag.");
                Require(ManufacturingRules.FailureRecovery(new RuleQuantity(long.MaxValue),true,false,true)==new RuleQuantity(long.MaxValue,4),"Representable exact recovery overflowed before reduction.");
                var next=ManufacturingRules.AdvanceTrade(5,14,4);Require(next.Level==6&&next.Xp==3,"XP failed immediate threshold/excess.");
                Require(ManufacturingRules.TradeAward(CraftQuality.Standard,10,5,10,true,false,false,true,true,0)==0&&ManufacturingRules.TradeAward(CraftQuality.Failed,6,5,10,true,false,false,true,true,0)==0,"Trivial or below-level XP farm.");
            });
            cases.Add("manufacturing_explicit_schema18_requires_formula_training_and_actual_station",()=>{
                var s=World(ManufacturePolicy());Require(s.Capture().SchemaVersion==18&&RepairPolicy().Initial().SchemaVersion==17,"Manufacturing changed old schema.");
                RejectUnchanged(s,host,ManufactureCommand(s),"ManufacturingCredentialMissing");LearnManufacturing(s);ManufactureStart(s);
                foreach(var facts in new[]{new SharedManufacturingFixture(level:4),new SharedManufacturingFixture(toolTrained:false),new SharedManufacturingFixture(stationReady:false)}){
                    var denied=World(ManufacturePolicy(facts:facts));LearnManufacturing(denied);RejectUnchanged(denied,host,ManufactureCommand(denied),facts.StationReady?"ManufacturingCredentialMissing":"ManufacturingStationUnavailable");
                }
            });
            cases.Add("manufacturing_reserves_whole_batch_and_consumes_only_at_resolution",()=>{
                var s=World(ManufacturePolicy(SeedForDeath(6)));LearnManufacturing(s);ManufactureStart(s);WorldAdvance(s,900);
                Require(Material(s,0)==new RuleQuantity(5)&&s.Capture().Work.AvailableAmount(SharedManufacturingFixture.Lot(0,0))==default&&Order(s).StabilizedAt==T(4500),"Processing debited early or left double-spendable ingredients.");
                WorldAdvance(s,13500);Require(Order(s).Quality==CraftQuality.Standard&&Order(s).Status==ManufacturingStatus.Complete&&s.Capture().AlchemyDoses.Length==5&&Material(s,0)==default&&Order(s).XpAward==4,"Standard batch did not settle actual units.");
            });
            cases.Add("manufacturing_voluntary_stop_retains_completed_phase_loses_only_partial",()=>{
                var s=World(ManufacturePolicy(SeedForDeath(6)));LearnManufacturing(s);ManufactureStart(s);WorldAdvance(s,899);ManufactureControl(s,CommandKind.PauseManufacturing);
                Require(Order(s).Work.Retained==default&&Order(s).Work.Labor==T(899)&&Material(s,0)==new RuleQuantity(5),"Unfinished processing was retained or paid twice.");
                ManufactureControl(s,CommandKind.ResumeManufacturing);WorldAdvance(s,900);ManufactureControl(s,CommandKind.PauseManufacturing);
                Require(Order(s).Work.Retained==T(900)&&Order(s).StabilizedAt.HasValue,"Exact phase boundary was lost.");
                ManufactureControl(s,CommandKind.ResumeManufacturing);WorldAdvance(s,100);ManufactureControl(s,CommandKind.PauseManufacturing);
                Require(Order(s).Work.Retained==T(900)&&Order(s).Work.Labor==T(1899),"Later interruption lost completed processing or refunded labor.");
                ManufactureControl(s,CommandKind.ResumeManufacturing);WorldAdvance(s,13500);Require(Order(s).Status==ManufacturingStatus.Complete,"Same paid order could not resume.");
            });
            cases.Add("manufacturing_cancel_before_work_releases_after_work_spends_without_recovery",()=>{
                var s=World(ManufacturePolicy());LearnManufacturing(s);ManufactureStart(s,extra:2);ManufactureControl(s,CommandKind.CancelManufacturing);
                Require(Material(s,0)==new RuleQuantity(5),"Unstarted cancellation lost ingredients.");ManufactureStart(s,extra:2);WorldAdvance(s,1);ManufactureControl(s,CommandKind.CancelManufacturing);
                Require(Enumerable.Range(0,4).All(i=>Material(s,i)==default)&&s.Capture().Work.AvailableAmount(SharedManufacturingFixture.Packaging)==new RuleQuantity(4)
                    &&s.Capture().AlchemyDoses.Length==0&&s.Capture().Trades.Single().Xp==0,"Abandonment refunded consumed inputs, wasted independent packaging or granted XP.");
            });
            cases.Add("manufacturing_masterwork_pending_choice_freezes_roll_claims_and_saved_advance",()=>{
                var p=ManufacturePolicy(SeedForDeath(16));var s=World(p);LearnManufacturing(s);ManufactureStart(s,extra:2);
                var advance=IC(s,CommandKind.AdvanceClock,x:14401,y:1);var result=s.Execute(host,advance);
                Require(result.Outcome==Outcome.Committed&&result.IsSuspended&&s.Capture().RuleClock==T(18000)&&s.Capture().ManufacturingAdvance.Target==T(18001)&&Order(s).Natural==16,"Advance did not suspend at exact quality boundary.");
                uint rng=s.Capture().RandomState;byte[] bytes=Bytes(s);Require(s.Execute(host,advance).IsSuspended&&Bytes(s).SequenceEqual(bytes),"Duplicate restarted suspended advance.");
                var discovered=s.DiscoverCommands(host,worker);
                var activity=WorldActivityProjection.OpenProcedures(s.Capture(),discovered).Single(x=>x.Id==Order(s).Id);
                var qualityOptions=discovered.Where(x=>x.Command.Kind==CommandKind.ResolveManufacturingQuality
                    &&x.Command.Target==Order(s).Id).ToArray();
                var fullYieldCatalyst=qualityOptions.Single(x=>x.Command.X==(int)CraftQualityChoice.FullYield&&x.Command.Y==4);
                var invalidCatalyst=new Command("manufacturing.invalid-quality."+s.Capture().Revision,worker,s.Capture().Revision,
                    CommandKind.ResolveManufacturingQuality,Order(s).Id,(int)CraftQualityChoice.Durability,2);
                var invalidQuery=s.QueryCommand(host,invalidCatalyst);
                Require(activity.Status==ManufacturingStatus.AwaitingChoice.ToString()
                    &&activity.RecordedWorkDone==Order(s).Work.Retained&&activity.RecordedWorkRequired==Order(s).Work.Required
                    &&activity.ResourceReservations.SequenceEqual(s.Capture().Work.Reservations.Where(x=>x.JobId==Order(s).Id))
                    &&activity.AvailableCommands.Count==4&&qualityOptions.Length==4&&qualityOptions.All(x=>x.Query.Admissible)
                    &&activity.AvailableCommands.Any(x=>x.Command.Id==fullYieldCatalyst.Command.Id)
                    &&invalidQuery.Supported&&!invalidQuery.Admissible&&invalidQuery.Code=="InvalidRetainedCatalyst"
                    &&Bytes(s).SequenceEqual(bytes),
                    "Pending manufacturing choice projection, legal catalyst/yield discovery, invalid-query assessment, or read purity was incorrect.");
                RejectUnchanged(s,host,IC(s,CommandKind.AdvanceClock,x:1,y:1),"ManufacturingChoicePending");RejectUnchanged(s,host,ManufactureCommand(s,CommandKind.CancelManufacturing,Order(s).Id),"ManufacturingChoicePending");
                string path=Path.Combine(directory,"manufacturing-choice.bin");new FileSaveStore().Save(path,s.Capture());var loaded=new Simulation(p,new FileSaveStore().Load(path),ExecutionProfile.Laboratory);
                var restoredOptions=loaded.DiscoverCommands(host,worker);
                var restoredChoice=restoredOptions.Single(x=>x.Command.Id==fullYieldCatalyst.Command.Id);
                Require(restoredChoice.Command.Target==fullYieldCatalyst.Command.Target&&restoredChoice.Command.X==fullYieldCatalyst.Command.X
                    &&restoredChoice.Command.Y==fullYieldCatalyst.Command.Y&&restoredChoice.Query.Admissible,
                    "Restored manufacturing choice did not reconstruct the same admissible command.");
                WorldCommit(s,fullYieldCatalyst.Command);WorldCommit(loaded,restoredChoice.Command);
                Require(Bytes(s).SequenceEqual(Bytes(loaded))&&s.Capture().RuleClock==T(18001)&&s.Capture().ManufacturingAdvance==null&&s.Capture().RandomState==rng
                    &&s.Capture().AlchemyDoses.Length==7&&Material(s,3)==new RuleQuantity(1)&&s.Capture().Work.Lots.Single(x=>x.Id==SharedManufacturingFixture.Packaging).Amount==new RuleQuantity(2),"Settlement lost continuation or duplicated result.");
                byte[] settled=Bytes(s);Require(s.Execute(host,fullYieldCatalyst.Command).Outcome==Outcome.Duplicate&&Bytes(s).SequenceEqual(settled),
                    "Repeating the discovered manufacturing choice settled the order twice.");
                Require(!s.Execute(host,advance).IsSuspended&&s.Execute(host,advance).Outcome==Outcome.Duplicate,"Completed initiating command still suspended.");
            });
            cases.Add("manufacturing_missing_full_packaging_allows_only_durability_no_partial_yield",()=>{
                var s=World(ManufacturePolicy(SeedForDeath(16)));LearnManufacturing(s);ManufactureStart(s,extra:1);WorldAdvance(s,14400);
                RejectUnchanged(s,host,ManufactureCommand(s,CommandKind.ResolveManufacturingQuality,Order(s).Id,(int)CraftQualityChoice.FullYield,1),"ManufacturingFullYieldUnavailable");
                ManufactureChoice(s,CraftQualityChoice.Durability,0);
                Require(s.Capture().AlchemyDoses.Length==5&&s.Capture().AlchemyDoses.All(x=>x.Hp==2&&x.MaximumHp==2)&&Material(s,0)==new RuleQuantity(1)
                    &&s.Capture().Work.Lots.Single(x=>x.Id==SharedManufacturingFixture.Packaging).Amount==new RuleQuantity(4),"Durability combined yield/potency or spent unused packaging.");
            });
            cases.Add("manufacturing_exceptional_yield_retains_no_catalyst",()=>{
                var s=World(ManufacturePolicy(SeedForDeath(11)));LearnManufacturing(s);ManufactureStart(s,extra:1);WorldAdvance(s,14400);
                RejectUnchanged(s,host,ManufactureCommand(s,CommandKind.ResolveManufacturingQuality,Order(s).Id,1,1),"InvalidRetainedCatalyst");ManufactureChoice(s);
                Require(s.Capture().AlchemyDoses.Length==6&&Material(s,0)==default&&Material(s,3)==default,"Exceptional retained catalyst or wrong yield.");
            });
            cases.Add("manufacturing_flawed_output_and_concrete_failure_research_award",()=>{
                var s=World(ManufacturePolicy(SeedForDeath(2),new SharedManufacturingFixture(recordedFailureObservation:true)));LearnManufacturing(s);ManufactureStart(s);WorldAdvance(s,14400);
                Require(Order(s).Quality==CraftQuality.Flawed&&s.Capture().AlchemyDoses.Length==2&&Order(s).XpAward==1&&Order(s).FindingId=="observation.sediment-timing"&&s.Capture().Trades.Single().Findings.Count==1,"Flawed lost ordinary outputs or unsupported finding credit.");
            });
            cases.Add("manufacturing_injured_failed_result_recovers_exact_divisible_and_indivisible_inputs",()=>{
                var s=World(ManufacturePolicy(WoundedCheckSeed(Injury.FineMotorTrauma,2),crafting:new SharedCraftingFixture(companionHp:1,events:new[]{new CraftingMishapFact("acid",4)})));
                CraftEvent(s,"acid");WorldAdvance(s,6);LearnManufacturing(s);ManufactureStart(s);WorldAdvance(s,14400);
                Require(Order(s).Quality==CraftQuality.Failed&&s.Capture().AlchemyDoses.Length==0&&Material(s,0)==default&&Material(s,3)==default&&Material(s,1)==new RuleQuantity(1)&&Material(s,2)==new RuleQuantity(5,4),"Failure recovery lost exact identity/unit rules.");
            });
            cases.Add("manufacturing_all_six_native_mishaps_dispatch_actual_order_and_spent_inputs",()=>{
                for(int mishap=1;mishap<=6;mishap++){
                    var s=World(ManufacturePolicy(ManufacturingMishapSeed(mishap),new SharedManufacturingFixture(xp:14,recordedFailureObservation:true)));LearnManufacturing(s);ManufactureStart(s);WorldAdvance(s,14400);
                    var j=Order(s);var incident=s.Capture().CraftingIncidents.Single();Require(j.Mishap==mishap&&j.Quality==CraftQuality.Mishap&&j.Status==ManufacturingStatus.Complete&&incident.LeadId==worker
                        &&incident.ParticipantIds.SequenceEqual(new[]{worker})&&Enumerable.Range(0,4).All(i=>Material(s,i)==default)&&s.Capture().AlchemyDoses.Length==0,"Native mishap bypassed order/input settlement.");
                    Require(j.XpAward==(mishap==6?0:1)&&s.Capture().Trades.Single().Level==(mishap==6?5:6),"Mishap6 awarded/advanced before lost-log exclusion.");
                }
            });
            cases.Add("manufacturing_returned_blood_resumes_original_age_after_stabilized_mixture",()=>{
                var p=ManufacturePolicy(SeedForDeath(16));var s=World(p);LearnManufacturing(s);ManufactureStart(s,extra:2);WorldAdvance(s,14400);ManufactureChoice(s,catalyst:3);
                Require(p.BloodUnprotectedAge(s.Capture(),0)==T(4500)&&p.BloodUnprotectedAge(s.Capture(),1)==T(18000),"Returned blood reset Fresh or aged while bound.");WorldAdvance(s,100);
                Require(p.BloodUnprotectedAge(s.Capture(),0)==T(4600),"Returned catalyst clock did not resume.");
            });
            cases.Add("manufacturing_raw_spoilage_before_processing_pauses_without_new_batch",()=>{
                var s=World(ManufacturePolicy(facts:new SharedManufacturingFixture(bloodIntervalSeconds:3600)));LearnManufacturing(s);WorldAdvance(s,3000);ManufactureStart(s);WorldAdvance(s,600);
                Require(Order(s).Status==ManufacturingStatus.Paused&&Order(s).Work.Labor==T(600)&&Order(s).Work.Retained==default&&Material(s,3)==new RuleQuantity(1),"Raw spoilage created stabilized mixture or discarded reservations.");
                RejectUnchanged(s,host,ManufactureCommand(s,CommandKind.ResumeManufacturing,Order(s).Id),"ManufacturingIngredientSpoiled");
            });
            cases.Add("manufacturing_stabilization_requires_usable_ingredient_at_exact_endpoint",()=>{
                foreach(int delay in new[]{2699,2700}){
                    var s=World(ManufacturePolicy(facts:new SharedManufacturingFixture(bloodIntervalSeconds:3600)));LearnManufacturing(s);WorldAdvance(s,delay);ManufactureStart(s);
                    uint rng=s.Capture().RandomState;WorldAdvance(s,900);var j=Order(s);
                    Require(j.Work.Labor==T(900)&&s.Capture().RandomState==rng&&s.Capture().AlchemyDoses.Length==0&&Material(s,3)==new RuleQuantity(1),"Processing changed RNG/output/inputs or refunded actual labor.");
                    Require(delay==2699?j.StabilizedAt==T(7199)&&j.Work.CompletedPhases==1&&j.Status==ManufacturingStatus.Working
                        :!j.StabilizedAt.HasValue&&j.Work.Retained==default&&j.Status==ManufacturingStatus.Paused,"Exact spoilage/stabilization priority was reversed.");
                }
            });
            cases.Add("manufacturing_awaiting_check_preserves_completed_labor_then_one_explicit_roll",()=>{
                var cure=new ConditionFixtureEvent(worker,ConditionOperation.Cure("event.cure",new ConditionStamp(T(18001)),"Stunned"));
                var p=ManufacturePolicy(SeedForDeath(6),conditions:new ConditionCombatFixture(CCApply("stun","Stunned",worker),CCGrant("ward",worker,new ConditionStamp(T(18000)),"Stunned"),cure));var s=World(p);
                CCDispatch(s,"stun",worker);CCDispatch(s,"ward",worker);LearnManufacturing(s);ManufactureStart(s);uint rng=s.Capture().RandomState;WorldAdvance(s,14400);
                Require(Order(s).Status==ManufacturingStatus.AwaitingCheck&&Order(s).Work.Complete&&s.Capture().RandomState==rng&&s.Capture().AlchemyDoses.Length==0,"Incapable endpoint rolled or erased completed work.");
                var awaiting=WorldActivityProjection.OpenProcedures(s.Capture(),s.DiscoverCommands(host,worker)).Single(x=>x.Id==Order(s).Id);
                Require(awaiting.Kind==WorldProcedureKind.Manufacturing&&awaiting.Status==ManufacturingStatus.AwaitingCheck.ToString()
                    &&awaiting.RecordedWorkRequired==Order(s).Work.Required,"Open activity view omitted the saved manufacturing check state.");
                string path=Path.Combine(directory,"manufacturing-awaiting.bin");new FileSaveStore().Save(path,s.Capture());s=new Simulation(p,new FileSaveStore().Load(path),ExecutionProfile.Laboratory);
                WorldAdvance(s,1);CCDispatch(s,"cure",worker);ManufactureControl(s,CommandKind.ResumeManufacturing);
                Require(Order(s).Status==ManufacturingStatus.Complete&&Order(s).Work.Labor==T(14400)&&s.Capture().RuleClock==T(18001),"Earned check added labor or failed to resolve once.");
            });
            cases.Add("manufacturing_tactical_bench_dose_spends_action_heals_and_returns_exact_empty_vial",()=>{
                var p=ManufacturePolicy(TacticalSeed(6,4,3),crafting:new SharedCraftingFixture(heroHp:1));var s=World(p);LearnManufacturing(s);ManufactureStart(s);WorldAdvance(s,14400);HeroToWorkshop(s);WorldAdvance(s,1);BeginEncounter(s);
                var dose=s.Capture().AlchemyDoses[0];var use=DoseCommand(s,dose.Id);WorldCommit(s,use);var spent=s.Capture().AlchemyDoses.Single(x=>x.Id==dose.Id);
                Require(spent.Spent&&spent.ActualHealing>0&&Life(s).Hp==1+spent.ActualHealing&&spent.MassPounds==new RuleQuantity(1,10)&&spent.Hp==dose.Hp&&spent.OwnerId==dose.OwnerId
                    &&spent.LocationId==dose.LocationId&&WorldLedger(s).ActionSpent&&s.Capture().RuleClock==T(18006),"Potion invented nutrition/time, lost empty vial or missed healing/Action.");
                byte[] bytes=Bytes(s);Require(s.Execute(host,use).Outcome==Outcome.Duplicate&&Bytes(s).SequenceEqual(bytes),"Duplicate potion replayed healing.");
                RejectUnchanged(s,host,DoseCommand(s,s.Capture().AlchemyDoses[1].Id),"ActionAlreadySpent");
                string path=Path.Combine(directory,"manufacturing-used-dose.bin");new FileSaveStore().Save(path,s.Capture());Require(Bytes(new Simulation(p,new FileSaveStore().Load(path),ExecutionProfile.Laboratory)).SequenceEqual(bytes),"Used dose/empty vial did not persist.");
            });
            cases.Add("manufacturing_dose_requires_own_turn_reach_ingestion_and_current_owner_grant",()=>{
                var s=World(ManufacturePolicy(SeedForDeath(6),new SharedManufacturingFixture(compatibleIngestion:false)));LearnManufacturing(s);ManufactureStart(s);WorldAdvance(s,14400);var dose=s.Capture().AlchemyDoses[0];
                RejectUnchanged(s,host,DoseCommand(s,dose.Id),"AlchemyOwnTacticalTurnRequired");BeginEncounter(s);RejectUnchanged(s,host,DoseCommand(s,dose.Id),"AlchemyDoseOutOfReach");
                var revoked=new Authority(host.Principal,new[]{hero});RejectUnchanged(s,revoked,DoseCommand(s,dose.Id),"InventoryNotAuthorized");
                // A separate lawful sequence reaches the bench before tactical entry.
                var near=World(ManufacturePolicy(SeedForDeath(6),new SharedManufacturingFixture(compatibleIngestion:false)));LearnManufacturing(near);ManufactureStart(near);WorldAdvance(near,14400);HeroToWorkshop(near);WorldAdvance(near,1);BeginEncounter(near);
                RejectUnchanged(near,host,DoseCommand(near,near.Capture().AlchemyDoses[0].Id),"AlchemyRecipientCannotIngest");
            });
            cases.Add("manufacturing_full_hp_still_spends_actual_dose_and_action",()=>{
                var s=World(ManufacturePolicy(SeedForDeath(6)));LearnManufacturing(s);ManufactureStart(s);WorldAdvance(s,14400);HeroToWorkshop(s);WorldAdvance(s,1);BeginEncounter(s);
                WorldCommit(s,DoseCommand(s,s.Capture().AlchemyDoses[0].Id));var used=s.Capture().AlchemyDoses.Single(x=>x.Spent);
                Require(used.ActualHealing==0&&used.PotentialHealing>=4&&Life(s).Hp==26&&WorldLedger(s).ActionSpent,"Zero-benefit use refunded dose, Action or over-healed.");
            });
            cases.Add("manufacturing_dose_positive_hp_ends_remote_dying_without_curing_independent_causes",()=>{
                var p=ManufacturePolicy(SeedForDeath(6),crafting:new SharedCraftingFixture(companionHp:1,events:new[]{new CraftingMishapFact("late-acid",4,at:T(18006))}),
                    conditions:new ConditionCombatFixture(CCApply("independent-sleep","Unconscious",worker,at:new ConditionStamp(T(18006)))));
                var s=World(p);LearnManufacturing(s);ManufactureStart(s);WorldAdvance(s,14400);HeroToWorkshop(s);WorldAdvance(s,1);CCDispatch(s,"independent-sleep",worker);CraftEvent(s,"late-acid");
                Require(Life(s,worker).Hp==0&&s.Capture().DyingCadences.Length==1,"Fixture failed to create actual off-roster dying.");BeginEncounter(s);
                WorldCommit(s,DoseCommand(s,s.Capture().AlchemyDoses[0].Id,worker));
                Require(Life(s,worker).Hp>0&&Life(s,worker).Prone&&Life(s,worker).LinkedInjuries.Count==1&&s.Capture().DyingCadences.Length==0
                    &&CCState(s,worker).View().Has(ConditionKind.Unconscious),"Healing missed zero-HP cleanup or cured unrelated posture/Injury/sleep.");
            });
            cases.Add("manufacturing_canonical_restore_rejects_forged_trade_or_missing_output",()=>{
                var p=ManufacturePolicy(SeedForDeath(6));var s=World(p);LearnManufacturing(s);ManufactureStart(s);WorldAdvance(s,14400);
                var forged=s.Capture();forged.Trades=new[]{new TradeProgressRecord(worker,SharedCraftingFixture.TradeId,9,0)};
                Throws<ArgumentException>(()=>new Simulation(p,forged,ExecutionProfile.Laboratory));
                forged=s.Capture();forged.AlchemyDoses=forged.AlchemyDoses.Skip(1).ToArray();
                Throws<ArgumentException>(()=>new Simulation(p,forged,ExecutionProfile.Laboratory));
            });
        }
    }
}
#endif
