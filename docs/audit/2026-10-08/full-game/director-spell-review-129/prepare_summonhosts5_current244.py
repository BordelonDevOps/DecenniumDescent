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
OLD_PACKET = AUDIT / "rank9_summonhosts5_current_source_201_prepared/DD_Rank9_SummonHosts5_CurrentSource_201.zip"
R243 = AUDIT / "rank9_planargates5_return243_received"
R202 = AUDIT / "rank9_summonhosts5_return202_received"
OUT = AUDIT / "rank9_summonhosts5_current_source_244_prepared"
ARCHIVE = OUT / "DD_Rank9_SummonHosts5_CurrentSource_244.zip"
DELIVERY = OUT / "DD_Rank9_SummonHosts5_CurrentSource_244_DELIVERY.json"
CANDIDATE_FILE = OUT / "CURRENT_SOURCE_CONFERENCE_CANDIDATE_244.json"
CONTEXT_FILE = OUT / "CURRENT_CONTEXT_244.json"
REQUEST_FILE = OUT / "REQUEST_244.txt"
PREPARATION = AUDIT / "RANK9SUMMONHOSTS5_SOURCE_PREPARATION_244.json"
PACKET_RECORD = AUDIT / "RANK9SUMMONHOSTS5_PACKET_244.json"
PENDING244 = AUDIT / "CURRENT37_PENDING_IDENTITY_AUDIT_244.json"
QUEUE244 = AUDIT / "CURRENT_SPELL_QUEUE_244.json"
HANDOFF244 = AUDIT / "CURRENT_HANDOFF_244.json"
SNAPSHOT244 = AUDIT / "CURRENT_SPELL_REVIEW_SNAPSHOT_244.md"
START = ROOT / "START_HERE.md"
INDEX = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json"
CATALOG = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json"
QUEUE243 = AUDIT / "CURRENT_SPELL_QUEUE_243.json"
HANDOFF243 = AUDIT / "CURRENT_HANDOFF_243.json"
PENDING242 = AUDIT / "CURRENT37_PENDING_IDENTITY_AUDIT_242.json"
R243_ZIP = R243 / "DD_Rank9_PlanarGates2_Director_Return243_HELD.zip"
R243_DELIVERY = R243 / "DD_Rank9_PlanarGates2_Director_Return243_HELD_DELIVERY.json"
R243_AUDIT = AUDIT / "RANK9_PLANARGATES5_RETURN243_INDEPENDENT_AUDIT.json"
R243_RECEIPT = AUDIT / "RANK9_PLANARGATES5_RETURN243_RECEIPT.json"
R202_DELIVERY = R202 / "DD_Rank9_SummonHosts5_Director_Return202_DELIVERY.json"
R202_AUDIT = AUDIT / "RANK9_SUMMONHOSTS5_RETURN202_INDEPENDENT_AUDIT.json"
R202_RECEIPT = AUDIT / "RANK9_SUMMONHOSTS5_RETURN202_RECEIPT.json"
R202_DECISION = AUDIT / "RANK9_SUMMONHOSTS5_DIRECTOR_DECISION_202.json"
R202_APPLICATION = AUDIT / "RANK9_SUMMONHOSTS5_APPLICATION_202.json"
R202_ACCEPTANCE = AUDIT / "RANK9_SUMMONHOSTS5_EXACT_ACCEPTANCE_202.json"
R202_VALIDATION = AUDIT / "RANK9_SUMMONHOSTS5_APPLICATION_VALIDATION_202.json"
SUMMON202 = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_candidates/rank9summonhosts5_reviewed_202"
RECENT_HOLDS = [
    "docs/audit/2026-10-08/full-game/director-spell-review-129/rank9_agencycontrol9_return238_received/DD_Rank9_AgencyControl2_Director_Return238.zip",
    "docs/audit/2026-10-08/full-game/director-spell-review-129/rank9_agencycontrol9_return238_received/DD_Rank9_AgencyControl2_Director_Return238_DELIVERY.json",
    "docs/audit/2026-10-08/full-game/director-spell-review-129/RANK9_AGENCYCONTROL9_RETURN238_INDEPENDENT_AUDIT.json",
    "docs/audit/2026-10-08/full-game/director-spell-review-129/RANK9_AGENCYCONTROL9_RETURN238_RECEIPT.json",
    "docs/audit/2026-10-08/full-game/director-spell-review-129/rank9_timefate6_return239_received/DD_Rank9_TimeFate4_Director_Return239_HELD.zip",
    "docs/audit/2026-10-08/full-game/director-spell-review-129/rank9_timefate6_return239_received/DD_Rank9_TimeFate4_Director_Return239_HELD_DELIVERY.json",
    "docs/audit/2026-10-08/full-game/director-spell-review-129/RANK9_TIMEFATE6_RETURN239_INDEPENDENT_AUDIT.json",
    "docs/audit/2026-10-08/full-game/director-spell-review-129/RANK9_TIMEFATE6_RETURN239_RECEIPT.json",
    "docs/audit/2026-10-08/full-game/director-spell-review-129/rank9_castingcost5_return240_received/DD_Rank9_UnholyAscendance_Director_Return240_HELD.zip",
    "docs/audit/2026-10-08/full-game/director-spell-review-129/rank9_castingcost5_return240_received/DD_Rank9_UnholyAscendance_Director_Return240_HELD_DELIVERY.json",
    "docs/audit/2026-10-08/full-game/director-spell-review-129/RANK9_CASTINGCOST5_RETURN240_INDEPENDENT_AUDIT.json",
    "docs/audit/2026-10-08/full-game/director-spell-review-129/RANK9_CASTINGCOST5_RETURN240_RECEIPT.json",
    "docs/audit/2026-10-08/full-game/director-spell-review-129/rank9_memorydenial6_return241_received/DD_Rank9_MemoryDenial2_Director_Return241_HELD.zip",
    "docs/audit/2026-10-08/full-game/director-spell-review-129/rank9_memorydenial6_return241_received/DD_Rank9_MemoryDenial2_Director_Return241_HELD_DELIVERY.json",
    "docs/audit/2026-10-08/full-game/director-spell-review-129/RANK9_MEMORYDENIAL6_RETURN241_INDEPENDENT_AUDIT.json",
    "docs/audit/2026-10-08/full-game/director-spell-review-129/RANK9_MEMORYDENIAL6_RETURN241_RECEIPT.json",
    "docs/audit/2026-10-08/full-game/director-spell-review-129/rank9_knowledgerevelation5_return242_received/DD_Rank9_FactionOmniscienceSupreme_Director_Return242_HELD.zip",
    "docs/audit/2026-10-08/full-game/director-spell-review-129/rank9_knowledgerevelation5_return242_received/DD_Rank9_FactionOmniscienceSupreme_Director_Return242_HELD_DELIVERY.json",
    "docs/audit/2026-10-08/full-game/director-spell-review-129/RANK9_KNOWLEDGEREVELATION5_RETURN242_INDEPENDENT_AUDIT.json",
    "docs/audit/2026-10-08/full-game/director-spell-review-129/RANK9_KNOWLEDGEREVELATION5_RETURN242_RECEIPT.json",
    "docs/audit/2026-10-08/full-game/director-spell-review-129/rank9_planargates5_return243_received/DD_Rank9_PlanarGates2_Director_Return243_HELD.zip",
    "docs/audit/2026-10-08/full-game/director-spell-review-129/rank9_planargates5_return243_received/DD_Rank9_PlanarGates2_Director_Return243_HELD_DELIVERY.json",
    "docs/audit/2026-10-08/full-game/director-spell-review-129/RANK9_PLANARGATES5_RETURN243_INDEPENDENT_AUDIT.json",
    "docs/audit/2026-10-08/full-game/director-spell-review-129/RANK9_PLANARGATES5_RETURN243_RECEIPT.json",
]
AUTH = {"reviewedApplied": 811, "pending": 37, "acceptedUnapplied": 0,
        "completeStandaloneProcedures": 535, "scopedInterfaces": 173}
