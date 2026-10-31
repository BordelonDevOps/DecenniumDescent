from __future__ import annotations

import hashlib
import json
import zipfile
import zlib
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[5]
AUDIT = ROOT / "docs/audit/2026-10-08/full-game/director-spell-review-129"
OUT = AUDIT / "rank9_planargates5_current_source_226_prepared"
ARCHIVE = OUT / "DD_Rank9_PlanarGates5_CurrentSource_226.zip"
DELIVERY = OUT / "DD_Rank9_PlanarGates5_CurrentSource_226_DELIVERY.json"
CANDIDATE = OUT / "CURRENT_SOURCE_CONFERENCE_CANDIDATE_226.json"
CONTEXT = OUT / "CURRENT_CONTEXT_226.json"
REQUEST = OUT / "REQUEST_226.txt"
QUEUE = AUDIT / "CURRENT_SPELL_QUEUE_226.json"
HANDOFF = AUDIT / "CURRENT_HANDOFF_226.json"
PENDING = AUDIT / "CURRENT37_PENDING_IDENTITY_AUDIT_225.json"
RETURN225 = AUDIT / "rank9_knowledgerevelation5_return225_received/DD_Rank9_KnowledgeRevelation1_Director_Return225.zip"
RETURN200 = AUDIT / "rank9_planargates5_return200_received/DD_Rank9_PlanarGates5_Director_Return200.zip"
REPORT = AUDIT / "RANK9PLANARGATES5_PACKET_226_INDEPENDENT_AUDIT.json"
RECEIPT = AUDIT / "RANK9PLANARGATES5_PACKET_226_RECEIPT.json"
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


def binding(zf: zipfile.ZipFile, name: str) -> dict:
    h = hashlib.sha256(); c = 0; n = 0
    with zf.open(name) as f:
        for b in iter(lambda: f.read(1024 * 1024), b""):
            h.update(b); c = zlib.crc32(b, c); n += len(b)
    return {"bytes": n, "sha256": h.hexdigest(), "crc32": f"{c & 0xffffffff:08x}"}


