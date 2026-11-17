#if DECENNIUM_TEST_ONLY && (UNITY_EDITOR || DEVELOPMENT_BUILD || HEADLESS_TESTS)
using System;
using System.Collections.Generic;
using System.Collections.ObjectModel;
using System.Linq;

namespace Decennium.Foundation.Laboratory
{
    public enum ExpeditionSeat { Player, FirstOpponent, RecoveryOpponent, FerryOpponent }
    public enum ExpeditionTurnSeat { None, Player, FirstOpponent, AutomaticDefender, Unavailable, RecoveryOpponent, FerryOpponent }
    public enum ExpeditionDecisionKind { None, Opportunity, ManufacturingQuality, Knockout, Press, Sanctuary }
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
        private static readonly Authority CastingHandoverGrant = new Authority(PlayerPrincipal, Party, inventoryOwners: Party, willingRecipients: Party);
        private static readonly Authority FirstOpponentGrant = new Authority(FirstOpponentPrincipal, FirstOpponentActors,
            inventoryOwners: FirstOpponentActors);
        private static readonly Authority HavenTransactionGrant = new Authority(PlayerPrincipal, new[] { Companion },
            inventoryOwners: new[] { Companion, TestOnlyHavenSaleProfile.BuyerId });
        private static readonly Authority ClockGrant = new Authority(SessionPrincipal, new[] { Hero }, canAdvanceClock: true);
        private static readonly Authority ClericMilestoneGrant = new Authority(PlayerPrincipal, Party, canModifyWorld: true, inventoryOwners: Party);
        private static readonly Authority CloseGrant = new Authority(SessionPrincipal, new[] { Hero }, canModifyWorld: true);
        private static readonly Authority RecoveryOpponentGrant = new Authority(PostRecoveryEncounterDefinition.Controller,
            new[] { PostRecoveryEncounterDefinition.Actor }, inventoryOwners: new[] { PostRecoveryEncounterDefinition.Actor });
        private static readonly Authority DefenderGrant = LaterDefenderController.DefenderAuthority();

        private readonly object gate = new object();
        private readonly TestOnlySharedWorldPolicy policy;
        private readonly FileSaveStore store = new FileSaveStore();
        private readonly HashSet<ExpeditionSeat> revoked = new HashSet<ExpeditionSeat>();
        private Simulation simulation;
        private LaterDefenderController defender;
        private FerryWraithController ferryController;

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

        public static ConnectedExpeditionSession StartWithConsumeDecay()
            => new ConnectedExpeditionSession(ExpeditionPolicy().EnableConnectedConsumeDecay());

        public static ConnectedExpeditionSession StartWithFleshWarden()
            => new ConnectedExpeditionSession(ExpeditionPolicy().EnableConnectedFleshWarden());

        public static ConnectedExpeditionSession StartWithClericSettlement(ClericInitialSelection initial,
            ClericRepertoireSelection repertoire, ClericMilestoneDeclaration declaration)
            => new ConnectedExpeditionSession(ExpeditionPolicy().EnableConnectedClericSettlement(initial, repertoire, declaration));

        public static ConnectedExpeditionSession StartWithClericCasting(ClericInitialSelection initial,
            ClericRepertoireSelection repertoire, ClericMilestoneDeclaration declaration)
            => new ConnectedExpeditionSession(ExpeditionPolicy().EnableConnectedClericCasting(initial, repertoire, declaration));

        public static ConnectedExpeditionSession StartWithClericLongRest(ClericInitialSelection initial,
            ClericRepertoireSelection repertoire, ClericMilestoneDeclaration declaration)
            => new ConnectedExpeditionSession(ExpeditionPolicy().EnableConnectedClericLongRest(initial, repertoire, declaration));

        public static ConnectedExpeditionSession StartWithPostRecoveryEncounter(ClericInitialSelection initial,
            ClericRepertoireSelection repertoire, ClericMilestoneDeclaration declaration,
            bool companionConsents = true, bool directorAuthorizes = true)
            => new ConnectedExpeditionSession(ExpeditionPolicy().EnablePostRecoveryEncounter(initial,repertoire,declaration,
                companionConsents,directorAuthorizes));

