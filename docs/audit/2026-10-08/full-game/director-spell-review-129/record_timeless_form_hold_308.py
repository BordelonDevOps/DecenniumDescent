from __future__ import annotations

import copy
import datetime as dt
import hashlib
import json
import pathlib
import zlib
import zipfile

ROOT = pathlib.Path.cwd()
A = ROOT / "docs/audit/2026-10-08/full-game/director-spell-review-129"
RETURN_DIR = A / "rank9_defenseform8_return308_received"
RETURN_ZIP = RETURN_DIR / "DD_Rank9_DefenseForm8_Director_Return308_HELD.zip"
RETURN_DELIVERY = RETURN_DIR / "DD_Rank9_DefenseForm8_Director_Return308_HELD_DELIVERY.json"
PACKET_ZIP = A / "rank9_defenseform8_current_source_308_prepared/DD_Rank9_DefenseForm8_CurrentSource_308.zip"
INDEX = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json"
CATALOG = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json"
QUEUE_308 = A / "CURRENT_SPELL_QUEUE_308.json"
HANDOFF_308 = A / "CURRENT_HANDOFF_308.json"
PENDING_307 = A / "CURRENT26_PENDING_IDENTITY_AUDIT_307.json"
AUTH = {"reviewedApplied": 822, "pending": 26, "acceptedUnapplied": 0,
        "completeStandaloneProcedures": 546, "scopedInterfaces": 173}
ORDER = [
    "alignment-ascension", "alignment-perfection", "astral-projection", "banishment-gate",
    "collapse-timeline", "conjure-demiplane-fortress", "corruption-purification",
    "divine-intervention-greater", "elemental-shell", "eternal-prophecy", "faction-incarnate",
    "faction-omniscience-supreme", "faction-perfection", "fate-rewrite", "final-word",
    "imprisonment", "invulnerable-sphere", "nullification-wave", "reality-anchor",
    "reverse-gravity-field", "summon-avatar-of-decay", "summon-elemental-avatar",
    "summon-herald-of-the-planes", "time-stop", "timeless-form", "wish",
]
DIRECTOR_TEXT = (
    "HOLD — timeless-form / DF218-B03. acceptedIds=[]; appliedIds=[]; heldIds=[timeless-form]. "
    "The missing dependency is an accepted operational Time Stop procedure, a legally acquired caster "
    "with complete activation history, and a complete joint encounter demonstrating Timeless Form’s "
    "promised exclusion. The preserved joint case remains held; no positive trace or obligation revision "
    "was introduced. All 87 source bindings verified. The 11 preserved cases replayed: 238 events, "
    "476 forward and 476 inverse operations. Numerical replay does not close the missing witness. "
    "Authority remains 822 applied / 26 pending / 0 accepted-unapplied, with 546 procedures / 173 "
    "interfaces. Final Word, Elemental Shell, and all unrelated holds remain unchanged. Next: "
    "invulnerable-sphere / DF218-B04, followed by nullification-wave. Nothing applied or changed canonically."
)


def raw(path: pathlib.Path) -> bytes:
    return path.read_bytes()


