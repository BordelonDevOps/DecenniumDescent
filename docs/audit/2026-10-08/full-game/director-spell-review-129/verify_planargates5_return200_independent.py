from __future__ import annotations

import hashlib
import json
import subprocess
import zipfile
import zlib
from collections import Counter
from pathlib import Path, PurePosixPath

import orjson

ROOT = Path(__file__).resolve().parents[5]
AUDIT = ROOT / "docs/audit/2026-10-08/full-game/director-spell-review-129"
RECEIVED = AUDIT / "rank9_planargates5_return200_received"
ARCHIVE = RECEIVED / "DD_Rank9_PlanarGates5_Director_Return200.zip"
DELIVERY = RECEIVED / "DD_Rank9_PlanarGates5_Director_Return200_DELIVERY.json"
SOURCE_DIR = AUDIT / "rank9_planargates5_current_source_199_prepared"
SOURCE_ARCHIVE = SOURCE_DIR / "DD_Rank9_PlanarGates5_CurrentSource_199.zip"
SOURCE_DELIVERY = SOURCE_DIR / "DD_Rank9_PlanarGates5_CurrentSource_199_DELIVERY.json"
INDEX = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json"
CATALOG = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json"
QUEUE = AUDIT / "CURRENT_SPELL_QUEUE_198.json"
HANDOFF = AUDIT / "CURRENT_HANDOFF_198.json"
PENDING = AUDIT / "CURRENT58_PENDING_IDENTITY_AUDIT_198.json"
REPORT = AUDIT / "RANK9_PLANARGATES5_RETURN200_INDEPENDENT_AUDIT.json"
SOURCE_COMMIT = "21241139fccc612fa40b83a047e9a11b4a55a14e"
SUBMISSION_COMMIT = "e7f9fe3632aec76ecc761b69395a7520af889bd9"
BASELINE = {
    "reviewedApplied": 790,
    "pending": 58,
    "acceptedUnapplied": 0,
    "completeStandaloneProcedures": 514,
    "scopedInterfaces": 173,
}
ACCEPTED = ["gate", "absolute-gate", "planar-sanctuary"]
HELD = ["banishment-gate", "conjure-demiplane-fortress"]
GROUP = ACCEPTED + HELD
NEXT = "rank9-summon-hosts5"
NEXT_IDS = [
    "summon-elemental-avatar",
    "conjure-magmatic-wyrm",
    "planar-army",
    "summon-herald-of-the-planes",
    "summon-avatar-of-decay",
]
EXPECTED_COUNTS = {
    "procedures": 5,
    "passingCompleteStaticProcedures": 3,
    "unacceptedProposedProcedures": 2,
    "originalQuestions": 30,
    "focusedAddenda": 2,
    "answeredDispositions": 32,
    "requiredMainCases": 10,
    "branches": 62,
    "cases": 72,
    "demonstratedCases": 49,
    "heldIncompleteCaseTraces": 23,
    "futureObligations": 9,
    "events": 4159,
    "beforeAfterEventStateHashes": 8318,
    "caseEndpointStateHashes": 144,
    "forwardEventOperations": 8318,
    "inverseEventOperations": 8318,
    "eventOperations": 16636,
    "proposalOperations": 20,
    "totalOperations": 16656,
    "actorProfiles": 5,
    "sourceBindings": 132,
    "additionalSourceBindings": 17,
    "sourceVerificationChecks": 1431,
    "profileChecks": 352,
    "dataIntegrityChecks": 178815,
    "clockChecksIncludedInData": 20948,
    "scopedSemanticChecks": 1209,
    "metadataAndProposalChecks": 279,
    "totalStaticChecks": 182086,
    "localBlockingFindings": 3,
    "localHoldRecords": 13,
    "inheritedHoldRecords": 148,
    "holdRecords": 161,
    "outerArchiveMembers": 125,
    "boundInputPacketMembers": 162,
}


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def file_sha(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def canonical_sha(value: object) -> str:
    raw = json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False
    ).encode("utf-8")
    return sha(raw)


