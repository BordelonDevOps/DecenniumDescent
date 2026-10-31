from __future__ import annotations

import collections
import hashlib
import json
import pathlib
import re
import zipfile
import zlib
from typing import Any


ROOT = pathlib.Path(__file__).resolve().parents[5]
AUDIT = pathlib.Path(__file__).resolve().parent
RETURN318 = AUDIT / "rank9_time_stop_return318_received"
BUILD = AUDIT / "rank9_time_stop_joint_witness_345_build_output_r3"
DELIVERY = AUDIT / "rank9_time_stop_joint_witness_345_delivery_r3"
SOURCES = {
    "catalog": ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json",
    "index": ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json",
    "core": ROOT / "DescentReviewChanges/ReviewBible/data/public/Decennium_Descent_Core_Systems_Data_v2_Known_Descent.json",
    "spells": ROOT / "DescentReviewChanges/ReviewBible/src/data/spells.js",
    "placements": ROOT / "DescentReviewChanges/ReviewBible/src/data/spell-placements.json",
    "wizard": ROOT / "DescentReviewChanges/ReviewBible/data/public/class_playtests/wizard.json",
    "cleric": ROOT / "DescentReviewChanges/ReviewBible/data/public/class_playtests/cleric.json",
    "integration": ROOT / "DescentReviewChanges/ReviewBible/docs/mechanics/SPELL_INTEGRATION_RULES.md",
    "combat": ROOT / "DescentReviewChanges/ReviewBible/docs/mechanics/COMBAT_ACTION_PLAYTEST.md",
    "ancestry_background": ROOT / "DescentReviewChanges/ReviewBible/docs/mechanics/ANCESTRY_BACKGROUND_SOURCE_BINDINGS.md",
}
SOURCE_MEMBER = {
    "catalog": "evidence/sources/catalog.json",
    "index": "evidence/sources/authored_review_index.json",
    "core": "evidence/sources/Decennium_Descent_Core_Systems_Data_v2_Known_Descent.json",
    "spells": "evidence/sources/spells.js",
    "placements": "evidence/sources/spell-placements.json",
    "wizard": "evidence/sources/class_playtests/wizard.json",
    "cleric": "evidence/sources/class_playtests/cleric.json",
    "integration": "evidence/sources/SPELL_INTEGRATION_RULES.md",
    "combat": "evidence/sources/COMBAT_ACTION_PLAYTEST.md",
    "ancestry_background": "evidence/sources/ANCESTRY_BACKGROUND_SOURCE_BINDINGS.md",
}
EXPECTED_CASES = {
    "TF318-345-ACTION-NATURAL.json": "natural-completion-action-mode",
    "TF318-345-CLERIC-UNIVERSAL-NATURAL.json": "natural-completion-cleric-universal",
    "TF318-345-ACTION-FAILED-THEN-INTERRUPTED.json": "failed-removal-then-successful-legal-interruption",
}
EXPECTED_BOOK_COUNTS = {1: 7, 2: 2, 3: 2, 4: 2, 5: 3, 6: 3, 7: 3, 8: 3,
                        9: 4, 10: 4, 11: 4, 12: 4, 13: 5, 14: 5, 15: 5, 16: 5, 17: 6}
WARD_TYPES = ("acid", "cold", "fire", "force", "lightning", "necrotic", "psychic", "radiant", "thunder")


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def crc(raw: bytes) -> str:
    return f"{zlib.crc32(raw) & 0xffffffff:08x}"


