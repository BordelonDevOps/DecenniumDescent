from __future__ import annotations

import copy
import datetime as dt
import hashlib
import json
import pathlib
import shutil
import subprocess
import zipfile
import zlib


ROOT = pathlib.Path(__file__).resolve().parents[5]
A = ROOT / "docs/audit/2026-10-08/full-game/director-spell-review-129"
ID = "psychic-scream"
NAME = "Psychic Scream"
BLOCKER = "PF182-B01"
REVISION = "PF182-B01-BOUNDED-ANATOMY-LIFECYCLE-CONTRACT-01"
NEXT_IDS = ["mass-phantom-killer", "weird"]
NEXT_GROUP = "rank9-psychic-fear7"
URL = "https://chatgpt.com/g/g-p-67f17555a8dc8191a2b5b81e6d8adc12-dungeon-crawler/c/6adc506d-8770-83ea-b64c-0345d9b9b682"
DELTA294 = A / "rank9_psychic_scream_closure_delta_294/DD_Rank9_PsychicScream_ClosureDelta_294.zip"
DELTA296_DIR = A / "rank9_psychic_scream_fixture_correction_296"
DELTA296 = DELTA296_DIR / "DD_Rank9_PsychicScream_FixtureCorrection_296.zip"
DELTA296_AUDIT = DELTA296_DIR / "INDEPENDENT_AUDIT_296.json"
DELTA296_CONTRACT = DELTA296_DIR / "ANATOMY_LIFECYCLE_CONTRACT_296.json"
RETURN234 = A / "rank9_psychicfear7_return234_received/DD_Rank9_PsychicFear3_Director_Return234_HELD.zip"
RETURN234_RECEIPT = A / "RANK9PSYCHICFEAR7_RETURN234_RECEIPT.json"
DISPOSITIONS294 = A / "rank9_psychic_scream_closure_delta_294/PRESERVED_PSYCHIC_SCREAM_DISPOSITIONS_294.json"
CASE_BINDINGS294 = A / "rank9_psychic_scream_closure_delta_294/PSYCHIC_SCREAM_CASE_BINDINGS_294.json"
INDEX = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json"
CATALOG = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json"
REGISTRY = ROOT / "DescentReviewChanges/ReviewBible/data/director/spell_review/accepted_interface_registry_06.json"
QUEUE0 = A / "CURRENT_SPELL_QUEUE_293.json"
HANDOFF0 = A / "CURRENT_HANDOFF_293.json"
PENDING0 = A / "CURRENT29_PENDING_IDENTITY_AUDIT_293.json"
PKG_REL = pathlib.Path("DescentReviewChanges/ReviewBible/data/public/spell_candidates/rank9psychicscream_reviewed_296")
PKG = ROOT / PKG_REL
MANUSCRIPT = ROOT / "DescentReviewChanges/ReviewBible/docs/spells/candidates/PSYCHIC_SCREAM_REVIEWED_296.md"
BEFORE = {"reviewedApplied": 819, "pending": 29, "acceptedUnapplied": 0, "completeStandaloneProcedures": 543, "scopedInterfaces": 173}
AFTER = {"reviewedApplied": 820, "pending": 28, "acceptedUnapplied": 0, "completeStandaloneProcedures": 544, "scopedInterfaces": 173}
RETAINED_BOUNDARIES = [
    "PF181-H01", "PF181-H02", "PF181-H03", "PF181-H04", "PF181-H07", "PF181-H08",
    "PF181-H09", "PF181-H10", "PF181-H11", "PF181-H12", "PF181-H13", "PF181-H14",
]
DIRECTOR_TEXT = (
    "ACCEPT psychic-scream / PF182-B01 — accepted=true, applied=false. "
    "I accept PF182-B01-BOUNDED-ANATOMY-LIFECYCLE-CONTRACT-01, revision296, and its four conditional synthetic fixtures for authored-procedure review. "
    "PF295-C01/C02 are resolved; PF182-B01 closes as an acceptance blocker. Verified: paid cast 0.2, save 0.3, final death 0.31, head consequence 0.32, with Form Change at 0.1; correct Instant Death calculation, terminal-form selection, headless/multihead outcomes, remains and equipment custody; 17 events, 34 forward and 34 inverse operations, state hashes, continuity and full reverse traversal; exact eight-member allowlist, payload hashes/CRCs and prior-packet bindings. "
    "The four fixtures supersede the two incomplete anatomy records for review coverage while preserving those historical records. PF181-H03 and actual-target source qualifications remain: synthetic anatomy supplies no campaign creature facts. Mage Evocation stun, all three printed placements, no Illusion acquisition route, and all other qualifications/downstream gates remain unchanged. "
    "Counts: 819 applied, 1 accepted-unapplied, and 28 other held. The canonical index remains 819/29 until application. After verified application: 820 applied / 28 pending / 0 accepted-unapplied; 544 procedures / 173 interfaces. Next: mass-phantom-killer / PF182-B02, then weird / PF182-B02, then final-word / DR217-B01. No other identity is accepted or applied."
)
QUALIFICATIONS = [
    "Acceptance is limited to Psychic Scream's Wizard/Enchantment authored-procedure review under PF182-B01-BOUNDED-ANATOMY-LIFECYCLE-CONTRACT-01 revision296.",
    "The four conditional anatomy/lifecycle fixtures are synthetic, not source-defined creature facts, observed runtime, or campaign actor evidence. They replace the two incomplete anatomy records for review coverage only; both historical records remain preserved byte-exact.",
    "PF181-H03 and all other retained PF181 boundary qualifications remain. Actual campaign use still requires source-qualified current body/form anatomy, enumerated heads, destructibility/vital relationship, and exact reversion/remains lifecycle.",
    "The Mage/Evocation damage/stun route remains independent. All three printed Enchantment, Evocation, and Illusion placements remain unchanged; Illusion supplies no class-access route. Actual access remains Mage/Evocation and Wizard/Enchantment only.",
    "Native catalog sourceStatus stays blocked-pending-operational-review; runtime selection remains disabled. No source-access, runtime, implementation, human-play, balance, cosmology, domain-closure, or release approval is granted.",
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


def bind(path: pathlib.Path, raw: bytes | None = None) -> dict:
    data = path.read_bytes() if raw is None else raw
    return {"path": path.relative_to(ROOT).as_posix(), "bytes": len(data), "sha256": sha(data), "crc32": f"{zlib.crc32(data) & 0xFFFFFFFF:08x}"}


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
    cleaned = []
    for old in rows:
        row = copy.deepcopy(old)
        key = next((k for k in ("identities", "pendingIds", "spellIds") if isinstance(row.get(k), list)), None)
        if key:
            row[key] = [item for item in row[key] if item != ID]
            if not row[key]:
                continue
            if "pendingCount" in row:
                row["pendingCount"] = len(row[key])
        row["priority"] = len(cleaned) + 1
        cleaned.append(row)
    return cleaned


def main() -> None:
    assert not PKG.exists() and not MANUSCRIPT.exists(), "Refusing to overwrite application outputs."
    assert bind(DELTA296)["sha256"] == "d6006fd3bf3999603ad55e090a3e53b39d151a35747938ad052db7bc527e23ac"
    assert bind(DELTA294)["sha256"] == "a64fbd6b4efd339c84d3bb4afd6fa5d42f72287bfa552f02e97963f81461b197"
    stamp = dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")
    current_head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    branch = subprocess.check_output(["git", "branch", "--show-current"], cwd=ROOT, text=True).strip()
    assert branch == "main"
    audit296 = read(DELTA296_AUDIT)
    contract = read(DELTA296_CONTRACT)
    assert audit296["status"] == "PASS" and audit296["caseCount"] == 4 and audit296["eventCount"] == 17
    assert audit296["forwardOperations"] == audit296["inverseOperations"] == 34
    assert contract["id"] == REVISION and contract["status"].startswith("PROPOSED_FOR_DIRECTOR_ADJUDICATION")

    index_raw = INDEX.read_bytes()
    catalog_raw = CATALOG.read_bytes()
    index0, catalog0 = read(INDEX), read(CATALOG)
    queue0, handoff0, pending0 = read(QUEUE0), read(HANDOFF0), read(PENDING0)
    assert index0["authoredCounts"] == {"reviewed": 819, "pending": 29}
    assert index0["representationCounts"]["completeReviewedStandaloneProcedures"] == 543
    assert queue0["currentAuthority"] == handoff0["currentAuthority"] == pending0["authority"] == BEFORE
    assert pending0["pendingCount"] == 29 and ID in pending0["pendingIds"]
    assert catalog0["spells"][395]["id"] == ID
    assert catalog0["spells"][395]["operational"] is None
    entry0 = copy.deepcopy(next(row for row in index0["entries"] if row["id"] == ID))
    live0 = {row["id"] for row in index0["entries"] if row["authoredStatus"] == "pending-authored-procedure"}
    assert ID in live0 and len(live0) == 29
    package_baseline = read(DISPOSITIONS294)
    assert package_baseline["return234Decision"]["heldCaseIds"] == [
        "RANK9PSYCHICFEAR7-180-PSYCHIC-SCREAM-B/positive-final-death-head-consequence",
        "RANK9PSYCHICFEAR7-180-PSYCHIC-SCREAM-B/headless-multihead-current-form",
    ]
    case_bindings = read(CASE_BINDINGS294)
    assert case_bindings["caseCount"] == 16 and case_bindings["eventCount"] == 227
    retained = sorted(RETAINED_BOUNDARIES)
    assert "PF181-H03" in retained and BLOCKER not in retained

    # Verify the exact accepted archive and every member before applying its scope.
    with zipfile.ZipFile(DELTA296) as archive:
        assert archive.testzip() is None
        assert len(archive.namelist()) == 8
        delta_members = {row["path"]: row for row in read(DELTA296_DIR / "DELIVERY_MANIFEST_296.json")["files"]}
        assert len(delta_members) == 7
        for member, row in delta_members.items():
            raw = archive.read(member)
            assert len(raw) == row["bytes"] and sha(raw) == row["sha256"]
            assert f"{zlib.crc32(raw) & 0xFFFFFFFF:08x}" == row["crc32"]
        fixture_values = [json.loads(archive.read(f"fixtures/{i:02d}.json")) for i in range(1, 5)]
    assert all(f["fixtureOnly"] and not f["observedRuntimeOrCampaign"] and not f["existingCreatureSourceEvidence"] for f in fixture_values)
    assert all(f["replayAudit"]["fullReverseTraversalRestoresInitial"] for f in fixture_values)

    with zipfile.ZipFile(RETURN234) as archive:
        assert archive.testzip() is None
        source_procedure = json.loads(archive.read("procedures/psychic-scream.json"))
        return_ref = bind(RETURN234)
        preserved_case_rows = case_bindings["cases"]
        for row in preserved_case_rows:
            raw = archive.read(row["member"])
            assert len(raw) == row["bytes"] and sha(raw) == row["sha256"]

    procedure = copy.deepcopy(source_procedure)
    original_enchantment = procedure["localProcedure"]["enchantment"]
    original_hold_sentence = "Missing anatomy/current-form/lifecycle facts hold the entire positive head branch."
    replacement_sentence = (
        "Missing actual-target source anatomy/current-form/lifecycle facts continue to block real-campaign use. "
        "For authored-procedure review only, Director-accepted synthetic conditional anatomy/lifecycle fixtures "
        "replace the two incomplete historical anatomy records under PF182-B01-BOUNDED-ANATOMY-LIFECYCLE-CONTRACT-01 revision296."
    )
    assert original_hold_sentence in original_enchantment
    procedure["localProcedure"]["enchantment"] = original_enchantment.replace(original_hold_sentence, replacement_sentence)
    procedure["accepted"] = True
    procedure["applied"] = True
    procedure["status"] = "director-accepted static authored procedure; applied to authored review index; runtime disabled"
    procedure["acceptedReviewRevision"] = {
        "id": REVISION,
        "revision": 296,
        "scope": "Wizard/Enchantment authored-procedure review only",
        "boundedSyntheticContract": copy.deepcopy(contract),
        "replacementFixtureIds": [fixture["id"] for fixture in fixture_values],
        "historicalHeldRecordsPreserved": package_baseline["return234Decision"]["heldCaseIds"],
        "retainedQualifications": retained,
        "actualTargetSourceQualification": "PF181-H03 and source-qualified actual body/form/head/lifecycle facts remain mandatory for actual campaign targets.",
    }
    procedure["closedBlockerIds"] = [BLOCKER]
    procedure["retainedQualificationIds"] = retained

    decision_id = "RANK9-PSYCHIC-SCREAM-PF182-B01-DIRECTOR-DECISION-296"
    acceptance_id = "RANK9-PSYCHIC-SCREAM-PF182-B01-ACCEPTANCE-296"
    application_id = "RANK9-PSYCHIC-SCREAM-PF182-B01-APPLICATION-296"
    decision_path = A / "PSYCHIC_SCREAM_DIRECTOR_DECISION_296.json"
    decision = {
        "id": decision_id,
        "recordedAtUtc": stamp,
        "decision": "EXACT_ACCEPT_BOUNDED_SYNTHETIC_AUTHORED_PROCEDURE_REVIEW_ROUTE",
        "identity": ID,
        "blocker": BLOCKER,
        "accepted": True,
        "appliedAtDecision": False,
        "source": {"service": "ChatGPT", "conversationTitle": "Calibration review part 6", "url": URL},
        "exactDirectorResponse": DIRECTOR_TEXT,
        "acceptedRevision": {"id": REVISION, "revision": 296, "scope": "Psychic Scream Wizard/Enchantment authored-procedure review only", "fixtureCount": 4, "acceptedArchive": bind(DELTA296), "retainedQualifications": QUALIFICATIONS, "retainedQualificationIds": retained},
        "verifiedCorrectionIds": ["PF295-C01", "PF295-C02"],
        "countsBeforeApplication": {"reviewedApplied": 819, "pending": 29, "acceptedUnapplied": 1, "otherHeld": 28},
        "forecastAfterVerifiedApplication": AFTER,
        "nextPriority": {"group": NEXT_GROUP, "pendingIds": NEXT_IDS, "blockers": {"mass-phantom-killer": "PF182-B02", "weird": "PF182-B02", "final-word": "DR217-B01"}},
        "noOtherIdentityAcceptedOrApplied": True,
        "nativeCatalogChanged": False,
        "runtimeSelectionEnabled": False,
    }
    write(decision_path, decision)
    decision_ref = bind(decision_path)
    acceptance_path = A / "PSYCHIC_SCREAM_ACCEPTANCE_296.json"
    acceptance = {
        "id": acceptance_id,
        "recordedAtUtc": stamp,
        "status": "ONE_EXACT_STATIC_AUTHORED_PROCEDURE_ACCEPTED",
        "acceptedIds": [ID],
        "appliedIds": [],
        "closedBlockerIds": [BLOCKER],
        "directorDecision": decision_ref,
        "acceptedRevision": {"id": REVISION, "revision": 296, "contract": bind(DELTA296_CONTRACT), "fixtures": [{"id": fixture["id"], "sha256": sha(encode(fixture))} for fixture in fixture_values]},
        "countsBeforeAcceptance": {"reviewedApplied": 819, "pending": 29, "acceptedUnapplied": 0},
        "countsAfterAcceptanceBeforeApplication": {"reviewedApplied": 819, "pending": 29, "acceptedUnapplied": 1},
        "retainedQualifications": QUALIFICATIONS,
        "retainedQualificationIds": retained,
        "historicalHeldCaseRecordsPreserved": package_baseline["return234Decision"]["heldCaseIds"],
        "actualTargetSourceRequirement": "PF181-H03 remains; synthetic anatomy supplies no campaign creature facts.",
    }
    write(acceptance_path, acceptance)
    acceptance_ref = bind(acceptance_path)
    return_receipt_path = A / "PSYCHIC_SCREAM_RETURN296_RECEIPT.json"
    return_receipt = {"id": "RANK9-PSYCHIC-SCREAM-DIRECTOR-RETURN296-RECEIPT", "recordedAtUtc": stamp, "status": "EXACT_ACCEPT_PF182_B01_ONLY", "acceptedIds": [ID], "appliedIds": [], "closedBlockerIds": [BLOCKER], "directorDecision": decision_ref, "acceptance": acceptance_ref, "acceptedArchive": bind(DELTA296), "sourceResponse": DIRECTOR_TEXT, "nextPriority": decision["nextPriority"], "retainedQualificationIds": retained}
    write(return_receipt_path, return_receipt)
    return_receipt_ref = bind(return_receipt_path)

    candidate_package = PKG
    (candidate_package / "fixtures").mkdir(parents=True)
    fixture_refs = []
    for number, fixture in enumerate(fixture_values, start=1):
        destination = candidate_package / "fixtures" / f"{number:02d}.json"
        write(destination, fixture)
        fixture_refs.append({"id": fixture["id"], **bind(destination)})
    procedure["originalQuestionsUnchanged"] = copy.deepcopy(source_procedure["originalQuestionsUnchanged"])
    procedure["nativeBookBindingsUnchanged"] = copy.deepcopy(source_procedure["nativeBookBindingsUnchanged"])
    procedure["nativeCardAndAccessUnchanged"] = copy.deepcopy(source_procedure["nativeCardAndAccessUnchanged"])
    write(candidate_package / "PROCEDURE_RECORD.json", procedure)
    procedure_ref = bind(candidate_package / "PROCEDURE_RECORD.json")

    old_held_ids = set(package_baseline["return234Decision"]["heldCaseIds"])
    old_held_event_count = sum(row["events"] for row in preserved_case_rows if row["id"] in old_held_ids)
    old_held_forward = sum(row["forwardOperations"] for row in preserved_case_rows if row["id"] in old_held_ids)
    old_held_inverse = sum(row["inverseOperations"] for row in preserved_case_rows if row["id"] in old_held_ids)
    fixture_event_count = sum(len(fixture["events"]) for fixture in fixture_values)
    fixture_forward = sum(sum(len(event["forward"]) for event in fixture["events"]) for fixture in fixture_values)
    fixture_inverse = sum(sum(len(event["inverse"]) for event in fixture["events"]) for fixture in fixture_values)
    coverage = {
        "id": "PSYCHIC-SCREAM-ACCEPTED-CASE-COVERAGE-296",
        "historicalReturn234": return_ref,
        "historicalCaseCount": 16,
        "historicalEventCount": 227,
        "historicalForwardOperations": 454,
        "historicalInverseOperations": 454,
        "historicalCases": preserved_case_rows,
        "historicalAnatomyRecordsPreservedButSupersededForReviewCoverage": sorted(old_held_ids),
        "supersededHistoricalEventCount": old_held_event_count,
        "supersededHistoricalForwardOperations": old_held_forward,
        "supersededHistoricalInverseOperations": old_held_inverse,
        "acceptedSyntheticFixtureCases": fixture_refs,
        "acceptedSyntheticFixtureCount": 4,
        "acceptedSyntheticEventCount": fixture_event_count,
        "acceptedSyntheticForwardOperations": fixture_forward,
        "acceptedSyntheticInverseOperations": fixture_inverse,
        "effectiveProcedureReviewCaseCount": len(preserved_case_rows) - len(old_held_ids) + len(fixture_values),
        "effectiveProcedureReviewEventCount": case_bindings["eventCount"] - old_held_event_count + fixture_event_count,
        "scope": "Four synthetic conditional fixtures supersede only the two incomplete anatomy records for authored-procedure review coverage; all other preserved Return234 cases remain byte-exact and in scope.",
        "runtimeOrCampaignEvidence": False,
    }
    write(candidate_package / "CASE_COVERAGE.json", coverage)
    coverage_ref = bind(candidate_package / "CASE_COVERAGE.json")

    evidence = {
        "id": "PSYCHIC-SCREAM-ACCEPTED-EVIDENCE-BINDINGS-296",
        "currentCatalog": bind(CATALOG, catalog_raw),
        "sourceProcedure": {"archive": return_ref, "member": "procedures/psychic-scream.json", "bytes": len(encode(source_procedure)), "sha256": sha(encode(source_procedure))},
        "return234Receipt": bind(RETURN234_RECEIPT),
        "closureDelta294": bind(DELTA294),
        "acceptedFixtureCorrection296": bind(DELTA296),
        "acceptedFixtureCorrectionAudit296": bind(DELTA296_AUDIT),
        "acceptedContract296": bind(DELTA296_CONTRACT),
        "currentAuthorityBeforeApplication": {"index": bind(INDEX, index_raw), "queue": bind(QUEUE0), "handoff": bind(HANDOFF0), "pendingAudit": bind(PENDING0), "interfaceRegistry": bind(REGISTRY)},
        "authority": BEFORE,
        "baseCommit": current_head,
        "workingTreeSnapshot": "Uncommitted authority snapshot; base commit recorded separately.",
        "acceptedRevision": REVISION,
        "retainedQualifications": QUALIFICATIONS,
    }
    write(candidate_package / "EVIDENCE_BINDINGS.json", evidence)
    evidence_ref = bind(candidate_package / "EVIDENCE_BINDINGS.json")

    procedure_content = (
        "Wizard/Enchantment: " + procedure["localProcedure"]["enchantment"] + "\n\n"
        "Mage/Evocation: " + procedure["localProcedure"]["evocation"] + "\n\n"
        "Shared resolution: " + procedure["localProcedure"]["resolution"] + "\n\n"
        "Selection/targeting: " + procedure["localProcedure"]["selection"] + " " + procedure["localProcedure"]["targeting"] + "\n\n"
        "Accepted review revision: " + REVISION + " revision296. Actual target source qualifications remain."
    )
    procedure_record = {
        "id": "PF182-STATIC-PSYCHIC-SCREAM-296",
        "spellId": ID,
        "status": "director-accepted static authored procedure; applied to authored review index; runtime disabled",
        "accepted": True,
        "applied": True,
        "procedureContent": procedure_content,
        "structuredProcedure": procedure["localProcedure"],
        "acceptedRevision": procedure["acceptedReviewRevision"],
        "nativeCardUnchanged": procedure["nativeCardAndAccessUnchanged"],
        "nativeBookBindingsUnchanged": procedure["nativeBookBindingsUnchanged"],
        "procedureSourceArchiveMember": {"archive": return_ref, "member": "procedures/psychic-scream.json"},
        "caseCoverageFile": "CASE_COVERAGE.json",
        "evidenceBindingsFile": "EVIDENCE_BINDINGS.json",
        "closedBlockerIds": [BLOCKER],
        "retainedQualificationIds": retained,
        "retainedQualifications": QUALIFICATIONS,
        "runtimeSelectionEnabled": False,
    }
    model = {
        "schemaVersion": 1,
        "moduleId": "rank9psychicscream-reviewed-296",
        "status": "ONE_EXACT_STATIC_AUTHORED_PROCEDURE_ACCEPTED_AND_APPLIED_RUNTIME_DISABLED",
        "scope": "Psychic Scream / PF182-B01 only; accepted bounded synthetic anatomy/lifecycle fixtures for authored procedure review. Actual-target source requirements remain.",
        "acceptedIds": [ID],
        "excludedPendingIds": sorted(live0 - {ID}),
        "unresolvedQualifications": {ID: QUALIFICATIONS},
        "sharedRequirements": {"scope": "No global/shared rule changes; native catalog unchanged; runtime selection disabled.", "runtimeSelectionEnabled": False},
        "spells": [{
            "id": ID,
            "name": NAME,
            "position": 0,
            "procedure": {
                "id": procedure_record["id"],
                "spellId": ID,
                "status": procedure_record["status"],
                "accepted": True,
                "applied": True,
                "procedureContent": procedure_content,
                "procedureRecordFile": "PROCEDURE_RECORD.json",
                "nativeCardUnchanged": procedure_record["nativeCardUnchanged"],
                "acceptedRevision": procedure_record["acceptedRevision"],
                "retainedQualifications": QUALIFICATIONS,
                "closedBlockerIds": [BLOCKER],
                "retainedHoldIds": retained,
                "caseCoverageFile": "CASE_COVERAGE.json",
                "evidenceBindingsFile": "EVIDENCE_BINDINGS.json",
                "directorDecisionId": decision_id,
            },
            "directorProcedureRecord": procedure_record,
            "previousProcedureRecord": source_procedure,
            "nativeCardUnchanged": procedure_record["nativeCardUnchanged"],
            "caseIds": [row["id"] for row in preserved_case_rows] + [fixture["id"] for fixture in fixture_values],
            "retainedHoldIds": retained,
            "runtimeSelectionEnabled": False,
        }],
        "sourceProcedureArchive": return_ref,
        "closureDelta294": bind(DELTA294),
        "acceptedFixtureCorrection296": bind(DELTA296),
        "directorDecision": decision_ref,
        "acceptanceReceipt": acceptance_ref,
        "returnReceipt": return_receipt_ref,
        "caseCoverage": coverage_ref,
        "evidenceBindings": evidence_ref,
        "runtimeSelectionEnabled": False,
        "runtimeTestsExecuted": False,
        "implementationApproved": False,
        "humanPlaytested": False,
        "balanceApproved": False,
        "cosmologyModified": False,
        "domainClosure": False,
        "releaseApproved": False,
    }
    write(candidate_package / "MODEL.json", model)
    model_ref = bind(candidate_package / "MODEL.json")
    manuscript = (
        "# Psychic Scream — accepted static authored procedure 296\n\n"
        "GPT accepted Psychic Scream / PF182-B01 under the bounded synthetic anatomy/lifecycle review revision. This acceptance closes only the authored-procedure review blocker. The native spell catalog remains blocked and runtime selection remains disabled.\n\n"
        "## Accepted conditional review route\n\n"
        "Four explicitly synthetic conditional anatomy fixtures cover positive final death with a destructible head, a headless body, enumerated multihead outcomes, and a changed-form terminal body. They are authored review fixtures, not creature source facts, observed play, or campaign history. The two incomplete historical anatomy records remain preserved but are superseded for review coverage.\n\n"
        "The death fixture commits the paid 26 RP Wizard/Enchantment cast at0.2, resolves the stipulated INT save at0.3, and applies all fourteen conditional d6 inputs at0.31. HP7/maxHP70 and damage84 produce overflow77, meeting the maximum-HP Instant Death threshold. The head consequence follows at0.32. The changed-form event remains at0.1 and uses an explicit fixture-only no-reversion rule. All 17 events replay forward and fully backward.\n\n"
        "## Retained qualifications\n\n" + "\n".join("- " + item for item in QUALIFICATIONS) + "\n"
    )
    MANUSCRIPT.parent.mkdir(parents=True, exist_ok=True)
    MANUSCRIPT.write_text(manuscript, encoding="utf-8", newline="\n")
    manuscript_ref = bind(MANUSCRIPT)
    package_manifest_path = candidate_package / "CANDIDATE_PACKAGE_MANIFEST.json"
    package_manifest = {"id": "PSYCHIC-SCREAM-PACKAGE-MANIFEST-296", "recordedAtUtc": stamp, "directorDecision": decision_ref, "acceptedFixtureCorrection": bind(DELTA296), "files": []}
    for path in sorted(item for item in candidate_package.rglob("*") if item.is_file() and item != package_manifest_path):
        package_manifest["files"].append({"path": (PKG_REL / path.relative_to(candidate_package)).as_posix(), "bytes": path.stat().st_size, "sha256": sha(path.read_bytes())})
    write(package_manifest_path, package_manifest)
    package_manifest_ref = bind(package_manifest_path)

    index1 = copy.deepcopy(index0)
    entry1 = copy.deepcopy(entry0)
    entry1.update({
        "authoredStatus": "reviewed-authored-operational-playtest",
        "procedureFile": "../spell_candidates/rank9psychicscream_reviewed_296/MODEL.json",
        "procedurePointer": "/spells/0/procedure",
        "wholeCardPointer": "/spells/0",
        "sourceStatus": entry0["sourceStatus"],
        "wholeCardIdField": "id",
        "sourceCatalogWholeCardPointer": entry0["wholeCardPointer"],
        "procedureTextPointer": "/spells/0/procedure/procedureContent",
        "directorProcedureRecordPointer": "/spells/0/directorProcedureRecord",
        "sharedRulesPointer": "/sharedRequirements",
        "spellLocalRequirementsPointer": "/spells/0/procedure",
        "manuscript": "../../../docs/spells/candidates/PSYCHIC_SCREAM_REVIEWED_296.md",
        "reviewId": acceptance_id,
        "runtimeSelectionEnabled": False,
        "historicalCandidateLabelsPreserved": True,
        "completeEvidenceRoot": PKG_REL.as_posix(),
        "completeEnvelopeBinding": model_ref,
        "caseEvidenceBindings": coverage_ref,
        "sourceArchiveBinding": return_ref,
        "candidatePackageManifestBinding": package_manifest_ref,
        "procedureSourceBinding": decision_ref,
        "acceptedFixtureCorrectionBinding": bind(DELTA296),
        "authoredAcceptanceReceipt": acceptance_ref,
        "authoredApplicationReceipt": application_id + ".json",
        "directorReturnReceipt": return_receipt_ref,
        "accepted": True,
        "applied": True,
        "closedBlockerIds": [BLOCKER],
        "retainedQualifications": QUALIFICATIONS,
        "retainedHoldIds": retained,
        "acceptedReviewRevision": REVISION,
    })
    target_i = next(i for i, row in enumerate(index1["entries"]) if row["id"] == ID)
    index1["entries"][target_i] = entry1
    assert not any(ID in row.get("acceptedIds", []) for row in index1["additionalStandaloneEnvelopes"])
    envelope = {
        "file": "../spell_candidates/rank9psychicscream_reviewed_296/MODEL.json",
        "binding": model_ref,
        "reviewId": acceptance_id,
        "acceptedIds": [ID],
        "unacceptedIds": [],
        "excludedPendingIds": sorted(live0 - {ID}),
        "authority": acceptance_ref,
        "applicationReceipt": application_id + ".json",
        "directorDecision": decision_ref,
        "sourceArchive": return_ref,
        "caseCoverageBinding": coverage_ref,
        "candidatePackageManifestBinding": package_manifest_ref,
        "closureDelta294": bind(DELTA294),
        "acceptedFixtureCorrection296": bind(DELTA296),
        "scope": "ONE_EXACT_STATIC_AUTHORED_PROCEDURE_ACCEPTED_AND_APPLIED_RUNTIME_DISABLED",
    }
    index1["additionalStandaloneEnvelopes"].append(envelope)
    index1["authoredCounts"] = {"reviewed": 820, "pending": 28}
    index1["representationCounts"]["completeReviewedStandaloneProcedures"] = 544
    live1 = {row["id"] for row in index1["entries"] if row["authoredStatus"] == "pending-authored-procedure"}
    assert live1 == live0 - {ID} and len(live1) == 28 and NEXT_IDS[0] in live1 and "final-word" in live1

    backup_path = A / "authored_review_index.before_psychic_scream_296.json"
    assert not backup_path.exists()
    backup_path.write_bytes(index_raw)
    write(INDEX, index1)
    index_core_ref = bind(INDEX)

    application_path = A / "PSYCHIC_SCREAM_APPLICATION_296.json"
    application = {
        "id": application_id,
        "recordedAtUtc": stamp,
        "status": "APPLIED_ONE_EXACT_DIRECTOR_ACCEPTED_AUTHORED_PROCEDURE",
        "acceptedIds": [ID],
        "appliedIds": [ID],
        "closedBlockerIds": [BLOCKER],
        "directorDecision": decision_ref,
        "acceptance": acceptance_ref,
        "directorReturnReceipt": return_receipt_ref,
        "acceptedArchive": bind(DELTA296),
        "closureDelta294": bind(DELTA294),
        "candidateEnvelope": model_ref,
        "candidatePackageManifest": package_manifest_ref,
        "caseCoverage": coverage_ref,
        "evidenceBindings": evidence_ref,
        "manuscript": manuscript_ref,
        "indexBefore": bind(backup_path, index_raw),
        "indexAfterCoreUpdate": index_core_ref,
        "countsBefore": BEFORE,
        "countsAfter": AFTER,
        "completeReviewedStandaloneProcedures": {"before": 543, "after": 544},
        "scopedInterfaces": 173,
        "catalogByteExact": CATALOG.read_bytes() == catalog_raw,
        "sourceStatusPreservedAsBlocked": True,
        "runtimeSelectionEnabled": False,
        "runtimeTestsExecuted": False,
        "implementationApproved": False,
        "humanPlaytested": False,
        "balanceApproved": False,
        "cosmologyModified": False,
        "domainClosure": False,
        "releaseApproved": False,
        "retainedQualificationIds": retained,
    }
    write(application_path, application)
    application_ref = bind(application_path)
    entry1["authoredApplicationReceipt"] = application_ref
    index1["entries"][target_i] = entry1
    index1["additionalStandaloneEnvelopes"][-1]["applicationReceipt"] = application_path.relative_to(ROOT).as_posix()
    write(INDEX, index1)
    index_ref = bind(INDEX)

    operations_path = A / "PSYCHIC_SCREAM_INDEX_OPERATIONS_296.json"
    operations = {
        "id": "PSYCHIC-SCREAM-INDEX-OPERATIONS-296",
        "recordedAtUtc": stamp,
        "before": bind(backup_path, index_raw),
        "after": index_ref,
        "operations": [
            {"op": "update-entry", "id": ID, "before": entry0, "after": entry1},
            {"op": "append-standalone-envelope", "acceptedIds": [ID]},
            {"op": "update-authored-counts", "before": {"reviewed": 819, "pending": 29}, "after": {"reviewed": 820, "pending": 28}},
            {"op": "increment-complete-procedure-count", "before": 543, "after": 544},
        ],
        "inverse": [
            {"op": "restore-entry", "id": ID, "value": entry0},
            {"op": "remove-appended-standalone-envelope", "acceptedIds": [ID]},
            {"op": "restore-authored-counts", "value": {"reviewed": 819, "pending": 29}},
            {"op": "restore-complete-procedure-count", "value": 543},
            {"op": "restore-byte-exact-index-from-backup", "backup": bind(backup_path, index_raw)},
        ],
        "catalogByteExact": CATALOG.read_bytes() == catalog_raw,
        "sourceStatusPreservedAsBlocked": True,
        "runtimeSelectionEnabled": False,
        "inverseRestoresExactIndex": backup_path.read_bytes() == index_raw,
    }
    write(operations_path, operations)

    pending_ids1 = sorted(live1)
    groups1 = clean_rows(pending0.get("groups", []))
    priority1 = [item for item in pending0.get("nextBlockerPriority", []) if item != ID]
    pending1 = copy.deepcopy(pending0)
    pending1.update({
        "id": "CURRENT28_PENDING_IDENTITY_AUDIT_296",
        "recordedAtUtc": stamp,
        "status": "PASS_EXACT_CURRENT_INDEX_PENDING_SET_AFTER_PSYCHIC_SCREAM_APPLICATION_296",
        "authority": AFTER,
        "indexBinding": index_ref,
        "catalogBinding": bind(CATALOG, catalog_raw),
        "pendingCount": 28,
        "pendingIds": pending_ids1,
        "groups": groups1,
        "heldIds": sorted(set(pending0.get("heldIds", [])) - {ID}),
        "acceptedIds": sorted(set(pending0.get("acceptedIds", [])) | {ID}),
        "appliedIds": sorted(set(pending0.get("appliedIds", [])) | {ID}),
        "applicationReceipt": application_ref,
        "acceptanceReceipt": acceptance_ref,
        "directorDecision": decision_ref,
        "closedBlockerIdsThisStep": sorted(set(pending0.get("closedBlockerIdsThisStep", [])) | {BLOCKER}),
        "lastDirectorReturn": {"decisionId": decision_id, "acceptedIds": [ID], "appliedIds": [ID], "heldIds": [], "closedBlockerIds": [BLOCKER], "acceptedArchive": bind(DELTA296)},
        "nextBlockerPriority": priority1,
        "preparedNextGroup": {"group": NEXT_GROUP, "pendingIds": NEXT_IDS, "freshPacketRequiredForCurrentAuthority": True, "blocker": "PF182-B02", "directorRequirement": package_baseline["return234Decision"].get("minimumMissingWitness", "Bind a currently operational genuine full-extra-turn grant, complete actor acquisition history, and the required inserted-turn branches.")},
        "remainingPendingCount": 28,
        "pendingIdentityCount": 28,
        "nextGroup": NEXT_GROUP,
        "nextPendingIds": NEXT_IDS,
        "nextPendingCount": 2,
    })
    pending_path = A / "CURRENT28_PENDING_IDENTITY_AUDIT_296.json"
    write(pending_path, pending1)
    pending_ref = bind(pending_path)

    queue1 = copy.deepcopy(queue0)
    closure_priority = [x for x in queue0.get("recommendedClosurePriority", []) if x != ID]
    recommended_order = clean_order(queue0.get("recommendedClosureOrder", []))
    next_row = {"group": NEXT_GROUP, "pendingIds": NEXT_IDS, "pendingCount": 2, "status": "DIRECTOR_NEXT_IDENTITY_AFTER_PSYCHIC_SCREAM_296", "freshPacketRequiredForCurrentAuthority": True, "blockerByIdentity": {"mass-phantom-killer": "PF182-B02", "weird": "PF182-B02"}, "directorRequirement": "Bind a currently operational genuine full-extra-turn grant with activation/cost/limits/timing, lawful acquisition and actor history; use it in both held spell branches while preserving clocks, saves, resource and Ready rules."}
    next_three = ["mass-phantom-killer", "weird", "final-word"]
    closure_priority = next_three + [x for x in closure_priority if x not in next_three]
    queue1.update({
        "id": "SPELL-REVIEW-QUEUE-296",
        "recordedAtUtc": stamp,
        "supersedesQueue": bind(QUEUE0),
        "parentQueue": bind(QUEUE0),
        "currentAuthority": AFTER,
        "currentIndexBinding": index_ref,
        "pendingIdentityAudit": pending_ref,
        "pendingCount": 28,
        "nextGroup": NEXT_GROUP,
        "next": next_row,
        "nextPendingIds": NEXT_IDS,
        "nextPendingCount": 2,
        "currentPendingGroups": groups1,
        "nextSuggestedGroups": [next_row],
        "recommendedClosurePriority": closure_priority,
        "recommendedClosureOrder": recommended_order,
        "lastReviewedBatch": {"group": NEXT_GROUP, "acceptedIds": [ID], "appliedIds": [], "heldIds": [], "closedBlockerIds": [BLOCKER]},
        "justAppliedBatch": {"reviewId": acceptance_id, "applicationId": application_id, "ids": [ID], "count": 1, "applicationReceipt": application_ref, "directorDecision": decision_ref},
        "packetStatus": "PSYCHIC_SCREAM_PF182_B01_ACCEPTED_AND_APPLIED; NEXT_MASS_PHANTOM_KILLER_PF182_B02",
        "currentAcceptedPacket": {"acceptedArchive": bind(DELTA296), "directorDecision": decision_ref, "acceptance": acceptance_ref, "application": application_ref, "closureDelta294": bind(DELTA294)},
        "currentDirectorPosition": {"stage": "PSYCHIC_SCREAM_ACCEPTED_APPLIED_PF182_B01; MASS_PHANTOM_KILLER_NEXT", "acceptedIds": [ID], "appliedIds": [ID], "heldIds": sorted(live1), "blockers": {"mass-phantom-killer": ["PF182-B02"], "weird": ["PF182-B02"]}, "nextPendingGroup": next_row},
        "nextPriorityContext": {"identity": "mass-phantom-killer", "blocker": "PF182-B02", "requirement": next_row["directorRequirement"]},
        "currentPreparation": next_row,
        "githubChanges": False,
        "canonicalRuntimeApplicationPerformed": False,
        "afterNextAcceptedAppliedForecast": {"remainingIdentities": 27},
    })
    queue_path = A / "CURRENT_SPELL_QUEUE_296.json"
    write(queue_path, queue1)
    queue_ref = bind(queue_path)

    handoff1 = copy.deepcopy(handoff0)
    handoff1.update({
        "id": "CURRENT-HANDOFF-296",
        "recordedAtUtc": stamp,
        "supersedes": handoff0["id"],
        "status": "PSYCHIC_SCREAM_APPLIED_NEXT_MASS_PHANTOM_KILLER_820_28",
        "authority": AFTER,
        "currentAuthority": AFTER,
        "indexBinding": index_ref,
        "queueBinding": queue_ref,
        "queue": queue_path.relative_to(ROOT).as_posix(),
        "pendingIdentityAudit": pending_ref,
        "appliedThisStep": True,
        "acceptedThisStep": [ID],
        "appliedThisStepRecord": {"identity": ID, "application": application_path.relative_to(ROOT).as_posix(), "applicationBinding": application_ref, "closedBlockerIds": [BLOCKER]},
        "nextStep": next_row,
        "nextGroup": NEXT_GROUP,
        "nextPendingCount": 2,
        "nextPendingIds": NEXT_IDS,
        "currentBlocker": {"identity": NEXT_IDS[0], "group": NEXT_GROUP, "blockerId": "PF182-B02"},
        "directorConnectionStatus": "GPT explicitly accepted Psychic Scream / PF182-B01 only; next is Mass Phantom Killer / PF182-B02, followed by Weird and Final Word.",
        "githubChanges": False,
        "latestBatch": {"accepted": [ID], "applied": [ID], "closed": [BLOCKER]},
        "currentPreparation": next_row,
        "canonicalRuntimeApplicationPerformed": False,
        "nextStepText": next_row["directorRequirement"],
    })
    handoff_path = A / "CURRENT_HANDOFF_296.json"
    write(handoff_path, handoff1)
    handoff_ref = bind(handoff_path)

    validation_path = A / "PSYCHIC_SCREAM_APPLICATION_VALIDATION_296.json"
    checks = [
        ("Director accepted only Psychic Scream / PF182-B01 under revision296", decision["accepted"] and decision["acceptedRevision"]["id"] == REVISION and decision["noOtherIdentityAcceptedOrApplied"]),
        ("Accepted archive SHA and eight-member allowlist are exact", bind(DELTA296)["sha256"] == "d6006fd3bf3999603ad55e090a3e53b39d151a35747938ad052db7bc527e23ac" and len(zipfile.ZipFile(DELTA296).namelist()) == 8),
        ("Four conditional fixtures and 17 new events remain synthetic and replayable", len(fixture_values) == 4 and fixture_event_count == 17 and all(f["replayAudit"]["fullReverseTraversalRestoresInitial"] for f in fixture_values)),
        ("Both historical anatomy records remain bound and preserved but superseded for review coverage", len(old_held_ids) == 2 and all(row["id"] in old_held_ids for row in preserved_case_rows if row["id"] in old_held_ids)),
        ("PF181-H03 and all retained boundary qualifications remain", "PF181-H03" in retained and len(retained) == 12),
        ("Only Psychic Scream leaves the pending index; pending set becomes 28", live1 == live0 - {ID} and len(live1) == 28),
        ("Authority advances exactly to 820/28/0 and 544/173", index1["authoredCounts"] == {"reviewed": 820, "pending": 28} and index1["representationCounts"]["completeReviewedStandaloneProcedures"] == 544 and AFTER["scopedInterfaces"] == 173),
        ("Native catalog stays byte-exact and sourceStatus remains blocked", CATALOG.read_bytes() == catalog_raw and index1["entries"][target_i]["sourceStatus"] == "blocked-pending-operational-review" and catalog0["spells"][395]["operational"] is None),
        ("Runtime and downstream gates remain disabled", model["runtimeSelectionEnabled"] is False and model["implementationApproved"] is False and model["releaseApproved"] is False),
        ("Next Director order is Mass Phantom Killer then Weird then Final Word", queue1["next"]["pendingIds"] == NEXT_IDS and closure_priority[:3] == next_three),
        ("Pending audit, queue, and handoff bind the final index and authority", pending1["indexBinding"]["sha256"] == index_ref["sha256"] and queue1["currentIndexBinding"]["sha256"] == index_ref["sha256"] and handoff1["indexBinding"]["sha256"] == index_ref["sha256"] and queue1["currentAuthority"] == handoff1["currentAuthority"] == pending1["authority"] == AFTER),
        ("Backup restores exact pre-application index bytes", backup_path.read_bytes() == index_raw),
    ]
    assert all(ok for _, ok in checks), [name for name, ok in checks if not ok]
    validation = {
        "id": "PSYCHIC-SCREAM-APPLICATION-VALIDATION-296",
        "recordedAtUtc": stamp,
        "status": "PASS",
        "checks": [{"check": name, "passed": bool(ok)} for name, ok in checks],
        "checkCount": len(checks),
        "failedChecks": 0,
        "acceptedIds": [ID],
        "appliedIds": [ID],
        "closedBlockerIds": [BLOCKER],
        "authority": AFTER,
        "index": index_ref,
        "application": application_ref,
        "acceptance": acceptance_ref,
        "pendingIdentityAudit": pending_ref,
        "queue": queue_ref,
        "handoff": handoff_ref,
        "indexOperations": bind(operations_path),
        "candidatePackage": model_ref,
        "candidatePackageManifest": package_manifest_ref,
        "catalogByteExact": True,
        "sourceStatusPreservedAsBlocked": True,
        "runtimeSelectionEnabled": False,
    }
    write(validation_path, validation)
    validation_ref = bind(validation_path)

    snapshot_path = A / "CURRENT_SPELL_REVIEW_SNAPSHOT_296.md"
    snapshot_path.write_text(
        "# Spell Review Snapshot — Psychic Scream Application 296\n\n"
        "Authority: **820 applied / 28 pending / 0 accepted-unapplied; 544 complete standalone procedures / 173 scoped interfaces.**\n\n"
        "Psychic Scream / PF182-B01 was accepted under the bounded synthetic anatomy/lifecycle contract and applied to the authored review index. PF181-H03 and all source-qualified actual-target requirements remain. The native spell catalog remains blocked and runtime selection is disabled.\n\n"
        "Next priority: **mass-phantom-killer / PF182-B02**, then **weird / PF182-B02**, followed by **final-word / DR217-B01**. The Director requires a genuine operational full-extra-turn grant, lawful acquisition and actor history for the shared two-spell review.\n\n"
        "Validation: " + validation_ref["path"] + " (" + validation_ref["sha256"] + ").\n",
        encoding="utf-8",
        newline="\n",
    )
    assert CATALOG.read_bytes() == catalog_raw and backup_path.read_bytes() == index_raw
    print(json.dumps({"status": "PASS", "acceptedAndApplied": ID, "authority": AFTER, "index": index_ref, "package": model_ref, "application": application_ref, "validation": validation_ref, "pendingAudit": pending_ref, "queue": queue_ref, "handoff": handoff_ref, "next": next_row}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
