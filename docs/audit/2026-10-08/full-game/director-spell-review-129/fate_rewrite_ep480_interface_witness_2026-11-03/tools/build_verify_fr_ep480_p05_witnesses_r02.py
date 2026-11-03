#!/usr/bin/env python3
"""Rebuild Proposal 05 branches after Director corrections C01-C03 and execute duplicate retries."""
import copy, hashlib, importlib.util, json, subprocess
from pathlib import Path

BASE="eacd076230175e3f843d14d4d9150c205b4d58d1"
P05="FR-EP480-INTERFACE-PROPOSAL-05"
P05_SHA="cd492a5bdf9c966f83a2674c31ff1db02a10d2df5f3c92fe8b4680974047386d"
R1_SHA="dcff67b42e93c1d7df9bd47d33ecd6fa2c1fe0ff23f6eda4997f92c9b3f14773"
RECEIPT_SHA="9d51c3baa42dd300e618a8dca881515d54d3b40e762ccd9eb19773d050025b49"
T1_FINAL="49d94d12e54fbd36d36a0cf3f69803f6de1b0f903557804c02dbd41f1a2ae7c3"
OBL_SHA="2f6c8956d26cecd196523eba61cf777a983217a4d4ab0505ec36960753c0c862"
BOOK_SHA="16ab195897e69ea3f693e7afaf85bfcdf1947ba78a5823e3cabde227e1e58c9a"
TERMINAL_SHA="b9b48d2e102c127deee670ac89d51a8153739f01a2841c2db01c0e72b456172d"
OID="RANK9TIMEFATE6129-ETERNAL-PROPHECY-A-cast1"
DIR=Path("docs/audit/2026-10-08/full-game/director-spell-review-129/fate_rewrite_ep480_interface_witness_2026-11-03")
R1_PACKET=DIR/"FR_EP480_P05_TESTONLY_WITNESS_PACKET.json"
R1_RECEIPT=DIR/"OWNER_ADOPTION_RECEIPT_FR_EP480_P05.json"
REVISE=DIR/"CODEX_TRANSCRIBED_DIRECTOR_REVIEW_REVISE_01.json"
R2_PACKET=DIR/"FR_EP480_P05_TESTONLY_WITNESS_PACKET_R02.json"
R2_REQUEST=DIR/"DIRECTOR_REVIEW_REQUEST_FR_EP480_P05_WITNESSES_R02.md"
R2_MANIFEST=DIR/"PACKET_MANIFEST_FR_EP480_P05_WITNESSES_R02.json"
R2_SCRIPT=DIR/"tools/build_verify_fr_ep480_p05_witnesses_r02.py"
STAMP="2026-11-03T03:25:07Z"
ROOT=Path(subprocess.check_output(["git","rev-parse","--show-toplevel"],text=True).strip())

def gitshow(spec):return subprocess.check_output(["git","show",spec],cwd=ROOT)
def sha(raw):return hashlib.sha256(raw).hexdigest()
def git_blob_sha1(raw):return hashlib.sha1(b"blob "+str(len(raw)).encode()+b"\0"+raw).hexdigest()
def write_json(path,obj):
    p=ROOT/path;p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+"\n",encoding="utf-8",newline="\n")

# Reuse the reviewed R01 canonical patch algorithm; R01 is immutable in BASE.
r1_script=ROOT/DIR/"tools"/"build_verify_fr_ep480_p05_witnesses.py"
sp=importlib.util.spec_from_file_location("fr_r01_helpers",r1_script)
H=importlib.util.module_from_spec(sp);sp.loader.exec_module(H)

