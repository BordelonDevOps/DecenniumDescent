#!/usr/bin/env python3
"""Prepare a current-authority, one-identity reassessment for AFP211-B01."""

from __future__ import annotations

import hashlib
import json
import zipfile
import zlib
from datetime import datetime, timezone
from pathlib import Path
from zipfile import ZipFile

A = Path(__file__).resolve().parent
ROOT = A.parents[4]
OUT = A / "rank9_alignment_ascension_review_335_prepared"
PACKET = OUT / "packet"
ARCHIVE = OUT / "DD_Rank9_AlignmentAscension_Review335.zip"
DELIVERY = OUT / "DD_Rank9_AlignmentAscension_Review335_DELIVERY.json"
QUEUE = A / "CURRENT_SPELL_QUEUE_334.json"
PENDING = A / "CURRENT25_PENDING_IDENTITY_AUDIT_334.json"
HANDOFF = A / "CURRENT_HANDOFF_334.json"
CATALOG = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json"
INDEX = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json"
CORE = ROOT / "DescentReviewChanges/ReviewBible/data/public/Decennium_Descent_Core_Systems_Data_v2_Known_Descent.json"
OLD_SOURCE = A / "rank9_alignmentfactionpurification5_current_source_287_prepared/CURRENT_SOURCE_CONFERENCE_CANDIDATE_287.json"
PRIOR = A / "rank9_alignmentfactionpurification5_return287_received/DD_Rank9_AlignmentFactionPurification5_Director_Return287_HELD.zip"
SPELL_ID = "alignment-ascension"
BLOCKER = "AFP211-B01"
COMPARATORS = ["alignment-avatar", "alignment-immunity"]
RELATED_ROWS = ["alignment-ascension", "alignment-avatar", "alignment-immunity", "alignment-revelation"]


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def crc(data: bytes) -> str:
    return f"{zlib.crc32(data) & 0xFFFFFFFF:08x}"


def bind(path: Path) -> dict:
    data = path.read_bytes()
    return {"path": path.relative_to(ROOT).as_posix(), "bytes": len(data), "sha256": sha(data), "crc32": crc(data)}


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def save(path: Path, value) -> None:
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def find_id(node, wanted):
    if isinstance(node, dict):
        if node.get("id") == wanted:
            return node
        for value in node.values():
            found = find_id(value, wanted)
            if found is not None:
                return found
    elif isinstance(node, list):
        for value in node:
            found = find_id(value, wanted)
            if found is not None:
                return found
    return None


def pointer_get(node, pointer: str):
    value = node
    for raw in pointer.strip("/").split("/"):
        part = raw.replace("~1", "/").replace("~0", "~")
        value = value[int(part)] if isinstance(value, list) else value[part]
    return value


