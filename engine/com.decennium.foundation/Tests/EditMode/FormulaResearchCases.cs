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
        private static TestOnlySharedWorldPolicy ResearchPolicy(uint seed = 1, SharedResearchFixture facts = null, ConditionCombatFixture conditions = null)
            => new TestOnlySharedWorldPolicy(new SharedCombatFixture(seed: seed), facts ?? new SharedResearchFixture(), conditions: conditions);
        private static Command ResearchCommand(Simulation s, CommandKind kind = CommandKind.StartFormulaResearch, string target = null, int method = 0, string worker = TestOnlyPolicy.CompanionId,string recipe=SharedResearchFixture.Recipe)
            => new Command("research." + (s.Capture().Revision + 1), worker, s.Capture().Revision, kind, target??SharedResearchFixture.EvidenceFor(recipe,copy:kind==CommandKind.StartFormulaCopy), method,
                kind==CommandKind.StartFormulaResearch||kind==CommandKind.StartFormulaCopy?SharedResearchFixture.Selector(recipe):0);
        private static FormulaWorkRecord ResearchJob(Simulation s) => s.Capture().FormulaWork.Last();
        private static void ResearchStart(Simulation s, string evidence = null, int method = 0, bool copy = false, string worker = TestOnlyPolicy.CompanionId,string recipe=SharedResearchFixture.Recipe)
            => WorldCommit(s, ResearchCommand(s, copy ? CommandKind.StartFormulaCopy : CommandKind.StartFormulaResearch, evidence??SharedResearchFixture.EvidenceFor(recipe,copy:copy), method, worker,recipe));
        private static void ResearchControl(Simulation s, CommandKind kind, string worker = TestOnlyPolicy.CompanionId)
            => WorldCommit(s, ResearchCommand(s, kind, ResearchJob(s).Id, worker: worker,recipe:ResearchJob(s).RecipeId));
        private static RuleQuantity WritingStock(Simulation s) => s.Capture().Work.Lots.Single(x => x.Id == SharedResearchFixture.Supplies).Amount;

        private static TestOnlySharedWorldPolicy ResearchStationPolicy(uint seed,TestOnlyResearchStationProfile station=null,
            SharedResearchFixture research=null,SharedCraftingFixture crafting=null,ConditionCombatFixture conditions=null)
        {
            var policy=new TestOnlySharedWorldPolicy(new SharedCombatFixture(seed:seed),research??new SharedResearchFixture(),
                crafting??new SharedCraftingFixture(),new SharedRepairFixture(),conditions:conditions);
            return station==null?policy:policy.EnableResearchStation(station);
        }

        private static void ResearchStationAudit(string directory,string label,Snapshot before,Snapshot after,int bonus,string eligibility)
        {
            var job=after.FormulaWork.Last();
            var actor=CharacterStateFacts.ForActor(before,job.WorkerId);
            int ability=actor.Rules.AbilityModifier(CharacterAbility.Intelligence),proficiency=actor.Rules.ProficiencyBonus;
            int injury=actor.InjuryPenalty(CharacterAbility.Intelligence,toolCheck:true);
            int dc=SharedResearchFixture.Difficulty(job.RecipeId);
            bool poisoned=TestOnlyClubAttackPolicy.ConditionsFor(before,job.WorkerId).View().Has(ConditionKind.Poisoned);
            var roll=PlaytestDice.RollD20(before.RandomState,disadvantageSources:poisoned?1:0);
            var expected=PlaytestRolls.TaskCheck(roll.Natural,ability+proficiency+injury+bonus,dc).Degree>=TaskDegree.Success
                ?FormulaWorkStatus.Success:FormulaWorkStatus.Failure;
            Require(job.Status==expected&&job.First==roll.First&&job.Second==(roll.Second??0)&&job.Natural==roll.Natural
                &&after.RandomState==roll.NextRandomState&&job.Work.Labor==T(28800)&&after.Revision==before.Revision+1,
                "Research check or elapsed labor differed from the audited inputs for "+label+".");
            var station=before.Structures.SingleOrDefault(x=>x.Id==TestOnlyResearchStationProfile.InstanceId);
            var receipt=after.Receipts.Single(x=>x.Revision==after.Revision);
            var path=Path.Combine(directory,"research-check-audit.tsv");
            if(!File.Exists(path))File.WriteAllLines(path,new[]{"witness\twork\tworker\trecipe\tevidence\tmethod\tresolved_at\trevision\tcommand"
                +"\tstation\teligibility\tbonus\tability\tproficiency\tinjury\tdc\tselection\tfirst\tsecond\tnatural\trng_before\trng_after\twords\tresult"});
            File.AppendAllLines(path,new[]{string.Join("\t",label,
                job.Id,job.WorkerId,job.RecipeId,job.EvidenceId,job.MethodId,job.UpdatedAt,receipt.Revision,receipt.Id,
                station?.Id??"ordinary",eligibility,bonus,ability,proficiency,injury,dc,roll.Selection,
                roll.First,roll.Second??0,roll.Natural,before.RandomState,after.RandomState,roll.WordsConsumed,job.Status)});
        }

        private static void AddResearchStationCases(Dictionary<string,Action> cases,string directory)
        {
            var host=TestOnlySharedWorldPolicy.Host();
            const string worker=TestOnlyPolicy.CompanionId;
            uint thresholdSeed=ManufacturingNaturalSeed(4);
            const string blocked="research-station-spill";
            CraftingMishapFact Spill(int at)=>new CraftingMishapFact(blocked,1,at:T(at),stationId:TestOnlyResearchStationProfile.InstanceId);

            cases.Add("mgt09_research_station_exact_bonus_connected_save_and_historical_result",()=>{
                var crafting=new SharedCraftingFixture(events:new[]{Spill(28800)});
                var ordinary=ResearchStationPolicy(thresholdSeed,crafting:crafting);
                var qualified=ResearchStationPolicy(thresholdSeed,new TestOnlyResearchStationProfile(),crafting:crafting);
                var baseline=World(ordinary);var station=World(qualified);
                var start=ResearchCommand(station);
                var store=new FileSaveStore();var codec=new SnapshotCodec();
                foreach(var run in new[]{baseline,station}) {
                    WorldCommit(run,start);WorldAdvance(run,14400);
                    Require(run.Capture().SchemaVersion==Snapshot.RepairWorkSchema&&ResearchJob(run).Work.Labor==T(14400)
                        &&WritingStock(run)==Q(3)&&!FormulaResearchRules.Knows(run.Capture(),worker,SharedResearchFixture.Recipe),
                        "Partial research spent materials or granted knowledge.");
                }
                var partial=Path.Combine(directory,"station-research-midwork.ddsave");
                store.Save(partial,station.Capture());
                var restored=new Simulation(qualified,store.Load(partial),ExecutionProfile.Laboratory);
                Throws<ArgumentException>(()=>new Simulation(ordinary,store.Load(partial),ExecutionProfile.Laboratory));
                foreach(var run in new[]{baseline,station,restored}) {
                    var before=run.Capture();WorldAdvance(run,14400);var after=run.Capture();
                    bool eligible=run!=baseline;
                    ResearchStationAudit(directory,eligible?"functioning":"ordinary",before,after,eligible?2:0,
                        eligible?"functioning at check":"ordinary workspace only");
                    var result=ResearchJob(run);
                    Require(result.Natural==4&&result.Status==(eligible?FormulaWorkStatus.Success:FormulaWorkStatus.Failure)
                        &&after.ManufacturingOrders.Length==0&&after.AlchemyDoses.Length==0&&after.Trades.Length==0
                        &&after.SkillTraining.SequenceEqual(before.SkillTraining)&&WritingStock(run)==Q(3)
                        &&FormulaResearchRules.Knows(after,worker,SharedResearchFixture.Recipe)==eligible,
                        "The +2 witness did not preserve the source-bound knowledge-only result.");
                }
                Require(Bytes(station).SequenceEqual(Bytes(restored))&&baseline.Capture().RandomState==station.Capture().RandomState,
                    "Station modifier changed the roll stream or deterministic restoration.");
                byte[] resolved=Bytes(station);
                Require(station.Execute(host,start).Outcome==Outcome.Duplicate&&resolved.SequenceEqual(Bytes(station)),"Retry changed a resolved check.");
                var conflict=new Command(start.Id,start.Actor,start.ExpectedRevision,start.Kind,SharedResearchFixture.FreshEvidence);
                RejectUnchanged(station,host,conflict,"CommandIdConflict");
                foreach(var run in new[]{station,restored})CraftEvent(run,blocked);
                var now=station.Capture();
                Require(CraftingRestrictions.StationUseBlocked(now,TestOnlyResearchStationProfile.InstanceId)
                    &&ResearchJob(station).Status==FormulaWorkStatus.Success&&Bytes(station).SequenceEqual(Bytes(restored)),
                    "A later same-time spill rewrote the earlier +2 check.");
                var settled=Path.Combine(directory,"station-research-resolved-then-blocked.ddsave");
                store.Save(settled,now);
                Require(Bytes(station).SequenceEqual(Bytes(new Simulation(qualified,store.Load(settled),ExecutionProfile.Laboratory))),
                    "Replay used current facility state instead of the historical check boundary.");
                var forged=codec.Decode(Bytes(station));
                var old=forged.FormulaWork.Single();
                forged.FormulaWork=new[]{new FormulaWorkRecord(old.Id,old.WorkerId,old.RecipeId,old.EvidenceId,old.MethodId,
                    old.Kind,FormulaWorkStatus.Failure,old.StartedAt,old.UpdatedAt,old.Work,old.First,old.Second,old.Natural)};
                Throws<ArgumentException>(()=>new Simulation(qualified,forged,ExecutionProfile.Laboratory));
                forged=codec.Decode(Bytes(station));
                forged.Structures=forged.Structures.Where(x=>x.Id!=TestOnlyResearchStationProfile.InstanceId).ToArray();
                Throws<ArgumentException>(()=>new Simulation(qualified,forged,ExecutionProfile.Laboratory));
            });

            cases.Add("mgt09_research_station_unavailable_variants_and_supported_spill_fall_back",()=>{
                var variants=new[]{(new TestOnlyResearchStationProfile(intact:false),"broken"),
                    (new TestOnlyResearchStationProfile(atWorksite:false),"offsite"),
                    (new TestOnlyResearchStationProfile(lawfulUse:false),"permission absent"),
                    (new TestOnlyResearchStationProfile(furnishingsInstalled:false),"furnishings absent despite profile label")};
                foreach(var (profile,reason) in variants) {
                    var run=World(ResearchStationPolicy(thresholdSeed,profile));
                    ResearchStart(run);var before=run.Capture();WorldAdvance(run,28800);
                    ResearchStationAudit(directory,reason,before,run.Capture(),0,reason);
                    Require(ResearchJob(run).Status==FormulaWorkStatus.Failure,"Unavailable facility supplied a bonus.");
                }
                var live=World(ResearchStationPolicy(thresholdSeed,new TestOnlyResearchStationProfile(),
                    crafting:new SharedCraftingFixture(events:new[]{Spill(14400)})));
                ResearchStart(live);WorldAdvance(live,14400);CraftEvent(live,blocked);
                var obstructed=live.Capture();
                Require(ResearchJob(live).Status==FormulaWorkStatus.Working
                    &&CraftingRestrictions.StationUseBlocked(obstructed,TestOnlyResearchStationProfile.InstanceId)
                    &&!CraftingRestrictions.StationUseBlocked(obstructed,SharedCraftingFixture.StationId),
                    "A bonus-facility spill blocked independent ordinary research.");
                WorldAdvance(live,14400);
                ResearchStationAudit(directory,"spill before completion",obstructed,live.Capture(),0,"station use blocked");
                Require(ResearchJob(live).Status==FormulaWorkStatus.Failure,"Eligible completion waited for or used the blocked bonus.");
            });

            cases.Add("mgt09_research_station_does_not_waive_independent_gates",()=>{
                var bonus=new TestOnlyResearchStationProfile();
                foreach(var (facts,code) in new[]{(new SharedResearchFixture(qualified:false),"ResearchCredentialMissing"),
                    (new SharedResearchFixture(accessible:false),"ResearchEvidenceUnavailable"),
                    (new SharedResearchFixture(sufficient:false),"ResearchEvidenceUnavailable"),
                    (new SharedResearchFixture(stationSuitable:false),"ResearchStationUnavailable")}) {
                    var run=World(ResearchStationPolicy(thresholdSeed,bonus,facts));
                    RejectUnchanged(run,host,ResearchCommand(run),code);
                }
                var tool=World(ResearchStationPolicy(thresholdSeed,bonus,crafting:new SharedCraftingFixture(toolHp:0)));
                RejectUnchanged(tool,host,ResearchCommand(tool),"ResearchToolsOrStationUnavailable");
                var moving=World(ResearchStationPolicy(thresholdSeed,bonus));
                WorldStep(moving,-1,0,actor:worker);
                RejectUnchanged(moving,host,ResearchCommand(moving),"ResearchStationOutOfReach");
                var hero=World(ResearchStationPolicy(thresholdSeed,new TestOnlyResearchStationProfile(TestOnlyPolicy.ActorId),
                    new SharedResearchFixture(TestOnlyPolicy.ActorId)));
                RejectUnchanged(hero,host,ResearchCommand(hero,worker:TestOnlyPolicy.ActorId),"ResearchStationOutOfReach");
                HeroToWorkshop(hero);BeginEncounter(hero);
                RejectUnchanged(hero,host,ResearchCommand(hero,worker:TestOnlyPolicy.ActorId),"ResearchParticipantInCombat");
                var late=World(ResearchStationPolicy(thresholdSeed,bonus));WorldAdvance(late,57600);
                RejectUnchanged(late,host,ResearchCommand(late),"ResearchWorkWindowClosed");
                var failed=World(ResearchStationPolicy(ManufacturingNaturalSeed(2),bonus));
                ResearchStart(failed);WorldAdvance(failed,28800);
                Require(ResearchJob(failed).Status==FormulaWorkStatus.Failure,"Retry fixture must fail its first roll.");
                RejectUnchanged(failed,host,ResearchCommand(failed),"UnchangedResearchEvidence");
            });

            cases.Add("mgt09_research_station_awaiting_check_uses_current_availability_after_restore",()=>{
                var cure=new ConditionFixtureEvent(worker,ConditionOperation.Cure("event.cure",new ConditionStamp(T(57601)),"Stunned"));
                var conditions=new ConditionCombatFixture(CCApply("stun","Stunned",worker),CCGrant("ward",worker,new ConditionStamp(T(57600)),"Stunned"),cure);
                var policy=ResearchStationPolicy(thresholdSeed,new TestOnlyResearchStationProfile(),
                    crafting:new SharedCraftingFixture(events:new[]{Spill(57600)}),conditions:conditions);
                var run=World(policy);CCDispatch(run,"stun",worker);CCDispatch(run,"ward",worker);
                WorldAdvance(run,28800);ResearchStart(run);var rng=run.Capture().RandomState;WorldAdvance(run,28800);
                Require(ResearchJob(run).Status==FormulaWorkStatus.AwaitingCheck&&ResearchJob(run).Work.Complete
                    &&run.Capture().RandomState==rng,"Fully worked incapacity consumed a research roll.");
                var path=Path.Combine(directory,"station-research-awaiting.ddsave");
                var store=new FileSaveStore();store.Save(path,run.Capture());
                var restored=new Simulation(policy,store.Load(path),ExecutionProfile.Laboratory);
                foreach(var branch in new[]{run,restored}) {
                    CraftEvent(branch,blocked);
                    RejectUnchanged(branch,host,ResearchCommand(branch,CommandKind.ResumeFormulaWork,ResearchJob(branch).Id),"ResearchWorkerIncapable");
                    WorldAdvance(branch,1);CCDispatch(branch,"cure",worker);var before=branch.Capture();
                    Require(ResearchJob(branch).Status==FormulaWorkStatus.AwaitingCheck&&before.RandomState==rng,"Restored eligibility automatically resolved waiting research.");
                    var complete=ResearchCommand(branch,CommandKind.ResumeFormulaWork,ResearchJob(branch).Id);
                    WorldCommit(branch,complete);
                    ResearchStationAudit(directory,"awaiting after spill",before,branch.Capture(),0,"station use blocked");
                    Require(ResearchJob(branch).Status==FormulaWorkStatus.Failure&&branch.Capture().RuleClock==T(57601)
                        &&branch.Execute(host,complete).Outcome==Outcome.Duplicate,"Deferred check repeated time, work or RNG.");
                }
                Require(Bytes(run).SequenceEqual(Bytes(restored)),"Deferred check replay diverged.");
            });

            cases.Add("mgt09_research_station_preserves_poison_injury_copying_and_manufacture",()=>{
                var conditions=new ConditionCombatFixture(CCApply("poison","Poisoned",worker,at:CJAt(6)));
                uint seed=0;
                for(uint probe=1;probe<2000000;probe++) {
                    var d4=DiceStream.Draw(probe,4);
                    var damage=PlaytestDamageDice.Resolve(new LifeState(26,1),d4.Value+1,default,d4.NextState);
                    if(damage.InjuryD6!=(int)Injury.FineMotorTrauma)continue;
                    var recovery=PlaytestDice.RollD20(damage.NextRandomState);
                    if(recovery.Natural!=20)continue;
                    var check=PlaytestDice.RollD20(recovery.NextRandomState,disadvantageSources:1);
                    if(check.Natural==4&&check.First!=4) { seed=probe;break; }
                }
                Require(seed!=0,"No injury and disadvantage witness seed.");
                var poisoned=World(ResearchStationPolicy(seed,new TestOnlyResearchStationProfile(),
                    crafting:new SharedCraftingFixture(companionHp:1,events:new[]{new CraftingMishapFact("acid",4)}),conditions:conditions));
                CraftEvent(poisoned,"acid");WorldAdvance(poisoned,6);CCDispatch(poisoned,"poison",worker);
                ResearchStart(poisoned);WorldAdvance(poisoned,28794);ResearchControl(poisoned,CommandKind.ResumeFormulaWork);
                var before=poisoned.Capture();WorldAdvance(poisoned,6);
                ResearchStationAudit(directory,"poisoned and injured",before,poisoned.Capture(),2,"functioning at check");
                Require(CharacterStateFacts.ForActor(before,worker).InjuryPenalty(CharacterAbility.Intelligence,toolCheck:true)==-1
                    &&ResearchJob(poisoned).Natural==4&&ResearchJob(poisoned).First!=4&&ResearchJob(poisoned).Status==FormulaWorkStatus.Failure,
                    "Station bypassed Poisoned or the injury that keeps total below the exact DC.");
                var plain=World(ManufacturePolicy(SeedForDeath(6)));
                var station=World(ManufacturePolicy(SeedForDeath(6)).EnableResearchStation(new TestOnlyResearchStationProfile()));
                foreach(var run in new[]{plain,station}) {
                    uint random=run.Capture().RandomState;LearnManufacturing(run);
                    Require(run.Capture().RandomState==random&&ResearchJob(run).Work.Labor==T(3600)
                        &&ResearchJob(run).Natural==0&&WritingStock(run)==Q(2),"Station changed copying cost or rolled a check.");
                    ManufactureStart(run);WorldAdvance(run,14400);
                }
                Require(Order(plain).Quality==CraftQuality.Standard&&Order(plain).Quality==Order(station).Quality
                    &&Order(plain).XpAward==Order(station).XpAward&&Order(plain).Natural==Order(station).Natural
                    &&plain.Capture().RandomState==station.Capture().RandomState,"The station bonus leaked into manufacturing.");
            });
        }

        private static void AddFormulaResearchCases(Dictionary<string, Action> cases, string directory)
        {
            AddResearchStationCases(cases,directory);
            var host = TestOnlySharedWorldPolicy.Host();
            cases.Add("active_work_phase_interruption_loses_only_unfinished_phase", () => {
                var work = new ActiveWorkProgress(new[] { T(28800), T(28800), T(14400) }).Credit(T(36001, 2));
                Require(work.Interrupt(false).Retained == T(36001, 2), "Knowledge retention rounded labor.");
                var lost = work.Interrupt(true);
                Require(lost.Retained == default && lost.Labor == T(36001, 2), "Unfinished first phase was kept or labor refunded.");
            });
            cases.Add("active_work_phase_boundary_and_actual_labor_survive_loss", () => {
                var work = new ActiveWorkProgress(new[] { T(28800), T(28800), T(14400) }).Credit(T(36000));
                var lost = work.Interrupt(true);
                Require(lost.CompletedPhases == 1 && lost.Partial == default && lost.Retained == T(28800) && lost.Labor == T(36000), "Forced interruption erased completed phase or refunded labor.");
                var done = lost.Credit(T(43200)); Require(done.Complete && done.Retained == T(72000) && done.Labor == T(79200), "Phase resumption double counted lost work.");
                Throws<ArgumentException>(() => done.Credit(T(1)));
            });
            cases.Add("active_work_phase_inputs_detached_and_invalid_credit_rejected", () => {
                var phases = new[] { T(1, 2), T(1, 3) }; var work = new ActiveWorkProgress(phases); phases[0] = T(99);
                Require(work.Required == T(5, 6) && work.Credit(T(5, 6)).Complete, "Phase plan was not detached/exact.");
                Throws<ArgumentException>(() => work.Credit(default)); Throws<ArgumentException>(() => work.Credit(T(1)));
                Throws<ArgumentException>(() => new ActiveWorkProgress(new[] { T(1) }, partial: T(1, 2)));
            });
            cases.Add("formula_research_duration_and_binary_task_degrees_are_source_bound", () => {
                Require(FormulaResearchRules.RequiredTime(0) == T(28800) && FormulaResearchRules.RequiredTime(20) == T(72000), "Research minimum or full retry duration changed.");
                Require(!FormulaResearchRules.Succeeds(5, 2, 8) && FormulaResearchRules.Succeeds(6, 2, 8), "Research DC edge wrong.");
                Require(!FormulaResearchRules.Succeeds(1, 7, 8) && FormulaResearchRules.Succeeds(1, 17, 8)
                    && FormulaResearchRules.Succeeds(20, -13, 8) && !FormulaResearchRules.Succeeds(20, -30, 8), "Task natural shifts became saving throws or automatic successes.");
            });
            cases.Add("formula_research_recipe14_uses_its_exact_recipe_dc_without_granting_recipe4",()=>{
                var facts=new SharedResearchFixture(recipeId:SharedResearchFixture.Recipe14);
                var s=World(ResearchPolicy(ManufacturingNaturalSeed(7),facts));ResearchStart(s,recipe:SharedResearchFixture.Recipe14);WorldAdvance(s,28800);
                Require(ResearchJob(s).RecipeId==SharedResearchFixture.Recipe14&&ResearchJob(s).Natural==7
                    &&ResearchJob(s).Status==FormulaWorkStatus.Failure
                    &&!FormulaResearchRules.Knows(s.Capture(),TestOnlyPolicy.CompanionId,SharedResearchFixture.Recipe14)
                    &&!FormulaResearchRules.Knows(s.Capture(),TestOnlyPolicy.CompanionId,SharedResearchFixture.Recipe),
                    "Recipe-14 research ignored its DC 11 or granted knowledge after a failed check.");
            });
            cases.Add("formula_research_schema15_is_explicit_and_authority_checked", () => {
                var p = ResearchPolicy(); var s = World(p);
                Require(s.Capture().SchemaVersion == 15 && ConnectedPolicy().Initial().SchemaVersion == 14, "Research changed an older profile.");
                Throws<InvalidOperationException>(() => new Simulation(p, p.Initial(), ExecutionProfile.Release));
                RejectUnchanged(s, new Authority("guest", new[] { TestOnlyPolicy.ActorId }), ResearchCommand(s), "NotAuthorized");
                RejectUnchanged(s, new Authority("guest", new[] { TestOnlyPolicy.CompanionId }), ResearchCommand(s, CommandKind.StartFormulaCopy, SharedResearchFixture.LegibleFormula), "InventoryNotAuthorized");
            });
            cases.Add("formula_research_checks_credential_evidence_station_and_identity", () => {
                foreach (var row in new[] {
                    (new SharedResearchFixture(qualified:false), "ResearchCredentialMissing"), (new SharedResearchFixture(accessible:false), "ResearchEvidenceUnavailable"),
                    (new SharedResearchFixture(sufficient:false), "ResearchEvidenceUnavailable"), (new SharedResearchFixture(stationSuitable:false), "ResearchStationUnavailable") }) {
                    var s = World(ResearchPolicy(facts:row.Item1)); RejectUnchanged(s, host, ResearchCommand(s), row.Item2);
                }
                var valid = World(ResearchPolicy()); RejectUnchanged(valid, host, ResearchCommand(valid, target:"my-new-evidence"), "UnknownResearchEvidence");
                RejectUnchanged(valid, host, ResearchCommand(valid, method:2), "UnknownResearchMethod");
            });
            cases.Add("formula_research_full_work_checks_once_grants_only_knowledge", () => {
                var s = World(ResearchPolicy(SeedForDeath(6))); var before = s.Capture(); ResearchStart(s); WorldAdvance(s, 28799);
                Require(ResearchJob(s).Status == FormulaWorkStatus.Working && s.Capture().RandomState == before.RandomState, "Research rolled before full labor.");
                WorldAdvance(s, 1); var job = ResearchJob(s);
                Require(job.Status == FormulaWorkStatus.Success && job.Natural == 6 && job.Work.Labor == T(28800)
                    && FormulaResearchRules.Knows(s.Capture(), TestOnlyPolicy.CompanionId, SharedResearchFixture.Recipe)
                    && s.Capture().Work.Lots.Count == before.Work.Lots.Count && WritingStock(s) == new RuleQuantity(3), "Knowledge research created output or charged writing/manufacturing inputs.");
                RejectUnchanged(s, host, ResearchCommand(s), "FormulaAlreadyKnown");
                RejectUnchanged(s, host, ResearchCommand(s, CommandKind.ResumeFormulaWork, job.Id), "FormulaWorkClosed");
            });
            cases.Add("formula_research_failed_evidence_cannot_reroll_but_new_method_earns_full_hours", () => {
                var s = World(ResearchPolicy(SeedForDeath(5))); ResearchStart(s); WorldAdvance(s, 28800); var failed = ResearchJob(s);
                Require(failed.Status == FormulaWorkStatus.Failure && failed.Natural == 5 && !FormulaResearchRules.Knows(s.Capture(), failed.WorkerId, failed.RecipeId), "Failure lost notes or granted knowledge.");
                RejectUnchanged(s, host, ResearchCommand(s), "UnchangedResearchEvidence");
                ResearchStart(s, method:1); Require(ResearchJob(s).PreviousAttemptId == failed.Id && ResearchJob(s).Work.Retained == default, "Retry inherited spent labor or lost failure identity.");
                WorldAdvance(s, 28799); Require(ResearchJob(s).Natural == 0, "Alternative-method retry skipped full duration.");
                WorldAdvance(s, 1); Require(ResearchJob(s).Work.Labor == T(28800) && ResearchJob(s).Natural != 0, "Retry did not resolve at full second Watch.");
            });
            cases.Add("formula_research_new_qualifying_evidence_permits_fresh_attempt", () => {
                var s = World(ResearchPolicy(SeedForDeath(5))); ResearchStart(s); WorldAdvance(s, 28800); ResearchStart(s, SharedResearchFixture.FreshEvidence);
                Require(ResearchJob(s).Work.Retained == default && ResearchJob(s).PreviousAttemptId != "", "Fresh source reset history or borrowed work.");
            });
            cases.Add("formula_research_pause_resume_is_exact_and_does_not_auto_resume", () => {
                var p = ResearchPolicy(); var s = World(p); ResearchStart(s); WorldAdvance(s, 1, 3); ResearchControl(s, CommandKind.PauseFormulaWork); WorldAdvance(s, 100);
                Require(ResearchJob(s).Work.Retained == T(1, 3), "Paused researcher earned elapsed time.");
                s = new Simulation(p, new SnapshotCodec().Decode(Bytes(s)), ExecutionProfile.Laboratory); ResearchControl(s, CommandKind.ResumeFormulaWork); WorldAdvance(s, 2, 3);
                Require(ResearchJob(s).Work.Retained == T(1), "Resume lost exact fractional work.");
            });
            cases.Add("formula_research_exclusive_worker_and_watch_boundary_are_enforced", () => {
                var s = World(ResearchPolicy()); FarmWork(s, CommandKind.PlantCrop); RejectUnchanged(s, host, ResearchCommand(s), "WorkerBusy");
                WorldAdvance(s, 3600); ResearchStart(s); WorldAdvance(s, 25200);
                Require(ResearchJob(s).Status == FormulaWorkStatus.Paused && ResearchJob(s).Work.Retained == T(25200), "Research crossed authored Watch without rescheduling.");
                ResearchControl(s, CommandKind.ResumeFormulaWork); WorldAdvance(s, 3600); Require(ResearchJob(s).Work.Complete, "Second legal Watch could not finish remaining work.");
                var closed = World(ResearchPolicy()); WorldAdvance(closed, 57600); RejectUnchanged(closed, host, ResearchCommand(closed), "ResearchWorkWindowClosed");
            });
            cases.Add("formula_research_cancel_retains_notes_but_fresh_attempt_gets_no_credit", () => {
                var s = World(ResearchPolicy()); ResearchStart(s); WorldAdvance(s, 100); ResearchControl(s, CommandKind.CancelFormulaWork); ResearchStart(s);
                Require(s.Capture().FormulaWork[0].Work.Labor == T(100) && s.Capture().FormulaWork[0].Status == FormulaWorkStatus.Cancelled && ResearchJob(s).Work.Retained == default, "Cancellation refunded or transferred labor.");
            });
            cases.Add("formula_copy_reserves_then_debits_first_positive_labor_once", () => {
                var s = World(ResearchPolicy()); ResearchStart(s, copy:true); var initialRandom = s.Capture().RandomState;
                Require(WritingStock(s) == new RuleQuantity(3) && s.Capture().Work.AvailableAmount(SharedResearchFixture.Supplies) == new RuleQuantity(2), "Scheduling consumed copy supplies.");
                ResearchControl(s, CommandKind.PauseFormulaWork); ResearchControl(s, CommandKind.ResumeFormulaWork); WorldAdvance(s, 1, 2);
                Require(WritingStock(s) == new RuleQuantity(2), "First positive work did not debit whole allotment.");
                ResearchControl(s, CommandKind.PauseFormulaWork); ResearchControl(s, CommandKind.ResumeFormulaWork); WorldAdvance(s, 7199, 2);
                Require(ResearchJob(s).Status == FormulaWorkStatus.Success && WritingStock(s) == new RuleQuantity(2) && s.Capture().RandomState == initialRandom, "Copy rolled, charged twice or failed once-only completion.");
            });
            cases.Add("formula_copy_cancel_before_work_releases_after_work_does_not_refund", () => {
                var s = World(ResearchPolicy()); ResearchStart(s, copy:true); ResearchControl(s, CommandKind.CancelFormulaWork);
                Require(s.Capture().Work.AvailableAmount(SharedResearchFixture.Supplies) == new RuleQuantity(3), "Unstarted copy lost supplies.");
                ResearchStart(s, copy:true); WorldAdvance(s, 1); ResearchControl(s, CommandKind.CancelFormulaWork);
                Require(WritingStock(s) == new RuleQuantity(2) && !FormulaResearchRules.Knows(s.Capture(), TestOnlyPolicy.CompanionId, SharedResearchFixture.Recipe), "Started cancellation refunded ink or completed formula.");
            });
            cases.Add("formula_copy_repeated_cancel_spends_finite_supplies_without_free_formula", () => {
                var p=ResearchPolicy();var s=World(p);
                for(int i=0;i<3;i++){ResearchStart(s,copy:true);WorldAdvance(s,1);ResearchControl(s,CommandKind.CancelFormulaWork);}
                s=new Simulation(p,new SnapshotCodec().Decode(Bytes(s)),ExecutionProfile.Laboratory);
                Require(WritingStock(s)==default&&!FormulaResearchRules.Knows(s.Capture(),TestOnlyPolicy.CompanionId,SharedResearchFixture.Recipe),"Cancellation manufactured supplies or knowledge.");
                RejectUnchanged(s,host,ResearchCommand(s,CommandKind.StartFormulaCopy,SharedResearchFixture.LegibleFormula),"WritingSuppliesUnavailable");
            });
            cases.Add("formula_research_condition_interrupt_preserves_work_until_explicit_resume", () => {
                var worker = TestOnlyPolicy.CompanionId;
                var p = ResearchPolicy(conditions:new ConditionCombatFixture(CCApply("stun", "Stunned", worker, new ConditionStamp(T(20)), new ConditionStamp(T(10)))));
                var s = World(p); ResearchStart(s); WorldAdvance(s, 10); CCDispatch(s, "stun", worker); WorldAdvance(s, 10);
                Require(ResearchJob(s).Status == FormulaWorkStatus.Paused && ResearchJob(s).Work.Retained == T(10), "Condition erased work or auto-resumed it.");
                ResearchControl(s, CommandKind.ResumeFormulaWork); WorldAdvance(s, 10); Require(ResearchJob(s).Work.Retained == T(20), "Lawful explicit resume did not continue work.");
            });
            cases.Add("formula_research_poisoned_check_uses_actual_completion_state", () => {
                var worker = TestOnlyPolicy.CompanionId; var p = ResearchPolicy(TacticalSeed(18, 3), conditions:new ConditionCombatFixture(CCApply("poison", "Poisoned", worker)));
                var s = World(p); CCDispatch(s, "poison", worker); ResearchStart(s); WorldAdvance(s, 28800);
                Require(ResearchJob(s).First == 18 && ResearchJob(s).Second == 3 && ResearchJob(s).Natural == 3 && ResearchJob(s).Status == FormulaWorkStatus.Failure, "Poisoned research ignored actual disadvantage.");
            });
            cases.Add("formula_research_remote_work_survives_tactical_decisions_and_slot_advance", () => {
                var s = World(ResearchPolicy()); ResearchStart(s); BeginEncounter(s); ConnectedEnd(s);
                Require(ResearchJob(s).Work.Retained == T(3), "Remote research did not use elapsed slot time.");
                RejectUnchanged(s, host, IC(s, CommandKind.AdvanceClock, x:100, y:1), "TacticalDecisionClockPaused");
            });
            cases.Add("formula_research_synchronous_handling_credits_remote_work_and_gates_finish_boundary", () => {
                var s = World(ResearchPolicy()); ResearchStart(s); var before = s.Capture().RuleClock;
                HandleI(s, TestOnlyInventoryPolicy.FoodId, new RuleQuantity(1, 10), HandlingKind.Stow);
                Require(ResearchJob(s).Work.Retained == T(1) && s.Capture().RuleClock == before.AddSeconds(1), "Synchronous handling skipped remote research work.");
                WorldAdvance(s,28798);
                RejectUnchanged(s,host,IC(s,CommandKind.HandleInventory,TestOnlyInventoryPolicy.FoodId,new InventoryRequest(new RuleQuantity(1,10),handling:HandlingKind.Stow)),"TimedHandlingBoundaryUnsupported");
            });
            cases.Add("formula_research_final_labor_incapacity_waits_for_one_explicit_check_after_restore", () => {
                string worker=TestOnlyPolicy.CompanionId;
                var cure=new ConditionFixtureEvent(worker,ConditionOperation.Cure("event.cure",new ConditionStamp(T(28800)),"Stunned"));
                var p=ResearchPolicy(SeedForDeath(6),conditions:new ConditionCombatFixture(CCApply("stun","Stunned",worker),CCGrant("ward",worker,new ConditionStamp(T(28800)),"Stunned"),cure));
                var s=World(p);CCDispatch(s,"stun",worker);CCDispatch(s,"ward",worker);ResearchStart(s);uint rng=s.Capture().RandomState;WorldAdvance(s,28800);
                Require(ResearchJob(s).Status==FormulaWorkStatus.AwaitingCheck&&ResearchJob(s).Work.Complete&&s.Capture().RandomState==rng,"Final labor rolled through incapacity or was discarded.");
                string path=Path.Combine(directory,"formula-awaiting-check.bin");new FileSaveStore().Save(path,s.Capture());s=new Simulation(p,new FileSaveStore().Load(path),ExecutionProfile.Laboratory);
                RejectUnchanged(s,host,ResearchCommand(s,CommandKind.ResumeFormulaWork,ResearchJob(s).Id),"ResearchWorkerIncapable");
                CCDispatch(s,"cure",worker);Require(ResearchJob(s).Status==FormulaWorkStatus.AwaitingCheck&&s.Capture().RandomState==rng,"Cure automatically rerolled pending research.");
                var command=ResearchCommand(s,CommandKind.ResumeFormulaWork,ResearchJob(s).Id);WorldCommit(s,command);var bytes=Bytes(s);
                Require(ResearchJob(s).Status==FormulaWorkStatus.Success&&ResearchJob(s).Work.Labor==T(28800)&&s.Capture().RuleClock==T(28800),"Explicit completion repeated work or failed its one roll.");
                Require(s.Execute(host,command).Outcome==Outcome.Duplicate&&Bytes(s).SequenceEqual(bytes),"Duplicate completion rerolled.");
            });
            cases.Add("formula_copy_final_labor_completes_despite_boundary_incapacity", () => {
                string worker=TestOnlyPolicy.CompanionId;
                var s=World(ResearchPolicy(conditions:new ConditionCombatFixture(CCApply("stun","Stunned",worker),CCGrant("ward",worker,new ConditionStamp(T(3600)),"Stunned"))));
                CCDispatch(s,"stun",worker);CCDispatch(s,"ward",worker);ResearchStart(s,copy:true);uint rng=s.Capture().RandomState;WorldAdvance(s,3600);
                Require(ResearchJob(s).Status==FormulaWorkStatus.Success&&ResearchJob(s).Work.Complete&&s.Capture().RandomState==rng&&WritingStock(s)==new RuleQuantity(2),"Completed transcription was erased by endpoint incapacity.");
            });
            cases.Add("formula_research_fully_worked_check_after_final_labor_window_needs_no_new_hours", () => {
                string worker=TestOnlyPolicy.CompanionId;
                var cure=new ConditionFixtureEvent(worker,ConditionOperation.Cure("event.cure",new ConditionStamp(T(57601)),"Stunned"));
                var p=ResearchPolicy(SeedForDeath(6),conditions:new ConditionCombatFixture(CCApply("stun","Stunned",worker),CCGrant("ward",worker,new ConditionStamp(T(57600)),"Stunned"),cure));
                var s=World(p);CCDispatch(s,"stun",worker);CCDispatch(s,"ward",worker);WorldAdvance(s,28800);ResearchStart(s);WorldAdvance(s,28800);
                Require(ResearchJob(s).Status==FormulaWorkStatus.AwaitingCheck,"Expected a fully worked check at final labor window.");
                WorldAdvance(s,1);CCDispatch(s,"cure",worker);ResearchControl(s,CommandKind.ResumeFormulaWork);
                Require(ResearchJob(s).Status==FormulaWorkStatus.Success&&ResearchJob(s).Work.Labor==T(28800)&&s.Capture().RuleClock==T(57601),"Deferred check incorrectly required another work window.");
            });
            cases.Add("formula_research_simultaneous_parent_and_immunity_expiry_does_not_pause_completion", () => {
                string worker=TestOnlyPolicy.CompanionId;
                var s=World(ResearchPolicy(SeedForDeath(6),conditions:new ConditionCombatFixture(CCApply("stun","Stunned",worker,new ConditionStamp(T(28800))),CCGrant("ward",worker,new ConditionStamp(T(28800)),"Stunned"))));
                CCDispatch(s,"stun",worker);CCDispatch(s,"ward",worker);ResearchStart(s);WorldAdvance(s,28800);
                Require(ResearchJob(s).Status==FormulaWorkStatus.Success&&ResearchJob(s).Natural==6,"Transient expiry ordering manufactured an interruption.");
            });
            cases.Add("formula_research_participant_entry_pauses_actual_labor", () => {
                var s=World(ResearchPolicy(facts:new SharedResearchFixture(TestOnlyPolicy.ActorId)));
                foreach(var step in new[]{new[]{0,1},new[]{0,1},new[]{1,0},new[]{1,0},new[]{1,0}}){WorldStep(s,step[0],step[1]);WorldAdvance(s,1);}
                ResearchStart(s,worker:TestOnlyPolicy.ActorId);WorldAdvance(s,10);BeginEncounter(s);
                Require(ResearchJob(s).Status==FormulaWorkStatus.Paused&&ResearchJob(s).Work.Retained==T(10),"Tactical participant kept researching or lost labor.");
                RejectUnchanged(s,host,ResearchCommand(s,CommandKind.ResumeFormulaWork,ResearchJob(s).Id,worker:TestOnlyPolicy.ActorId),"ResearchParticipantInCombat");
            });
            cases.Add("formula_copy_current_inventory_grant_applies_to_resume_and_duplicate", () => {
                var s=World(ResearchPolicy());var c=ResearchCommand(s,CommandKind.StartFormulaCopy,SharedResearchFixture.LegibleFormula);WorldCommit(s,c);
                var revoked=new Authority(host.Principal,new[]{TestOnlyPolicy.CompanionId});RejectUnchanged(s,revoked,c,"InventoryNotAuthorized");
                ResearchControl(s,CommandKind.PauseFormulaWork);
                RejectUnchanged(s,revoked,ResearchCommand(s,CommandKind.ResumeFormulaWork,ResearchJob(s).Id),"InventoryNotAuthorized");
            });
            cases.Add("formula_research_pending_knockout_blocks_rng_interleaving_and_completes_normally", () => {
                string worker=TestOnlyPolicy.CompanionId;
                var cure=new ConditionFixtureEvent(worker,ConditionOperation.Cure("event.cure",new ConditionStamp(T(28802)),"Stunned"));
                var p=new TestOnlySharedWorldPolicy(new SharedCombatFixture(1,SeedForDeath(16)),new SharedResearchFixture(),conditions:new ConditionCombatFixture(CCApply("stun","Stunned",worker),CCGrant("ward",worker,new ConditionStamp(T(28800)),"Stunned"),cure));
                var s=World(p);CCDispatch(s,"stun",worker);CCDispatch(s,"ward",worker);ResearchStart(s);WorldAdvance(s,28800);
                WorldStep(s,1,0);WorldAdvance(s,1);WorldStep(s,1,0);WorldAdvance(s,1);CCDispatch(s,"cure",worker);WorldStep(s,1,0);
                WorldCommit(s,Tac(s,CommandKind.SelectCombatStance,stance:(int)CombatStance.Aggressive));TacStep(s,3,0);
                WorldCommit(s,Tac(s,CommandKind.AttackUnarmed,AdditionalTacticalActor.Id,knockout:AttackKnockoutMode.AskIfEligible));
                Require(s.Capture().MeleeAttacks.Single().Pending&&ResearchJob(s).Status==FormulaWorkStatus.AwaitingCheck,"Expected two distinct pending decisions.");
                RejectUnchanged(s,host,ResearchCommand(s,CommandKind.ResumeFormulaWork,ResearchJob(s).Id),"TacticalChoicePending");
                RejectUnchanged(s,host,ResearchCommand(s,CommandKind.CancelFormulaWork,ResearchJob(s).Id),"TacticalChoicePending");
                WorldCommit(s,Tac(s,CommandKind.ResolveKnockout,s.Capture().MeleeAttacks.Single().Id,choice:true));
                Require(s.Capture().Lives.Single(x=>x.ActorId==AdditionalTacticalActor.Id).Stable,"Blocked research stranded the paid attack continuation.");
                ResearchControl(s,CommandKind.ResumeFormulaWork);Require(ResearchJob(s).Natural!=0,"Research could not finish after tactical choice resolved.");
            });
            cases.Add("formula_research_partial_disk_restore_and_forged_result_rejection", () => {
                var p = ResearchPolicy(SeedForDeath(6)); var s = World(p); ResearchStart(s); WorldAdvance(s, 123);
                string path = Path.Combine(directory, "formula-research-partial.bin"); new FileSaveStore().Save(path, s.Capture());
                var restored = new Simulation(p, new FileSaveStore().Load(path), ExecutionProfile.Laboratory); WorldAdvance(s, 28677); WorldAdvance(restored, 28677);
                Require(Bytes(s).SequenceEqual(Bytes(restored)), "Research disk continuation diverged.");
                var forged = s.Capture(); var job = forged.FormulaWork[0]; forged.FormulaWork[0] = new FormulaWorkRecord(job.Id, job.WorkerId, job.RecipeId, job.EvidenceId, job.MethodId,
                    job.Kind, FormulaWorkStatus.Failure, job.StartedAt, job.UpdatedAt, job.Work, 5, 0, 5);
                Throws<ArgumentException>(() => new Simulation(p, forged, ExecutionProfile.Laboratory));
            });
        }
    }
}
#endif