        public static ConnectedExpeditionSession StartWithDeclaredGeometry(ClericInitialSelection initial, ClericRepertoireSelection repertoire,
            ClericMilestoneDeclaration opening, BishopEntryRecord declaration, bool companionConsents = true, bool directorAuthorizes = true)
            => new ConnectedExpeditionSession(ExpeditionPolicy().EnableBishopEntry(initial,repertoire,opening,declaration,
                companionConsents,directorAuthorizes).EnableDeclaredGeometry());

        public static ConnectedExpeditionSession StartWithConsecration(ClericInitialSelection initial,ClericRepertoireSelection repertoire,
            ClericMilestoneDeclaration opening,BishopEntryRecord declaration,bool companionConsents=true,bool directorAuthorizes=true)
            => new ConnectedExpeditionSession(ExpeditionPolicy().EnableBishopEntry(initial,repertoire,opening,declaration)
                .EnableDeclaredGeometry().EnableFerryWraith(companionConsents,directorAuthorizes).EnableConsecration());

        public static ConnectedExpeditionSession StartWithFerryWraith(ClericInitialSelection initial,ClericRepertoireSelection repertoire,
            ClericMilestoneDeclaration opening,BishopEntryRecord declaration,bool companionConsents=true,bool directorAuthorizes=true)
            => new ConnectedExpeditionSession(ExpeditionPolicy().EnableBishopEntry(initial,repertoire,opening,declaration)
                .EnableDeclaredGeometry().EnableFerryWraith(companionConsents,directorAuthorizes));

        public static ConnectedExpeditionSession StartWithBishopEntry(ClericInitialSelection initial, ClericRepertoireSelection repertoire,
            ClericMilestoneDeclaration opening, BishopEntryRecord declaration, bool companionConsents = true, bool directorAuthorizes = true)
            => new ConnectedExpeditionSession(ExpeditionPolicy().EnableBishopEntry(initial,repertoire,opening,declaration,
                companionConsents,directorAuthorizes));

        public static ConnectedExpeditionSession StartWithClericCompanion(ClericInitialSelection selection)
            => new ConnectedExpeditionSession(ExpeditionPolicy().EnableConnectedCleric(selection));

        public static ConnectedExpeditionSession StartWithClericRepertoire(ClericInitialSelection initial, ClericRepertoireSelection repertoire)
            => new ConnectedExpeditionSession(ExpeditionPolicy().EnableConnectedClericRepertoire(initial, repertoire));

        public static ConnectedExpeditionSession StartWithFrightened(ClericInitialSelection initial, ClericRepertoireSelection repertoire)
            => new ConnectedExpeditionSession(ExpeditionPolicy().EnableConnectedFrightened(initial, repertoire));

