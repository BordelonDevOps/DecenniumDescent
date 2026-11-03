#!/usr/bin/env python3
"""Build and verify the adopted Fate Rewrite Proposal 05 TEST_ONLY branches."""
import copy, hashlib, json, subprocess, unicodedata
from pathlib import Path

BASE="f60207e291c8c87a46420469934a3d8a82aa7d87"
P05="FR-EP480-INTERFACE-PROPOSAL-05"
P05_SHA="cd492a5bdf9c966f83a2674c31ff1db02a10d2df5f3c92fe8b4680974047386d"
PASS_COMMIT="08c4e0db03fb3d20db56c01c16af7865110adc85"
T1_FINAL="49d94d12e54fbd36d36a0cf3f69803f6de1b0f903557804c02dbd41f1a2ae7c3"
PARENT_SHA="55de6c13eb5c86784933052e401d8f84ad600d6b1ec8830280eeb693d0c0347c"
OID="RANK9TIMEFATE6129-ETERNAL-PROPHECY-A-cast1"
OBL_SHA="2f6c8956d26cecd196523eba61cf777a983217a4d4ab0505ec36960753c0c862"
BOOK_SHA="16ab195897e69ea3f693e7afaf85bfcdf1947ba78a5823e3cabde227e1e58c9a"
TERMINAL_SHA="b9b48d2e102c127deee670ac89d51a8153739f01a2841c2db01c0e72b456172d"
DEADLINE=34560000100
EXPIRY=34560000101
COMPAT=Path("docs/audit/2026-10-08/full-game/director-spell-review-129/fate_rewrite_ep480_interface_spec_2026-11-02")
WITNESS=Path("docs/audit/2026-10-08/full-game/director-spell-review-129/fate_rewrite_ep480_interface_witness_2026-11-03")
P05_REL=COMPAT/"FATE_REWRITE_EP480_INTERFACE_PROPOSAL_05.json"
MAN_REL=COMPAT/"PACKET_MANIFEST_05.json"
PASS_REL=COMPAT/"CODEX_TRANSCRIBED_DIRECTOR_REVIEW_PASS_05.json"
T1_REL=Path("docs/audit/2026-10-08/full-game/director-spell-review-129/eternal_prophecy_ep480_testonly_witness_2026-11-02/EP480_TESTONLY_WITNESS_PACKET_T1_T4.json")
T1_SHA="e77130b2a2f41b2d7ef1064f206a22b6a04c2dc679727d8ba5d17dbc6a1c8bb7"
RECEIPT=WITNESS/"OWNER_ADOPTION_RECEIPT_FR_EP480_P05.json"
PACKET=WITNESS/"FR_EP480_P05_TESTONLY_WITNESS_PACKET.json"
REQUEST=WITNESS/"DIRECTOR_REVIEW_REQUEST_FR_EP480_P05_WITNESSES.md"
MANIFEST=WITNESS/"PACKET_MANIFEST_FR_EP480_P05_WITNESSES.json"
SCRIPT=WITNESS/"tools/build_verify_fr_ep480_p05_witnesses.py"
RESPONSE="Yes—adopt this exact Proposal 05"
ADOPTION=("I adopt FR-EP480-INTERFACE-PROPOSAL-05, SHA-256 "
"cd492a5bdf9c966f83a2674c31ff1db02a10d2df5f3c92fe8b4680974047386d, "
"solely for construction and submission of its two bounded TEST_ONLY branches, "
"FR-EP480-IFACE-COMPAT-01 and FR-EP480-IFACE-CONFLICT-01. No other premises, "
"seal, blocker closure, identity acceptance/application, or canon/runtime/campaign/queue change is authorized.")
ADOPTED_AT="2026-11-03T03:07:24Z"
ROOT=Path(subprocess.check_output(["git","rev-parse","--show-toplevel"],text=True).strip())

def git_show(spec): return subprocess.check_output(["git","show",spec],cwd=ROOT)
def sha(raw): return hashlib.sha256(raw).hexdigest()
def norm(v):
    if isinstance(v,str): return unicodedata.normalize("NFC",v)
    if isinstance(v,list): return [norm(x) for x in v]
    if isinstance(v,dict): return {unicodedata.normalize("NFC",str(k)):norm(x) for k,x in sorted(v.items(),key=lambda i:str(i[0]))}
    return v
def canon(v): return json.dumps(norm(v),ensure_ascii=False,separators=(",",":"),allow_nan=False).encode("utf-8")
def digest(v): return sha(canon(v))
def getp(root,p):
    cur=root
    for raw in p.split("/")[1:]:
        k=raw.replace("~1","/").replace("~0","~"); cur=cur[int(k)] if isinstance(cur,list) else cur[k]
    return cur
def tryget(root,p):
    try:return True,getp(root,p)
    except (KeyError,IndexError,TypeError):return False,None
def esc(k):return str(k).replace("~","~0").replace("/","~1")
def ptr(path):return "".join("/"+esc(k) for k in path)
def diff(a,b,path=()):
    if isinstance(a,dict) and isinstance(b,dict):
        out=[]
        for k in sorted(set(a)|set(b)):
            p=path+(str(k),)
            if k not in a:out.append({"op":"add","path":ptr(p),"beforeExists":False,"afterExists":True,"after":copy.deepcopy(b[k])})
            elif k not in b:out.append({"op":"remove","path":ptr(p),"beforeExists":True,"afterExists":False,"before":copy.deepcopy(a[k])})
            else:out.extend(diff(a[k],b[k],p))
        return out
    if a!=b:return [{"op":"replace","path":ptr(path),"beforeExists":True,"afterExists":True,"before":copy.deepcopy(a),"after":copy.deepcopy(b)}]
    return []
