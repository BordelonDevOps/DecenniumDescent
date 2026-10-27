import hashlib
import json
import zipfile
import zlib
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
OUTER_PATH = HERE / "rank9_impactexile4_return204_received" / "DD_Rank9_ImpactExile4_Director_Return204_UNACCEPTED.zip"
OLD_PATH = HERE / "rank9_summonhosts5_return202_received" / "DD_Rank9_SummonHosts5_Director_Return202.zip"
OUT = HERE / "RANK9IMPACTEXILE4_RETURN204_CARRY_FORWARD_AUDIT.json"
checks = []

def check(name, ok, detail=""):
    checks.append({"check": name, "passed": bool(ok), **({"detail": detail} if detail else {})})
    if not ok:
        raise AssertionError(name + (": " + detail if detail else ""))

def sha(data):
    return hashlib.sha256(data).hexdigest()

with zipfile.ZipFile(OUTER_PATH) as outer:
    prior = json.loads(outer.read("PRIOR_CONTEXT_PRESERVATION.json"))
    holds = json.loads(outer.read("RETURN202_HOLD_REGISTER_UNCHANGED.json"))
    inherited = json.loads(outer.read("INHERITED_BLOCKERS_UNCHANGED.json"))
    old_bytes = OLD_PATH.read_bytes()
    check("Return202 source archive byte length and SHA-256 match Return204 binding",
          len(old_bytes) == prior["sourceArchiveBinding"]["bytes"] and sha(old_bytes) == prior["sourceArchiveBinding"]["sha256"])
    with zipfile.ZipFile(OLD_PATH) as old:
        member = old.read("HOLD_REGISTER.json")
        binding = prior["holdMemberBinding"]
        check("Return202 HOLD_REGISTER member length, SHA-256, and CRC match its binding",
              len(member) == binding["bytes"] and sha(member) == binding["sha256"] and
              f"{zlib.crc32(member) & 0xffffffff:08x}" == binding["crc32"])
    check("Return202 applied IDs remain exactly Wyrm and Army",
          prior["acceptedIdsUnchanged"] == ["conjure-magmatic-wyrm", "planar-army"])
    check("Return202's 176 hold records and 15 local holds are retained",
          holds["recordCount"] == 176 and holds["localRecordCount"] == 15 and holds["inheritedRecordCount"] == 161)
    earlier = holds["currentNamedBlockersOutsideScopeUnchanged"]
    check("all seven pre-Return202 named blocker groups are unchanged",
          all(inherited.get(k) == v for k, v in earlier.items()))
    local_blockers = {
        row["spellIds"][0]: {
            "blockerIds": [row["id"]],
            "reasons": [row["missingFacts"]],
        }
        for row in holds["localRecords"]
        if row.get("blocking") is True and row["id"] in {"SH202-B01", "SH202-B02", "SH202-B03"}
    }
    check("all three Return202 blockers are carried forward with identical reasons",
          inherited["retainedReturn202Blockers"] == local_blockers)

report = {
    "id": "RANK9-IMPACTEXILE4-RETURN204-CARRY-FORWARD-AUDIT",
    "status": "PASS",
    "recordedAtUtc": datetime.now(timezone.utc).isoformat(),
    "checksPassed": len(checks),
    "checksFailed": 0,
    "checks": checks,
    "return202AcceptedIds": ["conjure-magmatic-wyrm", "planar-army"],
    "return202HeldIds": list(local_blockers),
    "retainedPriorBlockerGroups": sorted(earlier),
    "qualification": "Independent byte comparison of Return202 archive and its named hold register; prior blocker carry-forward only. No identity is accepted by this audit."
}
OUT.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print(json.dumps({"status": report["status"], "checksPassed": len(checks), "checksFailed": 0, "audit": str(OUT.relative_to(ROOT))}, indent=2))
