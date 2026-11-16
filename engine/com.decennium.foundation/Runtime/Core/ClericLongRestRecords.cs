using System;
using System.Globalization;

namespace Decennium.Foundation
{
    public enum ClericLongRestOutcome { Active, Interrupted, Completed }
    public enum ClericLongRestInterruption { None, Explicit, Damage, Encounter, AccessLost, BodyIneligible }
    public enum ClericLongRestBenefit { NotCompleted, Eligible, CadenceLimited, RestDebtOwed }

    /// <summary>Receipt provenance for one actual interval in the shared Rest and Work ledgers.</summary>
    public sealed class ClericLongRestRecord
    {
        public int Sequence { get; }
        public string Id => ClericLongRestProfile.IntervalPrefix + Sequence.ToString(CultureInfo.InvariantCulture);
        public string ActorId => ClericRpProfile.Actor;
        public string SiteId => ClericLongRestProfile.SiteId;
        public string StartCommandId { get; }
        public long StartRevision { get; }
        public RuleTime StartedAt { get; }
        public RuleTime DueAt => StartedAt.AddSeconds(ClericLongRestProfile.DurationSeconds);
        public ClericLongRestOutcome Outcome { get; }
        public ClericLongRestInterruption Interruption { get; }
        public ClericLongRestBenefit Benefit { get; }
        public string EndCommandId { get; }
        public long EndRevision { get; }
        public RuleTime? EndedAt { get; }
        public string CauseId { get; }

        public ClericLongRestRecord(int sequence, string startCommandId, long startRevision, RuleTime startedAt,
            ClericLongRestOutcome outcome = ClericLongRestOutcome.Active,
            ClericLongRestInterruption interruption = ClericLongRestInterruption.None,
            ClericLongRestBenefit benefit = ClericLongRestBenefit.NotCompleted,
            string endCommandId = "", long endRevision = 0, RuleTime? endedAt = null, string causeId = "")
        {
            bool active = outcome == ClericLongRestOutcome.Active;
            bool completed = outcome == ClericLongRestOutcome.Completed;
            if (sequence < 0 || sequence >= ClericLongRestProfile.MaxAttempts || !Validation.ValidId(startCommandId)
                || startRevision < 1 || startedAt < default(RuleTime)
                || !Enum.IsDefined(typeof(ClericLongRestOutcome), outcome)
                || !Enum.IsDefined(typeof(ClericLongRestInterruption), interruption)
                || !Enum.IsDefined(typeof(ClericLongRestBenefit), benefit)
                || (completed ? benefit == ClericLongRestBenefit.NotCompleted : benefit != ClericLongRestBenefit.NotCompleted)
                || (outcome == ClericLongRestOutcome.Interrupted
                    ? interruption == ClericLongRestInterruption.None : interruption != ClericLongRestInterruption.None)
                || (active ? endCommandId != "" || endRevision != 0 || endedAt.HasValue || causeId != ""
                    : !Validation.ValidId(endCommandId) || endRevision <= startRevision || !endedAt.HasValue
                        || endedAt < startedAt || endedAt > startedAt.AddSeconds(ClericLongRestProfile.DurationSeconds)
                        || !Validation.ValidId(causeId))
                || completed && endedAt != startedAt.AddSeconds(ClericLongRestProfile.DurationSeconds))
                throw new ArgumentException("Invalid source-bound Cleric Long Rest interval.");
            Sequence = sequence; StartCommandId = startCommandId; StartRevision = startRevision; StartedAt = startedAt;
            Outcome = outcome; Interruption = interruption; Benefit = benefit; EndCommandId = endCommandId;
            EndRevision = endRevision; EndedAt = endedAt; CauseId = causeId;
        }
    }

    /// <summary>Only known current Conviction. The existing capacity record still owns its maximum.
    /// Absence of this record means unavailable, never zero or implicit funding.</summary>
    public sealed class ConvictionBalanceRecord
    {
        public string ActorId => ClericRpProfile.Actor;
        public string FundingRestId { get; }
        public long FundingRevision { get; }
        public int Current { get; }
        public ConvictionBalanceRecord(string fundingRestId, long fundingRevision, int current)
        {
            if (!Validation.ValidId(fundingRestId) || fundingRevision < 1 || current < 0 || current > 5)
                throw new ArgumentException("Invalid source-bound Conviction balance.");
            FundingRestId = fundingRestId; FundingRevision = fundingRevision; Current = current;
        }
    }

