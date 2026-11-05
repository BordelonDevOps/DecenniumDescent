using System;
using System.Collections.Generic;
using System.Globalization;
using System.Linq;
using System.Numerics;

namespace Decennium.Foundation
{
    /// <summary>A fixed calendar, distinct from control mode and encounter identity. Empty intervals
    /// are addressed analytically; the cursor never awards a bank of skipped Actions.</summary>
    public sealed class WorldScheduleRecord
    {
        public string Id { get; }
        public RuleTime Origin { get; }
        public IReadOnlyList<string> Order { get; }
        public long ProcessedSlot { get; }
        public WorldScheduleRecord(string id, RuleTime origin, IEnumerable<string> order, long processedSlot = 0)
        {
            if (!Validation.ValidId(id) || !Validation.ValidId(id + ".start." + long.MaxValue.ToString(CultureInfo.InvariantCulture)) || order == null || processedSlot < 0)
                throw new ArgumentException("Invalid world schedule.");
            var actors = order.ToArray();
            if (actors.Length < 1 || actors.Length > 64 || actors.Any(x => !Validation.ValidId(x)) || actors.Distinct(StringComparer.Ordinal).Count() != actors.Length)
                throw new ArgumentException("Invalid schedule roster.");
            Id = id; Origin = origin; Order = Array.AsReadOnly(actors); ProcessedSlot = processedSlot;
        }
        public RuleTime Start(long ordinal)
        {
            if (ordinal < 0) throw new ArgumentOutOfRangeException(nameof(ordinal));
            return RuleTime.FromFraction((BigInteger)Origin.Numerator * Order.Count + (BigInteger)6 * ordinal * Origin.Denominator, (BigInteger)Origin.Denominator * Order.Count);
        }
        public long SlotAt(RuleTime at)
        {
            if (at < Origin) throw new ArgumentException("No pre-origin virtual turns.");
            return checked((long)(((BigInteger)at.Numerator * Origin.Denominator - (BigInteger)Origin.Numerator * at.Denominator) * Order.Count
                / ((BigInteger)6 * at.Denominator * Origin.Denominator)));
        }
        public long LatestStart(string actor, long slot)
        {
            int index = -1; for (int i = 0; i < Order.Count; i++) if (Order[i] == actor) index = i;
            if (index < 0 || slot < 0) throw new ArgumentException("Unknown actor or slot.");
            return slot < index ? -1 : slot - (slot - index) % Order.Count;
        }
        public string MarkerId(long ordinal)
        {
            if (ordinal < 0) throw new ArgumentOutOfRangeException(nameof(ordinal));
            return Id + ".start." + ordinal.ToString(CultureInfo.InvariantCulture);
        }
        public WorldScheduleRecord At(long slot) => new WorldScheduleRecord(Id, Origin, Order, slot);
    }

