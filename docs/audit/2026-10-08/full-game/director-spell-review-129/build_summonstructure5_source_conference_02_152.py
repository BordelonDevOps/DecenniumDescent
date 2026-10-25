from __future__ import annotations

import copy
import hashlib
import json
import zipfile
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[5]
FULL = ROOT / "docs/audit/2026-10-08/full-game"
AUDIT = FULL / "director-spell-review-129"
SPELL_REVIEW = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_playtests"
OLD_CANDIDATE = ROOT / "DescentReviewChanges/ReviewBible/data/director/spell_review/rank8_summon_structure_5_source_conference_01.json"
OLD_ARCHIVE = FULL / "DD_Rank8_Summon_Structure_5_Source_Conference_01.zip"
QUEUE_BEFORE = AUDIT / "CURRENT_SPELL_QUEUE_152.json"
HANDOFF_BEFORE = AUDIT / "CURRENT_HANDOFF_152.json"
PENDING = AUDIT / "CURRENT135_PENDING_IDENTITY_AUDIT_152.json"
QUEUE_AFTER = AUDIT / "CURRENT_SPELL_QUEUE_153.json"
HANDOFF_AFTER = AUDIT / "CURRENT_HANDOFF_153.json"
CANDIDATE = ROOT / "DescentReviewChanges/ReviewBible/data/director/spell_review/rank8_summon_structure_5_source_conference_02.json"
OUT = FULL / "rank8-summon-structure5-source-conference-02"
ARCHIVE = FULL / "DD_Rank8_Summon_Structure_5_Source_Conference_02.zip"
REQUEST = FULL / "RANK8_SUMMON_STRUCTURE_5_SOURCE_CONFERENCE_02_REQUEST.txt"
CHECK = FULL / "RANK8_SUMMON_STRUCTURE_5_SOURCE_CONFERENCE_02_CHECK.json"
PREPARATION = FULL / "RANK8_SUMMON_STRUCTURE_5_SOURCE_CONFERENCE_02_PREPARATION.json"
IDS = ["summon-greater-water-pet", "summon-archlich-shade", "faction-paragon", "conjure-sky-fortress", "shifting-fortress"]
LIFEFORM_DIR = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_candidates/rank8lifeform4_reviewed_151"
LIFEFORM_AUDIT = AUDIT


