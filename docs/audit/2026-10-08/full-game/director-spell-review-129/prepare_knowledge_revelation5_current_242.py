from __future__ import annotations

import copy
import hashlib
import json
import subprocess
import zipfile
import zlib
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath


ROOT = Path(__file__).resolve().parents[5]
AUDIT = ROOT / "docs/audit/2026-10-08/full-game/director-spell-review-129"
FULL = ROOT / "docs/audit/2026-10-08/full-game"
GROUP = "rank9-knowledge-revelation5"
SPELL = "faction-omniscience-supreme"
IDS = [SPELL]
AUTHORITY = {"reviewedApplied": 811, "pending": 37, "acceptedUnapplied": 0,
             "completeStandaloneProcedures": 535, "scopedInterfaces": 173}
INDEX = "DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json"
CATALOG = "DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json"
QUEUE_IN = "docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT_SPELL_QUEUE_241.json"
PENDING_IN = "docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT37_PENDING_IDENTITY_AUDIT_241.json"
HANDOFF_IN = "docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT_HANDOFF_241.json"
HISTORICAL_CANDIDATE = "DescentReviewChanges/ReviewBible/data/director/spell_review/rank9_knowledge_revelation_5_source_conference_01.json"
HISTORICAL_ARCHIVE = "docs/audit/2026-10-08/full-game/DD_Rank9_Knowledge_Revelation_5_Source_Conference_01.zip"
NOTES = "docs/audit/2026-10-08/full-game/director-spell-review-129/RANK9KNOWLEDGEREVELATION5_NEXT_CONFERENCE_NOTES_129.json"
PRIOR_CURRENT_CANDIDATE = AUDIT / "rank9_knowledgerevelation5_current_source_197_prepared/CURRENT_SOURCE_CONFERENCE_CANDIDATE_197.json"
PRIOR_RETURN_DIR = AUDIT / "rank9_knowledgerevelation5_return198_received"
PRIOR_RETURN_ZIP = PRIOR_RETURN_DIR / "DD_Rank9_KnowledgeRevelation5_Director_Return198.zip"
PRIOR_RETURN_DELIVERY = PRIOR_RETURN_DIR / "DD_Rank9_KnowledgeRevelation5_Director_Return198_DELIVERY.json"
PRIOR_DECISION = AUDIT / "RANK9_KNOWLEDGEREVELATION5_DIRECTOR_DECISION_198.json"
PRIOR_AUDIT = AUDIT / "RANK9_KNOWLEDGEREVELATION5_RETURN198_INDEPENDENT_AUDIT.json"
PRIOR_RECEIPT = AUDIT / "RANK9_KNOWLEDGEREVELATION5_RETURN198_RECEIPT.json"
RETURN241_AUDIT = AUDIT / "RANK9_MEMORYDENIAL6_RETURN241_INDEPENDENT_AUDIT.json"
RETURN241_RECEIPT = AUDIT / "RANK9_MEMORYDENIAL6_RETURN241_RECEIPT.json"
RETURN241_DELIVERY = AUDIT / "rank9_memorydenial6_return241_received/DD_Rank9_MemoryDenial2_Director_Return241_HELD_DELIVERY.json"
RETURN241_ZIP = AUDIT / "rank9_memorydenial6_return241_received/DD_Rank9_MemoryDenial2_Director_Return241_HELD.zip"
RETURN240_DOCS = [
    "RANK9_CASTINGCOST5_RETURN240_INDEPENDENT_AUDIT.json", "RANK9_CASTINGCOST5_RETURN240_RECEIPT.json",
    "rank9_castingcost5_return240_received/DD_Rank9_UnholyAscendance_Director_Return240_HELD_DELIVERY.json",
    "rank9_castingcost5_return240_received/DD_Rank9_UnholyAscendance_Director_Return240_HELD.zip"]
RETURN239_DOCS = [
    "RANK9_TIMEFATE6_RETURN239_INDEPENDENT_AUDIT.json", "RANK9_TIMEFATE6_RETURN239_RECEIPT.json",
    "rank9_timefate6_return239_received/DD_Rank9_TimeFate4_Director_Return239_HELD_DELIVERY.json",
    "rank9_timefate6_return239_received/DD_Rank9_TimeFate4_Director_Return239_HELD.zip"]
RETURN238_DOCS = [
    "RANK9_AGENCYCONTROL9_RETURN238_INDEPENDENT_AUDIT.json", "RANK9_AGENCYCONTROL9_RETURN238_RECEIPT.json",
    "rank9_agencycontrol9_return238_received/DD_Rank9_AgencyControl2_Director_Return238_DELIVERY.json",
    "rank9_agencycontrol9_return238_received/DD_Rank9_AgencyControl2_Director_Return238.zip"]
SUP_DIR = AUDIT / "rank9_knowledgerevelation5_return198_witness_supplement_242"
SUP_ZIP_NAME = "DD_Rank9_KnowledgeRevelation5_Return198_TargetWitness_242.zip"
SUP_DELIVERY_NAME = "DD_Rank9_KnowledgeRevelation5_Return198_TargetWitness_242_DELIVERY.json"
OUT = AUDIT / "rank9_knowledgerevelation5_current_source_242_prepared"
PACKET_ZIP_NAME = "DD_Rank9_KnowledgeRevelation5_CurrentSource_242.zip"
PACKET_DELIVERY_NAME = "DD_Rank9_KnowledgeRevelation5_CurrentSource_242_DELIVERY.json"
PACKET_RECORD = AUDIT / "RANK9KNOWLEDGEREVELATION5_PACKET_242.json"
PREPARATION = AUDIT / "RANK9KNOWLEDGEREVELATION5_SOURCE_PREPARATION_242.json"
PENDING_OUT = AUDIT / "CURRENT37_PENDING_IDENTITY_AUDIT_242.json"
QUEUE_OUT = AUDIT / "CURRENT_SPELL_QUEUE_242.json"
HANDOFF_OUT = AUDIT / "CURRENT_HANDOFF_242.json"
SNAPSHOT_OUT = AUDIT / "CURRENT_SPELL_REVIEW_SNAPSHOT_242.md"
CHAT = "https://chatgpt.com/g/g-p-67f17555a8dc8191a2b5b81e6d8adc12-dungeon-crawler/c/6adc506d-8770-83ea-b64c-0345d9b9b682"


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def json_bytes(value) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8")


def read(raw: bytes):
    return json.loads(raw.decode("utf-8-sig"))


