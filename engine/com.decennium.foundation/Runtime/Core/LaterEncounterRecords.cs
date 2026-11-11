using System;
using System.Collections.Generic;
using System.Linq;

namespace Decennium.Foundation
{
    public sealed class LaterEncounterDefinition
    {
        public string EncounterId { get; }
        public string EpochId { get; }
        public string HeroId { get; }
        public string DefenderId { get; }
        public string DefenderClubId { get; }
        public string CharacterProfileId { get; }
        public string EngagementId { get; }
        public string TieDecisionId { get; }
        public int FromX => 1;
        public int FromY => 3;
        public int ArrivalX => 0;
        public int ArrivalY => 3;
        public int DefenderX => 0;
        public int DefenderY => 4;
        public int DefenderMaximumHp => 26;
        public int DefenderOpeningHp => 8;
        public int DefenderWalkingSpeed => 30;

        public LaterEncounterDefinition(string encounterId, string epochId, string heroId, string defenderId,
            string defenderClubId, string characterProfileId, string engagementId, string tieDecisionId)
        {
            if (new[] { encounterId, epochId, heroId, defenderId, defenderClubId, characterProfileId,
                    engagementId, tieDecisionId }.Any(id => !Validation.ValidId(id))
                || heroId == defenderId || encounterId == epochId)
                throw new ArgumentException("Invalid later encounter definition.");
            EncounterId = encounterId;
            EpochId = epochId;
            HeroId = heroId;
            DefenderId = defenderId;
            DefenderClubId = defenderClubId;
            CharacterProfileId = characterProfileId;
            EngagementId = engagementId;
            TieDecisionId = tieDecisionId;
        }

        public bool IsApproach(WorldTraversalRecord edge) => edge.ActorId == HeroId && !edge.Running
            && edge.FromX == FromX && edge.FromY == FromY && edge.ToX == ArrivalX && edge.ToY == ArrivalY;
    }

    public sealed class LaterInitiativeDraw
    {
        public string ActorId { get; }
        public int Natural { get; }
        public int DexterityModifier { get; }
        public int Bonus { get; }
        public int Total => checked(Natural + DexterityModifier + Bonus);
        public uint RandomBefore { get; }
        public uint RandomAfter { get; }
        public int WordsConsumed { get; }

        public LaterInitiativeDraw(string actorId, int natural, int dexterityModifier, int bonus,
            uint randomBefore, uint randomAfter, int wordsConsumed)
        {
            if (!Validation.ValidId(actorId) || natural < 1 || natural > 20 || dexterityModifier < -5
                || dexterityModifier > 10 || randomBefore == 0 || randomAfter == 0 || wordsConsumed < 1)
                throw new ArgumentException("Invalid later initiative draw.");
            ActorId = actorId;
            Natural = natural;
            DexterityModifier = dexterityModifier;
            Bonus = bonus;
            _ = Total;
            RandomBefore = randomBefore;
            RandomAfter = randomAfter;
            WordsConsumed = wordsConsumed;
        }
    }

    public sealed class LaterEncounterEntry
    {
        public WorldScheduleRecord Epoch { get; }
        public long ApproachRevision { get; }
        public long ArrivalRevision { get; }
        public string ArrivalCommandId { get; }
        public RuleTime RequestedUntil { get; }
        public IReadOnlyList<LaterInitiativeDraw> Draws { get; }
        public WorldIntervalRecord HeroExpenditureAtArrival { get; }
        public bool Tied => Draws[0].Total == Draws[1].Total;

        public LaterEncounterEntry(WorldScheduleRecord epoch, long approachRevision, long arrivalRevision,
            string arrivalCommandId, RuleTime requestedUntil, IEnumerable<LaterInitiativeDraw> draws, WorldIntervalRecord heroExpenditure)
        {
            var rows = draws?.ToArray();
            if (epoch == null || epoch.Order.Count != 2 || approachRevision < 1 || arrivalRevision <= approachRevision
                || !Validation.ValidId(arrivalCommandId) || requestedUntil < epoch.Origin || heroExpenditure == null
                || rows == null || rows.Length != 2 || rows.Any(x => x == null)
                || StringComparer.Ordinal.Compare(rows[0].ActorId, rows[1].ActorId) >= 0
                || rows[0].RandomAfter != rows[1].RandomBefore)
                throw new ArgumentException("Invalid later encounter entry.");
            Epoch = epoch;
            ApproachRevision = approachRevision;
            ArrivalRevision = arrivalRevision;
            ArrivalCommandId = arrivalCommandId;
            RequestedUntil = requestedUntil;
            Draws = Array.AsReadOnly(rows);
            HeroExpenditureAtArrival = heroExpenditure;
        }

        public LaterEncounterEntry At(long slot) => slot == Epoch.ProcessedSlot ? this
            : new LaterEncounterEntry(Epoch.At(slot), ApproachRevision, ArrivalRevision, ArrivalCommandId, RequestedUntil,
                Draws, HeroExpenditureAtArrival);
    }