GROUP = "rank9-summon-hosts5"
TARGETS = ["summon-elemental-avatar", "summon-herald-of-the-planes", "summon-avatar-of-decay"]
CLOSED = ["conjure-magmatic-wyrm", "planar-army"]
BLOCKERS = {"summon-elemental-avatar": ["SH202-B01"], "summon-herald-of-the-planes": ["SH202-B02"],
            "summon-avatar-of-decay": ["SH202-B03"]}


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def crc(raw: bytes) -> str:
    return f"{zlib.crc32(raw) & 0xffffffff:08x}"


def dump(value: object) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8")


def read(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def info(path: Path, raw: bytes | None = None) -> dict:
    b = path.read_bytes() if raw is None else raw
    return {"path": path.relative_to(ROOT).as_posix(), "bytes": len(b), "sha256": sha(b), "crc32": crc(b)}


def binding(path: str, raw: bytes) -> dict:
    blob = hashlib.sha1(b"blob " + str(len(raw)).encode("ascii") + b"\0" + raw).hexdigest()
    return {"path": path, "bytes": len(raw), "sha256": sha(raw), "gitBlobSHA1": blob}


def main() -> None:
    if any(p.exists() for p in (OUT, PREPARATION, PACKET_RECORD, PENDING244, QUEUE244, HANDOFF244, SNAPSHOT244)):
        raise FileExistsError("Refusing to overwrite packet244 outputs")
    index, catalog = read(INDEX), read(CATALOG)
    queue243, handoff243, pending = read(QUEUE243), read(HANDOFF243), read(PENDING242)
    r243_delivery, r243_audit, r243_receipt = read(R243_DELIVERY), read(R243_AUDIT), read(R243_RECEIPT)
    r202_receipt = read(R202_RECEIPT)
    assert queue243["currentAuthority"] == handoff243["currentAuthority"] == AUTH
    assert r243_delivery["authority"] == AUTH and r243_delivery["accepted"] is False
    assert r243_audit["status"] == r243_receipt["status"] == "PASS" and r243_audit["checksPassed"] == 17
    assert r243_audit["heldIds"] == ["banishment-gate", "conjure-demiplane-fortress"]
    assert r202_receipt["acceptedIds"] == CLOSED and set(r202_receipt["unacceptedIds"]) == set(TARGETS)
    assert index["authoredCounts"] == {"reviewed": 811, "pending": 37}
    assert index["representationCounts"]["completeReviewedStandaloneProcedures"] == 535
    entries = {x["id"]: x for x in index["entries"]}
    spells = {x["id"]: x for x in catalog["spells"]}
    live_pending = sorted(x["id"] for x in index["entries"] if x.get("authoredStatus") == "pending-authored-procedure")
    assert live_pending == sorted(pending["pendingIds"]) and len(live_pending) == 37
    assert set(TARGETS) <= set(live_pending)
    assert all(entries[s]["sourceStatus"] == "blocked-pending-operational-review" for s in TARGETS)
    assert all(entries[s]["authoredStatus"] == "reviewed-authored-operational-playtest" for s in CLOSED)
    assert all(s in spells for s in TARGETS + CLOSED)
    head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    branch = subprocess.check_output(["git", "branch", "--show-current"], cwd=ROOT, text=True).strip()
    assert branch == "main"
    now = datetime.now(timezone.utc).isoformat()

    # Current pending audit is re-bound to the current index/catalog without changing its 37 identities.
    p244 = copy.deepcopy(pending)
    p244.update({"id": "CURRENT37-PENDING-IDENTITY-AUDIT-244", "recordedAtUtc": now,
        "status": "PASSED_EXACT_CURRENT_INDEX_PENDING_SET_AFTER_RETURN243", "authority": AUTH,
        "indexBinding": info(INDEX), "catalogBinding": info(CATALOG),
        "auditedReturn243": {"heldIds": ["banishment-gate", "conjure-demiplane-fortress"],
            "blockers": {"banishment-gate": ["PG200-B03", "PG200-B04"], "conjure-demiplane-fortress": ["PG200-B06"]},
            "independentAudit": info(R243_AUDIT), "authorityUnchanged": AUTH},
        "preparedNextGroup": {"group": GROUP, "pendingIds": TARGETS, "pendingCount": 3,
            "status": "FRESH_CURRENT_SOURCE_PACKET_244_PREPARED_UNSENT"}})
    pbytes = dump(p244)
    PENDING244.write_bytes(pbytes)
    packet_rel = "docs/audit/2026-10-08/full-game/director-spell-review-129/rank9_summonhosts5_current_source_244_prepared/DD_Rank9_SummonHosts5_CurrentSource_244.zip"

    q = copy.deepcopy(queue243)
    q.update({"id": "SPELL-REVIEW-QUEUE-244", "recordedAtUtc": now, "supersedesQueue": info(QUEUE243),
        "nextGroup": GROUP, "packetStatus": "RANK9_SUMMONHOSTS5_PACKET_244_PREPARED_UNSENT_811_37"})
    for row in q["currentPendingGroups"]:
        if row["group"] == "rank9-planar-gates5":
            row.update({"status": "HELD_RETURN243_INDEPENDENTLY_AUDITED", "freshPacketRequiredForCurrentAuthority": True,
                "lastDirectorReturn": {"return": 243, "acceptedIds": [], "appliedIds": [],
                    "heldIds": ["banishment-gate", "conjure-demiplane-fortress"],
                    "blockers": {"banishment-gate": ["PG200-B03", "PG200-B04"], "conjure-demiplane-fortress": ["PG200-B06"]},
                    "independentAudit": info(R243_AUDIT)}})
        if row["group"] == GROUP:
            row.update({"status": "FRESH_CURRENT_PACKET_244_PREPARED_UNSENT_811_37", "pendingIds": TARGETS,
                "pendingCount": 3, "freshPacketRequiredForCurrentAuthority": True,
                "preparedPacket": {"path": packet_rel, "status": "PREPARED_UNSENT"},
                "lastDirectorReturn": {"return": 202, "acceptedIds": CLOSED, "appliedIds": CLOSED,
                    "heldIds": TARGETS, "blockers": BLOCKERS, "independentAudit": info(R202_AUDIT)}})
    next_row = next(x for x in q["currentPendingGroups"] if x["group"] == GROUP)
    q["next"] = {"group": GROUP, "pendingIds": TARGETS, "pendingCount": 3,
        "status": "CURRENT_SOURCE_PACKET_PREPARED_UNSENT", "freshPacketRequiredForCurrentAuthority": True,
        "historicalCandidate": next_row.get("candidate"), "historicalArchive": next_row.get("archive"), "packetPath": packet_rel}
    q["nextSuggestedGroups"] = [copy.deepcopy(next_row)]
    q["pendingIdentityAudit"] = {"id": p244["id"], "path": PENDING244.relative_to(ROOT).as_posix(),
        "pendingCount": 37, "sha256": sha(pbytes)}
    q["currentReturnAudit"], q["currentReturnDelivery"], q["currentReturnArchive"] = info(R243_AUDIT), info(R243_DELIVERY), info(R243_ZIP)
    q["currentReturnReceipt"] = info(R243_RECEIPT)
    q["lastReviewedBatch"] = {"return": 243, "group": "rank9-planar-gates5", "acceptedIds": [], "appliedIds": [],
        "heldIds": ["banishment-gate", "conjure-demiplane-fortress"],
        "blockers": {"banishment-gate": ["PG200-B03", "PG200-B04"], "conjure-demiplane-fortress": ["PG200-B06"]},
        "independentAudit": info(R243_AUDIT)}
    q["currentPacket"] = q["currentPacketDelivery"] = q["currentPreparation"] = None
    qbytes = dump(q)
    QUEUE244.write_bytes(qbytes)

    h = copy.deepcopy(handoff243)
    h.update({"id": "CURRENT-HANDOFF-244", "recordedAtUtc": now,
        "status": "RETURN243_AUDITED_HELD_NEXT_SUMMONHOSTS5_PACKET_244_PREPARED_UNSENT_811_37"})
    h["latestBatch"] = {"return": 243, "group": "rank9-planar-gates5", "ids": ["banishment-gate", "conjure-demiplane-fortress"],
        "acceptedIds": [], "appliedIds": [], "heldIds": ["banishment-gate", "conjure-demiplane-fortress"],
        "blockers": {"banishment-gate": ["PG200-B03", "PG200-B04"], "conjure-demiplane-fortress": ["PG200-B06"]},
        "independentAudit": info(R243_AUDIT)}
    h["nextStep"] = {"group": GROUP, "pendingIds": TARGETS, "pendingCount": 3,
        "status": "CURRENT_SOURCE_PACKET_244_PREPARED_UNSENT_AT_AUTHORITY_811_37_0", "freshPacketRequiredForCurrentAuthority": True,
        "candidate": next_row.get("candidate"), "archive": next_row.get("archive"), "packetPath": packet_rel}
    h["nextGroup"], h["nextPendingCount"] = GROUP, 3
    h["pendingIdentityAudit"] = {"id": p244["id"], "path": PENDING244.relative_to(ROOT).as_posix(), "pendingCount": 37, "sha256": sha(pbytes)}
    h["queue"] = {"path": QUEUE244.relative_to(ROOT).as_posix(), "bytes": len(qbytes), "sha256": sha(qbytes), "crc32": crc(qbytes)}
    h["currentQueueBinding"] = copy.deepcopy(h["queue"])
    h["appliedThisStep"] = {"return": 243, "group": "rank9-planar-gates5", "ids": ["banishment-gate", "conjure-demiplane-fortress"],
        "acceptedIds": [], "appliedIds": [], "heldIds": ["banishment-gate", "conjure-demiplane-fortress"],
        "blockers": {"banishment-gate": ["PG200-B03", "PG200-B04"], "conjure-demiplane-fortress": ["PG200-B06"]},
        "sourceAuthorityBefore": AUTH, "sourceAuthorityAfter": AUTH, "directorReturn": info(R243_ZIP),
        "deliveryManifest": info(R243_DELIVERY), "independentAudit": info(R243_AUDIT), "auditReceipt": info(R243_RECEIPT), "exactAcceptance": False}
    h["unacceptedThisStep"] = {"ids": ["banishment-gate", "conjure-demiplane-fortress"],
        "blockers": {"banishment-gate": ["PG200-B03", "PG200-B04"], "conjure-demiplane-fortress": ["PG200-B06"]}, "retainedInPendingSet": True}
    h["currentReturnBinding"], h["currentReturnDelivery"], h["currentReturnAudit"], h["currentReturnReceipt"] = info(R243_ZIP), info(R243_DELIVERY), info(R243_AUDIT), info(R243_RECEIPT)
    h["currentPreparation"] = h["currentPacket"] = h["currentPacketDelivery"] = None
    h["nextPreparedRequest"] = {"group": GROUP, "pendingIds": TARGETS, "pendingCount": 3,
        "status": "CURRENT_SOURCE_PACKET_244_PREPARED_UNSENT", "freshPacketRequiredForCurrentAuthority": True, "packetPath": packet_rel}
    h["resumePriority"] = "Submit the fresh packet for exactly the three pending Summon Hosts identities; keep the two Return202 acceptances closed, audit the response, and apply only exact accepted identities."
    hbytes = dump(h)
    HANDOFF244.write_bytes(hbytes)

    start_lines = START.read_text(encoding="utf-8-sig").splitlines()
    start_lines[0] = ("**Current ordinary spell-review handoff [244](docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT_HANDOFF_244.json):** "
        "Authority remains **811 reviewed-applied / 37 pending / 0 accepted-unapplied**. Return243 held the two Planar Gates identities and passed an independent 17-check audit. "
        "A fresh Rank9 Summon Hosts5 packet for `summon-elemental-avatar`, `summon-herald-of-the-planes`, and `summon-avatar-of-decay` is prepared for GPT. "
        "Return202 acceptances `conjure-magmatic-wyrm` and `planar-army` remain closed. See [packet record](docs/audit/2026-10-08/full-game/director-spell-review-129/RANK9SUMMONHOSTS5_PACKET_244.json).")
    START.write_text("\n".join(start_lines) + "\n", encoding="utf-8", newline="\n")

    # Rebind the historical 210 source rows to this checkout and filter the old five-ID proposal to the three live pending IDs.
    with zipfile.ZipFile(OLD_PACKET) as old:
        historical = json.loads(old.read("CURRENT_SOURCE_CONFERENCE_CANDIDATE_201.json"))
        old_context = json.loads(old.read("CURRENT_CONTEXT_201.json"))
        old_members = {n: old.read(n) for n in old.namelist() if n != "MANIFEST.json"}
    historical_by_id = {x["spellId"]: x for x in historical["records"]}
    assert set(TARGETS + CLOSED) <= set(historical_by_id)
    candidate = copy.deepcopy(historical)
    candidate.update({"id": "CURRENT-SOURCE-CONFERENCE-CANDIDATE-244", "recordedAtUtc": now,
        "status": "PREPARED_CURRENT_AUTHORITY_811_37_EXACT_THREE_PENDING_SUMMON_HOSTS_IDENTITIES",
        "currentSourceCommit": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),
        "currentBranch": "main", "currentAuthority": AUTH, "countsUnchanged": index["authoredCounts"],
        "currentPendingGroup": {"group": GROUP, "spellIds": TARGETS, "count": 3},
        "closedAcceptedSpellIds": CLOSED,
        "closedAcceptedSpellDecisionBinding": {"return": 202, "acceptedIds": CLOSED, "appliedIds": CLOSED,
            "decisionPath": R202_DECISION.relative_to(ROOT).as_posix(), "applicationPath": R202_APPLICATION.relative_to(ROOT).as_posix(),
            "exactAcceptancePath": R202_ACCEPTANCE.relative_to(ROOT).as_posix(), "auditPath": R202_AUDIT.relative_to(ROOT).as_posix(), "doNotReopen": True},
        "previousReturn243Binding": {"archive": info(R243_ZIP), "delivery": info(R243_DELIVERY),
            "independentAudit": info(R243_AUDIT), "receipt": info(R243_RECEIPT), "outsideScope": True}})
    candidate["records"] = [copy.deepcopy(historical_by_id[s]) for s in TARGETS]
    for row in candidate["records"]:
        sid = row["spellId"]
        row["currentIndexEntry"] = copy.deepcopy(entries[sid])
        row["completeCurrentCatalogSourceAndAccess"] = copy.deepcopy(spells[sid])
        row["status"] = "Pending current identity; reassess each SH202 blocker only against exact source-qualified evidence."
        row["closedAcceptedSpellIds"] = CLOSED
    history_rows = historical["sourceBindings"]
    extra_paths = ["START_HERE.md", INDEX.relative_to(ROOT).as_posix(), CATALOG.relative_to(ROOT).as_posix(),
        PENDING244.relative_to(ROOT).as_posix(), QUEUE244.relative_to(ROOT).as_posix(), HANDOFF244.relative_to(ROOT).as_posix(),
        QUEUE243.relative_to(ROOT).as_posix(), HANDOFF243.relative_to(ROOT).as_posix(), PENDING242.relative_to(ROOT).as_posix(),
        "docs/audit/2026-10-08/full-game/director-spell-review-129/RANK9PLANARGATES5_PACKET_243_SUBMISSION.json",
        "docs/audit/2026-10-08/full-game/director-spell-review-129/RANK9PLANARGATES5_PACKET_243.json",
        R243_AUDIT.relative_to(ROOT).as_posix(), R243_RECEIPT.relative_to(ROOT).as_posix(),
        R202_AUDIT.relative_to(ROOT).as_posix(), R202_RECEIPT.relative_to(ROOT).as_posix(),
        R202_DECISION.relative_to(ROOT).as_posix(), R202_APPLICATION.relative_to(ROOT).as_posix(),
        R202_ACCEPTANCE.relative_to(ROOT).as_posix(), R202_VALIDATION.relative_to(ROOT).as_posix(),
        R202_DELIVERY.relative_to(ROOT).as_posix(),
        "docs/audit/2026-10-08/full-game/director-spell-review-129/RANK9SUMMONHOSTS5_PACKET_201.json",
        "docs/audit/2026-10-08/full-game/director-spell-review-129/RANK9SUMMONHOSTS5_NEXT_CONFERENCE_NOTES_129.json"]
    extra_paths += [p.relative_to(ROOT).as_posix() for p in sorted(SUMMON202.rglob("*")) if p.is_file()]
    extra_paths += RECENT_HOLDS
    source_paths = sorted(set(r["path"] for r in history_rows) | set(extra_paths))
    source_bytes = {p: (ROOT / p).read_bytes() for p in source_paths}
    rows = [binding(p, source_bytes[p]) for p in source_paths]
    old_hashes = {r["path"]: (r["bytes"], r["sha256"]) for r in history_rows}
    changed = [p for p in old_hashes if (len(source_bytes[p]), sha(source_bytes[p])) != old_hashes[p]]
    candidate["historicalSourceBindings"] = copy.deepcopy(history_rows)
    candidate["sourceBindings"] = rows
    candidate["sourceBindingRefresh"] = {"historicalSourceFiles": len(history_rows), "sourceFiles": len(rows),
        "changedSinceHistoricalCandidate": len(changed), "changedPaths": changed[:100],
        "allSourceBindingsRefreshedFromCurrentWorkingTree": True, "exactOverlayBoundBySHA256AndGitBlobSHA1": True}
    candidate["currentPendingIdentityAudit"] = info(PENDING244, pbytes)
    context = copy.deepcopy(old_context)
    context.update({"id": "CURRENT-CONTEXT-244", "recordedAtUtc": now, "sourceBranch": "main",
        "sourceCommit": candidate["currentSourceCommit"], "sourceAuthority": AUTH,
        "targetGroup": {"group": GROUP, "pendingIds": TARGETS, "count": 3},
        "currentPendingAudit": info(PENDING244, pbytes), "currentQueue": info(QUEUE244, qbytes),
        "currentHandoff": info(HANDOFF244, hbytes), "currentIndexCounts": index["authoredCounts"],
        "return202AcceptedApplied": {"acceptedIds": CLOSED, "appliedIds": CLOSED, "doNotReopen": True,
            "decision": info(R202_DECISION), "application": info(R202_APPLICATION), "audit": info(R202_AUDIT), "receipt": info(R202_RECEIPT)},
        "return243AuditedOutsideScope": {"heldIds": ["banishment-gate", "conjure-demiplane-fortress"],
            "audit": info(R243_AUDIT), "receipt": info(R243_RECEIPT)},
        "sourceBindingRefresh": candidate["sourceBindingRefresh"]})
    context["qualification"] = ("Review only the three pending Summon Hosts identities. Return202's conjure-magmatic-wyrm and planar-army acceptances are closed. "
        "Keep the 32 original questions, two focused addenda, and eight future requirements as context. Reassess source blockers; invent no actors, acquired extra-turn sources, damage, events, or history.")

    request = (
        "GPT director - continue the ordinary spell review at current workspace authority 811 reviewed-applied / 37 pending / 0 accepted-unapplied, "
        "with 535 complete standalone procedures and 173 scoped interfaces. Review exactly summon-elemental-avatar, summon-herald-of-the-planes, "
        "and summon-avatar-of-decay, the only pending identities in rank9-summon-hosts5.\n\n"
        f"Current source snapshot: branch main, HEAD {candidate['currentSourceCommit']}, plus exact working-tree overlay bindings in this packet. Use the refreshed source rows, queue 244/handoff 244/pending audit, "
        "Return202 exact acceptance/application/audit/receipt, and Return243 independent audit/receipt. conjure-magmatic-wyrm and planar-army were accepted and applied exactly in Return202; do not reopen them. "
        "The three target IDs remain pending under SH202-B01/B02/B03; reassess each against current evidence instead of carrying blockers forward mechanically. Keep all other holds outside scope: Return238 AG190-B01/B02; Return239 TF192-B01/B02/B04/B05; Return240 CC194-B04; Return241 MD196-B01/B02; Return242 KR198-B01; and Return243 PG200-B03/B04/B06.\n\n"
        "Preserve all 32 original questions, two focused addenda, and eight future requirements as source context, but adjudicate only the three named pending identities. Preserve exact native placement, class route, cost, source entry, acquisition path and prior lifecycle. "
        "Resolve only what current source evidence supports; do not invent extra-turn providers, damage, actors, control events or acquisition histories. Keep runtime, implementation, human-play, balance, cosmology, completion and release gates closed.\n\n"
        "Return explicit per-identity accepted/applied/held decisions with exact blockers and minimum missing witnesses, all case and reversible-operation results, a sealed ZIP and matching DELIVERY.json, and the next pending group. "
        "Do not modify canonical files or run supplied programs. Apply no changes in this review."
    )

    # Refresh all prior packet current/source copies and add the new Return243 and Return202 evidence.
    members: dict[str, bytes] = {}
    for name, prior in old_members.items():
        if name.startswith("current/") or name.startswith("sources_current/"):
            rel = name.split("/", 1)[1]
            path = ROOT / rel
            members[name] = path.read_bytes() if path.is_file() else prior
        elif name in {"CURRENT_SOURCE_CONFERENCE_CANDIDATE_201.json", "CURRENT_CONTEXT_201.json", "REQUEST_201.txt"}:
            continue
        else:
            members[name] = prior
    members["HISTORICAL_CURRENT_SOURCE_CONFERENCE_CANDIDATE_201.json"] = old_members["CURRENT_SOURCE_CONFERENCE_CANDIDATE_201.json"]
    members["HISTORICAL_CURRENT_CONTEXT_201.json"] = old_members["CURRENT_CONTEXT_201.json"]
    members["HISTORICAL_REQUEST_201.txt"] = old_members["REQUEST_201.txt"]
    members["CURRENT_SOURCE_CONFERENCE_CANDIDATE_244.json"] = dump(candidate)
    members["CURRENT_CONTEXT_244.json"] = dump(context)
    members["REQUEST_244.txt"] = request.encode("utf-8")
    members["current/" + PENDING244.relative_to(ROOT).as_posix()] = pbytes
    members["current/" + QUEUE244.relative_to(ROOT).as_posix()] = qbytes
    members["current/" + HANDOFF244.relative_to(ROOT).as_posix()] = hbytes
    for p, raw in source_bytes.items():
        members["sources_current/" + p] = raw
    evidence = {
        "evidence/RETURN243.zip": R243_ZIP, "evidence/RETURN243_DELIVERY.json": R243_DELIVERY,
        "evidence/RETURN243_INDEPENDENT_AUDIT.json": R243_AUDIT, "evidence/RETURN243_RECEIPT.json": R243_RECEIPT,
        "evidence/RETURN202_DELIVERY.json": R202_DELIVERY, "evidence/RETURN202_INDEPENDENT_AUDIT.json": R202_AUDIT,
        "evidence/RETURN202_RECEIPT.json": R202_RECEIPT, "evidence/RETURN202_DIRECTOR_DECISION.json": R202_DECISION,
        "evidence/RETURN202_APPLICATION.json": R202_APPLICATION, "evidence/RETURN202_EXACT_ACCEPTANCE.json": R202_ACCEPTANCE,
        "evidence/RETURN202_APPLICATION_VALIDATION.json": R202_VALIDATION,
    }
    for name, path in evidence.items():
        members[name] = path.read_bytes()
    for path in RECENT_HOLDS:
        members["evidence/recent_holds/" + path.replace("\\", "/")] = (ROOT / path).read_bytes()
    for p in sorted(SUMMON202.rglob("*")):
        if p.is_file():
            members["current/" + p.relative_to(ROOT).as_posix()] = p.read_bytes()

    OUT.mkdir(parents=True)
    CANDIDATE_FILE.write_bytes(members["CURRENT_SOURCE_CONFERENCE_CANDIDATE_244.json"])
    CONTEXT_FILE.write_bytes(members["CURRENT_CONTEXT_244.json"])
    REQUEST_FILE.write_bytes(members["REQUEST_244.txt"])
    manifest_rows = []
    with zipfile.ZipFile(ARCHIVE, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for name in sorted(members):
            raw = members[name]
            z.writestr(name, raw)
            manifest_rows.append({"path": name, "bytes": len(raw), "sha256": sha(raw), "crc32": crc(raw)})
        z.writestr("MANIFEST.json", dump({"id": "RANK9-SUMMON-HOSTS5-CURRENT-SOURCE-244-MANIFEST",
            "memberCountExcludingSelf": len(manifest_rows), "sourceAuthority": AUTH,
            "scope": TARGETS, "closedAcceptedIds": CLOSED, "members": manifest_rows}))
    with zipfile.ZipFile(ARCHIVE) as z:
        assert z.testzip() is None and len(z.namelist()) == len(set(z.namelist()))
        assert z.read("REQUEST_244.txt").decode("utf-8") == request
    raw = ARCHIVE.read_bytes()
    delivery = {"id": "RANK9-SUMMON-HOSTS5-CURRENT-SOURCE-DELIVERY-244", "status": "PREPARED_UNSENT",
        "group": GROUP, "pendingIds": TARGETS, "accepted": False, "applied": False,
        "sourceBranch": "main", "sourceCommit": candidate["currentSourceCommit"], "sourceAuthority": AUTH,
        "closedAcceptedIds": CLOSED, "outsideScopeHolds": {"faction-omniscience-supreme": ["KR198-B01"],
            "banishment-gate": ["PG200-B03", "PG200-B04"], "conjure-demiplane-fortress": ["PG200-B06"]},
        "archive": {"path": ARCHIVE.name, "bytes": len(raw), "sha256": sha(raw), "crc32": crc(raw)},
        "candidate": {"path": CANDIDATE_FILE.name, "bytes": CANDIDATE_FILE.stat().st_size, "sha256": sha(CANDIDATE_FILE.read_bytes())},
        "context": {"path": CONTEXT_FILE.name, "bytes": CONTEXT_FILE.stat().st_size, "sha256": sha(CONTEXT_FILE.read_bytes())},
        "request": {"path": REQUEST_FILE.name, "bytes": REQUEST_FILE.stat().st_size, "sha256": sha(REQUEST_FILE.read_bytes())},
        "sourceBindings": len(rows), "archiveMembers": len(manifest_rows) + 1,
        "return202AcceptedApplied": CLOSED, "return243HeldOutsideScope": ["banishment-gate", "conjure-demiplane-fortress"]}
    DELIVERY.write_bytes(dump(delivery))

    checks = [
        {"check": "Current index/pending authority is exactly 811/37/0 and all 37 IDs match", "passed": index["authoredCounts"] == {"reviewed": 811, "pending": 37} and live_pending == pending["pendingIds"]},
        {"check": "Only the three pending Summon Hosts IDs are in review scope", "passed": [x["spellId"] for x in candidate["records"]] == TARGETS},
        {"check": "Both Return202 acceptances remain applied, excluded and closed", "passed": r202_receipt["acceptedIds"] == CLOSED and not (set(CLOSED) & set(TARGETS))},
        {"check": "Return243 passed 17 independent checks and retains the two exact Planar holds outside scope", "passed": r243_audit["status"] == "PASS" and r243_audit["checksPassed"] == 17 and r243_audit["heldIds"] == ["banishment-gate", "conjure-demiplane-fortress"] and set(TARGETS).isdisjoint(r243_audit["heldIds"])},
        {"check": "All 210 historical source paths and added current artifacts are refreshed", "passed": len(historical["sourceBindings"]) == 210 and len(rows) >= 210 and all((ROOT / p).is_file() for p in source_paths)},
        {"check": "Packet ZIP member paths are unique, the archive is readable, and scope is in delivery", "passed": zipfile.is_zipfile(ARCHIVE) and len(manifest_rows) + 1 == len(set(manifest_rows[i]["path"] for i in range(len(manifest_rows)))) + 1 and delivery["pendingIds"] == TARGETS},
        {"check": "Queue/handoff 244 point to this group and preserve current authority", "passed": q["currentAuthority"] == h["currentAuthority"] == AUTH and q["next"]["group"] == h["nextStep"]["group"] == GROUP},
    ]
    prep = {"id": "RANK9-SUMMON-HOSTS5-SOURCE-PREPARATION-244", "recordedAtUtc": now,
        "status": "PASS" if all(c["passed"] for c in checks) else "FAIL", "checks": checks,
        "sourceBranch": "main", "sourceCommit": candidate["currentSourceCommit"], "sourceAuthority": AUTH,
        "targetGroup": GROUP, "pendingIds": TARGETS, "closedAcceptedIds": CLOSED,
        "historicalSourceBindingCount": len(historical["sourceBindings"]), "refreshedSourceBindingCount": len(rows),
        "changedSinceHistoricalCandidate": changed, "packet": delivery["archive"],
        "deliveryManifest": info(DELIVERY), "return202Audit": info(R202_AUDIT), "return243Audit": info(R243_AUDIT),
        "canonicalChanges": False}
    PREPARATION.write_bytes(dump(prep))
    PACKET_RECORD.write_bytes(dump({"id": "RANK9SUMMONHOSTS5-PACKET-244", "status": "PREPARED_UNSENT",
        "group": GROUP, "pendingIds": TARGETS, "closedAcceptedIds": CLOSED, "sourceAuthority": AUTH,
        "sourceBranch": "main", "sourceCommit": candidate["currentSourceCommit"], "archive": delivery["archive"],
        "deliveryManifest": info(DELIVERY), "candidate": info(CANDIDATE_FILE), "context": info(CONTEXT_FILE),
        "request": info(REQUEST_FILE), "sourceBindings": len(rows), "canonicalChanges": False}))
    SNAPSHOT244.write_text("# Current ordinary spell-review snapshot 244\n\n"
        "Return243 was independently audited and held only `banishment-gate` and `conjure-demiplane-fortress`; authority remains 811 reviewed/applied, 37 pending, 0 accepted-unapplied (535 complete standalone procedures; 173 scoped interfaces). "
        "Next is `rank9-summon-hosts5`, scoped to `summon-elemental-avatar`, `summon-herald-of-the-planes`, and `summon-avatar-of-decay`. "
        "Return202 acceptances `conjure-magmatic-wyrm` and `planar-army` remain applied and closed context.\n", encoding="utf-8", newline="\n")
    print(json.dumps({"status": prep["status"], "archive": delivery["archive"], "sourceBindings": len(rows),
        "members": delivery["archiveMembers"], "checks": checks}, indent=2))
    if prep["status"] != "PASS":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
