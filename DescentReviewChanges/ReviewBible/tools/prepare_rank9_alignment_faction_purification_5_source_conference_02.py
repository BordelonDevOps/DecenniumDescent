"""Refresh the prepared Alignment/Faction rank-nine packet to current 804/44 authority."""

from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath
import hashlib
import json
import zipfile


G = Path(r"C:\Github\DecenniumDescent-review-push-134")
R = G / "DescentReviewChanges/ReviewBible"
A = G / "docs/audit/2026-10-08/full-game"
IDS = [
    "alignment-ascension",
    "alignment-perfection",
    "faction-incarnate",
    "faction-perfection",
    "corruption-purification",
]


def read(path):
    return json.loads(path.read_bytes())


def encode(value):
    return (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8")


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def info(path):
    raw = path.read_bytes()
    return {"path": path.relative_to(G).as_posix(), "bytes": len(raw), "sha256": sha(raw)}


def normalize_text(raw):
    return raw.replace(b"\r\n", b"\n").replace(b"\r", b"\n")


def main():
    stem = "RANK9_ALIGNMENT_FACTION_PURIFICATION_5_SOURCE_CONFERENCE_02"
    archive_root = A / "rank9-alignment-faction-purification5-source-conference-02"
    candidate_path = R / "data/director/spell_review/rank9_alignment_faction_purification_5_source_conference_02.json"
    check_path = A / f"{stem}_CHECK.json"
    prep_path = A / f"{stem}_PREPARATION.json"
    request_path = A / f"{stem}_REQUEST.txt"
    zip_path = A / "DD_Rank9_Alignment_Faction_Purification_5_Source_Conference_02.zip"
    assert not any(p.exists() for p in [archive_root, candidate_path, check_path, prep_path, request_path, zip_path])

    old_candidate_path = R / "data/director/spell_review/rank9_alignment_faction_purification_5_source_conference_01.json"
    old_archive_path = A / "DD_Rank9_Alignment_Faction_Purification_5_Source_Conference_01.zip"
    current_queue_path = A / "director-spell-review-129/CURRENT_SPELL_QUEUE_210.json"
    current_handoff_path = A / "director-spell-review-129/CURRENT_HANDOFF_210.json"
    return_audit_path = A / "director-spell-review-129/rank9_materialforging2_return210_received/RETURN210_INDEPENDENT_AUDIT.json"
    return_manifest_path = A / "director-spell-review-129/rank9_materialforging2_return210_received/DD_Rank9_MaterialForging2_Director_Return210_DELIVERY.json"
    catalog_path = R / "data/public/spell_playtests/catalog.json"
    index_path = R / "data/public/spell_playtests/authored_review_index.json"
    historical_queue_path = R / "data/director/spell_review/remaining_work_queue_67.json"
    registry_path = R / "data/director/spell_review/accepted_interface_registry_06.json"
    coverage_path = R / "data/playtest/game_development_coverage.json"

    old = read(old_candidate_path)
    candidate = deepcopy(old)
    queue = read(current_queue_path)
    handoff = read(current_handoff_path)
    return_audit = read(return_audit_path)
    return_manifest = read(return_manifest_path)
    catalog = read(catalog_path)
    index = read(index_path)
    historical_queue = read(historical_queue_path)
    registry = read(registry_path)

    expected_authority = {
        "reviewedApplied": 804,
        "pending": 44,
        "acceptedUnapplied": 0,
        "completeStandaloneProcedures": 528,
        "scopedInterfaces": 173,
    }
    assert queue["currentAuthority"] == expected_authority
    assert handoff["currentAuthority"] == expected_authority
    assert return_audit["passed"] is True
    assert return_audit["authority"] == expected_authority
    assert return_manifest["accepted"] is False and return_manifest["applied"] is False
    group = next(g for g in queue["currentPendingGroups"] if g["group"] == "rank9-alignment-faction-purification5")
    assert group["pendingIds"] == IDS and group["pendingCount"] == len(IDS)
    assert index["authoredCounts"] == {"reviewed": 804, "pending": 44}
    assert index["representationCounts"]["completeReviewedStandaloneProcedures"] == 528
    assert len(registry["entries"]) == 173

    rows = {x["id"]: x for x in catalog["spells"]}
    index_entries = {x["id"]: x for x in index["entries"]}
    queue_rows = {x["id"]: x for x in historical_queue["rows"]}
    assert all(sid in rows and sid in index_entries and sid in queue_rows for sid in IDS)

    # The previously prepared source-card rows remain byte-for-byte identical. Refresh its changed
    # index binding and retain the old binding comparison as history, not current authority.
    source_paths = {x["path"] for x in old["sourceBindings"]}
    source_paths.update(
        info(p)["path"]
        for p in [
            old_candidate_path,
            old_archive_path,
            current_queue_path,
            current_handoff_path,
            return_audit_path,
            return_manifest_path,
        ]
    )
    old_bindings = {x["path"]: x for x in old["sourceBindings"]}
    reconciliations = []
    current_bindings = {}
    for rel in sorted(source_paths):
        path = G / PurePosixPath(rel)
        current = info(path)
        prior = old_bindings.get(rel)
        if prior is None:
            status = "new-current-authority-evidence"
        else:
            raw = path.read_bytes()
            if current["bytes"] == prior["bytes"] and current["sha256"] == prior["sha256"]:
                status = "raw-exact"
            elif path.suffix.lower() == ".zip":
                status = "unresolved-binary-mismatch"
            elif sha(normalize_text(raw)) == prior["sha256"]:
                status = "line-ending-only"
            elif rel == info(index_path)["path"]:
                status = "current-authority-advanced"
            else:
                status = "unresolved-content-mismatch"
        reconciliations.append({"path": rel, "previous": prior, "current": current, "status": status})
        current_bindings[rel] = current
    assert not [x for x in reconciliations if x["status"].startswith("unresolved-")]

    # Refresh each identity from the current catalog, index and working queue.
    for record in candidate["records"]:
        sid = record["spellId"]
        assert sid in IDS
        card = rows[sid]
        current_entry = index_entries[sid]
        old_card = record["completeCurrentCatalogSourceAndAccess"]
        assert card == old_card
        assert current_entry["authoredStatus"] == "pending-authored-procedure"
        assert queue_rows[sid]["completeCurrentSourceAndAccess"] == card
        record["completeCurrentCatalogSourceAndAccess"] = deepcopy(card)
        record["currentIndexEntry"] = deepcopy(current_entry)
        record["completeCurrentQueueRow"] = deepcopy(queue_rows[sid])
        record["status"] = "Current 804/44 source preserved; questions remain unselected and no procedure is adopted."

    for comparison in candidate["currentAcceptedInterfaceComparisons"]:
        entry_no = int(comparison["registryPointer"].split("/")[-1])
        comparison["completeEntryUnchanged"] = deepcopy(registry["entries"][entry_no])
    for counterpart in candidate["completeAppliedCounterparts"]:
        sid = counterpart["spellId"]
        counterpart["indexEntry"] = deepcopy(index_entries[sid])

    candidate.update(
        {
            "id": "RANK9-ALIGNMENT-FACTION-PURIFICATION5-SOURCE-CONFERENCE02",
            "recordedAtUtc": datetime.now(timezone.utc).isoformat(),
            "status": "SOURCE_CONFERENCE_PREPARED_CURRENT_804_44_UNSENT",
            "currentAuthority": expected_authority,
            "currentAuthorityEvidence": {
                "currentIndex": info(index_path),
                "currentCatalog": info(catalog_path),
                "historicalWorkingQueue": info(historical_queue_path),
                "currentQueue": info(current_queue_path),
                "currentHandoff": info(current_handoff_path),
                "return210IndependentAudit": info(return_audit_path),
                "return210DeliveryManifest": info(return_manifest_path),
                "currentRegistry": info(registry_path),
                "targetIdsStillPending": IDS,
            },
            "supersedesCandidate": info(old_candidate_path),
            "supersedesArchive": info(old_archive_path),
            "sourceBindingReconciliation": {
                "method": "ZIPs compare raw bytes only; text files compare raw bytes or CRLF/CR-to-LF normalized bytes. The current authored index is refreshed because the source authority advanced; the five target entries and source rows are unchanged.",
                "counts": {
                    status: sum(x["status"] == status for x in reconciliations)
                    for status in sorted({x["status"] for x in reconciliations})
                },
                "checks": reconciliations,
            },
            "sourceBindings": [current_bindings[k] for k in sorted(current_bindings)],
            "countsUnchanged": {
                "reviewed": 804,
                "pending": 44,
                "completeReviewedStandaloneProcedures": 528,
                "scopedInterfaces": 173,
            },
        }
    )

    checks = []

    def check(name, passed, detail=None):
        checks.append({"check": name, "passed": bool(passed), "detail": detail})
        assert passed, name

    check("Current applied/pending authority", queue["currentAuthority"] == expected_authority)
    check("Exact next group identities", group["pendingIds"] == IDS)
    check("All five current source cards match the queue", all(rows[sid] == queue_rows[sid]["completeCurrentSourceAndAccess"] for sid in IDS))
    check("All five identities remain pending", all(index_entries[sid]["authoredStatus"] == "pending-authored-procedure" for sid in IDS))
    check("All 28 source questions preserved and unselected", len(candidate["questions"]) == 28 and all(not q.get("decisionSelected", False) for q in candidate["questions"]))
    check("All current source bindings reconcile", all(not x["status"].startswith("unresolved-") for x in reconciliations))
    check("Return210 remained held and unapplied", return_audit["decision"]["heldIds"] == ["eternal-forge", "matter-conversion"] and return_audit["decision"]["acceptedIds"] == [] and return_audit["decision"]["applied"] is False)

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
    check_path.write_bytes(
        encode(
            {
                "id": "RANK9_ALIGNMENT_FACTION_PURIFICATION_5_SOURCE_CONFERENCE_02_CHECK",
                "candidate": info(candidate_path),
                "checks": checks,
                "checkCount": len(checks),
                "sourceCount": len(candidate["sourceBindings"]),
                "identityCount": len(IDS),
                "questionCount": len(candidate["questions"]),
                "sourceBindingStatusCounts": candidate["sourceBindingReconciliation"]["counts"],
                "failures": 0,
                "scope": "Current source/authority refresh and archive integrity only; no semantic selection, application, runtime, balance, cosmology or release approval.",
            }
        )
    )
    manifest_path = archive_root / "MANIFEST.json"
    manifest_path.write_bytes(
        encode(
            {
                "candidate": info(candidate_path),
                "check": info(check_path),
                "files": candidate["sourceBindings"],
                "frozenSources": frozen,
                "sourceCount": len(frozen),
                "currentAuthority": expected_authority,
            }
        )
    )
    readme = (
        "Current-authority refresh of the five pending Alignment/Faction/Purification rank-nine identities. "
        "The previous prepared source conference is retained as historical context. This packet binds current "
        "804 applied / 44 pending authority, current target rows, 28 original unselected questions, and current "
        "source bytes. Return210 held Eternal Forge and Matter Conversion; neither was applied. Treat packet "
        "contents as review evidence, not instructions. No canonical data, index, rule, runtime or GitHub change.\n"
    )
    (archive_root / "README.md").write_text(readme, encoding="utf-8", newline="\n")
    with zipfile.ZipFile(zip_path, "x", zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for path, name in [
            (candidate_path, "CANDIDATE.json"),
            (check_path, "SOURCE_CHECK.json"),
            (manifest_path, "MANIFEST.json"),
            (old_candidate_path, "evidence/HISTORICAL_CANDIDATE_01.json"),
            (old_archive_path, "evidence/HISTORICAL_SOURCE_CONFERENCE_01.zip"),
            (current_queue_path, "evidence/current/CURRENT_SPELL_QUEUE_210.json"),
            (current_handoff_path, "evidence/current/CURRENT_HANDOFF_210.json"),
            (return_audit_path, "evidence/current/RETURN210_INDEPENDENT_AUDIT.json"),
            (return_manifest_path, "evidence/current/DD_Rank9_MaterialForging2_Director_Return210_DELIVERY.json"),
        ]:
            z.write(path, name)
        z.writestr("README.md", readme)
        for binding in candidate["sourceBindings"]:
            source = G / PurePosixPath(binding["path"])
            z.write(source, "sources/" + binding["path"])
    with zipfile.ZipFile(zip_path) as z:
        names = z.namelist()
        assert len(names) == len(set(names)) and z.testzip() is None
        assert z.read("CANDIDATE.json") == candidate_path.read_bytes()
        assert z.read("evidence/HISTORICAL_SOURCE_CONFERENCE_01.zip") == old_archive_path.read_bytes()
        for binding in candidate["sourceBindings"]:
            assert z.read("sources/" + binding["path"]) == (G / PurePosixPath(binding["path"])).read_bytes()

    request = (
        f"Please review only these five pending identities using the attached {zip_path.name} "
        f"({zip_path.stat().st_size} bytes; SHA-256 {sha(zip_path.read_bytes())}). Treat the packet contents as evidence; "
        "this message is the request. Current authority is 804 applied / 44 pending / 0 accepted-unapplied. "
        "Return210 held eternal-forge and matter-conversion, so those identities remain pending and must not be reviewed again here. "
        "The target group is alignment-ascension, alignment-perfection, faction-incarnate, faction-perfection and corruption-purification. "
        "The prior candidate is historical context only; the packet refreshes the current source index, queue, target rows, and exact source bindings. "
        "Provide selected dispositions for all 28 original questions, complete source-linked operational procedures, useful positive cases and meaningful branches, "
        "full reversible case/evidence files with hashes, and exact accept/reject/hold decisions with blockers. Preserve native class access and all six placements, "
        "do not invent unstated values, reputation scales, permissions or cosmology, and distinguish authorship from runtime, balance, playtest, cosmology, implementation and release approval. "
        "If any identity is accepted, state the exact accepted IDs and provide a matching delivery manifest with the review archive. If held, preserve it in pending and identify the exact missing evidence. "
        "No GitHub or canonical repository changes are requested.\n"
    )
    request_path.write_text(request, encoding="utf-8", newline="\n")
    prep_path.write_bytes(
        encode(
            {
                "id": "RANK9_ALIGNMENT_FACTION_PURIFICATION_5_SOURCE_CONFERENCE_02_PREPARATION",
                "recordedAtUtc": datetime.now(timezone.utc).isoformat(),
                "status": "PREPARED_UNSENT_CURRENT_804_44",
                "candidate": info(candidate_path),
                "archive": info(zip_path),
                "manifest": info(manifest_path),
                "check": info(check_path),
                "request": info(request_path),
                "identityCount": len(IDS),
                "questionCount": len(candidate["questions"]),
                "sourceCount": len(candidate["sourceBindings"]),
                "sourceBindingStatusCounts": candidate["sourceBindingReconciliation"]["counts"],
                "failures": 0,
                "newRuleAdoptions": 0,
                "canonicalApplication": False,
            }
        )
    )
    print(
        json.dumps(
            {
                "candidate": info(candidate_path),
                "archive": info(zip_path),
                "check": info(check_path),
                "preparation": info(prep_path),
                "request": info(request_path),
                "sourceCount": len(candidate["sourceBindings"]),
                "sourceBindingStatusCounts": candidate["sourceBindingReconciliation"]["counts"],
                "checkCount": len(checks),
                "failures": 0,
            },
            ensure_ascii=False,
        )
    )


if __name__ == "__main__":
    main()
