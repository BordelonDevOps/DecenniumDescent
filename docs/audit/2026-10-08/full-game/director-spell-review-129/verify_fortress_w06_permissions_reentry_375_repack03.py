from __future__ import annotations

import hashlib
import json
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
import build_fortress_closure_intake_367 as intake  # noqa: E402

OUTPUT = ROOT / "fortress_w06_permissions_reentry_375_repack03"
PAYLOAD = OUTPUT / "payload"
CASE_PATH = PAYLOAD / "case/PG328_W06_PERMISSIONS_REENTRY_CASE_375_REPACK03_TESTONLY.json"
ARCHIVE_PATH = OUTPUT / "DD_Rank9_ConjureDemiplaneFortress_W06_PermissionsReentry_375_Repack03_TESTONLY.zip"
DELIVERY_PATH = OUTPUT / "DD_Rank9_ConjureDemiplaneFortress_W06_PermissionsReentry_375_Repack03_DELIVERY.json"
FIXTURE_PATH = ROOT / "conjure_demiplane_fortress_closure_intake_367/payload/fixtures/PG328-W03_BENEFICIAL_SHORT_REST_367_TESTONLY.json"
P368_AUTH_PATH = ROOT / "conjure_demiplane_fortress_closure_intake_367/OWNER_P368_W03_TESTONLY_AUTHORIZATION_372.json"
QUEUE_PATH = PAYLOAD / "authority/CURRENT_SPELL_QUEUE_361.json"
PARENT_MEMBER = (
    "evidence/packet328/prior/Return284_cases/"
    "RANK9PLANARGATES5129-CONJURE-DEMIPLANE-FORTRESS-A__permissions-reentry.json"
)


