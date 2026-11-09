using System;
using System.Linq;

namespace Decennium.Foundation
{
    /// <summary>Persisted projection of an authored route's exact physical pose. While Attached,
    /// this is derived from route Progress and fingerprinted route-motion content. While Detached,
    /// it is the frozen exact rejoin reference; ordinary traversal owns the live position.</summary>
    public sealed class ExpeditionRouteSpatialRecord
    {
        public string RouteId { get; }
        public string TravelerId { get; }
        public long TravelStartedRevision { get; }
        public RuleQuantity X { get; }
        public RuleQuantity Y { get; }
        public bool Detached { get; }

        public ExpeditionRouteSpatialRecord(string routeId, string travelerId, long travelStartedRevision,
            RuleQuantity x, RuleQuantity y, bool detached)
        {
            if (!Validation.ValidId(routeId) || !Validation.ValidId(travelerId) || travelStartedRevision < 1
                || x < default(RuleQuantity) || y < default(RuleQuantity))
                throw new ArgumentException("Invalid expedition route spatial record.");
            RouteId = routeId; TravelerId = travelerId; TravelStartedRevision = travelStartedRevision;
            X = x; Y = y; Detached = detached;
        }

        public ExpeditionRouteSpatialRecord With(RuleQuantity x, RuleQuantity y, bool detached)
            => new ExpeditionRouteSpatialRecord(RouteId, TravelerId, TravelStartedRevision, x, y, detached);
    }

    public static class ExpeditionRouteSpatialValidation
    {
        public static void Validate(Snapshot s)
        {
            if (s.RouteTravelSpatial == null || s.RouteTravelSpatial.Length > ExpeditionRouteTravelValidation.MaxRecords
                || s.RouteTravelSpatial.Any(x => x == null))
                throw new ArgumentException("Invalid expedition route spatial records.");
            if (s.SchemaVersion < Snapshot.RouteObservationSchema)
            {
                if (s.RouteTravelSpatial.Length != 0) throw new ArgumentException("Route spatial state requires schema53.");
                return;
            }
            bool Active(ExpeditionRouteTravelRecord travel) => travel.Status == ExpeditionRouteTravelStatus.Moving
                || travel.Status == ExpeditionRouteTravelStatus.Paused;
            if (s.RouteTravelSpatial.Select(x => x.TravelStartedRevision).Distinct().Count() != s.RouteTravelSpatial.Length
                || s.RouteTravelSpatial.Select(x => x.TravelerId).Distinct(StringComparer.Ordinal).Count() != s.RouteTravelSpatial.Length
                || s.RouteTravelSpatial.Any(x => x.TravelStartedRevision > s.Revision
                    || !s.RouteTravels.Any(t => t.RouteId == x.RouteId && t.TravelerId == x.TravelerId
                        && t.StartedRevision == x.TravelStartedRevision && Active(t))
                    || x.Detached && s.RouteTravels.Single(t => t.StartedRevision == x.TravelStartedRevision).Status
                        != ExpeditionRouteTravelStatus.Paused
                    || s.ObservationMapWidth > 0 && (x.X >= new RuleQuantity(s.ObservationMapWidth)
                        || x.Y >= new RuleQuantity(s.ObservationMapHeight))))
                throw new ArgumentException("Invalid expedition route spatial references.");
            var active = s.RouteTravels.Where(Active).ToArray();
            if (active.Any(t => s.RouteTravelSpatial.Count(x => x.TravelStartedRevision == t.StartedRevision
                    && x.TravelerId == t.TravelerId && x.RouteId == t.RouteId) != 1)
                || s.RouteTravelSpatial.Any(x => !active.Any(t => t.StartedRevision == x.TravelStartedRevision)))
                throw new ArgumentException("Active route travel requires one spatial authority record.");
        }
    }
}
