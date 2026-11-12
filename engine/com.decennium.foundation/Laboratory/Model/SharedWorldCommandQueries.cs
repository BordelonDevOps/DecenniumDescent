#if DECENNIUM_TEST_ONLY && (UNITY_EDITOR || DEVELOPMENT_BUILD || HEADLESS_TESTS)
using System;
using System.Collections.Generic;
using System.Globalization;
using System.Linq;

namespace Decennium.Foundation.Laboratory
{
    public sealed partial class TestOnlySharedWorldPolicy
    {
        private bool WorldWalkable(Snapshot s, int x, int y)
            => TestOnlyPolicy.Walkable(x, y) && (observationFixture == null || ObservationGeometry.SupportsAnchorAt(s, x, y));

        private sealed class WorldStepFacts
        {
            public bool Scheduled;
            public bool OffCalendar;
            public bool StartsEncounter;
            public bool DashAlreadyPaid;
            public bool DetachesRoute;
            public RuleQuantity InitialDistance;
            public int ToX;
            public int ToY;
            public long Cost;
            public CharterAttemptReadiness CharterDeparture;
        }

        private string AssessWorldStep(Snapshot s, Command c, out WorldStepFacts facts, bool reinforcementApproach = false)
        {
            facts = null;
            var definition = reinforcementApproach ? s.Reinforcement.Definition : null;
            string mode = reinforcementApproach ? "walk" : c.Target;
            int dx = reinforcementApproach ? definition.EntryX - definition.FromX : c.X;
            int dy = reinforcementApproach ? definition.EntryY - definition.FromY : c.Y;
            var expected = reinforcementApproach ? CommandKind.BeginReinforcementApproach : CommandKind.BeginWorldStep;
            if (c.Kind != expected || c.Inventory != null || (mode != "walk" && mode != "run")
                || !WorldSpatialQueries.Neighbor(0, 0, dx, dy, false)) return "InvalidWorldStep";
            if (s.RouteTravels.Any(x => x.Status == ExpeditionRouteTravelStatus.Moving && x.TravelerId == c.Actor))
                return "RouteTravelMustPauseFirst";
            if (routeMotionFixture != null && s.RouteTravelSpatial.Any(x => !x.Detached && x.TravelerId != c.Actor))
                return "RouteTravelerMustDetachBeforeOtherMovement";
            bool scheduled = WorldTiming.ForActor(s, c.Actor) != null;
            bool offCalendar = !scheduled && (c.Actor == TestOnlyPolicy.CompanionId || IsOffCalendarActivity(s, c.Actor));
            if (!scheduled && (!offCalendar || s.InventoryCombat && !reinforcementApproach)) return "NoActivityCalendar";
            if (!scheduled && mode == "run" && !IsOffCalendarActivity(s, c.Actor)) return "OffCalendarDashBudgetUnsupported";
            if (s.WorldTraversals.Any(x => x.ActorId == c.Actor)) return "TraversalAlreadyPending";
            if (s.WorldTraversals.Any(x => WorldTiming.ForActor(s, x.ActorId) != null))
                return scheduled ? "ConcurrentHostileTraversalUnsupported" : "ConcurrentWorldTraversalUnsupported";
            if (s.WorldTraversals.Length != 0) return "ConcurrentWorldTraversalUnsupported";
            if (OrdinaryInventory.Busy(s, c.Actor)) return "WorkerBusy";
            if (!Permissions(s, c.Actor).VoluntarySpeed || Speed(s, c.Actor) == 0) return "ConditionPreventsMovement";

            var actor = s.Actors.Single(x => x.Id == c.Actor);
            int toX, toY;
            try { toX = checked(actor.X + dx); toY = checked(actor.Y + dy); }
            catch (OverflowException) { return "InvalidWorldStep"; }
            string pressurePathFailure=AssessExpeditionPressureMovement(s,c.Actor,actor.X,actor.Y,toX,toY,false)
                ?? AssessLocalRetreatMovement(s,c.Actor,actor.X,actor.Y,toX,toY,false);
            if(pressurePathFailure!=null)return pressurePathFailure;
            if(HuntingTrapValidation.BlocksGridMove(s,c.Actor,toX,toY))return "HuntingTrapTetherPreventsMovement";
            RuleQuantity initialDistance = default;
            bool detachesRoute = false;
            if (routeMotionFixture != null)
            {
                var travel = OpenRouteTravel(s, c.Actor);
                var spatialPosition = s.RouteTravelSpatial.SingleOrDefault(x => x.TravelerId == c.Actor);
                if (travel != null && travel.Status == ExpeditionRouteTravelStatus.Paused
                    && spatialPosition != null && !spatialPosition.Detached)
                {
                    var route = routeTravelFixture.Find(travel.RouteId);
                    var checkpoint = route.PositionAt(travel.Progress);
                    if (checkpoint == null || actor.X != checkpoint.X || actor.Y != checkpoint.Y
                        || spatialPosition.X != routeMotionFixture.PositionAt(route.Id, travel.Progress).X
                        || spatialPosition.Y != routeMotionFixture.PositionAt(route.Id, travel.Progress).Y)
                        return "RoutePositionAuthorityMismatch";
                    var pose = new ObservationPoint(spatialPosition.X, spatialPosition.Y);
                    bool atCheckpoint = pose.X.Denominator == 1 && pose.Y.Denominator == 1;
                    if (!atCheckpoint)
                    {
                        var leg = routeMotionFixture.LegAt(route.Id, travel.Progress);
                        if (leg == null || actor.X != leg.FromX || actor.Y != leg.FromY
                            || toX != leg.ToX || toY != leg.ToY)
                            return "RouteDepartureDirectionUnsupported";
                        initialDistance = leg.DistanceFeetAt(travel.Progress);
                        if (initialDistance <= default(RuleQuantity) || initialDistance >= new RuleQuantity(5))
                            return "RouteDepartureOffsetUnsupported";
                    }
                    detachesRoute = true;
                }
            }
            var spatial = WorldSpatialQueries.Step(s, actor.Id, actor.X, actor.Y, toX, toY, false, false, (x, y) => WorldWalkable(s, x, y));
            if (spatial == SpatialStepFailure.Blocked) return "Blocked";
            if (spatial == SpatialStepFailure.Occupied) return "Occupied";
            if (RoutePathReserved(s, actor.Id, toX, toY)) return "RouteTravelPathReserved";

            bool startsEncounter = WorldStepWouldStartEncounter(s, actor.Id, actor.X, actor.Y, toX, toY);
            if (startsEncounter && s.RestIntervals.Any(x => x.Status == RestIntervalStatus.Active))
                return "RestInterruptionAuthorityUnsupported";
            if (startsEncounter && HasActiveHavenCare(s)) return "HavenCareCombatTransitionUnsupported";
            if (startsEncounter && connectedCombat == null) return "TacticalTransitionRequired";
            bool dashPaid = false;
            if (mode == "run")
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
            var edge = new WorldTraversalRecord(c.Actor, s.Revision + 1, actor.X, actor.Y, toX, toY,
                initialDistance, running: mode == "run");
            long movementCost;
            try { movementCost = checked(CostPerFoot(s, edge) * 5); }
            catch (OverflowException) { return "InvalidWorldStep"; }
            bool hasActivityBudget = offCalendar && IsOffCalendarActivity(s, c.Actor);
            RuleQuantity available = scheduled ? Remaining(s, c.Actor)
                : hasActivityBudget ? ActivityRemaining(s, c.Actor) : new RuleQuantity(long.MaxValue);
            if (mode == "run") {
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
                DashAlreadyPaid = dashPaid, DetachesRoute = detachesRoute, InitialDistance = initialDistance,
                ToX = toX, ToY = toY, Cost = movementCost };
            return AssessLaterWorldStep(s, edge) ?? AssessReengagementDeparture(s, c) ?? AssessCharterWorldStep(s, c, facts);
        }

