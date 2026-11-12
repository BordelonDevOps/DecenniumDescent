using System;
using System.Collections.Generic;
using System.Globalization;
using System.Linq;

namespace Decennium.Foundation
{
    public readonly struct ExplorationSearchCell : IEquatable<ExplorationSearchCell>
    {
        public int X { get; }
        public int Y { get; }

        public ExplorationSearchCell(int x, int y)
        {
            if (x < 0 || y < 0 || x >= 64 || y >= 64) throw new ArgumentOutOfRangeException(nameof(x));
            X = x;
            Y = y;
        }

        public bool Equals(ExplorationSearchCell other) => X == other.X && Y == other.Y;
        public override bool Equals(object obj) => obj is ExplorationSearchCell cell && Equals(cell);
        public override int GetHashCode() => (X << 6) | Y;
        public override string ToString() => X.ToString(CultureInfo.InvariantCulture) + "," + Y.ToString(CultureInfo.InvariantCulture);
    }

    public sealed class ExplorationSearchDefinition
    {
        public const string Source = "46a4d52728ee6956f0bebcb5d2103ffd5bc67ba4";
        public const string Director = "TEST_ONLY.director.ordinary-visual-search.v1";
        public const string VisibleFringe = "TEST_ONLY.faint-visible-fringe-at-recess.v1";
        public const string FingerprintPrefix = "TEST_ONLY.exploration-search-v1-";

        public string SourceRevision { get; }
        public string DirectorId { get; }
        public string CueId { get; }
        public string SearcherId { get; }
        public string ConcealedActorId { get; }
        public ExplorationSearchCell Anchor { get; }
        public ExplorationSearchCell CueCandidate { get; }
        public ExplorationSearchCell Sign { get; }
        public ExplorationSearchCell Occlusion { get; }

        public ExplorationSearchDefinition(string source, string director, string cue, string searcher, string concealedActor,
            ExplorationSearchCell anchor, ExplorationSearchCell candidate, ExplorationSearchCell sign, ExplorationSearchCell occlusion)
        {
            bool independent = director == Director && cue == VisibleFringe;
            bool connected = director == ConnectedExplorationObservation.SearchDirector && cue == ConnectedExplorationObservation.VisibleFringe;
            if (source != Source || !independent && !connected || !Validation.ValidId(searcher)
                || !Validation.ValidId(concealedActor) || searcher == concealedActor
                || new[] { anchor, candidate, sign, occlusion }.Distinct().Count() != 4)
                throw new ArgumentException("Invalid authored visual Search authority.");
            SourceRevision = source;
            DirectorId = director;
            CueId = cue;
            SearcherId = searcher;
            ConcealedActorId = concealedActor;
            Anchor = anchor;
            CueCandidate = candidate;
            Sign = sign;
            Occlusion = occlusion;
        }

        public bool SameAs(ExplorationSearchDefinition other) => other != null && SourceRevision == other.SourceRevision
            && DirectorId == other.DirectorId && CueId == other.CueId && SearcherId == other.SearcherId
            && ConcealedActorId == other.ConcealedActorId && Anchor.Equals(other.Anchor)
            && CueCandidate.Equals(other.CueCandidate) && Sign.Equals(other.Sign) && Occlusion.Equals(other.Occlusion);
    }

    public enum ExplorationSearchStatus { Pending, Completed, Cancelled, Interrupted }
    public enum ExplorationSearchInterruption { None, VisualCapabilityLost, SearcherDisplaced, TacticalControlEntered }

    public sealed class ExplorationSearchEnd
    {
        public ExplorationSearchStatus Status { get; }
        public ExplorationSearchInterruption Interruption { get; }
        public long Revision { get; }
        public string CommandId { get; }
        public RuleTime At { get; }
        public string ObservationId { get; }
        public string CueId { get; }
        public string HideId { get; }

