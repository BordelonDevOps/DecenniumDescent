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
FULL = ROOT / "docs/audit/2026-10-08/full-game"
AUDIT = FULL / "director-spell-review-129"
GROUP = "rank9-miracle-reality2"
TARGETS = ["divine-intervention-greater", "wish"]
AUTHORITY = {"reviewedApplied": 816, "pending": 32, "acceptedUnapplied": 0, "completeStandaloneProcedures": 540, "scopedInterfaces": 173}
INDEX = "DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json"
CATALOG = "DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json"
ACCESS = "DescentReviewChanges/ReviewBible/data/director/spell_review/accepted_interface_registry_06.json"
HIST_CANDIDATE = "DescentReviewChanges/ReviewBible/data/director/spell_review/rank9_miracle_reality_2_source_conference_01.json"
HIST_ARCHIVE = FULL / "DD_Rank9_Miracle_Reality_2_Source_Conference_01.zip"
HIST_NOTES = AUDIT / "RANK9MIRACLEREALITY2_NEXT_CONFERENCE_NOTES_129.json"
CHAT = "https://chatgpt.com/g/g-p-67f17555a8dc8191a2b5b81e6d8adc12-dungeon-crawler/c/6adc506d-8770-83ea-b64c-0345d9b9b682"

RETURN_INFO = {
    284: ("rank9_planargates5_return284_received", "DD_Rank9_PlanarGates5_Director_Return284_HELD.zip", "DD_Rank9_PlanarGates5_Director_Return284_HELD_DELIVERY.json", "RANK9_PLANARGATES5_RETURN284_INDEPENDENT_AUDIT.json", "RANK9_PLANARGATES5_RETURN284_RECEIPT.json", ["banishment-gate", "conjure-demiplane-fortress"], ["PG200-B03", "PG200-B04", "PG200-B06"]),
    285: ("rank9_summonhosts5_return285_received", "DD_Rank9_SummonHosts5_Director_Return285_HELD.zip", "DD_Rank9_SummonHosts5_Director_Return285_HELD_DELIVERY.json", "RANK9SUMMONHOSTS5_RETURN285_INDEPENDENT_AUDIT.json", "RANK9SUMMONHOSTS5_RETURN285_RECEIPT.json", ["summon-elemental-avatar", "summon-herald-of-the-planes", "summon-avatar-of-decay"], ["SH202-B01", "SH202-B02", "SH202-B03"]),
    286: ("rank9_impactexile4_return286_received", "DD_Rank9_ImpactExile4_Director_Return286_HELD.zip", "DD_Rank9_ImpactExile4_Director_Return286_HELD_DELIVERY.json", "RANK9IMPACTEXILE4_RETURN286_INDEPENDENT_AUDIT.json", "RANK9IMPACTEXILE4_RETURN286_RECEIPT.json", ["reverse-gravity-field"], ["IE204-B02"]),
    287: ("rank9_alignmentfactionpurification5_return287_received", "DD_Rank9_AlignmentFactionPurification5_Director_Return287_HELD.zip", "DD_Rank9_AlignmentFactionPurification5_Director_Return287_HELD_DELIVERY.json", "RANK9ALIGNFACTIONPURIFICATION5_RETURN287_INDEPENDENT_AUDIT.json", "RANK9ALIGNFACTIONPURIFICATION5_RETURN287_RECEIPT.json", ["alignment-ascension", "alignment-perfection", "faction-incarnate", "faction-perfection", "corruption-purification"], ["AFP211-B01", "AFP211-B02", "AFP211-B03", "AFP211-B04", "AFP211-B05"]),
    288: ("rank9_projectionconfinement2_return288_received", "DD_Rank9_ProjectionConfinement2_Director_Return288_HELD.zip", "DD_Rank9_ProjectionConfinement2_Director_Return288_HELD_DELIVERY.json", "RANK9PROJECTIONCONFINEMENT2_RETURN288_INDEPENDENT_AUDIT.json", "RANK9PROJECTIONCONFINEMENT2_RETURN288_RECEIPT.json", ["astral-projection", "imprisonment"], ["PC232-B01", "PC232-B02"]),
}


def enc(value) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8")


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def crc(raw: bytes) -> str:
    return f"{zlib.crc32(raw) & 0xffffffff:08x}"