        private static WorldTraversalRecord AddOrdinaryWorldTraversal(Snapshot state, Command command, WorldStepFacts facts, bool running)
        {
            var actor = state.Actors.Single(x => x.Id == command.Actor);
            var edge = new WorldTraversalRecord(actor.Id, state.Revision + 1, actor.X, actor.Y, facts.ToX, facts.ToY,
                facts.InitialDistance, running);
            state.WorldTraversals = state.WorldTraversals.Append(edge).ToArray();
            return edge;
        }

        private bool WorldStepWouldStartEncounter(Snapshot s, string actor, int fromX, int fromY, int toX, int toY)
            => (s.LaterEncounter == null || s.LaterEncounter.FirstExit == null && s.WorldSchedule.Order.Contains(actor))
                && s.WorldSchedule.Order.Where(id => id != actor && !SoldierTacticalFeatures.IsAlly(s, actor, id)
                && (connectedCombat == null || !s.Lives.Single(l => l.ActorId == id).Dead)).Any(id => {
                    var enemy = s.Actors.Single(a => a.Id == id);
                    return WorldSpatialQueries.WithinRange(fromX, fromY, enemy.X, enemy.Y, 1)
                        || WorldSpatialQueries.WithinRange(toX, toY, enemy.X, enemy.Y, 1);
                });

