from __future__ import annotations

import datetime as dt
import hashlib
import json
import pathlib
import subprocess
import zipfile
import zlib


ROOT = pathlib.Path(__file__).resolve().parents[5]
A = ROOT / "docs/audit/2026-10-08/full-game/director-spell-review-129"
INDEX = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json"
CATALOG = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json"
BASE = "351fe708ab21d1d63e5301f16336adf3712bfbf0"
ID = "nullification-wave"
NEXT = "summon-herald-of-the-planes"
BLOCKER = "WC188-B01"
RESIDUALS = ["NW355-R1", "NW355-R2", "NW355-R3", "NW355-R4"]
ARCHIVE = A / "rank9_nullification_wave_closure355_repack01_delivery/DD_Rank9_NullificationWave_WC188B01_Closure355_Repack01.zip"
RETURN281 = A / "rank9_wardcontrol6_return281_received/DD_Rank9_WardControl6_Director_Return281_HELD.zip"
VALIDATION = A / "NULLIFICATION_WAVE_CLOSURE355_REPACK01_APPLICATION_VALIDATION.json"
SNAPSHOT = A / "CURRENT_SPELL_REVIEW_SNAPSHOT_357.md"


def raw(path: pathlib.Path) -> bytes:
    return path.read_bytes()


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def bind(path: pathlib.Path, data: bytes | None = None) -> dict:
    b = raw(path) if data is None else data
    return {"path": path.relative_to(ROOT).as_posix(), "bytes": len(b), "sha256": sha(b),
            "crc32": f"{zlib.crc32(b) & 0xffffffff:08x}"}


