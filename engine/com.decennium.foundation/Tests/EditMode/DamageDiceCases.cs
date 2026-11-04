#if DECENNIUM_TEST_ONLY && (UNITY_EDITOR || HEADLESS_TESTS)
using System;
using System.Collections.Generic;
using Decennium.Foundation.Laboratory;

namespace Decennium.Foundation.Tests
{
    public static partial class FoundationCases
    {
        private static void AddDamageDiceCases(Dictionary<string,Action> cases)
        {
            cases.Add("damage_dice_no_trigger_draws_nothing",()=>{
                var before=new LifeState(26,26,5);var r=PlaytestDamageDice.Resolve(before,4,T(0),1);
                Require(r.WordsConsumed==0&&r.NextRandomState==1&&r.WoundRoll==null&&r.InjuryD6==null&&r.StableD4==null&&r.Pending==null
                    &&r.Outcome.State.Hp==26&&r.Outcome.State.TemporaryHp==1,"Buffered damage consumed unnecessary dice."); });
            cases.Add("damage_dice_instant_death_precedes_all_dice_and_knockout",()=>{
                foreach(var before in new[]{new LifeState(26,1),new LifeState(26,0)}) {
                    var r=PlaytestDamageDice.Resolve(before,before.Hp+26,T(0),1,melee:true,knockout:KnockoutInstruction.AskIfEligible);
                    Require(r.Outcome.InstantDeath&&r.Outcome.State.Dead&&r.Pending==null&&r.WordsConsumed==0&&r.NextRandomState==1,"Instant Death offered prevention or drew dice.");} });
            cases.Add("damage_dice_exact_half_threshold_and_overlapping_triggers_roll_once",()=>{
                var below=PlaytestDamageDice.Resolve(new LifeState(25,25),12,T(0),1);
                var half=PlaytestDamageDice.Resolve(new LifeState(25,25),13,T(0),1,constitutionSaveModifier:20);
                var both=PlaytestDamageDice.Resolve(new LifeState(25,12),13,T(0),1,constitutionSaveModifier:20,maiming:true);
                Require(below.WoundRoll==null&&half.WoundRoll!=null&&both.WordsConsumed==half.WordsConsumed&&both.NextRandomState==half.NextRandomState
                    &&both.Outcome.WoundSaves==1,"Half threshold rounded down or overlapping triggers rerolled."); });
            cases.Add("damage_dice_failure_by_four_has_no_injury_draw",()=>{
                uint seed=SeedForDeath(6);var r=PlaytestDamageDice.Resolve(new LifeState(26,1),1,T(0),seed);
                Require(r.Outcome.State.Wounds.Count==1&&r.Outcome.State.Wounds[0]==Injury.None&&r.InjuryD6==null
                    &&r.NextRandomState==r.WoundRoll.NextRandomState,"Mild Wound failure drew an Injury."); });
            cases.Add("damage_dice_failure_by_five_draws_exactly_one_injury",()=>{
                uint seed=SeedForDeath(5);var r=PlaytestDamageDice.Resolve(new LifeState(26,1),1,T(0),seed);
                var draw=DiceStream.Draw(r.WoundRoll.NextRandomState,6);
                Require(r.InjuryD6==draw.Value+1&&r.NextRandomState==draw.NextState&&r.WordsConsumed==r.WoundRoll.WordsConsumed+draw.WordsConsumed
                    &&r.Outcome.State.Wounds.Count==1&&(int)r.Outcome.State.Wounds[0]==r.InjuryD6,"Wrong linked Injury draw or sequence."); });
            cases.Add("damage_dice_existing_three_wound_failure_is_fatal_without_injury_or_choice",()=>{
                var before=new LifeState(26,1,wounds:new[]{Injury.None,Injury.None,Injury.None});
                var r=PlaytestDamageDice.Resolve(before,1,T(0),SeedForDeath(1),melee:true,knockout:KnockoutInstruction.AskIfEligible);
                Require(r.Outcome.State.Dead&&r.Outcome.State.Wounds.Count==3&&r.InjuryD6==null&&r.Pending==null&&r.StableD4==null
                    &&r.NextRandomState==r.WoundRoll.NextRandomState,"Fatal Wounds created fourth Wound or knockout protection."); });
            cases.Add("damage_dice_third_new_wound_still_allows_knockout",()=>{
                var before=new LifeState(26,1,wounds:new[]{Injury.None,Injury.None});
                var r=PlaytestDamageDice.Resolve(before,1,T(1,3),SeedForDeath(9),melee:true,knockout:KnockoutInstruction.KnockOutIfEligible);
                Require(r.Outcome.State.Stable&&!r.Outcome.State.Dead&&r.Outcome.State.Wounds.Count==3&&r.InjuryD6==null
                    &&r.StableD4.HasValue&&r.Outcome.State.StableUntil==T(1,3).AddSeconds(r.StableD4.Value*3600L),"New third Wound incorrectly killed or rounded recovery."); });
            cases.Add("damage_dice_pending_choice_preserves_inputs_without_final_outcome",()=>{
                var before=new LifeState(26,1);var r=PlaytestDamageDice.Resolve(before,1,T(2,3),SeedForDeath(5),melee:true,knockout:KnockoutInstruction.AskIfEligible);
                Require(r.Pending!=null&&r.Outcome==null&&r.StableD4==null&&before.Hp==1&&before.Wounds.Count==0
                    &&r.Pending.Before==before&&r.Pending.At==T(2,3)&&r.Pending.NextRandomState==r.NextRandomState,"Pending branch exposed final life or changed original state."); });
            cases.Add("damage_dice_accept_knockout_draws_only_remaining_d4",()=>{
                var before=new LifeState(26,1);var first=PlaytestDamageDice.Resolve(before,1,T(2,3),SeedForDeath(5),melee:true,knockout:KnockoutInstruction.AskIfEligible);
                var r=first.Pending.Complete(true);var d4=DiceStream.Draw(first.NextRandomState,4);
                Require(r.Pending==null&&r.WoundRoll==first.WoundRoll&&r.InjuryD6==first.InjuryD6&&r.NextRandomState==d4.NextState
                    &&r.WordsConsumed==first.WordsConsumed+d4.WordsConsumed&&r.StableD4==d4.Value+1&&r.Outcome.State.Stable
                    &&r.Outcome.State.StableUntil==T(2,3).AddSeconds((d4.Value+1)*3600L),"Continuation rerolled paid results or lost exact deadline."); });
            cases.Add("damage_dice_ordinary_continuation_draws_nothing_more",()=>{
                var first=PlaytestDamageDice.Resolve(new LifeState(26,1),1,T(0),1,melee:true,knockout:KnockoutInstruction.AskIfEligible);
                var r=first.Pending.Complete(false);
                Require(r.Pending==null&&!r.Outcome.State.Stable&&!r.Outcome.State.Dead&&r.Outcome.State.Hp==0&&r.StableD4==null
                    &&r.NextRandomState==first.NextRandomState&&r.WordsConsumed==first.WordsConsumed,"Ordinary continuation rolled or treated dying as dead."); });
            cases.Add("damage_dice_conditional_instruction_and_late_choice_agree",()=>{
                var before=new LifeState(26,1,2);uint seed=SeedForDeath(3);
                var pending=PlaytestDamageDice.Resolve(before,3,T(1,7),seed,melee:true,knockout:KnockoutInstruction.AskIfEligible).Pending;
                foreach(bool choice in new[]{false,true}) {
                    var later=pending.Complete(choice);var early=PlaytestDamageDice.Resolve(before,3,T(1,7),seed,melee:true,
                        knockout:choice?KnockoutInstruction.KnockOutIfEligible:KnockoutInstruction.OrdinaryOutcome);
                    Require(later.NextRandomState==early.NextRandomState&&later.WordsConsumed==early.WordsConsumed&&later.StableD4==early.StableD4
                        &&later.Outcome.State.Stable==early.Outcome.State.Stable&&later.Outcome.State.StableUntil==early.Outcome.State.StableUntil
                        &&later.Outcome.State.Wounds.Count==early.Outcome.State.Wounds.Count,"Choice timing altered rolls or life outcome.");} });
            cases.Add("damage_dice_ordinary_creature_can_choose_knockout_before_ordinary_death",()=>{
                var r=PlaytestDamageDice.Resolve(new LifeState(26,1,usesDeathSaves:false),1,T(0),SeedForDeath(20),melee:true,knockout:KnockoutInstruction.AskIfEligible);
                Require(r.Pending!=null&&r.Pending.Complete(false).Outcome.State.Dead&&r.Pending.Complete(true).Outcome.State.Stable
                    &&!r.Pending.Complete(true).Outcome.State.UsesDeathSaves,"Ordinary death hid legal knockout choice or granted death saves."); });
            cases.Add("damage_dice_already_zero_cannot_be_knocked_out_again",()=>{
                var r=PlaytestDamageDice.Resolve(new LifeState(26,0),1,T(0),1,critical:true,melee:true,knockout:KnockoutInstruction.AskIfEligible);
                Require(r.Pending==null&&r.StableD4==null&&r.WordsConsumed==0&&r.Outcome.State.DeathFailures==2&&!r.Outcome.State.Stable,"Already-zero attack offered new knockout or extra dice."); });
            cases.Add("damage_dice_nonzero_result_does_not_draw_recovery",()=>{
                var r=PlaytestDamageDice.Resolve(new LifeState(26,26),1,T(0),1,melee:true,knockout:KnockoutInstruction.KnockOutIfEligible);
                Require(r.Pending==null&&r.StableD4==null&&r.WordsConsumed==0&&r.Outcome.State.Hp==25,"Conditional instruction became guaranteed knockout."); });
            cases.Add("damage_dice_maiming_can_trigger_without_hp_loss",()=>{
                var r=PlaytestDamageDice.Resolve(new LifeState(26,26,10),1,T(0),1,maiming:true);
                Require(r.WoundRoll!=null&&r.Outcome.State.Hp==26&&r.Outcome.State.TemporaryHp==9&&r.Outcome.State.Wounds.Count==1,"Maiming trigger was hidden by temporaryHP."); });
            cases.Add("damage_dice_wound_saves_have_no_natural_one_or_twenty_override",()=>{
                var fail=PlaytestDamageDice.Resolve(new LifeState(26,1),1,T(0),SeedForDeath(20),constitutionSaveModifier:-30);
                var pass=PlaytestDamageDice.Resolve(new LifeState(26,1),1,T(0),SeedForDeath(1),constitutionSaveModifier:30);
                Require(fail.Outcome.State.Wounds.Count==1&&fail.InjuryD6.HasValue&&pass.Outcome.State.Wounds.Count==0&&pass.InjuryD6==null,"Generic save acquired attack/death natural rules."); });
            cases.Add("damage_dice_large_damage_and_modifiers_remain_exact",()=>{
                var r=PlaytestDamageDice.Resolve(new LifeState(long.MaxValue,long.MaxValue),long.MaxValue,T(0),1,constitutionSaveModifier:int.MaxValue);
                Require(!r.Outcome.InstantDeath&&r.Outcome.WoundDc==long.MaxValue/2&&r.Outcome.State.Hp==0&&r.InjuryD6.HasValue,"Widened damage branch overflowed."); });
            cases.Add("damage_dice_invalid_inputs_reject_before_returning_a_result",()=>{
                var live=new LifeState(26,26);
                Throws<ArgumentException>(()=>PlaytestDamageDice.Resolve(null,0,T(0),1));Throws<ArgumentException>(()=>PlaytestDamageDice.Resolve(new LifeState(26,0,dead:true),1,T(0),1));
                Throws<ArgumentException>(()=>PlaytestDamageDice.Resolve(live,-1,T(0),1));Throws<ArgumentException>(()=>PlaytestDamageDice.Resolve(live,1,T(0),0));
                Throws<ArgumentException>(()=>PlaytestDamageDice.Resolve(live,1,T(0),1,knockout:(KnockoutInstruction)99));
                Throws<ArgumentException>(()=>PlaytestDamageDice.Resolve(live,1,T(0),1,knockout:KnockoutInstruction.KnockOutIfEligible)); });
            cases.Add("prototype_armor_uses_adopted_dexterity_modifier_with_negative_floor",()=>{
                Require(PrototypeArmor.UnarmoredBaseAc(10)==10&&PrototypeArmor.UnarmoredBaseAc(11)==10&&PrototypeArmor.UnarmoredBaseAc(12)==11
                    &&PrototypeArmor.UnarmoredBaseAc(9)==9&&PrototypeArmor.UnarmoredBaseAc(3)==6,"Adopted baseline or negative rounding differs.");
                Require(PrototypeArmor.UnarmoredBaseAc(int.MinValue)==-1073741819L&&PrototypeArmor.UnarmoredBaseAc(int.MaxValue)==1073741828L,"Arithmetic support overflowed; no creation legality implied."); });
        }
    }
}
#endif
