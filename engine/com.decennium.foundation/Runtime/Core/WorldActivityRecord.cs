using System;
using System.Collections.Generic;
using System.Linq;
using System.Numerics;

namespace Decennium.Foundation
{
    public enum WorldActionCommitment { None, Dash, ActiveLabor }
    public enum WorldProcedureKind { Crop, WaterFill, Intake, FormulaWork, Repair, Manufacturing, FishingTrapRetrieval, SupplyCache, FishingTrapSetup, Harvest, Mining, Prospecting, MiningAssay, MineralPreparation, CacheExcavation, RouteMappingWork }

    /// <summary>Derived activity projection over the existing procedure records. It is never saved
    /// independently; each domain procedure remains authoritative for its state and settlement.</summary>
    public sealed class WorldProcedureActivity
    {
        public string Id { get; }
        public string ActorId { get; }
        public WorldProcedureKind Kind { get; }
        /// <summary>The source procedure's status name. Null only for rows built with the legacy identity-only constructor.</summary>
        public string Status { get; }
        /// <summary>Exact recorded active-work progress, in seconds, when the procedure stores it.</summary>
        public RuleTime? RecordedWorkDone { get; }
        /// <summary>Exact required active-work time when the procedure record stores it.</summary>
        public RuleTime? RecordedWorkRequired { get; }
        /// <summary>Existing ledger intervals and material reservations linked to this procedure ID.</summary>
        public IReadOnlyList<WorkerInterval> WorkerIntervals { get; }
        public IReadOnlyList<ResourceReservation> ResourceReservations { get; }
        /// <summary>Nearest future start/end of a linked worker interval, if one is recorded.</summary>
        public RuleTime? NextWorkerBoundary { get; }
        /// <summary>Admissible pause/resume/cancel/resolve options discovered for this exact actor and procedure.</summary>
        public IReadOnlyList<CommandOption> AvailableCommands { get; }
        public WorldProcedureActivity(string id, string actorId, WorldProcedureKind kind)
            : this(id, actorId, kind, null, null, null, Array.Empty<WorkerInterval>(),
                Array.Empty<ResourceReservation>(), null, Array.Empty<CommandOption>())
        {
        }

        internal WorldProcedureActivity(string id, string actorId, WorldProcedureKind kind, string status,
            RuleTime? recordedWorkDone, RuleTime? recordedWorkRequired, IEnumerable<WorkerInterval> workerIntervals,
            IEnumerable<ResourceReservation> resourceReservations, RuleTime? nextWorkerBoundary,
            IEnumerable<CommandOption> availableCommands)
        {
            if (!Validation.ValidId(id) || !Validation.ValidId(actorId) || !Enum.IsDefined(typeof(WorldProcedureKind), kind))
                throw new ArgumentException("Invalid projected world activity.");
            if (workerIntervals == null) throw new ArgumentNullException(nameof(workerIntervals));
            if (resourceReservations == null) throw new ArgumentNullException(nameof(resourceReservations));
            if (availableCommands == null) throw new ArgumentNullException(nameof(availableCommands));
            Id = id; ActorId = actorId; Kind = kind; Status = status;
            RecordedWorkDone = recordedWorkDone; RecordedWorkRequired = recordedWorkRequired;
            WorkerIntervals = Array.AsReadOnly(workerIntervals.ToArray());
            ResourceReservations = Array.AsReadOnly(resourceReservations.ToArray());
            NextWorkerBoundary = nextWorkerBoundary;
            AvailableCommands = Array.AsReadOnly(availableCommands.ToArray());
        }
    }

    /// <summary>Read-only view of one saved partial traversal. The traversal record remains authoritative.</summary>
    public sealed class WorldTraversalActivity
    {
        public string ActorId { get; }
        public long StartedRevision { get; }
        public int FromX { get; }
        public int FromY { get; }
        public int ToX { get; }
        public int ToY { get; }
        public RuleQuantity DistanceFeet { get; }
        public bool Running { get; }
        public WorldTraversalStatus Status { get; }
        /// <summary>Admissible suspend/resume controls discovered for this actor and snapshot revision.</summary>
        public IReadOnlyList<CommandOption> AvailableCommands { get; }

        internal WorldTraversalActivity(WorldTraversalRecord traversal, IEnumerable<CommandOption> availableCommands)
        {
            if (traversal == null) throw new ArgumentNullException(nameof(traversal));
            if (availableCommands == null) throw new ArgumentNullException(nameof(availableCommands));
            ActorId = traversal.ActorId; StartedRevision = traversal.StartedRevision;
            FromX = traversal.FromX; FromY = traversal.FromY; ToX = traversal.ToX; ToY = traversal.ToY;
            DistanceFeet = traversal.DistanceFeet; Running = traversal.Running; Status = traversal.Status;
            AvailableCommands = Array.AsReadOnly(availableCommands.ToArray());
        }
    }

