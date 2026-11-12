#if DECENNIUM_TEST_ONLY && (UNITY_EDITOR || DEVELOPMENT_BUILD || HEADLESS_TESTS)
using System;
using System.Collections.Generic;
using System.Globalization;
using System.Linq;
using System.Security.Cryptography;
using System.Text;

namespace Decennium.Foundation.Laboratory
{
    public sealed class TestOnlyHavenSaleProfile
    {
        public const string BuyerId = "TEST_ONLY.haven-copper-buyer";
        public const string SellerId = TestOnlyHavenAppraisalProfile.WorkerId;
        public const string OfferId = "TEST_ONLY.haven-iron-offer";
        public const string OfferVersionId = OfferId + ".v1";
        public const string CounterId = TestOnlyHavenAppraisalProfile.DeskId;
        public const string MandateId = "TEST_ONLY.buyer-authorized-iron-and-tender";
        public const string ClearanceId = "TEST_ONLY.iron-routine-sale-priority-cleared";
        public const string ExemptionId = "TEST_ONLY.iron-offer-written-routine-levy-exemption";
        public const string IssuerId = "TEST_ONLY.haven-authorized-revenue-office";
        public const string JurisdictionId = "TEST_ONLY.haven-routine-goods-jurisdiction";
        public const string TenderLotId = "TEST_ONLY.haven-buyer-two-copper-coins";
        public const string CoinProfileId = "TEST_ONLY.haven-coins-physical-profile";
        public const string CurrencyUnitId = "TEST_ONLY.genuine-copper-piece";
        public const string MintId = "TEST_ONLY.haven-accepted-copper-mint";
        public const string BuyerBallastId = "TEST_ONLY.haven-buyer-capacity-ballast";
        internal const string BuyerCharacterProfile = "TEST_ONLY.haven-buyer-character";
        internal const int BuyerX = TestOnlyHavenAppraisalProfile.SiteX;
        internal const int BuyerY = TestOnlyHavenAppraisalProfile.SiteY + 1;
        internal static RuleQuantity CoinMass => new RuleQuantity(1, 50);
        // Authored positive packed volume for the selected physical tender. The source supplies coin weight.
        internal static RuleQuantity CoinVolume => new RuleQuantity(1, 20000);
        public static RuleQuantity QuoteCopper => new RuleQuantity(7, 3);
        public const long PaymentCopper = 2;

        public bool BuyerConsented { get; }
        public bool DispositionCleared { get; }
        public bool WrittenExemption { get; }
        public bool CurrencyAccepted { get; }
        public bool BuyerBallast { get; }
        public int OpeningCoins { get; }
        public RuleTime ValidFrom { get; }
        public RuleTime ExpiresAt { get; }

        public TestOnlyHavenSaleProfile(bool buyerConsented = true, bool dispositionCleared = true,
            bool writtenExemption = true, bool currencyAccepted = true, int openingCoins = 2,
            int validFrom = 0, int expiresAt = 14400, bool buyerBallast = false)
        {
            if (openingCoins < 1 || openingCoins > 2 || validFrom < 0 || expiresAt <= validFrom)
                throw new ArgumentException("Invalid finite sale fixture.");
            BuyerConsented = buyerConsented;
            DispositionCleared = dispositionCleared;
            WrittenExemption = writtenExemption;
            CurrencyAccepted = currencyAccepted;
            BuyerBallast = buyerBallast;
            OpeningCoins = openingCoins;
            ValidFrom = new RuleTime(validFrom);
            ExpiresAt = new RuleTime(expiresAt);
        }

