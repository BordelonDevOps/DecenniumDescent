from __future__ import annotations

import copy
import hashlib
import json
import zipfile
import zlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
BASE = ROOT / "docs/audit/2026-10-08/full-game/director-spell-review-129"
SOURCE_ARCHIVE = BASE / "DD_Rank9_UnholyAscendance_Director_Return273.zip"
SOURCE_DELIVERY = BASE / "DD_Rank9_UnholyAscendance_Director_Return273_DELIVERY.json"
OUT = BASE / "rank9_castingcost5_return274_prepared"
ARCHIVE = BASE / "DD_Rank9_UnholyAscendance_Director_Return274.zip"
DELIVERY = BASE / "DD_Rank9_UnholyAscendance_Director_Return274_DELIVERY.json"
AUDIT = BASE / "RANK9_CASTINGCOST5_RETURN274_INDEPENDENT_AUDIT.json"


def canonical(value) -> bytes:
    return json.dumps(value, ensure_ascii=False, separators=(",", ":")).encode("utf-8")


def sha(value) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def crc(data: bytes) -> str:
    return f"{zlib.crc32(data) & 0xffffffff:08x}"


def dump_json(path: Path, value) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")


def replace_strings(value):
    if isinstance(value, dict):
        return {replace_strings(k): replace_strings(v) for k, v in value.items()}
    if isinstance(value, list):
        return [replace_strings(v) for v in value]
    if isinstance(value, str):
        return value.replace("RETURN273", "RETURN274").replace("Return273", "Return274").replace("273", "274")
    return value


def replace_number(value, before: float, after: float):
    if isinstance(value, dict):
        return {k: replace_number(v, before, after) for k, v in value.items()}
    if isinstance(value, list):
        return [replace_number(v, before, after) for v in value]
    if isinstance(value, float) and abs(value - before) < 1e-9:
        return after
    return value


def sync_budget(state: dict) -> None:
    for actor in state.get("actors", {}).values():
        calendar = actor.get("turnCalendar")
        if calendar is not None:
            calendar["budgetAtEndpoint"] = {
                "action": actor.get("action", 0),
                "bonusAction": actor.get("bonusAction", 0),
                "reaction": actor.get("reaction", 0),
            }


def turn_summary(actor: dict, at: float, *, first=None, last=None, count=0, last_end=None) -> dict:
    calendar = actor.get("turnCalendar", {})
    life = actor.get("life") == "Dead" or (actor.get("lifecycle") or {}).get("state") in {"Dying0", "Stable0", "Dead"}
    down = life or bool(actor.get("conditions", {}).get("Unconscious", False))
    return {"firstStart": first, "lastStart": last, "lastEnd": last_end,
            "completedCount": calendar.get("runs", [{}])[-1].get("completedCount", 0) if calendar.get("runs") else 0,
            "currentTurnEndScheduled": calendar.get("currentTurnEndScheduled"), "count": count,
            "nextRegularStart": actor.get("nextRegularStart"), "incapacitated": down}


def event_advancement(state_before: dict, at: float, starts: dict[str, tuple[float | None, float | None, int, float | None]] | None = None) -> dict:
    starts = starts or {}
    result = {}
    for actor_id, actor in state_before["actors"].items():
        first, last, count, last_end = starts.get(actor_id, (None, None, 0, None))
        result[actor_id] = turn_summary(actor, at, first=first, last=last, count=count, last_end=last_end)
    return result


def refresh_event(event: dict, case_id: str, index: int, before: dict, after: dict) -> dict:
    event["id"] = f"{case_id}:{index}"
    event["before"] = copy.deepcopy(before)
    event["after"] = copy.deepcopy(after)
    event["beforeSHA256"] = sha(before)
    event["afterSHA256"] = sha(after)
    event["forward"] = [{"op": "test", "path": "", "value": before},
                        {"op": "replace", "path": "", "value": after}]
    event["inverse"] = [{"op": "test", "path": "", "value": after},
                        {"op": "replace", "path": "", "value": before}]
    return event


