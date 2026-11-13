#if DECENNIUM_TEST_ONLY && (UNITY_EDITOR || DEVELOPMENT_BUILD || HEADLESS_TESTS)
using System;
using System.Collections.Generic;
using System.Collections.ObjectModel;
using System.Linq;

namespace Decennium.Foundation.Laboratory
{
    public sealed class ExpeditionVisibleActor
    {
        public string Id { get; }
        public int X { get; }
        public int Y { get; }

        internal ExpeditionVisibleActor(ActorState actor)
        {
            Id = actor.Id;
            X = actor.X;
            Y = actor.Y;
        }
    }

    public sealed class ExpeditionOwnActor
    {
        public ExpeditionVisibleActor Position { get; }
        public long Hp { get; }
        public long MaximumHp { get; }
        public bool Dead { get; }
        public IReadOnlyList<ConditionClause> Conditions { get; }
        public IReadOnlyList<string> HeldItems { get; }
        public IReadOnlyList<ExpeditionVisibleActor> VisibleOpponents { get; }
        public string Travel { get; }
        public ExpeditionTraversalView Traversal { get; }

        internal ExpeditionOwnActor(Snapshot state, ActorState actor, Authority grant)
        {
            Position = new ExpeditionVisibleActor(actor);
            var life = state.Lives.Single(x => x.ActorId == actor.Id);
            Hp = life.Hp;
            MaximumHp = life.MaximumHp;
            Dead = life.Dead;
            Conditions = Array.AsReadOnly(TestOnlyClubAttackPolicy.CombatConditions(state, actor.Id).Active.ToArray());
            HeldItems = Array.AsReadOnly(life.HeldItems.ToArray());
            var roster = state.InventoryCombat ? state.Encounter.Order : Array.Empty<string>();
            VisibleOpponents = Array.AsReadOnly(state.Actors.Where(x => !grant.Controls(x.Id) && roster.Contains(x.Id)
                && roster.Contains(actor.Id) && ObservationRules.CanSee(state, actor.Id, x.Id))
                .Select(x => new ExpeditionVisibleActor(x)).ToArray());
            var edge = state.WorldTraversals.SingleOrDefault(x => x.ActorId == actor.Id);
            Traversal = edge == null ? null : new ExpeditionTraversalView(state, edge);
            Travel = edge == null ? "" : FormattableString.Invariant(
                $"Toward ({edge.ToX}, {edge.ToY}), {edge.DistanceFeet} of 5 feet, {edge.Status}");
        }
    }

    public sealed class ExpeditionTraversalView
    {
        public int FromX { get; }
        public int FromY { get; }
        public int ToX { get; }
        public int ToY { get; }
        public RuleQuantity ExactX { get; }
        public RuleQuantity ExactY { get; }
        public RuleQuantity DistanceFeet { get; }
        public RuleQuantity EdgeFeetRemaining { get; }
        public WorldTraversalStatus Status { get; }
        public string CalendarId { get; }
        public long IntervalIndex { get; }
        public bool PersonalStart { get; }
        public RuleQuantity MovementSpent { get; }
        public RuleQuantity MovementRemaining { get; }

        internal ExpeditionTraversalView(Snapshot state, WorldTraversalRecord edge)
        {
            FromX = edge.FromX; FromY = edge.FromY; ToX = edge.ToX; ToY = edge.ToY;
            var point = WorldPositionResolver.Position(state, edge.ActorId);
            ExactX = point.X; ExactY = point.Y;
            DistanceFeet = edge.DistanceFeet;
            EdgeFeetRemaining = new RuleQuantity(5) - DistanceFeet;
            Status = edge.Status;
            var calendar = WorldTiming.ForActor(state, edge.ActorId);
            PersonalStart = calendar != null;
            if (calendar != null) {
                var interval = state.WorldIntervals.Single(x => x.ActorId == edge.ActorId);
                CalendarId = calendar.Id;
                IntervalIndex = interval.LastStart;
                MovementSpent = interval.MovementSpent;
                MovementRemaining = TestOnlySharedWorldPolicy.Remaining(state, edge.ActorId);
            } else {
                var activity = state.WorldActivityIntervals.Single(x => x.ActorId == edge.ActorId);
                CalendarId = activity.CalendarId;
                IntervalIndex = activity.IntervalIndex;
                MovementSpent = activity.MovementSpent;
                MovementRemaining = TestOnlySharedWorldPolicy.ActivityRemaining(state, edge.ActorId);
            }
        }
    }

