using System;
using System.Collections.Generic;
using System.Linq;
using System.Numerics;

namespace Decennium.Foundation
{
    public enum WorldActionCommitment { None, Dash, ActiveLabor }
    public enum WorldProcedureKind { Crop, WaterFill, Intake, FormulaWork, Repair, Manufacturing, FishingTrapRetrieval, SupplyCache, FishingTrapSetup, Harvest }

    /// <summary>Derived activity projection over the existing procedure records. It is never saved
    /// independently; each domain procedure remains authoritative for its state and settlement.</summary>
    public sealed class WorldProcedureActivity
    {
        public string Id { get; }
        public string ActorId { get; }
        public WorldProcedureKind Kind { get; }
        public WorldProcedureActivity(string id, string actorId, WorldProcedureKind kind)
        {
            if (!Validation.ValidId(id) || !Validation.ValidId(actorId) || !Enum.IsDefined(typeof(WorldProcedureKind), kind))
                throw new ArgumentException("Invalid projected world activity.");
            Id = id; ActorId = actorId; Kind = kind;
        }
    }

    public static class WorldActivityProjection
    {
        /// <summary>Projects procedures which currently claim an actor's active work interval,
        /// preserving the historical domain-family and record order used by activity settlement.</summary>
        public static IReadOnlyList<WorldProcedureActivity> CurrentWork(Snapshot s)
        {
            if (s == null) throw new ArgumentNullException(nameof(s));
            var result = new List<WorldProcedureActivity>();
            foreach (var crop in s.Crops ?? Array.Empty<CropBatchRecord>())
                foreach (var task in crop.Tasks.Where(x => x.Status == CropWorkStatus.Working))
                    result.Add(new WorldProcedureActivity(task.Id, task.WorkerId, WorldProcedureKind.Crop));
            foreach (var fill in s.WaterFills ?? Array.Empty<WaterFillRecord>())
                if (fill.Status == WaterFillStatus.Working) result.Add(new WorldProcedureActivity(fill.Id, fill.WorkerId, WorldProcedureKind.WaterFill));
            foreach (var intake in s.Intakes ?? Array.Empty<IntakeRecord>())
                if (intake.Status == IntakeStatus.Working) result.Add(new WorldProcedureActivity(intake.Id, intake.ActorId, WorldProcedureKind.Intake));
            foreach (var formula in s.FormulaWork ?? Array.Empty<FormulaWorkRecord>())
                if (formula.Status == FormulaWorkStatus.Working) result.Add(new WorldProcedureActivity(formula.Id, formula.WorkerId, WorldProcedureKind.FormulaWork));
            foreach (var repair in s.RepairWork ?? Array.Empty<RepairWorkRecord>())
                if (repair.Status == RepairWorkStatus.Working) result.Add(new WorldProcedureActivity(repair.Id, repair.WorkerId, WorldProcedureKind.Repair));
            foreach (var order in s.ManufacturingOrders ?? Array.Empty<ManufacturingOrderRecord>())
                if (order.Status == ManufacturingStatus.Working) result.Add(new WorldProcedureActivity(order.Id, order.WorkerId, WorldProcedureKind.Manufacturing));
            foreach (var retrieval in s.FishingTrapRetrievals ?? Array.Empty<FishingTrapRetrievalRecord>())
                if (retrieval.Status == FishingTrapRetrievalStatus.Working) result.Add(new WorldProcedureActivity(retrieval.Id, retrieval.WorkerId, WorldProcedureKind.FishingTrapRetrieval));
            foreach (var attempt in s.SupplyCacheAttempts ?? Array.Empty<SupplyCacheAttemptRecord>())
                if (attempt.Status == SupplyCacheAttemptStatus.Working) result.Add(new WorldProcedureActivity(attempt.Id, attempt.ActorId, WorldProcedureKind.SupplyCache));
            foreach (var attempt in s.FishingTrapAttempts ?? Array.Empty<FishingTrapAttemptRecord>())
                if (attempt.Status == FishingTrapAttemptStatus.SettingUp) result.Add(new WorldProcedureActivity(attempt.Id, attempt.SetterId, WorldProcedureKind.FishingTrapSetup));
            foreach (var attempt in s.HarvestAttempts ?? Array.Empty<HarvestAttemptRecord>())
                if (attempt.Status == HarvestAttemptStatus.Working) result.Add(new WorldProcedureActivity(attempt.Id, attempt.WorkerId, WorldProcedureKind.Harvest));
            return result.AsReadOnly();
        }
    }