    public static class WorldActivityProjection
    {
        /// <summary>Projects procedures which currently claim an actor's active work interval,
        /// preserving the historical domain-family and record order used by activity settlement.</summary>
        public static IReadOnlyList<WorldProcedureActivity> CurrentWork(Snapshot s)
            => CurrentWorkCore(s, null, false, false);

        /// <summary>Enriches current work with facts from its procedure record, the shared work ledger,
        /// and command options already discovered by Simulation. It does not discover or authorize commands.</summary>
        public static IReadOnlyList<WorldProcedureActivity> CurrentWork(Snapshot s, IEnumerable<CommandOption> discoveredOptions)
        {
            if (discoveredOptions == null) throw new ArgumentNullException(nameof(discoveredOptions));
            return CurrentWorkCore(s, discoveredOptions.Where(x => x != null).ToArray(), true, false);
        }

        /// <summary>Projects persisted work procedures in working, paused, or explicit awaiting states. It is
        /// separate from CurrentWork so active-labor conflict checks keep their historical membership and order.</summary>
        public static IReadOnlyList<WorldProcedureActivity> OpenProcedures(Snapshot s, IEnumerable<CommandOption> discoveredOptions)
        {
            if (discoveredOptions == null) throw new ArgumentNullException(nameof(discoveredOptions));
            return CurrentWorkCore(s, discoveredOptions.Where(x => x != null).ToArray(), true, true);
        }

        /// <summary>Projects persisted partial traversals and only their same-revision admissible
        /// suspend/resume controls. It does not discover commands or change route state.</summary>
        public static IReadOnlyList<WorldTraversalActivity> Traversals(Snapshot s, IEnumerable<CommandOption> discoveredOptions)
        {
            if (s == null) throw new ArgumentNullException(nameof(s));
            if (discoveredOptions == null) throw new ArgumentNullException(nameof(discoveredOptions));
            var options = discoveredOptions.Where(x => x != null).ToArray();
            return Array.AsReadOnly((s.WorldTraversals ?? Array.Empty<WorldTraversalRecord>())
                .OrderBy(x => x.ActorId, StringComparer.Ordinal)
                .Select(edge => new WorldTraversalActivity(edge, options.Where(x => x.Command.Actor == edge.ActorId
                    && (x.Command.Kind == CommandKind.SuspendWorldStep || x.Command.Kind == CommandKind.ResumeWorldStep)
                    && x.Command.Target == "" && x.Command.X == 0 && x.Command.Y == 0
                    && x.Command.ExpectedRevision == s.Revision && x.Query.ObservedRevision == s.Revision
                    && x.Query.Supported && x.Query.Admissible)
                    .OrderBy(x => x.Command.Kind).ThenBy(x => x.Command.Id, StringComparer.Ordinal)))
                .ToArray());
        }

