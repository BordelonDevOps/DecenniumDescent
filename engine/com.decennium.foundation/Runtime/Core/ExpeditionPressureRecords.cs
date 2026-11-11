using System;
using System.Collections.Generic;
using System.Linq;
using System.Numerics;

namespace Decennium.Foundation
{
    public enum ExpeditionPressureChangeKind { OpenCombat = 1, SecuredRouteEntry = 2, ExposedCampUse = 3, FullWatchLyingLow = 4, SuccessfulRetreat = 5 }
    public enum ExpeditionPressureExposureEndKind { RouteTransition = 1, SafeHavenArrival = 2, SevereClosure = 3, RetreatCompleted = 4 }
    public enum ExpeditionPressureSettlementReason { WatchEnd = 1, HavenArrival = 2, HavenArrivalAtWatchEnd = 3 }
    public enum ExpeditionPressureOutcome { None = 0, Minor = 1, Standard = 2, Severe = 3 }
    public enum ExpeditionPressureConsequenceKind { None = 0, TimedRouteObstruction = 1, RouteClosure = 2 }
    public enum ExpeditionPressureCheckpointContext { Route = 1, Camp = 2 }

    /// <summary>Immutable fixed-cohort TEST_ONLY authority. Current Pressure is derived from this
    /// starting fact and checkpoint history; this record is not a second mutable pressure counter.</summary>
    public sealed class ExpeditionPressureCohortRecord
    {
        private readonly string[] members;
        public string Id { get; }
        public string ProfileFingerprint { get; }
        public string RouteFingerprint { get; }
        public int InitialPressure { get; }
        public IReadOnlyList<string> Members { get; }

        public ExpeditionPressureCohortRecord(string id, string profileFingerprint, string routeFingerprint,
            int initialPressure, IEnumerable<string> members)
            : this(id, profileFingerprint, routeFingerprint, initialPressure, members, 1) { }

        public static ExpeditionPressureCohortRecord ForLocalRetreat(string id, string profileFingerprint,
            string routeFingerprint, int initialPressure, IEnumerable<string> members)
            => new ExpeditionPressureCohortRecord(id, profileFingerprint, routeFingerprint, initialPressure, members, 2);

        private ExpeditionPressureCohortRecord(string id, string profileFingerprint, string routeFingerprint,
            int initialPressure, IEnumerable<string> members, int memberCount)
        {
            this.members = (members ?? Array.Empty<string>()).ToArray();
            if (!Validation.ValidId(id) || string.IsNullOrEmpty(profileFingerprint) || profileFingerprint.Length > 96
                || string.IsNullOrEmpty(routeFingerprint) || routeFingerprint.Length > 96
                || initialPressure < 0 || initialPressure > 6 || this.members.Length != memberCount
                || this.members.Any(x => !Validation.ValidId(x))
                || this.members.Distinct(StringComparer.Ordinal).Count() != this.members.Length)
                throw new ArgumentException("Invalid fixed expedition-pressure cohort.");
            Id = id; ProfileFingerprint = profileFingerprint; RouteFingerprint = routeFingerprint;
            InitialPressure = initialPressure; Members = Array.AsReadOnly(this.members);
        }

        public bool SameAs(ExpeditionPressureCohortRecord other) => other != null && Id == other.Id
            && ProfileFingerprint == other.ProfileFingerprint && RouteFingerprint == other.RouteFingerprint
            && InitialPressure == other.InitialPressure && members.SequenceEqual(other.members, StringComparer.Ordinal);
    }

    /// <summary>One interval in which the fixed cohort is actually exposed on an authored route.
    /// Ended intervals remain persisted as causal history.</summary>
    public sealed class ExpeditionPressureExposureRecord
    {
        public string Id { get; }
        public string CohortId { get; }
        public string RouteId { get; }
        public long StartedRevision { get; }
        public RuleTime StartedAt { get; }
        public RuleTime? EndedAt { get; }
        public long EndRevision { get; }
        public ExpeditionPressureExposureEndKind EndKind { get; }

        public ExpeditionPressureExposureRecord(string id, string cohortId, string routeId, long startedRevision,
            RuleTime startedAt, RuleTime? endedAt = null, long endRevision = 0,
            ExpeditionPressureExposureEndKind endKind = 0)
        {
            if (!Validation.ValidId(id) || !Validation.ValidId(cohortId) || !Validation.ValidId(routeId)
                || startedRevision < 1 || endRevision < 0 || endedAt.HasValue != (endRevision > 0)
                || endedAt.HasValue != Enum.IsDefined(typeof(ExpeditionPressureExposureEndKind), endKind)
                || endedAt.HasValue && endedAt.Value < startedAt)
                throw new ArgumentException("Invalid expedition-pressure exposure interval.");
            Id = id; CohortId = cohortId; RouteId = routeId; StartedRevision = startedRevision;
            StartedAt = startedAt; EndedAt = endedAt; EndRevision = endRevision; EndKind = endKind;
        }

        public ExpeditionPressureExposureRecord End(RuleTime at, long revision, ExpeditionPressureExposureEndKind kind)
            => new ExpeditionPressureExposureRecord(Id, CohortId, RouteId, StartedRevision, StartedAt, at, revision, kind);
        public bool SameAs(ExpeditionPressureExposureRecord x) => x != null && Id == x.Id && CohortId == x.CohortId
            && RouteId == x.RouteId && StartedRevision == x.StartedRevision && StartedAt == x.StartedAt
            && EndedAt == x.EndedAt && EndRevision == x.EndRevision && EndKind == x.EndKind;
    }

