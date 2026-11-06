#if DECENNIUM_TEST_ONLY && (UNITY_EDITOR || DEVELOPMENT_BUILD || HEADLESS_TESTS)
using System;
using System.Collections.Generic;
using System.Globalization;
using System.Linq;
using System.Numerics;
using System.Security.Cryptography;
using System.Text;

namespace Decennium.Foundation.Laboratory
{
    /// <summary>Explicit cell channels. Placement is validated separately from each query channel;
    /// sight, effect and movement blockers remain independent facts.</summary>
    public sealed class ObservationGridCell
    {
        public int X { get; }
        public int Y { get; }
        public bool BlocksSight { get; }
        public bool BlocksEffect { get; }
        public bool BlocksMovement { get; }
        public bool Solid { get; }
        public ObservationGridCell(int x, int y, bool blocksSight, bool blocksEffect, bool blocksMovement, bool solid = false)
        {
            if (!blocksSight && !blocksEffect && !blocksMovement && !solid || solid && !blocksMovement)
                throw new ArgumentException("Observation cell must declare a blocker channel; solid cells must block movement.");
            X = x; Y = y; BlocksSight = blocksSight; BlocksEffect = blocksEffect; BlocksMovement = blocksMovement; Solid = solid;
        }
        internal string Key => string.Join(",", new[] { X.ToString(CultureInfo.InvariantCulture), Y.ToString(CultureInfo.InvariantCulture),
            BlocksSight ? "1" : "0", BlocksEffect ? "1" : "0", BlocksMovement ? "1" : "0", Solid ? "1" : "0" });
    }

    /// <summary>Explicit per-actor TEST_ONLY sight and candidate-search reach. These values are
    /// fixture facts, not universal Decennium sensory ranges.</summary>
    public sealed class ObservationSightProfile
    {
        public string ActorId { get; }
        public long SightRangeFeet { get; }
        public long SearchRangeFeet { get; }
        public ObservationSightProfile(string actorId, long sightRangeFeet, long searchRangeFeet)
        {
            if (!Validation.ValidId(actorId) || sightRangeFeet < 0 || searchRangeFeet < 0)
                throw new ArgumentException("Invalid authored observation profile.");
            ActorId = actorId; SightRangeFeet = sightRangeFeet; SearchRangeFeet = searchRangeFeet;
        }
        internal string Key => ActorId + "|" + SightRangeFeet.ToString(CultureInfo.InvariantCulture) + "|" + SearchRangeFeet.ToString(CultureInfo.InvariantCulture);
    }

    /// <summary>Immutable, content-fingerprinted planar map for the TEST_ONLY shared-world host.</summary>
    public sealed class ObservationFixture
    {
        private readonly ObservationGridCell[] cells;
        private readonly ObservationSightProfile[] profiles;
        public int Width { get; }
        public int Height { get; }
        public IReadOnlyList<ObservationGridCell> Cells => Array.AsReadOnly(cells);
        public IReadOnlyList<ObservationSightProfile> Profiles => Array.AsReadOnly(profiles);
        public ObservationFixture(int width, int height, IEnumerable<ObservationGridCell> cells,
            IEnumerable<ObservationSightProfile> profiles)
        {
            if (width < 1 || width > 64 || height < 1 || height > 64 || cells == null || profiles == null)
                throw new ArgumentException("Invalid authored observation map.");
            this.cells = cells.ToArray(); this.profiles = profiles.ToArray();
            if (this.cells.Any(x => x == null) || this.profiles.Any(x => x == null)
                || this.cells.Any(x => x.X < 0 || x.X >= width || x.Y < 0 || x.Y >= height)
                || this.cells.Select(x => x.X + "," + x.Y).Distinct(StringComparer.Ordinal).Count() != this.cells.Length
                || this.profiles.Select(x => x.ActorId).Distinct(StringComparer.Ordinal).Count() != this.profiles.Length
                || this.profiles.Length < 2 || this.profiles.Length > Snapshot.MaxActors)
                throw new ArgumentException("Invalid or duplicate observation fixture rows.");
            Width = width; Height = height;
            this.cells = this.cells.OrderBy(x => x.X).ThenBy(x => x.Y).ToArray();
            this.profiles = this.profiles.OrderBy(x => x.ActorId, StringComparer.Ordinal).ToArray();
        }
        public bool InBounds(int x, int y) => x >= 0 && x < Width && y >= 0 && y < Height;
        public ObservationSightProfile Profile(string actorId) => profiles.SingleOrDefault(x => x.ActorId == actorId);
        public ObservationGridCell Cell(int x, int y) => cells.SingleOrDefault(c => c.X == x && c.Y == y);
        internal bool SupportsAnchorAt(int x, int y) => InBounds(x, y)
            && !Blocks(x, y, ObservationChannel.Sight)
            && !Blocks(x, y, ObservationChannel.Effect)
            && !Blocks(x, y, ObservationChannel.Movement);
        internal bool Blocks(int x, int y, ObservationChannel channel)
        {
            var cell = Cell(x, y);
            if (cell == null) return false;
            return channel == ObservationChannel.Sight ? cell.BlocksSight
                : channel == ObservationChannel.Effect ? cell.BlocksEffect : cell.BlocksMovement;
        }
        internal string Key => "observation-map-v1|" + Width.ToString(CultureInfo.InvariantCulture) + "x" + Height.ToString(CultureInfo.InvariantCulture)
            + "|cells=" + string.Join(";", cells.Select(x => x.Key)) + "|profiles=" + string.Join(";", profiles.Select(x => x.Key))
            + "|cell-centres|chebyshev-5ft|supercover-closed-cell-corner-blocks|channels-independent";
        internal static string BindFingerprint(string prior, ObservationFixture fixture)
            => BindFingerprint(prior, fixture, ObservationAlgorithmVersion.LegacySampledV1);

