from __future__ import annotations

import hashlib
import json
import zipfile
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
REPO = HERE.parents[4]
OUT = HERE / "rank9_timeless_form_closure_346_delivery"
PAYLOAD = OUT / "payload"
OLD_ZIP = HERE / "rank9_defenseform8_return308_received" / "DD_Rank9_DefenseForm8_Director_Return308_HELD.zip"
W345_DIR = HERE / "rank9_time_stop_joint_witness_345_delivery_r6"
W345_ZIP = W345_DIR / "DD_Rank9_TimeStop_TF318_Witness345.zip"
W345_DELIVERY = W345_DIR / "DD_Rank9_TimeStop_TF318_Witness345_DELIVERY.json"
CURRENT = HERE
SPELL_DATA = REPO / "DescentReviewChanges/ReviewBible/data/public/spell_playtests"
CLASS_DATA = REPO / "DescentReviewChanges/ReviewBible/data/public/class_playtests"
TIMESTOP_PACKAGE = REPO / "DescentReviewChanges/ReviewBible/data/public/spell_candidates/rank9timestop_reviewed_345"
TIMELESS_PACKAGE = REPO / "DescentReviewChanges/ReviewBible/data/public/spell_candidates/rank9defenseform8_reviewed_218/DIRECTOR_RETURN"

OLD_CASES = [
    "RANK9DEFENSEFORM8129-TIMELESS-FORM-A.json",
    "RANK9DEFENSEFORM8129-TIMELESS-FORM-A1-HASTE-PAID-COST.json",
    "RANK9DEFENSEFORM8129-TIMELESS-FORM-A2-BOTH-SLOW.json",
    "RANK9DEFENSEFORM8129-TIMELESS-FORM-B.json",
    "RANK9DEFENSEFORM8129-TIMELESS-FORM-COUNTER.json",
    "RANK9DEFENSEFORM8129-TIMELESS-FORM-GATE-access.json",
    "RANK9DEFENSEFORM8129-TIMELESS-FORM-GATE-components.json",
    "RANK9DEFENSEFORM8129-TIMELESS-FORM-GATE-range.json",
    "RANK9DEFENSEFORM8129-TIMELESS-FORM-GATE-resource.json",
    "RANK9DEFENSEFORM8129-TIMELESS-FORM-READY-EXPIRES.json",
    "RANK9DEFENSEFORM8129-TIMELESS-FORM-SUPPRESSION.json",
]
W345_NEW_CASES = [
    "TF318-345-ACTION-NATURAL.json",
    "TF318-345-CLERIC-UNIVERSAL-NATURAL.json",
    "TF318-345-ACTION-FAILED-THEN-INTERRUPTED.json",
]
W345_PRESERVED_READY = [
    "RANK9TIMEFATE6129-TIME-STOP-B__ready-release-exact.json",
    "RANK9TIMEFATE6129-TIME-STOP-B__ready-expiry-exact.json",
]


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def file_bytes(path: Path) -> bytes:
    return path.read_bytes()


def rel(path: Path) -> str:
    return path.resolve().relative_to(REPO.resolve()).as_posix()


def bind(path: Path) -> dict[str, Any]:
    raw = file_bytes(path)
    import zlib

    return {"path": rel(path), "bytes": len(raw), "sha256": sha256(raw), "crc32": f"{zlib.crc32(raw) & 0xffffffff:08x}"}


def write_member(name: str, raw: bytes) -> None:
    path = PAYLOAD / Path(name)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(raw)


def copy_member(name: str, source: Path) -> None:
    write_member(name, file_bytes(source))