    /// <summary>One off-calendar actor's ordinary six-second activity allowance. Its interval is
    /// anchored to the shared calendar origin and does not create an initiative turn.</summary>
    public sealed class WorldActivityIntervalRecord
    {
        public string CalendarId { get; }
        public string ActorId { get; }
        public long IntervalIndex { get; }
        public RuleQuantity MovementSpent { get; }
        public WorldActionCommitment Action { get; }
        public string ActionReference { get; }
        public long ActionReferenceRevision { get; }
        public bool DashPaid => Action == WorldActionCommitment.Dash;

        public WorldActivityIntervalRecord(string calendarId, string actorId, long intervalIndex,
            RuleQuantity movementSpent = default, WorldActionCommitment action = WorldActionCommitment.None,
            string actionReference = "", long actionReferenceRevision = 0)
        {
            if (!Validation.ValidId(calendarId) || !Validation.ValidId(actorId) || intervalIndex < 0
                || !Enum.IsDefined(typeof(WorldActionCommitment), action)
                || action == WorldActionCommitment.None && (actionReference != "" || actionReferenceRevision != 0)
                || action == WorldActionCommitment.Dash && (!Validation.ValidId(actionReference) || actionReferenceRevision < 1)
                || action == WorldActionCommitment.ActiveLabor && (!Validation.ValidId(actionReference) || actionReferenceRevision < 0))
                throw new ArgumentException("Invalid off-calendar activity interval.");
            CalendarId = calendarId;
            ActorId = actorId;
            IntervalIndex = intervalIndex;
            MovementSpent = movementSpent;
            Action = action;
            ActionReference = actionReference;
            ActionReferenceRevision = actionReferenceRevision;
        }

        public WorldActivityIntervalRecord Spend(RuleQuantity cost)
            => new WorldActivityIntervalRecord(CalendarId, ActorId, IntervalIndex, MovementSpent + cost,
                Action, ActionReference, ActionReferenceRevision);

        public WorldActivityIntervalRecord PayDash(string commandId, long commandRevision)
        {
            if (Action != WorldActionCommitment.None) throw new InvalidOperationException("Ordinary action already committed.");
            return new WorldActivityIntervalRecord(CalendarId, ActorId, IntervalIndex, MovementSpent,
                WorldActionCommitment.Dash, commandId, commandRevision);
        }

        public WorldActivityIntervalRecord CommitActiveLabor(string workReference)
        {
            if (!Validation.ValidId(workReference)) throw new ArgumentException("Invalid active-labor reference.");
            if (Action == WorldActionCommitment.Dash) throw new InvalidOperationException("Dash already committed this activity interval.");
            return new WorldActivityIntervalRecord(CalendarId, ActorId, IntervalIndex, MovementSpent,
                WorldActionCommitment.ActiveLabor, workReference, 0);
        }

        public static long IndexAt(WorldScheduleRecord calendar, RuleTime at)
        {
            if (calendar == null || at < calendar.Origin) throw new ArgumentException("Activity time precedes its calendar.");
            BigInteger elapsedNumerator = (BigInteger)at.Numerator * calendar.Origin.Denominator
                - (BigInteger)calendar.Origin.Numerator * at.Denominator;
            BigInteger elapsedDenominator = (BigInteger)6 * at.Denominator * calendar.Origin.Denominator;
            return checked((long)(elapsedNumerator / elapsedDenominator));
        }

