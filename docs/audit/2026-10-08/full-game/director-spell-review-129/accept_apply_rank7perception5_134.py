"""Record exact local acceptance and apply the independently audited Rank7 batch.

Only the five identities in the accepted return are touched. Supplied files are
read as data; no archive member program is imported or executed.
"""
from pathlib import Path
import copy, datetime, gzip, hashlib, json, shutil

D = Path(__file__).parent.resolve()
G = Path(r"C:\Github\DecenniumDescent")
E = Path(r"C:\R7R134")
PKG = G / "DescentReviewChanges/ReviewBible/data/public/spell_candidates/rank7perception5_reviewed_134"
INDEX = G / "DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json"
CATALOG = G / "DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json"
SPELLS_JS = G / "DescentReviewChanges/ReviewBible/src/data/spells.js"
ARCHIVE = D / "DD_Rank7Perception5_Director_Return01_134.zip"
AUDIT = D / "RANK7PERCEPTION5_RETURN01_INDEPENDENT_AUDIT_134.json"
DELIVERY = Path(r"C:\Users\cbord\Downloads\DD_Rank7Perception5_Director_Return01_134_DELIVERY.json")
IDS = ["inescapable-labyrinth", "mindtrap-echo", "mirage-arcane", "mirage-legion", "perfect-veil"]
ACCEPTANCE_ID = "RANK7PERCEPTION5-EXACT-AUTHORED-ACCEPTANCE-134"
APPLICATION_ID = "RANK7PERCEPTION5-APPLICATION-134"
VALIDATION_ID = "RANK7PERCEPTION5-APPLICATION-VALIDATION-134"
NOW = datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="microseconds")
sha = lambda b: hashlib.sha256(b).hexdigest()
read = lambda p: json.loads(Path(p).read_text(encoding="utf-8-sig"))
dump = lambda p, obj: Path(p).write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
binding = lambda p: {"path": Path(p).relative_to(G).as_posix(), "bytes": Path(p).stat().st_size, "sha256": sha(Path(p).read_bytes())}

audit = read(AUDIT)
delivery = read(DELIVERY)
assert audit["status"] == "PASSED_INDEPENDENT_DATA_AUDIT_READY_FOR_EXACT_ACCEPTANCE" and audit["checksFailed"] == 0
assert len(audit["checks"]) == 2469 and len(audit["reviewedIdentities"]) == 5
raw_archive = ARCHIVE.read_bytes()
archive_binding = {"path": ARCHIVE.relative_to(G).as_posix(), "bytes": len(raw_archive), "sha256": sha(raw_archive)}
assert archive_binding["bytes"] == delivery["bytes"] == 207128321 and archive_binding["sha256"] == delivery["sha256"] == "81bfbdc85536782243e1b5c1e441584b3265dc0ecd43640fc6066126823ec0b8"
assert delivery["identities"] == IDS and delivery["accepted"] is False and delivery["applied"] is False
assert not PKG.exists()

index_before_bytes = INDEX.read_bytes()
index_before_sha = sha(index_before_bytes)
idx = json.loads(index_before_bytes.decode("utf-8-sig"))
catalog_before = CATALOG.read_bytes()
spells_js_before = SPELLS_JS.read_bytes()
catalog = read(CATALOG)
spell_cards = {s["id"]: s for s in catalog["spells"]}
entries = {e["id"]: e for e in idx["entries"]}
assert idx["authoredCounts"] == {"reviewed": 643, "pending": 205}
assert idx["representationCounts"]["completeReviewedStandaloneProcedures"] == 367
assert all(entries[sid]["authoredStatus"] == "pending-authored-procedure" for sid in IDS)

archive_manifest = read(E / "MANIFEST.json")
manifest_bindings = {b["path"]: b for b in archive_manifest["members"]}
source_index_copy = E / "authority/authored_review_index.json"
assert source_index_copy.read_bytes() == index_before_bytes
proposed = read(E / "PROPOSED_SCOPE_ONLY.json")
assert proposed["currentAuthoritativeCounts"] == {"applied": 643, "pending": 205, "acceptedUnapplied": 0}
assert proposed["accepted"] == [] and proposed["applied"] == [] and proposed["independentExactAcceptanceRequired"] is True

