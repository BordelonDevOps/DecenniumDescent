from pathlib import Path
import json, hashlib
root=Path(__file__).resolve().parents[5]; here=Path(__file__).resolve().parent
old=root/'docs/unity/evidence/2026-11-23-tac01-ordinary-magic/support/OrdinaryCompatibility.cs'
s=old.read_text(); s=s[:s.index(' public static void Backup')]+ '\n}\n'
s=s.replace('public static class OrdinaryCompatibility','public static class WorkCompatibility')
original=' static Snapshot S(ConnectedExpeditionSession s)=>(Snapshot)typeof(FoundationCases).GetMethod("ShortRestCapture",BindingFlags.Static|BindingFlags.NonPublic).Invoke(null,new object[]{s});'
capture=' static string CapturePath; static Snapshot S(ConnectedExpeditionSession s){string p=CapturePath+"."+Guid.NewGuid().ToString("N");s.Save(p);var snapshot=new FileSaveStore().Load(p);File.Delete(p);return snapshot;}'
assert original in s; s=s.replace(original,capture)
observe=''' static string Views(ConnectedExpeditionSession s)=>JsonSerializer.Serialize(Enum.GetValues(typeof(ExpeditionSeat)).Cast<ExpeditionSeat>().Select(seat=>new{seat,view=s.View(seat),hero=s.DiscoverCastingCommands(seat,ConnectedExpeditionSession.Hero),companion=s.DiscoverCastingCommands(seat,ConnectedExpeditionSession.Companion)}).ToArray(),J);
'''
s=s.replace(' public static void Run',observe+' public static void Run')
s=s.replace('var rows=new List<object>();','CapturePath=Path.Combine(dir,"capture.ddsave");var rows=new List<object>();')
s=s.replace('var successor=New(116);','string expected=File.ReadAllText(Path.Combine(args[1],"wire"+wire+".views.json"));File.WriteAllText(Path.Combine(dir,"wire"+wire+".before-final-restore.views.json"),Views(replay));replay.Restore(Path.Combine(dir,"wire"+wire+"-continued.ddsave"));File.WriteAllText(Path.Combine(dir,"wire"+wire+".views.json"),Views(replay));File.WriteAllText(Path.Combine(dir,"wire"+wire+".restored-views.json"),Views(restored));Check(Views(restored)==expected&&Views(replay)==expected,"Original-profile strict-restored views/discovery changed wire"+wire);\n    var successor=ConnectedExpeditionSession.StartWithConnectedWorkControl(ClericInitialSelection.AuthoredExample(),ClericRepertoireSelection.AuthoredExample(),ClericMilestoneDeclaration.AuthoredExample(),BishopEntryRecord.Announced());')
s=s.replace('"116 adopted legacy profile"','"Work-control adopted legacy profile"').replace('rejectedBy116=true','rejectedByWorkControl=true,strictRestoredObservationsEqual=true')
s=s.replace('rows.Count==21','rows.Count==22').replace('Incomplete95–115','Incomplete95–116')
(here/'WorkCompatibility.cs').write_text(s)
factory=s[s.index(' static ConnectedExpeditionSession New('):s.index(' static void Replay(')]
baseline='using System;using System.IO;using System.Linq;using System.Text.Json;using Decennium.Foundation;using Decennium.Foundation.Laboratory;\npublic static class BaselineOldViews {\nstatic readonly JsonSerializerOptions J=new JsonSerializerOptions{IncludeFields=true,WriteIndented=true};\n'+factory+observe+''' public static void Run(string dir,string[] args){foreach(var input in JsonDocument.Parse(File.ReadAllText(args[0])).RootElement.EnumerateArray()){int wire=input.GetProperty("wire").GetInt32();var session=New(wire);session.Restore(input.GetProperty("path").GetString());File.WriteAllText(Path.Combine(dir,"wire"+wire+".views.json"),Views(session));}File.WriteAllText(Path.Combine(dir,"result.json"),"{\\"status\\":\\"PASS\\",\\"profiles\\":22}");}
}
'''
(here/'BaselineOldViews.cs').write_text(baseline)
inputs=json.loads((root/'engine/artifacts/ordinary-magic-qualification/candidate-01/authentic-legacy/sources.json').read_text(encoding='utf-8-sig'))
p=root/'engine/artifacts/ordinary-magic-qualification/candidate-02/five-paths-01/TypedUninterrupted/r440.ddsave'
inputs.append({'wire':116,'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'authority':'Accepted OMA Candidate02 actual440-command typed path'})
for row in inputs: assert hashlib.sha256(Path(row['path']).read_bytes()).hexdigest()==row['sha256']
(here/'compatibility-sources.json').write_text(json.dumps(sorted(inputs,key=lambda x:x['wire']),indent=2)+'\n')
print('Prepared22 authentic inputs, public-save compatibility and accepted-runtime observation baseline')
