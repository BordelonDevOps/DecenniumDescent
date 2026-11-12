using System;
using System.Collections.Generic;
using System.Globalization;
using System.Linq;

namespace Decennium.Foundation
{
    public sealed class ExplorationHideDefinition
    {
        public const string Director = "TEST_ONLY.director.ordinary-hide.v1";
        public const string Witness = "TEST_ONLY.search-witness";
        public const string FingerprintPrefix = "TEST_ONLY.exploration-hide-v1-";

        public string SourceRevision { get; }
        public string DirectorId { get; }
        public string HiderId { get; }
        public string WitnessId { get; }
        public ExplorationSearchCell Recess { get; }
        public ExplorationSearchCell Alternate { get; }

        public ExplorationHideDefinition(string source, string director, string hider, string witness,
            ExplorationSearchCell recess, ExplorationSearchCell alternate)
        {
            bool independent = director == Director && witness == Witness;
            bool connected = director == ConnectedExplorationObservation.HideDirector
                && hider == ConnectedExplorationObservation.Hero && witness == ConnectedExplorationObservation.Buyer;
            if (source != ExplorationSearchDefinition.Source || !independent && !connected || !Validation.ValidId(hider)
                || hider == witness || !recess.Equals(new ExplorationSearchCell(1, 0))
                || !alternate.Equals(new ExplorationSearchCell(2, 0)))
                throw new ArgumentException("Invalid authored ordinary Hide authority.");
            SourceRevision = source;
            DirectorId = director;
            HiderId = hider;
            WitnessId = witness;
            Recess = recess;
            Alternate = alternate;
        }

        public bool Allows(ExplorationSearchCell cell) => cell.Equals(Recess) || cell.Equals(Alternate);
        public bool SameAs(ExplorationHideDefinition other) => other != null && SourceRevision == other.SourceRevision
            && DirectorId == other.DirectorId && HiderId == other.HiderId && WitnessId == other.WitnessId
            && Recess.Equals(other.Recess) && Alternate.Equals(other.Alternate);
    }

    public enum ExplorationHideStatus { Pending, Completed, Cancelled, Interrupted }
    public enum ExplorationHideInterruption { None, ActionCapabilityLost, HiderDisplaced, TacticalControlEntered }
    public enum ExplorationHideNoRoll { None, NoEligibleObservers, UnchangedFailure }
    [Flags]
    public enum ExplorationHideObservers { None = 0, Searcher = 1, Witness = 2 }

    public sealed class ExplorationHideRelocation
    {
        public ExplorationSearchCell From { get; }
        public ExplorationSearchCell To { get; }
        public long StartedRevision { get; }
        public long ArrivedRevision { get; }
        public string ArrivalCommandId { get; }
        public RuleTime At { get; }

        public ExplorationHideRelocation(ExplorationSearchCell from, ExplorationSearchCell to, long startedRevision,
            long arrivedRevision, string arrivalCommandId, RuleTime at)
        {
            if (from.Equals(to) || startedRevision < 1 || arrivedRevision <= startedRevision
                || !Validation.ValidId(arrivalCommandId))
                throw new ArgumentException("Invalid ordinary Hide relocation.");
            From = from;
            To = to;
            StartedRevision = startedRevision;
            ArrivedRevision = arrivedRevision;
            ArrivalCommandId = arrivalCommandId;
            At = at;
        }
    }

    public sealed class ExplorationHideEnd
    {
        public ExplorationHideStatus Status { get; }
        public ExplorationHideInterruption Interruption { get; }
        public long Revision { get; }
        public string CommandId { get; }
        public RuleTime At { get; }
        public string ObservationId { get; }
        public ExplorationHideNoRoll NoRoll { get; }
        public string PriorFailureId { get; }
        public string PriorFailureObserverId { get; }
        public ExplorationHideObservers EligibleObservers { get; }

        public ExplorationHideEnd(ExplorationHideStatus status, ExplorationHideInterruption interruption,
            long revision, string commandId, RuleTime at, string observationId = "",
            ExplorationHideNoRoll noRoll = ExplorationHideNoRoll.None, string priorFailureId = "",
            string priorFailureObserverId = "", ExplorationHideObservers eligibleObservers = ExplorationHideObservers.None)
        {
            bool completed = status == ExplorationHideStatus.Completed;
            bool interrupted = status == ExplorationHideStatus.Interrupted;
            bool suppressed = noRoll == ExplorationHideNoRoll.UnchangedFailure;
            if ((!completed && !interrupted && status != ExplorationHideStatus.Cancelled)
                || !Enum.IsDefined(typeof(ExplorationHideInterruption), interruption)
                || !Enum.IsDefined(typeof(ExplorationHideNoRoll), noRoll)
                || interrupted != (interruption != ExplorationHideInterruption.None)
                || revision < 1 || !Validation.ValidId(commandId)
                || (completed && noRoll == ExplorationHideNoRoll.None ? !Validation.ValidId(observationId) : observationId != "")
                || !completed && noRoll != ExplorationHideNoRoll.None
                || (eligibleObservers & ~(ExplorationHideObservers.Searcher | ExplorationHideObservers.Witness)) != 0
                || (eligibleObservers != ExplorationHideObservers.None) != (completed && noRoll != ExplorationHideNoRoll.NoEligibleObservers)
                || (suppressed ? !Validation.ValidId(priorFailureId) || !Validation.ValidId(priorFailureObserverId)
                    : priorFailureId != "" || priorFailureObserverId != ""))
                throw new ArgumentException("Invalid ordinary Hide completion or interruption.");
            Status = status;
            Interruption = interruption;
            Revision = revision;
            CommandId = commandId;
            At = at;
            ObservationId = observationId;
            NoRoll = noRoll;
            PriorFailureId = priorFailureId;
            PriorFailureObserverId = priorFailureObserverId;
            EligibleObservers = eligibleObservers;
        }
    }

