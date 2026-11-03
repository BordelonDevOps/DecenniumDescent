#if DECENNIUM_TEST_ONLY && (UNITY_EDITOR || DEVELOPMENT_BUILD || HEADLESS_TESTS)
using System;
using System.Collections.Generic;
using System.Collections.ObjectModel;

namespace Decennium.Foundation.Laboratory
{
    /// <summary>Six explicitly assigned scores. Generation and ancestry legality are separate.</summary>
    public sealed class CharacterAbilities
    {
        public int Strength { get; }
        public int Dexterity { get; }
        public int Constitution { get; }
        public int Intelligence { get; }
        public int Wisdom { get; }
        public int Charisma { get; }
        public CharacterAbilities(int strength, int dexterity, int constitution, int intelligence, int wisdom, int charisma)
        {
            Strength = strength; Dexterity = dexterity; Constitution = constitution;
            Intelligence = intelligence; Wisdom = wisdom; Charisma = charisma;
        }
        public int this[string ability] => ability switch {
            "STR" => Strength, "DEX" => Dexterity, "CON" => Constitution,
            "INT" => Intelligence, "WIS" => Wisdom, "CHA" => Charisma,
            _ => throw new ArgumentException("Unknown ability.", nameof(ability))
        };
    }

    public sealed class CharacterClassLevels
    {
        public int TotalLevel { get; }
        public int ProficiencyBonus => PlaytestCharacters.ProficiencyBonus(TotalLevel);
        public IReadOnlyDictionary<string, int> Levels { get; }
        public IReadOnlyList<string> AcquisitionOrder { get; }
        internal CharacterClassLevels(int total, Dictionary<string, int> levels, string[] order)
        {
            TotalLevel = total;
            Levels = new ReadOnlyDictionary<string, int>(levels);
            AcquisitionOrder = Array.AsReadOnly(order);
        }
    }

    public sealed class ClassPrerequisiteFailure
    {
        public string ClassName { get; }
        public string Ability { get; }
        public int Required => 13;
        public int Actual { get; }
        internal ClassPrerequisiteFailure(string name, string ability, int actual)
        { ClassName = name; Ability = ability; Actual = actual; }
    }

    public enum WeaveTier { None = 0, Minor = 1, Hybrid = 2, Half = 3, Full = 4 }

    public sealed class RpConstituent
    {
        public string ClassName { get; }
        public int ClassLevel { get; }
        public WeaveTier Tier { get; }
        public int Pool { get; }
        public int AcquisitionIndex { get; }
        internal RpConstituent(string name, int level, WeaveTier tier, int pool, int acquired)
        { ClassName = name; ClassLevel = level; Tier = tier; Pool = pool; AcquisitionIndex = acquired; }
    }

    /// <summary>Capacity calculation only: does not grant ranks, spell access or current RP.</summary>
    public sealed class MergedRpResult
    {
        public int Maximum { get; }
        public RpConstituent Primary { get; }
        public RpConstituent Secondary { get; }
        public int SecondaryBonus { get; }
        public IReadOnlyList<RpConstituent> NoncontributingWeaveClasses { get; }
        internal MergedRpResult(List<RpConstituent> ranked)
        {
            Primary = ranked.Count > 0 ? ranked[0] : null;
            Secondary = ranked.Count > 1 ? ranked[1] : null;
            SecondaryBonus = Secondary == null ? 0 : (Secondary.Pool + 3) / 4;
            Maximum = (Primary?.Pool ?? 0) + SecondaryBonus;
            NoncontributingWeaveClasses = Array.AsReadOnly(ranked.Count > 2
                ? ranked.GetRange(2, ranked.Count - 2).ToArray() : Array.Empty<RpConstituent>());
        }
    }

    /// <summary>CHR-02 source-defined calculators; no complete builder or grants are implied.</summary>
    public static partial class PlaytestCharacters
    {
        public static int PointBuyCost(IReadOnlyList<int> scores)
        {
            if (scores == null) throw new ArgumentNullException(nameof(scores));
            if (scores.Count != 6) throw new ArgumentException("Assign six pre-ancestry scores.", nameof(scores));
            int cost = 0;
            foreach (int score in scores) {
                if (score < 8 || score > 15) throw new ArgumentOutOfRangeException(nameof(scores));
                cost += score <= 13 ? score - 8 : score == 14 ? 7 : 9;
            }
            if (cost > 27) throw new ArgumentException("Point buy exceeds 27 points.", nameof(scores));
            return cost;
        }

