from __future__ import annotations

import copy
import hashlib
import json
import subprocess
import zipfile
import zlib
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath

ROOT = Path(r"C:\Github\DecenniumDescent-review-push-134")
BASE = ROOT / "docs/audit/2026-10-08/full-game/director-spell-review-129"
GROUP = "rank9-casting-cost5"
IDS = ["unholy-ascendance"]
AUTH = {"reviewedApplied": 811, "pending": 37, "acceptedUnapplied": 0, "completeStandaloneProcedures": 535, "scopedInterfaces": 173}
CHAT = "https://chatgpt.com/g/g-p-67f17555a8dc8191a2b5b81e6d8adc12-dungeon-crawler/c/6adc506d-8770-83ea-b64c-0345d9b9b682"
QUEUE0 = BASE / "CURRENT_SPELL_QUEUE_239.json"
HANDOFF0 = BASE / "CURRENT_HANDOFF_239.json"
PENDING0 = BASE / "CURRENT37_PENDING_IDENTITY_AUDIT_239.json"
INDEX = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json"
CATALOG = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json"
OLD_PACKET193 = BASE / "rank9_castingcost5_current_source_193_prepared/DD_Rank9_CastingCost5_CurrentSource_193.zip"
OLD_PACKET222 = BASE / "rank9_castingcost5_current_source_222_prepared_retry1/DD_Rank9_CastingCost5_CurrentSource_222.zip"
TEMPLATE = BASE / "rank9_castingcost5_current_source_193_prepared/CURRENT_SOURCE_CONFERENCE_CANDIDATE_193.json"
HIST_CANDIDATE = ROOT / "DescentReviewChanges/ReviewBible/data/director/spell_review/rank9_casting_cost_5_source_conference_01.json"
HIST_ARCHIVE = ROOT / "docs/audit/2026-10-08/full-game/DD_Rank9_Casting_Cost_5_Source_Conference_01.zip"
R222_DIR = BASE / "rank9_castingcost5_return222_received"
R222_ZIP = R222_DIR / "DD_Rank9_CastingCost2_Director_Return222.zip"
R222_DELIVERY = R222_DIR / "DD_Rank9_CastingCost2_Director_Return222_DELIVERY.json"
R222_RECEIPT = BASE / "RANK9_CASTINGCOST5_RETURN222_RECEIPT.json"
R222_AUDIT = BASE / "RANK9_CASTINGCOST5_RETURN222_INDEPENDENT_AUDIT.json"
R222_DECISION = BASE / "RANK9_CASTINGCOST5_DIRECTOR_DECISION_222.json"
R222_ACCEPTANCE = BASE / "RANK9_CASTINGCOST5_EXACT_ACCEPTANCE_222.json"
R222_APPLICATION = BASE / "RANK9_CASTINGCOST5_APPLICATION_222.json"
R222_VALIDATION = BASE / "RANK9_CASTINGCOST5_APPLICATION_VALIDATION_222.json"
R222_INDEX_OPS = BASE / "RANK9_CASTINGCOST5_INDEX_OPERATIONS_222.json"
R239_DIR = BASE / "rank9_timefate6_return239_received"
R239_ZIP = R239_DIR / "DD_Rank9_TimeFate4_Director_Return239_HELD.zip"
R239_DELIVERY = R239_DIR / "DD_Rank9_TimeFate4_Director_Return239_HELD_DELIVERY.json"
R239_RECEIPT = BASE / "RANK9_TIMEFATE6_RETURN239_RECEIPT.json"
R239_AUDIT = BASE / "RANK9_TIMEFATE6_RETURN239_INDEPENDENT_AUDIT.json"
R238_DIR = BASE / "rank9_agencycontrol9_return238_received"
R238_ZIP = R238_DIR / "DD_Rank9_AgencyControl2_Director_Return238.zip"
R238_DELIVERY = R238_DIR / "DD_Rank9_AgencyControl2_Director_Return238_DELIVERY.json"
R238_RECEIPT = BASE / "RANK9_AGENCYCONTROL9_RETURN238_RECEIPT.json"
R238_AUDIT = BASE / "RANK9_AGENCYCONTROL9_RETURN238_INDEPENDENT_AUDIT.json"
OUT = BASE / "rank9_castingcost5_current_source_240_prepared"


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def crc(raw: bytes) -> str:
    return f"{zlib.crc32(raw) & 0xffffffff:08x}"