def git_blob(commit: str, path: str) -> bytes:
    return subprocess.run(
        ["git", "cat-file", "blob", f"{commit}:{path}"],
        cwd=ROOT,
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    ).stdout


def git_object(commit: str, path: str = "") -> str:
    target = f"{commit}^{{tree}}" if not path else f"{commit}:{path}"
    return subprocess.run(
        ["git", "rev-parse", target], cwd=ROOT, check=True, text=True, capture_output=True
    ).stdout.strip()


def stream_member(member) -> tuple[int, str, int]:
    h = hashlib.sha256()
    crc = 0
    size = 0
    for chunk in iter(lambda: member.read(1024 * 1024), b""):
        size += len(chunk)
        h.update(chunk)
        crc = zlib.crc32(chunk, crc)
    return size, h.hexdigest(), crc & 0xFFFFFFFF


def iter_case_objects(stream):
    """Yield one object at a time from the large compact CASEBOOK JSON array."""
    marker = b'"cases":['
    chunk_size = 1024 * 1024
    carry = bytearray()
    found = False
    current = bytearray()
    depth = 0
    in_string = escaped = started = False
    while True:
        chunk = stream.read(chunk_size)
        if not chunk:
            if started or depth:
                raise ValueError("CASEBOOK ended inside a case object")
            return
        if not found:
            carry.extend(chunk)
            at = carry.find(marker)
            if at < 0:
                if len(carry) > len(marker):
                    del carry[:-len(marker)]
                continue
            chunk = bytes(carry[at + len(marker):])
            carry.clear()
            found = True
        for byte in chunk:
            if not started:
                if byte in b" \r\n\t,":
                    continue
                if byte == ord("]"):
                    return
                if byte != ord("{"):
                    raise ValueError(f"Expected a CASEBOOK case object, got byte {byte}")
                started, depth, in_string, escaped = True, 1, False, False
                current.clear()
                current.append(byte)
                continue
            current.append(byte)
            if in_string:
                if escaped:
                    escaped = False
                elif byte == ord("\\"):
                    escaped = True
                elif byte == ord('"'):
                    in_string = False
                continue
            if byte == ord('"'):
                in_string = True
            elif byte in (ord("{"), ord("[")):
                depth += 1
            elif byte in (ord("}"), ord("]")):
                depth -= 1
                if depth == 0:
                    yield orjson.loads(current)
                    current.clear()
                    started = False


def record(checks: list[dict], name: str, passed: bool, detail: object = None) -> None:
    checks.append({"check": name, "passed": bool(passed), "detail": detail})


