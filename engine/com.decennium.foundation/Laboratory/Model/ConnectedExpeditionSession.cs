#if DECENNIUM_TEST_ONLY && (UNITY_EDITOR || DEVELOPMENT_BUILD || HEADLESS_TESTS)
using System;
using System.Collections.Generic;
using System.Collections.ObjectModel;
using System.Linq;

namespace Decennium.Foundation.Laboratory
{
    public enum ExpeditionSeat { Player, FirstOpponent }
    public enum ExpeditionTurnSeat { None, Player, FirstOpponent, AutomaticDefender, Unavailable }
    public enum ExpeditionDecisionKind { None, Opportunity, ManufacturingQuality, Knockout, Press }
    public enum ExpeditionResponse { Unavailable, NotAuthorized, StaleRevision, CommandIdConflict, Committed, Duplicate, Waiting }

    public sealed class ExpeditionActionResult
    {
        public ExpeditionResponse Response { get; }
        public long Revision { get; }
        public RuleTime Clock { get; }
        public ExpeditionTurnSeat NextSeat { get; }
        public ExpeditionDecisionKind PendingDecision { get; }
        public bool OpportunityPending => PendingDecision == ExpeditionDecisionKind.Opportunity;

        internal ExpeditionActionResult(ExpeditionResponse response, Snapshot state, bool discloseTacticalSlot = true)
        {
            Response = response;
            Revision = state.Revision;
            Clock = state.RuleClock;
            if (!discloseTacticalSlot) {
                NextSeat = ExpeditionTurnSeat.Unavailable;
                return;
            }
            string actor = ConnectedExpeditionSession.ActingActor(state, out var decision, out _);
            PendingDecision = decision;
            NextSeat = ConnectedExpeditionSession.SeatForActor(actor);
        }
    }

    /// <summary>Local TEST_ONLY host for the selected connected recipe-4 scenario.
    /// The embedding application is trusted to bind inputs to seats and control the file operations.</summary>
    public sealed partial class ConnectedExpeditionSession
    {
        public const string Profile = "TEST_ONLY.connected-expedition-recipe4.v1";
        public const string Hero = TestOnlyPolicy.ActorId;
        public const string Companion = TestOnlyPolicy.CompanionId;
        public const string FirstOpponent = AdditionalTacticalActor.Id;
        public const string FirstOpponentPrincipal = "TEST_ONLY.session-first-opponent";
        private const string PlayerPrincipal = "TEST_ONLY.host";
        private const string SessionPrincipal = "TEST_ONLY.session-operator";
        private const string ResearchSource = "research.guild-notes";
        private const string Recipe = "recipe-4";
        private static readonly string[] Party = { Hero, Companion };
        private static readonly string[] FirstOpponentActors = { FirstOpponent };
        private static readonly Authority PlayerGrant = new Authority(PlayerPrincipal, Party, inventoryOwners: Party);
        private static readonly Authority FirstOpponentGrant = new Authority(FirstOpponentPrincipal, FirstOpponentActors,
            inventoryOwners: FirstOpponentActors);
        private static readonly Authority HavenTransactionGrant = new Authority(PlayerPrincipal, new[] { Companion },
            inventoryOwners: new[] { Companion, TestOnlyHavenSaleProfile.BuyerId });
        private static readonly Authority ClockGrant = new Authority(SessionPrincipal, new[] { Hero }, canAdvanceClock: true);
        private static readonly Authority CloseGrant = new Authority(SessionPrincipal, new[] { Hero }, canModifyWorld: true);
        private static readonly Authority DefenderGrant = LaterDefenderController.DefenderAuthority();

        private readonly object gate = new object();
        private readonly TestOnlySharedWorldPolicy policy;
        private readonly FileSaveStore store = new FileSaveStore();
        private readonly HashSet<ExpeditionSeat> revoked = new HashSet<ExpeditionSeat>();
        private Simulation simulation;
        private LaterDefenderController defender;

        private ConnectedExpeditionSession(TestOnlySharedWorldPolicy policy)
        {
            this.policy = policy;
            Adopt(Validate(policy.Initial()));
        }

        public static ConnectedExpeditionSession Start() => new ConnectedExpeditionSession(ExpeditionPolicy());

        public static ConnectedExpeditionSession StartWithFishingTrap()
            => new ConnectedExpeditionSession(ExpeditionPolicy().EnableConnectedFishingTrap(ConnectedTrapProfile));

