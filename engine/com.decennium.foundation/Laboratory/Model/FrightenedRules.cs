#if DECENNIUM_TEST_ONLY && (UNITY_EDITOR || DEVELOPMENT_BUILD || HEADLESS_TESTS)
using System;
using System.Collections.Generic;
using System.Linq;
using System.Numerics;

namespace Decennium.Foundation.Laboratory
{
    /// <summary>Exact willing-displacement assessment under the admitted planar metric.
    /// Source motion changes the contemporaneous geometry, but is never charged as the
    /// affected actor's motion. This supplies no forced-movement or action authority.</summary>
    public static class FrightenedMovementRules
    {
        private readonly struct Signed : IComparable<Signed>
        {
            internal readonly BigInteger N, D;
            internal Signed(BigInteger numerator, BigInteger denominator)
            {
                if (denominator == 0) throw new ArgumentException("Zero denominator.");
                if (denominator < 0) { numerator = -numerator; denominator = -denominator; }
                var gcd = BigInteger.GreatestCommonDivisor(BigInteger.Abs(numerator), denominator);
                N = numerator / gcd; D = denominator / gcd;
            }
            internal static Signed From(RuleQuantity value) => new Signed(value.Numerator, value.Denominator);
            internal static Signed Add(Signed a, Signed b) => new Signed(a.N * b.D + b.N * a.D, a.D * b.D);
            internal static Signed Subtract(Signed a, Signed b) => new Signed(a.N * b.D - b.N * a.D, a.D * b.D);
            internal static Signed Multiply(Signed a, Signed b) => new Signed(a.N * b.N, a.D * b.D);
            internal Signed Abs() => new Signed(BigInteger.Abs(N), D);
            public int CompareTo(Signed other) => (N * other.D).CompareTo(other.N * D);
            internal RuleQuantity Quantity() => RuleQuantity.FromFraction(N, D);
        }

        /// <summary>First exact fraction after which this straight simultaneous segment
        /// would include prohibited willing approach, or null for a lawful entire segment.</summary>
        public static RuleQuantity? FirstProhibitedFraction(
            (RuleQuantity X, RuleQuantity Y) actorFrom, (RuleQuantity X, RuleQuantity Y) actorTo,
            (RuleQuantity X, RuleQuantity Y) sourceFrom, (RuleQuantity X, RuleQuantity Y) sourceTo)
        {
            var zero = new Signed(0, 1); var one = new Signed(1, 1);
            Signed Difference(RuleQuantity a, RuleQuantity b) => Signed.Subtract(Signed.From(a), Signed.From(b));
            var x = Difference(actorFrom.X, sourceFrom.X); var y = Difference(actorFrom.Y, sourceFrom.Y);
            var actorDx = Difference(actorTo.X, actorFrom.X); var actorDy = Difference(actorTo.Y, actorFrom.Y);
            if (actorDx.N == 0 && actorDy.N == 0) return null;
            var relativeDx = Signed.Subtract(actorDx, Difference(sourceTo.X, sourceFrom.X));
            var relativeDy = Signed.Subtract(actorDy, Difference(sourceTo.Y, sourceFrom.Y));
            var boundaries = new List<Signed> { zero, one };
            void Root(Signed start, Signed velocity)
            {
                if (velocity.N == 0) return;
                var root = new Signed(-start.N * velocity.D, start.D * velocity.N);
                if (root.CompareTo(zero) > 0 && root.CompareTo(one) < 0
                    && !boundaries.Any(value => value.CompareTo(root) == 0)) boundaries.Add(root);
            }
            // These are every change of sign or active facet of max(abs(x),abs(y)).
            Root(x, relativeDx); Root(y, relativeDy);
            Root(Signed.Subtract(x, y), Signed.Subtract(relativeDx, relativeDy));
            Root(Signed.Add(x, y), Signed.Add(relativeDx, relativeDy));
            boundaries.Sort();
            for (int i = 0; i + 1 < boundaries.Count; i++) {
                var sample = Signed.Multiply(Signed.Add(boundaries[i], boundaries[i + 1]), new Signed(1, 2));
                var atX = Signed.Add(x, Signed.Multiply(relativeDx, sample));
                var atY = Signed.Add(y, Signed.Multiply(relativeDy, sample));
                // Evaluate the norm's directional derivative using only actor velocity.
                // At zero on an axis, its absolute-value derivative cannot be negative.
                bool xCloser = atX.N.Sign * actorDx.N.Sign < 0;
                bool yCloser = atY.N.Sign * actorDy.N.Sign < 0;
                int dominant = atX.Abs().CompareTo(atY.Abs());
                if (dominant > 0 ? xCloser : dominant < 0 ? yCloser : xCloser && yCloser)
                    return boundaries[i].Quantity();
            }
            return null;
        }
    }

    /// <summary>Shared condition/observation projection. No caller supplies the feared
    /// entity, its visibility, a distance or an exemption from willing movement.</summary>
    internal static class FrightenedRules
    {
        internal static ConditionApplication[] Operative(Snapshot state, string actor)
        {
            var journal = state.Conditions.SingleOrDefault(x => x.Target == actor);
            if (journal == null || journal.PolicyId != ConditionJournal.RelationshipPolicyId)
                return Array.Empty<ConditionApplication>();
            var ledger = TestOnlyClubAttackPolicy.ConditionsFor(state, actor);
            var ids = new HashSet<string>(ledger.View().Sources(ConditionKind.Frightened), StringComparer.Ordinal);
            return ledger.Applications.Where(x => ids.Contains(x.Id)).Select(x => x.Application).ToArray();
        }
        internal static bool VisibleSource(Snapshot state, string actor)
            => Operative(state, actor).Any(x => ObservationRules.CanSee(state, actor, x.Fear.FearedEntityId));

        internal static string WillingStepFailure(Snapshot state, string actor,
            (RuleQuantity X, RuleQuantity Y) destination)
        {
            var origin = WorldPositionResolver.Position(state, actor);
            foreach (var application in Operative(state, actor)) {
                var source = WorldPositionResolver.Position(state, application.Fear.FearedEntityId);
                if (FrightenedMovementRules.FirstProhibitedFraction(origin, destination, source, source).HasValue)
                    return "FrightenedPreventsWillingApproach";
            }
            return null;
        }
    }
}
#endif
