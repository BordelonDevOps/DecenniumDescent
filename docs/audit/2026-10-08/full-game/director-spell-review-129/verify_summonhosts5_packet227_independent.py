from __future__ import annotations

import hashlib
import json
import subprocess
import zipfile
import zlib
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[5]
AUDIT = ROOT / "docs/audit/2026-10-08/full-game/director-spell-review-129"
PACKET_DIR = AUDIT / "rank9_summonhosts5_current_source_227_prepared"
ARCHIVE = PACKET_DIR / "DD_Rank9_SummonHosts5_CurrentSource_227.zip"
DELIVERY = PACKET_DIR / "DD_Rank9_SummonHosts5_CurrentSource_227_DELIVERY.json"
CANDIDATE = PACKET_DIR / "CURRENT_SOURCE_CONFERENCE_CANDIDATE_227.json"
CONTEXT = PACKET_DIR / "CURRENT_CONTEXT_227.json"
REQUEST = PACKET_DIR / "REQUEST_227.txt"
PREPARATION = AUDIT / "RANK9SUMMONHOSTS5_SOURCE_PREPARATION_227.json"
REPORT = AUDIT / "RANK9SUMMONHOSTS5_PACKET_227_INDEPENDENT_AUDIT.json"
RECEIPT = AUDIT / "RANK9SUMMONHOSTS5_PACKET_227_RECEIPT.json"
TARGETS = ["summon-elemental-avatar", "summon-herald-of-the-planes", "summon-avatar-of-decay"]
CLOSED = ["conjure-magmatic-wyrm", "planar-army"]
AUTH = {"reviewedApplied": 811, "pending": 37, "acceptedUnapplied": 0,
        "completeStandaloneProcedures": 535, "scopedInterfaces": 173}


def file_hash(path: Path) -> tuple[int, str, str]:
    h, crc, size = hashlib.sha256(), 0, 0
    with path.open("rb") as stream:
        for b in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(b); crc = zlib.crc32(b, crc); size += len(b)
    return size, h.hexdigest(), f"{crc & 0xffffffff:08x}"


def member_hash(z: zipfile.ZipFile, name: str) -> tuple[int, str, str]:
    h, crc, size = hashlib.sha256(), 0, 0
    with z.open(name) as stream:
        for b in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(b); crc = zlib.crc32(b, crc); size += len(b)
    return size, h.hexdigest(), f"{crc & 0xffffffff:08x}"


def record(checks, name, passed, detail=None):
    checks.append({"check": name, "passed": bool(passed), "detail": detail})


