#if DECENNIUM_TEST_ONLY && (UNITY_EDITOR || HEADLESS_TESTS)
using System;
using System.Collections.Generic;
using Decennium.Foundation.Laboratory;

namespace Decennium.Foundation.Tests
{
    public static partial class FoundationCases
    {
        private static RangedAttackRequest Ranged(long distance=10,int ac=12,CombatCover cover=CombatCover.None,
            bool locationKnown=true,bool visible=true,bool lineClear=true,bool attackerUnseen=false,bool closeHostile=false,
            bool proficient=true,ConditionClauses attacker=null,ConditionClauses target=null,
            int extraAdvantage=0,int extraDisadvantage=0)
            =>new RangedAttackRequest(distance,80,320,ac,3,2,proficient,0,cover,locationKnown,visible,lineClear,
                attackerUnseen,closeHostile,attacker??new ConditionClauses(),target??new ConditionClauses(),
                additionalAdvantageSources:extraAdvantage,additionalDisadvantageSources:extraDisadvantage);

        private static void AddRangedAttackResolutionCases(Dictionary<string,Action> cases)
        {
            cases.Add("ranged_attack_uses_dexterity_proficiency_and_cover_ac",()=>{
                var r=RangedAttackRules.Resolve(1,Ranged(ac:12,cover:CombatCover.Half));
                Require(r.Legal&&r.AttackModifier==5&&r.EffectiveArmorClass==14&&r.Roll.Selection==D20Selection.Normal
                    &&r.Attack.Hit==(r.Roll.Natural!=1&&(r.Roll.Natural==20||r.Roll.Natural+r.AttackModifier>=r.EffectiveArmorClass)),
                    "Ranged attack omitted Dexterity, proficiency or half cover."); });
            cases.Add("ranged_attack_unproficient_and_three_quarter_cover",()=>{
                var r=RangedAttackRules.Resolve(2,Ranged(ac:12,cover:CombatCover.ThreeQuarters,proficient:false));
                Require(r.Legal&&r.AttackModifier==3&&r.EffectiveArmorClass==17,"Unproficient ranged attack added proficiency or cover was wrong."); });
            cases.Add("ranged_attack_long_range_disadvantage_cancels_unseen_advantage",()=>{
                var r=RangedAttackRules.Resolve(3,Ranged(distance:81,attackerUnseen:true));
                Require(r.Legal&&r.RangeDisadvantage&&r.Roll.Selection==D20Selection.Normal,"Long range and unseen attacker did not cancel."); });
            cases.Add("ranged_attack_unknown_target_blocked_line_and_total_cover_do_not_roll",()=>{
                foreach(var test in new[]{(RangedAttackFailure.UnknownTargetLocation,Ranged(locationKnown:false)),
                    (RangedAttackFailure.BlockedLineOfFire,Ranged(lineClear:false)),(RangedAttackFailure.TotalCover,Ranged(cover:CombatCover.Total))}) {
                    var r=RangedAttackRules.Resolve(123,test.Item2);
                    Require(!r.Legal&&r.Failure==test.Item1&&r.Roll==null&&r.RandomStateAfter==123,"Illegal target consumed a die or returned the wrong failure.");}
            });
            cases.Add("ranged_attack_beyond_long_range_does_not_roll",()=>{
                var r=RangedAttackRules.Resolve(124,Ranged(distance:321));
                Require(!r.Legal&&r.Failure==RangedAttackFailure.OutOfRange&&r.Roll==null&&r.RandomStateAfter==124,
                    "Target beyond maximum range consumed a die."); });
            cases.Add("ranged_attack_unseen_target_and_close_hostile_apply_disadvantage",()=>{
                var r=RangedAttackRules.Resolve(5,Ranged(visible:false,closeHostile:true));
                Require(r.Legal&&r.Roll.Selection==D20Selection.Disadvantage,"Unseen target and eligible close hostile were omitted."); });
            cases.Add("ranged_attack_condition_sources_cancel_across_kinds",()=>{
                var r=RangedAttackRules.Resolve(6,Ranged(attacker:new ConditionClauses(ConditionClause.Poisoned),
                    target:new ConditionClauses(ConditionClause.Stunned)));
                Require(r.Legal&&r.Roll.Selection==D20Selection.Normal,"Attacker disadvantage did not cancel target-condition advantage."); });
            cases.Add("ranged_attack_external_modifier_presence_does_not_overflow_or_stack",()=>{
                var request=new RangedAttackRequest(10,80,320,12,3,2,true,0,CombatCover.None,true,true,true,false,false,
                    new ConditionClauses(),new ConditionClauses(),additionalAdvantageSources:int.MaxValue,additionalDisadvantageSources:int.MaxValue);
                var r=RangedAttackRules.Resolve(7,request);
                Require(r.Legal&&r.Roll.Selection==D20Selection.Normal,"Large modifier counts overflowed or stacked instead of canceling."); });
            cases.Add("ranged_attack_critical_condition_applies_only_on_hit",()=>{
                uint hitSeed=1,missSeed=1;bool foundHit=false,foundMiss=false;
                for(uint i=1;i<100000&&(!foundHit||!foundMiss);i++) {
                    int value=PlaytestDice.RollD20(i,1,0).Natural;
                    if(value==19&&!foundHit){hitSeed=i;foundHit=true;}
                    if(value==1&&!foundMiss){missSeed=i;foundMiss=true;}
                }
                Require(foundHit&&foundMiss,"Could not find deterministic natural-20 and natural-1 seeds.");
                var target=new ConditionClauses(ConditionClause.Unconscious);
                var hit=RangedAttackRules.Resolve(hitSeed,Ranged(distance:5,ac:0,target:target));
                Require(hit.Legal&&hit.Attack.Hit&&hit.Critical,"Close unconscious target did not produce a critical hit.");
                var miss=RangedAttackRules.Resolve(missSeed,Ranged(distance:5,ac:12,target:target));
                Require(miss.Legal&&!miss.Attack.Hit&&!miss.Critical,"Critical condition turned a miss into a critical hit."); });
            cases.Add("ranged_attack_rejects_invalid_profiles_and_sources",()=>{
                Throws<ArgumentException>(()=>RangedAttackRules.Resolve(1,new RangedAttackRequest(-1,80,320,10,0,2,true,0,CombatCover.None,true,true,true,false,false,new ConditionClauses(),new ConditionClauses())));
                Throws<ArgumentException>(()=>RangedAttackRules.Resolve(1,new RangedAttackRequest(1,80,40,10,0,2,true,0,CombatCover.None,true,true,true,false,false,new ConditionClauses(),new ConditionClauses())));
                Throws<ArgumentException>(()=>RangedAttackRules.Resolve(1,new RangedAttackRequest(1,80,320,10,0,2,true,0,CombatCover.None,true,true,true,false,false,null,new ConditionClauses())));
                Throws<ArgumentException>(()=>RangedAttackRules.Resolve(1,new RangedAttackRequest(1,80,320,10,0,2,true,0,(CombatCover)99,true,true,true,false,false,new ConditionClauses(),new ConditionClauses())));
            });
        }
    }
}
#endif
