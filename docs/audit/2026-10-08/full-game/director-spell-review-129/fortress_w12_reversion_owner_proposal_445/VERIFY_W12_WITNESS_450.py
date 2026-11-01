from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REVIEW_ROOT = ROOT.parent
PARENT = REVIEW_ROOT / "fortress_w01_structural_damage_witness_403_repack02" / "W01_REPLAY_403.json"
FILES = {
    "proposal": ROOT / "PG328_W12_REVERSION_OWNER_PROPOSAL_445_TESTONLY.json",
    "adoption": ROOT / "OWNER_PG328_W12_ADOPTION_445_TESTONLY.json",
    "witness": ROOT / "W12_WITNESS_450_TESTONLY.json",
    "validation": ROOT / "BUILD_VALIDATION_450.json",
}


def sha_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha(path: Path) -> str:
    return sha_bytes(path.read_bytes())


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


proposal, adoption = load(FILES["proposal"]), load(FILES["adoption"])
witness, validation = load(FILES["witness"]), load(FILES["validation"])
parent = load(PARENT)
snapshot_sha = sha_bytes(json.dumps(parent["stateSnapshots"]["S030"], sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8"))
commit = proposal["readAtCommit"]
bindings = proposal["sourceBindings"]
binding_checks = []
for binding in bindings:
    raw = subprocess.check_output(["git", "show", f"{commit}:{binding['path']}"])
    binding_checks.append(sha_bytes(raw) == binding["sha256"])

inputs = proposal["ownerProposedInputs"]
schedule = inputs["scheduledTimeAdvance"]
event_ordering = inputs["eventOrdering"]
boundary = witness["scopeBoundary"]
no_effects = all(boundary[key] is False for key in ("sealPresent", "FortressAcceptedOrApplied", "spellIdentityAcceptedOrApplied", "canonicalRuleChanged", "historicalParentMutated", "campaignEventsAsserted", "queueChanged", "generalizationBeyondW12")) and boundary["testOnly"] is True

checks = {
    "proposal exact hash": sha(FILES["proposal"]) == "93d31941e6a6d4d059cb3a108d0e247d07cc8e6cce395712f1c0ad45523df14c",
    "owner adoption pins exact proposal": adoption["scope"]["proposalSha256"] == sha(FILES["proposal"]) and adoption["ownerAuthorization"]["adoptsExactProposalSha256"] is True,
    "unchanged W01-403 S030 replay and snapshot": sha(PARENT) == proposal["scope"]["parentSha256"] == witness["parent"]["replaySha256"] and snapshot_sha == proposal["scope"]["parentStateSha256"] == witness["parent"]["s030SnapshotSha256"],
    "all 18 historical source bindings": len(bindings) == 18 and all(binding_checks) and witness["proposalSource"]["readAtCommit"] == commit,
    "adopted terms copied exactly": all(witness["adoptedScenario"][key] == inputs[key] for key in ("startingState", "spellAndTransformation", "perceptionAndDispel", "counterspellDecisions", "scheduledTimeAdvance", "resourceLedger", "terminalClosure", "preCastInteractions", "eventOrdering")),
    "45 START and 44 END markers": schedule["counts"] == {"starts": 45, "ends": 44} and sum(len(actor["starts"]) for actor in schedule["markersByActor"].values()) == 45 and sum(len(actor["ends"]) for actor in schedule["markersByActor"].values()) == 44,
    "12 ordered authored steps through 79.31": len(event_ordering) == 12 and event_ordering[0]["time"] == 13.1 and event_ordering[-1]["time"] == 79.31 and all(event_ordering[i]["time"] <= event_ordering[i + 1]["time"] for i in range(11)),
    "scope boundary and artifact hashes": no_effects and witness["queueAtAdoption"]["mutation"] is False and validation["status"] == "PASS" and validation["witnessSha256"] == sha(FILES["witness"]) and validation["result"]["failed"] == 0,
}
for name, passed in checks.items():
    print(("PASS" if passed else "FAIL") + ": " + name)
if not all(checks.values()):
    raise SystemExit(1)
print(f"PASS: {sum(checks.values())}/{len(checks)} verifier checks; W12 remains TEST_ONLY and unsealed.")