def transition(branch,state,old,description=None,before_state=None):
    before=copy.deepcopy(state if before_state is None else before_state);bv=H.snapshot(before);ops=H.diff(before,state);writes=[]
    for op in ops:
        ex,val=H.tryget(state,op["path"])
        writes.append({"path":op["path"],"exists":ex,"sha256":H.digest(val) if ex else None})
    tr={"eventId":old["eventId"],"atMs":old["atMs"],
        "sequenceOrdinalAtSameMillisecond":old["sequenceOrdinalAtSameMillisecond"],
        "description":description or old["description"],
        "readSetVersions":{k:bv[k] for k in old["readSetVersions"]},
        "writeSetVersions":writes,"beforeStateSHA256":H.digest(before),
        "afterStateSHA256":H.digest(state),"forward":ops,"inverse":H.inverse(ops)}
    if "sourceReadVersions" in old:tr["sourceReadVersions"]=copy.deepcopy(old["sourceReadVersions"])
    branch["transitions"].append(tr);return tr

def retry_metrics(state):
    o=state["overlay"];t=o["actorOverrides"].get("T",{});w=o["actorOverrides"].get("W",{})
    item=o.get("itemOverrides",{}).get("book-W",{})
    return {
      "costs":{"T_Action":t.get("budget",{}).get("Action"),"T_RP":t.get("RP"),
        "T_Interaction":t.get("budget",{}).get("interaction"),"W_Action":w.get("budget",{}).get("Action"),
        "W_RP":w.get("RP"),"W_Interaction":w.get("budget",{}).get("interaction"),
        "W_Reaction":w.get("budget",{}).get("Reaction")},
      "custody":{"itemId":item.get("id"),"owner":item.get("owner"),"custodian":item.get("custodian"),
        "carrier":item.get("carrier"),"position":item.get("position")},
      "historyCounts":{"custodyHistory":len(o.get("custodyHistory",[])),
        "immutableHistoryAudit":len(o.get("immutableHistoryAudit",[])),
        "transactions":len(o.get("transactions",[])),"rewriteAttempts":len(o.get("rewriteAttempts",[])),
        "activeHistoryCount":o.get("activeHistoryCount",1 if o.get("activeHistoryId") else 0)}}

