#if DECENNIUM_TEST_ONLY && (UNITY_EDITOR || DEVELOPMENT_BUILD || HEADLESS_TESTS)
using System;
using System.Collections.Generic;
using System.Collections.ObjectModel;
using System.Linq;
using System.Numerics;

namespace Decennium.Foundation.Laboratory
{
    /// <summary>Exact physical time plus the source's ordered phase at that instant.
    /// It does not choose or schedule a creature's deadline.</summary>
    public readonly struct EffectClockMarker : IComparable<EffectClockMarker>, IEquatable<EffectClockMarker>
    {
        public const int EndEffectApplication = 10, EndEffectExpiry = 20, NextEvent = 30;
        public RuleTime Time { get; }
        public int Phase { get; }
        public EffectClockMarker(RuleTime time, int phase = 0)
        { if (phase < 0) throw new ArgumentOutOfRangeException(nameof(phase)); Time = time; Phase = phase; }
        public int CompareTo(EffectClockMarker other)
        { int order = Time.CompareTo(other.Time); return order != 0 ? order : Phase.CompareTo(other.Phase); }
        public bool Equals(EffectClockMarker other) => Time == other.Time && Phase == other.Phase;
        public override bool Equals(object obj) => obj is EffectClockMarker other && Equals(other);
        public override int GetHashCode() => unchecked(Time.GetHashCode() * 397 ^ Phase);
    }

    public enum MaximumHpSource
    { Ribcrusher, BoneBreakingStrike, DeathlessSilence, FleshWarden, Conjuration, FleshAscendant,
      FamiliarBond, Tenacity, Tough, ToughAsNails, DarkFortitude }
    public enum CompletedRestKind { Short, Long }

    /// <summary>Retained numerical provenance. Eligibility, acquisition and actual controller/gear
    /// are caller responsibilities. Dynamic level changes require a new value; snapshots stay fixed.</summary>
    public sealed class MaximumHpMagnitude
    {
        public MaximumHpSource Source { get; }
        public long Amount { get; }
        public int? CharacterLevel { get; }
        public int? WarriorLevel { get; }
        public int? WizardLevel { get; }
        public int? AcquisitionLevel { get; }
        public int? CreationWizardLevel { get; }
        public int? Scale { get; }
        public long? Modifier { get; }
        public MaximumHpMagnitude(MaximumHpSource source, int? characterLevel = null, int? warriorLevel = null,
            int? wizardLevel = null, int? acquisitionLevel = null, int? creationWizardLevel = null,
            int? scale = null, long? modifier = null)
        {
            if (!Enum.IsDefined(typeof(MaximumHpSource), source)) throw new ArgumentException("Unsupported maximum-HP source.");
            foreach (int? level in new[] { characterLevel, warriorLevel, wizardLevel, acquisitionLevel, creationWizardLevel })
                if (level.HasValue && (level < 1 || level > 20)) throw new ArgumentOutOfRangeException(nameof(characterLevel));
            if (scale.HasValue && (scale < 1 || scale > 4) || modifier.HasValue && modifier < 1)
                throw new ArgumentException("Invalid Monk magnitude inputs.");
            Source = source; CharacterLevel = characterLevel; WarriorLevel = warriorLevel; WizardLevel = wizardLevel;
            AcquisitionLevel = acquisitionLevel; CreationWizardLevel = creationWizardLevel; Scale = scale; Modifier = modifier;
            if (PlaytestMaximumHp.IsTrauma(source)) {
                if (!scale.HasValue || !modifier.HasValue) throw new ArgumentException("Monk trauma requires S and M snapshots.");
                int coefficient = source == MaximumHpSource.Ribcrusher ? 1 : source == MaximumHpSource.BoneBreakingStrike ? 2 : 4;
                Amount = checked(coefficient * (long)scale.Value + modifier.Value); return;
            }
            switch (source) {
                case MaximumHpSource.FleshWarden: Amount = 2 * Required(warriorLevel); break;
                case MaximumHpSource.Conjuration: Amount = Required(creationWizardLevel); break;
                case MaximumHpSource.FleshAscendant: Amount = 2 * Required(wizardLevel); break;
                case MaximumHpSource.Tough:
                    int current = Required(characterLevel), acquired = Required(acquisitionLevel);
                    if (acquired > current) throw new ArgumentException("Acquisition snapshot exceeds current character level.");
                    Amount = 2 * acquired; break;
                case MaximumHpSource.FamiliarBond: case MaximumHpSource.Tenacity: Amount = Required(characterLevel); break;
                default: Amount = 2 * Required(characterLevel); break;
            }
        }
        private static int Required(int? level) => level ?? throw new ArgumentException("Required source level snapshot is missing.");
    }

