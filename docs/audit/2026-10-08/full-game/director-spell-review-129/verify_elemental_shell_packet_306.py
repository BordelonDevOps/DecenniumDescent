from __future__ import annotations

import datetime as dt
import hashlib
import json
import pathlib
import zlib
import zipfile
from pathlib import PurePosixPath

ROOT = pathlib.Path.cwd()
A = ROOT / "docs/audit/2026-10-08/full-game/director-spell-review-129"
PACKET = A / "rank9_defenseform8_current_source_306_prepared/DD_Rank9_DefenseForm8_CurrentSource_306.zip"
DELIVERY = A / "rank9_defenseform8_current_source_306_prepared/DD_Rank9_DefenseForm8_CurrentSource_306_DELIVERY.json"
PREP = A / "RANK9_DEFENSEFORM8_SOURCE_PREPARATION_306.json"
PRIOR_PACKET = A / "rank9_defenseform8_source_packet_218_refreshed/DD_Rank9_DefenseForm8_CurrentSource_218.zip"
PRIOR_RETURN = A / "rank9_defenseform8_return218_received/DD_Rank9_DefenseForm5_Director_Return218.zip"
PRIOR_DELIVERY = A / "rank9_defenseform8_return218_received/DD_Rank9_DefenseForm5_Director_Return218_DELIVERY.json"
AUTHORITY = {"reviewedApplied": 822, "pending": 26, "acceptedUnapplied": 0,
             "completeStandaloneProcedures": 546, "scopedInterfaces": 173}

def digest(b: bytes) -> tuple[int, str, str]:
    return len(b), hashlib.sha256(b).hexdigest(), f"{zlib.crc32(b) & 0xffffffff:08x}"

def check(name: str, ok: bool, detail=None):
    CHECKS.append({"check": name, "passed": bool(ok), "detail": detail})

