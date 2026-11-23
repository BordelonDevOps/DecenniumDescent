"""Reconcile accepted progress and actual successor selection; preserve formal obligations."""
import copy
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
PACKET = Path(__file__).resolve().parent
REL = PACKET.relative_to(ROOT).as_posix()
BASELINE = "4abfdd598b48225002fabdec2f8121ce23fb4d49"
path = ROOT / "docs/unity/IMPLEMENTATION_STATUS.json"
before = json.loads(subprocess.check_output(["git", "show", BASELINE + ":docs/unity/IMPLEMENTATION_STATUS.json"], cwd=ROOT))
current = json.loads(path.read_text(encoding="utf-8-sig"))
assert current == before, "Review intervening map changes instead of overwriting them."
after = copy.deepcopy(before)
after["status"] = "FULL_CSHARP_GOAL_ACTIVE_INT05_SOURCE_API_DESIGN"
after["nextModule"] = {
    "id": "INT-05-ADMITTED-COMMAND-AND-CHOICE-SURFACE",
    "status": "SELECTED_FOR_SOURCE_API_DESIGN_NOT_RUNTIME_IMPLEMENTATION",
    "afterAcceptedModule": "MGT-02-CONNECTED-WORK-CONTROL",
    "actualGptRecommendationResponse": "e5e0261e-f693-5c9c-92f3-1be2225d25bf",
    "codexSelectionConcurred": True,
    "sourceApiReview": "OPEN_HC01_TO_HC05_AND_EXACT_INVENTORY_EVIDENCE_PLAN",
    "implementationAuthorized": False, "runtimeStarted": False,
    "formalDependencies": ["FND-05", "INT-03"], "formalGraphUnchanged": True,
    "definition": REL + "/MODULE_DEFINITION.md", "contract": REL + "/SOURCE_API_CONTRACT.md",
    "inventory": REL + "/OPERATION_INVENTORY.json", "selection": REL + "/SELECTION_CONCURRENCE.json",
    "unityAuthorized": False,
}
after["hold"]["implementation"] = "FULL_CSHARP_GOAL_ACTIVE_INT05_SOURCE_API_DESIGN"
after["hold"]["allowed"] = "Complete INT-05 admission/source/API inventory and contract review with GPT; preserve accepted runtime/evidence. Implement only after actual HC-01–05 and inventory/evidence agreement."
after["hold"]["nextRecordedGate"] = "Actual agreement on the selected INT-05 source/API contract and complete operation/profile/payload/source/evidence dispositions."
updates = {
    "FND-02": "Versioned canonical saves, strict causal restore, pending-state continuation, atomic invalid-save rejection and explicit backup recovery are accepted for the named profiles. Historical Ferry qualification covers authentic95–113 and current114; later Consecration115, ordinary magical activity116 and connected work control remain separately accepted. Latest MGT-02 qualification includes 22 authentic original-policy continuations and strict current-profile pending work/quality/receipt/backup continuation, with same-wire birthplace limits retained.",
    "INT-04": "The independent recipe4 semantic/parity verifier remains accepted. Historical TAC-10 retains 1,584 passing cases and five matching 463-command paths; Consecration and OMA retain their exact later acceptance. Latest MGT-02 has five complete 244-command paths and 4,256 exact comparisons. Its raw regression is 1,600 PASS / one retained I/O FAIL, actual exits 0/0/1/0; the separately reviewed exact same-binary recheck reconciles 1,601 unique passing cases. No raw failure is erased and the I/O cause remains unresolved.",
}
evidence = [
    "docs/unity/evidence/2026-11-17-chr05-consecration/README.md",
    "docs/unity/evidence/2026-11-23-tac01-ordinary-magic/FINAL_ACCEPTANCE.md",
    "docs/unity/evidence/2026-11-23-mgt02-connected-work-control/FINAL_ACCEPTANCE.json",
    "docs/unity/evidence/2026-11-23-mgt02-connected-work-control/ACCEPTANCE_EVIDENCE_MATRIX.md",
]
for p in evidence:
    assert (ROOT / p).is_file(), p
for item in after["workItems"]:
    if item["id"] in updates:
        item["implementedOrAcceptedScope"] = updates[item["id"]]
        item["evidence"] += [p for p in evidence if p not in item["evidence"]]
for old, new in zip(before["workItems"], after["workItems"]):
    for key in old:
        if key not in ("implementedOrAcceptedScope", "evidence"):
            assert old[key] == new[key], (old["id"], key)
