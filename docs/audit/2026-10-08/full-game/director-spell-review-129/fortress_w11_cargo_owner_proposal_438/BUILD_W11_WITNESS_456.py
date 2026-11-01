from __future__ import annotations
import copy, hashlib, json, zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REVIEW = ROOT.parent
REPO = ROOT.parents[5]
BASE = REVIEW / "fortress_w01_structural_damage_witness_403_repack02" / "W01_REPLAY_403.json"
P = ROOT / "OWNER_PG328_W11_ADOPTION_PROPOSAL_438.json"
O = ROOT / "OWNER_PG328_W11_ADOPTION_438_TESTONLY.json"
W0 = ROOT / "W11_WITNESS_449_TESTONLY.json"
T0 = ROOT / "W11_LIFECYCLE_TRACE_438.json"
TRACE = ROOT / "W11_LIFECYCLE_TRACE_456.json"
WITNESS = ROOT / "W11_WITNESS_456_TESTONLY.json"
VALIDATION = ROOT / "BUILD_VALIDATION_456.json"
README = ROOT / "README_WITNESS_456.md"
BUILDER = ROOT / "BUILD_W11_WITNESS_456.py"
VERIFIER = ROOT / "VERIFY_W11_WITNESS_456.py"
MANIFEST = ROOT / "MANIFEST_456.json"
ARCHIVE = ROOT / "DD_Fortress_W11_Witness_456_TESTONLY.zip"
DELIVERY = ROOT / "DELIVERY_456.json"

