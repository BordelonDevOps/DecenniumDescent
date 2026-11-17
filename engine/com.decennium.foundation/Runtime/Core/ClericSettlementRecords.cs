using System;
using System.Collections.Generic;
using System.Collections.ObjectModel;
using System.Linq;

namespace Decennium.Foundation
{
    public enum RadianceCurePreference { None, Frightened, Poisoned }

    /// <summary>A conditional recipient decision, never an assertion of authority or a cure invocation.</summary>
    public sealed class HealingRiteRequest
    {
        public RadianceCurePreference CurePreference { get; }
        public HealingRiteRequest(RadianceCurePreference curePreference = RadianceCurePreference.None)
        {
            if (!Enum.IsDefined(typeof(RadianceCurePreference), curePreference))
                throw new ArgumentException("Invalid Radiance cure preference.");
            CurePreference = curePreference;
        }
    }

    /// <summary>Immutable Director-authored opening objective. Declaring it supplies no award.</summary>
    public sealed class ClericMilestoneDeclaration
    {
        public const string FixedId = "TEST_ONLY.cleric.opening-milestone";
        public const string FixedObjective = "TEST_ONLY.cleric.two-conflicts-recipe4-alive.v1";
        public string MilestoneId => FixedId;
        public string ActorId => ClericRpProfile.Actor;
        public string ObjectiveId => FixedObjective;
        public string SourceRevision => ClericRpProfile.SourceRevision;
        public long DeclaredRevision => 0;
        public string FirstEncounterId => "world.fixed-conflict";
        public string LaterEncounterId => "TEST_ONLY.later-conflict";
        public string SpecimenId => ConnectedBloodSpecimen.SpecimenId;
        public string RecipeId => ConnectedRecipe4Batch.RecipeId;
        public string Binding => string.Join("|", ObjectiveId, MilestoneId, ActorId, SourceRevision, "0",
            FirstEncounterId, LaterEncounterId, SpecimenId, RecipeId, "actual-normal-closure|consumed-settled-batch|alive-not-positive-hp");
        public string Digest { get; }
        public ClericMilestoneDeclaration(string milestone, string actor, string objective, string sourceRevision,
            long declaredRevision, string firstEncounter, string laterEncounter, string specimen, string recipe, string digest)
        {
            using (var sha = System.Security.Cryptography.SHA256.Create())
                Digest = string.Concat(sha.ComputeHash(System.Text.Encoding.UTF8.GetBytes(Binding))
                    .Select(x => x.ToString("x2", System.Globalization.CultureInfo.InvariantCulture)));
            if (milestone != MilestoneId || actor != ActorId || objective != ObjectiveId || sourceRevision != SourceRevision
                || declaredRevision != 0 || firstEncounter != FirstEncounterId || laterEncounter != LaterEncounterId
                || specimen != SpecimenId || recipe != RecipeId || digest != Digest)
                throw new ArgumentException("Unsupported opening Cleric objective or declaration binding.");
        }
        private ClericMilestoneDeclaration()
        {
            using (var sha = System.Security.Cryptography.SHA256.Create())
                Digest = string.Concat(sha.ComputeHash(System.Text.Encoding.UTF8.GetBytes(Binding))
                    .Select(x => x.ToString("x2", System.Globalization.CultureInfo.InvariantCulture)));
        }
        public static ClericMilestoneDeclaration AuthoredExample() => new ClericMilestoneDeclaration();
    }

