#if DECENNIUM_TEST_ONLY && (UNITY_EDITOR || DEVELOPMENT_BUILD || HEADLESS_TESTS)
using System;
using System.Collections.Generic;
using System.Globalization;
using System.Linq;
using System.Security.Cryptography;
using System.Text;

namespace Decennium.Foundation.Laboratory
{
    /// <summary>One authored FL-19/21/22 self-funded episode. The scope attests the complete sale,
    /// tax and mandatory rescue/quarantine inputs through the cutoff, with no conflicting superior claim.
    /// Other costs, all-party liabilities and allocation after reserves are outside the represented register.</summary>
    public sealed class TestOnlyExpeditionBillProfile
    {
        public const string EpisodeId = "TEST_ONLY.haven-iron-episode";
        public const string CharterVersionId = "TEST_ONLY.haven-self-charter.v1";
        public const string BillVersionId = "TEST_ONLY.haven-iron-episode-bill.v1";
        public const string WorkerId = TestOnlyHavenMealProfile.CustomerId;
        public const string DeskId = TestOnlyHavenAppraisalProfile.DeskId;
        public const string ResponsibilityTermsId = "TEST_ONLY.haven-self-net-own-capital-terms.v1";
        public const string ScopeId = "TEST_ONLY.haven-iron-episode-covered-register.v1";
        public const string LedgerAuthorityId = "TEST_ONLY.haven-ledger-claimant-delegation.v1";
        public ExpeditionBillCharter Charter { get; }
        public bool RepresentativeAuthorized { get; }
        public bool RecordsAccessible { get; }
        public bool WritingFacilitiesAvailable { get; }

        public TestOnlyExpeditionBillProfile(ExpeditionBillCoverage coverage = ExpeditionBillCoverage.Required,
            bool representativeAuthorized = true, bool recordsAccessible = true, bool writingFacilitiesAvailable = true,
            int validFrom = 0, int authorizationUntil = 10800, int dueAt = 14400)
        {
            // The owning member supplies use of the existing pack under these terms and retains its title.
            // The claimant delegation includes reading the selected Quartermaster records and doing self-service ledger work.
            // This scenario's prospective goals are deliberately distinct from the source-defined computations.
            Charter = new ExpeditionBillCharter(EpisodeId, CharterVersionId, BillVersionId, WorkerId,
                new[] { TestOnlyPolicy.ActorId, TestOnlyPolicy.CompanionId }, TestOnlyPolicy.ActorId, PortableKitFixture.Pack,
                ResponsibilityTermsId, ScopeId, LedgerAuthorityId, DeskId, coverage, default, new RuleTime(dueAt),
                new RuleTime(validFrom), new RuleTime(authorizationUntil), new RuleQuantity(2), new RuleQuantity(3), new RuleQuantity(1));
            RepresentativeAuthorized = representativeAuthorized;
            RecordsAccessible = recordsAccessible;
            WritingFacilitiesAvailable = writingFacilitiesAvailable;
        }

        internal string Key => string.Join("|", "FL19-FL21-FL22-46a4d52728ee6956f0bebcb5d2103ffd5bc67ba4",
            Charter.BindingKey, "Self-net-0-own-capital-no-grant-loan-or-contribution", "representative-records-claims-and-bill",
            "one-slot-read-and-write-2,3", "gross-net-realized-profit-unresolved", RepresentativeAuthorized,
            RecordsAccessible, WritingFacilitiesAvailable);
    }

    public sealed partial class TestOnlySharedWorldPolicy
    {
        private TestOnlyExpeditionBillProfile expeditionBillProfile;

        public TestOnlySharedWorldPolicy EnableExpeditionBill(TestOnlyExpeditionBillProfile profile)
        {
            if (profile == null) throw new ArgumentNullException(nameof(profile));
            if (initializationStarted || expeditionBillProfile != null || SelectedSchema != Snapshot.HavenMealSchema)
                throw new InvalidOperationException("Select one Expedition bill on the funded Haven meal host before initialization.");
            expeditionBillProfile = profile;
            using (var sha = SHA256.Create())
                ContentFingerprint = "TEST_ONLY.expedition-bill-v1-" + string.Concat(sha.ComputeHash(
                    Encoding.UTF8.GetBytes(ContentFingerprint + "|" + profile.Key)).Select(x => x.ToString("x2", CultureInfo.InvariantCulture)));
            return this;
        }

