from __future__ import annotations

import hashlib
import json
import zipfile
import zlib
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath

ROOT = Path(r"C:\Github\DecenniumDescent-review-push-134")
BASE = ROOT / "docs/audit/2026-10-08/full-game/director-spell-review-129"
RETURN_DIR = BASE / "rank9_castingcost5_return240_received"
RETURN_ZIP = RETURN_DIR / "DD_Rank9_UnholyAscendance_Director_Return240_HELD.zip"
DELIVERY = RETURN_DIR / "DD_Rank9_UnholyAscendance_Director_Return240_HELD_DELIVERY.json"
SOURCE_DIR = BASE / "rank9_castingcost5_current_source_240_prepared"
SOURCE_ZIP = SOURCE_DIR / "DD_Rank9_CastingCost5_CurrentSource_240.zip"
SOURCE_DELIVERY = SOURCE_DIR / "DD_Rank9_CastingCost5_CurrentSource_240_DELIVERY.json"
SOURCE_PREP = BASE / "RANK9_CASTINGCOST5_SOURCE_PREPARATION_240.json"
TARGET = "unholy-ascendance"
NEXT = {"group": "rank9-memory-denial6", "pendingIds": ["mind-collapse", "unravel-identity"]}
AUTH = {"reviewedApplied": 811, "pending": 37, "acceptedUnapplied": 0,
        "completeStandaloneProcedures": 535, "scopedInterfaces": 173}


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def crc(raw: bytes) -> str:
    return f"{zlib.crc32(raw) & 0xffffffff:08x}"


