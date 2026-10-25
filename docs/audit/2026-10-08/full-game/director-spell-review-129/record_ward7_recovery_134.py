from pathlib import Path
import datetime, hashlib, json

D = Path(__file__).parent.resolve(); G = Path(r"C:\Github\DecenniumDescent")
sha = lambda b: hashlib.sha256(b).hexdigest()
def bind(p):
    p = Path(p).resolve(); b = p.read_bytes()
    try: label = p.relative_to(G).as_posix()
    except ValueError: label = str(p)
    return {"path": label, "bytes": len(b), "sha256": sha(b)}

receipt = {
    "id": "WARD7-RECOVERY-REQUEST-134",
    "recordedAtUtc": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="microseconds"),
    "status": "INTERRUPTED_STREAM_STOPPED_SAVED_WORK_RECOVERY_SENT",
    "conversationId": "6adc506d-8770-83ea-b64c-0345d9b9b682",
    "currentCounts": {"appliedReviewed": 648, "pending": 200, "acceptedUnapplied": 0},
    "interruptedAfter": "4m 39s; UI showed Connection interrupted. Waiting for the complete answer.",
    "existingOutputArtifacts": ["DD_Rank7Perception5_Director_Return01_134.zip", "DD_Rank7Perception5_Director_Return01_134_DELIVERY.json"],
    "savedWard7ReturnArtifactAvailable": False,
    "savedWorkspaceInspection": {
        "proceduresForSevenIdentitiesPresent": True,
        "sharedRulesAndNativeAccessPresent": True,
        "actorProfilesAndPreservedEvidencePresent": True,
        "serializedCasesPresent": False,
        "questionDispositionsPresent": False,
        "validationReportPresent": False,
        "finalZipPresent": False,
        "priorCaseDraftStoppedAtSyntaxErrorBeforeWritingCaseData": True,
        "originalQuestions": 20,
        "followupQuestions": 6,
        "totalQuestionDispositionsRequired": 26,
        "requiredNewCases": 14,
        "separateUnassignedProfileAnalyses": 2,
    },
    "assistantAcknowledgement": "The saved workspace contains all seven procedure files, shared rules, native/access records, actor profiles and preserved evidence. It has no serialized Ward7 cases, question dispositions, validation report or final ZIP. The prior case draft stopped at a syntax error before writing case data; I’ll preserve it without executing it. The saved request also requires six followups alongside the 20 original questions, for 26 dispositions total.",
    "latestDirectorProgress": "Preserve saved procedures/evidence byte-for-byte; author only case data, all 26 dispositions, validation and packaging. Corruption Immunity positive case remains conditional unless a supplied source other than Venom Rain supports it; Venom Rain applies Poisoned.",
    "currentBuildStatus": {"mainCasesAuthored": 14, "branchesAuthored": 6, "questionDispositionsAuthored": 26, "sourceSemanticAndStateTransitionValidation": "in_progress", "finalPackageReady": False, "armorOfFaithCorrection": "Saved prose said +2 AC; accepted source card says +3 AC. Director will preserve saved bytes and record correction explicitly."},
    "userInstruction": "Resume the existing saved Ward7 workspace; inspect saved procedures, cases, questions and validations; preserve completed work; complete only missing steps; do not rerun source builders or repeat cases; return the complete data-only ZIP and delivery manifest; do not accept or apply; continue the remaining queue.",
    "freshContext": bind(D / "DD_Rank7Perception5_Applied_Ward7_Context_134.zip"),
    "visibleRequestVerified": True,
    "assistantRunActive": True,
    "acceptanceOrApplicationByDirector": False,
}
path = D / "WARD7_RECOVERY_REQUEST_134.json"
path.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
for name in ["CURRENT_SPELL_QUEUE_134.json", "CURRENT_HANDOFF_134.json"]:
    p = D / name; obj = json.loads(p.read_text(encoding="utf-8-sig"))
    obj["ward7RecoveryRequest"] = bind(path)
    obj["lastUpdatedAtUtc"] = receipt["recordedAtUtc"]
    if name == "CURRENT_HANDOFF_134.json":
        obj["ward7Handoff"]["recoveryReceipt"] = bind(path)
        obj["ward7Handoff"]["lastObservedStatus"] = "Saved-work recovery active; procedures and evidence preserved byte-for-byte; 14 cases, 26 question dispositions, validation and packaging remain to be built."
        obj["ward7Handoff"]["latestDirectorProgress"] = "Corruption Immunity positive case remains conditional unless a supplied source other than Venom Rain supports it; Venom Rain applies Poisoned."
    p.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps({"receipt": bind(path), "queue": bind(D / "CURRENT_SPELL_QUEUE_134.json"), "handoff": bind(D / "CURRENT_HANDOFF_134.json")}, indent=2))
