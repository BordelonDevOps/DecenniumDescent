#if DECENNIUM_TEST_ONLY && (UNITY_EDITOR || DEVELOPMENT_BUILD || HEADLESS_TESTS)
using System;
using System.Collections.Generic;
using System.Linq;

namespace Decennium.Foundation.Laboratory
{
    public sealed partial class ConnectedExpeditionSession
    {
        private static bool WorkControlSelected(Snapshot state)
            => ConnectedWorkControlProfile.SelectedFingerprint(state.ContentFingerprint);

        private static bool WorkControlCommand(CommandKind kind)
            => TestOnlyFillingPolicy.IsWaterFillCommand(kind)
                || kind == CommandKind.StartMining || kind == CommandKind.PauseMining || kind == CommandKind.ResumeMining
                || kind == CommandKind.StartFormulaResearch || kind == CommandKind.PauseFormulaWork
                || kind == CommandKind.ResumeFormulaWork || kind == CommandKind.CancelFormulaWork
                || kind == CommandKind.StartManufacturing || kind == CommandKind.PauseManufacturing
                || kind == CommandKind.ResumeManufacturing || kind == CommandKind.CancelManufacturing
                || kind == CommandKind.ResolveManufacturingQuality;

        public CommandQueryResult QueryCommand(ExpeditionSeat seat, Command command)
        {
            lock (gate) {
                var state = simulation.Capture();
                if (!WorkControlSelected(state)) return new CommandQueryResult(false, false, "UnsupportedOperation", state.Revision);
                return QueryCastingCommand(seat, command);
            }
        }

        public IReadOnlyList<CommandOption> DiscoverCommands(ExpeditionSeat seat, string actor)
        {
            lock (gate) {
                if (!WorkControlSelected(simulation.Capture())) return Array.AsReadOnly(Array.Empty<CommandOption>());
                return DiscoverCastingCommands(seat, actor);
            }
        }

        private IReadOnlyList<CommandOption> DiscoverWorkControlCommands(Snapshot state, ExpeditionSeat seat, string actor, Authority grant)
        {
            var commands = policy.DiscoverCommands(state.Copy(), grant, actor)
                .Where(c => !WorkControlCommand(c.Kind) || c.Kind == CommandKind.StartFormulaResearch
                    || c.Kind == CommandKind.StartManufacturing || c.Kind == CommandKind.ResolveManufacturingQuality)
                .Concat(WorkControlCandidates(state, actor, grant));
            return Array.AsReadOnly(commands.Where(c => ExposedCommand(state, seat, c.Kind)
                && ExposedPayload(state, c) && KnownTarget(state, seat, c))
                .Select(c => new CommandOption(c, simulation.QueryCommand(SeatCommandGrant(state, seat, c), c)))
                .Where(x => x.Query.Supported).ToArray());
        }

        private static IEnumerable<ExpeditionFillParameters> FillParameters(Snapshot state, string actor, Authority grant)
        {
            foreach(var item in state.InventoryLots.Where(x => x.Nutrition == NutritionKind.WaterPints && grant.MayUseInventory(x.OwnerId))
                .OrderBy(x => x.LotId, StringComparer.Ordinal)) {
                var source = state.Work.Lots.Single(x => x.Id == item.LotId);
                var container = state.Vessels.SingleOrDefault(x => x.Id == source.LocationId);
                if(source.UnitId != TestOnlyInventoryPolicy.WaterUnit || !WaterFilling.Accessible(state, actor, source)
                    || container != null && !grant.MayUseInventory(container.OwnerId))continue;
                foreach(var destination in state.Vessels.Where(x => grant.MayUseInventory(x.OwnerId)
                    && WaterFilling.Accessible(state, actor, x) && x.Id != container?.Id).OrderBy(x => x.Id, StringComparer.Ordinal))
                    yield return new ExpeditionFillParameters(source.Id, destination.Id, source.UnitId,
                        state.Work.AvailableAmount(source.Id), WaterFilling.FreeCapacity(state, destination.Id));
            }
        }

        private static ExpeditionMiningParameters MiningParameters(Snapshot state, Authority grant)
        {
            var site = ProjectMiningSite(state, grant);
            return site?.ObservedLocally == true ? new ExpeditionMiningParameters(site) : null;
        }