    /// <summary>Exact ordinary-interval spending, including exploration before the first combat input.
    /// A LastStart of -1 is the single bootstrap allowance before this actor's first scheduled Start.</summary>
    public sealed class WorldIntervalRecord
    {
        public string ActorId { get; }
        public long LastStart { get; }
        public RuleQuantity MovementSpent { get; }
        public bool ActionSpent { get; }
        public bool DashPaid { get; }
        public bool ReactionAvailable { get; }
        public int Interactions { get; }
        public WorldIntervalRecord(string actor, long lastStart, RuleQuantity movementSpent = default, bool actionSpent = false,
            bool dashPaid = false, bool reactionAvailable = true, int interactions = 0)
        {
            if (!Validation.ValidId(actor) || lastStart < -1 || dashPaid && !actionSpent || interactions < 0 || interactions > 2
                || interactions == 2 && (!actionSpent || dashPaid)) throw new ArgumentException("Invalid interval ledger.");
            ActorId = actor; LastStart = lastStart; MovementSpent = movementSpent; ActionSpent = actionSpent;
            DashPaid = dashPaid; ReactionAvailable = reactionAvailable; Interactions = interactions;
        }
        public WorldIntervalRecord Spend(RuleQuantity cost) => new WorldIntervalRecord(ActorId, LastStart, MovementSpent + cost, ActionSpent, DashPaid, ReactionAvailable, Interactions);
        public WorldIntervalRecord PayDash()
        {
            if (ActionSpent) throw new InvalidOperationException("Action already spent.");
            return new WorldIntervalRecord(ActorId, LastStart, MovementSpent, true, true, ReactionAvailable, Interactions);
        }
        public WorldIntervalRecord PayAction()
        {
            if (ActionSpent) throw new InvalidOperationException("Action already spent.");
            return new WorldIntervalRecord(ActorId, LastStart, MovementSpent, true, DashPaid, ReactionAvailable, Interactions);
        }
        public WorldIntervalRecord SpendInteraction()
        {
            if (Interactions >= 2) throw new InvalidOperationException("Ordinary interaction allowance exhausted.");
            if (Interactions == 0)
                return new WorldIntervalRecord(ActorId, LastStart, MovementSpent, ActionSpent, DashPaid, ReactionAvailable, 1);
            if (ActionSpent) throw new InvalidOperationException("Second ordinary interaction requires an available Action.");
            return new WorldIntervalRecord(ActorId, LastStart, MovementSpent, true, false, ReactionAvailable, 2);
        }
        public WorldIntervalRecord WithReaction(bool available) => new WorldIntervalRecord(ActorId, LastStart, MovementSpent, ActionSpent, DashPaid, available, Interactions);
    }
    public enum WorldTraversalStatus { Moving, WaitingForRefresh, Suspended }
    /// <summary>Actual partial position along one cardinal five-foot edge. ActorState is the last
    /// completed grid anchor; spatial consumers must account for this offset before using that anchor.</summary>
    public sealed class WorldTraversalRecord
    {
        public string ActorId { get; }
        public long StartedRevision { get; }
        public int FromX { get; } public int FromY { get; } public int ToX { get; } public int ToY { get; }
        public RuleQuantity DistanceFeet { get; }
        public bool Running { get; }
        public WorldTraversalStatus Status { get; }
        public WorldTraversalRecord(string actor, long revision, int fromX, int fromY, int toX, int toY, RuleQuantity distance = default,
            bool running = false, WorldTraversalStatus status = WorldTraversalStatus.Moving)
        {
            if (!Validation.ValidId(actor) || revision < 1 || Math.Abs((long)toX - fromX) + Math.Abs((long)toY - fromY) != 1
                || distance >= new RuleQuantity(5) || !Enum.IsDefined(typeof(WorldTraversalStatus), status)) throw new ArgumentException("Invalid partial traversal.");
            ActorId = actor; StartedRevision = revision; FromX = fromX; FromY = fromY; ToX = toX; ToY = toY;
            DistanceFeet = distance; Running = running; Status = status;
        }
        public WorldTraversalRecord With(RuleQuantity distance, WorldTraversalStatus status) => new WorldTraversalRecord(ActorId, StartedRevision, FromX, FromY, ToX, ToY, distance, Running, status);
    }
    public static class WorldScheduleValidation
    {
        public static void Validate(Snapshot s)
        {
            if (s.WorldIntervals == null || s.WorldTraversals == null || s.WorldIntervals.Length > 64 || s.WorldTraversals.Length > 64
                || s.WorldIntervals.Any(x => x == null) || s.WorldTraversals.Any(x => x == null)) throw new ArgumentException("Invalid world records.");
            var schedule = s.WorldSchedule;
            if (schedule == null) {
                if (s.WorldIntervals.Length + s.WorldTraversals.Length != 0) throw new ArgumentException("World records require their calendar.");
                return;
            }
            if (s.SchemaVersion < Snapshot.SharedWorldSchema || schedule.SlotAt(s.RuleClock) != schedule.ProcessedSlot
                || schedule.Order.Any(x => !s.Actors.Any(a => a.Id == x))
                || !schedule.Order.OrderBy(x => x, StringComparer.Ordinal).SequenceEqual(s.WorldIntervals.Select(x => x.ActorId).OrderBy(x => x, StringComparer.Ordinal))
                || s.WorldIntervals.Any(x => x.LastStart != schedule.LatestStart(x.ActorId, schedule.ProcessedSlot))
                || s.WorldTraversals.Select(x => x.ActorId).Distinct(StringComparer.Ordinal).Count() != s.WorldTraversals.Length)
                throw new ArgumentException("World calendar or interval mismatch.");
            foreach (var edge in s.WorldTraversals) {
                var actor = s.Actors.SingleOrDefault(x => x.Id == edge.ActorId);
                // A traversal can belong either to an actor in the tactical calendar or to an
                // expedition member moving during noncombat exploration. The latter shares the
                // same actor position and clock, but never receives an initiative interval.
                if (actor == null || !schedule.Order.Contains(edge.ActorId) && s.InventoryCombat
                    || edge.StartedRevision > s.Revision || actor.X != edge.FromX || actor.Y != edge.FromY)
                    throw new ArgumentException("Invalid traversal reference.");
            }
        }
    }
}