def main():
    global CHECKS
    CHECKS = []
    delivery = json.loads(DELIVERY.read_text(encoding="utf-8-sig"))
    packet_bytes = PACKET.read_bytes()
    outer = delivery["archive"]
    check("outer archive bytes, SHA-256, CRC32 match delivery", digest(packet_bytes) == (outer["bytes"], outer["sha256"], outer["crc32"]))
    assert digest(packet_bytes) == (outer["bytes"], outer["sha256"], outer["crc32"])

    with zipfile.ZipFile(PACKET) as z:
        assert z.testzip() is None
        names = z.namelist()
        name_set = set(names)
        unsafe = [n for n in names if not n or "\\" in n or PurePosixPath(n).is_absolute() or any(x in ("", ".", "..") for x in PurePosixPath(n).parts)]
        check("ZIP integrity and unique safe member paths", len(names) == len(name_set) and not unsafe, {"members": len(names), "unsafe": unsafe})
        check("outer exact allowlist covers every archive member", set(delivery["exactAllowlist"]) == name_set and delivery["memberCount"] == len(names), {"archive": len(names), "allowlist": len(delivery["exactAllowlist"])})
        external = {r["path"]: r for r in delivery["members"]}
        external_errors = []
        for name in names:
            actual = digest(z.read(name))
            row = external.get(name)
            if row is None or actual != (row["bytes"], row["sha256"], row["crc32"]):
                external_errors.append(name)
        check("every ZIP member matches the outer delivery binding", not external_errors, external_errors[:10])

        manifest = json.loads(z.read("MEMBER_MANIFEST.json"))
        internal = {r["path"]: r for r in manifest["members"]}
        payload_names = name_set - {"MEMBER_MANIFEST.json"}
        internal_errors = []
        for name in payload_names:
            row = internal.get(name)
            if row is None or digest(z.read(name)) != (row["bytes"], row["sha256"], row["crc32"]):
                internal_errors.append(name)
        check("internal manifest covers and verifies every payload member", not internal_errors and set(internal) == payload_names and manifest["memberCountExcludingSelf"] == len(payload_names), {"payload": len(payload_names), "errors": internal_errors[:10]})

        candidate = json.loads(z.read("current/CURRENT_SOURCE_CONFERENCE_CANDIDATE_306.json"))
        source_bindings = candidate["sourceBindings"]
        source_errors = []
        for row in source_bindings:
            member = "sources_current/" + row["path"]
            worktree = ROOT / PurePosixPath(row["path"])
            if member not in name_set or digest(z.read(member)) != (row["bytes"], row["sha256"], row["crc32"]) or not worktree.exists() or digest(worktree.read_bytes()) != (row["bytes"], row["sha256"], row["crc32"]):
                source_errors.append(row["path"])
        check("87 refreshed source bindings match archive and current worktree", len(source_bindings) == 87 and not source_errors, {"count": len(source_bindings), "errors": source_errors[:10]})

        with zipfile.ZipFile(PRIOR_PACKET) as old_source:
            old_candidate = json.loads(old_source.read("CURRENT_SOURCE_CONFERENCE_CANDIDATE_218.json"))
            old_rows = {r["path"]: r for r in old_candidate["sourceBindings"]}
            changes = []
            for row in source_bindings:
                old_member = "sources_current/" + row["path"]
                if old_member not in old_source.namelist() or z.read("sources_current/" + row["path"]) != old_source.read(old_member):
                    changes.append(row["path"])
        check("refresh difference is explicitly disclosed and exactly one source", len(changes) == 1 and candidate["sourceBindingRefresh"]["changedFromReturn218Packet"] and len(candidate["sourceBindingRefresh"]["changedFromReturn218Packet"]) == 1, {"changedPaths": changes, "oldBindings": len(old_rows)})

        index = json.loads(z.read("current/DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json"))
        catalog = json.loads(z.read("current/DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json"))
        q = json.loads(z.read("current/CURRENT_SPELL_QUEUE_304.json"))
        h = json.loads(z.read("current/CURRENT_HANDOFF_305.json"))
        p = json.loads(z.read("current/CURRENT26_PENDING_IDENTITY_AUDIT_304.json"))
        decision = json.loads(z.read("current/FINAL_WORD_DIRECTOR_DECISION_303.json"))
        entry = next(r for r in index["entries"] if r["id"] == "elemental-shell")
        spell = next(r for r in catalog["spells"] if r["id"] == "elemental-shell")
        check("current authority and target pending/non-operational state are exact", delivery["authority"] == AUTHORITY and index["authoredCounts"] == {"reviewed": 822, "pending": 26} and entry["authoredStatus"] == "pending-authored-procedure" and spell.get("operational") is None, {"authority": delivery["authority"], "entry": entry["authoredStatus"], "operational": spell.get("operational")})
        check("packet adjudication target is Elemental Shell only", delivery["targetIds"] == ["elemental-shell"] and manifest["targetPendingIds"] == ["elemental-shell"] and candidate["currentReviewTargets"][0]["spellId"] == "elemental-shell", delivery["targetIds"])
        check("handoff pointer correction and queue/pending binding pass; Final Word remains held", h["currentAuthority"] == q["currentAuthority"] == p["authority"] == AUTHORITY and h["nextPendingGroup"] == h["currentPreparation"] and h["nextPendingGroup"]["group"] == "rank9-defense-form8" and h["historicalNextPendingGroupPointer304"]["directorReturn"] == 289 and decision["heldIds"] == ["final-word"] and decision["blockerIds"] == ["DR217-B01"], {"next": h["nextPendingGroup"]["group"], "held": decision["heldIds"]})

        with zipfile.ZipFile(PRIOR_RETURN) as old_return:
            old_delivery = json.loads(PRIOR_DELIVERY.read_text(encoding="utf-8-sig"))
            old_external = {r["path"]: r for r in old_delivery["members"]}
            old_internal = json.loads(old_return.read("MEMBER_MANIFEST.json"))
            old_internal_map = {r["path"]: r for r in old_internal["members"]}
            case_index = json.loads(old_return.read("CASE_INDEX.json"))
            shell_cases = [r for r in case_index["cases"] if r.get("spellId") == "elemental-shell"]
            case_errors = []
            for row in shell_cases:
                name = row["path"]
                data = old_return.read(name)
                expected = digest(data)
                if digest(z.read("history/Return218/" + name)) != expected:
                    case_errors.append(name)
                for bindings in (old_external, old_internal_map):
                    b = bindings.get(name)
                    if b is None or expected != (b["bytes"], b["sha256"], b["crc32"]):
                        case_errors.append(name + "#original-binding")
        check("all 21 prior Elemental Shell case records are preserved byte-exact", len(shell_cases) == 21 and not case_errors, {"caseCount": len(shell_cases), "errors": case_errors[:10]})
        case_ids = {row.get("caseId") or row.get("id") for row in shell_cases}
        check("packet retains both required completed CH07 Null case records", {"DF218-SHELL-NULL-POSITIVE-HP", "DF218-SHELL-NULL-STABLE-ZERO"}.issubset(case_ids), sorted(x for x in case_ids if x))
        request = z.read("current/REQUEST_306.txt").decode("utf-8")
        check("request scopes the two Elemental Shell blockers and forbids inferred/synthetic witnesses", "ELEMENTAL SHELL ONLY" in request.upper() and "DF218-B01" in request and "DF218-B02" in request and "Do not synthesize" in request and "Time Stop" not in request, {"requestBytes": len(request)})
        check("packet makes no canonical changes or runtime/application claims", delivery["canonicalChanges"] is False and delivery["githubChanges"] is False and delivery["runtimeExecuted"] is False and delivery["sourceProgramsExecuted"] is False, {k: delivery[k] for k in ("canonicalChanges", "githubChanges", "runtimeExecuted", "sourceProgramsExecuted")})

    prep = json.loads(PREP.read_text(encoding="utf-8-sig"))
    check("source-preparation record matches target, source count, case count, and authority", prep["sourceAuthority"] == AUTHORITY and prep["pendingIds"] == ["elemental-shell"] and prep["currentSourceFileCount"] == 87 and prep["targetCaseCountFromReturn218"] == 21 and prep["canonicalChanges"] is False and prep["githubChanges"] is False, {"pendingIds": prep["pendingIds"], "sources": prep["currentSourceFileCount"], "cases": prep["targetCaseCountFromReturn218"]})

    failed = [r for r in CHECKS if not r["passed"]]
    report = {"id": "ELEMENTAL-SHELL-PACKET-306-INDEPENDENT-AUDIT", "recordedAtUtc": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
              "status": "PASS" if not failed else "FAIL", "archive": {"path": PACKET.relative_to(ROOT).as_posix(), "bytes": len(packet_bytes), "sha256": hashlib.sha256(packet_bytes).hexdigest(), "crc32": f"{zlib.crc32(packet_bytes) & 0xffffffff:08x}"},
              "delivery": {"path": DELIVERY.relative_to(ROOT).as_posix(), **dict(zip(("bytes", "sha256", "crc32"), digest(DELIVERY.read_bytes())))},
              "authority": AUTHORITY, "targetIds": ["elemental-shell"], "checkCount": len(CHECKS), "passedChecks": len(CHECKS)-len(failed), "failedChecks": len(failed), "checks": CHECKS,
              "acceptedIds": [], "appliedIds": [], "canonicalChanges": False, "runtimeExecuted": False}
    out = A / "ELEMENTAL_SHELL_PACKET_306_INDEPENDENT_AUDIT.json"
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"status": report["status"], "checkCount": report["checkCount"], "passedChecks": report["passedChecks"], "failedChecks": report["failedChecks"], "audit": out.relative_to(ROOT).as_posix(), "archiveSha256": report["archive"]["sha256"], "failed": failed}, ensure_ascii=False, indent=2))
    assert not failed, failed

if __name__ == "__main__":
    main()