        public ExplorationSearchEnd(ExplorationSearchStatus status, ExplorationSearchInterruption interruption,
            long revision, string commandId, RuleTime at, string observationId = "", string cueId = "", string hideId = "")
        {
            bool completed = status == ExplorationSearchStatus.Completed;
            bool interrupted = status == ExplorationSearchStatus.Interrupted;
            if ((!completed && !interrupted && status != ExplorationSearchStatus.Cancelled)
                || !Enum.IsDefined(typeof(ExplorationSearchInterruption), interruption)
                || interrupted != (interruption != ExplorationSearchInterruption.None)
                || revision < 1 || !Validation.ValidId(commandId)
                || completed && !Validation.ValidId(observationId) || !completed && observationId != ""
                || (cueId == "") != (hideId == "") || cueId != "" && (!completed || !Validation.ValidId(cueId) || !Validation.ValidId(hideId)))
                throw new ArgumentException("Invalid ordinary Search completion or interruption.");
            Status = status;
            Interruption = interruption;
            Revision = revision;
            CommandId = commandId;
            At = at;
            ObservationId = observationId;
            CueId = cueId;
            HideId = hideId;
        }
    }

    public sealed class ExplorationSearchAttempt
    {
        public string Id => "exploration.search." + Revision.ToString(CultureInfo.InvariantCulture);
        public long Revision { get; }
        public string CommandId { get; }
        public long IntervalIndex { get; }
        public RuleTime StartedAt { get; }
        public RuleTime DueAt { get; }
        public ExplorationSearchCell Candidate { get; }
        public ExplorationSearchEnd End { get; }
        public ExplorationSearchStatus Status => End?.Status ?? ExplorationSearchStatus.Pending;

        public ExplorationSearchAttempt(long revision, string commandId, long intervalIndex, RuleTime startedAt,
            RuleTime dueAt, ExplorationSearchCell candidate, ExplorationSearchEnd end = null)
        {
            if (revision < 1 || !Validation.ValidId(commandId) || intervalIndex < 0 || dueAt <= startedAt
                || end != null && (end.Revision <= revision || end.At < startedAt || end.At > dueAt
                    || end.Status == ExplorationSearchStatus.Completed && end.At != dueAt))
                throw new ArgumentException("Invalid ordinary Search timeline.");
            Revision = revision;
            CommandId = commandId;
            IntervalIndex = intervalIndex;
            StartedAt = startedAt;
            DueAt = dueAt;
            Candidate = candidate;
            End = end;
        }

        public ExplorationSearchAttempt Finish(ExplorationSearchEnd end)
            => new ExplorationSearchAttempt(Revision, CommandId, IntervalIndex, StartedAt, DueAt, Candidate, end);
    }

    public sealed class ExplorationSearchRecord
    {
        public const int MaxAttempts = 64;
        public ExplorationSearchDefinition Definition { get; }
        public IReadOnlyList<ExplorationSearchAttempt> Attempts { get; }
        public ExplorationSearchAttempt Pending => Attempts.LastOrDefault(x => x.End == null);

        public ExplorationSearchRecord(ExplorationSearchDefinition definition, IEnumerable<ExplorationSearchAttempt> attempts = null)
        {
            Definition = definition ?? throw new ArgumentNullException(nameof(definition));
            var rows = (attempts ?? Array.Empty<ExplorationSearchAttempt>()).Take(MaxAttempts + 1).ToArray();
            if (rows.Length > MaxAttempts || rows.Any(x => x == null)
                || rows.Skip(1).Where((x, i) => rows[i].End == null || x.Revision <= rows[i].End.Revision
                    || x.IntervalIndex <= rows[i].IntervalIndex || x.StartedAt < rows[i].DueAt).Any())
                throw new ArgumentException("Invalid ordinary Search history.");
            Attempts = Array.AsReadOnly(rows);
        }

        public ExplorationSearchRecord Start(ExplorationSearchAttempt attempt)
            => new ExplorationSearchRecord(Definition, Attempts.Append(attempt));

        public ExplorationSearchRecord Finish(ExplorationSearchEnd end)
            => new ExplorationSearchRecord(Definition, Attempts.Take(Attempts.Count - 1).Append(Pending.Finish(end)));

        public static string Marker(string calendarId, long intervalIndex)
            => calendarId + ".activity." + intervalIndex.ToString(CultureInfo.InvariantCulture);
    }
}
