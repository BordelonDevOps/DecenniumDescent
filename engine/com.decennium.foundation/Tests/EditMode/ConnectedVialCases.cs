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

        private static ConnectedExpeditionSession StartVialScenario()
        {
            var session = ConnectedExpeditionSession.StartWithCarriedVial();
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
