#if DECENNIUM_TEST_ONLY && (UNITY_EDITOR || HEADLESS_TESTS)
using System;
using System.Collections.Generic;
using Decennium.Foundation.Laboratory;

namespace Decennium.Foundation.Tests
{
    public static partial class FoundationCases
    {
        private static uint RangedSeed(int natural)
        {
            for(uint seed=1;seed<100000;seed++)if(PlaytestDice.RollD20(seed).Natural==natural)return seed;
            throw new Exception("Unable to find a deterministic d20 seed.");
        }

        private static void AddRepeatingCrossbowShotCases(Dictionary<string,Action> cases)
        {
            cases.Add("repeating_crossbow_hit_spends_bolt_and_rolls_source_d10_damage",()=>{
                uint seed=RangedSeed(12);var request=Ranged(ac:0);var magazine=new RepeatingFiveMagazine(2);
                var shot=RepeatingCrossbowShotRules.Resolve(seed,request,magazine,18);
                var attack=RangedAttackRules.Resolve(seed,request);var damage=DiceStream.Draw(attack.RandomStateAfter,10);
                Require(shot.Legal&&shot.Attempted&&shot.Attack.Attack.Hit&&shot.MagazineAfter.LoadedBolts==1
                    &&shot.CarriedBoltsAfter==18&&shot.DamageDice.Count==1&&shot.DamageDice[0]==damage.Value+1
                    &&shot.DamageModifier==3&&shot.RolledDamageBeforeDefense==shot.DamageDice[0]+3
                    &&shot.DamageType=="piercing"&&shot.RandomStateAfter==damage.NextState,
                    "Crossbow hit did not atomically spend one loaded bolt and roll d10 plus Dexterity."); });
            cases.Add("repeating_crossbow_miss_spends_bolt_without_damage_dice",()=>{
                uint seed=RangedSeed(1);var request=Ranged(ac:0);var magazine=new RepeatingFiveMagazine(2);
                var shot=RepeatingCrossbowShotRules.Resolve(seed,request,magazine,18);
                Require(shot.Legal&&shot.Attempted&&!shot.Attack.Attack.Hit&&shot.MagazineAfter.LoadedBolts==1
                    &&shot.DamageDice.Count==0&&shot.RandomStateAfter==shot.Attack.RandomStateAfter,
                    "A legal miss failed to spend one bolt or rolled damage dice."); });
            cases.Add("repeating_crossbow_critical_doubles_only_weapon_dice",()=>{
                uint seed=RangedSeed(20);var request=Ranged(ac:0);var shot=RepeatingCrossbowShotRules.Resolve(seed,request,new RepeatingFiveMagazine(1),0);
                var first=DiceStream.Draw(shot.Attack.RandomStateAfter,10);var second=DiceStream.Draw(first.NextState,10);
                Require(shot.Legal&&shot.Attack.Critical&&shot.DamageDice.Count==2&&shot.DamageDice[0]==first.Value+1
                    &&shot.DamageDice[1]==second.Value+1&&shot.RolledDamageBeforeDefense==shot.DamageDice[0]+shot.DamageDice[1]+3
                    &&shot.DamageModifier==3&&shot.MagazineAfter.LoadedBolts==0&&shot.RandomStateAfter==second.NextState,
                    "Critical did not double crossbow dice or added Dexterity more than once."); });
            cases.Add("repeating_crossbow_empty_magazine_with_carried_bolts_cannot_shoot",()=>{
                var magazine=new RepeatingFiveMagazine();var shot=RepeatingCrossbowShotRules.Resolve(42,Ranged(),magazine,20);
                Require(!shot.Legal&&!shot.Attempted&&shot.Failure==RepeatingCrossbowShotFailure.NoAmmunition
                    &&ReferenceEquals(shot.MagazineAfter,magazine)&&shot.CarriedBoltsAfter==20&&shot.Attack==null
                    &&shot.RandomStateAfter==42,"Carried spare bolts were treated as loaded ammunition or a die was consumed."); });
            cases.Add("repeating_crossbow_illegal_target_does_not_spend_magazine_or_randomness",()=>{
                foreach(var request in new[]{Ranged(distance:321),Ranged(cover:CombatCover.Total),Ranged(lineClear:false),Ranged(locationKnown:false)}) {
                    var magazine=new RepeatingFiveMagazine(2);var shot=RepeatingCrossbowShotRules.Resolve(43,request,magazine,18);
                    Require(!shot.Legal&&!shot.Attempted&&shot.MagazineAfter.LoadedBolts==2&&shot.CarriedBoltsAfter==18
                        &&shot.Attack==null&&shot.RandomStateAfter==43,"Illegal attack attempt spent ammunition or RNG.");}
            });
            cases.Add("repeating_crossbow_wrong_profile_and_invalid_inventory_fail_closed",()=>{
                var wrong=new RangedAttackRequest(10,100,400,12,3,2,true,0,CombatCover.None,true,true,true,false,false,new ConditionClauses(),new ConditionClauses());
                var magazine=new RepeatingFiveMagazine(2);var shot=RepeatingCrossbowShotRules.Resolve(44,wrong,magazine,20);
                Require(!shot.Legal&&shot.Failure==RepeatingCrossbowShotFailure.WrongWeaponRangeProfile
                    &&shot.MagazineAfter.LoadedBolts==2&&shot.RandomStateAfter==44,"Wrong source profile consumed state.");
                Throws<ArgumentOutOfRangeException>(()=>RepeatingCrossbowShotRules.Resolve(1,Ranged(),magazine,-1));
                Throws<ArgumentNullException>(()=>RepeatingCrossbowShotRules.Resolve(1,Ranged(),null,0)); });
            cases.Add("repeating_crossbow_flat_attack_bonus_does_not_change_damage_modifier",()=>{
                var request=new RangedAttackRequest(10,80,320,0,3,2,true,5,CombatCover.None,true,true,true,false,false,new ConditionClauses(),new ConditionClauses());
                var shot=RepeatingCrossbowShotRules.Resolve(RangedSeed(12),request,new RepeatingFiveMagazine(1),0);
                Require(shot.Legal&&shot.Attack.AttackModifier==10&&shot.DamageModifier==3
                    &&shot.RolledDamageBeforeDefense==shot.DamageDice[0]+3,"A flat attack bonus was incorrectly added to damage."); });
        }
    }
}
#endif
