from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[6]
BASE = Path("docs/audit/2026-10-08/full-game/director-spell-review-129")
PACK = BASE / "elemental_shell_branch_order_recommendation_479"
NOTE = PACK / "DIRECTOR_READBACK_SHELL_BRANCH_ORDER_479.json"
QUEUE = BASE / "CURRENT_SPELL_QUEUE_476_REPACK01.json"
B01 = BASE / "elemental_shell_b01_test_source_proposal_478_repack01/OWNER_DF218_B01_TEST_SOURCE_PROPOSAL_478_REPACK01_TESTONLY.json"
B01_READBACK = BASE / "elemental_shell_b01_test_source_proposal_478_repack01/DIRECTOR_READBACK_478_REPACK01.json"
B01_VALIDATION = BASE / "elemental_shell_b01_test_source_proposal_478_repack01/INDEPENDENT_VALIDATION_478_REPACK01.json"
B02 = BASE / "elemental_shell_b02_integrated_preflight_477_repack01/SHELL_B02_INTEGRATED_PREFLIGHT_477_REPACK01_TESTONLY.json"
B02_READBACK = BASE / "elemental_shell_b02_integrated_preflight_477_repack01/DIRECTOR_READBACK_477_REPACK01_SUCCESSOR_READY.json"
B02_VALIDATION = BASE / "elemental_shell_b02_integrated_preflight_477_repack01/VALIDATION_DIRECTOR_READBACK_477_REPACK01_SUCCESSOR_READY.json"


def read(path: Path):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def sha(path: Path) -> str:
    return hashlib.sha256((ROOT / path).read_bytes()).hexdigest()


note = read(NOTE)
queue = read(QUEUE)
b01 = read(B01)
b01_readback = read(B01_READBACK)
b01_validation = read(B01_VALIDATION)
b02 = read(B02)
b02_readback = read(B02_READBACK)
b02_validation = read(B02_VALIDATION)

checks = {
    "current_queue_is_exact_Queue476_831_17_0": sha(QUEUE) == "4ae9ed74080e2919e7223aeee54fe1d0a380b0117248648027a3f5dfbc95e9cb" and queue["currentAuthority"]["reviewedApplied"] == 831 and queue["currentAuthority"]["pending"] == 17 and queue["currentAuthority"]["acceptedUnapplied"] == 0,
    "B01_exact_proposal_hash_and_Director_readiness_match": sha(B01) == "e00c3c8fad96883b6fe1d7ac07e1ed07f4b2f7b2f275dcee1853ce30b576ea69" and b01_readback["status"] == "READY_FOR_OWNER_ADOPTION",
    "B02_exact_proposal_hash_and_Director_readiness_match": sha(B02) == "b673305a49eb10dcfd7da1de676ea883cbcb2f34abcc308310ef00fd0c549c64" and b02_readback["status"] == "READY_FOR_OWNER_ADOPTION",
    "B01_independent_validation_passes_76_checks": b01_validation["status"] == "PASS" and b01_validation["checksPassed"] == 76 and b01_validation["checksFailed"] == 0,
    "B02_successor_validation_passes_13_checks": b02_validation["status"] == "PASS" and b02_validation["passed"] == 13 and b02_validation["failed"] == 0,
    "both_proposals_are_still_unadopted_and_witness_free": b01["classification"] == "OWNER_PROPOSED_TEST_ONLY_SOURCE_CONTRACT_NOT_ADOPTED_NO_WITNESS" and b01["decisionBoundary"]["witnessConstructed"] is False and b02["proposedOwnerPremises"]["adopted"] is False and b02_readback["ownerAdoption"]["received"] is False and "before constructing the branch" in b02_readback["nextPermittedStep"],
    "Director_recommendation_orders_B01_then_B02_and_requires_both": note["status"] == "RECOMMEND_B01_PROPOSAL478_REPACK01_FIRST" and [x["order"] for x in note["recommendedSequence"]] == [1, 2] and "Both subparts are required" in note["exactDirectorResponse"],
    "recommendation_is_separate_from_owner_authorization_and_queue_effects": note["ownerAuthorization"]["status"] == "AWAITING_EXACT_BRANCH_SELECTION" and note["decisionBoundary"]["queueChanged"] is False and note["decisionBoundary"]["ShellAccepted"] is False,
}
passed = sum(checks.values())
result = {
    "status": "PASS" if passed == len(checks) else "FAIL",
    "passed": passed,
    "failed": len(checks) - passed,
    "checks": [{"name": name, "passed": value} for name, value in checks.items()],
}
(ROOT / PACK / "VALIDATION_479.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
print(json.dumps(result, indent=2))
raise SystemExit(0 if passed == len(checks) else 1)