def canon(x): return json.dumps(x, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
def sha_bytes(x): return hashlib.sha256(x).hexdigest()
def sha(p): return sha_bytes(p.read_bytes())
def load(p): return json.loads(p.read_text(encoding="utf-8"))
def dump(p, x): p.write_text(json.dumps(x, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")

def main():
    proposal, adoption, oldw, trace, parent = load(P), load(O), load(W0), load(T0), load(BASE)
    closure = proposal["closure"]
    s030 = parent["stateSnapshots"]["S030"]
    s030_hash = sha_bytes(canon(s030))

    # W449-C02: the acquired cargo occupies B's right hand; inherited focus-B remains left.
    trace["actions"][1]["actionUse"] = "one Secure Cargo lift Action; right hand holds cargo-B and left hand remains occupied by focus-B"
    trace["actions"][1]["handsBefore"] = {"left": "focus-B", "right": "free"}
    trace["actions"][1]["handsAfter"] = {"left": "focus-B", "right": "cargo-B"}

    # W449-C03: concentration begins at commit 96.1; perception still begins at 96.3.
    trace["events"][19]["concentrationDeadline"] = 696.1
    trace["events"][19]["concentrationStartsAt"] = 96.1
    trace["events"][19]["auraPerceptionBeginsAt"] = 96.3

    # W449-C04: record the adopted 36.0 custody transfer with before/after values.
    action = trace["actions"][6]
    action["cargoTransfer"] = {
        "itemId": "cargo-A", "time": 36.0, "action": "Secure Cargo attach/transfer",
        "before": {"owner": "A", "custodian": "A", "bounds": {"x": [34, 35], "y": [6, 7], "z": [3, 4]}, "AWeightLb": 12, "ALoad": 1.2, "hands": {"left": "focus-A", "right": "cargo-A"}},
        "after": {"owner": "A", "custodian": "PG328-W11-R1:greater-fire-pet-1", "bounds": {"x": [39, 40], "y": [6, 7], "z": [3, 4]}, "AWeightLb": 2, "ALoad": 0.2, "petCombinedWeightLb": 110, "petLoad": 1, "petCapacityLb": 210, "petCapacityLoad": 14, "hands": {"left": "focus-A", "right": "free"}},
        "endpointBodyBounds": {"x": [33, 38], "y": [6, 11], "z": [0, 6]}, "minimumBodyCargoGapFeet": 1, "positiveVolumeOverlap": False
    }
    expiry = trace["events"][15]
    expiry.update({
        "cargoItemId": "cargo-A",
        "cargoBefore": {"owner": "A", "custodian": "PG328-W11-R1:greater-fire-pet-1", "bounds": {"x": [39, 40], "y": [6, 7], "z": [3, 4]}},
        "cargoAfter": {"owner": "A", "custodian": None, "bounds": {"x": [39, 40], "y": [6, 7], "z": [0, 1]}, "support": "branch-only Fortress z=0 floor patch [39,40]x[6,7]"},
        "fallResult": {"distanceFeet": 3, "damage": 0, "itemIdentityPreserved": True, "massLb": 10, "load": 1, "quantity": 1, "basis": "adopted narrow TEST_ONLY outcome for this exact cargo-A fall only"},
        "expiredPetReturnedAsBody": False, "expiredPetLootCreated": False
    })

    # W449-C04: append actual Q27 terminal events after the successful 102.3 Dispel.
    placements = {x["actor"]: x for x in closure["bodyPlacements"]}
    event_additions = [
        {"time": 102.3, "type": "Q27_FORTRESS_TERMINATION", "substep": 1,
         "before": {"rootActive": True, "spaceExists": True}, "after": {"rootActive": False, "spaceExists": False},
         "cause": "successful adopted rank-9 Dispel; event 23 roll 23 vs DC19", "campaignEventAsserted": False},
    ]
    for substep, actor_id, before_pos in [(2, "A", [25, 10, 0]), (3, "B", [35, 20, 0]), (4, "actor-w11-firepet-owner", [25, 20, 0])]:
        place = placements[actor_id]
        event = {"time": 102.3, "type": "Q27_BODY_RETURN", "substep": substep, "actor": actor_id,
                 "before": {"plane": "Fortress space", "position": before_pos},
                 "after": {"plane": "fixture:origin", "position": place["originPlacement"], "bounds": place["bounds"], "support": "adopted Q27 origin ground placement"},
                 "placementRule": "Proposal438 closure; body order A, B, Mage", "positiveVolumeOverlap": False}
        if actor_id == "B":
            event["carriedItemsBeforeAndAfter"] = [{"id": "cargo-B", "owner": "B", "custodian": "B", "boundsAtReturn": placements["B"]["carriedItems"][0]["boundsAtReturn"], "custodyChanged": False}]
        if actor_id == "actor-w11-firepet-owner": event["expiredPetReturnedAsBody"] = False
        event_additions.append(event)
    for substep, item in [(5, closure["looseItemsStableIdOrder"][0]), (6, closure["looseItemsStableIdOrder"][1])]:
        before, after = item["currentLooseBounds"], item["fixtureOriginPlacement"]
        event_additions.append({"time": 102.3, "type": "Q27_LOOSE_ITEM_SETTLEMENT", "substep": substep,
            "itemId": item["id"], "before": {"plane": "Fortress space", "bounds": before, "owner": item["owner"], "custodian": item["custodian"]},
            "after": {"plane": "fixture:origin", "bounds": after, "support": item["support"], "owner": item["owner"], "custodian": item["custodian"]},
            "projectionDelta": item["projectionDelta"], "evaluatedAtClosureStart": True,
            "expiryPreserved": item.get("expiry")})
    trace["events"].extend(event_additions)
    trace["closureResults"] = {"time": 102.3, "substeps": [x["type"] for x in event_additions],
        "bodyOrder": ["A", "B", "actor-w11-firepet-owner"],
        "looseItemOrder": [x["id"] for x in closure["looseItemsStableIdOrder"]],
        "tileDeadline": 3606.13, "expiredPetReturnedAsBody": False, "campaignOccurrenceAsserted": False}
    trace["id"] = "PG328-W11-LIFECYCLE-TRACE-456"
    trace["classification"] = "OWNER_ADOPTED_TEST_ONLY_LIFECYCLE_TRACE_WITH_Q27_RESULTS"
    trace["status"] = "TEST_ONLY_UNSEALED_PENDING_DIRECTOR_REVIEW"
    trace["branchId"] = "PG328-W11-R1"
    trace["parent"].update({"replaySha256": sha(BASE), "snapshotSha256": s030_hash, "sha256": sha(BASE)})
    trace["boundary"]["witnessConstructed"] = True

    witness = copy.deepcopy(oldw)
    witness["id"] = "PG328-W11-LIFECYCLE-WITNESS-456"
    witness["witnessId"] = witness["id"]
    witness["status"] = "READY_FOR_DIRECTOR_REVIEW"
    witness["supersedesWitness"] = {"path": "director-spell-review-129/fortress_w11_cargo_owner_proposal_438/W11_WITNESS_449_TESTONLY.json", "sha256": sha(W0)}
    witness["parent"].update({"replaySha256": sha(BASE), "snapshotSha256": s030_hash, "s030SnapshotSha256": s030_hash})
    witness["trace"].update({"path": "director-spell-review-129/fortress_w11_cargo_owner_proposal_438/W11_LIFECYCLE_TRACE_456.json",
        "classification": trace["classification"], "eventCount": len(trace["events"]), "eventSha256": sha_bytes(canon(trace["events"])),
        "turnMarkerCount": len(trace["turnMarkers"]), "actionCount": len(trace["actions"]), "petPhaseCount": len(trace["petPhases"]),
        "adoptedBranchId": "PG328-W11-R1", "sourceTraceBranchId": "PG328-W11-R1-PROPOSED"})
    witness["trace"]["sha256"] = sha_bytes(canon(trace))
    witness["correctionDisposition"] = {f"W449-C0{i}": "RESOLVED" for i in range(1, 5)}
    witness["trace"]["actions"] = copy.deepcopy(trace["actions"])
    witness["trace"]["events"] = copy.deepcopy(trace["events"])
    witness["trace"]["turnMarkers"] = copy.deepcopy(trace["turnMarkers"])
    witness["trace"]["petPhases"] = copy.deepcopy(trace["petPhases"])

    dump(TRACE, trace)
    # Bind the embedded trace hash to the exact on-disk JSON bytes, not canonical JSON.
    witness["trace"]["sha256"] = sha(TRACE)
    dump(WITNESS, witness)

    checks = {
        "proposal and adoption unchanged": sha(P) == "44c150647453fb762aec288fc83ce2afe0a77c160ca810682919d320078ae3de" and adoption["scope"]["proposalSha256"] == sha(P),
        "parent whole-file and S030 hashes separated": witness["parent"]["replaySha256"] == sha(BASE) and witness["parent"]["snapshotSha256"] == s030_hash == witness["parent"]["s030SnapshotSha256"],
        "B hands match adopted cargo custody": "left hand remains occupied by focus-B" in trace["actions"][1]["actionUse"] and trace["actions"][1]["handsAfter"] == {"left": "focus-B", "right": "cargo-B"},
        "Sight deadline starts at commit": trace["events"][19]["time"] == 96.3 and trace["events"][19]["concentrationStartsAt"] == 96.1 and trace["events"][19]["concentrationDeadline"] == 696.1 and trace["events"][19]["auraPerceptionBeginsAt"] == 96.3,
        "cargo transfer at 36.0 records before and after custody": action["cargoTransfer"]["before"]["custodian"] == "A" and action["cargoTransfer"]["after"]["custodian"] == "PG328-W11-R1:greater-fire-pet-1" and action["cargoTransfer"]["after"]["owner"] == "A",
        "expiry at 94.3 records supported zero-damage fall": expiry["cargoFallsFeet"] == 3 and expiry["cargoAfter"]["custodian"] is None and expiry["fallResult"]["damage"] == 0 and bool(expiry["cargoAfter"]["support"]),
        "Q27 closes root, A/B/Mage, then stable-ID items": [x["type"] for x in event_additions] == ["Q27_FORTRESS_TERMINATION", "Q27_BODY_RETURN", "Q27_BODY_RETURN", "Q27_BODY_RETURN", "Q27_LOOSE_ITEM_SETTLEMENT", "Q27_LOOSE_ITEM_SETTLEMENT"] and [x["itemId"] for x in event_additions if x["type"] == "Q27_LOOSE_ITEM_SETTLEMENT"] == [x["id"] for x in closure["looseItemsStableIdOrder"]],
        "tile expiry and pet exclusion preserved": trace["closureResults"]["tileDeadline"] == 3606.13 and trace["closureResults"]["expiredPetReturnedAsBody"] is False,
        "TEST_ONLY boundary and queue unchanged": witness["terminalAndQueueBoundary"]["queue"] == "830 applied / 18 pending / 0 accepted-unapplied" and all(witness["terminalAndQueueBoundary"][x] is False for x in ("sealPresent", "FortressAcceptedOrApplied", "spellIdentityAcceptedOrApplied", "canonicalRuleChanged", "historicalParentMutated", "campaignEventsAsserted", "queueChanged")),
        "trace and witness hashes bind": witness["trace"]["sha256"] == sha(TRACE) and witness["trace"]["eventCount"] == len(trace["events"]),
    }
    validation = {"id": "PG328-W11-BUILD-VALIDATION-456", "classification": "TEST_ONLY_WITNESS_BUILD_VALIDATION", "status": "PASS" if all(checks.values()) else "FAIL", "witnessPath": WITNESS.name, "witnessSha256": sha(WITNESS), "tracePath": TRACE.name, "traceSha256": sha(TRACE), "checks": checks, "passed": sum(checks.values()), "failed": sum(not x for x in checks.values()), "boundary": "Hypothetical W11-R1 only; no campaign, seal, identity acceptance/application, canon, parent, or queue mutation."}
    dump(VALIDATION, validation)
    if not all(checks.values()): raise SystemExit("Build validation failed")
    README.write_text("# W11 reversible lifecycle corrections 456\n\nThis owner-adopted TEST_ONLY successor preserves Proposal438 and its adoption bytes. It corrects W449-C01–C04: the S030 snapshot hash is distinguished from the W01 replay-file hash; B's hands remain focus-B left and cargo-B right; Arcane Sight starts its 600-second concentration at commit 96.1 (deadline 696.1) while perception begins at 96.3; and actual cargo custody at 36.0, pet expiry/fall at 94.3, and ordered Q27 root/body/item settlement at 102.3 are recorded.\n\nThe trace keeps the exact 74 regular turn markers, 10 actions and 10 finite pet phases. It describes one hypothetical branch and does not claim an invertible state-patch chain.\n\nNo campaign event, seal, Fortress identity acceptance/application, canon change, parent mutation, or queue mutation is asserted. Authority remains 830/18/0 and Fortress remains held under PG200-B06.\n", encoding="utf-8", newline="\n")
    package=[BUILDER,VERIFIER,P,O,ROOT.parent/"DIRECTOR_READBACK_454.json",TRACE,WITNESS,VALIDATION,README]
    manifest={"id":"PG328-W11-MANIFEST-456","classification":"TEST_ONLY_DIRECTOR_REVIEW_PACKAGE","files":[{"path":p.name if p.parent==ROOT else p.name,"bytes":p.stat().st_size,"sha256":sha(p)} for p in package]}
    dump(MANIFEST,manifest); package.append(MANIFEST)
    with zipfile.ZipFile(ARCHIVE,"w",compression=zipfile.ZIP_DEFLATED) as z:
        for p in package: z.write(p,arcname=p.name)
    dump(DELIVERY,{"id":"PG328-W11-DELIVERY-456","classification":"TEST_ONLY_UNSEALED_PENDING_DIRECTOR_REVIEW","witnessPath":WITNESS.name,"witnessBytes":WITNESS.stat().st_size,"witnessSha256":sha(WITNESS),"traceSha256":sha(TRACE),"validationSha256":sha(VALIDATION),"manifestSha256":sha(MANIFEST),"archivePath":ARCHIVE.name,"archiveBytes":ARCHIVE.stat().st_size,"archiveSha256":sha(ARCHIVE),"queue":{"reviewedApplied":830,"pending":18,"acceptedUnapplied":0,"changed":False},"directorReviewRequested":True})
    print(json.dumps({"status": validation["status"], "passed": validation["passed"], "failed": validation["failed"], "events": len(trace["events"]), "witnessSha256": sha(WITNESS), "traceSha256": sha(TRACE)}, indent=2))

if __name__ == "__main__": main()