def main():
    checks = []
    delivery = json.loads(DELIVERY.read_text(encoding="utf-8-sig"))
    candidate = json.loads(CANDIDATE.read_text(encoding="utf-8-sig"))
    context = json.loads(CONTEXT.read_text(encoding="utf-8-sig"))
    prep = json.loads(PREPARATION.read_text(encoding="utf-8-sig"))
    size, digest, crc = file_hash(ARCHIVE)
    record(checks, "Packet ZIP exact bytes/SHA/CRC match delivery manifest",
        (size, digest, crc) == (delivery["archive"]["bytes"], delivery["archive"]["sha256"], delivery["archive"]["crc32"])
        and prep["status"] == "PASS", {"bytes": size, "sha256": digest, "crc32": crc})
    with zipfile.ZipFile(ARCHIVE) as z:
        names, infos = z.namelist(), z.infolist()
        safe = all("\\" not in n and not PurePosixPath(n).is_absolute() and ".." not in PurePosixPath(n).parts for n in names)
        rows = {x["path"]: x for x in z.namelist() and json.loads(z.read("MANIFEST.json"))["members"]}
        record(checks, "323 unique safe members match internal manifest allowlist",
            len(names) == len(set(names)) == delivery["archiveMembers"] == 323
            and set(names) - {"MANIFEST.json"} == set(rows)
            and safe and z.testzip() is None,
            {"archiveMembers": len(names), "manifestMembers": len(rows), "safe": safe})
        failed = []
        for name, row in rows.items():
            if member_hash(z, name) != (row["bytes"], row["sha256"], row["crc32"].lower()):
                failed.append(name)
        record(checks, "All 322 nonmanifest ZIP members match their independent byte/SHA/CRC hashes",
            not failed, {"checked": len(rows), "failures": failed[:8]})
        manifest = json.loads(z.read("MANIFEST.json"))
        record(checks, "Internal manifest self-exclusion and authority/scope are exact",
            manifest["memberCountExcludingSelf"] == 322
            and manifest["sourceAuthority"] == AUTH
            and manifest["scope"] == TARGETS and manifest["closedAcceptedIds"] == CLOSED,
            {"count": manifest["memberCountExcludingSelf"], "scope": manifest["scope"]})
        archive_candidate = json.loads(z.read("CURRENT_SOURCE_CONFERENCE_CANDIDATE_227.json"))
        archive_context = json.loads(z.read("CURRENT_CONTEXT_227.json"))
        archive_request = z.read("REQUEST_227.txt")
        record(checks, "Candidate, context, and request in ZIP equal the submitted sidecars",
            archive_candidate == candidate and archive_context == context and archive_request == REQUEST.read_bytes(),
            {"requestBytes": len(archive_request)})
        row_failures = []
        for row in candidate["sourceBindings"]:
            p = row["path"]
            source = (ROOT / p).read_bytes()
            blob = hashlib.sha1(b"blob " + str(len(source)).encode("ascii") + b"\0" + source).hexdigest()
            zipped = member_hash(z, "sources_current/" + p)
            if (len(source), hashlib.sha256(source).hexdigest(), blob) != (row["bytes"], row["sha256"], row["gitBlobSHA1"]):
                row_failures.append(p + ":local-binding")
            if zipped != (row["bytes"], row["sha256"], f"{zlib.crc32(source) & 0xffffffff:08x}"):
                row_failures.append(p + ":zip-copy")
        record(checks, "All refreshed source rows independently match local bytes and ZIP copies",
            len(candidate["sourceBindings"]) == delivery["sourceBindings"] == 238 and not row_failures,
            {"sourceBindings": len(candidate["sourceBindings"]), "failures": row_failures[:8]})
        q = json.loads(z.read("current/docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT_SPELL_QUEUE_227.json"))
        h = json.loads(z.read("current/docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT_HANDOFF_227.json"))
        pending = json.loads(z.read("current/docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT37_PENDING_IDENTITY_AUDIT_227.json"))
        record(checks, "Embedded queue/handoff/pending audit agree on 811/37/0 and exact target group",
            q["currentAuthority"] == h["currentAuthority"] == pending["authority"] == AUTH
            and q["next"]["group"] == h["nextStep"]["group"] == "rank9-summon-hosts5"
            and q["next"]["pendingIds"] == h["nextStep"]["pendingIds"] == TARGETS
            and pending["pendingCount"] == 37 and set(TARGETS) <= set(pending["pendingIds"]),
            {"next": q["next"], "pendingCount": pending["pendingCount"]})
        ids = [x["spellId"] for x in candidate["records"]]
        record(checks, "Only three pending identities are adjudicated; prior Return202 acceptances are closed",
            ids == TARGETS and candidate["closedAcceptedSpellIds"] == CLOSED
            and context["return202AcceptedApplied"]["acceptedIds"] == CLOSED
            and context["return202AcceptedApplied"]["appliedIds"] == CLOSED
            and context["return202AcceptedApplied"]["doNotReopen"] is True,
            {"scope": ids, "closedAccepted": candidate["closedAcceptedSpellIds"]})
        record(checks, "All three target rows bind current pending entries and native catalog rows",
            all(x["currentIndexEntry"]["authoredStatus"] == "pending-authored-procedure"
                and x["currentIndexEntry"]["sourceStatus"] == "blocked-pending-operational-review"
                and x["completeCurrentCatalogSourceAndAccess"]["id"] == x["spellId"] for x in candidate["records"]),
            {"targetRows": len(candidate["records"])})
        prior202_receipt = json.loads(z.read("evidence/RETURN202_RECEIPT.json"))
        record(checks, "Current files contain Return202 acceptances, blockers, and audited Return226 scope bindings",
            context["return202AcceptedApplied"]["acceptedIds"] == CLOSED
            and context["return202AcceptedApplied"]["appliedIds"] == CLOSED
            and prior202_receipt["acceptedIds"] == CLOSED
            and set(prior202_receipt["unacceptedIds"]) == set(TARGETS)
            and context["return226AuditedOutsideScope"]["heldIds"] == ["banishment-gate", "conjure-demiplane-fortress"]
            and set(BLOCKERS_FOR_TARGETS) == set(TARGETS),
            {"return202Accepted": context["return202AcceptedApplied"]["acceptedIds"],
             "return226OutsideScope": context["return226AuditedOutsideScope"]["heldIds"]})
        package_evidence = ["evidence/RETURN226.zip", "evidence/RETURN226_DELIVERY.json",
            "evidence/RETURN226_INDEPENDENT_AUDIT.json", "evidence/RETURN226_RECEIPT.json",
            "evidence/RETURN202_DELIVERY.json", "evidence/RETURN202_INDEPENDENT_AUDIT.json",
            "evidence/RETURN202_RECEIPT.json", "evidence/RETURN202_DIRECTOR_DECISION.json",
            "evidence/RETURN202_APPLICATION.json", "evidence/RETURN202_EXACT_ACCEPTANCE.json"]
        record(checks, "All required prior director decisions, audits, receipts, and acceptance records are present",
            all(n in names for n in package_evidence), {"evidenceFiles": len(package_evidence)})

    index = json.loads((ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json").read_text(encoding="utf-8-sig"))
    catalog = json.loads((ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json").read_text(encoding="utf-8-sig"))
    status = {x["id"]: x["authoredStatus"] for x in index["entries"]}
    record(checks, "Live index confirms three targets pending and two Return202 identities already reviewed/applied",
        all(status[s] == "pending-authored-procedure" for s in TARGETS)
        and all(status[s] == "reviewed-authored-operational-playtest" for s in CLOSED)
        and all(s in {x["id"] for x in catalog["spells"]} for s in TARGETS + CLOSED),
        {"pending": [s for s in TARGETS if status[s] == "pending-authored-procedure"], "closed": CLOSED})
    recalc = file_hash(DELIVERY)
    report = {"id": "RANK9SUMMONHOSTS5-PACKET-227-INDEPENDENT-AUDIT",
        "status": "PASS" if all(c["passed"] for c in checks) else "FAIL",
        "archive": {"path": ARCHIVE.relative_to(ROOT).as_posix(), "bytes": size, "sha256": digest, "crc32": crc},
        "delivery": {"path": DELIVERY.relative_to(ROOT).as_posix(), "bytes": recalc[0], "sha256": recalc[1], "crc32": recalc[2]},
        "sourceAuthority": AUTH, "targetIds": TARGETS, "closedAcceptedIds": CLOSED,
        "checkCount": len(checks), "passedChecks": sum(c["passed"] for c in checks),
        "failedChecks": [c for c in checks if not c["passed"]], "checks": checks}
    REPORT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    receipt = {"id": "RANK9SUMMONHOSTS5-PACKET-227-RECEIPT", "status": report["status"],
        "archiveSHA256": digest, "deliverySHA256": recalc[1], "checkCount": len(checks),
        "passedChecks": report["passedChecks"], "failedChecks": len(report["failedChecks"]),
        "targetIds": TARGETS, "closedAcceptedIds": CLOSED, "sourceAuthority": AUTH}
    RECEIPT.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(receipt, indent=2))
    if report["status"] != "PASS":
        raise SystemExit(1)


BLOCKERS_FOR_TARGETS = {"summon-elemental-avatar": ["SH202-B01"], "summon-herald-of-the-planes": ["SH202-B02"],
    "summon-avatar-of-decay": ["SH202-B03"]}


if __name__ == "__main__":
    main()