        internal string Key => string.Join("|", "FL19-22-FL25-EX03-07-46a4d52728ee6956f0bebcb5d2103ffd5bc67ba4",
            OfferId, OfferVersionId, CounterId, SellerId, BuyerId, BuyerCharacterProfile, BuyerX, BuyerY, "buyer-10-8hp-30ft",
            MandateId, ClearanceId, ExemptionId, IssuerId, JurisdictionId, "registered-routine-3-percent-exempt",
            "no-other-charge", "1800-joint-seconds-half-open-auto-exchange", SharedMiningFixture.UnitA, TenderLotId,
            CoinProfileId, CurrencyUnitId, MintId, QuoteCopper, PaymentCopper, CoinMass, CoinVolume,
            BuyerConsented, DispositionCleared, WrittenExemption, CurrencyAccepted, OpeningCoins, ValidFrom, ExpiresAt,
            BuyerBallast, BuyerBallastId, "199/2 pound ballast");
    }

    public sealed partial class TestOnlySharedWorldPolicy
    {
        private TestOnlyHavenSaleProfile havenSaleProfile;

        public TestOnlySharedWorldPolicy EnableHavenSale(TestOnlyHavenSaleProfile profile)
        {
            if (profile == null) throw new ArgumentNullException(nameof(profile));
            if (initializationStarted || havenSaleProfile != null || SelectedSchema != Snapshot.HavenAppraisalSchema)
                throw new InvalidOperationException("Select one funded sale after the bounded Haven appraisal profile and before initialization.");
            havenSaleProfile = profile;
            bodies.RegisterDeferredConditionTarget(TestOnlyHavenSaleProfile.BuyerId);
            using (var sha = SHA256.Create())
                ContentFingerprint = "TEST_ONLY.haven-sale-v1-" + string.Concat(sha.ComputeHash(
                    Encoding.UTF8.GetBytes(ContentFingerprint + "|" + profile.Key)).Select(x => x.ToString("x2", CultureInfo.InvariantCulture)));
            return this;
        }

        private void InitializeHavenBuyer(Snapshot s)
        {
            if (havenSaleProfile == null) return;
            const string buyer = TestOnlyHavenSaleProfile.BuyerId;
            s.Actors = s.Actors.Append(new ActorState { Id = buyer, X = TestOnlyHavenSaleProfile.BuyerX,
                Y = TestOnlyHavenSaleProfile.BuyerY }).ToArray();
            s.Characters = s.Characters.Append(new ActorCharacterRecord(buyer, TestOnlyHavenSaleProfile.BuyerCharacterProfile,
                new[] { 10, 10, 10, 10, 10, 10 }, new[] { new CharacterLevelFact("Merchant", 8) })).ToArray();
            s.Lives = s.Lives.Append(ActorLifeRules.Record(buyer, new LifeState(8, 8, usesDeathSaves: false), false)).ToArray();
            s.ActorMovement = s.ActorMovement.Append(new ActorMovementRecord(buyer, 30)).ToArray();
            s.TacticalActors = s.TacticalActors.Append(new ActorTacticalRecord(buyer)).ToArray();
            s.Conditions = s.Conditions.Append(new ConditionJournal(ConditionHistory.PolicyId, buyer, new ConditionStamp(s.RuleClock))).ToArray();
        }

        private static PortableStorageProfileRecord HavenCoinProfile()
            => new PortableStorageProfileRecord(TestOnlyHavenSaleProfile.CoinProfileId, TestOnlyHavenSaleProfile.CurrencyUnitId,
                TestOnlyHavenSaleProfile.CoinVolume, massPerUnitLb: TestOnlyHavenSaleProfile.CoinMass);

