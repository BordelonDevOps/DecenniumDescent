#if DECENNIUM_TEST_ONLY && (UNITY_EDITOR || DEVELOPMENT_BUILD || HEADLESS_TESTS)
using System;
using System.Collections.Generic;
using System.Linq;

namespace Decennium.Foundation.Laboratory
{
    /// <summary>Versioned TEST_ONLY observation procedures. Schema51 saves keep their original
    /// sampled profile available for exact historical receipt replay.</summary>
    public enum ObservationAlgorithmVersion
    {
        LegacySampledV1 = 1,
        ExactPathIntervalsV2 = 2
    }

    public sealed class ObservationMovementSegment
    {
        internal WorldTraversalRecord Edge { get; }
        internal RuleQuantity FromDistance { get; }
        internal RuleQuantity ToDistance { get; }
        public ObservationMovementSegment(WorldTraversalRecord edge, RuleQuantity fromDistance, RuleQuantity toDistance)
        { Edge = edge; FromDistance = fromDistance; ToDistance = toDistance; }
    }

    /// <summary>A per-observer view record. This projection deliberately has no hidden actor entries.</summary>
    public sealed class ObservationKnownLocation
    {
        public string ActorId { get; }
        public RuleQuantity X { get; }
        public RuleQuantity Y { get; }
        public ObservationEvidenceKind Evidence { get; }
        public RuleTime EvidenceAt { get; }
        internal ObservationKnownLocation(string actorId, RuleQuantity x, RuleQuantity y,
            ObservationEvidenceKind evidence, RuleTime evidenceAt)
        { ActorId = actorId; X = x; Y = y; Evidence = evidence; EvidenceAt = evidenceAt; }
    }

    /// <summary>
    /// Schema51 TEST_ONLY observation state. Geometry is fixture-authored; condition journals remain
    /// authoritative for sensory conditions and Invisible application episodes. This class stores only
    /// observer-specific knowledge and projects no information to an observer who has not acquired it.
    /// </summary>
    public static class ObservationRules
    {
        /// <summary>True only when this snapshot actually selected and persisted observation
        /// content. Append-only schemas may include unrelated systems without an observation map.</summary>
        public static bool Enabled(Snapshot s)
            => s != null && s.SchemaVersion >= Snapshot.ObservationSchema
                && s.ObservationMapWidth > 0 && s.ObservationMapHeight > 0
                && s.ObservationProfiles != null && s.ObservationProfiles.Length > 0;

        public static void Initialize(Snapshot s, ObservationFixture fixture)
        {
            if (s == null || fixture == null || s.SchemaVersion < Snapshot.ObservationSchema)
                throw new ArgumentException("Schema51 observation content is required.");
            s.ObserverKnowledge = Array.Empty<ObserverKnowledgeRecord>();
            foreach (var observer in s.Actors.OrderBy(x => x.Id, StringComparer.Ordinal))
                foreach (var target in s.Actors.OrderBy(x => x.Id, StringComparer.Ordinal))
                    if (observer.Id != target.Id && DirectSightAt(s, observer.Id, target.Id,
                        ObservationGeometry.Position(s, observer.Id), ObservationGeometry.Position(s, target.Id)))
                        Set(s, NewKnowledge(s, observer.Id, target.Id, true, ObservationGeometry.Position(s, target.Id),
                            ObservationEvidenceKind.DirectSight, s.RuleClock, 0));
        }

        /// <summary>Refreshes endpoint visibility and invalidates stale locations after unseen movement.</summary>
        public static void Refresh(Snapshot s, RuleTime at, long revision)
        {
            if (!Enabled(s)) return;
            foreach (var observer in s.Actors.OrderBy(x => x.Id, StringComparer.Ordinal))
                foreach (var target in s.Actors.OrderBy(x => x.Id, StringComparer.Ordinal))
                {
                    if (observer.Id == target.Id) continue;
                    var prior = Knowledge(s, observer.Id, target.Id);
                    var targetPosition = ObservationGeometry.Position(s, target.Id);
                    string episode = CurrentInvisibleEpisodeId(s, target.Id);
                    if (DirectSightAt(s, observer.Id, target.Id, ObservationGeometry.Position(s, observer.Id), targetPosition))
                    {
                        if (prior == null || !prior.CurrentLocationKnown || prior.LastKnownX != targetPosition.X
                            || prior.LastKnownY != targetPosition.Y || prior.Evidence != ObservationEvidenceKind.DirectSight
                            || prior.HiddenAttemptId != "" || prior.RevealedInvisibleEpisodeId != episode)
                            Set(s, NewKnowledge(s, observer.Id, target.Id, true, targetPosition,
                                ObservationEvidenceKind.DirectSight, at, revision, revealedEpisode: episode));
                    }
                    else if (prior != null)
                    {
                        bool stillAtLastKnown = prior.CurrentLocationKnown && prior.LastKnownX == targetPosition.X
                            && prior.LastKnownY == targetPosition.Y;
                        bool current = prior.CurrentLocationKnown && stillAtLastKnown;
                        string revealed = episode == "" ? "" : prior.RevealedInvisibleEpisodeId;
                        if (current && episode != "") revealed = episode;
                        if (current != prior.CurrentLocationKnown || revealed != prior.RevealedInvisibleEpisodeId)
                            Set(s, Copy(prior, currentLocationKnown: current, revealedEpisode: revealed));
                    }
                }
        }