def canonical(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def load(path: pathlib.Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def check(checks: list[dict[str, Any]], name: str, condition: bool, detail: str) -> None:
    checks.append({"id": name, "passed": bool(condition), "detail": detail})


def replay_case(case: dict[str, Any]) -> tuple[bool, str]:
    state = json.loads(json.dumps(case["initialState"]))
    forward_count = inverse_count = 0

    def apply(value: dict[str, Any], operations: list[dict[str, Any]]) -> dict[str, Any]:
        result = json.loads(json.dumps(value))
        for operation in operations:
            if operation.get("path") != "":
                raise ValueError("non-root patch is outside this witness schema")
            if operation["op"] == "test":
                if canonical(result) != canonical(operation["value"]):
                    raise ValueError("test precondition failed")
            elif operation["op"] == "replace":
                result = json.loads(json.dumps(operation["value"]))
            else:
                raise ValueError(f"unknown patch operation {operation['op']}")
        return result

    for event in case["events"]:
        before, after = event["before"], event["after"]
        if canonical(state) != canonical(before):
            return False, f"{event['id']}: forward continuity failed"
        if sha(canonical(before)) != event["beforeSHA256"] or sha(canonical(after)) != event["afterSHA256"]:
            return False, f"{event['id']}: state digest mismatch"
        state = apply(state, event["forward"])
        if canonical(state) != canonical(after):
            return False, f"{event['id']}: forward patch mismatch"
        if canonical(apply(state, event["inverse"])) != canonical(before):
            return False, f"{event['id']}: inverse patch mismatch"
        forward_count += len(event["forward"])
        inverse_count += len(event["inverse"])
    if canonical(state) != canonical(case["finalState"]):
        return False, "final forward replay mismatch"
    reverse = json.loads(json.dumps(case["finalState"]))
    for event in reversed(case["events"]):
        reverse = apply(reverse, event["inverse"])
    if canonical(reverse) != canonical(case["initialState"]):
        return False, "full reverse replay mismatch"
    if forward_count != inverse_count:
        return False, "forward/inverse operation counts differ"
    return True, f"{len(case['events'])} events, {forward_count} forward and {inverse_count} inverse operations"


def expected_ward(catalog: dict[str, Any], actor: dict[str, Any]) -> str:
    spells = {row["id"]: row for row in catalog["spells"]}
    school = actor["schoolBonuses"]["selectedSchool"]
    observed: set[str] = set()
    for spell_id in actor["preparedRankedSpellIds"]:
        spell = spells[spell_id]
        if spell.get("classAccess", {}).get("Wizard", {}).get("school") != school:
            continue
        text = " ".join(entry.get("original", {}).get("effect", "")
                         for entry in spell.get("source", {}).get("coreEntries", [])).lower()
        observed.update(element for element in WARD_TYPES if element in text)
    return next((element for element in WARD_TYPES if element in observed), "force")


def main() -> int:
    checks: list[dict[str, Any]] = []
    errors: list[str] = []
    try:
        zip_path = DELIVERY / "DD_Rank9_TimeStop_TF318_Witness345.zip"
        delivery_path = DELIVERY / "DD_Rank9_TimeStop_TF318_Witness345_DELIVERY.json"
        zip_raw = zip_path.read_bytes()
        delivery_raw = delivery_path.read_bytes()
        delivery = json.loads(delivery_raw)
        catalog = load(SOURCES["catalog"])
        wizard_source = load(SOURCES["wizard"])
        spell_index = {row["id"]: index for index, row in enumerate(catalog["spells"])}
        spell_rows = {row["id"]: row for row in catalog["spells"]}

        check(checks, "delivery-identity", delivery.get("id") == "TIME-STOP-TF318-WITNESS345-DELIVERY" and delivery.get("reviewId") == "Witness345",
              "Delivery record names only Witness345.")
        check(checks, "authority-unchanged", delivery.get("authority") == {"reviewedApplied": 823, "pending": 25,
              "acceptedUnapplied": 0, "completeStandaloneProcedures": 547, "scopedInterfaces": 173},
              "Authority remains 823 applied, 25 pending, 0 accepted-unapplied.")
        check(checks, "no-application-claim", delivery.get("acceptedIds") == [] and delivery.get("appliedIds") == [] and
              delivery.get("applicationAuthorized") is False and delivery.get("canonicalFilesChanged") is False,
              "No identity was accepted/applied and no canonical spell file was changed.")
        archive_record = delivery.get("archive", {})
        check(checks, "archive-binding", archive_record.get("sha256") == sha(zip_raw) and archive_record.get("bytes") == len(zip_raw) and
              archive_record.get("crc32") == crc(zip_raw), "Delivery JSON binds the exact ZIP bytes.")

        with zipfile.ZipFile(zip_path) as archive:
            names = archive.namelist()
            check(checks, "archive-no-duplicate-members", len(names) == len(set(names)), "ZIP contains unique member paths.")
            check(checks, "archive-no-unsafe-paths", all(not pathlib.PurePosixPath(name).is_absolute() and ".." not in pathlib.PurePosixPath(name).parts for name in names),
                  "ZIP member paths are relative and remain inside the archive.")
            member_bytes = {name: archive.read(name) for name in names}
        manifest = json.loads(member_bytes["MEMBER_MANIFEST.json"])
        expected_names = set(manifest["exactPayloadAllowlist"]) | {"MEMBER_MANIFEST.json"}
        check(checks, "manifest-allowlist", set(names) == expected_names and manifest.get("memberCount") == len(names),
              "Every ZIP member is present in the exact payload allowlist and no extra member exists.")
        member_rows = {row["path"]: row for row in manifest["members"]}
        integrity_ok = True
        for name in manifest["exactPayloadAllowlist"]:
            raw = member_bytes[name]
            row = member_rows.get(name, {})
            integrity_ok &= row.get("bytes") == len(raw) and row.get("sha256") == sha(raw) and row.get("crc32") == crc(raw)
        check(checks, "member-checksums", integrity_ok, "Each allowlisted payload member matches its recorded size, SHA-256, and CRC32.")

        preserved = sorted((RETURN318 / "cases").glob("*.json"))
        preserved_actual = sorted(name for name in names if name.startswith("cases/preserved/"))
        preserved_ok = len(preserved) == 14 and len(preserved_actual) == 14
        if preserved_ok:
            source_by_name = {path.name: path.read_bytes() for path in preserved}
            preserved_ok = all(member_bytes["cases/preserved/" + name] == raw for name, raw in source_by_name.items())
        check(checks, "fourteen-preserved-cases-byte-exact", preserved_ok,
              "All fourteen Return318 cases are preserved byte-exact.")

        source_snapshots_ok = True
        actor_bindings = json.loads(member_bytes["ACTOR_AND_SOURCE_BINDINGS.json"])
        binding_rows = {row["path"]: row for row in actor_bindings.get("sourceBindings", [])}
        for key, source_path in SOURCES.items():
            member_path = SOURCE_MEMBER[key]
            raw = source_path.read_bytes()
            row = binding_rows.get(source_path.relative_to(ROOT).as_posix(), {})
            source_snapshots_ok &= member_bytes[member_path] == raw and row.get("bytes") == len(raw) and row.get("sha256") == sha(raw)
        check(checks, "current-source-bindings", source_snapshots_ok,
              "All ten included current source snapshots match the working tree and actor binding manifest.")

        cases: dict[str, dict[str, Any]] = {}
        for name, expected_branch in EXPECTED_CASES.items():
            member_name = "cases/new/TF318-345-" + name.removeprefix("TF318-345-")
            # The member name equals the filename under cases/new.
            member_name = "cases/new/" + name
            case_raw = member_bytes[member_name]
            case = json.loads(case_raw)
            disk_case = (BUILD / "cases" / name).read_bytes()
            same_case = case_raw == disk_case and case.get("branch") == expected_branch
            check(checks, "case-" + name, same_case, f"{name} is the branch-bound generated case.")
            cases[name] = case
            replay_ok, replay_detail = replay_case(case)
            check(checks, "replay-" + name, replay_ok, replay_detail)

        expected_case_names = {"cases/new/" + name for name in EXPECTED_CASES}
        check(checks, "exact-new-case-count", {name for name in names if name.startswith("cases/new/")} == expected_case_names,
              "The archive contains exactly the three requested new conditional branches.")
        schema_ok = all(cases[name]["initialState"].get("fixtureMode") == "AUTHORED_CONDITIONAL_REVIEW_FIXTURE_ONLY" and
                        cases[name].get("status") == "DEMONSTRATED_CONDITIONAL_FIXTURE" for name in EXPECTED_CASES)
        check(checks, "conditional-fixture-boundary", schema_ok,
              "Every new branch is explicitly a conditional review fixture, not campaign or runtime evidence.")

        wizard_checks_ok = True
        progression_ok = True
        spellbook_source_ok = True
        for case_name, case in cases.items():
            for actor_id, actor in case["finalState"]["actors"].items():
                if actor["class"] != "Wizard":
                    wizard_checks_ok &= actor.get("HP", {}).get("max") == actor.get("hp") == actor.get("maxHP") == 105
                    continue
                book = actor.get("spellbook") or []
                ids = [row.get("id") for row in book]
                counts = collections.Counter(row.get("acquiredAtClassLevel") for row in book)
                wizard_checks_ok &= len(book) == 67 and len(set(ids)) == 67 and all(row.get("rank", 0) >= 1 for row in book)
                wizard_checks_ok &= actor.get("knownRankedSpellIds") == ids
                wizard_checks_ok &= counts == collections.Counter(EXPECTED_BOOK_COUNTS)
                wizard_checks_ok &= len(actor.get("knownCantripIds", [])) == 5 and not (set(ids) & set(actor["knownCantripIds"]))
                wizard_checks_ok &= all(spell_rows.get(cantrip, {}).get("classAccess", {}).get("Wizard", {}).get("rank") == 0
                                        for cantrip in actor.get("knownCantripIds", []))
                wizard_checks_ok &= (len(actor.get("preparedRankedSpellIds", [])) == 22 and
                    len(set(actor["preparedRankedSpellIds"])) == 22 and set(actor["preparedRankedSpellIds"]) <= set(ids))
                history = actor.get("preparationHistory", [{}])[0]
                wizard_checks_ok &= (history.get("durationMinutes") == 45 and history.get("matrixEfficiencyApplied") is True and
                    history.get("preparedRankedSpellIds") == actor["preparedRankedSpellIds"])
                cantrip_history = actor.get("knownCantripAcquisitionHistory", [])
                wizard_checks_ok &= [(row.get("classLevel"), len(row.get("spellIds", []))) for row in cantrip_history] == [(1, 3), (4, 1), (10, 1)]
                auto = {row.get("id"): row for row in actor.get("automaticFeatures", [])}
                expected_auto_levels = {"wizard.base.counterspell": 2, "wizard.supplement.ritual-casting": 2,
                    "wizard.supplement.school-mastery": 5, "wizard.supplement.arcane-ward": 6, "wizard.supplement.dual-cast": 9}
                wizard_checks_ok &= all(auto.get(card_id, {}).get("acquiredAtClassLevel") == level for card_id, level in expected_auto_levels.items())
                wizard_checks_ok &= auto.get("wizard.supplement.dual-cast", {}).get("invoked") is False
                wizard_checks_ok &= actor.get("schoolBonuses", {}).get("spellAttackBonus") == 2 and actor.get("schoolBonuses", {}).get("spellSaveDCBonus") == 2
                wizard_checks_ok &= actor.get("abilityCheckBonuses", {}).get("dispelMagic") == 1
                wizard_checks_ok &= ({"wizard.arch.arcane-sight", "wizard.arch.dispel-magic", "wizard.base.counterspell"} <=
                    {row.get("cardId") for row in actor.get("alwaysPreparedClassMatrices", [])})
                wizard_checks_ok &= "divinationFailedSaveReroll" not in actor.get("finiteUses", {})
                expected_resistance = expected_ward(catalog, actor)
                wizard_checks_ok &= actor.get("resistances") == [expected_resistance] and actor.get("arcaneWardChoice", {}).get("damageType") == expected_resistance

                known = set(ids)
                for row in book:
                    access = spell_rows.get(row["id"], {}).get("classAccess", {}).get("Wizard", {})
                    max_rank = min(9, (row["acquiredAtClassLevel"] + 1) // 2)
                    progression_ok &= access.get("minimumClassLevel", 99) <= row["acquiredAtClassLevel"] and row["rank"] <= max_rank
                    spellbook_source_ok &= row.get("sourcePath") == f"catalog.json#/spells/{spell_index[row['id']]}/classAccess/Wizard"
                school_bonus = [row for row in book if row.get("acquisitionKind") == "arcane-school-specialization-bonus-spell"]
                progression_ok &= (len(school_bonus) == 1 and school_bonus[0].get("rank") == 1 and
                    school_bonus[0].get("school") == actor["schoolBonuses"]["selectedSchool"])
                target_id = actor.get("candidateSpellAcquisitions", [{}])[0].get("spellId")
                candidate = actor.get("candidateSpellAcquisitions", [{}])[0]
                spellbook_source_ok &= (target_id in known and candidate.get("sourcePath") ==
                    f"catalog.json#/spells/{spell_index[target_id]}/classAccess/Wizard")
        check(checks, "wizard-repertoires-features-and-preparation", wizard_checks_ok,
              "Wizard spellbooks, cantrips, preparation, automatic features, school bonuses, class matrices, and Arcane Ward state are internally and source-consistent.")
        check(checks, "spellbook-level-and-school-progression", progression_ok,
              "All ranked spell additions meet source rank/level gates and the separate level-one school bonus is legal.")
        check(checks, "catalog-array-pointer-provenance", spellbook_source_ok,
              "Spell acquisition provenance uses actual catalog array indices for each identity.")

        ordering_ok = True
        cast_semantics_ok = True
        perception_ok = True
        clock_ok = True
        custody_ok = True
        for case_name, case in cases.items():
            kinds = [event["kind"] for event in case["events"]]
            tf = [kinds.index("TIMELESS_FORM_CAST_COMMIT"), kinds.index("TIMELESS_FORM_COUNTER_WINDOW"),
                  kinds.index("TIMELESS_FORM_SURVIVING_CAST_RESOLUTION")]
            ts = [kinds.index("PAID_TIME_STOP_COMMIT"), kinds.index("COUNTER_WINDOW_DECISION"), kinds.index("TIME_STOP_OPEN")]
            ordering_ok &= tf == sorted(tf) and ts == sorted(ts)
            opened = case["events"][kinds.index("TIME_STOP_OPEN")]
            anchor = opened["after"]["world"]["temporalInterval"]["worldAnchorMs"]
            clock_ok &= opened["inputs"].get("worldAnchorMs") == anchor == opened["after"]["clockLedger"][-1].get("worldAnchorMs")
            expected_anchor = 0 if "UNIVERSAL" in case_name else 100
            clock_ok &= anchor == expected_anchor
            final = case["finalState"]
            source = final["effects"].get("timeless-form-P", {})
            clock_ok &= source.get("originalDeadlineWorldMs") == 60000 and source.get("expiredAtWorldMs") == 60000
            clock_ok &= final["world"].get("ordinaryRound") == 10
            for actor_id, actor in final["actors"].items():
                custody_ok &= final["items"][f"focus-{actor_id}"]["position"] == actor["position"]
                custody_ok &= actor.get("regularStarts", []) == actor.get("regularSchedule", {}).get("startMarkersMs", [])
                custody_ok &= actor.get("regularEnds", []) == actor.get("regularSchedule", {}).get("endMarkersMs", [])
                for record in actor.get("reactionRefreshHistory", []):
                    clock_ok &= record.get("after") == 1 and record.get("sourcePath") == "COMBAT_ACTION_PLAYTEST.md#L35"
            for snapshot in [case["initialState"]] + [event["after"] for event in case["events"]] + [final]:
                for actor_id in ("C", "P"):
                    custody_ok &= snapshot["items"][f"focus-{actor_id}"]["position"] == snapshot["actors"][actor_id]["position"]
            casts = final["casts"]
            tf_cast = next((row for row in casts if row.get("spellId") == "timeless-form"), {})
            ts_cast = next((row for row in casts if row.get("spellId") == "time-stop"), {})
            cast_semantics_ok &= tf_cast.get("baseDissonanceApplied") == 0
            cast_semantics_ok &= ts_cast.get("baseDissonanceApplied") == (2 if ts_cast.get("actor") == "C" and final["actors"]["C"]["class"] == "Cleric" else 0)
            for actor_id in ("C", "P"):
                actor = final["actors"][actor_id]
                if actor["class"] == "Wizard":
                    cast_semantics_ok &= all(row.get("baseDissonanceApplied") == 0 for row in casts if row.get("actor") == actor_id and
                        row.get("spellId") in ("time-stop", "timeless-form", "wizard.arch.dispel-magic"))
            temporal_events = [event for event in case["events"] if event["kind"] in
                ("PERSONAL_PHASE_START", "PERSONAL_PHASE_END", "IMMUNE_PEER_MOVEMENT")]
            for event in temporal_events:
                clock_ok &= event["after"]["clockLedger"][-1].get("worldTimeMs") == anchor
            if case["branch"].startswith("natural"):
                close_idx = kinds.index("TIME_STOP_NATURAL_CLOSE")
                last_peer_end = max(i for i, event in enumerate(case["events"]) if event["kind"] == "PERSONAL_PHASE_END" and
                                    event["inputs"].get("actor") == "P")
                ordering_ok &= close_idx > last_peer_end and kinds[-1] == "TIMELESS_FORM_ORIGINAL_DEADLINE"
            else:
                detections = [event for event in case["events"] if event["kind"] == "ARCANE_SIGHT_DETECTS_TIME_STOP"]
                commits = [event for event in case["events"] if event["kind"] == "ARCH_DISPEL_CAST_COMMIT"]
                windows = [event for event in case["events"] if event["kind"].startswith("DISPEL_COUNTERSPELL_WINDOW_")]
                resolutions = [event for event in case["events"] if event["kind"] == "ARCH_DISPEL_CHECK_AND_EFFECT_RESOLUTION"]
                perception_ok &= len(detections) == len(commits) == len(windows) == len(resolutions) == 2
                for event in detections:
                    record = event["after"]["perception"]["perceivedEffects"][-1]
                    route = record.get("perceptionRoute", {})
                    observer = record.get("observer")
                    arcane = event["after"]["effects"].get(f"arcane-sight-{observer}", {})
                    concentration = event["after"]["actors"][observer].get("concentration") or {}
                    perception_ok &= record.get("perceivedBeforeActionCommit") is True and record.get("distanceFeet", 999) <= 60
                    perception_ok &= route.get("sourceCardId") == "wizard.arch.arcane-sight" and route.get("paidRP") == 2
                    perception_ok &= route.get("remainingMsAtPerception", 0) > 0 and route.get("activeConcentration") is True
                    perception_ok &= arcane.get("status") == "active" and concentration.get("id") == arcane.get("applicationId")
                for commit, window, resolution in zip(commits, windows, resolutions):
                    cast_semantics_ok &= commit["after"]["casts"][-1].get("spellRank") == 3 and commit["after"]["casts"][-1].get("targetEffectRank") == 9
                    ordering_ok &= case["events"].index(commit) < case["events"].index(window) < case["events"].index(resolution)
                    cast_semantics_ok &= resolution["after"]["casts"][-1].get("check", {}).get("modifier") is None
                rolls = [event["after"]["casts"][-1]["check"] for event in resolutions]
                cast_semantics_ok &= ([(row.get("die"), row.get("total"), row.get("outcome")) for row in rolls] ==
                    [(1, 13, "failure"), (8, 20, "success")])
                cast_semantics_ok &= all(row.get("sigilAuthorityBonus") == 1 and row.get("DC") == 19 for row in rolls)
                failed = next(event for event in resolutions if event["inputs"]["expected"] == "failure")
                succeeded = next(event for event in resolutions if event["inputs"]["expected"] == "success")
                cast_semantics_ok &= failed["after"]["world"]["temporalInterval"] is not None
                cast_semantics_ok &= failed["after"]["actors"]["P"]["recharge"]["wizard.arch.dispel-magic"]["roundsRemaining"] == 2
                cast_semantics_ok &= succeeded["after"]["world"]["temporalInterval"] is None
        check(checks, "cast-commit-counter-resolution-order", ordering_ok,
              "Timeless Form, Time Stop, and both Dispel casts resolve only after their eligible interruption windows.")
        check(checks, "paid-source-bound-perception", perception_ok,
              "Both Dispel attempts have active, paid, concentration-bound Arcane Sight detection before Action commitment.")
        check(checks, "dissonance-and-dispel-math", cast_semantics_ok,
              "Wizard first-family casts apply zero base Dissonance; Cleric Time Stop applies ordinary base strain; Dispel ranks and checks are correct.")
        check(checks, "world-clock-and-reaction-refresh", clock_ok,
              "World anchors, regular schedules, round progression, and source-bound Reaction refreshes are consistent.")
        check(checks, "focus-custody-follows-position", custody_ok,
              "Both carried focus positions remain bound to their custodians through every snapshot.")

        check(checks, "generator-replay-audit", delivery.get("newCasesReplayPassed") is True and
              delivery.get("preservedTimeStopCaseCount") == 14 and delivery.get("newConditionalCaseCount") == 3,
              "Delivery records three replayed new cases and fourteen preserved cases.")
    except Exception as error:  # Preserve an actionable report even when an unexpected schema fault occurs.
        errors.append(f"{type(error).__name__}: {error}")

    passed = not errors and all(row["passed"] for row in checks)
    report = {"id": "TIME-STOP-TF318-WITNESS345-INDEPENDENT-REVIEW", "status": "PASS" if passed else "FAIL",
        "checks": checks, "errors": errors, "authority": {"reviewedApplied": 823, "pending": 25, "acceptedUnapplied": 0},
        "archive": {"fileName": "DD_Rank9_TimeStop_TF318_Witness345.zip", "sha256": sha((DELIVERY / "DD_Rank9_TimeStop_TF318_Witness345.zip").read_bytes()),
                    "bytes": (DELIVERY / "DD_Rank9_TimeStop_TF318_Witness345.zip").stat().st_size},
        "applicationPerformed": False, "canonicalFilesChanged": False}
    report_path = DELIVERY / "TIME_STOP_TF318_WITNESS345_INDEPENDENT_REVIEW.json"
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": report["status"], "checks": len(checks),
        "failedChecks": [row["id"] for row in checks if not row["passed"]], "errors": errors,
        "report": str(report_path)}, indent=2))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
