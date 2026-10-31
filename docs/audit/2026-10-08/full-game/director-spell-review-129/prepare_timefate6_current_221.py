from __future__ import annotations

import copy
import gzip
import hashlib
import json
import subprocess
import zipfile
import zlib
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath

ROOT = Path(r"C:\Github\DecenniumDescent-review-push-134")
BASE = ROOT / "docs/audit/2026-10-08/full-game/director-spell-review-129"
GROUP = "rank9-time-fate6"
IDS = ["time-stop", "fate-rewrite", "collapse-timeline", "eternal-prophecy"]
AUTH = {
    "reviewedApplied": 810,
    "pending": 38,
    "acceptedUnapplied": 0,
    "completeStandaloneProcedures": 534,
    "scopedInterfaces": 173,
}
CHAT = "https://chatgpt.com/g/g-p-67f17555a8dc8191a2b5b81e6d8adc12-dungeon-crawler/c/6adc506d-8770-83ea-b64c-0345d9b9b682"
QUEUE0 = BASE / "CURRENT_SPELL_QUEUE_220.json"
HANDOFF0 = BASE / "CURRENT_HANDOFF_220.json"
PENDING0 = BASE / "CURRENT38_PENDING_IDENTITY_AUDIT_220.json"
CAPTURE220 = BASE / "RANK9_AGENCYCONTROL9_RETURN220_INLINE_CAPTURE.json"
INDEX = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json"
CATALOG = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json"
TEMPLATE_DIR = BASE / "rank9_timefate6_current_source_191_prepared"
OLD_PACKET = TEMPLATE_DIR / "DD_Rank9_TimeFate6_CurrentSource_191.zip"
TEMPLATE = TEMPLATE_DIR / "CURRENT_SOURCE_CONFERENCE_CANDIDATE_191.json"
HIST_CANDIDATE = ROOT / "DescentReviewChanges/ReviewBible/data/director/spell_review/rank9_time_fate_6_source_conference_01.json"
HIST_ARCHIVE = ROOT / "docs/audit/2026-10-08/full-game/DD_Rank9_Time_Fate_6_Source_Conference_01.zip"
RETURN192_DIR = BASE / "rank9_timefate6_return192_received"
RETURN192_ZIP = RETURN192_DIR / "DD_Rank9_TimeFate6_Director_Return192.zip"
RETURN192_DELIVERY = RETURN192_DIR / "DD_Rank9_TimeFate6_Director_Return192_DELIVERY.json"
RETURN192_RECEIPT = BASE / "RANK9_TIMEFATE6_RETURN192_RECEIPT.json"
RETURN192_AUDIT = BASE / "RANK9_TIMEFATE6_RETURN192_INDEPENDENT_AUDIT.json"
RETURN192_DECISION = BASE / "RANK9_TIMEFATE6_DIRECTOR_DECISION_192.json"
RETURN192_ACCEPTANCE = BASE / "RANK9_TIMEFATE6_EXACT_ACCEPTANCE_192.json"
RETURN192_APPLICATION = BASE / "RANK9_TIMEFATE6_APPLICATION_192.json"
RETURN192_VALIDATION = BASE / "RANK9_TIMEFATE6_APPLICATION_VALIDATION_192.json"
RETURN192_INDEX_OPS = BASE / "RANK9_TIMEFATE6_INDEX_OPERATIONS_192.json"
PREP191 = BASE / "RANK9_TIMEFATE6_SOURCE_PREPARATION_191.json"
PACKET191 = BASE / "RANK9_TIMEFATE6_PACKET_191.json"
OUT = BASE / "rank9_timefate6_current_source_221_prepared"


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def crc(data: bytes) -> str:
    return f"{zlib.crc32(data) & 0xffffffff:08x}"