    /// <summary>A single source-evidenced Pressure cause or reduction. Multiple actual attacks can
    /// be recorded independently; checkpoint aggregation applies the OpenCombat category once per Watch.</summary>
    public sealed class ExpeditionPressureChangeRecord
    {
        public string Id { get; }
        public string CohortId { get; }
        public string ExposureId { get; }
        public string RouteId { get; }
        public long WatchIndex { get; }
        public ExpeditionPressureChangeKind Kind { get; }
        public string SourceId { get; }
        public long SourceRevision { get; }
        public RuleTime At { get; }

        public ExpeditionPressureChangeRecord(string id, string cohortId, string exposureId, string routeId,
            long watchIndex, ExpeditionPressureChangeKind kind, string sourceId, long sourceRevision, RuleTime at)
        {
            if (!Validation.ValidId(id) || !Validation.ValidId(cohortId) || !Validation.ValidId(exposureId)
                || !Validation.ValidId(routeId) || watchIndex < 0 || !Enum.IsDefined(typeof(ExpeditionPressureChangeKind), kind)
                || !Validation.ValidId(sourceId) || sourceRevision < 1)
                throw new ArgumentException("Invalid expedition-pressure change evidence.");
            Id = id; CohortId = cohortId; ExposureId = exposureId; RouteId = routeId;
            WatchIndex = watchIndex; Kind = kind; SourceId = sourceId; SourceRevision = sourceRevision; At = at;
        }

        public bool SameAs(ExpeditionPressureChangeRecord x) => x != null && Id == x.Id && CohortId == x.CohortId
            && ExposureId == x.ExposureId && RouteId == x.RouteId && WatchIndex == x.WatchIndex && Kind == x.Kind
            && SourceId == x.SourceId && SourceRevision == x.SourceRevision && At == x.At;
    }

    /// <summary>Exactly-once settlement for one fixed cohort and Watch. It carries stored Pressure,
    /// the source-adjusted check value, causal evidence, shared RNG evidence and the chosen finite consequence.</summary>
    public sealed class ExpeditionPressureCheckpointRecord
    {
        private readonly string[] causeIds;
        private readonly string[] reductionIds;
        public string Id { get; }
        public string CohortId { get; }
        public long WatchIndex { get; }
        public RuleTime At { get; }
        public ExpeditionPressureSettlementReason Reason { get; }
        public string RouteId { get; }
        public string RouteFingerprint { get; }
        public string ProfileFingerprint { get; }
        public ExpeditionRouteQuality RouteQuality { get; }
        public int RiskFloor { get; }
        public int PressureBefore { get; }
        public int StoredPressure { get; }
        public int EffectivePressure { get; }
        public IReadOnlyList<string> CauseIds { get; }
        public IReadOnlyList<string> ReductionIds { get; }
        public int Natural { get; }
        public int ModifiedTotal { get; }
        public bool RollWasModifiedOrRerolled { get; }
        public uint RandomBefore { get; }
        public uint RandomAfter { get; }
        public long WordsConsumed { get; }
        public ExpeditionPressureOutcome Outcome { get; }
        public ExpeditionPressureConsequenceKind Consequence { get; }
        public ExpeditionPressureCheckpointContext Context { get; }
        public string AffectedRouteId { get; }
        public string RetreatRouteId { get; }
        public RuleQuantity RouteProgress { get; }
        public RuleTime? ConsequenceEndsAt { get; }
        public string CommandId { get; }
        public long AppliedRevision { get; }