        private static IEnumerable<Command> WorkControlCandidates(Snapshot state, string actor, Authority grant)
        {
            int index = 0;
            Command Candidate(CommandKind kind, string target, InventoryRequest inventory = null, MiningSelectionRequest mining = null)
            {
                string id;
                do { id = "option.work-control." + state.Revision.ToString(System.Globalization.CultureInfo.InvariantCulture)
                    + "." + Array.FindIndex(state.Actors, x => x.Id == actor).ToString(System.Globalization.CultureInfo.InvariantCulture)
                    + "." + (index++).ToString(System.Globalization.CultureInfo.InvariantCulture); }
                while(state.Receipts.Any(x => x.Principal == grant.Principal && x.Id == id));
                return new Command(id, actor, state.Revision, kind, target, inventory: inventory, miningSelection: mining);
            }
            foreach(var pair in FillParameters(state, actor, grant))
                foreach(var amount in pair.ExampleAmounts)
                    yield return Candidate(CommandKind.StartWaterFill, pair.SourceId, new InventoryRequest(amount, pair.DestinationId));
            // Visibility filtering precedes exposing categories, unit IDs or native denial details.
            var mining = MiningParameters(state, grant);
            if(mining != null && state.MiningAttempts.Length == 0) {
                var sets = mining.CategoryIds.Select(x => new[] { x }).ToList();
                if(mining.CategoryIds.Count > 1)sets.Add(mining.CategoryIds.ToArray());
                foreach(var set in sets)
                    foreach(var ability in mining.Abilities)
                        foreach(bool hurry in mining.HurriedChoices)
                            yield return Candidate(CommandKind.StartMining, mining.DepositId,
                                mining: new MiningSelectionRequest(mining.VersionId, set, ability, hurry));
            }
            foreach(var job in state.WaterFills.Where(x => x.WorkerId == actor && x.Pending).OrderBy(x => x.Id, StringComparer.Ordinal)) {
                yield return Candidate(job.Status == WaterFillStatus.Working ? CommandKind.PauseWaterFill : CommandKind.ResumeWaterFill, job.Id);
                yield return Candidate(CommandKind.CancelWaterFill, job.Id);
            }
            foreach(var job in state.MiningAttempts.Where(x => x.WorkerId == actor).OrderBy(x => x.Id, StringComparer.Ordinal)) {
                if(job.Status == MiningAttemptStatus.Working)yield return Candidate(CommandKind.PauseMining, job.Id);
                else if(job.Status == MiningAttemptStatus.Paused || job.Status == MiningAttemptStatus.AwaitingCheck)
                    yield return Candidate(CommandKind.ResumeMining, job.Id);
            }
            foreach(var job in state.FormulaWork.Where(x => x.WorkerId == actor && x.Kind == FormulaWorkKind.Research)
                .OrderBy(x => x.Id, StringComparer.Ordinal)) {
                if(job.Status != FormulaWorkStatus.Working && job.Status != FormulaWorkStatus.Paused && job.Status != FormulaWorkStatus.AwaitingCheck)continue;
                yield return Candidate(job.Status == FormulaWorkStatus.Working ? CommandKind.PauseFormulaWork : CommandKind.ResumeFormulaWork, job.Id);
                yield return Candidate(CommandKind.CancelFormulaWork, job.Id);
            }
            foreach(var job in state.ManufacturingOrders.Where(x => x.WorkerId == actor && x.RecipeId == Recipe)
                .OrderBy(x => x.Id, StringComparer.Ordinal)) {
                if(job.Status != ManufacturingStatus.Working && job.Status != ManufacturingStatus.Paused && job.Status != ManufacturingStatus.AwaitingCheck)continue;
                yield return Candidate(job.Status == ManufacturingStatus.Working ? CommandKind.PauseManufacturing : CommandKind.ResumeManufacturing, job.Id);
                yield return Candidate(CommandKind.CancelManufacturing, job.Id);
            }
        }