    /// <summary>Actual objective evidence, separate from shared milestone award and consumption.</summary>
    public sealed class ClericObjectiveCompletion
    {
        public string DeclarationDigest { get; }
        public string FirstClosureCommand { get; }
        public long FirstClosureRevision { get; }
        public string BatchOrderId { get; }
        public long BatchSettlementRevision { get; }
        public string LaterClosureCommand { get; }
        public long Revision { get; }
        public RuleTime At { get; }
        public ClericObjectiveCompletion(string declarationDigest, string firstClosureCommand, long firstClosureRevision,
            string batchOrderId, long batchSettlementRevision, string laterClosureCommand, long revision, RuleTime at)
        {
            if (declarationDigest != ClericMilestoneDeclaration.AuthoredExample().Digest
                || !Validation.ValidId(firstClosureCommand) || !Validation.ValidId(batchOrderId) || !Validation.ValidId(laterClosureCommand)
                || firstClosureRevision < 1 || batchSettlementRevision <= firstClosureRevision
                || revision <= batchSettlementRevision || at < default(RuleTime))
                throw new ArgumentException("Invalid earned Cleric objective evidence.");
            DeclarationDigest = declarationDigest; FirstClosureCommand = firstClosureCommand; FirstClosureRevision = firstClosureRevision;
            BatchOrderId = batchOrderId; BatchSettlementRevision = batchSettlementRevision;
            LaterClosureCommand = laterClosureCommand; Revision = revision; At = at;
        }
    }

    public sealed class ClericInvocationPathRecord
    {
        public string ActorId { get; }
        public string PathId { get; }
        public string SourceRevision { get; }
        public string MilestoneId { get; }
        public long AcquiredRevision { get; }
        public ClericInvocationPathRecord(string actor, string path, string sourceRevision, string milestone, long revision)
        {
            if (actor != ClericRpProfile.Actor || path != ClericSettlementProfile.Radiance
                || sourceRevision != ClericRpProfile.SourceRevision || milestone != ClericMilestoneDeclaration.FixedId || revision < 1)
                throw new ArgumentException("Invalid earned Invocation path.");
            ActorId = actor; PathId = path; SourceRevision = sourceRevision; MilestoneId = milestone; AcquiredRevision = revision;
        }
    }

    /// <summary>Capacity provenance only. There is deliberately no numeric balance, funding or payment.</summary>
    public sealed class ConvictionCapacityRecord
    {
        public string ActorId { get; }
        public string SourceRevision { get; }
        public string PoolMilestoneId { get; }
        public long PoolAcquiredRevision { get; }
        public int Maximum => PoolAcquiredRevision == 0 ? 3 : 5;
        public int? Current => null;
        public bool CurrentAvailable => false;
        public ConvictionCapacityRecord(string actor, string sourceRevision, string poolMilestone, long poolRevision)
        {
            if (actor != ClericRpProfile.Actor || sourceRevision != ClericRpProfile.SourceRevision || poolRevision < 0
                || (poolRevision == 0 ? poolMilestone != "" : poolMilestone != ClericMilestoneDeclaration.FixedId))
                throw new ArgumentException("Invalid Conviction capacity provenance.");
            ActorId = actor; SourceRevision = sourceRevision; PoolMilestoneId = poolMilestone; PoolAcquiredRevision = poolRevision;
        }
    }

