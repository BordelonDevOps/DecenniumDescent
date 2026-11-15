using System;
using System.Globalization;

namespace Decennium.Foundation
{
    /// <summary>Choices only. Source access, components, consent authority and costs are host-derived.</summary>
    public sealed class SpellCastRequest
    {
        public string SpellId { get; }
        public string FocusItemId { get; }
        public bool WillingTarget { get; }
        public bool ElectFocusedDc { get; }
        public SpellCastRequest(string spellId, string focusItemId = "", bool willingTarget = false, bool electFocusedDc = false)
        {
            if (!Validation.ValidId(spellId) || focusItemId == null || focusItemId != "" && !Validation.ValidId(focusItemId))
                throw new ArgumentException("Invalid ordinary spell selection.");
            SpellId = spellId; FocusItemId = focusItemId; WillingTarget = willingTarget; ElectFocusedDc = electFocusedDc;
        }
        public string Fingerprint => string.Join("|", SpellId, FocusItemId, WillingTarget ? "1" : "0", ElectFocusedDc ? "1" : "0");
    }

    /// <summary>The recipient elects an existing benefit before an actual eligible check is rolled.</summary>
    public sealed class GuidanceChoice
    {
        public string EffectId { get; }
        public GuidanceChoice(string effectId)
        {
            if (!Validation.ValidId(effectId)) throw new ArgumentException("Invalid Guidance choice.");
            EffectId = effectId;
        }
    }

    public enum SanctuaryResponseKind { Retarget, Forgo }
    public sealed class SanctuaryResponseRequest
    {
        public SanctuaryResponseKind Kind { get; }
        public string TargetId { get; }
        public SanctuaryResponseRequest(SanctuaryResponseKind kind, string targetId = "")
        {
            if (!Enum.IsDefined(typeof(SanctuaryResponseKind), kind) || targetId == null
                || kind == SanctuaryResponseKind.Retarget && !Validation.ValidId(targetId)
                || kind == SanctuaryResponseKind.Forgo && targetId != "")
                throw new ArgumentException("Invalid Sanctuary response.");
            Kind = kind; TargetId = targetId;
        }
        public string Fingerprint => ((int)Kind).ToString(CultureInfo.InvariantCulture) + "|" + TargetId;
    }

    /// <summary>A real owner interval, or the exact interval carried into an admitted new calendar.
    /// Carried intervals have no new local Start; their global identity must never be computed from -1.</summary>
    public sealed class SpellTurnIdentity
    {
        public string ActorId { get; }
        public string EpochId { get; }
        public long LocalStart { get; }
        public long GlobalStart { get; }
        public long CarriedAdmissionRevision { get; }
        public bool IsCarried => CarriedAdmissionRevision != 0;
        public SpellTurnIdentity(string actorId, string epochId, long localStart, long globalStart, long carriedAdmissionRevision = 0)
        {
            if (!Validation.ValidId(actorId) || !Validation.ValidId(epochId) || carriedAdmissionRevision < 0
                || carriedAdmissionRevision == 0 && (localStart < 0 || globalStart < 0)
                || carriedAdmissionRevision != 0 && (localStart != -1 || globalStart < -1))
                throw new ArgumentException("Invalid casting interval identity.");
            ActorId = actorId; EpochId = epochId; LocalStart = localStart;
            GlobalStart = globalStart; CarriedAdmissionRevision = carriedAdmissionRevision;
        }
        public bool SameAs(SpellTurnIdentity other) => other != null && ActorId == other.ActorId && EpochId == other.EpochId
            && LocalStart == other.LocalStart && GlobalStart == other.GlobalStart && CarriedAdmissionRevision == other.CarriedAdmissionRevision;
        public string Binding => string.Join("|", ActorId, EpochId, LocalStart.ToString(CultureInfo.InvariantCulture),
            GlobalStart.ToString(CultureInfo.InvariantCulture), CarriedAdmissionRevision.ToString(CultureInfo.InvariantCulture));
    }

