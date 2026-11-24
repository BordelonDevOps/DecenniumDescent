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
        private static void AddAdmittedPlanningCases(Dictionary<string,Action> cases,string directory)
        {
            cases.Add("int05_owned_planning_read_proof_and_genuine_restore",()=> {
                var session=ConnectedExpeditionSession.Start();
                var sim=CastingSimulation(session);
                var command=new Command("int05.plan.before-close",ConnectedExpeditionSession.Hero,0,
                    CommandKind.StartNextCharterPlan,TestOnlyNextCharterPlanProfile.VersionId);
                AssertNativeInitialAssessmentV1(sim,command,HavenSaleHost(),"NextCharterPlanningCloseRequired");
                const BindingFlags fields=BindingFlags.Instance|BindingFlags.NonPublic;
                var origin=(VerifiedSimulationOrigin)typeof(Simulation).GetField("verificationOrigin",fields).GetValue(sim);
                var checkpoint=(IVerifiedCommandAssessmentV1)typeof(Simulation).GetField("checkpoint",fields).GetValue(sim);
                var other=CastingSimulation(ConnectedExpeditionSession.Start());
                var foreign=other.Capture();
                Require(checkpoint.AssessFacts(origin,ProbeReadContext(other,foreign),foreign,HavenSaleHost(),command).Status
                    ==NativeAssessmentStatusV1.VerificationUnavailable,"Equal bytes transferred another owner's read proof.");
                var changed=sim.Capture();var context=ProbeReadContext(sim,changed);changed.RandomState^=1;
                Require(checkpoint.AssessFacts(origin,context,changed,HavenSaleHost(),command).Status
                    ==NativeAssessmentStatusV1.VerificationUnavailable,"Altered full canonical state retained planning proof.");
                foreach(var input in QualityWalkthrough().TakeWhile(x=>x.Kind!=CommandKind.StartNextCharterPlan))
                    CommitVialRoute(session,input);
                var plan=QualityWalkthrough().Single(x=>x.Kind==CommandKind.StartNextCharterPlan);
                sim=CastingSimulation(session);
                AssertNativeInitialAssessmentV1(sim,plan,HavenSaleHost());
                var current=sim.Capture();
                Require(checkpoint.AssessFacts(origin,ProbeReadContext(sim,current),current,HavenSaleHost(),plan).Status
                    ==NativeAssessmentStatusV1.VerificationUnavailable,"An earlier checkpoint authorized a later revision.");
                string path=Path.Combine(directory,"int05-planning-before.ddsave");session.Save(path);session.Restore(path);
                AssertNativeInitialAssessmentV1(CastingSimulation(session),plan,HavenSaleHost());
                CommitVialRoute(session,plan);
                CommitVialRoute(session,QualityWalkthrough().Single(x=>x.ExpectedRevision==plan.ExpectedRevision+1));
                path=Path.Combine(directory,"int05-planning-completed.ddsave");session.Save(path);session.Restore(path);
                Require(CastingSimulation(session).Capture().NextCharterPlans.Single().Report!=null,
                    "Planning checks did not preserve the actual work and completed report.");
            });
        }
    }
}
#endif
