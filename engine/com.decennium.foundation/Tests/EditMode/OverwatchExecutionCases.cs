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
        private static TestOnlySharedWorldPolicy OverwatchExecutionPolicy(uint seed=1,OverwatchExecutionFixture execution=null,
            OverwatchDesignationFixture designation=null,PeriodicRiderFixture periodic=null,long enemyHp=26)
        {
            periodic=periodic??new PeriodicRiderFixture(new[]{new PeriodicRiderApplicationFact(
                "ow.fixture.bleed.event","ow.fixture.bleed.rider",TestOnlyPolicy.ActorId,AdditionalTacticalActor.Id,10)});
            return new TestOnlySharedWorldPolicy(execution??new OverwatchExecutionFixture(),designation??new OverwatchDesignationFixture(),
                new OverwatchFoundationFixture(),periodic,new RepeatingCrossbowFixture(),new CharacterAdvancementFixture(),new SharedCombatFixture(enemyHp,seed));
        }

        private static Simulation OverwatchTrigger(TestOnlySharedWorldPolicy policy)
        {
            var s=World(policy);
            WorldCommit(s,new Command("ow.begin",TestOnlyPolicy.ActorId,s.Capture().Revision,CommandKind.BeginFixedEncounter));
            RangedCommit(s,RangedCommand(s,CommandKind.ReloadRepeatingCrossbow,amount:1));
            WorldCommit(s,Tac(s,CommandKind.SelectCombatStance,stance:(int)CombatStance.Aggressive));
            WorldCommit(s,new Command("ow.designate",TestOnlyPolicy.ActorId,s.Capture().Revision,CommandKind.DesignateOverwatch,
                s.Capture().Encounter.CurrentTurnId,x:1,y:-1));
            WorldCommit(s,Tac(s,CommandKind.EndRegularTurn));
            WorldCommit(s,Tac(s,CommandKind.SelectCombatStance,actor:AdditionalTacticalActor.Id,stance:(int)CombatStance.Guarded));
            TacStep(s,3,0);
            return s;
        }

        private static Command OverwatchResponse(Simulation s,bool accept)
        {
            var v=s.Capture();var offer=v.OverwatchOffers.Single(x=>x.Status==OverwatchOfferStatus.Pending);
            return new Command("ow.respond."+(v.Revision+1),offer.OwnerId,v.Revision,CommandKind.RespondOverwatch,offer.Id,
                combat:new CombatRequest(v.Encounter.CurrentTurnId,choice:accept));
        }

        private static Command OverwatchRiderCommand(Simulation s,OverwatchRider rider)
        {
            var v=s.Capture();var choice=v.OverwatchRiderChoices.Single(x=>x.Status==OverwatchRiderChoiceStatus.Pending);
            return new Command("ow.rider."+(v.Revision+1),choice.OwnerId,v.Revision,CommandKind.ResolveOverwatchRider,choice.Id,overwatchRider:rider);
        }

        private static Simulation OverwatchVerticalTrigger(uint seed,OverwatchExecutionFixture execution=null)
        {
            var p=OverwatchExecutionPolicy(seed,execution,new OverwatchDesignationFixture(1,0));var s=World(p);
            WorldCommit(s,new Command("ow.vertical.begin",TestOnlyPolicy.ActorId,s.Capture().Revision,CommandKind.BeginFixedEncounter));
            RangedCommit(s,RangedCommand(s,CommandKind.ReloadRepeatingCrossbow,amount:1));
            WorldCommit(s,Tac(s,CommandKind.SelectCombatStance,stance:(int)CombatStance.Aggressive));
            foreach(var cell in new[]{new[]{0,1},new[]{0,2},new[]{0,3},new[]{0,4},new[]{1,4},new[]{2,4}})TacStep(s,cell[0],cell[1]);
            WorldCommit(s,new Command("ow.vertical.designate",TestOnlyPolicy.ActorId,s.Capture().Revision,CommandKind.DesignateOverwatch,
                s.Capture().Encounter.CurrentTurnId,x:1,y:0));
            WorldCommit(s,Tac(s,CommandKind.EndRegularTurn));
            WorldCommit(s,Tac(s,CommandKind.SelectCombatStance,actor:AdditionalTacticalActor.Id,stance:(int)CombatStance.Guarded));
            foreach(var cell in new[]{new[]{4,1},new[]{4,2},new[]{3,2},new[]{2,2}})TacStep(s,cell[0],cell[1]);
            return s;
        }

        private static Simulation OverwatchCompetingPostStep(bool designateBeforeAttack)
        {
            var s=World(OverwatchExecutionPolicy(SeedForNatural(20),designation:new OverwatchDesignationFixture(0,-1)));
            WorldCommit(s,new Command("ow.order.begin",TestOnlyPolicy.ActorId,s.Capture().Revision,CommandKind.BeginFixedEncounter));
            RangedCommit(s,RangedCommand(s,CommandKind.ReloadRepeatingCrossbow,amount:1));
            WorldCommit(s,Tac(s,CommandKind.SelectCombatStance,stance:(int)CombatStance.Aggressive));
            WorldCommit(s,Tac(s,CommandKind.EndRegularTurn));
            WorldCommit(s,Tac(s,CommandKind.SelectCombatStance,actor:AdditionalTacticalActor.Id,stance:(int)CombatStance.Guarded));
            TacStep(s,3,0);TacStep(s,2,0);TacStep(s,1,0);ConnectedEnd(s);
            WorldCommit(s,Tac(s,CommandKind.SelectCombatStance,stance:(int)CombatStance.Aggressive));
            Action designate=()=>WorldCommit(s,new Command("ow.order.designate",TestOnlyPolicy.ActorId,s.Capture().Revision,
                CommandKind.DesignateOverwatch,s.Capture().Encounter.CurrentTurnId,x:0,y:-1));
            if(designateBeforeAttack)designate();
            WorldCommit(s,Tac(s,CommandKind.AttackUnarmed,AdditionalTacticalActor.Id));
            Require(s.Capture().Presses.Any(x=>x.ActorId==TestOnlyPolicy.ActorId&&x.TargetId==AdditionalTacticalActor.Id),
                "The source attack did not arm the intended Press entitlement.");
            if(!designateBeforeAttack)designate();
            WorldCommit(s,Tac(s,CommandKind.EndRegularTurn));
            WorldCommit(s,Tac(s,CommandKind.SelectCombatStance,actor:AdditionalTacticalActor.Id,stance:(int)CombatStance.Guarded));
            TacStep(s,2,0);AnswerOpportunity(s,false);
            return s;
        }

        private static void AddOverwatchExecutionCases(Dictionary<string,Action> cases,string directory)
        {
            var host=TestOnlySharedWorldPolicy.Host();var codec=new SnapshotCodec();
            cases.Add("overwatch_schema26_completed_entry_persists_response_and_snare_choice",()=>{
                var p=OverwatchExecutionPolicy(SeedForNatural(10));var s=OverwatchTrigger(p);var offered=s.Capture();
                var offer=offered.OverwatchOffers.Single();var zone=offered.OverwatchDesignations.Single();
                Require(offered.SchemaVersion==Snapshot.OverwatchExecutionSchema&&offer.Status==OverwatchOfferStatus.Pending
                    &&offer.MoveId==offered.TacticalMoves.Single(x=>x.Status==TacticalMoveStatus.Completed).Id
                    &&offer.TargetId==AdditionalTacticalActor.Id&&offer.OwnerId==TestOnlyPolicy.ActorId&&zone.Contains(3,0)
                    &&offered.RandomState!=0&&offered.RepeatingCrossbows.Single().LoadedBoltLots.Count==1,
                    "Completed entry into the authored cardinal zone did not create one live Overwatch response.");
                RejectUnchanged(s,host,Tac(s,CommandKind.EndRegularTurn,actor:AdditionalTacticalActor.Id),"OverwatchChoicePending");
                var pendingBytes=Bytes(s);var restored=new Simulation(p,codec.Decode(pendingBytes),ExecutionProfile.Laboratory);
                Require(pendingBytes.SequenceEqual(Bytes(restored)),"Pending Overwatch response did not survive canonical save and receipt replay.");
                WorldCommit(s,OverwatchResponse(s,true));var afterShot=s.Capture();var attack=afterShot.RangedAttacks.Single();
                var choice=afterShot.OverwatchRiderChoices.Single();
                Require(attack.Attack.Hit&&attack.Damage.Dice.Count==1&&attack.Damage.Dice[0]>=1&&attack.Damage.Dice[0]<=8
                    &&attack.Damage.FlatModifier==2&&afterShot.RepeatingCrossbows.Single().LoadedBoltLots.Count==0
                    &&!afterShot.TacticalActors.Single(x=>x.ActorId==TestOnlyPolicy.ActorId).ReactionAvailable
                    &&!afterShot.WorldIntervals.Single(x=>x.ActorId==TestOnlyPolicy.ActorId).ReactionAvailable
                    &&afterShot.OverwatchIntervals.Single().ShotStatus==OverwatchShotStatus.Spent
                    &&choice.Status==OverwatchRiderChoiceStatus.Pending,
                    "Accepted Overwatch did not use the shared Reaction, one loaded bolt, source 1d8+DEX damage and a rider choice.");
                byte[] shotBytes=Bytes(s);restored=new Simulation(p,codec.Decode(shotBytes),ExecutionProfile.Laboratory);
                Require(shotBytes.SequenceEqual(Bytes(restored)),"Unresolved rider selection did not survive canonical save and command replay.");
                WorldCommit(s,OverwatchRiderCommand(s,OverwatchRider.Snare));var snare=s.Capture().OverwatchRiderChoices.Single();
                Require(snare.Status==OverwatchRiderChoiceStatus.Resolved&&snare.Choice==OverwatchRider.Snare
                    &&snare.ExpiresAfterTurnOrdinal==3&&TestOnlyClubAttackPolicy.WalkingSpeed(s.Capture(),AdditionalTacticalActor.Id)==15,
                    "Snare did not apply its source-scoped speed penalty through the next target turn.");
                byte[] snareBytes=Bytes(s);restored=new Simulation(p,codec.Decode(snareBytes),ExecutionProfile.Laboratory);
                Require(snareBytes.SequenceEqual(Bytes(restored)),"Resolved Snare did not survive canonical save and command replay.");
                ConnectedEnd(s);ConnectedEnd(s);var active=s.Capture().OverwatchRiderChoices.Single();
                Require(active.Status==OverwatchRiderChoiceStatus.Resolved&&TestOnlyClubAttackPolicy.WalkingSpeed(s.Capture(),AdditionalTacticalActor.Id)==20,
                    "Snare did not remain through the target's next regular turn.");
                ConnectedEnd(s);var expired=s.Capture();
                Require(!expired.OverwatchRiderChoices.Any(x=>x.Choice==OverwatchRider.Snare&&x.Status==OverwatchRiderChoiceStatus.Resolved)
                    &&TestOnlyClubAttackPolicy.WalkingSpeed(expired,AdditionalTacticalActor.Id)==30,
                    "Snare did not expire by the end of the target's next regular turn.");
            });
            cases.Add("overwatch_decline_forfeits_interval_without_spending_reaction_or_ammunition",()=>{
                var s=OverwatchTrigger(OverwatchExecutionPolicy(SeedForNatural(10)));WorldCommit(s,OverwatchResponse(s,false));var v=s.Capture();
                Require(v.OverwatchOffers.Single().Status==OverwatchOfferStatus.Declined&&v.OverwatchIntervals.Single().ShotStatus==OverwatchShotStatus.Forfeited
                    &&v.TacticalActors.Single(x=>x.ActorId==TestOnlyPolicy.ActorId).ReactionAvailable
                    &&v.WorldIntervals.Single(x=>x.ActorId==TestOnlyPolicy.ActorId).ReactionAvailable
                    &&v.RepeatingCrossbows.Single().LoadedBoltLots.Count==1&&v.RangedAttacks.Length==0&&v.OverwatchRiderChoices.Length==0,
                    "Declining did not forfeit only the Overwatch entitlement while preserving shared Reaction and ammunition.");
            });
            cases.Add("overwatch_miss_spends_reaction_and_bolt_without_opening_rider_choice",()=>{
                var s=OverwatchTrigger(OverwatchExecutionPolicy(SeedForNatural(1)));WorldCommit(s,OverwatchResponse(s,true));var v=s.Capture();
                Require(!v.RangedAttacks.Single().Attack.Hit&&v.OverwatchOffers.Single().Status==OverwatchOfferStatus.Accepted
                    &&v.OverwatchIntervals.Single().ShotStatus==OverwatchShotStatus.Spent&&v.RepeatingCrossbows.Single().LoadedBoltLots.Count==0
                    &&!v.TacticalActors.Single(x=>x.ActorId==TestOnlyPolicy.ActorId).ReactionAvailable&&v.OverwatchRiderChoices.Length==0,
                    "A missed accepted shot refunded its Reaction or bolt, or incorrectly offered a hit rider.");
            });
            cases.Add("overwatch_registered_bleed_choice_uses_shared_periodic_record_and_calendar",()=>{
                var s=OverwatchTrigger(OverwatchExecutionPolicy(SeedForNatural(10)));WorldCommit(s,OverwatchResponse(s,true));
                WorldCommit(s,OverwatchRiderCommand(s,OverwatchRider.Bleed));var v=s.Capture();var rider=v.PeriodicRiders.Single();
                Require(rider.Present&&rider.OwnerId==TestOnlyPolicy.ActorId&&rider.TargetId==AdditionalTacticalActor.Id
                    &&rider.ProfileId==PeriodicRiderFixture.ProfileId&&rider.SourceId==PeriodicRiderFixture.SourceId
                    &&rider.NextStartSlot==3&&rider.RemainingTicks==1
                    &&v.PeriodicRiderEvents.Single(x=>x.Kind==PeriodicRiderEventKind.Applied).At==v.RuleClock
                    &&v.OverwatchRiderChoices.Single().Choice==OverwatchRider.Bleed,
                    "Bleed rider bypassed the registered condition profile or failed to schedule on the target's next shared start.");
                byte[] bytes=Bytes(s);var restored=new Simulation(OverwatchExecutionPolicy(SeedForNatural(10)),codec.Decode(bytes),ExecutionProfile.Laboratory);
                Require(bytes.SequenceEqual(Bytes(restored)),"Applied Overwatch Bleed failed canonical save/replay validation.");
            });
            cases.Add("overwatch_push_uses_recorded_strength_save_and_forced_move",()=>{
                var s=OverwatchTrigger(OverwatchExecutionPolicy(SeedForNatural(10),new OverwatchExecutionFixture(additionalStrengthSaveModifier:-100)));
                WorldCommit(s,OverwatchResponse(s,true));uint before=s.Capture().RandomState;WorldCommit(s,OverwatchRiderCommand(s,OverwatchRider.Push));
                var v=s.Capture();var result=v.OverwatchRiderChoices.Single();var target=v.Actors.Single(x=>x.Id==AdditionalTacticalActor.Id);
                Require(result.Choice==OverwatchRider.Push&&result.SaveNatural>=1&&result.SaveNatural<=20&&!result.SaveSucceeded
                    &&result.SaveDc==10&&result.RandomBefore==before&&result.RandomAfter==v.RandomState&&result.RandomWordsConsumed>0
                    &&result.FromX==3&&result.FromY==0&&result.ToX==4&&result.ToY==0&&result.MovedFeet==5
                    &&target.X==4&&target.Y==0&&v.MeleeAttacks.Length==0,
                    "Push did not record the real Strength save and forced movement without routing through ordinary movement reactions.");
            });
            cases.Add("overwatch_push_success_keeps_target_in_place_and_records_save",()=>{
                var s=OverwatchTrigger(OverwatchExecutionPolicy(SeedForNatural(10),new OverwatchExecutionFixture(additionalStrengthSaveModifier:100)));
                WorldCommit(s,OverwatchResponse(s,true));uint before=s.Capture().RandomState;WorldCommit(s,OverwatchRiderCommand(s,OverwatchRider.Push));
                var v=s.Capture();var result=v.OverwatchRiderChoices.Single();var target=v.Actors.Single(x=>x.Id==AdditionalTacticalActor.Id);
                Require(result.SaveSucceeded&&result.SaveNatural>=1&&result.SaveNatural<=20&&result.SaveDc==10&&result.SaveModifier==100
                    &&result.RandomBefore==before&&result.RandomAfter==v.RandomState&&result.RandomWordsConsumed>0
                    &&result.FromX==3&&result.FromY==0&&result.ToX==3&&result.ToY==0&&result.MovedFeet==0&&target.X==3&&target.Y==0,
                    "A successful Push Strength save did not preserve position and its complete deterministic audit.");
            });
            cases.Add("overwatch_push_failure_stops_at_blocked_cell_without_collision_or_refund",()=>{
                var s=OverwatchVerticalTrigger(SeedForNatural(10),new OverwatchExecutionFixture(additionalStrengthSaveModifier:-100));
                var offer=s.Capture().OverwatchOffers.Single(x=>x.Status==OverwatchOfferStatus.Pending);
                Require(s.Capture().Actors.Single(x=>x.Id==TestOnlyPolicy.ActorId).X==2&&s.Capture().Actors.Single(x=>x.Id==TestOnlyPolicy.ActorId).Y==4
                    &&s.Capture().Actors.Single(x=>x.Id==AdditionalTacticalActor.Id).X==2&&s.Capture().Actors.Single(x=>x.Id==AdditionalTacticalActor.Id).Y==2
                    &&offer.TargetId==AdditionalTacticalActor.Id,"The vertical cardinal firing lane did not offer its intended target.");
                WorldCommit(s,OverwatchResponse(s,true));WorldCommit(s,OverwatchRiderCommand(s,OverwatchRider.Push));var v=s.Capture();
                var result=v.OverwatchRiderChoices.Single();var target=v.Actors.Single(x=>x.Id==AdditionalTacticalActor.Id);
                Require(!result.SaveSucceeded&&result.MovedFeet==0&&result.FromX==2&&result.FromY==2&&result.ToX==2&&result.ToY==2
                    &&target.X==2&&target.Y==2&&v.Lives.Single(x=>x.ActorId==AdditionalTacticalActor.Id).Hp<26,
                    "A failed Push stopped on the blocked cell but applied collision damage, refunded the shot, or changed location.");
            });
            cases.Add("overwatch_and_press_mixed_occurrences_follow_source_application_order",()=>{
                var pressFirst=OverwatchCompetingPostStep(false);var pressOffer=TestOnlyClubAttackPolicy.CurrentPressOffer(pressFirst.Capture());
                var overwatchOffer=pressFirst.Capture().OverwatchOffers.Single(x=>x.Status==OverwatchOfferStatus.Pending);
                Require(pressOffer!=null&&pressOffer.CreatedRevision==overwatchOffer.CreatedRevision
                    &&pressOffer.ArmedRevision<overwatchOffer.SourceAppliedRevision,
                    "Earlier Press application did not take precedence over the later same-checkpoint Overwatch application.");
                RejectUnchanged(pressFirst,host,OverwatchResponse(pressFirst,true),"EarlierPostStepChoicePending");
                WorldCommit(pressFirst,PressChoice(pressFirst,true));
                Require(pressFirst.Capture().Actors.Single(x=>x.Id==TestOnlyPolicy.ActorId).X==0
                    &&pressFirst.Capture().TacticalActors.Single(x=>x.ActorId==TestOnlyPolicy.ActorId).PressConsumed,
                    "Accepted earlier Press moved before the higher-order pending checkpoint was resolved.");
                WorldCommit(pressFirst,OverwatchResponse(pressFirst,false));
                Require(pressFirst.Capture().Actors.Single(x=>x.Id==TestOnlyPolicy.ActorId).X==1
                    &&pressFirst.Capture().TacticalMoves.Last().Kind==TacticalMoveKind.Press,
                    "The deferred accepted Press did not follow after the later Overwatch occurrence resolved.");

                var overwatchFirst=OverwatchCompetingPostStep(true);pressOffer=TestOnlyClubAttackPolicy.CurrentPressOffer(overwatchFirst.Capture());
                overwatchOffer=overwatchFirst.Capture().OverwatchOffers.Single(x=>x.Status==OverwatchOfferStatus.Pending);
                Require(pressOffer!=null&&pressOffer.CreatedRevision==overwatchOffer.CreatedRevision
                    &&pressOffer.ArmedRevision>overwatchOffer.SourceAppliedRevision,
                    "Earlier Overwatch application did not take precedence over the later same-checkpoint Press application.");
                RejectUnchanged(overwatchFirst,host,PressChoice(overwatchFirst,true),"OverwatchChoicePending");
                WorldCommit(overwatchFirst,OverwatchResponse(overwatchFirst,false));
                WorldCommit(overwatchFirst,PressChoice(overwatchFirst,true));
                Require(overwatchFirst.Capture().Actors.Single(x=>x.Id==TestOnlyPolicy.ActorId).X==1
                    &&overwatchFirst.Capture().TacticalActors.Single(x=>x.ActorId==TestOnlyPolicy.ActorId).PressConsumed,
                    "Resolving the earlier Overwatch occurrence failed to unblock the later Press follow.");
            });
            cases.Add("overwatch_accepted_opportunity_attack_invalidates_without_refiring_or_duplicate_trigger",()=>{
                var s=World(OverwatchExecutionPolicy(SeedForNatural(20),designation:new OverwatchDesignationFixture(0,-1)));
                WorldCommit(s,new Command("ow.oa.begin",TestOnlyPolicy.ActorId,s.Capture().Revision,CommandKind.BeginFixedEncounter));
                RangedCommit(s,RangedCommand(s,CommandKind.ReloadRepeatingCrossbow,amount:1));
                WorldCommit(s,Tac(s,CommandKind.SelectCombatStance,stance:(int)CombatStance.Aggressive));WorldCommit(s,Tac(s,CommandKind.EndRegularTurn));
                WorldCommit(s,Tac(s,CommandKind.SelectCombatStance,actor:AdditionalTacticalActor.Id,stance:(int)CombatStance.Guarded));
                TacStep(s,3,0);TacStep(s,2,0);TacStep(s,1,0);ConnectedEnd(s);
                WorldCommit(s,Tac(s,CommandKind.SelectCombatStance,stance:(int)CombatStance.Aggressive));
                WorldCommit(s,new Command("ow.oa.designate",TestOnlyPolicy.ActorId,s.Capture().Revision,CommandKind.DesignateOverwatch,
                    s.Capture().Encounter.CurrentTurnId,x:0,y:-1));WorldCommit(s,Tac(s,CommandKind.EndRegularTurn));
                WorldCommit(s,Tac(s,CommandKind.SelectCombatStance,actor:AdditionalTacticalActor.Id,stance:(int)CombatStance.Guarded));TacStep(s,2,0);
                Require(TestOnlyClubAttackPolicy.PendingMove(s.Capture())!=null,"Departure did not wait for the pre-movement OA response.");
                AnswerOpportunity(s,true);var v=s.Capture();
                Require(v.TacticalMoves.Last().Status==TacticalMoveStatus.Completed&&v.Actors.Single(x=>x.Id==AdditionalTacticalActor.Id).X==2
                    &&v.OverwatchOffers.Single().Status==OverwatchOfferStatus.Invalidated&&v.RangedAttacks.Length==0
                    &&v.RepeatingCrossbows.Single().LoadedBoltLots.Count==1
                    &&!v.TacticalActors.Single(x=>x.ActorId==TestOnlyPolicy.ActorId).ReactionAvailable,
                    "Accepted pre-departure OA did not spend the shared Reaction and permanently invalidate the later Overwatch occurrence.");
            });
            cases.Add("overwatch_prevented_departure_has_no_post_step_offer_or_movement_cost",()=>{
                var s=World(OverwatchExecutionPolicy(SeedForNatural(20),designation:new OverwatchDesignationFixture(0,-1),enemyHp:1));
                WorldCommit(s,new Command("ow.prevent.begin",TestOnlyPolicy.ActorId,s.Capture().Revision,CommandKind.BeginFixedEncounter));
                RangedCommit(s,RangedCommand(s,CommandKind.ReloadRepeatingCrossbow,amount:1));
                WorldCommit(s,Tac(s,CommandKind.SelectCombatStance,stance:(int)CombatStance.Aggressive));WorldCommit(s,Tac(s,CommandKind.EndRegularTurn));
                WorldCommit(s,Tac(s,CommandKind.SelectCombatStance,actor:AdditionalTacticalActor.Id,stance:(int)CombatStance.Guarded));
                TacStep(s,3,0);TacStep(s,2,0);TacStep(s,1,0);ConnectedEnd(s);
                WorldCommit(s,Tac(s,CommandKind.SelectCombatStance,stance:(int)CombatStance.Aggressive));
                WorldCommit(s,new Command("ow.prevent.designate",TestOnlyPolicy.ActorId,s.Capture().Revision,CommandKind.DesignateOverwatch,
                    s.Capture().Encounter.CurrentTurnId,x:0,y:-1));WorldCommit(s,Tac(s,CommandKind.EndRegularTurn));
                WorldCommit(s,Tac(s,CommandKind.SelectCombatStance,actor:AdditionalTacticalActor.Id,stance:(int)CombatStance.Guarded));TacStep(s,2,0);
                AnswerOpportunity(s,true);var v=s.Capture();var move=v.TacticalMoves.Last();
                Require(move.Status==TacticalMoveStatus.Interrupted&&move.CostPaid==0&&v.Actors.Single(x=>x.Id==AdditionalTacticalActor.Id).X==1
                    &&v.ActorMovement.Single(x=>x.ActorId==AdditionalTacticalActor.Id).Spent==0&&v.OverwatchOffers.Length==0
                    &&v.OverwatchIntervals.Where(x=>x.ActorId==TestOnlyPolicy.ActorId).OrderByDescending(x=>x.LastRegularStart).First().ShotStatus==OverwatchShotStatus.Available
                    &&v.RepeatingCrossbows.Single().LoadedBoltLots.Count==1,
                    "A step prevented by its pre-departure OA emitted Overwatch or charged movement, ammunition, or entitlement.");
            });
            cases.Add("overwatch_rejects_unconnected_attack_and_hidden_trigger_facts",()=>{
                var p=OverwatchExecutionPolicy(SeedForNatural(10),designation:new OverwatchDesignationFixture(0,-1));var s=World(p);
                WorldCommit(s,new Command("ow.attack-zone.begin",TestOnlyPolicy.ActorId,s.Capture().Revision,CommandKind.BeginFixedEncounter));
                WorldCommit(s,Tac(s,CommandKind.SelectCombatStance,stance:(int)CombatStance.Aggressive));WorldCommit(s,Tac(s,CommandKind.EndRegularTurn));
                WorldCommit(s,Tac(s,CommandKind.SelectCombatStance,actor:AdditionalTacticalActor.Id,stance:(int)CombatStance.Guarded));
                TacStep(s,3,0);TacStep(s,2,0);TacStep(s,1,0);ConnectedEnd(s);
                WorldCommit(s,Tac(s,CommandKind.SelectCombatStance,stance:(int)CombatStance.Aggressive));
                WorldCommit(s,new Command("ow.attack-zone.designate",TestOnlyPolicy.ActorId,s.Capture().Revision,CommandKind.DesignateOverwatch,
                    s.Capture().Encounter.CurrentTurnId,x:0,y:-1));WorldCommit(s,Tac(s,CommandKind.EndRegularTurn));
                WorldCommit(s,Tac(s,CommandKind.SelectCombatStance,actor:AdditionalTacticalActor.Id,stance:(int)CombatStance.Guarded));
                // The attack-from-zone rule is intentionally held closed until its trigger can be resolved.
                RejectUnchanged(s,host,Tac(s,CommandKind.AttackUnarmed,TestOnlyPolicy.ActorId,actor:AdditionalTacticalActor.Id),"OverwatchAttackTriggerNotImplemented");
                var hidden=OverwatchTrigger(OverwatchExecutionPolicy(SeedForNatural(10),new OverwatchExecutionFixture(targetVisible:false)));
                Require(hidden.Capture().OverwatchOffers.Length==0,"An explicit hidden-target fixture generated a controller response.");
            });
        }
    }
}
#endif
