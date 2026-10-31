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
BASE = ROOT / "docs/audit/2026-10-08/full-game/director-spell-review-129"
FULL = ROOT / "docs/audit/2026-10-08/full-game"
GROUP, TARGETS = "rank9-death-recovery7", ["final-word"]
AUTH = {"reviewedApplied": 816, "pending": 32, "acceptedUnapplied": 0,
        "completeStandaloneProcedures": 540, "scopedInterfaces": 173}
CHAT = "https://chatgpt.com/g/g-p-67f17555a8dc8191a2b5b81e6d8adc12-dungeon-crawler/c/6adc506d-8770-83ea-b64c-0345d9b9b682"
INDEX = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json"
CATALOG = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json"
ACCESS = ROOT / "DescentReviewChanges/ReviewBible/data/director/spell_review/accepted_interface_registry_06.json"
WORK_QUEUE = ROOT / "DescentReviewChanges/ReviewBible/data/director/spell_review/remaining_work_queue_66.json"
Q278, H278, P278 = (BASE / n for n in ["CURRENT_SPELL_QUEUE_278.json", "CURRENT_HANDOFF_278.json", "CURRENT32_PENDING_IDENTITY_AUDIT_278.json"])
Q279, H279, P279 = (BASE / n for n in ["CURRENT_SPELL_QUEUE_279.json", "CURRENT_HANDOFF_279.json", "CURRENT32_PENDING_IDENTITY_AUDIT_279.json"])
RULING278 = BASE / "PSYCHICFEAR7_DIRECTOR_RULING_278.json"
CROSSCHECK278 = BASE / "PSYCHICFEAR7_DIRECTOR_RULING_278_CROSSCHECK.json"
PACKET278_AUDIT = BASE / "RANK9PSYCHICFEAR7_PACKET278_INDEPENDENT_AUDIT.json"
PACKET278_RECEIPT = BASE / "RANK9PSYCHICFEAR7_PACKET278_RECEIPT.json"
PRIOR_CANDIDATE = BASE / "rank9_deathrecovery7_current_source_235_prepared/CURRENT_SOURCE_CONFERENCE_CANDIDATE_235.json"
PRIOR_PACKET = BASE / "rank9_deathrecovery7_current_source_235_prepared/DD_Rank9_DeathRecovery7_CurrentSource_235.zip"
PRIOR_DELIVERY = BASE / "rank9_deathrecovery7_current_source_235_prepared/DD_Rank9_DeathRecovery7_CurrentSource_235_DELIVERY.json"
PRIOR_PACKET_AUDIT = BASE / "RANK9DEATHRECOVERY7_PACKET235_INDEPENDENT_AUDIT.json"
PRIOR_PACKET_RECEIPT = BASE / "RANK9DEATHRECOVERY7_PACKET235_RECEIPT.json"
RETURN235 = BASE / "rank9_deathrecovery7_return235_received/DD_Rank9_FinalWord_Director_Return235_HELD.zip"
RETURN235_DELIVERY = BASE / "rank9_deathrecovery7_return235_received/DD_Rank9_FinalWord_Director_Return235_HELD_DELIVERY.json"
RETURN235_AUDIT = BASE / "RANK9DEATHRECOVERY7_RETURN235_INDEPENDENT_AUDIT.json"
RETURN235_RECEIPT = BASE / "RANK9DEATHRECOVERY7_RETURN235_RECEIPT.json"
RETURN217 = BASE / "rank9_deathrecovery7_return217_received/DD_Rank9_DeathRecovery3_Director_Return217.zip"
RETURN217_DELIVERY = BASE / "rank9_deathrecovery7_return217_received/DD_Rank9_DeathRecovery3_Director_Return217_DELIVERY.json"
RETURN217_AUDIT = BASE / "rank9_deathrecovery7_return217_received/RETURN217_INDEPENDENT_AUDIT.json"
RETURN217_ROOT = BASE / "rank9_deathrecovery7_return217_received/extracted"
RETURN184_DELIVERY = BASE / "rank9_deathrecovery7_return184_received/DD_Rank9_DeathRecovery7_Director_Return184_DELIVERY.json"
RETURN184_AUDIT = BASE / "RANK9_DEATHRECOVERY7_RETURN184_INDEPENDENT_AUDIT.json"
RETURN184_DECISION = BASE / "RANK9_DEATHRECOVERY7_GPT_RETURN_184.json"
HIST_CANDIDATE = ROOT / "DescentReviewChanges/ReviewBible/data/director/spell_review/rank9_death_recovery_7_source_conference_01.json"
HIST_ARCHIVE = FULL / "DD_Rank9_Death_Recovery_7_Source_Conference_01.zip"
OUT = BASE / "rank9_deathrecovery7_current_source_279_prepared_review2"