        private static IReadOnlyList<WorldProcedureActivity> CurrentWorkCore(Snapshot s, CommandOption[] options, bool includeDetails, bool includeOpen)
        {
            if (s == null) throw new ArgumentNullException(nameof(s));
            var result = new List<WorldProcedureActivity>();
            foreach (var crop in s.Crops ?? Array.Empty<CropBatchRecord>())
                foreach (var task in crop.Tasks.Where(x => x.Status == CropWorkStatus.Working
                    || includeOpen && x.Status == CropWorkStatus.Paused))
                    result.Add(Create(s, task.Id, task.WorkerId, WorldProcedureKind.Crop, includeDetails ? task.Status.ToString() : null,
                        includeDetails ? (RuleTime?)task.Progress : null, null, options, includeDetails));
            foreach (var fill in s.WaterFills ?? Array.Empty<WaterFillRecord>())
                if (fill.Status == WaterFillStatus.Working || includeOpen && fill.Status == WaterFillStatus.Paused)
                    result.Add(Create(s, fill.Id, fill.WorkerId, WorldProcedureKind.WaterFill,
                    includeDetails ? fill.Status.ToString() : null, includeDetails ? (RuleTime?)fill.Progress : null, null, options, includeDetails));
            foreach (var intake in s.Intakes ?? Array.Empty<IntakeRecord>())
                if (intake.Status == IntakeStatus.Working) result.Add(Create(s, intake.Id, intake.ActorId, WorldProcedureKind.Intake,
                    includeDetails ? intake.Status.ToString() : null, null, null, options, includeDetails));
            foreach (var formula in s.FormulaWork ?? Array.Empty<FormulaWorkRecord>())
                if (formula.Status == FormulaWorkStatus.Working || includeOpen
                    && (formula.Status == FormulaWorkStatus.Paused || formula.Status == FormulaWorkStatus.AwaitingCheck))
                    result.Add(Create(s, formula.Id, formula.WorkerId, WorldProcedureKind.FormulaWork,
                    includeDetails ? formula.Status.ToString() : null, includeDetails ? (RuleTime?)formula.Work.Retained : null,
                    includeDetails ? (RuleTime?)formula.Work.Required : null, options, includeDetails));
            foreach (var repair in s.RepairWork ?? Array.Empty<RepairWorkRecord>())
                if (repair.Status == RepairWorkStatus.Working || includeOpen && repair.Open)
                    result.Add(Create(s, repair.Id, repair.WorkerId, WorldProcedureKind.Repair,
                    includeDetails ? repair.Status.ToString() : null, includeDetails ? (RuleTime?)repair.Work.Retained : null,
                    includeDetails ? (RuleTime?)repair.Work.Required : null, options, includeDetails));
            foreach (var order in s.ManufacturingOrders ?? Array.Empty<ManufacturingOrderRecord>())
                if (order.Status == ManufacturingStatus.Working || includeOpen && order.Open)
                    result.Add(Create(s, order.Id, order.WorkerId, WorldProcedureKind.Manufacturing,
                    includeDetails ? order.Status.ToString() : null, includeDetails ? (RuleTime?)order.Work.Retained : null,
                    includeDetails ? (RuleTime?)order.Work.Required : null, options, includeDetails));
            foreach (var retrieval in s.FishingTrapRetrievals ?? Array.Empty<FishingTrapRetrievalRecord>())
                if (retrieval.Status == FishingTrapRetrievalStatus.Working
                    || includeOpen && retrieval.Status == FishingTrapRetrievalStatus.Paused)
                    result.Add(Create(s, retrieval.Id, retrieval.WorkerId,
                    WorldProcedureKind.FishingTrapRetrieval, includeDetails ? retrieval.Status.ToString() : null,
                    includeDetails ? (RuleTime?)retrieval.WorkDone : null, null, options, includeDetails));
            foreach (var attempt in s.SupplyCacheAttempts ?? Array.Empty<SupplyCacheAttemptRecord>())
                if (attempt.Status == SupplyCacheAttemptStatus.Working) result.Add(Create(s, attempt.Id, attempt.ActorId,
                    WorldProcedureKind.SupplyCache, includeDetails ? attempt.Status.ToString() : null, null, null, options, includeDetails));
            foreach (var attempt in s.FishingTrapAttempts ?? Array.Empty<FishingTrapAttemptRecord>())
                if (attempt.Status == FishingTrapAttemptStatus.SettingUp
                    || includeOpen && attempt.Status == FishingTrapAttemptStatus.Paused)
                    result.Add(Create(s, attempt.Id, attempt.SetterId,
                    WorldProcedureKind.FishingTrapSetup, includeDetails ? attempt.Status.ToString() : null,
                    includeDetails ? (RuleTime?)attempt.SetupLabor : null, null, options, includeDetails));
            foreach (var attempt in s.HarvestAttempts ?? Array.Empty<HarvestAttemptRecord>())
                if (attempt.Status == HarvestAttemptStatus.Working || includeOpen && attempt.Status == HarvestAttemptStatus.Paused)
                    result.Add(Create(s, attempt.Id, attempt.WorkerId, WorldProcedureKind.Harvest,
                    includeDetails ? attempt.Status.ToString() : null, includeDetails ? (RuleTime?)attempt.WorkDone : null,
                    includeDetails ? (RuleTime?)attempt.Duration : null, options, includeDetails));
            foreach (var attempt in s.MiningAttempts ?? Array.Empty<MiningAttemptRecord>())
                if (attempt.Status == MiningAttemptStatus.Working || includeOpen
                    && (attempt.Status == MiningAttemptStatus.Paused || attempt.Status == MiningAttemptStatus.AwaitingCheck))
                    result.Add(Create(s, attempt.Id, attempt.WorkerId, WorldProcedureKind.Mining,
                    includeDetails ? attempt.Status.ToString() : null,
                    includeDetails ? (RuleTime?)attempt.WorkDone : null,
                    includeDetails ? (RuleTime?)new RuleTime(attempt.DurationSeconds) : null, options, includeDetails));
            foreach (var attempt in s.ProspectingAttempts ?? Array.Empty<ProspectingAttemptRecord>())
                if (attempt.Status == ProspectingAttemptStatus.Working || includeOpen
                    && (attempt.Status == ProspectingAttemptStatus.Paused || attempt.Status == ProspectingAttemptStatus.AwaitingCheck))
                    result.Add(Create(s, attempt.Id, attempt.ActorId, WorldProcedureKind.Prospecting,
                    includeDetails ? attempt.Status.ToString() : null, includeDetails ? (RuleTime?)attempt.WorkDone : null,
                    includeDetails ? (RuleTime?)new RuleTime(ProspectingValidation.WorkSeconds) : null, options, includeDetails));
            foreach (var attempt in s.MiningAssayAttempts ?? Array.Empty<MiningAssayAttemptRecord>())
                if (attempt.Status == MiningAssayStatus.Working || includeOpen
                    && (attempt.Status == MiningAssayStatus.Paused || attempt.Status == MiningAssayStatus.AwaitingCheck))
                    result.Add(Create(s, attempt.Id, attempt.WorkerId, WorldProcedureKind.MiningAssay,
                    includeDetails ? attempt.Status.ToString() : null, includeDetails ? (RuleTime?)attempt.WorkDone : null,
                    includeDetails ? (RuleTime?)new RuleTime(MiningAssayValidation.WorkSeconds) : null, options, includeDetails));
            foreach (var attempt in s.DestructiveMiningAssayAttempts ?? Array.Empty<DestructiveMiningAssayAttemptRecord>())
                if (attempt.Status == MiningAssayStatus.Working || includeOpen
                    && (attempt.Status == MiningAssayStatus.Paused || attempt.Status == MiningAssayStatus.AwaitingCheck))
                    result.Add(Create(s, attempt.Id, attempt.WorkerId, WorldProcedureKind.MiningAssay,
                    includeDetails ? attempt.Status.ToString() : null, includeDetails ? (RuleTime?)attempt.WorkDone : null,
                    includeDetails ? (RuleTime?)new RuleTime(MiningAssayValidation.WorkSeconds) : null, options, includeDetails));
            foreach (var attempt in s.MineralPreparationAttempts ?? Array.Empty<MineralPreparationAttemptRecord>())
                if (attempt.Status == MineralPreparationStatus.Working || includeOpen
                    && (attempt.Status == MineralPreparationStatus.Paused || attempt.Status == MineralPreparationStatus.AwaitingCompletion))
                    result.Add(Create(s, attempt.Id, attempt.WorkerId, WorldProcedureKind.MineralPreparation,
                    includeDetails ? attempt.Status.ToString() : null, includeDetails ? (RuleTime?)attempt.WorkDone : null,
                    includeDetails ? (RuleTime?)new RuleTime(MineralPreparationValidation.WorkSeconds) : null, options, includeDetails));
            foreach (var excavation in s.CacheExcavations ?? Array.Empty<CacheExcavationRecord>())
                if (excavation.Status == CacheExcavationStatus.Working
                    || includeOpen && excavation.Status == CacheExcavationStatus.Paused)
                    result.Add(Create(s, excavation.Id, excavation.WorkerId, WorldProcedureKind.CacheExcavation,
                    includeDetails ? excavation.Status.ToString() : null, includeDetails ? (RuleTime?)excavation.WorkDone : null,
                    includeDetails ? (RuleTime?)new RuleTime(CacheExcavationRecord.RequiredWorkSeconds) : null, options, includeDetails));
            foreach (var attempt in s.RouteMappingWorkAttempts ?? Array.Empty<ExpeditionRouteMappingWorkAttemptRecord>())
                if (attempt.Status == ExpeditionRouteMappingWorkStatus.Working
                    || includeOpen && (attempt.Status == ExpeditionRouteMappingWorkStatus.Paused
                        || attempt.Status == ExpeditionRouteMappingWorkStatus.AwaitingCheck))
                    foreach (string worker in new[] { attempt.LeadId }.Concat(attempt.AssistantIds))
                        result.Add(Create(s, attempt.Id, worker, WorldProcedureKind.RouteMappingWork,
                            includeDetails ? attempt.Status.ToString() : null,
                            includeDetails ? (RuleTime?)attempt.WorkDone : null,
                            includeDetails ? (RuleTime?)attempt.WorkRequired : null, options, includeDetails));
            return result.AsReadOnly();
        }

