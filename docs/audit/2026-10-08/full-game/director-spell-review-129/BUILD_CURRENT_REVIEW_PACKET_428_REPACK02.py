from __future__ import annotations

import copy
import hashlib
import json
import zlib
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def read_json(name: str) -> tuple[dict, bytes]:
    data = (ROOT / name).read_bytes()
    return json.loads(data.decode("utf-8")), data


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def binding(path: str, data: bytes) -> dict:
    return {"path": path, "bytes": len(data), "sha256": digest(data), "crc32": f"{zlib.crc32(data) & 0xffffffff:08x}"}


def write_json(name: str, value: dict) -> bytes:
    data = (json.dumps(value, indent=2, ensure_ascii=False) + "\n").encode("utf-8")
    (ROOT / name).write_bytes(data)
    return data


def main() -> None:
    old_queue_name = "CURRENT_SPELL_QUEUE_428_REPACK01.json"
    old_handoff_name = "CURRENT_HANDOFF_428_REPACK01.json"
    queue_name = "CURRENT_SPELL_QUEUE_428_REPACK02.json"
    handoff_name = "CURRENT_HANDOFF_428_REPACK02.json"
    request_name = "CURRENT_REVIEW_PACKET_428_REPACK02.md"

    old_queue, old_queue_bytes = read_json(old_queue_name)
    old_handoff, old_handoff_bytes = read_json(old_handoff_name)
    delivery, _ = read_json("fortress_w09_successor_witness_428/DELIVERY_428.json")
    manifest, _ = read_json("fortress_w09_successor_witness_428/MANIFEST_428.json")
    independent, _ = read_json("fortress_w09_successor_witness_428/INDEPENDENT_VERIFICATION_428.json")
    overlays_delivery, _ = read_json("fortress_w01_successor_overlays_425/DELIVERY_425.json")
    overlays_verifier, _ = read_json("fortress_w01_successor_overlays_425/VERIFIER_RESULT_425.json")
    replay_path = ROOT / "fortress_w09_successor_witness_428/W09_REPLAY_428_TESTONLY.json"
    archive_path = ROOT / "fortress_w09_successor_witness_428/DD_Fortress_W09_Successor_Witness_428_TESTONLY.zip"
    replay_sha = digest(replay_path.read_bytes())
    archive_sha = digest(archive_path.read_bytes())
    assert replay_sha == delivery["witnessSha256"]
    assert archive_sha == delivery["archiveSha256"]
    assert independent["status"] == "PASS_PENDING_GPT_DIRECTOR_REVIEW"
    assert independent["checksFailed"] == 0
    assert overlays_delivery["status"] == "PASS_STATIC_OVERLAYS_PENDING_GPT_DIRECTOR_READBACK"
    assert overlays_verifier["checksFailed"] == 0
    assert old_queue["currentAuthority"] == {"reviewedApplied": 830, "pending": 18, "acceptedUnapplied": 0, "completeStandaloneProcedures": 554, "scopedInterfaces": 173}

    queue = copy.deepcopy(old_queue)
    queue["id"] = "CURRENT-SPELL-QUEUE-428-REPACK02"
    queue["supersedesQueue"] = binding(old_queue_name, old_queue_bytes)
    queue["currentHandoffPath"] = f"docs/audit/2026-10-08/full-game/director-spell-review-129/{handoff_name}"
    queue["currentReviewPacket"] = {
        "witnessPath": "docs/audit/2026-10-08/full-game/director-spell-review-129/fortress_w09_successor_witness_428/W09_REPLAY_428_TESTONLY.json",
        "witnessSha256": replay_sha,
        "archivePath": "docs/audit/2026-10-08/full-game/director-spell-review-129/fortress_w09_successor_witness_428/DD_Fortress_W09_Successor_Witness_428_TESTONLY.zip",
        "archiveSha256": archive_sha,
        "deliveryPath": "docs/audit/2026-10-08/full-game/director-spell-review-129/fortress_w09_successor_witness_428/DELIVERY_428.json",
        "manifestPath": "docs/audit/2026-10-08/full-game/director-spell-review-129/fortress_w09_successor_witness_428/MANIFEST_428.json",
        "requestPath": f"docs/audit/2026-10-08/full-game/director-spell-review-129/{request_name}",
        "classification": "TEST_ONLY_UNSEALED_PENDING_GPT_DIRECTOR_REVIEW",
        "supersedesWitnessSha256": old_queue["currentReviewPacket"]["witnessSha256"],
    }
    queue["repackNote"] = "Only the exact current W09 review-artifact pointer and handoff location were reconciled after the corrected 428 delivery. Authority, identity dispositions, pending IDs, and all historical witness source snapshots are unchanged."
    queue_bytes = write_json(queue_name, queue)

    handoff = copy.deepcopy(old_handoff)
    handoff["id"] = "CURRENT-HANDOFF-428-REPACK02"
    handoff["supersedes"] = f"docs/audit/2026-10-08/full-game/director-spell-review-129/{old_handoff_name}"
    handoff["queue"] = binding(f"docs/audit/2026-10-08/full-game/director-spell-review-129/{queue_name}", queue_bytes)
    handoff["currentReviewPacket"] = copy.deepcopy(queue["currentReviewPacket"])
    handoff["W09Witness"]["replaySha256"] = replay_sha
    handoff["W09Witness"]["archiveSha256"] = archive_sha
    handoff["W09Witness"]["deliveryPath"] = queue["currentReviewPacket"]["deliveryPath"]
    handoff["W09Witness"]["manifestPath"] = queue["currentReviewPacket"]["manifestPath"]
    handoff["W09Witness"]["status"] = delivery["status"]
    handoff["nextStep"] = "GPT Director: review W01 successor overlays 425 and the exact corrected, owner-adopted PG328-W09-R1 reversible TEST_ONLY witness 428 at the hashes in currentReviewPacket. Return precise pass/hold findings and state whether Fortress is ready for identity acceptance. Do not infer a witness seal, campaign event, canonical change, or application. Authority remains 830 applied / 18 pending / 0 accepted-unapplied. If Fortress becomes accepted, continue the remaining pending identities from this queue."
    handoff["repackNote"] = queue["repackNote"]
    handoff_bytes = write_json(handoff_name, handoff)

    request = f"""# Director review request — current queue packet 428 repack 02

Please review the current W01 successor overlays 425 and the corrected W09 witness 428 using the exact artifacts below. The review request follows current queue 428; only its review-packet pointer is refreshed to the corrected W09 delivery. Queue authority and dispositions remain **830 applied / 18 pending / 0 accepted-unapplied**.

## Exact review artifacts

- W01 overlays ZIP: `{overlays_delivery['archive']['sha256']}` ({overlays_delivery['archive']['bytes']} bytes). Static verifier: {overlays_verifier['checksPassed']} checks passed, 0 failed; independent review: {overlays_delivery['status']}.
- W09 replay JSON: `{replay_sha}` ({replay_path.stat().st_size} bytes).
- W09 witness ZIP: `{archive_sha}` ({delivery['archiveBytes']} bytes), {delivery['memberCount']} members. Delivery status: `{delivery['status']}`.
- W09 independent checks: {independent['checksPassed']} passed, {independent['checksFailed']} failed; {independent['eventCount']} events.
- W09 adoption is scoped to hypothetical PG328-W09-R1 construction only. The witness remains TEST_ONLY and unsealed.

## GitHub main links

- [W01 review request](https://github.com/BordelonDevOps/DecenniumDescent/blob/main/docs/audit/2026-10-08/full-game/director-spell-review-129/fortress_w01_successor_overlays_425/DIRECTOR_REVIEW_REQUEST_425.md)
- [W01 overlays ZIP](https://github.com/BordelonDevOps/DecenniumDescent/blob/main/docs/audit/2026-10-08/full-game/director-spell-review-129/fortress_w01_successor_overlays_425/DD_Fortress_W01_Successor_Overlays_425_TESTONLY.zip)
- [W01 verifier result](https://github.com/BordelonDevOps/DecenniumDescent/blob/main/docs/audit/2026-10-08/full-game/director-spell-review-129/fortress_w01_successor_overlays_425/VERIFIER_RESULT_425.json)
- [W09 review request](https://github.com/BordelonDevOps/DecenniumDescent/blob/main/docs/audit/2026-10-08/full-game/director-spell-review-129/fortress_w09_successor_witness_428/DIRECTOR_REVIEW_REQUEST_428.md)
- [W09 replay JSON](https://github.com/BordelonDevOps/DecenniumDescent/blob/main/docs/audit/2026-10-08/full-game/director-spell-review-129/fortress_w09_successor_witness_428/W09_REPLAY_428_TESTONLY.json)
- [W09 witness ZIP](https://github.com/BordelonDevOps/DecenniumDescent/blob/main/docs/audit/2026-10-08/full-game/director-spell-review-129/fortress_w09_successor_witness_428/DD_Fortress_W09_Successor_Witness_428_TESTONLY.zip)
- [W09 delivery](https://github.com/BordelonDevOps/DecenniumDescent/blob/main/docs/audit/2026-10-08/full-game/director-spell-review-129/fortress_w09_successor_witness_428/DELIVERY_428.json)
- [Updated queue](https://github.com/BordelonDevOps/DecenniumDescent/blob/main/docs/audit/2026-10-08/full-game/director-spell-review-129/{queue_name})
- [Updated handoff](https://github.com/BordelonDevOps/DecenniumDescent/blob/main/docs/audit/2026-10-08/full-game/director-spell-review-129/{handoff_name})

Please verify the exact source/adoption bindings, W01 overlay scope and checks, and W09 corrected replay hash, timing, support-state witness, and closure order. Return a precise pass/hold list and whether Fortress is ready for identity acceptance. Do not infer a witness seal, campaign event, canonical change, or application. The W09 witness binds the prior queue snapshot as its construction-time source; this repack changes no witness source or event.
"""
    (ROOT / request_name).write_text(request, encoding="utf-8")

    check_queue, check_queue_bytes = read_json(queue_name)
    check_handoff, _ = read_json(handoff_name)
    assert check_queue["currentAuthority"] == old_queue["currentAuthority"]
    assert check_queue["remainingPendingIds"] == old_queue["remainingPendingIds"]
    assert check_queue["acceptedIds"] == old_queue["acceptedIds"] and check_queue["appliedIds"] == old_queue["appliedIds"]
    assert check_queue["currentReviewPacket"]["witnessSha256"] == replay_sha
    assert check_handoff["queue"]["sha256"] == digest(check_queue_bytes)
    assert check_handoff["W09Witness"]["replaySha256"] == replay_sha
    print(json.dumps({"queue": queue_name, "queueSha256": digest(queue_bytes), "handoff": handoff_name, "handoffSha256": digest(handoff_bytes), "request": request_name, "w09ReplaySha256": replay_sha, "w09ArchiveSha256": archive_sha, "authority": queue["currentAuthority"], "assertions": "PASS"}, indent=2))


if __name__ == "__main__":
    main()