        public static ConnectedExpeditionSession StartWithShortRest()
            => new ConnectedExpeditionSession(ExpeditionPolicy().EnableConnectedShortRest());

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
            ferryController = new FerryWraithController(replacement, policy);
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
                var grant = SeatCommandGrant(state,seat,command);
                if (grant == null || command == null || !grant.Controls(command.Actor))
                    return new ExpeditionActionResult(ExpeditionResponse.NotAuthorized, state, discloseTacticalSlot: false);
                if (!ExposedCommand(state, seat, command.Kind))
                    return new ExpeditionActionResult(ExpeditionResponse.Unavailable, state,
                        seat == ExpeditionSeat.Player || seat == ExpeditionSeat.FirstOpponent && FirstEncounterActive(state)
                        || seat == ExpeditionSeat.RecoveryOpponent && PostRecoveryProfile.Active(state)
                        || seat == ExpeditionSeat.FerryOpponent && FerryWraithProfile.Active(state));
                if (seat == ExpeditionSeat.Player && command.Actor == Companion
                    && ((command.Kind == CommandKind.StartHavenSale && command.Target == TestOnlyHavenSaleProfile.OfferVersionId)
                        || (command.Kind == CommandKind.PurchaseHavenMeal && command.Target == TestOnlyHavenMealProfile.OfferVersionId)))
                    grant = HavenTransactionGrant;
                if (seat == ExpeditionSeat.Player && state.ConnectedClericSettlement && state.BishopEntry==null && command.Kind == CommandKind.AwardCharacterMilestone)
                    grant = ClericMilestoneGrant;
                return Execute(state, grant, command, () => KnownTarget(state, seat, command),
                    seat == ExpeditionSeat.Player || seat == ExpeditionSeat.FirstOpponent && FirstEncounterActive(state)
                        || seat == ExpeditionSeat.RecoveryOpponent && PostRecoveryProfile.Active(state)
                        || seat == ExpeditionSeat.FerryOpponent && FerryWraithProfile.Active(state));
            }
        }

        public CommandQueryResult QueryCastingCommand(ExpeditionSeat seat,Command command)
        {
            lock(gate) {
                var state=simulation.Capture();var grant=SeatCommandGrant(state,seat,command);
                if(grant==null||command==null||!grant.Controls(command.Actor))return new CommandQueryResult(true,false,"NotAuthorized",state.Revision);
                if(!state.ConnectedClericCasting||!ExposedCommand(state,seat,command.Kind)||!ExposedPayload(state,command)
                    ||!KnownTarget(state,seat,command))return new CommandQueryResult(false,false,"UnsupportedOperation",state.Revision);
                return simulation.QueryCommand(grant,command);
            }
        }

        public IReadOnlyList<CommandOption> DiscoverCastingCommands(ExpeditionSeat seat,string actor)
        {
            lock(gate) {
                var state=simulation.Capture();var grant=SeatGrant(seat);
                if(!state.ConnectedClericCasting||grant==null||!grant.Controls(actor))return Array.AsReadOnly(Array.Empty<CommandOption>());
                var options=simulation.DiscoverCommands(grant,actor).Where(x=>ExposedCommand(state,seat,x.Command.Kind)
                    &&ExposedPayload(state,x.Command)&&KnownTarget(state,seat,x.Command));
                // New-profile candidates use the same narrowly selected host grant as query/submission.
                // Never grant world-modification authority to the whole discovery operation.
                if(state.BishopEntry!=null)options=options.Select(x=>new CommandOption(x.Command,
                    simulation.QueryCommand(SeatCommandGrant(state,seat,x.Command),x.Command)));
                return Array.AsReadOnly(options.ToArray());
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
                var current=simulation.Capture();
                if(FerryWraithProfile.Active(current)) {
                    var grant=SeatGrant(ExpeditionSeat.FerryOpponent);
                    if(grant==null)return new ExpeditionActionResult(ExpeditionResponse.NotAuthorized,current,false);
                    var planned=ferryController.Plan(grant);var dispatched=ferryController.Dispatch(grant,planned);
                    var mapped=dispatched==DefenderDispatchStatus.Committed?ExpeditionResponse.Committed
                        :dispatched==DefenderDispatchStatus.Duplicate?ExpeditionResponse.Duplicate
                        :dispatched==DefenderDispatchStatus.Stale?ExpeditionResponse.StaleRevision
                        :dispatched==DefenderDispatchStatus.Waiting?ExpeditionResponse.Waiting:ExpeditionResponse.Unavailable;
                    return new ExpeditionActionResult(mapped,simulation.Capture());
                }
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

        public FerryDecisionView ObserveFerryDecision(ExpeditionSeat seat)
        {
            lock(gate)return ferryController.Plan(seat==ExpeditionSeat.FerryOpponent?SeatGrant(seat):null).View;
        }

        /// <summary>Trusted host path for a later source reuse. Player seats do not receive this authority.</summary>
        public ExpeditionActionResult SubmitDefenderIntimidatingPresence(Authority grant, Command command)
        {
            lock (gate) {
                var state = simulation.Capture();
                if (!LaterDefenderController.HasGrant(grant) || command?.Actor != FrightenedProfile.Actor)
                    return new ExpeditionActionResult(ExpeditionResponse.NotAuthorized, state, discloseTacticalSlot: false);
                if (!state.ConnectedFrightened || command.Kind != CommandKind.UseIntimidatingPresence)
                    return new ExpeditionActionResult(ExpeditionResponse.Unavailable, state);
                return Execute(state, grant, command, () => command.IntimidatingPresence != null);
            }
        }

        public ExpeditionActionResult SubmitDefenderSanctuary(Authority grant,Command command)
        {
            lock(gate) {
                var state=simulation.Capture();
                if(!LaterDefenderController.HasGrant(grant)||command?.Actor!=TestOnlySharedWorldPolicy.LaterDefenderId)
                    return new ExpeditionActionResult(ExpeditionResponse.NotAuthorized,state,discloseTacticalSlot:false);
                if(!state.ConnectedClericCasting||command.Kind!=CommandKind.RespondSanctuary)
                    return new ExpeditionActionResult(ExpeditionResponse.Unavailable,state);
                return Execute(state,grant,command,()=>TestOnlySharedWorldPolicy.PendingSanctuary(state)?.Id==command.Target);
            }
        }

        private Authority SeatGrant(ExpeditionSeat seat)
        {
            if (revoked.Contains(seat)) return null;
            return seat switch {
                ExpeditionSeat.Player => PlayerGrant,
                ExpeditionSeat.FirstOpponent => FirstOpponentGrant,
                ExpeditionSeat.RecoveryOpponent => simulation?.Capture().PostRecoveryEncounter != null ? RecoveryOpponentGrant : null,
                ExpeditionSeat.FerryOpponent => simulation?.Capture().FerryWraith!=null?FerryWraithController.CreatureAuthority():null,
                _ => null
            };
        }

        private Authority SeatCommandGrant(Snapshot state,ExpeditionSeat seat,Command command)
        {
            var grant=SeatGrant(seat);
            if(grant!=null&&seat==ExpeditionSeat.Player&&state.BishopEntry!=null
                &&command?.Kind==CommandKind.AwardCharacterMilestone&&grant.Controls(command.Actor))
                return ClericMilestoneGrant;
            if(grant!=null&&seat==ExpeditionSeat.Player&&state.ConnectedClericCasting
                &&command?.Inventory?.Handling==HandlingKind.Handover&&Party.Contains(command.Inventory.Destination)
                &&(command.Kind==CommandKind.HandlePortableEquipment&&command.Target==SpellCastingProfile.FocusId
                    ||command.Kind==CommandKind.HandleVessel&&command.Target==TestOnlyFillingPolicy.FlaskId))
                return CastingHandoverGrant;
            return grant;
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
            var sanctuary=TestOnlySharedWorldPolicy.PendingSanctuary(state);
            if(sanctuary!=null) {
                decision=ExpeditionDecisionKind.Sanctuary;decisionId=sanctuary.Id;return sanctuary.ActorId;
            }
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
                PostRecoveryEncounterDefinition.Actor => ExpeditionTurnSeat.RecoveryOpponent,
                FerryWraithProfile.Actor => ExpeditionTurnSeat.FerryOpponent,
                "" => ExpeditionTurnSeat.None,
                _ => ExpeditionTurnSeat.Unavailable
            };
        }

        private static bool ExposedPayload(Snapshot state, Command command)
        {
            if(command.Kind==CommandKind.EncounterDash)return state.FerryWraith!=null&&FerryWraithProfile.DashPayloadValid(command);
            if(command.Kind==CommandKind.UseConsecrate)return state.Consecration!=null&&ConsecrationRules.PayloadValid(command);
            if(command.Kind==CommandKind.TearExposedSeal)return state.FerryWraith!=null&&FerryWraithProfile.SealPayloadValid(command);
            if (BishopProfile.InvocationPayloadFailure(state,command)!=null)return false;
            if (state.DeclaredGeometry != null && (command.Kind == CommandKind.BeginWorldStep
                || command.Kind == CommandKind.SuspendWorldStep || command.Kind == CommandKind.ResumeWorldStep))
                return command.Inventory == null && command.Combat == null && command.Advancement == null
                    && command.Ranged == null && command.OverwatchRider == OverwatchRider.None
                    && command.SuppressionFire == null && command.DefensiveFormation == null && command.ExpeditionAssignment == null
                    && command.HarvestSelection == null && command.MiningSelection == null && command.ProspectingExposure == null
                    && command.RouteMappingWork == null && command.IntimidatingPresence == null && command.HealingRite == null
                    && command.SpellCast == null && command.Guidance == null && command.SanctuaryResponse == null
                    && command.DivineInvocation == null;
            if (command.Advancement != null && (!state.ConnectedClericSettlement || command.Kind != CommandKind.AdvanceCharacterLevel)
                || command.Ranged != null || command.OverwatchRider != OverwatchRider.None
                || command.SuppressionFire != null || command.DefensiveFormation != null || command.ExpeditionAssignment != null
                || command.HarvestSelection != null || command.ProspectingExposure != null || command.RouteMappingWork != null)
                return false;
            if (state.ConnectedClericSettlement && (command.Kind == CommandKind.AwardCharacterMilestone || command.Kind == CommandKind.AdvanceCharacterLevel))
                return command.Actor == ClericRpProfile.Actor && command.X == 0 && command.Y == 0 && command.Inventory == null
                    && command.Combat == null && command.MiningSelection == null && command.IntimidatingPresence == null && command.HealingRite == null;
            if (ClericRepertoireProfile.IsCommand(command.Kind) || command.Kind == CommandKind.UseHealingRite || command.Kind == CommandKind.ConsumeDecay || WoundTreatmentStation.IsCommand(command.Kind) || ShortRestBerth.IsCommand(command.Kind) || ClericLongRestProfile.IsCommand(command.Kind))
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
                if(state.ConnectedClericCasting && (command.Kind==CommandKind.HandlePortableEquipment && command.Target==SpellCastingProfile.FocusId
                    || command.Kind==CommandKind.HandleVessel && command.Target==TestOnlyFillingPolicy.FlaskId))
                    return command.Inventory.Handling==HandlingKind.Handover ? Party.Contains(command.Inventory.Destination)
                        :command.Inventory.Destination=="";
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
            => CombatCommands.Contains(kind)
                || seat==ExpeditionSeat.FerryOpponent&&state.FerryWraith!=null&&(kind==CommandKind.AttackCreatureFeature||kind==CommandKind.RespondSanctuary)
                || seat == ExpeditionSeat.RecoveryOpponent && state.PostRecoveryEncounter != null
                    && (kind == CommandKind.UseIntimidatingPresence || state.ConnectedClericCasting && kind == CommandKind.RespondSanctuary)
                || seat == ExpeditionSeat.Player && (PartyCommands.Contains(kind)
                || state.FerryWraith!=null && kind==CommandKind.EncounterDash
                || state.DeclaredGeometry != null && (kind == CommandKind.SuspendWorldStep || kind == CommandKind.ResumeWorldStep)
                || state.ConnectedClericRepertoire && ClericRepertoireProfile.IsCommand(kind)
                || state.ConnectedClericCasting && (SpellCastingProfile.IsUtilityCommand(kind)
                    || kind==CommandKind.EquipPortableItem || kind==CommandKind.RemovePortableItem || kind==CommandKind.HandleVessel)
                || state.ConnectedClericSettlement && (kind == CommandKind.AwardCharacterMilestone || kind == CommandKind.AdvanceCharacterLevel)
                || (state.ConnectedCompanionDose || state.ConnectedClericRp) && kind == CommandKind.BeginReinforcementApproach
                || state.ConnectedClericRp && (kind == CommandKind.UseHealingRite || ShortRestBerth.IsCommand(kind))
                || state.FerryWraith!=null && kind==CommandKind.TearExposedSeal
                || state.Consecration!=null && kind==CommandKind.UseConsecrate
                || state.BishopEntry!=null && kind==CommandKind.UseDivineInvocation
                || state.ConnectedClericLongRest && (ClericLongRestProfile.IsCommand(kind) || kind == CommandKind.ResolveExpeditionStrainRecovery)
                || (state.ConnectedCompanionStabilization||state.ConnectedClericCasting) && kind == CommandKind.StabilizeCompanion
                || state.ConnectedWoundTreatment && WoundTreatmentStation.IsCommand(kind)
                || state.ConnectedConsumeDecay && kind == CommandKind.ConsumeDecay
                || state.ConnectedShortRest && ShortRestBerth.IsCommand(kind));

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
            if (state.InventoryCombat && !state.ConnectedFrightened || state.WorldTraversals.Any(x => x.ActorId == Hero)) return null;
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
            if (seat == ExpeditionSeat.RecoveryOpponent && !PostRecoveryProfile.Active(state)) return false;
            if (seat == ExpeditionSeat.FerryOpponent && !FerryWraithProfile.Active(state)) return false;
            if (state.DeclaredGeometry != null && command.Kind == CommandKind.BeginWorldStep)
                return seat == ExpeditionSeat.Player && Party.Contains(actor) && (target == "walk" || target == "run");
            if (KnownServices.TryGetValue(command.Kind, out var service)) return target == service;
            bool KnownInventory(string owner) => seat == ExpeditionSeat.Player && Party.Contains(owner);
            switch (command.Kind) {
                case CommandKind.EncounterDash:
                    // Fresh context/turn legality belongs to the shared resolver. Static host
                    // admission lets an authorized exact receipt retry survive a later turn/exit.
                    return state.FerryWraith!=null&&seat==ExpeditionSeat.Player&&Party.Contains(actor);
                case CommandKind.TearExposedSeal:
                    return state.FerryWraith!=null&&seat==ExpeditionSeat.Player&&target==FerryWraithProfile.Seal
                        &&TestOnlySharedWorldPolicy.CanSeeFerrySeal(state,actor);
                case CommandKind.SuspendWorldStep:
                case CommandKind.ResumeWorldStep:
                    return state.DeclaredGeometry != null && seat == ExpeditionSeat.Player && Party.Contains(actor) && target == "";
                case CommandKind.UseConsecrate:
                    return state.Consecration!=null&&seat==ExpeditionSeat.Player&&actor==Companion&&target==""&&command.GetConsecrateRequest()!=null;
                case CommandKind.UseDivineInvocation:
                    return state.BishopEntry!=null&&seat==ExpeditionSeat.Player&&actor==Companion&&target==""
                        &&command.DivineInvocation!=null&&command.DivineInvocation.TargetIds.All(Party.Contains);
                case CommandKind.UseIntimidatingPresence:
                    return seat==ExpeditionSeat.RecoveryOpponent && actor==PostRecoveryEncounterDefinition.Actor
                        && command.IntimidatingPresence!=null && command.IntimidatingPresence.TargetIds.All(Party.Contains);
                case CommandKind.Hide:
                    return state.ConnectedFrightened && seat == ExpeditionSeat.Player && state.InventoryCombat
                        && Party.Contains(actor) && actor == state.Encounter.CurrentActor && target == state.Encounter.CurrentTurnId
                        || actor == Hero && OrdinaryObservationOpen(state) && target == HideStartToken(state);
                case CommandKind.Search:
                    return state.ConnectedFrightened && seat == ExpeditionSeat.Player && state.InventoryCombat
                        && Party.Contains(actor) && actor == state.Encounter.CurrentActor && target == state.Encounter.CurrentTurnId
                        || actor == Companion && OrdinaryObservationOpen(state) && target == SearchStartToken(state);
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
                case CommandKind.AttackCreatureFeature:
                    return seat==ExpeditionSeat.FerryOpponent&&actor==FerryWraithProfile.Actor&&FerryWraithProfile.Active(state)
                        &&command.Combat?.FeatureId==FerryWraithProfile.Feature&&command.Combat.TurnId==state.Encounter.CurrentTurnId
                        &&state.Encounter.Order.Contains(target)&&ObservationRules.CanSee(state,actor,target);
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
                    if(command.Kind==CommandKind.HandlePortableEquipment&&seat==ExpeditionSeat.Player
                        &&SpellCastingProfile.AdmitsCompanionClub(state,target))
                        return actor==ClericRpProfile.Actor&&state.Clubs.Any(x=>x.Id==target
                            &&KnownInventory(x.OwnerId)&&KnownInventory(x.CustodianId));
                    return !IsSelectedTrapInventory(state, target)
                        && state.PortableEquipment.Any(x => x.Id == target && KnownInventory(x.OwnerId) && KnownInventory(x.CustodianId)
                        && !state.Work.Lots.Any(lot => lot.Id == x.LinkedId && InSelectedCache(lot)));
                case CommandKind.EquipPortableItem:
                case CommandKind.RemovePortableItem:
                    return state.ConnectedClericCasting && seat==ExpeditionSeat.Player && target==SpellCastingProfile.FocusId;
                case CommandKind.HandleVessel:
                    return state.ConnectedClericCasting && seat==ExpeditionSeat.Player && target==TestOnlyFillingPolicy.FlaskId;
                case CommandKind.GroundCastingStrain:
                    return state.ConnectedClericCasting && seat==ExpeditionSeat.Player && actor==Companion && target=="";
                case CommandKind.EndSpellConcentration:
                    return state.ConnectedClericCasting && seat==ExpeditionSeat.Player && actor==Companion
                        && state.SpellEffects.Any(x=>x.Id==target && x.CasterId==actor && x.RequiresConcentration && x.Present);
                case CommandKind.FocusDetectedAura:
                    return state.ConnectedClericCasting && seat==ExpeditionSeat.Player && actor==Companion && target.StartsWith("aura.",StringComparison.Ordinal);
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
                case CommandKind.ConsumeDecay:
                    return state.ConnectedConsumeDecay && seat == ExpeditionSeat.Player && actor == Hero && target == ConsumeDecaySite.Id;
                case CommandKind.UseHealingRite:
                    return state.ConnectedClericRp && seat == ExpeditionSeat.Player && actor == Companion && Party.Contains(target);
                case CommandKind.AwardCharacterMilestone:
                case CommandKind.AdvanceCharacterLevel:
                    return state.ConnectedClericSettlement && seat == ExpeditionSeat.Player && actor == Companion
                        && (target == state.ClericMilestone.MilestoneId || state.BishopEntry!=null && target==BishopProfile.Milestone);
                case CommandKind.CastKnownSpell:
                    if(state.ConnectedClericCasting && command.SpellCast!=null)
                        return seat==ExpeditionSeat.Player && actor==Companion
                            && (state.BishopEntry!=null&&command.SpellCast.SpellId==BishopProfile.Dispel?target.StartsWith("aura.",StringComparison.Ordinal)
                                :Party.Contains(target) || target==TestOnlySharedWorldPolicy.LaterDefenderId
                                || state.PostRecoveryEncounter!=null && target==PostRecoveryEncounterDefinition.Actor
                                || state.InventoryLots.Any(x=>x.LotId==target&&Party.Contains(x.OwnerId)));
                    return state.ConnectedClericRepertoire && seat==ExpeditionSeat.Player && actor==Companion && SpellSourceCatalog.Get(target)!=null;
                case CommandKind.RespondSanctuary:
                    return state.ConnectedClericCasting&&(seat==ExpeditionSeat.Player&&Party.Contains(actor)
                        || seat==ExpeditionSeat.RecoveryOpponent&&actor==PostRecoveryEncounterDefinition.Actor
                        || seat==ExpeditionSeat.FerryOpponent&&actor==FerryWraithProfile.Actor)
                        &&state.SanctuaryAdmissions.Any(x=>x.Pending&&x.ActorId==actor&&x.Id==target)
                        &&command.SanctuaryResponse!=null
                        &&(command.SanctuaryResponse.Kind==SanctuaryResponseKind.Forgo||Party.Contains(command.SanctuaryResponse.TargetId)
                            ||command.SanctuaryResponse.TargetId==TestOnlySharedWorldPolicy.LaterDefenderId
                            ||state.PostRecoveryEncounter!=null&&command.SanctuaryResponse.TargetId==PostRecoveryEncounterDefinition.Actor);
                case CommandKind.AcquireEarnedSpell:
                    return state.ConnectedClericRepertoire && seat == ExpeditionSeat.Player && actor == Companion
                        && SpellSourceCatalog.Get(target) != null;
                case CommandKind.BeginLongRest:
                    return state.ConnectedClericLongRest && seat == ExpeditionSeat.Player && actor == Companion && target == ClericLongRestProfile.SiteId;
                case CommandKind.InterruptLongRest:
                    return state.ConnectedClericLongRest && seat == ExpeditionSeat.Player && actor == Companion
                        && state.ClericLongRests.Any(x => x.Id == target);
                case CommandKind.ResolveExpeditionStrainRecovery:
                    return state.ConnectedClericLongRest && seat == ExpeditionSeat.Player && actor == Companion
                        && state.ExpeditionStrainRecoveryOffers.Any(x => x.Pending && x.ActorId == actor && x.PointIds.Contains(target));
                case CommandKind.BeginMutationShortRest:
                    return state.ConnectedFleshWarden && seat == ExpeditionSeat.Player && actor == Hero && FleshWardenProfile.IsMutation(target);
                case CommandKind.BeginShortRest:
                    return (state.ConnectedShortRest || state.ConnectedClericRp) && seat == ExpeditionSeat.Player && actor == Hero && target == ShortRestBerth.Id;
                case CommandKind.InterruptShortRest:
                    return state.ConnectedShortRest && seat == ExpeditionSeat.Player && actor == Hero
                        && state.ShortRests.Any(x => x.Id == target);
                case CommandKind.StartWoundTreatment:
                case CommandKind.InterruptWoundTreatment:
                    return state.ConnectedWoundTreatment && seat == ExpeditionSeat.Player && actor == Hero && target == Companion;
                case CommandKind.StabilizeCompanion:
                    return (state.ConnectedCompanionStabilization||state.ConnectedClericCasting) && seat == ExpeditionSeat.Player && actor == Hero && target == Companion;
                case CommandKind.BeginReinforcementApproach:
                    return (state.ConnectedCompanionDose || state.ConnectedClericRp) && seat == ExpeditionSeat.Player && actor == Companion
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
