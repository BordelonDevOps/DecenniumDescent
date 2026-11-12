#if DECENNIUM_TEST_ONLY && (UNITY_EDITOR || DEVELOPMENT_BUILD || HEADLESS_TESTS)
using System;
using System.Linq;

namespace Decennium.Foundation.Laboratory
{
    public sealed partial class TestOnlySharedWorldPolicy
    {
        private SurpriseAwarenessBinding surpriseEntryBinding;

        private static bool IsSurpriseEntryQuery(CommandKind kind)
            => kind == CommandKind.AttackClub || kind == CommandKind.AttackUnarmed || kind == CommandKind.HandlePortableEquipment;

        public TestOnlySharedWorldPolicy EnableSurpriseAwareEntry(SurpriseAwareness outcome)
        {
            if (initializationStarted || surpriseEntryBinding != null || SelectedSchema != Snapshot.ReengagementSchema)
                throw new InvalidOperationException("Select the surprise-aware entry on the re-engagement host before initialization.");
            var later = laterEncounterDefinition;
            var binding = new SurpriseAwarenessBinding(SurpriseAwarenessBinding.RuleRevision, SurpriseAwarenessBinding.Director,
                later.EncounterId, later.HeroId, later.DefenderId, SurpriseAwarenessBinding.EvidenceFor(outcome), outcome);
            surpriseEntryBinding = binding;
            ContentFingerprint = "TEST_ONLY.surprise-entry-v1-" + RetreatHash(string.Join("|", ContentFingerprint,
                binding.SourceRevision, binding.DirectorId, binding.EncounterId, binding.ParticipantId, binding.ThreatId,
                binding.EvidenceId));
            return this;
        }

        private void InitializeSurpriseEntry(Snapshot state)
        {
            if (surpriseEntryBinding != null) state.SurpriseEntry = new SurpriseEntryRecord(surpriseEntryBinding);
        }

        private static void ApplySurpriseEntry(Snapshot state, Command arrival)
        {
            var record = state.SurpriseEntry;
            if (record != null)
                state.SurpriseEntry = record.Apply(new SurpriseEntryDecision(state.Revision + 1, arrival.Id, state.RuleClock));
        }

        private static WorldIntervalRecord RecordSurpriseFirstStart(Snapshot state, WorldScheduleRecord epoch,
            long localOrdinal, WorldIntervalRecord refreshed)
        {
            var record = state.SurpriseEntry;
            if (record?.Decision == null || record.FirstStart != null || record.Binding.ParticipantId != refreshed.ActorId
                || record.Binding.EncounterId != state.Encounter?.Id || epoch.Id != state.LaterEncounter.Definition.EpochId
                || epoch.Start(localOrdinal) != state.RuleClock)
                return refreshed;

            int ordinal = checked((int)refreshed.LastStart);
            var before = Interval(state, refreshed.ActorId);
            var reaction = new ReactionClock(before.ReactionAvailable, record.SurprisePending, before.LastStart)
                .RegularStart(ordinal);
            state.SurpriseEntry = record.Start(new SurpriseFirstStart(state.Revision + 1, ordinal, state.RuleClock));
            return refreshed.WithReaction(reaction.Available);
        }

        private static void CompleteSurpriseFirstEnd(Snapshot state, Command cause, ManufacturingAdvanceRecord pendingBefore)
        {
            var record = state.SurpriseEntry;
            var start = record?.FirstStart;
            if (start == null || record.FirstEnd != null || state.ManufacturingAdvance != null || PendingCalendarChoice(state))
                return;
            var binding = record.Binding;
            RuleTime endAt = state.LaterEncounter.Entry.Epoch.Start(start.Ordinal + 1);
            if (state.RuleClock != endAt) return;

            string turnId = start.TurnId(binding.EncounterId);
            if (SurpriseEntryValidation.IsRegularEnd(cause, binding.ParticipantId, turnId))
                state.SurpriseEntry = record.Complete(new SurpriseFirstEnd(state.Revision + 1, cause.Id, state.Revision + 1, endAt));
            else if (pendingBefore?.OutgoingSlotId == turnId && pendingBefore.Target == endAt)
                state.SurpriseEntry = record.Complete(new SurpriseFirstEnd(pendingBefore.CommandRevision,
                    pendingBefore.CommandId, state.Revision + 1, endAt));
        }
    }

    internal static class SurprisePermissions
    {
        public static ConditionPermissions Restrict(Snapshot state, string actor, ConditionPermissions permissions)
        {
            var record = state.SurpriseEntry;
            if (record?.SurprisePending != true || record.Binding.ParticipantId != actor
                || record.Binding.EncounterId != state.Encounter?.Id)
                return permissions;

            var interval = state.WorldIntervals.SingleOrDefault(x => x.ActorId == actor);
            var reaction = new ReactionClock(interval?.ReactionAvailable ?? false, record.SurprisePending,
                interval?.LastStart ?? -1);
            bool firstOwnTurn = record.FirstStart != null && record.FirstStart.Ordinal == state.Encounter.TurnOrdinal;
            return new ConditionPermissions(permissions.Action && !firstOwnTurn, permissions.BonusAction && !firstOwnTurn,
                permissions.Reaction && !reaction.SurprisePending, permissions.VoluntarySpeed && !firstOwnTurn,
                permissions.Dash && !firstOwnTurn, permissions.ConcentrationMayContinue, permissions.MustChooseActionOrMovement);
        }
    }
}
#endif
