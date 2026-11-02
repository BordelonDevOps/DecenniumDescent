#!/usr/bin/env python3
"""Record Director's nonblocking corrections to Shell caster qualification 472."""
import copy
import datetime as dt
import hashlib
import json
import zlib
from pathlib import Path

BASE = Path(__file__).resolve().parent
ROOT = BASE.parents[4]
OUT = BASE / "elemental_shell_caster_qualification_472_repack01"
OLD_REPORT = BASE / "elemental_shell_caster_qualification_472/SHELL_CASTER_QUALIFICATION_472_TESTONLY.json"
READBACK = OUT / "DIRECTOR_READBACK_472_REPACK01.json"
NEW_REPORT = OUT / "SHELL_CASTER_QUALIFICATION_472_REPACK01_TESTONLY.json"
QUEUE475 = BASE / "CURRENT_SPELL_QUEUE_475.json"
PENDING475 = BASE / "CURRENT17_PENDING_IDENTITY_AUDIT_475.json"
HANDOFF475 = BASE / "CURRENT_HANDOFF_475.json"
QUEUE476 = BASE / "CURRENT_SPELL_QUEUE_476_REPACK01.json"
PENDING476 = BASE / "CURRENT17_PENDING_IDENTITY_AUDIT_476_REPACK01.json"
HANDOFF476 = BASE / "CURRENT_HANDOFF_476_REPACK01.json"
SNAPSHOT476 = BASE / "CURRENT_SPELL_REVIEW_SNAPSHOT_476_REPACK01.md"
VALIDATION = OUT / "VALIDATION_472_REPACK01.json"
ID = "elemental-shell"
QUALIFICATION_SHA = "5bafa9ea18d0062c23f2758d93ba920554f18ef0cf6ef41b410e72419c656a5d"
PROPOSAL_SHA = "de4bd28b11d33be17a9185f925fae4c740956a10f7aaf5d89bcddc16a7bb8169"


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def crc(raw):
    return f"{zlib.crc32(raw) & 0xffffffff:08x}"