def setp(root,p,exists,value=None):
    parts=p.split("/")[1:]; cur=root
    for raw in parts[:-1]:
        k=raw.replace("~1","/").replace("~0","~"); cur=cur[int(k)] if isinstance(cur,list) else cur[k]
    k=parts[-1].replace("~1","/").replace("~0","~")
    if isinstance(cur,list):cur[int(k)]=copy.deepcopy(value)
    elif exists:cur[k]=copy.deepcopy(value)
    else:del cur[k]
def apply(state,ops):
    for op in ops:
        ex,val=tryget(state,op["path"])
        if ex!=op["beforeExists"] or (ex and val!=op.get("before")):raise AssertionError("patch precondition "+op["path"])
        setp(state,op["path"],op["afterExists"],op.get("after"))
def inverse(ops):
    return [{"op":{"add":"remove","remove":"add","replace":"replace"}[x["op"]],"path":x["path"],
      "beforeExists":x["afterExists"],"afterExists":x["beforeExists"],
      **({"before":copy.deepcopy(x["after"])} if x["afterExists"] else {}),
      **({"after":copy.deepcopy(x["before"])} if x["beforeExists"] else {})} for x in reversed(ops)]
def snapshot(s):
    o=s["overlay"]; f=o.get("fixture",{})
    return {"branchState":digest(s),"T":digest(o.get("actorOverrides",{}).get("T")),
      "W":digest(o.get("actorOverrides",{}).get("W")),"book-W":digest(o.get("itemOverrides",{}).get("book-W")),
      "obligation":digest(o.get("newObligations",{}).get(OID)),"terminalRecord":digest(o.get("terminalRecord")),
      "terminalScheduler":digest(o.get("terminalScheduler")),
      "supportAndMarker":digest({"supportPatch":f.get("supportPatch"),"cacheMarker":f.get("cacheMarker")})}
def add_transition(branch,state,event,at,ordinal,description,mutate,reads):
    before=copy.deepcopy(state); bh=digest(before); vb=snapshot(before); mutate(state); ah=digest(state); va=snapshot(state)
    ops=diff(before,state); writes=[]
    for op in ops:
        ex,val=tryget(state,op["path"]); writes.append({"path":op["path"],"exists":ex,"sha256":digest(val) if ex else None})
    tr={"eventId":event,"atMs":at,"sequenceOrdinalAtSameMillisecond":ordinal,"description":description,
        "readSetVersions":{k:vb[k] for k in reads},"writeSetVersions":writes,
        "beforeStateSHA256":bh,"afterStateSHA256":ah,"forward":ops,"inverse":inverse(ops)}
    branch["transitions"].append(tr); return tr

def verify_sources(proposal):
    out=[]
    for b in proposal["sourceBindings"]:
        raw=git_show(f"{BASE}:{b['path']}")
        if sha(raw)!=b["sha256"] or len(raw)!=b["bytes"]:raise AssertionError("proposal source mismatch "+b["path"])
        blob=subprocess.check_output(["git","rev-parse",f"{BASE}:{b['path']}"],cwd=ROOT,text=True).strip()
        if b["path"].endswith(".json"):
            data=json.loads(raw)
            for p in b.get("pointers",[]):getp(data,p)
        out.append({"role":b["role"],"path":b["path"],"bytes":len(raw),"gitBlobSha1":blob,
                    "sha256":sha(raw),"pointers":b.get("pointers",[])})
    return out

def source_t1(proposal,sources,packet):
    parent=sources["exact_Return323_case_A_raw_parent"]["events"][2]["after"]
    if digest(parent)!=PARENT_SHA or digest(packet["parentProjection"]["state"])!=PARENT_SHA:raise AssertionError("source parent hash")
    if packet["parentProjectionCanonicalSHA256"]!=PARENT_SHA:raise AssertionError("parent packet hash")
    b=next(x for x in packet["branches"] if x["caseId"]=="EP480-T1"); state=copy.deepcopy(b["branchStartState"])
    if digest(state)!=b["branchStartStateSHA256"]:raise AssertionError("T1 start hash")
    for tr in b["transitions"]:
        if digest(state)!=tr["beforeStateSHA256"]:raise AssertionError("T1 before hash")
        apply(state,tr["forward"])
        if digest(state)!=tr["afterStateSHA256"]:raise AssertionError("T1 after hash")
    if digest(state)!=T1_FINAL or b["finalStateSHA256"]!=T1_FINAL:raise AssertionError("T1 final hash")
    final=copy.deepcopy(state)
    for tr in reversed(b["transitions"]):
        apply(state,tr["inverse"])
        if digest(state)!=tr["beforeStateSHA256"]:raise AssertionError("T1 inverse")
    if digest(state)!=b["branchStartStateSHA256"]:raise AssertionError("T1 inverse start")
    ob=final["overlay"]["newObligations"][OID]
    if digest(ob)!=OBL_SHA or digest(final["overlay"]["itemOverrides"]["book-W"])!=BOOK_SHA:raise AssertionError("T1 object version")
    if ob["status"]!="fulfilled" or not final["overlay"]["terminalScheduler"]["consumed"] or final["overlay"]["terminalScheduler"]["active"]:raise AssertionError("T1 terminal state")
    return b,final

def scene(proposal):
    s=proposal["compatibleRewrite"]["newPremises"]["scene"]; p=s["additionalGateGeometryOverlay"]
    return {"classification":p["classification"],"volumeFt":p["volumeFt"],"collisionBlocking":p["collisionBlocking"],
     "opaque":p["opaque"],"blocksRaysThatIntersectVolume":p["blocksRaysThatIntersectVolume"],"basis":p["basis"],
     "northBypass":p["northBypass"],"southBypass":p["southBypass"],
     "noLineOfSightThroughGateAssumed":p["noLineOfSightThroughGateAssumed"],
     "routeAndRayRule":p["routeAndRayRule"],"inheritedGateSource":s["inheritedGate"]}
