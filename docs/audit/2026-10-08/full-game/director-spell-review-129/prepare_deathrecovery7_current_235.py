from __future__ import annotations

import copy
import hashlib
import json
import subprocess
import zipfile
import zlib
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[5]
FULL = ROOT / "docs/audit/2026-10-08/full-game"
BASE = FULL / "director-spell-review-129"
GROUP = "rank9-death-recovery7"
TARGETS = ["final-word"]
AUTHORITY = {"reviewedApplied": 811, "pending": 37, "acceptedUnapplied": 0, "completeStandaloneProcedures": 535, "scopedInterfaces": 173}
INDEX = "DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json"
CATALOG = "DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json"
ACCESS = "DescentReviewChanges/ReviewBible/data/director/spell_review/accepted_interface_registry_06.json"
WORK_QUEUE = "DescentReviewChanges/ReviewBible/data/director/spell_review/remaining_work_queue_66.json"
CHAT = "https://chatgpt.com/g/g-p-67f17555a8dc8191a2b5b81e6d8adc12-dungeon-crawler/c/6adc506d-8770-83ea-b64c-0345d9b9b682"
OUT = BASE / "rank9_deathrecovery7_current_source_235_prepared"


def enc(value) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8")


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def crc(raw: bytes) -> str:
    return f"{zlib.crc32(raw) & 0xffffffff:08x}"


def info(path: Path, raw: bytes | None = None) -> dict:
    data = path.read_bytes() if raw is None else raw
    return {"path": path.relative_to(ROOT).as_posix(), "bytes": len(data), "sha256": sha(data), "crc32": crc(data)}


