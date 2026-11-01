#!/usr/bin/env python3
"""Build the owner-authorized, reversible TEST_ONLY PG328-W09-R1 witness."""
from __future__ import annotations
import copy, hashlib, json, math, shutil, zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[6]
BASE = ROOT / "docs/audit/2026-10-08/full-game/director-spell-review-129"
OWNER = BASE / "fortress_w09_owner_adoption_427/OWNER_PG328_W09_SUPPORT_ADOPTION_427_TESTONLY.json"
PROPOSAL = BASE / "fortress_w09_owner_proposal_426_repack01/OWNER_PROPOSAL_W09_426_REPACK01_TESTONLY.json"
PREFLIGHT = BASE / "fortress_w09_owner_proposal_426_repack01/GEOMETRY_PREFLIGHT_W09_426_REPACK01_TESTONLY.json"
READBACK = BASE / "fortress_w09_owner_proposal_426_repack01/DIRECTOR_READBACK_426_REPACK01.json"
PARENT = BASE / "fortress_w01_structural_damage_witness_403_repack02/W01_REPLAY_403.json"
GEOMETRY = BASE / "fortress_w01_successor_overlays_425/evidence/GEOMETRY_405.json"
SUPPORT = BASE / "fortress_w01_successor_overlays_425/SUPPORT_OVERLAY_425_TESTONLY.json"
OWNER_W01 = BASE / "fortress_w01_owner_adoption_424/OWNER_PG328_W01_PROPOSALS_ADOPTION_424_TESTONLY.json"
OVERLAY_ZIP = BASE / "fortress_w01_successor_overlays_425/DD_Fortress_W01_Successor_Overlays_425_TESTONLY.zip"
QUEUE = BASE / "CURRENT_SPELL_QUEUE_423_REPACK01.json"
HANDOFF = BASE / "CURRENT_HANDOFF_423_REPACK01.json"
OUT = BASE / "fortress_w09_successor_witness_428"
ARCHIVE = "DD_Fortress_W09_Successor_Witness_428_TESTONLY.zip"


