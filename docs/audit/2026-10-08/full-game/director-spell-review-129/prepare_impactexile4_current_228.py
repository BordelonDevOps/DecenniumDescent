from __future__ import annotations
import copy, hashlib, json, subprocess, zipfile, zlib
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
AUDIT = ROOT / "docs/audit/2026-10-08/full-game/director-spell-review-129"
FULL = ROOT / "docs/audit/2026-10-08/full-game"
GROUP, TARGETS = "rank9-impact-exile4", ["reverse-gravity-field"]
CLOSED = ["eternal-anvil", "transmute-flesh-to-energy", "planar-collapse"]
BLOCKER = {"reverse-gravity-field": ["IE204-B02"]}
AUTH = {"reviewedApplied": 811, "pending": 37, "acceptedUnapplied": 0,
        "completeStandaloneProcedures": 535, "scopedInterfaces": 173}
INDEX = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json"
CATALOG = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json"
QUEUE227, HANDOFF227, PENDING227 = (AUDIT / n for n in ("CURRENT_SPELL_QUEUE_227.json", "CURRENT_HANDOFF_227.json", "CURRENT37_PENDING_IDENTITY_AUDIT_227.json"))
QUEUE228, HANDOFF228, PENDING228 = (AUDIT / n for n in ("CURRENT_SPELL_QUEUE_228.json", "CURRENT_HANDOFF_228.json", "CURRENT37_PENDING_IDENTITY_AUDIT_228.json"))
SNAPSHOT = AUDIT / "CURRENT_SPELL_REVIEW_SNAPSHOT_228.md"
OUT = AUDIT / "rank9_impactexile4_current_source_228_prepared"
ARCHIVE, DELIVERY = OUT / "DD_Rank9_ImpactExile4_CurrentSource_228.zip", OUT / "DD_Rank9_ImpactExile4_CurrentSource_228_DELIVERY.json"
CANDIDATE_FILE, CONTEXT_FILE, REQUEST_FILE = (OUT / n for n in ("CURRENT_SOURCE_CONFERENCE_CANDIDATE_228.json", "CURRENT_CONTEXT_228.json", "REQUEST_228.txt"))
PREP, PACKET = AUDIT / "RANK9IMPACTEXILE4_SOURCE_PREPARATION_228.json", AUDIT / "RANK9IMPACTEXILE4_PACKET_228.json"
START = ROOT / "START_HERE.md"
HIST_CANDIDATE = ROOT / "DescentReviewChanges/ReviewBible/data/director/spell_review/rank9_impact_exile_4_source_conference_01.json"
HIST_ARCHIVE, NOTES = FULL / "DD_Rank9_Impact_Exile_4_Source_Conference_01.zip", AUDIT / "RANK9IMPACTEXILE4_NEXT_CONFERENCE_NOTES_129.json"
R204 = AUDIT / "rank9_impactexile4_return204_received"
R205 = AUDIT / "rank9_impactexile4_return205_received"
R227 = AUDIT / "rank9_summonhosts5_return227_received"
R205_ZIP, R205_DELIVERY = R205 / "DD_Rank9_ImpactExile4_Director_Return205.zip", R205 / "DD_Rank9_ImpactExile4_Director_Return205_DELIVERY.json"
R204_ZIP = R204 / "DD_Rank9_ImpactExile4_Director_Return204_UNACCEPTED.zip"
R204_DELIVERY = R204 / "DD_Rank9_ImpactExile4_Director_Return204_UNACCEPTED_DELIVERY.json"
R205_AUDIT, R205_RECEIPT = AUDIT / "RANK9IMPACTEXILE4_RETURN205_INDEPENDENT_AUDIT.json", AUDIT / "RANK9IMPACTEXILE4_RETURN205_RECEIPT.json"
R205_DECISION, R205_ACCEPTANCE = AUDIT / "RANK9IMPACTEXILE4_DIRECTOR_DECISION_205.json", AUDIT / "RANK9IMPACTEXILE4_EXACT_ACCEPTANCE_205.json"
R205_APP, R205_VALIDATION = AUDIT / "RANK9IMPACTEXILE4_APPLICATION_205.json", AUDIT / "RANK9IMPACTEXILE4_APPLICATION_VALIDATION_205.json"
R204_AUDIT, R204_RECEIPT, R204_CARRY = (AUDIT / n for n in ("RANK9IMPACTEXILE4_RETURN204_INDEPENDENT_AUDIT.json", "RANK9IMPACTEXILE4_RETURN204_RECEIPT.json", "RANK9IMPACTEXILE4_RETURN204_CARRY_FORWARD_AUDIT.json"))
R227_DELIVERY, R227_AUDIT, R227_RECEIPT = R227 / "DD_Rank9_SummonHosts3_Director_Return227_DELIVERY.json", AUDIT / "RANK9SUMMONHOSTS5_RETURN227_INDEPENDENT_AUDIT.json", AUDIT / "RANK9SUMMONHOSTS5_RETURN227_RECEIPT.json"
R227_SUBMISSION, R227_PACKET = AUDIT / "RANK9SUMMONHOSTS5_PACKET_227_SUBMISSION.json", AUDIT / "RANK9SUMMONHOSTS5_PACKET_227.json"
CHAT = "https://chatgpt.com/g/g-p-67f17555a8dc8191a2b5b81e6d8adc12-dungeon-crawler/c/6adc506d-8770-83ea-b64c-0345d9b9b682"