        private void InitializeExpeditionBill(Snapshot state)
        {
            if (expeditionBillProfile == null) return;
            var charter = expeditionBillProfile.Charter;
            if (!state.PortableEquipment.Any(x => x.Id == charter.CapitalId && x.OwnerId == charter.CapitalOwnerId))
                throw new InvalidOperationException("The self-funded charter lacks its starting member-owned capital.");
            state.ExpeditionBillCharter = charter;
        }

        private static bool IsExpeditionBillCommand(CommandKind kind)
            => kind == CommandKind.StartExpeditionBill || kind == CommandKind.PauseExpeditionBill
                || kind == CommandKind.ResumeExpeditionBill || kind == CommandKind.FinalizeExpeditionBill || kind == CommandKind.CancelExpeditionBill;

        private static ExpeditionBillRecord OpenExpeditionBill(Snapshot state) => state.ExpeditionBills.SingleOrDefault(x => x.Open);

        private IEnumerable<Command> DiscoverExpeditionBillCommands(Snapshot state, string actor)
        {
            if (expeditionBillProfile == null || actor != TestOnlyExpeditionBillProfile.WorkerId) yield break;
            Command Option(CommandKind kind, string target) => new Command("option."
                + state.Revision.ToString(CultureInfo.InvariantCulture) + ".expedition-bill." + kind, actor, state.Revision, kind, target);
            var job = OpenExpeditionBill(state);
            if (job == null) {
                if (state.HavenMealPurchases.Length == 1 && state.ExpeditionBills.All(x => x.Report == null))
                    yield return Option(CommandKind.StartExpeditionBill, TestOnlyExpeditionBillProfile.BillVersionId);
                yield break;
            }
            yield return Option(CommandKind.CancelExpeditionBill, job.Id);
            switch (job.Status) {
                case ExpeditionBillStatus.Working: yield return Option(CommandKind.PauseExpeditionBill, job.Id); break;
                case ExpeditionBillStatus.Paused: yield return Option(CommandKind.ResumeExpeditionBill, job.Id); break;
                case ExpeditionBillStatus.PendingCompletion: yield return Option(CommandKind.FinalizeExpeditionBill, job.Id); break;
            }
        }

        private string ExpeditionBillAuthorityFailure(Snapshot state)
        {
            if (state.ExpeditionBillCharter?.BindingKey != expeditionBillProfile.Charter.BindingKey
                || !expeditionBillProfile.RepresentativeAuthorized) return "ExpeditionBillRepresentativeUnauthorized";
            if (!expeditionBillProfile.RecordsAccessible) return "ExpeditionBillRecordsUnavailable";
            if (!state.ExpeditionBillCharter.Coverage.HasFlag(ExpeditionBillCoverage.NoConflictingSuperiorClaim))
                return "ExpeditionBillSuperiorClaimUncleared";
            if (state.ExpeditionBillCharter.Coverage != ExpeditionBillCoverage.Required)
                return "ExpeditionBillScopeIncomplete";
            return null;
        }

