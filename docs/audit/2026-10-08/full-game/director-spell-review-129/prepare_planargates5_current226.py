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
OLD_PACKET = AUDIT / "rank9_planargates5_current_source_199_prepared/DD_Rank9_PlanarGates5_CurrentSource_199.zip"
RETURN225_DIR = AUDIT / "rank9_knowledgerevelation5_return225_received"
RETURN225_ZIP = RETURN225_DIR / "DD_Rank9_KnowledgeRevelation1_Director_Return225.zip"
RETURN225_DELIVERY = RETURN225_DIR / "DD_Rank9_KnowledgeRevelation1_Director_Return225_DELIVERY.json"
RETURN225_AUDIT = AUDIT / "RANK9_KNOWLEDGEREVELATION5_RETURN225_INDEPENDENT_AUDIT.json"
RETURN225_RECEIPT = AUDIT / "RANK9_KNOWLEDGEREVELATION5_RETURN225_RECEIPT.json"
RETURN225_DECISION = AUDIT / "rank9_knowledgerevelation5_return225_received/extracted/DIRECTOR_DECISION.json"
RETURN200_DIR = AUDIT / "rank9_planargates5_return200_received"
RETURN200_ZIP = RETURN200_DIR / "DD_Rank9_PlanarGates5_Director_Return200.zip"
RETURN200_DELIVERY = RETURN200_DIR / "DD_Rank9_PlanarGates5_Director_Return200_DELIVERY.json"
RETURN200_AUDIT = AUDIT / "RANK9_PLANARGATES5_RETURN200_INDEPENDENT_AUDIT.json"
RETURN200_APPLICATION = AUDIT / "RANK9_PLANARGATES5_APPLICATION_200.json"
RETURN200_DECISION = AUDIT / "RANK9_PLANARGATES5_DIRECTOR_DECISION_200.json"
RETURN200_RECEIPT = AUDIT / "RANK9_PLANARGATES5_RETURN200_RECEIPT.json"
QUEUE225 = AUDIT / "CURRENT_SPELL_QUEUE_225.json"
HANDOFF225 = AUDIT / "CURRENT_HANDOFF_225.json"
PENDING225 = AUDIT / "CURRENT37_PENDING_IDENTITY_AUDIT_225.json"
INDEX = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json"
CATALOG = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json"
OUT = AUDIT / "rank9_planargates5_current_source_226_prepared"
ARCHIVE = OUT / "DD_Rank9_PlanarGates5_CurrentSource_226.zip"
DELIVERY = OUT / "DD_Rank9_PlanarGates5_CurrentSource_226_DELIVERY.json"
CANDIDATE_FILE = OUT / "CURRENT_SOURCE_CONFERENCE_CANDIDATE_226.json"
CONTEXT_FILE = OUT / "CURRENT_CONTEXT_226.json"
REQUEST_FILE = OUT / "REQUEST_226.txt"
PREPARATION = AUDIT / "RANK9PLANARGATES5_SOURCE_PREPARATION_226.json"
PACKET_RECORD = AUDIT / "RANK9PLANARGATES5_PACKET_226.json"
QUEUE226 = AUDIT / "CURRENT_SPELL_QUEUE_226.json"
HANDOFF226 = AUDIT / "CURRENT_HANDOFF_226.json"
SNAPSHOT226 = AUDIT / "CURRENT_SPELL_REVIEW_SNAPSHOT_226.md"
TARGET_IDS = ["banishment-gate", "conjure-demiplane-fortress"]
CLOSED_IDS = ["gate", "absolute-gate", "planar-sanctuary"]
AUTH = {"reviewedApplied": 811, "pending": 37, "acceptedUnapplied": 0,
        "completeStandaloneProcedures": 535, "scopedInterfaces": 173}


def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def crc(b: bytes) -> str:
    return f"{zlib.crc32(b) & 0xffffffff:08x}"


def git_blob_sha(b: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(b)).encode("ascii") + b"\0" + b).hexdigest()


def info(path: Path, raw: bytes | None = None) -> dict:
    b = path.read_bytes() if raw is None else raw
    return {"path": path.relative_to(ROOT).as_posix(), "bytes": len(b), "sha256": sha(b), "crc32": crc(b)}


