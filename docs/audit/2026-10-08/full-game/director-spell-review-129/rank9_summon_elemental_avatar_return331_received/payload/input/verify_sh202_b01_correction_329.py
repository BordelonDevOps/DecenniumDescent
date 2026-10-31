from __future__ import annotations
import json, pathlib
from datetime import datetime, timezone

HERE = pathlib.Path(__file__).resolve().parent
DELTA = json.loads((HERE / "SH202_B01_CORRECTION_DELTA_329.json").read_text(encoding="utf-8"))
checks = []
def ck(name, ok, detail=None):
    checks.append({"check": name, "passed": bool(ok), "detail": detail})
    if not ok: raise AssertionError(f"{name}: {detail}")
cases = {row["id"]: row for row in DELTA["conditionalCases"]}
ck("exactly six focused conditional test fixtures", len(cases) == 6 and all(row["fixtureStatus"] == "CONDITIONAL_AUTHORED_REVIEW_INPUT_NOT_GAMEPLAY" for row in cases.values()), len(cases))
c1 = cases["SH329-C01-conditional-extra-turn-strike-cap"]
ck("conditional full-turn input grants no fourth strike or reset", c1["expected"] == {"fourthStrikeAccepted": False, "attemptedStrikesAfter": 3, "ownerAllowanceReset": False, "newDamageRootCreated": False, "budgetReset": False} and c1["conditionalInput"]["sourceAcquired"] is False, c1["expected"])
c2 = cases["SH329-C02-conditional-typed-fire-force-components"]
ck("damage components stay typed and separate through resistance", c2["expected"]["fireAfterResistance"] == 3 and c2["expected"]["forceAfterResistance"] == 8 and c2["expected"]["totalAppliedOnce"] == 11 and c2["expected"]["componentRootsRemainDistinct"] is True and c2["conditionalInput"]["sourceBinding"] is None, c2["expected"])
c3 = cases["SH329-C03-conditional-different-source-controller-transition"]
ck("controller transition preserves owner and strike budget", c3["transition"]["sourceOwnerBefore"] == c3["transition"]["sourceOwnerAfter"] == "owner-A" and c3["expected"]["thirdStrikeAccepted"] is True and c3["expected"]["fourthStrikeAccepted"] is False and c3["expected"]["strikeCapReset"] is False, c3["expected"])
c4 = cases["SH329-C04-same-family-aura-arbitration"]
ck("aura arbitration applies one greatest pool and consumes the losing due marker", c4["expected"]["appliedPool"] == 10 and c4["expected"]["packetsApplied"] == 1 and c4["expected"]["loserDueOpportunityConsumed"] is True and c4["expected"]["laterReplay"] is False and c4["expected"]["tieWinner"] == "earlier-application-then-sourceId", c4["expected"])
c5 = cases["SH329-C05-outside-initiative-exposure-transition"]
ck("outside-initiative clock survives initiative entry without immediate pulse", c5["expected"]["pulseAtInitiativeEntry"] is False and c5["expected"]["dueMarkerAfterEntrySeconds"] == 6 and c5["expected"]["pulseCountAtSixSeconds"] == 1 and c5["expected"]["extraTurnPulse"] is False, c5["expected"])
c6 = cases["SH329-C06-local-aura-and-rider-only-suppression"]
ck("local and rider suppression do not delete body, reset command, or replay pulses", c6["expected"]["sourceBodyPersists"] is True and c6["expected"]["strikeAttemptsAfter"] == 1 and c6["expected"]["ownerBudgetChanged"] is False and c6["expected"]["missedLocalPulseReplayed"] is False and c6["expected"]["riderSuppressionRemovesBody"] is False, c6["expected"])
ck("current authority is unchanged and the spell remains unaccepted pending Director decision", DELTA["authorityBefore"] == DELTA["authorityAfter"] and DELTA["authorityBefore"]["pending"] == 25 and DELTA["authorityBefore"]["acceptedUnapplied"] == 0 and DELTA["status"] == "FOCUSED_CONDITIONAL_CORRECTION_READY_FOR_DIRECTOR_REVIEW", DELTA["authorityAfter"])
ck("no canon, runtime, or actual gameplay claim is made", DELTA["provenance"] == {"conditionalFixturesAreGameplay": False, "userAuthorshipClaim": False, "canonicalMutation": False, "runtimeExecuted": False}, DELTA["provenance"])
result = {"id":"SH202-B01-CORRECTION-329-INDEPENDENT-AUDIT", "recordedAtUtc":datetime.now(timezone.utc).isoformat(timespec="seconds"), "status":"PASS" if all(row["passed"] for row in checks) else "FAIL", "checks":checks, "checkCount":len(checks), "passedChecks":sum(row["passed"] for row in checks), "failedChecks":sum(not row["passed"] for row in checks), "acceptedIds":[], "appliedIds":[], "scopeIds":["summon-elemental-avatar"], "blockerIds":["SH202-B01"], "runtimeExecuted":False, "canonicalFilesChanged":False}
(HERE / "SH202_B01_CORRECTION_AUDIT_329.json").write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
print(json.dumps({"status":result["status"],"checks":result["checkCount"],"passed":result["passedChecks"],"failed":result["failedChecks"]},indent=2))
