from __future__ import annotations

import hashlib
import io
import json
import subprocess
import zipfile
import zlib
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
RECEIVED = HERE / "rank9_impactexile4_return204_received"
ARCHIVE = RECEIVED / "DD_Rank9_ImpactExile4_Director_Return204_UNACCEPTED.zip"
DELIVERY = RECEIVED / "DD_Rank9_ImpactExile4_Director_Return204_UNACCEPTED_DELIVERY.json"
OUT = HERE / "RANK9IMPACTEXILE4_RETURN204_INDEPENDENT_AUDIT.json"
EXPECTED_ZIP_SHA = "b0e79fd8ca0b61730ba2ba6e04e3b4cb553147e091a0b20b57317c0d86905b3f"
SOURCE_COMMIT = "3bce65038b561b10aa572d7bb42c99bc98e770dc"
SUBMISSION_COMMIT = "d5e32c3bd3897a1dacb47944cd4c463b933ff601"
BRANCH = "codex/ordinary-spell-review-complete"
IDS = ["eternal-anvil", "reverse-gravity-field", "transmute-flesh-to-energy", "planar-collapse"]
BLOCKERS = ["IE204-B01", "IE204-B02", "IE204-B03", "IE204-B04"]
checks: list[dict] = []

def check(name: str, ok: bool, detail: str = "") -> None:
    checks.append({"check": name, "passed": bool(ok), **({"detail": detail} if detail else {})})
    if not ok:
        raise AssertionError(f"{name}: {detail}")

def digest_bytes(data: bytes) -> tuple[int, str, str]:
    return len(data), hashlib.sha256(data).hexdigest(), f"{zlib.crc32(data) & 0xffffffff:08x}"

def digest_member(archive: zipfile.ZipFile, name: str) -> tuple[int, str, str]:
    sha = hashlib.sha256()
    crc = 0
    size = 0
    with archive.open(name) as stream:
        while chunk := stream.read(8 * 1024 * 1024):
            size += len(chunk)
            sha.update(chunk)
            crc = zlib.crc32(chunk, crc)
    return size, sha.hexdigest(), f"{crc & 0xffffffff:08x}"

def member_json(archive: zipfile.ZipFile, name: str):
    return json.loads(archive.read(name).decode("utf-8"))

def git_tree(commit: str, paths: list[str]) -> dict[str, tuple[str, int]]:
    found: dict[str, tuple[str, int]] = {}
    for start in range(0, len(paths), 35):
        batch = paths[start:start + 35]
        result = subprocess.run(
            ["git", "ls-tree", "-r", "-z", "--full-tree", commit, "--", *batch],
            cwd=ROOT, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        )
        for record in result.stdout.split(b"\0"):
            if not record:
                continue
            header, raw_path = record.split(b"\t", 1)
            _mode, kind, oid = header.decode("ascii").split(" ")
            if kind == "blob":
                found[raw_path.decode("utf-8")] = (oid, -1)
    return found

def git_blob_bytes(oids: list[str]) -> list[bytes]:
    result = subprocess.run(
        ["git", "cat-file", "--batch"], cwd=ROOT, check=True,
        input=("".join(oid + "\n" for oid in oids)).encode("ascii"),
        stdout=subprocess.PIPE, stderr=subprocess.PIPE,
    )
    data = result.stdout
    offset = 0
    blobs: list[bytes] = []
    for expected in oids:
        end = data.index(b"\n", offset)
        header = data[offset:end].decode("ascii").split()
        if len(header) != 3 or header[0] != expected or header[1] != "blob":
            raise AssertionError(f"Unexpected git cat-file header: {header}")
        size = int(header[2])
        start = end + 1
        blob = data[start:start + size]
        if len(blob) != size or data[start + size:start + size + 1] != b"\n":
            raise AssertionError("Truncated git cat-file response")
        blobs.append(blob)
        offset = start + size + 1
    if offset != len(data):
        raise AssertionError("Unexpected trailing git cat-file bytes")
    return blobs