        internal static string BindFingerprint(string prior, ObservationFixture fixture,
            ObservationAlgorithmVersion algorithmVersion)
        {
            string fingerprintKind = algorithmVersion == ObservationAlgorithmVersion.LegacySampledV1
                ? "TEST_ONLY.observation-v1-" : "TEST_ONLY.observation-v2-";
            string procedure = algorithmVersion == ObservationAlgorithmVersion.LegacySampledV1
                ? fixture.Key : fixture.Key + "|exact-path-sight-intervals-v2|excluded-sight-loss-boundaries";
            using (var sha = SHA256.Create())
                return fingerprintKind + string.Concat(sha.ComputeHash(Encoding.UTF8.GetBytes(prior + "|" + procedure))
                    .Select(b => b.ToString("x2", CultureInfo.InvariantCulture)));
        }
        internal string ValidateSnapshot(Snapshot s)
        {
            if (s.Actors.Any(a => !SupportsAnchorAt(a.X, a.Y))
                || s.Objects.Any(o => !SupportsAnchorAt(o.X, o.Y))
                || !s.Actors.Select(a => a.Id).OrderBy(x => x, StringComparer.Ordinal)
                    .SequenceEqual(profiles.Select(x => x.ActorId).OrderBy(x => x, StringComparer.Ordinal)))
                return "ObservationMapPlacementOrProfileMismatch";
            if (s.ObservationMapWidth != Width || s.ObservationMapHeight != Height
                || s.ObservationCells.Length != cells.Length || s.ObservationProfiles.Length != profiles.Length
                || s.ObservationCells.OrderBy(x => x.X).ThenBy(x => x.Y)
                    .Zip(cells, (a, b) => a.X == b.X && a.Y == b.Y && a.BlocksSight == b.BlocksSight
                        && a.BlocksEffect == b.BlocksEffect && a.BlocksMovement == b.BlocksMovement && a.Solid == b.Solid).Any(x => !x)
                || s.ObservationProfiles.OrderBy(x => x.ActorId, StringComparer.Ordinal)
                    .Zip(profiles, (a, b) => a.ActorId == b.ActorId && a.SightRangeFeet == b.SightRangeFeet
                        && a.SearchRangeFeet == b.SearchRangeFeet).Any(x => !x)) return "ObservationContentMismatch";
            if (s.WorldTraversals.Any(x => !InBounds(x.FromX, x.FromY) || !InBounds(x.ToX, x.ToY)
                || !SupportsAnchorAt(x.FromX, x.FromY) || !SupportsAnchorAt(x.ToX, x.ToY)))
                return "ObservationTraversalOutsideSupportedAnchors";
            return null;
        }
        internal void Initialize(Snapshot s)
        {
            s.ObservationMapWidth = Width; s.ObservationMapHeight = Height;
            s.ObservationCells = cells.Select(x => new ObservationMapCellRecord(x.X, x.Y,
                x.BlocksSight, x.BlocksEffect, x.BlocksMovement, x.Solid)).ToArray();
            s.ObservationProfiles = profiles.Select(x => new ObservationProfileRecord(x.ActorId,
                x.SightRangeFeet, x.SearchRangeFeet)).ToArray();
        }
    }