def shell(spec,start):
    ok=spec["branchId"].endswith("COMPAT-01")
    return {"branchId":spec["branchId"],"executionChildId":spec["executionChildId"],
     "scenario":"compatible post-fulfillment rewrite" if ok else "conflicting removal request",
     "classification":"TEST_ONLY_BRANCH_LOCAL_CONSTRUCTION","branchStartState":copy.deepcopy(start),
     "branchStartStateSHA256":digest(start),"transitions":[]}
def expire(proposal,branch,state):
    bid=branch["branchId"]; child=branch["executionChildId"]; at=EXPIRY
    def mutate(s):
        o=s["overlay"]; o["nowMs"]=at
        o["fateRewriteInterface"]={"proposalId":P05,"proposalSha256":P05_SHA,"branchId":bid,"executionChildId":child,
         "parentCaseId":"EP480-T1","parentExecutionChildId":"EP480-WITNESS-OBLIGATION-BOOK-W-01-T1",
         "classification":"TEST_ONLY; no campaign/canon/runtime/queue effect"}
        o["fixture"]["gateGeometryOverlay_TEST_ONLY"]=copy.deepcopy(scene(proposal))
        o["ordinaryMagicalInterventionsEnabled"]=True; o["ordinarySpellExpressionEnabled"]=True
        for key in ("EP480-PREVENT-ALLY-DELIVERY","EP480-PREVENT-CARRY-ROUTE","EP480-PREVENT-OTHER-DELIVERY","EP480-SUPPRESS-ORDINARY-EXPRESSION"):
            x=o["preventionOperands"][key]
            if x["persistsUntilMs"]!=DEADLINE or not x["inclusiveThroughDeadline"]:raise AssertionError("deadline mismatch")
            x.update({"active":False,"expiredAtMs":at,"historyPreserved":True})
        o["postDeadlineExpiry"]={"atMs":at,"deadlineInclusiveThroughMs":DEADLINE,"expiredAfterInclusiveDeadline":True,
         "ordinaryMagicalInterventionsEnabled":True,"ordinarySpellExpressionEnabled":True,
         "terminalSchedulerStayedConsumedInactive":True,"historyPreserved":True}
    t=add_transition(branch,state,bid+"-EXPIRY-01",at,1,
     "Expire the four operands after the inclusive deadline; preserve consumed terminal and source histories.",
     mutate,["branchState","terminalScheduler","obligation","supportAndMarker"])
    t["sourceReadVersions"]={"proposalSha256":P05_SHA,"T1FinalStateSha256":T1_FINAL,
     "obligationSha256":OBL_SHA,"terminalAfterSha256":TERMINAL_SHA}
