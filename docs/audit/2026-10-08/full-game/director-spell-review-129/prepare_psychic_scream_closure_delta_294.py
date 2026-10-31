from __future__ import annotations

import datetime as dt
import hashlib
import json
import pathlib
import shutil
import zipfile
import zlib


ROOT = pathlib.Path(__file__).resolve().parents[5]
A = ROOT / "docs/audit/2026-10-08/full-game/director-spell-review-129"
OUT = A / "rank9_psychic_scream_closure_delta_294"
PKG278_DIR = A / "rank9_psychicfear7_current_source_278_prepared_review1"
PKG278 = PKG278_DIR / "DD_Rank9_PsychicFear7_CurrentSource_278.zip"
CANDIDATE278_PATH = PKG278_DIR / "CURRENT_SOURCE_CONFERENCE_CANDIDATE_278.json"
RETURN234 = A / "rank9_psychicfear7_return234_received/DD_Rank9_PsychicFear3_Director_Return234_HELD.zip"
RETURN234_AUDIT = A / "RANK9PSYCHICFEAR7_RETURN234_INDEPENDENT_AUDIT.json"
RETURN234_RECEIPT = A / "RANK9PSYCHICFEAR7_RETURN234_RECEIPT.json"
ID = "psychic-scream"
BLOCKER = "PF182-B01"
PROPOSAL = "PF182-B01-BOUNDED-ANATOMY-LIFECYCLE-CONTRACT-01"
NEXT_GROUP = "rank9-psychic-fear7"
TARGET_CASE_PREFIX = "RANK9PSYCHICFEAR7-180-PSYCHIC-SCREAM-"
CURRENT_AUTHORITY_FILES = {
    "index": "DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json",
    "catalog": "DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json",
    "accessRegistry": "DescentReviewChanges/ReviewBible/data/director/spell_review/accepted_interface_registry_06.json",
    "queue": "docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT_SPELL_QUEUE_293.json",
    "handoff": "docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT_HANDOFF_293.json",
    "pendingAudit": "docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT29_PENDING_IDENTITY_AUDIT_293.json",
    "puppetmastersAcceptance": "docs/audit/2026-10-08/full-game/director-spell-review-129/PUPPETMASTERS_REALM_ACCEPTANCE_293.json",
    "puppetmastersApplication": "docs/audit/2026-10-08/full-game/director-spell-review-129/PUPPETMASTERS_REALM_APPLICATION_293.json",
    "puppetmastersValidation": "docs/audit/2026-10-08/full-game/director-spell-review-129/PUPPETMASTERS_REALM_APPLICATION_VALIDATION_293.json",
}


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def bind(path: pathlib.Path, raw: bytes | None = None):
    data = path.read_bytes() if raw is None else raw
    return {
        "path": path.relative_to(ROOT).as_posix(),
        "bytes": len(data),
        "sha256": sha(data),
        "crc32": f"{zlib.crc32(data) & 0xFFFFFFFF:08x}",
    }


def read_json(raw: bytes):
    return json.loads(raw.decode("utf-8-sig"))


def write_json(path: pathlib.Path, value) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")


def copy_exact(source: pathlib.Path, destination: pathlib.Path) -> dict:
    raw = source.read_bytes()
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_bytes(raw)
    return {"source": bind(source, raw), "packetPath": destination.relative_to(OUT).as_posix(), "packetBytes": len(raw), "packetSha256": sha(destination.read_bytes())}


