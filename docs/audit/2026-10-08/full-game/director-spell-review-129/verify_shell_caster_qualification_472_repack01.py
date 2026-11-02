#!/usr/bin/env python3
"""Verify Shell qualification readback 472 Repack01 and the unchanged 17-identity authority."""
import hashlib
import json
import zlib
from pathlib import Path

BASE = Path(__file__).resolve().parent
ROOT = BASE.parents[4]
PKG = BASE / "elemental_shell_caster_qualification_472_repack01"
OLD = BASE / "elemental_shell_caster_qualification_472/SHELL_CASTER_QUALIFICATION_472_TESTONLY.json"
REPORT = PKG / "SHELL_CASTER_QUALIFICATION_472_REPACK01_TESTONLY.json"
READBACK = PKG / "DIRECTOR_READBACK_472_REPACK01.json"
QUEUE475 = BASE / "CURRENT_SPELL_QUEUE_475.json"
QUEUE476 = BASE / "CURRENT_SPELL_QUEUE_476_REPACK01.json"
PENDING476 = BASE / "CURRENT17_PENDING_IDENTITY_AUDIT_476_REPACK01.json"
HANDOFF476 = BASE / "CURRENT_HANDOFF_476_REPACK01.json"
CHECKS = []


def check(label, ok, detail=None):
    CHECKS.append({"check": label, "passed": bool(ok), **({"detail": detail} if detail is not None else {})})
    if not ok:
        raise AssertionError(f"FAIL: {label}: {detail}")


def read(p):
    return json.loads(p.read_text(encoding="utf-8-sig"))


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def crc(raw):
    return f"{zlib.crc32(raw) & 0xffffffff:08x}"


def bind(path, raw=None):
    raw = path.read_bytes() if raw is None else raw
    return {"path": path.relative_to(ROOT).as_posix(), "bytes": len(raw), "sha256": sha(raw), "crc32": crc(raw)}


