#if DECENNIUM_TEST_ONLY && (UNITY_EDITOR || HEADLESS_TESTS)
using System;
using System.Collections.Generic;
using System.Linq;
using Decennium.Foundation.Laboratory;

namespace Decennium.Foundation.Tests
{
    public static partial class FoundationCases
    {
        private static TestOnlySharedWorldPolicy DefensiveFormationPolicy(uint seed=1,int walkingSpeed=60)
            =>new TestOnlySharedWorldPolicy(SoldierCharacterBuildFixture.ForTacticalTechniques(),new OverwatchFoundationFixture(),
                new CharacterAdvancementFixture(null,false,false,true,true,true,true),new SharedCombatFixture(seed:seed),walkingSpeed:walkingSpeed);

        private static void AdvanceSoldierToDefensiveFormation(Simulation s)
        {
            WorldCommit(s,AwardMilestone(s,"opening.milestone.soldier-2",id:"formation.milestone.2"));
            WorldCommit(s,AdvanceLevel(s,id:"formation.advance.2"));
            WorldCommit(s,AwardMilestone(s,"opening.milestone.soldier-3",id:"formation.milestone.3"));
            WorldCommit(s,new Command("formation.advance.3",TestOnlyPolicy.ActorId,s.Capture().Revision,CommandKind.AdvanceCharacterLevel,
                "opening.milestone.soldier-3",advancement:new CharacterAdvancementRequest(new[]{CharacterFeatureIds.CommandStep,
                    CharacterFeatureIds.DefensiveFormation})));
        }

        private static Command ActivateFormation(Simulation s,string[] recipients,string id="formation.activate")
        {
            var v=s.Capture();return new Command(id,v.Encounter.CurrentActor,v.Revision,CommandKind.ActivateDefensiveFormation,
                defensiveFormation:new DefensiveFormationRequest(v.Encounter.CurrentTurnId,recipients));
        }