        public static ConnectedExpeditionSession StartWithCarriedVial()
            => new ConnectedExpeditionSession(ExpeditionPolicy().EnableConnectedCarriedVial());

        public static ConnectedExpeditionSession StartWithStowedVial()
            => new ConnectedExpeditionSession(ExpeditionPolicy().EnableConnectedStowedVial());

        public static ConnectedExpeditionSession StartWithTacticalVial()
            => new ConnectedExpeditionSession(ExpeditionPolicy().EnableConnectedTacticalVial());

        public static ConnectedExpeditionSession StartWithCompanionDose()
            => new ConnectedExpeditionSession(ExpeditionPolicy().EnableConnectedCompanionDose());

        public static ConnectedExpeditionSession StartWithWoundTreatment()
            => new ConnectedExpeditionSession(ExpeditionPolicy().EnableConnectedWoundTreatment());

        public static ConnectedExpeditionSession StartWithCompanionStabilization()
            => new ConnectedExpeditionSession(ExpeditionPolicy().EnableConnectedCompanionStabilization());

        private static TestOnlySharedWorldPolicy ExpeditionPolicy() =>
            new TestOnlySharedWorldPolicy(new PortableKitFixture(), new SharedCombatFixture(enemyHp: 1, seed: 8),
                new SupplyCacheFixture())
                .EnableMining(new SharedMiningFixture())
                .EnableHavenAppraisal(new TestOnlyHavenAppraisalProfile())
                .EnableHavenSale(new TestOnlyHavenSaleProfile())
                .EnableHavenMeal(new TestOnlyHavenMealProfile())
                .EnableExpeditionBill(new TestOnlyExpeditionBillProfile())
                .EnableExpeditionClose(new TestOnlyExpeditionCloseProfile())
                .EnableNextCharterPlan(new TestOnlyNextCharterPlanProfile(reserveWaterStartsCarried: true))
                .EnableNextCharterAgreement(new TestOnlyNextCharterAgreementProfile())
                .EnableCharterAttempt(new TestOnlyCharterAttemptProfile())
                .EnableLaterEncounter()
                .EnableCompanionReinforcement(new TestOnlyReinforcementProfile())
                .EnableLivingOpponentRetreat(new TestOnlyLivingOpponentRetreatProfile())
                .EnablePhysicalReengagement(true, true)
                .EnableSurpriseAwareEntry(SurpriseAwareness.Warned)
                .EnableConnectedExplorationObservation()
                .EnableConnectedFormulaResearch()
                .EnableConnectedBloodSpecimen()
                .EnableConnectedRecipe4Batch()
                .EnableVerifiedPlanningPassage();

        private Simulation Validate(Snapshot state)
            => new Simulation(policy, state, ExecutionProfile.Laboratory, CommandVerification.VerifiedPrefix);

        private void Adopt(Simulation replacement)
        {
            simulation = replacement;
            defender = new LaterDefenderController(replacement, policy);
        }

        public void Save(string path)
        {
            lock (gate) store.Save(path, simulation.Capture());
        }

        public void Restore(string path)
        {
            lock (gate) Adopt(Validate(store.Load(path)));
        }

        public string RecoverBackup(string path)
        {
            lock (gate) {
                Simulation replacement = null;
                string displaced = store.RecoverBackup(path, snapshot => replacement = Validate(snapshot));
                Adopt(replacement);
                return displaced;
            }
        }

        public void SetSeatEnabled(ExpeditionSeat seat, bool enabled)
        {
            if (!Enum.IsDefined(typeof(ExpeditionSeat), seat)) throw new ArgumentOutOfRangeException(nameof(seat));
            lock (gate) {
                if (enabled) revoked.Remove(seat);
                else revoked.Add(seat);
            }
        }

