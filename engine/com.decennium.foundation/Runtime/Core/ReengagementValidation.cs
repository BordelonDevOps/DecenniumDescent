using System;
using System.Linq;

namespace Decennium.Foundation
{
    public static class ReengagementValidation
    {
        public static void Validate(Snapshot s)
        {
            var r = s.Reengagement;
            if (s.SchemaVersion != Snapshot.ReengagementSchema) {
                if (r != null || s.Encounter?.InheritedPhase != null || s.ClosedEncounters.Any(x => x.Encounter.InheritedPhase != null))
                    throw new ArgumentException("Inherited re-engagement requires schema 89.");
                return;
            }
            if (r == null || s.Retreat == null || !s.TestOnly)
                throw new ArgumentException("Missing selected re-engagement authority.");
            var d = r.Definition;
            var original = s.Retreat.Definition;
            if (d.RootId != original.EncounterId || d.LeadId != original.LeadId || d.CompanionId != original.CompanionId
                || d.DefenderId != original.DefenderId || d.ControllerId != original.ControllerId)
                throw new ArgumentException("Re-engagement does not bind the original opposition and party.");
            var exit = s.Retreat.SuccessfulExit;
            var phase = s.Reinforcement.Admission?.Phase;
            if (r.Contacts.Count != 0 && (exit == null || phase == null || d.ConsentId == "" || d.DirectorMandateId == ""))
                throw new ArgumentException("Contact requires the successful retreat and explicit authority.");
            foreach (var x in r.Contacts) {
                var approach = s.Receipts.SingleOrDefault(c => c.Revision == x.ApproachRevision);
                var arrival = s.Receipts.SingleOrDefault(c => c.Revision == x.ArrivalRevision && c.Id == x.ArrivalCommandId);
                if (approach == null || approach.Principal != d.ControllerId || !d.IsWalk(CommandHistory.Read(approach))
                    || arrival == null || CommandHistory.Read(arrival).Kind != CommandKind.AdvanceClock
                    || x.ApproachRevision <= exit.Revision || x.At <= exit.At || x.At > s.RuleClock
                    || x.MarkerOrdinal >= 0 && (!phase.Owns(x.MarkerOrdinal) || phase.Start(x.MarkerOrdinal) != x.At
                        || phase.Actor(x.MarkerOrdinal) != d.LeadId))
                    throw new ArgumentException("Invalid re-engagement approach, arrival or inherited marker.");
            }

            var all = EncounterHistory.All(s).ToArray();
            var segment = all.SingleOrDefault(x => x.Id == d.SegmentId);
            if (all.Any(x => x.InheritedPhase != null && x.Id != d.SegmentId) || (segment == null) != (r.Entry == null))
                throw new ArgumentException("Invalid re-engagement segment identity.");
            if (segment == null) return;
            var entry = r.Entry;
            var inherited = segment.InheritedPhase;
            if (inherited == null || inherited.Epoch.Id != phase.Epoch.Id || inherited.Epoch.Origin != phase.Epoch.Origin
                || inherited.FirstTurn != phase.FirstTurn || inherited.FirstRound != phase.FirstRound
                || !inherited.Epoch.Order.SequenceEqual(phase.Epoch.Order) || !phase.Epoch.Order.All(d.IsParticipant)
                || segment.Origin != entry.At || segment.StartRevisions[0] != entry.ArrivalRevision
                || segment.ObservedOrdinals[0] != entry.MarkerOrdinal)
                throw new ArgumentException("Invalid inherited re-engagement timing.");
            if (s.Encounter == segment) {
                if (!s.InventoryCombat || segment.TurnOrdinal != phase.GlobalTurn(phase.Epoch.ProcessedSlot))
                    throw new ArgumentException("Invalid active re-engagement interval.");
                return;
            }
            var closed = s.ClosedEncounters.Single(x => x.Encounter.Id == d.SegmentId);
            var end = s.Receipts.SingleOrDefault(c => c.Revision == closed.ClosedRevision && c.Id == closed.Reason);
            var command = end == null ? null : CommandHistory.Read(end);
            if (command?.Kind != CommandKind.EndFixedEncounter || command.Target != segment.CurrentTurnId
                || command.Actor != segment.CurrentActor || closed.ClosedAt != segment.StartAt(segment.TurnOrdinal + 1)
                || !s.Lives.Single(x => x.ActorId == d.DefenderId).Dead)
                throw new ArgumentException("Invalid resolved re-engagement exit provenance.");
        }
    }
}
