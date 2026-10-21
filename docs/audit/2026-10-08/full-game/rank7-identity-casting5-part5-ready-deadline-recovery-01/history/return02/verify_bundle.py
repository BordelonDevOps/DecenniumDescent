#!/usr/bin/env python3
"""Read-only archival, source, full-value and fixture verification; imports no project code."""
from pathlib import Path,PurePosixPath
import json,zipfile,hashlib,copy,ast,argparse,io
ROOT=Path(__file__).resolve().parent
def enc(x):return (json.dumps(x,ensure_ascii=False,indent=2)+"\n").encode("utf-8")
def sha(b):return hashlib.sha256(b).hexdigest()
def get(x,p):
 for k in p.split("/")[1:] if p else []:
  k=k.replace("~1","/").replace("~0","~")
  x=x[int(k)] if isinstance(x,list) else x[k]
 return x
def put(x,o,reverse=False):
 parts=o["pointer"].split("/")[1:];p=x
 for k in parts[:-1]:
  k=k.replace("~1","/").replace("~0","~")
  p=p[int(k)] if isinstance(p,list) else p[k]
 k=parts[-1].replace("~1","/").replace("~0","~");k=int(k) if isinstance(p,list) else k
 present=(k in p) if isinstance(p,dict) else 0<=k<len(p)
 exists=o["afterExists"] if reverse else o["beforeExists"]
 if present!=exists:raise ValueError("Pointer presence drift: "+o["pointer"])
 old=o["after"] if reverse else o["before"]
 if exists and p[k]!=old:raise ValueError("Full before-value drift: "+o["pointer"])
 exists=o["beforeExists"] if reverse else o["afterExists"]
 if exists:p[k]=copy.deepcopy(o["before"] if reverse else o["after"])
 else:del p[k]
def diff(a,b,p=""):
 if type(a)!=type(b):return [p]
 if isinstance(a,dict):
  out=[]
  for k in a.keys()|b.keys():
   q=p+"/"+str(k)
   if k not in a or k not in b:out.append(q)
   else:out+=diff(a[k],b[k],q)
  return out
 if isinstance(a,list):
  if len(a)!=len(b):return [p]
  return [q for i,(x,y) in enumerate(zip(a,b)) for q in diff(x,y,p+"/"+str(i))]
 return [] if a==b else [p]
