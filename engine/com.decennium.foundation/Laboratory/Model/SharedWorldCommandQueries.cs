#if DECENNIUM_TEST_ONLY && (UNITY_EDITOR || DEVELOPMENT_BUILD || HEADLESS_TESTS)
using System;
using System.Collections.Generic;
using System.Globalization;
using System.Linq;

namespace Decennium.Foundation.Laboratory
{
    public sealed partial class TestOnlySharedWorldPolicy
    {
        private sealed class WorldStepFacts
        {
            public bool Scheduled;
            public bool OffCalendar;
            public bool StartsEncounter;
            public bool DashAlreadyPaid;
            public int ToX;
            public int ToY;
            public long Cost;
        }

        private string AssessWorldStep(Snapshot s, Command c, out WorldStepFacts facts)
        {
            facts = null;
            if (c.Kind != CommandKind.BeginWorldStep || c.Inventory != null || (c.Target != "walk" && c.Target != "run")
                || !WorldSpatialQueries.Neighbor(0, 0, c.X, c.Y, false)) return "InvalidWorldStep";
            bool scheduled = s.WorldSchedule.Order.Contains(c.Actor);
            bool offCalendar = !scheduled && (c.Actor == TestOnlyPolicy.CompanionId || IsOffCalendarActivity(s, c.Actor));
            if (!scheduled && (!offCalendar || s.InventoryCombat)) return "NoActivityCalendar";
            if (!scheduled && c.Target == "run" && !IsOffCalendarActivity(s, c.Actor)) return "OffCalendarDashBudgetUnsupported";
            if (s.WorldTraversals.Any(x => x.ActorId == c.Actor)) return "TraversalAlreadyPending";
            if (s.WorldTraversals.Any(x => s.WorldSchedule.Order.Contains(x.ActorId)))
                return scheduled ? "ConcurrentHostileTraversalUnsupported" : "ConcurrentWorldTraversalUnsupported";
            if (s.WorldTraversals.Length != 0) return "ConcurrentWorldTraversalUnsupported";
            if (OrdinaryInventory.Busy(s, c.Actor)) return "WorkerBusy";
            if (!Permissions(s, c.Actor).VoluntarySpeed || Speed(s, c.Actor) == 0) return "ConditionPreventsMovement";

            var actor = s.Actors.Single(x => x.Id == c.Actor);
            int toX, toY;
            try { toX = checked(actor.X + c.X); toY = checked(actor.Y + c.Y); }
            catch (OverflowException) { return "InvalidWorldStep"; }
            var spatial = WorldSpatialQueries.Step(s, actor.Id, actor.X, actor.Y, toX, toY, false, false, TestOnlyPolicy.Walkable);
            if (spatial == SpatialStepFailure.Blocked) return "Blocked";
            if (spatial == SpatialStepFailure.Occupied) return "Occupied";

            bool startsEncounter = s.WorldSchedule.Order.Where(id => id != actor.Id && !SoldierTacticalFeatures.IsAlly(s, actor.Id, id)
                && (connectedCombat == null || !s.Lives.Single(l => l.ActorId == id).Dead)).Any(id => {
                    var enemy = s.Actors.Single(a => a.Id == id);
                    return WorldSpatialQueries.WithinRange(actor.X, actor.Y, enemy.X, enemy.Y, 1)
                        || WorldSpatialQueries.WithinRange(toX, toY, enemy.X, enemy.Y, 1);
                });
            if (startsEncounter && connectedCombat == null) return "TacticalTransitionRequired";
            bool dashPaid = false;
            if (c.Target == "run")
            {
                dashPaid = scheduled ? Interval(s, c.Actor).DashPaid : ActivityInterval(s, c.Actor).DashPaid;
                if (scheduled)
                {
                    var interval = Interval(s, c.Actor);
                    if (!dashPaid && interval.ActionSpent) return "ActionAlreadySpent";
                    if (!dashPaid && !Permissions(s, c.Actor).Dash) return "ConditionPreventsDash";
                }
                else
                {
                    var activity = ActivityInterval(s, c.Actor);
                    if (!dashPaid && ActivityHasLabor(s, c.Actor)) return "OffCalendarLaborOverlapsActivity";
                    if (!dashPaid && activity.Action != WorldActionCommitment.None) return "ActionAlreadySpent";
                    if (!dashPaid && !Permissions(s, c.Actor).Dash) return "ConditionPreventsDash";
                }
            }
            var edge = new WorldTraversalRecord(c.Actor, s.Revision + 1, actor.X, actor.Y, toX, toY, running: c.Target == "run");
            long movementCost;
            try { movementCost = checked(CostPerFoot(s, edge) * 5); }
            catch (OverflowException) { return "InvalidWorldStep"; }
            bool hasActivityBudget = offCalendar && IsOffCalendarActivity(s, c.Actor);
            RuleQuantity available = scheduled ? Remaining(s, c.Actor)
                : hasActivityBudget ? ActivityRemaining(s, c.Actor) : new RuleQuantity(long.MaxValue);
            if (c.Target == "run") {
                if (!dashPaid) {
                    var maximum = new RuleQuantity(Speed(s, c.Actor)).Scale(2);
                    var spent = scheduled ? Interval(s, c.Actor).MovementSpent : ActivityInterval(s, c.Actor).MovementSpent;
                    available = maximum > spent ? maximum - spent : default;
                }
            }
            // Starting a route edge does not spend its full distance immediately. Slow actors
            // accrue exact partial progress across later clock intervals, so only an exhausted
            // movement allowance prevents entering the edge.
            if ((scheduled || hasActivityBudget) && available == default) return "InsufficientMovement";
            facts = new WorldStepFacts { Scheduled = scheduled, OffCalendar = offCalendar, StartsEncounter = startsEncounter,
                DashAlreadyPaid = dashPaid,
                ToX = toX, ToY = toY, Cost = movementCost };
            return null;
        }