        private void InitializeHavenTender(Snapshot s)
        {
            if (havenSaleProfile == null) return;
            const string buyer = TestOnlyHavenSaleProfile.BuyerId;
            const string tender = TestOnlyHavenSaleProfile.TenderLotId;
            var count = new RuleQuantity(havenSaleProfile.OpeningCoins);
            var stock = new ResourceLot(tender, TestOnlyHavenSaleProfile.CurrencyUnitId, count, buyer, buyer);
            s.Work = new WorkLedger(s.Work.Lots.Append(stock), s.Work.WorkerIntervals, s.Work.Reservations);
            s.InventoryLots = s.InventoryLots.Append(new InventoryLotRecord(tender, "", buyer, count, s.RuleClock,
                NutritionKind.None, null, InventoryAccess.Ready)).ToArray();
            s.PortableStorageProfiles = new[] { HavenCoinProfile() };
            PortableEquipmentRules.RegisterInventoryLot(s, tender, buyer, buyer);
            if (havenSaleProfile.BuyerBallast) {
                var mass = new RuleQuantity(199, 2);
                s.PortableEquipment = s.PortableEquipment.Append(new PortableEquipmentRecord(TestOnlyHavenSaleProfile.BuyerBallastId,
                    "TEST_ONLY.haven-buyer-ballast", buyer, buyer, "", PortablePlacement.Ground, PortableLinkKind.None, "",
                    PortableMassBasis.Fixed, mass, mass, groundX: TestOnlyHavenSaleProfile.BuyerX,
                    groundY: TestOnlyHavenSaleProfile.BuyerY)).ToArray();
            }
        }

        private string ValidateHavenSaleContent(Snapshot s)
        {
            if (havenSaleProfile == null) return null;
            var expected = HavenCoinProfile();
            var actual = s.PortableStorageProfiles.SingleOrDefault(x => x.ProfileId == expected.ProfileId);
            if (s.PortableStorageProfiles.Length != (connectedBloodSpecimen ? 2 : 1))
                return "InvalidHavenTenderProfile";
            if (actual == null || actual.ProfileId != expected.ProfileId || actual.QuantityUnitId != expected.QuantityUnitId
                || actual.MassPerUnitLb != expected.MassPerUnitLb || actual.PackedVolumePerUnitCubicFeet != expected.PackedVolumePerUnitCubicFeet
                || actual.AllowedContainedProfileIds.Count != 0 || actual.RequiresInstalledTemporaryCamp)
                return "InvalidHavenTenderProfile";
            const string buyer = TestOnlyHavenSaleProfile.BuyerId;
            return !s.WorldSchedule.Order.Contains(buyer) && s.Actors.Any(x => x.Id == buyer)
                && !s.Clubs.Any(x => x.OwnerId == buyer) && !s.SkillTraining.Any(x => x.ActorId == buyer)
                ? null : "InvalidHavenBuyerRegistration";
        }

        private static bool IsHavenSaleCommand(CommandKind kind)
            => kind == CommandKind.StartHavenSale || kind == CommandKind.PauseHavenSale || kind == CommandKind.ResumeHavenSale
                || kind == CommandKind.FinalizeHavenSale || kind == CommandKind.CancelHavenSale;

        private IEnumerable<Command> DiscoverHavenSaleCommands(Snapshot s, string actor)
        {
            if (havenSaleProfile == null || actor != TestOnlyHavenSaleProfile.SellerId && actor != TestOnlyHavenSaleProfile.BuyerId)
                yield break;
            Command OfferCommand(CommandKind kind, string target) => new Command("option." + s.Revision.ToString(CultureInfo.InvariantCulture)
                + ".haven-sale." + kind, actor, s.Revision, kind, target);
            var sale = s.HavenSales.SingleOrDefault(x => x.Open);
            bool seller = actor == TestOnlyHavenSaleProfile.SellerId;
            if (sale == null) {
                if (seller && s.HavenAppraisals.Any(x => x.Status == HavenAppraisalStatus.Completed)
                    && !s.HavenSales.Any(x => x.Status == HavenSaleStatus.Paid))
                    yield return OfferCommand(CommandKind.StartHavenSale, TestOnlyHavenSaleProfile.OfferVersionId);
                yield break;
            }
            yield return OfferCommand(CommandKind.CancelHavenSale, sale.Id);
            if (sale.Status == HavenSaleStatus.Working) yield return OfferCommand(CommandKind.PauseHavenSale, sale.Id);
            if (seller && sale.Status == HavenSaleStatus.Paused) yield return OfferCommand(CommandKind.ResumeHavenSale, sale.Id);
            if (seller && sale.Status == HavenSaleStatus.PendingSettlement) yield return OfferCommand(CommandKind.FinalizeHavenSale, sale.Id);
        }