        public ExpeditionPressureCheckpointRecord(string id, string cohortId, long watchIndex, RuleTime at,
            ExpeditionPressureSettlementReason reason, string routeId, string routeFingerprint, string profileFingerprint,
            ExpeditionRouteQuality routeQuality, int riskFloor, int pressureBefore, int storedPressure, int effectivePressure,
            IEnumerable<string> causeIds, IEnumerable<string> reductionIds, int natural, int modifiedTotal,
            bool rollWasModifiedOrRerolled, uint randomBefore, uint randomAfter, long wordsConsumed,
            ExpeditionPressureOutcome outcome, ExpeditionPressureConsequenceKind consequence,
            string affectedRouteId, string retreatRouteId, RuleQuantity routeProgress, RuleTime? consequenceEndsAt,
            string commandId, long appliedRevision, ExpeditionPressureCheckpointContext context = ExpeditionPressureCheckpointContext.Route)
        {
            this.causeIds = (causeIds ?? Array.Empty<string>()).ToArray();
            this.reductionIds = (reductionIds ?? Array.Empty<string>()).ToArray();
            if (!Validation.ValidId(id) || !Validation.ValidId(cohortId) || watchIndex < 0
                || !Enum.IsDefined(typeof(ExpeditionPressureSettlementReason), reason) || !Validation.ValidId(routeId)
                || string.IsNullOrEmpty(routeFingerprint) || routeFingerprint.Length > 96
                || string.IsNullOrEmpty(profileFingerprint) || profileFingerprint.Length > 96
                || !Enum.IsDefined(typeof(ExpeditionRouteQuality), routeQuality)
                || riskFloor < 0 || riskFloor > 6 || pressureBefore < 0 || pressureBefore > 6
                || storedPressure < riskFloor || storedPressure > 6 || effectivePressure < 0 || effectivePressure > 6
                || this.causeIds.Length > 128 || this.reductionIds.Length > 128
                || this.causeIds.Any(x => !Validation.ValidId(x)) || this.reductionIds.Any(x => !Validation.ValidId(x))
                || this.causeIds.Distinct(StringComparer.Ordinal).Count() != this.causeIds.Length
                || this.reductionIds.Distinct(StringComparer.Ordinal).Count() != this.reductionIds.Length
                || !Enum.IsDefined(typeof(ExpeditionPressureOutcome), outcome)
                || !Enum.IsDefined(typeof(ExpeditionPressureConsequenceKind), consequence)
                || !Enum.IsDefined(typeof(ExpeditionPressureCheckpointContext), context)
                || affectedRouteId == null || affectedRouteId != "" && !Validation.ValidId(affectedRouteId)
                || retreatRouteId == null || retreatRouteId != "" && !Validation.ValidId(retreatRouteId)
                || routeProgress < default(RuleQuantity)
                || commandId == null || commandId != "" && !Validation.ValidId(commandId) || appliedRevision < 1
                || randomBefore == 0 || randomAfter == 0 || wordsConsumed < 0
                || (natural == 0) != (wordsConsumed == 0) || natural < 0 || natural > 6
                || natural == 0 && modifiedTotal != 0 || natural != 0 && (modifiedTotal < -100 || modifiedTotal > 106)
                || natural == 0 && (randomBefore != randomAfter || rollWasModifiedOrRerolled)
                || consequence == ExpeditionPressureConsequenceKind.None
                    && (affectedRouteId != "" || retreatRouteId != "" || consequenceEndsAt.HasValue)
                || consequence == ExpeditionPressureConsequenceKind.TimedRouteObstruction
                    && (affectedRouteId != routeId || retreatRouteId != "" || !consequenceEndsAt.HasValue
                        || consequenceEndsAt.Value <= at || outcome != ExpeditionPressureOutcome.Minor
                            && outcome != ExpeditionPressureOutcome.Standard)
                || consequence == ExpeditionPressureConsequenceKind.RouteClosure
                    && (affectedRouteId != routeId || retreatRouteId == "" || consequenceEndsAt.HasValue
                        || outcome != ExpeditionPressureOutcome.Severe)
                || outcome == ExpeditionPressureOutcome.None && consequence != ExpeditionPressureConsequenceKind.None
                || outcome == ExpeditionPressureOutcome.Minor && consequence != ExpeditionPressureConsequenceKind.TimedRouteObstruction
                || outcome == ExpeditionPressureOutcome.Standard && consequence != ExpeditionPressureConsequenceKind.TimedRouteObstruction
                || outcome == ExpeditionPressureOutcome.Severe && consequence != ExpeditionPressureConsequenceKind.RouteClosure)
                throw new ArgumentException("Invalid expedition-pressure checkpoint.");
            Id = id; CohortId = cohortId; WatchIndex = watchIndex; At = at; Reason = reason; RouteId = routeId;
            RouteFingerprint = routeFingerprint; ProfileFingerprint = profileFingerprint; RouteQuality = routeQuality; RiskFloor = riskFloor;
            PressureBefore = pressureBefore; StoredPressure = storedPressure; EffectivePressure = effectivePressure;
            CauseIds = Array.AsReadOnly(this.causeIds); ReductionIds = Array.AsReadOnly(this.reductionIds);
            Natural = natural; ModifiedTotal = modifiedTotal; RollWasModifiedOrRerolled = rollWasModifiedOrRerolled;
            RandomBefore = randomBefore; RandomAfter = randomAfter; WordsConsumed = wordsConsumed; Outcome = outcome;
            Consequence = consequence; Context = context; AffectedRouteId = affectedRouteId; RetreatRouteId = retreatRouteId;
            RouteProgress = routeProgress;
            ConsequenceEndsAt = consequenceEndsAt; CommandId = commandId; AppliedRevision = appliedRevision;
            if (natural != 0)
            {
                var draw = DiceStream.Draw(randomBefore, 6);
                if (draw.Value + 1 != natural || draw.NextState != randomAfter || draw.WordsConsumed != wordsConsumed)
                    throw new ArgumentException("Pressure check RNG evidence does not match the shared stream.");
            }
        }

        public bool SameAs(ExpeditionPressureCheckpointRecord x) => x != null && Id == x.Id && CohortId == x.CohortId
            && WatchIndex == x.WatchIndex && At == x.At && Reason == x.Reason && RouteId == x.RouteId
            && RouteFingerprint == x.RouteFingerprint && ProfileFingerprint == x.ProfileFingerprint && RouteQuality == x.RouteQuality && RiskFloor == x.RiskFloor
            && PressureBefore == x.PressureBefore && StoredPressure == x.StoredPressure && EffectivePressure == x.EffectivePressure
            && causeIds.SequenceEqual(x.causeIds, StringComparer.Ordinal) && reductionIds.SequenceEqual(x.reductionIds, StringComparer.Ordinal)
            && Natural == x.Natural && ModifiedTotal == x.ModifiedTotal && RollWasModifiedOrRerolled == x.RollWasModifiedOrRerolled
            && RandomBefore == x.RandomBefore && RandomAfter == x.RandomAfter && WordsConsumed == x.WordsConsumed
            && Outcome == x.Outcome && Consequence == x.Consequence && Context == x.Context && AffectedRouteId == x.AffectedRouteId
            && RetreatRouteId == x.RetreatRouteId && RouteProgress == x.RouteProgress && ConsequenceEndsAt == x.ConsequenceEndsAt
            && CommandId == x.CommandId && AppliedRevision == x.AppliedRevision;
    }

    public static class ExpeditionPressureRules
    {
        public const long WatchSeconds = 28_800;

        /// <summary>Apply source categories and the shared two-credit limit to one Watch value.</summary>
        public static int Settle(int pressureBefore, bool openCombatCategory, int qualifyingReductionCredits, int riskFloor)
            => Settle(pressureBefore, openCombatCategory ? 1 : 0, qualifyingReductionCredits, riskFloor);

