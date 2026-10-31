from __future__ import annotations

import datetime as dt
import hashlib
import json
import pathlib
import zlib

ROOT = pathlib.Path.cwd()
A = ROOT / "docs/audit/2026-10-08/full-game/director-spell-review-129"
AUTHORITY = {"reviewedApplied": 822, "pending": 26, "acceptedUnapplied": 0,
             "completeStandaloneProcedures": 546, "scopedInterfaces": 173}

def bind(path: pathlib.Path) -> dict:
    raw = path.read_bytes()
    return {"path": path.relative_to(ROOT).as_posix(), "bytes": len(raw),
            "sha256": hashlib.sha256(raw).hexdigest(), "crc32": f"{zlib.crc32(raw) & 0xffffffff:08x}"}

def read(path: pathlib.Path):
    return json.loads(path.read_text(encoding="utf-8-sig"))

def main():
    stamp = dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")
    packet = A / "rank9_defenseform8_current_source_306_prepared/DD_Rank9_DefenseForm8_CurrentSource_306.zip"
    delivery = A / "rank9_defenseform8_current_source_306_prepared/DD_Rank9_DefenseForm8_CurrentSource_306_DELIVERY.json"
    audit = A / "ELEMENTAL_SHELL_PACKET_306_INDEPENDENT_AUDIT.json"
    prep = A / "RANK9_DEFENSEFORM8_SOURCE_PREPARATION_306.json"
    audit_obj, prep_obj = read(audit), read(prep)
    assert audit_obj["status"] == "PASS" and audit_obj["failedChecks"] == 0 and audit_obj["checkCount"] == 15
    assert prep_obj["status"] == "CURRENT_SOURCE_PACKET_PREPARED_UNSENT_822_26_0"
    assert prep_obj["sourceAuthority"] == AUTHORITY and prep_obj["pendingIds"] == ["elemental-shell"]
    assert prep_obj["targetCaseCountFromReturn218"] == 21 and prep_obj["currentSourceFileCount"] == 87
    confirmation = {
        "id": "ELEMENTAL-SHELL-HANDOFF-DIRECTOR-CONFIRMATION-306", "recordedAtUtc": stamp,
        "source": {"service": "ChatGPT", "conversationTitle": "Calibration review part 6",
                   "url": "https://chatgpt.com/g/g-p-67f17555a8dc8191a2b5b81e6d8adc12-dungeon-crawler/c/6adc506d-8770-83ea-b64c-0345d9b9b682"},
        "exactResponse": "Confirmed—the correction is sufficient. /nextPendingGroup now exactly matches /currentPreparation. The stale pointer is preserved unchanged under /historicalNextPendingGroupPointer304. Handoff, requirements and current queue size/SHA-256/CRC bindings verify. Authority remains 822 applied / 26 pending / 0 accepted-unapplied; 546 procedures / 173 interfaces. Proceed with the Elemental Shell-only packet for DF218-B01/B02, refreshing the 87-source inventory and preserving all 21 cases. The recorded requirements accurately preserve my ruling; no further handoff correction is needed. Next: Elemental Shell → Timeless Form → Invulnerable Sphere. Final Word remains held. No synthetic substitution, acceptance or application is authorized by this confirmation.",
        "acceptedIds": [], "appliedIds": [], "canonicalFilesChanged": False,
    }
    confirmation_path = A / "ELEMENTAL_SHELL_HANDOFF_DIRECTOR_CONFIRMATION_306.json"
    confirmation_path.write_text(json.dumps(confirmation, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    receipt = {
        "id": "ELEMENTAL-SHELL-DELTA-306-SUBMISSION-RECEIPT", "recordedAtUtc": stamp,
        "status": "READY_FOR_DIRECTOR_ADJUDICATION",
        "currentAuthority": AUTHORITY, "targetIds": ["elemental-shell"],
        "blockersSubmitted": ["DF218-B01", "DF218-B02"],
        "packet": bind(packet), "deliveryManifest": bind(delivery), "independentAudit": bind(audit),
        "sourcePreparation": bind(prep), "correctedHandoff": bind(A / "CURRENT_HANDOFF_305.json"),
        "handoffCorrectionValidation": bind(A / "ELEMENTAL_SHELL_HANDOFF_CORRECTION_VALIDATION_305.json"),
        "directorHandoffConfirmation": bind(confirmation_path),
        "preservedCaseCount": 21, "refreshedCurrentSourceCount": 87,
        "acceptedIds": [], "appliedIds": [], "heldIds": [],
        "canonicalFilesChanged": False, "runtimeExecuted": False,
        "request": "Adjudicate Elemental Shell only under DF218-B01/B02. Issue exact ACCEPT only if both source-qualified witnesses close the recorded blockers; otherwise HOLD with the narrowest outstanding evidence and no synthetic substitution. Do not adjudicate other identities or authorize application.",
    }
    receipt_path = A / "ELEMENTAL_SHELL_PACKET_306_SUBMISSION_RECEIPT.json"
    receipt_path.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"status": receipt["status"], "packet": receipt["packet"], "audit": receipt["independentAudit"],
                      "receipt": bind(receipt_path), "directorConfirmation": bind(confirmation_path)}, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
