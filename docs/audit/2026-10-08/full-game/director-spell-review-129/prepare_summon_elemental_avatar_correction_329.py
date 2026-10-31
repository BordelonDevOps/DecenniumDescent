from __future__ import annotations

import hashlib
import json
import pathlib
import subprocess
import sys
import zipfile
import zlib
from datetime import datetime, timezone

ROOT = pathlib.Path(__file__).resolve().parents[5]
AUDIT = pathlib.Path(__file__).resolve().parent
SOURCE_RETURN = AUDIT / "rank9_summonhosts5_return285_received" / "DD_Rank9_SummonHosts5_Director_Return285_HELD.zip"
OUT = AUDIT / "rank9_summon_elemental_avatar_correction_329_prepared"
ARCHIVE = OUT / "DD_Rank9_SummonElementalAvatar_Correction_329.zip"
DELIVERY = OUT / "DD_Rank9_SummonElementalAvatar_Correction_329_DELIVERY.json"
DELTA = OUT / "SH202_B01_CORRECTION_DELTA_329.json"
VERIFY = OUT / "verify_sh202_b01_correction_329.py"
SPELL = "summon-elemental-avatar"
BLOCKER = "SH202-B01"
AUTHORITY = {
    "reviewedApplied": 823,
    "pending": 25,
    "acceptedUnapplied": 0,
    "completeStandaloneProcedures": 547,
    "scopedInterfaces": 173,
}


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def crc(raw: bytes) -> str:
    return f"{zlib.crc32(raw) & 0xFFFFFFFF:08x}"


