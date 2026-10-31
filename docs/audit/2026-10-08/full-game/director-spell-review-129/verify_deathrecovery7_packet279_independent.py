from __future__ import annotations

import hashlib
import io
import json
import pathlib
import re
import zipfile
import zlib
from datetime import datetime, timezone

ROOT = pathlib.Path(__file__).resolve().parents[5]
BASE = ROOT / "docs/audit/2026-10-08/full-game/director-spell-review-129"
OUT = BASE / "rank9_deathrecovery7_current_source_279_prepared_review2"
ARCHIVE = OUT / "DD_Rank9_DeathRecovery7_CurrentSource_279.zip"
DELIVERY = OUT / "DD_Rank9_DeathRecovery7_CurrentSource_279_DELIVERY.json"
REPORT = BASE / "RANK9DEATHRECOVERY7_PACKET279_INDEPENDENT_AUDIT.json"
RECEIPT = BASE / "RANK9DEATHRECOVERY7_PACKET279_RECEIPT.json"
TARGETS = ["final-word"]
AUTH = {"reviewedApplied": 816, "pending": 32, "acceptedUnapplied": 0,
        "completeStandaloneProcedures": 540, "scopedInterfaces": 173}
CHECKS: list[dict] = []


def digest(raw: bytes) -> dict:
    return {"bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest(), "crc32": f"{zlib.crc32(raw) & 0xffffffff:08x}"}


def readj(raw: bytes):
    return json.loads(raw.decode("utf-8-sig"))


def check(name: str, passed: bool, detail=None) -> None:
    CHECKS.append({"check": name, "passed": bool(passed), "detail": detail})


def matches(raw: bytes, expected: dict) -> bool:
    got = digest(raw)
    return all(got.get(k) == expected.get(k) for k in ("bytes", "sha256")) and (expected.get("crc32") is None or got["crc32"] == expected["crc32"])


def safe(name: str) -> bool:
    p = pathlib.PurePosixPath(name)
    return bool(name) and not p.is_absolute() and ".." not in p.parts and "\\" not in name and not re.match(r"^[A-Za-z]:", name)


d = readj(DELIVERY.read_bytes())
archive_bytes = ARCHIVE.read_bytes()
archive_digest = digest(archive_bytes)
check("archive byte count, SHA-256 and CRC32 match delivery", matches(archive_bytes, d.get("archive", {})), archive_digest)
check("delivery exact scope/authority and no acceptance/application", d.get("group") == "rank9-death-recovery7" and d.get("targetIds") == TARGETS and d.get("authority") == AUTH and d.get("acceptedIds") == d.get("appliedIds") == [] and d.get("canonicalChanges") is False and d.get("githubChanges") is False and d.get("runtimeExecuted") is False, {k: d.get(k) for k in ["group", "targetIds", "authority", "acceptedIds", "appliedIds"]})
check("archive is below GitHub's regular 100 MB blob limit", len(archive_bytes) < 100_000_000, len(archive_bytes))

z = zipfile.ZipFile(io.BytesIO(archive_bytes))
names, name_set = z.namelist(), set(z.namelist())
ext = {x.get("path"): x for x in d.get("members", []) if isinstance(x, dict)}
check("ZIP integrity and unique safe member names", z.testzip() is None and len(names) == len(name_set) and all(safe(n) for n in names) and all(not i.is_dir() for i in z.infolist()), {"members": len(names)})
check("exact delivery allowlist and member binding cover all ZIP entries", set(ext) == name_set and set(d.get("exactAllowlist", [])) == name_set and len(ext) == d.get("memberCount") == len(names) and d.get("payloadCount") == len(names)-1, {"archive": len(names), "deliveryMembers": len(ext)})
bad = [n for n in names if n not in ext or not matches(z.read(n), ext[n])]
check("all archive members match external byte/SHA/CRC", not bad, bad[:15])
manifest_raw = z.read("MANIFEST.json")
manifest = readj(manifest_raw)
rows = {x.get("path"): x for x in manifest.get("members", [])}
check("embedded manifest is externally bound and covers all payload members", matches(manifest_raw, d.get("memberManifest", {})) and set(rows) == name_set-{"MANIFEST.json"} and len(rows) == d.get("payloadCount"), {"manifest": len(rows), "payload": len(name_set)-1})
inner_bad = [n for n, r in rows.items() if n not in name_set or not matches(z.read(n), r)]
check("all payload members match embedded manifest", not inner_bad, inner_bad[:15])

candidate = readj(z.read("current/CURRENT_SOURCE_CONFERENCE_CANDIDATE_279.json"))
context = readj(z.read("CURRENT_CONTEXT_279.json"))
request = z.read("REQUEST_279.txt").decode("utf-8")
check("candidate/context scope only final-word at 816/32", candidate.get("currentPendingGroup") == {"group": "rank9-death-recovery7", "spellIds": TARGETS, "count": 1} and candidate.get("currentAuthority") == AUTH and context.get("authority") == AUTH and context.get("targetGroup") == {"group": "rank9-death-recovery7", "pendingIds": TARGETS, "count": 1}, context.get("targetGroup"))
check("request states exact current snapshot split and no other identity scope", "Exact target: final-word. No other identity is in scope." in request and "separately attached final queue/handoff/pending snapshots 279 are authoritative" in request and "No application or canonical/runtime/GitHub changes are requested" in request, request[:700])
check("candidate contains 74 refreshed source bindings", len(candidate.get("sourceBindings", [])) == 74 and candidate.get("sourceBindingRefresh", {}).get("sourceContentsFromCurrentWorkingTree") is True, len(candidate.get("sourceBindings", [])))
source_bad=[]
for r in candidate.get("sourceBindings", []):
    member="sources_current/"+r["path"]
    if member not in name_set or not matches(z.read(member),r): source_bad.append(r.get("path"))
    local=ROOT/pathlib.PurePosixPath(r["path"])
    if not local.is_file() or not matches(local.read_bytes(),r): source_bad.append("working-tree:"+r.get("path",""))
check("all refreshed sources match archive and current working tree", not source_bad, source_bad[:15])

idx=readj(z.read("current/DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json"))
cat=readj(z.read("current/DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json"))
ie={r.get("id"):r for r in idx.get("entries",[])}; ce={r.get("id"):r for r in cat.get("spells",[])}
check("current index/catalog contain 32 pending and final-word remains non-operational", idx.get("authoredCounts")=={"reviewed":816,"pending":32} and sum(r.get("authoredStatus")=="pending-authored-procedure" for r in idx.get("entries",[]))==32 and ie.get("final-word",{}).get("authoredStatus")=="pending-authored-procedure" and ie.get("final-word",{}).get("sourceStatus")=="blocked-pending-operational-review" and ce.get("final-word",{}).get("operational") is None, ie.get("final-word"))
check("current target record equals current index/catalog bytes", candidate.get("currentReviewTargets",[{}])[0].get("currentIndexEntry")==ie.get("final-word") and candidate.get("currentReviewTargets",[{}])[0].get("completeCurrentCatalogSourceAndAccess")==ce.get("final-word"), candidate.get("currentReviewTargets",[{}])[0].get("spellId"))

for base_name in ["CURRENT_SPELL_QUEUE_278.json","CURRENT_HANDOFF_278.json","CURRENT32_PENDING_IDENTITY_AUDIT_278.json"]:
    member="parent_snapshot/"+base_name
    expected=candidate.get("currentAuthorityEvidence",{}).get({"CURRENT_SPELL_QUEUE_278.json":"parentQueue278","CURRENT_HANDOFF_278.json":"parentHandoff278","CURRENT32_PENDING_IDENTITY_AUDIT_278.json":"parentPendingIdentityAudit278"}[base_name],{})
    check(f"parent snapshot {base_name} is explicitly named and bound", member in name_set and matches(z.read(member),expected), digest(z.read(member)) if member in name_set else None)
check("archive carries the Return278 ruling and check, not stale final snapshots", "current/docs/audit/2026-10-08/full-game/director-spell-review-129/PSYCHICFEAR7_DIRECTOR_RULING_278.json" in name_set and "current/docs/audit/2026-10-08/full-game/director-spell-review-129/PSYCHICFEAR7_DIRECTOR_RULING_278_CROSSCHECK.json" in name_set and not any(n.endswith("CURRENT_SPELL_QUEUE_279.json") or n.endswith("CURRENT_HANDOFF_279.json") or n.endswith("CURRENT32_PENDING_IDENTITY_AUDIT_279.json") for n in names), None)

old_return_decision=readj(z.read("history/RETURN217_EXTRACTED_DIRECTOR_DECISION.json"))
old_blockers=readj(z.read("history/RETURN217_EXTRACTED_BLOCKERS.json"))
fw=[x for x in old_blockers.get("blockers",[]) if x.get("id")=="DR217-B01"]
check("Return217 history retains only doom/eternal-pact acceptance and final-word DR217-B01 hold", old_return_decision.get("acceptedIds")==["doom","eternal-pact"] and "final-word" in old_return_decision.get("heldIds",[]) and len(fw)==1, old_return_decision.get("heldIds"))
case_members=[n for n in names if re.fullmatch(r"history/Return217/preserved_cases/DR184-FINAL-WORD-[^/]+\.json",n)]
local_return=BASE/"rank9_deathrecovery7_return217_received/DD_Rank9_DeathRecovery3_Director_Return217.zip"
case_bad=[]
with zipfile.ZipFile(local_return) as source:
    for n in case_members:
        rel=n.split("history/Return217/",1)[1]
        if rel not in source.namelist() or source.read(rel)!=z.read(n): case_bad.append(rel)
check("all 16 preserved final-word cases are byte-exact to Return217 archive", len(case_members)==16 and not case_bad, case_bad)
check("prior Return235 audits and receipt are preserved", all(n in name_set for n in ["history/RETURN235_INDEPENDENT_AUDIT.json","history/RETURN235_RECEIPT.json","history/DD_Rank9_FinalWord_Director_Return235_HELD.zip"]) and readj(z.read("history/RETURN235_INDEPENDENT_AUDIT.json")).get("status")=="PASS", None)

q=json.loads((BASE/"CURRENT_SPELL_QUEUE_279.json").read_text(encoding="utf-8-sig"))
h=json.loads((BASE/"CURRENT_HANDOFF_279.json").read_text(encoding="utf-8-sig"))
p=json.loads((BASE/"CURRENT32_PENDING_IDENTITY_AUDIT_279.json").read_text(encoding="utf-8-sig"))
check("separate final queue/handoff/pending snapshots agree on authority and final-word", q.get("currentAuthority")==h.get("currentAuthority")==p.get("authority")==AUTH and q.get("nextGroup")==h.get("nextGroup")=="rank9-death-recovery7" and q.get("nextPendingIds")==h.get("nextPendingIds")==TARGETS and p.get("preparedNextGroup",{}).get("pendingIds")==TARGETS and p.get("pendingCount")==32, {"queue":q.get("nextGroup"),"handoff":h.get("nextGroup"),"pending":p.get("pendingCount")})
check("external snapshots bind this exact Packet279 archive and delivery", q.get("currentPacket",{}).get("sha256")==archive_digest["sha256"] and h.get("currentPacket",{}).get("sha256")==archive_digest["sha256"] and q.get("currentDeliveryManifest",{}).get("sha256")==digest(DELIVERY.read_bytes())["sha256"] and h.get("currentDeliveryManifest",{}).get("sha256")==digest(DELIVERY.read_bytes())["sha256"], {"archive":archive_digest,"delivery":digest(DELIVERY.read_bytes())})

fails=[r for r in CHECKS if not r["passed"]]
report={"id":"RANK9DEATHRECOVERY7-PACKET279-INDEPENDENT-AUDIT","checkedAtUtc":datetime.now(timezone.utc).isoformat(),
        "status":"PASS" if not fails else "FAIL","archive":{"path":ARCHIVE.relative_to(ROOT).as_posix(),**archive_digest},
        "delivery":{"path":DELIVERY.relative_to(ROOT).as_posix(),**digest(DELIVERY.read_bytes())},"authority":AUTH,
        "group":"rank9-death-recovery7","targetIds":TARGETS,"checkCount":len(CHECKS),"passedChecks":len(CHECKS)-len(fails),"failedChecks":len(fails),"checks":CHECKS}
REPORT.write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
receipt={"id":"RANK9DEATHRECOVERY7-PACKET279-RECEIPT","status":report["status"],"archive":report["archive"],"delivery":report["delivery"],
         "independentAudit":{"path":REPORT.relative_to(ROOT).as_posix(),**digest(REPORT.read_bytes())},"checkCount":len(CHECKS),
         "passedChecks":len(CHECKS)-len(fails),"failedChecks":len(fails)}
RECEIPT.write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
print(json.dumps({"status":report["status"],"checkCount":len(CHECKS),"passedChecks":report["passedChecks"],"failedChecks":len(fails),"failures":fails,"archiveSha256":archive_digest["sha256"]},indent=2))
