#if DECENNIUM_TEST_ONLY && (UNITY_EDITOR || HEADLESS_TESTS)
using System;
using System.Collections.Generic;
using System.Linq;
using Decennium.Foundation.Laboratory;

namespace Decennium.Foundation.Tests
{
    public static partial class FoundationCases
    {
        private static LifeState ChangeExhaustionFromZero(LifeState state,long maximum,int level)=>PlaytestConditions.ChangeExhaustion(state,maximum,0,level);
        private static ConditionClauses C(params ConditionClause[] clauses)=>new ConditionClauses(clauses);
        private static void AddConditionProjectionCases(Dictionary<string,Action> cases)
        {
            cases.Add("condition_clauses_detach_deduplicate_and_reject_unknown",()=>{
                var source=new[]{ConditionClause.Poisoned,ConditionClause.Poisoned};var c=new ConditionClauses(source);source[0]=ConditionClause.Prone;
                Require(c.Active.Count==1&&c.Has(ConditionClause.Poisoned)&&!c.Has(ConditionClause.Prone),"Projection leaked caller data or duplicated penalties.");
                Throws<NotSupportedException>(()=>((IList<ConditionClause>)c.Active)[0]=ConditionClause.Prone);
                Throws<ArgumentException>(()=>C((ConditionClause)99));Throws<ArgumentException>(()=>new ConditionClauses(null)); });
            cases.Add("condition_exhaustion_halves_unmodified_maximum_once",()=>{
                var s=ChangeExhaustionFromZero(new LifeState(31,28),31,4);
                Require(s.MaximumHp==15&&s.Hp==15,"Odd maximum did not floor/clamp.");s=ChangeExhaustionFromZero(s,31,5);
                Require(s.MaximumHp==15&&s.Hp==15,"Existing Exhaustion was halved twice.");s=ChangeExhaustionFromZero(s,41,5);
                Require(s.MaximumHp==20&&s.Hp==15,"Maximum buff healed HP.");s=ChangeExhaustionFromZero(s,41,3);
                Require(s.MaximumHp==41&&s.Hp==15,"Removing Exhaustion healed HP."); });
            cases.Add("condition_exhaustion_minimum_and_critical_healing_ceiling",()=>{
                var s=ChangeExhaustionFromZero(new LifeState(1,1,5,new[]{Injury.None,Injury.None,Injury.None}),1,4);
                Require(s.MaximumHp==1&&s.Hp==1&&s.HealingCeiling==1&&s.TemporaryHp==5&&s.Wounds.Count==3,"Exhaustion erased temporary HP/Wounds or made max zero.");
                s=ChangeExhaustionFromZero(new LifeState(31,28,wounds:new[]{Injury.None,Injury.None,Injury.None}),31,4);
                Require(s.Hp==15&&s.HealingCeiling==14&&PlaytestLife.Heal(s,10).Hp==15,"Maximum reduction applied a healing-only ceiling retroactively."); });
            cases.Add("condition_exhaustion_six_kills_without_damage_or_revival",()=>{
                var s=ChangeExhaustionFromZero(new LifeState(20,0,7,stable:true,stableUntil:T(1,3)),20,6);
                Require(s.Dead&&!s.Stable&&s.Hp==0&&s.StableUntil==null&&s.TemporaryHp==7&&s.Wounds.Count==0,"Level6 was treated as damage or retained Stable timer.");
                var recovered=ChangeExhaustionFromZero(s,20,0);Require(recovered.Dead&&recovered.MaximumHp==20&&recovered.Hp==0,"Clearing Exhaustion resurrected."); });
            cases.Add("condition_exhaustion_preserves_dying_history_and_exact_recovery",()=>{
                var s=new LifeState(26,0,3,new[]{Injury.Concussion},deathSuccesses:1,deathFailures:2,lastDeathTurn:7);
                var changed=ChangeExhaustionFromZero(s,26,4);Require(changed.DeathSuccesses==1&&changed.DeathFailures==2&&changed.LastDeathTurn==7&&changed.Wounds.Single()==Injury.Concussion,"Maximum recomputation erased ongoing dying state.");
                s=new LifeState(26,0,stable:true,stableUntil:T(19,3));changed=ChangeExhaustionFromZero(s,26,4);
                Require(changed.Stable&&changed.StableUntil==T(19,3),"Maximum recomputation restarted exact Stable deadline."); });
            cases.Add("condition_capacity_recalculation_never_rekills_track_six_survivor",()=>{
                var survivor=new LifeState(26,0,4,stable:true,stableUntil:T(17,3));
                var recomputed=PlaytestConditions.RecomputeExhaustionCapacity(survivor,40,6);
                Require(!recomputed.Dead&&recomputed.Stable&&recomputed.StableUntil==T(17,3)&&recomputed.MaximumHp==20,"Capacity-only calculation killed a surviving track6 state.");
                var repeated=PlaytestConditions.ChangeExhaustion(recomputed,40,6,6);Require(!repeated.Dead&&repeated.Stable,"Same-level reapplication became a lethal transition.");
                var living=PlaytestConditions.RecomputeExhaustionCapacity(new LifeState(26,4),40,6);Require(living.Hp==4&&!living.Dead,"Capacity-only recomputation killed living positive HP.");
                Throws<ArgumentOutOfRangeException>(()=>PlaytestConditions.ChangeExhaustion(survivor,26,7,6)); });
            cases.Add("condition_exhaustion_sampled_idempotence_and_no_healing",()=>{
                int samples=0;for(int max=1;max<=200;max++)foreach(int hp in new[]{0,max/2,max})for(int level=0;level<=6;level++) {
                    var current=ChangeExhaustionFromZero(new LifeState(max,hp),max,level);var repeated=PlaytestConditions.ChangeExhaustion(current,max,level,level);
                    Require(current.MaximumHp==repeated.MaximumHp&&current.Hp==repeated.Hp&&current.Dead==repeated.Dead&&current.Hp<=hp
                        &&current.MaximumHp>=1&&current.Hp<=current.MaximumHp&&current.Dead==(level==6),"Exhaustion state invariant failed.");
                    Require(ChangeExhaustionFromZero(current,max,0).Hp==current.Hp,"Removing Exhaustion healed a sampled state.");samples++;
                }Require(samples==4200,"Missing Exhaustion samples."); });
            cases.Add("condition_speed_flats_precede_halving_and_zero_overrides",()=>{
                Require(PlaytestConditions.EffectiveSpeed(30,-15,C(),2)==7&&PlaytestConditions.EffectiveSpeed(30,-100,C(),2)==0,"Speed adjustment order wrong.");
                foreach(var c in new[]{ConditionClause.Grappled,ConditionClause.Restrained,ConditionClause.Paralyzed,ConditionClause.Petrified,ConditionClause.Stunned,ConditionClause.Unconscious})
                    Require(PlaytestConditions.EffectiveSpeed(30,100,C(c))==0,"Positive bonus bypassed zero Speed.");
                Require(PlaytestConditions.EffectiveSpeed(30,100,C(),5)==0&&PlaytestConditions.EffectiveSpeed(30,0,C(ConditionClause.Incapacitated))==30,"Incapacitated became immobile or Exhaustion5 failed."); });
            cases.Add("condition_speed_widens_before_halving_and_rejects_final_overflow",()=>{
                Require(PlaytestConditions.EffectiveSpeed(long.MaxValue,long.MaxValue,C(),2)==long.MaxValue
                    &&PlaytestConditions.EffectiveSpeed(0,long.MinValue,C())==0,"Speed intermediate overflow or negative wrap.");
                Throws<OverflowException>(()=>PlaytestConditions.EffectiveSpeed(long.MaxValue,1,C()));
                Require(PlaytestConditions.EffectiveSpeed(long.MaxValue,long.MaxValue,C(ConditionClause.Grappled))==0,"Irrelevant overflowing bonus defeated zero override."); });
            cases.Add("condition_incapacitated_blocks_actions_but_retains_movement",()=>{
                var p=PlaytestConditions.Permissions(C(ConditionClause.Incapacitated));Require(!p.Action&&!p.BonusAction&&!p.Reaction&&!p.ConcentrationMayContinue&&p.VoluntarySpeed&&!p.Dash,"Incapacitated restrictions wrong.");
                foreach(var c in new[]{ConditionClause.Paralyzed,ConditionClause.Petrified,ConditionClause.Stunned,ConditionClause.Unconscious}) {
                    p=PlaytestConditions.Permissions(C(c));Require(!p.Action&&!p.BonusAction&&!p.Reaction&&!p.VoluntarySpeed&&!p.ConcentrationMayContinue,"Inherited Incapacitated/immobility missing.");}
            });
            cases.Add("condition_dazed_requires_choice_and_never_grants_dash",()=>{
                var p=PlaytestConditions.Permissions(C(ConditionClause.Dazed));Require(p.Action&&p.VoluntarySpeed&&p.MustChooseActionOrMovement&&!p.BonusAction&&!p.Dash&&p.Reaction&&p.ConcentrationMayContinue,"Fresh Dazed modes wrong.");
                p=PlaytestConditions.Permissions(C(ConditionClause.Dazed),voluntarySpeedSpent:5);Require(!p.Action&&p.VoluntarySpeed&&!p.MustChooseActionOrMovement,"Movement before Dazed refunded an Action.");
                p=PlaytestConditions.Permissions(C(ConditionClause.Dazed),actionsTaken:1);Require(!p.Action&&!p.VoluntarySpeed&&!p.MustChooseActionOrMovement,"Dazed extra Action or movement bypass.");
                p=PlaytestConditions.Permissions(C(ConditionClause.Dazed),actionsTaken:1,voluntarySpeedSpent:5);Require(!p.Action&&!p.VoluntarySpeed,"Mid-turn Dazed undid both earlier spendings."); });
            cases.Add("condition_staggered_reaction_constraint_is_independent_of_dazed",()=>{
                var p=PlaytestConditions.Permissions(C(ConditionClause.Staggered));Require(p.Action&&p.BonusAction&&!p.Reaction&&p.VoluntarySpeed&&p.ConcentrationMayContinue,"Staggered removed unrelated permissions.");
                p=PlaytestConditions.Permissions(C(ConditionClause.Dazed,ConditionClause.Staggered));Require(p.Action&&!p.BonusAction&&!p.Reaction,"Combined restrictions lost a condition."); });
            cases.Add("condition_prone_melee_and_ranged_endpoints_match_core",()=>{
                var prone=C(ConditionClause.Prone);
                Require(PlaytestConditions.Attack(C(),prone).RollMode==D20Selection.Advantage
                    &&PlaytestConditions.Attack(C(),prone,10).RollMode==D20Selection.Disadvantage
                    &&PlaytestConditions.Attack(C(),prone,5,ConditionAttackKind.Ranged).RollMode==D20Selection.Disadvantage
                    &&PlaytestConditions.Attack(C(),prone,0,ConditionAttackKind.Ranged).RollMode==D20Selection.Disadvantage,"Prone range/kind branch wrong."); });
            cases.Add("condition_many_advantages_and_disadvantages_cancel_once",()=>{
                var r=PlaytestConditions.Attack(C(ConditionClause.Blinded,ConditionClause.Poisoned,ConditionClause.Prone,ConditionClause.Restrained),C(ConditionClause.Restrained));
                Require(r.AdvantagePresent&&r.DisadvantagePresent&&r.RollMode==D20Selection.Normal,"Condition penalties used majority voting.");
                r=PlaytestConditions.Attack(C(),C(),otherAdvantage:true,otherDisadvantage:true);Require(r.RollMode==D20Selection.Normal,"External opposite modifiers did not cancel."); });
            cases.Add("condition_invisible_known_location_ends_modifiers_without_sight",()=>{
                var invisible=C(ConditionClause.Invisible);
                Require(PlaytestConditions.Attack(invisible,C()).RollMode==D20Selection.Advantage
                    &&PlaytestConditions.Attack(invisible,C(),attackerInvisibleLocationKnown:true).RollMode==D20Selection.Normal
                    &&PlaytestConditions.Attack(invisible,C(),targetSeesInvisibleAttacker:true).RollMode==D20Selection.Normal,"Invisible attacker endpoint wrong.");
                Require(PlaytestConditions.Attack(C(),invisible).RollMode==D20Selection.Disadvantage
                    &&PlaytestConditions.Attack(C(),invisible,targetInvisibleLocationKnown:true).RollMode==D20Selection.Normal
                    &&PlaytestConditions.Attack(C(),invisible,attackerSeesInvisibleTarget:true).RollMode==D20Selection.Normal,"Invisible target endpoint wrong.");
                Require(PlaytestConditions.Attack(C(ConditionClause.Invisible,ConditionClause.Poisoned),C(),attackerInvisibleLocationKnown:true).RollMode==D20Selection.Disadvantage,"Location revelation erased independent Poisoned."); });
            cases.Add("condition_frightened_visibility_and_exhaustion_attack_penalties",()=>{
                Require(PlaytestConditions.Attack(C(ConditionClause.Frightened),C()).RollMode==D20Selection.Normal
                    &&PlaytestConditions.Attack(C(ConditionClause.Frightened),C(),frightenedSourceVisible:true).RollMode==D20Selection.Disadvantage,"Fear visibility misapplied.");
                Require(PlaytestConditions.Attack(C(),C(),attackerExhaustion:2).RollMode==D20Selection.Normal
                    &&PlaytestConditions.Attack(C(),C(),attackerExhaustion:3).RollMode==D20Selection.Disadvantage,"Exhaustion attack threshold wrong."); });
            cases.Add("condition_critical_if_hit_never_overrides_a_miss",()=>{
                foreach(var c in new[]{ConditionClause.Paralyzed,ConditionClause.Unconscious}) {
                    var r=PlaytestConditions.Attack(C(),C(c));var miss=PlaytestRolls.AttackRoll(1,100,10);
                    Require(r.CriticalIfHit&&r.AdvantagePresent&&!miss.Hit&&!(miss.Hit&&r.CriticalIfHit),"Critical-if-hit turned a miss into hit.");
                    Require(!PlaytestConditions.Attack(C(),C(c),6).CriticalIfHit,"Critical clause exceeded five feet.");
                    Require(PlaytestConditions.Attack(C(),C(c),5,ConditionAttackKind.Ranged).CriticalIfHit,"Adjacent ranged hit lost critical clause.");}
                Require(!PlaytestConditions.Attack(C(),C(ConditionClause.Petrified)).CriticalIfHit&&!PlaytestConditions.Attack(C(),C(ConditionClause.Prone)).CriticalIfHit,"Advantage alone became critical."); });
            cases.Add("condition_attack_ability_is_separate_from_rolled_modifiers",()=>{
                var r=PlaytestConditions.Attack(C(ConditionClause.Unconscious),C(ConditionClause.Restrained));Require(!r.AttackerNotIncapacitated&&r.AdvantagePresent,"Illegal attacker was made able by advantage.");
                Require(PlaytestConditions.Attack(C(ConditionClause.Dazed),C()).AttackerNotIncapacitated,"Dazed silently became Incapacitated."); });
            cases.Add("condition_corrupted_halves_healing_once_before_existing_ceiling",()=>{
                long amount=PlaytestConditions.HpRestorationAmount(5,true);Require(amount==2&&PlaytestLife.Heal(new LifeState(20,2),amount).Hp==4,"Odd healing did not round down once.");
                var critical=new LifeState(20,18,wounds:new[]{Injury.None,Injury.None,Injury.None});Require(PlaytestLife.Heal(critical,PlaytestConditions.HpRestorationAmount(10,true)).Hp==19,"Corrupted bypassed Wound healing ceiling.");
                Require(PlaytestConditions.HpRestorationAmount(5,false)==5&&PlaytestConditions.HpRestorationAmount(long.MaxValue,true)==long.MaxValue/2,"Uncorrupted/extreme healing changed."); });
            cases.Add("condition_zero_corrupted_healing_preserves_dying_or_stable_state",()=>{
                var s=new LifeState(20,0,deathFailures:2);var healed=PlaytestLife.Heal(s,PlaytestConditions.HpRestorationAmount(1,true));Require(healed.Hp==0&&healed.DeathFailures==2&&!healed.Stable,"Zero healing cleared dying state.");
                s=new LifeState(20,0,stable:true,stableUntil:T(10,3));healed=PlaytestLife.Heal(s,PlaytestConditions.HpRestorationAmount(1,true));Require(healed.Stable&&healed.StableUntil==T(10,3),"Zero healing restarted recovery.");
                Throws<ArgumentException>(()=>PlaytestLife.Heal(new LifeState(20,0,dead:true),PlaytestConditions.HpRestorationAmount(20,true))); });
            cases.Add("condition_guaranteed_one_hp_recovery_is_not_corrupted_healing",()=>{
                Require(PlaytestConditions.HpRestorationAmount(1,true,HpRestorationKind.DeathNaturalTwenty)==1
                    &&PlaytestConditions.HpRestorationAmount(1,true,HpRestorationKind.StableRecovery)==1,"Corrupted erased guaranteed recovery.");
                Throws<ArgumentException>(()=>PlaytestConditions.HpRestorationAmount(2,true,HpRestorationKind.StableRecovery));
                Throws<ArgumentException>(()=>PlaytestConditions.HpRestorationAmount(0,true,HpRestorationKind.DeathNaturalTwenty)); });
            cases.Add("condition_petrified_resistance_obeys_corruption_exception",()=>{
                Require(PlaytestConditions.PetrifiedDamage(11)==5&&PlaytestConditions.PetrifiedDamage(11,corruptionDamage:true)==11
                    &&PlaytestConditions.PetrifiedDamage(11,true,true)==5&&PlaytestConditions.PetrifiedDamage(11,immune:true)==0
                    &&PlaytestConditions.PetrifiedDamage(11,true,immune:true)==0,"Petrified resistance/immunity ordering wrong.");
                Require(PlaytestConditions.PetrifiedDamage(long.MaxValue)==long.MaxValue/2&&PlaytestConditions.PetrifiedDamage(1)==0,"Resistance rounding/overflow wrong."); });
            cases.Add("condition_speed_uses_existing_standing_and_crawling_budget",()=>{
                long speed=PlaytestConditions.EffectiveSpeed(30,-5,C(),2);var ledger=new MovementLedger();ledger=ledger.Stand(speed);
                Require(speed==12&&ledger.Spent==6&&ledger.Remaining(speed)==6,"Derived Speed did not govern standing budget.");
                Require(PlaytestCombatBudgets.MovementCost(5,crawling:true)==10&&PlaytestCombatBudgets.MovementCost(5,TerrainCost.Difficult,crawling:true)==15,"Crawl costs diverged.");
                Throws<ArgumentException>(()=>new MovementLedger().Stand(PlaytestConditions.EffectiveSpeed(30,0,C(ConditionClause.Grappled)))); });
            cases.Add("condition_projection_invalid_inputs_fail_closed",()=>{
                Throws<ArgumentOutOfRangeException>(()=>PlaytestConditions.ExhaustionMaximum(20,7));Throws<ArgumentOutOfRangeException>(()=>PlaytestConditions.ExhaustionMaximum(0,4));
                Throws<ArgumentNullException>(()=>ChangeExhaustionFromZero(null,20,1));Throws<ArgumentNullException>(()=>PlaytestConditions.Permissions(null));
                Throws<ArgumentException>(()=>PlaytestConditions.Permissions(C(),actionsTaken:-1));Throws<ArgumentException>(()=>PlaytestConditions.Permissions(C(),voluntarySpeedSpent:-1));
                Throws<ArgumentOutOfRangeException>(()=>PlaytestConditions.EffectiveSpeed(-1,0,C(ConditionClause.Grappled)));Throws<ArgumentOutOfRangeException>(()=>PlaytestConditions.EffectiveSpeed(30,0,C(),-1));
                Throws<ArgumentException>(()=>PlaytestConditions.Attack(C(),C(),-1));Throws<ArgumentException>(()=>PlaytestConditions.Attack(C(),C(),kind:(ConditionAttackKind)99));
                Throws<ArgumentOutOfRangeException>(()=>PlaytestConditions.Attack(C(),C(),attackerExhaustion:7));Throws<ArgumentNullException>(()=>PlaytestConditions.Attack(null,C()));
                Throws<ArgumentException>(()=>PlaytestConditions.HpRestorationAmount(-1,true));Throws<ArgumentException>(()=>PlaytestConditions.HpRestorationAmount(1,true,(HpRestorationKind)99));
                Throws<ArgumentOutOfRangeException>(()=>PlaytestConditions.PetrifiedDamage(-1,immune:true)); });
        }
    }
}
#endif