def build_compat(proposal,start):
    spec=proposal["compatibleRewrite"]; prem=spec["newPremises"]; bid=spec["branchId"]; child=spec["executionChildId"]
    b=shell(spec,start); s=copy.deepcopy(start); expire(proposal,b,s); consent=prem["ownerConsent"]
    def cm(x):
        o=x["overlay"]; o["nowMs"]=consent["atMs"]; o["ownerConsent"]=copy.deepcopy(consent)
        o["actorOverrides"]["W"]["position"]=consent["poses"]["W"]; o["actorOverrides"]["T"]["position"]=consent["poses"]["T"]
        o["actorOverrides"]["T"].update({"RP":64,"Dissonance":0,"Refrain":0,"seenFamilies":[],"lastSpell":None,"spellsThisTurn":0,"pendingCast":None})
        o["actorOverrides"]["W"]["RP"]=38
    add_transition(b,s,"FR-EP480-COMPAT-OWNER-CONSENT-01",consent["atMs"],1,"W grants the exact post-expiry pickup permission; bind actor/resource projection.",cm,["T","W","obligation","book-W"])
    load=copy.deepcopy(prem["fixtureLoadout"])
    def lm(x):
        o=x["overlay"]; o["nowMs"]=consent["atMs"]; o["fixture"]["fateRewriteLoadout_TEST_ONLY"]=copy.deepcopy(load)
        o["fixture"]["fateRewriteLoadout_TEST_ONLY"]["preparedPointer"]=spec["proposedRelease"]["preparedPointer"]
        o["fixture"]["fateRewriteLoadout_TEST_ONLY"]["knownPointer"]=spec["proposedRelease"]["knownPointer"]
    add_transition(b,s,"FR-EP480-COMPAT-LOADOUT-01",consent["atMs"],2,"Add only the adopted branch-local ordinary slings and Wizard focus.",lm,["T","W","book-W","supportAndMarker"])
    tm,wm=prem["orderedApproachMovements"]
    def mt(x):
        o=x["overlay"]; o["nowMs"]=tm["endMs"]; a=o["actorOverrides"]["T"]; a["position"]=tm["end"]; a["budget"]["movement"]=tm["remainingMovement"]
        o.setdefault("movementHistory",[]).append(copy.deepcopy(tm))
    add_transition(b,s,tm["eventId"],tm["endMs"],1,"T completes the southern bypass within inherited movement.",mt,["T","W","book-W","supportAndMarker"])
    def mw(x):
        o=x["overlay"]; o["nowMs"]=wm["endMs"]; a=o["actorOverrides"]["W"]; a["position"]=wm["end"]; a["budget"]["movement"]=wm["remainingMovement"]
        o.setdefault("movementHistory",[]).append(copy.deepcopy(wm))
    add_transition(b,s,wm["eventId"],wm["endMs"],1,"W completes the north bypass after T; no body overlap or refresh.",mw,["T","W","book-W","supportAndMarker"])
    te=spec["targetEvent"]
    def pickup(x):
        o=x["overlay"]; o["nowMs"]=te["atMs"]; t=o["actorOverrides"]["T"]
        if t["budget"]["interaction"]!=1 or o["itemOverrides"]["book-W"]["custodian"]!="cache":raise AssertionError("pickup precondition")
        t["budget"]["interaction"]=0; item=o["itemOverrides"]["book-W"]
        item.update({"custodian":"T","carrier":"FR-EP480-T-BOOK-SLING-01","position":[10.75,-3.5,4.5]})
        ev={"eventId":te["eventId"],"atMs":te["atMs"],"kind":"atomic pickup","itemId":"book-W","owner":"W",
          "custodianBefore":"cache","custodianAfter":"T","carrierAfter":"FR-EP480-T-BOOK-SLING-01","itemObjectSha256Before":BOOK_SHA,
          "actor":"T","interactionSpent":1,"ActionSpent":0,"RPSpent":0,"pickupDistanceFt":te["pickupDistanceFt"]["T"],
          "supportMarkerPreserved":te["versionChecks"]["supportMarker"],"status":"active"}
        o.setdefault("custodyHistory",[]).append(ev); o["activeHistoryId"]=te["eventId"]; o["targetCustodyEvent"]=copy.deepcopy(ev)
    add_transition(b,s,te["eventId"],te["atMs"],1,"T spends its inherited Interaction to carry the same book from cache.",pickup,["T","W","book-W","obligation","terminalRecord","supportAndMarker"])
    b["targetEvent"]={**copy.deepcopy(te),"stateAtTargetSha256":b["transitions"][-1]["afterStateSHA256"],"targetAgeAtReleaseMs":1,"targetIsNewCompatibleCustodyEvent":True,"400DayOldProphecyCreationTargeted":False}
    r=spec["proposedRelease"]; sid="FR-EP480-COMPAT-ATOMIC-REPLACEMENT-01"
    def commit(x):
        o=x["overlay"]; o["nowMs"]=r["nowMs"]; t=o["actorOverrides"]["T"]
        if t["RP"]!=64 or t["budget"]["Action"]!=1 or t["pendingCast"] is not None or t["Dissonance"]!=0 or t["Refrain"]!=0 or t["seenFamilies"]!=[]:raise AssertionError("cast precondition")
        t["budget"]["Action"]=0;t["RP"]=38;t["seenFamilies"]=["fate-rewrite"];t["lastSpell"]="fate-rewrite";t["spellsThisTurn"]=1
        t["pendingCast"]={"spell":"fate-rewrite","targetEventId":te["eventId"],"committedAtMs":r["nowMs"],"ActionCommitted":True,"RPCommitted":26}
        o.setdefault("castHistory",[]).append({"spell":"fate-rewrite","caster":"T","class":"Wizard","classLevel":17,
          "knownPointer":r["knownPointer"],"preparedPointer":r["preparedPointer"],"profileSha256":r["profileSha256"],
          "components":r["components"],"ActionSpent":1,"RPSpent":26,"RPBefore":64,"RPAfter":38,
          "Dissonance":0,"Refrain":0,"seenFamilies":["fate-rewrite"],"lastSpell":"fate-rewrite","spellsThisTurn":1,
          "committedAtMs":r["nowMs"],"pendingCast":True,"TEST_ONLY":True})
    tr=add_transition(b,s,"FR-EP480-COMPAT-CAST-COMMIT-01",r["nowMs"],1,"Commit Action, 26 RP, and history once before counters.",commit,["T","W","book-W","obligation","terminalRecord","supportAndMarker"])
    tr["sourceReadVersions"]={"wizardProfileSha256":r["profileSha256"],"proposalSha256":P05_SHA}
    cw=r["counterWindow"]
    def response(x):
        o=x["overlay"];o["nowMs"]=r["nowMs"]; row=copy.deepcopy(cw)
        row.update({"eventId":"FR-EP480-COMPAT-COUNTER-RESPONSE-01","atMs":r["nowMs"],"choice":"voluntary decline",
          "ReactionSpent":False,"RPSpent":0,"rechargeOrFeedback":False})
        o.setdefault("responseWindows",[]).append(row)
    add_transition(b,s,"FR-EP480-COMPAT-COUNTER-RESPONSE-01",r["nowMs"],2,"W declines the eligible counter; no reaction, RP or recharge cost.",response,["T","W","book-W","supportAndMarker"])
    def settle(x):
        o=x["overlay"];o["nowMs"]=r["nowMs"];w=o["actorOverrides"]["W"];item=o["itemOverrides"]["book-W"]
        if w["budget"]["interaction"]!=1 or item["custodian"]!="T" or item["carrier"]!="FR-EP480-T-BOOK-SLING-01":raise AssertionError("settlement version/cost")
        if o["newObligations"][OID]["status"]!="fulfilled" or o["terminalRecord"]["atMs"]!=34560000099:raise AssertionError("protected source version changed")
        tx={"transactionId":sid,"idempotencyKey":sid,"atMs":r["nowMs"],
          "reservation":{"actor":"W","resource":"interaction","amount":1,"status":"reserved-before-transaction"},
          "writeOrder":["debit W reserved inherited Interaction","write book-W custody/carrier and dependent versions","commit all writes atomically"],
          "atomic":True,"allWritesCommitOrAbortTogether":True,"beforeBookSha256":digest(item)}
        w["budget"]["interaction"]-=1
        prior=copy.deepcopy(o["targetCustodyEvent"])
        rep={"eventId":sid,"atMs":r["nowMs"],"kind":"replacement custody outcome","supersedesEventId":te["eventId"],
          "itemId":"book-W","owner":"W","custodianBefore":"T","custodianAfter":"W","carrierAfter":"FR-EP480-W-BOOK-SLING-01",
          "positionAfter":[15.95,0,4.5],"interactionActor":"W","interactionSpent":1,"ActionSpent":0,"RPSpent":0,
          "itemObjectSha256Before":digest(item),"status":"active","TEST_ONLY":True}
        o.setdefault("immutableHistoryAudit",[]).append(prior)
        o.setdefault("supersededCausalEdges",[]).append({"fromEventId":te["eventId"],"toEventId":sid,
          "status":"superseded","originalTInteractionRemainsSunk":True})
        item.update({"custodian":"W","carrier":"FR-EP480-W-BOOK-SLING-01","position":[15.95,0,4.5]})
        o.setdefault("custodyHistory",[]).append(rep);o["activeHistoryId"]=sid;o["activeHistoryCount"]=1;o["successfulReplacement"]=copy.deepcopy(rep)
        tx.update({"afterBookSha256":digest(item),"committed":True,"WInteractionAfter":w["budget"]["interaction"]})
        o.setdefault("transactions",[]).append(tx)
        o.setdefault("outcomes",[]).append({"eventId":sid,"outcome":"success","result":"same unique book-W remains owned by W; current custodian/carrier W sling",
          "obligationPredicateReceiptTerminalUnchanged":True,"TOriginalInteractionSunk":True,"TActionAnd26RPSunk":True,
          "WAdditionalInteractionSpent":True,"noRefundOrRefresh":True})
        o["resolvedSuccessfully"]=True
    tr=add_transition(b,s,sid,r["nowMs"],3,"Reserve W Interaction; debit before custody/version writes inside one atomic replacement.",settle,["T","W","book-W","obligation","terminalRecord","supportAndMarker"])
    tr["sourceReadVersions"]={"obligationSha256":OBL_SHA,"terminalAfterSha256":TERMINAL_SHA,"bookObjectSha256BeforeTarget":BOOK_SHA,"proposalSha256":P05_SHA}
    settlement_hash=tr["afterStateSHA256"]
    def clear(x):
        o=x["overlay"];o["nowMs"]=r["nowMs"];t=o["actorOverrides"]["T"]
        if t["pendingCast"] is None:raise AssertionError("pending cast absent")
        t["pendingCast"]=None;o["pendingCastClearedAfterResolution"]=True
    add_transition(b,s,"FR-EP480-COMPAT-PENDING-CLEAR-01",r["nowMs"],4,"Clear the pending cast after resolution.",clear,["T","W","book-W","obligation"])
    b["finalStateSHA256"]=digest(s)
    b["idempotency"]={"key":sid,"firstCallPostStateSHA256":settlement_hash,"retryBeforeStateSHA256":settlement_hash,
      "retryAfterStateSHA256":settlement_hash,"sameKeyRetry":"NO_OP","noDuplicateCustodyOrHistory":True}
    b["terminalAssertions"]={"T1ParentAndFulfilledObligationPreserved":True,"nativePromiseChanged":False,"guaranteeProved":False,
      "firstCacheArrivalStillTrue":True,"oneUniqueBookObject":True,"finalCustodian":"W","finalCarrier":"FR-EP480-W-BOOK-SLING-01",
      "TInteractionSpent":1,"WInteractionSpent":1,"TActionSpent":1,"TRPSpent":26,"T_RP":38,"T_Action":0,
      "T_seenFamilies":["fate-rewrite"],"T_lastSpell":"fate-rewrite","T_spellsThisTurn":1,"W_RP":38,"W_Reaction":1,
      "noRefundRefreshOrReward":True,"oneActiveHistory":True,"immutableAuditRetainsSupersededPickup":True,
      "TF192_B02_B04Open":True,"Queue481Unchanged_836_12_0":True,"noSealOrIdentityAcceptanceApplication":True}
    b["costAndCustodyDeltas"]={"movementFt":{"T":13.901795,"W":29.2},"interactions":{"T_originalPickup":1,"W_additionalAlternative":1},
      "spell":{"T_Action":1,"T_RP":26,"CounterspellReaction":0,"CounterspellRP":0},
      "custody":{"cache_to_T":te["eventId"],"T_to_W":sid},"bookCount":1,"destroyed":False}
    b["atomicSettlementContract"]=copy.deepcopy(r["interactionCostSettlement"])
    b["forwardInverse"]={"transitionCount":len(b["transitions"]),"everyTransitionHasForwardAndInverse":True,
      "inverseRestoresBranchStartSHA256":b["branchStartStateSHA256"],"stateIsBranchLocal":True}
    return b

