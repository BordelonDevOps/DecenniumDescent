#!/usr/bin/env python3
"""Prepare a current-authority, one-identity reassessment for AFP211-B02."""

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
OUT = A / "rank9_alignment_perfection_review_336_prepared"
PACKET = OUT / "packet"
ARCHIVE = OUT / "DD_Rank9_AlignmentPerfection_Review336.zip"
DELIVERY = OUT / "DD_Rank9_AlignmentPerfection_Review336_DELIVERY.json"
QUEUE = A / "CURRENT_SPELL_QUEUE_335.json"
PENDING = A / "CURRENT25_PENDING_IDENTITY_AUDIT_335.json"
HANDOFF = A / "CURRENT_HANDOFF_335.json"
CATALOG = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json"
INDEX = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json"
CORE = ROOT / "DescentReviewChanges/ReviewBible/data/public/Decennium_Descent_Core_Systems_Data_v2_Known_Descent.json"
OLD_SOURCE = A / "rank9_alignmentfactionpurification5_current_source_287_prepared/CURRENT_SOURCE_CONFERENCE_CANDIDATE_287.json"
PRIOR = A / "rank9_alignmentfactionpurification5_return287_received/DD_Rank9_AlignmentFactionPurification5_Director_Return287_HELD.zip"
RETURN335 = A / "rank9_alignment_ascension_return335_received/payload/COMPARATOR_SCOPE.json"
SPELL_ID = "alignment-perfection"
BLOCKER = "AFP211-B02"
APPLIED_ALIGNMENT_BOUNDARIES = ["alignment-lock", "alignment-anchor", "alignment-purge", "alignment-suggestion"]
TARGET_QUESTIONS = {"AP9-09", "AP9-10", "AP9-11", "AP9-12"}


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
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")


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


def load_from_zip(archive: ZipFile, member: str):
    return json.loads(archive.read(member))


