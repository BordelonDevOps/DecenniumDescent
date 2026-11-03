#if DECENNIUM_TEST_ONLY && (UNITY_EDITOR || DEVELOPMENT_BUILD || HEADLESS_TESTS)
using System;
namespace Decennium.Foundation.Laboratory {
    public static partial class PlaytestCharacters {
        // Exact prerequisite/tier/pool projection of the pinned character_foundation.json.
        // Source snapshot and projection validation live in 2026-11-03-engine-expansion evidence.
        private sealed class ClassProfile {
            internal readonly string[] Prerequisites;
            internal readonly WeaveTier Tier;
            internal readonly int[] Pools;
            internal ClassProfile(string[] prerequisites, WeaveTier tier, int[] pools)
            { Prerequisites = prerequisites; Tier = tier; Pools = pools; }
        }
        private static ClassProfile ClassProfileFor(string name) {
            switch (name) {
                case "Bard": return new ClassProfile(new[] { "CHA" }, WeaveTier.Hybrid, new[] { 2,3,5,7,9,11,14,17,20,23,26,29,32,35,38,41,44,47,50,54 });
                case "Cleric": return new ClassProfile(new[] { "WIS" }, WeaveTier.Full, new[] { 3,4,7,9,12,15,18,21,24,27,30,33,36,39,42,45,48,51,54,58 });
                case "Crimson Agent": return new ClassProfile(new[] { "DEX", "CON" }, WeaveTier.Hybrid, new[] { 2,2,4,5,6,8,9,11,12,14,15,17,18,20,21,23,24,26,27,29 });
                case "Dragoon": return new ClassProfile(new[] { "STR", "DEX" }, WeaveTier.Minor, new[] { 1,1,2,3,4,5,6,7,8,9,11,12,13,14,15,16,17,18,19,20 });
                case "Druid": return new ClassProfile(new[] { "WIS" }, WeaveTier.Full, new[] { 3,4,7,9,12,15,18,21,24,27,30,33,36,39,42,45,48,51,54,58 });
                case "Mage": return new ClassProfile(new[] { "INT" }, WeaveTier.Full, new[] { 3,5,8,10,14,17,20,23,26,29,32,35,38,41,44,47,50,53,56,60 });
                case "Mirrorsage": return new ClassProfile(new[] { "INT", "CHA" }, WeaveTier.Hybrid, new[] { 2,3,5,7,9,11,14,17,20,23,26,29,32,35,38,41,44,47,50,54 });
                case "Monk": return new ClassProfile(new[] { "DEX", "WIS" }, WeaveTier.Minor, new[] { 1,1,2,3,4,5,6,7,8,9,11,12,13,14,15,16,17,18,19,20 });
                case "Oracle": return new ClassProfile(new[] { "WIS", "CHA" }, WeaveTier.None, new[] { 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0 });
                case "Paladin": return new ClassProfile(new[] { "STR", "CHA" }, WeaveTier.Half, new[] { 1,2,3,4,6,8,10,12,14,16,18,20,22,24,26,28,30,32,34,36 });
                case "Ranger": return new ClassProfile(new[] { "DEX", "WIS" }, WeaveTier.Half, new[] { 1,2,3,4,6,8,10,12,14,16,18,20,22,24,26,28,30,32,34,36 });
                case "Shaman": return new ClassProfile(new[] { "WIS", "CON" }, WeaveTier.Hybrid, new[] { 3,4,7,9,12,15,18,21,24,27,30,33,36,39,42,45,48,51,54,58 });
                case "Soldier": return new ClassProfile(new[] { "STR", "CON" }, WeaveTier.None, new[] { 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0 });
                case "Thief": return new ClassProfile(new[] { "DEX" }, WeaveTier.Minor, new[] { 1,1,2,3,4,5,6,7,8,9,11,12,13,14,15,16,17,18,19,20 });
                case "Tinker": return new ClassProfile(new[] { "INT", "DEX" }, WeaveTier.Minor, new[] { 1,2,3,4,6,8,10,12,14,16,18,20,22,24,26,28,30,32,34,36 });
                case "Warrior": return new ClassProfile(new[] { "STR", "CON" }, WeaveTier.None, new[] { 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0 });
                case "Wizard": return new ClassProfile(new[] { "INT" }, WeaveTier.Full, new[] { 4,6,10,12,16,20,24,28,32,36,40,44,48,52,56,60,64,68,72,80 });
                default: throw new ArgumentException("Unknown Base class.", nameof(name));
            }
        }
    }
}
#endif
