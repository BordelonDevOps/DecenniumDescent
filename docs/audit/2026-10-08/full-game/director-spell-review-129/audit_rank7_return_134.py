"""Independent data-only audit for Rank7Perception5 return 134.

Reads the exact received ZIP and extracted JSON/Markdown as data. It does not
import, evaluate, or execute anything supplied in the archive and cannot
change acceptance/application state.
"""
from pathlib import Path, PurePosixPath
import argparse, copy, datetime, hashlib, json, stat, zipfile

P = argparse.ArgumentParser()
P.add_argument("report")
A = P.parse_args()
D = Path(__file__).parent.resolve()
G = Path(r"C:\Github\DecenniumDescent")
E = Path(r"C:\R7R134").resolve()
ARCHIVE = Path(r"C:\Users\cbord\Downloads\DD_Rank7Perception5_Director_Return01_134.zip")
DELIVERY = Path(r"C:\Users\cbord\Downloads\DD_Rank7Perception5_Director_Return01_134_DELIVERY.json")
RECEIPT = D / "RANK7PERCEPTION5_RETURN01_RECEIVED_134.json"
REPORT = (D / A.report).resolve()
assert REPORT.parent == D and E.is_dir()
IDS = ["inescapable-labyrinth", "mindtrap-echo", "mirage-arcane", "mirage-legion", "perfect-veil"]
sha = lambda b: hashlib.sha256(b).hexdigest()
read = lambda p: json.loads(Path(p).read_text(encoding="utf-8-sig"))
checks, errors, findings = [], [], []

def check(name, condition, detail=None):
    checks.append(name)
    if not condition:
        errors.append({"check": name, "detail": detail})

def load(rel):
    return read(E / rel)

def state_hash(value):
    # The return's state hashes use Python's sorted-key JSON serialization.
    return sha(json.dumps(value, sort_keys=True).encode("utf-8"))

def tokens(path):
    if path == "":
        return []
    assert path.startswith("/")
    return [x.replace("~1", "/").replace("~0", "~") for x in path[1:].split("/")]

def get_at(root, path):
    node = root
    for t in tokens(path):
        node = node[int(t)] if isinstance(node, list) else node[t]
    return node

def replace_at(root, path, value):
    ts = tokens(path)
    if not ts:
        return copy.deepcopy(value)
    node = root
    for t in ts[:-1]:
        node = node[int(t)] if isinstance(node, list) else node[t]
    key = int(ts[-1]) if isinstance(node, list) else ts[-1]
    assert (0 <= key < len(node)) if isinstance(node, list) else (key in node)
    node[key] = copy.deepcopy(value)
    return root

def apply_ops(state, operations):
    state = copy.deepcopy(state)
    for op in operations:
        if op["op"] == "test":
            assert get_at(state, op["path"]) == op["value"]
        elif op["op"] == "replace":
            state = replace_at(state, op["path"], op["value"])
        else:
            raise AssertionError("unsupported operation: " + str(op.get("op")))
    return state

expected_delivery = {
    "filename": ARCHIVE.name,
    "bytes": 207128321,
    "sha256": "81bfbdc85536782243e1b5c1e441584b3265dc0ecd43640fc6066126823ec0b8",
    "members": 145,
    "bindings": 144,
    "identities": IDS,
    "questions": 29,
    "mainCases": 10,
    "branches": 27,
    "events": 264,
    "currentCounts": {"applied": 643, "pending": 205, "acceptedUnapplied": 0},
    "accepted": False,
    "applied": False,
}
delivery = read(DELIVERY)
for key, value in expected_delivery.items():
    check("delivery:" + key, delivery.get(key) == value, {"expected": value, "actual": delivery.get(key)})
raw_archive = ARCHIVE.read_bytes()
check("archive-byte-sha", len(raw_archive) == expected_delivery["bytes"] and sha(raw_archive) == expected_delivery["sha256"])

