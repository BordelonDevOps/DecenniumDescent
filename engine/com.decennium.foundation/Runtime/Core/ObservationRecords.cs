using System;
using System.Linq;
using System.Numerics;

namespace Decennium.Foundation
{
    /// <summary>DirectSightLimit is the excluded right-hand boundary where direct sight ceased along a path.
    /// The target may have moved (leaving stale location evidence) or stayed in place while its observer moved.</summary>
    public enum ObservationEvidenceKind { None = 0, DirectSight = 1, Search = 2, AttackEvidence = 3, DirectSightLimit = 4 }
    public enum ObservationActionKind { Hide, Search }
    public enum ObservationDieSelection { None, Normal, Advantage, Disadvantage }
    public enum ObservationTaskDegree { None, CriticalFailure, Failure, Success, CriticalSuccess }
    public enum ObservationActionOutcome { NoEligibleObservers, HideAttempted, SearchNoFinding, SearchFound }

    /// <summary>Persisted authored map cell; all geometry channels remain independent.</summary>
    public sealed class ObservationMapCellRecord
    {
        public int X { get; }
        public int Y { get; }
        public bool BlocksSight { get; }
        public bool BlocksEffect { get; }
        public bool BlocksMovement { get; }
        public bool Solid { get; }
        public ObservationMapCellRecord(int x, int y, bool blocksSight, bool blocksEffect, bool blocksMovement, bool solid)
        {
            if (x < 0 || y < 0 || !blocksSight && !blocksEffect && !blocksMovement && !solid || solid && !blocksMovement)
                throw new ArgumentException("Invalid observation cell channels.");
            X = x; Y = y; BlocksSight = blocksSight; BlocksEffect = blocksEffect; BlocksMovement = blocksMovement; Solid = solid;
        }
        public bool SameAs(ObservationMapCellRecord x) => x != null && X == x.X && Y == x.Y
            && BlocksSight == x.BlocksSight && BlocksEffect == x.BlocksEffect && BlocksMovement == x.BlocksMovement && Solid == x.Solid;
    }

    /// <summary>Explicit observer ranges loaded from fingerprinted TEST_ONLY content.</summary>
    public sealed class ObservationProfileRecord
    {
        public string ActorId { get; }
        public long SightRangeFeet { get; }
        public long SearchRangeFeet { get; }
        public ObservationProfileRecord(string actorId, long sightRangeFeet, long searchRangeFeet)
        {
            if (!Validation.ValidId(actorId) || sightRangeFeet < 0 || searchRangeFeet < 0)
                throw new ArgumentException("Invalid observation profile.");
            ActorId = actorId; SightRangeFeet = sightRangeFeet; SearchRangeFeet = searchRangeFeet;
        }
        public bool SameAs(ObservationProfileRecord x) => x != null && ActorId == x.ActorId
            && SightRangeFeet == x.SightRangeFeet && SearchRangeFeet == x.SearchRangeFeet;
    }

    /// <summary>Auditable tactical Hide or candidate-space Search check. For an unsuccessful Search,
    /// TargetId is deliberately empty so the observer receives no hidden identity from the record.</summary>
    public sealed class ObservationActionRecord
    {
        public string Id { get; }
        public string ActorId { get; }
        public string TargetId { get; }
        public ObservationActionKind Kind { get; }
        public ObservationActionOutcome Outcome { get; }
        public RuleTime At { get; }
        public long Revision { get; }
        public RuleQuantity X { get; }
        public RuleQuantity Y { get; }
        public int First { get; }
        public int Second { get; }
        public int Natural { get; }
        public int Modifier { get; }
        public long Total { get; }
        public ObservationDieSelection Selection { get; }
        public uint RandomBefore { get; }
        public uint RandomAfter { get; }
        public long WordsConsumed { get; }