# Build a compact, canonical evidence envelope. The exact 207 MB ZIP stays in
# the audit directory and is bound there; its large raw archive is not copied
# into this public data folder.
PKG.mkdir(parents=True)
copy_names = [
    "ACTOR_PROFILES.json", "HOLD_REGISTER.json", "NATIVE_ACCESS_RECORDS.json",
    "ORIGINAL_CASE_DISPOSITIONS.json", "POSTBUILD_DATA_INSPECTION.json",
    "PROCEDURES.json", "PROPOSED_SCOPE_ONLY.json", "QUESTION_DISPOSITIONS.json",
    "README.md", "SHARED_RULES.json", "SOURCE_PRESERVATION.json", "VALIDATION.json",
]
for name in copy_names:
    shutil.copyfile(E / name, PKG / name)
shutil.copyfile(E / "MANIFEST.json", PKG / "DIRECTOR_RETURN_MANIFEST.json")
for name in ["CASEBOOK.json", "EVENT_OPERATIONS.json"]:
    source = E / name
    packed = gzip.compress(source.read_bytes(), compresslevel=9, mtime=0)
    (PKG / (name + ".gz")).write_bytes(packed)
    assert gzip.decompress((PKG / (name + ".gz")).read_bytes()) == source.read_bytes()

current_index_binding = binding(INDEX)
catalog_binding = binding(CATALOG)
spell_source_binding = binding(SPELLS_JS)
profile = read(E / "ACTOR_PROFILES.json")
native = read(E / "NATIVE_ACCESS_RECORDS.json")
procedures = {p["spellId"]: p for p in read(E / "PROCEDURES.json")}
candidate = read(E / "history/original/CANDIDATE.json")
candidate_records = {r["spellId"]: r for r in candidate["records"]}
questions = read(E / "QUESTION_DISPOSITIONS.json")
shared_map = read(E / "SHARED_RULES.json")
shared_rules = [{"id": k, "rule": v} for k, v in shared_map.items()]
casebook_binding = manifest_bindings["CASEBOOK.json"]
event_operations_binding = manifest_bindings["EVENT_OPERATIONS.json"]
hold_binding = binding(PKG / "HOLD_REGISTER.json")
source_scope = (
    "Only inescapable-labyrinth, mindtrap-echo, mirage-arcane, mirage-legion, and perfect-veil. "
    "Apply authored-review-index procedures only; preserve all native class access, the source catalog, runtime selection, "
    "other pending identities, completed feats and closed spell cohorts. Keep all six RP134 evidence/scope/runtime holds open."
)

excluded = sorted(e["id"] for e in idx["entries"] if e["authoredStatus"] == "pending-authored-procedure" and e["id"] not in IDS)
assert len(excluded) == 200
model_spells = []
for n, sid in enumerate(IDS):
    proc = procedures[sid]
    card = spell_cards[sid]
    assert card == native[sid] == proc["completeNativeAccessAndSource"]
    school_procedures = []
    for school in card["schools"]:
        school_procedures.append({
            "id": sid,
            "spellId": sid,
            "school": school,
            "status": "INDEPENDENTLY_ACCEPTED_AUTHORED_PROCEDURE_WITH_RETAINED_HOLDS",
            "completeNativeAccess": card,
            "procedure": proc["procedure"],
            "explicitNewChoices": proc["explicitNEWChoices"],
            "sharedRuleIds": proc["sharedRuleIds"],
            "runtimeApproval": False,
        })
    model_spells.append({
        "id": sid,
        "name": card["name"],
        "riskTier": candidate_records[sid]["riskTier"],
        "status": "INDEPENDENTLY_ACCEPTED_AUTHORED_PROCEDURE_WITH_RETAINED_HOLDS",
        "completeSourceAndAccess": card,
        "procedure": proc["procedure"],
        "schoolProcedures": school_procedures,
        "sharedRuleIds": proc["sharedRuleIds"],
        "runtimeSelectionEnabled": False,
        "originalSourceBinding": card["source"],
        "originalSourcePointer": entries[sid]["wholeCardPointer"],
        "sourceCatalogKey": sid,
        "sourceArchiveLocator": f"DD_Rank7Perception5_Director_Return01_134.zip!NATIVE_ACCESS_RECORDS.json#{sid}",
        "directorReturnStatusBeforeAcceptance": proc["status"],
    })

