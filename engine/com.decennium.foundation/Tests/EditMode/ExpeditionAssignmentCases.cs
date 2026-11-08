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
        }
    }
}
#endif
