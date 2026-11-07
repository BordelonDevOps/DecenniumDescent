#if DECENNIUM_TEST_ONLY && (UNITY_EDITOR || DEVELOPMENT_BUILD || HEADLESS_TESTS)
using System;
using System.Globalization;
using System.Linq;

namespace Decennium.Foundation.Laboratory
{
    /// <summary>TEST_ONLY nondestructive assay over an explicitly authored mining manifest.
    /// It records knowledge only and never mutates mineral units or inventory.</summary>
    public sealed partial class TestOnlySharedWorldPolicy
    {
        private bool HasMiningAssay => miningFixture != null && miningFixture.AssayProfiles.Length > 0;

        private static void PutMiningAssay(Snapshot s, MiningAssayAttemptRecord value)
            => s.MiningAssayAttempts = s.MiningAssayAttempts.Select(x => x.Id == value.Id ? value : x).ToArray();

        private static RuleTime AddMiningAssayTime(RuleTime a, RuleTime b)
            => RuleTime.FromFraction((System.Numerics.BigInteger)a.Numerator * b.Denominator
                + (System.Numerics.BigInteger)b.Numerator * a.Denominator,
                (System.Numerics.BigInteger)a.Denominator * b.Denominator);
        private static RuleTime SubtractMiningAssayTime(RuleTime a, RuleTime b)
            => RuleTime.FromFraction((System.Numerics.BigInteger)a.Numerator * b.Denominator
                - (System.Numerics.BigInteger)b.Numerator * a.Denominator,
                (System.Numerics.BigInteger)a.Denominator * b.Denominator);

        private bool IsMiningAssayCommand(Command c) => HasMiningAssay && (c.Kind == CommandKind.StartMiningAssay
            || c.Kind == CommandKind.PauseMiningAssay || c.Kind == CommandKind.ResumeMiningAssay
            || c.Kind == CommandKind.CancelMiningAssay);

        private string MiningAssayAccess(Snapshot s, string actorId, MiningAssayProfileRecord profile, string exceptJob = "")
        {
            if (!HasMiningAssay || profile == null) return "MiningAssayNotSelected";
            if (s.InventoryCombat && s.WorldSchedule.Order.Contains(actorId)) return "MiningAssayRequiresExploration";
            if (!IsMiningWorker(actorId) || !CapableWorker(s, actorId) || s.WorldTraversals.Any(x => x.ActorId == actorId))
                return "MiningAssayWorkerUnavailable";
            if (MiningWorkerBusy(s, actorId, exceptJob)) return "WorkerBusy";
            var deposit = s.MiningDeposits.Single(x => x.Id == profile.DepositId);
            var worker = s.Actors.Single(x => x.Id == actorId);
            if (!WorldSpatialQueries.WithinCardinalRange(worker.X, worker.Y, deposit.SiteX, deposit.SiteY, 1))
                return "MiningAssayManifestOutOfReach";
            if (AvailableHands(s, actorId) < profile.RequiredHands) return "MiningAssayHandsUnavailable";
            foreach (string id in profile.RequiredImplementIds) {
                var item = s.PortableEquipment.SingleOrDefault(x => x.Id == id);
                if (item == null || item.OwnerId != deposit.OwnerId || !PortableEquipmentRules.Accessible(s, actorId, item))
                    return "MiningAssayImplementUnavailable";
                if (item.Placement == PortablePlacement.Ground && (item.GroundX != deposit.SiteX || item.GroundY != deposit.SiteY))
                    return "MiningAssayImplementOutOfReach";
            }
            return null;
        }

        private sealed class MiningAssayAssessment
        {
            public MiningAssayProfileRecord Profile;
            public MiningAssayAttemptRecord Current;
            public DestructiveMiningAssayProfileRecord DestructiveProfile;
            public DestructiveMiningAssayAttemptRecord DestructiveCurrent;
            public int WisdomModifier, ProficiencyRank, ProficiencyBonus, CheckDc;
        }

        private static bool MiningAssayResolved(MiningAssayStatus status)
            => status == MiningAssayStatus.Success || status == MiningAssayStatus.CriticalSuccess
                || status == MiningAssayStatus.Failure || status == MiningAssayStatus.CriticalFailure;
        private static bool DestructiveAssayOpen(MiningAssayStatus status)
            => status == MiningAssayStatus.Working || status == MiningAssayStatus.Paused || status == MiningAssayStatus.AwaitingCheck;

