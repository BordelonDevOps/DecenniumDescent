using System;
using System.Collections.Generic;
using System.Linq;

namespace Decennium.Foundation
{
    public enum RetreatTaskDegree { CriticalFailure, Failure, Success, CriticalSuccess }
    public enum RetreatOutcome { Continue, Successful, Failed, Incomplete, PhysicallyBlocked, Abandoned, OpponentResolved }

    public sealed class RetreatDefinition
    {
        public string Id { get; }
        public string EncounterId { get; }
        public string LeadId { get; }
        public string CompanionId { get; }
        public string DefenderId { get; }
        public string ClubId { get; }
        public string ControllerId { get; }
        public string LeadMandateId { get; }
        public string CompanionConsentId { get; }
        public string OperationId { get; }
        public string RouteId { get; }
        public string RouteAccessId { get; }
        public string RouteFingerprint { get; }
        public string CohortId { get; }
        public string ExposureId { get; }
        public ExpeditionRouteQuality Quality => ExpeditionRouteQuality.Known;
        public int Risk => 1;
        public int InitialPressure => 1;
        public int TaskDc => 12;
        public int CrossingY => 1;
        public int RouteCapacity => 2;

        public RetreatDefinition(string id, string encounterId, string leadId, string companionId, string defenderId,
            string clubId, string controllerId, string leadMandateId, string companionConsentId, string operationId,
            string routeId, string routeAccessId, string routeFingerprint, string cohortId, string exposureId)
        {
            if (new[] { id, encounterId, leadId, companionId, defenderId, clubId, controllerId, operationId, routeId,
                routeFingerprint, cohortId, exposureId }.Any(x => !Validation.ValidId(x))
                || new[] { leadMandateId, companionConsentId, routeAccessId }.Any(x => x != "" && !Validation.ValidId(x))
                || new[] { leadId, companionId, defenderId }.Distinct(StringComparer.Ordinal).Count() != 3)
                throw new ArgumentException("Invalid retreat definition.");
            Id = id;
            EncounterId = encounterId;
            LeadId = leadId;
            CompanionId = companionId;
            DefenderId = defenderId;
            ClubId = clubId;
            ControllerId = controllerId;
            LeadMandateId = leadMandateId;
            CompanionConsentId = companionConsentId;
            OperationId = operationId;
            RouteId = routeId;
            RouteAccessId = routeAccessId;
            RouteFingerprint = routeFingerprint;
            CohortId = cohortId;
            ExposureId = exposureId;
        }

        public bool IsWithdrawing(string actor) => actor == LeadId || actor == CompanionId;
        public int LaneX(string actor) => actor == LeadId ? 0 : actor == CompanionId ? 1 : -1;
        public bool IsLanePoint(string actor, int x, int y) => IsWithdrawing(actor) && x == LaneX(actor) && y >= 0 && y <= 3;
        public bool IsCrossing(TacticalMoveRecord move) => move != null && move.Status == TacticalMoveStatus.Completed
            && move.Kind == TacticalMoveKind.Ordinary && IsLanePoint(move.ActorId, move.ToX, move.ToY)
            && move.FromX == move.ToX && move.FromY == CrossingY + 1 && move.ToY == CrossingY;
    }

    public static class RetreatRules
    {
        public static int Escape(RetreatTaskDegree degree) => degree == RetreatTaskDegree.CriticalSuccess ? 2
            : degree == RetreatTaskDegree.Success ? 1 : 0;
        public static int Pursuit(RetreatTaskDegree degree) => degree == RetreatTaskDegree.CriticalFailure ? 2
            : degree == RetreatTaskDegree.Failure ? 1 : 0;
        public static RetreatOutcome ResolveCounters(int escape, int pursuit)
            => pursuit >= 3 ? RetreatOutcome.Failed : escape >= 3 ? RetreatOutcome.Successful : RetreatOutcome.Continue;
    }

    public sealed class RetreatTaskRecord
    {
        public long Revision { get; }
        public string CommandId { get; }
        public RuleTime At { get; }
        public int Turn { get; }
        public int Modifier { get; }
        public int First { get; }
        public int Second { get; }
        public int Natural => Second == 0 ? First : Math.Min(First, Second);
        public uint RandomBefore { get; }
        public uint RandomAfter { get; }
        public long WordsConsumed { get; }
        public RetreatTaskDegree Degree { get; }

        public RetreatTaskRecord(long revision, string commandId, RuleTime at, int turn, int modifier, int first, int second,
            uint randomBefore, uint randomAfter, long wordsConsumed, RetreatTaskDegree degree)
        {
            if (revision < 1 || !Validation.ValidId(commandId) || turn < 0 || first < 1 || first > 20 || second < 0
                || second > 20 || randomBefore == 0 || randomAfter == 0 || wordsConsumed < 1
                || !Enum.IsDefined(typeof(RetreatTaskDegree), degree))
                throw new ArgumentException("Invalid retreat task evidence.");
            var a = DiceStream.Draw(randomBefore, 20);
            var b = second == 0 ? a : DiceStream.Draw(a.NextState, 20);
            if (a.Value + 1 != first || second != 0 && b.Value + 1 != second || b.NextState != randomAfter
                || a.WordsConsumed + (second == 0 ? 0 : b.WordsConsumed) != wordsConsumed)
                throw new ArgumentException("Retreat task evidence does not match the shared RNG.");
            Revision = revision;
            CommandId = commandId;
            At = at;
            Turn = turn;
            Modifier = modifier;
            First = first;
            Second = second;
            RandomBefore = randomBefore;
            RandomAfter = randomAfter;
            WordsConsumed = wordsConsumed;
            Degree = degree;
        }
    }

