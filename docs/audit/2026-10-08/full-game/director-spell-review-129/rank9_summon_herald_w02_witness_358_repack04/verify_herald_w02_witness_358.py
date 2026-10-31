from __future__ import annotations

import hashlib
import json
import zipfile
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[6]
AUDIT = ROOT / "docs/audit/2026-10-08/full-game/director-spell-review-129"
OUT = AUDIT / "rank9_summon_herald_w02_witness_358_repack04"


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
ready_binding = read("08_READY_ACTION_RULE_BINDING_358.json")
revision = read("09_SH332_W02_W03_W04_REPACK04_CORRECTION_358.json")

# Re-open and hash the pinned approval source independently of the builder.
clean_archive = AUDIT / "rank9_summon_herald_w01_content_reconciliation_358_repack01/DD_Rank9_SummonHerald_SH202B02_W01_Content_Reconciliation_358_Repack01.zip"
clean_archive_sha = sha_bytes(clean_archive.read_bytes())
check("W01_REBOUND_ARCHIVE", w01["sealedCleanReaffirmation"]["w01Approved"] and clean_archive_sha == w01["sealedCleanReaffirmation"]["archiveSHA256"], "Recomputed the W01 clean Repack01 hash and verified the sealed W01 approval binding.")

auth = json.loads((AUDIT / "OWNER_LUMEN_W02_TEST_AUTHORIZATION_358.json").read_text(encoding="utf-8"))
check("OWNER_W02_AUTHORITY", auth["status"] == "AUTHORIZED_FUTURE_TEST_ONLY_W02_AFTER_W01_APPROVAL" and w02["sourceProfileBinding"]["w01Approval"], "Owner authorization and approved W01 prerequisite bind the exact TEST_ONLY fixture.")
ready_source_path=ROOT / ready_binding["sourcePath"]
ready_source_bytes=ready_source_path.read_bytes()
ready_lines=ready_source_bytes.decode("utf-8").splitlines()
ready_excerpt="\n".join(ready_lines[ready_binding["sourceLines"][0]-1:ready_binding["sourceLines"][1]])
check("READY_RULE_SOURCE_BOUND", sha_bytes(ready_source_bytes)==ready_binding["sourceSHA256"] and ready_excerpt==ready_binding["sourceExcerpt"] and revision["status"]=="READY_FOR_DIRECTOR_RECHECK" and "W01 fixes its temporary-call deadline at paid declaration/preparation+60000ms" in ready_binding["rulesApplied"]["targetAndClock"] and ready_binding["rulesApplied"]["targetAndClock"]==revision["sourceBinding"]["rulesApplied"]["targetAndClock"], "Independently reopened the exact Ready rule source text and verified its source hash, excerpt, W01-specific clock exception and correction-revision record.")
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
b_prep=w04_events["W04-01-CASTER-B-READY-PREPARE"]
a_decl=w04_events["W04-03-CASTER-A-DECLARE-PAY"]
b_counter_decline=w04_events["W04-04-COUNTERSPELL-B-DECLINES-A-CAST"]
b_release=w04_events["W04-05-CASTER-B-READY-RELEASE-RESERVES-LUMEN"]
a_resolve=w04_events["W04-06-CASTER-A-FINAL-ADMISSION-FAILS"]
preparation_state=b_prep["stateAfter"]
a_pending_state=a_decl["stateAfter"]
release_state=b_release["stateAfter"]
failed_state=a_resolve["stateAfter"]
forward_ids=[e["eventId"] for e in w04_s["forwardEvents"]]
sequence_ok=(
    b_prep["virtualOffsetMilliseconds"]==0
    and preparation_state["casters"]["B"]["turnState"]["action"]=="spent"
    and preparation_state["casters"]["B"]["concentrationAvailable"] is False
    and preparation_state["casters"]["B"]["readySpell"]["expiresAtNextOwnTurnStartMs"]==6000
    and preparation_state["lumen"]["reservationId"] is None
    and a_decl["virtualOffsetMilliseconds"]==1000
    and a_pending_state["casters"]["A"]["rp"]==38
    and a_pending_state["lumen"]["reservationId"] is None
    and len(a_pending_state["pendingCallDeclarations"])==1
    and len(a_pending_state["pendingReadySpellDeclarations"])==1
    and b_counter_decline["virtualOffsetMilliseconds"]==1000
    and b_release["virtualOffsetMilliseconds"]==1000
    and forward_ids.index("W04-03-CASTER-A-DECLARE-PAY")<forward_ids.index("W04-04-COUNTERSPELL-B-DECLINES-A-CAST")<forward_ids.index("W04-05-CASTER-B-READY-RELEASE-RESERVES-LUMEN")<forward_ids.index("W04-06-CASTER-A-FINAL-ADMISSION-FAILS")
    and release_state["casters"]["B"]["turnState"]["reaction"]=="spent"
    and release_state["casters"]["B"]["counterspell"]["reactionAvailable"] is False
    and release_state["lumen"]["reservationId"]=="W04-B-CALL"
    and release_state["lumen"]["call"]["startOffsetMs"]==1000
    and release_state["lumen"]["call"]["deadlineOffsetMs"]==60000
    and w04_events["W04-09-DEADLINE-BLOCKED-RETURN"]["virtualOffsetMilliseconds"]==60000
    and w04_events["W04-09-DEADLINE-BLOCKED-RETURN"]["stateAfter"]["lumen"]["call"]["endOffsetMs"]==60000
    and w04_s["paidCallDeclarations"][0]["effectDurationRemainingMsAtRelease"]==59000
    and failed_state["casters"]["A"]["rp"]==38
    and failed_state["casters"]["A"]["concentrationAvailable"] is True
    and failed_state["lumen"]["reservationId"]=="W04-B-CALL"
    and "paid-failure" in failed_state["casters"]["A"]["lastResolution"]
)
check("SOURCE_LEGAL_READY_COMPETITION", sequence_ok, "B pays/casts with Ready on its earlier ordered turn, holds concentration to the trigger, and uses one Reaction release. The call manifests at 1000ms but honors W01's paid-preparation+60000ms deadline, ending at 60000ms with 59000ms active; A's later ordinary Action fails admission without a duplicate.")

