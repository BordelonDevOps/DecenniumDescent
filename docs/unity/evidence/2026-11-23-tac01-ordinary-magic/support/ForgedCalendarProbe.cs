using System;using System.IO;using System.Linq;using System.Reflection;using System.Collections.Generic;using System.Security.Cryptography;using System.Text.Json;using Decennium.Foundation;using Decennium.Foundation.Laboratory;using Decennium.Foundation.Tests;
public static class ForgedCalendarProbe {
 static readonly SnapshotCodec Codec=new SnapshotCodec();static readonly List<object> Rows=new List<object>();static readonly JsonSerializerOptions J=new JsonSerializerOptions{IncludeFields=true,WriteIndented=true};
 static void Check(bool ok,string why){if(!ok)throw new Exception(why);}
 static Snapshot S(ConnectedExpeditionSession s)=>(Snapshot)typeof(FoundationCases).GetMethod("ShortRestCapture",BindingFlags.NonPublic|BindingFlags.Static).Invoke(null,new object[]{s});
 static ConnectedExpeditionSession New()=>ConnectedExpeditionSession.StartWithOrdinaryMagicalActivity(ClericInitialSelection.AuthoredExample(),ClericRepertoireSelection.AuthoredExample(),ClericMilestoneDeclaration.AuthoredExample(),BishopEntryRecord.Announced());
 static byte[] Section(MagicalActivityCalendarRecord record){using(var stream=new MemoryStream()){using(var w=new BinaryWriter(stream,System.Text.Encoding.UTF8,true)){typeof(SnapshotCodec).Assembly.GetType("Decennium.Foundation.OrdinaryMagicCodec").GetMethod("Write",BindingFlags.Static|BindingFlags.NonPublic).Invoke(null,new object[]{w,record});w.Flush();}return stream.ToArray();}}
 static string Hash(byte[] bytes){using(var h=SHA256.Create())return string.Concat(h.ComputeHash(bytes).Select(x=>x.ToString("x2")));}
 static void Reject(string source,string dir,string name,Func<MagicalActivityCalendarRecord,MagicalActivityCalendarRecord> change){
  byte[] authentic=File.ReadAllBytes(source);var original=Codec.Decode(authentic);byte[] old=Section(original.OrdinaryMagic),replacement=Section(change(original.OrdinaryMagic));int start=authentic.Length-32-old.Length;
  Check(start>0&&authentic.Skip(start).Take(old.Length).SequenceEqual(old),"Calendar is not the exact final payload section");
  byte[] payload=authentic.Take(start).Concat(replacement).ToArray(),forged;using(var hash=SHA256.Create())forged=payload.Concat(hash.ComputeHash(payload)).ToArray();
  string path=Path.Combine(dir,name+".malformed.ddsave");File.WriteAllBytes(path,forged);bool rejected=false;string reason="";
  try{Codec.Decode(forged);}catch(Exception e)when(e is ArgumentException||e is InvalidDataException){rejected=true;reason=e.Message;}Check(rejected,"Rechecksummed causal forgery decoded: "+name);
  var session=New();session.Restore(source);byte[] before=Codec.Encode(S(session));rejected=false;try{session.Restore(path);}catch(Exception e)when(e is ArgumentException||e is InvalidDataException){rejected=true;}
  Check(rejected&&before.SequenceEqual(Codec.Encode(S(session))),"Rejected restore changed live state "+name);
  Rows.Add(new{name,source,sourceSha256=Hash(authentic),forgedSha256=Hash(forged),recomputedChecksum=true,decodeRejected=true,restoreRejected=true,liveUnchanged=true,reason});File.WriteAllText(Path.Combine(dir,"progress.json"),JsonSerializer.Serialize(Rows,J));
 }
 static MagicalSegmentRecord Segment(MagicalSegmentRecord x,long ordinal)=>new MagicalSegmentRecord(ordinal,x.Origin,x.ContextEpoch,x.InInitiative,x.ConsumedAtOpen,x.CauseId,x.Revision,x.At,x.Closed,x.CloseCauseId,x.CloseRevision,x.CloseAt);
 static MagicalSettlementRecord Settlement(MagicalSettlementRecord x,long ordinal)=>new MagicalSettlementRecord(ordinal,x.Origin,x.SegmentOrdinal,x.ContextEpoch,x.CauseId,x.Revision,x.At,x.Reason,x.IdleEligible,x.MagicalActivity,x.Grounding,x.Proficiency,x.Before,x.After);
 static MagicalActivityCalendarRecord TieSwap(MagicalActivityCalendarRecord r){
  var segment=r.Segments.Single(x=>x.Ordinal==r.Current.SegmentOrdinal);var end=r.Settlements.Single(x=>x.At==segment.At&&x.Origin.EpochId!=segment.Origin.EpochId);
  Check(end.Ordinal<segment.Ordinal&&end.SegmentOrdinal<end.Ordinal,"No actual settlement/first-new-Start phase tie");var c=r.Current;
  return r.With(r.NextOrdinal,new MagicalAllowanceRecord(c.Origin,c.OriginAt,c.Deadline,c.ContextEpoch,c.InInitiative,c.Consumed,end.Ordinal),segments:r.Segments.Select(x=>x==segment?Segment(x,end.Ordinal):x),settlements:r.Settlements.Select(x=>x==end?Settlement(x,segment.Ordinal):x));
 }
 public static void Run(string dir,string[] args){string root=args[0],late=Path.Combine(root,"main-01/late-consecrate-paid.ddsave"),admitted=Path.Combine(root,"main-01/ferry-admitted.ddsave");
  Reject(late,dir,"invented-origin-endpoint",r=>{var c=r.Current;return r.With(r.NextOrdinal,new MagicalAllowanceRecord(c.Origin,c.OriginAt.AddSeconds(1),c.Deadline.AddSeconds(1),c.ContextEpoch,c.InInitiative,c.Consumed,c.SegmentOrdinal));});
  Reject(late,dir,"invented-consumed-opportunity",r=>{var c=r.Current;return r.With(r.NextOrdinal,new MagicalAllowanceRecord(c.Origin,c.OriginAt,c.Deadline,c.ContextEpoch,c.InInitiative,!c.Consumed,c.SegmentOrdinal));});
  Reject(late,dir,"wrong-paid-activity-classification",r=>{var a=r.Activities.Last();return r.With(r.NextOrdinal,r.Current,activities:r.Activities.Select(x=>x==a?new MagicalActivityContextRecord(a.Ordinal,a.CommandId,a.Revision,a.At,a.Origin,a.SegmentOrdinal,a.ContextEpoch,a.InInitiative,a.ConsumedAtUse,CastingActivityKind.Grounding):x));});
  Reject(late,dir,"activity-without-paid-source",r=>{var a=r.Activities.Last();return r.With(r.NextOrdinal,r.Current,activities:r.Activities.Select(x=>x==a?new MagicalActivityContextRecord(a.Ordinal,"oma.forged-unpaid-source",a.Revision,a.At,a.Origin,a.SegmentOrdinal,a.ContextEpoch,a.InInitiative,a.ConsumedAtUse,a.Kind):x));});
  Reject(admitted,dir,"forged-carried-spending",r=>{var t=r.Transitions.Last(x=>x.FromEpoch!=x.ToEpoch);var c=t.AdmissionCarry;var w=c.Interval;var carry=new ReinforcementCarry(new WorldIntervalRecord(w.ActorId,w.LastStart,w.MovementSpent,!w.ActionSpent,w.DashPaid,w.ReactionAvailable,w.Interactions),c.BonusActionAvailable);return r.With(r.NextOrdinal,r.Current,transitions:r.Transitions.Select(x=>x==t?new MagicalTransitionRecord(t.Ordinal,t.CauseId,t.Revision,t.At,t.Origin,t.FromEpoch,t.ToEpoch,t.FromInitiative,t.ToInitiative,t.Consumed,carry):x));});
  Reject(late,dir,"missing-genuine-zero-end",r=>{var end=r.Settlements.First(x=>x.Before==0&&x.After==0);return r.With(r.NextOrdinal,r.Current,settlements:r.Settlements.Where(x=>x!=end));});
  Reject(Path.Combine(root,"carry-01/rites-0/ground-replaced.ddsave"),dir,"full-deadline-refresh-phase-swap",TieSwap);
  Reject(Path.Combine(root,"early-stance-3-corrected/ferry-admitted.ddsave"),dir,"index-zero-admission-refresh-phase-swap",TieSwap);
  File.WriteAllText(Path.Combine(dir,"result.json"),JsonSerializer.Serialize(new{status="PASS",cases=Rows,scope="Malformed negative files splice only the actual calendar section with a recomputed SHA256 checksum. They are never adopted. Independent decode and strict live-session restore reject while preserving original state. Actual tied events retain time/counts and contiguous ordinal set; swap reverses settlement versus replacement Start."},J));
 }
}