        /// <summary>Returns only the current/last-known entries available to one observer.</summary>
        public static IReadOnlyList<ObservationKnownLocation> KnownLocations(Snapshot s, string observerId)
        {
            if (s == null || !Validation.ValidId(observerId) || !s.Actors.Any(x => x.Id == observerId))
                throw new ArgumentException("A current observer is required.");
            var known = new List<ObservationKnownLocation>();
            foreach (var target in s.Actors.Where(x => x.Id != observerId).OrderBy(x => x.Id, StringComparer.Ordinal))
            {
                var point = ObservationGeometry.Position(s, target.Id);
                var row = Knowledge(s, observerId, target.Id);
                if (CanSee(s, observerId, target.Id))
                    known.Add(new ObservationKnownLocation(target.Id, point.X, point.Y,
                        ObservationEvidenceKind.DirectSight, row?.EvidenceAt ?? s.RuleClock));
                else if (row != null && row.CurrentLocationKnown && row.LastKnownX == point.X && row.LastKnownY == point.Y
                    && !HiddenTo(s, observerId, target.Id))
                    known.Add(new ObservationKnownLocation(target.Id, row.LastKnownX, row.LastKnownY, row.Evidence, row.EvidenceAt));
            }
            return Array.AsReadOnly(known.ToArray());
        }

        public static bool CanSee(Snapshot s, string observerId, string targetId)
        {
            if (!Enabled(s) || observerId == targetId) return false;
            if (!DirectSightAt(s, observerId, targetId, ObservationGeometry.Position(s, observerId), ObservationGeometry.Position(s, targetId)))
                return false;
            return !HiddenTo(s, observerId, targetId);
        }

        /// <summary>Known location is separate from sight, but successful Hide suppresses stale knowledge.</summary>
        public static bool LocationKnown(Snapshot s, string observerId, string targetId)
        {
            if (CanSee(s, observerId, targetId)) return true;
            var row = Knowledge(s, observerId, targetId);
            if (row == null || !row.CurrentLocationKnown || HiddenTo(s, observerId, targetId)) return false;
            var actual = ObservationGeometry.Position(s, targetId);
            return row.LastKnownX == actual.X && row.LastKnownY == actual.Y;
        }

        public static bool HiddenTo(Snapshot s, string observerId, string targetId)
        {
            if (!Enabled(s) || observerId == targetId) return false;
            var row = Knowledge(s, observerId, targetId);
            if (row == null || row.HiddenAttemptId == "") return false;
            return !DirectSightAt(s, observerId, targetId, ObservationGeometry.Position(s, observerId), ObservationGeometry.Position(s, targetId));
        }

        /// <summary>True only for the Invisible episode explicitly disclosed to this observer.</summary>
        public static bool InvisibleRevealed(Snapshot s, string observerId, string targetId)
        {
            string episode = CurrentInvisibleEpisodeId(s, targetId);
            if (episode == "") return false;
            return Knowledge(s, observerId, targetId)?.RevealedInvisibleEpisodeId == episode;
        }