    /// <summary>Ordered completion settlement, including completion-only endings on a capped rest.
    /// This is causal evidence; life, RP, casting and Conviction records own current state.</summary>
    public sealed class ClericLongRestSettlementRecord
    {
        public string RestId { get; }
        public string CommandId { get; }
        public long Revision { get; }
        public RuleTime At { get; }
        public ClericLongRestBenefit Benefit { get; }
        public string BeneficialRestId { get; }
        public string PreviousBeneficialRestId { get; }
        public long CapacityAcquiredRevision { get; }
        public long HpBefore { get; }
        public long EffectiveMaximumHp { get; }
        public long HealingRequested { get; }
        public long HealingPotential { get; }
        public long HpAfter { get; }
        public long ActualHealing => HpAfter - HpBefore;
        public long TemporaryHpBefore { get; }
        public long TemporaryHpAfter { get; }
        public int Wounds { get; }
        public int ExpendedHitDice { get; }
        public int HitDiceAllowance { get; }
        public int HitDiceRecovered { get; }
        public int RpBefore { get; }
        public int RpMaximum { get; }
        public int RpAfter { get; }
        public int? ConvictionBefore { get; }
        public int? ConvictionAfter { get; }
        public int? ConvictionRestored => ConvictionBefore.HasValue && ConvictionAfter.HasValue
            ? ConvictionAfter.Value - ConvictionBefore.Value : (int?)null;
        public int DissonanceBefore { get; }
        public int DissonanceAfter { get; }
        public string LastSpellId { get; }
        public int Refrain { get; }
        public long LastCastRevision { get; }
        public bool ResetsShortRestAllowance => Benefit == ClericLongRestBenefit.Eligible;
        public string ShortRestEpochId => ResetsShortRestAllowance ? BeneficialRestId : "";
        public int ShortRestBenefitAllowance => ResetsShortRestAllowance ? 2 : 0;