    internal enum ObservationChannel { Sight, Effect, Movement }

    /// <summary>Exact rational point in authored grid-cell coordinates. Actor anchors are integer
    /// cell centres; active world movement offsets them by the persisted exact partial distance.</summary>
    internal readonly struct ObservationPoint
    {
        internal RuleQuantity X { get; }
        internal RuleQuantity Y { get; }
        internal ObservationPoint(RuleQuantity x, RuleQuantity y) { X = x; Y = y; }
    }

    /// <summary>Deterministic planar visibility, line-of-effect and movement-channel queries.</summary>
    public static class ObservationGeometry
    {
        private readonly struct Fraction : IComparable<Fraction>, IEquatable<Fraction>
        {
            internal readonly BigInteger N, D;
            internal Fraction(BigInteger n, BigInteger d)
            {
                if (d == 0) throw new DivideByZeroException();
                if (d < 0) { n = -n; d = -d; }
                var gcd = BigInteger.GreatestCommonDivisor(BigInteger.Abs(n), d);
                N = n / gcd; D = d / gcd;
            }
            internal Fraction(long n) { N = n; D = 1; }
            internal static Fraction From(RuleQuantity value) => new Fraction(value.Numerator, value.Denominator);
            public int CompareTo(Fraction other) => (N * other.D).CompareTo(other.N * D);
            public bool Equals(Fraction other) => N == other.N && D == other.D;
            public override bool Equals(object obj) => obj is Fraction other && Equals(other);
            public override int GetHashCode() => unchecked(N.GetHashCode() * 397 ^ D.GetHashCode());
            public static Fraction operator +(Fraction a, Fraction b) => new Fraction(a.N * b.D + b.N * a.D, a.D * b.D);
            public static Fraction operator -(Fraction a, Fraction b) => new Fraction(a.N * b.D - b.N * a.D, a.D * b.D);
            public static Fraction operator -(Fraction value) => new Fraction(-value.N, value.D);
            public static Fraction operator *(Fraction a, Fraction b) => new Fraction(a.N * b.N, a.D * b.D);
            public static Fraction operator /(Fraction a, Fraction b) => new Fraction(a.N * b.D, a.D * b.N);
            public static bool operator <(Fraction a, Fraction b) => a.CompareTo(b) < 0;
            public static bool operator >(Fraction a, Fraction b) => a.CompareTo(b) > 0;
            public static bool operator <=(Fraction a, Fraction b) => a.CompareTo(b) <= 0;
            public static bool operator >=(Fraction a, Fraction b) => a.CompareTo(b) >= 0;
            internal static Fraction Abs(Fraction x) => x.N < 0 ? new Fraction(-x.N, x.D) : x;
            internal RuleQuantity NonnegativeQuantity() => RuleQuantity.FromFraction(N, D);
        }

        private readonly struct Point
        {
            internal readonly Fraction X, Y;
            internal Point(Fraction x, Fraction y) { X = x; Y = y; }
            internal static Point From(ObservationPoint p) => new Point(Fraction.From(p.X), Fraction.From(p.Y));
            internal static Point Cell(int x, int y) => new Point(new Fraction(x), new Fraction(y));
            internal static Point Lerp(Point a, Point b, Fraction t) => new Point(a.X + (b.X - a.X) * t, a.Y + (b.Y - a.Y) * t);
        }

        internal static ObservationPoint Position(Snapshot s, string actorId)
        {
            var actor = s.Actors.Single(a => a.Id == actorId);
            var edge = s.WorldTraversals.SingleOrDefault(x => x.ActorId == actorId);
            if (edge == null) return new ObservationPoint(new RuleQuantity(actor.X), new RuleQuantity(actor.Y));
            int dx = Math.Sign(edge.ToX - edge.FromX), dy = Math.Sign(edge.ToY - edge.FromY);
            RuleQuantity Coordinate(int origin, int direction)
            {
                BigInteger numerator = (BigInteger)origin * 5 * edge.DistanceFeet.Denominator
                    + (BigInteger)direction * edge.DistanceFeet.Numerator;
                return RuleQuantity.FromFraction(numerator, (BigInteger)5 * edge.DistanceFeet.Denominator);
            }
            return new ObservationPoint(Coordinate(edge.FromX, dx), Coordinate(edge.FromY, dy));
        }

