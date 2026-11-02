from __future__ import annotations

import hashlib
import json
import subprocess
import zipfile
from datetime import datetime, timezone
from pathlib import Path


HERE = Path(__file__).resolve().parent
REVIEW = HERE.parent
ROOT = REVIEW.parents[4]
PROPOSAL_DIR = REVIEW / "elemental_shell_b01_test_source_proposal_478_repack01"
PREP_DIR = REVIEW / "elemental_shell_caster_premise_proposal_468"
QUAL_DIR = REVIEW / "elemental_shell_caster_qualification_472_repack01"
PROPOSAL_VALIDATION = PROPOSAL_DIR / "INDEPENDENT_VALIDATION_478_REPACK01.json"
ZIP_PATH = HERE / "DD_ElementalShell_B01_Witness_480_TESTONLY.zip"
VALIDATION_PATH = HERE / "INDEPENDENT_VALIDATION_480.json"


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


subprocess.run(["python", "-B", str(HERE / "build_b01_witness_480.py")], cwd=ROOT, check=True)
subprocess.run(["python", "-B", str(HERE / "verify_b01_witness_480.py")], cwd=ROOT, check=True)
validation = json.loads(VALIDATION_PATH.read_text(encoding="utf-8"))
assert validation["status"] == "PASS" and validation["failed"] == 0

payloads = [
    ("README_480.md", HERE / "README_480.md"),
    ("OWNER_DF218_B01_TEST_SOURCE_PROPOSAL_478_REPACK01_TESTONLY.json", PROPOSAL_DIR / "OWNER_DF218_B01_TEST_SOURCE_PROPOSAL_478_REPACK01_TESTONLY.json"),
    ("DIRECTOR_READBACK_478_REPACK01.json", PROPOSAL_DIR / "DIRECTOR_READBACK_478_REPACK01.json"),
    ("INDEPENDENT_VALIDATION_478_REPACK01.json", PROPOSAL_VALIDATION),
    ("SOURCE_GEOMETRY_PREFLIGHT_478_REPACK01.json", PROPOSAL_DIR / "SOURCE_GEOMETRY_PREFLIGHT_478_REPACK01.json"),
    ("OWNER_DF218_B01_ADOPTION_478_REPACK01_TESTONLY.json", PROPOSAL_DIR / "OWNER_DF218_B01_ADOPTION_478_REPACK01_TESTONLY.json"),
    ("CASTER_PREPARATION_PREMISE_468_TESTONLY.json", PREP_DIR / "CASTER_PREPARATION_PREMISE_468_TESTONLY.json"),
    ("OWNER_DF218_SHELL_CASTER_PREMISE_PROPOSAL_468_TESTONLY.json", PREP_DIR / "OWNER_DF218_SHELL_CASTER_PREMISE_PROPOSAL_468_TESTONLY.json"),
    ("OWNER_DF218_B02_SHELL_CASTER_PREMISE_ADOPTION_468_TESTONLY.json", PREP_DIR / "OWNER_DF218_B02_SHELL_CASTER_PREMISE_ADOPTION_468_TESTONLY.json"),
    ("DIRECTOR_READBACK_468.json", PREP_DIR / "DIRECTOR_READBACK_468.json"),
    ("SHELL_CASTER_QUALIFICATION_472_REPACK01_TESTONLY.json", QUAL_DIR / "SHELL_CASTER_QUALIFICATION_472_REPACK01_TESTONLY.json"),
    ("DIRECTOR_READBACK_472_REPACK01.json", QUAL_DIR / "DIRECTOR_READBACK_472_REPACK01.json"),
    ("DF218_B01_WITNESS_480_TESTONLY.json", HERE / "DF218_B01_WITNESS_480_TESTONLY.json"),
    ("B01_EVENT_TRACE_480.json", HERE / "B01_EVENT_TRACE_480.json"),
    ("INDEPENDENT_VALIDATION_480.json", VALIDATION_PATH),
    ("build_b01_witness_480.py", HERE / "build_b01_witness_480.py"),
    ("verify_b01_witness_480.py", HERE / "verify_b01_witness_480.py"),
]

manifest = {
    "schemaVersion": 1,
    "id": "MANIFEST-DF218-B01-WITNESS-480",
    "classification": "ADOPTED_TEST_ONLY_WITNESS_PACKET",
    "createdAtUtc": datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z"),
    "branchId": "DF218-SHELL-B01-TESTONLY-R1",
    "proposalSha256": "e00c3c8fad96883b6fe1d7ac07e1ed07f4b2f7b2f275dcee1853ce30b576ea69",
    "ownerAuthorization": "Adopt exact B01 Proposal478 Repack01 (Recommended)",
    "witnessSha256": validation["witnessSha256"],
    "validationSha256": sha(VALIDATION_PATH.read_bytes()),
    "memberCountExcludingManifest": len(payloads),
    "members": [{"path": name, "bytes": path.stat().st_size, "sha256": sha(path.read_bytes())} for name, path in payloads],
    "nonEffects": {"B01Closed": False, "B02Constructed": False, "identityAcceptedOrApplied": False, "canonicalRuleChanged": False, "queueChanged": False, "campaignEventClaimed": False},
}
manifest_bytes = (json.dumps(manifest, indent=2, ensure_ascii=False) + "\n").encode("utf-8")
(HERE / "MANIFEST_480.json").write_bytes(manifest_bytes)

with zipfile.ZipFile(ZIP_PATH, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
    for name, path in payloads:
        archive.writestr(name, path.read_bytes())
    archive.writestr("MANIFEST_480.json", manifest_bytes)

delivery = {
    "schemaVersion": 1,
    "id": "DELIVERY-DF218-B01-WITNESS-480",
    "status": "READY_FOR_GPT_DIRECTOR_REVIEW",
    "classification": "OWNER_ADOPTED_TEST_ONLY_WITNESS_NOT_SEALED",
    "archivePath": str(ZIP_PATH.relative_to(ROOT)).replace("\\", "/"),
    "archiveBytes": ZIP_PATH.stat().st_size,
    "archiveSha256": sha(ZIP_PATH.read_bytes()),
    "memberCount": len(payloads) + 1,
    "manifestPath": str((HERE / "MANIFEST_480.json").relative_to(ROOT)).replace("\\", "/"),
    "manifestSha256": sha(manifest_bytes),
    "proposalSha256": manifest["proposalSha256"],
    "ownerAdoptionPath": str((PROPOSAL_DIR / "OWNER_DF218_B01_ADOPTION_478_REPACK01_TESTONLY.json").relative_to(ROOT)).replace("\\", "/"),
    "ownerReply": manifest["ownerAuthorization"],
    "witnessPath": str((HERE / "DF218_B01_WITNESS_480_TESTONLY.json").relative_to(ROOT)).replace("\\", "/"),
    "witnessSha256": validation["witnessSha256"],
    "validationPath": str(VALIDATION_PATH.relative_to(ROOT)).replace("\\", "/"),
    "validationSha256": sha(VALIDATION_PATH.read_bytes()),
    "queueAuthority": {"reviewedApplied": 831, "pending": 17, "acceptedUnapplied": 0},
    "decisionBoundary": {"B01DirectorPass": False, "B01Closed": False, "B02Closed": False, "identityAcceptedOrApplied": False, "canonicalRuleChanged": False, "queueChanged": False, "campaignEventClaimed": False},
}
(HERE / "DELIVERY_480.json").write_text(json.dumps(delivery, indent=2) + "\n", encoding="utf-8", newline="\n")
print(json.dumps(delivery, indent=2))