        /// <summary>Apply distinct increase categories and the shared two-credit limit to one Watch value.</summary>
        public static int Settle(int pressureBefore, int increaseCategoryCount, int qualifyingReductionCredits, int riskFloor)
        {
            if (pressureBefore < 0 || pressureBefore > 6 || increaseCategoryCount < 0 || increaseCategoryCount > 5
                || qualifyingReductionCredits < 0
                || riskFloor < 0 || riskFloor > 6)
                throw new ArgumentOutOfRangeException(nameof(pressureBefore));
            int reductions = Math.Min(2, qualifyingReductionCredits);
            return Math.Max(riskFloor, Math.Min(6, pressureBefore + increaseCategoryCount - reductions));
        }

        public static int EffectiveForCheckpoint(int storedPressure, ExpeditionRouteQuality quality,
            ExpeditionPressureCheckpointContext context)
        {
            if (!Enum.IsDefined(typeof(ExpeditionPressureCheckpointContext), context))
                throw new ArgumentOutOfRangeException(nameof(context));
            return context == ExpeditionPressureCheckpointContext.Camp
                ? storedPressure : EffectiveForRouteCheck(storedPressure, quality);
        }

        public static int IncreaseCategoryCount(IEnumerable<ExpeditionPressureChangeRecord> changes)
            => changes.Where(x => x.Kind == ExpeditionPressureChangeKind.OpenCombat
                    || x.Kind == ExpeditionPressureChangeKind.ExposedCampUse)
                .Select(x => x.Kind).Distinct().Count();

        internal static int ReductionCreditCount(IEnumerable<ExpeditionPressureChangeRecord> changes)
            => changes.Count(x => x.Kind == ExpeditionPressureChangeKind.SecuredRouteEntry
                || x.Kind == ExpeditionPressureChangeKind.FullWatchLyingLow);

        public static int Current(Snapshot snapshot, string cohortId)
        {
            if (snapshot == null || !Validation.ValidId(cohortId)) throw new ArgumentException("Invalid pressure query.");
            return CurrentAt(snapshot, cohortId, snapshot.Revision, snapshot.RuleClock);
        }

        /// <summary>Resolve Pressure at an explicit causal cutoff. The command resolver may include its
        /// pending revision while advancing across multiple checkpoints before the receipt is committed.</summary>
        public static int CurrentAt(Snapshot snapshot, string cohortId, long revision, RuleTime at)
        {
            if (snapshot == null || !Validation.ValidId(cohortId) || revision < 0
                || snapshot.Revision < long.MaxValue && revision > snapshot.Revision + 1
                || revision > snapshot.Revision && snapshot.Revision == long.MaxValue
                || at < default(RuleTime) || at > snapshot.RuleClock)
                throw new ArgumentException("Invalid causal pressure query.");
            var cohort = snapshot.ExpeditionPressureCohorts.SingleOrDefault(x => x.Id == cohortId);
            if (cohort == null || snapshot.Retreat?.Definition.CohortId == cohort.Id
                && !snapshot.ExpeditionPressureExposures.Any(x => x.CohortId == cohort.Id && x.StartedRevision <= revision && x.StartedAt <= at))
                throw new ArgumentException("Unknown pressure cohort.");
            return At(snapshot, cohort, revision, at);
        }

        /// <summary>Resolve the Pressure value visible at one causal point from immutable checkpoints and
        /// source history. Schema68's late same-Watch reconciliation is derived from the existing records.</summary>
        internal static int At(Snapshot snapshot, ExpeditionPressureCohortRecord cohort, long revision, RuleTime at)
        {
            var latest = snapshot.ExpeditionPressureCheckpoints.Where(x => x.CohortId == cohort.Id
                    && x.AppliedRevision <= revision && x.At <= at)
                .OrderBy(x => x.WatchIndex).LastOrDefault();
            if (snapshot.Retreat?.Definition.CohortId == cohort.Id)
                return LocalRetreatPressure(snapshot, cohort, latest, revision, at, includeExitAtBoundary: true);
            return latest == null ? cohort.InitialPressure : AfterCheckpoint(snapshot, latest, revision, at);
        }

        // At an exact tie the Watch checkpoint owns the earlier stage of the receipt.
        internal static int LocalRetreatPressure(Snapshot s, ExpeditionPressureCohortRecord cohort,
            ExpeditionPressureCheckpointRecord latest, long revision, RuleTime at, bool includeExitAtBoundary)
        {
            var exit = s.ExpeditionPressureChanges.SingleOrDefault(x => x.CohortId == cohort.Id
                && x.Kind == ExpeditionPressureChangeKind.SuccessfulRetreat && x.SourceRevision <= revision
                && (x.At < at || x.At == at && (includeExitAtBoundary || x.SourceRevision < revision))
                && (latest == null || x.SourceRevision > latest.AppliedRevision
                    || x.SourceRevision == latest.AppliedRevision && x.At >= latest.At));
            int value = latest?.StoredPressure ?? cohort.InitialPressure;
            return exit == null ? value : Settle(value, true, 0, s.Retreat.Definition.Risk);
        }

        internal static int AfterCheckpoint(Snapshot snapshot, ExpeditionPressureCheckpointRecord checkpoint,
            long revision, RuleTime at)
        {
            if (snapshot.SchemaVersion < Snapshot.ExpeditionPressureLifecycleSchema) return checkpoint.StoredPressure;
            BigInteger watchEnd = (new BigInteger(checkpoint.WatchIndex) + BigInteger.One) * WatchSeconds;
            bool watchClosed = new BigInteger(at.Numerator) >= watchEnd * at.Denominator;
            bool admittedAfterCheckpoint = snapshot.ExpeditionPressureExposures.Any(x => x.CohortId == checkpoint.CohortId
                && x.RouteId == checkpoint.RouteId && x.StartedRevision <= checkpoint.AppliedRevision
                && x.StartedAt <= checkpoint.At && x.EndKind == ExpeditionPressureExposureEndKind.SafeHavenArrival
                && x.EndedAt.HasValue && x.EndedAt.Value > checkpoint.At && x.EndRevision > checkpoint.AppliedRevision
                && x.EndRevision <= revision && x.EndedAt.Value <= at);
            if (!watchClosed && !admittedAfterCheckpoint) return checkpoint.StoredPressure;

            var changes = snapshot.ExpeditionPressureChanges.Where(x => x.CohortId == checkpoint.CohortId
                    && x.WatchIndex == checkpoint.WatchIndex && x.SourceRevision <= revision && x.At <= at).ToArray();
            int reconciled = Settle(checkpoint.PressureBefore, IncreaseCategoryCount(changes),
                ReductionCreditCount(changes), checkpoint.RiskFloor);
            return checkpoint.StoredPressure + (reconciled - checkpoint.StoredPressure);
        }