    /// <summary>One actual effect application, not one row per textual alias. In particular the
    /// Flesh Ascendant engine/card aliases must enter as the same application identity.</summary>
    public sealed class MaximumHpApplication
    {
        public string Id { get; }
        public string Owner { get; }
        public string Target { get; }
        public MaximumHpMagnitude Magnitude { get; }
        public MaximumHpSource Source => Magnitude.Source;
        public long Amount => Magnitude.Amount;
        public string Group => PlaytestMaximumHp.IsTrauma(Source) ? "monk-trauma-global" : PlaytestMaximumHp.SourceId(Source);
        public EffectClockMarker Starts { get; }
        public EffectClockMarker? Expires { get; }
        public bool Present { get; }
        public bool Suppressed { get; }
        public bool EndsOnCompletedRest { get; }
        public string EndedReason { get; }
        public MaximumHpApplication(string id, string owner, string target, MaximumHpMagnitude magnitude,
            EffectClockMarker starts = default, EffectClockMarker? expires = null, bool present = true,
            bool suppressed = false, bool endsOnCompletedRest = false, string endedReason = null)
        {
            PlaytestMaximumHp.Identity(id); PlaytestMaximumHp.Identity(owner); PlaytestMaximumHp.Identity(target);
            if (magnitude == null) throw new ArgumentNullException(nameof(magnitude));
            if (expires.HasValue && expires.Value.CompareTo(starts) <= 0) throw new ArgumentException("Expiry must follow application.");
            bool trauma = PlaytestMaximumHp.IsTrauma(magnitude.Source);
            if (endsOnCompletedRest && !trauma || trauma && !endsOnCompletedRest && !expires.HasValue)
                throw new ArgumentException("Only Monk trauma has the supplied rest endpoint, and trauma needs a legal endpoint.");
            if (present && endedReason != null) throw new ArgumentException("A present effect cannot have an ended reason.");
            Id = id; Owner = owner; Target = target; Magnitude = magnitude; Starts = starts; Expires = expires;
            Present = present; Suppressed = suppressed; EndsOnCompletedRest = endsOnCompletedRest; EndedReason = endedReason;
        }
        public bool Operative(EffectClockMarker now) => Present && !Suppressed && Starts.CompareTo(now) <= 0
            && (!Expires.HasValue || now.CompareTo(Expires.Value) < 0);
        public MaximumHpApplication WithSuppression(bool suppressed) => new MaximumHpApplication(Id, Owner, Target,
            Magnitude, Starts, Expires, Present, suppressed, EndsOnCompletedRest, EndedReason);
        public MaximumHpApplication Remove(string reason)
        { PlaytestMaximumHp.Identity(reason); return new MaximumHpApplication(Id, Owner, Target, Magnitude,
            Starts, Expires, false, Suppressed, EndsOnCompletedRest, reason); }
    }