        public static bool CanSee(Snapshot s, ObservationFixture fixture, string observerId, string targetId)
            => CanSeeAt(fixture, Profile(fixture, observerId), Point.From(Position(s, observerId)), Point.From(Position(s, targetId)));

        public static bool CanSee(Snapshot s, string observerId, string targetId)
        {
            if (s == null || s.ObservationMapWidth < 1) return false;
            return GeometricSight(s, observerId, Position(s, observerId), Position(s, targetId));
        }

        internal static bool GeometricSight(Snapshot s, string observerId, ObservationPoint observerPosition, ObservationPoint targetPosition)
        {
            var profile = s.ObservationProfiles.SingleOrDefault(x => x.ActorId == observerId);
            if (profile == null) return false;
            Point from = Point.From(observerPosition), to = Point.From(targetPosition);
            Fraction range = new Fraction(profile.SightRangeFeet, 5);
            return Fraction.Abs(to.X - from.X) <= range && Fraction.Abs(to.Y - from.Y) <= range
                && ClearLine(s, from, to, ObservationChannel.Sight);
        }

        public static bool LineOfEffectClear(Snapshot s, ObservationFixture fixture, string sourceId, string targetId)
            => ClearLine(fixture, Point.From(Position(s, sourceId)), Point.From(Position(s, targetId)), ObservationChannel.Effect);

        public static bool LineOfEffectClear(Snapshot s, string sourceId, string targetId)
            => s != null && s.ObservationMapWidth > 0
                && ClearLine(s, Point.From(Position(s, sourceId)), Point.From(Position(s, targetId)), ObservationChannel.Effect);

        public static bool Walkable(ObservationFixture fixture, int x, int y)
            => fixture != null && fixture.InBounds(x, y) && !fixture.Blocks(x, y, ObservationChannel.Movement);

        public static bool Walkable(Snapshot s, int x, int y)
            => s != null && x >= 0 && x < s.ObservationMapWidth && y >= 0 && y < s.ObservationMapHeight
                && !s.ObservationCells.Any(c => c.X == x && c.Y == y && c.BlocksMovement);

        /// <summary>Checks whether an actor or anchored object may use this cell as a position.
        /// A blocker on any observation channel needs a separately authored surface/anchor model.</summary>
        public static bool SupportsAnchorAt(ObservationFixture fixture, int x, int y)
            => fixture != null && fixture.SupportsAnchorAt(x, y);

        public static bool SupportsAnchorAt(Snapshot s, int x, int y)
            => s != null && x >= 0 && x < s.ObservationMapWidth && y >= 0 && y < s.ObservationMapHeight
                && !s.ObservationCells.Any(c => c.X == x && c.Y == y
                    && (c.BlocksSight || c.BlocksEffect || c.BlocksMovement));

        internal static bool ClearLine(ObservationFixture fixture, ObservationPoint from, ObservationPoint to, ObservationChannel channel)
            => ClearLine(fixture, Point.From(from), Point.From(to), channel);

        private static bool CanSeeAt(ObservationFixture fixture, ObservationSightProfile profile, Point from, Point to)
        {
            if (fixture == null || profile == null) return false;
            Fraction rangeCells = new Fraction(profile.SightRangeFeet, 5);
            if (Fraction.Abs(to.X - from.X) > rangeCells || Fraction.Abs(to.Y - from.Y) > rangeCells) return false;
            return ClearLine(fixture, from, to, ObservationChannel.Sight);
        }

        private static bool ClearLine(ObservationFixture fixture, Point from, Point to, ObservationChannel channel)
        {
            if (fixture == null) return false;
            foreach (var cell in fixture.Cells)
            {
                if (!fixture.Blocks(cell.X, cell.Y, channel)) continue;
                var minX = new Fraction(2L * cell.X - 1, 2); var maxX = new Fraction(2L * cell.X + 1, 2);
                var minY = new Fraction(2L * cell.Y - 1, 2); var maxY = new Fraction(2L * cell.Y + 1, 2);
                if (SegmentIntersects(from, to, minX, maxX, minY, maxY)) return false;
            }
            return true;
        }