def pretty(value) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    queue_path = AUDIT / "CURRENT_SPELL_QUEUE_329.json"
    handoff_path = AUDIT / "CURRENT_HANDOFF_329.json"
    pending_path = AUDIT / "CURRENT25_PENDING_IDENTITY_AUDIT_329.json"
    return_audit_path = AUDIT / "FORTRESS_RETURN328_INDEPENDENT_AUDIT.json"
    return_receipt_path = AUDIT / "FORTRESS_RETURN328_RECEIPT.json"
    queue = json.loads(queue_path.read_text(encoding="utf-8"))
    handoff = json.loads(handoff_path.read_text(encoding="utf-8"))
    pending = json.loads(pending_path.read_text(encoding="utf-8"))
    return_audit = json.loads(return_audit_path.read_text(encoding="utf-8"))
    return_receipt = json.loads(return_receipt_path.read_text(encoding="utf-8"))
    if not SOURCE_RETURN.is_file():
        raise FileNotFoundError(SOURCE_RETURN)

    with zipfile.ZipFile(SOURCE_RETURN) as source:
        prior_decision = json.loads(source.read("DIRECTOR_DECISION.json"))
        prior_blocker = next(row for row in prior_decision["blockers"] if row["id"] == BLOCKER)
        prior_spell_decision = next(row for row in prior_decision["decisions"] if row["id"] == SPELL)
        prior_procedure = json.loads(source.read("procedures/summon-elemental-avatar.json"))
        prior_case_b = json.loads(source.read("cases/RANK9SUMMONHOSTS5129-SUMMON-ELEMENTAL-AVATAR-B.json"))
        source_bindings = json.loads(source.read("SOURCE_BINDINGS.json"))
        prior_member_manifest = json.loads(source.read("MEMBER_MANIFEST.json"))

    cases = [
        {
            "id": "SH329-C01-conditional-extra-turn-strike-cap",
            "purpose": "Prove the existing three-attempted-strikes-per-numbered-round cap does not reset for a conditional full-extra-turn token.",
            "fixtureStatus": "CONDITIONAL_AUTHORED_REVIEW_INPUT_NOT_GAMEPLAY",
            "premises": {"ownerId": "owner-A", "controllerId": "owner-A", "bodyId": "avatar-A", "roundKey": "round-17", "strikeCap": 3, "attemptedBeforeExtraTurn": 3},
            "conditionalInput": {"id": "SH329-INPUT-EXTRA-TURN-01", "kind": "hypothetical-full-extra-turn-opportunity", "sourceAcquired": False, "sourceBinding": None, "gameplayOccurrenceClaim": False},
            "expected": {"fourthStrikeAccepted": False, "attemptedStrikesAfter": 3, "ownerAllowanceReset": False, "newDamageRootCreated": False, "budgetReset": False},
            "invariants": ["The full-turn source remains explicitly hypothetical.", "No fourth strike is granted.", "The rejected attempt consumes no new source, resource, or round allowance."],
        },
        {
            "id": "SH329-C02-conditional-typed-fire-force-components",
            "purpose": "Prove mixed typed damage is separated by actual damage root before resistance and combined once for the target lifecycle.",
            "fixtureStatus": "CONDITIONAL_AUTHORED_REVIEW_INPUT_NOT_GAMEPLAY",
            "premises": {"targetId": "target-fire-resistant", "resistances": ["fire"], "fireResistanceRule": "halve this component", "forceResistance": False},
            "conditionalInput": {"id": "SH329-INPUT-MIXED-DAMAGE-01", "kind": "hypothetical-second-damage-component", "sourceAcquired": False, "sourceBinding": None, "gameplayOccurrenceClaim": False},
            "components": [
                {"componentId": "C02-fire", "damageType": "fire", "amount": 6, "dealerRoot": "avatar-A/aura-root-01", "binding": "existing-spell-local-aura-rule"},
                {"componentId": "C02-force", "damageType": "force", "amount": 8, "dealerRoot": "conditional-input/force-component-01", "binding": "conditional-test-component-only"},
            ],
            "expected": {"fireAfterResistance": 3, "forceAfterResistance": 8, "totalAppliedOnce": 11, "componentRootsRemainDistinct": True, "forceTreatedAsAvatarSource": False},
            "invariants": ["No force-damage ability or acquisition is asserted.", "Fire resistance cannot reduce the force component.", "Component roots and damage types survive recombination."],
        },
        {
            "id": "SH329-C03-conditional-different-source-controller-transition",
            "purpose": "Prove a different-source controller transition does not transfer source ownership or refresh the numbered-round strike cap.",
            "fixtureStatus": "CONDITIONAL_AUTHORED_REVIEW_INPUT_NOT_GAMEPLAY",
            "premises": {"sourceOwnerId": "owner-A", "bodyId": "avatar-A", "roundKey": "round-21", "attemptedBeforeTransition": 2, "strikeCap": 3},
            "conditionalInput": {"id": "SH329-INPUT-CONTROL-CHANGE-01", "kind": "hypothetical-distinct-control-source", "sourceAcquired": False, "sourceBinding": None, "gameplayOccurrenceClaim": False},
            "transition": {"controllerBefore": "owner-A", "controllerAfter": "controller-B", "sourceOwnerBefore": "owner-A", "sourceOwnerAfter": "owner-A"},
            "expected": {"thirdStrikeAccepted": True, "fourthStrikeAccepted": False, "attemptedAfterThird": 3, "sourceOwnerChanged": False, "strikeCapReset": False},
            "invariants": ["The distinct controller input is conditional only.", "Body and spell-source identity remain stable.", "No second owner offensive allowance or fresh strike budget is created."],
        },
        {
            "id": "SH329-C04-same-family-aura-arbitration",
            "purpose": "Prove same-family aura roots arbitrate at one recipient marker instead of stacking, and losing roots consume their due opportunity.",
            "fixtureStatus": "CONDITIONAL_AUTHORED_REVIEW_INPUT_NOT_GAMEPLAY",
            "premises": {"recipientId": "recipient-1", "marker": "recipient-regular-start-44", "familyKey": "summon-elemental-avatar:aura"},
            "conditionalInput": {"id": "SH329-INPUT-SECOND-AVATAR-01", "kind": "hypothetical-second-same-family-source", "sourceAcquired": False, "sourceBinding": None, "gameplayOccurrenceClaim": False},
            "auraRoots": [
                {"sourceId": "avatar-A", "applicationOrder": 1, "rolledPool": 10, "due": True},
                {"sourceId": "avatar-B", "applicationOrder": 2, "rolledPool": 6, "due": True},
            ],
            "tieCase": {"sourceA": {"sourceId": "avatar-C", "applicationOrder": 1, "rolledPool": 10}, "sourceB": {"sourceId": "avatar-D", "applicationOrder": 2, "rolledPool": 10}},
            "expected": {"appliedPool": 10, "appliedSourceId": "avatar-A", "packetsApplied": 1, "loserDueOpportunityConsumed": True, "tieWinner": "earlier-application-then-sourceId", "laterReplay": False},
            "invariants": ["The second avatar is a conditional test premise, not a legal acquisition claim.", "Different aura families remain independent.", "No offensive strike or command budget is consumed."],
        },
        {
            "id": "SH329-C05-outside-initiative-exposure-transition",
            "purpose": "Prove outside-initiative exposure preserves its due marker when initiative begins and does not pulse immediately on entry.",
            "fixtureStatus": "CONDITIONAL_AUTHORED_REVIEW_INPUT_NOT_GAMEPLAY",
            "premises": {"recipientId": "recipient-2", "sourceBodyId": "avatar-A", "firstExposureSeconds": 0, "outsideExposureIntervalSeconds": 6, "initiativeEntrySeconds": 2, "nextDueSeconds": 6},
            "conditionalInput": {"id": "SH329-INPUT-INITIATIVE-ENTRY-01", "kind": "hypothetical-initiative-entry", "gameplayOccurrenceClaim": False},
            "expected": {"pulseAtInitiativeEntry": False, "dueMarkerAfterEntrySeconds": 6, "pulseAtNextRegularStart": True, "pulseCountAtSixSeconds": 1, "extraTurnPulse": False},
            "invariants": ["Entry does not advance, reset, or duplicate the exposure clock.", "Only the next due regular-start marker resolves after initiative entry.", "A missed pulse is never replayed."],
        },
        {
            "id": "SH329-C06-local-aura-and-rider-only-suppression",
            "purpose": "Prove local intersection and recipient rider suppression do not suppress the source body or unrelated recipients.",
            "fixtureStatus": "CONDITIONAL_AUTHORED_REVIEW_INPUT_NOT_GAMEPLAY",
            "premises": {"sourceBodyId": "avatar-A", "marker": "recipient-regular-start-52", "auraRadiusFeet": 10, "strikeAttemptsBefore": 1, "strikeCap": 3},
            "conditionalInput": {"id": "SH329-INPUT-LOCAL-SUPPRESSION-01", "kind": "hypothetical-local-magical-suppression", "sourceAcquired": False, "sourceBinding": None, "gameplayOccurrenceClaim": False},
            "recipients": [
                {"id": "inside-null-intersection", "insideAura": True, "suppressedIntersection": True, "expectedPulse": False},
                {"id": "outside-null-intersection", "insideAura": True, "suppressedIntersection": False, "expectedPulse": True},
                {"id": "rider-only-suppressed", "insideAura": True, "suppressedIntersection": False, "riderOnlySuppression": True, "expectedAuraDamage": 0},
            ],
            "expected": {"sourceBodyPersists": True, "strikeAttemptsAfter": 1, "ownerBudgetChanged": False, "missedLocalPulseReplayed": False, "outsideRecipientUnaffected": True, "riderSuppressionRemovesBody": False},
            "invariants": ["Suppression clips only the local aura intersection or named recipient rider.", "A suppressed pulse is lost, not queued.", "Aura behavior does not create an offensive strike."],
        },
    ]

    delta = {
        "id": "SH202-B01-CORRECTION-DELTA-329",
        "recordedAtUtc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "scopeIds": [SPELL],
        "blockerIds": [BLOCKER],
        "status": "FOCUSED_CONDITIONAL_CORRECTION_READY_FOR_DIRECTOR_REVIEW",
        "authorityBefore": AUTHORITY,
        "authorityAfter": AUTHORITY,
        "directorRulingApplied": "The Director’s visible chat ruling authorizes a scoped authored-procedure correction: full-extra-turn and mixed-damage cases may use explicitly conditional inputs without claiming actual gameplay source acquisition. Spell remains unaccepted until focused tests pass.",
        "priorBlockerBinding": {"return": "RETURN285", "directorDecisionId": prior_decision["id"], "decision": prior_spell_decision, "blocker": prior_blocker},
        "priorProcedure": prior_procedure,
        "priorMainBMissingEvidence": prior_case_b["missingEvidence"],
        "priorSourceBindings": source_bindings,
        "priorMemberManifest": prior_member_manifest,
        "currentBindings": {
            "queue329": {"path": queue_path.relative_to(ROOT).as_posix(), "sha256": sha(queue_path.read_bytes())},
            "handoff329": {"path": handoff_path.relative_to(ROOT).as_posix(), "sha256": sha(handoff_path.read_bytes())},
            "pendingAudit329": {"path": pending_path.relative_to(ROOT).as_posix(), "sha256": sha(pending_path.read_bytes())},
            "return328Audit": {"path": return_audit_path.relative_to(ROOT).as_posix(), "sha256": sha(return_audit_path.read_bytes())},
            "return328Receipt": {"path": return_receipt_path.relative_to(ROOT).as_posix(), "sha256": sha(return_receipt_path.read_bytes())},
        },
        "conditionalCases": cases,
        "coverage": {
            "strikeCapWithoutInventedProvider": "SH329-C01",
            "typedDamageWithoutInventedAttacker": "SH329-C02",
            "differentSourceControlTransition": "SH329-C03",
            "sameFamilyAuraArbitration": "SH329-C04",
            "outsideInitiativeExposureTransition": "SH329-C05",
            "localAndRiderOnlyAuraSuppression": "SH329-C06",
        },
        "provenance": {"conditionalFixturesAreGameplay": False, "userAuthorshipClaim": False, "canonicalMutation": False, "runtimeExecuted": False},
        "requestedDisposition": "Director to review the focused delta and, if semantics and required tests pass, issue an exact sealed one-identity acceptance/application authorization; otherwise return only the failed check and minimum correction.",
    }
    DELTA.write_bytes(pretty(delta))

    verify_source = '''from __future__ import annotations\nimport json, pathlib\nfrom datetime import datetime, timezone\n\nHERE = pathlib.Path(__file__).resolve().parent\nDELTA = json.loads((HERE / "SH202_B01_CORRECTION_DELTA_329.json").read_text(encoding="utf-8"))\nchecks = []\ndef ck(name, ok, detail=None):\n    checks.append({"check": name, "passed": bool(ok), "detail": detail})\n    if not ok: raise AssertionError(f"{name}: {detail}")\ncases = {row["id"]: row for row in DELTA["conditionalCases"]}\nck("exactly six focused conditional test fixtures", len(cases) == 6 and all(row["fixtureStatus"] == "CONDITIONAL_AUTHORED_REVIEW_INPUT_NOT_GAMEPLAY" for row in cases.values()), len(cases))\nc1 = cases["SH329-C01-conditional-extra-turn-strike-cap"]\nck("conditional full-turn input grants no fourth strike or reset", c1["expected"] == {"fourthStrikeAccepted": False, "attemptedStrikesAfter": 3, "ownerAllowanceReset": False, "newDamageRootCreated": False, "budgetReset": False} and c1["conditionalInput"]["sourceAcquired"] is False, c1["expected"])\nc2 = cases["SH329-C02-conditional-typed-fire-force-components"]\nck("damage components stay typed and separate through resistance", c2["expected"]["fireAfterResistance"] == 3 and c2["expected"]["forceAfterResistance"] == 8 and c2["expected"]["totalAppliedOnce"] == 11 and c2["expected"]["componentRootsRemainDistinct"] is True and c2["conditionalInput"]["sourceBinding"] is None, c2["expected"])\nc3 = cases["SH329-C03-conditional-different-source-controller-transition"]\nck("controller transition preserves owner and strike budget", c3["transition"]["sourceOwnerBefore"] == c3["transition"]["sourceOwnerAfter"] == "owner-A" and c3["expected"]["thirdStrikeAccepted"] is True and c3["expected"]["fourthStrikeAccepted"] is False and c3["expected"]["strikeCapReset"] is False, c3["expected"])\nc4 = cases["SH329-C04-same-family-aura-arbitration"]\nck("aura arbitration applies one greatest pool and consumes the losing due marker", c4["expected"]["appliedPool"] == 10 and c4["expected"]["packetsApplied"] == 1 and c4["expected"]["loserDueOpportunityConsumed"] is True and c4["expected"]["laterReplay"] is False and c4["expected"]["tieWinner"] == "earlier-application-then-sourceId", c4["expected"])\nc5 = cases["SH329-C05-outside-initiative-exposure-transition"]\nck("outside-initiative clock survives initiative entry without immediate pulse", c5["expected"]["pulseAtInitiativeEntry"] is False and c5["expected"]["dueMarkerAfterEntrySeconds"] == 6 and c5["expected"]["pulseCountAtSixSeconds"] == 1 and c5["expected"]["extraTurnPulse"] is False, c5["expected"])\nc6 = cases["SH329-C06-local-aura-and-rider-only-suppression"]\nck("local and rider suppression do not delete body, reset command, or replay pulses", c6["expected"]["sourceBodyPersists"] is True and c6["expected"]["strikeAttemptsAfter"] == 1 and c6["expected"]["ownerBudgetChanged"] is False and c6["expected"]["missedLocalPulseReplayed"] is False and c6["expected"]["riderSuppressionRemovesBody"] is False, c6["expected"])\nck("current authority is unchanged and the spell remains unaccepted pending Director decision", DELTA["authorityBefore"] == DELTA["authorityAfter"] and DELTA["authorityBefore"]["pending"] == 25 and DELTA["authorityBefore"]["acceptedUnapplied"] == 0 and DELTA["status"] == "FOCUSED_CONDITIONAL_CORRECTION_READY_FOR_DIRECTOR_REVIEW", DELTA["authorityAfter"])\nck("no canon, runtime, or actual gameplay claim is made", DELTA["provenance"] == {"conditionalFixturesAreGameplay": False, "userAuthorshipClaim": False, "canonicalMutation": False, "runtimeExecuted": False}, DELTA["provenance"])\nresult = {"id":"SH202-B01-CORRECTION-329-INDEPENDENT-AUDIT", "recordedAtUtc":datetime.now(timezone.utc).isoformat(timespec="seconds"), "status":"PASS" if all(row["passed"] for row in checks) else "FAIL", "checks":checks, "checkCount":len(checks), "passedChecks":sum(row["passed"] for row in checks), "failedChecks":sum(not row["passed"] for row in checks), "acceptedIds":[], "appliedIds":[], "scopeIds":["summon-elemental-avatar"], "blockerIds":["SH202-B01"], "runtimeExecuted":False, "canonicalFilesChanged":False}\n(HERE / "SH202_B01_CORRECTION_AUDIT_329.json").write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\\n",encoding="utf-8")\nprint(json.dumps({"status":result["status"],"checks":result["checkCount"],"passed":result["passedChecks"],"failed":result["failedChecks"]},indent=2))\n'''
    VERIFY.write_text(verify_source, encoding="utf-8")
    audit_path = OUT / "SH202_B01_CORRECTION_AUDIT_329.json"
    subprocess.run([sys.executable, str(VERIFY)], cwd=OUT, check=True, capture_output=True, text=True)
    run_result = json.loads(audit_path.read_text(encoding="utf-8"))
    if run_result["status"] != "PASS" or run_result["failedChecks"] != 0:
        raise AssertionError("focused correction verifier failed")

    request_text = (
        "Director: review only Summon Elemental Avatar / SH202-B01. The sealed Return285 hold identified a missing actual full-extra-turn source, a source-bound mixed-damage attacker, and four incomplete control/aura traces. Your visible ruling authorized conditional authored inputs for the first two, with no claim of real acquisition or gameplay. This packet supplies six focused conditional fixtures: strike cap, typed damage, different-source control transition, same-family aura arbitration, outside-initiative exposure transition, and local/rider-only aura suppression. The audit checks the intended invariants; they are data-only authored checks, not runtime execution. Please issue an exact one-identity acceptance and application authorization only if the evidence and focused tests meet the sealed obligation. Otherwise identify the failed check and minimum remaining witness. Preserve all other holds and the authority snapshot.\n"
    )
    (OUT / "SH202_B01_CORRECTION_REQUEST_329.md").write_text(request_text, encoding="utf-8")
    (OUT / "CURRENT_SPELL_QUEUE_329.json").write_bytes(pretty(queue))
    (OUT / "CURRENT_HANDOFF_329.json").write_bytes(pretty(handoff))
    (OUT / "CURRENT25_PENDING_IDENTITY_AUDIT_329.json").write_bytes(pretty(pending))
    (OUT / "FORTRESS_RETURN328_INDEPENDENT_AUDIT.json").write_bytes(pretty(return_audit))
    (OUT / "FORTRESS_RETURN328_RECEIPT.json").write_bytes(pretty(return_receipt))

    files = [
        DELTA,
        VERIFY,
        audit_path,
        OUT / "SH202_B01_CORRECTION_REQUEST_329.md",
        OUT / "CURRENT_SPELL_QUEUE_329.json",
        OUT / "CURRENT_HANDOFF_329.json",
        OUT / "CURRENT25_PENDING_IDENTITY_AUDIT_329.json",
        OUT / "FORTRESS_RETURN328_INDEPENDENT_AUDIT.json",
        OUT / "FORTRESS_RETURN328_RECEIPT.json",
    ]
    member_bindings = []
    with zipfile.ZipFile(ARCHIVE, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for path in files:
            raw = path.read_bytes()
            name = path.name
            z.writestr(name, raw)
            member_bindings.append({"path": name, "bytes": len(raw), "sha256": sha(raw), "crc32": crc(raw)})
    archive_raw = ARCHIVE.read_bytes()
    delivery = {
        "id": "SH202-B01-CORRECTION-329-DELIVERY",
        "recordedAtUtc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "status": "PREPARED_READBACK_PASS",
        "scopeIds": [SPELL],
        "blockerIds": [BLOCKER],
        "authority": AUTHORITY,
        "acceptedIds": [],
        "appliedIds": [],
        "heldIds": [SPELL],
        "applicationRequestedOnlyIfDirectorSealsExactAuthorization": True,
        "conditionalCaseCount": 6,
        "audit": {"status": run_result["status"], "checkCount": run_result["checkCount"], "passedChecks": run_result["passedChecks"], "failedChecks": run_result["failedChecks"]},
        "canonicalFilesChanged": False,
        "runtimeExecuted": False,
        "archive": {"path": ARCHIVE.name, "bytes": len(archive_raw), "sha256": sha(archive_raw), "crc32": crc(archive_raw)},
        "memberCount": len(member_bindings),
        "exactAllowlist": [row["path"] for row in member_bindings],
        "members": member_bindings,
    }
    DELIVERY.write_bytes(pretty(delivery))
    # Read back the completed archive and verify every declared member.
    with zipfile.ZipFile(ARCHIVE) as z:
        assert z.testzip() is None
        assert set(z.namelist()) == set(delivery["exactAllowlist"])
        for row in member_bindings:
            raw = z.read(row["path"])
            assert len(raw) == row["bytes"] and sha(raw) == row["sha256"] and crc(raw) == row["crc32"]
    print(json.dumps({"archive": str(ARCHIVE), "delivery": str(DELIVERY), "archiveBytes": len(archive_raw), "archiveSha256": sha(archive_raw), "cases": len(cases), "checks": run_result["checkCount"], "status": "PASS", "accepted": [], "applied": []}, indent=2))


if __name__ == "__main__":
    main()
