using System;
using System.Collections.Generic;
using System.Linq;

namespace Decennium.Foundation
{
    public enum ReinforcementEventKind { Began = 1, Suspended, Resumed, Arrived, Deferred, Cancelled, NoLongerNeeded, Admitted }

    public sealed class ReinforcementDefinition
    {
        public string Id { get; }
        public string EncounterId { get; }
        public string EpochId { get; }
        public string CompanionId { get; }
        public string AllyId { get; }
        public string ControllerId { get; }
        public string ParticipationMandateId { get; }
        public string AlliedSideId { get; }
        public string PlayerTieChoiceId { get; }
        public string DirectorTieChoiceId { get; }
        public string AwarenessPolicyId => "TEST_ONLY.mutual-ally-and-entrant-defender-sight.v1";
        public int FromX => 2;
        public int FromY => 3;
        public int EntryX => 1;
        public int EntryY => 3;

        public ReinforcementDefinition(string id, string encounterId, string epochId, string companionId, string allyId,
            string controllerId, string participationMandateId, string alliedSideId, string playerTieChoiceId, string directorTieChoiceId)
        {
            if (new[] { id, encounterId, epochId, companionId, allyId, controllerId }.Any(x => !Validation.ValidId(x))
                || new[] { participationMandateId, alliedSideId, playerTieChoiceId, directorTieChoiceId }
                    .Any(x => x != "" && !Validation.ValidId(x)) || companionId == allyId)
                throw new ArgumentException("Invalid reinforcement definition.");
            Id = id;
            EncounterId = encounterId;
            EpochId = epochId;
            CompanionId = companionId;
            AllyId = allyId;
            ControllerId = controllerId;
            ParticipationMandateId = participationMandateId;
            AlliedSideId = alliedSideId;
            PlayerTieChoiceId = playerTieChoiceId;
            DirectorTieChoiceId = directorTieChoiceId;
        }

        public bool Matches(WorldTraversalRecord edge) => edge != null && edge.ActorId == CompanionId && !edge.Running
            && edge.FromX == FromX && edge.FromY == FromY && edge.ToX == EntryX && edge.ToY == EntryY;
    }

    public sealed class ReinforcementEvent
    {
        public ReinforcementEventKind Kind { get; }
        public long Revision { get; }
        public string CommandId { get; }
        public RuleTime At { get; }
        public string Reason { get; }
        public RuleQuantity Distance { get; }

        public ReinforcementEvent(ReinforcementEventKind kind, long revision, string commandId, RuleTime at,
            string reason, RuleQuantity distance)
        {
            if (!Enum.IsDefined(typeof(ReinforcementEventKind), kind) || revision < 1 || !Validation.ValidId(commandId)
                || !Validation.ValidId(reason) || distance > new RuleQuantity(5))
                throw new ArgumentException("Invalid reinforcement event.");
            Kind = kind;
            Revision = revision;
            CommandId = commandId;
            At = at;
            Reason = reason;
            Distance = distance;
        }
    }

    /// <summary>Historical values at transfer. Only Snapshot.WorldIntervals remains spendable.</summary>
    public sealed class ReinforcementCarry
    {
        public WorldIntervalRecord Interval { get; }
        public bool BonusActionAvailable { get; }

        public ReinforcementCarry(WorldIntervalRecord interval, bool bonusActionAvailable)
        {
            Interval = interval ?? throw new ArgumentNullException(nameof(interval));
            BonusActionAvailable = bonusActionAvailable;
        }
    }

    public sealed class ReinforcementAdmission
    {
        public EncounterRosterPhase Phase { get; }
        public LaterInitiativeDraw Draw { get; }
        public IReadOnlyList<ReinforcementCarry> Carried { get; }

        public ReinforcementAdmission(EncounterRosterPhase phase, LaterInitiativeDraw draw, IEnumerable<ReinforcementCarry> carried)
        {
            Phase = phase ?? throw new ArgumentNullException(nameof(phase));
            Draw = draw ?? throw new ArgumentNullException(nameof(draw));
            var rows = carried?.ToArray();
            if (phase.Epoch.Order.Count != 3 || rows == null || rows.Length != 3 || rows.Any(x => x == null)
                || !phase.Epoch.Order.OrderBy(x => x, StringComparer.Ordinal)
                    .SequenceEqual(rows.Select(x => x.Interval.ActorId).OrderBy(x => x, StringComparer.Ordinal))
                || !phase.Epoch.Order.Contains(draw.ActorId))
                throw new ArgumentException("Invalid reinforcement admission.");
            Carried = Array.AsReadOnly(rows.OrderBy(x => x.Interval.ActorId, StringComparer.Ordinal).ToArray());
        }