assert before["readiness"] == after["readiness"]
assert before["completionContract"] == after["completionContract"]
for key in ("lastAcceptedImplementation", "activeImplementation", "completedModulePlan", "acceptedImplementationHistory", "previousCompletedModulePlan"):
    assert before[key] == after[key], key
path.write_bytes((json.dumps(after, indent=2, ensure_ascii=False) + "\n").encode("utf-8"))

md = ROOT / "docs/unity/IMPLEMENTATION_MAP.md"
text = md.read_text(encoding="utf-8-sig")
old_gate = next(line for line in text.splitlines() if line.startswith("**Current development gate:**"))
new_gate = "**Current development gate:** INT-05-ADMITTED-COMMAND-AND-CHOICE-SURFACE is selected for source/API design by actual GPT response `e5e0261e-f693-5c9c-92f3-1be2225d25bf` and Codex concurrence. Complete HC-01–05 and the exact operation/profile/payload/source/evidence inventory before runtime implementation. The static census is 78 command candidates across 24 startup factories plus two separate operator kinds; it is not executable coverage. [Selected module and open contract](evidence/2026-11-23-int05-admitted-command-surface/MODULE_DEFINITION.md). The detailed FND-02, MGT-02, INT-04 and INT-05 rows retain their existing whole-workstream statuses while recording later accepted scope."
text = text.replace(old_gate, new_gate, 1)
for ident, scope in updates.items():
    start = text.index("#### " + ident + " ")
    end = text.find("\n#### ", start + 1)
    if end < 0:
        end = len(text)
    section = text[start:end]
    old_scope = next(line for line in section.splitlines() if line.startswith("**Implemented / accepted scope:**"))
    section = section.replace(old_scope, "**Implemented / accepted scope:** " + scope)
    old_evidence = next(line for line in section.splitlines() if line.startswith("**Evidence:"))
    section = section.replace(old_evidence, old_evidence + " · [Later accepted modules and exact qualification](evidence/2026-11-23-mgt02-connected-work-control/ACCEPTANCE_EVIDENCE_MATRIX.md)")
    text = text[:start] + section + text[end:]
md.write_bytes(text.encode("utf-8"))

handoff = ROOT / "docs/unity/DEVELOPMENT_HANDOFF.md"
text = handoff.read_text(encoding="utf-8-sig")
marker = "# Decennium C# gameplay simulation handoff\n"
assert text.startswith(marker)
notice = "\nCurrent successor design (2026-11-23): **INT-05 admitted command and choice surface is selected for source/API design.** Actual GPT recommendation `e5e0261e-f693-5c9c-92f3-1be2225d25bf` and Codex concurrence follow accepted MGT-02. [Definition and criteria](evidence/2026-11-23-int05-admitted-command-surface/MODULE_DEFINITION.md), [proposed HC-01–05 contract](evidence/2026-11-23-int05-admitted-command-surface/SOURCE_API_CONTRACT.md). The 78-command/24-factory/two-operator census is static; exact source/profile/payload/witness dispositions remain open. No new runtime or test has started. Obtain actual agreement before implementation; preserve all accepted modules, 49 workstreams/120 edges/100 obligations and the full C# mandate. Unity, storage cleanup and Support remain deferred. Earlier entries below retain historical status at their original checkpoints.\n"
handoff.write_bytes((marker + notice + text[len(marker):]).encode("utf-8"))
report = {
    "baseline": BASELINE, "status": "DOCUMENTATION_ONLY_ACTUAL_SELECTION_AND_ACCEPTED_PROGRESS",
    "gptRecommendation": "e5e0261e-f693-5c9c-92f3-1be2225d25bf", "codexSelectionConcurred": True,
    "updatedDetailedRows": list(updates), "changedRowFields": ["implementedOrAcceptedScope", "evidence"],
    "workstreams": len(after["workItems"]), "dependencyEdges": sum(len(x["dependencies"]) for x in after["workItems"]),
    "completionCriteria": sum(len(x["completionCriteria"]) for x in after["workItems"]),
    "allOriginalCriteriaDependenciesStatusesAndWholeFlagsPreserved": True,
    "readinessAndCompletionContractUnchanged": True, "priorAcceptanceRecordsUnchanged": True,
    "sourceApiAccepted": False, "runtimeChanged": False, "testsOrBuildsExecuted": False, "unityAuthorized": False,
}
(PACKET / "MAP_SELECTION_RECONCILIATION.json").write_bytes((json.dumps(report, indent=2) + "\n").encode("utf-8"))
print(json.dumps(report))