def main() -> None:
    marker = OUT / "PREPARATION_AUDIT_335.json"
    if OUT.exists():
        if marker.exists() and load(marker).get("id") != "ALIGNMENT-ASCENSION-REVIEW335-PREPARATION-AUDIT":
            raise RuntimeError(f"Output marker belongs to another preparation; refusing to overwrite: {OUT}")
        if not marker.exists() and any(path.is_file() for path in OUT.rglob("*")):
            partial = PACKET / "00_CURRENT_AUTHORITY_334.json"
            if not partial.is_file() or load(partial).get("authority") != load(QUEUE).get("currentAuthority"):
                raise RuntimeError(f"Output contains files without this generator's preparation marker; refusing to overwrite: {OUT}")
    PACKET.mkdir(parents=True, exist_ok=True)

    queue, pending, handoff = load(QUEUE), load(PENDING), load(HANDOFF)
    catalog, index = load(CATALOG), load(INDEX)
    current_rows = {ident: find_id(catalog, ident) for ident in RELATED_ROWS}
    spell, index_row = current_rows[SPELL_ID], find_id(index, SPELL_ID)
    if any(value is None for value in current_rows.values()) or index_row is None:
        raise RuntimeError("Current target/comparator catalog rows or target index row are missing.")

    old_source = load(OLD_SOURCE)
    old_record = next(row for row in old_source.get("records", []) if row.get("spellId") == SPELL_ID)
    with ZipFile(PRIOR) as prior:
        previous_decision = load_from_zip(prior, "DIRECTOR_DECISION.json")
        prior_target = next(row for row in previous_decision.get("decisions", []) if row.get("id") == SPELL_ID)
        hold_register = load_from_zip(prior, "HOLD_REGISTER.json")
        prior_hold = next(row for row in hold_register.get("identityBlockers", []) if row.get("id") == BLOCKER)
        source_reassessment = load_from_zip(prior, "SOURCE_COMPARISON_248_TO_287.json")
        questions = load_from_zip(prior, "QUESTION_DISPOSITIONS.json")
        target_questions = [row for row in questions if SPELL_ID in row.get("originalQuestionUnchanged", {}).get("spellIds", [])]
        case_dispositions = load_from_zip(prior, "CASE_DISPOSITIONS.json")
        target_cases = [row for row in case_dispositions if row.get("spellId") == SPELL_ID]
        comparator_verification = load_from_zip(prior, "COMPARATOR_VERIFICATION.json")
        target_comparators = [row for row in comparator_verification.get("comparators", []) if row.get("id") in COMPARATORS]
        procedure = load_from_zip(prior, "procedures/alignment-ascension.json")
        cases = {
            ident: json.loads(prior.read(f"cases/{ident}.json"))
            for ident in ["AFP211-AA-effective-read", "AFP211-AA-protected-information"]
        }
        case_bindings = {
            ident: {"path": f"cases/{ident}.json", "bytes": len(prior.read(f"cases/{ident}.json")), "sha256": sha(prior.read(f"cases/{ident}.json")), "crc32": crc(prior.read(f"cases/{ident}.json"))}
            for ident in cases
        }
        prior_binding = bind(PRIOR)

    if {row.get("id") for row in target_cases} != {"AFP211-AA-effective-read", "AFP211-AA-protected-information"}:
        raise RuntimeError("Previous return does not contain the expected two Alignment Ascension cases.")
    if {row.get("id") for row in target_comparators} != set(COMPARATORS):
        raise RuntimeError("Previous comparator record is missing Alignment Avatar or Alignment Immunity.")

    core = load(CORE)
    core_rows = []
    def collect_core(node):
        if isinstance(node, dict):
            if node.get("name") == "Alignment Ascension":
                core_rows.append(node)
            for value in node.values():
                collect_core(value)
        elif isinstance(node, list):
            for value in node:
                collect_core(value)
    collect_core(core)
    if len(core_rows) != 2:
        raise RuntimeError(f"Expected both Alignment Ascension core placements, found {len(core_rows)}.")

    prior_bindings = {row["path"]: row for row in old_source.get("sourceBindings", [])}
    same, changed, missing = 0, [], []
    for previous in old_source.get("sourceBindings", []):
        path = ROOT / Path(previous["path"])
        if not path.is_file():
            missing.append(previous["path"])
            continue
        current = bind(path)
        if current.get("bytes") == previous.get("bytes") and current.get("sha256") == previous.get("sha256"):
            same += 1
        else:
            changed.append({"path": previous["path"], "old": {"bytes": previous.get("bytes"), "sha256": previous.get("sha256")}, "current": {"bytes": current["bytes"], "sha256": current["sha256"]}})
    source_diff = {
        "priorSourceBindingCount": len(old_source.get("sourceBindings", [])),
        "unchangedCount": same,
        "changed": changed,
        "missing": missing,
        "targetCurrentCatalogRowUnchanged": old_record.get("completeCurrentCatalogSourceAndAccess") == spell,
        "targetCurrentIndexRowUnchanged": old_record.get("currentIndexEntry") == index_row,
    }

    comparator_bindings = []
    for comparator in target_comparators:
        expected = comparator.get("indexEntry", {}).get("completeEnvelopeBinding", {})
        path = ROOT / Path(expected.get("path", ""))
        current = bind(path)
        model = load(path)
        pointer = comparator.get("indexEntry", {}).get("procedurePointer")
        current_procedure = pointer_get(model, pointer)
        previous_procedure = comparator.get("procedure")
        comparator_bindings.append({"id": comparator["id"], "priorProcedure": previous_procedure, "currentProcedure": current_procedure, "procedureExactUnchanged": current_procedure == previous_procedure, "comparisonScope": comparator.get("scope"), "procedurePointer": pointer, "priorEnvelopeBinding": expected, "currentEnvelopeBinding": current, "envelopeUnchanged": expected.get("bytes") == current["bytes"] and expected.get("sha256") == current["sha256"]})

    current_source_refs = {
        "catalog": bind(CATALOG),
        "index": bind(INDEX),
        "core": bind(CORE),
        "priorReturn287": prior_binding,
        "priorCurrentSourceCandidate287": bind(OLD_SOURCE),
        "sourceBindingSetReconciliation": source_diff,
    }
    payload = {
        "00_CURRENT_AUTHORITY_334.json": {
            "authority": queue["currentAuthority"],
            "queue": bind(QUEUE),
            "pendingAudit": bind(PENDING),
            "handoff": bind(HANDOFF),
            "activeReview": queue.get("activeReview"),
            "continuingPriorityOrder": queue.get("continuingPriorityOrder", []),
            "priorHeldSpellIds": queue.get("separatelyRetainedHolds", []),
        },
        "01_CURRENT_ALIGNMENT_ASCENSION_CATALOG_ROW.json": spell,
        "02_CURRENT_ALIGNMENT_ASCENSION_INDEX_ROW.json": index_row,
        "03_CURRENT_RELATED_COMPARATOR_CATALOG_ROWS.json": [current_rows[ident] for ident in RELATED_ROWS if ident != SPELL_ID],
        "04_CURRENT_CORE_ALIGNMENT_ASCENSION_ROWS.json": core_rows,
        "05_RETURN287_TARGET_DECISION_AND_HOLD.json": {
            "historicalAuthorityOnly": previous_decision.get("authorityBefore"),
            "targetDecision": prior_target,
            "identityHold": prior_hold,
            "priorArchiveBinding": prior_binding,
        },
        "06_RETURN287_SOURCE_REASSESSMENT.json": source_reassessment,
        "07_RETURN287_TARGET_QUESTION_DISPOSITIONS.json": target_questions,
        "08_RETURN287_TARGET_CASE_DISPOSITIONS.json": target_cases,
        "09_RETURN287_INCOMPLETE_PROCEDURE_PROPOSAL.json": procedure,
        "10_RETURN287_CONDITIONAL_CASES.json": {"caseBindings": case_bindings, "cases": cases, "notReplayed": True},
        "11_CURRENT_COMPARATOR_BOUNDARIES.json": comparator_bindings,
        "12_CURRENT_SOURCE_RECONCILIATION.json": current_source_refs,
    }
    for name, value in payload.items():
        (PACKET / name).write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    request = """# Director review request — Alignment Ascension / AFP211-B01

One identity only. Return334 designates Alignment Ascension / AFP211-B01 next. Queue334 is current at 823 reviewed/applied, 25 pending, zero accepted-unapplied; Return287’s 816/32 authority is historical only. The packet binds the exact current target catalog/index rows, both native Core placements, current Alignment Avatar/Alignment Immunity/Alignment Revelation rows, the previous target-specific hold, source reconciliation, and the two preserved conditional component cases.

Do not replay the two cases or the old five-identity group. They pass only as bounded conditional traces: one reads an existing Lock’s effective alignment without erasing underlying history; the other keeps undefined and protected information indeterminate. Neither is a paid Ascension, full transformation, or useful-insight encounter. Reconcile only whether current exact sources now supply AFP211-B01’s missing content: (1) an authorized useful energy-body form and identity/HP, defenses, abilities, occupancy/support, movement, senses, attacks, casting, gear and custody; (2) duration/concentration plus alignment change, incapacitation/death, suppression, dispel/replacement and safe end/return; and (3) a bounded useful divine-insight contract naming qualified subjects/fields, reach, update/action/resource cadence and protection/undefined-information behavior.

Alignment Avatar is a comparison source with its own exact profile; Alignment Immunity supplies a protected-axis boundary; neither transfers a form, power, duration, permission or cure to Alignment Ascension. Alignment Revelation is an analogy only, not a granted insight contract. Do not infer body statistics, alignment axes, targets, omniscience, permissions, actor facts or cosmology from any comparator. No user-selected authoring values for these missing contracts are present in this packet.

If current source text actually closes the full native positive promise and the required paid useful encounters, identify exact source anchors and provide only the minimal reversible result. Otherwise seal an exact one-identity HOLD with the smallest unresolved authoring/source decisions, accepted/applied/held IDs, application authorization, current authority/counts and next current pending priority. Keep conditional fixtures distinct from campaign or user-authored events. Do not alter canonical files. Attach a sealed ZIP and matching delivery JSON; no application without exact sealed authorization.
"""
    (OUT / "REQUEST_335.md").write_text(request, encoding="utf-8")

    members = []
    for path in sorted(PACKET.rglob("*")):
        if path.is_file():
            data = path.read_bytes()
            members.append({"path": path.relative_to(PACKET).as_posix(), "bytes": len(data), "sha256": sha(data), "crc32": crc(data)})
    save(PACKET / "MEMBER_MANIFEST.json", {"id": "ALIGNMENT-ASCENSION-REVIEW335-PAYLOAD-MANIFEST", "payloadMemberCount": len(members), "members": members})
    archive_members = [{"path": "REQUEST_335.md", "bytes": (OUT / "REQUEST_335.md").stat().st_size, "sha256": sha((OUT / "REQUEST_335.md").read_bytes()), "crc32": crc((OUT / "REQUEST_335.md").read_bytes())}]
    archive_members.extend({"path": path.relative_to(PACKET).as_posix(), "bytes": path.stat().st_size, "sha256": sha(path.read_bytes()), "crc32": crc(path.read_bytes())} for path in sorted(PACKET.rglob("*")) if path.is_file())
    with zipfile.ZipFile(ARCHIVE, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        archive.write(OUT / "REQUEST_335.md", "REQUEST_335.md")
        for path in sorted(PACKET.rglob("*")):
            if path.is_file():
                archive.write(path, path.relative_to(PACKET).as_posix())
    archive_bytes = ARCHIVE.read_bytes()
    with ZipFile(ARCHIVE) as archive:
        bad = archive.testzip()
        names = archive.namelist()
        if bad or len(names) != len(set(names)) or set(names) != {row["path"] for row in archive_members}:
            raise RuntimeError(f"Archive verification failed: {bad}; {len(names)} entries")
        for row in archive_members:
            data = archive.read(row["path"])
            if len(data) != row["bytes"] or sha(data) != row["sha256"] or crc(data) != row["crc32"]:
                raise RuntimeError(f"Archive member binding mismatch: {row['path']}")

    checks = {
        "current_authority_823_25_0": queue.get("currentAuthority") == {"reviewedApplied": 823, "pending": 25, "acceptedUnapplied": 0, "completeStandaloneProcedures": 547, "scopedInterfaces": 173},
        "director_selected_target": queue.get("next") == SPELL_ID and queue.get("activeReview", {}).get("blockerIds") == [BLOCKER],
        "current_target_rows": spell.get("id") == index_row.get("id") == SPELL_ID and spell.get("operational") is None,
        "current_rows_match_return287_source": source_diff["targetCurrentCatalogRowUnchanged"] and source_diff["targetCurrentIndexRowUnchanged"],
        "prior_exact_hold_and_missing_fields": prior_target.get("decision") == "HOLD" and prior_target.get("blockerIds") == [BLOCKER] and prior_target.get("completePositiveSpellWitness") is False and set(prior_hold.get("questions", [])) >= {"AA9-05", "AA9-06", "AA9-07", "AA9-08"},
        "prior_target_question_rows": {row.get("id") for row in target_questions} >= {"AFP9-01", "AA9-04", "AA9-05", "AA9-06", "AA9-07", "AA9-08"},
        "two_prior_cases_not_recast_as_complete": {row.get("id") for row in target_cases} == {"AFP211-AA-effective-read", "AFP211-AA-protected-information"} and all(row.get("completeSpellWitness") is False and row.get("dataReplay") == "PASS" for row in target_cases),
        "unaccepted_proposal_preserved": procedure.get("accepted") is False and procedure.get("applied") is False and procedure.get("held") is True and bool(procedure.get("unresolvedMandatoryFields")),
        "comparison_procedures_exact_and_not_transferred": len(comparator_bindings) == 2 and all(row.get("procedureExactUnchanged") for row in comparator_bindings) and all("no transfer" in row.get("comparisonScope", "").lower() for row in comparator_bindings),
        "source_bindings_readable": len(old_source.get("sourceBindings", [])) >= 100 and not missing,
        "archive_crc_and_manifest": bad is None and len(names) == len(archive_members),
    }
    if not all(checks.values()):
        raise RuntimeError("Review335 preparation failed: " + json.dumps(checks, ensure_ascii=False))

    delivery = {
        "id": "ALIGNMENT-ASCENSION-REVIEW335-DELIVERY",
        "archive": {"fileName": ARCHIVE.name, "bytes": len(archive_bytes), "sha256": sha(archive_bytes), "crc32": crc(archive_bytes)},
        "archiveMemberCount": len(archive_members),
        "payloadMemberCount": len(members) + 1,
        "exactAllowlist": sorted(row["path"] for row in archive_members),
        "members": archive_members,
        "targetId": SPELL_ID,
        "blockerId": BLOCKER,
        "authority": queue["currentAuthority"],
        "currentQueue": bind(QUEUE),
        "currentPendingAudit": bind(PENDING),
        "currentCatalog": bind(CATALOG),
        "currentIndex": bind(INDEX),
        "priorReturn287": prior_binding,
        "acceptedIds": [],
        "appliedIds": [],
        "canonicalMutation": False,
    }
    save(DELIVERY, delivery)
    audit = {
        "id": "ALIGNMENT-ASCENSION-REVIEW335-PREPARATION-AUDIT",
        "recordedAtUtc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "status": "PASS_PACKET_PREPARED_NOT_SENT",
        "checks": checks,
        "checkCount": len(checks),
        "passed": sum(checks.values()),
        "failed": sum(not value for value in checks.values()),
        "archive": delivery["archive"],
        "delivery": bind(DELIVERY),
        "authority": queue["currentAuthority"],
        "scope": [SPELL_ID],
        "canonicalFilesChanged": False,
        "applicationPerformed": False,
    }
    save(OUT / "PREPARATION_AUDIT_335.json", audit)
    print(json.dumps({"archive": str(ARCHIVE), **delivery["archive"], "delivery": str(DELIVERY), "checks": len(checks), "passed": sum(checks.values()), "failed": sum(not value for value in checks.values()), "priorSourceBindings": {"count": len(old_source.get("sourceBindings", [])), "unchanged": same, "changed": changed, "missing": missing}}, indent=2))


def load_from_zip(archive: ZipFile, member: str):
    return json.loads(archive.read(member))


if __name__ == "__main__":
    main()
