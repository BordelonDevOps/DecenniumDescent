using System;using System.IO;using System.Linq;using System.Reflection;using System.Text.Json;using Decennium.Foundation;using Decennium.Foundation.Laboratory;using Decennium.Foundation.Tests;
public static class PartitionProbe {
 static readonly JsonSerializerOptions J=Options();
 static JsonSerializerOptions Options(){var resolver=new System.Text.Json.Serialization.Metadata.DefaultJsonTypeInfoResolver();resolver.Modifiers.Add(info=>{if(info.Type==typeof(ResourceLot)||info.Type==typeof(ResourceReservation)){var legacy=info.Properties.SingleOrDefault(x=>x.Name=="Quantity");if(legacy!=null)info.Properties.Remove(legacy);}});return new JsonSerializerOptions{IncludeFields=true,WriteIndented=true,TypeInfoResolver=resolver};}
 static Snapshot S(ConnectedExpeditionSession s)=>(Snapshot)typeof(FoundationCases).GetMethod("ShortRestCapture",BindingFlags.Static|BindingFlags.NonPublic).Invoke(null,new object[]{s});
 static ConnectedExpeditionSession New()=>ConnectedExpeditionSession.StartWithOrdinaryMagicalActivity(ClericInitialSelection.AuthoredExample(),ClericRepertoireSelection.AuthoredExample(),ClericMilestoneDeclaration.AuthoredExample(),BishopEntryRecord.Announced());
 static void Check(bool ok,string why){if(!ok)throw new Exception(why);}
 static void Save(ConnectedExpeditionSession s,string path){var bytes=new SnapshotCodec().Encode(S(s));s.Save(path);s.Restore(path);Check(bytes.SequenceEqual(new SnapshotCodec().Encode(S(s))),"Restore changed bytes");File.WriteAllText(path+".json",JsonSerializer.Serialize(S(s),J));}
 static void Advance(ConnectedExpeditionSession s,int seconds,string id){var before=S(s);var r=s.SubmitSessionCommand(new Command(id,ConnectedExpeditionSession.Hero,before.Revision,CommandKind.AdvanceClock,x:seconds,y:1));Check(r.Response==ExpeditionResponse.Committed,"Advance "+id+" "+r.Response);}
 public static void Run(string dir,string[] args){
   var result=FoundationCases.Run("tac01_ordinary_magic_consumed_strain_sparse_partition_regression",dir);File.WriteAllText(Path.Combine(dir,"focused-result.json"),JsonSerializer.Serialize(result,J));Check(result.Passed,result.Error);
   Continue(dir,new[]{dir});
 }
 public static void Continue(string dir,string[] args){
   if(args[0]!=dir)foreach(var name in new[]{"sparse-whole-after.ddsave","sparse-partitioned-after.ddsave","focused-result.json"})File.Copy(Path.Combine(args[0],name),Path.Combine(dir,name));
   foreach(var name in new[]{"sparse-whole-after","sparse-partitioned-after"}){var state=new FileSaveStore().Load(Path.Combine(dir,name+".ddsave"));File.WriteAllText(Path.Combine(dir,name+".json"),JsonSerializer.Serialize(state,J));}
   var whole=New();whole.Restore(Path.Combine(dir,"sparse-whole-after.ddsave"));var parts=New();parts.Restore(Path.Combine(dir,"sparse-whole-after.ddsave"));
   Advance(whole,28800,"oma.partition.long.whole");for(int i=0;i<8;i++)Advance(parts,3600,"oma.partition.long.part."+i);
   Save(whole,Path.Combine(dir,"eight-hour-whole.ddsave"));Save(parts,Path.Combine(dir,"eight-hour-parts.ddsave"));
   File.WriteAllText(Path.Combine(dir,"result.json"),JsonSerializer.Serialize(new{status="EXECUTIONS_PASS_COMPARISON_PENDING",scope="Complete raw snapshots and distinct histories retained; normalized comparison is separate."},J));
 }
}