    public sealed class ExpeditionOwnedItem
    {
        public string Id { get; }
        public string OwnerId { get; }
        public RuleQuantity? Available { get; }
        public string Placement { get; }
        public bool? Open { get; }

        internal ExpeditionOwnedItem(string id, string ownerId, RuleQuantity? available, string placement, bool? open = null)
        {
            Id = id;
            OwnerId = ownerId;
            Available = available;
            Placement = placement;
            Open = open;
        }
    }

    public sealed class ExpeditionWorkStatus
    {
        public string Id { get; }
        public string ActorId { get; }
        public string Kind { get; }
        public string Status { get; }
        public RuleTime? Remaining { get; }

        internal ExpeditionWorkStatus(string id, string actorId, string kind, string status, RuleTime? remaining = null)
        {
            Id = id;
            ActorId = actorId;
            Kind = kind;
            Status = status;
            Remaining = remaining;
        }
    }

    public sealed class ExpeditionSeatView
    {
        public string Profile => ConnectedExpeditionSession.Profile;
        public bool TestOnly => true;
        public bool Enabled { get; }
        public long Revision { get; }
        public RuleTime Clock { get; }
        public bool InEncounter { get; }
        public ExpeditionTurnSeat NextSeat { get; }
        public ExpeditionDecisionKind PendingDecision { get; }
        public bool OpportunityPending => PendingDecision == ExpeditionDecisionKind.Opportunity;
        public string ActingActorId { get; }
        public string TurnId { get; }
        public string DecisionId { get; }
        public string OpportunityId => OpportunityPending ? DecisionId : "";
        public IReadOnlyList<ExpeditionOwnActor> Actors { get; }
        public IReadOnlyList<ExpeditionOwnedItem> Items { get; }
        public IReadOnlyList<ExpeditionWorkStatus> Work { get; }
        public IReadOnlyList<CommandKind> Commands { get; }
        public IReadOnlyDictionary<CommandKind, string> KnownTargets { get; }
        public long HistoricalSaleCopper { get; }
        public ExpeditionCacheView Cache { get; }
        public ExpeditionObservationView Observation { get; }
        public ExpeditionMiningSiteView MiningSite { get; }
        public ExpeditionFishingTrapView FishingTrap { get; }

        internal ExpeditionSeatView(ExpeditionActionResult position, bool enabled, bool combat, string actorId,
            string turnId, string decisionId, IEnumerable<ExpeditionOwnActor> actors,
            IEnumerable<ExpeditionOwnedItem> items, IEnumerable<ExpeditionWorkStatus> work,
            IEnumerable<CommandKind> commands, IReadOnlyDictionary<CommandKind, string> knownTargets,
            long historicalSaleCopper, ExpeditionCacheView cache = null, ExpeditionObservationView observation = null,
            ExpeditionMiningSiteView miningSite = null, ExpeditionFishingTrapView fishingTrap = null)
        {
            Enabled = enabled;
            Revision = position.Revision;
            Clock = position.Clock;
            InEncounter = combat;
            NextSeat = enabled ? position.NextSeat : ExpeditionTurnSeat.Unavailable;
            PendingDecision = position.PendingDecision;
            ActingActorId = actorId;
            TurnId = turnId;
            DecisionId = decisionId;
            Actors = Array.AsReadOnly(actors.ToArray());
            Items = Array.AsReadOnly(items.ToArray());
            Work = Array.AsReadOnly(work.ToArray());
            Commands = Array.AsReadOnly(commands.ToArray());
            KnownTargets = knownTargets;
            HistoricalSaleCopper = historicalSaleCopper;
            Cache = cache;
            Observation = observation;
            MiningSite = miningSite;
            FishingTrap = fishingTrap;
        }
    }

    public sealed class ExpeditionFishingTrapView
    {
        public string Id { get; }
        public string SiteId { get; }
        public int SiteX { get; }
        public int SiteY { get; }
        public string ReceiverId { get; }
        public int ReceiverX { get; }
        public int ReceiverY { get; }
        public string WorkerId { get; }
        public string AttemptId { get; }
        public RuleTime? SetupLabor { get; }
        public RuleTime? DeployedAt { get; }
        public RuleTime? ScheduledCheckAt { get; }
        public FishingTrapAttemptStatus? SetupStatus { get; }
        public RuleTime? RetrievalLabor { get; }
        public FishingTrapRetrievalStatus? RetrievalStatus { get; }
        public bool ObservedLocally { get; }
        public FishingTrapPhysicalStatus? PhysicalStatus { get; }
        public FishingTrapCheckOutcome? CheckOutcome { get; }
        public string CapturedCreatureId { get; }

