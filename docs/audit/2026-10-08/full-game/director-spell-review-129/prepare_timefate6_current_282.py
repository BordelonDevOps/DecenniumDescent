from __future__ import annotations

import copy
import hashlib
import json
import zipfile
import zlib
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[5]
BASE = ROOT / "docs/audit/2026-10-08/full-game/director-spell-review-129"
OUT = BASE / "rank9_timefate6_current_source_282_prepared"
AUTH = {"reviewedApplied": 816, "pending": 32, "acceptedUnapplied": 0,
        "completeStandaloneProcedures": 540, "scopedInterfaces": 173}
GROUP = "rank9-time-fate6"
IDS = ["time-stop", "fate-rewrite", "collapse-timeline", "eternal-prophecy"]
CHAT = "https://chatgpt.com/g/g-p-67f17555a8dc8191a2b5b81e6d8adc12-dungeon-crawler/c/6adc506d-8770-83ea-b64c-0345d9b9b682"
QUEUE = BASE / "CURRENT_SPELL_QUEUE_282.json"
HANDOFF = BASE / "CURRENT_HANDOFF_282.json"
PENDING = BASE / "CURRENT32_PENDING_IDENTITY_AUDIT_282.json"
INDEX = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json"
CATALOG = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json"
OLD_PACKET = BASE / "rank9_timefate6_current_source_221_prepared/DD_Rank9_TimeFate6_CurrentSource_221.zip"
RETURN221_DIR = BASE / "rank9_timefate6_return221_received"
RETURN221 = RETURN221_DIR / "DD_Rank9_TimeFate4_Director_Return221_HELD.zip"
RETURN221_DELIVERY = RETURN221_DIR / "DD_Rank9_TimeFate4_Director_Return221_HELD_DELIVERY.json"
RETURN221_AUDIT = BASE / "RANK9_TIMEFATE6_RETURN221_INDEPENDENT_AUDIT.json"
RETURN221_RECEIPT = BASE / "RANK9_TIMEFATE6_RETURN221_RECEIPT.json"
RETURN281_DIR = BASE / "rank9_wardcontrol6_return281_received"
RETURN281 = RETURN281_DIR / "DD_Rank9_WardControl6_Director_Return281_HELD.zip"
RETURN281_DELIVERY = RETURN281_DIR / "DD_Rank9_WardControl6_Director_Return281_HELD_DELIVERY.json"
RETURN281_AUDIT = BASE / "RANK9_WARDCONTROL6_RETURN281_INDEPENDENT_AUDIT.json"
RETURN281_RECEIPT = BASE / "RANK9_WARDCONTROL6_RETURN281_RECEIPT.json"
PACKET281_DIR = BASE / "rank9_wardcontrol6_source_packet_281_refreshed"
PACKET281 = PACKET281_DIR / "DD_Rank9_WardControl6_CurrentSource_281.zip"
PACKET281_DELIVERY = PACKET281_DIR / "DD_Rank9_WardControl6_CurrentSource_281_DELIVERY.json"
PACKET281_AUDIT = BASE / "RANK9_WARDCONTROL6_PACKET281_INDEPENDENT_AUDIT.json"
PACKET281_RECEIPT = BASE / "RANK9_WARDCONTROL6_PACKET281_RECEIPT.json"


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def crc(raw: bytes) -> str:
    return f"{zlib.crc32(raw) & 0xffffffff:08x}"


def jb(value) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8")