def main() -> None:
    marker = OUT / "PREPARATION_AUDIT_336.json"
    if OUT.exists():
        if marker.exists() and load(marker).get("id") != "ALIGNMENT-PERFECTION-REVIEW336-PREPARATION-AUDIT":
            raise RuntimeError(f"Output marker belongs to another preparation; refusing to overwrite: {OUT}")
        if not marker.exists() and any(path.is_file() for path in OUT.rglob("*")):
            partial = PACKET / "00_CURRENT_AUTHORITY_335.json"
            if not partial.is_file() or load(partial).get("authority") != load(QUEUE).get("currentAuthority"):
                raise RuntimeError(f"Output contains files without this generator's preparation marker; refusing to overwrite: {OUT}")
    PACKET.mkdir(parents=True, exist_ok=True)

    queue, pending, handoff = load(QUEUE), load(PENDING), load(HANDOFF)
    catalog, index = load(CATALOG), load(INDEX)
    spell, index_row = find_id(catalog, SPELL_ID), find_id(index, SPELL_ID)
    immunity_index = find_id(index, "alignment-immunity")
    if spell is None or index_row is None or immunity_index is None:
        raise RuntimeError("Current Alignment Perfection or Alignment Immunity index rows are missing.")

    old_source = load(OLD_SOURCE)
    old_record = next(row for row in old_source.get("records", []) if row.get("spellId") == SPELL_ID)
    with ZipFile(PRIOR) as prior:
        previous_decision = load_from_zip(prior, "DIRECTOR_DECISION.json")
        prior_target = next(row for row in previous_decision.get("decisions", []) if row.get("id") == SPELL_ID)
        hold_register = load_from_zip(prior, "HOLD_REGISTER.json")
        prior_hold = next(row for row in hold_register.get("identityBlockers", []) if row.get("id") == BLOCKER)
        questions = load_from_zip(prior, "QUESTION_DISPOSITIONS.json")
        target_questions = [row for row in questions if row.get("id") in TARGET_QUESTIONS or row.get("id") in {"AFP9-01", "AFP9-02", "AFP9-03"}]
        case_dispositions = load_from_zip(prior, "CASE_DISPOSITIONS.json")
        target_cases = [row for row in case_dispositions if row.get("spellId") == SPELL_ID]
        procedure = load_from_zip(prior, "procedures/alignment-perfection.json")
        cases = {
            ident: json.loads(prior.read(f"cases/{ident}.json"))
            for ident in ["AFP211-AP-underlying-removal", "AFP211-AP-undefined-benefit"]
        }
        case_bindings = {
            ident: {"path": f"cases/{ident}.json", "bytes": len(prior.read(f"cases/{ident}.json")), "sha256": sha(prior.read(f"cases/{ident}.json")), "crc32": crc(prior.read(f"cases/{ident}.json"))}
            for ident in cases
        }
        prior_binding = bind(PRIOR)
        comparison_evidence = load_from_zip(prior, "COMPARISON_EVIDENCE.json")
        source_reassessment = load_from_zip(prior, "SOURCE_COMPARISON_248_TO_287.json")
        comparator_verification = load_from_zip(prior, "COMPARATOR_VERIFICATION.json")
        applied_rows = [row for row in old_source.get("completeAppliedCounterparts", []) if row.get("spellId") in APPLIED_ALIGNMENT_BOUNDARIES]

    return335_comparators = load(RETURN335)
    immunity_boundary = next(row for row in return335_comparators.get("exactEnvelopeComparisons", []) if row.get("id") == "alignment-immunity")
    current_rows = []
    for row in applied_rows:
        source = row.get("source", {})
        path = ROOT / Path(source.get("path", ""))
        current = bind(path)
        current_raw = path.read_bytes()
        normalized = current_raw.replace(b"\r\n", b"\n")
        model = load(path)
        current_card = pointer_get(model, row.get("pointer", ""))
        current_rows.append({
            "spellId": row["spellId"],
            "previousAppliedCounterpart": row,
            "currentSourceBinding": current,
            "lfNormalizedSourceBinding": {"bytes": len(normalized), "sha256": sha(normalized)},
            "sourceMatchesAfterLfNormalization": source.get("bytes") == len(normalized) and source.get("sha256") == sha(normalized),
            "currentCardExact": current_card == row.get("completeCurrentCard"),
            "pointer": row.get("pointer"),
            "scope": "Boundary comparison only; these procedures and permissions do not transfer to Alignment Perfection.",
        })

    core = load(CORE)
    core_rows = []
    def collect_core(node):
        if isinstance(node, dict):
            if node.get("name") == "Alignment Perfection":
                core_rows.append(node)
            for value in node.values():
                collect_core(value)
        elif isinstance(node, list):
            for value in node:
                collect_core(value)
    collect_core(core)
    if len(core_rows) != 1:
        raise RuntimeError(f"Expected one Alignment Perfection core placement, found {len(core_rows)}.")

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

    return335_boundary = {
        "source": RETURN335.relative_to(ROOT).as_posix(),
        "sourceBinding": bind(RETURN335),
        "closedEvidenceFinding": return335_comparators.get("closedEvidenceFinding"),
        "alignmentImmunity": immunity_boundary,
        "currentAlignmentImmunityIndexRow": immunity_index,
        "scope": "The accepted protected-component rule applies to actual alignment-dependent positive and negative effects; it is a boundary only and adds no Alignment Perfection benefit profile or permission.",
    }

    payload = {
        "00_CURRENT_AUTHORITY_335.json": {
            "authority": queue["currentAuthority"],
            "queue": bind(QUEUE),
            "pendingAudit": bind(PENDING),
            "handoff": bind(HANDOFF),
            "activeReview": queue.get("activeReview"),
            "continuingPriorityOrder": queue.get("continuingPriorityOrder", []),
            "priorHeldSpellIds": queue.get("separatelyRetainedHolds", []),
        },
        "01_CURRENT_ALIGNMENT_PERFECTION_CATALOG_ROW.json": spell,
        "02_CURRENT_ALIGNMENT_PERFECTION_INDEX_ROW.json": index_row,
        "03_CURRENT_CORE_ALIGNMENT_PERFECTION_ROW.json": core_rows[0],
        "04_RETURN287_TARGET_DECISION_AND_HOLD.json": {
            "historicalAuthorityOnly": previous_decision.get("authorityBefore"),
            "targetDecision": prior_target,
            "identityHold": prior_hold,
            "priorArchiveBinding": prior_binding,
        },
        "05_RETURN287_TARGET_SOURCE_PROPOSAL.json": {
            "previousSourceCandidateBinding": bind(OLD_SOURCE),
            "targetRecord": old_record,
            "sourceReassessment": source_reassessment,
            "unacceptedProcedureProposal": procedure,
            "closedComparatorEvidence": comparator_verification,
            "previousComparisonEvidence": comparison_evidence,
        },
        "06_RETURN287_TARGET_QUESTION_DISPOSITIONS.json": target_questions,
        "07_RETURN287_TARGET_CASE_DISPOSITIONS.json": target_cases,
        "08_RETURN287_CONDITIONAL_CASES.json": {"caseBindings": case_bindings, "cases": cases, "notReplayed": True},
        "09_CURRENT_APPLIED_ALIGNMENT_BOUNDARIES.json": current_rows,
        "10_CURRENT_ALIGNMENT_IMMUNITY_BOUNDARY.json": return335_boundary,
        "11_CURRENT_SOURCE_RECONCILIATION.json": {
            "catalog": bind(CATALOG),
            "index": bind(INDEX),
            "core": bind(CORE),
            "priorReturn287": prior_binding,
            "priorCurrentSourceCandidate287": bind(OLD_SOURCE),
            "sourceBindingSetReconciliation": source_diff,
        },
    }
    for name, value in payload.items():
        (PACKET / name).write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")

    request = """# Director review request — Alignment Perfection / AFP211-B02

One identity only. Return335 designates Alignment Perfection / AFP211-B02 next. Queue335 is current at 823 reviewed/applied, 25 pending, zero accepted-unapplied; Return287’s 816/32 authority is historical only. The packet binds the exact current target catalog/index/Core row, the prior target hold and unaccepted proposal, its four spell-specific question dispositions, source-set reconciliation, two preserved conditional components, the relevant applied Alignment Lock/Anchor/Purge/Suggestion boundaries, and Return335’s closed Alignment Immunity comparison.

Do not replay or re-audit either Return287 case, or reopen AFP211-E01. Those cases remain bounded components only: conditionally authorized removal of one imposed record leaves a protected Lock snapshot and oath history intact; a Neutral/undefined axis receives no invented benefit. Neither is a paid cast or complete positive encounter. Reconcile only whether current exact sources supply AFP211-B02’s unresolved content: (1) the exact imposed alignment alterations the spell may cleanse, who/what is eligible, and source-protection/Lock/Anchor interactions while retaining legitimate underlying conduct and oath history; (2) a complete useful benefit map for defined axis combinations, both Neutral labels, and undefined inputs, with actual effects, amounts, eligibility, costs/uses and stacking; and (3) a complete benefit lifecycle covering live/snapshot inputs, duration, suppression, ending/recast and no refill or recreation of removed history. Also test the native “Instantaneous” operation against the selected separate benefit clock without inventing durations.

Alignment Immunity’s protected-component scope, and the applied Lock/Anchor/Purge/Suggestion boundaries, are comparisons only. They supply no rank9 benefit values, new permission, cure, forced alignment conversion, or restoration of history. Preserve selected willing-recipient direction and exact native access. Do not infer Good/Lawful superiority, actors, missing facts, or user-selected mechanics. The packet contains no newly authorized benefit values.

If exact current sources close the full native promise and complete paid useful positive/adverse encounters, identify exact anchors and provide only a minimal reversible result. Otherwise seal a one-identity HOLD with the smallest unresolved authoring/source decisions, exact IDs and application authorization, authority/counts, and next current pending priority. Keep conditional fixtures distinct from campaign or user-authored events. Do not alter canonical files. Attach a sealed ZIP and matching delivery JSON; no application without exact sealed authorization.
"""
    (OUT / "REQUEST_336.md").write_text(request, encoding="utf-8", newline="\n")

    members = []
    for path in sorted(PACKET.rglob("*")):
        if path.is_file() and path.name != "MEMBER_MANIFEST.json":
            data = path.read_bytes()
            members.append({"path": path.relative_to(PACKET).as_posix(), "bytes": len(data), "sha256": sha(data), "crc32": crc(data)})
    save(PACKET / "MEMBER_MANIFEST.json", {"id": "ALIGNMENT-PERFECTION-REVIEW336-PAYLOAD-MANIFEST", "payloadMemberCount": len(members), "members": members})
    archive_members = []
    request_path = OUT / "REQUEST_336.md"
    data = request_path.read_bytes()
    archive_members.append({"path": request_path.name, "bytes": len(data), "sha256": sha(data), "crc32": crc(data)})
    archive_members.extend({"path": path.relative_to(PACKET).as_posix(), "bytes": path.stat().st_size, "sha256": sha(path.read_bytes()), "crc32": crc(path.read_bytes())} for path in sorted(PACKET.rglob("*")) if path.is_file())
    with zipfile.ZipFile(ARCHIVE, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        archive.write(request_path, request_path.name)
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

    expected_authority = {"reviewedApplied": 823, "pending": 25, "acceptedUnapplied": 0, "completeStandaloneProcedures": 547, "scopedInterfaces": 173}
    checks = {
        "current_authority_823_25_0": queue.get("currentAuthority") == expected_authority,
        "director_selected_target": queue.get("next") == SPELL_ID and queue.get("activeReview", {}).get("blockerIds") == [BLOCKER],
        "current_target_rows": spell.get("id") == index_row.get("id") == SPELL_ID and spell.get("operational") is None,
        "current_rows_match_return287_source": source_diff["targetCurrentCatalogRowUnchanged"] and source_diff["targetCurrentIndexRowUnchanged"],
        "prior_exact_hold_and_missing_fields": prior_target.get("decision") == "HOLD" and prior_target.get("blockerIds") == [BLOCKER] and prior_target.get("completePositiveSpellWitness") is False and set(prior_hold.get("questions", [])) == {"AP9-09", "AP9-10", "AP9-12"},
        "target_questions_preserved": TARGET_QUESTIONS <= {row.get("id") for row in target_questions},
        "two_prior_cases_not_recast_as_complete": {row.get("id") for row in target_cases} == {"AFP211-AP-underlying-removal", "AFP211-AP-undefined-benefit"} and all(row.get("completeSpellWitness") is False and row.get("dataReplay") == "PASS" for row in target_cases),
        "unaccepted_proposal_preserved": procedure.get("accepted") is False and procedure.get("applied") is False and procedure.get("held") is True and set(procedure.get("unresolvedMandatoryFields", [])) == set(prior_hold.get("missing", [])),
        "applied_alignment_comparators_exact_after_line_ending_normalization": len(current_rows) == 4 and all(row.get("sourceMatchesAfterLfNormalization") and row.get("currentCardExact") for row in current_rows),
        "immunity_comparator_current_and_closed": immunity_boundary.get("procedureExactMatch") is True and return335_comparators.get("closedEvidenceFinding", {}).get("status") == "CLOSED",
        "source_bindings_readable": len(old_source.get("sourceBindings", [])) == 130 and same == 129 and len(changed) == 1 and not missing and changed[0]["path"].endswith("authored_review_index.json"),
        "archive_crc_and_manifest": bad is None and len(names) == len(archive_members),
    }
    if not all(checks.values()):
        raise RuntimeError("Review336 preparation failed: " + json.dumps(checks, ensure_ascii=False))

    delivery = {
        "id": "ALIGNMENT-PERFECTION-REVIEW336-DELIVERY",
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
        "precedingReturn335ComparatorBoundary": bind(RETURN335),
        "acceptedIds": [],
        "appliedIds": [],
        "canonicalMutation": False,
    }
    save(DELIVERY, delivery)
    audit = {
        "id": "ALIGNMENT-PERFECTION-REVIEW336-PREPARATION-AUDIT",
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
    save(marker, audit)
    print(json.dumps({"archive": str(ARCHIVE), **delivery["archive"], "delivery": str(DELIVERY), "checks": len(checks), "passed": sum(checks.values()), "failed": sum(not value for value in checks.values()), "priorSourceBindings": {"count": len(old_source.get("sourceBindings", [])), "unchanged": same, "changed": changed, "missing": missing}}, indent=2))


if __name__ == "__main__":
    main()
