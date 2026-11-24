#if DECENNIUM_TEST_ONLY && (UNITY_EDITOR || HEADLESS_TESTS)
using System;
using System.Collections.Generic;
using System.Linq;
using System.IO;
using System.Reflection;
using Decennium.Foundation.Laboratory;

namespace Decennium.Foundation.Tests
{
    public static partial class FoundationCases
    {
        // Protocol probes below are technical infrastructure evidence, not a gameplay profile.
        private sealed class AssessmentProbePolicy : ICommandPolicy, IReadStateProjectionPolicyV1,
            ICommandAssessmentFactsPolicyV1, IVerifiedCommandPolicy, ICommandInventoryClaims
        {
            private readonly TestOnlyPolicy native = new TestOnlyPolicy();
            internal int DirectCalls, VerifiedCalls;
            internal bool RequiresVerification;
            internal Action<Snapshot> DuringRead;
            internal Action DuringClaims;
            public string ContentFingerprint => native.ContentFingerprint;
            public bool TestOnly => true;
            public Snapshot Initial() => native.Initial();
            public string Resolve(Snapshot s, Command c) => native.Resolve(s,c);
            public string ValidateState(Snapshot s) => native.ValidateState(s);
            public IReadStateProjectionV1 CreateReadProjection(ReadStateStampV1 stamp, Snapshot s) => new ProjectionProbe(stamp);
            public bool SupportsAssessment(CommandKind kind) => kind == CommandKind.Interact || kind == CommandKind.Move;
            public bool RequiresVerifiedAssessment(CommandKind kind) => RequiresVerification;
            public IEnumerable<string> RequiredInventoryOwners(Snapshot s, Command c)
            { DuringClaims?.Invoke(); return Array.Empty<string>(); }
            public NativeCommandAssessmentV1 AssessFacts(NativeReadContextV1 context, Snapshot s, Authority a, Command c)
            { DirectCalls++; return Read(context,s); }
            private NativeCommandAssessmentV1 Read(NativeReadContextV1 context, Snapshot s)
            {
                Require(context.IsBoundTo(s), "Assessment did not receive its owning exact snapshot.");
                DuringRead?.Invoke(s);
                return new NativeCommandAssessmentV1(s.Revision, true, true);
            }
            public IVerifiedCommandCheckpoint Seal(VerifiedSimulationOrigin origin) => new ProbeCheckpoint(this,origin);
            private sealed class ProbeCheckpoint : IVerifiedCommandCheckpoint, IVerifiedCommandAssessmentV1
            {
                private readonly AssessmentProbePolicy policy;
                private readonly VerifiedSimulationOrigin owner;
                internal ProbeCheckpoint(AssessmentProbePolicy policy, VerifiedSimulationOrigin owner)
                { this.policy=policy; this.owner=owner; }
                public string VerifyNext(VerifiedSimulationOrigin origin, Snapshot predecessor, Snapshot candidate,
                    CommandReceipt receipt, out IVerifiedCommandCheckpoint successor)
                { successor=null; return "ProtocolProbeDoesNotExecuteVerifiedTransitions"; }
                public NativeCommandAssessmentV1 AssessFacts(VerifiedSimulationOrigin origin, NativeReadContextV1 context,
                    Snapshot s, Authority a, Command c)
                {
                    Require(ReferenceEquals(origin,owner), "Owning verification origin changed.");
                    policy.VerifiedCalls++; return policy.Read(context,s);
                }
            }
        }