    /// <summary>One actual paid Rite's nonrecursive Radiance result and owned-calendar identity.</summary>
    public sealed class RadianceUseRecord
    {
        public string RiteCommandId { get; }
        public long Revision { get; }
        public string ActorId { get; }
        public string TargetId { get; }
        public string SourceRevision { get; }
        public string EpochId { get; }
        public long LocalStart { get; }
        public int PhaseFirstTurn { get; }
        public int GlobalStart { get; }
        public ConditionStamp At { get; }
        public long BaseHpAfter { get; }
        private readonly long hpBefore;
        public long PreRadianceHp() => hpBefore;
        public long AdditionalPotential { get; }
        public long HpAfter { get; }
        public long AdditionalGain => HpAfter - hpBefore;
        public RadianceCurePreference CurePreference { get; }
        public string CureOperationId { get; }
        public ReadOnlyCollection<string> EndedApplicationIds { get; }
        public RadianceUseRecord(string riteCommand, long revision, string actor, string target, string sourceRevision,
            string epoch, long localStart, int phaseFirstTurn, int globalStart, ConditionStamp at,
            long baseHpAfter, long additionalPotential, long hpAfter, RadianceCurePreference preference,
            string cureOperation, IEnumerable<string> endedApplications, long? hpBefore = null)
        {
            var ids = endedApplications?.ToArray();
            long predecessor = hpBefore ?? baseHpAfter;
            if (!Validation.ValidId(riteCommand) || revision < 1 || actor != ClericRpProfile.Actor || !Validation.ValidId(target)
                || sourceRevision != ClericRpProfile.SourceRevision || !Validation.ValidId(epoch) || localStart < 0
                || phaseFirstTurn < 0 || globalStart != checked(localStart + phaseFirstTurn)
                || baseHpAfter < 1 || predecessor < baseHpAfter || predecessor - baseHpAfter > 1
                || additionalPotential < 0 || additionalPotential > 1 || hpAfter < predecessor
                || hpAfter - predecessor > additionalPotential || !Enum.IsDefined(typeof(RadianceCurePreference), preference)
                || ids == null || ids.Length > ConditionJournal.MaxOperations || ids.Any(x => !Validation.ValidId(x))
                || ids.Distinct(StringComparer.Ordinal).Count() != ids.Length
                || (ids.Length == 0 ? cureOperation != "" : !Validation.ValidId(cureOperation))
                || preference == RadianceCurePreference.None && ids.Length != 0)
                throw new ArgumentException("Invalid paid Radiance result.");
            RiteCommandId = riteCommand; Revision = revision; ActorId = actor; TargetId = target; SourceRevision = sourceRevision;
            EpochId = epoch; LocalStart = localStart; PhaseFirstTurn = phaseFirstTurn; GlobalStart = globalStart; At = at;
            BaseHpAfter = baseHpAfter; this.hpBefore = predecessor; AdditionalPotential = additionalPotential; HpAfter = hpAfter;
            CurePreference = preference; CureOperationId = cureOperation;
            EndedApplicationIds = Array.AsReadOnly(ids.OrderBy(x => x, StringComparer.Ordinal).ToArray());
        }
    }

    public static partial class ClericSettlementProfile
    {
        public const string FingerprintPrefix = "TEST_ONLY.cleric-settlement-v1-";
        public const byte Marker = 13;
        public const string Attunement = "cleric.base.invocation-attunement";
        public const string Radiance = "cleric.base.radiance.radiance";
        public const string JudgingLight = "cleric.base.judging-light";
        public const string ConvictionPool = "cleric.base.conviction-pool";
        public const string RadianceCardSha256 = "35f3566de386bca746618537d03e3561d74b8a35e1633c073ddef7e77f507821";
        public static IReadOnlyList<string> SelectedCards { get; } = Array.AsReadOnly(new[] { ConvictionPool, JudgingLight });
        public static bool SelectedFingerprint(string value) => value != null && (value.StartsWith(FingerprintPrefix, StringComparison.Ordinal)
            || SpellCastingProfile.SelectedFingerprint(value));
        public static bool ValidEarnedGrant(Snapshot state, CharacterFeatureGrantRecord grant)
        {
            if (!state.ConnectedClericSettlement || grant.ActorId != ClericRpProfile.Actor || grant.ClassName != "Cleric"
                || grant.ClassLevel != 2 || grant.MilestoneId != ClericMilestoneDeclaration.FixedId || grant.GrantedRevision < 1)
                return false;
            return (grant.Origin == CharacterFeatureGrantOrigin.SelectedCard && SelectedCards.Contains(grant.FeatureId)
                || grant.Origin == CharacterFeatureGrantOrigin.EarnedAutomaticClassFeature
                    && (grant.FeatureId == Attunement || grant.FeatureId == Radiance))
                && state.ClericInvocationPath?.AcquiredRevision == grant.GrantedRevision
                && state.CharacterAdvancements.Any(x => x.ActorId == grant.ActorId && x.Revision == grant.GrantedRevision
                    && x.MilestoneId == grant.MilestoneId && x.ClassName == "Cleric" && x.ClassLevel == 2)
                && state.CharacterMilestones.Any(x => x.ActorId == grant.ActorId && x.MilestoneId == grant.MilestoneId
                    && x.ConsumedRevision == grant.GrantedRevision);
        }
    }
}
