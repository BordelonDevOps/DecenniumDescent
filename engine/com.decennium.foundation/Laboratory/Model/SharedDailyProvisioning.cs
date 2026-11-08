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
    /// <summary>Immutable first TEST_ONLY provisioning profile. It enrolls the ordinary hero and
    /// companion from RuleTime zero, with the pinned Small/Medium daily food and water quantities.</summary>
    public sealed class TestOnlyDailyProvisioningProfile
    {
        public const string SourceId = "campaign.unsupported-supply";
        public const string TrackId = "expedition.strain";
        public const int CheckRegistryVersion = 1;
        public const string MapRouteCheckId = "route.mapping.stationary";
        public const string RouteReconnaissanceCheckId = "route.reconnaissance";
        public const string SourceRevision = "46a4d52728ee6956f0bebcb5d2103ffd5bc67ba4";
        public const string ExpeditionBookBlob = "466871fc128dc5f06043a874da2b9c1d94ed80a5";
        public const string StrainPlaytestBlob = "7005aaf9558f0ce4f445ffe982dfa9b6f36c8ee4";
        public const string StrainBindingsBlob = "2be335369152191d3aaf47a558f6c5344b18bb4a";

        private readonly string[] roster;
        public RuleTime CanonicalDayOrigin => default;
        public RuleQuantity FoodRequired => new RuleQuantity(2);
        public RuleQuantity WaterRequired => new RuleQuantity(8);
        public IReadOnlyList<string> Roster => Array.AsReadOnly(roster);

        public TestOnlyDailyProvisioningProfile()
        {
            roster = new[] { TestOnlyPolicy.ActorId, TestOnlyPolicy.CompanionId }
                .OrderBy(x => x, StringComparer.Ordinal).ToArray();
        }

        internal string CanonicalKey => "daily-provisioning-v1|origin=0|food-lb=2|water-pint=8|"
            + "source-revision=" + SourceRevision + "|expedition-book=" + ExpeditionBookBlob
            + "|strain-playtest=" + StrainPlaytestBlob + "|strain-bindings=" + StrainBindingsBlob
            + "|strain-source=" + SourceId + ":" + TrackId + "|check-registry=" + CheckRegistryVersion.ToString(CultureInfo.InvariantCulture)
            + ":" + MapRouteCheckId + "," + RouteReconnaissanceCheckId
            + "|roster=" + string.Join(";", roster);

        internal bool Registers(string checkId) => checkId == MapRouteCheckId || checkId == RouteReconnaissanceCheckId;

        internal string ValidateBindings(Snapshot s)
            => roster.All(actor => s.Actors.Any(x => x.Id == actor) && s.Lives.Any(x => x.ActorId == actor))
                ? null : "DailyProvisioningRosterActorMissing";

        internal static string BindFingerprint(string prior, TestOnlyDailyProvisioningProfile profile)
        {
            using (var sha = SHA256.Create())
                return "TEST_ONLY.provision-v1-" + string.Concat(sha.ComputeHash(Encoding.UTF8.GetBytes(prior + "|" + profile.CanonicalKey))
                    .Select(b => b.ToString("x2", CultureInfo.InvariantCulture)));
        }
    }

    public readonly struct ExpeditionStrainEffectProjection
    {
        public int Level { get; }
        public int InitiativeModifier => Level >= 1 ? -1 : 0;
        public int ExpeditionCheckModifier => Level >= 1 ? -1 : 0;
        public bool ExpeditionCheckDisadvantage => Level >= 3;
        public int AttackModifier => Level >= 2 ? -1 : 0;
        public int SavingThrowModifier => Level >= 2 ? -1 : 0;
        public long FlatSpeedModifier => Level >= 2 ? -10 : 0;
        public bool DashProhibited => Level >= 5;
        public bool Incapacitated => Level >= 5;
        public bool TacticalVoluntaryMovementAllowed => Level < 5;
        public bool SlowTravel => Level >= 5;
        internal ExpeditionStrainEffectProjection(int level) { Level = level; }
        public long EffectiveMaximumHp(long baseMaximumHp)
            => PlaytestMaximumHp.SystemicMaximum(baseMaximumHp, expedition: Level);
    }

    /// <summary>Pure TEST_ONLY projection of the retained provisional Expedition Strain overlay.
    /// It is source-qualified by the daily profile and never merges serum Strain or Core Exhaustion.</summary>
    public static class ExpeditionStrainRules
    {
        public static ExpeditionStrainEffectProjection Project(Snapshot s, string actorId,
            RuleTime at, long revision)
        {
            if (s == null || !Validation.ValidId(actorId) || revision < 0)
                throw new ArgumentException("Invalid Expedition Strain projection request.");
            if (s.SchemaVersion < Snapshot.DailyProvisioningSchema)
                return new ExpeditionStrainEffectProjection(0);
            int level = s.ExpeditionStrainGains.Where(x => x.ActorId == actorId && x.Revision <= revision && x.At <= at)
                .Sum(x => x.AddedAmount);
            if (level < 0 || level > 6) throw new InvalidOperationException("Invalid Expedition Strain point total.");
            return new ExpeditionStrainEffectProjection(level);
        }

        public static ExpeditionStrainEffectProjection Current(Snapshot s, string actorId)
            // Command-policy resolution operates on a detached candidate whose revision is still
            // the committed revision. Boundary effects written by that candidate are stamped for
            // the revision that Simulation will commit after policy resolution.
            => Project(s, actorId, s.RuleClock, checked(s.Revision + 1));

        public static long EffectiveMaximumHp(Snapshot s, string actorId, RuleTime at, long revision)
        {
            var life = s.Lives.Single(x => x.ActorId == actorId);
            return Project(s, actorId, at, revision).EffectiveMaximumHp(life.MaximumHp);
        }

        public static bool DashLocked(Snapshot s, string actorId)
        {
            var projection = Current(s, actorId);
            var value = s.ExpeditionDashLocks.SingleOrDefault(x => x.ActorId == actorId);
            return projection.Level >= 3 && value != null && s.RuleClock < value.Deadline;
        }

        internal static ConditionPermissions RestrictPermissions(Snapshot s, string actorId, ConditionPermissions prior)
        {
            if (!Current(s, actorId).Incapacitated) return prior;
            return new ConditionPermissions(false, false, false,
                s.InventoryCombat ? false : prior.VoluntarySpeed, false, false, prior.MustChooseActionOrMovement);
        }

        internal static void RecordDash(Snapshot s, string actorId, long revision)
        {
            var value = CreateDashLock(s, actorId, revision);
            if (value == null) return;
            s.ExpeditionDashLocks = s.ExpeditionDashLocks.Where(x => x.ActorId != actorId)
                .Concat(new[] { value }).ToArray();
        }

        internal static void ClampLife(Snapshot s, string actorId, RuleTime at, long revision)
        {
            var before = s.Lives.Single(x => x.ActorId == actorId);
            long maximum = Project(s, actorId, at, revision).EffectiveMaximumHp(before.MaximumHp);
            if (before.Hp <= maximum) return;
            var after = new ActorLifeRecord(before.ActorId, before.MaximumHp, maximum, before.TemporaryHp,
                before.LinkedInjuries, before.Stable, before.Dead, before.UsesDeathSaves,
                before.DeathSuccesses, before.DeathFailures, before.StableUntil, before.LastDeathTurn,
                before.Prone, before.HeldItems);
            s.Lives = s.Lives.Select(x => x.ActorId == actorId ? after : x).ToArray();
        }

        internal static RuleTime InitiativeMarkerPhase(FixedEncounterRecord encounter, string actor)
        {
            int index = encounter == null ? -1 : Array.IndexOf(encounter.Order.ToArray(), actor);
            if (index < 0) throw new ArgumentException("Actor has no initiative marker.");
            return RuleTime.FromFraction((BigInteger)encounter.Origin.Numerator * encounter.Order.Count
                    + (BigInteger)6 * (index + 1) * encounter.Origin.Denominator,
                (BigInteger)encounter.Origin.Denominator * encounter.Order.Count);
        }

        internal static ExpeditionDashLockRecord CreateDashLock(Snapshot s, string actor, long revision)
        {
            var projection = Current(s, actor);
            if (projection.Level < 3) return null;
            if (projection.DashProhibited) throw new InvalidOperationException("ExpeditionStrainPreventsDash");
            var encounter = s.Encounter;
            // Retained encounter history is not active tactical control. Off-calendar actors also
            // have no initiative marker, even while a tactical encounter is active.
            if (!s.InventoryCombat || encounter == null || !encounter.Order.Contains(actor))
                return new ExpeditionDashLockRecord(actor, revision, s.RuleClock, CampGreens.Add(s.RuleClock, new RuleTime(6)));

            RuleTime phase = InitiativeMarkerPhase(encounter, actor);
            BigInteger differenceNumerator = (BigInteger)s.RuleClock.Numerator * phase.Denominator
                - (BigInteger)phase.Numerator * s.RuleClock.Denominator;
            BigInteger commonDenominator = (BigInteger)s.RuleClock.Denominator * phase.Denominator;
            BigInteger cycle = FloorDivide(differenceNumerator, commonDenominator * 6) + 1;
            RuleTime first = RuleTime.FromFraction((BigInteger)phase.Numerator * commonDenominator
                    + cycle * 6 * commonDenominator * phase.Denominator,
                (BigInteger)phase.Denominator * commonDenominator);
            if (encounter.CurrentActor == actor)
            {
                RuleTime currentEnd = FixedEncounterRules.Start(encounter, checked(encounter.TurnOrdinal + 1));
                if (first == currentEnd) first = CampGreens.Add(first, new RuleTime(6));
            }
            return new ExpeditionDashLockRecord(actor, revision, s.RuleClock, first, encounter.Id, phase);
        }

        private static BigInteger FloorDivide(BigInteger numerator, BigInteger denominator)
        {
            BigInteger quotient = BigInteger.DivRem(numerator, denominator, out BigInteger remainder);
            return numerator < 0 && remainder != 0 ? quotient - 1 : quotient;
        }
    }

    public sealed partial class TestOnlySharedWorldPolicy
    {
        private TestOnlyDailyProvisioningProfile dailyProvisioning;

        /// <summary>Opts this finite TEST_ONLY host into fixed-roster canonical daily provisioning
        /// and the versioned Map Route/recon Expedition-check registry.</summary>
        public TestOnlySharedWorldPolicy EnableDailyProvisioning(TestOnlyDailyProvisioningProfile profile = null)
        {
            if (initializationStarted) throw new InvalidOperationException("World initialization has already started.");
            if (dailyProvisioning != null) throw new ArgumentException("Daily provisioning is already selected.");
            dailyProvisioning = profile ?? new TestOnlyDailyProvisioningProfile();
            ContentFingerprint = TestOnlyDailyProvisioningProfile.BindFingerprint(ContentFingerprint, dailyProvisioning);
            return this;
        }

        private void InitializeDailyProvisioning(Snapshot s)
        {
            if (dailyProvisioning == null) return;
            string error = dailyProvisioning.ValidateBindings(s);
            if (error != null) throw new InvalidOperationException(error);
            if (s.SchemaVersion != Snapshot.DailyProvisioningSchema || s.RuleClock != dailyProvisioning.CanonicalDayOrigin)
                throw new InvalidOperationException("DailyProvisioningRequiresCanonicalInitialProfile");
            s.DailyProvisioningSettlements = Array.Empty<DailyProvisioningSettlementRecord>();
            s.DailyProvisioningConsumption = Array.Empty<DailyProvisioningConsumptionRecord>();
            s.ExpeditionStrainGains = Array.Empty<ExpeditionStrainGainRecord>();
            s.ExpeditionDashLocks = Array.Empty<ExpeditionDashLockRecord>();
        }

        private string ValidateDailyProvisioningState(Snapshot s)
        {
            if (dailyProvisioning == null)
                return s.SchemaVersion != Snapshot.DailyProvisioningSchema && s.DailyProvisioningSettlements.Length == 0
                    && s.DailyProvisioningConsumption.Length == 0 && s.ExpeditionStrainGains.Length == 0
                    && s.ExpeditionDashLocks.Length == 0 ? null : "DailyProvisioningProfileMissing";
            if (s.SchemaVersion != Snapshot.DailyProvisioningSchema || !s.TestOnly
                || s.ContentFingerprint != ContentFingerprint || dailyProvisioning.ValidateBindings(s) != null)
                return "DailyProvisioningProfileMismatch";
            return ValidateDailyProvisioningHistory(s);
        }

        private string ValidateDailyProvisioningHistory(Snapshot s)
        {
            BigInteger dueDays = BigInteger.Divide(s.RuleClock.Numerator,
                (BigInteger)s.RuleClock.Denominator * 86400);
            if (dueDays > ExpeditionProvisioningValidation.MaxSettlements / dailyProvisioning.Roster.Count
                || dueDays * dailyProvisioning.Roster.Count != s.DailyProvisioningSettlements.Length)
                return "DailyProvisioningSettlementCoverageMismatch";
            for (long day = 0; day < (long)dueDays; day++)
            {
                RuleTime start = ProvisioningBoundary(day);
                RuleTime end = ProvisioningBoundary(checked(day + 1));
                foreach (string actor in dailyProvisioning.Roster)
                {
                    string id = ProvisioningSettlementId(day, actor);
                    var settlement = s.DailyProvisioningSettlements.SingleOrDefault(x => x.Id == id);
                    if (settlement == null || settlement.DayOrdinal != day || settlement.ActorId != actor
                        || settlement.Start != start || settlement.End != end
                        || settlement.FoodRequired != dailyProvisioning.FoodRequired
                        || settlement.WaterRequired != dailyProvisioning.WaterRequired)
                        return "DailyProvisioningSettlementProfileMismatch";
                    var earlierIds = new HashSet<string>(s.DailyProvisioningSettlements.Where(x => x.DayOrdinal < day)
                        .Select(x => x.Id), StringComparer.Ordinal);
                    var priorEvidence = s.DailyProvisioningConsumption.Where(x => earlierIds.Contains(x.SettlementId)).ToArray();
                    var expected = DailyConsumption(s, id, actor, start, end, priorEvidence)
                        .OrderBy(x => x.IntakeId, StringComparer.Ordinal).ToArray();
                    var actual = s.DailyProvisioningConsumption.Where(x => x.SettlementId == id)
                        .OrderBy(x => x.IntakeId, StringComparer.Ordinal).ToArray();
                    if (expected.Length != actual.Length || expected.Where((x, i) => x.SettlementId != actual[i].SettlementId
                        || x.IntakeId != actual[i].IntakeId || x.ActorId != actual[i].ActorId || x.LotId != actual[i].LotId
                        || x.ReservationId != actual[i].ReservationId || x.Nutrition != actual[i].Nutrition || x.Amount != actual[i].Amount).Any())
                        return "DailyProvisioningAttributionMismatch";
                    if (settlement.HasShortfall != (settlement.StrainGainId != ""))
                        return "DailyProvisioningStrainOutcomeMismatch";
                }
            }

            foreach (var gain in s.ExpeditionStrainGains)
            {
                var settlement = s.DailyProvisioningSettlements.SingleOrDefault(x => x.Id == gain.SettlementId);
                if (settlement == null || settlement.StrainGainId != gain.Id || gain.SourceId != TestOnlyDailyProvisioningProfile.SourceId
                    || gain.TrackId != TestOnlyDailyProvisioningProfile.TrackId || gain.AttemptedAmount != 1
                    || gain.OrdinaryRemovable != true || gain.RemovalGateMet != false)
                    return "DailyProvisioningStrainBindingMismatch";
                // Several crossed day boundaries can settle in one accepted clock command, so
                // earlier same-command gains have the same revision as this record. Historical
                // Strain is ordered by its canonical elapsed-time endpoint, not command revision.
                int priorLevel = s.ExpeditionStrainGains.Where(x => x.ActorId == gain.ActorId
                    && (x.At < gain.At || x.At == gain.At && x.Revision < gain.Revision))
                    .Sum(x => x.AddedAmount);
                int added = Math.Min(1, 6 - priorLevel);
                var expectedEndpoint = priorLevel >= 5 ? ExpeditionStrainEndpoint.OrdinaryDeath : ExpeditionStrainEndpoint.None;
                if (gain.LevelBefore != priorLevel || gain.AddedAmount != added || gain.Endpoint != expectedEndpoint)
                    return "DailyProvisioningStrainHistoryMismatch";
            }
            foreach (var life in s.Lives.Where(x => dailyProvisioning.Roster.Contains(x.ActorId)))
            {
                var projection = ExpeditionStrainRules.Current(s, life.ActorId);
                if (projection.Level == 6 && !life.Dead) return "LivingActorAtOrdinaryExpeditionStrainEndpoint";
                long effectiveMaximum = projection.EffectiveMaximumHp(life.MaximumHp);
                if (life.Hp > effectiveMaximum) return "ExpeditionStrainMaximumHpNotApplied";
            }
            return null;
        }

        private static RuleTime ProvisioningBoundary(long day)
            => RuleTime.FromFraction((BigInteger)day * 86400, BigInteger.One);

        private static string ProvisioningSettlementId(long day, string actor)
            => "provisioning.day." + day.ToString(CultureInfo.InvariantCulture) + "." + actor;

        private RuleTime? NextProvisioningBoundary(Snapshot s)
        {
            if (dailyProvisioning == null) return null;
            if (s.DailyProvisioningSettlements.Length % dailyProvisioning.Roster.Count != 0)
                throw new InvalidOperationException("PartialDailyProvisioningDay");
            long day = s.DailyProvisioningSettlements.Length / dailyProvisioning.Roster.Count;
            if (day >= ExpeditionProvisioningValidation.MaxSettlements / dailyProvisioning.Roster.Count) return null;
            return ProvisioningBoundary(checked(day + 1));
        }

        private static IEnumerable<DailyProvisioningConsumptionRecord> DailyConsumption(Snapshot s, string settlementId,
            string actor, RuleTime start, RuleTime end, IEnumerable<DailyProvisioningConsumptionRecord> priorEvidence)
        {
            var existing = priorEvidence.ToArray();
            var values = new List<DailyProvisioningConsumptionRecord>();
            foreach (var intake in s.Intakes.Where(x => x.ActorId == actor).OrderBy(x => x.StartedAt).ThenBy(x => x.Id, StringComparer.Ordinal))
            {
                var lot = s.InventoryLots.Single(x => x.LotId == intake.LotId);
                if (lot.Nutrition != NutritionKind.FoodPounds && lot.Nutrition != NutritionKind.WaterPints) continue;
                var reservation = s.Work.Reservations.Single(x => x.Id == intake.ReservationId);
                RuleTime overlapStart = intake.StartedAt > start ? intake.StartedAt : start;
                RuleTime intakeEnd = intake.EndedAt ?? end;
                RuleTime overlapEnd = intakeEnd < end ? intakeEnd : end;
                if (lot.FreshUntil.HasValue && lot.FreshUntil.Value < overlapEnd) overlapEnd = lot.FreshUntil.Value;
                if (overlapEnd <= overlapStart) continue;
                long rate = OrdinaryInventory.SecondsPerUnit(lot.Nutrition);
                RuleQuantity intervalAmount = OrdinaryInventory.Quantity(CampGreens.Subtract(overlapEnd, overlapStart), rate);
                RuleQuantity prior = RuleQuantity.Sum(existing.Where(x => x.IntakeId == intake.Id)
                    .Select(x => x.Amount));
                if (reservation.ConsumedAmount < prior) throw new InvalidOperationException("DailyProvisioningEvidenceExceedsActualConsumption");
                RuleQuantity unaccounted = reservation.ConsumedAmount - prior;
                RuleQuantity amount = intervalAmount < unaccounted ? intervalAmount : unaccounted;
                if (amount > default(RuleQuantity))
                    values.Add(new DailyProvisioningConsumptionRecord(settlementId, intake.Id, actor, intake.LotId,
                        intake.ReservationId, lot.Nutrition, amount));
            }
            return values;
        }

        private string SettleDueProvisioning(Snapshot s)
        {
            if (dailyProvisioning == null) return null;
            if (s.DailyProvisioningSettlements.Length % dailyProvisioning.Roster.Count != 0)
                return "PartialDailyProvisioningDay";
            long day = s.DailyProvisioningSettlements.Length / dailyProvisioning.Roster.Count;
            RuleTime end = ProvisioningBoundary(checked(day + 1));
            while (end <= s.RuleClock)
            {
                if (s.DailyProvisioningSettlements.Length + dailyProvisioning.Roster.Count > ExpeditionProvisioningValidation.MaxSettlements)
                    return "DailyProvisioningHistoryCapacityReached";
                RuleTime start = ProvisioningBoundary(day);
                foreach (string actor in dailyProvisioning.Roster)
                {
                    string id = ProvisioningSettlementId(day, actor);
                    if (s.DailyProvisioningSettlements.Any(x => x.Id == id)) return "DailyProvisioningSettlementAlreadyExists";
                    var contributions = DailyConsumption(s, id, actor, start, end, s.DailyProvisioningConsumption).ToArray();
                    RuleQuantity food = RuleQuantity.Sum(contributions.Where(x => x.Nutrition == NutritionKind.FoodPounds).Select(x => x.Amount));
                    RuleQuantity water = RuleQuantity.Sum(contributions.Where(x => x.Nutrition == NutritionKind.WaterPints).Select(x => x.Amount));
                    bool living = !s.Lives.Single(x => x.ActorId == actor).Dead;
                    string gainId = "";
                    if (food < dailyProvisioning.FoodRequired || water < dailyProvisioning.WaterRequired)
                    {
                        if (s.ExpeditionStrainGains.Length >= ExpeditionProvisioningValidation.MaxStrainGains)
                            return "ExpeditionStrainHistoryCapacityReached";
                        gainId = id + ".gain";
                        int level = ExpeditionStrainRules.Project(s, actor, end, s.Revision + 1).Level;
                        int added = Math.Min(1, 6 - level);
                        var endpoint = level >= 5 ? ExpeditionStrainEndpoint.OrdinaryDeath : ExpeditionStrainEndpoint.None;
                        var gain = new ExpeditionStrainGainRecord(gainId, added > 0 ? gainId + ".point" : "", id,
                            actor, TestOnlyDailyProvisioningProfile.SourceId, TestOnlyDailyProvisioningProfile.TrackId,
                            end, s.Revision + 1, level, 1, added, true, false, endpoint);
                        s.ExpeditionStrainGains = s.ExpeditionStrainGains.Concat(new[] { gain }).ToArray();
                        if (endpoint == ExpeditionStrainEndpoint.OrdinaryDeath && living)
                        {
                            var before = s.Lives.Single(x => x.ActorId == actor);
                            var priorLife = ActorLifeRules.Read(before);
                            var after = new LifeState(priorLife.MaximumHp, 0, priorLife.TemporaryHp, priorLife.Wounds,
                                stable: false, dead: true, deathSuccesses: before.DeathSuccesses,
                                deathFailures: before.DeathFailures, usesDeathSaves: before.UsesDeathSaves,
                                lastDeathTurn: before.LastDeathTurn);
                            TestOnlyClubAttackPolicy.ApplyLife(s, before, after);
                        }
                    }
                    var settlement = new DailyProvisioningSettlementRecord(id, actor, day, start, end,
                        dailyProvisioning.FoodRequired, dailyProvisioning.WaterRequired, food, water,
                        living, gainId, s.Revision + 1);
                    s.DailyProvisioningSettlements = s.DailyProvisioningSettlements.Concat(new[] { settlement }).ToArray();
                    s.DailyProvisioningConsumption = s.DailyProvisioningConsumption.Concat(contributions).ToArray();
                    ExpeditionStrainRules.ClampLife(s, actor, end, s.Revision + 1);
                }
                day = checked(day + 1);
                end = ProvisioningBoundary(checked(day + 1));
            }
            return null;
        }
    }
}
#endif
