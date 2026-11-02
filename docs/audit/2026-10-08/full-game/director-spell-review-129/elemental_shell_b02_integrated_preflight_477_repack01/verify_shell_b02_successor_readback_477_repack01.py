import hashlib
import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[6]
HERE = Path(__file__).resolve().parent
READBACK_PATH = HERE / "DIRECTOR_READBACK_477_REPACK01_SUCCESSOR_READY.json"
VALIDATION_PATH = HERE / "VALIDATION_DIRECTOR_READBACK_477_REPACK01_SUCCESSOR_READY.json"


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest().lower()


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


readback_bytes = READBACK_PATH.read_bytes()
readback = json.loads(readback_bytes.decode("utf-8"))
queue_path = ROOT / readback["currentAuthority"]["queuePath"]
queue_bytes = queue_path.read_bytes()
queue = json.loads(queue_bytes.decode("utf-8"))
preflight_path = ROOT / readback["reviewedPreflight"]["path"]
preflight_bytes = preflight_path.read_bytes()
preflight = json.loads(preflight_bytes.decode("utf-8"))
historical = readback["controllingRecordResolution"]["historicalReceipt"]
historical_path = ROOT / historical["path"]
historical_bytes = historical_path.read_bytes()
historical_json = json.loads(historical_bytes.decode("utf-8"))
github_ref = readback["reviewedPreflight"]["githubRef"]

checks = []


def check(name: str, condition: bool, detail=None):
    checks.append({"name": name, "passed": bool(condition), **({"detail": detail} if detail is not None else {})})


check(
    "Director output SHA-256 matches the exact received correction",
    sha256(readback_bytes) == "e5ca751b8bce61bd655337379f78f0936940986380110c64f9aa6faa4529becc",
)
check(
    "Readback is an exact-target readiness correction for the b673 Repack01 successor",
    readback["status"] == "READY_FOR_OWNER_ADOPTION"
    and readback["classification"] == "TEST_ONLY_PROPOSAL_READINESS_NOT_ADOPTION_OR_IDENTITY_DECISION"
    and readback["reviewedPreflight"]["sha256"] == "b673305a49eb10dcfd7da1de676ea883cbcb2f34abcc308310ef00fd0c549c64"
    and readback["reviewedPreflight"]["bytes"] == 40789,
)
check(
    "Saved NOT_READY receipt remains intact and targets only original 529245 preflight",
    len(historical_bytes) == historical["bytes"]
    and sha256(historical_bytes) == historical["sha256"]
    and historical_json["status"] == "NOT_READY_FOR_OWNER_ADOPTION"
    and historical_json["reviewedPreflightSha256"] == "529245d4a1fc28c7e83a9ba562eb76c8b91ddd5d7d864e1e156c38d88c9739d0",
)
check(
    "Correction supersedes historical NOT_READY decision for the exact successor only",
    readback["controllingRecordResolution"]["answer"] == "YES_FOR_THE_EXACT_SUCCESSOR_ONLY"
    and readback["controllingRecordResolution"]["originalReceiptRewritten"] is False
    and readback["controllingRecordResolution"]["supersedesForSuccessorOnly"] is True,
)
check(
    "All seven corrections are resolved for proposal readiness and no corrections remain",
    len(readback["corrections"]) == 7
    and {item["id"] for item in readback["corrections"]}
    == {f"477-C0{i}" for i in range(1, 8)}
    and all(item["status"] == "RESOLVED_FOR_PROPOSAL_READINESS" for item in readback["corrections"])
    and readback["remainingCorrections"] == [],
)
check(
    "Owner adoption is still required and is bound to the exact B02 branch only",
    readback["ownerAdoption"]["received"] is False
    and readback["ownerAdoption"]["requiredExactProposalSha256"]
    == "b673305a49eb10dcfd7da1de676ea883cbcb2f34abcc308310ef00fd0c549c64"
    and readback["ownerAdoption"]["branchId"] == "DF218-SHELL-B02-R2-PROPOSED"
    and len(readback["ownerAdoption"]["scope"]) == 7,
)
check(
    "Next step requires owner adoption before witness construction and later review",
    "before constructing" in readback["nextPermittedStep"]
    and "A later completed witness still requires review" in readback["nextPermittedStep"],
)
check(
    "B01 remains separate and unadopted",
    readback["separateB01"]["status"] == "READY_FOR_OWNER_ADOPTION_UNCHANGED"
    and readback["separateB01"]["ownerAdoptionReceived"] is False
    and readback["separateB01"]["notReviewedOrAdoptedByThisRecord"] is True,
)
check(
    "No identity acceptance, application, campaign, canonical or queue effect is asserted",
    readback["identityDisposition"]["status"] == "HELD"
    and readback["identityDisposition"]["acceptedIds"] == []
    and readback["identityDisposition"]["appliedIds"] == []
    and readback["identityDisposition"]["applicationAuthorized"] is False
    and all(value is False for value in readback["nonEffects"].values()),
)
check(
    "Current Queue476 bytes and 831/17/0 authority match",
    sha256(queue_bytes) == readback["currentAuthority"]["queueSha256"]
    and queue["currentAuthority"]["reviewedApplied"] == 831
    and queue["currentAuthority"]["pending"] == 17
    and queue["currentAuthority"]["acceptedUnapplied"] == 0
    and queue["nextIdentity"] == "elemental-shell",
)
check(
    "Repack01 file bytes and preflight semantics match the readback target",
    len(preflight_bytes) == readback["reviewedPreflight"]["bytes"]
    and sha256(preflight_bytes) == readback["reviewedPreflight"]["sha256"]
    and preflight["id"] == readback["reviewedPreflight"]["id"],
)