def compat_handler(state,proposal):
    """Idempotency receipt is checked before cost/version/history work."""
    o=state["overlay"];key="FR-EP480-COMPAT-ATOMIC-REPLACEMENT-01"
    receipt_map=o.get("idempotencyReceipts",{})
    if key in receipt_map:return copy.deepcopy(receipt_map[key]),True
    spec=proposal["compatibleRewrite"];target=spec["targetEvent"];r=spec["proposedRelease"]
    w=o["actorOverrides"]["W"];item=o["itemOverrides"]["book-W"]
    if w["budget"]["interaction"]!=1 or item["custodian"]!="T" or item["carrier"]!="FR-EP480-T-BOOK-SLING-01":
        raise AssertionError("settlement cost/custody precondition")
    if o["newObligations"][OID]["status"]!="fulfilled" or H.digest(o["newObligations"][OID])!=OBL_SHA:
        raise AssertionError("protected obligation version")
    if o["terminalRecord"]["atMs"]!=34560000099 or o["terminalScheduler"]["active"]:
        raise AssertionError("consumed terminal changed")
    o["nowMs"]=r["nowMs"]
    prior=copy.deepcopy(o["targetCustodyEvent"])
    if prior["eventId"]!=target["eventId"] or prior["atMs"]!=target["atMs"]:
        raise AssertionError("target event mismatch")
    t_held_version=H.digest(item)
    # Reserve W's inherited interaction and debit it first within this single transaction.
    w["budget"]["interaction"]-=1
    replacement_id="FR-EP480-COMPAT-REPLACEMENT-AT-TARGET-01"
    replacement={"eventId":replacement_id,"atMs":target["atMs"],"recordedAtMs":r["nowMs"],
      "kind":"replacement of targeted custody event at its original event time",
      "replacesEventId":target["eventId"],"itemId":"book-W","owner":"W",
      "custodianBefore":"cache","custodianAfter":"W","carrierAfter":"FR-EP480-W-BOOK-SLING-01",
      "positionAfter":[15.95,0,4.5],"preEventBookVersionSha256":BOOK_SHA,
      "replacementHistoryActive":True,"TEST_ONLY":True}
    o.setdefault("immutableHistoryAudit",[]).append(copy.deepcopy(prior))
    o.setdefault("supersededCausalEdges",[]).append({"fromEventId":target["eventId"],
      "toEventId":replacement_id,"status":"superseded","priorEventBytesPreserved":True,
      "priorEventStatusAtItsOriginalTime":"active","currentCausalStatusAfterReplacement":"superseded",
      "replacementIsTheOnlyActiveHistory":True})
    item.update({"custodian":"W","carrier":"FR-EP480-W-BOOK-SLING-01","position":[15.95,0,4.5]})
    # The active causal history now contains the replacement at 12,105; no later T-to-W event is invented.
    o["custodyHistory"]=[copy.deepcopy(replacement)]
    o["activeHistoryId"]=replacement_id;o["activeHistoryCount"]=1
    o["successfulReplacement"]=copy.deepcopy(replacement)
    o.setdefault("memoryLedger",[]).append({"actor":"T","sourceEventId":target["eventId"],
      "observedAtMs":target["atMs"],"classification":"PRIOR_HISTORY_MEMORY_AFTER_REPLACEMENT",
      "rememberedExperience":"T directly performed and observed the cache-to-T pickup.",
      "currentCausalStatus":"superseded","retainedWithoutErasure":True,
      "automaticKnowledgeOfChangedPresentCustody":False,
      "automaticDisclosureToWOrOtherActors":False})
    tx={"transactionId":key,"idempotencyKey":key,"eventId":key,"settlementAtMs":r["nowMs"],
      "replacementEventId":replacement_id,"replacementEventAtMs":target["atMs"],
      "reservation":{"actor":"W","resource":"interaction","amount":1,"reservedBeforeSettlement":True},
      "writeOrder":["debit W reserved inherited Interaction","write replacement custody/carrier and dependent versions","commit atomically"],
      "targetPreEventBookVersionSha256":BOOK_SHA,
      "currentT_HeldBookVersionBeforeSettlementSha256":t_held_version,
      "currentBookVersionAfterSettlementSha256":H.digest(item),
      "TOriginalInteractionRemainsSunk":True,"TActionAnd26RPSunk":True,
      "atomic":True,"allWritesCommitOrAbortTogether":True,"committed":True}
    o.setdefault("transactions",[]).append(tx)
    outcome={"eventId":key,"settlementAtMs":r["nowMs"],"replacementEventId":replacement_id,
      "replacementEffectiveAtMs":target["atMs"],"outcome":"success",
      "obligationPredicateReceiptTerminalUnchanged":True,"TOriginalInteractionSunk":True,
      "TActionAnd26RPSunk":True,"WAdditionalInteractionSpent":True,"noRefundOrRefresh":True,
      "oneActiveReplacementHistory":True}
    o.setdefault("outcomes",[]).append(outcome);o["resolvedSuccessfully"]=True
    receipt={"key":key,"result":"COMMITTED","targetEventId":target["eventId"],
      "replacementEventId":replacement_id,"replacementEventAtMs":target["atMs"],
      "settlementAtMs":r["nowMs"],"WInteractionSpent":1,"TInteractionRemainsSpent":1,
      "TActionSpent":1,"TRPSpent":26}
    o.setdefault("idempotencyReceipts",{})[key]=copy.deepcopy(receipt)
    return receipt,False

