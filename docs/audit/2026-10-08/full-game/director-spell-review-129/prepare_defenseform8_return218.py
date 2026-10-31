from __future__ import annotations

import copy
import hashlib
import json
import pathlib
import subprocess
import zipfile
import zlib
from datetime import datetime, timezone


ROOT = pathlib.Path(r"C:\Github\DecenniumDescent-review-push-134")
BASE = ROOT / "docs/audit/2026-10-08/full-game/director-spell-review-129"
OLD_PACKET = BASE / "rank9_defenseform8_return185_prepared/DD_Rank9_DefenseForm8_CurrentSource_185.zip"
OLD_CANDIDATE_PATH = "DescentReviewChanges/ReviewBible/data/director/spell_review/rank9_defense_form_8_source_conference_01.json"
OLD_SOURCE_ARCHIVE_PATH = "docs/audit/2026-10-08/full-game/DD_Rank9_Defense_Form_8_Source_Conference_01.zip"
GROUP = "rank9-defense-form8"
IDS = ["absolute-immunity", "elemental-shell", "body-to-void", "timeless-form", "invulnerable-sphere"]
ALREADY_ACCEPTED = ["astral-shell", "divine-shield", "eternal-protection"]
AUTHORITY = {"reviewedApplied": 808, "pending": 40, "acceptedUnapplied": 0, "completeStandaloneProcedures": 532, "scopedInterfaces": 173}
CHAT = "https://chatgpt.com/g/g-p-67f17555a8dc8191a2b5b81e6d8adc12-dungeon-crawler/c/6adc506d-8770-83ea-b64c-0345d9b9b682"
OUT = BASE / "rank9_defenseform8_source_packet_218_refreshed"
PACKET = OUT / "DD_Rank9_DefenseForm8_CurrentSource_218.zip"
DELIVERY = OUT / "DD_Rank9_DefenseForm8_CurrentSource_218_DELIVERY.json"
PREP = BASE / "RANK9_DEFENSEFORM8_SOURCE_PREPARATION_218.json"
PACKET_RECORD = BASE / "RANK9_DEFENSEFORM8_PACKET_218.json"
QUEUE_BEFORE = BASE / "CURRENT_SPELL_QUEUE_217.json"
HANDOFF_BEFORE = BASE / "CURRENT_HANDOFF_217.json"
PENDING = BASE / "CURRENT40_PENDING_IDENTITY_AUDIT_217.json"
RETURN186_DIR = BASE / "rank9_defenseform8_return186_received"
RETURN217_DIR = BASE / "rank9_deathrecovery7_return217_received"
QUEUE_AFTER = BASE / "CURRENT_SPELL_QUEUE_218.json"
HANDOFF_AFTER = BASE / "CURRENT_HANDOFF_218.json"
SNAPSHOT = BASE / "CURRENT_SPELL_REVIEW_SNAPSHOT_218.md"
REQUEST_EXTERNAL = BASE / "RANK9_DEFENSEFORM8_RETURN217_REQUEST.txt"
RECONCILIATION = BASE / "CURRENT_CANDIDATE_BINDING_RECONCILIATION_218.json"


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def crc(raw: bytes) -> str:
    return f"{zlib.crc32(raw) & 0xFFFFFFFF:08x}"


def json_bytes(value) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8")


