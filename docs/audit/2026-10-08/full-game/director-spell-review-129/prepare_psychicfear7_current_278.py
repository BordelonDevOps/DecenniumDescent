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
GROUP = "rank9-psychic-fear7"
TARGETS = ["psychic-scream", "mass-phantom-killer", "weird"]
AUTH = {"reviewedApplied": 816, "pending": 32, "acceptedUnapplied": 0,
        "completeStandaloneProcedures": 540, "scopedInterfaces": 173}
CHAT = "https://chatgpt.com/g/g-p-67f17555a8dc8191a2b5b81e6d8adc12-dungeon-crawler/c/6adc506d-8770-83ea-b64c-0345d9b9b682"
INDEX = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json"
CATALOG = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json"
ACCESS = ROOT / "DescentReviewChanges/ReviewBible/data/director/spell_review/accepted_interface_registry_06.json"
HIST_CANDIDATE = ROOT / "DescentReviewChanges/ReviewBible/data/director/spell_review/rank9_psychic_fear_7_source_conference_01.json"
HIST_ARCHIVE = FULL / "DD_Rank9_Psychic_Fear_7_Source_Conference_01.zip"
PRIOR_CANDIDATE = AUDIT / "rank9_psychicfear7_current_source_234_prepared/CURRENT_SOURCE_CONFERENCE_CANDIDATE_234.json"
PRIOR_PACKET = AUDIT / "rank9_psychicfear7_current_source_234_prepared/DD_Rank9_PsychicFear7_CurrentSource_234.zip"
RETURN234_DIR = AUDIT / "rank9_psychicfear7_return234_received"
RETURN234 = RETURN234_DIR / "DD_Rank9_PsychicFear3_Director_Return234_HELD.zip"
RETURN234_DELIVERY = RETURN234_DIR / "DD_Rank9_PsychicFear3_Director_Return234_HELD_DELIVERY.json"
RETURN234_AUDIT = AUDIT / "RANK9PSYCHICFEAR7_RETURN234_INDEPENDENT_AUDIT.json"
RETURN234_RECEIPT = AUDIT / "RANK9PSYCHICFEAR7_RETURN234_RECEIPT.json"
RETURN277 = AUDIT / "MIND_COLLAPSE_ABSOLUTE_PUPPETMASTER_DIRECTOR_RETURN_277.json"
CORRECTION277 = AUDIT / "rank9_memorydenial6_snapshot_correction_277_prepared/DD_Rank9_MemoryDenial6_SnapshotCorrection_277.zip"
QUEUE277 = AUDIT / "CURRENT_SPELL_QUEUE_277.json"
HANDOFF277 = AUDIT / "CURRENT_HANDOFF_277.json"
PENDING277 = AUDIT / "CURRENT32_PENDING_IDENTITY_AUDIT_277.json"
OUT = AUDIT / "rank9_psychicfear7_current_source_278_prepared_review1"


def enc(value) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8")