counter_windows=w04["counterHistory"]["eligibleWindows"]
counter_ok=(len(counter_windows)==2 and all(x["eligible"]=="YES" and x["counterspellKnownAutomatically"] and x["reactionAvailableAtTrigger"] and x["rechargeStateAtTrigger"]=="ready" and x["perceivesTrigger"] and x["lineOfSight"] and x["distanceFeet"]<=60 and x["decision"].startswith("EXPLICIT_TEST_ONLY_DECLINE") and x["rpSpent"]==0 and not x["reactionSpent"] and x["reactionAfter"].startswith("available") and x["rechargeAfter"]=="ready" for x in counter_windows) and counter_windows[0]["windowTiming"].startswith("Ready spell preparation") and counter_windows[1]["windowTiming"].startswith("A's ordinary cast-start") and all(not s["counterHistory"]["eligibleWindows"] and all(x["result"].startswith("INELIGIBLE") for x in s["counterHistory"]["ineligibleWindows"]) for s in w03["witnesses"]))
check("COUNTERSPELL_ELIGIBILITY_AND_NONUSE", counter_ok, "W04 records the preparation-time Ready cast and A ordinary cast-start windows; both cost-free declines are distinct from B's later Reaction release. Ready release creates no second counter window; W03 bases remain exact.")