        private string DestructiveAssayAccess(Snapshot s, string actorId, DestructiveMiningAssayProfileRecord profile,
            DestructiveMiningAssayAttemptRecord current = null)
        {
            var sample = s.MiningAssaySamples.Single(x => x.Id == profile.SampleId);
            var method = s.MiningAssayProfiles.Single(x => x.Id == profile.MethodProfileId);
            string access = MiningAssayAccess(s, actorId, method, current?.Id ?? "");
            if (access != null) return access;
            if (current != null && current.WorkDone > default(RuleTime)) {
                var committed = s.Work.Reservations.SingleOrDefault(x => x.Id == current.ReservationId);
                return committed != null && committed.ConsumedAmount == profile.SampleAmount
                    && current.EvidenceBasisId == DestructiveMiningAssayValidation.EvidenceBasis(s, sample.InventoryLotId)
                    ? null : "MiningAssayEvidenceInvalidated";
            }
            var provenance = s.InventoryLots.SingleOrDefault(x => x.LotId == sample.InventoryLotId);
            var lot = s.Work.Lots.SingleOrDefault(x => x.Id == sample.InventoryLotId);
            var item = s.PortableEquipment.SingleOrDefault(x => x.Id == sample.Id);
            if (provenance == null || lot == null || item == null || lot.Amount != profile.SampleAmount
                || provenance.CreatedAmount != profile.SampleAmount || item.OwnerId != s.MiningDeposits.Single(x => x.Id == sample.DepositId).OwnerId
                || item.LinkedId != sample.InventoryLotId || !PortableEquipmentRules.Accessible(s, actorId, item))
                return "MiningAssaySampleUnavailable";
            if (item.Placement == PortablePlacement.Ground) {
                var deposit = s.MiningDeposits.Single(x => x.Id == sample.DepositId);
                if (item.GroundX != deposit.SiteX || item.GroundY != deposit.SiteY) return "MiningAssaySampleOutOfReach";
            }
            if (current == null && s.Work.AvailableAmount(sample.InventoryLotId) != profile.SampleAmount)
                return "MiningAssaySampleUnavailable";
            if (current != null) {
                var claim = s.Work.Reservations.SingleOrDefault(x => x.Id == current.ReservationId);
                if (claim == null || claim.RemainingAmount != profile.SampleAmount
                    || claim.ConsumedAmount != default(RuleQuantity)) return "MiningAssaySampleUnavailable";
            }
            return null;
        }