        public ReinforcementAdmission At(long slot) => slot == Phase.Epoch.ProcessedSlot ? this
            : new ReinforcementAdmission(new EncounterRosterPhase(Phase.Epoch.At(slot), Phase.FirstTurn, Phase.FirstRound), Draw, Carried);
    }

    public sealed class ReinforcementRecord
    {
        public ReinforcementDefinition Definition { get; }
        public IReadOnlyList<ReinforcementEvent> Events { get; }
        public ReinforcementAdmission Admission { get; }
        public ReinforcementEvent Began => Find(ReinforcementEventKind.Began);
        public ReinforcementEvent Arrival => Find(ReinforcementEventKind.Arrived);
        public ReinforcementEvent Joined => Find(ReinforcementEventKind.Admitted);
        public ReinforcementEvent Ended => Events.SingleOrDefault(x => x.Kind == ReinforcementEventKind.Cancelled
            || x.Kind == ReinforcementEventKind.NoLongerNeeded);
        public bool Pending => Began != null && Ended == null && Admission == null;

        public ReinforcementRecord(ReinforcementDefinition definition, IEnumerable<ReinforcementEvent> events = null,
            ReinforcementAdmission admission = null)
        {
            Definition = definition ?? throw new ArgumentNullException(nameof(definition));
            var rows = (events ?? Array.Empty<ReinforcementEvent>()).ToArray();
            if (rows.Length > 2 * Validation.MaxReceipts || rows.Any(x => x == null)
                || rows.Length > 0 && rows[0].Kind != ReinforcementEventKind.Began
                || rows.Skip(1).Where((x, i) => x.Revision < rows[i].Revision || x.At < rows[i].At).Any()
                || rows.GroupBy(x => x.Kind).Any(x => x.Key != ReinforcementEventKind.Suspended && x.Key != ReinforcementEventKind.Resumed
                    && x.Key != ReinforcementEventKind.Deferred && x.Count() > 1)
                || rows.Count(x => x.Kind == ReinforcementEventKind.Cancelled || x.Kind == ReinforcementEventKind.NoLongerNeeded) > 1)
                throw new ArgumentException("Invalid reinforcement history.");
            Events = Array.AsReadOnly(rows);
            Admission = admission;
            if ((admission != null) != (Joined != null)
                || Arrival != null && (Arrival.Revision <= Began.Revision || Arrival.Distance != new RuleQuantity(5))
                || admission != null && (Arrival == null || Ended != null || Joined != rows.Last()
                    || Joined.At != admission.Phase.Epoch.Origin || Joined.Revision < Arrival.Revision
                    || admission.Draw.ActorId != definition.CompanionId || admission.Phase.Epoch.Id != definition.EpochId)
                || Ended != null && Ended != rows.Last())
                throw new ArgumentException("Invalid reinforcement stage.");
        }
        private ReinforcementEvent Find(ReinforcementEventKind kind) => Events.SingleOrDefault(x => x.Kind == kind);
        public ReinforcementRecord Append(ReinforcementEvent entry, ReinforcementAdmission admission = null)
            => new ReinforcementRecord(Definition, Events.Append(entry), admission ?? Admission);
        public ReinforcementRecord At(long slot) => new ReinforcementRecord(Definition, Events, Admission.At(slot));
        public bool OwnsApproach(WorldTraversalRecord edge) => Began != null && Definition.Matches(edge) && edge.StartedRevision == Began.Revision;
    }

    public static class ReinforcementValidation
    {
        public static bool IsInstruction(CommandKind kind) => kind == CommandKind.BeginReinforcementApproach
            || kind == CommandKind.CancelReinforcementApproach;

        public static IEnumerable<string> Order(IEnumerable<LaterInitiativeDraw> incumbents, LaterInitiativeDraw entrant)
            => incumbents.Append(entrant).OrderByDescending(x => x.Total).Select(x => x.ActorId);