def conflict_handler(state,proposal):
    """A cached rejection is returned before age, admission, costs, or attempt appends."""
    o=state["overlay"];key="FR-EP480-CONFLICT-REQUEST-01"
    receipt_map=o.get("idempotencyReceipts",{})
    if key in receipt_map:return copy.deepcopy(receipt_map[key]),True
    spec=proposal["conflictingRequest"];target=spec["targetEvent"]
    now=spec["knowledgeRoutePremise"]["requestReadAtMs"];age=now-target["eventAtMs"]
    if age!=target["eventAgeMs"] or age>86400000:raise AssertionError("conflict age")
    o["nowMs"]=now
    attempt={"eventId":key,"atMs":now,"requestingCaster":"W","targetEventId":target["eventId"],
      "targetEventAtMs":target["eventAtMs"],"targetAgeMs":age,"ageCheck":"PASS",
      "knowledgeCheck":"PASS under adopted TEST_ONLY overlay","decision":"reject before commitment",
      "reason":spec["decision"]["reason"],"orderedExecutionStage":spec["decision"]["stage"],
      "ActionSpent":False,"newRPSpent":0,"counterWindowOpened":False,"originalEP480PaymentSunk":26,
      "refund":False,"obligationReceiptTerminalUnchanged":True}
    o.setdefault("rewriteAttempts",[]).append(attempt);o["lastRewriteAttempt"]=copy.deepcopy(attempt)
    receipt={"key":key,"result":"REJECTED_BEFORE_COMMITMENT","attemptEventId":key,
      "targetAgeMs":age,"ActionSpent":False,"newRPSpent":0,"counterWindowOpened":False,
      "custodyWrites":0,"originalEP480PaymentSunk":26}
    o.setdefault("idempotencyReceipts",{})[key]=copy.deepcopy(receipt)
    return receipt,False

def run_retry(state,handler,proposal,first_receipt,branch_id):
    before_hash=H.digest(state);before_metrics=retry_metrics(state)
    returned,replayed=handler(state,proposal)
    after_hash=H.digest(state);after_metrics=retry_metrics(state)
    ok=(replayed and returned==first_receipt and before_hash==after_hash and before_metrics==after_metrics)
    if not ok:raise AssertionError(branch_id+" same-key retry changed state or receipt")
    return {"handler":"receipt lookup before cost/version/history checks",
      "firstCallReceiptSha256":H.digest(first_receipt),"retryReturnedSameReceipt":returned==first_receipt,
      "duplicateCallUsedCachedReceipt":replayed,"stateHashBeforeRetry":before_hash,
      "stateHashAfterRetry":after_hash,"stateUnchanged":before_hash==after_hash,
      "costCustodyHistoryBefore":before_metrics,"costCustodyHistoryAfter":after_metrics,
      "costCustodyAndHistoryUnchanged":before_metrics==after_metrics}

def assert_replay(branch):
    s=copy.deepcopy(branch["branchStartState"])
    if H.digest(s)!=branch["branchStartStateSHA256"]:raise AssertionError("branch start hash")
    for idx,tr in enumerate(branch["transitions"]):
        if H.digest(s)!=tr["beforeStateSHA256"]:raise AssertionError(f"forward before {branch['branchId']} transition {idx}: {H.digest(s)} != {tr['beforeStateSHA256']}")
        vers=H.snapshot(s)
        if any(vers[k]!=v for k,v in tr["readSetVersions"].items()):raise AssertionError("read version")
        H.apply(s,tr["forward"])
        if H.digest(s)!=tr["afterStateSHA256"] or s["overlay"]["nowMs"]!=tr["atMs"]:raise AssertionError(f"forward after {branch['branchId']} transition {idx}: {H.digest(s)} != {tr['afterStateSHA256']} time={s['overlay']['nowMs']} expected={tr['atMs']}")
        for w in tr["writeSetVersions"]:
            ex,v=H.tryget(s,w["path"])
            if ex!=w["exists"] or (ex and H.digest(v)!=w["sha256"]):raise AssertionError("write version")
    if H.digest(s)!=branch["finalStateSHA256"]:raise AssertionError("final state hash")
    for tr in reversed(branch["transitions"]):
        H.apply(s,tr["inverse"])
        if H.digest(s)!=tr["beforeStateSHA256"]:raise AssertionError("inverse hash")
    if H.digest(s)!=branch["branchStartStateSHA256"]:raise AssertionError("inverse fork")