def read(path: Path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def encode(value) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8")


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def bind(path: Path) -> dict:
    raw = path.read_bytes()
    return {"path": path.relative_to(ROOT).as_posix(), "bytes": len(raw), "sha256": sha(raw)}


def write(path: Path, value) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(encode(value))


def main() -> None:
    outputs = [CANDIDATE, OUT, ARCHIVE, REQUEST, CHECK, PREPARATION, QUEUE_AFTER, HANDOFF_AFTER]
    assert not [str(p) for p in outputs if p.exists()], "Conference02 outputs already exist; inspect before retrying."
    old = read(OLD_CANDIDATE)
    old_prep = read(FULL / "RANK8_SUMMON_STRUCTURE_5_SOURCE_CONFERENCE_01_PREPARATION.json")
    old_check = read(FULL / "RANK8_SUMMON_STRUCTURE_5_SOURCE_CONFERENCE_01_CHECK.json")
    idx_path = SPELL_REVIEW / "authored_review_index.json"
    catalog_path = SPELL_REVIEW / "catalog.json"
    index = read(idx_path)
    catalog = read(catalog_path)
    queue = read(QUEUE_BEFORE)
    handoff = read(HANDOFF_BEFORE)
    pending = read(PENDING)
    registry_path = ROOT / "DescentReviewChanges/ReviewBible/data/director/spell_review/accepted_interface_registry_06.json"
    registry = read(registry_path)
    assert old_prep["status"] == "PREPARED_UNSENT" and old_check["failures"] == 0
    assert index["authoredCounts"] == {"reviewed": 713, "pending": 135}
    assert index["representationCounts"]["completeReviewedStandaloneProcedures"] == 437
    assert queue["currentAuthority"]["reviewedApplied"] == 713 and queue["currentAuthority"]["pending"] == 135
    assert queue["pendingIdentityAudit"]["sha256"] == sha(PENDING.read_bytes())
    assert handoff["currentIndexBinding"]["sha256"] == sha(idx_path.read_bytes())
    assert pending["indexBinding"]["sha256"] == sha(idx_path.read_bytes()) and pending["pendingCount"] == 135
    first = queue["currentPendingGroups"][0]
    assert first["group"] == "rank8-summon-structure5" and first["pendingIds"] == IDS
    entries = {e["id"]: e for e in index["entries"]}
    live_pending = {e["id"] for e in index["entries"] if e["authoredStatus"] == "pending-authored-procedure"}
    assert set(pending["pendingIds"]) == live_pending and len(live_pending) == 135
    catalog_spells = {s["id"]: s for s in catalog["spells"]}
    old_records = {r["spellId"]: r for r in old["records"]}
    assert list(old_records) == IDS
    for sid in IDS:
        assert sid in live_pending and entries[sid]["authoredStatus"] == "pending-authored-procedure"
        assert old_records[sid]["completeCurrentCatalogSourceAndAccess"] == catalog_spells[sid]

    old_archive_binding = old_prep["archive"]
    old_archive_raw = OLD_ARCHIVE.read_bytes()
    assert len(old_archive_raw) == old_archive_binding["bytes"] and sha(old_archive_raw) == old_archive_binding["sha256"]
    old_candidate_binding = bind(OLD_CANDIDATE)
    now = datetime.now(timezone.utc).isoformat()

    candidate = copy.deepcopy(old)
    candidate.update({
        "id": "RANK8-SUMMON-STRUCTURE5-SOURCE-CONFERENCE02",
        "recordedAtUtc": now,
        "status": "SOURCE_CONFERENCE_PREPARED_UNSENT",
        "priorConferenceSupersededBy": "This Conference02 packet is freshly bound to current authority 713/135. Conference01 remains preserved as historical 525/323 material and its bindings are not current acceptance evidence.",
        "currentAuthority": {
            "reviewedApplied": 713, "pending": 135, "acceptedUnapplied": 0,
            "completeReviewedStandaloneProcedures": 437,
            "index": bind(idx_path), "catalog": bind(catalog_path),
            "currentQueue": bind(QUEUE_BEFORE), "pendingIdentityAudit": bind(PENDING),
            "priorHandoff": bind(HANDOFF_BEFORE),
        },
        "countsUnchanged": copy.deepcopy(index["authoredCounts"]),
        "gptCommunication": "Fresh Rank8 Summon/Structure5 source conference for current authority 713 reviewed / 135 pending. The 20 original source choices remain unselected; exact prior comparison scopes are preserved without reopening any completed spell or feat cohort.",
        "historicalConference01": {
            "status": "HISTORICAL_SOURCE_PACKET_ONLY",
            "authority": copy.deepcopy(old["countsUnchanged"]),
            "candidate": old_candidate_binding,
            "archive": {"path": OLD_ARCHIVE.relative_to(ROOT).as_posix(), "bytes": len(old_archive_raw), "sha256": sha(old_archive_raw)},
            "originalSourceBindings": copy.deepcopy(old["sourceBindings"]),
            "originalCheck": bind(FULL / "RANK8_SUMMON_STRUCTURE_5_SOURCE_CONFERENCE_01_CHECK.json"),
        },
        "historicalPendingComparisonsNowReviewed": [],
        "pendingComparisonsNotAuthority": [],
        "conference01QuestionSetPreserved": {"questions": copy.deepcopy(old["questions"]), "questionCount": len(old["questions"]), "allStillUnselected": True},
        "nonAcceptanceOfLaterSourceChanges": "Current source files in this packet are bound current context only. If a local source or procedure differs from a historical accepted snapshot or receipt, that difference does not expand accepted scope. Use recorded acceptance/application receipts as the limit; do not reopen accepted identities.",
    })
    assert len(candidate["questions"]) == 20 and all(q["decisionSelected"] is False for q in candidate["questions"])
    assert set().union(*(set(q["spellIds"]) for q in candidate["questions"])) == set(IDS)

    for record in candidate["records"]:
        sid = record["spellId"]
        record["completeCurrentCatalogSourceAndAccess"] = copy.deepcopy(catalog_spells[sid])
        record["currentIndexEntry"] = copy.deepcopy(entries[sid])
        record["currentAuthorityStatus"] = "pending-authored-procedure at current 713/135 authority"

    # The former pending comparisons are now reviewed; preserve the old records only as historical context.
    for group in old["pendingComparisonsNotAuthority"]:
        ids = list(group["identities"])
        assert all(entries[sid]["authoredStatus"] == "reviewed-authored-operational-playtest" for sid in ids)
        candidate["historicalPendingComparisonsNowReviewed"].append({
            "historicalGroup": copy.deepcopy(group), "currentReviewedIds": ids,
            "currentIndexEntries": [copy.deepcopy(entries[sid]) for sid in ids],
            "qualification": "Historical pending comparison only; every listed identity is reviewed in the exact 713/135 index and none is pending authority.",
        })

    # Refresh registry rows while retaining the original conference snapshots for comparison.
    current_registry_entries = []
    for item in candidate["currentAcceptedInterfaceComparisons"]:
        pointer = item["registryPointer"].strip("/").split("/")
        value = registry
        for token in pointer:
            value = value[int(token)] if isinstance(value, list) else value[token]
        current_registry_entries.append({"registryPointer": item["registryPointer"], "completeCurrentEntry": copy.deepcopy(value), "historicalConference01Entry": copy.deepcopy(item["completeEntryUnchanged"])})
    candidate["currentAcceptedInterfaceComparisons"] = current_registry_entries

    # Add the newly applied Life/Form4 batch as an exact, scoped recent comparison.
    life_model_path = LIFEFORM_DIR / "MODEL.json"
    life_acceptance = LIFEFORM_AUDIT / "LIFE_FORM4_EXACT_ACCEPTANCE_151.json"
    life_application = LIFEFORM_AUDIT / "LIFE_FORM4_APPLICATION_151.json"
    life_decision = LIFEFORM_AUDIT / "GPT_DIRECTOR_DECISION_LIFE_FORM4_151.json"
    life_model = read(life_model_path)
    life_indices = {row["id"]: row for row in index["entries"]}
    lifeform_comparisons = []
    for i, spell in enumerate(life_model["spells"]):
        sid = spell["id"]
        assert sid in {"animal-shapes", "clone", "flesh-to-grave", "perfect-form"}
        lifeform_comparisons.append({
            "spellId": sid, "source": bind(life_model_path), "pointer": f"/spells/{i}",
            "completeCurrentAcceptedProcedure": copy.deepcopy(spell),
            "currentIndexEntry": copy.deepcopy(life_indices[sid]),
            "exactAcceptance": bind(life_acceptance), "applicationReceipt": bind(life_application),
            "directorDecision": bind(life_decision),
            "qualification": "Accepted and applied authored comparison with all holds retained. No runtime, human-play, balance, cosmology, or release approval; not reopened by this conference.",
        })
    candidate["recentlyAppliedLifeForm4Comparisons"] = lifeform_comparisons

    # Record current comparison bindings separately from the historical source hashes.
    source_paths = {row["path"] for row in old["sourceBindings"]}
    source_paths.update({
        bind(idx_path)["path"], bind(catalog_path)["path"], bind(QUEUE_BEFORE)["path"],
        bind(PENDING)["path"], bind(HANDOFF_BEFORE)["path"], bind(registry_path)["path"],
        bind(life_model_path)["path"], bind(LIFEFORM_DIR / "CANDIDATE_PACKAGE_MANIFEST.json")["path"],
        bind(life_acceptance)["path"], bind(life_application)["path"], bind(life_decision)["path"],
        bind(LIFEFORM_AUDIT / "rank8lifeform4_return151_received/DIRECTOR_RETURN_DELIVERY.json")["path"],
    })
    current_bindings = []
    changed_from_conference01 = []
    historical_bindings = {row["path"]: row for row in old["sourceBindings"]}
    for relative in sorted(source_paths):
        source = ROOT / Path(*relative.split("/"))
        assert source.is_file(), f"Missing current source: {relative}"
        row = bind(source)
        current_bindings.append(row)
        prior = historical_bindings.get(relative)
        if prior and (prior["bytes"], prior["sha256"]) != (row["bytes"], row["sha256"]):
            changed_from_conference01.append({
                "path": relative, "conference01Binding": {"bytes": prior["bytes"], "sha256": prior["sha256"]},
                "currentBinding": row, "scope": "Current context only; a changed backing file does not alter an earlier accepted scope.",
            })
    candidate["sourceBindings"] = current_bindings
    candidate["historicalSourceBindingDeltas"] = changed_from_conference01
    candidate["sourceBindingCounts"] = {"currentFiles": len(current_bindings), "historicalChangedFilesExplicitlyRecorded": len(changed_from_conference01)}

    # Freeze the complete source set, plus the immutable Conference01 archive.
    OUT.mkdir(parents=True)
    (OUT / "sources").mkdir()
    frozen = []
    for row in current_bindings:
        source = ROOT / Path(*row["path"].split("/"))
        dest = OUT / "sources" / Path(*row["path"].split("/"))
        dest.parent.mkdir(parents=True, exist_ok=True)
        raw = source.read_bytes()
        assert len(raw) == row["bytes"] and sha(raw) == row["sha256"]
        dest.write_bytes(raw)
        assert dest.read_bytes() == raw
        frozen.append({**row, "frozenCopy": dest.relative_to(ROOT).as_posix()})
    (OUT / "historical").mkdir()
    (OUT / "historical/Conference01_CANDIDATE.json").write_bytes(OLD_CANDIDATE.read_bytes())
    (OUT / "historical/Conference01_ARCHIVE.zip").write_bytes(old_archive_raw)
    (OUT / "historical/Conference01_CHECK.json").write_bytes((FULL / "RANK8_SUMMON_STRUCTURE_5_SOURCE_CONFERENCE_01_CHECK.json").read_bytes())

    checks = []
    def ck(name: str, passed: bool) -> None:
        checks.append({"check": name, "passed": bool(passed)})
        assert passed, name
    ck("Exact current applied authority is 713/135/0", index["authoredCounts"] == {"reviewed": 713, "pending": 135} and queue["currentAuthority"]["acceptedUnapplied"] == 0)
    ck("All five target identities are the first exact pending group", first["pendingIds"] == IDS and all(entries[s]["authoredStatus"] == "pending-authored-procedure" for s in IDS))
    ck("Pending identity audit matches all 135 current identities", set(pending["pendingIds"]) == live_pending and pending["pendingCount"] == 135)
    ck("Original 20 questions are unchanged, unique, cover all five identities and remain unselected", len(candidate["questions"]) == 20 and len({q["id"] for q in candidate["questions"]}) == 20 and all(not q["decisionSelected"] for q in candidate["questions"]) and set().union(*(set(q["spellIds"]) for q in candidate["questions"])) == set(IDS))
    ck("All five native catalog/access rows match the current catalog exactly", all(next(r for r in candidate["records"] if r["spellId"] == s)["completeCurrentCatalogSourceAndAccess"] == catalog_spells[s] for s in IDS))
    ck("All historical superseded pending comparisons now resolve to reviewed identities", all(all(entries[s]["authoredStatus"] == "reviewed-authored-operational-playtest" for s in row["currentReviewedIds"]) for row in candidate["historicalPendingComparisonsNowReviewed"]))
    ck("Current index, catalog, queue, pending audit and handoff are byte-bound", len([r for r in current_bindings if r["path"] in {bind(idx_path)["path"], bind(catalog_path)["path"], bind(QUEUE_BEFORE)["path"], bind(PENDING)["path"], bind(HANDOFF_BEFORE)["path"]}]) == 5)
    ck("Conference01 archive is preserved as historical 525/323 material", old["countsUnchanged"] == {"reviewed": 525, "pending": 323} and len(old_archive_raw) == old_archive_binding["bytes"] and sha(old_archive_raw) == old_archive_binding["sha256"])
    ck("Life/Form4 is included only as exact accepted applied comparison", {x["spellId"] for x in lifeform_comparisons} == {"animal-shapes", "clone", "flesh-to-grave", "perfect-form"} and all(life_indices[s]["authoredStatus"] == "reviewed-authored-operational-playtest" for s in {x["spellId"] for x in lifeform_comparisons}))
    ck("All recorded historical source deltas are explicit and do not transfer acceptance", all("does not alter" in row["scope"] for row in changed_from_conference01))
    ck("Source archive includes only reviewed source bindings; no source program was run", len(current_bindings) >= 68 and candidate["newRuleAdoptions"] == 0 and candidate["runtimeTestsExecuted"] == 0)
    ck("Closed feats and completed spell cohorts stay outside target IDs", not set(IDS).intersection({"feat335", "erase-mind", "feeblemind", "mass-dominate", "mind-ravel"}))

    candidate_bytes = encode(candidate)
    CANDIDATE.write_bytes(candidate_bytes)
    candidate_binding = bind(CANDIDATE)
    (OUT / "README.md").write_text("Fresh Rank8 Summon/Structure5 Conference02, bound to 713 reviewed / 135 pending. Five exact pending IDs, the original 20 unselected source choices, current queue/handoff/index/catalog, and complete bound source context are preserved. Conference01 remains explicitly historical at 525/323. No procedure or rule has been adopted.\n", encoding="utf-8", newline="\n")
    check_doc = {
        "id": "RANK8-SUMMON-STRUCTURE5-SOURCE-CHECK-152", "status": "PASS",
        "candidate": candidate_binding, "checks": checks, "checkCount": len(checks), "failures": 0,
        "sourceCount": len(current_bindings), "historicalSourceDeltas": len(changed_from_conference01),
        "sourceAuthority": {"reviewedApplied": 713, "pending": 135, "acceptedUnapplied": 0},
        "targetIds": IDS, "questions": 20, "historicalConference01Retained": True,
        "newRuleAdoptions": 0, "runtimeTestsExecuted": 0,
    }
    CHECK.write_bytes(encode(check_doc))
    manifest = {
        "id": "RANK8-SUMMON-STRUCTURE5-SOURCE-CONFERENCE02-MANIFEST-152",
        "candidate": candidate_binding, "check": bind(CHECK), "sourceCount": len(current_bindings),
        "frozenSources": frozen, "historicalConference01Archive": {"path": "historical/Conference01_ARCHIVE.zip", "bytes": len(old_archive_raw), "sha256": sha(old_archive_raw)},
        "sourceAuthority": candidate["currentAuthority"],
    }
    write(OUT / "MANIFEST.json", manifest)
    request = (
        f"Review {ARCHIVE.name} for the exact current authority 713 applied-reviewed / 135 pending / 0 accepted-unapplied.\n"
        "Review only Summon Greater Water Pet, Summon Archlich Shade, Faction Paragon, Conjure Sky Fortress, and Shifting Fortress. "
        "The packet has the exact live queue, pending audit, current handoff, current index/catalog/native rows, and all current source bindings. "
        "The 20 source questions remain unselected; Conference01 is retained as historical 525/323 evidence only. Preserve any recorded accepted snapshot scope; later working-copy changes do not expand prior acceptance. "
        "Resolve each source question, return complete proposed procedures and every disposition, and run the independent failure check. Keep missing profile/geometry/equipment/weapon content and all runtime, human-play, balance, cosmology, and release qualifications explicit. "
        "If the exact package passes, state accepted=true and applied=false for only the exact accepted IDs. If it fails, keep every identity unaccepted and unapplied and list exact blockers. Do not alter canonical files or reopen feat335 or any completed/applied spell cohort.\n"
    )
    REQUEST.write_text(request, encoding="utf-8", newline="\n")
    with zipfile.ZipFile(ARCHIVE, "x", zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        z.write(CANDIDATE, "CANDIDATE.json")
        z.write(CHECK, "SOURCE_CHECK.json")
        z.write(OUT / "MANIFEST.json", "MANIFEST.json")
        z.write(OUT / "README.md", "README.md")
        z.write(REQUEST, "REQUEST.txt")
        z.write(OUT / "historical/Conference01_CANDIDATE.json", "historical/Conference01_CANDIDATE.json")
        z.write(OUT / "historical/Conference01_ARCHIVE.zip", "historical/Conference01_ARCHIVE.zip")
        z.write(OUT / "historical/Conference01_CHECK.json", "historical/Conference01_CHECK.json")
        for row in frozen:
            src = ROOT / Path(*row["frozenCopy"].split("/"))
            z.write(src, "sources/" + row["path"])
    with zipfile.ZipFile(ARCHIVE) as z:
        assert z.testzip() is None and len(z.namelist()) == len(set(z.namelist()))
        assert z.read("CANDIDATE.json") == candidate_bytes
        assert json.loads(z.read("SOURCE_CHECK.json"))["failures"] == 0
        for row in frozen:
            raw = z.read("sources/" + row["path"])
            assert len(raw) == row["bytes"] and sha(raw) == row["sha256"]
        assert z.read("historical/Conference01_ARCHIVE.zip") == old_archive_raw
    archive_binding = bind(ARCHIVE)
    request_binding = bind(REQUEST)
    preparation = {
        "id": "RANK8-SUMMON-STRUCTURE5-SOURCE-CONFERENCE02-PREPARATION-152",
        "recordedAtUtc": datetime.now(timezone.utc).isoformat(), "status": "PREPARED_UNSENT",
        "candidate": candidate_binding, "archive": archive_binding, "manifest": bind(OUT / "MANIFEST.json"),
        "check": bind(CHECK), "request": request_binding, "sourceCount": len(current_bindings),
        "identityCount": 5, "questionCount": 20, "historicalDeltas": len(changed_from_conference01),
        "archiveMemberCount": len(zipfile.ZipFile(ARCHIVE).namelist()), "allArchiveMembersVerified": True,
        "sourceAuthority": {"reviewedApplied": 713, "pending": 135, "acceptedUnapplied": 0},
        "nextGroup": first["group"], "canonicalIndexOrCatalogModified": False,
    }
    write(PREPARATION, preparation)

    queue_after = copy.deepcopy(queue)
    next_group = queue_after["currentPendingGroups"][0]
    next_group["candidate"] = candidate_binding
    next_group["archive"] = archive_binding
    next_group["preparation"] = bind(PREPARATION)
    next_group["freshPacketRequiredForCurrentAuthority"] = False
    queue_after.update({
        "id": "SPELL-REVIEW-QUEUE-153", "recordedAtUtc": datetime.now(timezone.utc).isoformat(),
        "sourceConferencePrepared": {"group": first["group"], "candidate": candidate_binding, "archive": archive_binding, "preparation": bind(PREPARATION), "status": "PREPARED_UNSENT"},
    })
    write(QUEUE_AFTER, queue_after)
    handoff_after = copy.deepcopy(handoff)
    handoff_after.update({
        "id": "CURRENT-HANDOFF-153", "recordedAtUtc": datetime.now(timezone.utc).isoformat(),
        "status": "RANK8_SUMMON_STRUCTURE5_PACKET02_PREPARED_UNSENT_713_135",
        "currentQueueBinding": bind(QUEUE_AFTER), "nextGroup": first["group"],
        "nextPreparedRequest": {"group": first["group"], "candidate": candidate_binding, "archive": archive_binding, "preparation": bind(PREPARATION), "request": request_binding, "freshPacketRequiredForCurrentAuthority": False, "status": "prepared-unsent"},
        "resumePriority": "Submit exact Conference02 to Calibration review part6 for independent source question resolution and failure checking. Apply only an exact accepted return, then continue with the new queue's next pending group.",
    })
    write(HANDOFF_AFTER, handoff_after)
    print(json.dumps({"status": "PREPARATION_PASS", "candidate": candidate_binding, "archive": archive_binding, "request": request_binding, "checks": len(checks), "sources": len(current_bindings), "historicalDeltas": len(changed_from_conference01), "nextAuthority": {"reviewed": 713, "pending": 135}}, indent=2))


if __name__ == "__main__":
    main()
