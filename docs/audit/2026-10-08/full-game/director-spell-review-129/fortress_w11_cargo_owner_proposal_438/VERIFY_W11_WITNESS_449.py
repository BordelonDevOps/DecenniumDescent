from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REVIEW_ROOT = ROOT.parent
PARENT = REVIEW_ROOT / "fortress_w01_structural_damage_witness_403_repack02" / "W01_REPLAY_403.json"
FILES = {
    "proposal": ROOT / "OWNER_PG328_W11_ADOPTION_PROPOSAL_438.json",
    "adoption": ROOT / "OWNER_PG328_W11_ADOPTION_438_TESTONLY.json",
    "trace": ROOT / "W11_LIFECYCLE_TRACE_438.json",
    "readback": ROOT / "DIRECTOR_READBACK_438.json",
    "witness": ROOT / "W11_WITNESS_449_TESTONLY.json",
    "validation": ROOT / "BUILD_VALIDATION_449.json",
}


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


proposal, adoption, trace = (load(FILES[key]) for key in ("proposal", "adoption", "trace"))
readback, witness, validation = (load(FILES[key]) for key in ("readback", "witness", "validation"))
parent = load(PARENT)
snapshot = parent["stateSnapshots"]["S030"]
snapshot_sha = hashlib.sha256(
    json.dumps(snapshot, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
).hexdigest()

checks = {
    "proposal exact hash": sha(FILES["proposal"]) == "44c150647453fb762aec288fc83ce2afe0a77c160ca810682919d320078ae3de",
    "adoption pins exact proposal": adoption["scope"]["proposalSha256"] == sha(FILES["proposal"]),
    "parent replay and S030 unchanged": sha(PARENT) == proposal["parent"]["sha256"] == witness["parent"]["replaySha256"] and snapshot_sha == witness["parent"]["s030SnapshotSha256"],
    "Director proposal readiness receipt": "ready for owner adoption" in readback["ruling"].lower(),
    "trace branch explicitly mapped after adoption": trace["branchId"] == "PG328-W11-R1-PROPOSED" and witness["trace"]["adoptedBranchId"] == "PG328-W11-R1",
    "74 ordered turns, 24 events, 10 actions, 10 phases": len(trace["turnMarkers"]) == 74 and len(trace["events"]) == 24 and len(trace["actions"]) == 10 and len(trace["petPhases"]) == 10 and all(trace["turnMarkers"][i]["startSeconds"] < trace["turnMarkers"][i + 1]["startSeconds"] for i in range(73)),
    "no campaign/canon/queue/acceptance effects": all(trace["boundary"][key] is False for key in ("parentW01Mutated", "campaignEventsAsserted", "FortressAcceptedOrApplied", "canonChanged", "queueChanged", "sealIssued", "sealed")) and witness["terminalAndQueueBoundary"]["queueChanged"] is False,
    "validation and witness hashes": validation["status"] == "PASS" and validation["witnessSha256"] == sha(FILES["witness"]) and validation["result"]["failed"] == 0,
}
for name, ok in checks.items():
    print(("PASS" if ok else "FAIL") + ": " + name)
if not all(checks.values()):
    raise SystemExit(1)
print(f"PASS: {sum(checks.values())}/{len(checks)} verifier checks; W11 remains TEST_ONLY and unsealed.")