def json_member(name: str, value: Any) -> bytes:
    raw = (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    write_member(name, raw)
    return raw


def zip_read(archive: zipfile.ZipFile, name: str) -> bytes:
    if name not in archive.namelist():
        raise RuntimeError(f"Missing source archive member: {name}")
    return archive.read(name)


def selected_records(records: Any, spell_ids: set[str]) -> list[dict[str, Any]]:
    if not isinstance(records, list):
        return []
    return [record for record in records if isinstance(record, dict) and record.get("spellId") in spell_ids]


def actor_slice(actor: dict[str, Any], state: dict[str, Any]) -> dict[str, Any]:
    spell_ids = {"timeless-form", "time-stop"}
    prep_rows = []
    for row in actor.get("preparationHistory", []) or []:
        prepared = [sid for sid in row.get("preparedRankedSpellIds", []) if sid in spell_ids]
        if prepared:
            prep_rows.append({
                "sourcePath": row.get("sourcePath"),
                "completedAfterLongRest": row.get("completedAfterLongRest"),
                "durationMinutes": row.get("durationMinutes"),
                "preparationLimit": row.get("preparationLimit"),
                "preparedRelevantSpellIds": prepared,
                "candidateFixtureOnly": row.get("candidateFixtureOnly"),
            })
    book_rows = [row for row in actor.get("spellbook", []) or [] if row.get("id") in spell_ids]
    acquisition_rows = [row for row in actor.get("spellbookAcquisitionHistory", []) or [] if row.get("spellId") in spell_ids]
    candidate_rows = [row for row in actor.get("candidateSpellAcquisitions", []) or [] if row.get("spellId") in spell_ids]
    resource_rows = selected_records(actor.get("resourceHistory"), spell_ids)
    items = state.get("items", {})
    focus_ids = sorted({
        row.get("focusItemId") for row in resource_rows if row.get("focusItemId")
    })
    focus_rows = {item_id: items.get(item_id) for item_id in focus_ids}
    return {
        "id": actor.get("id"),
        "class": actor.get("class"),
        "classLevel": actor.get("classLevel"),
        "classPath": actor.get("classPath"),
        "profileId": actor.get("profileId"),
        "position": actor.get("position"),
        "spellAccessSource": actor.get("spellAccessSource"),
        "spellbookRelevantRows": book_rows,
        "preparedRelevantSpellIds": [sid for sid in actor.get("preparedRankedSpellIds", []) or [] if sid in spell_ids],
        "preparationHistory": prep_rows,
        "spellbookAcquisitionHistory": acquisition_rows,
        "candidateSpellAcquisitions": candidate_rows,
        "castResourceHistory": resource_rows,
        "focusItems": focus_rows,
        "budget": actor.get("budget"),
        "ready": actor.get("ready"),
        "concentration": actor.get("concentration"),
        "recharge": actor.get("recharge"),
        "regularSchedule": actor.get("regularSchedule"),
        "regularStarts": actor.get("regularStarts"),
        "regularEnds": actor.get("regularEnds"),
        "personalTurnCasts": actor.get("personalTurnCasts"),
        "reactionRefreshHistory": actor.get("reactionRefreshHistory"),
    }


def interval_slice(interval: Any) -> Any:
    if not isinstance(interval, dict):
        return interval
    keys = [
        "source", "mode", "d4", "turnsGranted", "turnsUsed", "worldAnchorMs", "endWorldMs",
        "ordinaryWallet", "originalRegularMarkers", "ordinaryClockCursor", "clockLedger",
        "pausedSourceDeadlines", "personalPhaseHistory", "caster", "immunePeer", "immuneParticipants",
    ]
    return {key: interval.get(key) for key in keys if key in interval}


def state_slice(state: dict[str, Any]) -> dict[str, Any]:
    world = state.get("world", {})
    effects = state.get("effects", {})
    relevant_effects = {
        key: value for key, value in effects.items()
        if isinstance(value, dict) and value.get("spellId") in {"timeless-form", "time-stop"}
    }
    return {
        "world": {
            "nowMs": world.get("nowMs"),
            "ordinaryRound": world.get("ordinaryRound"),
            "paused": world.get("paused"),
            "temporalInterval": interval_slice(world.get("temporalInterval")),
        },
        "timelessAndTimeStopEffects": relevant_effects,
        "actors": {actor_id: actor_slice(actor, state) for actor_id, actor in state.get("actors", {}).items()},
    }


def event_projection(case: dict[str, Any], member: str, source_hash: str, source_bytes: int) -> dict[str, Any]:
    snapshots = []
    for index, event in enumerate(case.get("events", [])):
        snapshots.append({
            "index": index,
            "pointer": f"/events/{index}",
            "id": event.get("id"),
            "kind": event.get("kind"),
            "inputs": event.get("inputs"),
            "narrative": event.get("narrative"),
            "beforeSHA256": event.get("beforeSHA256"),
            "afterSHA256": event.get("afterSHA256"),
            "afterState": state_slice(event.get("after", {})) if event.get("kind") in {
                "TIMELESS_FORM_CAST_COMMIT", "TIMELESS_FORM_SURVIVING_CAST_RESOLUTION", "UNIVERSAL_REACTION_TRIGGER",
                "PAID_TIME_STOP_COMMIT", "COUNTER_WINDOW_DECISION", "TIME_STOP_OPEN", "PERSONAL_PHASE_START",
                "IMMUNE_PEER_INDEPENDENT_MOVEMENT", "PERSONAL_PHASE_END", "ARCH_DISPEL_CHECK_AND_EFFECT_RESOLUTION",
                "TIME_STOP_NATURAL_CLOSE", "REGULAR_TURN_RESUMED_AND_ENDED", "REGULAR_START", "REGULAR_END",
                "TIMELESS_FORM_ORIGINAL_DEADLINE",
            } else None,
        })
    initial = case.get("initialState", {})
    return {
        "id": case.get("id"),
        "member": member,
        "memberBytes": source_bytes,
        "memberSha256": source_hash,
        "status": case.get("status"),
        "branch": case.get("branch"),
        "requirementIds": case.get("requirementIds"),
        "holdIdsAtAuthoring": case.get("holdIds"),
        "scenarioPremise": case.get("scenarioPremise"),
        "initialActors": {actor_id: actor_slice(actor, initial) for actor_id, actor in initial.get("actors", {}).items()},
        "initialTimelessFormEffects": {
            key: value for key, value in initial.get("effects", {}).items()
            if isinstance(value, dict) and value.get("spellId") == "timeless-form"
        },
        "events": snapshots,
        "ordinaryTurnQueue": case.get("ordinaryTurnQueue"),
        "counts": case.get("counts"),
    }


def build() -> dict[str, Any]:
    PAYLOAD.mkdir(parents=True, exist_ok=True)
    (OUT / "README.md").write_text(
        "# Timeless Form / DF218-B03 closure submission (346)\n\n"
        "This packet asks the Director to review only the changed-evidence closure for Timeless Form / DF218-B03. "
        "It binds the accepted and statically applied W345 Time Stop procedure to the existing conditional joint traces, "
        "adds a positive crosswalk, and carries the 11 Return308 Timeless Form cases byte-for-byte. "
        "The packet itself does not accept or apply Timeless Form. Candidate-only acquisition, retained qualifications, "
        "and possible missing combined branches are stated explicitly.\n\n"
        "Current authority: Queue344, 824 applied / 24 pending / 0 accepted-unapplied; 0 first-review identities / "
        "24 closure tasks; 548 complete standalone procedures / 173 scoped interfaces.\n\n"
        "The source W345 archive is the exact r6 artifact already attached earlier in this Director thread and is "
        "bound by SHA-256 in the crosswalk. The projection is a derived view only; it does not modify W345 cases.\n",
        encoding="utf-8",
    )
    write_member("README.md", (OUT / "README.md").read_bytes())

    # Current authority and the prior hold/requirements.
    for name in ["CURRENT_HANDOFF_344.json", "CURRENT_SPELL_QUEUE_344.json", "CURRENT24_PENDING_IDENTITY_AUDIT_344.json"]:
        copy_member(f"evidence/authority/{name}", HERE / name)
    for name in [
        "TIMELESS_FORM_DIRECTOR_DECISION_308.json",
        "TIMELESS_FORM_DIRECTOR_REQUIREMENTS_308.json",
        "TIMELESS_FORM_RETURN308_INDEPENDENT_AUDIT.json",
    ]:
        copy_member(f"evidence/prior/{name}", HERE / name)
    copy_member("evidence/timeless_form/PROCEDURE_RECORD_218.json", TIMELESS_PACKAGE / "procedures/timeless-form.json")

    # Bind Q20/Q21/Q22 without rewriting the source file or any prior case.
    qpath = TIMELESS_PACKAGE / "QUESTION_DISPOSITIONS.json"
    qsource = read_json(qpath)
    questions = qsource.get("questions", [])
    selected_questions = [q for q in questions if q.get("id") in {"DF9-Q20", "DF9-Q21", "DF9-Q22"}]
    if {q.get("id") for q in selected_questions} != {"DF9-Q20", "DF9-Q21", "DF9-Q22"}:
        raise RuntimeError("Expected DF9-Q20/Q21/Q22 dispositions are absent")
    json_member("evidence/timeless_form/QUESTION_DISPOSITIONS_DF9_Q20_Q22.json", {
        "source": bind(qpath),
        "questions": selected_questions,
    })

    # Accepted Time Stop source, acceptance, application, contract and source snapshots.
    for name in [
        "TIME_STOP_WITNESS345_ACCEPTANCE.json",
        "TIME_STOP_WITNESS345_APPLICATION.json",
        "TIME_STOP_WITNESS345_APPLICATION_VALIDATION.json",
        "TIME_STOP_WITNESS345_DIRECTOR_DECISION.json",
        "TIME_STOP_WITNESS345_INDEX_OPERATIONS.json",
        "TIME_STOP_WITNESS345_RECEIPT.json",
    ]:
        copy_member(f"evidence/time_stop/{name}", HERE / name)
    for name in ["PROCEDURE_RECORD.json", "MODEL.json", "CASE_COVERAGE.json", "EVIDENCE_BINDINGS.json", "CANDIDATE_PACKAGE_MANIFEST.json"]:
        copy_member(f"evidence/time_stop/rank9timestop_reviewed_345/{name}", TIMESTOP_PACKAGE / name)
    copy_member("evidence/time_stop/W345_DELIVERY.json", W345_DELIVERY)
    copy_member("evidence/time_stop/W345_INDEPENDENT_REVIEW.json", W345_DIR / "TIME_STOP_TF318_WITNESS345_INDEPENDENT_REVIEW.json")
    copy_member("evidence/time_stop/W345_GENERATOR_REPLAY.json", W345_DIR / "TIME_STOP_TF318_WITNESS345_GENERATOR_REPLAY.json")
    with zipfile.ZipFile(W345_ZIP) as w345:
        for source_member, target in [
            ("ACTOR_AND_SOURCE_BINDINGS.json", "evidence/time_stop/ACTOR_AND_SOURCE_BINDINGS.json"),
            ("evidence/TF318_JOINT_INTERFACE_CONTRACT.md", "evidence/time_stop/TF318_JOINT_INTERFACE_CONTRACT.md"),
            ("evidence/TF318_DIRECTOR_SCOPE.json", "evidence/time_stop/TF318_DIRECTOR_SCOPE.json"),
            ("evidence/JOINT_INTERFACE_AUTHORIZATION.json", "evidence/time_stop/JOINT_INTERFACE_AUTHORIZATION.json"),
        ]:
            write_member(target, zip_read(w345, source_member))

    # Rebind current source state and exact class data after W345 application.
    for name in ["authored_review_index.json", "catalog.json"]:
        copy_member(f"evidence/current/{name}", SPELL_DATA / name)
    core = REPO / "DescentReviewChanges/ReviewBible/data/public/Decennium_Descent_Core_Systems_Data_v2_Known_Descent.json"
    copy_member("evidence/current/Decennium_Descent_Core_Systems_Data_v2_Known_Descent.json", core)
    for class_name in ["wizard", "cleric", "druid", "mage"]:
        copy_member(f"evidence/current/class_playtests/{class_name}.json", CLASS_DATA / f"{class_name}.json")
    for name in ["COMBAT_ACTION_PLAYTEST.md", "SPELL_INTEGRATION_RULES.md"]:
        with zipfile.ZipFile(W345_ZIP) as w345:
            source_member = f"evidence/sources/{name}"
            write_member(f"evidence/current/{name}", zip_read(w345, source_member))

    # Preserve Return308's 11 historical Timeless Form cases byte-exact.
    old_case_bindings = []
    with zipfile.ZipFile(OLD_ZIP) as old:
        old_names = {f"cases/{name}" for name in OLD_CASES}
        present = {name for name in old.namelist() if name in old_names}
        if present != old_names:
            raise RuntimeError(f"Historical Timeless Form case set mismatch: {sorted(old_names - present)}")
        for name in OLD_CASES:
            member = f"cases/{name}"
            raw = zip_read(old, member)
            write_member(f"history/Return218/preserved_cases/{name}", raw)
            old_case_bindings.append({"member": member, "bytes": len(raw), "sha256": sha256(raw)})

    # Build derived projections from unchanged W345 cases and exact member hashes.
    projected_cases = []
    with zipfile.ZipFile(W345_ZIP) as w345:
        for filename in W345_NEW_CASES:
            member = f"cases/new/{filename}"
            raw = zip_read(w345, member)
            case = json.loads(raw)
            if sha256(raw) != sha256(zip_read(w345, member)):
                raise RuntimeError(f"Unstable W345 case read: {member}")
            projected_cases.append(event_projection(case, member, sha256(raw), len(raw)))
        ready_cases = []
        for filename in W345_PRESERVED_READY:
            member = f"cases/preserved/{filename}"
            raw = zip_read(w345, member)
            ready_cases.append({"member": member, "bytes": len(raw), "sha256": sha256(raw)})
        old_witness_member = "cases/RANK9DEFENSEFORM8129-TIMELESS-FORM-B.json"
        old_witness = json.loads(zip_read(zipfile.ZipFile(OLD_ZIP), old_witness_member))
        old_event = old_witness["events"][4]
        w345_member_hashes = {
            f"cases/new/{filename}": {
                "bytes": w345.getinfo(f"cases/new/{filename}").file_size,
                "sha256": sha256(zip_read(w345, f"cases/new/{filename}")),
            }
            for filename in W345_NEW_CASES
        }

    projection = {
        "id": "TIMELESS-FORM-W345-POSITIVE-INTERFACE-PROJECTION-346",
        "sourceArchive": bind(W345_ZIP),
        "sourceMemberHashes": w345_member_hashes,
        "newJointCases": projected_cases,
        "ReadySourceCases": ready_cases,
        "oldHeldCaseEvent": {
            "archive": bind(OLD_ZIP),
            "member": old_witness_member,
            "caseId": old_witness.get("id"),
            "eventPointer": "/events/4",
            "event": old_event,
            "sha256OfPreservedCase": sha256(zip_read(zipfile.ZipFile(OLD_ZIP), old_witness_member)),
        },
        "projectionBoundary": "Derived pointer-and-state view only; source W345 and Return308 cases are not rewritten.",
    }
    projection_raw = json_member("crosswalk/W345_TIMELESS_FORM_EVIDENCE_PROJECTION.json", projection)

    accepted = read_json(HERE / "TIME_STOP_WITNESS345_ACCEPTANCE.json")
    application = read_json(HERE / "TIME_STOP_WITNESS345_APPLICATION.json")
    q = read_json(HERE / "CURRENT_SPELL_QUEUE_344.json")
    h = read_json(HERE / "CURRENT_HANDOFF_344.json")
    p = read_json(HERE / "CURRENT24_PENDING_IDENTITY_AUDIT_344.json")
    time_stop_proc_path = TIMESTOP_PACKAGE / "PROCEDURE_RECORD.json"
    time_stop_proc = read_json(time_stop_proc_path)
    current_index = read_json(SPELL_DATA / "authored_review_index.json")
    raw_entries = current_index.get("entries", {})
    index_entries = raw_entries if isinstance(raw_entries, dict) else {row.get("id"): row for row in raw_entries}
    question_map = {x["id"]: x for x in selected_questions}
    q20, q21, q22 = question_map["DF9-Q20"], question_map["DF9-Q21"], question_map["DF9-Q22"]

    crosswalk = {
        "id": "TIMELESS-FORM-DF218-B03-POSITIVE-CROSSWALK-346",
        "identity": "timeless-form",
        "blockerIds": ["DF218-B03"],
        "decisionRequested": "Director review only; no acceptance, application, or canonical mutation is requested as part of this packet.",
        "currentAuthority": q.get("currentAuthority"),
        "queueBindings": {
            "queue344": bind(HERE / "CURRENT_SPELL_QUEUE_344.json"),
            "handoff344": bind(HERE / "CURRENT_HANDOFF_344.json"),
            "pendingAudit344": bind(HERE / "CURRENT24_PENDING_IDENTITY_AUDIT_344.json"),
            "closureTasksRemaining": h.get("closureTasksRemaining"),
            "firstReviewTasksRemaining": h.get("firstReviewTasksRemaining"),
            "pendingIdsContainTimelessForm": "timeless-form" in p.get("pendingIds", []),
            "timeStopRemovedFromPending": "time-stop" not in p.get("pendingIds", []),
        },
        "directorInstructions": {
            "sourceConversation": "Review Time Stop Witness Evidence",
            "sourceUrl": "https://chatgpt.com/g/g-p-67f17555a8dc8191a2b5b81e6d8adc12-dungeon-crawler/c/6ae5c784-afec-83e9-a2ca-5e2638b95750",
            "bindingCommit": "200a8d569e548c9bd7bd7e4d016e46ce7e089636",
            "requirements": [
                "Bind to rank9timestop_reviewed_345/PROCEDURE_RECORD.json, W345 acceptance/application records, and TF318-JOINT-INTERFACE-01; preserve Time Stop's limited scope and qualifications.",
                "Reuse W345 r6 qualified actors and paid histories through exact class, repertoire/preparation, component/focus, resource, Action/Reaction, interruption, geometry, and prior-effect pointers; keep Timeless Form acquisition explicitly contingent on its own review.",
                "Crosswalk DF9-Q20/Q21/Q22 and held Return308 case event 4; reference the three W345 joint cases where they satisfy obligations and identify any uncovered branch.",
                "Reconcile Return308's 'without ... paused clocks' wording with TF318's authorized world-clock pause; show independent agency, regular turns, Reaction, recharge, Ready, concentration, retained expenditures, exactly-once resumption, and the original 60,000-ms deadline.",
                "Preserve all 11 historical Timeless Form cases byte-exact and append positive crosswalk evidence without rewriting historical HOLD evidence.",
            ],
        },
        "priorTimelessFormHold": {
            "decision": bind(HERE / "TIMELESS_FORM_DIRECTOR_DECISION_308.json"),
            "requirements": bind(HERE / "TIMELESS_FORM_DIRECTOR_REQUIREMENTS_308.json"),
            "heldCase": "history/Return218/preserved_cases/RANK9DEFENSEFORM8129-TIMELESS-FORM-B.json#/events/4",
            "oldEventFinding": "Time-Stop-access/procedure-held; not a positive interaction.",
            "oldAuthoritySupersededByQueue344": True,
        },
        "timelessFormSourceAndAcquisition": {
            "priorProcedure": bind(TIMELESS_PACKAGE / "procedures/timeless-form.json"),
            "questionDispositions": bind(qpath),
            "currentIndexEntry": index_entries.get("timeless-form"),
            "classAccess": {"classes": ["Druid", "Mage", "Wizard"], "school": "Transmutation", "rank": 9, "minimumClassLevel": 17, "baseRpCost": 26, "castingTime": "Action", "components": "V/S/F", "nativeRangeFeet": 120},
            "selectedBehaviorPreserved": {"target": "one actually willing perceived creature within 120ft/LoE, including self", "durationMs": 60000, "concentration": False},
            "candidateAcquisitionOnly": True,
            "noPriorOrCampaignAcquisitionClaim": True,
        },
        "acceptedTimeStopBinding": {
            "procedureRecord": bind(time_stop_proc_path),
            "procedureId": time_stop_proc.get("id"),
            "procedureStatus": time_stop_proc.get("status"),
            "acceptance": bind(HERE / "TIME_STOP_WITNESS345_ACCEPTANCE.json"),
            "application": bind(HERE / "TIME_STOP_WITNESS345_APPLICATION.json"),
            "acceptedIds": accepted.get("acceptedIds"),
            "appliedIds": application.get("appliedIds"),
            "closedBlockerIds": application.get("closedBlockerIds"),
            "runtimeSelectionEnabled": index_entries.get("time-stop", {}).get("runtimeSelectionEnabled"),
            "sourceStatus": index_entries.get("time-stop", {}).get("sourceStatus"),
            "scopeBoundary": "Time Stop / TF192-B01 only; Timeless Form / DF218-B03 remains open; runtime remains disabled; all unrelated holds unchanged.",
        },
        "jointWitnesses": [
            {"caseId": row["id"], "archiveMember": row["member"], "bytes": row["memberBytes"], "sha256": row["memberSha256"], "status": row["status"], "holdIdsAtAuthoring": row["holdIdsAtAuthoring"]}
            for row in projected_cases
        ],
        "questionCrosswalk": [
            {
                "questionId": "DF9-Q20",
                "retainedDisposition": q20.get("disposition"),
                "TimeStopJointEvidence": [
                    "ACTION-NATURAL: event 3 establishes the self-recipient's active 60,000-ms Timeless Form expression before Time Stop; event 8 opens accepted global pause; events 12 and 17 show independent movement; event 57 ends the expression at its original 60,000-ms world deadline.",
                    "CLERIC-UNIVERSAL-NATURAL: events 3-7 establish the same order for the actual Universal Reaction route; events 11/16/21 show independent movement; event 63 ends at the same original deadline.",
                ],
                "priorAgingAndNoClockPauseByTimelessForm": "Return218 selected aging behavior remains carried unchanged; the new pause belongs to accepted Time Stop's single-world scheduler, not to Timeless Form. No aging reversal, rest, healing, recharge, lifespan, or permanent benefit is added.",
            },
            {
                "questionId": "DF9-Q21",
                "retainedDisposition": q21.get("disposition"),
                "TimeStopJointEvidence": [
                    "W345 preserves the existing paid/cast budgets and spends no Reaction or recharge solely by entering personal phases; the original Timeless Form payment and Time Stop payment remain in resource histories.",
                    "The existing Return218 Haste-paid-cost, both-Slow, and suppression cases remain byte-exact and continue to govern Q21. The new W345 joint traces do not instantiate an active Haste or Slow effect and are not offered as new Haste/Slow branch proof.",
                ],
            },
            {
                "questionId": "DF9-Q22",
                "retainedDisposition": q22.get("disposition"),
                "TimeStopJointEvidence": [
                    "ACTION-NATURAL covers Wizard/Illusion Action mode, actual 50-ft geometry, two personal rounds, and natural close.",
                    "CLERIC-UNIVERSAL-NATURAL covers a perceived Action trigger at 50 ft, the exact Universal Reaction route, three personal rounds, and natural close.",
                    "ACTION-FAILED-THEN-INTERRUPTED covers a failed Dispel that leaves Time Stop in force followed by a successful source-qualified Dispel, exactly-once resumption, and the unchanged Timeless Form deadline.",
                ],
            },
        ],
        "clockLifecycleReconciliation": {
            "proposedInterpretationForDirector": "Return308's 'without ... paused clocks' means Timeless Form itself does not pause unrelated clocks or grant a clock exception. Under the subsequently accepted TF318 Time Stop procedure, the one global world-clock cursor is paused. Therefore Timeless Form's existing world deadline is frozen with that cursor, never reset or extended by personal-turn count, and resumes at its original absolute world deadline.",
            "observedAnchors": {
                "ACTION-NATURAL": {"startedMs": 0, "deadlineMs": 60000, "pauseAtMs": 100, "resumeAtMs": 100, "remainingAtPauseMs": 59900, "remainingAfterResumeMs": 59900, "pauseClosesNaturally": True},
                "CLERIC-UNIVERSAL-NATURAL": {"startedMs": 0, "deadlineMs": 60000, "pauseAtMs": 0, "resumeAtMs": 0, "remainingAtPauseMs": 60000, "remainingAfterResumeMs": 60000, "pauseClosesNaturally": True},
                "ACTION-FAILED-THEN-INTERRUPTED": {"startedMs": 0, "deadlineMs": 60000, "pauseAtMs": 100, "resumeAtMs": 100, "remainingAtPauseMs": 59900, "remainingAfterResumeMs": 59900, "pauseClosesBySuccessfulDispel": True},
            },
            "readyCrosswalk": {
                "timeStopReadyRelease": "cases/preserved/RANK9TIMEFATE6129-TIME-STOP-B__ready-release-exact.json; exact Ready release pauses the original queue, retains its paid record, and resumes at the original markers.",
                "timeStopReadyExpiry": "cases/preserved/RANK9TIMEFATE6129-TIME-STOP-B__ready-expiry-exact.json; Ready expires at its original 6,000-ms own-start deadline.",
                "timelessFormReadyCase": "Return218 preserved RANK9DEFENSEFORM8129-TIMELESS-FORM-READY-EXPIRES.json.",
                "combinedBranchStatus": "No Ready spell is instantiated in the three new joint Timeless Form/Time Stop cases. The two underlying Ready procedures are independently source-bound; a combined Ready+Timeless Form+Time Stop scenario is listed as an untested cross-product, not claimed as proven.",
            },
            "regularTurnQueue": "W345 stores 20 ordered regular slots, each with exactly one START and END. Personal phases create no ordinary-start marker. The interrupted current slot resumes and ends once before the next scheduled slot.",
            "reactionRechargeConcentration": "Personal phases do not refresh shared Reaction or recharge. Existing Arcane Sight concentration remains active; Timeless Form is nonconcentration. Exact Ready/recharge semantics are also retained in W345's source and preserved cases.",
            "resourceRetention": "The Timeless Form 26-RP Action and Time Stop's actual 26-RP Action/Reaction are recorded once; failed Dispel cost/recharge remains paid; successful Dispel closes only the captured Time Stop source.",
        },
        "identifiedUncoveredOrConditionalBranches": [
            {
                "branch": "Actual Timeless Form acquisition outside the candidate fixture",
                "status": "conditional by instruction",
                "evidence": "All three W345 traces mark Timeless Form as candidateAcquisitionOnly=true and explicitly claim no prior/campaign acquisition. Director requested that this remain contingent on Timeless Form's own review.",
            },
            {
                "branch": "Ready active in the same Timeless Form/Time Stop encounter",
                "status": "not co-instantiated",
                "evidence": "W345 provides exact separate Time Stop Ready-release and Ready-expiry cases plus the prior Timeless Form Ready case; no case combines those with this new joint witness.",
            },
            {
                "branch": "Active Haste or Slow source during the same joint encounter",
                "status": "not co-instantiated",
                "evidence": "Q21's prior Haste/Slow paid-cost, both-Slow, and suppression cases remain byte-exact; W345's three joint cases do not contain an active Haste/Slow source.",
            },
            {
                "branch": "Action-mode Time Stop d4 values 2-4 in a Timeless Form joint trace",
                "status": "not co-instantiated",
                "evidence": "The joint Action traces use d4=1 / two personal rounds; the Universal joint trace uses its exact three-turn route. No joint Action trace samples the longer 3-5-round outcomes.",
            },
        ],
        "historicalPreservation": {
            "sourceArchive": bind(OLD_ZIP),
            "sourceCaseCount": 11,
            "caseBindings": old_case_bindings,
            "copiedCasePaths": [f"history/Return218/preserved_cases/{name}" for name in OLD_CASES],
            "event4RemainsHeld": True,
            "noHistoricalHOLDRewrite": True,
        },
        "noApplicationAuthorization": True,
        "projectionBinding": {"payloadPath": "crosswalk/W345_TIMELESS_FORM_EVIDENCE_PROJECTION.json", "bytes": len(projection_raw), "sha256": sha256(projection_raw)},
    }
    json_member("crosswalk/TIMELESS_FORM_DF218_B03_POSITIVE_CROSSWALK.json", crosswalk)

    request = """# Director request 346 — Timeless Form / DF218-B03 only

Please review this exact current-authority closure packet for `timeless-form` / `DF218-B03`. Current authority is Queue344: 824 applied / 24 pending / 0 accepted-unapplied; 0 first-review identities / 24 closure tasks; 548 complete standalone procedures / 173 scoped interfaces.

The packet binds the accepted and statically applied W345 Time Stop procedure, keeps its limited scope and qualifications, maps W345's three joint cases to DF9-Q20/Q21/Q22, reconciles the world-clock pause with the original 60,000-ms Timeless Form deadline, and preserves all 11 Return308 cases byte-exact. Timeless Form acquisition is still marked candidate-only and conditional. The separate Ready and active Haste/Slow cross-products, and longer Action-mode d4 values, are explicitly disclosed rather than claimed as traced.

Return a sealed ruling with `acceptedIds`, `appliedIds`, `heldIds`, `blockerIds`, `closedBlockerIds`, and `applicationAuthorized`; identify any actual missing branch by exact case/field. If you accept Timeless Form, state whether canonical authored-index application is authorized. No Timeless Form acceptance or application is presumed by this submission. Preserve TF192-H-WORLD, DF218-Q-AGING, every unrelated disposition, and all runtime/downstream gates.
"""
    write_member("DIRECTOR_REQUEST_346.md", request.encode("utf-8"))

    # Exact top-level member allowlist and payload checksums (manifest self-excludes).
    member_rows = []
    for path in sorted(PAYLOAD.rglob("*")):
        if not path.is_file() or path.name == "MEMBER_MANIFEST.json":
            continue
        raw = path.read_bytes()
        import zlib

        member_rows.append({
            "path": path.relative_to(PAYLOAD).as_posix(),
            "bytes": len(raw),
            "sha256": sha256(raw),
            "crc32": f"{zlib.crc32(raw) & 0xffffffff:08x}",
        })
    json_member("MEMBER_MANIFEST.json", {
        "id": "TIMELESS-FORM-CLOSURE346-PAYLOAD-MANIFEST",
        "memberCountExcludingSelf": len(member_rows),
        "members": member_rows,
    })

    archive = OUT / "DD_Rank9_TimelessForm_DF218B03_Closure346.zip"
    archive.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for path in sorted(PAYLOAD.rglob("*")):
            if path.is_file():
                z.write(path, path.relative_to(PAYLOAD).as_posix())
    return {
        "archive": archive,
        "payloadMembers": len(member_rows) + 1,
        "preservedTimelessFormCases": len(old_case_bindings),
        "projectedW345JointCases": len(projected_cases),
    }


if __name__ == "__main__":
    result = build()
    print(json.dumps({
        "archive": str(result["archive"]),
        "payloadMembers": result["payloadMembers"],
        "preservedTimelessFormCases": result["preservedTimelessFormCases"],
        "projectedW345JointCases": result["projectedW345JointCases"],
    }, indent=2))