        private string AssessMiningAssayCommand(Snapshot s, Command c, out MiningAssayAssessment facts)
        {
            facts = null;
            if (!HasMiningAssay || s.SchemaVersion < Snapshot.MiningAssaySchema) return "MiningAssayNotSelected";
            if (c.Inventory != null || c.Combat != null || c.Advancement != null || c.Ranged != null
                || c.HarvestSelection != null || c.MiningSelection != null || c.ProspectingExposure != null
                || c.OverwatchRider != OverwatchRider.None || c.SuppressionFire != null || c.DefensiveFormation != null
                || c.ExpeditionAssignment != null || c.X != 0 || c.Y != 0)
                return "InvalidMiningAssayCommand";
            if (PendingCalendarChoice(s)) return "TacticalChoicePending";
            if (c.Kind == CommandKind.StartMiningAssay) {
                var destructiveProfile = s.DestructiveMiningAssayProfiles.SingleOrDefault(x => x.Id == c.Target);
                if (destructiveProfile != null) {
                    var sample = s.MiningAssaySamples.Single(x => x.Id == destructiveProfile.SampleId);
                    var method = s.MiningAssayProfiles.Single(x => x.Id == destructiveProfile.MethodProfileId);
                    string evidence = DestructiveMiningAssayValidation.EvidenceBasis(s, sample.InventoryLotId);
                    if (s.DestructiveMiningAssayAttempts.Any(x => x.EvidenceBasisId == evidence
                        && x.MethodProfileId == method.Id && MiningAssayResolved(x.Status))) return "MiningAssayEvidenceAlreadyAttempted";
                    if (s.DestructiveMiningAssayAttempts.Any(x => x.EvidenceBasisId == evidence
                        && x.MethodProfileId == method.Id && DestructiveAssayOpen(x.Status))) return "MiningAssayEvidenceBusy";
                    if (IsOffCalendarActivity(s, c.Actor) && StartsOrResumesActivityWork(c)) {
                        var activity = ActivityInterval(s, c.Actor);
                        if (activity.Action == WorldActionCommitment.Dash || activity.Action == WorldActionCommitment.ActiveLabor
                            && !CanContinueActivityLabor(s, c.Actor)) return "OffCalendarActionAlreadySpent";
                    }
                    string sampleAccess = DestructiveAssayAccess(s, c.Actor, destructiveProfile);
                    if (sampleAccess != null) return sampleAccess;
                    var destructiveCheck = AbilityCheckRules.Derive(s, c.Actor, "mining-tools", CharacterAbility.Wisdom);
                    facts = new MiningAssayAssessment { Profile = method, DestructiveProfile = destructiveProfile,
                        WisdomModifier = destructiveCheck.AbilityModifier, ProficiencyRank = destructiveCheck.ProficiencyRank,
                        ProficiencyBonus = destructiveCheck.ProficiencyBonus, CheckDc = MiningAssayValidation.Difficulty(s, method) };
                    return null;
                }
                var profile = s.MiningAssayProfiles.SingleOrDefault(x => x.Id == c.Target);
                if (profile == null) return "MiningAssayManifestUnavailable";
                if (s.MiningAssayAttempts.Any(x => x.ProfileId == profile.Id)) return "MiningAssayEvidenceAlreadyAttempted";
                if (s.MiningAssayAttempts.Any(x => x.DepositId == profile.DepositId
                    && (x.Status == MiningAssayStatus.Working || x.Status == MiningAssayStatus.Paused
                        || x.Status == MiningAssayStatus.AwaitingCheck))) return "MiningAssayManifestBusy";
                if (IsOffCalendarActivity(s, c.Actor) && StartsOrResumesActivityWork(c)) {
                    var activity = ActivityInterval(s, c.Actor);
                    if (activity.Action == WorldActionCommitment.Dash || activity.Action == WorldActionCommitment.ActiveLabor
                        && !CanContinueActivityLabor(s, c.Actor)) return "OffCalendarActionAlreadySpent";
                }
                string access = MiningAssayAccess(s, c.Actor, profile);
                if (access != null) return access;
                var check = AbilityCheckRules.Derive(s, c.Actor, "mining-tools", CharacterAbility.Wisdom);
                facts = new MiningAssayAssessment { Profile = profile, WisdomModifier = check.AbilityModifier,
                    ProficiencyRank = check.ProficiencyRank, ProficiencyBonus = check.ProficiencyBonus,
                    CheckDc = MiningAssayValidation.Difficulty(s, profile) };
                return null;
            }

            var destructiveCurrent = s.DestructiveMiningAssayAttempts.SingleOrDefault(x => x.Id == c.Target && x.WorkerId == c.Actor);
            if (destructiveCurrent != null) {
                var profile = s.DestructiveMiningAssayProfiles.Single(x => x.Id == destructiveCurrent.ProfileId);
                if (c.Kind == CommandKind.PauseMiningAssay) {
                    if (destructiveCurrent.Status != MiningAssayStatus.Working) return "MiningAssayNotWorking";
                } else if (c.Kind == CommandKind.CancelMiningAssay) {
                    if (!DestructiveAssayOpen(destructiveCurrent.Status)) return "MiningAssayNotCancellable";
                } else if (c.Kind == CommandKind.ResumeMiningAssay) {
                    if (destructiveCurrent.Status != MiningAssayStatus.Paused
                        && destructiveCurrent.Status != MiningAssayStatus.AwaitingCheck) return "MiningAssayNotPaused";
                    string destructiveResumeAccess = DestructiveAssayAccess(s, c.Actor, profile, destructiveCurrent);
                    if (destructiveResumeAccess != null) return destructiveResumeAccess;
                } else return "InvalidMiningAssayCommand";
                facts = new MiningAssayAssessment { Profile = s.MiningAssayProfiles.Single(x => x.Id == profile.MethodProfileId),
                    DestructiveProfile = profile, DestructiveCurrent = destructiveCurrent };
                return null;
            }

            var current = s.MiningAssayAttempts.SingleOrDefault(x => x.Id == c.Target && x.WorkerId == c.Actor);
            if (current == null) return "UnknownMiningAssayAttempt";
            var currentProfile = s.MiningAssayProfiles.Single(x => x.Id == current.ProfileId);
            if (c.Kind == CommandKind.PauseMiningAssay) {
                if (current.Status != MiningAssayStatus.Working) return "MiningAssayNotWorking";
                facts = new MiningAssayAssessment { Profile = currentProfile, Current = current };
                return null;
            }
            if (c.Kind != CommandKind.ResumeMiningAssay) return "InvalidMiningAssayCommand";
            if (current.Status != MiningAssayStatus.Paused && current.Status != MiningAssayStatus.AwaitingCheck)
                return "MiningAssayNotPaused";
            string resumeAccess = MiningAssayAccess(s, c.Actor, currentProfile, current.Id);
            if (resumeAccess != null) return resumeAccess;
            facts = new MiningAssayAssessment { Profile = currentProfile, Current = current };
            return null;
        }