        internal static string CurrentInvisibleEpisodeId(Snapshot s, string targetId)
        {
            if (s.SchemaVersion < Snapshot.ConditionSchema || !s.Conditions.Any(x => x.Target == targetId)) return "";
            var ledger = TestOnlyClubAttackPolicy.ConditionsFor(s, targetId);
            var currentIds = new HashSet<string>(ledger.View().Sources(ConditionKind.Invisible), StringComparer.Ordinal);
            if (currentIds.Count == 0) return "";
            var all = ledger.Applications.Where(x => x.Application.Kind == ConditionKind.Invisible).ToArray();
            var connected = new HashSet<string>(currentIds, StringComparer.Ordinal);
            var starts = all.Where(x => currentIds.Contains(x.Id)).Select(x => x.Application.Starts).ToArray();
            var ends = all.Where(x => currentIds.Contains(x.Id)).Select(EndOf).ToArray();
            var earliest = starts.Min(); var latest = ends.Max();
            bool changed;
            do
            {
                changed = false;
                foreach (var instance in all)
                {
                    if (connected.Contains(instance.Id)) continue;
                    var start = instance.Application.Starts; var end = EndOf(instance);
                    if (start.CompareTo(latest) <= 0 && end.CompareTo(earliest) >= 0)
                    {
                        connected.Add(instance.Id); starts = starts.Concat(new[] { start }).ToArray();
                        ends = ends.Concat(new[] { end }).ToArray(); earliest = starts.Min(); latest = ends.Max(); changed = true;
                    }
                }
            } while (changed);
            return all.Where(x => connected.Contains(x.Id)).OrderBy(x => x.Application.Starts)
                .ThenBy(x => x.Id, StringComparer.Ordinal).First().Id;
        }

        private static EffectClockMarker EndOf(ConditionInstance instance)
        {
            var ends = new[] { instance.EndedAt, instance.Application.Expires }.Where(x => x.HasValue)
                .Select(x => x.Value).ToArray();
            return ends.Length == 0 ? new EffectClockMarker(new RuleTime(long.MaxValue), int.MaxValue) : ends.Min();
        }

        internal static bool DirectSightAt(Snapshot s, string observerId, string targetId,
            ObservationPoint observerPosition, ObservationPoint targetPosition)
        {
            if (s.SchemaVersion < Snapshot.ConditionSchema || !s.Actors.Any(x => x.Id == observerId)
                || !s.Actors.Any(x => x.Id == targetId) || !ActorLifeRules.CanAct(s, observerId)) return false;
            var observer = TestOnlyClubAttackPolicy.ConditionsFor(s, observerId).View();
            var target = TestOnlyClubAttackPolicy.ConditionsFor(s, targetId).View();
            return !observer.Unaware && !observer.BlocksSight && !target.Has(ConditionKind.Invisible)
                && ObservationGeometry.GeometricSight(s, observerId, observerPosition, targetPosition);
        }

        /// <summary>Checks sight with only the target's Invisible component lifted. Used to avoid
        /// counting the same known Invisible episode as both condition disadvantage and generic unseen.</summary>
        internal static bool InvisibleIsOnlySightBlocker(Snapshot s, string observerId, string targetId)
        {
            if (!TestOnlyClubAttackPolicy.ConditionsFor(s, targetId).View().Has(ConditionKind.Invisible)
                || !ActorLifeRules.CanAct(s, observerId)) return false;
            var observer = TestOnlyClubAttackPolicy.ConditionsFor(s, observerId).View();
            return !observer.Unaware && !observer.BlocksSight
                && ObservationGeometry.GeometricSight(s, observerId, ObservationGeometry.Position(s, observerId),
                    ObservationGeometry.Position(s, targetId));
        }

        internal static void DiscloseLocation(Snapshot s, string observerId, string targetId,
            ObservationEvidenceKind evidence, RuleTime at, long revision)
        {
            if (evidence != ObservationEvidenceKind.Search && evidence != ObservationEvidenceKind.AttackEvidence)
                throw new ArgumentOutOfRangeException(nameof(evidence));
            var position = ObservationGeometry.Position(s, targetId);
            string episode = CurrentInvisibleEpisodeId(s, targetId);
            var prior = Knowledge(s, observerId, targetId);
            Set(s, NewKnowledge(s, observerId, targetId, true, position, evidence, at, revision,
                revealedEpisode: episode == "" ? prior?.RevealedInvisibleEpisodeId ?? "" : episode));
        }

        internal static void ApplyHide(Snapshot s, string observerId, string targetId, string attemptId,
            RuleTime at, long revision)
        {
            var prior = Knowledge(s, observerId, targetId);
            string episode = CurrentInvisibleEpisodeId(s, targetId);
            if (prior == null)
                prior = NewKnowledge(s, observerId, targetId, false, default, ObservationEvidenceKind.None, at, revision);
            Set(s, Copy(prior, currentLocationKnown: false, hiddenAttemptId: attemptId,
                revealedEpisode: episode == "" ? prior.RevealedInvisibleEpisodeId : episode));
        }