def sha(b): return hashlib.sha256(b).hexdigest()
def crc(b): return f"{zlib.crc32(b) & 0xffffffff:08x}"
def dump(v): return (json.dumps(v, ensure_ascii=False, indent=2) + "\n").encode()
def read(p): return json.loads(p.read_text(encoding="utf-8-sig"))
def info(p, raw=None):
    b = p.read_bytes() if raw is None else raw
    return {"path": p.relative_to(ROOT).as_posix(), "bytes": len(b), "sha256": sha(b), "crc32": crc(b)}
def row(path, raw):
    blob = hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()
    return {"path": path, "bytes": len(raw), "sha256": sha(raw), "gitBlobSHA1": blob}

def main():
    if any(p.exists() for p in (OUT, PREP, PACKET, QUEUE228, HANDOFF228, PENDING228, SNAPSHOT)):
        raise FileExistsError("Refusing to overwrite packet228 outputs")
    head = subprocess.check_output(["git","rev-parse","HEAD"],cwd=ROOT,text=True).strip()
    branch = subprocess.check_output(["git","branch","--show-current"],cwd=ROOT,text=True).strip()
    assert branch == "main"
    index, catalog, q227, h227, p227 = map(read, (INDEX,CATALOG,QUEUE227,HANDOFF227,PENDING227))
    group = next(x for x in q227["currentPendingGroups"] if x["group"] == GROUP)
    assert q227["currentAuthority"] == h227["currentAuthority"] == p227["authority"] == AUTH
    assert group["pendingIds"] == TARGETS and group["freshPacketRequiredForCurrentAuthority"] is True
    assert p227["pendingCount"] == 37 and set(TARGETS) <= set(p227["pendingIds"])
    assert index["authoredCounts"] == {"reviewed":811,"pending":37}
    assert index["representationCounts"]["completeReviewedStandaloneProcedures"] == 535
    live = sorted(x["id"] for x in index["entries"] if x.get("authoredStatus") == "pending-authored-procedure")
    assert live == sorted(p227["pendingIds"]) and len(live) == 37
    entries, spells = {x["id"]:x for x in index["entries"]}, {x["id"]:x for x in catalog["spells"]}
    assert entries[TARGETS[0]]["sourceStatus"] == "blocked-pending-operational-review"
    assert all(entries[s]["authoredStatus"] == "reviewed-authored-operational-playtest" for s in CLOSED)
    assert all(s in spells for s in TARGETS + CLOSED)

    hist_raw = subprocess.check_output(["git", "cat-file", "blob", f"{head}:{HIST_CANDIDATE.relative_to(ROOT).as_posix()}"], cwd=ROOT)
    hist_zip_raw = HIST_ARCHIVE.read_bytes()
    historical = json.loads(hist_raw.decode("utf-8-sig"))
    assert len(hist_raw) == group["candidate"]["bytes"] and sha(hist_raw) == group["candidate"]["sha256"]
    assert len(hist_zip_raw) == group["archive"]["bytes"] and sha(hist_zip_raw) == group["archive"]["sha256"]
    hist_by_id = {x["spellId"]:x for x in historical["records"]}
    assert set(CLOSED + TARGETS) <= set(hist_by_id)
    hist_bindings = historical["sourceBindings"]
    with zipfile.ZipFile(HIST_ARCHIVE) as z:
        assert z.testzip() is None and len(z.namelist()) == len(set(z.namelist()))
        for x in hist_bindings:
            b = z.read("sources/" + x["path"])
            assert len(b) == x["bytes"] and sha(b) == x["sha256"]

    r205_audit,r205_receipt,r205_decision,r205_accept,r205_app,r205_val = map(read,(R205_AUDIT,R205_RECEIPT,R205_DECISION,R205_ACCEPTANCE,R205_APP,R205_VALIDATION))
    r227_audit,r227_receipt,r227_delivery = map(read,(R227_AUDIT,R227_RECEIPT,R227_DELIVERY))
    assert r205_audit["status"] == "PASS" and r205_receipt["acceptedIds"] == CLOSED
    assert r205_decision["blockers"]["reverse-gravity-field"]["blockerRecords"][0]["id"] == "IE204-B02"
    assert set(r205_accept.get("acceptedIds",[])) == set(CLOSED) and r205_app["acceptedIds"] == CLOSED and r205_val["status"] == "PASS"
    assert r227_audit["status"] == r227_receipt["status"] == "PASS" and r227_delivery["accepted"] is False and r227_delivery["applied"] is False

    now = datetime.now(timezone.utc).isoformat()
    lines = START.read_text(encoding="utf-8-sig").splitlines()
    lines[0] = ("**Current ordinary spell-review handoff [228](docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT_HANDOFF_228.json):** "
        "Return227 independently audited and held all three Summon Hosts5 targets; authority remains **811 reviewed-applied / 37 pending / 0 accepted-unapplied**. "
        "The fresh Impact/Exile4 packet is scoped to reverse-gravity-field; the three Return205 acceptances remain closed. "
        "See [packet record](docs/audit/2026-10-08/full-game/director-spell-review-129/RANK9IMPACTEXILE4_PACKET_228.json).")
    START.write_text("\n".join(lines)+"\n",encoding="utf-8",newline="\n")

    p228 = copy.deepcopy(p227)
    p228.update({"id":"CURRENT37-PENDING-IDENTITY-AUDIT-228","recordedAtUtc":now,
        "status":"PASSED_EXACT_CURRENT_INDEX_PENDING_SET_AFTER_RETURN227","authority":AUTH,
        "indexBinding":info(INDEX),"catalogBinding":info(CATALOG),
        "auditedReturn227":{"heldIds":r227_receipt["heldIds"],
            "blockers":{"summon-elemental-avatar":["SH202-B01"],"summon-herald-of-the-planes":["SH202-B02"],"summon-avatar-of-decay":["SH202-B03"]},
            "independentAudit":info(R227_AUDIT),"authorityUnchanged":AUTH},
        "preparedNextGroup":{"group":GROUP,"pendingIds":TARGETS,"pendingCount":1,"status":"CURRENT_SOURCE_PACKET_228_PREPARED_UNSENT"}})
    PENDING228.write_bytes(dump(p228))

    extras = [
        "START_HERE.md", INDEX.relative_to(ROOT).as_posix(), CATALOG.relative_to(ROOT).as_posix(),
        QUEUE227.relative_to(ROOT).as_posix(), HANDOFF227.relative_to(ROOT).as_posix(), PENDING227.relative_to(ROOT).as_posix(),
        "DescentReviewChanges/ReviewBible/data/public/spell_candidates/transport6_reviewed_128/MODEL.json",
        "DescentReviewChanges/ReviewBible/data/public/spell_candidates/transport6_reviewed_128/PROCEDURES.json",
        "DescentReviewChanges/ReviewBible/data/public/spell_candidates/transport6_reviewed_128/SHARED_RULES.json",
        "DescentReviewChanges/ReviewBible/data/public/spell_candidates/rank9planargates5_reviewed_200/MODEL.json",
        "DescentReviewChanges/ReviewBible/data/public/spell_candidates/rank9memorydenial6_reviewed_196/MODEL.json",
        "DescentReviewChanges/ReviewBible/data/public/spell_candidates/rank9knowledgerevelation5_reviewed_198/MODEL.json",
        "DescentReviewChanges/ReviewBible/data/public/spell_candidates/rank9summonhosts5_reviewed_202/MODEL.json",
        "DescentReviewChanges/ReviewBible/data/public/spell_candidates/rank9summonhosts5_reviewed_202/STANDALONE_PROCEDURES.md",
        "DescentReviewChanges/ReviewBible/data/public/spell_candidates/damage_control_25_reviewed_10.json",
        "DescentReviewChanges/ReviewBible/data/public/spell_candidates/persistent_damage_20_reviewed_07.json",
        *[f"docs/audit/2026-10-08/full-game/director-spell-review-129/{n}" for n in [
            "RANK9IMPACTEXILE4_PACKET_203.json","RANK9IMPACTEXILE4_DIRECTOR_DECISION_205.json",
            "RANK9IMPACTEXILE4_EXACT_ACCEPTANCE_205.json","RANK9IMPACTEXILE4_APPLICATION_205.json",
            "RANK9IMPACTEXILE4_APPLICATION_VALIDATION_205.json","RANK9IMPACTEXILE4_RETURN205_INDEPENDENT_AUDIT.json",
            "RANK9IMPACTEXILE4_RETURN205_RECEIPT.json","RANK9IMPACTEXILE4_RETURN204_INDEPENDENT_AUDIT.json",
            "RANK9IMPACTEXILE4_RETURN204_RECEIPT.json","RANK9IMPACTEXILE4_RETURN204_CARRY_FORWARD_AUDIT.json",
            "RANK9SUMMONHOSTS5_PACKET_227.json","RANK9SUMMONHOSTS5_PACKET_227_SUBMISSION.json",
            "RANK9SUMMONHOSTS5_RETURN227_INDEPENDENT_AUDIT.json","RANK9SUMMONHOSTS5_RETURN227_RECEIPT.json",
            "RANK9_PLANARGATES5_RETURN226_INDEPENDENT_AUDIT.json","RANK9_PLANARGATES5_RETURN226_RECEIPT.json"]],
        PENDING228.relative_to(ROOT).as_posix(),
    ]
    for folder in ["rank9summonhosts5_reviewed_202","rank9planargates5_reviewed_200","rank9knowledgerevelation5_reviewed_198","rank9memorydenial6_reviewed_196"]:
        extras.extend(p.relative_to(ROOT).as_posix() for p in sorted((ROOT/"DescentReviewChanges/ReviewBible/data/public/spell_candidates"/folder).rglob("*")) if p.is_file())
    paths = sorted(set([x["path"] for x in hist_bindings]) | set(extras))
    current = {p:(ROOT/p).read_bytes() for p in paths}
    source_rows = []
    for p,b in current.items(): source_rows.append({"path":p,"bytes":len(b),"sha256":sha(b),"gitBlobSHA1":hashlib.sha1(b"blob "+str(len(b)).encode()+b"\0"+b).hexdigest()})
    hist_hashes={x["path"]:(x["bytes"],x["sha256"]) for x in hist_bindings}
    changed=[p for p in hist_hashes if (len(current[p]),sha(current[p])) != hist_hashes[p]]

    record = copy.deepcopy(hist_by_id[TARGETS[0]])
    record.update({"currentIndexEntry":copy.deepcopy(entries[TARGETS[0]]),
        "completeCurrentCatalogSourceAndAccess":copy.deepcopy(spells[TARGETS[0]]),
        "status":"Pending at current 811/37/0 authority; reassess IE204-B02 only against source-qualified current evidence.",
        "closedAcceptedSpellIds":CLOSED})
    candidate=copy.deepcopy(historical)
    candidate.update({"id":"CURRENT-SOURCE-CONFERENCE-CANDIDATE-228","recordedAtUtc":now,
        "status":"PREPARED_CURRENT_AUTHORITY_811_37_EXACT_REVERSE_GRAVITY_PENDING_IDENTITY",
        "currentSourceCommit":head,"currentBranch":branch,"currentAuthority":AUTH,"countsUnchanged":index["authoredCounts"],
        "currentPendingGroup":{"group":GROUP,"spellIds":TARGETS,"count":1},"closedAcceptedSpellIds":CLOSED,
        "closedAcceptedSpellDecisionBinding":{"return":205,"acceptedIds":CLOSED,"appliedIds":CLOSED,"doNotReopen":True,
            "decision":info(R205_DECISION),"acceptance":info(R205_ACCEPTANCE),"application":info(R205_APP),
            "independentAudit":info(R205_AUDIT),"receipt":info(R205_RECEIPT)},
        "previousReturn227Binding":{"delivery":info(R227_DELIVERY),"independentAudit":info(R227_AUDIT),
            "receipt":info(R227_RECEIPT),"outsideScope":True,"heldIds":r227_receipt["heldIds"]},
        "historicalSourceBindings":copy.deepcopy(hist_bindings),"sourceBindings":source_rows,
        "sourceBindingRefresh":{"historicalSourceFiles":len(hist_bindings),"sourceFiles":len(source_rows),
            "changedSinceHistoricalCandidate":len(changed),"changedPaths":changed[:100],"allSourceBindingsRefreshedFromCurrentWorkingTree":True},
        "currentPendingIdentityAudit":info(PENDING228,PENDING228.read_bytes()),"records":[record]})
    cbytes=dump(candidate)
    notes=read(NOTES)
    assert len(notes["completeOriginalQuestionsUnchanged"])==26 and len(notes["focusedAdditionalQuestions"])==2
    assert len(notes["requiredNewCases"])==8 and len(notes["originalFutureCaseRequirementsUnchanged"])==7
    minimum=r205_decision["blockers"]["reverse-gravity-field"]["preciseRemainingWitnesses"]
    context={"id":"RANK9-IMPACT-EXILE4-CURRENT-DIRECTOR-CONTEXT-228","recordedAtUtc":now,
        "sourceCommit":head,"sourceBranch":branch,"sourceAuthority":AUTH,"targetGroup":{"group":GROUP,"pendingIds":TARGETS,"count":1},
        "currentPendingIdentityAudit":info(PENDING228,PENDING228.read_bytes()),"historicalCandidate":info(HIST_CANDIDATE,hist_raw),
        "historicalSourceArchive":info(HIST_ARCHIVE,hist_zip_raw),
        "priorAcceptedAppliedBatch205":{"acceptedIds":CLOSED,"appliedIds":CLOSED,"doNotReopen":True,"audit":info(R205_AUDIT),"receipt":info(R205_RECEIPT)},
        "priorHold":{"spellId":TARGETS[0],"blockers":BLOCKER[TARGETS[0]],"minimumMissingWitnesses":minimum,"reassessAgainstCurrentEvidence":True},
        "return227OutsideScope":{"heldIds":r227_receipt["heldIds"],"audit":info(R227_AUDIT),"receipt":info(R227_RECEIPT)},
        "preservation":{"originalQuestions":26,"focusedAddenda":2,"requiredMainCases":8,"futureCaseRequirements":7},
        "currentSourceBindings":len(source_rows),"historicalSourceBindings":len(hist_bindings),
        "canonicalChanges":False,"runtimeExecuted":False,"otherHoldsOutsideScope":p227.get("preservedHolds",[])}
    request=("GPT director — continue the ordinary spell review at authority 811 reviewed-applied / 37 pending / 0 accepted-unapplied, with 535 complete standalone procedures and 173 scoped interfaces. Review exactly reverse-gravity-field, the only pending identity in rank9-impact-exile4.\n\n"
        f"Current source snapshot: branch {branch}, HEAD {head}, plus the exact working-tree overlay bound in this packet. Use the refreshed source bindings, queue228/handoff228/pending audit, historical source conference, and Return204/205 evidence. Return205 accepted and applied exactly eternal-anvil, transmute-flesh-to-energy, and planar-collapse; do not reopen them. Return227's three Summon Hosts holds remain outside scope.\n\n"
        "Preserve all 26 original questions, two focused addenda, eight required main cases, seven future requirements, exact native placement/class access/cost/source/acquisition/prior lifecycle, and every passing/adverse branch. Reassess IE204-B02 against current source evidence instead of carrying it mechanically. Do not invent object durability, impact breakage/custody, or tether/anchor strength. Prior minimum missing witnesses: an actual 20 lb crate material/durability and 60 ft/120 ft impact/breakage/custody rule; an actual tether/anchor rated attachment strength and relevant upward-force/load rule.\n\n"
        "Return explicit accepted/applied/held status with exact blockers and minimum missing witnesses, replay the required main cases and preserved branches with reversible operations, seal a ZIP plus matching DELIVERY.json, and state the next pending group. Do not modify canonical files or run supplied programs. Apply no changes in this review. Keep runtime, implementation, human-play, balance, cosmology, domain-closure, completion and release gates closed.")
    files={"CURRENT_CONTEXT_228.json":dump(context),"CURRENT_SOURCE_CONFERENCE_CANDIDATE_228.json":cbytes,
        "HISTORICAL_SOURCE_CONFERENCE_CANDIDATE_01.json":hist_raw,"HISTORICAL_SOURCE_CONFERENCE_ARCHIVE_01.zip":hist_zip_raw,
        "HISTORICAL_NOTES/RANK9IMPACTEXILE4_NEXT_CONFERENCE_NOTES_129.json":NOTES.read_bytes(),"REQUEST_228.txt":request.encode(),
        **{"current/"+p:b for p,b in current.items()}}
    evidence={
        "evidence/RETURN204.zip":R204_ZIP,"evidence/RETURN204_DELIVERY.json":R204_DELIVERY,
        "evidence/RETURN204_INDEPENDENT_AUDIT.json":R204_AUDIT,"evidence/RETURN204_RECEIPT.json":R204_RECEIPT,
        "evidence/RETURN204_CARRY_FORWARD_AUDIT.json":R204_CARRY,
        "evidence/RETURN205.zip":R205_ZIP,"evidence/RETURN205_DELIVERY.json":R205_DELIVERY,
        "evidence/RETURN205_INDEPENDENT_AUDIT.json":R205_AUDIT,"evidence/RETURN205_RECEIPT.json":R205_RECEIPT,
        "evidence/RETURN205_DECISION.json":R205_DECISION,"evidence/RETURN205_EXACT_ACCEPTANCE.json":R205_ACCEPTANCE,
        "evidence/RETURN205_APPLICATION.json":R205_APP,"evidence/RETURN205_APPLICATION_VALIDATION.json":R205_VALIDATION,
        "evidence/RETURN227_DELIVERY.json":R227_DELIVERY,"evidence/RETURN227_INDEPENDENT_AUDIT.json":R227_AUDIT,
        "evidence/RETURN227_RECEIPT.json":R227_RECEIPT,"evidence/RETURN227_SUBMISSION.json":R227_SUBMISSION,
        "evidence/RETURN227_PACKET_RECORD.json":R227_PACKET}
    files.update({name:path.read_bytes() for name,path in evidence.items()})
    assert len(files)==len(set(files))
    OUT.mkdir(parents=True)
    CANDIDATE_FILE.write_bytes(cbytes); CONTEXT_FILE.write_bytes(files["CURRENT_CONTEXT_228.json"]); REQUEST_FILE.write_bytes(files["REQUEST_228.txt"])
    members=[]
    with zipfile.ZipFile(ARCHIVE,"w",zipfile.ZIP_DEFLATED,compresslevel=6) as z:
        for name,b in sorted(files.items()):
            z.writestr(name,b); members.append({"path":name,"bytes":len(b),"sha256":sha(b),"crc32":crc(b)})
        z.writestr("MANIFEST.json",dump({"id":"RANK9-IMPACT-EXILE4-CURRENT-SOURCE-MANIFEST-228","sourceCommit":head,
            "sourceBranch":branch,"sourceAuthority":AUTH,"group":GROUP,"pendingIds":TARGETS,"closedAcceptedIds":CLOSED,
            "memberCountExcludingSelf":len(members),"members":members}))
    with zipfile.ZipFile(ARCHIVE) as z:
        assert z.testzip() is None and len(z.namelist())==len(set(z.namelist()))==len(members)+1
        assert z.read("REQUEST_228.txt")==request.encode()
    araw=ARCHIVE.read_bytes()
    packet_binding={"path":ARCHIVE.relative_to(ROOT).as_posix(),"bytes":len(araw),"sha256":sha(araw),"crc32":crc(araw)}
    delivery={"id":"RANK9-IMPACT-EXILE4-CURRENT-SOURCE-DELIVERY-228","status":"PREPARED_UNSENT",
        "archive":packet_binding,"members":len(members)+1,"manifestBindings":len(members),"sourceCommit":head,"sourceBranch":branch,
        "sourceAuthority":AUTH,"group":GROUP,"pendingIds":TARGETS,"accepted":False,"applied":False,"closedAcceptedIds":CLOSED,
        "candidate":{"path":CANDIDATE_FILE.relative_to(ROOT).as_posix(),"bytes":len(cbytes),"sha256":sha(cbytes)},
        "context":{"path":CONTEXT_FILE.relative_to(ROOT).as_posix(),"bytes":len(files["CURRENT_CONTEXT_228.json"]),"sha256":sha(files["CURRENT_CONTEXT_228.json"])},
        "request":{"path":REQUEST_FILE.relative_to(ROOT).as_posix(),"bytes":len(request.encode()),"sha256":sha(request.encode())},
        "historicalCandidate":info(HIST_CANDIDATE,hist_raw),"historicalSourceArchive":info(HIST_ARCHIVE,hist_zip_raw),
        "sourceBindings":len(source_rows),"sourceChanges":changed,"return205HeldBlocker":"IE204-B02",
        "return227HeldOutsideScope":r227_receipt["heldIds"],"conversation":CHAT}
    dbytes=dump(delivery); DELIVERY.write_bytes(dbytes)
    delivery_binding=info(DELIVERY,dbytes)
    preparation_checks=[
        {"check":"Current main branch authority, pending index, queue and source catalog agree on 811/37/0","passed":branch=="main" and index["authoredCounts"]=={"reviewed":811,"pending":37} and live==sorted(p227["pendingIds"])},
        {"check":"Exact current review scope contains only reverse-gravity-field","passed":group["pendingIds"]==TARGETS and [x["spellId"] for x in candidate["records"]]==TARGETS},
        {"check":"Return205 acceptance/application for the other three group identities remains closed","passed":r205_receipt["acceptedIds"]==CLOSED and r205_app["acceptedIds"]==CLOSED},
        {"check":"Return227 three-identity hold is audited and outside scope","passed":r227_audit["status"]=="PASS" and r227_delivery["accepted"] is False},
        {"check":"Historical source conference hashes and 149 source archive rows verified","passed":len(hist_bindings)==149 and sha(hist_raw)==group["candidate"]["sha256"] and sha(hist_zip_raw)==group["archive"]["sha256"]},
        {"check":"All 26 questions, two addenda, eight cases and seven future requirements preserved","passed":len(notes["completeOriginalQuestionsUnchanged"])==26 and len(notes["focusedAdditionalQuestions"])==2 and len(notes["requiredNewCases"])==8 and len(notes["originalFutureCaseRequirementsUnchanged"])==7},
        {"check":"Every source binding is refreshed from current working-tree bytes","passed":len(source_rows)>=149 and all(len(current[x["path"]])==x["bytes"] and sha(current[x["path"]])==x["sha256"] for x in source_rows)},
        {"check":"Packet archive and matching manifest have unique members and valid CRC","passed":len(members)+1==delivery["members"] and packet_binding["sha256"]==sha(araw)}
    ]
    assert all(x["passed"] for x in preparation_checks), [x for x in preparation_checks if not x["passed"]]
    prep={"id":"RANK9IMPACTEXILE4-SOURCE-PREPARATION-228","recordedAtUtc":now,"status":"PASS","checks":preparation_checks,
        "sourceCommit":head,"sourceBranch":branch,"sourceAuthority":AUTH,"targetGroup":GROUP,"pendingIds":TARGETS,
        "closedAcceptedIds":CLOSED,"historicalSourceBindings":len(hist_bindings),"refreshedSourceBindings":len(source_rows),
        "changedHistoricalSources":changed,"originalQuestions":26,"focusedAddenda":2,"requiredMainCases":8,
        "futureRequirements":7,"packet":packet_binding,"deliveryManifest":delivery_binding,"canonicalChanges":False}
    PREP.write_bytes(dump(prep))
    PACKET.write_bytes(dump({"id":"RANK9IMPACTEXILE4-PACKET-228","status":"PREPARED_AND_SOURCE_CHECKED_UNSENT",
        "group":GROUP,"pendingIds":TARGETS,"closedAcceptedIds":CLOSED,"sourceAuthority":AUTH,"sourceBranch":branch,
        "sourceCommit":head,"archive":packet_binding,"deliveryManifest":delivery_binding,"sourceBindings":len(source_rows),
        "canonicalChanges":False}))
    prepared={"group":GROUP,"pendingIds":TARGETS,"pendingCount":1,"status":"CURRENT_SOURCE_PACKET_228_PREPARED_UNSENT",
        "freshPacketRequiredForCurrentAuthority":True,"packet":packet_binding,"deliveryManifest":delivery_binding}
    q=copy.deepcopy(q227); q.update({"id":"SPELL-REVIEW-QUEUE-228","recordedAtUtc":now,"supersedesQueue":info(QUEUE227),
        "nextGroup":GROUP,"next":prepared,"nextPreparedRequest":prepared,"packetStatus":"RANK9_IMPACT_EXILE4_PACKET_228_PREPARED_UNSENT_811_37"})
    for r in q["currentPendingGroups"]:
        if r["group"]=="rank9-summon-hosts5":
            r.update({"status":"HELD_RETURN227_INDEPENDENTLY_AUDITED","lastDirectorReturn":{"return":227,"acceptedIds":[],"appliedIds":[],
                "heldIds":r227_receipt["heldIds"],"independentAudit":info(R227_AUDIT),"receipt":info(R227_RECEIPT)}})
        if r["group"]==GROUP:
            r.update({"status":"CURRENT_SOURCE_PACKET_228_PREPARED_UNSENT_811_37","pendingIds":TARGETS,"pendingCount":1,
                "freshPacketRequiredForCurrentAuthority":True,"preparedPacket":packet_binding,"preparedDelivery":delivery_binding,
                "lastDirectorReturn":{"return":205,"acceptedIds":CLOSED,"appliedIds":CLOSED,"heldIds":TARGETS,"blockers":BLOCKER,
                    "independentAudit":info(R205_AUDIT)}})
    q["currentPacket"],q["currentPacketDelivery"],q["currentPreparation"]=packet_binding,delivery_binding,info(PREP)
    q["pendingIdentityAudit"]={"id":p228["id"],"path":PENDING228.relative_to(ROOT).as_posix(),"pendingCount":37,"sha256":sha(PENDING228.read_bytes())}
    q["currentReturnArchive"],q["currentReturnDelivery"],q["currentReturnAudit"],q["currentReturnReceipt"]=info(R227/"DD_Rank9_SummonHosts3_Director_Return227.zip"),info(R227_DELIVERY),info(R227_AUDIT),info(R227_RECEIPT)
    q["lastReviewedBatch"]={"return":227,"group":"rank9-summon-hosts5","acceptedIds":[],"appliedIds":[],"heldIds":r227_receipt["heldIds"],
        "blockers":{"summon-elemental-avatar":["SH202-B01"],"summon-herald-of-the-planes":["SH202-B02"],"summon-avatar-of-decay":["SH202-B03"]},
        "independentAudit":info(R227_AUDIT),"auditReceipt":info(R227_RECEIPT)}
    QUEUE228.write_bytes(dump(q))
    h=copy.deepcopy(h227); h.update({"id":"CURRENT-HANDOFF-228","recordedAtUtc":now,"status":"RETURN227_AUDITED_HELD_NEXT_IMPACTEXILE4_PACKET_228_PREPARED_UNSENT_811_37"})
    h["latestBatch"]={"return":227,"group":"rank9-summon-hosts5","ids":r227_receipt["heldIds"],"acceptedIds":[],"appliedIds":[],
        "heldIds":r227_receipt["heldIds"],"blockers":{"summon-elemental-avatar":["SH202-B01"],"summon-herald-of-the-planes":["SH202-B02"],"summon-avatar-of-decay":["SH202-B03"]},
        "independentAudit":info(R227_AUDIT),"auditReceipt":info(R227_RECEIPT)}
    h["nextStep"]={"group":GROUP,"pendingIds":TARGETS,"pendingCount":1,"status":"CURRENT_SOURCE_PACKET_228_PREPARED_UNSENT_AT_AUTHORITY_811_37_0",
        "freshPacketRequiredForCurrentAuthority":True,"candidate":group.get("candidate"),"archive":group.get("archive"),"packet":packet_binding,"deliveryManifest":delivery_binding}
    h["nextGroup"],h["nextPendingCount"]=GROUP,1
    h["pendingIdentityAudit"]={"id":p228["id"],"path":PENDING228.relative_to(ROOT).as_posix(),"pendingCount":37,"sha256":sha(PENDING228.read_bytes())}
    h["queue"]=info(QUEUE228); h["currentQueueBinding"]=h["queue"]
    h["currentPacket"],h["currentPacketDelivery"],h["currentPreparation"]=packet_binding,delivery_binding,info(PREP)
    h["currentReturnBinding"],h["currentReturnDelivery"],h["currentReturnAudit"],h["currentReturnReceipt"]=info(R227/"DD_Rank9_SummonHosts3_Director_Return227.zip"),info(R227_DELIVERY),info(R227_AUDIT),info(R227_RECEIPT)
    h["nextPreparedRequest"]=prepared
    h["resumePriority"]="Submit packet228 for exactly reverse-gravity-field to GPT, ping if stalled, audit the return, and apply only an exact accepted identity."
    HANDOFF228.write_bytes(dump(h))
    SNAPSHOT.write_text("# Current ordinary spell-review checkpoint 228\n\nReturn227 was independently audited and held exactly the three Summon Hosts5 identities. "
        "Authority remains **811 reviewed-applied / 37 pending / 0 accepted-unapplied** (535 complete standalone procedures; 173 scoped interfaces). "
        "The next fresh packet is rank9-impact-exile4, scoped to reverse-gravity-field; the Return205 acceptances remain closed.\n",encoding="utf-8",newline="\n")
    print(json.dumps({"status":"PASS","authority":AUTH,"group":GROUP,"pendingIds":TARGETS,"archive":packet_binding,
        "deliveryManifest":delivery_binding,"sourceBindings":len(source_rows),"packetMembers":len(members)+1,
        "checks":preparation_checks},ensure_ascii=False,indent=2))

if __name__=="__main__": main()
