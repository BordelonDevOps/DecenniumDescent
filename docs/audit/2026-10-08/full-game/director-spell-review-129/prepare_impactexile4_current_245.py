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
QUEUE244, HANDOFF244, PENDING244 = (AUDIT / n for n in ("CURRENT_SPELL_QUEUE_244.json", "CURRENT_HANDOFF_244.json", "CURRENT37_PENDING_IDENTITY_AUDIT_244.json"))
QUEUE245, HANDOFF245, PENDING245 = (AUDIT / n for n in ("CURRENT_SPELL_QUEUE_245.json", "CURRENT_HANDOFF_245.json", "CURRENT37_PENDING_IDENTITY_AUDIT_245.json"))
SNAPSHOT = AUDIT / "CURRENT_SPELL_REVIEW_SNAPSHOT_245.md"
OUT = AUDIT / "rank9_impactexile4_current_source_245_prepared"
ARCHIVE, DELIVERY = OUT / "DD_Rank9_ImpactExile4_CurrentSource_245.zip", OUT / "DD_Rank9_ImpactExile4_CurrentSource_245_DELIVERY.json"
CANDIDATE_FILE, CONTEXT_FILE, REQUEST_FILE = (OUT / n for n in ("CURRENT_SOURCE_CONFERENCE_CANDIDATE_245.json", "CURRENT_CONTEXT_245.json", "REQUEST_245.txt"))
PREP, PACKET = AUDIT / "RANK9IMPACTEXILE4_SOURCE_PREPARATION_245.json", AUDIT / "RANK9IMPACTEXILE4_PACKET_245.json"
START = ROOT / "START_HERE.md"
HIST_CANDIDATE = ROOT / "DescentReviewChanges/ReviewBible/data/director/spell_review/rank9_impact_exile_4_source_conference_01.json"
HIST_ARCHIVE, NOTES = FULL / "DD_Rank9_Impact_Exile_4_Source_Conference_01.zip", AUDIT / "RANK9IMPACTEXILE4_NEXT_CONFERENCE_NOTES_129.json"
R204 = AUDIT / "rank9_impactexile4_return204_received"
R205 = AUDIT / "rank9_impactexile4_return205_received"
R228 = AUDIT / "rank9_impactexile4_return228_received"
R244 = AUDIT / "rank9_summonhosts5_return244_received"
R205_ZIP, R205_DELIVERY = R205 / "DD_Rank9_ImpactExile4_Director_Return205.zip", R205 / "DD_Rank9_ImpactExile4_Director_Return205_DELIVERY.json"
R204_ZIP = R204 / "DD_Rank9_ImpactExile4_Director_Return204_UNACCEPTED.zip"
R204_DELIVERY = R204 / "DD_Rank9_ImpactExile4_Director_Return204_UNACCEPTED_DELIVERY.json"
R205_AUDIT, R205_RECEIPT = AUDIT / "RANK9IMPACTEXILE4_RETURN205_INDEPENDENT_AUDIT.json", AUDIT / "RANK9IMPACTEXILE4_RETURN205_RECEIPT.json"
R205_DECISION, R205_ACCEPTANCE = AUDIT / "RANK9IMPACTEXILE4_DIRECTOR_DECISION_205.json", AUDIT / "RANK9IMPACTEXILE4_EXACT_ACCEPTANCE_205.json"
R205_APP, R205_VALIDATION = AUDIT / "RANK9IMPACTEXILE4_APPLICATION_205.json", AUDIT / "RANK9IMPACTEXILE4_APPLICATION_VALIDATION_205.json"
R204_AUDIT, R204_RECEIPT, R204_CARRY = (AUDIT / n for n in ("RANK9IMPACTEXILE4_RETURN204_INDEPENDENT_AUDIT.json", "RANK9IMPACTEXILE4_RETURN204_RECEIPT.json", "RANK9IMPACTEXILE4_RETURN204_CARRY_FORWARD_AUDIT.json"))
R228_ZIP, R228_DELIVERY = R228 / "DD_Rank9_ImpactExile1_Director_Return228.zip", R228 / "DD_Rank9_ImpactExile1_Director_Return228_DELIVERY.json"
R228_DECISION = R228 / "extracted/DIRECTOR_DECISION.json"
R228_AUDIT, R228_RECEIPT = AUDIT / "RANK9IMPACTEXILE4_RETURN228_INDEPENDENT_AUDIT.json", AUDIT / "RANK9IMPACTEXILE4_RETURN228_RECEIPT.json"
R228_SUBMISSION, R228_PACKET = AUDIT / "RANK9IMPACTEXILE4_PACKET_228_SUBMISSION.json", AUDIT / "RANK9IMPACTEXILE4_PACKET_228.json"
R244_ZIP, R244_DELIVERY = R244 / "DD_Rank9_SummonHosts3_Director_Return244_HELD.zip", R244 / "DD_Rank9_SummonHosts3_Director_Return244_HELD_DELIVERY.json"
R244_AUDIT, R244_RECEIPT = AUDIT / "RANK9SUMMONHOSTS5_RETURN244_INDEPENDENT_AUDIT.json", AUDIT / "RANK9SUMMONHOSTS5_RETURN244_RECEIPT.json"
R244_SUBMISSION, R244_PACKET = AUDIT / "RANK9SUMMONHOSTS5_PACKET_244_SUBMISSION.json", AUDIT / "RANK9SUMMONHOSTS5_PACKET_244.json"
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
    # This script is resumable after a partial local build; these packet245 paths
    # were absent before its first run and are owned by this preparation.
    head = subprocess.check_output(["git","rev-parse","HEAD"],cwd=ROOT,text=True).strip()
    branch = subprocess.check_output(["git","branch","--show-current"],cwd=ROOT,text=True).strip()
    assert branch == "main"
    index, catalog, q244, h244, p244 = map(read, (INDEX,CATALOG,QUEUE244,HANDOFF244,PENDING244))
    group = next(x for x in q244["currentPendingGroups"] if x["group"] == GROUP)
    assert q244["currentAuthority"] == h244["currentAuthority"] == p244["authority"] == AUTH
    assert group["pendingIds"] == TARGETS and group["freshPacketRequiredForCurrentAuthority"] is True
    assert p244["pendingCount"] == 37 and set(TARGETS) <= set(p244["pendingIds"])
    assert index["authoredCounts"] == {"reviewed":811,"pending":37}
    assert index["representationCounts"]["completeReviewedStandaloneProcedures"] == 535
    live = sorted(x["id"] for x in index["entries"] if x.get("authoredStatus") == "pending-authored-procedure")
    assert live == sorted(p244["pendingIds"]) and len(live) == 37
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
    r228_audit,r228_receipt,r228_delivery,r228_decision = map(read,(R228_AUDIT,R228_RECEIPT,R228_DELIVERY,R228_DECISION))
    r244_audit,r244_receipt,r244_delivery = map(read,(R244_AUDIT,R244_RECEIPT,R244_DELIVERY))
    assert r205_audit["status"] == "PASS" and r205_receipt["acceptedIds"] == CLOSED
    assert r205_decision["blockers"]["reverse-gravity-field"]["blockerRecords"][0]["id"] == "IE204-B02"
    assert set(r205_accept.get("acceptedIds",[])) == set(CLOSED) and r205_app["acceptedIds"] == CLOSED and r205_val["status"] == "PASS"
    assert r228_audit["status"] == r228_receipt["status"] == "PASS"
    assert r228_delivery["accepted"] is False and r228_delivery["applied"] is False
    assert r228_decision["heldIds"] == ["reverse-gravity-field"]
    assert r228_decision["perIdentity"][0]["blockerIds"] == ["IE204-B02"]
    assert r244_audit["status"] == r244_receipt["status"] == "PASS" and r244_delivery["accepted"] is False and r244_delivery["applied"] is False

    now = datetime.now(timezone.utc).isoformat()
    lines = START.read_text(encoding="utf-8-sig").splitlines()
    lines[0] = ("**Current ordinary spell-review handoff [245](docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT_HANDOFF_245.json):** "
        "Return244 independently audited and held all three Summon Hosts5 targets; reverse-gravity-field remains held from Return228. Authority remains **811 reviewed-applied / 37 pending / 0 accepted-unapplied**. "
        "The fresh Impact/Exile4 packet is scoped to reverse-gravity-field; the three Return205 acceptances remain closed. "
        "See [packet record](docs/audit/2026-10-08/full-game/director-spell-review-129/RANK9IMPACTEXILE4_PACKET_245.json).")
    START.write_text("\n".join(lines)+"\n",encoding="utf-8",newline="\n")

    p245 = copy.deepcopy(p244)
    p245.update({"id":"CURRENT37-PENDING-IDENTITY-AUDIT-245","recordedAtUtc":now,
        "status":"PASSED_EXACT_CURRENT_INDEX_PENDING_SET_AFTER_RETURN244","authority":AUTH,
        "indexBinding":info(INDEX),"catalogBinding":info(CATALOG),
        "auditedReturn244":{"heldIds":r244_receipt["heldIds"],
            "blockers":{"summon-elemental-avatar":["SH202-B01"],"summon-herald-of-the-planes":["SH202-B02"],"summon-avatar-of-decay":["SH202-B03"]},
            "independentAudit":info(R244_AUDIT),"authorityUnchanged":AUTH},
        "auditedImpactReturn228":{"heldIds":["reverse-gravity-field"],"blockers":{"reverse-gravity-field":["IE204-B02"]},
            "independentAudit":info(R228_AUDIT),"receipt":info(R228_RECEIPT),"reassessAgainstCurrentEvidence":True},
        "preparedNextGroup":{"group":GROUP,"pendingIds":TARGETS,"pendingCount":1,"status":"CURRENT_SOURCE_PACKET_245_PREPARED_UNSENT"}})
    PENDING245.write_bytes(dump(p245))

    extras = [
        "START_HERE.md", INDEX.relative_to(ROOT).as_posix(), CATALOG.relative_to(ROOT).as_posix(),
        QUEUE244.relative_to(ROOT).as_posix(), HANDOFF244.relative_to(ROOT).as_posix(), PENDING244.relative_to(ROOT).as_posix(),
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
            "RANK9IMPACTEXILE4_PACKET_228.json","RANK9IMPACTEXILE4_PACKET_228_SUBMISSION.json",
            "RANK9IMPACTEXILE4_RETURN228_INDEPENDENT_AUDIT.json","RANK9IMPACTEXILE4_RETURN228_RECEIPT.json",
            "RANK9SUMMONHOSTS5_PACKET_244.json","RANK9SUMMONHOSTS5_PACKET_244_SUBMISSION.json",
            "RANK9SUMMONHOSTS5_RETURN244_INDEPENDENT_AUDIT.json","RANK9SUMMONHOSTS5_RETURN244_RECEIPT.json",
            "RANK9_AGENCYCONTROL9_RETURN238_INDEPENDENT_AUDIT.json","RANK9_AGENCYCONTROL9_RETURN238_RECEIPT.json",
            "RANK9_TIMEFATE6_RETURN239_INDEPENDENT_AUDIT.json","RANK9_TIMEFATE6_RETURN239_RECEIPT.json",
            "RANK9_CASTINGCOST5_RETURN240_INDEPENDENT_AUDIT.json","RANK9_CASTINGCOST5_RETURN240_RECEIPT.json",
            "RANK9_MEMORYDENIAL6_RETURN241_INDEPENDENT_AUDIT.json","RANK9_MEMORYDENIAL6_RETURN241_RECEIPT.json",
            "RANK9_KNOWLEDGEREVELATION5_RETURN242_INDEPENDENT_AUDIT.json","RANK9_KNOWLEDGEREVELATION5_RETURN242_RECEIPT.json",
            "RANK9_PLANARGATES5_RETURN243_INDEPENDENT_AUDIT.json","RANK9_PLANARGATES5_RETURN243_RECEIPT.json",
            "RANK9_PLANARGATES5_RETURN226_INDEPENDENT_AUDIT.json","RANK9_PLANARGATES5_RETURN226_RECEIPT.json"]],
        PENDING245.relative_to(ROOT).as_posix(),
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
    candidate.update({"id":"CURRENT-SOURCE-CONFERENCE-CANDIDATE-245","recordedAtUtc":now,
        "status":"PREPARED_CURRENT_AUTHORITY_811_37_EXACT_REVERSE_GRAVITY_PENDING_IDENTITY",
        "currentSourceCommit":head,"currentBranch":branch,"currentAuthority":AUTH,"countsUnchanged":index["authoredCounts"],
        "currentPendingGroup":{"group":GROUP,"spellIds":TARGETS,"count":1},"closedAcceptedSpellIds":CLOSED,
        "closedAcceptedSpellDecisionBinding":{"return":205,"acceptedIds":CLOSED,"appliedIds":CLOSED,"doNotReopen":True,
            "decision":info(R205_DECISION),"acceptance":info(R205_ACCEPTANCE),"application":info(R205_APP),
            "independentAudit":info(R205_AUDIT),"receipt":info(R205_RECEIPT)},
        "previousReturn244Binding":{"delivery":info(R244_DELIVERY),"independentAudit":info(R244_AUDIT),
            "receipt":info(R244_RECEIPT),"outsideScope":True,"heldIds":r244_receipt["heldIds"]},
        "previousImpactReturn228Binding":{"delivery":info(R228_DELIVERY),"independentAudit":info(R228_AUDIT),
            "receipt":info(R228_RECEIPT),"sameIdentityPriorHold":True,"heldIds":["reverse-gravity-field"],
            "blockers":{"reverse-gravity-field":["IE204-B02"]}},
        "historicalSourceBindings":copy.deepcopy(hist_bindings),"sourceBindings":source_rows,
        "sourceBindingRefresh":{"historicalSourceFiles":len(hist_bindings),"sourceFiles":len(source_rows),
            "changedSinceHistoricalCandidate":len(changed),"changedPaths":changed[:100],"allSourceBindingsRefreshedFromCurrentWorkingTree":True},
        "currentPendingIdentityAudit":info(PENDING245,PENDING245.read_bytes()),"records":[record]})
    cbytes=dump(candidate)
    notes=read(NOTES)
    assert len(notes["completeOriginalQuestionsUnchanged"])==26 and len(notes["focusedAdditionalQuestions"])==2
    assert len(notes["requiredNewCases"])==8 and len(notes["originalFutureCaseRequirementsUnchanged"])==7
    minimum=r228_decision["perIdentity"][0]["minimumMissingWitnesses"]
    context={"id":"RANK9-IMPACT-EXILE4-CURRENT-DIRECTOR-CONTEXT-245","recordedAtUtc":now,
        "sourceCommit":head,"sourceBranch":branch,"sourceAuthority":AUTH,"targetGroup":{"group":GROUP,"pendingIds":TARGETS,"count":1},
        "currentPendingIdentityAudit":info(PENDING245,PENDING245.read_bytes()),"historicalCandidate":info(HIST_CANDIDATE,hist_raw),
        "historicalSourceArchive":info(HIST_ARCHIVE,hist_zip_raw),
        "priorAcceptedAppliedBatch205":{"acceptedIds":CLOSED,"appliedIds":CLOSED,"doNotReopen":True,"audit":info(R205_AUDIT),"receipt":info(R205_RECEIPT)},
        "priorHold":{"spellId":TARGETS[0],"blockers":BLOCKER[TARGETS[0]],"minimumMissingWitnesses":minimum,"reassessAgainstCurrentEvidence":True},
        "return244OutsideScope":{"heldIds":r244_receipt["heldIds"],"audit":info(R244_AUDIT),"receipt":info(R244_RECEIPT)},
        "priorReturn228SameIdentityHold":{"heldIds":["reverse-gravity-field"],"blockers":{"reverse-gravity-field":["IE204-B02"]},
            "decision":info(R228_DECISION),"archive":info(R228_ZIP),"delivery":info(R228_DELIVERY),
            "audit":info(R228_AUDIT),"receipt":info(R228_RECEIPT)},
        "preservation":{"originalQuestions":26,"focusedAddenda":2,"requiredMainCases":8,"futureCaseRequirements":7},
        "currentSourceBindings":len(source_rows),"historicalSourceBindings":len(hist_bindings),
        "canonicalChanges":False,"runtimeExecuted":False,"otherHoldsOutsideScope":p244.get("preservedHolds",[])}
    request=("GPT director — continue the ordinary spell review at authority 811 reviewed-applied / 37 pending / 0 accepted-unapplied, with 535 complete standalone procedures and 173 scoped interfaces. Review exactly reverse-gravity-field, the only pending identity in rank9-impact-exile4.\n\n"
        f"Current source snapshot: branch {branch}, HEAD {head}, plus the exact working-tree overlay bound in this packet. Use the refreshed source bindings, queue245/handoff245/pending audit, historical source conference, and Return204/205/228 evidence. Return205 accepted and applied exactly eternal-anvil, transmute-flesh-to-energy, and planar-collapse; do not reopen them. Return228 held reverse-gravity-field under IE204-B02; reassess that blocker against this packet's current evidence instead of assuming it. Return244's three Summon Hosts holds and the separate Return238–243 holds remain outside scope; preserve them exactly.\n\n"
        "Preserve all 26 original questions, two focused addenda, eight required main cases, seven future requirements, exact native placement/class access/cost/source/acquisition/prior lifecycle, and every passing/adverse branch. Reassess IE204-B02 against current source evidence instead of carrying it mechanically. Do not invent object durability, impact breakage/custody, or tether/anchor strength. Prior minimum missing witnesses: an actual 20 lb crate material/durability and 60 ft/120 ft impact/breakage/custody rule; an actual tether/anchor rated attachment strength and relevant upward-force/load rule.\n\n"
        "Return explicit accepted/applied/held status with exact blockers and minimum missing witnesses, replay the required main cases and preserved branches with reversible operations, seal a ZIP plus matching DELIVERY.json, and state the next pending group. Do not modify canonical files or run supplied programs. Apply no changes in this review. Keep runtime, implementation, human-play, balance, cosmology, domain-closure, completion and release gates closed.")
    files={"CURRENT_CONTEXT_245.json":dump(context),"CURRENT_SOURCE_CONFERENCE_CANDIDATE_245.json":cbytes,
        "HISTORICAL_SOURCE_CONFERENCE_CANDIDATE_01.json":hist_raw,"HISTORICAL_SOURCE_CONFERENCE_ARCHIVE_01.zip":hist_zip_raw,
        "HISTORICAL_NOTES/RANK9IMPACTEXILE4_NEXT_CONFERENCE_NOTES_129.json":NOTES.read_bytes(),"REQUEST_245.txt":request.encode(),
        **{"current/"+p:b for p,b in current.items()}}
    evidence={
        "evidence/RETURN204.zip":R204_ZIP,"evidence/RETURN204_DELIVERY.json":R204_DELIVERY,
        "evidence/RETURN204_INDEPENDENT_AUDIT.json":R204_AUDIT,"evidence/RETURN204_RECEIPT.json":R204_RECEIPT,
        "evidence/RETURN204_CARRY_FORWARD_AUDIT.json":R204_CARRY,
        "evidence/RETURN205.zip":R205_ZIP,"evidence/RETURN205_DELIVERY.json":R205_DELIVERY,
        "evidence/RETURN205_INDEPENDENT_AUDIT.json":R205_AUDIT,"evidence/RETURN205_RECEIPT.json":R205_RECEIPT,
        "evidence/RETURN205_DECISION.json":R205_DECISION,"evidence/RETURN205_EXACT_ACCEPTANCE.json":R205_ACCEPTANCE,
        "evidence/RETURN205_APPLICATION.json":R205_APP,"evidence/RETURN205_APPLICATION_VALIDATION.json":R205_VALIDATION,
        "evidence/RETURN228.zip":R228_ZIP,"evidence/RETURN228_DELIVERY.json":R228_DELIVERY,
        "evidence/RETURN228_DECISION.json":R228_DECISION,"evidence/RETURN228_INDEPENDENT_AUDIT.json":R228_AUDIT,
        "evidence/RETURN228_RECEIPT.json":R228_RECEIPT,"evidence/RETURN228_SUBMISSION.json":R228_SUBMISSION,
        "evidence/RETURN228_PACKET_RECORD.json":R228_PACKET,
        "evidence/RETURN238.zip":AUDIT/"rank9_agencycontrol9_return238_received/DD_Rank9_AgencyControl2_Director_Return238.zip",
        "evidence/RETURN238_DELIVERY.json":AUDIT/"rank9_agencycontrol9_return238_received/DD_Rank9_AgencyControl2_Director_Return238_DELIVERY.json",
        "evidence/RETURN238_INDEPENDENT_AUDIT.json":AUDIT/"RANK9_AGENCYCONTROL9_RETURN238_INDEPENDENT_AUDIT.json",
        "evidence/RETURN238_RECEIPT.json":AUDIT/"RANK9_AGENCYCONTROL9_RETURN238_RECEIPT.json",
        "evidence/RETURN239.zip":AUDIT/"rank9_timefate6_return239_received/DD_Rank9_TimeFate4_Director_Return239_HELD.zip",
        "evidence/RETURN239_DELIVERY.json":AUDIT/"rank9_timefate6_return239_received/DD_Rank9_TimeFate4_Director_Return239_HELD_DELIVERY.json",
        "evidence/RETURN239_INDEPENDENT_AUDIT.json":AUDIT/"RANK9_TIMEFATE6_RETURN239_INDEPENDENT_AUDIT.json",
        "evidence/RETURN239_RECEIPT.json":AUDIT/"RANK9_TIMEFATE6_RETURN239_RECEIPT.json",
        "evidence/RETURN240.zip":AUDIT/"rank9_castingcost5_return240_received/DD_Rank9_UnholyAscendance_Director_Return240_HELD.zip",
        "evidence/RETURN240_DELIVERY.json":AUDIT/"rank9_castingcost5_return240_received/DD_Rank9_UnholyAscendance_Director_Return240_HELD_DELIVERY.json",
        "evidence/RETURN240_INDEPENDENT_AUDIT.json":AUDIT/"RANK9_CASTINGCOST5_RETURN240_INDEPENDENT_AUDIT.json",
        "evidence/RETURN240_RECEIPT.json":AUDIT/"RANK9_CASTINGCOST5_RETURN240_RECEIPT.json",
        "evidence/RETURN241.zip":AUDIT/"rank9_memorydenial6_return241_received/DD_Rank9_MemoryDenial2_Director_Return241_HELD.zip",
        "evidence/RETURN241_DELIVERY.json":AUDIT/"rank9_memorydenial6_return241_received/DD_Rank9_MemoryDenial2_Director_Return241_HELD_DELIVERY.json",
        "evidence/RETURN241_INDEPENDENT_AUDIT.json":AUDIT/"RANK9_MEMORYDENIAL6_RETURN241_INDEPENDENT_AUDIT.json",
        "evidence/RETURN241_RECEIPT.json":AUDIT/"RANK9_MEMORYDENIAL6_RETURN241_RECEIPT.json",
        "evidence/RETURN242.zip":AUDIT/"rank9_knowledgerevelation5_return242_received/DD_Rank9_FactionOmniscienceSupreme_Director_Return242_HELD.zip",
        "evidence/RETURN242_DELIVERY.json":AUDIT/"rank9_knowledgerevelation5_return242_received/DD_Rank9_FactionOmniscienceSupreme_Director_Return242_HELD_DELIVERY.json",
        "evidence/RETURN242_INDEPENDENT_AUDIT.json":AUDIT/"RANK9_KNOWLEDGEREVELATION5_RETURN242_INDEPENDENT_AUDIT.json",
        "evidence/RETURN242_RECEIPT.json":AUDIT/"RANK9_KNOWLEDGEREVELATION5_RETURN242_RECEIPT.json",
        "evidence/RETURN243.zip":AUDIT/"rank9_planargates5_return243_received/DD_Rank9_PlanarGates2_Director_Return243_HELD.zip",
        "evidence/RETURN243_DELIVERY.json":AUDIT/"rank9_planargates5_return243_received/DD_Rank9_PlanarGates2_Director_Return243_HELD_DELIVERY.json",
        "evidence/RETURN243_INDEPENDENT_AUDIT.json":AUDIT/"RANK9_PLANARGATES5_RETURN243_INDEPENDENT_AUDIT.json",
        "evidence/RETURN243_RECEIPT.json":AUDIT/"RANK9_PLANARGATES5_RETURN243_RECEIPT.json",
        "evidence/RETURN244.zip":R244_ZIP,
        "evidence/RETURN244_DELIVERY.json":R244_DELIVERY,"evidence/RETURN244_INDEPENDENT_AUDIT.json":R244_AUDIT,
        "evidence/RETURN244_RECEIPT.json":R244_RECEIPT,"evidence/RETURN244_SUBMISSION.json":R244_SUBMISSION,
        "evidence/RETURN244_PACKET_RECORD.json":R244_PACKET}
    files.update({name:path.read_bytes() for name,path in evidence.items()})
    assert len(files)==len(set(files))
    OUT.mkdir(parents=True, exist_ok=True)
    CANDIDATE_FILE.write_bytes(cbytes); CONTEXT_FILE.write_bytes(files["CURRENT_CONTEXT_245.json"]); REQUEST_FILE.write_bytes(files["REQUEST_245.txt"])
    members=[]
    with zipfile.ZipFile(ARCHIVE,"w",zipfile.ZIP_DEFLATED,compresslevel=6) as z:
        for name,b in sorted(files.items()):
            z.writestr(name,b); members.append({"path":name,"bytes":len(b),"sha256":sha(b),"crc32":crc(b)})
        z.writestr("MANIFEST.json",dump({"id":"RANK9-IMPACT-EXILE4-CURRENT-SOURCE-MANIFEST-245","sourceCommit":head,
            "sourceBranch":branch,"sourceAuthority":AUTH,"group":GROUP,"pendingIds":TARGETS,"closedAcceptedIds":CLOSED,
            "memberCountExcludingSelf":len(members),"members":members}))
    with zipfile.ZipFile(ARCHIVE) as z:
        assert z.testzip() is None and len(z.namelist())==len(set(z.namelist()))==len(members)+1
        assert z.read("REQUEST_245.txt")==request.encode()
    araw=ARCHIVE.read_bytes()
    packet_binding={"path":ARCHIVE.relative_to(ROOT).as_posix(),"bytes":len(araw),"sha256":sha(araw),"crc32":crc(araw)}
    delivery={"id":"RANK9-IMPACT-EXILE4-CURRENT-SOURCE-DELIVERY-245","status":"PREPARED_UNSENT",
        "archive":packet_binding,"members":len(members)+1,"manifestBindings":len(members),"sourceCommit":head,"sourceBranch":branch,
        "sourceAuthority":AUTH,"group":GROUP,"pendingIds":TARGETS,"accepted":False,"applied":False,"closedAcceptedIds":CLOSED,
        "candidate":{"path":CANDIDATE_FILE.relative_to(ROOT).as_posix(),"bytes":len(cbytes),"sha256":sha(cbytes)},
        "context":{"path":CONTEXT_FILE.relative_to(ROOT).as_posix(),"bytes":len(files["CURRENT_CONTEXT_245.json"]),"sha256":sha(files["CURRENT_CONTEXT_245.json"])},
        "request":{"path":REQUEST_FILE.relative_to(ROOT).as_posix(),"bytes":len(request.encode()),"sha256":sha(request.encode())},
        "historicalCandidate":info(HIST_CANDIDATE,hist_raw),"historicalSourceArchive":info(HIST_ARCHIVE,hist_zip_raw),
        "sourceBindings":len(source_rows),"sourceChanges":changed,"return205HeldBlocker":"IE204-B02",
        "return244HeldOutsideScope":r244_receipt["heldIds"],"conversation":CHAT}
    dbytes=dump(delivery); DELIVERY.write_bytes(dbytes)
    delivery_binding=info(DELIVERY,dbytes)
    preparation_checks=[
        {"check":"Current main branch authority, pending index, queue and source catalog agree on 811/37/0","passed":branch=="main" and index["authoredCounts"]=={"reviewed":811,"pending":37} and live==sorted(p244["pendingIds"])},
        {"check":"Exact current review scope contains only reverse-gravity-field","passed":group["pendingIds"]==TARGETS and [x["spellId"] for x in candidate["records"]]==TARGETS},
        {"check":"Return205 acceptance/application for the other three group identities remains closed","passed":r205_receipt["acceptedIds"]==CLOSED and r205_app["acceptedIds"]==CLOSED},
        {"check":"Return244 three-identity hold is audited and outside scope","passed":r244_audit["status"]=="PASS" and r244_delivery["accepted"] is False},
        {"check":"Return228 same-identity hold is independently audited and remains open for reassessment","passed":r228_audit["status"]=="PASS" and r228_decision["perIdentity"][0]["blockerIds"]==BLOCKER[TARGETS[0]]},
        {"check":"Historical source conference hashes and 149 source archive rows verified","passed":len(hist_bindings)==149 and sha(hist_raw)==group["candidate"]["sha256"] and sha(hist_zip_raw)==group["archive"]["sha256"]},
        {"check":"All 26 questions, two addenda, eight cases and seven future requirements preserved","passed":len(notes["completeOriginalQuestionsUnchanged"])==26 and len(notes["focusedAdditionalQuestions"])==2 and len(notes["requiredNewCases"])==8 and len(notes["originalFutureCaseRequirementsUnchanged"])==7},
        {"check":"Every source binding is refreshed from current working-tree bytes","passed":len(source_rows)>=149 and all(len(current[x["path"]])==x["bytes"] and sha(current[x["path"]])==x["sha256"] for x in source_rows)},
        {"check":"Packet archive and matching manifest have unique members and valid CRC","passed":len(members)+1==delivery["members"] and packet_binding["sha256"]==sha(araw)}
    ]
    assert all(x["passed"] for x in preparation_checks), [x for x in preparation_checks if not x["passed"]]
    prep={"id":"RANK9IMPACTEXILE4-SOURCE-PREPARATION-245","recordedAtUtc":now,"status":"PASS","checks":preparation_checks,
        "sourceCommit":head,"sourceBranch":branch,"sourceAuthority":AUTH,"targetGroup":GROUP,"pendingIds":TARGETS,
        "closedAcceptedIds":CLOSED,"historicalSourceBindings":len(hist_bindings),"refreshedSourceBindings":len(source_rows),
        "changedHistoricalSources":changed,"originalQuestions":26,"focusedAddenda":2,"requiredMainCases":8,
        "futureRequirements":7,"packet":packet_binding,"deliveryManifest":delivery_binding,"canonicalChanges":False}
    PREP.write_bytes(dump(prep))
    PACKET.write_bytes(dump({"id":"RANK9IMPACTEXILE4-PACKET-245","status":"PREPARED_AND_SOURCE_CHECKED_UNSENT",
        "group":GROUP,"pendingIds":TARGETS,"closedAcceptedIds":CLOSED,"sourceAuthority":AUTH,"sourceBranch":branch,
        "sourceCommit":head,"archive":packet_binding,"deliveryManifest":delivery_binding,"sourceBindings":len(source_rows),
        "canonicalChanges":False}))
    prepared={"group":GROUP,"pendingIds":TARGETS,"pendingCount":1,"status":"CURRENT_SOURCE_PACKET_245_PREPARED_UNSENT",
        "freshPacketRequiredForCurrentAuthority":True,"packet":packet_binding,"deliveryManifest":delivery_binding}
    q=copy.deepcopy(q244); q.update({"id":"SPELL-REVIEW-QUEUE-245","recordedAtUtc":now,"supersedesQueue":info(QUEUE244),
        "nextGroup":GROUP,"next":prepared,"nextPreparedRequest":prepared,"packetStatus":"RANK9_IMPACT_EXILE4_PACKET_245_PREPARED_UNSENT_811_37"})
    for r in q["currentPendingGroups"]:
        if r["group"]=="rank9-summon-hosts5":
            r.update({"status":"HELD_RETURN244_INDEPENDENTLY_AUDITED","lastDirectorReturn":{"return":244,"acceptedIds":[],"appliedIds":[],
                "heldIds":r244_receipt["heldIds"],"independentAudit":info(R244_AUDIT),"receipt":info(R244_RECEIPT)}})
        if r["group"]==GROUP:
            r.update({"status":"CURRENT_SOURCE_PACKET_245_PREPARED_UNSENT_811_37","pendingIds":TARGETS,"pendingCount":1,
                "freshPacketRequiredForCurrentAuthority":True,"preparedPacket":packet_binding,"preparedDelivery":delivery_binding,
                "lastDirectorReturn":{"return":228,"acceptedIds":[],"appliedIds":[],"heldIds":TARGETS,"blockers":BLOCKER,
                    "independentAudit":info(R228_AUDIT),"receipt":info(R228_RECEIPT)},
                "priorAcceptedAppliedBatch":{"return":205,"acceptedIds":CLOSED,"appliedIds":CLOSED,"doNotReopen":True,
                    "independentAudit":info(R205_AUDIT)}})
    q["currentPacket"],q["currentPacketDelivery"],q["currentPreparation"]=packet_binding,delivery_binding,info(PREP)
    q["pendingIdentityAudit"]={"id":p245["id"],"path":PENDING245.relative_to(ROOT).as_posix(),"pendingCount":37,"sha256":sha(PENDING245.read_bytes())}
    q["currentReturnArchive"],q["currentReturnDelivery"],q["currentReturnAudit"],q["currentReturnReceipt"]=info(R244_ZIP),info(R244_DELIVERY),info(R244_AUDIT),info(R244_RECEIPT)
    q["lastReviewedBatch"]={"return":244,"group":"rank9-summon-hosts5","acceptedIds":[],"appliedIds":[],"heldIds":r244_receipt["heldIds"],
        "blockers":{"summon-elemental-avatar":["SH202-B01"],"summon-herald-of-the-planes":["SH202-B02"],"summon-avatar-of-decay":["SH202-B03"]},
        "independentAudit":info(R244_AUDIT),"auditReceipt":info(R244_RECEIPT)}
    QUEUE245.write_bytes(dump(q))
    h=copy.deepcopy(h244); h.update({"id":"CURRENT-HANDOFF-245","recordedAtUtc":now,"status":"RETURN244_AUDITED_HELD_NEXT_IMPACTEXILE4_PACKET_245_PREPARED_UNSENT_811_37"})
    h["latestBatch"]={"return":244,"group":"rank9-summon-hosts5","ids":r244_receipt["heldIds"],"acceptedIds":[],"appliedIds":[],
        "heldIds":r244_receipt["heldIds"],"blockers":{"summon-elemental-avatar":["SH202-B01"],"summon-herald-of-the-planes":["SH202-B02"],"summon-avatar-of-decay":["SH202-B03"]},
        "independentAudit":info(R244_AUDIT),"auditReceipt":info(R244_RECEIPT)}
    h["nextStep"]={"group":GROUP,"pendingIds":TARGETS,"pendingCount":1,"status":"CURRENT_SOURCE_PACKET_245_PREPARED_UNSENT_AT_AUTHORITY_811_37_0",
        "freshPacketRequiredForCurrentAuthority":True,"candidate":group.get("candidate"),"archive":group.get("archive"),"packet":packet_binding,"deliveryManifest":delivery_binding}
    h["nextGroup"],h["nextPendingCount"]=GROUP,1
    h["pendingIdentityAudit"]={"id":p245["id"],"path":PENDING245.relative_to(ROOT).as_posix(),"pendingCount":37,"sha256":sha(PENDING245.read_bytes())}
    h["queue"]=info(QUEUE245); h["currentQueueBinding"]=h["queue"]
    h["currentPacket"],h["currentPacketDelivery"],h["currentPreparation"]=packet_binding,delivery_binding,info(PREP)
    h["currentReturnBinding"],h["currentReturnDelivery"],h["currentReturnAudit"],h["currentReturnReceipt"]=info(R244_ZIP),info(R244_DELIVERY),info(R244_AUDIT),info(R244_RECEIPT)
    h["nextPreparedRequest"]=prepared
    h["resumePriority"]="Submit packet245 for exactly reverse-gravity-field to GPT, ping if stalled, audit the return, and apply only an exact accepted identity."
    HANDOFF245.write_bytes(dump(h))
    SNAPSHOT.write_text("# Current ordinary spell-review checkpoint 245\n\nReturn244 was independently audited and held exactly the three Summon Hosts5 identities. "
        "Authority remains **811 reviewed-applied / 37 pending / 0 accepted-unapplied** (535 complete standalone procedures; 173 scoped interfaces). "
        "The next fresh packet is rank9-impact-exile4, scoped to reverse-gravity-field; the Return205 acceptances remain closed.\n",encoding="utf-8",newline="\n")
    print(json.dumps({"status":"PASS","authority":AUTH,"group":GROUP,"pendingIds":TARGETS,"archive":packet_binding,
        "deliveryManifest":delivery_binding,"sourceBindings":len(source_rows),"packetMembers":len(members)+1,
        "checks":preparation_checks},ensure_ascii=False,indent=2))

if __name__=="__main__": main()