        private static WorldProcedureActivity Create(Snapshot s, string id, string actorId, WorldProcedureKind kind,
            string status, RuleTime? workDone, RuleTime? workRequired, CommandOption[] options, bool includeDetails)
            => includeDetails ? Project(s, id, actorId, kind, status, workDone, workRequired, options)
                : new WorldProcedureActivity(id, actorId, kind);

        private static WorldProcedureActivity Project(Snapshot s, string id, string actorId, WorldProcedureKind kind,
            string status, RuleTime? workDone, RuleTime? workRequired, CommandOption[] options)
        {
            var workerIntervals = s.Work.WorkerIntervals.Where(x => x.JobId == id && x.WorkerId == actorId).ToArray();
            var resourceReservations = s.Work.Reservations.Where(x => x.JobId == id).ToArray();
            RuleTime? nextBoundary = null;
            foreach (var interval in workerIntervals)
            {
                if (interval.Start > s.RuleClock && (!nextBoundary.HasValue || interval.Start < nextBoundary.Value)) nextBoundary = interval.Start;
                if (interval.End > s.RuleClock && (!nextBoundary.HasValue || interval.End < nextBoundary.Value)) nextBoundary = interval.End;
            }
            string controlTarget = kind == WorldProcedureKind.FishingTrapSetup
                ? s.FishingTrapAttempts.SingleOrDefault(x => x.Id == id)?.TrapId
                : kind == WorldProcedureKind.FishingTrapRetrieval
                    ? s.FishingTrapRetrievals.SingleOrDefault(x => x.Id == id)?.TrapId : id;
            var controls = options.Where(x => x.Command.Actor == actorId
                    && (x.Command.Target == id && IsProcedureControl(x.Command.Kind)
                        || (kind == WorldProcedureKind.FishingTrapSetup || kind == WorldProcedureKind.FishingTrapRetrieval)
                            && x.Command.Kind == CommandKind.Interact && x.Command.Target == controlTarget)
                    && x.Command.ExpectedRevision == s.Revision && x.Query.ObservedRevision == s.Revision
                    && x.Query.Supported && x.Query.Admissible)
                .OrderBy(x => x.Command.Kind).ThenBy(x => x.Command.Id, StringComparer.Ordinal).ToArray();
            return new WorldProcedureActivity(id, actorId, kind, status, workDone, workRequired,
                workerIntervals, resourceReservations, nextBoundary, controls);
        }

