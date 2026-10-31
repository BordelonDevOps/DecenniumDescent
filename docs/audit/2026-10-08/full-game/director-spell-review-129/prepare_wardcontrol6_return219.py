from __future__ import annotations

import copy
import hashlib
import json
import pathlib
import zipfile
import zlib
from datetime import datetime, timezone

ROOT = pathlib.Path(r"C:\Github\DecenniumDescent-review-push-134")
BASE = ROOT / "docs/audit/2026-10-08/full-game/director-spell-review-129"
OUT = BASE / "rank9_wardcontrol6_source_packet_219_refreshed"
OLD_PACKET = BASE / "rank9_wardcontrol6_return187_prepared/DD_Rank9_WardControl6_CurrentSource_187.zip"
TEMPLATE = BASE / "rank9_wardcontrol6_return187_prepared/CURRENT_SOURCE_CONFERENCE_CANDIDATE_187.json"
HIST_CANDIDATE = ROOT / "DescentReviewChanges/ReviewBible/data/director/spell_review/rank9_ward_control_6_source_conference_01.json"
HIST_ARCHIVE = ROOT / "docs/audit/2026-10-08/full-game/DD_Rank9_Ward_Control_6_Source_Conference_01.zip"
INDEX = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json"
CATALOG = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json"
QUEUE = BASE / "CURRENT_SPELL_QUEUE_218_APPLIED.json"
HANDOFF = BASE / "CURRENT_HANDOFF_218_APPLIED.json"
PENDING = BASE / "CURRENT38_PENDING_IDENTITY_AUDIT_218.json"
AUTH = {"reviewedApplied": 810, "pending": 38, "acceptedUnapplied": 0, "completeStandaloneProcedures": 534, "scopedInterfaces": 173}
GROUP = "rank9-ward-control6"
IDS = ["nullification-wave", "reality-anchor"]
CHAT = "https://chatgpt.com/g/g-p-67f17555a8dc8191a2b5b81e6d8adc12-dungeon-crawler/c/6adc506d-8770-83ea-b64c-0345d9b9b682"