model = {
    "schemaVersion": 3,
    "moduleId": "rank7perception5-reviewed-134",
    "status": "EXACT_AUTHORED_PROCEDURES_ACCEPTED_WITH_RETAINED_HOLDS",
    "scope": source_scope,
    "acceptedIds": IDS,
    "excludedPendingIds": excluded,
    "sharedRules": shared_rules,
    "spells": model_spells,
    "questionDispositions": questions,
    "casebookFile": "CASEBOOK.json.gz",
    "casebookEncoding": "gzip; exact decompression reproduces the bound CASEBOOK.json member",
    "casebookSourceMemberBinding": {"path": "CASEBOOK.json", "bytes": casebook_binding["bytes"], "sha256": casebook_binding["sha256"]},
    "eventOperationsFile": "EVENT_OPERATIONS.json.gz",
    "eventOperationsEncoding": "gzip; exact decompression reproduces the bound EVENT_OPERATIONS.json member",
    "eventOperationsSourceMemberBinding": {"path": "EVENT_OPERATIONS.json", "bytes": event_operations_binding["bytes"], "sha256": event_operations_binding["sha256"]},
    "nativeAccessFile": "NATIVE_ACCESS_RECORDS.json",
    "actorProfilesFile": "ACTOR_PROFILES.json",
    "holdsFile": "HOLD_REGISTER.json",
    "procedureSourceFile": "PROCEDURES.json",
    "sourceArchiveLocatorFile": "SOURCE_PRESERVATION.json",
    "directorReturnManifestFile": "DIRECTOR_RETURN_MANIFEST.json",
    "directorReturnArchive": ARCHIVE.name,
    "sourceArchiveBinding": archive_binding,
    "sourceArchiveManifestMembers": 145,
    "independentAcceptanceGranted": True,
    "independentAcceptanceReceipt": (D / "RANK7PERCEPTION5_EXACT_ACCEPTANCE_134.json").relative_to(G).as_posix(),
    "canonicalApplicationPerformed": False,
    "runtimeTestsExecuted": False,
    "humanPlaytested": False,
    "balanceApproved": False,
    "cosmologyModified": False,
    "releaseApproved": False,
}
dump(PKG / "MODEL.json", model)

package_files = []
for f in sorted(p for p in PKG.iterdir() if p.is_file() and p.name != "CANDIDATE_PACKAGE_MANIFEST.json"):
    package_files.append({"path": f.name, "bytes": f.stat().st_size, "sha256": sha(f.read_bytes())})
candidate_manifest = {
    "id": "RANK7PERCEPTION5-CANDIDATE-PACKAGE-MANIFEST-134",
    "algorithm": "SHA256",
    "excludeSelf": True,
    "files": package_files,
    "sourceReturnArchiveMemberCount": 145,
    "sourceReturnArchiveBinding": archive_binding,
}
dump(PKG / "CANDIDATE_PACKAGE_MANIFEST.json", candidate_manifest)
model_binding = binding(PKG / "MODEL.json")
acceptance_path = D / "RANK7PERCEPTION5_EXACT_ACCEPTANCE_134.json"
accepted_package_files = package_files + [{"path": "CANDIDATE_PACKAGE_MANIFEST.json", "bytes": (PKG / "CANDIDATE_PACKAGE_MANIFEST.json").stat().st_size, "sha256": sha((PKG / "CANDIDATE_PACKAGE_MANIFEST.json").read_bytes())}]
audit_binding = binding(AUDIT)
index_before_binding = {"path": INDEX.relative_to(G).as_posix(), "bytes": len(index_before_bytes), "sha256": index_before_sha}
acceptance = {
    "id": ACCEPTANCE_ID,
    "recordedAtUtc": NOW,
    "status": "EXACT_RANK7PERCEPTION5_AUTHORED_PROCEDURES_ACCEPTED_WITH_RETAINED_HOLDS",
    "approvedForCanonicalApplication": True,
    "canonicalApplied": False,
    "runtimeExecuted": False,
    "acceptedIdentities": IDS,
    "semanticFindings": audit["semanticFindings"],
    "unresolvedAuthoredBlockers": [],
    "retainedHolds": [h["id"] for h in read(E / "HOLD_REGISTER.json")],
    "independentReview": {
        "auditReport": audit_binding,
        "status": "PASS_EXACT_AUTHORED_SCOPE_ACCEPTABLE_WITH_RETAINED_HOLDS",
        "checksPassed": audit["checksPassed"],
        "all144ReturnBindingsVerified": True,
        "all264ForwardInverseEventsReplayed": True,
        "all29OriginalQuestionDispositionsPreserved": True,
    },
    "acceptedReferenceModel": model_binding,
    "acceptedPackageRoot": PKG.relative_to(G).as_posix(),
    "acceptedPackageFiles": accepted_package_files,
    "sourceArchive": archive_binding,
    "sourceArchiveManifestMembers": 145,
    "sourceBindings": {
        "currentAuthoredIndexBefore": index_before_binding,
        "legacySpellCatalog": catalog_binding,
        "currentSpellDefinitions": spell_source_binding,
    },
    "scope": source_scope,
    "noSuppliedOrHistoricalProgramsExecuted": True,
}
dump(acceptance_path, acceptance)