        private string AssessTraversalControl(Snapshot s, Command c, out WorldTraversalRecord edge)
        {
            edge = null;
            if (c.Inventory != null || c.Target != "" || c.X != 0 || c.Y != 0) return "InvalidTraversalControl";
            edge = s.WorldTraversals.SingleOrDefault(x => x.ActorId == c.Actor);
            if (edge == null) return "NoPendingTraversal";
            if (c.Kind == CommandKind.SuspendWorldStep)
                return edge.Status == WorldTraversalStatus.Suspended ? "TraversalAlreadySuspended" : null;
            if (c.Kind != CommandKind.ResumeWorldStep) return "InvalidTraversalControl";
            bool offCalendarActivity = IsOffCalendarActivity(s, c.Actor);
            bool waitingForFreshActivityDash = offCalendarActivity && edge.Running && edge.Status == WorldTraversalStatus.WaitingForRefresh;
            if (edge.Status != WorldTraversalStatus.Suspended && !waitingForFreshActivityDash) return "TraversalNotSuspended";
            if (!s.WorldSchedule.Order.Contains(c.Actor) && edge.Running && !offCalendarActivity) return "OffCalendarDashBudgetUnsupported";
            if (!Permissions(s, c.Actor).VoluntarySpeed || Speed(s, c.Actor) == 0) return "ConditionPreventsMovement";
            if (edge.Running)
            {
                bool dashPaid = s.WorldSchedule.Order.Contains(c.Actor) ? Interval(s, c.Actor).DashPaid : ActivityInterval(s, c.Actor).DashPaid;
                if (!dashPaid)
                {
                    if (s.WorldSchedule.Order.Contains(c.Actor))
                    {
                        if (Interval(s, c.Actor).ActionSpent) return "ActionAlreadySpent";
                        if (!Permissions(s, c.Actor).Dash) return "ConditionPreventsDash";
                    }
                    else
                    {
                        if (ActivityHasLabor(s, c.Actor)) return "OffCalendarLaborOverlapsActivity";
                        if (ActivityInterval(s, c.Actor).Action != WorldActionCommitment.None) return "ActionAlreadySpent";
                        if (!Permissions(s, c.Actor).Dash) return "ConditionPreventsDash";
                    }
                }
            }
            return null;
        }