def raw_sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_sha(value: object) -> str:
    data = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(data).hexdigest()


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def main() -> None:
    case = read_json(CASE_PATH)
    delivery = read_json(DELIVERY_PATH)
    manifest = read_json(PAYLOAD / "MANIFEST.json")
    queue = read_json(QUEUE_PATH)
    owner_p368 = read_json(P368_AUTH_PATH)

    with zipfile.ZipFile(ARCHIVE_PATH) as archive:
        assert archive.testzip() is None
        members = set(archive.namelist())
        assert len(manifest["files"]) == 13
        assert len(members) == 14
        for row in manifest["files"]:
            member_name = f"payload/{row['path']}"
            assert member_name in members
            contents = archive.read(member_name)
            assert len(contents) == row["bytes"]
            assert hashlib.sha256(contents).hexdigest() == row["sha256"]
    assert delivery["archive"]["bytes"] == ARCHIVE_PATH.stat().st_size
    assert delivery["archive"]["sha256"] == raw_sha(ARCHIVE_PATH)
    assert delivery["parentFinalSHA256"] == case["parentFinalSHA256"]
    assert case["initialSHA256"] == canonical_sha(case["initial"])
    assert case["finalSHA256"] == canonical_sha(case["final"])

    parent_archive = zipfile.ZipFile(PAYLOAD / "authority/PG328_HELD_ARCHIVE.zip")
    parent_raw = parent_archive.read(PARENT_MEMBER)
    parent = json.loads(parent_raw)
    assert hashlib.sha256(parent_raw).hexdigest() == case["parentCaseSHA256"]
    assert parent["finalSHA256"] == case["parentFinalSHA256"]
    assert canonical_sha(parent["final"]) == case["parentFinalSHA256"]
    assert case["initial"] == parent["final"]

    for event in case["events"]:
        assert canonical_sha(event["before"]) == event["beforeSHA256"]
        assert canonical_sha(event["after"]) == event["afterSHA256"]
        assert intake.apply_ops(event["before"], event["forward"]) == event["after"]
        assert intake.apply_ops(event["after"], event["inverse"]) == event["before"]
    reverse = case["final"]
    for event in reversed(case["events"]):
        reverse = intake.apply_ops(reverse, event["inverse"])
    assert reverse == parent["final"]
    assert len(case["events"]) == 57

    route = next(
        event for event in case["events"]
        if event["kind"] == "TEST_ONLY_VOLUNTARY_MOVEMENT"
        and event["detail"]["actorId"] == "B"
        and event["eventTime"]["initiativeSeconds"] == 31.1
    )
    assert route["detail"]["pathFeet"] == [[15, 10, 0], [20, 10, 0]]
    assert route["detail"]["movementCostFeet"] == 5
    assert route["detail"]["movementAfterFeet"] == 25
    assert len(route["detail"]["sweptBodyCollisionChecks"]) == 1
    sweep = route["detail"]["sweptBodyCollisionChecks"][0]
    assert sweep["sweptBodyBoundsFeet"] == {"min": [12.5, 7.5, 0], "max": [22.5, 12.5, 6]}
    assert sweep["courtyardClearanceFromFiveFootOuterWallBandFeet"] == 2.5
    assert sweep["sweptBodyRemainsInsideUnobstructedCourtyard"] is True
    assert sweep["glyphMountPositiveVolumeConflict"] is False
    glyph = case["fixturePremises"]["fixedGeometryAndCarrierBounds"]["interiorExitControlGlyph"]
    assert glyph["positionFeet"] == [18, 12.5, 3]
    assert glyph["mounting"]["boundsFeet"] == {
        "min": [17.75, 12.5, 0], "max": [18.25, 13, 3.25]
    }

    end_a = case["events"][11]
    assert end_a["kind"] == "REGULAR_END"
    assert end_a["detail"]["spellEfficiencyExpiredAtThisEnd"]
    assert end_a["after"]["actors"]["A"]["spellEfficiency"] is None
    assert end_a["before"]["actors"]["A"]["lastSpell"] == end_a["after"]["actors"]["A"]["lastSpell"]
    assert end_a["before"]["actors"]["A"]["spellHistory"] == end_a["after"]["actors"]["A"]["spellHistory"]
    b_crossings = [event for event in case["events"] if event["kind"] == "TEST_ONLY_ATOMIC_WHOLE_GRAPH_CROSSING" and event["detail"]["actorId"] == "B"]
    assert len(b_crossings) == 3
    assert all(event["detail"]["lastArrivedFromPlaneKeyAfter"] == event["detail"]["sourcePlane"] for event in b_crossings)
    space_id = "RANK9PLANARGATES5129-CONJURE-DEMIPLANE-FORTRESS-A/permissions-reentry/cast1/space"
    inherited_doors = parent["final"]["spaces"][space_id]["doors"]
    assert all(event["before"]["spaces"][space_id]["doors"] == inherited_doors
               and event["after"]["spaces"][space_id]["doors"] == inherited_doors
               for event in case["events"])
    b_transits = [receipt for receipt in case["final"]["transitReceipts"] if receipt["group"] == ["B"]]
    assert len(b_transits) == 3
    for receipt in b_transits:
        for fit in receipt["sourceAndDestinationApertureFitReceipt"].values():
            assert all(fit["verticalFitsUnderBothInterpretations"].values())

    fixture_hash = raw_sha(FIXTURE_PATH)
    assert fixture_hash == owner_p368["scope"]["fixtureSha256"]
    assert delivery["w03Fixture367SHA256"] == fixture_hash
    assert queue["currentAuthority"]["reviewedApplied"] == 828
    assert queue["pendingCount"] == 20
    assert queue["acceptedUnapplied"] == 0
    assert delivery["queueBeforeAndAfter"] == {"applied": 828, "pending": 20, "acceptedUnapplied": 0}
    print(json.dumps({
        "result": "PASS",
        "manifestFileCount": 13,
        "archiveSha256": raw_sha(ARCHIVE_PATH),
        "deliveryArchiveHashMatches": True,
        "parentInitialMatchesExactly": True,
        "eventCount": len(case["events"]),
        "allForwardInverseAndFullReverseReplay": True,
        "event52Route": route["detail"]["pathFeet"],
        "outerWallClearanceFeet": sweep["courtyardClearanceFromFiveFootOuterWallBandFeet"],
        "postMountBounds": glyph["mounting"]["boundsFeet"],
        "w03FixtureUnchanged": True,
        "queue": "828/20/0",
    }, indent=2))


if __name__ == "__main__":
    main()