with zipfile.ZipFile(ARCHIVE) as z:
    infos = [i for i in z.infolist() if not i.is_dir()]
    names = [i.filename for i in infos]
    check("zip-crc", z.testzip() is None)
    check("unique-safe-members", len(names) == len(set(names)) == len({n.casefold() for n in names}) and all(
        n and not n.startswith("/") and "\\" not in n and ":" not in n and ".." not in PurePosixPath(n).parts
        and not stat.S_ISLNK(i.external_attr >> 16) for i, n in zip(infos, names)))
    root_manifest_bytes = z.read("MANIFEST.json")
    manifest = json.loads(root_manifest_bytes.decode("utf-8-sig"))
    artifact = json.loads(z.read("ARTIFACT_BINDINGS.json").decode("utf-8-sig"))
    bindings = manifest["members"]
    check("root-manifest-count", manifest.get("algorithm") == "SHA256" and manifest.get("excludedSelf") == "MANIFEST.json exact ZIP/delivery binds self" and manifest.get("membersIncludingSelf") == len(names))
    check("artifact-binding-exact-set", artifact.get("bindings") == [b for b in bindings if b["path"] != "ARTIFACT_BINDINGS.json"])
    check("manifest-exact-member-set", len(bindings) == len({b["path"] for b in bindings}) and {b["path"] for b in bindings} == set(names) - {"MANIFEST.json"})
    for b in bindings:
        data = z.read(b["path"])
        check("zip-binding:" + b["path"], len(data) == b["bytes"] and sha(data) == b["sha256"])
        extracted = (E / PurePosixPath(b["path"])).resolve()
        check("extracted-binding:" + b["path"], extracted.is_relative_to(E) and extracted.is_file() and extracted.stat().st_size == b["bytes"] and sha(extracted.read_bytes()) == b["sha256"])

receipt = read(RECEIPT)
check("receipt-exact-archive", receipt.get("archive", {}).get("bytes") == len(raw_archive) and receipt.get("archive", {}).get("sha256") == sha(raw_archive) and receipt.get("bindings") == 144 and receipt.get("members") == 145)

index_path = G / "DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json"
catalog_path = G / "DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json"
source_js = G / "DescentReviewChanges/ReviewBible/src/data/spells.js"
index = read(index_path)
catalog = read(catalog_path)
index_copy_bytes = (E / "authority/authored_review_index.json").read_bytes()
check("current-index-copy-byte-exact", index_copy_bytes == index_path.read_bytes())
check("current-counts", index["authoredCounts"] == {"reviewed": 643, "pending": 205} and sum(e["authoredStatus"] == "reviewed-authored-operational-playtest" for e in index["entries"]) == 643 and sum(e["authoredStatus"] == "pending-authored-procedure" for e in index["entries"]) == 205)
index_entries = {e["id"]: e for e in index["entries"]}
catalog_spells = {s["id"]: s for s in catalog["spells"]}
check("exact-five-pending", all(i in index_entries and index_entries[i]["authoredStatus"] == "pending-authored-procedure" for i in IDS))
native = load("NATIVE_ACCESS_RECORDS.json")
procedures = load("PROCEDURES.json")
proc_by_id = {p["spellId"]: p for p in procedures}
check("procedure-identity-set", len(procedures) == 5 and set(proc_by_id) == set(IDS))
check("native-identity-set", set(native) == set(IDS))
source_js_hash = sha(source_js.read_bytes())
for sid in IDS:
    check("native-current-card:" + sid, native[sid] == catalog_spells[sid])
    proc = proc_by_id[sid]
    check("procedure-current-source:" + sid, proc["completeNativeAccessAndSource"] == catalog_spells[sid])
    check("procedure-file-mirror:" + sid, load("procedures/" + sid + ".json") == proc)
    check("procedure-remains-pending:" + sid, proc["status"] == "PROPOSED_PENDING_INDEPENDENT_EXACT_ACCEPTANCE" and proc["authorAcceptance"] is False and proc["authorApplication"] is False)
    check("source-catalog-binding:" + sid, proc["completeNativeAccessAndSource"]["source"]["catalogSha256"] == source_js_hash)

proposed = load("PROPOSED_SCOPE_ONLY.json")
check("no-premature-accept-apply", proposed["identities"] == IDS and not proposed["accepted"] and not proposed["applied"] and not proposed["canonicalIndexOperationsExecuted"] and proposed["independentExactAcceptanceRequired"] is True)
check("proposal-counts-match", proposed["currentAuthoritativeCounts"] == {"applied": 643, "pending": 205, "acceptedUnapplied": 0})
routing = load("AUTHORITY_ROUTING.json")
check("scope-boundaries", routing["allFivePending"] == IDS and routing["current"] == proposed["currentAuthoritativeCounts"] and routing["acceptanceByAuthor"] is False and routing["applicationByAuthor"] is False and "335feats" in routing["closed"] and "completed16/72" in routing["closed"])