        /// <summary>Tests attack membership against the exposure's causal end. A same-receipt opportunity
        /// attack is included only when the completed movement record proves it interrupted that departure.</summary>
        public static bool AttackWithinExposure(Snapshot snapshot, ExpeditionPressureExposureRecord exposure,
            string attackerId, string targetId, long revision, RuleTime at, bool opportunity)
        {
            if (snapshot == null || exposure == null || !Validation.ValidId(attackerId) || !Validation.ValidId(targetId)
                || revision <= exposure.StartedRevision || at < exposure.StartedAt) return false;
            if (!exposure.EndedAt.HasValue) return true;
            if (at > exposure.EndedAt.Value) return false;
            if (revision < exposure.EndRevision) return true;
            if (revision != exposure.EndRevision || at != exposure.EndedAt.Value || !opportunity
                || exposure.EndKind != ExpeditionPressureExposureEndKind.RetreatCompleted) return false;
            return snapshot.TacticalMoves.Any(move => move.ActorId == targetId
                && move.Status == TacticalMoveStatus.Completed && move.ResolvedRevision == exposure.EndRevision
                && move.Reactors.Contains(attackerId));
        }

        public static int EffectiveForRouteCheck(int storedPressure, ExpeditionRouteQuality quality)
        {
            if (storedPressure < 0 || storedPressure > 6 || !Enum.IsDefined(typeof(ExpeditionRouteQuality), quality))
                throw new ArgumentOutOfRangeException(nameof(storedPressure));
            if (storedPressure == 0 || storedPressure == 6) return storedPressure;
            int modifier = quality == ExpeditionRouteQuality.Secured ? -1
                : quality == ExpeditionRouteQuality.Contested ? 1 : 0;
            return Math.Max(0, Math.Min(6, storedPressure + modifier));
        }

        public static ExpeditionPressureOutcome Classify(int effectivePressure, int natural, int modifiedTotal,
            bool rollWasModifiedOrRerolled)
        {
            if (effectivePressure < 0 || effectivePressure > 6) throw new ArgumentOutOfRangeException(nameof(effectivePressure));
            if (effectivePressure == 0) return ExpeditionPressureOutcome.None;
            if (effectivePressure == 6) return ExpeditionPressureOutcome.Severe;
            if (natural < 1 || natural > 6 || modifiedTotal < -100 || modifiedTotal > 106)
                throw new ArgumentOutOfRangeException(nameof(natural));
            if (modifiedTotal > effectivePressure) return ExpeditionPressureOutcome.None;
            if (natural == 1) return ExpeditionPressureOutcome.Severe;
            if (modifiedTotal == effectivePressure && rollWasModifiedOrRerolled) return ExpeditionPressureOutcome.Minor;
            return ExpeditionPressureOutcome.Standard;
        }
    }

    public static class ExpeditionPressureValidation
    {
        public const int MaxCohorts = 8;
        public const int MaxExposures = 256;
        public const int MaxChanges = 1024;
        public const int MaxCheckpoints = 512;