def readj(path: Path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def jb(value) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8")


def bind(path: Path, raw: bytes | None = None):
    data = path.read_bytes() if raw is None else raw
    return {"path": path.relative_to(ROOT).as_posix(), "bytes": len(data), "sha256": sha(data), "crc32": crc(data)}


def safe_member(name: str) -> bool:
    p = PurePosixPath(name)
    return bool(name) and "\\" not in name and not p.is_absolute() and all(part not in ("", ".", "..") and not part.startswith(".") for part in p.parts)


def add_file(files: dict[str, bytes], name: str, data: bytes):
    assert safe_member(name), name
    assert name not in files, f"Duplicate packet member: {name}"
    files[name] = data


def main():
    assert not OUT.exists(), f"Output already exists: {OUT}"
    required = [
        QUEUE0, HANDOFF0, PENDING0, CAPTURE220, INDEX, CATALOG, OLD_PACKET, TEMPLATE,
        HIST_CANDIDATE, HIST_ARCHIVE, RETURN192_ZIP, RETURN192_DELIVERY, RETURN192_RECEIPT,
        RETURN192_AUDIT, RETURN192_DECISION, RETURN192_ACCEPTANCE, RETURN192_APPLICATION,
        RETURN192_VALIDATION, RETURN192_INDEX_OPS, PREP191, PACKET191,
    ]
    for path in required:
        assert path.exists(), f"Required source missing: {path}"

    now = datetime.now(timezone.utc).isoformat()
    q0, h0, p0 = readj(QUEUE0), readj(HANDOFF0), readj(PENDING0)
    capture220 = readj(CAPTURE220)
    index, catalog = readj(INDEX), readj(CATALOG)
    assert q0["currentAuthority"] == h0["currentAuthority"] == p0["authority"] == AUTH
    assert p0["pendingCount"] == 38 and set(p0["pendingIds"]) >= set(IDS)
    assert capture220["sourceAuthority"] == AUTH
    assert capture220["directorDecision"]["heldIds"] == ["absolute-domination", "puppetmaster-s-realm"]
    assert capture220["directorDecision"]["acceptedIds"] == []
    assert capture220["exportStatus"]["returnArchiveSealed"] is False
    assert capture220["preservedTraceSet"]["freshFullStateInverseReplayCompleted"] is False

    qgroups = q0["currentPendingGroups"]
    target = next(group for group in qgroups if group["group"] == GROUP)
    assert target["pendingIds"] == IDS and target["pendingCount"] == 4
    assert q0["nextSuggestedGroups"] and any(g["group"] == GROUP for g in q0["nextSuggestedGroups"])
    assert index["authoredCounts"] == {"reviewed": 810, "pending": 38}
    assert index["representationCounts"]["completeReviewedStandaloneProcedures"] == 534
    index_rows = {row["id"]: row for row in index["entries"]}
    catalog_rows = {row["id"]: row for row in catalog["spells"]}
    for spell_id in IDS:
        assert index_rows[spell_id]["authoredStatus"] == "pending-authored-procedure"
        assert index_rows[spell_id]["sourceStatus"] == "blocked-pending-operational-review"
        assert catalog_rows[spell_id].get("operational") is None
    for spell_id in ["time-fracture", "foresight-perfect"]:
        assert spell_id not in p0["pendingIds"]

    old_candidate = readj(TEMPLATE)
    historical_candidate = readj(HIST_CANDIDATE)
    old_bindings = old_candidate["sourceBindings"]
    assert len(old_bindings) == 140 and len(historical_candidate["sourceBindings"]) == 140
    with zipfile.ZipFile(HIST_ARCHIVE) as historical_zip:
        assert historical_zip.testzip() is None
        for binding in historical_candidate["sourceBindings"]:
            raw = historical_zip.read("sources/" + binding["path"])
            assert len(raw) == binding["bytes"] and sha(raw) == binding["sha256"]

    old_zip_contents: dict[str, bytes] = {}
    with zipfile.ZipFile(OLD_PACKET) as old_zip:
        assert old_zip.testzip() is None
        assert len(old_zip.namelist()) == 169 and len(set(old_zip.namelist())) == 169
        current_bindings = []
        refreshed_sources = {}
        changed_sources = []
        for binding in old_bindings:
            path = binding["path"]
            assert safe_member(path)
            raw = (ROOT / Path(path)).read_bytes()
            current_bindings.append({"path": path, "bytes": len(raw), "sha256": sha(raw)})
            refreshed_sources["sources_current/" + path] = raw
            old_raw = old_zip.read("sources_current/" + path)
            if old_raw != raw:
                changed_sources.append({"path": path, "previousPacketSha256": sha(old_raw), "currentSha256": sha(raw), "currentBytes": len(raw)})
        for name in old_zip.namelist():
            if name.startswith("sources_current/") or name in {"MANIFEST.json"}:
                continue
            old_zip_contents[name] = old_zip.read(name)
    assert len(current_bindings) == 140

    source_commit = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    branch = subprocess.check_output(["git", "branch", "--show-current"], cwd=ROOT, text=True).strip()
    assert branch == "main"
    source_snapshot = {
        "kind": "working-tree",
        "headCommit": source_commit,
        "branch": branch,
        "indexBinding": bind(INDEX),
        "catalogBinding": bind(CATALOG),
    }

    capture_binding = bind(CAPTURE220)
    source_context = {
        "id": "TIMEFATE6-CURRENT-SOURCE-CONTEXT-221",
        "recordedAtUtc": now,
        "sourceAuthority": AUTH,
        "sourceSnapshot": source_snapshot,
        "group": GROUP,
        "pendingIds": IDS,
        "priorGroupReturn": capture_binding,
        "priorGroupArchiveSealed": False,
        "acceptedIds": [],
        "appliedIds": [],
        "currentIndexBinding": bind(INDEX),
        "currentCatalogBinding": bind(CATALOG),
        "currentPendingAuditInput": bind(PENDING0),
        "currentQueueInput": bind(QUEUE0),
        "currentHandoffInput": bind(HANDOFF0),
        "historicalCandidate": bind(TEMPLATE),
        "historicalSourceCandidate": bind(HIST_CANDIDATE),
        "historicalSourceArchive": bind(HIST_ARCHIVE),
        "previousTimeFateReturn192Receipt": bind(RETURN192_RECEIPT),
        "previousTimeFateReturn192Audit": bind(RETURN192_AUDIT),
    }

    candidate = copy.deepcopy(old_candidate)
    candidate["historicalSourceBindings"] = copy.deepcopy(old_candidate.get("historicalSourceBindings", old_bindings))
    candidate["sourceBindings"] = current_bindings
    candidate["id"] = "RANK9-TIME-FATE6-CURRENT-SOURCE-CONTEXT-221"
    candidate["recordedAtUtc"] = now
    candidate["status"] = "CURRENT_SOURCE_BINDINGS_REFRESHED_FOR_810_REVIEWED_38_PENDING_AUTHORITY"
    candidate["currentAuthority"] = AUTH
    candidate["currentPendingGroup"] = {"group": GROUP, "spellIds": IDS, "count": 4}
    candidate["currentIndexBinding"] = bind(INDEX)
    candidate["currentCatalogBinding"] = bind(CATALOG)
    candidate["currentPendingAuditInputBinding"] = bind(PENDING0)
    candidate["currentQueueInputBinding"] = bind(QUEUE0)
    candidate["currentHandoffInputBinding"] = bind(HANDOFF0)
    candidate["currentAgencyControl220InlineReturnBinding"] = capture_binding
    candidate["currentAgencyControl220SourcePacketSha256"] = capture220["sourcePacket"]["sha256"]
    candidate["currentAgencyControl220ArchiveDelivered"] = False
    candidate["sourceSnapshot"] = source_snapshot
    candidate["currentSourceCommit"] = source_commit
    candidate["currentBranch"] = branch
    candidate["historicalCandidateBinding"] = bind(TEMPLATE)
    candidate["queueCandidateBinding"] = copy.deepcopy(target["candidate"])
    candidate["historicalSourceArchiveBinding"] = bind(HIST_ARCHIVE)
    candidate["sourceBindingRefresh"] = {
        "sourceFiles": len(current_bindings),
        "changedSinceTimeFateSourcePacket191": changed_sources,
        "allSourceBindingsRefreshedFromWorkingTree": True,
    }
    candidate["countsUnchanged"] = {"reviewed": 810, "pending": 38}
    candidate["currentPendingIdSet"] = sorted(p0["pendingIds"])
    candidate["currentTimeFateReturn192ReceiptBinding"] = bind(RETURN192_RECEIPT)
    candidate["currentTimeFateReturn192AuditBinding"] = bind(RETURN192_AUDIT)
    candidate["currentReturn192DirectorDecisionBinding"] = bind(RETURN192_DECISION)

    prior_hold_receipt = readj(RETURN192_RECEIPT)
    assert prior_hold_receipt["unacceptedIds"] == IDS
    assert prior_hold_receipt["acceptedIds"] == ["time-fracture", "foresight-perfect"]
    prior_blocker_ids = {
        spell_id: prior_hold_receipt["blockers"][spell_id]["blockerIds"]
        for spell_id in IDS
    }
    assert prior_blocker_ids == {
        "time-stop": ["TF192-B01"],
        "fate-rewrite": ["TF192-B04"],
        "collapse-timeline": ["TF192-B05"],
        "eternal-prophecy": ["TF192-B02"],
    }

    out_files: dict[str, bytes] = {}
    for name, raw in old_zip_contents.items():
        add_file(out_files, "historical_packet_191/" + name, raw)
    for name, raw in refreshed_sources.items():
        add_file(out_files, name, raw)

    selected_return_members = [
        "DIRECTOR_DECISION.json",
        "EVIDENCE_MANIFEST.json",
        "HOLD_REGISTER.json",
        "INDEPENDENT_SEMANTIC_FAILURE_CHECK.json",
        "MEMBER_MANIFEST.json",
        "PROCEDURES.json",
        "STANDALONE_PROCEDURES.md",
        "procedures/time-stop.json",
        "procedures/fate-rewrite.json",
        "procedures/collapse-timeline.json",
        "procedures/eternal-prophecy.json",
        "procedures/time-fracture.json",
        "procedures/foresight-perfect.json",
    ]
    with zipfile.ZipFile(RETURN192_ZIP) as return_zip:
        assert return_zip.testzip() is None
        return_casebook = json.loads(return_zip.read("CASEBOOK.json"))
        pending_cases = {
            "id": "TIMEFATE6-RETURN192-FOUR-PENDING-CASES",
            "runtimeExecuted": False,
            "scope": "Only the four identities still pending at current authority 810/38/0.",
            "cases": [case for case in return_casebook["cases"] if case.get("spellId") in IDS],
        }
        assert len(pending_cases["cases"]) == 62
        add_file(out_files, "director_history/timefate6_return192_pending_cases.json.gz", gzip.compress(jb(pending_cases), compresslevel=6, mtime=0))
        for name in selected_return_members:
            add_file(out_files, "director_history/timefate6_return192/" + name, return_zip.read(name))

    history_paths = [
        RETURN192_RECEIPT, RETURN192_AUDIT, RETURN192_DECISION, RETURN192_ACCEPTANCE,
        RETURN192_APPLICATION, RETURN192_VALIDATION, RETURN192_INDEX_OPS,
        PREP191, PACKET191, RETURN192_DELIVERY, CAPTURE220,
    ]
    for path in history_paths:
        add_file(out_files, "authority_history/" + path.relative_to(ROOT).as_posix(), path.read_bytes())

    authority_inputs = {
        "authority_current/authored_review_index.json": INDEX.read_bytes(),
        "authority_current/catalog.json": CATALOG.read_bytes(),
        "authority_current/CURRENT_SPELL_QUEUE_220_INPUT.json": QUEUE0.read_bytes(),
        "authority_current/CURRENT_HANDOFF_220_INPUT.json": HANDOFF0.read_bytes(),
        "authority_current/CURRENT38_PENDING_IDENTITY_AUDIT_220_INPUT.json": PENDING0.read_bytes(),
        "authority_current/CURRENT_SOURCE_CONTEXT_221.json": jb(source_context),
    }
    for name, raw in authority_inputs.items():
        add_file(out_files, name, raw)

    request = (
        "GPT director — continue the ordinary-spell review at current authority 810 reviewed/applied / 38 pending / 0 accepted-unapplied, "
        "with 534 complete standalone procedures and 173 scoped interfaces. Review only the four currently pending Rank9 Time/Fate6 identities: "
        "time-stop, fate-rewrite, collapse-timeline, and eternal-prophecy. Do not re-review time-fracture, foresight-perfect, completed feats, or any other spell.\n\n"
        f"Current source snapshot: branch {branch}, HEAD {source_commit}; current index/catalog and the latest queue, handoff, pending audit, "
        "and Return220 inline capture are included. Return220 preserved the two Agency/Control9 holds without acceptance or application; its return archive "
        "was not sealed and its 15 case files/315 events were not freshly replayed.\n\n"
        "Reassess only the exact four prior Time/Fate6 blockers from Return192 against refreshed current source. Carry TF192-B01 for time-stop, "
        "TF192-B04 for fate-rewrite, TF192-B05 for collapse-timeline, and TF192-B02 for eternal-prophecy unless the required source-grounded witness "
        "is now complete. The attached prior Return192 decision, hold register, semantic-failure check, procedures and the 62 cases for these four pending "
        "identities preserve the exact earlier findings. Keep the two already accepted Time/Fate6 identities out of scope.\n\n"
        "Return explicit accepted/held rulings for only the four listed IDs, exact blocker and conditional qualification IDs, source-faithful procedure fields, "
        "reversible before/after traces, exact costs/deadlines/resource and custody histories, and a verifiable compact ZIP plus delivery manifest bound to this packet. "
        "Keep all acceptances unapplied; do not edit canonical files or execute supplied programs. Preserve runtime, implementation, human-play, balance, cosmology, "
        "domain-closure, completion and release gates. I will independently audit and apply only exact acceptances."
    )
    candidate_path = OUT / "CURRENT_SOURCE_CONFERENCE_CANDIDATE_221.json"
    context_path = OUT / "CURRENT_CONTEXT_221.json"
    request_path = OUT / "REQUEST_221.txt"
    candidate_raw = jb(candidate)
    context_raw = jb(source_context)
    request_raw = (request + "\n").encode("utf-8")
    add_file(out_files, "CURRENT_SOURCE_CONFERENCE_CANDIDATE_221.json", candidate_raw)
    add_file(out_files, "CURRENT_CONTEXT_221.json", context_raw)
    add_file(out_files, "REQUEST_221.txt", request_raw)

    payload_rows = []
    for name in sorted(out_files):
        raw = out_files[name]
        payload_rows.append({"path": name, "bytes": len(raw), "sha256": sha(raw), "crc32": crc(raw)})
    manifest = {
        "id": "RANK9-TIME-FATE6-CURRENT-SOURCE-PACKET-MANIFEST-221",
        "sourceSnapshot": source_snapshot,
        "sourceAuthority": AUTH,
        "group": GROUP,
        "pendingIds": IDS,
        "payloadMemberCount": len(payload_rows),
        "members": payload_rows,
    }
    manifest_raw = jb(manifest)

    OUT.mkdir(parents=True)
    packet_path = OUT / "DD_Rank9_TimeFate6_CurrentSource_221.zip"
    with zipfile.ZipFile(packet_path, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=6) as packet_zip:
        for name in sorted(out_files):
            packet_zip.writestr(name, out_files[name])
        packet_zip.writestr("MANIFEST.json", manifest_raw)
    with zipfile.ZipFile(packet_path) as packet_zip:
        assert packet_zip.testzip() is None
        assert len(packet_zip.namelist()) == len(payload_rows) + 1
        for row in payload_rows:
            raw = packet_zip.read(row["path"])
            assert len(raw) == row["bytes"] and sha(raw) == row["sha256"] and crc(raw) == row["crc32"]
        assert json.loads(packet_zip.read("MANIFEST.json"))["members"] == payload_rows
        for binding in current_bindings:
            assert packet_zip.read("sources_current/" + binding["path"]) == (ROOT / Path(binding["path"])).read_bytes()
        assert json.loads(packet_zip.read("CURRENT_SOURCE_CONFERENCE_CANDIDATE_221.json"))["sourceBindings"] == current_bindings

    packet_binding = bind(packet_path)
    candidate_binding = bind(candidate_path, candidate_raw)
    delivery_path = OUT / "DD_Rank9_TimeFate6_CurrentSource_221_DELIVERY.json"
    delivery = {
        "id": "RANK9-TIME-FATE6-CURRENT-SOURCE-DELIVERY-221",
        "status": "PREPARED_UNSENT",
        "archive": packet_binding,
        "memberCount": len(payload_rows) + 1,
        "payloadMemberCount": len(payload_rows),
        "sourceSnapshot": source_snapshot,
        "sourceAuthority": AUTH,
        "group": GROUP,
        "pendingIds": IDS,
        "candidate": candidate_binding,
        "historicalSourceArchive": bind(HIST_ARCHIVE),
        "sourceFilesRefreshed": len(current_bindings),
        "sourceFilesChangedSinceTimeFateSourcePacket191": changed_sources,
        "accepted": False,
        "applied": False,
        "conversation": CHAT,
    }
    delivery_raw = jb(delivery)
    delivery_path.write_bytes(delivery_raw)
    request_path.write_bytes(request_raw)
    candidate_path.write_bytes(candidate_raw)
    context_path.write_bytes(context_raw)

    delivery_binding = bind(delivery_path)
    prep_path = BASE / "RANK9_TIMEFATE6_SOURCE_PREPARATION_221.json"
    prep = {
        "id": "RANK9-TIMEFATE6-SOURCE-PREPARATION-221",
        "recordedAtUtc": now,
        "status": "CURRENT_SOURCE_PACKET_PREPARED_UNSENT",
        "sourceAuthority": AUTH,
        "sourceSnapshot": source_snapshot,
        "group": GROUP,
        "pendingIds": IDS,
        "historicalCandidate": bind(HIST_CANDIDATE),
        "historicalArchive": bind(HIST_ARCHIVE),
        "priorReturn192Receipt": bind(RETURN192_RECEIPT),
        "priorReturn220InlineCapture": capture_binding,
        "sourceFilesRefreshed": len(current_bindings),
        "changedSinceTimeFateSourcePacket191": changed_sources,
        "currentCandidate": candidate_binding,
        "packet": packet_binding,
        "deliveryManifest": delivery_binding,
        "payloadMemberCount": len(payload_rows),
        "return192PendingCasesIncluded": len(pending_cases["cases"]),
        "checksPassed": 9,
        "checksFailed": 0,
        "checks": [
            {"check": "Authority 810/38/0 and 534/173 representation counts agree across index, queue, handoff and pending audit", "passed": True},
            {"check": "Exactly the four target Time/Fate6 identities remain pending; prior accepted identities remain excluded", "passed": True},
            {"check": "Return220 inline holds and no-archive/no-replay status are preserved without application", "passed": True},
            {"check": "Historical Time/Fate source packet and source-conference archive pass integrity and all 140 historical bindings", "passed": True},
            {"check": "All 140 Time/Fate source bindings are refreshed from current working-tree bytes", "passed": True},
            {"check": "Current index/catalog status for all target identities matches the candidate and current pending set", "passed": True},
            {"check": "Return192 decision, hold register, semantic-failure check, procedures and all 62 target cases are included", "passed": True},
            {"check": "Request restricts the director to four pending identities and preserves all prior/unrelated gates", "passed": True},
            {"check": "Packet integrity, unique safe members and all embedded member SHA/CRC values verify", "passed": True},
        ],
        "canonicalChangesBeforePreparation": False,
        "accepted": False,
        "applied": False,
        "request": request,
    }
    prep_path.write_bytes(jb(prep))
    prep_binding = bind(prep_path)
    packet_record_path = BASE / "RANK9_TIMEFATE6_PACKET_221.json"
    packet_record = {
        "id": "RANK9-TIMEFATE6-PACKET-221",
        "status": "PREPARED_UNSENT",
        "sourceAuthority": AUTH,
        "group": GROUP,
        "pendingIds": IDS,
        "packet": packet_binding,
        "deliveryManifest": delivery_binding,
        "preparation": prep_binding,
        "candidate": candidate_binding,
        "conversation": CHAT,
        "checksPassed": 9,
        "checksFailed": 0,
    }
    packet_record_path.write_bytes(jb(packet_record))
    packet_record_binding = bind(packet_record_path)

    capture_ref = bind(CAPTURE220)
    pending_after = copy.deepcopy(p0)
    pending_after.update({
        "id": "CURRENT38-PENDING-IDENTITY-AUDIT-221",
        "recordedAtUtc": now,
        "status": "PASSED_EXACT_CURRENT_INDEX_PENDING_SET_WITH_TIME_FATE6_PACKET_221",
        "lastInlineDirectorReturn": capture_ref,
        "preparedNextGroup": {"group": GROUP, "pendingIds": IDS, "packet": packet_binding, "deliveryManifest": delivery_binding},
    })
    pending_path = BASE / "CURRENT38_PENDING_IDENTITY_AUDIT_221.json"
    pending_path.write_bytes(jb(pending_after))
    pending_binding = bind(pending_path)

    qafter = copy.deepcopy(q0)
    agency = next(group for group in qafter["currentPendingGroups"] if group["group"] == "rank9-agency-control9")
    agency.update({
        "status": "INLINE_HELD_NO_ARCHIVE_810_38",
        "freshPacketRequiredForCurrentAuthority": True,
        "directorDecisionCapture": capture_ref,
        "acceptedIds": [],
        "appliedIds": [],
    })
    time_group = next(group for group in qafter["currentPendingGroups"] if group["group"] == GROUP)
    time_group.update({
        "status": "CURRENT_SOURCE_PACKET_PREPARED_UNSENT_810_38",
        "candidate": candidate_binding,
        "preparedPacket": packet_binding,
        "deliveryManifest": delivery_binding,
        "packetRecord": packet_record_binding,
        "preparation": prep_binding,
        "freshPacketRequiredForCurrentAuthority": False,
    })
    last_batch = {
        "return": 220,
        "group": "rank9-agency-control9",
        "ids": ["absolute-domination", "puppetmaster-s-realm"],
        "acceptedIds": [],
        "appliedIds": [],
        "heldIds": ["absolute-domination", "puppetmaster-s-realm"],
        "blockers": {"absolute-domination": ["AG190-B01"], "puppetmaster-s-realm": ["AG190-B02"]},
        "conditionalQualifications": {spell_id: capture220["directorDecision"]["perIdentity"][spell_id]["conditionalQualificationIds"] for spell_id in capture220["directorDecision"]["heldIds"]},
        "authorityAfter": AUTH,
        "auditStatus": "INLINE_ONLY_NO_SEALED_ARCHIVE_TRACE_REPLAY_UNVERIFIED",
        "decisionCapture": capture_ref,
        "sourcePacket": capture220["sourcePacket"],
    }
    qafter.update({
        "id": "SPELL-REVIEW-QUEUE-221",
        "recordedAtUtc": now,
        "supersedesQueue": bind(QUEUE0),
        "currentReturnAudit": {
            "status": "INLINE_DIRECTOR_HOLDS_CAPTURED; NO SEALED RETURN ARCHIVE; TRACE REPLAY NOT COMPLETED",
            "capture": capture_ref,
            "sourceArchive": capture220["sourcePacket"],
            "returnArchive": None,
            "deliveryManifest": None,
            "independentReplay": False,
        },
        "currentReturnDelivery": None,
        "currentReturnArchive": None,
        "currentReturnDecision": capture_ref,
        "lastReviewedBatch": last_batch,
        "nextGroup": GROUP,
        "next": {"group": GROUP, "pendingIds": IDS, "pendingCount": len(IDS), "status": "CURRENT_SOURCE_PACKET_PREPARED_UNSENT", "packet": packet_binding, "deliveryManifest": delivery_binding, "packetRecord": packet_record_binding, "preparation": prep_binding, "candidate": candidate_binding},
        "nextPreparedRequest": {"group": GROUP, "pendingIds": IDS, "request": bind(request_path, request_raw), "status": "PREPARED_UNSENT"},
        "currentPreparation": prep_binding,
        "currentPacket": packet_binding,
        "currentDeliveryManifest": delivery_binding,
        "currentPacketDelivery": delivery_binding,
        "currentReturnSourceArchive": capture220["sourcePacket"],
        "currentReturnSourceDelivery": {
            "path": capture220["sourcePacket"]["deliveryManifestPath"],
            "sha256": capture220["sourcePacket"]["deliveryManifestSha256"],
        },
        "pendingIdentityAudit": pending_binding,
        "parentQueue": bind(QUEUE0),
        "packetStatus": "RANK9_TIMEFATE6_CURRENT_SOURCE_PACKET_221_PREPARED_UNSENT_810_38",
        "pendingCount": 38,
        "githubChanges": False,
    })
    queue_path = BASE / "CURRENT_SPELL_QUEUE_221.json"
    queue_path.write_bytes(jb(qafter))
    queue_binding = bind(queue_path)

    hafter = copy.deepcopy(h0)
    preserved = copy.deepcopy(hafter.get("preservedOtherHolds", []))
    preserved.append({
        "ids": ["absolute-domination", "puppetmaster-s-realm"],
        "blockerIds": {"absolute-domination": ["AG190-B01"], "puppetmaster-s-realm": ["AG190-B02"]},
        "conditionalQualificationIds": capture220["directorDecision"]["sharedQualificationIds"],
        "decisionCapture": capture_ref,
        "traceReplayVerified": False,
    })
    hafter.update({
        "id": "CURRENT-HANDOFF-221",
        "recordedAtUtc": now,
        "status": "RANK9_TIMEFATE6_CURRENT_SOURCE_PACKET_PREPARED_UNSENT_810_38",
        "currentAuthority": AUTH,
        "latestBatch": last_batch,
        "preservedOtherHolds": preserved,
        "nextGroup": GROUP,
        "nextStep": {"group": GROUP, "pendingIds": IDS, "pendingCount": len(IDS), "status": "CURRENT_SOURCE_PACKET_PREPARED_UNSENT", "packet": packet_binding, "deliveryManifest": delivery_binding},
        "pendingIdentityAudit": pending_binding,
        "queue": queue_binding,
        "currentPreparation": prep_binding,
        "currentPacket": packet_binding,
        "currentPacketDelivery": delivery_binding,
        "appliedThisStep": False,
        "githubChanges": False,
        "runtimeSelectionEnabled": False,
        "canonicalRuntimeApplicationPerformed": False,
    })
    handoff_path = BASE / "CURRENT_HANDOFF_221.json"
    handoff_path.write_bytes(jb(hafter))
    handoff_binding = bind(handoff_path)

    snapshot_path = BASE / "CURRENT_SPELL_REVIEW_SNAPSHOT_221.md"
    snapshot_path.write_text(
        "# Current ordinary spell-review checkpoint 221\n\n"
        "Authority remains **810 reviewed/applied / 38 pending / 0 accepted-unapplied**, with 534 complete standalone procedures and 173 scoped interfaces. "
        "Return220 held absolute-domination and puppetmaster-s-realm under AG190-B01/B02. Its ruling was inline-only, no Return220 ZIP/manifest was sealed, "
        "and the preserved 15 cases/315 events were not freshly replayed. The fresh next packet covers only the four pending Time/Fate6 identities: "
        "time-stop, fate-rewrite, collapse-timeline, and eternal-prophecy.\n\n"
        "See [handoff](CURRENT_HANDOFF_221.json), [queue](CURRENT_SPELL_QUEUE_221.json), [pending audit](CURRENT38_PENDING_IDENTITY_AUDIT_221.json), "
        "[Return220 inline capture](RANK9_AGENCYCONTROL9_RETURN220_INLINE_CAPTURE.json), [packet record](RANK9_TIMEFATE6_PACKET_221.json), "
        "and [source packet](rank9_timefate6_current_source_221_prepared/DD_Rank9_TimeFate6_CurrentSource_221.zip).\n",
        encoding="utf-8",
        newline="\n",
    )

    print(json.dumps({
        "status": "PREPARED_UNSENT",
        "sourceCommit": source_commit,
        "sourceBranch": branch,
        "authority": AUTH,
        "group": GROUP,
        "pendingIds": IDS,
        "refreshedSources": len(current_bindings),
        "changedSinceTimeFateSourcePacket191": changed_sources,
        "pendingReturn192CasesIncluded": len(pending_cases["cases"]),
        "payloadMembers": len(payload_rows),
        "packet": packet_binding,
        "deliveryManifest": delivery_binding,
        "checksPassed": 9,
        "checksFailed": 0,
        "queue": queue_binding,
        "handoff": handoff_binding,
        "capture": capture_ref,
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
