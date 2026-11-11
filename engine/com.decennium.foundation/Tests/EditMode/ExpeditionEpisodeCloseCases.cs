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
        private const string CloseEpisode = TestOnlyExpeditionBillProfile.EpisodeId;
        private const string CloseLeader = TestOnlyExpeditionCloseProfile.LeaderId;

        private static TestOnlySharedWorldPolicy ClosePolicy(TestOnlyExpeditionCloseProfile profile = null, ConditionCombatFixture conditions = null)
            => BillPolicy(conditions: conditions).EnableExpeditionClose(profile ?? new TestOnlyExpeditionCloseProfile());

        private static Command CloseCommand(Simulation sim, string actor = CloseLeader, string target = CloseEpisode)
            => MiningCommand(sim, CommandKind.CloseExpeditionEpisode, target, actor: actor);

        private static Simulation CloseReady(TestOnlySharedWorldPolicy policy = null)
        {
            var sim = BillAtDesk(policy ?? ClosePolicy(), withEncounter: true);
            SaleCommit(sim, BillCommand(sim));
            WorldAdvance(sim, 1800);
            WorldStep(sim, 1, 0, actor: SaleSeller);
            WorldAdvance(sim, 2);
            Require(BillJob(sim).Report != null && sim.Capture().Actors.Single(x => x.Id == SaleSeller).X == 3,
                "The connected procedure did not reach the real closing boundary.");
            return sim;
        }

        private static ExpeditionEpisodeCloseRecord Closure(Simulation sim) => sim.Capture().ExpeditionEpisodeClose;

        private static void AddExpeditionEpisodeCloseCases(Dictionary<string, Action> cases, string directory)
        {
            var host = HavenSaleHost();
            var closer = new Authority(host.Principal, new[] { CloseLeader });
            cases.Add("mgt10_episode_close_connected_actual_state_zero_time_and_replay", () =>
            {
                var sim = CloseReady();
                var before = sim.Capture();
                var codec = new SnapshotCodec();
                var command = CloseCommand(sim);
                byte[] beforeQuery = Bytes(sim);
                var query = sim.QueryCommand(closer, command);
                Require(query.Supported && query.Admissible && beforeQuery.SequenceEqual(Bytes(sim))
                    && sim.DiscoverCommands(closer, CloseLeader).Any(x => x.Command.Kind == CommandKind.CloseExpeditionEpisode && x.Query.Admissible),
                    "The read-only close query was unavailable to the appointed controller without property grants: " + query.Code);
                Require(before.SchemaVersion == Snapshot.ExpeditionEpisodeCloseSchema && before.Encounter != null
                    && before.ClosedEncounters.Length == 0 && !before.InventoryCombat
                    && before.Lives.Single(x => x.ActorId == AdditionalTacticalActor.Id).Dead,
                    "The scenario lost the supported fixed conflict exit evidence.");
                var replay = SaveBill(sim, ClosePolicy(), directory, "mgt10-episode-close-before");
                foreach (var run in new[] { sim, replay }) {
                    var result = run.Execute(closer, command);
                    Require(result.Outcome == Outcome.Committed, "Legitimate closure was rejected: " + result.Code);
                    var after = run.Capture();
                    var close = after.ExpeditionEpisodeClose;
                    Require(close.SourceRevision == before.Revision && close.CloseRevision == before.Revision + 1
                        && close.ClosedAt == before.RuleClock && close.CommandId == command.Id && close.CloserId == CloseLeader
                        && close.EncounterId == before.Encounter.Id && close.HostileId == AdditionalTacticalActor.Id
                        && close.HostileX == new RuleQuantity(3) && close.HostileY == default
                        && close.BillId == before.ExpeditionBills.Single().Id
                        && close.BillReportRevision == before.ExpeditionBills.Single().UpdatedRevision,
                        "The close lost its actual temporal, tactical, bill or command evidence.");
                    var o = close.Outcome;
                    Require(o.PrimaryMetric == ExpeditionCloseMetric.RealizedNetExpedition && o.RealizedNetCopper == 2
                        && o.NetTargetCopper == new RuleQuantity(3) && !o.PrimaryTargetMet && o.RealizedGrossCopper == 2
                        && o.GrossTargetCopper == new RuleQuantity(2) && o.GrossTargetMet && o.ProfitTargetCopper == new RuleQuantity(1)
                        && o.ProfitTargetMet == null, "Close misreported the prospective metric or inferred profit.");
                    Require(close.Members.Count == 2 && close.Members.All(x => x.Life.Hp == 26 && x.Life.MaximumHp == 26
                        && x.Life.TemporaryHp == 0 && x.Life.LinkedInjuries.Count == 0 && x.AttainedLevels >= 1)
                        && close.Members.Single(x => x.ActorId == CloseLeader).X == new RuleQuantity(2)
                        && close.Members.Single(x => x.ActorId == SaleSeller).Y == new RuleQuantity(3)
                        && close.Members.All(x => x.LastMovementRevision > 0)
                        && close.MiningDispositions.Single(x => x.UnitId == AppraisalIron).Status == MiningUnitStatus.Extracted
                        && close.MiningDispositions.Single(x => x.UnitId == SharedMiningFixture.UnitB).Status == MiningUnitStatus.Forfeited,
                        "The close conflated membership, life, location or terminal acquisition facts.");
                    Require(close.Stock.Single(x => x.Stock.Id == PortableKitFixture.Rations).Stock.Amount == new RuleQuantity(20)
                        && close.Stock.Single(x => x.Stock.Id == PortableKitFixture.Water).Stock.LocationId == PortableKitFixture.Skin
                        && close.Stock.Single(x => x.Stock.Id == PortableKitFixture.Water).Stock.Amount == new RuleQuantity(4)
                        && close.Stock.Single(x => x.Stock.Id == HavenMealLot).Stock.Amount == default
                        && close.Stock.Single(x => x.Stock.Id == SaleTender).Provenance.OwnerId == SaleBuyer
                        && close.Stock.Single(x => x.Stock.Id == AppraisalIron).Stock.CustodianId == SaleBuyer
                        && close.Equipment.Any(x => x.Id == PortableKitFixture.Pack)
                        && close.Vessels.Any(x => x.Id == PortableKitFixture.Skin),
                        "The close failed to observe exact stock, ancestry, containers or title and custody.");
                    CheckClosureCoverage(close);
                    after.Revision = before.Revision;
                    after.Receipts = before.Receipts;
                    after.ExpeditionEpisodeClose = null;
                    Require(codec.Encode(after).SequenceEqual(beforeQuery),
                        "Closing mutated state outside the new record and command receipt.");
                    byte[] closedBytes = Bytes(run);
                    Require(run.Execute(closer, command).Outcome == Outcome.Duplicate && closedBytes.SequenceEqual(Bytes(run)),
                        "Identical closure was not idempotent.");
                    RejectUnchanged(run, closer, new Command(command.Id, command.Actor, command.ExpectedRevision,
                        command.Kind, "conflicting-episode"), "CommandIdConflict");
                    RejectUnchanged(run, closer, CloseCommand(run), "ExpeditionEpisodeAlreadyClosed");
                    RejectUnchanged(run, host, BillCommand(run), "ExpeditionEpisodeAlreadyClosed");
                }
                Require(Bytes(sim).SequenceEqual(Bytes(replay)), "Same closure command differed after disk restore.");
                var afterRestore = SaveBill(sim, ClosePolicy(), directory, "mgt10-episode-close-after");
                foreach (var run in new[] { sim, afterRestore }) {
                    var close = Closure(run);
                    WorldStep(run, -1, 0, actor: SaleSeller);
                    WorldAdvance(run, 6);
                    SaleCommit(run, Portable(run, CommandKind.HandlePortableEquipment, SaleTender, handling: HandlingKind.Drop, actor: SaleBuyer));
                    Require(ReferenceEquals(close, Closure(run)) && run.Capture().Actors.Single(x => x.Id == SaleSeller).X == 2
                        && run.Capture().PortableEquipment.Single(x => x.Id == SaleTender).Placement == PortablePlacement.Ground
                        && close.Equipment.Single(x => x.Id == SaleTender).Placement == PortablePlacement.Carried,
                        "Ordinary post-close movement or handling rewrote the historical projection.");
                }
                Require(Bytes(sim).SequenceEqual(Bytes(afterRestore)), "Post-close movement and handling replay diverged.");
                Throws<ArgumentException>(() => new Simulation(BillPolicy(), sim.Capture(), ExecutionProfile.Laboratory));
                Throws<InvalidOperationException>(() => new Simulation(ClosePolicy(), sim.Capture(), ExecutionProfile.Release));
                WriteClosureAudit(directory, sim.Capture(), "ordinary-movement-and-vendor-handling");
            });
            cases.Add("mgt10_episode_close_authority_receipts_and_stable_admission", () =>
            {
                var fresh = PortableWorld(ClosePolicy());
                RejectUnchanged(fresh, host, CloseCommand(fresh), "ExpeditionCloseEncounterUnresolved");
                WorldCommit(fresh, IC(fresh, CommandKind.BeginFixedEncounter));
                RejectUnchanged(fresh, host, CloseCommand(fresh), "ExpeditionCloseTacticalBoundary");
                var incomplete = BillAtDesk(ClosePolicy(), withEncounter: true);
                RejectUnchanged(incomplete, host, CloseCommand(incomplete), "ExpeditionCloseReconciledBillRequired");
                SaleCommit(incomplete, BillCommand(incomplete));
                WorldAdvance(incomplete, 1, 2);
                RejectUnchanged(incomplete, host, CloseCommand(incomplete), "ExpeditionCloseReconciledBillRequired");

                foreach (var entry in new[] {
                    (new TestOnlyExpeditionCloseProfile(mandateAuthorized: false), "ExpeditionCloseLeaderUnauthorized"),
                    (new TestOnlyExpeditionCloseProfile(evidenceAccessible: false), "ExpeditionCloseEvidenceUnavailable"),
                    (new TestOnlyExpeditionCloseProfile(declaresNoRecruitedCompanion: true), "ExpeditionCloseCoverageContradicted")
                }) {
                    var run = CloseReady(ClosePolicy(entry.Item1));
                    RejectUnchanged(run, host, CloseCommand(run), entry.Item2);
                    var query = run.QueryCommand(host, CloseCommand(run));
                    Require(query.Supported && !query.Admissible && query.Code == entry.Item2,
                        "Query silently accepted missing authority or contradicted coverage.");
                }

                var sim = CloseReady();
                RejectUnchanged(sim, host, CloseCommand(sim, actor: SaleSeller), "ExpeditionCloseLeaderUnauthorized");
                RejectUnchanged(sim, new Authority("without-hero", new[] { SaleSeller }), CloseCommand(sim), "NotAuthorized");
                RejectUnchanged(sim, host, CloseCommand(sim, target: "different-episode"), "ExpeditionCloseEpisodeMismatch");
                var projected = sim.Capture();
                projected.Characters = projected.Characters.Where(x => x.ActorId != SaleSeller).ToArray();
                Require(ClosePolicy().QueryCommand(projected, host, CloseCommand(sim)).Code == "ExpeditionCloseMemberFactsMissing",
                    "The admission projection replaced a missing mandatory member record with a guess.");
                WorldStep(sim, -1, 0, actor: SaleSeller);
                WorldAdvance(sim, 1, 2);
                RejectUnchanged(sim, host, CloseCommand(sim), "ExpeditionCloseUnresolvedTraversal");
                WorldAdvance(sim, 6);
                PortableCommit(sim, Portable(sim, CommandKind.HandlePortableEquipment, PortableKitFixture.Rations, handling: HandlingKind.Retrieve));
                WorldCommit(sim, IC(sim, CommandKind.StartIntake, PortableKitFixture.Rations, new InventoryRequest(new RuleQuantity(1))));
                RejectUnchanged(sim, host, CloseCommand(sim), "ExpeditionCloseOpenCommitments");
                WorldAdvance(sim, 900);
                SaleCommit(sim, CloseCommand(sim));
                Require(Closure(sim).Stock.Single(x => x.Stock.Id == PortableKitFixture.Rations).Stock.Amount == new RuleQuantity(19),
                    "A completed independent intake did not produce the actual changed stock for closure.");
            });
            cases.Add("mgt10_episode_close_captures_condition_and_actual_vendor_placement_after_offer_expiry", () =>
            {
                var clock = CloseReady().Capture().RuleClock.AddSeconds(18000);
                var condition = CCApply("episode-close-poison", "Poisoned", SaleSeller,
                    expires: new ConditionStamp(clock.AddSeconds(12)), at: new ConditionStamp(clock));
                var conditions = new ConditionCombatFixture(condition);
                var sim = CloseReady(ClosePolicy(conditions: conditions));
                WorldAdvance(sim, 17999);
                SaleCommit(sim, Portable(sim, CommandKind.HandlePortableEquipment, SaleTender, handling: HandlingKind.Drop, actor: SaleBuyer));
                var before = sim.Capture();
                Require(before.RuleClock == clock && before.RuleClock > before.ExpeditionBillCharter.AuthorizationUntil
                    && before.RuleClock > before.HavenMealPurchases.Single().Offer.ExpiresAt
                    && before.RuleClock > before.HavenSales.Single().Basis.ExpiresAt,
                    "Late closing witness failed to cross all historical service deadlines.");
                SaleCommit(sim, CCCommand(sim, "episode-close-poison", SaleSeller));
                SaleCommit(sim, CloseCommand(sim));
                var close = Closure(sim);
                var captured = close.Members.Single(x => x.ActorId == SaleSeller).Conditions.Single(x => x.Kind == "Poisoned");
                Require(captured.Effective && captured.Expires?.Time == clock.AddSeconds(12)
                    && close.Equipment.Single(x => x.Id == SaleTender).Placement == PortablePlacement.Ground
                    && close.Stock.Single(x => x.Stock.Id == SaleTender).Provenance.OwnerId == SaleBuyer,
                    "Closing failed to observe the lawful change in condition or title/custody evidence.");
                var replay = SaveBill(sim, ClosePolicy(conditions: conditions), directory, "mgt10-episode-close-conditioned");
                foreach (var branch in new[] { sim, replay }) {
                    WorldAdvance(branch, 18);
                    Require(!TestOnlyClubAttackPolicy.ConditionsFor(branch.Capture(), SaleSeller).View().Has(ConditionKind.Poisoned)
                        && Closure(branch).Members.Single(x => x.ActorId == SaleSeller).Conditions.Any(x => x.Kind == "Poisoned"),
                        "Later condition expiry rewrote the historical closing observation.");
                    SaleCommit(branch, Portable(branch, CommandKind.HandlePortableEquipment, SaleTender, handling: HandlingKind.Pickup, actor: SaleBuyer));
                    Require(Closure(branch).Equipment.Single(x => x.Id == SaleTender).Placement == PortablePlacement.Ground,
                        "Later custody rewrote closing placement.");
                }
                Require(Bytes(sim).SequenceEqual(Bytes(replay)), "Post-close condition and handling replay diverged.");
                WriteClosureAudit(directory, sim.Capture(), "condition-expiry-and-vendor-handling");
            });
            cases.Add("mgt10_episode_close_evidence_aggregates_interrupted_and_resumed_root_intakes", () =>
            {
                var sim = PurchasedMealForClose();
                InterruptCloseMeal(sim);
                EatMeal(sim, new RuleQuantity(1, 2));
                WorldAdvance(sim, 450);
                VerifyMealConsumptionClose(sim, directory, "interrupted-root", new[] { IntakeStatus.Interrupted, IntakeStatus.Complete },
                    new[] { new RuleQuantity(1, 6), new RuleQuantity(1, 2) }, new[] { HavenMealLot, HavenMealLot });
            });
            cases.Add("mgt10_episode_close_evidence_aggregates_two_completed_partial_intakes", () =>
            {
                var sim = PurchasedMealForClose();
                EatMeal(sim, new RuleQuantity(1, 3));
                WorldAdvance(sim, 300);
                WorldAdvance(sim, 6);
                EatMeal(sim, new RuleQuantity(1, 3));
                WorldAdvance(sim, 300);
                VerifyMealConsumptionClose(sim, directory, "two-complete-root", new[] { IntakeStatus.Complete, IntakeStatus.Complete },
                    new[] { new RuleQuantity(1, 3), new RuleQuantity(1, 3) }, new[] { HavenMealLot, HavenMealLot });
            });
            cases.Add("mgt10_episode_close_evidence_aggregates_descendant_portion_after_drop_and_return", () =>
            {
                var sim = PurchasedMealForClose();
                InterruptCloseMeal(sim);
                WorldCommit(sim, IC(sim, CommandKind.PortionInventory, HavenMealLot, new InventoryRequest(new RuleQuantity(1, 6)), SaleSeller));
                string child = sim.Capture().InventoryLots.Single(x => x.ParentId == HavenMealLot).LotId;
                PortableCommit(sim, HandleMeal(sim, HandlingKind.Drop));
                WorldAdvance(sim, 6);
                PortableCommit(sim, HandleMeal(sim, HandlingKind.Drop, child));
                WorldStep(sim, 1, 0, actor: SaleSeller);
                WorldAdvance(sim, 6);
                WorldStep(sim, -1, 0, actor: SaleSeller);
                WorldAdvance(sim, 6);
                PortableCommit(sim, HandleMeal(sim, HandlingKind.Pickup, child));
                WorldAdvance(sim, 6);
                EatMeal(sim, new RuleQuantity(1, 6), child);
                WorldAdvance(sim, 150);
                WorldAdvance(sim, 6);
                PortableCommit(sim, HandleMeal(sim, HandlingKind.Pickup));
                WorldAdvance(sim, 6);
                EatMeal(sim, new RuleQuantity(1, 3));
                WorldAdvance(sim, 300);
                VerifyMealConsumptionClose(sim, directory, "descendant-meal",
                    new[] { IntakeStatus.Interrupted, IntakeStatus.Complete, IntakeStatus.Complete },
                    new[] { new RuleQuantity(1, 6), new RuleQuantity(1, 6), new RuleQuantity(1, 3) },
                    new[] { HavenMealLot, child, HavenMealLot });
            });
            cases.Add("mgt10_episode_close_evidence_rejects_live_partial_and_unrelated_consumption", () =>
            {
                var sim = PurchasedMealForClose();
                SaleCommit(sim, BillCommand(sim));
                WorldAdvance(sim, 1800);
                EatMeal(sim, new RuleQuantity(2, 3));
                WorldAdvance(sim, 150);
                RejectUnchanged(sim, host, CloseCommand(sim), "ExpeditionCloseMealIntakeRequired");
                var first = sim.Capture().Intakes.Single();
                WorldCommit(sim, IC(sim, CommandKind.InterruptIntake, first.Id, actor: SaleSeller));
                WorldAdvance(sim, 6);
                RejectUnchanged(sim, host, CloseCommand(sim), "ExpeditionCloseMealIntakeRequired");

                PortableCommit(sim, Portable(sim, CommandKind.HandlePortableEquipment, PortableKitFixture.Rations, handling: HandlingKind.Retrieve));
                WorldCommit(sim, IC(sim, CommandKind.PortionInventory, PortableKitFixture.Rations, new InventoryRequest(new RuleQuantity(1, 2))));
                string ration = sim.Capture().InventoryLots.Single(x => x.ParentId == PortableKitFixture.Rations).LotId;
                WorldStep(sim, -1, 0);
                WorldAdvance(sim, 6);
                for (int step = 0; step < 3; step++) {
                    WorldStep(sim, 0, 1);
                    WorldAdvance(sim, 6);
                }
                PortableCommit(sim, Portable(sim, CommandKind.HandlePortableEquipment, ration, SaleSeller, HandlingKind.Handover));
                WorldAdvance(sim, 6);
                EatMeal(sim, new RuleQuantity(1, 2), ration);
                WorldAdvance(sim, 450);
                var unrelated = sim.Capture();
                Require(OrdinaryInventory.Consumed(unrelated, SaleSeller, NutritionKind.FoodPounds) == new RuleQuantity(2, 3)
                    && unrelated.Work.Lots.Single(x => x.Id == HavenMealLot).Amount == new RuleQuantity(1, 2),
                    "The same customer did not eat unrelated rations while leaving actual meal stock.");
                RejectUnchanged(sim, host, CloseCommand(sim), "ExpeditionCloseMealIntakeRequired");

                WorldAdvance(sim, 6);
                EatMeal(sim, new RuleQuantity(1, 2));
                WorldAdvance(sim, 450);
                SaleCommit(sim, CloseCommand(sim));
                var closed = sim.Capture();
                var close = closed.ExpeditionEpisodeClose;
                string unrelatedId = closed.Intakes.Single(x => x.LotId == ration).Id;
                Require(close.MealIntakeIds.Count == 2 && !close.MealIntakeIds.Contains(unrelatedId),
                    "Corrected closure attributed an unrelated intake to the purchased meal.");
                var codec = new SnapshotCodec();
                foreach (var ids in new[] { new[] { first.Id }, new[] { first.Id, unrelatedId } }) {
                    var forged = closed.Copy();
                    forged.ExpeditionEpisodeClose = AlterClose(close, intakeIds: ids);
                    Throws<ArgumentException>(() => codec.Encode(forged));
                }
                Throws<ArgumentException>(() => AlterClose(close, intakeIds: new[] { first.Id, first.Id }));
            });
            cases.Add("mgt10_episode_close_rejects_isolated_forged_history_and_projection", () =>
            {
                var sim = CloseReady();
                SaleCommit(sim, CloseCommand(sim));
                WorldStep(sim, -1, 0, actor: SaleSeller);
                WorldAdvance(sim, 6);
                var actual = sim.Capture();
                var close = actual.ExpeditionEpisodeClose;
                var codec = new SnapshotCodec();
                var recorded = close.Members.Single(x => x.ActorId == SaleSeller);
                var moved = new ExpeditionCloseMember(recorded.Life, new RuleQuantity(2), recorded.Y,
                    recorded.LastMovementRevision, recorded.AttainedLevels, recorded.Conditions);
                var falseMembers = close.Members.Select(x => x.ActorId == SaleSeller ? moved : x);
                var stock = close.Stock.Single(x => x.Stock.Id == PortableKitFixture.Rations);
                var falseStock = close.Stock.Select(x => x != stock ? x : new ExpeditionCloseStock(stock.Provenance,
                    new ResourceLot(stock.Stock.Id, stock.Stock.UnitId, new RuleQuantity(19), stock.Stock.LocationId, stock.Stock.CustodianId)));
                var falseCoverage = close.Coverage.Select(x => x.Field != ExpeditionCloseField.Pressure ? x
                    : new ExpeditionCloseCoverage(x.Field, ExpeditionCloseKnowledge.KnownValue, "invented-pressure-zero"));
                var hp = recorded.Life;
                var differentLife = new ActorLifeRecord(hp.ActorId, hp.MaximumHp, hp.Hp - 1, hp.TemporaryHp, hp.LinkedInjuries,
                    hp.Stable, hp.Dead, hp.UsesDeathSaves, hp.DeathSuccesses, hp.DeathFailures, hp.StableUntil,
                    hp.LastDeathTurn, hp.Prone, hp.HeldItems);
                var hurt = new ExpeditionCloseMember(differentLife, recorded.X, recorded.Y, recorded.LastMovementRevision,
                    recorded.AttainedLevels, recorded.Conditions);
                foreach (var forged in new[] { AlterClose(close, members: falseMembers),
                    AlterClose(close, members: close.Members.Select(x => x.ActorId == SaleSeller ? hurt : x)),
                    AlterClose(close, stock: falseStock), AlterClose(close, coverage: falseCoverage) }) {
                    var state = actual.Copy();
                    state.ExpeditionEpisodeClose = forged;
                    var structurallyValid = codec.Decode(codec.Encode(state));
                    try {
                        new Simulation(ClosePolicy(), structurallyValid, ExecutionProfile.Laboratory);
                        throw new Exception("Canonical replay accepted a coherently encoded false close.");
                    } catch (ArgumentException error) {
                        Require(error.Message == "InvalidSharedWorldReplay", "Forgery did not isolate the historical projection: " + error.Message);
                    }
                }
                foreach (var forged in new[] {
                    AlterClose(close, outcome: new ExpeditionCloseOutcome(close.Outcome.PrimaryMetric, 3, close.Outcome.NetTargetCopper,
                        close.Outcome.RealizedGrossCopper, close.Outcome.GrossTargetCopper, close.Outcome.ProfitTargetCopper)),
                    AlterClose(close, billRevision: close.BillReportRevision - 1),
                    AlterClose(close, sourceRevision: close.SourceRevision + 1) }) {
                    var state = actual.Copy();
                    state.ExpeditionEpisodeClose = forged;
                    Throws<ArgumentException>(() => codec.Encode(state));
                }
            });
        }

        private static Simulation PurchasedMealForClose()
        {
            var sim = MealAtCounter(ClosePolicy(), withEncounter: true);
            SaleCommit(sim, PurchaseMeal(sim));
            return sim;
        }

        private static void InterruptCloseMeal(Simulation sim)
        {
            EatMeal(sim, new RuleQuantity(2, 3));
            WorldAdvance(sim, 150);
            WorldCommit(sim, IC(sim, CommandKind.InterruptIntake, sim.Capture().Intakes.Single().Id, actor: SaleSeller));
            WorldAdvance(sim, 6);
        }

        private static void VerifyMealConsumptionClose(Simulation sim, string directory, string name,
            IntakeStatus[] statuses, RuleQuantity[] amounts, string[] lots)
        {
            var before = sim.Capture();
            var entries = before.Intakes.OrderBy(x => x.StartedAt).ToArray();
            var debits = entries.Select(x => before.Work.Reservations.Single(r => r.Id == x.ReservationId)).ToArray();
            Require(entries.Select(x => x.Status).SequenceEqual(statuses) && entries.Select(x => x.LotId).SequenceEqual(lots)
                && debits.Select(x => x.ConsumedAmount).SequenceEqual(amounts) && debits.All(x => x.RemainingAmount == default)
                && lots.Distinct().All(id => before.Work.Lots.Single(x => x.Id == id).Amount == default)
                && RuleQuantity.Sum(amounts) == new RuleQuantity(2, 3), "The actual terminal meal debits were not established.");
            WorldAdvance(sim, 6);
            SaleCommit(sim, BillCommand(sim));
            WorldAdvance(sim, 1800);
            var replay = SaveBill(sim, ClosePolicy(), directory, name + "-before-close");
            var command = CloseCommand(sim);
            byte[] beforeQuery = Bytes(sim);
            Require(sim.QueryCommand(HavenSaleHost(), command).Admissible && beforeQuery.SequenceEqual(Bytes(sim)),
                "Closure preview rejected the fully consumed serving or changed state.");
            foreach (var branch in new[] { sim, replay }) {
                SaleCommit(branch, command);
                var captured = Closure(branch);
                Require(captured.MealIntakeIds.SequenceEqual(entries.Select(x => x.Id).OrderBy(x => x, StringComparer.Ordinal))
                    && captured.ClosedAt == branch.Capture().RuleClock && captured.Outcome.RealizedNetCopper == 2,
                    "The close did not retain the complete exact terminal meal history.");
                WorldStep(branch, 1, 0, actor: SaleSeller);
                WorldAdvance(branch, 2);
                Require(ReferenceEquals(Closure(branch), captured), "Later movement rewrote closed meal evidence.");
            }
            Require(Bytes(sim).SequenceEqual(Bytes(replay)), "Restored meal history did not replay the same close and continuation.");
            SaveBill(sim, ClosePolicy(), directory, name + "-after-close");
            WriteClosureAudit(directory, sim.Capture(), "ordinary-movement");
        }

        private static ExpeditionEpisodeCloseRecord AlterClose(ExpeditionEpisodeCloseRecord close,
            ExpeditionCloseOutcome outcome = null, IEnumerable<ExpeditionCloseMember> members = null,
            IEnumerable<ExpeditionCloseStock> stock = null, IEnumerable<ExpeditionCloseCoverage> coverage = null,
            long? billRevision = null, long? sourceRevision = null, IEnumerable<string> intakeIds = null)
            => new ExpeditionEpisodeCloseRecord(close.EpisodeId, close.CharterVersionId, close.CloserId, close.MandateId,
                close.EvidenceAuthorityId, close.CommandId, sourceRevision ?? close.SourceRevision, close.ClosedAt,
                close.BillId, billRevision ?? close.BillReportRevision, close.EncounterId, close.EncounterExitRevision,
                close.HostileId, close.HostileX, close.HostileY, close.MiningAttemptId, intakeIds ?? close.MealIntakeIds, outcome ?? close.Outcome,
                members ?? close.Members, close.MiningDispositions, stock ?? close.Stock, close.Equipment, close.Vessels, coverage ?? close.Coverage);

        private static void CheckClosureCoverage(ExpeditionEpisodeCloseRecord close)
        {
            var known = new[] { ExpeditionCloseField.Outcome, ExpeditionCloseField.MembersAndLocations, ExpeditionCloseField.LifeAndInjuries,
                ExpeditionCloseField.Conditions, ExpeditionCloseField.ProvisionsAndContainers, ExpeditionCloseField.Movement,
                ExpeditionCloseField.Companions, ExpeditionCloseField.HostileDeath, ExpeditionCloseField.CargoTitleAndCustody,
                ExpeditionCloseField.MiningDispositions, ExpeditionCloseField.QuotesAndPayments };
            var none = new[] { ExpeditionCloseField.NamedRouteTravel, ExpeditionCloseField.Camps, ExpeditionCloseField.Pursuit,
                ExpeditionCloseField.Devices, ExpeditionCloseField.HarvestAndSalvageClaims, ExpeditionCloseField.Insurance,
                ExpeditionCloseField.FactionActions, ExpeditionCloseField.RecordedAdvancement };
            var unresolved = new[] { ExpeditionCloseField.ResourcePools, ExpeditionCloseField.Pressure, ExpeditionCloseField.Strain,
                ExpeditionCloseField.RestDebt, ExpeditionCloseField.CorpseHandling, ExpeditionCloseField.WiderLiabilitiesAndProfit,
                ExpeditionCloseField.StandingAndRenown, ExpeditionCloseField.UnadjudicatedEntitlements };
            Require(known.All(x => close.StatusOf(x).Knowledge == ExpeditionCloseKnowledge.KnownValue)
                && none.All(x => close.StatusOf(x).Knowledge == ExpeditionCloseKnowledge.KnownNone)
                && unresolved.All(x => close.StatusOf(x).Knowledge == ExpeditionCloseKnowledge.Unresolved)
                && close.StatusOf(ExpeditionCloseField.Heat).Knowledge == ExpeditionCloseKnowledge.NotApplicable
                && close.Coverage.Count == known.Length + none.Length + unresolved.Length + 1
                && close.Coverage.All(x => !string.IsNullOrEmpty(x.BasisId)),
                "The close omitted or silently resolved a required coverage category.");
        }

        private static void WriteClosureAudit(string directory, Snapshot state, string continuation)
        {
            var close = state.ExpeditionEpisodeClose;
            var bill = state.ExpeditionBills.Single();
            var sale = state.HavenSales.Single();
            var meal = state.HavenMealPurchases.Single();
            var appraisal = state.HavenAppraisals.Single();
            var rows = new List<string> {
                "event\ttime\trevision\tdetail",
                string.Join("\t", "bill-cutoff", bill.Basis.AccountingCutoff, bill.Basis.CutoffRevision, bill.Basis.SaleId + "/" + bill.Basis.MealId),
                string.Join("\t", "bill-observation", bill.UpdatedAt, bill.UpdatedRevision, bill.Report.OwnerId + "/" + bill.Report.PhysicalCount),
                string.Join("\t", "appraisal", appraisal.UpdatedAt, appraisal.UpdatedRevision, appraisal.Id + "/value-" + appraisal.ResultCopper),
                string.Join("\t", "sale", sale.UpdatedAt, sale.UpdatedRevision, sale.Id + "/quote-" + sale.Basis.ExactQuoteCopper + "/paid-" + sale.PaymentCopper),
                string.Join("\t", "meal", meal.EndedAt, meal.Revision, meal.Id + "/quote-" + meal.Offer.ExactQuoteCopper + "/paid-" + meal.PaymentCopper),
                string.Join("\t", "episode-close", close.ClosedAt, close.CloseRevision, close.EpisodeId + "/" + close.SourceRevision),
                string.Join("\t", "primary-net", close.ClosedAt, close.CloseRevision, close.Outcome.RealizedNetCopper + "/target-" + close.Outcome.NetTargetCopper + "/unmet"),
                string.Join("\t", "gross", close.ClosedAt, close.CloseRevision, close.Outcome.RealizedGrossCopper + "/target-" + close.Outcome.GrossTargetCopper + "/met"),
                string.Join("\t", "profit", close.ClosedAt, close.CloseRevision, "target-" + close.Outcome.ProfitTargetCopper + "/unevaluated")
            };
            rows.AddRange(close.Members.Select(x => string.Join("\t", "member-" + x.ActorId, close.ClosedAt, close.CloseRevision,
                x.X + "," + x.Y + "/HP-" + x.Life.Hp + "/" + x.Life.MaximumHp)));
            rows.AddRange(close.MealIntakeIds.Select(id => {
                var intake = state.Intakes.Single(x => x.Id == id);
                var debit = state.Work.Reservations.Single(x => x.Id == intake.ReservationId);
                return string.Join("\t", "meal-intake-" + id, intake.EndedAt, close.CloseRevision,
                    intake.LotId + "/" + intake.Status + "/" + debit.ConsumedAmount);
            }));
            rows.AddRange(close.MiningDispositions.Select(x => string.Join("\t", "mining-" + x.UnitId, close.ClosedAt,
                close.CloseRevision, x.Status)));
            rows.AddRange(close.Stock.Select(x => string.Join("\t", "stock-" + x.Stock.Id, close.ClosedAt, close.CloseRevision,
                x.Stock.Amount + "/" + x.Provenance.OwnerId + "/" + x.Stock.CustodianId + "/" + x.Stock.LocationId)));
            rows.AddRange(close.Members.SelectMany(x => x.Conditions.Select(c => string.Join("\t", "condition-" + x.ActorId,
                close.ClosedAt, close.CloseRevision, c.Kind + "/expiry-" + c.Expires?.Time))));
            rows.AddRange(close.Coverage.Select(x => string.Join("\t", "coverage-" + x.Field, close.ClosedAt, close.CloseRevision,
                x.Knowledge + "/" + x.BasisId)));
            rows.Add(string.Join("\t", "continued", state.RuleClock, state.Revision, continuation));
            File.WriteAllLines(Path.Combine(directory, "episode-close-audit.tsv"), rows);
        }
    }
}
#endif