def readj(path: Path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def enc(value) -> str:
    return json.dumps(value, ensure_ascii=False, indent=2) + "\n"


def info(path: Path) -> dict:
    raw = path.read_bytes()
    return {"path": path.relative_to(ROOT).as_posix(), "bytes": len(raw), "sha256": sha(raw), "crc32": crc(raw)}


def safe_member(name: str) -> bool:
    path = PurePosixPath(name)
    return bool(name) and "\\" not in name and not path.is_absolute() and all(part not in ("", ".", "..") for part in path.parts)


def main() -> None:
    checks: list[dict] = []

    def check(name: str, passed: bool, details=None) -> None:
        checks.append({"id": name, "passed": bool(passed), "details": details})
        if not passed:
            raise AssertionError(f"Audit check failed: {name}: {details}")

    now = datetime.now(timezone.utc).isoformat()
    delivery = readj(DELIVERY)
    source_delivery = readj(SOURCE_DELIVERY)
    preparation = readj(SOURCE_PREP)
    return_info, delivery_info = info(RETURN_ZIP), info(DELIVERY)
    source_info = info(SOURCE_ZIP)

    check("downloaded return bytes match sidecar size/SHA/CRC",
          all(return_info[key] == delivery["archive"][key] for key in ("bytes", "sha256", "crc32")), return_info)
    check("sealed sidecar binds Return240, current authority and exact source packet",
          delivery["id"] == "RETURN240-DELIVERY" and delivery["sourceAuthority"] == AUTH and
          delivery["sourceArchive"] == {"path": "DD_Rank9_CastingCost5_CurrentSource_240.zip",
              "bytes": source_info["bytes"], "sha256": source_info["sha256"], "crc32": source_info["crc32"]} and
          all(source_info[key] == preparation["packet"][key] == source_delivery["archive"][key]
              for key in ("bytes", "sha256", "crc32")), {"source": source_info, "authority": delivery["sourceAuthority"]})

    with zipfile.ZipFile(RETURN_ZIP) as archive, zipfile.ZipFile(SOURCE_ZIP) as source_archive:
        names = archive.namelist()
        expected_rows = {row["path"]: row for row in delivery["members"]}
        internal_manifest = json.loads(archive.read("MEMBER_MANIFEST.json"))
        internal_rows = {row["path"]: row for row in internal_manifest["members"]}
        check("ZIP integrity, safe unique names and exact 59-member scope",
              archive.testzip() is None and len(names) == len(set(names)) == delivery["memberCount"] == 59 and
              all(safe_member(name) for name in names), {"members": len(names)})
        check("external and internal member manifests reconcile",
              delivery["payloadMemberCount"] == internal_manifest["payloadMemberCount"] == 58 and
              set(expected_rows) == set(names) and set(internal_rows) == set(names) - {"MEMBER_MANIFEST.json"} and
              set(expected_rows) == set(internal_rows) | {"MEMBER_MANIFEST.json"},
              {"external": len(expected_rows), "internal": len(internal_rows), "zip": len(names)})
        member_errors = []
        for name, row in expected_rows.items():
            raw = archive.read(name)
            if {"bytes": len(raw), "sha256": sha(raw), "crc32": crc(raw)} != {key: row[key] for key in ("bytes", "sha256", "crc32")}:
                member_errors.append(name)
        check("all 59 ZIP members match sidecar size/SHA/CRC", not member_errors, member_errors[:10])
        internal_errors = []
        for name, row in internal_rows.items():
            raw = archive.read(name)
            if {"bytes": len(raw), "sha256": sha(raw), "crc32": crc(raw)} != {key: row[key] for key in ("bytes", "sha256", "crc32")}:
                internal_errors.append(name)
        check("all 58 payload members match internal manifest", not internal_errors, internal_errors[:10])

        decision = json.loads(archive.read("DIRECTOR_DECISION.json"))
        counts = json.loads(archive.read("COUNTS.json"))
        source_binding = json.loads(archive.read("SOURCE_BINDING.json"))
        hold_register = json.loads(archive.read("HOLD_REGISTER.json"))
        semantic = json.loads(archive.read("INDEPENDENT_SEMANTIC_FAILURE_CHECK.json"))
        validation = json.loads(archive.read("VALIDATION.json"))
        integrity = json.loads(archive.read("INTEGRITY_CHECK.json"))
        clock = json.loads(archive.read("CLOCK_CHECK.json"))
        source_check = json.loads(archive.read("SOURCE_CHECK.json"))
        preservation = json.loads(archive.read("PRESERVATION_CHECK.json"))
        case_names = sorted(name for name in names if name.startswith("cases/") and name.endswith(".json"))
        cases = [json.loads(archive.read(name)) for name in case_names]

        check("only unholy-ascendance was reviewed and remains unapplied/held",
              delivery["accepted"] is False and delivery["applied"] is False and delivery["acceptedIds"] == [] and
              delivery["appliedIds"] == [] and delivery["heldIds"] == [TARGET] and
              decision["scope"] == [TARGET] and decision["accepted"] is False and decision["applied"] is False and
              decision["acceptedIds"] == [] and decision["appliedIds"] == [] and decision["heldIds"] == [TARGET] and
              len(decision["decisions"]) == 1 and decision["decisions"][0]["spellId"] == TARGET and
              decision["decisions"][0]["blockerIds"] == ["CC194-B04"],
              {"accepted": delivery["acceptedIds"], "applied": delivery["appliedIds"], "held": delivery["heldIds"]})
        expected_quals = ["CC194-H01", "CC194-H02", "CC194-H07", "CC194-H08"]
        expected_linked = ["CC194-H05", "CC194-H06"]
        check("CC194-B04 and all eight retained qualification IDs match the sealed ruling",
              delivery["blockerIds"] == ["CC194-B04"] and decision["blockerIds"] == ["CC194-B04"] and
              delivery["conditionalQualificationIds"] == decision["conditionalQualificationIds"] == expected_quals and
              delivery["linkedQuestionQualificationIds"] == decision["linkedQuestionQualificationIds"] == expected_linked and
              hold_register["currentBlockers"][0]["id"] == "CC194-B04" and
              hold_register["targetConditionalQualificationIds"] == expected_quals and
              hold_register["linkedQuestionConditionalQualificationIds"] == expected_linked and
              len(hold_register["retainedAllCC194Qualifications"]) == 8,
              {"blocker": delivery["blockerIds"], "conditional": delivery["conditionalQualificationIds"], "linked": delivery["linkedQuestionQualificationIds"]})
        check("exact next pending group is Memory/Denial6",
              delivery["nextPendingGroup"]["group"] == NEXT["group"] and
              delivery["nextPendingGroup"]["pendingIds"] == NEXT["pendingIds"] and
              decision["nextPendingGroup"] == delivery["nextPendingGroup"], delivery["nextPendingGroup"])

        events = sum(len(case.get("events", [])) for case in cases)
        check("case files and event/operation totals reconcile",
              len(case_names) == len(cases) == counts["preservedCases"] == delivery["counts"]["preservedCases"] == 11 and
              all(case.get("spellId") == TARGET for case in cases) and
              events == counts["events"] == delivery["counts"]["events"] == 317 and
              counts["forwardOperations"] == counts["inverseOperations"] == 634 and
              counts["eventOperations"] == 1268 and counts["acceptedIds"] == counts["appliedIds"] == 0 and counts["heldIds"] == 1 and
              delivery["counts"] == counts and validation["counts"] == counts and decision["counts"] == counts,
              {"cases": len(cases), "events": events, "forward": counts["forwardOperations"], "inverse": counts["inverseOperations"]})
        check("all reported replay, preservation, semantic and packaging checks pass structurally",
              all(report["failureCount"] == 0 and report["checkCount"] == len(report["checks"]) and
                  all(item.get("pass", False) for item in report["checks"])
                  for report in (integrity, clock, source_check, preservation, semantic)) and
              semantic["status"] == "HELD_CC194_B04" and validation["status"] == "DATA_PASS_SEMANTIC_HOLD" and
              delivery["packageValidation"]["status"] == "PASS" and delivery["packageValidation"]["failureCount"] == 0 and
              all(item.get("pass", False) for item in delivery["packageValidation"]["checks"]),
              {"integrity": integrity["checkCount"], "clock": clock["checkCount"], "source": source_check["checkCount"],
               "preservation": preservation["checkCount"], "semantic": semantic["status"],
               "packageValidation": delivery["packageValidation"]["checkCount"]})

        candidate = json.loads(source_archive.read("CURRENT_SOURCE_CONFERENCE_CANDIDATE_240.json"))
        source_manifest = json.loads(source_archive.read("MANIFEST.json"))
        source_member_rows = {row["path"]: row for row in source_manifest["members"]}
        candidate_rows = {"sources_current/" + row["path"]: row for row in candidate["sourceBindings"]}
        return_rows = {row["path"]: row for row in source_binding["currentSourceBindings"]}
        source_errors = []
        if len(candidate_rows) != 117 or len(return_rows) != 117:
            source_errors.append("source-binding-count")
        if set(candidate_rows) != set(return_rows):
            source_errors.append("source-binding-path-set")
        for name, candidate_row in candidate_rows.items():
            returned_row = return_rows.get(name)
            archive_row = source_member_rows.get(name)
            if returned_row is None or archive_row is None:
                source_errors.append(name)
                continue
            raw = source_archive.read(name)
            local = (ROOT / Path(*PurePosixPath(name.removeprefix("sources_current/")).parts)).read_bytes()
            if not (len(raw) == candidate_row["bytes"] == returned_row["bytes"] == archive_row["bytes"] == len(local) and
                    sha(raw) == candidate_row["sha256"] == returned_row["sha256"] == archive_row["sha256"] == sha(local) and
                    crc(raw) == returned_row["crc32"] == archive_row["crc32"] == crc(local)):
                source_errors.append(name)
        check("all 117 current source bindings match candidate, packet, manifest, return and working tree",
              len(candidate_rows) == len(return_rows) == 117 and not source_errors,
              {"candidate": len(candidate_rows), "returned": len(return_rows), "errors": source_errors[:10]})
        snapshot = source_binding["snapshot"]
        source_snapshot = preparation["sourceSnapshot"]
        check("return snapshot agrees with Packet240 main branch, commit and current indexes",
              snapshot["branch"] == source_snapshot["branch"] == "main" and
              snapshot["headCommit"] == source_snapshot["headCommit"] and
              snapshot["indexBinding"] == source_snapshot["indexBinding"] and
              snapshot["catalogBinding"] == source_snapshot["catalogBinding"] and
              source_binding["sourceAuthority"] == AUTH and source_binding["sourceArchiveIncluded"] is False,
              {"branch": snapshot["branch"], "headCommit": snapshot["headCommit"]})

        # The compact return keeps selected historical decision files. Verify them against the local sealed archives.
        old222 = BASE / "rank9_castingcost5_return222_received/DD_Rank9_CastingCost2_Director_Return222.zip"
        old239 = BASE / "rank9_timefate6_return239_received/DD_Rank9_TimeFate4_Director_Return239_HELD.zip"
        carried_errors = []
        with zipfile.ZipFile(old222) as z222, zipfile.ZipFile(old239) as z239:
            expected = {
                "prior222/DIRECTOR_DECISION.json": (z222, "DIRECTOR_DECISION.json"),
                "prior222/HOLD_REGISTER.json": (z222, "HOLD_REGISTER.json"),
                "prior222/MEMBER_MANIFEST.json": (z222, "MEMBER_MANIFEST.json"),
                "prior222/SOURCE_ANCHORS.json": (z222, "SOURCE_ANCHORS.json"),
                "prior222/procedures/unholy-ascendance.json": (z222, "procedures/unholy-ascendance.json"),
                "prior239/DIRECTOR_DECISION.json": (z239, "DIRECTOR_DECISION.json"),
                "prior239/HOLD_REGISTER.json": (z239, "HOLD_REGISTER.json"),
            }
            for member, (prior, prior_member) in expected.items():
                if archive.read(member) != prior.read(prior_member):
                    carried_errors.append(member)
        check("prior Return222 unholy decision and Return239 holds are preserved byte-exactly",
              not carried_errors, carried_errors)
        check("decision explicitly preserves accepted/application and downstream gates",
              decision["acceptedIds"] == decision["appliedIds"] == [] and
              decision["canonicalChanges"] is False and decision["runtimeExecuted"] is False and
              decision["suppliedProgramsExecuted"] is False and
              any("canonical application" in item for item in delivery["qualifications"]),
              {"canonicalChanges": decision["canonicalChanges"], "runtimeExecuted": decision["runtimeExecuted"]})

    audit_path = BASE / "RANK9_CASTINGCOST5_RETURN240_INDEPENDENT_AUDIT.json"
    audit = {
        "id": "RANK9-CASTINGCOST5-RETURN240-INDEPENDENT-AUDIT",
        "recordedAtUtc": now,
        "status": "PASS_PACKAGE_BINDING_AND_SCOPE; UNHOLY_ASCENDANCE_HELD_CC194_B04",
        "returnArchive": return_info,
        "deliveryManifest": delivery_info,
        "sourcePacket": source_info,
        "sourceDeliveryManifest": info(SOURCE_DELIVERY),
        "sourceAuthority": AUTH,
        "reviewedIds": [TARGET],
        "acceptedIds": [],
        "appliedIds": [],
        "heldIds": [TARGET],
        "blockerIds": ["CC194-B04"],
        "nextPendingGroup": NEXT,
        "checkCount": len(checks),
        "checksPassed": sum(row["passed"] for row in checks),
        "checksFailed": sum(not row["passed"] for row in checks),
        "checks": checks,
        "limitations": [
            "Independently checked the downloaded return and delivery bytes, all 59 members, exact scope and ruling, current authority and source-packet binding, all 117 refreshed source files, carried Return222/Return239 decisions, and reported check-record consistency.",
            "Reported replay totals and individual reported integrity/clock/source/preservation checks were checked for internal consistency; GPT-supplied replay code was not executed and the 317-event semantic replay was not independently reproduced."
        ],
    }
    audit_path.write_text(enc(audit), encoding="utf-8", newline="\n")
    receipt_path = BASE / "RANK9_CASTINGCOST5_RETURN240_RECEIPT.json"
    receipt = {
        "id": "RANK9-CASTINGCOST5-DIRECTOR-RETURN-240-RECEIPT",
        "recordedAtUtc": now,
        "status": "UNHOLY_ASCENDANCE_HELD; RETURN_ARCHIVE_AND_SOURCE_BINDINGS_INDEPENDENTLY_VERIFIED",
        "reviewedIds": [TARGET], "acceptedIds": [], "appliedIds": [], "heldIds": [TARGET],
        "blockers": {TARGET: {"blockerIds": ["CC194-B04"],
            "minimumMissingWitnesses": decision["decisions"][0]["minimumMissingWitnesses"],
            "conditionalQualificationIds": ["CC194-H01", "CC194-H02", "CC194-H07", "CC194-H08"],
            "linkedQuestionQualificationIds": ["CC194-H05", "CC194-H06"]}},
        "sourceAuthority": AUTH, "sourcePacket": source_info,
        "directorReturn": return_info, "deliveryManifest": delivery_info,
        "counts": counts,
        "independentAudit": {"path": audit_path.relative_to(ROOT).as_posix(),
                             "checkCount": len(checks), "checksFailed": 0},
        "nextGroup": NEXT["group"], "nextPendingIds": NEXT["pendingIds"],
        "canonicalFilesModified": False, "githubModified": False, "runtimeExecuted": False,
    }
    receipt_path.write_text(enc(receipt), encoding="utf-8", newline="\n")

    print(json.dumps({"status": audit["status"], "checksPassed": audit["checksPassed"],
                      "checksFailed": audit["checksFailed"], "return": return_info,
                      "sourceBindingsVerified": 117, "nextPendingGroup": NEXT}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
