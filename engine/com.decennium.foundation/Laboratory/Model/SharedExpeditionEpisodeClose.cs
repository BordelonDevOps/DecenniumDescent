#if DECENNIUM_TEST_ONLY && (UNITY_EDITOR || DEVELOPMENT_BUILD || HEADLESS_TESTS)
using System;
using System.Collections.Generic;
using System.Globalization;
using System.Linq;
using System.Security.Cryptography;
using System.Text;

namespace Decennium.Foundation.Laboratory
{
    public sealed class TestOnlyExpeditionCloseProfile
    {
        public const string LeaderId = TestOnlyPolicy.ActorId;
        public const string MandateId = "TEST_ONLY.iron-episode-leader-close.v1";
        public const string EvidenceId = "TEST_ONLY.iron-episode-close-record-access.v1";
        public const ExpeditionCloseMetric PrimaryMetric = ExpeditionCloseMetric.RealizedNetExpedition;
        public bool MandateAuthorized { get; }
        public bool EvidenceAccessible { get; }
        public bool DeclaresNoRecruitedCompanion { get; }

        public TestOnlyExpeditionCloseProfile(bool mandateAuthorized = true, bool evidenceAccessible = true,
            bool declaresNoRecruitedCompanion = false)
        {
            MandateAuthorized = mandateAuthorized;
            EvidenceAccessible = evidenceAccessible;
            DeclaresNoRecruitedCompanion = declaresNoRecruitedCompanion;
        }

        internal string Key => string.Join("|", "FL26-46a4d52728ee6956f0bebcb5d2103ffd5bc67ba4",
            TestOnlyExpeditionBillProfile.EpisodeId, TestOnlyExpeditionBillProfile.CharterVersionId, LeaderId, MandateId,
            EvidenceId, PrimaryMetric, MandateAuthorized, EvidenceAccessible, DeclaresNoRecruitedCompanion,
            "scoped-none:named-route,camp,pursuit,devices,harvest,salvage,insurance,faction-proceeding,advancement-award",
            "no-underways-subject", "unresolved:pressure,strain,rest-debt,class-pools,corpse-handling,liabilities,profit,standing,renown,entitlements");
    }

    public sealed partial class TestOnlySharedWorldPolicy
    {
        private TestOnlyExpeditionCloseProfile expeditionCloseProfile;

        public TestOnlySharedWorldPolicy EnableExpeditionClose(TestOnlyExpeditionCloseProfile profile)
        {
            if (profile == null) throw new ArgumentNullException(nameof(profile));
            if (initializationStarted || expeditionCloseProfile != null || SelectedSchema != Snapshot.ExpeditionBillSchema)
                throw new InvalidOperationException("Select one episode close on the self-funded Expedition bill profile before initialization.");
            expeditionCloseProfile = profile;
            using (var sha = SHA256.Create())
                ContentFingerprint = "TEST_ONLY.expedition-close-v1-" + string.Concat(sha.ComputeHash(
                    Encoding.UTF8.GetBytes(ContentFingerprint + "|" + profile.Key)).Select(x => x.ToString("x2", CultureInfo.InvariantCulture)));
            return this;
        }

        private Command DiscoverExpeditionClose(Snapshot state, string actor)
        {
            if (expeditionCloseProfile == null || actor != TestOnlyExpeditionCloseProfile.LeaderId || state.ExpeditionEpisodeClose != null
                || !state.ExpeditionBills.Any(x => x.Report != null)) return null;
            return new Command("option." + state.Revision.ToString(CultureInfo.InvariantCulture) + ".expedition-close", actor,
                state.Revision, CommandKind.CloseExpeditionEpisode, TestOnlyExpeditionBillProfile.EpisodeId);
        }

