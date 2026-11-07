using System;
using System.Linq;
using System.Numerics;

namespace Decennium.Foundation
{
    /// <summary>Resolves one actor's exact physical point from the active movement authority.
    /// Ordinary traversal takes precedence while detached; an attached route pose is a validated
    /// Progress projection; ActorState is the integer anchor fallback.</summary>
    public static class WorldPositionResolver
    {
        public static (RuleQuantity X, RuleQuantity Y) Position(Snapshot snapshot, string actorId)
        {
            if (snapshot == null || !Validation.ValidId(actorId)) throw new ArgumentException("A world actor is required.");
            var actor = snapshot.Actors.Single(x => x.Id == actorId);
            var edge = snapshot.WorldTraversals?.SingleOrDefault(x => x.ActorId == actorId);
            if (edge != null)
            {
                int dx = Math.Sign(edge.ToX - edge.FromX), dy = Math.Sign(edge.ToY - edge.FromY);
                RuleQuantity Coordinate(int origin, int direction)
                {
                    BigInteger numerator = (BigInteger)origin * 5 * edge.DistanceFeet.Denominator
                        + (BigInteger)direction * edge.DistanceFeet.Numerator;
                    return RuleQuantity.FromFraction(numerator, (BigInteger)5 * edge.DistanceFeet.Denominator);
                }
                return (Coordinate(edge.FromX, dx), Coordinate(edge.FromY, dy));
            }
            var route = snapshot.RouteTravelSpatial?.SingleOrDefault(x => x.TravelerId == actorId && !x.Detached);
            return route == null ? (new RuleQuantity(actor.X), new RuleQuantity(actor.Y)) : (route.X, route.Y);
        }
    }
}