        private void BookMiningAssay(Snapshot s, MiningAssayAttemptRecord attempt)
        {
            RuleTime remaining = SubtractMiningAssayTime(new RuleTime(MiningAssayValidation.WorkSeconds), attempt.WorkDone);
            RuleTime end = AddMiningAssayTime(s.RuleClock, remaining);
            int index = s.Work.WorkerIntervals.Count(x => x.JobId == attempt.Id);
            string intervalId = attempt.Id + ".labor." + index.ToString(CultureInfo.InvariantCulture);
            s.Work = s.Work.Reserve(attempt.Id, new[] { new WorkerInterval(intervalId, attempt.Id, attempt.WorkerId, s.RuleClock, end) },
                Array.Empty<ResourceReservation>());
        }

        private static void PutDestructiveMiningAssay(Snapshot s, DestructiveMiningAssayAttemptRecord value)
            => s.DestructiveMiningAssayAttempts = s.DestructiveMiningAssayAttempts.Select(x => x.Id == value.Id ? value : x).ToArray();

        private void BookDestructiveMiningAssay(Snapshot s, DestructiveMiningAssayAttemptRecord attempt, bool reserveSample)
        {
            RuleTime remaining = SubtractMiningAssayTime(new RuleTime(MiningAssayValidation.WorkSeconds), attempt.WorkDone);
            RuleTime end = AddMiningAssayTime(s.RuleClock, remaining);
            int index = s.Work.WorkerIntervals.Count(x => x.JobId == attempt.Id);
            string intervalId = attempt.Id + ".labor." + index.ToString(CultureInfo.InvariantCulture);
            var intervals = new[] { new WorkerInterval(intervalId, attempt.Id, attempt.WorkerId, s.RuleClock, end) };
            var claims = reserveSample
                ? new[] { new ResourceReservation(attempt.ReservationId, attempt.Id, attempt.InventoryLotId, attempt.SampleAmount) }
                : Array.Empty<ResourceReservation>();
            s.Work = s.Work.Reserve(attempt.Id, intervals, claims);
        }

        private void PauseIncompatibleMiningAssay(Snapshot s)
        {
            foreach (var attempt in s.MiningAssayAttempts.Where(x => x.Status == MiningAssayStatus.Working).ToArray()) {
                var profile = s.MiningAssayProfiles.Single(x => x.Id == attempt.ProfileId);
                if (MiningAssayAccess(s, attempt.WorkerId, profile, attempt.Id) != null) {
                    s.Work = s.Work.CancelFutureWork(attempt.Id, s.RuleClock);
                    PutMiningAssay(s, attempt.WithWork(s.RuleClock, attempt.WorkDone, MiningAssayStatus.Paused));
                }
            }
            foreach (var attempt in s.DestructiveMiningAssayAttempts.Where(x => x.Status == MiningAssayStatus.Working).ToArray()) {
                var profile = s.DestructiveMiningAssayProfiles.Single(x => x.Id == attempt.ProfileId);
                if (DestructiveAssayAccess(s, attempt.WorkerId, profile, attempt) != null) {
                    s.Work = s.Work.CancelFutureWork(attempt.Id, s.RuleClock);
                    PutDestructiveMiningAssay(s, attempt.WithWork(s.RuleClock, attempt.WorkDone, MiningAssayStatus.Paused));
                }
            }
        }

