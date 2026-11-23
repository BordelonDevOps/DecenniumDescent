using System;using System.IO;using System.Linq;using System.Collections.Generic;using System.Reflection;using System.Text.Json;using Decennium.Foundation;using Decennium.Foundation.Laboratory;using Decennium.Foundation.Tests;
public static class OrdinaryBoundaryProbe {
 const string A=ClericRpProfile.Actor,H=ConnectedExpeditionSession.Hero;
 static readonly SnapshotCodec Codec=new SnapshotCodec();static readonly JsonSerializerOptions J=new JsonSerializerOptions{IncludeFields=true,WriteIndented=true};
 static void Check(bool ok,string why){if(!ok)throw new Exception(why);}
 static Snapshot S(ConnectedExpeditionSession s)=>(Snapshot)typeof(FoundationCases).GetMethod("ShortRestCapture",BindingFlags.Static|BindingFlags.NonPublic).Invoke(null,new object[]{s});
 static ConnectedExpeditionSession At(string path){var s=ConnectedExpeditionSession.StartWithOrdinaryMagicalActivity(ClericInitialSelection.AuthoredExample(),ClericRepertoireSelection.AuthoredExample(),ClericMilestoneDeclaration.AuthoredExample(),BishopEntryRecord.Announced());s.Restore(path);return s;}
 static void Paid(ConnectedExpeditionSession s,Command c){var r=c.Kind==CommandKind.AdvanceClock?s.SubmitSessionCommand(c):s.Submit(ExpeditionSeat.Player,c);Check(r.Response==ExpeditionResponse.Committed,c.Id+" "+r.Response);}
 static RuleTime Offset(RuleTime at,int n,int d=1)=>new RuleTime(checked(at.Numerator*d+(long)n*at.Denominator),checked(at.Denominator*d));
 static void Advance(ConnectedExpeditionSession s,RuleTime at,string id){var now=S(s).RuleClock;Check(at>now,"Positive real advance required");var delta=new RuleTime(checked(at.Numerator*now.Denominator-now.Numerator*at.Denominator),checked(at.Denominator*now.Denominator));Paid(s,new Command(id,H,S(s).Revision,CommandKind.AdvanceClock,x:checked((int)delta.Numerator),y:checked((int)delta.Denominator)));}
 static RuleTime Next(Snapshot s){var e=WorldTiming.ForActor(s,A);return e.Start(e.LatestStart(A,e.ProcessedSlot)+e.Order.Count);}
 static void Save(ConnectedExpeditionSession s,string file){var before=Codec.Encode(S(s));s.Save(file);s.Restore(file);Check(before.SequenceEqual(Codec.Encode(S(s))),"Strict restore changed canonical state");}
 static object Facts(Snapshot s)=>new{s.Revision,s.RuleClock,s.RandomState,allowance=s.OrdinaryMagic.Current,strain=s.CastingStrain,interval=s.WorldIntervals.Single(x=>x.ActorId==A),settlements=s.OrdinaryMagic.Settlements,recharges=s.AbilityRecharges,effects=s.SpellEffects};
 public static void Run(string dir,string[] args){
  string root=args[0];var contexts=new[]{Path.Combine(root,"c1/cases/tac01_ordinary_magic_genuine_c1_late_rite_and_settlement/c1-open-late-interval.ddsave"),Path.Combine(root,"five-paths-01/ConsoleRestored/r351.ddsave"),Path.Combine(root,"five-paths-01/ConsoleRestored/r436.ddsave")};var rows=new List<object>();
  for(int context=0;context<contexts.Length;context++){
   var s=At(contexts[context]);Check(!S(s).InventoryCombat,"Requires genuine closed context");
   // Three real free Guidance casts supply meaningful strain; no artificial resource or state setup.
   for(int n=0;n<3;n++){Advance(s,Next(S(s)),"oma.bound.seed-time."+n);Paid(s,new Command("oma.bound.seed."+n,A,S(s).Revision,CommandKind.CastKnownSpell,A,spellCast:new SpellCastRequest("guidance",willingTarget:true)));}
   Advance(s,Next(S(s)),"oma.bound.base");var baseline=S(s);var start=baseline.RuleClock;int dissonance=baseline.CastingStrain.Single().Dissonance;Check(dissonance>2,"Meaningful strain missing");
   string fork=Path.Combine(dir,"context"+context+"-base.ddsave");Save(s,fork);int[] points={1999,2000,2001,5999,6000,6001};
   foreach(int point in points){
    s=At(fork);Advance(s,Offset(start,point,1000),"oma.bound.to."+point);var before=S(s);bool refreshed=point>=6000;
    Check(before.CastingStrain.Single().Dissonance==dissonance-(refreshed?1:0),"Idle settlement moved from next owner Start");
    var old=before.OrdinaryMagic.Settlements.Where(x=>x.Origin.SameAs(baseline.OrdinaryMagic.Current.Origin)).ToArray();
    Check(old.Length==(refreshed?1:0),"Wrong before/at/after settlement count");
    if(refreshed)Check(old[0].At==Offset(start,6)&&old[0].IdleEligible&&old[0].After==dissonance-1,"Old opportunity did not settle before new use");
    var cmd=new Command("oma.bound.ground."+point,A,before.Revision,CommandKind.GroundCastingStrain);var bytes=Codec.Encode(before);var query=s.QueryCastingCommand(ExpeditionSeat.Player,cmd);
    Check(query.Admissible&&bytes.SequenceEqual(Codec.Encode(S(s))),"Boundary query not pure/available "+query.Code);Paid(s,cmd);var paid=S(s);
    Check(paid.RuleClock==before.RuleClock&&paid.RandomState==before.RandomState&&paid.OrdinaryMagic.Activities.Last().Origin.SameAs(before.OrdinaryMagic.Current.Origin),"Producer did not bind actual current allowance");
    var origin=before.OrdinaryMagic.Current.Origin;var deadline=before.OrdinaryMagic.Current.Deadline;Advance(s,deadline,"oma.bound.settle."+point);var end=S(s);var settlement=end.OrdinaryMagic.Settlements.Single(x=>x.Origin.SameAs(origin));
    int pb=CharacterRuleFacts.ForActor(before,A).ProficiencyBonus;
    Check(settlement.At==deadline&&settlement.Grounding&&!settlement.MagicalActivity&&settlement.Before==before.CastingStrain.Single().Dissonance&&settlement.After==Math.Max(0,settlement.Before-pb),"Ground did not settle once at actual deadline");
    Save(s,Path.Combine(dir,"context"+context+"-at"+point+"-after.ddsave"));rows.Add(new{context,point,epoch=WorldTiming.ForActor(baseline,A).Id,before=Facts(before),paid=Facts(paid),settlement,after=Facts(end)});
    File.WriteAllText(Path.Combine(dir,"progress.json"),JsonSerializer.Serialize(rows,J));
   }
  }
  File.WriteAllText(Path.Combine(dir,"result.json"),JsonSerializer.Serialize(new{status="PASS",scope="Three actual outside contexts, meaningful strain, six exact old-End/next-owner-Start positions each, pure query, real paid Ground, exact once settlement, strict restore. No fabricated calendar/state.",cases=rows},J));
 }
 public static void Producers(string dir,string[] args){
  string root=args[0];var rows=new List<object>();
  var s=At(Path.Combine(root,"five-paths-01/ConsoleRestored/r344.ddsave"));Advance(s,Offset(Next(S(s)),3),"oma.ward.late");var before=S(s);
  var cast=new Command("oma.ward.cast",A,before.Revision,CommandKind.CastKnownSpell,A,spellCast:new SpellCastRequest("arcane-ward",SpellCastingProfile.FocusId,willingTarget:true));
  var q=s.QueryCastingCommand(ExpeditionSeat.Player,cast);Check(q.Admissible,"Actual late Ward unavailable: "+q.Code);Paid(s,cast);var paid=S(s);var ward=paid.SpellEffects.Single(x=>x.CastId==cast.Id);
  Check(ward.ExpiryKind==SpellExpiryKind.NextCasterStart&&ward.ExpiresAt==Next(before)&&ward.StartedAt==before.RuleClock,"Late Ward did not capture next actual current-context Start");
  Advance(s,Offset(ward.ExpiresAt,-1,1000),"oma.ward.before-expiry");Check(S(s).SpellEffects.Single(x=>x.Id==ward.Id).Present,"Ward ended early");
  Save(s,Path.Combine(dir,"ward-before-expiry.ddsave"));Advance(s,ward.ExpiresAt,"oma.ward.at-expiry");var ended=S(s).SpellEffects.Single(x=>x.Id==ward.Id);Check(!ended.Present&&ended.EndedAt==ward.ExpiresAt,"Ward did not expire at captured Start");
  Save(s,Path.Combine(dir,"ward-expired.ddsave"));rows.Add(new{name="late-ward-next-caster-start",before=Facts(before),paid=Facts(paid),ended,after=Facts(S(s))});
  string source=Path.Combine(root,"five-paths-01/ConsoleRestored/r352.ddsave");s=At(source);var original=S(s).Consecration.Zones.Last();Advance(s,Next(S(s)),"oma.recharge.next");var state=S(s);var body=state.Actors.Single(x=>x.Id==A);
  var tryAgain=new Command("oma.recharge.too-soon",A,state.Revision,CommandKind.UseConsecrate,consecrate:new ConsecrateRequest(body.X,body.Y));var canonical=Codec.Encode(state);var denied=s.QueryCastingCommand(ExpeditionSeat.Player,tryAgain);var response=s.Submit(ExpeditionSeat.Player,tryAgain);
  Check(denied.Code=="ConsecrateRecharging"&&response.Response==ExpeditionResponse.Unavailable&&canonical.SequenceEqual(Codec.Encode(S(s))),"Actual recharge-not-ready denial incorrect");rows.Add(new{name="actual-recharge-not-ready",denied.Code,response.Response,recharge=state.AbilityRecharges});
  foreach(bool exact in new[]{false,true}){
   s=At(source);Advance(s,exact?original.ExpiresAt:Offset(original.ExpiresAt,-1,1000),"oma.zone.expiry-branch");state=S(s);body=state.Actors.Single(x=>x.Id==A);
   Paid(s,new Command("oma.zone.new",A,state.Revision,CommandKind.UseConsecrate,consecrate:new ConsecrateRequest(body.X,body.Y)));var after=S(s);var old=after.Consecration.Zones.Single(x=>x.CommandId==original.CommandId);var latest=after.Consecration.Zones.Last();
   Check(old.End==(exact?ConsecrationEnd.Expiry:ConsecrationEnd.Replacement)&&old.EndAt==state.RuleClock&&latest.ExpiresAt==state.RuleClock.AddSeconds(18),"Expiry/replacement producer tie changed");
   Save(s,Path.Combine(dir,exact?"expiry-tie.ddsave":"replacement-before-expiry.ddsave"));rows.Add(new{name=exact?"expiry-before-same-time-producer":"replacement-before-expiry",old,latest,after=Facts(after)});
  }
  File.WriteAllText(Path.Combine(dir,"result.json"),JsonSerializer.Serialize(new{status="PASS",scope="Actual late Ward captures next current-calendar owner Start; actual not-ready recharge rejects atomically; existing terrain expiry runs before same-time producer while earlier producer replaces. No source/lifetime changes.",cases=rows},J));
 }
}