    public sealed class ExplorationHideAttempt
    {
        public string Id => "exploration.hide." + Revision.ToString(CultureInfo.InvariantCulture);
        public long Revision { get; }
        public string CommandId { get; }
        public string CalendarId { get; }
        public long PaidStart { get; }
        public RuleTime StartedAt { get; }
        public RuleTime DueAt { get; }
        public ExplorationSearchCell Anchor { get; }
        public ExplorationHideRelocation Relocation { get; }
        public ExplorationHideEnd End { get; }
        public ExplorationHideStatus Status => End?.Status ?? ExplorationHideStatus.Pending;

        public ExplorationHideAttempt(long revision, string commandId, string calendarId, long paidStart, RuleTime startedAt,
            RuleTime dueAt, ExplorationSearchCell anchor, ExplorationHideRelocation relocation = null, ExplorationHideEnd end = null)
        {
            if (revision < 1 || !Validation.ValidId(commandId) || !Validation.ValidId(calendarId) || paidStart < 0
                || dueAt <= startedAt || relocation != null && (relocation.ArrivedRevision >= revision
                    || relocation.At > startedAt || !relocation.To.Equals(anchor))
                || end != null && (end.Revision <= revision || end.At < startedAt || end.At > dueAt
                    || end.Status == ExplorationHideStatus.Completed && end.At != dueAt))
                throw new ArgumentException("Invalid ordinary Hide timeline.");
            Revision = revision;
            CommandId = commandId;
            CalendarId = calendarId;
            PaidStart = paidStart;
            StartedAt = startedAt;
            DueAt = dueAt;
            Anchor = anchor;
            Relocation = relocation;
            End = end;
        }

        public ExplorationHideAttempt Finish(ExplorationHideEnd end)
            => new ExplorationHideAttempt(Revision, CommandId, CalendarId, PaidStart, StartedAt, DueAt, Anchor, Relocation, end);
    }

    public sealed class ExplorationHideRecord
    {
        public const int MaxAttempts = 64;
        public ExplorationHideDefinition Definition { get; }
        public ExplorationHideRelocation LatestRelocation { get; }
        public IReadOnlyList<ExplorationHideAttempt> Attempts { get; }
        public ExplorationHideAttempt Pending => Attempts.LastOrDefault(x => x.End == null);

        public ExplorationHideRecord(ExplorationHideDefinition definition, ExplorationHideRelocation latestRelocation = null,
            IEnumerable<ExplorationHideAttempt> attempts = null)
        {
            Definition = definition ?? throw new ArgumentNullException(nameof(definition));
            var rows = (attempts ?? Array.Empty<ExplorationHideAttempt>()).Take(MaxAttempts + 1).ToArray();
            if (rows.Length > MaxAttempts || rows.Any(x => x == null)
                || rows.Skip(1).Where((x, i) => rows[i].End == null || x.Revision <= rows[i].End.Revision
                    || x.PaidStart <= rows[i].PaidStart || x.StartedAt < rows[i].DueAt).Any())
                throw new ArgumentException("Invalid ordinary Hide history.");
            LatestRelocation = latestRelocation;
            Attempts = Array.AsReadOnly(rows);
        }

        public ExplorationHideRecord WithRelocation(ExplorationHideRelocation relocation)
            => new ExplorationHideRecord(Definition, relocation, Attempts);

        public ExplorationHideRecord Start(ExplorationHideAttempt attempt)
            => new ExplorationHideRecord(Definition, LatestRelocation, Attempts.Append(attempt));

        public ExplorationHideRecord Finish(ExplorationHideEnd end)
            => new ExplorationHideRecord(Definition, LatestRelocation, Attempts.Take(Attempts.Count - 1).Append(Pending.Finish(end)));
    }

    public sealed class ExplorationHideView
    {
        public string AttemptId { get; }
        public ExplorationHideStatus Status { get; }
        public RuleTime StartedAt { get; }
        public RuleTime DueAt { get; }
        public RuleTime? EndedAt { get; }

        internal ExplorationHideView(ExplorationHideAttempt attempt)
        {
            AttemptId = attempt.Id;
            Status = attempt.Status;
            StartedAt = attempt.StartedAt;
            DueAt = attempt.DueAt;
            EndedAt = attempt.End?.At;
        }
    }
}
