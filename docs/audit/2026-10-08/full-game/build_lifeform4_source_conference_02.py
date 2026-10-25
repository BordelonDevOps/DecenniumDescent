from __future__ import annotations

import copy
import hashlib
import json
import zipfile
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
FULL = ROOT / "docs/audit/2026-10-08/full-game"
AUDIT = FULL / "director-spell-review-129"
BASE_CANDIDATE = ROOT / "DescentReviewChanges/ReviewBible/data/director/spell_review/rank8_life_form_4_source_conference_01.json"
CANDIDATE = ROOT / "DescentReviewChanges/ReviewBible/data/director/spell_review/rank8_life_form_4_source_conference_02.json"
INDEX = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json"
CATALOG = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json"
REGISTRY = ROOT / "DescentReviewChanges/ReviewBible/data/director/spell_review/accepted_interface_registry_06.json"
QUEUE_150 = AUDIT / "CURRENT_SPELL_QUEUE_150.json"
PENDING_150 = AUDIT / "CURRENT139_PENDING_IDENTITY_AUDIT_150.json"
HANDOFF_150 = AUDIT / "CURRENT_HANDOFF_150.json"
QUEUE_151 = AUDIT / "CURRENT_SPELL_QUEUE_151.json"
HANDOFF_151 = AUDIT / "CURRENT_HANDOFF_151.json"
MEMORY_ROOT = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_candidates/rank8memorycontrol4_reviewed_150"
MEMORY_RECEIPT = AUDIT / "MEMORY_CONTROL4_EXACT_ACCEPTANCE_150.json"
MEMORY_APPLICATION = AUDIT / "MEMORY_CONTROL4_APPLICATION_150.json"
MEMORY_DECISION = AUDIT / "GPT_DIRECTOR_DECISION_MEMORY_CONTROL4_150.json"
MEMORY_DELIVERY = AUDIT / "rank8memorycontrol4_return150_received/DIRECTOR_RETURN_DELIVERY.json"
OUT = FULL / "rank8-life-form4-source-conference-02"
ARCHIVE = FULL / "DD_Rank8_Life_Form_4_Source_Conference_02.zip"
CHECK = FULL / "RANK8_LIFE_FORM_4_SOURCE_CONFERENCE_02_CHECK.json"
PREPARATION = FULL / "RANK8_LIFE_FORM_4_SOURCE_CONFERENCE_02_PREPARATION.json"
REQUEST = FULL / "RANK8_LIFE_FORM_4_SOURCE_CONFERENCE_02_REQUEST.txt"
IDS = ["animal-shapes", "clone", "flesh-to-grave", "perfect-form"]