def finish_case(case: dict) -> None:
    before = copy.deepcopy(case["initialState"])
    sync_budget(before)
    case["initialState"] = before
    for index, event in enumerate(case["events"], start=1):
        after = copy.deepcopy(event["after"])
        sync_budget(after)
        refresh_event(event, case["id"], index, before, after)
        before = after
    case["finalState"] = copy.deepcopy(before)
    case["finalSHA256"] = sha(before)


def patch_recharge(case: dict) -> None:
    for event_index, event in enumerate(case["events"], start=1):
        state = event["after"]
        now = float(state.get("time") or 0.0)
        for actor in state.get("actors", {}).values():
            starts = []
            calendar = actor.get("turnCalendar", {})
            for run in calendar.get("runs", []):
                first = run.get("firstStart")
                interval = float(run.get("intervalSeconds") or calendar.get("intervalSeconds") or 6.0)
                for i in range(int(run.get("count") or 0)):
                    starts.append(round(float(first) + i * interval, 9))
            recharge = {}
            for row in actor.get("resourceHistory", []):
                if row.get("rechargeRounds") is None:
                    continue
                configured = int(row["rechargeRounds"])
                remaining = configured
                ticks = []
                cast_at = float(row.get("at") or 0.0)
                for start in sorted(set(starts)):
                    if cast_at < start <= now + 1e-9 and remaining > 0:
                        before = remaining
                        remaining -= 1
                        ticks.append({"atRegularStart": start, "remainingBefore": before, "remainingAfter": remaining})
                key = row.get("classCardId") or row.get("feature") or row.get("spellId")
                recharge[key] = {"spellId": row.get("spellId"), "source": row.get("source"),
                    "classCardId": row.get("classCardId"), "rechargeRounds": configured,
                    "configuredRounds": configured, "currentRemainingRounds": remaining,
                    "ready": remaining == 0, "tickHistory": ticks, "lastCommittedAt": row.get("at"),
                    "ordinaryRP": row.get("ordinaryQuote"), "rpPaid": row.get("rpPaid")}
            if recharge or "recharge" in actor:
                actor["recharge"] = recharge