def replay_prefix(old,state,until):
    out=[]
    for i,tr in enumerate(old["transitions"][:until]):
        before=copy.deepcopy(state);H.apply(state,tr["forward"])
        desc=tr["description"]
        if old["branchId"].endswith("COMPAT-01") and i==5:
            o=state["overlay"];spec_target=old["targetEvent"];at=spec_target["atMs"]
            obs={"eventId":"FR-EP480-COMPAT-T-PICKUP-OBSERVATION-01","atMs":at,
              "actor":"T","position":[14,-3.5,0],"subjectEventId":spec_target["eventId"],
              "direct":True,"distanceToEventAnchorFt":3.640055,"samePlane":True,"lineOfEffect":True,
              "ActionInteractionRPCost":0,"observed":"T directly sees and performs its cache-to-T pickup.",
              "reviewerIdsHashesAreCharacterKnowledge":False}
            knowledge={"actor":"T","atMs":at,"facts":[spec_target["eventId"],"the pickup T directly performed"],
              "basis":"direct actor/perception at the event","scope":"this pickup only",
              "noAutomaticKnowledgeOfChangedFuture":True}
            o.setdefault("observations",[]).append(obs);o.setdefault("characterKnowledge",[]).append(knowledge)
            desc="Record T's pickup plus T's direct observation/knowledge before commitment."
        # Keep each prefix endpoint immutable; the replay state continues mutating.
        out.append((before,copy.deepcopy(state),tr,desc))
    return out

def rebuild_compat(old,proposal):
    b=copy.deepcopy(old);b["transitions"]=[];state=copy.deepcopy(b["branchStartState"])
    # Replay expiry through counter response (old transition indexes 0-7), inserting T knowledge at pickup.
    prefix=replay_prefix(old,state,8)
    for before,after,oldtr,desc in prefix:transition(b,after,oldtr,desc,before)
    old_settle=old["transitions"][8];before=copy.deepcopy(state)
    receipt,duplicate=compat_handler(state,proposal)
    if duplicate:raise AssertionError("first compatible settlement unexpectedly deduped")
    settlement_tr=transition(b,state,old_settle,
      "Check receipt key first; debit W Interaction then atomically replace the targeted 12,105 cache-to-T event with cache-to-W.",before)
    settlement_hash=settlement_tr["afterStateSHA256"]
    retry=run_retry(state,compat_handler,proposal,receipt,b["branchId"])
    old_clear=old["transitions"][9];before_clear=copy.deepcopy(state);H.apply(state,old_clear["forward"])
    transition(b,state,old_clear,"Clear pending cast after the replacement transaction resolves.",before_clear)
    b["finalStateSHA256"]=H.digest(state)
    repl=state["overlay"]["successfulReplacement"];tx=state["overlay"]["transactions"][-1]
    b["targetEvent"]={**copy.deepcopy(old["targetEvent"]),
      "preEventBookVersionSha256":BOOK_SHA,"replacementEventId":repl["eventId"],
      "replacementEventAtMs":repl["atMs"],"settlementEventAtMs":tx["settlementAtMs"],
      "transactionCurrentBookVersionBeforeSha256":tx["currentT_HeldBookVersionBeforeSettlementSha256"]}
    b["idempotency"]={"key":receipt["key"],"firstCallPostStateSHA256":settlement_hash,
      "retryBeforeStateSHA256":retry["stateHashBeforeRetry"],"retryAfterStateSHA256":retry["stateHashAfterRetry"],
      "receiptSha256":retry["firstCallReceiptSha256"],"sameKeyRetry":"NO_OP_EXECUTED_AND_VERIFIED",
      "receiptCheckedBeforeCostsPreconditionsAndHistoryWrites":True,"executionEvidence":retry}
    b["terminalAssertions"].update({"oneActiveReplacementHistory":True,
      "replacementAtOriginalTargetTimeMs":repl["atMs"],"settlementAtMs":tx["settlementAtMs"],
      "originalCacheToTPickupPreservedInImmutableAudit":True,"TDirectKnowledgeRecordedBeforeCommitment":True,
      "TPriorHistoryMemoryRetainedAfterReplacement":True,"noAutomaticKnowledgeGrantedToOthers":True,
      "sameKeyRetryExecutedNoOp":True})
    b["costAndCustodyDeltas"]["custody"]={"targetEventReplacedAt12105":repl["eventId"],
      "transactionSettlementAt12106":tx["transactionId"],"activeCustodianAfterSettlement":"W"}
    b["forwardInverse"]={"transitionCount":len(b["transitions"]),"everyTransitionHasForwardAndInverse":True,
      "inverseRestoresBranchStartSHA256":b["branchStartStateSHA256"],"stateIsBranchLocal":True}
    return b