        private static bool ClearLine(Snapshot s, Point from, Point to, ObservationChannel channel)
        {
            foreach (var cell in s.ObservationCells)
            {
                bool blocks = channel == ObservationChannel.Sight ? cell.BlocksSight
                    : channel == ObservationChannel.Effect ? cell.BlocksEffect : cell.BlocksMovement;
                if (!blocks) continue;
                var minX = new Fraction(2L * cell.X - 1, 2); var maxX = new Fraction(2L * cell.X + 1, 2);
                var minY = new Fraction(2L * cell.Y - 1, 2); var maxY = new Fraction(2L * cell.Y + 1, 2);
                if (SegmentIntersects(from, to, minX, maxX, minY, maxY)) return false;
            }
            return true;
        }

        private static bool SegmentIntersects(Point a, Point b, Fraction minX, Fraction maxX, Fraction minY, Fraction maxY)
        {
            Fraction enter = new Fraction(0), exit = new Fraction(1);
            if (!ClipAxis(a.X, b.X - a.X, minX, maxX, ref enter, ref exit)
                || !ClipAxis(a.Y, b.Y - a.Y, minY, maxY, ref enter, ref exit)) return false;
            return enter <= exit && exit >= new Fraction(0) && enter <= new Fraction(1);
        }

        private static bool ClipAxis(Fraction origin, Fraction delta, Fraction minimum, Fraction maximum,
            ref Fraction enter, ref Fraction exit)
        {
            if (delta.N == 0) return origin >= minimum && origin <= maximum;
            Fraction a = (minimum - origin) / delta, b = (maximum - origin) / delta;
            if (a > b) { var temp = a; a = b; b = temp; }
            if (a > enter) enter = a;
            if (b < exit) exit = b;
            return enter <= exit;
        }

        /// <summary>Returns exact path parameters at which sight can change along one straight cell
        /// edge. Between consecutive values, blocker-cell supercover and Chebyshev range are stable.</summary>
        internal static IReadOnlyList<RuleQuantity> VisibilityBreakpoints(ObservationFixture fixture,
            ObservationPoint fixedPosition, int fromX, int fromY, int toX, int toY, long rangeFeet)
            => VisibilityBreakpointsCore(fixture.Cells.Where(x => x.BlocksSight).Select(x => (X: x.X, Y: x.Y)),
                fixedPosition, fromX, fromY, toX, toY, rangeFeet);

        internal static IReadOnlyList<RuleQuantity> VisibilityBreakpoints(Snapshot s, ObservationPoint fixedPosition,
            int fromX, int fromY, int toX, int toY, long rangeFeet)
            => VisibilityBreakpointsCore(s.ObservationCells.Where(x => x.BlocksSight).Select(x => (X: x.X, Y: x.Y)),
                fixedPosition, fromX, fromY, toX, toY, rangeFeet);

        private static IReadOnlyList<RuleQuantity> VisibilityBreakpointsCore(IEnumerable<(int X, int Y)> blockers,
            ObservationPoint fixedPosition, int fromX, int fromY, int toX, int toY, long rangeFeet)
        {
            var values = new List<Fraction> { new Fraction(0), new Fraction(1) };
            Point fixedPoint = Point.From(fixedPosition);
            Point start = Point.Cell(fromX, fromY), end = Point.Cell(toX, toY);
            Fraction dx = end.X - start.X, dy = end.Y - start.Y;
            Fraction range = new Fraction(rangeFeet, 5);
            if (dx.N != 0)
            {
                AddParameter(values, (fixedPoint.X - range - start.X) / dx);
                AddParameter(values, (fixedPoint.X + range - start.X) / dx);
            }
            if (dy.N != 0)
            {
                AddParameter(values, (fixedPoint.Y - range - start.Y) / dy);
                AddParameter(values, (fixedPoint.Y + range - start.Y) / dy);
            }
            foreach (var cell in blockers)
            {
                for (int sx = -1; sx <= 1; sx += 2)
                    for (int sy = -1; sy <= 1; sy += 2)
                    {
                        var corner = new Point(new Fraction(2L * cell.X + sx, 2), new Fraction(2L * cell.Y + sy, 2));
                        Fraction vx = corner.X - fixedPoint.X, vy = corner.Y - fixedPoint.Y;
                        Fraction wx = start.X - fixedPoint.X, wy = start.Y - fixedPoint.Y;
                        Fraction denominator = dx * vy - dy * vx;
                        Fraction numerator = -(wx * vy - wy * vx);
                        if (denominator.N != 0) AddParameter(values, numerator / denominator);
                        else if (numerator.N == 0)
                        {
                            Fraction lengthSquared = dx * dx + dy * dy;
                            if (lengthSquared.N != 0)
                                AddParameter(values, ((corner.X - start.X) * dx + (corner.Y - start.Y) * dy) / lengthSquared);
                        }
                    }
            }
            values.Sort();
            var unique = new List<Fraction>();
            foreach (var value in values) if (unique.Count == 0 || !unique[unique.Count - 1].Equals(value)) unique.Add(value);
            return Array.AsReadOnly(unique.Select(x => x.NonnegativeQuantity()).ToArray());
        }

