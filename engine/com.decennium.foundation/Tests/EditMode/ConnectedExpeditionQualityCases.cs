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
        private static void AddConnectedExpeditionQualityCases(Dictionary<string, Action> cases, string directory)
        {
            cases.Add("int05_recipe4_quality_explanation_agrees_with_native_settlement", () =>
            {
                const ExpeditionSeat player = ExpeditionSeat.Player;
                const string orderId = "manufacture.order.104";
                string pending = Path.Combine(directory, "quality-pending.ddsave");
                string observed = Path.Combine(directory, "quality-observed.ddsave");
                var original = ReachQualityChoice(2);
                original.Save(pending);
                var canonical = File.ReadAllBytes(pending);
                var view = original.View(player);
                var explanation = original.ExplainManufacturingQuality(player, view.Revision, view.DecisionId);
                Require(explanation != null && explanation.Revision == 106 && explanation.DecisionId == orderId
                    && explanation.WorkerId == ConnectedExpeditionSession.Companion && explanation.RecipeId == "recipe-4"
                    && explanation.TestOnly && explanation.Quality == CraftQuality.Exceptional
                    && explanation.RecipeSourceRevision == "46a4d52728ee6956f0bebcb5d2103ffd5bc67ba4"
                    && explanation.RecipeSourceBlobId == "74b948a92e30e0bacbaafa8529432c265d4bf0af"
                    && explanation.RecipeSourcePointer == "/recipes/3"
                    && explanation.ReviewedPublicRecipeReference.EndsWith("@a71c2e54ad86a8b35377323f16a9f4ff7df986e0#recipe-4", StringComparison.Ordinal)
                    && explanation.HealingEffect.Contains("2d4+2") && explanation.HealingEffect.Contains("magical nonspell"),
                    "The explanation must bind the current owned choice to its reviewed public recipe.");
                Require(explanation.Alternatives.Count == 2, "Both selected alternatives must be available.");
                var full = explanation.Alternatives[0];
                var durable = explanation.Alternatives[1];
                Require(full.Choice == CraftQualityChoice.FullYield && full.DoseCount == 6 && full.VialStructuralHp == 1
                    && full.SupplementaryVialsConsumed == Q(1) && full.SupplementaryVialsReleased == Q(1)
                    && durable.Choice == CraftQualityChoice.Durability && durable.DoseCount == 5 && durable.VialStructuralHp == 2
                    && durable.SupplementaryVialsConsumed == default && durable.SupplementaryVialsReleased == Q(2),
                    "The two alternatives must describe the native Exceptional choices.");
                Require(explanation.Alternatives is IList<ExpeditionManufacturingQualityAlternative> list && list.IsReadOnly,
                    "Alternatives must be detached and immutable.");
                Require(QualitySignature(explanation) == QualitySignature(original.ExplainManufacturingQuality(player, 106, orderId))
                    && original.View(player).DecisionId == view.DecisionId && original.View(player).Clock == view.Clock,
                    "Repeated explanations must agree and preserve the permitted decision.");
                Require(original.ExplainManufacturingQuality(ExpeditionSeat.FirstOpponent, 106, orderId) == null
                    && original.ExplainManufacturingQuality((ExpeditionSeat)99, 106, orderId) == null
                    && original.ExplainManufacturingQuality(player, 105, orderId) == null
                    && original.ExplainManufacturingQuality(player, 106, "manufacture.order.105") == null
                    && original.ExplainManufacturingQuality(player, 106, "bad id") == null
                    && original.ExplainManufacturingQuality(player, 106, null) == null,
                    "Unauthorized, stale, mismatched and malformed inputs must return uniform null.");
                original.Save(observed);
                Require(canonical.SequenceEqual(File.ReadAllBytes(observed)), "Every explanation must preserve complete bytes.");

                foreach (var alternative in explanation.Alternatives) {
                    var session = ConnectedExpeditionSession.Start();
                    session.SetSeatEnabled(player, false);
                    session.Restore(pending);
                    var command = new Command("quality.actual-choice", explanation.WorkerId, explanation.Revision,
                        CommandKind.ResolveManufacturingQuality, explanation.DecisionId, x: (int)alternative.Choice);
                    Require(session.ExplainManufacturingQuality(player, 106, orderId) == null
                        && session.Submit(player, command).Response == ExpeditionResponse.NotAuthorized,
                        "A restored preview or old result must not carry authority.");
                    session.SetSeatEnabled(player, true);
                    Require(QualitySignature(explanation) == QualitySignature(session.ExplainManufacturingQuality(player, 106, orderId)),
                        "Authentic restoration must reproduce the advisory result for the current owner.");
                    Require(session.Submit(player, command).Response == ExpeditionResponse.Committed,
                        "A displayed native choice must actually settle.");
                    session.Save(observed);
                    var state = new FileSaveStore().Load(observed);
                    var packaging = state.Work.Reservations.Single(x => x.Id == orderId + ".packaging");
                    Require(state.AlchemyDoses.Length == alternative.DoseCount && state.AlchemyDoses.All(x =>
                            x.Hp == alternative.VialStructuralHp && x.MaximumHp == alternative.VialMaximumStructuralHp)
                        && packaging.ConsumedAmount == alternative.SupplementaryVialsConsumed
                        && packaging.ReleasedAmount == alternative.SupplementaryVialsReleased,
                        "Actual settlement must match every displayed quantity.");
                    var committed = File.ReadAllBytes(observed);
                    var conflict = new Command(command.Id, command.Actor, command.ExpectedRevision, command.Kind,
                        command.Target, x: alternative.Choice == CraftQualityChoice.FullYield ? 2 : 1);
                    var stale = new Command("quality.stale-preview", command.Actor, command.ExpectedRevision,
                        command.Kind, command.Target, x: command.X);
                    Require(session.ExplainManufacturingQuality(player, 106, orderId) == null
                        && session.ExplainManufacturingQuality(player, 107, orderId) == null
                        && session.Submit(player, stale).Response == ExpeditionResponse.StaleRevision
                        && session.Submit(player, command).Response == ExpeditionResponse.Duplicate
                        && session.Submit(player, conflict).Response == ExpeditionResponse.CommandIdConflict,
                        "Settlement must clear the explanation and preserve stale/retry/conflict behavior.");
                    session.Save(observed);
                    Require(committed.SequenceEqual(File.ReadAllBytes(observed)), "Controls must leave the terminal state unchanged.");
                }
            });

            cases.Add("int05_recipe4_quality_explanation_omits_unfunded_and_lower_priority_choices", () =>
            {
                const ExpeditionSeat player = ExpeditionSeat.Player;
                const string orderId = "manufacture.order.104";
                var noExtras = ReachQualityChoice(0);
                var explanation = noExtras.ExplainManufacturingQuality(player, 106, orderId);
                Require(explanation != null && explanation.Alternatives.Count == 1, "Unfunded Full Yield must be omitted.");
                var option = explanation.Alternatives.Single();
                Require(option.Choice == CraftQualityChoice.Durability && option.DoseCount == 5 && option.VialStructuralHp == 2
                    && option.SupplementaryVialsConsumed == default && option.SupplementaryVialsReleased == default,
                    "The zero-reserve native choice remains useful and releases no phantom vials.");
                string path = Path.Combine(directory, "quality-zero-vials.ddsave");
                noExtras.Save(path);
                var actual = new FileSaveStore().Load(path);
                Require(!actual.Work.Reservations.Any(x => x.Id == orderId + ".packaging"),
                    "The genuine zero-extra path must not create a packaging claim.");

                // Detached selector probes only. The states are never restored or executed.
                var select = typeof(ConnectedExpeditionSession).GetMethod("OwnedQualityOrder",
                    BindingFlags.NonPublic | BindingFlags.Static);
                var grant = new Authority("TEST_ONLY.preview-probe", new[] { ConnectedExpeditionSession.Companion },
                    inventoryOwners: new[] { ConnectedExpeditionSession.Companion });
                object Pick(Snapshot state, Authority access) => select.Invoke(null, new object[] { state, access, 106L, orderId });
                Require(Pick(actual, grant) != null, "The detached gate control must recognize its genuine pending order.");
                var noInventory = new Authority("TEST_ONLY.preview-probe", new[] { ConnectedExpeditionSession.Companion });
                Require(Pick(actual, noInventory) == null, "Control without inventory permission must not disclose the choice.");
                var noKnowledge = actual.Copy();
                noKnowledge.FormulaWork = Array.Empty<FormulaWorkRecord>();
                Require(Pick(noKnowledge, grant) == null, "Public recipe visibility must not grant formula knowledge.");
                var masterwork = actual.Copy();
                var order = actual.ManufacturingOrders.Single();
                masterwork.ManufacturingOrders = new[] { new ManufacturingOrderRecord(order.Id, order.WorkerId, order.RecipeId,
                    order.MaterialSet, order.ExtraVials, order.TakeTen, order.Status, order.Work, order.StartedAt, order.UpdatedAt,
                    order.StabilizedAt, first: 20, natural: 20, quality: CraftQuality.Masterwork) };
                Require(Pick(masterwork, grant) == null, "The Exceptional explanation must not partially project Masterwork.");
                var interrupted = actual.Copy();
                var attack = actual.MeleeAttacks.First();
                interrupted.MeleeAttacks = new[] { new MeleeAttackRecord(attack.Id, attack.Revision, 0, attack.TurnOrdinal,
                    attack.AttackerId, attack.TargetId, attack.WeaponId, attack.At, attack.Instruction, attack.Attack, attack.Damage) };
                Require(Pick(interrupted, grant) == null, "A higher-priority knockout must hide the underlying quality decision.");

                var full = new Command("quality.unfunded", explanation.WorkerId, 106, CommandKind.ResolveManufacturingQuality, orderId, x: 1);
                var durable = new Command("quality.durable", explanation.WorkerId, 106, CommandKind.ResolveManufacturingQuality, orderId, x: 2);
                Require(noExtras.Submit(player, full).Response == ExpeditionResponse.Unavailable
                    && noExtras.Submit(player, durable).Response == ExpeditionResponse.Committed,
                    "Native commands must agree with the zero-reserve explanation.");
                noExtras.Save(path);
                var finished = new FileSaveStore().Load(path);
                Require(finished.AlchemyDoses.Length == option.DoseCount && finished.AlchemyDoses.All(x => x.Hp == option.VialStructuralHp)
                    && !finished.Work.Reservations.Any(x => x.Id == orderId + ".packaging"),
                    "Zero-reserve settlement must preserve the displayed count, HP and packaging absence.");
            });
        }

        private static string QualitySignature(ExpeditionManufacturingQualityExplanation explanation)
            => string.Join("|", explanation.Revision, explanation.DecisionId, explanation.WorkerId, explanation.RecipeId,
                explanation.Quality, explanation.RecipeSourceRevision, explanation.RecipeSourceBlobId,
                explanation.RecipeSourcePointer, explanation.ReviewedPublicRecipeReference, explanation.HealingEffect,
                string.Join(";", explanation.Alternatives.Select(x => string.Join(":", x.Choice, x.DoseCount,
                    x.VialStructuralHp, x.VialMaximumStructuralHp, x.SupplementaryVialsConsumed, x.SupplementaryVialsReleased))));

        private static ConnectedExpeditionSession ReachQualityChoice(int extraVials)
        {
            const ExpeditionSeat player = ExpeditionSeat.Player;
            var session = ConnectedExpeditionSession.Start();
            Require(session.ExplainManufacturingQuality(player, 0, "manufacture.order.104") == null,
                "A recipe decision cannot be previewed before it exists.");
            foreach (var input in QualityWalkthrough()) {
                // Commit this caller-supplied identifier before the explanation to exercise probe ID collision handling.
                var command = input.ExpectedRevision == 0
                    ? new Command("quality.explanation", input.Actor, 0, input.Kind, input.Target, input.X, input.Y) : input;
                if (command.Kind == CommandKind.StartManufacturing && command.Y != extraVials)
                    command = new Command(command.Id, command.Actor, command.ExpectedRevision, command.Kind,
                        command.Target, command.X, extraVials);
                var result = command.Kind == CommandKind.AdvanceClock || command.Kind == CommandKind.EndFixedEncounter
                    ? session.SubmitSessionCommand(command)
                    : session.Submit(command.Actor == ConnectedExpeditionSession.FirstOpponent ? ExpeditionSeat.FirstOpponent : player, command);
                Require(result.Response == ExpeditionResponse.Committed && result.Revision == command.ExpectedRevision + 1,
                    "The accepted public input did not commit: " + command.Id);
            }
            return session;
        }

        // Accepted public walkthrough through its genuine pending quality choice.
        private static IEnumerable<Command> QualityWalkthrough()
        {
            yield return new Command("i-0", ConnectedExpeditionSession.Hero, 0, CommandKind.BeginWorldStep, target: "walk", x: 1);
            yield return new Command("i-1", ConnectedExpeditionSession.Hero, 1, CommandKind.AdvanceClock, x: 2, y: 1);
            yield return new Command("i-2", ConnectedExpeditionSession.Hero, 2, CommandKind.BeginWorldStep, target: "walk", x: 1);
            yield return new Command("i-3", ConnectedExpeditionSession.Hero, 3, CommandKind.AdvanceClock, x: 2, y: 1);
            yield return new Command("i-4", ConnectedExpeditionSession.Hero, 4, CommandKind.BeginWorldStep, target: "walk", x: 1);
            yield return new Command("tactical.command.6", ConnectedExpeditionSession.FirstOpponent, 5, CommandKind.SelectCombatStance,
                combat: new CombatRequest("world.fixed-conflict.turn.1", "", 1));
            yield return new Command("tactical.command.7", ConnectedExpeditionSession.FirstOpponent, 6, CommandKind.TacticalStep,
                target: "world.fixed-conflict.turn.1", x: 3);
            yield return new Command("tactical.command.8", ConnectedExpeditionSession.FirstOpponent, 7, CommandKind.EndRegularTurn,
                target: "world.fixed-conflict.turn.1");
            yield return new Command("tactical.command.9", ConnectedExpeditionSession.Hero, 8, CommandKind.SelectCombatStance,
                combat: new CombatRequest("world.fixed-conflict.turn.2", "", 1));
            yield return new Command("tactical.command.10", ConnectedExpeditionSession.Hero, 9, CommandKind.AttackClub,
                target: "TEST_ONLY.third-combatant", combat: new CombatRequest("world.fixed-conflict.turn.2", "TEST_ONLY.actor-club", 0));
            yield return new Command("tactical.command.11", ConnectedExpeditionSession.Hero, 10, CommandKind.EndRegularTurn,
                target: "world.fixed-conflict.turn.2");
            yield return new Command("tactical.command.12", ConnectedExpeditionSession.FirstOpponent, 11, CommandKind.EndRegularTurn,
                target: "world.fixed-conflict.turn.3");
            yield return new Command("tactical.command.13", ConnectedExpeditionSession.Hero, 12, CommandKind.SelectCombatStance,
                combat: new CombatRequest("world.fixed-conflict.turn.4", "", 1));
            yield return new Command("tactical.command.14", ConnectedExpeditionSession.Hero, 13, CommandKind.AttackClub,
                target: "TEST_ONLY.third-combatant", combat: new CombatRequest("world.fixed-conflict.turn.4", "TEST_ONLY.actor-club", 0));
            yield return new Command("tactical.command.15", ConnectedExpeditionSession.Hero, 14, CommandKind.EndFixedEncounter,
                target: "world.fixed-conflict.turn.4");
            yield return new Command("mining.command.16", ConnectedExpeditionSession.Companion, 15, CommandKind.StartMining,
                target: "TEST_ONLY.mining.deposit", miningSelection: new MiningSelectionRequest("TEST_ONLY.mining.deposit-v1", new[] { "TEST_ONLY.mining.category.iron" }, MiningAbilityChoice.Wisdom, false, "", "", ""));
            yield return new Command("i-16", ConnectedExpeditionSession.Hero, 16, CommandKind.AdvanceClock, x: 1800, y: 1);
            yield return new Command("portable.command.18", ConnectedExpeditionSession.Companion, 17, CommandKind.HandlePortableEquipment,
                target: "TEST_ONLY.mining.unit.iron", inventory: new InventoryRequest(new RuleQuantity(1, 1), "", HandlingKind.Retrieve));
            yield return new Command("i-18", ConnectedExpeditionSession.Companion, 18, CommandKind.BeginWorldStep, target: "walk", x: -1);
            yield return new Command("i-19", ConnectedExpeditionSession.Hero, 19, CommandKind.AdvanceClock, x: 6, y: 1);
            yield return new Command("portable.command.21", ConnectedExpeditionSession.Companion, 20, CommandKind.HandlePortableEquipment,
                target: "TEST_ONLY.mining.unit.iron", inventory: new InventoryRequest(new RuleQuantity(1, 1), "", HandlingKind.Drop));
            yield return new Command("i-21", ConnectedExpeditionSession.Hero, 21, CommandKind.AdvanceClock, x: 6, y: 1);
            yield return new Command("mining.command.23", ConnectedExpeditionSession.Companion, 22, CommandKind.StartHavenAppraisal,
                target: "TEST_ONLY.haven-appraisal-desk");
            yield return new Command("i-23", ConnectedExpeditionSession.Hero, 23, CommandKind.AdvanceClock, x: 1800, y: 1);
            yield return new Command("portable.command.25", ConnectedExpeditionSession.Companion, 24, CommandKind.HandlePortableEquipment,
                target: "TEST_ONLY.mining.unit.iron", inventory: new InventoryRequest(new RuleQuantity(1, 1), "", HandlingKind.Pickup));
            yield return new Command("i-25", ConnectedExpeditionSession.Hero, 25, CommandKind.AdvanceClock, x: 6, y: 1);
            yield return new Command("mining.command.27", ConnectedExpeditionSession.Companion, 26, CommandKind.StartHavenSale,
                target: "TEST_ONLY.haven-iron-offer.v1");
            yield return new Command("i-27", ConnectedExpeditionSession.Hero, 27, CommandKind.AdvanceClock, x: 1800, y: 1);
            yield return new Command("i-28", ConnectedExpeditionSession.Hero, 28, CommandKind.AdvanceClock, x: 6, y: 1);
            yield return new Command("mining.command.30", ConnectedExpeditionSession.Companion, 29, CommandKind.PurchaseHavenMeal,
                target: "TEST_ONLY.haven-ordinary-hot-meal.v1");
            yield return new Command("i-30", ConnectedExpeditionSession.Companion, 30, CommandKind.StartIntake,
                target: "TEST_ONLY.haven-cooked-serving", inventory: new InventoryRequest(new RuleQuantity(2, 3), "", HandlingKind.Pickup));
            yield return new Command("i-31", ConnectedExpeditionSession.Hero, 31, CommandKind.AdvanceClock, x: 150, y: 1);
            yield return new Command("i-32", ConnectedExpeditionSession.Companion, 32, CommandKind.InterruptIntake, target: "inventory.31.intake");
            yield return new Command("i-33", ConnectedExpeditionSession.Hero, 33, CommandKind.AdvanceClock, x: 6, y: 1);
            yield return new Command("i-34", ConnectedExpeditionSession.Companion, 34, CommandKind.PortionInventory,
                target: "TEST_ONLY.haven-cooked-serving", inventory: new InventoryRequest(new RuleQuantity(1, 6), "", HandlingKind.Pickup));
            yield return new Command("portable.command.36", ConnectedExpeditionSession.Companion, 35, CommandKind.HandlePortableEquipment,
                target: "TEST_ONLY.haven-cooked-serving", inventory: new InventoryRequest(new RuleQuantity(1, 1), "", HandlingKind.Drop));
            yield return new Command("i-36", ConnectedExpeditionSession.Hero, 36, CommandKind.AdvanceClock, x: 6, y: 1);
            yield return new Command("portable.command.38", ConnectedExpeditionSession.Companion, 37, CommandKind.HandlePortableEquipment,
                target: "inventory.35.lot", inventory: new InventoryRequest(new RuleQuantity(1, 1), "", HandlingKind.Drop));
            yield return new Command("i-38", ConnectedExpeditionSession.Companion, 38, CommandKind.BeginWorldStep, target: "walk", x: 1);
            yield return new Command("i-39", ConnectedExpeditionSession.Hero, 39, CommandKind.AdvanceClock, x: 6, y: 1);
            yield return new Command("i-40", ConnectedExpeditionSession.Companion, 40, CommandKind.BeginWorldStep, target: "walk", x: -1);
            yield return new Command("i-41", ConnectedExpeditionSession.Hero, 41, CommandKind.AdvanceClock, x: 6, y: 1);
            yield return new Command("portable.command.43", ConnectedExpeditionSession.Companion, 42, CommandKind.HandlePortableEquipment,
                target: "inventory.35.lot", inventory: new InventoryRequest(new RuleQuantity(1, 1), "", HandlingKind.Pickup));
            yield return new Command("i-43", ConnectedExpeditionSession.Hero, 43, CommandKind.AdvanceClock, x: 6, y: 1);
            yield return new Command("i-44", ConnectedExpeditionSession.Companion, 44, CommandKind.StartIntake,
                target: "inventory.35.lot", inventory: new InventoryRequest(new RuleQuantity(1, 6), "", HandlingKind.Pickup));
            yield return new Command("i-45", ConnectedExpeditionSession.Hero, 45, CommandKind.AdvanceClock, x: 156, y: 1);
            yield return new Command("portable.command.47", ConnectedExpeditionSession.Companion, 46, CommandKind.HandlePortableEquipment,
                target: "TEST_ONLY.haven-cooked-serving", inventory: new InventoryRequest(new RuleQuantity(1, 1), "", HandlingKind.Pickup));
            yield return new Command("i-47", ConnectedExpeditionSession.Hero, 47, CommandKind.AdvanceClock, x: 6, y: 1);
            yield return new Command("i-48", ConnectedExpeditionSession.Companion, 48, CommandKind.StartIntake,
                target: "TEST_ONLY.haven-cooked-serving", inventory: new InventoryRequest(new RuleQuantity(1, 3), "", HandlingKind.Pickup));
            yield return new Command("i-49", ConnectedExpeditionSession.Hero, 49, CommandKind.AdvanceClock, x: 300, y: 1);
            yield return new Command("mining.command.51", ConnectedExpeditionSession.Companion, 50, CommandKind.StartExpeditionBill,
                target: "TEST_ONLY.haven-iron-episode-bill.v1");
            yield return new Command("i-51", ConnectedExpeditionSession.Hero, 51, CommandKind.AdvanceClock, x: 1800, y: 1);
            yield return new Command("mining.command.53", ConnectedExpeditionSession.Hero, 52, CommandKind.CloseExpeditionEpisode,
                target: "TEST_ONLY.haven-iron-episode");
            yield return new Command("i-53", ConnectedExpeditionSession.Companion, 53, CommandKind.BeginWorldStep, target: "walk", x: 1);
            yield return new Command("i-54", ConnectedExpeditionSession.Hero, 54, CommandKind.AdvanceClock, x: 6, y: 1);
            yield return new Command("i-55", ConnectedExpeditionSession.Hero, 55, CommandKind.BeginWorldStep, target: "walk", x: -1);
            yield return new Command("i-56", ConnectedExpeditionSession.Hero, 56, CommandKind.AdvanceClock, x: 6, y: 1);
            yield return new Command("i-57", ConnectedExpeditionSession.Hero, 57, CommandKind.BeginWorldStep, target: "walk", y: 1);
            yield return new Command("i-58", ConnectedExpeditionSession.Hero, 58, CommandKind.AdvanceClock, x: 6, y: 1);
            yield return new Command("i-59", ConnectedExpeditionSession.Hero, 59, CommandKind.BeginWorldStep, target: "walk", y: 1);
            yield return new Command("i-60", ConnectedExpeditionSession.Hero, 60, CommandKind.AdvanceClock, x: 6, y: 1);
            yield return new Command("i-61", ConnectedExpeditionSession.Hero, 61, CommandKind.BeginWorldStep, target: "walk", y: 1);
            yield return new Command("i-62", ConnectedExpeditionSession.Hero, 62, CommandKind.AdvanceClock, x: 6, y: 1);
            yield return new Command("i-63", ConnectedExpeditionSession.Hero, 63, CommandKind.BeginWorldStep, target: "walk", x: 1);
            yield return new Command("i-64", ConnectedExpeditionSession.Hero, 64, CommandKind.AdvanceClock, x: 6, y: 1);
            yield return new Command("mining.command.66", ConnectedExpeditionSession.Hero, 65, CommandKind.StartNextCharterPlan,
                target: "TEST_ONLY.haven-approach-plan.v1");
            yield return new Command("i-66", ConnectedExpeditionSession.Hero, 66, CommandKind.AdvanceClock, x: 3600, y: 1);
            yield return new Command("i-67", ConnectedExpeditionSession.Hero, 67, CommandKind.BeginWorldStep, target: "walk", x: -1);
            yield return new Command("i-68", ConnectedExpeditionSession.Hero, 68, CommandKind.AdvanceClock, x: 6, y: 1);
            yield return new Command("i-69", ConnectedExpeditionSession.Companion, 69, CommandKind.BeginWorldStep, target: "walk", x: 1);
            yield return new Command("i-70", ConnectedExpeditionSession.Hero, 70, CommandKind.AdvanceClock, x: 6, y: 1);
            yield return new Command("i-71", ConnectedExpeditionSession.Hero, 71, CommandKind.BeginWorldStep, target: "walk", x: 1);
            yield return new Command("i-72", ConnectedExpeditionSession.Hero, 72, CommandKind.AdvanceClock, x: 6, y: 1);
            yield return new Command("portable.command.74", ConnectedExpeditionSession.Hero, 73, CommandKind.HandlePortableEquipment,
                target: "TEST_ONLY.pack-rations", inventory: new InventoryRequest(new RuleQuantity(1, 1), "", HandlingKind.Retrieve));
            yield return new Command("i-74", ConnectedExpeditionSession.Hero, 74, CommandKind.AdvanceClock, x: 6, y: 1);
            yield return new Command("portable.command.76", ConnectedExpeditionSession.Hero, 75, CommandKind.HandlePortableEquipment,
                target: "TEST_ONLY.pack-skin", inventory: new InventoryRequest(new RuleQuantity(1, 1), "", HandlingKind.Retrieve));
            yield return new Command("i-76", ConnectedExpeditionSession.Hero, 76, CommandKind.AdvanceClock, x: 6, y: 1);
            yield return new Command("mining.command.78", ConnectedExpeditionSession.Hero, 77, CommandKind.AcceptNextCharter,
                target: "TEST_ONLY.haven-approach-charter-offer.v1");
            yield return new Command("i-78", ConnectedExpeditionSession.Hero, 78, CommandKind.BeginWorldStep, target: "walk", x: 1);
            yield return new Command("i-79", ConnectedExpeditionSession.Hero, 79, CommandKind.AdvanceClock, x: 6, y: 1);
            yield return new Command("i-80", ConnectedExpeditionSession.Hero, 80, CommandKind.BeginWorldStep, target: "walk", x: -1);
            yield return new Command("i-81", ConnectedExpeditionSession.Hero, 81, CommandKind.AdvanceClock, x: 6, y: 1);
            yield return new Command("mining.command.83", ConnectedExpeditionSession.Hero, 82, CommandKind.StartCharterAttempt,
                target: "TEST_ONLY.haven-approach-charter");
            yield return new Command("i-83", ConnectedExpeditionSession.Hero, 83, CommandKind.BeginWorldStep, target: "walk", x: 1);
            yield return new Command("i-84", ConnectedExpeditionSession.Hero, 84, CommandKind.AdvanceClock, x: 3, y: 2);
            yield return new Command("mining.command.86", ConnectedExpeditionSession.Hero, 85, CommandKind.ObserveCharterApproach,
                target: "charter.attempt.83");
            yield return new Command("i-86", ConnectedExpeditionSession.Hero, 86, CommandKind.BeginWorldStep, target: "walk", x: -1);
            yield return new Command("i-87", ConnectedExpeditionSession.Hero, 87, CommandKind.AdvanceClock, x: 3, y: 2);
            yield return new Command("i-88", ConnectedExpeditionSession.Hero, 88, CommandKind.BeginWorldStep, target: "walk", x: -1);
            yield return new Command("i-89", ConnectedExpeditionSession.Hero, 89, CommandKind.AdvanceClock, x: 6, y: 1);
            yield return new Command("i-90", ConnectedExpeditionSession.Companion, 90, CommandKind.OpenPortableContainer,
                target: "TEST_ONLY.preservation.sealable-vessel");
            yield return new Command("i-91", ConnectedExpeditionSession.Companion, 91, CommandKind.StartHarvestPreservationTreatment,
                target: "manufacture.recipe14.set0.component2", inventory: new InventoryRequest(new RuleQuantity(1, 1), "", HandlingKind.Pickup));
            yield return new Command("i-92", ConnectedExpeditionSession.Hero, 92, CommandKind.AdvanceClock, x: 1800, y: 1);
            yield return new Command("option.93.connected-research.start", ConnectedExpeditionSession.Companion, 93, CommandKind.StartFormulaResearch,
                target: "research.guild-notes");
            yield return new Command("i-94", ConnectedExpeditionSession.Hero, 94, CommandKind.AdvanceClock, x: 15421, y: 1);
            yield return new Command("option.95.connected-research.control", ConnectedExpeditionSession.Companion, 95, CommandKind.ResumeFormulaWork,
                target: "formula.94");
            yield return new Command("i-96", ConnectedExpeditionSession.Hero, 96, CommandKind.AdvanceClock, x: 13379, y: 1);
            yield return new Command("i-97", ConnectedExpeditionSession.Companion, 97, CommandKind.HandlePortableEquipment,
                target: "TEST_ONLY.preservation.sealable-vessel", inventory: new InventoryRequest(new RuleQuantity(1, 1), "", HandlingKind.Pickup));
            yield return new Command("i-98", ConnectedExpeditionSession.Companion, 98, CommandKind.BeginWorldStep, target: "walk", x: -1);
            yield return new Command("i-99", ConnectedExpeditionSession.Hero, 99, CommandKind.AdvanceClock, x: 6, y: 1);
            yield return new Command("i-100", ConnectedExpeditionSession.Companion, 100, CommandKind.HandlePortableEquipment,
                target: "TEST_ONLY.preservation.sealable-vessel", inventory: new InventoryRequest(new RuleQuantity(1, 1), "", HandlingKind.Drop));
            yield return new Command("i-101", ConnectedExpeditionSession.Companion, 101, CommandKind.OpenPortableContainer,
                target: "TEST_ONLY.preservation.sealable-vessel");
            yield return new Command("i-102", ConnectedExpeditionSession.Hero, 102, CommandKind.AdvanceClock, x: 60, y: 1);
            yield return new Command("recipe4.batch.103", ConnectedExpeditionSession.Companion, 103, CommandKind.StartManufacturing,
                target: "recipe-4", y: 2);
            yield return new Command("i-104", ConnectedExpeditionSession.Hero, 104, CommandKind.AdvanceClock, x: 900, y: 1);
            yield return new Command("i-105", ConnectedExpeditionSession.Hero, 105, CommandKind.AdvanceClock, x: 13500, y: 1);
        }
    }
}
#endif