        private string AssessRepairStart(Snapshot s, Command c)
        {
            if (repair == null) return "ToolRepairNotSelected";
            if (c.Inventory != null || c.Combat != null || c.X != 0 || c.Y != 0) return "InvalidRepairRequest";
            if (PendingCalendarChoice(s)) return "TacticalChoicePending";
            string access = RepairAccess(s, c.Actor, c.Target);
            if (access != null) return access;
            if (s.RepairWork.Any(x => x.TargetId == c.Target && x.Open)) return "RepairTargetClaimed";
            var target = s.Structures.Single(x => x.Id == c.Target);
            if (target.Hp == target.MaximumHp) return "TargetDoesNotNeedRepair";
            if (RepairWorkerBusy(s, c.Actor, c.Target)) return "WorkerBusy";
            if (s.Work.AvailableAmount(RepairMaterialsLotId) < new RuleQuantity(1)) return "RepairMaterialsUnavailable";
            if (s.RepairWork.Length == RepairWorkValidation.MaxRecords) return "RepairHistoryCapacityReached";
            return null;
        }

        private string AssessRepairCommand(Snapshot s, Command c, out RepairWorkRecord current)
        {
            current = null;
            if (repair == null) return "ToolRepairNotSelected";
            if (c.Inventory != null || c.Combat != null || c.X != 0 || c.Y != 0) return "InvalidRepairRequest";
            if (PendingCalendarChoice(s)) return "TacticalChoicePending";
            if (c.Kind == CommandKind.StartToolRepair) return AssessRepairStart(s, c);
            current = s.RepairWork.SingleOrDefault(x => x.Id == c.Target && x.WorkerId == c.Actor);
            if (current == null) return "UnknownRepairWork";
            if (!current.Open) return "RepairWorkClosed";
            if (c.Kind == CommandKind.PauseToolRepair)
                return current.Status == RepairWorkStatus.Working ? null : "RepairNotWorking";
            if (c.Kind == CommandKind.CancelToolRepair) return null;
            if (c.Kind != CommandKind.ResumeToolRepair) return "InvalidRepairRequest";
            if (current.Status == RepairWorkStatus.Working) return "RepairAlreadyWorking";
            string access = RepairAccess(s, c.Actor, current.TargetId, current.Status != RepairWorkStatus.AwaitingCheck);
            if (access != null) return access;
            if (RepairWorkerBusy(s, c.Actor, current.TargetId)) return "WorkerBusy";
            return null;
        }

