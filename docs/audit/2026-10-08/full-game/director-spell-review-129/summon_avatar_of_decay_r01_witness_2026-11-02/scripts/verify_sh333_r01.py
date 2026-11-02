import copy,hashlib,json,math,os
from pathlib import Path
O=Path(os.environ["TEMP"])/"r01pkg"
def canonical(x):return json.dumps(x,sort_keys=True,separators=(",",":"),ensure_ascii=False,allow_nan=False).encode()
def sha(b):return hashlib.sha256(b).hexdigest()
def need(ok,msg):
 if not ok:raise AssertionError(msg)
def read(n):return (O/n).read_bytes()
def js(n):return json.loads(read(n))
def decode(s):return s.replace("~1","/").replace("~0","~")
def apply(state,ops):
 x=copy.deepcopy(state)
 for op in ops:
  parts=[decode(v) for v in op["path"].split("/")[1:]]
  parent=x
  for q in parts[:-1]:parent=parent[int(q)] if isinstance(parent,list) else parent[q]
  key=parts[-1];exists=(0<=int(key)<len(parent)) if isinstance(parent,list) else key in parent;target=parent[int(key)] if isinstance(parent,list) and exists else parent.get(key) if isinstance(parent,dict) and exists else None
  if op["op"]=="test":need(target==op["value"],"patch test "+op["path"])
  elif op["op"]=="add":
   if isinstance(parent,list):parent.insert(int(key),copy.deepcopy(op["value"]))
   else:need(key not in parent,"patch add exists "+op["path"]);parent[key]=copy.deepcopy(op["value"])
  elif op["op"]=="replace":
   need(exists,"patch replace absent "+op["path"])
   if isinstance(parent,list):parent[int(key)]=copy.deepcopy(op["value"])
   else:parent[key]=copy.deepcopy(op["value"])
  elif op["op"]=="remove":
   need(exists,"patch remove absent "+op["path"])
   if isinstance(parent,list):del parent[int(key)]
   else:del parent[key]
  else:raise AssertionError("unknown patch operation")
 return x

manifest=js("MEMBER_MANIFEST_410.json")
for m in manifest["members"]:
 raw=read(m["path"]);need(len(raw)==m["bytes"] and sha(raw)==m["sha256"],"manifest "+m["path"])
sb=js("SOURCE_BINDINGS_410.json");proposal=js("PROPOSAL_REPACK03_TESTONLY.json")
for b in sb["bindings"]:
 raw=read(b["member"]);need(len(raw)==b["bytes"] and sha(raw)==b["sha256"],"source "+b["member"])
for i,pb in enumerate(proposal["bindings"]):
 b=next(x for x in sb["bindings"] if x.get("proposalBindingIndex")==i)
 need((b["repositoryPath"],b["bytes"],b["sha256"])==(pb["path"],pb["bytes"],pb["sha256"]),"binding pointer "+str(i))