        private bool SaleTermsValidAt(RuleTime time)
            => havenSaleProfile.ValidFrom <= time && time < havenSaleProfile.ExpiresAt;

        private string SaleTermsFailure()
        {
            if (!havenSaleProfile.BuyerConsented) return "HavenSaleBuyerMandateMissing";
            if (!havenSaleProfile.DispositionCleared) return "HavenSaleDispositionNotCleared";
            if (!havenSaleProfile.WrittenExemption) return "HavenSaleExemptionMissing";
            if (!havenSaleProfile.CurrencyAccepted) return "HavenSaleTenderNotAccepted";
            return null;
        }

        private static bool SaleAssetAtParty(Snapshot s, string lotId, string party, string unitId, RuleQuantity amount,
            NutritionKind nutrition = NutritionKind.None)
        {
            var lot = s.Work.Lots.SingleOrDefault(x => x.Id == lotId);
            var inventory = s.InventoryLots.SingleOrDefault(x => x.LotId == lotId);
            var item = s.PortableEquipment.SingleOrDefault(x => x.Id == lotId);
            return lot != null && lot.UnitId == unitId && lot.Amount == amount && lot.LocationId == party && lot.CustodianId == party
                && inventory != null && inventory.ParentId == "" && inventory.OwnerId == party && inventory.CreatedAmount == amount
                && inventory.Access == InventoryAccess.Ready && inventory.Nutrition == nutrition
                && !s.InventoryLots.Any(x => x.ParentId == lotId)
                && item != null && item.LinkKind == PortableLinkKind.InventoryLot && item.LinkedId == lotId && item.ParentId == ""
                && item.OwnerId == party && item.CustodianId == party && item.Placement == PortablePlacement.Carried
                && PortableEquipmentRules.Accessible(s, party, item) && !s.PortableEquipment.Any(x => x.ParentId == lotId);
        }

        private static string SaleAssets(Snapshot s)
        {
            var appraisal = s.HavenAppraisals.SingleOrDefault(x => x.Status == HavenAppraisalStatus.Completed);
            const string goods = SharedMiningFixture.UnitA;
            const string seller = TestOnlyHavenSaleProfile.SellerId;
            var unit = s.MiningUnits.SingleOrDefault(x => x.Id == goods);
            if (appraisal == null || appraisal.Basis.UnitId != goods || appraisal.Basis.OwnerId != seller
                || appraisal.Basis.CustodianId != seller || appraisal.Basis.Quantity != TestOnlyHavenAppraisalProfile.WholeUnitMass
                || unit == null || unit.Status != MiningUnitStatus.Extracted || unit.ReceivedLotId != goods
                || unit.Condition != MiningUnitCondition.Intact || unit.MassPounds != appraisal.Basis.Quantity
                || !s.MiningDeposits.Any(x => x.Id == unit.DepositId && x.VersionId == appraisal.Basis.DepositVersionId)
                || !SaleAssetAtParty(s, goods, seller, "mass-pound", appraisal.Basis.Quantity))
                return "HavenSaleAppraisedIronUnavailable";
            const string tender = TestOnlyHavenSaleProfile.TenderLotId;
            var coins = s.PortableEquipment.SingleOrDefault(x => x.Id == tender);
            if (!SaleAssetAtParty(s, tender, TestOnlyHavenSaleProfile.BuyerId, TestOnlyHavenSaleProfile.CurrencyUnitId,
                new RuleQuantity(TestOnlyHavenSaleProfile.PaymentCopper)) || coins.MassBasis != PortableMassBasis.CountedQuantity
                || coins.ProfileId != TestOnlyHavenSaleProfile.CoinProfileId)
                return "HavenSaleTenderUnavailable";
            return null;
        }

