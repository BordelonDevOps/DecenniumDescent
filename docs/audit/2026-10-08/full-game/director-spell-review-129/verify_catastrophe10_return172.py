from __future__ import annotations

import hashlib
import json
import subprocess
import zipfile
import zlib
from fractions import Fraction
from pathlib import Path, PurePosixPath

import jsonpatch

ROOT = Path(__file__).resolve().parents[5]
AUDIT = ROOT / "docs/audit/2026-10-08/full-game/director-spell-review-129"
RECV = AUDIT / "rank9_catastrophe10_return172_received"
RETURN = RECV / "DD_Rank9_Catastrophe10_Director_Return172.zip"
DELIVERY = RECV / "DD_Rank9_Catastrophe10_Director_Return172_DELIVERY.json"
PACKET = ROOT / "docs/audit/2026-10-08/full-game/DD_Rank9_Catastrophe_10_Source_Conference_02.zip"
CANDIDATE = ROOT / "DescentReviewChanges/ReviewBible/data/director/spell_review/rank9_catastrophe_10_source_conference_02.json"
INDEX = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json"
CATALOG = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json"
QUEUE = AUDIT / "CURRENT_SPELL_QUEUE_170.json"
HANDOFF = AUDIT / "CURRENT_HANDOFF_170.json"
IDS = [
    "cataclysmic-conjuration",
    "elemental-apocalypse",
    "planar-overload",
    "armageddon",
    "cataclysm",
    "arcane-apocalypse",
    "meteor-swarm",
    "starfire-core",
    "ragnarok",
    "final-spark",
]
AUTHORITY = {
    "reviewedApplied": 739,
    "pending": 109,
    "acceptedUnapplied": 0,
    "completeReviewedStandaloneProcedures": 463,
    "scopedInterfaces": 173,
}
checks: list[dict] = []
failures: list[str] = []


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def read(path: Path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def check(label: str, ok: bool, detail=None) -> None:
    checks.append({"check": label, "passed": bool(ok), **({"detail": detail} if detail is not None else {})})
    if not ok:
        failures.append(label)


def canonical_hash(value) -> str:
    data = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return sha(data)


def git_blob(path: Path) -> str:
    return subprocess.run(
        ["git", "hash-object", str(path)], cwd=ROOT, check=True, capture_output=True, text=True
    ).stdout.strip()


def main() -> int:
    delivered = read(DELIVERY)
    zip_bytes = RETURN.read_bytes()
    with zipfile.ZipFile(RETURN) as archive:
        infos = archive.infolist()
        names = [entry.filename for entry in infos]
        corrupt = archive.testzip()
        members = {name: archive.read(name) for name in names}

    checks.append({"check": "Downloaded return ZIP matches the delivery size and SHA-256", "passed": len(zip_bytes) == delivered["bytes"] == 17790499 and sha(zip_bytes) == delivered["sha256"] == "eda99c21a4936a5fd277fcf50fdf5f4eb35a12a79f8efa262bf97f795e152bcb"})
    if not checks[-1]["passed"]:
        failures.append(checks[-1]["check"])
    check("Delivery manifest accepts exactly these ten IDs and leaves them unapplied", delivered["accepted"] is True and delivered["applied"] is False and delivered["exactAcceptedIds"] == IDS and delivered["thisReturnAcceptedUnappliedIds"] == IDS and delivered["staticAuthoredReviewBlockers"] == [])
    check("Delivery JSON is safely saved and bound to the advertised archive filename", DELIVERY.is_file() and delivered["fileName"] == RETURN.name and delivered["memberCount"] == 98)
    check("ZIP CRC passes with 98 unique, safe member paths", corrupt is None and len(names) == 98 and len(set(names)) == 98 and not [n for n in names if n.startswith(("/", "\\")) or "\\" in n or ".." in PurePosixPath(n).parts])

    external_members = {item["path"]: item for item in delivered["members"]}
    check("Delivery member map is a unique exact allowlist of every ZIP member", len(external_members) == len(delivered["members"]) == len(names) and set(external_members) == set(names))
    member_mismatches = []
    info_by_name = {entry.filename: entry for entry in infos}
    for name, entry in external_members.items():
        data = members.get(name)
        if data is None or len(data) != entry.get("bytes") or sha(data) != entry.get("sha256"):
            member_mismatches.append(name)
            continue
        expected_crc = entry.get("crc32")
        actual_crc = f"{zlib.crc32(data) & 0xffffffff:08x}"
        if expected_crc is not None and str(expected_crc).lower().removeprefix("0x") != actual_crc:
            member_mismatches.append(name)
        if info_by_name[name].CRC != zlib.crc32(data) & 0xffffffff:
            member_mismatches.append(name)
    check("All 98 members match delivery byte counts, SHA-256, and CRC32", not member_mismatches, member_mismatches[:10])
    package_checks = delivered["packageChecks"]
    check("All 297 published package checks pass", len(package_checks) == 297 and all(row.get("pass") is True for row in package_checks))

    member_manifest = json.loads(members["MEMBER_MANIFEST.json"])
    internal_manifest = {item["path"]: item for item in member_manifest["members"]}
    expected_without_manifest = {name for name in names if name != "MEMBER_MANIFEST.json"}
    check("Internal manifest covers the other 97 members without hidden or temporary entries", member_manifest["memberCountExcludingSelf"] == 97 and member_manifest["zipMemberCountIncludingSelf"] == 98 and member_manifest["noHiddenOrTemporaryMembers"] is True and set(internal_manifest) == expected_without_manifest)
    internal_mismatches = []
    for name, entry in internal_manifest.items():
        data = members.get(name)
        if data is None or len(data) != entry["bytes"] or sha(data) != entry["sha256"] or f"{zlib.crc32(data) & 0xffffffff:08x}" != entry["crc32"].lower():
            internal_mismatches.append(name)
    check("All 97 internal-manifest entries independently match", not internal_mismatches, internal_mismatches[:10])

    decision = json.loads(members["DIRECTOR_DECISION.json"])
    check("Director decision independently confirms accepted=true, applied=false, exact IDs, and no blockers", decision["accepted"] is True and decision["applied"] is False and decision["exactAcceptedIds"] == IDS and decision["unacceptedIds"] == [] and decision["staticAuthoredReviewBlockers"] == [] and decision["thisDecisionAcceptedUnappliedIds"] == IDS and decision["canonicalApplicationPerformed"] is False)
    check("Director decision and delivery bind the 739/109/0/463 baseline", decision["baselineCanonicalAuthority"]["reviewedApplied"] == 739 and decision["baselineCanonicalAuthority"]["pending"] == 109 and decision["baselineCanonicalAuthority"]["acceptedUnapplied"] == 0 and decision["baselineCanonicalAuthority"]["completeReviewedStandaloneProcedures"] == 463 and delivered["canonicalAuthorityUnchanged"] == {"appliedReviewed": 739, "pending": 109, "acceptedUnappliedBeforeThisReturn": 0, "completeStandaloneProcedures": 463})
    check("Decision does not reopen closed cohorts or approve runtime, play, balance, cosmology, domain, or release", decision["closedCohortsReopened"] == [] and all(decision[k] is False for k in ["runtimeTestsExecuted", "sourceProgramsExecuted", "humanPlaytested", "balanceApproved", "cosmologyApproved", "domainClosure", "releaseApproved"]) and all(delivered[k] is False for k in ["sourceProgramsExecuted", "runtimeTestsExecuted", "humanPlaytested", "balanceApproved", "cosmologyApproved", "domainClosure", "releaseApproved"]))
    check("Return count fields agree across delivery and model", delivered["counts"] == {"procedures": 10, "questions": 25, "mainCases": 20, "branches": 39, "cases": 59, "events": 574, "eventOperations": 2296, "proposalOperations": 40, "holds": 45, "wholeCaseHeld": 13} and delivered["holdCountQualification"] == {"localRetainedHolds": 16, "inheritedClosedScopeHoldRecords": 29, "totalRegistered": 45, "wholeCaseHeldTraces": 13})

    source_verification = json.loads(members["SOURCE_VERIFICATION.json"])
    remote_verification = json.loads(members["REMOTE_SOURCE_VERIFICATION.json"])
    source_manifest = json.loads(members["source/SOURCE_MEMBER_MANIFEST_Conference02.json"])
    source_records = json.loads(members["SOURCE_RECORDS.json"])
    check("All 265 source and preservation checks pass with no reported failure", source_verification["sourceBindingCount"] == 86 and len(source_verification["checks"]) == source_verification["passed"] == 265 and source_verification["failed"] == [] and all(row.get("pass") is True for row in source_verification["checks"]))
    check("Return is bound to the exact submitted Conference02 archive and candidate bytes", source_verification["sourceArchive"]["bytes"] == len(PACKET.read_bytes()) == 11511997 and source_verification["sourceArchive"]["sha256"] == sha(PACKET.read_bytes()) == "c0d1558b63f5fa2161ffaa7fc129fd2fc4dc148b238d7dfe06125661389d6e1f" and members["source/DD_Rank9_Catastrophe_10_Source_Conference_02.zip"] == PACKET.read_bytes() and members["source/CANDIDATE_Conference02.json"] == CANDIDATE.read_bytes())
    with zipfile.ZipFile(PACKET) as packet:
        packet_candidate = packet.read("CANDIDATE.json")
        packet_member_manifest = json.loads(packet.read("MANIFEST.json"))
    check("Submitted packet candidate is the live candidate and the return embeds its exact question source", packet_candidate == CANDIDATE.read_bytes() and packet_member_manifest["candidate"]["sha256"] == sha(CANDIDATE.read_bytes()))
    check("All 86 live source bindings in the submitted manifest still match repository files", len(source_manifest["liveCurrentSourceBindings"]) == 86 and all((ROOT / row["path"]).is_file() and (ROOT / row["path"]).stat().st_size == row["bytes"] and sha((ROOT / row["path"]).read_bytes()) == row["sha256"] for row in source_manifest["liveCurrentSourceBindings"]))
    authority = source_verification["authority"]
    authority_files_ok = True
    for key in ["index", "catalog", "currentQueue", "currentHandoff", "pendingIdentityAudit", "latestApplication", "latestExactAcceptance", "latestApplicationValidation", "latestDirectorReturnReceipt"]:
        binding = authority[key]
        path = ROOT / binding["path"]
        authority_files_ok &= path.is_file() and path.stat().st_size == binding["bytes"] and sha(path.read_bytes()) == binding["sha256"]
    check("All nine current-authority/source baseline files remain byte-identical to GPT’s bound snapshot", authority_files_ok)
    check("GitHub source commit is the packet’s exact commit and is an ancestor of this branch", remote_verification["repository"] == "BordelonDevOps/DecenniumDescent" and remote_verification["branch"] == "codex/ordinary-spell-review-complete" and remote_verification["requestedCommit"] == "ecf760fee6a8f4e2fcd711086c7c45fcec215e7b" and remote_verification["observedHead"] == remote_verification["requestedCommit"] and remote_verification["canonicalMutations"] == 0 and subprocess.run(["git", "merge-base", "--is-ancestor", remote_verification["requestedCommit"], "HEAD"], cwd=ROOT).returncode == 0 and git_blob(PACKET) == remote_verification["archiveGitBlob"] and git_blob(CANDIDATE) == remote_verification["candidateGitBlob"])

    index = read(INDEX)
    catalog = read(CATALOG)
    live_index = {row["id"]: row for row in index["entries"]}
    live_catalog = {row["id"]: row for row in catalog["spells"]}
    pending_ids = sorted(row["id"] for row in index["entries"] if row["authoredStatus"] == "pending-authored-procedure")
    check("Live canonical index remains at 739/109/0 and includes exactly these ten in the pending set", index["authoredCounts"] == {"reviewed": 739, "pending": 109} and len(pending_ids) == 109 and set(IDS).issubset(set(pending_ids)) and all(live_index[sid]["authoredStatus"] == "pending-authored-procedure" for sid in IDS))
    check("Live index and catalog still match GPT’s bound canonical hashes", len(INDEX.read_bytes()) == authority["index"]["bytes"] and sha(INDEX.read_bytes()) == authority["index"]["sha256"] and len(CATALOG.read_bytes()) == authority["catalog"]["bytes"] and sha(CATALOG.read_bytes()) == authority["catalog"]["sha256"])
    check("Current queue places these exact identities first in Rank9 Catastrophe10", read(QUEUE)["currentPendingGroups"][0]["group"] == "rank9-catastrophe10" and read(QUEUE)["currentPendingGroups"][0]["pendingIds"] == IDS and read(HANDOFF)["currentAuthority"] == AUTHORITY)

    procedures = json.loads(members["PROCEDURES.json"])
    check("Ten complete, accepted-unapplied procedures are present in exact accepted-ID order", len(procedures) == 10 and [row["id"] for row in procedures] == IDS and all(row["accepted"] is True and row["applied"] is False for row in procedures))
    source_by_id = {row["spellId"]: row for row in source_records}
    native_ok = all(
        row["completeNativeSourceAndAccess"] == source_by_id[row["id"]]["completeCurrentCatalogSourceAndAccess"]
        and row["completeNativeSourceAndAccess"] == live_catalog[row["id"]]
        and row["currentIndexEntryUnchanged"] == source_by_id[row["id"]]["currentIndexEntry"]
        and live_index[row["id"]]["sourceStatus"] == "blocked-pending-operational-review"
        and row["status"] == "accepted-static-authored-procedure-with-retained-holds-unapplied"
        for row in procedures
    )
    check("All ten procedures preserve exact native catalog/class-access rows and pending/runtime-disabled index state", native_ok)
    model = json.loads(members["MODEL.json"])
    check("Model metadata preserves all static-only, unapplied, and no-runtime qualifications", model["accepted"] is True and model["applied"] is False and model["acceptedIds"] == IDS and model["authorityAtSubmission"] == {"appliedReviewed": 739, "pending": 109, "acceptedUnapplied": 0, "standaloneProcedures": 463} and model["runtimeSelectionEnabled"] is False and all(model[k] is False for k in ["runtimeTestsExecuted", "sourceProgramsExecuted", "humanPlaytested", "balanceApproved", "cosmologyApproved", "domainClosure", "releaseApproved", "canonicalApplicationPerformed"]))

    original_questions = json.loads(members["ORIGINAL_QUESTIONS.json"])
    question_rows = json.loads(members["QUESTION_DISPOSITIONS.json"])
    candidate = json.loads(CANDIDATE.read_bytes())
    original_candidate_questions = candidate["questions"]
    check("All 25 original source questions exactly match the submitted candidate and are individually answered", len(original_questions) == len(question_rows) == len(original_candidate_questions) == 25 and [row["id"] for row in original_questions] == [row["id"] for row in question_rows] == [row["id"] for row in original_candidate_questions] and all(row["originalQuestionUnchanged"] == original_questions[i] == original_candidate_questions[i] and row.get("decisionSelected") is True and row.get("selectedOption") and row.get("selectionAndJustification") and row.get("completeProcedureIds") and row.get("holdIds") for i, row in enumerate(question_rows)))
    obligations = json.loads(members["ORIGINAL_OBLIGATIONS.json"])
    obligation_rows = json.loads(members["OBLIGATION_DISPOSITIONS.json"])
    check("All ten original review obligations are preserved and dispositioned", len(obligations) == len(obligation_rows) == 10 and all(row["originalUnchanged"] == obligations[i] and row["caseIds"] for i, row in enumerate(obligation_rows)))
    coverage = json.loads(members["COVERAGE.json"])
    check("Coverage maps every exact question and obligation to the procedure/case evidence", len(coverage["questionCoverage"]) == 25 and {row["questionId"] for row in coverage["questionCoverage"]} == {row["id"] for row in original_questions} and len(coverage["obligations"]) == 10 and len(coverage["procedures"]) == 10)

    cases = json.loads(members["CASEBOOK.json"])
    case_by_id = {case["id"]: case for case in cases}
    events = [event for case in cases for event in case["events"]]
    op_count = sum(len(event["forward"]) + len(event["inverse"]) for event in events)
    replay_failures = []
    for case in cases:
        state = case["initialState"]
        if canonical_hash(state) != case["events"][0]["beforeSHA256"] if case["events"] else False:
            replay_failures.append(f"{case['id']}:initial")
            continue
        for event in case["events"]:
            if state != event["beforeState"] or canonical_hash(state) != event["beforeSHA256"]:
                replay_failures.append(f"{case['id']}:{event['id']}:before")
                break
            try:
                after = jsonpatch.JsonPatch(event["forward"]).apply(state, in_place=False)
                if after != event["afterState"] or canonical_hash(after) != event["afterSHA256"]:
                    replay_failures.append(f"{case['id']}:{event['id']}:forward")
                    break
                restored = jsonpatch.JsonPatch(event["inverse"]).apply(after, in_place=False)
                if restored != state:
                    replay_failures.append(f"{case['id']}:{event['id']}:inverse")
                    break
                state = after
            except Exception as exc:  # Preserve the failing event and exception type in the audit.
                replay_failures.append(f"{case['id']}:{event['id']}:replay:{type(exc).__name__}")
                break
        if not any(item.startswith(case["id"] + ":") for item in replay_failures) and state != case["finalState"]:
            replay_failures.append(f"{case['id']}:final")
    check("Casebook has 59 unique cases (20 main/39 branches), 574 events, and 2,296 reversible operations", len(cases) == len(case_by_id) == 59 and sum(c["kind"] == "main" for c in cases) == 20 and sum(c["kind"] == "branch" for c in cases) == 39 and len(events) == sum(c["eventCount"] for c in cases) == 574 and op_count == sum(c["eventOperationCount"] for c in cases) == 2296 and all(c["assertsRuntime"] is False for c in cases))
    check("Independent JSON-patch replay verifies each event, inverse, state hash, and final state", not replay_failures, replay_failures[:20])
    held_cases = [case["id"] for case in cases if case["wholeCaseHeld"]]
    check("All 13 whole-case-held traces are explicitly held with retained holds", len(held_cases) == 13 and all(case_by_id[cid]["holdIds"] and case_by_id[cid]["status"].startswith("whole-case-held") for cid in held_cases))

    holds = json.loads(members["HOLD_REGISTER.json"])
    hold_ids = [row["id"] for row in holds]
    inherited_source = json.loads(members["inherited/REMAINING4_HOLD_REGISTER_169.json"])
    inherited_holds = inherited_source if isinstance(inherited_source, list) else inherited_source.get("holds", [])
    inherited_ids = {row["id"] for row in inherited_holds}
    inherited_registered = {row["id"] for row in holds if row["kind"] == "inherited-closed-scope-reference"}
    check("All 45 unique hold records remain retained; the 29 inherited records match prior hold evidence", len(holds) == len(hold_ids) == 45 and len(inherited_registered) == 29 and inherited_registered == inherited_ids and all(row["retained"] is True for row in holds))
    check("All 16 batch-specific source, access, content, physical, lifecycle, runtime, human, balance, cosmology, release, and spell-local holds remain", len(holds) - len(inherited_registered) == 16 and {"source", "access", "content", "physical", "lifecycle", "runtime", "human", "balance", "cosmology", "release"}.issubset({row["kind"] for row in holds}))

    data_validation = json.loads(members["DATA_VALIDATION.json"])
    semantic = json.loads(members["SEMANTIC_FAILURE_CHECK.json"])
    mixed = json.loads(members["MIXED_ALLOCATION_VALIDATION.json"])
    metadata = json.loads(members["METADATA_VALIDATION.json"])
    check("All 12,798 director data checks pass with zero listed failures", data_validation["checkCount"] == data_validation["passed"] == 12798 and data_validation["failures"] == [] and all(row.get("pass") is True for row in data_validation["checks"]))
    check("All 36 independent semantic failure checks pass with no unresolved blocker", semantic["checkCount"] == semantic["passed"] == 36 and semantic["blockers"] == [] and all(row.get("pass") is True for row in semantic["checks"]) and semantic["draftDefectsCorrectedBeforeDecision"])
    check("All 20 mixed-damage allocation checks pass and do not grant defenses", len(mixed["checks"]) == mixed["passed"] == 20 and all(row.get("pass") is True for row in mixed["checks"]) and len(mixed["vectors"]) == 6 and "only" in mixed["scope"])
    mixed_failures = []
    for i, vector in enumerate(mixed["vectors"]):
        inputs = vector["input"]
        budget = min(vector["authorizedFlatBudgetAssumedForAlgebraOnly"], sum(inputs.values()))
        if budget != vector["cappedBudget"]:
            mixed_failures.append(f"{i}:cap")
            continue
        exact = {kind: (Fraction(value * budget, sum(inputs.values())) if sum(inputs.values()) else Fraction(0)) for kind, value in inputs.items()}
        if {kind: str(value) for kind, value in exact.items()} != vector["exactShares"]:
            mixed_failures.append(f"{i}:shares")
            continue
        allocated = {kind: share.numerator // share.denominator for kind, share in exact.items()}
        remaining = budget - sum(allocated.values())
        order = sorted((kind for kind, share in exact.items() if share.denominator != 1), key=lambda kind: (-(exact[kind] - allocated[kind]), kind))
        for kind in order[:remaining]:
            allocated[kind] += 1
        if allocated != vector["allocation"] or {kind: inputs[kind] - allocated[kind] for kind in inputs} != vector["remaining"]:
            mixed_failures.append(f"{i}:allocation")
    check("Independent rational arithmetic reproduces all six mixed-allocation vectors", not mixed_failures, mixed_failures)
    check("All four metadata checks pass", len(metadata["checks"]) == metadata["passed"] == 4 and metadata["failed"] == [] and all(row.get("pass") is True for row in metadata["checks"]))

    proposal_ops = json.loads(members["PROPOSAL_OPERATIONS.json"])
    proposal_failures = []
    for row in proposal_ops:
        if row["executed"] is not False or row["beforeState"]["applied"] is not False or row["afterState"]["applied"] is not False:
            proposal_failures.append(row["id"] + ":scope")
        try:
            advanced = jsonpatch.JsonPatch(row["forward"]).apply(row["beforeState"], in_place=False)
            restored = jsonpatch.JsonPatch(row["inverse"]).apply(advanced, in_place=False)
            if advanced != row["afterState"] or restored != row["beforeState"]:
                proposal_failures.append(row["id"] + ":inverse")
        except Exception as exc:
            proposal_failures.append(row["id"] + ":replay:" + type(exc).__name__)
    check("Ten isolated proposal operations are reversible and none was executed against canonical files", len(proposal_ops) == 10 and sum(len(row["forward"]) + len(row["inverse"]) for row in proposal_ops) == 40 and not proposal_failures, proposal_failures)

    expected_counts = delivered["counts"]
    check("External delivery, model, and data validation agree on all published counts", model["returnCounts"] == expected_counts == data_validation["counts"])
    result = {
        "id": "RANK9-CATASTROPHE10-RETURN-INDEPENDENT-AUDIT-172",
        "status": "PASS" if not failures else "FAIL",
        "checkCount": len(checks),
        "checksPassed": len(checks) - len(failures),
        "checksFailed": len(failures),
        "failedChecks": failures,
        "checks": checks,
        "accepted": delivered["accepted"],
        "applied": delivered["applied"],
        "acceptedIds": IDS,
        "authorityBeforeApplication": AUTHORITY,
        "directorReturn": {"path": RETURN.relative_to(ROOT).as_posix(), "bytes": len(zip_bytes), "sha256": sha(zip_bytes)},
        "deliveryManifest": {"path": DELIVERY.relative_to(ROOT).as_posix(), "bytes": DELIVERY.stat().st_size, "sha256": sha(DELIVERY.read_bytes())},
        "sourceBindingsChecked": len(source_manifest["liveCurrentSourceBindings"]),
        "eventCount": len(events),
        "reversibleEventOperations": op_count,
        "heldWholeCaseCount": len(held_cases),
    }
    output = AUDIT / "RANK9_CATASTROPHE10_RETURN172_INDEPENDENT_AUDIT.json"
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({k: result[k] for k in ["id", "status", "checkCount", "checksPassed", "checksFailed", "failedChecks", "acceptedIds", "sourceBindingsChecked", "eventCount", "reversibleEventOperations", "heldWholeCaseCount"]}, indent=2))
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