        private bool RoutePathReserved(Snapshot s, string actor, int x, int y)
        {
            if (routeTravelFixture == null) return false;
            foreach (var travel in s.RouteTravels.Where(t => t.Status == ExpeditionRouteTravelStatus.Moving
                && t.TravelerId != actor))
            {
                var route = routeTravelFixture.Find(travel.RouteId);
                if (route != null && route.Positions.Any(p => p.Progress > travel.Progress && p.X == x && p.Y == y))
                    return true;
            }
            return false;
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
            string contactObstruction = ReengagementTraversalObstruction(s, edge);
            if (contactObstruction != null) return contactObstruction;
            bool offCalendarActivity = IsOffCalendarActivity(s, c.Actor);
            bool waitingForFreshActivityDash = offCalendarActivity && edge.Running && edge.Status == WorldTraversalStatus.WaitingForRefresh;
            if (edge.Status != WorldTraversalStatus.Suspended && !waitingForFreshActivityDash) return "TraversalNotSuspended";
            if (WorldTiming.ForActor(s, c.Actor) == null && edge.Running && !offCalendarActivity) return "OffCalendarDashBudgetUnsupported";
            if (!Permissions(s, c.Actor).VoluntarySpeed || Speed(s, c.Actor) == 0) return "ConditionPreventsMovement";
            if (edge.Running)
            {
                bool dashPaid = WorldTiming.ForActor(s, c.Actor) != null ? Interval(s, c.Actor).DashPaid : ActivityInterval(s, c.Actor).DashPaid;
                if (!dashPaid)
                {
                    if (WorldTiming.ForActor(s, c.Actor) != null)
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
            return AssessCharterTraversalResume(s, edge);
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
            if (restDebtProfile != null && restDebtProfile.IncludesActor(actor))
            {
                var activeRest = s.RestIntervals.SingleOrDefault(x => x.ActorId == actor && x.Status == RestIntervalStatus.Active);
                if (activeRest != null)
                    yield return new Command("option." + s.Revision.ToString(CultureInfo.InvariantCulture) + ".rest.interrupt",
                        actor, s.Revision, CommandKind.InterruptRest, activeRest.Id);
                else
                {
                    int restSiteIndex = 0;
                    var actorBody = s.Actors.Single(x => x.Id == actor);
                    foreach (var site in restDebtProfile.Sites.Where(x => x.SafeBerth && x.QualifyingRestEligible
                        && actorBody.X == x.X && actorBody.Y == x.Y).OrderBy(x => x.Id, StringComparer.Ordinal))
                        yield return new Command("option." + s.Revision.ToString(CultureInfo.InvariantCulture) + ".rest.begin."
                            + (restSiteIndex++).ToString(CultureInfo.InvariantCulture), actor, s.Revision,
                            CommandKind.BeginRest, site.Id);
                }

                long currentDay = checked((long)(s.RuleClock.Numerator
                    / ((System.Numerics.BigInteger)s.RuleClock.Denominator * 86400)));
                foreach (long day in new[] { currentDay, checked(currentDay + 1) })
                {
                    if (s.RestWatchSchedules.Length >= ExpeditionProvisioningValidation.MaxRestWatchSchedules) break;
                    for (int slot = 0; slot <= (int)RestWatchSlot.Evening; slot++)
                    {
                        if (WatchStart(day, (RestWatchSlot)slot) < s.RuleClock) continue;
                        yield return new Command("option." + s.Revision.ToString(CultureInfo.InvariantCulture) + ".rest.schedule."
                            + day.ToString(CultureInfo.InvariantCulture) + "." + slot.ToString(CultureInfo.InvariantCulture),
                            actor, s.Revision, CommandKind.ScheduleRestWatch,
                            "day." + day.ToString(CultureInfo.InvariantCulture), slot);
                    }
                }
            }
            foreach (var moraleCommand in DiscoverMoraleRestCommands(s, actor)) yield return moraleCommand;
            foreach (var havenCommand in DiscoverHavenCareCommands(s, actor)) yield return havenCommand;
            foreach (var saleCommand in DiscoverHavenSaleCommands(s, actor)) yield return saleCommand;
            foreach (var mealCommand in DiscoverHavenMealCommands(s, actor)) yield return mealCommand;
            foreach (var billCommand in DiscoverExpeditionBillCommands(s, actor)) yield return billCommand;
            foreach (var planCommand in DiscoverNextCharterPlan(s, actor)) yield return planCommand;
            foreach (var agreementCommand in DiscoverNextCharterAgreement(s, actor)) yield return agreementCommand;
            foreach (var attemptCommand in DiscoverCharterAttempt(s, actor)) yield return attemptCommand;
            var closeCommand = DiscoverExpeditionClose(s, actor);
            if (closeCommand != null) yield return closeCommand;
            foreach (var campCommand in DiscoverExpeditionCampUseCommands(s, actor)) yield return campCommand;
            foreach (var campBuildCommand in DiscoverTemporaryCampConstructionCommands(s, actor)) yield return campBuildCommand;
            foreach(var advancement in CharacterAdvancementRules.Discover(s,actor))yield return advancement;
            var pending = s.WorldTraversals.SingleOrDefault(x => x.ActorId == actor);
            var routeTravel = routeTravelFixture == null ? null : OpenRouteTravel(s, actor);
            if (pending != null)
            {
                var kind = pending.Status == WorldTraversalStatus.Suspended || pending.Status == WorldTraversalStatus.WaitingForRefresh
                    ? CommandKind.ResumeWorldStep : CommandKind.SuspendWorldStep;
                yield return new Command("option." + s.Revision.ToString(CultureInfo.InvariantCulture) + ".world." + (index++).ToString(CultureInfo.InvariantCulture),
                    actor, s.Revision, kind);
            }
            else if (!s.RouteTravels.Any(x => x.Status == ExpeditionRouteTravelStatus.Moving && x.TravelerId == actor))
            {
                foreach (var delta in new[] { new[] { 0, -1 }, new[] { -1, 0 }, new[] { 1, 0 }, new[] { 0, 1 } })
                    foreach (string mode in new[] { "walk", "run" })
                        yield return new Command("option." + s.Revision.ToString(CultureInfo.InvariantCulture) + ".world." + (index++).ToString(CultureInfo.InvariantCulture),
                            actor, s.Revision, CommandKind.BeginWorldStep, mode, delta[0], delta[1]);
            }
            if(routeTravel!=null)
                yield return new Command("option."+s.Revision.ToString(CultureInfo.InvariantCulture)+".route."+(index++).ToString(CultureInfo.InvariantCulture),
                    actor,s.Revision,routeTravel.Status==ExpeditionRouteTravelStatus.Moving?CommandKind.PauseRouteTravel:CommandKind.ResumeRouteTravel,
                    routeTravel.RouteId);
            else if(routeTravelFixture!=null&&!s.RouteTravels.Any(x=>x.TravelerId==actor
                &&(x.Status==ExpeditionRouteTravelStatus.Moving||x.Status==ExpeditionRouteTravelStatus.Paused)))
                foreach(var route in routeTravelFixture.Routes.OrderBy(x=>x.Id,StringComparer.Ordinal))
                    yield return new Command("option."+s.Revision.ToString(CultureInfo.InvariantCulture)+".route."+(index++).ToString(CultureInfo.InvariantCulture),
                        actor,s.Revision,CommandKind.StartRouteTravel,route.Id);
            if(routeMappingFixture!=null)
                foreach(var result in routeMappingFixture.Results.Where(x=>x.ActorId==actor
                    &&s.RouteMappingResults.All(applied=>applied.ResultId!=x.ResultId)).OrderBy(x=>x.ResultId,StringComparer.Ordinal))
                    yield return new Command("option."+s.Revision.ToString(CultureInfo.InvariantCulture)+".route-mapping."+(index++).ToString(CultureInfo.InvariantCulture),
                        actor,s.Revision,CommandKind.ConsumeTestOnlyRouteMappingResult,result.ResultId);
            if (routeReconnaissanceFixture != null)
            {
                foreach (var currentReconnaissance in s.RouteReconnaissanceAttempts.Where(x => x.LeadId == actor
                    && x.Status != ExpeditionRouteReconnaissanceStatus.Resolved).OrderBy(x => x.StartedRevision))
                {
                    CommandKind control = currentReconnaissance.Status == ExpeditionRouteReconnaissanceStatus.Working
                        ? CommandKind.PauseRouteReconnaissance : CommandKind.ResumeRouteReconnaissance;
                    yield return new Command("option." + s.Revision.ToString(CultureInfo.InvariantCulture) + ".route-recon."
                        + (index++).ToString(CultureInfo.InvariantCulture), actor, s.Revision, control, currentReconnaissance.Id);
                }
                foreach (var task in routeReconnaissanceFixture.Tasks.OrderBy(x => x.RouteId, StringComparer.Ordinal))
                {
                    var segment = s.RouteSegments.SingleOrDefault(x => x.RouteId == task.RouteId
                        && x.StartingProgress == default);
                    if (segment != null && segment.Status != ExpeditionRouteSegmentStatus.ReconnaissanceRequired) continue;
                    if (segment != null && segment.TravelerId != actor) continue;
                    yield return new Command("option." + s.Revision.ToString(CultureInfo.InvariantCulture) + ".route-recon."
                        + (index++).ToString(CultureInfo.InvariantCulture), actor, s.Revision,
                        CommandKind.StartRouteReconnaissance, task.RouteId);
                }
            }
            if (routeMappingWorkFixture != null)
            {
                foreach (var currentMappingWork in s.RouteMappingWorkAttempts.Where(x => x.LeadId == actor
                    && x.Status != ExpeditionRouteMappingWorkStatus.Resolved).OrderBy(x => x.StartedRevision))
                {
                    CommandKind control = currentMappingWork.Status == ExpeditionRouteMappingWorkStatus.Working
                        ? CommandKind.PauseRouteMappingWork : CommandKind.ResumeRouteMappingWork;
                    yield return new Command("option." + s.Revision.ToString(CultureInfo.InvariantCulture) + ".route-work." + (index++).ToString(CultureInfo.InvariantCulture),
                        actor, s.Revision, control, currentMappingWork.Id);
                }
                foreach (var task in routeMappingWorkFixture.Tasks.OrderBy(x => x.RouteId, StringComparer.Ordinal))
                {
                    if (s.RouteMappingWorkAttempts.Any(x => x.RouteId == task.RouteId
                        && x.Status != ExpeditionRouteMappingWorkStatus.Resolved)) continue;
                    Command CreateRouteWork(string[] helpers)
                        => new Command("option." + s.Revision.ToString(CultureInfo.InvariantCulture) + ".route-work." + (index++).ToString(CultureInfo.InvariantCulture),
                            actor, s.Revision, CommandKind.StartRouteMappingWork, task.RouteId,
                            routeMappingWork: new RouteMappingWorkRequest(helpers));
                    yield return CreateRouteWork(Array.Empty<string>());
                    var route = routeTravelFixture.Find(task.RouteId);
                    var assistants = s.Actors.Where(x => x.Id != actor
                            && WorldSpatialQueries.CardinalDistance(x.X, x.Y, route.FromX, route.FromY) == 1
                            && CharacterSkillTrainingFacts.IsTrained(s, x.Id,
                                TestOnlyExpeditionRouteMappingWorkFixture.SkillId))
                        .Select(x => x.Id).OrderBy(x => x, StringComparer.Ordinal).ToArray();
                    for (int first = 0; first < assistants.Length; first++)
                    {
                        yield return CreateRouteWork(new[] { assistants[first] });
                        for (int second = first + 1; second < assistants.Length; second++)
                        {
                            yield return CreateRouteWork(new[] { assistants[first], assistants[second] });
                            for (int third = second + 1; third < assistants.Length; third++)
                                yield return CreateRouteWork(new[] { assistants[first], assistants[second], assistants[third] });
                        }
                    }
                }
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
            if(harvestPreservationEnabled&&!harvestPreservationTreatmentEnabled) {
                var work=s.HarvestRequirementWorks.SingleOrDefault(x=>x.WorkerId==actor
                    &&(x.Status==HarvestRequirementWorkStatus.Working||x.Status==HarvestRequirementWorkStatus.Paused));
                if(work!=null) {
                    var kind=work.Status==HarvestRequirementWorkStatus.Working
                        ?CommandKind.PauseHarvestRequirementWork:CommandKind.ResumeHarvestRequirementWork;
                    yield return new Command("option."+s.Revision.ToString(CultureInfo.InvariantCulture)+".harvest-requirement."+(index++).ToString(CultureInfo.InvariantCulture),
                        actor,s.Revision,kind,work.Id);
                } else if(!OrdinaryInventory.Busy(s,actor)) {
                    foreach(var lot in s.InventoryLots.OrderBy(x=>x.LotId,StringComparer.Ordinal)) {
                        if(!HarvestPreservationRules.TryProject(s,lot.LotId,out var view)||view.State!=HarvestPreservationState.Fresh)continue;
                        RuleQuantity available=s.Work.AvailableAmount(lot.LotId);if(available==default)continue;
                        yield return new Command("option."+s.Revision.ToString(CultureInfo.InvariantCulture)+".harvest-requirement."+(index++).ToString(CultureInfo.InvariantCulture),
                            actor,s.Revision,CommandKind.StartHarvestRequirementWork,lot.LotId,
                            inventory:new InventoryRequest(available,"",HandlingKind.Pickup));
                    }
                }
            }
            if(harvestPreservationTreatmentEnabled&&actor==TestOnlyPolicy.ActorId
                &&s.WorldSchedule.Order.Contains(actor)&&!OrdinaryInventory.Busy(s,actor)) {
                foreach(var lot in s.InventoryLots.OrderBy(x=>x.LotId,StringComparer.Ordinal)) {
                    if(!HarvestPreservationRules.TryProject(s,lot.LotId,out var view)
                        ||view.State==HarvestPreservationState.Spoiled)continue;
                    RuleQuantity available=s.Work.AvailableAmount(lot.LotId);if(available==default)continue;
                    yield return new Command("option."+s.Revision.ToString(CultureInfo.InvariantCulture)
                        +".harvest-treatment."+(index++).ToString(CultureInfo.InvariantCulture),actor,s.Revision,
                        CommandKind.StartHarvestPreservationTreatment,lot.LotId,
                        inventory:new InventoryRequest(available,"",HandlingKind.Pickup));
                }
            }
            if(miningFixture!=null&&IsMiningWorker(actor)) {
                var attempt=s.MiningAttempts.SingleOrDefault(x=>x.WorkerId==actor
                    &&(x.Status==MiningAttemptStatus.Working||x.Status==MiningAttemptStatus.Paused||x.Status==MiningAttemptStatus.AwaitingCheck));
                if(attempt!=null) {
                    CommandKind kind=attempt.Status==MiningAttemptStatus.Working?CommandKind.PauseMining:CommandKind.ResumeMining;
                    yield return new Command("option."+s.Revision.ToString(CultureInfo.InvariantCulture)+".mining."+(index++).ToString(CultureInfo.InvariantCulture),
                        actor,s.Revision,kind,attempt.Id);
                } else if(s.MiningAttempts.Length==0) {
                    var deposit=s.MiningDeposits.SingleOrDefault();
                    foreach(var category in s.MiningCategories.Where(x=>x.DepositId==deposit?.Id&&x.Accessible).OrderBy(x=>x.Id,StringComparer.Ordinal)) {
                        if(deposit==null)break;
                        var selection=new MiningSelectionRequest(deposit.VersionId,new[]{category.Id});
                        yield return new Command("option."+s.Revision.ToString(CultureInfo.InvariantCulture)+".mining."+(index++).ToString(CultureInfo.InvariantCulture),
                            actor,s.Revision,CommandKind.StartMining,deposit.Id,miningSelection:selection);
                    }
                }
            }
            if(miningFixture!=null&&miningFixture.MineralPreparationProfiles.Length>0&&IsMiningWorker(actor)) {
                var attempts=s.MineralPreparationAttempts.Where(x=>x.WorkerId==actor
                    &&(x.Status==MineralPreparationStatus.Working||x.Status==MineralPreparationStatus.Paused
                        ||x.Status==MineralPreparationStatus.AwaitingCompletion))
                    .OrderBy(x=>x.StartedAt).ThenBy(x=>x.Id,StringComparer.Ordinal).ToArray();
                foreach(var attempt in attempts) {
                    CommandKind kind=attempt.Status==MineralPreparationStatus.Working
                        ?CommandKind.PauseMineralPreparation:CommandKind.ResumeMineralPreparation;
                    yield return new Command("option."+s.Revision.ToString(CultureInfo.InvariantCulture)+".mineral-preparation."+(index++).ToString(CultureInfo.InvariantCulture),
                        actor,s.Revision,kind,attempt.Id);
                }
                if(attempts.Length==0)foreach(var profile in s.MineralPreparationProfiles.OrderBy(x=>x.Id,StringComparer.Ordinal))
                    if(!s.MineralPreparationAttempts.Any(x=>x.ProfileId==profile.Id))
                        yield return new Command("option."+s.Revision.ToString(CultureInfo.InvariantCulture)+".mineral-preparation."+(index++).ToString(CultureInfo.InvariantCulture),
                            actor,s.Revision,CommandKind.StartMineralPreparation,profile.UnitId);
            }
            if(prospectingFixture!=null&&IsProspectingWorker(actor)) {
                var attempt=s.ProspectingAttempts.SingleOrDefault(x=>x.ActorId==actor
                    &&(x.Status==ProspectingAttemptStatus.Working||x.Status==ProspectingAttemptStatus.Paused
                        ||x.Status==ProspectingAttemptStatus.AwaitingCheck));
                if(attempt!=null) {
                    CommandKind kind=attempt.Status==ProspectingAttemptStatus.Working?CommandKind.PauseProspecting:CommandKind.ResumeProspecting;
                    yield return new Command("option."+s.Revision.ToString(CultureInfo.InvariantCulture)+".prospecting."+(index++).ToString(CultureInfo.InvariantCulture),
                        actor,s.Revision,kind,attempt.Id);
                } else foreach(var patch in s.ProspectingPatches.OrderBy(x=>x.Id,StringComparer.Ordinal)) {
                    yield return new Command("option."+s.Revision.ToString(CultureInfo.InvariantCulture)+".prospecting."+(index++).ToString(CultureInfo.InvariantCulture),
                        actor,s.Revision,CommandKind.StartProspecting,patch.Id);
                }
            }
            if(HasMiningAssay&&IsMiningWorker(actor)) {
                var attempts=s.MiningAssayAttempts.Where(x=>x.WorkerId==actor
                    &&(x.Status==MiningAssayStatus.Working||x.Status==MiningAssayStatus.Paused||x.Status==MiningAssayStatus.AwaitingCheck))
                    .OrderBy(x=>x.StartedAt).ThenBy(x=>x.Id,StringComparer.Ordinal).ToArray();
                var destructiveAttempts=s.DestructiveMiningAssayAttempts.Where(x=>x.WorkerId==actor
                    &&(x.Status==MiningAssayStatus.Working||x.Status==MiningAssayStatus.Paused||x.Status==MiningAssayStatus.AwaitingCheck))
                    .OrderBy(x=>x.StartedAt).ThenBy(x=>x.Id,StringComparer.Ordinal).ToArray();
                foreach(var attempt in attempts) {
                    CommandKind kind=attempt.Status==MiningAssayStatus.Working?CommandKind.PauseMiningAssay:CommandKind.ResumeMiningAssay;
                    yield return new Command("option."+s.Revision.ToString(CultureInfo.InvariantCulture)+".mining-assay."+(index++).ToString(CultureInfo.InvariantCulture),
                        actor,s.Revision,kind,attempt.Id);
                }
                foreach(var destructive in destructiveAttempts) {
                    CommandKind kind=destructive.Status==MiningAssayStatus.Working?CommandKind.PauseMiningAssay:CommandKind.ResumeMiningAssay;
                    yield return new Command("option."+s.Revision.ToString(CultureInfo.InvariantCulture)+".mining-assay."+(index++).ToString(CultureInfo.InvariantCulture),
                        actor,s.Revision,kind,destructive.Id);
                    yield return new Command("option."+s.Revision.ToString(CultureInfo.InvariantCulture)+".mining-assay."+(index++).ToString(CultureInfo.InvariantCulture),
                        actor,s.Revision,CommandKind.CancelMiningAssay,destructive.Id);
                }
                if(attempts.Length==0&&destructiveAttempts.Length==0) {
                    foreach(var profile in s.MiningAssayProfiles.OrderBy(x=>x.Id,StringComparer.Ordinal)) {
                        if(s.MiningAssayAttempts.Any(x=>x.ProfileId==profile.Id))continue;
                        yield return new Command("option."+s.Revision.ToString(CultureInfo.InvariantCulture)+".mining-assay."+(index++).ToString(CultureInfo.InvariantCulture),
                            actor,s.Revision,CommandKind.StartMiningAssay,profile.Id);
                    }
                    foreach(var profile in s.DestructiveMiningAssayProfiles.OrderBy(x=>x.Id,StringComparer.Ordinal))
                        yield return new Command("option."+s.Revision.ToString(CultureInfo.InvariantCulture)+".mining-assay."+(index++).ToString(CultureInfo.InvariantCulture),
                            actor,s.Revision,CommandKind.StartMiningAssay,profile.Id);
                }
            }
            foreach (var command in DiscoverFishingTrapControls(s, actor)) yield return command;
            foreach (var command in DiscoverFishingTrapResponsibilityHandoverCommands(s, authority, actor)) yield return command;
            foreach (var command in DiscoverCacheExcavationControls(s, actor)) yield return command;
            foreach (var command in DiscoverContextualInteractions(s, authority, actor)) yield return command;
            foreach (var command in DiscoverManufacturingCommands(s, actor)) yield return command;
        }

        private IEnumerable<Command> DiscoverContextualInteractions(Snapshot s,Authority authority,string actor)
        {
            foreach(var command in DiscoverHuntingTrapCommands(s,actor))yield return command;
            if(!authority.MayUseInventory(actor))yield break;
            foreach(var command in DiscoverSupplyCacheCommands(s,actor))yield return command;
            foreach(var command in DiscoverOrdinaryReceptacleCommands(s,actor))yield return command;
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
            if(c.Kind==CommandKind.HandoverFishingTrapResponsibility)
                return QueryFishingTrapResponsibilityHandover(s,authority,c);
            if (IsHavenCareCommand(c.Kind)) return QueryHavenCareCommand(s, c);
            if(recipe347Fixture!=null&&Recipe347Command(c.Kind)) {
                string failure=AssessRecipe347(s,c,out var order);
                if(failure==null)failure=Recipe347WorkWatchCommandFailure(s,c);
                var costs=new List<CommandCost>();
                if(failure==null&&(c.Kind==CommandKind.StartRecipe347
                    ||c.Kind==CommandKind.ResumeRecipe347&&order.Status==Recipe347OrderStatus.Paused)) {
                    RuleTime duration=Recipe347Subtract(Recipe347NextBookingEnd(s,order),s.RuleClock);
                    if(duration.Denominator==1)costs.Add(new CommandCost("work-seconds",order.Id,duration.Numerator));
                }
                return new CommandQueryResult(true,failure==null,failure??"Available",s.Revision,costs);
            }
            if(recipe347Fixture!=null&&c.Kind==CommandKind.PortionInventory) {
                string failure=ResolveCore(s.Copy(),c);
                return new CommandQueryResult(true,failure==null,failure??"Available",s.Revision,Array.Empty<CommandCost>());
            }
            if(recipe347Fixture!=null&&Recipe347WorkStartCommand(c)) {
                var preview=s.Copy();string failure=ResolveCore(preview,c);
                if(failure==null)failure=Recipe347ProjectedWorkWatchFailure(s,preview,c);
                return new CommandQueryResult(true,failure==null,failure??"Available",s.Revision,Array.Empty<CommandCost>());
            }
            string workWatchFailure=Recipe347WorkWatchCommandFailure(s,c);
            if(workWatchFailure!=null)return new CommandQueryResult(true,false,workWatchFailure,s.Revision,Array.Empty<CommandCost>());
            if(portableStorageFixture!=null&&PortableCommand(c.Kind)) {
                string failure=ResolveCore(s.Copy(),c);
                var costs=failure==null
                    ?s.InventoryCombat?new[]{new CommandCost("interaction","",1)}
                        :new[]{new CommandCost("work-seconds","",1)}
                    :Array.Empty<CommandCost>();
                return new CommandQueryResult(true,failure==null,failure??"Available",s.Revision,costs);
            }
            if (surpriseEntryBinding != null && IsSurpriseEntryQuery(c.Kind)) {
                if (!s.InventoryCombat || s.Encounter?.Id != surpriseEntryBinding.EncounterId)
                    return new CommandQueryResult(false, false, "UnsupportedOperation", s.Revision);
                string failure = ResolveCore(s.Copy(), c);
                var costs = new List<CommandCost>();
                if (failure == null) {
                    if (c.Kind == CommandKind.HandlePortableEquipment) costs.Add(new CommandCost("interaction", "", 1));
                    if (c.Kind != CommandKind.HandlePortableEquipment || Interval(s, c.Actor).Interactions == 1)
                        costs.Add(new CommandCost("action", "", 1));
                }
                return new CommandQueryResult(true, failure == null, failure ?? "Available", s.Revision, costs);
            }
            if (IsTemporaryCampConstructionCommand(c.Kind)) return QueryTemporaryCampConstruction(s,c);
            if (IsExpeditionCampUseCommand(c.Kind)) return QueryExpeditionCampUse(s, c);
            if(c.Kind==CommandKind.AwardCharacterMilestone||c.Kind==CommandKind.AdvanceCharacterLevel) {
                string failure=CharacterAdvancementRules.Assess(s,c);
                return new CommandQueryResult(true,failure==null,failure??"Available",s.Revision);
            }
            if (RouteMappingResultCommand(c.Kind)) return QueryRouteMappingResultCommand(s, c);
            if (RouteMappingWorkCommand(c.Kind)) return QueryRouteMappingWork(s, c);
            if (RouteReconnaissanceCommand(c.Kind)) return QueryRouteReconnaissance(s, c);
            if (RouteTravelCommand(c.Kind)) return QueryRouteTravelCommand(s, c);
            if (c.Kind == CommandKind.Search || c.Kind == CommandKind.CancelExplorationSearch)
                return QueryObservationSearchCommand(s, c);
            if (CacheExcavationCommand(c)) return QueryCacheExcavationControl(s, c);
            if (IsSupplyCacheCommand(c)) return QuerySupplyCacheCommand(s,c);
            if (IsOrdinaryReceptacleCommand(s,c)) return QueryOrdinaryReceptacleCommand(s,c);
            if (IsHuntingTrapCommand(s,c)) return QueryHuntingTrapCommand(s,c);
            if (c.Kind == CommandKind.Interact) return QueryFishingTrapControl(s, c);
            if (c.Kind == CommandKind.ResolveManufacturingQuality) return QueryManufacturingQualityChoice(s, c);
            if (c.Kind == CommandKind.PauseManufacturing || c.Kind == CommandKind.ResumeManufacturing || c.Kind == CommandKind.CancelManufacturing)
                return QueryManufacturingControl(s, c);
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
            if(HarvestPreservationTreatmentCommand(c.Kind)) {
                string failure=AssessHarvestPreservationTreatment(s,c,out _,out _);
                var costs=new List<CommandCost>();
                if(failure==null)costs.Add(new CommandCost("work-seconds","",HarvestPreservationTreatmentValidation.WorkSeconds));
                return new CommandQueryResult(true,failure==null,failure??"Available",s.Revision,costs);
            }
            if(HarvestRequirementWorkCommand(c.Kind)) {
                string failure=AssessHarvestRequirementWork(s,c,out var current,out _);
                var costs=new List<CommandCost>();
                if(failure==null&&c.Kind==CommandKind.StartHarvestRequirementWork) {
                    RuleTime duration=HarvestRequirementDuration(s,c.Target);
                    if(duration.Denominator==1)costs.Add(new CommandCost("work-seconds","",duration.Numerator));
                } else if(failure==null&&c.Kind==CommandKind.ResumeHarvestRequirementWork&&current.Work.Remaining.Denominator==1)
                    costs.Add(new CommandCost("work-seconds",current.Id,current.Work.Remaining.Numerator));
                return new CommandQueryResult(true,failure==null,failure??"Available",s.Revision,costs);
            }
            if(c.Kind==CommandKind.StartMining||c.Kind==CommandKind.PauseMining||c.Kind==CommandKind.ResumeMining) {
                string failure=AssessMiningCommand(s,c,out var facts);var costs=new List<CommandCost>();
                if(failure==null&&c.Kind==CommandKind.StartMining) {
                    costs.Add(new CommandCost("work-seconds","",facts.Duration));
                    costs.AddRange(facts.UnitIds.Select(id=>new CommandCost("finite-source-unit",id,1)));
                } else if(failure==null&&c.Kind==CommandKind.ResumeMining&&facts.Current.Status==MiningAttemptStatus.Paused) {
                    RuleTime remaining=SubtractMiningTime(new RuleTime(facts.Current.DurationSeconds),facts.Current.WorkDone);
                    if(remaining.Denominator==1)costs.Add(new CommandCost("work-seconds","",remaining.Numerator));
                }
                return new CommandQueryResult(true,failure==null,failure??"Available",s.Revision,costs);
            }
            if(c.Kind==CommandKind.StartMineralPreparation||c.Kind==CommandKind.PauseMineralPreparation
                ||c.Kind==CommandKind.ResumeMineralPreparation) {
                string failure=AssessMineralPreparationCommand(s,c,out var facts);var costs=new List<CommandCost>();
                if(failure==null&&c.Kind==CommandKind.StartMineralPreparation) {
                    costs.Add(new CommandCost("work-seconds","",MineralPreparationValidation.WorkSeconds));
                    costs.Add(new CommandCost("whole-mineral-unit",facts.Unit.Id,1));
                } else if(failure==null&&c.Kind==CommandKind.ResumeMineralPreparation
                    &&facts.Current.Status==MineralPreparationStatus.Paused) {
                    RuleTime remaining=SubtractMiningTime(new RuleTime(MineralPreparationValidation.WorkSeconds),facts.Current.WorkDone);
                    if(remaining.Denominator==1)costs.Add(new CommandCost("work-seconds","",remaining.Numerator));
                }
                return new CommandQueryResult(true,failure==null,failure??"Available",s.Revision,costs);
            }
            if(c.Kind==CommandKind.StartProspecting||c.Kind==CommandKind.PauseProspecting
                ||c.Kind==CommandKind.ResumeProspecting||c.Kind==CommandKind.RecordProspectingExposure) {
                string failure=AssessProspectingCommand(s,c,out var facts);var costs=new List<CommandCost>();
                if(failure==null&&c.Kind==CommandKind.StartProspecting)
                    costs.Add(new CommandCost("work-seconds","",ProspectingValidation.WorkSeconds));
                else if(failure==null&&c.Kind==CommandKind.ResumeProspecting&&facts.Current.Status==ProspectingAttemptStatus.Paused
                    &&facts.Current.WorkDone<new RuleTime(ProspectingValidation.WorkSeconds)) {
                    RuleTime remaining=SubtractProspectingTime(new RuleTime(ProspectingValidation.WorkSeconds),facts.Current.WorkDone);
                    if(remaining.Denominator==1)costs.Add(new CommandCost("work-seconds","",remaining.Numerator));
                }
                return new CommandQueryResult(true,failure==null,failure??"Available",s.Revision,costs);
            }
            if(c.Kind==CommandKind.StartMiningAssay||c.Kind==CommandKind.PauseMiningAssay||c.Kind==CommandKind.ResumeMiningAssay
                ||c.Kind==CommandKind.CancelMiningAssay) {
                string failure=AssessMiningAssayCommand(s,c,out var facts);var costs=new List<CommandCost>();
                if(failure==null&&c.Kind==CommandKind.StartMiningAssay)
                    costs.Add(new CommandCost("work-seconds","",MiningAssayValidation.WorkSeconds));
                else if(failure==null&&c.Kind==CommandKind.ResumeMiningAssay) {
                    var current=facts.DestructiveCurrent!=null?(RuleTime?)facts.DestructiveCurrent.WorkDone:facts.Current?.WorkDone;
                    var status=facts.DestructiveCurrent!=null?facts.DestructiveCurrent.Status:facts.Current?.Status;
                    if(status==MiningAssayStatus.Paused&&current.HasValue&&current.Value<new RuleTime(MiningAssayValidation.WorkSeconds)) {
                    RuleTime remaining=SubtractMiningAssayTime(new RuleTime(MiningAssayValidation.WorkSeconds),current.Value);
                    if(remaining.Denominator==1)costs.Add(new CommandCost("work-seconds","",remaining.Numerator));
                    }
                }
                return new CommandQueryResult(true,failure==null,failure??"Available",s.Revision,costs);
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
                string available = s.Reengagement?.Definition.IsApproachCommand(s, c) == true ? "ReengagementApproachAvailable" : "Available";
                return new CommandQueryResult(true, true, available, s.Revision, costs);
            }
            if (c.Kind == CommandKind.SuspendWorldStep || c.Kind == CommandKind.ResumeWorldStep)
            {
                string failure = AssessTraversalControl(s, c, out var edge);
                var costs = new List<CommandCost>();
                if (failure == null && c.Kind == CommandKind.ResumeWorldStep && edge.Running)
                {
                    bool paid = WorldTiming.ForActor(s, c.Actor) != null ? Interval(s, c.Actor).DashPaid : ActivityInterval(s, c.Actor).DashPaid;
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
