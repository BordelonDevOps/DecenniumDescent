from __future__ import annotations
import copy, hashlib, json, zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parent; REVIEW=ROOT.parent; REPO=REVIEW.parents[4]
W=ROOT/"W05_W10_WITNESS_452_TESTONLY.json"; V=ROOT/"BUILD_VALIDATION_452.json"; M=ROOT/"MANIFEST_452.json"; A=ROOT/"DD_Fortress_W05_W10_Witness_452_TESTONLY.zip"; D=ROOT/"DELIVERY_452.json"
P=REVIEW/"fortress_w05_w10_joint_preflight_443"/"PG328_W05_W10_JOINT_PROPOSAL_443_TESTONLY.json"; O=REVIEW/"fortress_w05_w10_joint_preflight_443"/"OWNER_PG328_W05_W10_ADOPTION_443_TESTONLY.json"; S=REVIEW/"fortress_w01_structural_damage_witness_403_repack02"/"W01_REPLAY_403.json"
def canon(x): return json.dumps(x,sort_keys=True,separators=(",",":"),ensure_ascii=False).encode("utf-8")
def hbytes(b): return hashlib.sha256(b).hexdigest()
def hfile(p): return hbytes(p.read_bytes())
def hobj(x): return hbytes(canon(x))
def read(p): return json.loads(p.read_text(encoding="utf-8"))
def apply(doc,ops):
    doc=copy.deepcopy(doc)
    for op in ops:
        parts=[p.replace("~1","/").replace("~0","~") for p in op["path"].lstrip("/").split("/")]; parent=doc
        for p in parts[:-1]: parent=parent[int(p)] if isinstance(parent,list) else parent[p]
        leaf=parts[-1]
        if isinstance(parent,list):
            i=int(leaf)
            if op["op"]=="add": parent.insert(i,copy.deepcopy(op["value"]))
            elif op["op"]=="remove": parent.pop(i)
            else: parent[i]=copy.deepcopy(op["value"])
        elif op["op"]=="add": parent[leaf]=copy.deepcopy(op["value"])
        elif op["op"]=="remove": del parent[leaf]
        else: parent[leaf]=copy.deepcopy(op["value"])
    return doc
w=read(W); v=read(V); m=read(M); d=read(D); p=read(P); o=read(O); parent=read(S); tr=w["stateTransitionReplay"]; events=w["eventTrace"]["events"]; initial=parent["stateSnapshots"]["S030"]
checks={}
checks["proposal/adoption exact hashes"]=hfile(P)=="1fd045800181958d34e141763e07fe230a2261a3879e8115869551c2a6d20b85" and o["scope"]["proposalSha256"]==hfile(P)
checks["parent replay/S030 hashes"]=hfile(S)=="2b60ae35d828bd6028d71f202c1dd61c823d6212bb45c7f633ecd8f6b51d44fb" and hobj(initial)==tr["initialStateSha256"]==w["parent"]["snapshotSha256"]
checks["embedded initial state is exact parent S030"]=tr["initialState"]==initial
checks["all source binding hashes match"]=len(w["sourceBindings"])==12 and all(hfile(REPO/x["path"])==x["sha256"]==x["actualSha256"] and x["matches"] for x in w["sourceBindings"])
checks["adopted inputs exact"]=w["adoptedScenario"]==p["ownerProposedInputs"]
checks["event ids/order unique"]=len({x["eventId"] for x in events})==len(events) and events==sorted(events,key=lambda x:(x["timeSeconds"],x["orderAtTime"],x["kind"]))
replay=copy.deepcopy(initial); forward_ok=True
for e in events:
    t=e["stateTransition"]
    if hobj(replay)!=t["beforeStateSha256"]: forward_ok=False; break
    replay=apply(replay,t["forwardOperations"])
    if hobj(replay)!=t["afterStateSha256"]: forward_ok=False; break
checks["forward event-by-event replay reaches exact terminal state"]=forward_ok and replay==tr["terminalState"] and hobj(replay)==tr["terminalStateSha256"]
reverse=copy.deepcopy(replay); inverse_ok=True
for e in reversed(events):
    t=e["stateTransition"]
    if hobj(reverse)!=t["afterStateSha256"]: inverse_ok=False; break
    reverse=apply(reverse,t["inverseOperations"])
    if hobj(reverse)!=t["beforeStateSha256"]: inverse_ok=False; break