def build_conflict(proposal,start):
    spec=proposal["conflictingRequest"];bid=spec["branchId"];child=spec["executionChildId"]
    b=shell(spec,start);s=copy.deepcopy(start);expire(proposal,b,s)
    move=next(x for x in spec["branchTimeline"] if x.get("eventId")=="FR-EP480-CONFLICT-W-APPROACH-01")
    def mm(x):
        o=x["overlay"];o["nowMs"]=move["endMs"];w=o["actorOverrides"]["W"];w["position"]=move["end"]
        w["budget"]["movement"]=move["remainingMovement"];w["RP"]=38;o["actorOverrides"]["T"]["position"]=[5,0,0]
        o.setdefault("movementHistory",[]).append(copy.deepcopy(move))
    add_transition(b,s,move["eventId"],move["endMs"],1,"After fork/expiry W spends 20 ft on the supported north bypass.",mm,["T","W","book-W","obligation","supportAndMarker"])
    obs=spec["knowledgeRoutePremise"]["observer"]
    def observe(x):
        o=x["overlay"];o["nowMs"]=obs["atMs"];o.setdefault("observations",[]).append({"eventId":"FR-EP480-CONFLICT-POSTFORK-OBSERVATION-01",
          "atMs":obs["atMs"],"actor":"W","position":obs["position"],"site":obs["site"],"distanceFt":obs["distanceFt"],
          "samePlane":obs["samePlane"],"sightAndLoE":obs["sightAndLoE"],"ray":obs["ray"],"gateVolumeIntersected":False,
          "ActionInteractionRPCost":0,"observed":"W directly sees and recognizes own book-W at supported cache."})
    add_transition(b,s,"FR-EP480-CONFLICT-POSTFORK-OBSERVATION-01",obs["atMs"],1,"Record W's direct post-fork sighting on the clear ray.",observe,["W","book-W","supportAndMarker"])
    know=spec["knowledgeRoutePremise"]["postForkKnowledgeWrite"]
    def km(x):
        o=x["overlay"];o["nowMs"]=know["atMs"];o.setdefault("knowledgeOverlays",[]).append({**copy.deepcopy(know),
          "facts":["W's own cast","W's predicate and deadline","direct current sighting of own book-W at cache"],
          "reviewerEventIdsHashesHiddenFromCharacter":True})
    add_transition(b,s,know["eventId"],know["atMs"],1,"Add knowledge after observation; no pre-fork knowledge is invented.",km,["W","book-W","obligation","supportAndMarker"])
    now=spec["knowledgeRoutePremise"]["requestReadAtMs"];de=spec["decision"];target=spec["targetEvent"]
    def request(x):
        o=x["overlay"];o["nowMs"]=now;age=now-target["eventAtMs"]
        if age!=target["eventAgeMs"] or age>86400000:raise AssertionError("conflict age")
        rec={"eventId":"FR-EP480-CONFLICT-REQUEST-01","atMs":now,"requestingCaster":"W",
          "targetEventId":target["eventId"],"targetEventAtMs":target["eventAtMs"],"targetAgeMs":age,
          "ageCheck":"PASS","knowledgeCheck":"PASS under adopted TEST_ONLY overlay",
          "decision":"reject before commitment","reason":de["reason"],"orderedExecutionStage":de["stage"],
          "ActionSpent":False,"newRPSpent":0,"counterWindowOpened":False,"originalEP480PaymentSunk":26,
          "refund":False,"obligationReceiptTerminalUnchanged":True}
        o.setdefault("rewriteAttempts",[]).append(rec);o["lastRewriteAttempt"]=copy.deepcopy(rec)
    tr=add_transition(b,s,"FR-EP480-CONFLICT-REQUEST-01",now,1,"Reject at ordered step 3 before commitment or counter.",request,
      ["T","W","book-W","obligation","terminalRecord","supportAndMarker"])
    rh=tr["afterStateSHA256"];b["finalStateSHA256"]=digest(s);b["targetEvent"]=copy.deepcopy(target)
    b["idempotency"]={"key":"FR-EP480-CONFLICT-REQUEST-01","firstCallPostStateSHA256":rh,
      "retryBeforeStateSHA256":rh,"retryAfterStateSHA256":rh,"sameKeyRetry":"NO_OP","noDuplicateAttempt":True}
    b["knowledgeAndObservation"]={"forkAtMs":DEADLINE,"noKnowledgeWriteBeforeFork":True,
      "observationAtMs":obs["atMs"],"knowledgeWriteAtMs":know["atMs"],"requestAtMs":now,
      "eventAgeMs":now-target["eventAtMs"],"ageLimitMs":86400000,"reviewerBindingsRemainPrivate":True}
    b["terminalAssertions"]={"decision":"REJECT_BEFORE_COMMITMENT","ageCheckPasses":True,
      "knowledgeRoutePassesUnderTESTONLYPremise":True,"ActionSpent":False,"newRPSpent":0,"counterWindowOpened":False,
      "W_RP":38,"W_ActionAvailable":1,"W_ReactionAvailable":1,"originalEP480PaymentSunk":26,"refund":False,
      "bookStillAtCache":True,"custodyUnchanged":True,"obligationFulfilledReceiptTerminalUnchanged":True,
      "noPreForkObservationOrKnowledgeInvented":True,"noSealOrBlockerClosureOrIdentityAcceptanceApplication":True,
      "TF192_B02_B04Open":True,"Queue481Unchanged_836_12_0":True}
    b["costAndCustodyDeltas"]={"movementFt":{"W":20},"WRemainingMovementFt":10,"newActionSpent":0,
      "newRPSpent":0,"counterCost":0,"custodyWrites":0,"inheritedEP480CostRemainsSunkRP":26,"refund":False}
    b["forwardInverse"]={"transitionCount":len(b["transitions"]),"everyTransitionHasForwardAndInverse":True,
      "inverseRestoresBranchStartSHA256":b["branchStartStateSHA256"],"stateIsBranchLocal":True}
    return b

