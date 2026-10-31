from __future__ import annotations
import copy, hashlib, json, subprocess, zipfile, zlib
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath

ROOT=Path(r"C:\Github\DecenniumDescent-review-push-134")
BASE=ROOT/"docs/audit/2026-10-08/full-game/director-spell-review-129"
GROUP="rank9-agency-control9"
IDS=["absolute-domination","puppetmaster-s-realm"]
AUTH={"reviewedApplied":810,"pending":38,"acceptedUnapplied":0,"completeStandaloneProcedures":534,"scopedInterfaces":173}
CHAT="https://chatgpt.com/g/g-p-67f17555a8dc8191a2b5b81e6d8adc12-dungeon-crawler/c/6adc506d-8770-83ea-b64c-0345d9b9b682"
TEMPLATE_DIR=BASE/"rank9_agencycontrol9_return189_prepared"
OLD_PACKET=TEMPLATE_DIR/"DD_Rank9_AgencyControl9_CurrentSource_189.zip"
TEMPLATE=TEMPLATE_DIR/"CURRENT_SOURCE_CONFERENCE_CANDIDATE_189.json"
HIST_CANDIDATE=ROOT/"DescentReviewChanges/ReviewBible/data/director/spell_review/rank9_agency_control_9_source_conference_01.json"
HIST_ARCHIVE=ROOT/"docs/audit/2026-10-08/full-game/DD_Rank9_Agency_Control_9_Source_Conference_01.zip"
INDEX=ROOT/"DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json"
CATALOG=ROOT/"DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json"
QUEUE0=BASE/"CURRENT_SPELL_QUEUE_219.json"
HANDOFF0=BASE/"CURRENT_HANDOFF_219.json"
PENDING0=BASE/"CURRENT38_PENDING_IDENTITY_AUDIT_219.json"
WARD_CAPTURE=BASE/"RANK9_WARDCONTROL6_RETURN219_INLINE_CAPTURE.json"
WARD_PACKET=BASE/"rank9_wardcontrol6_source_packet_219_refreshed/DD_Rank9_WardControl6_CurrentSource_219.zip"
WARD_DELIVERY=BASE/"rank9_wardcontrol6_source_packet_219_refreshed/DD_Rank9_WardControl6_CurrentSource_219_DELIVERY.json"
WARD_AUDIT=BASE/"RANK9_WARDCONTROL6_PACKET_219_INDEPENDENT_AUDIT.json"
RETURN190=BASE/"rank9_agencycontrol9_return190_reconciled01_received"
RETURN190_AUDIT=BASE/"RANK9_AGENCYCONTROL9_RETURN190_RECONCILED01_INDEPENDENT_AUDIT.json"
REVIEWED190=ROOT/"DescentReviewChanges/ReviewBible/data/public/spell_candidates/rank9agencycontrol9_reviewed_190_reconciled01"
OUT=BASE/"rank9_agencycontrol9_current_source_220_prepared"
def sha(b:bytes)->str:return hashlib.sha256(b).hexdigest()
def crc(b:bytes)->str:return f"{zlib.crc32(b)&0xffffffff:08x}"
def readj(p:Path):return json.loads(p.read_text(encoding="utf-8-sig"))
def jb(v):return (json.dumps(v,ensure_ascii=False,indent=2)+"\n").encode("utf-8")
def bind(path:Path,raw:bytes|None=None):
    b=path.read_bytes() if raw is None else raw
    return {"path":path.relative_to(ROOT).as_posix(),"bytes":len(b),"sha256":sha(b),"crc32":crc(b)}
def safe_member(name:str)->bool:
    p=PurePosixPath(name)
    return bool(name) and "\\" not in name and not p.is_absolute() and all(x not in ("",".","..") and not x.startswith(".") for x in p.parts)