        private static bool AtSalePosition(Snapshot s, string actor, int x, int y)
        {
            var position = WorldPositionResolver.Position(s, actor);
            return position.X == new RuleQuantity(x) && position.Y == new RuleQuantity(y)
                && !s.WorldTraversals.Any(t => t.ActorId == actor)
                && !s.RouteTravels.Any(t => t.TravelerId == actor && t.Status == ExpeditionRouteTravelStatus.Moving);
        }

        private string SaleCounterFailure(Snapshot s)
        {
            const string seller = TestOnlyHavenSaleProfile.SellerId;
            const string buyer = TestOnlyHavenSaleProfile.BuyerId;
            var counter = s.Structures.SingleOrDefault(x => x.Id == TestOnlyHavenSaleProfile.CounterId);
            if (counter == null || counter.ProfileId != AppraisalDeskStructure || counter.LocationId != AppraisalGround
                || counter.Broken || CraftingRestrictions.StationUseBlocked(s, counter.Id))
                return "HavenSaleCounterUnavailable";
            if (s.InventoryCombat || s.Encounter != null && !ResolvedConflict(s) || PendingCalendarChoice(s))
                return "HavenSaleCombatUnavailable";
            if (!AtSalePosition(s, seller, TestOnlyHavenAppraisalProfile.SiteX, TestOnlyHavenAppraisalProfile.SiteY)
                || !AtSalePosition(s, buyer, TestOnlyHavenSaleProfile.BuyerX, TestOnlyHavenSaleProfile.BuyerY)
                || !NearPortable(s.Actors.Single(x => x.Id == seller), s.Actors.Single(x => x.Id == buyer)))
                return "HavenSaleParticipantsNotAtCounter";
            foreach (string participant in new[] { seller, buyer })
                if (!CapableWorker(s, participant) || View(s, participant).BlocksSight || AvailableHands(s, participant) < 1)
                    return "HavenSaleParticipantIncapable";
            return null;
        }

        private static string PrepareSaleDelivery(Snapshot s, out Snapshot delivery)
        {
            delivery = s.Copy();
            TransferWholePortableLotTitle(delivery, SharedMiningFixture.UnitA, TestOnlyHavenSaleProfile.BuyerId);
            TransferWholePortableLotTitle(delivery, TestOnlyHavenSaleProfile.TenderLotId, TestOnlyHavenSaleProfile.SellerId);
            PortableEquipmentRules.SynchronizeLinks(delivery);
            return CheckPortableProjectedState(delivery);
        }

        private static void TransferWholePortableLotTitle(Snapshot s, string lotId, string recipient)
        {
            var item = s.PortableEquipment.Single(x => x.Id == lotId);
            SetPortable(s, new PortableEquipmentRecord(item.Id, item.ProfileId, recipient, recipient, "", PortablePlacement.Carried,
                item.LinkKind, item.LinkedId, item.MassBasis, item.SourceWeightLb, item.OperationalWeightLb, item.PrintedLoad));
            s.InventoryLots = s.InventoryLots.Select(x => x.LotId != lotId ? x : new InventoryLotRecord(x.LotId,
                x.ParentId, recipient, x.CreatedAmount, x.CreatedAt, x.Nutrition, x.FreshUntil, InventoryAccess.Ready)).ToArray();
        }

        private HavenSaleBasis CreateSaleBasis(HavenAppraisalRecord appraisal) => new HavenSaleBasis(
            TestOnlyHavenSaleProfile.OfferId, TestOnlyHavenSaleProfile.OfferVersionId, TestOnlyHavenSaleProfile.SellerId,
            TestOnlyHavenSaleProfile.BuyerId, TestOnlyHavenSaleProfile.CounterId, TestOnlyHavenSaleProfile.MandateId,
            TestOnlyHavenSaleProfile.ClearanceId, TestOnlyHavenSaleProfile.ExemptionId, TestOnlyHavenSaleProfile.IssuerId,
            TestOnlyHavenSaleProfile.JurisdictionId, appraisal.Id, SharedMiningFixture.UnitA, TestOnlyHavenSaleProfile.TenderLotId,
            TestOnlyHavenSaleProfile.CurrencyUnitId, TestOnlyHavenSaleProfile.MintId, appraisal.Basis.Quantity,
            TestOnlyHavenSaleProfile.PaymentCopper, TestOnlyHavenSaleProfile.QuoteCopper, havenSaleProfile.ValidFrom, havenSaleProfile.ExpiresAt);

