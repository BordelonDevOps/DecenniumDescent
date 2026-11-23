using System;using System.IO;using System.Linq;using System.Collections.Generic;using System.Reflection;using System.Text.Json;using Decennium.Foundation;using Decennium.Foundation.Laboratory;using Decennium.Foundation.Tests;
public static class OrdinaryPendingProbe {
 const string A=ClericRpProfile.Actor,H=ConnectedExpeditionSession.Hero;
 static readonly SnapshotCodec Codec=new SnapshotCodec();static readonly JsonSerializerOptions J=new JsonSerializerOptions{IncludeFields=true,WriteIndented=true};
 static void Check(bool ok,string why){if(!ok)throw new Exception(why);}
 static Snapshot S(ConnectedExpeditionSession s)=>(Snapshot)typeof(FoundationCases).GetMethod("ShortRestCapture",BindingFlags.Static|BindingFlags.NonPublic).Invoke(null,new object[]{s});
 static Command[] Cards(Snapshot s,string tag){var a=s.Actors.Single(x=>x.Id==A);return new[]{new Command("oma.pending."+tag+".rite",A,s.Revision,CommandKind.UseHealingRite,H),new Command("oma.pending."+tag+".consecrate",A,s.Revision,CommandKind.UseConsecrate,consecrate:new ConsecrateRequest(a.X,a.Y)),new Command("oma.pending."+tag+".guidance",A,s.Revision,CommandKind.CastKnownSpell,A,spellCast:new SpellCastRequest("guidance",willingTarget:true)),new Command("oma.pending."+tag+".ground",A,s.Revision,CommandKind.GroundCastingStrain)};}
 public static void Run(string dir,string[] args){
  var s=ConnectedExpeditionSession.StartWithOrdinaryMagicalActivity(ClericInitialSelection.AuthoredExample(),ClericRepertoireSelection.AuthoredExample(),ClericMilestoneDeclaration.AuthoredExample(),BishopEntryRecord.Announced());s.Restore(args[0]);var before=S(s);var baseline=Cards(before,"baseline").Select(c=>new{kind=c.Kind.ToString(),code=s.QueryCastingCommand(ExpeditionSeat.Player,c).Code,admissible=s.QueryCastingCommand(ExpeditionSeat.Player,c).Admissible}).ToArray();
  File.WriteAllText(Path.Combine(dir,"before-facts.json"),JsonSerializer.Serialize(new{before.Revision,before.RuleClock,before.Encounter,before.Actors,before.Lives,before.WorldIntervals,before.Stances,baseline},J));
  Check(baseline.All(x=>x.admissible),"Actual baseline must admit four already owned operations");s.Save(Path.Combine(dir,"before-movement.ddsave"));
  var movement=s.Submit(ExpeditionSeat.Player,new Command("oma.pending.actual-move",A,before.Revision,CommandKind.TacticalStep,before.Encounter.CurrentTurnId,2,3));var after=S(s);s.Save(Path.Combine(dir,"after-movement.ddsave"));var pending=s.View(ExpeditionSeat.Player).PendingDecision;
  File.WriteAllText(Path.Combine(dir,"movement.json"),JsonSerializer.Serialize(new{movement.Response,after.Revision,after.RuleClock,after.Encounter,pending},J));
  Check(movement.Response==ExpeditionResponse.Committed&&pending!=ExpeditionDecisionKind.None,"Actual movement did not open a pending choice");
  var rows=new List<object>();
  foreach(var c in Cards(after,"blocked")){var bytes=Codec.Encode(S(s));var q=s.QueryCastingCommand(ExpeditionSeat.Player,c);var r=s.Submit(ExpeditionSeat.Player,c);Check(q.Code=="TacticalChoicePending"&&!q.Admissible&&r.Response==ExpeditionResponse.Unavailable&&bytes.SequenceEqual(Codec.Encode(S(s))),"Pending guard not isolated: "+c.Kind+" "+q.Code+" "+r.Response);rows.Add(new{kind=c.Kind.ToString(),q.Code,r.Response,unchanged=true});}
  s.Restore(Path.Combine(dir,"after-movement.ddsave"));Check(Codec.Encode(after).SequenceEqual(Codec.Encode(S(s))),"Strict pending restore changed bytes");
  File.WriteAllText(Path.Combine(dir,"result.json"),JsonSerializer.Serialize(new{status="PASS",scope="Otherwise available source-owned four producers on actual Cleric own turn, genuine movement opens pending OA choice without spending Action. All specifically TacticalChoicePending, canonical unchanged; actual pending save strictly restored. Shared casting guard equivalence covers Focus/Invocation rather than pretending unavailable grants/effects are present.",baseline,pending,cases=rows},J));
 }
}