        public ExpeditionActionResult Submit(ExpeditionSeat seat, Command command)
        {
            lock (gate) {
                var state = simulation.Capture();
                var grant = SeatGrant(seat);
                if (grant == null || command == null || !grant.Controls(command.Actor))
                    return new ExpeditionActionResult(ExpeditionResponse.NotAuthorized, state, discloseTacticalSlot: false);
                if (!ExposedCommand(state, seat, command.Kind))
                    return new ExpeditionActionResult(ExpeditionResponse.Unavailable, state,
                        seat == ExpeditionSeat.Player || FirstEncounterActive(state));
                if (seat == ExpeditionSeat.Player && command.Actor == Companion
                    && ((command.Kind == CommandKind.StartHavenSale && command.Target == TestOnlyHavenSaleProfile.OfferVersionId)
                        || (command.Kind == CommandKind.PurchaseHavenMeal && command.Target == TestOnlyHavenMealProfile.OfferVersionId)))
                    grant = HavenTransactionGrant;
                return Execute(state, grant, command, () => KnownTarget(state, seat, command),
                    seat == ExpeditionSeat.Player || FirstEncounterActive(state));
            }
        }

        public ExpeditionActionResult SubmitSessionCommand(Command command)
        {
            lock (gate) {
                var state = simulation.Capture();
                if (command == null || command.Actor != Hero)
                    return new ExpeditionActionResult(ExpeditionResponse.NotAuthorized, state);
                switch (command.Kind) {
                    case CommandKind.AdvanceClock:
                        return Execute(state, ClockGrant, command, () => command.Target == "");
                    case CommandKind.EndFixedEncounter:
                        return Execute(state, CloseGrant, command, () => state.InventoryCombat && command.Target == state.Encounter?.CurrentTurnId);
                    default:
                        return new ExpeditionActionResult(ExpeditionResponse.Unavailable, state);
                }
            }
        }

        public ExpeditionActionResult AdvanceAutomaticDefender()
        {
            lock (gate) {
                var decision = defender.Plan(DefenderGrant);
                var result = defender.Dispatch(DefenderGrant, decision);
                var response = result switch {
                    DefenderDispatchStatus.Committed => ExpeditionResponse.Committed,
                    DefenderDispatchStatus.Duplicate => ExpeditionResponse.Duplicate,
                    DefenderDispatchStatus.Stale => ExpeditionResponse.StaleRevision,
                    DefenderDispatchStatus.Waiting => ExpeditionResponse.Waiting,
                    _ => ExpeditionResponse.Unavailable
                };
                return new ExpeditionActionResult(response, simulation.Capture());
            }
        }

        private Authority SeatGrant(ExpeditionSeat seat)
        {
            if (revoked.Contains(seat)) return null;
            return seat switch {
                ExpeditionSeat.Player => PlayerGrant,
                ExpeditionSeat.FirstOpponent => FirstOpponentGrant,
                _ => null
            };
        }

        private ExpeditionActionResult Execute(Snapshot state, Authority grant, Command command, Func<bool> targetAllowed,
            bool discloseTacticalSlot = true)
        {
            ExpeditionActionResult Respond(ExpeditionResponse response)
                => new ExpeditionActionResult(response, state, discloseTacticalSlot);
            if (!Validation.ValidId(command.Id) || command.Target == null
                || (command.Target != "" && !Validation.ValidId(command.Target)) || !ExposedPayload(state, command))
                return Respond(ExpeditionResponse.Unavailable);
            var previous = state.Receipts.FirstOrDefault(r => r.Principal == grant.Principal && r.Id == command.Id);
            if (previous != null) {
                if (!command.MatchesReceipt(previous)) return Respond(ExpeditionResponse.CommandIdConflict);
                // Retried receipts still pass through the engine with the current grant.
            } else {
                if (command.ExpectedRevision != state.Revision) return Respond(ExpeditionResponse.StaleRevision);
                if (!targetAllowed()) return Respond(ExpeditionResponse.Unavailable);
            }
            var result = simulation.Execute(grant, command);
            if (result.Outcome == Outcome.Committed)
                return new ExpeditionActionResult(ExpeditionResponse.Committed, simulation.Capture(), discloseTacticalSlot);
            return Respond(result.Outcome == Outcome.Duplicate ? ExpeditionResponse.Duplicate : ExpeditionResponse.Unavailable);
        }

        private static bool FirstEncounterActive(Snapshot state)
            => state.InventoryCombat && state.Encounter.Order.Contains(FirstOpponent);

