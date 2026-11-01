from __future__ import annotations

import copy
import hashlib
import json
import math
import sys
import zipfile
from io import BytesIO
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REPO = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(ROOT))
import build_fortress_closure_intake_367 as intake

SRCZIP = ROOT / "fortress_w08_manifest_binding_repair_397" / "DD_Rank9_ConjureDemiplaneFortress_PG328-W08_FixedEntryAnchor396_ManifestRepair397_TESTONLY.zip"
QUEUE = ROOT / "CURRENT_SPELL_QUEUE_404.json"
HANDOFF = ROOT / "CURRENT_HANDOFF_404.json"
INTAKE = ROOT / "conjure_demiplane_fortress_closure_intake_367"
OUT = ROOT / "fortress_w08_occupied_antimagic_witness_412_repack01"
ZIPNAME = "DD_Rank9_ConjureDemiplaneFortress_PG328_W08_OccupiedAntimagicWitness_412_Repack01_TESTONLY.zip"
CASE_ID = "PG328-W08-OCCUPIED-ANTIMAGIC-WITNESS-412-TESTONLY"
CASE_FILE = "PG328_W08_OCCUPIED_ANTIMAGIC_INTEGRATED_WITNESS_412_REPACK01_TESTONLY.json"
Q27_SETTLEMENT_EVENT_ID = CASE_ID + ":Q27-SETTLEMENT"
PARENT_ID = "RANK9PLANARGATES5129-CONJURE-DEMIPLANE-FORTRESS-B/occupied-antimagic"
PARENT_MEMBER = "evidence/packet328/prior/Return284_cases/RANK9PLANARGATES5129-CONJURE-DEMIPLANE-FORTRESS-B__occupied-antimagic.json"
SPACE = PARENT_ID + "/cast1/space"
FORTRESS_EFFECT = PARENT_ID + "/cast1"
FIELD_CAST = "PG328-W08/occupied-antimagic/antimagic-field-cast1"
ORIGIN = "fixture:origin"
PANEL_ID = "W08-FLOOR-PANEL-A-01"
RAISED = 1.0 / 12.0
CENTER = [18.5, 14.0, 1.0 / 24.0]
CONTACT = [17.5, 12.25, 1.0 / 24.0]
CASTER_LOE_FROM_BODY = [17.5, 12.0, 5.583333333333333]

IDS = {
    "package": "w08.source.package397", "archive": "w08.source.held-archive",
    "parent": "w08.source.parent-case", "queue": "w08.authority.queue404",
    "handoff": "w08.authority.handoff404", "blocker": "w08.authority.blocker367",
    "coverage": "w08.authority.coverage367", "adoption": "w08.owner.adoption412",
    "panel": "w08.proposal.panel396", "support": "w08.proposal.support396",
    "carrier": "w08.proposal.carrier396", "fieldend": "w08.proposal.fieldend386",
    "model": "w08.source.antimagic149", "profile": "w08.source.wizard20",
    "wizard": "w08.source.wizard", "combat": "w08.source.combat",
    "body": "w08.source.body", "rules": "w08.source.pg328-rules",
    "procedure": "w08.source.fortress-procedure", "catalog": "w08.authority.catalog366",
    "review395": "w08.director.review395", "review397": "w08.director.review397",
    "review412": "w08.director.witness-review412",
    "seal03": "w08.authority.seal-w03", "seal06": "w08.authority.seal-w06",
    "seal07": "w08.authority.seal-w07",
}


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def file_sha(path: Path) -> str:
    return sha(path.read_bytes())