        public ObservationActionRecord(string id, string actorId, string targetId, ObservationActionKind kind,
            ObservationActionOutcome outcome, RuleTime at, long revision, RuleQuantity x, RuleQuantity y,
            int first, int second, int natural, int modifier, long total, ObservationDieSelection selection,
            uint randomBefore, uint randomAfter, long wordsConsumed)
        {
            if (!Validation.ValidId(id) || !Validation.ValidId(actorId) || targetId == null
                || targetId != "" && !Validation.ValidId(targetId) || !Enum.IsDefined(typeof(ObservationActionKind), kind)
                || !Enum.IsDefined(typeof(ObservationActionOutcome), outcome) || !Enum.IsDefined(typeof(ObservationDieSelection), selection)
                || revision < 1 || x.Numerator < 0 || y.Numerator < 0 || randomBefore == 0 || randomAfter == 0 || wordsConsumed < 0)
                throw new ArgumentException("Invalid observation action record.");
            bool noRoll = selection == ObservationDieSelection.None;
            if (noRoll)
            {
                if (first != 0 || second != 0 || natural != 0 || modifier != 0 || total != 0
                    || randomBefore != randomAfter || wordsConsumed != 0
                    || outcome != ObservationActionOutcome.NoEligibleObservers && outcome != ObservationActionOutcome.SearchNoFinding)
                    throw new ArgumentException("Invalid unrolled observation action.");
            }
            else
            {
                if (!Enum.IsDefined(typeof(ObservationDieSelection), selection) || first < 1 || first > 20
                    || (selection == ObservationDieSelection.Normal) != (second == 0)
                    || second < 0 || second > 20 || selection != ObservationDieSelection.Normal && second == 0
                    || natural != (selection == ObservationDieSelection.Advantage ? Math.Max(first, second)
                        : selection == ObservationDieSelection.Disadvantage ? Math.Min(first, second) : first)
                    || total != (long)natural + modifier
                    || wordsConsumed != (selection == ObservationDieSelection.Normal ? 1 : 2))
                    throw new ArgumentException("Invalid observation die audit.");
            }
            if (kind == ObservationActionKind.Hide && (targetId != ""
                    || outcome != ObservationActionOutcome.HideAttempted && outcome != ObservationActionOutcome.NoEligibleObservers)
                || kind == ObservationActionKind.Search && (outcome == ObservationActionOutcome.SearchFound) != (targetId != "")
                || kind == ObservationActionKind.Search && outcome != ObservationActionOutcome.SearchFound
                    && outcome != ObservationActionOutcome.SearchNoFinding)
                throw new ArgumentException("Observation action outcome does not match its kind.");
            if (kind == ObservationActionKind.Search && (x.Denominator != 1 || y.Denominator != 1))
                throw new ArgumentException("Search must name one authored grid cell.");
            Id = id; ActorId = actorId; TargetId = targetId; Kind = kind; Outcome = outcome; At = at; Revision = revision;
            X = x; Y = y; First = first; Second = second; Natural = natural; Modifier = modifier; Total = total;
            Selection = selection; RandomBefore = randomBefore; RandomAfter = randomAfter; WordsConsumed = wordsConsumed;
        }
        public bool SameAs(ObservationActionRecord x) => x != null && Id == x.Id && ActorId == x.ActorId && TargetId == x.TargetId
            && Kind == x.Kind && Outcome == x.Outcome && At == x.At && Revision == x.Revision && X == x.X && Y == x.Y
            && First == x.First && Second == x.Second && Natural == x.Natural && Modifier == x.Modifier && Total == x.Total
            && Selection == x.Selection && RandomBefore == x.RandomBefore && RandomAfter == x.RandomAfter && WordsConsumed == x.WordsConsumed;
    }