        public static void Validate(Snapshot s)
        {
            if (s.ExpeditionPressureCohorts == null || s.ExpeditionPressureExposures == null
                || s.ExpeditionPressureChanges == null || s.ExpeditionPressureCheckpoints == null
                || s.ExpeditionPressureCohorts.Length > MaxCohorts || s.ExpeditionPressureExposures.Length > MaxExposures
                || s.ExpeditionPressureChanges.Length > MaxChanges || s.ExpeditionPressureCheckpoints.Length > MaxCheckpoints
                || s.ExpeditionPressureCohorts.Any(x => x == null) || s.ExpeditionPressureExposures.Any(x => x == null)
                || s.ExpeditionPressureChanges.Any(x => x == null) || s.ExpeditionPressureCheckpoints.Any(x => x == null))
                throw new ArgumentException("Invalid expedition-pressure collections.");
            if (s.SchemaVersion < Snapshot.ExpeditionPressureSchema)
            {
                if (s.ExpeditionPressureCohorts.Length + s.ExpeditionPressureExposures.Length
                    + s.ExpeditionPressureChanges.Length + s.ExpeditionPressureCheckpoints.Length != 0)
                    throw new ArgumentException("Expedition pressure requires schema67.");
                return;
            }
            bool localRetreat = s.SchemaVersion >= Snapshot.RetreatSchema && s.Retreat != null;
            if (localRetreat) ValidateLocalAuthority(s);
            if((s.SchemaVersion==Snapshot.HarvestPreservationSchema||s.SchemaVersion==Snapshot.HarvestPreservationTreatmentSchema
                    ||s.SchemaVersion==Snapshot.HarvestPreservationExposureSchema||s.SchemaVersion==Snapshot.MiningAssistantSchema
                    ||s.SchemaVersion==Snapshot.HavenAppraisalSchema||s.SchemaVersion==Snapshot.HavenSaleSchema||s.SchemaVersion>=Snapshot.HavenMealSchema)
                &&s.TestOnly&&s.ExpeditionPressureCohorts.Length==0
                &&s.ExpeditionPressureExposures.Length==0&&s.ExpeditionPressureChanges.Length==0
                &&s.ExpeditionPressureCheckpoints.Length==0)return;
            if (s.SchemaVersion == Snapshot.ExpeditionPressureSchema
                && s.ExpeditionPressureExposures.Any(x => x.EndKind == ExpeditionPressureExposureEndKind.RetreatCompleted))
                throw new ArgumentException("Retreat completion requires the pressure lifecycle schema.");
            if (s.ExpeditionPressureCohorts.Length != 1
                || s.ExpeditionPressureCohorts.Select(x => x.Id).Distinct(StringComparer.Ordinal).Count() != s.ExpeditionPressureCohorts.Length
                || s.ExpeditionPressureCohorts.Any(x => x.Members.Count != (localRetreat ? 2 : 1)
                    || x.Members.Any(id => !s.Actors.Any(a => a.Id == id)) || x.ProfileFingerprint != s.ContentFingerprint)
                || s.ExpeditionPressureExposures.Select(x => x.Id).Distinct(StringComparer.Ordinal).Count() != s.ExpeditionPressureExposures.Length
                || s.ExpeditionPressureChanges.Select(x => x.Id).Distinct(StringComparer.Ordinal).Count() != s.ExpeditionPressureChanges.Length
                || s.ExpeditionPressureCheckpoints.Select(x => x.Id).Distinct(StringComparer.Ordinal).Count() != s.ExpeditionPressureCheckpoints.Length
                || s.ExpeditionPressureCheckpoints.GroupBy(x => x.CohortId + "|" + x.WatchIndex, StringComparer.Ordinal).Any(g => g.Count() > 1)
                || s.ExpeditionPressureExposures.Any(x => x.StartedRevision > s.Revision || x.EndRevision > s.Revision
                    || !s.ExpeditionPressureCohorts.Any(c => c.Id == x.CohortId)
                    || !localRetreat && !s.RouteTravels.Any(t => t.RouteId == x.RouteId && t.TravelerId == s.ExpeditionPressureCohorts.Single(c => c.Id == x.CohortId).Members[0]
                        && t.StartedRevision == x.StartedRevision)
                    || !s.Receipts.Any(r => r.Revision == x.StartedRevision)
                    || x.EndedAt.HasValue && (x.EndedAt.Value > s.RuleClock || x.EndRevision < x.StartedRevision
                        || !s.Receipts.Any(r => r.Revision == x.EndRevision)))
                || s.ExpeditionPressureChanges.Any(x => x.SourceRevision > s.Revision
                    || !s.ExpeditionPressureCohorts.Any(c => c.Id == x.CohortId)
                    || !ValidChangeWatchIndex(x) || !SourceExists(s, x))
                || s.ExpeditionPressureCheckpoints.Any(x => x.AppliedRevision > s.Revision
                    || x.At > s.RuleClock || !s.ExpeditionPressureCohorts.Any(c => c.Id == x.CohortId)
                    || x.CauseIds.Any(id => !s.ExpeditionPressureChanges.Any(c => c.Id == id && c.CohortId == x.CohortId
                        && c.WatchIndex == x.WatchIndex && (c.Kind == ExpeditionPressureChangeKind.OpenCombat
                            || s.SchemaVersion >= Snapshot.ExpeditionCampUseSchema
                                && c.Kind == ExpeditionPressureChangeKind.ExposedCampUse)))
                    || x.ReductionIds.Any(id => !s.ExpeditionPressureChanges.Any(c => c.Id == id && c.CohortId == x.CohortId
                        && c.WatchIndex == x.WatchIndex && (c.Kind == ExpeditionPressureChangeKind.SecuredRouteEntry
                            || s.SchemaVersion >= Snapshot.ExpeditionCampUseSchema
                                && c.Kind == ExpeditionPressureChangeKind.FullWatchLyingLow)))
                    || !s.Receipts.Any(r => r.Revision == x.AppliedRevision && r.Id == x.CommandId)
                    || x.ProfileFingerprint != s.ExpeditionPressureCohorts.Single(c => c.Id == x.CohortId).ProfileFingerprint
                    || x.RouteFingerprint != s.ExpeditionPressureCohorts.Single(c => c.Id == x.CohortId).RouteFingerprint
                    || x.Context != ExpeditionPressureCheckpointContext.Route
                        && s.SchemaVersion < Snapshot.ExpeditionCampUseSchema
                    || x.EffectivePressure != ExpeditionPressureRules.EffectiveForCheckpoint(x.StoredPressure,
                        x.RouteQuality, x.Context)
                    || ExpeditionPressureRules.Classify(x.EffectivePressure, x.Natural, x.ModifiedTotal,
                        x.RollWasModifiedOrRerolled) != x.Outcome
                    || !ValidCheckpointTime(x) || !ValidCheckpointRoll(x)
                    || !localRetreat && !s.RouteTravels.Any(t => t.TravelerId == s.ExpeditionPressureCohorts.Single(c => c.Id == x.CohortId).Members[0]
                        && t.RouteId == x.RouteId && t.StartedRevision <= x.AppliedRevision)))
                throw new ArgumentException("Invalid expedition-pressure references or checkpoints.");

            if (s.SchemaVersion >= Snapshot.ExpeditionCampUseSchema)
                foreach (var checkpoint in s.ExpeditionPressureCheckpoints)
                {
                    bool watchEnd = checkpoint.Reason == ExpeditionPressureSettlementReason.WatchEnd
                        || checkpoint.Reason == ExpeditionPressureSettlementReason.HavenArrivalAtWatchEnd;
                    bool actualCampUse = watchEnd && s.ExpeditionCampActivities.Any(use =>
                        use.CohortId == checkpoint.CohortId && use.Kind == ExpeditionCampActivityKind.Use
                        && use.StartedAt < checkpoint.At
                        && (!use.EndedAt.HasValue || use.EndedAt.Value >= checkpoint.At)
                        && s.ExpeditionCampSites.Any(site => site.Id == use.CampId
                            && site.CohortId == checkpoint.CohortId && site.RouteId == checkpoint.RouteId)
                        && s.ExpeditionPressureExposures.Any(exposure => exposure.Id == use.ExposureId
                            && exposure.CohortId == checkpoint.CohortId && exposure.RouteId == checkpoint.RouteId
                            && exposure.StartedAt < checkpoint.At
                            && (!exposure.EndedAt.HasValue || exposure.EndedAt.Value >= checkpoint.At)));
                    if ((checkpoint.Context == ExpeditionPressureCheckpointContext.Camp) != actualCampUse)
                        throw new ArgumentException("Pressure checkpoint camp context does not match physical camp use.");
                }

            foreach (var c in s.ExpeditionPressureCheckpoints.OrderBy(x => x.WatchIndex))
            {
                var cohort = s.ExpeditionPressureCohorts.Single(x => x.Id == c.CohortId);
                var previous = s.ExpeditionPressureCheckpoints.Where(x => x.CohortId == c.CohortId && x.WatchIndex < c.WatchIndex)
                    .OrderBy(x => x.WatchIndex).LastOrDefault();
                int before = localRetreat
                    ? ExpeditionPressureRules.LocalRetreatPressure(s, cohort, previous, c.AppliedRevision, c.At, includeExitAtBoundary: false)
                    : previous == null ? cohort.InitialPressure : ExpeditionPressureRules.AfterCheckpoint(s, previous, c.AppliedRevision, c.At);
                var available = s.ExpeditionPressureChanges.Where(x => x.CohortId == c.CohortId
                    && x.WatchIndex == c.WatchIndex && x.SourceRevision <= c.AppliedRevision && x.At <= c.At).ToArray();
                var causeRecords = available.Where(x => x.Kind == ExpeditionPressureChangeKind.OpenCombat
                        || s.SchemaVersion >= Snapshot.ExpeditionCampUseSchema
                            && x.Kind == ExpeditionPressureChangeKind.ExposedCampUse)
                    .OrderBy(x => x.SourceRevision).ThenBy(x => x.Id, StringComparer.Ordinal).ToArray();
                var reductionRecords = available.Where(x => x.Kind == ExpeditionPressureChangeKind.SecuredRouteEntry
                        || s.SchemaVersion >= Snapshot.ExpeditionCampUseSchema
                            && x.Kind == ExpeditionPressureChangeKind.FullWatchLyingLow)
                    .OrderBy(x => x.SourceRevision).ThenBy(x => x.Id, StringComparer.Ordinal).Take(2).ToArray();
                var causes = causeRecords.Select(x => x.Id);
                var reductions = reductionRecords.Select(x => x.Id);
                int computed = ExpeditionPressureRules.Settle(before,
                    ExpeditionPressureRules.IncreaseCategoryCount(causeRecords), reductionRecords.Length, c.RiskFloor);
                if (before != c.PressureBefore || computed != c.StoredPressure
                    || !c.CauseIds.SequenceEqual(causes, StringComparer.Ordinal)
                    || !c.ReductionIds.SequenceEqual(reductions, StringComparer.Ordinal))
                    throw new ArgumentException("Expedition-pressure checkpoint does not derive from its source history.");
            }
        }

