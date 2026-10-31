from __future__ import annotations

import copy
import hashlib
import json
import math
import pathlib
import zipfile
import zlib


ROOT = pathlib.Path(__file__).resolve().parents[5]
AUDIT = ROOT / "docs/audit/2026-10-08/full-game/director-spell-review-129"
DELIVERY = AUDIT / "rank9_nullification_wave_closure355_repack01_delivery"
WITNESS_PATH = AUDIT / "NULLIFICATION_WAVE_CLOSURE_WITNESS_355_REPACK01.json"
RETURN247 = AUDIT / "rank9_materialforging2_return247_received/DD_Rank9_MaterialForging2_Director_Return247_HELD.zip"
RETURN281 = AUDIT / "rank9_wardcontrol6_return281_received/DD_Rank9_WardControl6_Director_Return281_HELD.zip"
SUPPLEMENT = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_candidates/eternalforge_reviewed_255/SUPPLEMENT255_W2.json"
QUEUE = AUDIT / "CURRENT_SPELL_QUEUE_356.json"
PENDING = AUDIT / "CURRENT22_PENDING_IDENTITY_AUDIT_356.json"
WIZARD_SOURCE = ROOT / "DescentReviewChanges/ReviewBible/data/public/class_playtests/wizard.json"
SPELL_CATALOG = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json"
CLASS_BINDINGS = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_playtests/class_spell_bindings.json"
TARGET = "nullification-wave"