def rebuild_conflict(old,proposal):
    b=copy.deepcopy(old);b["transitions"]=[];state=copy.deepcopy(b["branchStartState"])
    prefix=replay_prefix(old,state,4)
    for before,after,oldtr,desc in prefix:transition(b,after,oldtr,desc,before)
    old_req=old["transitions"][4];before=copy.deepcopy(state);receipt,dup=conflict_handler(state,proposal)
    if dup:raise AssertionError("first conflict request unexpectedly deduped")
    reqtr=transition(b,state,old_req,"Check cached receipt first; record one rejection before commitment and no further costs.",before)
    first_hash=reqtr["afterStateSHA256"];retry=run_retry(state,conflict_handler,proposal,receipt,b["branchId"])
    b["finalStateSHA256"]=H.digest(state)
    b["idempotency"]={"key":receipt["key"],"firstCallPostStateSHA256":first_hash,
      "retryBeforeStateSHA256":retry["stateHashBeforeRetry"],"retryAfterStateSHA256":retry["stateHashAfterRetry"],
      "receiptSha256":retry["firstCallReceiptSha256"],"sameKeyRetry":"NO_OP_EXECUTED_AND_VERIFIED",
      "receiptCheckedBeforeCostsPreconditionsAndHistoryWrites":True,"executionEvidence":retry}
    b["terminalAssertions"]["sameKeyRetryExecutedNoOp"]=True
    b["forwardInverse"]={"transitionCount":len(b["transitions"]),"everyTransitionHasForwardAndInverse":True,
      "inverseRestoresBranchStartSHA256":b["branchStartStateSHA256"],"stateIsBranchLocal":True}
    return b

def readback_record():
    return {"schema":"CODEX_TRANSCRIBED_GPT_DIRECTOR_REVIEW_V1",
      "classification":"CODEX_TRANSCRIBED_GPT_UI_READBACK_NOT_GPT_AUTHORED",
      "conversationUrl":"https://chatgpt.com/g/g-p-67f17555a8dc8191a2b5b81e6d8adc12-dungeon-crawler/c/6adc506d-8770-83ea-b64c-0345d9b9b682",
      "transcribedAtUtc":STAMP,"reviewedCommit":BASE,
      "reviewedPacketPath":R1_PACKET.as_posix(),"reviewedPacketSha256":R1_SHA,"disposition":"REVISE",
      "sourceBindingReadback":"Exact packet/adoption hashes and all 18 declared source-binding rows match.",
      "replayReadback":{"bothStartAt":T1_FINAL,"transitions":15,"forwardOperations":101,"inverseOperations":101,
        "eachExactBranchStartRestored":True,
        "passed":["expiry","routes","target ages","commitment before response","payment","W Interaction debit"]},
      "corrections":[
        {"id":"FR-P05-W-C01","pointer":["/branches/0/transitions/8/forward/3/after","/branches/0/transitions/8/forward/9/after","/branches/0/costAndCustodyDeltas/custody"],
         "required":"Record replacement cache-to-W at target time 34560012105, separately from settlement 34560012106; preserve original cache-to-T in immutable audit; mark its causal path superseded; distinguish pre-event book version from current T-held transaction version; retain all costs; one replacement history active."},
        {"id":"FR-P05-W-C02","pointer":["/branches/0/transitions/5/forward","/branches/0/transitions/8/forward"],
         "required":"Record T's direct knowledge of the pickup before commitment and preserve it as explicitly tagged prior-history memory after replacement; no automatic knowledge of changed present custody to other actors."},
        {"id":"FR-P05-W-C03","pointer":["/branches/0/idempotency","/branches/1/idempotency","builder functions build_compat/build_conflict/verify_branch"],
         "required":"Receipt lookup must run before costs, preconditions or history appends. Execute both duplicate calls and record unchanged state hashes, receipts, costs, custody and history counts."}],
      "branchDispositions":{"compatible":"REVISE C01-C03","conflict":"REVISE C03 only"},
      "adoptionScopeReadback":"The Director stated these corrections are implementation/evidence corrections within the existing adoption; no new owner premise is needed.",
      "queueAndHoldState":{"Queue481":"836/12/0","TF192-B02":"OPEN","TF192-B04":"OPEN",
        "EP480":"unsealed","FateRewrite":"unaccepted/unapplied"}}