def main():
    old, report, rb = read(OLD), read(REPORT), read(READBACK)
    q475, q476 = read(QUEUE475), read(QUEUE476)
    pending, handoff = read(PENDING476), read(HANDOFF476)
    check("Director readback passes only caster acquisition/preparation", rb["decision"] == "PASS_TEST_ONLY_CASTER_ACQUISITION_AND_PREPARATION_SUBPART_OF_DF218_B02"
          and report["directorDisposition"]["fullDF218B02Satisfied"] is False)
    check("Readback identifies exact reviewed qualification472 bytes", rb["reviewedQualification"]["sha256"] == sha(OLD.read_bytes())
          and rb["reviewedQualification"]["sha256"] == "5bafa9ea18d0062c23f2758d93ba920554f18ef0cf6ef41b410e72419c656a5d")
    check("Original qualification472 artifact remains unchanged", report["supersedes"]["sha256"] == sha(OLD.read_bytes()))
    check("Proposal468 and owner adoption remain exactly bound", report["adoptedProposal"]["sha256"] == "de4bd28b11d33be17a9185f925fae4c740956a10f7aaf5d89bcddc16a7bb8169"
          and report["ownerAdoption"]["proposalSha256"] == report["adoptedProposal"]["sha256"])
    check("Current authority is separated from the historical 830/18/0 snapshot",
          report["authority"]["qualificationTimeSnapshot"]["reviewedApplied"] == 830
          and report["authority"]["qualificationTimeSnapshot"]["pending"] == 18
          and report["authority"]["qualificationTimeSnapshot"]["acceptedUnapplied"] == 0
          and report["authority"]["qualificationTimeSnapshot"]["Fortress"] == "HELD_UNDER_PG200-B06"
          and report["authority"]["currentSnapshot"]["queue"] == bind(QUEUE475))
    check("Current authority follows Queue475 at 831/17/0 with static-only Fortress status",
          report["authority"]["currentSnapshot"]["reviewedApplied"] == 831
          and report["authority"]["currentSnapshot"]["pending"] == 17
          and report["authority"]["currentSnapshot"]["acceptedUnapplied"] == 0
          and report["authority"]["currentSnapshot"]["Fortress"] == "ACCEPTED_APPLIED_STATIC_AUTHORED_REVIEW_ONLY")
    correction = report["remainingB02RequirementsOutsideThisPremise"][2]
    check("Dealer correction names responsible creature and Greater Fire Pet route",
          "actual responsible creature dealer" in correction and "Greater Fire Pet" in correction
          and "DF9-Q14" in correction and "cross-bind466" in correction
          and "actual Avatar dealer" not in correction)
    check("Qualification preparation facts remain unchanged", report["adoptedPremise"]["hypotheticalPreparation"]["uninterruptedDurationSeconds"] == 2700
          and report["adoptedPremise"]["hypotheticalPreparation"]["preparedOrdinaryCount"] == 24
          and report["adoptedPremise"]["hypotheticalPreparation"]["divinationOnlyPosition"].startswith("UNASSIGNED"))
    check("Both B01 and B02 remain open", report["directorDisposition"]["openBlockers"] == ["DF218-B01", "DF218-B02"])
    check("No cast, encounter, witness, blocker closure, or identity disposition authorized",
          report["directorDisposition"]["shellCastAuthorized"] is False
          and report["directorDisposition"]["encounterOrWitnessConstructionAuthorized"] is False
          and report["directorDisposition"]["blockerClosureAuthorized"] is False
          and report["directorDisposition"]["identityAcceptanceOrApplicationAuthorized"] is False
          and report["nonEffects"]["spellCast"] is False
          and report["nonEffects"]["encounterOrWitnessConstructed"] is False)
    check("Queue476 preserves 831/17/0 authority and the pending identity set",
          q476["currentAuthority"] == q475["currentAuthority"]
          and q476["remainingPendingIds"] == q475["remainingPendingIds"]
          and q476["nextIdentity"] == "elemental-shell"
          and q476["nextBlockerIds"] == ["DF218-B01", "DF218-B02"])
    check("Queue476 reports a caster-subpart pass without closing the spell identity",
          q476["currentReviewPacket"]["classification"] == "DIRECTOR_PASS_TESTONLY_CASTER_QUALIFICATION_SUBPART_ONLY"
          and q476["currentReviewPacket"]["shellCastAuthorized"] is False
          and q476["currentReviewPacket"]["witnessConstructionAuthorized"] is False)
    check("Queue, pending audit, and handoff bind consistently",
          pending["currentQueueBinding"] == bind(QUEUE476)
          and handoff["queue"] == bind(QUEUE476)
          and handoff["pendingIdentityAudit"] == bind(PENDING476)
          and pending["authority"] == q476["currentAuthority"] == handoff["authority"])
    check("Application and native source/catalog state remain unchanged", q476["currentApplication"] == q475["application"]
          and q476["runtimeSelectionEnabled"] is False and q476["runtimeExecuted"] is False)
    check("Readback, report, queue, pending audit, and handoff exist",
          all(p.is_file() for p in [READBACK, REPORT, QUEUE476, PENDING476, HANDOFF476]))

    result = {"id": "SHELL-CASTER-QUALIFICATION-472-REPACK01-INDEPENDENT-VALIDATION",
              "status": "PASS", "checksPassed": len(CHECKS), "checksFailed": 0,
              "qualificationSha256": sha(REPORT.read_bytes()), "authority": q476["currentAuthority"],
              "checks": CHECKS}
    result_path = PKG / "INDEPENDENT_VALIDATION_472_REPACK01.json"
    result_bytes = (json.dumps(result, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    result_path.write_bytes(result_bytes)
    result_ref = bind(result_path, result_bytes)
    handoff["independentValidation472Repack01"] = result_ref
    handoff_bytes = (json.dumps(handoff, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    HANDOFF476.write_bytes(handoff_bytes)
    print(json.dumps({**result, "validationBinding": result_ref, "handoffSha256": sha(handoff_bytes)}, indent=2))


if __name__ == "__main__":
    main()
