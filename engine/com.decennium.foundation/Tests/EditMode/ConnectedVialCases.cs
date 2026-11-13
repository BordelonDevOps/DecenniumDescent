#if DECENNIUM_TEST_ONLY && (UNITY_EDITOR || HEADLESS_TESTS)
using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Reflection;
using Decennium.Foundation.Laboratory;

namespace Decennium.Foundation.Tests
{
    public static partial class FoundationCases
    {
        private const string VialId = "manufacture.order.104.dose0";
        private const string SiblingVialId = "manufacture.order.104.dose1";

        private static ConnectedExpeditionSession StartVialScenario(bool stow = false)
            => StartVialScenario(stow ? ConnectedExpeditionSession.StartWithStowedVial() : ConnectedExpeditionSession.StartWithCarriedVial());

        private static ConnectedExpeditionSession StartVialScenario(ConnectedExpeditionSession session)
        {
            foreach (var input in QualityWalkthrough()) CommitVialRoute(session, input);
            CommitVialRoute(session, new Command("recipe4.batch.106", ConnectedExpeditionSession.Companion, 106,
                CommandKind.ResolveManufacturingQuality, "manufacture.order.104", x: 1));
            CommitVialRoute(session, new Command("i-107", ConnectedExpeditionSession.Companion, 107,
                CommandKind.ClosePortableContainer, ConnectedBloodSpecimen.Vessel));
            return session;
        }

        private static void CommitVialRoute(ConnectedExpeditionSession session, Command command)
        {
            var seat = command.Actor == ConnectedExpeditionSession.FirstOpponent ? ExpeditionSeat.FirstOpponent : ExpeditionSeat.Player;
            var result = command.Kind == CommandKind.AdvanceClock || command.Kind == CommandKind.EndFixedEncounter
                ? session.SubmitSessionCommand(command) : session.Submit(seat, command);
            Require(result.Response == ExpeditionResponse.Committed && result.Revision == command.ExpectedRevision + 1,
                "Carried-vial route did not commit " + command.Id + ": " + result.Response);
        }

        private static Command VialPickup(string id, int revision, long quantity = 1)
            => new Command(id, ConnectedExpeditionSession.Hero, revision, CommandKind.HandlePortableEquipment, VialId,
                inventory: new InventoryRequest(Q(quantity)));

        private static Command VialUse(string id, int revision, string dose = VialId)
            => new Command(id, ConnectedExpeditionSession.Hero, revision, CommandKind.UseAlchemyDose, dose,
                inventory: new InventoryRequest(Q(1), ConnectedExpeditionSession.Hero));

        private static void VialWalk(ConnectedExpeditionSession session, string id, int revision, int x, int seconds = 6)
        {
            CommitVialRoute(session, new Command(id, ConnectedExpeditionSession.Hero, revision, CommandKind.BeginWorldStep, "walk", x: x));
            CommitVialRoute(session, new Command(id + "-paid", ConnectedExpeditionSession.Hero, revision + 1, CommandKind.AdvanceClock, x: seconds, y: 1));
        }