    public sealed class LaterEncounterInterruption
    {
        public long ApproachRevision { get; }
        public long Revision { get; }
        public string CommandId { get; }
        public RuleTime At { get; }
        public string Reason { get; }

        public LaterEncounterInterruption(long approachRevision, long revision, string commandId, RuleTime at, string reason)
        {
            if (approachRevision < 1 || revision <= approachRevision || !Validation.ValidId(commandId) || !Validation.ValidId(reason))
                throw new ArgumentException("Invalid interrupted later encounter entry.");
            ApproachRevision = approachRevision;
            Revision = revision;
            CommandId = commandId;
            At = at;
            Reason = reason;
        }
    }

    public sealed class LaterEncounterRecord
    {
        public LaterEncounterDefinition Definition { get; }
        public ClosedEncounterRecord FirstExit { get; }
        public LaterEncounterEntry Entry { get; }
        public IReadOnlyList<LaterEncounterInterruption> Interruptions { get; }

        public LaterEncounterRecord(LaterEncounterDefinition definition, ClosedEncounterRecord firstExit = null,
            LaterEncounterEntry entry = null, IEnumerable<LaterEncounterInterruption> interruptions = null)
        {
            Definition = definition ?? throw new ArgumentNullException(nameof(definition));
            var stops = (interruptions ?? Array.Empty<LaterEncounterInterruption>()).ToArray();
            if (stops.Length > Validation.MaxReceipts || stops.Any(x => x == null)
                || stops.Skip(1).Where((x, i) => x.Revision <= stops[i].Revision || x.At < stops[i].At).Any()
                || stops.Any(x => firstExit == null || x.ApproachRevision <= firstExit.ClosedRevision
                    || entry != null && x.Revision >= entry.ApproachRevision))
                throw new ArgumentException("Invalid later encounter interruption history.");
            if (entry != null && (firstExit == null || entry.ApproachRevision <= firstExit.ClosedRevision
                || entry.Epoch.Origin < firstExit.ClosedAt || entry.Epoch.Id != definition.EpochId
                || entry.HeroExpenditureAtArrival.ActorId != definition.HeroId
                || !entry.Draws.Select(x => x.ActorId).OrderBy(x => x, StringComparer.Ordinal)
                    .SequenceEqual(new[] { definition.HeroId, definition.DefenderId }.OrderBy(x => x, StringComparer.Ordinal))
                || !entry.Epoch.Order.SequenceEqual(entry.Draws.OrderByDescending(x => x.Total)
                    .ThenBy(x => x.ActorId != definition.DefenderId).Select(x => x.ActorId))))
                throw new ArgumentException("Invalid later encounter timeline.");
            FirstExit = firstExit;
            Entry = entry;
            Interruptions = Array.AsReadOnly(stops);
        }

        public LaterEncounterRecord WithFirstExit(ClosedEncounterRecord exit) => new LaterEncounterRecord(Definition, exit);
        public LaterEncounterRecord WithEntry(LaterEncounterEntry entry) => new LaterEncounterRecord(Definition, FirstExit, entry, Interruptions);
        public LaterEncounterRecord Interrupted(LaterEncounterInterruption interruption)
            => new LaterEncounterRecord(Definition, FirstExit, Entry, Interruptions.Append(interruption));
    }

    /// <summary>One current interval per actor. The predecessor calendar still owns remote activity
    /// and earlier virtual markers, including for actors whose spendable interval has changed owner.</summary>
    public static class WorldTiming
    {
        public static WorldScheduleRecord ForActor(Snapshot state, string actor)
        {
            var later = state.LaterEncounter?.Entry?.Epoch;
            if (later != null && later.Order.Contains(actor)) return later;
            var earlier = state.WorldSchedule;
            return earlier != null && earlier.Order.Contains(actor) ? earlier : null;
        }

        public static WorldScheduleRecord FindEpoch(Snapshot state, string id)
        {
            if (state.WorldSchedule?.Id == id) return state.WorldSchedule;
            var later = state.LaterEncounter?.Entry?.Epoch;
            return later?.Id == id ? later : null;
        }

        public static WorldScheduleRecord ForEncounter(Snapshot state) =>
            IsLaterActive(state) ? state.LaterEncounter.Entry.Epoch : state.WorldSchedule;

        public static bool IsLaterActive(Snapshot state) => state.LaterEncounter?.Entry != null
            && state.Encounter?.Id == state.LaterEncounter.Definition.EncounterId;

        public static IEnumerable<string> IntervalActors(Snapshot state)
        {
            if (state.WorldSchedule == null) return Array.Empty<string>();
            var later = state.LaterEncounter?.Entry?.Epoch;
            return later == null ? state.WorldSchedule.Order : state.WorldSchedule.Order.Union(later.Order, StringComparer.Ordinal);
        }
    }

