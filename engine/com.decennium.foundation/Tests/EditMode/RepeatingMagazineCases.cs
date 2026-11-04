#if DECENNIUM_TEST_ONLY && (UNITY_EDITOR || HEADLESS_TESTS)
using System;
using System.Collections.Generic;
using Decennium.Foundation.Laboratory;

namespace Decennium.Foundation.Tests
{
    public static partial class FoundationCases
    {
        private static void AddRepeatingMagazineCases(Dictionary<string,Action> cases)
        {
            cases.Add("repeating5_magazine_starts_empty_and_empty_weapon_cannot_fire",()=>{
                var magazine=new RepeatingFiveMagazine();
                Require(magazine.LoadedBolts==0&&!magazine.CanFire&&!magazine.TrySpendForAttack(out var same)
                    &&ReferenceEquals(magazine,same),"Empty starting magazine fired or changed state."); });
            cases.Add("repeating5_load_moves_only_carried_bolts_up_to_capacity",()=>{
                var result=new RepeatingFiveMagazine().Reload(20,true);
                Require(result.Status==MagazineReloadStatus.Loaded&&result.BoltsLoaded==5&&result.Magazine.LoadedBolts==5
                    &&result.CarriedBoltsRemaining==15,"Reload created bolts or exceeded capacity."); });
            cases.Add("repeating5_each_attack_attempt_spends_one_bolt",()=>{
                var magazine=new RepeatingFiveMagazine(5);int attacks=0;
                while(magazine.TrySpendForAttack(out var next)){attacks++;magazine=next;}
                Require(attacks==5&&magazine.LoadedBolts==0&&!magazine.CanFire,"Magazine allowed a sixth attack or failed to spend a bolt."); });
            cases.Add("repeating5_partial_reload_uses_remaining_capacity_only",()=>{
                var result=new RepeatingFiveMagazine(3).Reload(20,true);
                Require(result.BoltsLoaded==2&&result.Magazine.LoadedBolts==5&&result.CarriedBoltsRemaining==18,
                    "Partial magazine reload exceeded physical capacity or lost carried bolts."); });
            cases.Add("repeating5_reload_requires_free_hand_and_preserves_inventory",()=>{
                var magazine=new RepeatingFiveMagazine(2);var result=magazine.Reload(20,false);
                Require(result.Status==MagazineReloadStatus.NoFreeLoadingHand&&ReferenceEquals(result.Magazine,magazine)
                    &&result.BoltsLoaded==0&&result.CarriedBoltsRemaining==20,"Reload without a free hand changed resources."); });
            cases.Add("repeating5_full_or_empty_stock_reload_fails_without_transfer",()=>{
                var full=new RepeatingFiveMagazine(5).Reload(20,true);var none=new RepeatingFiveMagazine().Reload(0,true);
                Require(full.Status==MagazineReloadStatus.MagazineFull&&full.BoltsLoaded==0&&full.CarriedBoltsRemaining==20
                    &&none.Status==MagazineReloadStatus.NoCarriedBolts&&none.Magazine.LoadedBolts==0,"Ineligible reload created or removed ammunition."); });
            cases.Add("repeating5_magazine_rejects_capacity_and_inventory_underflow",()=>{
                Throws<ArgumentOutOfRangeException>(()=>new RepeatingFiveMagazine(-1));
                Throws<ArgumentOutOfRangeException>(()=>new RepeatingFiveMagazine(6));
                Throws<ArgumentOutOfRangeException>(()=>new RepeatingFiveMagazine().Reload(-1,true)); });
        }
    }
}
#endif
