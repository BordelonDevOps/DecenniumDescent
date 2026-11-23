using System;
using System.IO;
using System.Linq;
using System.Text;
using System.Text.Json;
using System.Reflection;
using System.Collections.Generic;
using System.Security.Cryptography;
using Decennium.Foundation;
using Decennium.Foundation.Laboratory;

// Negative-file construction only: codec section writers are reflected to encode deliberately
// inconsistent records. No reflected state is ever adopted or counted as a playable witness.
public static class WorkControlForgeries
{
    static readonly SnapshotCodec Codec=new SnapshotCodec();
    static readonly JsonSerializerOptions J=new JsonSerializerOptions{WriteIndented=true,IncludeFields=true};
    static readonly List<object> Rows=new List<object>();
    static string Dir,Root;
    static void Check(bool ok,string why){if(!ok)throw new Exception(why);}
    static ConnectedExpeditionSession New()=>ConnectedExpeditionSession.StartWithConnectedWorkControl(
        ClericInitialSelection.AuthoredExample(),ClericRepertoireSelection.AuthoredExample(),ClericMilestoneDeclaration.AuthoredExample(),BishopEntryRecord.Announced());
    static byte[] Capture(ConnectedExpeditionSession s){string p=Path.Combine(Dir,"live.ddsave");s.Save(p);return File.ReadAllBytes(p);}
    static string Hash(byte[] data){using(var h=SHA256.Create())return string.Concat(h.ComputeHash(data).Select(x=>x.ToString("x2")));}
    static byte[] Write(Action<BinaryWriter> action){using(var m=new MemoryStream()){using(var w=new BinaryWriter(m,Encoding.UTF8,true)){action(w);w.Flush();}return m.ToArray();}}
    static void Text(BinaryWriter w,string value){var b=Encoding.UTF8.GetBytes(value);w.Write(b.Length);w.Write(b);}
    static byte[] Text(string value)=>Write(w=>Text(w,value));
    static byte[] Section(string type,object state)=>Write(w=>typeof(SnapshotCodec).Assembly.GetType("Decennium.Foundation."+type)
        .GetMethod("Write",BindingFlags.Public|BindingFlags.NonPublic|BindingFlags.Static).Invoke(null,type=="HarvestCodec"
            ?new[]{(object)w,state,((Snapshot)state).SchemaVersion}:new[]{(object)w,state}));
    static byte[] Work(Snapshot s){var b=new WorkLedgerCodec().Encode(s.Work,2);return BitConverter.GetBytes(b.Length).Concat(b).ToArray();}
    static byte[] Receipts(IEnumerable<CommandReceipt> values)=>Write(w=>{var rows=values.OrderBy(x=>x.Revision).ToArray();w.Write(rows.Length);
        foreach(var r in rows){Text(w,r.Principal);Text(w,r.Id);Text(w,r.Fingerprint);w.Write(r.Revision);}});
    static byte[] Replace(byte[] input,byte[] before,byte[] after){var hits=new List<int>();for(int i=0;i<=input.Length-before.Length;i++){
        if(input[i]!=before[0])continue;bool yes=true;for(int j=1;j<before.Length;j++)if(input[i+j]!=before[j]){yes=false;break;}if(yes)hits.Add(i);}
        Check(hits.Count==1,"Section must be unique, got "+hits.Count);int offset=hits[0];return input.Take(offset).Concat(after).Concat(input.Skip(offset+before.Length)).ToArray();}
    static void Reject(string relative,string name,Func<Snapshot,byte[],byte[]> mutate)
    {
        string source=Path.Combine(Root,relative);byte[] authentic=File.ReadAllBytes(source);var s=Codec.Decode(authentic);
        byte[] payload=mutate(s,authentic.Take(authentic.Length-32).ToArray()),forged;
        using(var h=SHA256.Create())forged=payload.Concat(h.ComputeHash(payload)).ToArray();
        string path=Path.Combine(Dir,name+".forged.ddsave");File.WriteAllBytes(path,forged);
        bool decodeRejected=false;string decodeReason="";try{Codec.Decode(forged);}catch(Exception e)when(e is ArgumentException||e is InvalidDataException){decodeRejected=true;decodeReason=e.Message;}
        var session=New();session.Restore(source);byte[] live=Capture(session);bool rejected=false;string reason="";
        try{session.Restore(path);}catch(Exception e)when(e is ArgumentException||e is InvalidDataException){rejected=true;reason=e.Message;}
        Check(rejected&&live.SequenceEqual(Capture(session)),"Forgery restored or changed live state: "+name);
        Rows.Add(new{name,source,sourceSha256=Hash(authentic),forgedSha256=Hash(forged),recomputedChecksum=true,
            decodeRejected,decodeReason,restoreRejected=true,liveUnchanged=true,reason});
        File.WriteAllText(Path.Combine(Dir,"progress.json"),JsonSerializer.Serialize(Rows,J));Console.WriteLine("PASS forgery "+name);
    }
    static WaterFillRecord Fill(WaterFillRecord f,string actor=null,string source=null,RuleQuantity? amount=null,RuleTime? progress=null,string claim=null)
        =>new WaterFillRecord(f.Id,actor??f.WorkerId,source??f.SourceLotId,f.DestinationId,claim??f.ReservationId,amount??f.Amount,f.StartedAt,progress??f.Progress,f.EndedAt,f.Status,f.OutputLotId);
    static byte[] Change(Snapshot s,byte[] bytes,string section,Action<Snapshot> mutate){byte[] before=Section(section,s);mutate(s);return Replace(bytes,before,Section(section,s));}
    public static void Run(string dir,string[] args)
    {
        Dir=dir;Root=args[0];const string fill="principal-work-01/paused-fill.ddsave",quality="principal-prefix-02/r106.ddsave",done="principal-prefix-02/r107.ddsave";
        if(args.Length<2 || args[1]!="remaining" && args[1]!="age-only") {
        Reject(fill,"wrong-work-actor",(s,b)=>Change(s,b,"WaterVesselCodec",x=>x.WaterFills=x.WaterFills.Select(f=>Fill(f,actor:ConnectedExpeditionSession.Hero)).ToArray()));
        Reject(fill,"wrong-work-source",(s,b)=>Change(s,b,"WaterVesselCodec",x=>x.WaterFills=x.WaterFills.Select(f=>Fill(f,source:"TEST_ONLY.forged-water-source")).ToArray()));
        Reject(fill,"wrong-work-amount",(s,b)=>Change(s,b,"WaterVesselCodec",x=>x.WaterFills=x.WaterFills.Select(f=>Fill(f,amount:new RuleQuantity(3,4))).ToArray()));
        Reject(fill,"wrong-work-reservation",(s,b)=>Change(s,b,"WaterVesselCodec",x=>x.WaterFills=x.WaterFills.Select(f=>Fill(f,claim:"TEST_ONLY.forged-claim")).ToArray()));
        Reject(fill,"coherent-shortened-labor-versus-real-clock-receipt",(s,b)=>{
            var f=s.WaterFills.Single();Check(f.Progress==new RuleTime(3,2),"Not genuine fractional paused labor");
            byte[] water=Section("WaterVesselCodec",s),work=Work(s);s.WaterFills=new[]{Fill(f,progress:new RuleTime(1))};
            s.Work=new WorkLedger(s.Work.Lots,s.Work.WorkerIntervals.Select(w=>w.JobId==f.Id?new WorkerInterval(w.Id,w.JobId,w.WorkerId,w.Start,w.Start.AddSeconds(1)):w),s.Work.Reservations);
            return Replace(Replace(b,water,Section("WaterVesselCodec",s)),work,Work(s));});
        Reject("branches-01/ManufacturingCancelPositive/final.ddsave","changed-positive-cancel-settlement",(s,b)=>{
            byte[] old=Work(s);string id=s.ManufacturingOrders.Single().Id;
            s.Work=new WorkLedger(s.Work.Lots,s.Work.WorkerIntervals,s.Work.Reservations.Select(r=>r.JobId==id&&r.ConsumedAmount>default(RuleQuantity)
                ?new ResourceReservation(r.Id,r.JobId,r.LotId,r.Amount,released:r.Amount):r));return Replace(b,old,Work(s));});
        Reject(done,"forged-formula-identity",(s,b)=>Change(s,b,"FormulaWorkCodec",x=>x.FormulaWork=x.FormulaWork.Select(f=>new FormulaWorkRecord(f.Id,f.WorkerId,"TEST_ONLY.forged-recipe",f.EvidenceId,f.MethodId,f.Kind,f.Status,f.StartedAt,f.UpdatedAt,f.Work,f.First,f.Second,f.Natural,f.PreviousAttemptId)).ToArray()));
        Reject(done,"missing-produced-dose",(s,b)=>Change(s,b,"ManufacturingCodec",x=>x.AlchemyDoses=x.AlchemyDoses.Skip(1).ToArray()));
        Reject(quality,"false-pending-choice-state",(s,b)=>Change(s,b,"ManufacturingCodec",x=>x.ManufacturingOrders=x.ManufacturingOrders.Select(f=>new ManufacturingOrderRecord(f.Id,f.WorkerId,f.RecipeId,f.MaterialSet,f.ExtraVials,f.TakeTen,ManufacturingStatus.Complete,f.Work,f.StartedAt,f.UpdatedAt,f.StabilizedAt,f.First,f.Second,f.Natural,f.Quality,f.Choice,f.RetainedCatalyst,f.Mishap,f.XpAward,f.FindingId,f.MishapIncidentId)).ToArray()));
        Reject(fill,"missing-causal-receipt",(s,b)=>Replace(b,Receipts(s.Receipts),Receipts(s.Receipts.Where(r=>r.Revision!=235))));
        Reject(fill,"duplicate-causal-receipt",(s,b)=>Replace(b,Receipts(s.Receipts),Receipts(s.Receipts.Concat(new[]{s.Receipts.Last()}))));
        }
        if(args.Length<2 || args[1]!="age-only") {
        Reject(fill,"incorrect-root",(s,b)=>{byte[] old=Text(s.ContentFingerprint);Check(b.Skip(8).Take(old.Length).SequenceEqual(old),"Root is not at its explicit header offset");
            byte[] replacement=Text(s.ContentFingerprint.Substring(0,s.ContentFingerprint.Length-1)+(s.ContentFingerprint.EndsWith("0")?"1":"0"));
            return b.Take(8).Concat(replacement).Concat(b.Skip(8+old.Length)).ToArray();});
        Reject(fill,"incorrect-predecessor",(s,b)=>{byte[] before=Section("OrdinaryMagicCodec",s.OrdinaryMagic);string p=s.OrdinaryMagic.PredecessorFingerprint;
            byte[] after=Replace(before,Text(p),Text(p.Substring(0,p.Length-1)+(p.EndsWith("0")?"1":"0")));return Replace(b,before,after);});
        }
        Reject(done,"changed-ingredient-age-origin",(s,b)=>{var v=s.BloodSpecimen;byte[] before=Section("ConnectedBloodSpecimenCodec",v);
            Check(v.Origin==default(RuleTime),"Unexpected authored ingredient origin");
            int offset=new[]{v.AuthorityId,v.LotId,v.SourceOccurrence,v.RecipeOccurrence}.Sum(x=>Text(x).Length);
            byte[] after=(byte[])before.Clone();Buffer.BlockCopy(BitConverter.GetBytes(1L),0,after,offset,8);
            return Replace(b,before,after);});
        File.WriteAllText(Path.Combine(Dir,"result.json"),JsonSerializer.Serialize(new{status="PASS",cases=Rows,
            scope="Genuine work-control parents, negative-only codec-section construction, recomputed outer and applicable nested checksums, strict live-session rejection. Structural/semantic decode rejection is distinguished from policy replay rejection; no forged save is adopted."},J));
    }
}
