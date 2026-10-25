from pathlib import Path
import datetime, hashlib, json, zipfile

D = Path(__file__).parent.resolve()
G = Path(r"C:\Github\DecenniumDescent")
INDEX = G / "DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json"
CATALOG = G / "DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json"
WARD_ARCHIVE = G / "docs/audit/2026-10-08/full-game/DD_Ward_7_Source_Conference_01.zip"
NOW = datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="microseconds")
sha = lambda b: hashlib.sha256(b).hexdigest()
read = lambda p: json.loads(Path(p).read_text(encoding="utf-8-sig"))
dump = lambda p, x: Path(p).write_text(json.dumps(x, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
def binding(p):
    p = Path(p).resolve()
    try:
        label = p.relative_to(G).as_posix()
    except ValueError:
        label = str(p)
    data = p.read_bytes()
    return {"path": label, "bytes": len(data), "sha256": sha(data)}

ids = ["inescapable-labyrinth", "mindtrap-echo", "mirage-arcane", "mirage-legion", "perfect-veil"]
index_bytes = INDEX.read_bytes()
index = json.loads(index_bytes.decode("utf-8-sig"))
assert index["authoredCounts"] == {"reviewed": 648, "pending": 200}
entries = {e["id"]: e for e in index["entries"]}
assert all(entries[s]["authoredStatus"] == "reviewed-authored-operational-playtest" for s in ids)
pending = sorted(e["id"] for e in index["entries"] if e["authoredStatus"] == "pending-authored-procedure")
assert len(pending) == 200
catalog = read(CATALOG)
cards = {s["id"]: s for s in catalog["spells"]}
pending_audit = {
    "id": "CURRENT200-PENDING-IDENTITY-AUDIT-134",
    "recordedAtUtc": NOW,
    "status": "PASSED_EXACT_CURRENT_INDEX_PENDING_SET",
    "indexBinding": binding(INDEX),
    "catalogBinding": binding(CATALOG),
    "authoredCounts": index["authoredCounts"],
    "pendingCount": len(pending),
    "pendingIds": pending,
    "allPendingExistInSourceCatalog": all(s in cards for s in pending),
    "closed335AndCompletedCohortsReopened": False,
}
assert pending_audit["allPendingExistInSourceCatalog"]
dump(D / "CURRENT200_PENDING_IDENTITY_AUDIT_134.json", pending_audit)

accepted = D / "RANK7PERCEPTION5_EXACT_ACCEPTANCE_134.json"
applied = D / "RANK7PERCEPTION5_APPLICATION_134.json"
validated = D / "RANK7PERCEPTION5_APPLICATION_VALIDATION_134.json"
archive = D / "DD_Rank7Perception5_Director_Return01_134.zip"
delivery = Path(r"C:\Users\cbord\Downloads\DD_Rank7Perception5_Director_Return01_134_DELIVERY.json")
rank7 = {
    "status": "exact-return-received-independently-audited-accepted-applied",
    "identities": ids,
    "currentCounts": {"appliedReviewed": 648, "indexPending": 200, "acceptedUnapplied": 0},
    "returnArchive": binding(archive),
    "deliveryRecord": binding(delivery),
    "independentAudit": binding(D / "RANK7PERCEPTION5_RETURN01_INDEPENDENT_AUDIT_134.json"),
    "acceptanceReceipt": binding(accepted),
    "applicationReceipt": binding(applied),
    "validationReceipt": binding(validated),
}
receipt = read(D / "RANK7PERCEPTION5_SENT_133.json")
receipt["id"] = "RANK7PERCEPTION5-HANDOFF-134"
receipt["recordedAtUtc"] = NOW
receipt["status"] = rank7["status"].upper().replace("-", "_")
receipt["currentCounts"] = {"reviewedApplied": 648, "pending": 200, "acceptedUnapplied": 0}
receipt["directorReturn"] = rank7["returnArchive"]
receipt["deliveryRecord"] = rank7["deliveryRecord"]
receipt["independentAudit"] = rank7["independentAudit"]
receipt["acceptanceReceipt"] = rank7["acceptanceReceipt"]
receipt["applicationReceipt"] = rank7["applicationReceipt"]
receipt["validationReceipt"] = rank7["validationReceipt"]
receipt["recoveryStatus"] = "RETURN_VERIFIED_ACCEPTED_APPLIED; WARD7_RETURN_NEXT"
dump(D / "RANK7PERCEPTION5_SENT_134.json", receipt)

queue = read(D / "CURRENT_SPELL_QUEUE_133.json")
queue["id"] = "SPELL-REVIEW-QUEUE-134"
queue["recordedAtUtc"] = NOW
queue["lastUpdatedAtUtc"] = NOW
queue["currentCounts"] = {
    "appliedReviewed": 648, "indexPending": 200, "acceptedUnapplied": 0,
    "needsAcceptance": 200, "submittedAwaitingReturn": 200,
    "otherUnaccepted": 0, "missingReturnArtifacts": 0,
    "historicalMissingReturnReconstructionPending": 8, "returnedNeedsCorrection": 0,
}
for group in queue["groups"]:
    if group["group"] == "rank7-perception5":
        group["currentPhase"] = "applied-authored-review-134-with-retained-holds"
        group["previousPhase"] = "returned-audited-accepted-134"
        group["applicationReceipt"] = str(applied)
        group["exactAcceptanceReceipt"] = str(accepted)
    elif group["group"] == "ward7":
        group["currentPhase"] = "director-source-verified-return-pending"
        group["currentCounts"] = queue["currentCounts"]
        group["latestDirectorStatus"] = "GPT reports source verification complete; authored return unfinished"
        group["nextAction"] = "Resume saved Ward7 files and deliver exact complete return; then continue remaining queue."
queue["nextSuggestedGroups"] = [g for g in queue.get("nextSuggestedGroups", []) if g != "rank7-perception5"]
queue["acceptedIdentities"] = list(dict.fromkeys(queue.get("acceptedIdentities", []) + ids))
queue["appliedAcceptedIdentities"] = list(dict.fromkeys(queue.get("appliedAcceptedIdentities", []) + ids))
queue["latestAcceptanceReceipts"] = list(dict.fromkeys(queue.get("latestAcceptanceReceipts", []) + [str(accepted)]))
queue["latestApplicationReceipts"] = list(dict.fromkeys(queue.get("latestApplicationReceipts", []) + [str(applied)]))
queue["lastAppliedIdentity"] = {"id": ids[-1], "acceptance": str(accepted), "application": str(applied), "validation": str(validated)}
queue["currentPendingIdentityAudit"] = str(D / "CURRENT200_PENDING_IDENTITY_AUDIT_134.json")
queue["rank7Perception5Handoff"] = {**rank7, "receipt": binding(D / "RANK7PERCEPTION5_SENT_134.json")}
queue["directorConnectionStatus"] = "Rank7 return accepted/applied; GPT reports Ward7 source verification complete and return unfinished; refreshed 648/200 context is next."
queue["resumePriority"] = "Complete the seven Ward7 identities from saved source-verified work; independently audit and apply each exact accepted batch, then proceed through all remaining 200 pending ordinary spells."
dump(D / "CURRENT_SPELL_QUEUE_134.json", queue)

handoff = read(D / "CURRENT_HANDOFF_133.json")
handoff["id"] = "ORDINARY-SPELL-REVIEW-HANDOFF-134"
handoff["recordedAtUtc"] = NOW
handoff["lastUpdatedAtUtc"] = NOW
handoff["status"] = "RANK7PERCEPTION5_APPLIED_WARD7_RETURN_PENDING_200_PENDING"
handoff["currentCounts"] = {"reviewedApplied": 648, "pending": 200, "standalone": 372, "scopedInterfaces": 173, "acceptedUnapplied": 0}
handoff.setdefault("appliedThisTurn", {})["Rank7Perception5"] = ids
handoff["applicationReceipts"] = list(dict.fromkeys(handoff.get("applicationReceipts", []) + [str(applied)]))
handoff["lastAppliedIdentity"] = queue["lastAppliedIdentity"]
handoff["currentSpellQueue"] = str(D / "CURRENT_SPELL_QUEUE_134.json")
handoff["currentPendingIdentityAudit"] = str(D / "CURRENT200_PENDING_IDENTITY_AUDIT_134.json")
handoff["next"] = "Finish the seven-identity Ward7 return from GPT's saved source-verified work, independently audit and apply it, then continue all remaining groups until all 200 pending ordinary spells are applied."
handoff["nextPreparedPacket"] = "Ward7 seven-identity group"
handoff["nextPacket"] = {
    "sourceArchive": binding(WARD_ARCHIVE),
    "sourceCheck": binding(G / "docs/audit/2026-10-08/full-game/WARD_7_SOURCE_CONFERENCE_01_CHECK.json"),
    "request": binding(G / "docs/audit/2026-10-08/full-game/WARD_7_SOURCE_CONFERENCE_01_REQUEST.txt"),
    "identities": queue["groups"][[g["group"] for g in queue["groups"]].index("ward7")]["identities"],
}
handoff["rank7Perception5Handoff"] = {**rank7, "receipt": binding(D / "RANK7PERCEPTION5_SENT_134.json")}
handoff["ward7Handoff"] = {
    "status": "source-verified-return-unfinished-resume-request-ready",
    "currentCounts": queue["currentCounts"],
    "sourceArchive": binding(WARD_ARCHIVE),
    "identities": handoff["nextPacket"]["identities"],
    "gptLastOutput": "Ward7 source verification is complete; its return is still unfinished.",
}
dump(D / "CURRENT_HANDOFF_134.json", handoff)

# A compact fresh authority packet for GPT; exclude prior raw return archives.
context_zip = D / "DD_Rank7Perception5_Applied_Ward7_Context_134.zip"
members = [
    (INDEX, "authority/authored_review_index.json"),
    (CATALOG, "authority/catalog.json"),
    (D / "CURRENT_SPELL_QUEUE_134.json", "authority/CURRENT_SPELL_QUEUE_134.json"),
    (D / "CURRENT_HANDOFF_134.json", "authority/CURRENT_HANDOFF_134.json"),
    (D / "CURRENT200_PENDING_IDENTITY_AUDIT_134.json", "authority/CURRENT200_PENDING_IDENTITY_AUDIT_134.json"),
    (D / "RANK7PERCEPTION5_EXACT_ACCEPTANCE_134.json", "rank7/EXACT_ACCEPTANCE.json"),
    (D / "RANK7PERCEPTION5_APPLICATION_134.json", "rank7/APPLICATION.json"),
    (D / "RANK7PERCEPTION5_APPLICATION_VALIDATION_134.json", "rank7/APPLICATION_VALIDATION.json"),
    (G / "DescentReviewChanges/ReviewBible/data/public/spell_candidates/rank7perception5_reviewed_134/MODEL.json", "rank7/MODEL.json"),
    (G / "DescentReviewChanges/ReviewBible/data/public/spell_candidates/rank7perception5_reviewed_134/HOLD_REGISTER.json", "rank7/HOLD_REGISTER.json"),
    (G / "docs/audit/2026-10-08/full-game/WARD_7_SOURCE_CONFERENCE_01_CHECK.json", "ward7/SOURCE_CHECK.json"),
    (G / "docs/audit/2026-10-08/full-game/WARD_7_SOURCE_CONFERENCE_01_PREPARATION.json", "ward7/SOURCE_PREPARATION.json"),
    (G / "docs/audit/2026-10-08/full-game/WARD_7_SOURCE_CONFERENCE_01_REQUEST.txt", "ward7/SOURCE_REQUEST.txt"),
    (WARD_ARCHIVE, "ward7/DD_Ward_7_Source_Conference_01.zip"),
]
with zipfile.ZipFile(context_zip, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=6) as z:
    for p, name in members:
        z.write(p, name)
context_manifest = {"id": "RANK7PERCEPTION5-APPLIED-WARD7-CONTEXT-134", "sourceBindings": [
    {"path": name, "bytes": Path(p).stat().st_size, "sha256": sha(Path(p).read_bytes())} for p, name in members
]}
dump(D / "RANK7PERCEPTION5_APPLIED_WARD7_CONTEXT_134.json", context_manifest)
with zipfile.ZipFile(context_zip, "r") as z:
    assert z.testzip() is None
context_binding = binding(context_zip)
dump(D / "RANK7PERCEPTION5_APPLIED_WARD7_CONTEXT_134_DELIVERY.json", {"contextArchive": context_binding, "manifest": context_manifest})
print(json.dumps({"counts": queue["currentCounts"], "pendingAudit": binding(D / "CURRENT200_PENDING_IDENTITY_AUDIT_134.json"), "ward7Archive": binding(WARD_ARCHIVE), "context": context_binding, "queue": binding(D / "CURRENT_SPELL_QUEUE_134.json"), "handoff": binding(D / "CURRENT_HANDOFF_134.json")}, indent=2))
