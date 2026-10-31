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
BASE = ROOT / "docs/audit/2026-10-08/full-game/director-spell-review-129"
FULL = ROOT / "docs/audit/2026-10-08/full-game"
GROUP = "rank9-defense-form8"
TARGETS = ["elemental-shell", "timeless-form", "invulnerable-sphere"]
PREVIOUS_ACCEPTED = ["absolute-immunity", "body-to-void"]
AUTHORITY = {"reviewedApplied": 811, "pending": 37, "acceptedUnapplied": 0, "completeStandaloneProcedures": 535, "scopedInterfaces": 173}
CHAT = "https://chatgpt.com/g/g-p-67f17555a8dc8191a2b5b81e6d8adc12-dungeon-crawler/c/6adc506d-8770-83ea-b64c-0345d9b9b682"
OUT = BASE / "rank9_defenseform8_current_source_236_prepared"
PACKET = OUT / "DD_Rank9_DefenseForm8_CurrentSource_236.zip"
DELIVERY = OUT / "DD_Rank9_DefenseForm8_CurrentSource_236_DELIVERY.json"
PREP = BASE / "RANK9_DEFENSEFORM8_SOURCE_PREPARATION_236.json"
PACKET_RECORD = BASE / "RANK9_DEFENSEFORM8_PACKET_236.json"


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def crc(raw: bytes) -> str:
    return f"{zlib.crc32(raw) & 0xffffffff:08x}"


def enc(value) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8")