def read(path: pathlib.Path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def ref(path: pathlib.Path, data: bytes | None = None) -> dict:
    b = raw(path) if data is None else data
    return {"path": path.relative_to(ROOT).as_posix(), "bytes": len(b),
            "sha256": hashlib.sha256(b).hexdigest(), "crc32": f"{zlib.crc32(b) & 0xffffffff:08x}"}


def write(path: pathlib.Path, obj) -> bytes:
    b = (json.dumps(obj, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    path.write_bytes(b)
    return b


def check(label: str, ok: bool, detail: str = "") -> dict:
    return {"check": label, "passed": bool(ok), "detail": detail}


def main() -> None:
    stamp = dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")
    delivery = read(RETURN_DELIVERY)
    archive_raw = raw(RETURN_ZIP)
    digest = hashlib.sha256(archive_raw).hexdigest()
    crc = f"{zlib.crc32(archive_raw) & 0xffffffff:08x}"
    findings: list[dict] = []
    findings.append(check("return archive outer byte/hash/CRC binding",
                          len(archive_raw) == delivery["archive"]["bytes"]
                          and digest == delivery["archive"]["sha256"]
                          and crc == delivery["archive"]["crc32"],
                          f"{len(archive_raw)} bytes; SHA-256 {digest}; CRC32 {crc}"))
    with zipfile.ZipFile(RETURN_ZIP) as rz:
        names = rz.namelist()
        name_set = set(names)
        findings.append(check("return ZIP integrity, unique safe names and member count",
                              len(names) == len(name_set) == delivery["memberCount"] == 40
                              and all(not pathlib.PurePosixPath(n).is_absolute() and ".." not in pathlib.PurePosixPath(n).parts for n in names)
                              and rz.testzip() is None,
                              f"{len(names)} members; testzip passed"))
        findings.append(check("outer exact allowlist and member bindings",
                              set(delivery["exactAllowlist"]) == name_set
                              and {x["path"] for x in delivery["members"]} == name_set
                              and len(delivery["members"]) == len(name_set),
                              "all return members are listed exactly once"))
        member_manifest = json.loads(rz.read("MEMBER_MANIFEST.json"))
        manifest_row = delivery["memberManifest"]
        manifest_bytes = rz.read("MEMBER_MANIFEST.json")
        findings.append(check("member manifest binding and self-exclusion",
                              len(manifest_bytes) == manifest_row["bytes"]
                              and hashlib.sha256(manifest_bytes).hexdigest() == manifest_row["sha256"]
                              and f"{zlib.crc32(manifest_bytes) & 0xffffffff:08x}" == manifest_row["crc32"]
                              and member_manifest["selfExcluded"] is True
                              and member_manifest["memberCountExcludingSelf"] == 39
                              and member_manifest["scopeIds"] == ["timeless-form"],
                              "MEMBER_MANIFEST.json binds 39 non-self members"))
        expected_member_rows = {x["path"]: x for x in delivery["members"]}
        manifest_member_rows = {x["path"]: x for x in member_manifest["members"]}
        member_ok = set(expected_member_rows) - {"MEMBER_MANIFEST.json"} == set(manifest_member_rows)
        for path, row in expected_member_rows.items():
            b = rz.read(path)
            actual = {"bytes": len(b), "sha256": hashlib.sha256(b).hexdigest(),
                      "crc32": f"{zlib.crc32(b) & 0xffffffff:08x}"}
            expected = {k: row[k] for k in actual}
            member_ok &= actual == expected
            if path != "MEMBER_MANIFEST.json":
                member_ok &= actual == {k: manifest_member_rows[path][k] for k in actual}
        findings.append(check("all delivery and internal manifest payload hashes/CRCs",
                              member_ok, f"{len(expected_member_rows)} external and 39 internal payload rows checked"))

        decision = json.loads(rz.read("DIRECTOR_DECISION.json"))
        blockers = json.loads(rz.read("BLOCKERS.json"))
        counts = json.loads(rz.read("COUNTS.json"))
        source_bindings = json.loads(rz.read("SOURCE_BINDINGS.json"))
        next_group = json.loads(rz.read("NEXT_PENDING_GROUP.json"))
        validation = json.loads(rz.read("VALIDATION.json"))
        semantic = json.loads(rz.read("INDEPENDENT_SEMANTIC_FAILURE_CHECK.json"))
        findings.append(check("scope and exact Director disposition",
                              decision["scopeIds"] == ["timeless-form"]
                              and decision["acceptedIds"] == [] and decision["appliedIds"] == []
                              and decision["heldIds"] == ["timeless-form"]
                              and decision["decisions"][0]["decision"] == "HOLD"
                              and decision["decisions"][0]["blockerIds"] == ["DF218-B03"]
                              and delivery["acceptedIds"] == [] and delivery["appliedIds"] == []
                              and delivery["heldIds"] == ["timeless-form"]
                              and delivery["blockerIds"] == ["DF218-B03"],
                              "only Timeless Form held under DF218-B03"))
        findings.append(check("authority remains unchanged",
                              decision["authorityBefore"] == decision["authorityAfter"] == delivery["authority"] == AUTH,
                              json.dumps(AUTH, sort_keys=True)))
        findings.append(check("quantitative replay is accurately scoped",
                              counts["preservedCases"] == 11 and counts["events"] == 238
                              and counts["forwardOperations"] == counts["inverseOperations"] == 476
                              and counts["fullReverseTraversals"] == 11
                              and counts["newTraces"] == counts["newEvents"] == 0
                              and counts["mainCasesWithCompletePositiveJointTimeStopWitness"] == 0,
                              "replay checks do not constitute a positive Time Stop encounter"))
        findings.append(check("Director validation and semantic blocker agree",
                              validation["status"] == "PASS" and validation["failedCount"] == 0
                              and validation["checkCount"] == 5063
                              and semantic["decision"] == "HOLD"
                              and semantic["wholeIdentityComplete"] is False
                              and semantic["openBlockerIds"] == ["DF218-B03"]
                              and blockers["targetId"] == "timeless-form"
                              and [b["id"] for b in blockers["blockers"]] == ["DF218-B03"],
                              "5,063 supplied checks pass; DF218-B03 remains open"))

        # Verify the external source packet and its 87 current source rows independently.
        packet_raw = raw(PACKET_ZIP)
        packet_hash = hashlib.sha256(packet_raw).hexdigest()
        src = source_bindings["sourceArchive"]
        findings.append(check("external Packet308 source archive binding",
                              len(packet_raw) == src["bytes"] and packet_hash == src["sha256"]
                              and src["crc32"] == f"{zlib.crc32(packet_raw) & 0xffffffff:08x}"
                              and src["sha256"] == decision["sourceArchive"]["sha256"],
                              f"{len(packet_raw)} bytes; SHA-256 {packet_hash}"))
        source_rows = source_bindings["sourceRows"]
        current_source_ok = len(source_rows) == 87
        with zipfile.ZipFile(PACKET_ZIP) as pz:
            current_names = set(pz.namelist())
            for row in source_rows:
                path = row["path"]
                embedded_name = "sources_current/" + path
                if embedded_name not in current_names:
                    current_source_ok = False
                    continue
                embedded = pz.read(embedded_name)
                live_path = ROOT / pathlib.Path(path)
                live = live_path.read_bytes() if live_path.exists() else b""
                expected = {"bytes": row["bytes"], "sha256": row["sha256"], "crc32": row["crc32"]}
                for payload in (embedded, live):
                    actual = {"bytes": len(payload), "sha256": hashlib.sha256(payload).hexdigest(),
                              "crc32": f"{zlib.crc32(payload) & 0xffffffff:08x}"}
                    current_source_ok &= actual == expected
            return_case_names = [n for n in names if n.startswith("cases/")]
            historic_case_names = [n for n in pz.namelist() if n.startswith("history/Return218/preserved_cases/")]
            case_ok = len(return_case_names) == len(historic_case_names) == 11
            case_map = {n.split("/", 3)[-1]: n for n in historic_case_names}
            for out_name in return_case_names:
                leaf = out_name.split("/", 1)[1]
                case_ok &= leaf in case_map and rz.read(out_name) == pz.read(case_map[leaf])
            procedure_ok = ("procedures/timeless-form.json" in name_set
                            and rz.read("procedures/timeless-form.json")
                            == pz.read("history/Return218/procedures/timeless-form.json"))
        findings.append(check("87 current source rows match Packet308 and the worktree",
                              current_source_ok, "exact byte length, SHA-256 and CRC32 checked per row"))
        findings.append(check("all 11 prior cases and the procedure remain byte-exact",
                              case_ok and procedure_ok,
                              "compared with Packet308 history/Return218 members"))

        index = read(INDEX)
        catalog = read(CATALOG)
        index_by_id = {x["id"]: x for x in index["entries"]}
        catalog_by_id = {x["id"]: x for x in catalog["spells"]}
        time_stop = catalog_by_id["time-stop"]
        findings.append(check("current spell state supports the hold",
                              index_by_id["timeless-form"]["authoredStatus"] == "pending-authored-procedure"
                              and index_by_id["time-stop"]["authoredStatus"] == "pending-authored-procedure"
                              and time_stop.get("operational") is None
                              and index_by_id["time-stop"].get("procedurePointer") is None,
                              "Time Stop remains pending with operational=null and no accepted procedure pointer"))

        prev_audit = read(PENDING_307)
        expected_pending = prev_audit["pendingIds"]
        findings.append(check("pending set and next Director priority reconcile",
                              expected_pending == next_group["allPendingIds"]
                              and expected_pending == ORDER
                              and next_group["authority"] == AUTH
                              and next_group["queueMutationPerformed"] is False
                              and next_group["nextIdentity"] == "invulnerable-sphere"
                              and next_group["nextBlockerIds"] == ["DF218-B04"]
                              and next_group["continuingPriorityOrder"][0] == "invulnerable-sphere"
                              and next_group["firstReviewTasksRemaining"] == 0
                              and next_group["closureTasksRemaining"] == 26,
                              "26 pending unchanged; Invulnerable Sphere is next"))

    failed = [x for x in findings if not x["passed"]]
    audit = {
        "id": "TIMELESS-FORM-RETURN308-INDEPENDENT-AUDIT",
        "recordedAtUtc": stamp,
        "status": "PASS" if not failed else "FAIL",
        "checkCount": len(findings), "passedChecks": len(findings) - len(failed),
        "failedChecks": len(failed), "checks": findings,
        "returnArchive": ref(RETURN_ZIP), "returnDelivery": ref(RETURN_DELIVERY),
        "sourcePacket": ref(PACKET_ZIP),
        "interpretation": "Director HOLD verified; no acceptance, application, canonical index/catalog mutation, or positive Time Stop encounter is claimed.",
    }
    audit_path = A / "TIMELESS_FORM_RETURN308_INDEPENDENT_AUDIT.json"
    write(audit_path, audit)
    if failed:
        raise SystemExit("Independent return audit failed: " + json.dumps(failed, indent=2))

    # Record the Director ruling and a successor status without editing the authored index or catalog.
    decision_path = A / "TIMELESS_FORM_DIRECTOR_DECISION_308.json"
    decision = {
        "id": "TIMELESS-FORM-DF218-B03-DIRECTOR-DECISION-308", "recordedAtUtc": stamp,
        "decision": "HOLD_TIMELESS_FORM_PENDING_ACCEPTED_TIME_STOP_AND_COMPLETE_JOINT_WITNESS",
        "identity": "timeless-form", "blocker": "DF218-B03", "accepted": False, "applied": False,
        "acceptedIds": [], "appliedIds": [], "heldIds": ["timeless-form"],
        "blockerIds": ["DF218-B03"],
        "source": {"service": "ChatGPT", "conversationTitle": "Calibration review part 6",
                   "url": "https://chatgpt.com/g/g-p-67f17555a8dc8191a2b5b81e6d8adc12-dungeon-crawler/c/6adc506d-8770-83ea-b64c-0345d9b9b682"},
        "exactDirectorResponse": DIRECTOR_TEXT,
        "returnArchive": ref(RETURN_ZIP), "returnDelivery": ref(RETURN_DELIVERY),
        "independentAudit": ref(audit_path), "authority": AUTH,
        "minimumMissingWitness": [
            "Exact accepted operational Time Stop procedure with source/acceptance bindings defining activation, costs, eligible actors, affected/excluded entities, permitted actions, and native chronology.",
            "Lawfully acquired caster with complete activation history: class/repertoire/preparation, components, resources, Action/interruption accounting, target/area geometry, and relevant prior effects.",
            "Complete joint encounter where lawfully established Timeless Form encounters that Time Stop; demonstrate exclusion using actual permissions and preserve ordinary turns, recharge, Reaction, Ready, concentration, resources, and original deadlines without added opportunities or paused clocks.",
        ],
        "historicalCase": "history/Return218/preserved_cases/RANK9DEFENSEFORM8129-TIMELESS-FORM-B.json#/events/4 remains Time-Stop-access/procedure-held.",
        "nextActionableIdentity": "invulnerable-sphere", "nextBlockerIds": ["DF218-B04"],
        "nextAfterThat": {"identity": "nullification-wave", "blockerIds": ["WC188-B01"]},
        "canonicalFilesChanged": False,
    }
    decision_bytes = write(decision_path, decision)
    receipt_path = A / "TIMELESS_FORM_HOLD_RECEIPT_308.json"
    receipt = {
        "id": "TIMELESS-FORM-HOLD-RECEIPT-308", "recordedAtUtc": stamp,
        "status": "DIRECTOR_HELD_TIMELESS_FORM_DF218_B03_NEXT_INVULNERABLE_SPHERE",
        "acceptedIds": [], "appliedIds": [], "heldIds": ["timeless-form"],
        "blockerIds": {"timeless-form": ["DF218-B03"]},
        "decision": ref(decision_path, decision_bytes), "returnArchive": ref(RETURN_ZIP),
        "returnDelivery": ref(RETURN_DELIVERY), "independentAudit": ref(audit_path),
        "currentAuthority": AUTH, "nextActionableIdentity": "invulnerable-sphere",
        "nextBlockerIds": ["DF218-B04"], "firstReviewTasksRemaining": 0,
        "closureTasksRemaining": 26, "canonicalFilesChanged": False,
    }
    receipt_bytes = write(receipt_path, receipt)

    queue_prev = read(QUEUE_308)
    pending_prev = read(PENDING_307)
    queue_path = A / "CURRENT_SPELL_QUEUE_309.json"
    queue = copy.deepcopy(queue_prev)
    queue["id"] = "SPELL-REVIEW-QUEUE-309"
    queue["recordedAtUtc"] = stamp
    queue["supersedesQueue"] = ref(QUEUE_308)
    queue["currentAuthority"] = AUTH
    queue["nextGroup"] = "rank9-defense-form8"
    queue["next"] = {
        "group": "rank9-defense-form8", "pendingIds": ["invulnerable-sphere"],
        "pendingCount": 1, "status": "DIRECTOR_NEXT_AFTER_TIMELESS_FORM_HOLD_308",
        "freshPacketRequiredForCurrentAuthority": True,
        "blockerByIdentity": {"invulnerable-sphere": ["DF218-B04"]},
        "directorRequirement": "Prepare Invulnerable Sphere / DF218-B04 only after Director confirms its exact current minimum evidence and scope. Timeless Form remains held under DF218-B03; Final Word and Elemental Shell remain held. Next after Sphere is Nullification Wave / WC188-B01.",
    }
    queue["nextSuggestedGroups"] = [copy.deepcopy(queue["next"])]
    queue["nextPreparedRequest"] = queue["next"]
    queue["packetStatus"] = "RETURN308_RECEIVED_AND_INDEPENDENTLY_VERIFIED_HELD"
    queue["currentReturnDecision"] = ref(decision_path, decision_bytes)
    queue["currentReturnArchive"] = ref(RETURN_ZIP)
    queue["currentReturnDelivery"] = ref(RETURN_DELIVERY)
    queue["currentReturnAudit"] = ref(audit_path)
    queue["currentReturnReceipt"] = ref(receipt_path, receipt_bytes)
    queue["currentReturnAcceptedIds"] = []
    queue["currentReturnAppliedIds"] = []
    queue["currentReturnHeldIds"] = ["timeless-form"]
    queue["currentReturnBlockers"] = {"timeless-form": ["DF218-B03"]}
    queue["githubChanges"] = False
    queue_bytes = write(queue_path, queue)

    pending_path = A / "CURRENT26_PENDING_IDENTITY_AUDIT_308.json"
    pending = copy.deepcopy(pending_prev)
    pending["id"] = "CURRENT26-PENDING-IDENTITY-AUDIT-308"
    pending["recordedAtUtc"] = stamp
    pending["status"] = "PASS_CURRENT_822_26_AFTER_TIMELESS_FORM_HOLD_308"
    pending["supersedes"] = ref(PENDING_307)
    pending["pendingCount"] = 26
    pending["pendingIds"] = ORDER
    pending["heldIds"] = sorted(set(pending.get("heldIds", [])) | {"timeless-form"})
    pending["lastDirectorDecision"] = ref(decision_path, decision_bytes)
    pending["lastDirectorHoldReceipt"] = ref(receipt_path, receipt_bytes)
    pending["lastDirectorReturnAudit"] = ref(audit_path)
    pending["lastDirectorReturnArchive"] = ref(RETURN_ZIP)
    pending["nextPendingGroup"] = queue["next"]
    pending["firstReviewTasksRemaining"] = 0
    pending["remainingPendingCount"] = 26
    pending_bytes = write(pending_path, pending)

    handoff_path = A / "CURRENT_HANDOFF_309.json"
    handoff = copy.deepcopy(read(HANDOFF_308))
    handoff.update({
        "id": "CURRENT-HANDOFF-309", "recordedAtUtc": stamp,
        "supersedes": ref(HANDOFF_308),
        "status": "TIMELESS_FORM_HELD_NEXT_INVULNERABLE_SPHERE_822_26",
        "authority": AUTH, "currentAuthority": AUTH,
        "queueBinding": ref(queue_path, queue_bytes), "queue": ref(queue_path, queue_bytes),
        "pendingIdentityAudit": ref(pending_path, pending_bytes),
        "appliedThisStep": False, "acceptedThisStep": [],
        "nextStep": queue["next"], "nextStepText": queue["next"]["directorRequirement"],
        "nextGroup": "rank9-defense-form8", "nextPendingCount": 1,
        "nextPendingIds": ["invulnerable-sphere"],
        "currentBlocker": {"identity": "invulnerable-sphere", "group": "rank9-defense-form8", "blockerIds": ["DF218-B04"]},
        "directorConnectionStatus": DIRECTOR_TEXT,
        "githubChanges": False, "runtimeSelectionEnabled": False,
        "latestBatch": {"accepted": [], "applied": [], "held": {"timeless-form": ["DF218-B03"]}},
        "currentReturnDecision": ref(decision_path, decision_bytes),
        "currentReturnArchive": ref(RETURN_ZIP), "currentReturnDelivery": ref(RETURN_DELIVERY),
        "currentReturnAudit": ref(audit_path), "currentReturnReceipt": ref(receipt_path, receipt_bytes),
        "canonicalRuntimeApplicationPerformed": False,
        "canonicalFilesChangedByThisRuling": False,
        "firstReviewTasksRemaining": 0, "currentReturnCrosscheck": ref(audit_path),
    })
    handoff_bytes = write(handoff_path, handoff)

    validation_path = A / "TIMELESS_FORM_HOLD_VALIDATION_309.json"
    validation_checks = [
        check("Return308 archive and manifest bindings pass independent verification", not failed),
        check("Director explicitly held only Timeless Form under DF218-B03", decision["heldIds"] == ["timeless-form"] and decision["blockerIds"] == ["DF218-B03"]),
        check("Acceptance and application are both empty", decision["acceptedIds"] == [] and decision["appliedIds"] == []),
        check("Current index/catalog and 26 pending identities remain unchanged", read(INDEX) == index and read(CATALOG) == catalog and pending["pendingIds"] == ORDER),
        check("Invulnerable Sphere is the next identity under DF218-B04", queue["next"]["pendingIds"] == ["invulnerable-sphere"] and queue["next"]["blockerByIdentity"]["invulnerable-sphere"] == ["DF218-B04"]),
        check("Authority remains 822/26/0 with 546 procedures and 173 interfaces", handoff["currentAuthority"] == AUTH),
        check("Canonical index/catalog, runtime and application were not changed", handoff["canonicalFilesChangedByThisRuling"] is False and handoff["canonicalRuntimeApplicationPerformed"] is False),
    ]
    validation = {
        "id": "TIMELESS-FORM-HOLD-AND-NEXT-QUEUE-VALIDATION-309", "recordedAtUtc": stamp,
        "status": "PASS" if all(x["passed"] for x in validation_checks) else "FAIL",
        "checkCount": len(validation_checks), "passedChecks": sum(x["passed"] for x in validation_checks),
        "failedChecks": sum(not x["passed"] for x in validation_checks), "checks": validation_checks,
        "directorDecision": ref(decision_path), "holdReceipt": ref(receipt_path),
        "returnAudit": ref(audit_path), "pendingIdentityAudit": ref(pending_path),
        "queue": ref(queue_path), "handoff": ref(handoff_path), "authority": AUTH,
        "heldIdentity": "timeless-form", "nextActionableIdentity": "invulnerable-sphere",
        "acceptedIds": [], "appliedIds": [], "canonicalFilesChanged": False,
        "runtimeSelectionEnabled": False,
    }
    write(validation_path, validation)
    if validation["failedChecks"]:
        raise SystemExit("Hold-chain validation failed: " + json.dumps(validation_checks, indent=2))

    snapshot = A / "CURRENT_SPELL_REVIEW_SNAPSHOT_309.md"
    snapshot.write_text(
        "# Current spell review snapshot — Return308\n\n"
        f"Recorded: {stamp}\n\n"
        "Director decision: **HOLD** for Timeless Form / `timeless-form` / DF218-B03. "
        "No identity was accepted or applied. The accepted operational Time Stop procedure, "
        "lawful caster activation history, and complete joint encounter remain missing.\n\n"
        "The Return308 archive and all 87 current source bindings passed independent integrity checks; "
        "all 11 historical Timeless Form cases and its procedure match Return218 byte for byte. "
        "The Director's 238-event numerical replay does not establish the missing encounter.\n\n"
        "Authority remains **822 applied / 26 pending / 0 accepted-unapplied**, with 546 standalone "
        "procedures and 173 scoped interfaces. Final Word and Elemental Shell remain separately held.\n\n"
        "Next: **Invulnerable Sphere / DF218-B04**, then **Nullification Wave / WC188-B01**. "
        "Current index/catalog and runtime selection were not changed.\n",
        encoding="utf-8",
    )
    print(json.dumps({"returnAudit": str(audit_path), "decision": str(decision_path),
                      "holdReceipt": str(receipt_path), "queue": str(queue_path),
                      "pendingAudit": str(pending_path), "handoff": str(handoff_path),
                      "validation": str(validation_path), "snapshot": str(snapshot),
                      "returnChecks": len(findings), "returnFailures": len(failed),
                      "holdChecks": len(validation_checks), "holdFailures": validation["failedChecks"],
                      "nextIdentity": "invulnerable-sphere"}, indent=2))


if __name__ == "__main__":
    main()
