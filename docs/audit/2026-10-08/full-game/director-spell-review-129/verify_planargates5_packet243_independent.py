from __future__ import annotations

import hashlib
import json
import zipfile
import zlib
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[5]
AUDIT = ROOT / "docs/audit/2026-10-08/full-game/director-spell-review-129"
OUT = AUDIT / "rank9_planargates5_current_source_243_prepared"
ARCHIVE = OUT / "DD_Rank9_PlanarGates5_CurrentSource_243.zip"
DELIVERY = OUT / "DD_Rank9_PlanarGates5_CurrentSource_243_DELIVERY.json"
CANDIDATE = OUT / "CURRENT_SOURCE_CONFERENCE_CANDIDATE_243.json"
CONTEXT = OUT / "CURRENT_CONTEXT_243.json"
REQUEST = OUT / "REQUEST_243.txt"
QUEUE = AUDIT / "CURRENT_SPELL_QUEUE_243.json"
HANDOFF = AUDIT / "CURRENT_HANDOFF_243.json"
PENDING = AUDIT / "CURRENT37_PENDING_IDENTITY_AUDIT_242.json"
RETURN242_DIR = AUDIT / "rank9_knowledgerevelation5_return242_received"
RETURN242 = RETURN242_DIR / "DD_Rank9_FactionOmniscienceSupreme_Director_Return242_HELD.zip"
RETURN242_DELIVERY = RETURN242_DIR / "DD_Rank9_FactionOmniscienceSupreme_Director_Return242_HELD_DELIVERY.json"
RETURN242_AUDIT = AUDIT / "RANK9_KNOWLEDGEREVELATION5_RETURN242_INDEPENDENT_AUDIT.json"
RETURN200_AUDIT = AUDIT / "RANK9_PLANARGATES5_RETURN200_INDEPENDENT_AUDIT.json"
RETURN200_APPLICATION = AUDIT / "RANK9_PLANARGATES5_APPLICATION_200.json"
REPORT = AUDIT / "RANK9PLANARGATES5_PACKET_243_INDEPENDENT_AUDIT.json"
RECEIPT = AUDIT / "RANK9PLANARGATES5_PACKET_243_RECEIPT.json"
AUTH = {"reviewedApplied": 811, "pending": 37, "acceptedUnapplied": 0,
        "completeStandaloneProcedures": 535, "scopedInterfaces": 173}
TARGET = ["banishment-gate", "conjure-demiplane-fortress"]
CLOSED = ["gate", "absolute-gate", "planar-sanctuary"]


def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def crc(b: bytes) -> str:
    return f"{zlib.crc32(b) & 0xffffffff:08x}"


def blobsha(b: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(b)).encode("ascii") + b"\0" + b).hexdigest()


def safe(name: str) -> bool:
    p = PurePosixPath(name)
    return bool(name) and not p.is_absolute() and ".." not in p.parts and "\\" not in name


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def member_binding(zf: zipfile.ZipFile, name: str) -> dict:
    h = hashlib.sha256(); c = 0; n = 0
    with zf.open(name) as f:
        for b in iter(lambda: f.read(1024 * 1024), b""):
            h.update(b); c = zlib.crc32(b, c); n += len(b)
    return {"bytes": n, "sha256": h.hexdigest(), "crc32": f"{c & 0xffffffff:08x}"}