    public sealed class MaximumHpCalculation
    {
        public long BaseMaximum { get; }
        public BigInteger AdditiveBonuses { get; }
        public long MonkTraumaReduction { get; }
        public BigInteger PreSystemicMaximum { get; }
        public long EffectiveMaximum { get; }
        public IReadOnlyDictionary<string, string> SelectedApplications { get; }
        internal MaximumHpCalculation(long original, BigInteger bonuses, long trauma, BigInteger pre, long maximum,
            IDictionary<string, MaximumHpApplication> selected)
        {
            BaseMaximum = original; AdditiveBonuses = bonuses; MonkTraumaReduction = trauma;
            PreSystemicMaximum = pre; EffectiveMaximum = maximum;
            SelectedApplications = new ReadOnlyDictionary<string, string>(selected.ToDictionary(x => x.Key, x => x.Value.Id, StringComparer.Ordinal));
        }
    }

    public sealed class MaximumHpChange
    {
        public MaximumHpCalculation Calculation { get; }
        public LifeState State { get; }
        public long CapacityClamp { get; }
        public long ActualHpDamage => 0;
        public long ActualHpGained => 0;
        public int WoundSaves => 0;
        public int DeathFailuresAdded => 0;
        internal MaximumHpChange(MaximumHpCalculation calculation, LifeState before)
        { Calculation = calculation; State = PlaytestMaximumHp.ApplyCapacity(before, calculation.EffectiveMaximum); CapacityClamp = before.Hp - State.Hp; }
    }

    public enum HpThresholdRelation { Below, AtOrBelow, Above, AtOrAbove }
    public enum HpChangeKind { Damage, DirectHpLoss, Healing, CapacityChange }
    public readonly struct HpFraction
    {
        private readonly long denominator;
        public long Numerator { get; }
        public long Denominator => denominator == 0 ? 1 : denominator;
        public HpFraction(long numerator, long denominator)
        {
            if (denominator < 1 || numerator < 0 || numerator > denominator) throw new ArgumentException("Threshold fraction must be within zero and one.");
            long divisor = (long)BigInteger.GreatestCommonDivisor(numerator, denominator);
            Numerator = numerator / divisor; this.denominator = denominator / divisor;
        }
        public static HpFraction Quarter => new HpFraction(1, 4);
        public static HpFraction Half => new HpFraction(1, 2);
    }

    /// <summary>Frozen event-effective maximum and normal-HP values; not a permission or use counter.
    /// Capacity snapshots use a comparison maximum encompassing both values, never a damage event.</summary>
    public sealed class HpEventSnapshot
    {
        public string Id { get; }
        public long BeforeHp { get; }
        public long AfterHp { get; }
        public long EffectiveMaximum { get; }
        public HpChangeKind Kind { get; }
        public HpEventSnapshot(string id, long beforeHp, long afterHp, long effectiveMaximum, HpChangeKind kind)
        {
            PlaytestMaximumHp.Identity(id); PlaytestMaximumHp.Hp(beforeHp, effectiveMaximum); PlaytestMaximumHp.Hp(afterHp, effectiveMaximum);
            if (!Enum.IsDefined(typeof(HpChangeKind), kind) || (kind == HpChangeKind.Damage || kind == HpChangeKind.DirectHpLoss) && afterHp > beforeHp
                || kind == HpChangeKind.Healing && afterHp < beforeHp) throw new ArgumentException("Invalid HP event direction/kind.");
            Id = id; BeforeHp = beforeHp; AfterHp = afterHp; EffectiveMaximum = effectiveMaximum; Kind = kind;
        }
        public bool FallsAcross(HpFraction fraction, bool inclusive = true)
        {
            var relation = inclusive ? HpThresholdRelation.AtOrBelow : HpThresholdRelation.Below;
            return (Kind == HpChangeKind.Damage || Kind == HpChangeKind.DirectHpLoss) && AfterHp < BeforeHp
                && !PlaytestMaximumHp.Threshold(BeforeHp, EffectiveMaximum, fraction, relation)
                && PlaytestMaximumHp.Threshold(AfterHp, EffectiveMaximum, fraction, relation);
        }
        public bool HealedAboveHalf => Kind == HpChangeKind.Healing && AfterHp > BeforeHp
            && PlaytestMaximumHp.Threshold(AfterHp, EffectiveMaximum, HpFraction.Half, HpThresholdRelation.Above);
        public bool DamageLeftBelowHalf => Kind == HpChangeKind.Damage && AfterHp < BeforeHp
            && PlaytestMaximumHp.Threshold(AfterHp, EffectiveMaximum, HpFraction.Half);
    }

