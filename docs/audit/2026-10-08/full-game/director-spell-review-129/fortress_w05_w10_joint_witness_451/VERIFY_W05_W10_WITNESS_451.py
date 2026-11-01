from __future__ import annotations

import hashlib
import json
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REVIEW = ROOT.parent
REPO = REVIEW.parents[4]
PROPOSAL = REVIEW / "fortress_w05_w10_joint_preflight_443" / "PG328_W05_W10_JOINT_PROPOSAL_443_TESTONLY.json"
ADOPTION = REVIEW / "fortress_w05_w10_joint_preflight_443" / "OWNER_PG328_W05_W10_ADOPTION_443_TESTONLY.json"
PARENT = REVIEW / "fortress_w01_structural_damage_witness_403_repack02" / "W01_REPLAY_403.json"
WITNESS = ROOT / "W05_W10_WITNESS_451_TESTONLY.json"
VALIDATION = ROOT / "BUILD_VALIDATION_451.json"
MANIFEST = ROOT / "MANIFEST_451.json"
ARCHIVE = ROOT / "DD_Fortress_W05_W10_Witness_451_TESTONLY.zip"
DELIVERY = ROOT / "DELIVERY_451.json"


def sha_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha(path: Path) -> str:
    return sha_bytes(path.read_bytes())


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


proposal, adoption, parent = load(PROPOSAL), load(ADOPTION), load(PARENT)
witness, validation = load(WITNESS), load(VALIDATION)
manifest, delivery = load(MANIFEST), load(DELIVERY)
inputs = proposal["ownerProposedInputs"]
snap_sha = sha_bytes(json.dumps(parent["stateSnapshots"]["S030"], sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8"))
events = witness["eventTrace"]["events"]
root_inputs = REPO
binding_checks = [
    sha(root_inputs / expected["path"]) == expected["sha256"] == actual["actualSha256"]
    and actual["path"] == expected["path"]
    and actual["matches"] is True
    for expected, actual in zip(proposal["sourceBindings"], witness["sourceBindings"], strict=True)
]
event_order = sorted(events, key=lambda event: (float("inf") if event["timeSeconds"] is None else event["timeSeconds"], event["orderAtTime"], event["kind"]))
scope = witness["scopeBoundary"]
queue = witness["queueAtAdoption"]

checks = {
    "proposal is exact owner-approved SHA-256": sha(PROPOSAL) == "1fd045800181958d34e141763e07fe230a2261a3879e8115869551c2a6d20b85",
    "owner adoption pins proposal and has explicit authorization": adoption["scope"]["proposalSha256"] == sha(PROPOSAL) and adoption["ownerAuthorization"]["adoptsExactProposalSha256"] is True,
    "Director marked exact proposal ready for owner adoption": adoption["directorReview"]["status"] == "PASS_READY_FOR_OWNER_ADOPTION",
    "unchanged W01-403 S030 parent and snapshot": sha(PARENT) == proposal["scope"]["parentSha256"] == witness["parent"]["replaySha256"] and snap_sha == witness["parent"]["snapshotSha256"],
    "all 12 proposal source bindings still match": len(binding_checks) == 12 and all(binding_checks) and all(item["matches"] for item in witness["sourceBindings"]),
    "adopted scenario is copied exactly": witness["adoptedScenario"] == inputs,
    "nine bolt commits and windows, eight earlier resolves, final damage": sum(event["kind"] == "ARCANE_BOLT_COMMIT" for event in events) == 9 and sum(event["kind"] == "COUNTERSPELL_WINDOW" for event in events) == 9 and sum(event["kind"] == "ARCANE_BOLT_RESOLVE" for event in events) == 8 and sum(event["kind"] == "ARCANE_BOLT_DAMAGE" for event in events) == 1,
    "focus set-down and all Grounding starts match proposal": [event["timeSeconds"] for event in events if event["kind"] == "FOCUS_CONTROLLED_SETDOWN"] == [18.1] and [event["timeSeconds"] for event in events if event["kind"] == "GROUNDING_ACTION"] == inputs["cadence"]["groundingStarts"],
    "final damage precedes Wound save and callback release": [event["kind"] for event in events if event["timeSeconds"] == 109.3 and event["kind"] in ("ARCANE_BOLT_DAMAGE", "WOUND_SAVE", "ZERO_HP_CALLBACKS_AND_TILE_RELEASE")] == ["ARCANE_BOLT_DAMAGE", "WOUND_SAVE", "ZERO_HP_CALLBACKS_AND_TILE_RELEASE"],
    "three failed death saves and Dead transition at 126": [event["timeSeconds"] for event in events if event["kind"] == "DEATH_SAVE"] == [114, 120, 126] and [event["timeSeconds"] for event in events if event["kind"] == "A_BECOMES_DEAD"] == [126],
    "Sight and Dispel timing and Q27 projection match proposal": [event["timeSeconds"] for event in events if event["kind"] == "ARCANE_SIGHT"] == [inputs["localGeometry"]["sight"]["time"]] and [event["timeSeconds"] for event in events if event["kind"] == "ARCH_DISPEL"] == [inputs["localGeometry"]["dispel"]["time"]] and witness["eventTrace"]["terminalProjection"] == inputs["localGeometry"]["q27Projection"],
    "event IDs unique and trace ordered": len({event["eventId"] for event in events}) == len(events) and events == event_order,
    "queue remains 830/18/0 and unmodified": queue == {"reviewedApplied": 830, "pending": 18, "acceptedUnapplied": 0, "mutation": False, "identityAcceptedOrApplied": False},
    "no seal, acceptance, campaign, canon, parent, or queue effect": scope["testOnly"] is True and all(value is False for key, value in scope.items() if key != "testOnly") and witness["parent"]["parentMutated"] is False,
    "build validation binds witness and reports 12/0": validation["status"] == "PASS" and validation["witnessSha256"] == sha(WITNESS) and validation["passed"] == 12 and validation["failed"] == 0,
    "archive hash, delivery, and manifest bindings": delivery["archiveSha256"] == sha(ARCHIVE) and delivery["witnessSha256"] == sha(WITNESS) and delivery["validationSha256"] == sha(VALIDATION) and all(sha(REVIEW / item["path"]) == item["sha256"] for item in manifest["files"]),
}

with zipfile.ZipFile(ARCHIVE) as archive:
    archive_ok = archive.testzip() is None and {"W05_W10_WITNESS_451_TESTONLY.json", "BUILD_VALIDATION_451.json", "MANIFEST_451.json"}.issubset(set(archive.namelist()))
checks["archive opens and contains key artifacts"] = archive_ok

for name, ok in checks.items():
    print(("PASS" if ok else "FAIL") + ": " + name)
if not all(checks.values()):
    raise SystemExit(1)
print(f"PASS: {sum(checks.values())}/{len(checks)} verifier checks; W05/W10 remains TEST_ONLY and unsealed.")