    /// <summary>One observer's result against a single shared Hide roll.</summary>
    public sealed class ObservationHideResultRecord
    {
        public string AttemptId { get; }
        public string ObserverId { get; }
        public RuleQuantity ObserverX { get; }
        public RuleQuantity ObserverY { get; }
        public int Dc { get; }
        public ObservationTaskDegree Degree { get; }
        public bool HiddenEstablished { get; }
        public ObservationHideResultRecord(string attemptId, string observerId, RuleQuantity observerX, RuleQuantity observerY,
            int dc, ObservationTaskDegree degree, bool hiddenEstablished)
        {
            if (!Validation.ValidId(attemptId) || !Validation.ValidId(observerId) || dc < 0
                || degree < ObservationTaskDegree.CriticalFailure || degree > ObservationTaskDegree.CriticalSuccess
                || hiddenEstablished != (degree >= ObservationTaskDegree.Success))
                throw new ArgumentException("Invalid observer-specific Hide result.");
            AttemptId = attemptId; ObserverId = observerId; ObserverX = observerX; ObserverY = observerY;
            Dc = dc; Degree = degree; HiddenEstablished = hiddenEstablished;
        }
        public bool SameAs(ObservationHideResultRecord x) => x != null && AttemptId == x.AttemptId && ObserverId == x.ObserverId
            && ObserverX == x.ObserverX && ObserverY == x.ObserverY && Dc == x.Dc && Degree == x.Degree
            && HiddenEstablished == x.HiddenEstablished;
    }

    /// <summary>Per-observer current and last-known location knowledge. This is never a shared
    /// world-visibility flag: each row belongs to exactly one observer/target pair.</summary>
    public sealed class ObserverKnowledgeRecord
    {
        public string ObserverId { get; }
        public string TargetId { get; }
        public bool HasLastKnownLocation { get; }
        public bool CurrentLocationKnown { get; }
        public RuleQuantity LastKnownX { get; }
        public RuleQuantity LastKnownY { get; }
        public ObservationEvidenceKind Evidence { get; }
        public RuleTime EvidenceAt { get; }
        public long EvidenceRevision { get; }
        public string HiddenAttemptId { get; }
        public string RevealedInvisibleEpisodeId { get; }
        public ObserverKnowledgeRecord(string observerId, string targetId, bool hasLastKnownLocation, bool currentLocationKnown,
            RuleQuantity lastKnownX, RuleQuantity lastKnownY, ObservationEvidenceKind evidence, RuleTime evidenceAt,
            long evidenceRevision, string hiddenAttemptId = "", string revealedInvisibleEpisodeId = "")
        {
            if (!Validation.ValidId(observerId) || !Validation.ValidId(targetId) || observerId == targetId
                || !Enum.IsDefined(typeof(ObservationEvidenceKind), evidence) || evidenceRevision < 0
                || hiddenAttemptId == null || hiddenAttemptId != "" && !Validation.ValidId(hiddenAttemptId)
                || revealedInvisibleEpisodeId == null || revealedInvisibleEpisodeId != "" && !Validation.ValidId(revealedInvisibleEpisodeId)
                || currentLocationKnown && (!hasLastKnownLocation || evidence == ObservationEvidenceKind.None || hiddenAttemptId != "")
                || !hasLastKnownLocation && (lastKnownX != default || lastKnownY != default || currentLocationKnown || evidence != ObservationEvidenceKind.None)
                || hasLastKnownLocation && evidence == ObservationEvidenceKind.None)
                throw new ArgumentException("Invalid observer knowledge record.");
            ObserverId = observerId; TargetId = targetId; HasLastKnownLocation = hasLastKnownLocation;
            CurrentLocationKnown = currentLocationKnown; LastKnownX = lastKnownX; LastKnownY = lastKnownY;
            Evidence = evidence; EvidenceAt = evidenceAt; EvidenceRevision = evidenceRevision;
            HiddenAttemptId = hiddenAttemptId; RevealedInvisibleEpisodeId = revealedInvisibleEpisodeId;
        }
        public bool SameAs(ObserverKnowledgeRecord x) => x != null && ObserverId == x.ObserverId && TargetId == x.TargetId
            && HasLastKnownLocation == x.HasLastKnownLocation && CurrentLocationKnown == x.CurrentLocationKnown
            && LastKnownX == x.LastKnownX && LastKnownY == x.LastKnownY && Evidence == x.Evidence
            && EvidenceAt == x.EvidenceAt && EvidenceRevision == x.EvidenceRevision
            && HiddenAttemptId == x.HiddenAttemptId && RevealedInvisibleEpisodeId == x.RevealedInvisibleEpisodeId;
    }

    public static class ObservationValidation
    {
        public const int MaxCells = 4096, MaxProfiles = Snapshot.MaxActors, MaxAttempts = 512, MaxHideResults = 4096,
            MaxKnowledgePairs = Snapshot.MaxActors * (Snapshot.MaxActors - 1);