def read_json(p: Path): return json.loads(p.read_text(encoding="utf-8-sig"))
def sha_bytes(b: bytes) -> str: return hashlib.sha256(b).hexdigest()
def sha_file(p: Path) -> str: return sha_bytes(p.read_bytes())
def canonical(v: object) -> bytes: return json.dumps(v, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
def digest(v: object) -> str: return sha_bytes(canonical(v))
def rel(p: Path) -> str: return p.relative_to(ROOT).as_posix()
def num(v): return round(float(v), 9)
def bounds_obj(b): return {"x": b[0:2], "y": b[2:4], "z": b[4:6]}
def l1(a,b): return sum(abs(float(y)-float(x)) for x,y in zip(a,b))
def esc(s): return str(s).replace("~","~0").replace("/","~1")


def diff(a, b, path=""):
    if isinstance(a, dict) and isinstance(b, dict):
        out=[]
        for k in sorted(a.keys()-b.keys()): out.append({"op":"remove","path":path+"/"+esc(k)})
        for k in sorted(b.keys()-a.keys()): out.append({"op":"add","path":path+"/"+esc(k),"value":b[k]})
        for k in sorted(a.keys()&b.keys()): out.extend(diff(a[k],b[k],path+"/"+esc(k)))
        return out
    if isinstance(a, list) and isinstance(b, list) and len(a)==len(b):
        out=[]
        for i,(x,y) in enumerate(zip(a,b)): out.extend(diff(x,y,path+f"/{i}"))
        return out
    if type(a) is type(b) and a == b: return []
    return [{"op":"replace","path":path,"value":b}]


def pointer_parent(doc, pointer):
    toks=[t.replace("~1","/").replace("~0","~") for t in pointer.split("/")[1:]]
    cur=doc
    for t in toks[:-1]: cur=cur[int(t)] if isinstance(cur,list) else cur[t]
    return cur,toks[-1]


def apply_ops(doc, ops):
    doc=copy.deepcopy(doc)
    for op in ops:
        parent,key=pointer_parent(doc,op["path"])
        if op["op"]=="remove":
            if isinstance(parent,list): parent.pop(int(key))
            else: del parent[key]
        elif op["op"] in ("add","replace"):
            if isinstance(parent,list):
                if op["op"]=="add": parent.insert(int(key),copy.deepcopy(op["value"]))
                else: parent[int(key)]=copy.deepcopy(op["value"])
            else: parent[key]=copy.deepcopy(op["value"])
        else: raise ValueError(op)
    return doc


def source_bindings():
    files=[("w09OwnerAdoption",OWNER),("w09Proposal",PROPOSAL),("w09DirectorReadback",READBACK),
           ("w09GeometryPreflight",PREFLIGHT),("w01ParentReplay403",PARENT),("geometry405",GEOMETRY),
           ("supportOverlay425",SUPPORT),("w01OwnerAdoption424",OWNER_W01),
           ("w01OverlayPackage425",OVERLAY_ZIP),("currentQueue423",QUEUE),("currentHandoff423",HANDOFF)]
    return [{"id":name,"path":rel(p),"bytes":p.stat().st_size,"sha256":sha_file(p)} for name,p in files]


def actor_projection(a):
    keys=("id","profile","profileSHA256","class","level","PB","M","S","HP","maxHP","RP","maxRP",
          "Dissonance","Refrain","lastSpell","preparedFamiliesUsed","spellHistory","resourceHistory","concentration",
          "conditions","tempHP","wounds","death","plane","position","size","bodyBox","bodyMassLb","orientation",
          "rootBody","form","AC","speed","hands","voice","focusAccessible","equipment","carriedLoad",
          "carriedWeightLb","action","bonusAction","reaction","movement","regularSchedule","recharge","magicThisTurn",
          "spellEfficiency","knowledgeShield","companionCommandRound","companionOffenseRound","lastArrivedFromPlaneKey",
          "placementConflict","shortRestsSinceLong","lastBeneficialLongRest","arcaneRecoveryUsed","conviction",
          "w01MobileAllowanceRemainingFeet","stance","w01HandState")
    return {k:copy.deepcopy(a[k]) for k in keys if k in a}


def position_at(points, distance):
    left=float(distance)
    for i,(a,b) in enumerate(zip(points,points[1:])):
        d=l1(a,b)
        if left <= d + 1e-9:
            if d==0: return list(b)
            f=max(0.0,min(1.0,left/d))
            return [num(x+(y-x)*f) for x,y in zip(a,b)]
        left-=d
    if abs(left)<=1e-7: return list(points[-1])
    raise ValueError(f"distance {distance} exceeds route")


def route_slice(points, start, end):
    result=[position_at(points,start)]
    cumulative=0.0
    for a,b in zip(points,points[1:]):
        d=l1(a,b); cumulative2=cumulative+d
        if start+1e-9 < cumulative2 < end-1e-9 and d>0: result.append(list(b))
        cumulative=cumulative2
    endpoint=position_at(points,end)
    if result[-1]!=endpoint: result.append(endpoint)
    return result


def main():
    owner=read_json(OWNER); proposal=read_json(PROPOSAL); pre=read_json(PREFLIGHT); rb=read_json(READBACK)
    parent=read_json(PARENT); geom=read_json(GEOMETRY); support=read_json(SUPPORT); queue=read_json(QUEUE)
    assert owner["ownerAuthorization"]["verbatim"]=="Adopt exact W09 proposal"
    assert owner["scope"]["proposalSha256"]==sha_file(PROPOSAL)=="f4dfbf3403c63f603ef188be972c4425cc627309d4fb77cc86934afecd6b8a9d"
    assert rb["proposalSha256"]==owner["scope"]["proposalSha256"]
    assert rb["preflightSha256"]==sha_file(PREFLIGHT)
    assert parent["terminalStateId"]=="S030" and parent["terminalStateSha256"]==pre["inheritedTerminal"]["stateSha256"]
    initial_parent=parent["stateSnapshots"]["S030"]
    assert digest(initial_parent)==parent["terminalStateSha256"]
    assert initial_parent["time"]==12.9 and initial_parent["actors"]["A"]["position"]==[25,6,0]
    assert len(proposal["proposedOwnerAdoption"]["exactTerms"])==9
    assert queue["currentAuthority"]=={"reviewedApplied":830,"pending":18,"acceptedUnapplied":0,"completeStandaloneProcedures":554,"scopedInterfaces":173}

    bindings=source_bindings()
    expected={"w01ParentReplay403":pre["sourceBindings"][0]["sha256"],"geometry405":pre["sourceBindings"][2]["sha256"],"supportOverlay425":pre["sourceBindings"][4]["sha256"]}
    byid={x["id"]:x for x in bindings}
    for k,v in expected.items(): assert byid[k]["sha256"]==v,(k,byid[k]["sha256"],v)
    nav=next(x for x in geom["navigationPaths"] if x["id"]=="keep-flight-0")
    waypoints=pre["route"]["orderedWaypoints"]
    assert waypoints[-1]==nav["positions"][18]
    route=[copy.deepcopy(p) for p in waypoints[:-1]]+copy.deepcopy(nav["positions"][1:19])
    route_total=sum(l1(a,b) for a,b in zip(route,route[1:]))
    assert abs(route_total-100)<1e-8
    target=pre["attackGeometry"]["targetPanelId"]
    panel=next(p for p in geom["panels"] if p["id"]==target)
    assert panel["AC"]==17 and panel["HP"]==60
    dep=copy.deepcopy(pre["supportGraph"]["dependentStairParts"])
    contacts=copy.deepcopy(pre["supportGraph"]["actorFootContactPartsBeforeTargetRemoval"])
    assert len(dep)==18
    support_after_move={18:["origin-ground-face"],24:["origin-ground-face"],
      30:["origin-ground-face","keep-F0-0-2","keep-F0-1-2"],
      36:[x["partId"] for x in contacts]}
    assert support_after_move[36]==["keep-tread-0-9","keep-riser-0-9"]
    geometry_part_ids={x["id"] for x in geom["panels"]}
    assert {part_id for ids in support_after_move.values() for part_id in ids} <= geometry_part_ids
    assert {"keep-tread-0-1","keep-riser-0-1"} <= geometry_part_ids

    actors={k:actor_projection(v) for k,v in initial_parent["actors"].items()}
    tile_id="PG328-W01-403:CLAY-TILE-1"
    tile_source=copy.deepcopy(initial_parent["items"][tile_id])
    inherited_bounds=[tile_source["heldBoundsFeet"]["x"][0],tile_source["heldBoundsFeet"]["x"][1],
                      tile_source["heldBoundsFeet"]["y"][0],tile_source["heldBoundsFeet"]["y"][1],
                      tile_source["heldBoundsFeet"]["z"][0],tile_source["heldBoundsFeet"]["z"][1]]
    fortress={"branchId":"PG328-W09-R1","classification":"TEST_ONLY_BRANCH_STRUCTURAL_LEDGER",
      "geometryPath":rel(GEOMETRY),"geometrySha256":sha_file(GEOMETRY),
      "supportOverlayPath":rel(SUPPORT),"supportOverlaySha256":sha_file(SUPPORT),
      "rootId":"origin-ground-face","targetPanel":{"id":target,"boundsFeet":pre["attackGeometry"]["targetBoundsFeet"],"ac":17,"hp":60,"originalHp":60,"destroyed":False},
      "dependentStairPartsOnTargetRemoval":dep,"destroyedParts":[],
      "actorABottomSupportPartIds":["origin-ground-face"],"actorAHasBottomSupport":True,
      "historicalW01SouthPanelHp":55,"routeTotalFeet":100,"routeProgressFeet":0,"movementLegs":[],"attackHistory":[],"fall":None}
    state={"time":initial_parent["time"],"mode":initial_parent["mode"],"actors":actors,
      "inheritedParentState":copy.deepcopy(initial_parent),
      "parentSnapshotReference":{"stateId":"S030","stateSha256":parent["terminalStateSha256"],"sourcePath":rel(PARENT),
        "sourceReplaySha256":sha_file(PARENT),"copiedWithoutBranchEdits":True},
      "tile":tile_source,"fortressW09":fortress,"turnBudgets":{k:None for k in actors},
      "processedEventIds":copy.deepcopy(initial_parent["processedEventIds"]),
      "clock":copy.deepcopy(initial_parent["clock"]),
      "queueAuthority":{"queueId":queue["id"],"reviewedApplied":830,"pending":18,"acceptedUnapplied":0,
                        "nextIdentity":"conjure-demiplane-fortress","identityAcceptedOrApplied":False}}
    branch_start=copy.deepcopy(state); branch_start_sha=digest(branch_start)
    events=[]
    R=proposal["proposedOwnerAdoption"]["exactTerms"]

    def emit(event_id,event_time,kind,inputs,mutator,priority=0):
        nonlocal state
        before=copy.deepcopy(state); before_hash=digest(before)
        mutator(state)
        state["time"]=event_time
        delta=event_time-initial_parent["time"]
        state["clock"]["elapsedSeconds"]=num(initial_parent["clock"]["elapsedSeconds"]+delta)
        for clock_key in ("HornRemaining","OpeningRemaining"):
            if clock_key in initial_parent["clock"]:
                state["clock"][clock_key]=num(initial_parent["clock"][clock_key]-delta)
        state["processedEventIds"].append(event_id)
        after=copy.deepcopy(state); after_hash=digest(after)
        ev={"eventId":event_id,"time":event_time,"kind":kind,"ordinal":len(events)+1,
            "authoredInputs":inputs,"beforeStateSha256":before_hash,"afterStateSha256":after_hash,
            "forwardPatch":diff(before,after),"inversePatch":diff(after,before)}
        events.append(ev)
        replayed=apply_ops(before,ev["forwardPatch"])
        if digest(replayed)!=after_hash:
            def first_diff(a,b,path=""):
                if type(a)!=type(b): return (path,type(a).__name__,type(b).__name__,repr(a)[:200],repr(b)[:200])
                if isinstance(a,dict):
                    for k in sorted(a.keys()|b.keys()):
                        if k not in a or k not in b: return (path+"/"+k,"missing",repr(a.get(k))[:100],repr(b.get(k))[:100])
                        d=first_diff(a[k],b[k],path+"/"+k)
                        if d: return d
                elif isinstance(a,list):
                    if len(a)!=len(b): return (path,"length",len(a),len(b))
                    for i,(x,y) in enumerate(zip(a,b)):
                        d=first_diff(x,y,path+f"/{i}")
                        if d: return d
                elif a!=b: return (path,repr(a)[:200],repr(b)[:200])
                return None
            print("forward mismatch",event_id,digest(replayed),after_hash,first_diff(replayed,after),ev["forwardPatch"][:8])
            raise AssertionError("forward patch mismatch")
        reverted=apply_ops(after,ev["inversePatch"])
        if digest(reverted)!=before_hash:
            print("inverse mismatch",event_id,digest(reverted),before_hash,ev["inversePatch"][:8])
            raise AssertionError("inverse patch mismatch")

    descriptors=[]
    for aid,a in actors.items():
        sched=a["regularSchedule"]; t=float(sched["nextStart"])
        limit=108.0 if aid=="A" else 108.9-float(sched["endOffset"])
        while t<=limit+1e-7:
            descriptors.append((num(t),0,"TURN_START",aid))
            descriptors.append((num(t+float(sched["endOffset"])),10,"TURN_END",aid))
            t+=float(sched["period"])
    # Keep the four movement allocations at the adopted per-turn totals.
    spends=[(18.0,30.0),(24.0,30.0),(30.0,30.0),(36.0,10.0)]
    for t,_ in spends: descriptors.append((num(t if t>18 else 18.01),2,"MOVE",None))
    descriptors.append((18.01,1,"CARRY_REPOSITION",None))
    for i,t in enumerate(pre["attackGeometry"]["stipulatedAttackTimes"],1): descriptors.append((num(t),3,"ATTACK",i))
    descriptors.append((108.9,20,"FALL_LAND",None))
    descriptors.sort(key=lambda x:(x[0],x[1],str(x[2]),str(x[3])))

    move_index=0; route_progress=0.0; attack_index=0
    relative=pre["route"]["certifiedCarryRelativeBoundsFeet"]
    def carry_bounds(pos): return [num(pos[0]+relative[0]),num(pos[0]+relative[1]),num(pos[1]+relative[2]),num(pos[1]+relative[3]),num(pos[2]+relative[4]),num(pos[2]+relative[5])]

    for t,priority,kind,data in descriptors:
        if kind=="TURN_START":
            aid=data; actor=state["actors"][aid]
            def start(s,aid=aid,t=t,actor=actor):
                a=s["actors"][aid]; sch=a["regularSchedule"]
                assert abs(float(sch["nextStart"])-t)<1e-7
                a["action"]=1; a["bonusAction"]=1; a["reaction"]=1; a["movement"]=float(a["speed"])
                sch["starts"].append(t); sch["nextStart"]=num(t+float(sch["period"])); sch["nextEnd"]=num(t+float(sch["endOffset"]))
                s["turnBudgets"][aid]={"startedAt":t,"actionGranted":1,"actionSpent":False,"bonusActionGranted":1,
                    "bonusActionSpent":False,"reactionGranted":1,"reactionSpent":False,"movementGrantedFeet":float(a["speed"]),
                    "movementSpentFeet":0.0,"freeObjectInteractionUsed":False}
            emit(f"PG328-W09-R1:TURN-START-{aid}-{t:g}",t,"REGULAR_TURN_START",{"actor":aid,"resourceRefresh":"source regular schedule only","authoredChoice":"none at marker"},start,priority)
        elif kind=="TURN_END":
            aid=data; tstart=round(t-float(actors[aid]["regularSchedule"]["endOffset"]),9)
            def end(s,aid=aid,t=t,tstart=tstart):
                a=s["actors"][aid]; b=s["turnBudgets"][aid]
                assert b is not None and abs(b["startedAt"]-tstart)<1e-7
                a["regularSchedule"]["ends"].append(t); a["regularSchedule"]["nextEnd"]=None
                bcopy=copy.deepcopy(b)
                a["regularSchedule"]["budgetHistory"].append({"time":tstart,"action":1,"BA":1,"Reaction":1,"Move":b["movementGrantedFeet"],"recharge":{},
                  "endDisposition":{"regularTurnEndedAt":t,"recordedAt":t,
                    "Action":{"spent":1 if b["actionSpent"] else 0,"unusedExpired":0 if b["actionSpent"] else 1},
                    "BonusAction":{"spent":1 if b["bonusActionSpent"] else 0,"unusedExpired":0 if b["bonusActionSpent"] else 1},
                    "Reaction":{"spent":1 if b["reactionSpent"] else 0,"availableOffTurnUntilSpentOrNextOwnStart":not b["reactionSpent"]},
                    "MovementFeet":{"granted":b["movementGrantedFeet"],"spent":b["movementSpentFeet"],"unusedExpired":num(b["movementGrantedFeet"]-b["movementSpentFeet"])}}})
                a["action"]=0; a["bonusAction"]=0; a["movement"]=0
                s["turnBudgets"][aid]=None
            emit(f"PG328-W09-R1:TURN-END-{aid}-{t:g}",t,"REGULAR_TURN_END",{"actor":aid,"authoredChoice":"none beyond the A witness plan","B_C_DNoAction":aid!="A"},end,priority)
        elif kind=="CARRY_REPOSITION":
            def carry(s):
                b=s["turnBudgets"]["A"]; a=s["actors"]["A"]
                assert b is not None and b["startedAt"]==18.0 and a["position"]==[25,6,0]
                item=s["tile"]
                item["heldBoundsBeforeW09Feet"]=copy.deepcopy(item["heldBoundsFeet"])
                item["heldBoundsFeet"]={"x":[27,28],"y":[7,8],"z":[3,3.25]}
                b["freeObjectInteractionUsed"]=True
            emit("PG328-W09-R1:CARRY-REPOSITION-18.01",18.01,"TEST_ONLY_FREE_OBJECT_INTERACTION",{
              "actor":"A","sourceHeldBoundsFeet":inherited_bounds,"orderedSubmotions":["horizontal_translate","vertical_raise"],
              "intermediateBoundsFeet":[27,28,7,8,0,0.25],"correctedBoundsFeet":[27,28,7,8,3,3.25],
              "sweptAabbs":pre["carryTransition"]["sweptCollisionCheck"]["results"],"noActionOrMovementSpent":True,
              "oneOrdinaryFreeObjectInteraction":True,"afterRegularStart":18.0},carry,priority)
        elif kind=="MOVE":
            tstart=spends[move_index][0]; spend=spends[move_index][1]
            assert abs(t-(18.01 if tstart==18 else tstart))<1e-7
            support_parts=copy.deepcopy(support_after_move[int(round(tstart))])
            start_progress=route_progress; end_progress=route_progress+spend
            path=route_slice(route,start_progress,end_progress); move_index+=1
            newpos=path[-1]; newbounds=carry_bounds(newpos)
            # The chosen relative tile volume stays within A's adopted body envelope throughout this segment.
            for p in path:
                b=carry_bounds(p)
                assert b[0]>=p[0] and b[1]<=p[0]+5 and b[2]>=p[1] and b[3]<=p[1]+5 and b[4]>=p[2] and b[5]<=p[2]+6
            def move(s,newpos=newpos,newbounds=newbounds,spend=spend,start_progress=start_progress,end_progress=end_progress,path=path,tstart=tstart,support_parts=support_parts):
                a=s["actors"]["A"]; b=s["turnBudgets"]["A"]
                assert b is not None and abs(b["startedAt"]-tstart)<1e-7 and a["movement"]>=spend
                a["position"]=copy.deepcopy(newpos); a["movement"]=num(a["movement"]-spend)
                b["movementSpentFeet"]=num(b["movementSpentFeet"]+spend)
                s["tile"]["heldBoundsFeet"]=bounds_obj(newbounds)
                s["fortressW09"]["routeProgressFeet"]=end_progress
                s["fortressW09"]["actorABottomSupportPartIds"]=copy.deepcopy(support_parts)
                s["fortressW09"]["actorAHasBottomSupport"]=True
                s["fortressW09"]["movementLegs"].append({"turnStart":tstart,"spentFeet":spend,"routeProgressBefore":start_progress,
                  "routeProgressAfter":end_progress,"positions":path,"tileBoundsAtEndFeet":newbounds,"dash":False})
            emit(f"PG328-W09-R1:MOVE-{int(tstart)}",t,"REGULAR_MOVEMENT",{
              "actor":"A","turnStart":tstart,"grantedFeet":30,"spentFeet":spend,"noDash":True,"routePoints":path,
              "routeFeetBefore":start_progress,"routeFeetAfter":end_progress,"tileRelativeBoundsFeet":relative,
              "bodyEnvelopeContainment":"PASS for each listed route point",
              "supportAfter":{"partIds":support_parts,"supported":True}},move,priority)
            route_progress=end_progress
        elif kind=="ATTACK":
            attack_index=data; t=num(t); damage=5
            target_hp_before=state["fortressW09"]["targetPanel"]["hp"]
            def attack(s,attack_index=attack_index,t=t,damage=damage):
                a=s["actors"]["A"]; b=s["turnBudgets"]["A"]; f=s["fortressW09"]
                assert b is not None and b["startedAt"]==t-0.1 and a["action"]==1
                a["action"]=0; b["actionSpent"]=True
                hp_before=f["targetPanel"]["hp"]; f["targetPanel"]["hp"]=max(0,hp_before-damage)
                carry_world=carry_bounds(a["position"]); strike_bounds=[45,46,60,61,4.75,5.0]
                swing=[
                  {"id":"tile-to-strike","fromBoundsFeet":carry_world,"toBoundsFeet":strike_bounds,
                    "forwardPatch":[{"op":"replace","path":"/boundsFeet","value":strike_bounds}],
                    "inversePatch":[{"op":"replace","path":"/boundsFeet","value":carry_world}]},
                  {"id":"tile-return-to-carry","fromBoundsFeet":strike_bounds,"toBoundsFeet":carry_world,
                    "forwardPatch":[{"op":"replace","path":"/boundsFeet","value":carry_world}],
                    "inversePatch":[{"op":"replace","path":"/boundsFeet","value":strike_bounds}]}
                ]
                record={"index":attack_index,"time":t,"targetPanelId":target,"d20":16,"strengthModifier":1,"proficiency":0,
                  "attackTotal":17,"targetAC":17,"hit":True,"damageDie":4,"damageDieResult":4,"damage":damage,
                  "panelHpBefore":hp_before,"panelHpAfter":f["targetPanel"]["hp"],"action":"ordinary Attack/Sunder","rpSpent":0,
                  "tileId":tile_id,"heldBy":"A:right","tileBoundsBeforeStrikeFeet":carry_world,
                  "strikeBoundsFeet":strike_bounds,"tileBoundsAfterReturnFeet":carry_world,
                  "tileSwingSubmotions":swing,"oneOrdinaryActionIncludesStrikeAndReturn":True,
                  "extraMovementFeet":0,"tileConsumed":False}
                f["attackHistory"].append(record)
                if attack_index==12:
                    assert f["targetPanel"]["hp"]==0
                    f["targetPanel"]["destroyed"]=True
                    f["destroyedParts"]=copy.deepcopy(f["dependentStairPartsOnTargetRemoval"])
                    f["actorAHasBottomSupport"]=False; f["actorABottomSupportPartIds"]=[]
                    f["fall"]={"status":"PENDING_NEXT_REGULAR_SLOT_END","initiatedAt":t,"fallStartMarker":108.9,
                      "xFeet":a["position"][0],"yFeet":a["position"][1],"startFeetZ":a["position"][2],"damageRuleBound":"existing Falling procedure"}
            emit(f"PG328-W09-R1:ATTACK-{attack_index:02d}-{t:g}",t,"TEST_ONLY_ORDINARY_ATTACK_SUNDER",{
              "actor":"A","targetPanelId":target,"roll":{"d20":16,"strengthModifier":1,"proficiency":0,"total":17,"AC":17},
              "damage":{"d4":4,"strengthModifier":1,"total":damage},"actionCost":1,"rpCost":0,
              "supportAfter":{"partIds":([] if attack_index==12 else copy.deepcopy(state["fortressW09"]["actorABottomSupportPartIds"])),"supported":attack_index!=12},
              "tileStrikeBoundsFeet":[45,46,60,61,4.75,5.0],
              "tileBoundsBeforeStrikeFeet":carry_bounds([45,59.5,4.5]),"tileBoundsAfterReturnFeet":carry_bounds([45,59.5,4.5]),
              "tileSwingSubmotions":[
                {"id":"tile-to-strike","fromBoundsFeet":carry_bounds([45,59.5,4.5]),"toBoundsFeet":[45,46,60,61,4.75,5.0],
                 "forwardPatch":[{"op":"replace","path":"/boundsFeet","value":[45,46,60,61,4.75,5.0]}],
                 "inversePatch":[{"op":"replace","path":"/boundsFeet","value":carry_bounds([45,59.5,4.5])}]},
                {"id":"tile-return-to-carry","fromBoundsFeet":[45,46,60,61,4.75,5.0],"toBoundsFeet":carry_bounds([45,59.5,4.5]),
                 "forwardPatch":[{"op":"replace","path":"/boundsFeet","value":carry_bounds([45,59.5,4.5])}],
                 "inversePatch":[{"op":"replace","path":"/boundsFeet","value":[45,46,60,61,4.75,5.0]}]}
              ],"positiveVolumePenetration":False,
              "targetHpBefore":target_hp_before,"targetHpAfter":max(0,target_hp_before-damage),
              "stipulatedInputNotAnActualRoll":True,"structuralCollapseOnFinalHitOnly":attack_index==12},attack,priority)
        elif kind=="FALL_LAND":
            def land(s):
                a=s["actors"]["A"]; f=s["fortressW09"]
                assert f["fall"] and f["targetPanel"]["hp"]==0 and not f["actorAHasBottomSupport"]
                a["position"]=[45,59.5,0.5]; s["tile"]["heldBoundsFeet"]=bounds_obj(carry_bounds(a["position"]))
                f["actorABottomSupportPartIds"]=["keep-tread-0-1","keep-riser-0-1"]
                f["actorAHasBottomSupport"]=True
                f["fall"].update({"status":"LANDED_TEST_ONLY","landedAt":108.9,"landingPartId":"keep-tread-0-1",
                  "landingFeetZ":0.5,"distanceFeet":4.0,"damage":0,"proneFromFallingDamage":False})
            emit("PG328-W09-R1:FALL-LAND-108.9",108.9,"TEST_ONLY_FALL_LANDING",{
              "afterRegularMarkersThroughAEnd":True,"fixedXY":[45,59.5],"firstSupportingSurface":"keep-tread-0-1 top face z=0.5 ft",
              "fallDistanceFeet":4.0,"damage":0,"proneFromFallingDamage":False,"campaignOccurrence":False,
              "supportAfter":{"partIds":["keep-tread-0-1","keep-riser-0-1"],"supported":True}},land,priority)

    assert move_index==4 and attack_index==12
    assert state["actors"]["A"]["position"]==[45,59.5,0.5]
    assert state["actors"]["A"]["HP"]==122 and state["actors"]["A"]["RP"]==53
    assert state["fortressW09"]["actorABottomSupportPartIds"]==["keep-tread-0-1","keep-riser-0-1"]
    assert state["fortressW09"]["actorAHasBottomSupport"] is True
    assert state["fortressW09"]["targetPanel"]["hp"]==0 and len(state["fortressW09"]["destroyedParts"])==18
    assert state["fortressW09"]["fall"]["distanceFeet"]==4.0
    assert state["tile"]["expiresAtEventTime"]==3606.13 and not state["tile"]["consumed"]
    assert state["queueAuthority"]["pending"]==18 and state["queueAuthority"]["reviewedApplied"]==830

    marker_events=[e for e in events if e["kind"] in ("REGULAR_TURN_START","REGULAR_TURN_END")]
    start_counts={a:sum(e["kind"]=="REGULAR_TURN_START" and e["authoredInputs"]["actor"]==a for e in marker_events) for a in actors}
    end_counts={a:sum(e["kind"]=="REGULAR_TURN_END" and e["authoredInputs"]["actor"]==a for e in marker_events) for a in actors}
    assert start_counts=={a:16 for a in actors} and end_counts=={a:16 for a in actors}
    inherited_boundary=[e for e in parent["events"] if e.get("kind")=="REGULAR_TURN_END" and e.get("time")==12.9]
    assert len(inherited_boundary)==1 and inherited_boundary[0]["eventId"] in initial_parent["processedEventIds"]
    inherited_boundary_marker={"eventId":inherited_boundary[0]["eventId"],"time":12.9,"kind":"REGULAR_TURN_END",
      "actor":"A","sourcePath":rel(PARENT),"sourceReplaySha256":sha_file(PARENT),"inheritedFromExactS030Parent":True}
    replay={"id":"PG328-W09-R1-REVERSIBLE-WITNESS-428-TESTONLY",
      "classification":"REVERSIBLE_HYPOTHETICAL_TEST_ONLY_SUCCESSOR_WITNESS_FOR_DIRECTOR_REVIEW_UNSEALED",
      "status":"READY_FOR_DIRECTOR_REVIEW; TEST_ONLY; UNSEALED",
      "scope":{"spellId":"conjure-demiplane-fortress","holdId":"PG200-B06","witnessId":"PG328-W09","branchId":"PG328-W09-R1",
        "campaignOccurrence":False,"canonicalRulesChanged":False,"fixtureMutated":False,"runtimeExecuted":False,"identityAcceptedOrApplied":False},
      "ownerAdoption":{"path":rel(OWNER),"sha256":sha_file(OWNER),"proposalId":proposal["id"],"proposalSha256":sha_file(PROPOSAL),
        "exactTerms":R,"exactTermsDigest":digest(R)},
      "parentBinding":{"path":rel(PARENT),"replayId":parent["id"],"sourceSnapshotCommit":pre["sourceSnapshotCommit"],
        "terminalStateId":"S030","terminalStateSha256":parent["terminalStateSha256"],"terminalTime":12.9,
        "parentBytesMutated":False,"branchBeginsWithExactParentSnapshot":True,
        "embeddedParentSnapshotSha256":digest(initial_parent),"embeddedParentSnapshotUntouched":True},
      "sourceBindings":bindings,
      "branchInitialStateId":"PG328-W09-R1-S000_PARENT_S030_PLUS_TESTONLY_BRANCH_OVERLAY",
      "branchInitialStateSha256":branch_start_sha,"stateSnapshots":{"PG328-W09-R1-S000_PARENT_S030_PLUS_TESTONLY_BRANCH_OVERLAY":branch_start,
        "PG328-W09-R1-S"+str(len(events)).zfill(3)+"_TERMINAL":state},
      "events":events,"terminalStateId":"PG328-W09-R1-S"+str(len(events)).zfill(3)+"_TERMINAL","terminalStateSha256":digest(state),
      "initiativeMarkerCoverage":{"intervalStart":12.9,"fallMarker":108.9,"regularStartCountByActor":start_counts,
        "regularEndCountByActor":end_counts,"allBcdChoices":"No rescue, movement, attack, spell, reaction, rest, recovery or clock-reset action.",
        "markersAreSourceScheduleEvents":True,"inheritedBoundaryMarker":inherited_boundary_marker},
      "movementPlan":{"turnSpendsFeet":[30,30,30,10],"routeTotalFeet":route_total,"routePoints":route,
        "turnEndpoints":[x["authoredInputs"]["routePoints"][-1] for x in events if x["kind"]=="REGULAR_MOVEMENT"],"dash":False,
        "carryRelativeBoundsFeet":relative,"allMovementAndCarryAreHypothetical":True},
      "combatPlan":{"attackCount":12,"attackTimes":pre["attackGeometry"]["stipulatedAttackTimes"],"attackTotal":17,"targetAC":17,
        "damagePerHit":5,"targetHpBefore":60,"targetHpAfter":0,"allRollsStipulated":True,"rpSpent":0},
      "structuralAndFallOutcome":{"destroyedTarget":target,"destroyedDependentPartIds":dep,"destroyedDependentPartCount":18,
        "retainedRoot":"origin-ground-face","retainedHistoricalW01SouthPanelHp":55,"landedOn":"keep-tread-0-1","fallDistanceFeet":4,
        "damage":0,"proneFromFallingDamage":False,"allOutcomesHypothetical":True},
      "queueAndDecisionState":{"queueId":queue["id"],"reviewedApplied":830,"pending":18,"acceptedUnapplied":0,
        "identityAcceptedOrApplied":False,"appliedIds":[],"queueChanged":False},
      "nonEffects":["No campaign events are asserted.","No W09 or Fortress seal is issued.","No Fortress acceptance or application is issued.",
        "No canonical rule or fixture is changed.","Queue 423 and its 830/18/0 authority remain unchanged.",
        "The W01-403 parent bytes, Geometry405, SupportOverlay425, prior seals and unrelated branches remain unchanged."]}

    OUT.mkdir(parents=True,exist_ok=True)
    (OUT/"evidence").mkdir(exist_ok=True)
    # Keep the portable package tied to exact source bytes used to construct the branch.
    evidence_files=[(PROPOSAL,"W09_PROPOSAL_426_REPACK01.json"),(READBACK,"W09_DIRECTOR_READBACK_426_REPACK01.json"),
      (PREFLIGHT,"W09_GEOMETRY_PREFLIGHT_426_REPACK01.json"),(PARENT,"W01_REPLAY_403_REPACK02.json"),
      (GEOMETRY,"GEOMETRY_405.json"),(SUPPORT,"SUPPORT_OVERLAY_425_TESTONLY.json"),(OWNER_W01,"W01_OWNER_ADOPTION_424.json"),
      (OVERLAY_ZIP,"W01_SUCCESSOR_OVERLAYS_425_TESTONLY.zip"),(QUEUE,"CURRENT_SPELL_QUEUE_423_REPACK01.json"),(HANDOFF,"CURRENT_HANDOFF_423_REPACK01.json")]
    for src,name in evidence_files: shutil.copyfile(src,OUT/"evidence"/name)
    shutil.copyfile(OWNER,OUT/"OWNER_PG328_W09_SUPPORT_ADOPTION_427_TESTONLY.json")
    (OUT/"W09_REPLAY_428_TESTONLY.json").write_text(json.dumps(replay,ensure_ascii=False,indent=2)+"\n",encoding="utf-8",newline="\n")
    (OUT/"SOURCE_BINDINGS_428.json").write_text(json.dumps({"id":"PG328-W09-R1-SOURCE-BINDINGS-428","bindings":bindings},ensure_ascii=False,indent=2)+"\n",encoding="utf-8",newline="\n")
    correction={"schemaVersion":1,"id":"PG328-W09-R1-DIRECTOR-C01-RESOLUTION-428",
      "classification":"DIRECTOR_REQUESTED_TEST_ONLY_STATE_LEDGER_CORRECTION",
      "sourceDirectorResponse":{"service":"ChatGPT","conversationTitle":"Calibration review part 6",
        "conversationId":"6adc506d-8770-83ea-b64c-0345d9b9b682","messageId":"6c6faa34-1e1d-56f7-b9e7-05f094583410",
        "reviewedCommit":"3db1e4241f83d99462fc8eaab985a0ff3080fc60","priorArchiveSha256":"bf6ca5730e0a0f40d7e217d04ce5d8f678d4e944e474e8af629430e3030658c2"},
      "findingId":"W09-428-C01","finding":"Synchronize actor A's live bottom-support IDs and supported flag with the existing adopted geometry at each named state/event.",
      "noAdditionalOwnerPremiseRequired":True,
      "expectedSupportStates":[
        {"state":"branchInitialStateId","actorAPositionFeet":[25,6,0],"supportPartIds":["origin-ground-face"],"hasBottomSupport":True},
        {"eventIndex":8,"eventId":"PG328-W09-R1:MOVE-18","actorAPositionFeet":[49,10,0],"supportPartIds":["origin-ground-face"],"hasBottomSupport":True},
        {"eventIndex":17,"eventId":"PG328-W09-R1:MOVE-24","actorAPositionFeet":[55,34,0],"supportPartIds":["origin-ground-face"],"hasBottomSupport":True},
        {"eventIndex":26,"eventId":"PG328-W09-R1:MOVE-30","actorAPositionFeet":[46,55,0],"supportPartIds":["origin-ground-face","keep-F0-0-2","keep-F0-1-2"],"hasBottomSupport":True},
        {"eventIndex":35,"eventId":"PG328-W09-R1:MOVE-36","actorAPositionFeet":[45,59.5,4.5],"supportPartIds":["keep-tread-0-9","keep-riser-0-9"],"hasBottomSupport":True},
        {"eventIndex":135,"eventId":"PG328-W09-R1:ATTACK-12-102.1","actorAPositionFeet":[45,59.5,4.5],"supportPartIds":[],"hasBottomSupport":False},
        {"eventIndex":145,"eventId":"PG328-W09-R1:FALL-LAND-108.9","actorAPositionFeet":[45,59.5,0.5],"supportPartIds":["keep-tread-0-1","keep-riser-0-1"],"hasBottomSupport":True}],
      "regenerated":{"affectedEventStateHashes":True,"forwardPatches":True,"inversePatches":True,"independentSupportAssertions":True},
      "nonEffects":["No campaign event or gameplay occurrence is asserted.","No new owner premise or canonical rule is introduced.",
        "No seal, Fortress acceptance/application, fixture mutation or queue change is authorized."]}
    (OUT/"DIRECTOR_C01_CORRECTION_428.json").write_text(json.dumps(correction,ensure_ascii=False,indent=2)+"\n",encoding="utf-8",newline="\n")
    (OUT/"DIRECTOR_REVIEW_REQUEST_428.md").write_text(
      "# Director review request — Fortress W01 overlays and W09-R1 (TEST_ONLY)\n\n"
      "Please review the exact owner-adopted W01 successor overlays 425 and PG328-W09-R1 reversible witness 428. "
      "The owner adopted both W01 proposals exactly (record 424) and adopted W09 Repack01 by exact proposal hash "
      "(record 427; proposal SHA-256 `f4dfbf3403c63f603ef188be972c4425cc627309d4fb77cc86934afecd6b8a9d`).\n\n"
      "W01 overlays 425: static verifier PASS, 8,134 checks, 0 failures; independent verification 9/9. "
      "W09 witness 428: reversible replay PASS, 146 events including 128 regular-turn markers, 100-foot route, 12 stipulated attacks, "
      "18 dependent stair parts and the specified 4-foot hypothetical fall. The entire unchanged S030 parent snapshot is embedded and bound by hash. "
      "Each attack explicitly traces the held tile from carry bounds to the strike bounds and back with inverse operations. No actual campaign occurrence is asserted.\n\n"
      "Director finding W09-428-C01 is addressed in `DIRECTOR_C01_CORRECTION_428.json`: A's bottom-support ledger now matches the existing adopted geometry at the initial pose, movement events 8/17/26/35, final attack event 135 and landing event 145. The witness generator now records each transition, and the independent verifier checks each pose/support pair and reversible patch. No new owner premise was required.\n\n"
      "Please return precise findings on the W01 support/z46 overlays, each W09 source binding and event sequence, all movement/carry/contact "
      "geometry, attack submotions and inputs, support loss, falling result, reversibility, and non-effects. State explicitly whether any correction remains and whether "
      "Fortress is ready for identity acceptance. Do not treat this packet as a seal, campaign event, canonical change, or application.\n\n"
      "- W01 package: `fortress_w01_successor_overlays_425/DD_Fortress_W01_Successor_Overlays_425_TESTONLY.zip` (SHA-256 `8d1857bcedc412181d90ab2cb6347b2f40b0694c648a081ca2af40f58ad4200e`)\n"
      "- W09 witness: `W09_REPLAY_428_TESTONLY.json` (SHA-256 `"+sha_bytes((OUT/"W09_REPLAY_428_TESTONLY.json").read_bytes())+"`)\n"
      "- W09 packet: `DD_Fortress_W09_Successor_Witness_428_TESTONLY.zip`; verify hash in `DELIVERY_428.json`.\n"
      "- Current authority: `CURRENT_SPELL_QUEUE_428_REPACK01.json`, 830 applied / 18 pending / 0 accepted-unapplied.\n"
      "- Current handoff: `CURRENT_HANDOFF_428_REPACK01.json`.\n",encoding="utf-8",newline="\n")
    build_script_copy=OUT/"BUILD_W09_REPLAY_428.py"
    if Path(__file__).resolve()!=build_script_copy.resolve(): shutil.copyfile(Path(__file__),build_script_copy)
    # Verification is completed by the separate verifier before archive and delivery are sealed.
    manifest_files=[]
    for p in sorted(x for x in OUT.rglob("*") if x.is_file() and x.name not in {"MANIFEST_428.json","DELIVERY_428.json",ARCHIVE}):
        manifest_files.append({"path":p.relative_to(OUT).as_posix(),"bytes":p.stat().st_size,"sha256":sha_file(p)})
    manifest={"id":"PG328-W09-R1-MANIFEST-428","artifact":ARCHIVE,"status":"TEST_ONLY_UNSEALED_PENDING_DIRECTOR_REVIEW",
      "files":manifest_files,"sourceBindings":bindings}
    (OUT/"MANIFEST_428.json").write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+"\n",encoding="utf-8",newline="\n")
    archive=OUT/ARCHIVE
    with zipfile.ZipFile(archive,"w",compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for p in sorted(x for x in OUT.rglob("*") if x.is_file() and x.name not in {"DELIVERY_428.json",ARCHIVE}):
            info=zipfile.ZipInfo(p.relative_to(OUT).as_posix(),date_time=(2026,11,1,0,0,0))
            info.compress_type=zipfile.ZIP_DEFLATED; info.external_attr=0o600<<16
            z.writestr(info,p.read_bytes(),compress_type=zipfile.ZIP_DEFLATED,compresslevel=9)
    delivery={"id":"PG328-W09-R1-DELIVERY-428","artifact":ARCHIVE,"archiveBytes":archive.stat().st_size,
      "archiveSha256":sha_file(archive),"manifestSha256":sha_file(OUT/"MANIFEST_428.json"),"memberCount":len(manifest_files)+1,
      "witnessPath":"W09_REPLAY_428_TESTONLY.json","witnessSha256":sha_file(OUT/"W09_REPLAY_428_TESTONLY.json"),
      "status":"TEST_ONLY_UNSEALED_PENDING_DIRECTOR_REVIEW"}
    (OUT/"DELIVERY_428.json").write_text(json.dumps(delivery,ensure_ascii=False,indent=2)+"\n",encoding="utf-8",newline="\n")
    print(json.dumps({"output":str(OUT),"events":len(events),"turnMarkers":len(marker_events),"startCounts":start_counts,
      "endCounts":end_counts,"routeFeet":route_total,"witnessSha256":sha_file(OUT/"W09_REPLAY_428_TESTONLY.json"),
      "archiveBytes":archive.stat().st_size,"archiveSha256":sha_file(archive)},indent=2))

if __name__=="__main__": main()