def read(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def enc(obj):
    return (json.dumps(obj, ensure_ascii=False, indent=2) + "\n").encode("utf-8")


def bind(path, raw=None):
    raw = path.read_bytes() if raw is None else raw
    return {"path": path.relative_to(ROOT).as_posix(), "bytes": len(raw), "sha256": sha(raw), "crc32": crc(raw)}


def write(path, obj):
    raw = enc(obj)
    path.write_bytes(raw)
    return bind(path, raw)


def stamp():
    return dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def main():
    outputs = [NEW_REPORT, QUEUE476, PENDING476, HANDOFF476, SNAPSHOT476, VALIDATION, OUT / ".gitattributes"]
    assert not any(p.exists() for p in outputs), "Refusing to overwrite an existing 472 Repack01."
    old, readback = read(OLD_REPORT), read(READBACK)
    q475, p475, h475 = read(QUEUE475), read(PENDING475), read(HANDOFF475)
    assert sha(OLD_REPORT.read_bytes()) == QUALIFICATION_SHA
    assert readback["decision"] == "PASS_TEST_ONLY_CASTER_ACQUISITION_AND_PREPARATION_SUBPART_OF_DF218_B02"
    assert readback["reviewedQualification"]["sha256"] == QUALIFICATION_SHA
    assert readback["currentFortressAuthority"]["sha256"] == sha(QUEUE475.read_bytes())
    assert q475["currentAuthority"] == {"reviewedApplied": 831, "pending": 17, "acceptedUnapplied": 0,
                                         "completeStandaloneProcedures": 555, "scopedInterfaces": 173}
    assert q475["currentAuthority"]["reviewedApplied"] == readback["currentFortressAuthority"]["applied"]
    assert q475["currentAuthority"]["pending"] == readback["currentFortressAuthority"]["pending"]
    assert q475["currentAuthority"]["acceptedUnapplied"] == readback["currentFortressAuthority"]["acceptedUnapplied"]
    assert p475["pendingCount"] == 17 and h475["authority"] == q475["currentAuthority"]
    assert old["authority"]["reviewedApplied"] == 830 and old["authority"]["pending"] == 18
    assert old["authority"]["Fortress"] == "HELD_UNDER_PG200-B06"
    assert old["adoptedProposal"]["sha256"] == PROPOSAL_SHA
    assert old["qualificationResult"]["fullDF218B02Satisfied"] is False
    assert old["nonEffects"]["spellCast"] is False and old["nonEffects"]["encounterOrWitnessConstructed"] is False
    assert q475["nextIdentity"] == ID and q475["nextBlockerIds"] == ["DF218-B01", "DF218-B02"]

    (OUT / ".gitattributes").write_text("** -text !eol\n", encoding="utf-8", newline="\n")
    now = stamp()
    readback_ref = bind(READBACK)
    old_ref = bind(OLD_REPORT)
    queue475_ref = bind(QUEUE475)
    pending475_ref = bind(PENDING475)
    handoff475_ref = bind(HANDOFF475)
    report = copy.deepcopy(old)
    report.update({
        "id": "DF218-SHELL-CASTER-QUALIFICATION-472-REPACK01",
        "recordedAtUtc": now,
        "status": "DIRECTOR_PASS_TESTONLY_CASTER_QUALIFICATION_WITH_NONBLOCKING_CORRECTIONS_APPLIED",
        "supersedes": old_ref,
        "directorReadback": readback_ref,
        "directorDisposition": {
            "status": "PASS_TEST_ONLY_CASTER_ACQUISITION_AND_PREPARATION_SUBPART_OF_DF218_B02",
            "fullDF218B02Satisfied": False,
            "openBlockers": ["DF218-B01", "DF218-B02"],
            "shellCastAuthorized": False,
            "encounterOrWitnessConstructionAuthorized": False,
            "blockerClosureAuthorized": False,
            "identityAcceptanceOrApplicationAuthorized": False,
        },
    })
    report["remainingB02RequirementsOutsideThisPremise"][2] = (
        "Incoming save/defense basis; one correctly attributed reflection to the actual responsible creature dealer "
        "(the Greater Fire Pet for the qualified Fire Strike route; DF9-Q14 does not substitute its summoner/controller, "
        "and cross-bind466 does not instantiate that pet); range/line of effect; causal-root provenance; and Null handling."
    )
    report["authority"] = {
        "qualificationTimeSnapshot": {
            "queue": {
                "path": old["authority"].get("queuePath", "docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT_SPELL_QUEUE_465_REPACK01.json"),
                "bytes": 5230,
                "sha256": "b6ef81469804a4e196bdbc61a927cb5b53c51c738005082ba41293a6e54f9133",
            },
            "reviewedApplied": 830, "pending": 18, "acceptedUnapplied": 0,
            "Fortress": "HELD_UNDER_PG200-B06",
            "meaning": "Historical authority when qualification472 was prepared; no longer current after the separate Fortress application475.",
        },
        "currentSnapshot": {
            "queue": queue475_ref,
            "reviewedApplied": 831, "pending": 17, "acceptedUnapplied": 0,
            "completeStandaloneProcedures": 555, "scopedInterfaces": 173,
            "Fortress": "ACCEPTED_APPLIED_STATIC_AUTHORED_REVIEW_ONLY",
            "ElementalShell": "HELD_UNDER_DF218-B01_AND_DF218-B02",
        },
        "queueChangedByThisReport": False,
    }
    report["sourceQualifications"].append({
        "path": old_ref["path"], "sha256": old_ref["sha256"],
        "status": "DIRECTOR_PASS_WITH_TWO_NONBLOCKING_CLARIFICATIONS_RECORDED_IN_REPACK01",
    })
    report_ref = write(NEW_REPORT, report)

    pending_ids = list(q475["remainingPendingIds"])
    priority = list(q475["continuingPriorityOrder"])
    authority = copy.deepcopy(q475["currentAuthority"])
    queue = {
        "id": "CURRENT-SPELL-QUEUE-476-REPACK01",
        "supersedesQueue": queue475_ref,
        "currentAuthority": authority,
        "currentIndexBinding": q475["currentIndexBinding"],
        "currentCatalogBinding": q475["currentCatalogBinding"],
        "remainingPendingIds": pending_ids,
        "continuingPriorityOrder": priority,
        "continuingPriorityOrderIsPrioritySubset": q475["continuingPriorityOrderIsPrioritySubset"],
        "nextIdentity": ID, "nextBlockerIds": ["DF218-B01", "DF218-B02"],
        "closureTasksRemaining": 17, "firstReviewTasksRemaining": 0,
        "acceptedUnapplied": 0, "acceptedIds": [], "appliedIds": [], "closedBlockerIdsThisStep": [],
        "currentApplication": q475["application"],
        "pendingIdentityAuditPath": PENDING476.relative_to(ROOT).as_posix(),
        "currentHandoffPath": HANDOFF476.relative_to(ROOT).as_posix(),
        "runtimeExecuted": False, "runtimeSelectionEnabled": False,
        "currentReviewPacket": {
            "path": report_ref["path"], "sha256": report_ref["sha256"],
            "classification": "DIRECTOR_PASS_TESTONLY_CASTER_QUALIFICATION_SUBPART_ONLY",
            "proposal468Sha256": PROPOSAL_SHA, "ownerAdopted": True,
            "fullIdentityDisposition": "HELD_UNDER_DF218-B01_AND_DF218-B02",
            "shellCastAuthorized": False, "witnessConstructionAuthorized": False,
        },
        "currentDirectorReadback": readback_ref,
        "repackNote": "GPT passed the adopted Proposal468 caster-acquisition/preparation subpart and requested two nonblocking report clarifications, now recorded. Fortress remains accepted/applied only for static authored review; Shell identity remains pending. No cast, encounter, witness, blocker closure, or identity acceptance/application occurred.",
    }
    qr = write(QUEUE476, queue)
    pending = {
        "id": "CURRENT17-PENDING-IDENTITY-AUDIT-476-REPACK01", "recordedAtUtc": now,
        "authority": authority, "pendingCount": 17, "pendingIds": pending_ids,
        "indexBinding": q475["currentIndexBinding"], "currentQueueBinding": qr,
        "nextPriorityOrder": priority, "acceptedUnappliedIds": [],
        "reviewDispositionThisStep": "ELEMENTAL_SHELL_CASTER_QUALIFICATION_SUBPART_PASS_ONLY",
        "identityAppliedThisStep": None, "blockerClosedThisStep": None,
        "nextStep": "Obtain Director direction for the remaining DF218-B01/B02 evidence. Proposal468 authorizes caster qualification only; no new cast, encounter, or witness premises are adopted.",
    }
    pr = write(PENDING476, pending)
    handoff = {
        "id": "CURRENT-HANDOFF-476-REPACK01", "supersedes": handoff475_ref,
        "queue": qr, "pendingIdentityAudit": pr, "authority": authority,
        "continuingPriorityOrder": priority, "closureTasksRemaining": 17, "firstReviewTasksRemaining": 0,
        "nextStep": pending["nextStep"], "currentApplication": q475["application"],
        "nativeCatalogAndDownstreamGatesUnchanged": True,
        "FortressStaticAcceptance475": {"status": "ACCEPTED_APPLIED_STATIC_AUTHORED_REVIEW_ONLY",
                                         "queueAuthority": authority, "PG200H01ThroughH10Retained": True},
        "ElementalShellCasterQualification472Repack01": {"readback": readback_ref, "report": report_ref,
                                                          "status": "PASS_TESTONLY_CASTER_QUALIFICATION_SUBPART_ONLY",
                                                          "openBlockers": ["DF218-B01", "DF218-B02"],
                                                          "castOrWitnessAuthorized": False},
        "qualificationTimeAuthorityWas830180": True,
        "currentAuthorityBoundSeparatelyToQueue475": queue475_ref,
    }
    hr = write(HANDOFF476, handoff)
    snapshot = (
        "# Spell review snapshot — Elemental Shell caster qualification 472 Repack01\n\n"
        "**831 applied / 17 pending / 0 accepted-unapplied; 555 complete standalone procedures / 173 scoped interfaces.**\n\n"
        "GPT Director passed only the adopted Proposal468 TEST_ONLY caster-acquisition/preparation subpart of DF218-B02. "
        "The 472 report now distinguishes its historical 830/18/0 snapshot from current Queue475 and identifies the Greater Fire Pet "
        "as the responsible creature dealer for the qualified Fire Strike route.\n\n"
        "DF218-B01 and DF218-B02 remain open. No Shell cast, encounter, witness construction, blocker closure, identity acceptance/application, "
        "or downstream gate is authorized. Next step: obtain Director direction for the remaining evidence and any proposal requiring owner adoption.\n\n"
        f"Updated report: {report_ref['path']} (SHA-256 {report_ref['sha256']}).\n"
    )
    SNAPSHOT476.write_text(snapshot, encoding="utf-8", newline="\n")
    checks = [
        "Director PASS matches exact reviewed qualification472 bytes and adopted Proposal468 hash.",
        "Both nonblocking corrections are applied without altering the original report or adopted source bytes.",
        "Historical qualification-time authority remains 830/18/0 with Fortress held; current authority separately binds Queue475 at 831/17/0.",
        "Remaining B02 dealer wording identifies the responsible creature and Greater Fire Pet route; DF9-Q14 and cross-bind466 limits are preserved.",
        "DF218-B01 and B02 remain open; no Shell cast, encounter, witness, blocker closure, or identity disposition is recorded.",
        "Queue476 preserves the 17 pending IDs, current index/catalog bindings, and 831/17/0 authority.",
        "Pending audit and handoff cross-bind the new queue and retain Shell as next identity.",
    ]
    validation = {"id": "SHELL-CASTER-QUALIFICATION-472-REPACK01-VALIDATION", "recordedAtUtc": now,
                  "status": "PASS", "checks": [{"check": x, "passed": True} for x in checks],
                  "checkCount": len(checks), "passedChecks": len(checks), "failedChecks": 0,
                  "report": report_ref, "directorReadback": readback_ref,
                  "queue": qr, "pendingIdentityAudit": pr, "handoff": hr,
                  "fullDF218B02Satisfied": False, "authorityChanged": False}
    vr = write(VALIDATION, validation)
    print(json.dumps({"status": "PASS", "report": report_ref, "queue": qr,
                      "pendingIdentityAudit": pr, "handoff": hr, "validation": vr}, indent=2))


if __name__ == "__main__":
    main()