def main():
 ap=argparse.ArgumentParser();ap.add_argument("--report",type=Path,required=True);ap.add_argument("--manifest",action="store_true");a=ap.parse_args()
 if a.report.exists():raise SystemExit("Preserve existing report: choose a new output")
 checks=[]
 def ck(name,ok,category="source/structure"):
  checks.append({"id":name,"category":category,"pass":bool(ok)})
  if not ok:raise AssertionError(name)
 def read(name):return json.loads((ROOT/name).read_bytes())
 def zcheck(z,label):
  ns=z.namelist()
  ck(label+" safe/unique",len(ns)==len(set(ns)) and all(not PurePosixPath(n).is_absolute() and ".." not in PurePosixPath(n).parts and "\\" not in n and ":" not in n for n in ns))
  ck(label+" CRC",z.testzip() is None)
  return ns
 def bound(b,r):return len(b)==r["bytes"] and sha(b)==r["sha256"]
 localname="DD_Rank7_Identity_Casting5_Local_Corrections_01.zip"
 lb=(ROOT/"inputs"/localname).read_bytes()
 ck("Incoming archive exact",len(lb)==14757388 and sha(lb)=="bbc7ed5790a0b287a43e324f545d473066dd0584328b3904b49db2563b7bd5f5")
 with zipfile.ZipFile(io.BytesIO(lb)) as local:
  ck("Incoming14 members",len(zcheck(local,"incoming"))==14)
  for r in json.loads(local.read("MANIFEST.json"))["files"]:ck("incoming member "+r["path"],bound(local.read(r["path"]),r))
  oldraw=local.read("input/DD_Rank7_Identity_Casting_5_Part5_Conference_Return_01.zip")
  ck("Complete Return01 exact",len(oldraw)==14578890 and sha(oldraw)=="cdc2b871521cdb2c33bb2b23932d5fcb25dcb486e794e826c637d48d10beb5b7")
  with zipfile.ZipFile(io.BytesIO(oldraw)) as old:
   ck("Return01 51 members",len(zcheck(old,"Return01"))==51)
   for r in json.loads(old.read("MANIFEST.json"))["files"]:ck("Return01 member "+r["path"],bound(old.read(r["path"]),r))
   braw=old.read("MODEL.json");base=json.loads(braw)
   ck("Return01 model exact anchor",len(braw)==11968546 and sha(braw)=="2cd09a244b6f49a6aa1240ed295470bcbdaff8df038bb51092756849a47ef2f5")
   ck("Full baseline copy",braw==(ROOT/"baseline/RETURN01_MODEL.json").read_bytes())
   sr=old.read("inputs/DD_Rank7_Identity_Casting_5_Source_Conference_01.zip")
   ck("Original conference retained",sr==(ROOT/"inputs/DD_Rank7_Identity_Casting_5_Source_Conference_01.zip").read_bytes() and len(sr)==4534073 and sha(sr)=="fad1e1d4b5146782305d94f62194f8856300dde461a2aec4ef1b5b37e61490ec")
   with zipfile.ZipFile(io.BytesIO(sr)) as source:
    ck("Original source72 members",len(zcheck(source,"source"))==72)
    entries=json.loads(source.read("MANIFEST.json"))["files"];ck("68 full source bindings",len(entries)==68)
    sources={}
    for r in entries:
     data=source.read("sources/"+r["path"]);sources[r["path"]]=data
     ck("native source "+r["path"],bound(data,r))
     text=data.decode("utf-16") if data.startswith((b"\xff\xfe",b"\xfe\xff")) else data.decode("utf-8-sig")
     ck("readable full source "+r["path"],bool(text))
     if r["path"].endswith(".json"):json.loads(text);ck("JSON parse "+r["path"],True)
     elif r["path"].endswith(".py"):ast.parse(text);ck("syntax only "+r["path"],True)
    for r in json.loads(local.read("LOCAL_SEMANTIC_REVIEW.json"))["sourceBindings"]:
     data=local.read("sources/"+r["path"])
     ck("supplement source "+r["path"],bound(data,r) and (ROOT/"sources"/r["path"]).read_bytes()==data)
     if r["path"] in sources:ck("unchanged overlap "+r["path"],data==sources[r["path"]])
     else:ck("new actual advancement source",r["path"].endswith("CHARACTER_CREATION_PLAYTEST.md"))
    for r in read("CONTEXT_BINDINGS.json"):
     data=(ROOT/r["path"]).read_bytes()
     ck("full context "+r["path"],bound(data,r) and data==old.read(r["path"]))
    m=read("MODEL.json");mraw=(ROOT/"MODEL.json").read_bytes()
    ck("stable complete serialization",enc(m)==mraw)
    for planfile,raw in [("EXACT_OPERATIONS_FROM_RETURN01.json",braw),("EXACT_OPERATIONS_FROM_SOURCE.json",source.read("CANDIDATE.json"))]:
     plan=read(planfile);ck("plan count "+planfile,len(plan["operations"])==plan["operationCount"])
     ck("plan successor "+planfile,bound(mraw,plan["successor"]))
     doc=json.loads(raw)
     for op in plan["operations"]:put(doc,op);ck("forward "+planfile+op["pointer"],True,"full-value replay")
     ck("full forward "+planfile,enc(doc)==mraw,"full-value replay")
     for op in reversed(plan["operations"]):put(doc,op,True);ck("reverse "+planfile+op["pointer"],True,"full-value replay")
     ck("full reverse "+planfile,enc(doc)==raw,"full-value replay")
    oldops=json.loads(old.read("EXACT_OPERATIONS_FROM_SOURCE.json"))["operations"]
    ck("Original27 operations unchanged prefix",read("EXACT_OPERATIONS_FROM_SOURCE.json")["operations"][:27]==oldops)
    for k in base:
     if k not in ("id","status","currentVectors"):ck("complete original root unchanged "+k,m[k]==base[k],"preservation")
    for i,r in enumerate(m["records"]):
     ck("full native/access/procedure "+r["spellId"],r==base["records"][i],"preservation")
     ck("risk C "+r["spellId"],r["riskTier"]=="C")
     for fn in ["PLAYER_CHAPTER.md","DIRECTOR_REVIEW.md"]:
      ck("full procedure rendered "+r["spellId"]+fn,r["proposedProcedure"] in (ROOT/fn).read_text())
    for shared in m["selectedSharedRules"]:
     for fn in ["PLAYER_CHAPTER.md","DIRECTOR_REVIEW.md"]:ck("shared rendering "+shared["id"]+fn,shared["wording"] in (ROOT/fn).read_text())
    for fn in ["SPELL_DISPOSITIONS.json","QUESTION_DISPOSITIONS.json","DI7_COMPARISON.json","HOLD_REGISTER.json","CLOCK_AND_BODY_MATRIX.json","DECISIONS.md"]:
     ck("complete unchanged mirror/history "+fn,(ROOT/fn).read_bytes()==old.read(fn),"preservation")
    ck("11 conditional records unchanged",len(m["conditionalBranchRegister"])==11 and m["conditionalBranchRegister"]==base["conditionalBranchRegister"])
    cd=read("CASE_DISPOSITIONS.json");ck("complete current case mirror",cd["cases"]==m["currentVectors"])
    ck("complete current evidence mirror",read("evidence/worked_cases.json")==m["currentVectors"])
    ck("prior raw evidence known historical mismatch",json.loads(old.read("evidence/worked_cases.json"))!=base["currentVectors"])
    prof=read("ACTOR_FEATURE_ACCOUNTING.json")["profiles"]
    ck("profile mirror",prof==read("evidence/actor_profiles.json"))
    origprof=json.loads(old.read("ACTOR_FEATURE_ACCOUNTING.json"))["profiles"]
    for key,val in origprof.items():ck("base profile exact "+key,prof[key]==val)
    allc={x["id"]:x for c in m["currentVectors"] for x in [c]+c["independentBranches"]}
    oldc={x["id"]:x for c in base["currentVectors"] for x in [c]+c["independentBranches"]}
    ck("ten mains thirtynine branches same IDs",len(m["currentVectors"])==10 and len(allc)==49 and set(allc)==set(oldc))
    ck("same eleven conditional branch flags",sum(c["disposition"].startswith("CONDITIONAL") for c in allc.values())==11)
    ch=[c["id"] for c in m["currentVectors"] if c!=oldc[c["id"]]]
    af=read("AFFECTED_CASES.json")
    ck("complete affected record list",ch==[r["caseId"] for r in af["cases"]])
    for r in af["cases"]:ck("full before/after "+r["caseId"],r["before"]==oldc[r["caseId"]] and r["after"]==allc[r["caseId"]])
    allowedcadence={"action","bonusAction","reaction","regularStart","nextRegularStart","counterRecharge","movementSpent","companionCommandUsed","companionOffenseUsed"}
    actorseen=set()
    for c in allc.values():
     previous=c["initialState"]
     ck("terminal full equality "+c["id"],c["timeline"][-1]["after"]==c["expectedFinalState"])
     ck("ordered event times "+c["id"],[e["timeSeconds"] for e in c["timeline"]]==sorted(e["timeSeconds"] for e in c["timeline"]))
     for idx,e in enumerate(c["timeline"]):
      d=diff(previous,e["before"])
      ck("no unexplained noncadence gap "+c["id"]+str(idx),all(p.startswith("/actors/") and p.split("/")[-1] in allowedcadence for p in d))
      for who,p in previous["actors"].items():
       q=e["before"]["actors"][who]
       if not p["action"] and q["action"]:ck("real START before Action refill "+c["id"]+str(idx)+who,q["regularStart"]>p["regularStart"])
      starts=e.get("regularStartsBeforeEvent",[])
      ck("no repeated START record "+c["id"]+str(idx),len([r["actor"] for r in starts])==len({r["actor"] for r in starts}))
      for side in ("before","after"):
       ck("actor bounds "+c["id"]+str(idx)+side,all(0<=s["hp"]<=s["maxHp"] and 0<=s["rp"]<=s["maxRp"] and s["tempHp"]>=0 for s in e[side]["actors"].values()))
      previous=e["after"]
     for who,p in c["actorDefinitions"].items():
      ck("full class engine untouched "+c["id"]+who,p["completeEngine"]==oldc[c["id"]]["actorDefinitions"][who]["completeEngine"],"preservation")
      key=sha(enc(p))
      if key in actorseen:continue
      actorseen.add(key)
      cls=json.loads(sources[p["source"]["path"]])
      pb=2+(p["totalLevel"]-1)//4;mod=(p["INT"]-10)//2
      ck("actor natural saves "+key,all(p["saves"][k]==(p[k]-10)//2+(pb if k in ("INT","WIS") else 0) for k in ["STR","DEX","CON","INT","WIS","CHA"]))
      ck("actor source RP/rank/DC "+key,(p["maxRp"],p["maxRank"],p["spellDc"],p["PB"],p["Limit"])==(cls["rpByClassLevel"][12],cls["maxSpellRankByClassLevel"][12],8+pb+mod,pb,max(4,2+pb+mod)))
      cards={a["id"]:a for a in cls["cards"]};sched={a["classLevel"]:a for a in cls["schedule"]};seen=set()
      for row in p["selectedAcquisition"]:
       ck("selection quota "+key+str(row["classLevel"]),len(row["cards"])==sched[row["classLevel"]]["choose"])
       for card in row["cards"]:
        ck("actual selected full card "+key+card["id"],cards[card["id"]]==card and card["minimumClassLevel"]<=row["classLevel"] and card["id"] not in seen)
        seen.add(card["id"])
      for card in p["automaticCards"]:ck("actual automatic full card "+key+card["id"],card==cards[card["id"]] and card["minimumClassLevel"]<=13)
    adept=json.loads(sources["DescentReviewChanges/ReviewBible/data/director/feat_candidates/exact_01/cohorts/magic_core.json"])["records"][21]
    for cid,who,pid in [("RIC5-02-B-a","wizard","W13I_ADEPT_C12"),("RIC5-02-B-b","mage","M13L_SCULPT_ADEPT_C12")]:
     p=allc[cid]["actorDefinitions"][who]
     ck("full exact new actor mirror "+pid,prof[pid]==p)
     ck("legal class12 instead of score "+pid,"Metamagic Adept" in p["asiHistory"]["class12"] and p["CHA"]==8 and p["saves"]["CHA"]==-1)
     ck("full feat source remains unchanged/disabled "+pid,p["featAcquisition"]["completeSourceRecordUnchanged"]==adept and adept["selectionEnabled"] is False)
     ck("actual two modes "+pid,p["featAcquisition"]["chosenModes"]==["Reach","Sculpt"])
     for state in [allc[cid]["initialState"],allc[cid]["expectedFinalState"]]+[e[s] for e in allc[cid]["timeline"] for s in ("before","after")]:
      ck("consistent actor profile "+pid+str(state["actors"][who]["rp"]),state["actors"][who]["profile"]==pid)
    au=read("ACTION_AUDIT.json")
    ck("complete event audit121",len(au["events"])==121)
    ck("44 real Action commitments",sum(len(r["ordinaryActionsCommitted"]) for r in au["events"])==44)
    for row in au["events"]:
     c=allc[row["caseId"]];i=row["eventIndex"];e=c["timeline"][i]
     ck("whole ledger audit "+row["caseId"]+str(i),row["actorLedgerStates"]=={who:{"before":{k:s[k] for k in ["action","bonusAction","reaction","regularStart","nextRegularStart"]},"after":{k:e["after"]["actors"][who][k] for k in ["action","bonusAction","reaction","regularStart","nextRegularStart"]}} for who,s in e["before"]["actors"].items()})
     for who in row["ordinaryActionsCommitted"]:
      ck("Action debit "+row["caseId"]+str(i)+who,e["before"]["actors"][who]["action"] and not e["after"]["actors"][who]["action"])
      st=e["after"]["actors"][who]["regularStart"]
      for j in range(i+1,len(c["timeline"])):
       later=c["timeline"][j]
       if later["before"]["actors"][who]["regularStart"]!=st:break
       ck("spent propagates "+row["caseId"]+str(i)+"/"+str(j)+who,all(not later[s]["actors"][who]["action"] for s in ("before","after") if later[s]["actors"][who]["regularStart"]==st))
    d=read("TARGETED_DIAGNOSTIC_EVIDENCE.json")
    ck("eleven failures reproduced then fixed",sum(not r["pass"] for r in d["before"])==11 and all(r["pass"] for r in d["after"]))
    er=allc["RIC5-03-B-a"]["expectedFinalState"]["actors"]["caster"]
    ck("Erase actual first history/D preserved",(er["rp"],er["dissonance"],er["lastSpell"],er["refrain"],er["preparedFamiliesUsed"])==(31,0,"erase-from-reality",0,["erase-from-reality"]))
    ne=read("NUMERICAL_STATE_EVIDENCE.json")
    ck("next repeat source arithmetic",ne["erase"]["nextCastAfter"]["rp"]==31-17 and ne["erase"]["nextCastAfter"]["dissonance"]==2+1)
    e=allc["RIC5-02-A-a"]["timeline"][2]
    ck("Ready after Surge before original START",60.5<e["timeSeconds"]==60.9<e["before"]["actors"]["mage"]["nextRegularStart"]==61)
    ck("Ready no Action refresh",e["regularStartsBeforeEvent"]==[] and not e["before"]["actors"]["mage"]["action"] and not e["after"]["actors"]["mage"]["action"])
    if (ROOT/"ARTIFACT_OPERATIONS_FROM_RETURN01.json").exists():
     ao=read("ARTIFACT_OPERATIONS_FROM_RETURN01.json")
     for op in ao["operations"]:
      b=old.read(op["path"]);now=(ROOT/op["path"]).read_bytes()
      ck("full artifact before "+op["path"],b==op["beforeText"].encode("utf-8") and bound(b,op["beforeBinding"]),"artifact replay")
      ck("full artifact after "+op["path"],now==op["afterText"].encode("utf-8") and bound(now,op["afterBinding"]),"artifact replay")
      ck("artifact reverse complete "+op["path"],op["beforeText"].encode("utf-8")==b,"artifact replay")
    spec=read("SPECIFICATION_REPORT.json");ck("isolated report no engine",spec["failures"]==spec["errors"]==0 and spec["projectRuntimeTests"]==0)
    ck("counts and adoption remain",m["newRuleAdoptions"]==0 and m["runtimeTestsExecuted"]==0 and not m["wholeGameComplete"] and m["correctionConference02"]["unchangedCounts"]=={"reviewed":525,"pending":323,"standalone":249,"interfaces":173,"acceptedButUnapplied":39})
 if a.manifest:
  mf=read("MANIFEST.json")
  for item in mf["files"]:ck("return member "+item["path"],bound((ROOT/item["path"]).read_bytes(),item),"return manifest")
 out={"id":"RIC5-CORRECTION02-READONLY-VERIFICATION","scope":"Source bytes, exact operations, full mirrors, preservation and declared finite fixture states; no project runtime or local diagnostic script execution.",
      "checkCount":len(checks),"failures":sum(not r["pass"] for r in checks),"runtimeTestsExecuted":0,"checks":checks}
 a.report.write_bytes(enc(out))
 print(json.dumps({"checks":out["checkCount"],"failures":out["failures"],"manifest":a.manifest}))
if __name__=="__main__":main()