        private static void AddSoldierDefensiveFormationCases(Dictionary<string,Action> cases,string directory)
        {
            var host=TestOnlySharedWorldPolicy.Host();var codec=new SnapshotCodec();
            cases.Add("soldier_defensive_formation_schema34_grants_source_legal_pair_and_roundtrips",()=>{
                var p=DefensiveFormationPolicy();var s=World(p);
                Require(s.Capture().SchemaVersion==Snapshot.DefensiveFormationSchema,"The explicit Defensive Formation fixture did not select schema34.");
                AdvanceSoldierToDefensiveFormation(s);var v=s.Capture();var grants=v.CharacterFeatureGrants.Where(x=>x.ClassLevel==3)
                    .Select(x=>x.FeatureId).OrderBy(x=>x,StringComparer.Ordinal).ToArray();var bytes=Bytes(s);
                Require(grants.SequenceEqual(new[]{CharacterFeatureIds.CommandStep,CharacterFeatureIds.DefensiveFormation}
                        .OrderBy(x=>x,StringComparer.Ordinal))
                    &&v.CharacterAdvancements.OrderBy(x=>x.ClassLevel).Select(x=>x.NewTotalLevel).SequenceEqual(new[]{2,3})
                    &&bytes.SequenceEqual(Bytes(new Simulation(p,codec.Decode(bytes),ExecutionProfile.Laboratory))),
                    "Schema34 did not atomically grant the third source-legal Soldier level-three pair and replay its advancement history.");
            });
            cases.Add("soldier_defensive_formation_queries_cost_one_bonus_action_and_reject_invalid_targets_purely",()=>{
                var p=DefensiveFormationPolicy();var s=World(p);AdvanceSoldierToDefensiveFormation(s);BeginEncounter(s);
                WorldCommit(s,Tac(s,CommandKind.SelectCombatStance,stance:(int)CombatStance.Aggressive));
                TacStep(s,1,0);TacStep(s,2,0);TacStep(s,3,0);
                var option=ActivateFormation(s,new[]{TestOnlyPolicy.ActorId,TestOnlyPolicy.CompanionId},"formation.query.activate");
                var before=Bytes(s);uint random=s.Capture().RandomState;var query=s.QueryCommand(host,option);
                Require(query.Supported&&query.Admissible&&query.Code=="Available"&&query.Costs.Count==1
                    &&query.Costs[0].Kind=="bonus-action"&&query.Costs[0].Amount==1
                    &&Bytes(s).SequenceEqual(before)&&s.Capture().RandomState==random,
                    "Defensive Formation query was not pure or failed to report exactly one shared Bonus Action.");
                var invalid=ActivateFormation(s,new[]{AdditionalTacticalActor.Id},"formation.query.hostile");
                RejectUnchanged(s,host,invalid,"RecipientMustBeAlly");
                Require(Bytes(s).SequenceEqual(before)&&s.Capture().RandomState==random,
                    "Invalid Defensive Formation recipients changed state or consumed randomness.");
            });
            cases.Add("soldier_defensive_formation_resolves_ordered_optional_shifts_without_oa_or_normal_movement_cost",()=>{
                var p=DefensiveFormationPolicy();var s=World(p);AdvanceSoldierToDefensiveFormation(s);BeginEncounter(s);
                WorldCommit(s,Tac(s,CommandKind.SelectCombatStance,stance:(int)CombatStance.Aggressive));
                TacStep(s,0,1);TacStep(s,1,1);TacStep(s,1,0);TacStep(s,2,0);TacStep(s,3,0);
                long fullMovement=TestOnlyClubAttackPolicy.WalkingSpeed(s.Capture(),TestOnlyPolicy.ActorId);
                var loop=new[]{new[]{3,1},new[]{4,1},new[]{3,0}};int loopIndex=0;
                while(s.Capture().WorldIntervals.Single(x=>x.ActorId==TestOnlyPolicy.ActorId).MovementSpent<new RuleQuantity(fullMovement)) {
                    var next=loop[loopIndex++%loop.Length];TacStep(s,next[0],next[1]);
                }
                Require(s.Capture().WorldIntervals.Single(x=>x.ActorId==TestOnlyPolicy.ActorId).MovementSpent==new RuleQuantity(fullMovement),
                    "The setup did not spend the Soldier's full ordinary movement while keeping the Soldier adjacent to the enemy.");
                var activationCommand=ActivateFormation(s,new[]{TestOnlyPolicy.ActorId,TestOnlyPolicy.CompanionId},"formation.sequence");
                var beforeActivation=s.Capture();WorldCommit(s,activationCommand);var active=s.Capture();var activation=active.DefensiveFormations.Single();
                Require(activation.Active&&activation.Shifts.Select(x=>x.RecipientActorId).SequenceEqual(new[]{TestOnlyPolicy.ActorId,TestOnlyPolicy.CompanionId})
                    &&activation.Shifts[0].Status==DefensiveFormationShiftStatus.AwaitingResponse
                    &&!active.BonusActions.Single(x=>x.ActorId==TestOnlyPolicy.ActorId).Available,
                    "Activation did not immediately persist the ordered recipients, first response, and spent Bonus Action.");
                var pendingBytes=Bytes(s);s=new Simulation(p,codec.Decode(pendingBytes),ExecutionProfile.Laboratory);
                Require(pendingBytes.SequenceEqual(Bytes(s)),"Pending Defensive Formation shift changed on save/restore.");
                var responseBody=Body(s);var current=Tac(s,CommandKind.RespondDefensiveFormation,activation.Id,TestOnlyPolicy.ActorId,
                    x:responseBody.X,y:responseBody.Y,choice:true);
                RejectUnchanged(s,host,current,"InvalidTacticalStep");
                var movementBefore=s.Capture();var spentBefore=movementBefore.ActorMovement.Single(x=>x.ActorId==TestOnlyPolicy.ActorId).Spent;
                var intervalBefore=movementBefore.WorldIntervals.Single(x=>x.ActorId==TestOnlyPolicy.ActorId).MovementSpent;
                Require(intervalBefore==new RuleQuantity(fullMovement),
                    "The independent shift regression did not start with ordinary movement fully spent.");
                int attacksBefore=movementBefore.MeleeAttacks.Length;
                int shiftX=responseBody.X-1,shiftY=responseBody.Y==0?0:responseBody.Y+1;
                WorldCommit(s,Tac(s,CommandKind.RespondDefensiveFormation,activation.Id,TestOnlyPolicy.ActorId,x:shiftX,y:shiftY,choice:true));
                var moved=s.Capture();var completed=moved.DefensiveFormations.Single();var shift=completed.Shifts[0];
                var move=moved.TacticalMoves.Single(x=>x.Id==shift.MoveId);
                Require(shift.Status==DefensiveFormationShiftStatus.Moved&&move.Kind==TacticalMoveKind.DefensiveFormationShift
                    &&move.Status==TacticalMoveStatus.Completed&&move.ParentDefensiveFormationId==activation.Id&&move.CostPaid==5
                    &&move.Reactors.Count==0&&moved.Actors.Single(x=>x.Id==TestOnlyPolicy.ActorId).X==shiftX
                    &&moved.Actors.Single(x=>x.Id==TestOnlyPolicy.ActorId).Y==shiftY
                    &&moved.ActorMovement.Single(x=>x.ActorId==TestOnlyPolicy.ActorId).Spent==spentBefore
                    &&moved.WorldIntervals.Single(x=>x.ActorId==TestOnlyPolicy.ActorId).MovementSpent==intervalBefore
                    &&moved.MeleeAttacks.Length==attacksBefore
                    &&completed.Shifts[1].Status==DefensiveFormationShiftStatus.AwaitingResponse,
                    "The first ordered shift failed to move five feet without opportunity attacks or normal movement debit before offering the next recipient.");
                var betweenBytes=Bytes(s);s=new Simulation(p,codec.Decode(betweenBytes),ExecutionProfile.Laboratory);
                Require(betweenBytes.SequenceEqual(Bytes(s)),"The between-recipient continuation changed on save/restore.");
                WorldCommit(s,Tac(s,CommandKind.RespondDefensiveFormation,activation.Id,TestOnlyPolicy.CompanionId,choice:false));
                var resolved=s.Capture().DefensiveFormations.Single();
                Require(resolved.Active&&resolved.Shifts[0].Status==DefensiveFormationShiftStatus.Moved
                    &&resolved.Shifts[1].Status==DefensiveFormationShiftStatus.Declined
                    &&CharacterAdvancementRules.ReduceIncomingDamage(SeparatedFormationTestSnapshot(s.Capture()),TestOnlyPolicy.ActorId,10)==10,
                    "Declining the second shift did not preserve formation protection, or a separated ally incorrectly counted as adjacent.");
                var copy=s.Capture().Copy();var soldier=copy.Actors.Single(x=>x.Id==TestOnlyPolicy.ActorId);
                copy.Actors=copy.Actors.Select(x=>x.Id==TestOnlyPolicy.CompanionId?Moved(x,soldier.X+1,soldier.Y):x).ToArray();
                copy.ShieldStationarity=copy.ShieldStationarity.Select(x=>x.ActorId==TestOnlyPolicy.ActorId
                    ?new ShieldStationarityRecord(x.ActorId,x.LastRegularStart,true):x).ToArray();
                Require(CharacterAdvancementRules.ReduceIncomingDamage(copy,TestOnlyPolicy.ActorId,10)==9,
                    "Active Defensive Formation did not reduce damage by one while the recipients were adjacent.");
                copy.Actors=copy.Actors.Select(x=>x.Id==TestOnlyPolicy.CompanionId?Moved(x,0,4):x).ToArray();
                Require(CharacterAdvancementRules.ReduceIncomingDamage(copy,TestOnlyPolicy.ActorId,10)==10,
                    "Defensive Formation failed to recalculate adjacency after one recipient moved away.");
                copy.Actors=copy.Actors.Select(x=>x.Id==TestOnlyPolicy.CompanionId?Moved(x,soldier.X+1,soldier.Y):x).ToArray();
                copy.ShieldStationarity=copy.ShieldStationarity.Select(x=>x.ActorId==TestOnlyPolicy.ActorId
                    ?new ShieldStationarityRecord(x.ActorId,x.LastRegularStart,false):x).ToArray();
                Require(CharacterAdvancementRules.ReduceIncomingDamage(copy,TestOnlyPolicy.ActorId,10)==9,
                    "Shield Trained and Defensive Formation stacked instead of applying only the strongest flat reduction.");
            });
            cases.Add("soldier_defensive_formation_expires_at_owner_next_start_and_remains_one_use_per_encounter",()=>{
                var p=DefensiveFormationPolicy();var s=World(p);AdvanceSoldierToDefensiveFormation(s);BeginEncounter(s);
                WorldCommit(s,Tac(s,CommandKind.SelectCombatStance,stance:(int)CombatStance.Aggressive));
                var command=ActivateFormation(s,new[]{TestOnlyPolicy.ActorId,TestOnlyPolicy.CompanionId},"formation.expiry");
                WorldCommit(s,command);
                WorldCommit(s,Tac(s,CommandKind.RespondDefensiveFormation,command.Id,TestOnlyPolicy.ActorId,choice:false));
                WorldCommit(s,Tac(s,CommandKind.RespondDefensiveFormation,command.Id,TestOnlyPolicy.CompanionId,choice:false));
                var active=s.Capture().DefensiveFormations.Single();long expiry=active.ExpirySlot;
                while(s.Capture().WorldSchedule.ProcessedSlot<expiry)TacEnd(s);
                var expired=s.Capture();
                Require(expired.WorldSchedule.ProcessedSlot==expiry&&expired.Encounter.CurrentActor==TestOnlyPolicy.ActorId
                    &&expired.DefensiveFormations.Single().Status==DefensiveFormationStatus.Expired,
                    "Defensive Formation did not expire precisely when its owner's next regular turn started.");
                RejectUnchanged(s,host,ActivateFormation(s,new[]{TestOnlyPolicy.ActorId},"formation.second-use"),"DefensiveFormationAlreadyUsed");
            });
            cases.Add("soldier_defensive_formation_skips_unable_recipients_without_removing_protection",()=>{
                var p=DefensiveFormationPolicy(walkingSpeed:0);var s=World(p);AdvanceSoldierToDefensiveFormation(s);BeginEncounter(s);
                WorldCommit(s,Tac(s,CommandKind.SelectCombatStance,stance:(int)CombatStance.Aggressive));
                var command=ActivateFormation(s,new[]{TestOnlyPolicy.ActorId,TestOnlyPolicy.CompanionId},"formation.unable-to-move");
                WorldCommit(s,command);var state=s.Capture();var activation=state.DefensiveFormations.Single();
                Require(activation.Active&&activation.Shifts.All(x=>x.Status==DefensiveFormationShiftStatus.Skipped)
                    &&activation.Shifts.Select(x=>x.RecipientActorId).SequenceEqual(new[]{TestOnlyPolicy.ActorId,TestOnlyPolicy.CompanionId})
                    &&!state.WorldIntervals.Single(x=>x.ActorId==TestOnlyPolicy.ActorId).ActionSpent,
                    "Recipients unable to shift did not skip independently in selection order while keeping the activation active.");
                var adjacent=state.Copy();
                adjacent.Actors=adjacent.Actors.Select(x=>x.Id==TestOnlyPolicy.CompanionId?Moved(x,1,0):x).ToArray();
                adjacent.ShieldStationarity=adjacent.ShieldStationarity.Select(x=>x.ActorId==TestOnlyPolicy.ActorId
                    ?new ShieldStationarityRecord(x.ActorId,x.LastRegularStart,true):x).ToArray();
                Require(CharacterAdvancementRules.ReduceIncomingDamage(adjacent,TestOnlyPolicy.ActorId,10)==9,
                    "Skipping unavailable shifts removed the immediately active Defensive Formation benefit.");
            });
            cases.Add("soldier_defensive_formation_shift_preserves_press_and_resumes_saved_continuation",()=>{
                var p=DefensiveFormationPolicy(SeedForNatural(19));var s=World(p);AdvanceSoldierToDefensiveFormation(s);BeginEncounter(s);
                WorldCommit(s,Tac(s,CommandKind.SelectCombatStance,stance:(int)CombatStance.Aggressive));
                TacStep(s,1,0);TacStep(s,2,0);TacStep(s,3,0);TacEnd(s);TacEnd(s);
                Require(s.Capture().Encounter.CurrentActor==AdditionalTacticalActor.Id,"The three-actor schedule did not reach the hostile actor.");
                WorldCommit(s,Tac(s,CommandKind.AttackUnarmed,TestOnlyPolicy.ActorId,AdditionalTacticalActor.Id));
                Require(s.Capture().MeleeAttacks.Last().Attack.Hit
                    &&TestOnlyClubAttackPolicy.ActivePress(s.Capture(),AdditionalTacticalActor.Id)?.TargetId==TestOnlyPolicy.ActorId,
                    "The hostile setup attack did not establish the Press entitlement against the Soldier.");
                TacEnd(s);
                var activationCommand=ActivateFormation(s,new[]{TestOnlyPolicy.ActorId},"formation.press-continuation");WorldCommit(s,activationCommand);
                WorldCommit(s,Tac(s,CommandKind.RespondDefensiveFormation,activationCommand.Id,TestOnlyPolicy.ActorId,x:2,y:0,choice:true));
                var offered=s.Capture();var activation=offered.DefensiveFormations.Single();var shift=activation.Shifts.Single();
                Require(shift.Status==DefensiveFormationShiftStatus.Moving&&offered.TacticalMoves.Single(x=>x.Id==shift.MoveId).Status==TacticalMoveStatus.Completed
                    &&TestOnlyClubAttackPolicy.CurrentPressOffer(offered)?.ActorId==AdditionalTacticalActor.Id
                    &&offered.MeleeAttacks.Length==1,
                    "Leaving adjacency with a Defensive Formation shift failed to offer the existing Press choice or incorrectly opened an OA.");
                var offeredBytes=Bytes(s);s=new Simulation(p,new SnapshotCodec().Decode(offeredBytes),ExecutionProfile.Laboratory);
                Require(offeredBytes.SequenceEqual(Bytes(s)),"A pending Press continuation from Defensive Formation did not survive save/restore.");
                WorldCommit(s,PressChoice(s,true));var followed=s.Capture();var pressMove=followed.TacticalMoves.Single(x=>x.Kind==TacticalMoveKind.Press);
                Require(pressMove.Status==TacticalMoveStatus.Completed&&pressMove.ParentPressOffer!=""
                    &&Resources(s,AdditionalTacticalActor.Id).PressConsumed,
                    "The eligible Press follow was not preserved or its one-use entitlement was not consumed on acceptance.");
                var followedBytes=Bytes(s);s=new Simulation(p,new SnapshotCodec().Decode(followedBytes),ExecutionProfile.Laboratory);
                Require(followedBytes.SequenceEqual(Bytes(s)),"The accepted Press follow from Defensive Formation did not survive save/restore.");
                var completed=s.Capture();
                Require(completed.DefensiveFormations.Single().Shifts.Single().Status==DefensiveFormationShiftStatus.Moved
                    &&completed.Actors.Single(x=>x.Id==AdditionalTacticalActor.Id).X==3
                    &&completed.Actors.Single(x=>x.Id==TestOnlyPolicy.ActorId).X==2
                    &&TestOnlyClubAttackPolicy.PendingMove(completed)==null,
                    "The accepted Press continuation did not finish before resolving the formation's shift record.");
            });
        }

        private static ActorState Moved(ActorState source,int x,int y)
        {var copy=source.Copy();copy.X=x;copy.Y=y;return copy;}

        private static Snapshot SeparatedFormationTestSnapshot(Snapshot source)
        {
            var copy=source.Copy();
            copy.Actors=copy.Actors.Select(x=>x.Id==TestOnlyPolicy.CompanionId?Moved(x,0,4):x).ToArray();
            return copy;
        }
    }
}
#endif