def read(path: Path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def encoded(value) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8")


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def binding(path: Path) -> dict:
    raw = path.read_bytes()
    return {"path": path.relative_to(ROOT).as_posix(), "bytes": len(raw), "sha256": sha(raw)}


def write(path: Path, value) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(encoded(value))


def main() -> None:
    outputs = [CANDIDATE, OUT, ARCHIVE, CHECK, PREPARATION, REQUEST, QUEUE_151, HANDOFF_151]
    existing = [str(path) for path in outputs if path.exists()]
    assert not existing, f"Conference02 output already exists; inspect before retry: {existing}"

    old = read(BASE_CANDIDATE)
    index = read(INDEX)
    catalog = read(CATALOG)
    registry = read(REGISTRY)
    queue = read(QUEUE_150)
    pending = read(PENDING_150)
    handoff = read(HANDOFF_150)
    assert index["authoredCounts"] == {"reviewed": 709, "pending": 139}
    assert index["representationCounts"]["completeReviewedStandaloneProcedures"] == 433
    assert queue["currentAuthority"]["reviewedApplied"] == 709 and queue["currentAuthority"]["pending"] == 139
    assert pending["pendingCount"] == 139 and pending["indexBinding"]["sha256"] == binding(INDEX)["sha256"]
    assert handoff["nextGroup"] == "rank8-life-form4"
    target_group = queue["currentPendingGroups"][0]
    assert target_group["group"] == "rank8-life-form4" and target_group["pendingIds"] == IDS
    rows = {entry["id"]: entry for entry in index["entries"]}
    assert set(IDS) <= set(pending["pendingIds"])
    assert all(rows[identity]["authoredStatus"] == "pending-authored-procedure" for identity in IDS)

    memory_model_path = MEMORY_ROOT / "MODEL.json"
    memory_model = read(memory_model_path)
    memory_receipt = read(MEMORY_RECEIPT)
    memory_application = read(MEMORY_APPLICATION)
    memory_decision = read(MEMORY_DECISION)
    memory_delivery = read(MEMORY_DELIVERY)
    memory_procedures = {spell["id"]: spell for spell in memory_model["spells"]}
    memory_ids = ["erase-mind", "feeblemind", "mass-dominate", "mind-ravel"]
    assert memory_receipt["acceptedIds"] == memory_ids and memory_receipt["countsAfter"] == {"reviewed": 709, "pending": 139, "acceptedUnapplied": 0}
    assert memory_application["acceptedIds"] == memory_ids and memory_application["counts"]["after"] == {"reviewed": 709, "pending": 139, "acceptedUnapplied": 0}
    assert memory_decision["accepted"] is True and memory_decision["acceptedIds"] == memory_ids
    assert memory_delivery["accepted"] is True and memory_delivery["applied"] is False and memory_delivery["acceptedIds"] == memory_ids
    memory_model_binding = binding(memory_model_path)
    assert all(rows[identity]["authoredStatus"] == "reviewed-authored-operational-playtest" for identity in memory_ids)
    assert all(rows[identity]["completeEnvelopeBinding"]["sha256"] == memory_model_binding["sha256"] for identity in memory_ids)

    now = datetime.now(timezone.utc).isoformat()
    candidate = copy.deepcopy(old)
    candidate.update({
        "id": "RANK8-LIFE-FORM4-SOURCE-CONFERENCE02",
        "recordedAtUtc": now,
        "status": "SOURCE_CONFERENCE_PREPARED_UNSENT",
        "priorConferenceSupersededBy": "This packet is freshly bound to authority 709/139; Conference01 remains preserved as a historical 525/323 source packet.",
        "currentAuthority": {
            "reviewedApplied": 709, "pending": 139, "acceptedUnapplied": 0,
            "completeReviewedStandaloneProcedures": 433,
            "index": binding(INDEX), "catalog": binding(CATALOG),
            "currentQueue": binding(QUEUE_150), "pendingIdentityAudit": binding(PENDING_150),
            "priorHandoff": binding(HANDOFF_150),
        },
        "countsUnchanged": copy.deepcopy(index["authoredCounts"]),
        "gptCommunication": "Fresh Life/Form4 source conference for current authority 709 reviewed / 139 pending. Memory/Control4 Return150 is accepted and applied; preserve its four exact procedures as reviewed comparisons. Do not reopen any completed feat or spell cohort.",
    })

    for record in candidate["records"]:
        identity = record["spellId"]
        assert identity in IDS
        native = next(spell for spell in catalog["spells"] if spell["id"] == identity)
        assert record["completeCurrentCatalogSourceAndAccess"] == native
        record["currentIndexEntry"] = copy.deepcopy(rows[identity])

    superseded = []
    for old_group in candidate["pendingComparisonsNotAuthority"]:
        identities = old_group["identities"]
        assert all(rows[identity]["authoredStatus"] == "reviewed-authored-operational-playtest" for identity in identities)
        superseded.append({
            **copy.deepcopy(old_group),
            "currentDisposition": "SUPERSEDED_BY_LATER_REVIEW_AND_APPLICATION",
            "currentReviewedIds": identities,
            "qualification": "The 709/139 index shows every identity in this former pending comparison is now reviewed. These historical packet bytes are preserved and are not current pending authorities.",
        })
    candidate["historicalPendingComparisonsNowReviewed"] = superseded
    candidate["pendingComparisonsNotAuthority"] = []

    memory_comparisons = []
    for i, identity in enumerate(memory_ids):
        spell = memory_procedures[identity]
        memory_comparisons.append({
            "spellId": identity,
            "source": memory_model_binding,
            "pointer": f"/spells/{i}",
            "completeCurrentCardAndProcedure": copy.deepcopy(spell),
            "completeSharedRules": copy.deepcopy(memory_model["sharedRules"]),
            "currentIndexEntry": copy.deepcopy(rows[identity]),
            "exactAcceptance": binding(MEMORY_RECEIPT),
            "applicationReceipt": binding(MEMORY_APPLICATION),
            "directorDecision": binding(MEMORY_DECISION),
            "deliveryRecord": binding(MEMORY_DELIVERY),
            "sealedDirectorArchive": memory_receipt["directorReturn"],
            "qualification": "Exact authored procedures accepted and applied with all retained holds. This comparison grants no runtime, human-play, balance, source, cosmology or release approval.",
        })
    candidate["recentlyAppliedMemoryControl4Comparisons"] = memory_comparisons

    source_paths = {row["path"] for row in old["sourceBindings"]}
    source_paths.update({
        binding(QUEUE_150)["path"], binding(PENDING_150)["path"], binding(HANDOFF_150)["path"],
        binding(memory_model_path)["path"], binding(MEMORY_ROOT / "CANDIDATE_PACKAGE_MANIFEST.json")["path"],
        binding(MEMORY_RECEIPT)["path"], binding(MEMORY_APPLICATION)["path"],
        binding(MEMORY_DECISION)["path"], binding(MEMORY_DELIVERY)["path"],
    })
    source_rows = []
    for relative in sorted(source_paths):
        path = ROOT / Path(*relative.split("/"))
        assert path.is_file(), f"Bound source is missing: {relative}"
        source_rows.append(binding(path))
    candidate["sourceBindings"] = source_rows

    checks = []
    def ck(name: str, passed: bool) -> None:
        checks.append({"check": name, "passed": bool(passed)})
        assert passed, name

    ck("Current authored authority is 709 reviewed and 139 pending", index["authoredCounts"] == {"reviewed": 709, "pending": 139})
    ck("Complete reviewed procedure count is 433", index["representationCounts"]["completeReviewedStandaloneProcedures"] == 433)
    ck("Pending identity audit exactly matches current index", set(pending["pendingIds"]) == {e["id"] for e in index["entries"] if e["authoredStatus"] == "pending-authored-procedure"})
    ck("Life/Form4 is the exact next group", target_group["pendingIds"] == IDS)
    ck("All four Life/Form4 identities remain pending", all(rows[identity]["authoredStatus"] == "pending-authored-procedure" for identity in IDS))
    ck("All four native catalog/access records remain byte-source bound", all(next(s for s in catalog["spells"] if s["id"] == identity) == next(r for r in candidate["records"] if r["spellId"] == identity)["completeCurrentCatalogSourceAndAccess"] for identity in IDS))
    ck("All former pending comparison groups are now reviewed", all(rows[identity]["authoredStatus"] == "reviewed-authored-operational-playtest" for group in superseded for identity in group["identities"]))
    ck("Memory/Control4 exact acceptance is for four IDs and applied at 709/139", memory_receipt["acceptedIds"] == memory_ids and memory_application["counts"]["after"] == {"reviewed": 709, "pending": 139, "acceptedUnapplied": 0})
    ck("173 accepted-interface entries remain available", len(registry["entries"]) == 173 and len(candidate["currentAcceptedInterfaceComparisons"]) == 19)
    ck("24 unique conference questions remain unselected", len(candidate["questions"]) == 24 and len({q["id"] for q in candidate["questions"]}) == 24 and all(q["decisionSelected"] is False for q in candidate["questions"]))
    ck("All four target identities are covered by conference questions", set().union(*(set(q["spellIds"]) for q in candidate["questions"])) == set(IDS))
    ck("No proposal or runtime approval is adopted", candidate["newRuleAdoptions"] == 0 and candidate["runtimeTestsExecuted"] == 0 and candidate["humanPlaytests"] == 0)
    ck("Prior 58 source inputs are retained", len(old["sourceBindings"]) == 58)
    ck("All current and historical source bindings are unique", len(source_rows) == len({row["path"] for row in source_rows}))
    ck("Source catalog bytes remain unchanged", binding(CATALOG)["sha256"] == "773fb0b3b0fdb501858ded33c02d90dc4db3009bd1b9f7112c244d998218f05b")

    OUT.mkdir(parents=True)
    frozen = []
    for row in source_rows:
        source = ROOT / Path(*row["path"].split("/"))
        destination = OUT / "sources" / Path(*row["path"].split("/"))
        destination.parent.mkdir(parents=True, exist_ok=True)
        raw = source.read_bytes()
        assert len(raw) == row["bytes"] and sha(raw) == row["sha256"]
        destination.write_bytes(raw)
        assert destination.read_bytes() == raw
        frozen.append({**row, "frozenCopy": destination.relative_to(ROOT).as_posix()})

    candidate_bytes = encoded(candidate)
    CANDIDATE.parent.mkdir(parents=True, exist_ok=True)
    CANDIDATE.write_bytes(candidate_bytes)
    candidate_binding = binding(CANDIDATE)
    readme = (
        "Life/Form4 source conference02 is freshly bound to 709 reviewed / 139 pending.\n"
        "It covers Animal Shapes, Clone, Flesh to Grave, and Perfect Form with 24 unselected questions.\n"
        "Conference01 is retained only as historical 525/323 source material. Memory/Control4 Return150 is accepted and applied; its four exact procedures are included as reviewed comparisons.\n"
        "No new rule, runtime behavior, human-play result, balance, cosmology, or release approval is adopted.\n"
    )
    (OUT / "README.md").write_text(readme, encoding="utf-8", newline="\n")
    check_doc = {
        "candidate": candidate_binding,
        "status": "PASS",
        "checks": checks,
        "checkCount": len(checks),
        "failedChecks": 0,
        "sourceCount": len(source_rows),
        "sourceBindingsAllVerified": True,
        "sourceAuthority": {"reviewedApplied": 709, "pending": 139, "acceptedUnapplied": 0},
        "targetIds": IDS,
        "questions": 24,
        "historicalConference01Retained": True,
        "runtimeOrRuleApproval": False,
    }
    check_bytes = encoded(check_doc)
    CHECK.write_bytes(check_bytes)
    manifest = {
        "id": "RANK8-LIFE-FORM4-SOURCE-CONFERENCE02-MANIFEST",
        "candidate": candidate_binding,
        "sourceCount": len(source_rows),
        "frozenSources": frozen,
        "check": binding(CHECK),
        "sourceAuthority": candidate["currentAuthority"],
    }
    write(OUT / "MANIFEST.json", manifest)
    request_text = (
        f"Review {ARCHIVE.name}; source authority is 709 reviewed / 139 pending / 0 accepted-unapplied.\n"
        "This is the fresh Life/Form4 packet for Animal Shapes, Clone, Flesh to Grave, and Perfect Form (24 unselected questions). "
        "Use its exact current catalog, index, pending audit, application queue, prior handoff, accepted-interface entries and bound source passages. "
        "Conference01 is historical 525/323 material only. The former pending comparisons are now reviewed; Memory/Control4 Return150 is accepted and applied, and its four procedures are included as exact comparisons. "
        "Decide each authored form, lifecycle, return, score and fatal-Exhaustion choice; retain missing source, content, profile, cosmology, runtime, human-play, balance and release holds. "
        "Return per-question dispositions, exact accepted IDs, a complete authored procedure package and a sealed delivery record. Apply only the exact procedures accepted by the director. Do not reopen feat335 or completed spell cohorts.\n"
    )
    REQUEST.write_text(request_text, encoding="utf-8", newline="\n")
    with zipfile.ZipFile(ARCHIVE, "x", zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        archive.write(CANDIDATE, "CANDIDATE.json")
        archive.write(CHECK, "SOURCE_CHECK.json")
        archive.write(OUT / "MANIFEST.json", "MANIFEST.json")
        archive.write(OUT / "README.md", "README.md")
        for row in source_rows:
            archive.write(OUT / "sources" / Path(*row["path"].split("/")), "sources/" + row["path"])
    with zipfile.ZipFile(ARCHIVE) as archive:
        assert archive.testzip() is None
        assert len(archive.namelist()) == len(set(archive.namelist()))
        assert archive.read("CANDIDATE.json") == candidate_bytes
        for row in source_rows:
            raw = (OUT / "sources" / Path(*row["path"].split("/"))).read_bytes()
            assert archive.read("sources/" + row["path"]) == raw
    archive_binding = binding(ARCHIVE)
    preparation = {
        "id": "RANK8-LIFE-FORM4-SOURCE-CONFERENCE02-PREPARATION",
        "recordedAtUtc": now,
        "status": "PREPARED_UNSENT",
        "candidate": candidate_binding,
        "archive": archive_binding,
        "check": binding(CHECK),
        "manifest": binding(OUT / "MANIFEST.json"),
        "request": binding(REQUEST),
        "sourceCount": len(source_rows),
        "identityCount": 4,
        "questionCount": 24,
        "authority": candidate["currentAuthority"],
        "allArchiveMembersVerified": True,
        "newRuleAdoptions": 0,
    }
    write(PREPARATION, preparation)

    queue151 = copy.deepcopy(queue)
    queue151.update({"id": "SPELL-REVIEW-QUEUE-151", "recordedAtUtc": now, "packetStatus": "FRESH_LIFE_FORM4_PACKET02_PREPARED_UNSENT"})
    queue151["currentPendingGroups"][0]["candidate"] = candidate_binding
    queue151["currentPendingGroups"][0]["sourceArchive"] = archive_binding
    queue151["nextSuggestedGroups"] = queue151["currentPendingGroups"][:5]
    queue151["next"] = {"group": "rank8-life-form4", "pendingCount": 4, "archive": archive_binding, "candidate": candidate_binding, "freshPacketRequiredForCurrentAuthority": False}
    queue151["nextGroup"] = "rank8-life-form4"
    write(QUEUE_151, queue151)
    handoff151 = copy.deepcopy(handoff)
    handoff151.update({
        "id": "CURRENT-HANDOFF-151", "recordedAtUtc": now,
        "status": "RANK8_LIFE_FORM4_PACKET02_PREPARED_UNSENT",
        "nextGroup": "rank8-life-form4",
        "nextPreparedRequest": {"group": "rank8-life-form4", "candidate": candidate_binding, "archive": archive_binding, "pendingIds": IDS, "freshPacketRequiredForCurrentAuthority": False, "status": "prepared-unsent"},
        "resumePriority": "Submit the fresh Conference02 ZIP to Calibration review part 6. Apply only exact director-accepted IDs, then continue with the next current pending group.",
    })
    write(HANDOFF_151, handoff151)
    print(json.dumps({"status": "PREPARED_UNSENT", "authority": candidate["currentAuthority"], "ids": IDS, "questions": 24, "sourceCount": len(source_rows), "checksPassed": len(checks), "archive": archive_binding}, indent=2))


if __name__ == "__main__":
    main()