        private static void AddParameter(List<Fraction> values, Fraction value)
        { if (value >= new Fraction(0) && value <= new Fraction(1)) values.Add(value); }

        internal static IReadOnlyList<RuleQuantity> ObservationSamples(ObservationFixture fixture,
            ObservationPoint fixedPosition, int fromX, int fromY, int toX, int toY, long rangeFeet)
            => ObservationSamples(VisibilityBreakpoints(fixture, fixedPosition, fromX, fromY, toX, toY, rangeFeet));

        internal static IReadOnlyList<RuleQuantity> ObservationSamples(Snapshot s, ObservationPoint fixedPosition,
            int fromX, int fromY, int toX, int toY, long rangeFeet)
            => ObservationSamples(VisibilityBreakpoints(s, fixedPosition, fromX, fromY, toX, toY, rangeFeet));

        internal static IReadOnlyList<RuleQuantity> ObservationSamples(Snapshot s, ObservationPoint fixedPosition,
            int fromX, int fromY, int toX, int toY, long rangeFeet, RuleQuantity minimum, RuleQuantity maximum)
        {
            if (minimum > maximum || maximum > new RuleQuantity(1)) throw new ArgumentException("Invalid visibility interval.");
            var boundaries = new List<RuleQuantity> { minimum, maximum };
            boundaries.AddRange(VisibilityBreakpoints(s, fixedPosition, fromX, fromY, toX, toY, rangeFeet)
                .Where(x => x > minimum && x < maximum));
            return ObservationSamples(Array.AsReadOnly(boundaries.Distinct().OrderBy(x => x).ToArray()));
        }

        private static IReadOnlyList<RuleQuantity> ObservationSamples(IReadOnlyList<RuleQuantity> values)
        {
            var breaks = values.ToArray();
            var samples = new List<RuleQuantity>(breaks);
            for (int i = 0; i + 1 < breaks.Length; i++)
                samples.Add(RuleQuantity.FromFraction((BigInteger)breaks[i].Numerator * breaks[i + 1].Denominator
                    + (BigInteger)breaks[i + 1].Numerator * breaks[i].Denominator,
                    (BigInteger)2 * breaks[i].Denominator * breaks[i + 1].Denominator));
            return Array.AsReadOnly(samples.OrderBy(x => x).ToArray());
        }

        internal static ObservationPoint AtEdge(int fromX, int fromY, int toX, int toY, RuleQuantity parameter)
        {
            int dx = Math.Sign(toX - fromX), dy = Math.Sign(toY - fromY);
            RuleQuantity Coordinate(int origin, int direction)
            {
                BigInteger numerator = (BigInteger)origin * parameter.Denominator + (BigInteger)direction * parameter.Numerator;
                return RuleQuantity.FromFraction(numerator, parameter.Denominator);
            }
            return new ObservationPoint(Coordinate(fromX, dx), Coordinate(fromY, dy));
        }

        internal static RuleTime AtTime(RuleTime start, RuleTime end, RuleQuantity fraction)
        {
            BigInteger deltaN = (BigInteger)end.Numerator * start.Denominator - (BigInteger)start.Numerator * end.Denominator;
            BigInteger deltaD = (BigInteger)end.Denominator * start.Denominator;
            BigInteger n = (BigInteger)start.Numerator * deltaD * fraction.Denominator
                + deltaN * fraction.Numerator * start.Denominator;
            BigInteger d = (BigInteger)start.Denominator * deltaD * fraction.Denominator;
            return RuleTime.FromFraction(n, d);
        }

        private static ObservationSightProfile Profile(ObservationFixture fixture, string actorId)
            => fixture?.Profile(actorId);
    }
}
#endif
