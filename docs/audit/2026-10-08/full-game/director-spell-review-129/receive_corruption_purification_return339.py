#!/usr/bin/env python3
"""Independently verify Return339 and advance the Director-prioritized queue."""
from __future__ import annotations

import hashlib
import json
import shutil
import zlib
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath
from zipfile import ZipFile

A = Path(__file__).resolve().parent
ROOT = A.parents[4]
PREP = A / "rank9_corruption_purification_review_339_prepared"
PREP_ZIP = PREP / "DD_Rank9_CorruptionPurification_Review339.zip"
PREP_DELIVERY = PREP / "DD_Rank9_CorruptionPurification_Review339_DELIVERY.json"
DOWNLOADS = Path.home() / "Downloads"
IN_ZIP = DOWNLOADS / "DD_CorruptionPurification_Director_Return339_HELD.zip"
IN_DELIVERY = DOWNLOADS / "DD_CorruptionPurification_Director_Return339_HELD_DELIVERY.json"
RECEIVED = A / "rank9_corruption_purification_return339_received"
PAYLOAD = RECEIVED / "payload"
ARCHIVE = RECEIVED / IN_ZIP.name
DELIVERY = RECEIVED / IN_DELIVERY.name
AUDIT = A / "CORRUPTION_PURIFICATION_RETURN339_INDEPENDENT_AUDIT.json"
RECEIPT = A / "CORRUPTION_PURIFICATION_RETURN339_RECEIPT.json"
QUEUE = A / "CURRENT_SPELL_QUEUE_339.json"
PENDING = A / "CURRENT25_PENDING_IDENTITY_AUDIT_339.json"
HANDOFF = A / "CURRENT_HANDOFF_339.json"
SNAPSHOT = A / "CURRENT_SPELL_REVIEW_SNAPSHOT_339.md"
CATALOG = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json"
INDEX = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json"
CORE = ROOT / "DescentReviewChanges/ReviewBible/data/public/Decennium_Descent_Core_Systems_Data_v2_Known_Descent.json"

AUTHORITY = {
    "reviewedApplied": 823,
    "pending": 25,
    "acceptedUnapplied": 0,
    "completeStandaloneProcedures": 547,
    "scopedInterfaces": 173,
}
SPELL = "corruption-purification"
BLOCKER = "AFP211-B05"
NEXT = "astral-projection"
NEXT_BLOCKER = "PC232-B01"
NEXT_GROUP = "rank9-projection-confinement2"
checks: list[dict] = []


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def crc(data: bytes) -> str:
    return f"{zlib.crc32(data) & 0xFFFFFFFF:08x}"