        private static RuleTime? NextMiningAssayBoundary(Snapshot s)
        {
            var ends = s.MiningAssayAttempts.Where(x => x.Status == MiningAssayStatus.Working)
                .Select(x => s.Work.WorkerIntervals.Single(w => w.JobId == x.Id && w.Start <= s.RuleClock && w.End > s.RuleClock).End)
                .Concat(s.DestructiveMiningAssayAttempts.Where(x => x.Status == MiningAssayStatus.Working)
                    .Select(x => s.Work.WorkerIntervals.Single(w => w.JobId == x.Id && w.Start <= s.RuleClock && w.End > s.RuleClock).End))
                .ToArray();
            return ends.Length == 0 ? (RuleTime?)null : ends.Min();
        }

        private void CreditMiningAssayWork(Snapshot s, RuleTime elapsed)
        {
            foreach (var attempt in s.MiningAssayAttempts.Where(x => x.Status == MiningAssayStatus.Working).ToArray()) {
                if (!s.Work.WorkerIntervals.Any(w => w.JobId == attempt.Id && w.Start <= attempt.UpdatedAt && w.End >= s.RuleClock)) continue;
                RuleTime work = AddMiningAssayTime(attempt.WorkDone, elapsed);
                PutMiningAssay(s, work >= new RuleTime(MiningAssayValidation.WorkSeconds)
                    ? attempt.WithWork(s.RuleClock, new RuleTime(MiningAssayValidation.WorkSeconds), MiningAssayStatus.AwaitingCheck)
                    : attempt.WithWork(s.RuleClock, work, MiningAssayStatus.Working));
            }
            foreach (var attempt in s.DestructiveMiningAssayAttempts.Where(x => x.Status == MiningAssayStatus.Working).ToArray()) {
                if (!s.Work.WorkerIntervals.Any(w => w.JobId == attempt.Id && w.Start <= attempt.UpdatedAt && w.End >= s.RuleClock)) continue;
                if (elapsed > default(RuleTime) && attempt.WorkDone == default(RuleTime))
                    s.Work = s.Work.Consume(attempt.Id, attempt.ReservationId);
                RuleTime work = AddMiningAssayTime(attempt.WorkDone, elapsed);
                PutDestructiveMiningAssay(s, work >= new RuleTime(MiningAssayValidation.WorkSeconds)
                    ? attempt.WithWork(s.RuleClock, new RuleTime(MiningAssayValidation.WorkSeconds), MiningAssayStatus.AwaitingCheck)
                    : attempt.WithWork(s.RuleClock, work, MiningAssayStatus.Working));
            }
        }

        private void ResolveReadyMiningAssays(Snapshot s)
        {
            foreach (var attempt in s.MiningAssayAttempts.Where(x => x.Status == MiningAssayStatus.AwaitingCheck).ToArray()) {
                var profile = s.MiningAssayProfiles.Single(x => x.Id == attempt.ProfileId);
                if (MiningAssayAccess(s, attempt.WorkerId, profile, attempt.Id) == null) FinishMiningAssayCheck(s, attempt, profile);
            }
            foreach (var attempt in s.DestructiveMiningAssayAttempts.Where(x => x.Status == MiningAssayStatus.AwaitingCheck).ToArray()) {
                var profile = s.DestructiveMiningAssayProfiles.Single(x => x.Id == attempt.ProfileId);
                if (DestructiveAssayAccess(s, attempt.WorkerId, profile, attempt) == null)
                    FinishDestructiveMiningAssayCheck(s, attempt, s.MiningAssayProfiles.Single(x => x.Id == profile.MethodProfileId));
            }
        }

