#if DECENNIUM_TEST_ONLY && (UNITY_EDITOR || HEADLESS_TESTS)
using System;
using System.Collections.Generic;
using System.Linq;
using Decennium.Foundation.Laboratory;
namespace Decennium.Foundation.Tests {
    public static partial class FoundationCases {
        // Literal source data, not values read from the runtime projection.
        private static void AddCharacterProfileCases(Dictionary<string,Action> cases) {
            cases.Add("build_profile_bard", () => {
                var expected = new[] { 2,3,5,7,9,11,14,17,20,23,26,29,32,35,38,41,44,47,50,54 };
                for(int level=1;level<=20;level++) {
                    var r=PlaytestCharacters.MergedRp(ClassLevels(("Bard",level)),new[]{"Bard"});
                    Require(r.Maximum==expected[level-1], "Bard source RP row at level " + level);
                    Require(r.Primary.Tier==WeaveTier.Hybrid && r.Primary.ClassLevel==level && r.Primary.Pool==expected[level-1], "Source tier and own class level.");
                }
                var f=PlaytestCharacters.NewClassPrerequisiteFailures(new[]{"Mage"},"Bard",AllScores(12)).Where(x=>x.ClassName=="Bard").ToArray();
                Require(f.Select(x=>x.Ability).SequenceEqual(new[]{"CHA"}) && f.All(x=>x.Required==13 && x.Actual==12),"Exact prerequisite gates.");
            });
            cases.Add("build_profile_cleric", () => {
                var expected = new[] { 3,4,7,9,12,15,18,21,24,27,30,33,36,39,42,45,48,51,54,58 };
                for(int level=1;level<=20;level++) {
                    var r=PlaytestCharacters.MergedRp(ClassLevels(("Cleric",level)),new[]{"Cleric"});
                    Require(r.Maximum==expected[level-1], "Cleric source RP row at level " + level);
                    Require(r.Primary.Tier==WeaveTier.Full && r.Primary.ClassLevel==level && r.Primary.Pool==expected[level-1], "Source tier and own class level.");
                }
                var f=PlaytestCharacters.NewClassPrerequisiteFailures(new[]{"Bard"},"Cleric",AllScores(12)).Where(x=>x.ClassName=="Cleric").ToArray();
                Require(f.Select(x=>x.Ability).SequenceEqual(new[]{"WIS"}) && f.All(x=>x.Required==13 && x.Actual==12),"Exact prerequisite gates.");
            });
            cases.Add("build_profile_crimson-agent", () => {
                var expected = new[] { 2,2,4,5,6,8,9,11,12,14,15,17,18,20,21,23,24,26,27,29 };
                for(int level=1;level<=20;level++) {
                    var r=PlaytestCharacters.MergedRp(ClassLevels(("Crimson Agent",level)),new[]{"Crimson Agent"});
                    Require(r.Maximum==expected[level-1], "Crimson Agent source RP row at level " + level);
                    Require(r.Primary.Tier==WeaveTier.Hybrid && r.Primary.ClassLevel==level && r.Primary.Pool==expected[level-1], "Source tier and own class level.");
                }
                var f=PlaytestCharacters.NewClassPrerequisiteFailures(new[]{"Bard"},"Crimson Agent",AllScores(12)).Where(x=>x.ClassName=="Crimson Agent").ToArray();
                Require(f.Select(x=>x.Ability).SequenceEqual(new[]{"DEX","CON"}) && f.All(x=>x.Required==13 && x.Actual==12),"Exact prerequisite gates.");
            });
            cases.Add("build_profile_dragoon", () => {
                var expected = new[] { 1,1,2,3,4,5,6,7,8,9,11,12,13,14,15,16,17,18,19,20 };
                for(int level=1;level<=20;level++) {
                    var r=PlaytestCharacters.MergedRp(ClassLevels(("Dragoon",level)),new[]{"Dragoon"});
                    Require(r.Maximum==expected[level-1], "Dragoon source RP row at level " + level);
                    Require(r.Primary.Tier==WeaveTier.Minor && r.Primary.ClassLevel==level && r.Primary.Pool==expected[level-1], "Source tier and own class level.");
                }
                var f=PlaytestCharacters.NewClassPrerequisiteFailures(new[]{"Bard"},"Dragoon",AllScores(12)).Where(x=>x.ClassName=="Dragoon").ToArray();
                Require(f.Select(x=>x.Ability).SequenceEqual(new[]{"STR","DEX"}) && f.All(x=>x.Required==13 && x.Actual==12),"Exact prerequisite gates.");
            });
            cases.Add("build_profile_druid", () => {
                var expected = new[] { 3,4,7,9,12,15,18,21,24,27,30,33,36,39,42,45,48,51,54,58 };
                for(int level=1;level<=20;level++) {
                    var r=PlaytestCharacters.MergedRp(ClassLevels(("Druid",level)),new[]{"Druid"});
                    Require(r.Maximum==expected[level-1], "Druid source RP row at level " + level);
                    Require(r.Primary.Tier==WeaveTier.Full && r.Primary.ClassLevel==level && r.Primary.Pool==expected[level-1], "Source tier and own class level.");
                }
                var f=PlaytestCharacters.NewClassPrerequisiteFailures(new[]{"Bard"},"Druid",AllScores(12)).Where(x=>x.ClassName=="Druid").ToArray();
                Require(f.Select(x=>x.Ability).SequenceEqual(new[]{"WIS"}) && f.All(x=>x.Required==13 && x.Actual==12),"Exact prerequisite gates.");
            });
            cases.Add("build_profile_mage", () => {
                var expected = new[] { 3,5,8,10,14,17,20,23,26,29,32,35,38,41,44,47,50,53,56,60 };
                for(int level=1;level<=20;level++) {
                    var r=PlaytestCharacters.MergedRp(ClassLevels(("Mage",level)),new[]{"Mage"});
                    Require(r.Maximum==expected[level-1], "Mage source RP row at level " + level);
                    Require(r.Primary.Tier==WeaveTier.Full && r.Primary.ClassLevel==level && r.Primary.Pool==expected[level-1], "Source tier and own class level.");
                }
                var f=PlaytestCharacters.NewClassPrerequisiteFailures(new[]{"Bard"},"Mage",AllScores(12)).Where(x=>x.ClassName=="Mage").ToArray();
                Require(f.Select(x=>x.Ability).SequenceEqual(new[]{"INT"}) && f.All(x=>x.Required==13 && x.Actual==12),"Exact prerequisite gates.");
            });
            cases.Add("build_profile_mirrorsage", () => {
                var expected = new[] { 2,3,5,7,9,11,14,17,20,23,26,29,32,35,38,41,44,47,50,54 };
                for(int level=1;level<=20;level++) {
                    var r=PlaytestCharacters.MergedRp(ClassLevels(("Mirrorsage",level)),new[]{"Mirrorsage"});
                    Require(r.Maximum==expected[level-1], "Mirrorsage source RP row at level " + level);
                    Require(r.Primary.Tier==WeaveTier.Hybrid && r.Primary.ClassLevel==level && r.Primary.Pool==expected[level-1], "Source tier and own class level.");
                }
                var f=PlaytestCharacters.NewClassPrerequisiteFailures(new[]{"Bard"},"Mirrorsage",AllScores(12)).Where(x=>x.ClassName=="Mirrorsage").ToArray();
                Require(f.Select(x=>x.Ability).SequenceEqual(new[]{"INT","CHA"}) && f.All(x=>x.Required==13 && x.Actual==12),"Exact prerequisite gates.");
            });
            cases.Add("build_profile_monk", () => {
                var expected = new[] { 1,1,2,3,4,5,6,7,8,9,11,12,13,14,15,16,17,18,19,20 };
                for(int level=1;level<=20;level++) {
                    var r=PlaytestCharacters.MergedRp(ClassLevels(("Monk",level)),new[]{"Monk"});
                    Require(r.Maximum==expected[level-1], "Monk source RP row at level " + level);
                    Require(r.Primary.Tier==WeaveTier.Minor && r.Primary.ClassLevel==level && r.Primary.Pool==expected[level-1], "Source tier and own class level.");
                }
                var f=PlaytestCharacters.NewClassPrerequisiteFailures(new[]{"Bard"},"Monk",AllScores(12)).Where(x=>x.ClassName=="Monk").ToArray();
                Require(f.Select(x=>x.Ability).SequenceEqual(new[]{"DEX","WIS"}) && f.All(x=>x.Required==13 && x.Actual==12),"Exact prerequisite gates.");
            });
            cases.Add("build_profile_oracle", () => {
                var expected = new[] { 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0 };
                for(int level=1;level<=20;level++) {
                    var r=PlaytestCharacters.MergedRp(ClassLevels(("Oracle",level)),new[]{"Oracle"});
                    Require(r.Maximum==expected[level-1], "Oracle source RP row at level " + level);
                }
                var f=PlaytestCharacters.NewClassPrerequisiteFailures(new[]{"Bard"},"Oracle",AllScores(12)).Where(x=>x.ClassName=="Oracle").ToArray();
                Require(f.Select(x=>x.Ability).SequenceEqual(new[]{"WIS","CHA"}) && f.All(x=>x.Required==13 && x.Actual==12),"Exact prerequisite gates.");
            });
            cases.Add("build_profile_paladin", () => {
                var expected = new[] { 1,2,3,4,6,8,10,12,14,16,18,20,22,24,26,28,30,32,34,36 };
                for(int level=1;level<=20;level++) {
                    var r=PlaytestCharacters.MergedRp(ClassLevels(("Paladin",level)),new[]{"Paladin"});
                    Require(r.Maximum==expected[level-1], "Paladin source RP row at level " + level);
                    Require(r.Primary.Tier==WeaveTier.Half && r.Primary.ClassLevel==level && r.Primary.Pool==expected[level-1], "Source tier and own class level.");
                }
                var f=PlaytestCharacters.NewClassPrerequisiteFailures(new[]{"Bard"},"Paladin",AllScores(12)).Where(x=>x.ClassName=="Paladin").ToArray();
                Require(f.Select(x=>x.Ability).SequenceEqual(new[]{"STR","CHA"}) && f.All(x=>x.Required==13 && x.Actual==12),"Exact prerequisite gates.");
            });
            cases.Add("build_profile_ranger", () => {
                var expected = new[] { 1,2,3,4,6,8,10,12,14,16,18,20,22,24,26,28,30,32,34,36 };
                for(int level=1;level<=20;level++) {
                    var r=PlaytestCharacters.MergedRp(ClassLevels(("Ranger",level)),new[]{"Ranger"});
                    Require(r.Maximum==expected[level-1], "Ranger source RP row at level " + level);
                    Require(r.Primary.Tier==WeaveTier.Half && r.Primary.ClassLevel==level && r.Primary.Pool==expected[level-1], "Source tier and own class level.");
                }
                var f=PlaytestCharacters.NewClassPrerequisiteFailures(new[]{"Bard"},"Ranger",AllScores(12)).Where(x=>x.ClassName=="Ranger").ToArray();
                Require(f.Select(x=>x.Ability).SequenceEqual(new[]{"DEX","WIS"}) && f.All(x=>x.Required==13 && x.Actual==12),"Exact prerequisite gates.");
            });
            cases.Add("build_profile_shaman", () => {
                var expected = new[] { 3,4,7,9,12,15,18,21,24,27,30,33,36,39,42,45,48,51,54,58 };
                for(int level=1;level<=20;level++) {
                    var r=PlaytestCharacters.MergedRp(ClassLevels(("Shaman",level)),new[]{"Shaman"});
                    Require(r.Maximum==expected[level-1], "Shaman source RP row at level " + level);
                    Require(r.Primary.Tier==WeaveTier.Hybrid && r.Primary.ClassLevel==level && r.Primary.Pool==expected[level-1], "Source tier and own class level.");
                }
                var f=PlaytestCharacters.NewClassPrerequisiteFailures(new[]{"Bard"},"Shaman",AllScores(12)).Where(x=>x.ClassName=="Shaman").ToArray();
                Require(f.Select(x=>x.Ability).SequenceEqual(new[]{"WIS","CON"}) && f.All(x=>x.Required==13 && x.Actual==12),"Exact prerequisite gates.");
            });
            cases.Add("build_profile_soldier", () => {
                var expected = new[] { 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0 };
                for(int level=1;level<=20;level++) {
                    var r=PlaytestCharacters.MergedRp(ClassLevels(("Soldier",level)),new[]{"Soldier"});
                    Require(r.Maximum==expected[level-1], "Soldier source RP row at level " + level);
                }
                var f=PlaytestCharacters.NewClassPrerequisiteFailures(new[]{"Bard"},"Soldier",AllScores(12)).Where(x=>x.ClassName=="Soldier").ToArray();
                Require(f.Select(x=>x.Ability).SequenceEqual(new[]{"STR","CON"}) && f.All(x=>x.Required==13 && x.Actual==12),"Exact prerequisite gates.");
            });
            cases.Add("build_profile_thief", () => {
                var expected = new[] { 1,1,2,3,4,5,6,7,8,9,11,12,13,14,15,16,17,18,19,20 };
                for(int level=1;level<=20;level++) {
                    var r=PlaytestCharacters.MergedRp(ClassLevels(("Thief",level)),new[]{"Thief"});
                    Require(r.Maximum==expected[level-1], "Thief source RP row at level " + level);
                    Require(r.Primary.Tier==WeaveTier.Minor && r.Primary.ClassLevel==level && r.Primary.Pool==expected[level-1], "Source tier and own class level.");
                }
                var f=PlaytestCharacters.NewClassPrerequisiteFailures(new[]{"Bard"},"Thief",AllScores(12)).Where(x=>x.ClassName=="Thief").ToArray();
                Require(f.Select(x=>x.Ability).SequenceEqual(new[]{"DEX"}) && f.All(x=>x.Required==13 && x.Actual==12),"Exact prerequisite gates.");
            });
            cases.Add("build_profile_tinker", () => {
                var expected = new[] { 1,2,3,4,6,8,10,12,14,16,18,20,22,24,26,28,30,32,34,36 };
                for(int level=1;level<=20;level++) {
                    var r=PlaytestCharacters.MergedRp(ClassLevels(("Tinker",level)),new[]{"Tinker"});
                    Require(r.Maximum==expected[level-1], "Tinker source RP row at level " + level);
                    Require(r.Primary.Tier==WeaveTier.Minor && r.Primary.ClassLevel==level && r.Primary.Pool==expected[level-1], "Source tier and own class level.");
                }
                var f=PlaytestCharacters.NewClassPrerequisiteFailures(new[]{"Bard"},"Tinker",AllScores(12)).Where(x=>x.ClassName=="Tinker").ToArray();
                Require(f.Select(x=>x.Ability).SequenceEqual(new[]{"INT","DEX"}) && f.All(x=>x.Required==13 && x.Actual==12),"Exact prerequisite gates.");
            });
            cases.Add("build_profile_warrior", () => {
                var expected = new[] { 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0 };
                for(int level=1;level<=20;level++) {
                    var r=PlaytestCharacters.MergedRp(ClassLevels(("Warrior",level)),new[]{"Warrior"});
                    Require(r.Maximum==expected[level-1], "Warrior source RP row at level " + level);
                }
                var f=PlaytestCharacters.NewClassPrerequisiteFailures(new[]{"Bard"},"Warrior",AllScores(12)).Where(x=>x.ClassName=="Warrior").ToArray();
                Require(f.Select(x=>x.Ability).SequenceEqual(new[]{"STR","CON"}) && f.All(x=>x.Required==13 && x.Actual==12),"Exact prerequisite gates.");
            });
            cases.Add("build_profile_wizard", () => {
                var expected = new[] { 4,6,10,12,16,20,24,28,32,36,40,44,48,52,56,60,64,68,72,80 };
                for(int level=1;level<=20;level++) {
                    var r=PlaytestCharacters.MergedRp(ClassLevels(("Wizard",level)),new[]{"Wizard"});
                    Require(r.Maximum==expected[level-1], "Wizard source RP row at level " + level);
                    Require(r.Primary.Tier==WeaveTier.Full && r.Primary.ClassLevel==level && r.Primary.Pool==expected[level-1], "Source tier and own class level.");
                }
                var f=PlaytestCharacters.NewClassPrerequisiteFailures(new[]{"Bard"},"Wizard",AllScores(12)).Where(x=>x.ClassName=="Wizard").ToArray();
                Require(f.Select(x=>x.Ability).SequenceEqual(new[]{"INT"}) && f.All(x=>x.Required==13 && x.Actual==12),"Exact prerequisite gates.");
            });
        }
    }
}
#endif