def verify_branch(b):
    s=copy.deepcopy(b["branchStartState"])
    if digest(s)!=b["branchStartStateSHA256"]:raise AssertionError("branch start")
    for t in b["transitions"]:
        if digest(s)!=t["beforeStateSHA256"]:raise AssertionError("forward before")
        vers=snapshot(s)
        if any(vers[k]!=v for k,v in t["readSetVersions"].items()):raise AssertionError("read versions")
        apply(s,t["forward"])
        if digest(s)!=t["afterStateSHA256"] or s["overlay"]["nowMs"]!=t["atMs"]:raise AssertionError("forward after/clock")
        for w in t["writeSetVersions"]:
            ex,v=tryget(s,w["path"])
            if ex!=w["exists"] or (ex and digest(v)!=w["sha256"]):raise AssertionError("write versions")
    if digest(s)!=b["finalStateSHA256"]:raise AssertionError("branch final")
    for t in reversed(b["transitions"]):
        apply(s,t["inverse"])
        if digest(s)!=t["beforeStateSHA256"]:raise AssertionError("inverse")
    if digest(s)!=b["branchStartStateSHA256"]:raise AssertionError("inverse fork")
    if b["forwardInverse"]["transitionCount"]!=len(b["transitions"]):raise AssertionError("transition count")

def write_json(path,obj):
    p=ROOT/path;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+"\n",encoding="utf-8",newline="\n")