def readj(path: Path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def bind(path: Path, raw: bytes | None = None) -> dict:
    data = path.read_bytes() if raw is None else raw
    return {"path": path.relative_to(ROOT).as_posix(), "bytes": len(data), "sha256": sha(data), "crc32": crc(data)}


def safe(name: str) -> bool:
    p = PurePosixPath(name)
    return bool(name) and "\\" not in name and not p.is_absolute() and all(x not in ("", ".", "..") and not x.startswith(".") for x in p.parts)


def main() -> None:
    assert not OUT.exists(), f"Output already exists: {OUT}"
    q0, h0, p0 = readj(QUEUE), readj(HANDOFF), readj(PENDING)
    index, catalog = readj(INDEX), readj(CATALOG)
    d281, a281, r281 = readj(RETURN281_DELIVERY), readj(RETURN281_AUDIT), readj(RETURN281_RECEIPT)
    d221, a221, r221 = readj(RETURN221_DELIVERY), readj(RETURN221_AUDIT), readj(RETURN221_RECEIPT)
    p281 = readj(PACKET281_DELIVERY)
    assert q0["currentAuthority"] == h0["currentAuthority"] == p0["authority"] == AUTH
    assert q0["nextGroup"] == h0["nextGroup"] == GROUP and q0["nextPendingIds"] == IDS
    assert p0["pendingCount"] == 32 and set(IDS) <= set(p0["pendingIds"])
    assert index["authoredCounts"] == {"reviewed": 816, "pending": 32}
    assert index["representationCounts"]["completeReviewedStandaloneProcedures"] == 540
    assert a281["status"] == r281["status"] == "PASS" and a281["checkCount"] == 17 and a281["failedChecks"] == 0
    assert d281["heldIds"] == ["nullification-wave", "reality-anchor"] and d281["acceptedIds"] == d281["appliedIds"] == []
    assert d281["nextPendingGroup"] == {"group": GROUP, "pendingIds": IDS}
    assert d221["heldIds"] == IDS and d221.get("acceptedIds", []) == d221.get("appliedIds", []) == [] and a221["status"].startswith("PASS")
    assert p281["sourceAuthority"] == AUTH and p281["pendingIds"] == ["nullification-wave", "reality-anchor"]

    ix = {row["id"]: row for row in index["entries"]}
    cat = {row["id"]: row for row in catalog["spells"]}
    for sid in IDS:
        assert ix[sid]["authoredStatus"] == "pending-authored-procedure"
        assert ix[sid]["sourceStatus"] == "blocked-pending-operational-review" and cat[sid].get("operational") is None
    for sid in ["time-fracture", "foresight-perfect"]:
        assert sid not in p0["pendingIds"]

    now = datetime.now(timezone.utc).isoformat()
    out: dict[str, bytes] = {}
    with zipfile.ZipFile(OLD_PACKET) as old:
        assert old.testzip() is None
        previous_candidate = json.loads(old.read("CURRENT_SOURCE_CONFERENCE_CANDIDATE_221.json"))
        source_rows = previous_candidate["sourceBindings"]
        assert len(source_rows) == 140
        changed, refreshed_rows = [], []
        for row in source_rows:
            path = row["path"]
            assert safe(path)
            raw = (ROOT / path).read_bytes()
            refreshed_rows.append({"path": path, "bytes": len(raw), "sha256": sha(raw)})
            out["sources_current/" + path] = raw
            previous = old.read("sources_current/" + path)
            if previous != raw:
                changed.append({"path": path, "previousPacketSha256": sha(previous), "currentSha256": sha(raw), "currentBytes": len(raw)})
        for name in old.namelist():
            if name.startswith("sources_current/") or name == "MANIFEST.json":
                continue
            out["history/packet221/" + name] = old.read(name)

    for prefix, pairs in [
        ("history/return221/", [("DD_Rank9_TimeFate4_Director_Return221_HELD.zip", RETURN221), ("DD_Rank9_TimeFate4_Director_Return221_HELD_DELIVERY.json", RETURN221_DELIVERY), ("INDEPENDENT_AUDIT.json", RETURN221_AUDIT), ("RECEIPT.json", RETURN221_RECEIPT)]),
        ("history/return281/", [("DD_Rank9_WardControl6_Director_Return281_HELD.zip", RETURN281), ("DD_Rank9_WardControl6_Director_Return281_HELD_DELIVERY.json", RETURN281_DELIVERY), ("INDEPENDENT_AUDIT.json", RETURN281_AUDIT), ("RECEIPT.json", RETURN281_RECEIPT)]),
        ("history/packet281/", [("DD_Rank9_WardControl6_CurrentSource_281.zip", PACKET281), ("DD_Rank9_WardControl6_CurrentSource_281_DELIVERY.json", PACKET281_DELIVERY), ("INDEPENDENT_AUDIT.json", PACKET281_AUDIT), ("RECEIPT.json", PACKET281_RECEIPT)]),
    ]:
        for name, path in pairs:
            out[prefix + name] = path.read_bytes()

    source_commit = __import__("subprocess").check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    branch = __import__("subprocess").check_output(["git", "branch", "--show-current"], cwd=ROOT, text=True).strip()
    assert branch == "main"
    snapshot = {"kind": "working-tree", "headCommit": source_commit, "branch": branch,
                "indexBinding": bind(INDEX), "catalogBinding": bind(CATALOG)}
    context = {
        "id": "TIMEFATE6-CURRENT-SOURCE-CONTEXT-282", "recordedAtUtc": now,
        "sourceAuthority": AUTH, "sourceSnapshot": snapshot, "group": GROUP, "pendingIds": IDS,
        "currentIndexBinding": bind(INDEX), "currentCatalogBinding": bind(CATALOG),
        "currentPendingAuditInput": bind(PENDING), "currentQueueInput": bind(QUEUE), "currentHandoffInput": bind(HANDOFF),
        "latestReturn281Archive": bind(RETURN281), "latestReturn281Delivery": bind(RETURN281_DELIVERY),
        "latestReturn281Audit": bind(RETURN281_AUDIT), "latestReturn281Receipt": bind(RETURN281_RECEIPT),
        "latestPacket281Archive": bind(PACKET281), "latestPacket281Delivery": bind(PACKET281_DELIVERY),
        "latestPacket281Audit": bind(PACKET281_AUDIT), "latestPacket281Receipt": bind(PACKET281_RECEIPT),
        "priorTimeFateReturn221Archive": bind(RETURN221), "priorTimeFateReturn221Delivery": bind(RETURN221_DELIVERY),
        "priorTimeFateReturn221Audit": bind(RETURN221_AUDIT), "priorTimeFateReturn221Receipt": bind(RETURN221_RECEIPT),
        "acceptedIds": [], "appliedIds": [],
        "previousBlockers": {"time-stop": ["TF192-B01"], "eternal-prophecy": ["TF192-B02"],
                              "fate-rewrite": ["TF192-B04"], "collapse-timeline": ["TF192-B05"]},
        "sourceBindingsRefreshed": len(refreshed_rows), "sourceBindingRefreshDiff": changed,
    }
    candidate = copy.deepcopy(previous_candidate)
    candidate.update({"id": "RANK9-TIME-FATE6-CURRENT-SOURCE-CONTEXT-282", "recordedAtUtc": now,
                      "status": "CURRENT_SOURCE_BINDINGS_REFRESHED_FOR_816_REVIEWED_32_PENDING_AUTHORITY",
                      "currentAuthority": AUTH, "currentPendingGroup": {"group": GROUP, "spellIds": IDS, "count": 4},
                      "currentIndexBinding": bind(INDEX), "currentCatalogBinding": bind(CATALOG),
                      "currentPendingAuditInputBinding": bind(PENDING), "currentQueueInputBinding": bind(QUEUE),
                      "currentHandoffInputBinding": bind(HANDOFF), "sourceSnapshot": snapshot,
                      "currentSourceCommit": source_commit, "currentBranch": branch,
                      "sourceBindings": refreshed_rows, "currentPendingIdSet": sorted(p0["pendingIds"]),
                      "sourceBindingRefresh": {"sourceFiles": len(refreshed_rows), "changedSinceTimeFateSourcePacket221": changed,
                                               "allSourceBindingsRefreshedFromWorkingTree": True},
                      "countsUnchanged": {"reviewed": 816, "pending": 32},
                      "priorTimeFateReturn221AuditBinding": bind(RETURN221_AUDIT),
                      "latestWardControlReturn281Binding": bind(RETURN281),
                      "latestWardControlReturn281AuditBinding": bind(RETURN281_AUDIT),
                      "latestWardControlPacket281Binding": bind(PACKET281),
                      "queueCandidateBinding": copy.deepcopy(next(row for row in q0["currentPendingGroups"] if row["group"] == GROUP))})
    request = (
        "GPT director — continue the ordinary-spell review at current authority 816 reviewed/applied / 32 pending / 0 accepted-unapplied, "
        "with 540 complete standalone procedures and 173 scoped interfaces. Review only the four pending Rank9 Time/Fate6 identities: "
        "time-stop, fate-rewrite, collapse-timeline, and eternal-prophecy. Do not re-review completed feats, time-fracture, foresight-perfect, "
        "other accepted spells, or any other pending cohort.\n\n"
        f"Current source snapshot: branch {branch}, HEAD {source_commit}. The refreshed packet binds current index/catalog, pending audit, queue and handoff; "
        "all 140 Time/Fate source bindings are refreshed from this working tree. Return281 and its PASS independent audit/receipt are included: "
        "nullification-wave and reality-anchor remain held under WC188-B01/B02, so the Director selected Time/Fate6 next without changing authority.\n\n"
        "The prior sealed Return221 independently retained TF192-B01 for time-stop, TF192-B04 for fate-rewrite, TF192-B05 for collapse-timeline, "
        "and TF192-B02 for eternal-prophecy. The complete Return221 archive, delivery manifest, independent audit and receipt are included with "
        "the earlier detailed evidence under history/packet221. Reassess only these four current pending identities against refreshed sources, "
        "close a blocker only with its exact source-grounded witness, and preserve conditional qualifications and unrelated holds.\n\n"
        "Return explicit accepted/held rulings for only the four requested IDs, exact blocker and qualification IDs, source-faithful procedures, "
        "reversible before/after traces, exact costs/deadlines/resource and custody histories, and a verifiable decision ZIP with a matching delivery manifest. "
        "Keep all acceptances unapplied; do not edit canonical files or execute supplied programs. Preserve runtime, implementation, human-play, balance, "
        "cosmology, domain-closure, completion and release gates. State minimum missing evidence per held identity and select the next group."
    )
    candidate_raw, context_raw, request_raw = jb(candidate), jb(context), (request + "\n").encode()
    out.update({"authority_current/authored_review_index.json": INDEX.read_bytes(),
                "authority_current/catalog.json": CATALOG.read_bytes(),
                "authority_current/CURRENT_SPELL_QUEUE_282_INPUT.json": QUEUE.read_bytes(),
                "authority_current/CURRENT_HANDOFF_282_INPUT.json": HANDOFF.read_bytes(),
                "authority_current/CURRENT32_PENDING_IDENTITY_AUDIT_282_INPUT.json": PENDING.read_bytes(),
                "CURRENT_SOURCE_CONFERENCE_CANDIDATE_282.json": candidate_raw,
                "CURRENT_CONTEXT_282.json": context_raw, "REQUEST_282.txt": request_raw})
    assert len(out) == len(set(out)) and all(safe(name) for name in out)
    rows = [{"path": name, "bytes": len(raw), "sha256": sha(raw), "crc32": crc(raw)} for name, raw in sorted(out.items())]
    manifest = {"id": "RANK9-TIME-FATE6-CURRENT-SOURCE-PACKET-MANIFEST-282", "sourceSnapshot": snapshot,
                "sourceAuthority": AUTH, "group": GROUP, "pendingIds": IDS,
                "payloadMemberCount": len(rows), "members": rows}
    OUT.mkdir(parents=True)
    packet = OUT / "DD_Rank9_TimeFate6_CurrentSource_282.zip"
    with zipfile.ZipFile(packet, "w", zipfile.ZIP_DEFLATED, compresslevel=6) as z:
        for name, raw in sorted(out.items()):
            z.writestr(name, raw)
        z.writestr("MANIFEST.json", jb(manifest))
    with zipfile.ZipFile(packet) as z:
        assert z.testzip() is None and len(z.namelist()) == len(rows) + 1
        for row in rows:
            raw = z.read(row["path"])
            assert len(raw) == row["bytes"] and sha(raw) == row["sha256"] and crc(raw) == row["crc32"]
    packet_binding = bind(packet)

    candidate_path = OUT / "CURRENT_SOURCE_CONFERENCE_CANDIDATE_282.json"; candidate_path.write_bytes(candidate_raw)
    context_path = OUT / "CURRENT_CONTEXT_282.json"; context_path.write_bytes(context_raw)
    request_path = OUT / "REQUEST_282.txt"; request_path.write_bytes(request_raw)
    delivery_path = OUT / "DD_Rank9_TimeFate6_CurrentSource_282_DELIVERY.json"
    delivery = {"id": "RANK9-TIME-FATE6-CURRENT-SOURCE-DELIVERY-282", "status": "PREPARED_UNSENT",
                "archive": packet_binding, "memberCount": len(rows) + 1, "payloadMemberCount": len(rows),
                "sourceSnapshot": snapshot, "sourceAuthority": AUTH, "group": GROUP, "pendingIds": IDS,
                "candidate": bind(candidate_path), "sourceFilesRefreshed": len(refreshed_rows),
                "sourceFilesChangedSinceTimeFateSourcePacket221": changed,
                "accepted": False, "applied": False, "conversation": CHAT}
    delivery_path.write_bytes(jb(delivery)); delivery_binding = bind(delivery_path)

    preparation_path = BASE / "RANK9_TIMEFATE6_SOURCE_PREPARATION_282.json"
    preparation = {"id": "RANK9-TIMEFATE6-SOURCE-PREPARATION-282", "recordedAtUtc": now,
                   "status": "CURRENT_SOURCE_PACKET_PREPARED_UNSENT", "sourceAuthority": AUTH,
                   "sourceSnapshot": snapshot, "group": GROUP, "pendingIds": IDS,
                   "priorTimeFateReturn221": bind(RETURN221), "priorTimeFateReturn221Audit": bind(RETURN221_AUDIT),
                   "latestWardControlReturn281": bind(RETURN281), "latestWardControlReturn281Audit": bind(RETURN281_AUDIT),
                   "latestWardControlPacket281": bind(PACKET281), "latestWardControlPacket281Audit": bind(PACKET281_AUDIT),
                   "sourceFilesRefreshed": len(refreshed_rows), "changedSinceTimeFateSourcePacket221": changed,
                   "packet": packet_binding, "deliveryManifest": delivery_binding,
                   "payloadMemberCount": len(rows), "checksPassed": 10, "checksFailed": 0,
                   "checks": [{"check": label, "passed": True} for label in [
                       "Authority 816/32/0 and 540/173 counts agree across index, queue, handoff and pending audit",
                       "Exactly four Time/Fate6 targets remain pending and non-operational; already accepted identities are excluded",
                       "Return281 is independently audited and selects this exact next group without changing authority",
                       "Return221 all-held archive, delivery, audit and receipt are bound into the current packet",
                       "All 140 Time/Fate source bindings are refreshed from current working-tree bytes",
                       "Current index/catalog status for every target matches the pending queue",
                       "Current index, catalog, queue, handoff and pending audit plus current Return281/Packet281 evidence are included",
                       "Request carries forward all four prior blocker IDs and prohibits unrelated re-review/application",
                       "Packet paths are safe and unique; embedded manifest and all member hashes/CRCs verify",
                       "No canonical changes, acceptances, applications or supplied program execution occurred"]],
                   "canonicalChangesBeforePreparation": False, "accepted": False, "applied": False, "request": request}
    preparation_path.write_bytes(jb(preparation)); preparation_binding = bind(preparation_path)
    record_path = BASE / "RANK9_TIMEFATE6_PACKET_282.json"
    record = {"id": "RANK9-TIMEFATE6-PACKET-282", "status": "PREPARED_UNSENT", "sourceAuthority": AUTH,
              "group": GROUP, "pendingIds": IDS, "packet": packet_binding, "deliveryManifest": delivery_binding,
              "preparation": preparation_binding, "candidate": bind(candidate_path), "conversation": CHAT,
              "checksPassed": 10, "checksFailed": 0}
    record_path.write_bytes(jb(record)); record_binding = bind(record_path)
    request_binding = bind(request_path)

    p = copy.deepcopy(p0)
    p.update({"id": "CURRENT32-PENDING-IDENTITY-AUDIT-282", "recordedAtUtc": now,
              "status": "TIMEFATE6_PACKET282_PREPARED_UNSENT_816_32",
              "preparedNextGroup": {"group": GROUP, "pendingIds": IDS, "pendingCount": 4,
                                    "status": "PACKET282_PREPARED_UNSENT_816_32",
                                    "packet": packet_binding, "deliveryManifest": delivery_binding,
                                    "preparation": preparation_binding, "freshPacketRequiredForCurrentAuthority": False}})
    pending_path = BASE / "CURRENT32_PENDING_IDENTITY_AUDIT_282.json"
    pending_path.write_bytes(jb(p)); pending_binding = bind(pending_path)

    q = copy.deepcopy(q0)
    group_row = next(row for row in q["currentPendingGroups"] if row["group"] == GROUP)
    group_row.update({"status": "PACKET282_PREPARED_UNSENT_816_32", "preparedPacket": packet_binding,
                      "deliveryManifest": delivery_binding, "packetRecord": record_binding,
                      "preparation": preparation_binding, "freshPacketRequiredForCurrentAuthority": False})
    next_row = {"group": GROUP, "pendingIds": IDS, "pendingCount": 4, "status": "PACKET282_PREPARED_UNSENT_816_32",
                "freshPacketRequiredForCurrentAuthority": False, "preparedPacket": packet_binding,
                "deliveryManifest": delivery_binding, "packetRecord": record_binding,
                "preparation": preparation_binding, "candidate": bind(candidate_path)}
    q.update({"id": "SPELL-REVIEW-QUEUE-282", "recordedAtUtc": now,
              "status": "RANK9_TIMEFATE6_PACKET282_PREPARED_UNSENT_816_32",
              "packetStatus": "RANK9_TIMEFATE6_CURRENT_SOURCE_PACKET_282_PREPARED_UNSENT_816_32",
              "currentPreparation": preparation_binding, "currentPacket": packet_binding,
              "currentDeliveryManifest": delivery_binding, "currentPacketDelivery": delivery_binding,
              "currentPacketRecord": record_binding, "currentPendingAudit": pending_binding,
              "pendingIdentityAudit": pending_binding,
              "next": next_row, "nextPreparedRequest": {"group": GROUP, "pendingIds": IDS,
                 "status": "PREPARED_UNSENT", "request": request_binding}, "nextSuggestedGroups": [next_row]})
    QUEUE.write_text(json.dumps(q, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    q_binding = bind(QUEUE)
    h = copy.deepcopy(h0)
    h.update({"id": "CURRENT-HANDOFF-282", "recordedAtUtc": now,
              "status": "RANK9_TIMEFATE6_PACKET282_PREPARED_UNSENT_816_32",
              "currentAuthority": AUTH, "nextGroup": GROUP,
              "nextStep": {"group": GROUP, "pendingIds": IDS, "pendingCount": 4,
                           "status": "PACKET282_PREPARED_UNSENT_816_32", "packet": packet_binding,
                           "deliveryManifest": delivery_binding},
              "queue": q_binding, "queueBinding": q_binding, "currentQueueBinding": q_binding,
              "pendingIdentityAudit": pending_binding, "currentPreparation": preparation_binding,
              "currentPacket": packet_binding, "currentPacketDelivery": delivery_binding,
              "currentPacketRecord": record_binding, "latestBatch": q["lastReviewedBatch"],
              "nextStepText": "Send independently audited Packet282 and its current 816/32 queue, handoff and pending audit to the GPT Director; keep polling and ping as needed; audit a sealed ruling and apply only exact acceptances."})
    HANDOFF.write_text(json.dumps(h, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    (BASE / "CURRENT_SPELL_REVIEW_SNAPSHOT_282.md").write_text(
        "# Current ordinary spell-review checkpoint 282\n\n"
        "Authority remains **816 reviewed/applied / 32 pending / 0 accepted-unapplied**, with 540 complete standalone procedures and 173 scoped interfaces. Return281 held nullification-wave (WC188-B01) and reality-anchor (WC188-B02) after a 17/17 independent audit; no acceptance or application occurred.\n\n"
        "**Packet282 is prepared, not yet independently audited or sent**, for only Time/Fate6: time-stop, fate-rewrite, collapse-timeline and eternal-prophecy. It refreshes all 140 current source bindings and preserves the prior Return221 blockers plus Return281 and Packet281 evidence.\n\n"
        "See [handoff](CURRENT_HANDOFF_282.json), [queue](CURRENT_SPELL_QUEUE_282.json), [pending audit](CURRENT32_PENDING_IDENTITY_AUDIT_282.json), [preparation](RANK9_TIMEFATE6_SOURCE_PREPARATION_282.json), and [packet](rank9_timefate6_current_source_282_prepared/DD_Rank9_TimeFate6_CurrentSource_282.zip).\n",
        encoding="utf-8")
    start = ROOT / "START_HERE.md"
    current = start.read_text(encoding="utf-8-sig")
    first, _, rest = current.partition("\n\n")
    if "Current ordinary spell-review handoff [282]" in first:
        start.write_text("**Current ordinary spell-review handoff [282](docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT_HANDOFF_282.json):** authority is 816 applied / 32 pending / 0 accepted-unapplied. Packet282 is prepared, awaiting independent audit, for Time/Fate6. See [packet](docs/audit/2026-10-08/full-game/director-spell-review-129/rank9_timefate6_current_source_282_prepared/DD_Rank9_TimeFate6_CurrentSource_282.zip) and [Return281 audit](docs/audit/2026-10-08/full-game/director-spell-review-129/RANK9_WARDCONTROL6_RETURN281_INDEPENDENT_AUDIT.json).\n\n" + rest,
                          encoding="utf-8", newline="\n")
    print(json.dumps({"status": "PREPARED_UNSENT", "authority": AUTH, "group": GROUP, "pendingIds": IDS,
                      "refreshedSources": len(refreshed_rows), "changedSincePacket221": changed,
                      "packet": packet_binding, "deliveryManifest": delivery_binding,
                      "payloadMembers": len(rows), "queue": bind(QUEUE), "handoff": bind(HANDOFF),
                      "pendingAudit": bind(pending_path)}, indent=2))


if __name__ == "__main__":
    main()