        public static void ProcessWorldTraversalSegments(Snapshot s, IReadOnlyList<ObservationMovementSegment> segments,
            RuleTime start, RuleTime end, long revision,
            ObservationAlgorithmVersion algorithmVersion = ObservationAlgorithmVersion.ExactPathIntervalsV2)
        {
            if (segments == null || segments.Count == 0 || !Enabled(s)) return;
            if (algorithmVersion != ObservationAlgorithmVersion.LegacySampledV1
                && algorithmVersion != ObservationAlgorithmVersion.ExactPathIntervalsV2)
                throw new ArgumentOutOfRangeException(nameof(algorithmVersion));
            var moving = new HashSet<string>(segments.Select(x => x.Edge.ActorId), StringComparer.Ordinal);
            foreach (var segment in segments.OrderBy(x => x.Edge.ActorId, StringComparer.Ordinal))
            {
                string mover = segment.Edge.ActorId;
                RuleQuantity minimum = segment.FromDistance.Scale(1, 5), maximum = segment.ToDistance.Scale(1, 5);
                if (maximum <= minimum) continue;
                foreach (var other in s.Actors.Where(x => x.Id != mover && !moving.Contains(x.Id)).OrderBy(x => x.Id, StringComparer.Ordinal))
                {
                    var fixedPoint = ObservationGeometry.Position(s, other.Id);
                    RecordPathSight(s, segment, mover, other.Id, true, fixedPoint, minimum, maximum, start, end, revision,
                        algorithmVersion);
                    RecordPathSight(s, segment, mover, other.Id, false, fixedPoint, minimum, maximum, start, end, revision,
                        algorithmVersion);
                }
            }
        }

        private static void RecordPathSight(Snapshot s, ObservationMovementSegment segment, string mover, string other,
            bool moverIsTarget, ObservationPoint fixedPoint, RuleQuantity minimum, RuleQuantity maximum,
            RuleTime start, RuleTime end, long revision, ObservationAlgorithmVersion algorithmVersion)
        {
            string observer = moverIsTarget ? other : mover;
            string target = moverIsTarget ? mover : other;
            long range = s.ObservationProfiles.Single(x => x.ActorId == observer).SightRangeFeet;
            bool VisibleAt(RuleQuantity parameter)
            {
                var movingPoint = ObservationGeometry.AtEdge(segment.Edge.FromX, segment.Edge.FromY,
                    segment.Edge.ToX, segment.Edge.ToY, parameter);
                var observerPoint = moverIsTarget ? fixedPoint : movingPoint;
                var targetPoint = moverIsTarget ? movingPoint : fixedPoint;
                return DirectSightAt(s, observer, target, observerPoint, targetPoint);
            }

            RuleQuantity lastParameter = default;
            bool found = false;
            bool isSightLimit = false;
            if (algorithmVersion == ObservationAlgorithmVersion.LegacySampledV1)
            {
                var samples = ObservationGeometry.ObservationSamples(s, fixedPoint, segment.Edge.FromX, segment.Edge.FromY,
                    segment.Edge.ToX, segment.Edge.ToY, range, minimum, maximum);
                foreach (var sample in samples)
                    if (VisibleAt(sample))
                    {
                        found = true;
                        lastParameter = sample;
                    }
            }
            else
            {
                var boundaries = ObservationGeometry.VisibilityBreakpoints(s, fixedPoint, segment.Edge.FromX,
                    segment.Edge.FromY, segment.Edge.ToX, segment.Edge.ToY, range)
                    .Where(x => x > minimum && x < maximum)
                    .Concat(new[] { minimum, maximum }).Distinct().OrderBy(x => x).ToArray();
                for (int i = 0; i < boundaries.Length; i++)
                {
                    RuleQuantity boundary = boundaries[i];
                    if (VisibleAt(boundary))
                    {
                        found = true;
                        lastParameter = boundary;
                        isSightLimit = false;
                    }
                    if (i + 1 >= boundaries.Length) continue;
                    RuleQuantity next = boundaries[i + 1];
                    if (VisibleAt(Midpoint(boundary, next)) && !VisibleAt(next))
                    {
                        found = true;
                        lastParameter = next;
                        isSightLimit = true;
                    }
                }
            }
            if (!found) return;
            RuleQuantity subsegment = FractionBetween(lastParameter, minimum, maximum);
            RuleTime evidenceAt = ObservationGeometry.AtTime(start, end, subsegment);
            var movingTarget = ObservationGeometry.AtEdge(segment.Edge.FromX, segment.Edge.FromY,
                segment.Edge.ToX, segment.Edge.ToY, lastParameter);
            var lastVisible = moverIsTarget ? movingTarget : fixedPoint;
            var actualTarget = ObservationGeometry.Position(s, target);
            bool stillCurrent = !moverIsTarget
                || !isSightLimit && lastVisible.X == actualTarget.X && lastVisible.Y == actualTarget.Y;
            var prior = Knowledge(s, observer, target);
            string episode = CurrentInvisibleEpisodeId(s, target);
            Set(s, NewKnowledge(s, observer, target, stillCurrent, lastVisible,
                isSightLimit ? ObservationEvidenceKind.DirectSightLimit : ObservationEvidenceKind.DirectSight,
                evidenceAt, revision,
                revealedEpisode: episode == "" ? prior?.RevealedInvisibleEpisodeId ?? "" : episode));
        }

