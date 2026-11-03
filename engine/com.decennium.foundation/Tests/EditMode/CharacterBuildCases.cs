#if DECENNIUM_TEST_ONLY && (UNITY_EDITOR || HEADLESS_TESTS)
using System;
using System.Collections.Generic;
using System.Linq;
using Decennium.Foundation.Laboratory;

namespace Decennium.Foundation.Tests
{
    public static partial class FoundationCases
    {
        private static Dictionary<string,int> ClassLevels(params (string Name, int Level)[] pairs)
            => pairs.ToDictionary(p => p.Name, p => p.Level, StringComparer.Ordinal);
        private static CharacterAbilities AllScores(int value) => new CharacterAbilities(value,value,value,value,value,value);
        private static void AddCharacterBuildCases(Dictionary<string, Action> cases)
        {
            cases.Add("build_point_buy_source_arrays_and_unspent_budget", () => {
                Require(PlaytestCharacters.PointBuyCost(new[] {15,15,15,8,8,8}) == 27
                    && PlaytestCharacters.PointBuyCost(new[] {15,14,13,12,10,8}) == 27
                    && PlaytestCharacters.PointBuyCost(new[] {8,8,8,8,8,8}) == 0, "27 is a budget, not mandatory expenditure."); });
            cases.Add("build_point_buy_each_price", () => {
                int[] costs = {0,1,2,3,4,5,7,9};
                for (int score=8; score<=15; score++)
                    Require(PlaytestCharacters.PointBuyCost(new[] {score,8,8,8,8,8}) == costs[score-8], "Wrong nonlinear point price."); });
            cases.Add("build_point_buy_rejects_overspend_counts_ranges", () => {
                Throws<ArgumentException>(() => PlaytestCharacters.PointBuyCost(new[] {15,15,15,9,8,8}));
                foreach (int value in new[] {int.MinValue,7,16,int.MaxValue})
                    Throws<ArgumentOutOfRangeException>(() => PlaytestCharacters.PointBuyCost(new[] {value,8,8,8,8,8}));
                foreach (int count in new[] {0,5,7})
                    Throws<ArgumentException>(() => PlaytestCharacters.PointBuyCost(Enumerable.Repeat(8,count).ToArray()));
                Throws<ArgumentNullException>(() => PlaytestCharacters.PointBuyCost(null)); });
            cases.Add("build_class_levels_total_and_order", () => {
                var r = PlaytestCharacters.ValidateClassLevels(ClassLevels(("Mage",5),("Bard",5)),new[] {"Bard","Mage"});
                Require(r.TotalLevel == 10 && r.ProficiencyBonus == 4 && r.Levels["Mage"] == 5
                    && r.AcquisitionOrder.SequenceEqual(new[] {"Bard","Mage"}), "Use acquisition chronology, not dictionary ordering."); });
            cases.Add("build_class_levels_empty_and_combined_cap", () => {
                Throws<ArgumentException>(() => PlaytestCharacters.ValidateClassLevels(ClassLevels(),Array.Empty<string>()));
                Throws<ArgumentException>(() => PlaytestCharacters.ValidateClassLevels(ClassLevels(("Bard",11),("Mage",10)),new[] {"Bard","Mage"}));
                Require(PlaytestCharacters.ValidateClassLevels(ClassLevels(("Bard",10),("Mage",10)),new[] {"Bard","Mage"}).TotalLevel==20,"Level20 accepted."); });
            cases.Add("build_class_levels_invalid_individual_levels_and_names", () => {
                foreach (int n in new[] {int.MinValue,0,21,int.MaxValue})
                    Throws<ArgumentOutOfRangeException>(() => PlaytestCharacters.ValidateClassLevels(ClassLevels(("Bard",n)),new[] {"Bard"}));
                foreach (string name in new[] {"bard","Fighter","Swashbuckler","Bard "})
                    Throws<ArgumentException>(() => PlaytestCharacters.ValidateClassLevels(ClassLevels((name,1)),new[] {name})); });
            cases.Add("build_class_levels_exact_order_membership", () => {
                var levels=ClassLevels(("Cleric",6),("Druid",6));
                foreach (string[] order in new[] {new[]{"Cleric"},new[]{"Cleric","Cleric"},new[]{"Cleric","Wizard"},new[]{"Cleric","Druid","Druid"},new[]{"Cleric",null}})
                    Throws<ArgumentException>(() => PlaytestCharacters.ValidateClassLevels(levels,order));
                var insensitive = new Dictionary<string,int>(StringComparer.OrdinalIgnoreCase) { ["Bard"]=1 };
                Throws<ArgumentException>(() => PlaytestCharacters.ValidateClassLevels(insensitive,new[]{"bard"})); });
            cases.Add("build_class_levels_null_rejected", () => {
                Throws<ArgumentNullException>(() => PlaytestCharacters.ValidateClassLevels(null,new[]{"Bard"}));
                Throws<ArgumentNullException>(() => PlaytestCharacters.ValidateClassLevels(ClassLevels(("Bard",1)),null)); });
            cases.Add("build_class_levels_detached_readonly", () => {
                var levels=ClassLevels(("Bard",2)); var order=new[]{"Bard"};
                var r=PlaytestCharacters.ValidateClassLevels(levels,order);
                levels.Clear(); order[0]="Mage";
                Require(r.TotalLevel==2 && r.Levels["Bard"]==2 && r.AcquisitionOrder[0]=="Bard","Caller alias.");
                Throws<NotSupportedException>(()=>((IDictionary<string,int>)r.Levels)["Bard"]=9);
                Throws<NotSupportedException>(()=>((IList<string>)r.AcquisitionOrder)[0]="Mage"); });
            cases.Add("build_entry_source_all_pass_and_agent_constitution", () => {
                Require(PlaytestCharacters.NewClassPrerequisiteFailures(new[]{"Bard","Cleric"},"Crimson Agent",AllScores(13)).Count==0,"13 passes all gates.");
                var r=PlaytestCharacters.NewClassPrerequisiteFailures(new[]{"Bard"},"Crimson Agent",new CharacterAbilities(13,13,12,13,13,13));
                Require(r.Count==1 && r[0].ClassName=="Crimson Agent" && r[0].Ability=="CON" && r[0].Required==13 && r[0].Actual==12,"CON gate cannot become INT."); });
            cases.Add("build_entry_every_held_class_checked", () => {
                var r=PlaytestCharacters.NewClassPrerequisiteFailures(new[]{"Bard","Cleric"},"Mage",new CharacterAbilities(13,13,12,13,13,12));
                Require(r.Count==1 && r[0].ClassName=="Bard" && r[0].Ability=="CHA","Third-class entry still tests the first class."); });
            cases.Add("build_entry_all_failures_ordered_and_held_duplicates_deduplicated", () => {
                var r=PlaytestCharacters.NewClassPrerequisiteFailures(new[]{"Bard","Cleric","Bard"},"Crimson Agent",AllScores(int.MinValue));
                Require(r.Select(x=>x.ClassName+":"+x.Ability).SequenceEqual(new[]{"Bard:CHA","Cleric:WIS","Crimson Agent:DEX","Crimson Agent:CON"})
                    && r.All(x=>x.Actual==int.MinValue),"Report all gates in source order, once.");
                Throws<NotSupportedException>(()=>((IList<ClassPrerequisiteFailure>)r).Clear()); });
            cases.Add("build_entry_not_first_class_or_retention_or_existing_advancement", () => {
                Require(PlaytestCharacters.NewClassPrerequisiteFailures(Array.Empty<string>(),"Bard",null).Count==0
                    && PlaytestCharacters.NewClassPrerequisiteFailures(new[]{"Bard","Cleric"},"Bard",AllScores(1)).Count==0
                    && PlaytestCharacters.NewClassPrerequisiteFailures(new[]{"Bard"},"Bard",null).Count==0,"Only new-class entry needs scores."); });
            cases.Add("build_entry_unknown_names_validated_before_exemptions", () => {
                Throws<ArgumentException>(()=>PlaytestCharacters.NewClassPrerequisiteFailures(Array.Empty<string>(),"Fighter",null));
                Throws<ArgumentException>(()=>PlaytestCharacters.NewClassPrerequisiteFailures(new[]{"Bard","Fighter"},"Bard",null));
                Throws<ArgumentNullException>(()=>PlaytestCharacters.NewClassPrerequisiteFailures(null,"Bard",AllScores(13)));
                Throws<ArgumentNullException>(()=>PlaytestCharacters.NewClassPrerequisiteFailures(new[]{"Bard"},"Mage",null)); });
            cases.Add("build_abilities_exact_names", () => {
                var scores=new CharacterAbilities(1,2,3,4,5,6);
                Require(new[]{"STR","DEX","CON","INT","WIS","CHA"}.Select(x=>scores[x]).SequenceEqual(new[]{1,2,3,4,5,6}),"Ability mapping.");
                Throws<ArgumentException>(()=>{int unused=scores["str"];}); });
            cases.Add("build_rp_three_class_source_example", () => {
                var r=PlaytestCharacters.MergedRp(ClassLevels(("Cleric",6),("Druid",6),("Wizard",1)),new[]{"Druid","Cleric","Wizard"});
                Require(r.Maximum==19 && r.SecondaryBonus==4 && r.Primary.ClassName=="Druid" && r.Secondary.ClassName=="Cleric"
                    && r.NoncontributingWeaveClasses.Count==1 && r.NoncontributingWeaveClasses[0].ClassName=="Wizard","15+ceil(15/4), not a tertiary bonus."); });
            cases.Add("build_rp_tier_precedes_level_and_capacity_can_fall", () => {
                var before=PlaytestCharacters.MergedRp(ClassLevels(("Bard",10)),new[]{"Bard"});
                var after=PlaytestCharacters.MergedRp(ClassLevels(("Bard",10),("Wizard",1)),new[]{"Bard","Wizard"});
                Require(before.Maximum==23 && after.Maximum==10 && after.Primary.ClassName=="Wizard" && after.SecondaryBonus==6
                    && PlaytestCharacters.ClampAfterCapacityChange(20,after.Maximum)==10,"Full tier wins even though capacity falls."); });
            cases.Add("build_rp_level_precedes_pool_and_pool_precedes_acquisition", () => {
                var a=PlaytestCharacters.MergedRp(ClassLevels(("Cleric",4),("Wizard",3)),new[]{"Wizard","Cleric"});
                var b=PlaytestCharacters.MergedRp(ClassLevels(("Cleric",1),("Wizard",1)),new[]{"Cleric","Wizard"});
                Require(a.Primary.ClassName=="Cleric" && a.Maximum==12 && b.Primary.ClassName=="Wizard" && b.Maximum==5,"Sort precedence."); });
            cases.Add("build_rp_acquisition_tie_not_dictionary_order", () => {
                var r=PlaytestCharacters.MergedRp(ClassLevels(("Cleric",6),("Druid",6)),new[]{"Druid","Cleric"});
                Require(r.Primary.ClassName=="Druid" && r.Primary.AcquisitionIndex==0 && r.Secondary.AcquisitionIndex==1,"Acquisition breaks exact tie."); });
            cases.Add("build_rp_none_and_single_constituent", () => {
                var a=PlaytestCharacters.MergedRp(ClassLevels(("Oracle",10),("Soldier",5),("Warrior",5)),new[]{"Oracle","Soldier","Warrior"});
                var b=PlaytestCharacters.MergedRp(ClassLevels(("Bard",5),("Oracle",5)),new[]{"Oracle","Bard"});
                Require(a.Maximum==0 && a.Primary==null && a.Secondary==null && a.SecondaryBonus==0 && a.NoncontributingWeaveClasses.Count==0
                    && b.Maximum==9 && b.Primary.ClassName=="Bard" && b.Primary.AcquisitionIndex==1 && b.Secondary==null,"Non-Weave classes never contribute."); });
            cases.Add("build_rp_quarter_rounds_up", () => {
                int[] expected={1,1,2,2};
                for(int level=1;level<=4;level++) {
                    var r=PlaytestCharacters.MergedRp(ClassLevels(("Wizard",10),("Bard",level)),new[]{"Wizard","Bard"});
                    Require(r.SecondaryBonus==expected[level-1],"Ceiling of pools 2,3,5,7.");
                } });
            cases.Add("build_rp_result_detached_and_readonly", () => {
                var levels=ClassLevels(("Cleric",6),("Druid",6),("Wizard",1));var order=new[]{"Druid","Cleric","Wizard"};
                var r=PlaytestCharacters.MergedRp(levels,order);levels.Clear();order[0]="Bard";
                Require(r.Maximum==19 && r.Primary.ClassName=="Druid" && r.NoncontributingWeaveClasses[0].ClassLevel==1,"Caller mutation.");
                Throws<NotSupportedException>(()=>((IList<RpConstituent>)r.NoncontributingWeaveClasses).Clear()); });
            cases.Add("build_rp_rejects_invalid_build_including_none_tier", () => {
                Throws<ArgumentException>(()=>PlaytestCharacters.MergedRp(ClassLevels(("Oracle",20),("Soldier",1)),new[]{"Oracle","Soldier"}));
                Throws<ArgumentException>(()=>PlaytestCharacters.MergedRp(ClassLevels(("Wizard",1),("Bard",1)),new[]{"Wizard","Wizard"}));
                Throws<ArgumentNullException>(()=>PlaytestCharacters.MergedRp(null,Array.Empty<string>())); });
            AddCharacterProfileCases(cases);
        }
    }
}
#endif
