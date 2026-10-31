from __future__ import annotations

import hashlib
import json
import pathlib
import re
import zipfile
import zlib
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[5]
BASE = ROOT / "docs/audit/2026-10-08/full-game/director-spell-review-129"
OUT = BASE / "rank9_defenseform8_current_source_236_prepared"
ARCHIVE = OUT / "DD_Rank9_DefenseForm8_CurrentSource_236.zip"
DELIVERY = OUT / "DD_Rank9_DefenseForm8_CurrentSource_236_DELIVERY.json"
REPORT = BASE / "RANK9_DEFENSEFORM8_PACKET236_INDEPENDENT_AUDIT.json"
RECEIPT = BASE / "RANK9_DEFENSEFORM8_PACKET236_RECEIPT.json"
AUTHORITY = {"reviewedApplied": 811, "pending": 37, "acceptedUnapplied": 0, "completeStandaloneProcedures": 535, "scopedInterfaces": 173}
TARGETS = ["elemental-shell", "timeless-form", "invulnerable-sphere"]
checks: list[dict] = []


def digest(raw: bytes) -> dict:
    return {"bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest(), "crc32": f"{zlib.crc32(raw) & 0xffffffff:08x}"}


def read_json(raw: bytes):
    return json.loads(raw.decode("utf-8-sig"))


def matches(raw: bytes, expected: dict) -> bool:
    got = digest(raw)
    return isinstance(expected, dict) and all(got.get(key) == expected.get(key) for key in ("bytes", "sha256", "crc32"))


def safe(name: str) -> bool:
    path = PurePosixPath(name)
    return bool(name) and "\\" not in name and not path.is_absolute() and not re.match(r"^[A-Za-z]:", name) and all(part not in ("", ".", "..") for part in path.parts)


def check(name: str, passed: bool, detail=None) -> None:
    checks.append({"check": name, "passed": bool(passed), "detail": detail})


delivery = json.loads(DELIVERY.read_text(encoding="utf-8-sig"))
archive_raw = ARCHIVE.read_bytes()
delivery_raw = DELIVERY.read_bytes()
archive_digest = digest(archive_raw)
delivery_digest = digest(delivery_raw)
check("outer archive and external delivery identify Packet236 and exact archive bytes", delivery.get("id") == "RANK9-DEFENSEFORM8-CURRENT-SOURCE-236-DELIVERY" and delivery.get("archive", {}).get("fileName") == ARCHIVE.name and matches(archive_raw, delivery.get("archive", {})), {"actual": archive_digest, "expected": delivery.get("archive")})
check("delivery authority and target scope are exactly current 811/37/0 and the three pending Defense/Form8 identities", delivery.get("authority") == AUTHORITY and delivery.get("targetIds") == TARGETS and delivery.get("group") == "rank9-defense-form8" and delivery.get("canonicalChanges") is False and delivery.get("githubChanges") is False and delivery.get("sourceProgramsExecuted") is False and delivery.get("runtimeExecuted") is False, {"authority": delivery.get("authority"), "targetIds": delivery.get("targetIds"), "group": delivery.get("group")})

q = json.loads((BASE / "CURRENT_SPELL_QUEUE_236.json").read_text(encoding="utf-8-sig"))
h = json.loads((BASE / "CURRENT_HANDOFF_236.json").read_text(encoding="utf-8-sig"))
p = json.loads((BASE / "CURRENT37_PENDING_IDENTITY_AUDIT_236.json").read_text(encoding="utf-8-sig"))
index = json.loads((ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json").read_text(encoding="utf-8-sig"))
catalog = json.loads((ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json").read_text(encoding="utf-8-sig"))
entries = {row["id"]: row for row in index["entries"]}
spells = {row["id"]: row for row in catalog["spells"]}
check("current queue/handoff/pending snapshots and native index agree on unchanged authority", q.get("currentAuthority") == h.get("currentAuthority") == p.get("authority") == AUTHORITY and p.get("pendingCount") == 37 and index.get("authoredCounts") == {"reviewed": 811, "pending": 37}, {"queue": q.get("currentAuthority"), "handoff": h.get("currentAuthority"), "pendingCount": p.get("pendingCount"), "index": index.get("authoredCounts")})
check("all requested targets remain pending/non-operational and prior Return218 acceptances are applied", all(entries.get(s, {}).get("authoredStatus") == "pending-authored-procedure" and spells.get(s, {}).get("operational") is None for s in TARGETS) and all(entries.get(s, {}).get("authoredStatus") == "reviewed-authored-operational-playtest" for s in ("absolute-immunity", "body-to-void")), {s: {"index": entries.get(s, {}).get("authoredStatus"), "operational": spells.get(s, {}).get("operational") is not None} for s in TARGETS + ["absolute-immunity", "body-to-void"]})

with zipfile.ZipFile(ARCHIVE) as z:
    names = z.namelist()
    name_set = set(names)
    check("ZIP integrity passes and member paths are unique, safe ordinary files", z.testzip() is None and len(names) == len(name_set) and all(safe(name) for name in names) and all(not info.is_dir() for info in z.infolist()), {"members": len(names), "unique": len(name_set), "unsafe": [name for name in names if not safe(name)][:10]})
    external_allowlist = delivery.get("exactAllowlist", [])
    external_members = {row.get("path"): row for row in delivery.get("members", []) if isinstance(row, dict)}
    check("external allowlist and member inventory exactly cover the archive", set(external_allowlist) == name_set and len(external_allowlist) == len(names) and set(external_members) == name_set and len(external_members) == len(names) == delivery.get("memberCount"), {"archive": len(names), "allowlist": len(external_allowlist), "memberRecords": len(external_members), "memberCount": delivery.get("memberCount")})
    external_errors = [name for name in names if name not in external_members or not matches(z.read(name), external_members[name])]
    check("every archive member matches external bytes/SHA/CRC", not external_errors, external_errors[:12])
    manifest_raw = z.read("MEMBER_MANIFEST.json")
    manifest = read_json(manifest_raw)
    internal_map = {row["path"]: row for row in manifest.get("members", [])}
    check("embedded manifest covers every payload member exactly and is self-excluding", set(internal_map) == name_set - {"MEMBER_MANIFEST.json"} and len(internal_map) == delivery.get("payloadCount") and matches(manifest_raw, delivery.get("memberManifest", {})), {"payload": len(internal_map), "payloadCount": delivery.get("payloadCount")})
    internal_errors = [name for name, row in internal_map.items() if not matches(z.read(name), row)]
    check("every payload member matches the internal manifest", not internal_errors, internal_errors[:12])

    source_rows = delivery.get("sourceBindings", [])
    source_errors = []
    for row in source_rows:
        member = "sources_current/" + row["path"]
        if member not in name_set or not matches(z.read(member), row):
            source_errors.append({"path": row.get("path"), "issue": "missing or packet source hash mismatch"})
            continue
        current_file = ROOT / PurePosixPath(row["path"])
        if not current_file.exists() or current_file.read_bytes() != z.read(member):
            source_errors.append({"path": row.get("path"), "issue": "worktree differs from packet current-source snapshot"})
    check("all 87 refreshed sources bind exact packet bytes and current worktree files", len(source_rows) == 87 and not source_errors, {"bindingCount": len(source_rows), "errors": source_errors[:12]})

    candidate = read_json(z.read("current/CURRENT_SOURCE_CONFERENCE_CANDIDATE_236.json"))
    recon = candidate.get("candidateBindingReconciliation", {})
    check("current candidate is structurally equal to the queue-bound historical candidate with byte difference disclosed", candidate.get("currentAuthority") == AUTHORITY and candidate.get("currentPendingGroup", {}).get("spellIds") == TARGETS and recon.get("jsonStructuralEquality") is True and recon.get("fieldDifferences") == 0 and bool(recon.get("currentWorktreeCandidateBinding", {}).get("sha256")) and bool(recon.get("queueCandidateBinding", {}).get("sha256")), {"currentPendingGroup": candidate.get("currentPendingGroup"), "reconciliation": recon})
    leads = read_json(z.read("current/SOURCE_SEARCH_LEADS_236.json"))
    check("source-search candidates are explicitly leads, not silently promoted witnesses", leads.get("authority") == AUTHORITY and leads.get("scopeIds") == TARGETS and leads.get("leadsAreNotFindings") is True and len(leads.get("leads", [])) == 5 and {row.get("source") for row in leads.get("leads", [])} == {"catalog.json"}, leads)

    excerpt_manifest = read_json(z.read("history/Return218_EXCERPT_BINDINGS_236.json"))
    prior_archive = BASE / "rank9_defenseform8_return218_received/DD_Rank9_DefenseForm5_Director_Return218.zip"
    prior_delivery = json.loads((BASE / "rank9_defenseform8_return218_received/DD_Rank9_DefenseForm5_Director_Return218_DELIVERY.json").read_text(encoding="utf-8-sig"))
    prior_manifest_rows = {row["path"]: row for row in prior_delivery["members"]}
    excerpt_errors = []
    with zipfile.ZipFile(prior_archive) as old:
        old_names = set(old.namelist())
        for row in excerpt_manifest.get("excerpts", []):
            opath, ppath = row["originalPath"], row["packetPath"]
            if opath not in old_names or ppath not in name_set:
                excerpt_errors.append({"path": opath, "issue": "not present"})
                continue
            old_raw, new_raw = old.read(opath), z.read(ppath)
            if old_raw != new_raw or not matches(new_raw, row) or opath not in prior_manifest_rows or not matches(old_raw, prior_manifest_rows[opath]):
                excerpt_errors.append({"path": opath, "issue": "not exact or external source manifest mismatch"})
    check("all exact prior Return218 target procedures and cases are preserved under dual source delivery bindings", len(excerpt_manifest.get("excerpts", [])) == delivery.get("previousReturnExcerptCount") and not excerpt_errors, {"excerpts": len(excerpt_manifest.get("excerpts", [])), "sourceArchive": excerpt_manifest.get("sourceArchive"), "errors": excerpt_errors[:12]})
    target_cases = [row for row in excerpt_manifest.get("excerpts", []) if re.fullmatch(r"preserved_cases/[^/]+\.json|cases/[^/]+\.json", row.get("originalPath", ""))]
    target_case_spell_ids = set()
    for row in target_cases:
        name = row["packetPath"]
        case = read_json(z.read(name))
        target_case_spell_ids.add(case.get("spellId"))
    check("all 46 carried Return218 case records are limited to the three held target spells", len(target_cases) == 46 and target_case_spell_ids == set(TARGETS), {"targetCases": len(target_cases), "spellIds": sorted(target_case_spell_ids)})

    old_decision = read_json(z.read("history/Return218/DIRECTOR_DECISION.json"))
    old_blockers = read_json(z.read("history/Return218/BLOCKER_REASSESSMENT.json"))
    blocker_ids = {row.get("currentId") for row in old_blockers.get("records", []) if row.get("decision") == "RETAIN_EXACT_SOURCE_DEPENDENCY"}
    check("previous held decisions and four precise blocker IDs are retained without reopening accepted spells", old_decision.get("acceptedIds") == ["absolute-immunity", "body-to-void"] and old_decision.get("heldIds") == TARGETS and blocker_ids == {"DF218-B01", "DF218-B02", "DF218-B03", "DF218-B04"}, {"acceptedIds": old_decision.get("acceptedIds"), "heldIds": old_decision.get("heldIds"), "blockerIds": sorted(blocker_ids)})

    current_return_audit = read_json(z.read("current/RETURN235_INDEPENDENT_AUDIT.json"))
    current_return = read_json(z.read("current/RETURN235_DELIVERY.json"))
    check("latest Return235 is independently audited and preserved with final-word held", current_return_audit.get("status") == "PASS" and current_return_audit.get("failedChecks") == 0 and current_return.get("acceptedIds") == current_return.get("appliedIds") == [] and current_return.get("heldIds") == ["final-word"], {"auditStatus": current_return_audit.get("status"), "heldIds": current_return.get("heldIds")})

failures = [row for row in checks if not row["passed"]]
report = {"id": "RANK9DEFENSEFORM8-PACKET236-INDEPENDENT-AUDIT", "recordedAtUtc": datetime.now(timezone.utc).isoformat(), "status": "PASS" if not failures else "FAIL", "archive": {"path": ARCHIVE.relative_to(ROOT).as_posix(), **archive_digest}, "delivery": {"path": DELIVERY.relative_to(ROOT).as_posix(), **delivery_digest}, "authority": delivery.get("authority"), "targetIds": delivery.get("targetIds"), "currentSourceBindingCount": len(delivery.get("sourceBindings", [])), "priorReturnExcerptCount": delivery.get("previousReturnExcerptCount"), "targetCaseCount": len(target_cases) if "target_cases" in locals() else 0, "checkCount": len(checks), "passedChecks": len(checks) - len(failures), "failedChecks": len(failures), "checks": checks}
REPORT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
receipt = {"id": "RANK9DEFENSEFORM8-PACKET236-RECEIPT", "status": report["status"], "archive": report["archive"], "delivery": report["delivery"], "independentAudit": {"path": REPORT.relative_to(ROOT).as_posix(), **digest(REPORT.read_bytes())}, "checkCount": len(checks), "passedChecks": len(checks) - len(failures), "failedChecks": len(failures)}
RECEIPT.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps({"status": report["status"], "checkCount": len(checks), "passedChecks": len(checks)-len(failures), "failedChecks": len(failures), "failures": failures, "archiveSha256": archive_digest["sha256"], "targetCaseCount": report["targetCaseCount"]}, ensure_ascii=False, indent=2))