def canonical(value: object) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def sha(value: object) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def raw_digest(raw: bytes) -> dict:
    return {"bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest(), "crc32": f"{zlib.crc32(raw) & 0xffffffff:08x}"}


def pointer(path: str) -> list[str]:
    if path == "":
        return []
    if not path.startswith("/"):
        raise AssertionError(f"bad JSON pointer {path}")
    return [part.replace("~1", "/").replace("~0", "~") for part in path[1:].split("/")]


def at(document: object, parts: list[str]) -> object:
    node = document
    for part in parts:
        node = node[int(part)] if isinstance(node, list) else node[part]
    return node


def parent(document: object, parts: list[str]) -> tuple[object, str]:
    node = document
    for part in parts[:-1]:
        node = node[int(part)] if isinstance(node, list) else node[part]
    return node, parts[-1]


def patch(document: object, operations: list[dict]) -> object:
    for change in operations:
        op, path = change["op"], change["path"]
        parts = pointer(path)
        if op == "test":
            assert at(document, parts) == change["value"], path
            continue
        if not parts:
            assert op == "replace"
            document = copy.deepcopy(change["value"])
            continue
        container, key = parent(document, parts)
        if op == "replace":
            if isinstance(container, list):
                container[int(key)] = copy.deepcopy(change["value"])
            else:
                container[key] = copy.deepcopy(change["value"])
        elif op == "add":
            if isinstance(container, list):
                container.insert(len(container) if key == "-" else int(key), copy.deepcopy(change["value"]))
            else:
                container[key] = copy.deepcopy(change["value"])
        elif op == "remove":
            if isinstance(container, list):
                container.pop(int(key))
            else:
                del container[key]
        else:
            raise AssertionError(f"unsupported operation {op}")
    return document


def segment_hits_box(start: list[float], end: list[float], box: list[list[float]]) -> bool:
    low, high = box
    t0, t1 = 0.0, 1.0
    for axis in range(3):
        delta = end[axis] - start[axis]
        if abs(delta) < 1e-12:
            if start[axis] < low[axis] or start[axis] > high[axis]:
                return False
            continue
        near = (low[axis] - start[axis]) / delta
        far = (high[axis] - start[axis]) / delta
        if near > far:
            near, far = far, near
        t0, t1 = max(t0, near), min(t1, far)
        if t0 > t1:
            return False
    return t1 >= 0 and t0 <= 1


def main() -> None:
    witness = json.loads(WITNESS_PATH.read_text(encoding="utf-8"))
    replay = json.loads((AUDIT / "NULLIFICATION_WAVE_FORGE_BRANCH_REPLAY_355.json").read_text(encoding="utf-8"))
    checks: list[dict] = []

    def record(label: str, passed: bool, detail: str) -> None:
        checks.append({"check": label, "passed": bool(passed), "detail": detail})

    initial = copy.deepcopy(replay["preE20SnapshotState"])
    events = witness["encounter"]["events"]
    final = witness["encounter"]["finalState"]
    base_hash = sha(initial)
    record("exact Return247 to pre-E20 snapshot binding", replay["status"] == "PASS_EXACT_SOURCE_ARCHIVE_REPLAY_TO_PRE_E20_SNAPSHOT" and base_hash == replay["preE20Snapshot"]["stateSHA256"] == witness["encounter"]["baseStateSHA256"], base_hash)

    # Reconstruct the pre-E20 branch directly from the source archive and W2 event replay.
    supplement = json.loads(SUPPLEMENT.read_text(encoding="utf-8"))
    source_events = supplement["eventReplay"]["branches"][0]["events"]
    e20_index = next(i for i, row in enumerate(source_events) if row["id"] == "MF247-F-W2-E20-PAID-GREATER-DISPEL")
    with zipfile.ZipFile(RETURN247) as archive:
        source_case = json.loads(archive.read("cases/MF210-F02.json"))
    branch_state = copy.deepcopy(source_case["events"][-1]["after"])
    assert sha(branch_state) == supplement["eventReplay"]["baseStateSHA256"]
    for source_event in source_events[:e20_index]:
        assert sha(branch_state) == source_event["beforeSHA256"], source_event["id"]
        branch_state = patch(branch_state, source_event["forward"])
        assert sha(branch_state) == source_event["afterSHA256"], source_event["id"]
    record("independent 19-event W2 source replay", e20_index == 19 and branch_state == initial and sha(branch_state) == base_hash, f"replayed {e20_index} events through {source_events[e20_index - 1]['id']}")
    e18 = next(row for row in source_events if row["id"] == "MF247-F-W2-E18-B-HIDE-CHARGE")
    record("source E18 Hide and charge already precede branch boundary", e18["id"] in initial["processedEvents"] and initial["rolls"][2]["id"] == "hideW2" and initial["items"]["bracelet-1"]["charges"] == 0 and any(row.get("rollId") == "hideW2" and row["before"] == 1 and row["after"] == 0 for row in initial["supplement"]["chargeTransactions"]), "E18 is source-replayed once before E19 and before the independent Wave branch")

    active_roots = sorted((item_id, row["imprintRoot"]["id"]) for item_id, row in initial["items"].items() if row.get("imprintRoot", {}).get("active") is True)
    scan = final["scene"]["waveClosure355"]["activeEffectScan"]
    record("single live target and no hidden active casts", active_roots == [("bracelet-1", "castF2")] and scan["pendingCasts"] == {} and scan["activeConcentrations"] == [] and scan["activeEffectRegistryRows"] == [], json.dumps(scan, ensure_ascii=False))

    # Verify every event state and both operation directions without importing builder code.
    cursor = copy.deepcopy(initial)
    inverse_cursor = copy.deepcopy(final)
    inverse_ids: list[str] = []
    event_chain_ok = True
    for event in events:
        if cursor != event["beforeState"] or sha(cursor) != event["beforeSHA256"]:
            event_chain_ok = False
            break
        advanced = patch(copy.deepcopy(cursor), event["forward"])
        if advanced != event["afterState"] or sha(advanced) != event["afterSHA256"]:
            event_chain_ok = False
            break
        cursor = advanced
    if cursor != final or sha(cursor) != sha(final):
        event_chain_ok = False
    for event in reversed(events):
        if inverse_cursor != event["afterState"] or sha(inverse_cursor) != event["afterSHA256"]:
            event_chain_ok = False
            break
        inverse_cursor = patch(copy.deepcopy(inverse_cursor), event["inverse"])
        if inverse_cursor != event["beforeState"] or sha(inverse_cursor) != event["beforeSHA256"]:
            event_chain_ok = False
            break
        inverse_ids.append(event["id"])
    record("independent full forward and inverse replay", event_chain_ok and len(events) == len(inverse_ids) == 12 and inverse_cursor == initial, f"{len(events)} forward and {len(inverse_ids)} inverse events; restored {sha(inverse_cursor)}")

    # Independently validate preparation, payment, components, and turn cadence against Return281.
    with zipfile.ZipFile(RETURN281) as archive:
        profiles_raw = archive.read("ACTOR_PROFILES.json")
        profiles = json.loads(profiles_raw)
        wave_case = json.loads(archive.read("cases/return237/preserved/WC219-NW-FORM.json"))
        case_index = json.loads(archive.read("CASE_INDEX.json"))
        profile = profiles["W219"]
        source_wave_event = wave_case["events"][9]
        wave_rows = [row for row in case_index["cases"] if row.get("spellId") == TARGET]
        wave_case_hashes = []
        for row in wave_rows:
            raw = archive.read(row["path"])
            observed = raw_digest(raw)
            assert observed["bytes"] == row["bytes"] and observed["sha256"] == row["sha256"]
            wave_case_hashes.append(observed["sha256"])

    actor = final["actors"]["WC355"]
    cast = final["supplement"]["waveWitness355"]["castRecords"][0]
    record("distinct legal Wizard acquisition, preparation, focus and components", actor["id"] == "WC355" and actor["class"] == "Wizard" and actor["classLevel"] == 18 and profile["classLevel"] == 18 and TARGET in [row["spellId"] for row in profile["spellbook"]] and TARGET in profile["ordinaryRepertoire"] and TARGET in actor["preparedSpells"] and cast["preparationRecord"]["prepared"] and cast["focusHeld"] and cast["components"] == ["V", "S", "F"], f"W219 level-17 Wave acquisition and prepared set of {profile['preparedCount']}; separate WC355 actor")
    record("actual Action and final 26 RP payment", cast["paidRP"] == 26 and cast["baseRP"] == 26 and cast["additionalRP"] == 0 and actor["RP"] == 42 and actor["resourceHistory"][0]["before"] == 68 and actor["resourceHistory"][0]["after"] == 42 and actor["actionHistory"][0]["remaining"] == 0 and source_wave_event["id"] == "WC219-NW-FORM:10", "One Action; 68 RP to 42 RP; zero Dissonance/Refrain and first prepared family")

    # Re-evaluate the prior counter-window defect against source-bound Wizard/card/component data.
    wizard_source = json.loads(WIZARD_SOURCE.read_text(encoding="utf-8"))
    wizard_card = next(row for row in wizard_source["cards"] if row["id"] == "wizard.base.counterspell")
    catalog = json.loads(SPELL_CATALOG.read_text(encoding="utf-8"))
    counter_catalog = next(row for row in catalog["spells"] if row["id"] == "counterspell")
    bindings = json.loads(CLASS_BINDINGS.read_text(encoding="utf-8"))
    counter_binding = next(row for row in bindings if row["cardId"] == "wizard.base.counterspell")
    assert wizard_card["acquisition"] == "automatic" and wizard_card["activation"] == "Reaction"
    assert wizard_card["cost"] == "3 RP" and wizard_card["frequency"] == "Automatic at Wizard 2; recharge 2 rounds"
    assert "always-prepared class matrices" in wizard_source["engine"][12]
    assert counter_catalog["operational"]["components"] == ["V", "S", "F"]
    assert counter_binding["authority"] == "data/public/class_playtests/wizard.json"
    counter_window = final["supplement"]["waveWitness355"]["counterWindows"][0]
    counter_a = counter_window["responders"]["A"]
    a_at_window = next(event for event in events if event["id"] == "WC355-NW-E05-COUNTER-WINDOW")["beforeState"]["actors"]["A"]
    record("NW355-R1 automatic Counterspell eligibility and TEST_ONLY decline", counter_window["eligibleResponders"] == ["A"] and counter_a["classCardId"] == wizard_card["id"] and counter_a["automaticallyAcquired"] and counter_a["alwaysPreparedClassMatrix"] and counter_a["preparedCounterspell"] and counter_a["ordinaryPreparedListContainsCounterspell"] is False and counter_a["perceivesCasting"] and counter_a["distanceFeet"] == 10 and counter_a["inRange"] and counter_a["rangeFeet"] == 60 and counter_a["lineOfSight"] == "clear" and counter_a["lineOfEffect"] == "clear" and counter_a["components"]["V"] and counter_a["components"]["S"] and counter_a["components"]["F"] and counter_a["reactionAvailable"] and counter_a["rpAvailableBefore"] == a_at_window["RP"] == 49 and counter_a["rpSufficient"] and counter_a["rechargeCounterBefore"] == 0 and counter_a["rechargeReady"] and "declines" in counter_a["response"] and counter_a["resourcesSpent"] == {"Reaction": 0, "RP": 0, "recharge": 0} and counter_catalog["operational"]["components"] == ["V", "S", "F"] and counter_binding["authority"] == "data/public/class_playtests/wizard.json", "Card / always-prepared matrix / components / perception / range / Reaction / 3 RP / recharge all evaluated; A declines without spending")
    stow = next(event for event in events if event["id"] == "WC355-NW-E02-A-PASS-TO-W219-SLOT")
    record("Counterspell hand components are available after logged free interaction", stow["afterState"]["actors"]["A"]["hands"] == {"left": "focus", "right": "free"} and stow["afterState"]["actors"]["A"]["freeInteraction"] == 0 and counter_a["components"]["somaticHand"] == "right hand free after authored free interaction" and counter_a["components"]["materialFocus"] == "Wizard focus held in left hand", "TEST_ONLY branch transition stows dagger and leaves an open somatic hand plus held focus")
    reaction_rows = [row for row in final["actors"]["A"]["reactionHistory"] if row.get("windowId") == counter_window["id"]]
    record("Counterspell response appears in the complete response ledgers", len(reaction_rows) == 1 and reaction_rows[0]["eligible"] and not reaction_rows[0]["spent"] and reaction_rows[0]["RPBefore"] == reaction_rows[0]["RPAfter"] == 49 and reaction_rows[0]["counterspellRechargeBefore"] == reaction_rows[0]["counterspellRechargeAfter"] == 0 and any(row.get("actor") == "A" and row.get("type") == "counter-window-response" and row.get("eligible") and not row.get("spent") for row in final["scene"]["waveClosure355"]["actionReactionReadyLedger"]["events"]), "A's eligibility and explicit decline are recorded in reaction history and encounter ledger")

    e11 = next(event for event in events if event["id"] == "WC355-NW-E11-W219-NEXT-REGULAR-START")
    record("NW355-R2 turnCast resets at next regular turn, cumulative history retained", e11["beforeState"]["actors"]["WC355"]["turnCast"] is True and e11["afterState"]["actors"]["WC355"]["turnCast"] is False and actor["turnCast"] is False and actor["castHistory"] == [cast["id"]] and actor["families"] == [TARGET] and actor["resourceHistory"][0]["paid"] == 26 and actor["Refrain"] == 0, "Per-turn flag clears at E11 while cumulative cast, family, payment and Refrain history remain")
    branch_b = events[0]["afterState"]["scene"]["waveClosure355"]["actionReactionReadyLedger"]["branchOpening"]["B"]
    record("NW355-R3 branch-opening B Hide ledger correctly points to historical E18", branch_b["priorAction"]["eventId"] == e18["id"] and branch_b["priorAction"]["rollId"] == "hideW2" and branch_b["priorAction"]["historicalEventAlreadyInProcessedEvents"] and branch_b["priorAction"]["chargeSpent"] == 1 and branch_b["priorAction"]["chargeTransaction"]["after"] == 0 and branch_b["priorAction"]["roll"] == initial["rolls"][2] and branch_b["Action"] == 0 and "does not replay" in branch_b["slot"].lower() and not any(row["id"] == e18["id"] for row in events), "Already-processed Hide/charge is represented at branch opening and never re-executed")

    geom = final["scene"]["waveClosure355"]
    center = geom["perceivedFixedCenterFeet"]
    item_point = geom["itemAnchorFeet"]
    wall = geom["authoredTestSceneWalls"][0]
    sample = geom["coveredSamplePointFeet"]
    item_distance = math.dist(center, item_point)
    sample_distance = math.dist(center, sample)
    wall_blocks_sample = segment_hits_box(center, sample, wall["boxFeet"])
    wall_blocks_item = segment_hits_box(center, item_point, wall["boxFeet"])
    record("3D sphere range and initial opaque-cover clipping", geom["radiusFeet"] == 60 and geom["rangeToCenterFeet"] <= 60 and math.isclose(item_distance, geom["itemAnchorDistanceFeet"]) and item_distance < 60 and math.isclose(sample_distance, geom["coveredSampleDistanceFeet"]) and sample_distance < 60 and wall_blocks_sample and not wall_blocks_item and geom["volumeClippedByCover"] and not geom["initialCoverClipsTarget"], f"item={item_distance:.6f} ft visible; covered sample={sample_distance:.6f} ft blocked by {wall['id']}")
    capture_snapshot = final["supplement"]["waveWitness355"]["captureRecords"][0]["initialCoverSnapshot"]
    scene_wall_snapshot = geom["sceneWallsAtSnapshot"]
    record("NW355-R4 exact covered-sample distance and consistent source/test wall snapshots", math.isclose(sample_distance, math.sqrt(234)) and math.isclose(capture_snapshot["coveredSample"]["distanceFeet"], math.sqrt(234)) and capture_snapshot["sceneWalls"] == scene_wall_snapshot and capture_snapshot["sourceSceneWallsBeforeFixture"] == geom["sourceSceneWallsBeforeFixture"] and capture_snapshot["authoredTestSceneWalls"] == geom["authoredTestSceneWalls"] and scene_wall_snapshot == capture_snapshot["sourceSceneWallsBeforeFixture"] + capture_snapshot["authoredTestSceneWalls"], f"distance={sample_distance:.15f}; immutable wall snapshot reconciles source walls plus labeled TEST_ONLY fixture wall")

    before_item, after_item = initial["items"]["bracelet-1"], final["items"]["bracelet-1"]
    body_before = {k: v for k, v in before_item.items() if k not in {"imprintRoot", "revision"}}
    body_after = {k: v for k, v in after_item.items() if k not in {"imprintRoot", "revision"}}
    endings = [row for row in final["supplement"]["imprintEndings"] if row.get("rootId") == "castF2"]
    record("one-time root ending and preserved damaged mundane body", before_item["imprintRoot"]["active"] is True and after_item["imprintRoot"]["active"] is False and body_before == body_after and len(endings) == 1 and after_item["HP"] == 2 and after_item["charges"] == 0 and after_item["custodian"] == "B-right-wrist" and after_item["owner"] == "A" and after_item["worn"] is True, "Only castF2 ends; damage, spent charge, custody, ownership, worn state and body remain byte-equivalent")

    cap = final["scene"]["waveClosure355"]["captureResult"]
    capture_rows = final["supplement"]["waveWitness355"]["captureRecords"]
    record("direct source-sigil resolution with no save or DC28 check", cap["captured"] == ["castF2"] and cap["save"] is None and cap["check"] is None and cap["GreaterDispelDC28Check"] is None and len(capture_rows) == 1 and capture_rows[0]["endingAppliedExactlyOnce"], "No additional save, rank check, or Greater Dispel DC 28 test")

    probe = final["supplement"]["waveWitness355"]["postTerminationFunctionChecks"][0]
    record("post-end magic lost while mundane item function survives", probe["total"] == probe["d20"] + probe["dexModifier"] + probe["proficiencyBonus"] + probe["braceletPassiveBonus"] == 12 and probe["result"] == "not hidden" and probe["ordinaryAdornmentPersists"] and probe["chargeSpent"] == 0 and probe["authorship"].startswith("finite authored"), "Fixture Hide check loses +1 imprint bonus; ordinary adornment and bracelet body persist")

    record("all 18 historical Wave cases retained", len(wave_rows) == 18 and len(wave_case_hashes) == 18, f"validated {len(wave_case_hashes)} byte/hash bindings from the complete Return281 archive")
    queue = json.loads(QUEUE.read_text(encoding="utf-8"))
    pending = json.loads(PENDING.read_text(encoding="utf-8"))
    record("full queue preserved with no inferred acceptance", queue["pendingCount"] == pending["pendingCount"] == 22 and len(pending["pendingIds"]) == 22 and TARGET in pending["pendingIds"] and queue["supersedesQueue"].endswith("CURRENT_SPELL_QUEUE_355.json") and queue["currentPacket"]["status"] == "DIRECTOR_REVIEW_PENDING" and not witness["acceptedIds"] and not witness["appliedIds"] and not witness["closedBlockerIds"] and witness["applicationAuthorized"] is False, "22 identities remain pending; Repack01 pending; no identity accepted/applied and no blocker closed")

    failures = [row for row in checks if not row["passed"]]
    result = {
        "id": "NULLIFICATION-WAVE-CLOSURE355-REPACK01-INDEPENDENT-AUDIT",
        "recordedBy": "verify_nullification_wave_closure355_repack01.py (separate verifier implementation)",
        "status": "PASS" if not failures else "FAIL",
        "checkCount": len(checks), "passedChecks": len(checks) - len(failures), "failedChecks": len(failures),
        "checks": checks,
        "scopeIds": [TARGET], "blockerIds": ["WC188-B01"],
        "witnessBinding": {"path": WITNESS_PATH.relative_to(ROOT).as_posix(), **raw_digest(WITNESS_PATH.read_bytes())},
        "sourceBindings": {
            "return247Archive": raw_digest(RETURN247.read_bytes()),
            "return281Archive": raw_digest(RETURN281.read_bytes()),
            "supplement255W2": raw_digest(SUPPLEMENT.read_bytes()),
        },
        "authority": witness["baseAuthority"],
        "interpretiveLimit": "Independent data, source, geometry, payment, lifecycle, queue, and reversible-patch verification of an authored TEST_ONLY witness. This is not observed play, Director acceptance, or application authorization.",
    }
    output = AUDIT / "NULLIFICATION_WAVE_CLOSURE355_REPACK01_INDEPENDENT_AUDIT.json"
    output.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({"status": result["status"], "checks": result["checkCount"], "passed": result["passedChecks"], "failed": result["failedChecks"], "output": str(output)}, indent=2))
    if failures:
        raise SystemExit(json.dumps(failures, indent=2))


if __name__ == "__main__":
    main()