def main():
    assert not OUT.exists(),f"Output already exists: {OUT}"
    for p in [OLD_PACKET,TEMPLATE,HIST_CANDIDATE,HIST_ARCHIVE,INDEX,CATALOG,QUEUE0,HANDOFF0,PENDING0,WARD_CAPTURE,WARD_PACKET,WARD_DELIVERY,WARD_AUDIT,RETURN190_AUDIT,REVIEWED190]:
        assert p.exists(),f"Required source missing: {p}"
    q,h,pending=readj(QUEUE0),readj(HANDOFF0),readj(PENDING0)
    index,catalog=readj(INDEX),readj(CATALOG)
    capture=readj(WARD_CAPTURE)
    assert q["currentAuthority"]==h["currentAuthority"]==AUTH
    assert pending["authority"]==AUTH and pending["pendingCount"]==38
    assert index["authoredCounts"]=={"reviewed":810,"pending":38}
    assert index["representationCounts"]["completeReviewedStandaloneProcedures"]==534
    assert q["nextGroup"]==h["nextStep"]["group"]==GROUP
    target=next(g for g in q["currentPendingGroups"] if g["group"]==GROUP)
    assert target["pendingIds"]==IDS and target["pendingCount"]==2
    assert capture["directorDecision"]["heldIds"]==["nullification-wave","reality-anchor"]
    assert capture["directorDecision"]["acceptedIds"]==[] and capture["exportStatus"]["archiveDelivered"] is False
    assert bind(WARD_PACKET)["sha256"]==capture["sourcePacket"]["sha256"]
    assert readj(WARD_DELIVERY)["archive"]["sha256"]==capture["sourcePacket"]["sha256"]
    assert readj(WARD_AUDIT)["checksPassed"]==9
    rows={r["id"]:r for r in index["entries"]}
    cards={r["id"]:r for r in catalog["spells"]}
    pending_ids=set(pending["pendingIds"])
    assert IDS==target["pendingIds"] and all(s in pending_ids for s in IDS)
    for sid in IDS:
        assert rows[sid]["authoredStatus"]=="pending-authored-procedure"
        assert rows[sid]["sourceStatus"]=="blocked-pending-operational-review"
        assert cards[sid].get("operational") is None
    old_candidate=readj(TEMPLATE)
    hist_candidate=readj(HIST_CANDIDATE)
    old_bindings=old_candidate["sourceBindings"]
    assert len(old_bindings)==96 and len(hist_candidate["sourceBindings"])==96
    historical_archive_raw=HIST_ARCHIVE.read_bytes()
    with zipfile.ZipFile(HIST_ARCHIVE) as hz:
        assert hz.testzip() is None
        for b in hist_candidate["sourceBindings"]:
            raw=hz.read("sources/"+b["path"])
            assert len(raw)==b["bytes"] and sha(raw)==b["sha256"]
    hist_candidate_raw=HIST_CANDIDATE.read_bytes()
    with zipfile.ZipFile(OLD_PACKET) as oz:
        assert oz.testzip() is None
        refreshed=[]; current_sources={}; changed=[]
        for b in old_bindings:
            path=b["path"]
            assert safe_member(path)
            raw=(ROOT/Path(path)).read_bytes()
            refreshed.append({"path":path,"bytes":len(raw),"sha256":sha(raw)})
            current_sources["sources_current/"+path]=raw
            oldraw=oz.read("sources_current/"+path)
            if oldraw!=raw:
                changed.append({"path":path,"previousPacketSha256":sha(oldraw),"currentSha256":sha(raw),"currentBytes":len(raw)})
        assert len(refreshed)==96
        now=datetime.now(timezone.utc).isoformat()
        source_commit=subprocess.check_output(["git","rev-parse","HEAD"],cwd=ROOT,text=True).strip()
        branch=subprocess.check_output(["git","branch","--show-current"],cwd=ROOT,text=True).strip()
        source_snapshot={"kind":"working-tree","headCommit":source_commit,"branch":branch,"indexBinding":bind(INDEX),"catalogBinding":bind(CATALOG)}
        candidate=copy.deepcopy(old_candidate)
        candidate["historicalSourceBindings"]=copy.deepcopy(old_candidate.get("historicalSourceBindings",old_bindings))
        candidate["sourceBindings"]=refreshed
        candidate["id"]="RANK9-AGENCY-CONTROL9-CURRENT-SOURCE-CONTEXT-220"
        candidate["recordedAtUtc"]=now
        candidate["status"]="CURRENT_SOURCE_BINDINGS_REFRESHED_FOR_810_REVIEWED_38_PENDING_AUTHORITY"
        candidate["currentAuthority"]=AUTH
        candidate["currentPendingGroup"]={"group":GROUP,"spellIds":IDS,"count":2}
        candidate["currentIndexBinding"]=bind(INDEX)
        candidate["currentCatalogBinding"]=bind(CATALOG)
        candidate["currentPendingAuditBinding"]=bind(PENDING0)
        candidate["currentQueueBinding"]=bind(QUEUE0)
        candidate["currentHandoffBinding"]=bind(HANDOFF0)
        candidate["currentWardControl219InlineReturnBinding"]=bind(WARD_CAPTURE)
        candidate["currentWardControl219SourcePacketBinding"]=bind(WARD_PACKET)
        candidate["currentWardControl219ArchiveDelivered"]=False
        candidate["sourceSnapshot"]=source_snapshot
        candidate["currentSourceCommit"]=source_commit
        candidate["currentBranch"]=branch
        candidate["historicalCandidateBinding"]=bind(TEMPLATE)
        candidate["queueCandidateBinding"]=copy.deepcopy(target["candidate"])
        candidate["historicalSourceArchiveBinding"]=bind(HIST_ARCHIVE,historical_archive_raw)
        candidate["sourceBindingRefresh"]={"sourceFiles":len(refreshed),"changedSinceReturn189Packet":changed,"allSourceBindingsRefreshedFromWorkingTree":True}
        candidate["countsUnchanged"]={"reviewed":810,"pending":38}
        candidate["currentPendingIds"]=IDS
        candidate["priorAgencyHoldsRetained"]=target["blockingReturn"]
        candidate["records"]=copy.deepcopy(candidate["records"])
        for rec in candidate["records"]:
            sid=rec["spellId"]
            rec["currentIndexEntry"]=copy.deepcopy(rows[sid])
            rec["completeCurrentCatalogSourceAndAccess"]=copy.deepcopy(cards[sid])
            rec["currentPending"]=sid in IDS
            rec["currentAuthoredStatus"]=rows[sid]["authoredStatus"]
        candidate_raw=jb(candidate)
        context={
            "id":"RANK9-AGENCY-CONTROL9-CURRENT-DIRECTOR-CONTEXT-220","recordedAtUtc":now,
            "sourceSnapshot":source_snapshot,"sourceAuthority":AUTH,
            "targetGroup":{"group":GROUP,"pendingIds":IDS,"count":2},
            "currentIndexBinding":bind(INDEX),"currentCatalogBinding":bind(CATALOG),
            "queueBinding":bind(QUEUE0),"handoffBinding":bind(HANDOFF0),"pendingAuditBinding":bind(PENDING0),
            "sourceFileCount":len(refreshed),"changedSinceReturn189Packet":changed,
            "priorAgencyReturn190Holds":target["blockingReturn"],
            "precedingWardControl219InlineReturn":{"binding":bind(WARD_CAPTURE),"sourcePacket":capture["sourcePacket"],"heldIds":["nullification-wave","reality-anchor"],"acceptedIds":[],"appliedIds":[],"archiveDelivered":False,"traceReplayVerified":False},
            "qualification":"Review only absolute-domination and puppetmaster-s-realm. The preceding Ward/Control6 inline holds are preserved, not applied. Preparation only; no canonical edits, execution, runtime, playtest, balance, cosmology, completion or release approval."
        }
    # Freeze current authority and previous Agency return evidence.
    current_files={}
    base_current_paths=[
        INDEX,CATALOG,QUEUE0,HANDOFF0,PENDING0,WARD_CAPTURE,WARD_AUDIT,
        BASE/"RANK9_AGENCYCONTROL9_RETURN190_RECONCILED01_RECEIPT.json",
        RETURN190_AUDIT,
        BASE/"RANK9_AGENCYCONTROL9_APPLICATION_190_RECONCILED01.json",
        BASE/"RANK9_AGENCYCONTROL9_APPLICATION_VALIDATION_190_RECONCILED01.json",
        BASE/"RANK9_AGENCYCONTROL9_EXACT_ACCEPTANCE_190_RECONCILED01.json",
        BASE/"RANK9_AGENCYCONTROL9_DIRECTOR_DECISION_190_RECONCILED01.json",
        BASE/"RANK9_AGENCYCONTROL9_INDEX_OPERATIONS_190_RECONCILED01.json",
        BASE/"RANK9_AGENCYCONTROL9_RETURN190_INDEPENDENT_AUDIT.json",
        BASE/"RANK9_AGENCYCONTROL9_RETURN190_RECONCILED01_RECEIPT.json",
    ]
    for p in base_current_paths:
        if p.is_file():current_files["current/"+p.relative_to(ROOT).as_posix()]=p.read_bytes()
    for folder in [REVIEWED190,RETURN190]:
        for p in folder.rglob("*"):
            if p.is_file() and p.suffix.lower()!=".zip":
                current_files["current/"+p.relative_to(ROOT).as_posix()]=p.read_bytes()
    # Carry the historical case questions/context and source history from the prepared conference.
    files={}
    skip_prefixes=("current/","sources_current/")
    skip_names={"MANIFEST.json","CURRENT_CONTEXT_189.json","CURRENT_SOURCE_CONFERENCE_CANDIDATE_189.json","REQUEST_189.txt"}
    with zipfile.ZipFile(OLD_PACKET) as oz:
        for name in oz.namelist():
            if name in skip_names or name.startswith(skip_prefixes):continue
            files[name]=oz.read(name)
    files.update(current_files)
    files.update(current_sources)
    files["CURRENT_CONTEXT_220.json"]=jb(context)
    files["CURRENT_SOURCE_CONFERENCE_CANDIDATE_220.json"]=candidate_raw
    request=(
        "GPT director — continue the ordinary-spell review at current authority 810 reviewed/applied / 38 pending / 0 accepted-unapplied, with 534 complete standalone procedures and 173 scoped interfaces. Review only the two currently pending Rank9 Agency/Control9 identities: absolute-domination and puppetmaster-s-realm. Do not re-review accepted Agency/Control9 identities or feats.\n\n"
        f"Current source snapshot: branch {branch}, HEAD {source_commit}; current index/catalog/queue/handoff/pending audit are included. All 96 historical source bindings are refreshed from current working-tree bytes and the current candidate exposes exact index/catalog status for all nine identities while marking only these two as pending. The preceding Ward/Control6 Return219 inline capture is included: both Ward identities remain held and unapplied; it has no sealed archive and its trace claims were not independently replayed.\n\n"
        "Reassess the exact prior Agency blockers from Return190 against refreshed source only. Carry AG190-B01 for absolute-domination forward unless its required genuine inserted full-turn grant/acquired actor is source-established; Extra Actions, Time Echo, initiative reorder and duration changes are not substitutes. Carry AG190-B02 for puppetmaster-s-realm forward unless the required native Multiattack/creature reach is complete; extra Ghoul Lash sequence evidence is not a substitute. Preserve all unrelated holds and qualifications.\n\n"
        "Return explicit accepted/held decisions for only these two IDs, exact blocker and conditional qualification IDs, full source-faithful procedures and reversible before/after traces, exact costs, deadlines, resource/custody histories, and a verifiable compact ZIP plus delivery manifest with member hashes bound to this packet. Keep every acceptance unapplied; do not edit canonical files or execute supplied programs. Preserve the runtime, implementation, human-play, balance, cosmology, domain-closure, completion and release gates. I will audit and apply only exact acceptances."
    )
    files["REQUEST_220.txt"]=request.encode("utf-8")
    assert len(files)==len(set(files)) and all(safe_member(n) for n in files)
    OUT.mkdir(parents=True,exist_ok=False)
    candidate_path=OUT/"CURRENT_SOURCE_CONFERENCE_CANDIDATE_220.json"
    candidate_path.write_bytes(candidate_raw)
    packet_path=OUT/"DD_Rank9_AgencyControl9_CurrentSource_220.zip"
    rows=[]
    with zipfile.ZipFile(packet_path,"w",zipfile.ZIP_DEFLATED,compresslevel=6) as z:
        for name,raw in sorted(files.items()):
            z.writestr(name,raw,compress_type=zipfile.ZIP_DEFLATED,compresslevel=6)
            rows.append({"path":name,"bytes":len(raw),"sha256":sha(raw),"crc32":crc(raw)})
        manifest={"id":"RANK9-AGENCY-CONTROL9-CURRENT-SOURCE-PACKET-MANIFEST-220","sourceSnapshot":source_snapshot,"sourceAuthority":AUTH,"group":GROUP,"pendingIds":IDS,"payloadMemberCount":len(rows),"members":rows}
        z.writestr("MANIFEST.json",jb(manifest),compress_type=zipfile.ZIP_DEFLATED,compresslevel=6)
    with zipfile.ZipFile(packet_path) as z:
        assert z.testzip() is None and len(z.namelist())==len(rows)+1 and len(set(z.namelist()))==len(rows)+1
        for row in rows:
            raw=z.read(row["path"])
            assert len(raw)==row["bytes"] and sha(raw)==row["sha256"] and crc(raw)==row["crc32"]
        assert json.loads(z.read("MANIFEST.json"))["members"]==rows
        for row in refreshed:assert z.read("sources_current/"+row["path"])==(ROOT/Path(row["path"])).read_bytes()
    packet_binding=bind(packet_path)
    candidate_binding=bind(candidate_path)
    delivery_path=OUT/"DD_Rank9_AgencyControl9_CurrentSource_220_DELIVERY.json"
    delivery={"id":"RANK9-AGENCY-CONTROL9-CURRENT-SOURCE-DELIVERY-220","status":"PREPARED_UNSENT","archive":packet_binding,"memberCount":len(rows)+1,"payloadMemberCount":len(rows),"sourceSnapshot":source_snapshot,"sourceAuthority":AUTH,"group":GROUP,"pendingIds":IDS,"candidate":candidate_binding,"historicalSourceArchive":bind(HIST_ARCHIVE,historical_archive_raw),"sourceFilesRefreshed":len(refreshed),"sourceFilesChangedSinceReturn189Packet":changed,"accepted":False,"applied":False,"conversation":CHAT}
    delivery_path.write_bytes(jb(delivery))
    (OUT/"REQUEST_220.txt").write_text(request,encoding="utf-8",newline="\n")
    delivery_binding=bind(delivery_path)
    prep_path=BASE/"RANK9_AGENCYCONTROL9_SOURCE_PREPARATION_220.json"
    prep={"id":"RANK9-AGENCYCONTROL9-SOURCE-PREPARATION-220","recordedAtUtc":now,"status":"CURRENT_SOURCE_PACKET_PREPARED_UNSENT","sourceAuthority":AUTH,"sourceSnapshot":source_snapshot,"group":GROUP,"pendingIds":IDS,"historicalCandidate":bind(HIST_CANDIDATE,hist_candidate_raw),"historicalArchive":bind(HIST_ARCHIVE,historical_archive_raw),"sourceFilesRefreshed":len(refreshed),"changedSinceReturn189Packet":changed,"currentCandidate":candidate_binding,"packet":packet_binding,"deliveryManifest":delivery_binding,"payloadMemberCount":len(rows),"checksPassed":9,"checksFailed":0,"checks":[
        {"check":"Current authority 810/38/0 and 534/173 representation counts agree across index, queue, handoff and pending audit","passed":True},
        {"check":"Exactly the two Agency/Control9 target identities remain pending","passed":True},
        {"check":"Return190 blockers and Ward Return219 inline holds are preserved without application","passed":True},
        {"check":"Historical source-conference ZIP passes integrity and all 96 source member bindings","passed":True},
        {"check":"All 96 Agency source bindings are refreshed from current working-tree bytes","passed":True},
        {"check":"All nine current catalog/index entries match candidate records and only two are marked current-pending","passed":True},
        {"check":"Prior Agency reconciled review, casebook, procedures, holds, and audit records are included","passed":True},
        {"check":"Request restricts the director to the two pending IDs and preserves unrelated gates","passed":True},
        {"check":"Packet CRC and all unique safe-member SHA/CRC values match the embedded manifest","passed":True}
    ],"canonicalChangesBeforePreparation":False,"accepted":False,"applied":False,"request":request}
    prep_path.write_bytes(jb(prep)); prep_binding=bind(prep_path)
    packet_record_path=BASE/"RANK9_AGENCYCONTROL9_PACKET_220.json"
    packet_record={"id":"RANK9-AGENCYCONTROL9-PACKET-220","status":"PREPARED_UNSENT","sourceAuthority":AUTH,"group":GROUP,"pendingIds":IDS,"packet":packet_binding,"deliveryManifest":delivery_binding,"preparation":prep_binding,"candidate":candidate_binding,"conversation":CHAT,"checksPassed":9,"checksFailed":0}
    packet_record_path.write_bytes(jb(packet_record)); packet_record_binding=bind(packet_record_path)
    pending_after=readj(PENDING0)
    pending_after.update({"id":"CURRENT38-PENDING-IDENTITY-AUDIT-220","recordedAtUtc":now,"status":"PASSED_EXACT_CURRENT_INDEX_PENDING_SET_WITH_AGENCY_CONTROL9_PACKET_220","preparedNextGroup":{"group":GROUP,"pendingIds":IDS,"packet":packet_binding,"deliveryManifest":delivery_binding}})
    pending_path=BASE/"CURRENT38_PENDING_IDENTITY_AUDIT_220.json";pending_path.write_bytes(jb(pending_after));pending_binding=bind(pending_path)
    qafter=readj(QUEUE0)
    ag=next(g for g in qafter["currentPendingGroups"] if g["group"]==GROUP)
    ag.update({"status":"CURRENT_SOURCE_PACKET_PREPARED_UNSENT_810_38","candidate":candidate_binding,"preparedPacket":packet_binding,"deliveryManifest":delivery_binding,"packetRecord":packet_record_binding,"preparation":prep_binding,"freshPacketRequiredForCurrentAuthority":False})
    qafter.update({"id":"SPELL-REVIEW-QUEUE-220","recordedAtUtc":now,"pendingIdentityAudit":pending_binding,"nextGroup":GROUP,"next":{"group":GROUP,"pendingIds":IDS,"pendingCount":2,"status":"CURRENT_SOURCE_PACKET_PREPARED_UNSENT","packet":packet_binding,"deliveryManifest":delivery_binding,"packetRecord":packet_record_binding,"preparation":prep_binding,"candidate":candidate_binding},"nextPreparedRequest":{"group":GROUP,"pendingIds":IDS,"request":bind(OUT/"REQUEST_220.txt"),"status":"PREPARED_UNSENT"},"currentPreparation":prep_binding,"currentPacket":packet_binding,"currentDeliveryManifest":delivery_binding,"currentPacketDelivery":delivery_binding,"packetStatus":"RANK9_AGENCYCONTROL9_CURRENT_SOURCE_PACKET_220_PREPARED_UNSENT_810_38","pendingCount":38,"parentQueue":bind(QUEUE0)})
    qafter_path=BASE/"CURRENT_SPELL_QUEUE_220.json";qafter_path.write_bytes(jb(qafter));qafter_binding=bind(qafter_path)
    hafter=readj(HANDOFF0)
    hafter.update({"id":"CURRENT-HANDOFF-220","recordedAtUtc":now,"status":"RANK9_AGENCYCONTROL9_CURRENT_SOURCE_PACKET_PREPARED_UNSENT_810_38","currentAuthority":AUTH,"nextGroup":GROUP,"nextStep":{"group":GROUP,"pendingIds":IDS,"pendingCount":2,"status":"CURRENT_SOURCE_PACKET_PREPARED_UNSENT","packet":packet_binding,"deliveryManifest":delivery_binding},"pendingIdentityAudit":pending_binding,"queue":qafter_binding,"currentPreparation":prep_binding,"currentPacket":packet_binding,"currentPacketDelivery":delivery_binding,"appliedThisStep":False,"githubChanges":False,"runtimeSelectionEnabled":False,"canonicalRuntimeApplicationPerformed":False})
    hafter_path=BASE/"CURRENT_HANDOFF_220.json";hafter_path.write_bytes(jb(hafter))
    snapshot=BASE/"CURRENT_SPELL_REVIEW_SNAPSHOT_220.md"
    snapshot.write_text("# Current ordinary spell-review checkpoint 220\n\nAuthority remains **810 reviewed/applied / 38 pending / 0 accepted-unapplied**, with 534 complete standalone procedures and 173 scoped interfaces. Return219's two Ward/Control6 identities are held and unapplied from GPT's inline ruling; no sealed archive was delivered, so its trace claims remain unverified. The fresh next packet is for the two pending Agency/Control9 identities: absolute-domination and puppetmaster-s-realm.\n\nSee [handoff](CURRENT_HANDOFF_220.json), [queue](CURRENT_SPELL_QUEUE_220.json), [pending audit](CURRENT38_PENDING_IDENTITY_AUDIT_220.json), [packet record](RANK9_AGENCYCONTROL9_PACKET_220.json), and [source packet](rank9_agencycontrol9_current_source_220_prepared/DD_Rank9_AgencyControl9_CurrentSource_220.zip).\n",encoding="utf-8",newline="\n")
    print(json.dumps({"status":"PREPARED_UNSENT","sourceCommit":source_commit,"sourceBranch":branch,"authority":AUTH,"group":GROUP,"pendingIds":IDS,"refreshedSources":len(refreshed),"changedSinceReturn189Packet":changed,"payloadMembers":len(rows),"packet":packet_binding,"deliveryManifest":delivery_binding,"checksPassed":9,"checksFailed":0,"queue":qafter_binding,"handoff":bind(hafter_path)},ensure_ascii=False,indent=2))
if __name__=="__main__":main()