    /// <summary>Persisted casting cadence. Mechanical operations supply no cast, rest or funding authority.</summary>
    public sealed class CastingStrainRecord
    {
        public string ActorId { get; }
        public int Dissonance { get; }
        public string LastSpellId { get; }
        public int Refrain { get; }
        public long LastCastRevision { get; }
        public CastingStrainRecord(string actorId, int dissonance = 0, string lastSpellId = "", int refrain = 0, long lastCastRevision = 0)
        {
            if (!Validation.ValidId(actorId) || dissonance < 0 || lastSpellId == null
                || lastSpellId != "" && !Validation.ValidId(lastSpellId) || refrain < 0 || refrain > 3 || lastCastRevision < 0
                || (lastSpellId == "") != (lastCastRevision == 0) || lastSpellId == "" && (refrain != 0 || dissonance != 0))
                throw new ArgumentException("Invalid casting strain history.");
            ActorId = actorId; Dissonance = dissonance; LastSpellId = lastSpellId; Refrain = refrain; LastCastRevision = lastCastRevision;
        }
        public static int Limit(int proficiency, int actualCastingModifier)
        {
            if (proficiency < 0) throw new ArgumentOutOfRangeException(nameof(proficiency));
            return Math.Max(4, checked(2 + proficiency + Math.Max(0, actualCastingModifier)));
        }
        public bool RankedBlocked(int proficiency, int actualCastingModifier)
            => Dissonance >= checked(Limit(proficiency, actualCastingModifier) + 6);
        public int RankedSurcharge(int proficiency, int actualCastingModifier)
        {
            int limit = Limit(proficiency, actualCastingModifier);
            return Dissonance >= checked(limit + 6) ? 3 : Dissonance >= checked(limit + 3) ? 2 : Dissonance >= limit ? 1 : 0;
        }
        public CastingStrainRecord BeginAdmittedCast(string spellId, int rank, long revision)
        {
            if (!Validation.ValidId(spellId) || rank < 0 || rank > 1 || revision <= LastCastRevision)
                throw new ArgumentException("Invalid admitted casting cadence event.");
            int repeat = spellId == LastSpellId ? Math.Min(3, Refrain + 1) : 0;
            return new CastingStrainRecord(ActorId, checked(Dissonance + (rank == 0 ? 0 : 1) + repeat), spellId, repeat, revision);
        }
        public CastingStrainRecord ReduceAtSettledEnd(int amount)
        {
            if (amount < 0) throw new ArgumentOutOfRangeException(nameof(amount));
            return new CastingStrainRecord(ActorId, Math.Max(0, Dissonance - amount), LastSpellId, Refrain, LastCastRevision);
        }
    }

    public enum CastingActivityKind { Spell, MagicalClassAbility, DetectFocus, Grounding }
    public sealed class CastingActivityRecord
    {
        public string CommandId { get; }
        public long Revision { get; }
        public SpellTurnIdentity Turn { get; }
        public RuleTime At { get; }
        public CastingActivityKind Kind { get; }
        public CastingActivityRecord(string commandId, long revision, SpellTurnIdentity turn, RuleTime at, CastingActivityKind kind)
        {
            if (!Validation.ValidId(commandId) || revision < 1 || turn == null || turn.IsCarried
                || !Enum.IsDefined(typeof(CastingActivityKind), kind)) throw new ArgumentException("Invalid casting activity.");
            CommandId = commandId; Revision = revision; Turn = turn; At = at; Kind = kind;
        }
        public bool IsMagical => Kind != CastingActivityKind.Grounding;
    }

    public sealed class CastingTurnEndRecord
    {
        public SpellTurnIdentity Turn { get; }
        public string CauseId { get; }
        public long Revision { get; }
        public RuleTime At { get; }
        public int Before { get; }
        public int After { get; }
        public bool MagicalActivity { get; }
        public bool Grounding { get; }
        public int Proficiency { get; }
        public CastingTurnEndRecord(SpellTurnIdentity turn, string causeId, long revision, RuleTime at,
            int before, int after, bool magicalActivity, bool grounding, int proficiency)
        {
            if (turn == null || turn.IsCarried || !Validation.ValidId(causeId) || revision < 1 || before < 0 || proficiency < 0
                || after != Math.Max(0, before - (magicalActivity ? 0 : grounding ? proficiency : 1)))
                throw new ArgumentException("Invalid regular-End casting settlement.");
            Turn = turn; CauseId = causeId; Revision = revision; At = at; Before = before; After = after;
            MagicalActivity = magicalActivity; Grounding = grounding; Proficiency = proficiency;
        }
    }

