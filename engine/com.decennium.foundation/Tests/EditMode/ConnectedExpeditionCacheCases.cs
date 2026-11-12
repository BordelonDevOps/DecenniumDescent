#if DECENNIUM_TEST_ONLY && (UNITY_EDITOR || HEADLESS_TESTS)
using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using Decennium.Foundation.Laboratory;

namespace Decennium.Foundation.Tests
{
    public static partial class FoundationCases
    {
        private static void AddConnectedExpeditionCacheCases(Dictionary<string, Action> cases, string directory)
        {
            cases.Add("exp03_session_cache_scope_interrupted_work_and_partial_pickup", () =>
            {
                const ExpeditionSeat player = ExpeditionSeat.Player;
                const ExpeditionSeat director = ExpeditionSeat.FirstOpponent;
                const string hero = ConnectedExpeditionSession.Hero;
                const string companion = ConnectedExpeditionSession.Companion;
                const string ration = TestOnlyInventoryPolicy.FoodId;
                const string cacheId = SupplyCacheFixture.CacheId;
                var session = ConnectedExpeditionSession.Start();
                int input = 0;
                Command Request(CommandKind kind, string target = "", int x = 0, int y = 0,
                    InventoryRequest inventory = null, string actor = hero, CombatRequest combat = null)
                    => new Command("session.cache." + (++input).ToString(System.Globalization.CultureInfo.InvariantCulture),
                        actor, session.View(player).Revision, kind, target, x, y, inventory, combat);
                void Commit(ExpeditionActionResult result)
                    => Require(result.Response == ExpeditionResponse.Committed,
                        "Public cache input failed at revision " + result.Revision + ": " + result.Response);
                Command CacheAction(SupplyCacheInteraction operation, string actor = hero)
                    => Request(CommandKind.Interact, cacheId, (int)operation, actor: actor);
                void Advance(int seconds)
                    => Commit(session.SubmitSessionCommand(Request(CommandKind.AdvanceClock, x: seconds, y: 1)));
                var pickup = new InventoryRequest(new RuleQuantity(2));
                var initial = session.View(player);
                Require(initial.Cache == null && initial.Items.All(x => x.Id != ration)
                    && session.Submit(player, Request(CommandKind.HandleInventory, ration, inventory: pickup)).Response
                        == ExpeditionResponse.Unavailable
                    && session.Submit(player, Request(CommandKind.HandleInventory, "absent", inventory: pickup)).Response
                        == ExpeditionResponse.Unavailable, "Remote or absent stock must be equally unavailable.");

                Commit(session.Submit(player, Request(CommandKind.BeginWorldStep, "walk", x: 1)));
                Advance(2);
                Commit(session.Submit(player, Request(CommandKind.BeginWorldStep, "walk", y: 1)));
                Require(session.View(player).Cache == null
                    && session.Submit(player, CacheAction(SupplyCacheInteraction.PickWithTools)).Response == ExpeditionResponse.Unavailable,
                    "A traversing hero cannot use a stationary cache interaction.");
                Advance(2);
                var closed = session.View(player);
                Require(closed.Cache?.Id == cacheId && closed.Cache.Locked && !closed.Cache.Open
                    && closed.Cache.StockId == "" && closed.Cache.AvailablePounds == null && closed.Items.All(x => x.Id != ration)
                    && session.View(director).Cache == null
                    && session.Submit(director, CacheAction(SupplyCacheInteraction.PickWithTools)).Response == ExpeditionResponse.NotAuthorized
                    && session.Submit(player, CacheAction(SupplyCacheInteraction.PickWithTools, companion)).Response == ExpeditionResponse.Unavailable
                    && session.Submit(player, CacheAction(SupplyCacheInteraction.UnlockWithKey)).Response == ExpeditionResponse.Unavailable
                    && session.Submit(player, CacheAction(SupplyCacheInteraction.Open)).Response == ExpeditionResponse.Unavailable
                    && session.Submit(player, CacheAction(SupplyCacheInteraction.PickWithTools)).Response == ExpeditionResponse.Unavailable,
                    "The locked cache must preserve physical tools, seat, actor, method and stock boundaries.");
                Commit(session.Submit(player, Request(CommandKind.HandlePortableEquipment,
                    closed.Items.Single(x => x.Id == SupplyCacheFixture.ToolsId).Id,
                    inventory: new InventoryRequest(new RuleQuantity(1), handling: HandlingKind.Retrieve))));
                Advance(1);

                var work = session.View(player);
                Commit(session.Submit(player, new Command("session.cache.compatible-mining", companion, work.Revision,
                    CommandKind.StartMining, work.KnownTargets[CommandKind.StartMining],
                    miningSelection: new MiningSelectionRequest(SharedMiningFixture.DepositVersionId, new[] { SharedMiningFixture.CategoryA }))));
                string file = Path.Combine(directory, "int03-cache-interrupted.ddsave");
                var store = new FileSaveStore();
                session.Save(file);
                var beforePick = store.Load(file);
                var firstPick = CacheAction(SupplyCacheInteraction.PickWithTools);
                Commit(session.Submit(player, firstPick));
                var booked = session.View(player);
                Require(booked.Clock == beforePick.RuleClock && booked.Cache.PickAttemptId != ""
                    && booked.Cache.PickDueAt == booked.Clock.AddSeconds(6) && booked.Cache.Locked,
                    "Starting a pick must book the actual due interval without a clock or lock advance.");
                Advance(2);
                Commit(session.Submit(player, CacheAction(SupplyCacheInteraction.Interrupt)));
                session.Save(file);
                var interrupted = store.Load(file);
                var attempt = interrupted.SupplyCacheAttempts.Single();
                var actualWork = interrupted.MiningAttempts.Single();
                Require(attempt.Status == SupplyCacheAttemptStatus.Interrupted && attempt.Natural == 0
                    && interrupted.RuleClock == booked.Clock.AddSeconds(2) && interrupted.RandomState == beforePick.RandomState
                    && interrupted.Work.WorkerIntervals.Single(x => x.JobId == attempt.Id).End == interrupted.RuleClock
                    && interrupted.WorldIntervals.Single(x => x.ActorId == hero).ActionSpent
                    && actualWork.WorkDone == new RuleTime(2) && interrupted.SupplyCaches.Single().Locked,
                    "Interrupt must keep elapsed labor and Action, make no pick draw, and credit concurrent work once.");
                Require(session.Submit(player, CacheAction(SupplyCacheInteraction.PickWithTools)).Response == ExpeditionResponse.Unavailable,
                    "Interrupt must not restore the current Action.");
                session.SetSeatEnabled(player, false);
                Require(session.View(player).Cache == null && session.Submit(player, firstPick).Response == ExpeditionResponse.NotAuthorized,
                    "The current grant must precede duplicate handling and projection.");
                session.SetSeatEnabled(player, true);
                Require(session.Submit(player, firstPick).Response == ExpeditionResponse.Duplicate
                    && session.Submit(player, new Command(firstPick.Id, hero, firstPick.ExpectedRevision,
                        CommandKind.Interact, cacheId, (int)SupplyCacheInteraction.Open)).Response == ExpeditionResponse.CommandIdConflict,
                    "A pick receipt survives interruption without repeating payment.");

                Advance(4);
                for (int retry = 0; retry < 6 && session.View(player).Cache.Locked; retry++) {
                    Commit(session.Submit(player, CacheAction(SupplyCacheInteraction.PickWithTools)));
                    var fresh = session.View(player);
                    Require(fresh.Cache.PickDueAt == fresh.Clock.AddSeconds(6), "A fresh attempt must book its entire interval.");
                    Advance(6);
                }
                Require(!session.View(player).Cache.Locked && !session.View(player).Cache.Open,
                    "The real tool check must unlock without opening.");
                Commit(session.Submit(player, CacheAction(SupplyCacheInteraction.Open)));
                var open = session.View(player).Cache;
                Require(open.Open && open.StockId == ration && open.AvailablePounds == new RuleQuantity(2)
                    && session.Submit(player, Request(CommandKind.PortionInventory, open.StockId,
                        inventory: new InventoryRequest(new RuleQuantity(1)))).Response == ExpeditionResponse.Unavailable
                    && session.Submit(player, Request(CommandKind.StartIntake, open.StockId,
                        inventory: new InventoryRequest(new RuleQuantity(1)))).Response == ExpeditionResponse.Unavailable,
                    "Open cache stock is visible and permits only the selected pickup.");
                var partial = session.Submit(player, Request(CommandKind.HandleInventory, open.StockId,
                    inventory: new InventoryRequest(new RuleQuantity(1, 2))));
                Commit(partial);
                session.Save(file);
                var carried = store.Load(file);
                var child = carried.InventoryLots.Single(x => x.ParentId == ration);
                Require(child.CreatedAmount == new RuleQuantity(1, 2) && child.OwnerId == hero && child.Access == InventoryAccess.Ready
                    && session.View(player).Cache.AvailablePounds == new RuleQuantity(3, 2)
                    && session.View(player).Items.Any(x => x.Id == child.LotId) && session.View(player).Items.All(x => x.Id != ration),
                    "Partial pickup must preserve root remainder and expose the actual carried child.");
                Commit(session.Submit(player, Request(CommandKind.PortionInventory, child.LotId,
                    inventory: new InventoryRequest(new RuleQuantity(1, 4)))));

                session = ConnectedExpeditionSession.Start();
                for (int step = 0; step < 3; step++) {
                    Commit(session.Submit(player, Request(CommandKind.BeginWorldStep, "walk", x: 1)));
                    if (step < 2) Advance(2);
                }
                var firstTurn = session.View(director);
                Commit(session.Submit(director, Request(CommandKind.SelectCombatStance, actor: ConnectedExpeditionSession.FirstOpponent,
                    combat: new CombatRequest(firstTurn.TurnId, stance: (int)CombatStance.Aggressive))));
                Commit(session.Submit(director, Request(CommandKind.TacticalStep, firstTurn.TurnId, x: 3,
                    actor: ConnectedExpeditionSession.FirstOpponent)));
                Commit(session.Submit(director, Request(CommandKind.EndRegularTurn, firstTurn.TurnId,
                    actor: ConnectedExpeditionSession.FirstOpponent)));
                var heroTurn = session.View(player).TurnId;
                Commit(session.Submit(player, Request(CommandKind.SelectCombatStance,
                    combat: new CombatRequest(heroTurn, stance: (int)CombatStance.Aggressive))));
                Commit(session.Submit(player, Request(CommandKind.TacticalStep, heroTurn, x: 1)));
                var reaction = session.View(director);
                if (reaction.OpportunityId != "")
                    Commit(session.Submit(director, Request(CommandKind.RespondOpportunityAttack, reaction.OpportunityId,
                        actor: reaction.ActingActorId, combat: new CombatRequest(reaction.TurnId))));
                Commit(session.Submit(player, Request(CommandKind.TacticalStep, heroTurn, x: 1, y: 1)));
                Commit(session.Submit(player, Request(CommandKind.HandlePortableEquipment, SupplyCacheFixture.ToolsId,
                    inventory: new InventoryRequest(new RuleQuantity(1), handling: HandlingKind.Retrieve))));
                var tactical = session.View(player);
                var position = tactical.Actors.Single(x => x.Position.Id == hero).Position;
                Require(tactical.InEncounter && position.X == 1 && position.Y == 1 && tactical.Cache == null
                    && session.Submit(player, CacheAction(SupplyCacheInteraction.PickWithTools)).Response == ExpeditionResponse.Unavailable,
                    "Even an adjacent hero in actual combat must use the ordinary-session cache boundary.");
            });
        }
    }
}
#endif