        private IEnumerable<Command> DiscoverSharedWorldCommands(Snapshot s, Authority authority, string actor)
        {
            var options = new List<Command>(); int index = 0;
            var pending = s.WorldTraversals.SingleOrDefault(x => x.ActorId == actor);
            if (pending != null)
            {
                var kind = pending.Status == WorldTraversalStatus.Suspended || pending.Status == WorldTraversalStatus.WaitingForRefresh
                    ? CommandKind.ResumeWorldStep : CommandKind.SuspendWorldStep;
                yield return new Command("option." + s.Revision.ToString(CultureInfo.InvariantCulture) + ".world." + (index++).ToString(CultureInfo.InvariantCulture),
                    actor, s.Revision, kind);
            }
            else
            {
                foreach (var delta in new[] { new[] { 0, -1 }, new[] { -1, 0 }, new[] { 1, 0 }, new[] { 0, 1 } })
                    foreach (string mode in new[] { "walk", "run" })
                        yield return new Command("option." + s.Revision.ToString(CultureInfo.InvariantCulture) + ".world." + (index++).ToString(CultureInfo.InvariantCulture),
                            actor, s.Revision, CommandKind.BeginWorldStep, mode, delta[0], delta[1]);
            }
            if (repair != null && IsRepairWorker(actor))
            {
                var job = s.RepairWork.SingleOrDefault(x => x.WorkerId == actor && x.Open);
                if (job == null)
                {
                    yield return new Command("option." + s.Revision.ToString(CultureInfo.InvariantCulture) + ".repair." + (index++).ToString(CultureInfo.InvariantCulture),
                        actor, s.Revision, CommandKind.StartToolRepair, SharedCraftingFixture.ToolId);
                }
                else
                {
                    if (job.Status == RepairWorkStatus.Working)
                        yield return new Command("option." + s.Revision.ToString(CultureInfo.InvariantCulture) + ".repair." + (index++).ToString(CultureInfo.InvariantCulture),
                            actor, s.Revision, CommandKind.PauseToolRepair, job.Id);
                    else
                        yield return new Command("option." + s.Revision.ToString(CultureInfo.InvariantCulture) + ".repair." + (index++).ToString(CultureInfo.InvariantCulture),
                            actor, s.Revision, CommandKind.ResumeToolRepair, job.Id);
                    yield return new Command("option." + s.Revision.ToString(CultureInfo.InvariantCulture) + ".repair." + (index++).ToString(CultureInfo.InvariantCulture),
                        actor, s.Revision, CommandKind.CancelToolRepair, job.Id);
                }
            }
            if (harvestFixture != null && IsHarvestWorker(actor))
            {
                var attempt = s.HarvestAttempts.SingleOrDefault(x => x.WorkerId == actor
                    && (x.Status == HarvestAttemptStatus.Working || x.Status == HarvestAttemptStatus.Paused));
                if (attempt != null)
                {
                    var kind = attempt.Status == HarvestAttemptStatus.Working ? CommandKind.PauseHarvest : CommandKind.ResumeHarvest;
                    yield return new Command("option." + s.Revision.ToString(CultureInfo.InvariantCulture) + ".harvest." + (index++).ToString(CultureInfo.InvariantCulture),
                        actor, s.Revision, kind, attempt.Id);
                }
                else if (s.HarvestAttempts.Length == 0)
                {
                    var manifest = s.HarvestManifests.SingleOrDefault();
                    foreach (var category in s.HarvestCategories.Where(x => x.ManifestId == manifest?.Id).OrderBy(x => x.Id, StringComparer.Ordinal))
                    {
                        if (manifest == null) break;
                        if (s.SchemaVersion >= Snapshot.HarvestManifestSchema)
                        {
                            var selection = new HarvestSelectionRequest(manifest.AnatomyVersionId, new[] { category.Id });
                            yield return new Command("option." + s.Revision.ToString(CultureInfo.InvariantCulture) + ".harvest." + (index++).ToString(CultureInfo.InvariantCulture),
                                actor, s.Revision, CommandKind.StartHarvest, manifest.Id, harvestSelection: selection);
                        }
                        else
                        {
                            yield return new Command("option." + s.Revision.ToString(CultureInfo.InvariantCulture) + ".harvest." + (index++).ToString(CultureInfo.InvariantCulture),
                                actor, s.Revision, CommandKind.StartHarvest, category.Id);
                        }
                    }
                }
            }
            foreach (var command in DiscoverFishingTrapControls(s, actor)) yield return command;
            foreach (var command in DiscoverManufacturingQualityChoices(s, actor)) yield return command;
        }

        private IEnumerable<Command> DiscoverTacticalMovementCommands(Snapshot s, string actor)
        {
            int index = 0; string turnId = s.Encounter.CurrentTurnId;
            foreach (var delta in new[] { new[] { -1, -1 }, new[] { -1, 0 }, new[] { -1, 1 }, new[] { 0, -1 },
                new[] { 0, 1 }, new[] { 1, -1 }, new[] { 1, 0 }, new[] { 1, 1 } })
            {
                yield return new Command("option." + s.Revision.ToString(CultureInfo.InvariantCulture) + ".tactical-step." + (index++).ToString(CultureInfo.InvariantCulture),
                    actor, s.Revision, CommandKind.TacticalStep, turnId, delta[0], delta[1]);
                yield return new Command("option." + s.Revision.ToString(CultureInfo.InvariantCulture) + ".tactical-reposition." + (index++).ToString(CultureInfo.InvariantCulture),
                    actor, s.Revision, CommandKind.TacticalRepositionStep, turnId, delta[0], delta[1]);
            }
        }