def read(path: Path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def bind(path: str, raw: bytes) -> dict:
    return {"path": path, "bytes": len(raw), "sha256": sha(raw), "crc32": crc(raw)}


def file_bind(path: Path) -> dict:
    return bind(path.relative_to(ROOT).as_posix(), path.read_bytes())


def safe(name: str) -> bool:
    p = PurePosixPath(name)
    return bool(name) and "\\" not in name and not p.is_absolute() and all(part not in ("", ".", "..") for part in p.parts)


def add(files: dict[str, bytes], name: str, raw: bytes) -> None:
    assert safe(name), name
    assert name not in files, name
    files[name] = raw


def main() -> None:
    assert not PREP.exists() and not PACKET_RECORD.exists()
    if OUT.exists():
        assert {path.name for path in OUT.iterdir()} == {PACKET.name, DELIVERY.name}
    branch = subprocess.check_output(["git", "branch", "--show-current"], cwd=ROOT, text=True).strip()
    commit = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    assert branch == "main", branch
    now = datetime.now(timezone.utc).isoformat()

    qpath = BASE / "CURRENT_SPELL_QUEUE_236.json"
    hpath = BASE / "CURRENT_HANDOFF_236.json"
    ppath = BASE / "CURRENT37_PENDING_IDENTITY_AUDIT_236.json"
    q, h, p = read(qpath), read(hpath), read(ppath)
    assert q["currentAuthority"] == h["currentAuthority"] == p["authority"] == AUTHORITY
    assert q["nextGroup"] == GROUP and q["next"]["pendingIds"] == TARGETS
    assert q["status"] == "RETURN235_AUDITED_HELD_811_37_0_PACKET236_PREPARATION"
    assert p["pendingCount"] == len(p["pendingIds"]) == 37 and set(TARGETS).issubset(p["pendingIds"])

    index_path = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json"
    catalog_path = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json"
    access_path = ROOT / "DescentReviewChanges/ReviewBible/data/director/spell_review/accepted_interface_registry_06.json"
    work_queue_path = ROOT / "DescentReviewChanges/ReviewBible/data/director/spell_review/remaining_work_queue_66.json"
    index_raw, catalog_raw, access_raw, work_queue_raw = (x.read_bytes() for x in (index_path, catalog_path, access_path, work_queue_path))
    index, catalog = json.loads(index_raw.decode("utf-8-sig")), json.loads(catalog_raw.decode("utf-8-sig"))
    assert index.get("authoredCounts") == {"reviewed": 811, "pending": 37}
    assert index.get("representationCounts", {}).get("completeReviewedStandaloneProcedures") == 535
    entries = {row["id"]: row for row in index["entries"]}
    spells = {row["id"]: row for row in catalog["spells"]}
    assert all(entries[s]["authoredStatus"] == "pending-authored-procedure" and spells[s].get("operational") is None for s in TARGETS)
    assert all(entries[s]["authoredStatus"] == "reviewed-authored-operational-playtest" for s in PREVIOUS_ACCEPTED)

    queue_group = next(row for row in q["currentPendingGroups"] if row["group"] == GROUP)
    candidate_path = ROOT / PurePosixPath(queue_group["candidate"]["path"])
    source_archive_path = ROOT / PurePosixPath(queue_group["archive"]["path"])
    current_candidate_raw = candidate_path.read_bytes()
    current_candidate = json.loads(current_candidate_raw.decode("utf-8-sig"))
    historical_candidate_raw = source_archive_path.read_bytes()
    assert (len(historical_candidate_raw), sha(historical_candidate_raw)) == (queue_group["archive"]["bytes"], queue_group["archive"]["sha256"])
    with zipfile.ZipFile(source_archive_path) as source_zip:
        assert source_zip.testzip() is None
        conference_candidate_raw = source_zip.read("CANDIDATE.json")
    conference_candidate = json.loads(conference_candidate_raw.decode("utf-8-sig"))
    assert current_candidate == conference_candidate
    candidate_reconciliation = {
        "id": "RANK9-DEFENSEFORM8-CANDIDATE-BINDING-RECONCILIATION-236",
        "recordedAtUtc": now,
        "queueCandidateBinding": queue_group["candidate"],
        "historicalArchiveCandidateBinding": bind("CANDIDATE.json", conference_candidate_raw),
        "currentWorktreeCandidateBinding": file_bind(candidate_path),
        "sourceArchiveBinding": file_bind(source_archive_path),
        "jsonStructuralEquality": True,
        "fieldDifferences": 0,
        "byteEqualityQueueCandidateToCurrent": sha(current_candidate_raw) == queue_group["candidate"]["sha256"] and len(current_candidate_raw) == queue_group["candidate"]["bytes"],
        "differenceType": "Current worktree candidate is byte-distinct from the queue-bound conference candidate but JSON-structurally identical." if current_candidate_raw != conference_candidate_raw else "byte-exact",
        "authority": AUTHORITY,
        "scope": TARGETS,
    }

    prior_packet = BASE / "rank9_defenseform8_source_packet_218_refreshed/DD_Rank9_DefenseForm8_CurrentSource_218.zip"
    prior_return_dir = BASE / "rank9_defenseform8_return218_received"
    prior_return = prior_return_dir / "DD_Rank9_DefenseForm5_Director_Return218.zip"
    prior_delivery = prior_return_dir / "DD_Rank9_DefenseForm5_Director_Return218_DELIVERY.json"
    prior_audit = BASE / "RANK9_DEFENSEFORM8_RETURN218_INDEPENDENT_AUDIT.json"
    assert read(prior_audit)["status"] == "PASS" and read(prior_audit)["checksFailed"] == 0
    prior_delivery_obj = read(prior_delivery)
    assert prior_delivery_obj["acceptedIds"] == PREVIOUS_ACCEPTED and prior_delivery_obj["applied"] is False
    assert prior_delivery_obj["heldIds"] == TARGETS and prior_delivery_obj["authority"]["reviewedApplied"] == 808

    # Refresh every historical source path into exact present working-tree bytes.
    with zipfile.ZipFile(prior_packet) as old_packet:
        assert old_packet.testzip() is None
        old_candidate = json.loads(old_packet.read("HISTORICAL_SOURCE_CONFERENCE_CANDIDATE_01.json").decode("utf-8-sig"))
        old_prepared_candidate = json.loads(old_packet.read("CURRENT_SOURCE_CONFERENCE_CANDIDATE_218.json").decode("utf-8-sig"))
        prior_prepared_sources = {row["path"]: old_packet.read("sources_current/" + row["path"]) for row in old_prepared_candidate["sourceBindings"]}
        prior_member_manifest_raw = old_packet.read("MANIFEST.json")
    assert old_candidate == conference_candidate and old_candidate == current_candidate
    assert len(old_prepared_candidate["sourceBindings"]) == 87
    refreshed = []
    source_files: dict[str, bytes] = {}
    changed = []
    for old in old_prepared_candidate["sourceBindings"]:
        rel = old["path"]
        source_path = ROOT / PurePosixPath(rel)
        raw = source_path.read_bytes()
        row = bind(rel, raw)
        refreshed.append(row)
        source_files["sources_current/" + rel] = raw
        if raw != prior_prepared_sources.get(rel):
            old_raw = prior_prepared_sources.get(rel, b"")
            changed.append({"path": rel, "previousBytes": len(old_raw), "previousSha256": sha(old_raw), "currentBytes": len(raw), "currentSha256": sha(raw)})
    assert len(refreshed) == len(source_files) == 87 and len({row["path"] for row in refreshed}) == 87

    # Preserve all target-specific prior procedures and case traces, while
    # carrying the prior decision, exact blocker register, and outer manifests.
    with zipfile.ZipFile(prior_return) as old_return:
        assert old_return.testzip() is None
        old_names = set(old_return.namelist())
        old_external_members = {row["path"]: row for row in prior_delivery_obj.get("members", [])}
        prior_manifest = json.loads(old_return.read("MEMBER_MANIFEST.json"))
        prior_internal_members = {row["path"]: row for row in prior_manifest["members"]}
        required_history = [
            "DIRECTOR_DECISION.json", "BLOCKER_REASSESSMENT.json", "COUNTS.json", "CASE_INDEX.json",
            "PROCEDURES.json", "INDEPENDENT_SEMANTIC_FAILURE_CHECK.json", "MEMBER_MANIFEST.json",
        ]
        excerpt_names = list(required_history)
        proc_records = json.loads(old_return.read("PROCEDURES.json"))["spells"]
        for spell in proc_records:
            if spell.get("spellId") in TARGETS:
                excerpt_names.append("procedures/" + spell["spellId"] + ".json")
        case_index = json.loads(old_return.read("CASE_INDEX.json"))
        target_cases = [row for row in case_index["cases"] if row.get("spellId") in TARGETS]
        excerpt_names.extend(row["path"] for row in target_cases)
        assert len(target_cases) > 15
        excerpts = []
        history_files: dict[str, bytes] = {}
        for name in sorted(set(excerpt_names)):
            assert name in old_names and name in old_external_members, name
            raw = old_return.read(name)
            external = old_external_members[name]
            assert (len(raw), sha(raw), crc(raw)) == (external["bytes"], external["sha256"], external["crc32"])
            if name in prior_internal_members:
                internal = prior_internal_members[name]
                assert (len(raw), sha(raw), crc(raw)) == (internal["bytes"], internal["sha256"], internal["crc32"])
            elif name != "MEMBER_MANIFEST.json":
                raise AssertionError(f"No internal source binding for excerpt: {name}")
            out_name = "history/Return218/" + name
            history_files[out_name] = raw
            excerpts.append({"originalPath": name, "packetPath": out_name, "bytes": len(raw), "sha256": sha(raw), "crc32": crc(raw)})
    excerpts_manifest = {
        "id": "RANK9-DEFENSEFORM8-RETURN218-EXCERPT-MANIFEST-236",
        "sourceArchive": file_bind(prior_return),
        "sourceDelivery": file_bind(prior_delivery),
        "sourceIndependentAudit": file_bind(prior_audit),
        "sourceInternalManifest": {"originalPath": "MEMBER_MANIFEST.json", "bytes": len(prior_member_manifest_raw), "sha256": sha(prior_member_manifest_raw), "crc32": crc(prior_member_manifest_raw)},
        "excerptCount": len(excerpts),
        "excerpts": excerpts,
        "note": "Each excerpt is byte-identical to the exact member independently bound by both Return218's internal archive manifest and external delivery manifest.",
    }

    return235_archive = BASE / "rank9_deathrecovery7_return235_received/DD_Rank9_FinalWord_Director_Return235_HELD.zip"
    return235_delivery = BASE / "rank9_deathrecovery7_return235_received/DD_Rank9_FinalWord_Director_Return235_HELD_DELIVERY.json"
    return235_audit = BASE / "RANK9DEATHRECOVERY7_RETURN235_INDEPENDENT_AUDIT.json"
    return235_receipt = BASE / "RANK9DEATHRECOVERY7_RETURN235_RECEIPT.json"
    assert read(return235_audit)["status"] == read(return235_receipt)["status"] == "PASS"

    focused_questions = [row for row in current_candidate.get("questions", []) if set(row.get("spellIds", [])) & set(TARGETS)]
    target_records = [row for row in current_candidate.get("records", []) if row.get("spellId") in TARGETS]
    assert len(target_records) == len(TARGETS) and len(focused_questions) >= 10
    candidate = copy.deepcopy(current_candidate)
    candidate.update({
        "id": "CURRENT-SOURCE-CONFERENCE-CANDIDATE-236",
        "recordedAtUtc": now,
        "status": "PREPARED_CURRENT_AUTHORITY_811_37_EXACT_DEFENSE_FORM8_PENDING_GROUP",
        "sourceCommitBase": commit,
        "sourceBranch": branch,
        "currentWorkingTreeSnapshot": True,
        "currentAuthority": AUTHORITY,
        "currentPendingGroup": {"group": GROUP, "spellIds": TARGETS, "count": len(TARGETS), "alreadyAcceptedAppliedIds": PREVIOUS_ACCEPTED},
        "currentReviewTargets": [{"spellId": s, "currentIndexEntry": entries[s], "completeCurrentCatalogSourceAndAccess": spells[s], "status": "Pending at current 811/37/0 authority; only identity in this packet's review scope."} for s in TARGETS],
        "sourceBindings": refreshed,
        "sourceBindingRefresh": {"sourceFiles": len(refreshed), "changedFromReturn218Packet": changed, "allSourcesReadFromCurrentWorktree": True, "currentIndexBinding": file_bind(index_path), "currentCatalogBinding": file_bind(catalog_path)},
        "candidateBindingReconciliation": candidate_reconciliation,
        "currentAuthorityEvidence": {"index": file_bind(index_path), "catalog": file_bind(catalog_path), "accessRegistry": file_bind(access_path), "workQueue": file_bind(work_queue_path), "queue": file_bind(qpath), "handoff": file_bind(hpath), "pendingIdentityAudit": file_bind(ppath), "return235Audit": file_bind(return235_audit)},
        "previousDefenseFormReturn": {"return": 218, "acceptedAppliedIds": PREVIOUS_ACCEPTED, "heldIds": TARGETS, "blockerIds": {"elemental-shell": ["DF218-B01", "DF218-B02"], "timeless-form": ["DF218-B03"], "invulnerable-sphere": ["DF218-B04"]}, "independentAudit": file_bind(prior_audit)},
        "priorHeldIdentitiesNotReopened": ["psychic-scream", "mass-phantom-killer", "weird", "final-word"],
        "newRuleAdoptions": 0,
    })

    source_search_leads = {
        "id": "DEFENSEFORM8-236-CURRENT-SOURCE-LEADS",
        "authority": AUTHORITY,
        "scopeIds": TARGETS,
        "leadsAreNotFindings": True,
        "leads": [
            {"source": "catalog.json", "pointer": "/spells (id=faction-portal)/operational", "lead": "Faction Portal currently defines one-way transit to a specific known same- or other-plane faction headquarters and rechecks exact teleport/planar blockers at crossing. Reassess whether an actually lawful exact route and current actor are source-established against Invulnerable Sphere; do not infer that a source exists just from the procedure."},
            {"source": "catalog.json", "pointer": "/spells (id=summon-spectral-steed)/operational", "lead": "Spectral Steed has one commanded planar crossing attempt to a specific known other-plane site, but is a noncombat mount with no damaging Action. Assess it only if it meets the exact blocked branch; do not treat its name as a valid companion attacker."},
            {"source": "catalog.json", "pointer": "/spells (id=time-stop)/operational", "lead": "Current card remains blocked-pending-operational-review with operational=null. Check the complete current bound sources for any later accepted operational Time Stop interface; class access alone is not a positive source."},
            {"source": "catalog.json", "pointer": "/spells (id=volcanic-cage or deep-crust-spike)/operational", "lead": "Both are blocked-pending-operational-review with operational=null. Their printed descriptions are not automatically an instantiated noncreature environmental damage source."},
            {"source": "catalog.json", "pointer": "/spells (id=dominate-beast)/operational", "lead": "Current Dominate Beast includes an owner-attached companion execution bridge. Reassess whether any complete current source actually instantiates the companion/proxy body, equipment, native attack, controller acquisition, command payment and attached phase required by DF218-B02."},
        ],
    }
    request = f"""REQUEST_236 — CURRENT-SOURCE REASSESSMENT OF THE THREE REMAINING DEFENSE/FORM IDENTITIES

Director: GPT in Calibration review part 6.
Current authority: 811 reviewed/applied, 37 pending, 0 accepted-unapplied; 535 complete standalone procedures; 173 scoped interfaces.
Exact scope: {', '.join(TARGETS)} only.

Return218 already accepted and Codex applied {', '.join(PREVIOUS_ACCEPTED)}. Do not revisit those, the 335-feat review, completed spell cohorts, or unrelated holds. The current pending authority audit, queue, handoff, index and catalog all bind the 811/37 state. The Defense/Form8 candidate now in the worktree is JSON-structurally identical to the queue-bound source-conference candidate; the byte/hash difference and exact equality are recorded in CANDIDATE_BINDING_RECONCILIATION_236.json. The original source-conference archive remains byte-exact to the queue binding. All 87 historical source paths are refreshed to current worktree bytes.

Reassess only the exact Return218 whole-identity blockers from the supplied current source snapshot and the byte-bound prior procedures/cases:
• elemental-shell: DF218-B01 (a source-established quantified noncreature elemental packet with geometry/type/damage/timing and bearer history) and DF218-B02 (an actually instantiated accessible companion/proxy with complete body/profile, equipment, native attack, controller acquisition, command payment and attached phase history).
• timeless-form: DF218-B03 (a currently operational, legally acquired Time Stop source with the actor, actual excluded permissions and native chronology; Time Stop's printed class access or pending card alone is insufficient).
• invulnerable-sphere: DF218-B04 (a lawful acquired planar crossing with a specific authorized destination, complete body/custody, and a valid attempted crossing against the actual closed partition).

The packet includes exact prior blocker assessments, procedures and every Return218 target case, each byte-verified against its original internal and external archive manifests; all 87 current source snapshots; the full current index, catalog, access registry, work queue and queue/handoff/pending snapshots; and Return235's audited held decision. Reconsider with the current evidence. Source-search leads are explicitly unqualified leads: Faction Portal may supply a real planar route if its actual actor/site/activation satisfy the gate; Spectral Steed has a planar attempt but no damaging Action; Time Stop, Volcanic Cage and Deep Crust Spike currently have no operational card; Dominate Beast's companion bridge still needs an actually instantiated source-qualified companion. Do not promote a lead into a witness by inference.

If any blocker can now be closed, cite exact current source paths, JSON pointers or passages, actor identity/lifecycle, legal activation and the precise case operations; author complete source-bound cases for all meaningful branches of that spell. Otherwise retain only the exact minimum missing evidence under its existing blocker ID and explain why the current source leads do not qualify. Do not invent a creature, hazard, access permission, plane/site, lawful cast or time-stop event.

Keep accepted=true/applied=false only for exact source-complete acceptances; acceptedIds/appliedIds/heldIds must reconcile per identity. Do not edit canonical files, apply changes, change GitHub, execute supplied programs, or claim runtime, implementation, human play, balance, cosmology, domain-closure, completion or release approval. Return the sealed decision ZIP, exact DELIVERY.json and the next pending group. The exact three targets are the entire scope.
"""

    files: dict[str, bytes] = {}
    for name, path, raw in [
        ("current/DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json", index_path, index_raw),
        ("current/DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json", catalog_path, catalog_raw),
        ("current/DescentReviewChanges/ReviewBible/data/director/spell_review/accepted_interface_registry_06.json", access_path, access_raw),
        ("current/DescentReviewChanges/ReviewBible/data/director/spell_review/remaining_work_queue_66.json", work_queue_path, work_queue_raw),
        ("current/" + qpath.relative_to(ROOT).as_posix(), qpath, qpath.read_bytes()),
        ("current/" + hpath.relative_to(ROOT).as_posix(), hpath, hpath.read_bytes()),
        ("current/" + ppath.relative_to(ROOT).as_posix(), ppath, ppath.read_bytes()),
        ("current/" + (BASE / "CURRENT_SPELL_REVIEW_SNAPSHOT_236.md").relative_to(ROOT).as_posix(), BASE / "CURRENT_SPELL_REVIEW_SNAPSHOT_236.md", (BASE / "CURRENT_SPELL_REVIEW_SNAPSHOT_236.md").read_bytes()),
    ]:
        add(files, name, raw)
    add(files, "current/CURRENT_AUTHORITY_236.json", enc({"authority": AUTHORITY, "targetIds": TARGETS, "acceptedIds": [], "appliedIds": [], "canonicalChanges": False}))
    add(files, "current/CURRENT_CANDIDATE_BINDING_RECONCILIATION_236.json", enc(candidate_reconciliation))
    add(files, "current/CURRENT_SOURCE_CONFERENCE_CANDIDATE_236.json", enc(candidate))
    add(files, "current/SOURCE_SEARCH_LEADS_236.json", enc(source_search_leads))
    add(files, "current/REQUEST_236.txt", request.encode("utf-8"))
    add(files, "current/RETURN235_DELIVERY.json", return235_delivery.read_bytes())
    add(files, "current/RETURN235_INDEPENDENT_AUDIT.json", return235_audit.read_bytes())
    add(files, "current/RETURN235_RECEIPT.json", return235_receipt.read_bytes())
    for out_name, raw in source_files.items():
        add(files, out_name, raw)

    add(files, "history/Source_Conference_01.zip", source_archive_path.read_bytes())
    add(files, "history/Candidate_Source_Conference_01.json", conference_candidate_raw)
    add(files, "history/Return218_DELIVERY.json", prior_delivery.read_bytes())
    add(files, "history/Return218_INDEPENDENT_AUDIT.json", prior_audit.read_bytes())
    add(files, "history/Return218_EXCERPT_BINDINGS_236.json", enc(excerpts_manifest))
    for out_name, raw in history_files.items():
        add(files, out_name, raw)
    for original_name, path in [
        ("Return186_INDEPENDENT_AUDIT.json", BASE / "RANK9_DEFENSEFORM8_RETURN186_INDEPENDENT_AUDIT.json"),
        ("Return186_DIRECTOR_DECISION.json", BASE / "RANK9_DEFENSEFORM8_DIRECTOR_DECISION_186.json"),
        ("Return186_EXACT_ACCEPTANCE.json", BASE / "RANK9_DEFENSEFORM8_EXACT_ACCEPTANCE_186.json"),
        ("Return186_APPLICATION_VALIDATION.json", BASE / "RANK9_DEFENSEFORM8_APPLICATION_VALIDATION_186.json"),
    ]:
        add(files, "history/" + original_name, path.read_bytes())

    OUT.mkdir(parents=True, exist_ok=True)
    member_rows = [{"path": path, "bytes": len(raw), "sha256": sha(raw), "crc32": crc(raw)} for path, raw in sorted(files.items())]
    manifest = {"id": "RANK9-DEFENSEFORM8-CURRENT-SOURCE-PACKET-MANIFEST-236", "sourceCommit": commit, "sourceAuthority": AUTHORITY, "targetGroup": GROUP, "targetPendingIds": TARGETS, "memberCountExcludingSelf": len(member_rows), "members": member_rows}
    manifest_raw = enc(manifest)
    with zipfile.ZipFile(PACKET, "w", zipfile.ZIP_DEFLATED, compresslevel=6) as z:
        for name, raw in sorted(files.items()):
            z.writestr(name, raw)
        z.writestr("MEMBER_MANIFEST.json", manifest_raw)
    with zipfile.ZipFile(PACKET) as z:
        names = z.namelist()
        assert z.testzip() is None and len(names) == len(set(names)) and set(names) == set(files) | {"MEMBER_MANIFEST.json"}
        assert json.loads(z.read("MEMBER_MANIFEST.json")) == manifest
        for row in member_rows:
            raw = z.read(row["path"])
            assert (len(raw), sha(raw), crc(raw)) == (row["bytes"], row["sha256"], row["crc32"]), row["path"]

    archive_raw = PACKET.read_bytes()
    delivery_obj = {
        "id": "RANK9-DEFENSEFORM8-CURRENT-SOURCE-236-DELIVERY",
        "createdAtUtc": now,
        "group": GROUP,
        "targetIds": TARGETS,
        "authority": AUTHORITY,
        "archive": {"fileName": PACKET.name, **bind(PACKET.name, archive_raw)},
        "sourceBindings": refreshed,
        "memberCount": len(files) + 1,
        "payloadCount": len(files),
        "memberManifest": {"path": "MEMBER_MANIFEST.json", "bytes": len(manifest_raw), "sha256": sha(manifest_raw), "crc32": crc(manifest_raw)},
        "members": member_rows + [{"path": "MEMBER_MANIFEST.json", "bytes": len(manifest_raw), "sha256": sha(manifest_raw), "crc32": crc(manifest_raw)}],
        "exactAllowlist": sorted([*files.keys(), "MEMBER_MANIFEST.json"]),
        "candidateBindingReconciliation": candidate_reconciliation,
        "previousReturnExcerptCount": len(excerpts),
        "currentSourceBindingCount": len(refreshed),
        "sourceProgramsExecuted": False,
        "runtimeExecuted": False,
        "canonicalChanges": False,
        "githubChanges": False,
        "notes": "Fresh current-authority review of only three pending Defense/Form8 identities; GPT is director. Prior accepted identities remain closed.",
    }
    DELIVERY.write_bytes(enc(delivery_obj))

    checks = [
        {"check": "Current queue, handoff, pending identity audit and authored index agree on 811/37/0", "passed": q["currentAuthority"] == h["currentAuthority"] == p["authority"] == AUTHORITY and p["pendingCount"] == 37 and index["authoredCounts"] == {"reviewed": 811, "pending": 37}},
        {"check": "Exact three pending targets remain non-operational and the two prior acceptances are applied/closed", "passed": all(entries[s]["authoredStatus"] == "pending-authored-procedure" and spells[s].get("operational") is None for s in TARGETS) and all(entries[s]["authoredStatus"] == "reviewed-authored-operational-playtest" for s in PREVIOUS_ACCEPTED)},
        {"check": "Queue-bound archive is byte-exact and current worktree candidate is structurally identical", "passed": sha(historical_candidate_raw) == queue_group["archive"]["sha256"] and candidate_reconciliation["jsonStructuralEquality"] and current_candidate == conference_candidate},
        {"check": "All 87 historical source paths refresh to current worktree bytes", "passed": len(refreshed) == 87 and all((ROOT / PurePosixPath(row["path"])).read_bytes() == source_files["sources_current/" + row["path"]] for row in refreshed)},
        {"check": "Return218 history excerpts match internal and external bindings (manifest remains self-excluding)", "passed": bool(excerpts) and len(target_cases) > 15 and all(row["originalPath"] in old_external_members and (row["originalPath"] in prior_internal_members or row["originalPath"] == "MEMBER_MANIFEST.json") for row in excerpts)},
        {"check": "Packet has exact current target scope and source lead qualifications", "passed": candidate["currentPendingGroup"]["spellIds"] == TARGETS and source_search_leads["leadsAreNotFindings"] is True and len(source_search_leads["leads"]) == 5},
        {"check": "Saved packet CRC scan and internal manifest cover every unique safe member", "passed": len(names) == len(files) + 1 and len(set(names)) == len(names) and all(safe(name) for name in names)},
        {"check": "Outer archive and external delivery exactly bind packet members and authority", "passed": delivery_obj["authority"] == AUTHORITY and delivery_obj["memberCount"] == len(names) and delivery_obj["exactAllowlist"] == sorted(names) and delivery_obj["archive"]["sha256"] == sha(archive_raw)},
    ]
    assert all(row["passed"] for row in checks), checks

    prep = {"id": "RANK9-DEFENSEFORM8-SOURCE-PREPARATION-236", "recordedAtUtc": now, "status": "CURRENT_SOURCE_PACKET_PREPARED_UNSENT_811_37_0", "sourceCommit": commit, "sourceBranch": branch, "sourceAuthority": AUTHORITY, "group": GROUP, "pendingIds": TARGETS, "previousAcceptedAppliedIds": PREVIOUS_ACCEPTED, "currentSourceFileCount": len(refreshed), "changedFromReturn218Packet": changed, "candidateBindingReconciliation": candidate_reconciliation, "historyExcerptCount": len(excerpts), "targetCaseCountFromReturn218": len(target_cases), "packet": {"path": PACKET.relative_to(ROOT).as_posix(), **bind(PACKET.name, archive_raw)}, "deliveryManifest": file_bind(DELIVERY), "memberCount": len(names), "checksPassed": len(checks), "checksFailed": 0, "checks": checks, "canonicalChanges": False, "githubChanges": False}
    PREP.write_bytes(enc(prep))
    packet_record = {"id": "RANK9-DEFENSEFORM8-PACKET-236", "status": "PREPARED_UNSENT", "group": GROUP, "pendingIds": TARGETS, "sourceAuthority": AUTHORITY, "packet": prep["packet"], "deliveryManifest": file_bind(DELIVERY), "preparation": file_bind(PREP), "conversation": CHAT, "checksPassed": len(checks), "checksFailed": 0}
    PACKET_RECORD.write_bytes(enc(packet_record))

    q_after = copy.deepcopy(q)
    group_after = next(row for row in q_after["currentPendingGroups"] if row["group"] == GROUP)
    group_after.update({"status": "CURRENT_SOURCE_PACKET_236_PREPARED_UNSENT_AT_811_37_0", "preparedPacket": prep["packet"], "deliveryManifest": file_bind(DELIVERY), "packetRecord": file_bind(PACKET_RECORD), "preparation": file_bind(PREP), "freshPacketRequiredForCurrentAuthority": True})
    next_record = {"group": GROUP, "pendingIds": TARGETS, "pendingCount": len(TARGETS), "status": "CURRENT_SOURCE_PACKET_236_PREPARED_UNSENT_AT_811_37_0", "freshPacketRequiredForCurrentAuthority": True, "preparedPacket": prep["packet"], "deliveryManifest": file_bind(DELIVERY), "packetRecord": file_bind(PACKET_RECORD), "preparation": file_bind(PREP)}
    q_after.update({"id": "SPELL-REVIEW-QUEUE-236", "recordedAtUtc": now, "nextGroup": GROUP, "next": next_record, "nextPreparedRequest": next_record, "currentPreparation": file_bind(PREP), "currentPacket": prep["packet"], "currentDeliveryManifest": file_bind(DELIVERY), "packetStatus": "RANK9_DEFENSEFORM8_SOURCE_PACKET_236_PREPARED_UNSENT_811_37", "status": "RANK9_DEFENSEFORM8_SOURCE_PACKET_236_PREPARED_UNSENT_811_37"})
    qpath.write_bytes(enc(q_after))
    q_bind = file_bind(qpath)
    h_after = copy.deepcopy(h)
    h_after.update({"id": "CURRENT-HANDOFF-236", "recordedAtUtc": now, "status": "RANK9_DEFENSEFORM8_CURRENT_SOURCE_PACKET_PREPARED_UNSENT_811_37", "queue": q_bind, "currentQueueBinding": q_bind, "currentPacket": prep["packet"], "currentPacketDelivery": file_bind(DELIVERY), "currentPreparation": file_bind(PREP), "nextGroup": GROUP, "nextPendingIds": TARGETS, "nextPendingCount": len(TARGETS), "nextStep": "Send the fresh Packet236 to GPT, keep monitoring the browser and ping if needed; independently audit its sealed decision and apply only exact accepted identities.", "resumePriority": "Packet236 is prepared for exactly elemental-shell, timeless-form and invulnerable-sphere. GPT is the director; monitor, ping as needed, then independently audit before applying any exact acceptance."})
    hpath.write_bytes(enc(h_after))
    print(json.dumps({"status": prep["status"], "authority": AUTHORITY, "targets": TARGETS, "currentSources": len(refreshed), "sourceChangesSinceReturn218": len(changed), "previousReturnCaseExcerpts": len(excerpts), "targetCases": len(target_cases), "packet": prep["packet"], "deliveryManifest": prep["deliveryManifest"], "checksPassed": len(checks), "checksFailed": 0}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