def read_json(path: pathlib.Path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def bind(path: str, raw: bytes) -> dict:
    return {"path": path, "bytes": len(raw), "sha256": sha(raw), "crc32": crc(raw)}


def file_bind(path: pathlib.Path) -> dict:
    return bind(path.relative_to(ROOT).as_posix(), path.read_bytes())


def git_head() -> str:
    return subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()


def git_blob(rel: str) -> bytes:
    return subprocess.check_output(["git", "cat-file", "blob", f"HEAD:{rel}"], cwd=ROOT)


def git_blob_id(rel: str) -> str:
    return subprocess.check_output(["git", "rev-parse", f"HEAD:{rel}"], cwd=ROOT, text=True).strip()


def write_json(path: pathlib.Path, value) -> None:
    path.write_bytes(json_bytes(value))


def main() -> None:
    ts = datetime.now(timezone.utc).isoformat()
    require_not_exists = [OUT, PREP, PACKET_RECORD, QUEUE_AFTER, HANDOFF_AFTER, SNAPSHOT]
    already = [str(path) for path in require_not_exists if path.exists()]
    if already:
        raise RuntimeError(f"Fresh packet outputs already exist; inspect before retry: {already}")

    queue = read_json(QUEUE_BEFORE)
    handoff = read_json(HANDOFF_BEFORE)
    pending = read_json(PENDING)
    index_path = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json"
    catalog_path = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json"
    index_raw = index_path.read_bytes()
    catalog_raw = catalog_path.read_bytes()
    index = json.loads(index_raw.decode("utf-8-sig"))
    catalog = json.loads(catalog_raw.decode("utf-8-sig"))
    idx_bind = file_bind(index_path)
    cat_bind = file_bind(catalog_path)
    current_group = next(g for g in queue["currentPendingGroups"] if g["group"] == GROUP)
    if queue["currentAuthority"] != AUTHORITY or handoff["currentAuthority"] != AUTHORITY:
        raise RuntimeError("Queue/handoff do not match current 808/40/0 authority")
    if pending.get("exactPendingCount") != 40 or pending.get("authority") != AUTHORITY:
        raise RuntimeError("Current pending audit does not match 808/40/0")
    if queue["currentIndexBinding"]["sha256"] != idx_bind["sha256"] or queue["currentCatalogBinding"]["sha256"] != cat_bind["sha256"]:
        raise RuntimeError("Current index/catalog bytes differ from queue217")
    if index.get("authoredCounts") != {"reviewed": 808, "pending": 40}:
        raise RuntimeError("Current index counts are not 808/40")
    if current_group["pendingIds"] != IDS or current_group["pendingCount"] != len(IDS):
        raise RuntimeError(f"Defense/Form8 current pending IDs mismatch: {current_group.get('pendingIds')}")
    if not set(IDS).issubset(set(pending["pendingIds"])):
        raise RuntimeError("Target IDs are absent from exact pending identity audit")
    entry_map = {row["id"]: row for row in index["entries"]}
    catalog_map = {row["id"]: row for row in catalog["spells"]}
    if not all(entry_map[s]["authoredStatus"] == "pending-authored-procedure" and catalog_map[s]["operational"] is None for s in IDS):
        raise RuntimeError("A Defense/Form8 target is already non-pending or operational")
    if not all(entry_map[s]["authoredStatus"] == "reviewed-authored-operational-playtest" for s in ALREADY_ACCEPTED):
        raise RuntimeError("Return186 accepted identities are not already applied")

    return186_audit = read_json(BASE / "RANK9_DEFENSEFORM8_RETURN186_INDEPENDENT_AUDIT.json")
    return186_delivery = read_json(RETURN186_DIR / "DD_Rank9_DefenseForm8_Director_Return186_DELIVERY.json")
    return186_decision = read_json(BASE / "RANK9_DEFENSEFORM8_DIRECTOR_DECISION_186.json")
    return217_decision = read_json(RETURN217_DIR / "extracted/DIRECTOR_DECISION.json")
    if return186_audit.get("status") != "PASS" or return186_audit.get("checksFailed") != 0:
        raise RuntimeError("Return186 baseline audit is not a clean PASS")
    if return186_delivery.get("acceptedIds") != ALREADY_ACCEPTED or return186_delivery.get("applied") is not False:
        raise RuntimeError("Return186 accepted identities/before-application state differs")
    if return186_decision.get("acceptedIds") != ALREADY_ACCEPTED:
        raise RuntimeError("Return186 director decision differs")
    if return217_decision.get("acceptedIds") != ["doom", "eternal-pact"] or return217_decision.get("heldIds") != ["final-word"]:
        raise RuntimeError("Return217 accepted/held context differs")

    # Reuse the historical source candidate and full source archive, but refresh
    # every one of its 87 bound source snapshots from the current checkout.
    with zipfile.ZipFile(OLD_PACKET, "r") as oldzip:
        if oldzip.testzip() is not None:
            raise RuntimeError("Historical prepared packet ZIP has a corrupt member")
        historical_candidate_raw = oldzip.read("HISTORICAL_SOURCE_CONFERENCE_CANDIDATE_01.json")
        historical_archive_raw = oldzip.read("HISTORICAL_SOURCE_CONFERENCE_ARCHIVE_01.zip")
        refreshed_old_raw = oldzip.read("CURRENT_SOURCE_CONFERENCE_CANDIDATE_185.json")
        old_context = json.loads(oldzip.read("CURRENT_CONTEXT_185.json"))
        old_refreshed = json.loads(refreshed_old_raw)
        original_sources = {row["path"]: oldzip.read("sources_current/" + row["path"]) for row in old_refreshed["sourceBindings"]}
    historical_candidate = json.loads(historical_candidate_raw.decode("utf-8-sig"))
    historical_source_archive = (ROOT / OLD_SOURCE_ARCHIVE_PATH).read_bytes()
    historical_source_candidate = (ROOT / OLD_CANDIDATE_PATH).read_bytes()
    current_source_candidate = json.loads(historical_source_candidate.decode("utf-8-sig"))
    if historical_archive_raw != historical_source_archive:
        raise RuntimeError("Historical source archive does not match its local byte-exact source binding")
    if historical_candidate != current_source_candidate:
        raise RuntimeError("Current source candidate differs structurally from the queue-bound historical candidate")
    candidate_reconciliation = {
        "id": "RANK9-DEFENSEFORM8-CANDIDATE-BINDING-RECONCILIATION-218",
        "recordedAtUtc": ts,
        "historicalQueueBinding": bind(OLD_CANDIDATE_PATH, historical_candidate_raw),
        "currentWorktreeBinding": bind(OLD_CANDIDATE_PATH, historical_source_candidate),
        "jsonStructuralEquality": True,
        "fieldDifferences": 0,
        "byteEquality": historical_candidate_raw == historical_source_candidate,
        "differenceType": "none" if historical_candidate_raw == historical_source_candidate else "JSON serialization only (whitespace/property ordering)",
        "queueCandidateBinding": current_group["candidate"],
        "currentAuthority": AUTHORITY,
    }
    write_json(RECONCILIATION, candidate_reconciliation)
    if [x.get("spellId") for x in historical_candidate.get("records", [])] != ["absolute-immunity", "astral-shell", "divine-shield", "eternal-protection", "elemental-shell", "body-to-void", "timeless-form", "invulnerable-sphere"]:
        raise RuntimeError("Historical Defense/Form8 candidate does not contain the exact eight original records")
    if len(old_refreshed.get("sourceBindings", [])) != 87:
        raise RuntimeError("Historical Defense/Form8 source map does not contain 87 bindings")

    refreshed_bindings = []
    source_files = {}
    changed_from_previous = []
    for old in old_refreshed["sourceBindings"]:
        rel = old["path"]
        path = ROOT / pathlib.PurePosixPath(rel)
        raw = path.read_bytes()
        row = {"path": rel, "bytes": len(raw), "sha256": sha(raw), "crc32": crc(raw)}
        try:
            committed = git_blob(rel)
            row["gitBlobSHA1"] = git_blob_id(rel) if committed == raw else None
        except Exception:
            row["gitBlobSHA1"] = None
        if rel in original_sources and raw != original_sources[rel]:
            changed_from_previous.append({"path": rel, "previousBytes": len(original_sources[rel]), "previousSHA256": sha(original_sources[rel]), "currentBytes": len(raw), "currentSHA256": sha(raw)})
        refreshed_bindings.append(row)
        source_files["sources_current/" + rel] = raw
    if bind(OLD_CANDIDATE_PATH, historical_candidate_raw)["sha256"] != current_group["candidate"]["sha256"] or bind(OLD_CANDIDATE_PATH, historical_candidate_raw)["bytes"] != current_group["candidate"]["bytes"]:
        raise RuntimeError("Queue217 candidate binding does not match the exact historical packet bytes")
    if bind(OLD_SOURCE_ARCHIVE_PATH, historical_source_archive)["sha256"] != current_group["archive"]["sha256"] or bind(OLD_SOURCE_ARCHIVE_PATH, historical_source_archive)["bytes"] != current_group["archive"]["bytes"]:
        raise RuntimeError("Current Defense/Form8 source archive does not match queue217")

    derived = copy.deepcopy(old_refreshed)
    derived.update({
        "id": "RANK9-DEFENSE-FORM8-CURRENT-SOURCE-CONTEXT-218",
        "recordedAtUtc": ts,
        "status": "FRESH_CURRENT_SOURCE_BINDINGS_FOR_808_REVIEWED_40_PENDING_AUTHORITY",
        "historicalCandidateBinding": bind(OLD_CANDIDATE_PATH, historical_candidate_raw),
        "currentCandidateBinding": bind(OLD_CANDIDATE_PATH, historical_source_candidate),
        "candidateBindingReconciliation": file_bind(RECONCILIATION),
        "historicalSourceArchiveBinding": bind(OLD_SOURCE_ARCHIVE_PATH, historical_archive_raw),
        "historicalSourceBindings": copy.deepcopy(historical_candidate.get("sourceBindings", [])),
        "sourceBindings": refreshed_bindings,
        "sourceCommit": git_head(),
        "currentAuthority": AUTHORITY,
        "currentPendingGroup": {"group": GROUP, "spellIds": IDS, "count": len(IDS), "alreadyAcceptedIds": ALREADY_ACCEPTED},
        "sourceBindingRefresh": {"sourceFiles": len(refreshed_bindings), "changedFromPriorPreparedPacket": changed_from_previous, "currentIndexBinding": idx_bind, "currentCatalogBinding": cat_bind},
        "priorReturn186": {"acceptedAppliedIds": ALREADY_ACCEPTED, "heldIds": IDS, "independentAudit": file_bind(BASE / "RANK9_DEFENSEFORM8_RETURN186_INDEPENDENT_AUDIT.json")},
        "currentReturn217": {"acceptedAppliedIds": ["doom", "eternal-pact"], "heldIds": ["final-word"], "blockerIds": ["DR217-B01"], "independentApplicationAudit": file_bind(BASE / "RANK9DEATHRECOVERY3_POST_APPLICATION_INDEPENDENT_AUDIT_217.json")},
        "priorHeldIdentitiesNotReopened": ["psychic-scream", "mass-phantom-killer", "weird", "final-word"],
        "newRuleAdoptions": 0,
        "canonicalFilesEdited": False,
    })

    current_files = {
        "current/DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json": index_raw,
        "current/DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json": catalog_raw,
        "current/docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT_SPELL_QUEUE_217.json": QUEUE_BEFORE.read_bytes(),
        "current/docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT_HANDOFF_217.json": HANDOFF_BEFORE.read_bytes(),
        "current/docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT40_PENDING_IDENTITY_AUDIT_217.json": PENDING.read_bytes(),
        "current/docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT_CANDIDATE_BINDING_RECONCILIATION_218.json": RECONCILIATION.read_bytes(),
        "current/docs/audit/2026-10-08/full-game/director-spell-review-129/RANK9DEATHRECOVERY3_EXACT_ACCEPTANCE_217.json": (BASE / "RANK9DEATHRECOVERY3_EXACT_ACCEPTANCE_217.json").read_bytes(),
        "current/docs/audit/2026-10-08/full-game/director-spell-review-129/RANK9DEATHRECOVERY3_APPLICATION_217.json": (BASE / "RANK9DEATHRECOVERY3_APPLICATION_217.json").read_bytes(),
        "current/docs/audit/2026-10-08/full-game/director-spell-review-129/RANK9DEATHRECOVERY3_APPLICATION_VALIDATION_217.json": (BASE / "RANK9DEATHRECOVERY3_APPLICATION_VALIDATION_217.json").read_bytes(),
        "current/docs/audit/2026-10-08/full-game/director-spell-review-129/RANK9DEATHRECOVERY3_POST_APPLICATION_INDEPENDENT_AUDIT_217.json": (BASE / "RANK9DEATHRECOVERY3_POST_APPLICATION_INDEPENDENT_AUDIT_217.json").read_bytes(),
        "current/docs/audit/2026-10-08/full-game/director-spell-review-129/RANK9DEATHRECOVERY3_REPRESENTATION_COUNT_RECONCILIATION_217.json": (BASE / "RANK9DEATHRECOVERY3_REPRESENTATION_COUNT_RECONCILIATION_217.json").read_bytes(),
        "current/docs/audit/2026-10-08/full-game/director-spell-review-129/RANK9_DEFENSEFORM8_NEXT_CONFERENCE_NOTES_129.json": (BASE / "RANK9DEFENSEFORM8_NEXT_CONFERENCE_NOTES_129.json").read_bytes(),
        "current/docs/audit/2026-10-08/full-game/director-spell-review-129/RANK9_DEFENSEFORM8_RETURN186_RECEIPT.json": (BASE / "RANK9_DEFENSEFORM8_RETURN186_RECEIPT.json").read_bytes(),
        "current/docs/audit/2026-10-08/full-game/director-spell-review-129/RANK9_DEFENSEFORM8_RETURN186_INDEPENDENT_AUDIT.json": (BASE / "RANK9_DEFENSEFORM8_RETURN186_INDEPENDENT_AUDIT.json").read_bytes(),
        "current/docs/audit/2026-10-08/full-game/director-spell-review-129/RANK9_DEFENSEFORM8_DIRECTOR_DECISION_186.json": (BASE / "RANK9_DEFENSEFORM8_DIRECTOR_DECISION_186.json").read_bytes(),
        "current/docs/audit/2026-10-08/full-game/director-spell-review-129/RANK9_DEFENSEFORM8_EXACT_ACCEPTANCE_186.json": (BASE / "RANK9_DEFENSEFORM8_EXACT_ACCEPTANCE_186.json").read_bytes(),
        "current/docs/audit/2026-10-08/full-game/director-spell-review-129/RANK9_DEFENSEFORM8_APPLICATION_186.json": (BASE / "RANK9_DEFENSEFORM8_APPLICATION_186.json").read_bytes(),
        "current/docs/audit/2026-10-08/full-game/director-spell-review-129/RANK9_DEFENSEFORM8_APPLICATION_VALIDATION_186.json": (BASE / "RANK9_DEFENSEFORM8_APPLICATION_VALIDATION_186.json").read_bytes(),
        "current/docs/audit/2026-10-08/full-game/director-spell-review-129/rank9_defenseform8_return186_received/DD_Rank9_DefenseForm8_Director_Return186.zip": (RETURN186_DIR / "DD_Rank9_DefenseForm8_Director_Return186.zip").read_bytes(),
        "current/docs/audit/2026-10-08/full-game/director-spell-review-129/rank9_defenseform8_return186_received/DD_Rank9_DefenseForm8_Director_Return186_DELIVERY.json": (RETURN186_DIR / "DD_Rank9_DefenseForm8_Director_Return186_DELIVERY.json").read_bytes(),
        "current/docs/audit/2026-10-08/full-game/director-spell-review-129/rank9_deathrecovery7_return217_received/DD_Rank9_DeathRecovery3_Director_Return217_DELIVERY.json": (RETURN217_DIR / "DD_Rank9_DeathRecovery3_Director_Return217_DELIVERY.json").read_bytes(),
    }
    current_context = {
        "id": "RANK9-DEFENSE-FORM8-CURRENT-DIRECTOR-CONTEXT-218",
        "recordedAtUtc": ts,
        "sourceCommit": git_head(),
        "sourceAuthority": AUTHORITY,
        "currentPendingGroup": {"group": GROUP, "pendingIds": IDS, "pendingCount": len(IDS)},
        "recentBatch": {"return": 217, "acceptedAppliedIds": ["doom", "eternal-pact"], "heldIds": ["final-word"], "blockerIds": ["DR217-B01"]},
        "priorDefenseFormReturn": {"return": 186, "acceptedAppliedIds": ALREADY_ACCEPTED, "heldIds": IDS, "blockerIds": ["DF186-H-TRACKS", "DF186-H-NULL", "DF186-H-ENV", "DF186-H-COMPANION", "DF186-H-OCCUPIED", "DF186-H-AGING", "DF186-H-TIMESTOP", "DF186-H-PLANAR", "DF186-H-CONTROL"]},
        "currentIndexBinding": idx_bind,
        "currentCatalogBinding": cat_bind,
        "candidateBindingReconciliation": file_bind(RECONCILIATION),
        "currentQueue217": file_bind(QUEUE_BEFORE),
        "currentHandoff217": file_bind(HANDOFF_BEFORE),
        "currentPendingAudit217": file_bind(PENDING),
        "currentReturn217ApplicationAudit": file_bind(BASE / "RANK9DEATHRECOVERY3_POST_APPLICATION_INDEPENDENT_AUDIT_217.json"),
        "historicalNotesQualification": "RANK9DEFENSEFORM8_NEXT_CONFERENCE_NOTES_129.json is guidance to recheck against current source, not authority.",
        "qualification": "Static authored-procedure review only. GPT director must not edit index, catalog, queue, handoff or GitHub. Preserve prior exact acceptances and unrelated holds; do not reopen the 335 feats or completed cohorts.",
    }

    request = (
        "GPT director — review the exact five current pending Rank9 Defense/Form8 identities in the attached authority-808 packet.\n\n"
        f"Current authority is 808 reviewed/applied / 40 pending / 0 accepted-unapplied; 532 complete standalone procedures and 173 scoped interfaces. Review only: {', '.join(IDS)}.\n\n"
        "Return186 already accepted and Codex applied astral-shell, divine-shield and eternal-protection. Do not revisit those identities. Reassess Return186’s DF186 blocker set against the refreshed source and current evidence; make spell-local design choices within your director authority and hold only for genuinely missing source facts or permissions. Preserve all prior unrelated holds, including Final Word’s DR217-B01 and the Psychic/Fear holds. Do not reopen feats or completed cohorts.\n\n"
        "The packet binds the exact current index/catalog, queue/handoff, 40-identity pending audit, the 808/40 application and independent audit for Return217, the complete Return186 archive/delivery/audit/decision, the historical source archive and candidate, and all 87 refreshed source snapshots. The queue-bound candidate bytes and current worktree candidate serialize differently, but a structural JSON comparison found zero field differences; the packet includes both exact bindings and the reconciliation record. The old Return186 decisions remain evidence to reassess, not automatic blockers.\n\n"
        "For the exact five IDs, return per-identity accepted/held decisions, exact blocker IDs, any conditional qualification IDs, source-backed procedures and cases, and an independently reproducible audit. Keep accepted=true/applied=false in your decision; do not apply or change canonical files. Attach the matching ZIP archive and external delivery manifest with exact member inventory, hashes, CRCs, and current authority. Preserve all runtime, implementation, human-play, balance, cosmology, domain-closure and release qualifications. Codex will independently audit and apply exact acceptances, then refresh the next batch.\n"
    )
    request_raw = request.encode("utf-8")
    files = {
        "CURRENT_CONTEXT_218.json": json_bytes(current_context),
        "CURRENT_SOURCE_CONFERENCE_CANDIDATE_218.json": json_bytes(derived),
        "CURRENT_SOURCE_CONFERENCE_CANDIDATE_FILE_218.json": historical_source_candidate,
        "HISTORICAL_SOURCE_CONFERENCE_CANDIDATE_01.json": historical_candidate_raw,
        "CANDIDATE_BINDING_RECONCILIATION_218.json": RECONCILIATION.read_bytes(),
        "HISTORICAL_SOURCE_CONFERENCE_ARCHIVE_01.zip": historical_archive_raw,
        "HISTORICAL_RETURN186.zip": (RETURN186_DIR / "DD_Rank9_DefenseForm8_Director_Return186.zip").read_bytes(),
        "HISTORICAL_RETURN186_DELIVERY.json": (RETURN186_DIR / "DD_Rank9_DefenseForm8_Director_Return186_DELIVERY.json").read_bytes(),
        "REQUEST_218.txt": request_raw,
        **current_files,
        **source_files,
    }
    OUT.mkdir(parents=True, exist_ok=False)
    member_rows = [{"path": path, "bytes": len(raw), "sha256": sha(raw), "crc32": crc(raw)} for path, raw in sorted(files.items())]
    internal_manifest = {
        "id": "RANK9-DEFENSE-FORM8-CURRENT-SOURCE-PACKET-MANIFEST-218",
        "sourceCommit": git_head(),
        "sourceAuthority": AUTHORITY,
        "targetGroup": GROUP,
        "targetPendingIds": IDS,
        "memberCountExcludingSelf": len(member_rows),
        "members": member_rows,
    }
    with zipfile.ZipFile(PACKET, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=6) as zf:
        for path, raw in sorted(files.items()):
            zf.writestr(path, raw, compress_type=zipfile.ZIP_DEFLATED, compresslevel=6)
        zf.writestr("MANIFEST.json", json_bytes(internal_manifest), compress_type=zipfile.ZIP_DEFLATED, compresslevel=6)
    with zipfile.ZipFile(PACKET, "r") as zf:
        names = zf.namelist()
        if zf.testzip() is not None or len(names) != len(set(names)) or set(names) != set(files) | {"MANIFEST.json"}:
            raise RuntimeError("New packet ZIP has CRC, duplicate-name, or exact-allowlist failure")
        for row in member_rows:
            raw = zf.read(row["path"])
            if len(raw) != row["bytes"] or sha(raw) != row["sha256"] or crc(raw) != row["crc32"]:
                raise RuntimeError(f"Member binding failed: {row['path']}")
        if json.loads(zf.read("MANIFEST.json")) != internal_manifest:
            raise RuntimeError("Internal packet manifest differs from exact member allowlist")
    archive_bind = file_bind(PACKET)
    external_delivery = {
        "id": "RANK9-DEFENSE-FORM8-CURRENT-SOURCE-DELIVERY-218",
        "archive": {"fileName": PACKET.name, **{k: archive_bind[k] for k in ("bytes", "sha256", "crc32")}},
        "memberCount": len(member_rows) + 1,
        "payloadCountExcludingInternalManifest": len(member_rows),
        "sourceAuthority": AUTHORITY,
        "group": GROUP,
        "pendingIds": IDS,
        "currentIndexBinding": idx_bind,
        "currentCatalogBinding": cat_bind,
        "sourceCandidateBinding": bind(OLD_CANDIDATE_PATH, historical_source_candidate),
        "historicalSourceCandidateBinding": bind(OLD_CANDIDATE_PATH, historical_candidate_raw),
        "candidateBindingReconciliation": file_bind(RECONCILIATION),
        "sourceArchiveBinding": bind(OLD_SOURCE_ARCHIVE_PATH, historical_archive_raw),
        "members": member_rows + [{"path": "MANIFEST.json", "bytes": len(json_bytes(internal_manifest)), "sha256": sha(json_bytes(internal_manifest)), "crc32": crc(json_bytes(internal_manifest))}],
        "checksPassed": 8,
        "checksFailed": 0,
    }
    write_json(DELIVERY, external_delivery)

    # Read the saved ZIP back and compute all source refresh checks before the
    # current queue/handoff advertise the prepared request.
    checks = [
        {"check": "Current 808/40/0 authority matches queue, handoff, pending audit and authored index", "passed": queue["currentAuthority"] == handoff["currentAuthority"] == AUTHORITY and pending["exactPendingCount"] == 40 and pending["authority"] == AUTHORITY and index["authoredCounts"] == {"reviewed": 808, "pending": 40}},
        {"check": "Exact five current pending IDs are in the native catalog and remain unreviewed", "passed": current_group["pendingIds"] == IDS and all(entry_map[s]["authoredStatus"] == "pending-authored-procedure" and catalog_map[s]["operational"] is None for s in IDS)},
        {"check": "Return186 accepted three are already applied and excluded from the review request", "passed": all(entry_map[s]["authoredStatus"] == "reviewed-authored-operational-playtest" for s in ALREADY_ACCEPTED) and set(IDS).isdisjoint(ALREADY_ACCEPTED)},
        {"check": "All 87 source snapshots refresh from the current worktree; queue-bound and current candidate JSON are structurally equal; current archive hash matches queue217", "passed": len(refreshed_bindings) == 87 and candidate_reconciliation["jsonStructuralEquality"] and candidate_reconciliation["fieldDifferences"] == 0 and candidate_reconciliation["currentWorktreeBinding"]["sha256"] == sha(historical_source_candidate) and bind(OLD_CANDIDATE_PATH, historical_candidate_raw)["sha256"] == current_group["candidate"]["sha256"] and bind(OLD_SOURCE_ARCHIVE_PATH, historical_source_archive)["sha256"] == current_group["archive"]["sha256"]},
        {"check": "Current Return217 application audit and held identities are included", "passed": current_context["currentReturn217ApplicationAudit"] == file_bind(BASE / "RANK9DEATHRECOVERY3_POST_APPLICATION_INDEPENDENT_AUDIT_217.json") and current_context["recentBatch"]["heldIds"] == ["final-word"]},
        {"check": "Historical Return186 archive, delivery and independent audit are bound", "passed": return186_audit["status"] == "PASS" and external_delivery["memberCount"] == len(member_rows) + 1},
        {"check": "Packet internal/external manifests bind the exact 87 source files and full unique member set", "passed": len(member_rows) == len(files) and len(set(files)) == len(files) and len(internal_manifest["members"]) == len(files)},
        {"check": "Saved packet outer size/SHA/CRC, CRC scan, exact allowlist and all member hashes pass", "passed": archive_bind["bytes"] == PACKET.stat().st_size and len(member_rows) == len(files) and len(names) == len(files) + 1},
    ]
    if not all(x["passed"] for x in checks):
        raise RuntimeError("Current Defense/Form8 packet preparation checks failed")
    prep = {
        "id": "RANK9-DEFENSEFORM8-SOURCE-PREPARATION-218",
        "recordedAtUtc": ts,
        "status": "CURRENT_SOURCE_PACKET_PREPARED_UNSENT_808_40_0",
        "sourceCommit": git_head(),
        "sourceAuthority": AUTHORITY,
        "group": GROUP,
        "pendingIds": IDS,
        "alreadyAcceptedIds": ALREADY_ACCEPTED,
        "historicalCandidate": bind(OLD_CANDIDATE_PATH, historical_candidate_raw),
        "currentCandidate": bind(OLD_CANDIDATE_PATH, historical_source_candidate),
        "candidateBindingReconciliation": file_bind(RECONCILIATION),
        "historicalSourceArchive": bind(OLD_SOURCE_ARCHIVE_PATH, historical_archive_raw),
        "currentDerivedCandidate": bind("CURRENT_SOURCE_CONFERENCE_CANDIDATE_218.json", json_bytes(derived)),
        "currentSourceFileCount": len(refreshed_bindings),
        "changedFromReturn185Packet": changed_from_previous,
        "currentIndexBinding": idx_bind,
        "currentCatalogBinding": cat_bind,
        "packet": archive_bind,
        "deliveryManifest": file_bind(DELIVERY),
        "members": len(member_rows) + 1,
        "checksPassed": len(checks),
        "checksFailed": 0,
        "checks": checks,
        "canonicalChangesBeforePreparation": False,
        "request": request,
    }
    write_json(PREP, prep)
    packet_record = {
        "id": "RANK9-DEFENSEFORM8-PACKET-218",
        "status": "PREPARED_UNSENT",
        "group": GROUP,
        "pendingIds": IDS,
        "sourceAuthority": AUTHORITY,
        "packet": archive_bind,
        "deliveryManifest": file_bind(DELIVERY),
        "preparation": file_bind(PREP),
        "conversation": CHAT,
        "checksPassed": len(checks),
        "checksFailed": 0,
    }
    write_json(PACKET_RECORD, packet_record)

    queue_after = copy.deepcopy(queue)
    group_after = next(g for g in queue_after["currentPendingGroups"] if g["group"] == GROUP)
    group_after.update({"status": "CURRENT_SOURCE_PACKET_218_PREPARED_UNSENT_AT_808_40_0", "preparedPacket": archive_bind, "deliveryManifest": file_bind(DELIVERY), "packetRecord": file_bind(PACKET_RECORD), "preparation": file_bind(PREP), "freshPacketRequiredForCurrentAuthority": True})
    next_record = {"group": GROUP, "pendingIds": IDS, "pendingCount": len(IDS), "status": "CURRENT_SOURCE_PACKET_218_PREPARED_UNSENT_AT_808_40_0", "freshPacketRequiredForCurrentAuthority": True, "preparedPacket": archive_bind, "deliveryManifest": file_bind(DELIVERY), "packetRecord": file_bind(PACKET_RECORD), "preparation": file_bind(PREP)}
    queue_after.update({"id": "SPELL-REVIEW-QUEUE-218", "recordedAtUtc": ts, "supersedesQueue": file_bind(QUEUE_BEFORE), "currentPendingGroups": queue_after["currentPendingGroups"], "nextGroup": GROUP, "next": next_record, "nextPreparedRequest": next_record, "nextSuggestedGroups": [g for g in queue_after["currentPendingGroups"] if not str(g.get("status", "")).startswith("HELD_")][:5], "currentPreparation": file_bind(PREP), "currentPacket": archive_bind, "currentDeliveryManifest": file_bind(DELIVERY), "packetStatus": "RANK9_DEFENSEFORM8_SOURCE_PACKET_218_PREPARED_UNSENT_808_40"})
    write_json(QUEUE_AFTER, queue_after)
    queue_binding = file_bind(QUEUE_AFTER)
    handoff_after = copy.deepcopy(handoff)
    handoff_after.update({"id": "CURRENT-HANDOFF-218", "recordedAtUtc": ts, "status": "RANK9_DEFENSEFORM8_CURRENT_SOURCE_PACKET_PREPARED_UNSENT_808_40", "currentAuthority": AUTHORITY, "currentQueue": queue_binding, "currentPendingIdentityAudit": file_bind(PENDING), "nextGroup": GROUP, "nextPendingIds": IDS, "nextPendingCount": len(IDS), "nextPreparedRequest": next_record, "currentPreparation": file_bind(PREP), "currentPacket": archive_bind, "currentDeliveryManifest": file_bind(DELIVERY), "postApplicationIndependentAudit": file_bind(BASE / "RANK9DEATHRECOVERY3_POST_APPLICATION_INDEPENDENT_AUDIT_217.json"), "resumePriority": "Send the refreshed Defense/Form8 packet to GPT director; audit and apply only exact accepted identities; retain Final Word and Psychic/Fear holds; continue queue until pending reaches zero."})
    write_json(HANDOFF_AFTER, handoff_after)
    snapshot = (
        "# Current Spell Review Snapshot — Packet 218\n\n"
        "Current authority is **808 applied / 40 pending / 0 accepted-unapplied**. Return217 applied Doom and Eternal Pact; Final Word remains held on DR217-B01. Psychic/Fear identities remain held on PF182-B01/B02.\n\n"
        f"A current-source packet is prepared for exactly five Defense/Form8 identities: `{', '.join(IDS)}`. The earlier three Return186 acceptances are already applied and excluded. Packet checks passed; it has not yet been sent.\n"
    )
    SNAPSHOT.write_text(snapshot, encoding="utf-8")
    REQUEST_EXTERNAL.write_text(request, encoding="utf-8")

    print(json.dumps({"status": "PREPARED_UNSENT", "authority": AUTHORITY, "group": GROUP, "pendingIds": IDS, "sourceFiles": len(refreshed_bindings), "changedFromReturn185": changed_from_previous, "packet": archive_bind, "deliveryManifest": file_bind(DELIVERY), "memberCount": len(member_rows) + 1, "checksPassed": len(checks), "checksFailed": 0, "next": str(REQUEST_EXTERNAL.relative_to(ROOT))}, indent=2))


if __name__ == "__main__":
    main()
