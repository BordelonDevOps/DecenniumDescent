import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[6]
PACKET = Path(__file__).with_name("FINAL_WORD_GAZETTEER_SOURCE_LEAD_476_REPACK01.json")


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest().upper()


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


note = read_json(PACKET)
source_path = ROOT / note["source"]["path"]
decision_path = ROOT / note["directorReview"]["requiredWitnessReference"]["path"]
queue_path = ROOT / note["currentAuthority"]["queuePath"]
pending_path = ROOT / note["currentAuthority"]["pendingAuditPath"]
validation_path = Path(__file__).with_name("VALIDATION_476_REPACK01.json")

source_bytes = source_path.read_bytes()
source_text = source_bytes.decode("utf-8")
source_lines = source_text.splitlines()
queue = read_json(queue_path)
pending = read_json(pending_path)
decision = read_json(decision_path)

checks = []


def check(name: str, condition: bool):
    checks.append({"name": name, "passed": bool(condition)})


anchor = note["source"]["anchor"]
context_lines = note["source"]["adjacentContext"]
check(
    "gazetteer bytes and SHA-256 match the bound source",
    len(source_bytes) == note["source"]["bytes"]
    and sha256(source_bytes) == note["source"]["sha256"],
)
check(
    "exact surface-hook anchor resolves at the declared line",
    len(source_lines) >= anchor["line"]
    and source_lines[anchor["line"] - 1] == anchor["text"],
)
check(
    "adjacent context lines resolve exactly",
    all(source_lines[item["line"] - 1] == item["text"] for item in context_lines),
)
check(
    "Final Word Director hold and required witness fields remain bound",
    sha256(decision_path.read_bytes())
    == note["directorReview"]["requiredWitnessReference"]["sha256"]
    and decision.get("decision")
    == "HOLD_FINAL_WORD_PENDING_POSITIVE_SOURCE_QUALIFIED_CAPTURE_WITNESS"
    and "current living body/HP" in decision["minimumMissingWitness"][0],
)
check(
    "current Queue476 byte binding and authority match",
    len(queue_path.read_bytes()) == note["currentAuthority"]["queueBytes"]
    and sha256(queue_path.read_bytes()) == note["currentAuthority"]["queueSha256"]
    and queue["currentAuthority"]["reviewedApplied"] == 831
    and queue["currentAuthority"]["pending"] == 17
    and queue["currentAuthority"]["acceptedUnapplied"] == 0,
)
check(
    "current pending audit is bound and records Final Word pending",
    len(pending_path.read_bytes()) == note["currentAuthority"]["pendingAuditBytes"]
    and sha256(pending_path.read_bytes()) == note["currentAuthority"]["pendingAuditSha256"]
    and "final-word" in pending["pendingIds"],
)
check(
    "Elemental Shell remains first and Final Word remains second in priority order",
    queue["nextIdentity"] == "elemental-shell"
    and queue["continuingPriorityOrder"][:2] == ["elemental-shell", "final-word"],
)
check(
    "note records no acceptance, application, blocker closure, or queue effect",
    note["effects"]["finalWordAccepted"] is False
    and note["effects"]["finalWordApplied"] is False
    and note["effects"]["blockerClosed"] is False
    and note["effects"]["queueChanged"] is False,
)

failed = [item for item in checks if not item["passed"]]
report = {
    "status": "PASS" if not failed else "FAIL",
    "passed": len(checks) - len(failed),
    "failed": len(failed),
    "packet": {
        "path": str(PACKET.relative_to(ROOT)).replace("\\", "/"),
        "bytes": len(PACKET.read_bytes()),
        "sha256": sha256(PACKET.read_bytes()),
    },
    "checks": checks,
}
validation_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
print(json.dumps(report, indent=2))
raise SystemExit(0 if not failed else 1)
