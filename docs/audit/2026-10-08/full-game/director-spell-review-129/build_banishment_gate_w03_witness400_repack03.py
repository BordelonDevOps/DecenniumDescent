#!/usr/bin/env python3
"""Repair only R6 in the exact reviewed W03 Repack02; preserve all originals."""
import argparse
import copy
import hashlib
import io
import json
import math
from pathlib import Path
import zipfile

BASE = Path(__file__).resolve().parent
REPO = BASE.parents[4]
PRIOR_DIR = BASE / "banishment_gate_w03_lich_taxonomy_witness400_repack02"
OUT = BASE / "banishment_gate_w03_lich_taxonomy_witness400_repack03"
PRIOR_NAME = "DD_Rank9_BanishmentGate_PG327W03_LichTaxonomy_Witness400_Repack02_TESTONLY.zip"
NAME = "DD_Rank9_BanishmentGate_PG327W03_LichTaxonomy_Witness400_Repack03_TESTONLY.zip"
PRIOR_SHA = "9ce22e2a240b0ac92eb98d676c197c3d6e64696e7b59595cec885c6f4d383cd7"
PRIOR_COMMIT = "a669773b9f7b8cdea5c250b59aa9ceaa273b6f14"
CARD = "wizard.base.counterspell"
PROFILE_REF = "sources/W07_BOUND_ACTOR_PROFILES_351fe708.json#/Wizard20/automaticCards/1"
ENGINE_MEMBER = "sources/WIZARD_CLASS_ENGINE_W07.md"


def sha(data):
    return hashlib.sha256(data).hexdigest()


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()


def encode(value):
    return (json.dumps(value, indent=2, ensure_ascii=False) + "\n").encode()


def escaped(key):
    return str(key).replace("~", "~0").replace("/", "~1")


def delta(before, after, path=""):
    """Field-scoped RFC6902 operations; every removal/replacement is tested."""
    if canonical(before) == canonical(after):
        return []
    if isinstance(before, dict) and isinstance(after, dict):
        result = []
        for key in sorted(before.keys() - after.keys()):
            p = path + "/" + escaped(key)
            result += [{"op": "test", "path": p, "value": before[key]}, {"op": "remove", "path": p}]
        for key in sorted(after.keys() - before.keys()):
            result += [{"op": "add", "path": path + "/" + escaped(key), "value": after[key]}]
        for key in sorted(before.keys() & after.keys()):
            result += delta(before[key], after[key], path + "/" + escaped(key))
        return result
    return [{"op": "test", "path": path, "value": before}, {"op": "replace", "path": path, "value": after}]


def readiness(state, actor_id):
    actor = state["actors"][actor_id]
    focus = "focus-" + actor_id
    actor["handCustody"] = {
        "leftHand": {"itemId": focus, "held": True, "custodian": actor_id, "carriedBy": actor_id},
        "rightHand": {"itemId": None, "free": True, "usableForSomatic": True},
        "voiceAvailable": True,
        "premise": "Authored TEST_ONLY opening custody, not an extra interaction or campaign fact",
    }
    state["items"][focus].update({"carriedBy": actor_id, "carryingState": "held-in-left-hand", "heldIn": "left"})
    actor["recharge"][CARD] = 0
    actor["counterspellReadiness"] = {
        "source": PROFILE_REF,
        "classMatrixRule": ENGINE_MEMBER + "#L44",
        "acquiredAutomaticallyAtWizardLevel": 2,
        "alwaysPrepared": True,
        "ordinaryPreparedSlotRequired": False,
        "costRP": 3,
        "reactionCost": 1,
        "rechargeKey": CARD,
        "rechargeCounter": 0,
        "rechargeReady": True,
        "componentsAvailable": ["V", "S", "F"],
        "focusItemId": focus,
        "freeSomaticHand": "right",
        "openingReadinessPremise": "TEST_ONLY; no prior cooldown; no new refresh is granted",
        "castPerception": {
            "casterId": "A", "perceivesCasting": True, "lineOfSight": True,
            "lineOfEffect": True, "obscured": False, "silenced": False,
            "geometry": "Existing clear open fixture:origin; no walls, blockers or unlisted bodies",
            "premise": "Explicit TEST_ONLY perception; not a campaign observation",
        },
    }