    /// <summary>Reviewed bounded maximum-HP ledger and threshold predicates. No feat acquisition,
    /// companion lifecycle, Ki payment, lethal track transition, event dispatch or persistence host.</summary>
    public static class PlaytestMaximumHp
    {
        internal static void Identity(string id) { if (string.IsNullOrWhiteSpace(id)) throw new ArgumentException("Nonempty identity required."); }
        internal static void Hp(long hp, long maximum) { if (maximum < 1 || hp < 0 || hp > maximum) throw new ArgumentOutOfRangeException(nameof(hp)); }
        internal static bool IsTrauma(MaximumHpSource source) => source == MaximumHpSource.Ribcrusher || source == MaximumHpSource.BoneBreakingStrike || source == MaximumHpSource.DeathlessSilence;
        public static string SourceId(MaximumHpSource source)
        {
            switch (source) {
                case MaximumHpSource.Ribcrusher: return "monk.hero.iron-fist-master.ribcrusher-strike";
                case MaximumHpSource.BoneBreakingStrike: return "monk.hero.iron-fist-master.bone-breaking-strike";
                case MaximumHpSource.DeathlessSilence: return "monk.hero.way-of-shadow.deathless-silence";
                case MaximumHpSource.FleshWarden: return "warrior.supplement.flesh-warden";
                case MaximumHpSource.Conjuration: return "wizard.engine[10]";
                case MaximumHpSource.FleshAscendant: return "wizard.hero.necromancer.flesh-ascendant";
                case MaximumHpSource.FamiliarBond: return "feat:familiar_bond";
                case MaximumHpSource.Tenacity: return "feat:tenacity";
                case MaximumHpSource.Tough: return "feat:tough";
                case MaximumHpSource.ToughAsNails: return "feat:tough_as_nails";
                case MaximumHpSource.DarkFortitude: return "feat:dark_fortitude";
                default: throw new ArgumentException("Unreviewed maximum-HP source.");
            }
        }
        public static MaximumHpSource SourceFromId(string source)
        {
            if (source == "wizard.engine[24]") return MaximumHpSource.FleshAscendant;
            foreach (MaximumHpSource value in Enum.GetValues(typeof(MaximumHpSource))) if (SourceId(value) == source) return value;
            throw new ArgumentException("Unreviewed maximum-HP source.");
        }
        private static MaximumHpApplication[] Records(IEnumerable<MaximumHpApplication> records)
        {
            if (records == null) throw new ArgumentNullException(nameof(records));
            var rows = records.ToArray(); var ids = new HashSet<string>(StringComparer.Ordinal);
            if (rows.Any(x => x == null || !ids.Add(x.Id))) throw new ArgumentException("Null or duplicate maximum-HP application.");
            return rows;
        }
        public static MaximumHpCalculation Calculate(long baseMaximum, IEnumerable<MaximumHpApplication> records, string target,
            EffectClockMarker now = default, int expedition = 0, int exhaustion = 0)
        {
            if (baseMaximum < 1) throw new ArgumentOutOfRangeException(nameof(baseMaximum));
            Identity(target); var rows = Records(records);
            var selected = new SortedDictionary<string, MaximumHpApplication>(StringComparer.Ordinal);
            foreach (var row in rows.Where(x => x.Target == target && x.Operative(now))) {
                if (!selected.TryGetValue(row.Group, out var old) || row.Amount > old.Amount
                    || row.Amount == old.Amount && (row.Starts.CompareTo(old.Starts) < 0
                    || row.Starts.Equals(old.Starts) && string.CompareOrdinal(row.Id, old.Id) < 0)) selected[row.Group] = row;
            }
            BigInteger bonuses = 0; long trauma = 0;
            foreach (var row in selected.Values) { if (IsTrauma(row.Source)) trauma = row.Amount; else bonuses += row.Amount; }
            BigInteger pre = BigInteger.Max(1, (BigInteger)baseMaximum + bonuses - trauma);
            return new MaximumHpCalculation(baseMaximum, bonuses, trauma, pre, SystemicMaximum(pre, expedition, exhaustion), selected);
        }
        public static long SystemicMaximum(BigInteger otherwiseMaximum, int expedition = 0, int exhaustion = 0)
        {
            if (otherwiseMaximum < 1 || expedition < 0 || expedition > 6 || exhaustion < 0 || exhaustion > 6)
                throw new ArgumentOutOfRangeException(nameof(otherwiseMaximum));
            BigInteger numerator = otherwiseMaximum, denominator = 1;
            if (expedition >= 4) { numerator *= 3; denominator *= 4; }
            if (exhaustion >= 4) denominator *= 2;
            return checked((long)BigInteger.Max(1, numerator / denominator));
        }
        public static LifeState ApplyCapacity(LifeState state, long maximum)
        {
            if (state == null) throw new ArgumentNullException(nameof(state));
            long hp = PlaytestCharacters.ClampAfterCapacityChange(state.Hp, maximum);
            return new LifeState(maximum, hp, state.TemporaryHp, state.Wounds, stable: state.Stable, dead: state.Dead,
                deathSuccesses: state.DeathSuccesses, deathFailures: state.DeathFailures, usesDeathSaves: state.UsesDeathSaves,
                lastDeathTurn: state.LastDeathTurn, stableUntil: state.StableUntil);
        }
        public static MaximumHpChange Recompute(LifeState state, long baseMaximum, IEnumerable<MaximumHpApplication> records,
            string target, EffectClockMarker now = default, int expedition = 0, int exhaustion = 0)
        {
            if (state == null) throw new ArgumentNullException(nameof(state));
            return new MaximumHpChange(Calculate(baseMaximum, records, target, now, expedition, exhaustion), state);
        }
        public static IReadOnlyList<MaximumHpApplication> CompleteRest(IEnumerable<MaximumHpApplication> records,
            string target, bool completed, CompletedRestKind kind)
        {
            Identity(target); if (!Enum.IsDefined(typeof(CompletedRestKind), kind)) throw new ArgumentException("Unsupported rest kind.");
            string reason = kind == CompletedRestKind.Short ? "completed-target-short-rest" : "completed-target-long-rest";
            return Array.AsReadOnly(Records(records).Select(x => completed && x.Target == target && x.EndsOnCompletedRest && x.Present ? x.Remove(reason) : x).ToArray());
        }
        public static bool Threshold(long hp, long maximum, HpFraction fraction, HpThresholdRelation relation = HpThresholdRelation.Below)
        {
            Hp(hp, maximum); BigInteger left = (BigInteger)hp * fraction.Denominator, right = (BigInteger)maximum * fraction.Numerator;
            switch (relation) {
                case HpThresholdRelation.Below: return left < right;
                case HpThresholdRelation.AtOrBelow: return left <= right;
                case HpThresholdRelation.Above: return left > right;
                case HpThresholdRelation.AtOrAbove: return left >= right;
                default: throw new ArgumentException("Unsupported threshold relation.");
            }
        }
        public static int PainEmpowerment(long hp, long maximum)
        { Hp(hp, maximum); return (int)BigInteger.Min(5, (BigInteger)10 * (maximum - hp) / maximum); }
        public static long PercentageAmount(long maximum, long denominator, long sourceMinimum = 0)
        {
            if (maximum < 1 || denominator < 1 || sourceMinimum < 0) throw new ArgumentOutOfRangeException(nameof(maximum));
            return Math.Max(sourceMinimum, maximum / denominator);
        }
    }
}
#endif
