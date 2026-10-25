"""Independent data-only audit of the Ward7 Director Return01 135 ZIP.

This script reads the return as bytes and JSON only. It does not import or run
anything contained in the archive, and it never accepts or applies the batch.
"""
from pathlib import Path, PurePosixPath
import argparse
import copy
import hashlib
import json
import stat
import zipfile

P = argparse.ArgumentParser()
P.add_argument("report")
A = P.parse_args()
D = Path(__file__).parent.resolve()
G = Path(r"C:\Github\DecenniumDescent")
E = Path(r"C:\W7R135").resolve()
ARCHIVE = D / "DD_Ward7_Director_Return01_135.zip"
RECEIPT = D / "WARD7_RETURN01_RECEIVED_135.json"
EXPECTATIONS = D / "WARD7_RETURN_EXPECTATIONS_134.json"
DELIVERY_PATH = D / "WARD7_RETURN01_DELIVERY_135.json"
REPORT = (D / A.report).resolve()
IDS = [
    "arcane-aegis", "spell-turning", "dimensional-lock",
    "resonance-fortress", "faction-aegis", "corruption-immunity",
    "summon-living-armor",
]
DELIVERY = {
    "file": "DD_Ward7_Director_Return01_135.zip",
    "bytes": 104811664,
    "sha256": "c39b97e32c7be0029a3b429a5abc5b7da2d743a74cd052bef5b33167c1611edb",
    "members": 154,
    "manifestBindings": 153,
    "dataInspectionChecksPassed": 11317,
    "mainCases": 14,
    "branches": 10,
    "events": 157,
    "dataOperationsIncludingTests": 3732,
    "scope": "Proposed authored data for exact independent semantic audit; explicit holds retained. No independent acceptance/application, runtime/human/balance/cosmology/release approval.",
    "authority": {"applied": 648, "pending": 200, "acceptedUnapplied": 0},
    "baselineFilesPreserved": 109,
    "suppliedOrHistoricalProgramsExecuted": False,
    "nextPendingGroup": "manifestation7",
}

sha = lambda b: hashlib.sha256(b).hexdigest()
read = lambda p: json.loads(Path(p).read_text(encoding="utf-8-sig"))
checks, errors = [], []

def check(name, condition, detail=None):
    checks.append(name)
    if not condition:
        errors.append({"check": name, "detail": detail})