def responder(state, actor_id):
    actor = state["actors"][actor_id]
    distance = math.dist(actor["position"], state["actors"]["A"]["position"])
    return {
        "actorId": actor_id, "automaticCardId": CARD, "source": PROFILE_REF,
        "classMatrixRule": ENGINE_MEMBER + "#L44", "acquired": True, "alwaysPrepared": True,
        "distanceFeet": round(distance, 6), "counterspellRangeFeet": 60, "withinRange": distance <= 60,
        "perceivesCasting": True, "lineOfSight": True, "lineOfEffect": True,
        "reactionAvailable": actor["reaction"] == 1, "reactionBefore": actor["reaction"],
        "currentRP": actor["RP"], "costRP": 3, "affordable": actor["RP"] >= 3,
        "rechargeKey": CARD, "rechargeCounter": actor["recharge"][CARD], "rechargeReady": True,
        "componentsAvailable": ["V", "S", "F"], "focusItemId": "focus-" + actor_id,
        "heldFocusHand": "left", "freeSomaticHand": "right", "voiceAvailable": True,
        "Dissonance": actor["Dissonance"], "Refrain": actor["Refrain"],
        "eligibility": "eligible", "decision": "decline", "disposition": "TEST_ONLY eligible responder explicitly declines",
        "decisionPremise": "Hypothetical cooperative witness; not a campaign choice",
        "attempted": False, "roll": None, "RPSpent": 0, "reactionSpent": False,
        "rechargeChanged": False, "castingHistoryChanged": False, "strainChanged": False,
    }