        internal ExpeditionFishingTrapView(FishingTrapPhysicalRecord trap, FishingReceiveLocationRecord receiver,
            FishingTrapAttemptRecord attempt, FishingTrapRetrievalRecord retrieval, bool observed)
        {
            Id = trap.TrapId;
            SiteId = trap.SiteId;
            SiteX = ConnectedExpeditionSession.ConnectedTrapProfile.TrapX;
            SiteY = ConnectedExpeditionSession.ConnectedTrapProfile.TrapY;
            ReceiverId = receiver.Id;
            ReceiverX = receiver.X; ReceiverY = receiver.Y;
            WorkerId = ConnectedExpeditionSession.Companion;
            AttemptId = attempt?.Id;
            SetupLabor = attempt?.SetupLabor;
            DeployedAt = attempt?.SetupCompletedAt;
            ScheduledCheckAt = attempt?.CheckDueAt;
            if (attempt?.Status == FishingTrapAttemptStatus.SettingUp || attempt?.Status == FishingTrapAttemptStatus.Paused
                || attempt?.Status == FishingTrapAttemptStatus.Cancelled)
                SetupStatus = attempt.Status;
            RetrievalLabor = retrieval?.WorkDone;
            RetrievalStatus = retrieval?.Status;
            ObservedLocally = observed;
            PhysicalStatus = observed ? trap.Status : (FishingTrapPhysicalStatus?)null;
            CheckOutcome = observed ? attempt?.CheckOutcome : null;
            CapturedCreatureId = observed && attempt?.CapturedCreatureId != "" ? attempt?.CapturedCreatureId : null;
        }
    }

    public sealed class ExpeditionMiningSiteView
    {
        public string Id { get; }
        public string DepositId { get; }
        public string VersionId { get; }
        public int X { get; }
        public int Y { get; }
        public bool ObservedLocally { get; }
        public bool? ClaimClosed { get; }
        public IReadOnlyList<ExpeditionMiningUnitView> Units { get; }

        internal ExpeditionMiningSiteView(MiningDepositRecord deposit, bool observed, bool? claimClosed,
            IEnumerable<ExpeditionMiningUnitView> units)
        {
            Id = deposit.SiteId;
            DepositId = deposit.Id;
            VersionId = deposit.VersionId;
            X = deposit.SiteX;
            Y = deposit.SiteY;
            ObservedLocally = observed;
            ClaimClosed = claimClosed;
            Units = Array.AsReadOnly(units.ToArray());
        }
    }

    public sealed class ExpeditionMiningUnitView
    {
        public string Id { get; }
        public string CategoryId { get; }
        public MiningUnitStatus Status { get; }
        public string RecoveredLotId { get; }

        internal ExpeditionMiningUnitView(MiningMaterialUnitRecord unit)
        {
            Id = unit.Id;
            CategoryId = unit.CategoryId;
            Status = unit.Status;
            RecoveredLotId = unit.ReceivedLotId;
        }
    }

    public sealed class ExpeditionObservationView
    {
        public bool OrdinaryStageOpen { get; }
        public string HiderId => ConnectedExpeditionSession.Hero;
        public string SearcherId => ConnectedExpeditionSession.Companion;
        public string HideStartId { get; }
        public string SearchStartId { get; }
        public IReadOnlyList<ExplorationHideView> HideAttempts { get; }
        public IReadOnlyList<ExplorationSearchView> SearchAttempts { get; }
        public IReadOnlyList<ObservationKnownLocation> HiderKnowledge { get; }
        public IReadOnlyList<ObservationKnownLocation> SearcherKnowledge { get; }

        internal ExpeditionObservationView(bool stageOpen, string hideStartId, string searchStartId,
            IEnumerable<ExplorationHideView> hideAttempts, IEnumerable<ExplorationSearchView> searchAttempts,
            IReadOnlyList<ObservationKnownLocation> hiderKnowledge, IReadOnlyList<ObservationKnownLocation> searcherKnowledge)
        {
            OrdinaryStageOpen = stageOpen;
            HideStartId = hideStartId;
            SearchStartId = searchStartId;
            HideAttempts = Array.AsReadOnly(hideAttempts.ToArray());
            SearchAttempts = Array.AsReadOnly(searchAttempts.ToArray());
            HiderKnowledge = hiderKnowledge;
            SearcherKnowledge = searcherKnowledge;
        }
    }