def load(path: pathlib.Path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def main() -> None:
    assert not VALIDATION.exists() and not SNAPSHOT.exists(), "Refusing to overwrite final readback outputs."
    index = load(INDEX)
    before = load(A / "authored_review_index.before_nullification_wave_357.json")
    catalog_raw = raw(CATALOG)
    catalog_git = subprocess.check_output(
        ["git", "show", f"{BASE}:{CATALOG.relative_to(ROOT).as_posix()}"], cwd=ROOT
    )
    application = load(A / "NULLIFICATION_WAVE_CLOSURE355_REPACK01_APPLICATION.json")
    decision = load(A / "NULLIFICATION_WAVE_CLOSURE355_REPACK01_DIRECTOR_DECISION.json")
    acceptance = load(A / "NULLIFICATION_WAVE_CLOSURE355_REPACK01_ACCEPTANCE.json")
    receipt = load(A / "NULLIFICATION_WAVE_CLOSURE355_REPACK01_RECEIPT.json")
    operations = load(A / "NULLIFICATION_WAVE_CLOSURE355_REPACK01_INDEX_OPERATIONS.json")
    audit = load(A / "NULLIFICATION_WAVE_CLOSURE355_REPACK01_INDEPENDENT_AUDIT.json")
    queue = load(A / "CURRENT_SPELL_QUEUE_357.json")
    pending = load(A / "CURRENT21_PENDING_IDENTITY_AUDIT_357.json")
    handoff = load(A / "CURRENT_HANDOFF_357.json")
    pkg = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_candidates/rank9nullificationwave_reviewed_357"
    manifest = load(pkg / "CANDIDATE_PACKAGE_MANIFEST.json")
    model = load(pkg / "MODEL.json")
    package_members = manifest["members"]
    evidence_bindings = load(pkg / "EVIDENCE_BINDINGS.json")
    source_proc = evidence_bindings["sourceProcedure"]
    with zipfile.ZipFile(RETURN281) as zf:
        source_proc_raw = zf.read(source_proc["member"])
    with zipfile.ZipFile(ARCHIVE) as zf:
        assert zf.testzip() is None
        closure_manifest = json.loads(zf.read("MEMBER_MANIFEST.json"))
        closure_members = closure_manifest["members"]
        member_checks = [
            len(zf.read(row["path"])) == row["bytes"] and sha(zf.read(row["path"])) == row["sha256"]
            and f"{zlib.crc32(zf.read(row['path'])) & 0xffffffff:08x}" == row["crc32"]
            for row in closure_members
        ]

    entry_before = next(row for row in before["entries"] if row["id"] == ID)
    entry_after = next(row for row in index["entries"] if row["id"] == ID)
    other_ids = [row["id"] for row in before["entries"]
                 if row.get("authoredStatus") == "pending-authored-procedure" and row["id"] != ID]
    pending_ids = pending["pendingIds"]
    current_index_ref = bind(INDEX)
    queue_ref = bind(A / "CURRENT_SPELL_QUEUE_357.json")
    pending_ref = bind(A / "CURRENT21_PENDING_IDENTITY_AUDIT_357.json")
    app_ref = bind(A / "NULLIFICATION_WAVE_CLOSURE355_REPACK01_APPLICATION.json")
    checks = [
        ("Director sealed acceptance authorizes only nullification-wave", decision["acceptedIds"] == [ID] and decision["appliedIds"] == [] and decision["applicationAuthorized"] is True and decision["remainingDefectPaths"] == []),
        ("all four residuals closed with no active blocker", decision["closedBlockerIds"] == [BLOCKER] and decision["closedResidualIds"] == RESIDUALS and decision["blockerIds"] == [] and decision["heldIds"] == []),
        ("accepted archive binding matches all manifested members", application["archive"]["sha256"] == sha(raw(ARCHIVE)) and len(member_checks) == 26 and all(member_checks)),
        ("independent semantic audit passes 19 of 19", audit["status"] == "PASS" and audit["checkCount"] == 19 and audit["failedChecks"] == 0),
        ("authored index has 827 reviewed, 21 pending and 551 standalone procedures", index["authoredCounts"] == {"reviewed": 827, "pending": 21} and index["representationCounts"]["completeReviewedStandaloneProcedures"] == 551),
        ("only the accepted identity changes among pending index entries", entry_before["authoredStatus"] == "pending-authored-procedure" and entry_after["authoredStatus"] == "reviewed-authored-operational-playtest" and all(next(r for r in index["entries"] if r["id"] == x) == next(r for r in before["entries"] if r["id"] == x) for x in other_ids) and set(pending_ids) == set(other_ids) and len(pending_ids) == 21),
        ("catalog working copy remains byte-exact and normalizes to committed catalog", len(catalog_raw) == application["catalogWorkingCopyBinding"]["bytes"] and sha(catalog_raw) == application["catalogWorkingCopyBinding"]["sha256"] and catalog_raw.replace(b"\r\n", b"\n") == catalog_git),
        ("source procedure remains bound and unchanged", len(source_proc_raw) == source_proc["bytes"] and sha(source_proc_raw) == source_proc["sha256"] and application["sourceProcedureChanged"] is False),
        ("candidate-package members match manifest hashes", len(package_members) == 5 and all(len(raw(ROOT / r["path"])) == r["bytes"] and sha(raw(ROOT / r["path"])) == r["sha256"] for r in package_members)),
        ("queue, pending audit and handoff cross-bind the applied index", queue["currentIndexBinding"]["sha256"] == pending["indexBinding"]["sha256"] == current_index_ref["sha256"] and pending["currentQueueBinding"]["sha256"] == queue_ref["sha256"] and handoff["queueBinding"]["sha256"] == queue_ref["sha256"] and handoff["pendingIdentityAuditBinding"]["sha256"] == pending_ref["sha256"]),
        ("next priority is Herald W01 and Lumen fixture remains conditional", queue["nextIdentity"] == NEXT and queue["nextBlockerIds"] == ["SH202-B02"] and "conditional on W01 approval" in pending["nextStep"]),
        ("runtime and downstream execution remain disabled", application["runtimeSelectionEnabled"] is False and application["runtimeExecuted"] is False and model["implementationApproved"] is False and model["releaseApproved"] is False),
        ("index operations preserve exact rollback image", sha(raw(A / "authored_review_index.before_nullification_wave_357.json")) == operations["backup"]["sha256"] == application["indexBindingBefore"]["sha256"] and operations["inverseRestoresExactIndex"] is True and operations["afterBinding"]["sha256"] == current_index_ref["sha256"]),
        ("acceptance, application and receipt agree on identity and authority", acceptance["acceptedIds"] == receipt["acceptedIds"] == application["acceptedIds"] == [ID] and receipt["applicationAuthorizedIds"] == [ID] and application["appliedIds"] == [ID]),
    ]
    assert all(passed for _, passed in checks), [name for name, passed in checks if not passed]
    stamp = dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")
    validation = {
        "id": "NULLIFICATION-WAVE-CLOSURE355-REPACK01-APPLICATION-VALIDATION-357",
        "recordedAtUtc": stamp, "status": "PASS",
        "checks": [{"check": name, "passed": bool(passed)} for name, passed in checks],
        "checkCount": len(checks), "passedChecks": len(checks), "failedChecks": 0,
        "acceptedIds": [ID], "appliedIds": [ID], "closedBlockerIds": [BLOCKER], "closedResidualIds": RESIDUALS,
        "authority": pending["authority"], "index": current_index_ref, "application": app_ref,
        "decision": bind(A / "NULLIFICATION_WAVE_CLOSURE355_REPACK01_DIRECTOR_DECISION.json"),
        "acceptance": bind(A / "NULLIFICATION_WAVE_CLOSURE355_REPACK01_ACCEPTANCE.json"),
        "receipt": bind(A / "NULLIFICATION_WAVE_CLOSURE355_REPACK01_RECEIPT.json"),
        "archive": bind(ARCHIVE), "audit": bind(A / "NULLIFICATION_WAVE_CLOSURE355_REPACK01_INDEPENDENT_AUDIT.json"),
        "queue": queue_ref, "pendingIdentityAudit": pending_ref,
        "handoff": bind(A / "CURRENT_HANDOFF_357.json"),
        "indexOperations": bind(A / "NULLIFICATION_WAVE_CLOSURE355_REPACK01_INDEX_OPERATIONS.json"),
        "nativeCatalogChanged": False, "sourceProcedureChanged": False,
        "runtimeSelectionEnabled": False, "nextIdentity": NEXT,
    }
    VALIDATION.write_text(json.dumps(validation, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    validation_ref = bind(VALIDATION)
    SNAPSHOT.write_text(
        "# Spell review snapshot — Nullification Wave Closure355 Repack01 application\n\n"
        "**827 applied / 21 pending / 0 accepted-unapplied; 551 complete standalone procedures / 173 scoped interfaces; 0 first reviews / 21 closure tasks.**\n\n"
        "GPT sealed-accepted and authorized Nullification Wave / WC188-B01 only. NW355-R1–R4 are closed. The source procedure and native catalog remain unchanged; runtime selection remains disabled.\n\n"
        "The next directed priority is Summon Herald of the Planes / SH202-B02. Prepare the W01 content reconciliation first. The user's TEST_ONLY W02 authorization remains conditional on W01 approval.\n\n"
        f"Application validation: {validation_ref['path']} (SHA-256 {validation_ref['sha256']}).\n",
        encoding="utf-8", newline="\n",
    )
    print(json.dumps({"status": "PASS", "checkCount": len(checks), "acceptedApplied": ID,
                      "authority": pending["authority"], "validation": validation_ref,
                      "nextIdentity": NEXT}, indent=2))


if __name__ == "__main__":
    main()
