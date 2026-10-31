from __future__ import annotations

import copy
import datetime as dt
import hashlib
import json
import pathlib
import zlib
import zipfile


ROOT = pathlib.Path(__file__).resolve().parents[5]
A = ROOT / "docs/audit/2026-10-08/full-game/director-spell-review-129"
PACKET = A / "rank9_ag190_b02_closure_review_293"
PKG_REL = pathlib.Path(
    "DescentReviewChanges/ReviewBible/data/public/spell_candidates/"
    "rank9agencycontrol9_puppetmastersrealm_reviewed_293"
)
PKG = ROOT / PKG_REL
MANUSCRIPT = ROOT / "DescentReviewChanges/ReviewBible/docs/spells/candidates/PUPPETMASTERS_REALM_REVIEWED_293.md"
INDEX = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json"
CATALOG = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json"
BASE = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_candidates/rank9agencycontrol9_reviewed_190_reconciled01"
ID = "puppetmaster-s-realm"
NAME = "Puppetmaster's Realm"
BLOCKER = "AG190-B02"
ROUTE = "AG190-B02-ALTERNATE-REVIEW-ROUTE-01"
NEXT = "psychic-scream"
NEXT_BLOCKER = "PF182-B01"
NEXT_GROUP = "rank9-psychic-fear7"
URL = "https://chatgpt.com/g/g-p-67f17555a8dc8191a2b5b81e6d8adc12-dungeon-crawler/c/6adc506d-8770-83ea-b64c-0345d9b9b682"
BEFORE = {
    "reviewedApplied": 818,
    "pending": 30,
    "acceptedUnapplied": 0,
    "completeStandaloneProcedures": 542,
    "scopedInterfaces": 173,
}
AFTER = {
    "reviewedApplied": 819,
    "pending": 29,
    "acceptedUnapplied": 0,
    "completeStandaloneProcedures": 543,
    "scopedInterfaces": 173,
}
DIRECTOR_TEXT = (
    "ACCEPT puppetmaster-s-realm — accepted=true, applied=false. "
    "I authorize AG190-B02-ALTERNATE-REVIEW-ROUTE-01, limited to this spell’s authored-procedure review. "
    "The acquired Ghoul Lash two-Bone-Shot trace satisfies the independent attack-member routing obligation. "
    "AG190-B02 closes as a whole-identity acceptance blocker. "
    "AG190-H-SOURCE and H150-ROSTER remain retained. Ghoul Lash is not native NPC Multiattack. "
    "That conditional branch still requires a complete lawful creature profile, authorized attack members, "
    "numeric reach/range, and acquisition/control history. Cave Bear’s missing reach and narrative-only Bite "
    "are not filled by this decision. All other AG190 qualifications and downstream gates remain unchanged. "
    "Independent checks passed: ZIP CRCs, exact 11-member allowlist and all 10 payload size/hash bindings. "
    "Seven preserved records remain byte-identical to Return238. 157 events, 314 forward operations and "
    "314 inverse operations, including state hashes, continuity and full reverse traversal. The native-Multiattack "
    "hold record remains documentary, not a positive encounter. Counts: 818 applied; this decision adds "
    "1 accepted-unapplied, leaving 29 other held identities. The canonical index remains at 30 pending until "
    "application. After your independently verified application: 819 applied / 29 pending / 0 accepted-unapplied; "
    "543 procedures / 173 interfaces. Next: psychic-scream / PF182-B01, followed by mass-phantom-killer and "
    "weird / PF182-B02. The remaining queue order is unchanged. No other identity is accepted or applied."
)
QUALS = [
    "Acceptance is limited to Puppetmaster's Realm authored-procedure review under AG190-B02-ALTERNATE-REVIEW-ROUTE-01.",
    "The Ghoul Lash two-Bone-Shot trace is an acquired class-feature attack-member routing witness only; it is not native NPC Multiattack.",
    "AG190-H-SOURCE and H150-ROSTER remain retained. Any actual NPC native-Multiattack branch still requires a complete lawful creature profile, authorized attack members, numeric reach/range, and acquisition/control history.",
    "Cave Bear's missing Claws reach and narrative-only Bite are not inferred or supplied by this review route.",
    "All other AG190 qualifications remain retained; native catalog is byte-exact, runtime selection is disabled, and implementation, human-play, balance, cosmology, domain-closure, and release gates remain closed.",
]


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def read(path: pathlib.Path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def encode(value) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8")


def write(path: pathlib.Path, value) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(encode(value))


def bind(path: pathlib.Path, raw: bytes | None = None):
    data = path.read_bytes() if raw is None else raw
    return {
        "path": path.relative_to(ROOT).as_posix(),
        "bytes": len(data),
        "sha256": sha(data),
        "crc32": f"{zlib.crc32(data) & 0xFFFFFFFF:08x}",
    }


def clean_rows(rows):
    cleaned = []
    for original in rows:
        row = copy.deepcopy(original)
        key = next((k for k in ("pendingIds", "identities", "spellIds") if isinstance(row.get(k), list)), None)
        if key:
            row[key] = [item for item in row[key] if item != ID]
            if not row[key]:
                continue
            if "pendingCount" in row:
                row["pendingCount"] = len(row[key])
        cleaned.append(row)
    return cleaned


def clean_order(rows):
    result = []
    for old in rows:
        row = copy.deepcopy(old)
        key = next((k for k in ("identities", "pendingIds", "spellIds") if isinstance(row.get(k), list)), None)
        if key:
            row[key] = [item for item in row[key] if item != ID]
            if not row[key]:
                continue
        row["priority"] = len(result) + 1
        result.append(row)
    return result


def main():
    assert not PKG.exists() and not MANUSCRIPT.exists(), "Refusing to overwrite application outputs."
    stamp = dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")
    audit_path = PACKET / "AG190_B02_CLOSURE_REVIEW_INDEPENDENT_AUDIT_293.json"
    request_path = PACKET / "AG190_B02_CLOSURE_REVIEW_REQUEST_293.json"
    source_search_path = PACKET / "AG190_B02_NATIVE_MULTIATTACK_SOURCE_SEARCH_293.json"
    zip_path = PACKET / "DD_Rank9_AgencyControl9_PuppetmastersRealm_ClosureReview_293.zip"
    manifest_path = PACKET / "DELIVERY_MANIFEST_293.json"
    audit = read(audit_path)
    request = read(request_path)
    delivery = read(manifest_path)
    archive_raw = zip_path.read_bytes()
    assert sha(archive_raw) == "ae5dbd25fb55a471ebceedd327bcf22bf754c73006b720c41623e52edb40481e"
    assert audit["status"] == "PASS" and audit["passedChecks"] == 15 and not audit["failedChecks"]
    assert request["identity"] == ID and request["blocker"] == BLOCKER
    assert request["proposedSpellSpecificReviewRoute"]["revisionIdRequested"] == ROUTE
    assert delivery["notAcceptedOrApplied"] is True
    with zipfile.ZipFile(zip_path) as archive:
        names = archive.namelist()
        assert len(names) == 11 and len(set(names)) == 11 and archive.testzip() is None
        expected_names = {
            "AG190_B02_NATIVE_MULTIATTACK_SOURCE_SEARCH_293.json",
            "AG190_B02_CLOSURE_REVIEW_REQUEST_293.json",
            "AG190_B02_CLOSURE_REVIEW_INDEPENDENT_AUDIT_293.json",
            "DELIVERY_MANIFEST_293.json",
            *(pathlib.Path(item["path"]).name for item in delivery["preservedCases"]),
        }
        assert set(names) == expected_names
        for member in names:
            assert archive.read(member)

    preserved = []
    total_events = total_forward = total_inverse = 0
    for item in delivery["preservedCases"]:
        path = ROOT / item["path"]
        raw = path.read_bytes()
        assert len(raw) == item["bytes"] and sha(raw) == item["sha256"]
        case = read(path)
        events = case.get("events", [])
        total_events += len(events)
        total_forward += sum(len(event.get("forward", [])) for event in events)
        total_inverse += sum(len(event.get("inverse", [])) for event in events)
        preserved.append(bind(path, raw))
    assert len(preserved) == 7
    assert (total_events, total_forward, total_inverse) == (157, 314, 314)

    source_path = BASE / "procedures/puppetmaster-s-realm.json"
    source_raw = source_path.read_bytes()
    source = read(source_path)
    procedure = copy.deepcopy(source["procedure"])
    assert source["id"] == ID and BLOCKER in source["holdIds"]
    assert "AG190-H-SOURCE" in source["holdIds"]
    procedure["attacks"] += (
        " Under the Director-authorized " + ROUTE + ", the acquired Ghoul Lash two-Bone-Shot trace is the positive "
        "attack-member routing witness for this authored procedure only. It is not native NPC Multiattack."
    )
    procedure["conflicts"] += (
        " The native NPC Multiattack positive branch remains held under AG190-H-SOURCE and H150-ROSTER until a "
        "complete lawful creature profile, authorized attack members, numeric reach/range, and acquisition/control "
        "history are available. Do not infer Cave Bear Claws reach or promote narrative Bite to an action."
    )
    procedure["directorAuthorizedReviewRoute"] = {
        "id": ROUTE,
        "scope": "Puppetmaster's Realm authored-procedure acceptance only",
        "acceptedWitness": "The acquired Ghoul Lash two-Bone-Shot trace satisfies independent attack-member routing.",
        "notNativeNpcMultiattack": True,
        "retainedQualifications": ["AG190-H-SOURCE", "H150-ROSTER"],
    }
    retained_holds = [item for item in source["holdIds"] if item != BLOCKER]
    assert "AG190-H-SOURCE" in retained_holds
    retained_global_holds = sorted(set(retained_holds + ["H150-ROSTER"]))

    index_raw = INDEX.read_bytes()
    catalog_raw = CATALOG.read_bytes()
    index0 = read(INDEX)
    catalog0 = read(CATALOG)
    old_audit = read(A / "CURRENT30_PENDING_IDENTITY_AUDIT_292.json")
    old_queue = read(A / "CURRENT_SPELL_QUEUE_292.json")
    old_handoff = read(A / "CURRENT_HANDOFF_292.json")
    assert sha(index_raw) == delivery["currentAuthority"]["indexBinding"]["sha256"]
    assert index0["authoredCounts"] == {"reviewed": 818, "pending": 30}
    assert index0["representationCounts"]["completeReviewedStandaloneProcedures"] == 542
    assert old_audit["authority"] == old_queue["currentAuthority"] == old_handoff["currentAuthority"] == BEFORE
    assert catalog0["spells"][389]["id"] == ID
    entry0 = copy.deepcopy(next(item for item in index0["entries"] if item["id"] == ID))
    live0 = {item["id"] for item in index0["entries"] if item["authoredStatus"] == "pending-authored-procedure"}
    assert ID in live0 and len(live0) == 30

    decision_id = "RANK9-AGENCYCONTROL9-PUPPETMASTERS-REALM-DIRECTOR-DECISION-293"
    acceptance_id = "RANK9-AGENCYCONTROL9-PUPPETMASTERS-REALM-ACCEPTANCE-293"
    application_id = "RANK9-AGENCYCONTROL9-PUPPETMASTERS-REALM-APPLICATION-293"
    decision_path = A / "PUPPETMASTERS_REALM_DIRECTOR_DECISION_293.json"
    decision = {
        "id": decision_id,
        "recordedAtUtc": stamp,
        "decision": "EXACT_ACCEPT_WITH_SPELL_SPECIFIC_ALTERNATE_REVIEW_ROUTE",
        "identity": ID,
        "blocker": BLOCKER,
        "accepted": True,
        "appliedAtDecision": False,
        "source": {"service": "ChatGPT", "conversationTitle": "Calibration review part 6", "url": URL},
        "exactDirectorResponse": DIRECTOR_TEXT,
        "authorizedRevision": {
            "id": ROUTE,
            "scope": "This spell's authored-procedure review only.",
            "positiveWitness": "Acquired Ghoul Lash two-Bone-Shot trace for independent attack-member routing.",
            "nativeNpcMultiattackClaimed": False,
            "retainedQualifications": ["AG190-H-SOURCE", "H150-ROSTER"],
        },
        "packet": bind(zip_path, archive_raw),
        "deliveryManifest": bind(manifest_path),
        "reviewRequest": bind(request_path),
        "sourceSearch": bind(source_search_path),
        "independentAudit": bind(audit_path),
        "verifiedEvidence": {
            "archiveMemberCount": 11,
            "payloadCountExcludingManifest": 10,
            "preservedCaseCount": len(preserved),
            "events": total_events,
            "forwardOperations": total_forward,
            "inverseOperations": total_inverse,
        },
        "authorityAtDecision": {
            "reviewedApplied": 818,
            "pending": 30,
            "acceptedUnapplied": 1,
            "otherHeld": 29,
            "completeStandaloneProcedures": 542,
            "scopedInterfaces": 173,
        },
        "authorityAfterApplicationExpected": AFTER,
        "nextPriority": {
            "identity": NEXT,
            "blocker": NEXT_BLOCKER,
            "group": NEXT_GROUP,
            "afterThisGroup": ["mass-phantom-killer", "weird"],
            "remainingCount": 29,
        },
        "retainedQualifications": QUALS,
        "retainedHoldIds": retained_global_holds,
        "otherSpellAccepted": False,
        "catalogChangedByDecision": False,
        "downstreamGatesStillClosed": True,
    }
    write(decision_path, decision)
    decision_ref = bind(decision_path)

    PKG.mkdir(parents=True)
    source_procedure = copy.deepcopy(source)
    source_procedure["procedure"] = procedure
    source_procedure.update(
        {
            "status": "DIRECTOR_ACCEPTED_STATIC_AUTHORED_PROCEDURE_APPLIED_RUNTIME_DISABLED",
            "accepted": True,
            "applied": True,
            "blockerIds": [],
            "closedBlockerIds": [BLOCKER],
            "resolvedBlockerIds": [BLOCKER],
            "directorAuthorizedReviewRoute": ROUTE,
            "retainedQualifications": QUALS,
            "holdIds": retained_holds,
            "retainedGlobalHoldIds": retained_global_holds,
            "directorDecisionBinding": decision_ref,
            "closureReviewRequest": bind(request_path),
            "closureReviewAudit": bind(audit_path),
            "scope": "Puppetmaster's Realm authored procedure and class-feature attack-member routing witness only; native NPC Multiattack remains held; runtime disabled.",
        }
    )
    witness_path = BASE / "cases/RANK9AGENCYCONTROL9129-PUPPETMASTER-S-REALM-B__actual-two-attack-command.json"
    held_path = BASE / "cases/RANK9AGENCYCONTROL9129-PUPPETMASTER-S-REALM-B__native-multiattack-held.json"
    coverage = {
        "id": "PUPPETMASTERS-REALM-CASE-COVERAGE-293",
        "spellId": ID,
        "preservedCases": {"bindings": preserved, "count": 7, "unchanged": True},
        "acceptedWitness": {
            "routeId": ROUTE,
            "binding": bind(witness_path),
            "status": "AUTHORED_STATIC_TRACE",
            "trace": "Acquired Ghoul Lash uses two copies of Bone Shot as independent class-feature attack members.",
            "satisfies": "Independent attack-member routing obligation for authored-procedure review.",
            "nativeNpcMultiattack": False,
        },
        "retainedNativeMultiattackHold": {
            "binding": bind(held_path),
            "documentaryOnly": True,
            "nativeNpcMultiattackPositiveEncounter": False,
            "requiredFacts": ["complete lawful creature profile", "authorized attack members", "numeric reach/range", "acquisition/control history"],
            "retainedHoldIds": ["AG190-H-SOURCE", "H150-ROSTER"],
        },
        "replayTotals": {"events": total_events, "forwardOperations": total_forward, "inverseOperations": total_inverse},
        "lifecycleAssertions": {
            "redirectionAndVoluntaryMovementCasesPreserved": True,
            "forcedMovementAndTeleportDistinctionPreserved": True,
            "twoRealmArbitrationAndTerminalTurningPreserved": True,
            "paidCounteredReadyAndNoHiddenEventOracleCasesPreserved": True,
            "noCreatureStatisticsInferred": True,
        },
        "scope": "Static authored cases; no NPC native-Multiattack source, runtime operation, or downstream gate is asserted.",
    }
    evidence = {
        "id": "PUPPETMASTERS-REALM-ACCEPTED-EVIDENCE-293",
        "sourceProcedure": bind(source_path, source_raw),
        "deliveryManifest": bind(manifest_path),
        "closurePacket": bind(zip_path, archive_raw),
        "reviewRequest": bind(request_path),
        "sourceSearch": bind(source_search_path),
        "independentAudit": bind(audit_path),
        "directorDecision": decision_ref,
        "preservedCases": preserved,
        "acceptedGhoulLashWitness": bind(witness_path),
        "retainedNativeMultiattackHold": bind(held_path),
        "retainedQualifications": QUALS,
    }
    write(PKG / "DIRECTOR_DECISION.json", decision)
    write(PKG / "PREVIOUS_PROCEDURE_RECORD.json", source)
    write(PKG / "PROCEDURE_RECORD.json", source_procedure)
    write(PKG / "CASE_COVERAGE.json", coverage)
    write(PKG / "EVIDENCE_BINDINGS.json", evidence)
    write(PKG / "AG190_B02_CLOSURE_REVIEW_REQUEST_293.json", request)
    write(PKG / "AG190_B02_CLOSURE_REVIEW_AUDIT_293.json", audit)
    write(PKG / "AG190_B02_NATIVE_MULTIATTACK_SOURCE_SEARCH_293.json", read(source_search_path))
    model = {
        "schemaVersion": 1,
        "moduleId": "rank9agencycontrol9-puppetmastersrealm-reviewed-293",
        "status": "ONE_EXACT_STATIC_AUTHORED_PROCEDURE_ACCEPTED_AND_APPLIED_RUNTIME_DISABLED",
        "scope": "Puppetmaster's Realm authored procedure accepted under AG190-B02-ALTERNATE-REVIEW-ROUTE-01. The Ghoul Lash class-feature witness does not stand for native NPC Multiattack.",
        "acceptedIds": [ID],
        "unacceptedIds": [],
        "excludedPendingIds": sorted(live0 - {ID}),
        "unresolvedQualifications": {ID: QUALS},
        "sharedRequirements": {"scope": "No global rule or native catalog changes; actual NPC Multiattack remains source-qualified.", "runtimeSelectionEnabled": False},
        "spells": [
            {
                "id": ID,
                "name": NAME,
                "position": 0,
                "procedure": {
                    "id": "AG190-STATIC-PUPPETMASTERS-REALM-293",
                    "spellId": ID,
                    "status": "director-accepted static authored procedure; applied to authored review index; runtime disabled",
                    "accepted": True,
                    "applied": True,
                    "nativeCardUnchanged": copy.deepcopy(source["nativeCardUnchanged"]),
                    "procedureContent": json.dumps(procedure, ensure_ascii=False, indent=2),
                    "procedureRecordFile": "PROCEDURE_RECORD.json",
                    "directorAuthorizedReviewRoute": ROUTE,
                    "retainedQualifications": QUALS,
                    "closedBlockerIds": [BLOCKER],
                    "retainedHoldIds": retained_global_holds,
                    "caseIds": source["caseIds"],
                    "directorDecisionId": decision_id,
                    "evidenceBindingsFile": "EVIDENCE_BINDINGS.json",
                    "caseCoverageFile": "CASE_COVERAGE.json",
                },
                "directorProcedureRecord": source_procedure,
                "previousProcedureRecord": source,
                "nativeCardUnchanged": copy.deepcopy(source["nativeCardUnchanged"]),
                "caseIds": source["caseIds"],
                "retainedHoldIds": retained_global_holds,
                "runtimeSelectionEnabled": False,
            }
        ],
        "sourceProcedure": bind(source_path, source_raw),
        "directorDecision": decision_ref,
        "closurePacket": bind(zip_path, archive_raw),
        "independentAudit": bind(audit_path),
        "caseCoverage": coverage,
        "evidenceBindings": evidence,
        "runtimeSelectionEnabled": False,
        "runtimeTestsExecuted": False,
        "implementationApproved": False,
        "humanPlaytested": False,
        "balanceApproved": False,
        "cosmologyModified": False,
        "domainClosure": False,
        "releaseApproved": False,
    }
    write(PKG / "MODEL.json", model)
    manuscript = (
        "# Puppetmaster's Realm — accepted static authored procedure 293\n\n"
        "Director accepted Puppetmaster's Realm / AG190-B02 under the spell-specific " + ROUTE + ". "
        "This closes the whole-identity authored-procedure acceptance blocker. The acquired Ghoul Lash "
        "two-Bone-Shot trace supplies the independent attack-member routing witness; it is not native NPC Multiattack.\n\n"
        "The native catalog, creature statistics, runtime selection, and downstream gates remain unchanged.\n\n"
        "## Preserved procedure\n\n" + json.dumps(procedure, ensure_ascii=False, indent=2) + "\n\n"
        "## Retained qualifications\n\n" + "\n".join("- " + item for item in QUALS) + "\n"
    )
    (PKG / "STANDALONE_PROCEDURES.md").write_text(manuscript, encoding="utf-8", newline="\n")
    MANUSCRIPT.parent.mkdir(parents=True, exist_ok=True)
    MANUSCRIPT.write_text(manuscript, encoding="utf-8", newline="\n")

    package_manifest = {
        "id": "PUPPETMASTERS-REALM-PACKAGE-MANIFEST-293",
        "recordedAtUtc": stamp,
        "status": "DIRECTOR_ACCEPTED_STATIC_PROCEDURE_RUNTIME_DISABLED",
        "directorDecision": decision_ref,
        "files": [],
    }
    for path in sorted(PKG.rglob("*")):
        if path.is_file() and path.name != "CANDIDATE_PACKAGE_MANIFEST.json":
            package_manifest["files"].append(
                {"path": (PKG_REL / path.relative_to(PKG)).as_posix(), "bytes": path.stat().st_size, "sha256": sha(path.read_bytes())}
            )
    package_manifest_path = PKG / "CANDIDATE_PACKAGE_MANIFEST.json"
    write(package_manifest_path, package_manifest)
    model_ref = bind(PKG / "MODEL.json")
    package_ref = bind(package_manifest_path)
    coverage_ref = bind(PKG / "CASE_COVERAGE.json")
    evidence_ref = bind(PKG / "EVIDENCE_BINDINGS.json")
    manuscript_ref = bind(MANUSCRIPT)

    acceptance = {
        "id": acceptance_id,
        "recordedAtUtc": stamp,
        "status": "ONE_EXACT_STATIC_AUTHORED_PROCEDURE_ACCEPTED",
        "acceptedIds": [ID],
        "appliedIds": [],
        "closedBlockerIds": [BLOCKER],
        "directorDecision": decision_ref,
        "candidateEnvelope": model_ref,
        "candidatePackageManifest": package_ref,
        "evidenceBindings": evidence_ref,
        "caseCoverage": coverage_ref,
        "closurePacket": bind(zip_path, archive_raw),
        "independentAudit": bind(audit_path),
        "countsBefore": {"reviewedApplied": 818, "pending": 30, "acceptedUnapplied": 0},
        "countsAfterAcceptanceBeforeApplication": {"reviewedApplied": 818, "pending": 30, "acceptedUnapplied": 1},
        "retainedQualifications": QUALS,
        "retainedHoldIds": retained_global_holds,
    }
    acceptance_path = A / "PUPPETMASTERS_REALM_ACCEPTANCE_293.json"
    write(acceptance_path, acceptance)
    acceptance_ref = bind(acceptance_path)
    receipt = {
        "id": "RANK9-AGENCYCONTROL9-PUPPETMASTERS-REALM-RETURN293-RECEIPT",
        "recordedAtUtc": stamp,
        "status": "EXACT_ACCEPT_PUPPETMASTERS_REALM_AG190_B02_ONLY",
        "acceptedIds": [ID],
        "appliedIds": [],
        "closedBlockerIds": [BLOCKER],
        "directorDecision": decision_ref,
        "acceptance": acceptance_ref,
        "closurePacket": bind(zip_path, archive_raw),
        "independentAudit": bind(audit_path),
        "nextPriority": decision["nextPriority"],
        "retainedHoldIds": retained_global_holds,
        "sourceResponse": DIRECTOR_TEXT,
    }
    receipt_path = A / "PUPPETMASTERS_REALM_RETURN293_RECEIPT.json"
    write(receipt_path, receipt)
    receipt_ref = bind(receipt_path)

    backup = A / "authored_review_index.before_puppetmasters_realm_293.json"
    assert not backup.exists()
    backup.write_bytes(index_raw)
    index1 = copy.deepcopy(index0)
    entry1 = copy.deepcopy(entry0)
    entry1.update(
        {
            "authoredStatus": "reviewed-authored-operational-playtest",
            "procedureFile": "../spell_candidates/rank9agencycontrol9_puppetmastersrealm_reviewed_293/MODEL.json",
            "procedurePointer": "/spells/0/procedure",
            "wholeCardPointer": "/spells/0",
            "wholeCardIdField": "id",
            "sourceCatalogWholeCardPointer": entry0.get("sourceCatalogWholeCardPointer") or entry0["wholeCardPointer"],
            "procedureTextPointer": "/spells/0/procedure/procedureContent",
            "directorProcedureRecordPointer": "/spells/0/directorProcedureRecord",
            "sharedRulesPointer": "/sharedRequirements",
            "spellLocalRequirementsPointer": "/spells/0/procedure",
            "manuscript": "../../../docs/spells/candidates/PUPPETMASTERS_REALM_REVIEWED_293.md",
            "reviewId": acceptance_id,
            "runtimeSelectionEnabled": False,
            "historicalCandidateLabelsPreserved": True,
            "completeEvidenceRoot": PKG_REL.as_posix(),
            "completeEnvelopeBinding": model_ref,
            "caseEvidenceBindings": coverage_ref,
            "candidatePackageManifestBinding": package_ref,
            "procedureSourceBinding": decision_ref,
            "authoredAcceptanceReceipt": acceptance_ref,
            "authoredApplicationReceipt": application_id + ".json",
            "directorReturnReceipt": receipt_ref,
            "accepted": True,
            "applied": True,
            "closedBlockerIds": [BLOCKER],
            "retainedQualifications": QUALS,
            "retainedHoldIds": retained_global_holds,
            "directorAuthorizedReviewRoute": ROUTE,
        }
    )
    entry_i = next(i for i, item in enumerate(index1["entries"]) if item["id"] == ID)
    index1["entries"][entry_i] = entry1
    assert not any(ID in item.get("acceptedIds", []) for item in index1["additionalStandaloneEnvelopes"])
    envelope = {
        "file": "../spell_candidates/rank9agencycontrol9_puppetmastersrealm_reviewed_293/MODEL.json",
        "binding": model_ref,
        "reviewId": acceptance_id,
        "acceptedIds": [ID],
        "unacceptedIds": [],
        "excludedPendingIds": sorted(live0 - {ID}),
        "authority": acceptance_ref,
        "applicationReceipt": application_id + ".json",
        "directorDecision": decision_ref,
        "directorReturnReceipt": receipt_ref,
        "caseCoverage": coverage_ref,
        "candidatePackageManifestBinding": package_ref,
        "closurePacket": bind(zip_path, archive_raw),
        "independentAudit": bind(audit_path),
        "scope": "ONE_EXACT_STATIC_AUTHORED_PROCEDURE_ACCEPTED_AND_APPLIED_RUNTIME_DISABLED",
    }
    index1["additionalStandaloneEnvelopes"].append(envelope)
    index1["authoredCounts"] = {"reviewed": 819, "pending": 29}
    index1["representationCounts"]["completeReviewedStandaloneProcedures"] = 543
    live1 = {item["id"] for item in index1["entries"] if item["authoredStatus"] == "pending-authored-procedure"}
    assert live1 == live0 - {ID} and len(live1) == 29 and NEXT in live1
    write(INDEX, index1)
    index_core_ref = bind(INDEX)

    application = {
        "id": application_id,
        "recordedAtUtc": stamp,
        "status": "APPLIED_ONE_EXACT_DIRECTOR_ACCEPTED_AUTHORED_PROCEDURE",
        "acceptedIds": [ID],
        "appliedIds": [ID],
        "closedBlockerIds": [BLOCKER],
        "directorAcceptance": acceptance_ref,
        "directorDecision": decision_ref,
        "directorReturnReceipt": receipt_ref,
        "closurePacket": bind(zip_path, archive_raw),
        "independentAudit": bind(audit_path),
        "candidateEnvelope": model_ref,
        "candidatePackageManifest": package_ref,
        "evidenceBindings": evidence_ref,
        "caseCoverage": coverage_ref,
        "manuscript": manuscript_ref,
        "indexBefore": bind(backup, index_raw),
        "indexAfterCoreUpdate": index_core_ref,
        "countsBefore": BEFORE,
        "countsAfter": AFTER,
        "completeReviewedStandaloneProcedures": {"before": 542, "after": 543},
        "scopedInterfaces": 173,
        "catalogChanged": False,
        "sourceStatusPreservedAsBlocked": True,
        "nativeNpcMultiattackEnabled": False,
        "runtimeSelectionEnabled": False,
        "runtimeTestsExecuted": False,
        "implementationApproved": False,
        "humanPlaytested": False,
        "balanceApproved": False,
        "cosmologyModified": False,
        "domainClosure": False,
        "releaseApproved": False,
    }
    application_path = A / "PUPPETMASTERS_REALM_APPLICATION_293.json"
    write(application_path, application)
    application_ref = bind(application_path)
    entry1["authoredApplicationReceipt"] = application_ref
    index1["entries"][entry_i] = entry1
    index1["additionalStandaloneEnvelopes"][-1]["applicationReceipt"] = application_ref
    write(INDEX, index1)
    index_ref = bind(INDEX)
    ops_path = A / "PUPPETMASTERS_REALM_INDEX_OPERATIONS_293.json"
    write(
        ops_path,
        {
            "id": "PUPPETMASTERS-REALM-INDEX-OPERATIONS-293",
            "recordedAtUtc": stamp,
            "before": bind(backup, index_raw),
            "after": index_ref,
            "operations": [
                {"op": "update-entry", "id": ID, "before": entry0, "after": entry1},
                {"op": "append-standalone-envelope", "acceptedIds": [ID]},
                {"op": "update-authored-counts", "before": {"reviewed": 818, "pending": 30}, "after": {"reviewed": 819, "pending": 29}},
                {"op": "increment-complete-procedure-count", "before": 542, "after": 543},
            ],
            "inverse": [
                {"op": "restore-entry", "id": ID, "value": entry0},
                {"op": "remove-appended-standalone-envelope", "acceptedIds": [ID]},
                {"op": "restore-authored-counts", "value": {"reviewed": 818, "pending": 30}},
                {"op": "restore-complete-procedure-count", "value": 542},
                {"op": "restore-byte-exact-index-from-backup", "backup": bind(backup, index_raw)},
            ],
            "catalogByteExact": CATALOG.read_bytes() == catalog_raw,
            "nativeCardUnchanged": True,
            "sourceStatusPreservedAsBlocked": True,
            "nativeNpcMultiattackEnabled": False,
            "inverseRestoresExactIndex": backup.read_bytes() == index_raw,
        },
    )

    authority = copy.deepcopy(AFTER)
    groups = clean_rows(old_audit["groups"])
    order = clean_order(old_queue["recommendedClosureOrder"])
    next_requirement = "Psychic Scream / PF182-B01 is next: resolve explicit head anatomy, final-death/head consequence, and changed-form/remains settlement. Then review mass-phantom-killer and weird / PF182-B02."
    next_item = {
        "group": NEXT_GROUP,
        "pendingIds": [NEXT, "mass-phantom-killer", "weird"],
        "pendingCount": 3,
        "status": "DIRECTOR_NEXT_IDENTITY_AFTER_PUPPETMASTERS_REALM_293",
        "freshPacketRequiredForCurrentAuthority": True,
        "directorRequirement": next_requirement,
        "blockerByIdentity": {NEXT: NEXT_BLOCKER, "mass-phantom-killer": "PF182-B02", "weird": "PF182-B02"},
    }
    pending = copy.deepcopy(old_audit)
    pending.update(
        {
            "id": "CURRENT29_PENDING_IDENTITY_AUDIT_293",
            "recordedAtUtc": stamp,
            "status": "PASS_EXACT_CURRENT_INDEX_PENDING_SET_AFTER_PUPPETMASTERS_REALM_APPLICATION_293",
            "authority": authority,
            "indexBinding": index_ref,
            "catalogBinding": bind(CATALOG, catalog_raw),
            "pendingCount": 29,
            "pendingIds": sorted(live1),
            "groups": groups,
            "heldIds": sorted(set(old_audit.get("heldIds", [])) - {ID}),
            "acceptedIds": sorted(set(old_audit.get("acceptedIds", [])) | {ID}),
            "appliedIds": sorted(set(old_audit.get("appliedIds", [])) | {ID}),
            "applicationReceipt": application_ref,
            "directorDecision": decision_ref,
            "acceptanceReceipt": acceptance_ref,
            "closedBlockerIdsThisStep": sorted(set(old_audit.get("closedBlockerIdsThisStep", [])) | {BLOCKER}),
            "lastDirectorReturn": {
                "decisionId": decision_id,
                "acceptedIds": [ID],
                "appliedIds": [ID],
                "heldIds": [],
                "closedBlockerIds": [BLOCKER],
                "authorizedRevision": ROUTE,
                "packet": bind(zip_path, archive_raw),
                "independentAudit": bind(audit_path),
            },
            "nextBlockerPriority": [item for item in old_queue["recommendedClosurePriority"] if item != ID],
            "preparedNextGroup": next_item,
            "remainingPendingCount": 29,
            "pendingIdentityCount": 29,
            "nativeNpcMultiattackEnabled": False,
        }
    )
    pending_path = A / "CURRENT29_PENDING_IDENTITY_AUDIT_293.json"
    write(pending_path, pending)
    pending_ref = bind(pending_path)

    queue = copy.deepcopy(old_queue)
    queue.update(
        {
            "id": "SPELL-REVIEW-QUEUE-293",
            "recordedAtUtc": stamp,
            "supersedesQueue": bind(A / "CURRENT_SPELL_QUEUE_292.json"),
            "parentQueue": bind(A / "CURRENT_SPELL_QUEUE_292.json"),
            "currentAuthority": authority,
            "currentIndexBinding": index_ref,
            "pendingIdentityAudit": pending_ref,
            "pendingCount": 29,
            "nextGroup": NEXT_GROUP,
            "next": next_item,
            "nextPendingIds": [NEXT, "mass-phantom-killer", "weird"],
            "currentPendingGroups": groups,
            "nextSuggestedGroups": [next_item],
            "recommendedClosureOrder": order,
            "recommendedClosurePriority": [item for item in old_queue["recommendedClosurePriority"] if item != ID],
            "lastReviewedBatch": {"group": "rank9-agency-control9", "acceptedIds": [ID], "appliedIds": [ID], "heldIds": [], "closedBlockerIds": [BLOCKER]},
            "justAppliedBatch": {
                "reviewId": acceptance_id,
                "applicationId": application_id,
                "ids": [ID],
                "count": 1,
                "applicationReceipt": application_ref,
                "directorDecision": decision_ref,
                "closurePacket": bind(zip_path, archive_raw),
                "independentAudit": bind(audit_path),
            },
            "packetStatus": "PUPPETMASTERS_REALM_AG190_B02_ACCEPTED_AND_APPLIED; NEXT_PSYCHIC_SCREAM_PF182_B01",
            "currentAcceptedPacket": {
                "sourceProcedure": bind(source_path, source_raw),
                "directorDecision": decision_ref,
                "acceptance": acceptance_ref,
                "application": application_ref,
                "closurePacket": bind(zip_path, archive_raw),
                "independentAudit": bind(audit_path),
            },
            "currentDirectorPosition": {
                "stage": "PUPPETMASTERS_REALM_ACCEPTED_AG190_B02; PSYCHIC_SCREAM_NEXT",
                "acceptedIds": [ID],
                "appliedIds": [ID],
                "heldIds": sorted(live1),
                "blockers": {NEXT: [NEXT_BLOCKER], "mass-phantom-killer": ["PF182-B02"], "weird": ["PF182-B02"]},
                "nextPendingGroup": {"group": NEXT_GROUP, "pendingIds": [NEXT], "pendingCount": 1, "reportedByDirector": True},
            },
            "nextPriorityContext": {"identity": NEXT, "blocker": NEXT_BLOCKER, "requirement": next_requirement},
            "githubChanges": False,
            "canonicalRuntimeApplicationPerformed": False,
            "afterNextAcceptedAppliedForecast": {"remainingIdentities": 28},
        }
    )
    queue_path = A / "CURRENT_SPELL_QUEUE_293.json"
    write(queue_path, queue)
    queue_ref = bind(queue_path)
    handoff = copy.deepcopy(old_handoff)
    handoff.update(
        {
            "id": "CURRENT-HANDOFF-293",
            "recordedAtUtc": stamp,
            "supersedes": old_handoff["id"],
            "status": "PUPPETMASTERS_REALM_APPLIED_NEXT_PSYCHIC_SCREAM_819_29",
            "authority": authority,
            "currentAuthority": authority,
            "indexBinding": index_ref,
            "queueBinding": queue_ref,
            "queue": queue_path.relative_to(ROOT).as_posix(),
            "pendingIdentityAudit": pending_ref,
            "appliedThisStep": True,
            "acceptedThisStep": [ID],
            "appliedThisStepRecord": {"identity": ID, "application": application_path.relative_to(ROOT).as_posix(), "applicationBinding": application_ref, "closedBlockerIds": [BLOCKER]},
            "nextStep": next_item,
            "nextGroup": NEXT_GROUP,
            "nextPendingCount": 3,
            "nextPendingIds": [NEXT, "mass-phantom-killer", "weird"],
            "currentBlocker": {"identity": NEXT, "group": NEXT_GROUP, "blockerId": NEXT_BLOCKER},
            "directorConnectionStatus": "GPT explicitly accepted Puppetmaster's Realm / AG190-B02 under AG190-B02-ALTERNATE-REVIEW-ROUTE-01 only; next is Psychic Scream / PF182-B01.",
            "githubChanges": False,
            "latestBatch": {"accepted": [ID], "applied": [ID], "closed": [BLOCKER]},
            "currentPreparation": next_item,
            "canonicalRuntimeApplicationPerformed": False,
            "nextStepText": next_requirement,
        }
    )
    handoff_path = A / "CURRENT_HANDOFF_293.json"
    write(handoff_path, handoff)
    handoff_ref = bind(handoff_path)

    checks = [
        ("Director accepted Puppetmaster's Realm under the exact spell-specific route only", decision["accepted"] and decision["authorizedRevision"]["id"] == ROUTE and decision["otherSpellAccepted"] is False),
        ("Packet293 exact ZIP hash, CRC, 11 members, and independent audit pass", sha(archive_raw) == "ae5dbd25fb55a471ebceedd327bcf22bf754c73006b720c41623e52edb40481e" and len(names) == 11 and audit["passedChecks"] == 15),
        ("Seven preserved case hashes and 157-event full reversible traversal validate", len(preserved) == 7 and (total_events, total_forward, total_inverse) == (157, 314, 314)),
        ("Accepted Ghoul Lash witness is not relabeled as NPC Multiattack", coverage["acceptedWitness"]["nativeNpcMultiattack"] is False and coverage["retainedNativeMultiattackHold"]["documentaryOnly"] is True),
        ("Only Puppetmaster's Realm leaves the pending set", live1 == live0 - {ID} and len(live1) == 29 and NEXT in live1),
        ("Authority advances to 819/29/0 and 543/173", index1["authoredCounts"] == {"reviewed": 819, "pending": 29} and index1["representationCounts"]["completeReviewedStandaloneProcedures"] == 543 and authority == AFTER),
        ("Native catalog byte-exact and source remains blocked", CATALOG.read_bytes() == catalog_raw and index1["entries"][entry_i]["sourceStatus"] == "blocked-pending-operational-review"),
        ("AG190-H-SOURCE and H150-ROSTER remain retained", "AG190-H-SOURCE" in retained_global_holds and "H150-ROSTER" in retained_global_holds and ROUTE in index1["entries"][entry_i]["retainedQualifications"][0]),
        ("Runtime and downstream gates remain closed", model["runtimeSelectionEnabled"] is False and model["implementationApproved"] is False and model["releaseApproved"] is False),
        ("Next priority is Psychic Scream / PF182-B01", queue["next"]["pendingIds"][0] == NEXT and queue["nextGroup"] == NEXT_GROUP and decision["nextPriority"]["blocker"] == NEXT_BLOCKER),
        ("Backup restores exact original index bytes", backup.read_bytes() == index_raw),
        ("Pending audit, queue, and handoff bind final index", pending["indexBinding"]["sha256"] == index_ref["sha256"] and queue["currentIndexBinding"]["sha256"] == index_ref["sha256"] and handoff["indexBinding"]["sha256"] == index_ref["sha256"]),
    ]
    assert all(ok for _, ok in checks), [name for name, ok in checks if not ok]
    validation = {
        "id": "PUPPETMASTERS-REALM-APPLICATION-VALIDATION-293",
        "recordedAtUtc": stamp,
        "status": "PASS",
        "checks": [{"check": name, "passed": ok} for name, ok in checks],
        "checkCount": len(checks),
        "failedChecks": 0,
        "acceptedIds": [ID],
        "appliedIds": [ID],
        "closedBlockerIds": [BLOCKER],
        "retainedHoldIds": retained_global_holds,
        "authority": authority,
        "index": index_ref,
        "application": application_ref,
        "pendingIdentityAudit": pending_ref,
        "queue": queue_ref,
        "handoff": handoff_ref,
        "indexOperations": bind(ops_path),
        "catalogByteExact": True,
        "sourceStatusPreservedAsBlocked": True,
        "nativeNpcMultiattackEnabled": False,
        "runtimeSelectionEnabled": False,
    }
    validation_path = A / "PUPPETMASTERS_REALM_APPLICATION_VALIDATION_293.json"
    write(validation_path, validation)
    validation_ref = bind(validation_path)
    snapshot_path = A / "CURRENT_SPELL_REVIEW_SNAPSHOT_293.md"
    snapshot_path.write_text(
        "# Spell Review Snapshot — Puppetmaster's Realm Application 293\n\n"
        "Authority: **819 applied / 29 pending / 0 accepted-unapplied; 543 complete standalone procedures / 173 scoped interfaces.**\n\n"
        "Puppetmaster's Realm / AG190-B02 was accepted under AG190-B02-ALTERNATE-REVIEW-ROUTE-01 and applied to the authored review index. The acquired Ghoul Lash two-Bone-Shot trace is the class-feature routing witness; it is not native NPC Multiattack. AG190-H-SOURCE and H150-ROSTER remain retained, and sourceStatus/runtime/downstream gates remain blocked.\n\n"
        "Next priority: **psychic-scream / PF182-B01**, followed by mass-phantom-killer and weird / PF182-B02.\n\n"
        "Validation: " + validation_ref["path"] + " (" + validation_ref["sha256"] + ").\n",
        encoding="utf-8",
        newline="\n",
    )
    assert sha(INDEX.read_bytes()) == index_ref["sha256"] and CATALOG.read_bytes() == catalog_raw
    assert backup.read_bytes() == index_raw and application_ref["path"] == application_path.relative_to(ROOT).as_posix()
    print(json.dumps({"status": "PASS", "acceptedApplied": ID, "route": ROUTE, "authority": AFTER, "index": index_ref, "application": application_ref, "validation": validation_ref, "pendingAudit": pending_ref, "queue": queue_ref, "next": decision["nextPriority"]}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
