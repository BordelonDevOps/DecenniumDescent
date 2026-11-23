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
