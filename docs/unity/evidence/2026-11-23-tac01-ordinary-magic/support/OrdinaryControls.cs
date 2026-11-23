using System;using System.IO;using System.Linq;using System.Reflection;using System.Collections.Generic;using System.Text.Json;using Decennium.Foundation;using Decennium.Foundation.Laboratory;using Decennium.Foundation.Tests;
public static class OrdinaryControls {
 static readonly JsonSerializerOptions J=new JsonSerializerOptions{IncludeFields=true,WriteIndented=true};static readonly SnapshotCodec Codec=new SnapshotCodec();
 static Snapshot S(ConnectedExpeditionSession s)=>(Snapshot)typeof(FoundationCases).GetMethod("ShortRestCapture",BindingFlags.Static|BindingFlags.NonPublic).Invoke(null,new object[]{s});
 static void Check(bool ok,string why){if(!ok)throw new Exception(why);}
 static ConnectedExpeditionSession New(int w){var i=ClericInitialSelection.AuthoredExample();var r=ClericRepertoireSelection.AuthoredExample();var m=ClericMilestoneDeclaration.AuthoredExample();var b=BishopEntryRecord.Announced();return w switch{95=>ConnectedExpeditionSession.Start(),96=>ConnectedExpeditionSession.StartWithCarriedVial(),97=>ConnectedExpeditionSession.StartWithStowedVial(),98=>ConnectedExpeditionSession.StartWithTacticalVial(),99=>ConnectedExpeditionSession.StartWithCompanionDose(),100=>ConnectedExpeditionSession.StartWithCompanionStabilization(),101=>ConnectedExpeditionSession.StartWithWoundTreatment(),102=>ConnectedExpeditionSession.StartWithConsumeDecay(),103=>ConnectedExpeditionSession.StartWithShortRest(),104=>ConnectedExpeditionSession.StartWithFleshWarden(),105=>ConnectedExpeditionSession.StartWithClericCompanion(i),106=>ConnectedExpeditionSession.StartWithClericRepertoire(i,r),107=>ConnectedExpeditionSession.StartWithFrightened(i,r),108=>ConnectedExpeditionSession.StartWithClericSettlement(i,r,m),109=>ConnectedExpeditionSession.StartWithClericCasting(i,r,m),110=>ConnectedExpeditionSession.StartWithClericLongRest(i,r,m),111=>ConnectedExpeditionSession.StartWithPostRecoveryEncounter(i,r,m),112=>ConnectedExpeditionSession.StartWithBishopEntry(i,r,m,b),113=>ConnectedExpeditionSession.StartWithDeclaredGeometry(i,r,m,b),114=>ConnectedExpeditionSession.StartWithFerryWraith(i,r,m,b),115=>ConnectedExpeditionSession.StartWithConsecration(i,r,m,b),116=>ConnectedExpeditionSession.StartWithOrdinaryMagicalActivity(i,r,m,b),_=>throw new Exception("wire")};}
 static void Replay(ConnectedExpeditionSession s,CommandReceipt receipt){var c=CommandHistory.Read(receipt);ExpeditionActionResult r;
 if(receipt.Principal=="TEST_ONLY.session-operator")r=s.SubmitSessionCommand(c);
 else if(c.Kind==CommandKind.UseIntimidatingPresence&&c.Actor=="TEST_ONLY.later-defender")r=s.SubmitDefenderIntimidatingPresence(LaterDefenderController.DefenderAuthority(),c);
 else if(c.Kind==CommandKind.RespondSanctuary&&receipt.Principal=="TEST_ONLY.tac10-later-defender.v1")r=s.SubmitDefenderSanctuary(LaterDefenderController.DefenderAuthority(),c);
 else if(c.Actor=="TEST_ONLY.later-defender"||receipt.Principal=="TEST_ONLY.ferry-controller")r=s.AdvanceAutomaticDefender();
 else r=s.Submit(c.Actor=="TEST_ONLY.third-combatant"?ExpeditionSeat.FirstOpponent:c.Actor=="TEST_ONLY.recovery-defender"?ExpeditionSeat.RecoveryOpponent:ExpeditionSeat.Player,c);
 Check(r.Response==ExpeditionResponse.Committed&&r.Revision==receipt.Revision,"Continuation failed "+receipt.Revision+" "+c.Id+" "+r.Response);var actual=S(s).Receipts.Last();Check(actual.Fingerprint==receipt.Fingerprint&&actual.Principal==receipt.Principal&&actual.Id==receipt.Id,"Receipt mismatch");}


