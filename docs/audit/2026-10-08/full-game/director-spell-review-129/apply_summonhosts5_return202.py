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
RECEIVED = AUDIT / "rank9_summonhosts5_return202_received"
ZIP = RECEIVED / "DD_Rank9_SummonHosts5_Director_Return202.zip"
DELIVERY = RECEIVED / "DD_Rank9_SummonHosts5_Director_Return202_DELIVERY.json"
AUDIT_JSON = AUDIT / "RANK9_SUMMONHOSTS5_RETURN202_INDEPENDENT_AUDIT.json"
INDEX = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json"
CATALOG = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json"
Q0, H0, P0 = (AUDIT / name for name in (
    "CURRENT_SPELL_QUEUE_201.json", "CURRENT_HANDOFF_201.json",
    "CURRENT55_PENDING_IDENTITY_AUDIT_201.json"))
BACKUP = AUDIT / "authored_review_index.before_summonhosts5_202.json"
PKG_REL = Path("DescentReviewChanges/ReviewBible/data/public/spell_candidates/rank9summonhosts5_reviewed_202")
PKG = ROOT / PKG_REL
STAGE = PKG.with_name(PKG.name + ".staging")
MAN = ROOT / "DescentReviewChanges/ReviewBible/docs/spells/candidates/RANK9_SUMMON_HOSTS5_REVIEWED_202.md"
ACCEPTED = ["conjure-magmatic-wyrm", "planar-army"]
UNACCEPTED = ["summon-elemental-avatar", "summon-herald-of-the-planes", "summon-avatar-of-decay"]
GROUP_IDS = ["summon-elemental-avatar", "conjure-magmatic-wyrm", "planar-army",
             "summon-herald-of-the-planes", "summon-avatar-of-decay"]
NEXT = "rank9-impact-exile4"
NEXT_IDS = ["eternal-anvil", "reverse-gravity-field", "transmute-flesh-to-energy", "planar-collapse"]
BEFORE = {"reviewed": 793, "pending": 55}
AFTER = {"reviewed": 795, "pending": 53}
COMPLETE0, COMPLETE1 = 517, 519
REVIEW = "RANK9-SUMMONHOSTS5-EXACT-AUTHORED-ACCEPTANCE-202"
APP = "RANK9-SUMMONHOSTS5-APPLICATION-202"
DEC = AUDIT / "RANK9_SUMMONHOSTS5_DIRECTOR_DECISION_202.json"
ACC = AUDIT / "RANK9_SUMMONHOSTS5_EXACT_ACCEPTANCE_202.json"
RCPT = AUDIT / "RANK9_SUMMONHOSTS5_RETURN202_RECEIPT.json"
APPFILE = AUDIT / "RANK9_SUMMONHOSTS5_APPLICATION_202.json"
OPS = AUDIT / "RANK9_SUMMONHOSTS5_INDEX_OPERATIONS_202.json"
P1 = AUDIT / "CURRENT53_PENDING_IDENTITY_AUDIT_202.json"
Q1 = AUDIT / "CURRENT_SPELL_QUEUE_202.json"
H1 = AUDIT / "CURRENT_HANDOFF_202.json"
VALID = AUDIT / "RANK9_SUMMONHOSTS5_APPLICATION_VALIDATION_202.json"
SNAP = AUDIT / "CURRENT_SPELL_REVIEW_SNAPSHOT_202.md"


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def sha_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


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
    for pos, (start, heading) in enumerate(starts):
        if heading in GROUP_IDS:
            end = starts[pos + 1][0] if pos + 1 < len(starts) else len(lines)
            result[heading] = "\n".join(lines[start + 1:end]).strip()
    return result


