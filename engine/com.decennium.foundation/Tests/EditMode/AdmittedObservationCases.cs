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
        private static void AssertObservationInitialV1(Simulation sim, Command command, string failure = null)
            => AssertNativeInitialAssessmentV1(sim,command,TestOnlySharedWorldPolicy.Host(),failure);

        private static void AssertNativeInitialAssessmentV1(Simulation sim, Command command, Authority authority, string failure = null)
        {
            var before = Bytes(sim);
            for (int i=0; i<3; i++) {
                var read=sim.AssessCommandFactsV1(authority,command,sim.Capture().Revision);
                Require(read.Supported && read.Admissible==(failure==null) && read.InitialEligibility==(failure==null)
                    && read.CommitFeasibility==null && read.Constraint?.NativeCode==failure
                    && read.ProhibitedCallAttempts.All(x=>x==0) && before.SequenceEqual(Bytes(sim)),
                    "Initial read disagreed, used execution machinery, or changed state: "+command.Kind+"/"+failure+"/"+read.Status+"/"+read.Constraint?.NativeCode);
            }
        }

        private static void AddAdmittedObservationCases(Dictionary<string,Action> cases,string directory)
        {
            cases.Add("int05_observation_genuine_initial_reads_cancel_restore_and_retry",()=> {
                var policy=ConnectedObservationPolicy();
                var sim=ConnectedObservationReady();
                var hide=ExplorationHideCommand(sim,"int05.hide.begin");
                AssertObservationInitialV1(sim,hide);
                WorldCommit(sim,hide);
                var pending=Bytes(sim);
                File.WriteAllBytes(Path.Combine(directory,"int05-hide-pending.ddsave"),pending);
                sim=new Simulation(policy,new SnapshotCodec().Decode(pending),ExecutionProfile.Laboratory);
                var cancel=CancelHideCommand(sim);
                AssertObservationInitialV1(sim,cancel);
                WorldCommit(sim,cancel);
                AssertObservationInitialV1(sim,new Command("int05.hide.no-pending",cancel.Actor,sim.Capture().Revision,
                    CommandKind.CancelExplorationHide,cancel.Target),"NoPendingOrdinaryHide");
                var after=Bytes(sim);
                var retry=sim.AssessCommandFactsV1(TestOnlySharedWorldPolicy.Host(),cancel,sim.Capture().Revision);
                Require(retry.Status==NativeAssessmentStatusV1.AlreadyCommitted && after.SequenceEqual(Bytes(sim)),
                    "Observation exact retry required new eligibility or changed state.");

                sim=ConnectedObservationReady();
                var search=ExplorationSearchCommand(sim,id:"int05.search.begin");
                AssertObservationInitialV1(sim,search);
                WorldCommit(sim,search);
                pending=Bytes(sim);File.WriteAllBytes(Path.Combine(directory,"int05-search-pending.ddsave"),pending);
                sim=new Simulation(ConnectedObservationPolicy(),new SnapshotCodec().Decode(pending),ExecutionProfile.Laboratory);
                var cancelSearch=SearchCancellation(sim);
                AssertObservationInitialV1(sim,cancelSearch);
                WorldCommit(sim,cancelSearch);
                AssertObservationInitialV1(sim,new Command("int05.search.no-pending",cancelSearch.Actor,sim.Capture().Revision,
                    CommandKind.CancelExplorationSearch,cancelSearch.Target),"NoPendingOrdinarySearch");
                File.WriteAllBytes(Path.Combine(directory,"int05-search-cancelled.ddsave"),Bytes(sim));

                // Exact prior native fixture; no connected-profile reachability claim.
                sim=World(ExplorationSearchPolicy(enabled:false));
                var absent=IC(sim,CommandKind.CancelExplorationHide);
                AssertObservationInitialV1(sim,absent,"OrdinaryHideUnavailable");
                Require(sim.Execute(TestOnlySharedWorldPolicy.Host(),absent).Code=="OrdinaryHideUnavailable",
                    "Missing Hide profile lost its early cancellation denial.");
                foreach(var kind in new[]{CommandKind.CancelExplorationSearch,CommandKind.StartMining,
                    CommandKind.PauseMining,CommandKind.ResumeMining}) {
                    var request=IC(sim,kind);
                    AssertObservationInitialV1(sim,request,"SharedCommandNotImplemented");
                    RejectUnchanged(sim,TestOnlySharedWorldPolicy.Host(),request,"SharedCommandNotImplemented");
                }
            });
        }
    }
}
#endif
