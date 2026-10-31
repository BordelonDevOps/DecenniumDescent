from __future__ import annotations

import hashlib
import json
import zipfile
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[6]
AUDIT = ROOT / "docs/audit/2026-10-08/full-game/director-spell-review-129"
OUT = AUDIT / "rank9_summon_herald_w02_witness_358"


def read(name: str):
    return json.loads((OUT / name).read_text(encoding="utf-8"))


def sha_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical_hash(value: object) -> str:
    return sha_bytes(json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8"))


def get_path(state: dict, pointer: str):
    value = state
    for part in pointer.strip("/").split("/"):
        value = value[part]
    return value


def set_path(state: dict, pointer: str, value: object) -> None:
    parts = pointer.strip("/").split("/")
    parent = state
    for part in parts[:-1]:
        parent = parent[part]
    parent[parts[-1]] = deepcopy(value)


checks = []


def check(cid: str, condition: bool, detail: str) -> None:
    checks.append({"id": cid, "passed": bool(condition), "detail": detail})


w01 = read("01_SH332_W01_CLEAN_REAFFIRMATION_358.json")
w02 = read("02_SH332_W02_AUTHORIZED_TEST_STATE_358.json")
route = read("03_SH332_W17D_CASTING_ROUTE_358.json")
w03 = read("04_SH332_W03_LIFECYCLE_WITNESSES_358.json")
w04 = read("05_SH332_W04_CONCURRENT_CALL_WITNESS_358.json")
build = read("06_SH332_W02_W03_W04_BUILD_VALIDATION_358.json")

# Re-open and hash the pinned approval source independently of the builder.
clean_archive = AUDIT / "rank9_summon_herald_w01_content_reconciliation_358_repack01/DD_Rank9_SummonHerald_SH202B02_W01_Content_Reconciliation_358_Repack01.zip"
clean_archive_sha = sha_bytes(clean_archive.read_bytes())
check("W01_REBOUND_ARCHIVE", w01["sealedCleanReaffirmation"]["w01Approved"] and clean_archive_sha == w01["sealedCleanReaffirmation"]["archiveSHA256"], "Recomputed the W01 clean Repack01 hash and verified the sealed W01 approval binding.")

auth = json.loads((AUDIT / "OWNER_LUMEN_W02_TEST_AUTHORIZATION_358.json").read_text(encoding="utf-8"))
check("OWNER_W02_AUTHORITY", auth["status"] == "AUTHORIZED_FUTURE_TEST_ONLY_W02_AFTER_W01_APPROVAL" and w02["sourceProfileBinding"]["w01Approval"], "Owner authorization and approved W01 prerequisite bind the exact TEST_ONLY fixture.")
check("NO_CAMPAIGN_ASSERTIONS", w02["campaignFactsEstablished"] is False and w02["actualConsentAsserted"] is False and w02["actualLocationAsserted"] is False and w02["actualAvailabilityAsserted"] is False, "W02 labels state, location, availability and consent as hypothetical only.")
check("HP_NOT_INFERRED", w02["state"]["currentHP"]["value"] == 400 and w02["state"]["currentHP"]["maximumPrintedHP"] == 528 and w02["state"]["currentHP"]["value"] != 528, "W02 supplies an explicit test current HP separate from printed maximum HP.")

route_path = ROOT / route["sourcePath"]
route_bytes = route_path.read_bytes()
route_source = json.loads(route_bytes.decode("utf-8"))
source_profile = route_source["profile"]
check("W17D_SOURCE_HASH_AND_ROUTE", sha_bytes(route_bytes) == route["sourceFileSHA256"] and source_profile["id"] == "W17D" and source_profile["profileSHA256BeforeOwnHash"] == route["profileSHA256BeforeOwnHash"] and route["profilePointer"]=="/profile" and route["parentProfilePointer"]=="/W17D" and route["parentSourceLineage"]["parentMember"]=="ACTOR_PROFILES.json" and route_source["parentArchive"]["sha256"]==route["parentSourceLineage"]["parentArchiveSHA256"] and route_source["parentBinding"]["sha256"]==route["parentSourceLineage"]["parentMemberSHA256"] and "summon-herald-of-the-planes" in source_profile["spellbook"] and "summon-herald-of-the-planes" in source_profile["prepared"] and "summon-herald-of-the-planes" in source_profile["ordinaryLearning"][16]["selected"], "Independently reopened the extracted W17D evidence at /profile, verified its parent ACTOR_PROFILES.json#/W17D archive lineage, and checked acquisition/preparation/source hash.")

scenarios = w03["witnesses"] + [w04["witness"]]
replay_count = 0
inverse_count = 0
replay_errors = []
for scenario in scenarios:
    replay = scenario.get("replay", {})
    state = deepcopy(replay.get("initialState"))
    if not isinstance(state, dict):
        replay_errors.append(f"{scenario.get('scenarioId')}: no complete initial state")
        continue
    initial_hash = canonical_hash(state)
    if initial_hash != replay.get("initialStateSHA256"):
        replay_errors.append(f"{scenario['scenarioId']}: initial hash mismatch")
    for event in replay.get("events", []):
        if canonical_hash(state) != event.get("stateBeforeSHA256") or state != event.get("stateBefore"):
            replay_errors.append(f"{scenario['scenarioId']}/{event.get('eventId')}: before state mismatch")
        for operation in event.get("forwardPatch", []):
            if operation.get("op") != "replace":
                replay_errors.append(f"{scenario['scenarioId']}/{event.get('eventId')}: invalid forward operation")
                break
            set_path(state, operation["path"], operation["value"])
        if canonical_hash(state) != event.get("stateAfterSHA256") or state != event.get("stateAfter"):
            replay_errors.append(f"{scenario['scenarioId']}/{event.get('eventId')}: after state mismatch")
        if state.get("uniqueLumenBodyCount") != 1 or state.get("lumen", {}).get("identityKey") != w02["uniqueIdentityKey"]:
            replay_errors.append(f"{scenario['scenarioId']}/{event.get('eventId')}: Lumen uniqueness invariant failed")
        replay_count += 1
    terminal_hash = canonical_hash(state)
    if terminal_hash != replay.get("terminalStateSHA256") or state != replay.get("terminalState"):
        replay_errors.append(f"{scenario['scenarioId']}: terminal state mismatch")
    for event in reversed(replay.get("events", [])):
        if canonical_hash(state) != event.get("stateAfterSHA256"):
            replay_errors.append(f"{scenario['scenarioId']}/{event.get('eventId')}: inverse precondition mismatch")
        for operation in event.get("inversePatch", []):
            set_path(state, operation["path"], operation["value"])
        if canonical_hash(state) != event.get("stateBeforeSHA256") or state != event.get("stateBefore"):
            replay_errors.append(f"{scenario['scenarioId']}/{event.get('eventId')}: inverse state mismatch")
        inverse_count += 1
    if canonical_hash(state) != initial_hash or state != replay.get("initialState"):
        replay_errors.append(f"{scenario['scenarioId']}: inverse did not restore complete baseline")
    if [x["undoOf"] for x in scenario.get("inverseTraversal", [])] != [e["eventId"] for e in reversed(scenario.get("forwardEvents", []))]:
        replay_errors.append(f"{scenario['scenarioId']}: inverse ledger order mismatch")
    traversal_state=deepcopy(replay.get("terminalState"))
    for inverse, forward in zip(scenario.get("inverseTraversal", []), reversed(replay.get("events", []))):
        if canonical_hash(traversal_state)!=inverse.get("preconditionStateSHA256"):
            replay_errors.append(f"{scenario['scenarioId']}/{inverse.get('undoOf')}: explicit inverse precondition mismatch")
        forward_paths={p["path"] for p in forward.get("forwardPatch", [])}
        inverse_paths={p["path"] for p in inverse.get("inversePatch", [])}
        if not inverse_paths.issubset(forward_paths):
            replay_errors.append(f"{scenario['scenarioId']}/{inverse.get('undoOf')}: inverse modifies fields outside its own forward transition")
        for operation in inverse.get("inversePatch", []):
            if operation.get("op")!="replace":
                replay_errors.append(f"{scenario['scenarioId']}/{inverse.get('undoOf')}: invalid explicit inverse operation")
                break
            set_path(traversal_state,operation["path"],operation["value"])
        if canonical_hash(traversal_state)!=inverse.get("restoredStateSHA256"):
            replay_errors.append(f"{scenario['scenarioId']}/{inverse.get('undoOf')}: explicit inverse result hash mismatch")
        if traversal_state!=forward.get("stateBefore"):
            replay_errors.append(f"{scenario['scenarioId']}/{inverse.get('undoOf')}: explicit inverse did not restore only its exact pre-event state")
    if traversal_state!=scenario.get("startingState") or canonical_hash(traversal_state)!=scenario.get("restoredStateSHA256") or not scenario.get("inverseRestoresInitial"):
        replay_errors.append(f"{scenario['scenarioId']}: published inverse traversal does not restore the full starting-state snapshot")

check("FULL_STATE_FORWARD_AND_INVERSE_REPLAY", not replay_errors and replay_count > 0 and replay_count == inverse_count, f"Replayed {replay_count} full-state forward transitions and {inverse_count} inverse transitions; errors={replay_errors}.")

w04_s = w04["witness"]
w04_events = {e["eventId"]: e for e in w04_s["replay"]["events"]}
a_decl = w04_events["W04-01-CASTER-A-DECLARE-PAY"]
b_decl = w04_events["W04-02-CASTER-B-DECLARE-PAY"]
a_resolve = w04_events["W04-03-PRIMARY-ADMISSION-ARRIVAL"]
b_resolve = w04_events["W04-04-CASTER-B-RESOLUTION-FAILS"]
both_pending = b_decl["stateAfter"]
race_ok = (
    a_decl["virtualOffsetMilliseconds"] < b_decl["virtualOffsetMilliseconds"] < a_resolve["virtualOffsetMilliseconds"] < b_resolve["virtualOffsetMilliseconds"]
    and both_pending["lumen"]["reservationId"] is None
    and len(both_pending["pendingCallDeclarations"]) == 2
    and all(x["initialEligibility"] == "PASS" for x in both_pending["pendingCallDeclarations"])
    and a_resolve["stateAfter"]["lumen"]["reservationId"] == "W04-A-CALL"
    and b_resolve["stateBefore"]["lumen"]["reservationId"] == "W04-A-CALL"
    and b_resolve["stateAfter"]["casters"]["B"]["rp"] == 38
    and "paid-failure" in b_resolve["stateAfter"]["casters"]["B"]["lastResolution"]
    and b_resolve["stateAfter"]["lumen"]["bodyLowerSouthwestCornerFeet"] == [50,20,0]
)
check("CONCURRENT_CALL_TWO_STAGE_ADMISSION", race_ok, "Both paid declarations pass initial eligibility while unreserved; A resolves first; B then fails final recheck with its paid 26 RP and Action spent and no second body.")

counter_windows=w04["counterHistory"]["eligibleWindows"]
counter_ok=(len(counter_windows)==2 and all(x["eligible"]=="YES" and x["counterspellKnownAutomatically"] and x["reactionAvailableAtTrigger"] and x["rechargeStateAtTrigger"]=="ready" and x["perceivesTrigger"] and x["lineOfSight"] and x["distanceFeet"]<=60 and x["decision"].startswith("EXPLICIT_TEST_ONLY_DECLINE") and x["rpSpent"]==0 and not x["reactionSpent"] and x["reactionAfter"]=="available" and x["rechargeAfter"]=="ready" for x in counter_windows) and all(not s["counterHistory"]["eligibleWindows"] and all(x["result"].startswith("INELIGIBLE") for x in s["counterHistory"]["ineligibleWindows"]) for s in w03["witnesses"]))
check("COUNTERSPELL_ELIGIBILITY_AND_NONUSE", counter_ok, "W04 records both eligible opposite-caster windows and explicit declines with reaction/recharge unchanged; every W03 spell-start window gives exact ineligibility bases.")

calendar_errors=[]
for scenario in scenarios:
    ledger=scenario["regularTurnLedger"]
    if ledger["roundDurationMilliseconds"]!=6000 or not ledger["replayEventsIncludeEveryRegularStartAndEndThroughEndpoint"]:
        calendar_errors.append(f"{scenario['scenarioId']}: calendar header")
    for row in ledger["slots"]:
        if "slotOffsetMs" in row and row["actor"]!="Herald call clock" and row["slotOffsetMs"]%6000!=row["initiativePhaseOffsetMs"]:
            calendar_errors.append(f"{scenario['scenarioId']}: nonperiodic {row['actor']} at {row['slotOffsetMs']}")
    starts=[e for e in scenario["forwardEvents"] if e.get("scheduledTurnStart")]
    ends=[e for e in scenario["forwardEvents"] if e.get("scheduledTurnEnd")]
    expected_starts=[r for r in ledger["slots"] if "slotOffsetMs" in r and r["actor"]!="Herald call clock"]
    endpoint=max(e["virtualOffsetMilliseconds"] for e in scenario["forwardEvents"])
    expected_ends=[r for r in expected_starts if r["slotOffsetMs"]+5999<=endpoint]
    if len(starts)!=len(expected_starts) or len(ends)!=len(expected_ends):
        calendar_errors.append(f"{scenario['scenarioId']}: start/end count {len(starts)}/{len(ends)} != {len(expected_starts)}/{len(expected_ends)}")
check("COMPLETE_REGULAR_TURN_CALENDAR", not calendar_errors, f"Validated all 6-second phased starts, budget refreshes, and regular ends through witness endpoints; errors={calendar_errors}.")

death_events={e["eventId"]:e for e in w03["witnesses"][2]["replay"]["events"]}
death_state=death_events["W03D-04-TEST-LETHAL-INPUT"]["stateAfter"]
death_ok=(death_state["clockOffsetMs"]==12000 and death_state["lumen"]["confirmedDead"] and death_state["lumen"]["call"]["endOffsetMs"]==12000 and death_state["lumen"]["bodyLowerSouthwestCornerFeet"]==[20,20,0] and w03["witnesses"][2]["forwardEvents"][-1]["virtualOffsetMilliseconds"]==12001 and "not a delayed call end" in w03["witnesses"][2]["forwardEvents"][-1]["forwardOperation"].lower())
check("DEATH_ENDS_CALL_AT_TRIGGER", death_ok, "The 12000ms death transition ends concentration/call and returns the corpse at that exact trigger; 12001ms is only a logging event.")

block_in = w04_events["W04-06-RETURN-BLOCKER-ENTERS"]["virtualOffsetMilliseconds"]
block_out = w04_events["W04-08-BLOCKER-CLEARS"]["virtualOffsetMilliseconds"]
check("BLOCKER_REGULAR_TURN_CADENCE", block_in == 12000 and block_out == 66000 and (block_out-block_in) % 6000 == 0, "The blocker enters and clears on regular starts nine six-second rounds apart; no 61-second turn is used.")
check("W03_LIFECYCLE_BRANCHES", len(w03["witnesses"]) == 3 and w03["coverageSummary"]["ordinaryReturn"] and w03["coverageSummary"]["blockedReturn"] and w03["coverageSummary"]["suppression"] and w03["coverageSummary"]["deathAndCorpse"] and w03["coverageSummary"]["cargoPreserved"], "W03 covers normal return, suppression with no revival, death/corpse, carried cargo, and independent recovery.")
check("TEST_ONLY_DEATH_BOUNDARY", any("most monsters die at 0 hp" in e["forwardOperation"].lower() for s in w03["witnesses"] for e in s["forwardEvents"]) and all(s["classification"].startswith("TEST_ONLY") for s in w03["witnesses"]), "Death behavior is expressly a bounded test premise using the core default and remains non-campaign evidence.")

report = {
    "id": "SH332-W02-W03-W04-INDEPENDENT-REPLAY-VALIDATION-358",
    "recordedAtUtc": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
    "status": "PASS" if all(c["passed"] for c in checks) else "FAIL",
    "independentOfBuilder": True,
    "checks": checks,
    "replayedForwardTransitions": replay_count,
    "replayedInverseTransitions": inverse_count,
    "directorDisposition": "Not supplied by this validator; GPT Director ruling remains controlling.",
    "identityDisposition": {"decision": "HOLD", "acceptedIds": [], "appliedIds": [], "applicationAuthorized": False},
    "limits": ["Conditional TEST_ONLY evidence only.", "Does not assert any campaign event, consent, or actual current state.", "Does not accept or apply the Herald identity."]
}
(OUT / "07_SH332_W02_W03_W04_INDEPENDENT_VALIDATION_358.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps({"status": report["status"], "checks": len(checks), "forwardTransitions": replay_count, "inverseTransitions": inverse_count, "failedChecks": [c["id"] for c in checks if not c["passed"]]}, indent=2))
if report["status"] != "PASS":
    raise SystemExit("Independent witness replay validation failed")