preservation = load("SOURCE_PRESERVATION.json")
check("data-only-and-no-code-execution", preservation["allOriginalInputBytesPreserved"] is True and "none executed" in preservation["originalProgramTreatment"] and preservation["currentCounts"] == proposed["currentAuthoritativeCounts"])
expected_inputs = {
    "DD_Rank7_Perception_5_Source_Conference_01.zip": (3610050, "df26e8b3606912c04eb82d559c9f75df391b053b2846b0002500474a207bc421", G / "docs/audit/2026-10-08/full-game/DD_Rank7_Perception_5_Source_Conference_01.zip"),
    "DD_PlanarTravel6_Applied_Rank7Perception5_Context_133.zip": (387746, "2880b0ce9cdd335f6031e2ab8a0463c284c97d342a0ea03161fdc1f8e1a6a794", G / "docs/audit/2026-10-08/full-game/director-spell-review-129/DD_PlanarTravel6_Applied_Rank7Perception5_Context_133.zip"),
}
for item in preservation["directExactInputs"]:
    name = Path(item["path"]).name.replace("(1)", "")
    expected = expected_inputs.get(name)
    check("original-input-receipt:" + name, expected is not None and item["bytes"] == expected[0] and item["sha256"] == expected[1] and expected[2].is_file() and expected[2].stat().st_size == expected[0] and sha(expected[2].read_bytes()) == expected[1])

current_authority = E / "evidence/current-authority"
current_files = [p for p in current_authority.rglob("*") if p.is_file()]
check("current-authority-evidence-count", len(current_files) == 15)
for f in current_files:
    rel = f.relative_to(current_authority)
    live = G / rel
    check("current-authority:" + rel.as_posix(), live.is_file() and live.read_bytes() == f.read_bytes())

questions_source = load("history/INDEPENDENT_QUESTIONS_127.json")
questions = load("QUESTION_DISPOSITIONS.json")
source_questions = {q["id"]: q for q in questions_source["originalQuestions"] + questions_source["additionalFocusedQuestions"]}
question_by_id = {q["id"]: q for q in questions}
check("all-29-question-ids", len(questions) == 29 and len(question_by_id) == 29 and set(question_by_id) == set(source_questions))
casebook = load("CASEBOOK.json")
cases = casebook["allCases"]
case_by_id = {c["id"]: c for c in cases}
main_ids = casebook["mainCaseIds"]
check("case-counts", len(cases) == 37 and len(case_by_id) == 37 and len(main_ids) == 10 and casebook["mainCases"] == 10 and casebook["branchCases"] == 27 and casebook["authoredDataOnly"] is True)
check("main-branch-partition", len(set(main_ids)) == 10 and set(main_ids) <= set(case_by_id) and len(set(case_by_id) - set(main_ids)) == 27)
for qid, q in question_by_id.items():
    check("question-preserved:" + qid, q.get("completeOriginalQuestionUnchanged") == source_questions[qid] and q.get("sourceOriginalDecisionFlagNotMutated") is True)
    check("question-disposition:" + qid, bool(q.get("completeDisposition")) and q.get("status") == "PROPOSED_AUTHORED_DISPOSITION_NOT_INDEPENDENT_ACCEPTANCE" and set(q.get("operativeProcedureIds", [])) <= set(IDS) and set(q.get("completeCaseIds", [])) <= set(case_by_id))

profiles = load("ACTOR_PROFILES.json")
event_by_id = {}
total_events = 0
for case in cases:
    cid = case["id"]
    for pid, profile in case["profiles"].items():
        check("case-profile:" + cid + ":" + pid, profiles.get(pid) == profile)
    events = case["events"]
    total_events += len(events)
    check("case-nonempty:" + cid, bool(events) and isinstance(case["initial"], dict) and isinstance(case["final"], dict))
    if not events:
        continue
    check("case-start:" + cid, case["initial"] == events[0]["before"])
    check("case-end:" + cid, case["final"] == events[-1]["after"])
    for n, event in enumerate(events):
        eid = event["id"]
        check("unique-event:" + eid, eid not in event_by_id)
        event_by_id[eid] = event
        check("event-state-hashes:" + eid, state_hash(event["before"]) == event["beforeHash"] and state_hash(event["after"]) == event["afterHash"])
        check("event-time:" + eid, event["time"] == event["after"]["time"] and event["before"]["time"] <= event["after"]["time"])
        if n:
            check("event-continuity:" + eid, events[n - 1]["after"] == event["before"])
        try:
            check("forward-replay:" + eid, apply_ops(event["before"], event["forward"]) == event["after"])
            check("inverse-replay:" + eid, apply_ops(event["after"], event["inverse"]) == event["before"])
        except Exception as exc:
            check("operation-replay-exception:" + eid, False, repr(exc))
check("total-events", total_events == 264 and len(event_by_id) == 264)