        private string AssessExpeditionClose(Snapshot state, Command command, out ExpeditionEpisodeCloseRecord close)
        {
            close = null;
            if (expeditionCloseProfile == null || state.SchemaVersion != Snapshot.ExpeditionEpisodeCloseSchema)
                return "ExpeditionCloseNotSelected";
            if (command.Actor != TestOnlyExpeditionCloseProfile.LeaderId || !expeditionCloseProfile.MandateAuthorized)
                return "ExpeditionCloseLeaderUnauthorized";
            if (!expeditionCloseProfile.EvidenceAccessible) return "ExpeditionCloseEvidenceUnavailable";
            if (command.X != 0 || command.Y != 0 || command.Inventory != null || command.Combat != null || command.Advancement != null
                || command.Ranged != null || command.OverwatchRider != OverwatchRider.None || command.SuppressionFire != null
                || command.DefensiveFormation != null || command.ExpeditionAssignment != null || command.HarvestSelection != null
                || command.MiningSelection != null || command.ProspectingExposure != null || command.RouteMappingWork != null)
                return "InvalidExpeditionClosePayload";
            var charter = state.ExpeditionBillCharter;
            if (command.Target != TestOnlyExpeditionBillProfile.EpisodeId || charter?.EpisodeId != command.Target
                || charter.BindingKey != expeditionBillProfile.Charter.BindingKey) return "ExpeditionCloseEpisodeMismatch";
            if (state.ExpeditionEpisodeClose != null) return "ExpeditionEpisodeAlreadyClosed";
            if (state.InventoryCombat || PendingCalendarChoice(state)) return "ExpeditionCloseTacticalBoundary";
            if (state.Encounter?.Id != "world.fixed-conflict" || !ResolvedConflict(state)) return "ExpeditionCloseEncounterUnresolved";
            var exit = state.Receipts.LastOrDefault(x => CommandHistory.Read(x).Kind == CommandKind.EndFixedEncounter);
            if (exit == null || exit.Revision < state.Encounter.StartRevisions[0]) return "ExpeditionCloseEncounterUnresolved";

            var bill = state.ExpeditionBills.SingleOrDefault(x => x.Status == ExpeditionBillStatus.Reconciled);
            if (bill == null || ExpeditionBillInputs(state, bill.Basis, out _) != null) return "ExpeditionCloseReconciledBillRequired";
            if (bill.StartRevision <= exit.Revision) return "ExpeditionCloseHistoryMismatch";
            var view = View(state, command.Actor);
            if (!ActorLifeRules.CanAct(state, command.Actor) || view.Unaware || view.Clauses.Incapacitated)
                return "ExpeditionCloseLeaderIncapable";
            if (TestOnlyClubAttackPolicy.HasUnprocessedConditionDeadline(state)) return "ExpeditionCloseUnprocessedConditionDeadline";
            if (charter.MemberIds.Any(id => !state.Actors.Any(x => x.Id == id) || !state.Lives.Any(x => x.ActorId == id)
                || !state.Characters.Any(x => x.ActorId == id) || !state.Conditions.Any(x => x.Target == id)))
                return "ExpeditionCloseMemberFactsMissing";
            var members = new HashSet<string>(charter.MemberIds, StringComparer.Ordinal);
            if (state.WorldTraversals.Any(x => members.Contains(x.ActorId))
                || state.RouteTravels.Any(x => members.Contains(x.TravelerId) && x.Status == ExpeditionRouteTravelStatus.Moving))
                return "ExpeditionCloseUnresolvedTraversal";

            var meal = state.HavenMealPurchases.Single();
            var sale = state.HavenSales.Single(x => x.Id == bill.Basis.SaleId);
            if (!ExpeditionEpisodeCloseValidation.TryReadMealIntakes(state, meal, state.RuleClock, out var intakeIds))
                return "ExpeditionCloseMealIntakeRequired";
            var attempt = state.MiningAttempts.SingleOrDefault(x => x.SelectedUnitIds.Contains(sale.Basis.GoodsLotId)
                && (x.Status == MiningAttemptStatus.Success || x.Status == MiningAttemptStatus.CriticalSuccess)
                && x.ClosedAt.HasValue && x.ClosedAt.Value <= sale.StartedAt);
            if (attempt == null) return "ExpeditionCloseExtractionRequired";
            var units = state.MiningUnits.Where(x => x.DepositId == attempt.DepositId).ToArray();
            if (!units.Any(x => x.Id == sale.Basis.GoodsLotId && x.Status == MiningUnitStatus.Extracted && x.ReceivedLotId == sale.Basis.GoodsLotId)
                || !units.Any(x => x.Id == SharedMiningFixture.UnitB && x.Status == MiningUnitStatus.Forfeited)
                || units.Any(x => x.Status == MiningUnitStatus.Available))
                return "ExpeditionCloseMiningDispositionsIncomplete";

            var related = new HashSet<string>(new[] { sale.Basis.GoodsLotId, sale.Basis.TenderLotId, meal.Offer.MealLotId }, StringComparer.Ordinal);
            var scopedStock = state.InventoryLots.Where(x => members.Contains(x.OwnerId) || related.Contains(x.LotId)
                    || state.Work.Lots.Any(y => y.Id == x.LotId && members.Contains(y.CustodianId)))
                .Select(x => new ExpeditionCloseStock(x, state.Work.Lots.Single(y => y.Id == x.LotId))).ToArray();
            if (HasOpenExpeditionCloseCommitments(state, members, scopedStock)) return "ExpeditionCloseOpenCommitments";
            if (ClosureCoverageContradicted(state, members)) return "ExpeditionCloseCoverageContradicted";

            var capturedMembers = charter.MemberIds.Select(id => CaptureClosingMember(state, id)).ToArray();
            var hostile = WorldPositionResolver.Position(state, AdditionalTacticalActor.Id);
            var outcome = new ExpeditionCloseOutcome(TestOnlyExpeditionCloseProfile.PrimaryMetric,
                bill.Basis.NetExpeditionCopper, charter.NetTargetCopper, bill.Basis.GrossSaleCopper,
                charter.GrossTargetCopper, charter.ProfitAfterReservesTargetCopper);
            close = new ExpeditionEpisodeCloseRecord(charter.EpisodeId, charter.VersionId, command.Actor,
                TestOnlyExpeditionCloseProfile.MandateId, TestOnlyExpeditionCloseProfile.EvidenceId, command.Id, state.Revision,
                state.RuleClock, bill.Id, bill.UpdatedRevision, state.Encounter.Id, exit.Revision, AdditionalTacticalActor.Id,
                hostile.X, hostile.Y, attempt.Id, intakeIds, outcome, capturedMembers,
                units.Select(x => new ExpeditionCloseMiningDisposition(x.Id, x.Status, x.ReceivedLotId)), scopedStock,
                state.PortableEquipment.Where(x => members.Contains(x.OwnerId) || members.Contains(x.CustodianId) || related.Contains(x.Id)),
                state.Vessels.Where(x => members.Contains(x.OwnerId) || members.Contains(x.CustodianId)), EpisodeCloseCoverage());
            return null;
        }