def disk_bytes(obj):return (json.dumps(obj,ensure_ascii=False,indent=2)+"\n").encode("utf-8")
def build():
    raw=git_show(f"{BASE}:{P05_REL.as_posix()}")
    if sha(raw)!=P05_SHA:raise AssertionError("proposal SHA")
    prop=json.loads(raw)
    if prop["id"]!=P05 or prop["status"]!="SUBMITTED_FOR_DIRECTOR_READINESS_REVIEW":raise AssertionError("proposal immutability")
    mr=git_show(f"{BASE}:{MAN_REL.as_posix()}");manifest=json.loads(mr)
    pr=git_show(f"{BASE}:{PASS_REL.as_posix()}");passrec=json.loads(pr)
    if passrec["disposition"]!="PASS_FOR_OWNER_ADOPTION" or passrec["reviewedProposalSha256"]!=P05_SHA:raise AssertionError("Director pass")
    for f in manifest["files"]:
        r=git_show(f"{BASE}:{(COMPAT/f['path']).as_posix()}")
        if len(r)!=f["bytes"] or sha(r)!=f["sha256"]:raise AssertionError("P05 manifest "+f["path"])
    if manifest["files"][1]["sha256"]!=P05_SHA:raise AssertionError("manifest proposal")
    receipt={"schema":"DD_OWNER_ADOPTION_RECEIPT_V1","receiptId":"OWNER-ADOPTION-FR-EP480-P05-2026-11-03-01",
      "recordedAtUtc":ADOPTED_AT,"adoptionStatus":"ADOPTED_FOR_TWO_TEST_ONLY_WITNESS_BRANCHES",
      "proposal":{"id":P05,"path":P05_REL.as_posix(),"sha256":P05_SHA,"reviewedCommit":PASS_COMMIT,"baseMainCommit":BASE},
      "directorReadiness":{"disposition":"PASS_FOR_OWNER_ADOPTION","readbackPath":PASS_REL.as_posix(),"readbackCommit":BASE},
      "ownerResponse":RESPONSE,"acceptedOwnerAdoptionText":ADOPTION,
      "scope":{"authorizedBranches":["FR-EP480-IFACE-COMPAT-01","FR-EP480-IFACE-CONFLICT-01"],
       "authorizedWork":["Construct and submit these two bounded TEST_ONLY branches for Director evidence review."]},
      "authorityLimits":{"additionalPremises":False,"seal":False,"blockerClosure":False,
       "identityAcceptanceOrApplication":False,"canonChange":False,"runtimeChange":False,"campaignClaim":False,
       "queueChange":False,"nativeGuaranteeCertification":False},"proposalBytesChanged":False}
    write_json(RECEIPT,receipt); rr=(ROOT/RECEIPT).read_bytes()
    bindings=verify_sources(prop)
    traw=git_show(f"{BASE}:{T1_REL.as_posix()}")
    if sha(traw)!=T1_SHA:raise AssertionError("T1 packet hash")
    tp=json.loads(traw); sm={x["role"]:json.loads(git_show(f"{BASE}:{x['path']}")) for x in bindings if x["path"].endswith(".json")}
    parent_branch,t1=source_t1(prop,sm,tp)
    for x in (prop["compatibleRewrite"],prop["conflictingRequest"]):
        if x["branchStartStateSha256"]!=T1_FINAL:raise AssertionError("branch start binding")
    a=build_compat(prop,t1);b=build_conflict(prop,t1);verify_branch(a);verify_branch(b)
    q=sm["Queue481"]
    if (q["currentAuthority"]["reviewedApplied"],q["currentAuthority"]["pending"],q["acceptedUnapplied"])!=(836,12,0):raise AssertionError("Queue481 changed")
    if q["nextIdentity"]!="fate-rewrite" or q["nextBlockerIds"]!=["TF192-B04"] or q["nextDependencyIds"]!=["TF192-B02"]:raise AssertionError("handoff changed")
    passblob=subprocess.check_output(["git","rev-parse",f"{BASE}:{PASS_REL.as_posix()}"],cwd=ROOT,text=True).strip()
    manblob=subprocess.check_output(["git","rev-parse",f"{BASE}:{MAN_REL.as_posix()}"],cwd=ROOT,text=True).strip()
    tblob=subprocess.check_output(["git","rev-parse",f"{BASE}:{T1_REL.as_posix()}"],cwd=ROOT,text=True).strip()
    sources=bindings+[
      {"role":"proposal05_manifest","path":MAN_REL.as_posix(),"bytes":len(mr),"gitBlobSha1":manblob,"sha256":sha(mr)},
      {"role":"director_pass_transcription","path":PASS_REL.as_posix(),"bytes":len(pr),"gitBlobSha1":passblob,"sha256":sha(pr)},
      {"role":"accepted_static_only_EP480_T1_T4_packet","path":T1_REL.as_posix(),"bytes":len(traw),"gitBlobSha1":tblob,"sha256":sha(traw)},
      {"role":"owner_adoption_receipt","path":RECEIPT.as_posix(),"bytes":len(rr),"gitBlobSha1":None,"sha256":sha(rr)}]
    return {"schema":"FATE_REWRITE_EP480_INTERFACE_WITNESS_PACKET_V1","packetId":"FR-EP480-P05-TESTONLY-WITNESSES-2026-11-03",
      "classification":"TEST_ONLY_STATIC_INTERFACE_WITNESS_CONSTRUCTION","spellId":"fate-rewrite","blockerId":"TF192-B04",
      "reviewedProposal":{"id":P05,"sha256":P05_SHA,"commit":PASS_COMMIT,"bytesUnchanged":True},
      "ownerAdoptionReceipt":{"path":RECEIPT.as_posix(),"sha256":sha(rr),"response":RESPONSE,"scope":"two specified branches only"},
      "directorReadiness":{"disposition":"PASS_FOR_OWNER_ADOPTION","readbackPath":PASS_REL.as_posix(),"readbackSha256":sha(pr),
        "readbackGitBlobSha1":passblob,"readbackIsCodexTranscription":True},"baseMainCommit":BASE,
      "queueState":{"id":"CURRENT-SPELL-QUEUE-481","sha256":prop["queueState"]["sha256"],"reviewedApplied":836,"pending":12,
        "acceptedUnapplied":0,"nextIdentity":"fate-rewrite","nextBlockerIds":["TF192-B04"],
        "nextDependencyIds":["TF192-B02"],"queueChanged":False},
      "sourceBindings":sources,
      "parentWitness":{"path":T1_REL.as_posix(),"sha256":T1_SHA,"caseId":"EP480-T1",
        "branchStartStateSHA256":parent_branch["branchStartStateSHA256"],"finalStateSHA256":T1_FINAL,"state":t1},
      "sourceVersions":{"sourceParentStateSHA256":PARENT_SHA,"obligationId":OID,"obligationSHA256":OBL_SHA,
        "bookObjectSHA256":BOOK_SHA,"terminalAfterSHA256":TERMINAL_SHA,"proposal05SHA256":P05_SHA},
      "testOnlyControls":{"branchCount":2,"branchesIndependent":True,"eachForksFromExactT1Final":True,
        "nativePromiseUnchanged":True,"guaranteeProved":False,"noCampaignFact":True,"noCanonRuntimeCatalogIndexChange":True,
        "noSealOrBlockerClosure":True,"noIdentityAcceptanceOrApplication":True,"noQueueMutation":True,
        "historicalCasesAndQuestionDispositionsReplayed":False,"TF192_B02_B04RemainOpen":True},
      "branches":[a,b],"summary":{"branchCount":2,"compatibleBranch":"FR-EP480-IFACE-COMPAT-01",
        "conflictBranch":"FR-EP480-IFACE-CONFLICT-01","transitions":len(a["transitions"])+len(b["transitions"]),
        "allForwardAndInverseChecksPass":True,"bothInverseToT1Final":True,
        "spellIdentityAcceptanceOrApplication":False,"queueState":"836/12/0"}}