        private static void AddConnectedVialCases(Dictionary<string, Action> cases, string directory)
        {
            cases.Add("mgt01_connected_tactical_packed_vial_two_routes_and_restore", () =>
            {
                const ExpeditionSeat player = ExpeditionSeat.Player;
                const string hero = ConnectedExpeditionSession.Hero;
                const string packId = ConnectedVialRules.PackId;
                var codec = new SnapshotCodec();
                var store = new FileSaveStore();
                var session = StartVialScenario(ConnectedExpeditionSession.StartWithTacticalVial());
                var active = session;
                string branch = "common";
                string PathFor(string point) => Path.Combine(directory, "tactical-vial-" + branch + "-" + point + ".ddsave");
                Snapshot Save(string point)
                {
                    active.Save(PathFor(point));
                    return store.Load(PathFor(point));
                }
                void Restore(string point, Snapshot expected)
                {
                    var restored = ConnectedExpeditionSession.StartWithTacticalVial();
                    restored.Restore(PathFor(point));
                    active = restored;
                    Require(codec.Encode(expected).SequenceEqual(codec.Encode(Save(point + "-restored"))),
                        "Strict restore must preserve " + branch + " " + point + ".");
                }
                void Deny(Snapshot before, Command command, ExpeditionResponse response = ExpeditionResponse.Unavailable,
                    ExpeditionSeat seat = player)
                {
                    Require(active.Submit(seat, command).Response == response
                        && codec.Encode(before).SequenceEqual(codec.Encode(Save(command.Id + "-unchanged"))),
                        "Rejected or retried tactical command changed state: " + command.Id);
                }
                Command Retrieve(string id, long revision, string actor = hero)
                    => new Command(id, actor, revision, CommandKind.HandlePortableEquipment, VialId,
                        inventory: new InventoryRequest(Q(1), handling: HandlingKind.Retrieve));
                Command Open(string id, long revision)
                    => new Command(id, hero, revision, CommandKind.OpenPortableContainer, packId);
                PortableEquipmentRecord Body(Snapshot state) => state.PortableEquipment.Single(x => x.Id == VialId);
                PortableEquipmentRecord Pack(Snapshot state) => state.PortableEquipment.Single(x => x.Id == packId);
                AlchemyDoseRecord Dose(Snapshot state) => state.AlchemyDoses.Single(x => x.Id == VialId);
                WorldIntervalRecord IntervalAt(Snapshot state) => state.WorldIntervals.Single(x => x.ActorId == hero);
                void CheckHandling(Snapshot before, Snapshot after, PortableOperation operation, bool action, int count)
                {
                    var entry = after.PortableHandling.Last();
                    var original = PortableEquipmentRules.CarriedBurden(before, hero);
                    var final = PortableEquipmentRules.CarriedBurden(after, hero);
                    Require(entry.Operation == operation && entry.Revision == after.Revision && entry.ActorId == hero
                        && entry.Tactical && entry.StartedAt == before.RuleClock && entry.EndedAt == before.RuleClock
                        && after.RuleClock == before.RuleClock && after.RandomState == before.RandomState
                        && after.Work.WorkerIntervals.Count == before.Work.WorkerIntervals.Count
                        && after.Encounter.CurrentTurnId == before.Encounter.CurrentTurnId
                        && after.InventoryInteractions == count && IntervalAt(after).Interactions == count
                        && IntervalAt(after).ActionSpent == action && final.Pounds == original.Pounds && final.Load == original.Load,
                        "Tactical handling must charge exactly the owning turn ledger and conserve time, RNG, and burden.");
                }

                VialWalk(active, "vial.approach", 108, 1);
                CommitVialRoute(active, VialPickup("vial.pickup", 110));
                CommitVialRoute(active, new Command("vial.stow", hero, 111, CommandKind.HandlePortableEquipment, VialId,
                    inventory: new InventoryRequest(Q(1), packId, HandlingKind.Stow)));
                var common = Save("packed");
                foreach (bool closed in new[] { true, false }) {
                    branch = "common";
                    Restore("packed", common);
                    branch = closed ? "closed" : "open";
                    if (closed) CommitVialRoute(active, new Command("tactical-vial.ordinary-close", hero, 112,
                        CommandKind.ClosePortableContainer, packId));
                    int departure = closed ? 113 : 112;
                    VialWalk(active, "tactical-vial.away", departure, -1);
                    VialWalk(active, "tactical-vial.entry", departure + 2, -1, 12);
                    var entered = Save("entry");
                    Require(entered.WireSchemaVersion == 98 && entered.SchemaVersion == 90 && entered.InventoryCombat
                        && entered.Encounter.CurrentActor == hero && entered.Actors.Single(x => x.Id == hero).X == 0
                        && Body(entered).ParentId == packId && Pack(entered).Open != closed
                        && entered.InventoryInteractions == 0 && !IntervalAt(entered).ActionSpent,
                        "Both real routes must enter remote combat with the exact packed vial and a fresh regular turn.");
                    Restore("entry", entered);
                    var old = ConnectedExpeditionSession.StartWithStowedVial();
                    Throws<ArgumentException>(() => old.Restore(PathFor("entry")));
                    Require(old.View(player).Revision == 0, "Wire97 must reject a genuine wire98 save atomically.");
                    int revision = checked((int)entered.Revision);
                    Deny(entered, Retrieve("tactical-vial.wrong-seat", revision), ExpeditionResponse.NotAuthorized, ExpeditionSeat.FirstOpponent);
                    Deny(entered, Retrieve("tactical-vial.wrong-actor", revision, ConnectedExpeditionSession.Companion));
                    Deny(entered, VialUse("tactical-vial.contained-use", revision));
                    if (closed) {
                        Deny(entered, Retrieve("tactical-vial.closed-retrieve", revision));
                        var open = Open("tactical-vial.open", revision);
                        CommitVialRoute(active, open);
                        var opened = Save("opened");
                        CheckHandling(entered, opened, PortableOperation.Open, false, 1);
                        Require(Pack(opened).Open && Body(opened).ParentId == packId && !Dose(opened).Spent
                            && Body(opened).HeldHands == 0 && Dose(opened).LocationId == packId,
                            "Opening the pack changes access only.");
                        Restore("opened", opened);
                        Deny(opened, open, ExpeditionResponse.Duplicate);
                        active.SetSeatEnabled(player, false);
                        Deny(opened, open, ExpeditionResponse.NotAuthorized);
                        active.SetSeatEnabled(player, true);
                        Deny(opened, Open(open.Id, opened.Revision), ExpeditionResponse.CommandIdConflict);
                        Deny(opened, Retrieve("tactical-vial.stale", revision), ExpeditionResponse.StaleRevision);
                        Deny(opened, VialUse("tactical-vial.open-contained-use", ++revision));
                    }

                    var beforeRetrieve = Save("before-retrieve");
                    // Detached probes exercise the real resolver with one imposed control state.
                    // These copies are neither executed gameplay nor eligible for restoration.
                    var policy = (TestOnlySharedWorldPolicy)typeof(ConnectedExpeditionSession)
                        .GetField("policy", BindingFlags.Instance | BindingFlags.NonPublic).GetValue(active);
                    var resolve = typeof(TestOnlySharedWorldPolicy).GetMethod("ResolvePortableEquipment",
                        BindingFlags.Instance | BindingFlags.NonPublic);
                    var spent = beforeRetrieve.Copy();
                    spent.WorldIntervals = spent.WorldIntervals.Select(x => x.ActorId == hero ? x.PayAction() : x).ToArray();
                    var spentResult = (string)resolve.Invoke(policy, new object[] { spent, Retrieve("probe.spent", revision) });
                    Require(closed ? spentResult == "ActionAlreadySpent"
                        : spentResult == null && spent.InventoryInteractions == 1 && IntervalAt(spent).ActionSpent,
                        "A spent Action prohibits a second interaction and preserves an available free one.");
                    var fullHands = beforeRetrieve.Copy();
                    var extraHeld = new PortableEquipmentRecord("probe.held-shield", "armor-and-shields.shield",
                        hero, hero, "", PortablePlacement.Carried, PortableLinkKind.None, "", PortableMassBasis.Fixed,
                        Q(6), Q(6), wearable: true, heldHands: 1);
                    fullHands.PortableEquipment = fullHands.PortableEquipment.Append(extraHeld).ToArray();
                    Require((string)resolve.Invoke(policy, new object[] { fullHands, Retrieve("probe.hands", revision) })
                        == "HandlingHandRequired", "Retrieval must require a genuinely free hand.");

                    var retrieve = Retrieve("tactical-vial.retrieve", revision++);
                    CommitVialRoute(active, retrieve);
                    var retrieved = Save("retrieved");
                    CheckHandling(beforeRetrieve, retrieved, PortableOperation.Retrieve, closed, closed ? 2 : 1);
                    Require(Body(retrieved).ParentId == "" && Body(retrieved).HeldHands == 1
                        && Body(retrieved).OwnerId == ConnectedExpeditionSession.Companion
                        && Body(retrieved).CustodianId == hero && Dose(retrieved).LocationId == hero
                        && retrieved.AlchemyDoses.Single(x => x.Id == SiblingVialId).LocationId
                            == entered.AlchemyDoses.Single(x => x.Id == SiblingVialId).LocationId,
                        "Tactical retrieval must hold the one existing dose and leave sibling output where it was.");
                    Restore("retrieved", retrieved);
                    Deny(retrieved, retrieve, ExpeditionResponse.Duplicate);
                    if (closed) {
                        var forged = retrieved.Copy();
                        forged.InventoryInteractions = 1;
                        forged.WorldIntervals = forged.WorldIntervals.Select(x => x.ActorId == hero
                            ? new WorldIntervalRecord(hero, x.LastStart, x.MovementSpent,
                                reactionAvailable: x.ReactionAvailable, interactions: 1) : x).ToArray();
                        try {
                            store.Save(PathFor("forged-spending"), forged);
                            Throws<ArgumentException>(() => active.Restore(PathFor("forged-spending")));
                        }
                        catch (ArgumentException) {
                            // Core validation may reject before strict history replay receives the forged record.
                        }
                        Require(codec.Encode(retrieved).SequenceEqual(codec.Encode(Save("forged-spending-unchanged"))),
                            "Forged tactical spending must not alter the live restored state.");
                        Deny(retrieved, VialUse("tactical-vial.action-spent", revision));
                        CommitVialRoute(active, new Command("tactical-vial.stance", hero, revision++, CommandKind.SelectCombatStance,
                            combat: new CombatRequest(retrieved.Encounter.CurrentTurnId, stance: 1)));
                        CommitVialRoute(active, new Command("tactical-vial.end-first", hero, revision, CommandKind.EndRegularTurn,
                            retrieved.Encounter.CurrentTurnId));
                        var defender = Save("defender-turn");
                        Deny(defender, VialUse("tactical-vial.wrong-turn", checked((int)defender.Revision)));
                        for (int i = 0; i < 12 && active.View(player).ActingActorId != hero; i++)
                            Require(active.AdvanceAutomaticDefender().Response == ExpeditionResponse.Committed,
                                "Actual intervening defender decisions must progress.");
                        revision = checked((int)active.View(player).Revision);
                    }
                    var ready = Save("ready-to-use");
                    Require(ready.Encounter.CurrentActor == hero && !IntervalAt(ready).ActionSpent,
                        "Drinking must await a real available Action.");
                    var use = VialUse("tactical-vial.drink", revision);
                    CommitVialRoute(active, use);
                    var used = Save("used");
                    Require(Dose(used).Spent && Dose(used).FirstD4 >= 1 && Dose(used).SecondD4 >= 1
                        && Body(used).HeldHands == 1 && IntervalAt(used).ActionSpent
                        && used.RuleClock == ready.RuleClock && used.RandomState != ready.RandomState,
                        "The held vial uses the existing Action and real dose resolution.");
                    Restore("used", used);
                    Deny(used, use, ExpeditionResponse.Duplicate);
                }
            });
            cases.Add("mgt01_connected_stowed_vial_paid_hand_transitions_and_restore", () =>
            {
                const ExpeditionSeat player = ExpeditionSeat.Player;
                const string hero = ConnectedExpeditionSession.Hero;
                const string pack = ConnectedVialRules.PackId;
                var session = StartVialScenario(stow: true);
                var codec = new SnapshotCodec();
                var store = new FileSaveStore();
                Snapshot Save(ConnectedExpeditionSession active, string point)
                {
                    string file = Path.Combine(directory, "stow-" + point + ".ddsave");
                    active.Save(file);
                    return store.Load(file);
                }
                Command Handle(string id, long revision, HandlingKind kind, string destination = "")
                    => new Command(id, hero, revision, CommandKind.HandlePortableEquipment, VialId,
                        inventory: new InventoryRequest(Q(1), destination, kind));
                PortableEquipmentRecord Body(Snapshot state) => state.PortableEquipment.Single(x => x.Id == VialId);
                PortableEquipmentRecord Pack(Snapshot state) => state.PortableEquipment.Single(x => x.Id == pack);
                bool Same(Snapshot first, Snapshot second) => codec.Encode(first).SequenceEqual(codec.Encode(second));
                bool SameBurden(Snapshot first, Snapshot second)
                {
                    var before = PortableEquipmentRules.CarriedBurden(first, hero);
                    var after = PortableEquipmentRules.CarriedBurden(second, hero);
                    return before.Pounds == after.Pounds && before.Load == after.Load;
                }
                VialWalk(session, "vial.approach", 108, 1);
                CommitVialRoute(session, VialPickup("vial.pickup", 110));
                var held = Save(session, "held");
                var stow = Handle("vial.stow", 111, HandlingKind.Stow, pack);
                Require(session.Submit(ExpeditionSeat.FirstOpponent, stow).Response == ExpeditionResponse.NotAuthorized
                    && session.Submit(player, Handle("vial.wrong-pack", 111, HandlingKind.Stow, "TEST_ONLY.actor-pouch"))
                        .Response == ExpeditionResponse.Unavailable
                    && Same(held, Save(session, "stow-rejected")), "Only the current owner grant and exact pack may stow.");
                CommitVialRoute(session, stow);
                var stowed = Save(session, "contained");
                var contained = Body(stowed);
                var dose = stowed.AlchemyDoses.Single(x => x.Id == VialId);
                Require(stowed.WireSchemaVersion == 97 && stowed.SchemaVersion == 90
                    && contained.Placement == PortablePlacement.Contained && contained.HeldHands == 0 && contained.ParentId == pack
                    && dose.CustodianId == hero && dose.LocationId == pack && dose.OwnerId == ConnectedExpeditionSession.Companion
                    && SameBurden(held, stowed) && stowed.RuleClock == held.RuleClock.AddSeconds(1)
                    && Pack(held).FitMemberIds.SequenceEqual(Pack(stowed).FitMemberIds)
                    && stowed.Clubs.Count(x => x.HeldBy == hero) == 1,
                    "Stow must use the already occupied hand, keep one body, and pay one second.");
                Require(session.Submit(player, stow).Response == ExpeditionResponse.Duplicate
                    && session.Submit(player, new Command(stow.Id, hero, 111, stow.Kind, stow.Target, x: 1, inventory: stow.Inventory))
                        .Response == ExpeditionResponse.CommandIdConflict
                    && session.Submit(player, VialUse("vial.stowed-direct", 112)).Response == ExpeditionResponse.Unavailable
                    && Same(stowed, Save(session, "stow-retries")), "Retries and direct use must preserve contained state.");

                CommitVialRoute(session, new Command("vial.stow-close", hero, 112, CommandKind.ClosePortableContainer, pack));
                VialWalk(session, "vial.stow-away", 113, -1);
                var away = Save(session, "away");
                Require(!Pack(away).Open && Body(away).ParentId == pack && away.Actors.Single(x => x.Id == hero).X == 1,
                    "The hero must reach actual ordinary ground beyond the bench with a closed pack.");
                var restored = ConnectedExpeditionSession.StartWithStowedVial();
                restored.Restore(Path.Combine(directory, "stow-away.ddsave"));
                Require(Same(away, Save(restored, "away-restored")), "Authentic contained restore must preserve full bytes.");
                var legacy = ConnectedExpeditionSession.StartWithCarriedVial();
                Throws<ArgumentException>(() => legacy.Restore(Path.Combine(directory, "stow-away.ddsave")));
                Require(legacy.View(player).Revision == 0, "Wire96 must reject wire97 atomically.");

                var unselected = away.Copy();
                unselected.ConnectedStowedVial = false;
                Throws<ArgumentException>(() => codec.Encode(unselected));
                var wrongParent = away.Copy();
                wrongParent.PortableEquipment = wrongParent.PortableEquipment.Select(x => x.Id == VialId
                    ? x.With(parentId: "TEST_ONLY.actor-pouch") : x).ToArray();
                wrongParent.AlchemyDoses = wrongParent.AlchemyDoses.Select(x => x.Id == VialId
                    ? x.WithPlacement(hero, "TEST_ONLY.actor-pouch") : x).ToArray();
                Throws<ArgumentException>(() => codec.Encode(wrongParent));

                // These isolated probes do not execute or install a gameplay history.
                var dropEquipment = typeof(TestOnlyClubAttackPolicy).GetMethod("DropConditionEquipment",
                    BindingFlags.Static | BindingFlags.NonPublic);
                var drop = away.Copy();
                dropEquipment.Invoke(null, new object[] { drop, hero });
                Require(Body(drop).ParentId == pack && Body(drop).HeldHands == 0
                    && drop.AlchemyDoses.Single(x => x.Id == VialId).LocationId == pack,
                    "Mandatory held-item drop must leave the contained vial in the pack.");
                var policy = (TestOnlySharedWorldPolicy)typeof(ConnectedExpeditionSession)
                    .GetField("policy", BindingFlags.Instance | BindingFlags.NonPublic).GetValue(session);
                var openCombat = away.Copy();
                openCombat.PortableEquipment = openCombat.PortableEquipment.Select(x => x.Id == pack ? x.With(open: true) : x).ToArray();
                // A genuine remote encounter supplies the tactical shape for a detached access-only probe below.

                foreach (var active in new[] { session, restored }) {
                    Require(active.Submit(player, Handle("vial.closed-retrieve", 115, HandlingKind.Retrieve))
                        .Response == ExpeditionResponse.Unavailable && Same(away, Save(active, "closed-rejected")),
                        "Closed pack retrieval must fail without paying time.");
                    CommitVialRoute(active, new Command("vial.reopen", hero, 115, CommandKind.OpenPortableContainer, pack));
                    var reopened = Save(active, "reopened");
                    Require(Pack(reopened).Open && Body(reopened).ParentId == pack
                        && reopened.RuleClock == away.RuleClock.AddSeconds(1), "Reopening must pay separately and preserve containment.");
                    var retrieve = Handle("vial.retrieve", 116, HandlingKind.Retrieve);
                    CommitVialRoute(active, retrieve);
                    var retrieved = Save(active, "retrieved");
                    Require(Body(retrieved).ParentId == "" && Body(retrieved).HeldHands == 1
                        && retrieved.AlchemyDoses.Single(x => x.Id == VialId).LocationId == hero
                        && SameBurden(reopened, retrieved) && retrieved.RuleClock == reopened.RuleClock.AddSeconds(1)
                        && active.Submit(player, retrieve).Response == ExpeditionResponse.Duplicate,
                        "Retrieve must restore one held hand after one second without changing burden.");
                    VialWalk(active, "vial.entry", 117, -1, 12);
                    var remote = Save(active, "remote");
                    var inaccessible = remote.Copy();
                    inaccessible.PortableEquipment = inaccessible.PortableEquipment.Select(x => x.Id == VialId
                        ? Body(openCombat) : x).ToArray();
                    inaccessible.AlchemyDoses = inaccessible.AlchemyDoses.Select(x => x.Id == VialId
                        ? x.WithPlacement(hero, pack) : x).ToArray();
                    var useMethod = typeof(TestOnlySharedWorldPolicy).GetMethod("UseAlchemy", BindingFlags.Instance | BindingFlags.NonPublic);
                    Require((string)useMethod.Invoke(policy, new object[] { inaccessible, VialUse("vial.open-contained-probe", 119), true })
                        == "AlchemyDoseOutOfReach", "The held-dose access assessment must reject an open contained vial on a legal turn.");
                    CommitVialRoute(active, VialUse("vial.remote-use", 119));
                    var used = Save(active, active == session ? "used" : "used-restored");
                    Require(used.AlchemyDoses.Single(x => x.Id == VialId).Spent && Body(used).HeldHands == 1
                        && used.Actors.Single(x => x.Id == hero).X == 0, "The same retrieved dose must be used remotely.");
                }
                Require(File.ReadAllBytes(Path.Combine(directory, "stow-used.ddsave"))
                    .SequenceEqual(File.ReadAllBytes(Path.Combine(directory, "stow-used-restored.ddsave"))),
                    "Restored and uninterrupted routes must use the same vial with identical canonical output.");
            });

            cases.Add("mgt01_connected_finished_vial_carry_remote_use_and_restore", () =>
            {
                const ExpeditionSeat player = ExpeditionSeat.Player;
                const string hero = ConnectedExpeditionSession.Hero;
                const string companion = ConnectedExpeditionSession.Companion;
                var session = StartVialScenario();
                var store = new FileSaveStore();
                Snapshot Saved(ConnectedExpeditionSession active, string name)
                {
                    string file = Path.Combine(directory, name + ".ddsave");
                    active.Save(file);
                    return store.Load(file);
                }
                var codec = new SnapshotCodec();
                var settled = Saved(session, "vial-settled");
                var vial = settled.PortableEquipment.Single(x => x.Id == VialId);
                Require(settled.WireSchemaVersion == 96 && settled.SchemaVersion == 90 && settled.AlchemyDoses.Length == 6
                    && vial.LinkKind == PortableLinkKind.AlchemyDose && vial.LinkedId == VialId && vial.OwnerId == companion
                    && vial.Placement == PortablePlacement.Ground && vial.GroundX == 3 && vial.GroundY == 3
                    && !settled.InventoryLots.Any(x => x.LotId == VialId) && !settled.Work.Lots.Any(x => x.Id == VialId)
                    && session.View(player).Items.Count(x => x.Id == VialId) == 1
                    && !session.View(ExpeditionSeat.FirstOpponent).Items.Any(x => x.Id == VialId),
                    "The real order must expose one authorized physical body and no second lot.");
                var reject = VialPickup("vial.out-of-reach", 108);
                Require(session.Submit(ExpeditionSeat.FirstOpponent, reject).Response == ExpeditionResponse.NotAuthorized
                    && session.Submit(player, reject).Response == ExpeditionResponse.Unavailable
                    && codec.Encode(settled).SequenceEqual(codec.Encode(Saved(session, "vial-remote-pickup-rejected"))),
                    "Wrong seat and distant pickup must leave the complete state unchanged.");

                VialWalk(session, "vial.approach", 108, 1);
                var atBench = Saved(session, "vial-before-pickup");
                var beforeBurden = PortableEquipmentRules.CarriedBurden(atBench, hero);
                var pickup = VialPickup("vial.pickup", 110);
                Require(session.Submit(player, VialPickup("vial.stale", 109)).Response == ExpeditionResponse.StaleRevision
                    && session.Submit(player, VialPickup("vial.malformed", 110, 2)).Response == ExpeditionResponse.Unavailable
                    && codec.Encode(atBench).SequenceEqual(codec.Encode(Saved(session, "vial-invalid-pickup"))),
                    "Stale and malformed pickup must remain atomic.");

                CommitVialRoute(session, pickup);
                var picked = Saved(session, "vial-picked");
                var carried = picked.PortableEquipment.Single(x => x.Id == VialId);
                var dose = picked.AlchemyDoses.Single(x => x.Id == VialId);
                var sibling = picked.AlchemyDoses.Single(x => x.Id == SiblingVialId);
                var afterBurden = PortableEquipmentRules.CarriedBurden(picked, hero);
                Require(picked.RuleClock == atBench.RuleClock.AddSeconds(1) && carried.Placement == PortablePlacement.Carried
                    && carried.HeldHands == 1 && carried.ParentId == "" && dose.OwnerId == companion && dose.MakerId == companion
                    && dose.CustodianId == hero && dose.LocationId == hero && sibling.LocationId == "TEST_ONLY.prepared-plot"
                    && afterBurden.Pounds == beforeBurden.Pounds + new RuleQuantity(1, 5)
                    && afterBurden.Load == beforeBurden.Load + new RuleQuantity(1, 50)
                    && picked.Clubs.Count(x => x.HeldBy == hero) == 1,
                    "Pickup must pay one second and add exactly the one held vial while preserving title and sibling access.");
                Require(session.Submit(player, pickup).Response == ExpeditionResponse.Duplicate
                    && session.Submit(player, VialPickup(pickup.Id, 110, 2)).Response == ExpeditionResponse.CommandIdConflict
                    && session.Submit(player, VialPickup("vial.already-picked", 111)).Response == ExpeditionResponse.Unavailable
                    && codec.Encode(picked).SequenceEqual(codec.Encode(Saved(session, "vial-pickup-retries"))),
                    "Retry, conflict and fresh pickup of an already carried vial must leave the state unchanged.");

                VialWalk(session, "vial.return", 111, -1);
                VialWalk(session, "vial.entry", 113, -1, 12);
                var remote = Saved(session, "vial-remote");
                var actor = remote.Actors.Single(x => x.Id == hero);
                Require(remote.InventoryCombat && remote.Encounter.CurrentActor == hero && actor.X == 0 && actor.Y == 3,
                    "The hero must reach the actual later turn beyond workshop reach.");
                var copy = ConnectedExpeditionSession.StartWithCarriedVial();
                copy.Restore(Path.Combine(directory, "vial-remote.ddsave"));
                Require(codec.Encode(remote).SequenceEqual(codec.Encode(Saved(copy, "vial-remote-restored"))),
                    "Authentic wire96 restore must preserve the complete carried state.");
                var use = VialUse("vial.remote-use", 115);
                foreach (var active in new[] { session, copy }) {
                    Require(active.Submit(player, VialUse("vial.remote-sibling", 115, SiblingVialId)).Response == ExpeditionResponse.Unavailable,
                        "The sibling has no remote access.");
                    CommitVialRoute(active, use);
                    var used = Saved(active, active == session ? "vial-used" : "vial-used-restored");
                    var empty = used.AlchemyDoses.Single(x => x.Id == VialId);
                    var after = PortableEquipmentRules.CarriedBurden(used, hero);
                    var before = PortableEquipmentRules.CarriedBurden(remote, hero);
                    Require(empty.Spent && empty.Id == dose.Id && empty.OwnerId == companion && empty.CustodianId == hero
                        && empty.LocationId == hero && empty.Hp == dose.Hp && empty.MaximumHp == dose.MaximumHp
                        && empty.PotentialHealing == empty.FirstD4 + empty.SecondD4 + 2 && empty.ActualHealing == 0
                        && used.WorldIntervals.Single(x => x.ActorId == hero).ActionSpent
                        && used.PortableEquipment.Single(x => x.Id == VialId).HeldHands == 1
                        && after.Pounds == before.Pounds - new RuleQuantity(1, 10)
                        && after.Load == before.Load - new RuleQuantity(1, 100)
                        && used.AlchemyDoses.Where(x => x.Spent).Select(x => x.Id).SequenceEqual(new[] { VialId }),
                        "Use must pay an Action and retain the same held empty vial at exactly its own reduced burden.");
                    Require(active.Submit(player, use).Response == ExpeditionResponse.Duplicate
                        && active.Submit(player, VialUse("vial.spent-again", 116)).Response == ExpeditionResponse.Unavailable
                        && codec.Encode(used).SequenceEqual(codec.Encode(Saved(active, "vial-use-retries"))),
                        "Repeat use must preserve full state.");
                }
                Require(File.ReadAllBytes(Path.Combine(directory, "vial-used.ddsave"))
                    .SequenceEqual(File.ReadAllBytes(Path.Combine(directory, "vial-used-restored.ddsave"))),
                    "Live and restored use must produce identical canonical bytes.");

                var wrong = ConnectedExpeditionSession.Start();
                Throws<ArgumentException>(() => wrong.Restore(Path.Combine(directory, "vial-remote.ddsave")));
                Require(wrong.View(player).Revision == 0, "Wrong-profile restore must be atomic.");
                var selectedPolicy = (TestOnlySharedWorldPolicy)typeof(ConnectedExpeditionSession)
                    .GetField("policy", BindingFlags.Instance | BindingFlags.NonPublic).GetValue(copy);
                Throws<InvalidOperationException>(() => new Simulation(selectedPolicy, remote, ExecutionProfile.Release));

                var oldEnvelope = remote.Copy();
                oldEnvelope.ConnectedCarriedVial = false;
                Throws<ArgumentException>(() => codec.Encode(oldEnvelope));
                var duplicateBody = remote.Copy();
                duplicateBody.PortableEquipment = duplicateBody.PortableEquipment.Append(carried).ToArray();
                Throws<ArgumentException>(() => codec.Encode(duplicateBody));
                var contradictoryCustody = remote.Copy();
                contradictoryCustody.AlchemyDoses = contradictoryCustody.AlchemyDoses.Select(x => x.Id == VialId
                    ? x.WithPlacement(companion, "TEST_ONLY.prepared-plot") : x).ToArray();
                Throws<ArgumentException>(() => codec.Encode(contradictoryCustody));
                var fakeSpent = remote.Copy();
                fakeSpent.AlchemyDoses = fakeSpent.AlchemyDoses.Select(x => x.Id == VialId
                    ? new AlchemyDoseRecord(x.Id, x.OrderId, x.RecipeId, x.MakerId, x.OwnerId, x.CustodianId, x.LocationId,
                        x.CreatedAt, x.MaximumHp, x.Hp, remote.RuleClock, hero, hero, 1, 1, 4, 0) : x).ToArray();
                string forged = Path.Combine(directory, "vial-forged-spent.ddsave");
                store.Save(forged, fakeSpent);
                Throws<ArgumentException>(() => copy.Restore(forged));
                Require(copy.View(player).Revision == 116, "Coherent forged use without a receipt must not replace the live state.");

                // Detached consequence witness from a genuinely carried save. It cannot be restored or submitted.
                var drop = remote.Copy();
                var dropEquipment = typeof(TestOnlyClubAttackPolicy).GetMethod("DropConditionEquipment", BindingFlags.Static | BindingFlags.NonPublic);
                dropEquipment.Invoke(null, new object[] { drop, hero });
                var ground = drop.PortableEquipment.Single(x => x.Id == VialId);
                Require(ground.Placement == PortablePlacement.Ground && ground.HeldHands == 0 && ground.GroundX == actor.X
                    && ground.GroundY == actor.Y && drop.AlchemyDoses.Single(x => x.Id == VialId).LocationId
                        == PortableEquipmentValidation.GroundLocation(ground)
                    && !drop.AlchemyDoses.Single(x => x.Id == VialId).Spent,
                    "Mandatory drop must place the same intact unused body and clear hand occupancy.");
            });
        }
    }
}
#endif
