from __future__ import annotations

import hashlib
import json
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REVIEW = ROOT.parent
PROPOSAL_PATH = REVIEW / "fortress_w05_w10_joint_preflight_443" / "PG328_W05_W10_JOINT_PROPOSAL_443_TESTONLY.json"
ADOPTION_PATH = REVIEW / "fortress_w05_w10_joint_preflight_443" / "OWNER_PG328_W05_W10_ADOPTION_443_TESTONLY.json"
PARENT_PATH = REVIEW / "fortress_w01_structural_damage_witness_403_repack02" / "W01_REPLAY_403.json"
WITNESS_PATH = ROOT / "W05_W10_WITNESS_451_TESTONLY.json"
VALIDATION_PATH = ROOT / "BUILD_VALIDATION_451.json"
VERIFY_PATH = ROOT / "VERIFY_W05_W10_WITNESS_451.py"
README_PATH = ROOT / "README_WITNESS_451.md"
BUILDER_PATH = ROOT / "BUILD_W05_W10_WITNESS_451.py"
MANIFEST_PATH = ROOT / "MANIFEST_451.json"
ARCHIVE_PATH = ROOT / "DD_Fortress_W05_W10_Witness_451_TESTONLY.zip"
DELIVERY_PATH = ROOT / "DELIVERY_451.json"
EXPECTED_PROPOSAL_SHA = "1fd045800181958d34e141763e07fe230a2261a3879e8115869551c2a6d20b85"
EXPECTED_PARENT_SHA = "2b60ae35d828bd6028d71f202c1dd61c823d6212bb45c7f633ecd8f6b51d44fb"


def sha_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha(path: Path) -> str:
    return sha_bytes(path.read_bytes())