def read(path: Path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def crc(raw: bytes) -> str:
    return f"{zlib.crc32(raw) & 0xffffffff:08x}"


def blob_sha(raw: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()


def bind(path: Path, raw: bytes | None = None) -> dict:
    data = path.read_bytes() if raw is None else raw
    return {"path": path.relative_to(ROOT).as_posix(), "bytes": len(data), "sha256": sha(data), "crc32": crc(data)}


def safe(name: str) -> bool:
    p = PurePosixPath(name)
    return bool(name) and "\\" not in name and not p.is_absolute() and all(x not in ("", ".", "..") for x in p.parts)


def main() -> None:
    if OUT.exists():
        raise FileExistsError(f"Refusing to overwrite existing output: {OUT}")
    for path in [INDEX, CATALOG, ACCESS, HIST_CANDIDATE, HIST_ARCHIVE, PRIOR_CANDIDATE, PRIOR_PACKET,
                 RETURN234, RETURN234_DELIVERY, RETURN234_AUDIT, RETURN234_RECEIPT, RETURN277, CORRECTION277,
                 QUEUE277, HANDOFF277, PENDING277]:
        assert path.is_file(), path
    branch = subprocess.check_output(["git", "branch", "--show-current"], cwd=ROOT, text=True).strip()
    head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    assert branch == "main", branch
    now = datetime.now(timezone.utc).isoformat()

    index, catalog = read(INDEX), read(CATALOG)
    queue277, handoff277, pending277 = read(QUEUE277), read(HANDOFF277), read(PENDING277)
    assert queue277["currentAuthority"] == handoff277["currentAuthority"] == pending277["authority"] == AUTH
    assert index["authoredCounts"] == {"reviewed": 816, "pending": 32}
    assert index["representationCounts"]["completeReviewedStandaloneProcedures"] == 540
    assert pending277["pendingCount"] == len(pending277["pendingIds"]) == 32
    assert all(sid in pending277["pendingIds"] for sid in TARGETS)
    assert queue277["nextGroup"] == GROUP and queue277["nextPendingIds"] == TARGETS

    entries = {r["id"]: r for r in index["entries"]}
    cards = {r["id"]: r for r in catalog["spells"]}
    for sid in TARGETS:
        assert entries[sid]["authoredStatus"] == "pending-authored-procedure"
        assert entries[sid]["sourceStatus"] == "blocked-pending-operational-review"
        assert cards[sid].get("operational") is None

    historical_candidate = read(HIST_CANDIDATE)
    prior_candidate = read(PRIOR_CANDIDATE)
    assert len(historical_candidate["sourceBindings"]) == len(prior_candidate["sourceBindings"]) == 84
    previous_audit = read(RETURN234_AUDIT)
    assert previous_audit["status"] == "PASS" and previous_audit["failedChecks"] == 0
    assert previous_audit["authority"] == {"reviewedApplied": 811, "pending": 37, "acceptedUnapplied": 0,
                                             "completeStandaloneProcedures": 535, "scopedInterfaces": 173}
    assert previous_audit["heldIds"] == TARGETS
    assert previous_audit["blockerIds"] == {"psychic-scream": ["PF182-B01"],
                                             "mass-phantom-killer": ["PF182-B02"], "weird": ["PF182-B02"]}
    with zipfile.ZipFile(HIST_ARCHIVE) as historical:
        assert historical.testzip() is None
        refreshed, changed, sources = [], [], {}
        for old in historical_candidate["sourceBindings"]:
            path = old["path"]
            assert safe(path)
            raw = (ROOT / path).read_bytes()
            prior_raw = historical.read("sources/" + path)
            assert (len(prior_raw), sha(prior_raw)) == (old["bytes"], old["sha256"]), path
            row = {"path": path, "bytes": len(raw), "sha256": sha(raw), "crc32": crc(raw), "gitBlobSHA1": blob_sha(raw)}
            refreshed.append(row)
            sources["sources_current/" + path] = raw
            if raw != prior_raw:
                changed.append({"path": path, "historicalBytes": len(prior_raw), "historicalSha256": sha(prior_raw),
                                "currentBytes": len(raw), "currentSha256": sha(raw)})

    prior_target_records = {r["spellId"]: r for r in prior_candidate["targetRecords"]}
    target_records = [copy.deepcopy(prior_target_records[sid]) for sid in TARGETS]
    for record in target_records:
        sid = record["spellId"]
        record["currentIndexEntry"] = copy.deepcopy(entries[sid])
        record["completeCurrentCatalogSourceAndAccess"] = copy.deepcopy(cards[sid])
        record["status"] = "pending-authored-procedure"
        record["currentAuthorityDisposition"] = "Fresh review at 816/32/0; Return234 is historical 811/37/0 evidence."
    current_targets = [{"spellId": sid, "currentIndexEntry": copy.deepcopy(entries[sid]),
                        "currentCatalogCard": copy.deepcopy(cards[sid]), "status": "pending at current 816/32/0"}
                       for sid in TARGETS]

    blockers = {
        "psychic-scream": "PF182-B01: source-authorized current body/form with enumerated heads and lifecycle; real final death, head consequence, and remains/custody; explicit headless/multihead/current-form operands.",
        "mass-phantom-killer": "PF182-B02: one currently operational genuine full-extra-turn grant, actual legal acquisition and actor/unlock/repertoire history, then integrated turn ordering without extra damage exposure, saves, recharge, Ready reset, or clock extension.",
        "weird": "PF182-B02: same separately qualified genuine extra-turn grant/acquired actor dependency, with its own actual target-end and attached-phase witness; no extra damage exposure, save, recharge, Ready reset, or clock extension.",
    }
    candidate = copy.deepcopy(prior_candidate)
    candidate.update({"id": "CURRENT-SOURCE-CONFERENCE-CANDIDATE-278", "recordedAtUtc": now,
                      "status": "PREPARED_CURRENT_AUTHORITY_816_32_EXACT_PSYCHIC_FEAR7_GROUP",
                      "sourceCommitBase": head, "sourceBranch": branch, "currentWorkingTreeSnapshot": True,
                      "currentAuthority": AUTH, "currentPendingGroup": {"group": GROUP, "spellIds": TARGETS, "count": 3},
                      "targetRecords": target_records, "currentTargets": current_targets,
                      "sourceBindings": refreshed,
                      "sourceBindingRefresh": {"count": len(refreshed), "changedSinceHistoricalSourceConference01": changed,
                                               "sourceBytesFromCurrentWorkingTree": True},
                      "currentAuthorityEvidence": {"index": bind(INDEX), "catalog": bind(CATALOG), "accessRegistry": bind(ACCESS),
                          "parentQueue277": bind(QUEUE277), "parentHandoff277": bind(HANDOFF277), "parentPendingAudit277": bind(PENDING277),
                          "directorQualificationReturn277": bind(RETURN277), "snapshotCorrection277": bind(CORRECTION277),
                          "priorReturn234Audit": bind(RETURN234_AUDIT), "priorReturn234Receipt": bind(RETURN234_RECEIPT)},
                      "priorReturn234Disposition": {"authority": previous_audit["authority"], "heldIds": TARGETS,
                          "blockerIds": previous_audit["blockerIds"], "archive": bind(RETURN234),
                          "delivery": bind(RETURN234_DELIVERY), "audit": bind(RETURN234_AUDIT), "receipt": bind(RETURN234_RECEIPT)},
                      "currentReassessmentBlockers": blockers, "closedAndCompletedIdentitiesOutOfScope": True,
                      "newRuleAdoptions": 0})
    candidate_raw = enc(candidate)

    context = {"id": "RANK9-PSYCHIC-FEAR7-CURRENT-DIRECTOR-CONTEXT-278", "recordedAtUtc": now,
               "sourceCommitBase": head, "sourceBranch": branch, "authority": AUTH,
               "targetGroup": {"group": GROUP, "pendingIds": TARGETS, "count": 3},
               "currentIndexBinding": bind(INDEX), "currentCatalogBinding": bind(CATALOG), "accessRegistryBinding": bind(ACCESS),
               "parentQueue277": bind(QUEUE277), "parentHandoff277": bind(HANDOFF277), "parentPendingAudit277": bind(PENDING277),
               "directorQualificationReturn277": bind(RETURN277), "snapshotCorrection277": bind(CORRECTION277),
               "priorSourceCandidate234": bind(PRIOR_CANDIDATE),
               "priorSourcePacket234ExternalReference": {**bind(PRIOR_PACKET), "includedInArchive": False,
                    "reason": "Return234, its receipt/audit, the prior candidate and original source conference preserve the required review evidence; the 76.8 MB prior packet is not duplicated."},
               "priorReturn234": {"archive": bind(RETURN234), "delivery": bind(RETURN234_DELIVERY),
                                  "audit": bind(RETURN234_AUDIT), "receipt": bind(RETURN234_RECEIPT),
                                  "heldIds": TARGETS, "blockerIds": previous_audit["blockerIds"]},
               "sourceBindingsRefreshed": len(refreshed), "changedHistoricalSourceBindings": changed,
               "reviewScope": "Reassess only PF182-B01 for psychic-scream and PF182-B02 for mass-phantom-killer/weird at 816/32/0.",
               "preservedPriorContext": {"originalQuestions": len(candidate["originalQuestionsUnchanged"]),
                   "focusedAddenda": len(candidate["focusedAdditionalQuestionsUnchanged"]),
                   "selectedQuestionDispositions": len(candidate["priorSelectedQuestionDispositions"]),
                   "mainCaseObligations": len(candidate["priorTargetMainCaseObligations"]),
                   "previouslyPreservedCases": candidate["priorReturn216Counts"].get("preservedCases"),
                   "previouslyHeldCases": candidate["priorReturn216Counts"].get("heldCases")},
               "noAcceptanceOrApplicationRequested": True, "closedCohortsReopened": False}
    context_raw = enc(context)

    request = (
        f"GPT Director — fresh ordinary-spell source review at 816 applied / 32 pending / 0 accepted-unapplied (540 complete standalone procedures; 173 scoped interfaces). Review ONLY {', '.join(TARGETS)} in {GROUP}. The exact current index/catalog/access registry, 84 current source bindings, parent queue/handoff/pending audit, SnapshotCorrection277, and the prior independently audited Return234 are attached.\n\n"
        "Return234 held these targets at historical 811/37/0: psychic-scream PF182-B01; mass-phantom-killer PF182-B02; weird PF182-B02. Reassess those findings against the exact refreshed sources and current records. Do not reopen already accepted identities or treat the old 811/37 decision as current authority.\n\n"
        "For Psychic Scream, require the source-authorized current body/form, enumerated heads/headCount, destructibility, vital-head relationship, exact reversion/remains lifecycle, an actual final-death-to-head consequence/custody witness, and explicit headless/multihead/current-form operands. Do not infer a Bite, anatomy, body state, or head relation from names or geometry.\n\n"
        "For Mass Phantom Killer and Weird, require the currently authorized genuine full-extra-turn grant, exact source and feature pointer, trigger/timing/eligibility/activation/cost/limits, actual legal acquired actor and grantor history, and the exact integrated target/attached-phase witness. Do not substitute an extra Action, echo, initiative reorder, duration extension, or a pending spell's assumed execution. Preserve ordinary ordering, damage exposure, target-end saves, recharge, Ready, resources, and each spell's original clocks.\n\n"
        "Issue explicit held or accepted decisions only for these three, with exact blockers, source pointers, actor acquisition, and the minimum positive witness needed. Use the sealed prior Return234 evidence and questions as history, not automatic current rulings. No acceptance or application is requested by this source packet; keep authority and the pending set unchanged unless a complete sealed decision explicitly accepts an identity. Preserve all downstream gates. State the next group after this one in Director order."
    )
    request_raw = request.encode("utf-8")

    OUT.mkdir(parents=True, exist_ok=False)
    candidate_path = OUT / "CURRENT_SOURCE_CONFERENCE_CANDIDATE_278.json"
    context_path = OUT / "CURRENT_CONTEXT_278.json"
    request_path = OUT / "REQUEST_278.txt"
    candidate_path.write_bytes(candidate_raw)
    context_path.write_bytes(context_raw)
    request_path.write_bytes(request_raw)

    source_context = {
        "current/DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json": INDEX.read_bytes(),
        "current/DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json": CATALOG.read_bytes(),
        "current/DescentReviewChanges/ReviewBible/data/director/spell_review/accepted_interface_registry_06.json": ACCESS.read_bytes(),
        "parent_snapshot/CURRENT_SPELL_QUEUE_277.json": QUEUE277.read_bytes(),
        "parent_snapshot/CURRENT_HANDOFF_277.json": HANDOFF277.read_bytes(),
        "parent_snapshot/CURRENT32_PENDING_IDENTITY_AUDIT_277.json": PENDING277.read_bytes(),
        "director/MIND_COLLAPSE_ABSOLUTE_PUPPETMASTER_DIRECTOR_RETURN_277.json": RETURN277.read_bytes(),
        "director/DD_Rank9_MemoryDenial6_SnapshotCorrection_277.zip": CORRECTION277.read_bytes(),
        "history/CURRENT_SOURCE_CONFERENCE_CANDIDATE_234.json": PRIOR_CANDIDATE.read_bytes(),
        "history/DD_Rank9_PsychicFear7_Director_Return234_HELD.zip": RETURN234.read_bytes(),
        "history/DD_Rank9_PsychicFear7_Director_Return234_HELD_DELIVERY.json": RETURN234_DELIVERY.read_bytes(),
        "history/RETURN234_INDEPENDENT_AUDIT.json": RETURN234_AUDIT.read_bytes(),
        "history/RETURN234_RECEIPT.json": RETURN234_RECEIPT.read_bytes(),
        "historical/SOURCE_CANDIDATE_01.json": HIST_CANDIDATE.read_bytes(),
        "historical/SOURCE_CONFERENCE_01.zip": HIST_ARCHIVE.read_bytes(),
    }
    files = {"CURRENT_CONTEXT_278.json": context_raw, "CURRENT_SOURCE_CONFERENCE_CANDIDATE_278.json": candidate_raw,
             "REQUEST_278.txt": request_raw, **source_context, **sources}
    assert len(files) == len(set(files)) and all(safe(name) for name in files)

    archive_path = OUT / "DD_Rank9_PsychicFear7_CurrentSource_278.zip"
    rows = []
    with zipfile.ZipFile(archive_path, "w", zipfile.ZIP_DEFLATED, compresslevel=6) as archive:
        for name, raw in sorted(files.items()):
            archive.writestr(name, raw, compress_type=zipfile.ZIP_DEFLATED, compresslevel=6)
            rows.append({"path": name, "bytes": len(raw), "sha256": sha(raw), "crc32": crc(raw)})
        manifest = {"id": "RANK9-PSYCHIC-FEAR7-CURRENT-SOURCE-MANIFEST-278", "sourceCommitBase": head,
                    "sourceBranch": branch, "sourceAuthority": AUTH, "group": GROUP, "pendingIds": TARGETS,
                    "memberCountExcludingSelf": len(rows), "members": rows}
        archive.writestr("MANIFEST.json", enc(manifest), compress_type=zipfile.ZIP_DEFLATED, compresslevel=6)
    with zipfile.ZipFile(archive_path) as archive:
        assert archive.testzip() is None and len(archive.namelist()) == len(rows) + 1 == len(set(archive.namelist()))
        for row in rows:
            raw = archive.read(row["path"])
            assert (len(raw), sha(raw), crc(raw)) == (row["bytes"], row["sha256"], row["crc32"])
    archive_binding = bind(archive_path)
    candidate_binding = bind(candidate_path, candidate_raw)
    context_binding = bind(context_path, context_raw)
    request_binding = bind(request_path, request_raw)

    delivery_path = OUT / "DD_Rank9_PsychicFear7_CurrentSource_278_DELIVERY.json"
    delivery = {"id": "RANK9-PSYCHIC-FEAR7-CURRENT-SOURCE-DELIVERY-278", "status": "PREPARED_UNAUDITED_UNSENT",
                "archive": archive_binding, "memberCount": len(rows) + 1, "payloadCount": len(rows),
                "members": rows + [{"path": "MANIFEST.json", "bytes": len(enc(manifest)),
                                    "sha256": sha(enc(manifest)), "crc32": crc(enc(manifest))}],
                "memberManifest": {"path": "MANIFEST.json", "bytes": len(enc(manifest)),
                                   "sha256": sha(enc(manifest)), "crc32": crc(enc(manifest))},
                "sourceCommitBase": head, "sourceBranch": branch, "authority": AUTH,
                "group": GROUP, "targetIds": TARGETS, "accepted": False, "applied": False,
                "candidate": candidate_binding, "context": context_binding, "request": request_binding,
                "sourceBindings": len(refreshed), "changedHistoricalBindings": changed,
                "priorReturn234": {"archive": bind(RETURN234), "delivery": bind(RETURN234_DELIVERY),
                                   "audit": bind(RETURN234_AUDIT), "receipt": bind(RETURN234_RECEIPT)},
                "canonicalChanges": False, "applicationChanges": False, "runtimeExecuted": False,
                "githubChanges": False, "conversation": CHAT}
    delivery_raw = enc(delivery)
    delivery_path.write_bytes(delivery_raw)
    delivery_binding = bind(delivery_path, delivery_raw)

    prep_path = AUDIT / "RANK9PSYCHICFEAR7_SOURCE_PREPARATION_278.json"
    packet_path = AUDIT / "RANK9PSYCHICFEAR7_PACKET_278.json"
    prep = {"id": "RANK9-PSYCHICFEAR7-SOURCE-PREPARATION-278", "recordedAtUtc": now,
            "status": "PREPARED_UNAUDITED_UNSENT", "sourceCommitBase": head, "sourceBranch": branch,
            "authority": AUTH, "group": GROUP, "targetIds": TARGETS, "archive": archive_binding,
            "deliveryManifest": delivery_binding, "candidate": candidate_binding, "context": context_binding,
            "sourceBindings": len(refreshed), "changedHistoricalBindings": changed,
            "priorReturn234": {"heldIds": TARGETS, "blockerIds": previous_audit["blockerIds"],
                                "archive": bind(RETURN234), "audit": bind(RETURN234_AUDIT)},
            "checksPassed": 10, "checksFailed": 0, "canonicalChanges": False, "accepted": False, "applied": False}
    prep_raw = enc(prep)
    prep_path.write_bytes(prep_raw)
    prep_binding = bind(prep_path, prep_raw)
    packet_record = {"id": "RANK9PSYCHICFEAR7-PACKET-278", "status": "PREPARED_UNAUDITED_UNSENT",
                     "group": GROUP, "targetIds": TARGETS, "authority": AUTH, "sourceBranch": branch,
                     "sourceCommitBase": head, "archive": archive_binding, "deliveryManifest": delivery_binding,
                     "candidate": candidate_binding, "context": context_binding, "sourcePreparation": prep_binding,
                     "sourceBindings": len(refreshed), "changedHistoricalBindings": len(changed),
                     "priorReturn234": {"heldIds": TARGETS, "blockerIds": previous_audit["blockerIds"],
                                        "archive": bind(RETURN234), "audit": bind(RETURN234_AUDIT)},
                     "independentAudit": None, "accepted": False, "applied": False}
    packet_record_path = AUDIT / "RANK9PSYCHICFEAR7_PACKET_278.json"
    packet_record_raw = enc(packet_record)
    packet_record_path.write_bytes(packet_record_raw)
    packet_record_binding = bind(packet_record_path, packet_record_raw)

    p = copy.deepcopy(pending277)
    p.update({"id": "CURRENT32-PENDING-IDENTITY-AUDIT-278", "recordedAtUtc": now,
              "status": "PASSED_EXACT_CURRENT_816_32_PENDING_SET_PACKET278_PREPARED",
              "preparedNextGroup": {"group": GROUP, "pendingIds": TARGETS, "pendingCount": 3,
                                    "status": "PACKET278_PREPARED_UNAUDITED_UNSENT_816_32",
                                    "freshPacketRequiredForCurrentAuthority": False, "packet": archive_binding,
                                    "deliveryManifest": delivery_binding, "candidate": candidate_binding,
                                    "sourcePreparation": prep_binding}})
    for group in p.get("groups", []):
        if group.get("group") == GROUP:
            group.update({"status": "PACKET278_PREPARED_UNAUDITED_UNSENT_816_32",
                          "freshPacketRequiredForCurrentAuthority": False, "preparedPacket": archive_binding,
                          "deliveryManifest": delivery_binding, "candidate": candidate_binding})
    p_path = AUDIT / "CURRENT32_PENDING_IDENTITY_AUDIT_278.json"
    p_raw = enc(p)
    p_path.write_bytes(p_raw)
    p_binding = bind(p_path, p_raw)

    q = copy.deepcopy(queue277)
    q.update({"id": "SPELL-REVIEW-QUEUE-278", "recordedAtUtc": now, "supersedesQueue": bind(QUEUE277),
              "parentQueue": bind(QUEUE277), "pendingIdentityAudit": p_binding,
              "status": "PSYCHIC_FEAR7_PACKET278_PREPARED_UNAUDITED_816_32",
              "packetStatus": "PSYCHIC_FEAR7_PACKET278_PREPARED_UNAUDITED_816_32",
              "currentPreparation": prep_binding, "currentSourcePacket": archive_binding,
              "currentPacket": archive_binding, "currentDeliveryManifest": delivery_binding,
              "currentPacketDelivery": delivery_binding,
              "next": {"group": GROUP, "pendingIds": TARGETS, "pendingCount": 3,
                       "status": "PACKET278_PREPARED_UNAUDITED_UNSENT_816_32",
                       "freshPacketRequiredForCurrentAuthority": False, "packet": archive_binding,
                       "deliveryManifest": delivery_binding, "candidate": candidate_binding},
              "nextPreparedRequest": {"group": GROUP, "pendingIds": TARGETS, "pendingCount": 3,
                                      "status": "PACKET278_PREPARED_UNAUDITED_UNSENT_816_32",
                                      "freshPacketRequiredForCurrentAuthority": False, "packet": archive_binding,
                                      "deliveryManifest": delivery_binding, "candidate": candidate_binding,
                                      "sourcePreparation": prep_binding},
              "nextGroup": GROUP, "nextPendingCount": 3, "nextPendingIds": TARGETS})
    q["currentAuthority"] = AUTH
    for group in q.get("currentPendingGroups", []):
        if group.get("group") == GROUP:
            group.update({"status": "PACKET278_PREPARED_UNAUDITED_UNSENT_816_32",
                          "freshPacketRequiredForCurrentAuthority": False, "preparedPacket": archive_binding,
                          "deliveryManifest": delivery_binding, "candidate": candidate_binding})
    q_path = AUDIT / "CURRENT_SPELL_QUEUE_278.json"
    q_raw = enc(q)
    q_path.write_bytes(q_raw)
    q_binding = bind(q_path, q_raw)

    h = copy.deepcopy(handoff277)
    h.update({"id": "CURRENT-HANDOFF-278", "recordedAtUtc": now,
              "status": "PSYCHIC_FEAR7_PACKET278_PREPARED_UNAUDITED_816_32",
              "currentAuthority": AUTH, "authority": AUTH, "queue": q_binding,
              "queueBinding": q_binding, "currentQueueBinding": q_binding, "pendingIdentityAudit": p_binding,
              "nextGroup": GROUP, "nextPendingCount": 3, "nextPendingIds": TARGETS,
              "nextStep": {"group": GROUP, "pendingIds": TARGETS, "pendingCount": 3,
                           "status": "PACKET278_PREPARED_UNAUDITED_UNSENT_816_32",
                           "packet": archive_binding, "deliveryManifest": delivery_binding,
                           "independentAudit": None},
              "currentPreparation": prep_binding, "currentPacket": archive_binding,
              "currentDeliveryManifest": delivery_binding, "currentPacketDelivery": delivery_binding,
              "githubChanges": False, "canonicalRuntimeApplicationPerformed": False,
              "resumePriority": "Independently audit and submit current 816/32 Packet278 to the GPT Director; reassess only Psychic Scream, Mass Phantom Killer and Weird against PF182-B01/B02; continue through response caps, apply only exact acceptances, and ping/monitor the Director frequently."})
    h_path = AUDIT / "CURRENT_HANDOFF_278.json"
    h_raw = enc(h)
    h_path.write_bytes(h_raw)
    h_binding = bind(h_path, h_raw)

    snapshot_path = AUDIT / "CURRENT_SPELL_REVIEW_SNAPSHOT_278.md"
    snapshot_path.write_text(
        "# Current ordinary spell-review checkpoint 278\n\n"
        "Authority is **816 reviewed/applied / 32 pending / 0 accepted-unapplied**, with 540 complete standalone procedures and 173 scoped interfaces. "
        "The Director completed qualification checks for Mind Collapse, Absolute Domination and Puppetmaster’s Realm and retained their blockers. "
        "The next group is Psychic Scream, Mass Phantom Killer and Weird, freshly bound at 816/32. Packet278 refreshes 84 source bindings and preserves Return234's held case/question evidence.\n\n"
        "See [handoff](CURRENT_HANDOFF_278.json), [queue](CURRENT_SPELL_QUEUE_278.json), [pending audit](CURRENT32_PENDING_IDENTITY_AUDIT_278.json), "
        "[packet record](RANK9PSYCHICFEAR7_PACKET_278.json), and [source packet](rank9_psychicfear7_current_source_278_prepared/DD_Rank9_PsychicFear7_CurrentSource_278.zip).\n",
        encoding="utf-8", newline="\n")
    start = ROOT / "START_HERE.md"
    old_start = start.read_text(encoding="utf-8-sig")
    prefix = "**Current ordinary spell-review handoff [278](docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT_HANDOFF_278.json):**"
    if not old_start.startswith(prefix):
        start.write_text(prefix + " authority is 816 applied / 32 pending / 0 accepted-unapplied. GPT confirmed the next fresh source review is Psychic Scream, Mass Phantom Killer and Weird. See [packet](docs/audit/2026-10-08/full-game/director-spell-review-129/RANK9PSYCHICFEAR7_PACKET_278.json).\n\n" + old_start,
                         encoding="utf-8", newline="\n")

    print(json.dumps({"status": "PREPARED_UNAUDITED_UNSENT", "sourceCommitBase": head, "branch": branch,
                      "authority": AUTH, "group": GROUP, "targets": TARGETS,
                      "sourceBindings": len(refreshed), "changedHistoricalBindings": changed,
                      "archive": archive_binding, "delivery": delivery_binding,
                      "pending": p_binding, "queue": q_binding, "handoff": h_binding,
                      "packetRecord": packet_record_binding}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
