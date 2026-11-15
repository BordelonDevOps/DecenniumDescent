using System;
using System.Linq;

namespace Decennium.Foundation
{
    public static partial class ClericSettlementProfile
    {
        public static bool ValidAdvancement(Snapshot s, CharacterAdvancementRecord a)
            => s.ConnectedClericSettlement && a.ActorId == ClericRpProfile.Actor && a.MilestoneId == ClericMilestoneDeclaration.FixedId
                && a.ClassName == "Cleric" && a.ClassLevel == 2 && a.PreviousTotalLevel == 1 && a.NewTotalLevel == 2
                && a.BaseHpGain == 5 && a.HitPointMethod == HitPointGainMethod.FixedAverage
                && a.MaximumHpBefore == 8 && a.MaximumHpAfter == 13 && a.CurrentHpBefore <= 8
                && a.CurrentHpAfter == a.CurrentHpBefore && a.SelectedFeatureIds.SequenceEqual(SelectedCards)
                && a.AsiAbilityIncreases.Count == 0 && a.AbilityScoresBefore.Count == 0 && a.AbilityScoresAfter.Count == 0
                && s.ClericInvocationPath?.AcquiredRevision == a.Revision;

        public static bool ValidChoices(CharacterAdvancementRequest request)
            => request != null && request.UsesClericSettlementReceipt && request.FeatureIds.SequenceEqual(SelectedCards)
                && request.InvocationPath == Radiance && request.EarnedSpell == ClericRepertoireProfile.FutureChoice
                && request.AsiAbilityIncreases.Count == 0 && request.FeatId == "";

        // Structural causal links are also reconstructed by the selected policy's strict command replay.
        public static bool QualifiesCure(Snapshot s, string target, ConditionOperation operation)
            => s.ConnectedClericSettlement && operation.Kind == ConditionOperationKind.Cure
                && s.RadianceUses.Any(x => x.TargetId == target && x.CureOperationId == operation.Id
                    && x.At.Equals(operation.At) && x.CurePreference != RadianceCurePreference.None
                    && operation.Subject == x.CurePreference.ToString() && x.EndedApplicationIds.Count != 0);

        public static bool CuredBeforeRepeat(Snapshot s, FrightenedTimingRecord timing)
            => s.ConnectedClericSettlement && s.RadianceUses.Any(x => x.TargetId == timing.TargetId
                && x.CurePreference == RadianceCurePreference.Frightened && x.At.CompareTo(timing.RepeatAt) < 0
                && x.EndedApplicationIds.Contains(timing.ApplicationId)
                && s.Conditions.Single(j => j.Target == timing.TargetId).Operations.Any(o => o.Id == x.CureOperationId && QualifiesCure(s,timing.TargetId,o)));