    public sealed class ExpeditionCacheView
    {
        public string Id { get; }
        public int X { get; }
        public int Y { get; }
        public bool Locked { get; }
        public bool Open { get; }
        public string PickAttemptId { get; }
        public RuleTime? PickDueAt { get; }
        public string StockId { get; }
        public RuleQuantity? AvailablePounds { get; }

        internal ExpeditionCacheView(SupplyCacheRecord cache, SupplyCacheAttemptRecord pick, RuleTime? due,
            RuleQuantity available)
        {
            Id = cache.Id;
            X = cache.X;
            Y = cache.Y;
            Locked = cache.Locked;
            Open = cache.Open;
            PickAttemptId = pick?.Id ?? "";
            PickDueAt = due;
            StockId = available == default ? "" : cache.RationLotId;
            AvailablePounds = available == default ? (RuleQuantity?)null : available;
        }
    }

    public sealed partial class ConnectedExpeditionSession
    {
        private static readonly IReadOnlyDictionary<CommandKind, string> NoKnownTargets =
            new ReadOnlyDictionary<CommandKind, string>(new Dictionary<CommandKind, string>());

        /// <summary>Projects only the granted actors, their resources and jobs, and actual sight of tactical opponents.
        /// Command families and named services are supported inputs. The resolver determines current availability.</summary>
        public ExpeditionSeatView View(ExpeditionSeat seat)
        {
            lock (gate) {
                var state = simulation.Capture();
                var grant = SeatGrant(seat);
                bool player = seat == ExpeditionSeat.Player;
                bool discloseTacticalSlot = grant != null && (player || FirstEncounterActive(state));
                var position = new ExpeditionActionResult(ExpeditionResponse.Waiting, state, discloseTacticalSlot);
                if (grant == null)
                    return new ExpeditionSeatView(position, false, false, "", "", "", Array.Empty<ExpeditionOwnActor>(),
                        Array.Empty<ExpeditionOwnedItem>(), Array.Empty<ExpeditionWorkStatus>(), Array.Empty<CommandKind>(),
                        NoKnownTargets, 0);
                string acting = ActingActor(state, out var decision, out string decisionId);
                string ownedActing = grant.Controls(acting) ? acting : "";
                string ownedDecision = ownedActing != "" ? decisionId : "";
                bool ownsTacticalResponse = ownedActing != "" && (decision == ExpeditionDecisionKind.Opportunity
                    || decision == ExpeditionDecisionKind.Knockout || decision == ExpeditionDecisionKind.Press);
                string turn = state.InventoryCombat && (ownsTacticalResponse || grant.Controls(state.Encounter.CurrentActor))
                    ? state.Encounter.CurrentTurnId : "";
                IEnumerable<CommandKind> commands = player ? CombatCommands.Concat(PartyCommands) : CombatCommands;
                IReadOnlyDictionary<CommandKind, string> targets = player ? KnownServices : NoKnownTargets;
                if (player && state.ConnectedCompanionDose) {
                    commands = commands.Append(CommandKind.BeginReinforcementApproach);
                    var selected = KnownServices.ToDictionary(x => x.Key, x => x.Value);
                    selected.Add(CommandKind.BeginReinforcementApproach, state.Reinforcement.Definition.Id);
                    if (state.ConnectedCompanionStabilization) {
                        commands = commands.Append(CommandKind.StabilizeCompanion);
                        selected.Add(CommandKind.StabilizeCompanion, Companion);
                    }
                    targets = new System.Collections.ObjectModel.ReadOnlyDictionary<CommandKind, string>(selected);
                }
                return new ExpeditionSeatView(position, true, discloseTacticalSlot && state.InventoryCombat,
                    ownedActing, turn, ownedDecision,
                    state.Actors.Where(x => grant.Controls(x.Id)).Select(x => new ExpeditionOwnActor(state, x, grant)),
                    ProjectItems(state, grant), player ? ProjectWork(state, grant) : Array.Empty<ExpeditionWorkStatus>(),
                    commands, targets,
                    player ? state.HavenSales.Where(x => grant.Controls(x.Basis.SellerId)).Sum(x => x.PaymentCopper ?? 0) : 0,
                    player ? ProjectCache(state) : null, player ? ProjectObservation(state, grant) : null,
                    player ? ProjectMiningSite(state, grant) : null,
                    player ? ProjectFishingTrap(state, grant) : null);
            }
        }