def build(source_archive):
    raw = source_archive.read_bytes()
    assert sha(raw) == PRIOR_SHA, "Input must be the exact reviewed Repack02 archive"
    old = zipfile.ZipFile(io.BytesIO(raw))
    assert old.testzip() is None
    assert len(old.namelist()) == len(set(old.namelist())) == 31
    payloads = {n.removeprefix("packet/"): old.read(n) for n in old.namelist()}
    prior_manifest = json.loads(payloads["MANIFEST.json"])
    assert set(payloads) == {x["path"] for x in prior_manifest["files"]} | {"MANIFEST.json"}
    for entry in prior_manifest["files"]:
        assert len(payloads[entry["path"]]) == entry["bytes"]
        assert sha(payloads[entry["path"]]) == entry["sha256"]

    nested = zipfile.ZipFile(io.BytesIO(payloads["sources/W07_Repack01_TESTONLY.zip"]))
    engine = nested.read("sources/rules/WIZARD_CLASS_ENGINE.md")
    assert sha(engine) == "208b5ec1332c55702296448a6b09c32ca770b24674f909bdcba90b106a8fda6b"
    payloads[ENGINE_MEMBER] = engine
    profile = json.loads(payloads["sources/W07_BOUND_ACTOR_PROFILES_351fe708.json"])["Wizard20"]
    assert profile["automaticCards"][1]["id"] == CARD
    assert "always-prepared class matrices" in engine.decode().splitlines()[43]

    replay = json.loads(payloads["W03_REPLAY_400.json"])
    untouched_initial = copy.deepcopy(replay["stateSnapshots"][0])
    for snap in replay["stateSnapshots"][1:]:
        for actor_id in ("B", "D"):
            readiness(snap["state"], actor_id)
        snap["state"]["fixture"]["counterspellReadinessPremises"] = {
            "scope": "TEST_ONLY R6 repair; existing B/D bodies and focus items only",
            "actors": ["B", "D"], "campaignFact": False,
            "noActionReactionOrRefreshGranted": True,
        }
    commit = replay["events"][3]
    pending_state = replay["stateSnapshots"][4]["state"]
    window = commit["authoredInputs"]["counterspellWindow"]
    for index, actor_id in ((1, "B"), (3, "D")):
        window["dispositions"][index] = responder(pending_state, actor_id)
    window["eligibleResponders"] = ["B", "D"]
    window["potentialRespondersWithUnadjudicatedEligibility"] = [
        row["actorId"] for row in window["dispositions"] if row["eligibility"] == "unadjudicated"
    ]
    window["eligibilityAdjudication"] = (
        "B and D are source-qualified eligible responders and explicitly decline. "
        "A's self-response remains no-attempt with eligibility unadjudicated; no self-counter prohibition is adopted. "
        "Other existing no-attempt rows do not claim eligibility or a response."
    )
    window["decisionOrder"] = ["B", "D"]
    window["noResponseCastCreated"] = True
    pending_state["pendingCast"]["counterspellWindow"] = copy.deepcopy(window)
    pending_state["pendingCast"]["counterspellWindow"]["status"] = "OPEN_DECISIONS_RECORDED_BEFORE_RESOLUTION"
    pending_state["pendingCastStack"] = copy.deepcopy(pending_state["pendingCastStack"])
    for pending in pending_state["pendingCastStack"]:
        if isinstance(pending, dict) and pending.get("castId") == pending_state["pendingCast"]["castId"]:
            pending["counterspellWindow"] = copy.deepcopy(pending_state["pendingCast"]["counterspellWindow"])
    replay["id"] = "PG327-W03-LICH-TAXONOMY-WITNESS400-REPACK03"
    replay["supersedes"] = {"commit": PRIOR_COMMIT, "archiveSha256": PRIOR_SHA, "scope": "R6 only"}
    snapshots = {snap["id"]: snap for snap in replay["stateSnapshots"]}
    for snap in snapshots.values():
        snap["stateSha256"] = sha(canonical(snap["state"]))
    for event in replay["events"]:
        before = snapshots[event["beforeSnapshot"]]["state"]
        after = snapshots[event["afterSnapshot"]]["state"]
        event["beforeStateSha256"] = sha(canonical(before))
        event["afterStateSha256"] = sha(canonical(after))
        event["forwardPatch"] = delta(before, after)
        event["inversePatch"] = delta(after, before)
    assert replay["stateSnapshots"][0] == untouched_initial
    payloads["W03_REPLAY_400.json"] = encode(replay)

    scenario = json.loads(payloads["W03_SCENARIO_400_TESTONLY.json"])
    scenario["gateSetupCast"]["counterspellDisposition"] = copy.deepcopy(window)
    scenario["counterspellRepairScope"] = "R6 only; no changes to ritual, Gate, source rules or other witness predicates"
    payloads["W03_SCENARIO_400_TESTONLY.json"] = encode(scenario)
    bindings = json.loads(payloads["SOURCE_BINDINGS_400.json"])
    bindings["sourceFiles"].append({
        "member": ENGINE_MEMBER,
        "repositoryPath": "DescentReviewChanges/ReviewBible/docs/mechanics/classes/wizard.md",
        "sourceCommit": "351fe708ab21d1d63e5301f16336adf3712bfbf0",
        "representation": "Exact bytes extracted from preserved sealed W07 archive",
        "containerMember": "sources/W07_Repack01_TESTONLY.zip",
        "containerSha256": sha(payloads["sources/W07_Repack01_TESTONLY.zip"]),
        "nestedMember": "sources/rules/WIZARD_CLASS_ENGINE.md", "bytes": len(engine), "sha256": sha(engine),
    })
    bindings["counterspellR6"] = {
        "card": PROFILE_REF,
        "alwaysPreparedTextLocator": ENGINE_MEMBER + "#L44",
        "componentWitnessPrecedent": "sources/W07_GUST_CORPSE_CASE_363.json#/events/2/before/pendingCast/counterspellWindow/eligibleReactors/0",
        "noCatalogCounterspellSubstitution": True, "noNewRule": True,
    }
    payloads["SOURCE_BINDINGS_400.json"] = encode(bindings)
    repair = json.loads(payloads["DIRECTOR_REVIEW_REPAIR_MAP_400_REPACK02.json"])
    repair["id"] = "DIRECTOR-REVIEW-REPAIR-MAP-W03-400-REPACK03"
    repair["repairs"][5]["correction"] = "Source-qualified B/D eligibility, exact perception/components/readiness, explicit eligible declines and zero response expenditure; A self-response remains unadjudicated no-attempt."
    payloads["DIRECTOR_REVIEW_REPAIR_MAP_400_REPACK02.json"] = encode(repair)
    audit = json.loads(payloads["LOCAL_AUDIT_400.json"])
    audit["id"] = "PG327-W03-WITNESS-400-REPACK03-BUILD-AUDIT"
    audit["result"] = "REQUIRES_INDEPENDENT_VERIFIER"
    audit["claims"] = "Retained prior checks plus R6 repair; independent verifier must validate before any review disposition."
    audit["checks"]["sourceBoundEligibleBDCounterspellDeclines"] = "VERIFY_INDEPENDENTLY"
    payloads["LOCAL_AUDIT_400.json"] = encode(audit)
    payloads["COUNTERSPELL_R6_REPAIR_400_REPACK03.json"] = encode({
        "id": "W03-400-R6-REPACK03", "status": "TEST_ONLY_REPAIR_FOR_REVIEW",
        "priorCommit": PRIOR_COMMIT, "priorArchiveSha256": PRIOR_SHA,
        "sourceRuleChanged": False, "newCampaignFact": False,
        "changedPredicate": "B/D actual source-bound eligibility before explicit cost-free declines",
        "actorIds": ["B", "D"], "card": PROFILE_REF,
        "existingPassedResidualsPreserved": ["R1", "R2", "R3", "R4", "R5", "R7"],
        "acceptedIds": [], "appliedIds": [], "applicationAuthorized": False,
    })
    payloads["README.md"] = (
        "# W03 Witness400 Repack03 — R6 correction\n\n"
        "Repairs only B/D Counterspell eligibility in the exact reviewed Repack02. "
        "The automatic always-prepared Wizard class card, existing 60-foot window, Reaction, 3 RP and recharge rules are unchanged. "
        "Both eligible responders explicitly decline; no response roll, cost, cooldown, strain or casting history is created. "
        "Opening hand custody, perception and readiness are reversible TEST_ONLY premises. "
        "Historical /initial and every source payload remain preserved.\n\n"
        "Builder and independent verifier are adjacent repository scripts. Run the verifier with this archive and the pinned prior archive. "
        "This build does not itself seal W03, accept/apply Gate, promote canon or mutate Queue361.\n"
    ).encode()
    payloads["DIRECTOR_REVIEW_REQUEST_400.md"] = (
        "# Focused R6 correction\n\nReview B/D source-bound Counterspell eligibility and cost-free declines. "
        "Recheck dependent snapshots, patches, hashes and package records; preserve R1–R5/R7 and all source boundaries. "
        "A separate explicit Director ruling controls any seal or identity acceptance.\n"
    ).encode()
    del payloads["MANIFEST.json"]
    payloads["MANIFEST.json"] = encode({
        "id": "W03-400-REPACK03-MANIFEST", "status": "TEST_ONLY_REVIEW_EVIDENCE",
        "fileCountExcludingManifest": len(payloads),
        "files": [{"path": n, "bytes": len(v), "sha256": sha(v)} for n, v in sorted(payloads.items())],
    })
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / ".gitattributes").write_text("** -text !eol\npacket/sources/** -diff -whitespace\n*.zip filter=lfs diff=lfs merge=lfs -text\n", encoding="utf-8")
    for name, content in payloads.items():
        target = OUT / "packet" / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(content)
    with zipfile.ZipFile(OUT / NAME, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for name, content in sorted(payloads.items()):
            info = zipfile.ZipInfo("packet/" + name, (2026, 11, 1, 0, 0, 0))
            info.external_attr = 0o100644 << 16
            archive.writestr(info, content, compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)
    with zipfile.ZipFile(OUT / NAME) as archive:
        members = [{"path": i.filename, "bytes": i.file_size, "sha256": sha(archive.read(i)), "crc32": format(i.CRC, "08x")} for i in archive.infolist()]
    delivery = {
        "id": "W03-400-REPACK03-DELIVERY", "status": "AWAITING_INDEPENDENT_REVIEW",
        "archive": {"filename": NAME, "bytes": (OUT / NAME).stat().st_size, "sha256": sha((OUT / NAME).read_bytes()), "zipMemberCount": len(members), "zipMembers": members},
        "builder": {"path": str(Path(__file__).relative_to(REPO)), "sha256": sha(Path(__file__).read_bytes())},
        "supersedes": {"commit": PRIOR_COMMIT, "archiveSha256": PRIOR_SHA, "historicalArchiveUnchanged": True},
        "scope": "TEST_ONLY R6 repair; no identity, queue or canonical mutation",
        "queue": {"applied": 828, "pending": 20, "acceptedUnapplied": 0},
        "acceptedIds": [], "appliedIds": [], "applicationAuthorized": False,
    }
    (OUT / "ARCHIVE_DELIVERY_400_REPACK03.json").write_bytes(encode(delivery))
    print(json.dumps({"archive": str(OUT / NAME), "sha256": delivery["archive"]["sha256"], "bytes": delivery["archive"]["bytes"], "members": len(members)}))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-archive", type=Path, default=PRIOR_DIR / PRIOR_NAME)
    build(parser.parse_args().source_archive)