        public static RuleTime StartAt(WorldScheduleRecord calendar, long intervalIndex)
        {
            if (calendar == null || intervalIndex < 0) throw new ArgumentOutOfRangeException(nameof(intervalIndex));
            return RuleTime.FromFraction((BigInteger)calendar.Origin.Numerator
                + (BigInteger)6 * intervalIndex * calendar.Origin.Denominator, calendar.Origin.Denominator);
        }

        public static RuleTime EndAt(WorldScheduleRecord calendar, long intervalIndex)
        {
            if (calendar == null || intervalIndex < 0) throw new ArgumentOutOfRangeException(nameof(intervalIndex));
            return RuleTime.FromFraction((BigInteger)calendar.Origin.Numerator
                + (BigInteger)6 * (intervalIndex + BigInteger.One) * calendar.Origin.Denominator, calendar.Origin.Denominator);
        }
    }

    public static class WorldActivityValidation
    {
        private static bool KnownProcedure(Snapshot s, string id, string actor)
        {
            return s.Crops.SelectMany(x => x.Tasks).Any(x => x.Id == id && x.WorkerId == actor)
                || s.WaterFills.Any(x => x.Id == id && x.WorkerId == actor)
                || s.Intakes.Any(x => x.Id == id && x.ActorId == actor)
                || s.FormulaWork.Any(x => x.Id == id && x.WorkerId == actor)
                || s.RepairWork.Any(x => x.Id == id && x.WorkerId == actor)
                || s.ManufacturingOrders.Any(x => x.Id == id && x.WorkerId == actor)
                || s.FishingTrapRetrievals.Any(x => x.Id == id && x.WorkerId == actor)
                || s.SupplyCacheAttempts.Any(x => x.Id == id && x.ActorId == actor)
                || s.FishingTrapAttempts.Any(x => x.Id == id && x.SetterId == actor);
        }

        /// <summary>Returns persisted work-interval provenance for positive labor in a segment.
        /// An active procedure lacking a matching worker interval remains a claim of its own.</summary>
        public static string ActiveLaborReference(Snapshot s, string actor, RuleTime start, RuleTime end)
        {
            if (s == null || !Validation.ValidId(actor) || end <= start) throw new ArgumentException("Invalid labor segment.");
            var intervals = s.Work.WorkerIntervals.Where(x => x.WorkerId == actor && x.Start < end && x.End > start)
                .OrderByDescending(x => x.End).ThenByDescending(x => x.Start).ThenBy(x => x.Id, StringComparer.Ordinal).ToArray();
            if (intervals.Length != 0) return intervals[0].Id;
            var claim = WorldActivityProjection.CurrentWork(s).FirstOrDefault(x => x.ActorId == actor
                && !s.Work.WorkerIntervals.Any(w => w.JobId == x.Id && w.WorkerId == actor));
            return claim?.Id ?? "";
        }

        /// <summary>Normalizes ledger intervals and procedure Working records into one
        /// availability answer. Linked records count once; an unlinked Working record still blocks.</summary>
        public static bool HasActiveLabor(Snapshot s, string actor, RuleTime start, RuleTime end)
        {
            if (s == null || !Validation.ValidId(actor) || end <= start) throw new ArgumentException("Invalid labor interval.");
            if (s.Work.WorkerIntervals.Any(x => x.WorkerId == actor && x.Start < end && x.End > start)) return true;
            return WorldActivityProjection.CurrentWork(s).Any(x => x.ActorId == actor
                && !s.Work.WorkerIntervals.Any(w => w.JobId == x.Id && w.WorkerId == actor));
        }

        private static bool HasReference(Snapshot s, WorldActivityIntervalRecord activity, RuleTime start, RuleTime end)
        {
            if (activity.ActionReferenceRevision != 0) return false;
            if (s.Work.WorkerIntervals.Any(x => x.Id == activity.ActionReference && x.WorkerId == activity.ActorId
                && x.Start < end && x.End > start)) return true;
            return KnownProcedure(s, activity.ActionReference, activity.ActorId);
        }