        private static ExpeditionFishingTrapView ProjectFishingTrap(Snapshot state, Authority grant)
        {
            if (!grant.Controls(Companion) || !grant.MayUseInventory(Companion)) return null;
            var trap = state.FishingTraps.SingleOrDefault(x => x.TrapId == SharedFishingTrapFixture.TrapId);
            if (trap == null) return null;
            var receiver = state.FishingReceiveLocations.Single(x => x.Id == ConnectedTrapProfile.ReceiverIdentity);
            var attempt = state.FishingTrapAttempts.Where(x => x.TrapId == trap.TrapId && x.SetterId == Companion)
                .OrderByDescending(TestOnlySharedWorldPolicy.FishingTrapCommandSequence).FirstOrDefault();
            var retrieval = state.FishingTrapRetrievals.SingleOrDefault(x => x.AttemptId == attempt?.Id && x.WorkerId == Companion);
            bool observed = CanObserveTrap(state, trap.X, trap.Y);
            return new ExpeditionFishingTrapView(trap, receiver, attempt, retrieval, observed);
        }

        private static ExpeditionMiningSiteView ProjectMiningSite(Snapshot state, Authority grant)
        {
            var deposit = state.MiningDeposits.SingleOrDefault(x => x.Id == SharedMiningFixture.DepositId);
            if (deposit == null || !grant.Controls(deposit.OwnerId) || !grant.MayUseInventory(deposit.OwnerId)) return null;
            var worker = state.Actors.Single(x => x.Id == deposit.OwnerId);
            bool observed = !state.InventoryCombat && !state.WorldTraversals.Any(x => x.ActorId == worker.Id)
                && TestOnlyClubAttackPolicy.Aware(state, worker.Id)
                && !TestOnlyClubAttackPolicy.ConditionsFor(state, worker.Id).View().BlocksSight
                && WorldSpatialQueries.WithinCardinalRange(worker.X, worker.Y, deposit.SiteX, deposit.SiteY, 1);
            var categories = state.MiningCategories.Where(x => x.DepositId == deposit.Id && x.Accessible);
            var units = observed ? state.MiningUnits.Where(x => x.DepositId == deposit.Id && categories.Any(c => c.Id == x.CategoryId))
                .Select(x => new ExpeditionMiningUnitView(x)) : Enumerable.Empty<ExpeditionMiningUnitView>();
            bool? claimClosed = observed ? state.MiningAttempts.Any(x => x.DepositId == deposit.Id) : (bool?)null;
            return new ExpeditionMiningSiteView(deposit, observed, claimClosed, units);
        }

        private ExpeditionObservationView ProjectObservation(Snapshot state, Authority grant)
        {
            bool stageOpen = OrdinaryObservationOpen(state);
            return new ExpeditionObservationView(stageOpen, stageOpen ? HideStartToken(state) : null,
                stageOpen ? SearchStartToken(state) : null,
                state.ExplorationHide.Attempts.Select(x => simulation.ObserveExplorationHide(grant, x.Id)),
                state.ExplorationSearch.Attempts.Select(x => simulation.ObserveExplorationSearch(grant, x.Id)),
                stageOpen ? ObservationRules.KnownLocations(state, Hero) : Array.Empty<ObservationKnownLocation>(),
                stageOpen ? ObservationRules.KnownLocations(state, Companion) : Array.Empty<ObservationKnownLocation>());
        }

        private static ExpeditionCacheView ProjectCache(Snapshot state)
        {
            var cache = ReachableCache(state);
            if (cache == null) return null;
            var pick = state.SupplyCacheAttempts.SingleOrDefault(x => x.CacheId == cache.Id && x.ActorId == Hero
                && x.Status == SupplyCacheAttemptStatus.Working);
            RuleTime? due = pick == null ? (RuleTime?)null
                : state.Work.WorkerIntervals.Single(x => x.JobId == pick.Id && x.WorkerId == Hero).End;
            return new ExpeditionCacheView(cache, pick, due, AvailableCacheRations(state, cache));
        }