def git_blob_sha(raw: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()


def read(path: Path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def info(path: Path, raw: bytes | None = None) -> dict:
    data = path.read_bytes() if raw is None else raw
    return {"path": path.relative_to(ROOT).as_posix(), "bytes": len(data), "sha256": sha(data), "crc32": crc(data)}


def safe(name: str) -> bool:
    path = PurePosixPath(name)
    return bool(name) and "\\" not in name and not path.is_absolute() and all(part not in ("", ".", "..") for part in path.parts)


def return_artifacts(number: int) -> dict:
    folder, archive_name, delivery_name, audit_name, receipt_name, held, blockers = RETURN_INFO[number]
    received = AUDIT / folder
    archive, delivery = received / archive_name, received / delivery_name
    audit, receipt = AUDIT / audit_name, AUDIT / receipt_name
    audit_doc, delivery_doc = read(audit), read(delivery)
    assert audit_doc.get("status") == "PASS" and audit_doc.get("failedChecks", 0) == 0 and all(x.get("passed") is True for x in audit_doc.get("checks", [])), number
    assert delivery_doc.get("heldIds") == held and delivery_doc.get("acceptedIds") == [] and delivery_doc.get("appliedIds") == [], number
    with zipfile.ZipFile(archive) as z:
        assert z.testzip() is None
    return {"archivePath": archive, "deliveryPath": delivery, "auditPath": audit, "receiptPath": receipt,
            "archive": info(archive), "delivery": info(delivery), "audit": info(audit), "receipt": info(receipt),
            "heldIds": held, "blockerIds": blockers, "decisionId": delivery_doc.get("id")}


def main() -> None:
    head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    branch = subprocess.check_output(["git", "branch", "--show-current"], cwd=ROOT, text=True).strip()
    assert branch == "main"
    now = datetime.now(timezone.utc).isoformat()

    index_path, catalog_path, access_path = ROOT / INDEX, ROOT / CATALOG, ROOT / ACCESS
    index, catalog = read(index_path), read(catalog_path)
    queue288_path = AUDIT / "CURRENT_SPELL_QUEUE_288.json"
    handoff288_path = AUDIT / "CURRENT_HANDOFF_288.json"
    pending288_path = AUDIT / "CURRENT32_PENDING_IDENTITY_AUDIT_288.json"
    q0, h0, p0 = read(queue288_path), read(handoff288_path), read(pending288_path)
    assert q0["currentAuthority"] == h0["currentAuthority"] == p0["authority"] == AUTHORITY
    assert index["authoredCounts"] == {"reviewed": 816, "pending": 32}
    assert index["representationCounts"]["completeReviewedStandaloneProcedures"] == 540
    entries = {row["id"]: row for row in index["entries"]}
    spells = {row["id"]: row for row in catalog["spells"]}
    pending_ids = {row["id"] for row in index["entries"] if row.get("authoredStatus") == "pending-authored-procedure"}
    assert len(pending_ids) == 32 and set(TARGETS) <= pending_ids
    pending_group = next(row for row in q0["currentPendingGroups"] if row["group"] == GROUP)
    assert pending_group["pendingIds"] == TARGETS and pending_group["pendingCount"] == 2
    for sid in TARGETS:
        assert entries[sid]["authoredStatus"] == "pending-authored-procedure"
        assert entries[sid]["sourceStatus"] == "blocked-pending-operational-review"
        assert spells[sid]["id"] == sid

    # Verify prior 233 as a historical target ruling, not an unsent conference.
    prior233_dir = AUDIT / "rank9_miraclereality2_return233_received"
    prior233_archive = prior233_dir / "DD_Rank9_MiracleReality2_Director_Return233_HELD.zip"
    prior233_delivery = prior233_dir / "DD_Rank9_MiracleReality2_Director_Return233_HELD_DELIVERY.json"
    prior233_audit = AUDIT / "RANK9MIRACLEREALITY2_RETURN233_INDEPENDENT_AUDIT.json"
    prior233_receipt = AUDIT / "RANK9MIRACLEREALITY2_RETURN233_RECEIPT.json"
    with zipfile.ZipFile(prior233_archive) as z:
        prior233_decision = json.loads(z.read("DIRECTOR_DECISION.json").decode("utf-8-sig"))
    prior233_blockers = {x["id"]: x["blockerIds"] for x in prior233_decision["perIdentityDecisions"]}
    assert prior233_decision["authority"] == {"reviewedApplied": 811, "pending": 37, "acceptedUnapplied": 0, "completeStandaloneProcedures": 535, "scopedInterfaces": 173}
    assert prior233_decision["heldIds"] == TARGETS and prior233_decision["acceptedIds"] == [] and prior233_decision["appliedIds"] == []
    assert prior233_blockers == {"divine-intervention-greater": ["MR233-B01"], "wish": ["MR233-B02"]}
    assert read(prior233_audit).get("status") == "PASS" and read(prior233_audit).get("checkCount") == 30 and read(prior233_audit).get("failedChecks") == 0

    returns = {n: return_artifacts(n) for n in RETURN_INFO}
    return288 = returns[288]
    assert return288["heldIds"] == ["astral-projection", "imprisonment"]
    hold_entries = [{"returnNumber": n, "heldIds": a["heldIds"], "blockerIds": a["blockerIds"], "archive": a["archive"], "delivery": a["delivery"], "audit": a["audit"], "receipt": a["receipt"]} for n, a in returns.items()]
    prior_target = {"returnNumber": 233, "group": GROUP, "heldIds": TARGETS, "blockerIds": prior233_blockers,
                    "authority": prior233_decision["authority"], "archive": info(prior233_archive), "delivery": info(prior233_delivery),
                    "audit": info(prior233_audit), "receipt": info(prior233_receipt), "status": "PRIOR_HELD_REASSESS_AT_CURRENT_AUTHORITY"}

    # First make Return288 and the 289 pending packet explicit in local tracking.
    return_record = {
        "archive": return288["archive"], "deliveryManifest": return288["delivery"], "decisionId": return288["decisionId"],
        "independentAudit": return288["audit"], "receipt": return288["receipt"], "acceptedIds": [], "appliedIds": [],
        "heldIds": return288["heldIds"], "blockerIds": {"astral-projection": ["PC232-B01"], "imprisonment": ["PC232-B02"]},
        "nextPendingGroup": {"group": GROUP, "pendingIds": TARGETS},
    }
    packet288_path = AUDIT / "RANK9PROJECTIONCONFINEMENT2_PACKET_288.json"
    packet288 = read(packet288_path)
    packet288.update({"status": "RETURN288_AUDITED_HELD_816_32_0", "directorReturn": return_record,
                      "independentReturnAudit": return288["audit"], "returnReceipt": return288["receipt"],
                      "canonicalChanges": False, "applicationChanges": False})
    packet288_path.write_bytes(enc(packet288))
    submission288_path = AUDIT / "RANK9PROJECTIONCONFINEMENT2_PACKET_288_SUBMISSION.json"
    submission288 = read(submission288_path)
    submission288.update({"status": "RETURN288_AUDITED_HELD_816_32_0", "directorReturn": return_record,
                          "independentReturnAudit": return288["audit"], "returnReceipt": return288["receipt"],
                          "canonicalChanges": False, "applicationChanges": False})
    submission288_path.write_bytes(enc(submission288))

    pending288 = read(pending288_path)
    pending288.update({"id": "CURRENT32-PENDING-IDENTITY-AUDIT-288", "recordedAtUtc": now,
                       "status": "RETURN288_AUDITED_HELD_PENDING_PACKET289_816_32_0",
                       "lastDirectorReturn": return_record,
                       "preparedNextGroup": {"group": GROUP, "pendingIds": TARGETS, "pendingCount": 2,
                                             "historicalWorkflow": "Return233 previously held both targets under MR233-B01/B02 at 811/37/0; reassess from current 816/32/0 source without automatic inheritance.",
                                             "freshPacketRequiredForCurrentAuthority": True}})
    pending288_path.write_bytes(enc(pending288))

    q288 = read(queue288_path)
    q288.update({"recordedAtUtc": now, "status": "RETURN288_AUDITED_HELD_816_32_0",
                 "packetStatus": "RETURN288_AUDITED_HELD_816_32_0", "currentReturnArchive": return288["archive"],
                 "currentReturnDelivery": return288["delivery"], "currentReturnAudit": return288["audit"],
                 "currentReturnReceipt": return288["receipt"], "currentReturnDecision": return288["decisionId"],
                 "currentReturnBinding": return288["archive"], "currentReturnHeldIds": return288["heldIds"],
                 "currentReturnAcceptedIds": [], "currentReturnAppliedIds": [], "currentReturnBlockers": return_record["blockerIds"],
                 "currentDirectorPosition": {"stage": "Return288 sealed and independently audited PASS 27/27", "acceptedIds": [], "appliedIds": [],
                                             "heldIds": return288["heldIds"], "blockers": return_record["blockerIds"],
                                             "nextPendingGroup": {"group": GROUP, "pendingIds": TARGETS, "pendingCount": 2, "reportedByDirector": True}},
                 "lastReviewedBatch": {"group": "rank9-projection-confinement2", "pendingIds": return288["heldIds"], "acceptedIds": [],
                                       "appliedIds": [], "heldIds": return288["heldIds"], "blockerIds": return_record["blockerIds"],
                                       "returnArchive": return288["archive"], "returnDelivery": return288["delivery"],
                                       "returnAudit": return288["audit"], "returnReceipt": return288["receipt"]},
                 "nextGroup": GROUP, "nextPendingIds": TARGETS, "nextPendingCount": 2, "githubChanges": False})
    progress = q288.setdefault("directorProgress", [])
    if not any(row.get("stage") == "return288-audited" for row in progress):
        progress.append({"stage": "return288-audited", "recordedAtUtc": now,
            "message": "Return288 ZIP and DELIVERY independently match the Director seal; 27/27 checks pass. Astral Projection and Imprisonment remain held under PC232-B01/B02 at 816/32/0. Next Miracle/Reality2 at current source; preserve prior Return233 MR233-B01/B02 as history."})
    q288["followUpPingsSent"] = 3
    q288["nextPreparedRequest"] = {"group": GROUP, "pendingIds": TARGETS, "pendingCount": 2,
        "status": "PACKET289_PREPARATION_IN_PROGRESS_816_32_0", "freshPacketRequiredForCurrentAuthority": True,
        "historicalWorkflow": "Return233 previously held divine-intervention-greater under MR233-B01 and wish under MR233-B02 at 811/37/0; reassess current source at 816/32/0, preserving history without automatic inheritance.",
        "previousTargetRuling": prior_target, "previousHeldBatches": hold_entries,
        "preservedOriginalQuestions": 24, "focusedAdditionalQuestions": 2, "totalQuestions": 26,
        "requiredMainCases": 4, "futureRequirements": 8, "packet": None, "deliveryManifest": None, "independentAudit": None, "auditReceipt": None}
    row288 = next(row for row in q288["currentPendingGroups"] if row["group"] == GROUP)
    row288.update({"status": "PACKET289_PREPARATION_IN_PROGRESS_816_32_0", "currentAuthority": AUTHORITY,
                   "freshPacketRequiredForCurrentAuthority": True, "priorTargetRuling": prior_target,
                   "mostRecentReturn": {"heldIds": return288["heldIds"], "blockers": return_record["blockerIds"], "audit": return288["audit"]}})
    q288["nextSuggestedGroups"] = [{"group": GROUP, "pendingIds": TARGETS, "pendingCount": 2, "selectedByDirectorReturn": 288}]
    queue288_path.write_bytes(enc(q288))

    handoff288 = read(AUDIT / "CURRENT_HANDOFF_288.json")
    handoff288.update({"recordedAtUtc": now, "status": "RETURN288_AUDITED_HELD_PACKET289_PREPARATION_816_32",
                       "currentReturnBinding": return288["archive"], "currentReturnDelivery": return288["delivery"],
                       "currentReturnAudit": return288["audit"], "currentReturnReceipt": return288["receipt"],
                       "currentReturnDecision": return288["decisionId"], "nextGroup": GROUP, "nextPendingCount": 2,
                       "latestBatch": {"group": "rank9-projection-confinement2", "acceptedIds": [], "appliedIds": [],
                                       "heldIds": return288["heldIds"], "blockerIds": return_record["blockerIds"],
                                       "returnArchive": return288["archive"], "independentAudit": return288["audit"], "receipt": return288["receipt"]},
                       "nextStep": "Prepare and independently audit fresh current-authority Packet289 for only divine-intervention-greater and wish. Preserve Return233's prior MR233-B01/B02 hold as history, not automatic authority; submit to GPT, monitor and ping, audit the sealed return, then apply only exact accepted IDs.",
                       "resumePriority": "Build and independently audit Packet289 from current 816/32/0 source, explicitly carry Return233 target history and Return284–288 unrelated holds; send to GPT, read the browser frequently and ping if needed.",
                       "githubChanges": False})
    handoff288["currentQueueBinding"] = info(queue288_path)
    (AUDIT / "CURRENT_HANDOFF_288.json").write_bytes(enc(handoff288))
    snapshot288_path = AUDIT / "CURRENT_SPELL_REVIEW_SNAPSHOT_288.md"
    snapshot288_path.write_text(
        "# Current Ordinary Spell Review Snapshot 288\n\n"
        "Authority: **816 reviewed/applied / 32 pending / 0 accepted-unapplied**; 540 complete standalone procedures and 173 scoped interfaces.\n\n"
        "Return288 independently passed 27/27 and held astral-projection and imprisonment under PC232-B01/B02. The next group is **Rank9 Miracle/Reality2**: divine-intervention-greater and wish. Return233 previously held these targets under MR233-B01/B02 at 811/37/0; Packet289 will reassess from current source at 816/32/0 without treating the old holds as automatic authority.\n\n"
        "Preserve the Return284–288 holds and all prior acceptances. Packet289 carries the two target histories, current target source records, 24 original questions, two focused additions, four required main cases and eight future requirements. No runtime, implementation, human-play, balance, cosmology, domain-closure, completion or release gate is opened.\n",
        encoding="utf-8")

    # Build fresh queue289 and handoff289 from the reconciled sealed Return288.
    pending289 = copy.deepcopy(pending288)
    pending289.update({"id": "CURRENT32-PENDING-IDENTITY-AUDIT-289", "recordedAtUtc": now,
                       "status": "RETURN288_AUDITED_HELD_PACKET289_PREPARATION_816_32_0",
                       "previousTargetRuling": prior_target, "preparedNextGroup": {"group": GROUP, "pendingIds": TARGETS, "pendingCount": 2,
                       "freshPacketRequiredForCurrentAuthority": True, "status": "PACKET289_PREPARATION_IN_PROGRESS"}})
    pending289_path = AUDIT / "CURRENT32_PENDING_IDENTITY_AUDIT_289.json"
    pending289["id"] = "CURRENT32-PENDING-IDENTITY-AUDIT-289"
    pending289_path.write_bytes(enc(pending289))

    queue289 = copy.deepcopy(q288)
    queue289.update({"id": "SPELL-REVIEW-QUEUE-289", "recordedAtUtc": now, "supersedesQueue": "SPELL-REVIEW-QUEUE-288",
                     "pendingIdentityAudit": info(pending289_path), "status": "PACKET289_PREPARED_PENDING_AUDIT_816_32_0",
                     "packetStatus": "PACKET289_PREPARED_PENDING_AUDIT_816_32_0", "currentPacket": None,
                     "currentDeliveryManifest": None, "currentPreparation": None, "currentPacketAudit": None,
                     "currentPacketAuditReceipt": None, "nextGroup": GROUP, "nextPendingIds": TARGETS,
                     "nextPendingCount": 2, "githubChanges": False,
                     "nextPreparedRequest": copy.deepcopy(q288["nextPreparedRequest"])})
    queue289_path = AUDIT / "CURRENT_SPELL_QUEUE_289.json"
    queue289["queueSnapshot"] = None
    queue289_path.write_bytes(enc(queue289))

    handoff289_doc = copy.deepcopy(handoff288)
    handoff289_doc.update({"id": "CURRENT-HANDOFF-289", "recordedAtUtc": now,
                       "status": "PACKET289_PREPARED_PENDING_AUDIT_816_32",
                       "queue": info(queue289_path), "currentQueueBinding": info(queue289_path),
                       "pendingIdentityAudit": info(pending289_path), "currentPacket": None,
                       "currentPacketDelivery": None, "currentPacketAudit": None, "currentPacketAuditReceipt": None,
                       "nextGroup": GROUP, "nextPendingCount": 2, "currentReturnBinding": return288["archive"],
                       "currentReturnAudit": return288["audit"], "currentReturnReceipt": return288["receipt"],
                       "previousTargetRuling": prior_target,
                       "nextStep": "Independently audit Packet289 for only divine-intervention-greater and wish; preserve Return233's MR233-B01/B02 history and Return284–288 holds; send to GPT and audit its sealed decision before any application.",
                       "resumePriority": "Validate Packet289, then submit and keep reading/pinging GPT until its ZIP and DELIVERY are sealed; apply only exact accepted IDs.",
                       "githubChanges": False})
    handoff289_path = AUDIT / "CURRENT_HANDOFF_289.json"
    handoff289_path.write_bytes(enc(handoff289_doc))
    snapshot289_path = AUDIT / "CURRENT_SPELL_REVIEW_SNAPSHOT_289.md"
    snapshot289_path.write_text(
        "# Current Ordinary Spell Review Snapshot 289\n\n"
        "Authority: **816 reviewed/applied / 32 pending / 0 accepted-unapplied**; 540 complete standalone procedures and 173 scoped interfaces.\n\n"
        "Return288 independently passed 27/27 and held astral-projection and imprisonment under PC232-B01/B02. Packet289 reviews only **divine-intervention-greater** and **wish**. Return233 is an exact prior HOLD under MR233-B01/B02 at 811/37/0; this packet requires reassessment from the current 816/32/0 source, with the earlier ruling preserved as history.\n\n"
        "The review retains 24 original questions, two focused additions, four required main cases, eight future requirements and recent holds from Returns284–288. No spell is applied during review; no runtime or implementation gate is opened.\n",
        encoding="utf-8")
    start = ROOT / "START_HERE.md"
    start_lines = start.read_text(encoding="utf-8-sig").splitlines()
    start_lines[0] = "**Current ordinary spell-review handoff [289](docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT_HANDOFF_289.json):** Return288 independently audited PASS 27/27 and held astral-projection and imprisonment; authority remains **816 reviewed-applied / 32 pending / 0 accepted-unapplied**. Preparing Packet289 for only divine-intervention-greater and wish, with their prior Return233 MR233-B01/B02 hold preserved as history for current-source reassessment."
    start.write_text("\n".join(start_lines) + "\n", encoding="utf-8")

    # Reuse the complete historical Miracle/Reality question and case set;
    # refresh every source binding against the current main working tree.
    old_candidate = read(ROOT / HIST_CANDIDATE)
    old_notes = read(HIST_NOTES)
    old_candidate_file = ROOT / "docs/audit/2026-10-08/full-game/director-spell-review-129/rank9_miraclereality2_current_source_233_prepared/CURRENT_SOURCE_CONFERENCE_CANDIDATE_233.json"
    prior_candidate = read(old_candidate_file)
    assert [row["spellId"] for row in old_candidate["records"]] == TARGETS
    assert len(old_candidate["questions"]) == 24 and len(old_candidate["futureCaseRequirements"]) == 8
    assert len(old_notes["completeOriginalQuestionsUnchanged"]) == 24 and len(old_notes["focusedAdditionalQuestions"]) == 2
    assert len(old_notes["allQuestions"]) == 26 and len(old_notes["requiredNewCases"]) == 4 and len(old_notes["originalFutureCaseRequirementsUnchanged"]) == 8
    historical_bindings = old_candidate["sourceBindings"]
    historical_zip_raw = HIST_ARCHIVE.read_bytes()
    refreshed, changed, source_files = [], [], {}
    with zipfile.ZipFile(HIST_ARCHIVE) as historical_zip:
        assert historical_zip.testzip() is None
        for old in historical_bindings:
            path = old["path"]
            assert safe(path)
            original = historical_zip.read("sources/" + path)
            assert (len(original), sha(original)) == (old["bytes"], old["sha256"])
            current = (ROOT / path).read_bytes()
            row = {"path": path, "bytes": len(current), "sha256": sha(current), "gitBlobSHA1": git_blob_sha(current)}
            refreshed.append(row)
            source_files["sources_current/" + path] = current
            if (row["bytes"], row["sha256"]) != (old["bytes"], old["sha256"]):
                changed.append({"path": path, "historicalBytes": old["bytes"], "historicalSha256": old["sha256"], "currentBytes": row["bytes"], "currentSha256": row["sha256"]})
    assert len(refreshed) == len({x["path"] for x in refreshed}) == 153

    previous_audits = []
    for number, item in returns.items():
        previous_audits.extend([(f"evidence/RETURN{number}_DELIVERY.json", item["deliveryPath"].read_bytes()),
                                 (f"evidence/RETURN{number}_INDEPENDENT_AUDIT.json", item["auditPath"].read_bytes()),
                                 (f"evidence/RETURN{number}_RECEIPT.json", item["receiptPath"].read_bytes())])
    native_placements = sum(len(spells[sid].get("source", {}).get("original", {}).get("placements", [])) for sid in TARGETS)

    candidate = copy.deepcopy(prior_candidate)
    candidate.update({"id": "CURRENT-SOURCE-CONFERENCE-CANDIDATE-289", "recordedAtUtc": now,
        "status": "PREPARED_CURRENT_AUTHORITY_816_32_EXACT_MIRACLE_REALITY2_GROUP", "sourceCommitBase": head,
        "sourceBranch": branch, "currentWorkingTreeSnapshot": True, "currentAuthority": AUTHORITY,
        "currentPendingGroup": {"group": GROUP, "spellIds": TARGETS, "count": 2},
        "historicalWorkflow": {"conference129": "PREPARED_NOT_SENT", "sourceConference01": "PREPARED_UNSENT",
                               "priorDirectorRuling": "Return233 held both identities at 811/37/0; see priorTargetRuling."},
        "sourceBindings": refreshed, "sourceBindingRefresh": {"sourceFiles": len(refreshed), "changedSinceHistoricalCandidate": changed,
            "sourceContentsFromCurrentWorkingTree": True, "sourceCommitBase": head},
        "currentReviewTargets": [{"spellId": sid, "currentIndexEntry": copy.deepcopy(entries[sid]),
            "completeCurrentCatalogSourceAndAccess": copy.deepcopy(spells[sid]),
            "status": "Pending at current 816/32/0; reassess from current source and preserve prior Return233 HOLD as history."} for sid in TARGETS],
        "currentAuthorityEvidence": {"currentIndex": info(index_path), "currentCatalog": info(catalog_path), "currentAccessRegistry": info(access_path),
            "currentQueue": info(queue289_path), "currentHandoff": info(handoff289_path), "currentPendingIdentityAudit": info(pending289_path),
            "latestReturn288Audit": return288["audit"], "priorTargetReturn233": prior_target, "targetIdsStillPending": TARGETS},
        "priorTargetRuling": prior_target, "preservedRecentHolds": hold_entries, "newRuleAdoptions": 0})
    candidate_raw = enc(candidate)

    out = AUDIT / "rank9_miraclereality2_current_source_289_prepared"
    out.mkdir(parents=True, exist_ok=True)
    candidate_path = out / "CURRENT_SOURCE_CONFERENCE_CANDIDATE_289.json"
    context_path = out / "CURRENT_CONTEXT_289.json"
    request_path = out / "REQUEST_289.txt"
    archive_path = out / "DD_Rank9_MiracleReality2_CurrentSource_289.zip"
    delivery_path = out / "DD_Rank9_MiracleReality2_CurrentSource_289_DELIVERY.json"
    candidate_path.write_bytes(candidate_raw)

    context = {"id": "RANK9-MIRACLE-REALITY2-CURRENT-DIRECTOR-CONTEXT-289", "recordedAtUtc": now,
        "sourceCommitBase": head, "sourceBranch": branch, "currentWorkingTreeSnapshot": True, "sourceAuthority": AUTHORITY,
        "targetGroup": {"group": GROUP, "pendingIds": TARGETS, "count": 2}, "currentIndexCounts": index["authoredCounts"],
        "queue": info(queue289_path), "handoff": info(handoff289_path), "pendingIdentityAudit": info(pending289_path),
        "priorTargetRuling": prior_target,
        "priorTargetRulingInterpretation": "The exact Return233 ruling is historical evidence only. Reassess both spells from current source; do not automatically retain or erase the former holds.",
        "latestReturn288": {"archive": return288["archive"], "delivery": return288["delivery"], "audit": return288["audit"], "receipt": return288["receipt"]},
        "preservedRecentHolds": hold_entries, "historicalConference": {"candidate": info(ROOT / HIST_CANDIDATE),
            "notes": info(HIST_NOTES), "archive": info(HIST_ARCHIVE, historical_zip_raw),
            "sourceConferencePreparedUnsent": True},
        "preservation": {"originalQuestions": 24, "focusedAdditionalQuestions": 2, "totalQuestions": 26,
            "requiredMainCases": 4, "futureRequirements": 8, "nativePlacements": native_placements, "newRuleAdoptions": 0},
        "sourceBindings": len(refreshed), "changedHistoricalBindings": changed,
        "currentSourcePacket288": {"archive": q0.get("currentPacket"), "independentAudit": q0.get("currentPacketAudit"),
            "receipt": q0.get("currentPacketAuditReceipt"), "historyCorrection": q0.get("historyCorrection")},
        "canonicalChanges": False, "runtimeExecuted": False, "applicationChanges": False}
    context_raw = enc(context)
    context_path.write_bytes(context_raw)

    request = (
        f"GPT Director — continue ordinary spell review at current authority 816 reviewed/applied / 32 pending / 0 accepted-unapplied (540 complete standalone procedures; 173 scoped interfaces). Review ONLY divine-intervention-greater and wish in {GROUP}.\n\n"
        f"This packet binds a fresh main-source snapshot at HEAD {head} plus 153 refreshed current source files. It includes the exact current index/catalog/access data, queue289/handoff289/pending audit289, the prior Return233 decision and independent audit, the sealed Return288 ZIP and audit, and audited Return284–288 history.\n\n"
        "Prior target ruling: Return233 held divine-intervention-greater under MR233-B01 and wish under MR233-B02 at authority 811/37/0. Preserve this as history, then reassess both targets from the current 816/32/0 source. The historical source-conference material was prepared but unsent; it is not a Director ruling. Do not silently inherit, erase, or apply the old decision.\n\n"
        "Preserve all 24 original questions, two focused additions, four required main cases and eight future requirements. Reconcile each source distinction and the exact current class routes, printed placements, casting costs, source facts, acquisition eligibility and lifecycle. Separate current source facts from missing operational contracts or newly proposed rules. Do not import D&D Divine Intervention/Wish rules, arbitrary limits, percentages, cooldowns, costs, deity behavior, random success, or assumed freeform outcomes.\n\n"
        "Return284–288 holds remain unchanged and outside this review: planar-gates, summon-hosts, reverse-gravity-field, alignment/faction/purification, astral-projection and imprisonment. Preserve all existing acceptances and all downstream gates. Disposition all 26 questions, both procedures, four main cases, eight future requirements and all preserved replay evidence. State exact acceptedIds/appliedIds/heldIds, blocker IDs and minimum missing witnesses, evidence/replay counts, actor-clock status and exact next pending group.\n\n"
        "Do not edit canonical files, apply spells during this review, run supplied source programs or game runtime, or open implementation, human-play, balance, cosmology, domain-closure, completion or release gates. Seal the decision ZIP plus matching DELIVERY.json and continue until both are attached."
    )
    request_raw = request.encode("utf-8")
    request_path.write_bytes(request_raw)

    current_paths = ["START_HERE.md", INDEX, CATALOG, ACCESS,
        "DescentReviewChanges/ReviewBible/data/director/spell_review/remaining_work_queue_66.json", HIST_CANDIDATE,
        "docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT_SPELL_QUEUE_288.json",
        "docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT_HANDOFF_288.json",
        "docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT32_PENDING_IDENTITY_AUDIT_288.json",
        "docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT_SPELL_REVIEW_SNAPSHOT_288.md",
        "docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT_SPELL_QUEUE_289.json",
        "docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT_HANDOFF_289.json",
        "docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT32_PENDING_IDENTITY_AUDIT_289.json",
        "docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT_SPELL_REVIEW_SNAPSHOT_289.md",
        "docs/audit/2026-10-08/full-game/director-spell-review-129/RANK9PROJECTIONCONFINEMENT2_RETURN288_INDEPENDENT_AUDIT.json",
        "docs/audit/2026-10-08/full-game/director-spell-review-129/RANK9PROJECTIONCONFINEMENT2_RETURN288_RECEIPT.json",
        "docs/audit/2026-10-08/full-game/director-spell-review-129/RANK9PROJECTIONCONFINEMENT2_PACKET_288_SUBMISSION.json",
        "docs/audit/2026-10-08/full-game/director-spell-review-129/RANK9MIRACLEREALITY2_RETURN233_INDEPENDENT_AUDIT.json",
        "docs/audit/2026-10-08/full-game/director-spell-review-129/RANK9MIRACLEREALITY2_RETURN233_RECEIPT.json",
        "docs/audit/2026-10-08/full-game/director-spell-review-129/RANK9MIRACLEREALITY2_PACKET_233.json",
        "docs/audit/2026-10-08/full-game/director-spell-review-129/RANK9MIRACLEREALITY2_NEXT_CONFERENCE_NOTES_129.json"]
    current_files = {path: (ROOT / path).read_bytes() for path in current_paths if (ROOT / path).is_file()}
    files = {"CURRENT_CONTEXT_289.json": context_raw, "CURRENT_SOURCE_CONFERENCE_CANDIDATE_289.json": candidate_raw,
        "REQUEST_289.txt": request_raw, "prior_target/RETURN233.zip": prior233_archive.read_bytes(),
        "prior_target/RETURN233_DELIVERY.json": prior233_delivery.read_bytes(),
        "prior_target/RETURN233_INDEPENDENT_AUDIT.json": prior233_audit.read_bytes(),
        "prior_target/RETURN233_RECEIPT.json": prior233_receipt.read_bytes(),
        "history/NEXT_CONFERENCE_NOTES_129.json": HIST_NOTES.read_bytes(),
        "history/SOURCE_CONFERENCE_CANDIDATE_01.json": (ROOT / HIST_CANDIDATE).read_bytes()}
    files.update({"current/" + path: raw for path, raw in current_files.items()})
    files.update(source_files)
    # Prior return ZIPs are not duplicated for the already-audited unrelated holds;
    # their exact manifests, audits and receipts are present, and Packet288 carried
    # the full Return284-287 archives in the same Director thread.
    files.update(previous_audits)
    files["evidence/RETURN288.zip"] = return288["archivePath"].read_bytes()
    files["evidence/RETURN288_DELIVERY.json"] = return288["deliveryPath"].read_bytes()
    files["evidence/RETURN288_INDEPENDENT_AUDIT.json"] = return288["auditPath"].read_bytes()
    files["evidence/RETURN288_RECEIPT.json"] = return288["receiptPath"].read_bytes()
    assert all(safe(name) for name in files)

    rows = []
    with zipfile.ZipFile(archive_path, "w", zipfile.ZIP_DEFLATED, compresslevel=6) as archive:
        for name, raw in sorted(files.items()):
            archive.writestr(name, raw)
            rows.append({"path": name, "bytes": len(raw), "sha256": sha(raw), "crc32": crc(raw)})
        manifest = {"id": "RANK9-MIRACLE-REALITY2-CURRENT-SOURCE-MANIFEST-289", "sourceCommitBase": head,
            "sourceBranch": branch, "sourceAuthority": AUTHORITY, "group": GROUP, "pendingIds": TARGETS,
            "memberCountExcludingSelf": len(rows), "members": rows}
        archive.writestr("MANIFEST.json", enc(manifest))
    with zipfile.ZipFile(archive_path) as archive:
        assert archive.testzip() is None and len(archive.namelist()) == len(rows) + 1 == len(set(archive.namelist()))
        for row in rows:
            assert (len(archive.read(row["path"])), sha(archive.read(row["path"])), crc(archive.read(row["path"]))) == (row["bytes"], row["sha256"], row["crc32"])
        manifest_raw = archive.read("MANIFEST.json")

    archive_info, candidate_info, context_info, request_info = info(archive_path), info(candidate_path, candidate_raw), info(context_path, context_raw), info(request_path, request_raw)
    delivery = {"id": "RANK9-MIRACLE-REALITY2-CURRENT-SOURCE-DELIVERY-289", "status": "PREPARED_UNAUDITED_UNSENT",
        "archive": archive_info, "members": len(rows) + 1, "manifestBindings": len(rows), "sourceCommitBase": head,
        "sourceBranch": branch, "sourceAuthority": AUTHORITY, "group": GROUP, "pendingIds": TARGETS,
        "accepted": False, "applied": False, "candidate": candidate_info, "context": context_info, "request": request_info,
        "historicalCandidate": info(ROOT / HIST_CANDIDATE), "priorTargetRuling": prior_target,
        "sourceBindings": len(refreshed), "changedSourceBindings": changed, "originalQuestions": 24,
        "focusedAdditionalQuestions": 2, "requiredMainCases": 4, "futureRequirements": 8,
        "nativePlacements": native_placements, "preservedRecentHolds": hold_entries,
        "zipMemberCount": len(rows) + 1, "payloadMemberCount": len(rows),
        "memberManifest": {"path": "MANIFEST.json", "bytes": len(manifest_raw), "sha256": sha(manifest_raw), "crc32": crc(manifest_raw)},
        "members": rows,
        "canonicalChanges": False, "applicationChanges": False, "conversation": CHAT}
    delivery_raw = enc(delivery)
    delivery_path.write_bytes(delivery_raw)
    prep_path = AUDIT / "RANK9MIRACLEREALITY2_SOURCE_PREPARATION_289.json"
    packet_path = AUDIT / "RANK9MIRACLEREALITY2_PACKET_289.json"
    prep = {"id": "RANK9MIRACLEREALITY2-SOURCE-PREPARATION-289", "recordedAtUtc": now,
        "status": "PREPARED_UNAUDITED_UNSENT", "sourceCommitBase": head, "sourceBranch": branch,
        "sourceAuthority": AUTHORITY, "targetGroup": GROUP, "pendingIds": TARGETS, "archive": archive_info,
        "deliveryManifest": info(delivery_path, delivery_raw), "candidate": candidate_info, "context": context_info,
        "sourceBindings": len(refreshed), "changedHistoricalBindings": changed, "originalQuestions": 24,
        "focusedAdditionalQuestions": 2, "requiredMainCases": 4, "futureRequirements": 8,
        "nativePlacements": native_placements, "priorTargetRuling": prior_target,
        "canonicalChanges": False, "accepted": False, "applied": False}
    prep_path.write_bytes(enc(prep))
    packet = {"id": "RANK9MIRACLEREALITY2-PACKET-289", "status": "PREPARED_UNAUDITED_UNSENT",
        "group": GROUP, "pendingIds": TARGETS, "sourceAuthority": AUTHORITY, "sourceBranch": branch,
        "sourceCommitBase": head, "archive": archive_info, "deliveryManifest": info(delivery_path, delivery_raw),
        "candidate": candidate_info, "originalQuestions": 24, "focusedAdditionalQuestions": 2,
        "totalQuestions": 26, "requiredMainCases": 4, "futureRequirements": 8,
        "nativePlacements": native_placements, "refreshedSourceBindings": len(refreshed),
        "changedHistoricalBindings": len(changed), "priorTargetRuling": prior_target,
        "preservedRecentHolds": hold_entries, "canonicalChanges": False, "independentAudit": None}
    packet_path.write_bytes(enc(packet))

    # Bind the prepared packet and audit request in the current tracking files.
    prep_info, delivery_info = info(prep_path), info(delivery_path, delivery_raw)
    queue_doc = read(queue289_path)
    queue_doc["currentPacket"] = archive_info
    queue_doc["currentDeliveryManifest"] = delivery_info
    queue_doc["currentPreparation"] = prep_info
    queue_doc["nextPreparedRequest"].update({"status": "PACKET289_PREPARED_UNAUDITED_UNSENT", "packet": archive_info,
        "deliveryManifest": delivery_info, "candidate": candidate_info, "sourcePreparation": prep_info,
        "priorTargetRuling": prior_target})
    queue289_path.write_bytes(enc(queue_doc))
    handoff_doc = read(handoff289_path)
    handoff_doc.update({"currentPacket": archive_info, "currentPacketDelivery": delivery_info,
        "currentPreparation": prep_info, "currentQueueBinding": info(queue289_path),
        "status": "PACKET289_PREPARED_UNAUDITED_816_32", "nextPreparedRequest": queue_doc["nextPreparedRequest"],
        "resumePriority": "Independently audit Packet289, submit it to GPT, read the browser frequently and ping if needed, audit the sealed return, then apply exact accepted IDs only."})
    handoff289_path.write_bytes(enc(handoff_doc))

    print(json.dumps({"status": "PREPARED_UNAUDITED_UNSENT", "sourceCommitBase": head, "branch": branch,
        "authority": AUTHORITY, "targets": TARGETS, "priorTargetBlockers": prior233_blockers,
        "sourceBindings": len(refreshed), "changedHistoricalBindings": len(changed), "questions": 26,
        "mainCases": 4, "futureRequirements": 8, "nativePlacements": native_placements,
        "members": len(rows) + 1, "archiveBytes": archive_info["bytes"], "archiveSha256": archive_info["sha256"],
        "deliveryManifestBytes": len(delivery_raw), "deliveryManifestSha256": sha(delivery_raw),
        "out": str(archive_path), "recentHolds": {n: a["heldIds"] for n, a in returns.items()}}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