        private void FinishDestructiveMiningAssayCheck(Snapshot s, DestructiveMiningAssayAttemptRecord prior,
            MiningAssayProfileRecord method)
        {
            int injury = CharacterStateFacts.ForActor(s, prior.WorkerId, "mining-tools")
                .InjuryPenalty(CharacterAbility.Wisdom, toolCheck: true);
            int modifier = checked(prior.WisdomModifier + prior.ProficiencyBonus + injury);
            int disadvantage = (prior.ProficiencyRank == 0 ? 1 : 0)
                + (TestOnlyClubAttackPolicy.ConditionsFor(s, prior.WorkerId).View().Has(ConditionKind.Poisoned) ? 1 : 0);
            uint before = s.RandomState;
            var roll = PlaytestDice.RollD20(before, disadvantageSources: disadvantage);
            var check = PlaytestRolls.TaskCheck(roll.Natural, modifier, prior.CheckDc);
            s.RandomState = roll.NextRandomState;
            MiningAssayStatus status = check.Degree == TaskDegree.CriticalSuccess ? MiningAssayStatus.CriticalSuccess
                : check.Degree == TaskDegree.Success ? MiningAssayStatus.Success
                : check.Degree == TaskDegree.Failure ? MiningAssayStatus.Failure : MiningAssayStatus.CriticalFailure;
            string[] findings = status == MiningAssayStatus.Success || status == MiningAssayStatus.CriticalSuccess
                ? method.Findings.Select(x => x.Id).OrderBy(x => x, StringComparer.Ordinal).ToArray() : Array.Empty<string>();
            MiningCheckDegree degree = check.Degree == TaskDegree.CriticalSuccess ? MiningCheckDegree.CriticalSuccess
                : check.Degree == TaskDegree.Success ? MiningCheckDegree.Success
                : check.Degree == TaskDegree.Failure ? MiningCheckDegree.Failure : MiningCheckDegree.CriticalFailure;
            PutDestructiveMiningAssay(s, prior.WithResult(s.RuleClock, status, degree,
                roll.Selection == D20Selection.Normal ? MiningDiceSelection.Normal : MiningDiceSelection.Disadvantage,
                roll.First, roll.Second ?? 0, roll.Natural, modifier, before, roll.NextRandomState, roll.WordsConsumed, findings));
        }

        private void FinishMiningAssayCheck(Snapshot s, MiningAssayAttemptRecord prior, MiningAssayProfileRecord profile)
        {
            int injury = CharacterStateFacts.ForActor(s, prior.WorkerId, "mining-tools")
                .InjuryPenalty(CharacterAbility.Wisdom, toolCheck: true);
            int modifier = checked(prior.WisdomModifier + prior.ProficiencyBonus + injury);
            int disadvantage = (prior.ProficiencyRank == 0 ? 1 : 0)
                + (TestOnlyClubAttackPolicy.ConditionsFor(s, prior.WorkerId).View().Has(ConditionKind.Poisoned) ? 1 : 0);
            uint before = s.RandomState;
            var roll = PlaytestDice.RollD20(before, disadvantageSources: disadvantage);
            var check = PlaytestRolls.TaskCheck(roll.Natural, modifier, prior.CheckDc);
            s.RandomState = roll.NextRandomState;
            MiningAssayStatus status = check.Degree == TaskDegree.CriticalSuccess ? MiningAssayStatus.CriticalSuccess
                : check.Degree == TaskDegree.Success ? MiningAssayStatus.Success
                : check.Degree == TaskDegree.Failure ? MiningAssayStatus.Failure : MiningAssayStatus.CriticalFailure;
            string[] findings = status == MiningAssayStatus.Success || status == MiningAssayStatus.CriticalSuccess
                ? profile.Findings.Select(x => x.Id).OrderBy(x => x, StringComparer.Ordinal).ToArray() : Array.Empty<string>();
            MiningCheckDegree degree = check.Degree == TaskDegree.CriticalSuccess ? MiningCheckDegree.CriticalSuccess
                : check.Degree == TaskDegree.Success ? MiningCheckDegree.Success
                : check.Degree == TaskDegree.Failure ? MiningCheckDegree.Failure : MiningCheckDegree.CriticalFailure;
            PutMiningAssay(s, prior.WithResult(s.RuleClock, status, degree,
                roll.Selection == D20Selection.Normal ? MiningDiceSelection.Normal : MiningDiceSelection.Disadvantage,
                roll.First, roll.Second ?? 0, roll.Natural, modifier, before, roll.NextRandomState, roll.WordsConsumed, findings));
        }