        public static void Validate(Snapshot s)
        {
            if (s.WorldActivityIntervals == null || s.WorldActivityIntervals.Length > 64
                || s.WorldActivityIntervals.Any(x => x == null)) throw new ArgumentException("Invalid activity records.");
            if (s.SchemaVersion < Snapshot.OffCalendarActivitySchema)
            {
                if (s.WorldActivityIntervals.Length != 0) throw new ArgumentException("Activity records require their schema.");
                return;
            }
            var calendar = s.WorldSchedule;
            if (calendar == null) throw new ArgumentException("Off-calendar activity requires its shared calendar.");
            var expected = s.Actors.Where(x => !calendar.Order.Contains(x.Id)).Select(x => x.Id).OrderBy(x => x, StringComparer.Ordinal).ToArray();
            var actual = s.WorldActivityIntervals.Select(x => x.ActorId).OrderBy(x => x, StringComparer.Ordinal).ToArray();
            if (!expected.SequenceEqual(actual) || s.WorldActivityIntervals.Any(x => x.CalendarId != calendar.Id
                || x.IntervalIndex != WorldActivityIntervalRecord.IndexAt(calendar, s.RuleClock)))
                throw new ArgumentException("Off-calendar activity calendar mismatch.");
            foreach (var edge in s.WorldTraversals.Where(x => x.Running && !calendar.Order.Contains(x.ActorId))) {
                var instructionReceipts = s.Receipts.Where(x => x.Revision == edge.StartedRevision).ToArray();
                if (instructionReceipts.Length != 1)
                    throw new ArgumentException("Off-calendar running traversal must reference one originating run instruction.");
                Command instruction;
                try { instruction = CommandHistory.Read(instructionReceipts[0]); }
                catch (ArgumentException) { throw new ArgumentException("Off-calendar running traversal has invalid instruction history."); }
                if (instruction.Actor != edge.ActorId || instruction.Kind != CommandKind.BeginWorldStep || instruction.Target != "run")
                    throw new ArgumentException("Off-calendar running traversal references a non-run instruction.");
            }
            foreach (var activity in s.WorldActivityIntervals.Where(x => x.Action != WorldActionCommitment.None))
            {
                RuleTime start = WorldActivityIntervalRecord.StartAt(calendar, activity.IntervalIndex);
                RuleTime end = WorldActivityIntervalRecord.EndAt(calendar, activity.IntervalIndex);
                if (activity.Action == WorldActionCommitment.Dash) {
                    var matchingReceipts = s.Receipts.Where(x => x.Id == activity.ActionReference
                        && x.Revision == activity.ActionReferenceRevision).ToArray();
                    if (matchingReceipts.Length != 1)
                        throw new ArgumentException("Dash activity must reference exactly one committed command revision.");
                    var receipt = matchingReceipts[0];
                    Command command;
                    try { command = CommandHistory.Read(receipt); }
                    catch (ArgumentException) { throw new ArgumentException("Dash activity has no valid originating command."); }
                    if (command.Actor != activity.ActorId
                        || command.Kind != CommandKind.BeginWorldStep && command.Kind != CommandKind.ResumeWorldStep
                        || command.Kind == CommandKind.BeginWorldStep && command.Target != "run")
                        throw new ArgumentException("Dash activity references a non-Dash command.");
                    if (HasActiveLabor(s, activity.ActorId, start, end))
                        throw new ArgumentException("Dash overlaps committed labor.");
                } else if (!HasReference(s, activity, start, end)) {
                    throw new ArgumentException("Active labor must reference its work history.");
                }
            }
            foreach (var edge in s.WorldTraversals.Where(x => x.Running && !calendar.Order.Contains(x.ActorId)
                && x.Status == WorldTraversalStatus.Moving))
                if (!s.WorldActivityIntervals.Single(x => x.ActorId == edge.ActorId).DashPaid)
                    throw new ArgumentException("Off-calendar running has no paid Dash.");
        }
    }
}