delivery = json.loads(DELIVERY.read_text(encoding="utf-8"))
archive_bytes, archive_sha, archive_crc = digest_bytes(ARCHIVE.read_bytes())
check("outer ZIP length and SHA-256 match delivery", archive_bytes == delivery["bytes"] and archive_sha == delivery["sha256"] == EXPECTED_ZIP_SHA)
check("four exact pending identities returned with no acceptance/application",
      delivery["accepted"] is False and delivery["applied"] is False and
      delivery["acceptedIds"] == [] and delivery["unacceptedIds"] == IDS and
      delivery["authority"] == {"reviewedApplied":795,"pending":53,"acceptedUnapplied":0,"completeStandaloneProcedures":519,"scopedInterfaces":173})
expected_counts = delivery["counts"]
check("delivery counts record 26 questions, 2 addenda, 8 cases, 36 total, and 7 future obligations",
      expected_counts["originalQuestions"] == 26 and expected_counts["focusedAddenda"] == 2 and
      expected_counts["requiredMainCases"] == expected_counts["mainCases"] == 8 and
      expected_counts["branches"] == 28 and expected_counts["cases"] == 36 and
      expected_counts["futureObligations"] == 7)
check("delivery records zero procedures and four blocking identities",
      expected_counts["procedures"] == expected_counts["passingProceduresReturned"] == 0 and
      expected_counts["blockingIdentityDecisions"] == 4 and expected_counts["untracedCaseObligations"] == 9)

