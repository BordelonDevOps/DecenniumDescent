from __future__ import annotations

import datetime as dt
import hashlib
import json
import pathlib
import subprocess
import zlib
import zipfile

ROOT = pathlib.Path.cwd()
A = ROOT / "docs/audit/2026-10-08/full-game/director-spell-review-129"
OUT = A / "rank9_wardcontrol6_source_packet_312_prepared"
PACKET = OUT / "DD_Rank9_WardControl6_CurrentSource_312.zip"
DELIVERY = OUT / "DD_Rank9_WardControl6_CurrentSource_312_DELIVERY.json"
OLD_SOURCE_PACKET = A / "rank9_wardcontrol6_source_packet_281_refreshed/DD_Rank9_WardControl6_CurrentSource_281.zip"
OLD_SOURCE_DELIVERY = A / "rank9_wardcontrol6_source_packet_281_refreshed/DD_Rank9_WardControl6_CurrentSource_281_DELIVERY.json"
OLD_RETURN = A / "rank9_wardcontrol6_return281_received/DD_Rank9_WardControl6_Director_Return281_HELD.zip"
OLD_RETURN_DELIVERY = A / "rank9_wardcontrol6_return281_received/DD_Rank9_WardControl6_Director_Return281_HELD_DELIVERY.json"
OLD_RETURN_AUDIT = A / "RANK9_WARDCONTROL6_RETURN281_INDEPENDENT_AUDIT.json"
RETURN310 = A / "rank9_defenseform8_return310_received/DD_Rank9_DefenseForm8_Director_Return310_HELD.zip"
RETURN310_DELIVERY = A / "rank9_defenseform8_return310_received/DD_Rank9_DefenseForm8_Director_Return310_HELD_DELIVERY.json"
RETURN310_AUDIT = A / "INVULNERABLE_SPHERE_RETURN310_INDEPENDENT_AUDIT.json"
RETURN310_HOLD = A / "INVULNERABLE_SPHERE_HOLD_RECEIPT_310.json"
QUEUE311 = A / "CURRENT_SPELL_QUEUE_311.json"
HANDOFF311 = A / "CURRENT_HANDOFF_311.json"
PENDING310 = A / "CURRENT26_PENDING_IDENTITY_AUDIT_310.json"
INDEX = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json"
CATALOG = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json"
GROUP = "rank9-ward-control6"
TARGET = "nullification-wave"
BLOCKER = "WC188-B01"
AUTH = {"reviewedApplied": 822, "pending": 26, "acceptedUnapplied": 0,
        "completeStandaloneProcedures": 546, "scopedInterfaces": 173}
ETERNAL_DIR = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_candidates/eternalforge_reviewed_255"
AUDIT_EXTRA = A


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def crc(raw: bytes) -> str:
    return f"{zlib.crc32(raw) & 0xffffffff:08x}"


def digest(raw: bytes) -> dict:
    return {"bytes": len(raw), "sha256": sha(raw), "crc32": crc(raw)}


