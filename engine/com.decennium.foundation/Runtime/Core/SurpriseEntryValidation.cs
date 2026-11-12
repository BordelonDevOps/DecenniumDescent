using System;
using System.Linq;

namespace Decennium.Foundation
{
    public static class SurpriseEntryValidation
    {
        public static bool ConflictingAwareness(Snapshot state, SurpriseAwarenessBinding binding, long arrivalRevision)
        {
            if (binding.Outcome != SurpriseAwareness.Surprised) return false;
            string hero = binding.ParticipantId, threat = binding.ThreatId;
            bool ThreatExchange(string attacker, string target) => attacker == threat && target == hero
                || attacker == hero && target == threat;
            return state.ObserverKnowledge.Any(x => x.ObserverId == hero && x.TargetId == threat
                    && x.Evidence == ObservationEvidenceKind.AttackEvidence && x.EvidenceRevision < arrivalRevision)
                || state.MeleeAttacks.Any(x => x.Revision < arrivalRevision && ThreatExchange(x.AttackerId, x.TargetId))
                || state.RangedAttacks.Any(x => x.Revision < arrivalRevision && ThreatExchange(x.AttackerId, x.TargetId))
                || state.CharacterFeatureGrants.Any(x => x.ActorId == hero && x.FeatureId == "warrior.base.combat-instinct"
                    && x.GrantedRevision < arrivalRevision);
        }

        public static bool IsRegularEnd(Command command, string actor, string turnId)
            => command != null && (command.Kind == CommandKind.EndRegularTurn || command.Kind == CommandKind.EndFixedEncounter)
                && command.Actor == actor && command.Target == turnId;

        public static void Validate(Snapshot state)
        {
            var record = state.SurpriseEntry;
            if (state.SchemaVersion != Snapshot.SurpriseEntrySchema) {
                if (record != null) throw new ArgumentException("Surprise entry requires schema 90.");
                return;
            }
            if (!state.TestOnly || record == null || state.LaterEncounter == null)
                throw new ArgumentException("Missing TEST_ONLY surprise entry authority.");

            var binding = record.Binding;
            var later = state.LaterEncounter;
            if (binding.EncounterId != later.Definition.EncounterId || binding.ParticipantId != later.Definition.HeroId
                || binding.ThreatId != later.Definition.DefenderId)
                throw new ArgumentException("Surprise authority does not identify this genuine encounter and threat.");
            var decision = record.Decision;
            var entry = later.Entry;
            if ((decision == null) != (entry == null))
                throw new ArgumentException("Surprise decision does not match successful genuine entry.");
            if (decision == null) return;

            if (decision.Revision != entry.ArrivalRevision || decision.CommandId != entry.ArrivalCommandId
                || decision.At != entry.Epoch.Origin || ConflictingAwareness(state, binding, decision.Revision))
                throw new ArgumentException("Invalid surprise entry or contradictory awareness.");
            var encounter = EncounterHistory.All(state).Single(x => x.Id == binding.EncounterId);
            int ordinal = Array.IndexOf(entry.Epoch.Order.ToArray(), binding.ParticipantId);
            var start = record.FirstStart;
            int observedStart = Array.IndexOf(encounter.ObservedOrdinals.ToArray(), ordinal);
            if ((start == null) != (observedStart < 0) || start != null && (start.Ordinal != ordinal
                || start.At != entry.Epoch.Start(ordinal) || start.Revision != encounter.StartRevisions[observedStart]))
                throw new ArgumentException("Invalid surprise first regular Start.");

            if (record.SurprisePending && start == null
                && (state.WorldIntervals.Single(x => x.ActorId == binding.ParticipantId).ReactionAvailable
                    || state.TacticalActors.Single(x => x.ActorId == binding.ParticipantId).ReactionAvailable))
                throw new ArgumentException("The surprised participant has no initial Reaction.");
            if (start == null) return;

            var endAt = entry.Epoch.Start(ordinal + 1);
            var end = record.FirstEnd;
            if (end == null) {
                if (state.RuleClock > endAt || state.RuleClock == endAt && state.ManufacturingAdvance == null)
                    throw new ArgumentException("Missing actual surprise first End.");
                return;
            }
            var endReceipt = state.Receipts.SingleOrDefault(x => x.Revision == end.EndRevision && x.Id == end.EndCommandId);
            if (endReceipt == null || !IsRegularEnd(CommandHistory.Read(endReceipt), binding.ParticipantId, start.TurnId(binding.EncounterId))
                || end.At != endAt || state.RuleClock < end.At || end.CompletedRevision > state.Revision)
                throw new ArgumentException("Invalid surprise first-End completion evidence.");
            if (end.CompletedRevision != end.EndRevision) {
                var completion = CommandHistory.Read(state.Receipts.Single(x => x.Revision == end.CompletedRevision));
                if (completion.Kind != CommandKind.ResolveManufacturingQuality && completion.Kind != CommandKind.ResolveExpeditionStrainRecovery
                    && completion.Kind != CommandKind.ResolveRecipe347Quality)
                    throw new ArgumentException("Invalid continuation of the surprise first End.");
            }
        }
    }
}