        public ExpeditionWorkObservation ObserveWork(ExpeditionSeat seat, string actor)
        {
            lock(gate) {
                var state = simulation.Capture(); var grant = SeatGrant(seat);
                if(!WorkControlSelected(state) || grant == null || !grant.Controls(actor))
                    return new ExpeditionWorkObservation(false, state.Revision, "", Array.Empty<ExpeditionControlledWorkView>(),
                        Array.Empty<ExpeditionFillParameters>(), null);
                var options = DiscoverWorkControlCommands(state, seat, actor, grant);
                var jobs = new List<ExpeditionControlledWorkView>();
                ExpeditionControlledWorkView Project(string id, string kind, string status, RuleTime started,
                    RuleTime labor, RuleTime retained, RuleTime required, RuleTime remaining, string stage = "",
                    ActiveWorkProgress progress = null, RuleTime? committed = null, string vessel = "",
                    RuleQuantity? capacity = null, bool opening = false)
                {
                    var claims = from claim in state.Work.Reservations
                        where claim.JobId == id
                        join item in state.InventoryLots on claim.LotId equals item.LotId
                        where grant.MayUseInventory(item.OwnerId)
                        join lot in state.Work.Lots on claim.LotId equals lot.Id
                        select new ExpeditionWorkClaimView(claim, lot, item.OwnerId);
                    return new ExpeditionControlledWorkView(id, actor, kind, status, started, labor, retained, required, remaining,
                        stage, progress, committed, vessel, capacity, opening, claims,
                        state.Work.WorkerIntervals.Where(x => x.JobId == id && x.WorkerId == actor)
                            .Select(x => new ExpeditionWorkBookingView(x, state.RuleClock)),
                        options.Where(x => WorkControlCommand(x.Command.Kind) && x.Command.Target == id));
                }
                foreach(var job in state.WaterFills.Where(x => x.WorkerId == actor)) {
                    var vessel = state.Vessels.Single(x => x.Id == job.DestinationId);
                    bool visible = grant.MayUseInventory(vessel.OwnerId);
                    jobs.Add(Project(job.Id, "WaterFill", job.Status.ToString(), job.StartedAt, job.Progress, job.Progress,
                        new RuleTime(60), CampGreens.Subtract(new RuleTime(60), job.Progress), vessel: visible ? vessel.Id : "",
                        capacity: visible ? (job.Pending ? job.Amount : default(RuleQuantity)) : (RuleQuantity?)null,
                        opening: visible && job.Status == WaterFillStatus.Working));
                }
                foreach(var job in state.MiningAttempts.Where(x => x.WorkerId == actor))
                    jobs.Add(Project(job.Id, "Mining", job.Status.ToString(), job.StartedAt, job.WorkDone, job.WorkDone,
                        new RuleTime(job.DurationSeconds), CampGreens.Subtract(new RuleTime(job.DurationSeconds), job.WorkDone),
                        MiningExtractionRules.Stage(job).ToString(), committed: job.CommittedAt));
                foreach(var job in state.FormulaWork.Where(x => x.WorkerId == actor && x.Kind == FormulaWorkKind.Research))
                    jobs.Add(Project(job.Id, "Research", job.Status.ToString(), job.StartedAt, job.Work.Labor, job.Work.Retained,
                        job.Work.Required, job.Work.Remaining, progress: job.Work));
                foreach(var job in state.ManufacturingOrders.Where(x => x.WorkerId == actor && x.RecipeId == Recipe))
                    jobs.Add(Project(job.Id, "Manufacturing", job.Status.ToString(), job.StartedAt, job.Work.Labor, job.Work.Retained,
                        job.Work.Required, job.Work.Remaining, progress: job.Work));
                return new ExpeditionWorkObservation(true, state.Revision, actor, jobs, FillParameters(state, actor, grant), MiningParameters(state, grant));
            }
        }

        private static bool KnownWorkControlTarget(Snapshot state, ExpeditionSeat seat, Command command)
        {
            if (seat != ExpeditionSeat.Player || !Party.Contains(command.Actor)) return false;
            string actor = command.Actor, target = command.Target;
            switch (command.Kind) {
                case CommandKind.StartWaterFill:
                    var source = state.Work.Lots.SingleOrDefault(x => x.Id == target);
                    var item = state.InventoryLots.SingleOrDefault(x => x.LotId == target);
                    var vessel = state.Vessels.SingleOrDefault(x => x.Id == command.Inventory?.Destination);
                    return source != null && item != null && vessel != null && Party.Contains(item.OwnerId)
                        && Party.Contains(vessel.OwnerId) && WaterFilling.Accessible(state, actor, source);
                case CommandKind.PauseWaterFill:
                case CommandKind.ResumeWaterFill:
                case CommandKind.CancelWaterFill:
                    return state.WaterFills.Any(x => x.Id == target && x.WorkerId == actor);
                case CommandKind.StartMining:
                    var site = ProjectMiningSite(state, PlayerGrant);
                    return site?.ObservedLocally == true && target == site.DepositId;
                case CommandKind.PauseMining:
                case CommandKind.ResumeMining:
                    return state.MiningAttempts.Any(x => x.Id == target && x.WorkerId == actor);
                case CommandKind.StartFormulaResearch:
                    return actor == Companion && target == ResearchSource;
                case CommandKind.PauseFormulaWork:
                case CommandKind.ResumeFormulaWork:
                case CommandKind.CancelFormulaWork:
                    return state.FormulaWork.Any(x => x.Id == target && x.WorkerId == actor && x.Kind == FormulaWorkKind.Research);
                case CommandKind.StartManufacturing:
                    return actor == Companion && target == Recipe;
                case CommandKind.PauseManufacturing:
                case CommandKind.ResumeManufacturing:
                case CommandKind.CancelManufacturing:
                case CommandKind.ResolveManufacturingQuality:
                    return state.ManufacturingOrders.Any(x => x.Id == target && x.WorkerId == actor && x.RecipeId == Recipe);
                default:
                    return false;
            }
        }
    }
}
#endif
