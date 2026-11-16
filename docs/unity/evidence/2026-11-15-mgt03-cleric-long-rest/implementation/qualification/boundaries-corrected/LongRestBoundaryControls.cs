using System;
using System.IO;
using System.Linq;
using System.Reflection;
using System.Collections.Generic;
using System.Text.Json;
using System.Text.Json.Serialization.Metadata;
using Decennium.Foundation;
using Decennium.Foundation.Laboratory;
public static class LongRestBoundaryControls {
    const string Actor=ClericRpProfile.Actor,Hero=ConnectedExpeditionSession.Hero;
    static void Need(bool value,string text){if(!value)throw new Exception(text);}
    static Simulation Sim(ConnectedExpeditionSession s)=>(Simulation)s.GetType().GetField("simulation",BindingFlags.NonPublic|BindingFlags.Instance).GetValue(s);
    static TestOnlySharedWorldPolicy Policy(ConnectedExpeditionSession s)=>(TestOnlySharedWorldPolicy)s.GetType().GetField("policy",BindingFlags.NonPublic|BindingFlags.Instance).GetValue(s);
    static Snapshot State(ConnectedExpeditionSession s)=>Sim(s).Capture();
    static ConnectedExpeditionSession New(string path){var s=ConnectedExpeditionSession.StartWithClericLongRest(ClericInitialSelection.AuthoredExample(),ClericRepertoireSelection.AuthoredExample(),ClericMilestoneDeclaration.AuthoredExample());s.Restore(path);return s;}
    static void Commit(ConnectedExpeditionSession s,Command c){var r=c.Kind==CommandKind.AdvanceClock?s.SubmitSessionCommand(c):s.Submit(ExpeditionSeat.Player,c);Need(r.Response==ExpeditionResponse.Committed,"Control failed "+c.Kind+": "+r.Response);}
    public static string Run(string checkpoints,string output){
        var reports=new List<object>();var codec=new SnapshotCodec();
        var grant=new Authority("TEST_ONLY.host",new[]{Hero,Actor},inventoryOwners:new[]{Hero,Actor});
        var ready=New(Path.Combine(checkpoints,"long-rest-interrupted.ddsave"));var original=codec.Encode(State(ready));
        // These deliberately altered candidates exercise the actual policy methods, not a supported save or genuine encounter.
        foreach(string kind in new[]{"mode","position","body","work"}){
            var candidate=State(ready);string expected;
            if(kind=="mode"){candidate.InventoryCombat=true;expected="LongRestRequiresSettledEncounterClosure";}
            else if(kind=="position"){candidate.Actors.Single(x=>x.Id==Actor).X++;expected="LongRestRequiresStationaryBerthAccess";}
            else if(kind=="body"){
                var before=candidate.Lives.Single(x=>x.ActorId==Actor);
                typeof(TestOnlyClubAttackPolicy).GetMethod("ApplyLife",BindingFlags.NonPublic|BindingFlags.Static)
                    .Invoke(null,new object[]{candidate,before,new LifeState(before.MaximumHp,0)});
                expected="LongRestBodyUnsupported";
            }else{
                candidate.Work=candidate.Work.Reserve("detached.long-rest.work",new[]{new WorkerInterval("detached.long-rest.worker","detached.long-rest.work",Actor,candidate.RuleClock,candidate.RuleClock.AddSeconds(60))},Array.Empty<ResourceReservation>());
                expected="LongRestActorOccupied";
            }
            var resolver=new DefaultJsonTypeInfoResolver();
            resolver.Modifiers.Add(info=>{if(info.Type==typeof(ResourceLot)||info.Type==typeof(ResourceReservation)){
                var legacy=info.Properties.Single(x=>x.Name=="Quantity");info.Properties.Remove(legacy);
            }});
            var jsonOptions=new JsonSerializerOptions{IncludeFields=true,TypeInfoResolver=resolver};string beforeJson=JsonSerializer.Serialize(candidate,jsonOptions);
            var command=new Command("detached.long-rest.admission."+kind,Actor,candidate.Revision,CommandKind.BeginLongRest,ClericLongRestProfile.SiteId);
            var query=Policy(ready).QueryCommand(candidate,grant,command);string resolved=Policy(ready).Resolve(candidate,command);
            Need(!query.Admissible&&query.Code==expected&&resolved==expected&&beforeJson==JsonSerializer.Serialize(candidate,jsonOptions)
                &&original.SequenceEqual(codec.Encode(State(ready))),"Detached admission changed state or disagreed: "+kind+" "+query.Code+" / "+resolved);
            File.WriteAllText(Path.Combine(output,"detached-admission-"+kind+"-before.json"),beforeJson);
            File.WriteAllText(Path.Combine(output,"detached-admission-"+kind+"-after.json"),JsonSerializer.Serialize(candidate,jsonOptions));
            reports.Add(new{kind,scope="Detached setup; actual policy query and resolver; no supported mutated save or genuine external event claimed",expected,unchanged=true});
        }
        foreach(string name in new[]{"long-rest-first-funded.ddsave","long-rest-cadence-172800.ddsave","long-rest-strain-five.ddsave","long-rest-terminal-provisioning.ddsave"}){
            var s=New(Path.Combine(checkpoints,name));var actual=State(s);var before=codec.Encode(actual);
            Need(actual.ExpeditionStrainRecoveryOffers.Length==0&&actual.ExpeditionStrainRemovals.Length==0
                &&actual.DailyProvisioningSettlements.All(x=>x.HasShortfall)
                &&actual.ExpeditionStrainGains.Where(x=>x.CauseKind==ExpeditionStrainCauseKind.RestDebtDeadline||x.CauseKind==ExpeditionStrainCauseKind.RestMissedWhileIndebted).All(x=>x.OrdinaryRemovable==null),
                "Genuine provisioning or unresolved Rest Debt was converted into free Strain recovery.");
            var c=new Command("boundary.unoffered."+actual.Revision,Actor,actual.Revision,CommandKind.ResolveExpeditionStrainRecovery,"TEST_ONLY.unoffered-point");
            var query=Sim(s).QueryCommand(grant,c);var result=Sim(s).Execute(grant,c);
            Need(!query.Admissible&&result.Outcome==Outcome.Rejected&&before.SequenceEqual(codec.Encode(State(s))),"Unoffered point changed genuine state.");
            File.WriteAllBytes(Path.Combine(output,name+"-denial-before.ddsave"),before);File.WriteAllBytes(Path.Combine(output,name+"-denial-after.ddsave"),codec.Encode(State(s)));
            if(name=="long-rest-terminal-provisioning.ddsave"){
                c=new Command("boundary.dead",Actor,actual.Revision,CommandKind.BeginLongRest,ClericLongRestProfile.SiteId);
                query=Sim(s).QueryCommand(grant,c);result=Sim(s).Execute(grant,c);
                Need(query.Code=="LongRestBodyUnsupported"&&result.Code==query.Code&&before.SequenceEqual(codec.Encode(State(s))),"Actually dead participant was admitted or changed state.");
            }
            reports.Add(new{name,scope="Genuine checkpoint and actual simulation command rejection",noOffer=true,noRemoval=true,restDebtClassificationUnresolved=true,unchanged=true});
        }
        var pending=New(Path.Combine(checkpoints,"long-rest-pending.ddsave"));var pendingBytes=codec.Encode(State(pending));
        string primary=Path.Combine(output,"backup-recovery.ddsave");pending.Save(primary);
        var funded=New(Path.Combine(checkpoints,"long-rest-first-funded.ddsave"));funded.Save(primary);
        Need(pendingBytes.SequenceEqual(File.ReadAllBytes(primary+".bak")),"Backup did not preserve genuine pending bytes.");
        byte[] corrupt={0x42,0x41,0x44};File.WriteAllBytes(primary,corrupt);string displaced=funded.RecoverBackup(primary);
        Need(pendingBytes.SequenceEqual(codec.Encode(State(funded)))&&pendingBytes.SequenceEqual(File.ReadAllBytes(primary))
            &&pendingBytes.SequenceEqual(File.ReadAllBytes(primary+".bak"))&&corrupt.SequenceEqual(File.ReadAllBytes(displaced)),"Explicit backup recovery did not preserve exact inputs.");
        var at=State(funded);var due=ClericLongRestProfile.Active(at).DueAt;
        // A genuine advance crosses completion with one second still to process. No offer exists because actual provisions are insufficient.
        var delta=new RuleTime(checked(due.Numerator*at.RuleClock.Denominator-at.RuleClock.Numerator*due.Denominator),checked(due.Denominator*at.RuleClock.Denominator)).AddSeconds(1);
        Commit(funded,new Command("boundary.rest.remaining-time",Hero,at.Revision,CommandKind.AdvanceClock,"",checked((int)delta.Numerator),checked((int)delta.Denominator)));
        var finished=State(funded);Need(finished.RuleClock==due.AddSeconds(1)&&ClericLongRestProfile.Active(finished)==null
            &&finished.ClericLongRestSettlements.Single().At==due&&finished.ConvictionBalance.Current==5
            &&finished.ExpeditionStrainRecoveryOffers.Length==0&&finished.ManufacturingAdvance==null,"Cross-boundary advance lost remaining time or duplicated recovery.");
        string continued=Path.Combine(output,"backup-recovered-continued.ddsave");funded.Save(continued);funded.Restore(continued);
        Need(codec.Encode(finished).SequenceEqual(codec.Encode(State(funded))),"Backup continuation failed strict restore.");
        reports.Add(new{scope="Genuine pending backup, explicit public recovery and continuation beyond completion",backupExact=true,displacedCorruptionPreserved=true,completedAt=due.ToString(),continuedAt=finished.RuleClock.ToString(),noPendingChoice=true,
            limitation="No positive Strain-point choice or held choice remainder is claimed: actual shortages block recovery, and Rest Debt removal classification remains unresolved."});
        return JsonSerializer.Serialize(reports);
    }
}