        private static IEnumerable<ExpeditionOwnedItem> ProjectItems(Snapshot state, Authority grant)
        {
            foreach (var item in state.PortableEquipment.Where(x => grant.MayUseInventory(x.OwnerId)
                && grant.Controls(x.CustodianId))) {
                if (IsSelectedTrapInventory(state, item.Id) || IsSelectedTrapInventory(state, item.LinkedId)) continue;
                if (item.LinkKind == PortableLinkKind.AlchemyDose) {
                    var linkedDose = state.AlchemyDoses.Single(x => x.Id == item.LinkedId);
                    yield return new ExpeditionOwnedItem(item.Id, item.OwnerId,
                        linkedDose.Spent ? default(RuleQuantity) : new RuleQuantity(1), item.Placement.ToString());
                    continue;
                }
                var lot = state.InventoryLots.FirstOrDefault(x => x.LotId == item.LinkedId && grant.MayUseInventory(x.OwnerId));
                if (lot != null && state.Work.Lots.Any(x => x.Id == lot.LotId && InSelectedCache(x))) continue;
                yield return new ExpeditionOwnedItem(item.Id, item.OwnerId, lot == null ? (RuleQuantity?)null
                    : state.Work.AvailableAmount(lot.LotId), item.Placement.ToString(), item.Open);
            }
            foreach (var item in state.Clubs.Where(x => grant.MayUseInventory(x.OwnerId) && grant.Controls(x.CustodianId)))
                yield return new ExpeditionOwnedItem(item.Id, item.OwnerId, null, item.HeldBy == "" ? "Ground" : "Held");
            foreach (var lot in state.InventoryLots.Where(x => grant.MayUseInventory(x.OwnerId)
                && !IsSelectedTrapInventory(state, x.LotId)
                && !state.PortableEquipment.Any(i => i.Id == x.LotId || i.LinkedId == x.LotId))) {
                if (state.Work.Lots.Any(x => x.Id == lot.LotId && grant.Controls(x.CustodianId) && !InSelectedCache(x)))
                    yield return new ExpeditionOwnedItem(lot.LotId, lot.OwnerId, state.Work.AvailableAmount(lot.LotId),
                        lot.Access.ToString());
            }
            foreach (var dose in state.AlchemyDoses.Where(x => grant.MayUseInventory(x.OwnerId)
                && grant.Controls(x.CustodianId) && !x.Spent && x.Id != ConnectedVialRules.SelectedId(state)))
                yield return new ExpeditionOwnedItem(dose.Id, dose.OwnerId, new RuleQuantity(1), "Dose");
        }

        private static IEnumerable<ExpeditionWorkStatus> ProjectWork(Snapshot state, Authority grant)
        {
            foreach (var job in state.MiningAttempts.Where(x => grant.Controls(x.WorkerId)))
                yield return new ExpeditionWorkStatus(job.Id, job.WorkerId, "Mining", job.Status.ToString());
            foreach (var job in state.Intakes.Where(x => grant.Controls(x.ActorId)))
                yield return new ExpeditionWorkStatus(job.Id, job.ActorId, "Intake", job.Status.ToString());
            foreach (var job in state.HavenAppraisals.Where(x => grant.Controls(x.WorkerId)))
                yield return new ExpeditionWorkStatus(job.Id, job.WorkerId, "Appraisal", job.Status.ToString(), job.Work.Remaining);
            foreach (var job in state.ExpeditionBills.Where(x => grant.Controls(x.WorkerId)))
                yield return new ExpeditionWorkStatus(job.Id, job.WorkerId, "Bill", job.Status.ToString(), job.Work.Remaining);
            foreach (var job in state.HavenSales.Where(x => grant.Controls(x.Basis.SellerId)))
                yield return new ExpeditionWorkStatus(job.Id, job.Basis.SellerId, "Sale", job.Status.ToString(), job.Work.Remaining);
            if (state.CharterAttempt != null && grant.Controls(Hero))
                yield return new ExpeditionWorkStatus(state.CharterAttempt.Id, Hero, "Charter", state.CharterAttempt.Outcome.ToString());
            foreach (var job in state.FormulaWork.Where(x => grant.Controls(x.WorkerId)))
                yield return new ExpeditionWorkStatus(job.Id, job.WorkerId, "Formula", job.Status.ToString(), job.Work.Remaining);
            foreach (var job in state.ManufacturingOrders.Where(x => grant.Controls(x.WorkerId)))
                yield return new ExpeditionWorkStatus(job.Id, job.WorkerId, "Manufacturing", job.Status.ToString(), job.Work.Remaining);
        }
    }
}
#endif