        private static void ValidateLocalAuthority(Snapshot s)
        {
            var retreat = s.Retreat;
            var d = retreat.Definition;
            var join = s.Reinforcement.Joined;
            if (join == null) {
                if (s.ExpeditionPressureCohorts.Length + s.ExpeditionPressureExposures.Length
                    + s.ExpeditionPressureChanges.Length + s.ExpeditionPressureCheckpoints.Length != 0)
                    throw new ArgumentException("Local Pressure requires actual reinforcement admission.");
                return;
            }
            if (s.ExpeditionPressureCohorts.Length == 0 && retreat.Round == null
                && s.ExpeditionPressureExposures.Length + s.ExpeditionPressureChanges.Length + s.ExpeditionPressureCheckpoints.Length == 0)
                return;
            if (s.ExpeditionPressureCohorts.Length != 1 || s.ExpeditionPressureExposures.Length != 1)
                throw new ArgumentException("Invalid local retreat Pressure authority count.");
            var cohort = s.ExpeditionPressureCohorts[0];
            var exposure = s.ExpeditionPressureExposures[0];
            if (d.RouteAccessId == "" || cohort.Id != d.CohortId || cohort.RouteFingerprint != d.RouteFingerprint
                || cohort.InitialPressure != d.InitialPressure || !cohort.Members.SequenceEqual(new[] { d.LeadId, d.CompanionId })
                || exposure?.Id != d.ExposureId || exposure.CohortId != d.CohortId || exposure.RouteId != d.RouteId
                || exposure.StartedRevision != join.Revision || exposure.StartedAt != join.At || exposure.EndedAt.HasValue
                || s.ExpeditionPressureCheckpoints.Any(x => x.At <= join.At || x.RouteId != d.RouteId
                    || x.RouteQuality != d.Quality || x.RiskFloor != d.Risk || x.Reason != ExpeditionPressureSettlementReason.WatchEnd
                    || x.RouteProgress != default || x.Context != ExpeditionPressureCheckpointContext.Route || x.ReductionIds.Count != 0)
                || s.ExpeditionPressureChanges.Any(x => x.Kind != ExpeditionPressureChangeKind.OpenCombat
                    && x.Kind != ExpeditionPressureChangeKind.SuccessfulRetreat)
                || s.ExpeditionPressureChanges.Count(x => x.Kind == ExpeditionPressureChangeKind.SuccessfulRetreat)
                    != (retreat.SuccessfulExit == null ? 0 : 1))
                throw new ArgumentException("Invalid local retreat Pressure history.");
        }

