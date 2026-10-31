from __future__ import annotations

import gzip
import hashlib
import json
import pathlib
import zipfile
from datetime import datetime, timezone
from typing import Any


ROOT = pathlib.Path(__file__).resolve().parents[5]
AUDIT = pathlib.Path(__file__).resolve().parent
OUT = AUDIT / "rank9_time_stop_current_source_318_prepared"
BASELINE_ZIP = AUDIT / "rank9_timefate6_current_source_282_prepared" / "DD_Rank9_TimeFate6_CurrentSource_282.zip"
RETURN282 = AUDIT / "rank9_timefate6_return282_received" / "DD_Rank9_TimeFate6_Director_Return282_HELD.zip"
RETURN308 = AUDIT / "rank9_defenseform8_return308_received" / "DD_Rank9_DefenseForm8_Director_Return308_HELD.zip"
RETURN316 = AUDIT / "rank9_wardcontrol6_reality_anchor_return316_received" / "DD_Rank9_WardControl6_Director_Return316_ACCEPTED.zip"


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def crc(data: bytes) -> str:
    import zlib
    return f"{zlib.crc32(data) & 0xffffffff:08x}"


def canonical(obj: Any) -> bytes:
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def pretty(obj: Any) -> bytes:
    return (json.dumps(obj, ensure_ascii=False, indent=2) + "\n").encode("utf-8")


def binding(path: pathlib.Path, display: str | None = None) -> dict[str, Any]:
    raw = path.read_bytes()
    return {"path": display or path.relative_to(ROOT).as_posix(), "bytes": len(raw), "sha256": sha(raw), "crc32": crc(raw)}