        private string ExpeditionBillInputs(Snapshot state, ExpeditionBillBasis previous, out ExpeditionBillBasis basis)
        {
            basis = previous;
            string authorityFailure = ExpeditionBillAuthorityFailure(state);
            if (authorityFailure != null) return authorityFailure;
            var sale = state.HavenSales.SingleOrDefault(x => x.Status == HavenSaleStatus.Paid);
            var meal = state.HavenMealPurchases.SingleOrDefault();
            if (sale == null || meal == null) return "ExpeditionBillPaidRecordsMissing";
            if (sale.Basis.OfferVersionId != TestOnlyHavenSaleProfile.OfferVersionId || !havenSaleProfile.WrittenExemption
                || !havenSaleProfile.DispositionCleared || sale.Basis.ClearanceId != TestOnlyHavenSaleProfile.ClearanceId
                || sale.Basis.ExemptionId != TestOnlyHavenSaleProfile.ExemptionId || sale.Basis.ExemptionIssuerId != TestOnlyHavenSaleProfile.IssuerId
                || sale.Basis.JurisdictionId != TestOnlyHavenSaleProfile.JurisdictionId
                || sale.Basis.TenderLotId != TestOnlyHavenSaleProfile.TenderLotId
                || sale.Basis.ExactQuoteCopper != TestOnlyHavenSaleProfile.QuoteCopper
                || sale.PaymentCopper != TestOnlyHavenSaleProfile.PaymentCopper
                || meal.Offer.ExactQuoteCopper != havenMealProfile.Offer.ExactQuoteCopper || meal.PaymentCopper != sale.PaymentCopper
                || meal.Offer.VersionId != TestOnlyHavenMealProfile.OfferVersionId
                || meal.Offer.SpendingClearanceId != TestOnlyHavenMealProfile.SpendingClearanceId)
                return "ExpeditionBillDispositionAuthorityMismatch";
            var appraisal = state.HavenAppraisals.SingleOrDefault(x => x.Id == sale.Basis.AppraisalId);
            if (appraisal?.Status != HavenAppraisalStatus.Completed || appraisal.Basis.ClearanceId != TestOnlyHavenAppraisalProfile.ClearanceId
                || appraisal.Basis.EvidenceId != TestOnlyHavenAppraisalProfile.EvidenceId)
                return "ExpeditionBillAppraisalEvidenceMismatch";
            var charter = state.ExpeditionBillCharter;
            basis ??= new ExpeditionBillBasis(charter.VersionId, charter.BillVersionId, sale.Id, sale.UpdatedRevision,
                meal.Id, meal.Revision, appraisal.Id, sale.Basis.ClearanceId, sale.Basis.ExemptionId, meal.Offer.SpendingClearanceId,
                sale.Basis.TenderLotId, state.Revision, state.RuleClock, sale.PaymentCopper.Value, meal.PaymentCopper);
            return basis.MatchesReceipts(state, charter) ? null : "ExpeditionBillPaidRecordsChanged";
        }

        private string ExpeditionBillWorkerFailure(Snapshot state, string worker)
        {
            var desk = state.Structures.SingleOrDefault(x => x.Id == TestOnlyExpeditionBillProfile.DeskId);
            if (desk == null || desk.ProfileId != AppraisalDeskStructure || desk.LocationId != AppraisalGround || desk.Broken
                || !expeditionBillProfile.WritingFacilitiesAvailable) return "ExpeditionBillDeskUnavailable";
            if (CraftingRestrictions.StationUseBlocked(state, desk.Id)) return "ExpeditionBillDeskUseBlocked";
            if (state.InventoryCombat || state.Encounter != null && !ResolvedConflict(state) || PendingCalendarChoice(state))
                return "ExpeditionBillCombatUnavailable";
            if (!CapableWorker(state, worker) || View(state, worker).BlocksSight || AvailableHands(state, worker) < 1)
                return "ExpeditionBillWorkerIncapable";
            if (!AtSalePosition(state, worker, TestOnlyHavenAppraisalProfile.SiteX, TestOnlyHavenAppraisalProfile.SiteY))
                return "ExpeditionBillWorkerNotAtDesk";
            return null;
        }