checks["inverse event-by-event replay restores exact S030"]=inverse_ok and reverse==initial and hobj(reverse)==tr["reverseRestorationExpectedSha256"]
by={}
for e in events: by.setdefault(e["kind"],[]).append(e)
checks["complete regular markers"]=len(by.get("REGULAR_TURN_START",[]))==80 and len(by.get("REGULAR_TURN_END",[]))==79
checks["nine complete bolt damage/interruption/response sequences"]=len(by.get("ARCANE_BOLT_COMMIT",[]))==9 and sum(x["details"].get("sourceSpell")=="wizard.base.arcane-bolt" for x in by.get("COUNTERSPELL_WINDOW",[]))==9 and all(len(by.get(k,[]))==9 for k in ["ARCANE_BOLT_ATTACK_ROLL","ARCANE_SHIELD_RESPONSE","ARCANE_BOLT_DAMAGE_RESOLUTION"])
checks["Grounding balance uses current, not future, RP"]=[x["details"]["RPAfter"] for x in by["GROUNDING_ACTION"]]==[78,77,76,75,74,73,72,71] and [x["rpAfterBolts"] for x in w["groundingResourceReadings"]]==[78,77,76,75,74,73,72,71]
checks["actual responder eligibility is enumerated"] = by["COUNTERSPELL_WINDOW"][0]["details"]["actualResponderChecks"][0]["eligible"] is False and all(x["details"]["actualResponderChecks"][0]["eligible"] for x in by["COUNTERSPELL_WINDOW"][1:9]) and by["ARCANE_SHIELD_RESPONSE"][0]["details"]["actualResponderChecks"][0]["eligible"] is False and all(x["details"]["actualResponderChecks"][0]["eligible"] for x in by["ARCANE_SHIELD_RESPONSE"][1:])
checks["Wound save and tile release ordered after damage"]=[x["kind"] for x in events if x["timeSeconds"]==109.3 and x["kind"] in ["ARCANE_BOLT_DAMAGE_RESOLUTION","WOUND_SAVE","ZERO_HP_CALLBACKS_AND_TILE_RELEASE"]]==["ARCANE_BOLT_DAMAGE_RESOLUTION","WOUND_SAVE","ZERO_HP_CALLBACKS_AND_TILE_RELEASE"] and by["ZERO_HP_CALLBACKS_AND_TILE_RELEASE"][0]["details"]["tileExpiryPreserved"]==3606.13
checks["three death saves precede Dead state"]=[x["timeSeconds"] for x in by["DEATH_SAVE"]]==[114,120,126] and len(by["A_BECOMES_DEAD"])==1 and by["A_BECOMES_DEAD"][0]["timeSeconds"]==126
checks["Sight resolution after its window"]=[x["kind"] for x in events if x["timeSeconds"]==127.2 and x["kind"] in ["COUNTERSPELL_WINDOW","ARCANE_SIGHT_RESOLUTION"]]==["COUNTERSPELL_WINDOW","ARCANE_SIGHT_RESOLUTION"]
checks["successful Dispel then root, bodies, stable-ID loose items at same time"]=[x["kind"] for x in events if x["timeSeconds"]==133.2 and x["kind"] in ["COUNTERSPELL_WINDOW","DISPEL_MAGIC_SUCCESSFUL_RESOLUTION","FORTRESS_ROOT_TERMINATION","Q27_BODY_CLOSURE_A","Q27_BODY_CLOSURE_B","Q27_LOOSE_ITEM_SETTLEMENT"]]==["COUNTERSPELL_WINDOW","DISPEL_MAGIC_SUCCESSFUL_RESOLUTION","FORTRESS_ROOT_TERMINATION","Q27_BODY_CLOSURE_A","Q27_BODY_CLOSURE_B","Q27_LOOSE_ITEM_SETTLEMENT","Q27_LOOSE_ITEM_SETTLEMENT","Q27_LOOSE_ITEM_SETTLEMENT"]
terminal=tr["terminalState"]; checks["root ended, actors and loose items settled"]=terminal["effects"]["RANK9PLANARGATES5129-CONJURE-DEMIPLANE-FORTRESS-A/cast1"]["active"] is False and terminal["spaces"]["RANK9PLANARGATES5129-CONJURE-DEMIPLANE-FORTRESS-A/cast1/space"]["exists"] is False and [x["details"]["id"] for x in by["Q27_LOOSE_ITEM_SETTLEMENT"]]==w["adoptedScenario"]["localGeometry"]["q27Projection"]["looseItemOrderByStableId"]
checks["spell/resource/concentration/recharge history terminal values"]=terminal["actors"]["B"]["RP"]==66 and terminal["actors"]["B"]["concentration"]["spellId"]=="wizard.arch.arcane-sight" and terminal["actors"]["B"]["recharge"]["wizard.arch.arcane-sight"]==1 and terminal["actors"]["B"]["recharge"]["wizard.arch.dispel-magic"]==2 and len(terminal["actors"]["B"]["spellHistory"])==11 and len(terminal["actors"]["B"]["testOnlySpellEfficiencyHistory"])==11
checks["authority and scope boundary unchanged"]=w["queueAtAdoption"]=={"reviewedApplied":830,"pending":18,"acceptedUnapplied":0,"mutation":False,"identityAcceptedOrApplied":False} and all(x is False for k,x in w["scopeBoundary"].items() if k!="testOnly")
checks["builder validation binds witness"]=v["status"]=="PASS" and v["witnessSha256"]==hfile(W) and v["failed"]==0 and v["passed"]==len(v["checks"])
checks["manifest/delivery/file hashes bind"]=all(hfile(REVIEW/x["path"])==x["sha256"] for x in m["files"]) and d["witnessSha256"]==hfile(W) and d["archiveSha256"]==hfile(A) and d["validationSha256"]==hfile(V)
with zipfile.ZipFile(A) as z: checks["archive integrity and core members"]=z.testzip() is None and {"W05_W10_WITNESS_452_TESTONLY.json","BUILD_VALIDATION_452.json","MANIFEST_452.json"}.issubset(set(z.namelist()))
for name,ok in checks.items(): print(("PASS" if ok else "FAIL")+": "+name)
if not all(checks.values()): raise SystemExit(1)
print(f"PASS: {sum(checks.values())}/{len(checks)} independent checks; TEST_ONLY/unsealed; queue 830/18/0.")