        private static string SaleLaborFailure(Snapshot s, RuleTime end, bool finalizing)
        {
            foreach (string participant in new[] { TestOnlyHavenSaleProfile.SellerId, TestOnlyHavenSaleProfile.BuyerId }) {
                if (OrdinaryInventory.Busy(s, participant) || s.ExpeditionAssignments.Any(x => x.WorkerId == participant && x.Open)
                    || !finalizing && WorldActivityValidation.HasActiveLabor(s, participant, s.RuleClock, end))
                    return "HavenSaleParticipantBusy";
                if (!finalizing && IsOffCalendarActivity(s, participant)) {
                    var interval = ActivityInterval(s, participant);
                    if (interval.Action == WorldActionCommitment.Dash
                        || interval.Action == WorldActionCommitment.ActiveLabor && !CanContinueActivityLabor(s, participant))
                        return "OffCalendarActionAlreadySpent";
                }
            }
            return null;
        }

        private string AssessHavenSale(Snapshot s, Command command, out HavenSaleRecord sale, out HavenSaleBasis basis,
            out Snapshot delivery)
        {
            sale = null;
            basis = null;
            delivery = null;
            if (havenSaleProfile == null || s.SchemaVersion < Snapshot.HavenSaleSchema) return "HavenSaleNotSelected";
            bool controls = command.Kind == CommandKind.PauseHavenSale || command.Kind == CommandKind.CancelHavenSale;
            if (command.Actor != TestOnlyHavenSaleProfile.SellerId && (!controls || command.Actor != TestOnlyHavenSaleProfile.BuyerId))
                return "HavenSaleParticipantUnauthorized";
            if (command.X != 0 || command.Y != 0 || command.Inventory != null || command.Combat != null
                || command.Advancement != null || command.Ranged != null || command.OverwatchRider != OverwatchRider.None
                || command.SuppressionFire != null || command.DefensiveFormation != null || command.ExpeditionAssignment != null
                || command.HarvestSelection != null || command.MiningSelection != null || command.ProspectingExposure != null
                || command.RouteMappingWork != null)
                return "InvalidHavenSalePayload";
            bool starting = command.Kind == CommandKind.StartHavenSale;
            if (starting) {
                if (command.Target != TestOnlyHavenSaleProfile.OfferVersionId) return "HavenSaleOfferUnknown";
                if (s.HavenSales.Any(x => x.Status == HavenSaleStatus.Paid)) return "HavenSaleAlreadyPaid";
                if (s.HavenSales.Any(x => x.Open)) return "HavenSaleAgreementOccupied";
                if (s.HavenSales.Length >= HavenSaleValidation.MaxRecords) return "HavenSaleHistoryCapacityReached";
            } else {
                sale = s.HavenSales.SingleOrDefault(x => x.Id == command.Target && x.Open);
                if (sale == null) return "HavenSaleAgreementNotOpen";
                if (command.Kind == CommandKind.CancelHavenSale) return null;
                if (command.Kind == CommandKind.PauseHavenSale)
                    return sale.Status == HavenSaleStatus.Working ? null : "HavenSaleWorkNotRunning";
                if (command.Kind == CommandKind.FinalizeHavenSale && sale.Status != HavenSaleStatus.PendingSettlement)
                    return "HavenSaleWorkIncomplete";
                if (command.Kind == CommandKind.ResumeHavenSale && sale.Status != HavenSaleStatus.Paused)
                    return "HavenSaleWorkNotPaused";
            }
            if (!SaleTermsValidAt(s.RuleClock)) return "HavenSaleOfferNotCurrent";
            bool finalizing = command.Kind == CommandKind.FinalizeHavenSale;
            var remaining = sale?.Work.Remaining ?? new RuleTime(HavenSaleRecord.RequiredSeconds);
            var end = CampGreens.Add(s.RuleClock, remaining);
            if (!finalizing && end >= havenSaleProfile.ExpiresAt) return "HavenSaleCannotFinishBeforeExpiry";
            string failure = SaleTermsFailure() ?? SaleAssets(s);
            if (failure != null) return failure;
            var appraisal = s.HavenAppraisals.Single(x => x.Status == HavenAppraisalStatus.Completed);
            basis = CreateSaleBasis(appraisal);
            if (!starting && appraisal.Id != sale.Basis.AppraisalId) return "HavenSaleAppraisalChanged";
            if (starting && (s.Work.AvailableAmount(basis.GoodsLotId) != basis.GoodsQuantity
                || s.Work.AvailableAmount(basis.TenderLotId) != new RuleQuantity(basis.TenderCount)))
                return "HavenSaleAssetReserved";
            return SaleCounterFailure(s) ?? SaleLaborFailure(s, end, finalizing) ?? PrepareSaleDelivery(s, out delivery);
        }