        public static void Validate(Snapshot s)
        {
            if (s.ObservationCells == null || s.ObservationProfiles == null || s.ObservationActions == null
                || s.ObservationHideResults == null || s.ObserverKnowledge == null
                || s.ObservationCells.Length > MaxCells || s.ObservationProfiles.Length > MaxProfiles
                || s.ObservationActions.Length > MaxAttempts || s.ObservationHideResults.Length > MaxHideResults
                || s.ObserverKnowledge.Length > MaxKnowledgePairs || s.ObservationCells.Any(x => x == null)
                || s.ObservationProfiles.Any(x => x == null) || s.ObservationActions.Any(x => x == null)
                || s.ObservationHideResults.Any(x => x == null) || s.ObserverKnowledge.Any(x => x == null))
                throw new ArgumentException("Invalid observation collections.");
            if (s.SchemaVersion < Snapshot.ObservationSchema)
            {
                if (s.ObservationMapWidth != 0 || s.ObservationMapHeight != 0 || s.ObservationCells.Length != 0
                    || s.ObservationProfiles.Length != 0 || s.ObservationActions.Length != 0
                    || s.ObservationHideResults.Length != 0 || s.ObserverKnowledge.Length != 0)
                    throw new ArgumentException("Observation state requires schema51.");
                return;
            }
            if (s.ObservationMapWidth < 1 || s.ObservationMapWidth > 64 || s.ObservationMapHeight < 1 || s.ObservationMapHeight > 64
                || s.ObservationCells.Select(x => x.X + "," + x.Y).Distinct(StringComparer.Ordinal).Count() != s.ObservationCells.Length
                || s.ObservationCells.Any(x => x.X >= s.ObservationMapWidth || x.Y >= s.ObservationMapHeight)
                || !s.Actors.Select(x => x.Id).OrderBy(x => x, StringComparer.Ordinal)
                    .SequenceEqual(s.ObservationProfiles.Select(x => x.ActorId).OrderBy(x => x, StringComparer.Ordinal))
                || s.ObservationCells.Any(x => (x.BlocksSight || x.BlocksEffect || x.BlocksMovement)
                    && (s.Actors.Any(a => a.X == x.X && a.Y == x.Y)
                    || s.Objects.Any(o => o.X == x.X && o.Y == x.Y)))
                || s.Actors.Any(x => x.X < 0 || x.X >= s.ObservationMapWidth || x.Y < 0 || x.Y >= s.ObservationMapHeight)
                || s.Objects.Any(x => x.X < 0 || x.X >= s.ObservationMapWidth || x.Y < 0 || x.Y >= s.ObservationMapHeight)
                || s.WorldTraversals.Any(x => x.FromX < 0 || x.FromX >= s.ObservationMapWidth || x.ToX < 0 || x.ToX >= s.ObservationMapWidth
                    || x.FromY < 0 || x.FromY >= s.ObservationMapHeight || x.ToY < 0 || x.ToY >= s.ObservationMapHeight
                    || s.ObservationCells.Any(c => (c.BlocksSight || c.BlocksEffect || c.BlocksMovement)
                        && (c.X == x.FromX && c.Y == x.FromY || c.X == x.ToX && c.Y == x.ToY))))
                throw new ArgumentException("Invalid authored observation map or unsupported anchor placement.");
            if (s.ObservationActions.Select(x => x.Id).Distinct(StringComparer.Ordinal).Count() != s.ObservationActions.Length
                || s.ObserverKnowledge.Select(x => x.ObserverId + "|" + x.TargetId).Distinct(StringComparer.Ordinal).Count() != s.ObserverKnowledge.Length
                || s.ObservationHideResults.Select(x => x.AttemptId + "|" + x.ObserverId).Distinct(StringComparer.Ordinal).Count() != s.ObservationHideResults.Length)
                throw new ArgumentException("Duplicate observation identity.");
            foreach (var action in s.ObservationActions)
            {
                if (!s.Actors.Any(x => x.Id == action.ActorId) || action.TargetId != "" && !s.Actors.Any(x => x.Id == action.TargetId)
                    || action.TargetId == action.ActorId || action.At > s.RuleClock || action.Revision > s.Revision
                    || !WithinMap(action.X, s.ObservationMapWidth) || !WithinMap(action.Y, s.ObservationMapHeight))
                    throw new ArgumentException("Observation action references invalid state.");
            }
            foreach (var result in s.ObservationHideResults)
            {
                var attempt = s.ObservationActions.SingleOrDefault(x => x.Id == result.AttemptId);
                if (attempt == null || attempt.Kind != ObservationActionKind.Hide || attempt.Outcome != ObservationActionOutcome.HideAttempted
                    || attempt.ActorId == result.ObserverId || !s.Actors.Any(x => x.Id == result.ObserverId)
                    || !WithinMap(result.ObserverX, s.ObservationMapWidth) || !WithinMap(result.ObserverY, s.ObservationMapHeight))
                    throw new ArgumentException("Hide result references an invalid observer or attempt.");
            }
            foreach (var knowledge in s.ObserverKnowledge)
            {
                if (!s.Actors.Any(x => x.Id == knowledge.ObserverId) || !s.Actors.Any(x => x.Id == knowledge.TargetId)
                    || knowledge.EvidenceAt > s.RuleClock || knowledge.EvidenceRevision > s.Revision
                    || knowledge.HasLastKnownLocation && (!WithinMap(knowledge.LastKnownX, s.ObservationMapWidth)
                        || !WithinMap(knowledge.LastKnownY, s.ObservationMapHeight)))
                    throw new ArgumentException("Observer knowledge references invalid state.");
                if (knowledge.HiddenAttemptId != "")
                {
                    var attempt = s.ObservationActions.SingleOrDefault(x => x.Id == knowledge.HiddenAttemptId);
                    if (attempt == null || attempt.Kind != ObservationActionKind.Hide || attempt.ActorId != knowledge.TargetId
                        || !s.ObservationHideResults.Any(x => x.AttemptId == attempt.Id && x.ObserverId == knowledge.ObserverId && x.HiddenEstablished))
                        throw new ArgumentException("Hidden state has no successful observer-specific Hide result.");
                }
                if (knowledge.RevealedInvisibleEpisodeId != "")
                {
                    var journal = s.Conditions.SingleOrDefault(x => x.Target == knowledge.TargetId);
                    if (journal == null || !journal.Operations.Any(x => x.Application != null
                        && x.Application.Id == knowledge.RevealedInvisibleEpisodeId && x.Application.Kind == "Invisible"))
                        throw new ArgumentException("Invisible revelation latch has no matching condition episode source.");
                }
                if (knowledge.CurrentLocationKnown)
                {
                    var actual = Position(s, knowledge.TargetId);
                    if (actual.X != knowledge.LastKnownX || actual.Y != knowledge.LastKnownY)
                        throw new ArgumentException("Current location knowledge disagrees with actual position.");
                }
            }
        }

        private static bool WithinMap(RuleQuantity coordinate, int extent)
            => coordinate.Numerator >= 0 && (BigInteger)coordinate.Numerator < (BigInteger)extent * coordinate.Denominator;

        private static (RuleQuantity X, RuleQuantity Y) Position(Snapshot s, string actorId)
        {
            var actor = s.Actors.Single(x => x.Id == actorId);
            var edge = s.WorldTraversals?.SingleOrDefault(x => x.ActorId == actorId);
            if (edge == null) return (new RuleQuantity(actor.X), new RuleQuantity(actor.Y));
            RuleQuantity Fraction(int origin, int direction)
            {
                BigInteger n = (BigInteger)origin * 5 * edge.DistanceFeet.Denominator + (BigInteger)direction * edge.DistanceFeet.Numerator;
                return RuleQuantity.FromFraction(n, (BigInteger)5 * edge.DistanceFeet.Denominator);
            }
            int dx = Math.Sign(edge.ToX - edge.FromX), dy = Math.Sign(edge.ToY - edge.FromY);
            return (Fraction(edge.FromX, dx), Fraction(edge.FromY, dy));
        }
    }
}