        internal static string ActingActor(Snapshot state, out ExpeditionDecisionKind decision, out string decisionId)
        {
            var attack = state.MeleeAttacks.SingleOrDefault(x => x.Pending);
            if (attack != null) {
                decision = ExpeditionDecisionKind.Knockout;
                decisionId = attack.Id;
                return attack.AttackerId;
            }
            var move = TestOnlyClubAttackPolicy.PendingMove(state);
            if (move != null && move.ResponseIndex < move.Reactors.Count) {
                decision = ExpeditionDecisionKind.Opportunity;
                decisionId = move.Id;
                return move.Reactors[move.ResponseIndex];
            }
            var press = TestOnlyClubAttackPolicy.CurrentPressOffer(state);
            if (press != null) {
                decision = ExpeditionDecisionKind.Press;
                decisionId = press.Id;
                return press.ActorId;
            }
            var quality = state.ManufacturingOrders.FirstOrDefault(x => x.Status == ManufacturingStatus.AwaitingChoice);
            if (quality != null) {
                decision = ExpeditionDecisionKind.ManufacturingQuality;
                decisionId = quality.Id;
                return quality.WorkerId;
            }
            decision = ExpeditionDecisionKind.None;
            decisionId = "";
            return state.InventoryCombat ? state.Encounter.CurrentActor : "";
        }

        internal static ExpeditionTurnSeat SeatForActor(string actor)
        {
            return actor switch {
                Hero => ExpeditionTurnSeat.Player,
                Companion => ExpeditionTurnSeat.Player,
                FirstOpponent => ExpeditionTurnSeat.FirstOpponent,
                TestOnlySharedWorldPolicy.LaterDefenderId => ExpeditionTurnSeat.AutomaticDefender,
                "" => ExpeditionTurnSeat.None,
                _ => ExpeditionTurnSeat.Unavailable
            };
        }

        private static bool ExposedPayload(Snapshot state, Command command)
        {
            if (command.Advancement != null || command.Ranged != null || command.OverwatchRider != OverwatchRider.None
                || command.SuppressionFire != null || command.DefensiveFormation != null || command.ExpeditionAssignment != null
                || command.HarvestSelection != null || command.ProspectingExposure != null || command.RouteMappingWork != null)
                return false;
            if (WoundTreatmentStation.IsCommand(command.Kind))
                return command.X == 0 && command.Y == 0 && command.Inventory == null && command.Combat == null && command.MiningSelection == null;
            if (command.Kind == CommandKind.Hide || command.Kind == CommandKind.Search
                || command.Kind == CommandKind.CancelExplorationHide || command.Kind == CommandKind.CancelExplorationSearch)
                return command.Inventory == null && command.Combat == null && command.MiningSelection == null;
            if (command.Kind == CommandKind.Interact)
                return command.Y == 0 && command.Combat == null && command.MiningSelection == null
                    && (command.Target == SharedFishingTrapFixture.TrapId && command.X == (int)FishingTrapInteraction.Retrieve
                        ? command.Inventory != null && command.Inventory.Amount == default
                            && command.Inventory.Handling == HandlingKind.Retrieve
                        : command.Inventory == null);
            if (command.Kind == CommandKind.HandleInventory)
                return command.X == 0 && command.Y == 0 && command.Combat == null && command.MiningSelection == null
                    && command.Inventory?.Destination == "";
            if (command.Inventory != null) {
                if (command.Kind == CommandKind.UseAlchemyDose)
                    return Party.Contains(command.Inventory.Destination);
                if (state.ConnectedStowedVial && command.Kind == CommandKind.HandlePortableEquipment
                    && command.Inventory.Handling == HandlingKind.Stow)
                    return command.Actor == ConnectedVialRules.CarrierId
                        && command.Target == ConnectedVialRules.SelectedId(state)
                        && command.Inventory.Destination == ConnectedVialRules.PackId;
                if (command.Inventory.Destination != "") return false;
                if (command.Kind == CommandKind.HandlePortableEquipment)
                    return command.Inventory.Handling == HandlingKind.Pickup || command.Inventory.Handling == HandlingKind.Drop
                        || command.Inventory.Handling == HandlingKind.Retrieve;
            }
            return true;
        }

        private static bool ExposedCommand(Snapshot state, ExpeditionSeat seat, CommandKind kind)
            => CombatCommands.Contains(kind) || seat == ExpeditionSeat.Player && (PartyCommands.Contains(kind)
                || state.ConnectedCompanionDose && kind == CommandKind.BeginReinforcementApproach
                || state.ConnectedCompanionStabilization && kind == CommandKind.StabilizeCompanion
                || state.ConnectedWoundTreatment && WoundTreatmentStation.IsCommand(kind));