bindings = readback["sourceBindings"]
correspondence = readback["sourceByteCorrespondence"]
check(
    "All 17 source bindings pair with 17 explicit byte-domain correspondences",
    len(bindings) == 17
    and len(correspondence) == 17
    and all(bindings[i]["path"] == correspondence[i]["path"] for i in range(17))
    and all(bindings[i]["bytes"] == correspondence[i]["declaredBytes"] for i in range(17))
    and all(bindings[i]["sha256"].lower() == correspondence[i]["declaredSha256"].lower() for i in range(17)),
)

binding_failures = []
for item in correspondence:
    source_path = ROOT / item["path"]
    try:
        working_bytes = source_path.read_bytes()
        git_bytes = subprocess.check_output(
            ["git", "show", f"{github_ref}:{item['path']}"],
            cwd=ROOT,
            stderr=subprocess.STDOUT,
        )
        working_ok = len(working_bytes) == item["readBytes"] and sha256(working_bytes) == item["readSha256"].lower()
        git_ok = len(git_bytes) == item["gitBytes"] and sha256(git_bytes) == item["gitSha256"].lower()
        transform = working_bytes.replace(b"\r\n", b"\n")
        if item["correspondence"] == "BYTE_IDENTICAL":
            transform_ok = working_bytes == git_bytes
        elif item["correspondence"] == "CRLF_TO_LF_ONLY":
            transform_ok = transform == git_bytes
        else:
            transform_ok = False
        if not (working_ok and git_ok and transform_ok):
            binding_failures.append(item["path"])
    except Exception as exc:  # report the exact broken source path for review
        binding_failures.append(f"{item['path']}: {exc}")

check(
    "All declared source attachments match current working bytes and commit-pinned Git blobs",
    len(binding_failures) == 0,
    binding_failures or None,
)

failed = [item for item in checks if not item["passed"]]
report = {
    "id": "DF218-B02-SUCCESSOR-READBACK-477-REPACK01-INDEPENDENT-VALIDATION",
    "status": "PASS" if not failed else "FAIL",
    "passed": len(checks) - len(failed),
    "failed": len(failed),
    "readback": {
        "path": str(READBACK_PATH.relative_to(ROOT)).replace("\\", "/"),
        "bytes": len(readback_bytes),
        "sha256": sha256(readback_bytes),
    },
    "reviewedPreflightSha256": readback["reviewedPreflight"]["sha256"],
    "historicalReceiptStatus": historical_json["status"],
    "ownerAdoptionReceived": readback["ownerAdoption"]["received"],
    "sourceBindingsVerified": len(correspondence) - len(binding_failures),
    "sourceGitRef": github_ref,
    "checks": checks,
}
VALIDATION_PATH.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
print(json.dumps(report, indent=2))
raise SystemExit(0 if not failed else 1)