def main() -> None:
    checks: list[dict] = []
    delivery = json.loads(DELIVERY.read_text(encoding="utf-8-sig"))
    source_delivery = json.loads(SOURCE_DELIVERY.read_text(encoding="utf-8-sig"))
    archive_size, archive_sha = ARCHIVE.stat().st_size, file_sha(ARCHIVE)
    delivery_sha = file_sha(DELIVERY)
    record(
        checks,
        "Return200 ZIP exact byte count and SHA-256 match delivery",
        archive_size == delivery["archive"]["bytes"] == 171541716
        and archive_sha == delivery["archive"]["sha256"]
        == "8afda34a91bad329273753232e02a76136bff01a3d1da95416b573c9f4fb284c",
        {"bytes": archive_size, "sha256": archive_sha},
    )
    record(
        checks,
        "Submitted source ZIP and source delivery are exact local byte matches",
        SOURCE_ARCHIVE.stat().st_size == source_delivery["archive"]["bytes"]
        and file_sha(SOURCE_ARCHIVE) == source_delivery["archive"]["sha256"]
        == delivery["sourcePacket"]["sha256"]
        and SOURCE_ARCHIVE.stat().st_size == delivery["sourcePacket"]["bytes"],
        {"sourceBytes": SOURCE_ARCHIVE.stat().st_size, "sourceSHA256": file_sha(SOURCE_ARCHIVE)},
    )
    record(
        checks,
        "Source commit, submission commit, and authority baseline match the current review",
        source_delivery["sourceCommit"] == SOURCE_COMMIT
        and delivery["authorityUnchanged"] == BASELINE
        and subprocess.run(
            ["git", "merge-base", "--is-ancestor", SOURCE_COMMIT, "HEAD"], cwd=ROOT
        ).returncode == 0
        and subprocess.run(
            ["git", "merge-base", "--is-ancestor", SUBMISSION_COMMIT, "HEAD"], cwd=ROOT
        ).returncode == 0,
        {"sourceCommit": SOURCE_COMMIT, "submissionCommit": SUBMISSION_COMMIT,
         "currentHead": subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT,
                                        check=True, text=True, capture_output=True).stdout.strip()},
    )

    index_raw, catalog_raw = INDEX.read_bytes(), CATALOG.read_bytes()
    index = json.loads(index_raw)
    catalog = json.loads(catalog_raw)
    rows = {item["id"]: item for item in index["entries"]}
    source_spells = {item["id"]: item for item in catalog["spells"]}
    live = {item["id"] for item in index["entries"]
            if item["authoredStatus"] == "pending-authored-procedure"}
    pending_doc = json.loads(PENDING.read_text(encoding="utf-8"))
    queue = json.loads(QUEUE.read_text(encoding="utf-8"))
    handoff = json.loads(HANDOFF.read_text(encoding="utf-8"))
    record(
        checks,
        "Current index, prior queue, handoff, and pending audit agree at 790/58/514",
        index["authoredCounts"] == {"reviewed": 790, "pending": 58}
        and index["representationCounts"]["completeReviewedStandaloneProcedures"] == 514
        and len(live) == 58 and set(pending_doc["pendingIds"]) == live
        and set(GROUP) <= live
        and pending_doc["indexBinding"]["sha256"] == sha(index_raw)
        and queue["currentAuthority"] == BASELINE and queue["pendingCount"] == 58
        and handoff["currentAuthority"] == BASELINE,
        {"pending": len(live), "targetIdsPresent": set(GROUP) <= live},
    )
    baseline_blob = git_blob(SOURCE_COMMIT, INDEX.relative_to(ROOT).as_posix())
    record(
        checks,
        "Working authoritative index is byte-identical to the source-commit index",
        baseline_blob == index_raw,
        {"sourceIndexBytes": len(baseline_blob), "sourceIndexSHA256": sha(baseline_blob)},
    )

    with zipfile.ZipFile(ARCHIVE) as archive:
        infos_list = archive.infolist()
        infos = {info.filename: info for info in infos_list}
        names = list(infos)
        delivery_rows = {row["path"]: row for row in delivery["members"]}
        safe = all(
            not name.startswith(("/", "\\")) and "\\" not in name
            and not PurePosixPath(name).is_absolute()
            and ".." not in PurePosixPath(name).parts
            for name in names
        )
        record(
            checks,
            "ZIP has 125 unique safe members and exactly matches the delivery allowlist",
            len(infos_list) == len(infos) == len(delivery_rows) == 125
            and set(names) == set(delivery_rows) and safe,
            {"archiveMembers": len(infos_list), "deliveryMembers": len(delivery_rows), "safeNames": safe},
        )
        member_failures = []
        total_uncompressed = 0
        for name, info in infos.items():
            size, digest, crc = stream_member(archive.open(info, "r"))
            total_uncompressed += size
            row = delivery_rows[name]
            if (size != row["bytes"] or digest != row["sha256"]
                    or f"{crc:08x}" != row["crc32"].lower() or info.CRC != crc):
                member_failures.append({"path": name, "bytes": size, "sha256": digest,
                                        "crc32": f"{crc:08x}"})
        record(
            checks,
            "All archive members independently match exact bytes, SHA-256, and CRC32",
            not member_failures,
            {"checked": len(infos), "uncompressedBytes": total_uncompressed,
             "failures": member_failures[:12]},
        )
        member_manifest = json.loads(archive.read("MEMBER_MANIFEST.json"))
        internal = {row["path"]: row for row in member_manifest["members"]}
        record(
            checks,
            "Internal member manifest is exact and excludes only itself",
            member_manifest["memberCountExcludingSelf"] == 124
            and member_manifest["archiveMemberCountIncludingSelf"] == 125
            and member_manifest["selfExclusion"] == "This manifest excludes itself to avoid circular hashing; delivery binds it and every outer member."
            and set(internal) == set(names) - {"MEMBER_MANIFEST.json"}
            and all(internal[n]["bytes"] == delivery_rows[n]["bytes"]
                    and internal[n]["sha256"] == delivery_rows[n]["sha256"] for n in internal),
            {"internalMembers": len(internal), "archiveMembers": len(names)},
        )

        # Verify the current source ZIP embedded in Return200 against the exact local submitted packet.
        embedded_size, embedded_sha, _ = stream_member(
            archive.open("source_packet/DD_Rank9_PlanarGates5_CurrentSource_199.zip", "r")
        )
        record(
            checks,
            "Return200 embeds the exact source ZIP submitted for review",
            embedded_size == SOURCE_ARCHIVE.stat().st_size
            and embedded_sha == file_sha(SOURCE_ARCHIVE),
            {"embeddedBytes": embedded_size, "embeddedSHA256": embedded_sha},
        )
        embedded_delivery = archive.read(
            "source_packet/DD_Rank9_PlanarGates5_CurrentSource_199_DELIVERY.json"
        )
        record(
            checks,
            "Return200 embeds the byte-exact source delivery JSON",
            embedded_delivery == SOURCE_DELIVERY.read_bytes(),
            {"embeddedDeliveryBytes": len(embedded_delivery)},
        )

        # Independently resolve every declared refreshed source leaf to its Git blob at the source commit.
        git_proof = json.loads(archive.read("GIT_SOURCE_PROOF.json"))
        leaf_failures = []
        for path, binding in git_proof["leaves"].items():
            try:
                raw = git_blob(SOURCE_COMMIT, path)
            except subprocess.CalledProcessError:
                leaf_failures.append({"path": path, "reason": "git blob not found"})
                continue
            blob_sha = hashlib.sha1(b"blob " + str(len(raw)).encode("ascii") + b"\0" + raw).hexdigest()
            if len(raw) != binding["size"] or blob_sha != binding["sha"]:
                leaf_failures.append({"path": path, "bytes": len(raw), "blobSHA1": blob_sha})
        tree_failures = []
        for path, binding in git_proof["trees"].items():
            if path == "":
                if binding["sha"] != SOURCE_COMMIT:
                    tree_failures.append({"path": path, "expected": SOURCE_COMMIT,
                                         "actual": binding["sha"]})
                continue
            try:
                actual = git_object(SOURCE_COMMIT, path)
            except subprocess.CalledProcessError:
                tree_failures.append({"path": path, "reason": "git tree not found"})
                continue
            if actual != binding["sha"]:
                tree_failures.append({"path": path, "actual": actual, "expected": binding["sha"]})
        record(
            checks,
            "All source proof Git blobs and trees independently resolve at the named commit",
            git_proof["commit"] == SOURCE_COMMIT and len(git_proof["leaves"]) == 152
            and len(git_proof["trees"]) == 46 and not leaf_failures and not tree_failures,
            {"leaves": len(git_proof["leaves"]), "leafFailures": leaf_failures[:8],
             "trees": len(git_proof["trees"]), "treeFailures": tree_failures[:8]},
        )

        supplemental = json.loads(archive.read("SUPPLEMENTAL_SOURCE_VERIFICATION.json"))
        supplemental_failures = []
        for binding in supplemental["bindings"]:
            path = "supplemental_sources/" + binding["path"]
            size, digest, _ = stream_member(archive.open(path, "r"))
            raw = git_blob(SOURCE_COMMIT, binding["path"])
            blob_sha = hashlib.sha1(b"blob " + str(len(raw)).encode("ascii") + b"\0" + raw).hexdigest()
            if (size != binding["bytes"] or digest != binding["sha256"]
                    or raw != archive.read(path) or blob_sha != binding["gitBlobSHA1"]
                    or binding["sourceCommit"] != SOURCE_COMMIT):
                supplemental_failures.append(binding["path"])
        record(
            checks,
            "All 17 supplemental source copies match their declared Git blobs and hashes",
            len(supplemental["bindings"]) == 17 and supplemental["checkCount"] == 78
            and all(item.get("pass") is True for item in supplemental["checks"])
            and not supplemental_failures,
            {"bindings": len(supplemental["bindings"]), "failures": supplemental_failures[:8]},
        )
        source_verification = json.loads(archive.read("SOURCE_VERIFICATION.json"))
        record(
            checks,
            "Refreshed-source verification reports 1,353 passing checks",
            source_verification["status"] == "PASS"
            and source_verification["sourceCommit"] == SOURCE_COMMIT
            and source_verification["checkCount"] == 1353
            and len(source_verification["checks"]) == 1353
            and all(item.get("pass") is True for item in source_verification["checks"]),
            {"status": source_verification["status"], "checks": len(source_verification["checks"])},
        )

        decision = json.loads(archive.read("DIRECTOR_DECISION.json"))
        procedures = json.loads(archive.read("PROCEDURES.json"))["spells"]
        procedure_map = {item["id"]: item for item in procedures}
        decisions = {item["spellId"]: item for item in decision["perIdentity"]}
        record(
            checks,
            "Director disposition is exactly three accepted and two held, with no application",
            decision["sourceCommit"] == SOURCE_COMMIT
            and decision["submissionCommit"] == SUBMISSION_COMMIT
            and decision["authorityUnchanged"] == BASELINE
            and decision["acceptedIds"] == ACCEPTED and decision["unacceptedIds"] == HELD
            and decision["applied"] is False and decision["canonicalFilesEdited"] is False
            and set(decisions) == set(procedure_map) == set(GROUP)
            and all(decisions[s]["accepted"] is True and decisions[s]["applied"] is False
                    and decisions[s]["blockerIds"] == [] and procedure_map[s]["accepted"] is True
                    and procedure_map[s]["applied"] is False for s in ACCEPTED)
            and all(decisions[s]["accepted"] is False and decisions[s]["applied"] is False
                    and decisions[s]["blockerIds"] for s in HELD)
            and all(procedure_map[s]["accepted"] is False and procedure_map[s]["applied"] is False
                    for s in HELD),
            {"acceptedIds": decision["acceptedIds"], "heldIds": decision["unacceptedIds"]},
        )
        index_entry_failures = []
        for sid in GROUP:
            old = rows[sid]
            expected = {
                "id": sid,
                "name": old["name"],
                "authoredStatus": old["authoredStatus"],
                "procedureFile": old["procedureFile"],
                "procedurePointer": old["procedurePointer"],
                "wholeCardPointer": old["wholeCardPointer"],
                "sourceStatus": old["sourceStatus"],
                "priorCatalogSelectionStatusUnchanged": True,
            }
            if (old["sourceStatus"] != "blocked-pending-operational-review"
                    or old["authoredStatus"] != "pending-authored-procedure"
                    or procedure_map[sid]["sourceIndexEntryUnchanged"] != expected
                    or procedure_map[sid]["nativeCardUnchanged"].get("id") != sid
                    or procedure_map[sid]["nativeCardUnchanged"].get("status") != "blocked-pending-operational-review"):
                index_entry_failures.append(sid)
        record(
            checks,
            "All five procedures bind to the exact pending index entries and preserve native-card status",
            not index_entry_failures,
            {"failures": index_entry_failures},
        )
        validation = json.loads(archive.read("VALIDATION.json"))
        counts = json.loads(archive.read("COUNTS.json"))
        data_integrity = json.loads(archive.read("DATA_INTEGRITY_CHECK.json"))
        semantic = json.loads(archive.read("INDEPENDENT_SEMANTIC_FAILURE_CHECK.json"))
        record(
            checks,
            "Declared counts and independent semantic check preserve the three-only acceptance boundary",
            counts == EXPECTED_COUNTS and validation["exactCounts"] == EXPECTED_COUNTS
            and validation["status"] == "INTEGRITY_PASS_SEMANTIC_PARTIAL_ACCEPTANCE"
            and validation["canonicalFilesUnchanged"] is True
            and data_integrity["status"] == "PASS" and data_integrity["failures"] == []
            and data_integrity["caseCount"] == 72 and data_integrity["eventCount"] == 4159
            and semantic["status"] == "PASS_WITH_EXPLICIT_BLOCKED_IDENTITIES"
            and semantic["checkCount"] == 1209 and semantic["checks"]
            and semantic["failedChecks"] == []
            and semantic["acceptedCandidatesOnlyIfDataAlsoPass"] == ACCEPTED
            and semantic["unacceptedCandidates"] == HELD,
            {"dataIntegrity": data_integrity["status"], "semantic": semantic["status"],
             "semanticChecks": len(semantic["checks"]), "failedChecks": len(semantic["failedChecks"])},
        )

        dispositions = json.loads(archive.read("CASE_DISPOSITIONS.json"))["cases"]
        disposition_map = {item["id"]: item for item in dispositions}
        accepted_cases = {case_id for sid in ACCEPTED for case_id in procedure_map[sid]["caseIds"]}
        held_cases = {case_id for sid in HELD for case_id in procedure_map[sid]["caseIds"]}
        record(
            checks,
            "All 49 accepted cases are demonstrated; all 23 held traces remain explicitly incomplete",
            len(dispositions) == 72 and len(accepted_cases) == 49 and len(held_cases) == 23
            and accepted_cases.isdisjoint(held_cases)
            and set(disposition_map) == accepted_cases | held_cases
            and all(disposition_map[c]["demonstrated"] is True
                    and disposition_map[c]["status"] == "STATIC_TRACE" for c in accepted_cases)
            and all(disposition_map[c]["demonstrated"] is False
                    and disposition_map[c]["status"].startswith("HELD_") for c in held_cases),
            {"acceptedCases": len(accepted_cases), "heldCases": len(held_cases)},
        )
        hold_register = json.loads(archive.read("HOLD_REGISTER.json"))
        blocker_map = {row["id"]: row for row in decision["blockers"]}
        record(
            checks,
            "Banishment Gate and Demiplane Fortress retain their named evidence blockers",
            set(decision["unacceptedIds"]) == set(HELD)
            and {sid: decisions[sid]["blockerIds"] for sid in HELD}
            == {"banishment-gate": ["PG200-B03", "PG200-B04"],
                "conjure-demiplane-fortress": ["PG200-B06"]}
            and {sid: blocker_map[b]["spellIds"] for sid, ids in
                 {"banishment-gate": ["PG200-B03", "PG200-B04"],
                  "conjure-demiplane-fortress": ["PG200-B06"]}.items() for b in ids}
            and hold_register["recordCount"] == 161
            and hold_register["localRecordCount"] == 13
            and hold_register["inheritedRecordCount"] == 148,
            {"heldIds": HELD, "blockerIds": {sid: decisions[sid]["blockerIds"] for sid in HELD},
             "holdRecords": hold_register["recordCount"]},
        )

        casebook_info = infos["CASEBOOK.json"]
        book_size, book_sha, book_crc = stream_member(archive.open("CASEBOOK.json", "r"))
        record(
            checks,
            "CASEBOOK byte digest matches its standalone data-integrity binding",
            book_size == casebook_info.file_size == 549968664
            and book_sha == data_integrity["validatedCasebookSHA256"]
            and book_crc == casebook_info.CRC,
            {"bytes": book_size, "sha256": book_sha, "crc32": f"{book_crc:08x}"},
        )
        case_ids: set[str] = set()
        main_ids: set[str] = set()
        events = forward_ops = inverse_ops = 0
        replay_failures = []
        status_counts: Counter[str] = Counter()
        for case in iter_case_objects(archive.open("CASEBOOK.json", "r")):
            case_id = case["id"]
            if case_id in case_ids:
                replay_failures.append({"case": case_id, "reason": "duplicate case id"})
                continue
            case_ids.add(case_id)
            if case.get("kind") == "main":
                main_ids.add(case_id)
            status_counts[str(case.get("status"))] += 1
            initial, final = case["initial"], case["final"]
            if canonical_sha(initial) != case["initialSHA256"] or canonical_sha(final) != case["finalSHA256"]:
                replay_failures.append({"case": case_id, "reason": "endpoint state hash"})
                continue
            state = initial
            previous_time = state.get("time")
            for event in case["events"]:
                events += 1
                forward, inverse = event["forward"], event["inverse"]
                forward_ops += len(forward)
                inverse_ops += len(inverse)
                before, after = event["before"], event["after"]
                good = (before == state and event["beforeSHA256"] == canonical_sha(before)
                        and event["afterSHA256"] == canonical_sha(after)
                        and len(forward) == len(inverse) == 2)
                if good:
                    good = (
                        forward[0] == {"op": "test", "path": "", "value": before}
                        and forward[1] == {"op": "replace", "path": "", "value": after}
                        and inverse[0] == {"op": "test", "path": "", "value": after}
                        and inverse[1] == {"op": "replace", "path": "", "value": before}
                    )
                before_time, after_time = before.get("time"), after.get("time")
                if (isinstance(before_time, (int, float)) and isinstance(after_time, (int, float))
                        and after_time < before_time):
                    good = False
                if (isinstance(previous_time, (int, float)) and isinstance(before_time, (int, float))
                        and before_time < previous_time):
                    good = False
                if not good:
                    replay_failures.append({"case": case_id, "event": event.get("id"),
                                            "reason": "chain/patch/hash/clock"})
                    break
                state, previous_time = after, after_time
            if state != final or canonical_sha(state) != case["finalSHA256"]:
                replay_failures.append({"case": case_id, "reason": "final chain state"})
            member_name = "cases/" + case_id.replace("/", "__") + ".json"
            member_case = json.loads(archive.read(member_name))
            if member_case != case:
                replay_failures.append({"case": case_id, "reason": "casebook/member mismatch"})
        branch_count = len(case_ids) - len(main_ids)
        record(
            checks,
            "All 72 cases and 4,159 events independently replay with reversible patches and monotone clocks",
            len(case_ids) == 72 and len(main_ids) == 10 and branch_count == 62
            and events == 4159 and forward_ops == inverse_ops == 8318
            and not replay_failures,
            {"cases": len(case_ids), "main": len(main_ids), "branches": branch_count,
             "events": events, "forwardOps": forward_ops, "inverseOps": inverse_ops,
             "statuses": dict(status_counts), "failures": replay_failures[:10]},
        )

        handoff_doc = json.loads(archive.read("NEXT_QUEUE_HANDOFF.json"))
        next_group = handoff_doc["nextCurrentQueueGroupUnchanged"]
        record(
            checks,
            "Return200 requires a fresh authority packet for the exact next five-spell group",
            handoff_doc["canonicalAuthorityUnchanged"] == BASELINE
            and handoff_doc["acceptedThisReturnUnapplied"] == ACCEPTED
            and next_group["group"] == NEXT and next_group["pendingIds"] == NEXT_IDS
            and next_group["pendingCount"] == 5
            and next_group["freshPacketRequiredForCurrentAuthority"] is True,
            next_group,
        )

    failures = [item for item in checks if not item["passed"]]
    report = {
        "id": "RANK9-PLANARGATES5-RETURN200-INDEPENDENT-AUDIT",
        "status": "PASS" if not failures else "FAIL",
        "checksPassed": len(checks) - len(failures),
        "checksFailed": len(failures),
        "checks": checks,
        "sourceCommit": SOURCE_COMMIT,
        "submissionCommit": SUBMISSION_COMMIT,
        "returnArchive": {"path": ARCHIVE.relative_to(ROOT).as_posix(), "bytes": archive_size,
                          "sha256": archive_sha},
        "delivery": {"path": DELIVERY.relative_to(ROOT).as_posix(), "bytes": DELIVERY.stat().st_size,
                     "sha256": delivery_sha},
        "acceptedIds": ACCEPTED,
        "unacceptedIds": HELD,
        "applied": False,
    }
    REPORT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"status": report["status"], "checksPassed": report["checksPassed"],
                      "checksFailed": report["checksFailed"], "failures": failures,
                      "report": REPORT.relative_to(ROOT).as_posix()}, ensure_ascii=False, indent=2))
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
