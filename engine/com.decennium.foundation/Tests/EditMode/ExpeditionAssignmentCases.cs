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
        private static Command ExpeditionCommand(Simulation s, CommandKind kind, string target = "",
            ExpeditionAssignmentRequest request = null, string actor = TestOnlyPolicy.CompanionId)
        {
            var state = s.Capture();
            return new Command("expedition.assignment.command." + (state.Revision + 1), actor, state.Revision,
                kind, target, expeditionAssignment: request);
        }

        private static void AddExpeditionAssignmentCases(Dictionary<string, Action> cases, string directory)
        {
            var host = TestOnlySharedWorldPolicy.Host();
            const string worker = TestOnlyPolicy.CompanionId;
            cases.Add("expedition_assignment_persists_travel_readiness_and_dispatches_existing_repair", () => {
                var policy = TestOnlySharedWorldPolicy.WithFishingTrapAndRepair(new SharedFishingTrapFixture(12, 1),
                    new SharedRepairFixture(siteX: 1, siteY: 3), new SharedCraftingFixture(toolHp: 0));
                var s = World(policy); var initial = s.Capture();
                Require(initial.SchemaVersion == Snapshot.ExpeditionAssignmentSchema, "Assignment fixture did not select its versioned schema.");
                var beforeWork = initial.Work;
                var request = new ExpeditionAssignmentRequest(ExpeditionWorkProcedure.ToolRepair, SharedCraftingFixture.ToolId);
                WorldCommit(s, ExpeditionCommand(s, CommandKind.AssignExpeditionWork, request: request));
                var assigned = s.Capture(); var assignment = assigned.ExpeditionAssignments.Single();
                Require(assignment.Status == ExpeditionAssignmentStatus.Travelling && assignment.SiteX == 1 && assignment.SiteY == 3
                    && assigned.RuleClock == initial.RuleClock && assigned.Work.WorkerIntervals.Count == beforeWork.WorkerIntervals.Count
                    && assigned.Work.Reservations.Count == beforeWork.Reservations.Count
                    && assigned.Work.Lots.Select(x => x.Id + "|" + x.Amount).SequenceEqual(beforeWork.Lots.Select(x => x.Id + "|" + x.Amount)),
                    "Assignment changed the clock, work ledger, or authored work-site location.");
                RejectUnchanged(s, host, ExpeditionCommand(s, CommandKind.StartExpeditionWork, assignment.Id), "ExpeditionAssignmentNotReady");
                WorldStep(s, -1, 0, actor: worker); WorldAdvance(s, 2, 5);
                Require(s.Capture().WorldTraversals.Single().DistanceFeet == new RuleQuantity(2)
                    && s.Capture().ExpeditionAssignments.Single().Status == ExpeditionAssignmentStatus.Travelling,
                    "Partial travel prematurely marked the worker ready.");
                string path = Path.Combine(directory, "expedition-repair-midroute.bin");
                new FileSaveStore().Save(path, s.Capture());
                s = new Simulation(policy, new FileSaveStore().Load(path), ExecutionProfile.Laboratory);
                WorldAdvance(s, 3, 5); Require(s.Capture().Actors.Single(x => x.Id == worker).X == 2
                    && s.Capture().ExpeditionAssignments.Single().Status == ExpeditionAssignmentStatus.Travelling,
                    "Restored first route edge lost its destination or readiness state.");
                WorldStep(s, -1, 0, actor: worker); WorldAdvance(s, 1);
                assignment = s.Capture().ExpeditionAssignments.Single();
                Require(assignment.Status == ExpeditionAssignmentStatus.Ready && s.Capture().Actors.Single(x => x.Id == worker).X == 1,
                    "Arrival at the authored repair site did not mark the assignment ready.");
                var start = ExpeditionCommand(s, CommandKind.StartExpeditionWork, assignment.Id);
                WorldCommit(s, start);
                assignment = s.Capture().ExpeditionAssignments.Single();
                var job = s.Capture().RepairWork.Single();
                Require(assignment.Status == ExpeditionAssignmentStatus.Started && assignment.WorkId == job.Id
                    && job.WorkerId == worker && job.TargetId == SharedCraftingFixture.ToolId,
                    "Assignment did not dispatch through the existing repair transaction.");
                var receipt = s.Capture().Receipts.Single(x => x.Id == start.Id);
                Require(CommandHistory.Read(receipt).MatchesReceipt(receipt), "Assignment start receipt did not round-trip.");
                var restored = new Simulation(policy, new SnapshotCodec().Decode(Bytes(s)), ExecutionProfile.Laboratory);
                Require(Bytes(s).SequenceEqual(Bytes(restored)) && restored.Capture().ExpeditionAssignments.Single().WorkId == job.Id,
                    "Started assignment or linked procedure changed across save/restore.");
            });

            cases.Add("expedition_assignment_travels_to_mine_and_dispatches_shared_extraction", () => {
                var fixture=new SharedMiningFixture(siteX:1,siteY:3);
                var unseeded=TestOnlySharedWorldPolicy.WithMining(fixture).EnableExpeditionAssignments();
                uint seed=MiningSeedFor(TaskDegree.Success,MiningModifier(unseeded.Initial()));
                var policy=TestOnlySharedWorldPolicy.WithMining(fixture,seed).EnableExpeditionAssignments();
                var s=World(policy);var initial=s.Capture();
                Require(initial.SchemaVersion==Snapshot.MiningExpeditionAssignmentSchema
                    &&initial.WorldActivityIntervals.Any(x=>x.ActorId==worker),
                    "Mining assignments did not select schema47 with the shared off-calendar activity ledger.");
                var selection=new MiningSelectionRequest(SharedMiningFixture.DepositVersionId,
                    new[]{SharedMiningFixture.CategoryA},MiningAbilityChoice.Wisdom);
                var request=new ExpeditionAssignmentRequest(ExpeditionWorkProcedure.MiningExtraction,
                    SharedMiningFixture.DepositId,miningSelection:selection);
                var assign=ExpeditionCommand(s,CommandKind.AssignExpeditionWork,request:request,actor:worker);
                WorldCommit(s,assign);
                var assignment=s.Capture().ExpeditionAssignments.Single();
                Require(assignment.Status==ExpeditionAssignmentStatus.Travelling&&assignment.SiteX==1&&assignment.SiteY==3
                    &&assignment.MiningSelection.CategoryIds.SequenceEqual(new[]{SharedMiningFixture.CategoryA})
                    &&s.Capture().RuleClock==initial.RuleClock&&s.Capture().MiningAttempts.Length==0
                    &&s.Capture().Work.Reservations.Count==initial.Work.Reservations.Count,
                    "Assigning extraction changed time/stock or failed to preserve the selected procedure.");
                var receipt=s.Capture().Receipts.Single(x=>x.Id==assign.Id);
                var replayed=CommandHistory.Read(receipt);
                Require(replayed.ExpeditionAssignment.MiningSelection.DepositVersionId==selection.DepositVersionId
                    &&replayed.ExpeditionAssignment.MiningSelection.CategoryIds.SequenceEqual(selection.CategoryIds),
                    "Mining assignment receipt did not reconstruct its explicit extraction choice.");

                WorldStep(s,-1,0,actor:worker);WorldAdvance(s,1);
                Require(s.Capture().ExpeditionAssignments.Single().Status==ExpeditionAssignmentStatus.Travelling,
                    "Partial route travel marked the mine assignment ready early.");
                WorldStep(s,-1,0,actor:worker);WorldAdvance(s,1);
                assignment=s.Capture().ExpeditionAssignments.Single();
                Require(assignment.Status==ExpeditionAssignmentStatus.Ready&&s.Capture().Actors.Single(x=>x.Id==worker).X==1,
                    "Arrival did not make the companion's mine assignment ready.");

                var start=ExpeditionCommand(s,CommandKind.StartExpeditionWork,assignment.Id,actor:worker);
                WorldCommit(s,start);
                assignment=s.Capture().ExpeditionAssignments.Single();
                var attempt=s.Capture().MiningAttempts.Single();
                Require(assignment.Status==ExpeditionAssignmentStatus.Started&&assignment.WorkId==attempt.Id
                    &&attempt.WorkerId==worker&&attempt.DepositId==SharedMiningFixture.DepositId
                    &&attempt.SelectedCategoryIds.SequenceEqual(selection.CategoryIds)
                    &&attempt.Ability==selection.Ability&&attempt.Status==MiningAttemptStatus.Working,
                    "Assignment did not delegate into the existing shared mining transaction.");
                var midwork=Bytes(s);
                s=new Simulation(policy,new SnapshotCodec().Decode(midwork),ExecutionProfile.Laboratory);
                Require(midwork.SequenceEqual(Bytes(s)),"Assigned mining work or selection changed on save/restore.");
                WorldAdvance(s,1800);
                var completed=s.Capture();attempt=completed.MiningAttempts.Single();
                Require(attempt.Status==MiningAttemptStatus.Success&&completed.MiningUnits.Single(x=>x.Id==SharedMiningFixture.UnitA).Status==MiningUnitStatus.Extracted
                    &&completed.MiningUnits.Single(x=>x.Id==SharedMiningFixture.UnitA).ReceivedContainerId==SharedMiningFixture.ReceiverId
                    &&completed.ExpeditionAssignments.Single().WorkId==attempt.Id,
                    "Assigned extraction did not settle finite mineral stock through the shared mining resolver.");
                var settled=Bytes(s);var duplicate=s.Execute(host,assign);
                Require(duplicate.Outcome==Outcome.Duplicate&&settled.SequenceEqual(Bytes(s)),
                    "Duplicate mining assignment replay changed travel, stock or work state.");
            });

            cases.Add("expedition_assignment_travels_to_physical_trap_and_reuses_retrieval", () => {
                var fixture = new SharedFishingTrapFixture(12, 1, identity: "assigned-trap",
                    setterId: TestOnlyPolicy.CompanionId, trapOwnerId: TestOnlyPolicy.ActorId);
                uint seed = TrapSeedForDegree(fixture, TaskDegree.Success);
                var policy = TestOnlySharedWorldPolicy.WithFishingTrap(fixture, seed).EnableExpeditionAssignments();
                var s = World(policy);
                WorldCommit(s, TrapOp(s, FishingTrapInteraction.Set, "assignment-trap-set", worker, fixture.TrapIdentity));
                WorldAdvance(s, 3300);
                var attempt = s.Capture().FishingTrapAttempts.Single();
                Require(attempt.CheckOutcome == FishingTrapCheckOutcome.CapturedInTrap, "Fixture did not produce a retrieval-ready physical catch.");
                var request = new ExpeditionAssignmentRequest(ExpeditionWorkProcedure.FishingTrapRetrieval,
                    fixture.TrapIdentity, fixture.ReceiverIdentity);
                WorldCommit(s, ExpeditionCommand(s, CommandKind.AssignExpeditionWork, request: request));
                var assignment = s.Capture().ExpeditionAssignments.Single();
                Require(assignment.Status == ExpeditionAssignmentStatus.Travelling && assignment.SiteX == fixture.TrapX
                    && assignment.SiteY == fixture.TrapY, "Trap assignment did not derive its site from the physical Trap.");
                WorldStep(s, 0, 1, actor: worker); WorldAdvance(s, 1);
                assignment = s.Capture().ExpeditionAssignments.Single();
                Require(assignment.Status == ExpeditionAssignmentStatus.Ready, "Worker did not become ready at the physical Trap.");
                var start = ExpeditionCommand(s, CommandKind.StartExpeditionWork, assignment.Id);
                RejectUnchanged(s, new Authority("worker-without-trap-owner", new[] { worker }), start, "InventoryNotAuthorized");
                var workerAndOwner = new Authority("worker-with-trap-owner", new[] { worker },
                    inventoryOwners: new[] { TestOnlyPolicy.ActorId });
                var startResult = s.Execute(workerAndOwner, start);
                Require(startResult.Outcome == Outcome.Committed, "Authorized worker could not start Trap retrieval after the missing-owner rejection.");
                assignment = s.Capture().ExpeditionAssignments.Single();
                var retrieval = s.Capture().FishingTrapRetrievals.Single();
                Require(assignment.Status == ExpeditionAssignmentStatus.Started && assignment.WorkId == retrieval.Id
                    && retrieval.WorkerId == worker && retrieval.TrapId == fixture.TrapIdentity
                    && retrieval.DestinationId == fixture.ReceiverIdentity,
                    "Assignment did not dispatch through the existing physical retrieval handler.");
                var bytes = Bytes(s); var restored = new Simulation(policy, new SnapshotCodec().Decode(bytes), ExecutionProfile.Laboratory);
                Require(bytes.SequenceEqual(Bytes(restored)) && restored.Capture().ExpeditionAssignments.Single().WorkId == retrieval.Id,
                    "Trap retrieval assignment or job link changed across save/restore.");
            });

            cases.Add("expedition_assignment_cancellation_has_no_work_or_item_side_effect", () => {
                var policy = TestOnlySharedWorldPolicy.WithFishingTrapAndRepair(new SharedFishingTrapFixture(12, 1),
                    new SharedRepairFixture(siteX: 1, siteY: 3), new SharedCraftingFixture(toolHp: 0));
                var s = World(policy);
                var request = new ExpeditionAssignmentRequest(ExpeditionWorkProcedure.ToolRepair, SharedCraftingFixture.ToolId);
                WorldCommit(s, ExpeditionCommand(s, CommandKind.AssignExpeditionWork, request: request));
                var id = s.Capture().ExpeditionAssignments.Single().Id;
                WorldCommit(s, ExpeditionCommand(s, CommandKind.CancelExpeditionWork, id));
                var state = s.Capture();
                Require(state.ExpeditionAssignments.Single().Status == ExpeditionAssignmentStatus.Cancelled
                    && state.RepairWork.Length == 0 && state.Work.Reservations.Count == 0
                    && state.Work.WorkerIntervals.Count == 0 && state.RuleClock == default,
                    "Cancelling assignment started or charged work.");
            });

            cases.Add("expedition_assignment_capacity_counts_closed_history_records", () => {
                var policy = TestOnlySharedWorldPolicy.WithFishingTrapAndRepair(new SharedFishingTrapFixture(12, 1),
                    new SharedRepairFixture(siteX: 1, siteY: 3), new SharedCraftingFixture(toolHp: 0));
                var state = policy.Initial();
                state.ExpeditionAssignments = Enumerable.Range(0, ExpeditionAssignmentValidation.MaxAssignments)
                    .Select(i => new ExpeditionWorkAssignmentRecord("closed.assignment." + i, worker,
                        ExpeditionWorkProcedure.ToolRepair, SharedCraftingFixture.ToolId, "", 1, 3,
                        default, default, ExpeditionAssignmentStatus.Cancelled)).ToArray();
                ExpeditionAssignmentValidation.Validate(state);
                Require(!ExpeditionAssignmentValidation.HasCapacity(state), "Closed assignment history was ignored by capacity check.");
                state.ExpeditionAssignments = state.ExpeditionAssignments.Take(ExpeditionAssignmentValidation.MaxAssignments - 1).ToArray();
                Require(ExpeditionAssignmentValidation.HasCapacity(state), "One remaining history slot was not available.");
            });

            cases.Add("off_calendar_activity_uses_fixed_six_second_dash_and_persists_without_initiative", () => {
                var fractionalCalendar = new WorldScheduleRecord("world.fractional", new RuleTime(1, 3), new[] { "hero", "guard" });
                Require(WorldActivityIntervalRecord.IndexAt(fractionalCalendar, new RuleTime(1, 3)) == 0
                    && WorldActivityIntervalRecord.EndAt(fractionalCalendar, 0) == new RuleTime(19, 3)
                    && WorldActivityIntervalRecord.IndexAt(fractionalCalendar, new RuleTime(19, 3)) == 1
                    && WorldActivityIntervalRecord.EndAt(fractionalCalendar, 1) == new RuleTime(37, 3)
                    && WorldActivityIntervalRecord.IndexAt(fractionalCalendar, new RuleTime(37, 3)) == 2,
                    "Fractional calendar origin shifted a six-second activity boundary.");
                var policy = TestOnlySharedWorldPolicy.WithFishingTrapAndRepair(new SharedFishingTrapFixture(12, 1),
                    new SharedRepairFixture(siteX: 1, siteY: 3), new SharedCraftingFixture(toolHp: 0), walkingSpeed: 1)
                    .EnableOffCalendarActivity();
                var s = World(policy); var initial = s.Capture();
                Require(initial.SchemaVersion == Snapshot.OffCalendarActivitySchema && initial.WorldActivityIntervals.Length == 1
                    && initial.WorldActivityIntervals[0].IntervalIndex == 0 && initial.WorldSchedule.Order.Count == 2
                    && !initial.WorldSchedule.Order.Contains(worker) && initial.WorldIntervals.All(x => x.ActorId != worker),
                    "Activity allowance became an initiative turn or selected the wrong schema.");
                var run = IC(s, CommandKind.BeginWorldStep, "run", actor: worker, x: -1); WorldCommit(s, run); WorldAdvance(s, 1);
                var activity = s.Capture().WorldActivityIntervals.Single();
                Require(activity.DashPaid && activity.ActionReference == run.Id && activity.MovementSpent == new RuleQuantity(1, 3)
                    && activity.ActionReferenceRevision == s.Capture().Receipts.Single(x => x.Principal == host.Principal && x.Id == run.Id).Revision
                    && s.Capture().WorldTraversals.Single().DistanceFeet == new RuleQuantity(1, 3),
                    "Off-calendar run did not persist its paid Dash and exact movement cost.");
                byte[] saved = Bytes(s); s = new Simulation(policy, new SnapshotCodec().Decode(saved), ExecutionProfile.Laboratory);
                Require(saved.SequenceEqual(Bytes(s)), "Off-calendar activity save/restore changed spending or traversal.");
                WorldCommit(s, IC(s, CommandKind.SuspendWorldStep, actor: worker)); var beforeResume = s.Capture().WorldActivityIntervals.Single();
                var sameIntervalResume = IC(s, CommandKind.ResumeWorldStep, actor: worker); WorldCommit(s, sameIntervalResume);
                activity = s.Capture().WorldActivityIntervals.Single();
                Require(activity.DashPaid && activity.ActionReference == run.Id && activity.MovementSpent == beforeResume.MovementSpent,
                    "Pause/resume refilled or re-paid the current activity interval.");
                WorldAdvance(s, 5); activity = s.Capture().WorldActivityIntervals.Single();
                Require(s.Capture().RuleClock == T(6) && activity.IntervalIndex == 1 && activity.DashPaid
                    && activity.ActionReference == run.Id && activity.ActionReferenceRevision == 1
                    && activity.MovementSpent == default && s.Capture().WorldTraversals.Single().Status == WorldTraversalStatus.Moving,
                    "The still-running route did not automatically pay one fresh Dash at the fixed boundary.");
                byte[] boundarySave = Bytes(s);
                s = new Simulation(policy, new SnapshotCodec().Decode(boundarySave), ExecutionProfile.Laboratory);
                Require(boundarySave.SequenceEqual(Bytes(s)) && s.Capture().WorldActivityIntervals.Single().DashPaid,
                    "Save/load at a boundary skipped or duplicated the automatic Dash payment.");
                WorldAdvance(s, 6); activity = s.Capture().WorldActivityIntervals.Single();
                Require(s.Capture().RuleClock == T(12) && activity.IntervalIndex == 2 && activity.DashPaid
                    && activity.ActionReference == run.Id && activity.MovementSpent == default
                    && s.Capture().WorldTraversals.Single().Status == WorldTraversalStatus.Moving
                    && s.Capture().WorldSchedule.Order.Count == 2 && s.Capture().WorldIntervals.All(x => x.ActorId != worker)
                    && !s.Capture().InventoryCombat && s.Capture().LifeEvents.Length == 0,
                    "Off-calendar activity failed to renew its route without creating a tactical turn or life marker.");

                var suspendedRoute = World(policy);
                WorldCommit(suspendedRoute, IC(suspendedRoute, CommandKind.BeginWorldStep, "run", actor: worker, x: -1));
                WorldCommit(suspendedRoute, IC(suspendedRoute, CommandKind.SuspendWorldStep, actor: worker));
                WorldAdvance(suspendedRoute, 6);
                Require(suspendedRoute.Capture().WorldTraversals.Single().Status == WorldTraversalStatus.Suspended
                    && !suspendedRoute.Capture().WorldActivityIntervals.Single().DashPaid,
                    "A voluntarily suspended route automatically paid Dash at a later boundary.");
                suspendedRoute = new Simulation(policy, new SnapshotCodec().Decode(Bytes(suspendedRoute)), ExecutionProfile.Laboratory);
                WorldAdvance(suspendedRoute, 6);
                Require(suspendedRoute.Capture().WorldTraversals.Single().Status == WorldTraversalStatus.Suspended
                    && !suspendedRoute.Capture().WorldActivityIntervals.Single().DashPaid,
                    "A saved voluntary pause automatically renewed on a later interval.");

                var missingOrigin = s.Capture();
                var originalEdge = missingOrigin.WorldTraversals.Single();
                missingOrigin.WorldTraversals = new[] { new WorldTraversalRecord(originalEdge.ActorId, originalEdge.StartedRevision + 100,
                    originalEdge.FromX, originalEdge.FromY, originalEdge.ToX, originalEdge.ToY, originalEdge.DistanceFeet,
                    originalEdge.Running, originalEdge.Status) };
                Throws<ArgumentException>(() => Validation.Snapshot(missingOrigin));

                var collisionWorld = World(policy);
                var collisionRun = new Command("activity.shared.command", worker, collisionWorld.Capture().Revision,
                    CommandKind.BeginWorldStep, "run", x: -1);
                WorldCommit(collisionWorld, collisionRun); WorldAdvance(collisionWorld, 1);
                var reusedId = new Command(collisionRun.Id, TestOnlyPolicy.ActorId, collisionWorld.Capture().Revision,
                    CommandKind.AdvanceClock, x: 1, y: 1);
                var secondPrincipal = new Authority("TEST_ONLY.second-principal", new[] { TestOnlyPolicy.ActorId }, canAdvanceClock: true);
                var reusedIdResult = collisionWorld.Execute(secondPrincipal, reusedId);
                Require(reusedIdResult.Outcome == Outcome.Committed
                    && collisionWorld.Capture().Receipts.Count(x => x.Id == collisionRun.Id) == 2
                    && collisionWorld.Capture().WorldActivityIntervals.Single().ActionReferenceRevision == 1,
                    "A second principal reusing a command ID made the paid Dash reference ambiguous.");
                var forgedDuplicate = collisionWorld.Capture();
                var originalReceipt = forgedDuplicate.Receipts.Single(x => x.Id == collisionRun.Id && x.Revision == 1);
                var duplicateRevisionReceipt = originalReceipt.Copy();
                duplicateRevisionReceipt.Principal = "TEST_ONLY.other-principal";
                forgedDuplicate.Receipts = forgedDuplicate.Receipts.Concat(new[] { duplicateRevisionReceipt }).ToArray();
                Throws<ArgumentException>(() => Validation.Snapshot(forgedDuplicate));

                var schema39 = TestOnlySharedWorldPolicy.WithFishingTrapAndRepair(new SharedFishingTrapFixture(12, 1),
                    new SharedRepairFixture(siteX: 1, siteY: 3), new SharedCraftingFixture(toolHp: 0)).Initial();
                var codec = new SnapshotCodec(); var oldBytes = codec.Encode(schema39); var oldDecoded = codec.Decode(oldBytes);
                Require(schema39.SchemaVersion == Snapshot.ExpeditionAssignmentSchema && schema39.WorldActivityIntervals.Length == 0
                    && oldDecoded.SchemaVersion == schema39.SchemaVersion && codec.Encode(oldDecoded).SequenceEqual(oldBytes),
                    "Schema39 wire bytes changed when activity accounting was added.");
            });

            cases.Add("off_calendar_action_and_worker_claims_share_the_fixed_activity_interval", () => {
                var policy = TestOnlySharedWorldPolicy.WithFishingTrapAndRepair(new SharedFishingTrapFixture(12, 1),
                    new SharedRepairFixture(siteX: 1, siteY: 3), new SharedCraftingFixture(toolHp: 0))
                    .EnableOffCalendarActivity();
                var s = World(policy);
                foreach (var delta in new[] { new[] { 1, 0 }, new[] { 0, 1 }, new[] { 0, 1 }, new[] { 0, 1 }, new[] { 1, 0 } }) {
                    WorldStep(s, delta[0], delta[1]); WorldAdvance(s, 1);
                }
                WorldCommit(s, IC(s, CommandKind.HandleInventory, TestOnlyInventoryPolicy.FoodId,
                    new InventoryRequest(new RuleQuantity(1), handling: HandlingKind.Drop), TestOnlyPolicy.ActorId));
                string dropped = s.Capture().InventoryLots.Single(x => x.ParentId == TestOnlyInventoryPolicy.FoodId
                    && x.Access == InventoryAccess.Ground).LotId;
                WorldStep(s, -1, 0); WorldAdvance(s, 1);
                var handling = IC(s, CommandKind.HandleInventory, dropped,
                    new InventoryRequest(new RuleQuantity(1), handling: HandlingKind.Pickup), worker);
                WorldCommit(s, handling); var labor = s.Capture().Work.WorkerIntervals.Single(x => x.WorkerId == worker);
                Require(labor.Start == T(7) && labor.End == T(8) && s.Capture().RuleClock == T(8),
                    "Fixture did not record the companion's completed ordinary handling segment.");
                Require(s.Capture().WorldActivityIntervals.Single().Action == WorldActionCommitment.ActiveLabor
                    && s.Capture().WorldActivityIntervals.Single().ActionReference == labor.Id
                    && s.Capture().WorldActivityIntervals.Single().ActionReferenceRevision == 0,
                    "Positive handling labor did not commit ActiveLabor with worker-interval provenance.");
                string picked = s.Capture().InventoryLots.Single(x => x.ParentId == dropped && x.Access == InventoryAccess.Ready).LotId;
                WorldCommit(s, IC(s, CommandKind.HandleInventory, picked,
                    new InventoryRequest(new RuleQuantity(1), handling: HandlingKind.Stow), worker));
                var segments = s.Capture().Work.WorkerIntervals.Where(x => x.WorkerId == worker).OrderBy(x => x.Start).ToArray();
                Require(segments.Length == 2 && segments[0].End == segments[1].Start && segments[1].End == T(9),
                    "Sequential labor was merged, overlapped or lost its interval history.");
                Require(s.Capture().WorldActivityIntervals.Single().Action == WorldActionCommitment.ActiveLabor
                    && s.Capture().WorldActivityIntervals.Single().ActionReference == segments[1].Id,
                    "Consecutive work segments did not share ActiveLabor while retaining separate provenance.");
                RejectUnchanged(s, host, IC(s, CommandKind.BeginWorldStep, "run", actor: worker, y: -1),
                    "OffCalendarLaborOverlapsActivity");
                WorldStep(s, 0, -1, actor: worker); WorldAdvance(s, 1);
                Require(s.Capture().WorldActivityIntervals.Single().IntervalIndex == 1
                    && s.Capture().WorldActivityIntervals.Single().MovementSpent == new RuleQuantity(5)
                    && s.Capture().Actors.Single(x => x.Id == worker).Y == 2 && !s.Capture().WorldActivityIntervals.Single().DashPaid,
                    "Completed labor improperly blocked ordinary walking or spent Dash.");

                var paused = World(policy);
                WorldCommit(paused, IC(paused, CommandKind.StartWaterFill, TestOnlyFillingPolicy.SupplyId,
                    new InventoryRequest(new RuleQuantity(1), TestOnlyFillingPolicy.FlaskId), worker));
                RejectUnchanged(paused, host, IC(paused, CommandKind.BeginWorldStep, "run", actor: worker, x: -1), "WorkerBusy");
                string fillId = paused.Capture().WaterFills.Single().Id;
                WorldCommit(paused, IC(paused, CommandKind.PauseWaterFill, fillId, actor: worker));
                Require(!paused.Capture().Work.WorkerIntervals.Any(x => x.WorkerId == worker && x.Start <= paused.Capture().RuleClock && x.End > paused.Capture().RuleClock),
                    "Paused work retained an active worker claim.");
                WorldStep(paused, -1, 0, true, worker);
                Require(paused.Capture().WorldActivityIntervals.Single().DashPaid,
                    "A paused reservation without active labor prevented Dash.");

                var afterDash = World(policy);
                WorldStep(afterDash, -1, 0, true, worker); WorldAdvance(afterDash, 1, 2);
                RejectUnchanged(afterDash, host, IC(afterDash, CommandKind.StartWaterFill, TestOnlyFillingPolicy.SupplyId,
                    new InventoryRequest(new RuleQuantity(1), TestOnlyFillingPolicy.FlaskId), worker), "OffCalendarActionAlreadySpent");

                var walkAfterDash = World(policy);
                WorldStep(walkAfterDash, -1, 0, true, worker); WorldAdvance(walkAfterDash, 1, 2);
                WorldStep(walkAfterDash, 0, -1, actor: worker); WorldAdvance(walkAfterDash, 1);
                Require(walkAfterDash.Capture().Actors.Single(x => x.Id == worker).Y == 2
                    && walkAfterDash.Capture().WorldActivityIntervals.Single().DashPaid
                    && walkAfterDash.Capture().WorldActivityIntervals.Single().MovementSpent == new RuleQuantity(10),
                    "Dash spending prohibited walking or duplicated movement accounting.");

                var credited = World(policy);
                WorldCommit(credited, IC(credited, CommandKind.StartWaterFill, TestOnlyFillingPolicy.SupplyId,
                    new InventoryRequest(new RuleQuantity(1), TestOnlyFillingPolicy.FlaskId), worker));
                WorldAdvance(credited, 1);
                var creditedSnapshot = credited.Capture();
                var creditedActivity = creditedSnapshot.WorldActivityIntervals.Single();
                var creditedInterval = creditedSnapshot.Work.WorkerIntervals.Single(x => x.WorkerId == worker);
                Require(creditedActivity.Action == WorldActionCommitment.ActiveLabor
                    && creditedActivity.ActionReference == creditedInterval.Id,
                    "Scheduler-credited labor did not commit the off-calendar Action.");
                string fillIdForPause = creditedSnapshot.WaterFills.Single().Id;
                WorldCommit(credited, IC(credited, CommandKind.PauseWaterFill, fillIdForPause, actor: worker));
                RejectUnchanged(credited, host, IC(credited, CommandKind.BeginWorldStep, "run", actor: worker, x: -1),
                    "OffCalendarLaborOverlapsActivity");

                var crossing = World(policy);
                WorldCommit(crossing, IC(crossing, CommandKind.StartWaterFill, TestOnlyFillingPolicy.SupplyId,
                    new InventoryRequest(new RuleQuantity(1), TestOnlyFillingPolicy.FlaskId), worker));
                WorldAdvance(crossing, 7);
                Require(crossing.Capture().RuleClock == T(7)
                    && crossing.Capture().WorldActivityIntervals.Single().IntervalIndex == 1
                    && crossing.Capture().WorldActivityIntervals.Single().Action == WorldActionCommitment.ActiveLabor
                    && crossing.Capture().WaterFills.Single().Progress == T(7),
                    "Active labor crossing the fixed boundary did not spend the new interval independently.");

                var unlinkedWorking = World(policy);
                WorldCommit(unlinkedWorking, IC(unlinkedWorking, CommandKind.StartWaterFill, TestOnlyFillingPolicy.SupplyId,
                    new InventoryRequest(new RuleQuantity(1), TestOnlyFillingPolicy.FlaskId), worker));
                var unlinkedSnapshot = unlinkedWorking.Capture();
                unlinkedSnapshot.Work = new WorkLedger(unlinkedSnapshot.Work.Lots,
                    unlinkedSnapshot.Work.WorkerIntervals.Where(x => x.WorkerId != worker), unlinkedSnapshot.Work.Reservations);
                Require(WorldActivityValidation.HasActiveLabor(unlinkedSnapshot, worker, T(0), T(6)),
                    "A Working procedure without a matching worker interval did not remain a labor claim.");
                var dashConflict = World(policy); WorldStep(dashConflict, -1, 0, true, worker);
                var contradictory = dashConflict.Capture();
                contradictory.Work = unlinkedSnapshot.Work;
                contradictory.WaterFills = unlinkedSnapshot.WaterFills;
                Throws<ArgumentException>(() => WorldActivityValidation.Validate(contradictory));

                var forged = World(policy).Capture();
                forged.WorldActivityIntervals[0] = new WorldActivityIntervalRecord(forged.WorldSchedule.Id, worker, 1);
                Throws<ArgumentException>(() => Validation.Snapshot(forged));
                var invalid = s.Capture();
                invalid.WorldActivityIntervals[0] = new WorldActivityIntervalRecord(invalid.WorldSchedule.Id, worker, 1,
                    action: WorldActionCommitment.Dash, actionReference: "forged.dash", actionReferenceRevision: 1);
                Throws<ArgumentException>(() => Validation.Snapshot(invalid));
            });

            cases.Add("assigned_camp_greens_uses_shared_travel_work_and_crop_authorities", () => {
                const string cropId = "TEST_ONLY.assigned-crop";
                var policy = new TestOnlySharedWorldPolicy(new SharedCombatFixture()).EnableCampGreensAssignments();
                var simulation = World(policy);
                Require(simulation.Capture().SchemaVersion == Snapshot.ExpeditionAssignmentSchema
                    && simulation.Capture().CropPlots.Any(x => x.Id == TestOnlyCropPolicy.PlotId),
                    "Assigned farming did not reuse the existing plot and assignment schema.");

                WorldStep(simulation, -1, 0, actor: worker);
                WorldAdvance(simulation, 1);
                var plantRequest = new ExpeditionAssignmentRequest(ExpeditionWorkProcedure.CropPlanting, cropId);
                WorldCommit(simulation, ExpeditionCommand(simulation, CommandKind.AssignExpeditionWork,
                    request: plantRequest, actor: worker));
                var assignment = simulation.Capture().ExpeditionAssignments.Single();
                Require(assignment.Status == ExpeditionAssignmentStatus.Travelling && assignment.TargetId == cropId
                    && assignment.SiteX == 3 && assignment.SiteY == 3,
                    "Planting assignment did not derive its destination from the authored plot.");

                WorldStep(simulation, 1, 0);
                WorldAdvance(simulation, 1);
                Require(simulation.Capture().ExpeditionAssignments.Single().Status == ExpeditionAssignmentStatus.Travelling,
                    "Lead exploration prematurely marked an unmoved companion ready.");
                WorldStep(simulation, 1, 0, actor: worker);
                WorldAdvance(simulation, 1);
                assignment = simulation.Capture().ExpeditionAssignments.Single();
                var afterTravel = simulation.Capture();
                Require(assignment.Status == ExpeditionAssignmentStatus.Ready
                    && afterTravel.Actors.Single(x => x.Id == worker).X == 3
                    && afterTravel.Actors.Single(x => x.Id == TestOnlyPolicy.ActorId).X == 1,
                    "Companion travel and lead exploration did not advance on the same clock: assignment="
                        + assignment.Status + ", worker=" + afterTravel.Actors.Single(x => x.Id == worker).X + ","
                        + afterTravel.Actors.Single(x => x.Id == worker).Y + ", lead="
                        + afterTravel.Actors.Single(x => x.Id == TestOnlyPolicy.ActorId).X + ","
                        + afterTravel.Actors.Single(x => x.Id == TestOnlyPolicy.ActorId).Y + ", clock=" + afterTravel.RuleClock
                        + ", traversals=" + afterTravel.WorldTraversals.Length);

                string cancelledPlantAssignment = assignment.Id;
                WorldCommit(simulation, ExpeditionCommand(simulation, CommandKind.CancelExpeditionWork,
                    cancelledPlantAssignment, actor: worker));
                WorldCommit(simulation, ExpeditionCommand(simulation, CommandKind.AssignExpeditionWork,
                    request: plantRequest, actor: worker));
                assignment = simulation.Capture().ExpeditionAssignments.Single(x => x.Open && x.WorkerId == worker);
                Require(assignment.Id != cancelledPlantAssignment && assignment.Status == ExpeditionAssignmentStatus.Ready,
                    "A cancelled pre-start crop assignment prevented reusing its uncreated batch identity.");

                var startPlant = ExpeditionCommand(simulation, CommandKind.StartExpeditionWork, assignment.Id, actor: worker);
                WorldCommit(simulation, startPlant);
                var started = simulation.Capture().ExpeditionAssignments.Single(x => x.Id == assignment.Id);
                var plantTask = simulation.Capture().Crops.Single(x => x.Id == cropId).Tasks.Single();
                Require(started.Status == ExpeditionAssignmentStatus.Started && started.WorkId == plantTask.Id
                    && plantTask.Kind == CropWorkKind.Plant && plantTask.WorkerId == worker
                    && simulation.Capture().Work.Lots.Single(x => x.Id == TestOnlyCropPolicy.SeedLotId).Amount == new RuleQuantity(7)
                    && simulation.Capture().Work.Lots.Single(x => x.Id == TestOnlyCropPolicy.WaterLotId).Amount == new RuleQuantity(504),
                    "Assigned planting did not use Camp Greens costs and its authoritative crop task.");
                WorldAdvance(simulation, 1800);
                byte[] partialPlant = Bytes(simulation);
                var firstReplay = new Simulation(policy, new SnapshotCodec().Decode(partialPlant), ExecutionProfile.Laboratory);
                var secondReplay = new Simulation(policy, new SnapshotCodec().Decode(partialPlant), ExecutionProfile.Laboratory);
                Require(partialPlant.SequenceEqual(Bytes(firstReplay)), "Mid-plant save/restore changed crop or assignment state.");
                byte[] beforeDuplicate = Bytes(simulation);
                Require(simulation.Execute(TestOnlySharedWorldPolicy.Host(), startPlant).Outcome == Outcome.Duplicate
                    && beforeDuplicate.SequenceEqual(Bytes(simulation)), "Duplicate assignment start changed inputs or crop work.");
                WorldAdvance(firstReplay, 1800);
                WorldAdvance(secondReplay, 1800);
                Require(Bytes(firstReplay).SequenceEqual(Bytes(secondReplay))
                    && firstReplay.Capture().Crops.Single(x => x.Id == cropId).Stage == CropStage.Growing,
                    "Restored planting continuations did not settle deterministically.");
                simulation = firstReplay;

                string AssignAndStart(ExpeditionWorkProcedure procedure)
                {
                    WorldCommit(simulation, ExpeditionCommand(simulation, CommandKind.AssignExpeditionWork,
                        request: new ExpeditionAssignmentRequest(procedure, cropId), actor: worker));
                    var next = simulation.Capture().ExpeditionAssignments.Single(x => x.Open && x.WorkerId == worker);
                    WorldCommit(simulation, ExpeditionCommand(simulation, CommandKind.StartExpeditionWork, next.Id, actor: worker));
                    return next.Id;
                }

                for (int day = 0; day < 6; day++)
                {
                    WorldAdvance(simulation, 85500);
                    Require(simulation.Capture().Crops.Single(x => x.Id == cropId).CareUntil
                        == simulation.Capture().RuleClock.AddSeconds(900), "Tending did not begin 15 minutes before the care deadline.");
                    string tendingId = AssignAndStart(ExpeditionWorkProcedure.CropTending);
                    WorldAdvance(simulation, 900);
                    var crop = simulation.Capture().Crops.Single(x => x.Id == cropId);
                    Require(simulation.Capture().ExpeditionAssignments.Single(x => x.Id == tendingId).WorkId == crop.Tasks.Last().Id
                        && crop.Tasks.Last().Kind == CropWorkKind.Tend,
                        "Tending assignment did not link the authoritative crop work record.");
                }
                WorldAdvance(simulation, 86400);
                Require(simulation.Capture().Crops.Single(x => x.Id == cropId).Stage == CropStage.Mature,
                    "Assigned tending did not preserve the adopted growth schedule.");

                string harvestId = AssignAndStart(ExpeditionWorkProcedure.CropHarvesting);
                WorldAdvance(simulation, 1800);
                byte[] partialHarvest = Bytes(simulation);
                var harvestReplayA = new Simulation(policy, new SnapshotCodec().Decode(partialHarvest), ExecutionProfile.Laboratory);
                var harvestReplayB = new Simulation(policy, new SnapshotCodec().Decode(partialHarvest), ExecutionProfile.Laboratory);
                WorldAdvance(harvestReplayA, 1800);
                WorldAdvance(harvestReplayB, 1800);
                var finalA = harvestReplayA.Capture();
                var finalB = harvestReplayB.Capture();
                var finalCrop = finalA.Crops.Single(x => x.Id == cropId);
                var foodLot = finalA.CropFood.Single(x => x.BatchId == cropId);
                RuleQuantity cropYield = finalA.Work.Lots.Single(x => x.Id == foodLot.LotId).Amount;
                bool replayEqual = Bytes(harvestReplayA).SequenceEqual(Bytes(harvestReplayB));
                RuleQuantity edible = OrdinaryInventory.EdibleFood(finalA);
                string linkedWork = finalA.ExpeditionAssignments.Single(x => x.Id == harvestId).WorkId;
                Require(replayEqual && finalCrop.Stage == CropStage.Harvested && cropYield == new RuleQuantity(8)
                    && edible == new RuleQuantity(10) && linkedWork == finalCrop.Tasks.Last().Id,
                    "Assigned harvest did not save, replay, and settle through existing finite food output: replay="
                        + replayEqual + ", stage=" + finalCrop.Stage + ", crop yield=" + cropYield + ", edible=" + edible + ", assignmentWork="
                        + linkedWork + ", cropWork=" + finalCrop.Tasks.Last().Id + ", clock=" + finalA.RuleClock);
            });

            cases.Add("registered_workers_and_physical_sites_compose_crop_mining_exploration_and_replay", () => {
                const string cropId = "TEST_ONLY.binding-profile-crop";
                const string planter = AdditionalTacticalActor.Id;
                const string miner = TestOnlyPolicy.CompanionId;
                var fixture = new SharedMiningFixture(siteX: 4, siteY: 3, trainedWorkerIds: new[] { miner });
                var profile = new SharedExpeditionAssignmentProfile("TEST_ONLY.assignment-roster-sites-v1", new[] {
                    new ExpeditionAssignmentBinding(planter, ExpeditionWorkProcedure.CropPlanting, TestOnlyCropPolicy.PlotId, 3, 3),
                    new ExpeditionAssignmentBinding(planter, ExpeditionWorkProcedure.CropTending, TestOnlyCropPolicy.PlotId, 3, 3),
                    new ExpeditionAssignmentBinding(planter, ExpeditionWorkProcedure.CropHarvesting, TestOnlyCropPolicy.PlotId, 3, 3),
                    new ExpeditionAssignmentBinding(miner, ExpeditionWorkProcedure.MiningExtraction, SharedMiningFixture.SiteId, 4, 3),
                    // Registration permits asking the existing handler; it does not supply the
                    // planter's missing mining-tools training or physical mining access.
                    new ExpeditionAssignmentBinding(planter, ExpeditionWorkProcedure.MiningExtraction, SharedMiningFixture.SiteId, 4, 3)
                });
                var unseeded = TestOnlySharedWorldPolicy.WithMining(fixture)
                    .EnableCampGreensAssignments().EnableExpeditionAssignmentBindings(profile);
                var initial = unseeded.Initial();
                var minerCharacter = initial.Characters.Single(x => x.ActorId == miner);
                int minerModifier = PlaytestCharacters.AbilityModifier(minerCharacter.Abilities[4])
                    + PlaytestCharacters.ProficiencyBonus(minerCharacter.Levels.Count);
                Require(initial.SkillTraining.Where(x => x.SkillId == "mining-tools").Select(x => x.ActorId)
                    .SequenceEqual(new[] { miner })
                    && !initial.SkillTraining.Any(x => x.ActorId == planter && x.SkillId == "mining-tools")
                    && initial.MiningDeposits.Single().SiteX == 4
                    && initial.CropPlots.Single().Id == TestOnlyCropPolicy.PlotId,
                    "The authored worker/site profile changed qualification, ownership, or the existing physical targets.");

                uint seed = MiningSeedFor(TaskDegree.Success, minerModifier);
                var policy = TestOnlySharedWorldPolicy.WithMining(fixture, seed)
                    .EnableCampGreensAssignments().EnableExpeditionAssignmentBindings(profile);
                var sim = World(policy);
                var host = policy.HostAuthority();
                var mineSelection = MiningSelection(SharedMiningFixture.CategoryA);
                var mineRequest = new ExpeditionAssignmentRequest(ExpeditionWorkProcedure.MiningExtraction,
                    SharedMiningFixture.DepositId, miningSelection: mineSelection);

                RejectUnchanged(sim, host, ExpeditionCommand(sim, CommandKind.AssignExpeditionWork,
                    request: mineRequest, actor: TestOnlyPolicy.ActorId), "ExpeditionAssignmentWorkerNotRegistered");

                // The registered planter reaches the mine first. Registration permits the
                // existing procedure to be requested; it grants neither skill nor free hands.
                WorldCommit(sim, ExpeditionCommand(sim, CommandKind.AssignExpeditionWork,
                    request: mineRequest, actor: planter));
                var unqualifiedAssignment = sim.Capture().ExpeditionAssignments.Single(x => x.WorkerId == planter && x.Open);
                foreach (var step in new[] { new[] { 0, 1 }, new[] { 0, 1 }, new[] { 0, 1 } }) {
                    WorldStep(sim, step[0], step[1], actor: planter); WorldAdvance(sim, 1);
                }
                unqualifiedAssignment = sim.Capture().ExpeditionAssignments.Single(x => x.Id == unqualifiedAssignment.Id);
                Require(unqualifiedAssignment.Status == ExpeditionAssignmentStatus.Ready,
                    "The registered unqualified worker did not reach the mine for handler revalidation.");
                RejectUnchanged(sim, host, ExpeditionCommand(sim, CommandKind.StartExpeditionWork,
                    unqualifiedAssignment.Id, actor: planter), "TwoHandsRequired");
                Require(sim.Capture().MiningAttempts.Length == 0
                    && sim.Capture().Work.Lots.Single(x => x.Id == SharedMiningFixture.UnitA).Amount == new RuleQuantity(1),
                    "An unqualified registered worker created an attempt or consumed mineral stock.");
                WorldCommit(sim, ExpeditionCommand(sim, CommandKind.CancelExpeditionWork,
                    unqualifiedAssignment.Id, actor: planter));
                WorldStep(sim, 0, -1, actor: planter); WorldAdvance(sim, 1);
                WorldStep(sim, 0, -1, actor: planter); WorldAdvance(sim, 1);

                WorldCommit(sim, ExpeditionCommand(sim, CommandKind.AssignExpeditionWork,
                    request: mineRequest, actor: miner));
                var mineAssignment = sim.Capture().ExpeditionAssignments.Single(x => x.WorkerId == miner && x.Open);
                Require(mineAssignment.SiteX == 4 && mineAssignment.SiteY == 3
                    && mineAssignment.Status == ExpeditionAssignmentStatus.Travelling,
                    "Mining assignment did not resolve the separately registered deposit site.");
                WorldStep(sim, 1, 0, actor: miner); WorldAdvance(sim, 1);
                mineAssignment = sim.Capture().ExpeditionAssignments.Single(x => x.Id == mineAssignment.Id);
                Require(mineAssignment.Status == ExpeditionAssignmentStatus.Ready,
                    "The registered miner did not become ready at the physical deposit.");
                var startMine = ExpeditionCommand(sim, CommandKind.StartExpeditionWork, mineAssignment.Id, actor: miner);
                WorldCommit(sim, startMine);

                var seedBefore = sim.Capture().Work.Lots.Single(x => x.Id == TestOnlyCropPolicy.SeedLotId).Amount;
                var waterBefore = sim.Capture().Work.Lots.Single(x => x.Id == TestOnlyCropPolicy.WaterLotId).Amount;
                WorldCommit(sim, ExpeditionCommand(sim, CommandKind.AssignExpeditionWork,
                    request: new ExpeditionAssignmentRequest(ExpeditionWorkProcedure.CropPlanting, cropId), actor: planter));
                var plantAssignment = sim.Capture().ExpeditionAssignments.Single(x => x.WorkerId == planter && x.Open);
                Require(plantAssignment.SiteX == 3 && plantAssignment.SiteY == 3
                    && plantAssignment.Status == ExpeditionAssignmentStatus.Travelling,
                    "Crop assignment did not resolve its registered prepared-plot identity and location.");
                foreach (var step in new[] { new[] { 0, 1 }, new[] { -1, 0 }, new[] { 0, 1 } }) {
                    WorldStep(sim, step[0], step[1], actor: planter); WorldAdvance(sim, 1);
                }
                plantAssignment = sim.Capture().ExpeditionAssignments.Single(x => x.Id == plantAssignment.Id);
                Require(plantAssignment.Status == ExpeditionAssignmentStatus.Ready,
                    "The registered planter did not arrive at the prepared plot.");
                var startPlant = ExpeditionCommand(sim, CommandKind.StartExpeditionWork, plantAssignment.Id, actor: planter);
                WorldCommit(sim, startPlant);
                var plantTask = sim.Capture().Crops.Single(x => x.Id == cropId).Tasks.Single();
                // Keep lead exploration live while the registered workers occupy different sites.
                WorldStep(sim, 0, 1, actor: TestOnlyPolicy.ActorId); WorldAdvance(sim, 1);
                WorldAdvance(sim, 600);
                WorldCommit(sim, IC(sim, CommandKind.PauseCrop, cropId, actor: planter));
                var paused = sim.Capture();
                Require(paused.ExpeditionAssignments.Single(x => x.Id == plantAssignment.Id).WorkId == plantTask.Id
                    && paused.Crops.Single(x => x.Id == cropId).Tasks.Single().Progress == new RuleTime(601)
                    && paused.Work.Lots.Single(x => x.Id == TestOnlyCropPolicy.SeedLotId).Amount == new RuleQuantity(7)
                    && paused.Work.Lots.Single(x => x.Id == TestOnlyCropPolicy.WaterLotId).Amount == new RuleQuantity(504),
                    "Planting did not retain its authoritative work link and exactly-once input debit at pause.");

                var started = sim.Capture();
                var attempt = started.MiningAttempts.Single();
                Require(mineAssignment.WorkerId == miner && attempt.WorkerId == miner && attempt.Status == MiningAttemptStatus.Working
                    && started.ExpeditionAssignments.Single(x => x.Id == mineAssignment.Id).WorkId == attempt.Id
                    && started.ExpeditionAssignments.Single(x => x.Id == plantAssignment.Id).WorkId == plantTask.Id,
                    "The two existing work handlers did not retain distinct authoritative worker/job links.");

                byte[] inProgress = Bytes(sim);
                var forgedWork = new SnapshotCodec().Decode(inProgress);
                forgedWork.ExpeditionAssignments = forgedWork.ExpeditionAssignments.Select(x => x.Id == mineAssignment.Id
                    ? new ExpeditionWorkAssignmentRecord(x.Id, x.WorkerId, x.Procedure, x.TargetId, x.DestinationId,
                        x.SiteX, x.SiteY, x.AssignedAt, x.UpdatedAt, x.Status, "forged.mining-work", x.MiningSelection) : x).ToArray();
                Throws<ArgumentException>(() => new Simulation(policy, forgedWork, ExecutionProfile.Laboratory));
                var forgedWorker = new SnapshotCodec().Decode(inProgress);
                forgedWorker.ExpeditionAssignments = forgedWorker.ExpeditionAssignments.Select(x => x.Id == mineAssignment.Id
                    ? new ExpeditionWorkAssignmentRecord(x.Id, planter, x.Procedure, x.TargetId, x.DestinationId,
                        x.SiteX, x.SiteY, x.AssignedAt, x.UpdatedAt, x.Status, x.WorkId, x.MiningSelection) : x).ToArray();
                Throws<ArgumentException>(() => new Simulation(policy, forgedWorker, ExecutionProfile.Laboratory));
                var forgedProcedure = new SnapshotCodec().Decode(inProgress);
                forgedProcedure.ExpeditionAssignments = forgedProcedure.ExpeditionAssignments.Select(x => x.Id == mineAssignment.Id
                    ? new ExpeditionWorkAssignmentRecord(x.Id, x.WorkerId, ExpeditionWorkProcedure.CacheExcavation,
                        x.TargetId, "", x.SiteX, x.SiteY, x.AssignedAt, x.UpdatedAt, x.Status, x.WorkId) : x).ToArray();
                Throws<ArgumentException>(() => new Simulation(policy, forgedProcedure, ExecutionProfile.Laboratory));

                var replayA = new Simulation(policy, new SnapshotCodec().Decode(inProgress), ExecutionProfile.Laboratory);
                var replayB = new Simulation(policy, new SnapshotCodec().Decode(inProgress), ExecutionProfile.Laboratory);
                WorldCommit(replayA, IC(replayA, CommandKind.PlantCrop, cropId, actor: planter));
                WorldCommit(replayB, IC(replayB, CommandKind.PlantCrop, cropId, actor: planter));
                WorldAdvance(replayA, 1196); WorldAdvance(replayB, 1196);
                WorldAdvance(replayA, 1803); WorldAdvance(replayB, 1803);
                var resultA = replayA.Capture(); var resultB = replayB.Capture();
                var extracted = resultA.MiningUnits.Single(x => x.Id == SharedMiningFixture.UnitA);
                var received = resultA.Work.Lots.Single(x => x.Id == extracted.ReceivedLotId);
                Require(Bytes(replayA).SequenceEqual(Bytes(replayB)) && resultA.RandomState == resultB.RandomState
                    && resultA.MiningAttempts.Single().Status == MiningAttemptStatus.Success
                    && extracted.Status == MiningUnitStatus.Extracted && extracted.ReceivedContainerId == SharedMiningFixture.ReceiverId
                    && received.LocationId == SharedMiningFixture.ReceiverId && received.CustodianId == SharedMiningFixture.OwnerId
                    && resultA.ExpeditionAssignments.Single(x => x.Id == mineAssignment.Id).WorkId == resultA.MiningAttempts.Single().Id
                    && resultA.ExpeditionAssignments.Single(x => x.Id == plantAssignment.Id).WorkId == plantTask.Id
                    && resultA.Crops.Single(x => x.Id == cropId).Stage == CropStage.Growing
                    && resultA.Crops.Single(x => x.Id == cropId).Tasks.Single().Progress == new RuleTime(3600)
                    && resultA.Work.Lots.Single(x => x.Id == TestOnlyCropPolicy.SeedLotId).Amount == new RuleQuantity(7)
                    && resultA.Work.Lots.Single(x => x.Id == TestOnlyCropPolicy.WaterLotId).Amount == new RuleQuantity(504)
                    && resultA.Actors.Single(x => x.Id == TestOnlyPolicy.ActorId).X == 0
                    && resultA.Actors.Single(x => x.Id == TestOnlyPolicy.ActorId).Y == 1,
                    "Restored exploration, crop labor, extraction, custody, RNG, or receipts diverged.");
                Require(replayA.Execute(host, startMine).Outcome == Outcome.Duplicate
                    && Bytes(replayA).SequenceEqual(Bytes(replayB)),
                    "Duplicate mining assignment replay changed the settled shared world.");

            });

            cases.Add("registered_tool_repair_composes_crop_exploration_save_and_replay", () => {
                const string cropId = "TEST_ONLY.repair-binding-crop";
                const string repairWorker = TestOnlyPolicy.CompanionId;
                const string cropWorker = AdditionalTacticalActor.Id;
                SharedExpeditionAssignmentProfile Profile() => new SharedExpeditionAssignmentProfile(
                    "TEST_ONLY.assignment-repair-crop-v1", new[] {
                        new ExpeditionAssignmentBinding(repairWorker, ExpeditionWorkProcedure.ToolRepair,
                            TestOnlyCropPolicy.PlotId, 1, 3),
                        new ExpeditionAssignmentBinding(cropWorker, ExpeditionWorkProcedure.CropPlanting,
                            TestOnlyCropPolicy.PlotId, 3, 3)
                    });
                TestOnlySharedWorldPolicy BoundPolicy(uint seed, bool trained) => RepairPolicy(seed,
                    new SharedRepairFixture(trained: trained, siteX: 1, siteY: 3),
                    new SharedCraftingFixture(toolHp: 0))
                    .EnableCampGreensAssignments().EnableExpeditionAssignmentBindings(Profile());
                void TravelTo(Simulation simulation, string actorId, int x, int y)
                {
                    for (int step = 0; step < 10; step++)
                    {
                        var actor = simulation.Capture().Actors.Single(a => a.Id == actorId);
                        if (actor.X == x && actor.Y == y) return;
                        int dx = actor.X == x ? 0 : Math.Sign(x - actor.X);
                        int dy = dx == 0 ? Math.Sign(y - actor.Y) : 0;
                        WorldStep(simulation, dx, dy, actor: actorId);
                        WorldAdvance(simulation, 1);
                    }
                    var arrived = simulation.Capture().Actors.Single(a => a.Id == actorId);
                    Require(arrived.X == x && arrived.Y == y, actorId + " did not reach its registered work site.");
                }

                uint seed = 0;
                for (uint candidate = 1; candidate < 10000 && seed == 0; candidate++)
                {
                    var probePolicy = BoundPolicy(candidate, true);
                    var initial = probePolicy.Initial();
                    var actorFacts = CharacterStateFacts.ForActor(initial, repairWorker);
                    int modifier = actorFacts.Rules.AbilityModifier(CharacterAbility.Dexterity) + actorFacts.Rules.ProficiencyBonus;
                    if (ObjectStructureRules.RepairSucceeds(PlaytestDice.RollD20(initial.RandomState).Natural, modifier)) seed = candidate;
                }
                Require(seed != 0, "Could not select a deterministic repair success seed.");

                var host = TestOnlySharedWorldPolicy.Host();
                var repairRequest = new ExpeditionAssignmentRequest(ExpeditionWorkProcedure.ToolRepair, SharedCraftingFixture.ToolId);
                var untrained = World(BoundPolicy(seed, false));
                WorldCommit(untrained, ExpeditionCommand(untrained, CommandKind.AssignExpeditionWork,
                    request: repairRequest, actor: repairWorker));
                var untrainedAssignment = untrained.Capture().ExpeditionAssignments.Single();
                Require(untrainedAssignment.SiteX == 1 && untrainedAssignment.SiteY == 3,
                    "Repair assignment did not retain the registered physical site.");
                TravelTo(untrained, repairWorker, 1, 3);
                var untrainedStart = ExpeditionCommand(untrained, CommandKind.StartExpeditionWork,
                    untrainedAssignment.Id, actor: repairWorker);
                RejectUnchanged(untrained, host, untrainedStart, "RepairTrainingMissing");
                Require(untrained.Capture().RepairWork.Length == 0
                    && RepairStock(untrained) == new RuleQuantity(2)
                    && untrained.Capture().Work.Reservations.Count == 0,
                    "Registration granted repair qualification or consumed materials.");

                var policy = BoundPolicy(seed, true);
                var simulation = World(policy);
                WorldCommit(simulation, ExpeditionCommand(simulation, CommandKind.AssignExpeditionWork,
                    request: repairRequest, actor: repairWorker));
                WorldCommit(simulation, ExpeditionCommand(simulation, CommandKind.AssignExpeditionWork,
                    request: new ExpeditionAssignmentRequest(ExpeditionWorkProcedure.CropPlanting, cropId), actor: cropWorker));
                var repairAssignment = simulation.Capture().ExpeditionAssignments.Single(x => x.WorkerId == repairWorker);
                var cropAssignment = simulation.Capture().ExpeditionAssignments.Single(x => x.WorkerId == cropWorker);
                Require(repairAssignment.Status == ExpeditionAssignmentStatus.Travelling && repairAssignment.SiteX == 1
                    && repairAssignment.SiteY == 3 && cropAssignment.Status == ExpeditionAssignmentStatus.Travelling
                    && cropAssignment.SiteX == 3 && cropAssignment.SiteY == 3,
                    "Registered repair/crop assignments did not derive their physical sites.");

                TravelTo(simulation, repairWorker, 1, 3);
                TravelTo(simulation, cropWorker, 3, 3);
                repairAssignment = simulation.Capture().ExpeditionAssignments.Single(x => x.Id == repairAssignment.Id);
                cropAssignment = simulation.Capture().ExpeditionAssignments.Single(x => x.Id == cropAssignment.Id);
                Require(repairAssignment.Status == ExpeditionAssignmentStatus.Ready
                    && cropAssignment.Status == ExpeditionAssignmentStatus.Ready,
                    "A registered worker was not made ready on arrival at the actual site.");

                WorldCommit(simulation, ExpeditionCommand(simulation, CommandKind.StartExpeditionWork,
                    cropAssignment.Id, actor: cropWorker));
                var cropWork = simulation.Capture().Crops.Single(x => x.Id == cropId).Tasks.Single();
                var startRepair = ExpeditionCommand(simulation, CommandKind.StartExpeditionWork,
                    repairAssignment.Id, actor: repairWorker);
                WorldCommit(simulation, startRepair);
                var repairWork = simulation.Capture().RepairWork.Single();
                Require(simulation.Capture().ExpeditionAssignments.Single(x => x.Id == repairAssignment.Id).WorkId == repairWork.Id
                    && repairWork.WorkerId == repairWorker && repairWork.TargetId == SharedCraftingFixture.ToolId,
                    "Registered repair did not link to the existing repair job and worker.");

                // The lead continues direct exploration while crop planting and repair share the clock.
                WorldStep(simulation, 0, 1, actor: TestOnlyPolicy.ActorId);
                WorldAdvance(simulation, 1);
                WorldAdvance(simulation, 299);
                WorldCommit(simulation, RepairCommand(simulation, CommandKind.PauseToolRepair, repairWork.Id, repairWorker));
                var paused = simulation.Capture();
                repairWork = paused.RepairWork.Single();
                cropWork = paused.Crops.Single(x => x.Id == cropId).Tasks.Single();
                var materialClaim = paused.Work.Reservations.Single(x => x.JobId == repairWork.Id);
                Require(repairWork.Status == RepairWorkStatus.Paused && repairWork.Work.Labor == T(300)
                    && materialClaim.Status == ReservationStatus.Consumed && materialClaim.ConsumedAmount == new RuleQuantity(1)
                    && RepairStock(simulation) == new RuleQuantity(1)
                    && cropWork.Status == CropWorkStatus.Working && cropWork.Progress == T(300)
                    && paused.Actors.Single(x => x.Id == TestOnlyPolicy.ActorId).X == 0,
                    "Pause did not retain partial repair, one-time materials, crop labor and lead exploration.");

                byte[] pausedBytes = Bytes(simulation);
                var codec = new SnapshotCodec();
                var replayA = new Simulation(policy, codec.Decode(pausedBytes), ExecutionProfile.Laboratory);
                var replayB = new Simulation(policy, codec.Decode(pausedBytes), ExecutionProfile.Laboratory);
                Require(pausedBytes.SequenceEqual(Bytes(replayA)) && pausedBytes.SequenceEqual(Bytes(replayB)),
                    "Partial repair/crop work changed across save and restore.");

                var wrongWorkerResume = RepairCommand(replayA, CommandKind.ResumeToolRepair, repairWork.Id, cropWorker);
                RejectUnchanged(replayA, host, wrongWorkerResume, "UnknownRepairWork");
                var resumeRepair = RepairCommand(replayA, CommandKind.ResumeToolRepair, repairWork.Id, repairWorker);
                WorldCommit(replayA, resumeRepair);
                WorldCommit(replayB, resumeRepair);
                WorldAdvance(replayA, 3300);
                WorldAdvance(replayB, 3300);
                byte[] finishedBytes = Bytes(replayA);
                var finalA = replayA.Capture();
                var finalB = replayB.Capture();
                var settledClaim = finalA.Work.Reservations.Single(x => x.JobId == repairWork.Id);
                var restoredFinal = new Simulation(policy, codec.Decode(finishedBytes), ExecutionProfile.Laboratory);
                Require(finishedBytes.SequenceEqual(Bytes(replayB)) && finishedBytes.SequenceEqual(Bytes(restoredFinal))
                    && finalA.RandomState == finalB.RandomState
                    && finalA.RepairWork.Single().Status == RepairWorkStatus.Success
                    && finalA.RepairWork.Single().Work.Labor == T(3600)
                    && finalA.RepairWork.Single().WorkerId == repairWorker
                    && finalA.Structures.Single(x => x.Id == SharedCraftingFixture.ToolId).Hp
                        == finalA.Structures.Single(x => x.Id == SharedCraftingFixture.ToolId).MaximumHp
                    && RepairStock(replayA) == new RuleQuantity(1)
                    && settledClaim.Status == ReservationStatus.Consumed && settledClaim.ConsumedAmount == new RuleQuantity(1)
                    && finalA.ExpeditionAssignments.Single(x => x.Id == repairAssignment.Id).WorkId == repairWork.Id
                    && finalA.ExpeditionAssignments.Single(x => x.Id == cropAssignment.Id).WorkId == cropWork.Id
                    && finalA.Crops.Single(x => x.Id == cropId).Tasks.Single().Status == CropWorkStatus.Complete,
                    "Repair completion, crop work, material settlement, assignment links or deterministic replay diverged.");
                Require(replayA.Execute(host, resumeRepair).Outcome == Outcome.Duplicate
                    && finishedBytes.SequenceEqual(Bytes(replayA))
                    && replayA.Execute(host, startRepair).Outcome == Outcome.Duplicate
                    && finishedBytes.SequenceEqual(Bytes(replayA)),
                    "Duplicate repair work/start receipts changed the settled shared simulation.");
            });
        }
    }
}
#endif