fixture_binding=next(x for x in sb["bindings"] if x.get("proposalBindingIndex")==3)
fixture=js(fixture_binding["member"])
need(sha(canonical(fixture["initialState"]))==fixture["initialSHA256"],"fixture initial checksum")
ad=js("OWNER_ADOPTION_SH333_R01_REPACK03_TESTONLY.json")
proposal_raw=read("PROPOSAL_REPACK03_TESTONLY.json")
need(sha(proposal_raw)==ad["adoptedProposal"]["sha256"]=="35e602db0b0d8939092c793165a293983bd7d61a7f18f0747a93d94fa1f903e3","adopted proposal")
need(ad["scope"]["branchId"]=="SH333-R01" and ad["scope"]["endpointTick"]==2110,"adoption scope")
need("no verbatim R01-specific user reply" in ad["recordingBasis"]["kind"],"recording basis transparency")
auth=js("AUTHORIZATION_AND_SCOPE_410.json")
need(auth["explicitNonClaims"] and auth["currentAuthority"]["pending"]==15,"authority boundaries")
queue=js("sources/CURRENT_SPELL_QUEUE_478.json")
need(queue["currentAuthority"]=={"reviewedApplied":833,"pending":15,"acceptedUnapplied":0,"completeStandaloneProcedures":557,"scopedInterfaces":173},"Queue478 counts")
need(queue["nextIdentity"]=="summon-avatar-of-decay" and queue["nextBlockerIds"]==["SH202-B03"],"Queue478 next")
readback=js("sources/DIRECTOR_READBACK_SH333_R01_REPACK03_QUEUE478_01.json")
confirmation=js("sources/DIRECTOR_CONFIRMATION_SH333_R01_REPACK03_QUEUE478_01.json")
need(readback["directorReadback"]["proposalSha256"]==ad["adoptedProposal"]["sha256"],"Director readiness proposal hash")
need(readback["directorReadback"]["sourceBindingsDeclared"]==12 and readback["directorReadback"]["sourceBindingsMatched"]==12,"Director source binding readback")
need(confirmation["directorConfirmation"]["decision"]=="READY_FOR_OWNER_ADOPTION_REMAINS_VALID","Director confirmation")
initial_doc=js("INITIAL_410.json");initial=initial_doc["state"];snap=js("SNAPSHOTS_410.json");events=js("EVENTS_410.json");expected=js("EXPECTED_TERMINAL_410.json")
need(initial_doc["sha256"]==sha(canonical(initial)),"initial hash")
parent=copy.deepcopy(fixture["initialState"]["world"]);parent_hash=sha(canonical(fixture["initialState"]))
need(initial["parentProjection"]["fixtureInitialSHA256"]==parent_hash,"parent state binding")
need(initial["parentProjection"]["fixtureWorldInitial"]==parent,"parent world unchanged in projection")
parent["actors"]["C"]["pos"]=[45,-5,0]
need(initial["world"]==parent,"initial projection has only adopted C-position override")
need(initial["tick"]==300 and initial["worldElapsedSeconds"]==3.0,"branch initial tick")
need(len(events)==51 and len(snap)==52,"chronology cardinality")
need(snap["S000"]==initial,"snapshot initial")
cursor=copy.deepcopy(initial)
sequence_ids=[]
for i,e in enumerate(events):
 sid=f"S{i:03d}";tid=f"S{i+1:03d}"
 need(e["beforeStateId"]==sid and e["afterStateId"]==tid,"event order "+str(i))
 need(cursor==snap[sid] and sha(canonical(cursor))==e["beforeSHA256"],"before state "+str(i))
 cursor=apply(cursor,e["forward"])
 need(cursor==snap[tid] and sha(canonical(cursor))==e["afterSHA256"],"forward replay "+str(i))
 if e["evidence"]["proposalSequence"] is not None:
  sequence_ids.append(proposal["sequence"].index(e["evidence"]["proposalSequence"]))
need(sequence_ids==list(range(31)),"proposal sequence coverage")
need(cursor==expected["state"] and sha(canonical(cursor))==expected["sha256"],"terminal match")
reverse=copy.deepcopy(cursor)
for i in range(len(events)-1,-1,-1):
 e=events[i];need(reverse==snap[e["afterStateId"]],"inverse after "+str(i))
 reverse=apply(reverse,e["inverse"])
 need(reverse==snap[e["beforeStateId"]],"inverse replay "+str(i))