        private static void AddAdmittedAssessmentCases(Dictionary<string, Action> cases, string directory)
        {
            cases.Add("int05_native_assessment_authority_retry_and_verified_routing", () => {
                var policy=new AssessmentProbePolicy(); var sim=new Simulation(policy,policy.Initial(),ExecutionProfile.Laboratory);
                var grant=TestOnlyPolicy.Host(); var command=Open(); var before=Bytes(sim);
                var read=sim.AssessCommandFactsV1(grant,command,0);
                Require(read.Admissible && read.InitialEligibility==true && read.CommitFeasibility==true
                    && policy.DirectCalls==1 && read.ProhibitedCallAttempts.All(x=>x==0) && before.SequenceEqual(Bytes(sim)),
                    "Fresh pure native assessment altered state or skipped its policy.");
                Require(sim.AssessCommandFactsV1(grant,command,1).Status==NativeAssessmentStatusV1.StaleObservation
                    && policy.DirectCalls==1,"Observation freshness reached gameplay assessment.");
                var revoked=new Authority(grant.Principal,Array.Empty<string>());
                Require(sim.AssessCommandFactsV1(revoked,command,1).Constraint?.NativeCode=="NotAuthorized",
                    "Observation freshness bypassed current native authority.");
                Require(sim.Execute(grant,command).Outcome==Outcome.Committed,"Legacy execution was changed by extraction.");
                policy.DuringRead=s=>throw new InvalidOperationException("Fresh eligibility must not run on a retry.");
                var committed=Bytes(sim); read=sim.AssessCommandFactsV1(grant,command,1);
                Require(read.Status==NativeAssessmentStatusV1.AlreadyCommitted && read.MatchingReceiptRevision==1
                    && read.InitialEligibility==null && policy.DirectCalls==1 && committed.SequenceEqual(Bytes(sim)),
                    "Exact retry did not preserve original command revision or bypass fresh eligibility.");
                Require(sim.AssessCommandFactsV1(revoked,command,1).Constraint?.NativeCode=="NotAuthorized",
                    "A retained receipt bypassed revoked control.");
                var conflict=new Command(command.Id,command.Actor,0,CommandKind.Move,x:-1);
                Require(sim.AssessCommandFactsV1(grant,conflict,1).Constraint?.NativeCode=="CommandIdConflict"
                    && sim.Execute(grant,conflict).Code=="CommandIdConflict","Conflict extraction changed legacy meaning.");
                var stale=new Command("int05.stale",command.Actor,0,CommandKind.Move,x:-1);
                Require(sim.AssessCommandFactsV1(grant,stale,1).Constraint?.NativeCode=="StaleRevision"
                    && policy.DirectCalls==1,"Original command freshness did not precede new eligibility.");

                var verifiedPolicy=new AssessmentProbePolicy {RequiresVerification=true};
                var verified=new Simulation(verifiedPolicy,verifiedPolicy.Initial(),ExecutionProfile.Laboratory,CommandVerification.VerifiedPrefix);
                Require(verified.AssessCommandFactsV1(grant,command,0).Admissible
                    && verifiedPolicy.VerifiedCalls==1 && verifiedPolicy.DirectCalls==0,"Verified route used an unverified fallback.");
                var missing=new Simulation(verifiedPolicy,verifiedPolicy.Initial(),ExecutionProfile.Laboratory);
                Require(missing.AssessCommandFactsV1(grant,command,0).Status==NativeAssessmentStatusV1.VerificationUnavailable
                    && verifiedPolicy.VerifiedCalls==1 && verifiedPolicy.DirectCalls==0,"Missing owning capability fell back to direct assessment.");
            });

            cases.Add("int05_read_guard_detects_caught_execution_attempts", () => {
                var policy=new AssessmentProbePolicy(); var sim=new Simulation(policy,policy.Initial(),ExecutionProfile.Laboratory);
                var worldPolicy=new TestOnlySharedWorldPolicy(); var world=World(worldPolicy).Capture(); var before=Bytes(sim);
                var attempts=new Dictionary<NativeReadOperationV1,Action> {
                    [NativeReadOperationV1.OwnerReentry]=()=>sim.Capture(),
                    [NativeReadOperationV1.RandomDraw]=()=>DiceStream.Draw(1,20),
                    [NativeReadOperationV1.SnapshotValidation]=()=>new SnapshotCodec().Encode(world),
                    [NativeReadOperationV1.PolicyValidation]=()=>worldPolicy.ValidateState(world),
                    [NativeReadOperationV1.Resolver]=()=>worldPolicy.Resolve(world.Copy(),Open()),
                    [NativeReadOperationV1.HistoryReplay]=()=>InvokeReadForbiddenProbe(worldPolicy,"ReplayReceipt",world,null,null,false),
                    [NativeReadOperationV1.ConditionLifecycle]=()=>ConditionHistory.Restore(world.Conditions[0]),
                    [NativeReadOperationV1.DeadlineAdvancement]=()=>InvokeReadForbiddenProbe(worldPolicy,"AdvanceTo",world,world.RuleClock,false,null,null),
                    [NativeReadOperationV1.ResourceReservation]=()=>world.Work.Reserve("int05.probe",Array.Empty<WorkerInterval>(),Array.Empty<ResourceReservation>())
                };
                foreach(var pair in attempts) {
                    policy.DuringRead=s=> { try { pair.Value(); } catch(InvalidOperationException) { } };
                    var result=sim.AssessCommandFactsV1(TestOnlyPolicy.Host(),Open(),0);
                    Require(result.Status==NativeAssessmentStatusV1.ProjectionUnavailable
                        &&result.ProhibitedCallAttempts[(int)pair.Key]>0 && before.SequenceEqual(Bytes(sim)),
                        "A caught forbidden read operation was accepted: "+pair.Key);
                }
                policy.DuringRead=null;
                policy.DuringClaims=()=>DiceStream.Draw(1,6);
                var caught=sim.AssessCommandFactsV1(TestOnlyPolicy.Host(),Open(),0);
                Require(caught.Status==NativeAssessmentStatusV1.ProjectionUnavailable
                    &&caught.ProhibitedCallAttempts[(int)NativeReadOperationV1.RandomDraw]==1,
                    "Inventory-claim exception conversion hid a forbidden call.");
                policy.DuringClaims=null;
                foreach(var entry in new Action[] {
                    ()=>sim.QueryCommand(TestOnlyPolicy.Host(),Open()),
                    ()=>sim.AssessCommandAdmission(TestOnlyPolicy.Host(),Open()),
                    ()=>sim.DiscoverCommands(TestOnlyPolicy.Host(),TestOnlyPolicy.ActorId),
                    ()=>sim.ObserveExplorationSearch(TestOnlyPolicy.Host(),"missing"),
                    ()=>sim.ObserveExplorationHide(TestOnlyPolicy.Host(),"missing"),
                    ()=>sim.AssessCommandFactsV1(TestOnlyPolicy.Host(),Open(),0)
                }) {
                    policy.DuringRead=s=> { try { entry(); } catch(InvalidOperationException) { } };
                    var result=sim.AssessCommandFactsV1(TestOnlyPolicy.Host(),Open(),0);
                    Require(result.Status==NativeAssessmentStatusV1.ProjectionUnavailable
                        &&result.ProhibitedCallAttempts[(int)NativeReadOperationV1.OwnerReentry]==1,
                        "A nested public owner entry escaped the read boundary.");
                }
                foreach(var error in new Exception[] {new NotSupportedException("derived"),new NullReferenceException("derived")}) {
                    policy.DuringRead=s=>throw error;
                    Require(sim.AssessCommandFactsV1(TestOnlyPolicy.Host(),Open(),0).Status==NativeAssessmentStatusV1.ProjectionUnavailable,
                        "A derived assessment exception escaped its technical result.");
                }
                policy.DuringRead=null;
                Require(sim.AssessCommandFactsV1(TestOnlyPolicy.Host(),Open(),0).Admissible
                    &&sim.Execute(TestOnlyPolicy.Host(),Open()).Outcome==Outcome.Committed,
                    "Read guard leaked into a subsequent read or legacy execution.");
            });

            cases.Add("int05_genuine_concentration_assessment_execution_restore", () => {
                var session=CastingFirstOwnTurn(); const string actor=ClericRpProfile.Actor;
                CommitVialRoute(session,new Command("int05.concentration.cast",actor,ShortRestCapture(session).Revision,
                    CommandKind.CastKnownSpell,actor,spellCast:new SpellCastRequest("sanctuary",SpellCastingProfile.FocusId,true)));
                var sim=CastingSimulation(session); var state=sim.Capture();
                var effect=state.SpellEffects.Single(x=>x.Present&&x.RequiresConcentration);
                var command=new Command("int05.concentration.end",actor,state.Revision,CommandKind.EndSpellConcentration,effect.Id);
                var before=Bytes(sim); var grant=CastingAuthority();
                for(int i=0;i<3;i++) {
                    var assessment=sim.AssessCommandFactsV1(grant,command,state.Revision);
                    Require(assessment.Admissible && assessment.InitialEligibility==true && assessment.CommitFeasibility==null
                        && assessment.ProhibitedCallAttempts.All(x=>x==0)
                        && before.SequenceEqual(Bytes(sim)),"Concentration query consumed or changed genuine gameplay.");
                }
                string save=Path.Combine(directory,"int05-concentration-before.ddsave"); session.Save(save); session.Restore(save);
                sim=CastingSimulation(session);
                Require(before.SequenceEqual(Bytes(sim)) && sim.AssessCommandFactsV1(grant,command,state.Revision).Admissible,
                    "Strict restore changed the concentration assessment.");
                CommitVialRoute(session,command); var ended=ShortRestCapture(session); sim=CastingSimulation(session);
                Require(!ended.SpellEffects.Single(x=>x.Id==effect.Id).Present && ended.RandomState==state.RandomState
                    && ended.RuleClock==state.RuleClock && ended.Revision==state.Revision+1,"Actual concentration ending changed its native cost or outcome.");
                var retry=sim.AssessCommandFactsV1(grant,command,ended.Revision);
                Require(retry.Status==NativeAssessmentStatusV1.AlreadyCommitted && retry.MatchingReceiptRevision==ended.Revision,
                    "A genuine ended effect could not be recognized as an exact retry.");
                var absent=new Command("int05.concentration.absent",actor,ended.Revision,CommandKind.EndSpellConcentration,effect.Id);
                var denied=sim.AssessCommandFactsV1(grant,absent,ended.Revision);
                Require(!denied.Admissible && denied.Constraint?.NativeCode=="ConcentrationUnavailable"
                    && denied.Constraint.SourceLine==364 && denied.ProhibitedCallAttempts.All(x=>x==0)
                    && sim.Execute(grant,absent).Code==denied.Constraint.NativeCode,
                    "Fresh concentration denial lacks its shared native origin or disagrees with execution.");
                string after=Path.Combine(directory,"int05-concentration-after.ddsave");session.Save(after);
                var bytes=Bytes(sim);session.Restore(after);
                Require(bytes.SequenceEqual(Bytes(CastingSimulation(session))),"Concentration result failed authenticated replay/restore.");
            });
        }

        // Labelled private-entry instrumentation only; this is not a genuine gameplay producer.
        private static void InvokeReadForbiddenProbe(TestOnlySharedWorldPolicy policy, string name, params object[] args)
        {
            try { typeof(TestOnlySharedWorldPolicy).GetMethod(name,BindingFlags.Instance|BindingFlags.NonPublic).Invoke(policy,args); }
            catch(TargetInvocationException ex) { throw ex.InnerException; }
        }
    }
}
#endif