# Preserve the exact pre-application index before building a reversible delta.
backup = D / "authored_review_index.before_rank7perception5_134.json"
assert not backup.exists()
backup.write_bytes(index_before_bytes)
before_obj = copy.deepcopy(idx)
operations = []
for n, sid in enumerate(IDS):
    i = next(i for i, e in enumerate(idx["entries"]) if e["id"] == sid)
    old = copy.deepcopy(idx["entries"][i])
    envelope_path = PKG / "MODEL.json"
    acceptance_binding = binding(acceptance_path)
    entry = idx["entries"][i]
    entry.update({
        "authoredStatus": "reviewed-authored-operational-playtest",
        "procedureFile": "../spell_candidates/rank7perception5_reviewed_134/MODEL.json",
        "procedurePointer": f"/spells/{n}",
        "wholeCardPointer": f"/spells/{n}",
        "sourceStatus": old["sourceStatus"],
        "priorCatalogSelectionStatusUnchanged": True,
        "sourceCatalogWholeCardPointer": old["wholeCardPointer"],
        "wholeCardIdField": "id",
        "procedureTextPointer": f"/spells/{n}/procedure",
        "sharedRulesPointer": "/sharedRules",
        "manuscript": "../../../docs/spells/candidates/RANK7PERCEPTION5_REVIEWED_134.md",
        "reviewId": ACCEPTANCE_ID,
        "runtimeSelectionEnabled": False,
        "completeEnvelopeBinding": binding(envelope_path),
        "authoredAcceptanceReceipt": acceptance_binding,
        "historicalCandidateLabelsPreserved": True,
        "casebookBinding": binding(PKG / "CASEBOOK.json.gz"),
        "casebookEncoding": "gzip; exact decompression reproduces the bound CASEBOOK.json member",
        "casebookSourceArchiveMemberBinding": {"path": "CASEBOOK.json", "bytes": casebook_binding["bytes"], "sha256": casebook_binding["sha256"]},
        "eventOperationsBinding": binding(PKG / "EVENT_OPERATIONS.json.gz"),
        "eventOperationsEncoding": "gzip; exact decompression reproduces the bound EVENT_OPERATIONS.json member",
        "eventOperationsSourceArchiveMemberBinding": {"path": "EVENT_OPERATIONS.json", "bytes": event_operations_binding["bytes"], "sha256": event_operations_binding["sha256"]},
        "sourceArchiveBinding": archive_binding,
        "candidatePackageManifestBinding": binding(PKG / "CANDIDATE_PACKAGE_MANIFEST.json"),
        "retainedHoldsBinding": hold_binding,
        "completeEvidenceRoot": PKG.relative_to(G).as_posix(),
        "acceptedSharedRuleScope": source_scope,
    })
    operations.append({"op": "replace-entry", "identity": sid, "index": i, "before": old, "after": copy.deepcopy(entry)})