        private void BookHavenSale(Snapshot s, HavenSaleRecord sale, bool reserve)
        {
            var basis = sale.Basis;
            var end = CampGreens.Add(s.RuleClock, sale.Work.Remaining);
            string stamp = (s.Revision + 1).ToString(CultureInfo.InvariantCulture);
            var bookings = new[] {
                new WorkerInterval(sale.Id + ".seller." + stamp, sale.Id, basis.SellerId, s.RuleClock, end),
                new WorkerInterval(sale.Id + ".buyer." + stamp, sale.Id, basis.BuyerId, s.RuleClock, end) };
            var claims = reserve ? new[] {
                new ResourceReservation(sale.GoodsClaimId, sale.Id, basis.GoodsLotId, basis.GoodsQuantity),
                new ResourceReservation(sale.TenderClaimId, sale.Id, basis.TenderLotId, new RuleQuantity(basis.TenderCount)) }
                : Array.Empty<ResourceReservation>();
            s.Work = s.Work.Reserve(sale.Id, bookings, claims);
            foreach (var booking in bookings) CommitActivityLabor(s, booking.WorkerId, sale.Id);
        }

        private static void PutHavenSale(Snapshot s, HavenSaleRecord sale)
            => s.HavenSales = s.HavenSales.Select(x => x.Id == sale.Id ? sale : x).ToArray();

        private static void EndHavenSale(Snapshot s, HavenSaleRecord sale, HavenSaleStatus status, string reason)
        {
            s.Work = s.Work.CancelFutureWork(sale.Id, s.RuleClock).Release(sale.Id, sale.GoodsClaimId).Release(sale.Id, sale.TenderClaimId);
            PutHavenSale(s, sale.With(s, sale.Work.Labor, status, reason));
        }

        private static void PauseHavenSale(Snapshot s, HavenSaleRecord sale, string reason)
        {
            s.Work = s.Work.CancelFutureWork(sale.Id, s.RuleClock);
            PutHavenSale(s, sale.With(s, sale.Work.Labor, HavenSaleStatus.Paused, reason));
        }

        private static void ApplyHavenPayment(Snapshot s, HavenSaleRecord sale, Snapshot delivery)
        {
            s.PortableEquipment = delivery.PortableEquipment;
            s.InventoryLots = delivery.InventoryLots;
            s.Work = delivery.Work;
            EndHavenSale(s, sale, HavenSaleStatus.Paid, "HavenSalePaid");
        }