def jb(value) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8")


def readj(path: Path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def bind(path: Path, raw: bytes | None = None):
    data = path.read_bytes() if raw is None else raw
    return {"path": path.relative_to(ROOT).as_posix(), "bytes": len(data), "sha256": sha(data), "crc32": crc(data)}


def safe_member(name: str) -> bool:
    path = PurePosixPath(name)
    return bool(name) and "\\" not in name and not path.is_absolute() and all(part not in ("", ".", "..") and not part.startswith(".") for part in path.parts)


def add_file(files: dict[str, bytes], name: str, raw: bytes) -> None:
    assert safe_member(name), name
    assert name not in files, f"Duplicate member: {name}"
    files[name] = raw


def main() -> None:
    assert not OUT.exists(), f"Output already exists: {OUT}"
    required = [QUEUE0, HANDOFF0, PENDING0, INDEX, CATALOG, OLD_PACKET193, OLD_PACKET222, TEMPLATE,
                HIST_CANDIDATE, HIST_ARCHIVE, R222_ZIP, R222_DELIVERY, R222_RECEIPT, R222_AUDIT,
                R222_DECISION, R222_ACCEPTANCE, R222_APPLICATION, R222_VALIDATION, R222_INDEX_OPS,
                R239_ZIP, R239_DELIVERY, R239_RECEIPT, R239_AUDIT, R238_ZIP, R238_DELIVERY, R238_RECEIPT, R238_AUDIT]
    for path in required:
        assert path.exists(), f"Required source missing: {path}"

    now = datetime.now(timezone.utc).isoformat()
    q0, h0, p0 = readj(QUEUE0), readj(HANDOFF0), readj(PENDING0)
    index, catalog = readj(INDEX), readj(CATALOG)
    r222_receipt, r222_audit = readj(R222_RECEIPT), readj(R222_AUDIT)
    r239_receipt, r239_audit = readj(R239_RECEIPT), readj(R239_AUDIT)
    r238_receipt, r238_audit = readj(R238_RECEIPT), readj(R238_AUDIT)
    r238_delivery = readj(R238_DELIVERY)
    assert q0["currentAuthority"] == h0["currentAuthority"] == p0["authority"] == AUTH
    assert p0["pendingCount"] == 37 and IDS[0] in p0["pendingIds"]
    assert q0["nextGroup"] == h0["nextGroup"] == GROUP
    assert r222_audit["status"] == "PASS" and r222_audit["checksFailed"] == 0
    assert r222_receipt["acceptedIds"] == ["perfect-spell"] and r222_receipt["heldIds"] == IDS and r222_receipt["appliedIds"] == []
    assert r239_audit["checksFailed"] == 0 and r239_audit["status"].startswith("PASS_PACKAGE_BINDING_AND_SCOPE")
    assert r239_receipt["heldIds"] == ["time-stop", "fate-rewrite", "collapse-timeline", "eternal-prophecy"]
    assert r238_audit["status"] == "PASS" and r238_delivery["heldIds"] == ["absolute-domination", "puppetmaster-s-realm"]

    target = next(row for row in q0["currentPendingGroups"] if row["group"] == GROUP)
    assert target["pendingIds"] == IDS and target["pendingCount"] == 1 and target["freshPacketRequiredForCurrentAuthority"] is True
    assert target["status"] == "RETURN222_PERFECT_SPELL_APPLIED_UNHOLY_ASCENDANCE_HELD_CC194-B04"
    assert index["authoredCounts"] == {"reviewed": 811, "pending": 37}
    assert index["representationCounts"]["completeReviewedStandaloneProcedures"] == 535
    index_rows = {row["id"]: row for row in index["entries"]}
    catalog_rows = {row["id"]: row for row in catalog["spells"]}
    assert IDS[0] in index_rows and IDS[0] in p0["pendingIds"]
    assert index_rows[IDS[0]]["authoredStatus"] == "pending-authored-procedure"
    assert index_rows[IDS[0]]["sourceStatus"] == "blocked-pending-operational-review"
    assert catalog_rows[IDS[0]].get("operational") is None
    assert "perfect-spell" not in p0["pendingIds"]

    hist_archive_raw = HIST_ARCHIVE.read_bytes()
    historical_candidate = readj(HIST_CANDIDATE)
    old_candidate = readj(TEMPLATE)
    old_bindings = old_candidate["sourceBindings"]
    assert len(old_bindings) == len(historical_candidate["sourceBindings"]) == 117
    with zipfile.ZipFile(HIST_ARCHIVE) as historical_zip:
        assert historical_zip.testzip() is None
        for binding in historical_candidate["sourceBindings"]:
            raw = historical_zip.read("sources/" + binding["path"])
            assert len(raw) == binding["bytes"] and sha(raw) == binding["sha256"]

    old_sources, prior193_sources = {}, {}
    with zipfile.ZipFile(OLD_PACKET193) as archive193, zipfile.ZipFile(OLD_PACKET222) as archive222:
        assert archive193.testzip() is None and archive222.testzip() is None
        for binding in old_bindings:
            name = "sources_current/" + binding["path"]
            old_bytes = archive193.read(name)
            assert len(old_bytes) == binding["bytes"] and sha(old_bytes) == binding["sha256"]
            prior193_sources[binding["path"]] = old_bytes
            old_sources[binding["path"]] = archive222.read(name)
        old_candidate_222 = json.loads(archive222.read("CURRENT_SOURCE_CONFERENCE_CANDIDATE_222.json"))

    refreshed, current_sources, changed = [], {}, []
    for binding in old_bindings:
        path = binding["path"]
        assert safe_member(path)
        raw = (ROOT / Path(path)).read_bytes()
        refreshed.append({"path": path, "bytes": len(raw), "sha256": sha(raw)})
        current_sources["sources_current/" + path] = raw
        if raw != prior193_sources[path]:
            changed.append({"path": path, "previousPacketSha256": sha(prior193_sources[path]), "currentSha256": sha(raw), "currentBytes": len(raw)})
        assert old_sources[path]  # Historical packet222 has the same source family; it remains separately namespaced below.
    assert len(refreshed) == 117

    source_commit = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    branch = subprocess.check_output(["git", "branch", "--show-current"], cwd=ROOT, text=True).strip()
    assert branch == "main"
    source_snapshot = {"kind": "working-tree", "headCommit": source_commit, "branch": branch, "indexBinding": bind(INDEX), "catalogBinding": bind(CATALOG)}

    current = copy.deepcopy(old_candidate_222)
    current["historicalSourceBindings"] = copy.deepcopy(old_candidate_222.get("historicalSourceBindings", old_bindings))
    current["sourceBindings"] = refreshed
    current["id"] = "RANK9-CASTING-COST5-CURRENT-SOURCE-CONTEXT-240"
    current["recordedAtUtc"] = now
    current["status"] = "CURRENT_SOURCE_BINDINGS_REFRESHED_FOR_811_REVIEWED_37_PENDING_AUTHORITY"
    current["currentAuthority"] = AUTH
    current["currentPendingGroup"] = {"group": GROUP, "spellIds": IDS, "count": len(IDS)}
    current["currentIndexBinding"] = bind(INDEX)
    current["currentCatalogBinding"] = bind(CATALOG)
    current["currentPendingAuditInputBinding"] = bind(PENDING0)
    current["currentQueueInputBinding"] = bind(QUEUE0)
    current["currentHandoffInputBinding"] = bind(HANDOFF0)
    current["currentCastingCostReturn222ReceiptBinding"] = bind(R222_RECEIPT)
    current["currentCastingCostReturn222AuditBinding"] = bind(R222_AUDIT)
    current["currentCastingCostReturn222ArchiveBinding"] = bind(R222_ZIP)
    current["currentTimeFateReturn239ReceiptBinding"] = bind(R239_RECEIPT)
    current["currentTimeFateReturn239AuditBinding"] = bind(R239_AUDIT)
    current["currentTimeFateReturn239ArchiveBinding"] = bind(R239_ZIP)
    current["currentAgencyControlReturn238ReceiptBinding"] = bind(R238_RECEIPT)
    current["currentAgencyControlReturn238AuditBinding"] = bind(R238_AUDIT)
    current["sourceSnapshot"] = source_snapshot
    current["currentSourceCommit"] = source_commit
    current["currentBranch"] = branch
    current["historicalCandidateBinding"] = bind(TEMPLATE)
    current["queueCandidateBinding"] = copy.deepcopy(target.get("candidate"))
    current["historicalSourceArchiveBinding"] = bind(HIST_ARCHIVE, hist_archive_raw)
    current["sourceBindingRefresh"] = {"sourceFiles": len(refreshed), "changedSinceCastingCostSourcePacket193": changed, "allSourceBindingsRefreshedFromWorkingTree": True}
    current["countsUnchanged"] = {"reviewed": 811, "pending": 37}
    current["excludedAcceptedAppliedIds"] = ["perfect-spell", "ritual-mastery", "world-rewrite", "resonance-perfection"]
    current["priorUnholyBlocker"] = "CC194-B04"
    for record in current.get("records", []):
        sid = record.get("spellId")
        if sid in index_rows:
            if "currentIndexEntry" in record:
                record["historicalIndexEntry"] = copy.deepcopy(record["currentIndexEntry"])
            record["currentIndexEntry"] = copy.deepcopy(index_rows[sid])
    candidate_raw = jb(current)

    files: dict[str, bytes] = {}
    with zipfile.ZipFile(OLD_PACKET222) as archive222:
        for name in archive222.namelist():
            if name.startswith("sources_current/") or name == "MANIFEST.json":
                continue
            add_file(files, "historical_packet_222/" + name, archive222.read(name))
    for name, raw in current_sources.items():
        add_file(files, name, raw)

    history_files = [R222_RECEIPT, R222_AUDIT, R222_DECISION, R222_ACCEPTANCE, R222_APPLICATION, R222_VALIDATION, R222_INDEX_OPS,
                     R222_DELIVERY, R239_RECEIPT, R239_AUDIT, R239_ZIP, R239_DELIVERY, R238_RECEIPT, R238_AUDIT, R238_ZIP, R238_DELIVERY]
    for path in history_files:
        add_file(files, "authority_history/" + path.relative_to(ROOT).as_posix(), path.read_bytes())
    authority_files = {
        "authority_current/authored_review_index.json": INDEX.read_bytes(),
        "authority_current/catalog.json": CATALOG.read_bytes(),
        "authority_current/CURRENT_SPELL_QUEUE_239_INPUT.json": QUEUE0.read_bytes(),
        "authority_current/CURRENT_HANDOFF_239_INPUT.json": HANDOFF0.read_bytes(),
        "authority_current/CURRENT37_PENDING_IDENTITY_AUDIT_239_INPUT.json": PENDING0.read_bytes(),
    }
    for name, raw in authority_files.items():
        add_file(files, name, raw)

    request = (
        "GPT director — continue the ordinary-spell review at current authority 811 reviewed/applied / 37 pending / 0 accepted-unapplied, "
        "with 535 complete standalone procedures and 173 scoped interfaces. Review only the one pending Rank9 Casting/Cost5 identity: unholy-ascendance. "
        "Do not re-review perfect-spell (accepted and applied), ritual-mastery, world-rewrite, resonance-perfection, the four Time/Fate6 holds, feats, or any other spell.\n\n"
        f"Current source snapshot: branch {branch}, HEAD {source_commit}; current index/catalog, queue239, handoff239, pending audit239, and the latest sealed Return239 decision and independent audit are included. "
        "Return239 retained time-stop, fate-rewrite, collapse-timeline and eternal-prophecy as held; Return238 retained absolute-domination and puppetmaster-s-realm. Casting/Cost5 Return222 accepted and applied perfect-spell, leaving only unholy-ascendance pending.\n\n"
        "Reassess only CC194-B04 for unholy-ascendance against the refreshed current sources, the sealed Return222 ruling and its current applied state. Preserve its exact minimum missing recipient contract and all CC194-H qualifications unless new source-grounded evidence closes them. Require the new caster-Undead form's source-grounded zero-HP/Null recipient contract and complete type-healing, death and other-form adverse traces; preserve actual damage versus non-damage, exact costs, original HP/wounds/equipment and Hunt holds. Do not import monster/global-Null rules.\n\n"
        "Return an explicit accepted/held ruling for unholy-ascendance, exact blocker and conditional qualification IDs, a source-faithful procedure and reversible before/after traces, exact costs and resource/custody histories, and a verifiable ZIP plus matching delivery manifest bound to this packet. Keep every acceptance unapplied; do not edit canonical files or execute supplied programs. Preserve all other accepted spells, feats, holds and runtime, implementation, human-play, balance, cosmology, domain-closure, completion and release gates. I will independently audit and apply only an exact acceptance."
    )
    context = {
        "id": "RANK9-CASTING-COST5-CURRENT-CONTEXT-240", "recordedAtUtc": now, "sourceAuthority": AUTH,
        "sourceSnapshot": source_snapshot, "group": GROUP, "pendingIds": IDS,
        "priorCastingCostReturn222Receipt": bind(R222_RECEIPT), "priorCastingCostReturn222Audit": bind(R222_AUDIT),
        "priorCastingCostReturn222Archive": bind(R222_ZIP), "priorCastingCostReturn222Delivery": bind(R222_DELIVERY),
        "latestTimeFateReturn239Receipt": bind(R239_RECEIPT), "latestTimeFateReturn239Audit": bind(R239_AUDIT),
        "latestTimeFateReturn239Archive": bind(R239_ZIP), "latestTimeFateReturn239Delivery": bind(R239_DELIVERY),
        "priorAgencyControlReturn238Receipt": bind(R238_RECEIPT), "priorAgencyControlReturn238Audit": bind(R238_AUDIT),
        "currentIndex": bind(INDEX), "currentCatalog": bind(CATALOG), "currentPendingInput": bind(PENDING0),
        "currentQueueInput": bind(QUEUE0), "currentHandoffInput": bind(HANDOFF0),
        "historicalCandidate": bind(TEMPLATE), "historicalSourceArchive": bind(HIST_ARCHIVE, hist_archive_raw),
        "excludedAcceptedAppliedIds": current["excludedAcceptedAppliedIds"], "priorUnholyBlocker": "CC194-B04",
    }
    add_file(files, "CURRENT_CONTEXT_240.json", jb(context))
    add_file(files, "CURRENT_SOURCE_CONFERENCE_CANDIDATE_240.json", candidate_raw)
    add_file(files, "REQUEST_240.txt", (request + "\n").encode("utf-8"))

    rows = [{"path": name, "bytes": len(raw), "sha256": sha(raw), "crc32": crc(raw)} for name, raw in sorted(files.items())]
    manifest = {"id": "RANK9-CASTING-COST5-CURRENT-SOURCE-PACKET-MANIFEST-240", "sourceSnapshot": source_snapshot,
                "sourceAuthority": AUTH, "group": GROUP, "pendingIds": IDS, "payloadMemberCount": len(rows), "members": rows}
    manifest_raw = jb(manifest)
    OUT.mkdir(parents=True)
    packet_path = OUT / "DD_Rank9_CastingCost5_CurrentSource_240.zip"
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
        assert json.loads(packet.read("CURRENT_SOURCE_CONFERENCE_CANDIDATE_240.json"))["sourceBindings"] == refreshed
        for binding in refreshed:
            assert packet.read("sources_current/" + binding["path"]) == (ROOT / Path(binding["path"])).read_bytes()

    packet_binding = bind(packet_path)
    candidate_path = OUT / "CURRENT_SOURCE_CONFERENCE_CANDIDATE_240.json"
    context_path = OUT / "CURRENT_CONTEXT_240.json"
    request_path = OUT / "REQUEST_240.txt"
    candidate_path.write_bytes(candidate_raw)
    context_path.write_bytes(jb(context))
    request_path.write_bytes((request + "\n").encode("utf-8"))
    delivery_path = OUT / "DD_Rank9_CastingCost5_CurrentSource_240_DELIVERY.json"
    delivery = {"id": "RANK9-CASTING-COST5-CURRENT-SOURCE-DELIVERY-240", "status": "PREPARED_UNSENT", "archive": packet_binding,
                "memberCount": len(rows) + 1, "payloadMemberCount": len(rows), "sourceSnapshot": source_snapshot,
                "sourceAuthority": AUTH, "group": GROUP, "pendingIds": IDS,
                "candidate": bind(candidate_path, candidate_raw), "historicalSourceArchive": bind(HIST_ARCHIVE, hist_archive_raw),
                "sourceFilesRefreshed": len(refreshed), "sourceFilesChangedSinceCastingCostSourcePacket193": changed,
                "previousReturn222": bind(R222_ZIP), "latestReturn239": bind(R239_ZIP), "previousReturn238": bind(R238_ZIP),
                "accepted": False, "applied": False, "conversation": CHAT}
    delivery_path.write_bytes(jb(delivery))
    delivery_binding = bind(delivery_path)

    prep_checks = [
        "Authority 811/37/0 and 535/173 representation counts agree across current index, queue239, handoff239 and pending audit239.",
        "Exactly unholy-ascendance remains pending in Casting/Cost5; perfect-spell and the other three identities are already accepted/applied and excluded.",
        "Return222 accepted perfect-spell and retained only CC194-B04 for unholy-ascendance; its independent audit passed.",
        "Return239's four Time/Fate6 holds and Return238's two Agency/Control9 holds are included with their independently audited receipts.",
        f"All {len(refreshed)} historical Casting/Cost5 source bindings have been refreshed from current working-tree bytes.",
        "Current catalog/index entries are bound and only unholy-ascendance is targeted in this packet.",
        f"Historical packet and {len(rows)} payload members pass safe-path, size, SHA-256 and CRC32 reconciliation.",
        "Request explicitly forbids application and preserves all other accepted spells, holds and downstream gates.",
    ]
    prep_path = BASE / "RANK9_CASTINGCOST5_SOURCE_PREPARATION_240.json"
    prep = {"id": "RANK9-CASTING-COST5-SOURCE-PREPARATION-240", "recordedAtUtc": now, "status": "CURRENT_SOURCE_PACKET_PREPARED_UNSENT",
            "sourceAuthority": AUTH, "sourceSnapshot": source_snapshot, "group": GROUP, "pendingIds": IDS,
            "historicalCandidate": bind(TEMPLATE), "historicalArchive": bind(HIST_ARCHIVE, hist_archive_raw),
            "previousReturn222": bind(R222_RECEIPT), "latestTimeFateReturn239": bind(R239_RECEIPT),
            "refreshedSourceFiles": len(refreshed), "changedSincePacket193": changed,
            "candidate": bind(candidate_path, candidate_raw), "packet": packet_binding, "deliveryManifest": delivery_binding,
            "payloadMemberCount": len(rows), "checksPassed": len(prep_checks), "checksFailed": 0,
            "checks": [{"check": label, "passed": True} for label in prep_checks], "canonicalChangesBeforePreparation": False,
            "accepted": False, "applied": False, "request": request}
    prep_path.write_bytes(jb(prep))
    prep_binding = bind(prep_path)
    packet_record_path = BASE / "RANK9_CASTINGCOST5_PACKET_240.json"
    packet_record = {"id": "RANK9-CASTING-COST5-PACKET-240", "status": "PREPARED_UNSENT", "sourceAuthority": AUTH,
                     "group": GROUP, "pendingIds": IDS, "packet": packet_binding, "deliveryManifest": delivery_binding,
                     "preparation": prep_binding, "candidate": bind(candidate_path, candidate_raw), "conversation": CHAT,
                     "checksPassed": len(prep_checks), "checksFailed": 0}
    packet_record_path.write_bytes(jb(packet_record))
    packet_record_binding = bind(packet_record_path)

    pending_after = copy.deepcopy(p0)
    pending_after.update({"id": "CURRENT37-PENDING-IDENTITY-AUDIT-240", "recordedAtUtc": now,
                          "status": "PASSED_EXACT_CURRENT_INDEX_PENDING_SET_WITH_CASTING_COST5_PACKET_240",
                          "preparedNextGroup": {"group": GROUP, "pendingIds": IDS, "packet": packet_binding, "deliveryManifest": delivery_binding,
                                                "packetRecord": packet_record_binding, "preparation": prep_binding}})
    pending_path = BASE / "CURRENT37_PENDING_IDENTITY_AUDIT_240.json"
    pending_path.write_bytes(jb(pending_after))
    pending_binding = bind(pending_path)

    last_batch = copy.deepcopy(p0.get("lastDirectorReturn", {}))
    last_batch.update({"return": 239, "group": "rank9-time-fate6", "ids": r239_receipt["reviewedIds"],
                       "acceptedIds": [], "appliedIds": [], "heldIds": r239_receipt["heldIds"],
                       "blockers": {sid: row["blockerIds"] for sid, row in r239_receipt["blockers"].items()},
                       "authorityAfter": AUTH, "auditStatus": r239_audit["status"],
                       "decisionCapture": bind(R239_RECEIPT), "independentAudit": bind(R239_AUDIT)})

    qafter = copy.deepcopy(q0)
    casting_group = next(row for row in qafter["currentPendingGroups"] if row["group"] == GROUP)
    casting_group.update({"status": "CURRENT_SOURCE_PACKET_PREPARED_UNSENT_811_37", "candidate": bind(candidate_path, candidate_raw),
                          "preparedPacket": packet_binding, "deliveryManifest": delivery_binding, "packetRecord": packet_record_binding,
                          "preparation": prep_binding, "freshPacketRequiredForCurrentAuthority": False})
    time_group = next(row for row in qafter["currentPendingGroups"] if row["group"] == "rank9-time-fate6")
    time_group.update({"status": "RETURN239_ALL_HELD_ARCHIVE_AUDITED", "freshPacketRequiredForCurrentAuthority": True,
                       "directorReturn": bind(R239_ZIP), "directorDelivery": bind(R239_DELIVERY),
                       "independentAudit": bind(R239_AUDIT), "acceptedIds": [], "appliedIds": []})
    qafter.update({"id": "SPELL-REVIEW-QUEUE-240", "recordedAtUtc": now, "supersedesQueue": bind(QUEUE0),
                   "lastReviewedBatch": last_batch, "nextGroup": GROUP,
                   "next": {"group": GROUP, "pendingIds": IDS, "pendingCount": len(IDS), "status": "CURRENT_SOURCE_PACKET_PREPARED_UNSENT",
                            "packet": packet_binding, "deliveryManifest": delivery_binding, "packetRecord": packet_record_binding, "preparation": prep_binding},
                   "currentPreparation": prep_binding, "currentPacket": packet_binding, "currentDeliveryManifest": delivery_binding,
                   "currentPacketDelivery": delivery_binding, "pendingIdentityAudit": pending_binding, "parentQueue": bind(QUEUE0),
                   "packetStatus": "RANK9_CASTINGCOST5_CURRENT_SOURCE_PACKET_240_PREPARED_UNSENT_811_37", "pendingCount": 37, "githubChanges": False})
    queue_path = BASE / "CURRENT_SPELL_QUEUE_240.json"
    queue_path.write_bytes(jb(qafter))
    queue_binding = bind(queue_path)

    hafter = copy.deepcopy(h0)
    hafter.update({"id": "CURRENT-HANDOFF-240", "recordedAtUtc": now,
                   "status": "RANK9_CASTINGCOST5_CURRENT_SOURCE_PACKET_PREPARED_UNSENT_811_37", "currentAuthority": AUTH,
                   "latestBatch": last_batch, "nextGroup": GROUP,
                   "nextStep": {"group": GROUP, "pendingIds": IDS, "pendingCount": 1, "status": "CURRENT_SOURCE_PACKET_PREPARED_UNSENT",
                                "packet": packet_binding, "deliveryManifest": delivery_binding},
                   "pendingIdentityAudit": pending_binding, "queue": queue_binding,
                   "currentPreparation": prep_binding, "currentPacket": packet_binding, "currentPacketDelivery": delivery_binding,
                   "appliedThisStep": False, "githubChanges": False, "runtimeSelectionEnabled": False,
                   "canonicalRuntimeApplicationPerformed": False})
    handoff_path = BASE / "CURRENT_HANDOFF_240.json"
    handoff_path.write_bytes(jb(hafter))
    handoff_binding = bind(handoff_path)

    snapshot_path = BASE / "CURRENT_SPELL_REVIEW_SNAPSHOT_240.md"
    snapshot_path.write_text(
        "# Current ordinary spell-review checkpoint 240\n\n"
        "Authority remains **811 reviewed/applied / 37 pending / 0 accepted-unapplied**, with 535 complete standalone procedures and 173 scoped interfaces. "
        "Return239 passed independent package/source-binding verification and held the four Time/Fate6 identities. Return238's two Agency/Control9 holds remain preserved. "
        "The fresh next packet covers only the remaining Casting/Cost5 identity **unholy-ascendance**; **perfect-spell** is already accepted and applied.\n\n"
        "See [handoff](CURRENT_HANDOFF_240.json), [queue](CURRENT_SPELL_QUEUE_240.json), [pending audit](CURRENT37_PENDING_IDENTITY_AUDIT_240.json), "
        "[Return239 receipt](RANK9_TIMEFATE6_RETURN239_RECEIPT.json), [packet record](RANK9_CASTINGCOST5_PACKET_240.json), "
        "and [source packet](rank9_castingcost5_current_source_240_prepared/DD_Rank9_CastingCost5_CurrentSource_240.zip).\n",
        encoding="utf-8", newline="\n")

    print(json.dumps({"status": "PREPARED_UNSENT", "sourceCommit": source_commit, "sourceBranch": branch, "authority": AUTH,
                      "group": GROUP, "pendingIds": IDS, "refreshedSources": len(refreshed), "changedSincePacket193": changed,
                      "payloadMembers": len(rows), "packet": packet_binding, "deliveryManifest": delivery_binding,
                      "checksPassed": len(prep_checks), "checksFailed": 0, "queue": queue_binding, "handoff": handoff_binding}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