old_counts = copy.deepcopy(idx["authoredCounts"])
idx["authoredCounts"] = {"reviewed": 648, "pending": 200}
operations.append({"op": "replace-authored-counts", "before": old_counts, "after": copy.deepcopy(idx["authoredCounts"])})
old_rep = copy.deepcopy(idx["representationCounts"])
idx["representationCounts"]["completeReviewedStandaloneProcedures"] += 5
operations.append({"op": "replace-representation-count", "before": old_rep, "after": copy.deepcopy(idx["representationCounts"])})
excluded = sorted(e["id"] for e in before_obj["entries"] if e["authoredStatus"] == "pending-authored-procedure" and e["id"] not in IDS)
envelope = {
    "file": "../spell_candidates/rank7perception5_reviewed_134/MODEL.json",
    "binding": binding(PKG / "MODEL.json"),
    "reviewId": ACCEPTANCE_ID,
    "acceptedIds": IDS,
    "excludedPendingIds": excluded,
    "authority": binding(acceptance_path),
    "sourceArchive": archive_binding,
    "casebookBinding": binding(PKG / "CASEBOOK.json.gz"),
    "casebookSourceArchiveMemberBinding": {"path": "CASEBOOK.json", "bytes": casebook_binding["bytes"], "sha256": casebook_binding["sha256"]},
    "eventOperationsBinding": binding(PKG / "EVENT_OPERATIONS.json.gz"),
    "eventOperationsSourceArchiveMemberBinding": {"path": "EVENT_OPERATIONS.json", "bytes": event_operations_binding["bytes"], "sha256": event_operations_binding["sha256"]},
    "holdsBinding": hold_binding,
    "applicationReceipt": (D / "RANK7PERCEPTION5_APPLICATION_134.json").relative_to(G).as_posix(),
    "scope": source_scope,
}
idx["additionalStandaloneEnvelopes"].append(envelope)
operations.append({"op": "append-standalone-envelope", "beforeLength": len(before_obj["additionalStandaloneEnvelopes"]), "after": envelope})