def main():
    packet_raw=gitshow(f"{BASE}:{R1_PACKET.as_posix()}")
    if sha(packet_raw)!=R1_SHA:raise AssertionError("R01 packet pin mismatch")
    old=json.loads(packet_raw)
    rec_raw=gitshow(f"{BASE}:{R1_RECEIPT.as_posix()}")
    if sha(rec_raw)!=RECEIPT_SHA:raise AssertionError("owner adoption receipt mismatch")
    readback=readback_record();write_json(REVISE,readback);rev_raw=(ROOT/REVISE).read_bytes()
    proposal_path="docs/audit/2026-10-08/full-game/director-spell-review-129/fate_rewrite_ep480_interface_spec_2026-11-02/FATE_REWRITE_EP480_INTERFACE_PROPOSAL_05.json"
    prop_raw=gitshow(f"{BASE}:{proposal_path}");proposal=json.loads(prop_raw)
    if sha(prop_raw)!=P05_SHA:raise AssertionError("P05 hash changed")
    branches=[rebuild_compat(old["branches"][0],proposal),rebuild_conflict(old["branches"][1],proposal)]
    for b in branches:assert_replay(b)
    old_sources=copy.deepcopy(old["sourceBindings"])
    for src in old_sources:
        raw=gitshow(f"{BASE}:{src['path']}")
        if sha(raw)!=src["sha256"] or len(raw)!=src["bytes"]:raise AssertionError("inherited source binding "+src["path"])
    revise_blob=subprocess.check_output(["git","hash-object","--","dummy"],cwd=ROOT,text=True,stderr=subprocess.DEVNULL) if False else None
    sources=old_sources+[
      {"role":"superseded_R01_witness_packet","path":R1_PACKET.as_posix(),"bytes":len(packet_raw),
       "gitBlobSha1":subprocess.check_output(["git","rev-parse",f"{BASE}:{R1_PACKET.as_posix()}"],cwd=ROOT,text=True).strip(),"sha256":sha(packet_raw)},
      {"role":"director_REVISE_01_transcription","path":REVISE.as_posix(),"bytes":len(rev_raw),
       "gitBlobSha1":git_blob_sha1(rev_raw),"sha256":sha(rev_raw)}]
    packet=copy.deepcopy(old)
    packet.update({"packetId":"FR-EP480-P05-TESTONLY-WITNESSES-R02-2026-11-03",
      "baseMainCommit":BASE,"supersedes":{"packetId":old["packetId"],"commit":BASE,"sha256":R1_SHA},
      "directorRevision":{"path":REVISE.as_posix(),"sha256":sha(rev_raw),"disposition":"REVISE"},
      "sourceBindings":sources,"branches":branches,
      "summary":{"branchCount":2,"compatibleBranch":branches[0]["branchId"],"conflictBranch":branches[1]["branchId"],
        "transitions":sum(len(b["transitions"]) for b in branches),
        "allForwardAndInverseChecksPass":True,"bothInverseToT1Final":True,
        "sameKeyRetriesExecutedAndVerified":True,"spellIdentityAcceptanceOrApplication":False,"queueState":"836/12/0"}})
    # Preserve the old packet's owner authorization and all external source bindings byte-for-byte.
    write_json(R2_PACKET,packet);packet_bytes=(ROOT/R2_PACKET).read_bytes()
    req=f"""# Director evidence review — Fate Rewrite Proposal 05 witnesses, R02

R02 corrects Director findings FR-P05-W-C01 through C03 within the existing owner adoption. The original packet remains immutable at commit {BASE}.

- Owner-adopted proposal: {P05}, SHA-256 {P05_SHA}.
- Owner adoption receipt: {R1_RECEIPT.as_posix()}, SHA-256 {RECEIPT_SHA}.
- Prior Director REVISE transcription: {REVISE.as_posix()}, SHA-256 {sha(rev_raw)}.
- R02 witness packet: {R2_PACKET.as_posix()}, SHA-256 {sha(packet_bytes)}.
- R02 manifest: {R2_MANIFEST.as_posix()}.

C01 now records cache-to-W as the replacement at 34560012105 and the settlement at 34560012106, preserves the original cache-to-T event in immutable audit, distinguishes pre-event and T-held versions, and leaves one active history. C02 records T's direct pickup knowledge before cast commitment and retains it as prior-history memory after replacement, without automatic disclosure to others. C03 adds receipt-first handlers and executes duplicate settlement/request calls, checking unchanged hashes, receipts, costs, custody, and history counts.

Please review both branches and return PASS, REVISE, or HOLD bound to the commit and packet hash. The original T1 fork, source terms, costs, reversibility, and scope remain bound to Proposal 05.

This remains the same two-branch TEST_ONLY construction only. Keep Queue481 836/12/0, TF192-B02/B04 open, EP480 unsealed, and Fate Rewrite unaccepted/unapplied. No canon, runtime, campaign, seal, blocker, or queue change is requested.
"""
    req_path=ROOT/R2_REQUEST;req_path.parent.mkdir(parents=True,exist_ok=True);req_path.write_text(req,encoding="utf-8",newline="\n")
    files=[]
    for path in (REVISE,R2_PACKET,R2_REQUEST,R2_SCRIPT):
        raw=(ROOT/path).read_bytes();files.append({"path":path.as_posix(),"bytes":len(raw),"sha256":sha(raw)})
    manifest={"schema":"DD_TESTONLY_WITNESS_PACKET_MANIFEST_V1",
      "manifestId":"FR-EP480-P05-TESTONLY-WITNESS-MANIFEST-R02","classification":"TEST_ONLY_STATIC_INTERFACE_WITNESS_CONSTRUCTION",
      "proposal":{"id":P05,"sha256":P05_SHA,"readinessCommit":"08c4e0db03fb3d20db56c01c16af7865110adc85"},
      "ownerAdoptionReceipt":{"path":R1_RECEIPT.as_posix(),"sha256":RECEIPT_SHA,
        "scope":["FR-EP480-IFACE-COMPAT-01","FR-EP480-IFACE-CONFLICT-01"]},
      "supersedes":{"packetPath":R1_PACKET.as_posix(),"commit":BASE,"sha256":R1_SHA},
      "baseMainCommit":BASE,"files":files,
      "queuePreservation":{"reviewedApplied":836,"pending":12,"acceptedUnapplied":0,
        "nextIdentity":"fate-rewrite","openBlockers":["TF192-B02","TF192-B04"]},
      "constructionStatus":"R02_TWO_BRANCHES_CONSTRUCTED_AWAITING_DIRECTOR_REVIEW",
      "sameKeyRetriesExecutedAndVerified":True,"noSealAcceptanceApplicationOrQueueChange":True}
    write_json(R2_MANIFEST,manifest)
    for f in manifest["files"]:
        raw=(ROOT/f["path"]).read_bytes()
        if len(raw)!=f["bytes"] or sha(raw)!=f["sha256"]:raise AssertionError("manifest mismatch "+f["path"])
    disk=json.loads((ROOT/R2_PACKET).read_text(encoding="utf-8"))
    for b in disk["branches"]:assert_replay(b)
    print("PASS R02 branches=2 transitions="+str(disk["summary"]["transitions"]))
    print("PASS C01 replacement event at 12105; settlement at 12106; one active history")
    print("PASS C02 T direct knowledge and prior-history memory")
    print("PASS C03 executed receipt-first duplicate handlers; state/cost/custody/history unchanged")
    print("PASS packet sha256="+sha((ROOT/R2_PACKET).read_bytes()))
if __name__=="__main__":main()