def write_json(path: Path, obj: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def json_bytes(obj: object) -> bytes:
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8") + b"\n"


def read_json(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def get_member(z: zipfile.ZipFile, name: str) -> bytes:
    if name not in z.namelist():
        raise AssertionError(f"Missing package member: {name}")
    return z.read(name)


def add(payload: Path, bindings: list[dict], binding_id: str, dest: str, data: bytes,
        source: str, purpose: str, pointers: list[str] | None = None) -> Path:
    out = payload / dest
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_bytes(data)
    bindings.append({"id": binding_id, "path": dest, "bytes": len(data), "sha256": sha(data),
                     "source": source, "purpose": purpose, "pointers": pointers or []})
    return out


def distance(a: list[float], b: list[float]) -> float:
    return math.sqrt(sum((a[i] - b[i]) ** 2 for i in range(3)))


def bounds_from_axes(b: dict) -> dict:
    return {axis: list(b[axis]) for axis in ("x", "y", "z")}


def body_bounds(feet: list[float], size: list[float]) -> dict:
    return {"x": [feet[0]-size[0]/2, feet[0]+size[0]/2],
            "y": [feet[1]-size[1]/2, feet[1]+size[1]/2],
            "z": [feet[2], feet[2]+size[2]]}


def bounds_center(b: dict) -> list[float]:
    return [(b[a][0]+b[a][1])/2 for a in ("x", "y", "z")]


def segment_hits_box(a: list[float], b: list[float], box: dict, eps: float = 1e-9) -> bool:
    low = [box[k][0] for k in ("x", "y", "z")]
    high = [box[k][1] for k in ("x", "y", "z")]
    delta = [b[i]-a[i] for i in range(3)]
    enter, leave = 0.0, 1.0
    for i in range(3):
        if abs(delta[i]) < eps:
            if a[i] <= low[i]+eps or a[i] >= high[i]-eps:
                return False
            continue
        t0, t1 = (low[i]-a[i])/delta[i], (high[i]-a[i])/delta[i]
        enter, leave = max(enter, min(t0, t1)), min(leave, max(t0, t1))
        if leave-enter <= eps:
            return False
    return leave-enter > eps and enter < 1-eps and leave > eps


def main() -> None:
    package_bytes = SRCZIP.read_bytes()
    if sha(package_bytes) != "642659ff92f5364806a33288363fef9c3c6dd1912703638bf2598d5abab675f7":
        raise AssertionError("397 source package hash changed.")
    out = OUT
    payload = out / "payload"
    payload.mkdir(parents=True, exist_ok=True)
    bindings: list[dict] = []
    z = zipfile.ZipFile(SRCZIP)

    add(payload, bindings, IDS["package"], "authority/REFERENCE_PACKAGE_397.zip", package_bytes,
        str(SRCZIP.relative_to(REPO)).replace("\\", "/"), "Exact Director-reviewed 397 package.")
    held = (INTAKE / "payload/authority/PG328_HELD_ARCHIVE.zip").read_bytes()
    if sha(held) != "47af8e23be318210229f7fd2b360be809b2b7ed5d73b08abcbeaf7a078c3f1f4":
        raise AssertionError("Held archive hash mismatch.")
    parent_bytes = zipfile.ZipFile(BytesIO(held)).read(PARENT_MEMBER)
    if sha(parent_bytes) != "f12414164a641a6b8912b43e8f426f027772f3a58d92dbadfcbd45b4f5b14900":
        raise AssertionError("Return284 parent case hash mismatch.")
    parent = json.loads(parent_bytes.decode("utf-8-sig"))
    parent_state = copy.deepcopy(parent["final"])
    if intake.digest(parent_state) != "daedd7c4fd0693f445ba6b36569b55eb3520dd0ac5f181bf85774dac498da833":
        raise AssertionError("Return284 final state hash mismatch.")
    add(payload, bindings, IDS["archive"], "authority/PG328_HELD_ARCHIVE.zip", held,
        "intake367/payload/authority/PG328_HELD_ARCHIVE.zip", "Immutable parent archive.")
    add(payload, bindings, IDS["parent"], "parent/RETURN284_OCCUPIED_ANTIMAGIC_CASE.json", parent_bytes,
        f"PG328_HELD_ARCHIVE.zip::{PARENT_MEMBER}", "Exact held parent case.", ["/final", "/events/6"])

    member_map = {
        IDS["panel"]: ("payload/proposals/PG328-W01_W08_OCCUPIED_PANEL_GEOMETRY_PROPOSAL_396_TESTONLY.json",
                       "proposals/PG328-W01_W08_OCCUPIED_PANEL_GEOMETRY_PROPOSAL_396_TESTONLY.json"),
        IDS["support"]: ("payload/proposals/OWNER_PG328_W08_SUPPORT_COVER_CONTRACT_396_TESTONLY.json",
                         "proposals/OWNER_PG328_W08_SUPPORT_COVER_CONTRACT_396_TESTONLY.json"),
        IDS["carrier"]: ("payload/proposals/PG328-W08_Q27_CARRIER_BOUNDS_PROPOSAL_396_TESTONLY.json",
                         "proposals/PG328-W08_Q27_CARRIER_BOUNDS_PROPOSAL_396_TESTONLY.json"),
        IDS["fieldend"]: ("payload/proposals/OWNER_PG328_W08_FIELD_TERMINATION_PROPOSAL_386_TESTONLY.json",
                          "proposals/OWNER_PG328_W08_FIELD_TERMINATION_PROPOSAL_386_TESTONLY.json"),
    }
    for bind, (member, dest) in member_map.items():
        add(payload, bindings, bind, dest, get_member(z, member), f"REFERENCE_PACKAGE_397.zip::{member}",
            "Director-reviewed W08 proposal adopted for this TEST_ONLY witness.", [""])

    source_map = {
        IDS["model"]: ("payload/sources/ANTIMAGIC_FIELD_MODEL_149.json", "sources/ANTIMAGIC_FIELD_MODEL_149.json", []),
        IDS["profile"]: ("payload/sources/RETURN284_WIZARD20_PROFILE_TESTONLY.json", "sources/RETURN284_WIZARD20_PROFILE_TESTONLY.json", []),
        IDS["wizard"]: ("payload/sources/wizard.json", "sources/wizard.json", []),
        IDS["combat"]: ("payload/sources/COMBAT_ACTION_PLAYTEST.md", "sources/COMBAT_ACTION_PLAYTEST.md", []),
        IDS["body"]: ("payload/sources/BODY_EQUIPMENT_PLAYTEST.md", "sources/BODY_EQUIPMENT_PLAYTEST.md", []),
        IDS["rules"]: ("payload/rules/PG328_QUESTION_DISPOSITIONS.json", "rules/PG328_QUESTION_DISPOSITIONS.json",
                       ["/questions/2/answer", "/questions/6/answer"]),
        IDS["procedure"]: ("payload/rules/PG328_PROCEDURE_CURRENT.json", "rules/PG328_PROCEDURE_CURRENT.json", [""]),
        IDS["catalog"]: ("payload/authority/CURRENT_ANTIMAGIC_FIELD_CATALOG_CARD_366.json",
                         "authority/CURRENT_ANTIMAGIC_FIELD_CATALOG_CARD_366.json", [""]),
        IDS["review395"]: ("payload/reviews/DIRECTOR_PG328_W08_SUPPORT_COVER_REVIEW_395.json",
                           "reviews/DIRECTOR_PG328_W08_SUPPORT_COVER_REVIEW_395.json", [""]),
    }
    for bind, (member, dest, pointers) in source_map.items():
        add(payload, bindings, bind, dest, get_member(z, member), f"REFERENCE_PACKAGE_397.zip::{member}",
            "Bound source/review record.", pointers)

    authority_files = [
        (IDS["queue"], QUEUE, "authority/CURRENT_SPELL_QUEUE_404.json", "Current 829/19/0 queue."),
        (IDS["handoff"], HANDOFF, "authority/CURRENT_HANDOFF_404.json", "Current queue priority/handoff snapshot."),
        (IDS["blocker"], INTAKE / "payload/authority/PG328_BLOCKER_REASSESSMENT.json",
         "authority/PG328_BLOCKER_REASSESSMENT_367.json", "Historical residual map; queue404 controls counts."),
        (IDS["coverage"], INTAKE / "payload/COVERAGE_MAP_367.json",
         "authority/COVERAGE_MAP_367.json", "Fortress witness coverage map."),
        (IDS["seal03"], INTAKE / "OWNER_PG328_W03_TESTONLY_EVIDENCE_SEAL_395.json",
         "authority/OWNER_PG328_W03_TESTONLY_EVIDENCE_SEAL_395.json", "Prior W03 scoped test-only seal."),
        (IDS["seal06"], ROOT / "fortress_w06_permissions_reentry_375_repack03/DIRECTOR_SEAL_375_REPACK03.json",
         "authority/DIRECTOR_SEAL_375_REPACK03.json", "Prior W06 scoped test-only seal."),
        (IDS["seal07"], ROOT / "fortress_w07_real_dispel_374_repack02/DIRECTOR_SEAL_374_REPACK02.json",
         "authority/DIRECTOR_SEAL_374_REPACK02.json", "Prior W07 scoped test-only seal."),
    ]
    for bind, path, dest, purpose in authority_files:
        add(payload, bindings, bind, dest, path.read_bytes(),
            str(path.relative_to(REPO)).replace("\\", "/"), purpose, [""] if dest.endswith(".json") else [])

    review397 = ROOT / "fortress_w08_manifest_binding_repair_397/DIRECTOR_PG328_W08_MANIFEST_REVIEW_397.json"
    add(payload, bindings, IDS["review397"], "reviews/DIRECTOR_PG328_W08_MANIFEST_REVIEW_397.json",
        review397.read_bytes(), str(review397.relative_to(REPO)).replace("\\", "/"),
        "Director's 397 packaging pass and exact remaining adoption terms.", [""])

    profile = json.loads(get_member(z, "payload/sources/RETURN284_WIZARD20_PROFILE_TESTONLY.json"))
    model = json.loads(get_member(z, "payload/sources/ANTIMAGIC_FIELD_MODEL_149.json"))
    prebuild = json.loads(get_member(z, "payload/PG328-W08_OCCUPIED_ANTIMAGIC_PREBUILD_TESTONLY.json"))
    geom = json.loads(get_member(z, member_map[IDS["panel"]][0]))
    support_doc = json.loads(get_member(z, member_map[IDS["support"]][0]))
    carrier = json.loads(get_member(z, member_map[IDS["carrier"]][0]))
    termination = json.loads(get_member(z, member_map[IDS["fieldend"]][0]))
    queue = read_json(QUEUE)
    handoff = read_json(HANDOFF)
    if handoff["authority"]["reviewedApplied"] != 829 or handoff["authority"]["pending"] != 19 or handoff["authority"]["acceptedUnapplied"] != 0:
        raise AssertionError("Current handoff is not 829/19/0.")
    if sha(QUEUE.read_bytes()) != handoff["queue"]["sha256"]:
        raise AssertionError("Handoff404 queue hash mismatch.")
    if queue["currentAuthority"] != handoff["authority"]:
        raise AssertionError("Queue404/handoff authority counts diverge.")
    if queue["nextIdentity"] != "conjure-demiplane-fortress":
        raise AssertionError("Queue404 priority no longer starts with Fortress.")
    if "antimagic-field" not in profile["ordinaryLearning"][14]["selected"] or profile["spellbook"][52] != "antimagic-field" or profile["prepared"][15] != "antimagic-field":
        raise AssertionError("Wizard20 access/preparation bindings changed.")
    if model["spells"][2]["id"] != "antimagic-field":
        raise AssertionError("Model /spells/2 is not Antimagic Field.")
    catalog = json.loads(get_member(z, "payload/authority/CURRENT_ANTIMAGIC_FIELD_CATALOG_CARD_366.json"))
    if "pending" not in json.dumps(catalog).lower() and "blocked" not in json.dumps(catalog).lower():
        raise AssertionError("Current identity hold is not shown in the bound catalog card.")

    panel = copy.deepcopy(support_doc["proposedPanelContract"])
    support_center = support_doc["coverTreatment"]["candidateCenterFeet"]
    contact = panel["suppressionLocusCandidate"]["pointFeet"]
    if support_center != CENTER or contact != CONTACT or panel["supportsMassLb"] != 162:
        raise AssertionError("Candidate geometry/load differs from the Director-reviewed 396 contract.")
    tower = geom["proposedLocalFortressInstantiation"]["southwestTower"]
    arr = {x["id"]: x for x in carrier["arrangement"]}
    pre_items = {k: copy.deepcopy(v["preCastWorldBoundsFeet"]) for k, v in arr.items()}
    post_items = {k: copy.deepcopy(v["postReturnWorldBoundsFeet"]) for k, v in arr.items()}
    panel_bounds = bounds_from_axes(panel["volumeFeet"])
    raised_feet = [15.0, 10.0, RAISED]
    body_size = [5.0, 5.0, 6.0]
    pre_body = body_bounds(raised_feet, body_size)
    anchor = copy.deepcopy(carrier["postReturnCheck"]["exteriorFeetAnchor"])
    post_body = body_bounds(anchor, body_size)
    center_range = distance(raised_feet, CENTER)
    radius = float(prebuild["proposedCastState"]["proposedCastAfterRefresh"]["fieldRadiusFeet"])
    max_panel_range = max(distance(CENTER, [x, y, z])
                          for x in panel_bounds["x"] for y in panel_bounds["y"] for z in panel_bounds["z"])
    walls = tower["wallSolids"]
    stairs = tower["stairPath"]["boundsFeet"]
    caster_body_hit = segment_hits_box(CASTER_LOE_FROM_BODY, CENTER, pre_body)
    caster_item_hits = [item_id for item_id, bounds in pre_items.items()
                        if segment_hits_box(CASTER_LOE_FROM_BODY, CENTER, bounds_from_axes(bounds))]
    caster_panel_hit = segment_hits_box(CASTER_LOE_FROM_BODY, CENTER, panel_bounds)
    caster_wall_hits = [w["id"] for w in walls if segment_hits_box(CASTER_LOE_FROM_BODY, CENTER, w)]
    caster_stair_hit = segment_hits_box(CASTER_LOE_FROM_BODY, CENTER, stairs)
    panel_wall_hits = [w["id"] for w in walls if segment_hits_box(CENTER, CONTACT, w)]
    panel_stair_hit = segment_hits_box(CENTER, CONTACT, stairs)
    panel_penetration = segment_hits_box(CENTER, CONTACT, panel_bounds)
    if round(center_range, 9) != 5.315236223 or round(max_panel_range, 9) != 8.846001137:
        raise AssertionError(f"Unexpected distances: {center_range}, {max_panel_range}")
    if (center_range > 20 or max_panel_range > radius or caster_body_hit or caster_item_hits or caster_panel_hit
            or caster_wall_hits or caster_stair_hit or panel_wall_hits or panel_stair_hit or panel_penetration):
        raise AssertionError("Perception/LoE/field coverage geometry failed.")
    if pre_body["z"][0] != panel["topSurfaceZ"] or panel_bounds["z"] != [0.0, RAISED]:
        raise AssertionError("A is not supported at the adopted raised panel top.")
    if parent_state["actors"]["A"]["concentration"] is not None or parent_state["actors"]["A"]["RP"] != 54:
        raise AssertionError("Inherited cast preconditions changed.")

    owner_adoption = {        "id": "OWNER-PG328-W08-TESTONLY-ADOPTION-412",
        "recordedAtLocal": "2026-11-01",
        "ownerAuthorization": {
            "source": "User response in GPT Dungeon Crawler conversation Review SH202 B02 Archive",
            "verbatim": "adopt it for fuck sake, you are the director",
            "scope": "The exact three W08 adoption terms listed in Director's preceding readback."
        },
        "directorReadback": {
            "source": "GPT Dungeon Crawler Director response in the same conversation",
            "verbatim": "Adopted for PG328-W08 only. Your instruction supplies owner authorization; this message records the Director's scoped TEST_ONLY adoption.",
            "conversation": "https://chatgpt.com/g/g-p-67f17555a8dc8191a2b5b81e6d8adc12-dungeon-crawler/c/6ae66c6d-2d08-83ea-a1fa-042d649855a2",
        },
        "adoptedTerms": [
            {"panelId": PANEL_ID, "zFeet": [0, RAISED], "supportDatumZ": 0, "supportsWhole5x5Footprint": True,
             "supportedMassLb": 162, "noNewSpace": True, "noIndependentFooting": True},
            {"separateTestOnlyInitializationAfter": "/events/6", "raiseAAndCarriedItemsFeet": RAISED,
             "fixedQ27ClosureAnchorFeet": anchor},
            {"proposal": "OWNER-PG328-W08-ANTIMAGIC-FIELD-TERMINATION-PROPOSAL-386",
             "sha256": sha((payload / "proposals/OWNER_PG328_W08_FIELD_TERMINATION_PROPOSAL_386_TESTONLY.json").read_bytes()),
             "afterQ27Settlement": True, "noRelocation": True, "noRefund": True,
             "preserveIdentityPaymentHistory": True, "endConcentrationLink": True,
             "deadlineWorldElapsedSeconds": 66.1, "onlyIfEstablishedAtWorld": 6.1},
        ],
        "limits": {"testOnly": True, "campaignOccurrence": False, "fixtureMutated": False,
                   "canonicalRuleChanged": False, "identityAcceptedOrApplied": False,
                   "fortressAcceptedOrApplied": False, "queueChanged": False, "holdChanged": False},
    }
    add(payload, bindings, IDS["adoption"], "owner/OWNER_PG328_W08_TESTONLY_ADOPTION_412.json",
        json_bytes(owner_adoption), "Owner instruction and Director readback in cited GPT conversation.",
        "Scoped W08 authorization; no canonical or live-state effect.")

    director_review = {
        "id": "DIRECTOR-PG328-W08-WITNESS-REVIEW-412",
        "source": "GPT Dungeon Crawler Director response in the cited conversation.",
        "conversation": "https://chatgpt.com/g/g-p-67f17555a8dc8191a2b5b81e6d8adc12-dungeon-crawler/c/6ae66c6d-2d08-83ea-a1fa-042d649855a2",
        "reviewedArtifact": {
            "fileName": "DD_Rank9_ConjureDemiplaneFortress_PG328_W08_OccupiedAntimagicWitness_412_TESTONLY.zip",
            "sha256": "a5bf919ba80563ff90a39c1a22ad91aae9ef18be5e1b2328c81783ad4b69192b",
            "terminalStateSha256": "a147692d6dc8f1a7021cd3cf20019405b91200eeaa77f0042e4e5cdbd34a64ef"
        },
        "disposition": "REPAIR_REQUIRED; UNSEALED",
        "passed": [
            "Archive and manifest bindings.",
            "All 16 forward transitions and 16 inverses; full reverse restores exact parent state.",
            "Scheduling, payment 54 to 33 RP, strain, counter window, occupied-panel contact, carrier fit, fixed return anchor [15,0,0], and field termination under adopted proposal 386."
        ],
        "requiredRepairs": [
            {
                "id": "W08-412-R1",
                "pointer": "/events/8/detail/preconditions/target/lineOfEffectFromFocusAnchorFeet",
                "issue": "The recorded origin [17.75,11,3.3333333333333335] lies inside focus-A; walls/stairs-only checks do not establish a clear caster line.",
                "requiredSegmentFeet": {
                    "fromExposedBodyBoundary": CASTER_LOE_FROM_BODY,
                    "toCenter": CENTER
                },
                "requiredClearance": ["caster body", "carried items", "panel", "walls", "stairs"],
                "retainPerceptionPremise": True,
                "geometryOrAdoptionChangeRequired": False
            },
            {
                "id": "W08-412-R2",
                "pointer": "/actors/A/lastArrivedFromPlaneKey",
                "issue": "After event 14 (/events/13), the arrival-provenance field still names fixture:origin.",
                "arrivalOriginPlaneKey": SPACE,
                "arrivalEventId": Q27_SETTLEMENT_EVENT_ID,
                "historicalAdmissionRecordMustRemainUnchanged": True
            },
            {
                "id": "W08-412-R3",
                "pointer": "/events/8/detail/preconditions/statusNote",
                "issue": "The static authored Antimagic Field procedure was accepted and applied under Return149; preserve qualifications and runtime restrictions without describing the procedure as still pending identity review.",
                "metadataCorrectionOnly": True
            }
        ],
        "followupClarification": {
            "source": "GPT Dungeon Crawler Director response to the field-name clarification in the same conversation.",
            "exactReadback": "Yes—use that exact representation. No different event-reference field name is required. Treat lastArrivedFromEventId as explicit branch-local trace metadata, not a new global schema rule.",
            "arrivalOriginPlaneKey": SPACE,
            "arrivalEventId": Q27_SETTLEMENT_EVENT_ID,
            "samePairInQ27TerminalReceipt": True,
            "propagateThroughSubsequentSnapshotsAndFinalState": True,
            "inverseRestoresPriorOrigin": True,
            "inverseRemovesEventReferenceFieldIfPreviouslyAbsent": True,
            "historicalAdmissionEventAndTransitReceiptsUnchanged": True,
            "noAdditionalOwnerPremiseRequired": True
        },
        "scope": {
            "queue": {"applied": 829, "pending": 19, "acceptedUnapplied": 0},
            "fortressIdentityAcceptedOrApplied": False,
            "PG200B06Held": True,
            "fixtureMutated": False,
            "canonicalRulesChanged": False,
            "sealIssued": False
        }
    }
    add(payload, bindings, IDS["review412"], "reviews/DIRECTOR_PG328_W08_WITNESS_REVIEW_412.json",
        json_bytes(director_review), "Exact current Director repair disposition for submitted packet 412.",
        "Source-bound repair instructions; no owner adoption or seal supplied.")

    binding_ids = {b["id"] for b in bindings}
    refs = set()

    state = copy.deepcopy(parent_state)
    initial = copy.deepcopy(state)
    events: list[dict] = []

    def advance(at: float) -> None:
        delta = round(float(at) - float(state["time"]), 6)
        if delta < -1e-9:
            raise AssertionError(f"Time moved backward: {state['time']} -> {at}")
        state["time"] = float(at)
        state["clock"]["elapsedSeconds"] = round(state["clock"]["elapsedSeconds"] + delta, 6)
        for key in ("OpeningRemaining", "HornRemaining"):
            state["clock"][key] = round(state["clock"][key] - delta, 6)

    def event(event_id: str, kind: str, at: float, detail: dict, sources: list[str], rationale: str, mutate) -> None:
        missing = set(sources) - binding_ids
        if missing:
            raise AssertionError(f"Unbound event sources: {missing}")
        before = copy.deepcopy(state)
        advance(at)
        mutate()
        state["processedEventIds"].append(event_id)
        after = copy.deepcopy(state)
        et = {"initiativeSeconds": float(at), "worldElapsedSeconds": float(state["clock"]["elapsedSeconds"])}
        record = intake.make_transition(event_id, kind, before, after, et, sources, rationale)
        record["detail"] = copy.deepcopy(detail)
        record["ordinal"] = len(events) + 1
        events.append(record)
        refs.update(sources)
        assert intake.apply_ops(before, record["forward"]) == after
        assert intake.apply_ops(after, record["inverse"]) == before

    branch_geom = {
        "status": "OWNER_ADOPTED_TEST_ONLY_BRANCH_GEOMETRY",
        "panel": {"id": PANEL_ID, "partOf": panel["partOf"], "boundsFeet": panel_bounds,
                  "AC": 17, "HP": 60, "currentHP": 60, "magicalExpressionActive": True,
                  "suppressed": False, "supportGraph": copy.deepcopy(panel), "supportedMassLb": 162},
        "layout": {"towerId": tower["id"], "boundsFeet": tower["boundsFeet"],
                   "wallSolids": tower["wallSolids"], "stairs": stairs,
                   "interior": tower["openInterior"], "light": "ordinary"},
        "A": {"feet": raised_feet, "bodyBoundsFeet": pre_body,
              "casterLoEFromExposedBodyBoundaryFeet": CASTER_LOE_FROM_BODY,
              "perceivedFieldCenter": CENTER},
        "carriedItems": {k: {"boundsFeet": pre_items[k], "attachment": arr[k]["relation"],
                             "owner": "A", "custodian": "A"} for k in pre_items},
        "fieldCenter": CENTER, "radiusFeet": radius, "fixedClosureAnchor": anchor,
        "testOnly": True,
    }

    def initialize() -> None:
        sp = state["spaces"][SPACE]
        if "w08TestOnly" in sp:
            raise AssertionError("W08 branch geometry already exists.")
        sp["w08TestOnly"] = copy.deepcopy(branch_geom)
        a = state["actors"]["A"]
        a["position"] = copy.deepcopy(raised_feet)
        a["w08TestOnlyBodyBoundsFeet"] = copy.deepcopy(pre_body)
        a["w08TestOnlyPlacement"] = {"historicalEntry": "/events/6", "historicalFeet": [15, 10, 0],
                                     "separateRaisedDeltaFeet": [0, 0, RAISED], "testOnly": True}
        for item_id, bounds in pre_items.items():
            state["items"][item_id]["w08TestOnlyGeometry"] = {
                "occupiedBoundsFeet": copy.deepcopy(bounds), "attachment": arr[item_id]["relation"],
                "sameIdentityAndCustody": True
            }

    event(CASE_ID+":BRANCH-INITIALIZATION", "TEST_ONLY_BRANCH_INITIALIZATION", 0.9,
          {"historicalEntryPointer": "/events/6", "historicalEventId": parent["events"][6]["id"],
           "historicalEntryUnchanged": True, "raiseAAndItemsByFeet": RAISED,
           "supportDatumZ": 0, "panelTopZ": RAISED, "fixedClosureAnchorFeet": anchor,
           "fixtureMutated": False},
          [IDS["parent"], IDS["panel"], IDS["support"], IDS["carrier"], IDS["adoption"]],
          "Create a separate adopted test branch after unchanged historical admission; the held parent bytes remain immutable.", initialize)

    def start_actor(actor_id: str, at: float) -> None:
        old = copy.deepcopy(state["actors"][actor_id])
        sch = old["regularSchedule"]
        assert abs(sch["nextStart"]-at) < 1e-6
        def mutate():
            a = state["actors"][actor_id]
            for r in a.get("recharge", {}).values():
                if r.get("roundsUntilReady", 0) > 0:
                    r["roundsUntilReady"] -= 1
                r["ready"] = r.get("roundsUntilReady", 0) == 0
            a.update({"action":1,"bonusAction":1,"reaction":1,"movement":a.get("speed",30),"magicThisTurn":False})
            s = a["regularSchedule"]
            s["starts"].append(at)
            s["nextStart"] = round(at+s["period"],6)
            s["budgetHistory"].append({"time":at,"action":1,"BA":1,"Reaction":1,
                                       "Move":a["movement"],"recharge":copy.deepcopy(a.get("recharge",{}))})
        event(f"{CASE_ID}:START:{actor_id}:{at:.1f}","REGULAR_START",at,
              {"actorId":actor_id,"pendingEndPreserved":sch["nextEnd"],
               "nextStartAfter":round(at+sch["period"],6),"noOpPass":actor_id in ("B","C","D")},
              [IDS["combat"]],"Resolve the already-scheduled regular START; refresh ordinary budgets and preserve pending END.",mutate)

    def end_actor(actor_id: str, at: float) -> None:
        old = copy.deepcopy(state["actors"][actor_id])
        sch = old["regularSchedule"]
        assert sch["starts"] and abs(sch["starts"][-1]+sch["endOffset"]-at)<1e-6 and abs(sch["nextEnd"]-at)<1e-6
        before_eff = copy.deepcopy(old.get("spellEfficiency"))
        after_eff = before_eff
        if actor_id == "A" and isinstance(before_eff, list):
            after_eff = [e for e in before_eff if e.get("until") is None or e["until"] > at+1e-8]
            if not after_eff: after_eff = None
        elif actor_id == "A" and isinstance(before_eff, dict) and before_eff.get("until", 99) <= at+1e-8:
            after_eff = None
        def mutate():
            a = state["actors"][actor_id]
            a["regularSchedule"]["ends"].append(at)
            a["regularSchedule"]["nextEnd"] = round(at+a["regularSchedule"]["period"],6)
            if actor_id == "A": a["spellEfficiency"] = copy.deepcopy(after_eff)
        event(f"{CASE_ID}:END:{actor_id}:{at:.1f}","REGULAR_END",at,
              {"actorId":actor_id,"pendingEndBefore":sch["nextEnd"],
               "pendingEndAfter":round(at+sch["period"],6),"noOpPass":actor_id in ("B","C","D"),
               "spellEfficiencyBefore":before_eff,"spellEfficiencyAfter":after_eff},
              [IDS["combat"]],"Resolve the pending END once, expire only due family markers, and create no extra turn.",mutate)

    start_actor("B",1.0); end_actor("B",1.9)
    start_actor("C",2.0); end_actor("C",2.9)
    start_actor("D",3.0); end_actor("D",3.9)
    start_actor("A",6.0)

    actor = state["actors"]["A"]
    assert actor["action"] == 1 and actor["RP"] == 54 and actor["concentration"] is None
    assert actor["Dissonance"] == 0 and actor["Refrain"] == 0
    assert actor["position"] == raised_feet and actor["voice"] and actor["focusAccessible"]
    assert "focus-A" in actor["equipment"] and actor["plane"] == SPACE
    assert (center_range <= 20 and not caster_body_hit and not caster_item_hits and not caster_panel_hit
            and not caster_wall_hits and not caster_stair_hit)

    responders = {
        "A":{"class":"Wizard","eligibility":"UNADJUDICATED","decision":"NO_SELF_ATTEMPT_TEST_ONLY","reactionSpent":False},
        "B":{"class":"Wizard","counterspellAccess":True,"crossPlaneEligibility":"NOT_ESTABLISHED",
             "decision":"NO_ATTEMPT_TEST_ONLY","reactionSpent":False},
        "C":{"class":"Cleric","counterspellAccess":"NOT_ESTABLISHED","decision":"NO_ATTEMPT_TEST_ONLY","reactionSpent":False},
        "D":{"class":"Wizard","counterspellAccess":True,"crossPlaneEligibility":"NOT_ESTABLISHED",
             "decision":"NO_ATTEMPT_TEST_ONLY","reactionSpent":False},
    }
    cast_inputs = {
        "access":{"ordinaryLearning":"/ordinaryLearning/14/selected/1","spellbook":"/spellbook/52",                  "prepared":"/prepared/15","actor":"Wizard20","rank":8,"school":"Abjuration"},
        "components":{"V":True,"S":True,"F":"focus-A accessible in left hand","rightHandFree":True},
        "target":{"plane":SPACE,"centerFeet":CENTER,"perceived":True,"distanceFeet":round(center_range,9),
                  "lineOfEffectSegmentFeet":{"fromExposedBodyBoundary":CASTER_LOE_FROM_BODY,"toCenter":CENTER},
                  "casterBoundClearance":{"casterBodyHit":caster_body_hit,"carriedItemHits":caster_item_hits,
                      "panelHit":caster_panel_hit,"wallHits":caster_wall_hits,"stairsHit":caster_stair_hit,
                      "allClear":not (caster_body_hit or caster_item_hits or caster_panel_hit or caster_wall_hits or caster_stair_hit)}},
        "field":{"radiusFeet":radius,"maxDurationSeconds":60,"deadlineWorldElapsedSeconds":66.1,
                 "farthestPanelCornerFeet":round(max_panel_range,9),"completePanelWithinRadius":True},
        "cost":{"baseRP":21,"additionalRP":0,"discount":False,"totalRP":21,"poolBefore":54,"poolAfter":33,
                "firstAntimagicFamilyCast":True},
        "statusNote":"Return149's authored static Antimagic Field procedure is accepted and applied. Preserve its catalog qualifications and runtime restrictions; this TEST_ONLY witness does not change runtime or campaign authorization."
    }

    def commit():
        a=state["actors"]["A"]
        a["action"]=0; a["RP"]-=21; a["lastSpell"]="antimagic-field"
        if "antimagic-field" not in a["preparedFamiliesUsed"]: a["preparedFamiliesUsed"].append("antimagic-field")
        a["spellHistory"].append({"castId":FIELD_CAST,"spellId":"antimagic-field","class":"Wizard",
            "school":"Abjuration","rank":8,"time":6.0,"worldElapsedSeconds":6.1,"cost":21,
            "firstPreparedFamily":True,"baseDissonance":0,"Refrain":0,"originPlane":SPACE,
            "targetCenterFeet":CENTER,"components":["V","S","F"],"concentration":True,"testOnly":True})
        a["resourceHistory"].append({"event":FIELD_CAST,"RP":-21,"poolAfter":33,"discount":False})
        a["magicThisTurn"]=True
        state["pendingCast"]={"castId":FIELD_CAST,"casterId":"A","spellId":"antimagic-field",
            "phase":"COMMITTED_COSTS_PAID","targetCenterFeet":CENTER,"costRp":21,
            "caseTime":6.0,"worldElapsedSeconds":6.1,"testOnly":True}
    event(CASE_ID+":CAST-COMMIT","CAST_COMMIT",6.0,
          {"preconditions":cast_inputs,"costsBeforeCounterWindow":True,"lastSpellChangesAtCommit":True},
          [IDS["model"],IDS["profile"],IDS["wizard"],IDS["support"],IDS["carrier"],IDS["adoption"],IDS["review412"]],
          "Commit the candidate paid cast only after refreshed lawful access, component, target, range, LoE, concentration, cadence, and cost checks.",commit)

    def open_window():
        p=state["pendingCast"]; assert p and p["phase"]=="COMMITTED_COSTS_PAID"
        p["phase"]="COUNTERSPELL_WINDOW_OPEN"; p["responders"]=copy.deepcopy(responders)
    event(CASE_ID+":COUNTERSPELL-OPEN","COUNTERSPELL_WINDOW_OPEN",6.0,
          {"responders":responders,"crossPlaneEligibilityNotEstablished":True},
          [IDS["model"],IDS["profile"],IDS["wizard"]],
          "Record the cast-time window without asserting B/D cross-plane eligibility or inventing C access.",open_window)

    def close_window():
        p=state["pendingCast"]; assert p and p["phase"]=="COUNTERSPELL_WINDOW_OPEN"
        p["phase"]="WINDOW_CLOSED_NO_COUNTER_ATTEMPT"; p["responses"]=[]; p["noResponseBranch"]=True
    event(CASE_ID+":COUNTERSPELL-CLOSE-NO-ATTEMPT","COUNTERSPELL_WINDOW_CLOSED_NO_ATTEMPT",6.0,
          {"responses":[],"noResponseBranch":True,"noRoll":True,"noReactionsOrResourcesSpent":True,
           "eligibility":{"A":"UNADJUDICATED","B":"NOT_ESTABLISHED","C":"NOT_ESTABLISHED","D":"NOT_ESTABLISHED"}},
          [IDS["model"],IDS["profile"],IDS["wizard"]],
          "Close this explicit no-attempt test branch; do not decide cross-plane counterspell eligibility.",close_window)

    def resolve():
        p=state["pendingCast"]; assert p and p["phase"]=="WINDOW_CLOSED_NO_COUNTER_ATTEMPT"
        state["effects"][FIELD_CAST]={
            "id":FIELD_CAST,"spellId":"antimagic-field","owner":"A","rootPlane":SPACE,
            "rootCastId":FIELD_CAST,"rank":8,"active":True,"suppressed":False,"deadline":66.1,
            "concentration":True,"concentrationLinkActive":True,"target":None,"centerFeet":CENTER,
            "centerPlane":SPACE,"radiusFeet":radius,"maximumDurationSeconds":60,
            "establishedAtWorldElapsedSeconds":6.1,"createdAtCaseTime":6.0,"fixedCenter":True,
            "testOnly":True,"terminalReceipt":None}
        a=state["actors"]["A"]; a["concentration"]=FIELD_CAST
        old=a.get("spellEfficiency")
        ledger=copy.deepcopy(old) if isinstance(old,list) else ([copy.deepcopy(old)] if old else [])
        ledger.append({"family":"antimagic-field","until":12.9,"worldUntil":13.0,
            "triggeredByCastId":FIELD_CAST,"status":"TEST_ONLY_UNSPENT",
            "noDiscountAppliedByThisCast":True,"noCanonicalStackingRuleAsserted":True})
        a["spellEfficiency"]=ledger
        state["pendingCast"]=None
    event(CASE_ID+":CAST-RESOLVE","CAST_RESOLUTION",6.0,
          {"effectId":FIELD_CAST,"centerFeet":CENTER,"radiusFeet":radius,"deadlineWorldElapsedSeconds":66.1,
           "spellEfficiency":"Separate TEST_ONLY family ledger preserves Fortress endpoint 6.9 and Antimagic endpoint 12.9; no universal stacking rule asserted."},
          [IDS["model"],IDS["adoption"]],
          "Resolve the paid no-response test cast at world 6.1; establish its fixed center and concentration.",resolve)
    def suppress_panel():
        ps=state["spaces"][SPACE]["w08TestOnly"]["panel"]
        assert state["effects"][FIELD_CAST]["active"] and ps["magicalExpressionActive"]
        ps["magicalExpressionActive"]=False; ps["suppressed"]=True; ps["suppressedBy"]=FIELD_CAST
        ps["suppressedAt"]={"caseTime":6.0,"worldElapsedSeconds":6.1}
        ps["HPBeforeSuppression"]=ps["currentHP"]; ps["HPAfterSuppression"]=ps["currentHP"]
    event(CASE_ID+":SUPPRESS-OCCUPIED-PANEL","TEST_ONLY_OCCUPIED_STRUCTURAL_EXPRESSION_SUPPRESSED",6.0,
          {"panelId":PANEL_ID,"fieldId":FIELD_CAST,"panelPointFeet":CONTACT,"fieldCenterFeet":CENTER,
           "farthestPanelCornerFeet":round(max_panel_range,9),"panelCompletelyInField":True,
           "raysClear":True,"panelPenetration":False,"occupiedBy":"A","damage":0,"hpChanged":False},
          [IDS["model"],IDS["rules"],IDS["panel"],IDS["support"]],
          "Field volume contacts the adopted exposed panel face and suppresses its magical expression without damage; Q27 follows in its own event.",suppress_panel)

    def settle():
        ps=state["spaces"][SPACE]["w08TestOnly"]["panel"]
        assert not ps["magicalExpressionActive"] and state["effects"][FIELD_CAST]["active"]
        fe=state["effects"][FORTRESS_EFFECT]
        fe["active"]=False
        fe["terminalReceipt"]={"reason":"PG9-Q27 occupied structural region suppressed",
            "eventTime":{"caseTime":6.0,"worldElapsedSeconds":6.1},"space":SPACE,
            "anchorPlane":ORIGIN,"anchorFeet":anchor,"settlementOrder":["A","focus-A","pack-A","cargo-A"],
            "carriedItemsStayWithCarrier":True,"looseItems":[],"corpses":[],"testOnly":True,
            "arrivalOriginPlaneKey":SPACE,"arrivalEventId":Q27_SETTLEMENT_EVENT_ID}
        state["spaces"][SPACE]["exists"]=False
        state["spaces"][SPACE]["w08TestOnly"]["terminalAt"]={"caseTime":6.0,"worldElapsedSeconds":6.1}
        a=state["actors"]["A"]; a["plane"]=ORIGIN; a["position"]=copy.deepcopy(anchor)
        a["lastArrivedFromPlaneKey"]=SPACE
        a["lastArrivedFromEventId"]=Q27_SETTLEMENT_EVENT_ID
        a["w08TestOnlyBodyBoundsFeet"]=copy.deepcopy(post_body)
        a["w08TestOnlyTerminalPlacement"]={"fromSpace":SPACE,"toPlane":ORIGIN,
            "feet":anchor,"bodyBoundsFeet":post_body,"cause":"PG9-Q27"}
        for i in ("focus-A","pack-A","cargo-A"):
            it=state["items"][i]; it["plane"]=ORIGIN; it["custodian"]="A"
            it["w08TestOnlyGeometry"]["occupiedBoundsFeet"]=copy.deepcopy(post_items[i])
            it["w08TestOnlyGeometry"]["placement"]="carried with A at the fixed closure anchor"
    event(Q27_SETTLEMENT_EVENT_ID,"TEST_ONLY_FORTRESS_Q27_TERMINAL_SETTLEMENT",6.0,
          {"trigger":"Suppression of occupied panel's magical structural expression","rulePointer":"/questions/6/answer",
           "anchorPlane":ORIGIN,"anchorFeet":anchor,"bodyBoundsFeet":post_body,"itemBoundsFeet":post_items,
           "order":["A","focus-A","pack-A","cargo-A"],"outsideActorsB_C_DUnchanged":True,
           "arrivalOriginPlaneKey":SPACE,"arrivalEventId":Q27_SETTLEMENT_EVENT_ID,
           "historicalAdmissionPointer":"/events/6","historicalAdmissionTransitReceiptUnchanged":True,
           "fieldRemainsActiveUntilNextSameTimeEvent":True},
          [IDS["rules"],IDS["carrier"],IDS["body"],IDS["adoption"],IDS["review412"]],
          "Apply only the bound Q27 whole-source settlement after panel suppression; retain A and the original carried items at the fixed adopted anchor.",settle)

    def end_field():
        f=state["effects"][FIELD_CAST]; a=state["actors"]["A"]
        assert not state["spaces"][SPACE]["exists"] and f["active"] and a["concentration"]==FIELD_CAST
        f["active"]=False; f["concentrationLinkActive"]=False
        f["endReason"]="OWNER-ADOPTED-PG328-W08-PROPOSAL-386"
        f["endedAt"]={"caseTime":6.0,"worldElapsedSeconds":6.1}
        f["terminalReceipt"]={"reason":f["endReason"],"centerPlaneHistoricalOnly":SPACE,
            "centerFeetHistoricalOnly":CENTER,"relocated":False,"refundRp":0,
            "originalDeadlineWorldElapsedSecondsPreserved":66.1,"historyPreserved":True,"testOnly":True}
        a["concentration"]=None
    event(CASE_ID+":FIELD-TERMINATION","TEST_ONLY_INDEPENDENT_FIELD_TERMINATION",6.0,
          {"proposal":IDS["fieldend"],"afterFortressQ27":True,"notRelocated":True,"refundRp":0,
           "concentrationEnded":True,"deadlineWorldElapsedSecondsPreserved":66.1},
          [IDS["fieldend"],IDS["adoption"],IDS["rules"]],
          "Terminate the independent field only after Q27, per the exact owner-adopted scoped proposal; preserve identity, payment, history and deadline.",end_field)

    end_actor("A",6.9)
    final = copy.deepcopy(state)
    current_authority = queue["currentAuthority"]
    case = {
        "id":CASE_ID,"spellId":"conjure-demiplane-fortress","witnessId":"PG328-W08",
        "mainCaseId":PARENT_ID,"kind":"integrated reversible TEST_ONLY branch",
        "status":"READY_FOR_DIRECTOR_REVIEW; TEST_ONLY; UNSEALED",
        "directorReviewRepairBinding":{"id":IDS["review412"],"reviewDisposition":"REPAIR_REQUIRED; UNSEALED",
            "repack":"Repack01","adoptionChanged":False},
        "holdIds":["PG200-B06"],
        "scope":{"campaignOccurrence":False,"runtimeCast":False,"fixtureMutated":False,
                 "canonicalRulesChanged":False,"identityAcceptedOrApplied":False,
                 "fortressAcceptedOrApplied":False,"queueChanged":False},
        "parentBinding":{"archiveMember":PARENT_MEMBER,"archiveSha256":sha(held),
                         "parentCaseSha256":sha(parent_bytes),"parentFinalStateSha256":intake.digest(parent_state),
                         "historicalAdmissionPointer":"/events/6"},        "authority":{"queuePath":"CURRENT_SPELL_QUEUE_404.json","queueSha256":sha(QUEUE.read_bytes()),
                     "reviewedApplied":current_authority["reviewedApplied"],"pending":current_authority["pending"],
                     "acceptedUnapplied":current_authority["acceptedUnapplied"],"nextIdentity":queue["nextIdentity"],
                     "queueDelta":{"applied":0,"pending":0,"acceptedUnapplied":0}},
        "sourceBindingIds":sorted(refs),"initial":initial,"initialSHA256":intake.digest(initial),
        "events":events,"final":final,"finalSHA256":intake.digest(final),
    }
    add(payload, bindings, "w08.case.integrated412", f"case/{CASE_FILE}",
        json_bytes(case),"Generated from exact 397 package source and immutable parent.","Reversible state/event branch.")

    src_bind_file = add(payload, bindings, "w08.meta.bindings412-repack01", "authority/SOURCE_BINDINGS_412_REPACK01.json",
                        json_bytes(bindings),"Generated from all packet source snapshots.","Hash and pointer binding index.")
    # Binding index intentionally lists all external sources and the case; its own self-hash is in the package manifest.
    for b in bindings:
        path=payload/b["path"]
        if not path.is_file() or sha(path.read_bytes())!=b["sha256"] or path.stat().st_size!=b["bytes"]:
            raise AssertionError(f"Binding failed: {b['path']}")
    if not refs <= {b["id"] for b in bindings}:
        raise AssertionError("An event source binding is missing.")

    forward=copy.deepcopy(initial)
    for e in events:
        if intake.digest(forward)!=e["beforeSHA256"]: raise AssertionError(f"Broken forward chain {e['id']}")
        forward=intake.apply_ops(forward,e["forward"])
        if forward!=e["after"] or intake.digest(forward)!=e["afterSHA256"]: raise AssertionError(f"Forward replay {e['id']}")
        if intake.apply_ops(e["after"],e["inverse"])!=e["before"]: raise AssertionError(f"Inverse replay {e['id']}")
    reverse=copy.deepcopy(final)
    for e in reversed(events):
        reverse=intake.apply_ops(reverse,e["inverse"])
        if reverse!=e["before"]: raise AssertionError(f"Reverse replay {e['id']}")
    if forward!=final or reverse!=initial or intake.digest(initial)!=intake.digest(parent_state):
        raise AssertionError("Whole-chain forward/reverse or parent preservation failed.")
    assert final["actors"]["A"]["plane"]==ORIGIN and final["actors"]["A"]["position"]==anchor
    assert initial["actors"]["A"]["lastArrivedFromPlaneKey"]==ORIGIN
    assert final["actors"]["A"]["lastArrivedFromPlaneKey"]==SPACE
    assert final["actors"]["A"]["lastArrivedFromEventId"]==Q27_SETTLEMENT_EVENT_ID
    assert final["transitReceipts"]==initial["transitReceipts"]
    assert final["actors"]["A"]["spellHistory"][:len(initial["actors"]["A"]["spellHistory"])]==initial["actors"]["A"]["spellHistory"]
    assert final["actors"]["A"]["RP"]==33 and final["actors"]["A"]["lastSpell"]=="antimagic-field"
    assert final["actors"]["A"]["concentration"] is None
    assert final["effects"][FIELD_CAST]["active"] is False and final["effects"][FIELD_CAST]["deadline"]==66.1
    assert final["effects"][FORTRESS_EFFECT]["active"] is False and not final["spaces"][SPACE]["exists"]
    assert all(final["items"][i]["exists"] and not final["items"][i]["consumed"] and
               final["items"][i]["plane"]==ORIGIN and final["items"][i]["custodian"]=="A"
               for i in ("focus-A","pack-A","cargo-A"))
    assert queue["currentAuthority"]==handoff["authority"]
    assert current_authority["reviewedApplied"]==829 and current_authority["pending"]==19 and current_authority["acceptedUnapplied"]==0

    verification={
        "id":"INDEPENDENT-VERIFICATION-PG328-W08-WITNESS-412-REPACK01",
        "status":"PASS_INTEGRATED_TESTONLY_WITNESS_REPAIR_REPACK01; READY_FOR_DIRECTOR_REVIEW; NO_SEAL",
        "caseId":CASE_ID,"parentFinalStateSHA256":intake.digest(parent_state),
        "branchInitialEqualsParentFinal":True,"eventCount":len(events),
        "forwardTransitionCount":len(events),"inverseTransitionCount":len(events),
        "forwardReplay":True,"fullReverseRestoration":True,
        "geometry":{"panelId":PANEL_ID,"panelBoundsFeet":panel_bounds,"raisedFeet":RAISED,
            "supportedMassLb":162,"centerFeet":CENTER,"centerRangeFeet":round(center_range,9),
            "farthestPanelCornerFeet":round(max_panel_range,9),"radiusFeet":radius,
            "casterLoESegmentFeet":{"fromExposedBodyBoundary":CASTER_LOE_FROM_BODY,"toCenter":CENTER},
            "casterLoEBodyHit":caster_body_hit,"casterLoEItemHits":caster_item_hits,
            "casterLoEPanelHit":caster_panel_hit,"casterLoEWallHits":caster_wall_hits,
            "casterLoEStairHit":caster_stair_hit,"casterLoEAllClear":True,
            "panelRayWallHits":panel_wall_hits,"panelRayStairHit":panel_stair_hit,
            "panelPenetration":panel_penetration},
        "cast":{"accessPreparedAndComponentsBound":True,"actionRefreshedAt6_0":True,
            "costRp":21,"rpBefore":54,"rpAfter":33,"discount":False,
            "counterspellWindow":True,"noAttemptBranch":True,"crossPlaneEligibilityNotAsserted":True},
        "lifecycle":{"panelSuppressedWithoutDamage":True,"Q27SettlesSource":True,
            "fixedAnchorFeet":anchor,"itemsKeepIdentityAndCustody":True,"fieldEndsAfterQ27":True,
            "fieldNotRelocated":True,"refundRp":0,"deadline66_1Preserved":True,
            "concentrationLinkEnded":True,"AEnd6_9Processed":True,
            "arrivalOriginPlaneKey":SPACE,"arrivalEventId":Q27_SETTLEMENT_EVENT_ID,
            "historicalAdmissionRecordPreserved":True},
        "authority":{"applied":829,"pending":19,"acceptedUnapplied":0,"queueChanged":False,
            "identityAcceptedOrApplied":False,"PG200B06Held":True,"fixtureMutated":False,
            "canonChanged":False,"newSealIssued":False}
    }
    write_json(out/"VERIFICATION_412_REPACK01.json",verification)
    (out/"README_412_REPACK01.md").write_text(        "# W08 occupied-antimagic witness 412 Repack01\n\n"
        "Status: " + verification["status"] + "\n\n"
        "This is a source-bound, reversible TEST_ONLY branch for the owner-adopted W08 panel/placement terms and proposal 386. "
        "It records no campaign event, live fixture mutation, canon change, spell identity acceptance/application, or Fortress seal. "
        "The current queue remains 829 applied, 19 pending, 0 accepted/unapplied.\n",encoding="utf-8")
    (out/"DIRECTOR_REVIEW_REQUEST_412_REPACK01.md").write_text(
        "Director, the owner adopted the exact 396 support/placement terms and proposal 386 for PG328-W08 only. "
        "Please review lawful access, Action/cost/components, center perception and line of effect, scheduled markers, "
        "field coverage, cast-time response handling, occupied-panel suppression, Q27 placement, item custody, "
        "field termination, clocks, and full forward/inverse restoration. This Repack01 addresses Director findings W08-412-R1/R2/R3. "
        "Please verify these repairs and report the W08-only disposition; do not issue a seal or accept/apply Fortress, clear PG200-B06, mutate the fixture, "
        "change canon, or alter the 829/19/0 queue. The identity remains pending.\n",encoding="utf-8")

    manifest_files=[]
    for p in sorted(x for x in out.rglob("*") if x.is_file() and x.name not in (ZIPNAME,"DELIVERY_412_REPACK01.json","MANIFEST_412_REPACK01.json","INDEPENDENT_VERIFICATION_412_REPACK01.json","W08_TESTONLY_EVIDENCE_SEAL_412_REPACK01.json")):
        data=p.read_bytes(); manifest_files.append({"path":p.relative_to(out).as_posix(),"bytes":len(data),"sha256":sha(data)})
    manifest={"id":"MANIFEST-PG328-W08-WITNESS-412-REPACK01","artifact":ZIPNAME,"status":verification["status"],
              "files":manifest_files,"sourceBindings":bindings}
    write_json(out/"MANIFEST_412_REPACK01.json",manifest)

    zippath=out/ZIPNAME
    with zipfile.ZipFile(zippath,"w",compression=zipfile.ZIP_DEFLATED,compresslevel=9) as package:
        for p in sorted(x for x in out.rglob("*") if x.is_file() and x.name not in (ZIPNAME,"DELIVERY_412_REPACK01.json","INDEPENDENT_VERIFICATION_412_REPACK01.json","W08_TESTONLY_EVIDENCE_SEAL_412_REPACK01.json")):
            info=zipfile.ZipInfo(p.relative_to(out).as_posix(),date_time=(2026,11,1,0,0,0))
            info.compress_type=zipfile.ZIP_DEFLATED; info.external_attr=0o100644<<16
            package.writestr(info,p.read_bytes())
    with zipfile.ZipFile(zippath) as package:
        assert package.testzip() is None
        assert len(package.namelist())==len(manifest_files)+1
        for m in manifest_files:
            b=package.read(m["path"]); assert len(b)==m["bytes"] and sha(b)==m["sha256"]
    delivery={"id":"DELIVERY-PG328-W08-WITNESS-412-REPACK01","artifact":ZIPNAME,"sha256":file_sha(zippath),
        "bytes":zippath.stat().st_size,"members":len(manifest_files)+1,
        "manifestSha256":file_sha(out/"MANIFEST_412_REPACK01.json"),
        "status":"READY_FOR_DIRECTOR_REVIEW; TEST_ONLY; UNSEALED",
        "acceptedIds":[],"appliedIds":[],"applicationAuthorized":False,
        "fortressIdentityAcceptedOrApplied":False,
        "queue":{"applied":829,"pending":19,"acceptedUnapplied":0},
        "preservation":{"PG200-B06":"held","fixture":"unchanged","canonicalRules":"unchanged",
                        "W03_W06_W07_seals":"unchanged","queue":"unchanged"},
        "parentCaseSha256":sha(parent_bytes),"finalStateSha256":intake.digest(final),
        "verificationStatus":verification["status"],
        "reviewedPacket412Sha256":"a5bf919ba80563ff90a39c1a22ad91aae9ef18be5e1b2328c81783ad4b69192b",
        "directorConversation":"https://chatgpt.com/g/g-p-67f17555a8dc8191a2b5b81e6d8adc12-dungeon-crawler/c/6ae66c6d-2d08-83ea-a1fa-042d649855a2"}
    write_json(out/"DELIVERY_412_REPACK01.json",delivery)
    print(json.dumps({"status":"PASS","artifact":str(zippath),"sha256":delivery["sha256"],
        "bytes":delivery["bytes"],"members":delivery["members"],"events":len(events),
        "bindings":len(bindings),"forwardReverseReplay":True},indent=2))


if __name__ == "__main__":
    main()