        private static readonly CommandKind[] CombatCommands = {
            CommandKind.SelectCombatStance, CommandKind.AttackClub, CommandKind.TacticalStep,
            CommandKind.EndRegularTurn, CommandKind.RespondOpportunityAttack, CommandKind.ResolveKnockout,
            CommandKind.RespondPress
        };

        private static readonly IReadOnlyDictionary<CommandKind, string> KnownServices =
            new ReadOnlyDictionary<CommandKind, string>(new Dictionary<CommandKind, string> {
            { CommandKind.BeginWorldStep, "walk" },
            { CommandKind.StartMining, SharedMiningFixture.DepositId },
            { CommandKind.StartHavenAppraisal, TestOnlyHavenAppraisalProfile.DeskId },
            { CommandKind.StartHavenSale, TestOnlyHavenSaleProfile.OfferVersionId },
            { CommandKind.PurchaseHavenMeal, TestOnlyHavenMealProfile.OfferVersionId },
            { CommandKind.StartExpeditionBill, TestOnlyExpeditionBillProfile.BillVersionId },
            { CommandKind.CloseExpeditionEpisode, TestOnlyExpeditionBillProfile.EpisodeId },
            { CommandKind.StartNextCharterPlan, TestOnlyNextCharterPlanProfile.VersionId },
            { CommandKind.AcceptNextCharter, TestOnlyNextCharterAgreementProfile.OfferId },
            { CommandKind.StartCharterAttempt, TestOnlyNextCharterAgreementProfile.CharterId },
            { CommandKind.StartFormulaResearch, ResearchSource },
            { CommandKind.StartManufacturing, Recipe }
        });

        private static readonly CommandKind[] PartyCommands = KnownServices.Keys.Concat(new[] {
            CommandKind.HandlePortableEquipment, CommandKind.OpenPortableContainer, CommandKind.ClosePortableContainer,
            CommandKind.Interact, CommandKind.HandleInventory, CommandKind.PortionInventory, CommandKind.StartIntake,
            CommandKind.InterruptIntake,
            CommandKind.Hide, CommandKind.Search, CommandKind.CancelExplorationHide, CommandKind.CancelExplorationSearch,
            CommandKind.ObserveCharterApproach, CommandKind.StartHarvestPreservationTreatment,
            CommandKind.ResumeFormulaWork, CommandKind.ResolveManufacturingQuality, CommandKind.UseAlchemyDose
        }).ToArray();

        private static SupplyCacheRecord ReachableCache(Snapshot state)
        {
            if (state.InventoryCombat || state.WorldTraversals.Any(x => x.ActorId == Hero)) return null;
            return state.SupplyCaches.SingleOrDefault(x => x.Id == SupplyCacheFixture.CacheId && x.OwnerId == Hero
                && !SupplyCacheRules.Buried(state, x.Id) && TestOnlySharedWorldPolicy.NearCache(state, Hero, x));
        }

        private static bool InSelectedCache(ResourceLot lot) => lot.LocationId == SupplyCacheFixture.CacheId;

        private static bool IsSelectedTrapInventory(Snapshot state, string id)
            => state.FishingTraps.Length != 0
                && (id == SharedFishingTrapFixture.TrapId || id == SharedFishingTrapFixture.BaitLotId);

        private static bool KnownTrapInteraction(Snapshot state, Command command)
        {
            if (command.Actor != Companion || command.Target != SharedFishingTrapFixture.TrapId
                || state.FishingTraps.Length == 0) return false;
            var operation = (FishingTrapInteraction)command.X;
            switch (operation) {
                case FishingTrapInteraction.Set:
                case FishingTrapInteraction.Resume:
                case FishingTrapInteraction.Pause:
                case FishingTrapInteraction.Cancel:
                case FishingTrapInteraction.PauseRetrieval:
                case FishingTrapInteraction.ResumeRetrieval:
                    return true;
                case FishingTrapInteraction.Retrieve:
                    return command.Inventory?.Destination == ConnectedTrapProfile.ReceiverIdentity
                        && CanObserveTrap(state, ConnectedTrapProfile.TrapX, ConnectedTrapProfile.TrapY);
                default:
                    return false;
            }
        }