def request_text(packet):
    psha=sha(disk_bytes(packet)); rsha=packet["ownerAdoptionReceipt"]["sha256"]
    return f"""# Director evidence review — Fate Rewrite Proposal 05 branches

The owner adopted exact Proposal 05 solely to construct and submit these two bounded TEST_ONLY branches. Please review the evidence and return PASS, REVISE, or HOLD, bound to the commit in the submission message and the packet SHA-256 below.

- Adopted proposal: {P05}, SHA-256 {P05_SHA}; Director readiness PASS was recorded for commit {PASS_COMMIT}.
- Owner adoption receipt: {RECEIPT.as_posix()}, SHA-256 {rsha}.
- Witness packet: {PACKET.as_posix()}, SHA-256 {psha}.
- Packet manifest: {MANIFEST.as_posix()}.
- Source T1–T4 packet: {T1_REL.as_posix()}, SHA-256 {T1_SHA}.

Assess exact source/version binding, ordered transitions, route geometry and costs, the 1 ms compatible target, cast commitment before counters, W's Interaction reservation/debit before atomic custody/version writes, conflict observation and knowledge order, idempotency, and inverse restoration to T1 final hash {T1_FINAL}.

This is static TEST_ONLY evidence construction only. Preserve Queue481 at 836/12/0; keep TF192-B02 and TF192-B04 open; leave EP480 unsealed/static-only and do not accept/apply Fate Rewrite. No canon, runtime, campaign, seal, blocker, or queue change is requested.
"""
def main():
    packet=build();write_json(PACKET,packet)
    rq=request_text(packet);rp=ROOT/REQUEST;rp.parent.mkdir(parents=True,exist_ok=True);rp.write_text(rq,encoding="utf-8",newline="\n")
    entries=[]
    for p in (RECEIPT,PACKET,REQUEST,SCRIPT):
        raw=(ROOT/p).read_bytes();entries.append({"path":p.as_posix(),"bytes":len(raw),"sha256":sha(raw)})
    manifest={"schema":"DD_TESTONLY_WITNESS_PACKET_MANIFEST_V1","manifestId":"FR-EP480-P05-TESTONLY-WITNESS-MANIFEST-01",
      "classification":"TEST_ONLY_STATIC_INTERFACE_WITNESS_CONSTRUCTION",
      "proposal":{"id":P05,"sha256":P05_SHA,"readinessCommit":PASS_COMMIT},
      "ownerAdoptionReceipt":{"path":RECEIPT.as_posix(),"sha256":packet["ownerAdoptionReceipt"]["sha256"],
        "scope":["FR-EP480-IFACE-COMPAT-01","FR-EP480-IFACE-CONFLICT-01"]},
      "baseMainCommit":BASE,"files":entries,
      "queuePreservation":{"reviewedApplied":836,"pending":12,"acceptedUnapplied":0,"nextIdentity":"fate-rewrite",
        "openBlockers":["TF192-B02","TF192-B04"]},
      "constructionStatus":"TWO_BRANCHES_CONSTRUCTED_AWAITING_DIRECTOR_EVIDENCE_REVIEW",
      "noSealAcceptanceApplicationOrQueueChange":True}
    write_json(MANIFEST,manifest)
    actual=json.loads((ROOT/PACKET).read_text(encoding="utf-8"))
    if actual!=packet:raise AssertionError("serialized packet mismatch")
    for branch in actual["branches"]:verify_branch(branch)
    for item in manifest["files"]:
        raw=(ROOT/item["path"]).read_bytes()
        if len(raw)!=item["bytes"] or sha(raw)!=item["sha256"]:raise AssertionError("manifest mismatch "+item["path"])
    print("PASS branches="+str(len(actual["branches"]))+" transitions="+str(actual["summary"]["transitions"]))
    for branch in actual["branches"]:print("PASS "+branch["branchId"]+" "+branch["branchStartStateSHA256"]+" -> "+branch["finalStateSHA256"])
    print("PASS packet sha256="+sha((ROOT/PACKET).read_bytes()))
if __name__=="__main__":main()
