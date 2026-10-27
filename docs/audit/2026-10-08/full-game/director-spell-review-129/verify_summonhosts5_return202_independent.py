#!/usr/bin/env python3
"""Independently verify GPT director Return202 without executing archive code."""

from __future__ import annotations

import hashlib
import io
import json
import subprocess
import zipfile
import zlib
from pathlib import Path


HERE = Path(__file__).resolve().parent
RECEIVED = HERE / "rank9_summonhosts5_return202_received"
ARCHIVE = RECEIVED / "DD_Rank9_SummonHosts5_Director_Return202.zip"
DELIVERY = RECEIVED / "DD_Rank9_SummonHosts5_Director_Return202_DELIVERY.json"
AUDIT_OUT = HERE / "RANK9_SUMMONHOSTS5_RETURN202_INDEPENDENT_AUDIT.json"
EXPECTED_SOURCE_COMMIT = "0a7778f059bbeeba7e4a998c83bc3562a96abd52"
EXPECTED_SUBMISSION_COMMIT = "83f6cc4b555df74dfaa218f5c44ef0332105dde0"
EXPECTED_ACCEPTED = {"conjure-magmatic-wyrm", "planar-army"}
EXPECTED_BLOCKED = {
    "summon-elemental-avatar": "SH202-B01",
    "summon-herald-of-the-planes": "SH202-B02",
    "summon-avatar-of-decay": "SH202-B03",
}
EXPECTED_COUNTS = {
    "procedures": 5,
    "staticAcceptedProcedures": 2,
    "unacceptedProcedures": 3,
    "originalQuestions": 32,
    "focusedAddenda": 2,
    "selectedQuestionDispositions": 34,
    "requiredMainCases": 10,
    "mainCaseDispositions": 10,
    "branches": 51,
    "cases": 61,
    "events": 10769,
    "forwardEventOperations": 21538,
    "inverseEventOperations": 21538,
    "eventOperations": 43076,
    "proposalOperations": 20,
    "requiredFutureObligations": 8,
    "futureObligationDispositions": 8,
    "currentSourceBindings": 210,
    "supplementalSourceBindings": 7,
    "localBlockingHolds": 3,
    "inheritedHolds": 161,
    "totalHoldRecords": 176,
    "wholeMainCaseHolds": 5,
}
EXPECTED_CARRIED_NAMES = {
    "AG190": {"absolute-domination", "puppetmaster-s-realm"},
    "TF192": {"time-stop", "eternal-prophecy", "fate-rewrite", "collapse-timeline"},
    "CC194": {"perfect-spell", "unholy-ascendance"},
    "MD196": {"mind-collapse", "unravel-identity"},
}
EXPECTED_PRIOR_BLOCKER_GROUPS = {
    "retainedReturn188Blockers": {"nullification-wave", "reality-anchor"},
    "retainedReturn190Blockers": {"absolute-domination", "puppetmaster-s-realm"},
    "retainedReturn192Blockers": {"time-stop", "eternal-prophecy", "fate-rewrite", "collapse-timeline"},
    "retainedReturn194Blockers": {"perfect-spell", "unholy-ascendance"},
    "retainedReturn196Blockers": {"mind-collapse", "unravel-identity"},
    "retainedReturn198Blockers": {"faction-omniscience-supreme"},
}


def require(condition: bool, message: str, checks: list[str]) -> None:
    if not condition:
        raise AssertionError(message)
    checks.append(message)


def hash_file(path: Path) -> tuple[int, str, str]:
    sha = hashlib.sha256()
    crc = 0
    size = 0
    with path.open("rb") as stream:
        while chunk := stream.read(8 * 1024 * 1024):
            size += len(chunk)
            sha.update(chunk)
            crc = zlib.crc32(chunk, crc)
    return size, sha.hexdigest(), f"{crc & 0xffffffff:08x}"


def hash_member(archive: zipfile.ZipFile, info: zipfile.ZipInfo) -> tuple[int, str, str]:
    sha = hashlib.sha256()
    crc = 0
    size = 0
    with archive.open(info, "r") as stream:
        while chunk := stream.read(8 * 1024 * 1024):
            size += len(chunk)
            sha.update(chunk)
            crc = zlib.crc32(chunk, crc)
    return size, sha.hexdigest(), f"{crc & 0xffffffff:08x}"


def json_member(archive: zipfile.ZipFile, name: str):
    return json.loads(archive.read(name).decode("utf-8"))