need(reverse==initial and sha(canonical(reverse))==initial_doc["sha256"],"full reverse restoration")
w=cursor["world"];a=w["actors"];b=w["bodies"]
need((a["N1"]["RP"],a["N1"]["dissonance"],a["N1"]["refrain"])==(52,0,0),"N1 resource terminal")
need(a["N1"]["recharge"]["wizard.hero.necromancer.mental-binding"]==0,"Mental Binding recharge")
need(a["N1"]["concentration"] is None and a["F"]["conditions"]==[],"concentration/Charm expiry")
need((a["B"]["HP"],a["B"]["pos"])==(83,[40,-10,0]),"B aura/movement")
need(a["C"]["HP"]==102 and a["F"]["HP"]==9,"relay3/fire settlement")
need((b["N2:cast1:minion"]["HP"],b["N2:cast1:minion"]["pos"])==(51,[35,-20,0]),"Zombie aura settlement")
need(b["A:cast1:body1"]["HP"]==267,"Decay body unchanged")
need(b["A:cast1:body1"]["auraConsumed"]==["B:100","B:600","N2:cast1:minion:600","N2:cast1:minion:1200"],"aura consumed markers")
need(w["relations"]["relay:1"]["status"]=="resolved" and w["relations"]["relay:2"]["status"]=="resolved" and w["relations"]["relay:3"]["status"]=="resolved","relay status")
need(w["orders"]["order:2"]["status"]=="expired-unexecuted","losing order expiry")
need(w["hardGuards"]=={"A:N1:cast1:minion:encounter":True,"A:N2:cast1:minion:encounter":True,"A:F:encounter":True},"shared guards")
need(b["N1:cast1:minion"]["offenseHistory"][-1]["tick"]==390 and b["N1:cast2:minion"]["Dodge"],"N1 attached control/offense phase")
need(b["N2:cast1:minion"]["offenseHistory"][-1]["tick"]==490 and b["N2:cast2:minion"]["Dodge"],"N2 attached control/offense phase")
need(a["F"]["offenseHistory"][-1]["tick"]==510 and a["F"]["offenseHistory"][-1]["target"]=="C","F relay attack ledger")
# Independent nearest-AABB geometry: x/y are centered; z is floor elevation.
def gap(pa,ba,pb,bb):
 dx=max(abs(pa[0]-pb[0])-(ba[0]+bb[0])/2,0);dy=max(abs(pa[1]-pb[1])-(ba[1]+bb[1])/2,0)
 za=(pa[2],pa[2]+ba[2]);zb=(pb[2],pb[2]+bb[2]);dz=max(za[0]-zb[1],zb[0]-za[1],0)
 return math.sqrt(dx*dx+dy*dy+dz*dz)
bodypos=b["A:cast1:body1"]["pos"];bodybox=b["A:cast1:body1"]["box"]
need(gap([30,-20,0],[5,5,6],bodypos,bodybox)==2.5,"B initial gap")
need(gap([35,-20,0],[5,5,5],bodypos,bodybox)==7.5,"Zombie gap")
endgap=gap([40,-10,0],[5,5,6],bodypos,bodybox)
need(abs(endgap-math.sqrt(12.5**2+2.5**2))<1e-12 and endgap>10,"B endpoint gap")
led=js("CAST_CONTROL_RESOURCE_LEDGER_410.json")
need([x["tick"] for x in led["conditionSavesAndExpiry"] if x.get("actor")=="F"]==[580,1180,1780],"F repeat save schedule")
need([x["response"] for x in led["counterspell"][0]["responses"]]==["declined"]*4,"Counterspell declines")
report={"id":"SH333-R01-INDEPENDENT-VERIFICATION-410","result":"PASS","classification":"CONDITIONAL_TEST_ONLY",
 "checks":{"memberManifest":len(manifest["members"]),"proposalSourceBindings":12,"events":len(events),"forwardReplay":True,"fullInverseRestoration":True,
 "proposalSequenceEntries":len(sequence_ids),"branchInitialProjection":True,"terminalState":True,"geometry":True,"queueAuthority":True},
 "initialSHA256":sha(canonical(initial)),"terminalSHA256":sha(canonical(cursor)),"currentMainCommit":auth["currentAuthority"]["mainCommit"],
 "queue":{"applied":833,"pending":15,"acceptedUnapplied":0,"next":"summon-avatar-of-decay / SH202-B03"},
 "scope":"Independent source-byte checks, event patch replay/reversal, position geometry and terminal ledger checks. No game runtime execution, seal, blocker closure or identity disposition."}
(O/"VERIFICATION_410.json").write_bytes(json.dumps(report,indent=2,ensure_ascii=False).encode()+b"\n")
print(json.dumps(report,indent=2))