    public enum SpellEffectEndReason { None, Expired, Replaced, Voluntary, Incapacitated, Dead, DamageSaveFailed,
        GuidanceConsumed, SanctuaryDamage, SanctuaryHostileSave }
    public enum SpellExpiryKind { Absolute, NextCasterStart }
    public sealed class SpellEffectRecord
    {
        public string Id { get; }
        public string CastId { get; }
        public long CastRevision { get; }
        public string SpellId { get; }
        public string CasterId { get; }
        public string TargetId { get; }
        public RuleTime StartedAt { get; }
        public RuleTime ExpiresAt { get; }
        public SpellExpiryKind ExpiryKind { get; }
        public SpellTurnIdentity ExpiryTurn { get; }
        public bool RequiresConcentration { get; }
        public string EndCauseId { get; }
        public long EndRevision { get; }
        public RuleTime? EndedAt { get; }
        public SpellEffectEndReason EndReason { get; }
        public bool Present => EndReason == SpellEffectEndReason.None;
        public SpellEffectRecord(string id, string castId, long castRevision, string spellId, string casterId, string targetId,
            RuleTime startedAt, RuleTime expiresAt, SpellExpiryKind expiryKind, SpellTurnIdentity expiryTurn, bool concentration,
            string endCauseId = "", long endRevision = 0, RuleTime? endedAt = null, SpellEffectEndReason endReason = SpellEffectEndReason.None)
        {
            if (!Validation.ValidId(id) || !Validation.ValidId(castId) || castRevision < 1 || !Validation.ValidId(spellId)
                || !Validation.ValidId(casterId) || !Validation.ValidId(targetId) || expiresAt <= startedAt
                || !Enum.IsDefined(typeof(SpellExpiryKind), expiryKind) || !Enum.IsDefined(typeof(SpellEffectEndReason), endReason)
                || (expiryKind == SpellExpiryKind.NextCasterStart) != (expiryTurn != null)
                || expiryTurn != null && (expiryTurn.IsCarried || expiryTurn.ActorId != casterId)
                || endReason == SpellEffectEndReason.None && (endCauseId != "" || endRevision != 0 || endedAt.HasValue)
                || endReason != SpellEffectEndReason.None && (!Validation.ValidId(endCauseId) || endRevision < castRevision
                    || !endedAt.HasValue || endedAt.Value < startedAt || endedAt.Value > expiresAt))
                throw new ArgumentException("Invalid spell effect lifecycle.");
            Id = id; CastId = castId; CastRevision = castRevision; SpellId = spellId; CasterId = casterId; TargetId = targetId;
            StartedAt = startedAt; ExpiresAt = expiresAt; ExpiryKind = expiryKind; ExpiryTurn = expiryTurn; RequiresConcentration = concentration;
            EndCauseId = endCauseId; EndRevision = endRevision; EndedAt = endedAt; EndReason = endReason;
        }
        public SpellEffectRecord End(string causeId, long revision, RuleTime at, SpellEffectEndReason reason)
        {
            if (!Present || reason == SpellEffectEndReason.None) throw new InvalidOperationException("An effect can end only once.");
            return new SpellEffectRecord(Id, CastId, CastRevision, SpellId, CasterId, TargetId, StartedAt, ExpiresAt,
                ExpiryKind, ExpiryTurn, RequiresConcentration, causeId, revision, at, reason);
        }
    }

    public enum ConsumableContaminationKind { OrdinaryPoison, OrdinaryPathogen, MundaneAlchemicalPoison,
        MagicalPoison, Supernatural, Curse, Corruption, Enchantment, Unresolved }
    /// <summary>Occurrence provenance only. Quantity, custody and freshness remain in their existing shared records.</summary>
    public sealed class ConsumableContaminationRecord
    {
        public string Id { get; }
        public string LotId { get; }
        public string OriginId { get; }
        public long OriginRevision { get; }
        public ConsumableContaminationKind Kind { get; }
        public string DestroyedByCastId { get; }
        public long DestroyedRevision { get; }
        public bool Present => DestroyedRevision == 0;
        public bool Purifiable => Kind == ConsumableContaminationKind.OrdinaryPoison
            || Kind == ConsumableContaminationKind.OrdinaryPathogen || Kind == ConsumableContaminationKind.MundaneAlchemicalPoison;
        public ConsumableContaminationRecord(string id, string lotId, string originId, long originRevision,
            ConsumableContaminationKind kind, string destroyedByCastId = "", long destroyedRevision = 0)
        {
            if (!Validation.ValidId(id) || !Validation.ValidId(lotId) || !Validation.ValidId(originId) || originRevision < 0
                || !Enum.IsDefined(typeof(ConsumableContaminationKind), kind) || destroyedByCastId == null || destroyedRevision < 0
                || (destroyedRevision == 0) != (destroyedByCastId == "") || destroyedRevision != 0
                    && (!Validation.ValidId(destroyedByCastId) || destroyedRevision <= originRevision))
                throw new ArgumentException("Invalid consumable contamination provenance.");
            Id = id; LotId = lotId; OriginId = originId; OriginRevision = originRevision; Kind = kind;
            DestroyedByCastId = destroyedByCastId; DestroyedRevision = destroyedRevision;
            if (!Present && !Purifiable) throw new ArgumentException("Purify cannot destroy this contamination.");
        }
        public ConsumableContaminationRecord Destroy(string castId, long revision)
        {
            if (!Present || !Purifiable) throw new InvalidOperationException("Contamination is not eligible for destruction.");
            return new ConsumableContaminationRecord(Id, LotId, OriginId, OriginRevision, Kind, castId, revision);
        }
    }
}