def main() -> None:
    d = json.loads(DELIVERY.read_text(encoding="utf-8-sig"))
    candidate = json.loads(CANDIDATE.read_text(encoding="utf-8-sig"))
    context = json.loads(CONTEXT.read_text(encoding="utf-8-sig"))
    queue = json.loads(QUEUE.read_text(encoding="utf-8-sig"))
    handoff = json.loads(HANDOFF.read_text(encoding="utf-8-sig"))
    pending = json.loads(PENDING.read_text(encoding="utf-8-sig"))
    checks: list[dict] = []

    def check(name: str, passed: bool, detail=None) -> None:
        checks.append({"check": name, "passed": bool(passed), "detail": detail})

    archive_raw = ARCHIVE.read_bytes()
    outer = {"bytes": len(archive_raw), "sha256": sha(archive_raw), "crc32": crc(archive_raw)}
    check("Current packet archive matches delivery byte/SHA/CRC binding",
          all(outer[k] == d["archive"][k] for k in ("bytes", "sha256", "crc32")), outer)
    check("Exact review scope and authority are bound in delivery, context, candidate, queue, and handoff",
          d["group"] == "rank9-planar-gates5" and d["pendingIds"] == TARGET and d["sourceAuthority"] == AUTH
          and context["sourceAuthority"] == AUTH and candidate["currentAuthority"] == AUTH
          and candidate["currentPendingGroup"] == {"group": "rank9-planar-gates5", "spellIds": TARGET, "count": 2}
          and queue["currentAuthority"] == AUTH and queue["nextGroup"] == "rank9-planar-gates5"
          and handoff["currentAuthority"] == AUTH and handoff["nextGroup"] == "rank9-planar-gates5",
          {"target": d["pendingIds"], "authority": d["sourceAuthority"]})
    check("Return200 accepted/applied planar identities are closed and only two identities remain in scope",
          d["closedAcceptedIds"] == CLOSED and [x["spellId"] for x in candidate["records"]] == TARGET
          and candidate["closedAcceptedSpellIds"] == CLOSED
          and context["priorPlanarGateReturn200"]["acceptedIds"] == CLOSED
          and context["priorPlanarGateReturn200"]["appliedIds"] == CLOSED,
          {"closed": d["closedAcceptedIds"], "records": [x["spellId"] for x in candidate["records"]]})
    check("Current pending audit has 37 rows and includes only the selected pending Planar targets",
          pending["pendingCount"] == 37 and all(x in pending["pendingIds"] for x in TARGET)
          and all(next(e for e in json.loads((ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json").read_text(encoding="utf-8-sig"))["entries"] if e["id"] == x)["authoredStatus"] == "pending-authored-procedure" for x in TARGET),
          {"pendingCount": pending["pendingCount"], "targets": TARGET})
    check("Return225 is independently audited, held only outside scope, and names this exact next group",
          context["latestCurrentReturn"]["return"] == 225
          and context["latestCurrentReturn"]["heldIds"] == ["faction-omniscience-supreme"]
          and context["latestCurrentReturn"]["blockerIds"] == ["KR198-B01"]
          and context["latestCurrentReturn"]["independentAudit"]["path"].endswith("RANK9_KNOWLEDGEREVELATION5_RETURN225_INDEPENDENT_AUDIT.json"),
          context["latestCurrentReturn"])
    check("Candidate preserves the full 30-question and nine-future-obligation context while scoping only two pending records",
          len(candidate["questions"]) == 30 and len(candidate["futureCaseRequirements"]) == 9
          and {x["spellId"] for x in candidate["records"]} == set(TARGET),
          {"questions": len(candidate["questions"]), "futureRequirements": len(candidate["futureCaseRequirements"])})

    with zipfile.ZipFile(ARCHIVE) as z:
        names = z.namelist()
        check("ZIP CRCs, unique safe paths, and internal member manifest pass",
              z.testzip() is None and len(names) == len(set(names)) and all(safe(n) for n in names)
              and "MANIFEST.json" in names,
              {"memberCount": len(names), "unsafe": [n for n in names if not safe(n)]})
        manifest = json.loads(z.read("MANIFEST.json")); rows = {r["path"]: r for r in manifest["members"]}
        manifest_ok = set(names) - {"MANIFEST.json"} == set(rows) and manifest["memberCountExcludingSelf"] == len(rows)
        failures = []
        if manifest_ok:
            for name, row in rows.items():
                if binding(z, name) != {k: row[k] for k in ("bytes", "sha256", "crc32")}:
                    failures.append(name)
        check("Every archive member matches internal path/count/byte/SHA/CRC manifest", manifest_ok and not failures,
              {"members": len(rows), "failures": failures[:10]})
        check("Packet root candidate, context, and request are byte-identical to prepared local files",
              z.read("CURRENT_SOURCE_CONFERENCE_CANDIDATE_226.json") == CANDIDATE.read_bytes()
              and z.read("CURRENT_CONTEXT_226.json") == CONTEXT.read_bytes()
              and z.read("REQUEST_226.txt") == REQUEST.read_bytes(), None)
        source_failures = []
        for row in candidate["sourceBindings"]:
            name = "sources_current/" + row["path"]
            if name not in names:
                source_failures.append({"path": row["path"], "reason": "missing member"}); continue
            raw = z.read(name)
            if len(raw) != row["bytes"] or sha(raw) != row["sha256"] or blobsha(raw) != row["gitBlobSHA1"]:
                source_failures.append({"path": row["path"], "reason": "binding mismatch"})
        check("All current source rows match embedded bytes, SHA-256, and Git blob IDs",
              len(candidate["sourceBindings"]) >= 132 and not source_failures,
              {"rows": len(candidate["sourceBindings"]), "failures": source_failures[:10]})
        check("Return225 and Return200 audit artifacts are embedded and their dispositions agree",
              json.loads(z.read("evidence/RETURN225_INDEPENDENT_AUDIT.json"))["status"] == "PASS"
              and json.loads(z.read("evidence/PLANARGATES5_RETURN200_INDEPENDENT_AUDIT.json"))["status"] == "PASS"
              and json.loads(z.read("evidence/PLANARGATES5_RETURN200_APPLICATION.json"))["acceptedIds"] == CLOSED,
              {"return225Audit": "PASS", "return200Audit": "PASS", "closedApplied": CLOSED})
        check("New handoff and queue snapshots inside packet match current authority, target, and local bytes",
              z.read("current/" + QUEUE.relative_to(ROOT).as_posix()) == QUEUE.read_bytes()
              and z.read("current/" + HANDOFF.relative_to(ROOT).as_posix()) == HANDOFF.read_bytes()
              and z.read("current/" + PENDING.relative_to(ROOT).as_posix()) == PENDING.read_bytes(), None)
        exact_index = json.loads(z.read("current/DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json"))
        index_entries = {x["id"]: x for x in exact_index["entries"]}
        check("Embedded index marks targets pending and previous three Planar Gate spells closed",
              all(index_entries[x]["authoredStatus"] == "pending-authored-procedure" for x in TARGET)
              and all(index_entries[x]["authoredStatus"] == "reviewed-authored-operational-playtest" for x in CLOSED),
              {x: index_entries[x]["authoredStatus"] for x in TARGET + CLOSED})
        current_rows = candidate["sourceBindings"]
        check("Current queue/handoff include only two next identities and retain Return225 hold", queue["next"]["pendingIds"] == TARGET
              and queue["next"]["pendingCount"] == 2 and handoff["nextStep"]["pendingIds"] == TARGET
              and handoff["latestBatch"]["heldIds"] == ["faction-omniscience-supreme"]
              and len(current_rows) >= 132, {"next": queue["next"], "sourceRows": len(current_rows)})

    failures = [x for x in checks if not x["passed"]]
    report = {"id": "RANK9-PLANARGATES5-PACKET226-INDEPENDENT-AUDIT",
        "status": "PASS" if not failures else "FAIL", "checksPassed": len(checks) - len(failures),
        "checksFailed": len(failures), "archive": {"path": ARCHIVE.relative_to(ROOT).as_posix(), **outer},
        "delivery": {"path": DELIVERY.relative_to(ROOT).as_posix(), "bytes": DELIVERY.stat().st_size,
            "sha256": sha(DELIVERY.read_bytes())}, "authority": AUTH, "pendingIds": TARGET,
        "closedAcceptedIds": CLOSED, "checks": checks}
    REPORT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    receipt = {"id": "RANK9-PLANARGATES5-PACKET226-RECEIPT", "status": report["status"],
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
