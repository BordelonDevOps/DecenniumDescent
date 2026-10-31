from __future__ import annotations

import hashlib
import json
import subprocess
import zipfile
import zlib
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[5]
AUDIT = ROOT / "docs/audit/2026-10-08/full-game/director-spell-review-129"
PACKET_DIR = AUDIT / "rank9_summonhosts5_current_source_285_prepared"
ARCHIVE = PACKET_DIR / "DD_Rank9_SummonHosts5_CurrentSource_285.zip"
DELIVERY = PACKET_DIR / "DD_Rank9_SummonHosts5_CurrentSource_285_DELIVERY.json"
CANDIDATE = PACKET_DIR / "CURRENT_SOURCE_CONFERENCE_CANDIDATE_285.json"
CONTEXT = PACKET_DIR / "CURRENT_CONTEXT_285.json"
REQUEST = PACKET_DIR / "REQUEST_285.txt"
PREPARATION = AUDIT / "RANK9SUMMONHOSTS5_SOURCE_PREPARATION_285.json"
REPORT = AUDIT / "RANK9SUMMONHOSTS5_PACKET_285_INDEPENDENT_AUDIT.json"
RECEIPT = AUDIT / "RANK9SUMMONHOSTS5_PACKET_285_RECEIPT.json"
RETURN284_AUDIT = AUDIT / "RANK9_PLANARGATES5_RETURN284_INDEPENDENT_AUDIT.json"
TARGETS = ["summon-elemental-avatar", "summon-herald-of-the-planes", "summon-avatar-of-decay"]
CLOSED = ["conjure-magmatic-wyrm", "planar-army"]
AUTH = {"reviewedApplied": 816, "pending": 32, "acceptedUnapplied": 0,
        "completeStandaloneProcedures": 540, "scopedInterfaces": 173}


def file_hash(path: Path) -> tuple[int, str, str]:
    h, c, n = hashlib.sha256(), 0, 0
    with path.open("rb") as f:
        for b in iter(lambda: f.read(1024 * 1024), b""):
            h.update(b); c = zlib.crc32(b, c); n += len(b)
    return n, h.hexdigest(), f"{c & 0xffffffff:08x}"


def member_hash(z: zipfile.ZipFile, name: str) -> tuple[int, str, str]:
    h, c, n = hashlib.sha256(), 0, 0
    with z.open(name) as f:
        for b in iter(lambda: f.read(1024 * 1024), b""):
            h.update(b); c = zlib.crc32(b, c); n += len(b)
    return n, h.hexdigest(), f"{c & 0xffffffff:08x}"


def record(checks: list[dict], name: str, passed: bool, detail=None) -> None:
    checks.append({"check": name, "passed": bool(passed), "detail": detail})