def main():
    assert not OUT.exists(), "Refusing to overwrite a previously prepared closure packet."
    OUT.mkdir(parents=True)
    stamp = dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")
    candidate278 = json.loads(CANDIDATE278_PATH.read_text(encoding="utf-8-sig"))
    current_head = __import__("subprocess").check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    branch = __import__("subprocess").check_output(["git", "branch", "--show-current"], cwd=ROOT, text=True).strip()
    assert branch == "main"
    authority = {
        "reviewedApplied": 819,
        "pending": 29,
        "acceptedUnapplied": 0,
        "completeStandaloneProcedures": 543,
        "scopedInterfaces": 173,
    }

    pkg_zip_raw = PKG278.read_bytes()
    return_raw = RETURN234.read_bytes()
    pkg_zip_ref = bind(PKG278, pkg_zip_raw)
    return_ref = bind(RETURN234, return_raw)
    pkg_members = {}
    with zipfile.ZipFile(PKG278) as old_archive:
        assert old_archive.testzip() is None
        for member in old_archive.namelist():
            pkg_members[member] = old_archive.read(member)
    source_refresh = []
    changed = []
    unchanged = []
    for old in candidate278["sourceBindings"]:
        path = ROOT / old["path"]
        current_raw = path.read_bytes()
        archive_member = "sources_current/" + old["path"]
        assert archive_member in pkg_members
        archived_raw = pkg_members[archive_member]
        assert len(archived_raw) == old["bytes"] and sha(archived_raw) == old["sha256"]
        same = len(current_raw) == old["bytes"] and sha(current_raw) == old["sha256"]
        row = {
            "path": old["path"],
            "packet278OldCurrentBinding": {"bytes": old["bytes"], "sha256": old["sha256"], "crc32": old.get("crc32")},
            "packet278Archive": {"path": pkg_zip_ref["path"], "sha256": pkg_zip_ref["sha256"], "member": archive_member, "memberBytes": len(archived_raw), "memberSha256": sha(archived_raw)},
            "currentWorkingTreeBinding": {"bytes": len(current_raw), "sha256": sha(current_raw), "crc32": f"{zlib.crc32(current_raw) & 0xFFFFFFFF:08x}"},
            "unchangedSincePacket278": same,
        }
        if same:
            unchanged.append(row)
        else:
            changed.append(row)
            packet_copy = OUT / "source_refresh_changes" / "current_authored_review_index.json"
            packet_copy.parent.mkdir(parents=True, exist_ok=True)
            packet_copy.write_bytes(current_raw)
            row["currentCopyInPacket"] = packet_copy.relative_to(OUT).as_posix()
        source_refresh.append(row)
    assert len(source_refresh) == 84 and len(unchanged) == 83 and len(changed) == 1
    assert changed[0]["path"] == CURRENT_AUTHORITY_FILES["index"]

    current_refs = {}
    copied_authority = []
    for label, rel in CURRENT_AUTHORITY_FILES.items():
        source = ROOT / rel
        dest = OUT / "current_authority" / (label + "__" + pathlib.Path(rel).name)
        copied = copy_exact(source, dest)
        current_refs[label] = copied["source"]
        copied_authority.append(copied)
    for label, ref in current_refs.items():
        if label == "catalog":
            assert ref["sha256"] == "773fb0b3b0fdb501858ded33c02d90dc4db3009bd1b9f7112c244d998218f05b"
    current_index = current_refs["index"]
    assert current_index["sha256"] == "62cd01c9482c3d563598b5978aa4ac86b426e10149c8a004e9aac970b6c5e189"
    queue = json.loads((ROOT / CURRENT_AUTHORITY_FILES["queue"]).read_text(encoding="utf-8-sig"))
    handoff = json.loads((ROOT / CURRENT_AUTHORITY_FILES["handoff"]).read_text(encoding="utf-8-sig"))
    pending = json.loads((ROOT / CURRENT_AUTHORITY_FILES["pendingAudit"]).read_text(encoding="utf-8-sig"))
    assert queue["currentAuthority"] == handoff["currentAuthority"] == pending["authority"] == authority
    assert pending["pendingCount"] == 29 and ID in pending["pendingIds"]
    assert queue["next"]["pendingIds"][0] == ID

    # Return234 contains the exact 16 Psychic Scream target cases and its proposed procedure.
    out_cases = OUT / "preserved_psychic_scream" / "cases"
    out_proc = OUT / "preserved_psychic_scream" / "procedure"
    out_cases.mkdir(parents=True, exist_ok=True)
    case_bindings = []
    total_events = 0
    total_forward = 0
    total_inverse = 0
    held_case_ids = {
        TARGET_CASE_PREFIX + "B/positive-final-death-head-consequence",
        TARGET_CASE_PREFIX + "B/headless-multihead-current-form",
    }
    with zipfile.ZipFile(RETURN234) as old_return:
        assert old_return.testzip() is None
        case_members = sorted(name for name in old_return.namelist() if name.startswith("cases/") and "PSYCHIC-SCREAM" in name)
        assert len(case_members) == 16
        proc_member = "procedures/psychic-scream.json"
        procedure_raw = old_return.read(proc_member)
        procedure = read_json(procedure_raw)
        assert procedure["id"] == "PF182-PROCEDURE-psychic-scream"
        out_proc.mkdir(parents=True, exist_ok=True)
        proc_path = out_proc / "psychic-scream.json"
        proc_path.write_bytes(procedure_raw)
        procedure_binding = {"archive": return_ref, "member": proc_member, "bytes": len(procedure_raw), "sha256": sha(procedure_raw), "packetCopy": proc_path.relative_to(OUT).as_posix()}
        for case_number, member in enumerate(case_members, start=1):
            raw = old_return.read(member)
            case = read_json(raw)
            assert case["spellId"] == ID and case["id"].startswith(TARGET_CASE_PREFIX)
            # Keep the output path below Windows MAX_PATH; the exact source
            # member name remains bound in case_bindings below.
            path = out_cases / f"{case_number:02d}.json"
            path.write_bytes(raw)
            event_count = len(case.get("events", []))
            forward = sum(len(event.get("forward", [])) for event in case.get("events", []))
            inverse = sum(len(event.get("inverse", [])) for event in case.get("events", []))
            total_events += event_count
            total_forward += forward
            total_inverse += inverse
            case_bindings.append(
                {
                    "id": case["id"],
                    "status": case.get("status"),
                    "heldRequiredPositiveBranch": case["id"] in held_case_ids,
                    "archive": return_ref,
                    "member": member,
                    "bytes": len(raw),
                    "sha256": sha(raw),
                    "events": event_count,
                    "forwardOperations": forward,
                    "inverseOperations": inverse,
                    "packetCopy": path.relative_to(OUT).as_posix(),
                }
            )
    assert total_events == 227 and len(case_bindings) == 16
    assert sum(1 for row in case_bindings if row["heldRequiredPositiveBranch"]) == 2

    # Preserve only target-relevant saved questions, addenda, obligations, dispositions and the exact blocker.
    relevant = {
        "originalQuestions": [row for row in candidate278["originalQuestionsUnchanged"] if ID in row.get("spellIds", [])],
        "focusedAddenda": [row for row in candidate278["focusedAdditionalQuestionsUnchanged"] if ID in row.get("spellIds", [])],
        "selectedQuestionDispositions": [
            row for row in candidate278["priorSelectedQuestionDispositions"]
            if ID in row.get("spellIds", []) or any(ID in case_id for case_id in row.get("caseIds", []))
        ],
        "mainCaseObligations": [row for row in candidate278["priorTargetMainCaseObligations"] if row.get("spellId") == ID],
        "futureRequirements": candidate278["priorTargetFutureRequirements"],
        "blocker": next(row for row in candidate278["priorBlockersForFreshReassessment"] if row["id"] == BLOCKER),
        "return234Decision": next(row for row in json.loads(return_raw.decode("utf-8", "ignore")) if False) if False else None,
    }
    # Bind the independent prior disposition/decision files rather than treating old counts as current authority.
    return234_decision_member = "DIRECTOR_DECISION.json"
    with zipfile.ZipFile(RETURN234) as old_return:
        return_decision = read_json(old_return.read(return234_decision_member))
        return_psychic_decision = next(row for row in return_decision["perIdentityDecisions"] if row["id"] == ID)
        return_procedure_status = read_json(old_return.read("PROCEDURE_STATUS_234.json"))
        procedure_status_rows = return_procedure_status if isinstance(return_procedure_status, list) else return_procedure_status.get("perIdentity", return_procedure_status.get("identities", []))
        psychic_status = next((row for row in procedure_status_rows if row.get("id") == ID or row.get("spellId") == ID), None)
    relevant["return234Decision"] = return_psychic_decision
    relevant["return234HistoricalAuthority"] = return_decision["authority"]
    relevant["procedureStatus234"] = psychic_status
    relevant["preservedBlockerQualifications"] = sorted(
        set(return_psychic_decision.get("conditionalBoundaryIds", []))
        | {"PF181-H03", BLOCKER}
    )
    write_json(OUT / "PRESERVED_PSYCHIC_SCREAM_DISPOSITIONS_294.json", relevant)
    current_candidate_copy = OUT / "historical" / "CURRENT_SOURCE_CONFERENCE_CANDIDATE_278.json"
    current_candidate_copy.parent.mkdir(parents=True, exist_ok=True)
    current_candidate_copy.write_bytes(CANDIDATE278_PATH.read_bytes())

    source_search_path = ROOT / "DescentReviewChanges/ReviewBible/src/bestiary_data_full.json"
    bestiary = json.loads(source_search_path.read_text(encoding="utf-8-sig"))
    hydra = next(row for row in bestiary if row.get("name") == "Hydra")
    search = {
        "id": "PSYCHIC-SCREAM-CURRENT-ANATOMY-SOURCE-SEARCH-294",
        "recordedAtUtc": stamp,
        "scope": ["current DescentReviewChanges/ReviewBible/src/bestiary_data_full.json", "current spell catalog and bound current source conference 278"],
        "bestiaryBinding": bind(source_search_path),
        "HydraEntry": hydra,
        "finding": "The current Hydra record has one Crushing Maw action and no head count, destructibility, vital-head relationship, form reversion, or remains anatomy. It cannot supply the missing positive source witness.",
        "limits": "This is a bounded source search, not a universal absence claim. No creature anatomy is invented or inferred.",
    }
    write_json(OUT / "CURRENT_ANATOMY_SOURCE_SEARCH_294.json", search)

    # Proposed fields are deliberately separated from all existing source facts.
    proposal = {
        "id": PROPOSAL,
        "status": "PROPOSED_FOR_DIRECTOR_ADJUDICATION_NOT_ACCEPTED_NOT_SOURCE_EVIDENCE",
        "scope": "Psychic Scream / Wizard Enchantment authored procedure only. The Mage Evocation stun route and the historical Illusion placement are unchanged.",
        "existingSourceFacts": "None of the new anatomy values below are represented as existing creature facts. The current Hydra record is insufficient.",
        "proposedAuthoredFields": [
            {"field": "bodyInstanceId", "meaning": "Stable identity of the one actual body throughout the case.", "kind": "NEW authored case field"},
            {"field": "formTimeline[]", "meaning": "Ordered formId/formEpoch transitions with eventId, exact effective stage, and explicit death-time behavior.", "kind": "NEW authored case field"},
            {"field": "formTimeline[].headCount", "meaning": "Exact integer head count for that body/form epoch; zero is an explicit headless body, null/unknown blocks the positive rider.", "kind": "NEW authored case field"},
            {"field": "formTimeline[].heads[]", "meaning": "Unique head IDs enumerated for the current form, with explicit destructible, vitalRelationship, bodyAttachment, and remainsPartId values.", "kind": "NEW authored case field"},
            {"field": "formTimeline[].sourceOrFixtureBinding", "meaning": "Each anatomy value is tagged source-defined with exact path/hash/pointer, or authored synthetic fixture only; the two evidence classes may not be conflated.", "kind": "NEW provenance field"},
            {"field": "resolution.deathFormSnapshot", "meaning": "At the instant final death is established after damage, defenses, Null, survival and form rules, freeze bodyInstanceId, current form epoch, and enumerated head IDs.", "kind": "NEW authored ordering field"},
            {"field": "resolution.headConsequence[]", "meaning": "Only after final death, enumerate the snapshot's explicitly destructible heads and mark their remains part destroyed; this produces no extra damage, save, death event, severance while alive, or revival bypass.", "kind": "NEW authored ordering field"},
            {"field": "resolution.postDeathFormSettlement", "meaning": "Apply only a separately supplied form/death/reversion rule after the death-form snapshot and head consequence. Missing ordering or destination remains unresolved and blocks the positive branch.", "kind": "NEW authored ordering field"},
            {"field": "remainsAndCustody", "meaning": "Record location, support, each intact/destroyed body part, and every equipment owner/custodian; explosion changes only enumerated head parts and never silently transfers or deletes equipment.", "kind": "NEW authored case field"},
        ],
        "proposedRules": [
            "Resolve the committed Wizard Enchantment cast and all 14d6 inputs through actual damage defenses, temporary HP, Wounds, Null, survival and final death first.",
            "If and only if that event establishes final death, snapshot the actual current body/form and explicitly enumerated heads at that exact terminal stage; apply the native possible-head-consequence only to snapshot heads whose supplied field explicitly says destructible=true.",
            "An explicit headCount=0 yields no head consequence. More than one head is processed by its unique IDs, not by an inferred template. Unknown count, destructibility, vitality, form order, or remains mapping holds the positive branch.",
            "The selected contract does not define a monster, change the Bestiary, infer anatomy from type/name/geometry, add a third Illusion access route, or affect Mage Evocation stun.",
            "All proposal-only numeric fixture values remain synthetic and conditional. They demonstrate the proposed data contract, not an acquired campaign actor or source fact.",
        ],
        "proposedSyntheticFixtureOnly": {
            "positiveFinalDeath": {"bodyInstanceId": "SYNTHETIC-BODY-01", "formId": "SYNTHETIC-FORM-ONE-HEAD", "headCount": 1, "heads": [{"id": "H1", "destructible": True, "vitalRelationship": "vital", "bodyAttachment": "attached", "remainsPartId": "PART-H1"}], "sourceOrFixtureBinding": "authored fixture only; not an existing creature source", "damageInputs": [6] * 14, "damageTotal": 84, "initialHP": 70, "temporaryHP": 0, "nullOrSurvivalPrevention": False, "afterDamage": "final death", "afterDeathHeadState": {"H1": "destroyed"}, "equipmentOwnerAndCustodianUnchanged": True},
            "headlessFinalDeath": {"bodyInstanceId": "SYNTHETIC-BODY-02", "formId": "SYNTHETIC-FORM-HEADLESS", "headCount": 0, "heads": [], "sourceOrFixtureBinding": "authored fixture only; not an existing creature source", "expectedHeadConsequence": "none"},
            "multiheadFinalDeath": {"bodyInstanceId": "SYNTHETIC-BODY-03", "formId": "SYNTHETIC-FORM-THREE-HEADS", "headCount": 3, "heads": [{"id": "H1", "destructible": True, "vitalRelationship": "vital", "bodyAttachment": "attached", "remainsPartId": "PART-H1"}, {"id": "H2", "destructible": True, "vitalRelationship": "nonvital", "bodyAttachment": "attached", "remainsPartId": "PART-H2"}, {"id": "H3", "destructible": False, "vitalRelationship": "nonvital", "bodyAttachment": "attached", "remainsPartId": "PART-H3"}], "sourceOrFixtureBinding": "authored fixture only; not an existing creature source", "expectedHeadConsequence": {"H1": "destroyed", "H2": "destroyed", "H3": "intact"}},
            "changedFormFinalDeath": {"bodyInstanceId": "SYNTHETIC-BODY-04", "formTimeline": [{"formId": "SYNTHETIC-FORM-A", "formEpoch": 1, "headCount": 1, "heads": [{"id": "A-H1", "destructible": True}]}, {"formId": "SYNTHETIC-FORM-B", "formEpoch": 2, "headCount": 2, "heads": [{"id": "B-H1", "destructible": True}, {"id": "B-H2", "destructible": True}]}], "deathFormSnapshot": "SYNTHETIC-FORM-B/formEpoch-2", "postDeathFormSettlement": "explicit fixture rule after the death-form consequence", "sourceOrFixtureBinding": "authored fixture only; not an existing creature source"},
        },
        "retainedSourceQualification": "Actual campaign use remains source-qualified: a real target's current body/form anatomy and lifecycle must be supplied; synthetic fixtures do not satisfy this requirement.",
    }
    write_json(OUT / "ANATOMY_LIFECYCLE_PROPOSAL_294.json", proposal)

    request = {
        "schema": "DD-PF182-B01-closure-review-request-v1",
        "createdAtUtc": stamp,
        "identity": ID,
        "blocker": BLOCKER,
        "authority": authority,
        "authorityBindings": current_refs,
        "currentBaseCommit": current_head,
        "currentBranch": branch,
        "workingTreeSnapshot": "Uncommitted snapshot; commit HEAD is recorded separately and contains none of the current review applications.",
        "currentSnapshotIncludes": ["Puppetmaster's Realm accepted/authored index application 293", "Mind Collapse application 290", "Absolute Domination application 292"],
        "historicalMaterials": {
            "packet278Archive": pkg_zip_ref,
            "candidate278": bind(CANDIDATE278_PATH),
            "return234Archive": return_ref,
            "return234IndependentAudit": bind(RETURN234_AUDIT),
            "return234Receipt": bind(RETURN234_RECEIPT),
        },
        "sourceRefresh": {"sourceBindingCount": len(source_refresh), "unchangedCount": len(unchanged), "changedCount": len(changed), "changedPaths": [row["path"] for row in changed], "mapFile": "SOURCE_REFRESH_MAP_294.json"},
        "preservedTargetEvidence": {"procedure": procedure_binding, "caseCount": len(case_bindings), "eventCount": total_events, "heldRequiredPositiveBranches": sorted(held_case_ids), "caseBindingsFile": "PSYCHIC_SCREAM_CASE_BINDINGS_294.json", "dispositionsFile": "PRESERVED_PSYCHIC_SCREAM_DISPOSITIONS_294.json"},
        "proposedRevision": {"id": PROPOSAL, "status": proposal["status"], "scope": proposal["scope"], "proposalFile": "ANATOMY_LIFECYCLE_PROPOSAL_294.json"},
        "decisionRequested": "Adjudicate Psychic Scream / PF182-B01 only. Either ACCEPT this bounded NEW anatomy/lifecycle data contract and synthetic conditional fixtures for authored-procedure review while retaining PF181-H03/source-qualified actual-target requirements; or HOLD with exact missing authored fields or source facts. Confirm whether the two held anatomy records can be replaced by these explicitly authored conditional fixtures for procedure acceptance, while preserving the independent Mage Evocation stun route, all three placements, and no Illusion access route. No claim that synthetic anatomy is existing creature evidence. Confirm next order/count at 819 applied / 29 pending / 0 accepted-unapplied.",
        "notAcceptedOrApplied": True,
        "noCanonicalChangeProposed": True,
        "otherIdentitiesSubmitted": [],
    }
    write_json(OUT / "CLOSURE_REVIEW_REQUEST_294.json", request)
    write_json(OUT / "PSYCHIC_SCREAM_CASE_BINDINGS_294.json", {"return234Archive": return_ref, "procedure": procedure_binding, "cases": case_bindings, "caseCount": 16, "eventCount": total_events, "forwardOperations": total_forward, "inverseOperations": total_inverse, "heldRequiredPositiveBranches": sorted(held_case_ids)})
    write_json(OUT / "SOURCE_REFRESH_MAP_294.json", {"id": "PSYCHICFEAR7-SOURCE-REFRESH-MAP-294", "recordedAtUtc": stamp, "packet278Archive": pkg_zip_ref, "candidate278": bind(CANDIDATE278_PATH), "sourceBindingCount": len(source_refresh), "unchangedCount": len(unchanged), "changedCount": len(changed), "sourceBindings": source_refresh})
    write_json(OUT / "CURRENT_AUTHORITY_294.json", {"id": "PSYCHIC-SCREAM-CURRENT-AUTHORITY-294", "recordedAtUtc": stamp, "authority": authority, "currentBindings": current_refs, "indexSourceRefreshFromPacket278": changed[0], "currentPendingGroup": {"group": NEXT_GROUP, "identity": ID, "blocker": BLOCKER}, "packetSnapshot": "Current uncommitted working-tree snapshot distinct from base commit " + current_head})

    checks = [
        ("Current authority is 819 applied / 29 pending / 0 accepted-unapplied", authority == {"reviewedApplied": 819, "pending": 29, "acceptedUnapplied": 0, "completeStandaloneProcedures": 543, "scopedInterfaces": 173}),
        ("Current index/catalog/interface/queue/handoff/pending audit are bound", len(current_refs) == 9 and pending["authority"] == authority and queue["currentAuthority"] == authority and handoff["currentAuthority"] == authority),
        ("Packet278 source refresh covers all 84 bindings", len(source_refresh) == 84),
        ("Exactly 83 Packet278 bindings are unchanged and 1 current index binding changed", len(unchanged) == 83 and len(changed) == 1 and changed[0]["path"] == CURRENT_AUTHORITY_FILES["index"]),
        ("Packet278 exact member bytes and hashes match every historical binding", all(row["packet278Archive"]["memberSha256"] == row["packet278OldCurrentBinding"]["sha256"] for row in source_refresh)),
        ("Return234 target subset is exactly 16 Psychic Scream cases and 227 events", len(case_bindings) == 16 and total_events == 227),
        ("Both incomplete anatomy records remain explicitly held", all(row["heldRequiredPositiveBranch"] for row in case_bindings if row["id"] in held_case_ids) and sum(row["heldRequiredPositiveBranch"] for row in case_bindings) == 2),
        ("Psychic Scream source record retains three placements and two access routes", len(procedure["nativeBookBindingsUnchanged"]) == 3 and set(procedure["nativeCardAndAccessUnchanged"]["classAccess"]) == {"Mage", "Wizard"}),
        ("Anatomy contract is explicitly proposed and synthetic fixtures are not source facts", proposal["status"].startswith("PROPOSED") and "not an existing creature source" in proposal["proposedSyntheticFixtureOnly"]["positiveFinalDeath"]["sourceOrFixtureBinding"]),
        ("No canonical edits or application are proposed", request["notAcceptedOrApplied"] and request["noCanonicalChangeProposed"] and request["otherIdentitiesSubmitted"] == []),
    ]
    audit = {"id": "PSYCHIC-SCREAM-CLOSURE-DELTA-INDEPENDENT-AUDIT-294", "recordedAtUtc": stamp, "status": "PASS" if all(ok for _, ok in checks) else "FAIL", "checks": [{"check": name, "passed": bool(ok)} for name, ok in checks], "checkCount": len(checks), "passedChecks": sum(bool(ok) for _, ok in checks), "failedChecks": [name for name, ok in checks if not ok], "authority": authority, "cases": {"count": len(case_bindings), "events": total_events, "forwardOperations": total_forward, "inverseOperations": total_inverse}, "sourceRefresh": {"count": len(source_refresh), "unchanged": len(unchanged), "changed": len(changed)}}
    write_json(OUT / "INDEPENDENT_AUDIT_294.json", audit)
    assert audit["status"] == "PASS"

    manifest = {"id": "PSYCHIC-SCREAM-CLOSURE-DELTA-MANIFEST-294", "recordedAtUtc": stamp, "authority": authority, "currentBaseCommit": current_head, "currentBranch": branch, "status": "PREPARED_INDEPENDENTLY_AUDITED_UNSENT_NO_ACCEPTANCE_OR_APPLICATION", "zip": {"path": "DD_Rank9_PsychicScream_ClosureDelta_294.zip"}, "files": []}
    manifest_path = OUT / "DELIVERY_MANIFEST_294.json"
    write_json(manifest_path, manifest)
    archive_path = OUT / "DD_Rank9_PsychicScream_ClosureDelta_294.zip"
    with zipfile.ZipFile(archive_path, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=6) as archive:
        for path in sorted(OUT.rglob("*")):
            if path.is_file() and path not in {archive_path, manifest_path}:
                rel = path.relative_to(OUT).as_posix()
                raw = path.read_bytes()
                manifest["files"].append({"path": rel, "bytes": len(raw), "sha256": sha(raw), "crc32": f"{zlib.crc32(raw) & 0xFFFFFFFF:08x}"})
                archive.write(path, rel)
    write_json(manifest_path, manifest)
    # Rebuild archive after adding the final self-excluding manifest and checksummed file list.
    with zipfile.ZipFile(archive_path, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=6) as archive:
        for path in sorted(OUT.rglob("*")):
            if path.is_file() and path != archive_path:
                archive.write(path, path.relative_to(OUT).as_posix())
    with zipfile.ZipFile(archive_path) as archive:
        assert archive.testzip() is None
        names = archive.namelist()
        assert len(names) == len(set(names)) and "DELIVERY_MANIFEST_294.json" in names
    archive_raw = archive_path.read_bytes()
    print(json.dumps({"status": "PASS", "authority": authority, "sourceRefresh": {"count": len(source_refresh), "unchanged": len(unchanged), "changed": len(changed)}, "targetCases": {"count": len(case_bindings), "events": total_events, "forward": total_forward, "inverse": total_inverse}, "audit": bind(OUT / "INDEPENDENT_AUDIT_294.json"), "manifest": bind(manifest_path), "zip": {"path": archive_path.relative_to(ROOT).as_posix(), "bytes": len(archive_raw), "sha256": sha(archive_raw), "crc32": f"{zlib.crc32(archive_raw) & 0xFFFFFFFF:08x}"}, "proposal": PROPOSAL, "next": queue["next"]["pendingIds"]}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
