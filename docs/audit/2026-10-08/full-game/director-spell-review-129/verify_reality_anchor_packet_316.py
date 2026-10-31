from __future__ import annotations

import copy
import hashlib
import json
import pathlib
import sys
import zipfile
import zlib

import jsonpatch


ROOT = pathlib.Path.cwd()
A = ROOT / "docs/audit/2026-10-08/full-game/director-spell-review-129"
OUT = A / "rank9_wardcontrol6_reality_anchor_packet_316_prepared_build04"
PACKET = OUT / "DD_Rank9_WardControl6_RealityAnchor_316.zip"
DELIVERY = OUT / "DD_Rank9_WardControl6_RealityAnchor_316_DELIVERY.json"
RESULT = A / "REALITY_ANCHOR_PACKET_316_INDEPENDENT_AUDIT.json"
RETURN281 = A / "rank9_wardcontrol6_return281_received/DD_Rank9_WardControl6_Director_Return281_HELD.zip"
INDEX = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json"
CATALOG = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json"


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def digest(raw: bytes) -> dict:
    return {"bytes": len(raw), "sha256": sha(raw), "crc32": f"{zlib.crc32(raw) & 0xffffffff:08x}"}


def state_sha(state: dict) -> str:
    return sha(json.dumps(state, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8"))


def main() -> None:
    checks = []
    def passed(name: str, details=None):
        checks.append({"name": name, "status": "PASS", "details": details or {}})

    packet_raw = PACKET.read_bytes()
    delivery = json.loads(DELIVERY.read_text(encoding="utf-8-sig"))
    assert delivery["packet"]["sha256"] == sha(packet_raw) and delivery["packet"]["bytes"] == len(packet_raw)
    assert delivery["scopeIds"] == ["reality-anchor"] and delivery["blockerIds"] == ["WC188-B02"]
    passed("delivery_packet_binding", digest(packet_raw))

    with zipfile.ZipFile(PACKET) as z:
        assert z.testzip() is None
        names = set(z.namelist())
        assert len(names) == 158
        manifest = json.loads(z.read("MEMBER_MANIFEST.json"))
        assert manifest["memberCount"] == len(names) - 1
        for row in manifest["members"]:
            raw = z.read(row["path"])
            assert digest(raw) == {k: row[k] for k in ("bytes", "sha256", "crc32")}, row["path"]
        passed("outer_zip_and_157_member_manifest", {"members": len(names), "manifestEntries": manifest["memberCount"]})

        refresh = json.loads(z.read("authority/SOURCE_REFRESH_316.json"))
        assert refresh["sourceCount"] == 91 and refresh["changedSincePacket312"] == []
        for row in refresh["currentBindings"]:
            path = ROOT / pathlib.Path(row["path"])
            actual = path.read_bytes()
            packed = z.read("sources_current/" + row["path"])
            assert digest(actual) == {k: row[k] for k in ("bytes", "sha256", "crc32")}, row["path"]
            assert actual == packed, row["path"]
        passed("all_91_current_source_bindings", {"sourceCount": 91, "changedSince312": 0})

        audit = json.loads(z.read("authority/CURRENT26_PENDING_IDENTITY_AUDIT_316.json"))
        queue = json.loads(z.read("authority/CURRENT_SPELL_QUEUE_316.json"))
        handoff = json.loads(z.read("authority/CURRENT_HANDOFF_316.json"))
        assert audit["authority"] == {"reviewedApplied": 822, "pending": 26, "acceptedUnapplied": 0, "completeStandaloneProcedures": 546, "scopedInterfaces": 173}
        assert audit["pendingCount"] == 26 and audit["nextPendingIds"] == ["reality-anchor"]
        assert queue["next"] == "reality-anchor" and queue["closureTasksRemaining"] == 26
        assert handoff["applicationPerformed"] is False and handoff["acceptedThisStep"] == []
        idx = json.loads(INDEX.read_text(encoding="utf-8-sig"))
        cat = json.loads(CATALOG.read_text(encoding="utf-8-sig"))
        pending = {x["id"] for x in idx["entries"] if x.get("authoredStatus") == "pending-authored-procedure"}
        catalog = {x["id"] for x in cat["spells"]}
        assert len(pending) == 26 and pending <= catalog and "reality-anchor" in pending
        passed("authority_822_26_0_and_next_identity", {"pending": len(pending), "next": "reality-anchor", "acceptedUnapplied": 0})

        with zipfile.ZipFile(RETURN281) as old:
            assert z.read("authority/Return281_ARCHIVE.zip") == RETURN281.read_bytes()
            old_index = json.loads(old.read("CASE_INDEX.json"))
            old_rows = [r for r in old_index["cases"] if r.get("spellId") == "reality-anchor"]
            assert len(old_rows) == 14
            for name in ["ACTOR_PROFILES.json", "BLOCKERS.json", "QUALIFICATIONS.json", "SOURCE_PAIR_TABLE.json", "ORIGINAL_OBLIGATIONS.json", "QUESTION_DISPOSITIONS.json", "HOLD_REGISTER.json", "REMAINING_QUEUE.json", "CASE_INDEX.json", "procedures/reality-anchor.json"]:
                assert z.read("history/Return281/" + name) == old.read(name), name
            for row in old_rows:
                assert z.read("history/Return281/" + row["path"]) == old.read(row["path"]), row["path"]
        passed("Return281_exact_14_RA_records_and_procedure", {"records": 14})

        w2 = json.loads(z.read("source/eternal-forge/SUPPLEMENT255_W2.json"))
        w2b = w2["eventReplay"]["branches"][0]
        s = copy.deepcopy(w2["priorCase"]["endState"])
        assert state_sha(s) == w2b["baseStateSHA256"]
        for event in w2b["events"]:
            assert state_sha(s) == event["beforeSHA256"], event["id"]
            before = copy.deepcopy(s)
            s = jsonpatch.JsonPatch(event["forward"]).apply(s, in_place=False)
            assert state_sha(s) == event["afterSHA256"], event["id"]
            assert state_sha(jsonpatch.JsonPatch(event["inverse"]).apply(s, in_place=False)) == state_sha(before), event["id"]
        assert state_sha(s) == w2b["finalStateSHA256"] == "684d5206f81ad473ef4b61a1b84d104a02fb18a8ef2d884f5b9e133c40e7109e"
        assert s["items"]["bracelet-2"]["imprintRoot"]["id"] == "castF3" and s["items"]["bracelet-2"]["imprintRoot"]["active"] is True
        assert s["items"]["bracelet-1"]["imprintRoot"]["active"] is False
        passed("accepted_Forge_W2_exact_endpoint_forward_inverse_replay", {"events": len(w2b["events"]), "endStateSHA256": state_sha(s)})

        witness = json.loads(z.read("witness/REALITY_ANCHOR_WITNESS_SUPPLEMENT_316.json"))
        branches = witness["branches"]
        assert {b["id"] for b in branches} == {"WC188-B02-FORGE-SURVIVES", "WC188-B02-FORGE-TERMINATES-WHILE-DENIED"}
        total_events = 0
        for b in branches:
            assert state_sha(b["baseState"]) == "684d5206f81ad473ef4b61a1b84d104a02fb18a8ef2d884f5b9e133c40e7109e"
            assert z.read(f"witness/{b['id']}_BASE_STATE.json") == (json.dumps(b["baseState"], indent=2, ensure_ascii=False) + "\n").encode("utf-8")
            cur = copy.deepcopy(b["baseState"])
            previous_end = cur["time"]
            for event in b["events"]:
                assert event["timeStartSeconds"] >= previous_end - 1e-6, (b["id"], event["id"], event["timeStartSeconds"], previous_end)
                assert state_sha(cur) == event["beforeSHA256"], event["id"]
                before = copy.deepcopy(cur)
                cur = jsonpatch.JsonPatch(event["forward"]).apply(cur, in_place=False)
                assert state_sha(cur) == event["afterSHA256"], event["id"]
                reverse = jsonpatch.JsonPatch(event["inverse"]).apply(cur, in_place=False)
                assert state_sha(reverse) == state_sha(before), event["id"]
                previous_end = event["timeEndSeconds"]
                total_events += 1
            assert state_sha(cur) == b["finalStateSHA256"]
            assert cur == b["finalState"]
            assert z.read(f"witness/{b['id']}_FINAL_STATE.json") == (json.dumps(b["finalState"], indent=2, ensure_ascii=False) + "\n").encode("utf-8")
            assert cur["items"]["bracelet-2"]["imprintRoot"]["active"] == b["expectedFinal"]["forgeRootActive"]
            assert cur["time"] == b["expectedFinal"]["timeSeconds"]
            due = cur["supplement"]["realityAnchorWitness316"]["dueClockEvents"]
            assert all(x["timeSeconds"] <= cur["time"] for x in due)
            if b["id"].endswith("SURVIVES"):
                assert cur["items"]["bracelet-2"]["imprintRoot"]["active"] is True
                assert cur["items"]["bracelet-2"]["charges"] == 0
                assert cur["supplement"]["realityAnchorWitness316"]["deniedExpressions"][0]["chargeAfter"] == 1
            else:
                root = cur["items"]["bracelet-2"]["imprintRoot"]
                assert root["active"] is False and root["endReason"] == "actual-successful-greater-dispel-while-RA-denied"
                assert cur["items"]["bracelet-2"]["charges"] == 1
                assert cur["supplement"]["realityAnchorWitness316"]["functionEvents"][-1]["decision"] == "NO_LIVE_SOURCE"
                ending = cur["supplement"]["realityAnchorWitness316"]["imprintEndings"][0]
                assert ending["RAStillDeniesCastF3AtResolution"] is True and ending["physicalBodyPreserved"] is True
        for b in branches:
            final = b["finalState"]
            root = final["items"]["bracelet-2"]["imprintRoot"]
            records = [e["record"] for e in b["events"]]
            assert records[1]["immediatelySuppressedApplications"] == ["castF3"]
            immediate = jsonpatch.JsonPatch(b["events"][0]["forward"]).apply(copy.deepcopy(b["baseState"]), in_place=False)
            immediate = jsonpatch.JsonPatch(b["events"][1]["forward"]).apply(immediate, in_place=False)
            item0 = immediate["items"]["bracelet-2"]
            assert item0["imprintRoot"]["active"] and item0["imprintRoot"]["suppressed"] and item0["charges"] == 1 and item0["HP"] == 5
            ends = [e for e in b["events"] if e["kind"] == "regular-end"]
            assert any(e["record"]["actor"] == "B" and e["timeEndSeconds"] == 172812.0 for e in ends)
            assert any(e["record"]["actor"] == "A" and e["timeEndSeconds"] == 172812.2 for e in ends)
            a_ends = [e["record"] for e in ends if e["record"]["actor"] == "A"]
            assert [(e["endResult"]["dissonanceBefore"],e["endResult"]["dissonanceVented"],e["endResult"]["dissonanceAfter"]) for e in a_ends[:3]] == [(2,0,2),(2,1,1),(1,1,0)]
            starts = [e["record"] for e in b["events"] if e["kind"] == "regular-start"]
            assert starts and all(e["turnCastAfter"] is False for e in starts)
            assert all(x["ActionAfter"] == 0 and x["BonusActionAfter"] == 0 and x["freeInteractionAfter"] == 0 and x["movementRemainingAfter"] == 0 and x["nextRegularEndAfter"] is None for x in final["supplement"]["realityAnchorWitness316"]["dueClockEvents"] if x["kind"] == "regular-end")
            wear = next(e["record"] for e in b["events"] if e["kind"] == "lawful-wear")
            assert wear["actualWornBodyBoundsFeet"] == [[0,3,0],[0.4,3.4,0.1]]
            assert any(e["kind"] == "ordinary-movement-changed-hide-circumstance" and e["record"]["movementFeet"] == 5 for e in b["events"])
            hide = final["supplement"]["realityAnchorWitness316"]["hideOutcomes"]
            assert len(hide) == 2 and hide[0]["degree"] == "failure" and hide[0]["total"] == 10 and hide[0]["passivePerception"] == 11
            assert hide[0]["chargeBefore"] == hide[0]["chargeAfter"] == 1 and hide[0]["itemBonusApplied"] == 0 and hide[0]["advantageApplied"] is False
            assert hide[1]["changedCircumstanceFromPriorFailure"] is True
            if b["id"].endswith("SURVIVES"):
                assert hide[1]["dice"]["faces"] == [15,8] and hide[1]["dice"]["selected"] == 15 and hide[1]["total"] == 18
                assert hide[1]["degree"] == "success" and hide[1]["hiddenFromC"] and hide[1]["chargeCommittedBeforeRoll"] and hide[1]["chargeAfter"] == 0
            else:
                dispel = next(e["record"] for e in b["events"] if e["kind"] == "paid-greater-dispel-terminates-denied-imprint")
                assert (dispel["preCastRP"],dispel["baseRP"],dispel["preCastDissonance"],dispel["baseDissonance"],dispel["RefrainAdded"],dispel["firstFamily"],dispel["paidRP"],dispel["postCastRP"],dispel["dissonanceAfter"]) == (13,10,0,1,0,False,10,3,1)
                assert dispel["immutableCapturedApplications"] == ["castF3","castRA1"] and dispel["RAFieldAreaOverlapIncluded"]
                assert [(x["applicationId"],x["total"],x["success"]) for x in dispel["targetChecks"]] == [("castF3",28,True),("castRA1",27,False)]
                assert hide[1]["sourceDecision"] == "NO_LIVE_SOURCE" and hide[1]["degree"] == "failure" and hide[1]["chargeAfter"] == 1 and not hide[1]["advantageApplied"]
                assert a_ends[-1]["endResult"]["turnCast"] is True and a_ends[-1]["endResult"]["dissonanceAfter"] == 1
                assert root.get("suppressedBy") is None and root["suppressionHistory"][-1]["historicalProvenanceRetained"] is True
        assert total_events == witness["eventCount"] == delivery["witnessEventCount"] == 55
        passed("Return315_five_corrections_replayed_in_both_branches", {"branches": len(branches), "events": total_events, "hideOutcomes": 4, "inheritedEnds": 4, "castsAndVentingVerified": True})

        ret_path = A / "rank9_wardcontrol6_return315_received/DD_Rank9_WardControl6_Director_Return315_HELD.zip"
        with zipfile.ZipFile(ret_path) as ret:
            correction = json.loads(ret.read("CORRECTION_SHEET.json"))
            assert [x["id"] for x in correction["findings"]] == ["RA315-C01","RA315-C02","RA315-C03","RA315-C04","RA315-C05"]
            for source_member, packet_member in [("CORRECTION_SHEET.json","authority/Return315_CORRECTION_SHEET.json"),("A_EVENT_CORRECTION_LEDGER.json","authority/Return315_A_EVENT_CORRECTION_LEDGER.json"),("DIRECTOR_DECISION.json","authority/Return315_DIRECTOR_DECISION.json"),("DATA_VALIDATION.json","authority/Return315_DATA_VALIDATION.json")]:
                assert ret.read(source_member) == z.read(packet_member)
        assert z.read("authority/Return315_ARCHIVE.zip") == ret_path.read_bytes()
        passed("Return315_sealed_corrections_bound_and_addressed", {"corrections": 5})

    result = {
        "id": "REALITY-ANCHOR-PACKET-316-INDEPENDENT-AUDIT",
        "recordedAtUtc": __import__("datetime").datetime.now(__import__("datetime").timezone.utc).isoformat(timespec="seconds"),
        "status": "PASS",
        "packet": {"path": PACKET.relative_to(ROOT).as_posix(), **digest(packet_raw)},
        "delivery": {"path": DELIVERY.relative_to(ROOT).as_posix(), **digest(DELIVERY.read_bytes())},
        "checkCount": len(checks), "failures": [], "checks": checks,
        "sourceCount": 91, "return281RARecordCount": 14, "branchCount": 2,
        "witnessEventCount": delivery["witnessEventCount"],
        "authority": {"reviewedApplied": 822, "pending": 26, "acceptedUnapplied": 0},
        "acceptedIds": [], "appliedIds": [], "canonicalChanges": False,
    }
    RESULT.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({"status": result["status"], "checkCount": result["checkCount"], "failures": result["failures"], "resultPath": str(RESULT)}, indent=2))


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"FAIL: {type(exc).__name__}: {exc}", file=sys.stderr)
        raise