    public readonly struct RetreatPosition
    {
        public int X { get; }
        public int Y { get; }
        public RetreatPosition(int x, int y) { X = x; Y = y; }
    }

    public sealed class RetreatSettlement
    {
        public RetreatOutcome Outcome { get; }
        public long Revision { get; }
        public string CommandId { get; }
        public RuleTime At { get; }
        public int EndTurn { get; }
        public RetreatPosition Lead { get; }
        public RetreatPosition Companion { get; }
        public RetreatPosition Defender { get; }
        public string LeadCrossingId { get; }
        public string CompanionCrossingId { get; }
        public bool IncludesExchange => Outcome == RetreatOutcome.Continue || Outcome == RetreatOutcome.Successful
            || Outcome == RetreatOutcome.Failed || Outcome == RetreatOutcome.PhysicallyBlocked;

        public RetreatSettlement(RetreatOutcome outcome, long revision, string commandId, RuleTime at, int endTurn,
            RetreatPosition lead, RetreatPosition companion, RetreatPosition defender, string leadCrossingId, string companionCrossingId)
        {
            if (!Enum.IsDefined(typeof(RetreatOutcome), outcome) || revision < 1 || !Validation.ValidId(commandId) || endTurn < 0
                || new[] { leadCrossingId, companionCrossingId }.Any(x => x != "" && !Validation.ValidId(x)))
                throw new ArgumentException("Invalid retreat settlement.");
            Outcome = outcome;
            Revision = revision;
            CommandId = commandId;
            At = at;
            EndTurn = endTurn;
            Lead = lead;
            Companion = companion;
            Defender = defender;
            LeadCrossingId = leadCrossingId;
            CompanionCrossingId = companionCrossingId;
        }
    }

    public sealed class RetreatRound
    {
        public long Number { get; }
        public int FirstTurn { get; }
        public long StartRevision { get; }
        public RuleTime StartedAt { get; }
        public RetreatTaskRecord Task { get; }
        public string ThreatId { get; }
        public RetreatSettlement Settlement { get; }

        public RetreatRound(long number, int firstTurn, long startRevision, RuleTime startedAt,
            RetreatTaskRecord task = null, string threatId = "", RetreatSettlement settlement = null)
        {
            if (number < 2 || firstTurn < 2 || startRevision < 1 || threatId != "" && !Validation.ValidId(threatId)
                || task != null && (task.Revision <= startRevision || task.At < startedAt || task.Turn < firstTurn)
                || settlement != null && (settlement.Revision <= startRevision || settlement.At < startedAt
                    || settlement.IncludesExchange && (task == null || threatId == "")))
                throw new ArgumentException("Invalid retreat round.");
            Number = number;
            FirstTurn = firstTurn;
            StartRevision = startRevision;
            StartedAt = startedAt;
            Task = task;
            ThreatId = threatId;
            Settlement = settlement;
        }

        public RetreatRound WithTask(RetreatTaskRecord task) => new RetreatRound(Number, FirstTurn, StartRevision, StartedAt, task, ThreatId);
        public RetreatRound WithThreat(string threat) => new RetreatRound(Number, FirstTurn, StartRevision, StartedAt, Task, threat);
        public RetreatRound Settle(RetreatSettlement settlement)
            => new RetreatRound(Number, FirstTurn, StartRevision, StartedAt, Task, ThreatId, settlement);
    }

    public sealed class RetreatRecord
    {
        public RetreatDefinition Definition { get; }
        public long DeclaredRevision { get; }
        public string DeclarationId { get; }
        public IReadOnlyList<RetreatRound> Rounds { get; }
        public RetreatRound Round => Rounds.LastOrDefault();
        public bool Active => Round != null && Round.Settlement == null;
        public RetreatSettlement SuccessfulExit => Round?.Settlement?.Outcome == RetreatOutcome.Successful ? Round.Settlement : null;
        public int Escape => Rounds.Where(x => x.Settlement?.IncludesExchange == true).Sum(x => RetreatRules.Escape(x.Task.Degree));
        public int Pursuit => Rounds.Where(x => x.Settlement?.IncludesExchange == true).Sum(x => RetreatRules.Pursuit(x.Task.Degree));

        public RetreatRecord(RetreatDefinition definition, long declaredRevision = 0, string declarationId = "",
            IEnumerable<RetreatRound> rounds = null)
        {
            Definition = definition ?? throw new ArgumentNullException(nameof(definition));
            var rows = (rounds ?? Array.Empty<RetreatRound>()).ToArray();
            if (rows.Length > 5 || rows.Any(x => x == null) || (declaredRevision == 0) != (rows.Length == 0)
                || rows.Length == 0 && declarationId != ""
                || rows.Length != 0 && (!Validation.ValidId(declarationId) || declaredRevision <= rows[0].StartRevision)
                || rows.Skip(1).Where((row, i) => rows[i].Settlement?.Outcome != RetreatOutcome.Continue
                    || rows[i].Number + 1 != row.Number || rows[i].FirstTurn + 3 != row.FirstTurn
                    || rows[i].Settlement.Revision != row.StartRevision || rows[i].Settlement.At != row.StartedAt).Any())
                throw new ArgumentException("Invalid retreat attempt history.");
            DeclaredRevision = declaredRevision;
            DeclarationId = declarationId;
            Rounds = Array.AsReadOnly(rows);
        }

        public RetreatRecord WithRound(RetreatRound round)
            => new RetreatRecord(Definition, DeclaredRevision, DeclarationId, Rounds.Take(Rounds.Count - 1).Append(round));
        public RetreatRecord Continue(RetreatRound round)
            => new RetreatRecord(Definition, DeclaredRevision, DeclarationId, Rounds.Append(round));
    }
}
