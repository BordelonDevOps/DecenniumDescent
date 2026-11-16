using System;
using System.IO;
using System.Linq;
using System.Reflection;
using System.Collections.Generic;
using Decennium.Foundation;
using Decennium.Foundation.Laboratory;
public static class LongRestCommandControls {
    const string Actor=ClericRpProfile.Actor,Hero=ConnectedExpeditionSession.Hero;
    static void Need(bool value,string text){if(!value)throw new Exception(text);}
    static Simulation Sim(ConnectedExpeditionSession s)=>(Simulation)s.GetType().GetField("simulation",BindingFlags.NonPublic|BindingFlags.Instance).GetValue(s);
    static Snapshot State(ConnectedExpeditionSession s)=>Sim(s).Capture();
    static ConnectedExpeditionSession New(string path){var s=ConnectedExpeditionSession.StartWithClericLongRest(ClericInitialSelection.AuthoredExample(),ClericRepertoireSelection.AuthoredExample(),ClericMilestoneDeclaration.AuthoredExample());s.Restore(path);return s;}
    static void Commit(ConnectedExpeditionSession s,Command c){var r=c.Kind==CommandKind.AdvanceClock?s.SubmitSessionCommand(c):s.Submit(ExpeditionSeat.Player,c);Need(r.Response==ExpeditionResponse.Committed,"Control did not commit "+c.Kind+": "+r.Response);}
    static Command Make(ConnectedExpeditionSession s,string id,CommandKind kind,string target="",int x=0,int y=0,string actor=Actor)=>new Command(id,actor,State(s).Revision,kind,target,x,y);
    static void OwnTurn(ConnectedExpeditionSession s){for(int i=0;i<3;i++){var a=State(s);var e=WorldTiming.ForActor(a,Actor);if(e.Order[(int)(e.ProcessedSlot%e.Order.Count)]==Actor)return;Commit(s,Make(s,"control.own."+i,CommandKind.AdvanceClock,x:2,y:1,actor:Hero));}throw new Exception("No owning turn.");}
    public static string Run(string ready,string funded,string output){
        var session=New(ready);var codec=new SnapshotCodec();var reports=new List<object>();
        var grant=new Authority("TEST_ONLY.host",new[]{Hero,Actor},inventoryOwners:new[]{Hero,Actor});
        void Deny(string name,Command c,string expected,Authority authority=null){
            var sim=Sim(session);var before=codec.Encode(sim.Capture());var query=sim.QueryCommand(authority??grant,c);
            Need(before.SequenceEqual(codec.Encode(sim.Capture())),"Query changed "+name);
            var result=sim.Execute(authority??grant,c);var after=codec.Encode(sim.Capture());
            Need(!query.Admissible&&query.Code==expected&&result.Outcome==Outcome.Rejected&&result.Code==expected&&before.SequenceEqual(after),
                name+" differs: "+query.Code+" / "+result.Code);
            File.WriteAllBytes(Path.Combine(output,name+"-before.ddsave"),before);File.WriteAllBytes(Path.Combine(output,name+"-after.ddsave"),after);
            reports.Add(new{name,scope="Actual typed query and command",query=query.Code,result=result.Code,unchanged=true});
        }
        Deny("wrong-participant",Make(session,"control.hero",CommandKind.BeginLongRest,ClericLongRestProfile.SiteId,actor:Hero),"LongRestUnavailable");
        Deny("wrong-site",Make(session,"control.site",CommandKind.BeginLongRest,"TEST_ONLY.unknown-berth"),"LongRestSiteUnavailable");
        Deny("extra-payload",Make(session,"control.payload",CommandKind.BeginLongRest,ClericLongRestProfile.SiteId,x:1),"UnexpectedLongRestPayload");
        Deny("stale",new Command("control.stale",Actor,State(session).Revision-1,CommandKind.BeginLongRest,ClericLongRestProfile.SiteId),"StaleRevision");
        session=New(funded);OwnTurn(session);
        Commit(session,new Command("control.concentration.cast",Actor,State(session).Revision,CommandKind.CastKnownSpell,Actor,
            spellCast:new SpellCastRequest("sanctuary",SpellCastingProfile.FocusId,true)));
        session.Save(Path.Combine(output,"long-rest-concentration-active.ddsave"));
        Deny("active-concentration",Make(session,"control.concentration.denied",CommandKind.BeginLongRest,ClericLongRestProfile.SiteId),"LongRestRequiresConcentrationEnded");
        string effect=State(session).SpellEffects.Single(x=>x.Present&&x.CasterId==Actor&&x.RequiresConcentration).Id;
        Commit(session,Make(session,"control.concentration.end",CommandKind.EndSpellConcentration,effect));
        Need(session.DiscoverCastingCommands(ExpeditionSeat.Player,Actor).Any(x=>x.Command.Kind==CommandKind.BeginLongRest),"Lawful ending did not expose rest.");
        var begin=Make(session,"control.rest.begin",CommandKind.BeginLongRest,ClericLongRestProfile.SiteId);
        var beforeQuery=codec.Encode(State(session));Need(session.QueryCastingCommand(ExpeditionSeat.Player,begin).Admissible
            &&beforeQuery.SequenceEqual(codec.Encode(State(session))),"Public admission query was not pure.");Commit(session,begin);
        var activeBytes=codec.Encode(State(session));
        Need(session.Submit(ExpeditionSeat.Player,begin).Response==ExpeditionResponse.Duplicate&&activeBytes.SequenceEqual(codec.Encode(State(session))),"Authorized exact retry changed state.");
        Deny("revoked-retry",begin,"NotAuthorized",new Authority("TEST_ONLY.host",new[]{Hero},inventoryOwners:new[]{Hero}));
        Deny("conflicting-id",new Command(begin.Id,Actor,State(session).Revision,CommandKind.BeginLongRest,ClericLongRestProfile.SiteId,1),"CommandIdConflict");
        Deny("already-active",Make(session,"control.rest.second",CommandKind.BeginLongRest,ClericLongRestProfile.SiteId),"LongRestAlreadyActive");
        Deny("wrong-interruption",Make(session,"control.interrupt.wrong",CommandKind.InterruptLongRest,"TEST_ONLY.unknown-rest"),"NoMatchingActiveLongRest");
        Deny("resting-movement",Make(session,"control.move",CommandKind.BeginWorldStep,"walk",1),"LongRestRequiresInterruption");
        session.Save(Path.Combine(output,"long-rest-concentration-started.ddsave"));
        Commit(session,Make(session,"control.rest.almost",CommandKind.AdvanceClock,x:28799,y:1,actor:Hero));
        var almost=State(session);Need(ClericLongRestProfile.Active(almost)!=null&&almost.ClericLongRestSettlements.Length==1,"Insufficient duration settled recovery.");
        session.Save(Path.Combine(output,"long-rest-before-due.ddsave"));
        Commit(session,Make(session,"control.rest.finish",CommandKind.AdvanceClock,x:1,y:1,actor:Hero));
        var complete=State(session);Need(complete.ClericLongRestSettlements.Last().Benefit==ClericLongRestBenefit.CadenceLimited
            &&complete.ResonancePools.Single().Current==2&&complete.ConvictionBalance.Current==5,"Concentration branch incorrectly recovered resources inside the cap.");
        session.Save(Path.Combine(output,"long-rest-concentration-completed.ddsave"));
        var advance=Make(session,"control.rest.repeat-time",CommandKind.AdvanceClock,x:1,y:1,actor:Hero);Commit(session,advance);
        Need(State(session).ClericLongRestSettlements.Length==complete.ClericLongRestSettlements.Length,"Later time settled a completed rest again.");
        reports.Add(new{scope="Genuine accepted cast, rest denial, voluntary concentration ending, full rest and paid resource retention",queryPure=true,authorizedRetryUnchanged=true,insufficientDuration=true,noDoubleSettlement=true});
        return System.Text.Json.JsonSerializer.Serialize(reports);
    }
}