def binding(path: str, raw: bytes) -> dict:
    return {"path": path, "bytes": len(raw), "sha256": sha(raw), "crc32": f"{zlib.crc32(raw) & 0xffffffff:08x}"}


def workspace_bytes(path: str) -> bytes:
    local = ROOT / Path(path)
    if local.is_file():
        return local.read_bytes()
    return subprocess.check_output(["git", "cat-file", "blob", f"HEAD:{path}"], cwd=ROOT)


def git_blob_id(raw: bytes) -> str:
    return subprocess.check_output(["git", "hash-object", "--stdin"], cwd=ROOT, input=raw).decode().strip()


def safe_member(name: str) -> bool:
    p = PurePosixPath(name)
    return bool(name) and "\\" not in name and not p.is_absolute() and all(x not in ("", ".", "..") and not x.startswith(".") for x in p.parts)


def state_sha(value: object) -> str:
    return sha(json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False).encode("utf-8"))


def zip_member_binding(zf: zipfile.ZipFile, name: str) -> dict:
    h = hashlib.sha256()
    crc = 0
    size = 0
    with zf.open(name) as f:
        for part in iter(lambda: f.read(1024 * 1024), b""):
            size += len(part)
            h.update(part)
            crc = zlib.crc32(part, crc)
    return {"bytes": size, "sha256": h.hexdigest(), "crc32": f"{crc & 0xffffffff:08x}"}


def replay_case(case: dict) -> tuple[bool, int, int, int]:
    if state_sha(case["initialState"]) != case["initialSHA256"] or state_sha(case["finalState"]) != case["finalSHA256"]:
        return False, 0, 0, 0
    state = case["initialState"]
    prev_time = float("-inf")
    fcount = icount = 0
    for event in case["events"]:
        before, after = event["beforeState"], event["afterState"]
        fops, iops = event["forward"], event["inverse"]
        fcount += len(fops)
        icount += len(iops)
        if (before != state or state_sha(before) != event["beforeSHA256"]
                or state_sha(after) != event["afterSHA256"] or len(fops) != 2 or len(iops) != 2):
            return False, fcount, icount, len(case["events"])
        t = after.get("time")
        if isinstance(t, (int, float)):
            if t < prev_time:
                return False, fcount, icount, len(case["events"])
            prev_time = t
        if not (fops[0] == {"op": "test", "path": "", "value": before}
                and fops[1] == {"op": "replace", "path": "", "value": after}
                and iops[0] == {"op": "test", "path": "", "value": after}
                and iops[1] == {"op": "replace", "path": "", "value": before}):
            return False, fcount, icount, len(case["events"])
        state = after
    return state == case["finalState"], fcount, icount, len(case["events"])


def relevant(row: dict, spell: str = SPELL) -> bool:
    if not isinstance(row, dict):
        return spell in str(row) or "faction" in str(row).lower()
    if spell in row.get("spellIds", []):
        return True
    return spell in row.get("id", "") or spell in row.get("spellId", "")