        private string ResolveExpeditionClose(Snapshot state, Command command)
        {
            string failure = AssessExpeditionClose(state, command, out var close);
            if (failure == null) state.ExpeditionEpisodeClose = close;
            return failure;
        }

        private static bool HasOpenExpeditionCloseCommitments(Snapshot state, HashSet<string> members,
            IEnumerable<ExpeditionCloseStock> scopedStock)
        {
            var lotIds = new HashSet<string>(scopedStock.Select(x => x.Stock.Id), StringComparer.Ordinal);
            return WorldActivityProjection.OpenProcedures(state, Array.Empty<CommandOption>()).Any(x => members.Contains(x.ActorId))
                || state.Work.WorkerIntervals.Any(x => members.Contains(x.WorkerId) && x.End > state.RuleClock)
                || state.ExpeditionAssignments.Any(x => members.Contains(x.WorkerId) && x.Open)
                || state.Work.Reservations.Any(x => lotIds.Contains(x.LotId) && x.RemainingAmount != default);
        }

        private bool ClosureCoverageContradicted(Snapshot state, HashSet<string> members)
            => expeditionCloseProfile.DeclaresNoRecruitedCompanion && members.Contains(TestOnlyPolicy.CompanionId)
                || state.RouteTravels.Any(x => members.Contains(x.TravelerId))
                || state.ExpeditionCampActivities.Length != 0
                || state.HarvestAttempts.Any(x => members.Contains(x.WorkerId))
                || state.CharacterMilestones.Any(x => members.Contains(x.ActorId))
                || state.CharacterAdvancements.Any(x => members.Contains(x.ActorId));

        private static ExpeditionCloseMember CaptureClosingMember(Snapshot state, string actor)
        {
            var position = WorldPositionResolver.Position(state, actor);
            long movement = state.Receipts.LastOrDefault(r => {
                var command = CommandHistory.Read(r);
                return command.Actor == actor && command.Kind == CommandKind.BeginWorldStep;
            })?.Revision ?? 0;
            var conditions = TestOnlyClubAttackPolicy.ConditionsFor(state, actor);
            var effective = conditions.View().Components;
            var present = conditions.Applications.Where(x => x.Present(conditions.Now)).ToArray();
            ConditionStamp? Expiry(ConditionInstance instance)
            {
                var expiry = instance.Application.Expires;
                return expiry.HasValue ? new ConditionStamp(expiry.Value.Time, expiry.Value.Phase) : (ConditionStamp?)null;
            }
            var current = present.Select(x => new ExpeditionCloseCondition(x.Id, x.Application.Kind.ToString(),
                effective.Any(c => c.ApplicationId == x.Id && c.Kind == x.Application.Kind && !c.Inherited), false, Expiry(x)))
                .Concat(effective.Where(x => x.Inherited).Select(x => new ExpeditionCloseCondition(x.ApplicationId, x.Kind.ToString(),
                    true, true, Expiry(present.Single(instance => instance.Id == x.ApplicationId)))));
            return new ExpeditionCloseMember(state.Lives.Single(x => x.ActorId == actor), position.X, position.Y, movement,
                state.Characters.Single(x => x.ActorId == actor).Levels.Count, current);
        }