        internal static void Validate(Snapshot s)
        {
            bool selected = SelectedFingerprint(s.ContentFingerprint);
            if (s.ConnectedClericSettlement != selected || s.RadianceUses == null || s.RadianceUses.Length > 128 || s.RadianceUses.Any(x => x == null))
                throw new ArgumentException("Invalid Cleric settlement envelope.");
            if (!selected) {
                if (s.ClericMilestone != null || s.ClericObjective != null || s.ClericInvocationPath != null || s.ConvictionCapacity != null
                    || s.RadianceUses.Length != 0 || s.CharacterFeatureGrants.Any(x => x.Origin == CharacterFeatureGrantOrigin.EarnedAutomaticClassFeature))
                    throw new ArgumentException("Earned Cleric settlement requires its explicit envelope.");
                return;
            }
            if (!s.TestOnly || !s.ConnectedFrightened || s.SchemaVersion != Snapshot.SurpriseEntrySchema
                || s.ClericMilestone == null || s.ConvictionCapacity == null)
                throw new ArgumentException("Missing announced Cleric objective or capacity provenance.");
            var actor = s.Characters.Single(x => x.ActorId == ClericRpProfile.Actor);
            var advances = s.CharacterAdvancements.Where(x => x.ActorId == actor.ActorId).ToArray();
            var awards = s.CharacterMilestones.Where(x => x.ActorId == actor.ActorId).ToArray();
            if (advances.Length > 1 || awards.Length > 1 || actor.Levels.Count != 1 + advances.Length
                || actor.Levels.Any(x => x.ClassName != "Cleric") || actor.Levels[0].BaseHp != 8
                || actor.Levels.Count == 2 && actor.Levels[1].BaseHp != 5
                || (s.ClericInvocationPath != null) != (advances.Length == 1))
                throw new ArgumentException("Invalid earned Cleric chronology.");
            var completion = s.ClericObjective;
            if (completion != null) {
                var first = s.LaterEncounter?.FirstExit;
                var last = s.ClosedEncounters.SingleOrDefault(x => x.Encounter.Id == s.ClericMilestone.LaterEncounterId);
                var batch = s.ConnectedBatch;
                if (first == null || last == null || first.Encounter.Id != s.ClericMilestone.FirstEncounterId
                    || first.Reason != completion.FirstClosureCommand || first.ClosedRevision != completion.FirstClosureRevision
                    || last.Reason != completion.LaterClosureCommand || last.ClosedRevision != completion.Revision || last.ClosedAt != completion.At
                    || completion.Revision > s.Revision || completion.At > s.RuleClock || batch == null
                    || batch.OrderId != completion.BatchOrderId || batch.SettlementRevision != completion.BatchSettlementRevision
                    || batch.Disposition != ConnectedSpecimenDisposition.Consumed
                    || !s.ManufacturingOrders.Any(x => x.Id == batch.OrderId && x.RecipeId == ConnectedRecipe4Batch.RecipeId
                        && x.Status == ManufacturingStatus.Complete)
                    || !s.Receipts.Any(x => x.Id == last.Reason && x.Revision == last.ClosedRevision
                        && CommandHistory.Read(x).Kind == CommandKind.EndFixedEncounter))
                    throw new ArgumentException("Cleric objective is not backed by actual closed encounters and a settled consumed batch.");
            }
            foreach (var award in awards) {
                var receipt = s.Receipts.SingleOrDefault(x => x.Revision == award.AwardedRevision);
                var command = receipt == null ? null : CommandHistory.Read(receipt);
                if (completion == null || award.MilestoneId != s.ClericMilestone.MilestoneId || award.AwardedRevision <= completion.Revision
                    || command?.Kind != CommandKind.AwardCharacterMilestone || command.Actor != actor.ActorId
                    || command.Target != award.MilestoneId || receipt.Principal != "TEST_ONLY.host")
                    throw new ArgumentException("Unattributed Cleric milestone award.");
            }
            if (advances.Length == 1) {
                var a = advances[0]; var receipt = s.Receipts.SingleOrDefault(x => x.Revision == a.Revision);
                var command = receipt == null ? null : CommandHistory.Read(receipt);
                if (!ValidAdvancement(s,a) || command?.Kind != CommandKind.AdvanceCharacterLevel || command.Actor != actor.ActorId
                    || command.Target != a.MilestoneId || !ValidChoices(command.Advancement) || receipt.Principal != "TEST_ONLY.host"
                    || awards.Length != 1 || awards[0].ConsumedRevision != a.Revision
                    || s.ConvictionCapacity.PoolAcquiredRevision != a.Revision || s.ConvictionCapacity.PoolMilestoneId != a.MilestoneId
                    || s.CharacterFeatureGrants.Count(x => ValidEarnedGrant(s,x)) != 4
                    || s.CharacterHitDice.Count(x => x.ActorId == actor.ActorId && x.LevelOrdinal == 2 && x.ClassName == "Cleric" && x.DieSize == 8) != 1)
                    throw new ArgumentException("Invalid atomic Cleric settlement provenance.");
            } else if (s.ConvictionCapacity.PoolAcquiredRevision != 0 || s.RadianceUses.Length != 0
                || awards.Any(x => x.ConsumedRevision != 0)) throw new ArgumentException("Premature Cleric settlement effects.");
            if (s.CharacterFeatureGrants.Any(x => x.ActorId == actor.ActorId && x.Origin != CharacterFeatureGrantOrigin.InitialClassSelection
                && !ValidEarnedGrant(s,x))) throw new ArgumentException("Unsupported earned Cleric grant.");
            if (s.RadianceUses.Select(x => x.RiteCommandId).Distinct(StringComparer.Ordinal).Count() != s.RadianceUses.Length
                || s.RadianceUses.Select(x => x.ActorId + "|" + x.EpochId + "|" + x.LocalStart.ToString(System.Globalization.CultureInfo.InvariantCulture))
                    .Distinct(StringComparer.Ordinal).Count() != s.RadianceUses.Length
                || !s.RadianceUses.Select(x => x.Revision).SequenceEqual(s.RadianceUses.Select(x => x.Revision).OrderBy(x => x)))
                throw new ArgumentException("Duplicate or unordered Radiance use.");
            foreach (var use in s.RadianceUses) {
                var rite = s.HealingRites.SingleOrDefault(x => x.CommandId == use.RiteCommandId);
                var epoch = WorldTiming.FindEpoch(s,use.EpochId); var phase = s.Reinforcement?.Admission?.Phase;
                var receipt = s.Receipts.SingleOrDefault(x => x.Revision == use.Revision);
                var command = receipt == null ? null : CommandHistory.Read(receipt);
                if (rite == null || rite.Revision != use.Revision || rite.ActorId != use.ActorId || rite.TargetId != use.TargetId
                    || rite.At != use.At.Time || rite.TurnOrdinal != use.GlobalStart || rite.HpAfter != use.BaseHpAfter || rite.ActualGain <= 0
                    || use.Revision <= s.ClericInvocationPath.AcquiredRevision || use.Revision > s.Revision || use.At.Time > s.RuleClock
                    || epoch == null || phase?.Epoch.Id != epoch.Id || use.PhaseFirstTurn != phase.FirstTurn
                    || epoch.SlotAt(use.At.Time) != use.LocalStart || epoch.LatestStart(use.ActorId,use.LocalStart) != use.LocalStart
                    || phase.GlobalTurn(use.LocalStart) != use.GlobalStart || epoch.Start(use.LocalStart) > use.At.Time
                    || command?.Kind != CommandKind.UseHealingRite || command.Actor != use.ActorId || command.Target != use.TargetId
                    || (command.HealingRite?.CurePreference ?? RadianceCurePreference.None) != use.CurePreference)
                    throw new ArgumentException("Unqualified Radiance payment, ownership or calendar marker.");
                var journal = s.Conditions.Single(x => x.Target == use.TargetId);
                var cure = journal.Operations.SingleOrDefault(x => x.Id == use.CureOperationId);
                if (use.EndedApplicationIds.Count == 0 ? cure != null : cure == null || !QualifiesCure(s,use.TargetId,cure)
                    || use.CureOperationId != use.RiteCommandId + ".radiance.cure"
                    || use.EndedApplicationIds.Any(id => !journal.Operations.Any(x => x.Kind == ConditionOperationKind.Apply
                        && x.Application.Id == id && x.Application.Kind == use.CurePreference.ToString() && x.Application.GenericCureAllowed
                        && x.At.CompareTo(use.At) <= 0 && (!x.Application.Expires.HasValue || x.Application.Expires.Value.CompareTo(use.At) > 0))))
                    throw new ArgumentException("Invalid Radiance cure provenance.");
            }
            foreach (var journal in s.Conditions)
                if (journal.Operations.Any(x => x.Kind == ConditionOperationKind.Cure && (x.Subject == "Frightened" || x.Subject == "Poisoned")
                    && !QualifiesCure(s,journal.Target,x))) throw new ArgumentException("Unqualified Cleric condition cure.");
        }
    }
}
