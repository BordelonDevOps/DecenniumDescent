using System;
using System.Linq;

namespace Decennium.Foundation
{
    public static class ActorConditionValidation
    {
        public static void Validate(Snapshot s)
        {
            if (s.Conditions == null || s.Conditions.Length > Snapshot.MaxActors || s.Conditions.Any(x => x == null))
                throw new ArgumentException("Invalid condition journal collection.");
            if (s.SchemaVersion < Snapshot.ConditionSchema) {
                if (s.Conditions.Length != 0) throw new ArgumentException("Conditions require schema12.");
                return;
            }
            if (!s.Actors.Select(x => x.Id).OrderBy(x => x, StringComparer.Ordinal)
                .SequenceEqual(s.Conditions.Select(x => x.Target).OrderBy(x => x, StringComparer.Ordinal)))
                throw new ArgumentException("Condition journals must match all admitted actors.");
            if (s.Conditions.Any(x => x.Now.Time != s.RuleClock || x.Now.Phase != 0))
                throw new ArgumentException("Condition clock disagrees with world clock.");
        }
    }
}