 static readonly List<object> Rows=new List<object>();const string A=ClericRpProfile.Actor,H=ConnectedExpeditionSession.Hero;
 static Command[] Cards(Snapshot s,string suffix)=>new[]{
  new Command("oma.controls.consecrate."+suffix,A,s.Revision,CommandKind.UseConsecrate,consecrate:new ConsecrateRequest(8,2)),
  new Command("oma.controls.rite."+suffix,A,s.Revision,CommandKind.UseHealingRite,H),
  new Command("oma.controls.invocation."+suffix,A,s.Revision,CommandKind.UseDivineInvocation,divineInvocation:new DivineInvocationRequest(new[]{H,A})),
  new Command("oma.controls.guidance."+suffix,A,s.Revision,CommandKind.CastKnownSpell,H,spellCast:new SpellCastRequest("guidance",willingTarget:true)),
  new Command("oma.controls.ground."+suffix,A,s.Revision,CommandKind.GroundCastingStrain)};
 static void Deny(ConnectedExpeditionSession s,Command c,string name,ExpeditionSeat seat=ExpeditionSeat.Player){
  byte[] before=Codec.Encode(S(s));var q=s.QueryCastingCommand(seat,c);Check(!q.Admissible,name+" unexpectedly admissible "+c.Kind);var r=s.Submit(seat,c);
  Check(r.Response!=ExpeditionResponse.Committed&&r.Response!=ExpeditionResponse.Duplicate&&before.SequenceEqual(Codec.Encode(S(s))),name+" rejection changed gameplay");
  Rows.Add(new{name,kind=c.Kind.ToString(),seat=seat.ToString(),query=q.Code,response=r.Response.ToString(),unchanged=true,revision=S(s).Revision});
 }
 static void Commit(ConnectedExpeditionSession s,Command c){var r=c.Kind==CommandKind.AdvanceClock||c.Kind==CommandKind.EndFixedEncounter?s.SubmitSessionCommand(c):s.Submit(ExpeditionSeat.Player,c);Check(r.Response==ExpeditionResponse.Committed,c.Id+" "+r.Response);}
 static ConnectedExpeditionSession At(string path){var s=New(116);s.Restore(path);return s;}
 static ConnectedExpeditionSession Prefix(string root,Snapshot final,long revision){var files=Directory.GetFiles(root,"r*.ddsave").Where(p=>!p.Contains("after-read")).Select(p=>new{path=p,revision=long.Parse(Path.GetFileNameWithoutExtension(p).Substring(1))}).Where(x=>x.revision<=revision).OrderByDescending(x=>x.revision);var chosen=files.First();var s=At(chosen.path);foreach(var r in final.Receipts.Where(x=>x.Revision>chosen.revision&&x.Revision<=revision))Replay(s,r);Check(S(s).Revision==revision,"Prefix revision mismatch");return s;}
 public static void Run(string dir,string[] args){
  string root=args[0];var final=new FileSaveStore().Load(Path.Combine(root,"r440.ddsave"));var s=At(Path.Combine(root,"r351.ddsave"));var ready=S(s);
  foreach(var c in Cards(ready,"baseline"))Check(s.QueryCastingCommand(ExpeditionSeat.Player,c).Admissible,"Control baseline unavailable "+c.Kind);
  foreach(var seat in new[]{ExpeditionSeat.FirstOpponent,ExpeditionSeat.RecoveryOpponent,ExpeditionSeat.FerryOpponent}){
   foreach(var c in Cards(ready,"seat"))Deny(s,c,"wrong-or-revoked-seat",seat);
   Deny(s,new Command("oma.controls.focus.seat",A,ready.Revision,CommandKind.FocusDetectedAura,"TEST_ONLY.unknown-aura"),"focus-other-seat",seat);
   Check(s.DiscoverCastingCommands(seat,A).Count==0,"Seat leaked discovery");
  }
  Deny(s,new Command("oma.controls.stale",A,ready.Revision-1,CommandKind.GroundCastingStrain),"stale-revision");
  Deny(s,new Command("oma.controls.unknown",A,ready.Revision,CommandKind.CastKnownSpell,A,spellCast:new SpellCastRequest("unknown-spell",willingTarget:true)),"unknown-source");
  Deny(s,new Command("oma.controls.components",A,ready.Revision,CommandKind.CastKnownSpell,A,spellCast:new SpellCastRequest("detect-magic")),"missing-focus-component");
  Deny(s,new Command("oma.controls.center",A,ready.Revision,CommandKind.UseConsecrate,consecrate:new ConsecrateRequest(999,999)),"unsupported-center");
  Deny(s,new Command("oma.controls.target",A,ready.Revision,CommandKind.UseHealingRite,FerryWraithProfile.Actor),"source-target-restriction");
  Deny(s,new Command("oma.controls.no-detect",A,ready.Revision,CommandKind.FocusDetectedAura,"TEST_ONLY.unknown-aura"),"focus-without-effect");
  s=At(Path.Combine(root,"r352.ddsave"));var paid=S(s);var original=CommandHistory.Read(paid.Receipts.Last());byte[] paidBytes=Codec.Encode(paid);
  Check(s.Submit(ExpeditionSeat.Player,original).Response==ExpeditionResponse.Duplicate&&paidBytes.SequenceEqual(Codec.Encode(S(s))),"Persisted authorized retry changed state");
  Rows.Add(new{name="persisted-authorized-retry",revision=paid.Revision,response="Duplicate",unchanged=true});
  Deny(s,new Command(original.Id,A,original.ExpectedRevision,CommandKind.UseConsecrate,consecrate:new ConsecrateRequest(7,2)),"conflicting-id-payload");
  foreach(var c in Cards(paid,"spent"))Deny(s,c,"already-spent-action");
  s=At(Path.Combine(root,"r351.ddsave"));Commit(s,new Command("oma.controls.traverse",A,S(s).Revision,CommandKind.BeginWorldStep,"walk",-1,0));
  Check(S(s).WorldTraversals.Any(x=>x.ActorId==A),"No genuine active traversal");s.Save(Path.Combine(dir,"active-traversal.ddsave"));
  foreach(var c in Cards(S(s),"traverse"))Deny(s,c,"actual-active-traversal");
  var restReceipt=final.Receipts.First(x=>CommandHistory.Read(x).Kind==CommandKind.BeginLongRest);s=Prefix(root,final,restReceipt.Revision);s.Save(Path.Combine(dir,"actual-active-long-rest.ddsave"));
  foreach(var c in Cards(S(s),"rest"))Deny(s,c,"actual-active-long-rest");
  var pending=final.Receipts.FirstOrDefault(x=>x.Revision>250&&new[]{CommandKind.RespondOpportunityAttack,CommandKind.RespondPress,CommandKind.RespondSanctuary}.Contains(CommandHistory.Read(x).Kind));
  Check(pending!=null,"No genuine pending-choice recipe");s=Prefix(root,final,pending.Revision-1);s.Save(Path.Combine(dir,"actual-pending-choice.ddsave"));
  foreach(var c in Cards(S(s),"pending"))Deny(s,c,"actual-pending-choice");
  File.WriteAllText(Path.Combine(dir,"result.json"),JsonSerializer.Serialize(new{status="PASS",cases=Rows,scope="Actual116 states and real supported commands; atomic reads/rejections, stationary/busy/pending restrictions, source/component/seat/freshness/identity controls and persisted authorized retry. Incapacity and capacity tested separately."},J));
 }
 public static void Incapacity(string dir,string[] args){
  var s=At(Path.Combine(args[0],"r355.ddsave"));var initial=S(s);Check(initial.Encounter.CurrentActor==H,"Expected real Hero opening");
  Commit(s,new Command("oma.incap.guard",H,initial.Revision,CommandKind.SelectCombatStance,combat:new CombatRequest(initial.Encounter.CurrentTurnId,stance:(int)CombatStance.Guarded)));
  Commit(s,new Command("oma.incap.move",H,S(s).Revision,CommandKind.TacticalStep,S(s).Encounter.CurrentTurnId,7,2));
  bool found=false;int count=0;
  for(;count<80;count++){
   var state=S(s);var life=state.Lives.Single(x=>x.ActorId==A);var view=TestOnlyClubAttackPolicy.ConditionsFor(state,A).View();
   if(state.Encounter.CurrentActor==A&&view.Has(ConditionKind.Unconscious)&&!life.Dead){found=true;s.Save(Path.Combine(dir,"actual-incapacitated-own-turn.ddsave"));foreach(var c in Cards(state,"incap"))Deny(s,c,"actual-incapacitated-owner");break;}
   Check(!life.Dead,"Cleric died before the selected incapacity witness");
   if(s.View(ExpeditionSeat.Player).NextSeat==ExpeditionTurnSeat.FerryOpponent){Check(s.AdvanceAutomaticDefender().Response==ExpeditionResponse.Committed,"Ferry action failed");continue;}
   string actor=state.Encounter.CurrentActor;
   if(!TestOnlyClubAttackPolicy.ConditionsFor(state,actor).View().Unaware&&!state.Stances.Any(x=>x.TurnOrdinal==state.Encounter.TurnOrdinal&&EncounterHistory.InCurrent(state,x.Revision)))
    Commit(s,new Command("oma.incap.guard."+state.Revision,actor,state.Revision,CommandKind.SelectCombatStance,combat:new CombatRequest(state.Encounter.CurrentTurnId,stance:(int)CombatStance.Guarded)));
   state=S(s);Commit(s,new Command("oma.incap.end."+state.Revision,actor,state.Revision,CommandKind.EndRegularTurn,state.Encounter.CurrentTurnId));
  }
  Check(found,"No actual incapacitated owner within80 commands");File.WriteAllText(Path.Combine(dir,"result.json"),JsonSerializer.Serialize(new{status="PASS",commands=count,cases=Rows,scope="Actual Ferry attacks and life/condition transitions, no injected damage or condition."},J));
 }
 public static void Capacity(string dir,string[] args){
  var s=At(Path.Combine(args[0],"r440.ddsave"));
  while(S(s).Receipts.Length<512){var state=S(s);Commit(s,new Command("oma.capacity.advance."+state.Revision,H,state.Revision,CommandKind.AdvanceClock,x:1,y:1));}
  s.Save(Path.Combine(dir,"actual-receipt-capacity.ddsave"));s.Restore(Path.Combine(dir,"actual-receipt-capacity.ddsave"));var full=S(s);
  foreach(var c in Cards(full,"capacity")){Deny(s,c,"actual-session-capacity");Check(s.QueryCastingCommand(ExpeditionSeat.Player,c).Code=="SessionCapacityReached","Capacity diagnostic mismatch");}
  Deny(s,new Command("oma.capacity.focus",A,full.Revision,CommandKind.FocusDetectedAura,"TEST_ONLY.unknown-aura"),"actual-session-capacity-focus");
  File.WriteAllText(Path.Combine(dir,"result.json"),JsonSerializer.Serialize(new{status="PASS",full.Revision,receiptCount=full.Receipts.Length,cases=Rows,scope="Genuine512-receipt campaign; six-operation session-capacity rejection preserves canonical state/RNG/resources/histories. Larger unreachable per-calendar bounds are separate structural guards."},J));
 }

}