        internal static readonly SharedFishingTrapFixture ConnectedTrapProfile = new SharedFishingTrapFixture();

        private static bool CanObserveTrap(Snapshot state, int x, int y)
            => !state.InventoryCombat && !state.WorldTraversals.Any(edge => edge.ActorId == Companion)
                && TestOnlyClubAttackPolicy.Aware(state, Companion)
                && !TestOnlyClubAttackPolicy.ConditionsFor(state, Companion).View().BlocksSight
                && TestOnlySharedWorldPolicy.FishingAccessFrom(state, Companion, x, y);

        private static RuleQuantity AvailableCacheRations(Snapshot state, SupplyCacheRecord cache)
        {
            if (cache?.Open != true || !state.Work.Lots.Any(x => x.Id == cache.RationLotId && InSelectedCache(x)
                && x.CustodianId == Hero) || !state.InventoryLots.Any(x => x.LotId == cache.RationLotId
                    && x.OwnerId == Hero && x.Access == InventoryAccess.Ground)) return default;
            return state.Work.AvailableAmount(cache.RationLotId);
        }

        private static bool KnownTarget(Snapshot state, ExpeditionSeat seat, Command command)
        {
            if (state.ConnectedWoundTreatment && WoundTreatmentStation.IsStationId(command.Target)) return false;
            string target = command.Target;
            string actor = command.Actor;
            if (seat == ExpeditionSeat.FirstOpponent && !FirstEncounterActive(state)) return false;
            if (KnownServices.TryGetValue(command.Kind, out var service)) return target == service;
            bool KnownInventory(string owner) => seat == ExpeditionSeat.Player && Party.Contains(owner);
            switch (command.Kind) {
                case CommandKind.Hide:
                    return actor == Hero && OrdinaryObservationOpen(state) && target == HideStartToken(state);
                case CommandKind.Search:
                    return actor == Companion && OrdinaryObservationOpen(state) && target == SearchStartToken(state);
                case CommandKind.CancelExplorationHide:
                    return actor == Hero && target == state.ExplorationHide?.Pending?.Id;
                case CommandKind.CancelExplorationSearch:
                    return actor == Companion && target == state.ExplorationSearch?.Pending?.Id;
                case CommandKind.SelectCombatStance:
                    return state.InventoryCombat && target == "" && command.Combat?.TurnId == state.Encounter?.CurrentTurnId;
                case CommandKind.EndRegularTurn:
                case CommandKind.TacticalStep:
                    return state.InventoryCombat && target == state.Encounter?.CurrentTurnId;
                case CommandKind.AttackClub:
                    return state.InventoryCombat && command.Combat != null && command.Combat.TurnId == state.Encounter?.CurrentTurnId
                        && state.Clubs.Any(x => x.Id == command.Combat.WeaponId && x.OwnerId == actor && x.CustodianId == actor)
                        && state.Encounter.Order.Contains(target) && ObservationRules.CanSee(state, actor, target);
                case CommandKind.RespondOpportunityAttack:
                    var pending = TestOnlyClubAttackPolicy.PendingMove(state);
                    return pending != null && pending.ResponseIndex < pending.Reactors.Count && target == pending.Id
                        && pending.Reactors[pending.ResponseIndex] == actor
                        && (command.Combat?.WeaponId == "" || state.Clubs.Any(x => x.Id == command.Combat?.WeaponId
                            && x.OwnerId == actor && x.CustodianId == actor));
                case CommandKind.ResolveKnockout:
                    return state.MeleeAttacks.Any(x => x.Pending && x.Id == target && x.AttackerId == actor);
                case CommandKind.RespondPress:
                    var offer = TestOnlyClubAttackPolicy.CurrentPressOffer(state);
                    return offer != null && offer.Id == target && offer.ActorId == actor;
                case CommandKind.HandlePortableEquipment:
                case CommandKind.OpenPortableContainer:
                case CommandKind.ClosePortableContainer:
                    return !IsSelectedTrapInventory(state, target)
                        && state.PortableEquipment.Any(x => x.Id == target && KnownInventory(x.OwnerId) && KnownInventory(x.CustodianId)
                        && !state.Work.Lots.Any(lot => lot.Id == x.LinkedId && InSelectedCache(lot)));
                case CommandKind.Interact:
                    if (target == SharedFishingTrapFixture.TrapId)
                        return seat == ExpeditionSeat.Player && KnownTrapInteraction(state, command);
                    var operation = (SupplyCacheInteraction)command.X;
                    return actor == Hero && target == SupplyCacheFixture.CacheId && ReachableCache(state) != null
                        && (operation == SupplyCacheInteraction.PickWithTools || operation == SupplyCacheInteraction.Open
                            || operation == SupplyCacheInteraction.Interrupt);
                case CommandKind.HandleInventory:
                    var cache = ReachableCache(state);
                    return actor == Hero && command.Inventory.Handling == HandlingKind.Pickup
                        && cache?.RationLotId == target && AvailableCacheRations(state, cache) > default(RuleQuantity);
                case CommandKind.PortionInventory:
                case CommandKind.StartIntake:
                    return !IsSelectedTrapInventory(state, target)
                        && state.InventoryLots.Any(x => x.LotId == target && KnownInventory(x.OwnerId))
                        && state.Work.Lots.Any(x => x.Id == target && KnownInventory(x.CustodianId) && !InSelectedCache(x));
                case CommandKind.InterruptIntake:
                    return state.Intakes.Any(x => x.Id == target && x.ActorId == actor);
                case CommandKind.StartWoundTreatment:
                case CommandKind.InterruptWoundTreatment:
                    return state.ConnectedWoundTreatment && seat == ExpeditionSeat.Player && actor == Hero && target == Companion;
                case CommandKind.StabilizeCompanion:
                    return state.ConnectedCompanionStabilization && seat == ExpeditionSeat.Player && actor == Hero && target == Companion;
                case CommandKind.BeginReinforcementApproach:
                    return state.ConnectedCompanionDose && seat == ExpeditionSeat.Player && actor == Companion
                        && target == state.Reinforcement?.Definition.Id;
                case CommandKind.ObserveCharterApproach:
                    return target == state.CharterAttempt?.Id;
                case CommandKind.StartHarvestPreservationTreatment:
                    return target == ConnectedBloodSpecimen.SpecimenId && actor == Companion;
                case CommandKind.ResumeFormulaWork:
                    return state.FormulaWork.Any(x => x.Id == target && x.WorkerId == actor);
                case CommandKind.ResolveManufacturingQuality:
                    return state.ManufacturingOrders.Any(x => x.Id == target && x.WorkerId == actor);
                case CommandKind.UseAlchemyDose:
                    return state.AlchemyDoses.Any(x => x.Id == target && KnownInventory(x.OwnerId) && KnownInventory(x.CustodianId));
                default:
                    return false;
            }
        }