        private string AssessExpeditionBill(Snapshot state, Command command, out ExpeditionBillRecord job, out ExpeditionBillBasis basis)
        {
            job = null;
            basis = null;
            if (expeditionBillProfile == null || state.SchemaVersion < Snapshot.ExpeditionBillSchema) return "ExpeditionBillNotSelected";
            if (state.ExpeditionEpisodeClose != null) return "ExpeditionEpisodeAlreadyClosed";
            if (command.Actor != TestOnlyExpeditionBillProfile.WorkerId) return "ExpeditionBillRepresentativeUnauthorized";
            if (command.X != 0 || command.Y != 0 || command.Inventory != null || command.Combat != null
                || command.Advancement != null || command.Ranged != null || command.OverwatchRider != OverwatchRider.None
                || command.SuppressionFire != null || command.DefensiveFormation != null || command.ExpeditionAssignment != null
                || command.HarvestSelection != null || command.MiningSelection != null || command.ProspectingExposure != null
                || command.RouteMappingWork != null) return "InvalidExpeditionBillPayload";
            job = OpenExpeditionBill(state);
            if (command.Kind == CommandKind.StartExpeditionBill) {
                if (command.Target != TestOnlyExpeditionBillProfile.BillVersionId) return "ExpeditionBillVersionUnknown";
                if (job != null) return "ExpeditionBillServiceSlotOccupied";
                if (state.ExpeditionBills.Any(x => x.Report != null)) return "ExpeditionBillAlreadyReconciled";
                if (state.ExpeditionBills.Length >= ExpeditionBillValidation.MaxAttempts) return "ExpeditionBillHistoryCapacityReached";
            } else {
                if (job == null || command.Target != job.Id) return "ExpeditionBillWorkNotOpen";
                if (command.Kind == CommandKind.CancelExpeditionBill) return null;
                if (command.Kind == CommandKind.PauseExpeditionBill)
                    return job.Status == ExpeditionBillStatus.Working ? null : "ExpeditionBillWorkNotRunning";
                if (command.Kind == CommandKind.ResumeExpeditionBill && job.Status != ExpeditionBillStatus.Paused)
                    return "ExpeditionBillWorkNotPaused";
                if (command.Kind == CommandKind.FinalizeExpeditionBill && job.Status != ExpeditionBillStatus.PendingCompletion)
                    return "ExpeditionBillWorkIncomplete";
            }
            var end = CampGreens.Add(state.RuleClock, job?.Work.Remaining ?? new RuleTime(ExpeditionBillRecord.RequiredSeconds));
            var charter = state.ExpeditionBillCharter;
            if (!charter.AuthorizedAt(state.RuleClock) || end >= charter.AuthorizationUntil) return "ExpeditionBillAuthorizationWindow";
            string failure = ExpeditionBillInputs(state, job?.Basis, out basis) ?? ExpeditionBillWorkerFailure(state, command.Actor);
            if (failure != null) return failure;
            if (end > state.RuleClock && IsOffCalendarActivity(state, command.Actor)) {
                var activity = ActivityInterval(state, command.Actor);
                if (activity.Action == WorldActionCommitment.Dash
                    || activity.Action == WorldActionCommitment.ActiveLabor && !CanContinueActivityLabor(state, command.Actor))
                    return "OffCalendarActionAlreadySpent";
            }
            if (WorkerHasIncompatibleLabor(state, command.Actor, end)) return "ExpeditionBillWorkerBusy";
            return null;
        }

        private static bool WorkerHasIncompatibleLabor(Snapshot state, string actor, RuleTime end)
            => state.ExpeditionAssignments.Any(x => x.WorkerId == actor && x.Open) || OrdinaryInventory.Busy(state, actor)
                || WorldActivityValidation.HasActiveLabor(state, actor, state.RuleClock,
                    end > state.RuleClock ? end : state.RuleClock.AddSeconds(1));

        private void BookExpeditionBill(Snapshot state, ExpeditionBillRecord job)
        {
            string intervalId = job.Id + ".labor." + (state.Revision + 1).ToString(CultureInfo.InvariantCulture);
            var interval = new WorkerInterval(intervalId, job.Id, job.WorkerId, state.RuleClock,
                CampGreens.Add(state.RuleClock, job.Work.Remaining));
            state.Work = state.Work.Reserve(job.Id, new[] { interval }, Array.Empty<ResourceReservation>());
            CommitActivityLabor(state, job.WorkerId, job.Id);
        }

        private static void PutExpeditionBill(Snapshot state, ExpeditionBillRecord job)
            => state.ExpeditionBills = state.ExpeditionBills.Select(x => x.Id == job.Id ? job : x).ToArray();

        private static void StopExpeditionBill(Snapshot state, ExpeditionBillRecord job, ExpeditionBillStatus status, string reason)
        {
            state.Work = state.Work.CancelFutureWork(job.Id, state.RuleClock);
            PutExpeditionBill(state, job.With(state, job.Work.Labor, status, reason));
        }

        private static void FinishExpeditionBill(Snapshot state, ExpeditionBillRecord job)
        {
            var lot = state.Work.Lots.Single(x => x.Id == job.Basis.TenderLotId);
            var title = state.InventoryLots.Single(x => x.LotId == lot.Id);
            var observation = new ExpeditionBillTenderObservation(title.OwnerId, lot.Amount);
            PutExpeditionBill(state, job.With(state, job.Work.Labor, ExpeditionBillStatus.Reconciled,
                "ExpeditionBillReconciled", observation));
        }

