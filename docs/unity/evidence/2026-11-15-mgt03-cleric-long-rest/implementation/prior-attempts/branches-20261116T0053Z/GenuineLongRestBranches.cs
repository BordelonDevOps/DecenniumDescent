using System;
using System.IO;
using System.Linq;
using System.Reflection;
using System.Collections.Generic;
using Decennium.Foundation;
using Decennium.Foundation.Laboratory;
public static class GenuineLongRestBranches {
    const string Actor=ClericRpProfile.Actor,Hero=ConnectedExpeditionSession.Hero;
    static void Need(bool value,string text){if(!value)throw new Exception(text);}
    static Simulation Sim(ConnectedExpeditionSession s)=>(Simulation)s.GetType().GetField("simulation",BindingFlags.NonPublic|BindingFlags.Instance).GetValue(s);
    static Snapshot State(ConnectedExpeditionSession s)=>Sim(s).Capture();
    static ConnectedExpeditionSession New(string path){var s=ConnectedExpeditionSession.StartWithClericLongRest(ClericInitialSelection.AuthoredExample(),ClericRepertoireSelection.AuthoredExample(),ClericMilestoneDeclaration.AuthoredExample());s.Restore(path);return s;}
    static void Commit(ConnectedExpeditionSession s,string actor,CommandKind kind,string target="",int x=0,int y=0){
        var c=new Command("long-rest.branch."+State(s).Revision,actor,State(s).Revision,kind,target,x,y);
        var r=kind==CommandKind.AdvanceClock?s.SubmitSessionCommand(c):s.Submit(ExpeditionSeat.Player,c);
        Need(r.Response==ExpeditionResponse.Committed,"Branch did not commit "+kind+" at "+c.ExpectedRevision+": "+r.Response);
    }
    static void AdvanceTo(ConnectedExpeditionSession s,RuleTime target){
        var at=State(s).RuleClock;var delta=new RuleTime(checked(target.Numerator*at.Denominator-at.Numerator*target.Denominator),checked(target.Denominator*at.Denominator));
        Need(delta>=default(RuleTime),"Branch tried to reverse time.");
        if(delta>default(RuleTime))Commit(s,Hero,CommandKind.AdvanceClock,x:checked((int)delta.Numerator),y:checked((int)delta.Denominator));
    }
    static void OwnTurn(ConnectedExpeditionSession s){for(int i=0;i<3;i++){var a=State(s);var e=WorldTiming.ForActor(a,Actor);if(e.Order[(int)(e.ProcessedSlot%e.Order.Count)]==Actor)return;Commit(s,Hero,CommandKind.AdvanceClock,x:2,y:1);}throw new Exception("No owning turn.");}
    static string Facts(Snapshot s)=>System.Text.Json.JsonSerializer.Serialize(new {
        clock=s.RuleClock.ToString(),s.RandomState,positions=s.Actors.Select(x=>new{x.Id,x.X,x.Y}),s.Lives,s.ResonancePools,
        conviction=s.ConvictionBalance?.Current,s.CastingStrain,s.KnownSpells,s.CharacterHitDice,s.CharacterFeatureGrants,
        s.InventoryLots,s.PortableEquipment,s.Vessels,s.VesselContents,lots=s.Work.Lots,
        daily=s.DailyProvisioningSettlements.Select(x=>new{x.ActorId,x.DayOrdinal,x.FoodConsumed,x.WaterConsumed,x.HasShortfall}),
        watches=s.RestWatchOutcomes.Select(x=>new{x.ActorId,x.DayOrdinal,x.Slot,x.Start,x.End,x.Outcome}),
        debt=s.RestDebtEvents.Select(x=>new{x.ActorId,x.Kind,x.At,x.DeadlineAfter}),
        strain=s.Lives.Select(x=>new{x.ActorId,Level=ExpeditionStrainRules.Current(s,x.ActorId).Level}),
        rest=s.ClericLongRestSettlements.Select(x=>new{x.At,x.Benefit,x.HpBefore,x.HpAfter,x.RpBefore,x.RpAfter,x.ConvictionBefore,x.ConvictionAfter,x.Refrain,x.DissonanceBefore,x.DissonanceAfter,x.HitDiceRecovered})});
    public static string Run(string ready,string reference,string output){
        var reports=new List<object>();var codec=new SnapshotCodec();
        var whole=New(ready);string folder=Path.Combine(output,"whole");Directory.CreateDirectory(folder);
        whole.Save(Path.Combine(folder,"long-rest-interrupted.ddsave"));AdvanceTo(whole,new RuleTime(57600));
        Commit(whole,Actor,CommandKind.BeginLongRest,ClericLongRestProfile.SiteId);
        Commit(whole,Hero,CommandKind.AdvanceClock,x:28800,y:1);
        var one=State(whole);var split=new FileSaveStore().Load(reference);
        Need(Facts(one)==Facts(split),"Whole/split partitions changed gameplay authority.");
        whole.Save(Path.Combine(folder,"long-rest-whole-funded.ddsave"));
        File.WriteAllText(Path.Combine(folder,"whole-gameplay.json"),Facts(one));File.WriteAllText(Path.Combine(folder,"split-gameplay.json"),Facts(split));
        reports.Add(new{branch="whole",gameplayParity=true,wholeRevision=one.Revision,splitRevision=split.Revision,
            distinction="Command IDs, receipt/revision partitions and derived provenance IDs differ; gameplay, finite resources, clock and RNG agree."});
        var debt=New(ready);folder=Path.Combine(output,"capped-debt");Directory.CreateDirectory(folder);
        debt.Save(Path.Combine(folder,"long-rest-interrupted.ddsave"));AdvanceTo(debt,new RuleTime(57601));
        Commit(debt,Actor,CommandKind.BeginLongRest,ClericLongRestProfile.SiteId);Commit(debt,Hero,CommandKind.AdvanceClock,x:28800,y:1);
        var first=State(debt);Need(first.ClericLongRestSettlements.Single().At==new RuleTime(86401),"Expected actual arbitrary completion.");
        debt.Save(Path.Combine(folder,"long-rest-debt-first-funded.ddsave"));OwnTurn(debt);Commit(debt,Actor,CommandKind.UseHealingRite,Hero);
        AdvanceTo(debt,new RuleTime(288001,2));Commit(debt,Actor,CommandKind.BeginLongRest,ClericLongRestProfile.SiteId);
        debt.Save(Path.Combine(folder,"long-rest-debt-before-capped.ddsave"));Commit(debt,Hero,CommandKind.AdvanceClock,x:28800,y:1);
        var after=State(debt);var last=after.ClericLongRestSettlements.Last();
        Need(after.RuleClock==new RuleTime(345601,2)&&last.Benefit==ClericLongRestBenefit.CadenceLimited
            &&last.RpBefore==2&&last.RpAfter==2&&last.ConvictionBefore==5&&last.ConvictionAfter==5
            &&!last.ResetsShortRestAllowance&&after.ExpeditionBeneficialRests.Length==1
            &&after.RestWatchOutcomes.Any(x=>x.ActorId==Actor&&x.DayOrdinal==1&&x.Outcome==RestWatchOutcomeKind.Missed)
            &&after.RestDebtEvents.Any(x=>x.ActorId==Actor&&x.Kind==RestDebtEventKind.Opened&&x.At==new RuleTime(172800))
            &&after.RestDebtEvents.Any(x=>x.ActorId==Actor&&x.Kind==RestDebtEventKind.Cleared&&x.EvidenceId==last.RestId&&x.At==last.At),
            "Safe capped completion failed to clear actual newly owed debt or improperly recovered class resources.");
        string path=Path.Combine(folder,"long-rest-debt-capped.ddsave");debt.Save(path);var bytes=codec.Encode(after);debt.Restore(path);
        Need(bytes.SequenceEqual(codec.Encode(State(debt))),"Capped debt clearance failed strict restore.");
        reports.Add(new{branch="capped-debt",firstBenefit=first.ClericLongRestSettlements.Single().At.ToString(),last,
            debt=after.RestDebtEvents.Where(x=>x.ActorId==Actor),scope="Actual missed Watch and public commands, with no synthetic strain/debt/support or inventory grants."});
        return System.Text.Json.JsonSerializer.Serialize(reports);
    }
}