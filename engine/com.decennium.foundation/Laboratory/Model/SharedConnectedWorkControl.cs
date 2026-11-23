#if DECENNIUM_TEST_ONLY && (UNITY_EDITOR || DEVELOPMENT_BUILD || HEADLESS_TESTS)
using System;

namespace Decennium.Foundation.Laboratory
{
    public sealed partial class TestOnlySharedWorldPolicy
    {
        private bool connectedWorkControl;

        private CommandQueryResult QueryConnectedWaterFill(Snapshot state, Command command)
        {
            // Fill commands reach only guards and the pure assessment in this resolver path.
            // Tactical assessment also prevents any pending-response gate from committing a choice.
            string failure = ResolveCore(state, command, assessTactical: true, assessFilling: true);
            var costs = new System.Collections.Generic.List<CommandCost>();
            if (failure == null && command.Kind == CommandKind.StartWaterFill)
                costs.Add(new CommandCost("work-seconds", "", 60));
            return new CommandQueryResult(true, failure == null, failure ?? "Available", state.Revision, costs);
        }


        internal TestOnlySharedWorldPolicy EnableConnectedWorkControl()
        {
            if (initializationStarted || connectedWorkControl || ordinaryMagicDeclaration == null
                || ContentFingerprint != OrdinaryMagicProfile.BindFingerprint(ordinaryMagicDeclaration.PredecessorFingerprint))
                throw new InvalidOperationException("Select connected work control once on a fresh ordinary-magic expedition.");
            ContentFingerprint = ConnectedWorkControlProfile.BindFingerprint(ContentFingerprint);
            connectedWorkControl = true;
            return this;
        }
    }
}
#endif