def main() -> None:
    assert not OUT.exists() and not SUP_DIR.exists()
    commit = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    branch = subprocess.check_output(["git", "branch", "--show-current"], cwd=ROOT, text=True).strip()
    assert branch == "main", branch

    index_raw, catalog_raw, queue_raw, pending_raw, handoff_raw = [workspace_bytes(p) for p in (INDEX, CATALOG, QUEUE_IN, PENDING_IN, HANDOFF_IN)]
    index, catalog, queue, pending, handoff = map(read, (index_raw, catalog_raw, queue_raw, pending_raw, handoff_raw))
    audit241, receipt241 = read(RETURN241_AUDIT.read_bytes()), read(RETURN241_RECEIPT.read_bytes())
    decision241 = read(zipfile.ZipFile(RETURN241_ZIP).read("DIRECTOR_DECISION.json"))
    assert audit241["status"] == receipt241["status"] == "PASS"
    assert receipt241["acceptedIds"] == receipt241["appliedIds"] == []
    assert receipt241["heldIds"] == ["mind-collapse", "unravel-identity"]
    assert queue["currentAuthority"] == handoff["currentAuthority"] == AUTHORITY
    assert index["authoredCounts"] == {"reviewed": 811, "pending": 37}
    assert index["representationCounts"]["completeReviewedStandaloneProcedures"] == 535
    assert pending["pendingCount"] == queue["pendingCount"] == 37
    target_group = next(x for x in queue["currentPendingGroups"] if x["group"] == GROUP)
    assert target_group["pendingIds"] == IDS and target_group["pendingCount"] == 1
    assert decision241["nextPendingGroup"]["group"] == GROUP
    assert decision241["nextPendingGroup"]["pendingIds"] == IDS
    pending_ids = set(pending["pendingIds"])
    assert SPELL in pending_ids

    hist_candidate_raw = workspace_bytes(HISTORICAL_CANDIDATE)
    hist_candidate = read(hist_candidate_raw)
    notes_raw = workspace_bytes(NOTES)
    notes = read(notes_raw)
    hist_archive_raw = workspace_bytes(HISTORICAL_ARCHIVE)
    old_current = read(PRIOR_CURRENT_CANDIDATE.read_bytes())
    old_record = next(x for x in old_current["records"] if x["spellId"] == SPELL)
    hist_bindings = hist_candidate["sourceBindings"]
    assert len(hist_bindings) == 126
    original_candidate_record = next(x for x in hist_candidate["records"] if x["spellId"] == SPELL)
    assert len(notes["allQuestions"]) == 28 and len(notes["requiredNewCases"]) == 10

    # Independently build a compact, exact-member witness supplement from Return198.
    prior_delivery = read(PRIOR_RETURN_DELIVERY.read_bytes())
    with zipfile.ZipFile(PRIOR_RETURN_ZIP) as prior:
        assert prior.testzip() is None
        casebook = read(prior.read("CASEBOOK.json"))
        target_cases = [x for x in casebook["cases"] if x.get("spellId") == SPELL]
        assert len(target_cases) == 8
        case_member_paths = sorted({next(x["path"] for x in prior_delivery["allOuterMembersIncludingManifest"]
                                         if x["path"].startswith("cases/") and x["path"].endswith(".json")
                                         and Path(x["path"]).stem.replace("__", "/") == c["id"])
                                   for c in target_cases})
        # Prefer casebook's exact identity-to-file mapping through the member basename.
        prefix = "RANK9KNOWLEDGEREVELATION5129-FACTION-OMNISCIENCE-SUPREME"
        case_member_paths = sorted(n for n in prior.namelist() if n.startswith("cases/" + prefix) and n.endswith(".json"))
        assert len(case_member_paths) == len(target_cases) == 8
        procedure_path = f"procedures/{SPELL}.json"
        blocker = next(x for x in read(prior.read("DIRECTOR_DECISION.json"))["blockers"] if x["id"] == "KR198-B01")
        old_decision = read(prior.read("DIRECTOR_DECISION.json"))
        old_holds = read(prior.read("HOLD_REGISTER.json"))
        source_obligations = read(prior.read("SOURCE_OBLIGATIONS.json"))
        question_dispositions = read(prior.read("QUESTION_DISPOSITIONS.json"))
        future_dispositions = read(prior.read("FUTURE_OBLIGATION_DISPOSITIONS.json"))
        case_dispositions = read(prior.read("CASE_DISPOSITIONS.json"))
        clock_results = read(prior.read("CLOCK_AND_INVERSE_RESULTS.json"))
        proposal_ops = read(prior.read("PROPOSAL_OPERATIONS.json"))
        fact_sources = read(prior.read("FACT_SOURCE_REGISTER.json"))
        qualifications = read(prior.read("QUALIFICATIONS.json"))
        validation = read(prior.read("VALIDATION.json"))
        model = read(prior.read("MODEL.json"))

        target_question_ids = set(blocker["questionIds"])
        target_hold_ids = {x["id"] for x in old_holds["newHolds"] if SPELL in x.get("spellIds", [])}
        selected_cases = []
        copied_sources: dict[str, bytes] = {}
        origin_rows = []

        def copy_original_member(source_name: str, destination: str | None = None) -> None:
            dest = destination or source_name
            raw = prior.read(source_name)
            actual = {"bytes": len(raw), "sha256": sha(raw), "crc32": f"{zlib.crc32(raw) & 0xffffffff:08x}"}
            outer = next(x for x in prior_delivery["allOuterMembersIncludingManifest"] if x["path"] == source_name)
            assert all(actual[k] == outer[k] for k in ("bytes", "sha256", "crc32")), source_name
            copied_sources[dest] = raw
            origin_rows.append({"destination": dest, "sourceArchiveMember": source_name, **actual})

        copy_original_member(procedure_path)
        for path in case_member_paths:
            copy_original_member(path)
            target_obj = next(x for x in target_cases if x["id"] == json.loads(prior.read(path))["id"])
            case_obj = read(prior.read(path))
            assert case_obj == target_obj
            passed, fops, iops, events = replay_case(case_obj)
            assert passed and fops == iops == 2 * events
            selected_cases.append({k: case_obj.get(k) for k in ("id", "spellId", "mainCaseId", "kind", "status", "holdIds",
                                                                      "questionIds", "futureObligationIds", "initialSHA256", "finalSHA256")}
                                  | {"events": events, "forwardOperations": fops, "inverseOperations": iops,
                                     "freshReplayPassed": passed, "sourceMember": path})

        filtered_obligations = {}
        for key, rows in source_obligations.items():
            if isinstance(rows, list):
                filtered_obligations[key] = [x for x in rows if relevant(x)]
            elif key in ("scope", "precedence"):
                filtered_obligations[key] = rows
        # Preserve the full accepted-interface list as shared mechanical context; do not reopen the four accepted spells.
        for key in ("acceptedInterfaces", "appliedCounterparts"):
            if key in source_obligations:
                filtered_obligations[key] = source_obligations[key]
        assert {x["id"] for x in filtered_obligations["allQuestions"]} >= target_question_ids
        target_questions = [x for x in question_dispositions if SPELL in x.get("spellIds", [])]
        target_futures = [x for x in future_dispositions if SPELL in x.get("originalObligationUnchanged", {}).get("spellIds", [])]
        target_case_dispositions = [x for x in case_dispositions if x.get("originalObligationUnchanged", {}).get("spellId") == SPELL]
        target_clock_rows = [x for x in clock_results["caseResults"] if prefix in x["caseId"]]
        target_ops = [x for x in proposal_ops if x.get("id") == SPELL]
        target_model_spell = next(x for x in model["spells"] if x["id"] == SPELL)
        target_hold_rows = [x for x in old_holds["holdRecords"]
                            if x.get("id") in target_hold_ids or SPELL in x.get("originalRecordUnchanged", {}).get("spellIds", [])]
        target_new_holds = [x for x in old_holds["newHolds"] if x.get("id") in target_hold_ids]
        assert len(target_questions) >= 1 and len(target_futures) >= 1 and len(target_case_dispositions) == 2
        assert len(target_clock_rows) == 8 and len(target_ops) == 1
        assert blocker["status"] == "OPEN" and blocker["blocking"] is True

        target_context = {
            "id": "KR198-TARGET-PRIOR-DECISION-CONTEXT-242",
            "sourceDecisionId": old_decision["id"],
            "authorityBaselineUnchanged": old_decision["authorityBaselineUnchanged"],
            "priorAcceptedIds": old_decision["acceptedIds"],
            "priorUnacceptedIds": old_decision["unacceptedIds"],
            "canonicalFilesChangedAtPriorReview": old_decision["canonicalFilesChanged"],
            "targetDecision": next(x for x in old_decision["perIdentity"] if x["id"] == SPELL),
            "targetBlocker": blocker,
            "targetHoldIds": sorted(target_hold_ids),
            "scopeWarning": "The four KR198 accepted identities were applied in 198 and are outside this return. This supplement preserves the single unresolved identity only.",
        }
        target_hold_register = {"newHolds": target_new_holds, "targetHoldRecords": target_hold_rows,
                               "targetHoldIds": sorted(target_hold_ids), "recordCount": len(target_hold_rows)}
        target_model = {"id": "KR198-TARGET-MODEL-CONTEXT-242", "scope": [SPELL],
                        "authorityBaselineUnchanged": model["authorityBaselineUnchanged"],
                        "priorAcceptedIds": model["acceptedIds"], "priorUnacceptedIds": model["unacceptedIds"],
                        "appliedAtReview": model["applied"], "targetSpell": target_model_spell}
        target_validation = {"id": "KR198-TARGET-VALIDATION-CONTEXT-242", "dataPass": validation["dataPass"],
                             "sourcePass": validation["sourcePass"], "wholeBatchAccepted": validation["wholeBatchAccepted"],
                             "unacceptedIds": validation["unacceptedIds"], "canonicalApplied": validation["canonicalApplied"],
                             "qualification": validation["qualification"]}
        case_context = {"id": "KR198-TARGET-CASE-CONTEXT-242", "cases": selected_cases,
                        "caseCount": len(selected_cases), "events": sum(x["events"] for x in selected_cases),
                        "forwardOperations": sum(x["forwardOperations"] for x in selected_cases),
                        "inverseOperations": sum(x["inverseOperations"] for x in selected_cases),
                        "allCaseFilesEqualCasebookAndReplay": all(x["freshReplayPassed"] for x in selected_cases)}

        copied_sources.update({
            "CASE_METADATA.json": json_bytes(case_context),
            "PRIOR_DIRECTOR_DECISION_CONTEXT.json": json_bytes(target_context),
            "PRIOR_MODEL_CONTEXT.json": json_bytes(target_model),
            "SOURCE_OBLIGATIONS.json": json_bytes(filtered_obligations),
            "QUESTION_DISPOSITIONS.json": json_bytes(target_questions),
            "FUTURE_OBLIGATION_DISPOSITIONS.json": json_bytes(target_futures),
            "CASE_DISPOSITIONS.json": json_bytes(target_case_dispositions),
            "CLOCK_AND_INVERSE_RESULTS.json": json_bytes({"caseResults": target_clock_rows,
                                                           "events": sum(x["events"] for x in selected_cases),
                                                           "forwardOperations": sum(x["forwardOperations"] for x in selected_cases),
                                                           "inverseOperations": sum(x["inverseOperations"] for x in selected_cases),
                                                           "allPass": True}),
            "PROPOSAL_OPERATIONS.json": json_bytes(target_ops),
            "FACT_SOURCE_REGISTER.json": json_bytes(fact_sources),
            "HOLD_REGISTER.json": json_bytes(target_hold_register),
            "VALIDATION_CONTEXT.json": json_bytes(target_validation),
            "QUALIFICATIONS.json": json_bytes(qualifications),
        })

        audit_files = [PRIOR_AUDIT, PRIOR_RECEIPT, PRIOR_DECISION]
        for file in audit_files:
            raw = file.read_bytes()
            dest = "provenance/" + file.name
            copied_sources[dest] = raw
            origin_rows.append({"destination": dest, "localSourcePath": str(file.relative_to(ROOT)).replace("\\", "/"),
                                "bytes": len(raw), "sha256": sha(raw), "crc32": f"{zlib.crc32(raw) & 0xffffffff:08x}"})
        origin_doc = {"id": "KR198-EXACT-ORIGINAL-MEMBER-BINDINGS-242",
                      "sourceReturnArchive": {"bytes": prior_delivery["archive"]["bytes"], "sha256": prior_delivery["archive"]["sha256"]},
                      "copiedOriginalMemberCount": len([x for x in origin_rows if "sourceArchiveMember" in x]),
                      "copiedMembers": origin_rows,
                      "priorIndependentAuditStatus": "PASS"}
        copied_sources["ORIGINAL_MEMBER_BINDINGS.json"] = json_bytes(origin_doc)
        copied_sources["README.md"] = (
            "# Return198 target evidence supplement\n\n"
            "This supplement preserves the exact prior procedure and all eight original faction-omniscience cases, plus the related questions, future obligations, blocker, holds, and prior audit receipt. "
            "The four previously accepted Knowledge/Revelation identities are recorded as closed context and are outside this review. "
            "The case files were compared against Return198 CASEBOOK objects and replayed locally before packaging.\n"
        ).encode("utf-8")
        assert len(copied_sources) == len(set(copied_sources)) and all(safe_member(x) for x in copied_sources)

        SUP_DIR.mkdir(parents=True)
        sup_zip = SUP_DIR / SUP_ZIP_NAME
        with zipfile.ZipFile(sup_zip, "w", zipfile.ZIP_DEFLATED, compresslevel=6) as out:
            rows = []
            for name in sorted(copied_sources):
                raw = copied_sources[name]
                out.writestr(name, raw, compress_type=zipfile.ZIP_DEFLATED, compresslevel=6)
                rows.append({"path": name, "bytes": len(raw), "sha256": sha(raw), "crc32": f"{zlib.crc32(raw) & 0xffffffff:08x}"})
            manifest = {"id": "KR198-TARGET-WITNESS-SUPPLEMENT-MANIFEST-242",
                        "sourceReturnArchive": {"bytes": prior_delivery["archive"]["bytes"], "sha256": prior_delivery["archive"]["sha256"]},
                        "targetIdentity": SPELL, "memberCountExcludingSelf": len(rows), "members": rows}
            out.writestr("SUPPLEMENT_MANIFEST.json", json_bytes(manifest), compress_type=zipfile.ZIP_DEFLATED, compresslevel=6)
    sup_zip = SUP_DIR / SUP_ZIP_NAME
    sup_file_bytes = sup_zip.read_bytes()
    sup_delivery = {"id": "KR198-TARGET-WITNESS-SUPPLEMENT-DELIVERY-242",
                    "archive": {"path": SUP_ZIP_NAME, "bytes": len(sup_file_bytes), "sha256": sha(sup_file_bytes)},
                    "members": len(copied_sources) + 1, "manifestBindings": len(copied_sources),
                    "sourceReturn198Archive": {"path": str(PRIOR_RETURN_ZIP.relative_to(ROOT)).replace("\\", "/"),
                                               "bytes": PRIOR_RETURN_ZIP.stat().st_size, "sha256": sha(PRIOR_RETURN_ZIP.read_bytes())},
                    "targetIdentity": SPELL, "originalCases": 8, "events": sum(x["events"] for x in selected_cases),
                    "accepted": False, "applied": False}
    sup_delivery_path = SUP_DIR / SUP_DELIVERY_NAME
    sup_delivery_path.write_bytes(json_bytes(sup_delivery))
    with zipfile.ZipFile(sup_zip) as zsup:
        assert zsup.testzip() is None
        sm = read(zsup.read("SUPPLEMENT_MANIFEST.json"))
        assert set(zsup.namelist()) - {"SUPPLEMENT_MANIFEST.json"} == {x["path"] for x in sm["members"]}
        for row in sm["members"]:
            assert zip_member_binding(zsup, row["path"]) == {k: row[k] for k in ("bytes", "sha256", "crc32")}

    entries = {x["id"]: x for x in index["entries"]}
    cards = {x["id"]: x for x in catalog["spells"]}
    entry, card = entries[SPELL], cards[SPELL]
    ptr = int(entry["wholeCardPointer"].rsplit("/", 1)[1])
    assert catalog["spells"][ptr]["id"] == SPELL
    assert entry["authoredStatus"] == "pending-authored-procedure" and entry["sourceStatus"] == "blocked-pending-operational-review"

    with zipfile.ZipFile(FULL / Path(HISTORICAL_ARCHIVE).name) as old_archive:
        assert old_archive.testzip() is None
        old_member_names = old_archive.namelist()
        assert len(old_member_names) == len(set(old_member_names)) and all(safe_member(x) for x in old_member_names)
        old_sources = {}
        for row in hist_bindings:
            raw = old_archive.read("sources/" + row["path"])
            assert len(raw) == row["bytes"] and sha(raw) == row["sha256"]
            old_sources[row["path"]] = raw

    refreshed, current_sources, changed = [], {}, []
    for old in hist_bindings:
        path = old["path"]
        assert safe_member(path)
        raw = workspace_bytes(path)
        row = {"path": path, "bytes": len(raw), "sha256": sha(raw), "gitBlobSHA1": git_blob_id(raw),
               "packetMember": "sources_current/" + path}
        refreshed.append(row)
        current_sources[row["packetMember"]] = raw
        if raw != old_sources[path]:
            changed.append({"path": path, "historicalBytes": len(old_sources[path]), "historicalSha256": sha(old_sources[path]),
                            "currentBytes": len(raw), "currentSha256": sha(raw)})
    assert len(refreshed) == 126 and len({x["path"] for x in refreshed}) == 126

    now = datetime.now(timezone.utc).isoformat()
    current_candidate = {
        "id": "RANK9-KNOWLEDGE-REVELATION5-CURRENT-SOURCE-CONTEXT-242",
        "recordedAtUtc": now,
        "status": "CURRENT_SOURCE_BINDINGS_REFRESHED_FOR_811_REVIEWED_37_PENDING_AUTHORITY",
        "sourceCommit": commit, "sourceBranch": branch, "sourceAuthority": AUTHORITY,
        "scope": {"group": GROUP, "pendingIds": IDS, "pendingCount": 1,
                  "explicitExclusions": ["cosmic-awareness", "cosmic-revelation", "divine-truth", "oracle-of-eternity"]},
        "historicalCandidateBinding": binding(HISTORICAL_CANDIDATE, hist_candidate_raw),
        "historicalSourceArchiveBinding": binding(HISTORICAL_ARCHIVE, hist_archive_raw),
        "historicalCandidateRecord": original_candidate_record,
        "historicalPriorCurrentCandidateRecord": old_record,
        "currentIndexEntry": entry, "currentCatalogCard": card,
        "historicalSourceBindings": hist_bindings, "currentSourceBindings": refreshed,
        "sourceBindingRefresh": {"count": len(refreshed), "changedSinceHistoricalArchive": changed,
                                 "sourceContentsFromCurrentWorkspaceSnapshot": True, "headCommit": commit},
        "currentPendingAuditBinding": binding(PENDING_IN, pending_raw),
        "currentQueueBinding": binding(QUEUE_IN, queue_raw),
        "priorReturn198TargetSupplement": {"path": str(sup_zip.relative_to(ROOT)).replace("\\", "/"),
                                           "bytes": len(sup_file_bytes), "sha256": sha(sup_file_bytes)},
        "priorBlocker": blocker,
        "preservedEvidence": {"questions": len(filtered_obligations["allQuestions"]),
                              "targetCaseCount": len(selected_cases), "targetEvents": sum(x["events"] for x in selected_cases),
                              "targetFutureObligations": len(target_futures), "targetHoldIds": sorted(target_hold_ids)},
        "accepted": False, "applied": False,
    }
    candidate_raw = json_bytes(current_candidate)

    current_return_docs = [
        str(RETURN241_AUDIT.relative_to(ROOT)).replace("\\", "/"),
        str(RETURN241_RECEIPT.relative_to(ROOT)).replace("\\", "/"),
        str(RETURN241_DELIVERY.relative_to(ROOT)).replace("\\", "/"),
        str(RETURN241_ZIP.relative_to(ROOT)).replace("\\", "/"),
        *[str((AUDIT / p).relative_to(ROOT)).replace("\\", "/") for p in RETURN240_DOCS],
        *[str((AUDIT / p).relative_to(ROOT)).replace("\\", "/") for p in RETURN239_DOCS],
        *[str((AUDIT / p).relative_to(ROOT)).replace("\\", "/") for p in RETURN238_DOCS],
        str(PRIOR_DECISION.relative_to(ROOT)).replace("\\", "/"),
        str(PRIOR_AUDIT.relative_to(ROOT)).replace("\\", "/"),
        str(PRIOR_RECEIPT.relative_to(ROOT)).replace("\\", "/"),
        "docs/audit/2026-10-08/full-game/director-spell-review-129/RANK9_KNOWLEDGEREVELATION5_APPLICATION_198.json",
        "docs/audit/2026-10-08/full-game/director-spell-review-129/RANK9_KNOWLEDGEREVELATION5_APPLICATION_VALIDATION_198.json",
        "docs/audit/2026-10-08/full-game/director-spell-review-129/RANK9_KNOWLEDGEREVELATION5_EXACT_ACCEPTANCE_198.json",
        "docs/audit/2026-10-08/full-game/director-spell-review-129/RANK9_KNOWLEDGEREVELATION5_INDEX_OPERATIONS_198.json",
        "docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT_HANDOFF_198.json",
        "docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT_SPELL_QUEUE_198.json",
    ]
    current_paths = [INDEX, CATALOG, QUEUE_IN, PENDING_IN, HANDOFF_IN, "START_HERE.md", *current_return_docs]
    current_files = {"current/" + p: workspace_bytes(p) for p in current_paths}

    carried_holds = {
        "AG190": {"ids": ["absolute-domination", "puppetmaster-s-realm"], "blockers": ["AG190-B01", "AG190-B02"]},
        "TF192": {"ids": ["time-stop", "eternal-prophecy", "fate-rewrite", "collapse-timeline"], "blockers": ["TF192-B01", "TF192-B02", "TF192-B04", "TF192-B05"]},
        "CC194": {"ids": ["unholy-ascendance"], "blockers": ["CC194-B04"]},
        "MD196": {"ids": ["mind-collapse", "unravel-identity"], "blockers": ["MD196-B01", "MD196-B02"]},
        "KR198": {"ids": [SPELL], "blockers": ["KR198-B01"]},
    }
    prior_applied_ids = ["cosmic-awareness", "cosmic-revelation", "divine-truth", "oracle-of-eternity"]
    prior_applied_index_entries = {sid: entries[sid] for sid in prior_applied_ids}
    assert all(entries[sid]["authoredStatus"] == "reviewed-authored-operational-playtest" for sid in prior_applied_ids)
    context = {
        "id": "RANK9-KNOWLEDGE-REVELATION5-CURRENT-DIRECTOR-CONTEXT-242",
        "recordedAtUtc": now, "sourceCommit": commit, "sourceBranch": branch, "sourceAuthority": AUTHORITY,
        "targetGroup": {"group": GROUP, "pendingIds": IDS, "count": 1},
        "currentQueue241NextGroupConfirmedByReturn241": decision241["nextPendingGroup"],
        "currentPendingAudit": pending["id"],
        "latestReturn241": {"audit": audit241["id"], "status": audit241["status"],
                            "acceptedIds": [], "heldIds": ["mind-collapse", "unravel-identity"],
                            "authorityUnchanged": AUTHORITY, "applicationPerformed": False},
        "priorKnowledgeRevelation198": {"acceptedIds": prior_applied_ids,
                                         "currentIndexEntries": prior_applied_index_entries, "unacceptedIds": [SPELL],
                                         "retainedBlockerIds": ["KR198-B01"],
                                         "currentIndexEntry": entry},
        "retainedNamedBlockersOutsideScope": carried_holds,
        "qualifiedScope": "One pending identity only. The four accepted/applied Knowledge/Revelation identities and all other pending cohorts are closed context, not review targets.",
        "qualification": "Review static authored procedure only. Use exact current 126 source bindings, current native card/index/queue, prior KR198 procedure and eight replayed cases. Retain KR198-B01 and KR198-H01/H02/H03/H04/H05/H06 unless a source-grounded complete faction past/present/distant-branch record and a concrete, scoped likely-future witness now pass the preserved whole positive obligation. Do not invent branch rosters, private member histories, split/dissolution events, or forecasts; distinguish missing records from true absence. Preserve all other named blocker cohorts and downstream runtime/playtest/balance/cosmology/domain/completion/release gates.",
    }

    request = (
        "GPT director — continue the ordinary spell review at current workspace authority 811 reviewed-applied / 37 pending / 0 accepted-unapplied, with 535 complete standalone procedures and 173 scoped interfaces. Review exactly faction-omniscience-supreme, the only pending identity in rank9-knowledge-revelation5.\n\n"
        f"Current source snapshot is branch {branch}, HEAD {commit}, plus the exact working-tree overlay bindings in this packet. Use the refreshed 126 source rows, current index/catalog/queue/handoff/pending audit, Return241 independent audit, and the attached compact Return198 target-witness supplement. The sealed Return238, Return239, and Return240 archives, decisions, audits and receipts are included. Current-source packet SHA will be bound in its delivery JSON.\n\n"
        "The four Knowledge/Revelation identities cosmic-awareness, cosmic-revelation, divine-truth, and oracle-of-eternity were accepted in Return198 and applied; do not reopen or reevaluate them. Preserve their accepted shared interfaces only as context. Return241’s two Memory/Denial6 identities remain held and unapplied under MD196-B01/B02; do not reopen them. Preserve Return240 CC194-B04, Return239 TF192-B01/B02/B04/B05, and Return238 AG190-B01/B02.\n\n"
        "Reassess only KR198-B01 and carry KR198-H01/H02/H03/H04/H05/H06 unless current bound evidence actually closes the blocker. The prior blocker requires a source-grounded exact canonical-faction past/present/distant-branch ledger and sufficiently concrete source-qualified likely-future premises for a positive whole-dossier witness. The current source book names factions and gives broad descriptions, but does not authorize inventing branch rosters, private member histories, split/dissolution events, or a campaign forecast. Distinguish true absence from missing records; separate public institutional facts, private member information, erased memory, divinely supplied truth, and recorded forecasts. Any likely-future statement must name its source premises, horizon, assumptions, uncertainty, and cannot force future decisions or grant faction membership benefits. Preserve the actual native card, costs, access, acquisition routes, prior lifecycle and every passing/adverse branch.\n\n"
        "Preserve/replay all eight exact Return198 target cases and the original questions, focused addenda, two required main obligations, future obligations, case/hold dispositions, and reversible operations. Accept only if the actual current source set supports a complete positive factual dossier and the source-qualified forecast obligation, with all protected/private/absence boundaries and failure branches passing. If it remains unsupported, return accepted=false/applied=false with KR198-B01 and its exact minimum missing witness. Keep runtime, implementation, human-play, balance, cosmology, domain-closure, completion, and release gates closed. Do not modify canonical files or run supplied programs. Name the next pending group after this exact-one-target decision."
    )

    source_files = {
        "CURRENT_CONTEXT_242.json": json_bytes(context),
        "CURRENT_SOURCE_CONFERENCE_CANDIDATE_242.json": candidate_raw,
        "HISTORICAL_SOURCE_CONFERENCE_CANDIDATE_01.json": hist_candidate_raw,
        "HISTORICAL_SOURCE_CONFERENCE_ARCHIVE_01.zip": hist_archive_raw,
        "HISTORICAL_NOTES/RANK9KNOWLEDGEREVELATION5_NEXT_CONFERENCE_NOTES_129.json": notes_raw,
        "REQUEST_242.txt": request.encode("utf-8"),
        "CURRENT_RETURN198_TARGET_WITNESS_SUPPLEMENT_242.zip": sup_file_bytes,
        "CURRENT_RETURN198_TARGET_WITNESS_SUPPLEMENT_242_DELIVERY.json": sup_delivery_path.read_bytes(),
        **current_files, **current_sources,
    }
    assert len(source_files) == len(set(source_files)) and all(safe_member(x) for x in source_files)
    OUT.mkdir(parents=True)
    current_candidate_path = OUT / "CURRENT_SOURCE_CONFERENCE_CANDIDATE_242.json"
    current_candidate_path.write_bytes(candidate_raw)
    packet_zip = OUT / PACKET_ZIP_NAME
    with zipfile.ZipFile(packet_zip, "w", zipfile.ZIP_DEFLATED, compresslevel=6) as out:
        rows = []
        for name in sorted(source_files):
            raw = source_files[name]
            out.writestr(name, raw, compress_type=zipfile.ZIP_DEFLATED, compresslevel=6)
            rows.append({"path": name, "bytes": len(raw), "sha256": sha(raw), "crc32": f"{zlib.crc32(raw) & 0xffffffff:08x}"})
        manifest = {"id": "RANK9-KNOWLEDGE-REVELATION5-CURRENT-SOURCE-MANIFEST-242",
                    "sourceCommit": commit, "sourceBranch": branch, "sourceAuthority": AUTHORITY,
                    "group": GROUP, "pendingIds": IDS, "memberCountExcludingSelf": len(rows), "members": rows}
        out.writestr("MANIFEST.json", json_bytes(manifest), compress_type=zipfile.ZIP_DEFLATED, compresslevel=6)
    packet_bytes = packet_zip.read_bytes()
    packet_binding = binding(str(packet_zip.relative_to(ROOT)).replace("\\", "/"), packet_bytes)
    candidate_binding = binding(str(current_candidate_path.relative_to(ROOT)).replace("\\", "/"), candidate_raw)
    packet_delivery = {"id": "RANK9-KNOWLEDGE-REVELATION5-CURRENT-SOURCE-DELIVERY-242", "status": "PREPARED_UNSENT",
                       "archive": {**packet_binding}, "members": len(rows) + 1, "manifestBindings": len(rows),
                       "sourceCommit": commit, "sourceBranch": branch, "sourceAuthority": AUTHORITY,
                       "group": GROUP, "pendingIds": IDS, "candidate": candidate_binding,
                       "historicalCandidate": binding(HISTORICAL_CANDIDATE, hist_candidate_raw),
                       "historicalArchive": binding(HISTORICAL_ARCHIVE, hist_archive_raw),
                       "targetWitnessSupplement": {"path": str(sup_zip.relative_to(ROOT)).replace("\\", "/"),
                                                    "bytes": len(sup_file_bytes), "sha256": sha(sup_file_bytes)},
                       "sourceFilesRefreshed": len(refreshed), "sourceFilesChangedSinceHistoricalArchive": changed,
                       "accepted": False, "applied": False, "conversation": CHAT}
    packet_delivery_path = OUT / PACKET_DELIVERY_NAME
    packet_delivery_raw = json_bytes(packet_delivery)
    packet_delivery_path.write_bytes(packet_delivery_raw)

    # Recompute the full exact pending set and preserve the Return241 holds before queuing this one identity.
    pending_audit = copy.deepcopy(pending)
    pending_audit.update({"id": "CURRENT37-PENDING-IDENTITY-AUDIT-242", "recordedAtUtc": now,
                          "status": "PASSED_EXACT_CURRENT_INDEX_PENDING_SET_AFTER_RETURN241",
                          "authority": AUTHORITY, "pendingCount": 37, "pendingIds": pending["pendingIds"],
                          "lastDirectorReturn": {"return": 224, "acceptedIds": [], "appliedIds": [],
                                                 "heldIds": ["mind-collapse", "unravel-identity"],
                                                 "blockers": {"mind-collapse": ["MD196-B01"], "unravel-identity": ["MD196-B02"]},
                                                 "independentAudit": binding(str(RETURN241_AUDIT.relative_to(ROOT)).replace("\\", "/"), RETURN241_AUDIT.read_bytes())},
                          "appliedReturn241": False,
                          "preparedNextGroup": {"group": GROUP, "pendingIds": IDS, "pendingCount": 1,
                                                "packet": packet_binding, "status": "PREPARED_UNSENT"},
                          "closed335AndCompletedCohortsReopened": False})
    pending_audit["indexBinding"] = binding(INDEX, index_raw)
    pending_audit["catalogBinding"] = binding(CATALOG, catalog_raw)
    pending_audit_path = PENDING_OUT
    pending_audit_path.write_bytes(json_bytes(pending_audit))

    packet_record = {"id": "RANK9KNOWLEDGEREVELATION5-PACKET-242", "status": "PREPARED_UNSENT", "group": GROUP,
                     "pendingIds": IDS, "sourceAuthority": AUTHORITY, "sourceCommit": commit,
                     "archive": packet_binding,
                     "deliveryManifest": binding(str(packet_delivery_path.relative_to(ROOT)).replace("\\", "/"), packet_delivery_raw),
                     "targetWitnessSupplement": packet_delivery["targetWitnessSupplement"],
                     "sourceBindings": len(refreshed), "priorCases": len(selected_cases),
                     "events": sum(x["events"] for x in selected_cases), "canonicalChanges": False}
    PACKET_RECORD.write_bytes(json_bytes(packet_record))
    prep_checks = [
        "Return241 independent audit passed with both Memory/Denial6 identities held and no applications.",
        "Exact current authority and 37 pending index identities were rebound from the workspace overlay.",
        "Only faction-omniscience-supreme is in the next group and remains pending in the native catalog.",
        "All 126 historical Knowledge/Revelation source members validated and were refreshed from current workspace bytes.",
        "Return198 target procedure, eight cases, exact blocker/holds, linked questions, future obligations and source provenance were preserved.",
        "All eight prior target case files equal their CASEBOOK records and independently replay with reversible operations.",
        "The four previously accepted Knowledge/Revelation identities are marked closed context and excluded from scope.",
        "Outer packet and supplement manifests bind every member by bytes, SHA-256 and CRC32.",
    ]
    preparation = {"id": "RANK9-KNOWLEDGE-REVELATION5-SOURCE-PREPARATION-242", "recordedAtUtc": now,
                   "status": "PASS", "checks": [{"check": x, "passed": True} for x in prep_checks],
                   "checkCount": len(prep_checks), "sourceCommit": commit, "sourceBranch": branch,
                   "sourceAuthority": AUTHORITY, "targetGroup": GROUP, "pendingIds": IDS,
                   "packet": packet_binding, "deliveryManifest": binding(str(packet_delivery_path.relative_to(ROOT)).replace("\\", "/"), packet_delivery_raw),
                   "targetWitnessSupplement": packet_delivery["targetWitnessSupplement"],
                   "refreshedBindings": len(refreshed), "changedHistoricalBindings": changed,
                   "priorCases": len(selected_cases), "priorEvents": sum(x["events"] for x in selected_cases),
                   "retainedBlockerIds": ["KR198-B01"], "canonicalChanges": False, "accepted": False, "applied": False}
    PREPARATION.write_bytes(json_bytes(preparation))

    packet_request = {"group": GROUP, "pendingIds": IDS, "pendingCount": 1, "status": "CURRENT_SOURCE_PACKET_PREPARED_UNSENT",
                      "freshPacketRequiredForCurrentAuthority": False, "packet": packet_binding,
                      "deliveryManifest": binding(str(packet_delivery_path.relative_to(ROOT)).replace("\\", "/"), packet_delivery_raw),
                      "packetRecord": binding(str(PACKET_RECORD.relative_to(ROOT)).replace("\\", "/"), PACKET_RECORD.read_bytes()),
                      "sourcePreparation": binding(str(PREPARATION.relative_to(ROOT)).replace("\\", "/"), PREPARATION.read_bytes())}
    q = copy.deepcopy(queue)
    q.update({"id": "SPELL-REVIEW-QUEUE-242", "recordedAtUtc": now, "currentAuthority": AUTHORITY,
              "pendingCount": 37, "nextGroup": GROUP, "next": packet_request, "nextPreparedRequest": packet_request,
              "packetStatus": "RANK9_KNOWLEDGE_REVELATION5_PACKET_242_PREPARED_UNSENT_811_37",
              "currentPacket": packet_binding, "currentPacketDelivery": packet_request["deliveryManifest"],
              "currentPreparation": packet_request["sourcePreparation"],
              "pendingIdentityAudit": {"path": str(PENDING_OUT.relative_to(ROOT)).replace("\\", "/"),
                                       "pending": 37, "sha256": sha(PENDING_OUT.read_bytes())},
              "currentReturnAudit": binding(str(RETURN241_AUDIT.relative_to(ROOT)).replace("\\", "/"), RETURN241_AUDIT.read_bytes()),
              "currentReturnBinding": binding(str(RETURN241_ZIP.relative_to(ROOT)).replace("\\", "/"), RETURN241_ZIP.read_bytes()),
              "currentReturnDelivery": binding(str(RETURN241_DELIVERY.relative_to(ROOT)).replace("\\", "/"), RETURN241_DELIVERY.read_bytes()),
              "currentReturnArchive": binding(str(RETURN241_ZIP.relative_to(ROOT)).replace("\\", "/"), RETURN241_ZIP.read_bytes())})
    groups = []
    for old in q["currentPendingGroups"]:
        g = copy.deepcopy(old)
        if g["group"] == GROUP:
            g.update({"status": "CURRENT_SOURCE_PACKET_PREPARED_UNSENT", "freshPacketRequiredForCurrentAuthority": False,
                      "packet": packet_binding, "deliveryManifest": packet_request["deliveryManifest"]})
        groups.append(g)
    q["currentPendingGroups"] = groups
    QUEUE_OUT.write_bytes(json_bytes(q))

    h = copy.deepcopy(handoff)
    h.update({"id": "CURRENT-HANDOFF-242", "recordedAtUtc": now,
              "status": "RANK9_MEMORYDENIAL6_RETURN241_AUDITED_NEXT_KNOWLEDGE_REVELATION5_811_37",
              "currentAuthority": AUTHORITY,
              "latestBatch": {"return": 224, "group": "rank9-memory-denial6", "ids": ["mind-collapse", "unravel-identity"],
                              "acceptedIds": [], "appliedIds": [], "heldIds": ["mind-collapse", "unravel-identity"],
                              "blockers": {"mind-collapse": ["MD196-B01"], "unravel-identity": ["MD196-B02"]},
                              "independentAudit": binding(str(RETURN241_AUDIT.relative_to(ROOT)).replace("\\", "/"), RETURN241_AUDIT.read_bytes())},
              "nextGroup": GROUP, "nextPendingCount": 1, "nextPreparedRequest": packet_request,
              "pendingIdentityAudit": {"id": pending_audit["id"], "path": str(PENDING_OUT.relative_to(ROOT)).replace("\\", "/"),
                                       "pendingCount": 37, "sha256": sha(PENDING_OUT.read_bytes())},
              "currentQueueBinding": binding(str(QUEUE_OUT.relative_to(ROOT)).replace("\\", "/"), QUEUE_OUT.read_bytes()),
              "currentPacket": packet_binding, "currentPacketDelivery": packet_request["deliveryManifest"],
              "currentPreparation": packet_request["sourcePreparation"],
              "currentReturnAudit": binding(str(RETURN241_AUDIT.relative_to(ROOT)).replace("\\", "/"), RETURN241_AUDIT.read_bytes()),
              "currentReturnBinding": binding(str(RETURN241_ZIP.relative_to(ROOT)).replace("\\", "/"), RETURN241_ZIP.read_bytes()),
              "currentReturnDelivery": binding(str(RETURN241_DELIVERY.relative_to(ROOT)).replace("\\", "/"), RETURN241_DELIVERY.read_bytes()),
              "resumePriority": "Upload Packet242, delivery manifest, and Return198 target-witness supplement to GPT; ping if the response stalls; independently audit and apply only exact accepted IDs, then continue the next pending spell group."})
    HANDOFF_OUT.write_bytes(json_bytes(h))
    snapshot = ("# Current ordinary spell-review checkpoint 242\n\n"
                "Return241 passed independent audit with both Memory/Denial6 spells held and unapplied. "
                "Authority remains **811 reviewed / 37 pending / 0 accepted-unapplied**, with 535 complete standalone procedures. "
                "The next one-identity group is Faction Omniscience (Supreme), carried forward under KR198-B01 with the original eight target cases. "
                "A refreshed 126-source packet and compact Return198 witness supplement are prepared for the GPT director. Runtime and downstream gates remain closed.\n")
    SNAPSHOT_OUT.write_text(snapshot, encoding="utf-8", newline="\n")

    # Seal the source archive and all listed members before considering it ready to upload.
    with zipfile.ZipFile(packet_zip) as zpacket:
        assert zpacket.testzip() is None
        packet_names = zpacket.namelist()
        manifest = read(zpacket.read("MANIFEST.json"))
        assert len(packet_names) == len(set(packet_names)) == len(rows) + 1
        assert set(packet_names) - {"MANIFEST.json"} == {x["path"] for x in manifest["members"]}
        for row in manifest["members"]:
            assert zip_member_binding(zpacket, row["path"]) == {k: row[k] for k in ("bytes", "sha256", "crc32")}
    print(json.dumps({"status": "PREPARED_UNSENT", "sourceCommit": commit, "authority": AUTHORITY,
                      "group": GROUP, "pendingIds": IDS, "packet": packet_binding,
                      "delivery": packet_request["deliveryManifest"], "supplement": packet_delivery["targetWitnessSupplement"],
                      "refreshedSources": len(refreshed), "changedSources": len(changed),
                      "priorCases": len(selected_cases), "priorEvents": sum(x["events"] for x in selected_cases),
                      "checks": len(prep_checks)}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
