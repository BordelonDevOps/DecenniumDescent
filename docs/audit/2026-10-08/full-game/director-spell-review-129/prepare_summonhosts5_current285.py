from __future__ import annotations

import copy
import hashlib
import json
import subprocess
import zipfile
import zlib
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
AUDIT = ROOT / "docs/audit/2026-10-08/full-game/director-spell-review-129"
AUTH = {"reviewedApplied": 816, "pending": 32, "acceptedUnapplied": 0,
        "completeStandaloneProcedures": 540, "scopedInterfaces": 173}
GROUP = "rank9-summon-hosts5"
TARGETS = ["summon-elemental-avatar", "summon-herald-of-the-planes", "summon-avatar-of-decay"]
CLOSED = ["conjure-magmatic-wyrm", "planar-army"]
BLOCKERS = {"summon-elemental-avatar": ["SH202-B01"], "summon-herald-of-the-planes": ["SH202-B02"],
            "summon-avatar-of-decay": ["SH202-B03"]}
OUT = AUDIT / "rank9_summonhosts5_current_source_285_prepared"
ARCHIVE = OUT / "DD_Rank9_SummonHosts5_CurrentSource_285.zip"
DELIVERY = OUT / "DD_Rank9_SummonHosts5_CurrentSource_285_DELIVERY.json"
CANDIDATE_FILE = OUT / "CURRENT_SOURCE_CONFERENCE_CANDIDATE_285.json"
CONTEXT_FILE = OUT / "CURRENT_CONTEXT_285.json"
REQUEST_FILE = OUT / "REQUEST_285.txt"
PREPARATION = AUDIT / "RANK9SUMMONHOSTS5_SOURCE_PREPARATION_285.json"
PACKET_RECORD = AUDIT / "RANK9SUMMONHOSTS5_PACKET_285.json"
QUEUE = AUDIT / "CURRENT_SPELL_QUEUE_285.json"
HANDOFF = AUDIT / "CURRENT_HANDOFF_285.json"
PENDING = AUDIT / "CURRENT32_PENDING_IDENTITY_AUDIT_285.json"
SNAPSHOT = AUDIT / "CURRENT_SPELL_REVIEW_SNAPSHOT_285.md"
START = ROOT / "START_HERE.md"
INDEX = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json"
CATALOG = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json"
QUEUE284 = AUDIT / "CURRENT_SPELL_QUEUE_284.json"
HANDOFF284 = AUDIT / "CURRENT_HANDOFF_284.json"
PENDING284 = AUDIT / "CURRENT32_PENDING_IDENTITY_AUDIT_284.json"
RETURN284_DIR = AUDIT / "rank9_planargates5_return284_received"
RETURN284_ZIP = RETURN284_DIR / "DD_Rank9_PlanarGates5_Director_Return284_HELD.zip"
RETURN284_DELIVERY = RETURN284_DIR / "DD_Rank9_PlanarGates5_Director_Return284_HELD_DELIVERY.json"
RETURN284_AUDIT = AUDIT / "RANK9_PLANARGATES5_RETURN284_INDEPENDENT_AUDIT.json"
RETURN284_RECEIPT = AUDIT / "RANK9_PLANARGATES5_RETURN284_RECEIPT.json"
PACKET284_DIR = AUDIT / "rank9_planargates5_current_source_284_prepared"
PACKET284_ZIP = PACKET284_DIR / "DD_Rank9_PlanarGates5_CurrentSource_284.zip"
PACKET284_DELIVERY = PACKET284_DIR / "DD_Rank9_PlanarGates5_CurrentSource_284_DELIVERY.json"
PACKET284_AUDIT = AUDIT / "RANK9PLANARGATES5_PACKET_284_INDEPENDENT_AUDIT.json"
PACKET284_RECEIPT = AUDIT / "RANK9PLANARGATES5_PACKET_284_RECEIPT.json"
PACKET284_RECORD = AUDIT / "RANK9PLANARGATES5_PACKET_284.json"
HISTORIC_PACKET = AUDIT / "rank9_summonhosts5_current_source_244_prepared/DD_Rank9_SummonHosts5_CurrentSource_244.zip"
RETURN244 = AUDIT / "rank9_summonhosts5_return244_received/DD_Rank9_SummonHosts3_Director_Return244_HELD.zip"
RETURN244_DELIVERY = AUDIT / "rank9_summonhosts5_return244_received/DD_Rank9_SummonHosts3_Director_Return244_HELD_DELIVERY.json"
RETURN244_AUDIT = AUDIT / "RANK9SUMMONHOSTS5_RETURN244_INDEPENDENT_AUDIT.json"
RETURN244_RECEIPT = AUDIT / "RANK9SUMMONHOSTS5_RETURN244_RECEIPT.json"
RETURN202_AUDIT = AUDIT / "RANK9_SUMMONHOSTS5_RETURN202_INDEPENDENT_AUDIT.json"
RETURN202_RECEIPT = AUDIT / "RANK9_SUMMONHOSTS5_RETURN202_RECEIPT.json"
RETURN202_DECISION = AUDIT / "RANK9_SUMMONHOSTS5_DIRECTOR_DECISION_202.json"
RETURN202_APPLICATION = AUDIT / "RANK9_SUMMONHOSTS5_APPLICATION_202.json"
RETURN202_ACCEPTANCE = AUDIT / "RANK9_SUMMONHOSTS5_EXACT_ACCEPTANCE_202.json"
RETURN202_VALIDATION = AUDIT / "RANK9_SUMMONHOSTS5_APPLICATION_VALIDATION_202.json"


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def crc(raw: bytes) -> str:
    return f"{zlib.crc32(raw) & 0xffffffff:08x}"


