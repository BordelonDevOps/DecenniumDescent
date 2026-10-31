from __future__ import annotations

import hashlib
import json
import sys
import zipfile
import zlib
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
REPO = HERE.parents[4]
OUT = HERE / "rank9_timeless_form_closure_346_delivery"
ARCHIVE = OUT / "DD_Rank9_TimelessForm_DF218B03_Closure346.zip"
W345 = HERE / "rank9_time_stop_joint_witness_345_delivery_r6/DD_Rank9_TimeStop_TF318_Witness345.zip"
OLD = HERE / "rank9_defenseform8_return308_received/DD_Rank9_DefenseForm8_Director_Return308_HELD.zip"
W345_DELIVERY = HERE / "rank9_time_stop_joint_witness_345_delivery_r6/DD_Rank9_TimeStop_TF318_Witness345_DELIVERY.json"
CURRENT_QUEUE = HERE / "CURRENT_SPELL_QUEUE_344.json"
CURRENT_HANDOFF = HERE / "CURRENT_HANDOFF_344.json"
CURRENT_PENDING = HERE / "CURRENT24_PENDING_IDENTITY_AUDIT_344.json"
TIMELESS_IDS = {
    "RANK9DEFENSEFORM8129-TIMELESS-FORM-A",
    "RANK9DEFENSEFORM8129-TIMELESS-FORM-A1-HASTE-PAID-COST",
    "RANK9DEFENSEFORM8129-TIMELESS-FORM-A2-BOTH-SLOW",
    "RANK9DEFENSEFORM8129-TIMELESS-FORM-B",
    "RANK9DEFENSEFORM8129-TIMELESS-FORM-COUNTER",
    "RANK9DEFENSEFORM8129-TIMELESS-FORM-GATE-access",
    "RANK9DEFENSEFORM8129-TIMELESS-FORM-GATE-components",
    "RANK9DEFENSEFORM8129-TIMELESS-FORM-GATE-range",
    "RANK9DEFENSEFORM8129-TIMELESS-FORM-GATE-resource",
    "RANK9DEFENSEFORM8129-TIMELESS-FORM-READY-EXPIRES",
    "RANK9DEFENSEFORM8129-TIMELESS-FORM-SUPPRESSION",
}
JOINT_CASES = {
    "TF318-345-ACTION-NATURAL": "cases/new/TF318-345-ACTION-NATURAL.json",
    "TF318-345-CLERIC-UNIVERSAL-NATURAL": "cases/new/TF318-345-CLERIC-UNIVERSAL-NATURAL.json",
    "TF318-345-ACTION-FAILED-THEN-INTERRUPTED": "cases/new/TF318-345-ACTION-FAILED-THEN-INTERRUPTED.json",
}


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def load(raw: bytes) -> Any:
    return json.loads(raw)