def source_row(path: Path, raw: bytes | None = None) -> dict:
    b = path.read_bytes() if raw is None else raw
    return {"path": path.relative_to(ROOT).as_posix(), "bytes": len(b), "sha256": sha(b), "gitBlobSHA1": git_blob_sha(b)}


def binding(row: dict) -> dict:
    return {"path": row["path"], "bytes": row["bytes"], "sha256": row["sha256"], "crc32": row["crc32"]}


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def dump_json(value: object) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8")


def main() -> None:
    assert not OUT.exists() and not any(p.exists() for p in (PREPARATION, PACKET_RECORD, QUEUE226, HANDOFF226, SNAPSHOT226))
    return225_audit = read_json(RETURN225_AUDIT)
    return225_delivery = read_json(RETURN225_DELIVERY)
    return200_audit = read_json(RETURN200_AUDIT)
    return200_application = read_json(RETURN200_APPLICATION)
    return200_decision = read_json(RETURN200_DECISION)
    assert return225_audit["status"] == "PASS" and return225_audit["checksFailed"] == 0
    assert return200_audit["status"] == "PASS" and return200_application["acceptedIds"] == CLOSED_IDS
    assert return200_application["status"] == "APPLIED_THREE_EXACT_AUTHORED_PROCEDURES_WITH_TWO_RETAINED_BLOCKERS"
    assert return200_decision["acceptedIds"] == CLOSED_IDS
    with zipfile.ZipFile(RETURN225_ZIP) as z:
        director_decision_raw = z.read("DIRECTOR_DECISION.json")
        director_decision = json.loads(director_decision_raw)
    assert director_decision["nextPendingGroup"] == {"group": "rank9-planar-gates5", "pendingIds": TARGET_IDS, "reviewStarted": False}
    assert director_decision["accepted"] is False and director_decision["applied"] is False

    queue225, handoff225 = read_json(QUEUE225), read_json(HANDOFF225)
    pending = read_json(PENDING225)
    index, catalog = read_json(INDEX), read_json(CATALOG)
    assert queue225["currentAuthority"] == handoff225["currentAuthority"] == AUTH
    assert pending["pendingCount"] == 37 and all(x in pending["pendingIds"] for x in TARGET_IDS + ["faction-omniscience-supreme"])
    entries = {x["id"]: x for x in index["entries"]}
    cards = {x["id"]: x for x in catalog["spells"]}
    assert all(entries[x]["authoredStatus"] == "pending-authored-procedure" for x in TARGET_IDS)
    assert all(entries[x]["authoredStatus"] == "reviewed-authored-operational-playtest" for x in CLOSED_IDS)
    assert all(x in cards for x in TARGET_IDS + CLOSED_IDS)

    head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, check=True, capture_output=True, text=True).stdout.strip()
    branch = subprocess.run(["git", "branch", "--show-current"], cwd=ROOT, check=True, capture_output=True, text=True).stdout.strip()
    assert branch == "main"
    timestamp = datetime.now(timezone.utc).isoformat()
    RETURN225_DECISION.parent.mkdir(parents=True, exist_ok=True)
    RETURN225_DECISION.write_bytes(director_decision_raw)
    packet_relative = "docs/audit/2026-10-08/full-game/director-spell-review-129/rank9_planargates5_current_source_226_prepared/DD_Rank9_PlanarGates5_CurrentSource_226.zip"

    # Preserve the established queue while replacing only the current decision and next exact group.
    queue = copy.deepcopy(queue225)
    queue.update({"id": "SPELL-REVIEW-QUEUE-226", "recordedAtUtc": timestamp,
                  "supersedesQueue": info(QUEUE225), "nextGroup": "rank9-planar-gates5",
                  "packetStatus": "RANK9_PLANARGATES5_PACKET_226_PREPARED_UNSENT_811_37"})
    for row in queue["currentPendingGroups"]:
        if row["group"] == "rank9-knowledge-revelation5":
            row["status"] = "HELD_RETURN225_KR198-B01_AUDITED"
            row["freshPacketRequiredForCurrentAuthority"] = True
            row["lastDirectorReturn"] = {"return": 225, "acceptedIds": [], "appliedIds": [],
                "heldIds": ["faction-omniscience-supreme"], "blockers": ["KR198-B01"],
                "independentAudit": info(RETURN225_AUDIT)}
        if row["group"] == "rank9-planar-gates5":
            row["status"] = "PENDING_FRESH_DIRECTOR_PACKET_AT_AUTHORITY_811_37_0"
            row["freshPacketRequiredForCurrentAuthority"] = True
            row["pendingIds"] = TARGET_IDS
            row["pendingCount"] = 2
    next_row = next(x for x in queue["currentPendingGroups"] if x["group"] == "rank9-planar-gates5")
    queue["next"] = {"group": "rank9-planar-gates5", "pendingIds": TARGET_IDS, "pendingCount": 2,
                     "status": "CURRENT_SOURCE_PACKET_PREPARED_UNSENT", "freshPacketRequiredForCurrentAuthority": True,
                     "historicalCandidate": next_row.get("candidate"), "historicalArchive": next_row.get("archive")}
    queue["nextSuggestedGroups"] = [copy.deepcopy(next_row)]
    queue["currentPendingGroups"] = queue["currentPendingGroups"]
    queue["currentReturnAudit"] = info(RETURN225_AUDIT)
    queue["currentReturnDelivery"] = info(RETURN225_DELIVERY)
    queue["currentReturnArchive"] = info(RETURN225_ZIP)
    queue["currentReturnReceipt"] = info(RETURN225_RECEIPT)
    queue["currentReturnDecision"] = info(RETURN225_DECISION)
    queue["currentReturnAudit"]["status"] = "PASS"
    queue["lastReviewedBatch"] = {"return": 225, "group": "rank9-knowledge-revelation5",
        "acceptedIds": [], "appliedIds": [], "heldIds": ["faction-omniscience-supreme"], "blockers": ["KR198-B01"],
        "independentAudit": info(RETURN225_AUDIT)}
    queue["pendingIdentityAudit"] = {"id": pending["id"], "path": PENDING225.relative_to(ROOT).as_posix(),
        "pendingCount": pending["pendingCount"], "sha256": sha(PENDING225.read_bytes())}
    queue["currentPacket"] = None
    queue["currentPacketDelivery"] = None
    queue["currentPreparation"] = None
    queue["currentReturnBinding"] = info(RETURN225_ZIP)
    queue["currentReturnSourceArchive"] = info(RETURN225_ZIP)
    queue["currentReturnSourceDelivery"] = info(RETURN225_DELIVERY)
    queue["currentReturnBinding"]["status"] = "INDEPENDENTLY_AUDITED_HELD"
    queue["nextPreparedRequest"] = {"group": "rank9-planar-gates5", "pendingIds": TARGET_IDS,
        "pendingCount": 2, "status": "CURRENT_SOURCE_PACKET_PREPARED_UNSENT",
        "freshPacketRequiredForCurrentAuthority": True, "packetPath": packet_relative}
    queue_bytes = dump_json(queue)
    QUEUE226.write_bytes(queue_bytes)

    handoff = copy.deepcopy(handoff225)
    handoff.update({"id": "CURRENT-HANDOFF-226", "recordedAtUtc": timestamp,
        "status": "RANK9_KNOWLEDGEREVELATION5_RETURN225_AUDITED_NEXT_PLANARGATES5_811_37"})
    handoff["latestBatch"] = {"return": 225, "group": "rank9-knowledge-revelation5",
        "ids": ["faction-omniscience-supreme"], "acceptedIds": [], "appliedIds": [],
        "heldIds": ["faction-omniscience-supreme"], "blockers": {"faction-omniscience-supreme": ["KR198-B01"]},
        "independentAudit": info(RETURN225_AUDIT)}
    handoff["nextStep"] = {"group": "rank9-planar-gates5", "pendingIds": TARGET_IDS, "pendingCount": 2,
        "status": "CURRENT_SOURCE_PACKET_PREPARED_UNSENT_AT_AUTHORITY_811_37_0",
        "freshPacketRequiredForCurrentAuthority": True, "candidate": next_row.get("candidate"), "archive": next_row.get("archive")}
    handoff["pendingIdentityAudit"] = {"id": pending["id"], "path": PENDING225.relative_to(ROOT).as_posix(),
        "pendingCount": pending["pendingCount"], "sha256": sha(PENDING225.read_bytes())}
    handoff["queue"] = {"path": QUEUE226.relative_to(ROOT).as_posix(), "bytes": len(queue_bytes),
        "sha256": sha(queue_bytes), "crc32": crc(queue_bytes)}
    handoff["appliedThisStep"] = {"return": 225, "group": "rank9-knowledge-revelation5",
        "ids": ["faction-omniscience-supreme"], "acceptedIds": [], "appliedIds": [],
        "heldIds": ["faction-omniscience-supreme"], "blockers": {"faction-omniscience-supreme": ["KR198-B01"]},
        "sourceAuthorityBefore": AUTH, "sourceAuthorityAfter": AUTH,
        "directorReturn": info(RETURN225_ZIP), "deliveryManifest": info(RETURN225_DELIVERY),
        "independentAudit": info(RETURN225_AUDIT), "currentDecision": info(RETURN225_DECISION),
        "exactAcceptance": False}
    handoff["nextGroup"] = "rank9-planar-gates5"
    handoff["nextPendingCount"] = 2
    handoff["unacceptedThisStep"] = {"ids": ["faction-omniscience-supreme"],
        "blockers": {"faction-omniscience-supreme": ["KR198-B01"]}, "retainedInPendingSet": True}
    handoff["currentReturnBinding"] = info(RETURN225_ZIP)
    handoff["currentReturnDelivery"] = info(RETURN225_DELIVERY)
    handoff["currentReturnAudit"] = info(RETURN225_AUDIT)
    handoff["currentPreparation"] = None
    handoff["currentPacket"] = None
    handoff["currentPacketDelivery"] = None
    handoff["currentQueueBinding"] = {"path": QUEUE226.relative_to(ROOT).as_posix(), "bytes": len(queue_bytes),
        "sha256": sha(queue_bytes), "crc32": crc(queue_bytes)}
    handoff["nextPreparedRequest"] = {"group": "rank9-planar-gates5", "pendingIds": TARGET_IDS,
        "pendingCount": 2, "status": "CURRENT_SOURCE_PACKET_PREPARED_UNSENT",
        "freshPacketRequiredForCurrentAuthority": True, "packetPath": packet_relative}
    handoff["resumePriority"] = "Submit fresh packet 226 for only banishment-gate and conjure-demiplane-fortress; preserve all prior acceptances and holds, audit the reply, and apply only exact accepted identities."
    handoff_bytes = dump_json(handoff)
    HANDOFF226.write_bytes(handoff_bytes)
    SNAPSHOT226.write_text(
        "# Current ordinary spell-review snapshot 226\n\n"
        "Return225 was independently audited and held only `faction-omniscience-supreme` under KR198-B01 and H01-H06. "
        "Authority remains 811 reviewed/applied, 37 pending, 0 accepted-unapplied (535 complete standalone procedures; 173 scoped interfaces). "
        "The GPT director named Rank9 Planar Gates5 as the next group. Its only pending identities are `banishment-gate` and `conjure-demiplane-fortress`; "
        "`gate`, `absolute-gate`, and `planar-sanctuary` were accepted and applied in Return200 and are closed context.\n",
        encoding="utf-8", newline="\n")

    # Rebind the original five-spell candidate to current bytes, then scope its decision records to the two pending identities.
    with zipfile.ZipFile(OLD_PACKET) as old:
        historical_candidate = json.loads(old.read("CURRENT_SOURCE_CONFERENCE_CANDIDATE_199.json"))
        historical_context = json.loads(old.read("CURRENT_CONTEXT_199.json"))
        old_members = {n: old.read(n) for n in old.namelist() if n != "MANIFEST.json"}
    candidate = copy.deepcopy(historical_candidate)
    candidate.update({"id": "CURRENT-SOURCE-CONFERENCE-CANDIDATE-226", "recordedAtUtc": timestamp,
        "status": "PREPARED_CURRENT_AUTHORITY_811_37_EXACT_TWO_PENDING_PLANAR_GATE_IDENTITIES",
        "currentSourceCommit": head, "currentBranch": branch, "currentAuthority": AUTH,
        "currentPendingGroup": {"group": "rank9-planar-gates5", "spellIds": TARGET_IDS, "count": 2},
        "countsUnchanged": index["authoredCounts"]})
    candidate["records"] = [copy.deepcopy(r) for r in candidate["records"] if r["spellId"] in TARGET_IDS]
    for record in candidate["records"]:
        sid = record["spellId"]
        record["completeCurrentCatalogSourceAndAccess"] = copy.deepcopy(cards[sid])
        record["currentIndexEntry"] = copy.deepcopy(entries[sid])
        record["status"] = "Pending exact current identity at authority 811/37; no new procedure or vector is selected."
        record["closedAcceptedSpellIds"] = CLOSED_IDS
    candidate["closedAcceptedSpellIds"] = CLOSED_IDS
    candidate["closedAcceptedSpellDecisionBinding"] = {
        "decisionPath": RETURN200_DECISION.relative_to(ROOT).as_posix(),
        "auditPath": RETURN200_AUDIT.relative_to(ROOT).as_posix(),
        "applicationPath": RETURN200_APPLICATION.relative_to(ROOT).as_posix(),
        "acceptedIds": CLOSED_IDS, "appliedIds": CLOSED_IDS,
        "doNotReopen": True}
    candidate["priorReturn225Binding"] = {"archive": info(RETURN225_ZIP), "delivery": info(RETURN225_DELIVERY),
        "independentAudit": info(RETURN225_AUDIT), "receipt": info(RETURN225_RECEIPT),
        "heldIds": ["faction-omniscience-supreme"], "blockerIds": ["KR198-B01"]}
    candidate["newCurrentAuthoritySnapshots"] = [
        info(INDEX), info(CATALOG), info(QUEUE226), info(HANDOFF226), info(PENDING225),
        info(RETURN225_ZIP), info(RETURN225_DELIVERY), info(RETURN225_AUDIT), info(RETURN225_RECEIPT), info(RETURN225_DECISION),
        info(RETURN200_DELIVERY), info(RETURN200_AUDIT), info(RETURN200_APPLICATION), info(RETURN200_DECISION), info(RETURN200_RECEIPT)]
    historical_bindings = {r["path"]: copy.deepcopy(r) for r in historical_candidate["sourceBindings"]}
    extra_paths = [INDEX, CATALOG, QUEUE226, HANDOFF226, PENDING225, RETURN225_ZIP, RETURN225_DELIVERY,
        RETURN225_AUDIT, RETURN225_RECEIPT, RETURN225_DECISION, RETURN200_DELIVERY, RETURN200_AUDIT,
        RETURN200_APPLICATION, RETURN200_DECISION, RETURN200_RECEIPT]
    current_paths = {ROOT / row["path"] for row in historical_candidate["sourceBindings"]}
    current_paths.update(p.resolve() for p in extra_paths)
    rows = [source_row(p) for p in sorted(current_paths, key=lambda p: p.relative_to(ROOT).as_posix())]
    candidate["historicalSourceBindings"] = historical_candidate["sourceBindings"]
    candidate["sourceBindings"] = rows
    old_by_path = {r["path"]: r for r in historical_candidate["sourceBindings"]}
    changed = sum(1 for r in rows if r["path"] in old_by_path and
                  (r["bytes"] != old_by_path[r["path"]]["bytes"] or r["sha256"] != old_by_path[r["path"]]["sha256"]))
    candidate["sourceBindingRefresh"] = {"sourceFiles": len(rows), "changedSinceHistoricalCandidate": changed,
        "sourceContentsFromGitCommit": False, "allSourceBindingsRefreshedFromCurrentWorkingTree": True,
        "allUncommittedBytesBoundBySHA256AndGitBlobId": True}
    candidate["historicalCandidateBinding"] = {"path": "HISTORICAL_CURRENT_SOURCE_CONFERENCE_CANDIDATE_199.json",
        "bytes": len(old_members["CURRENT_SOURCE_CONFERENCE_CANDIDATE_199.json"]),
        "sha256": sha(old_members["CURRENT_SOURCE_CONFERENCE_CANDIDATE_199.json"])}
    candidate["queueCandidateBinding"] = {"path": "CURRENT_SPELL_QUEUE_225.json",
        "bytes": len(QUEUE225.read_bytes()), "sha256": sha(QUEUE225.read_bytes())}

    context = copy.deepcopy(historical_context)
    context.update({"id": "CURRENT-CONTEXT-226", "recordedAtUtc": timestamp, "sourceCommit": head,
        "sourceBranch": branch, "sourceAuthority": AUTH,
        "targetGroup": {"group": "rank9-planar-gates5", "pendingIds": TARGET_IDS, "count": 2},
        "currentIndexCounts": index["authoredCounts"],
        "currentPendingAudit": {"path": PENDING225.relative_to(ROOT).as_posix(), "bytes": len(PENDING225.read_bytes()),
            "sha256": sha(PENDING225.read_bytes()), "pendingCount": pending["pendingCount"]},
        "sourceRefresh": {"sourceFileCount": len(rows), "changedSinceHistoricalCandidate": changed},
        "latestCurrentReturn": {"return": 225, "group": "rank9-knowledge-revelation5", "acceptedIds": [],
            "appliedIds": [], "heldIds": ["faction-omniscience-supreme"], "blockerIds": ["KR198-B01"],
            "archive": info(RETURN225_ZIP), "delivery": info(RETURN225_DELIVERY),
            "independentAudit": info(RETURN225_AUDIT), "receipt": info(RETURN225_RECEIPT)},
        "priorPlanarGateReturn200": {"acceptedIds": CLOSED_IDS, "appliedIds": CLOSED_IDS,
            "audit": info(RETURN200_AUDIT), "application": info(RETURN200_APPLICATION),
            "decision": info(RETURN200_DECISION), "doNotReopen": True}})
    candidate["latestCurrentReturn"] = context["latestCurrentReturn"]
    candidate["priorPlanarGateReturn200"] = context["priorPlanarGateReturn200"]

    context["retainedNamedBlockersOutsideScope"]["retainedReturn225Blockers"] = ["KR198-B01"]
    context["qualification"] = ("Only banishment-gate and conjure-demiplane-fortress are pending in this current group. "
        "Gate, Absolute Gate and Planar Sanctuary were accepted/applied exactly in Return200 and are closed context; "
        "the held Knowledge/Revelation5 identity remains outside this group. Historical broad questions are preserved but do not reopen closed identities.")

    # Refresh every historical current/source member against this checkout and add current decision provenance.
    refreshed: dict[str, bytes] = {}
    for name, prior_bytes in old_members.items():
        if name.startswith("current/") or name.startswith("sources_current/"):
            rel = name.split("/", 1)[1]
            refreshed[name] = (ROOT / rel).read_bytes()
        elif name == "CURRENT_SOURCE_CONFERENCE_CANDIDATE_199.json":
            continue
        elif name == "CURRENT_CONTEXT_199.json":
            continue
        elif name == "REQUEST_199.txt":
            refreshed["HISTORICAL_REQUEST_199.txt"] = prior_bytes
        else:
            refreshed[name] = prior_bytes
    refreshed["HISTORICAL_CURRENT_SOURCE_CONFERENCE_CANDIDATE_199.json"] = old_members["CURRENT_SOURCE_CONFERENCE_CANDIDATE_199.json"]
    refreshed["CURRENT_SOURCE_CONFERENCE_CANDIDATE_226.json"] = dump_json(candidate)
    refreshed["CURRENT_CONTEXT_226.json"] = dump_json(context)
    request = (
        "GPT director - continue the ordinary spell review at current workspace authority 811 reviewed-applied / 37 pending / "
        "0 accepted-unapplied, with 535 complete standalone procedures and 173 scoped interfaces. Review exactly "
        "banishment-gate and conjure-demiplane-fortress, the only pending identities in rank9-planar-gates5.\n\n"
        f"Current source snapshot: branch {branch}, HEAD {head}, plus the exact working-tree overlay bindings in this packet. "
        "Use the refreshed source rows, current queue 226/handoff 226/pending audit, Return225 independent audit and receipt, "
        "and the Return200 accepted/applied context. The three identities gate, absolute-gate, and planar-sanctuary were "
        "accepted and applied in Return200; do not reopen them. faction-omniscience-supreme remains held under KR198-B01 "
        "outside this group; do not reopen it.\n\n"
        "Preserve all 30 original questions and nine future requirements as source context, but adjudicate only the two pending "
        "identities named above. Preserve every exact native placement, class route, cost, source entry, acquisition path, and "
        "prior lifecycle. Resolve only what current source evidence supports; do not invent cosmology, destinations, creatures, "
        "or events. Keep runtime, implementation, human-play, balance, cosmology, completion, and release gates closed.\n\n"
        "Return explicit per-identity accepted/applied/held decisions with exact blockers and minimum missing witnesses, all "
        "case and reversible-operation results, a sealed ZIP and matching DELIVERY.json, and the next pending group. Do not "
        "modify canonical files or run supplied programs. Apply no changes in this review."
    )
    refreshed["REQUEST_226.txt"] = request.encode("utf-8")
    refreshed["current/" + QUEUE226.relative_to(ROOT).as_posix()] = queue_bytes
    refreshed["current/" + HANDOFF226.relative_to(ROOT).as_posix()] = handoff_bytes
    refreshed["current/" + PENDING225.relative_to(ROOT).as_posix()] = PENDING225.read_bytes()
    evidence_files = {
        "evidence/RETURN225.zip": RETURN225_ZIP, "evidence/RETURN225_DELIVERY.json": RETURN225_DELIVERY,
        "evidence/RETURN225_INDEPENDENT_AUDIT.json": RETURN225_AUDIT, "evidence/RETURN225_RECEIPT.json": RETURN225_RECEIPT,
        "evidence/RETURN225_DIRECTOR_DECISION.json": RETURN225_DECISION,
        "evidence/PLANARGATES5_RETURN200_DELIVERY.json": RETURN200_DELIVERY,
        "evidence/PLANARGATES5_RETURN200_INDEPENDENT_AUDIT.json": RETURN200_AUDIT,
        "evidence/PLANARGATES5_RETURN200_APPLICATION.json": RETURN200_APPLICATION,
        "evidence/PLANARGATES5_RETURN200_DECISION.json": RETURN200_DECISION,
        "evidence/PLANARGATES5_RETURN200_RECEIPT.json": RETURN200_RECEIPT,
    }
    for name, path in evidence_files.items():
        refreshed[name] = path.read_bytes()
    for row in rows:
        refreshed["sources_current/" + row["path"]] = (ROOT / row["path"]).read_bytes()

    OUT.mkdir(parents=True)
    candidate_file_bytes = refreshed["CURRENT_SOURCE_CONFERENCE_CANDIDATE_226.json"]
    CANDIDATE_FILE.write_bytes(candidate_file_bytes)
    CONTEXT_FILE.write_bytes(refreshed["CURRENT_CONTEXT_226.json"])
    REQUEST_FILE.write_bytes(refreshed["REQUEST_226.txt"])
    member_rows = []
    with zipfile.ZipFile(ARCHIVE, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for name in sorted(refreshed):
            z.writestr(name, refreshed[name])
            b = refreshed[name]
            member_rows.append({"path": name, "bytes": len(b), "sha256": sha(b), "crc32": crc(b)})
        manifest = {"id": "RANK9-PLANARGATES5-CURRENT-SOURCE-226-MANIFEST",
            "memberCountExcludingSelf": len(member_rows), "sourceAuthority": AUTH,
            "scope": TARGET_IDS, "closedAcceptedIds": CLOSED_IDS, "members": member_rows}
        z.writestr("MANIFEST.json", dump_json(manifest))
    with zipfile.ZipFile(ARCHIVE) as z:
        assert z.testzip() is None and len(z.namelist()) == len(set(z.namelist()))
        assert z.read("CURRENT_SOURCE_CONFERENCE_CANDIDATE_226.json") == candidate_file_bytes
    archive_raw = ARCHIVE.read_bytes()
    delivery = {"id": "RANK9-PLANARGATES5-CURRENT-SOURCE-DELIVERY-226", "status": "PREPARED_UNSENT",
        "group": "rank9-planar-gates5", "pendingIds": TARGET_IDS, "accepted": False, "applied": False,
        "sourceBranch": branch, "sourceCommit": head, "sourceAuthority": AUTH,
        "closedAcceptedIds": CLOSED_IDS, "reviewedHeldOutsideScope": ["faction-omniscience-supreme"],
        "archive": {"path": ARCHIVE.name, "bytes": len(archive_raw), "sha256": sha(archive_raw), "crc32": crc(archive_raw)},
        "candidate": {"path": CANDIDATE_FILE.name, "bytes": len(candidate_file_bytes), "sha256": sha(candidate_file_bytes)},
        "context": {"path": CONTEXT_FILE.name, "bytes": len(refreshed["CURRENT_CONTEXT_226.json"]), "sha256": sha(refreshed["CURRENT_CONTEXT_226.json"])},
        "request": {"path": REQUEST_FILE.name, "bytes": len(refreshed["REQUEST_226.txt"]), "sha256": sha(refreshed["REQUEST_226.txt"])},
        "sourceBindings": len(rows), "archiveMembers": len(member_rows) + 1,
        "previousPlanarAcceptedApplied": CLOSED_IDS, "return225HeldIds": ["faction-omniscience-supreme"]}
    DELIVERY.write_bytes(dump_json(delivery))

    checks = [
        {"check": "Return225 passed 14 independent checks and its named next group is Planar Gates5", "passed": return225_audit["status"] == "PASS" and director_decision["nextPendingGroup"]["group"] == "rank9-planar-gates5"},
        {"check": "Return200 three accepted Planar Gates identities are applied and current index status is closed", "passed": return200_application["acceptedIds"] == CLOSED_IDS and return200_application["status"] == "APPLIED_THREE_EXACT_AUTHORED_PROCEDURES_WITH_TWO_RETAINED_BLOCKERS" and all(entries[x]["authoredStatus"] == "reviewed-authored-operational-playtest" for x in CLOSED_IDS)},
        {"check": "Only the exact two pending identities are targeted at authority 811/37/0", "passed": all(entries[x]["authoredStatus"] == "pending-authored-procedure" for x in TARGET_IDS) and pending["pendingCount"] == 37},
        {"check": "All historical source rows are refreshed from this working tree", "passed": len(rows) >= 132 and len(candidate["records"]) == 2 and candidate["sourceBindingRefresh"]["allSourceBindingsRefreshedFromCurrentWorkingTree"]},
        {"check": "Archive CRC, unique paths, exact source snapshot, and 226 queue/handoff are preserved", "passed": zipfile.is_zipfile(ARCHIVE) and len(member_rows) == len(set(r["path"] for r in member_rows)) and sha(QUEUE226.read_bytes()) == handoff["queue"]["sha256"]},
    ]
    prep = {"id": "RANK9-PLANARGATES5-SOURCE-PREPARATION-226", "recordedAtUtc": timestamp,
        "status": "PASS" if all(x["passed"] for x in checks) else "FAIL", "checks": checks,
        "sourceBranch": branch, "sourceCommit": head, "sourceAuthority": AUTH,
        "targetGroup": "rank9-planar-gates5", "pendingIds": TARGET_IDS, "closedAcceptedIds": CLOSED_IDS,
        "sourceBindingCount": len(rows), "changedSinceHistoricalCandidate": changed,
        "packet": delivery["archive"], "deliveryManifest": info(DELIVERY), "return225Audit": info(RETURN225_AUDIT),
        "return200Audit": info(RETURN200_AUDIT), "canonicalChanges": False}
    PREPARATION.write_bytes(dump_json(prep))
    packet_record = {"id": "RANK9PLANARGATES5-PACKET-226", "status": "PREPARED_UNSENT",
        "group": "rank9-planar-gates5", "pendingIds": TARGET_IDS, "closedAcceptedIds": CLOSED_IDS,
        "sourceAuthority": AUTH, "sourceBranch": branch, "sourceCommit": head,
        "archive": delivery["archive"], "deliveryManifest": info(DELIVERY),
        "candidate": info(CANDIDATE_FILE), "context": info(CONTEXT_FILE), "request": info(REQUEST_FILE),
        "sourceBindings": len(rows), "canonicalChanges": False}
    PACKET_RECORD.write_bytes(dump_json(packet_record))
    print(json.dumps({"status": prep["status"], "packet": delivery["archive"], "sourceBindings": len(rows),
        "archiveMembers": len(member_rows) + 1, "checks": checks}, indent=2))
    if prep["status"] != "PASS":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