        private static ExpeditionCloseCoverage[] EpisodeCloseCoverage()
        {
            ExpeditionCloseCoverage Fact(ExpeditionCloseField field, ExpeditionCloseKnowledge status, string basis)
                => new ExpeditionCloseCoverage(field, status, basis);
            ExpeditionCloseCoverage Known(ExpeditionCloseField field, string basis) => Fact(field, ExpeditionCloseKnowledge.KnownValue, basis);
            ExpeditionCloseCoverage None(ExpeditionCloseField field, string basis) => Fact(field, ExpeditionCloseKnowledge.KnownNone, basis);
            ExpeditionCloseCoverage Unknown(ExpeditionCloseField field, string basis) => Fact(field, ExpeditionCloseKnowledge.Unresolved, basis);
            return new[] {
                Known(ExpeditionCloseField.Outcome, "resolved-conflict-and-reconciled-bill"),
                Known(ExpeditionCloseField.MembersAndLocations, "charter-members-and-resolved-world-points"),
                Known(ExpeditionCloseField.LifeAndInjuries, "current-actor-life-records"),
                Known(ExpeditionCloseField.Conditions, "operative-and-present-condition-records"),
                Known(ExpeditionCloseField.ProvisionsAndContainers, "actual-member-and-episode-stock"),
                Unknown(ExpeditionCloseField.ResourcePools, "class-pools-unrepresented"),
                Known(ExpeditionCloseField.Movement, "ordinary-movement-command-history"),
                None(ExpeditionCloseField.NamedRouteTravel, "authored-no-named-route-travel-in-episode"),
                None(ExpeditionCloseField.Camps, "authored-no-episode-camp-use"),
                Unknown(ExpeditionCloseField.Pressure, "pressure-authority-unrepresented"),
                None(ExpeditionCloseField.Pursuit, "authored-no-episode-pursuit-operation"),
                Fact(ExpeditionCloseField.Heat, ExpeditionCloseKnowledge.NotApplicable, "no-episode-underways-subject"),
                Unknown(ExpeditionCloseField.Strain, "strain-history-unrepresented"),
                Unknown(ExpeditionCloseField.RestDebt, "rest-debt-history-unrepresented"),
                Known(ExpeditionCloseField.Companions, "autonomous-companion-in-actual-roster"),
                None(ExpeditionCloseField.Devices, "authored-no-other-episode-companion-device"),
                Known(ExpeditionCloseField.HostileDeath, "supported-resolved-hostile-death"),
                Unknown(ExpeditionCloseField.CorpseHandling, "corpse-inventory-and-anatomy-unrepresented"),
                Known(ExpeditionCloseField.CargoTitleAndCustody, "current-authoritative-stock-and-title"),
                Known(ExpeditionCloseField.MiningDispositions, "terminal-extraction-unit-records"),
                None(ExpeditionCloseField.HarvestAndSalvageClaims, "authored-no-harvest-or-salvage-claim-undertaken"),
                Known(ExpeditionCloseField.QuotesAndPayments, "referenced-actual-bill-and-payment-history"),
                Unknown(ExpeditionCloseField.WiderLiabilitiesAndProfit, "wider-episode-costs-liabilities-and-allocations-unresolved"),
                None(ExpeditionCloseField.Insurance, "authored-no-episode-policy-or-filing"),
                Unknown(ExpeditionCloseField.StandingAndRenown, "standing-and-renown-history-unrepresented"),
                None(ExpeditionCloseField.FactionActions, "authored-no-episode-faction-proceeding"),
                None(ExpeditionCloseField.RecordedAdvancement, "authored-no-episode-award-or-advancement-event"),
                Unknown(ExpeditionCloseField.UnadjudicatedEntitlements, "earned-entitlement-adjudication-unrepresented")
            };
        }
    }
}
#endif