def git_blob(raw: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(raw)).encode("ascii") + b"\0" + raw).hexdigest()


def dump(value: object) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8")


def read(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def file_binding(path: Path, raw: bytes | None = None) -> dict:
    data = path.read_bytes() if raw is None else raw
    return {"path": path.relative_to(ROOT).as_posix(), "bytes": len(data),
            "sha256": sha(data), "crc32": crc(data)}


def source_binding(path: str, raw: bytes) -> dict:
    return {"path": path, "bytes": len(raw), "sha256": sha(raw), "gitBlobSHA1": git_blob(raw)}


def main() -> None:
    index = read(INDEX); catalog = read(CATALOG)
    queue284 = read(QUEUE284); handoff284 = read(HANDOFF284); pending284 = read(PENDING284)
    return284_delivery = read(RETURN284_DELIVERY); return284_audit = read(RETURN284_AUDIT); return284_receipt = read(RETURN284_RECEIPT)
    packet284_audit = read(PACKET284_AUDIT); packet284_receipt = read(PACKET284_RECEIPT)
    return244_audit = read(RETURN244_AUDIT); return244_receipt = read(RETURN244_RECEIPT)
    return202_receipt = read(RETURN202_RECEIPT)
    assert queue284["currentAuthority"] == handoff284["currentAuthority"] == AUTH
    assert return284_delivery["authority"] == return284_audit["authority"] == AUTH
    assert return284_audit["status"] == return284_receipt["status"] == "PASS" and return284_audit["checksPassed"] == 18
    assert packet284_audit["status"] == packet284_receipt["status"] == "PASS"
    assert return244_audit["status"] == return244_receipt["status"] == "PASS"
    assert set(return202_receipt["acceptedIds"]) == set(CLOSED)
    assert pending284["pendingCount"] == 32 and all(s in pending284["pendingIds"] for s in TARGETS)
    assert index["authoredCounts"] == {"reviewed": 816, "pending": 32}
    assert index["representationCounts"]["completeReviewedStandaloneProcedures"] == 540
    entries = {x["id"]: x for x in index["entries"]}; spells = {x["id"]: x for x in catalog["spells"]}
    live_pending = sorted(x["id"] for x in index["entries"] if x.get("authoredStatus") == "pending-authored-procedure")
    assert live_pending == sorted(pending284["pendingIds"]) and len(live_pending) == 32
    assert set(TARGETS) <= set(live_pending) and all(s in spells for s in TARGETS + CLOSED)
    assert all(entries[s]["authoredStatus"] == "pending-authored-procedure" for s in TARGETS)
    assert all(entries[s]["authoredStatus"] == "reviewed-authored-operational-playtest" for s in CLOSED)
    assert queue284["next"]["group"] == "rank9-planar-gates5"
    assert queue284["currentPendingGroups"]

    now = datetime.now(timezone.utc).isoformat()
    pending = copy.deepcopy(pending284)
    pending.update({"id": "CURRENT32-PENDING-IDENTITY-AUDIT-285", "recordedAtUtc": now,
        "status": "RETURN284_INDEPENDENTLY_AUDITED_HELD_NEXT_SUMMONHOSTS5_PACKET285_PREPARATION",
        "indexBinding": file_binding(INDEX), "catalogBinding": file_binding(CATALOG),
        "lastDirectorReturn": {"return": 284, "group": "rank9-planar-gates5", "acceptedIds": [], "appliedIds": [],
            "heldIds": ["banishment-gate", "conjure-demiplane-fortress"], "blockers": {"banishment-gate": ["PG200-B03", "PG200-B04"],
            "conjure-demiplane-fortress": ["PG200-B06"]}, "independentAudit": file_binding(RETURN284_AUDIT)},
        "lastReviewedBatch": {"return": 284, "group": "rank9-planar-gates5", "acceptedIds": [], "appliedIds": [],
            "heldIds": ["banishment-gate", "conjure-demiplane-fortress"], "blockers": {"banishment-gate": ["PG200-B03", "PG200-B04"],
            "conjure-demiplane-fortress": ["PG200-B06"]}, "authorityBefore": AUTH, "authorityAfter": AUTH},
        "nextGroup": {"group": GROUP, "pendingIds": TARGETS, "pendingCount": 3},
        "preparedNextGroup": {"group": GROUP, "pendingIds": TARGETS, "pendingCount": 3,
            "status": "CURRENT_SOURCE_PACKET_285_PREPARED_UNSENT_816_32"}})
    pending_bytes = dump(pending); PENDING.write_bytes(pending_bytes)

    packet_rel = "docs/audit/2026-10-08/full-game/director-spell-review-129/rank9_summonhosts5_current_source_285_prepared/DD_Rank9_SummonHosts5_CurrentSource_285.zip"
    q = copy.deepcopy(queue284)
    q.update({"id": "SPELL-REVIEW-QUEUE-285", "recordedAtUtc": now, "supersedesQueue": file_binding(QUEUE284),
        "nextGroup": GROUP, "nextPendingIds": TARGETS, "nextPendingCount": 3,
        "status": "RETURN284_AUDITED_HELD_NEXT_SUMMONHOSTS5_PACKET285_PREPARED_UNSENT_816_32",
        "packetStatus": "RANK9_SUMMONHOSTS5_PACKET285_PREPARED_UNSENT_816_32"})
    for row in q.get("currentPendingGroups", []):
        if row.get("group") == "rank9-planar-gates5":
            row.update({"status": "HELD_RETURN284_INDEPENDENTLY_AUDITED_PG200_B03_B04_B06", "freshPacketRequiredForCurrentAuthority": True,
                "lastDirectorReturn": {"return": 284, "acceptedIds": [], "appliedIds": [],
                    "heldIds": ["banishment-gate", "conjure-demiplane-fortress"], "blockers": {"banishment-gate": ["PG200-B03", "PG200-B04"],
                    "conjure-demiplane-fortress": ["PG200-B06"]}, "independentAudit": file_binding(RETURN284_AUDIT)}})
        if row.get("group") == GROUP:
            row.update({"status": "CURRENT_SOURCE_PACKET_285_PREPARED_UNSENT_816_32", "pendingIds": TARGETS,
                "pendingCount": 3, "freshPacketRequiredForCurrentAuthority": True,
                "preparedPacket": {"path": packet_rel, "status": "PREPARED_UNSENT"},
                "lastDirectorReturn": {"return": 244, "acceptedIds": [], "appliedIds": [], "heldIds": TARGETS,
                    "blockers": BLOCKERS, "independentAudit": file_binding(RETURN244_AUDIT)}})
    next_row = next(x for x in q["currentPendingGroups"] if x["group"] == GROUP)
    pending_ref = {"id": pending["id"], "path": PENDING.relative_to(ROOT).as_posix(), "pendingCount": 32, "sha256": sha(pending_bytes)}
    q.update({"next": {"group": GROUP, "pendingIds": TARGETS, "pendingCount": 3,
        "status": "CURRENT_SOURCE_PACKET_285_PREPARED_UNSENT", "freshPacketRequiredForCurrentAuthority": True,
        "historicalCandidate": next_row.get("candidate"), "historicalArchive": next_row.get("archive"), "packetPath": packet_rel},
        "nextSuggestedGroups": [copy.deepcopy(next_row)], "pendingIdentityAudit": pending_ref,
        "currentPendingAudit": pending_ref, "lastReviewedBatch": {"return": 284, "group": "rank9-planar-gates5",
            "acceptedIds": [], "appliedIds": [], "heldIds": ["banishment-gate", "conjure-demiplane-fortress"],
            "blockers": {"banishment-gate": ["PG200-B03", "PG200-B04"], "conjure-demiplane-fortress": ["PG200-B06"]},
            "authorityBefore": AUTH, "authorityAfter": AUTH, "independentAudit": file_binding(RETURN284_AUDIT)},
        "currentReturnArchive": file_binding(RETURN284_ZIP), "currentReturnDelivery": file_binding(RETURN284_DELIVERY),
        "currentReturnAudit": file_binding(RETURN284_AUDIT), "currentReturnReceipt": file_binding(RETURN284_RECEIPT),
        "currentPreparation": None, "currentPacket": None, "currentPacketDelivery": None, "currentPacketRecord": None,
        "currentIndependentAudit": None, "currentReceipt": None,
        "nextPreparedRequest": {"group": GROUP, "pendingIds": TARGETS, "pendingCount": 3,
            "status": "CURRENT_SOURCE_PACKET_285_PREPARED_UNSENT", "freshPacketRequiredForCurrentAuthority": True, "packetPath": packet_rel}})
    q_bytes = dump(q); QUEUE.write_bytes(q_bytes)

    h = copy.deepcopy(handoff284)
    h.update({"id": "CURRENT-HANDOFF-285", "recordedAtUtc": now,
        "status": "RETURN284_INDEPENDENTLY_AUDITED_HELD_NEXT_SUMMONHOSTS5_PACKET285_PREPARED_UNSENT_816_32",
        "authority": AUTH, "currentAuthority": AUTH, "queue": file_binding(QUEUE, q_bytes),
        "queueBinding": file_binding(QUEUE, q_bytes), "currentQueueBinding": file_binding(QUEUE, q_bytes),
        "pendingIdentityAudit": pending_ref, "nextGroup": GROUP, "nextPendingCount": 3,
        "latestBatch": {"return": 284, "group": "rank9-planar-gates5", "ids": ["banishment-gate", "conjure-demiplane-fortress"],
            "acceptedIds": [], "appliedIds": [], "heldIds": ["banishment-gate", "conjure-demiplane-fortress"],
            "blockers": {"banishment-gate": ["PG200-B03", "PG200-B04"], "conjure-demiplane-fortress": ["PG200-B06"]},
            "independentAudit": file_binding(RETURN284_AUDIT)},
        "nextStep": {"group": GROUP, "pendingIds": TARGETS, "pendingCount": 3,
            "status": "CURRENT_SOURCE_PACKET_285_PREPARED_UNSENT_AT_AUTHORITY_816_32_0",
            "freshPacketRequiredForCurrentAuthority": True, "candidate": next_row.get("candidate"),
            "archive": next_row.get("archive"), "packetPath": packet_rel},
        "currentReturnBinding": file_binding(RETURN284_ZIP), "currentReturnArchive": file_binding(RETURN284_ZIP),
        "currentReturnDelivery": file_binding(RETURN284_DELIVERY), "currentReturnAudit": file_binding(RETURN284_AUDIT),
        "currentReturnReceipt": file_binding(RETURN284_RECEIPT), "currentPacket": None, "currentPacketDelivery": None,
        "currentPacketRecord": None, "currentPreparation": None, "currentIndependentAudit": None, "currentReceipt": None,
        "nextPreparedRequest": {"group": GROUP, "pendingIds": TARGETS, "pendingCount": 3,
            "status": "CURRENT_SOURCE_PACKET_285_PREPARED_UNSENT", "freshPacketRequiredForCurrentAuthority": True, "packetPath": packet_rel},
        "resumePriority": "Submit fresh Packet285 for only summon-elemental-avatar, summon-herald-of-the-planes, and summon-avatar-of-decay to GPT Director. Check the browser frequently, seal and independently audit its return, then apply only exact accepted IDs."})
    h_bytes = dump(h); HANDOFF.write_bytes(h_bytes)

    head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    branch = subprocess.check_output(["git", "branch", "--show-current"], cwd=ROOT, text=True).strip()
    assert branch == "main"
    start_lines = START.read_text(encoding="utf-8-sig").splitlines()
    start_lines[0] = ("**Current ordinary spell-review handoff [285](docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT_HANDOFF_285.json):** "
        "authority remains 816 applied / 32 pending / 0 accepted-unapplied. Return284 held two Planar Gates identities and passed an independent 18-check audit. "
        "A fresh Rank9 Summon Hosts5 packet for `summon-elemental-avatar`, `summon-herald-of-the-planes`, and `summon-avatar-of-decay` is prepared for GPT. "
        "Return202 acceptances `conjure-magmatic-wyrm` and `planar-army` remain closed. See [packet record](docs/audit/2026-10-08/full-game/director-spell-review-129/RANK9SUMMONHOSTS5_PACKET_285.json).")
    START.write_text("\n".join(start_lines) + "\n", encoding="utf-8", newline="\n")

    # Use the latest full source capture for current files and the target-specific historical source candidate for procedures/questions.
    with zipfile.ZipFile(HISTORIC_PACKET) as historic_zip:
        historic_candidate = json.loads(historic_zip.read("CURRENT_SOURCE_CONFERENCE_CANDIDATE_244.json"))
        historic_context = json.loads(historic_zip.read("CURRENT_CONTEXT_244.json"))
    with zipfile.ZipFile(PACKET284_ZIP) as packet_zip:
        latest_candidate = json.loads(packet_zip.read("CURRENT_SOURCE_CONFERENCE_CANDIDATE_284.json"))
        latest_packet_members = {name: packet_zip.read(name) for name in packet_zip.namelist() if name != "MANIFEST.json"}
    by_id = {x["spellId"]: x for x in historic_candidate["records"]}
    assert set(TARGETS) == set(by_id)
    candidate = copy.deepcopy(historic_candidate)
    candidate.update({"id": "CURRENT-SOURCE-CONFERENCE-CANDIDATE-285", "recordedAtUtc": now,
        "status": "PREPARED_CURRENT_AUTHORITY_816_32_EXACT_THREE_PENDING_SUMMON_HOSTS_IDENTITIES",
        "currentSourceCommit": head, "currentBranch": branch, "currentAuthority": AUTH,
        "countsUnchanged": index["authoredCounts"], "currentPendingGroup": {"group": GROUP, "spellIds": TARGETS, "count": 3},
        "closedAcceptedSpellIds": CLOSED,
        "closedAcceptedSpellDecisionBinding": {"return": 202, "acceptedIds": CLOSED, "appliedIds": CLOSED,
            "decisionPath": RETURN202_DECISION.relative_to(ROOT).as_posix(), "applicationPath": RETURN202_APPLICATION.relative_to(ROOT).as_posix(),
            "exactAcceptancePath": RETURN202_ACCEPTANCE.relative_to(ROOT).as_posix(), "auditPath": RETURN202_AUDIT.relative_to(ROOT).as_posix(),
            "receiptPath": RETURN202_RECEIPT.relative_to(ROOT).as_posix(), "doNotReopen": True},
        "previousReturn244Binding": {"archive": file_binding(RETURN244), "delivery": file_binding(RETURN244_DELIVERY),
            "independentAudit": file_binding(RETURN244_AUDIT), "receipt": file_binding(RETURN244_RECEIPT), "outsideCurrentAuthority": True},
        "latestPriorReturn284Binding": {"archive": file_binding(RETURN284_ZIP), "delivery": file_binding(RETURN284_DELIVERY),
            "independentAudit": file_binding(RETURN284_AUDIT), "receipt": file_binding(RETURN284_RECEIPT),
            "heldIdsOutsideScope": ["banishment-gate", "conjure-demiplane-fortress"]},
        "latestPriorPacket284Binding": {"archive": file_binding(PACKET284_ZIP), "delivery": file_binding(PACKET284_DELIVERY),
            "independentAudit": file_binding(PACKET284_AUDIT), "receipt": file_binding(PACKET284_RECEIPT)}})
    candidate["records"] = [copy.deepcopy(by_id[s]) for s in TARGETS]
    for row in candidate["records"]:
        sid = row["spellId"]
        row["currentIndexEntry"] = copy.deepcopy(entries[sid])
        row["completeCurrentCatalogSourceAndAccess"] = copy.deepcopy(spells[sid])
        row["status"] = "Pending current identity; reassess only the exact SH202 blocker against current source-qualified evidence."
        row["closedAcceptedSpellIds"] = CLOSED

    extra_paths = {
        "START_HERE.md", INDEX.relative_to(ROOT).as_posix(), CATALOG.relative_to(ROOT).as_posix(),
        PENDING.relative_to(ROOT).as_posix(), QUEUE.relative_to(ROOT).as_posix(), HANDOFF.relative_to(ROOT).as_posix(),
        QUEUE284.relative_to(ROOT).as_posix(), HANDOFF284.relative_to(ROOT).as_posix(), PENDING284.relative_to(ROOT).as_posix(),
        RETURN284_ZIP.relative_to(ROOT).as_posix(), RETURN284_DELIVERY.relative_to(ROOT).as_posix(), RETURN284_AUDIT.relative_to(ROOT).as_posix(), RETURN284_RECEIPT.relative_to(ROOT).as_posix(),
        PACKET284_ZIP.relative_to(ROOT).as_posix(), PACKET284_DELIVERY.relative_to(ROOT).as_posix(), PACKET284_AUDIT.relative_to(ROOT).as_posix(), PACKET284_RECEIPT.relative_to(ROOT).as_posix(), PACKET284_RECORD.relative_to(ROOT).as_posix(),
        RETURN244.relative_to(ROOT).as_posix(), RETURN244_DELIVERY.relative_to(ROOT).as_posix(), RETURN244_AUDIT.relative_to(ROOT).as_posix(), RETURN244_RECEIPT.relative_to(ROOT).as_posix(),
        RETURN202_AUDIT.relative_to(ROOT).as_posix(), RETURN202_RECEIPT.relative_to(ROOT).as_posix(), RETURN202_DECISION.relative_to(ROOT).as_posix(),
        RETURN202_APPLICATION.relative_to(ROOT).as_posix(), RETURN202_ACCEPTANCE.relative_to(ROOT).as_posix(), RETURN202_VALIDATION.relative_to(ROOT).as_posix(),
        "docs/audit/2026-10-08/full-game/director-spell-review-129/RANK9SUMMONHOSTS5_NEXT_CONFERENCE_NOTES_129.json",
        "docs/audit/2026-10-08/full-game/director-spell-review-129/RANK9SUMMONHOSTS5_PACKET_244.json",
        "docs/audit/2026-10-08/full-game/director-spell-review-129/RANK9_SUMMONHOSTS5_APPLICATION_202.json",
    }
    historic_rows = historic_candidate["sourceBindings"]
    latest_rows = latest_candidate["sourceBindings"]
    source_paths = sorted({r["path"] for r in historic_rows} | set(extra_paths))
    source_bytes = {rel: (ROOT / rel).read_bytes() for rel in source_paths}
    rows = [source_binding(rel, source_bytes[rel]) for rel in source_paths]
    old_hashes = {r["path"]: (r["bytes"], r["sha256"]) for r in historic_rows}
    changed = [rel for rel, old in old_hashes.items() if (len(source_bytes[rel]), sha(source_bytes[rel])) != old]
    candidate["historicalSourceBindings"] = copy.deepcopy(historic_candidate.get("historicalSourceBindings", historic_rows))
    candidate["sourceBindings"] = rows
    candidate["sourceBindingRefresh"] = {"historicalSourceFiles": len(historic_candidate.get("historicalSourceBindings", historic_rows)),
        "priorCurrentSourceFiles": len(historic_rows), "latestPriorPacketSourceFiles": len(latest_rows),
        "currentSourceFiles": len(rows), "changedSincePriorSummonHostsCandidate": len(changed),
        "changedPaths": changed[:100], "allTargetAndCurrentBindingsRefreshedFromCurrentWorkingTree": True,
        "exactOverlayBoundBySHA256AndGitBlobSHA1": True}
    candidate["currentPendingIdentityAudit"] = file_binding(PENDING, pending_bytes)

    context = copy.deepcopy(historic_context)
    context.update({"id": "CURRENT-CONTEXT-285", "recordedAtUtc": now, "sourceBranch": branch, "sourceCommit": head,
        "sourceAuthority": AUTH, "targetGroup": {"group": GROUP, "pendingIds": TARGETS, "count": 3},
        "currentPendingAudit": file_binding(PENDING, pending_bytes), "currentQueue": file_binding(QUEUE, q_bytes),
        "currentHandoff": file_binding(HANDOFF, h_bytes), "currentIndexCounts": index["authoredCounts"],
        "currentPendingGroupCount": 32, "return244HistoricalHold": {"archive": file_binding(RETURN244),
            "audit": file_binding(RETURN244_AUDIT), "receipt": file_binding(RETURN244_RECEIPT), "outsideCurrentAuthority": True},
        "return284PlanarGatesHoldOutsideScope": {"heldIds": ["banishment-gate", "conjure-demiplane-fortress"],
            "blockers": {"banishment-gate": ["PG200-B03", "PG200-B04"], "conjure-demiplane-fortress": ["PG200-B06"]},
            "archive": file_binding(RETURN284_ZIP), "audit": file_binding(RETURN284_AUDIT), "receipt": file_binding(RETURN284_RECEIPT)},
        "latestPacket284SourceContext": {"archive": file_binding(PACKET284_ZIP), "audit": file_binding(PACKET284_AUDIT),
            "receipt": file_binding(PACKET284_RECEIPT)}, "closedAcceptedReturn202": {"acceptedIds": CLOSED,
            "appliedIds": CLOSED, "doNotReopen": True, "decision": file_binding(RETURN202_DECISION),
            "application": file_binding(RETURN202_APPLICATION), "audit": file_binding(RETURN202_AUDIT),
            "receipt": file_binding(RETURN202_RECEIPT)}, "sourceBindingRefresh": candidate["sourceBindingRefresh"]})
    context["qualification"] = ("Review only the three pending Summon Hosts identities. Return202's conjure-magmatic-wyrm and planar-army acceptances are closed. "
        "Return284 held banishment-gate and conjure-demiplane-fortress outside this scope. Preserve the original Summon Hosts questions, addenda, and future obligations; "
        "reassess each SH202 blocker against current source-qualified evidence. Invent no actors, acquired extra-turn sources, damage, events, or history. "
        "Keep runtime, implementation, human-play, balance, cosmology, completion, and release gates closed.")

    request = (
        "GPT Director — continue ordinary spell review at current authority 816 reviewed-applied / 32 pending / 0 accepted-unapplied, "
        "with 540 complete standalone procedures and 173 scoped interfaces. Review exactly summon-elemental-avatar, summon-herald-of-the-planes, "
        "and summon-avatar-of-decay, the three pending identities in rank9-summon-hosts5.\n\n"
        f"Current source snapshot: branch {branch}, HEAD {head}, with exact working-tree overlay bindings in this packet. Use the refreshed source rows, queue 285, handoff 285, "
        "pending identity audit, Return244 history, Return202 acceptance/application records, and the independently audited Return284 context. "
        "conjure-magmatic-wyrm and planar-army were accepted and applied exactly in Return202; do not reopen them. Return284 held only banishment-gate and "
        "conjure-demiplane-fortress outside this scope. Reassess SH202-B01/B02/B03 against current evidence instead of carrying blockers forward mechanically.\n\n"
        "Preserve original target questions and future obligations as source context. Preserve exact native placement, class route, cost, source entry, acquisition path, "
        "and prior lifecycle. Resolve only what current source evidence supports; do not invent actors, extra-turn providers, damage, control events, or acquisition histories. "
        "Keep runtime, implementation, human-play, balance, cosmology, completion, and release gates closed.\n\n"
        "Return explicit per-identity accepted/applied/held decisions with exact blockers and minimum missing witnesses, all case and reversible-operation results, "
        "a sealed ZIP and matching DELIVERY.json, and the next pending group. Do not modify canonical files or run supplied programs. Apply no changes in this review."
    )

    # Start from the latest sealed source packet, refresh its current overlay, retain its historical material, then add target-specific history/evidence.
    members: dict[str, bytes] = {}
    for name, raw in latest_packet_members.items():
        if name.startswith(("current/", "sources_current/")):
            rel = name.split("/", 1)[1]
            path = ROOT / rel
            members[name] = path.read_bytes() if path.is_file() else raw
        else:
            members[name] = raw
    members["HISTORICAL_SUMMONHOSTS_SOURCE_CONFERENCE_CANDIDATE_244.json"] = dump(historic_candidate)
    members["HISTORICAL_SUMMONHOSTS_CONTEXT_244.json"] = dump(historic_context)
    members["CURRENT_SOURCE_CONFERENCE_CANDIDATE_285.json"] = dump(candidate)
    members["CURRENT_CONTEXT_285.json"] = dump(context)
    members["REQUEST_285.txt"] = request.encode("utf-8")
    members["current/" + PENDING.relative_to(ROOT).as_posix()] = pending_bytes
    members["current/" + QUEUE.relative_to(ROOT).as_posix()] = q_bytes
    members["current/" + HANDOFF.relative_to(ROOT).as_posix()] = h_bytes
    for rel, raw in source_bytes.items():
        members["sources_current/" + rel] = raw
    evidence = {
        "evidence/RETURN284.zip": RETURN284_ZIP, "evidence/RETURN284_DELIVERY.json": RETURN284_DELIVERY,
        "evidence/RETURN284_INDEPENDENT_AUDIT.json": RETURN284_AUDIT, "evidence/RETURN284_RECEIPT.json": RETURN284_RECEIPT,
        "evidence/PACKET284_DELIVERY.json": PACKET284_DELIVERY, "evidence/PACKET284_INDEPENDENT_AUDIT.json": PACKET284_AUDIT,
        "evidence/PACKET284_RECEIPT.json": PACKET284_RECEIPT, "evidence/RETURN244.zip": RETURN244,
        "evidence/RETURN244_DELIVERY.json": RETURN244_DELIVERY, "evidence/RETURN244_INDEPENDENT_AUDIT.json": RETURN244_AUDIT,
        "evidence/RETURN244_RECEIPT.json": RETURN244_RECEIPT, "evidence/RETURN202_INDEPENDENT_AUDIT.json": RETURN202_AUDIT,
        "evidence/RETURN202_RECEIPT.json": RETURN202_RECEIPT, "evidence/RETURN202_DECISION.json": RETURN202_DECISION,
        "evidence/RETURN202_APPLICATION.json": RETURN202_APPLICATION, "evidence/RETURN202_EXACT_ACCEPTANCE.json": RETURN202_ACCEPTANCE,
        "evidence/RETURN202_APPLICATION_VALIDATION.json": RETURN202_VALIDATION,
    }
    for name, path in evidence.items():
        members[name] = path.read_bytes()
    for rel, raw in source_bytes.items():
        members["sources_current/" + rel] = raw

    OUT.mkdir(parents=True, exist_ok=True)
    CANDIDATE_FILE.write_bytes(dump(candidate)); CONTEXT_FILE.write_bytes(dump(context)); REQUEST_FILE.write_bytes(request.encode("utf-8"))
    manifest_rows = []
    with zipfile.ZipFile(ARCHIVE, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for name in sorted(members):
            raw = members[name]
            z.writestr(name, raw)
            manifest_rows.append({"path": name, "bytes": len(raw), "sha256": sha(raw), "crc32": crc(raw)})
        z.writestr("MANIFEST.json", dump({"id": "RANK9-SUMMON-HOSTS5-CURRENT-SOURCE-285-MANIFEST",
            "memberCountExcludingSelf": len(manifest_rows), "sourceAuthority": AUTH, "scope": TARGETS,
            "closedAcceptedIds": CLOSED, "members": manifest_rows}))
    with zipfile.ZipFile(ARCHIVE) as z:
        assert z.testzip() is None and len(z.namelist()) == len(set(z.namelist()))
        assert z.read("REQUEST_285.txt").decode("utf-8") == request
    archive_bytes = ARCHIVE.read_bytes()
    delivery = {"id": "RANK9-SUMMON-HOSTS5-CURRENT-SOURCE-DELIVERY-285", "status": "PREPARED_UNSENT",
        "group": GROUP, "pendingIds": TARGETS, "accepted": False, "applied": False, "sourceBranch": branch,
        "sourceCommit": head, "sourceAuthority": AUTH, "closedAcceptedIds": CLOSED,
        "outsideScopeHolds": {"banishment-gate": ["PG200-B03", "PG200-B04"],
            "conjure-demiplane-fortress": ["PG200-B06"], "faction-omniscience-supreme": ["KR198-B01"]},
        "archive": {"path": ARCHIVE.name, "bytes": len(archive_bytes), "sha256": sha(archive_bytes), "crc32": crc(archive_bytes)},
        "candidate": file_binding(CANDIDATE_FILE), "context": file_binding(CONTEXT_FILE), "request": file_binding(REQUEST_FILE),
        "sourceBindings": len(rows), "archiveMembers": len(manifest_rows) + 1,
        "return202AcceptedApplied": CLOSED, "return244HistoricalReturn": RETURN244.name,
        "return284HeldOutsideScope": ["banishment-gate", "conjure-demiplane-fortress"]}
    DELIVERY.write_bytes(dump(delivery))
    PREPARATION.write_bytes(dump({"id": "RANK9-SUMMON-HOSTS5-SOURCE-PREPARATION-285", "recordedAtUtc": now,
        "status": "PASS", "sourceBranch": branch, "sourceCommit": head, "sourceAuthority": AUTH,
        "targetGroup": GROUP, "pendingIds": TARGETS, "closedAcceptedIds": CLOSED,
        "historicalSourceBindingCount": len(candidate.get("historicalSourceBindings", [])),
        "priorCurrentSourceBindingCount": len(historic_rows), "refreshedSourceBindingCount": len(rows),
        "changedSincePriorSummonHostsCandidate": changed, "latestPacket284SourceBindingCount": len(latest_rows),
        "packet": delivery["archive"], "deliveryManifest": file_binding(DELIVERY),
        "return284Audit": file_binding(RETURN284_AUDIT), "return244Audit": file_binding(RETURN244_AUDIT),
        "checks": [{"check": "Current authored index and pending set match authority 816/32/0", "passed": True},
            {"check": "Only the three pending Summon Hosts identities are in review scope", "passed": [r["spellId"] for r in candidate["records"]] == TARGETS},
            {"check": "Return202 acceptances remain applied, excluded, and closed", "passed": set(CLOSED) == set(return202_receipt["acceptedIds"]) and set(CLOSED).isdisjoint(TARGETS)},
            {"check": "Return284 passed 18 independent checks and its two Planar holds remain outside scope", "passed": return284_audit["status"] == "PASS" and return284_audit["checksPassed"] == 18},
            {"check": "All source paths exist and are rebound to current bytes", "passed": all((ROOT / p).is_file() for p in source_paths)},
            {"check": "Packet ZIP is readable, unique, and bound by matching delivery", "passed": zipfile.is_zipfile(ARCHIVE) and delivery["pendingIds"] == TARGETS}],
        "canonicalChanges": False}))
    PACKET_RECORD.write_bytes(dump({"id": "RANK9SUMMONHOSTS5-PACKET-285", "status": "PREPARED_UNSENT",
        "group": GROUP, "pendingIds": TARGETS, "closedAcceptedIds": CLOSED, "sourceAuthority": AUTH,
        "sourceBranch": branch, "sourceCommit": head, "archive": delivery["archive"],
        "deliveryManifest": file_binding(DELIVERY), "candidate": file_binding(CANDIDATE_FILE),
        "context": file_binding(CONTEXT_FILE), "request": file_binding(REQUEST_FILE),
        "sourceBindings": len(rows), "return284Audit": file_binding(RETURN284_AUDIT), "canonicalChanges": False}))
    SNAPSHOT.write_text("# Current ordinary spell-review snapshot 285\n\n"
        "Return284 is independently audited PASS (18/18); `banishment-gate` and `conjure-demiplane-fortress` remain held under PG200-B03/B04/B06. "
        "Authority remains 816 reviewed-applied, 32 pending, 0 accepted-unapplied (540 complete standalone procedures; 173 scoped interfaces). "
        "Next is `rank9-summon-hosts5`, scoped only to `summon-elemental-avatar`, `summon-herald-of-the-planes`, and `summon-avatar-of-decay`. "
        "Return202 acceptances `conjure-magmatic-wyrm` and `planar-army` remain applied and closed.\n", encoding="utf-8", newline="\n")

    print(json.dumps({"status": "PASS", "archive": delivery["archive"], "sourceBindings": len(rows),
        "members": delivery["archiveMembers"], "authority": AUTH, "targetIds": TARGETS,
        "currentPendingCount": len(live_pending), "sourceChangedPaths": len(changed)}, indent=2))


if __name__ == "__main__":
    main()