def enc(x) -> bytes:
    return (json.dumps(x, ensure_ascii=False, indent=2) + "\n").encode("utf-8")


def read(path: Path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def crc(raw: bytes) -> str:
    return f"{zlib.crc32(raw) & 0xffffffff:08x}"


def info(path: Path, raw: bytes | None = None) -> dict:
    b = path.read_bytes() if raw is None else raw
    return {"path": path.relative_to(ROOT).as_posix(), "bytes": len(b), "sha256": sha(b), "crc32": crc(b)}


def safe(name: str) -> bool:
    p = PurePosixPath(name)
    return bool(name) and "\\" not in name and not p.is_absolute() and all(x not in ("", ".", "..") for x in p.parts)


def add(files: dict[str, bytes], name: str, raw: bytes) -> None:
    assert safe(name) and name not in files, name
    files[name] = raw


def main() -> None:
    assert not OUT.exists(), OUT
    branch = subprocess.check_output(["git", "branch", "--show-current"], cwd=ROOT, text=True).strip()
    head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    assert branch == "main", branch
    now = datetime.now(timezone.utc).isoformat()
    q, h, pending = read(Q279), read(H279), read(P279)
    assert q["currentAuthority"] == h["currentAuthority"] == pending["authority"] == AUTH
    assert q["nextGroup"] == GROUP and q["nextPendingIds"] == TARGETS
    assert q["status"].startswith(("RETURN278_AUDITED_HELD", "FINAL_WORD_PACKET279_PREPARED"))
    assert pending["pendingCount"] == len(pending["pendingIds"]) == 32 and "final-word" in pending["pendingIds"]
    index, catalog = read(INDEX), read(CATALOG)
    assert index["authoredCounts"] == {"reviewed": 816, "pending": 32}
    assert index["representationCounts"]["completeReviewedStandaloneProcedures"] == 540
    entries = {r["id"]: r for r in index["entries"]}
    spells = {r["id"]: r for r in catalog["spells"]}
    assert entries["final-word"]["authoredStatus"] == "pending-authored-procedure"
    assert entries["final-word"]["sourceStatus"] == "blocked-pending-operational-review"
    assert spells["final-word"]["operational"] is None

    q278 = read(BASE / "CURRENT_SPELL_QUEUE_278.json")
    group_row = next(r for r in q278["currentPendingGroups"] if r.get("group") == GROUP)
    hist_candidate_path = ROOT / group_row["candidate"]["path"]
    hist_archive_path = ROOT / group_row["archive"]["path"]
    historical_candidate = read(hist_candidate_path)
    prior_candidate = read(PRIOR_CANDIDATE)
    assert len(prior_candidate["sourceBindings"]) == 74
    prior_packet_audit, prior_packet_receipt = read(PRIOR_PACKET_AUDIT), read(PRIOR_PACKET_RECEIPT)
    return235_audit, return235_receipt = read(RETURN235_AUDIT), read(RETURN235_RECEIPT)
    return217_audit = read(RETURN217_AUDIT)
    return184_audit = read(RETURN184_AUDIT)
    assert prior_packet_audit["status"] == prior_packet_receipt["status"] == "PASS"
    assert return235_audit["status"] == return235_receipt["status"] == "PASS"
    assert return217_audit["status"] == return184_audit["status"] == "PASS"

    historical_source_bindings = prior_candidate.get("historicalSourceBindings", [])
    assert len(historical_source_bindings) == 74
    with zipfile.ZipFile(HIST_ARCHIVE) as old_zip:
        assert old_zip.testzip() is None
        source_bindings, sources_current, changed = [], {}, []
        for old in historical_source_bindings:
            rel = old["path"]
            old_bytes = old_zip.read("sources/" + rel)
            assert (len(old_bytes), sha(old_bytes)) == (old["bytes"], old["sha256"]), rel
            current = (ROOT / rel).read_bytes()
            row = {"path": rel, "bytes": len(current), "sha256": sha(current), "crc32": crc(current)}
            source_bindings.append(row)
            sources_current["sources_current/" + rel] = current
            if (len(current), sha(current)) != (old["bytes"], old["sha256"]):
                changed.append({"path": rel, "historicalBytes": old["bytes"], "historicalSha256": old["sha256"],
                                "currentBytes": len(current), "currentSha256": sha(current)})
    assert len(source_bindings) == len(sources_current) == 74

    current_candidate = copy.deepcopy(prior_candidate)
    current_candidate.update({
        "id": "CURRENT-SOURCE-CONFERENCE-CANDIDATE-279", "recordedAtUtc": now,
        "status": "PREPARED_CURRENT_AUTHORITY_816_32_EXACT_DEATH_RECOVERY7_FINAL_WORD_GROUP",
        "sourceCommitBase": head, "sourceBranch": branch, "currentWorkingTreeSnapshot": True,
        "currentAuthority": AUTH, "currentPendingGroup": {"group": GROUP, "spellIds": TARGETS, "count": 1},
        "currentReviewTargets": [{"spellId": "final-word", "currentIndexEntry": entries["final-word"],
                                  "completeCurrentCatalogSourceAndAccess": spells["final-word"],
                                  "status": "Pending at current 816/32/0 authority; sole review target."}],
        "sourceBindings": source_bindings,
        "sourceBindingRefresh": {"sourceFiles": 74, "changedSinceHistoricalCandidate": changed,
                                 "sourceContentsFromCurrentWorkingTree": True, "sourceCommitBase": head},
        "currentAuthorityEvidence": {"currentIndex": info(INDEX), "currentCatalog": info(CATALOG), "currentAccessRegistry": info(ACCESS),
             "currentWorkQueue": info(WORK_QUEUE), "parentQueue278": info(Q278), "parentHandoff278": info(H278),
             "parentPendingIdentityAudit278": info(P278), "psychicFearDirectorRuling278": info(RULING278),
             "psychicFearRulingCrosscheck278": info(CROSSCHECK278), "targetIdsStillPending": TARGETS},
        "lastTargetBlocker": {"id": "DR217-B01", "status": "REASSESS_FROM_FRESH_CURRENT_SOURCE",
             "sourceEvidenceRequired": "An exact source-qualified independent victim identity and lifecycle establishing that the actual soul is available for this capture, with actual custody/capture-bar/Hunt and summon-no-resource-farm facts. Ordinary class/body eligibility alone is insufficient. If no source supplies these facts, preserve the hold without inventing identity or soul availability."},
        "historicalWorkflow": {**prior_candidate.get("historicalWorkflow", {}),
             "priorPacket235": info(PRIOR_PACKET), "priorReturn235": info(RETURN235),
             "lastCurrentBatch278": info(RULING278), "currentFreshAssessmentRequired": True},
        "newRuleAdoptions": 0,
    })
    target_record = next(r for r in current_candidate["records"] if r.get("spellId") == "final-word")
    focused_questions = [r for r in current_candidate["questions"] if "final-word" in r.get("spellIds", [])]
    addendum = {
        "id": "DEATH279-ADD01", "spellIds": TARGETS,
        "request": "Reassess only the unresolved DR217-B01 positive branch against 816/32 current sources: cite an actual source-established identity/lifecycle satisfying victim eligibility, final death rather than prevention, available soul, custody/capture-bar/Hunt status and summon/no-resource-farm restrictions. Then determine if it can lawfully supply the already selected positive reserve/payment trace. Do not manufacture an NPC, infer soul availability from personhood/class/body/name, or treat source silence as positive evidence. If absent, hold with the narrowest missing witness. Preserve closed local design choices and all previously accepted identities.",
        "decisionSelected": False,
    }
    current_candidate["focusedCurrentAddendum"] = addendum
    current_candidate["currentReviewScope"] = {"group": GROUP, "spellIds": TARGETS, "priorDirectorBlocker": "DR217-B01",
                                                  "noOtherIdentityMayBeReopened": True,
                                                  "priorFocusedQuestionCount": len(focused_questions)}

    request_text = f"""REQUEST_279 — CURRENT-SOURCE REVIEW OF FINAL WORD ONLY

Director: GPT in Calibration review part 6.
Authority: 816 reviewed/applied, 32 pending, 0 accepted-unapplied; 540 complete standalone procedures; 173 scoped interfaces.
Exact target: final-word. No other identity is in scope.

Please review the candidate, the 74 refreshed current sources, audited Return184/Return217/Return235 history, and the exact preserved final-word cases. The ZIP carries the parent queue/handoff/pending snapshots 278 and the Return278 ruling; the separately attached final queue/handoff/pending snapshots 279 are authoritative for the current next target. Return235 is historical 811/37 and held final-word under DR217-B01; Packet278 held its three targets with no acceptance or application. Current source/index/catalog and the 816/32 snapshots govern.

Reassess the single unresolved positive branch: find and cite an actual source-established eligible victim/lifecycle with current body and HP, available soul, actual final death (not prevention), custody/capture-bar/Hunt status and summon/no-resource-farm facts; determine whether it can lawfully supply the already selected positive reserve/payment trace. Do not invent an NPC, identity or exception, or infer soul availability from personhood, class, body or spell name. If no admissible source exists, retain DR217-B01 and state the narrowest missing witness. Preserve accepted/applied doom, eternal-pact and all other closed identities.

Return a sealed decision ZIP and exact matching DELIVERY.json, explicitly naming acceptedIds, appliedIds, heldIds, blockers and the next group. No application or canonical/runtime/GitHub changes are requested. Any exact acceptance will be independently audited before application. Confirm the next ordered group.
"""

    files: dict[str, bytes] = {}
    for name, path in [("current/" + INDEX.relative_to(ROOT).as_posix(), INDEX),
                       ("current/" + CATALOG.relative_to(ROOT).as_posix(), CATALOG),
                       ("current/" + ACCESS.relative_to(ROOT).as_posix(), ACCESS),
                       ("current/" + WORK_QUEUE.relative_to(ROOT).as_posix(), WORK_QUEUE),
                       ("parent_snapshot/" + Q278.name, Q278),
                       ("parent_snapshot/" + H278.name, H278),
                       ("parent_snapshot/" + P278.name, P278),
                       ("parent_snapshot/CURRENT_SPELL_REVIEW_SNAPSHOT_278.md", BASE / "CURRENT_SPELL_REVIEW_SNAPSHOT_278.md"),
                       ("current/" + RULING278.relative_to(ROOT).as_posix(), RULING278),
                       ("current/" + CROSSCHECK278.relative_to(ROOT).as_posix(), CROSSCHECK278),
                       ("current/" + PACKET278_AUDIT.relative_to(ROOT).as_posix(), PACKET278_AUDIT),
                       ("current/" + PACKET278_RECEIPT.relative_to(ROOT).as_posix(), PACKET278_RECEIPT),
                       ("current/" + PRIOR_PACKET.relative_to(ROOT).as_posix(), PRIOR_PACKET),
                       ("current/" + PRIOR_DELIVERY.relative_to(ROOT).as_posix(), PRIOR_DELIVERY),
                       ("current/" + PRIOR_PACKET_AUDIT.relative_to(ROOT).as_posix(), PRIOR_PACKET_AUDIT),
                       ("current/" + PRIOR_PACKET_RECEIPT.relative_to(ROOT).as_posix(), PRIOR_PACKET_RECEIPT),
                       ("current/" + RETURN235.relative_to(ROOT).as_posix(), RETURN235),
                       ("current/" + RETURN235_DELIVERY.relative_to(ROOT).as_posix(), RETURN235_DELIVERY),
                       ("current/" + RETURN235_AUDIT.relative_to(ROOT).as_posix(), RETURN235_AUDIT),
                       ("current/" + RETURN235_RECEIPT.relative_to(ROOT).as_posix(), RETURN235_RECEIPT),
                       ("current/" + RETURN217_DELIVERY.relative_to(ROOT).as_posix(), RETURN217_DELIVERY),
                       ("current/" + RETURN217_AUDIT.relative_to(ROOT).as_posix(), RETURN217_AUDIT),
                       ("current/" + RETURN184_DELIVERY.relative_to(ROOT).as_posix(), RETURN184_DELIVERY),
                       ("current/" + RETURN184_AUDIT.relative_to(ROOT).as_posix(), RETURN184_AUDIT),
                       ("current/" + RETURN184_DECISION.relative_to(ROOT).as_posix(), RETURN184_DECISION)]:
        add(files, name, path.read_bytes())
    add(files, "current/CURRENT_SOURCE_CONFERENCE_CANDIDATE_279.json", enc(current_candidate))
    add(files, "current/REQUEST_279.txt", request_text.encode("utf-8"))
    for name, path in [("history/CURRENT_SOURCE_CONFERENCE_CANDIDATE_235.json", PRIOR_CANDIDATE),
                       ("history/DD_Rank9_DeathRecovery7_CurrentSource_235.zip", PRIOR_PACKET),
                       ("history/DD_Rank9_FinalWord_Director_Return235_HELD.zip", RETURN235),
                       ("history/DD_Rank9_FinalWord_Director_Return235_HELD_DELIVERY.json", RETURN235_DELIVERY),
                       ("history/RETURN235_INDEPENDENT_AUDIT.json", RETURN235_AUDIT),
                       ("history/RETURN235_RECEIPT.json", RETURN235_RECEIPT),
                       ("history/DD_Rank9_DeathRecovery3_Director_Return217_DELIVERY.json", RETURN217_DELIVERY),
                       ("history/RETURN217_INDEPENDENT_AUDIT.json", RETURN217_AUDIT),
                       ("history/RETURN184_DELIVERY.json", RETURN184_DELIVERY),
                       ("history/RETURN184_INDEPENDENT_AUDIT.json", RETURN184_AUDIT),
                       ("history/RETURN184_DIRECTOR_DECISION.json", RETURN184_DECISION),
                       ("history/SOURCE_CONFERENCE_01.zip", HIST_ARCHIVE),
                       ("history/SOURCE_CANDIDATE_01.json", HIST_CANDIDATE),
                       ("history/RETURN217_EXTRACTED_DIRECTOR_DECISION.json", RETURN217_ROOT / "DIRECTOR_DECISION.json"),
                       ("history/RETURN217_EXTRACTED_BLOCKERS.json", RETURN217_ROOT / "BLOCKERS.json"),
                       ("history/RETURN217_CASE_INDEX.json", RETURN217_ROOT / "CASE_INDEX.json"),
                       ("history/RETURN217_PROCEDURES.json", RETURN217_ROOT / "PROCEDURES.json"),
                       ("history/RETURN217_ORIGINAL_QUESTIONS.json", RETURN217_ROOT / "ORIGINAL_QUESTIONS_AND_OBLIGATIONS.json")]:
        add(files, name, path.read_bytes())
    with zipfile.ZipFile(RETURN217) as source:
        assert source.testzip() is None
        final_cases = [n for n in source.namelist() if n.startswith("preserved_cases/DR184-FINAL-WORD-") and n.endswith(".json")]
        assert len(final_cases) == 16
        for member in final_cases:
            raw = source.read(member)
            assert (RETURN217_ROOT / member).read_bytes() == raw
            add(files, "history/Return217/" + member, raw)
    for path, raw in sources_current.items():
        add(files, path, raw)

    OUT.mkdir(parents=True, exist_ok=False)
    candidate_path = OUT / "CURRENT_SOURCE_CONFERENCE_CANDIDATE_279.json"
    context_path = OUT / "CURRENT_CONTEXT_279.json"
    request_path = OUT / "REQUEST_279.txt"
    candidate_raw = enc(current_candidate)
    candidate_path.write_bytes(candidate_raw)
    request_path.write_text(request_text, encoding="utf-8", newline="\n")
    context = {"id": "RANK9-DEATH-RECOVERY7-CURRENT-CONTEXT-279", "recordedAtUtc": now,
               "sourceCommitBase": head, "sourceBranch": branch, "authority": AUTH,
               "targetGroup": {"group": GROUP, "pendingIds": TARGETS, "count": 1},
               "currentIndex": info(INDEX), "currentCatalog": info(CATALOG), "currentAccess": info(ACCESS),
               "parentQueue278": info(Q278), "parentHandoff278": info(H278), "parentPendingAudit278": info(P278),
               "finalCurrentQueue279ToAttachSeparately": True,
               "directorRuling278": info(RULING278), "packet235HistoricalHold": info(RETURN235),
               "priorSourcePathsRefreshed": 74, "changedHistoricalSourcePaths": changed,
               "noAcceptanceApplicationOrCanonicalChangesRequested": True}
    context_raw = enc(context)
    context_path.write_bytes(context_raw)
    add(files, "CURRENT_CONTEXT_279.json", context_raw)
    add(files, "CURRENT_SOURCE_CONFERENCE_CANDIDATE_279.json", candidate_raw)
    add(files, "REQUEST_279.txt", request_text.encode("utf-8"))

    archive_path = OUT / "DD_Rank9_DeathRecovery7_CurrentSource_279.zip"
    members = [{"path": n, "bytes": len(b), "sha256": sha(b), "crc32": crc(b)} for n, b in sorted(files.items())]
    manifest = {"id": "RANK9-DEATH-RECOVERY7-PACKET279-MANIFEST", "sourceCommitBase": head,
                "sourceBranch": branch, "authority": AUTH, "targetIds": TARGETS,
                "memberCountExcludingSelf": len(members), "members": members}
    manifest_raw = enc(manifest)
    with zipfile.ZipFile(archive_path, "w", zipfile.ZIP_DEFLATED, compresslevel=6) as z:
        for n, b in sorted(files.items()): z.writestr(n, b)
        z.writestr("MANIFEST.json", manifest_raw)
    with zipfile.ZipFile(archive_path) as z:
        assert z.testzip() is None and len(z.namelist()) == len(files) + 1 == len(set(z.namelist()))
        for rec in members: assert (len(z.read(rec["path"])), sha(z.read(rec["path"])), crc(z.read(rec["path"]))) == (rec["bytes"], rec["sha256"], rec["crc32"])

    delivery_path = OUT / "DD_Rank9_DeathRecovery7_CurrentSource_279_DELIVERY.json"
    delivery = {"id": "RANK9-DEATH-RECOVERY7-CURRENT-SOURCE-279-DELIVERY", "status": "PREPARED_UNAUDITED_UNSENT",
                "archive": info(archive_path), "memberCount": len(files)+1, "payloadCount": len(files),
                "memberManifest": {"path": "MANIFEST.json", "bytes": len(manifest_raw), "sha256": sha(manifest_raw), "crc32": crc(manifest_raw)},
                "members": members + [{"path": "MANIFEST.json", "bytes": len(manifest_raw), "sha256": sha(manifest_raw), "crc32": crc(manifest_raw)}],
                "exactAllowlist": sorted([*files.keys(), "MANIFEST.json"]), "sourceCommitBase": head, "sourceBranch": branch,
                "authority": AUTH, "group": GROUP, "targetIds": TARGETS,
                "sourceBindings": source_bindings, "changedSourceBindings": changed,
                "candidate": info(candidate_path, candidate_raw), "context": info(context_path, context_raw), "request": info(request_path),
                "priorDirectorReturn235": {"archive": info(RETURN235), "delivery": info(RETURN235_DELIVERY), "audit": info(RETURN235_AUDIT), "receipt": info(RETURN235_RECEIPT)},
                "previousCurrentBatch278Ruling": info(RULING278), "acceptedIds": [], "appliedIds": [], "canonicalChanges": False,
                "githubChanges": False, "runtimeExecuted": False, "sourceProgramsExecuted": False, "conversation": CHAT}
    delivery_path.write_bytes(enc(delivery))
    prep_path = BASE / "RANK9DEATHRECOVERY7_SOURCE_PREPARATION_279.json"
    prep = {"id": "RANK9DEATHRECOVERY7-SOURCE-PREPARATION-279", "status": "PREPARED_UNAUDITED_UNSENT",
            "recordedAtUtc": now, "sourceCommitBase": head, "sourceBranch": branch, "authority": AUTH,
            "group": GROUP, "targetIds": TARGETS, "sourceBindings": len(source_bindings), "changedSources": changed,
            "archive": info(archive_path), "delivery": info(delivery_path), "candidate": info(candidate_path),
            "context": info(context_path), "request": info(request_path), "historicalFinalWordCases": 16,
            "canonicalChanges": False, "accepted": False, "applied": False}
    prep_path.write_bytes(enc(prep))
    packet_path = BASE / "RANK9DEATHRECOVERY7_PACKET_279.json"
    packet = {"id": "RANK9DEATHRECOVERY7-PACKET-279", "status": "PREPARED_UNAUDITED_UNSENT", "group": GROUP,
              "targetIds": TARGETS, "authority": AUTH, "sourceBranch": branch, "sourceCommitBase": head,
              "archive": info(archive_path), "delivery": info(delivery_path), "candidate": info(candidate_path),
              "sourcePreparation": info(prep_path), "sourceBindings": len(source_bindings),
              "changedSourceBindings": len(changed), "independentAudit": None, "accepted": False, "applied": False}
    packet_path.write_bytes(enc(packet))

    pending279 = copy.deepcopy(pending)
    ng = pending279["preparedNextGroup"]
    ng.update({"status": "PACKET279_PREPARED_UNAUDITED_UNSENT_816_32", "freshPacketRequiredForCurrentAuthority": False,
               "packet": info(archive_path), "deliveryManifest": info(delivery_path), "candidate": info(candidate_path),
               "sourcePreparation": info(prep_path)})
    for g in pending279.get("groups", []):
        if g.get("group") == GROUP: g.update({"status": "PACKET279_PREPARED_UNAUDITED_UNSENT_816_32", "preparedPacket": info(archive_path), "candidate": info(candidate_path), "deliveryManifest": info(delivery_path)})
    pending279.update({"status": "PASS_EXACT_816_32_PENDING_SET_PACKET279_PREPARED", "recordedAtUtc": now})
    P279.write_text(json.dumps(pending279, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
    q.update({"status": "FINAL_WORD_PACKET279_PREPARED_UNAUDITED_816_32", "packetStatus": "FINAL_WORD_PACKET279_PREPARED_UNAUDITED_816_32",
              "currentPacket": info(archive_path), "currentSourcePacket": info(archive_path), "currentDeliveryManifest": info(delivery_path),
              "currentPacketDelivery": info(delivery_path), "currentPreparation": info(prep_path), "next": ng.copy(), "nextPreparedRequest": ng.copy(),
              "pendingIdentityAudit": info(P279), "packetAuditStatus": None, "packetAuditChecks": None, "packetAuditFailures": None,
              "nextGroup": GROUP, "nextPendingIds": TARGETS, "nextPendingCount": 1, "recordedAtUtc": now})
    for g in q.get("currentPendingGroups", []):
        if g.get("group") == GROUP: g.update({"status": "PACKET279_PREPARED_UNAUDITED_UNSENT_816_32", "preparedPacket": info(archive_path), "deliveryManifest": info(delivery_path), "candidate": info(candidate_path)})
    Q279.write_text(json.dumps(q, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
    h.update({"status": "FINAL_WORD_PACKET279_PREPARED_UNAUDITED_816_32", "currentPacket": info(archive_path),
              "currentPacketDelivery": info(delivery_path), "currentDeliveryManifest": info(delivery_path),
              "currentPreparation": info(prep_path), "pendingIdentityAudit": info(P279), "nextGroup": GROUP,
              "nextPendingCount": 1, "nextPendingIds": TARGETS, "recordedAtUtc": now,
              "nextStep": {"group": GROUP, "pendingIds": TARGETS, "pendingCount": 1, "status": "PACKET279_PREPARED_UNAUDITED_UNSENT_816_32",
                           "packet": info(archive_path), "deliveryManifest": info(delivery_path)}})
    H279.write_text(json.dumps(h, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
    q["pendingIdentityAudit"] = info(P279)
    Q279.write_text(json.dumps(q, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
    h["queue"] = info(Q279); h["queueBinding"] = info(Q279); h["currentQueueBinding"] = info(Q279)
    H279.write_text(json.dumps(h, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
    (BASE / "CURRENT_SPELL_REVIEW_SNAPSHOT_279.md").write_text(
        "# Current ordinary spell-review checkpoint 279\n\n"
        "Authority is **816 reviewed/applied / 32 pending / 0 accepted-unapplied**, with 540 complete standalone procedures and 173 scoped interfaces. The Director held the prior Psychic/Fear7 group; the next ordered target is final-word under DR217-B01. Packet279 refreshes 74 source bindings at 816/32 and preserves Return184/217/235 plus all 16 Return217 final-word cases.\n\n"
        "The packet is prepared but independently unaudited and unsent. Review only final-word. The positive source witness must establish current body/HP, soul availability, custody, capture, and lawful reserve expenditure.\n",
        encoding="utf-8", newline="\n")
    print(json.dumps({"status": "PREPARED_UNAUDITED_UNSENT", "authority": AUTH, "group": GROUP,
                      "targetIds": TARGETS, "sourceBindings": len(source_bindings), "changedSourceBindings": len(changed),
                      "memberCount": len(files)+1, "archive": info(archive_path), "delivery": info(delivery_path)}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