with zipfile.ZipFile(ARCHIVE, "r") as outer:
    infos = outer.infolist()
    names = [item.filename for item in infos]
    declared = {item["path"]: item for item in delivery["members"]}
    check("archive member names are unique and exactly match delivery allowlist",
          len(names) == len(set(names)) and set(names) == set(declared) and len(names) == delivery["archiveMemberCount"])
    check("archive paths contain no traversal",
          all(not n.startswith(("/", "\\")) and ".." not in Path(n).parts for n in names))
    check("ZIP central-directory CRC test passes", outer.testzip() is None)
    for name in names:
        size, sha, crc = digest_member(outer, name)
        expected = declared[name]
        check(f"member size/SHA/CRC verified: {name}",
              size == expected["bytes"] and sha == expected["sha256"] and crc == expected["crc32"])

    embedded = member_json(outer, "MANIFEST.json")
    embedded_members = {item["path"]: item for item in embedded["members"]}
    check("embedded manifest excludes only itself and matches delivery entries",
          embedded["memberCountExcludingSelf"] == 76 and
          set(embedded_members) == set(declared) - {"MANIFEST.json"} and
          all(embedded_members[k] == declared[k] for k in embedded_members))

    decision = member_json(outer, "DIRECTOR_DECISION.json")
    procedures = member_json(outer, "PROCEDURES.json")
    questions = member_json(outer, "QUESTION_DISPOSITIONS.json")
    cases = member_json(outer, "CASE_INDEX.json")
    semantic = member_json(outer, "INDEPENDENT_SEMANTIC_FAILURE_CHECK.json")
    blockers = member_json(outer, "OUTSTANDING_CASE_OBLIGATIONS.json")
    source_verification = member_json(outer, "SOURCE_VERIFICATION.json")
    source_delivery = member_json(outer, "SOURCE_DELIVERY_203.json")
    source_proof = member_json(outer, "source_proofs/GIT_SOURCE_PROOF.json")
    supplemental_proof = member_json(outer, "source_proofs/SUPPLEMENTAL_GIT_PROOF.json")
    withheld = member_json(outer, "WITHHELD_DRAFT_BINDINGS.json")

    check("director decision agrees with delivery and preserves 795/53",
          decision["id"] == "RANK9-IMPACTEXILE4-DIRECTOR-RETURN204" and
          decision["acceptedIds"] == [] and decision["unacceptedIds"] == IDS and
          decision["authority"] == delivery["authority"] and
          all(x["accepted"] is False and x["applied"] is False for x in decision["perIdentity"]))
    check("all four exact IE204 blockers are present",
          [x["blockerIds"][0] for x in decision["perIdentity"]] == BLOCKERS and
          [x["id"] for x in semantic["blockers"]] == BLOCKERS)
    check("all 28 question dispositions are explicit and acceptance remains false",
          questions["originalCount"] == 26 and questions["addendumCount"] == 2 and
          questions["answeredCount"] == 28 and len(questions["dispositions"]) == 28 and
          all(x["decisionSelected"] is True and x["accepted"] is False for x in questions["dispositions"]))
    check("case index covers 8 main cases plus 28 branches and 1,255 events",
          len(cases) == 36 and sum(x["events"] for x in cases) == 1255 and
          sum(x["kind"] == "main" for x in cases) == 8 and sum(x["kind"] == "branch" for x in cases) == 28)
    check("semantic gate correctly blocks all four identities",
          semantic["status"] == "FAIL" and len(semantic["checks"]) == 16 and
          sum(x["pass"] is True for x in semantic["checks"]) == 12 and
          sum(x["pass"] is False for x in semantic["checks"]) == 4 and
          procedures["spells"] == [] and procedures["passingProcedureCount"] == 0)
    check("four unaccepted drafts are preserved only by hash bindings",
          len(withheld["perIdentity"]) == 4 and all(x["accepted"] is False and x["applied"] is False for x in withheld["perIdentity"]))
    check("source verification summary passes 354 checks and binds expected source commit",
          source_verification["status"] == "PASS" and source_verification["checkCount"] == 354 and
          all(x["pass"] is True for x in source_verification["checks"]) and
          source_verification["sourceCommit"] == SOURCE_COMMIT)
    check("input packet delivery remains the prepared packet 203 at 795/53",
          source_delivery["sourceCommit"] == SOURCE_COMMIT and source_delivery["sourceAuthority"]["pending"] == 53 and
          source_delivery["archive"]["sha256"] == "24cd072f6db6b9a65fe399fe1692a3635251e785f06f1e454e2675df5b922d84")

    source_packet_bytes = outer.read("SOURCE_PACKET_203.zip")
    packet_size, packet_sha, _ = digest_bytes(source_packet_bytes)
    check("nested packet bytes match the packet 203 delivery record",
          packet_sha == source_delivery["archive"]["sha256"] and packet_size == source_delivery["archive"]["bytes"])
    with zipfile.ZipFile(io.BytesIO(source_packet_bytes), "r") as packet:
        packet_names = packet.namelist()
        check("nested packet central-directory CRC test passes", packet.testzip() is None)
        candidate = member_json(packet, "CURRENT_SOURCE_CONFERENCE_CANDIDATE_203.json")
        bindings = candidate["sourceBindings"]
        check("all 149 refreshed candidate bindings exist in sources_current",
              len(bindings) == 149 and {b["path"] for b in bindings} ==
              {n[len("sources_current/"):] for n in packet_names if n.startswith("sources_current/")})
        for binding in bindings:
            raw = packet.read("sources_current/" + binding["path"])
            size, sha, _ = digest_bytes(raw)
            check(f"refreshed source binding verified: {binding['path']}",
                  size == binding["bytes"] and sha == binding["sha256"])
        check("candidate binds source commit and current group",
              candidate["currentSourceCommit"] == SOURCE_COMMIT and
              candidate["currentBranch"] == BRANCH and
              candidate["currentPendingGroup"]["spellIds"] == IDS)

    proof_rows = source_proof["verified"]
    check("GitHub source proof has 177 paths and no errors",
          source_proof["commit"]["sha"] == SOURCE_COMMIT and len(proof_rows) == 177 and source_proof["errors"] == [])
    proof_paths = [x["path"] for x in proof_rows]
    tree = git_tree(SOURCE_COMMIT, proof_paths)
    check("all 177 source proof paths resolve in the local Git commit", len(tree) == 177)
    oids = []
    for row in proof_rows:
        oid = tree[row["path"]][0]
        check(f"Git tree object ID matches proof: {row['path']}",
              oid == row["gitBlobSHA1"] == row["treeBlob"]["sha"] and row["treeBlob"]["size"] == row["bytes"])
        oids.append(oid)
    blobs = git_blob_bytes(oids)
    for row, blob in zip(proof_rows, blobs):
        check(f"local Git blob bytes match source proof: {row['path']}",
              len(blob) == row["bytes"] and hashlib.sha256(blob).hexdigest() == row["sha256"])

    supplemental = supplemental_proof["blobs"]
    check("nine supplemental source blobs are bound to the same source commit",
          supplemental_proof["commit"] == SOURCE_COMMIT and len(supplemental) == 9)
    for item in supplemental:
        raw = outer.read("supplemental_sources/" + item["path"])
        check(f"supplemental source bytes match Git proof: {item['path']}",
              len(raw) == item["size"] and hashlib.sha1(b"blob " + str(len(raw)).encode("ascii") + b"\0" + raw).hexdigest() == item["sha"])

    qualification = delivery["qualifications"]
    check("no canonical edits, supplied program execution, or broader approval claimed",
          qualification["canonicalFilesChanged"] is False and qualification["suppliedProgramsExecuted"] is False and
          qualification["historicalProgramsExecuted"] is False and qualification["runtimeApproval"] is False and
          qualification["implementationApproval"] is False and qualification["humanPlayApproval"] is False and
          qualification["balanceApproval"] is False and qualification["cosmologyApproval"] is False and
          qualification["domainClosure"] is False and qualification["completionClaim"] is False and
          qualification["releaseApproval"] is False)