def read(path: pathlib.Path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def bind(path: pathlib.Path, raw: bytes | None = None, rel: str | None = None) -> dict:
    data = path.read_bytes() if raw is None else raw
    return {"path": rel or path.relative_to(ROOT).as_posix(), **digest(data)}


def jb(value) -> bytes:
    return (json.dumps(value, indent=2, ensure_ascii=False) + "\n").encode("utf-8")


def main() -> None:
    assert not OUT.exists(), f"Refusing to overwrite existing preparation directory: {OUT}"
    OUT.mkdir(parents=True)
    now = dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")
    branch = subprocess.check_output(["git", "branch", "--show-current"], cwd=ROOT, text=True).strip()
    base_commit = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    index_current = INDEX.read_bytes()
    catalog_current = CATALOG.read_bytes()
    with zipfile.ZipFile(OLD_RETURN) as old_return, zipfile.ZipFile(OLD_SOURCE_PACKET) as old_packet:
        old_rows = json.loads(old_return.read("SOURCE_BINDINGS.json"))["currentBindings"]
        old_case_index = json.loads(old_return.read("CASE_INDEX.json"))
        wave_rows = [r for r in old_case_index["cases"] if r["spellId"] == TARGET]
        assert len(old_rows) == 91 and len(wave_rows) == 18
        source_payload: dict[str, bytes] = {}
        old_source_payload: dict[str, bytes] = {}
        old_bindings = []
        current_bindings = []
        changed = []
        for row in old_rows:
            path = row["path"]
            current_file = ROOT / pathlib.Path(path)
            current_raw = current_file.read_bytes()
            old_raw = old_packet.read("sources_current/" + path)
            old_digest = digest(old_raw)
            assert old_digest["bytes"] == row["bytes"] and old_digest["sha256"] == row["sha256"], path
            current_digest = digest(current_raw)
            old_bindings.append({"path": path, **old_digest})
            current_bindings.append({"path": path, **current_digest})
            if current_raw != old_raw:
                changed.append({"path": path, "previousPacket": old_digest, "currentWorktree": current_digest})
            source_payload["sources_current/" + path] = current_raw
            old_source_payload["old_source_bindings/" + path + ".json"] = jb(old_digest)

        history_files: dict[str, bytes] = {}
        exact_history_names = [
            "ACTOR_PROFILES.json", "BLOCKERS.json", "QUALIFICATIONS.json", "SOURCE_PAIR_TABLE.json",
            "ORIGINAL_OBLIGATIONS.json", "QUESTION_DISPOSITIONS.json", "HOLD_REGISTER.json",
            "REMAINING_QUEUE.json", "procedures/nullification-wave.json",
        ]
        for name in exact_history_names:
            history_files["history/Return281/" + name] = old_return.read(name)
        for row in wave_rows:
            path = row["path"]
            history_files["history/Return281/" + path] = old_return.read(path)
        wave_case_ids = [r["id"] for r in wave_rows]
        assert "WC237-NW-HELPER" in wave_case_ids and "WC237-NW-COUNTER" in wave_case_ids
        case_index = {
            "id": "NULLIFICATION-WAVE-RETURN281-CASE-INDEX-312",
            "scopeIds": [TARGET],
            "sourceArchive": bind(OLD_RETURN),
            "caseCount": len(wave_rows),
            "cases": wave_rows,
            "historicalAnchorCasesExcludedFromTargetScope": True,
        }
        history_files["history/Return281/WAVE_CASE_INDEX_312.json"] = jb(case_index)

    source_refresh = {
        "id": "NULLIFICATION-WAVE-91-SOURCE-REFRESH-312",
        "recordedAtUtc": now,
        "sourceCount": len(current_bindings),
        "previousSourceArchive": bind(OLD_SOURCE_PACKET),
        "previousSourceDelivery": bind(OLD_SOURCE_DELIVERY),
        "previousReturnSourceBindings": bind(OLD_RETURN),
        "previousBindings": old_bindings,
        "currentBindings": current_bindings,
        "changedSincePacket281": changed,
        "all91RefreshedFromCurrentWorktree": True,
        "sourceFilesExecuted": False,
    }

    extra_paths = {
        "source/glove-null-ink/epilogue_relic_null_reviewed_01.json": ROOT / "DescentReviewChanges/ReviewBible/data/director/cosmology/epilogue_relic_null_reviewed_01.json",
        "source/glove-null-ink/COSMOLOGY_EPILOGUE_RELIC_NULL_PLAYTEST.md": ROOT / "DescentReviewChanges/ReviewBible/docs/mechanics/COSMOLOGY_EPILOGUE_RELIC_NULL_PLAYTEST.md",
        "source/eternal-forge/MODEL.json": ETERNAL_DIR / "MODEL.json",
        "source/eternal-forge/EXACT_ACCEPTANCE.json": ETERNAL_DIR / "EXACT_ACCEPTANCE.json",
        "source/eternal-forge/DIRECTOR_ACCEPTANCE.json": ETERNAL_DIR / "DIRECTOR_ACCEPTANCE.json",
        "source/eternal-forge/SUPPLEMENT255_W2.json": ETERNAL_DIR / "SUPPLEMENT255_W2.json",
        "source/eternal-forge/SUPPLEMENT255_INDEPENDENT_AUDIT.json": ETERNAL_DIR / "SUPPLEMENT255_INDEPENDENT_AUDIT.json",
        "evidence/ETERNAL_FORGE_EXACT_ACCEPTANCE_255.json": AUDIT_EXTRA / "ETERNAL_FORGE_EXACT_ACCEPTANCE_255.json",
        "evidence/ETERNAL_FORGE_DIRECTOR_ACCEPTANCE_255.json": AUDIT_EXTRA / "ETERNAL_FORGE_DIRECTOR_ACCEPTANCE_255.json",
        "evidence/ETERNAL_FORGE_MF210_B01_WITNESS_SUPPLEMENT_255.json": AUDIT_EXTRA / "ETERNAL_FORGE_MF210_B01_WITNESS_SUPPLEMENT_255.json",
        "evidence/ETERNAL_FORGE_MF210_B01_SUPPLEMENT_255_INDEPENDENT_AUDIT.json": AUDIT_EXTRA / "ETERNAL_FORGE_MF210_B01_SUPPLEMENT_255_INDEPENDENT_AUDIT.json",
    }
    extra_bindings = []
    extra_payload = {}
    for member, path in extra_paths.items():
        raw = path.read_bytes()
        extra_payload[member] = raw
        extra_bindings.append({"member": member, **bind(path, raw)})

    current_index = json.loads(index_current)
    current_catalog = json.loads(catalog_current)
    pending_ids = [r["id"] for r in current_index["entries"] if r.get("authoredStatus") == "pending-authored-procedure"]
    assert len(pending_ids) == 26 and all(sid in {r["id"] for r in current_catalog["spells"]} for sid in pending_ids)
    catalog_by_id = {r["id"]: r for r in current_catalog["spells"]}
    assert catalog_by_id[TARGET].get("operational") is None
    overlay = {
        "baseCommit": base_commit,
        "branch": branch,
        "baseIndex": digest(subprocess.check_output(["git", "show", f"{base_commit}:DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json"], cwd=ROOT)),
        "workingTreeIndex": digest(index_current),
        "baseCatalog": digest(subprocess.check_output(["git", "show", f"{base_commit}:DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json"], cwd=ROOT)),
        "workingTreeCatalog": digest(catalog_current),
        "canonicalFilesChangedByThisPacket": False,
    }

    requirements = {
        "id": "NULLIFICATION-WAVE-DIRECTOR-REQUIREMENTS-312",
        "recordedAtUtc": now,
        "status": "DIRECTOR_PREPARATION_GUIDANCE_ONLY_NOT_ADJUDICATION",
        "scopeIds": [TARGET], "blockerIds": [BLOCKER],
        "authority": AUTH,
        "separateNextIdentity": {"spellId": "reality-anchor", "blockerId": "WC188-B02", "jointPacketRequired": False},
        "missingEvidence": "A continuing magical property's classification and complete terminal history, not merely possession of a magical item.",
        "exactIncompleteRecordsToRetain": [
            "RANK9WARDCONTROL6129-NULLIFICATION-WAVE-B/unique-permanent-item-qualification",
            "WC219-NW-UNIQUE",
        ],
        "conditionalRecord": {"id": "RANK9WARDCONTROL6129-NULLIFICATION-WAVE-B/mandatory-reversion-conflict",
                              "status": "REMAINS_CONDITIONAL_DO_NOT_PROMOTE"},
        "candidateGloveOfNullInk": {
            "recordId": "RELIC-NULL-GLOVE-1",
            "anchor": "DescentReviewChanges/ReviewBible/data/director/cosmology/epilogue_relic_null_reviewed_01.json#/currentModule/relics/3",
            "factsAlreadySpecified": ["CH03 acquisition", "physical glove", "Action activation", "10-foot writing range", "one inscription", "600-second inscription lifetime"],
            "missing": "Whether its underlying continuing writing property is an independently terminable enhancement, and what permanent removal leaves behind or permits afterward. Ending a finite inscription does not demonstrate removal of the underlying property; Matrix-dust provenance supplies no removal permission.",
            "sourceBindings": [extra_bindings[0], extra_bindings[1]],
        },
        "candidateEternalForge": {
            "indexPointer": "authored_review_index.json#/entries/190",
            "procedurePointer": "spell_candidates/eternalforge_reviewed_255/MODEL.json#/spells/0/procedure",
            "acceptedEnvelopeBindings": [x for x in extra_bindings if "ACCEPTANCE" in x["member"] or "DIRECTOR_ACCEPTANCE" in x["member"]],
            "witnessW2Bindings": [x for x in extra_bindings if "W2" in x["member"] or "SUPPLEMENT_255" in x["member"]],
            "status": "LEAD_ONLY_NOT_VERIFIED_AS_CLOSING_WC188_B01",
            "note": "The W2 supplement is pending Director review. Bind it only as evidence; do not promote it to acceptance or assume termination of a Forge root proves a removable permanent item enhancement.",
        },
        "sourceBindings": {
            "currentWardControlInventoryCount": 91,
            "previousCurrentSourcePacket": bind(OLD_SOURCE_PACKET),
            "refreshRecord": {"path": "SOURCE_REFRESH_312.json", "changedCount": len(changed)},
            "preservePriorHashes": True,
        },
        "preserveExactReturn281": {
            "archive": bind(OLD_RETURN), "delivery": bind(OLD_RETURN_DELIVERY),
            "independentAudit": bind(OLD_RETURN_AUDIT),
            "procedureMember": "procedures/nullification-wave.json",
            "exactWaveCaseIds": wave_case_ids,
            "exactWaveCaseCount": 18,
            "preserveMemberPaths": exact_history_names + [r["path"] for r in wave_rows],
            "preserveCorrectedCases": ["WC237-NW-HELPER", "WC237-NW-COUNTER"],
            "preserveSupersededHistory": ["WC219-NW-HELPER", "WC219-NW-COUNTER"],
        },
        "preserveQuestionAndObligationIds": ["WC9-Q01", "WC9-Q06", "WC9-Q07", "WC9-Q08", "WARD129-ADD01"],
        "procedureConstraints": [
            "60-foot center range and 60-foot-radius 3D capture",
            "initial-cover clipping and immutable admission",
            "simultaneous-ending ordering and source-owned cleanup",
            "no-save operation; all-spell reflection; protected-source exceptions; antimagic interception",
            "do not import Greater Dispel scope/checks, rescan after wall removal, or erase completed physical changes",
        ],
        "qualificationHandling": "Retain all Return281 qualifications, including WC188-H-UNIQUE-PROPERTY and WC219-Q-UNIQUE/SOURCE/PHYSICAL/RUNTIME. The unique-property alias is not another blocker.",
        "realityAnchor": "Keep separate. Shared component evidence may later be reused; B02 additionally needs actual deny/allow, expiry/ending while denied, and surviving-source resumption without refill. Permission mode needs no invented school; Transmutation mode needs actual generating-school evidence.",
        "remainingOrder": ["nullification-wave", "reality-anchor", "time-stop", "fate-rewrite", "collapse-timeline", "eternal-prophecy", "faction-omniscience-supreme", "banishment-gate", "conjure-demiplane-fortress", "summon-elemental-avatar", "summon-herald-of-the-planes", "summon-avatar-of-decay", "reverse-gravity-field", "alignment-ascension", "alignment-perfection", "faction-incarnate", "faction-perfection", "corruption-purification", "astral-projection", "imprisonment", "divine-intervention-greater", "wish"],
        "separatelyHeld": ["final-word", "elemental-shell", "timeless-form", "invulnerable-sphere"],
        "closureTasksRemaining": 26, "firstReviewTasksRemaining": 0,
        "noAcceptanceOrApplicationIssued": True,
    }
    requirements_path = A / "NULLIFICATION_WAVE_DIRECTOR_REQUIREMENTS_312.json"
    requirements_path.write_text(json.dumps(requirements, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    pending_audit = {
        "id": "CURRENT26-PENDING-IDENTITY-AUDIT-311",
        "recordedAtUtc": now,
        "status": "PASS_CURRENT_822_26_AFTER_RETURN310_AND_WAVE_SCOPE_GUIDANCE",
        "supersedes": "CURRENT26-PENDING-IDENTITY-AUDIT-310",
        "authority": AUTH,
        "indexBinding": bind(INDEX, index_current), "catalogBinding": bind(CATALOG, catalog_current),
        "pendingCount": 26, "pendingIds": sorted(pending_ids),
        "allPendingIdsExistInNativeCatalog": True,
        "allCurrentPendingIdentitiesReviewed": True, "unreviewedPendingIds": [],
        "acceptedIds": [], "appliedIds": [],
        "separatelyHeldIds": ["final-word", "elemental-shell", "timeless-form", "invulnerable-sphere"],
        "separateBlockers": {"final-word": ["DR217-B01"], "elemental-shell": ["DF218-B01", "DF218-B02"],
                             "timeless-form": ["DF218-B03"], "invulnerable-sphere": ["DF218-B04"]},
        "nextGroup": GROUP, "nextPendingIds": ["nullification-wave", "reality-anchor"], "nextPendingCount": 2,
        "currentTargetIds": [TARGET], "currentBlockers": {TARGET: [BLOCKER]},
        "directorRequirements": {"path": requirements_path.relative_to(ROOT).as_posix(),
                                 "bytes": requirements_path.stat().st_size, "sha256": sha(requirements_path.read_bytes()),
                                 "crc32": crc(requirements_path.read_bytes())},
        "closureTasksRemaining": 26, "firstReviewTasksRemaining": 0,
        "canonicalFilesChanged": False,
    }
    pending_path = A / "CURRENT26_PENDING_IDENTITY_AUDIT_311.json"
    pending_path.write_text(json.dumps(pending_audit, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    queue = {
        "id": "SPELL-REVIEW-QUEUE-312", "recordedAtUtc": now,
        "supersedesQueue": bind(A / "CURRENT_SPELL_QUEUE_311.json"),
        "currentAuthority": AUTH, "currentIndexBinding": bind(INDEX, index_current),
        "currentCatalogBinding": bind(CATALOG, catalog_current),
        "pendingCount": 26, "acceptedUnapplied": 0,
        "nextGroup": GROUP, "nextPendingIds": ["nullification-wave", "reality-anchor"], "nextPendingCount": 2,
        "activeReview": {"identity": TARGET, "blockerIds": [BLOCKER], "scopeIds": [TARGET],
                         "jointReview": False, "status": "DIRECTOR_SCOPE_CONFIRMED_PACKET_IN_PREPARATION"},
        "next": {"group": GROUP, "pendingIds": [TARGET], "pendingCount": 1,
                 "status": "DIRECTOR_PREPARATION_GUIDANCE_WAVE_ALONE_312",
                 "freshPacketRequiredForCurrentAuthority": True,
                 "blockerByIdentity": {TARGET: [BLOCKER]},
                 "then": {"identity": "reality-anchor", "blockerIds": ["WC188-B02"]}},
        "remainingPriorityOrder": requirements["remainingOrder"],
        "separatelyHeld": requirements["separatelyHeld"],
        "closureTasksRemaining": 26, "firstReviewTasksRemaining": 0,
        "lastDirectorReturn": {"archive": bind(RETURN310), "delivery": bind(RETURN310_DELIVERY),
                               "independentAudit": bind(RETURN310_AUDIT), "holdReceipt": bind(RETURN310_HOLD),
                               "acceptedIds": [], "appliedIds": [], "heldIds": ["invulnerable-sphere"],
                               "blockerIds": ["DF218-B04"]},
        "directorRequirements": bind(requirements_path),
        "pendingIdentityAudit": bind(pending_path),
        "priorScopePointersSuperseded": ["CURRENT_HANDOFF_310.json#nextPendingGroup/currentPreparation", "CURRENT_HANDOFF_311.json#directorConnectionStatus"],
        "canonicalFilesChanged": False, "applicationPerformed": False,
    }
    queue_path = A / "CURRENT_SPELL_QUEUE_312.json"
    queue_path.write_text(json.dumps(queue, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    handoff = {
        "id": "CURRENT-HANDOFF-312", "recordedAtUtc": now,
        "supersedes": bind(A / "CURRENT_HANDOFF_311.json"),
        "status": "NULLIFICATION_WAVE_PACKET_312_PREPARED_UNSENT",
        "authority": AUTH, "indexBinding": bind(INDEX, index_current),
        "queueBinding": bind(queue_path), "queue": queue_path.relative_to(ROOT).as_posix(),
        "pendingIdentityAudit": bind(pending_path), "appliedThisStep": [], "acceptedThisStep": [],
        "currentBlocker": {"identity": TARGET, "group": GROUP, "blockerIds": [BLOCKER]},
        "nextPendingGroup": queue["next"],
        "directorRequirements": bind(requirements_path),
        "currentPreparation": {"path": "docs/audit/2026-10-08/full-game/director-spell-review-129/RANK9_WARDCONTROL6_SOURCE_PREPARATION_312.json",
                               "status": "PREPARING_PACKET", "scopeIds": [TARGET]},
        "currentPacket": {"path": PACKET.relative_to(ROOT).as_posix(), "status": "prepared-by-this-workflow"},
        "currentPacketDelivery": {"path": DELIVERY.relative_to(ROOT).as_posix()},
        "previousReturn": queue["lastDirectorReturn"],
        "remainingPriorityOrder": requirements["remainingOrder"],
        "separatelyHeld": requirements["separatelyHeld"],
        "closureTasksRemaining": 26, "firstReviewTasksRemaining": 0,
        "githubChanges": False, "canonicalFilesChanged": False, "applicationPerformed": False,
    }
    handoff_path = A / "CURRENT_HANDOFF_312.json"
    handoff_path.write_text(json.dumps(handoff, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    # Refresh the independent source set and bind the exact submission state.
    source_meta = {
        "id": "RANK9-WARDCONTROL6-CURRENT-SOURCE-CONTEXT-312",
        "recordedAtUtc": now, "currentAuthority": AUTH,
        "currentPendingGroup": {"group": GROUP, "spellIds": [TARGET], "count": 1},
        "currentIndexBinding": bind(INDEX, index_current), "currentCatalogBinding": bind(CATALOG, catalog_current),
        "pendingIdentityAuditBinding": bind(pending_path), "queueBinding": bind(queue_path), "handoffBinding": bind(handoff_path),
        "sourceSnapshot": overlay,
        "sourceBindingRefresh": {"sourceFiles": 91, "changedSincePacket281": changed,
                                 "allSourceBindingsRefreshedFromWorkingTree": True},
        "currentNext": queue["next"], "closureTasksRemaining": 26, "firstReviewTasksRemaining": 0,
    }
    request = (
        "Review only Nullification Wave / WC188-B01 at the current 822/26/0 authority. Reality Anchor / WC188-B02 "
        "is explicitly separate and remains next; do not adjudicate it in this packet. The 91 Ward/Control source "
        "bindings were refreshed with prior Packet281 hashes retained. Preserve the exact Return281 Nullification Wave "
        "procedure, blocker, qualifications, source-pair table, actor profiles, selected questions/obligations, and all "
        "18 Wave cases, including corrected WC237-NW-HELPER/WC237-NW-COUNTER and superseded WC219 predecessors. "
        "The Glove of Null Ink and Eternal Forge W2 records are leads only. Do not infer a qualifying permanent "
        "enhancement, termination right, acquisition or witness from possession, a finite inscription, or Forge-root "
        "termination. Adjudicate only source-supported evidence. Return the sealed decision ZIP and exact DELIVERY.json; "
        "if WC188-B01 remains open, state the narrowest remaining evidence without inventing a component or encounter. "
        "Do not revise unrelated blockers or accept/apply beyond the exact supported decision. Confirm acceptedIds, "
        "appliedIds, heldIds, authority, and next order/count."
    )
    core_payload = {
        "CURRENT_AUTHORITY_312.json": jb({"authority": AUTH, "scopeIds": [TARGET], "blockerIds": [BLOCKER], "sourceSnapshot": overlay}),
        "CURRENT_SOURCE_CONTEXT_312.json": jb(source_meta),
        "SOURCE_REFRESH_312.json": jb(source_refresh),
        "NULLIFICATION_WAVE_DIRECTOR_REQUIREMENTS_312.json": requirements_path.read_bytes(),
        "CURRENT26_PENDING_IDENTITY_AUDIT_311.json": pending_path.read_bytes(),
        "CURRENT_SPELL_QUEUE_312.json": queue_path.read_bytes(),
        "CURRENT_HANDOFF_312.json": handoff_path.read_bytes(),
        "RETURN310_HOLD_RECEIPT.json": RETURN310_HOLD.read_bytes(),
        "RETURN310_INDEPENDENT_AUDIT.json": RETURN310_AUDIT.read_bytes(),
        "RETURN310_DELIVERY.json": RETURN310_DELIVERY.read_bytes(),
        "RETURN310_DIRECTOR_RETURN.zip": RETURN310.read_bytes(),
        "RETURN281_INDEPENDENT_AUDIT.json": OLD_RETURN_AUDIT.read_bytes(),
        "RETURN281_DELIVERY.json": OLD_RETURN_DELIVERY.read_bytes(),
        "RETURN281_DIRECTOR_RETURN.zip": OLD_RETURN.read_bytes(),
        "REQUEST_312.txt": request.encode("utf-8"),
        "WAVE_CASE_INDEX_312.json": jb(case_index),
        "WAVE_SOURCE_EXTRA_BINDINGS_312.json": jb({"records": extra_bindings}),
        "ETERNAL_FORGE_ACCEPTED_ENVELOPE_AND_W2_CONTEXT_312.json": jb({
            "currentIndexEntryPointer": "authored_review_index.json#/entries/190",
            "sourceStatus": "accepted" if any(r.get("id") == "eternal-forge" and r.get("authoredStatus") == "accepted" for r in current_index["entries"]) else "review_current_index",
            "selectedLeadBindings": [x for x in extra_bindings if "eternal-forge" in x["member"]],
            "w2CurrentStatus": read(ETERNAL_DIR / "SUPPLEMENT255_W2.json")["status"],
            "w2IndependentAuditStatus": read(ETERNAL_DIR / "SUPPLEMENT255_INDEPENDENT_AUDIT.json")["status"],
            "limitations": "Lead only. The W2 supplement remains pending Director review; it does not prove WC188-B01 or authorize new acceptance/application.",
        }),
    }
    payload = {**source_payload, **old_source_payload, **history_files, **extra_payload, **core_payload}
    # Bind every non-manifest member, then write a self-excluding internal manifest.
    rows = [{"path": name, **digest(raw)} for name, raw in sorted(payload.items())]
    manifest = {
        "id": "RANK9-WARDCONTROL6-PACKET312-MEMBER-MANIFEST",
        "scopeIds": [TARGET], "blockerIds": [BLOCKER], "authority": AUTH,
        "acceptedIds": [], "appliedIds": [], "targetHeldIdsIfUnresolved": [TARGET],
        "sourceCount": 91, "sourceArchivePreviousPacket": bind(OLD_SOURCE_PACKET),
        "selfExcluded": True, "memberCountExcludingSelf": len(rows),
        "exactPayloadAllowlist": [r["path"] for r in rows], "members": rows,
    }
    manifest_raw = jb(manifest)
    all_members = {**payload, "MEMBER_MANIFEST.json": manifest_raw}
    OUT.mkdir(exist_ok=True)
    with zipfile.ZipFile(PACKET, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=6, allowZip64=True) as z:
        for name, raw in sorted(all_members.items()):
            info = zipfile.ZipInfo(name)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            z.writestr(info, raw, compress_type=zipfile.ZIP_DEFLATED, compresslevel=6)
    packet_raw = PACKET.read_bytes()
    delivery = {
        "id": "RANK9-WARDCONTROL6-CURRENT-SOURCE-PACKET-312-DELIVERY",
        "recordedAtUtc": now,
        "archive": {"fileName": PACKET.name, **digest(packet_raw)},
        "authority": AUTH, "targetIds": [TARGET], "blockerIds": [BLOCKER],
        "acceptedIds": [], "appliedIds": [], "proposedHeldIdsIfUnresolved": [TARGET],
        "nextPendingGroup": {"group": GROUP, "nextIdentity": TARGET, "blockerIds": [BLOCKER],
                             "thenIdentity": "reality-anchor", "thenBlockerIds": ["WC188-B02"]},
        "closureTasksRemaining": 26, "firstReviewTasksRemaining": 0,
        "sourceBindingRefresh": {"count": 91, "changedCount": len(changed), "changed": changed,
                                 "previousPacketSHA256": sha(OLD_SOURCE_PACKET.read_bytes())},
        "currentSourceSnapshot": overlay,
        "memberCount": len(all_members), "payloadCount": len(payload),
        "memberManifest": {"path": "MEMBER_MANIFEST.json", **digest(manifest_raw)},
        "exactAllowlist": sorted(all_members),
        "members": [{"path": name, **digest(raw)} for name, raw in sorted(all_members.items())],
        "newEvidenceAdded": False, "canonicalFilesChanged": False, "applicationPerformed": False,
        "submissionRequest": request,
    }
    DELIVERY.write_text(json.dumps(delivery, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    prep = {
        "id": "RANK9-WARDCONTROL6-SOURCE-PREPARATION-312",
        "recordedAtUtc": now, "status": "CURRENT_SOURCE_PACKET_PREPARED_UNSENT_822_26_0",
        "scopeIds": [TARGET], "blockerIds": [BLOCKER], "authority": AUTH,
        "sourceRefresh": bind(A / "SOURCE_REFRESH_312.json", jb(source_refresh)) if False else {
            "sourceCount": 91, "changedCount": len(changed), "changed": changed},
        "packet": {"path": PACKET.relative_to(ROOT).as_posix(), **digest(packet_raw)},
        "delivery": {"path": DELIVERY.relative_to(ROOT).as_posix(), **digest(DELIVERY.read_bytes())},
        "requirements": bind(requirements_path), "queue": bind(queue_path), "handoff": bind(handoff_path),
        "pendingAudit": bind(pending_path), "memberCount": len(all_members),
        "sourceSnapshot": overlay, "submissionPerformed": False,
    }
    (A / "RANK9_WARDCONTROL6_SOURCE_PREPARATION_312.json").write_text(json.dumps(prep, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    (A / "RANK9_WARDCONTROL6_PACKET_312.json").write_text(json.dumps({"id": "RANK9-WARDCONTROL6-PACKET-312",
        "packet": prep["packet"], "delivery": prep["delivery"], "scopeIds": [TARGET], "blockerIds": [BLOCKER],
        "authority": AUTH, "status": "PREPARED_UNSENT"}, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": prep["status"], "packet": prep["packet"], "delivery": prep["delivery"],
                      "sourceCount": 91, "changedSourceCount": len(changed), "waveCaseCount": len(wave_rows),
                      "memberCount": len(all_members), "externalLeadCount": len(extra_bindings)}, indent=2))


if __name__ == "__main__":
    main()
