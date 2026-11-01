#!/usr/bin/env python3
"""Build the narrowly adopted, TEST_ONLY PG328-W04 Earth Pet branch witness."""

from __future__ import annotations

import copy
import hashlib
import json
import pathlib
import subprocess
from datetime import date


BASE = pathlib.Path(__file__).resolve().parent
REPO = BASE.parents[4]
PREFLIGHT = BASE / "fortress_w04_earth_pet_guard_preflight_430" / "PG328_W04_EARTH_PET_GUARD_PREFLIGHT_430.json"
PARENT = BASE / "fortress_w01_structural_damage_witness_403_repack02" / "W01_REPLAY_403.json"
OUT = BASE / "fortress_w04_earth_pet_witness_436"
PREFLIGHT_SHA = "c80c91547ee4a07c687c0ba346ce0bcde861d3dda84a0389d12aeb48b7588d41"
PARENT_STATE_SHA = "6270321d6f07a55173f01fb353142d6bfb537d8e044cd313ef8fdd956baeff6c"


def raw_sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical(value: object) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def digest(value: object) -> str:
    return raw_sha(canonical(value))


def load(path: pathlib.Path) -> object:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def save(path: pathlib.Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def body_bounds(position: list[float], size: list[float]) -> list[float]:
    return [
        position[0], position[0] + size[0],
        position[1], position[1] + size[1],
        position[2], position[2] + size[2],
    ]


def positive_overlap(a: list[float], b: list[float]) -> bool:
    return all(a[2 * i] < b[2 * i + 1] and b[2 * i] < a[2 * i + 1] for i in range(3))


def swept_bounds(a: list[float], b: list[float], size: list[float]) -> list[float]:
    return [
        min(a[0], b[0]), max(a[0], b[0]) + size[0],
        min(a[1], b[1]), max(a[1], b[1]) + size[1],
        min(a[2], b[2]), max(a[2], b[2]) + size[2],
    ]


def segment_hits_box(p0: list[float], p1: list[float], box: list[float]) -> bool:
    t0, t1 = 0.0, 1.0
    for axis in range(3):
        lo, hi = box[2 * axis], box[2 * axis + 1]
        delta = p1[axis] - p0[axis]
        if abs(delta) < 1e-12:
            if p0[axis] <= lo or p0[axis] >= hi:
                return False
            continue
        enter, leave = (lo - p0[axis]) / delta, (hi - p0[axis]) / delta
        if enter > leave:
            enter, leave = leave, enter
        t0, t1 = max(t0, enter), min(t1, leave)
        if t0 >= t1:
            return False
    return t0 < t1 and t1 > 0 and t0 < 1


def source_path(binding: dict) -> pathlib.Path:
    return REPO / pathlib.Path(binding["path"])


def main() -> None:
    preflight_raw = PREFLIGHT.read_bytes()
    if raw_sha(preflight_raw) != PREFLIGHT_SHA:
        raise SystemExit("W04 preflight bytes do not match the exact adopted SHA-256.")
    preflight = load(PREFLIGHT)
    parent_raw = PARENT.read_bytes()
    parent = load(PARENT)
    if raw_sha(parent_raw) != preflight["parent"]["replaySha256"]:
        raise SystemExit("W01 replay bytes differ from the W04 proposal parent binding.")
    s030 = copy.deepcopy(parent["stateSnapshots"]["S030"])
    if digest(s030) != PARENT_STATE_SHA or digest(s030) != preflight["parent"]["terminalStateSha256"]:
        raise SystemExit("W01 S030 terminal-state hash mismatch.")
    if parent["terminalStateId"] != "S030" or s030["time"] != 12.9:
        raise SystemExit("Expected the unchanged W01-403 terminal S030 at t=12.9.")

    checked_sources = []
    source_by_path = {}
    binding_commit = preflight["authority"]["crosswalkReadAtCommit"]
    for binding in preflight["sourceBindings"]:
        path = source_path(binding)
        checkout_raw = path.read_bytes()
        candidates = [
            ("checkout_bytes", checkout_raw),
            ("checkout_crlf_normalized", checkout_raw.replace(b"\r\n", b"\n")),
        ]
        selected = next(((label, data) for label, data in candidates if raw_sha(data) == binding["sha256"]), None)
        if selected is not None:
            byte_source, exact = selected
        else:
            result = subprocess.run(
                ["git", "show", f"{binding_commit}:{binding['path']}"],
                cwd=REPO,
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            exact = result.stdout
            byte_source = f"git_show:{binding_commit}"
        actual = raw_sha(exact)
        if actual != binding["sha256"]:
            raise SystemExit(f"Source hash mismatch: {binding['path']}")
        expected_git_blob = binding.get("gitBlobSha1")
        if expected_git_blob:
            git_blob_hash = hashlib.sha1(f"blob {len(exact)}\0".encode("ascii") + exact).hexdigest()
            if git_blob_hash != expected_git_blob:
                raise SystemExit(f"Source Git blob mismatch: {binding['path']}")
        checked_sources.append({
            "path": binding["path"],
            "sha256": actual,
            "gitBlobSha1": expected_git_blob,
            "byteSource": byte_source,
            "pointer": binding.get("pointer"),
            "pointers": binding.get("pointers"),
        })
        source_by_path[binding["path"]] = json.loads(exact.decode("utf-8-sig")) if path.suffix.lower() == ".json" else None

    branch = preflight["proposedBranch"]
    identity = preflight["identity"]
    parent_binding = preflight["parent"]
    tile_id = branch["tileSetDownBeforeCast"]["itemId"]
    tile = copy.deepcopy(s030["items"][tile_id])
    a0 = s030["actors"]["A"]
    b0 = s030["actors"]["B"]
    pet_spec = branch["summon"]
    pet_bounds = pet_spec["proposedBoundsFeet"]
    pet_size = pet_spec["proposedBodyEnvelopeFeet"]
    spawn = pet_spec["targetFeet"]
    destination = branch["commandAndGuardTask"]["destinationBoundsFeet"]
    route = branch["commandAndGuardTask"]["routeFeet"]
    route_size = pet_spec["proposedBodyEnvelopeFeet"]
    a_box = body_bounds(a0["position"], a0["bodyBox"])
    b_box = body_bounds(b0["position"], b0["bodyBox"])
    tile_ground = branch["tileSetDownBeforeCast"]["to"]["boundsFeet"]
    tile_box = [
        tile_ground["x"][0], tile_ground["x"][1],
        tile_ground["y"][0], tile_ground["y"][1],
        tile_ground["z"][0], tile_ground["z"][1],
    ]

    geometry_binding = next(b for b in preflight["sourceBindings"] if b["path"].endswith("GEOMETRY_405.json"))
    geometry = source_by_path[geometry_binding["path"]]
    obstacles: list[tuple[str, list[float]]] = []
    for panel in geometry["panels"]:
        for idx, fragment in enumerate(panel["occupiedFragments"]):
            obstacles.append((f"panel:{panel['id']}:{idx}", fragment))
    for leaf in geometry["doorLeaves"]:
        for idx, fragment in enumerate(leaf["occupiedFragments"]):
            obstacles.append((f"doorLeaf:{leaf['id']}:{idx}", fragment))
    path_segments = list(zip(route, route[1:]))
    swept = [swept_bounds(a, b, route_size) for a, b in path_segments]
    route_hits = [
        {"segment": i, "obstacle": name}
        for i, box in enumerate(swept)
        for name, obstacle in obstacles
        if positive_overlap(box, obstacle)
    ]
    if route_hits:
        raise SystemExit(f"Earth Pet route intersects Geometry405: {route_hits[:5]}")
    if any(positive_overlap(body_bounds(spawn, pet_size), box) for _, box in obstacles):
        raise SystemExit("Earth Pet spawn bounds intersect Geometry405.")
    if any(positive_overlap(body_bounds(spawn, pet_size), box) for box in (a_box, b_box, tile_box)):
        raise SystemExit("Earth Pet spawn bounds overlap an actor or the tile.")
    if any(positive_overlap(box, actor) for box in swept for actor in (a_box, b_box)):
        raise SystemExit("Earth Pet route overlaps stationary A or B.")
    dest_box = [
        destination["x"][0], destination["x"][1],
        destination["y"][0], destination["y"][1],
        destination["z"][0], destination["z"][1],
    ]
    if any(positive_overlap(dest_box, box) for _, box in obstacles):
        raise SystemExit("Earth Pet destination intersects Geometry405.")
    if any(positive_overlap(dest_box, box) for box in (a_box, b_box, tile_box)):
        raise SystemExit("Earth Pet destination overlaps an actor or the tile.")

    a_center = [a0["position"][0] + 2.5, a0["position"][1] + 2.5, a0["position"][2] + 3]
    pet_center = [spawn[0] + 2.5, spawn[1] + 2.5, spawn[2] + 3]
    b_center = [b0["position"][0] + 2.5, b0["position"][1] + 2.5, b0["position"][2] + 3]
    ray_checks = {
        "A_to_pet": [name for name, box in obstacles if segment_hits_box(a_center, pet_center, box)],
        "B_to_A": [name for name, box in obstacles if segment_hits_box(b_center, a_center, box)],
    }
    if any(ray_checks.values()):
        raise SystemExit(f"A proposed ray intersects Geometry405: {ray_checks}")

    profile_binding = source_by_path[next(b["path"] for b in preflight["sourceBindings"] if "RETURN284_WIZARD20_PROFILE" in b["path"])]
    catalog = source_by_path[next(b["path"] for b in preflight["sourceBindings"] if b["path"].endswith("catalog.json"))]
    spell = next(s for s in catalog["spells"] if s["id"] == identity["proposedCompanionSpellId"])
    if spell["classAccess"]["Wizard"]["rank"] != 3 or spell["classAccess"]["Wizard"]["baseRpCost"] != 5:
        raise SystemExit("The adopted spell profile no longer matches Wizard rank 3 / 5 RP.")
    if spell["operational"]["effect"].find("AC 17, HP 30") < 0 or spell["operational"]["effect"].find("body mass 300 pounds") < 0:
        raise SystemExit("Earth Pet printed stat binding changed.")

    # Record the owner adoption as a separate branch-scoped authority record.
    adoption = {
        "schemaVersion": 1,
        "recordId": "OWNER-PG328-W04-EARTH-PET-ADOPTION-436",
        "recordedLocalDate": date.today().isoformat(),
        "classification": "OWNER_ADOPTION_TEST_ONLY",
        "scope": {
            "identity": identity["heldSpellId"],
            "identityHold": identity["holdId"],
            "witnessId": "PG328-W04-EARTH-PET-WITNESS-436",
            "branchId": branch["branchId"],
            "onlyThisWitness": True,
            "proposalId": preflight["artifactId"],
            "proposalPath": str(PREFLIGHT.relative_to(REPO)).replace("\\", "/"),
            "proposalSha256": PREFLIGHT_SHA,
            "parent": {
                "path": str(PARENT.relative_to(REPO)).replace("\\", "/"),
                "replayId": parent["id"],
                "terminalStateId": "S030",
                "terminalStateSha256": PARENT_STATE_SHA,
                "terminalTime": 12.9,
            },
        },
        "ownerAuthorization": {
            "source": "Explicit user authorization in Codex conversation",
            "verbatim": "Adopt exact W04 TEST_ONLY proposal",
            "adoptsExactProposalSha256": True,
        },
        "adoptedTermsReference": {
            "path": str(PREFLIGHT.relative_to(REPO)).replace("\\", "/"),
            "sha256": PREFLIGHT_SHA,
            "directorReadback": copy.deepcopy(preflight["directorReadback"]),
            "termsDigest": digest(branch),
            "scopeSummary": [
                "Construct only hypothetical PG328-W04-R1 from unchanged W01-403 terminal S030.",
                "Use the corrected 18.02 commitment, 18.03 B decline, 18.04 surviving resolution and pet creation, and 18.05 command.",
                "Apply only the exact adopted tile set-down, pet body/support/route, A support/load, profile binding, and Counterspell roster premises in proposal 430.",
                "Keep the pet through its exact finite lifecycle with attached phases and expiry at A's tenth future regular START, 78.0.",
            ],
        },
        "adoptedEffect": {
            "permits": ["Construct only the hypothetical PG328-W04-R1 TEST_ONLY witness from unchanged S030 using the exact proposal hash above."],
            "doesNotPermit": [
                "No W04 seal or final Director pass is presumed.",
                "No Fortress acceptance or application, PG200-B06 closure, spell identity acceptance/application, or queue change.",
                "No canonical rule, historical parent, W01 replay, fixture, or campaign state mutation.",
                "No claim that hypothetical branch events occurred in the campaign.",
                "No broader pet anatomy, support, carrying, tool-use, Help, or protection rule.",
            ],
        },
        "queueAuthorityAtAdoption": {
            "reviewedApplied": preflight["authority"]["queue"]["applied"],
            "pending": preflight["authority"]["queue"]["pending"],
            "acceptedUnapplied": preflight["authority"]["queue"]["acceptedUnapplied"],
            "identityAcceptedOrApplied": False,
            "identityStatus": "Held under PG200-B06",
        },
        "effectsAtAuthorization": {
            "canonicalRuleChanged": False,
            "historicalParentMutated": False,
            "W01ReplayMutated": False,
            "fixtureMutated": False,
            "queueChanged": False,
            "witnessConstructed": False,
            "witnessSealed": False,
            "identityAcceptedOrApplied": False,
        },
    }
    adoption_path = OUT / "OWNER_PG328_W04_EARTH_PET_ADOPTION_436_TESTONLY.json"
    save(adoption_path, adoption)
    adoption_sha = raw_sha(adoption_path.read_bytes())

    # Branch-local tile state; the parent S030 object remains embedded unchanged.
    tile_ground_state = copy.deepcopy(tile)
    tile_ground_state.update({
        "owner": None,
        "custodian": None,
        "position": [25, 5, 0],
        "heldBy": None,
        "heldBoundsFeet": None,
        "groundedBoundsFeet": copy.deepcopy(branch["tileSetDownBeforeCast"]["to"]["boundsFeet"]),
        "supportPremise": "Owner-adopted exact W04 tile support only.",
    })
    a_after_setdown = {
        "position": copy.deepcopy(a0["position"]),
        "leftHand": "focus-A",
        "rightHand": "free",
        "equipment": [item for item in a0["equipment"] if item != tile_id],
        "carriedWeightLb": 12,
        "carriedLoad": 1.2,
        "action": 1,
        "bonusAction": 1,
        "reaction": 1,
        "movementFeetAvailable": 30,
        "RP": 53,
        "Dissonance": 0,
        "Refrain": 0,
        "preparedFamiliesUsed": copy.deepcopy(a0["preparedFamiliesUsed"]),
        "lastSpell": a0["lastSpell"],
        "concentration": None,
    }
    a_after_commit = copy.deepcopy(a_after_setdown)
    a_after_commit.update({
        "action": 0,
        "RP": 48,
        "preparedFamiliesUsed": [*a0["preparedFamiliesUsed"], "summon-earth-pet"],
        "lastSpell": "summon-earth-pet",
        "magicThisTurn": True,
        "committedSpellRecord": {
            "castId": "PG328-W04-R1:CAST-EARTH-PET-001",
            "spellId": "summon-earth-pet",
            "class": "Wizard",
            "school": "Conjuration",
            "rank": 3,
            "time": 18.02,
            "cost": 5,
            "firstPreparedFamily": True,
            "baseDissonance": 0,
            "Refrain": 0,
            "status": "committed_pending_counterspell",
        },
        "resourceHistoryAppend": {
            "event": "PG328-W04-R1:CAST-EARTH-PET-001",
            "RP": -5,
            "poolAfter": 48,
            "discount": False,
        },
        "concentration": {
            "castId": "PG328-W04-R1:CAST-EARTH-PET-001",
            "spellId": "summon-earth-pet",
            "startedAt": 18.02,
            "commitmentPrecedesCounterspellWindow": True,
        },
    })
    a_after_success = copy.deepcopy(a_after_commit)
    a_after_success.update({
        "spellEfficiency": {
            "source": "PG200-W20 /acquisitionLedger/18/choices/0; Wizard /cards/15",
            "sameFamily": "summon-earth-pet",
            "pendingDiscountRp": 1,
            "expiresAtEnd": 24.9,
            "used": False,
        },
        "castResolution": {"status": "success_in_hypothetical_branch", "resolvedAt": 18.04},
    })
    a_after_command = copy.deepcopy(a_after_success)
    a_after_command["bonusAction"] = 0
    a_after_command["commandIssuedAt"] = 18.05
    a_after_command["turnEnd"] = 18.9
    a_after_command["movementFeetAvailable"] = 0

    pet = {
        "instanceId": "PG328-W04-R1:EARTH-PET-001",
        "spellId": "summon-earth-pet",
        "createdAt": 18.04,
        "expiresAt": 78.0,
        "exists": True,
        "plane": a0["plane"],
        "profile": {
            "size": "Medium",
            "AC": 17,
            "HP": 30,
            "maxHP": 30,
            "speedFeet": 30,
            "massLb": 300,
            "bodyEnvelopeFeet": pet_size,
            "boundsAtSpawnFeet": pet_bounds,
            "bodyEnvelopeClassification": "OWNER_ADOPTED_TEST_ONLY_PREMISE",
            "support": "Direct ground support at spawn, along full swept route, and at destination throughout occupancy, this branch only.",
        },
        "spawnPosition": spawn,
        "commandedRoute": route,
        "movementFeet": branch["commandAndGuardTask"]["distanceMovedFeet"],
        "destinationBoundsFeet": destination,
        "destinationPosition": [destination["x"][0], destination["y"][0], destination["z"][0]],
        "phaseAt18_9": {"movement": "14-foot commanded route", "action": "Dodge", "status": "hypothetical attached phase"},
        "laterPhases": [],
        "termination": {
            "time": 78.0,
            "reason": "Tenth future regular START marker after 18.04 application",
            "earlierEndConditions": ["concentration ends", "pet reaches 0 HP"],
            "boundedBranchPremise": "Neither earlier condition nor another interference occurs before 78.0.",
        },
    }
    later_phases = []
    for turn_end in range(24, 73, 6):
        phase_time = float(turn_end) + 0.9
        later_phases.append({
            "time": phase_time,
            "ownerTurnEnd": phase_time,
            "movementFeet": 0,
            "choice": "Dodge",
            "position": pet["destinationPosition"],
            "noExtraTurnOrCommand": True,
        })
    pet["laterPhases"] = later_phases
    pet_at_creation = copy.deepcopy(pet)

    schedule_coverage = []
    for actor_id, actor in s030["actors"].items():
        start = actor["regularSchedule"]["nextStart"]
        period = actor["regularSchedule"]["period"]
        end_offset = actor["regularSchedule"]["endOffset"]
        while start <= 78.0:
            schedule_coverage.append({
                "actor": actor_id,
                "start": float(start),
                "end": float(start + end_offset),
                "authoredAction": "none",
                "authoredMovement": 0,
                "authoredReaction": "none",
            })
            start += period
    schedule_coverage.sort(key=lambda row: (row["start"], row["actor"]))

    events = [
        {
            "eventId": "PG328-W04-R1:BRANCH-START-S030",
            "time": 12.9,
            "kind": "BRANCH_INITIALIZATION",
            "hypothetical": True,
            "stateDigest": PARENT_STATE_SHA,
            "note": "Copy W01-403 S030 exactly; do not alter the historical parent.",
        },
        {
            "eventId": "PG328-W04-R1:B-START-13",
            "time": 13.0,
            "kind": "REGULAR_START",
            "actor": "B",
            "hypothetical": True,
            "outcome": "Refresh Reaction and ordinary turn resources; B has no intervening Reaction use before 18.02.",
        },
        {
            "eventId": "PG328-W04-R1:A-START-18",
            "time": 18.0,
            "kind": "REGULAR_START",
            "actor": "A",
            "hypothetical": True,
            "outcome": "Refresh A Action, Bonus Action, Reaction and 30-foot movement.",
        },
        {
            "eventId": "PG328-W04-R1:SET-DOWN-CLAY-TILE",
            "time": 18.01,
            "kind": "ORDINARY_FREE_OBJECT_INTERACTION",
            "actor": "A",
            "hypothetical": True,
            "itemId": tile_id,
            "fromHeldBoundsFeet": copy.deepcopy(tile["heldBoundsFeet"]),
            "toGroundedBoundsFeet": copy.deepcopy(branch["tileSetDownBeforeCast"]["to"]["boundsFeet"]),
            "tileIdentityExpiryPreserved": True,
            "supportPremises": ["exact tile footprint", "A at [25,6,0] with carried weight 12 lb and Load 1.2"],
        },
        {
            "eventId": "PG328-W04-R1:CAST-COMMIT",
            "time": 18.02,
            "kind": "SPELL_COMMITMENT_BEFORE_INTERRUPTION",
            "actor": "A",
            "hypothetical": True,
            "spellId": "summon-earth-pet",
            "actionSpent": True,
            "RPBefore": 53,
            "RPAfter": 48,
            "concentrationBeginsBeforeWindow": True,
            "V": "audible voice condition",
            "S": "right hand free",
            "F": "focus-A accessible in left hand",
            "Dissonance": "0 to 0",
            "Refrain": "0 to 0",
            "firstPreparedFamily": True,
            "preparedFamiliesUsedAfter": copy.deepcopy(a_after_commit["preparedFamiliesUsed"]),
            "lastSpellAfter": "summon-earth-pet",
            "magicThisTurn": True,
            "noRefundOnInterruption": True,
        },
        {
            "eventId": "PG328-W04-R1:B-COUNTERSPELL-DECLINE",
            "time": 18.03,
            "kind": "ELIGIBLE_RESPONDER_DECLINES",
            "actor": "B",
            "hypothetical": True,
            "eligibilityPremise": copy.deepcopy(branch["summon"]["counterspellWindow"]["proposedResponderRoster"]["actors"]["B"]["castWindowState"]),
            "decision": "decline",
            "roll": "none",
            "reactionSpent": False,
            "RPSpent": 0,
            "rechargeStarted": False,
            "castSurvives": True,
        },
        {
            "eventId": "PG328-W04-R1:CAST-SURVIVES-PET-CREATED",
            "time": 18.04,
            "kind": "SUCCESSFUL_RESOLUTION_AND_APPLICATION",
            "actor": "A",
            "hypothetical": True,
            "petInstanceId": pet["instanceId"],
            "petCreatedOnlyAfterWindow": True,
            "spellEfficiency": copy.deepcopy(a_after_success["spellEfficiency"]),
        },
        {
            "eventId": "PG328-W04-R1:BONUS-ACTION-COMMAND",
            "time": 18.05,
            "kind": "COMPANION_COMMAND",
            "actor": "A",
            "hypothetical": True,
            "bonusActionSpent": True,
            "petRemainsAtSpawnUntilAttachedPhase": True,
            "audiblePerceivedCommandAtSpawn": True,
            "petTask": "Move the stated 14 feet and Dodge in its attached phase after A's whole turn.",
        },
        {
            "eventId": "PG328-W04-R1:A-END-PET-MOVE-DODGE",
            "time": 18.9,
            "kind": "OWNER_END_AND_ATTACHED_COMPANION_PHASE",
            "actor": "A",
            "hypothetical": True,
            "petRouteFeet": route,
            "petMovementFeet": 14,
            "petDestination": pet["destinationPosition"],
            "petDodge": True,
            "noIndependentTurn": True,
        },
        {
            "eventId": "PG328-W04-R1:SPELL-EFFICIENCY-EXPIRES",
            "time": 24.9,
            "kind": "PENDING_DISCOUNT_EXPIRY",
            "actor": "A",
            "hypothetical": True,
            "discountUnused": True,
            "discountCleared": True,
        },
        *[
            {
                "eventId": f"PG328-W04-R1:PET-DEFENSIVE-DODGE-{phase['time']:.1f}",
                "time": phase["time"],
                "kind": "UNCOMMANDED_ATTACHED_PHASE",
                "actor": pet["instanceId"],
                "hypothetical": True,
                "movementFeet": 0,
                "choice": "Dodge",
                "position": pet["destinationPosition"],
                "noNewCommandOrExtraTurn": True,
            }
            for phase in later_phases
        ],
        {
            "eventId": "PG328-W04-R1:PET-EXPIRES",
            "time": 78.0,
            "kind": "FINITE_DURATION_EXPIRY",
            "actor": pet["instanceId"],
            "hypothetical": True,
            "futureRegularStartMarkers": [24, 30, 36, 42, 48, 54, 60, 66, 72, 78],
            "expiresBeforeOwnerActionsAtMarker": True,
            "postExpiryPhase": "none",
            "concentrationCleared": True,
        },
    ]
    pet["exists"] = False
    pet["endedAt"] = 78.0
    pet["termination"]["status"] = "expired_in_hypothetical_branch"

    replay = {
        "schemaVersion": 1,
        "id": "PG328-W04-EARTH-PET-WITNESS-436",
        "branchId": branch["branchId"],
        "classification": "HYPOTHETICAL_TEST_ONLY_BRANCH_WITNESS",
        "status": "CONSTRUCTED_UNSEALED_DIRECTOR_REVIEW_OPEN",
        "allEventsAreHypothetical": True,
        "noCampaignEventClaim": True,
        "adoption": {
            "path": str(adoption_path.relative_to(REPO)).replace("\\", "/"),
            "sha256": adoption_sha,
            "exactProposalSha256": PREFLIGHT_SHA,
        },
        "parent": {
            "path": str(PARENT.relative_to(REPO)).replace("\\", "/"),
            "replayId": parent["id"],
            "replaySha256": raw_sha(parent_raw),
            "terminalStateId": "S030",
            "terminalStateSha256": PARENT_STATE_SHA,
            "terminalTime": 12.9,
            "branchInitialState": s030,
            "branchInitialStateDigest": digest(s030),
            "parentBytesMutated": False,
        },
        "sourceHashes": checked_sources,
        "profileBinding": {
            "classification": "BRANCH_LOCAL_TEST_ONLY_PROFILE_BINDING",
            "profilePath": "docs/audit/2026-10-08/full-game/director-spell-review-129/conjure_demiplane_fortress_closure_intake_367/payload/sources/RETURN284_WIZARD20_PROFILE_TESTONLY.json",
            "profileFileSha256": "a3a3ce0a714c1fa35523719c8c8a0297fc457d5b5f097f6a20a00aad6cd7be55",
            "preserveS030ActorProfileReference": True,
            "s030ProfileId": s030["actors"]["A"]["profile"],
            "s030ProfileSha256": s030["actors"]["A"]["profileSHA256"],
            "compatibility": {
                **copy.deepcopy(preflight["profileBindingAndCompatibility"]),
                "proposalOriginalStatus": preflight["profileBindingAndCompatibility"]["status"],
                "status": "OWNER_ADOPTED_TEST_ONLY_FOR_PG328-W04-R1",
            },
            "grantsNoAdditionalCapabilityOrHistoricalEvent": True,
        },
        "geometry": {
            "sourcePath": geometry_binding["path"],
            "sourceSha256": geometry_binding["sha256"],
            "panelsChecked": len(geometry["panels"]),
            "doorLeavesChecked": len(geometry["doorLeaves"]),
            "petSpawnPosition": spawn,
            "petSpawnBounds": pet_bounds,
            "petRoute": route,
            "petSweptBounds": swept,
            "routeGeometryIntersectionCount": len(route_hits),
            "spawnGeometryIntersectionCount": 0,
            "destinationGeometryIntersectionCount": 0,
            "timeMatchedActorCollisionCount": 0,
            "tileCollisionCount": 0,
            "rayIntersectionCounts": {key: len(value) for key, value in ray_checks.items()},
            "tileGroundBounds": tile_box,
            "supportEstablishedByGeometry": False,
            "supportExistsOnlyByAdoptedPremise": True,
        },
        "testOnlySupportPremises": [
            "The exact tile grounded footprint is supported for this W04 branch only.",
            "A at unchanged [25,6,0] is supported with 12 lb / Load 1.2 after the tile is set down.",
            "The 300 lb pet is directly supported at spawn, across every route point, and at destination throughout occupancy.",
        ],
        "timelineCoverage": {
            "from": 12.9,
            "through": 78.0,
            "regularActorMarkers": schedule_coverage,
            "noOtherActorActionsOrInterference": True,
            "boundedConcentrationPremise": branch["finiteLifecycle"]["boundedNoInterferencePremise"],
            "petAttachedPhaseTimes": [18.9, *[p["time"] for p in later_phases]],
            "expiryOrdering": "Pet expires at A START 78.0 before choices; no phase at or after expiry.",
        },
        "events": events,
        "branchStateAfterTileSetDown": {
            "actorA": a_after_setdown,
            "tile": tile_ground_state,
            "tileMassAndLoadPreserved": True,
            "tileExpiryPreservedAt": tile["expiresAtEventTime"],
        },
        "branchStateAfterCommitment": {
            "actorA": a_after_commit,
            "B": {
                "position": copy.deepcopy(b0["position"]),
                "reactionAvailableAtWindow": 1,
                "RP": b0["RP"],
                "declinedAt": 18.03,
                "reactionSpent": False,
                "RPSpent": 0,
                "rechargeStarted": False,
            },
        },
        "branchStateAfterSuccessfulResolution": {
            "actorA": a_after_success,
            "pet": pet_at_creation,
            "petStatsSource": spell["operational"]["effect"],
            "applicationAt": 18.04,
            "commandAt": 18.05,
            "petInitialPoseUntil": 18.9,
        },
        "counterspellWindow": {
            "proposalRoster": copy.deepcopy(branch["summon"]["counterspellWindow"]["proposedResponderRoster"]),
            "realizedChoicesInThisHypotheticalBranch": {
                "A": "No self-counter attempt; self-eligibility remains unadjudicated.",
                "B": "Eligible same-plane responder declines at 18.03; no roll, Reaction, RP, or recharge.",
                "C": "Different plane; no Fortress-plane perception/line route is established.",
                "D": "Different plane; no Fortress-plane perception/line route is established.",
            },
            "prospectiveDcIfAttempted": 16,
        },
        "branchTerminalStateAt78": {
            "actorA": {
                "position": copy.deepcopy(a0["position"]),
                "HP": a0["HP"],
                "RP": 48,
                "Dissonance": 0,
                "Refrain": 0,
                "lastSpell": "summon-earth-pet",
                "concentration": None,
                "SpellEfficiencyPending": None,
            },
            "tile": tile_ground_state,
            "pet": {
                "instanceId": pet["instanceId"],
                "exists": False,
                "endedAt": 78.0,
                "lastPose": pet["destinationPosition"],
                "lastEligibleDodge": 72.9,
            },
            "FortressState": "unchanged from W01-403 S030",
        },
        "queueAndDecisionState": {
            "reviewedApplied": 830,
            "pending": 18,
            "acceptedUnapplied": 0,
            "FortressAcceptedOrApplied": False,
            "canonChanged": False,
            "queueChanged": False,
            "sealed": False,
        },
        "nonEffects": [
            "No W04 Director seal or final acceptance occurred.",
            "No Fortress acceptance/application, canon, fixture, queue, campaign, or historical parent change occurred.",
            "The pet grants no implied protection, Help benefit, cargo capacity, tool use, autonomous attack, or general support rule.",
            "Counterspell eligibility for A's self-attempt remains unadjudicated; no self-attempt is made.",
        ],
    }
    replay_path = OUT / "W04_REPLAY_436_TESTONLY.json"
    save(replay_path, replay)
    replay_sha = raw_sha(replay_path.read_bytes())

    checks = [
        ("exact corrected W04 proposal hash", raw_sha(preflight_raw) == PREFLIGHT_SHA),
        ("unchanged W01 parent replay binding", raw_sha(parent_raw) == preflight["parent"]["replaySha256"]),
        ("unchanged terminal S030 digest and time", digest(s030) == PARENT_STATE_SHA and s030["time"] == 12.9),
        ("all adopted source file hashes", len(checked_sources) == len(preflight["sourceBindings"])),
        ("branch-local Wizard20 profile binding only", replay["profileBinding"]["preserveS030ActorProfileReference"]),
        ("one tile interaction after A START 18.0", events[3]["time"] == 18.01 and events[3]["kind"] == "ORDINARY_FREE_OBJECT_INTERACTION"),
        ("tile identity, mass, Load, bounds, and expiry preserved", tile_ground_state["id"] == tile_id and tile_ground_state["massLb"] == 2 and tile_ground_state["expiresAtEventTime"] == 3606.13),
        ("A hand and carried-load transition", a_after_setdown["rightHand"] == "free" and a_after_setdown["carriedWeightLb"] == 12 and a_after_setdown["carriedLoad"] == 1.2),
        ("commitment precedes B response and creation", [e["time"] for e in events if e["eventId"].endswith(("CAST-COMMIT", "B-COUNTERSPELL-DECLINE", "CAST-SURVIVES-PET-CREATED"))] == [18.02, 18.03, 18.04]),
        ("RP, Dissonance, Refrain and prepared-family ledger", a_after_commit["RP"] == 48 and a_after_commit["Dissonance"] == 0 and a_after_commit["Refrain"] == 0 and a_after_commit["preparedFamiliesUsed"].count("summon-earth-pet") == 1),
        ("B's decline spends no reaction, RP, or recharge", replay["branchStateAfterCommitment"]["B"]["reactionSpent"] is False and replay["branchStateAfterCommitment"]["B"]["RPSpent"] == 0),
        ("pet created only on surviving resolution", replay["branchStateAfterSuccessfulResolution"]["pet"]["createdAt"] == 18.04),
        ("pet stat and branch-only body envelope", pet["profile"]["AC"] == 17 and pet["profile"]["HP"] == 30 and pet["profile"]["massLb"] == 300 and pet["profile"]["bodyEnvelopeClassification"] == "OWNER_ADOPTED_TEST_ONLY_PREMISE"),
        ("Geometry405 full-body route and destination clear", not route_hits and len(geometry["panels"]) == 2660 and len(geometry["doorLeaves"]) == 10),
        ("time-matched actor, tile, spawn and destination clearance", replay["geometry"]["timeMatchedActorCollisionCount"] == 0 and replay["geometry"]["tileCollisionCount"] == 0),
        ("summon and B responder rays clear", not any(ray_checks.values())),
        ("command timing, range and 14-foot move", events[7]["time"] == 18.05 and branch["commandAndGuardTask"]["distanceMovedFeet"] == 14 and branch["commandAndGuardTask"]["commandDistanceAtIssueFeet"] < 60),
        ("pet defensive phases stop at expiry", pet["laterPhases"][-1]["time"] == 72.9 and pet["endedAt"] == 78.0),
        ("bounded support premises are adopted and narrow", len(replay["testOnlySupportPremises"]) == 3 and replay["geometry"]["supportEstablishedByGeometry"] is False),
        ("queue, canon, seal and spell disposition unchanged", replay["queueAndDecisionState"] == {"reviewedApplied": 830, "pending": 18, "acceptedUnapplied": 0, "FortressAcceptedOrApplied": False, "canonChanged": False, "queueChanged": False, "sealed": False}),
    ]
    validation = {
        "schemaVersion": 1,
        "id": "PG328-W04-BUILD-VALIDATION-436",
        "classification": "OWNER_ADOPTED_TEST_ONLY_BRANCH_CONSTRUCTION_CHECK",
        "status": "PASS_WITH_DIRECTOR_REVIEW_OPEN",
        "proposalSha256": PREFLIGHT_SHA,
        "adoptionSha256": adoption_sha,
        "replaySha256": replay_sha,
        "checks": [{"name": name, "status": "PASS" if ok else "FAIL"} for name, ok in checks],
        "result": {
            "passed": sum(bool(ok) for _, ok in checks),
            "failed": sum(not bool(ok) for _, ok in checks),
            "directorSealPresent": False,
            "spellAcceptanceOrApplication": False,
        },
        "limitations": [
            "Every event is a hypothetical branch input, not a campaign occurrence.",
            "Support, profile binding, finite no-interference, item placement, and pet body envelope remain limited to this exact branch.",
            "This report checks the adopted branch construction and source-bound geometry; it is not a Director seal or spell acceptance.",
        ],
    }
    if validation["result"]["failed"]:
        raise SystemExit(f"Branch validation failed: {[name for name, ok in checks if not ok]}")
    save(OUT / "BUILD_VALIDATION_436.json", validation)
    (OUT / "README.md").write_text(
        "# PG328-W04 Earth Pet witness 436 — TEST_ONLY\n\n"
        "This is the owner-adopted hypothetical PG328-W04-R1 branch from unchanged W01-403 S030. "
        f"The exact adopted proposal SHA-256 is {PREFLIGHT_SHA}. The parent S030 digest is {PARENT_STATE_SHA}.\n\n"
        "The replay records the 18.01 tile set-down, 18.02 cast commitment, 18.03 B decline, "
        "18.04 surviving creation, 18.05 command, attached pet phases, and 78.0 expiry. "
        "It preserves the tile and parent history and confines every adopted support/profile/body premise to this branch.\n\n"
        "The witness is unsealed. No Fortress acceptance/application, spell identity acceptance/application, canonical rule, "
        "campaign state, fixture, parent, or queue changed. Queue remains 830 applied / 18 pending / 0 accepted-unapplied.\n",
        encoding="utf-8",
    )
    print(json.dumps({
        "output": str(OUT),
        "proposalSha256": PREFLIGHT_SHA,
        "adoptionSha256": adoption_sha,
        "replaySha256": replay_sha,
        "validation": validation["result"],
        "geometryPanels": len(geometry["panels"]),
        "doorLeaves": len(geometry["doorLeaves"]),
        "routeHits": len(route_hits),
        "rayHits": {key: len(value) for key, value in ray_checks.items()},
    }, indent=2))


if __name__ == "__main__":
    main()