def dump(path: Path, value: object) -> None:
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def main() -> None:
    proposal = json.loads(PROPOSAL_PATH.read_text(encoding="utf-8"))
    adoption = json.loads(ADOPTION_PATH.read_text(encoding="utf-8"))
    parent = json.loads(PARENT_PATH.read_text(encoding="utf-8"))
    inputs = proposal["ownerProposedInputs"]
    snap = parent["stateSnapshots"]["S030"]
    snap_sha = sha_bytes(json.dumps(snap, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8"))

    events: list[dict] = []

    def add(time: float | None, order: int, kind: str, data: dict) -> None:
        events.append({"timeSeconds": time, "orderAtTime": order, "kind": kind, "details": data})

    focus = inputs["localGeometry"]["focusSetDown"]
    add(focus["time"], 1, "FOCUS_CONTROLLED_SETDOWN", focus)

    bolts = inputs["bolts"]
    offsets = bolts["eventOffsets"]
    for idx, start in enumerate(bolts["starts"], start=1):
        add(start + offsets["commit"], 1, "ARCANE_BOLT_COMMIT", {"bolt": idx, "startSeconds": start, "costRP": bolts["costRP"], "attack": bolts["attack"]})
        add(start + offsets["counterspellWindow"], 1, "COUNTERSPELL_WINDOW", {"bolt": idx, "response": inputs["responses"][0]})
        if idx < len(bolts["starts"]):
            add(start + offsets["resolve"], 1, "ARCANE_BOLT_RESOLVE", {"bolt": idx, "damage": bolts["damage"], "hpAfter": bolts["hpSequence"][idx]})
        else:
            add(start + offsets["resolve"], 1, "ARCANE_BOLT_DAMAGE", {"bolt": idx, "damage": bolts["damage"], "hpBefore": bolts["hpSequence"][-2], "hpAfter": bolts["hpSequence"][-1], "overflow": bolts["overflow"], "critical": bolts["critical"], "instantDeath": bolts["instantDeath"]})
            save = inputs["woundSave"]
            add(save["event"], save["substep"], "WOUND_SAVE", save)
            add(save["event"], 3, "ZERO_HP_CALLBACKS_AND_TILE_RELEASE", {"rule": save["orderedDamageSettlement"][2]["rule"], "tileDrop": inputs["localGeometry"]["tileDrop"]})

    cadence = inputs["cadence"]
    for idx, start in enumerate(cadence["groundingStarts"], start=1):
        add(start, 1, "GROUNDING_ACTION", {"ordinal": idx, "rule": cadence["grounding"], "rpAfterBolts": cadence["rpAfterBolts"]})

    death = inputs["deathSaves"]
    for idx, start in enumerate(death["starts"], start=1):
        add(start, 1, "DEATH_SAVE", {"ordinal": idx, "dieFace": death["dieFaceEach"], "modifier": death["modifier"], "result": "failure"})
    add(death["starts"][-1], 2, "A_BECOMES_DEAD", {"result": death["result"]})

    sight = inputs["localGeometry"]["sight"]
    add(sight["time"], 1, "ARCANE_SIGHT", sight)
    add(sight["counterspellWindow"], 1, "SIGHT_COUNTERSPELL_WINDOW", {"responders": sight["responders"]})
    dispel = inputs["localGeometry"]["dispel"]
    add(dispel["time"], 1, "ARCH_DISPEL", dispel)
    add(dispel["counterspellWindow"], 1, "DISPEL_COUNTERSPELL_WINDOW", {"responders": dispel["responders"]})
    add(None, 1, "Q27_TERMINAL_PROJECTION", {"trigger": "After the authored Arch Dispel resolution; no additional resolution timestamp is asserted.", "projection": inputs["localGeometry"]["q27Projection"]})

    events.sort(key=lambda event: (float("inf") if event["timeSeconds"] is None else event["timeSeconds"], event["orderAtTime"], event["kind"]))
    for idx, event in enumerate(events, start=1):
        event["eventId"] = f"PG328-W05-W10-R1-E{idx:03d}"

    source_bindings = []
    for binding in proposal["sourceBindings"]:
        path = REVIEW.parents[4] / binding["path"]
        # Paths are repository-relative; REVIEW.parents[4] is the checkout root.
        source_bindings.append({**binding, "actualSha256": sha(path), "matches": sha(path) == binding["sha256"]})

    witness = {
        "schemaVersion": 1,
        "id": "PG328-W05-W10-WITNESS-451",
        "classification": "TEST_ONLY_HYPOTHETICAL_BRANCH_WITNESS",
        "status": "TEST_ONLY_UNSEALED_PENDING_DIRECTOR_REVIEW",
        "branchId": proposal["scope"]["branch"],
        "components": proposal["scope"]["components"],
        "spell": proposal["scope"]["spell"],
        "identityHold": proposal["scope"]["hold"],
        "hypotheticalOnly": True,
        "campaignOccurrenceAsserted": False,
        "adoption": {
            "path": str(ADOPTION_PATH.relative_to(REVIEW)),
            "sha256": sha(ADOPTION_PATH),
            "proposalPath": str(PROPOSAL_PATH.relative_to(REVIEW)),
            "proposalSha256": sha(PROPOSAL_PATH),
            "exactProposalAdopted": adoption["scope"]["proposalSha256"] == sha(PROPOSAL_PATH),
            "ownerAuthorization": adoption["ownerAuthorization"]["verbatim"],
            "directorStatus": adoption["directorReview"]["status"],
        },
        "parent": {
            "path": str(PARENT_PATH.relative_to(REVIEW)),
            "pointer": "#/stateSnapshots/S030",
            "replaySha256": sha(PARENT_PATH),
            "snapshotSha256": snap_sha,
            "timeSeconds": proposal["scope"]["parentTime"],
            "parentMutated": False,
        },
        "sourceBindings": source_bindings,
        "adoptedScenario": inputs,
        "eventTrace": {
            "semantics": "Ordered hypothetical testimony derived only from proposal 443 inputs; no runtime execution or campaign assertion.",
            "eventCount": len(events),
            "events": events,
            "terminalProjection": inputs["localGeometry"]["q27Projection"],
        },
        "queueAtAdoption": {
            "reviewedApplied": adoption["queueAuthorityAtAdoption"]["reviewedApplied"],
            "pending": adoption["queueAuthorityAtAdoption"]["pending"],
            "acceptedUnapplied": adoption["queueAuthorityAtAdoption"]["acceptedUnapplied"],
            "mutation": False,
            "identityAcceptedOrApplied": False,
        },
        "scopeBoundary": {
            "testOnly": True,
            "sealPresent": False,
            "FortressAcceptedOrApplied": False,
            "spellIdentityAcceptedOrApplied": False,
            "PG200_B06Closed": False,
            "canonicalRuleChanged": False,
            "historicalParentMutated": False,
            "campaignEventsAsserted": False,
            "queueChanged": False,
            "generalizationBeyondW05W10": False,
        },
    }
    dump(WITNESS_PATH, witness)

    checks = {
        "proposal exact approved hash": sha(PROPOSAL_PATH) == EXPECTED_PROPOSAL_SHA,
        "owner adoption pins exact proposal": adoption["scope"]["proposalSha256"] == sha(PROPOSAL_PATH),
        "Director readiness and owner adoption are present": adoption["directorReview"]["status"] == "PASS_READY_FOR_OWNER_ADOPTION" and adoption["ownerAuthorization"]["adoptsExactProposalSha256"] is True,
        "parent and S030 source remain exact": sha(PARENT_PATH) == EXPECTED_PARENT_SHA == proposal["scope"]["parentSha256"] and snap_sha == inputs["parent"].get("s030SnapshotSha256", snap_sha),
        "all proposal source bindings match current checkout": len(source_bindings) == 12 and all(item["matches"] for item in source_bindings),
        "scenario is copied byte-for-value from adopted proposal": witness["adoptedScenario"] == proposal["ownerProposedInputs"],
        "nine bolts have exact commit/window/resolve schedule": sum(e["kind"] == "ARCANE_BOLT_COMMIT" for e in events) == 9 and sum(e["kind"] == "COUNTERSPELL_WINDOW" for e in events) == 9 and sum(e["kind"] == "ARCANE_BOLT_RESOLVE" for e in events) == 8 and sum(e["kind"] == "ARCANE_BOLT_DAMAGE" for e in events) == 1,
        "Wound save and callbacks preserve exact substep ordering": [e["kind"] for e in events if e["timeSeconds"] == 109.3 and e["kind"] in ("ARCANE_BOLT_DAMAGE", "WOUND_SAVE", "ZERO_HP_CALLBACKS_AND_TILE_RELEASE")] == ["ARCANE_BOLT_DAMAGE", "WOUND_SAVE", "ZERO_HP_CALLBACKS_AND_TILE_RELEASE"],
        "death, sight, and dispel timing copy exact proposal": [e["timeSeconds"] for e in events if e["kind"] == "DEATH_SAVE"] == death["starts"] and [e["timeSeconds"] for e in events if e["kind"] == "ARCANE_SIGHT"] == [sight["time"]] and [e["timeSeconds"] for e in events if e["kind"] == "ARCH_DISPEL"] == [dispel["time"]],
        "Q27 projection matches adopted terms": witness["eventTrace"]["terminalProjection"] == inputs["localGeometry"]["q27Projection"],
        "event order is deterministic and unique": len({e["eventId"] for e in events}) == len(events) and events == sorted(events, key=lambda e: (float("inf") if e["timeSeconds"] is None else e["timeSeconds"], e["orderAtTime"], e["kind"])),
        "TEST_ONLY queue and non-effect boundaries hold": witness["queueAtAdoption"] == {"reviewedApplied": 830, "pending": 18, "acceptedUnapplied": 0, "mutation": False, "identityAcceptedOrApplied": False} and all(value is False for key, value in witness["scopeBoundary"].items() if key != "testOnly"),
    }
    validation = {
        "id": "PG328-W05-W10-BUILD-VALIDATION-451",
        "classification": "TEST_ONLY_WITNESS_BUILD_VALIDATION",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "witnessPath": str(WITNESS_PATH.relative_to(REVIEW)),
        "witnessSha256": sha(WITNESS_PATH),
        "eventCount": len(events),
        "checks": checks,
        "passed": sum(checks.values()),
        "failed": sum(not value for value in checks.values()),
        "boundary": "W05/W10 hypothetical witness only; no seal, Fortress identity acceptance/application, canon, campaign fact, parent mutation, or queue mutation.",
    }
    dump(VALIDATION_PATH, validation)
    if not all(checks.values()):
        raise SystemExit("Witness validation failed; inspect BUILD_VALIDATION_451.json")

    README_PATH.write_text(
        "# W05/W10 hypothetical witness 451\n\n"
        "This TEST_ONLY witness constructs one reversible hypothetical PG328-W05-W10-R1 branch from unchanged W01-403 S030, using the exact owner-adopted proposal 443. It preserves the separate W05 and W10 components and copies the proposal inputs without adding mechanics or campaign facts.\n\n"
        "The ordered trace reports the authored bolt, wound-save, death-save, sight/dispel, and Q27 projection sequence. It does not claim runtime execution. The result remains unsealed and does not accept or apply Fortress, close PG200-B06, change canon, mutate S030, or alter the 830/18/0 queue.\n\n"
        "Run `python VERIFY_W05_W10_WITNESS_451.py` from this directory to verify adoption, parent, source bindings, sequence and scope.\n",
        encoding="utf-8",
    )

    # Include only exact proposal/adoption inputs and generated review artifacts.
    package_files = [
        BUILDER_PATH,
        VERIFY_PATH,
        PROPOSAL_PATH,
        ADOPTION_PATH,
        WITNESS_PATH,
        VALIDATION_PATH,
        README_PATH,
    ]
    manifest = {
        "id": "PG328-W05-W10-MANIFEST-451",
        "classification": "TEST_ONLY_REVIEW_PACKAGE",
        "files": [
            {"path": str(path.relative_to(REVIEW)), "bytes": path.stat().st_size, "sha256": sha(path)}
            for path in package_files
        ],
    }
    dump(MANIFEST_PATH, manifest)
    package_files.append(MANIFEST_PATH)
    with zipfile.ZipFile(ARCHIVE_PATH, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for path in package_files:
            archive.write(path, arcname=path.name)
    dump(DELIVERY_PATH, {
        "id": "PG328-W05-W10-DELIVERY-451",
        "classification": "TEST_ONLY_UNSEALED_PENDING_DIRECTOR_REVIEW",
        "witnessPath": str(WITNESS_PATH.relative_to(REVIEW)),
        "witnessBytes": WITNESS_PATH.stat().st_size,
        "witnessSha256": sha(WITNESS_PATH),
        "archivePath": str(ARCHIVE_PATH.relative_to(REVIEW)),
        "archiveBytes": ARCHIVE_PATH.stat().st_size,
        "archiveSha256": sha(ARCHIVE_PATH),
        "manifestPath": str(MANIFEST_PATH.relative_to(REVIEW)),
        "validationPath": str(VALIDATION_PATH.relative_to(REVIEW)),
        "validationSha256": sha(VALIDATION_PATH),
        "queue": {"reviewedApplied": 830, "pending": 18, "acceptedUnapplied": 0, "changed": False},
        "directorReviewRequested": True,
    })
    print(json.dumps({"status": validation["status"], "checksPassed": validation["passed"], "checksFailed": validation["failed"], "events": len(events), "witnessSha256": sha(WITNESS_PATH), "archiveSha256": sha(ARCHIVE_PATH)}, indent=2))


if __name__ == "__main__":
    main()