        private string ResolveExpeditionBill(Snapshot state, Command command)
        {
            string failure = AssessExpeditionBill(state, command, out var job, out var basis);
            if (failure != null) return failure;
            switch (command.Kind) {
                case CommandKind.StartExpeditionBill:
                    long revision = state.Revision + 1;
                    job = new ExpeditionBillRecord("expedition.bill." + revision.ToString(CultureInfo.InvariantCulture),
                        command.Actor, basis, revision, revision, state.RuleClock, default, ExpeditionBillStatus.Working, "ExpeditionBillAdmitted");
                    state.ExpeditionBills = state.ExpeditionBills.Append(job).ToArray();
                    BookExpeditionBill(state, job);
                    break;
                case CommandKind.PauseExpeditionBill:
                    StopExpeditionBill(state, job, ExpeditionBillStatus.Paused, "ExpeditionBillPausedByWorker");
                    break;
                case CommandKind.ResumeExpeditionBill:
                    BookExpeditionBill(state, job);
                    PutExpeditionBill(state, job.With(state, job.Work.Labor, ExpeditionBillStatus.Working, "ExpeditionBillResumed"));
                    break;
                case CommandKind.FinalizeExpeditionBill:
                    FinishExpeditionBill(state, job);
                    break;
                case CommandKind.CancelExpeditionBill:
                    StopExpeditionBill(state, job, ExpeditionBillStatus.Cancelled, "ExpeditionBillCancelled");
                    break;
            }
            return null;
        }

        private static RuleTime? NextExpeditionBillBoundary(Snapshot state)
        {
            var job = OpenExpeditionBill(state);
            if (job == null) return null;
            return job.Status == ExpeditionBillStatus.Working
                ? state.Work.WorkerIntervals.Single(x => x.JobId == job.Id && x.End > state.RuleClock).End
                : state.ExpeditionBillCharter.AuthorizationUntil;
        }

        private static void CreditExpeditionBill(Snapshot state, RuleTime elapsed)
        {
            var job = OpenExpeditionBill(state);
            if (job?.Status != ExpeditionBillStatus.Working) return;
            var progress = job.Work.Credit(elapsed);
            PutExpeditionBill(state, job.With(state, progress.Labor,
                progress.Complete ? ExpeditionBillStatus.PendingCompletion : ExpeditionBillStatus.Working,
                progress.Complete ? "ExpeditionBillCompletionDue" : "ExpeditionBillLaborCredited"));
        }

        private void ReconcileExpeditionBill(Snapshot state)
        {
            var job = OpenExpeditionBill(state);
            if (job == null) return;
            if (state.RuleClock >= state.ExpeditionBillCharter.AuthorizationUntil) {
                StopExpeditionBill(state, job, ExpeditionBillStatus.Expired, "ExpeditionBillAuthorizationExpired");
                return;
            }
            string invalid = ExpeditionBillInputs(state, job.Basis, out _);
            if (invalid != null) {
                StopExpeditionBill(state, job, ExpeditionBillStatus.Invalidated, invalid);
                return;
            }
            if (job.Status == ExpeditionBillStatus.Working) {
                string obstruction = ExpeditionBillWorkerFailure(state, job.WorkerId);
                if (obstruction != null) StopExpeditionBill(state, job, ExpeditionBillStatus.Paused, obstruction);
            }
        }

        private void FinishDueExpeditionBill(Snapshot state)
        {
            ReconcileExpeditionBill(state);
            var job = OpenExpeditionBill(state);
            if (job?.Status != ExpeditionBillStatus.PendingCompletion || job.Reason != "ExpeditionBillCompletionDue") return;
            string obstruction = ExpeditionBillWorkerFailure(state, job.WorkerId);
            if (obstruction == null && WorkerHasIncompatibleLabor(state, job.WorkerId, state.RuleClock))
                obstruction = "ExpeditionBillWorkerBusy";
            if (obstruction == null) FinishExpeditionBill(state, job);
            else PutExpeditionBill(state, job.With(state, job.Work.Labor, ExpeditionBillStatus.PendingCompletion, obstruction));
        }

        private string ValidateExpeditionBillProfile(Snapshot state)
        {
            if (expeditionBillProfile == null) return null;
            if (state.ExpeditionBillCharter?.BindingKey != expeditionBillProfile.Charter.BindingKey)
                return "ExpeditionBillCharterMismatch";
            foreach (var job in state.ExpeditionBills) {
                string failure = ExpeditionBillInputs(state, job.Basis, out _);
                if (failure != null) return failure;
            }
            return null;
        }
    }
}
#endif