        private string ResolveMiningAssay(Snapshot s, Command c)
        {
            bool destructive = c.Kind == CommandKind.StartMiningAssay
                ? s.DestructiveMiningAssayProfiles.Any(x => x.Id == c.Target)
                : s.DestructiveMiningAssayAttempts.Any(x => x.Id == c.Target && x.WorkerId == c.Actor);
            if (destructive) return ResolveDestructiveMiningAssay(s, c);
            string error = AssessMiningAssayCommand(s, c, out var facts);
            if (error != null) return error;
            if (c.Kind == CommandKind.StartMiningAssay) {
                string id = "mining-assay." + (s.Revision + 1).ToString(CultureInfo.InvariantCulture);
                var attempt = new MiningAssayAttemptRecord(id, c.Actor, facts.Profile.Id, facts.Profile.DepositId,
                    facts.Profile.DepositVersionId, s.RuleClock, s.RuleClock, default, MiningAssayStatus.Working,
                    facts.WisdomModifier, facts.ProficiencyRank, facts.ProficiencyBonus, facts.CheckDc, null,
                    MiningCheckDegree.None, MiningDiceSelection.None, 0, 0, 0, 0, 0, 0, 0, Array.Empty<string>());
                BookMiningAssay(s, attempt);
                s.MiningAssayAttempts = s.MiningAssayAttempts.Concat(new[] { attempt }).ToArray();
                return null;
            }
            var current = facts.Current;
            if (c.Kind == CommandKind.PauseMiningAssay) {
                s.Work = s.Work.CancelFutureWork(current.Id, s.RuleClock);
                PutMiningAssay(s, current.WithWork(s.RuleClock, current.WorkDone, MiningAssayStatus.Paused));
                return null;
            }
            if (current.Status == MiningAssayStatus.AwaitingCheck) {
                FinishMiningAssayCheck(s, current, facts.Profile);
                return null;
            }
            BookMiningAssay(s, current);
            PutMiningAssay(s, current.WithWork(s.RuleClock, current.WorkDone, MiningAssayStatus.Working));
            return null;
        }

        private string ResolveDestructiveMiningAssay(Snapshot s, Command c)
        {
            string error = AssessMiningAssayCommand(s, c, out var facts);
            if (error != null) return error;
            if (c.Kind == CommandKind.StartMiningAssay) {
                var profile = facts.DestructiveProfile;
                var sample = s.MiningAssaySamples.Single(x => x.Id == profile.SampleId);
                string id = "mining-assay.destructive." + (s.Revision + 1).ToString(CultureInfo.InvariantCulture);
                string reservation = id + ".sample";
                var attempt = new DestructiveMiningAssayAttemptRecord(id, c.Actor, profile.Id, sample.Id,
                    sample.InventoryLotId, profile.SampleAmount,
                    DestructiveMiningAssayValidation.EvidenceBasis(s, sample.InventoryLotId), profile.MethodProfileId,
                    reservation, s.RuleClock, s.RuleClock, default, MiningAssayStatus.Working, facts.WisdomModifier,
                    facts.ProficiencyRank, facts.ProficiencyBonus, facts.CheckDc, null, MiningCheckDegree.None,
                    MiningDiceSelection.None, 0, 0, 0, 0, 0, 0, 0, Array.Empty<string>());
                BookDestructiveMiningAssay(s, attempt, reserveSample: true);
                s.DestructiveMiningAssayAttempts = s.DestructiveMiningAssayAttempts.Concat(new[] { attempt }).ToArray();
                return null;
            }
            var current = facts.DestructiveCurrent;
            if (c.Kind == CommandKind.PauseMiningAssay) {
                s.Work = s.Work.CancelFutureWork(current.Id, s.RuleClock);
                PutDestructiveMiningAssay(s, current.WithWork(s.RuleClock, current.WorkDone, MiningAssayStatus.Paused));
                return null;
            }
            if (c.Kind == CommandKind.CancelMiningAssay) {
                var claim = s.Work.Reservations.Single(x => x.Id == current.ReservationId);
                if (claim.RemainingAmount > default(RuleQuantity)) s.Work = s.Work.Release(current.Id, current.ReservationId);
                s.Work = s.Work.CancelFutureWork(current.Id, s.RuleClock);
                PutDestructiveMiningAssay(s, current.WithWork(s.RuleClock, current.WorkDone, MiningAssayStatus.Cancelled));
                return null;
            }
            if (current.Status == MiningAssayStatus.AwaitingCheck) {
                FinishDestructiveMiningAssayCheck(s, current, facts.Profile);
                return null;
            }
            BookDestructiveMiningAssay(s, current, reserveSample: false);
            PutDestructiveMiningAssay(s, current.WithWork(s.RuleClock, current.WorkDone, MiningAssayStatus.Working));
            return null;
        }
    }
}
#endif