        private string ResolveHavenSale(Snapshot s, Command command)
        {
            string failure = AssessHavenSale(s, command, out var sale, out var basis, out var delivery);
            if (failure != null) return failure;
            switch (command.Kind) {
                case CommandKind.StartHavenSale:
                    long revision = s.Revision + 1;
                    sale = new HavenSaleRecord("haven.sale." + revision.ToString(CultureInfo.InvariantCulture), basis, revision,
                        revision, s.RuleClock, s.RuleClock, default, HavenSaleStatus.Working, "HavenSaleAdmitted", null);
                    BookHavenSale(s, sale, true);
                    s.HavenSales = s.HavenSales.Append(sale).ToArray();
                    break;
                case CommandKind.PauseHavenSale:
                    PauseHavenSale(s, sale, "HavenSalePausedByParty");
                    break;
                case CommandKind.ResumeHavenSale:
                    BookHavenSale(s, sale, false);
                    PutHavenSale(s, sale.With(s, sale.Work.Labor, HavenSaleStatus.Working, "HavenSaleResumed"));
                    break;
                case CommandKind.CancelHavenSale:
                    EndHavenSale(s, sale, HavenSaleStatus.Cancelled, "HavenSaleCancelledByParty");
                    break;
                case CommandKind.FinalizeHavenSale:
                    ApplyHavenPayment(s, sale, delivery);
                    break;
            }
            return null;
        }

        private static RuleTime? NextHavenSaleBoundary(Snapshot s)
        {
            var sale = s.HavenSales.SingleOrDefault(x => x.Open);
            if (sale == null) return null;
            if (sale.Status != HavenSaleStatus.Working) return sale.Basis.ExpiresAt;
            var workEnd = CampGreens.Add(s.RuleClock, sale.Work.Remaining);
            return workEnd < sale.Basis.ExpiresAt ? workEnd : sale.Basis.ExpiresAt;
        }

        private static void CreditHavenSaleWork(Snapshot s, RuleTime elapsed)
        {
            var sale = s.HavenSales.SingleOrDefault(x => x.Status == HavenSaleStatus.Working);
            if (sale == null) return;
            var progress = sale.Work.Credit(elapsed);
            PutHavenSale(s, sale.With(s, progress.Labor, progress.Complete ? HavenSaleStatus.PendingSettlement : HavenSaleStatus.Working,
                progress.Complete ? "HavenSaleSettlementDue" : "HavenSaleLaborCredited"));
        }

        private void ReconcileHavenSale(Snapshot s)
        {
            if (havenSaleProfile == null) return;
            var sale = s.HavenSales.SingleOrDefault(x => x.Open);
            if (sale == null) return;
            if (!sale.Basis.ValidAt(s.RuleClock)) {
                EndHavenSale(s, sale, HavenSaleStatus.Expired, "HavenSaleExpired");
                return;
            }
            string invalid = SaleTermsFailure() ?? SaleAssets(s);
            if (invalid != null) {
                EndHavenSale(s, sale, HavenSaleStatus.Invalidated, invalid);
                return;
            }
            if (sale.Status == HavenSaleStatus.Working) {
                string ineligible = SaleCounterFailure(s);
                if (ineligible != null) PauseHavenSale(s, sale, ineligible);
            }
        }

        private void SettleDueHavenSale(Snapshot s)
        {
            if (havenSaleProfile == null) return;
            ReconcileHavenSale(s);
            var sale = s.HavenSales.SingleOrDefault(x => x.Status == HavenSaleStatus.PendingSettlement && x.Reason == "HavenSaleSettlementDue");
            if (sale == null) return;
            string failure = SaleCounterFailure(s) ?? SaleLaborFailure(s, s.RuleClock, true);
            Snapshot delivery = null;
            if (failure == null) failure = PrepareSaleDelivery(s, out delivery);
            if (failure != null) PutHavenSale(s, sale.With(s, sale.Work.Labor, HavenSaleStatus.PendingSettlement, failure));
            else ApplyHavenPayment(s, sale, delivery);
        }
    }
}
#endif