def main() -> None:
    d = read_json(DELIVERY); candidate = read_json(CANDIDATE); context = read_json(CONTEXT)
    queue = read_json(QUEUE); handoff = read_json(HANDOFF); pending = read_json(PENDING)
    checks: list[dict] = []

    def check(name: str, passed: bool, detail=None) -> None:
        checks.append({"check": name, "passed": bool(passed), "detail": detail})

    archive_raw = ARCHIVE.read_bytes()
    outer = {"bytes": len(archive_raw), "sha256": sha(archive_raw), "crc32": crc(archive_raw)}
    check("Current packet archive matches delivery byte/SHA/CRC binding",
          all(outer[k] == d["archive"][k] for k in ("bytes", "sha256", "crc32")), outer)
    check("Exact scope and authority are bound across delivery, context, candidate, queue, and handoff",
          d["group"] == "rank9-planar-gates5" and d["pendingIds"] == TARGET and d["sourceAuthority"] == AUTH
          and context["sourceAuthority"] == AUTH and candidate["currentAuthority"] == AUTH
          and candidate["currentPendingGroup"] == {"group": "rank9-planar-gates5", "spellIds": TARGET, "count": 2}
          and queue["currentAuthority"] == AUTH and queue["nextGroup"] == "rank9-planar-gates5"
          and handoff["currentAuthority"] == AUTH and handoff["nextGroup"] == "rank9-planar-gates5",
          {"target": d["pendingIds"], "authority": d["sourceAuthority"]})
    check("Return200 applied Planar identities remain closed and only the two pending identities are scoped",
          d["closedAcceptedIds"] == CLOSED and [x["spellId"] for x in candidate["records"]] == TARGET
          and candidate["closedAcceptedSpellIds"] == CLOSED
          and context["priorPlanarGateReturn200"]["acceptedIds"] == CLOSED
          and context["priorPlanarGateReturn200"]["appliedIds"] == CLOSED,
          {"closed": d["closedAcceptedIds"], "records": [x["spellId"] for x in candidate["records"]]})
    idx = json.loads((ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json").read_text(encoding="utf-8-sig"))["entries"]
    index_entries = {x["id"]: x for x in idx}
    check("Current pending audit has 37 rows and selected targets are pending in the authored index",
          pending["pendingCount"] == 37 and all(x in pending["pendingIds"] for x in TARGET)
          and all(index_entries[x]["authoredStatus"] == "pending-authored-procedure" for x in TARGET),
          {"pendingCount": pending["pendingCount"], "targets": TARGET})
    lr = context["latestCurrentReturn"]
    check("Return242 is independently audited, held only outside this scope, and selects this exact next group",
          lr["return"] == 242 and lr["heldIds"] == ["faction-omniscience-supreme"]
          and lr["blockerIds"] == ["KR198-B01"]
          and lr["independentAudit"]["path"].endswith("RANK9_KNOWLEDGEREVELATION5_RETURN242_INDEPENDENT_AUDIT.json"), lr)
    check("Candidate preserves all 30 questions and nine future obligations while scoping two records",
          len(candidate["questions"]) == 30 and len(candidate["futureCaseRequirements"]) == 9
          and {x["spellId"] for x in candidate["records"]} == set(TARGET),
          {"questions": len(candidate["questions"]), "futureRequirements": len(candidate["futureCaseRequirements"])})

    with zipfile.ZipFile(ARCHIVE) as z:
        names = z.namelist()
        check("ZIP CRCs, unique safe paths, and internal manifest pass",
              z.testzip() is None and len(names) == len(set(names)) and all(safe(n) for n in names)
              and "MANIFEST.json" in names,
              {"memberCount": len(names), "unsafe": [n for n in names if not safe(n)]})
        manifest = json.loads(z.read("MANIFEST.json")); rows = {r["path"]: r for r in manifest["members"]}
        manifest_ok = set(names) - {"MANIFEST.json"} == set(rows) and manifest["memberCountExcludingSelf"] == len(rows)
        failures = []
        if manifest_ok:
            for name, row in rows.items():
                if member_binding(z, name) != {k: row[k] for k in ("bytes", "sha256", "crc32")}:
                    failures.append(name)
        check("Every ZIP member matches internal byte/SHA/CRC manifest", manifest_ok and not failures,
              {"members": len(rows), "failures": failures[:10]})
        check("Candidate, context, and request in ZIP are byte-identical to prepared files",
              z.read("CURRENT_SOURCE_CONFERENCE_CANDIDATE_243.json") == CANDIDATE.read_bytes()
              and z.read("CURRENT_CONTEXT_243.json") == CONTEXT.read_bytes()
              and z.read("REQUEST_243.txt") == REQUEST.read_bytes(), None)
        source_failures = []
        for row in candidate["sourceBindings"]:
            name = "sources_current/" + row["path"]
            if name not in names:
                source_failures.append({"path": row["path"], "reason": "missing member"}); continue
            actual = member_binding(z, name)
            if actual["bytes"] != row["bytes"] or actual["sha256"] != row["sha256"]:
                source_failures.append({"path": row["path"], "reason": "binding mismatch"})
            else:
                with z.open(name) as f:
                    raw = f.read()
                if blobsha(raw) != row["gitBlobSHA1"]:
                    source_failures.append({"path": row["path"], "reason": "Git blob mismatch"})
        check("All bound current source files match embedded byte/SHA/Git-blob identities",
              len(candidate["sourceBindings"]) == 161 and not source_failures,
              {"rows": len(candidate["sourceBindings"]), "failures": source_failures[:10]})
        r242_audit = json.loads(z.read("evidence/RETURN242_INDEPENDENT_AUDIT.json"))
        r200_audit = json.loads(z.read("evidence/PLANARGATES5_RETURN200_INDEPENDENT_AUDIT.json"))
        r200_app = json.loads(z.read("evidence/PLANARGATES5_RETURN200_APPLICATION.json"))
        check("Return242 audit and Return200 planar audit/application are embedded and consistent",
              r242_audit["status"] == "PASS" and r242_audit["checksPassed"] == 15
              and r200_audit["status"] == "PASS" and r200_app["acceptedIds"] == CLOSED,
              {"return242": r242_audit["status"], "return242Checks": r242_audit["checksPassed"],
               "return200": r200_audit["status"], "closedApplied": r200_app["acceptedIds"]})
        check("Current handoff and queue snapshots match local packet inputs",
              z.read("current/" + QUEUE.relative_to(ROOT).as_posix()) == QUEUE.read_bytes()
              and z.read("current/" + HANDOFF.relative_to(ROOT).as_posix()) == HANDOFF.read_bytes()
              and z.read("current/" + PENDING.relative_to(ROOT).as_posix()) == PENDING.read_bytes(), None)
        embedded_index = json.loads(z.read("current/DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json"))
        embedded = {x["id"]: x for x in embedded_index["entries"]}
        check("Embedded index preserves the two pending targets and three accepted Planar identities",
              all(embedded[x]["authoredStatus"] == "pending-authored-procedure" for x in TARGET)
              and all(embedded[x]["authoredStatus"] == "reviewed-authored-operational-playtest" for x in CLOSED),
              {x: embedded[x]["authoredStatus"] for x in TARGET + CLOSED})
        check("Queue and handoff select only two Planar spells and retain Return242 hold",
              queue["next"]["pendingIds"] == TARGET and queue["next"]["pendingCount"] == 2
              and handoff["nextStep"]["pendingIds"] == TARGET
              and handoff["latestBatch"]["heldIds"] == ["faction-omniscience-supreme"],
              {"next": queue["next"], "sourceRows": len(candidate["sourceBindings"])})

    failures = [x for x in checks if not x["passed"]]
    report = {"id": "RANK9-PLANARGATES5-PACKET243-INDEPENDENT-AUDIT",
        "status": "PASS" if not failures else "FAIL", "checksPassed": len(checks) - len(failures),
        "checksFailed": len(failures), "archive": {"path": ARCHIVE.relative_to(ROOT).as_posix(), **outer},
        "delivery": {"path": DELIVERY.relative_to(ROOT).as_posix(), "bytes": DELIVERY.stat().st_size,
            "sha256": sha(DELIVERY.read_bytes())}, "authority": AUTH, "pendingIds": TARGET,
        "closedAcceptedIds": CLOSED, "checks": checks}
    REPORT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    receipt = {"id": "RANK9-PLANARGATES5-PACKET243-RECEIPT", "status": report["status"],
        "auditReport": REPORT.name, "auditReportSHA256": sha(REPORT.read_bytes()),
        "archive": report["archive"], "delivery": report["delivery"], "authority": AUTH,
        "pendingIds": TARGET, "closedAcceptedIds": CLOSED,
        "checksPassed": report["checksPassed"], "checksFailed": report["checksFailed"]}
    RECEIPT.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": report["status"], "checksPassed": report["checksPassed"],
        "checksFailed": report["checksFailed"], "failures": failures}, indent=2))
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