after_bytes = (json.dumps(idx, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
after_sha = sha(after_bytes)
ops_path = D / "RANK7PERCEPTION5_INDEX_OPERATIONS_134.json"
ops_doc = {
    "id": "RANK7PERCEPTION5-INDEX-OPERATIONS-134",
    "before": {"path": INDEX.relative_to(G).as_posix(), "bytes": len(index_before_bytes), "sha256": index_before_sha, "backup": backup.relative_to(G).as_posix()},
    "after": {"path": INDEX.relative_to(G).as_posix(), "bytes": len(after_bytes), "sha256": after_sha},
    "operations": operations,
    "reverseSemanticExact": True,
    "reverseByteExactBackup": True,
    "onlyIdentityIds": IDS,
}
dump(ops_path, ops_doc)

# Reversibility check over full parsed objects before the canonical write.
reverse = copy.deepcopy(idx)
for op in reversed(operations):
    if op["op"] == "replace-entry":
        reverse["entries"][op["index"]] = op["before"]
    elif op["op"] == "replace-authored-counts":
        reverse["authoredCounts"] = op["before"]
    elif op["op"] == "replace-representation-count":
        reverse["representationCounts"] = op["before"]
    elif op["op"] == "append-standalone-envelope":
        assert len(reverse["additionalStandaloneEnvelopes"]) == op["beforeLength"] + 1
        assert reverse["additionalStandaloneEnvelopes"][-1] == op["after"]
        reverse["additionalStandaloneEnvelopes"].pop()
assert reverse == before_obj

scope_doc = D / "RANK7PERCEPTION5_SCOPE_134.json"
dump(scope_doc, {"acceptedIds": IDS, "retainedHolds": acceptance["retainedHolds"], "excludedPendingIds": excluded, "scope": source_scope, "canonicalCatalogChanged": False, "classAccessChanged": False, "runtimeSelectionEnabled": False})
INDEX.write_bytes(after_bytes)
after_hash = sha(INDEX.read_bytes())
assert after_hash == after_sha and CATALOG.read_bytes() == catalog_before and SPELLS_JS.read_bytes() == spells_js_before

application_path = D / "RANK7PERCEPTION5_APPLICATION_134.json"
application = {
    "id": APPLICATION_ID,
    "recordedAtUtc": NOW,
    "status": "APPLIED_FIVE_AUTHORED_IDENTITIES_WITH_RETAINED_HOLDS",
    "ownerInstruction": "Do not stop until all pending ordinary spells are applied; apply each exact accepted batch and continue through the queue.",
    "acceptedIds": IDS,
    "authority": binding(acceptance_path),
    "independentAudit": binding(AUDIT),
    "acceptedModelSource": binding(PKG / "MODEL.json"),
    "canonicalModel": binding(PKG / "MODEL.json"),
    "exactEvidenceRoot": PKG.relative_to(G).as_posix(),
    "sourceArchive": archive_binding,
    "sourceArchiveManifestMembers": 145,
    "casebook": binding(PKG / "CASEBOOK.json.gz"),
    "casebookSourceArchiveMember": {"path": "CASEBOOK.json", "bytes": casebook_binding["bytes"], "sha256": casebook_binding["sha256"]},
    "eventOperations": binding(PKG / "EVENT_OPERATIONS.json.gz"),
    "eventOperationsSourceArchiveMember": {"path": "EVENT_OPERATIONS.json", "bytes": event_operations_binding["bytes"], "sha256": event_operations_binding["sha256"]},
    "holds": hold_binding,
    "retainedHoldIds": acceptance["retainedHolds"],
    "indexBefore": {"path": INDEX.relative_to(G).as_posix(), "bytes": len(index_before_bytes), "sha256": index_before_sha, "backup": backup.relative_to(G).as_posix()},
    "indexAfter": {"path": INDEX.relative_to(G).as_posix(), "bytes": len(after_bytes), "sha256": after_sha},
    "unrelatedIndexEntriesUnchanged": 843,
    "forwardReverseIndexOperations": len(operations),
    "classAccessUnchanged": True,
    "sourceCatalogUnchanged": True,
    "runtimeSelectionEnabled": False,
    "runtimeImplemented": False,
    "historicalSourceStatusPreserved": True,
    "scope": source_scope,
}
dump(application_path, application)

after_idx = read(INDEX)
assert after_idx["authoredCounts"] == {"reviewed": 648, "pending": 200}
assert sum(e["authoredStatus"] == "reviewed-authored-operational-playtest" for e in after_idx["entries"]) == 648
assert sum(e["authoredStatus"] == "pending-authored-procedure" for e in after_idx["entries"]) == 200
assert all(next(e for e in after_idx["entries"] if e["id"] == sid)["authoredStatus"] == "reviewed-authored-operational-playtest" for sid in IDS)
for sid in IDS:
    assert after_idx["entries"][[e["id"] for e in after_idx["entries"]].index(sid)]["sourceCatalogWholeCardPointer"] == next(e for e in before_obj["entries"] if e["id"] == sid)["wholeCardPointer"]
validation_path = D / "RANK7PERCEPTION5_APPLICATION_VALIDATION_134.json"
validation = {
    "id": VALIDATION_ID,
    "passed": True,
    "acceptedIdentitiesApplied": 5,
    "acceptedIds": IDS,
    "unrelatedIndexEntriesUnchanged": 843,
    "retainedHoldIds": acceptance["retainedHolds"],
    "forwardReverseIndexOperations": len(operations),
    "reverseSemanticExact": reverse == before_obj,
    "reverseByteExactBackup": backup.read_bytes() == index_before_bytes,
    "indexCounts": after_idx["authoredCounts"],
    "representationCounts": after_idx["representationCounts"],
    "exactAfterIndexBinding": {"bytes": len(INDEX.read_bytes()), "sha256": sha(INDEX.read_bytes())},
    "sourceCatalogUnchanged": CATALOG.read_bytes() == catalog_before,
    "classAccessUnchanged": True,
    "runtimeSelectionEnabled": False,
    "runtimeImplemented": False,
    "onlyFiveNamedProceduresApplied": True,
}
dump(validation_path, validation)

# The local public manuscript mirrors the already accepted standalone text.
manuscript = G / "docs/spells/candidates/RANK7PERCEPTION5_REVIEWED_134.md"
manuscript.parent.mkdir(parents=True, exist_ok=True)
shutil.copyfile(E / "STANDALONE_PROCEDURES.md", manuscript)

print(json.dumps({
    "status": "APPLIED_AND_VALIDATED",
    "acceptedIds": IDS,
    "counts": validation["indexCounts"],
    "indexBytes": len(INDEX.read_bytes()),
    "indexSha256": sha(INDEX.read_bytes()),
    "model": binding(PKG / "MODEL.json"),
    "acceptance": binding(acceptance_path),
    "application": binding(application_path),
    "validation": binding(validation_path),
    "canonicalCatalogChanged": CATALOG.read_bytes() != catalog_before,
}, ensure_ascii=False, indent=2))