    public static class LaterEncounterValidation
    {
        public static void Validate(Snapshot state)
        {
            var later = state.LaterEncounter;
            if (state.SchemaVersion != Snapshot.LaterEncounterSchema) {
                if (later != null) throw new ArgumentException("Later encounter requires schema 86.");
                return;
            }
            if (later == null || !state.TestOnly || state.WorldSchedule == null)
                throw new ArgumentException("Later encounter requires selected TEST_ONLY world authority.");
            var definition = later.Definition;
            if (!state.WorldSchedule.Order.Contains(definition.HeroId)
                || state.WorldSchedule.Order.Contains(definition.DefenderId)
                || !state.Actors.Any(x => x.Id == definition.DefenderId)
                || !state.Characters.Any(x => x.ActorId == definition.DefenderId && x.ProfileId == definition.CharacterProfileId)
                || !state.Clubs.Any(x => x.Id == definition.DefenderClubId))
                throw new ArgumentException("Invalid later encounter actor registration.");
            if (later.FirstExit != null) ValidateExit(state, later.FirstExit);
            foreach (var stop in later.Interruptions) {
                var cause = ReceiptCommand(state, stop.Revision);
                if (cause.Kind != CommandKind.AdvanceClock || cause.Id != stop.CommandId || stop.At > state.RuleClock
                    || !IsApproach(definition, ReceiptCommand(state, stop.ApproachRevision)))
                    throw new ArgumentException("Invalid interrupted approach provenance.");
            }
            var entry = later.Entry;
            if (entry == null) {
                if (state.ClosedEncounters.Length != 0) throw new ArgumentException("Premature later encounter archive.");
                return;
            }
            if (entry.Epoch.Origin > state.RuleClock || entry.Epoch.ProcessedSlot != entry.Epoch.SlotAt(state.RuleClock)
                || entry.Epoch.Id == state.WorldSchedule.Id)
                throw new ArgumentException("Invalid later encounter epoch.");
            var approach = ReceiptCommand(state, entry.ApproachRevision);
            var arrival = ReceiptCommand(state, entry.ArrivalRevision);
            if (!IsApproach(definition, approach) || arrival.Kind != CommandKind.AdvanceClock || arrival.Id != entry.ArrivalCommandId)
                throw new ArgumentException("Invalid later encounter approach provenance.");

            var first = state.ClosedEncounters.SingleOrDefault(x => x.Encounter.Id == later.FirstExit.Encounter.Id);
            if (!SameExit(first, later.FirstExit)) throw new ArgumentException("Invalid first encounter archive.");
            var live = state.Encounter;
            var closed = state.ClosedEncounters.SingleOrDefault(x => x.Encounter.Id == definition.EncounterId);
            if (closed != null) ValidateExit(state, closed);
            var encounter = live ?? closed?.Encounter;
            if (encounter == null || encounter.Id != definition.EncounterId || encounter.Origin != entry.Epoch.Origin
                || encounter.StartRevisions[0] != entry.ArrivalRevision || encounter.ObservedOrdinals[0] != 0
                || !encounter.Order.SequenceEqual(entry.Epoch.Order)
                || (state.InventoryCombat ? closed != null || live == null || live.TurnOrdinal != entry.Epoch.ProcessedSlot
                    : closed == null || live != null))
                throw new ArgumentException("Invalid later encounter history.");
        }

        private static bool IsApproach(LaterEncounterDefinition definition, Command command)
            => command.Kind == CommandKind.BeginWorldStep && command.Actor == definition.HeroId && command.Target == "walk"
                && command.X == definition.ArrivalX - definition.FromX && command.Y == definition.ArrivalY - definition.FromY;

        private static Command ReceiptCommand(Snapshot state, long revision)
        {
            var receipt = state.Receipts.SingleOrDefault(x => x.Revision == revision);
            if (receipt == null) throw new ArgumentException("Later encounter receipt missing.");
            return CommandHistory.Read(receipt);
        }

        private static void ValidateExit(Snapshot state, ClosedEncounterRecord exit)
        {
            var command = ReceiptCommand(state, exit.ClosedRevision);
            if (exit.ClosedAt > state.RuleClock || command.Kind != CommandKind.EndFixedEncounter
                || command.Id != exit.Reason || command.Actor != exit.Encounter.CurrentActor || command.Target != exit.Encounter.CurrentTurnId)
                throw new ArgumentException("Invalid later encounter exit provenance.");
        }

        private static bool SameExit(ClosedEncounterRecord a, ClosedEncounterRecord b) => a != null
            && a.ClosedRevision == b.ClosedRevision && a.ClosedAt == b.ClosedAt && a.Reason == b.Reason
            && a.Encounter.Id == b.Encounter.Id && a.Encounter.Origin == b.Encounter.Origin
            && a.Encounter.Order.SequenceEqual(b.Encounter.Order)
            && a.Encounter.StartRevisions.SequenceEqual(b.Encounter.StartRevisions)
            && a.Encounter.ObservedOrdinals.SequenceEqual(b.Encounter.ObservedOrdinals);
    }
}
