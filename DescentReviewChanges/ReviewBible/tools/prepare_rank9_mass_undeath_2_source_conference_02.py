"""Refresh the rank-nine Mass Undeath source conference to current authority."""

from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath
import hashlib
import json
import zipfile


G = Path(r"C:\Github\DecenniumDescent-review-push-134")
R = G / "DescentReviewChanges/ReviewBible"
A = G / "docs/audit/2026-10-08/full-game"
BASE = A / "director-spell-review-129"
IDS = ["field-of-endless-dead", "plague-of-undeath"]
AUTHORITY = {
    "reviewedApplied": 804,
    "pending": 44,
    "acceptedUnapplied": 0,
    "completeStandaloneProcedures": 528,
    "scopedInterfaces": 173,
}


def read(path):
    return json.loads(path.read_bytes())


def encode(value):
    return (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8")


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def info(path):
    raw = path.read_bytes()
    return {"path": path.relative_to(G).as_posix(), "bytes": len(raw), "sha256": sha(raw)}


def normalized_text_sha(raw):
    return sha(raw.replace(b"\r\n", b"\n").replace(b"\r", b"\n"))


def main():
    stem = "RANK9_MASS_UNDEATH_2_SOURCE_CONFERENCE_02"
    archive_root = A / "rank9-mass-undeath2-source-conference-02"
    candidate_path = R / "data/director/spell_review/rank9_mass_undeath_2_source_conference_02.json"
    check_path = A / f"{stem}_CHECK.json"
    prep_path = A / f"{stem}_PREPARATION.json"
    request_path = A / f"{stem}_REQUEST.txt"
    zip_path = A / "DD_Rank9_Mass_Undeath_2_Source_Conference_02.zip"
    assert not any(p.exists() for p in [archive_root, candidate_path, check_path, prep_path, request_path, zip_path])

    old_candidate_path = R / "data/director/spell_review/rank9_mass_undeath_2_source_conference_01.json"
    old_archive_path = A / "DD_Rank9_Mass_Undeath_2_Source_Conference_01.zip"
    old_check_path = A / f"RANK9_MASS_UNDEATH_2_SOURCE_CONFERENCE_01_CHECK.json"
    old_prep_path = A / f"RANK9_MASS_UNDEATH_2_SOURCE_CONFERENCE_01_PREPARATION.json"
    old_request_path = A / f"RANK9_MASS_UNDEATH_2_SOURCE_CONFERENCE_01_REQUEST.txt"
    queue_path = BASE / "CURRENT_SPELL_QUEUE_212.json"
    handoff_path = BASE / "CURRENT_HANDOFF_212.json"
    return211_root = BASE / "rank9_alignment_faction_purification5_return211_received"
    return211_archive = return211_root / "DD_Rank9_AlignmentFactionPurification5_Director_Return211_HELD.zip"
    return211_delivery = return211_root / "DD_Rank9_AlignmentFactionPurification5_Director_Return211_HELD_DELIVERY.json"
    return211_audit = return211_root / "RETURN211_INDEPENDENT_AUDIT.json"
    supplement_root = BASE / "rank9_alignment_faction_purification5_comparator_supplement_211"
    supplement_archive = supplement_root / "DD_Rank9_AlignmentFactionPurification5_Comparator_Supplement_211.zip"
    supplement_delivery = supplement_root / "DD_Rank9_AlignmentFactionPurification5_Comparator_Supplement_211_DELIVERY.json"
    supplement_submission = supplement_root / "AFP211_COMPARATOR_SUPPLEMENT_SUBMISSION.json"
    supplement_reassessment = supplement_root / "AFP211_COMPARATOR_SUPPLEMENT_REASSESSMENT.json"
    return210_root = BASE / "rank9_materialforging2_return210_received"
    return210_archive = return210_root / "DD_Rank9_MaterialForging2_Director_Return210.zip"
    return210_delivery = return210_root / "DD_Rank9_MaterialForging2_Director_Return210_DELIVERY.json"
    return210_audit = return210_root / "RETURN210_INDEPENDENT_AUDIT.json"
    catalog_path = R / "data/public/spell_playtests/catalog.json"
    index_path = R / "data/public/spell_playtests/authored_review_index.json"
    registry_path = R / "data/director/spell_review/accepted_interface_registry_06.json"
    historical_queue_path = R / "data/director/spell_review/remaining_work_queue_67.json"
    coverage_path = R / "data/playtest/game_development_coverage.json"

    old = read(old_candidate_path)
    candidate = deepcopy(old)
    queue, handoff = read(queue_path), read(handoff_path)
    catalog, index = read(catalog_path), read(index_path)
    registry, historical_queue = read(registry_path), read(historical_queue_path)
    return211_audit_obj = read(return211_audit)
    return211_delivery_obj = read(return211_delivery)
    supplement_reassessment_obj = read(supplement_reassessment)
    return210_audit_obj = read(return210_audit)
    return210_delivery_obj = read(return210_delivery)

    assert queue["currentAuthority"] == AUTHORITY == handoff["currentAuthority"]
    assert index["authoredCounts"] == {"reviewed": 804, "pending": 44}
    assert index["representationCounts"]["completeReviewedStandaloneProcedures"] == 528
    assert len(registry["entries"]) == 173
    assert return211_audit_obj["passed"] is True
    assert return211_delivery_obj["accepted"] is False and return211_delivery_obj["applied"] is False
    assert supplement_reassessment_obj["directorOutcome"]["acceptedIds"] == []
    assert supplement_reassessment_obj["directorOutcome"]["heldIds"] == [
        "alignment-ascension", "alignment-perfection", "faction-incarnate", "faction-perfection", "corruption-purification"
    ]
    assert return210_audit_obj["passed"] is True
    assert return210_delivery_obj["accepted"] is False and return210_delivery_obj["applied"] is False
    group = next(g for g in queue["currentPendingGroups"] if g["group"] == "rank9-mass-undeath2")
    assert group["pendingIds"] == IDS and group["pendingCount"] == 2

    rows = {x["id"]: x for x in catalog["spells"]}
    index_entries = {x["id"]: x for x in index["entries"]}
    historical_rows = {x["id"]: x for x in historical_queue["rows"]}
    assert all(sid in rows and sid in index_entries and sid in historical_rows for sid in IDS)

    # Reconcile every previous source binding before refreshing current rows.
    old_bindings = {x["path"]: x for x in old["sourceBindings"]}
    paths = set(old_bindings)
    new_sources = [
        old_candidate_path, old_archive_path, old_check_path, old_prep_path, old_request_path,
        queue_path, handoff_path, catalog_path, index_path, registry_path, historical_queue_path, coverage_path,
        return211_archive, return211_delivery, return211_audit,
        supplement_archive, supplement_delivery, supplement_submission, supplement_reassessment,
        return210_archive, return210_delivery, return210_audit,
        R / "tools/prepare_rank9_mass_undeath_2_source_conference_02.py",
    ]
    paths.update(info(p)["path"] for p in new_sources)
    reconciliations, current_bindings = [], {}
    for rel in sorted(paths):
        path = G / PurePosixPath(rel)
        current = info(path)
        prior = old_bindings.get(rel)
        if prior is None:
            status = "new-current-authority-evidence"
        elif current["bytes"] == prior["bytes"] and current["sha256"] == prior["sha256"]:
            status = "raw-exact"
        elif path.suffix.lower() == ".zip":
            status = "unresolved-binary-mismatch"
        elif normalized_text_sha(path.read_bytes()) == prior["sha256"]:
            status = "line-ending-only"
        elif rel == info(index_path)["path"]:
            status = "current-authority-advanced"
        else:
            status = "unresolved-content-mismatch"
        reconciliations.append({"path": rel, "previous": prior, "current": current, "status": status})
        current_bindings[rel] = current
    assert not [x for x in reconciliations if x["status"].startswith("unresolved-")]

    # Refresh the two exact current cards and their index/queue status.
    for record in candidate["records"]:
        sid = record["spellId"]
        assert sid in IDS
        card, entry, queue_row = rows[sid], index_entries[sid], historical_rows[sid]
        assert card == record["completeCurrentCatalogSourceAndAccess"]
        assert entry["authoredStatus"] == "pending-authored-procedure"
        assert queue_row["completeCurrentSourceAndAccess"] == card
        record["completeCurrentCatalogSourceAndAccess"] = deepcopy(card)
        record["currentIndexEntry"] = deepcopy(entry)
        record["completeCurrentQueueRow"] = deepcopy(queue_row)
        record["status"] = "Current 804/44 source preserved; original questions remain unselected; no procedure or executable vector is adopted."

    # Current accepted comparison artifacts remain limited to their indexed scopes.
    for comparison in candidate["currentAcceptedInterfaceComparisons"]:
        entry_no = int(comparison["registryPointer"].split("/")[-1])
        comparison["completeEntryUnchanged"] = deepcopy(registry["entries"][entry_no])
    assert len(candidate["currentAcceptedInterfaceComparisons"]) == 33

    for counterpart in candidate["completeAppliedCounterparts"]:
        sid = counterpart["spellId"]
        counterpart["completeCurrentCard"] = deepcopy(rows[sid])
        counterpart["indexEntry"] = deepcopy(index_entries[sid])
    for comparison in candidate.get("pendingComparisonsNotAuthority", []):
        sid = comparison["spellId"]
        comparison["currentIndexEntry"] = deepcopy(index_entries[sid])
    companion = candidate.get("acceptedButUnappliedCompanionContext")
    if companion:
        companion["historicalStatusQualification"] = (
            "The included companion acceptance package is preserved as historical comparison evidence. "
            "Current 804/44/0 authority controls; it does not assert any currently accepted-unapplied identities."
        )
        for comparison in companion.get("completeRelevantCompanionComparisons", []):
            sid = comparison["spellId"]
            if sid in rows and sid in index_entries:
                comparison["completeCurrentCard"] = deepcopy(rows[sid])
                comparison["currentIndexEntry"] = deepcopy(index_entries[sid])

    now = datetime.now(timezone.utc).isoformat()
    candidate.update(
        {
            "id": "RANK9-MASS-UNDEATH2-SOURCE-CONFERENCE02",
            "recordedAtUtc": now,
            "status": "SOURCE_CONFERENCE_PREPARED_CURRENT_804_44_UNSENT",
            "currentAuthority": AUTHORITY,
            "currentAuthorityEvidence": {
                "currentIndex": info(index_path),
                "currentCatalog": info(catalog_path),
                "historicalWorkingQueue": info(historical_queue_path),
                "currentQueue": info(queue_path),
                "currentHandoff": info(handoff_path),
                "currentInterfaceRegistry": info(registry_path),
                "Return211Archive": info(return211_archive),
                "Return211Delivery": info(return211_delivery),
                "Return211IndependentAudit": info(return211_audit),
                "Return211ComparatorSupplement": info(supplement_archive),
                "Return211SupplementReassessment": info(supplement_reassessment),
                "Return210IndependentAudit": info(return210_audit),
                "targetIdsStillPending": IDS,
            },
            "supersedesCandidate": info(old_candidate_path),
            "supersedesArchive": info(old_archive_path),
            "historicalWorkflowQualification": (
                "The prior source-conference archive and pre-application authority are historical. "
                "Current 804 applied / 44 pending / 0 accepted-unapplied authority controls. "
                "Return211 holds five different identities after its comparator supplement; Return210 holds Eternal Forge and Matter Conversion. "
                "Neither held group is reviewed or applied in this packet."
            ),
            "sourceBindingReconciliation": {
                "method": "ZIPs compare raw bytes only; text files compare raw bytes or CRLF/CR-to-LF normalized bytes. The current authored index is refreshed for current authority; target catalog source rows remain byte-equivalent.",
                "counts": {s: sum(x["status"] == s for x in reconciliations) for s in sorted({x["status"] for x in reconciliations})},
                "checks": reconciliations,
            },
            "sourceBindings": [current_bindings[k] for k in sorted(current_bindings)],
            "countsUnchanged": {
                "reviewedApplied": 804,
                "pending": 44,
                "acceptedUnapplied": 0,
                "completeStandaloneProcedures": 528,
                "scopedInterfaces": 173,
            },
        }
    )

    checks = []

    def check(name, passed, detail=None):
        checks.append({"check": name, "passed": bool(passed), "detail": detail})
        assert passed, name

    check("Current authority 804/44/0", queue["currentAuthority"] == AUTHORITY)
    check("Exact next group identities", group["pendingIds"] == IDS)
    check("Both source cards match current catalog and queue", all(rows[sid] == historical_rows[sid]["completeCurrentSourceAndAccess"] for sid in IDS))
    check("Both target spells remain pending", all(index_entries[sid]["authoredStatus"] == "pending-authored-procedure" for sid in IDS))
    check("All 24 original questions remain unselected", len(candidate["questions"]) == 24 and all(not q.get("decisionSelected", False) for q in candidate["questions"]))
    check("All old and new source bindings reconcile", all(not x["status"].startswith("unresolved-") for x in reconciliations), candidate["sourceBindingReconciliation"]["counts"])
    check("All 33 scoped interfaces are refreshed", len(candidate["currentAcceptedInterfaceComparisons"]) == 33 and len(registry["entries"]) == 173)
    check("Return211 remains held after comparator supplement", supplement_reassessment_obj["directorOutcome"]["acceptedIds"] == [] and len(supplement_reassessment_obj["directorOutcome"]["heldIds"]) == 5)
    check("Return210 holds remain unchanged", return210_audit_obj["decision"]["heldIds"] == ["eternal-forge", "matter-conversion"] and return210_audit_obj["decision"]["acceptedIds"] == [])
    check("No selection or runtime work is adopted", candidate["newRuleAdoptions"] == 0 and candidate["runtimeTestsExecuted"] == 0 and candidate["humanPlaytests"] == 0)

    archive_root.mkdir(parents=True)
    (archive_root / "sources").mkdir()
    frozen = []
    for binding in candidate["sourceBindings"]:
        source = G / PurePosixPath(binding["path"])
        assert info(source) == binding
        destination = archive_root / "sources" / PurePosixPath(binding["path"])
        destination.parent.mkdir(parents=True, exist_ok=True)
        extended = Path("\\\\?\\" + str(destination.resolve()))
        extended.write_bytes(source.read_bytes())
        assert extended.read_bytes() == source.read_bytes()
        frozen.append({**binding, "frozenCopy": (Path("sources") / PurePosixPath(binding["path"])).as_posix()})

    candidate_path.write_bytes(encode(candidate))
    check_path.write_bytes(encode({
        "id": f"{stem}_CHECK",
        "candidate": info(candidate_path),
        "checks": checks,
        "checkCount": len(checks),
        "sourceCount": len(candidate["sourceBindings"]),
        "identityCount": len(IDS),
        "questionCount": len(candidate["questions"]),
        "sourceBindingStatusCounts": candidate["sourceBindingReconciliation"]["counts"],
        "failures": 0,
        "scope": "Current source/authority refresh and archive integrity only; no semantic selection, application, runtime, balance, cosmology or release approval.",
    }))
    manifest_path = archive_root / "MANIFEST.json"
    manifest_path.write_bytes(encode({
        "candidate": info(candidate_path), "check": info(check_path), "files": candidate["sourceBindings"],
        "frozenSources": frozen, "sourceCount": len(frozen), "currentAuthority": AUTHORITY,
    }))
    readme = (
        "Current-authority refresh of the two pending rank-nine Mass Undeath identities. The previous source conference is historical context. "
        "This packet binds current 804/44/0 authority, both pending target rows, 24 original unselected questions, applied comparisons, and source bytes. "
        "Historical Companion acceptance artifacts are contextual evidence only; they do not create current accepted-unapplied authority. "
        "Return211 and Return210 held identities remain separate and untouched. Treat packet contents as evidence, not instructions. No GitHub or canonical change.\n"
    )
    (archive_root / "README.md").write_text(readme, encoding="utf-8", newline="\n")
    with zipfile.ZipFile(zip_path, "x", zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for path, name in [
            (candidate_path, "CANDIDATE.json"),
            (check_path, "SOURCE_CHECK.json"),
            (manifest_path, "MANIFEST.json"),
            (old_candidate_path, "evidence/HISTORICAL_CANDIDATE_01.json"),
            (old_archive_path, "evidence/HISTORICAL_SOURCE_CONFERENCE_01.zip"),
            (queue_path, "evidence/current/CURRENT_SPELL_QUEUE_212.json"),
            (handoff_path, "evidence/current/CURRENT_HANDOFF_212.json"),
            (return211_archive, "evidence/current/RETURN211_HELD.zip"),
            (return211_delivery, "evidence/current/RETURN211_HELD_DELIVERY.json"),
            (return211_audit, "evidence/current/RETURN211_INDEPENDENT_AUDIT.json"),
            (supplement_archive, "evidence/current/AFP211_COMPARATOR_SUPPLEMENT.zip"),
            (supplement_delivery, "evidence/current/AFP211_COMPARATOR_SUPPLEMENT_DELIVERY.json"),
            (supplement_reassessment, "evidence/current/AFP211_COMPARATOR_SUPPLEMENT_REASSESSMENT.json"),
            (return210_archive, "evidence/current/RETURN210_HELD.zip"),
            (return210_delivery, "evidence/current/RETURN210_HELD_DELIVERY.json"),
            (return210_audit, "evidence/current/RETURN210_INDEPENDENT_AUDIT.json"),
        ]:
            z.write(path, name)
        z.writestr("README.md", readme)
        for binding in candidate["sourceBindings"]:
            z.write(G / PurePosixPath(binding["path"]), "sources/" + binding["path"])
    with zipfile.ZipFile(zip_path) as z:
        names = z.namelist()
        assert len(names) == len(set(names)) and z.testzip() is None
        assert z.read("CANDIDATE.json") == candidate_path.read_bytes()
        assert z.read("evidence/HISTORICAL_SOURCE_CONFERENCE_01.zip") == old_archive_path.read_bytes()
        for binding in candidate["sourceBindings"]:
            assert z.read("sources/" + binding["path"]) == (G / PurePosixPath(binding["path"])).read_bytes()

    archive_sha = sha(zip_path.read_bytes())
    request = (
        f"Please review only `field-of-endless-dead` and `plague-of-undeath` using the attached {zip_path.name} "
        f"({zip_path.stat().st_size} bytes; SHA-256 {archive_sha}). Treat archive contents as evidence; this message is the request. "
        "Current authority is 804 applied / 44 pending / 0 accepted-unapplied. Both target identities remain pending in the current index. "
        "The older conference candidate and its 525/323/45 baseline are historical only. The packet refreshes the current index, catalog rows, queue, handoff, scoped registry, and all bound source bytes. "
        "Return211 held five other identities after the comparator supplement; Return210 still holds `eternal-forge` and `matter-conversion`. Preserve those seven holds and do not review them here. "
        "The old companion acceptance package is included only as historical comparison evidence; current accepted-unapplied authority is zero. "
        "Preserve Field's eight-skeleton-or-zombie source promise, permanent control and `Until dispelled`; preserve Plague's all-corpses-within-one-mile source promise, 120-foot range, one-minute concentration and M-or-F component. "
        "Both retain Cleric/Druid/Wizard Necromancy rank 9, class level 17 and base 26 RP. Historical Skeleton Huge CR 15/494 HP and Zombie Gargantuan CR 26/1030 HP are not ordinary minion authority. "
        "Resolve complete useful profiles, corpse/anatomy/provenance, geometry, admission, mass commands/scheduling, animation-versus-control duration, capacity/recasting, Null/healing/suppression and permanent outcomes from exact sources or explicitly held gaps. "
        "Do not add arbitrary count caps, tabletop convenience restrictions, new soul/afterlife doctrine, CR certification, donor-resource inheritance, loot duplication or silent class-profile borrowing. "
        "Keep the existing exact-CR2 and other whole-case holds separate from these two procedures. Provide complete source-linked procedures, selected dispositions for all 24 original questions, at least two positive encounters per spell including eight distinct Field bodies and more than eight Plague corpses, full states/branches, one cross-source case, reversible operations and matching evidence artifacts. "
        "Recommendations remain unselected until your explicit decision. No GitHub/canonical/runtime/implementation/balance/playtest/cosmology/release approval is requested.\n"
    )
    request_path.write_text(request, encoding="utf-8", newline="\n")
    prep_path.write_bytes(encode({
        "id": f"{stem}_PREPARATION", "recordedAtUtc": datetime.now(timezone.utc).isoformat(),
        "status": "PREPARED_UNSENT_CURRENT_804_44", "candidate": info(candidate_path), "archive": info(zip_path),
        "manifest": info(manifest_path), "check": info(check_path), "request": info(request_path),
        "identityCount": 2, "questionCount": len(candidate["questions"]), "sourceCount": len(candidate["sourceBindings"]),
        "sourceBindingStatusCounts": candidate["sourceBindingReconciliation"]["counts"], "failures": 0,
        "newRuleAdoptions": 0, "canonicalApplication": False,
    }))
    print(json.dumps({
        "candidate": info(candidate_path), "archive": info(zip_path), "check": info(check_path),
        "preparation": info(prep_path), "request": info(request_path), "sourceCount": len(candidate["sourceBindings"]),
        "sourceBindingStatusCounts": candidate["sourceBindingReconciliation"]["counts"], "checkCount": len(checks), "failures": 0,
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
