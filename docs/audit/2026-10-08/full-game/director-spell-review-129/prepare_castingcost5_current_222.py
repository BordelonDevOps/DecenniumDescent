from __future__ import annotations

import copy
import gzip
import hashlib
import json
import subprocess
import zipfile
import zlib
from datetime import datetime, timezone
from json import JSONDecodeError
from pathlib import Path, PurePosixPath

ROOT = Path(r"C:\Github\DecenniumDescent-review-push-134")
BASE = ROOT / "docs/audit/2026-10-08/full-game/director-spell-review-129"
GROUP = "rank9-casting-cost5"
IDS = ["perfect-spell", "unholy-ascendance"]
AUTH = {"reviewedApplied": 810, "pending": 38, "acceptedUnapplied": 0, "completeStandaloneProcedures": 534, "scopedInterfaces": 173}
CHAT = "https://chatgpt.com/g/g-p-67f17555a8dc8191a2b5b81e6d8adc12-dungeon-crawler/c/6adc506d-8770-83ea-b64c-0345d9b9b682"
QUEUE0 = BASE / "CURRENT_SPELL_QUEUE_221.json"
HANDOFF0 = BASE / "CURRENT_HANDOFF_221.json"
PENDING0 = BASE / "CURRENT38_PENDING_IDENTITY_AUDIT_221.json"
INDEX = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json"
CATALOG = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json"
TEMPLATE_DIR = BASE / "rank9_castingcost5_current_source_193_prepared"
OLD_PACKET = TEMPLATE_DIR / "DD_Rank9_CastingCost5_CurrentSource_193.zip"
TEMPLATE = TEMPLATE_DIR / "CURRENT_SOURCE_CONFERENCE_CANDIDATE_193.json"
HIST_CANDIDATE = ROOT / "DescentReviewChanges/ReviewBible/data/director/spell_review/rank9_casting_cost_5_source_conference_01.json"
HIST_ARCHIVE = ROOT / "docs/audit/2026-10-08/full-game/DD_Rank9_Casting_Cost_5_Source_Conference_01.zip"
RETURN194_DIR = BASE / "rank9_castingcost5_return194_received"
RETURN194_ZIP = RETURN194_DIR / "DD_Rank9_CastingCost5_Director_Return194.zip"
RETURN194_DELIVERY = RETURN194_DIR / "DD_Rank9_CastingCost5_Director_Return194_DELIVERY.json"
RETURN194_RECEIPT = BASE / "RANK9_CASTINGCOST5_RETURN194_RECEIPT.json"
RETURN194_AUDIT = BASE / "RANK9_CASTINGCOST5_RETURN194_INDEPENDENT_AUDIT.json"
RETURN194_DECISION = BASE / "RANK9_CASTINGCOST5_DIRECTOR_DECISION_194.json"
RETURN194_ACCEPTANCE = BASE / "RANK9_CASTINGCOST5_EXACT_ACCEPTANCE_194.json"
RETURN194_APPLICATION = BASE / "RANK9_CASTINGCOST5_APPLICATION_194.json"
RETURN194_VALIDATION = BASE / "RANK9_CASTINGCOST5_APPLICATION_VALIDATION_194.json"
RETURN194_INDEX_OPS = BASE / "RANK9_CASTINGCOST5_INDEX_OPERATIONS_194.json"
PREP193 = BASE / "RANK9_CASTINGCOST5_SOURCE_PREPARATION_193.json"
PACKET193 = BASE / "RANK9_CASTINGCOST5_PACKET_193.json"
TIMEFATE_RECEIPT221 = BASE / "RANK9_TIMEFATE6_RETURN221_RECEIPT.json"
TIMEFATE_AUDIT221 = BASE / "RANK9_TIMEFATE6_RETURN221_INDEPENDENT_AUDIT.json"
TIMEFATE_ZIP221 = BASE / "rank9_timefate6_return221_received/DD_Rank9_TimeFate4_Director_Return221_HELD.zip"
TIMEFATE_DELIVERY221 = BASE / "rank9_timefate6_return221_received/DD_Rank9_TimeFate4_Director_Return221_HELD_DELIVERY.json"
OUT = BASE / "rank9_castingcost5_current_source_222_prepared_retry1"


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def crc(raw: bytes) -> str:
    return f"{zlib.crc32(raw) & 0xffffffff:08x}"