        private static bool OrdinaryObservationOpen(Snapshot state)
            => !state.InventoryCombat && ConnectedExplorationObservation.StageOpen(state);

        private static string HideStartToken(Snapshot state)
        {
            var interval = state.WorldIntervals.SingleOrDefault(x => x.ActorId == Hero);
            if (interval == null || interval.LastStart < 0 || interval.ActionSpent
                || state.ExplorationHide?.Pending != null || state.WorldTraversals.Any(x => x.ActorId == Hero)
                || state.RuleClock != state.WorldSchedule.Start(interval.LastStart)) return null;
            var position = state.Actors.Single(x => x.Id == Hero);
            var definition = state.ExplorationHide.Definition;
            var cell = new ExplorationSearchCell(position.X, position.Y);
            if (!cell.Equals(definition.Recess) && !cell.Equals(definition.Alternate)) return null;
            return state.WorldSchedule.MarkerId(interval.LastStart);
        }

        private static string SearchStartToken(Snapshot state)
        {
            var activity = state.WorldActivityIntervals.SingleOrDefault(x => x.ActorId == Companion);
            if (activity == null || activity.Action != WorldActionCommitment.None
                || state.ExplorationSearch?.Pending != null || state.WorldTraversals.Any(x => x.ActorId == Companion)
                || state.RuleClock != WorldActivityIntervalRecord.StartAt(state.WorldSchedule, activity.IntervalIndex)) return null;
            var position = state.Actors.Single(x => x.Id == Companion);
            if (!state.ExplorationSearch.Definition.Anchor.Equals(new ExplorationSearchCell(position.X, position.Y))) return null;
            return ExplorationSearchRecord.Marker(activity.CalendarId, activity.IntervalIndex);
        }
    }
}
#endif