def main() -> None:
    outputs = [BACKUP, MAN, DEC, ACC, RCPT, APPFILE, OPS, P1, Q1, H1, VALID, SNAP]
    assert read(AUDIT_JSON)["status"] == "PASS_WITH_THREE_EXACT_BLOCKERS"
    assert read(AUDIT_JSON)["checksPassed"] == 1484
    assert all(not path.exists() for path in outputs)
    assert not PKG.exists() and not STAGE.exists()

    delivery = read(DELIVERY)
    baseline = {
        "reviewedApplied": 793, "pending": 55, "acceptedUnapplied": 0,
        "completeStandaloneProcedures": 517, "scopedInterfaces": 173,
    }
    before_raw, catalog_raw = INDEX.read_bytes(), CATALOG.read_bytes()
    before, catalog = read(INDEX), read(CATALOG)
    q0, h0, p0 = map(read, (Q0, H0, P0))
    commit, branch = git("rev-parse", "HEAD"), git("branch", "--show-current")
    rows = {entry["id"]: entry for entry in before["entries"]}
    cats = {entry["id"] for entry in catalog["spells"]}
    live = {entry["id"] for entry in before["entries"]
            if entry["authoredStatus"] == "pending-authored-procedure"}
    assert before["authoredCounts"] == BEFORE
    assert before["representationCounts"]["completeReviewedStandaloneProcedures"] == COMPLETE0
    assert len(live) == 55 and set(GROUP_IDS) <= live and set(p0["pendingIds"]) == live
    assert p0["indexBinding"]["sha256"] == sha(before_raw)
    assert q0["currentAuthority"] == baseline and q0["pendingCount"] == 55
    assert h0["currentAuthority"] == baseline
    assert delivery["acceptedIds"] == ACCEPTED and delivery["unacceptedIds"] == UNACCEPTED
    assert delivery["applied"] is False
    assert delivery["boundCanonicalAuthorityUnchanged"] == baseline
    timestamp = datetime.now(timezone.utc).isoformat()

    with zipfile.ZipFile(ZIP) as archive:
        director = json.loads(archive.read("DIRECTOR_DECISION.json"))
        current_authority = json.loads(archive.read("CURRENT_AUTHORITY.json"))
        spell_records = json.loads(archive.read("PROCEDURES.json"))
        spell_map = {entry["id"]: entry for entry in spell_records}
        decisions = {entry["spellId"]: entry for entry in director["perIdentity"]}
        hold_register = json.loads(archive.read("HOLD_REGISTER.json"))
        next_doc = json.loads(archive.read("NEXT_QUEUE_GROUP.json"))["nextGroupUnchanged"]
        member_rows = {item["path"]: item for item in delivery["members"]}
        evidence_members = {item["path"]: item for item in delivery["members"]}

        assert current_authority["sourceAuthority"] == baseline
        assert current_authority["sourceCommit"] == "0a7778f059bbeeba7e4a998c83bc3562a96abd52"
        assert director["acceptedIds"] == ACCEPTED and director["unacceptedIds"] == UNACCEPTED
        assert director["applied"] is False
        assert delivery["boundCanonicalAuthorityUnchanged"] == baseline
        assert next_doc["group"] == NEXT and next_doc["pendingIds"] == NEXT_IDS
        assert next_doc["pendingCount"] == len(NEXT_IDS) and next_doc["freshPacketRequiredForCurrentAuthority"] is True
        assert set(spell_map) == set(decisions) == set(GROUP_IDS)
        assert all(decisions[s]["accepted"] and not decisions[s]["applied"]
                   and not decisions[s]["blockerIds"] for s in ACCEPTED)
        assert all(not decisions[s]["accepted"] and not decisions[s]["applied"]
                   and decisions[s]["blockerIds"] for s in UNACCEPTED)
        for sid in GROUP_IDS:
            old = rows[sid]
            rec = spell_map[sid]
            native = rec["nativeSourceAndAccess"]
            assert old["sourceStatus"] == "blocked-pending-operational-review"
            assert old["authoredStatus"] == "pending-authored-procedure"
            assert native["id"] == sid and native["name"] == old["name"]
            assert native["status"] == old["sourceStatus"]
            assert rec["accepted"] == decisions[sid]["accepted"] and rec["applied"] is False

        markdown = archive.read("STANDALONE_PROCEDURES.md").decode("utf-8")
        sections = md_sections(markdown)
        assert set(ACCEPTED) <= set(sections)
        cases = json.loads(archive.read("CASE_DISPOSITIONS.json"))
        questions = json.loads(archive.read("QUESTION_DISPOSITIONS.json"))
        future = json.loads(archive.read("FUTURE_OBLIGATION_DISPOSITIONS.json"))
        case_index = json.loads(archive.read("CASE_INDEX.json"))
        proc_member = {sid: f"procedures/{sid}.json" for sid in GROUP_IDS}
        accepted_case_ids = {sid: list(spell_map[sid]["caseIds"]) for sid in ACCEPTED}
        accepted_case_bindings = {}
        for sid, case_ids in accepted_case_ids.items():
            for case_id in case_ids:
                member = "cases/" + case_id.replace("/", "__") + ".json"
                assert member in member_rows
                accepted_case_bindings[case_id] = {"archiveMember": member, **member_rows[member]}

        blocker_map = {}
        local_holds = {item["id"]: item for item in hold_register["localRecords"]}
        for sid in UNACCEPTED:
            ids = decisions[sid]["blockerIds"]
            records = [copy.deepcopy(local_holds[bid]) for bid in ids]
            assert records and all(item["blocking"] and sid in item["spellIds"] for item in records)
            blocker_map[sid] = {"blockerIds": ids, "blockerRecords": records,
                                "retainedHoldIds": decisions[sid]["holdIds"]}

        STAGE.mkdir(parents=True)
        spells = []
        for pos, sid in enumerate(ACCEPTED):
            rec = spell_map[sid]
            native = copy.deepcopy(rec["nativeSourceAndAccess"])
            question_ids = copy.deepcopy(rec["questionIds"])
            selected_cases = copy.deepcopy(accepted_case_ids[sid])
            spells.append({
                "id": sid,
                "name": rows[sid]["name"],
                "position": pos,
                "procedure": {
                    "id": "SH202-STATIC-" + sid.upper().replace("-", "_"),
                    "spellId": sid,
                    "status": "director-accepted static authored procedure; applied to authored review index; runtime disabled",
                    "accepted": True,
                    "applied": False,
                    "nativeCardUnchanged": native,
                    "procedureContent": sections[sid],
                    "sharedRequirements": copy.deepcopy(rec["commonProcedure"]),
                    "spellLocalRequirements": copy.deepcopy(rec["spellLocalProcedure"]),
                    "bodyProfileIds": copy.deepcopy(rec["bodyProfileIds"]),
                    "questionIds": question_ids,
                    "qualifications": {
                        "directorQualification": rec["qualification"],
                        "retainedHoldIds": copy.deepcopy(rec["holdIds"]),
                    },
                    "caseIds": selected_cases,
                    "directorDecisionId": director["id"],
                },
                "directorProcedureRecord": copy.deepcopy(rec),
                "nativeCardUnchanged": native,
                "caseIds": selected_cases,
                "questionIds": question_ids,
                "holdIds": copy.deepcopy(rec["holdIds"]),
                "runtimeSelectionEnabled": False,
            })

        accepted_question_ids = {qid for sid in ACCEPTED for qid in spell_map[sid]["questionIds"]}
        question_records = [copy.deepcopy(item) for item in questions if item["id"] in accepted_question_ids]
        future_records = [copy.deepcopy(item) for item in future
                          if set(item.get("spellIds", [])) & set(ACCEPTED)]
        evidence = {
            "id": "SH202-ACCEPTED-EVIDENCE-BINDINGS",
            "sourceArchive": bind(ZIP),
            "casebookArchiveMember": member_rows["CASEBOOK.json"],
            "procedureArchiveMembers": {sid: member_rows[proc_member[sid]] for sid in ACCEPTED},
            "caseDispositionsArchiveMember": member_rows["CASE_DISPOSITIONS.json"],
            "caseIndexArchiveMember": member_rows["CASE_INDEX.json"],
            "acceptedCaseFiles": accepted_case_bindings,
            "acceptedCaseIds": accepted_case_ids,
            "acceptedQuestionIds": sorted(accepted_question_ids),
            "questionDispositionsArchiveMember": member_rows["QUESTION_DISPOSITIONS.json"],
            "futureObligationDispositionsArchiveMember": member_rows["FUTURE_OBLIGATION_DISPOSITIONS.json"],
            "sourceBindingsArchiveMember": member_rows["SOURCE_BINDINGS.json"],
        }
        write(STAGE / "RETURN_EVIDENCE_BINDINGS.json", evidence)
        write(STAGE / "QUESTION_DISPOSITIONS.json", question_records)
        write(STAGE / "FUTURE_OBLIGATION_DISPOSITIONS.json", future_records)
        (STAGE / "STANDALONE_PROCEDURES.md").write_text(
            "# Rank9 Summon Hosts5: accepted static procedures\n\n"
            "Only the two individually accepted procedures are included here. Their complete event and source evidence remains bound to the director return archive.\n\n"
            + "\n\n".join(f"# {sid}\n\n{sections[sid]}" for sid in ACCEPTED) + "\n",
            encoding="utf-8", newline="\n")
        (STAGE / "DIRECTOR_DELIVERY_OBSERVATION.json").write_bytes(DELIVERY.read_bytes())
        (STAGE / "INDEPENDENT_RETURN_AUDIT.json").write_bytes(AUDIT_JSON.read_bytes())

        archive_binding, delivery_binding, audit_binding = bind(ZIP), bind(DELIVERY), bind(AUDIT_JSON)
        packet_binding = q0["currentPacket"]
        case_disposition_binding = member_rows["CASE_DISPOSITIONS.json"]
        model = {
            "schemaVersion": 1,
            "moduleId": "rank9summonhosts5-reviewed-202",
            "status": "TWO_EXACT_STATIC_AUTHORED_PROCEDURES_APPLIED_WITH_THREE_BLOCKED",
            "scope": "Only Conjure Magmatic Wyrm and Planar Army are individually accepted and applied to the authored review index. Summon Elemental Avatar remains held under SH202-B01, Summon Herald of the Planes under SH202-B02, and Summon Avatar of Decay under SH202-B03. Native cards, source/access status and class routes are unchanged; runtime and downstream approval gates stay disabled.",
            "acceptedIds": ACCEPTED,
            "unacceptedIds": UNACCEPTED,
            "excludedPendingIds": sorted(live - set(ACCEPTED)),
            "unacceptedHolds": blocker_map,
            "sharedRequirements": {"scope": "No global/shared rule changes; native cards and class routes unchanged.", "runtimeSelectionEnabled": False},
            "spells": spells,
            "caseCoverage": {
                "caseCount": sum(len(value) for value in accepted_case_ids.values()),
                "caseIdsBySpell": accepted_case_ids,
                "caseDispositionsBinding": case_disposition_binding,
                "evidenceBindingsFile": "RETURN_EVIDENCE_BINDINGS.json",
            },
            "returnCounts": delivery["counts"],
            "sourceArchive": archive_binding,
            "deliveryManifest": delivery_binding,
            "independentAudit": audit_binding,
            "submittedSourcePacket": packet_binding,
            "casebookFile": "RETURN_EVIDENCE_BINDINGS.json#/casebookArchiveMember",
            "casebookSourceArchiveMemberBinding": member_rows["CASEBOOK.json"],
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
            "id": "RANK9-SUMMONHOSTS5-PACKAGE-MANIFEST-202",
            "sourceArchive": archive_binding,
            "deliveryManifest": delivery_binding,
            "independentAudit": audit_binding,
            "sourceAnchorCommit": current_authority["sourceCommit"],
            "files": [],
        }
        for file in sorted(path for path in STAGE.rglob("*") if path.is_file()):
            raw = file.read_bytes()
            package_manifest["files"].append({
                "path": (PKG_REL / file.relative_to(STAGE)).as_posix(),
                "bytes": len(raw), "sha256": sha(raw),
            })
        write(STAGE / "CANDIDATE_PACKAGE_MANIFEST.json", package_manifest)
        shutil.move(str(STAGE), str(PKG))
        model_binding = bind(PKG / "MODEL.json")
        package_manifest_binding = bind(PKG / "CANDIDATE_PACKAGE_MANIFEST.json")
        evidence_binding = bind(PKG / "RETURN_EVIDENCE_BINDINGS.json")
        MAN.parent.mkdir(parents=True, exist_ok=True)
        MAN.write_bytes((PKG / "STANDALONE_PROCEDURES.md").read_bytes())
        shutil.copyfile(INDEX, BACKUP)

        write(DEC, {
            "id": director["id"], "returnNumber": 202, "recordedAtUtc": timestamp,
            "decision": "PARTIAL_EXACT_IDENTITY_ACCEPTANCE",
            "acceptedIds": ACCEPTED, "unacceptedIds": UNACCEPTED,
            "blockers": blocker_map, "directorReturn": archive_binding,
            "deliveryManifest": delivery_binding, "independentAudit": audit_binding,
            "authorityAtDecision": baseline, "exactDirectorDecisions": director["perIdentity"],
            "qualifications": director["qualifications"],
            "scope": "Static authorship only; no runtime, implementation, human-play, balance, cosmology, domain closure, completion or release approval.",
            "canonicalFilesChangedByDirector": False,
        })
        acceptance = {
            "id": REVIEW, "recordedAtUtc": timestamp,
            "status": "TWO_EXACT_STATIC_AUTHORED_PROCEDURES_ACCEPTED_WITH_THREE_RETAINED_BLOCKERS",
            "acceptedIds": ACCEPTED, "unacceptedIds": UNACCEPTED,
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
            "id": "RANK9-SUMMONHOSTS5-RETURN202-RECEIPT",
            "recordedAtUtc": timestamp,
            "status": "TWO_ACCEPTED_THREE_BLOCKED_INDEPENDENT_AUDIT_PASSED",
            "reviewedIds": GROUP_IDS, "acceptedIds": ACCEPTED, "unacceptedIds": UNACCEPTED,
            "blockers": blocker_map, "directorReturn": archive_binding,
            "deliveryManifest": delivery_binding, "independentAudit": audit_binding,
            "sourceAuthority": baseline, "counts": delivery["counts"],
            "decisionId": director["id"],
        })
        write(APPFILE, {
            "id": APP, "recordedAtUtc": timestamp,
            "status": "APPLIED_TWO_EXACT_AUTHORED_PROCEDURES_WITH_THREE_RETAINED_BLOCKERS",
            "ownerInstruction": "Apply each exact director-accepted ordinary-spell batch, push it to GitHub, and continue until pending reaches zero.",
            "acceptedIds": ACCEPTED, "unacceptedIds": UNACCEPTED,
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
        for pos, sid in enumerate(ACCEPTED):
            index = next(i for i, entry in enumerate(before["entries"]) if entry["id"] == sid)
            old = before["entries"][index]
            new = copy.deepcopy(old)
            new.update({
                "authoredStatus": "reviewed-authored-operational-playtest",
                "procedureFile": "../spell_candidates/rank9summonhosts5_reviewed_202/MODEL.json",
                "procedurePointer": f"/spells/{pos}/procedure",
                "wholeCardPointer": f"/spells/{pos}",
                "sourceCatalogWholeCardPointer": old.get("sourceCatalogWholeCardPointer") or old["wholeCardPointer"],
                "wholeCardIdField": "id",
                "procedureTextPointer": f"/spells/{pos}/procedure/procedureContent",
                "directorProcedureRecordPointer": f"/spells/{pos}/directorProcedureRecord",
                "sharedRulesPointer": f"/spells/{pos}/procedure/sharedRequirements",
                "manuscript": "../../../docs/spells/candidates/RANK9_SUMMON_HOSTS5_REVIEWED_202.md",
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
            "file": "../spell_candidates/rank9summonhosts5_reviewed_202/MODEL.json",
            "binding": model_binding, "reviewId": REVIEW, "acceptedIds": ACCEPTED,
            "unacceptedIds": UNACCEPTED, "excludedPendingIds": sorted(live - set(ACCEPTED)),
            "authority": bind(ACC), "applicationReceipt": APPFILE.relative_to(ROOT).as_posix(),
            "sourceArchive": archive_binding, "deliveryManifest": delivery_binding,
            "evidenceBindings": evidence_binding, "candidatePackageManifestBinding": package_manifest_binding,
            "scope": acceptance["status"], "runtimeSelectionEnabled": False,
        })
        after["authoredCounts"] = AFTER
        after["representationCounts"]["completeReviewedStandaloneProcedures"] = COMPLETE1
        pending = {entry["id"] for entry in after["entries"]
                   if entry["authoredStatus"] == "pending-authored-procedure"}
        assert pending == live - set(ACCEPTED) and len(pending) == 53
        inverse = copy.deepcopy(after)
        for operation in operations:
            inverse["entries"][operation["index"]] = copy.deepcopy(operation["before"])
        inverse["additionalStandaloneEnvelopes"] = inverse["additionalStandaloneEnvelopes"][:-1]
        inverse["authoredCounts"] = copy.deepcopy(before["authoredCounts"])
        inverse["representationCounts"] = copy.deepcopy(before["representationCounts"])
        assert inverse == before
        after_raw = jb(after)
        temporary = INDEX.with_suffix(".json.summonhosts202.tmp")
        temporary.write_bytes(after_raw)
        temporary.replace(INDEX)
        assert CATALOG.read_bytes() == catalog_raw
        write(OPS, {"id": "RANK9-SUMMONHOSTS5-INDEX-OPERATIONS-202",
                    "before": bind(BACKUP, before_raw), "after": bind(INDEX, after_raw),
                    "operations": operations, "inverseSemanticExact": True,
                    "onlyIdentityIds": ACCEPTED})

        groups = []
        for old_group in q0["currentPendingGroups"]:
            remaining = [sid for sid in old_group["pendingIds"] if sid in pending]
            if not remaining:
                continue
            group = copy.deepcopy(old_group)
            group["pendingIds"] = remaining
            group["pendingCount"] = len(remaining)
            if group["group"] == "rank9-summon-hosts5":
                group.update({
                    "status": "PARTIAL_RETURN202_TWO_ACCEPTED_APPLIED_THREE_BLOCKED",
                    "freshPacketRequiredForCurrentAuthority": True,
                    "blockingReturn": {"ids": UNACCEPTED,
                                       "blockers": {sid: decisions[sid]["blockerIds"] for sid in UNACCEPTED},
                                       "receipt": RCPT.relative_to(ROOT).as_posix()},
                })
            if group["group"] == NEXT:
                group.update({"status": "PENDING_FRESH_PACKET_FOR_CURRENT_AUTHORITY",
                              "freshPacketRequiredForCurrentAuthority": True})
            groups.append(group)
        next_record = next(group for group in groups if group["group"] == NEXT)
        authority = {
            "reviewedApplied": 795, "pending": 53, "acceptedUnapplied": 0,
            "completeStandaloneProcedures": 519, "scopedInterfaces": 173,
        }
        pending_doc = {key: copy.deepcopy(value) for key, value in p0.items()
                       if key.startswith("retainedReturn")}
        pending_doc.update({
            "id": "CURRENT53-PENDING-IDENTITY-AUDIT-202",
            "recordedAtUtc": timestamp,
            "status": "PASSED_EXACT_CURRENT_INDEX_PENDING_SET",
            "indexBinding": bind(INDEX, after_raw), "catalogBinding": bind(CATALOG, catalog_raw),
            "authoredCounts": AFTER, "pendingCount": 53, "pendingIds": sorted(pending),
            "allPendingExistInSourceCatalog": pending <= cats, "acceptedUnapplied": 0,
            "retainedReturn202Blockers": {
                sid: {"blockerIds": decisions[sid]["blockerIds"],
                      "reasons": [record["missingFacts"] for record in blocker_map[sid]["blockerRecords"]]}
                for sid in UNACCEPTED
            },
            "closed335AndCompletedCohortsReopened": False,
            "currentAuthority": authority,
        })
        assert pending_doc["allPendingExistInSourceCatalog"] is True
        write(P1, pending_doc)
        next_request = {
            "group": NEXT, "pendingIds": next_doc["pendingIds"], "pendingCount": len(NEXT_IDS),
            "status": "PENDING_FRESH_PACKET_FOR_CURRENT_AUTHORITY",
            "freshPacketRequiredForCurrentAuthority": True,
            "candidate": next_doc["candidate"], "archive": next_doc["archive"],
        }
        q1 = copy.deepcopy(q0)
        q1.update({
            "id": "SPELL-REVIEW-QUEUE-202", "recordedAtUtc": timestamp,
            "currentAuthority": authority, "pendingCount": 53, "currentPendingGroups": groups,
            "justAppliedBatch": {"reviewId": REVIEW, "ids": ACCEPTED, "count": len(ACCEPTED),
                                 "applicationReceipt": APPFILE.relative_to(ROOT).as_posix(),
                                 "directorAcceptance": ACC.relative_to(ROOT).as_posix(),
                                 "independentAudit": AUDIT_JSON.relative_to(ROOT).as_posix()},
            "pendingIdentityAudit": {"path": P1.relative_to(ROOT).as_posix(), "pending": 53,
                                     "sha256": sha(P1.read_bytes())},
            "nextGroup": NEXT, "next": next_request, "nextPreparedRequest": next_request,
            "packetStatus": "RANK9_SUMMONHOSTS5_RETURN202_TWO_APPLIED_THREE_HELD_795_53_NEXT_RANK9_IMPACT_EXILE4",
            "currentReturnBinding": archive_binding, "currentReturnAudit": audit_binding,
        })
        for key in ("sourceConferencePrepared", "currentPacket", "currentPacketDelivery", "currentPreparation"):
            q1.pop(key, None)
        q1["currentSubmission"] = bind(RCPT)
        q1["currentSubmissionBinding"] = bind(RCPT)
        write(Q1, q1)
        h1 = copy.deepcopy(h0)
        h1.update({
            "id": "CURRENT-HANDOFF-202", "recordedAtUtc": timestamp,
            "status": "RANK9_SUMMONHOSTS5_TWO_APPLIED_THREE_HELD_NEXT_RANK9_IMPACT_EXILE4_53_PENDING",
            "currentAuthority": authority, "currentIndexBinding": bind(INDEX, after_raw),
            "currentCatalogBinding": bind(CATALOG, catalog_raw),
            "pendingIdentityAudit": {"id": pending_doc["id"], "path": P1.relative_to(ROOT).as_posix(),
                                     "pendingCount": 53, "sha256": sha(P1.read_bytes())},
            "appliedThisStep": {"reviewId": REVIEW, "ids": ACCEPTED, "count": len(ACCEPTED),
                                "applicationReceipt": APPFILE.relative_to(ROOT).as_posix(),
                                "directorAcceptance": ACC.relative_to(ROOT).as_posix(),
                                "independentAudit": AUDIT_JSON.relative_to(ROOT).as_posix(),
                                "applicationValidation": {"path": VALID.relative_to(ROOT).as_posix()}},
            "unacceptedThisStep": {"ids": UNACCEPTED,
                                    "blockers": {sid: decisions[sid]["blockerIds"] for sid in UNACCEPTED},
                                    "retainedInPendingSet": True},
            "nextGroup": NEXT, "nextPendingCount": len(NEXT_IDS), "nextPreparedRequest": next_request,
            "currentQueueBinding": bind(Q1), "currentReturnBinding": archive_binding,
            "independentAuditBinding": audit_binding, "parentHandoff": H0.relative_to(ROOT).as_posix(),
            "currentSubmissionBinding": bind(RCPT), "currentReturnAudit": audit_binding,
            "resumePriority": "Prepare a fresh Rank9 Impact/Exile4 packet at 795/53; submit it to the GPT director, independently audit, apply and push only exact accepted IDs, and continue until pending is zero. Retain SH202-B01, SH202-B02 and SH202-B03 unchanged.",
        })
        for key in ("sourceConferencePrepared", "currentPacket", "currentPacketDelivery", "currentPreparation"):
            h1.pop(key, None)
        write(H1, h1)
        shutil.copyfile(MAN, AUDIT / "RANK9_SUMMONHOSTS5_REVIEWED_202.md")
        SNAP.write_text(
            "# Current ordinary spell-review checkpoint 202\n\n"
            f"Return202 passed {read(AUDIT_JSON)['checksPassed']} independent checks, including all 106 archive members and 210 current-source plus 7 supplemental bindings. Applied exactly {', '.join(ACCEPTED)} as static authored procedures. Summon Elemental Avatar remains held under SH202-B01; Summon Herald of the Planes under SH202-B02; Summon Avatar of Decay under SH202-B03. Authority: **795 reviewed / 53 pending / 0 accepted-unapplied**, 519 complete standalone procedures. Next: Rank9 Impact/Exile4. Runtime and downstream approval gates remain disabled.\n",
            encoding="utf-8", newline="\n")
        start = ROOT / "START_HERE.md"
        prior_start = start.read_text(encoding="utf-8-sig") if start.exists() else ""
        start.write_text(
            f"**Current ordinary spell-review handoff [202](docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT_HANDOFF_202.json):** Applied exactly {', '.join(ACCEPTED)}. Authority is **795 reviewed / 53 pending / 0 accepted-unapplied**. Summon Elemental Avatar, Summon Herald of the Planes, and Summon Avatar of Decay remain pending under SH202-B01/B02/B03. Next group: Rank9 Impact/Exile4.\n\n" + prior_start,
            encoding="utf-8", newline="\n")

        validations = [
            ("Return archive and delivery match independent audit bindings",
             sha_file(ZIP) == delivery["archive"]["sha256"]
             and sha_file(DELIVERY) == read(AUDIT_JSON)["deliveryManifest"]["sha256"]),
            ("Exactly two director-accepted IDs were applied and all three held IDs remain pending",
             [op["identity"] for op in operations] == ACCEPTED and set(UNACCEPTED) <= pending),
            ("Authority advanced from 793/55/517 to 795/53/519",
             after["authoredCounts"] == AFTER
             and after["representationCounts"]["completeReviewedStandaloneProcedures"] == COMPLETE1),
            ("Pending identity set is exactly the previous set minus two acceptances",
             pending == live - set(ACCEPTED)),
            ("Index inverse is exact and catalog bytes are unchanged",
             inverse == before and CATALOG.read_bytes() == catalog_raw),
            ("Every candidate package file matches its manifest",
             all((ROOT / item["path"]).is_file()
                 and (ROOT / item["path"]).stat().st_size == item["bytes"]
                 and sha_file(ROOT / item["path"]) == item["sha256"]
                 for item in package_manifest["files"])),
            ("Accepted evidence binds every named case file and the full casebook in the Return202 archive",
             len(accepted_case_bindings) == sum(len(items) for items in accepted_case_ids.values())
             and all(item["archiveMember"] in member_rows for item in accepted_case_bindings.values())
             and evidence["casebookArchiveMember"]["path"] == "CASEBOOK.json"),
            ("Next group exactly matches the director handoff and remains pending",
             q1["nextGroup"] == NEXT and next_record["pendingIds"] == NEXT_IDS
             and next_record["pendingCount"] == len(NEXT_IDS)),
            ("Runtime and downstream approval gates remain disabled",
             all(model[key] is False for key in ("runtimeSelectionEnabled", "runtimeTestsExecuted",
                 "sourceProgramsExecuted", "implementationApproved", "humanPlaytested",
                 "balanceApproved", "cosmologyModified", "releaseApproved", "domainClosure"))),
            ("No closed feat or completed cohort was reopened",
             pending_doc["closed335AndCompletedCohortsReopened"] is False
             and set(ACCEPTED) <= set(p0["pendingIds"])),
        ]
        validation = {
            "id": "RANK9-SUMMONHOSTS5-APPLICATION-VALIDATION-202",
            "recordedAtUtc": timestamp,
            "status": "PASS" if all(item[1] for item in validations) else "FAIL",
            "checksPassed": sum(item[1] for item in validations),
            "checksFailed": sum(not item[1] for item in validations),
            "checks": [{"check": name, "passed": passed} for name, passed in validations],
            "acceptedIds": ACCEPTED, "unacceptedIds": UNACCEPTED,
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
            "acceptedIds": ACCEPTED, "unacceptedIds": UNACCEPTED,
            "authority": authority, "nextGroup": NEXT,
            "pendingAudit": P1.relative_to(ROOT).as_posix(),
            "independentAudit": read(AUDIT_JSON)["status"],
            "candidateManifest": package_manifest_binding,
            "candidateFiles": len(package_manifest["files"]),
        }, indent=2))


if __name__ == "__main__":
    main()