def read(path: Path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def safe(name: str) -> bool:
    p = PurePosixPath(name)
    return bool(name) and "\\" not in name and not p.is_absolute() and all(part not in ("", ".", "..") for part in p.parts)


def add(files: dict[str, bytes], name: str, raw: bytes) -> None:
    assert safe(name), name
    assert name not in files, name
    files[name] = raw


def main() -> None:
    branch = subprocess.check_output(["git", "branch", "--show-current"], cwd=ROOT, text=True).strip()
    commit = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    assert branch == "main", branch
    now = datetime.now(timezone.utc).isoformat()
    qpath = BASE / "CURRENT_SPELL_QUEUE_235.json"
    hpath = BASE / "CURRENT_HANDOFF_235.json"
    ppath = BASE / "CURRENT37_PENDING_IDENTITY_AUDIT_235.json"
    q, h, p = read(qpath), read(hpath), read(ppath)
    assert q["currentAuthority"] == h["currentAuthority"] == p["authority"] == AUTHORITY
    assert q["nextGroup"] == GROUP and q["next"]["pendingIds"] == TARGETS
    assert q["status"] == "RETURN234_AUDITED_HELD_811_37_0_PACKET235_PREPARATION"

    index_path, catalog_path, access_path, work_queue_path = (ROOT / x for x in (INDEX, CATALOG, ACCESS, WORK_QUEUE))
    index, catalog, access = read(index_path), read(catalog_path), read(access_path)
    assert index["authoredCounts"] == {"reviewed": 811, "pending": 37}
    assert index["representationCounts"]["completeReviewedStandaloneProcedures"] == 535
    entries = {item["id"]: item for item in index["entries"]}
    spells = {item["id"]: item for item in catalog["spells"]}
    pending = sorted(item["id"] for item in index["entries"] if item.get("authoredStatus") == "pending-authored-procedure")
    assert len(pending) == 37 and "final-word" in pending
    target_entry = entries["final-word"]
    target_spell = spells["final-word"]
    assert target_entry.get("authoredStatus") == "pending-authored-procedure"
    assert target_spell.get("id") == "final-word" and target_spell.get("operational") is None

    group_row = next(item for item in q["currentPendingGroups"] if item["group"] == GROUP)
    assert group_row["pendingIds"] == TARGETS and group_row["pendingCount"] == 1
    historical_candidate_path = ROOT / group_row["candidate"]["path"]
    historical_archive_path = ROOT / group_row["archive"]["path"]
    historical_candidate = read(historical_candidate_path)
    assert info(historical_candidate_path)["sha256"] == group_row["candidate"]["sha256"]
    assert info(historical_archive_path)["sha256"] == group_row["archive"]["sha256"]
    old_record = next(row for row in historical_candidate["records"] if row.get("spellId") == "final-word")

    # Preserve the original source conference's evidence while refreshing every
    # one of its 74 source paths to current working-tree bytes.
    with zipfile.ZipFile(historical_archive_path) as old_zip:
        assert old_zip.testzip() is None
        historical_source_candidate = json.loads(old_zip.read("CANDIDATE.json").decode("utf-8-sig"))
        assert historical_source_candidate["sourceBindings"] == historical_candidate["sourceBindings"]
        source_bindings, source_files, changed = [], {}, []
        for old in historical_candidate["sourceBindings"]:
            rel = old["path"]
            raw_old = old_zip.read("sources/" + rel)
            assert (len(raw_old), sha(raw_old)) == (old["bytes"], old["sha256"]), rel
            current_path = ROOT / rel
            current_raw = current_path.read_bytes()
            record = {"path": rel, "bytes": len(current_raw), "sha256": sha(current_raw), "crc32": crc(current_raw)}
            source_bindings.append(record)
            source_files["sources_current/" + rel] = current_raw
            if (len(current_raw), sha(current_raw)) != (old["bytes"], old["sha256"]):
                changed.append({"path": rel, "historicalBytes": old["bytes"], "historicalSha256": old["sha256"], "currentBytes": len(current_raw), "currentSha256": sha(current_raw)})
    assert len(source_bindings) == len(source_files) == 74 and len({row["path"] for row in source_bindings}) == 74

    r184_archive = BASE / "rank9_deathrecovery7_return184_received/DD_Rank9_DeathRecovery7_Director_Return184.zip"
    r184_delivery = BASE / "rank9_deathrecovery7_return184_received/DD_Rank9_DeathRecovery7_Director_Return184_DELIVERY.json"
    r184_audit = BASE / "RANK9_DEATHRECOVERY7_RETURN184_INDEPENDENT_AUDIT.json"
    r184_decision = BASE / "RANK9_DEATHRECOVERY7_GPT_RETURN_184.json"
    r184_extracted_decision = BASE / "rank9_deathrecovery7_return184_received/DIRECTOR_DECISION_184_EXTRACTED.json"
    r184_extracted_blockers = BASE / "rank9_deathrecovery7_return184_received/BLOCKERS_184_EXTRACTED.json"
    r217_archive = BASE / "rank9_deathrecovery7_return217_received/DD_Rank9_DeathRecovery3_Director_Return217.zip"
    r217_delivery = BASE / "rank9_deathrecovery7_return217_received/DD_Rank9_DeathRecovery3_Director_Return217_DELIVERY.json"
    r217_audit = BASE / "rank9_deathrecovery7_return217_received/RETURN217_INDEPENDENT_AUDIT.json"
    r217_extracted = BASE / "rank9_deathrecovery7_return217_received/extracted"
    r216_archive = BASE / "rank9_deathrecovery7_source_packet_216_refreshed/DD_Rank9_DeathRecovery7_CurrentSource_216.zip"
    r216_delivery = BASE / "rank9_deathrecovery7_source_packet_216_refreshed/DD_Rank9_DeathRecovery7_CurrentSource_216_DELIVERY.json"
    r216_reconciliation = BASE / "rank9_deathrecovery7_source_packet_216_refreshed/CURRENT_CANDIDATE_BINDING_RECONCILIATION.json"
    r217_receipt_candidates = [BASE / "rank9_deathrecovery7_return217_received/RANK9DEATHRECOVERY3_RETURN217_RECEIPT.json", BASE / "rank9_deathrecovery7_return217_received/RETURN217_RECEIPT.json"]
    r217_receipt = next((path for path in r217_receipt_candidates if path.exists()), None)
    assert r184_audit.exists() and read(r184_audit)["status"] == "PASS"
    assert r217_audit.exists() and read(r217_audit)["status"] == "PASS"
    assert read(r217_extracted / "BLOCKERS.json")["blockers"][0]["id"] == "DR217-B01"
    assert read(r217_extracted / "DIRECTOR_DECISION.json")["heldIds"] == ["final-word"]

    return234_archive = BASE / "rank9_psychicfear7_return234_received/DD_Rank9_PsychicFear3_Director_Return234_HELD.zip"
    return234_delivery = BASE / "rank9_psychicfear7_return234_received/DD_Rank9_PsychicFear3_Director_Return234_HELD_DELIVERY.json"
    return234_audit = BASE / "RANK9PSYCHICFEAR7_RETURN234_INDEPENDENT_AUDIT.json"
    return234_receipt = BASE / "RANK9PSYCHICFEAR7_RETURN234_RECEIPT.json"
    assert read(return234_audit)["status"] == "PASS" and read(return234_receipt)["status"] == "PASS"

    candidate = copy.deepcopy(historical_candidate)
    candidate.update({
        "id": "CURRENT-SOURCE-CONFERENCE-CANDIDATE-235",
        "recordedAtUtc": now,
        "status": "PREPARED_CURRENT_AUTHORITY_811_37_EXACT_DEATH_RECOVERY7_FINAL_WORD_GROUP",
        "sourceCommitBase": commit,
        "sourceBranch": branch,
        "currentWorkingTreeSnapshot": True,
        "currentAuthority": AUTHORITY,
        "currentPendingGroup": {"group": GROUP, "spellIds": TARGETS, "count": 1},
        "currentReviewTargets": [{"spellId": "final-word", "currentIndexEntry": target_entry, "completeCurrentCatalogSourceAndAccess": target_spell, "status": "Pending at current 811/37/0 authority; only identity in this packet's review scope."}],
        "selectedHistoricalRecordForTarget": old_record,
        "historicalReviewScope": {"identityCount": 7, "historicalTargetIds": [item["spellId"] for item in historical_candidate["records"]], "currentReviewScope": TARGETS, "qualification": "Historical context includes completed/closed spells; do not reopen them."},
        "historicalWorkflow": {"sourceConference01": "PREPARED_AND_SUBSEQUENTLY_REVIEWED", "return184": "PARTIALLY_ACCEPTED; final-word held DR184-B01", "return217": "doom and eternal-pact accepted/applied; final-word held DR217-B01", "priorDirectorReturn217": info(r217_archive), "currentFreshAssessmentRequired": True},
        "historicalSourceBindings": historical_candidate["sourceBindings"],
        "sourceBindings": source_bindings,
        "sourceBindingRefresh": {"sourceFiles": len(source_bindings), "changedSinceHistoricalCandidate": changed, "sourceContentsFromCurrentWorkingTree": True, "sourceCommitBase": commit},
        "currentAuthorityEvidence": {"currentIndex": info(index_path), "currentCatalog": info(catalog_path), "currentAccessRegistry": info(access_path), "currentWorkQueue": info(work_queue_path), "currentQueue": info(qpath), "currentHandoff": info(hpath), "currentPendingIdentityAudit": info(ppath), "latestReturn234Audit": info(return234_audit), "targetIdsStillPending": TARGETS},
        "lastTargetBlocker": {"id": "DR217-B01", "status": "REASSESS_FROM_FRESH_CURRENT_SOURCE", "sourceEvidenceRequired": "An exact source-qualified independent victim identity and lifecycle establishing that the actual soul is available for this capture, with actual custody/capture-bar/Hunt and summon-no-resource-farm facts. Ordinary class/body eligibility alone is insufficient. If no source supplies these facts, preserve the hold without inventing identity or soul availability."},
        "newRuleAdoptions": 0,
    })

    # Read the review from one identity's actual source operands. All old
    # questions and future requirements remain bundled as history; only the
    # target-specific subset and the latest unresolved witness are actionable.
    focused_questions = [row for row in historical_candidate["questions"] if "final-word" in row.get("spellIds", [])]
    addendum = {
        "id": "DEATH235-ADD01", "spellIds": TARGETS,
        "exactSourceOrConflict": "The prior director selected the spell-local threshold, reserve/payment, counter, concurrency, remainder and expiry rules but held the positive capture branch because no source-qualified victim had verified soul availability and capture eligibility.",
        "request": "Reassess only against current bound sources. Find and cite a real source-established identity/lifecycle satisfying victim eligibility, actual final death (not prevention), available soul, custody/capture-bar/Hunt status and any summon/no-farm restrictions. Then state whether it can lawfully supply the already selected positive reserve/payment trace. Do not manufacture an NPC, infer soul availability from personhood/class/body/name, or treat source silence as a positive witness. If no admissible source exists, retain DR217-B01 and identify the narrowest missing witness. Reconfirm the already selected 49/50 normal-HP boundary, unused reserve remainder, counter nonrefund, concurrent tokens and original expiry without reopening those closed local design choices.",
        "decisionSelected": False,
    }
    current_request = {
        "id": "REQUEST_235",
        "destination": "Calibration review part 6",
        "conversationUrl": CHAT,
        "directorRole": "GPT is the review director; provide a fresh, source-cited decision for exactly final-word.",
        "scope": {"group": GROUP, "targetIds": TARGETS, "authority": AUTHORITY, "noOtherIdentityMayBeReopened": True},
        "instructions": [
            "Use only the exact current source snapshot in sources_current/ plus the complete current index/catalog/access and current queue, handoff, and pending audit. Historical returns are evidence, not current authority.",
            "Read the prior Return184 and Return217 decisions, blocker DR217-B01, original target questions, and all preserved final-word cases. Preserve accepted/applied doom, eternal-pact, and the other completed identities; do not review them again.",
            "Resolve the positive source-established victim/soul/capture witness if the bound sources actually provide one. Cite source path, exact field or passage, identity and lifecycle. If absent, keep final-word held with a precise minimum missing witness.",
            "Keep authority 811/37/0 unless an exact accepted identity is independently audited and later applied. Do not edit canonical files, apply changes, change GitHub, execute supplied programs, or claim runtime/playtest/balance/cosmology/release approval.",
            "Return a sealed decision ZIP and its exact matching DELIVERY.json; state acceptedIds/appliedIds/heldIds and the next group. Do not create a new candidate identity or alter the target list."
        ],
        "focusedAddendum": addendum,
        "originalQuestionsApplicableToFinalWord": focused_questions,
        "historicalQuestionsPreservedUnchanged": historical_candidate["questions"],
        "historicalFutureRequirementsPreservedUnchanged": historical_candidate["futureCaseRequirements"],
        "noApplicationRequestedInPacket": True,
    }
    request_text = f"""REQUEST_235 — CURRENT-SOURCE REVIEW OF FINAL WORD ONLY

Director: GPT in Calibration review part 6.
Authority: 811 reviewed/applied, 37 pending, 0 accepted-unapplied; 535 complete standalone procedures; 173 scoped interfaces.
Exact target: final-word. No other identity is in scope.

Please review REQUEST_235.txt together with CURRENT_SOURCE_CONFERENCE_CANDIDATE_235.json, the current authority/index/catalog/access/queue/handoff/pending snapshots, all 74 refreshed current source files, the audited Return184/Return217 history, and the exact 16 preserved Return217 final-word cases.

Return217 accepted and applied doom and eternal-pact while holding final-word under DR217-B01. The prior director stated the local threshold, reserve/payment, counter, concurrency, remainder and expiry rules are already selected. Reassess the single unresolved positive branch from current source: find and cite an actual source-established identity/lifecycle whose soul is available for capture, including custody/capture-bar/Hunt and summon/no-resource-farm facts, or keep the identity held with the narrowest missing witness. Ordinary class/body eligibility, personhood or a spell name does not establish soul availability. Do not invent an NPC, identity or exception.

Preserve all other accepted and applied spells. Return a sealed decision ZIP and its exact matching DELIVERY.json, explicitly naming acceptedIds, appliedIds, heldIds, blocker IDs, and the next pending group. Do not edit canonical files, apply changes, alter GitHub, execute supplied programs, or claim runtime, playtest, balance, cosmology, domain-completion, or release approval. Any exact acceptance will be independently audited before Codex applies it.

Historical context is evidence only. Current source files in sources_current/ and the current authority snapshots govern this reassessment.
"""

    files: dict[str, bytes] = {}
    # Current authority and all indexed source paths from the historical source conference.
    for name, path in [(INDEX, index_path), (CATALOG, catalog_path), (ACCESS, access_path), (WORK_QUEUE, work_queue_path)]:
        add(files, "current/" + name, path.read_bytes())
    for row in (qpath, hpath, ppath, BASE / "CURRENT_SPELL_REVIEW_SNAPSHOT_235.md"):
        add(files, "current/" + row.relative_to(ROOT).as_posix(), row.read_bytes())
    add(files, "current/CURRENT_AUTHORITY_235.json", enc({"authority": AUTHORITY, "targetIds": TARGETS, "acceptedIds": [], "appliedIds": [], "canonicalChanges": False}))
    add(files, "current/RETURN234_DELIVERY.json", return234_delivery.read_bytes())
    add(files, "current/RETURN234_INDEPENDENT_AUDIT.json", return234_audit.read_bytes())
    add(files, "current/RETURN234_RECEIPT.json", return234_receipt.read_bytes())
    add(files, "current/CURRENT_SOURCE_CONFERENCE_CANDIDATE_235.json", enc(candidate))
    add(files, "current/REQUEST_235.txt", request_text.encode("utf-8"))
    for path, raw in source_files.items():
        add(files, path, raw)

    # Exact historical source conference and latest focused Death/Recovery returns.
    add(files, "history/Source_Conference_01.zip", historical_archive_path.read_bytes())
    add(files, "history/Candidate_Source_Conference_01.json", historical_candidate_path.read_bytes())
    for name, path in [
        ("RETURN184_DIRECTOR_DECISION.json", r184_decision),
        ("RETURN184_INDEPENDENT_AUDIT.json", r184_audit),
        ("RETURN184_DELIVERY.json", r184_delivery),
        ("RETURN184_EXTRACTED_DECISION.json", r184_extracted_decision),
        ("RETURN184_EXTRACTED_BLOCKERS.json", r184_extracted_blockers),
        ("RETURN217_DELIVERY.json", r217_delivery),
        ("RETURN217_INDEPENDENT_AUDIT.json", r217_audit),
        ("CURRENT_SOURCE_216_DELIVERY.json", r216_delivery),
        ("CURRENT_CANDIDATE_BINDING_RECONCILIATION_216.json", r216_reconciliation),
    ]:
        add(files, "history/" + name, path.read_bytes())
    if r217_receipt:
        add(files, "history/RETURN217_RECEIPT.json", r217_receipt.read_bytes())
    add(files, "history/CurrentSource216.zip", r216_archive.read_bytes())
    for path in [BASE / "RANK9_DEATHRECOVERY7_DIRECTOR_DECISION_184.json", BASE / "RANK9_DEATHRECOVERY7_EXACT_ACCEPTANCE_184.json", BASE / "RANK9_DEATHRECOVERY7_RETURN184_INDEPENDENT_AUDIT.json", BASE / "RANK9_DEATHRECOVERY7_GPT_RETURN_184.json"]:
        add(files, "history/" + path.name, path.read_bytes())

    # Select exact Return217 members needed to review final-word, and the 16
    # preserved Return184 final-word traces byte-for-byte from that archive.
    with zipfile.ZipFile(r217_archive) as return217_zip:
        assert return217_zip.testzip() is None
        exact_members = [
            "DIRECTOR_DECISION.json", "BLOCKERS.json", "ORIGINAL_QUESTIONS_AND_OBLIGATIONS.json",
            "CASE_INDEX.json", "PROCEDURES.json", "PROCEDURE_SOURCE_MAP.json",
            "QUESTION_DISPOSITIONS.json", "SOURCE_BINDINGS.json", "NATIVE_SOURCE_ROWS.json",
            "ACTOR_PROFILES.json", "COUNTS.json", "COVERAGE.json", "CLOCK_LEDGER.json",
            "DATA_INTEGRITY_CHECK.json", "HOLD_REGISTER.json", "NEXT_QUEUE_HANDOFF.json",
            "current/CURRENT_SPELL_QUEUE_216.json", "current/CURRENT_HANDOFF_216.json",
            "current/CURRENT42_PENDING_IDENTITY_AUDIT_216.json", "current/RETURN216_BLOCKERS.json",
            "current/RETURN216_DIRECTOR_DECISION.json", "current/RETURN216_INDEPENDENT_AUDIT.json",
        ]
        for member in exact_members:
            if member in return217_zip.namelist():
                add(files, "history/Return217/" + member, return217_zip.read(member))
        final_word_cases = [n for n in return217_zip.namelist() if n.startswith("preserved_cases/DR184-FINAL-WORD-") and n.endswith(".json")]
        assert len(final_word_cases) == 16
        for member in final_word_cases:
            raw = return217_zip.read(member)
            local = r217_extracted / member
            assert local.exists() and local.read_bytes() == raw
            add(files, "history/Return217/" + member, raw)

    # The current source snapshot is concise; exact file hashes and CRCs bind
    # every included member, and the embedded manifest is self-excluding.
    out_candidate = OUT / "CURRENT_SOURCE_CONFERENCE_CANDIDATE_235.json"
    out_candidate.parent.mkdir(parents=True, exist_ok=True)
    out_candidate.write_bytes(enc(candidate))
    request_path = OUT / "REQUEST_235.txt"
    request_path.write_text(request_text, encoding="utf-8")
    current_source = OUT / "DD_Rank9_DeathRecovery7_CurrentSource_235.zip"
    delivery_path = OUT / "DD_Rank9_DeathRecovery7_CurrentSource_235_DELIVERY.json"
    manifest = {"id": "RANK9-DEATH-RECOVERY7-CURRENT-SOURCE-235-MEMBER-MANIFEST", "members": []}
    # Exact portable member bindings.
    manifest["members"] = [{"path": name, "bytes": len(raw), "sha256": sha(raw), "crc32": crc(raw)} for name, raw in sorted(files.items())]
    manifest_raw = enc(manifest)
    with zipfile.ZipFile(current_source, "w", zipfile.ZIP_DEFLATED, compresslevel=6) as archive:
        for name, raw in sorted(files.items()):
            archive.writestr(name, raw)
        archive.writestr("MEMBER_MANIFEST.json", manifest_raw)
    with zipfile.ZipFile(current_source) as archive:
        assert archive.testzip() is None and len(archive.namelist()) == len(set(archive.namelist()))
        for item in manifest["members"]:
            raw = archive.read(item["path"])
            assert (len(raw), sha(raw), crc(raw)) == (item["bytes"], item["sha256"], item["crc32"])
        assert archive.read("MEMBER_MANIFEST.json") == manifest_raw

    packet_info = info(current_source)
    manifest_info = {"path": "MEMBER_MANIFEST.json", "bytes": len(manifest_raw), "sha256": sha(manifest_raw), "crc32": crc(manifest_raw)}
    payload = {"id": "RANK9-DEATH-RECOVERY7-CURRENT-SOURCE-235-DELIVERY", "createdAtUtc": now, "group": GROUP, "targetIds": TARGETS, "authority": AUTHORITY,
               "archive": {"fileName": current_source.name, **{k: packet_info[k] for k in ("bytes", "sha256", "crc32")}},
               "sourceBindings": [{"path": row["path"], "bytes": row["bytes"], "sha256": row["sha256"], "crc32": row["crc32"]} for row in source_bindings],
               "memberCount": len(files) + 1, "payloadCount": len(files), "memberManifest": manifest_info,
               "members": [{"path": name, "bytes": len(raw), "sha256": sha(raw), "crc32": crc(raw)} for name, raw in sorted(files.items())] + [{"path": "MEMBER_MANIFEST.json", **{k: manifest_info[k] for k in ("bytes", "sha256", "crc32")}}],
               "exactAllowlist": sorted([*files.keys(), "MEMBER_MANIFEST.json"]), "canonicalChanges": False, "githubChanges": False, "sourceProgramsExecuted": False, "runtimeExecuted": False,
               "originalQuestionsPreserved": len(historical_candidate["questions"]), "focusedQuestions": len(focused_questions), "focusedAddenda": 1, "priorFinalWordCases": len(final_word_cases),
               "nextPendingGroup": None, "notes": "Fresh current-authority source packet. GPT is director; only final-word is in scope. Historical accepted identities remain closed."}
    delivery_raw = enc(payload)
    delivery_path.write_bytes(enc(payload))

    prep = {"id": "RANK9DEATHRECOVERY7-SOURCE-PREPARATION-235", "status": "PREPARED_NOT_SENT", "recordedAtUtc": now, "group": GROUP, "targetIds": TARGETS, "authority": AUTHORITY,
            "branch": branch, "head": commit, "sourcePathsRefreshed": len(source_bindings), "sourceBindingsChangedSinceHistorical": changed,
            "includedMembers": len(files) + 1, "priorFinalWordCases": len(final_word_cases), "historicalQuestionsPreserved": len(historical_candidate["questions"]),
            "focusedQuestions": len(focused_questions), "focusedAddenda": 1, "archive": info(current_source), "deliveryManifest": info(delivery_path),
            "candidate": info(out_candidate), "request": info(request_path), "queueSnapshot": info(qpath), "handoffSnapshot": info(hpath), "pendingAuditSnapshot": info(ppath), "canonicalChanges": False, "githubChanges": False}
    (BASE / "RANK9DEATHRECOVERY7_SOURCE_PREPARATION_235.json").write_bytes(enc(prep))
    (BASE / "RANK9DEATHRECOVERY7_PACKET_235.json").write_bytes(enc({"id": "RANK9DEATHRECOVERY7-PACKET-235", "status": "PREPARED_NOT_SENT", "archive": prep["archive"], "deliveryManifest": prep["deliveryManifest"], "sourcePreparation": info(BASE / "RANK9DEATHRECOVERY7_SOURCE_PREPARATION_235.json"), "targetIds": TARGETS, "authority": AUTHORITY, "canonicalChanges": False, "githubChanges": False}))
    print(json.dumps({"status": prep["status"], "targetIds": TARGETS, "authority": AUTHORITY, "sourcePathsRefreshed": len(source_bindings), "priorFinalWordCases": len(final_word_cases), "includedMembers": len(files)+1, "archive": prep["archive"], "deliveryManifest": prep["deliveryManifest"], "changedSources": len(changed)}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