        private static long EventWatchIndex(RuleTime at)
            => checked((long)(new BigInteger(at.Numerator) / at.Denominator / ExpeditionPressureRules.WatchSeconds));

        private static bool ValidChangeWatchIndex(ExpeditionPressureChangeRecord change)
            => change.Kind == ExpeditionPressureChangeKind.FullWatchLyingLow
                ? SettlementWatchIndex(change.At, true) == change.WatchIndex
                : EventWatchIndex(change.At) == change.WatchIndex;

        private static long SettlementWatchIndex(RuleTime at, bool atWatchEnd)
        {
            BigInteger denominator = new BigInteger(at.Denominator);
            BigInteger watchUnits = denominator * ExpeditionPressureRules.WatchSeconds;
            BigInteger numerator = new BigInteger(at.Numerator);
            bool exact = numerator % watchUnits == 0;
            if (exact != atWatchEnd) return -1;
            BigInteger index = numerator / watchUnits;
            if (atWatchEnd) index -= BigInteger.One;
            return index < BigInteger.Zero || index > long.MaxValue ? -1 : (long)index;
        }

        private static bool ValidCheckpointTime(ExpeditionPressureCheckpointRecord x)
        {
            bool watchEnd = x.Reason == ExpeditionPressureSettlementReason.WatchEnd
                || x.Reason == ExpeditionPressureSettlementReason.HavenArrivalAtWatchEnd;
            if (!Enum.IsDefined(typeof(ExpeditionPressureSettlementReason), x.Reason)) return false;
            if (x.Reason == ExpeditionPressureSettlementReason.WatchEnd && !watchEnd) return false;
            return SettlementWatchIndex(x.At, watchEnd) == x.WatchIndex;
        }

        private static bool ValidCheckpointRoll(ExpeditionPressureCheckpointRecord x)
        {
            if (x.EffectivePressure == 0 || x.EffectivePressure == 6)
                return x.Natural == 0 && x.WordsConsumed == 0 && x.RandomBefore == x.RandomAfter
                    && !x.RollWasModifiedOrRerolled && x.ModifiedTotal == 0;
            return x.Natural >= 1 && x.Natural <= 6 && x.WordsConsumed > 0
                && x.ModifiedTotal == x.Natural && !x.RollWasModifiedOrRerolled;
        }

        private static bool SourceExists(Snapshot s, ExpeditionPressureChangeRecord change)
        {
            var exposure = s.ExpeditionPressureExposures.SingleOrDefault(x => x.Id == change.ExposureId
                && x.CohortId == change.CohortId && x.RouteId == change.RouteId);
            if (exposure == null) return false;
            if (change.Kind == ExpeditionPressureChangeKind.SuccessfulRetreat) {
                var exit = s.Retreat?.SuccessfulExit;
                return exit != null && change.SourceId == exit.CommandId && change.SourceRevision == exit.Revision
                    && change.At == exit.At && change.CohortId == s.Retreat.Definition.CohortId;
            }
            if (change.Kind == ExpeditionPressureChangeKind.ExposedCampUse
                || change.Kind == ExpeditionPressureChangeKind.FullWatchLyingLow)
                return s.SchemaVersion >= Snapshot.ExpeditionCampUseSchema
                    && ExpeditionCampValidation.SourceExists(s, exposure, change);
            if (change.Kind == ExpeditionPressureChangeKind.OpenCombat)
            {
                var melee = s.MeleeAttacks.SingleOrDefault(x => x.Id == change.SourceId);
                if (melee != null) return melee.Revision == change.SourceRevision && melee.At == change.At
                    && ExpeditionPressureRules.AttackWithinExposure(s, exposure, melee.AttackerId, melee.TargetId,
                        melee.Revision, melee.At, melee.Opportunity)
                    && (s.ExpeditionPressureCohorts.Single(c => c.Id == change.CohortId).Members.Contains(melee.AttackerId)
                        || s.ExpeditionPressureCohorts.Single(c => c.Id == change.CohortId).Members.Contains(melee.TargetId));
                var ranged = s.RangedAttacks.SingleOrDefault(x => x.Id == change.SourceId);
                return ranged != null && ranged.Revision == change.SourceRevision && ranged.At == change.At
                    && ExpeditionPressureRules.AttackWithinExposure(s, exposure, ranged.AttackerId, ranged.TargetId,
                        ranged.Revision, ranged.At, false)
                    && (s.ExpeditionPressureCohorts.Single(c => c.Id == change.CohortId).Members.Contains(ranged.AttackerId)
                        || s.ExpeditionPressureCohorts.Single(c => c.Id == change.CohortId).Members.Contains(ranged.TargetId));
            }
            if (change.SourceRevision != exposure.StartedRevision || change.At != exposure.StartedAt) return false;
            var travel = s.RouteTravels.SingleOrDefault(x => x.StartedRevision == change.SourceRevision
                && x.RouteId == change.RouteId
                && x.TravelerId == s.ExpeditionPressureCohorts.Single(c => c.Id == change.CohortId).Members[0]);
            var receipt = s.Receipts.SingleOrDefault(x => x.Revision == change.SourceRevision);
            if (travel == null || receipt == null || change.SourceId != receipt.Id) return false;
            try
            {
                var command = CommandHistory.Read(receipt);
                return command.Kind == CommandKind.StartRouteTravel && command.Actor == travel.TravelerId
                    && command.Target == travel.RouteId;
            }
            catch (ArgumentException) { return false; }
        }

    }
}