def verify_git_tree(commit: str, bindings: list[dict], checks: list[str]) -> dict[str, str]:
    paths = [binding["path"] for binding in bindings]
    tree: dict[str, str] = {}
    for start in range(0, len(paths), 35):
        batch = paths[start : start + 35]
        result = subprocess.run(
            ["git", "ls-tree", "-r", "-z", "--full-tree", commit, "--", *batch],
            cwd=HERE.parents[4],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        for record in result.stdout.split(b"\0"):
            if not record:
                continue
            header, path_bytes = record.split(b"\t", 1)
            _mode, object_type, object_id = header.decode("ascii").split(" ")
            require(object_type == "blob", "Source path resolves to a Git blob", checks)
            tree[path_bytes.decode("utf-8")] = object_id
    require(len(tree) == len(paths), "All source bindings resolve in the bound Git tree", checks)
    return tree


def main() -> None:
    checks: list[str] = []
    delivery_bytes = DELIVERY.read_bytes()
    delivery = json.loads(delivery_bytes.decode("utf-8"))
    archive_size, archive_sha, archive_crc = hash_file(ARCHIVE)
    declared_archive = delivery["archive"]
    require(archive_size == declared_archive["bytes"], "Outer ZIP byte length matches delivery manifest", checks)
    require(archive_sha == declared_archive["sha256"], "Outer ZIP SHA-256 matches delivery manifest", checks)
    require(archive_crc == declared_archive["crc32"], "Outer ZIP CRC32 matches delivery manifest", checks)
    require(delivery.get("memberCount") == 106, "Delivery manifest declares 106 ZIP members", checks)
    require(delivery.get("deliverySelfHash", "").startswith("Not self-referential"), "Delivery self-hash is explicitly informational", checks)

    with zipfile.ZipFile(ARCHIVE, "r") as outer:
        infos = outer.infolist()
        names = [item.filename for item in infos]
        require(len(names) == len(set(names)), "Outer ZIP has no duplicate member names", checks)
        declared_members = {member["path"]: member for member in delivery["members"]}
        require(set(names) == set(declared_members), "Outer ZIP member allowlist exactly matches delivery manifest", checks)
        require(len(names) == delivery["memberCount"], "Outer ZIP central directory member count matches manifest", checks)
        require(all(not name.startswith(("/", "\\")) and ".." not in Path(name).parts for name in names), "Outer ZIP member paths contain no traversal", checks)

        for info in infos:
            expected = declared_members[info.filename]
            size, sha, crc = hash_member(outer, info)
            require(size == expected["bytes"] == info.file_size, f"Member size verified: {info.filename}", checks)
            require(sha == expected["sha256"], f"Member SHA-256 verified: {info.filename}", checks)
            require(crc == expected["crc32"] == f"{info.CRC:08x}", f"Member CRC verified: {info.filename}", checks)

        member_manifest = json_member(outer, "MEMBER_MANIFEST.json")
        member_info = declared_members["MEMBER_MANIFEST.json"]
        require(member_info["bytes"] == delivery["manifestMember"]["bytes"], "Manifest member byte count agrees across delivery fields", checks)
        require(member_info["sha256"] == delivery["manifestMember"]["sha256"], "Manifest member SHA agrees across delivery fields", checks)
        embedded_members = {item["path"]: item for item in member_manifest.get("members", [])}
        require(member_manifest.get("memberCountExcludingThisManifest") == 105, "Embedded manifest declares 105 non-manifest members", checks)
        require(len(embedded_members) == 105, "Embedded manifest contains 105 entries", checks)
        require(set(embedded_members) == set(declared_members) - {"MEMBER_MANIFEST.json"}, "Embedded manifest paths match the delivery allowlist", checks)
        require(all(embedded_members[path] == item for path, item in embedded_members.items()), "Embedded manifest records match delivery hashes and sizes", checks)

        decision = json_member(outer, "DIRECTOR_DECISION.json")
        current = json_member(outer, "CURRENT_AUTHORITY.json")
        counts = json_member(outer, "COUNTS.json")
        integrity = json_member(outer, "DATA_INTEGRITY_CHECK.json")
        semantic = json_member(outer, "INDEPENDENT_SEMANTIC_FAILURE_CHECK.json")
        case_index = json_member(outer, "CASE_INDEX.json")
        question_dispositions = json_member(outer, "QUESTION_DISPOSITIONS.json")
        future_dispositions = json_member(outer, "FUTURE_OBLIGATION_DISPOSITIONS.json")
        source_bindings_doc = json_member(outer, "SOURCE_BINDINGS.json")
        source_verification = json_member(outer, "SOURCE_VERIFICATION.json")
        inherited_holds = json_member(outer, "INHERITED_HOLDS_UNCHANGED.json")
        package_verification = delivery["packageVerification"]

        require(decision.get("returnNumber") == 202, "Decision is Return202", checks)
        accepted = set(decision.get("acceptedIds", []))
        blocked = set(decision.get("unacceptedIds", []))
        require(accepted == EXPECTED_ACCEPTED, "Accepted spell identities match the exact director decision", checks)
        require(blocked == set(EXPECTED_BLOCKED), "Unaccepted spell identities match the exact director decision", checks)
        require(decision.get("applied") is False, "Director return does not claim application", checks)
        require(set(delivery.get("acceptedIds", [])) == EXPECTED_ACCEPTED, "Delivery accepted IDs match the decision", checks)
        require(set(delivery.get("unacceptedIds", [])) == set(EXPECTED_BLOCKED), "Delivery held IDs match the decision", checks)
        authority = decision["boundCanonicalAuthorityUnchanged"]
        require(authority == {"reviewedApplied": 793, "pending": 55, "acceptedUnapplied": 0, "completeStandaloneProcedures": 517, "scopedInterfaces": 173}, "Canonical authority is unchanged at 793/55/0", checks)
        require(current["sourceCommit"] == EXPECTED_SOURCE_COMMIT, "Current authority names the expected source commit", checks)
        require(current["sourceBranch"] == "codex/ordinary-spell-review-complete", "Current authority names the review branch", checks)
        require(source_bindings_doc["sourceCommit"] == EXPECTED_SOURCE_COMMIT, "Source binding document uses the bound source commit", checks)
        require(source_bindings_doc["submissionCommit"] == EXPECTED_SUBMISSION_COMMIT, "Source packet submission commit matches pushed HEAD", checks)
        require(source_verification.get("status") == "PASS", "Director source verification status is PASS", checks)
        require(len(source_bindings_doc.get("sourceBindings", [])) == 210, "Source binding list contains 210 files", checks)
        require(len(source_verification.get("sourceBindings", [])) == 210, "Source verification list contains 210 files", checks)
        supplemental_bindings = source_bindings_doc.get("supplementalBindings", [])
        require(len(supplemental_bindings) == 7, "Source binding document contains seven supplemental bindings", checks)
        require(len(source_verification.get("additionalBindings", [])) == 7, "Source verification document contains seven supplemental bindings", checks)
        require(source_verification.get("sourceProgramsExecuted") is False and source_verification.get("historicalProgramsExecuted") is False, "No supplied source or historical programs were executed", checks)
        require(package_verification.get("status") == "PASS" and package_verification.get("checkCount") == 324, "Director package-verification summary reports 324 passing checks", checks)
        require(all(item.get("pass") is True for item in package_verification.get("checks", [])), "Every declared package-verification check passes", checks)
        require(counts == {**counts, **EXPECTED_COUNTS}, "All required Return202 counts match", checks)
        require(delivery.get("counts") == counts, "Delivery count summary matches embedded COUNTS.json", checks)
        require(integrity.get("status") == "PASS" and not integrity.get("dataFailures"), "Data integrity report passes with no failures", checks)
        require(not integrity.get("scopedSemanticFailures"), "Scoped semantic report has no recorded predicate failures", checks)
        require(semantic.get("status") == "PARTIAL_ACCEPTANCE_WITH_THREE_EXACT_BLOCKERS", "Independent failure check retains three exact blockers", checks)
        semantic_blockers = {item["id"]: item for item in semantic.get("blockers", []) if item.get("blocking")}
        require(set(semantic_blockers) == set(EXPECTED_BLOCKED.values()), "Blocking IDs are exactly SH202-B01/B02/B03", checks)
        for per_identity in decision.get("perIdentity", []):
            spell_id = per_identity["spellId"]
            require(per_identity.get("applied") is False, f"No per-spell application claimed: {spell_id}", checks)
            if spell_id in EXPECTED_ACCEPTED:
                require(per_identity.get("accepted") is True and not per_identity.get("blockerIds"), f"Accepted identity has no blocker: {spell_id}", checks)
            else:
                require(per_identity.get("accepted") is False and per_identity.get("blockerIds") == [EXPECTED_BLOCKED[spell_id]], f"Held identity retains its exact blocker: {spell_id}", checks)

        require(len(question_dispositions) == 34, "Question dispositions cover 32 original questions and two addenda", checks)
        question_ids = [item["id"] for item in question_dispositions]
        expected_question_ids = {f"R9SH-{i:02d}" for i in range(1, 33)} | {"HOST129-ADD01", "HOST129-ADD02"}
        require(len(set(question_ids)) == 34 and set(question_ids) == expected_question_ids, "All 32 original question IDs and both addenda are preserved", checks)
        require(all(item.get("decisionSelected") is True and item.get("selectionDoesNotGrantAcceptance") is True for item in question_dispositions), "Every question disposition is explicit and does not itself grant acceptance", checks)
        require(len(future_dispositions) == 8, "Future obligation dispositions cover all eight obligations", checks)
        require(len(case_index) == 61, "Case index has ten main cases and 51 branches", checks)
        require(sum(item.get("events", 0) for item in case_index) == counts["events"], "Indexed case event totals sum to the reported 10,769", checks)
        main_cases = [item for item in case_index if item.get("caseKind") == "main"]
        require(len(main_cases) == 10, "Case index has ten required main cases", checks)
        main_by_spell: dict[str, list[dict]] = {}
        for item in main_cases:
            main_by_spell.setdefault(item["spellId"], []).append(item)
        require(all(len(main_by_spell.get(spell, [])) == 2 for spell in EXPECTED_ACCEPTED | set(EXPECTED_BLOCKED)), "Each reviewed spell has two main cases", checks)
        require(all(item.get("status") == "DEMONSTRATED" and not item.get("missingEvidence") for spell in EXPECTED_ACCEPTED for item in main_by_spell[spell]), "Both accepted spells have demonstrated main cases", checks)
        require(all(any(item.get("status") == "HELD_INCOMPLETE" for item in main_by_spell[spell]) for spell in EXPECTED_BLOCKED), "Each unaccepted spell retains at least one held main case", checks)

        require(inherited_holds.get("recordCount") == 161 and inherited_holds.get("inheritedRecordCount") == 148, "Inherited ledger retains 148 source-qualified records", checks)
        require(len(inherited_holds.get("inheritedHoldRecordsUnchanged", [])) == 148, "All 148 inherited hold records are present", checks)
        carried = inherited_holds.get("inheritedCarriedNamedBlockersUnchanged", {})
        require(set(carried) == set(EXPECTED_CARRIED_NAMES), "Carried named blocker batches are AG190/TF192/CC194/MD196", checks)
        for group, names in EXPECTED_CARRIED_NAMES.items():
            require(set(carried[group].get("ids", [])) == names, f"Inherited spell identities remain unchanged for {group}", checks)
        retained = current.get("retainedNamedBlockersOutsideScope", {})
        current_retained = inherited_holds.get("currentNamedBlockersOutsideScopeUnchanged", {})
        for group, names in EXPECTED_PRIOR_BLOCKER_GROUPS.items():
            require(set(retained.get(group, {})) == names, f"Current authority retains prior blockers {group}", checks)
            require(set(current_retained.get(group, {})) == names, f"Return202 preserves prior blockers {group}", checks)
        pg200 = inherited_holds.get("newHolds", [])
        pg200_blockers = {item["id"]: item for item in pg200 if item.get("id", "").startswith("PG200-B")}
        require(set(pg200_blockers) == {"PG200-B03", "PG200-B04", "PG200-B06"}, "Return200's three named blockers are carried unchanged", checks)
        require(set(retained.get("retainedReturn200Blockers", {})) == {"banishment-gate", "conjure-demiplane-fortress"}, "Current authority retains both Return200 spell holds", checks)
        require(inherited_holds.get("localBlockingCount") == 3, "Three local blocking holds match the unaccepted identities", checks)
        require(all(semantic_blockers[blocker]["spellIds"] == [spell] for spell, blocker in EXPECTED_BLOCKED.items()), "Each blocking ID maps to its exact spell", checks)

        source_binding = delivery["sourceArchiveBinding"]
        inner_bytes = outer.read("source_packet/DD_Rank9_SummonHosts5_CurrentSource_201.zip")
        require(len(inner_bytes) == source_binding["bytes"], "Nested current-source archive size matches its binding", checks)
        require(hashlib.sha256(inner_bytes).hexdigest() == source_binding["sha256"], "Nested current-source archive SHA-256 matches its binding", checks)

    bindings = source_bindings_doc["sourceBindings"]
    supplemental_bindings = source_bindings_doc["supplementalBindings"]
    tree = verify_git_tree(EXPECTED_SOURCE_COMMIT, bindings + supplemental_bindings, checks)
    with zipfile.ZipFile(io.BytesIO(inner_bytes), "r") as source_zip:
        source_names = set(source_zip.namelist())
        require(len(source_names) == len(source_zip.namelist()), "Nested source ZIP has no duplicate names", checks)
        for binding in bindings:
            member = binding["archiveMember"]
            path = binding["path"]
            require(member in source_names, f"Bound current source exists in nested ZIP: {path}", checks)
            info = source_zip.getinfo(member)
            sha = hashlib.sha256()
            git_sha = hashlib.sha1()
            git_sha.update(f"blob {info.file_size}\0".encode("ascii"))
            size = 0
            with source_zip.open(info, "r") as stream:
                while chunk := stream.read(4 * 1024 * 1024):
                    size += len(chunk)
                    sha.update(chunk)
                    git_sha.update(chunk)
            require(size == binding["bytes"] == info.file_size, f"Current-source size matches Git binding: {path}", checks)
            require(sha.hexdigest() == binding["sha256"], f"Current-source SHA-256 matches Git binding: {path}", checks)
            computed_git_blob = git_sha.hexdigest()
            require(computed_git_blob == binding["gitBlobSHA1"] == tree.get(path), f"Current-source Git blob matches bound commit: {path}", checks)

    with zipfile.ZipFile(ARCHIVE, "r") as outer:
        for binding in supplemental_bindings:
            member = binding["returnMember"]
            path = binding["path"]
            info = outer.getinfo(member)
            sha = hashlib.sha256()
            git_sha = hashlib.sha1()
            git_sha.update(f"blob {info.file_size}\0".encode("ascii"))
            size = 0
            with outer.open(info, "r") as stream:
                while chunk := stream.read(1024 * 1024):
                    size += len(chunk)
                    sha.update(chunk)
                    git_sha.update(chunk)
            require(size == binding["bytes"] == info.file_size, f"Supplemental source size matches binding: {path}", checks)
            require(sha.hexdigest() == binding["sha256"], f"Supplemental source SHA-256 matches binding: {path}", checks)
            require(git_sha.hexdigest() == binding["gitBlobSHA1"] == tree.get(path), f"Supplemental Git blob matches source commit: {path}", checks)

    submission = subprocess.run(
        ["git", "rev-parse", EXPECTED_SUBMISSION_COMMIT],
        cwd=HERE.parents[4],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    ).stdout.strip()
    require(submission == EXPECTED_SUBMISSION_COMMIT, "Submitted packet commit is present in the local repository", checks)

    audit = {
        "id": "RANK9-SUMMONHOSTS5-RETURN202-INDEPENDENT-AUDIT",
        "status": "PASS_WITH_THREE_EXACT_BLOCKERS",
        "archive": {
            "name": ARCHIVE.name,
            "bytes": archive_size,
            "sha256": archive_sha,
            "crc32": archive_crc,
            "memberCount": delivery["memberCount"],
            "membersVerified": len(delivery["members"]),
        },
        "deliveryManifest": {"name": DELIVERY.name, "bytes": len(delivery_bytes), "sha256": hashlib.sha256(delivery_bytes).hexdigest()},
        "sourceBindingsVerified": len(bindings),
        "supplementalBindingsVerified": len(supplemental_bindings),
        "sourceCommit": EXPECTED_SOURCE_COMMIT,
        "submissionCommit": EXPECTED_SUBMISSION_COMMIT,
        "acceptedIds": sorted(EXPECTED_ACCEPTED),
        "unacceptedBlockers": EXPECTED_BLOCKED,
        "authorityUnchanged": authority,
        "counts": counts,
        "checksPassed": len(checks),
        "checks": checks,
        "qualification": "Static authored review only; no canonical application, runtime, implementation, playtest, balance, cosmology, domain-closure, completion, or release approval is inferred.",
    }
    AUDIT_OUT.write_text(json.dumps(audit, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"status": audit["status"], "checksPassed": len(checks), "membersVerified": len(delivery["members"]), "sourceBindingsVerified": len(bindings), "acceptedIds": audit["acceptedIds"], "unacceptedBlockers": EXPECTED_BLOCKED, "archiveSha256": archive_sha, "audit": str(AUDIT_OUT)}, indent=2))


if __name__ == "__main__":
    main()