calendar_errors=[]
for scenario in scenarios:
    ledger=scenario["regularTurnLedger"]
    if ledger["roundDurationMilliseconds"]!=6000 or not ledger["replayEventsIncludeEveryRegularStartAndEndThroughEndpoint"] or not ledger.get("nonOverlappingOrderedSlots"):
        calendar_errors.append(f"{scenario['scenarioId']}: calendar header")
    slots=[r for r in ledger["slots"] if "slotOffsetMs" in r and r["actor"]!="Herald call clock"]
    if len({r["initiativePhaseOffsetMs"] for r in slots})!=len({r["actor"] for r in slots}):
        calendar_errors.append(f"{scenario['scenarioId']}: actor initiative phases are not unique")
    order_rank={actor:i for i,actor in enumerate(ledger["initiativeOrder"])}
    slots.sort(key=lambda r:(r["slotOffsetMs"],order_rank[r["actor"]]))
    for i,row in enumerate(slots):
        if row["slotOffsetMs"]%6000!=row["initiativePhaseOffsetMs"]:
            calendar_errors.append(f"{scenario['scenarioId']}: nonperiodic {row['actor']} at {row['slotOffsetMs']}")
        if i+1<len(slots):
            next_start=slots[i+1]["slotOffsetMs"]
        else:
            base=(row["slotOffsetMs"]//6000)*6000
            next_start=min((base+phase if base+phase>row["slotOffsetMs"] else base+phase+6000) for phase in {r["initiativePhaseOffsetMs"] for r in slots})
        if row.get("regularEndOffsetMs")!=next_start-1 or row.get("regularStartOffsetMs")!=row["slotOffsetMs"]:
            calendar_errors.append(f"{scenario['scenarioId']}: overlapping/wrong end for {row['actor']} at {row['slotOffsetMs']}")
    starts=[e for e in scenario["forwardEvents"] if e.get("scheduledTurnStart")]
    ends=[e for e in scenario["forwardEvents"] if e.get("scheduledTurnEnd")]
    expected_ends=[r for r in slots if r["regularEndOffsetMs"]<=max(e["virtualOffsetMilliseconds"] for e in scenario["forwardEvents"])]
    if len(starts)!=len(slots) or len(ends)!=len(expected_ends):
        calendar_errors.append(f"{scenario['scenarioId']}: start/end count {len(starts)}/{len(ends)} != {len(slots)}/{len(expected_ends)}")
    for event in starts:
        if event["scheduledTurnStart"].get("budgetRefresh")!={"Action":"ready","BonusAction":"ready","Reaction":"available","movementUsedFeet":0,"companionCommandSpent":False}:
            calendar_errors.append(f"{scenario['scenarioId']}: refresh not exact-once at {event['eventId']}")
    for end_event in ends:
        if end_event["scheduledTurnEnd"].get("regularEndOffsetMs")!=end_event["virtualOffsetMilliseconds"]:
            calendar_errors.append(f"{scenario['scenarioId']}: end marker mismatch at {end_event['eventId']}")
    if scenario is w04_s:
        deadline_i=next(i for i,e in enumerate(scenario["forwardEvents"]) if e["eventId"]=="W04-09-DEADLINE-BLOCKED-RETURN")
        a_start_i=next(i for i,e in enumerate(scenario["forwardEvents"]) if e.get("eventId")=="TURN-START-TEST_ONLY_W17D_CASTER_B-60000")
        if not deadline_i<a_start_i:
            calendar_errors.append("W04: absolute deadline did not resolve before equal-offset regular start")
check("COMPLETE_ORDERED_REGULAR_TURN_CALENDAR", not calendar_errors, f"Validated unique six-second phases, non-overlapping ordered slot boundaries, one exact refresh per start, and replayed all slot ends through each witness endpoint; errors={calendar_errors}.")

death_events={e["eventId"]:e for e in w03["witnesses"][2]["replay"]["events"]}
death_state=death_events["W03D-04-TEST-LETHAL-INPUT"]["stateAfter"]
death_ok=(death_state["clockOffsetMs"]==12000 and death_state["lumen"]["confirmedDead"] and death_state["lumen"]["call"]["endOffsetMs"]==12000 and death_state["lumen"]["bodyLowerSouthwestCornerFeet"]==[20,20,0] and w03["witnesses"][2]["forwardEvents"][-1]["virtualOffsetMilliseconds"]==12001 and "not a delayed call end" in w03["witnesses"][2]["forwardEvents"][-1]["forwardOperation"].lower())
check("DEATH_ENDS_CALL_AT_TRIGGER", death_ok, "The 12000ms death transition ends concentration/call and returns the corpse at that exact trigger; 12001ms is only a logging event.")

block_in = w04_events["W04-08-RETURN-BLOCKER-ENTERS"]["virtualOffsetMilliseconds"]
block_out = w04_events["W04-10-BLOCKER-CLEARS"]["virtualOffsetMilliseconds"]
check("BLOCKER_REGULAR_TURN_CADENCE", block_in == 16000 and block_out == 70000 and (block_out-block_in) % 6000 == 0 and block_in%6000==4000 and block_out%6000==4000, "The blocker enters and clears on its own phase-4000 regular slots nine six-second rounds apart.")
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