def state_hash(value):
    return sha(json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8"))

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
        assert op.get("op") in {"test", "replace"}
        if op["op"] == "test":
            assert get_at(state, op["path"]) == op["value"]
        else:
            state = replace_at(state, op["path"], op["value"])
    return state

assert E.is_dir() and ARCHIVE.is_file() and RECEIPT.is_file() and EXPECTATIONS.is_file()
raw = ARCHIVE.read_bytes()
delivery = read(DELIVERY_PATH)
check("delivery-metadata", delivery == DELIVERY)
check("archive-size-hash", len(raw) == DELIVERY["bytes"] and sha(raw) == DELIVERY["sha256"])
receipt = read(RECEIPT)
check("receiver-receipt", receipt.get("status") == "RECEIVED_BINDINGS_VERIFIED_NOT_ACCEPTED" and receipt.get("archive", {}).get("bytes") == len(raw) and receipt.get("archive", {}).get("sha256") == sha(raw) and receipt.get("members") == 154 and receipt.get("bindings") == 153 and receipt.get("canonicalChanges") is False and receipt.get("suppliedCodeExecuted") is False)

with zipfile.ZipFile(ARCHIVE) as z:
    infos = [i for i in z.infolist() if not i.is_dir()]
    names = [i.filename for i in infos]
    check("zip-crc", z.testzip() is None)
    check("unique-safe-members", len(names) == len(set(names)) == len({n.casefold() for n in names}) and all(n and not n.startswith("/") and "\\" not in n and ":" not in n and ".." not in PurePosixPath(n).parts and not stat.S_ISLNK(i.external_attr >> 16) for i, n in zip(infos, names)))
    manifest = json.loads(z.read("MANIFEST.json").decode("utf-8-sig"))
    artifact = json.loads(z.read("ARTIFACT_BINDINGS.json").decode("utf-8-sig"))
    bindings = manifest["files"]
    check("manifest-count-and-scope", manifest.get("id") == "W135-COMPLETE-MEMBER-MANIFEST" and manifest.get("selfExcluded") == "MANIFEST.json" and manifest.get("accepted") is False and manifest.get("applied") is False and len(names) == 154 and len(bindings) == 153)
    check("artifact-binding-exact", artifact.get("files") == [b for b in bindings if b["path"] != "ARTIFACT_BINDINGS.json"] and set(artifact.get("excludedOnly", [])) == {"MANIFEST.json", "ARTIFACT_BINDINGS.json"})
    check("manifest-member-set", len(bindings) == len({b["path"] for b in bindings}) and {b["path"] for b in bindings} == set(names) - {"MANIFEST.json"})
    for b in bindings:
        data = z.read(b["path"])
        check("zip-binding:" + b["path"], len(data) == b["bytes"] and sha(data) == b["sha256"])
        extracted = (E / PurePosixPath(b["path"])).resolve()
        check("extracted-binding:" + b["path"], extracted.is_relative_to(E) and extracted.is_file() and extracted.stat().st_size == b["bytes"] and sha(extracted.read_bytes()) == b["sha256"])

def load(rel):
    return read(E / rel)

expect = read(EXPECTATIONS)
check("source-bound-expectation-id-set", expect.get("identities") == IDS and len(expect.get("allQuestions", [])) == 26 and len(expect.get("requiredNewCases", [])) == 14)

# Preserve exact current authority and the current pending set.
index_path = G / "DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json"
catalog_path = G / "DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json"
spell_js = G / "DescentReviewChanges/ReviewBible/src/data/spells.js"
index = read(index_path)
catalog = read(catalog_path)
index_copy = E / "authority/authority/authored_review_index.json"
catalog_copy = E / "authority/authority/catalog.json"
check("current-authority-index-copy", index_copy.read_bytes() == index_path.read_bytes())
check("current-authority-catalog-copy", catalog_copy.read_bytes() == catalog_path.read_bytes())
check("current-counts", index.get("authoredCounts") == {"reviewed": 648, "pending": 200} and sum(e.get("authoredStatus") == "reviewed-authored-operational-playtest" for e in index["entries"]) == 648 and sum(e.get("authoredStatus") == "pending-authored-procedure" for e in index["entries"]) == 200)
index_by_id = {e["id"]: e for e in index["entries"]}
spell_by_id = {s["id"]: s for s in catalog["spells"]}
check("exact-seven-pending", all(index_by_id.get(i, {}).get("authoredStatus") == "pending-authored-procedure" for i in IDS))
pending_audit = read(D / "CURRENT200_PENDING_IDENTITY_AUDIT_134.json")
check("pending-set-audit", set(pending_audit.get("pendingIdentityIds", pending_audit.get("pendingIds", []))) == {e["id"] for e in index["entries"] if e.get("authoredStatus") == "pending-authored-procedure"})

# Exact native access and proposed procedure binding for all seven identities.
native = load("NATIVE_ACCESS_RECORDS.json")
procedures = load("PROCEDURES.json")
proc_by_id = {p.get("spellId"): p for p in procedures}
check("procedure-and-native-identity-set", set(proc_by_id) == set(IDS) and set(native) == set(IDS) and len(procedures) == 7)
js_hash = sha(spell_js.read_bytes())
for sid in IDS:
    card = spell_by_id[sid]
    proc = proc_by_id[sid]
    check("native-card-current:" + sid, native[sid] == card)
    check("procedure-source-current:" + sid, proc.get("completeNativeAccessAndSource") == card and proc.get("completeNativeAccessAndSource", {}).get("source", {}).get("catalogSha256") == js_hash)
    check("procedure-proposed-only:" + sid, proc.get("status") == "PROPOSED_AUTHORED_COMPLETE_PROCEDURE_FOR_INDEPENDENT_EXACT_REVIEW" and proc.get("accepted") is False and proc.get("applied") is False and bool(proc.get("procedure")))
    check("procedure-file-mirror:" + sid, load("procedures/" + sid + ".json") == proc)
check("not-accepted-applied", manifest.get("accepted") is False and manifest.get("applied") is False and load("CASEBOOK.json").get("notAcceptedOrApplied") is True and load("HOLD_REGISTER.json").get("noApplicationPerformed") is True)

# Preserve all 26 complete source questions and add one proposed disposition per ID.
question_source = expect["allQuestions"]
questions = load("QUESTION_DISPOSITIONS.json")
source_q = {q["id"]: q for q in question_source}
question_by_id = {q.get("id"): q for q in questions}
check("question-id-set", len(questions) == 26 and len(question_by_id) == 26 and set(question_by_id) == set(source_q))
casebook = load("CASEBOOK.json")
cases = casebook["allCases"]
case_by_id = {c["id"]: c for c in cases}
for qid, q in question_by_id.items():
    check("question-verbatim:" + qid, q.get("originalQuestion") == source_q[qid])
    check("question-pending:" + qid, q.get("status") == "DIRECTOR_PROPOSED_DISPOSITION_FOR_INDEPENDENT_REVIEW" and q.get("accepted") is False and q.get("applied") is False and bool(q.get("selectedRule")))
    check("question-references:" + qid, all(x.get("spellId") in IDS and x.get("sourceRecord") in {"procedures/" + sid + ".json" for sid in IDS} for x in q.get("selectedRule", [])) and set(q.get("evidenceCaseIds", [])) <= set(case_by_id))

# Map every original case obligation without deleting or silently substituting it.
crosswalk = load("CASE_OBLIGATION_CROSSWALK.json")
expected_cases = {c["id"]: c for c in expect["requiredNewCases"]}
crosswalk_by_id = {x.get("original", {}).get("id"): x for x in crosswalk}
main_ids = casebook.get("mainCaseIds", [])
check("original-obligation-id-set", len(crosswalk) == 14 and set(crosswalk_by_id) == set(expected_cases))
for oid, original in expected_cases.items():
    item = crosswalk_by_id[oid]
    check("obligation-preserved:" + oid, item.get("original") == original)
    check("obligation-mapped-to-main:" + oid, item.get("caseId") in main_ids and item.get("caseId") in case_by_id and bool(item.get("note")))
check("main-and-branch-counts", len(main_ids) == 14 and casebook.get("mainCases") == 14 and casebook.get("branches") == 10 and len(cases) == 24 and len(set(case_by_id)) == 24)
check("main-case-reference-set", len(set(main_ids)) == 14 and set(main_ids) <= set(case_by_id))

# Validate all full state snapshots, monotonic time, and reversible value operations.
profiles = load("ACTOR_PROFILES.json")
events_by_id = {}
total_events = total_ops = 0
for case in cases:
    cid = case["id"]
    for pid, profile in case.get("profiles", {}).items():
        check("case-profile:" + cid + ":" + pid, profiles.get(pid) == profile)
    events = case.get("events", [])
    total_events += len(events)
    check("case-nonempty:" + cid, bool(events) and isinstance(case.get("initial"), dict) and isinstance(case.get("final"), dict))
    if not events:
        continue
    check("case-start:" + cid, case["initial"] == events[0]["before"])
    check("case-end:" + cid, case["final"] == events[-1]["after"])
    for n, event in enumerate(events):
        eid = event["id"]
        check("event-unique:" + eid, eid not in events_by_id)
        events_by_id[eid] = event
        check("event-state-hashes:" + eid, state_hash(event["before"]) == event["beforeSHA256"] and state_hash(event["after"]) == event["afterSHA256"])
        check("event-time:" + eid, event["time"] == event["after"].get("time") and event["before"].get("time", 0) <= event["after"].get("time", 0))
        if n:
            check("event-continuity:" + eid, events[n - 1]["after"] == event["before"])
        for direction in ("forward", "inverse"):
            ops = event.get(direction, [])
            total_ops += len(ops)
            check("event-ops-nonempty:" + eid + ":" + direction, bool(ops))
        try:
            check("forward-replay:" + eid, apply_ops(event["before"], event["forward"]) == event["after"])
            check("inverse-replay:" + eid, apply_ops(event["after"], event["inverse"]) == event["before"])
        except Exception as exc:
            check("operation-replay-exception:" + eid, False, repr(exc))
check("event-count-and-unique", total_events == 157 and len(events_by_id) == 157 and casebook.get("events") == 157)
check("operation-count", total_ops == 3732)

# Explicitly verify every declared exact fork's parent state and hash.
for case in cases:
    parent = case.get("parentExactFork")
    if parent is None:
        continue
    parent_case = case_by_id.get(parent.get("case"))
    parent_event = events_by_id.get(parent.get("event"))
    check("exact-fork-parent:" + case["id"], parent_case is not None and parent_event is not None and parent_event in parent_case.get("events", []) and case.get("initial") == parent_event.get("after") and state_hash(case.get("initial")) == parent.get("stateSHA256"))

# Byte-exact preservation of the 109 source files observed before authoring.
preservation = load("RESUME_PRESERVATION_BASELINE.json")
check("resume-baseline-size", len(preservation) == 109 and DELIVERY["baselineFilesPreserved"] == 109)
for record in preservation:
    rel = record["path"]
    f = (E / PurePosixPath(rel)).resolve()
    check("resume-baseline:" + rel, f.is_relative_to(E) and f.is_file() and f.stat().st_size == record["bytes"] and sha(f.read_bytes()) == record["sha256"])
inventory = load("RESUME_INVENTORY.json")
check("resume-inventory-no-repeat-or-execution", inventory.get("existingAtResume", {}).get("procedures") == 7 and inventory.get("existingAtResume", {}).get("serializedCases") == 0 and inventory.get("historicalProgramExecuted") is False and inventory.get("sourceBuildersRerun") is False)

# Exact source and updated context packets are the already audited local bytes.
source_archive = G / "docs/audit/2026-10-08/full-game/DD_Ward_7_Source_Conference_01.zip"
source_copy = E / "authority/ward7/DD_Ward_7_Source_Conference_01.zip"
check("ward-source-archive-current", source_archive.is_file() and source_copy.read_bytes() == source_archive.read_bytes() and sha(source_copy.read_bytes()) == "dba4154d6cb241b54af32390eda2ee0726b5c11e0252eec4199f746352ba9ff5")
context_archive = D / "DD_Rank7Perception5_Applied_Ward7_Context_134.zip"
context_copy = E / "history/DD_Rank7Perception5_Applied_Ward7_Context_134.zip"
check("applied-context-exact", context_archive.is_file() and context_copy.read_bytes() == context_archive.read_bytes())
for rel, live in [
    ("authority/authority/CURRENT200_PENDING_IDENTITY_AUDIT_134.json", D / "CURRENT200_PENDING_IDENTITY_AUDIT_134.json"),
    ("authority/authority/CURRENT_HANDOFF_134.json", D / "CURRENT_HANDOFF_134.json"),
    ("authority/authority/CURRENT_SPELL_QUEUE_134.json", D / "CURRENT_SPELL_QUEUE_134.json"),
]:
    copied = E / rel
    if "PENDING_IDENTITY" in rel:
        check("current-queue-copy:" + rel, live.is_file() and copied.read_bytes() == live.read_bytes())
    else:
        local_obj, return_obj = read(live), read(copied)
        check("current-queue-state:" + rel, local_obj.get("currentCounts") == return_obj.get("currentCounts"))

# Holds and author self-report are records, never acceptance evidence.
holds = load("HOLD_REGISTER.json")
check("holds-retained", len(holds.get("currentInheritedHolds", [])) == 3 and len(holds.get("newQualifications", [])) == 15 and len(holds.get("unassignedRank9", [])) == 30 and holds.get("noApplicationPerformed") is True)
check("rank9-analyses-unassigned", len(load("UNASSIGNED_RANK9_ANALYSES.json")) == 2)
validation = load("VALIDATION.json")
check("author-validation-report-only", validation.get("checks") == 11317 and validation.get("failed") == 0 and validation.get("cases") == 24 and validation.get("mains") == 14 and validation.get("branches") == 10 and validation.get("events") == 157 and validation.get("currentCounts") == DELIVERY["authority"] and validation.get("sourceProgramsExecuted") is False)

report = {
    "id": "WARD7-RETURN01-INDEPENDENT-AUDIT-135",
    "status": "INDEPENDENT_AUDIT_PASS_NOT_ACCEPTED_OR_APPLIED" if not errors else "INDEPENDENT_AUDIT_FAILED",
    "archive": {"bytes": len(raw), "sha256": sha(raw)},
    "checksPassed": len(checks) - len(errors),
    "checksFailed": len(errors),
    "checks": checks,
    "errors": errors,
    "counts": {"identities": len(IDS), "questions": len(questions), "mains": len(main_ids), "branches": casebook.get("branches"), "cases": len(cases), "events": total_events, "operationsIncludingTests": total_ops, "applied": 648, "pending": 200, "acceptedUnapplied": 0},
    "canonicalChanges": False,
    "suppliedOrHistoricalProgramsExecuted": False,
}
REPORT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps({k: report[k] for k in ["status", "checksPassed", "checksFailed", "counts"]} | {"errorSample": errors[:12], "report": str(REPORT)}, ensure_ascii=False, indent=2))