def load_json(path: pathlib.Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def safe_member(name: str) -> None:
    p = pathlib.PurePosixPath(name)
    if p.is_absolute() or ".." in p.parts or "\\" in name or not name:
        raise ValueError(f"unsafe member: {name}")


def put(members: dict[str, bytes], name: str, raw: bytes) -> None:
    safe_member(name)
    if name in members:
        raise ValueError(f"duplicate member: {name}")
    members[name] = raw


def json_member(members: dict[str, bytes], name: str, value: Any) -> None:
    put(members, name, pretty(value))


def extract_zip_member(path: pathlib.Path, name: str) -> bytes:
    with zipfile.ZipFile(path) as zf:
        return zf.read(name)


def find_row(rows: list[dict[str, Any]], spell_id: str) -> dict[str, Any]:
    found = [row for row in rows if row.get("id") == spell_id]
    if len(found) != 1:
        raise ValueError(f"expected one catalog row for {spell_id}, found {len(found)}")
    return found[0]


def main() -> None:
    if OUT.exists():
        for p in OUT.iterdir():
            if p.is_file():
                p.unlink()
            elif p.is_dir():
                raise RuntimeError(f"unexpected nested directory in output: {p}")
    OUT.mkdir(parents=True, exist_ok=True)

    index_path = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json"
    catalog_path = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json"
    placements_path = ROOT / "DescentReviewChanges/ReviewBible/src/data/spell-placements.json"
    core_path = ROOT / "DescentReviewChanges/ReviewBible/data/public/Decennium_Descent_Core_Systems_Data_v2_Known_Descent.json"
    spells_js_path = ROOT / "DescentReviewChanges/ReviewBible/src/data/spells.js"
    queue317_path = AUDIT / "CURRENT_SPELL_QUEUE_317.json"
    handoff317_path = AUDIT / "CURRENT_HANDOFF_317.json"
    pending317_path = AUDIT / "CURRENT25_PENDING_IDENTITY_AUDIT_317.json"

    current_index_raw = index_path.read_bytes()
    current_catalog_raw = catalog_path.read_bytes()
    current_index = json.loads(current_index_raw)
    current_catalog = json.loads(current_catalog_raw)
    queue317 = load_json(queue317_path)
    handoff317 = load_json(handoff317_path)
    pending317 = load_json(pending317_path)
    spells = current_catalog["spells"]
    time_stop_row = find_row(spells, "time-stop")
    timeless_form_row = find_row(spells, "timeless-form")
    entries = current_index["entries"]
    time_stop_index = next(x for x in entries if x.get("id") == "time-stop")
    timeless_form_index = next(x for x in entries if x.get("id") == "timeless-form")

    # Packet282 is the baseline. Read its embedded candidate directly from the
    # exact archived bytes, then compare every one of its 140 raw source bindings.
    baseline_archive_raw = BASELINE_ZIP.read_bytes()
    baseline_archive_binding = binding(BASELINE_ZIP)
    with zipfile.ZipFile(BASELINE_ZIP) as zf:
        baseline_candidate_raw = zf.read("CURRENT_SOURCE_CONFERENCE_CANDIDATE_282.json")
        baseline_manifest_raw = zf.read("MANIFEST.json")
    baseline_candidate = json.loads(baseline_candidate_raw)
    baseline_manifest = json.loads(baseline_manifest_raw)
    old_bindings = baseline_candidate["sourceBindings"]
    if len(old_bindings) != 140:
        raise ValueError(f"Packet282 inventory changed: expected 140 rows, found {len(old_bindings)}")
    comparison_rows: list[dict[str, Any]] = []
    changed_paths: list[str] = []
    current_by_path: dict[str, bytes] = {}
    old_archive_names = {m["path"]: m for m in baseline_manifest["members"]}
    for old in old_bindings:
        rel = old["path"]
        local = ROOT / pathlib.Path(rel)
        if not local.is_file():
            comparison_rows.append({"path": rel, "oldBytes": old["bytes"], "oldSha256": old["sha256"], "currentBytes": None, "currentSha256": None, "status": "MISSING"})
            changed_paths.append(rel)
            continue
        raw = local.read_bytes()
        current_by_path[rel] = raw
        current_sha = sha(raw)
        status = "UNCHANGED" if len(raw) == old["bytes"] and current_sha == old["sha256"] else "CHANGED"
        if status == "CHANGED":
            changed_paths.append(rel)
        archive_name = "sources_current/" + rel
        archived_member = old_archive_names.get(archive_name)
        if not archived_member or archived_member["bytes"] != old["bytes"] or archived_member["sha256"] != old["sha256"]:
            raise ValueError(f"Packet282 manifest does not bind baseline source {rel}")
        comparison_rows.append({
            "path": rel,
            "oldBytes": old["bytes"],
            "oldSha256": old["sha256"],
            "currentBytes": len(raw),
            "currentSha256": current_sha,
            "status": status,
            "unchangedBinding": {"archive": baseline_archive_binding, "member": archive_name} if status == "UNCHANGED" else None,
        })
    if changed_paths != ["DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json"]:
        raise ValueError(f"Unexpected Packet282 source delta: {changed_paths}")

    # Recover the latest Time Stop blocker, procedure and preserved casebook from
    # the exact Return282 archive; retain only the Time Stop case records.
    return282_raw = RETURN282.read_bytes()
    return282_binding = binding(RETURN282)
    with zipfile.ZipFile(RETURN282) as zf:
        procedure_raw = zf.read("procedures/time-stop.json")
        hold_register_raw = zf.read("HOLD_REGISTER.json")
        casebook_gz = zf.read("CASEBOOK.json.gz")
        decision_raw = zf.read("DIRECTOR_DECISION.json")
        question_dispositions_raw = zf.read("QUESTION_DISPOSITIONS.json")
    procedure = json.loads(procedure_raw)
    hold_register = json.loads(hold_register_raw)
    casebook = json.loads(gzip.decompress(casebook_gz))
    all_cases = casebook.get("cases", [])
    ts_cases = [c for c in all_cases if c.get("spellId") == "time-stop"]
    expected_ids = procedure["caseIds"]
    if [c.get("id") for c in ts_cases] != expected_ids or len(ts_cases) != 14:
        raise ValueError("Return282 Time Stop casebook does not exactly match the 14 procedure case IDs")
    blocker = next(x for x in hold_register["currentBlockers"] if x["id"] == "TF192-B01")
    if procedure.get("blockerIds") != ["TF192-B01"] or not blocker:
        raise ValueError("Time Stop procedure/blocker binding is inconsistent")
    qualification_ids = procedure["holdIds"]
    # The procedure's boundary map uses uppercase names; bind each exact hold ID
    # to the authoritative wording through an explicit deterministic mapping.
    boundary_map = {
        "TF192-Q-BALANCE": "BALANCE", "TF192-Q-COMPLETION": "COMPLETION",
        "TF192-Q-COSMOLOGY": "COSMOLOGY", "TF192-Q-DOMAIN": "DOMAIN",
        "TF192-Q-PHYSICAL": "PHYSICAL", "TF192-Q-PLAY": "PLAY",
        "TF192-Q-RELEASE": "RELEASE", "TF192-Q-RUNTIME": "RUNTIME",
        "TF192-Q-SOURCE": "SOURCE",
    }
    qualifications = {qid: procedure["boundaries"][boundary_map[qid]] for qid in boundary_map}
    if set(qualifications) - set(qualification_ids):
        raise ValueError("Procedure is missing one or more qualification IDs")

    # Filter the exact nine original questions, the one focused addendum, and the
    # four Time Stop requirements from the Packet282 source candidate.
    candidate_questions = baseline_candidate["questions"]
    qids = [f"TF9-Q{i:02}" for i in range(1, 8)] + ["TF9-Q32", "TIME129-ADD01"]
    selected_questions = [q for q in candidate_questions if q.get("id") in qids and q.get("id") != "TIME129-ADD01"]
    if {q.get("id") for q in selected_questions} != set(qids) - {"TIME129-ADD01"}:
        raise ValueError("Packet282 source candidate is missing a requested original Time Stop question")
    selected_dispositions = []
    question_dispositions = json.loads(question_dispositions_raw)
    for item in question_dispositions.get("dispositions", []):
        if item.get("questionId") in qids:
            selected_dispositions.append(item)
    focused_addenda = [x for x in question_dispositions.get("focusedAddenda", []) if x.get("originalQuestionUnchanged", {}).get("id") == "TIME129-ADD01"]
    requirements = [x for x in baseline_candidate["futureCaseRequirements"] if x.get("id") in {"TF9-CAST", "TF9-STOP-MODES", "TF9-STOP-WORLD", "TF9-PERSISTENCE"}]
    if {x.get("id") for x in requirements} != {"TF9-CAST", "TF9-STOP-MODES", "TF9-STOP-WORLD", "TF9-PERSISTENCE"}:
        raise ValueError("Packet282 source candidate is missing a Time Stop future obligation")

    return308_binding = binding(RETURN308)
    return316_binding = binding(RETURN316)
    return308_delivery_path = AUDIT / "rank9_defenseform8_return308_received" / "DD_Rank9_DefenseForm8_Director_Return308_HELD_DELIVERY.json"
    return316_delivery_path = AUDIT / "rank9_wardcontrol6_reality_anchor_return316_received" / "DD_Rank9_WardControl6_Director_Return316_ACCEPTED_DELIVERY.json"

    members: dict[str, bytes] = {}
    # Current authority and canonical source snapshots.
    put(members, "authority/current/authored_review_index.json", current_index_raw)
    put(members, "authority/current/catalog.json", current_catalog_raw)
    for p, name in [(queue317_path, "authority/current/CURRENT_SPELL_QUEUE_317.json"),
                    (handoff317_path, "authority/current/CURRENT_HANDOFF_317.json"),
                    (pending317_path, "authority/current/CURRENT25_PENDING_IDENTITY_AUDIT_317.json")]:
        put(members, name, p.read_bytes())

    # Current catalog/index rows, core spell acquisition/source entries, and the
    # actual spell-placement source including the only immunity wording found.
    json_member(members, "evidence/native/current_time_stop_and_timeless_form_rows.json", {
        "sourceBindings": [binding(index_path), binding(catalog_path)],
        "indexEntries": {"time-stop": time_stop_index, "timeless-form": timeless_form_index},
        "catalogRows": {"time-stop": time_stop_row, "timeless-form": timeless_form_row},
    })
    put(members, "evidence/native/spell-placements.json", placements_path.read_bytes())
    put(members, "evidence/native/core_systems_time_stop_source.json", core_path.read_bytes())
    put(members, "evidence/native/spells.js", spells_js_path.read_bytes())

    # Fresh all-140 comparison; only the changed current file is shipped. The 139
    # exact unchanged members remain hash-bound to Packet282.
    json_member(members, "evidence/source_comparison/PACKET282_140_SOURCE_BINDING_COMPARISON.json", {
        "baselineArchive": baseline_archive_binding,
        "baselineCandidate": {"member": "CURRENT_SOURCE_CONFERENCE_CANDIDATE_282.json", "bytes": len(baseline_candidate_raw), "sha256": sha(baseline_candidate_raw)},
        "inventoryCount": len(comparison_rows),
        "unchangedCount": sum(x["status"] == "UNCHANGED" for x in comparison_rows),
        "changedCount": sum(x["status"] == "CHANGED" for x in comparison_rows),
        "missingCount": sum(x["status"] == "MISSING" for x in comparison_rows),
        "changedPaths": changed_paths,
        "rows": comparison_rows,
        "policy": "Packet282 is the exact baseline for 139 unchanged raw sources. Their archive-member bytes and SHA-256 values remain bound to Packet282. Current changed/new source files in this packet are supplied. No full historical archive is duplicated.",
    })
    put(members, "evidence/source_comparison/current_changed/authored_review_index.json", current_index_raw)
    json_member(members, "evidence/source_comparison/current_supplemental_bindings.json", {
        "note": "Supplemental current files directly needed to show Time Stop and Timeless Form native rows and acquisition/source wording. These were outside Packet282's 140-source comparison inventory; their current bytes are supplied here, without implying a change since Packet282.",
        "files": [binding(placements_path), binding(core_path), binding(spells_js_path)],
    })

    # Exact latest Time Stop procedure, blocker, qualification boundaries, target
    # questions/obligations, and hash-addressed records for 14 preserved cases.
    put(members, "evidence/time_stop/procedure.json", procedure_raw)
    json_member(members, "evidence/time_stop/TF192-B01.json", blocker)
    json_member(members, "evidence/time_stop/qualifications.json", {
        "qualificationIds": qualification_ids,
        "qualificationText": qualifications,
        "sourceProcedure": {"archive": return282_binding, "member": "procedures/time-stop.json", "bytes": len(procedure_raw), "sha256": sha(procedure_raw)},
    })
    json_member(members, "evidence/time_stop/questions_and_obligations.json", {
        "sourceCandidate": {"archive": baseline_archive_binding, "member": "CURRENT_SOURCE_CONFERENCE_CANDIDATE_282.json", "sha256": sha(baseline_candidate_raw)},
        "questions": selected_questions,
        "priorDispositions": selected_dispositions,
        "focusedAddenda": focused_addenda,
        "obligations": requirements,
    })
    case_manifest: list[dict[str, Any]] = []
    for case in ts_cases:
        case_id = case["id"]
        case_bytes = canonical(case)
        member = f"evidence/time_stop/preserved_cases/{case_id}.json"
        put(members, member, case_bytes)
        case_manifest.append({"id": case_id, "member": member, "bytes": len(case_bytes), "sha256": sha(case_bytes), "canonicalization": "UTF-8 JSON, sorted keys, no insignificant whitespace, ensure_ascii=false", "sourceCasebook": {"archive": return282_binding, "member": "CASEBOOK.json.gz", "memberBytes": len(casebook_gz), "memberSha256": sha(casebook_gz)}})
    json_member(members, "evidence/time_stop/preserved_case_manifest.json", {
        "count": len(case_manifest),
        "procedureCaseIds": expected_ids,
        "cases": case_manifest,
        "casebookDecodedCaseCount": len(all_cases),
    })
    put(members, "evidence/time_stop/return282_director_decision.json", decision_raw)

    # Timeless Form is shown only as an unresolved, pending dependency. Preserve
    # its latest Director hold and proposed lifecycle record without accepting it.
    with zipfile.ZipFile(RETURN308) as zf:
        tf_procedure_raw = zf.read("procedures/timeless-form.json")
        tf_req_raw = zf.read("evidence/TIMELESS_FORM_DIRECTOR_REQUIREMENTS_308.json")
    put(members, "evidence/timeless_form/return308_procedure_proposal.json", tf_procedure_raw)
    put(members, "evidence/timeless_form/director_requirements_308.json", tf_req_raw)
    for filename in ["TIMELESS_FORM_DIRECTOR_REQUIREMENTS_308.json", "TIMELESS_FORM_DIRECTOR_DECISION_308.json",
                     "TIMELESS_FORM_HOLD_RECEIPT_308.json", "TIMELESS_FORM_PACKET_308_INDEPENDENT_AUDIT.json",
                     "TIMELESS_FORM_RETURN308_INDEPENDENT_AUDIT.json"]:
        p = AUDIT / filename
        if p.exists():
            put(members, "evidence/timeless_form/current_audit/" + filename, p.read_bytes())
    put(members, "evidence/timeless_form/Return308_HELD.zip", RETURN308.read_bytes())
    put(members, "evidence/timeless_form/Return308_HELD_DELIVERY.json", return308_delivery_path.read_bytes())
    json_member(members, "evidence/timeless_form/blocker_dependency.json", {
        "timeStopBlocker": blocker,
        "timelessFormBlockerId": "DF218-B03",
        "timeStopStatus": {"index": time_stop_index, "catalog": {"id": time_stop_row["id"], "status": time_stop_row["status"], "operational": time_stop_row["operational"]}},
        "timelessFormStatus": {"index": timeless_form_index, "catalog": {"id": timeless_form_row["id"], "status": timeless_form_row["status"], "operational": timeless_form_row["operational"]}},
        "circularDependency": "Time Stop's required independently acting immune participant currently depends on Timeless Form's native immunity wording, but Timeless Form remains pending under DF218-B03 and lacks an accepted complete lifecycle. Neither pending identity is treated as accepted authority for the other.",
        "explicitJointInterfaceAuthoringRequest": "If no independently accepted immunity source exists, please issue an explicit, jointly authored interface contract for only the Time Stop/Timeless Form interaction needed here: lawful acquisition and paid activation, original duration/clock, immune actor body/equipment/resources/initiative, independent personal phase, legal counter/interruption or death branch, and exact interval/paused-queue restoration with no unauthorized refreshes, refunds, duplicate effects or resource grants. Keep both identities pending and do not adjudicate Timeless Form itself as accepted.",
    })

    # Prior accepted/applied Reality Anchor state, to anchor current authority.
    for filename in ["REALITY_ANCHOR_DIRECTOR_DECISION_316.json", "REALITY_ANCHOR_ACCEPTANCE_316.json",
                     "REALITY_ANCHOR_APPLICATION_316.json", "REALITY_ANCHOR_APPLICATION_VALIDATION_316.json",
                     "REALITY_ANCHOR_INDEX_OPERATIONS_316.json", "REALITY_ANCHOR_RETURN316_RECEIPT.json",
                     "REALITY_ANCHOR_RETURN316_INDEPENDENT_AUDIT.json"]:
        p = AUDIT / filename
        put(members, "authority/reality_anchor/" + filename, p.read_bytes())
    put(members, "authority/reality_anchor/Return316_ACCEPTED.zip", RETURN316.read_bytes())
    put(members, "authority/reality_anchor/Return316_ACCEPTED_DELIVERY.json", return316_delivery_path.read_bytes())

    request_text = f"""# Director request: Time Stop / TF192-B01 only (Packet318)

Please adjudicate only `time-stop` / `TF192-B01` at current authority **823 applied / 25 pending / 0 accepted-unapplied** (547 complete standalone procedures / 173 scoped interfaces). The other Time/Fate identities are unchanged context only. Do not re-review or accept Timeless Form, and do not alter any other hold.

The packet binds the current index and catalog, queue317/handoff317/pending audit317, Return316 acceptance and application receipts, a full old/current size+SHA-256 comparison for Packet282's 140-source inventory, the one changed file supplied, the exact latest Time Stop procedure and TF192-B01 record, all nine relevant questions plus TIME129-ADD01, four Time Stop obligations, and all 14 preserved Time Stop cases with canonical record hashes. It includes current Time Stop and Timeless Form native rows, the native source files, Return308's held Timeless Form procedure/lifecycle and DF218-B03 evidence.

The only native Time Stop-immunity wording located is Timeless Form's “Become immune to aging, time stop, haste/slow for 1 minute.” Current index and catalog still show Timeless Form as pending with a null procedure pointer / null operational procedure; no accepted independent immunity source or legally acquired immune actor was found. This packet therefore makes no positive-witness claim and does not turn the proposed local Time Stop/Timeless Form interaction into accepted authority.

Preserve all three Time Stop modes: Wizard/Illusion Action and Druid/Mage Transmutation Action; Cleric/Universal Reaction. If current evidence does not close TF192-B01, return the exact remaining witness and a sealed decision. Because the only located immunity route is the still-pending Timeless Form, I explicitly request the joint-interface authoring contract described in `evidence/timeless_form/blocker_dependency.json`, if that is required to resolve the circular dependency. Keep both identities pending unless the decision identifies exact accepted evidence. Do not apply unless you expressly accept `time-stop` alone.

No runtime, canon, implementation, balance, playtest, release, or global interface approval is requested. Preserve the five separate holds and the remaining 24-priority order; state acceptedIds, appliedIds, heldIds, current authority, remaining closure count, and next identity.
"""
    put(members, "REQUEST.md", request_text.encode("utf-8"))

    # A small top-level context file supplies exact scope and baseline bindings.
    context = {
        "id": "TIME-STOP-PACKET-318",
        "recordedAtUtc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "scopeIds": ["time-stop"],
        "blockerIds": ["TF192-B01"],
        "unchangedContextIds": ["fate-rewrite", "collapse-timeline", "eternal-prophecy"],
        "authority": {"reviewedApplied": 823, "pending": 25, "acceptedUnapplied": 0, "completeStandaloneProcedures": 547, "scopedInterfaces": 173},
        "pendingAuditHistoricalQueueProvenance": pending317.get("sourceQueue"),
        "currentQueueBinding": binding(queue317_path),
        "sourceBaseline": {"packet": "Packet282", **baseline_archive_binding, "inventoryCount": len(old_bindings)},
        "sourceComparison": {"unchanged": 139, "changed": 1, "missing": 0, "changedPath": changed_paths[0]},
        "return282": return282_binding,
        "return308": return308_binding,
        "return316": return316_binding,
        "acceptedIds": [], "appliedIds": [], "heldIds": [],
        "pendingClosureTasks": 25, "firstReviewTasks": 0,
        "runtimeExecuted": False,
    }
    json_member(members, "CONTEXT.json", context)

    # ZIP write and byte-for-byte readback.
    zip_path = OUT / "DD_Rank9_TimeStop_CurrentSource_318.zip"
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=6) as zf:
        for name in sorted(members):
            zf.writestr(name, members[name])
    archive_raw = zip_path.read_bytes()
    archive_binding = binding(zip_path)

    # Validate written ZIP against the in-memory allowlist, current source state,
    # authority, case membership, and the required exact blocker/scope.
    checks: list[dict[str, Any]] = []
    def check(name: str, condition: bool, detail: Any = None) -> None:
        checks.append({"check": name, "passed": bool(condition), "detail": detail})
        if not condition:
            raise AssertionError(f"failed: {name}: {detail}")
    with zipfile.ZipFile(zip_path) as zf:
        infos = zf.infolist()
        names = [x.filename for x in infos]
        bad = []
        for name in names:
            try: safe_member(name)
            except ValueError: bad.append(name)
        check("ZIP member list is unique/safe and exactly matches prepared allowlist", len(names) == len(set(names)) and not bad and set(names) == set(members), {"members": len(names), "unsafe": bad})
        check("ZIP CRC and every embedded member SHA-256 match prepared bytes", zf.testzip() is None and all(sha(zf.read(n)) == sha(members[n]) for n in members), {"count": len(names)})
        check("Packet282 140-source comparison has 139 unchanged and only the authored index changed", len(comparison_rows) == 140 and sum(x["status"] == "UNCHANGED" for x in comparison_rows) == 139 and changed_paths == ["DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json"], {"changedPaths": changed_paths})
        check("changed current authored index is supplied byte-exactly", zf.read("evidence/source_comparison/current_changed/authored_review_index.json") == current_index_raw and binding(index_path)["sha256"] == queue317["currentIndexBinding"]["sha256"], {"bytes": len(current_index_raw), "sha256": sha(current_index_raw)})
        check("current index/catalog/queue/handoff/pending audit bind 823/25/0", queue317["currentAuthority"] == context["authority"] and pending317["authority"] == context["authority"] and len(pending317["pendingIds"]) == 25 and queue317["pendingCount"] == 25, context["authority"])
        check("Time Stop is the only adjudication target and remains pending/non-operational", context["scopeIds"] == ["time-stop"] and time_stop_index["authoredStatus"] == "pending-authored-procedure" and time_stop_row["operational"] is None, {"index": time_stop_index["authoredStatus"], "operational": time_stop_row["operational"]})
        check("Timeless Form remains a separate pending blocker, not accepted authority", timeless_form_index["authoredStatus"] == "pending-authored-procedure" and timeless_form_index["procedurePointer"] is None and timeless_form_row["operational"] is None, {"index": timeless_form_index["authoredStatus"], "procedurePointer": timeless_form_index["procedurePointer"], "operational": timeless_form_row["operational"]})
        check("exact latest Time Stop procedure binds TF192-B01 and all 14 case IDs", procedure["blockerIds"] == ["TF192-B01"] and procedure["caseIds"] == [x["id"] for x in case_manifest] and len(case_manifest) == 14, {"caseCount": len(case_manifest)})
        packet_question_ids = {q["id"] for q in selected_questions} | {x["originalQuestionUnchanged"]["id"] for x in focused_addenda}
        check("questions/obligations exactly include Q01-Q07, Q32, ADD01 and four Time Stop requirements", packet_question_ids == set(qids) and {x["id"] for x in requirements} == {"TF9-CAST", "TF9-STOP-MODES", "TF9-STOP-WORLD", "TF9-PERSISTENCE"}, {"questions": sorted(packet_question_ids), "obligations": len(requirements)})
        check("Reality Anchor acceptance/application is the only new applied identity", load_json(AUDIT / "REALITY_ANCHOR_ACCEPTANCE_316.json")["acceptedIds"] == ["reality-anchor"] and load_json(AUDIT / "REALITY_ANCHOR_APPLICATION_316.json")["appliedIds"] == ["reality-anchor"], {"accepted": ["reality-anchor"], "applied": ["reality-anchor"]})
        check("no program execution or application occurred while preparing Time Stop packet", context["runtimeExecuted"] is False and context["acceptedIds"] == [] and context["appliedIds"] == [], None)
    audit_obj = {
        "id": "TIME-STOP-PACKET-318-INDEPENDENT-AUDIT",
        "recordedAtUtc": context["recordedAtUtc"],
        "status": "PASS",
        "archive": archive_binding,
        "memberCount": len(members),
        "sourceInventoryCount": 140,
        "unchangedSourceBindings": 139,
        "changedSourceBindings": 1,
        "changedPaths": changed_paths,
        "timeStopCases": len(case_manifest),
        "scopeIds": ["time-stop"],
        "authority": context["authority"],
        "checkCount": len(checks), "passedChecks": sum(1 for c in checks if c["passed"]), "failedChecks": 0,
        "checks": checks,
        "acceptedIds": [], "appliedIds": [], "heldIds": [],
        "canonicalFilesChanged": False,
        "runtimeExecuted": False,
        "immunityFinding": "Only the pending Timeless Form native row contains explicit Time Stop immunity wording; no accepted independent immunity source was located by the focused search. No positive immune-peer witness is claimed.",
    }
    audit_path = AUDIT / "TIME_STOP_PACKET_318_INDEPENDENT_AUDIT.json"
    audit_path.write_bytes(pretty(audit_obj))
    request_path = OUT / "TIME_STOP_DIRECTOR_REQUEST_318.md"
    request_path.write_text(request_text, encoding="utf-8", newline="\n")
    delivery = {
        "id": "TIME-STOP-PACKET-318-DELIVERY",
        "status": "PREPARED_FOR_DIRECTOR_REVIEW",
        "recordedAtUtc": context["recordedAtUtc"],
        "scopeIds": ["time-stop"], "blockerIds": ["TF192-B01"],
        "authority": context["authority"],
        "archive": {"path": (OUT / zip_path.name).relative_to(ROOT).as_posix(), **archive_binding},
        "request": {"path": (OUT / request_path.name).relative_to(ROOT).as_posix(), **binding(request_path)},
        "independentAudit": {"path": audit_path.relative_to(ROOT).as_posix(), **binding(audit_path)},
        "sourceComparison": {"path": (OUT / "PACKET282_140_SOURCE_BINDING_COMPARISON.json").relative_to(ROOT).as_posix(), **binding(OUT / "PACKET282_140_SOURCE_BINDING_COMPARISON.json")} if (OUT / "PACKET282_140_SOURCE_BINDING_COMPARISON.json").exists() else None,
        "acceptedIds": [], "appliedIds": [], "heldIds": [],
        "remainingClosureTasks": 25,
        "runtimeExecuted": False,
    }
    # Provide the comparison also as a standalone attachment.
    comparison_path = OUT / "PACKET282_140_SOURCE_BINDING_COMPARISON.json"
    comparison_path.write_bytes(pretty({
        "baselineArchive": baseline_archive_binding,
        "baselineCandidate": {"member": "CURRENT_SOURCE_CONFERENCE_CANDIDATE_282.json", "bytes": len(baseline_candidate_raw), "sha256": sha(baseline_candidate_raw)},
        "inventoryCount": len(comparison_rows), "unchangedCount": 139, "changedCount": 1, "missingCount": 0,
        "changedPaths": changed_paths, "rows": comparison_rows,
        "policy": "Packet282 is the exact baseline for the unchanged files. Changed current source files are included in the Packet318 ZIP; unchanged source files remain bound by member hashes to the earlier Packet282 archive.",
    }))
    delivery["sourceComparison"] = {"path": comparison_path.relative_to(ROOT).as_posix(), **binding(comparison_path)}
    delivery_path = OUT / "DD_Rank9_TimeStop_CurrentSource_318_DELIVERY.json"
    delivery_path.write_bytes(pretty(delivery))
    prep = {
        "id": "TIME-STOP-PACKET-318-PREPARATION",
        "recordedAtUtc": context["recordedAtUtc"],
        "status": "PREPARED_FOR_DIRECTOR_REVIEW",
        "authority": context["authority"],
        "scopeIds": ["time-stop"], "blockerIds": ["TF192-B01"],
        "packet": delivery["archive"], "delivery": {"path": delivery_path.relative_to(ROOT).as_posix(), **binding(delivery_path)},
        "independentAudit": delivery["independentAudit"],
        "sourceComparison": delivery["sourceComparison"],
        "caseIds": expected_ids,
        "questions": qids,
        "obligations": ["TF9-CAST", "TF9-STOP-MODES", "TF9-STOP-WORLD", "TF9-PERSISTENCE"],
        "immunityFinding": audit_obj["immunityFinding"],
        "canonicalFilesChanged": False,
        "runtimeExecuted": False,
        "acceptedIds": [], "appliedIds": [], "heldIds": [],
    }
    (OUT / "TIME_STOP_PACKET_318_PREPARATION.json").write_bytes(pretty(prep))
    print(json.dumps({"status": "PASS", "archive": str(zip_path), "archiveBytes": len(archive_raw), "archiveSha256": sha(archive_raw), "memberCount": len(members), "audit": str(audit_path), "delivery": str(delivery_path), "caseCount": len(case_manifest), "sourceInventory": {"unchanged": 139, "changed": 1, "changedPaths": changed_paths}, "authority": context["authority"]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