        public static void Validate(Snapshot state)
        {
            var reinforcement = state.Reinforcement;
            if (state.SchemaVersion != Snapshot.ReinforcementSchema) {
                if (reinforcement != null) throw new ArgumentException("Reinforcement requires schema 87.");
                return;
            }
            var later = state.LaterEncounter;
            if (reinforcement == null || later == null || !state.TestOnly)
                throw new ArgumentException("Reinforcement requires selected TEST_ONLY world authority.");
            var definition = reinforcement.Definition;
            if (definition.EncounterId != later.Definition.EncounterId || definition.AllyId != later.Definition.HeroId
                || definition.CompanionId == later.Definition.DefenderId
                || !state.Actors.Any(x => x.Id == definition.CompanionId)
                || definition.EpochId == state.WorldSchedule.Id || definition.EpochId == later.Definition.EpochId)
                throw new ArgumentException("Invalid reinforcement authority binding.");

            var phased = EncounterHistory.All(state).Where(x => x.RosterPhase != null).ToArray();
            if (phased.Any(x => x.Id != definition.EncounterId))
                throw new ArgumentException("An unrelated encounter cannot acquire a reinforcement phase.");
            var encounter = EncounterHistory.All(state).SingleOrDefault(x => x.Id == definition.EncounterId);
            if (reinforcement.Began != null && (encounter == null
                || new[] { definition.ParticipationMandateId, definition.AlliedSideId, definition.PlayerTieChoiceId,
                    definition.DirectorTieChoiceId }.Any(x => x == "")
                || !state.TacticalAllies.Any(x => x.Includes(definition.CompanionId) && x.Other(definition.CompanionId) == definition.AllyId)))
                throw new ArgumentException("An attempted approach requires recorded participation, alliance and tie authority.");

            foreach (var entry in reinforcement.Events) {
                var receipt = state.Receipts.SingleOrDefault(x => x.Revision == entry.Revision);
                if (receipt == null || receipt.Id != entry.CommandId || entry.At > state.RuleClock || later.Entry == null
                    || entry.Revision <= later.Entry.ArrivalRevision || entry.At < later.Entry.Epoch.Origin)
                    throw new ArgumentException("Invalid reinforcement receipt.");
                var command = CommandHistory.Read(receipt);
                switch (entry.Kind) {
                    case ReinforcementEventKind.Began:
                    case ReinforcementEventKind.Cancelled:
                        var expected = entry.Kind == ReinforcementEventKind.Began ? CommandKind.BeginReinforcementApproach
                            : CommandKind.CancelReinforcementApproach;
                        if (command.Kind != expected || command.Actor != definition.CompanionId || command.Target != definition.Id
                            || receipt.Principal != definition.ControllerId)
                            throw new ArgumentException("Invalid reinforcement consent or cancellation receipt.");
                        break;
                    case ReinforcementEventKind.Arrived:
                    case ReinforcementEventKind.Deferred:
                    case ReinforcementEventKind.Admitted:
                        int ordinal = encounter.ObservedOrdinals.Where((_, index) => encounter.StartRevisions[index] < entry.Revision)
                            .DefaultIfEmpty(-1).Last();
                        if (command.Kind != CommandKind.EndRegularTurn || ordinal < 0
                            || command.Actor != encounter.ActorAt(ordinal)
                            || command.Target != encounter.Id + ".turn." + ordinal.ToString(System.Globalization.CultureInfo.InvariantCulture)
                            || entry.At <= encounter.StartAt(ordinal) || entry.At > encounter.StartAt(ordinal + 1)
                            || entry.Kind != ReinforcementEventKind.Arrived
                                && ((ordinal + 1) % encounter.InitialOrder.Count != 0 || entry.At != encounter.StartAt(ordinal + 1)))
                            throw new ArgumentException("Invalid reinforcement boundary command.");
                        break;
                }
            }

            var admission = reinforcement.Admission;
            if (admission == null) {
                if (encounter?.RosterPhase != null) throw new ArgumentException("Premature reinforcement phase.");
                return;
            }
            var phase = admission.Phase;
            if (encounter?.RosterPhase == null || phase.Epoch.ProcessedSlot != phase.Epoch.SlotAt(state.RuleClock)
                || encounter.RosterPhase.Epoch.Id != phase.Epoch.Id || encounter.RosterPhase.Epoch.Origin != phase.Epoch.Origin
                || !encounter.RosterPhase.Epoch.Order.SequenceEqual(phase.Epoch.Order)
                || encounter.RosterPhase.FirstTurn != phase.FirstTurn || encounter.RosterPhase.FirstRound != phase.FirstRound
                || !phase.Epoch.Order.SequenceEqual(Order(later.Entry.Draws.OrderBy(x => Array.IndexOf(later.Entry.Epoch.Order.ToArray(), x.ActorId)),
                    admission.Draw)))
                throw new ArgumentException("Invalid admitted reinforcement phase.");

            var join = reinforcement.Joined;
            var joinCommand = CommandHistory.Read(state.Receipts.Single(x => x.Revision == join.Revision));
            int outgoing = phase.FirstTurn - 1;
            if (joinCommand.Kind != CommandKind.EndRegularTurn || joinCommand.Actor != encounter.ActorAt(outgoing)
                || joinCommand.Target != encounter.Id + ".turn." + outgoing.ToString(System.Globalization.CultureInfo.InvariantCulture)
                || encounter.StartRevisions[encounter.ObservedOrdinals.ToList().IndexOf(phase.FirstTurn)] != join.Revision)
                throw new ArgumentException("Invalid end-round admission provenance.");
        }
    }
}