        public ClericLongRestSettlementRecord(string restId, string commandId, long revision, RuleTime at,
            ClericLongRestBenefit benefit, string beneficialRestId, string previousBeneficialRestId,
            long capacityAcquiredRevision, long hpBefore, long effectiveMaximumHp, long healingRequested,
            long healingPotential, long hpAfter, long temporaryHpBefore, long temporaryHpAfter,
            int wounds, int expendedHitDice, int hitDiceAllowance, int hitDiceRecovered,
            int rpBefore, int rpMaximum, int rpAfter, int? convictionBefore, int? convictionAfter,
            int dissonanceBefore, int dissonanceAfter, string lastSpellId, int refrain, long lastCastRevision)
        {
            bool eligible = benefit == ClericLongRestBenefit.Eligible;
            if (!Validation.ValidId(restId) || !Validation.ValidId(commandId) || revision < 1 || at < default(RuleTime)
                || !Enum.IsDefined(typeof(ClericLongRestBenefit), benefit) || benefit == ClericLongRestBenefit.NotCompleted
                || (eligible ? !Validation.ValidId(beneficialRestId) : beneficialRestId != "")
                || previousBeneficialRestId == null || previousBeneficialRestId != "" && !Validation.ValidId(previousBeneficialRestId)
                || capacityAcquiredRevision < 1 || capacityAcquiredRevision >= revision
                || hpBefore < 1 || effectiveMaximumHp < 1 || hpAfter < hpBefore
                || healingRequested < 0 || healingPotential < 0 || healingPotential > healingRequested
                || hpAfter - hpBefore > healingPotential || temporaryHpBefore < 0 || temporaryHpAfter < 0
                || temporaryHpAfter > temporaryHpBefore || wounds < 0 || wounds > 3
                || expendedHitDice < 0 || expendedHitDice > 2 || hitDiceAllowance < 0 || hitDiceRecovered < 0
                || hitDiceRecovered > hitDiceAllowance || hitDiceRecovered > expendedHitDice
                || rpMaximum != 4 || rpBefore < 0 || rpBefore > rpMaximum || rpAfter < rpBefore || rpAfter > rpMaximum
                || convictionBefore < 0 || convictionBefore > 5 || convictionAfter < 0 || convictionAfter > 5
                || dissonanceBefore < 0 || dissonanceAfter < 0 || dissonanceAfter > dissonanceBefore
                || lastSpellId == null || lastSpellId != "" && !Validation.ValidId(lastSpellId)
                || refrain < 0 || refrain > 3 || lastCastRevision < 0 || lastCastRevision >= revision
                || (lastSpellId == "") != (lastCastRevision == 0)
                || eligible && (healingRequested != ClericLongRestProfile.HealingRequest(hpBefore, effectiveMaximumHp)
                    || hitDiceAllowance != ClericLongRestProfile.HitDiceAllowance(expendedHitDice, wounds)
                    || rpAfter != rpMaximum || convictionAfter != 5 || dissonanceAfter != 0)
                || !eligible && (healingRequested != 0 || healingPotential != 0 || hpAfter != hpBefore
                    || hitDiceAllowance != 0 || hitDiceRecovered != 0 || rpAfter != rpBefore
                    || convictionAfter != convictionBefore || dissonanceAfter != dissonanceBefore))
                throw new ArgumentException("Invalid Cleric Long Rest completion settlement.");
            RestId = restId; CommandId = commandId; Revision = revision; At = at; Benefit = benefit;
            BeneficialRestId = beneficialRestId; PreviousBeneficialRestId = previousBeneficialRestId;
            CapacityAcquiredRevision = capacityAcquiredRevision; HpBefore = hpBefore; EffectiveMaximumHp = effectiveMaximumHp;
            HealingRequested = healingRequested; HealingPotential = healingPotential; HpAfter = hpAfter;
            TemporaryHpBefore = temporaryHpBefore; TemporaryHpAfter = temporaryHpAfter; Wounds = wounds;
            ExpendedHitDice = expendedHitDice; HitDiceAllowance = hitDiceAllowance; HitDiceRecovered = hitDiceRecovered;
            RpBefore = rpBefore; RpMaximum = rpMaximum; RpAfter = rpAfter;
            ConvictionBefore = convictionBefore; ConvictionAfter = convictionAfter;
            DissonanceBefore = dissonanceBefore; DissonanceAfter = dissonanceAfter;
            LastSpellId = lastSpellId; Refrain = refrain; LastCastRevision = lastCastRevision;
        }
    }

    public static partial class ClericLongRestProfile
    {
        public const string FingerprintPrefix = "TEST_ONLY.cleric-long-rest-v1-";
        public const string ApprovalResponse = "8588491a-0698-50ec-9830-b4ad4208d1ce";
        public const string SiteId = "TEST_ONLY.cleric-long-rest-berth";
        public const string IntervalPrefix = "TEST_ONLY.cleric-long-rest.";
        public const int X = 1, Y = 3, DurationSeconds = 28800, BenefitCadenceSeconds = 86400;
        public const int MaxAttempts = 1024; // Technical retained-history capacity, not a rest rule.
        public const byte Marker = 15;
        public static bool SelectedFingerprint(string value)
            => value != null && value.StartsWith(FingerprintPrefix, StringComparison.Ordinal);
        public static string OccupancyId(string restId) => restId + ".occupancy";
        public static long HealingRequest(long currentHp, long effectiveMaximumHp)
        {
            if (currentHp < 0 || effectiveMaximumHp < 1) throw new ArgumentException("Invalid healing basis.");
            return Math.Max(0, effectiveMaximumHp - currentHp);
        }
        public static int HitDiceAllowance(int expended, int wounds)
        {
            if (expended < 0 || wounds < 0 || wounds > 3) throw new ArgumentException("Invalid Hit Dice recovery basis.");
            return Math.Max(0, checked(expended / 2 + expended % 2 - wounds));
        }
        public static bool DamageInterrupts(long resolvedDamage)
        {
            if (resolvedDamage < 0) throw new ArgumentOutOfRangeException(nameof(resolvedDamage));
            return resolvedDamage > 0;
        }
    }
}
