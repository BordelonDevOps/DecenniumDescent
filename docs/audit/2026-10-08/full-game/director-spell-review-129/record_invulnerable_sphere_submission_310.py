from __future__ import annotations

import datetime as dt
import hashlib
import json
import pathlib
import subprocess

ROOT = pathlib.Path.cwd()
A = ROOT / "docs/audit/2026-10-08/full-game/director-spell-review-129"
OUT = A / "rank9_defenseform8_current_source_310_prepared"
FILES = {
    "packet": OUT / "DD_Rank9_DefenseForm8_CurrentSource_310.zip",
    "delivery": OUT / "DD_Rank9_DefenseForm8_CurrentSource_310_DELIVERY.json",
    "independentAudit": A / "INVULNERABLE_SPHERE_PACKET_310_INDEPENDENT_AUDIT.json",
    "directorRequirements": A / "INVULNERABLE_SPHERE_DIRECTOR_REQUIREMENTS_310.json",
}
URL = "https://chatgpt.com/g/g-p-67f17555a8dc8191a2b5b81e6d8adc12-dungeon-crawler/c/6adc506d-8770-83ea-b64c-0345d9b9b682"
MESSAGE = (
    "Packet 310 is attached and independently verified PASS (13 checks, 0 failures). Please review only "
    "invulnerable-sphere / DF218-B04 under the current 822 applied / 26 pending / 0 accepted-unapplied authority. "
    "The packet preserves the exact Return218 Sphere procedure and all 14 case IDs, binds the current 87-source "
    "inventory and prior Return280/Return308 hold context, and keeps route leads explicitly non-findings. Adjudicate "
    "only what the packet evidence supports. Return the sealed decision ZIP and exact DELIVERY.json. If the required "
    "source-qualified lawful planar-crossing route and complete Sphere-caused denial witness are still missing, return "
    "HOLD with the narrowest exact missing evidence; do not invent actors, permissions, endpoints, or encounters, revise "
    "blockers, or accept/apply anything. Confirm acceptedIds, appliedIds, heldIds, current authority, exact next "
    "identity/order, and remaining closure-task count. Keep Final Word, Elemental Shell, and Timeless Form holds separate."
)


def sha(path: pathlib.Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    delivery = json.loads(FILES["delivery"].read_text(encoding="utf-8-sig"))
    audit = json.loads(FILES["independentAudit"].read_text(encoding="utf-8-sig"))
    assert audit["status"] == "PASS" and audit["failedChecks"] == 0
    assert audit["packet"]["sha256"] == delivery["archive"]["sha256"] == sha(FILES["packet"])
    assert all(p.is_file() for p in FILES.values())
    commit = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    receipt = {
        "id": "INVULNERABLE-SPHERE-PACKET310-SUBMISSION-RECEIPT",
        "recordedAtUtc": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
        "status": "SUBMITTED_WAITING_FOR_DIRECTOR_DECISION",
        "destination": {"service": "ChatGPT", "chatTitle": "Calibration review part 6", "url": URL},
        "scope": {"spellIds": ["invulnerable-sphere"], "blockerIds": ["DF218-B04"],
                  "authority": delivery["authority"]},
        "attachments": {
            key: {"path": path.relative_to(ROOT).as_posix(), "bytes": path.stat().st_size, "sha256": sha(path)}
            for key, path in FILES.items()
        },
        "packetArchive": delivery["archive"],
        "independentAudit": {"status": audit["status"], "checkCount": audit["checkCount"],
                             "failedChecks": audit["failedChecks"]},
        "message": MESSAGE,
        "submissionEvidence": "The sent message and all four attachment names were visible in the Director chat; the response showed Working.",
        "baseCommitAtSubmission": commit,
        "canonicalIndexChangedBySubmission": False,
        "applicationPerformed": False,
    }
    out = A / "INVULNERABLE_SPHERE_PACKET_310_SUBMISSION_RECEIPT.json"
    out.write_text(json.dumps(receipt, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({"status": receipt["status"], "path": out.relative_to(ROOT).as_posix(),
                      "sha256": sha(out), "attachments": len(FILES)}, indent=2))


if __name__ == "__main__":
    main()