        private static bool IsProcedureControl(CommandKind kind)
        {
            switch (kind)
            {
                case CommandKind.PauseCrop:
                case CommandKind.InterruptIntake:
                case CommandKind.PauseWaterFill: case CommandKind.ResumeWaterFill: case CommandKind.CancelWaterFill:
                case CommandKind.PauseFormulaWork: case CommandKind.ResumeFormulaWork: case CommandKind.CancelFormulaWork:
                case CommandKind.PauseToolRepair: case CommandKind.ResumeToolRepair: case CommandKind.CancelToolRepair:
                case CommandKind.PauseManufacturing: case CommandKind.ResumeManufacturing: case CommandKind.CancelManufacturing:
                case CommandKind.ResolveManufacturingQuality:
                case CommandKind.PauseHarvest: case CommandKind.ResumeHarvest:
                case CommandKind.PauseMining: case CommandKind.ResumeMining:
                case CommandKind.PauseProspecting: case CommandKind.ResumeProspecting:
                case CommandKind.PauseMiningAssay: case CommandKind.ResumeMiningAssay: case CommandKind.CancelMiningAssay:
                case CommandKind.PauseMineralPreparation: case CommandKind.ResumeMineralPreparation:
                case CommandKind.PauseCacheExcavation: case CommandKind.ResumeCacheExcavation:
                case CommandKind.PauseRouteMappingWork: case CommandKind.ResumeRouteMappingWork:
                    return true;
                default:
                    return false;
            }
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
                || s.FishingTrapAttempts.Any(x => x.Id == id && x.SetterId == actor)
                || s.MiningAttempts.Any(x => x.Id == id && x.WorkerId == actor)
                || s.ProspectingAttempts.Any(x => x.Id == id && x.ActorId == actor)
                || s.MiningAssayAttempts.Any(x => x.Id == id && x.WorkerId == actor)
                || s.DestructiveMiningAssayAttempts.Any(x => x.Id == id && x.WorkerId == actor)
                || s.MineralPreparationAttempts.Any(x => x.Id == id && x.WorkerId == actor)
                || s.CacheExcavations.Any(x => x.Id == id && x.WorkerId == actor);
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
