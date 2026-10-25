from pathlib import Path
import hashlib, json, zipfile

G = Path(r"C:\Github\DecenniumDescent")
D = Path(__file__).parent.resolve()
P = G / "docs/audit/2026-10-08/full-game/DD_Ward7_Director_Conference_128.zip"
RECEIPT = G / "docs/audit/2026-10-08/full-game/director-spell-review-128/WARD7_PACKET_128.json"
packet_receipt = json.loads(RECEIPT.read_text(encoding="utf-8-sig"))
raw = P.read_bytes(); sha = hashlib.sha256(raw).hexdigest()
assert len(raw) == packet_receipt["archive"]["bytes"] and sha == packet_receipt["archive"]["sha256"]
with zipfile.ZipFile(P) as z:
    q = json.loads(z.read("INDEPENDENT_QUESTIONS_128.json"))
    manifest = json.loads(z.read("MANIFEST.json"))
expectations = {
    "id": "WARD7-RETURN-EXPECTATIONS-134",
    "status": "SOURCE_BOUND_EXPECTATIONS_READY_FOR_RETURN_AUDIT",
    "sourcePacket": {"path": P.relative_to(G).as_posix(), "bytes": len(raw), "sha256": sha},
    "identities": q["identities"],
    "originalQuestions": q["completeOriginalQuestionsUnchanged"],
    "followupQuestions": q["focusedAdditionalQuestions"],
    "allQuestions": q["allQuestions"],
    "questionIds": [x["id"] for x in q["allQuestions"]],
    "requiredNewCases": q["requiredNewCases"],
    "requiredNewCaseIds": [x["id"] for x in q["requiredNewCases"]],
    "separateUnassignedProfileEvidence": q["separateUnassignedProfileEvidence"],
    "sourceBoundaryRequirements": q["originalFutureCaseRequirementsUnchanged"],
    "sourceChecks": q["sourceChecks"],
    "packetManifestBindings": manifest["files"],
    "runtimeExecuted": False,
    "sourceProgramsExecuted": False,
}
out = D / "WARD7_RETURN_EXPECTATIONS_134.json"
out.write_text(json.dumps(expectations, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps({"path": str(out), "bytes": out.stat().st_size, "sha256": hashlib.sha256(out.read_bytes()).hexdigest(), "identities": len(expectations["identities"]), "questions": len(expectations["allQuestions"]), "cases": len(expectations["requiredNewCases"]), "unassignedProfileAnalyses": len(expectations["separateUnassignedProfileEvidence"])}, indent=2))