head = subprocess.run(["git","rev-parse","HEAD"], cwd=ROOT, check=True, text=True, capture_output=True).stdout.strip()
remote = subprocess.run(["git","ls-remote","origin",f"refs/heads/{BRANCH}"], cwd=ROOT, check=True, text=True, capture_output=True).stdout.split()
remote_head = remote[0] if remote else None
check("submission commit is the pushed current branch head",
      head == SUBMISSION_COMMIT and remote_head == SUBMISSION_COMMIT,
      f"local={head}; remote={remote_head}")

report = {
    "id": "RANK9-IMPACTEXILE4-RETURN204-INDEPENDENT-AUDIT",
    "status": "PASS",
    "recordedAtUtc": __import__("datetime").datetime.now(__import__("datetime").timezone.utc).isoformat(),
    "sourceCommit": SOURCE_COMMIT,
    "submissionCommit": SUBMISSION_COMMIT,
    "branch": BRANCH,
    "archive": {"path": str(ARCHIVE.relative_to(ROOT)).replace("\\", "/"), "bytes": archive_bytes, "sha256": archive_sha},
    "delivery": {"path": str(DELIVERY.relative_to(ROOT)).replace("\\", "/"), "bytes": DELIVERY.stat().st_size, "sha256": hashlib.sha256(DELIVERY.read_bytes()).hexdigest()},
    "authorityUnchanged": delivery["authority"],
    "acceptedIds": [],
    "unacceptedIds": IDS,
    "blockers": [
        {"id":"IE204-B01","spellId":"eternal-anvil","missing":"suppression/resumption and complete manifestation geometry"},
        {"id":"IE204-B02","spellId":"reverse-gravity-field","missing":"sourced object aftermath and rated attachment evidence"},
        {"id":"IE204-B03","spellId":"transmute-flesh-to-energy","missing":"corpse-recast and changed-form anatomy traces"},
        {"id":"IE204-B04","spellId":"planar-collapse","missing":"warded return, immunity, removal, and admitted-body lifecycle"}
    ],
    "counts": delivery["counts"],
    "sourceProofPathsChecked": len(proof_rows),
    "refreshedSourceBindingsChecked": len(candidate["sourceBindings"]),
    "supplementalBindingsChecked": len(supplemental),
    "checksPassed": len(checks),
    "checksFailed": 0,
    "checks": checks,
    "decision": "Unaccepted and unapplied. No identities qualify for application; preserve all four drafts and exact holds."
}
OUT.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print(json.dumps({"status":report["status"],"checksPassed":report["checksPassed"],"checksFailed":0,"sourceProofPaths":len(proof_rows),"refreshedBindings":len(candidate["sourceBindings"]),"archiveSha256":archive_sha,"remoteHead":remote_head,"audit":str(OUT.relative_to(ROOT))},indent=2))