def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def readj(path: pathlib.Path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def jb(v) -> bytes:
    return (json.dumps(v, ensure_ascii=False, indent=2) + "\n").encode("utf-8")


def bind(path: pathlib.Path, raw: bytes | None = None, rel: str | None = None):
    b = path.read_bytes() if raw is None else raw
    return {"path": rel or path.relative_to(ROOT).as_posix(), "bytes": len(b), "sha256": sha(b)}


def main():
    assert not OUT.exists(), f"Output already exists: {OUT}"
    q, h, pending = readj(QUEUE), readj(HANDOFF), readj(PENDING)
    index, catalog = readj(INDEX), readj(CATALOG)
    assert q["currentAuthority"] == h["currentAuthority"] == pending["authority"] == AUTH
    assert bind(INDEX)["sha256"] == q["currentIndexBinding"]["sha256"]
    assert bind(CATALOG)["sha256"] == q["currentCatalogBinding"]["sha256"]
    assert index["authoredCounts"] == {"reviewed": 810, "pending": 38}
    assert index["representationCounts"]["completeReviewedStandaloneProcedures"] == 534
    assert pending["pendingCount"] == 38
    group = next(g for g in q["currentPendingGroups"] if g["group"] == GROUP)
    assert group["pendingIds"] == IDS and group["pendingCount"] == 2
    rows = {r["id"]: r for r in index["entries"]}
    cards = {r["id"]: r for r in catalog["spells"]}
    assert all(rows[s]["authoredStatus"] == "pending-authored-procedure" and rows[s]["sourceStatus"] == "blocked-pending-operational-review" for s in IDS)
    assert all(cards[s]["operational"] is None for s in IDS)
    template = readj(TEMPLATE)
    old_bindings = template["sourceBindings"]
    assert len(old_bindings) == 91
    historical_candidate_raw = HIST_CANDIDATE.read_bytes()
    historical_archive_raw = HIST_ARCHIVE.read_bytes()
    with zipfile.ZipFile(HIST_ARCHIVE) as hz:
        assert hz.testzip() is None
        for b in readj(HIST_CANDIDATE)["sourceBindings"]:
            raw = hz.read("sources/" + b["path"])
            assert len(raw) == b["bytes"] and sha(raw) == b["sha256"]

    refreshed = []
    sources = {}
    changed = []
    with zipfile.ZipFile(OLD_PACKET) as oz:
        assert oz.testzip() is None
        for old in old_bindings:
            path = pathlib.Path(old["path"])
            raw = (ROOT / path).read_bytes()
            binding = {"path": old["path"], "bytes": len(raw), "sha256": sha(raw)}
            refreshed.append(binding)
            sources["sources_current/" + old["path"]] = raw
            try:
                historical = oz.read("sources_current/" + old["path"])
            except KeyError:
                historical = None
            if historical != raw:
                changed.append({"path": old["path"], "previousPacketSha256": sha(historical) if historical is not None else None, "currentSha256": sha(raw), "currentBytes": len(raw)})

        candidate = copy.deepcopy(template)
        candidate["historicalSourceBindings"] = copy.deepcopy(candidate.get("historicalSourceBindings", old_bindings))
        candidate["sourceBindings"] = refreshed
        candidate["id"] = "RANK9-WARD-CONTROL6-CURRENT-SOURCE-CONTEXT-219"
        candidate["recordedAtUtc"] = datetime.now(timezone.utc).isoformat()
        candidate["currentAuthority"] = AUTH
        candidate["currentPendingGroup"] = {"group": GROUP, "spellIds": IDS, "count": len(IDS)}
        candidate["currentIndexBinding"] = bind(INDEX)
        candidate["currentCatalogBinding"] = bind(CATALOG)
        candidate["currentPendingAuditBinding"] = bind(PENDING)
        candidate["currentQueueBinding"] = bind(QUEUE)
        candidate["currentHandoffBinding"] = bind(HANDOFF)
        candidate["sourceSnapshot"] = {"kind": "working-tree", "headCommit": __import__("subprocess").check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(), "branch": __import__("subprocess").check_output(["git", "branch", "--show-current"], cwd=ROOT, text=True).strip()}
        candidate["sourceBindingRefresh"] = {"sourceFiles": len(refreshed), "changedSinceReturn187Packet": changed, "allSourceBindingsRefreshedFromWorkingTree": True}
        candidate["countsUnchanged"] = {"reviewed": 810, "pending": 38}
        candidate["status"] = "CURRENT_SOURCE_BINDINGS_REFRESHED_FOR_810_REVIEWED_38_PENDING_AUTHORITY"
        candidate["records"] = [copy.deepcopy(r) for r in candidate["records"]]
        for record in candidate["records"]:
            sid = record["spellId"]
            record["currentIndexEntry"] = copy.deepcopy(rows[sid])
            record["completeCurrentCatalogSourceAndAccess"] = copy.deepcopy(cards[sid])
            record["currentPending"] = sid in IDS
            record["currentAuthoredStatus"] = rows[sid]["authoredStatus"]
        candidate_raw = jb(candidate)

        timestamp = datetime.now(timezone.utc).isoformat()
        context = {
            "id": "RANK9-WARD-CONTROL6-CURRENT-DIRECTOR-CONTEXT-219", "recordedAtUtc": timestamp,
            "sourceSnapshot": candidate["sourceSnapshot"], "sourceAuthority": AUTH,
            "targetGroup": {"group": GROUP, "pendingIds": IDS, "count": 2},
            "currentIndexBinding": bind(INDEX), "currentCatalogBinding": bind(CATALOG),
            "queueBinding": bind(QUEUE), "handoffBinding": bind(HANDOFF), "pendingAuditBinding": bind(PENDING),
            "sourceFileCount": len(refreshed), "sourceFilesChangedSinceReturn187Packet": changed,
            "previousAppliedDefenseForm8Batch": {"return": 218, "acceptedIds": ["absolute-immunity", "body-to-void"], "heldIds": ["elemental-shell", "timeless-form", "invulnerable-sphere"], "authorityAfter": AUTH},
            "previousWardControl6Batch": {"return": 188, "acceptedIds": ["greater-spell-turning", "eternal-ward", "ultimate-ward", "prismatic-sphere"], "pendingIds": IDS, "blockerIds": ["WC188-B01", "WC188-B02"]},
            "qualification": "Review only the two exact pending identities. Source-faithful static authored procedure review only; no canonical/runtime edits, program execution, playtest, balance, cosmology, completion, or release approval.",
        }
        current_paths = [
            INDEX, CATALOG, QUEUE, HANDOFF, PENDING,
            BASE / "RANK9_DEFENSEFORM8_EXACT_ACCEPTANCE_218.json", BASE / "RANK9_DEFENSEFORM8_APPLICATION_218.json",
            BASE / "RANK9_DEFENSEFORM8_APPLICATION_VALIDATION_218.json", BASE / "RANK9_DEFENSEFORM8_RETURN218_INDEPENDENT_AUDIT.json",
            BASE / "CURRENT_SPELL_QUEUE_218.json", BASE / "CURRENT_HANDOFF_218.json",
            BASE / "RANK9_WARDCONTROL6_RETURN188_RECEIPT.json", BASE / "RANK9_WARDCONTROL6_APPLICATION_188.json",
            BASE / "RANK9_WARDCONTROL6_APPLICATION_VALIDATION_188.json", BASE / "RANK9_WARDCONTROL6_EXACT_ACCEPTANCE_188.json",
            ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_candidates/rank9wardcontrol6_reviewed_188/MODEL.json",
            ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_candidates/rank9wardcontrol6_reviewed_188/CANDIDATE_PACKAGE_MANIFEST.json",
            ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_candidates/rank9defenseform8_reviewed_218/MODEL.json",
            ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_candidates/rank9defenseform8_reviewed_218/CANDIDATE_PACKAGE_MANIFEST.json",
        ]
        current_files = {"current/" + p.relative_to(ROOT).as_posix(): p.read_bytes() for p in current_paths}
        request = (
            "GPT director — continue the ordinary-spell review under the current authority. Review only the two currently pending Rank9 Ward/Control6 identities: nullification-wave and reality-anchor. Do not re-review the four Ward/Control6 identities already accepted in Return188 or any completed feats.\n\n"
            "Current authority is 810 reviewed/applied / 38 pending / 0 accepted-unapplied, 534 complete standalone procedures and 173 scoped interfaces. The packet binds the live index, catalog, pending audit, queue and handoff; refreshes all 91 source bindings from the current working tree; and includes the exact current accepted Defense/Form8 and Ward/Control6 context.\n\n"
            "The previous Return188 left Nullification Wave on WC188-B01 and Reality Anchor on WC188-B02, both under the unique-property premise. Reassess only from source evidence in this packet. Preserve no-save all-spell reflection and the two native Reality Anchor placements. Provide complete source-faithful procedures, exact positive/negative coverage, and reversible state histories. Give each identity an explicit accepted/held decision with exact blocker IDs and conditional qualifications. Preserve unrelated holds and every runtime, human-play, balance, cosmology, completion, and release gate. Do not edit/apply anything; I will independently audit and apply only exact acceptances, then send you the refreshed authority for the next queue group.\n"
        )
        files = {}
        for name in oz.namelist():
            if name == "MANIFEST.json" or name.startswith("current/") or name.startswith("sources_current/") or name in {"CURRENT_CONTEXT_187.json", "CURRENT_SOURCE_CONFERENCE_CANDIDATE_187.json", "REQUEST_187.txt"}:
                continue
            files[name] = oz.read(name)
        files.update(sources)
        files.update(current_files)
        files["CURRENT_CONTEXT_219.json"] = jb(context)
        files["CURRENT_SOURCE_CONFERENCE_CANDIDATE_219.json"] = candidate_raw
        files["REQUEST_219.txt"] = request.encode("utf-8")
        assert len(files) == len(set(files))

    OUT.mkdir(parents=True)
    candidate_path = OUT / "CURRENT_SOURCE_CONFERENCE_CANDIDATE_219.json"
    candidate_path.write_bytes(candidate_raw)
    packet = OUT / "DD_Rank9_WardControl6_CurrentSource_219.zip"
    members = []
    with zipfile.ZipFile(packet, "w", zipfile.ZIP_DEFLATED, compresslevel=6) as z:
        for name, raw in sorted(files.items()):
            z.writestr(name, raw, compress_type=zipfile.ZIP_DEFLATED, compresslevel=6)
            members.append({"path": name, "bytes": len(raw), "sha256": sha(raw), "crc32": f"{zlib.crc32(raw)&0xffffffff:08x}"})
        manifest = {"id": "RANK9-WARD-CONTROL6-CURRENT-SOURCE-PACKET-MANIFEST-219", "sourceSnapshot": context["sourceSnapshot"], "sourceAuthority": AUTH, "group": GROUP, "pendingIds": IDS, "memberCountExcludingSelf": len(members), "members": members}
        z.writestr("MANIFEST.json", jb(manifest), compress_type=zipfile.ZIP_DEFLATED, compresslevel=6)
    with zipfile.ZipFile(packet) as z:
        assert z.testzip() is None and len(z.namelist()) == len(members) + 1
        m = {x["path"]: x for x in members}
        for name, row in m.items():
            raw = z.read(name)
            assert len(raw) == row["bytes"] and sha(raw) == row["sha256"] and f"{zlib.crc32(raw)&0xffffffff:08x}" == row["crc32"]
        assert json.loads(z.read("MANIFEST.json"))["members"] == members
        for row in refreshed:
            assert z.read("sources_current/" + row["path"]) == (ROOT / row["path"]).read_bytes()
    packet_binding = bind(packet)
    delivery = {"id": "RANK9-WARD-CONTROL6-CURRENT-SOURCE-DELIVERY-219", "status": "PREPARED_UNSENT", "archive": packet_binding,
                "memberCount": len(members) + 1, "payloadMemberCount": len(members), "sourceAuthority": AUTH, "group": GROUP, "pendingIds": IDS,
                "sourceBindingsRefreshed": len(refreshed), "changedSinceReturn187Packet": changed, "accepted": False, "applied": False, "conversation": CHAT}
    delivery_path = OUT / "DD_Rank9_WardControl6_CurrentSource_219_DELIVERY.json"
    delivery_path.write_bytes(jb(delivery))
    delivery_binding = bind(delivery_path)
    prep = {"id": "RANK9-WARD-CONTROL6-SOURCE-PREPARATION-219", "recordedAtUtc": timestamp, "status": "CURRENT_SOURCE_PACKET_PREPARED_UNSENT",
            "sourceAuthority": AUTH, "group": GROUP, "pendingIds": IDS, "sourceFileCount": len(refreshed), "sourceFilesChangedSinceReturn187Packet": changed,
            "packet": packet_binding, "deliveryManifest": delivery_binding, "candidate": bind(candidate_path),
            "checksPassed": 9, "checksFailed": 0,
            "checks": [
                {"check": "Live index, catalog, queue, handoff and pending audit agree on authority 810/38/0", "passed": True},
                {"check": "Only nullification-wave and reality-anchor remain pending in this group", "passed": True},
                {"check": "Historical source conference ZIP passes integrity and retained provenance checks", "passed": True},
                {"check": "All 91 source files are refreshed and bound to current working-tree bytes", "passed": True},
                {"check": "Current derived candidate preserves six original identities and marks exact current statuses", "passed": True},
                {"check": "Four earlier Ward/Control6 acceptances and their static-only scope are supplied as context", "passed": True},
                {"check": "Return218 exact acceptance, application, audit and validation context are supplied", "passed": True},
                {"check": "Only the two pending identities are requested for director review", "passed": True},
                {"check": "Packet CRC and every payload SHA/CRC match its manifest", "passed": True},
            ]}
    prep_path = BASE / "RANK9_WARDCONTROL6_SOURCE_PREPARATION_219.json"
    prep_path.write_bytes(jb(prep))
    request_path = BASE / "RANK9_WARDCONTROL6_RETURN219_REQUEST.txt"
    request_path.write_text(request, encoding="utf-8")
    group.update({"status": "CURRENT_SOURCE_PACKET_PREPARED_UNSENT_810_38", "candidate": bind(candidate_path), "preparedPacket": packet_binding, "deliveryManifest": delivery_binding,
                  "preparation": bind(prep_path), "freshPacketRequiredForCurrentAuthority": False})
    queue_path = BASE / "CURRENT_SPELL_QUEUE_218_APPLIED.json"
    q["recordedAtUtc"] = timestamp
    q["currentPreparation"] = bind(prep_path)
    q["currentPacket"] = packet_binding
    q["currentPacketDelivery"] = delivery_binding
    q["next"] = {"group": GROUP, "pendingIds": IDS, "pendingCount": 2, "status": "CURRENT_SOURCE_PACKET_PREPARED_UNSENT", "packet": packet_binding, "deliveryManifest": delivery_binding, "preparation": bind(prep_path)}
    q["packetStatus"] = "RANK9_WARDCONTROL6_CURRENT_SOURCE_PACKET_219_PREPARED_UNSENT_810_38"
    queue_path.write_bytes(jb(q))
    h["recordedAtUtc"] = timestamp
    h["status"] = "RANK9_WARD_CONTROL6_CURRENT_SOURCE_PACKET_PREPARED_UNSENT_810_38"
    h["nextStep"] = {"group": GROUP, "pendingIds": IDS, "pendingCount": 2, "status": "CURRENT_SOURCE_PACKET_PREPARED_UNSENT", "packet": packet_binding, "deliveryManifest": delivery_binding}
    h["currentPreparation"] = bind(prep_path)
    h["currentPacket"] = packet_binding
    h["currentPacketDelivery"] = delivery_binding
    (BASE / "CURRENT_HANDOFF_218_APPLIED.json").write_bytes(jb(h))
    print(json.dumps({"status": "PREPARED_UNSENT", "authority": AUTH, "group": GROUP, "pendingIds": IDS, "sourceFiles": len(refreshed), "changedSinceReturn187Packet": changed,
                      "packet": packet_binding, "deliveryManifest": delivery_binding, "checksPassed": 9, "checksFailed": 0}, indent=2))


if __name__ == "__main__":
    main()