        private static RuleQuantity Midpoint(RuleQuantity left, RuleQuantity right)
            => RuleQuantity.FromFraction((System.Numerics.BigInteger)left.Numerator * right.Denominator
                + (System.Numerics.BigInteger)right.Numerator * left.Denominator,
                (System.Numerics.BigInteger)2 * left.Denominator * right.Denominator);

        private static RuleQuantity FractionBetween(RuleQuantity point, RuleQuantity start, RuleQuantity end)
        {
            var numerator = (System.Numerics.BigInteger)point.Numerator * start.Denominator
                - (System.Numerics.BigInteger)start.Numerator * point.Denominator;
            numerator *= end.Denominator;
            var denominator = (System.Numerics.BigInteger)point.Denominator
                * ((System.Numerics.BigInteger)end.Numerator * start.Denominator
                    - (System.Numerics.BigInteger)start.Numerator * end.Denominator);
            return RuleQuantity.FromFraction(numerator, denominator);
        }

        private static ObserverKnowledgeRecord NewKnowledge(Snapshot s, string observer, string target,
            bool current, ObservationPoint point, ObservationEvidenceKind evidence, RuleTime at, long revision,
            string hiddenAttempt = "", string revealedEpisode = "")
            => new ObserverKnowledgeRecord(observer, target, evidence != ObservationEvidenceKind.None,
                current, point.X, point.Y, evidence, at, revision, hiddenAttempt, revealedEpisode);

        private static ObserverKnowledgeRecord Copy(ObserverKnowledgeRecord prior, bool? currentLocationKnown = null,
            string hiddenAttemptId = null, string revealedEpisode = null)
            => new ObserverKnowledgeRecord(prior.ObserverId, prior.TargetId, prior.HasLastKnownLocation,
                currentLocationKnown ?? prior.CurrentLocationKnown, prior.LastKnownX, prior.LastKnownY, prior.Evidence,
                prior.EvidenceAt, prior.EvidenceRevision, hiddenAttemptId ?? prior.HiddenAttemptId,
                revealedEpisode ?? prior.RevealedInvisibleEpisodeId);

        private static ObserverKnowledgeRecord Knowledge(Snapshot s, string observer, string target)
            => s.ObserverKnowledge.SingleOrDefault(x => x.ObserverId == observer && x.TargetId == target);

        private static void Set(Snapshot s, ObserverKnowledgeRecord value)
        {
            var prior = Knowledge(s, value.ObserverId, value.TargetId);
            if (prior == null)
            {
                if (s.ObserverKnowledge.Length >= ObservationValidation.MaxKnowledgePairs)
                    throw new InvalidOperationException("Observation knowledge capacity reached.");
                s.ObserverKnowledge = s.ObserverKnowledge.Concat(new[] { value }).OrderBy(x => x.ObserverId, StringComparer.Ordinal)
                    .ThenBy(x => x.TargetId, StringComparer.Ordinal).ToArray();
            }
            else s.ObserverKnowledge = s.ObserverKnowledge.Select(x => x.ObserverId == value.ObserverId && x.TargetId == value.TargetId ? value : x).ToArray();
        }
    }
}
#endif