def readj(path: Path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def jb(value) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8")


def bind(path: Path, raw: bytes | None = None):
    data = path.read_bytes() if raw is None else raw
    return {"path": path.relative_to(ROOT).as_posix(), "bytes": len(data), "sha256": sha(data), "crc32": crc(data)}


def safe_member(name: str) -> bool:
    path = PurePosixPath(name)
    return bool(name) and "\\" not in name and not path.is_absolute() and all(part not in ("", ".", "..") and not part.startswith(".") for part in path.parts)


def add_file(files: dict[str, bytes], name: str, raw: bytes):
    assert safe_member(name), name
    assert name not in files, f"Duplicate member: {name}"
    files[name] = raw


def iter_json_array(zf: zipfile.ZipFile, member: str, field: str):
    """Yield objects from one large top-level JSON array without loading its whole casebook."""
    decoder = json.JSONDecoder()
    with zf.open(member) as stream:
        buffer = ""
        position = 0
        marker = f'"{field}"'
        while marker not in buffer:
            chunk = stream.read(1 << 20)
            if not chunk:
                raise ValueError(f"Array key not found: {field}")
            buffer += chunk.decode("utf-8")
        array_start = buffer.find("[", buffer.find(marker))
        while array_start < 0:
            chunk = stream.read(1 << 20)
            if not chunk:
                raise ValueError(f"Array start not found: {field}")
            buffer += chunk.decode("utf-8")
            array_start = buffer.find("[", buffer.find(marker))
        position = array_start + 1
        while True:
            while position < len(buffer) and (buffer[position].isspace() or buffer[position] == ","):
                position += 1
            if position < len(buffer) and buffer[position] == "]":
                return
            try:
                value, end = decoder.raw_decode(buffer, position)
            except JSONDecodeError:
                chunk = stream.read(1 << 20)
                if not chunk:
                    raise
                # Preserve all bytes already read. Individual case records can
                # exceed one MiB; replacing the unread suffix would splice the
                # middle of a large JSON object into a false sibling array.
                buffer += chunk.decode("utf-8")
                continue
            yield value
            buffer = buffer[end:]
            position = 0


def main():
    assert not OUT.exists(), f"Output already exists: {OUT}"
    required = [QUEUE0, HANDOFF0, PENDING0, INDEX, CATALOG, OLD_PACKET, TEMPLATE, HIST_CANDIDATE, HIST_ARCHIVE,
                RETURN194_ZIP, RETURN194_DELIVERY, RETURN194_RECEIPT, RETURN194_AUDIT, RETURN194_DECISION,
                RETURN194_ACCEPTANCE, RETURN194_APPLICATION, RETURN194_VALIDATION, RETURN194_INDEX_OPS,
                PREP193, PACKET193, TIMEFATE_RECEIPT221, TIMEFATE_AUDIT221, TIMEFATE_ZIP221, TIMEFATE_DELIVERY221]
    for path in required:
        assert path.exists(), f"Required source missing: {path}"

    now = datetime.now(timezone.utc).isoformat()
    q0, h0, p0 = readj(QUEUE0), readj(HANDOFF0), readj(PENDING0)
    index, catalog = readj(INDEX), readj(CATALOG)
    tf_receipt, tf_audit = readj(TIMEFATE_RECEIPT221), readj(TIMEFATE_AUDIT221)
    assert q0["currentAuthority"] == h0["currentAuthority"] == p0["authority"] == AUTH
    assert p0["pendingCount"] == 38 and set(IDS) <= set(p0["pendingIds"])
    # Queue 221 still names the just-completed Time/Fate packet. The sealed
    # Return221 receipt is the evidence that lets this preparation advance to
    # the next target group without rewriting the prior checkpoint.
    assert q0["nextGroup"] == h0["nextGroup"] == "rank9-time-fate6"
    assert h0["nextStep"]["group"] == "rank9-time-fate6"
    assert h0["nextStep"]["status"] == "CURRENT_SOURCE_PACKET_PREPARED_UNSENT"
    assert tf_receipt["acceptedIds"] == [] and tf_receipt["appliedIds"] == []
    assert tf_audit["checksFailed"] == 0 and tf_audit["status"].startswith("PASS_PACKAGE_BINDING_AND_SCOPE")
    tf_return_binding = tf_receipt["directorReturn"]
    assert tf_return_binding["sha256"] == readj(TIMEFATE_DELIVERY221)["archive"]["sha256"]

    target = next(group for group in q0["currentPendingGroups"] if group["group"] == GROUP)
    assert target["pendingIds"] == IDS and target["pendingCount"] == 2
    assert index["authoredCounts"] == {"reviewed": 810, "pending": 38}
    assert index["representationCounts"]["completeReviewedStandaloneProcedures"] == 534
    index_rows = {row["id"]: row for row in index["entries"]}
    catalog_rows = {row["id"]: row for row in catalog["spells"]}
    for spell_id in IDS:
        assert spell_id in p0["pendingIds"]
        assert index_rows[spell_id]["authoredStatus"] == "pending-authored-procedure"
        assert index_rows[spell_id]["sourceStatus"] == "blocked-pending-operational-review"
        assert catalog_rows[spell_id].get("operational") is None

    old_candidate = readj(TEMPLATE)
    historical_candidate = readj(HIST_CANDIDATE)
    old_bindings = old_candidate["sourceBindings"]
    assert len(old_bindings) == len(historical_candidate["sourceBindings"]) == 117
    prior_receipt = readj(RETURN194_RECEIPT)
    assert prior_receipt["unacceptedIds"] == IDS
    assert prior_receipt["acceptedIds"] == ["ritual-mastery", "world-rewrite", "resonance-perfection"]
    expected_prior_blockers = {"perfect-spell": ["CC194-B01"], "unholy-ascendance": ["CC194-B04"]}
    assert {sid: prior_receipt["blockers"][sid]["blockerIds"] for sid in IDS} == expected_prior_blockers

    hist_archive_raw = HIST_ARCHIVE.read_bytes()
    with zipfile.ZipFile(HIST_ARCHIVE) as historical_zip:
        assert historical_zip.testzip() is None
        for binding in historical_candidate["sourceBindings"]:
            raw = historical_zip.read("sources/" + binding["path"])
            assert len(raw) == binding["bytes"] and sha(raw) == binding["sha256"]

    historical_source_members = {}
    with zipfile.ZipFile(OLD_PACKET) as old_zip:
        assert old_zip.testzip() is None and len(old_zip.namelist()) == 144 and len(set(old_zip.namelist())) == 144
        for binding in old_bindings:
            raw = old_zip.read("sources_current/" + binding["path"])
            assert len(raw) == binding["bytes"] and sha(raw) == binding["sha256"]
            historical_source_members[binding["path"]] = raw

    refreshed, current_sources, changed = [], {}, []
    for binding in old_bindings:
        path = binding["path"]
        assert safe_member(path)
        raw = (ROOT / Path(path)).read_bytes()
        refreshed.append({"path": path, "bytes": len(raw), "sha256": sha(raw)})
        current_sources["sources_current/" + path] = raw
        if raw != historical_source_members[path]:
            changed.append({"path": path, "previousPacketSha256": sha(historical_source_members[path]), "currentSha256": sha(raw), "currentBytes": len(raw)})
    assert len(refreshed) == 117

    source_commit = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    branch = subprocess.check_output(["git", "branch", "--show-current"], cwd=ROOT, text=True).strip()
    assert branch == "main"
    source_snapshot = {"kind": "working-tree", "headCommit": source_commit, "branch": branch, "indexBinding": bind(INDEX), "catalogBinding": bind(CATALOG)}

    current = copy.deepcopy(old_candidate)
    current["historicalSourceBindings"] = copy.deepcopy(old_candidate.get("historicalSourceBindings", old_bindings))
    current["sourceBindings"] = refreshed
    current["id"] = "RANK9-CASTING-COST5-CURRENT-SOURCE-CONTEXT-222"
    current["recordedAtUtc"] = now
    current["status"] = "CURRENT_SOURCE_BINDINGS_REFRESHED_FOR_810_REVIEWED_38_PENDING_AUTHORITY"
    current["currentAuthority"] = AUTH
    current["currentPendingGroup"] = {"group": GROUP, "spellIds": IDS, "count": len(IDS)}
    current["currentIndexBinding"] = bind(INDEX)
    current["currentCatalogBinding"] = bind(CATALOG)
    current["currentPendingAuditInputBinding"] = bind(PENDING0)
    current["currentQueueInputBinding"] = bind(QUEUE0)
    current["currentHandoffInputBinding"] = bind(HANDOFF0)
    current["currentTimeFate221ReceiptBinding"] = bind(TIMEFATE_RECEIPT221)
    current["currentTimeFate221IndependentAuditBinding"] = bind(TIMEFATE_AUDIT221)
    current["currentTimeFate221ReturnArchiveBinding"] = bind(TIMEFATE_ZIP221)
    current["sourceSnapshot"] = source_snapshot
    current["currentSourceCommit"] = source_commit
    current["currentBranch"] = branch
    current["historicalCandidateBinding"] = bind(TEMPLATE)
    current["queueCandidateBinding"] = copy.deepcopy(target["candidate"])
    current["historicalSourceArchiveBinding"] = bind(HIST_ARCHIVE, hist_archive_raw)
    current["sourceBindingRefresh"] = {"sourceFiles": len(refreshed), "changedSinceCastingCostSourcePacket193": changed, "allSourceBindingsRefreshedFromWorkingTree": True}
    current["countsUnchanged"] = {"reviewed": 810, "pending": 38}
    for record in current.get("records", []):
        sid = record.get("spellId")
        if sid in index_rows:
            if "currentIndexEntry" in record:
                record["historicalIndexEntry"] = copy.deepcopy(record["currentIndexEntry"])
                record["currentIndexEntry"] = copy.deepcopy(index_rows[sid])
            else:
                record["currentIndexEntry"] = copy.deepcopy(index_rows[sid])
    candidate_raw = jb(current)

    selected_return_members = [
        "DIRECTOR_DECISION.json", "EVIDENCE_MANIFEST.json", "HOLD_REGISTER.json",
        "INDEPENDENT_SEMANTIC_FAILURE_CHECK.json", "MEMBER_MANIFEST.json", "PROCEDURES.json",
        "QUESTION_DISPOSITIONS.json", "SOURCE_VERIFICATION.json", "STANDALONE_PROCEDURES.md", "VALIDATION.json",
        "procedures/perfect-spell.json", "procedures/unholy-ascendance.json",
    ]
    with zipfile.ZipFile(RETURN194_ZIP) as return_zip:
        assert return_zip.testzip() is None
        selected_cases = []
        for case in iter_json_array(return_zip, "CASEBOOK.json", "cases"):
            if case.get("spellId") in IDS:
                selected_cases.append(case)
        assert selected_cases and {case["spellId"] for case in selected_cases} == set(IDS)
        casebook = {"id": "CASTINGCOST5-RETURN194-PENDING-CASES", "runtimeExecuted": False,
                    "scope": "Only perfect-spell and unholy-ascendance remain pending at authority 810/38/0.", "cases": selected_cases}
        compact_cases = gzip.compress(jb(casebook), compresslevel=6, mtime=0)
        selected_contents = {name: return_zip.read(name) for name in selected_return_members}

    files: dict[str, bytes] = {}
    with zipfile.ZipFile(OLD_PACKET) as old_zip:
        for name in old_zip.namelist():
            if name.startswith("sources_current/") or name == "MANIFEST.json":
                continue
            add_file(files, "historical_packet_193/" + name, old_zip.read(name))
    for name, raw in current_sources.items():
        add_file(files, name, raw)
    for name, raw in selected_contents.items():
        add_file(files, "director_history/castingcost5_return194/" + name, raw)
    add_file(files, "director_history/castingcost5_return194_pending_cases.json.gz", compact_cases)

    history_files = [RETURN194_RECEIPT, RETURN194_AUDIT, RETURN194_DECISION, RETURN194_ACCEPTANCE, RETURN194_APPLICATION,
                     RETURN194_VALIDATION, RETURN194_INDEX_OPS, PREP193, PACKET193, RETURN194_DELIVERY,
                     TIMEFATE_RECEIPT221, TIMEFATE_AUDIT221, TIMEFATE_ZIP221, TIMEFATE_DELIVERY221]
    for path in history_files:
        add_file(files, "authority_history/" + path.relative_to(ROOT).as_posix(), path.read_bytes())

    authority_files = {
        "authority_current/authored_review_index.json": INDEX.read_bytes(),
        "authority_current/catalog.json": CATALOG.read_bytes(),
        "authority_current/CURRENT_SPELL_QUEUE_221_INPUT.json": QUEUE0.read_bytes(),
        "authority_current/CURRENT_HANDOFF_221_INPUT.json": HANDOFF0.read_bytes(),
        "authority_current/CURRENT38_PENDING_IDENTITY_AUDIT_221_INPUT.json": PENDING0.read_bytes(),
    }
    for name, raw in authority_files.items():
        add_file(files, name, raw)

    request = (
        "GPT director — continue the ordinary-spell review at current authority 810 reviewed/applied / 38 pending / 0 accepted-unapplied, "
        "with 534 complete standalone procedures and 173 scoped interfaces. Review only the two currently pending Rank9 Casting/Cost5 identities: "
        "perfect-spell and unholy-ascendance. Do not re-review ritual-mastery, world-rewrite, resonance-perfection, the two accepted Time/Fate6 spells, feats, or any other spell.\n\n"
        f"Current source snapshot: branch {branch}, HEAD {source_commit}; current index/catalog, queue, handoff, pending audit, and the independently audited Return221 Time/Fate6 ruling are included. "
        "Return221 held all four Time/Fate6 targets; the audit verified the return package and its 62 cases/628 events, with no decisions applied.\n\n"
        "Reassess only the exact prior Casting/Cost5 blockers from Return194 against refreshed current sources. Carry CC194-B01 for perfect-spell unless a source-faithful local conflict rule supports a positive funded/waived Harmonic Bulwark invocation while preserving honest leaf credit; root26 is not leaf payment. "
        "Carry CC194-B04 for unholy-ascendance unless the new caster-Undead form receives a source-grounded zero-HP/Null recipient contract and complete type-healing/death/other-form adverse traces. Preserve all listed CC194-H holds, accepted interfaces, actual damage versus non-damage, costs, original HP/wounds/equipment and Hunt holds; do not import monster/global-Null rules.\n\n"
        "Return explicit accepted/held decisions for only these two IDs, exact blocker and conditional qualification IDs, complete source-faithful procedures and reversible before/after traces, exact costs and resource/custody histories, and a verifiable compact ZIP plus delivery manifest bound to this packet. Keep every acceptance unapplied; do not edit canonical files or execute supplied programs. Preserve runtime, implementation, human-play, balance, cosmology, domain-closure, completion and release gates. I will audit and apply only exact acceptances."
    )
    context = {
        "id": "RANK9-CASTING-COST5-CURRENT-CONTEXT-222", "recordedAtUtc": now, "sourceAuthority": AUTH,
        "sourceSnapshot": source_snapshot, "group": GROUP, "pendingIds": IDS,
        "priorTimeFateReturn221Receipt": bind(TIMEFATE_RECEIPT221),
        "priorTimeFateReturn221Audit": bind(TIMEFATE_AUDIT221),
        "priorTimeFateArchive": bind(TIMEFATE_ZIP221), "priorTimeFateArchiveDelivered": True,
        "priorCastingCostReturn194Receipt": bind(RETURN194_RECEIPT), "priorCastingCostReturn194Audit": bind(RETURN194_AUDIT),
        "currentIndex": bind(INDEX), "currentCatalog": bind(CATALOG), "currentPendingInput": bind(PENDING0),
        "currentQueueInput": bind(QUEUE0), "currentHandoffInput": bind(HANDOFF0),
        "historicalCandidate": bind(TEMPLATE), "historicalSourceArchive": bind(HIST_ARCHIVE, hist_archive_raw),
    }
    context_raw = jb(context)
    request_raw = (request + "\n").encode("utf-8")
    add_file(files, "CURRENT_CONTEXT_222.json", context_raw)
    add_file(files, "CURRENT_SOURCE_CONFERENCE_CANDIDATE_222.json", candidate_raw)
    add_file(files, "REQUEST_222.txt", request_raw)

    rows = [{"path": name, "bytes": len(raw), "sha256": sha(raw), "crc32": crc(raw)} for name, raw in sorted(files.items())]
    manifest = {"id": "RANK9-CASTING-COST5-CURRENT-SOURCE-PACKET-MANIFEST-222", "sourceSnapshot": source_snapshot,
                "sourceAuthority": AUTH, "group": GROUP, "pendingIds": IDS, "payloadMemberCount": len(rows), "members": rows}
    manifest_raw = jb(manifest)
    OUT.mkdir(parents=True)
    packet_path = OUT / "DD_Rank9_CastingCost5_CurrentSource_222.zip"
    with zipfile.ZipFile(packet_path, "w", zipfile.ZIP_DEFLATED, compresslevel=6) as packet:
        for name, raw in sorted(files.items()):
            packet.writestr(name, raw, compress_type=zipfile.ZIP_DEFLATED, compresslevel=6)
        packet.writestr("MANIFEST.json", manifest_raw, compress_type=zipfile.ZIP_DEFLATED, compresslevel=6)
    with zipfile.ZipFile(packet_path) as packet:
        assert packet.testzip() is None and len(packet.namelist()) == len(rows) + 1 and len(set(packet.namelist())) == len(rows) + 1
        for row in rows:
            raw = packet.read(row["path"])
            assert len(raw) == row["bytes"] and sha(raw) == row["sha256"] and crc(raw) == row["crc32"]
        assert json.loads(packet.read("MANIFEST.json"))["members"] == rows
        assert json.loads(packet.read("CURRENT_SOURCE_CONFERENCE_CANDIDATE_222.json"))["sourceBindings"] == refreshed
        for binding in refreshed:
            assert packet.read("sources_current/" + binding["path"]) == (ROOT / Path(binding["path"])).read_bytes()

    packet_binding = bind(packet_path)
    candidate_path = OUT / "CURRENT_SOURCE_CONFERENCE_CANDIDATE_222.json"
    context_path = OUT / "CURRENT_CONTEXT_222.json"
    request_path = OUT / "REQUEST_222.txt"
    candidate_path.write_bytes(candidate_raw)
    context_path.write_bytes(context_raw)
    request_path.write_bytes(request_raw)
    delivery_path = OUT / "DD_Rank9_CastingCost5_CurrentSource_222_DELIVERY.json"
    delivery = {"id": "RANK9-CASTING-COST5-CURRENT-SOURCE-DELIVERY-222", "status": "PREPARED_UNSENT", "archive": packet_binding,
                "memberCount": len(rows) + 1, "payloadMemberCount": len(rows), "sourceSnapshot": source_snapshot,
                "sourceAuthority": AUTH, "group": GROUP, "pendingIds": IDS,
                "candidate": bind(candidate_path, candidate_raw), "historicalSourceArchive": bind(HIST_ARCHIVE, hist_archive_raw),
                "sourceFilesRefreshed": len(refreshed), "sourceFilesChangedSinceCastingCostSourcePacket193": changed,
                "return194PendingCaseCount": len(selected_cases), "accepted": False, "applied": False, "conversation": CHAT}
    delivery_path.write_bytes(jb(delivery))
    delivery_binding = bind(delivery_path)

    prep_path = BASE / "RANK9_CASTINGCOST5_SOURCE_PREPARATION_222.json"
    prep_checks = [
        "Authority 810/38/0 and 534/173 representation counts agree across the current index, queue, handoff and pending audit.",
        "Exactly perfect-spell and unholy-ascendance remain pending; the other three Casting/Cost5 identities remain out of scope and accepted.",
        "Time/Fate Return221 package and its independent hash/scope audit are preserved without application.",
        f"Historical Casting/Cost5 source packet and conference archive pass integrity and all {len(refreshed)} historical source bindings.",
        f"All {len(refreshed)} Casting/Cost5 source bindings are refreshed from current working-tree bytes.",
        "Current catalog/index entries for all five historical Casting/Cost5 identities are current and only the two targets are pending.",
        f"Return194 decision, hold register, semantic failure check, procedures and {len(selected_cases)} cases for the two pending identities are included.",
        "Request limits review to the two pending identities and preserves accepted interfaces and all unrelated gates.",
        "Packet ZIP, unique safe member paths, and every embedded member SHA-256/CRC32 reconcile.",
    ]
    prep = {"id": "RANK9-CASTING-COST5-SOURCE-PREPARATION-222", "recordedAtUtc": now, "status": "CURRENT_SOURCE_PACKET_PREPARED_UNSENT",
            "sourceAuthority": AUTH, "sourceSnapshot": source_snapshot, "group": GROUP, "pendingIds": IDS,
            "historicalCandidate": bind(HIST_CANDIDATE), "historicalArchive": bind(HIST_ARCHIVE, hist_archive_raw),
            "previousReturn194": bind(RETURN194_RECEIPT), "previousReturn221TimeFate": bind(TIMEFATE_RECEIPT221),
            "refreshedSourceFiles": len(refreshed), "changedSincePacket193": changed, "return194PendingCasesIncluded": len(selected_cases),
            "candidate": bind(candidate_path, candidate_raw), "packet": packet_binding, "deliveryManifest": delivery_binding,
            "payloadMemberCount": len(rows), "checksPassed": len(prep_checks), "checksFailed": 0,
            "checks": [{"check": label, "passed": True} for label in prep_checks], "canonicalChangesBeforePreparation": False,
            "accepted": False, "applied": False, "request": request}
    prep_path.write_bytes(jb(prep))
    prep_binding = bind(prep_path)
    packet_record_path = BASE / "RANK9_CASTINGCOST5_PACKET_222.json"
    packet_record = {"id": "RANK9-CASTING-COST5-PACKET-222", "status": "PREPARED_UNSENT", "sourceAuthority": AUTH,
                     "group": GROUP, "pendingIds": IDS, "packet": packet_binding, "deliveryManifest": delivery_binding,
                     "preparation": prep_binding, "candidate": bind(candidate_path, candidate_raw), "conversation": CHAT,
                     "checksPassed": len(prep_checks), "checksFailed": 0}
    packet_record_path.write_bytes(jb(packet_record))
    packet_record_binding = bind(packet_record_path)

    tf_capture_ref = bind(TIMEFATE_RECEIPT221)
    pending_after = copy.deepcopy(p0)
    pending_after.update({"id": "CURRENT38-PENDING-IDENTITY-AUDIT-222", "recordedAtUtc": now,
                          "status": "PASSED_EXACT_CURRENT_INDEX_PENDING_SET_WITH_CASTING_COST5_PACKET_222",
                          "lastDirectorReturn": tf_capture_ref,
                          "preparedNextGroup": {"group": GROUP, "pendingIds": IDS, "packet": packet_binding, "deliveryManifest": delivery_binding}})
    pending_path = BASE / "CURRENT38_PENDING_IDENTITY_AUDIT_222.json"
    pending_path.write_bytes(jb(pending_after))
    pending_binding = bind(pending_path)

    last_batch = {"return": 221, "group": "rank9-time-fate6", "ids": ["time-stop", "fate-rewrite", "collapse-timeline", "eternal-prophecy"],
                  "acceptedIds": [], "appliedIds": [], "heldIds": ["time-stop", "fate-rewrite", "collapse-timeline", "eternal-prophecy"],
                  "blockers": {"time-stop": ["TF192-B01"], "fate-rewrite": ["TF192-B04"], "collapse-timeline": ["TF192-B05"], "eternal-prophecy": ["TF192-B02"]},
                   "conditionalQualifications": {"shared": tf_receipt["commonQualifications"]},
                  "authorityAfter": AUTH, "auditStatus": "SEALED_RETURN_PACKAGE_INDEPENDENTLY_AUDITED; SEMANTIC_HOLDS_RETAINED",
                  "decisionCapture": tf_capture_ref, "directorReturn": tf_receipt["directorReturn"], "independentAudit": bind(TIMEFATE_AUDIT221)}

    qafter = copy.deepcopy(q0)
    casting_group = next(group for group in qafter["currentPendingGroups"] if group["group"] == GROUP)
    casting_group.update({"status": "CURRENT_SOURCE_PACKET_PREPARED_UNSENT_810_38", "candidate": bind(candidate_path, candidate_raw),
                          "preparedPacket": packet_binding, "deliveryManifest": delivery_binding, "packetRecord": packet_record_binding,
                          "preparation": prep_binding, "freshPacketRequiredForCurrentAuthority": False})
    time_group = next(group for group in qafter["currentPendingGroups"] if group["group"] == "rank9-time-fate6")
    time_group.update({"status": "RETURN221_ALL_HELD_ARCHIVE_AUDITED", "freshPacketRequiredForCurrentAuthority": True,
                       "directorReturn": tf_receipt["directorReturn"], "directorDelivery": bind(TIMEFATE_DELIVERY221),
                       "independentAudit": bind(TIMEFATE_AUDIT221), "acceptedIds": [], "appliedIds": []})
    qafter.update({"id": "SPELL-REVIEW-QUEUE-222", "recordedAtUtc": now, "supersedesQueue": bind(QUEUE0),
                   "currentReturnAudit": {"status": "SEALED_RETURN_ARCHIVE_AND_SIDECAR_INDEPENDENTLY_VERIFIED; FOUR_HELD; REPLAY_CLAIMS_HASH/COUNT_CHECKED",
                                          "receipt": tf_capture_ref, "archive": bind(TIMEFATE_ZIP221), "deliveryManifest": bind(TIMEFATE_DELIVERY221),
                                          "independentAudit": bind(TIMEFATE_AUDIT221), "independentSemanticReplay": False},
                   "currentReturnArchive": bind(TIMEFATE_ZIP221), "currentReturnDelivery": bind(TIMEFATE_DELIVERY221),
                   "currentReturnDecision": tf_capture_ref, "lastReviewedBatch": last_batch, "nextGroup": GROUP,
                   "next": {"group": GROUP, "pendingIds": IDS, "pendingCount": len(IDS), "status": "CURRENT_SOURCE_PACKET_PREPARED_UNSENT",
                            "packet": packet_binding, "deliveryManifest": delivery_binding, "packetRecord": packet_record_binding,
                            "preparation": prep_binding, "candidate": bind(candidate_path, candidate_raw)},
                   "nextPreparedRequest": {"group": GROUP, "pendingIds": IDS, "request": bind(request_path, request_raw), "status": "PREPARED_UNSENT"},
                   "currentPreparation": prep_binding, "currentPacket": packet_binding, "currentDeliveryManifest": delivery_binding,
                   "currentPacketDelivery": delivery_binding, "pendingIdentityAudit": pending_binding, "parentQueue": bind(QUEUE0),
                   "packetStatus": "RANK9_CASTINGCOST5_CURRENT_SOURCE_PACKET_222_PREPARED_UNSENT_810_38", "pendingCount": 38, "githubChanges": False})
    queue_path = BASE / "CURRENT_SPELL_QUEUE_222.json"
    queue_path.write_bytes(jb(qafter))
    queue_binding = bind(queue_path)

    hafter = copy.deepcopy(h0)
    preserved = copy.deepcopy(hafter.get("preservedOtherHolds", []))
    preserved.append({"ids": last_batch["ids"], "blockerIds": last_batch["blockers"],
                      "qualificationIds": last_batch["conditionalQualifications"]["shared"],
                      "decisionCapture": tf_capture_ref, "independentAudit": bind(TIMEFATE_AUDIT221), "traceReplayVerified": False})
    hafter.update({"id": "CURRENT-HANDOFF-222", "recordedAtUtc": now,
                   "status": "RANK9_CASTINGCOST5_CURRENT_SOURCE_PACKET_PREPARED_UNSENT_810_38", "currentAuthority": AUTH,
                   "latestBatch": last_batch, "preservedOtherHolds": preserved, "nextGroup": GROUP,
                   "nextStep": {"group": GROUP, "pendingIds": IDS, "pendingCount": len(IDS), "status": "CURRENT_SOURCE_PACKET_PREPARED_UNSENT",
                                "packet": packet_binding, "deliveryManifest": delivery_binding},
                   "pendingIdentityAudit": pending_binding, "queue": queue_binding,
                   "currentPreparation": prep_binding, "currentPacket": packet_binding, "currentPacketDelivery": delivery_binding,
                   "appliedThisStep": False, "githubChanges": False, "runtimeSelectionEnabled": False,
                   "canonicalRuntimeApplicationPerformed": False})
    handoff_path = BASE / "CURRENT_HANDOFF_222.json"
    handoff_path.write_bytes(jb(hafter))
    handoff_binding = bind(handoff_path)

    snapshot_path = BASE / "CURRENT_SPELL_REVIEW_SNAPSHOT_222.md"
    snapshot_path.write_text(
        "# Current ordinary spell-review checkpoint 222\n\n"
        "Authority remains **810 reviewed/applied / 38 pending / 0 accepted-unapplied**, with 534 complete standalone procedures and 173 scoped interfaces. "
        "Return221 held all four Time/Fate6 spells; its ZIP/sidecar, 23 members, and current source binding independently verified. GPT reported 62 cases/628 events and replay checks; this local package audit checked their hashes/counts without re-running GPT's simulation. "
        "The fresh next packet covers only the two pending Casting/Cost5 identities: perfect-spell and unholy-ascendance.\n\n"
        "See [handoff](CURRENT_HANDOFF_222.json), [queue](CURRENT_SPELL_QUEUE_222.json), [pending audit](CURRENT38_PENDING_IDENTITY_AUDIT_222.json), "
        "[Time/Fate Return221 receipt](RANK9_TIMEFATE6_RETURN221_RECEIPT.json), [packet record](RANK9_CASTINGCOST5_PACKET_222.json), "
        "and [source packet](rank9_castingcost5_current_source_222_prepared/DD_Rank9_CastingCost5_CurrentSource_222.zip).\n",
        encoding="utf-8", newline="\n")

    print(json.dumps({"status": "PREPARED_UNSENT", "sourceCommit": source_commit, "sourceBranch": branch, "authority": AUTH,
                      "group": GROUP, "pendingIds": IDS, "refreshedSources": len(refreshed), "changedSincePacket193": changed,
                      "return194PendingCasesIncluded": len(selected_cases), "payloadMembers": len(rows), "packet": packet_binding,
                      "deliveryManifest": delivery_binding, "checksPassed": len(prep_checks), "checksFailed": 0,
                      "queue": queue_binding, "handoff": handoff_binding,
                      "return221AuditChecks": tf_audit["checksPassed"]}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