def read(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def file_bind(path: Path) -> dict[str, Any]:
    raw = path.read_bytes()
    return {
        "path": path.resolve().relative_to(REPO.resolve()).as_posix(),
        "bytes": len(raw),
        "sha256": sha(raw),
        "crc32": f"{zlib.crc32(raw) & 0xffffffff:08x}",
    }


def payload_files(z: zipfile.ZipFile) -> dict[str, bytes]:
    return {name: z.read(name) for name in z.namelist() if not name.endswith("/")}


def event_index(case: dict[str, Any], kind: str) -> list[tuple[int, dict[str, Any]]]:
    return [(i, e) for i, e in enumerate(case.get("events", [])) if e.get("kind") == kind]


def assert_event(case: dict[str, Any], kind: str) -> tuple[int, dict[str, Any]]:
    matches = event_index(case, kind)
    if len(matches) != 1:
        raise AssertionError(f"{case.get('id')}: expected one {kind}, found {len(matches)}")
    return matches[0]


def projected_case(payload: dict[str, bytes], case_id: str) -> dict[str, Any]:
    projection = load(payload["crosswalk/W345_TIMELESS_FORM_EVIDENCE_PROJECTION.json"])
    return next(case for case in projection["newJointCases"] if case["id"] == case_id)


def verify_joint_case(case: dict[str, Any], source_member: str, raw_member: bytes) -> list[tuple[str, bool, str]]:
    checks: list[tuple[str, bool, str]] = []
    case_id = case.get("id")
    checks.append((f"{case_id}-source-member-binding", True, f"{source_member}; {len(raw_member)} bytes; SHA-256 {sha(raw_member)}"))
    checks.append((f"{case_id}-conditional-not-campaign", case.get("status") == "DEMONSTRATED_CONDITIONAL_FIXTURE" and "DF218-B03" in case.get("holdIds", []), "W345 authors these as conditional review fixtures and retains DF218-B03 at build time."))
    initial = case.get("initialState", {})
    actors = initial.get("actors", {})
    p = actors.get("P", {})
    timeless_acq = [row for row in (p.get("candidateSpellAcquisitions") or []) if row.get("spellId") == "timeless-form"]
    checks.append((f"{case_id}-Timeless-Form-acquisition-boundary", bool(timeless_acq) and all("candidate-only" in row.get("status", "") for row in timeless_acq), "The Timeless Form acquisition is explicitly candidate-only; no real prior/campaign acquisition is claimed."))
    time_form_event = assert_event(case, "TIMELESS_FORM_CAST_COMMIT")[1]
    form_cast = next((c for c in initial.get("casts", []) if c.get("spellId") == "timeless-form"), None)
    if form_cast is None:
        form_cast = next((c for c in time_form_event.get("after", {}).get("casts", []) if c.get("spellId") == "timeless-form"), None)
    checks.append((f"{case_id}-Timeless-Form-paid-history", bool(form_cast) and form_cast.get("actualPaid") == 26 and form_cast.get("components") == ["V", "S", "F"] and form_cast.get("focusItemId") == "focus-P" and form_cast.get("budget") == "Action", "One 26-RP Action with V/S/F and carried focus-P is recorded."))
    resolution_i, resolution = assert_event(case, "TIMELESS_FORM_SURVIVING_CAST_RESOLUTION")
    tf_effect = resolution.get("after", {}).get("effects", {}).get("timeless-form-P", {})
    checks.append((f"{case_id}-Timeless-Form-original-effect", tf_effect.get("startedAtWorldMs") == 0 and tf_effect.get("originalDeadlineWorldMs") == 60000 and tf_effect.get("concentration") is False and "time-stop" in tf_effect.get("protections", []), "The source trace starts the nonconcentration 60,000-ms self-recipient expression before Time Stop."))
    tf_cast = next((c for c in resolution.get("after", {}).get("casts", []) if c.get("spellId") == "timeless-form"), None)
    ppos = p.get("position")
    c_actor_initial = actors.get("C", {})
    cpos = c_actor_initial.get("position")
    distance = None
    if isinstance(ppos, list) and isinstance(cpos, list) and len(ppos) == len(cpos) == 3:
        distance = sum((float(x) - float(y)) ** 2 for x, y in zip(ppos, cpos)) ** 0.5
    p_acquisition = next((row for row in timeless_acq if row.get("sourcePath") == "catalog.json#/spells/765/classAccess/Wizard"), None)
    checks.append((f"{case_id}-class-acquisition-and-geometry", tf_cast is not None and p.get("class") == "Wizard" and p.get("classLevel") == 17 and p_acquisition is not None and "timeless-form" in p.get("preparedRankedSpellIds", []) and distance == 50 and tf_cast.get("actor") == "P" and time_form_event.get("inputs", {}).get("target") == "P", "Wizard17 has the catalog-bound prepared candidate for a self-targeted Timeless Form; the Time Stop caster is 50 ft away."))
    # Keep source acquisition and route qualification explicit for both Time Stop modes.
    stop_commit_i, stop_commit = assert_event(case, "PAID_TIME_STOP_COMMIT")
    stop_cast = next((c for c in stop_commit.get("after", {}).get("casts", []) if c.get("spellId") == "time-stop"), None)
    c_acquisitions = [row for row in (c_actor_initial.get("candidateSpellAcquisitions") or []) if row.get("spellId") == "time-stop"]
    route_ok = bool(stop_cast) and bool(c_acquisitions) and all("candidate-only" in row.get("status", "") for row in c_acquisitions)
    route = stop_commit.get("inputs", {}).get("mode")
    route_ok &= c_actor_initial.get("classLevel") == 17
    route_ok &= c_actor_initial.get("class") == ("Cleric" if case_id == "TF318-345-CLERIC-UNIVERSAL-NATURAL" else "Wizard")
    route_ok &= stop_cast.get("actualPaid") == 26 and stop_cast.get("components") == ["V", "S", "F"] and stop_cast.get("focusItemId") == "focus-C"
    route_ok &= stop_cast.get("budget") == ("Reaction" if route == "Universal" else "Action")
    checks.append((f"{case_id}-Time-Stop-source-and-paid-route", route_ok, f"Source-qualified {c_actor_initial.get('class')}17 candidate route records 26 RP, V/S/F, focus-C and the actual {route} budget; acquisition remains candidate-only."))
    order_ok = stop_commit_i > resolution_i
    form_counter = assert_event(case, "TIMELESS_FORM_COUNTER_WINDOW")[0]
    time_stop_counter = assert_event(case, "COUNTER_WINDOW_DECISION")[0]
    open_index = assert_event(case, "TIME_STOP_OPEN")[0]
    order_ok &= form_counter < resolution_i < stop_commit_i < time_stop_counter < open_index
    counter_event = case["events"][time_stop_counter]
    order_ok &= counter_event.get("inputs", {}).get("responder") == "P" and counter_event.get("inputs", {}).get("eligible") is True and counter_event.get("inputs", {}).get("decision") == "decline"
    checks.append((f"{case_id}-counter-and-commit-order", order_ok, "Timeless Form resolves after its counter window; Time Stop commits, offers the real responder window, then opens."))
    prior_effects = [actor.get("concentration") for actor in actors.values() if actor.get("concentration")]
    concentration_source_ok = len(prior_effects) == (2 if case_id != "TF318-345-CLERIC-UNIVERSAL-NATURAL" else 1) and all(x.get("status") == "active" and x.get("sourcePath") == "wizard.json#/cards/21" for x in prior_effects)
    checks.append((f"{case_id}-prior-concentration-source", concentration_source_ok, "The pre-existing paid Arcane Sight concentration source is identified and active; Timeless Form is nonconcentration."))

    stop_i, stop_event = assert_event(case, "TIME_STOP_OPEN")
    interval = stop_event.get("after", {}).get("world", {}).get("temporalInterval", {})
    anchor = interval.get("worldAnchorMs")
    stop_mode = interval.get("mode")
    checks.append((f"{case_id}-Time-Stop-global-pause", stop_event.get("after", {}).get("world", {}).get("paused") is True and anchor == stop_event.get("inputs", {}).get("worldAnchorMs"), f"Accepted Time Stop opens one global pause at {anchor} ms ({stop_mode})."))
    time_form_during = stop_event.get("after", {}).get("effects", {}).get("timeless-form-P", {})
    checks.append((f"{case_id}-Timeless-Form-excluded-effect-retained", time_form_during.get("status") == "active" and time_form_during.get("originalDeadlineWorldMs") == 60000, "The effect remains active and its original absolute deadline is unchanged across pause open."))
    wallets = interval.get("ordinaryWallet", {})
    wallet_ok = wallets.get("P", {}).get("Action") == 0 and wallets.get("P", {}).get("Reaction") == 1
    if interval.get("mode") == "Action":
        wallet_ok &= wallets.get("C", {}).get("Action") == 0 and wallets.get("C", {}).get("Reaction") == 1
    else:
        wallet_ok &= wallets.get("C", {}).get("Reaction") == 0
    checks.append((f"{case_id}-ordinary-action-reaction-wallets-retained", wallet_ok, "The exact ordinary wallets remain in the paused interval; spent Actions and the Universal Reaction are not refreshed."))

    # No event may move the global world cursor while the accepted Time Stop interval remains open.
    paused_rows = []
    unchanged_snapshots = True
    open_actors = stop_event.get("after", {}).get("actors", {})
    for event in case.get("events", [])[stop_i:]:
        state = event.get("after", {})
        world = state.get("world", {})
        if world.get("paused") is not True:
            break
        paused_rows.append((event.get("id"), world.get("nowMs")))
        current_interval = world.get("temporalInterval", {})
        unchanged_snapshots &= current_interval.get("ordinaryWallet") == wallets
        for actor_id, actor in state.get("actors", {}).items():
            prior = open_actors.get(actor_id, {})
            unchanged_snapshots &= actor.get("regularStarts") == prior.get("regularStarts")
            unchanged_snapshots &= actor.get("regularEnds") == prior.get("regularEnds")
            unchanged_snapshots &= actor.get("ready") == prior.get("ready")
            unchanged_snapshots &= actor.get("concentration") == prior.get("concentration")
            refresh_history = actor.get("reactionRefreshHistory")
            unchanged_snapshots &= refresh_history == prior.get("reactionRefreshHistory")
            for recharge in (actor.get("recharge") or {}).values():
                if isinstance(recharge, dict):
                    unchanged_snapshots &= recharge.get("ticksDuringPersonalTurns", 0) == 0
    checks.append((f"{case_id}-paused-world-cursor", bool(paused_rows) and all(now == anchor for _, now in paused_rows), f"All {len(paused_rows)} paused event snapshots retain world cursor {anchor} ms."))
    checks.append((f"{case_id}-pause-preserves-clocks-and-state", unchanged_snapshots, "Across every active personal phase, the ordinary wallets, regular markers, Ready, concentration and Reaction-refresh history stay unchanged; recharge has zero personal-turn ticks."))

    # Natural movement and legal interruption are separate branches; neither rewrites the other.
    movements = event_index(case, "IMMUNE_PEER_INDEPENDENT_MOVEMENT")
    if case_id == "TF318-345-ACTION-NATURAL":
        paid_i, paid = stop_commit_i, stop_commit
        checks.append((f"{case_id}-Action-mode-payment-and-route", paid.get("inputs", {}).get("actor") == "C" and paid.get("inputs", {}).get("mode") == "Action" and paid.get("inputs", {}).get("baseRP") == 26 and paid.get("inputs", {}).get("d4") == 1 and paid.get("inputs", {}).get("turnsGranted") == 2, "Wizard/Illusion Action route pays once; the authored d4=1 grants two personal rounds."))
        checks.append((f"{case_id}-immune-peer-independent-agency", len(movements) == 2 and all(e.get("inputs", {}).get("actor") == "P" for _, e in movements), "The immune recipient takes two actual movement actions during separate personal phases."))
    elif case_id == "TF318-345-CLERIC-UNIVERSAL-NATURAL":
        trigger = assert_event(case, "UNIVERSAL_REACTION_TRIGGER")[1]
        paid = assert_event(case, "PAID_TIME_STOP_COMMIT")[1]
        checks.append((f"{case_id}-Universal-trigger-and-reaction", trigger.get("inputs", {}).get("distanceFeet") == 50 and trigger.get("inputs", {}).get("loE") is True and trigger.get("inputs", {}).get("beforeNextAtomicEvent") is True and paid.get("inputs", {}).get("mode") == "Universal" and paid.get("inputs", {}).get("turnsGranted") == 3, "Perceived 50-ft trigger opens the Cleric Universal Reaction route for exactly three turns."))
        checks.append((f"{case_id}-immune-peer-independent-agency", len(movements) == 3 and all(e.get("inputs", {}).get("actor") == "P" for _, e in movements), "The immune recipient takes three actual movement actions during separate personal phases."))
    else:
        dispels = event_index(case, "ARCH_DISPEL_CHECK_AND_EFFECT_RESOLUTION")
        outcomes = [event.get("inputs", {}).get("expected") for _, event in dispels]
        checks.append((f"{case_id}-failed-then-successful-removal", len(dispels) == 2 and outcomes == ["failure", "success"] and dispels[0][1].get("after", {}).get("world", {}).get("paused") is True and dispels[1][1].get("after", {}).get("world", {}).get("paused") is False, "The failed paid removal leaves the interval active; the later successful captured-source Dispel closes it."))
        checks.append((f"{case_id}-remaining-personal-turn-count", len(movements) == 0, "This branch tests failed removal and successful interruption, not another natural movement completion."))

    natural_closes = event_index(case, "TIME_STOP_NATURAL_CLOSE")
    resumed = event_index(case, "REGULAR_TURN_RESUMED_AND_ENDED")
    checks.append((f"{case_id}-exactly-once-resumption", len(resumed) == 1 and (len(natural_closes) == 1 or case_id.endswith("FAILED-THEN-INTERRUPTED")), "The saved ordinary slot resumes and closes exactly once; natural-close branches close only after all included personal phases."))
    deadline_i, deadline_event = assert_event(case, "TIMELESS_FORM_ORIGINAL_DEADLINE")
    deadline_effect = deadline_event.get("after", {}).get("effects", {}).get("timeless-form-P", {})
    checks.append((f"{case_id}-deadline-and-expiry", deadline_event.get("inputs", {}).get("deadlineWorldMs") == 60000 and deadline_event.get("after", {}).get("world", {}).get("nowMs") == 60000 and deadline_effect.get("originalDeadlineWorldMs") == 60000 and deadline_effect.get("expiredAtWorldMs") == 60000, "The effect expires at the original 60,000-ms world deadline, without extension or reset."))
    queue = case.get("ordinaryTurnQueue", [])
    checks.append((f"{case_id}-regular-slot-conservation", len(queue) == 20 and all(s.get("startCount") == s.get("endCount") == 1 for s in queue) and sorted(s.get("queueOrder", -1) for s in queue) == list(range(1, 21)), "All 20 ordered ordinary slots have one START and one END; personal phases add no regular slots."))
    checks.append((f"{case_id}-concentration-and-ready-preserved", all(a.get("concentration", {}).get("status") == "active" for a in case.get("finalState", {}).get("actors", {}).values() if a.get("concentration")) and all(a.get("ready") is None or a.get("ready", {}).get("status") in {"held", "released", "expired"} for a in case.get("finalState", {}).get("actors", {}).values()), "Active Arcane Sight remains source-bound; no invalid Ready state is created or cleared."))
    return checks


def main() -> int:
    failures: list[str] = []
    checks: list[dict[str, Any]] = []

    def check(name: str, passed: bool, detail: str) -> None:
        checks.append({"id": name, "passed": bool(passed), "detail": detail})
        if not passed:
            failures.append(f"{name}: {detail}")

    if not ARCHIVE.is_file():
        print(f"Missing archive: {ARCHIVE}")
        return 2
    archive_bytes = ARCHIVE.read_bytes()
    archive_sha = sha(archive_bytes)
    try:
        with zipfile.ZipFile(ARCHIVE) as z:
            corrupt = z.testzip()
            infos = z.infolist()
            names = [i.filename for i in infos]
            safe = all(not name.startswith(("/", "\\")) and ".." not in Path(name).parts for name in names)
            payload = payload_files(z)
    except Exception as exc:
        print(f"Invalid closure ZIP: {exc}")
        return 2
    check("archive-zip-integrity", corrupt is None, "ZIP testzip passed." if corrupt is None else str(corrupt))
    check("archive-member-paths", safe and len(names) == len(set(names)), "Member paths are safe and unique." if safe and len(names) == len(set(names)) else "Unsafe or duplicate ZIP member path.")

    manifest = load(payload["MEMBER_MANIFEST.json"])
    rows = manifest.get("members", [])
    listed = {row["path"]: row for row in rows}
    actual_nonmanifest = {name: raw for name, raw in payload.items() if name != "MEMBER_MANIFEST.json"}
    allowlist_ok = set(listed) == set(actual_nonmanifest)
    hashes_ok = allowlist_ok and all(
        len(actual_nonmanifest[name]) == row["bytes"] and sha(actual_nonmanifest[name]) == row["sha256"] and f"{zlib.crc32(actual_nonmanifest[name]) & 0xffffffff:08x}" == row["crc32"]
        for name, row in listed.items()
    )
    check("payload-allowlist-and-member-hashes", manifest.get("memberCountExcludingSelf") == len(rows) and allowlist_ok and hashes_ok, f"{len(rows)} payload members bound; every size/SHA/CRC reconciles." if allowlist_ok and hashes_ok else "Payload allowlist or member hashes do not reconcile.")

    crosswalk = load(payload["crosswalk/TIMELESS_FORM_DF218_B03_POSITIVE_CROSSWALK.json"])
    projection = load(payload["crosswalk/W345_TIMELESS_FORM_EVIDENCE_PROJECTION.json"])
    queue = read(CURRENT_QUEUE)
    handoff = read(CURRENT_HANDOFF)
    pending = read(CURRENT_PENDING)
    authority = queue.get("currentAuthority", {})
    check("current-authority-and-queue", authority == handoff.get("currentAuthority") == pending.get("authority") and authority.get("reviewedApplied") == 824 and authority.get("pending") == 24 and authority.get("acceptedUnapplied") == 0 and handoff.get("closureTasksRemaining") == 24 and handoff.get("firstReviewTasksRemaining") == 0 and "timeless-form" in pending.get("pendingIds", []) and "time-stop" not in pending.get("pendingIds", []), f"Queue344 is 824/24/0, 24 closure, 0 first-review; Timeless Form is pending and Time Stop is applied.")
    check("crosswalk-current-authority-binding", crosswalk.get("currentAuthority") == authority and crosswalk.get("queueBindings", {}).get("closureTasksRemaining") == 24 and crosswalk.get("queueBindings", {}).get("pendingIdsContainTimelessForm") is True, "Crosswalk points at current Queue344 authority, not stale Return308 baseline.")

    accepted = read(HERE / "TIME_STOP_WITNESS345_ACCEPTANCE.json")
    applied = read(HERE / "TIME_STOP_WITNESS345_APPLICATION.json")
    proc = read(REPO / "DescentReviewChanges/ReviewBible/data/public/spell_candidates/rank9timestop_reviewed_345/PROCEDURE_RECORD.json")
    with zipfile.ZipFile(W345) as source:
        w345_outer = W345.read_bytes()
        outer_delivery = read(W345_DELIVERY)
        w345_projection_bind = projection.get("sourceArchive", {})
        w345_bound = w345_projection_bind.get("sha256") == sha(w345_outer) and w345_projection_bind.get("bytes") == len(w345_outer)
        check("accepted-time-stop-and-source-binding", accepted.get("acceptedIds") == ["time-stop"] and applied.get("appliedIds") == ["time-stop"] and applied.get("closedBlockerIds") == ["TF192-B01"] and proc.get("spellId") == "time-stop" and w345_bound and outer_delivery.get("archive", {}).get("sha256") == sha(w345_outer), "W345 acceptance/application and exact r6 archive bind; only TF192-B01 is closed.")
        check("time-stop-scope-and-runtime-boundary", any("DF218-B03 remains open" in row for row in accepted.get("retainedQualifications", [])) and applied.get("sourceStatusPreservedAsBlocked") is True and applied.get("runtimeSelectionEnabled") is False and applied.get("implementationApproved") is False, "Time Stop's static authored scope and disabled runtime boundary are retained.")

        historical = crosswalk["historicalPreservation"]
        old_copy_ok = True
        with zipfile.ZipFile(OLD) as old:
            old_bindings = {row["member"]: row for row in historical.get("caseBindings", [])}
            copied_names = [name for name in payload if name.startswith("history/Return218/preserved_cases/") and name.endswith(".json")]
            if len(copied_names) != 11 or set(old_bindings) != {f"cases/{Path(name).name}" for name in copied_names}:
                old_copy_ok = False
            for payload_name in copied_names:
                raw = payload[payload_name]
                old_member = f"cases/{Path(payload_name).name}"
                if old_member not in old.namelist() or raw != old.read(old_member) or sha(raw) != old_bindings.get(old_member, {}).get("sha256"):
                    old_copy_ok = False
            held_member = "cases/RANK9DEFENSEFORM8129-TIMELESS-FORM-B.json"
            old_held = json.loads(old.read(held_member))
        check("eleven-historical-cases-byte-exact", old_copy_ok, "All 11 Return308 Timeless Form cases are unchanged byte-for-byte in the closure package." if old_copy_ok else "Historical case bytes/count differ from Return308.")
        old_event4 = old_held["events"][4]
        check("historical-hold-remains-unrewritten", old_event4.get("kind") == "Time-Stop-access/procedure-held" and historical.get("event4RemainsHeld") is True and historical.get("noHistoricalHOLDRewrite") is True, "Return308 B event 4 remains the exact historical HOLD evidence; the positive proof is appended separately.")

        actual_case_members = {name for name in source.namelist() if name.startswith("cases/new/") and name.endswith(".json")}
        check("exact-three-joint-cases", actual_case_members == set(JOINT_CASES.values()) and len(projection.get("newJointCases", [])) == 3, "Projection references exactly the three accepted W345 r6 joint cases.")
        projected_sources = {row.get("member"): row for row in projection.get("newJointCases", [])}
        all_case_bytes_match = True
        for case_id, member in JOINT_CASES.items():
            raw = source.read(member)
            src_case = load(raw)
            proj = projected_sources.get(member)
            if proj is None or proj.get("id") != case_id or proj.get("memberSha256") != sha(raw) or proj.get("memberBytes") != len(raw):
                all_case_bytes_match = False
                continue
            recomputed = verify_joint_case(src_case, member, raw)
            for name, passed, detail in recomputed:
                check(name, passed, detail)
                if not passed:
                    all_case_bytes_match = False
        check("projection-cases-bind-original-members", all_case_bytes_match, "The compact evidence projection binds each untouched full W345 case member by byte length and SHA-256." if all_case_bytes_match else "At least one projected joint case does not match its original W345 member or an independent semantic check failed.")

        ready_hashes = {row.get("member"): row for row in projection.get("ReadySourceCases", [])}
        ready_ok = True
        for member in [
            "cases/preserved/RANK9TIMEFATE6129-TIME-STOP-B__ready-release-exact.json",
            "cases/preserved/RANK9TIMEFATE6129-TIME-STOP-B__ready-expiry-exact.json",
        ]:
            raw = source.read(member)
            case = load(raw)
            if ready_hashes.get(member, {}).get("sha256") != sha(raw):
                ready_ok = False
            if "ready-release" in member:
                ready_ok &= len(event_index(case, "REAL_READY_RELEASE")) == 1 and len(event_index(case, "STOP_OPEN")) == 1
            else:
                ready_events = [(i, e) for i, e in enumerate(case.get("events", [])) if e.get("kind") == "SOURCE_CLOCK" and (e.get("after", {}).get("actors", {}).get("W", {}).get("ready") or {}).get("status") == "expired"]
                ready_ok &= len(ready_events) >= 1 and ready_events[-1][1]["after"]["actors"]["W"]["ready"].get("expiresMs") == 6000
        check("ready-lifecycle-support-and-limit", ready_ok and "combinedBranchStatus" in crosswalk.get("clockLifecycleReconciliation", {}).get("readyCrosswalk", {}), "Source-bound W345 Ready release/expiry cases are intact; combined Ready+Timeless Form interaction is explicitly declared untested.")

    check("disclosed-cross-products", len(crosswalk.get("identifiedUncoveredOrConditionalBranches", [])) >= 4 and all(row.get("status") for row in crosswalk.get("identifiedUncoveredOrConditionalBranches", [])), "Candidate acquisition, Ready/Haste/Slow co-occurrence, and longer Action d4 branches are disclosed for Director disposition.")
    check("no-acceptance-or-application-claimed", crosswalk.get("noApplicationAuthorization") is True and crosswalk.get("decisionRequested", "").startswith("Director review only") and crosswalk.get("acceptedTimeStopBinding", {}).get("appliedIds") == ["time-stop"], "This packet requests no Timeless Form acceptance/application; the previous Time Stop application is bound only as dependency.")

    passed = sum(1 for row in checks if row["passed"])
    failures_count = len(checks) - passed
    status = "PASS_WITH_DECLARED_LIMITS" if failures_count == 0 else "FAIL"
    review = {
        "id": "TIMELESS-FORM-CLOSURE346-INDEPENDENT-REVIEW",
        "status": status,
        "scope": "Static structural/source and semantic review of the Timeless Form / DF218-B03 closure submission. No acceptance, application, runtime execution, campaign authentication, or human play is claimed.",
        "archive": {"path": str(ARCHIVE), "bytes": len(archive_bytes), "sha256": archive_sha, "crc32": f"{zlib.crc32(archive_bytes) & 0xffffffff:08x}"},
        "authority": authority,
        "checkCount": len(checks),
        "passedChecks": passed,
        "failedChecks": failures_count,
        "checks": checks,
        "identifiedUncoveredOrConditionalBranches": crosswalk.get("identifiedUncoveredOrConditionalBranches", []),
        "decisionStatus": {"acceptedIds": [], "appliedIds": [], "heldIds": ["timeless-form"], "blockerIds": ["DF218-B03"], "applicationAuthorized": False},
        "errors": failures,
    }
    review_path = OUT / "TIMELESS_FORM_CLOSURE346_INDEPENDENT_REVIEW.json"
    review_path.write_text(json.dumps(review, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    replay = {
        "id": "TIMELESS-FORM-CLOSURE346-GENERATOR-REPLAY",
        "status": status,
        "archiveSha256": archive_sha,
        "checks": [
            {"caseId": name, "member": member, "sha256": projected_sources.get(member, {}).get("memberSha256"), "checks": sum(1 for row in checks if row["id"].startswith(name))}
            for name, member in JOINT_CASES.items()
        ],
        "preservedHistoricalTimelessFormCases": 11,
        "projectedW345JointCases": 3,
        "forwardInverseReplayedHere": False,
        "replayBoundary": "Full W345 forward/inverse replay remains bound to its already accepted r6 independent review; this review reopens source snapshots and semantic event fields, not a rewritten or re-executed game runtime.",
    }
    replay_path = OUT / "TIMELESS_FORM_CLOSURE346_GENERATOR_REPLAY.json"
    replay_path.write_text(json.dumps(replay, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    delivery = {
        "id": "TIMELESS-FORM-CLOSURE346-DELIVERY",
        "status": status,
        "scopeIds": ["timeless-form"],
        "blockerIds": ["DF218-B03"],
        "acceptedIds": [],
        "appliedIds": [],
        "heldIds": ["timeless-form"],
        "applicationAuthorized": False,
        "authority": authority,
        "archive": {"fileName": ARCHIVE.name, "bytes": len(archive_bytes), "sha256": archive_sha, "crc32": f"{zlib.crc32(archive_bytes) & 0xffffffff:08x}"},
        "independentReview": file_bind(review_path),
        "generatorReplay": file_bind(replay_path),
        "payloadMemberCount": len(payload),
        "preservedTimelessFormHistoricalCases": 11,
        "referencedW345JointCases": 3,
        "runtimeSelectionEnabled": False,
        "canonicalFilesChanged": False,
    }
    delivery_path = OUT / "DD_Rank9_TimelessForm_DF218B03_Closure346_DELIVERY.json"
    delivery_path.write_text(json.dumps(delivery, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(json.dumps({"status": status, "checks": f"{passed}/{len(checks)}", "failed": failures_count, "archiveSha256": archive_sha, "delivery": str(delivery_path)}, indent=2))
    if failures_count:
        print("\n".join(failures))
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
