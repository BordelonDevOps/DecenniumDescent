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
        private static TestOnlyClubAttackPolicy TacticalPolicy(uint seed=1,long actorHp=26,long companionHp=26,int actorSpeed=30,int companionSpeed=30,
            AdditionalTacticalActor third=null,TacticalTerrainCell[] terrain=null,bool actorProne=false)
            =>new TestOnlyClubAttackPolicy(seed:seed,actorHp:actorHp,companionHp:companionHp,actorBaseWalkingSpeed:actorSpeed,companionBaseWalkingSpeed:companionSpeed,
                actorProne:actorProne,tactical:new TacticalCombatFixture(third,terrain));
        private static Simulation Tactical(TestOnlyClubAttackPolicy p=null,CombatStance stance=CombatStance.Aggressive)
        {var s=Clubs(p??TacticalPolicy());BeginEncounter(s);Stance(s,stance);return s;}
        private static Command Tac(Simulation s,CommandKind kind,string target=null,string actor=null,int x=0,int y=0,string weapon="",bool choice=false,
            AttackKnockoutMode knockout=AttackKnockoutMode.OrdinaryOutcome,int stance=0,PressHitInstruction press=PressHitInstruction.ArmOrReplace)
        {
            var v=s.Capture();actor=actor??v.Encounter.CurrentActor;
            bool combat=kind==CommandKind.AttackUnarmed||kind==CommandKind.AttackClub||kind==CommandKind.SelectCombatStance||kind==CommandKind.ResolveKnockout
                ||kind==CommandKind.RespondOpportunityAttack||kind==CommandKind.RespondPress||kind==CommandKind.RespondDefensiveFormation;
            if(target==null)target=combat?"":v.Encounter.CurrentTurnId;
            return new Command("tactical.command."+(v.Revision+1),actor,v.Revision,kind,target,x,y,
                combat:combat?new CombatRequest(v.Encounter.CurrentTurnId,weapon,stance,knockout,choice,press):null);
        }
        private static void CommitTac(Simulation s,Command c)
        {var r=s.Execute(TacticalCombatFixture.Host(),c);Require(r.Outcome==Outcome.Committed,c.Kind+" expected commit: "+r.Code);}
        private static void TacStep(Simulation s,int x,int y)=>CommitTac(s,Tac(s,CommandKind.TacticalStep,x:x,y:y));
        private static void TacEnd(Simulation s,CombatStance stance=CombatStance.Aggressive)
        {CommitTac(s,Tac(s,CommandKind.EndRegularTurn));CommitTac(s,Tac(s,CommandKind.SelectCombatStance,stance:(int)stance));}
        private static Command Opportunity(Simulation s,bool accept,string weapon=CombatProfileIds.OrdinaryUnarmed,AttackKnockoutMode knockout=AttackKnockoutMode.OrdinaryOutcome,PressHitInstruction press=PressHitInstruction.ArmOrReplace)
        {var m=TestOnlyClubAttackPolicy.PendingMove(s.Capture());return Tac(s,CommandKind.RespondOpportunityAttack,m.Id,m.Reactors[m.ResponseIndex],weapon:accept?weapon:"",choice:accept,knockout:knockout,press:press);}
        private static void AnswerOpportunity(Simulation s,bool accept,string weapon=CombatProfileIds.OrdinaryUnarmed,AttackKnockoutMode knockout=AttackKnockoutMode.OrdinaryOutcome)
            =>CommitTac(s,Opportunity(s,accept,weapon,knockout));
        private static Command PressChoice(Simulation s,bool accept)
        {var offer=TestOnlyClubAttackPolicy.CurrentPressOffer(s.Capture());return Tac(s,CommandKind.RespondPress,offer.Id,offer.ActorId,choice:accept);}
        private static ActorTacticalRecord Resources(Simulation s,string actor=TestOnlyPolicy.ActorId)=>s.Capture().TacticalActors.Single(a=>a.ActorId==actor);
        private static ActorState Body(Simulation s,string actor=TestOnlyPolicy.ActorId)=>s.Capture().Actors.Single(a=>a.Id==actor);
        private static void AddTacticalMovementCases(Dictionary<string,Action> cases,string directory)
        {
            var host=TacticalCombatFixture.Host();var codec=new SnapshotCodec();
            cases.Add("tactical_schema11_requires_explicit_speeds_and_retains_old_profiles",()=>{
                var p=TacticalPolicy(third:new AdditionalTacticalActor(1,1,25));var s=Tactical(p);var v=s.Capture();
                Require(v.SchemaVersion==11&&v.Actors.Length==3&&v.Encounter.Order.SequenceEqual(new[]{TestOnlyPolicy.ActorId,TestOnlyPolicy.CompanionId,AdditionalTacticalActor.Id})
                    &&v.TacticalActors.All(a=>a.ReactionAvailable)&&Resources(s,AdditionalTacticalActor.Id).LastRegularStart==-1,"Explicit third actor/initial Reaction facts wrong.");
                Require(Bytes(s).SequenceEqual(Bytes(RestoreClub(s,p))),"Schema11 initial history failed roundtrip.");
                Throws<ArgumentException>(()=>new TestOnlyClubAttackPolicy(tactical:new TacticalCombatFixture()));
                Throws<ArgumentException>(()=>TacticalPolicy(third:new AdditionalTacticalActor(0,0,30)));
                Throws<ArgumentException>(()=>new TestOnlyEncounterPolicy(AdditionalTacticalActor.Id));
                Require(PosturePolicy().Initial().SchemaVersion==10&&new TestOnlyClubAttackPolicy().Initial().SchemaVersion==9,"Legacy selected new schema.");
            });
            cases.Add("tactical_unarmed_formula_and_body_contract_have_no_hand_requirement",()=>{
                Require(PrototypeUnarmed.Damage(10)==1&&PrototypeUnarmed.Damage(10,2)==3&&PrototypeUnarmed.Damage(8)==0&&PrototypeUnarmed.Damage(1,2)==0,"Ordinary unarmed formula wrong.");
                foreach(var part in new[]{OrdinaryStrikingParts.Fist,OrdinaryStrikingParts.Elbow,OrdinaryStrikingParts.Knee,OrdinaryStrikingParts.Foot,OrdinaryStrikingParts.Head})Require(PrototypeUnarmed.CanStrike(part),"Usable nonhand part denied.");
                Require(!PrototypeUnarmed.CanStrike(OrdinaryStrikingParts.None)&&PrototypeUnarmed.Damage(int.MaxValue,long.MinValue)==0,"Body absence or widened damage floor wrong.");
                Throws<ArgumentException>(()=>PrototypeUnarmed.CanStrike((OrdinaryStrikingParts)32));Throws<OverflowException>(()=>PrototypeUnarmed.Damage(20,long.MaxValue));
            });
            cases.Add("tactical_unarmed_critical_keeps_flat_damage_and_no_damage_draw",()=>{
                var s=Tactical(TacticalPolicy(SeedForDeath(20)));var before=s.Capture().RandomState;
                CommitTac(s,Tac(s,CommandKind.AttackUnarmed,TestOnlyPolicy.CompanionId));var a=s.Capture().MeleeAttacks.Single();
                Require(a.Attack.Critical&&a.Attack.Modifier==0&&a.WeaponId==CombatProfileIds.OrdinaryUnarmed&&a.Damage.Total==3&&a.Damage.Dice.Count==0&&a.Damage.DiceWords==0
                    &&s.Capture().RandomState==PlaytestDice.RollD20(before).NextRandomState&&!a.Opportunity&&TestOnlyClubAttackPolicy.ActionSpent(s.Capture()),"Unarmed critical rolled/doubled flat damage or borrowed proficiency.");
            });
            cases.Add("tactical_unarmed_without_aggressive_deals_one_and_preserves_held_club",()=>{
                var s=Tactical(TacticalPolicy(SeedForDeath(16)),CombatStance.Guarded);CommitTac(s,Tac(s,CommandKind.AttackUnarmed,TestOnlyPolicy.CompanionId));
                Require(s.Capture().MeleeAttacks.Single().Damage.Total==1&&Life(s).HeldItems.Single()==TestOnlyClubAttackPolicy.ActorClub,"Unarmed gained weapon property or required empty hand.");
                RejectUnchanged(s,host,Tac(s,CommandKind.AttackUnarmed,TestOnlyPolicy.CompanionId),"ActionAlreadySpent");
            });
            cases.Add("tactical_unarmed_pending_knockout_roundtrips_without_reroll",()=>{
                var p=TacticalPolicy(SeedForDeath(16),companionHp:1);var s=Tactical(p);CommitTac(s,Tac(s,CommandKind.AttackUnarmed,TestOnlyPolicy.CompanionId,knockout:AttackKnockoutMode.AskIfEligible));
                var a=s.Capture().MeleeAttacks.Single();Require(a.Pending&&a.Damage.Dice.Count==0,"Unarmed knockout continuation absent.");
                s=RestoreClub(s,p);CommitTac(s,Tac(s,CommandKind.ResolveKnockout,a.Id,choice:true));
                Require(Life(s,TestOnlyPolicy.CompanionId).Stable&&s.Capture().MeleeAttacks.Single().Attack.RandomBefore==a.Attack.RandomBefore,"Choice rerolled unarmed attack.");
            });
            cases.Add("tactical_ordinary_step_spends_cost_without_action_time_or_dice",()=>{
                var s=Tactical();var before=s.Capture();TacStep(s,0,1);var v=s.Capture();
                Require(Body(s).X==0&&Body(s).Y==1&&v.ActorMovement.Single(m=>m.ActorId==TestOnlyPolicy.ActorId).Spent==5&&v.RuleClock==before.RuleClock&&v.RandomState==before.RandomState
                    &&!TestOnlyClubAttackPolicy.ActionSpent(v)&&v.TacticalMoves.Single().Status==TacticalMoveStatus.Completed,"Step spent Action/time/RNG or omitted cost.");
                Require(v.Clubs.Single(w=>w.HeldBy==TestOnlyPolicy.ActorId).CellY==1,"Held equipment location did not follow body.");
            });
            cases.Add("tactical_destination_terrain_and_crawl_costs_use_shared_ledger",()=>{
                var s=Tactical(TacticalPolicy(actorProne:true,terrain:new[]{new TacticalTerrainCell(0,1,TerrainCost.Difficult)}));TacStep(s,0,1);
                Require(TestOnlyClubAttackPolicy.WalkingLedger(s.Capture()).Spent==15&&Life(s).Prone,"Crawl+difficult did not cost3 per foot or silently stood.");
                s=Tactical(TacticalPolicy(terrain:new[]{new TacticalTerrainCell(0,1,TerrainCost.Severe)}));TacStep(s,0,1);Require(TestOnlyClubAttackPolicy.WalkingLedger(s.Capture()).Spent==15,"Severe terrain cost wrong.");
            });
            cases.Add("tactical_invalid_and_occupied_steps_reject_before_reactions",()=>{
                var s=Tactical();foreach(var cell in new[]{new CombatCell(0,0),new CombatCell(0,2)})RejectUnchanged(s,host,Tac(s,CommandKind.TacticalStep,x:cell.X,y:cell.Y),"InvalidTacticalStep");
                RejectUnchanged(s,host,Tac(s,CommandKind.TacticalStep,x:1,y:0),"OccupiedTacticalStep");
                RejectUnchanged(s,host,Tac(s,CommandKind.TacticalStep,x:-1,y:0),"BlockedTacticalStep");
                s=Tactical(TacticalPolicy(actorSpeed:0));RejectUnchanged(s,host,Tac(s,CommandKind.TacticalStep,x:0,y:1),"ZeroSpeedCannotMove");
                s=Tactical(TacticalPolicy(actorSpeed:4));RejectUnchanged(s,host,Tac(s,CommandKind.TacticalStep,x:0,y:1),"InsufficientMovement");
            });
            cases.Add("tactical_departure_captures_offer_before_motion_and_freezes_other_commands",()=>{
                var s=Tactical();TacStep(s,0,1);TacStep(s,0,2);var m=TestOnlyClubAttackPolicy.PendingMove(s.Capture());
                Require(m!=null&&m.Reactors.SequenceEqual(new[]{TestOnlyPolicy.CompanionId})&&Body(s).Y==1&&TestOnlyClubAttackPolicy.WalkingLedger(s.Capture()).Spent==5,"Announced step moved or paid early.");
                RejectUnchanged(s,host,Tac(s,CommandKind.EndRegularTurn),"OpportunityChoicePending");
                RejectUnchanged(s,host,Tac(s,CommandKind.TacticalStep,x:1,y:2),"OpportunityChoicePending");
                RejectUnchanged(s,host,Tac(s,CommandKind.DropProne),"OpportunityChoicePending");
            });
            cases.Add("tactical_declining_oa_preserves_reaction_and_finishes_fixed_step",()=>{
                var s=Tactical();TacStep(s,0,1);TacStep(s,0,2);uint rng=s.Capture().RandomState;AnswerOpportunity(s,false);
                Require(Resources(s,TestOnlyPolicy.CompanionId).ReactionAvailable&&Body(s).Y==2&&TestOnlyClubAttackPolicy.WalkingLedger(s.Capture()).Spent==10&&s.Capture().RandomState==rng,"Decline spent Reaction/dice or cancelled fixed step.");
            });
            cases.Add("tactical_accepted_oa_spends_reaction_not_action_and_uses_preexit_position",()=>{
                var s=Tactical(TacticalPolicy(SeedForDeath(16)));TacStep(s,0,1);TacStep(s,0,2);AnswerOpportunity(s,true);
                var a=s.Capture().MeleeAttacks.Single();Require(a.Opportunity&&a.AttackerId==TestOnlyPolicy.CompanionId&&a.TargetId==TestOnlyPolicy.ActorId&&a.Attack.Hit&&a.Damage.Total==1
                    &&!Resources(s,TestOnlyPolicy.CompanionId).ReactionAvailable&&!TestOnlyClubAttackPolicy.ActionSpent(s.Capture())&&Body(s).Y==2&&s.Capture().Presses.Length==0,"Offturn OA paid Action, used post-exit range or armed Press.");
                CommitTac(s,Tac(s,CommandKind.EncounterDash));
            });
            cases.Add("tactical_oa_miss_still_spends_reaction_and_commits_departure",()=>{
                var s=Tactical(TacticalPolicy(SeedForDeath(1)));TacStep(s,0,1);TacStep(s,0,2);AnswerOpportunity(s,true,TestOnlyClubAttackPolicy.CompanionClub);
                var a=s.Capture().MeleeAttacks.Single();Require(!a.Attack.Hit&&!Resources(s,TestOnlyPolicy.CompanionId).ReactionAvailable&&a.Damage.Dice.Count==0&&Body(s).Y==2,"Miss refunded Reaction or stopped legal step.");
            });
            cases.Add("tactical_controller_and_inventory_authority_precede_duplicate_lookup",()=>{
                var s=Tactical();TacStep(s,0,1);TacStep(s,0,2);var request=Opportunity(s,true,TestOnlyClubAttackPolicy.CompanionClub);
                RejectUnchanged(s,new Authority("TEST_ONLY.other",new[]{TestOnlyPolicy.ActorId}),request,"NotAuthorized");
                var noEquipment=new Authority("TEST_ONLY.host",new[]{TestOnlyPolicy.CompanionId});RejectUnchanged(s,noEquipment,request,"InventoryNotAuthorized");
                var wrong=Tac(s,CommandKind.RespondOpportunityAttack,request.Target,TestOnlyPolicy.ActorId,weapon:CombatProfileIds.OrdinaryUnarmed,choice:true);RejectUnchanged(s,host,wrong,"WrongReactionController");
                CommitTac(s,request);byte[] saved=Bytes(s);Require(s.Execute(host,request).Outcome==Outcome.Duplicate&&Bytes(s).SequenceEqual(saved),"Duplicate OA repeated effect.");
                RejectUnchanged(s,noEquipment,request,"InventoryNotAuthorized");
            });
            cases.Add("tactical_oa_knockout_choice_belongs_to_reactor_and_stops_without_cost",()=>{
                var p=TacticalPolicy(SeedForDeath(16),actorHp:1);var s=Tactical(p);TacStep(s,0,1);TacStep(s,0,2);AnswerOpportunity(s,true,knockout:AttackKnockoutMode.AskIfEligible);
                var a=s.Capture().MeleeAttacks.Single();Require(a.Pending&&a.Opportunity&&Body(s).Y==1&&Life(s).Hp==1,"Pending OA prematurely moved/applied life.");
                s=RestoreClub(s,p);RejectUnchanged(s,host,Tac(s,CommandKind.ResolveKnockout,a.Id,TestOnlyPolicy.ActorId,choice:true),"InvalidKnockoutChoice");
                var command=Tac(s,CommandKind.ResolveKnockout,a.Id,TestOnlyPolicy.CompanionId,choice:true);
                CommitTac(s,command);Require(Life(s).Stable&&Life(s).Prone&&Life(s).HeldItems.Count==0&&Body(s).Y==1&&TestOnlyClubAttackPolicy.WalkingLedger(s.Capture()).Spent==5
                    &&s.Capture().TacticalMoves.Last().Status==TacticalMoveStatus.Interrupted&&!Resources(s,TestOnlyPolicy.CompanionId).ReactionAvailable,"Stopped movement refunded paid attack or charged untraveled step.");
                Require(s.Capture().Clubs.Single(w=>w.Id==TestOnlyClubAttackPolicy.ActorClub).CellY==1,"Knockout dropped Club at untraveled destination.");
            });
            cases.Add("tactical_multi_reactor_capture_uses_initiative_and_survives_reload",()=>{
                var p=TacticalPolicy(third:new AdditionalTacticalActor(1,1,30));var s=Tactical(p);TacStep(s,0,1);TacStep(s,0,2);
                // Third remains adjacent at the destination and therefore is not eligible for this step.
                Require(TestOnlyClubAttackPolicy.PendingMove(s.Capture()).Reactors.SequenceEqual(new[]{TestOnlyPolicy.CompanionId}),"Within-reach third actor received OA.");
                AnswerOpportunity(s,false);TacStep(s,0,3);Require(TestOnlyClubAttackPolicy.PendingMove(s.Capture()).Reactors.SequenceEqual(new[]{AdditionalTacticalActor.Id}),"Third actor's later departure omitted.");
                s=RestoreClub(s,p);AnswerOpportunity(s,false);Require(Body(s).Y==3,"Third-controller continuation lost on reload.");
            });
            cases.Add("tactical_two_simultaneous_oa_offers_resolve_in_initiative_order",()=>{
                var p=TacticalPolicy(third:new AdditionalTacticalActor(0,1,30));var s=Tactical(p);TacStep(s,1,1);TacStep(s,2,2);
                var m=TestOnlyClubAttackPolicy.PendingMove(s.Capture());Require(m.Reactors.SequenceEqual(new[]{TestOnlyPolicy.CompanionId,AdditionalTacticalActor.Id}),"Captured offers were not in initiative order.");
                RejectUnchanged(s,host,Tac(s,CommandKind.RespondOpportunityAttack,m.Id,AdditionalTacticalActor.Id),"WrongReactionController");
                AnswerOpportunity(s,false);Require(TestOnlyClubAttackPolicy.PendingMove(s.Capture()).ResponseIndex==1&&Body(s).X==1,"First decline completed movement before second offer.");
                s=RestoreClub(s,p);AnswerOpportunity(s,false);Require(Body(s).X==2&&Body(s).Y==2&&Resources(s,TestOnlyPolicy.CompanionId).ReactionAvailable&&Resources(s,AdditionalTacticalActor.Id).ReactionAvailable,"Second decline lost preserved resources or destination.");
            });
            cases.Add("tactical_first_oa_stop_discards_later_offers_without_spending_them",()=>{
                var p=TacticalPolicy(SeedForDeath(16),actorHp:1,third:new AdditionalTacticalActor(0,1,30));var s=Tactical(p);TacStep(s,1,1);TacStep(s,2,2);
                AnswerOpportunity(s,true,knockout:AttackKnockoutMode.KnockOutIfEligible);
                Require(Life(s).Stable&&Body(s).X==1&&Body(s).Y==1&&TestOnlyClubAttackPolicy.PendingMove(s.Capture())==null
                    &&!Resources(s,TestOnlyPolicy.CompanionId).ReactionAvailable&&Resources(s,AdditionalTacticalActor.Id).ReactionAvailable
                    &&s.Capture().TacticalMoves.Last().ResponseIndex==1&&s.Capture().TacticalMoves.Last().Status==TacticalMoveStatus.Interrupted,"Stopped departure spent another creature's Reaction or moved.");
                s=RestoreClub(s,p);
            });
            cases.Add("tactical_reaction_refreshes_at_own_start_not_round_boundary",()=>{
                var s=Tactical(TacticalPolicy(SeedForDeath(1)));TacStep(s,0,1);TacStep(s,0,2);AnswerOpportunity(s,true);
                Require(!Resources(s,TestOnlyPolicy.CompanionId).ReactionAvailable&&Resources(s,TestOnlyPolicy.CompanionId).LastRegularStart==-1,"Pre-first-turn resource not spent.");
                TacEnd(s);Require(Resources(s,TestOnlyPolicy.CompanionId).ReactionAvailable&&Resources(s,TestOnlyPolicy.CompanionId).LastRegularStart==1,"First own Start did not refresh Reaction.");
            });
            cases.Add("tactical_numbered_round_wrap_does_not_refresh_other_actor_reaction",()=>{
                var s=Tactical(TacticalPolicy(SeedForDeath(16),third:new AdditionalTacticalActor(0,1,30)));TacEnd(s);TacEnd(s);TacStep(s,0,2);
                AnswerOpportunity(s,false);AnswerOpportunity(s,true);Require(!Resources(s,TestOnlyPolicy.CompanionId).ReactionAvailable,"Third actor's departure failed to spend companion Reaction.");
                TacEnd(s);Require(s.Capture().Encounter.Round==2&&!Resources(s,TestOnlyPolicy.CompanionId).ReactionAvailable,"Round wrap refreshed another creature's Reaction.");
                TacEnd(s);Require(Resources(s,TestOnlyPolicy.CompanionId).ReactionAvailable,"Next own Start failed to refresh Reaction.");
            });
            cases.Add("tactical_recovered_actor_without_held_club_still_receives_unarmed_oa",()=>{
                var p=TacticalPolicy(TacticalSeed(16,20,20,16),companionHp:1);var s=Tactical(p);
                CommitTac(s,Tac(s,CommandKind.AttackUnarmed,TestOnlyPolicy.CompanionId));TacEnd(s);
                Require(Life(s,TestOnlyPolicy.CompanionId).Hp==1&&Life(s,TestOnlyPolicy.CompanionId).Prone&&Life(s,TestOnlyPolicy.CompanionId).HeldItems.Count==0,"Natural20 recovery fixture did not retain dropped equipment/posture.");
                CommitTac(s,Tac(s,CommandKind.StandFromProne));TacEnd(s);TacStep(s,0,1);TacStep(s,0,2);
                RejectUnchanged(s,host,Opportunity(s,true,TestOnlyClubAttackPolicy.CompanionClub),"ClubNotHeld");
                Require(Resources(s,TestOnlyPolicy.CompanionId).ReactionAvailable,"Invalid weapon spent Reaction.");AnswerOpportunity(s,true);
                Require(s.Capture().MeleeAttacks.Last().WeaponId==CombatProfileIds.OrdinaryUnarmed&&s.Capture().MeleeAttacks.Last().Attack.Hit,"Dropped Club suppressed legal unarmed OA.");
            });
            cases.Add("tactical_focused_immediately_prohibits_oa_without_spending_resource",()=>{
                var s=Tactical(stance:CombatStance.Focused);TacEnd(s);TacStep(s,2,0);
                Require(TestOnlyClubAttackPolicy.PendingMove(s.Capture())==null&&Resources(s).ReactionAvailable&&Body(s,TestOnlyPolicy.CompanionId).X==2,"Unused Focused allowed ordinary OA or spent its resource.");
            });
            cases.Add("tactical_mobile_first_actual_step_suppresses_only_oa_not_later_steps",()=>{
                var s=Tactical(stance:CombatStance.Mobile);TacStep(s,0,1);Require(Resources(s).MobileFeet==5,"Safe first actual movement did not use Mobile allowance.");
                TacStep(s,0,2);Require(TestOnlyClubAttackPolicy.PendingMove(s.Capture())!=null,"Second step received renewed Mobile protection.");
                AnswerOpportunity(s,false);TacEnd(s);TacStep(s,2,0);AnswerIfPending(s);TacEnd(s,CombatStance.Aggressive);
                Require(Resources(s).MobileFeet==0&&TestOnlyClubAttackPolicy.ActiveStance(s.Capture(),TestOnlyPolicy.ActorId).Kind==CombatStance.Aggressive,"Own Start did not clear counter or forced Mobile.");
            });
            cases.Add("tactical_mobile_protection_uses_distance_not_standing_or_terrain_cost",()=>{
                var s=Tactical(TacticalPolicy(actorProne:true,terrain:new[]{new TacticalTerrainCell(0,1,TerrainCost.Difficult)}),CombatStance.Mobile);
                CommitTac(s,Tac(s,CommandKind.StandFromProne));Require(Resources(s).MobileFeet==0,"Standing consumed Mobile travel.");TacStep(s,0,1);
                Require(Resources(s).MobileFeet==5&&TestOnlyClubAttackPolicy.WalkingLedger(s.Capture()).Spent==25,"Terrain cost mistaken for Mobile distance.");
            });
            cases.Add("tactical_disengage_spends_action_and_expires_at_turn_end",()=>{
                var s=Tactical();CommitTac(s,Tac(s,CommandKind.Disengage));RejectUnchanged(s,host,Tac(s,CommandKind.EncounterDash),"ActionAlreadySpent");
                TacStep(s,0,1);TacStep(s,0,2);Require(TestOnlyClubAttackPolicy.PendingMove(s.Capture())==null&&Resources(s,TestOnlyPolicy.CompanionId).ReactionAvailable,"Disengage did not suppress OA.");
                TacEnd(s);Require(Resources(s).DisengageTurn==0&&s.Capture().Encounter.TurnOrdinal==1,"Disengage lost historical turn marker.");
            });
            cases.Add("tactical_own_action_attack_and_dash_do_not_block_remaining_movement",()=>{
                var s=Tactical(TacticalPolicy(SeedForDeath(16)));CommitTac(s,Tac(s,CommandKind.AttackUnarmed,TestOnlyPolicy.CompanionId));TacStep(s,0,1);
                Require(TestOnlyClubAttackPolicy.ActionSpent(s.Capture())&&Body(s).Y==1,"Action use blocked voluntary movement.");
                s=Tactical(TacticalPolicy(actorSpeed:5));CommitTac(s,Tac(s,CommandKind.EncounterDash));TacStep(s,0,1);TacStep(s,0,2);AnswerOpportunity(s,false);
                Require(TestOnlyClubAttackPolicy.WalkingLedger(s.Capture()).Spent==10,"Dash movement refunded prior cost.");
            });
            cases.Add("tactical_press_triggers_after_actual_retreat_and_uses_separate_budget",()=>{
                var s=Tactical(TacticalPolicy(SeedForDeath(16)));CommitTac(s,Tac(s,CommandKind.AttackUnarmed,TestOnlyPolicy.CompanionId));TacEnd(s);TacStep(s,2,0);
                Require(TestOnlyClubAttackPolicy.CurrentPressOffer(s.Capture())==null&&Body(s,TestOnlyPolicy.CompanionId).X==1,"Press triggered before actual departure.");
                AnswerOpportunity(s,false);var offer=TestOnlyClubAttackPolicy.CurrentPressOffer(s.Capture());Require(offer!=null&&offer.ActorId==TestOnlyPolicy.ActorId,"Completed retreat did not offer Press.");
                CommitTac(s,PressChoice(s,true));Require(Body(s).X==1&&Resources(s).PressConsumed&&s.Capture().ActorMovement.Single(m=>m.ActorId==TestOnlyPolicy.ActorId).Spent==0
                    &&s.Capture().TacticalMoves.Last().Kind==TacticalMoveKind.Press&&Resources(s).ReactionAvailable,"Press spent ordinary movement or Reaction.");
            });
            cases.Add("tactical_lateral_move_remaining_adjacent_never_triggers_press",()=>{
                var s=Tactical(TacticalPolicy(SeedForDeath(16)));CommitTac(s,Tac(s,CommandKind.AttackUnarmed,TestOnlyPolicy.CompanionId));TacEnd(s);TacStep(s,1,1);
                Require(TestOnlyClubAttackPolicy.PendingMove(s.Capture())==null&&TestOnlyClubAttackPolicy.CurrentPressOffer(s.Capture())==null&&!Resources(s).PressConsumed,"Lateral adjacency counted as retreat.");
            });
            cases.Add("tactical_press_decline_preserves_entitlement_for_later_retreat",()=>{
                var s=Tactical(TacticalPolicy(SeedForDeath(16)));CommitTac(s,Tac(s,CommandKind.AttackUnarmed,TestOnlyPolicy.CompanionId));TacEnd(s);TacStep(s,2,0);AnswerOpportunity(s,false);
                CommitTac(s,PressChoice(s,false));Require(!Resources(s).PressConsumed,"Declined follow consumed entitlement.");
                TacStep(s,1,0);TacStep(s,2,0);AnswerOpportunity(s,false);Require(TestOnlyClubAttackPolicy.CurrentPressOffer(s.Capture())!=null,"Later retreat did not offer retained Press.");CommitTac(s,PressChoice(s,true));
            });
            cases.Add("tactical_press_difficult_destination_or_prone_cost_exceeds_separate_budget",()=>{
                var s=Tactical(TacticalPolicy(SeedForDeath(16),terrain:new[]{new TacticalTerrainCell(1,0,TerrainCost.Difficult)}));
                CommitTac(s,Tac(s,CommandKind.AttackUnarmed,TestOnlyPolicy.CompanionId));TacEnd(s);TacStep(s,2,0);AnswerOpportunity(s,false);
                Require(TestOnlyClubAttackPolicy.CurrentPressOffer(s.Capture())==null&&!Resources(s).PressConsumed,"Five-point Press allowance entered difficult tile.");
            });
            cases.Add("tactical_mobile_departure_still_triggers_press_and_follow_consumes_distance",()=>{
                var s=Tactical(TacticalPolicy(SeedForDeath(16)),CombatStance.Mobile);CommitTac(s,Tac(s,CommandKind.AttackUnarmed,TestOnlyPolicy.CompanionId));TacEnd(s,CombatStance.Mobile);TacStep(s,2,0);
                Require(TestOnlyClubAttackPolicy.PendingMove(s.Capture())==null&&TestOnlyClubAttackPolicy.CurrentPressOffer(s.Capture())!=null,"Mobile suppressed Press or failed OA protection.");
                CommitTac(s,PressChoice(s,true));Require(Resources(s).MobileFeet==5&&Resources(s).PressConsumed,"Separate Press did not consume Mobile distance.");
            });
            cases.Add("tactical_accepted_press_interrupted_by_oa_retains_entitlement_cost",()=>{
                var p=TacticalPolicy(TacticalSeed(16,16),actorHp:1,third:new AdditionalTacticalActor(0,1,30));var s=Tactical(p);TacStep(s,1,1);
                CommitTac(s,Tac(s,CommandKind.AttackUnarmed,TestOnlyPolicy.CompanionId));TacEnd(s);TacStep(s,2,0);AnswerOpportunity(s,false);
                TacStep(s,3,0);AnswerOpportunity(s,false);CommitTac(s,PressChoice(s,true));
                Require(Resources(s).PressConsumed&&TestOnlyClubAttackPolicy.PendingMove(s.Capture()).Kind==TacticalMoveKind.Press&&Body(s).X==1&&Body(s).Y==1,"Accepted follow was not committed before its OA.");
                AnswerOpportunity(s,true,knockout:AttackKnockoutMode.AskIfEligible);var pending=s.Capture().MeleeAttacks.Single(a=>a.Pending);
                string file=Path.Combine(directory,"pending-press-knockout.ddsave");new FileSaveStore().Save(file,s.Capture());s=new Simulation(p,new FileSaveStore().Load(file),ExecutionProfile.Laboratory);
                CommitTac(s,Tac(s,CommandKind.ResolveKnockout,pending.Id,AdditionalTacticalActor.Id,choice:true));
                Require(Life(s).Stable&&Resources(s).PressConsumed&&Body(s).X==1&&Body(s).Y==1&&s.Capture().ActorMovement.Single(a=>a.ActorId==TestOnlyPolicy.ActorId).Spent==5
                    &&s.Capture().TacticalMoves.Last().CostPaid==0&&s.Capture().TacticalMoves.Last().Status==TacticalMoveStatus.Interrupted,"Interrupted Press refunded entitlement or charged distance/cost.");
            });
            cases.Add("tactical_competing_press_uses_application_order_and_revalidates_occupancy",()=>{
                var s=Tactical(TacticalPolicy(TacticalSeed(16,16,16),third:new AdditionalTacticalActor(0,1,30)));
                CommitTac(s,Tac(s,CommandKind.AttackUnarmed,TestOnlyPolicy.CompanionId));TacEnd(s);TacEnd(s);
                CommitTac(s,Tac(s,CommandKind.AttackUnarmed,TestOnlyPolicy.CompanionId));TacEnd(s);
                CommitTac(s,Tac(s,CommandKind.AttackUnarmed,TestOnlyPolicy.CompanionId));TacEnd(s);TacStep(s,2,0);AnswerIfPending(s);
                Require(TestOnlyClubAttackPolicy.CurrentPressOffer(s.Capture()).ActorId==AdditionalTacticalActor.Id,"Initiative order incorrectly replaced Press application order.");
                CommitTac(s,PressChoice(s,true));Require(Body(s,AdditionalTacticalActor.Id).X==1&&Body(s,AdditionalTacticalActor.Id).Y==0&&Resources(s,AdditionalTacticalActor.Id).PressConsumed
                    &&!Resources(s).PressConsumed&&TestOnlyClubAttackPolicy.CurrentPressOffer(s.Capture())==null&&s.Capture().PressOffers.Count(p=>p.Status==PressOfferStatus.Invalidated)==1,"Occupied vacated space did not invalidate later Press without spending it.");
            });
            cases.Add("tactical_nested_press_follows_actual_departures_and_terminates",()=>{
                var p=TacticalPolicy(TacticalSeed(16,16),third:new AdditionalTacticalActor(0,1,30));var s=Tactical(p);TacStep(s,1,1);TacEnd(s);TacEnd(s);
                CommitTac(s,Tac(s,CommandKind.AttackUnarmed,TestOnlyPolicy.ActorId));TacEnd(s,CombatStance.Mobile);
                CommitTac(s,Tac(s,CommandKind.AttackUnarmed,TestOnlyPolicy.CompanionId));TacEnd(s);TacStep(s,2,0);AnswerIfPending(s);TacStep(s,3,0);AnswerIfPending(s);
                CommitTac(s,PressChoice(s,true));Require(Body(s).X==2&&Body(s).Y==0&&Resources(s).MobileFeet==5&&TestOnlyClubAttackPolicy.CurrentPressOffer(s.Capture())?.ActorId==AdditionalTacticalActor.Id,"Completed Mobile-protected follow failed to trigger another holder's Press.");
                s=RestoreClub(s,p);CommitTac(s,PressChoice(s,true));Require(Body(s,AdditionalTacticalActor.Id).X==1&&Body(s,AdditionalTacticalActor.Id).Y==1&&Resources(s).PressConsumed&&Resources(s,AdditionalTacticalActor.Id).PressConsumed
                    &&TestOnlyClubAttackPolicy.PendingMove(s.Capture())==null&&TestOnlyClubAttackPolicy.CurrentPressOffer(s.Capture())==null,"Nested Press did not terminate after consuming finite entitlements.");
            });
            cases.Add("tactical_own_turn_oa_arms_press_and_consumed_follow_cannot_rearm",()=>{
                var s=Tactical(TacticalPolicy(TacticalSeed(16,16,16,16),third:new AdditionalTacticalActor(1,3,30)));TacStep(s,1,1);TacEnd(s);
                TacStep(s,0,1);TacStep(s,0,2);CommitTac(s,Tac(s,CommandKind.AttackUnarmed,TestOnlyPolicy.ActorId));TacEnd(s);
                CommitTac(s,Tac(s,CommandKind.AttackUnarmed,TestOnlyPolicy.CompanionId));TacEnd(s);TacStep(s,2,2);AnswerOpportunity(s,false);
                CommitTac(s,PressChoice(s,true));AnswerOpportunity(s,false);CommitTac(s,PressChoice(s,true));
                Require(TestOnlyClubAttackPolicy.PendingMove(s.Capture()).Reactors.Single()==TestOnlyPolicy.ActorId,"Nested follow did not open current actor's own-turn OA.");
                AnswerOpportunity(s,true);var armed=TestOnlyClubAttackPolicy.ActivePress(s.Capture(),TestOnlyPolicy.ActorId);
                Require(armed!=null&&armed.TargetId==AdditionalTacticalActor.Id&&s.Capture().MeleeAttacks.Last().Opportunity&&!TestOnlyClubAttackPolicy.ActionSpent(s.Capture()),"Own-turn OA failed to arm Press or spent Action.");
                CommitTac(s,PressChoice(s,true));AnswerIfPending(s);Require(Resources(s).PressConsumed&&Body(s).X==1&&Body(s).Y==3,"Current actor's follow did not consume entitlement.");
                CommitTac(s,Tac(s,CommandKind.AttackUnarmed,AdditionalTacticalActor.Id));Require(s.Capture().MeleeAttacks.Last().Attack.Hit&&TestOnlyClubAttackPolicy.ActivePress(s.Capture(),TestOnlyPolicy.ActorId).ArmedRevision==armed.ArmedRevision,"Later qualifying own-turn hit rearmed consumed Press.");
            });
            cases.Add("tactical_press_selector_retains_or_replaces_target_during_own_turn_oa",()=>{
                foreach(var choice in new[]{PressHitInstruction.KeepExisting,PressHitInstruction.ArmOrReplace}) {
                    var p=TacticalPolicy(TacticalSeed(16,16,16,16),third:new AdditionalTacticalActor(1,3,30));var s=Tactical(p);TacStep(s,1,1);TacEnd(s,CombatStance.Mobile);
                    TacStep(s,0,1);TacStep(s,0,2);CommitTac(s,Tac(s,CommandKind.AttackUnarmed,TestOnlyPolicy.ActorId));TacEnd(s,CombatStance.Focused);
                    CommitTac(s,Tac(s,CommandKind.AttackUnarmed,TestOnlyPolicy.CompanionId));TacEnd(s);
                    CommitTac(s,Tac(s,CommandKind.AttackUnarmed,TestOnlyPolicy.CompanionId));var old=TestOnlyClubAttackPolicy.ActivePress(s.Capture(),TestOnlyPolicy.ActorId);
                    TacStep(s,2,2);AnswerOpportunity(s,false);CommitTac(s,PressChoice(s,true));CommitTac(s,PressChoice(s,true));s=RestoreClub(s,p);
                    var command=Opportunity(s,true,press:choice);var different=Opportunity(s,true,press:choice==PressHitInstruction.KeepExisting?PressHitInstruction.ArmOrReplace:PressHitInstruction.KeepExisting);
                    CommitTac(s,command);Require(s.Execute(host,command).Outcome==Outcome.Duplicate,"Press selector lost idempotency.");RejectUnchanged(s,host,different,"CommandIdConflict");
                    var armed=TestOnlyClubAttackPolicy.ActivePress(s.Capture(),TestOnlyPolicy.ActorId);
                    Require(s.Capture().MeleeAttacks.Last().Attack.Hit&&s.Capture().MeleeAttacks.Last().PressInstruction==choice,"Qualifying own-turn OA lost selector.");
                    Require(choice==PressHitInstruction.KeepExisting?armed.SameAs(old):armed.TargetId==AdditionalTacticalActor.Id&&armed.ArmedRevision>old.ArmedRevision,"Controller's retain/replace choice was ignored.");
                    s=RestoreClub(s,p);if(choice==PressHitInstruction.ArmOrReplace)CommitTac(s,PressChoice(s,false));
                }
            });
            cases.Add("tactical_press_keep_empty_survives_pending_knockout_and_cannot_change",()=>{
                var p=TacticalPolicy(SeedForDeath(16),companionHp:1);var s=Tactical(p);
                CommitTac(s,Tac(s,CommandKind.AttackUnarmed,TestOnlyPolicy.CompanionId,knockout:AttackKnockoutMode.AskIfEligible,press:PressHitInstruction.KeepExisting));
                var pending=s.Capture().MeleeAttacks.Single();Require(pending.Pending&&pending.PressInstruction==PressHitInstruction.KeepExisting&&s.Capture().Presses.Length==0,"Keep-empty armed first Press or lost pending instruction.");
                string file=Path.Combine(directory,"pending-keep-press.ddsave");new FileSaveStore().Save(file,s.Capture());s=new Simulation(p,new FileSaveStore().Load(file),ExecutionProfile.Laboratory);
                RejectUnchanged(s,host,Tac(s,CommandKind.ResolveKnockout,pending.Id,choice:true,press:PressHitInstruction.KeepExisting),"InvalidKnockoutChoice");
                CommitTac(s,Tac(s,CommandKind.ResolveKnockout,pending.Id,choice:true));Require(s.Capture().Presses.Length==0&&s.Capture().MeleeAttacks.Single().PressInstruction==PressHitInstruction.KeepExisting&&Life(s,TestOnlyPolicy.CompanionId).Stable,"KO resolution reinterpreted Press or lost selector.");
                s=RestoreClub(s,p);
            });
            cases.Add("tactical_press_selector_rejects_nonattack_payloads_and_forged_history",()=>{
                var p=TacticalPolicy(SeedForDeath(16));var s=Tactical(p);CommitTac(s,Tac(s,CommandKind.AttackUnarmed,TestOnlyPolicy.CompanionId,press:PressHitInstruction.KeepExisting));
                var v=s.Capture();var a=v.MeleeAttacks.Single();v.MeleeAttacks=new[]{new MeleeAttackRecord(a.Id,a.Revision,a.ResolvedRevision,a.TurnOrdinal,a.AttackerId,a.TargetId,a.WeaponId,a.At,a.Instruction,a.Attack,a.Damage,a.Opportunity)};
                Throws<ArgumentException>(()=>new Simulation(p,codec.Decode(codec.Encode(v)),ExecutionProfile.Laboratory));
                s=Clubs(p);BeginEncounter(s);RejectUnchanged(s,host,Tac(s,CommandKind.SelectCombatStance,stance:(int)CombatStance.Aggressive,press:PressHitInstruction.KeepExisting),"InvalidStanceRequest");
                Throws<ArgumentException>(()=>new CombatRequest("turn",pressInstruction:(PressHitInstruction)2));
            });
            cases.Add("tactical_snapshot_rejects_forged_reaction_movement_and_press_state",()=>{
                var p=TacticalPolicy();var s=Tactical(p);TacStep(s,0,1);TacStep(s,0,2);
                var v=s.Capture();v.TacticalActors=v.TacticalActors.Select(a=>a.ActorId==TestOnlyPolicy.CompanionId?new ActorTacticalRecord(a.ActorId,a.LastRegularStart,false):a).ToArray();
                Throws<ArgumentException>(()=>new Simulation(p,codec.Decode(codec.Encode(v)),ExecutionProfile.Laboratory));
                v=s.Capture();var m=v.TacticalMoves.Last();v.TacticalMoves[v.TacticalMoves.Length-1]=m.Progress(m.Reactors.Count,m.Status);
                Throws<ArgumentException>(()=>new Simulation(p,codec.Decode(codec.Encode(v)),ExecutionProfile.Laboratory));
                v=s.Capture();v.TacticalActors=v.TacticalActors.Select(a=>new ActorTacticalRecord(a.ActorId,a.LastRegularStart,a.ReactionAvailable,a.MobileFeet,true)).ToArray();
                Throws<ArgumentException>(()=>new Simulation(p,codec.Decode(codec.Encode(v)),ExecutionProfile.Laboratory));
            });
            cases.Add("tactical_save_during_offer_and_each_response_preserves_deterministic_trace",()=>{
                var p=TacticalPolicy(SeedForDeath(16));var a=Tactical(p);TacStep(a,0,1);TacStep(a,0,2);
                string file=Path.Combine(directory,"pending-oa.ddsave");new FileSaveStore().Save(file,a.Capture());var b=new Simulation(p,new FileSaveStore().Load(file),ExecutionProfile.Laboratory);
                AnswerOpportunity(a,true);AnswerOpportunity(b,true);Require(Bytes(a).SequenceEqual(Bytes(b)),"Reload changed attack, movement or resource trace.");
            });
            cases.Add("tactical_history_reserves_whole_continuation_before_announcing_step",()=>{
                var p=TacticalPolicy();var s=Tactical(p);
                for(int i=0;i<62;i++) {
                    if(TestOnlyClubAttackPolicy.WalkingLedger(s.Capture()).Remaining(TestOnlyClubAttackPolicy.WalkingSpeed(s.Capture(),TestOnlyPolicy.ActorId))<5){TacEnd(s);TacEnd(s);}
                    TacStep(s,0,Body(s).Y==0?1:0);
                }
                Require(s.Capture().TacticalMoves.Length==62&&TestOnlyClubAttackPolicy.PendingMove(s.Capture())==null,"Bound fixture did not reach completed history.");
                s=RestoreClub(s,p);RejectUnchanged(s,host,Tac(s,CommandKind.TacticalStep,x:0,y:Body(s).Y==0?1:0),"ContinuationCapacityReached");
            });
            cases.Add("tactical_core_collections_are_detached_and_legacy_fields_reject",()=>{
                var p=TacticalPolicy();var s=Tactical(p);TacStep(s,0,1);TacStep(s,0,2);var v=s.Capture();
                Throws<NotSupportedException>(()=>((IList<string>)v.TacticalMoves.Last().Reactors)[0]=TestOnlyPolicy.ActorId);
                v.TacticalActors=Array.Empty<ActorTacticalRecord>();Throws<ArgumentException>(()=>codec.Encode(v));
                v=s.Capture();v.SchemaVersion=10;Throws<ArgumentException>(()=>codec.Encode(v));
                Throws<InvalidOperationException>(()=>new Simulation(p,p.Initial(),ExecutionProfile.Release));
                byte[] bad=Bytes(s);bad[4]=12;Resign(bad);Throws<InvalidDataException>(()=>codec.Decode(bad));
            });
        }
        private static void AnswerIfPending(Simulation s){while(TestOnlyClubAttackPolicy.PendingMove(s.Capture())!=null)AnswerOpportunity(s,false);}
        private static uint TacticalSeed(params int[] naturals)
        {
            for(uint seed=1;seed<1000000;seed++) {uint next=seed;bool match=true;foreach(int natural in naturals) {var roll=PlaytestDice.RollD20(next);next=roll.NextRandomState;if(roll.Natural!=natural){match=false;break;}}if(match)return seed;}
            throw new Exception("No deterministic tactical fixture seed.");
        }
    }
}
#endif