def bind(path: Path) -> dict:
    data = path.read_bytes()
    return {
        "path": path.relative_to(ROOT).as_posix(),
        "bytes": len(data),
        "sha256": sha(data),
        "crc32": crc(data),
    }


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def save(path: Path, value) -> None:
    path.write_text(
        json.dumps(value, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def check(check_id: str, passed: bool, detail: str) -> None:
    checks.append({"id": check_id, "passed": bool(passed), "detail": detail})


def safe_name(name: str) -> bool:
    p = PurePosixPath(name)
    return (
        bool(name)
        and not p.is_absolute()
        and ".." not in p.parts
        and "\\" not in name
        and ":" not in name
        and not name.startswith("/")
    )


def find_id(node, ident: str):
    if isinstance(node, dict):
        if node.get("id") == ident:
            return node
        for value in node.values():
            found = find_id(value, ident)
            if found is not None:
                return found
    elif isinstance(node, list):
        for value in node:
            found = find_id(value, ident)
            if found is not None:
                return found
    return None


def all_core_rows(node, name: str, found=None):
    found = [] if found is None else found
    if isinstance(node, dict):
        if node.get("name") == name:
            found.append(node)
        for value in node.values():
            all_core_rows(value, name, found)
    elif isinstance(node, list):
        for value in node:
            all_core_rows(value, name, found)
    return found


def main() -> None:
    if not IN_ZIP.is_file() or not IN_DELIVERY.is_file():
        raise FileNotFoundError("Primary Return339 ZIP or DELIVERY download is missing.")
    RECEIVED.mkdir(parents=True, exist_ok=True)
    if IN_ZIP.resolve() != ARCHIVE.resolve():
        shutil.copyfile(IN_ZIP, ARCHIVE)
    if IN_DELIVERY.resolve() != DELIVERY.resolve():
        shutil.copyfile(IN_DELIVERY, DELIVERY)

    archive_bytes = ARCHIVE.read_bytes()
    delivery_bytes = DELIVERY.read_bytes()
    delivery = json.loads(delivery_bytes)
    expected_archive = delivery.get("archive", {})
    check(
        "delivery-identity",
        delivery.get("id") == "CORRUPTION-PURIFICATION-DIRECTOR-RETURN339-DELIVERY"
        and delivery.get("reviewId") == "Return339",
        "Return339 delivery identity.",
    )
    check(
        "archive-name-size-sha-crc",
        expected_archive.get("fileName") == ARCHIVE.name
        and (
            expected_archive.get("bytes"),
            expected_archive.get("sha256"),
            expected_archive.get("crc32"),
        )
        == (len(archive_bytes), sha(archive_bytes), crc(archive_bytes)),
        json.dumps(expected_archive, ensure_ascii=False),
    )
    check(
        "single-target-hold-no-accept-or-apply",
        delivery.get("heldIds") == [SPELL]
        and delivery.get("blockerIds") == [BLOCKER]
        and delivery.get("acceptedIds") == []
        and delivery.get("appliedIds") == [],
        "Corruption Purification / AFP211-B05 only.",
    )
    check(
        "application-not-authorized",
        delivery.get("applicationAuthorization")
        == {"authorized": False, "authorizedIds": [], "canonicalMutationAuthorized": False},
        "Director did not authorize application or canonical mutation.",
    )
    check("authority-unchanged", delivery.get("authority") == AUTHORITY, repr(delivery.get("authority")))
    check(
        "next-priority-exact",
        delivery.get("nextPendingIdentity") == NEXT
        and delivery.get("nextBlockerId") == NEXT_BLOCKER
        and delivery.get("nextPendingGroup") == NEXT_GROUP,
        "Astral Projection / PC232-B01 is next.",
    )
    seal = delivery.get("sealVerification", {})
    seal_checks = seal.get("checks", [])
    check(
        "director-seal-claims-pass",
        seal.get("checksPassed") == 81
        and seal.get("checksFailed") == 0
        and len(seal_checks) == 81
        and all(row.get("status") == "PASS" for row in seal_checks),
        "Director reports 81/81 seal checks passing.",
    )

    with ZipFile(ARCHIVE) as z:
        names = z.namelist()
        name_set = set(names)
        unsafe = [name for name in names if not safe_name(name)]
        check(
            "zip-crc-and-safe-unique-names",
            z.testzip() is None and len(names) == len(name_set) == 39 and not unsafe,
            f"members={len(names)}; unsafe={unsafe[:3]}",
        )
        external_rows = delivery.get("members", [])
        external_map = {row.get("path"): row for row in external_rows}
        check(
            "external-roster-and-allowlist",
            len(external_rows) == len(external_map) == 39
            and delivery.get("archiveMemberCount") == 39
            and delivery.get("payloadMemberCount") == 38
            and delivery.get("exactAllowlist") == names == list(external_map),
            f"delivery={len(external_rows)} ZIP={len(names)}",
        )
        external_ok = True
        for row in external_rows:
            member = row["path"]
            data = z.read(member)
            external_ok &= (len(data), sha(data), crc(data)) == (
                row.get("bytes"), row.get("sha256"), row.get("crc32")
            )
        check("all-external-member-bindings", external_ok, "Every DELIVERY size/SHA/CRC matches its exact ZIP member.")

        root_manifest = json.loads(z.read("MEMBER_MANIFEST.json"))
        root_rows = root_manifest.get("members", [])
        root_ok = (
            root_manifest.get("id") == "CORRUPTION-PURIFICATION-DIRECTOR-RETURN339-PAYLOAD-MANIFEST"
            and root_manifest.get("payloadMemberCount") == 38
            and root_manifest.get("archiveMemberCount") == 39
            and root_manifest.get("exactPayloadAllowlist") == [n for n in names if n != "MEMBER_MANIFEST.json"]
            and len(root_rows) == 38
        )
        for row in root_rows:
            member = row.get("path", "")
            if member not in name_set or member == "MEMBER_MANIFEST.json":
                root_ok = False
                continue
            data = z.read(member)
            root_ok &= (len(data), sha(data), crc(data)) == (
                row.get("bytes"), row.get("sha256"), row.get("crc32")
            )
        check("root-manifest-exact-payload", root_ok, "The root manifest binds all 38 payload members.")

        nested = json.loads(z.read("evidence/MEMBER_MANIFEST.json"))
        nested_rows = nested.get("members", [])
        nested_archive_names = {
            n[len("evidence/") :]
            for n in names
            if n.startswith(("evidence/context/", "evidence/input/", "evidence/sources/"))
        }
        nested_ok = (
            nested.get("id") == "CORRUPTION-PURIFICATION-REVIEW339-PAYLOAD-MANIFEST"
            and nested.get("payloadMemberCount") == 22
            and {row.get("path") for row in nested_rows} == nested_archive_names
            and len(nested_rows) == 22
        )
        for row in nested_rows:
            member = "evidence/" + row.get("path", "")
            if member not in name_set:
                nested_ok = False
                continue
            data = z.read(member)
            nested_ok &= (len(data), sha(data), crc(data)) == (
                row.get("bytes"), row.get("sha256"), row.get("crc32")
            )
        check("nested-source-manifest-exact", nested_ok, "The nested manifest binds 22 prepared source/context members.")

        decision = json.loads(z.read("DIRECTOR_DECISION.json"))
        counts = json.loads(z.read("COUNTS.json"))
        hold = json.loads(z.read("HOLD_REGISTER.json"))
        coverage = json.loads(z.read("CASE_COVERAGE.json"))
        procedure = json.loads(z.read("PROCEDURE_STATUS.json"))
        queue_status = json.loads(z.read("QUEUE_STATUS.json"))
        source_rec = json.loads(z.read("SOURCE_RECONCILIATION.json"))
        semantic = json.loads(z.read("SEMANTIC_RECONCILIATION.json"))
        questions = json.loads(z.read("QUESTION_DISPOSITIONS.json"))
        validation = json.loads(z.read("VALIDATION.json"))

        check(
            "sealed-director-decision",
            decision.get("reviewedIds") == [SPELL]
            and decision.get("heldIds") == [SPELL]
            and decision.get("acceptedIds") == []
            and decision.get("appliedIds") == []
            and decision.get("applicationAuthorization") == delivery.get("applicationAuthorization")
            and decision.get("canonicalMutation") is False,
            "One identity held; no application or canonical mutation.",
        )
        decisions = decision.get("decisions", [])
        check(
            "decision-blocker-and-reason",
            len(decisions) == 1
            and decisions[0].get("id") == SPELL
            and decisions[0].get("decision") == "HOLD"
            and decisions[0].get("blockerIds") == [BLOCKER],
            "One decision: Corruption Purification / AFP211-B05.",
        )
        requirements = hold.get("requirements", [])
        requirement_ids = [r.get("id") for r in requirements]
        check(
            "three-open-return339-contracts",
            hold.get("spellId") == SPELL
            and hold.get("blockerId") == BLOCKER
            and hold.get("status") == "OPEN"
            and requirement_ids == ["AFP339-W01", "AFP339-W02", "AFP339-W03"]
            and all(r.get("status") == "OPEN" for r in requirements),
            "W01 category/protection/dependency; W02 admission/geometry; W03 permanent/Until Dispelled.",
        )
        check(
            "exact-scoped-question-dispositions",
            questions.get("scope") == SPELL
            and {r.get("id") for r in questions.get("records", [])}
            == {"CP9-22", "CP9-23", "CP9-24", "CP9-25", "CP9-26", "AFP9-27"},
            "Only five target-specific questions and AFP9-27 are dispositioned.",
        )
        check(
            "conditional-cases-preserved-unreplayed",
            coverage.get("spellId") == SPELL
            and {r.get("id") for r in coverage.get("preservedComponents", [])}
            == {"AFP211-CP-ordinary-removal", "AFP211-CP-new-exposure"}
            and all(
                r.get("currentStatus") == "PRESERVED_NOT_REPLAYED_OR_REAUDITED"
                and r.get("completePaidSpellWitness") is False
                and r.get("clockStatus") == "NOT_DEMONSTRATED"
                for r in coverage.get("preservedComponents", [])
            )
            and coverage.get("freshCaseReplays") == 0
            and coverage.get("freshCaseReaudits") == 0
            and coverage.get("newIntegratedCases") == 0,
            "Both prior conditional components retained without replay or promotion.",
        )
        check(
            "no-new-witness-or-rules",
            counts.get("completePaidUsefulWitnesses") == 0
            and counts.get("requiredPaidUsefulWitnesses") == 2
            and counts.get("freshForwardOperations") == 0
            and counts.get("freshInverseOperations") == 0
            and counts.get("freshClockChecks") == 0
            and counts.get("newGameRules") == 0,
            "Two paid useful witnesses remain absent; no cases or rules were added.",
        )
        closed = decision.get("closedEvidenceFinding", {})
        check(
            "closed-evidence-and-comparator-boundaries",
            closed == {"id": "AFP211-E01", "status": "CLOSED", "reopened": False}
            and counts.get("closedComparatorScopesRetained") == 6
            and counts.get("comparatorCasesReplayed") == 0,
            "AFP211-E01 remains closed; comparator cases were not replayed.",
        )
        native = procedure.get("nativeCard", {})
        check(
            "procedure-incomplete-and-nonoperational",
            procedure.get("id") == SPELL
            and procedure.get("status") == "SOURCE_BOUND_INCOMPLETE_NOT_OPERATIONAL"
            and procedure.get("accepted") is False
            and procedure.get("applied") is False
            and procedure.get("completeOperationalProcedure") is False
            and native.get("operational") is None,
            "Native procedure remains incomplete and operational=null.",
        )
        current_pending = load(A / "CURRENT25_PENDING_IDENTITY_AUDIT_338.json").get("pendingIds", [])
        check(
            "queue-authority-and-pending-set",
            queue_status.get("authority") == AUTHORITY
            and set(queue_status.get("pendingIds", [])) == set(current_pending)
            and len(current_pending) == 25
            and queue_status.get("remainingClosureTasks") == 25
            and queue_status.get("firstReviewTasks") == 0
            and queue_status.get("canonicalQueueUpdated") is False
            and queue_status.get("nextPendingIdentity") == NEXT
            and queue_status.get("nextBlockerId") == NEXT_BLOCKER
            and queue_status.get("nextPendingGroup") == NEXT_GROUP,
            "25 pending identities preserved; first-review count zero; Director next priority exact.",
        )
        check(
            "counts-and-semantic-hold",
            counts.get("authority") == AUTHORITY
            and counts.get("reviewedIdentities") == 1
            and counts.get("acceptedIdentities") == 0
            and counts.get("appliedIdentities") == 0
            and counts.get("heldIdentities") == 1
            and counts.get("sourceDataChecksPassed") == 91
            and counts.get("sourceDataChecksFailed") == 0
            and counts.get("semanticPasses") == 6
            and counts.get("semanticHeldFindings") == 3
            and semantic.get("result") == "HOLD",
            "Director's 91 source/data checks and 6-pass/3-held semantic result retained.",
        )
        validation_checks = validation.get("checks", [])
        check(
            "reported-validation-record",
            validation.get("status") == "PASS"
            and validation.get("checkCount") == 91
            and validation.get("passed") == 91
            and validation.get("failed") == 0
            and len(validation_checks) == 91
            and all(row.get("status") == "PASS" for row in validation_checks),
            "The returned validation record is internally consistent (91/91).",
        )

        # Verify that the submitted Review339 packet and its exact DELIVERY are the ones returned.
        source_packet = source_rec.get("sourcePacket", {})
        source_delivery = source_rec.get("sourceDelivery", {})
        check(
            "source-review339-packet-binding",
            source_packet.get("fileName") == PREP_ZIP.name
            and (source_packet.get("bytes"), source_packet.get("sha256"), source_packet.get("crc32"))
            == (PREP_ZIP.stat().st_size, sha(PREP_ZIP.read_bytes()), crc(PREP_ZIP.read_bytes()))
            and source_delivery.get("fileName") == PREP_DELIVERY.name
            and (source_delivery.get("bytes"), source_delivery.get("sha256"), source_delivery.get("crc32"))
            == (PREP_DELIVERY.stat().st_size, sha(PREP_DELIVERY.read_bytes()), crc(PREP_DELIVERY.read_bytes())),
            "Return binds the exact pushed Review339 ZIP and DELIVERY.",
        )
        check(
            "embedded-review339-delivery-exact",
            z.read("evidence/REVIEW339_DELIVERY_AS_RECEIVED.json") == PREP_DELIVERY.read_bytes(),
            "Embedded Review339 DELIVERY is byte-identical to the packet sent to the Director.",
        )

        # The packet context/input pair is validated against the sent Review339 archive and checkout.
        context_map = {
            "context/CURRENT25_PENDING_IDENTITY_AUDIT_338.json": A / "CURRENT25_PENDING_IDENTITY_AUDIT_338.json",
            "context/CURRENT_HANDOFF_338.json": A / "CURRENT_HANDOFF_338.json",
            "context/CURRENT_SPELL_QUEUE_338.json": A / "CURRENT_SPELL_QUEUE_338.json",
            "context/CURRENT_SPELL_REVIEW_SNAPSHOT_338.md": A / "CURRENT_SPELL_REVIEW_SNAPSHOT_338.md",
        }
        prepared_root = PREP / "packet"
        context_ok = all(
            z.read("evidence/" + name) == path.read_bytes()
            and (prepared_root / name).read_bytes() == path.read_bytes()
            for name, path in context_map.items()
        )
        input_names = [
            "00_CURRENT_AUTHORITY_338.json",
            "01_CURRENT_CORRUPTION_PURIFICATION_CATALOG_ROW.json",
            "02_CURRENT_CORRUPTION_PURIFICATION_INDEX_ROW.json",
            "03_CURRENT_CORE_CORRUPTION_PURIFICATION_ROW.json",
            "04_RETURN287_TARGET_DECISION_AND_HOLD.json",
            "05_RETURN287_TARGET_SOURCE_PROPOSAL.json",
            "06_RETURN287_TARGET_QUESTION_DISPOSITIONS.json",
            "07_RETURN287_TARGET_CASE_DISPOSITIONS.json",
            "08_RETURN287_PRESERVED_CONDITIONAL_CASES.json",
            "09_CLOSED_COMPARATOR_BOUNDARY.json",
            "10_PRIOR_RETURNS_AND_CURRENT_HOLDS.json",
            "11_CURRENT_SOURCE_RECONCILIATION.json",
        ]
        context_ok &= all(
            z.read("evidence/input/" + name) == (prepared_root / "input" / name).read_bytes()
            for name in input_names
        )
        check("prepared-context-and-input-pairs", context_ok, "All 16 context and target/history inputs match the submitted packet.")

        # Check every embedded full source against this checkout and the exact submitted packet member.
        source_rows = source_rec.get("embeddedSourcesVerified", [])
        sources_ok = len(source_rows) == 6
        with ZipFile(PREP_ZIP) as submitted:
            for row in source_rows:
                live = ROOT / row["path"]
                member = "evidence/sources/" + Path(row["packetMember"]).name
                sent_member = "sources/" + Path(row["packetMember"]).name
                data = live.read_bytes() if live.is_file() else b""
                sources_ok &= (
                    live.is_file()
                    and data == z.read(member) == submitted.read(sent_member)
                    and (len(data), sha(data), crc(data))
                    == (row.get("bytes"), row.get("sha256"), row.get("crc32"))
                )
        check("six-current-full-source-bindings", sources_ok, "All six full source documents match checkout and submitted Review339 members.")

        full_rows = source_rec.get("fullCurrentFilesVerified", [])
        full_ok = len(full_rows) == 3
        for row in full_rows:
            live = ROOT / row["path"]
            data = live.read_bytes() if live.is_file() else b""
            full_ok &= live.is_file() and (len(data), sha(data), crc(data)) == (
                row.get("bytes"), row.get("sha256"), row.get("crc32")
            )
        check("three-current-full-source-files", full_ok, "Current catalog, authored index and Core full-file bindings verified.")

        live_catalog = load(CATALOG)
        live_index = load(INDEX)
        live_core = load(CORE)
        cat_row = json.loads(z.read("evidence/input/01_CURRENT_CORRUPTION_PURIFICATION_CATALOG_ROW.json"))
        idx_row = json.loads(z.read("evidence/input/02_CURRENT_CORRUPTION_PURIFICATION_INDEX_ROW.json"))
        core_row = json.loads(z.read("evidence/input/03_CURRENT_CORE_CORRUPTION_PURIFICATION_ROW.json"))
        check(
            "exact-target-catalog-index-core-rows",
            cat_row == find_id(live_catalog, SPELL)
            and idx_row == find_id(live_index, SPELL)
            and all_core_rows(live_core, "Corruption Purification") == [core_row],
            "Embedded Corruption Purification rows match the exact current catalog/index/Core entries.",
        )

        current_source_reconciliation = json.loads(z.read("evidence/input/11_CURRENT_SOURCE_RECONCILIATION.json"))
        check(
            "source-reconciliation-indexed-row-claims",
            current_source_reconciliation.get("targetExactCatalogRowComparedToReturn287") is True
            and current_source_reconciliation.get("targetExactIndexRowComparedToReturn287") is True
            and len(current_source_reconciliation.get("sourceSetBindings", [])) == 6
            and len(current_source_reconciliation.get("fullCurrentSourceFilesVerified", [])) == 3,
            "Return339 source reconciliation records six source-set bindings and exact target comparisons.",
        )

        prior = json.loads(z.read("evidence/input/10_PRIOR_RETURNS_AND_CURRENT_HOLDS.json"))
        prior_ok = set(prior) == {"return336", "return337", "return338", "scope"}
        for return_key, folder, filename in [
            ("return336", "rank9_alignment_perfection_return336_received", "DD_AlignmentPerfection_Director_Return336_HELD.zip"),
            ("return337", "rank9_faction_incarnate_return337_received", "DD_FactionIncarnate_Director_Return337_HELD.zip"),
            ("return338", "rank9_faction_perfection_return338_received", "DD_FactionPerfection_Director_Return338_HELD.zip"),
        ]:
            old = prior.get(return_key, {})
            archive = A / folder / filename
            data = archive.read_bytes() if archive.is_file() else b""
            ref = old.get("archive", {})
            prior_ok &= archive.is_file() and (len(data), sha(data), crc(data)) == (
                ref.get("bytes"), ref.get("sha256"), ref.get("crc32")
            )
            prior_ok &= bool(old.get("heldIds")) and old.get("closedEvidenceFinding") == {
                "id": "AFP211-E01", "status": "CLOSED", "reopened": False
            }
        check("prior-return336-338-bindings-and-e01", prior_ok, "Return336/337/338 archives and hold/E01 records remain bound and unchanged.")

    if any(not row["passed"] for row in checks):
        raise RuntimeError("Return339 independent verification failed: " + json.dumps([c for c in checks if not c["passed"]]))

    # Extraction occurs only after every archive and source check has passed.
    with ZipFile(ARCHIVE) as z:
        for name in sorted(n for n in z.namelist() if n != "MEMBER_MANIFEST.json"):
            dst = PAYLOAD.joinpath(*PurePosixPath(name).parts)
            dst.parent.mkdir(parents=True, exist_ok=True)
            dst.write_bytes(z.read(name))

    timestamp = datetime.now(timezone.utc).isoformat(timespec="seconds")
    archive_ref = bind(ARCHIVE)
    delivery_ref = bind(DELIVERY)
    decision_path = PAYLOAD / "DIRECTOR_DECISION.json"
    hold_path = PAYLOAD / "HOLD_REGISTER.json"
    audit = {
        "id": "CORRUPTION-PURIFICATION-RETURN339-INDEPENDENT-AUDIT",
        "recordedAtUtc": timestamp,
        "status": "PASS_RETURN339_SEALED_HOLD_AFP211_B05",
        "archive": archive_ref,
        "delivery": delivery_ref,
        "archiveMemberCount": 39,
        "checks": checks,
        "checkCount": len(checks),
        "passed": sum(row["passed"] for row in checks),
        "failed": sum(not row["passed"] for row in checks),
        "decision": "HOLD",
        "acceptedIds": [],
        "appliedIds": [],
        "heldIds": [SPELL],
        "applicationAuthorizedIds": [],
        "authority": AUTHORITY,
        "openContractIds": ["AFP339-W01", "AFP339-W02", "AFP339-W03"],
        "closedEvidenceFinding": "AFP211-E01",
        "nextIdentity": NEXT,
        "nextBlockerIds": [NEXT_BLOCKER],
        "canonicalFilesChanged": False,
        "applicationPerformed": False,
    }
    save(AUDIT, audit)
    receipt = {
        "id": "CORRUPTION-PURIFICATION-RETURN339-RECEIPT",
        "recordedAtUtc": timestamp,
        "decision": "HOLD",
        "blockerIds": [BLOCKER],
        "archive": archive_ref,
        "delivery": delivery_ref,
        "directorDecision": bind(decision_path),
        "holdRegister": bind(hold_path),
        "independentAudit": bind(AUDIT),
        "acceptedIds": [],
        "appliedIds": [],
        "heldIds": [SPELL],
        "applicationAuthorizedIds": [],
        "openContractIds": ["AFP339-W01", "AFP339-W02", "AFP339-W03"],
        "closedEvidenceFinding": "AFP211-E01",
        "authority": AUTHORITY,
        "nextIdentity": NEXT,
        "nextBlockerIds": [NEXT_BLOCKER],
        "nextGroup": NEXT_GROUP,
        "canonicalFilesChanged": False,
        "applicationPerformed": False,
    }
    save(RECEIPT, receipt)

    previous_queue = load(A / "CURRENT_SPELL_QUEUE_338.json")
    previous_pending = load(A / "CURRENT25_PENDING_IDENTITY_AUDIT_338.json")
    previous_handoff = load(A / "CURRENT_HANDOFF_338.json")
    retained = sorted(
        set(previous_queue.get("separatelyRetainedHolds", []))
        | set(previous_queue.get("currentReturnHeldIds", []))
        | {SPELL}
    )
    audit_ref = bind(AUDIT)
    receipt_ref = bind(RECEIPT)
    decision_ref = bind(decision_path)

    queue = dict(previous_queue)
    queue.update(
        {
            "id": "SPELL-REVIEW-QUEUE-339",
            "recordedAtUtc": timestamp,
            "supersedesQueue": bind(A / "CURRENT_SPELL_QUEUE_338.json"),
            "currentAuthority": AUTHORITY,
            "pendingCount": 25,
            "acceptedUnapplied": 0,
            "closureTasksRemaining": 25,
            "firstReviewTasksRemaining": 0,
            "nextGroup": NEXT_GROUP,
            "next": NEXT,
            "nextPendingIds": [NEXT],
            "nextPendingCount": 1,
            "heldThisStep": [SPELL],
            "separatelyRetainedHolds": retained,
            "pendingIdentityAudit": PENDING.relative_to(ROOT).as_posix(),
            "currentHandoff": HANDOFF.relative_to(ROOT).as_posix(),
            "currentPacket": None,
            "currentPacketStatus": "RETURN339_CORRUPTION_PURIFICATION_HELD_ASTRAL_PROJECTION_PC232_B01_NEXT",
            "activeReview": {"spellId": NEXT, "blockerIds": [NEXT_BLOCKER], "packet": None, "status": "DIRECTOR_RETURN339_NEXT_PRIORITY"},
            "currentReturn": receipt_ref,
            "currentReturnReceipt": receipt_ref,
            "currentReturnArchive": archive_ref,
            "currentReturnDelivery": delivery_ref,
            "currentReturnAudit": audit_ref,
            "currentReturnDecision": decision_ref,
            "currentReturnAcceptedIds": [],
            "currentReturnAppliedIds": [],
            "currentReturnHeldIds": [SPELL],
            "currentReturnBlockers": {**previous_queue.get("currentReturnBlockers", {}), SPELL: [BLOCKER]},
            "currentDirectorInstruction": "Return339 holds Corruption Purification / AFP211-B05. AFP339-W01 category/protection/dependency matrix, W02 exact creature/environment admission and occupied area geometry, and W03 completed permanent removal versus Until Dispelled remain open. Two paid useful creature/area cure witnesses are still required; prior conditional cases remain unreplayed and AFP211-E01 stays closed. No application is authorized. Next Director priority: Astral Projection / PC232-B01.",
            "directorConnectionStatus": "Return339 independently verified. Corruption Purification remains held; next is Astral Projection / PC232-B01.",
            "applicationPerformed": False,
            "canonicalFilesChanged": False,
            "githubChanges": False,
        }
    )
    save(QUEUE, queue)

    pending = dict(previous_pending)
    pending.update(
        {
            "id": "SPELL-REVIEW-CURRENT25-PENDING-IDENTITY-AUDIT-339",
            "recordedAtUtc": timestamp,
            "status": "PASS_CURRENT_823_25_RETURN339_CORRUPTION_PURIFICATION_HOLD_ASTRAL_PROJECTION_NEXT",
            "supersedes": (A / "CURRENT25_PENDING_IDENTITY_AUDIT_338.json").name,
            "authority": AUTHORITY,
            "pendingCount": 25,
            "acceptedIds": [],
            "appliedIds": [],
            "heldThisStep": [SPELL],
            "separatelyHeldIds": retained,
            "nextGroup": NEXT_GROUP,
            "nextIdentity": NEXT,
            "nextBlockerIds": [NEXT_BLOCKER],
            "nextPendingIds": [NEXT],
            "nextPendingCount": 1,
            "nextStep": "Review Astral Projection / PC232-B01 from current exact catalog/index/Core sources. Preserve Return336/337/338/339 holds and AFP211-E01 closed; apply only an exact sealed acceptance.",
            "sourceQueue": QUEUE.relative_to(ROOT).as_posix(),
            "currentQueueBinding": bind(QUEUE),
            "currentReturn": receipt_ref,
            "currentReturnDelivery": delivery_ref,
            "currentReturnAudit": audit_ref,
            "currentReturnReceipt": receipt_ref,
            "noPendingTargetSilentlyAccepted": True,
            "allCurrentPendingIdentitiesReviewed": True,
            "unreviewedPendingIds": [],
            "canonicalFilesChanged": False,
            "applicationPerformed": False,
        }
    )
    save(PENDING, pending)

    handoff = dict(previous_handoff)
    handoff.update(
        {
            "id": "CURRENT-HANDOFF-339",
            "recordedAtUtc": timestamp,
            "supersedes": (A / "CURRENT_HANDOFF_338.json").name,
            "status": "RETURN339_VERIFIED_CORRUPTION_PURIFICATION_HELD_ASTRAL_PROJECTION_NEXT_823_25_0",
            "authority": AUTHORITY,
            "queue": QUEUE.relative_to(ROOT).as_posix(),
            "queueBinding": bind(QUEUE),
            "pendingIdentityAudit": PENDING.name,
            "pendingIdentityAuditBinding": bind(PENDING),
            "currentDirectorReturn": receipt_ref,
            "currentReturnReceipt": receipt_ref,
            "currentReturnAudit": audit_ref,
            "currentReturnArchive": archive_ref,
            "currentReturnDelivery": delivery_ref,
            "heldThisStep": [SPELL],
            "separatelyRetainedHolds": retained,
            "acceptedIds": [],
            "appliedIds": [],
            "applicationPerformed": False,
            "canonicalFilesChanged": False,
            "currentBlocker": {"identity": NEXT, "blockerId": NEXT_BLOCKER, "group": NEXT_GROUP},
            "nextPendingGroup": {"group": NEXT_GROUP, "pendingIds": [NEXT], "pendingCount": 1, "reportedByDirector": True},
            "nextStep": "Review Astral Projection / PC232-B01 using current exact source bindings; preserve all holds and AFP211-E01 closed; apply only an exact sealed acceptance.",
            "directorConnectionStatus": "Return339 sealed Corruption Purification HOLD; the Director designates Astral Projection / PC232-B01 as next.",
        }
    )
    save(HANDOFF, handoff)
    SNAPSHOT.write_text(
        "# Spell review status — queue 339\n\n"
        f"Return339 independently verified {len(checks)}/{len(checks)} checks and holds Corruption Purification / AFP211-B05. "
        "Authority remains **823 applied, 25 pending, 0 accepted-unapplied** (547 complete standalone procedures; 173 scoped interfaces).\n\n"
        "Three contracts remain open: complete the cure-category/protection/dependency matrix; define exact creature and environmental admission, occupied-area geometry and partial-source handling; and reconcile permanent completed removal with the native Until Dispelled duration. Two complete paid useful witnesses (creature and multi-source area) remain required. The earlier conditional components were preserved without replay, AFP211-E01 remains closed, and no canonical changes or application were authorized.\n\n"
        "Next Director-prioritized identity: **Astral Projection / PC232-B01**.\n",
        encoding="utf-8",
        newline="\n",
    )

    print(
        json.dumps(
            {
                "status": "PASS",
                "checks": len(checks),
                "passed": sum(row["passed"] for row in checks),
                "failed": sum(not row["passed"] for row in checks),
                "archiveMembers": 39,
                "held": SPELL,
                "authority": AUTHORITY,
                "next": NEXT,
                "receipt": str(RECEIPT),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
