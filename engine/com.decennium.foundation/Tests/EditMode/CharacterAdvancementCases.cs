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
        private static TestOnlySharedWorldPolicy AdvancementPolicy(ActorLifeRecord life=null)
            =>new TestOnlySharedWorldPolicy(new CharacterAdvancementFixture(life),new SharedCombatFixture());
        private static TestOnlySharedWorldPolicy CommandStepPolicy(params TacticalTerrainCell[] terrain)
            =>new TestOnlySharedWorldPolicy(SoldierCharacterBuildFixture.ForTacticalTechniques(),new OverwatchFoundationFixture(),
                new CharacterAdvancementFixture(null,false,false,true,true),new SharedCombatFixture(),terrain:terrain);
        private static Command AwardMilestone(Simulation s,string milestone="opening.milestone.soldier-2",string actor=null,string id="milestone.award")
            =>new Command(id,actor??TestOnlyPolicy.ActorId,s.Capture().Revision,CommandKind.AwardCharacterMilestone,milestone);
        private static Command AdvanceLevel(Simulation s,string milestone="opening.milestone.soldier-2",string one=CharacterAdvancementFixture.DefensivePositioning,
            string two=CharacterAdvancementFixture.TacticalReposition,string id="character.advance")
            =>new Command(id,TestOnlyPolicy.ActorId,s.Capture().Revision,CommandKind.AdvanceCharacterLevel,milestone,
                advancement:new CharacterAdvancementRequest(one,two));
        private static void AddCharacterAdvancementCases(Dictionary<string,Action> cases,string directory)
        {
            var host=TestOnlySharedWorldPolicy.Host();
            cases.Add("character_advancement_catalog_covers_all_pinned_classes_and_level_rows",()=>{
                var rows=ClassAdvancementScheduleCatalog.Rows;var sources=ClassAdvancementScheduleCatalog.Sources;
                Require(ClassAdvancementScheduleCatalog.SourceRevision=="46a4d52728ee6956f0bebcb5d2103ffd5bc67ba4"
                    &&sources.Count==17&&rows.Count==340
                    &&rows.Select(x=>x.ClassName+"|"+x.ClassLevel).Distinct(StringComparer.Ordinal).Count()==340
                    &&rows.Count(x=>x.Kind==ClassAdvancementScheduleKind.Structured)==280
                    &&rows.Count(x=>x.Kind==ClassAdvancementScheduleKind.NarrativeException)==60
                    &&sources.All(x=>x.Sha256.Length==64&&x.GitBlobId.Length==40&&x.DesignStatus.Contains("draft",StringComparison.OrdinalIgnoreCase)
                        &&!x.DesignStatus.Contains("release-approved",StringComparison.OrdinalIgnoreCase)),
                    "The class schedule catalog lost a pinned source, class-level row, or the authored draft/release distinction.");
                Require(rows.All(x=>x.ClassLevel>=1&&x.ClassLevel<=20&&x.SourcePath!=""&&x.SourceLocator.StartsWith("/",StringComparison.Ordinal))
                    &&rows.All(x=>rows.Count(r=>r.ClassName==x.ClassName&&r.ClassLevel==x.ClassLevel)==1),
                    "A schedule row lacks exact source addressing or is duplicated.");
                Throws<NotSupportedException>(()=>((IList<ClassAdvancementScheduleRow>)rows).Add(rows[0]));
            });
            cases.Add("character_advancement_catalog_preserves_structured_choices_and_unresolved_exceptions",()=>{
                var soldier2=ClassAdvancementScheduleCatalog.Get("Soldier",2);
                var soldier3=ClassAdvancementScheduleCatalog.Get("Soldier",3);
                var soldier3Candidates=ClassAdvancementOptionCatalog.Candidates(soldier3);
                var assessment=ClassAdvancementOptionCatalog.Get("Soldier",CharacterFeatureIds.TacticalAssessment);
                var commandStep=ClassAdvancementOptionCatalog.Get("Soldier",CharacterFeatureIds.CommandStep);
                var suppression=ClassAdvancementOptionCatalog.Get("Soldier",CharacterFeatureIds.SuppressionFire);
                var wizard10=ClassAdvancementScheduleCatalog.Get("Wizard",10);
                var druid1=ClassAdvancementScheduleCatalog.Get("Druid",1);
                Require(soldier2.Kind==ClassAdvancementScheduleKind.Structured&&soldier2.RequiredSelections==2
                    &&soldier2.Bands.SequenceEqual(new[]{"Base"})&&soldier2.MinimumActiveSelections==0
                    &&soldier2.HasAsiOrFeatOpportunity==false&&soldier2.SourceLocator=="/schedule/1"
                    &&soldier3.RequiredSelections==2&&soldier3.Bands.SequenceEqual(new[]{"Arch"})&&soldier3.MinimumActiveSelections==1
                    &&new[]{assessment,commandStep,suppression}.All(x=>x!=null&&soldier3Candidates.Contains(x))
                    &&assessment.Activation=="Bonus Action"&&commandStep.Kind=="passive"&&suppression.Activation=="Action"
                    &&wizard10.RequiredSelections==2&&wizard10.Bands.SequenceEqual(new[]{"Hero"})&&wizard10.MinimumActiveSelections==1,
                    "Structured schedule rows do not preserve their selection bands, active minimums, ASI flags, and locators.");
                Require(druid1.Kind==ClassAdvancementScheduleKind.NarrativeException&&!druid1.RequiredSelections.HasValue
                    &&druid1.Bands.Count==0&&!druid1.MinimumActiveSelections.HasValue&&!druid1.HasAsiOrFeatOpportunity.HasValue
                    &&druid1.SourceLocator=="/exceptionSchedule/1"
                    &&ClassAdvancementScheduleCatalog.Get("Oracle",20).Kind==ClassAdvancementScheduleKind.NarrativeException
                    &&ClassAdvancementScheduleCatalog.Get("Paladin",20).Kind==ClassAdvancementScheduleKind.NarrativeException
                    &&ClassAdvancementScheduleCatalog.Get("missing",1)==null,
                    "Narrative class exceptions were inferred as empty schedules or mapped to the wrong source rows.");
                Throws<NotSupportedException>(()=>((IList<string>)soldier2.Bands).Add("Hero"));
            });
            cases.Add("character_advancement_option_catalog_projects_pinned_cards_and_row_candidates",()=>{
                var all=ClassAdvancementOptionCatalog.Options;
                var soldier2=ClassAdvancementScheduleCatalog.Get("Soldier",2);
                var candidates=ClassAdvancementOptionCatalog.Candidates(soldier2);
                var steadyAim=ClassAdvancementOptionCatalog.Get("Soldier","soldier.base.steady-aim");
                Require(ClassAdvancementOptionCatalog.SourceRevision==ClassAdvancementScheduleCatalog.SourceRevision
                    &&all.Count==1223&&all.Select(x=>x.ClassName+"|"+x.Id).Distinct(StringComparer.Ordinal).Count()==1223
                    &&all.All(x=>x.SourceLocator.StartsWith("/cards/",StringComparison.Ordinal)&&x.SourcePath!=""&&x.DesignStatus!="")
                    &&candidates.Count==10&&candidates.All(x=>x.ClassName=="Soldier"&&x.Band=="Base"&&x.Acquisition=="selection"
                        &&x.MinimumClassLevel<=2)
                    &&new[]{CharacterAdvancementFixture.DefensivePositioning,CharacterAdvancementFixture.TacticalReposition,
                        CharacterFeatureIds.WarningShot,CharacterFeatureIds.CoveringFire}.All(id=>candidates.Any(x=>x.Id==id))
                    &&steadyAim!=null&&steadyAim.Activation=="Passive"&&!steadyAim.HasPathConstraint&&!steadyAim.HasDeclaredPrerequisite,
                    "Pinned class-card options or level-row band/level candidates were lost or widened.");
                Throws<NotSupportedException>(()=>((IList<ClassAdvancementOption>)all).Add(all[0]));
                Throws<NotSupportedException>(()=>((IList<ClassAdvancementOption>)candidates).Add(candidates[0]));
            });
            cases.Add("character_advancement_choice_list_receipts_roundtrip_and_preserve_legacy_pairs",()=>{
                string Fingerprint(Command command)
                {
                    var advancement=command.Advancement;
                    string selection=advancement.UsesLegacyPairReceipt
                        ?"|character-level-v1|"+advancement.FeatureOne+"|"+advancement.FeatureTwo
                        :"|character-level-v2|"+string.Join(",",advancement.FeatureIds);
                    return ((int)command.Kind).ToString(System.Globalization.CultureInfo.InvariantCulture)+"|"+command.Actor+"|"+command.Target+"|"
                        +command.ExpectedRevision.ToString(System.Globalization.CultureInfo.InvariantCulture)+"|"+command.X.ToString(System.Globalization.CultureInfo.InvariantCulture)
                        +"|"+command.Y.ToString(System.Globalization.CultureInfo.InvariantCulture)+selection;
                }
                foreach(var choices in new[]{Array.Empty<string>(),new[]{"card.only"},new[]{"card.d","card.b","card.a","card.c"}}) {
                    var command=new Command("history.list."+choices.Length,TestOnlyPolicy.ActorId,0,CommandKind.AdvanceCharacterLevel,"milestone.list",
                        advancement:new CharacterAdvancementRequest(choices));
                    var receipt=new CommandReceipt{Principal="TEST_ONLY.host",Id=command.Id,Fingerprint=Fingerprint(command),Revision=1};
                    var decoded=CommandHistory.Read(receipt);
                    Require(Fingerprint(decoded)==Fingerprint(command)&&decoded.Advancement.FeatureIds.SequenceEqual(command.Advancement.FeatureIds),
                        "Versioned advancement choice lists did not roundtrip canonically.");
                }
                var legacy=new Command("history.legacy",TestOnlyPolicy.ActorId,0,CommandKind.AdvanceCharacterLevel,"milestone.legacy",
                    advancement:new CharacterAdvancementRequest(CharacterAdvancementFixture.TacticalReposition,CharacterAdvancementFixture.DefensivePositioning));
                var legacyReceipt=new CommandReceipt{Principal="TEST_ONLY.host",Id=legacy.Id,Fingerprint=Fingerprint(legacy),Revision=1};
                var legacyDecoded=CommandHistory.Read(legacyReceipt);
                Require(legacyDecoded.Advancement.UsesLegacyPairReceipt
                    &&legacyDecoded.Advancement.FeatureOne==CharacterAdvancementFixture.TacticalReposition
                    &&legacyDecoded.Advancement.FeatureTwo==CharacterAdvancementFixture.DefensivePositioning,
                    "A historical pair receipt changed order or version during decoding.");

                var policy=AdvancementPolicy();var s=World(policy);WorldCommit(s,AwardMilestone(s));
                var selected=new Command("character.advance.v2",TestOnlyPolicy.ActorId,s.Capture().Revision,CommandKind.AdvanceCharacterLevel,
                    "opening.milestone.soldier-2",advancement:new CharacterAdvancementRequest(new[]{CharacterAdvancementFixture.TacticalReposition,
                        CharacterAdvancementFixture.DefensivePositioning}));
                WorldCommit(s,selected);
                var saved=s.Capture();var committed=CommandHistory.Read(saved.Receipts.Single(x=>x.Id==selected.Id));
                var bytes=Bytes(s);var replay=new Simulation(policy,new SnapshotCodec().Decode(bytes),ExecutionProfile.Laboratory);
                Require(committed.Advancement.FeatureIds.SequenceEqual(new[]{CharacterAdvancementFixture.DefensivePositioning,
                        CharacterAdvancementFixture.TacticalReposition})&&bytes.SequenceEqual(Bytes(replay)),
                    "A v2 advancement command did not commit, canonicalize, and survive snapshot replay.");

                var longChoices=new[]{new string('a',96),new string('b',96),new string('c',96),new string('d',96)};
                var oversized=new Command("history.oversized",TestOnlyPolicy.ActorId,s.Capture().Revision,CommandKind.AdvanceCharacterLevel,new string('m',96),
                    advancement:new CharacterAdvancementRequest(longChoices));
                Require(Fingerprint(oversized).Length>512,"The boundary fixture did not exceed the persisted receipt limit.");
                RejectUnchanged(s,host,oversized,"CommandFingerprintTooLong");
            });
            cases.Add("character_advancement_schema30_roundtrips_canonical_event_choice_lists",()=>{
                var samples=new[]{Array.Empty<string>(),new[]{"choice.one"},new[]{"choice.d","choice.b","choice.a","choice.c"}};
                for(int i=0;i<samples.Length;i++) {
                    var record=new CharacterAdvancementRecord("actor.history."+i,"milestone.history."+i,1,1,2,"Soldier",2,6,
                        HitPointGainMethod.FixedAverage,10,16,4,4,samples[i]);
                    var canonical=samples[i].OrderBy(x=>x,StringComparer.Ordinal).ToArray();
                    Require(record.SelectedFeatureIds.SequenceEqual(canonical)
                        &&record.FeatureOne==(canonical.Length>0?canonical[0]:"")
                        &&record.FeatureTwo==(canonical.Length>1?canonical[1]:""),
                        "A schema30 advancement record did not expose its canonical selected-card list.");
                }
                var policy=new TestOnlySharedWorldPolicy(new OverwatchFoundationFixture(),
                    new CharacterAdvancementFixture(null,false,true),new SharedCombatFixture());
                var s=World(policy);Require(s.Capture().SchemaVersion==Snapshot.CharacterAdvancementHistorySchema,
                    "The explicit advancement-history fixture did not select schema30.");
                WorldCommit(s,AwardMilestone(s));WorldCommit(s,AdvanceLevel(s));
                var snapshot=s.Capture();var before=Bytes(s);var restored=new Simulation(policy,new SnapshotCodec().Decode(before),ExecutionProfile.Laboratory);
                Require(snapshot.CharacterAdvancements.Single().SelectedFeatureIds.SequenceEqual(new[]{CharacterAdvancementFixture.DefensivePositioning,
                        CharacterAdvancementFixture.TacticalReposition}.OrderBy(x=>x,StringComparer.Ordinal))
                    &&before.SequenceEqual(Bytes(restored)),
                    "Schema30 did not persist the selected-feature list through a committed level-up and replay.");
            });
            cases.Add("character_advancement_schema30_validates_two_successive_soldier_level_events",()=>{
                var policy=new TestOnlySharedWorldPolicy(new OverwatchFoundationFixture(),
                    new CharacterAdvancementFixture(null,false,true),new SharedCombatFixture());
                var s=World(policy);WorldCommit(s,AwardMilestone(s));WorldCommit(s,AdvanceLevel(s));
                var state=s.Capture();var levelThree=state.Copy();levelThree.SchemaVersion=Snapshot.CommandStepSchema;
                const string milestone="opening.milestone.soldier-3";
                long awardRevision=checked(state.Revision+1),advanceRevision=checked(state.Revision+2);
                levelThree.Revision=advanceRevision;
                levelThree.CharacterMilestones=levelThree.CharacterMilestones.Concat(new[]{
                    new CharacterMilestoneRecord(milestone,TestOnlyPolicy.ActorId,awardRevision,advanceRevision)}).ToArray();
                levelThree.Characters=levelThree.Characters.Select(x=>x.ActorId==TestOnlyPolicy.ActorId
                    ?new ActorCharacterRecord(x.ActorId,x.ProfileId,x.Abilities,x.Levels.Concat(new[]{new CharacterLevelFact("Soldier",6)})):x).ToArray();
                levelThree.Lives=levelThree.Lives.Select(x=>x.ActorId==TestOnlyPolicy.ActorId
                    ?new ActorLifeRecord(x.ActorId,22,x.Hp,x.TemporaryHp,x.LinkedInjuries,x.Stable,x.Dead,x.UsesDeathSaves,x.DeathSuccesses,
                        x.DeathFailures,x.StableUntil,x.LastDeathTurn,x.Prone,x.HeldItems):x).ToArray();
                levelThree.CharacterHitDice=levelThree.CharacterHitDice.Concat(new[]{new CharacterHitDieRecord(TestOnlyPolicy.ActorId,3,"Soldier",10,false)}).ToArray();
                string[] selected={CharacterFeatureIds.CommandStep,CharacterFeatureIds.TacticalAssessment};
                levelThree.CharacterFeatureGrants=levelThree.CharacterFeatureGrants.Concat(selected.Select(feature=>
                    new CharacterFeatureGrantRecord(TestOnlyPolicy.ActorId,feature,"Soldier",3,milestone,advanceRevision))).ToArray();
                levelThree.CharacterAdvancements=levelThree.CharacterAdvancements.Concat(new[]{new CharacterAdvancementRecord(
                    TestOnlyPolicy.ActorId,milestone,advanceRevision,2,3,"Soldier",3,6,HitPointGainMethod.FixedAverage,16,22,
                    levelThree.Lives.Single(x=>x.ActorId==TestOnlyPolicy.ActorId).Hp,
                    levelThree.Lives.Single(x=>x.ActorId==TestOnlyPolicy.ActorId).Hp,selected)}).ToArray();
                CharacterAdvancementValidation.Validate(levelThree);

                var secondPair=levelThree.Copy();string[] alternate={CharacterFeatureIds.SuppressionFire,CharacterFeatureIds.TacticalAssessment};
                secondPair.CharacterFeatureGrants=secondPair.CharacterFeatureGrants.Where(x=>x.MilestoneId!=milestone)
                    .Concat(alternate.Select(feature=>new CharacterFeatureGrantRecord(TestOnlyPolicy.ActorId,feature,"Soldier",3,milestone,advanceRevision))).ToArray();
                secondPair.CharacterAdvancements=secondPair.CharacterAdvancements.Select(x=>x.MilestoneId==milestone
                    ?new CharacterAdvancementRecord(x.ActorId,x.MilestoneId,x.Revision,x.PreviousTotalLevel,x.NewTotalLevel,x.ClassName,
                        x.ClassLevel,x.BaseHpGain,x.HitPointMethod,x.MaximumHpBefore,x.MaximumHpAfter,x.CurrentHpBefore,x.CurrentHpAfter,alternate):x).ToArray();
                Throws<ArgumentException>(()=>CharacterAdvancementValidation.Validate(secondPair));

                var invalid=levelThree.Copy();
                invalid.CharacterAdvancements=invalid.CharacterAdvancements.Select(x=>x.MilestoneId==milestone
                    ?new CharacterAdvancementRecord(x.ActorId,x.MilestoneId,x.Revision,x.PreviousTotalLevel,x.NewTotalLevel,x.ClassName,
                        x.ClassLevel,x.BaseHpGain,x.HitPointMethod,x.MaximumHpBefore,x.MaximumHpAfter,x.CurrentHpBefore,x.CurrentHpAfter,
                        new[]{CharacterFeatureIds.CommandStep,CharacterFeatureIds.SuppressionFire}):x).ToArray();
                Throws<ArgumentException>(()=>CharacterAdvancementValidation.Validate(invalid));

                var extraGrant=levelThree.Copy();
                extraGrant.CharacterFeatureGrants=extraGrant.CharacterFeatureGrants.Concat(new[]{new CharacterFeatureGrantRecord(
                    TestOnlyPolicy.ActorId,CharacterFeatureIds.SuppressionFire,"Soldier",3,milestone,advanceRevision)}).ToArray();
                Throws<ArgumentException>(()=>CharacterAdvancementValidation.Validate(extraGrant));
            });
            cases.Add("character_advancement_schema32_commits_and_replays_the_first_arch_pair",()=>{
                var policy=CommandStepPolicy();var s=World(policy);
                Require(s.Capture().SchemaVersion==Snapshot.CommandStepSchema,"The explicit Command Step fixture did not select schema32.");
                WorldCommit(s,AwardMilestone(s,"opening.milestone.soldier-2",id:"milestone.soldier-2"));
                WorldCommit(s,AdvanceLevel(s,id:"advance.soldier-2"));
                var levelTwoBytes=Bytes(s);s=new Simulation(policy,new SnapshotCodec().Decode(levelTwoBytes),ExecutionProfile.Laboratory);
                Require(levelTwoBytes.SequenceEqual(Bytes(s))&&s.Capture().CharacterAdvancements.Single().NewTotalLevel==2,
                    "The committed Soldier 2 event did not validate at its own saved revision.");
                WorldCommit(s,AwardMilestone(s,"opening.milestone.soldier-3",id:"milestone.soldier-3"));
                var invalid=new Command("advance.soldier-3.invalid",TestOnlyPolicy.ActorId,s.Capture().Revision,CommandKind.AdvanceCharacterLevel,
                    "opening.milestone.soldier-3",advancement:new CharacterAdvancementRequest(new[]{CharacterFeatureIds.CommandStep,CharacterFeatureIds.SuppressionFire}));
                RejectUnchanged(s,TestOnlySharedWorldPolicy.Host(),invalid,"LegalFeatureChoiceNotImplemented");
                var valid=new Command("advance.soldier-3.valid",TestOnlyPolicy.ActorId,s.Capture().Revision,CommandKind.AdvanceCharacterLevel,
                    "opening.milestone.soldier-3",advancement:new CharacterAdvancementRequest(new[]{CharacterFeatureIds.TacticalAssessment,CharacterFeatureIds.CommandStep}));
                WorldCommit(s,valid);
                var state=s.Capture();var before=Bytes(s);var restored=new Simulation(policy,new SnapshotCodec().Decode(before),ExecutionProfile.Laboratory);
                Require(state.Characters.Single(x=>x.ActorId==TestOnlyPolicy.ActorId).Levels.Count==3
                    &&state.CharacterAdvancements.OrderBy(x=>x.ClassLevel).Select(x=>x.NewTotalLevel).SequenceEqual(new[]{2,3})
                    &&state.CharacterFeatureGrants.Where(x=>x.ClassLevel==3).Select(x=>x.FeatureId).OrderBy(x=>x,StringComparer.Ordinal)
                        .SequenceEqual(new[]{CharacterFeatureIds.CommandStep,CharacterFeatureIds.TacticalAssessment}.OrderBy(x=>x,StringComparer.Ordinal))
                    &&state.CharacterMilestones.Single(x=>x.MilestoneId=="opening.milestone.soldier-3").ConsumedRevision==valid.ExpectedRevision+1
                    &&state.Lives.Single(x=>x.ActorId==TestOnlyPolicy.ActorId).MaximumHp==22&&before.SequenceEqual(Bytes(restored)),
                    "Schema32 did not atomically commit both Arch cards, their hit die and HP capacity, or replay the second level event.");
            });
            cases.Add("soldier_command_step_is_action_linked_consentful_and_free_of_normal_movement_cost",()=>{
                var policy=CommandStepPolicy(new TacticalTerrainCell(0,1,TerrainCost.Difficult));var s=World(policy);
                WorldCommit(s,AwardMilestone(s,"opening.milestone.soldier-2",id:"cmdstep.milestone.2"));
                WorldCommit(s,AdvanceLevel(s,id:"cmdstep.advance.2"));
                WorldCommit(s,AwardMilestone(s,"opening.milestone.soldier-3",id:"cmdstep.milestone.3"));
                WorldCommit(s,new Command("cmdstep.advance.3",TestOnlyPolicy.ActorId,s.Capture().Revision,CommandKind.AdvanceCharacterLevel,
                    "opening.milestone.soldier-3",advancement:new CharacterAdvancementRequest(new[]{CharacterFeatureIds.CommandStep,CharacterFeatureIds.TacticalAssessment})));
                WorldStep(s,-1,0,actor:TestOnlyPolicy.CompanionId);WorldAdvance(s,1);
                WorldStep(s,0,-1,actor:TestOnlyPolicy.CompanionId);WorldAdvance(s,1);
                WorldStep(s,-1,0,actor:TestOnlyPolicy.CompanionId);WorldAdvance(s,1);
                WorldStep(s,0,-1,actor:TestOnlyPolicy.CompanionId);WorldAdvance(s,1);WorldAdvance(s,2);
                BeginEncounter(s);WorldCommit(s,Tac(s,CommandKind.SelectCombatStance,stance:(int)CombatStance.Aggressive));
                var host=TestOnlySharedWorldPolicy.Host();var assessmentOption=s.DiscoverCommands(host,TestOnlyPolicy.ActorId)
                    .Single(x=>x.Command.Kind==CommandKind.TacticalAssessment&&x.Command.Target==AdditionalTacticalActor.Id);
                WorldCommit(s,assessmentOption.Command);var assessment=s.Capture().TacticalAssessments.Single();
                Require(assessment.AllyActorId==TestOnlyPolicy.CompanionId&&assessment.EnemyActorId==AdditionalTacticalActor.Id
                    &&assessment.ArmorCategory=="unarmored"&&!assessment.HasCover,
                    "Tactical Assessment did not reveal its source-derived armor and cover facts on paid activation.");
                var loadout=s.Capture().InitialCharacterLoadouts.Single(x=>x.ActorId==TestOnlyPolicy.ActorId);
                var action=new Command("cmdstep.doff-shield",TestOnlyPolicy.ActorId,s.Capture().Revision,CommandKind.DoffPortableShield,loadout.ShieldId);
                WorldCommit(s,action);var turnId=s.Capture().Encounter.CurrentTurnId;
                var offerOptions=s.DiscoverCommands(host,TestOnlyPolicy.ActorId).Where(x=>x.Command.Kind==CommandKind.OfferCommandStep).ToArray();
                Require(offerOptions.Length>0,"Command Step offer was not discovered after the Soldier Action.");
                var firstOffer=offerOptions.Single();
                Require(firstOffer.Query.Admissible&&firstOffer.Command.Combat.WeaponId==action.Id,
                    "Command discovery did not bind its offer to the Soldier's completed Action receipt.");
                WorldCommit(s,firstOffer.Command);var declined=s.Capture().CommandStepOffers.Single(x=>x.Id==firstOffer.Command.Id);
                var decline=s.DiscoverCommands(host,TestOnlyPolicy.CompanionId).Single(x=>x.Command.Kind==CommandKind.RespondCommandStep&&!x.Command.Combat.Choice);
                WorldCommit(s,decline.Command);
                Require(declined.Status==CommandStepOfferStatus.Pending
                    &&s.Capture().CommandStepOffers.Single(x=>x.Id==declined.Id).Status==CommandStepOfferStatus.Declined
                    &&!s.Capture().CommandStepOffers.Any(x=>x.Status==CommandStepOfferStatus.Accepted),
                    "The willing ally's decline consumed Command Step or failed to resolve its offer.");
                var secondOffer=s.DiscoverCommands(host,TestOnlyPolicy.ActorId).Single(x=>x.Command.Kind==CommandKind.OfferCommandStep);
                WorldCommit(s,secondOffer.Command);var pendingBytes=Bytes(s);
                s=new Simulation(policy,new SnapshotCodec().Decode(pendingBytes),ExecutionProfile.Laboratory);
                Require(pendingBytes.SequenceEqual(Bytes(s)),"A pending action-linked Command Step offer did not survive save and restore.");
                var invalidStep=new Command("cmdstep.difficult",TestOnlyPolicy.CompanionId,s.Capture().Revision,CommandKind.RespondCommandStep,
                    secondOffer.Command.Id,0,1,combat:new CombatRequest(turnId,choice:true));
                RejectUnchanged(s,host,invalidStep,"InsufficientCommandStepMovement");
                var response=s.DiscoverCommands(host,TestOnlyPolicy.CompanionId).Single(x=>x.Command.Kind==CommandKind.RespondCommandStep
                    &&x.Command.Combat.Choice&&x.Command.X==1&&x.Command.Y==0);
                var allyIntervalBefore=s.Capture().WorldIntervals.Single(x=>x.ActorId==TestOnlyPolicy.CompanionId);
                int attacksBefore=s.Capture().MeleeAttacks.Length;
                WorldCommit(s,response.Command);
                var after=s.Capture();var accepted=after.CommandStepOffers.Single(x=>x.Id==secondOffer.Command.Id);
                var move=after.TacticalMoves.Single(x=>x.Id==accepted.MoveId);
                var allyIntervalAfter=after.WorldIntervals.Single(x=>x.ActorId==TestOnlyPolicy.CompanionId);
                var soldierInterval=after.WorldIntervals.Single(x=>x.ActorId==TestOnlyPolicy.ActorId);
                Require(accepted.Status==CommandStepOfferStatus.Accepted&&move.Kind==TacticalMoveKind.CommandStep&&move.Status==TacticalMoveStatus.Completed
                    &&move.ParentCommandStepOffer==accepted.Id&&move.Reactors.Count==0&&move.CostPaid==5
                    &&after.Actors.Single(x=>x.Id==TestOnlyPolicy.CompanionId).X==1&&after.Actors.Single(x=>x.Id==TestOnlyPolicy.CompanionId).Y==0
                    &&allyIntervalAfter.MovementSpent==allyIntervalBefore.MovementSpent&&soldierInterval.ActionSpent&&after.MeleeAttacks.Length==attacksBefore,
                    "Command Step failed to grant a separate five-foot move without an OA, normal movement debit, or a second Action spend.");
                var saved=Bytes(s);s=new Simulation(policy,new SnapshotCodec().Decode(saved),ExecutionProfile.Laboratory);
                Require(saved.SequenceEqual(Bytes(s)),"The accepted Command Step movement and action link did not survive save and restore.");
                var repeated=new Command("cmdstep.repeat",TestOnlyPolicy.ActorId,s.Capture().Revision,CommandKind.OfferCommandStep,TestOnlyPolicy.CompanionId,
                    combat:new CombatRequest(turnId,action.Id));
                RejectUnchanged(s,host,repeated,"CommandStepAlreadyUsedThisRound");
                TacEnd(s);TacStep(s,2,0);TacStep(s,3,0);
                WorldCommit(s,Tac(s,CommandKind.AttackUnarmed,AdditionalTacticalActor.Id,TestOnlyPolicy.CompanionId));
                var testedAttack=s.Capture().MeleeAttacks.Single(x=>x.AttackerId==TestOnlyPolicy.CompanionId&&x.TargetId==AdditionalTacticalActor.Id&&!x.Opportunity);
                var consumedAssessment=s.Capture().TacticalAssessments.Single(x=>x.Id==assessment.Id);
                Require(testedAttack.Attack.Modifier==1&&consumedAssessment.Status==TacticalAssessmentStatus.Consumed
                    &&consumedAssessment.ResolutionId==testedAttack.Id,
                    "Tactical Assessment did not add and consume +1 on the ally's first attempted attack against its assessed enemy.");
            });
            cases.Add("tactical_assessment_schema31_roundtrips_before_level3_is_granted",()=>{
                var policy=new TestOnlySharedWorldPolicy(SoldierCharacterBuildFixture.ForTacticalTechniques(),new OverwatchFoundationFixture(),
                    new CharacterAdvancementFixture(null,false,false,true),new SharedCombatFixture());
                var s=World(policy);var initial=s.Capture();var encoded=Bytes(s);
                var restored=new Simulation(policy,new SnapshotCodec().Decode(encoded),ExecutionProfile.Laboratory);
                Require(initial.SchemaVersion==Snapshot.TacticalAssessmentSchema&&initial.TacticalAssessments.Length==0
                    &&initial.CharacterFeatureGrants.All(x=>x.FeatureId!=CharacterFeatureIds.TacticalAssessment&&x.FeatureId!=CharacterFeatureIds.CommandStep)
                    &&encoded.SequenceEqual(Bytes(restored)),
                    "Schema31 did not preserve its opt-in base state or incorrectly granted level-3 cards before both handlers exist.");
                var host=TestOnlySharedWorldPolicy.Host();
                var request=new Command("assessment.before-encounter",TestOnlyPolicy.ActorId,initial.Revision,CommandKind.TacticalAssessment,
                    AdditionalTacticalActor.Id,combat:new CombatRequest("world.unstarted-turn",TestOnlyPolicy.CompanionId));
                RejectUnchanged(s,host,request,"TacticalAssessmentRequiresEncounter");
            });
            cases.Add("character_advancement_schema21_starts_as_source_scoped_soldier1",()=>{
                var p=AdvancementPolicy();var s=new Simulation(p,p.Initial(),ExecutionProfile.Laboratory);var v=s.Capture();
                Require(v.SchemaVersion==Snapshot.CharacterAdvancementSchema&&v.Characters.Single(x=>x.ActorId==TestOnlyPolicy.ActorId).Levels.Single().ClassName=="Soldier"
                    &&v.Characters.Single(x=>x.ActorId==TestOnlyPolicy.ActorId).Levels.Single().BaseHp==10
                    &&v.Lives.Single(x=>x.ActorId==TestOnlyPolicy.ActorId).MaximumHp==10&&v.Lives.Single(x=>x.ActorId==TestOnlyPolicy.ActorId).Hp==4
                    &&v.CharacterHitDice.Single().DieSize==10&&!v.CharacterHitDice.Single().Spent&&v.CharacterFeatureGrants.Length==0
                    &&v.Lives.Single(x=>x.ActorId==TestOnlyPolicy.ActorId).HeldItems.SequenceEqual(new[]{TestOnlyClubAttackPolicy.ActorClub})
                    &&v.Clubs.Single(x=>x.Id==TestOnlyClubAttackPolicy.ActorClub).HeldBy==TestOnlyPolicy.ActorId,
                    "Initial progression facts are not the fixed Soldier 1 baseline.");
                var bytes=Bytes(s);Require(bytes.SequenceEqual(Bytes(new Simulation(p,new SnapshotCodec().Decode(bytes),ExecutionProfile.Laboratory))),"Schema21 initial state did not roundtrip.");
            });
            cases.Add("character_advancement_rejects_missing_hit_dice_and_unknown_feature_grants",()=>{
                var p=AdvancementPolicy();var initial=World(p).Capture();var missingDice=initial.Copy();missingDice.CharacterHitDice=Array.Empty<CharacterHitDieRecord>();
                Throws<ArgumentException>(()=>new SnapshotCodec().Encode(missingDice));
                var s=World(p);WorldCommit(s,AwardMilestone(s));WorldCommit(s,AdvanceLevel(s));var invalid=s.Capture();var grant=invalid.CharacterFeatureGrants[0];
                invalid.CharacterFeatureGrants[0]=new CharacterFeatureGrantRecord(grant.ActorId,"soldier.base.unimplemented",grant.ClassName,grant.ClassLevel,grant.MilestoneId,grant.GrantedRevision);
                Throws<ArgumentException>(()=>new SnapshotCodec().Encode(invalid));
                foreach(int schema in new[]{21,22,23}) {
                    invalid=s.Capture();invalid.SchemaVersion=schema;
                    invalid.CharacterFeatureGrants=invalid.CharacterFeatureGrants.Concat(new[]{new CharacterFeatureGrantRecord(TestOnlyPolicy.ActorId,
                        CharacterFeatureIds.Overwatch,"Soldier",1,"opening.milestone.soldier-2",invalid.CharacterAdvancements.Single().Revision)}).ToArray();
                    Throws<ArgumentException>(()=>new SnapshotCodec().Encode(invalid));
                }
            });
            cases.Add("character_advancement_requires_host_award_and_unique_milestone",()=>{
                var p=AdvancementPolicy();var s=World(p);var noHost=new Authority("observer",new[]{TestOnlyPolicy.ActorId});
                RejectUnchanged(s,noHost,AwardMilestone(s),"NotAuthorized");
                var emptyControlHost=new Authority("director",Array.Empty<string>(),canModifyWorld:true);
                var award=s.Execute(emptyControlHost,AwardMilestone(s));Require(award.Outcome==Outcome.Committed,"World authority could not award milestone to a non-controlled actor.");
                var before=Bytes(s);var duplicate=s.Execute(emptyControlHost,AwardMilestone(s,id:"milestone.award.again"));
                Require(duplicate.Outcome==Outcome.Rejected&&duplicate.Code=="MilestoneAlreadyAwarded"&&before.SequenceEqual(Bytes(s)),"Semantic duplicate milestone was not rejected unchanged.");
            });
            cases.Add("character_advancement_preserves_a_spent_prior_hit_die",()=>{
                var p=new TestOnlySharedWorldPolicy(new CharacterAdvancementFixture(null,startingHitDieSpent:true),new SharedCombatFixture());
                var s=World(p);WorldCommit(s,AwardMilestone(s));WorldCommit(s,AdvanceLevel(s));
                var dice=s.Capture().CharacterHitDice.Where(x=>x.ActorId==TestOnlyPolicy.ActorId).OrderBy(x=>x.LevelOrdinal).ToArray();
                Require(dice.Length==2&&dice[0].Spent&&!dice[1].Spent,"Level gain refreshed a spent Hit Die or failed to add one unspent Hit Die.");
            });
            cases.Add("character_advancement_incomplete_and_unsupported_selections_are_atomic",()=>{
                var p=AdvancementPolicy();var s=World(p);WorldCommit(s,AwardMilestone(s));
                RejectUnchanged(s,host,AdvanceLevel(s,one:"",two:""),"IncompleteFeatureSelection");
                RejectUnchanged(s,host,AdvanceLevel(s,one:"soldier.base.unknown",two:CharacterAdvancementFixture.TacticalReposition,id:"character.advance.outside-schedule"),"FeatureOutsideClassSchedule");
                RejectUnchanged(s,host,AdvanceLevel(s,one:"soldier.base.steady-aim",two:CharacterAdvancementFixture.DefensivePositioning,
                    id:"character.advance.legal-but-unimplemented"),"LegalFeatureChoiceNotImplemented");
                Require(s.Capture().CharacterMilestones.Single().ConsumedRevision==0&&s.Capture().Characters.Single(x=>x.ActorId==TestOnlyPolicy.ActorId).Levels.Count==1,
                    "Rejected selection consumed the entitlement or partially advanced the character.");
            });
            cases.Add("character_advancement_uses_next_class_schedule_and_retains_unbound_level_three_entitlement",()=>{
                var p=AdvancementPolicy();var s=World(p);WorldCommit(s,AwardMilestone(s));WorldCommit(s,AdvanceLevel(s));
                const string nextMilestone="opening.milestone.soldier-3";
                WorldCommit(s,AwardMilestone(s,nextMilestone,id:"milestone.award.soldier3"));
                var row=ClassAdvancementScheduleCatalog.Get("Soldier",3);
                var candidates=ClassAdvancementOptionCatalog.Candidates(row);
                var active=candidates.First(x=>x.Kind=="active"&&!x.HasPathConstraint&&!x.HasDeclaredPrerequisite);
                var passive=candidates.First(x=>x.Kind!="active"&&!x.HasPathConstraint&&!x.HasDeclaredPrerequisite);
                Require(row.RequiredSelections==2&&row.MinimumActiveSelections==1&&active.MinimumClassLevel==3&&passive.MinimumClassLevel==3,
                    "The level-three request did not come from the next source schedule row.");
                var before=Bytes(s);
                RejectUnchanged(s,host,AdvanceLevel(s,milestone:nextMilestone,one:active.Id,two:passive.Id,id:"character.advance.soldier3-unbound"),
                    "LegalFeatureChoiceNotImplemented");
                var state=s.Capture();
                Require(before.SequenceEqual(Bytes(s))&&state.CharacterMilestones.Single(x=>x.MilestoneId==nextMilestone).ConsumedRevision==0
                    &&state.Characters.Single(x=>x.ActorId==TestOnlyPolicy.ActorId).Levels.Count==2&&state.CharacterAdvancements.Length==1,
                    "An unbound next-level row consumed its entitlement or partially changed progression.");
            });
            cases.Add("character_advancement_fixed_average_grants_cards_and_hit_die_without_healing",()=>{
                var p=AdvancementPolicy();var s=World(p);WorldCommit(s,AwardMilestone(s));WorldCommit(s,AdvanceLevel(s));var v=s.Capture();
                var character=v.Characters.Single(x=>x.ActorId==TestOnlyPolicy.ActorId);var life=v.Lives.Single(x=>x.ActorId==TestOnlyPolicy.ActorId);
                var result=v.CharacterAdvancements.Single();
                Require(v.SchemaVersion==21&&character.Levels.Count==2&&character.Levels[1].BaseHp==6&&life.MaximumHp==16&&life.Hp==4
                    &&v.CharacterHitDice.Count(x=>x.ActorId==TestOnlyPolicy.ActorId)==2&&!v.CharacterHitDice.Single(x=>x.LevelOrdinal==1).Spent
                    &&!v.CharacterHitDice.Single(x=>x.LevelOrdinal==2).Spent&&v.CharacterFeatureGrants.Select(x=>x.FeatureId).OrderBy(x=>x,StringComparer.Ordinal)
                        .SequenceEqual(new[]{CharacterAdvancementFixture.DefensivePositioning,CharacterAdvancementFixture.TacticalReposition}.OrderBy(x=>x,StringComparer.Ordinal))
                    &&v.CharacterMilestones.Single().ConsumedRevision==v.Revision&&result.HitPointMethod==HitPointGainMethod.FixedAverage
                    &&result.MaximumHpBefore==10&&result.MaximumHpAfter==16&&result.CurrentHpBefore==4&&result.CurrentHpAfter==4,
                    "Advancement did not preserve current HP while recording the sourced fixed-average increase and exact grants.");
                var bytes=Bytes(s);var restored=new Simulation(p,new SnapshotCodec().Decode(bytes),ExecutionProfile.Laboratory);
                Require(bytes.SequenceEqual(Bytes(restored)),"Advancement replay changed canonical save bytes.");
                var path=Path.Combine(directory,"soldier-level2.bin");new FileSaveStore().Save(path,v);
                Require(bytes.SequenceEqual(new SnapshotCodec().Encode(new FileSaveStore().Load(path))),"Schema21 advancement save did not persist.");
            });
            cases.Add("character_advancement_waits_for_traversal_and_tactical_control",()=>{
                var p=AdvancementPolicy();var s=World(p);WorldCommit(s,AwardMilestone(s));
                WorldCommit(s,new Command("level.traversal",TestOnlyPolicy.ActorId,s.Capture().Revision,CommandKind.BeginWorldStep,"walk",1,0));
                RejectUnchanged(s,host,AdvanceLevel(s,id:"advance.during.traversal"),"CharacterBusy");
                s=World(AdvancementPolicy());WorldCommit(s,AwardMilestone(s));
                WorldCommit(s,new Command("level.begin.combat",TestOnlyPolicy.ActorId,s.Capture().Revision,CommandKind.BeginFixedEncounter));
                RejectUnchanged(s,host,AdvanceLevel(s,id:"advance.during.tactical"),"TacticalControlActive");
            });
            cases.Add("character_advancement_preserves_down_state_and_temporary_resources",()=>{
                var initial=new ActorLifeRecord(TestOnlyPolicy.ActorId,10,0,3,new[]{2},true,false,true,3,1,new RuleTime(60),0,true,new[]{TestOnlyClubAttackPolicy.ActorClub});
                var p=AdvancementPolicy(initial);var s=World(p);WorldCommit(s,AwardMilestone(s));WorldCommit(s,AdvanceLevel(s));var life=s.Capture().Lives.Single(x=>x.ActorId==TestOnlyPolicy.ActorId);
                Require(life.MaximumHp==16&&life.Hp==0&&life.TemporaryHp==3&&life.LinkedInjuries.SequenceEqual(new[]{2})&&life.Stable&&!life.Dead
                    &&life.UsesDeathSaves&&life.DeathSuccesses==3&&life.DeathFailures==1&&life.StableUntil==new RuleTime(60)&&life.Prone,
                    "Level advancement healed or rewrote incapacitated life state.");
            });
            cases.Add("soldier_features_apply_explicit_cover_and_tactical_reposition_preserves_press",()=>{
                uint seed=1;while(PlaytestDice.RollD20(seed).Natural<11||PlaytestDice.RollD20(seed).Natural==20)seed++;
                var life=new ActorLifeRecord(TestOnlyPolicy.ActorId,10,10,0,Array.Empty<int>(),false,false,true,0,0,null,0,false,new[]{TestOnlyClubAttackPolicy.ActorClub});
                var fixture=new CharacterAdvancementFixture(life,new TacticalCoverRecord("cover.stone-pillar",1,1));
                var p=new TestOnlySharedWorldPolicy(fixture,new SharedCombatFixture(seed:seed));var s=World(p);
                WorldCommit(s,AwardMilestone(s));WorldCommit(s,AdvanceLevel(s));WorldAdvance(s,3);
                WorldStep(s,1,0);WorldAdvance(s,1);WorldStep(s,1,0);WorldAdvance(s,1);WorldStep(s,1,0);
                Require(s.Capture().InventoryCombat&&s.Capture().Encounter.CurrentActor==AdditionalTacticalActor.Id,
                    "The combat fixture did not enter on its authored initiative slot.");
                WorldCommit(s,Tac(s,CommandKind.SelectCombatStance,stance:(int)CombatStance.Aggressive,actor:AdditionalTacticalActor.Id));
                WorldCommit(s,Tac(s,CommandKind.TacticalStep,x:3,y:0,actor:AdditionalTacticalActor.Id));
                WorldCommit(s,Tac(s,CommandKind.AttackClub,target:TestOnlyPolicy.ActorId,actor:AdditionalTacticalActor.Id,weapon:AdditionalTacticalActor.ClubId));
                Require(s.Capture().MeleeAttacks.Single().Attack.ArmorClass==11&&s.Capture().Presses.Any(x=>x.ActorId==AdditionalTacticalActor.Id&&x.TargetId==TestOnlyPolicy.ActorId),
                    "Explicit qualifying cover did not grant +1 AC, or the source attack failed to arm Press.");
                WorldCommit(s,Tac(s,CommandKind.EndRegularTurn,actor:AdditionalTacticalActor.Id));
                var feature=Tac(s,CommandKind.ActivateTacticalReposition);WorldCommit(s,feature);
                long ordinarySpent=WorldLedger(s).MovementSpent.Numerator;
                var runtime=s.Capture().CharacterFeatureRuntime.Single();
                Require(runtime.RepositionRechargeRemaining==2&&!runtime.BonusActionAvailable&&runtime.RepositionBudgetRemaining==15,
                    "Activation did not spend its Bonus Action or establish the half-Speed budget and Recharge 2.");
                WorldCommit(s,Tac(s,CommandKind.TacticalRepositionStep,x:1,y:0));
                var state=s.Capture();var offer=state.PressOffers.Single(x=>x.Status==PressOfferStatus.Pending);
                Require(state.Actors.Single(x=>x.Id==TestOnlyPolicy.ActorId).X==1&&state.TacticalMoves.Last().Kind==TacticalMoveKind.TacticalReposition
                    &&state.TacticalMoves.Last().Reactors.Count==0&&state.MeleeAttacks.Length==1&&state.CharacterFeatureRuntime.Single().RepositionBudgetRemaining==10
                    &&WorldLedger(s).MovementSpent.Numerator==ordinarySpent&&offer.ActorId==AdditionalTacticalActor.Id,
                    "Reposition provoked an OA, spent ordinary movement, lost Press, or mispaid its special budget.");
                WorldCommit(s,Tac(s,CommandKind.RespondPress,target:offer.Id,actor:AdditionalTacticalActor.Id,choice:true));
                WorldCommit(s,Tac(s,CommandKind.TacticalRepositionStep,x:0,y:0));
                Require(s.Capture().TacticalMoves.Last().Kind==TacticalMoveKind.TacticalReposition&&s.Capture().CharacterFeatureRuntime.Single().RepositionBudgetRemaining==5
                    &&s.Capture().TacticalActors.Single(x=>x.ActorId==AdditionalTacticalActor.Id).PressConsumed,
                    "Accepted Press did not resolve before continuing the paid reposition budget.");
                WorldCommit(s,Tac(s,CommandKind.SelectCombatStance,stance:(int)CombatStance.Aggressive));WorldCommit(s,Tac(s,CommandKind.EndRegularTurn));
                WorldCommit(s,Tac(s,CommandKind.SelectCombatStance,actor:AdditionalTacticalActor.Id,stance:(int)CombatStance.Aggressive));WorldCommit(s,Tac(s,CommandKind.EndRegularTurn,actor:AdditionalTacticalActor.Id));
                Require(s.Capture().Encounter.CurrentActor==TestOnlyPolicy.ActorId&&s.Capture().CharacterFeatureRuntime.Single().RepositionRechargeRemaining==1
                    &&s.Capture().CharacterFeatureRuntime.Single().BonusActionAvailable,"Recharge did not advance on the Soldier's next regular start.");
                RejectUnchanged(s,host,Tac(s,CommandKind.ActivateTacticalReposition),"TacticalRepositionRecharging");
                WorldCommit(s,Tac(s,CommandKind.SelectCombatStance,stance:(int)CombatStance.Aggressive));WorldCommit(s,Tac(s,CommandKind.EndRegularTurn));
                WorldCommit(s,Tac(s,CommandKind.SelectCombatStance,actor:AdditionalTacticalActor.Id,stance:(int)CombatStance.Aggressive));WorldCommit(s,Tac(s,CommandKind.EndRegularTurn,actor:AdditionalTacticalActor.Id));
                Require(s.Capture().CharacterFeatureRuntime.Single().RepositionRechargeRemaining==0,"Recharge 2 did not become ready after two of the Soldier's regular starts.");
                var bytes=Bytes(s);Require(bytes.SequenceEqual(Bytes(new Simulation(p,new SnapshotCodec().Decode(bytes),ExecutionProfile.Laboratory))),"Feature runtime did not survive canonical replay.");
            });
            cases.Add("overwatch_schema24_separates_automatic_grant_and_persists_shared_bonus_actions",()=>{
                var p=new TestOnlySharedWorldPolicy(new OverwatchFoundationFixture(),new CharacterAdvancementFixture(),new SharedCombatFixture());
                var s=World(p);var v=s.Capture();var automatic=v.CharacterFeatureGrants.Single();
                Require(v.SchemaVersion==Snapshot.SharedBonusActionSchema&&v.BonusActions.Length==2
                    &&v.BonusActions.Single(x=>x.ActorId==TestOnlyPolicy.ActorId).LastRegularStart==0
                    &&v.BonusActions.All(x=>x.Available)&&automatic.FeatureId==CharacterFeatureIds.Overwatch
                    &&automatic.Origin==CharacterFeatureGrantOrigin.AutomaticClassFeature&&automatic.MilestoneId==""&&automatic.GrantedRevision==0
                    &&v.CharacterFeatureGrants.Count(x=>x.Origin==CharacterFeatureGrantOrigin.SelectedCard)==0,
                    "Schema24 did not model the shared interval budget and automatic Overwatch outside selected-card grants.");
                var codec=new SnapshotCodec();var bytes=codec.Encode(v);var restored=codec.Decode(bytes);
                Require(bytes.SequenceEqual(codec.Encode(restored))&&restored.CharacterFeatureGrants.Single().Origin==CharacterFeatureGrantOrigin.AutomaticClassFeature,
                    "Schema24 origin or action budget did not survive canonical save encoding.");
                var missing=v.Copy();missing.BonusActions=missing.BonusActions.Take(1).ToArray();Throws<ArgumentException>(()=>codec.Encode(missing));
                var stale=v.Copy();stale.BonusActions=stale.BonusActions.Select(x=>x.ActorId==TestOnlyPolicy.ActorId?new ActorBonusActionRecord(x.ActorId,-1):x).ToArray();
                Throws<ArgumentException>(()=>codec.Encode(stale));
            });
            cases.Add("soldier_schema27_persists_initial_cards_separately_from_automatic_overwatch",()=>{
                var p=new TestOnlySharedWorldPolicy(new SoldierInitialLoadoutFixture(),new OverwatchFoundationFixture(),
                    new CharacterAdvancementFixture(),new SharedCombatFixture());
                var s=World(p);var v=s.Capture();var selection=v.InitialClassSelections.Single();
                Require(v.SchemaVersion==Snapshot.SoldierInitialLoadoutSchema
                    &&v.Characters.Single(x=>x.ActorId==TestOnlyPolicy.ActorId).ProfileId==CharacterAdvancementProfileIds.TestOnlySoldierLevel1WithInitialCards
                    &&selection.ClassName=="Soldier"&&selection.ClassLevel==1&&selection.SourceRevision==SoldierInitialLoadoutFixture.SourceRevision
                    &&selection.SelectedFeatureIds.OrderBy(x=>x,StringComparer.Ordinal).SequenceEqual(new[]{CharacterFeatureIds.WarningShot,
                        CharacterFeatureIds.TacticalReposition,CharacterFeatureIds.ShieldTrained,CharacterFeatureIds.CoveringFire}.OrderBy(x=>x,StringComparer.Ordinal))
                    &&v.CharacterMilestones.Length==0&&v.CharacterFeatureGrants.Count(x=>x.Origin==CharacterFeatureGrantOrigin.InitialClassSelection)==4
                    &&v.CharacterFeatureGrants.Single(x=>x.FeatureId==CharacterFeatureIds.Overwatch).Origin==CharacterFeatureGrantOrigin.AutomaticClassFeature,
                    "Level 1 cards were not recorded as initial selections separately from automatic Overwatch.");
                var codec=new SnapshotCodec();var bytes=codec.Encode(v);var restored=codec.Decode(bytes);
                Require(bytes.SequenceEqual(codec.Encode(restored))&&restored.InitialClassSelections.Single().SelectedFeatureIds.SequenceEqual(selection.SelectedFeatureIds),
                    "Schema27 initial class selections did not survive canonical persistence.");
                var resumed=new Simulation(p,restored,ExecutionProfile.Laboratory);
                WorldCommit(resumed,new Command("soldier.initial.begin-combat",TestOnlyPolicy.ActorId,resumed.Capture().Revision,CommandKind.BeginFixedEncounter));
                WorldCommit(resumed,Tac(resumed,CommandKind.ActivateTacticalReposition));
                Require(resumed.Capture().CharacterFeatureRuntime.Single().RepositionRechargeRemaining==2
                    &&!resumed.Capture().BonusActions.Single(x=>x.ActorId==TestOnlyPolicy.ActorId).Available,
                    "Restored initial card ownership could not activate Tactical Reposition through the shared Bonus Action ledger.");
                var missingGrant=v.Copy();missingGrant.CharacterFeatureGrants=missingGrant.CharacterFeatureGrants
                    .Where(x=>x.FeatureId!=CharacterFeatureIds.WarningShot).ToArray();Throws<ArgumentException>(()=>codec.Encode(missingGrant));
                var wrongProfile=v.Copy();wrongProfile.Characters=wrongProfile.Characters.Select(x=>x.ActorId==TestOnlyPolicy.ActorId
                    ?new ActorCharacterRecord(x.ActorId,CharacterAdvancementProfileIds.TestOnlySoldierLevel1,x.Abilities,x.Levels):x).ToArray();
                Throws<ArgumentException>(()=>codec.Encode(wrongProfile));
                var oldSchema=v.Copy();oldSchema.SchemaVersion=Snapshot.OverwatchExecutionSchema;Throws<ArgumentException>(()=>codec.Encode(oldSchema));
                var milestone=new Command("soldier.initial.level-up",TestOnlyPolicy.ActorId,v.Revision,CommandKind.AwardCharacterMilestone,"soldier.level2");
                RejectUnchanged(s,TestOnlySharedWorldPolicy.Host(),milestone,"UnsupportedAdvancementPath");
            });
            cases.Add("overwatch_schema24_reposition_spends_shared_budget_and_regular_start_refills_it",()=>{
                var p=new TestOnlySharedWorldPolicy(new OverwatchFoundationFixture(),new CharacterAdvancementFixture(),new SharedCombatFixture());
                var s=World(p);WorldCommit(s,AwardMilestone(s));WorldCommit(s,AdvanceLevel(s));
                WorldCommit(s,new Command("schema24.begin.combat",TestOnlyPolicy.ActorId,s.Capture().Revision,CommandKind.BeginFixedEncounter));
                WorldCommit(s,Tac(s,CommandKind.ActivateTacticalReposition));var after=s.Capture();
                Require(!after.BonusActions.Single(x=>x.ActorId==TestOnlyPolicy.ActorId).Available
                    &&!after.CharacterFeatureRuntime.Single(x=>x.ActorId==TestOnlyPolicy.ActorId).BonusActionAvailable,
                    "Tactical Reposition did not consume the common schema24 Bonus Action budget.");
                WorldCommit(s,Tac(s,CommandKind.SelectCombatStance,stance:(int)CombatStance.Aggressive));
                WorldCommit(s,Tac(s,CommandKind.EndRegularTurn));
                WorldCommit(s,Tac(s,CommandKind.SelectCombatStance,actor:AdditionalTacticalActor.Id,stance:(int)CombatStance.Aggressive));
                WorldCommit(s,Tac(s,CommandKind.EndRegularTurn,actor:AdditionalTacticalActor.Id));
                var refreshed=s.Capture();Require(refreshed.Encounter.CurrentActor==TestOnlyPolicy.ActorId
                    &&refreshed.BonusActions.Single(x=>x.ActorId==TestOnlyPolicy.ActorId).Available
                    &&refreshed.BonusActions.Single(x=>x.ActorId==TestOnlyPolicy.ActorId).LastRegularStart==2
                    &&refreshed.CharacterFeatureRuntime.Single(x=>x.ActorId==TestOnlyPolicy.ActorId).BonusActionAvailable
                    &&refreshed.CharacterFeatureRuntime.Single(x=>x.ActorId==TestOnlyPolicy.ActorId).RepositionRechargeRemaining==1,
                    "The next regular start did not refill the shared Bonus Action budget and independently advance Reposition Recharge.");
                var bytes=Bytes(s);Require(bytes.SequenceEqual(Bytes(new Simulation(p,new SnapshotCodec().Decode(bytes),ExecutionProfile.Laboratory))),
                    "Schema24 shared action budget did not survive command replay.");
            });
            cases.Add("overwatch_schema25_designation_spends_shared_bonus_action_and_persists_zone",()=>{
                var periodic=new PeriodicRiderFixture(new[]{new PeriodicRiderApplicationFact("fixture.bleed.event","fixture.bleed",TestOnlyPolicy.ActorId,AdditionalTacticalActor.Id,10)});
                var p=new TestOnlySharedWorldPolicy(new OverwatchDesignationFixture(),new OverwatchFoundationFixture(),periodic,
                    new RepeatingCrossbowFixture(),new CharacterAdvancementFixture(),new SharedCombatFixture());
                var s=World(p);Require(s.Capture().SchemaVersion==Snapshot.OverwatchSchema&&s.Capture().OverwatchIntervals.Single().ShotStatus==OverwatchShotStatus.Available,
                    "Schema25 did not initialize the interval-owned Overwatch entitlement.");
                WorldCommit(s,new Command("schema25.begin.combat",TestOnlyPolicy.ActorId,s.Capture().Revision,CommandKind.BeginFixedEncounter));
                WorldCommit(s,Tac(s,CommandKind.SelectCombatStance,stance:(int)CombatStance.Aggressive));
                var designation=new Command("schema25.designate",TestOnlyPolicy.ActorId,s.Capture().Revision,CommandKind.DesignateOverwatch,
                    s.Capture().Encounter.CurrentTurnId,x:1,y:-1);
                WorldCommit(s,designation);var v=s.Capture();var zone=v.OverwatchDesignations.Single();
                Require(zone.Status==OverwatchDesignationStatus.Active&&zone.Contains(3,0)&&!zone.Contains(4,0)
                    &&v.OverwatchIntervals.Single().ShotStatus==OverwatchShotStatus.Available
                    &&!v.BonusActions.Single(x=>x.ActorId==TestOnlyPolicy.ActorId).Available,
                    "Designation did not persist its fixed 3-by-3 zone, preserve the interval shot, or spend the common Bonus Action.");
                var codec=new SnapshotCodec();var bytes=codec.Encode(v);var restored=codec.Decode(bytes);
                Require(bytes.SequenceEqual(codec.Encode(restored))&&zone.SameAs(restored.OverwatchDesignations.Single()),
                    "Schema25 designation did not survive canonical save encoding.");
                var second=new Command("schema25.designate.again",TestOnlyPolicy.ActorId,s.Capture().Revision,CommandKind.DesignateOverwatch,
                    s.Capture().Encounter.CurrentTurnId,x:1,y:-1);
                RejectUnchanged(s,host,second,"BonusActionUnavailable");
                Require(s.Capture().OverwatchDesignations.Single().Status==OverwatchDesignationStatus.Active,
                    "A rejected redeployment removed the previously active zone.");
            });
            cases.Add("overwatch_schema25_redeployment_replaces_zone_and_preserves_each_interval_shot_status",()=>{
                var periodic=new PeriodicRiderFixture(new[]{new PeriodicRiderApplicationFact("fixture.bleed.event","fixture.bleed",TestOnlyPolicy.ActorId,AdditionalTacticalActor.Id,10)});
                var p=new TestOnlySharedWorldPolicy(new OverwatchDesignationFixture(),new OverwatchFoundationFixture(),periodic,
                    new RepeatingCrossbowFixture(),new CharacterAdvancementFixture(),new SharedCombatFixture());
                var designated=World(p);WorldCommit(designated,new Command("schema25.replace.begin",TestOnlyPolicy.ActorId,designated.Capture().Revision,CommandKind.BeginFixedEncounter));
                WorldCommit(designated,Tac(designated,CommandKind.SelectCombatStance,stance:(int)CombatStance.Aggressive));
                WorldCommit(designated,new Command("schema25.replace.first",TestOnlyPolicy.ActorId,designated.Capture().Revision,CommandKind.DesignateOverwatch,
                    designated.Capture().Encounter.CurrentTurnId,x:1,y:-1));
                var baseState=designated.Capture();
                foreach(var status in new[]{OverwatchShotStatus.Available,OverwatchShotStatus.Spent,OverwatchShotStatus.Forfeited}) {
                    var seeded=baseState.Copy();
                    seeded.OverwatchIntervals=seeded.OverwatchIntervals.Select(x=>x.ActorId==TestOnlyPolicy.ActorId?x.WithStatus(status):x).ToArray();
                    seeded.BonusActions=seeded.BonusActions.Select(x=>x.ActorId==TestOnlyPolicy.ActorId
                        ?new ActorBonusActionRecord(x.ActorId,x.LastRegularStart,true):x).ToArray();
                    seeded.CharacterFeatureRuntime=seeded.CharacterFeatureRuntime.Select(x=>x.ActorId==TestOnlyPolicy.ActorId
                        ?x.WithBonusActionAvailable(true):x).ToArray();
                    // The current Base fixture has one Bonus Action per interval, so its normal
                    // command sequence cannot redeploy before the zone expires. Exercise the
                    // agreed replacement transition directly with a structurally valid available
                    // ledger; this does not add a second Bonus Action grant to the fixture.
                    var replacement=new Command("schema25.replace."+(int)status,TestOnlyPolicy.ActorId,seeded.Revision,
                        CommandKind.DesignateOverwatch,seeded.Encounter.CurrentTurnId,x:1,y:-1);
                    Require(p.Resolve(seeded,replacement)==null,"A valid available Bonus Action did not permit replacement.");
                    var after=seeded;var old=after.OverwatchDesignations.Single(x=>x.CreatedRevision==baseState.Revision);
                    var current=after.OverwatchDesignations.Single(x=>x.Status==OverwatchDesignationStatus.Active);
                    Require(old.Status==OverwatchDesignationStatus.Replaced&&current.Id!=old.Id&&current.LastRegularStart==old.LastRegularStart
                        &&after.OverwatchIntervals.Single(x=>x.ActorId==TestOnlyPolicy.ActorId).ShotStatus==status
                        &&!after.BonusActions.Single(x=>x.ActorId==TestOnlyPolicy.ActorId).Available,
                        "Redeployment failed to replace only the zone, preserve its interval endpoint/shot status, and spend the available shared Bonus Action.");
                }
            });
            cases.Add("overwatch_schema25_interval_history_compacts_after_sparse_long_world_advance",()=>{
                var periodic=new PeriodicRiderFixture(new[]{new PeriodicRiderApplicationFact("fixture.bleed.event","fixture.bleed",TestOnlyPolicy.ActorId,AdditionalTacticalActor.Id,10)});
                var p=new TestOnlySharedWorldPolicy(new OverwatchDesignationFixture(),new OverwatchFoundationFixture(),periodic,
                    new RepeatingCrossbowFixture(),new CharacterAdvancementFixture(),new SharedCombatFixture());
                var s=World(p);WorldAdvance(s,1000);var v=s.Capture();
                Require(v.OverwatchIntervals.Length<=2&&v.OverwatchIntervals.Where(x=>x.ActorId==TestOnlyPolicy.ActorId)
                    .OrderByDescending(x=>x.LastRegularStart).First().LastRegularStart>64,
                    "A large sparse calendar advance retained unbounded Overwatch interval history or failed to reach the new interval.");
            });
            cases.Add("overwatch_schema25_rejects_unknown_placement_and_invisible_zone_before_payment",()=>{
                var periodic=new PeriodicRiderFixture(new[]{new PeriodicRiderApplicationFact("fixture.bleed.event", "fixture.bleed",TestOnlyPolicy.ActorId,AdditionalTacticalActor.Id,10)});
                TestOnlySharedWorldPolicy Policy(OverwatchDesignationFixture fixture)=>new TestOnlySharedWorldPolicy(fixture,new OverwatchFoundationFixture(),periodic,
                    new RepeatingCrossbowFixture(),new CharacterAdvancementFixture(),new SharedCombatFixture());
                var s=World(Policy(new OverwatchDesignationFixture()));
                WorldCommit(s,new Command("schema25.invalid.begin",TestOnlyPolicy.ActorId,s.Capture().Revision,CommandKind.BeginFixedEncounter));
                WorldCommit(s,Tac(s,CommandKind.SelectCombatStance,stance:(int)CombatStance.Aggressive));
                RejectUnchanged(s,host,new Command("schema25.unknown.zone",TestOnlyPolicy.ActorId,s.Capture().Revision,CommandKind.DesignateOverwatch,
                    s.Capture().Encounter.CurrentTurnId,x:2,y:-1),"UnsupportedOverwatchPlacement");
                var invisible=World(Policy(new OverwatchDesignationFixture(1,-1,false)));
                WorldCommit(invisible,new Command("schema25.invisible.begin",TestOnlyPolicy.ActorId,invisible.Capture().Revision,CommandKind.BeginFixedEncounter));
                WorldCommit(invisible,Tac(invisible,CommandKind.SelectCombatStance,stance:(int)CombatStance.Aggressive));
                RejectUnchanged(invisible,host,new Command("schema25.invisible.zone",TestOnlyPolicy.ActorId,invisible.Capture().Revision,CommandKind.DesignateOverwatch,
                    invisible.Capture().Encounter.CurrentTurnId,x:1,y:-1),"OverwatchZoneNotVisible");
                Require(invisible.Capture().OverwatchDesignations.Length==0&&invisible.Capture().BonusActions.Single(x=>x.ActorId==TestOnlyPolicy.ActorId).Available,
                    "An invisible-zone rejection mutated the designation or Bonus Action ledger.");
            });
            cases.Add("overwatch_schema25_zone_expires_and_interval_entitlement_refreshes_at_next_soldier_start",()=>{
                var periodic=new PeriodicRiderFixture(new[]{new PeriodicRiderApplicationFact("fixture.bleed.event","fixture.bleed",TestOnlyPolicy.ActorId,AdditionalTacticalActor.Id,10)});
                var p=new TestOnlySharedWorldPolicy(new OverwatchDesignationFixture(),new OverwatchFoundationFixture(),periodic,
                    new RepeatingCrossbowFixture(),new CharacterAdvancementFixture(),new SharedCombatFixture());
                var s=World(p);WorldCommit(s,new Command("schema25.expire.begin",TestOnlyPolicy.ActorId,s.Capture().Revision,CommandKind.BeginFixedEncounter));
                WorldCommit(s,Tac(s,CommandKind.SelectCombatStance,stance:(int)CombatStance.Aggressive));
                WorldCommit(s,new Command("schema25.expire.designate",TestOnlyPolicy.ActorId,s.Capture().Revision,CommandKind.DesignateOverwatch,
                    s.Capture().Encounter.CurrentTurnId,x:1,y:-1));
                WorldCommit(s,Tac(s,CommandKind.EndRegularTurn));
                WorldCommit(s,Tac(s,CommandKind.SelectCombatStance,actor:AdditionalTacticalActor.Id,stance:(int)CombatStance.Aggressive));
                WorldCommit(s,Tac(s,CommandKind.EndRegularTurn,actor:AdditionalTacticalActor.Id));
                var v=s.Capture();var interval=v.OverwatchIntervals.Single(x=>x.ActorId==TestOnlyPolicy.ActorId&&x.LastRegularStart==2);
                Require(interval.ShotStatus==OverwatchShotStatus.Available&&v.OverwatchDesignations.Single().Status==OverwatchDesignationStatus.Expired
                    &&v.OverwatchDesignations.Single().EndedRevision==v.Revision
                    &&v.BonusActions.Single(x=>x.ActorId==TestOnlyPolicy.ActorId).Available,
                    "The previous zone survived the next regular start or the new interval did not refresh its shot and Bonus Action.");
                var bytes=Bytes(s);Require(bytes.SequenceEqual(Bytes(new Simulation(p,new SnapshotCodec().Decode(bytes),ExecutionProfile.Laboratory))),
                    "Schema25 interval refresh did not survive command-history replay.");
            });
        }
    }
}
#endif