for case in cases:
    parent = case["parentExactFork"]
    if parent is None:
        continue
    parent_case = case_by_id.get(parent["case"])
    parent_event = event_by_id.get(parent["event"])
    check("exact-branch-parent:" + case["id"], parent_case is not None and parent_event is not None and parent_event in parent_case["events"] and case["initial"] == parent_event["after"])
check("exact-fork-count", sum(c["parentExactFork"] is not None for c in cases) == 11)

event_ops = load("EVENT_OPERATIONS.json")
ops_by_id = {x["eventId"]: x for x in event_ops}
check("operation-event-set", len(event_ops) == 264 and len(ops_by_id) == 264 and set(ops_by_id) == set(event_by_id))
for eid, event in event_by_id.items():
    op = ops_by_id.get(eid, {})
    check("operation-mirror:" + eid, op.get("caseId") == event.get("id", "").split(":")[0] and op.get("beforeHash") == event["beforeHash"] and op.get("afterHash") == event["afterHash"] and op.get("forward") == event["forward"] and op.get("inverse") == event["inverse"])

original_dispositions = load("ORIGINAL_CASE_DISPOSITIONS.json")
check("original-obligation-set", len(original_dispositions["individualOriginalSourceObligations"]) == 5 and {x["spellId"] for x in original_dispositions["individualOriginalSourceObligations"]} == set(IDS))
check("original-records-preserved", original_dispositions["allOriginalQuestionRecordsPreserved"] is True and original_dispositions["historicalCasesRecoveredOrPretendedExact"] is False and len(original_dispositions["allCompleteOriginalFutureRequirementsUnchanged"]) == 9)
holds = load("HOLD_REGISTER.json")
hold_ids = [x["id"] for x in holds]
check("retained-holds", len(holds) == 6 and len(hold_ids) == len(set(hold_ids)) and "RP134-UNEXERCISED-REPEAT-PROVIDERS" in hold_ids and "RP134-RETAINED-COUNTERPART-HOLDS" in hold_ids and "RP134-NONRUNTIME" in hold_ids)

validation = load("VALIDATION.json")
inspection = load("POSTBUILD_DATA_INSPECTION.json")
check("author-self-validation-scope", validation["questions"] == 29 and validation["mainCases"] == 10 and validation["branches"] == 27 and validation["events"] == 264 and validation["allFullForwardInverseOperationsVerified"] is True and validation["authorAcceptedApplied"] is False and validation["suppliedHistoricalProgramsExecuted"] is False)
check("postbuild-self-inspection-scope", inspection["questions"] == 29 and inspection["mainCases"] == 10 and inspection["branches"] == 27 and inspection["events"] == 264 and inspection["acceptedApplied"] is False and inspection["runtimeHumanBalanceCosmologyTemporalReleaseApproved"] is False)

findings.extend([
    "All five authored procedures preserve the exact current native spell records; selected durations, costs, sensory rules, and encounter geometry are explicit NEW operational choices.",
    "All 29 original/focused questions are preserved verbatim with authored dispositions and complete case references; original decision flags remain unselected.",
    "All 10 main cases and 27 exact-fork branches have continuous states; every one of 264 forward and inverse event patches replays exactly and matches its duplicate operations ledger.",
    "The return remains a proposal only. Acceptance and canonical application are false; six explicit scope/runtime/evidence holds remain open.",
])
report = {
    "id": "RANK7PERCEPTION5-RETURN01-INDEPENDENT-AUDIT-134",
    "recordedAtUtc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
    "status": "PASSED_INDEPENDENT_DATA_AUDIT_READY_FOR_EXACT_ACCEPTANCE" if not errors else "FAILED_INDEPENDENT_DATA_AUDIT",
    "errors": errors,
    "checksPassed": len(checks) - len(errors),
    "checksFailed": len(errors),
    "checks": checks,
    "semanticFindings": findings,
    "reviewedIdentities": IDS,
    "returnArchive": {"path": str(ARCHIVE), "bytes": len(raw_archive), "sha256": sha(raw_archive), "manifestMembers": len(names), "manifestBindings": len(bindings)},
    "counts": {"questions": len(questions), "mains": len(main_ids), "branches": casebook["branchCases"], "events": total_events, "currentApplied": 643, "currentPending": 205, "currentAcceptedUnapplied": 0},
    "retainedHolds": hold_ids,
    "runtimeExecuted": False,
    "authorMarkedAcceptedOrAppliedInReturn": False,
    "canonicalChanges": False,
}
REPORT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps({"status": report["status"], "checksPassed": report["checksPassed"], "checksFailed": report["checksFailed"], "errorSample": errors[:10], "report": str(REPORT)}, ensure_ascii=False, indent=2))