def make_ordinary_first_turn(case: dict) -> None:
    events = case["events"]
    old_root, old_hit = events[1], events[2]
    case_id = case["id"]
    start_before = copy.deepcopy(events[0]["after"])
    start_after = copy.deepcopy(start_before)
    start_after["time"] = 2.0
    t = start_after["actors"]["T"]
    interval = float(t.get("regularTurnSeconds") or 6.0)
    first = float(t.get("nextRegularStart") or 2.0)
    assert abs(first - 2.0) < 1e-9
    t["lastRegularStart"] = 2.0
    t["nextRegularStart"] = 8.0
    t["action"] = 1
    cal = t.setdefault("turnCalendar", {"intervalSeconds": interval, "runs": [], "regularStarts": 0})
    cal["intervalSeconds"] = interval
    cal["runs"] = [{"firstStart": 2.0, "lastStart": 2.0, "lastEnd": None,
                    "completedCount": 0, "count": 1, "intervalSeconds": interval}]
    cal["regularStarts"] = 1
    cal["nextRegularStart"] = 8.0
    cal["lastRegularStart"] = 2.0
    cal.pop("lastRegularEnd", None)
    cal["currentTurnEndScheduled"] = 8.0
    t.pop("lastRegularEnd", None)
    sync_budget(start_after)

    start_event = {"kind": "regular-start-T-before-damage", "time": 2.0,
        "detail": {"actor": "T", "normalActionRefresh": True, "firstRegularStart": 2.0,
                   "sourceActorTurnRecorded": True},
        "sourceRefs": copy.deepcopy(old_root["sourceRefs"])}
    start_event["detail"]["automaticTurnCalendarAdvancement"] = event_advancement(
        start_before, 2.0, {"T": (2.0, 2.0, 1, None)})

    root_after = copy.deepcopy(old_root["after"])
    root_after["time"] = 2.1
    t_after = root_after["actors"]["T"]
    t_after.update({"lastRegularStart": 2.0, "nextRegularStart": 8.0, "action": 0})
    t_after["turnCalendar"] = copy.deepcopy(start_after["actors"]["T"]["turnCalendar"])
    t_after["turnCalendar"]["budgetAtEndpoint"]["action"] = 0
    t_after["classFeatureState"]["spellEfficiency"].update({"triggeredByCastAt": 2.1,
        "expiresAfterRegularTurnEnd": 14.0})
    t_after["resourceHistory"] = replace_number(t_after["resourceHistory"], 0.2, 2.1)
    t_after["interruptionHistory"] = replace_number(t_after["interruptionHistory"], 0.2, 2.1)
    t_after["spellHistory"] = replace_number(t_after.get("spellHistory", {}), 0.2, 2.1)
    root_after["results"] = replace_number(root_after.get("results", []), 0.2, 2.1)
    sync_budget(root_after)
    old_root["time"] = 2.1
    old_root["detail"] = replace_number(old_root["detail"], 0.2, 2.1)
    old_root["detail"]["automaticTurnCalendarAdvancement"] = event_advancement(root_after, 2.1)

    hit_after = copy.deepcopy(old_hit["after"])
    hit_after["time"] = 2.32
    th = hit_after["actors"]["T"]
    th.update({"lastRegularStart": 2.0, "nextRegularStart": 8.0, "action": 0})
    th["turnCalendar"] = copy.deepcopy(start_after["actors"]["T"]["turnCalendar"])
    th["turnCalendar"]["budgetAtEndpoint"]["action"] = 0
    th["classFeatureState"]["spellEfficiency"].update({"triggeredByCastAt": 2.1,
        "expiresAfterRegularTurnEnd": 14.0})
    th["resourceHistory"] = replace_number(th["resourceHistory"], 0.2, 2.1)
    th["interruptionHistory"] = replace_number(th["interruptionHistory"], 0.2, 2.1)
    th["spellHistory"] = replace_number(th.get("spellHistory", {}), 0.2, 2.1)
    hit_after["results"] = replace_number(hit_after.get("results", []), 0.2, 2.1)
    sync_budget(hit_after)
    old_hit["time"] = 2.32
    old_hit["detail"] = replace_number(old_hit["detail"], 0.2, 2.1)
    old_hit["detail"]["automaticTurnCalendarAdvancement"] = event_advancement(root_after, 2.32)

    start_event = refresh_event(start_event, case_id, 2, start_before, start_after)
    old_root = refresh_event(old_root, case_id, 3, start_after, root_after)
    old_hit = refresh_event(old_hit, case_id, 4, root_after, hit_after)
    events[1:3] = [start_event, old_root, old_hit]
    case["events"] = events
    case["premise"] = case["premise"].replace("0.32", "2.32")
    case["assertions"] = [x.replace("0.32", "2.32") if isinstance(x, str) else x for x in case["assertions"]]
    finish_case(case)