        private CommandQueryResult QuerySharedWorldCommand(Snapshot s, Authority authority, Command c)
        {
            if (c.Kind == CommandKind.Interact) return QueryFishingTrapControl(s, c);
            if (c.Kind == CommandKind.ResolveManufacturingQuality) return QueryManufacturingQualityChoice(s, c);
            if (c.Kind == CommandKind.TacticalStep || c.Kind == CommandKind.TacticalRepositionStep)
            {
                if (!s.InventoryCombat) return new CommandQueryResult(true, false, "TacticalMovementRequiresEncounter", s.Revision);
                string failure = bodies.AssessTacticalMovementCommand(s, c, out long movementCost);
                var costs = new List<CommandCost>();
                if (failure == null) costs.Add(new CommandCost("movement-feet", "", movementCost));
                return new CommandQueryResult(true, failure == null, failure ?? "Available", s.Revision, costs);
            }
            if (c.Kind == CommandKind.StartHarvest || c.Kind == CommandKind.PauseHarvest || c.Kind == CommandKind.ResumeHarvest)
            {
                string failure = AssessHarvestCommand(s, c, out var facts);
                var costs = new List<CommandCost>();
                if (failure == null && c.Kind == CommandKind.StartHarvest)
                {
                    if (facts.Duration.Denominator == 1)
                        costs.Add(new CommandCost("work-seconds", "", facts.Duration.Numerator));
                    costs.AddRange(facts.UnitIds.Select(id => new CommandCost("finite-source-unit", id, 1)));
                }
                else if (failure == null && c.Kind == CommandKind.ResumeHarvest && facts.Current.WorkDone < facts.Current.Duration
                    && facts.Current.Duration.Denominator == 1)
                {
                    var remaining = CampGreens.Subtract(facts.Current.Duration, facts.Current.WorkDone);
                    if (remaining.Denominator == 1) costs.Add(new CommandCost("work-seconds", "", remaining.Numerator));
                }
                return new CommandQueryResult(true, failure == null, failure ?? "Available", s.Revision, costs);
            }
            if (s.InventoryCombat && (c.Kind == CommandKind.BeginWorldStep || c.Kind == CommandKind.SuspendWorldStep || c.Kind == CommandKind.ResumeWorldStep))
                return new CommandQueryResult(false, false, "UnsupportedOperation", s.Revision);
            if (c.Kind == CommandKind.BeginWorldStep)
            {
                string failure = AssessWorldStep(s, c, out var facts);
                if (failure != null) return new CommandQueryResult(true, false, failure, s.Revision);
                if (facts.StartsEncounter) return new CommandQueryResult(true, true, "EncounterTransition", s.Revision);
                var costs = new List<CommandCost> { new CommandCost("movement-feet", "", facts.Cost) };
                if (c.Target == "run" && !facts.DashAlreadyPaid) costs.Add(new CommandCost("action", "", 1));
                return new CommandQueryResult(true, true, "Available", s.Revision, costs);
            }
            if (c.Kind == CommandKind.SuspendWorldStep || c.Kind == CommandKind.ResumeWorldStep)
            {
                string failure = AssessTraversalControl(s, c, out var edge);
                var costs = new List<CommandCost>();
                if (failure == null && c.Kind == CommandKind.ResumeWorldStep && edge.Running)
                {
                    bool paid = s.WorldSchedule.Order.Contains(c.Actor) ? Interval(s, c.Actor).DashPaid : ActivityInterval(s, c.Actor).DashPaid;
                    if (!paid) costs.Add(new CommandCost("action", "", 1));
                }
                return new CommandQueryResult(true, failure == null, failure ?? "Available", s.Revision, costs);
            }
            if (c.Kind == CommandKind.StartToolRepair)
            {
                string failure = AssessRepairCommand(s, c, out _);
                if (failure != null) return new CommandQueryResult(true, false, failure, s.Revision);
                var target = s.Structures.Single(x => x.Id == c.Target);
                var costs = new[] { new CommandCost("resource", RepairMaterialsLotId, 1),
                    new CommandCost("work-seconds", "", ObjectStructureRules.RepairLabor(target).Numerator) };
                return new CommandQueryResult(true, true, "Available", s.Revision, costs);
            }
            if (c.Kind == CommandKind.PauseToolRepair || c.Kind == CommandKind.ResumeToolRepair || c.Kind == CommandKind.CancelToolRepair)
            {
                string failure = AssessRepairCommand(s, c, out _);
                return new CommandQueryResult(true, failure == null, failure ?? "Available", s.Revision);
            }
            return null;
        }
    }
}
#endif
