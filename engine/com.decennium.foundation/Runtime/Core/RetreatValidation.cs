using System;
using System.Linq;

namespace Decennium.Foundation
{
    public static class RetreatValidation
    {
        public static bool IsCommand(CommandKind kind)
            => kind == CommandKind.DeclareRetreat || kind == CommandKind.AttemptRetreatEscape || kind == CommandKind.AbandonRetreat;

        public static void Validate(Snapshot state)
        {
            var retreat = state.Retreat;
            if (state.SchemaVersion < Snapshot.RetreatSchema) {
                if (retreat != null) throw new ArgumentException("Retreat requires schema 88.");
                return;
            }
            var reinforcement = state.Reinforcement;
            var later = state.LaterEncounter;
            if (!state.TestOnly || retreat == null || reinforcement == null || later == null)
                throw new ArgumentException("Retreat requires the selected TEST_ONLY reinforced world.");
            var d = retreat.Definition;
            if (d.EncounterId != later.Definition.EncounterId || d.LeadId != later.Definition.HeroId
                || d.CompanionId != reinforcement.Definition.CompanionId || d.DefenderId != later.Definition.DefenderId
                || d.ClubId != later.Definition.DefenderClubId)
                throw new ArgumentException("Retreat authority does not match the reinforced encounter.");
            if (retreat.Round == null) return;

            var encounter = EncounterHistory.All(state).SingleOrDefault(x => x.Id == d.EncounterId);
            if (encounter?.RosterPhase == null || retreat.DeclaredRevision != retreat.Rounds[0].StartRevision + 1
                || d.LeadMandateId == "" || d.CompanionConsentId == "" || d.RouteAccessId == "" || retreat.Active && state.Encounter?.Id != d.EncounterId)
                throw new ArgumentException("Invalid retreat declaration or active encounter.");
            AssertInstruction(state, d, retreat.DeclaredRevision, retreat.DeclarationId, CommandKind.DeclareRetreat);
            int escape = 0, pursuit = 0;
            foreach (var round in retreat.Rounds) {
                int index = encounter.ObservedOrdinals.ToList().IndexOf(round.FirstTurn);
                if (index < 0 || !encounter.RosterPhase.Owns(round.FirstTurn)
                    || (round.FirstTurn - encounter.RosterPhase.FirstTurn) % 3 != 0
                    || encounter.StartRevisions[index] != round.StartRevision || encounter.RoundAt(round.FirstTurn) != round.Number
                    || encounter.StartAt(round.FirstTurn) != round.StartedAt)
                    throw new ArgumentException("Retreat round does not start at the actual round boundary.");
                var task = round.Task;
                if (task != null) {
                    AssertInstruction(state, d, task.Revision, task.CommandId, CommandKind.AttemptRetreatEscape);
                    if (task.Turn < round.FirstTurn || task.Turn >= round.FirstTurn + 3 || encounter.ActorAt(task.Turn) != d.LeadId
                        || task.At != encounter.StartAt(task.Turn) || task.Revision <= retreat.DeclaredRevision)
                        throw new ArgumentException("Retreat task is outside the lead's actual regular turn.");
                }
                var threat = round.ThreatId == "" ? null : state.MeleeAttacks.SingleOrDefault(x => x.Id == round.ThreatId);
                if (round.ThreatId != "" && (threat == null || threat.AttackerId != d.DefenderId || threat.TargetId != d.LeadId
                    || threat.WeaponId != d.ClubId || threat.Opportunity || threat.Revision <= retreat.DeclaredRevision
                    || threat.TurnOrdinal < round.FirstTurn || threat.TurnOrdinal >= round.FirstTurn + 3
                    || encounter.ActorAt(threat.TurnOrdinal) != d.DefenderId || threat.At != encounter.StartAt(threat.TurnOrdinal)))
                    throw new ArgumentException("Invalid actual retreat threat.");
                var settlement = round.Settlement;
                if (settlement == null) continue;
                var receipt = RequireReceipt(state, settlement.Revision, settlement.CommandId);
                var command = CommandHistory.Read(receipt);
                if (settlement.At > state.RuleClock || settlement.EndTurn < round.FirstTurn
                    || settlement.EndTurn >= round.FirstTurn + 3 || task?.Revision > settlement.Revision
                    || threat?.Revision > settlement.Revision)
                    throw new ArgumentException("Invalid retreat settlement chronology.");
                if (settlement.Outcome == RetreatOutcome.Abandoned)
                    AssertInstruction(state, d, settlement.Revision, settlement.CommandId, CommandKind.AbandonRetreat);
                else if (settlement.Outcome != RetreatOutcome.OpponentResolved
                    && (command.Kind != CommandKind.EndRegularTurn || settlement.EndTurn != round.FirstTurn + 2
                        || command.Actor != encounter.ActorAt(settlement.EndTurn) || settlement.At != encounter.StartAt(settlement.EndTurn + 1)
                        || command.Target != TurnId(encounter.Id, settlement.EndTurn)))
                    throw new ArgumentException("Retreat settlement requires the actual outgoing End.");
                if (settlement.IncludesExchange) {
                    if (threat == null || threat.Pending || threat.ResolvedRevision > settlement.Revision)
                        throw new ArgumentException("A completed retreat exchange requires its resolved opposing attack.");
                    escape += RetreatRules.Escape(task.Degree);
                    pursuit += RetreatRules.Pursuit(task.Degree);
                    var threshold = RetreatRules.ResolveCounters(escape, pursuit);
                    if (threshold != settlement.Outcome && !(threshold == RetreatOutcome.Successful
                        && settlement.Outcome == RetreatOutcome.PhysicallyBlocked))
                        throw new ArgumentException("Retreat settlement does not follow its earned counters.");
                }
                ValidateCrossing(state, retreat, d.LeadId, settlement.LeadCrossingId, settlement.Lead, settlement);
                ValidateCrossing(state, retreat, d.CompanionId, settlement.CompanionCrossingId, settlement.Companion, settlement);
            }
            var exit = retreat.SuccessfulExit;
            if (exit != null) {
                var closed = state.ClosedEncounters.SingleOrDefault(x => x.Encounter.Id == d.EncounterId);
                if (closed == null || closed.ClosedRevision != exit.Revision || closed.ClosedAt != exit.At
                    || closed.Reason != exit.CommandId || closed.Encounter.TurnOrdinal != exit.EndTurn
                    || state.InventoryCombat && state.Reengagement?.IsSegment(state.Encounter?.Id) != true
                    || exit.LeadCrossingId == "" || exit.CompanionCrossingId == "")
                    throw new ArgumentException("Invalid living-opponent retreat exit provenance.");
            }
        }

