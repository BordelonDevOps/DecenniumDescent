#if DECENNIUM_TEST_ONLY && (UNITY_EDITOR || DEVELOPMENT_BUILD || HEADLESS_TESTS)
using System;
using System.Collections.Generic;
using System.Collections.ObjectModel;

namespace Decennium.Foundation.Laboratory
{
    /// <summary>A recorded class and HP base for one attained level, before Constitution.</summary>
    public readonly struct CharacterLevelRecord
    {
        public string ClassName { get; }
        public int BaseHp { get; }

        public CharacterLevelRecord(string className, int baseHp)
        {
            int die = PlaytestCharacters.HitDieForClass(className);
            if (baseHp < 1 || baseHp > die) throw new ArgumentOutOfRangeException(nameof(baseHp));
            ClassName = className;
            BaseHp = baseHp;
        }
    }

    /// <summary>
    /// Detached calculation, not an authoritative character or a final maximum-HP ledger.
    /// HitDiceBySize counts attained levels; it does not track, grant or refresh unspent dice.
    /// </summary>
    public sealed class CharacterHpResult
    {
        public long BaseMaximum { get; }
        public int TotalLevel => Levels.Count;
        public int ProficiencyBonus => PlaytestCharacters.ProficiencyBonus(TotalLevel);
        public IReadOnlyList<CharacterLevelRecord> Levels { get; }
        public IReadOnlyList<long> Contributions { get; }
        public IReadOnlyDictionary<int, int> HitDiceBySize { get; }

        internal CharacterHpResult(long baseMaximum, CharacterLevelRecord[] levels,
            long[] contributions, SortedDictionary<int, int> hitDice)
        {
            BaseMaximum = baseMaximum;
            // The calculator transfers ownership of fresh arrays/dictionary, never caller data.
            Levels = Array.AsReadOnly(levels);
            Contributions = Array.AsReadOnly(contributions);
            HitDiceBySize = new ReadOnlyDictionary<int, int>(hitDice);
        }
    }

    /// <summary>
    /// Provisional CHARACTER_CREATION_PLAYTEST.md numeric scope, CHR-01.
    /// Pure calculations: no grants, RNG, resource recovery, life-state changes or save writes.
    /// Sources/approval limits: docs/unity/evidence/2026-11-03-characters/SOURCE_BINDINGS.json.
    /// </summary>
    public static partial class PlaytestCharacters
    {
        // This arithmetic API accepts all int scores; generation/advancement legality is separate.
        public static int AbilityModifier(int score)
        {
            long difference = (long)score - 10;
            long quotient = difference / 2;
            if (difference < 0 && difference % 2 != 0) quotient--;
            return (int)quotient;
        }

        public static int ProficiencyBonus(int totalLevel)
        {
            if (totalLevel < 1 || totalLevel > 20) throw new ArgumentOutOfRangeException(nameof(totalLevel));
            return 2 + (totalLevel - 1) / 4;
        }

        // Exact name/hitDie projection of character_foundation.json /classes, pinned in evidence.
        // No aliases, caller-supplied die sizes or fallback class definitions.
        public static int HitDieForClass(string className)
        {
            if (className == null) throw new ArgumentNullException(nameof(className));
            switch (className)
            {
                case "Bard": return 8;
                case "Cleric": return 8;
                case "Crimson Agent": return 8;
                case "Dragoon": return 10;
                case "Druid": return 8;
                case "Mage": return 6;
                case "Mirrorsage": return 8;
                case "Monk": return 8;
                case "Oracle": return 6;
                case "Paladin": return 10;
                case "Ranger": return 8;
                case "Shaman": return 8;
                case "Soldier": return 10;
                case "Thief": return 8;
                case "Tinker": return 8;
                case "Warrior": return 12;
                case "Wizard": return 6;
                default: throw new ArgumentException("Unknown Base class.", nameof(className));
            }
        }

        /// <summary>Explicit fixed-average option for a later character level; does not choose it.</summary>
        public static int FixedHpBaseForClass(string className) => HitDieForClass(className) / 2 + 1;

        public static CharacterHpResult BaseMaximumHp(IReadOnlyList<CharacterLevelRecord> gainedLevels,
            int constitutionScore)
        {
            if (gainedLevels == null) throw new ArgumentNullException(nameof(gainedLevels));
            int count = gainedLevels.Count;
            if (count < 1 || count > 20)
                throw new ArgumentException("Record 1-20 chronological attained levels.", nameof(gainedLevels));

            var levels = new CharacterLevelRecord[count];
            var contributions = new long[count];
            var hitDice = new SortedDictionary<int, int>();
            int modifier = AbilityModifier(constitutionScore);
            long total = 0;
            for (int i = 0; i < count; i++)
            {
                CharacterLevelRecord level = gainedLevels[i];
                // Revalidate here as default(CharacterLevelRecord) bypasses its constructor.
                int die = HitDieForClass(level.ClassName);
                if (level.BaseHp < 1 || level.BaseHp > die || (i == 0 && level.BaseHp != die))
                    throw new ArgumentException("First character level uses maximum; later bases must fit the class die.",
                        nameof(gainedLevels));
                levels[i] = level;
                contributions[i] = Math.Max(1L, (long)level.BaseHp + modifier);
                total += contributions[i];
                hitDice.TryGetValue(die, out int previous);
                hitDice[die] = previous + 1;
            }
            return new CharacterHpResult(total, levels, contributions, hitDice);
        }

        /// <summary>
        /// Capacity-only clamp of a nonnegative current value. Does not heal or emit damage/healing
        /// triggers. The caller supplies the resolved maximum; HP effects/ledger are a separate rule.
        /// </summary>
        public static long ClampAfterCapacityChange(long current, long newMaximum)
        {
            if (current < 0) throw new ArgumentOutOfRangeException(nameof(current));
            if (newMaximum < 0) throw new ArgumentOutOfRangeException(nameof(newMaximum));
            return Math.Min(current, newMaximum);
        }
    }
}
#endif