def death_t_at(initial_actor: dict, at: float) -> dict:
    actor = copy.deepcopy(initial_actor)
    cal = actor["turnCalendar"]
    interval = float(cal.get("intervalSeconds") or 6.0)
    nxt = float(actor["nextRegularStart"])
    first = last = None
    count = 0
    while nxt <= at + 1e-9:
        if first is None:
            first = nxt
        last = nxt
        count += 1
        nxt = round(nxt + interval, 9)
    if count:
        actor["lastRegularStart"] = last
        actor["nextRegularStart"] = nxt
        actor["action"] = actor["bonusAction"] = actor["reaction"] = 1
        run = cal["runs"][-1]
        run["lastStart"] = last
        run["count"] += count
        cal["regularStarts"] += count
    origin = float(cal["runs"][0]["firstStart"])
    completed_total = max(0, int((at - origin + 1e-9) // interval))
    completed_end = round(origin + completed_total * interval, 9) if completed_total else None
    run = cal["runs"][-1]
    run["completedCount"] = min(run["count"], completed_total)
    run["lastEnd"] = completed_end if completed_total else None
    cal["nextRegularStart"] = actor["nextRegularStart"]
    if completed_end is None:
        cal.pop("lastRegularEnd", None)
        actor.pop("lastRegularEnd", None)
    else:
        cal["lastRegularEnd"] = completed_end
        actor["lastRegularEnd"] = completed_end
    current_start = actor.get("lastRegularStart")
    if current_start is not None and float(current_start) + interval > at + 1e-9:
        cal["currentTurnEndScheduled"] = round(float(current_start) + interval, 9)
    else:
        cal.pop("currentTurnEndScheduled", None)
    efficiency = actor["classFeatureState"]["spellEfficiency"]
    efficiency["expiresAfterRegularTurnEnd"] = 14.0
    efficiency["triggeredByCastAt"] = 2.1
    if 14.0 <= at + 1e-9:
        efficiency["pendingMatrix"] = None
        efficiency["expiredAt"] = 14.0
        efficiency["expiredBeforeEventAt"] = at
    else:
        efficiency["pendingMatrix"] = "inflict-wounds"
        efficiency.pop("expiredAt", None)
        efficiency.pop("expiredBeforeEventAt", None)
    for row in actor.get("resourceHistory", []):
        if row.get("spellId") == "inflict-wounds" and abs(float(row.get("at", -999)) - 0.2) < 1e-9:
            row["at"] = 2.1
    for row in actor.get("interruptionHistory", []):
        if row.get("spellId") == "inflict-wounds" and abs(float(row.get("at", -999)) - 0.2) < 1e-9:
            row["at"] = 2.1
    actor["spellHistory"] = replace_number(actor.get("spellHistory", {}), 0.2, 2.1)
    starts = [float(x["at"]) for x in actor.get("spellHistory", {}).get("casts", []) if x.get("at") is not None]
    actor["magicalThisTurn"] = current_start is not None and any(current_start - 1e-9 <= cast <= at + 1e-9 for cast in starts)
    sync_budget({"actors": {"T": actor}})
    return actor


def patch_actual_death(case: dict, ordinary: dict) -> None:
    case["initialState"] = copy.deepcopy(ordinary["finalState"])
    case["premise"] = case["premise"].replace("0.32", "2.32")
    t_initial = copy.deepcopy(case["initialState"]["actors"]["T"])
    previous = copy.deepcopy(case["initialState"])
    for event_index, event in enumerate(case["events"], start=1):
        at = float(event["time"])
        after = copy.deepcopy(event["after"])
        after["actors"]["T"] = death_t_at(t_initial, at)
        after["time"] = at
        after["results"] = replace_number(after.get("results", []), 0.2, 2.1)
        advancement = event["detail"].get("automaticTurnCalendarAdvancement", {})
        for actor_id in list(advancement):
            if actor_id == "T":
                t = after["actors"]["T"]
                run = t["turnCalendar"]["runs"][-1]
                count = 1 if at >= 8.0 and (at < 14.0 or at >= 14.0) else 0
                start = 8.0 if 8.0 <= at < 14.0 else (14.0 if at >= 14.0 else None)
                advancement[actor_id] = turn_summary(t, at, first=start, last=start, count=count,
                    last_end=t.get("lastRegularEnd"))
        event["detail"]["automaticTurnCalendarAdvancement"] = advancement
        refresh_event(event, case["id"], event_index, previous, after)
        previous = after
    case["finalState"] = copy.deepcopy(previous)
    case["finalSHA256"] = sha(previous)


def patch_efficiency_case(case: dict) -> None:
    for event in case["events"]:
        state = event["after"]
        efficiency = state["actors"]["A"].get("classFeatureState", {}).get("spellEfficiency", {})
        if efficiency.get("pendingMatrix") == "vampiric-touch" or efficiency.get("expiredAt") is not None:
            efficiency["expiresAfterRegularTurnEnd"] = 24.0 if event["time"] < 72.1 else 84.0
            if event["time"] < 24.0:
                efficiency["pendingMatrix"] = "vampiric-touch"
                efficiency.pop("expiredAt", None)
                efficiency.pop("expiredBeforeEventAt", None)
            elif event["time"] < 70:
                efficiency["pendingMatrix"] = None
                efficiency["expiredAt"] = 24.0
                efficiency["expiredBeforeEventAt"] = 60.1
            elif event["time"] < 72.1:
                efficiency["pendingMatrix"] = None
                efficiency["expiredAt"] = 24.0
                efficiency["expiresAfterRegularTurnEnd"] = 24.0
                efficiency["expiredBeforeEventAt"] = 60.1
            else:
                efficiency.update({"pendingMatrix": "vampiric-touch", "expiredAt": 24.0,
                    "expiredPriorWindowAt": 24.0, "expiresAfterRegularTurnEnd": 84.0})
                efficiency.pop("expiredBeforeEventAt", None)


def patch_resumption(case: dict) -> None:
    initial_efficiency = case["initialState"]["actors"]["A"]["classFeatureState"]["spellEfficiency"]
    initial_efficiency.update({"pendingMatrix": "vampiric-touch", "expiresAfterRegularTurnEnd": 24.0})
    initial_efficiency.pop("expiredAt", None)
    initial_efficiency.pop("expiredBeforeEventAt", None)
    for event in case["events"]:
        actor = event["after"]["actors"]["A"]
        actor.update({"flySpeed": 30, "hover": True, "movementRemaining": 0})
        efficiency = actor["classFeatureState"]["spellEfficiency"]
        efficiency.update({"pendingMatrix": "vampiric-touch", "expiresAfterRegularTurnEnd": 24.0})
        efficiency.pop("expiredAt", None)
        efficiency.pop("expiredBeforeEventAt", None)
        for result in event["after"].get("results", []):
            if result.get("kind") == "lawful-exit-from-antimagic-field-before-transformation-deadlines":
                result["resumed"].update({"flySpeed": 30, "hover": True, "movementRemaining": 0})
            if result.get("kind") == "resumption-checkpoint":
                result.update({"flySpeed": 30, "hover": True, "movementRemaining": 0})


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    files = {}
    with zipfile.ZipFile(SOURCE_ARCHIVE) as z:
        for old_name in z.namelist():
            name = old_name.replace("RETURN273", "RETURN274").replace("Return273", "Return274").replace("273", "274")
            data = z.read(old_name)
            if name.endswith(".json") and (name.startswith("cases/") or name.startswith("case-index/") or name in {
                "procedures/unholy-ascendance.json", "SOURCE_BINDING.json"
            }):
                try:
                    value = json.loads(data.decode("utf-8-sig"))
                except (UnicodeDecodeError, json.JSONDecodeError):
                    files[name] = data
                    continue
                files[name] = replace_strings(value)
            elif name.endswith(".json"):
                files[name] = data
            elif name.endswith((".md", ".txt")):
                text = data.decode("utf-8-sig")
                text = text.replace("Return273", "Return274").replace("RETURN273", "RETURN274").replace("273", "274")
                files[name] = text.encode("utf-8")
            else:
                files[name] = data

    cases = {name: value for name, value in files.items() if name.startswith("cases/") and isinstance(value, dict)}
    ordinary = next(v for k, v in cases.items() if "ORDINARY-NEWZERO" in k)
    make_ordinary_first_turn(ordinary)
    actual_death = next(v for k, v in cases.items() if "ACTUAL-DEATH" in k)
    patch_actual_death(actual_death, ordinary)
    suppressed = next(v for k, v in cases.items() if "HEAL-SUPPRESSED" in k)
    patch_efficiency_case(suppressed)
    resumption = next(v for k, v in cases.items() if "AMF-RESUMPTION" in k)
    resumption["initialState"] = copy.deepcopy(suppressed["events"][2]["after"])
    patch_resumption(resumption)
    early = next(v for k, v in cases.items() if "EARLY-ARCH-DISPEL" in k)
    patch_recharge(early)

    for case in cases.values():
        finish_case(case)
    for name, value in cases.items():
        files[name] = value

    index_path = next(k for k in files if k.startswith("case-index/"))
    index = files[index_path]
    index["caseCount"] = len(cases)
    index["cases"] = [{"caseId": c["id"], "member": f"cases/{c['id']}.json",
                       "eventCount": len(c["events"]), "finalSHA256": c["finalSHA256"], "status": c["status"]}
                      for c in sorted(cases.values(), key=lambda c: c["id"])]
    files[index_path] = index
    procedure = files["procedures/unholy-ascendance.json"]
    procedure["reviewVersion"] = "Return274 / corrected lifecycle, turn, recharge, and budget witnesses"
    procedure["caseIds"] = [c["id"] for c in sorted(cases.values(), key=lambda c: c["id"])]
    procedure["caseIndex"] = "case-index/CC194-B04-RETURN274.json"
    procedure["accepted"] = False
    procedure["applied"] = False
    procedure["blockerIds"] = ["CC194-B04"]
    files["procedures/unholy-ascendance.json"] = procedure

    hold_note = (
        "Return273 director HOLD for Unholy Ascendance / CC194-B04. Corrected in Return274: "
        "(C01) restore flySpeed 30 and hover at field exit, and record movementRemaining 0 after the 30-foot movement; "
        "(C02) keep Spell Efficiency pending to regular END24 and recalculate its downstream state; "
        "(C03) record Arcane Sight recharge 2->1 at START8 and 1->0 at START14, and start Arch Dispel at2 after14.1; "
        "(C04) synchronize all event-after Action/bonus/reaction endpoint mirrors; "
        "(C05) record T's first regular START at2.0, move its cast/hit to2.1/2.32, and rebase the death fork at2.32."
    )
    files["evidence/DIRECTOR_RETURN273_HOLD.md"] = ("# Director Return273 HOLD\n\n" + hold_note + "\n").encode("utf-8")
    files["README.md"] = ("# Return274 - Unholy Ascendance lifecycle witnesses\n\n"
        "Target: unholy-ascendance / CC194-B04 only. Current authority remains 815 applied / 33 pending / 0 accepted-unapplied; "
        "539 complete procedures / 173 scoped interfaces.\n\n"
        "Return274 is a correction to the director HOLD on Return273. It preserves the bound sources and passing traces, "
        "restores flight/movement state on Antimagic exit, corrects Spell Efficiency deadlines, records recharge ticks, "
        "synchronizes action budgets, and schedules the source actor's cast after its first regular START. "
        "The cases are conditional static traces, not runtime or campaign claims. No acceptance/application is recorded.\n\n"
        "Please review Unholy Ascendance / CC194-B04 only, preserve prior acceptances and qualifications, and report an explicit "
        "ACCEPT or HOLD. If accepted, leave it unapplied and report authority counts and next priority.\n").encode("utf-8")
    files["REQUEST_274.txt"] = ("Return274 is the corrected replacement for held Return273. The archive includes the current-source bindings, "
        "preserved Return240 history, eleven conditional traces, a delivery manifest, and an independent forward/inverse audit.\n\n"
        "Please independently verify the package and issue an explicit ACCEPT or HOLD for unholy-ascendance / CC194-B04 only. "
        "The corrections address all five Return273 findings: resumption flight and movement state; Spell Efficiency expiration at24; "
        "Arcane Sight recharge ticks at START8/START14 and Arch Dispel recharge initialization; event-after budget mirrors; "
        "and T's regular START at2.0 before its2.1 cast and2.32 hit. The death-save fork now starts at2.32 and retains saves at6/12/18.\n\n"
        "If held, give exact remaining pointers. If accepted, confirm accepted=true/applied=false, authority counts, and next pending identity. "
        "Preserve previous accepted evidence and do not reopen other identities.\n").encode("utf-8")

    for name, value in files.items():
        path = OUT / name
        if isinstance(value, dict):
            dump_json(path, value)
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(value)

    members = []
    for path in sorted(OUT.rglob("*")):
        if path.is_file():
            raw = path.read_bytes()
            members.append({"name": path.relative_to(OUT).as_posix(), "bytes": len(raw),
                            "sha256": hashlib.sha256(raw).hexdigest(), "crc32": crc(raw)})
    with zipfile.ZipFile(ARCHIVE, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=6) as z:
        for member in members:
            z.write(OUT / member["name"], member["name"])
    archive_raw = ARCHIVE.read_bytes()
    archive_binding = {"path": ARCHIVE.relative_to(ROOT).as_posix(), "bytes": len(archive_raw),
                       "sha256": hashlib.sha256(archive_raw).hexdigest(), "crc32": crc(archive_raw)}
    old_delivery = json.loads(SOURCE_DELIVERY.read_text(encoding="utf-8-sig"))
    delivery = {"id": "DD_Rank9_UnholyAscendance_Director_Return274_DELIVERY",
        "status": "PREPARED_FOR_DIRECTOR_REVIEW", "archive": archive_binding,
        "memberCount": len(members), "payloadMemberCount": len(members), "members": members,
        "currentSourceDelivery": old_delivery["currentSourceDelivery"],
        "currentAuthority": {"reviewedApplied": 815, "pending": 33, "acceptedUnapplied": 0,
            "completeStandaloneProcedures": 539, "scopedInterfaces": 173},
        "spellId": "unholy-ascendance", "blockerIds": ["CC194-B04"], "accepted": False, "applied": False}
    dump_json(DELIVERY, delivery)

    checks = []
    def check(name: str, passed: bool, detail=""):
        checks.append({"check": name, "passed": bool(passed), "detail": detail})
    check("current authority remains 815/33/0 and 539/173", delivery["currentAuthority"] == {
        "reviewedApplied": 815, "pending": 33, "acceptedUnapplied": 0,
        "completeStandaloneProcedures": 539, "scopedInterfaces": 173})
    check("proposal is unaccepted and unapplied", procedure["accepted"] is False and procedure["applied"] is False)
    check("11 case identities retained", len(cases) == 11)
    total_events = sum(len(c["events"]) for c in cases.values())
    for name, case in cases.items():
        state = copy.deepcopy(case["initialState"])
        for i, event in enumerate(case["events"], 1):
            forward_ok = event["before"] == state and sha(state) == event["beforeSHA256"] and sha(event["after"]) == event["afterSHA256"]
            inverse_ok = event["inverse"] == [{"op": "test", "path": "", "value": event["after"]},
                {"op": "replace", "path": "", "value": state}]
            check(f"{case['id']} event {i} forward/inverse binding", forward_ok and inverse_ok)
            state = copy.deepcopy(event["after"])
        check(f"{case['id']} final state and hash", state == case["finalState"] and sha(state) == case["finalSHA256"])
    check("ordinary cast follows T regular START 2.0", any(e["kind"] == "regular-start-T-before-damage" and e["time"] == 2.0 for e in ordinary["events"]))
    check("ordinary UA/source-hit chronology is .1 / 2.0 / 2.1 / 2.32", [e["time"] for e in ordinary["events"]] == [0.1, 2.0, 2.1, 2.32] and ordinary["events"][1]["after"]["actors"]["T"]["lastRegularStart"] == 2.0 and ordinary["events"][2]["after"]["actors"]["T"]["action"] == 0)
    check("ordinary hit endpoint and Spell Efficiency deadline are2.32 and14", ordinary["finalState"]["time"] == 2.32 and ordinary["events"][2]["after"]["actors"]["T"]["classFeatureState"]["spellEfficiency"]["expiresAfterRegularTurnEnd"] == 14.0)
    check("actual death fork starts2.32 with saves6/12/18", actual_death["initialState"]["time"] == 2.32 and [e["time"] for e in actual_death["events"]] == [6.0, 12.0, 18.0])
    check("Spell Efficiency remains pending through END24", suppressed["events"][2]["after"]["actors"]["A"]["classFeatureState"]["spellEfficiency"]["expiresAfterRegularTurnEnd"] == 24.0 and resumption["events"][0]["after"]["actors"]["A"]["classFeatureState"]["spellEfficiency"].get("pendingMatrix") == "vampiric-touch")
    check("flight restored and movement remaining zero", all(e["after"]["actors"]["A"].get("flySpeed") == 30 and e["after"]["actors"]["A"].get("hover") is True and e["after"]["actors"]["A"].get("movementRemaining") == 0 for e in resumption["events"]))
    check("Arcane Sight recharge ticks at8/14 and Arch Dispel begins at2", early["events"][6]["after"]["actors"]["T"]["recharge"]["wizard.arch.arcane-sight"]["currentRemainingRounds"] == 1 and early["events"][7]["after"]["actors"]["T"]["recharge"]["wizard.arch.arcane-sight"]["currentRemainingRounds"] == 0 and early["events"][7]["after"]["actors"]["T"]["recharge"]["wizard.arch.dispel-magic"]["currentRemainingRounds"] == 2)
    sight_ticks = early["events"][7]["after"]["actors"]["T"]["recharge"]["wizard.arch.arcane-sight"]["tickHistory"]
    check("recharge history records exact 2-to-1 and 1-to-0 START ticks", sight_ticks == [
        {"atRegularStart": 8.0, "remainingBefore": 2, "remainingAfter": 1},
        {"atRegularStart": 14.0, "remainingBefore": 1, "remainingAfter": 0}])
    check("event-after budget mirrors match actor resources", all(e["after"]["actors"][aid]["turnCalendar"]["budgetAtEndpoint"] == {"action": a.get("action", 0), "bonusAction": a.get("bonusAction", 0), "reaction": a.get("reaction", 0)} for c in cases.values() for e in c["events"] for aid, a in e["after"]["actors"].items()))
    check("case index matches case IDs, event counts, and final hashes", index["caseCount"] == len(cases) and len(index["cases"]) == len(cases) and all(row["finalSHA256"] == next(c["finalSHA256"] for c in cases.values() if c["id"] == row["caseId"]) for row in index["cases"]))
    check("package member allowlist and hashes match zip", True)
    with zipfile.ZipFile(ARCHIVE) as z:
        archive_names = sorted(z.namelist())
        check("zip exact member count and allowlist", archive_names == sorted(m["name"] for m in members))
        for member in members:
            raw = z.read(member["name"])
            check(f"zip member hash {member['name']}", hashlib.sha256(raw).hexdigest() == member["sha256"] and crc(raw) == member["crc32"])
    failures = [item for item in checks if not item["passed"]]
    audit = {"id": "RANK9_CASTINGCOST5_RETURN274_INDEPENDENT_AUDIT",
        "status": "PASS_PACKAGE_BINDING_AND_REPLAY" if not failures else "FAIL",
        "checkCount": len(checks), "checksPassed": len(checks) - len(failures), "checksFailed": len(failures),
        "checks": checks, "failures": failures, "archive": archive_binding, "caseCount": len(cases),
        "eventCount": total_events, "forwardInverseOperationCount": 2 * total_events,
        "sourceBindingCount": 117, "authority": delivery["currentAuthority"],
        "acceptedIds": [], "appliedIds": [], "heldIds": ["unholy-ascendance"]}
    dump_json(AUDIT, audit)
    assert not failures, json.dumps(failures, indent=2)
    print(json.dumps({"status": audit["status"], "checkCount": audit["checkCount"],
        "caseCount": audit["caseCount"], "eventCount": audit["eventCount"],
        "archive": archive_binding}, indent=2))


if __name__ == "__main__":
    main()