        private static void ValidateCrossing(Snapshot s, RetreatRecord retreat, string actor, string id,
            RetreatPosition position, RetreatSettlement settlement)
        {
            if (id == "") return;
            var d = retreat.Definition;
            var move = s.TacticalMoves.SingleOrDefault(x => x.Id == id);
            if (!d.IsCrossing(move) || move.ActorId != actor || move.ResolvedRevision <= retreat.DeclaredRevision
                || move.ResolvedRevision >= settlement.Revision || EncounterHistory.AtRevision(s, move.Revision)?.Id != d.EncounterId
                || !d.IsLanePoint(actor, position.X, position.Y) || position.Y > d.CrossingY)
                throw new ArgumentException("Invalid paid retreat crossing.");
        }

        private static string TurnId(string encounter, int turn)
            => encounter + ".turn." + turn.ToString(System.Globalization.CultureInfo.InvariantCulture);

        private static CommandReceipt RequireReceipt(Snapshot s, long revision, string id)
            => s.Receipts.SingleOrDefault(x => x.Revision == revision && x.Id == id)
                ?? throw new ArgumentException("Retreat receipt is missing.");

        private static void AssertInstruction(Snapshot s, RetreatDefinition d, long revision, string id, CommandKind kind)
        {
            var receipt = RequireReceipt(s, revision, id);
            var command = CommandHistory.Read(receipt);
            if (receipt.Principal != d.ControllerId || command.Kind != kind || command.Actor != d.LeadId || command.Target != d.Id)
                throw new ArgumentException("Invalid retreat command authority or provenance.");
        }
    }
}
