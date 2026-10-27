from __future__ import annotations

import copy
import hashlib
import json
import shutil
import subprocess
import zipfile
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
AUDIT = ROOT / "docs/audit/2026-10-08/full-game/director-spell-review-129"
RECEIVED = AUDIT / "rank9_impactexile4_return205_received"
ZIP = RECEIVED / "DD_Rank9_ImpactExile4_Director_Return205.zip"
DELIVERY = RECEIVED / "DD_Rank9_ImpactExile4_Director_Return205_DELIVERY.json"
AUDIT_JSON = AUDIT / "RANK9IMPACTEXILE4_RETURN205_INDEPENDENT_AUDIT.json"
INDEX = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json"
CATALOG = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json"
P0 = AUDIT / "CURRENT53_PENDING_IDENTITY_AUDIT_203.json"
Q0 = AUDIT / "CURRENT_SPELL_QUEUE_204.json"
H0 = AUDIT / "CURRENT_HANDOFF_204.json"
BACKUP = AUDIT / "authored_review_index.before_impactexile4_205.json"
PKG_REL = Path("DescentReviewChanges/ReviewBible/data/public/spell_candidates/rank9impactexile4_reviewed_205")
PKG = ROOT / PKG_REL
STAGE = PKG.with_name(PKG.name + ".staging")
MAN = ROOT / "DescentReviewChanges/ReviewBible/docs/spells/candidates/RANK9_IMPACT_EXILE4_REVIEWED_205.md"
ACCEPTED = ["eternal-anvil", "transmute-flesh-to-energy", "planar-collapse"]
HELD = ["reverse-gravity-field"]
GROUP_IDS = ["eternal-anvil", "reverse-gravity-field", "transmute-flesh-to-energy", "planar-collapse"]
NEXT = "rank9-illusion-reality5"
NEXT_IDS = ["supreme-illusion", "mirrored-world", "ethereal-disjunction", "illusory-reality", "soul-reflection"]
BEFORE = {"reviewed": 795, "pending": 53}
AFTER = {"reviewed": 798, "pending": 50}
COMPLETE0, COMPLETE1 = 519, 522
REVIEW = "RANK9-IMPACTEXILE4-EXACT-AUTHORED-ACCEPTANCE-205"
APP = "RANK9-IMPACTEXILE4-APPLICATION-205"
DEC = AUDIT / "RANK9IMPACTEXILE4_DIRECTOR_DECISION_205.json"
ACC = AUDIT / "RANK9IMPACTEXILE4_EXACT_ACCEPTANCE_205.json"
RCPT = AUDIT / "RANK9IMPACTEXILE4_RETURN205_RECEIPT.json"
APPFILE = AUDIT / "RANK9IMPACTEXILE4_APPLICATION_205.json"
OPS = AUDIT / "RANK9IMPACTEXILE4_INDEX_OPERATIONS_205.json"
P1 = AUDIT / "CURRENT50_PENDING_IDENTITY_AUDIT_205.json"
Q1 = AUDIT / "CURRENT_SPELL_QUEUE_205.json"
H1 = AUDIT / "CURRENT_HANDOFF_205.json"
VALID = AUDIT / "RANK9IMPACTEXILE4_APPLICATION_VALIDATION_205.json"
SNAP = AUDIT / "CURRENT_SPELL_REVIEW_SNAPSHOT_205.md"
EXPECTED_ARCHIVE_SHA = "9914504bde2c4ac555a38400797aee7739a91b4e4780f95bdd86416a66f4403d"


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def sha_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read(path: Path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def jb(value) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8")


def write(path: Path, value) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(jb(value))


def bind(path: Path, raw: bytes | None = None):
    value = path.read_bytes() if raw is None else raw
    return {"path": path.relative_to(ROOT).as_posix(), "bytes": len(value), "sha256": sha(value)}


def git(*args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True).strip()


def md_sections(markdown: str) -> dict[str, str]:
    lines = markdown.splitlines()
    starts = [(i, line[2:].strip()) for i, line in enumerate(lines) if line.startswith("# ")]
    result = {}
    for position, (start, heading) in enumerate(starts):
        if heading in GROUP_IDS:
            end = starts[position + 1][0] if position + 1 < len(starts) else len(lines)
            result[heading] = "\n".join(lines[start + 1:end]).strip()
    return result


def main() -> None:
    assert read(AUDIT_JSON)["status"] == "PASS", "Independent Return205 audit must pass before application."
    delivery = read(DELIVERY)
    archive_binding = bind(ZIP)
    delivery_binding = bind(DELIVERY)
    audit_binding = bind(AUDIT_JSON)
    assert archive_binding["sha256"] == delivery["sha256"] == EXPECTED_ARCHIVE_SHA
    assert archive_binding["bytes"] == delivery["bytes"]
    assert delivery["acceptedIds"] == ACCEPTED and delivery["heldIds"] == HELD
    assert delivery["applied"] is False and delivery["authorityAtReview"]["pending"] == 53
    assert not PKG.exists() and not STAGE.exists(), "Refusing to replace a candidate package directory."

    index_raw, catalog_raw = INDEX.read_bytes(), CATALOG.read_bytes()
    before, catalog = read(INDEX), read(CATALOG)
    pending_audit, queue_before, handoff_before = read(P0), read(Q0), read(H0)
    pending = {entry["id"] for entry in before["entries"]
               if entry["authoredStatus"] == "pending-authored-procedure"}
    catalog_ids = {entry["id"] for entry in catalog["spells"]}
    assert before["authoredCounts"] == BEFORE and pending_audit["currentAuthority"]["pending"] == 53
    assert pending == set(pending_audit["pendingIds"]) and set(ACCEPTED) <= pending
    assert pending <= catalog_ids and before["representationCounts"]["completeReviewedStandaloneProcedures"] == COMPLETE0
    assert git("rev-parse", "HEAD") == "2de1e419799c5dc2b5e5c423f5abe130605f3c4c"
    assert git("ls-remote", "origin", "refs/heads/codex/ordinary-spell-review-complete").split()[0] == git("rev-parse", "HEAD")

    with zipfile.ZipFile(ZIP, "r") as archive:
        decision = json.loads(archive.read("DIRECTOR_DECISION.json"))
        procedure_envelope = json.loads(archive.read("PROCEDURES.json"))
        questions_doc = json.loads(archive.read("QUESTION_DISPOSITIONS.json"))
        case_dispositions = json.loads(archive.read("CASE_DISPOSITIONS.json"))
        case_index = json.loads(archive.read("CASE_INDEX.json"))
        hold_register = json.loads(archive.read("HOLD_REGISTER.json"))
        outstanding = json.loads(archive.read("OUTSTANDING_CASE_OBLIGATIONS.json"))
        semantic = json.loads(archive.read("INDEPENDENT_SEMANTIC_FAILURE_CHECK.json"))
        source_delivery = json.loads(archive.read("SOURCE_DELIVERY_203.json"))
        next_doc = json.loads(archive.read("NEXT_QUEUE_HANDOFF.json"))["nextGroup"]
        member_rows = {row["path"]: row for row in delivery["members"]}
        spell_map = {entry["id"]: entry for entry in procedure_envelope["spells"]}
        decisions = {entry["id"]: entry for entry in decision["perIdentity"]}
        assert decision["acceptedIds"] == ACCEPTED and decision["heldIds"] == HELD and decision["applied"] is False
        assert set(spell_map) == set(ACCEPTED)
        assert set(decisions) == set(GROUP_IDS)
        assert semantic["acceptedEligibleIds"] == ACCEPTED and semantic["heldIds"] == HELD
        assert [row["id"] for row in decision["currentBlockers"]] == ["IE204-B02"]
        assert outstanding["heldIds"] == HELD and next_doc["group"] == NEXT and next_doc["pendingIds"] == NEXT_IDS
        assert next_doc["freshPacketRequiredForCurrentAuthority"] is True
        for sid in GROUP_IDS:
            old = next(entry for entry in before["entries"] if entry["id"] == sid)
            assert old["authoredStatus"] == "pending-authored-procedure"
            assert old["sourceStatus"] == "blocked-pending-operational-review"
            if sid in ACCEPTED:
                record = spell_map[sid]
                assert record["accepted"] is True and record["applied"] is False
                assert record["completeSourceAndAccess"]["id"] == sid
                assert record["completeSourceAndAccess"]["name"] == old["name"]
                assert record["completeSourceAndAccess"]["status"] == old["sourceStatus"]
                assert decisions[sid]["accepted"] is True and decisions[sid]["applied"] is False
            else:
                assert decisions[sid]["accepted"] is False and decisions[sid]["applied"] is False

        markdown = archive.read("STANDALONE_PROCEDURES.md").decode("utf-8")
        sections = md_sections(markdown)
        assert set(ACCEPTED) <= set(sections)
        accepted_case_ids = {sid: list(spell_map[sid]["caseIds"]) for sid in ACCEPTED}
        accepted_case_bindings = {}
        for sid, ids in accepted_case_ids.items():
            for case_id in ids:
                member = "cases/" + case_id.replace("/", "__") + ".json"
                assert member in member_rows
                accepted_case_bindings[case_id] = {"archiveMember": member, **member_rows[member]}
        assert len(accepted_case_bindings) == sum(map(len, accepted_case_ids.values()))

        accepted_question_ids = sorted({row["id"] for row in questions_doc["dispositions"]
                                         if set(row.get("spellIds", [])) & set(ACCEPTED)})
        accepted_question_records = [copy.deepcopy(row) for row in questions_doc["dispositions"]
                                     if row["id"] in accepted_question_ids]
        accepted_main_cases = [copy.deepcopy(row) for row in case_dispositions["mainCaseDispositions"]
                               if row.get("spellId") in ACCEPTED]
        accepted_future = [copy.deepcopy(row) for row in case_dispositions["futureObligationDispositions"]
                           if set(row.get("acceptedIdentityEvidence", {})) & set(ACCEPTED)]
        accepted_case_dispositions = {
            "id": "IE205-ACCEPTED-CASE-DISPOSITIONS",
            "originalRequiredCasesUnchanged": case_dispositions["originalRequiredCasesUnchanged"],
            "futureObligationsUnchanged": case_dispositions["futureObligationsUnchanged"],
            "mainCaseDispositions": accepted_main_cases,
            "futureObligationDispositions": accepted_future,
        }
        accepted_case_index = [copy.deepcopy(row) for row in case_index if row["spellId"] in ACCEPTED]
        assert len(accepted_case_index) == sum(map(len, accepted_case_ids.values()))
        blocker_record = next(row for row in hold_register["localRecords"] if row["id"] == "IE204-B02")
        blocker_decision = decisions[HELD[0]]
        blocker_map = {HELD[0]: {"blockerIds": blocker_decision["blockingIds"],
                                 "blockerRecords": [copy.deepcopy(blocker_record)],
                                 "retainedHoldIds": copy.deepcopy(blocker_decision["retainedHoldIds"]),
                                 "preciseRemainingWitnesses": copy.deepcopy(outstanding["blockers"][0]["preciseRemainingWitnesses"]),
                                 "retainedInPendingSet": True}}

        STAGE.mkdir(parents=True)
        spells = []
        actor_profiles = json.loads(archive.read("ACTOR_PROFILES.json"))
        for position, sid in enumerate(ACCEPTED):
            record = spell_map[sid]
            native = copy.deepcopy(record["completeSourceAndAccess"])
            question_ids = sorted(row["id"] for row in accepted_question_records if sid in row.get("spellIds", []))
            selected_cases = copy.deepcopy(accepted_case_ids[sid])
            body_profiles = sorted(profile_id for profile_id, profile in actor_profiles.items()
                                   if sid == profile.get("spellId") or sid in profile.get("spellIds", []))
            spells.append({
                "id": sid,
                "name": native["name"],
                "position": position,
                "procedure": {
                    "id": "IE205-STATIC-" + sid.upper().replace("-", "_"),
                    "spellId": sid,
                    "status": "director-accepted static authored procedure; applied to authored review index; runtime disabled",
                    "accepted": True,
                    "applied": False,
                    "nativeCardUnchanged": native,
                    "procedureContent": sections[sid],
                    "sharedRequirements": copy.deepcopy(record["commonProcedure"]),
                    "spellLocalRequirements": copy.deepcopy(record["rules"]),
                    "bodyProfileIds": body_profiles,
                    "questionIds": question_ids,
                    "qualifications": {
                        "directorQualification": record["reviewQualification"],
                        "retainedHoldIds": copy.deepcopy(record["holdIds"]),
                    },
                    "caseIds": selected_cases,
                    "directorDecisionId": decision["id"],
                },
                "directorProcedureRecord": copy.deepcopy(record),
                "nativeCardUnchanged": native,
                "caseIds": selected_cases,
                "questionIds": question_ids,
                "holdIds": copy.deepcopy(record["holdIds"]),
                "runtimeSelectionEnabled": False,
            })

        evidence = {
            "id": "IE205-ACCEPTED-EVIDENCE-BINDINGS",
            "sourceArchive": archive_binding,
            "caseIndexArchiveMember": member_rows["CASE_INDEX.json"],
            "caseDispositionsArchiveMember": member_rows["CASE_DISPOSITIONS.json"],
            "procedureArchiveMember": member_rows["PROCEDURES.json"],
            "acceptedCaseFiles": accepted_case_bindings,
            "acceptedCaseIds": accepted_case_ids,
            "acceptedQuestionIds": accepted_question_ids,
            "questionDispositionsArchiveMember": member_rows["QUESTION_DISPOSITIONS.json"],
            "sourceVerificationArchiveMember": member_rows["SOURCE_VERIFICATION_205.json"],
            "semanticGateArchiveMember": member_rows["INDEPENDENT_SEMANTIC_FAILURE_CHECK.json"],
        }
        write(STAGE / "RETURN_EVIDENCE_BINDINGS.json", evidence)
        write(STAGE / "QUESTION_DISPOSITIONS.json", accepted_question_records)
        write(STAGE / "CASE_DISPOSITIONS.json", accepted_case_dispositions)
        write(STAGE / "CASE_INDEX.json", accepted_case_index)
        write(STAGE / "DIRECTOR_DECISION.json", decision)
        write(STAGE / "INDEPENDENT_SEMANTIC_FAILURE_CHECK.json", semantic)
        write(STAGE / "OUTSTANDING_CASE_OBLIGATIONS.json", outstanding)
        (STAGE / "STANDALONE_PROCEDURES.md").write_text(
            "# Rank9 Impact/Exile4: accepted static procedures\n\n"
            "Only the three individually accepted procedures are included. Their event and source evidence remains bound to the director return archive. Reverse Gravity Field remains pending under IE204-B02.\n\n"
            + "\n\n".join(f"# {sid}\n\n{sections[sid]}" for sid in ACCEPTED) + "\n",
            encoding="utf-8", newline="\n")
        (STAGE / "DIRECTOR_DELIVERY_OBSERVATION.json").write_bytes(DELIVERY.read_bytes())
        (STAGE / "INDEPENDENT_RETURN_AUDIT.json").write_bytes(AUDIT_JSON.read_bytes())

        packet = queue_before["currentPacket"]
        model = {
            "schemaVersion": 1,
            "moduleId": "rank9impactexile4-reviewed-205",
            "status": "THREE_EXACT_STATIC_AUTHORED_PROCEDURES_APPLIED_WITH_ONE_BLOCKED",
            "scope": "Eternal Anvil, Transmute Flesh to Energy, and Planar Collapse are individually accepted and applied to the authored review index. Reverse Gravity Field remains pending under IE204-B02 for sourced crate durability and rated tether/anchor evidence. Native source cards, access routes, status, and all downstream approval gates remain unchanged or disabled.",
            "acceptedIds": ACCEPTED,
            "unacceptedIds": HELD,
            "excludedPendingIds": sorted(pending - set(ACCEPTED)),
            "unacceptedHolds": blocker_map,
            "sharedRequirements": {"scope": "No global/shared rule changes; native cards and class routes unchanged.",
                                   "runtimeSelectionEnabled": False},
            "spells": spells,
            "caseCoverage": {
                "caseCount": len(accepted_case_index),
                "caseIdsBySpell": accepted_case_ids,
                "caseDispositionsBinding": member_rows["CASE_DISPOSITIONS.json"],
                "evidenceBindingsFile": "RETURN_EVIDENCE_BINDINGS.json",
            },
            "returnCounts": delivery["counts"],
            "sourceArchive": archive_binding,
            "deliveryManifest": delivery_binding,
            "independentAudit": audit_binding,
            "submittedSourcePacket": packet,
            "casebookFile": "RETURN_EVIDENCE_BINDINGS.json#/acceptedCaseFiles",
            "casebookSourceArchiveMemberBinding": member_rows["CASE_INDEX.json"],
            "evidenceBindings": bind(STAGE / "RETURN_EVIDENCE_BINDINGS.json"),
            "runtimeSelectionEnabled": False,
            "runtimeTestsExecuted": False,
            "sourceProgramsExecuted": False,
            "implementationApproved": False,
            "humanPlaytested": False,
            "balanceApproved": False,
            "cosmologyModified": False,
            "releaseApproved": False,
            "domainClosure": False,
        }
        write(STAGE / "MODEL.json", model)
        package_manifest = {
            "id": "RANK9-IMPACTEXILE4-PACKAGE-MANIFEST-205",
            "sourceArchive": archive_binding,
            "deliveryManifest": delivery_binding,
            "independentAudit": audit_binding,
            "sourceAnchorCommit": source_delivery["sourceCommit"],
            "files": [],
        }
        for file in sorted(path for path in STAGE.rglob("*") if path.is_file()):
            raw = file.read_bytes()
            package_manifest["files"].append({"path": (PKG_REL / file.relative_to(STAGE)).as_posix(),
                                               "bytes": len(raw), "sha256": sha(raw)})
        write(STAGE / "CANDIDATE_PACKAGE_MANIFEST.json", package_manifest)
        shutil.move(str(STAGE), str(PKG))

    model_binding = bind(PKG / "MODEL.json")
    package_manifest_binding = bind(PKG / "CANDIDATE_PACKAGE_MANIFEST.json")
    evidence_binding = bind(PKG / "RETURN_EVIDENCE_BINDINGS.json")
    MAN.parent.mkdir(parents=True, exist_ok=True)
    MAN.write_bytes((PKG / "STANDALONE_PROCEDURES.md").read_bytes())
    shutil.copyfile(INDEX, BACKUP)
    before_raw = index_raw
    authority_before = copy.deepcopy(pending_audit["currentAuthority"])
    authority_after = {"reviewedApplied": 798, "pending": 50, "acceptedUnapplied": 0,
                       "completeStandaloneProcedures": 522, "scopedInterfaces": 173}

    write(DEC, {
        "id": decision["id"], "returnNumber": 205, "recordedAtUtc": datetime.now(timezone.utc).isoformat(),
        "decision": "THREE_EXACT_IDENTITY_ACCEPTANCES_ONE_RETAINED_BLOCKER",
        "acceptedIds": ACCEPTED, "unacceptedIds": HELD, "blockers": blocker_map,
        "directorReturn": archive_binding, "deliveryManifest": delivery_binding,
        "independentAudit": audit_binding, "authorityAtDecision": authority_before,
        "exactDirectorDecisions": decision["perIdentity"], "qualifications": decision["qualifications"],
        "scope": "Static authorship only; no runtime, implementation, human-play, balance, cosmology, domain closure, completion or release approval.",
        "canonicalFilesChangedByDirector": False,
    })
    acceptance = {
        "id": REVIEW, "recordedAtUtc": datetime.now(timezone.utc).isoformat(),
        "status": "THREE_EXACT_STATIC_AUTHORED_PROCEDURES_ACCEPTED_WITH_ONE_RETAINED_BLOCKER",
        "acceptedIds": ACCEPTED, "unacceptedIds": HELD,
        "directorDecision": bind(DEC), "directorReturn": archive_binding,
        "deliveryManifest": delivery_binding, "independentAudit": audit_binding,
        "candidateEnvelope": model_binding, "candidatePackageManifest": package_manifest_binding,
        "countsBefore": BEFORE, "countsAfter": AFTER,
        "completeReviewedStandaloneProceduresBefore": COMPLETE0,
        "completeReviewedStandaloneProceduresAfter": COMPLETE1,
        "blockers": blocker_map, "runtimeSelectionEnabled": False,
        "canonicalApplicationPerformedByOwner": False,
    }
    write(ACC, acceptance)
    write(RCPT, {
        "id": "RANK9IMPACTEXILE4-RETURN205-RECEIPT",
        "recordedAtUtc": datetime.now(timezone.utc).isoformat(),
        "status": "THREE_ACCEPTED_ONE_HELD_INDEPENDENT_AUDIT_PASSED",
        "reviewedIds": GROUP_IDS, "acceptedIds": ACCEPTED, "unacceptedIds": HELD,
        "blockers": blocker_map, "directorReturn": archive_binding,
        "deliveryManifest": delivery_binding, "independentAudit": audit_binding,
        "sourceAuthority": authority_before, "counts": delivery["counts"],
        "decisionId": decision["id"],
    })
    write(APPFILE, {
        "id": APP, "recordedAtUtc": datetime.now(timezone.utc).isoformat(),
        "status": "APPLIED_THREE_EXACT_AUTHORED_PROCEDURES_WITH_ONE_RETAINED_BLOCKER",
        "ownerInstruction": "Apply each exact director-accepted ordinary-spell batch, push it to GitHub, and continue until pending reaches zero.",
        "acceptedIds": ACCEPTED, "unacceptedIds": HELD,
        "directorAcceptance": bind(ACC), "directorDecision": bind(DEC),
        "directorReturnReceipt": bind(RCPT), "directorReturn": archive_binding,
        "deliveryManifest": delivery_binding, "independentAudit": audit_binding,
        "candidateEnvelope": model_binding, "candidatePackageManifest": package_manifest_binding,
        "evidenceBindings": evidence_binding, "manuscript": bind(MAN),
        "indexBefore": bind(BACKUP, before_raw), "countsBefore": BEFORE, "countsAfter": AFTER,
        "completeReviewedStandaloneProcedures": {"before": COMPLETE0, "after": COMPLETE1},
        "sourceStatusPreservedAsBlocked": True, "catalogChanged": False,
        "runtimeSelectionEnabled": False,
    })
    application_binding = bind(APPFILE)

    after = copy.deepcopy(before)
    operations = []
    for position, sid in enumerate(ACCEPTED):
        index = next(i for i, entry in enumerate(before["entries"]) if entry["id"] == sid)
        old = before["entries"][index]
        new = copy.deepcopy(old)
        new.update({
            "authoredStatus": "reviewed-authored-operational-playtest",
            "procedureFile": "../spell_candidates/rank9impactexile4_reviewed_205/MODEL.json",
            "procedurePointer": f"/spells/{position}/procedure",
            "wholeCardPointer": f"/spells/{position}",
            "sourceCatalogWholeCardPointer": old.get("sourceCatalogWholeCardPointer") or old["wholeCardPointer"],
            "wholeCardIdField": "id",
            "procedureTextPointer": f"/spells/{position}/procedure/procedureContent",
            "directorProcedureRecordPointer": f"/spells/{position}/directorProcedureRecord",
            "sharedRulesPointer": f"/spells/{position}/procedure/sharedRequirements",
            "manuscript": "../../../docs/spells/candidates/RANK9_IMPACT_EXILE4_REVIEWED_205.md",
            "reviewId": APP,
            "runtimeSelectionEnabled": False,
            "historicalCandidateLabelsPreserved": True,
            "completeEvidenceRoot": PKG_REL.as_posix(),
            "completeEnvelopeBinding": model_binding,
            "caseEvidenceBindings": evidence_binding,
            "sourceArchiveBinding": archive_binding,
            "deliveryManifestBinding": delivery_binding,
            "candidatePackageManifestBinding": package_manifest_binding,
            "procedureSourceBinding": bind(DEC),
            "authoredAcceptanceReceipt": bind(ACC),
            "authoredApplicationReceipt": application_binding,
        })
        assert old["sourceStatus"] == new["sourceStatus"] == "blocked-pending-operational-review"
        operations.append({"op": "replace-entry", "identity": sid, "index": index,
                           "before": copy.deepcopy(old), "after": copy.deepcopy(new)})
        after["entries"][index] = new
    after["additionalStandaloneEnvelopes"].append({
        "file": "../spell_candidates/rank9impactexile4_reviewed_205/MODEL.json",
        "binding": model_binding, "reviewId": REVIEW, "acceptedIds": ACCEPTED,
        "unacceptedIds": HELD, "excludedPendingIds": sorted(pending - set(ACCEPTED)),
        "authority": bind(ACC), "applicationReceipt": APPFILE.relative_to(ROOT).as_posix(),
        "sourceArchive": archive_binding, "deliveryManifest": delivery_binding,
        "evidenceBindings": evidence_binding, "candidatePackageManifestBinding": package_manifest_binding,
        "scope": acceptance["status"], "runtimeSelectionEnabled": False,
    })
    after["authoredCounts"] = AFTER
    after["representationCounts"]["completeReviewedStandaloneProcedures"] = COMPLETE1
    pending_after = {entry["id"] for entry in after["entries"]
                     if entry["authoredStatus"] == "pending-authored-procedure"}
    assert pending_after == pending - set(ACCEPTED) and len(pending_after) == 50
    inverse = copy.deepcopy(after)
    for operation in operations:
        inverse["entries"][operation["index"]] = copy.deepcopy(operation["before"])
    inverse["additionalStandaloneEnvelopes"] = inverse["additionalStandaloneEnvelopes"][:-1]
    inverse["authoredCounts"] = copy.deepcopy(before["authoredCounts"])
    inverse["representationCounts"] = copy.deepcopy(before["representationCounts"])
    assert inverse == before
    after_raw = jb(after)
    temporary = INDEX.with_suffix(".json.impactexile205.tmp")
    temporary.write_bytes(after_raw)
    temporary.replace(INDEX)
    assert CATALOG.read_bytes() == catalog_raw
    write(OPS, {"id": "RANK9IMPACTEXILE4-INDEX-OPERATIONS-205",
                "before": bind(BACKUP, before_raw), "after": bind(INDEX, after_raw),
                "operations": operations, "inverseSemanticExact": True,
                "onlyIdentityIds": ACCEPTED})

    groups = []
    for old_group in queue_before["currentPendingGroups"]:
        remaining = [sid for sid in old_group["pendingIds"] if sid in pending_after]
        if not remaining:
            continue
        group = copy.deepcopy(old_group)
        group["pendingIds"] = remaining
        group["pendingCount"] = len(remaining)
        if group["group"] == "rank9-impact-exile4":
            group.update({
                "status": "PARTIAL_RETURN205_THREE_ACCEPTED_APPLIED_ONE_HELD_IE204_B02",
                "freshPacketRequiredForCurrentAuthority": True,
                "blockingReturn": {"ids": HELD, "blockers": {HELD[0]: ["IE204-B02"]},
                                   "receipt": RCPT.relative_to(ROOT).as_posix()},
            })
        if group["group"] == NEXT:
            group.update({"status": "PENDING_FRESH_PACKET_FOR_CURRENT_AUTHORITY",
                          "freshPacketRequiredForCurrentAuthority": True})
        groups.append(group)
    next_record = next(group for group in groups if group["group"] == NEXT)
    authority = authority_after
    pending_doc = {key: copy.deepcopy(value) for key, value in pending_audit.items()
                   if key.startswith("retainedReturn")}
    pending_doc.update({
        "id": "CURRENT50-PENDING-IDENTITY-AUDIT-205",
        "recordedAtUtc": datetime.now(timezone.utc).isoformat(),
        "status": "PASSED_EXACT_CURRENT_INDEX_PENDING_SET",
        "indexBinding": bind(INDEX, after_raw), "catalogBinding": bind(CATALOG, catalog_raw),
        "authoredCounts": AFTER, "pendingCount": 50, "pendingIds": sorted(pending_after),
        "allPendingExistInSourceCatalog": pending_after <= catalog_ids, "acceptedUnapplied": 0,
        "retainedReturn205Blockers": {
            HELD[0]: {"blockerIds": ["IE204-B02"],
                      "reasons": [outstanding["blockers"][0]["minimalCorrection"]],
                      "retainedHoldIds": blocker_decision["retainedHoldIds"]}
        },
        "closed335AndCompletedCohortsReopened": False,
        "currentAuthority": authority,
    })
    assert pending_doc["allPendingExistInSourceCatalog"] is True
    write(P1, pending_doc)
    next_request = {
        "group": NEXT, "pendingIds": next_record["pendingIds"], "pendingCount": len(NEXT_IDS),
        "status": "PENDING_FRESH_PACKET_FOR_CURRENT_AUTHORITY",
        "freshPacketRequiredForCurrentAuthority": True,
        "candidate": next_doc["candidate"], "archive": next_doc["archive"],
    }
    q1 = copy.deepcopy(queue_before)
    q1.update({
        "id": "SPELL-REVIEW-QUEUE-205", "recordedAtUtc": datetime.now(timezone.utc).isoformat(),
        "currentAuthority": authority, "pendingCount": 50, "currentPendingGroups": groups,
        "justAppliedBatch": {"reviewId": REVIEW, "ids": ACCEPTED, "count": len(ACCEPTED),
                             "applicationReceipt": APPFILE.relative_to(ROOT).as_posix(),
                             "directorAcceptance": ACC.relative_to(ROOT).as_posix(),
                             "independentAudit": AUDIT_JSON.relative_to(ROOT).as_posix()},
        "pendingIdentityAudit": {"path": P1.relative_to(ROOT).as_posix(), "pending": 50,
                                 "sha256": sha(P1.read_bytes())},
        "nextGroup": NEXT, "next": next_request, "nextPreparedRequest": next_request,
        "packetStatus": "RANK9_IMPACT_EXILE4_RETURN205_THREE_APPLIED_ONE_HELD_798_50_NEXT_RANK9_ILLUSION_REALITY5",
        "currentReturnBinding": archive_binding, "currentReturnAudit": audit_binding,
        "currentReturnDelivery": delivery_binding, "currentReturnReceipt": bind(RCPT),
    })
    for key in ("sourceConferencePrepared", "currentPacket", "currentPacketDelivery", "currentPreparation"):
        q1.pop(key, None)
    q1.pop("currentReturnCarryForwardAudit", None)
    q1["currentSubmission"] = bind(RCPT)
    q1["currentSubmissionBinding"] = bind(RCPT)
    write(Q1, q1)
    queue_binding = bind(Q1)

    h1 = copy.deepcopy(handoff_before)
    h1.update({
        "id": "CURRENT-HANDOFF-205", "recordedAtUtc": datetime.now(timezone.utc).isoformat(),
        "status": "RANK9_IMPACT_EXILE4_RETURN205_THREE_APPLIED_ONE_HELD_NEXT_RANK9_ILLUSION_REALITY5_50_PENDING",
        "currentAuthority": authority, "currentIndexBinding": bind(INDEX, after_raw),
        "currentCatalogBinding": bind(CATALOG, catalog_raw),
        "pendingIdentityAudit": {"id": pending_doc["id"], "path": P1.relative_to(ROOT).as_posix(),
                                 "pendingCount": 50, "sha256": sha(P1.read_bytes())},
        "appliedThisStep": {"reviewId": REVIEW, "ids": ACCEPTED, "count": len(ACCEPTED),
                            "applicationReceipt": APPFILE.relative_to(ROOT).as_posix(),
                            "directorAcceptance": ACC.relative_to(ROOT).as_posix(),
                            "independentAudit": AUDIT_JSON.relative_to(ROOT).as_posix(),
                            "applicationValidation": {"path": VALID.relative_to(ROOT).as_posix()}},
        "unacceptedThisStep": {"ids": HELD, "blockers": {HELD[0]: ["IE204-B02"]},
                                "retainedInPendingSet": True},
        "nextGroup": NEXT, "nextPendingCount": len(NEXT_IDS), "nextPendingIds": NEXT_IDS,
        "nextPreparedRequest": next_request, "currentQueueBinding": queue_binding,
        "currentQueue": {"path": Q1.relative_to(ROOT).as_posix()},
        "currentReturnBinding": archive_binding, "currentReturnDelivery": delivery_binding,
        "independentAuditBinding": audit_binding, "currentReturnAudit": audit_binding,
        "parentHandoff": H0.relative_to(ROOT).as_posix(),
        "currentSubmissionBinding": bind(RCPT), "currentReturnReceipt": bind(RCPT),
        "resumePriority": "Prepare a fresh Rank9 Illusion/Reality5 packet at 798/50 and send it to the GPT director. Independently audit each return, apply and push only exact accepted IDs, keep Reverse Gravity Field pending under IE204-B02, and continue the queue until pending is zero.",
    })
    for key in ("sourceConferencePrepared", "currentPacket", "currentPacketDelivery", "currentPreparation"):
        h1.pop(key, None)
    h1.pop("currentReturnCarryForwardAudit", None)
    write(H1, h1)
    shutil.copyfile(MAN, AUDIT / "RANK9_IMPACT_EXILE4_REVIEWED_205.md")
    SNAP.write_text(
        "# Current ordinary spell-review checkpoint 205\n\n"
        f"Return205 passed {read(AUDIT_JSON)['checksPassed']} independent checks, including all {read(AUDIT_JSON)['outerMembersChecked']} archive members, {read(AUDIT_JSON)['caseEventsChecked']} reversible event traces, {read(AUDIT_JSON)['sourceProofPathsChecked']} source-proof paths, and {read(AUDIT_JSON)['sourceBindingsChecked']} refreshed source bindings. Applied exactly {', '.join(ACCEPTED)} as static authored procedures. Reverse Gravity Field remains pending under IE204-B02 for sourced crate durability and rated tether/anchor evidence. Authority: **798 reviewed / 50 pending / 0 accepted-unapplied**, 522 complete standalone procedures. Next: Rank9 Illusion/Reality5. Runtime and downstream approval gates remain disabled.\n",
        encoding="utf-8", newline="\n")
    start = ROOT / "START_HERE.md"
    prior_start = start.read_text(encoding="utf-8-sig") if start.exists() else ""
    start.write_text(
        f"**Current ordinary spell-review handoff [205](docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT_HANDOFF_205.json):** Applied exactly {', '.join(ACCEPTED)}. Authority is **798 reviewed / 50 pending / 0 accepted-unapplied**. Reverse Gravity Field remains pending under IE204-B02. Next group: Rank9 Illusion/Reality5.\n\n" + prior_start,
        encoding="utf-8", newline="\n")

    validations = [
        ("Return archive, delivery manifest and independent audit match recorded bindings",
         sha_file(ZIP) == archive_binding["sha256"] and sha_file(DELIVERY) == delivery_binding["sha256"]
         and read(AUDIT_JSON)["status"] == "PASS"),
        ("Exactly the three director-accepted IDs were applied and Reverse Gravity Field remains pending",
         [operation["identity"] for operation in operations] == ACCEPTED and HELD[0] in pending_after),
        ("Authority advanced from 795/53/519 to 798/50/522",
         after["authoredCounts"] == AFTER
         and after["representationCounts"]["completeReviewedStandaloneProcedures"] == COMPLETE1),
        ("Pending identity set is exactly the previous set minus three acceptances",
         pending_after == pending - set(ACCEPTED)),
        ("Index inverse is exact and catalog bytes are unchanged",
         inverse == before and CATALOG.read_bytes() == catalog_raw),
        ("Every candidate package file matches its package manifest",
         all((ROOT / item["path"]).is_file()
             and (ROOT / item["path"]).stat().st_size == item["bytes"]
             and sha_file(ROOT / item["path"]) == item["sha256"]
             for item in package_manifest["files"])),
        ("Accepted evidence binds all 37 accepted case files in the Return205 archive",
         len(accepted_case_bindings) == 37 and
         all(item["archiveMember"] in member_rows for item in accepted_case_bindings.values())),
        ("Next group matches GPT handoff and remains pending for a fresh packet",
         q1["nextGroup"] == NEXT and next_record["pendingIds"] == NEXT_IDS and
         next_record["pendingCount"] == len(NEXT_IDS)
         and q1["next"]["freshPacketRequiredForCurrentAuthority"] is True),
        ("Runtime and downstream approval gates remain disabled",
         all(model[key] is False for key in ("runtimeSelectionEnabled", "runtimeTestsExecuted",
             "sourceProgramsExecuted", "implementationApproved", "humanPlaytested",
             "balanceApproved", "cosmologyModified", "releaseApproved", "domainClosure"))),
        ("No closed feat or completed cohort was reopened",
         pending_doc["closed335AndCompletedCohortsReopened"] is False
         and set(ACCEPTED) <= set(pending_audit["pendingIds"])),
    ]
    validation = {
        "id": "RANK9IMPACTEXILE4-APPLICATION-VALIDATION-205",
        "recordedAtUtc": datetime.now(timezone.utc).isoformat(),
        "status": "PASS" if all(item[1] for item in validations) else "FAIL",
        "checksPassed": sum(item[1] for item in validations),
        "checksFailed": sum(not item[1] for item in validations),
        "checks": [{"check": name, "passed": passed} for name, passed in validations],
        "acceptedIds": ACCEPTED, "unacceptedIds": HELD,
        "countsBefore": {**BEFORE, "completeReviewedStandaloneProcedures": COMPLETE0},
        "countsAfter": {**AFTER, "completeReviewedStandaloneProcedures": COMPLETE1},
        "indexBefore": bind(BACKUP, before_raw), "indexAfter": bind(INDEX),
        "catalogUnchanged": bind(CATALOG, catalog_raw), "applicationReceipt": bind(APPFILE),
        "independentAudit": bind(AUDIT_JSON), "nextGroup": NEXT,
    }
    write(VALID, validation)
    if validation["status"] != "PASS":
        raise SystemExit("Application validation failed; inspect the validation report.")
    print(json.dumps({
        "status": validation["status"], "checksPassed": validation["checksPassed"],
        "acceptedIds": ACCEPTED, "unacceptedIds": HELD, "authority": authority,
        "nextGroup": NEXT, "pendingAudit": P1.relative_to(ROOT).as_posix(),
        "independentAudit": read(AUDIT_JSON)["status"], "candidateManifest": package_manifest_binding,
        "candidateFiles": len(package_manifest["files"]),
    }, indent=2))


if __name__ == "__main__":
    main()