        public static CharacterClassLevels ValidateClassLevels(IReadOnlyDictionary<string, int> classLevels,
            IReadOnlyList<string> acquisitionOrder)
        {
            if (classLevels == null) throw new ArgumentNullException(nameof(classLevels));
            if (acquisitionOrder == null) throw new ArgumentNullException(nameof(acquisitionOrder));
            if (classLevels.Count == 0 || classLevels.Count != acquisitionOrder.Count)
                throw new ArgumentException("Record every held class once in acquisition order.");
            var levels = new Dictionary<string, int>(StringComparer.Ordinal);
            long total = 0;
            foreach (var pair in classLevels) {
                HitDieForClass(pair.Key);
                if (pair.Value < 1 || pair.Value > 20) throw new ArgumentOutOfRangeException(nameof(classLevels));
                levels.Add(pair.Key, pair.Value);
                total += pair.Value;
            }
            if (total < 1 || total > 20) throw new ArgumentException("Combined level must be 1-20.", nameof(classLevels));
            var seen = new HashSet<string>(StringComparer.Ordinal);
            var order = new string[acquisitionOrder.Count];
            for (int i = 0; i < order.Length; i++) {
                string name = acquisitionOrder[i];
                if (name == null || !levels.ContainsKey(name) || !seen.Add(name))
                    throw new ArgumentException("Acquisition order must contain each held class exactly once.", nameof(acquisitionOrder));
                order[i] = name;
            }
            return new CharacterClassLevels((int)total, levels, order);
        }

        public static IReadOnlyList<ClassPrerequisiteFailure> NewClassPrerequisiteFailures(
            IReadOnlyList<string> heldClasses, string newClass, CharacterAbilities scores)
        {
            if (heldClasses == null) throw new ArgumentNullException(nameof(heldClasses));
            HitDieForClass(newClass);
            var names = new List<string>();
            var seen = new HashSet<string>(StringComparer.Ordinal);
            foreach (string name in heldClasses) {
                HitDieForClass(name);
                if (seen.Add(name)) names.Add(name);
            }
            // First class and advancement of an existing class do not run the entry gate.
            // Validate every supplied class before this early return, as the source does.
            if (names.Count == 0 || seen.Contains(newClass))
                return Array.AsReadOnly(Array.Empty<ClassPrerequisiteFailure>());
            if (scores == null) throw new ArgumentNullException(nameof(scores));
            names.Add(newClass);
            var failures = new List<ClassPrerequisiteFailure>();
            foreach (string name in names)
                foreach (string ability in ClassProfileFor(name).Prerequisites)
                    if (scores[ability] < 13) failures.Add(new ClassPrerequisiteFailure(name, ability, scores[ability]));
            return failures.AsReadOnly();
        }

        public static MergedRpResult MergedRp(IReadOnlyDictionary<string, int> classLevels,
            IReadOnlyList<string> acquisitionOrder)
        {
            CharacterClassLevels validated = ValidateClassLevels(classLevels, acquisitionOrder);
            var ranked = new List<RpConstituent>();
            for (int i = 0; i < validated.AcquisitionOrder.Count; i++) {
                string name = validated.AcquisitionOrder[i];
                ClassProfile profile = ClassProfileFor(name);
                if (profile.Tier == WeaveTier.None) continue;
                int level = validated.Levels[name];
                ranked.Add(new RpConstituent(name, level, profile.Tier, profile.Pools[level - 1], i));
            }
            ranked.Sort((a, b) => {
                int order = b.Tier.CompareTo(a.Tier);
                if (order == 0) order = b.ClassLevel.CompareTo(a.ClassLevel);
                if (order == 0) order = b.Pool.CompareTo(a.Pool);
                return order != 0 ? order : a.AcquisitionIndex.CompareTo(b.AcquisitionIndex);
            });
            return new MergedRpResult(ranked);
        }
    }
}
#endif
