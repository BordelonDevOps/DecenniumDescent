#if DECENNIUM_TEST_ONLY && (UNITY_EDITOR || DEVELOPMENT_BUILD || HEADLESS_TESTS)
using System.Collections.Generic;
using System.Linq;

namespace Decennium.Foundation.Laboratory
{
    /// <summary>Selected-profile extension preserves the exact public shape of predecessor views.</summary>
    public sealed class ExpeditionBishopSettlementView : ExpeditionClericSettlementView
    {
        public string BishopMilestoneId => BishopProfile.Milestone;
        public string BishopObjective => "After earned Cleric 2, complete the first eligible Long Rest, later paid positive Healing Rite care on the hero, then the paid eastward departure from the berth with both alive.";
        public long? BishopCompletedRevision { get; }
        public long? BishopAwardedRevision { get; }
        public long? BishopConsumedRevision { get; }
        public bool DivineInvocationOwned { get; }
        public int? DivineInvocationRecharge { get; }
        public IReadOnlyList<DivineInvocationRecord> InvocationHistory { get; }
        public IReadOnlyList<AuraOfFaithSaveRecord> AuraSaveHistory { get; }
        public IReadOnlyList<AuraOfFaithHealingRecord> AuraHealingHistory { get; }
        public IReadOnlyList<BishopDispelRecord> DispelHistory { get; }
        internal ExpeditionBishopSettlementView(Snapshot s):base(s)
        {
            BishopCompletedRevision=s.BishopEntry.Departure?.Complete==true?s.BishopEntry.Departure.CompletedRevision:(long?)null;
            var award=s.CharacterMilestones.SingleOrDefault(x=>x.ActorId==ClericRpProfile.Actor&&x.MilestoneId==BishopProfile.Milestone);
            BishopAwardedRevision=award?.AwardedRevision;BishopConsumedRevision=award?.ConsumedRevision;
            DivineInvocationOwned=BishopProfile.Earned(s);
            DivineInvocationRecharge=DivineInvocationOwned?s.AbilityRecharges.SingleOrDefault(x=>x.ActorId==ClericRpProfile.Actor&&x.AbilityId==BishopProfile.Invocation)?.Remaining??0:(int?)null;
            InvocationHistory=s.BishopEntry.Invocations;
            // The owned-card view does not publish opponents' event-time senses, life or geometry.
            // Complete causal records remain in the diagnostic snapshot and strict replay.
            AuraSaveHistory=System.Array.AsReadOnly(s.BishopEntry.AuraSaves.Where(x=>PostRecoveryEncounterDefinition.IsParty(x.Qualification.TargetId)).ToArray());
            AuraHealingHistory=s.BishopEntry.AuraHealing;DispelHistory=s.BishopEntry.Dispels;
        }
    }
}
#endif