def main() -> None:
    checks: list[dict] = []
    delivery = json.loads(DELIVERY.read_text(encoding="utf-8-sig"))
    candidate = json.loads(CANDIDATE.read_text(encoding="utf-8-sig"))
    context = json.loads(CONTEXT.read_text(encoding="utf-8-sig"))
    prep = json.loads(PREPARATION.read_text(encoding="utf-8-sig"))
    archive_info = file_hash(ARCHIVE); delivery_info = file_hash(DELIVERY)
    record(checks, "Packet285 ZIP exact byte/SHA/CRC values match its delivery manifest",
        archive_info == (delivery["archive"]["bytes"], delivery["archive"]["sha256"], delivery["archive"]["crc32"].lower())
        and prep["status"] == "PASS" and delivery["status"] == "PREPARED_UNSENT",
        {"bytes": archive_info[0], "sha256": archive_info[1], "crc32": archive_info[2]})
    with zipfile.ZipFile(ARCHIVE) as z:
        names = z.namelist(); name_set = set(names)
        safe = all("\\" not in n and not PurePosixPath(n).is_absolute() and ".." not in PurePosixPath(n).parts for n in names)
        manifest = json.loads(z.read("MANIFEST.json")); rows = {x["path"]: x for x in manifest["members"]}
        record(checks, "428 unique safe members match the archive manifest",
            len(names) == len(name_set) == delivery["archiveMembers"] == 428
            and manifest["memberCountExcludingSelf"] == 427 and set(names) - {"MANIFEST.json"} == set(rows)
            and safe and z.testzip() is None,
            {"archiveMembers": len(names), "manifestMembers": len(rows), "safe": safe})
        failures = [name for name, row in rows.items() if member_hash(z, name) !=
            (row["bytes"], row["sha256"], row["crc32"].lower())]
        record(checks, "All 427 nonmanifest members match their byte/SHA/CRC manifest rows",
            not failures, {"checked": len(rows), "failures": failures[:8]})
        record(checks, "Manifest declares the exact current authority, target scope, and closed acceptances",
            manifest["sourceAuthority"] == AUTH and manifest["scope"] == TARGETS and manifest["closedAcceptedIds"] == CLOSED,
            {"authority": manifest["sourceAuthority"], "scope": manifest["scope"], "closed": manifest["closedAcceptedIds"]})
        embedded_candidate = json.loads(z.read("CURRENT_SOURCE_CONFERENCE_CANDIDATE_285.json"))
        embedded_context = json.loads(z.read("CURRENT_CONTEXT_285.json"))
        record(checks, "Candidate, context, and request inside ZIP equal the sidecars",
            embedded_candidate == candidate and embedded_context == context and z.read("REQUEST_285.txt") == REQUEST.read_bytes(),
            {"requestBytes": len(z.read("REQUEST_285.txt"))})

        row_failures = []
        for row in candidate["sourceBindings"]:
            path = row["path"]; raw = (ROOT / path).read_bytes()
            blob = hashlib.sha1(b"blob " + str(len(raw)).encode("ascii") + b"\0" + raw).hexdigest()
            if (len(raw), hashlib.sha256(raw).hexdigest(), blob) != (row["bytes"], row["sha256"], row["gitBlobSHA1"]):
                row_failures.append(path + ":working-tree-binding")
            if member_hash(z, "sources_current/" + path) != (row["bytes"], row["sha256"], f"{zlib.crc32(raw) & 0xffffffff:08x}"):
                row_failures.append(path + ":archive-copy")
        record(checks, "All 280 source bindings independently match current working-tree bytes and ZIP copies",
            len(candidate["sourceBindings"]) == delivery["sourceBindings"] == 280 and not row_failures,
            {"sourceBindings": len(candidate["sourceBindings"]), "failures": row_failures[:8]})

        q = json.loads(z.read("current/docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT_SPELL_QUEUE_285.json"))
        h = json.loads(z.read("current/docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT_HANDOFF_285.json"))
        pending = json.loads(z.read("current/docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT32_PENDING_IDENTITY_AUDIT_285.json"))
        record(checks, "Embedded queue, handoff, and pending audit agree on 816/32/0 and the three target IDs",
            q["currentAuthority"] == h["currentAuthority"] == pending["authority"] == AUTH
            and q["next"]["group"] == h["nextStep"]["group"] == "rank9-summon-hosts5"
            and q["next"]["pendingIds"] == h["nextStep"]["pendingIds"] == TARGETS
            and pending["pendingCount"] == 32 and set(TARGETS) <= set(pending["pendingIds"]),
            {"nextGroup": q["next"]["group"], "pendingCount": pending["pendingCount"]})
        ids = [x["spellId"] for x in candidate["records"]]
        record(checks, "Only three pending Summon Hosts identities are in scope; Return202 acceptances remain closed",
            ids == TARGETS and candidate["closedAcceptedSpellIds"] == CLOSED
            and context["closedAcceptedReturn202"]["acceptedIds"] == CLOSED
            and context["closedAcceptedReturn202"]["appliedIds"] == CLOSED
            and context["closedAcceptedReturn202"]["doNotReopen"] is True,
            {"scope": ids, "closedAccepted": candidate["closedAcceptedSpellIds"]})
        record(checks, "All target rows bind current pending index entries and native catalog records",
            all(x["currentIndexEntry"]["authoredStatus"] == "pending-authored-procedure"
                and x["currentIndexEntry"]["sourceStatus"] == "blocked-pending-operational-review"
                and x["completeCurrentCatalogSourceAndAccess"]["id"] == x["spellId"] for x in candidate["records"]),
            {"targetRows": len(candidate["records"])})
        return284 = json.loads(z.read("evidence/RETURN284_INDEPENDENT_AUDIT.json"))
        record(checks, "Return284 was independently audited and its two Planar holds remain explicitly out of scope",
            return284["status"] == "PASS" and return284["checksPassed"] == 18
            and set(return284["heldIds"]) == {"banishment-gate", "conjure-demiplane-fortress"}
            and context["return284PlanarGatesHoldOutsideScope"]["heldIds"] == ["banishment-gate", "conjure-demiplane-fortress"],
            {"return284Status": return284["status"], "heldIds": return284["heldIds"]})
        evidence_names = ["evidence/RETURN284.zip", "evidence/RETURN284_DELIVERY.json", "evidence/RETURN284_INDEPENDENT_AUDIT.json",
            "evidence/RETURN284_RECEIPT.json", "evidence/PACKET284_DELIVERY.json", "evidence/PACKET284_INDEPENDENT_AUDIT.json",
            "evidence/PACKET284_RECEIPT.json", "evidence/RETURN244.zip", "evidence/RETURN244_DELIVERY.json",
            "evidence/RETURN244_INDEPENDENT_AUDIT.json", "evidence/RETURN244_RECEIPT.json", "evidence/RETURN202_INDEPENDENT_AUDIT.json",
            "evidence/RETURN202_RECEIPT.json", "evidence/RETURN202_DECISION.json", "evidence/RETURN202_APPLICATION.json",
            "evidence/RETURN202_EXACT_ACCEPTANCE.json", "evidence/RETURN202_APPLICATION_VALIDATION.json"]
        record(checks, "Sealed prior returns, audits, receipts, and acceptance/application records are present",
            all(name in name_set for name in evidence_names), {"evidenceFiles": len(evidence_names)})

    index = json.loads((ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json").read_text(encoding="utf-8-sig"))
    catalog = json.loads((ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json").read_text(encoding="utf-8-sig"))
    status = {x["id"]: x["authoredStatus"] for x in index["entries"]}
    catalog_ids = {x["id"] for x in catalog["spells"]}
    record(checks, "Live index confirms 816 reviewed and 32 pending, with target/closed identities in expected states",
        index["authoredCounts"] == {"reviewed": 816, "pending": 32}
        and all(status[s] == "pending-authored-procedure" for s in TARGETS)
        and all(status[s] == "reviewed-authored-operational-playtest" for s in CLOSED)
        and set(TARGETS + CLOSED) <= catalog_ids,
        {"targetPending": [s for s in TARGETS if status.get(s) == "pending-authored-procedure"], "closed": CLOSED})
    branch = subprocess.check_output(["git", "branch", "--show-current"], cwd=ROOT, text=True).strip()
    head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    record(checks, "Packet source binding reports current main branch and current checkout commit",
        branch == "main" and candidate["currentBranch"] == branch and candidate["currentSourceCommit"] == head
        and delivery["sourceBranch"] == branch and delivery["sourceCommit"] == head,
        {"branch": branch, "head": head})
    record(checks, "Return284 audit remains PASS in the current repository record",
        json.loads(RETURN284_AUDIT.read_text(encoding="utf-8-sig"))["status"] == "PASS",
        {"audit": RETURN284_AUDIT.name})

    failures = [c for c in checks if not c["passed"]]
    report = {"id": "RANK9SUMMONHOSTS5-PACKET-285-INDEPENDENT-AUDIT",
        "status": "PASS" if not failures else "FAIL", "archive": {"path": ARCHIVE.relative_to(ROOT).as_posix(),
            "bytes": archive_info[0], "sha256": archive_info[1], "crc32": archive_info[2]},
        "delivery": {"path": DELIVERY.relative_to(ROOT).as_posix(), "bytes": delivery_info[0],
            "sha256": delivery_info[1], "crc32": delivery_info[2]}, "sourceAuthority": AUTH,
        "targetIds": TARGETS, "closedAcceptedIds": CLOSED, "checkCount": len(checks),
        "passedChecks": sum(c["passed"] for c in checks), "failedChecks": failures, "checks": checks}
    REPORT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    receipt = {"id": "RANK9SUMMONHOSTS5-PACKET-285-RECEIPT", "status": report["status"],
        "archiveSHA256": archive_info[1], "deliverySHA256": delivery_info[1], "checkCount": len(checks),
        "passedChecks": report["passedChecks"], "failedChecks": len(failures), "targetIds": TARGETS,
        "closedAcceptedIds": CLOSED, "sourceAuthority": AUTH}
    RECEIPT.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(receipt, indent=2))
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
