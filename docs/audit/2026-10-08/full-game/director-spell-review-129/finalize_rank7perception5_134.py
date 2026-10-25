from pathlib import Path
import hashlib, json, shutil

D = Path(__file__).parent.resolve()
G = Path(r"C:\Github\DecenniumDescent")
INDEX = G / "DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json"
CATALOG = G / "DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json"
SPELLS_JS = G / "DescentReviewChanges/ReviewBible/src/data/spells.js"
PKG = G / "DescentReviewChanges/ReviewBible/data/public/spell_candidates/rank7perception5_reviewed_134"
IDS = ["inescapable-labyrinth", "mindtrap-echo", "mirage-arcane", "mirage-legion", "perfect-veil"]
sha = lambda b: hashlib.sha256(b).hexdigest()
read = lambda p: json.loads(Path(p).read_text(encoding="utf-8-sig"))
dump = lambda p, obj: Path(p).write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

audit = read(D / "RANK7PERCEPTION5_RETURN01_INDEPENDENT_AUDIT_134.json")
acceptance = read(D / "RANK7PERCEPTION5_EXACT_ACCEPTANCE_134.json")
application = read(D / "RANK7PERCEPTION5_APPLICATION_134.json")
ops_doc = read(D / "RANK7PERCEPTION5_INDEX_OPERATIONS_134.json")
before_bytes = (D / "authored_review_index.before_rank7perception5_134.json").read_bytes()
after_bytes = INDEX.read_bytes()
before = json.loads(before_bytes.decode("utf-8-sig"))
after = json.loads(after_bytes.decode("utf-8-sig"))
assert audit["status"] == "PASSED_INDEPENDENT_DATA_AUDIT_READY_FOR_EXACT_ACCEPTANCE" and audit["checksFailed"] == 0
assert acceptance["approvedForCanonicalApplication"] is True and acceptance["unresolvedAuthoredBlockers"] == []
assert application["acceptedIds"] == acceptance["acceptedIdentities"] == IDS
assert ops_doc["before"]["sha256"] == sha(before_bytes)
assert ops_doc["after"]["sha256"] == sha(after_bytes)

# Replay the recorded forward delta from the exact saved index, then reverse it.
forward = json.loads(json.dumps(before))
for op in ops_doc["operations"]:
    if op["op"] == "replace-entry":
        forward["entries"][op["index"]] = op["after"]
    elif op["op"] == "replace-authored-counts":
        forward["authoredCounts"] = op["after"]
    elif op["op"] == "replace-representation-count":
        forward["representationCounts"] = op["after"]
    elif op["op"] == "append-standalone-envelope":
        forward["additionalStandaloneEnvelopes"].append(op["after"])
    else:
        raise AssertionError(f"unknown index operation: {op['op']}")
assert forward == after
reverse = json.loads(json.dumps(forward))
for op in reversed(ops_doc["operations"]):
    if op["op"] == "replace-entry":
        reverse["entries"][op["index"]] = op["before"]
    elif op["op"] == "replace-authored-counts":
        reverse["authoredCounts"] = op["before"]
    elif op["op"] == "replace-representation-count":
        reverse["representationCounts"] = op["before"]
    elif op["op"] == "append-standalone-envelope":
        assert len(reverse["additionalStandaloneEnvelopes"]) == op["beforeLength"] + 1
        reverse["additionalStandaloneEnvelopes"].pop()
assert reverse == before

before_entries = {e["id"]: e for e in before["entries"]}
after_entries = {e["id"]: e for e in after["entries"]}
changed = [sid for sid in before_entries if before_entries[sid] != after_entries[sid]]
assert sorted(changed) == sorted(IDS)
assert after["authoredCounts"] == {"reviewed": 648, "pending": 200}
assert after["representationCounts"]["completeReviewedStandaloneProcedures"] == 372
for sid in IDS:
    assert after_entries[sid]["authoredStatus"] == "reviewed-authored-operational-playtest"
    assert after_entries[sid]["sourceCatalogWholeCardPointer"] == before_entries[sid]["wholeCardPointer"]
    assert after_entries[sid]["runtimeSelectionEnabled"] is False
assert len(CATALOG.read_bytes()) == acceptance["sourceBindings"]["legacySpellCatalog"]["bytes"]
assert sha(CATALOG.read_bytes()) == acceptance["sourceBindings"]["legacySpellCatalog"]["sha256"]
assert sha(SPELLS_JS.read_bytes()) == acceptance["sourceBindings"]["currentSpellDefinitions"]["sha256"]
assert application["classAccessUnchanged"] and application["sourceCatalogUnchanged"]
assert acceptance["retainedHolds"] == [h["id"] for h in read(PKG / "HOLD_REGISTER.json")]
manifest = read(PKG / "CANDIDATE_PACKAGE_MANIFEST.json")
for item in manifest["files"]:
    p = PKG / item["path"]
    b = p.read_bytes()
    assert len(b) == item["bytes"] and sha(b) == item["sha256"], item["path"]

validation = {
    "id": "RANK7PERCEPTION5-APPLICATION-VALIDATION-134",
    "passed": True,
    "acceptedIdentitiesApplied": len(IDS),
    "acceptedIds": IDS,
    "onlyIdentityEntriesChanged": sorted(changed) == sorted(IDS),
    "forwardOperationsReplayExact": forward == after,
    "reverseOperationsRestoreExactSemantics": reverse == before,
    "reverseByteExactBackup": sha(before_bytes) == ops_doc["before"]["sha256"],
    "retainedHoldIds": acceptance["retainedHolds"],
    "indexCounts": after["authoredCounts"],
    "representationCounts": after["representationCounts"],
    "indexAfter": {"bytes": len(after_bytes), "sha256": sha(after_bytes)},
    "sourceCatalogUnchanged": application["sourceCatalogUnchanged"],
    "classAccessUnchanged": application["classAccessUnchanged"],
    "runtimeSelectionEnabled": False,
    "runtimeImplemented": False,
    "packageFilesBound": len(manifest["files"]),
}
dump(D / "RANK7PERCEPTION5_APPLICATION_VALIDATION_134.json", validation)
manuscript = G / "docs/spells/candidates/RANK7PERCEPTION5_REVIEWED_134.md"
manuscript.parent.mkdir(parents=True, exist_ok=True)
shutil.copyfile(Path(r"C:\R7R134") / "STANDALONE_PROCEDURES.md", manuscript)
print(json.dumps(validation, ensure_ascii=False, indent=2))
