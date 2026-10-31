from __future__ import annotations

import copy
import hashlib
import json
import shutil
import subprocess
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[5]
BASE = ROOT / "docs/audit/2026-10-08/full-game/director-spell-review-129"
OUT = BASE / "banishment_gate_witness363"
PACK = OUT / "packet"
ZIP_PATH = OUT / "DD_Rank9_BanishmentGate_W07_GustCorpse_363_TESTONLY.zip"
ENC = "utf-8"


def canon_bytes(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode(ENC)


def sha(value):
    return hashlib.sha256(canon_bytes(value)).hexdigest()


def file_sha(data):
    return hashlib.sha256(data).hexdigest()


def write_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding=ENC)


def read_json(path):
    return json.loads(path.read_text(encoding=ENC))


def at_pointer(value, pointer):
    for part in pointer.strip("/").split("/") if pointer else []:
        part = part.replace("~1", "/").replace("~0", "~")
        value = value[int(part)] if isinstance(value, list) else value[part]
    return value


def git_source(path):
    raw = subprocess.check_output(["git", "show", f"HEAD:{path}"], cwd=ROOT)
    blob = subprocess.check_output(["git", "rev-parse", f"HEAD:{path}"], cwd=ROOT, text=True).strip()
    return raw, blob


def canonical_state_patch(before, after):
    return [
        {"op": "test", "path": "", "value": before},
        {"op": "replace", "path": "", "value": after},
    ]


def apply_root_patch(state, patch):
    current = copy.deepcopy(state)
    for operation in patch:
        if operation["path"] != "":
            raise AssertionError("Only root-snapshot operations are allowed in this witness")
        if operation["op"] == "test":
            if current != operation["value"]:
                raise AssertionError("Patch precondition failed")
        elif operation["op"] == "replace":
            current = copy.deepcopy(operation["value"])
        else:
            raise AssertionError("Unsupported patch operation")
    return current


if OUT.exists():
    for existing in (p for p in OUT.rglob("*") if p.is_file()):
        rel = existing.relative_to(OUT)
        if rel.parts[0] != "packet" and rel.name not in {ZIP_PATH.name, "ARCHIVE_DELIVERY_363.json"}:
            raise SystemExit(f"Refusing to overwrite unrecognized output: {existing}")
PACK.mkdir(parents=True, exist_ok=True)
verifier_source = BASE / "verify_banishment_gate_w07_gustcorpse_363.py"
verifier_member = PACK / "verification/verify_banishment_gate_w07_gustcorpse_363.py"
verifier_member.parent.mkdir(parents=True, exist_ok=True)
shutil.copyfile(verifier_source, verifier_member)

commit = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()

catalog_path = "DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json"
w20_path = "DescentReviewChanges/ReviewBible/data/public/spell_candidates/rank9planargates5_reviewed_200/ACTOR_PROFILES.json"
w17_path = "DescentReviewChanges/ReviewBible/data/public/spell_candidates/rank9agencycontrol9_reviewed_190_reconciled01/ACTOR_PROFILES.json"
guard_path = "src/bestiary_data_full.json"
procedure_path = "docs/audit/2026-10-08/full-game/director-spell-review-129/banishment_gate_return327_received/evidence/packet327/prior/procedures/banishment-gate.json"
rules = {
    "conditions": "DescentReviewChanges/ReviewBible/docs/mechanics/CONDITIONS_PLAYTEST.md",
    "core_resolution": "DescentReviewChanges/ReviewBible/docs/mechanics/CORE_RESOLUTION_PLAYTEST.md",
    "body_equipment": "DescentReviewChanges/ReviewBible/docs/mechanics/BODY_EQUIPMENT_PLAYTEST.md",
    "combat_action": "DescentReviewChanges/ReviewBible/docs/mechanics/COMBAT_ACTION_PLAYTEST.md",
    "healing_death": "DescentReviewChanges/ReviewBible/docs/mechanics/HEALING_DEATH_PLAYTEST.md",
    "creature_lifecycle": "DescentReviewChanges/ReviewBible/docs/mechanics/CREATURE_LIFECYCLE_PLAYTEST.md",
}

w20_all = read_json(ROOT / w20_path)
w20 = w20_all["Wizard20"]
w17_all = read_json(ROOT / w17_path)
w17 = w17_all["profiles"][0]
guard_all = read_json(ROOT / guard_path)
guard_src = guard_all[326]
catalog = read_json(ROOT / catalog_path)
spells = catalog.get("spells", [])
gate_entry = next((s for s in spells if s.get("id") == "banishment-gate"), None)
if not gate_entry:
    raise AssertionError("Banishment Gate catalog entry missing")
gust_entry = next((s for s in spells if s.get("id") == "gust"), None)
if not gust_entry or not gust_entry.get("operational"):
    raise AssertionError("Gust catalog entry missing")
gate_card = gate_entry
gust_card = gust_entry["operational"]

assert w20["id"] == "PG200-W20" and w20["classLevel"] == 20 and w20["spellDC"] == 19
assert "banishment-gate" in w20["spellbook"] and "banishment-gate" in w20["prepared"]
assert w20["rpMaximum"] == 80 and w20["campaignExistenceVerified"] is False
assert w17["id"] == "W17-f7ae29175032" and w17["classLevel"] == 17 and w17["spellDC"] == 19
assert "gust" in w17["cantrips"] and "counterspell" not in [x.get("spellId") for x in w17.get("spellbook", []) if isinstance(x, dict)]
assert guard_src["name"] == "Guard" and guard_src["type"] == "Humanoid" and guard_src["size"] == "Medium"
assert guard_src["hitPoints"] == 112 and guard_src["combat"]["draft"] is False
assert gate_entry["classAccess"]["Wizard"]["baseRpCost"] == 26
assert gate_entry["status"] == "blocked-pending-operational-review" and gate_entry["operational"] is None
assert gust_card["activation"] == "Action" and gust_card["rank"] == 0
assert gust_card["rangeFeet"] == 30 and gust_card["components"] == ["V", "S"]
assert "automatically fails Strength and Dexterity saving throws" in (ROOT / rules["conditions"]).read_text(encoding=ENC)

source_files = {
    catalog_path: "sources/catalog.json",
    w20_path: "sources/WIZARD20_ACTOR_PROFILES.json",
    w17_path: "sources/W17_ACTOR_PROFILES.json",
    guard_path: "sources/bestiary_data_full.json",
    **{v: f"sources/rules/{k.upper()}.md" for k, v in rules.items()},
}
bindings = []
for source_path, member in source_files.items():
    git_bytes, blob = git_source(source_path)
    worktree = (ROOT / source_path).read_bytes()
    dest = PACK / member
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes(git_bytes)
    bindings.append({
        "repositoryPath": source_path,
        "packetMember": member,
        "sourceCommit": commit,
        "gitBlobSha1": blob,
        "gitBytes": len(git_bytes),
        "gitSha256": file_sha(git_bytes),
        "workingTreeBytes": len(worktree),
        "workingTreeSha256": file_sha(worktree),
        "includedBytesAre": "exact git show HEAD bytes",
    })

procedure_bytes = (ROOT / procedure_path).read_bytes()
(PACK / "sources/RETURN327_banishment-gate.json").write_bytes(procedure_bytes)
bindings.append({
    "repositoryPath": procedure_path,
    "packetMember": "sources/RETURN327_banishment-gate.json",
    "sourceCommit": "historical prior-return packet retained in repository evidence",
    "bytes": len(procedure_bytes),
    "sha256": file_sha(procedure_bytes),
    "includedBytesAre": "byte-exact copy of preserved Return327 prior procedure",
})

prior_archive_path = BASE / "banishment_gate_current_authority_361/Return327_HELD_CONTEXT.zip"
prior_archive_bytes = prior_archive_path.read_bytes()
(PACK / "sources/Return327_HELD_CONTEXT.zip").write_bytes(prior_archive_bytes)
bindings.append({
    "repositoryPath": str(prior_archive_path.relative_to(ROOT)).replace("\\", "/"),
    "packetMember": "sources/Return327_HELD_CONTEXT.zip",
    "bytes": len(prior_archive_bytes),
    "sha256": file_sha(prior_archive_bytes),
    "includedBytesAre": "byte-exact copy; original sealed context preserved",
})

authority_files = [
    "CURRENT_SPELL_QUEUE_361.json",
    "CURRENT_HANDOFF_361.json",
    "PG327_W01_W08_WITNESS_PLAN_361.json",
    "PG327_W03_W06_W07_SOURCE_AUDIT_362.json",
]
for name in authority_files:
    src = BASE / name
    dst = PACK / f"authority/{name}"
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(src, dst)
    bindings.append({
        "repositoryPath": str(src.relative_to(ROOT)).replace("\\", "/"),
        "packetMember": f"authority/{name}",
        "bytes": src.stat().st_size,
        "sha256": file_sha(src.read_bytes()),
        "includedBytesAre": "byte-exact current authority evidence",
    })

source_extracts = {
    "sourceCommit": commit,
    "gate": {
        "path": catalog_path,
        "pointer": f"/spells/{next(i for i,s in enumerate(spells) if s.get('id') == 'banishment-gate')}",
        "catalogEntry": gate_entry,
        "historicalProcedure": read_json(ROOT / procedure_path),
        "wizard20Profile": {
            "path": w20_path,
            "pointer": "/Wizard20",
            "id": w20["id"],
            "class": w20["class"],
            "classLevel": w20["classLevel"],
            "PB": w20["PB"],
            "spellDC": w20["spellDC"],
            "rpMaximum": w20["rpMaximum"],
            "acquisitionPointer": "/Wizard20/ordinaryLearning/16/selected/2",
            "acquisition": w20["ordinaryLearning"][16]["selected"][2],
            "spellbookPointer": "/Wizard20/spellbook/63",
            "preparedPointer": "/Wizard20/prepared/2",
            "campaignExistenceVerified": w20["campaignExistenceVerified"],
        },
    },
    "gust": {
        "path": catalog_path,
        "pointer": f"/spells/{next(i for i,s in enumerate(spells) if s.get('id') == 'gust')}/operational",
        "card": gust_card,
        "w17Profile": {
            "path": w17_path,
            "pointer": "/profiles/0",
            "id": w17["id"],
            "class": w17["class"],
            "classLevel": w17["classLevel"],
            "spellDC": w17["spellDC"],
            "cantripAcquisitionPointer": "/profiles/0/cantripAcquisition/1",
            "cantripAcquisition": w17["cantripAcquisition"][1],
            "cantripsPointer": "/profiles/0/cantrips/3",
            "counterspellInBook": any(isinstance(x, dict) and x.get("spellId") == "counterspell" for x in w17.get("spellbook", [])),
            "counterspellPrepared": False,
            "preparation": w17["preparation"],
        },
    },
    "guard": {
        "path": guard_path,
        "pointer": "/326",
        "profile": guard_src,
        "fixturePremises": {
            "initialHP": 0,
            "deathStatus": "dying",
            "priorDeathFailures": 2,
            "conditions": ["Unconscious", "Prone"],
            "significantNpcClassification": "TEST_ONLY, using the Director-approved death-save lifecycle",
            "bodyPositionConvention": "position is horizontal center at the feet/base elevation; dimensions centered in x/y",
            "measuredProneHeightFeet": 1,
            "bodySpaceFeet": [5, 5, 1],
            "heldItems": [],
            "carriedItemIds": ["G01-paper-token"],
            "qualification": "all are owner-authorized TEST_ONLY premises, not campaign history",
        },
    },
}
write_json(PACK / "SOURCE_EXTRACTS_363.json", source_extracts)
write_json(PACK / "SOURCE_BINDINGS_363.json", {
    "id": "PG327-W07-SOURCE-BINDINGS-363",
    "sourceCommit": commit,
    "bindings": bindings,
    "hashConvention": "All SHA-256 values are over exact UTF-8/binary file bytes. Canonical repository sources bind Git HEAD and Git blob; working-tree bytes are shown separately where line-ending normalization differs.",
})

owner_authority = {
    "id": "OWNER-TESTONLY-W07-FIXTURE-AUTHORIZATION-363",
    "scope": "Banishment Gate W07 only; hypothetical finite fixture; no campaign facts",
    "ownerReply": "Yes—authorize this TEST_ONLY fixture.",
    "authorizedPremises": [
        "TEST_ONLY fixture actors, consent/eligibility, coordinates, body measurements and inventory",
        "Opening Guard state at zero HP, dying with two prior death-save failures, Unconscious and Prone under the Director-approved significant-NPC test classification",
        "One test-only carried genuine object and one Wizard focus; no held Guard item",
        "TEST_ONLY Wizard20 Gate creator and W17 Gust caster with source-bound profiles",
    ],
    "notAuthorizedOrAsserted": [
        "No campaign event, real-world person, campaign identity, or runtime spell execution",
        "No invented Guard ability scores, CON modifier, or save roll for Gust",
        "No type-change source; W03 remains open",
        "No Gate acceptance, application, canonical edit, or release from HOLD",
    ],
}
write_json(PACK / "OWNER_TESTONLY_AUTHORIZATION_363.json", owner_authority)

director_ruling = {
    "id": "PG327-W07-DIRECTOR-RULING-EXTRACT-363",
    "sourceConversation": "Review Time Stop Witness Evidence, GPT project chat; messages visible in submitted browser session",
    "rulings": [
        {
            "subject": "Gust source route",
            "disposition": "Approved for finite TEST_ONLY W07 witness, using Wizard17 DC19",
            "basis": "Director verified Gust operational card and W17 acquisition/profile. Unconscious automatically fails STR save; no Shove check.",
        },
        {
            "subject": "Gate creator",
            "disposition": "Wizard20 scoped reuse approved as TEST_ONLY Gate creator; W17 casts Gust",
            "basis": "Gate acquired at Wizard level 17, in spellbook and prepared; campaignExistenceVerified=false. Bind actual 26 RP, Action, V/S/F, legal point and concentration.",
        },
        {
            "subject": "Crossing geometry",
            "disposition": "5-foot complete crossing approved when Medium Prone body begins x=[-5,0], y=[-2.5,2.5], z=[0,1] and ends x=[0,5], y=[-2.5,2.5], z=[0,1]",
            "basis": "The initial stationary face touch triggers nothing; every body interior point crosses; no epsilon movement is required; use a distinct cell-local space.",
        },
        {
            "subject": "Death save",
            "disposition": "Director approved TEST_ONLY significant-NPC death-save classification; next original regular-start natural result 2–9 adds failure, and from two failures resolves death; no Wound save because no damage or Maiming occurs",
            "basis": "Guard remains at 0 HP, dying, alive and not Stable at scheduled regular-start marker; preserve the original marker and preceding start effects.",
        },
        {
            "subject": "Closure anchor and deadline",
            "disposition": "At atomic crossing/admission snapshot post-crossing origin-plane pose x=[0,5], y=[-2.5,2.5], z=[0,1], center(2.5,0), feet z=0, Prone; same corpse returns there if space is legal",
            "basis": "Cell deadline is admission+60s or earlier genuine ending. Gate concentration ending closes a still-live cell exactly once.",
        },
    ],
    "transcriptExcerpts": [
        "Yes—this Gust route is approved for constructing the finite TEST_ONLY W07 witness, using DC19. W07 itself remains unsealed pending the completed evidence.",
        "No additional mechanical source gap is identified for this route.",
        "The initial stationary face contact triggers nothing and places no occupied body interior across the portal plane.",
        "Confirming the anchor interpretation does not establish the completed W07 witness; the same corpse returns using the fixed admission-time anchor when the live cell closes.",
    ],
    "explicitNonDecision": {
        "banishmentGate": "HOLD",
        "blockers": ["PG200-B03", "PG200-B04"],
        "W03": "Open; no qualifying type-change source was found",
        "acceptedIds": [],
        "appliedIds": [],
        "applicationAuthorized": False,
    },
}
write_json(PACK / "W07_DIRECTOR_RULING_363.json", director_ruling)

BODY = [5, 5, 1]
GATE_ID = "BG-W07-TESTONLY-GATE-363"
CELL_ID = "BG-W07-TESTONLY-CELL-363"
CAST_GATE = f"{GATE_ID}/cast"
CAST_GUST = f"{GATE_ID}/gust"
GUARD_ID = "Guard-W07-TESTONLY"
TOKEN_ID = "G01-paper-token"


def actor_base(actor_id, profile_id, class_name, level, dc, pb, rp, max_rp, pos, size="Medium", dims=None):
    return {
        "id": actor_id,
        "profileId": profile_id,
        "class": class_name,
        "classLevel": level,
        "spellDC": dc,
        "PB": pb,
        "HP": None,
        "maxHP": None,
        "RP": rp,
        "maxRP": max_rp,
        "Dissonance": 0,
        "Refrain": 0,
        "lastSpell": None,
        "preparedFamiliesUsed": [],
        "spellHistory": [],
        "resourceHistory": [],
        "concentration": None,
        "conditions": [],
        "death": {"status": "alive", "successes": 0, "failures": 0, "saveInputs": []},
        "plane": "fixture:origin",
        "position": pos,
        "size": size,
        "bodyBox": dims or [5, 5, 6],
        "bodyPositionConvention": "horizontal center and feet/base elevation",
        "orientation": "standing",
        "heldItems": [],
        "carriedItemIds": [],
        "action": 0,
        "bonusAction": 0,
        "reaction": 1,
        "movement": 0,
        "regularSchedule": None,
        "recharge": {},
        "magicThisTurn": False,
        "visible": True,
        "lineOfEffect": True,
    }


initial = {
    "time": -0.1,
    "mode": "initiative",
    "fixture": {"id": "W07-TESTONLY-363", "campaignFact": False, "authorizationId": owner_authority["id"], "originTerrain": "clear; no movement or placement blockers; all unlisted bodies absent"},
    "actors": {},
    "items": {},
    "effects": {},
    "spaces": {"fixture:origin": {"kind": "ordinary-origin-plane", "identity": "fixture:origin", "existsOnlyForTest": True, "terrainBlockers": [], "opaqueCover": [], "hazards": [], "lawfulReturnSpaceAtAnchor": True}},
    "pendingCast": None,
    "crossingReceipts": {},
    "hardDenialClaims": [],
    "closureReceipts": [],
    "processedEventIds": [],
}
w20_actor = actor_base("W20", "PG200-W20", "Wizard", 20, 19, 6, 80, 80, [-50, 0, 0])
w20_actor.update({
    "profilePath": w20_path,
    "profilePointer": "/Wizard20",
    "profileSHA256": file_sha((ROOT / w20_path).read_bytes()),
    "knownSpells": ["banishment-gate", "counterspell"],
    "preparedSpells": list(w20["prepared"]),
    "spellbookIncludesCounterspell": True,
    "counterspellPrepared": False,
    "focusId": "focus-W20",
    "focusAccessible": True,
    "campaignExistenceVerified": False,
    "action": 0,
    "bonusAction": 0,
    "movement": 0,
    "regularSchedule": {"firstStart": 0.0, "period": 6.0, "endOffset": 0.9, "nextStart": 0.0, "nextEnd": 0.9, "starts": [], "ends": [], "budgetHistory": []},
})
w17_actor = actor_base("W17", w17["id"], "Wizard", 17, 19, w17["PB"], 64, w17["maximumRP"], [-26, 0, 0])
w17_actor.update({
    "profilePath": w17_path,
    "profilePointer": "/profiles/0",
    "profileSHA256": file_sha((ROOT / w17_path).read_bytes()),
    "knownCantrips": list(w17["cantrips"]),
    "preparedSpells": list(w17["ordinaryRepertoire"]),
    "cantripAcquisition": w17["cantripAcquisition"][1],
    "counterspellInSpellbook": False,
    "counterspellPrepared": False,
    "campaignExistenceVerified": False,
    "action": 0,
    "bonusAction": 0,
    "movement": 0,
    "regularSchedule": {"firstStart": 1.0, "period": 6.0, "endOffset": 1.9, "nextStart": 1.0, "nextEnd": 1.9, "starts": [], "ends": [], "budgetHistory": []},
})
guard_actor = {
    "id": GUARD_ID,
    "profileId": "Guard",
    "profilePath": guard_path,
    "profilePointer": "/326",
    "profileSHA256": file_sha((ROOT / guard_path).read_bytes()),
    "name": "Guard",
    "creatureType": "Humanoid",
    "size": "Medium",
    "armorClass": 15,
    "HP": 0,
    "maxHP": 112,
    "RP": None,
    "maxRP": None,
    "conditions": ["Unconscious", "Prone"],
    "lifeClassification": "TEST_ONLY_SIGNIFICANT_NPC_USING_DEATH_SAVES",
    "custodyStatus": "TEST_ONLY lawful fixture custody; owner-authorized; not a campaign fact",
    "fixtureConsent": "TEST_ONLY premise only; no campaign or real-world consent asserted",
    "death": {"status": "dying", "successes": 0, "failures": 2, "saveInputs": [{"fixtureState": "opening", "die": None, "result": "two existing failures are authorized TEST_ONLY opening state; no prior roll or campaign history asserted"}]},
    "plane": "fixture:origin",
    "position": [-2.5, 0, 0],
    "bodyBox": BODY,
    "bodyBoxWorld": {"x": [-5, 0], "y": [-2.5, 2.5], "z": [0, 1]},
    "bodyPositionConvention": "horizontal center and feet/base elevation",
    "measuredProneHeightFeet": 1,
    "orientation": "prone",
    "rootBodyIdentity": GUARD_ID,
    "corpseIdentity": None,
    "heldItems": [],
    "carriedItemIds": [TOKEN_ID],
    "action": 0,
    "bonusAction": 0,
    "reaction": 0,
    "movement": 0,
    "regularSchedule": {"firstStart": 2.0, "period": 6.0, "endOffset": 2.9, "nextStart": 2.0, "nextEnd": 2.9, "starts": [], "ends": [], "budgetHistory": []},
    "stabilized": False,
    "preventionOrReplacement": [],
    "noAbilityScoresProvided": True,
}
initial["actors"] = {"W20": w20_actor, "W17": w17_actor, GUARD_ID: guard_actor}
initial["items"] = {
    "focus-W20": {"id": "focus-W20", "ownerId": "W20", "type": "ordinaryWizardFocus", "testOnly": True, "value": None, "consumed": False},
    TOKEN_ID: {"id": TOKEN_ID, "kind": "genuineNonmagicalPocketToken", "massOz": 1, "carrierId": GUARD_ID, "held": False, "testOnly": True, "exists": True, "location": {"plane": "fixture:origin", "carrierId": GUARD_ID}},
}

state = copy.deepcopy(initial)
events = []


def event(eid, t, kind, narrative, source, authored, mutate):
    global state
    before = copy.deepcopy(state)
    after = copy.deepcopy(state)
    mutate(after)
    after["time"] = t
    after["processedEventIds"].append(eid)
    record = {
        "id": eid,
        "time": t,
        "kind": kind,
        "narrative": narrative,
        "source": source,
        "authoredInputs": authored,
        "before": before,
        "after": after,
        "beforeSHA256": sha(before),
        "afterSHA256": sha(after),
        "forward": canonical_state_patch(before, after),
        "inverse": canonical_state_patch(after, before),
    }
    assert state == before
    assert apply_root_patch(state, record["forward"]) == after
    state = after
    events.append(record)


def w20_start(s):
    a = s["actors"]["W20"]
    a["action"], a["bonusAction"], a["reaction"], a["movement"] = 1, 1, 1, 30
    a["regularSchedule"]["starts"].append(0.0)
    a["regularSchedule"]["nextStart"] = 6.0
    a["regularSchedule"]["budgetHistory"].append({"time": 0.0, "Action": 1, "BonusAction": 1, "Reaction": 1, "Movement": 30})


event(f"{GATE_ID}:0", 0.0, "REGULAR_START", "Wizard20 reaches its original scheduled regular-turn start and receives its ordinary budgets once.", "COMBAT_ACTION_PLAYTEST.md regular-turn schedule", {"refreshCount": 1}, w20_start)


def gate_commit(s):
    w = s["actors"]["W20"]
    w["action"] = 0
    w["RP"] = 54
    w["magicThisTurn"] = True
    w["lastSpell"] = "banishment-gate"
    w["preparedFamiliesUsed"].append("banishment-gate")
    w["spellHistory"].append({"castId": CAST_GATE, "spellId": "banishment-gate", "class": "Wizard", "rank": 9, "school": "Abjuration", "time": 0.1, "costRP": 26, "components": ["V", "S", "F"], "target": None, "concentration": True, "firstPreparedFamily": True, "baseDissonance": 0, "Refrain": 0})
    w["resourceHistory"].append({"event": CAST_GATE, "RP": -26, "poolAfter": 54, "discount": False})
    w["concentration"] = CAST_GATE
    s["pendingCast"] = {"castId": CAST_GATE, "casterId": "W20", "spellId": "banishment-gate", "committedAt": 0.1, "resolvesAt": 0.2, "actionPaid": True, "rpPaid": 26, "componentsProvided": ["V", "S", "F"], "focusId": "focus-W20", "counterspellWindow": {"eligibleReactors": [], "ineligible": [{"actorId": "W17", "reason": "Counterspell not in spellbook; not prepared"}, {"actorId": GUARD_ID, "reason": "Unconscious; Reaction unavailable"}], "result": "no eligible counterspell"}}


event(f"{GATE_ID}:1", 0.1, "CAST_COMMIT", "Wizard20 legally commits prepared Banishment Gate; Action, RP and components are paid once.", "Banishment Gate catalog card; Wizard20 source-bound profile; COMBAT_ACTION_PLAYTEST.md spell casting and interruption rules", {"point": [0, 0, 7.5], "distanceFeet": 50, "rangeFeet": 60, "selectedCreatureType": "Humanoid", "gateOpening": {"plane": "x=0", "y": [-5, 5], "z": [0, 15]}, "creatorId": "W20"}, gate_commit)


def gate_resolve(s):
    s["pendingCast"] = None
    s["effects"][GATE_ID] = {
        "id": GATE_ID,
        "spellId": "banishment-gate",
        "creatorId": "W20",
        "creatorConcentration": CAST_GATE,
        "status": "active",
        "createdAt": 0.2,
        "endsAt": 600.2,
        "selectedCreatureType": "Humanoid",
        "originPlane": "fixture:origin",
        "originAnchor": {"plane": "fixture:origin", "gatePlane": "x=0", "opening": {"y": [-5, 5], "z": [0, 15]}},
        "opening": {"x": 0, "y": [-5, 5], "z": [0, 15]},
        "concentration": True,
        "cells": [],
        "closeCount": 0,
    }


event(f"{GATE_ID}:2", 0.2, "CAST_RESOLVE", "Gate opens after the spell interruption window. The Guard only touches the plane while stationary, so no crossing, claim or cell occurs.", "Banishment Gate PG9-Q14–Q17; Director ruling on touch-only geometry", {"stationaryGuardBox": {"x": [-5, 0], "y": [-2.5, 2.5], "z": [0, 1]}, "touchOnly": True, "crossing": False, "admission": False, "claim": False, "cell": False}, gate_resolve)


def w20_end_turn(s):
    a = s["actors"]["W20"]
    a["regularSchedule"]["ends"].append(0.9)
    a["regularSchedule"]["nextStart"] = 6.0
    a["regularSchedule"]["budgetHistory"].append({"time": 0.0, "Action": 1, "BonusAction": 1, "Reaction": 1, "Movement": 30})
    a["action"] = a["bonusAction"] = a["movement"] = 0


event(f"{GATE_ID}:3", 0.9, "TURN_END", "Wizard20 ends its scheduled regular turn; Gate concentration and deadline continue.", "COMBAT_ACTION_PLAYTEST.md regular-turn schedule", {}, w20_end_turn)


def w17_start(s):
    a = s["actors"]["W17"]
    a["action"], a["bonusAction"], a["reaction"], a["movement"] = 1, 1, 1, 30
    a["regularSchedule"]["starts"].append(1.0)
    a["regularSchedule"]["nextStart"] = 7.0
    a["regularSchedule"]["budgetHistory"].append({"time": 1.0, "Action": 1, "BonusAction": 1, "Reaction": 1, "Movement": 30})


event(f"{GATE_ID}:4", 1.0, "REGULAR_START", "W17 begins its ordinary scheduled turn; this grants one Action and ordinary movement only.", "COMBAT_ACTION_PLAYTEST.md regular-turn schedule", {"movementSpent": 0}, w17_start)


def gust_commit(s):
    a = s["actors"]["W17"]
    a["action"] = 0
    a["magicThisTurn"] = True
    a["lastSpell"] = "gust"
    a["spellHistory"].append({"castId": CAST_GUST, "spellId": "gust", "class": "Wizard", "rank": 0, "time": 1.1, "costRP": 0, "components": ["V", "S"], "spellDC": 19, "origin": [-26, 0, 0.5], "targetId": GUARD_ID})
    a["resourceHistory"].append({"event": CAST_GUST, "RP": 0, "poolAfter": 64, "discount": False})
    s["pendingCast"] = {"castId": CAST_GUST, "casterId": "W17", "spellId": "gust", "committedAt": 1.1, "resolvesAt": 1.2, "actionPaid": True, "rpPaid": 0, "componentsProvided": ["V", "S"], "origin": [-26, 0, 0.5], "targetId": GUARD_ID, "rangeFeet": 23.5, "rangeLimitFeet": 30, "visible": True, "lineOfEffect": True, "counterspellWindow": {"eligibleReactors": [], "ineligible": [{"actorId": "W20", "reason": "Counterspell is not prepared"}, {"actorId": GUARD_ID, "reason": "Unconscious; Reaction unavailable"}], "result": "no eligible counterspell"}}


event(f"{GATE_ID}:5", 1.1, "CAST_COMMIT", "W17 commits the sourced Action Gust cantrip at DC19; no RP cost, Action paid once, target and range are legal.", "Gust catalog operational entry; W17 actor profile; COMBAT_ACTION_PLAYTEST.md", {"casterOrigin": [-26, 0, 0.5], "guardCenter": [-2.5, 0, 0.5], "centerDistanceFeet": 23.5, "within30Feet": True}, gust_commit)


def gust_cross_admit(s):
    s["pendingCast"] = None
    guard = s["actors"][GUARD_ID]
    guard["saveOutcome"] = {"ability": "STR", "spellDC": 19, "result": "automaticFailure", "die": None, "modifier": None, "source": "CONDITIONS_PLAYTEST.md:723; Unconscious"}
    guard["position"] = [0, 0, 0]
    guard["originPlaneAdmissionBox"] = {"x": [0, 5], "y": [-2.5, 2.5], "z": [0, 1]}
    guard["bodyBoxWorld"] = None
    guard["cellLocalBodyBox"] = {"x": [-2.5, 2.5], "y": [-2.5, 2.5], "z": [0, 1]}
    guard["plane"] = "fixture:banishment-cell"
    guard["cellLocalPosition"] = [0, 0, 0]
    guard["originReturnAnchor"] = {"plane": "fixture:origin", "bodyBox": {"x": [0, 5], "y": [-2.5, 2.5], "z": [0, 1]}, "center": [2.5, 0], "baseZ": 0, "orientation": "prone"}
    guard["crossingReceiptId"] = f"{GATE_ID}/crossing/1"
    guard["admittedToCellId"] = CELL_ID
    cell = {
        "id": CELL_ID,
        "parentGateId": GATE_ID,
        "primaryTargetId": GUARD_ID,
        "status": "active",
        "admittedAt": 1.2,
        "deadline": 61.2,
        "admissionPlusSeconds": 60,
        "localCenter": [0, 0],
        "bounds": {"x": [-7.5, 7.5], "y": [-7.5, 7.5], "z": [0, 10]},
        "contents": [GUARD_ID, TOKEN_ID],
        "closedAt": None,
        "closeCount": 0,
    }
    s["effects"][CELL_ID] = cell
    s["effects"][GATE_ID]["cells"].append(CELL_ID)
    s["crossingReceipts"][guard["crossingReceiptId"]] = {
        "targetId": GUARD_ID,
        "gateId": GATE_ID,
        "from": "fixture:origin",
        "to": CELL_ID,
        "movementSource": CAST_GUST,
        "forcedMovementFeet": 5,
        "bodyBoxBefore": {"x": [-5, 0], "y": [-2.5, 2.5], "z": [0, 1]},
        "bodyBoxAfterBeforeExile": {"x": [0, 5], "y": [-2.5, 2.5], "z": [0, 1]},
        "completeBodyCrossing": True,
        "admissionId": f"{CELL_ID}/admission/1",
        "admittedAt": 1.2,
        "claimSpent": True,
        "claims": {"creator": "W20", "target": GUARD_ID, "encounter": "fixture:banishment-gate-w07"},
        "duplicateDeliveryCount": 0,
    }
    s["hardDenialClaims"].append({"creator": "W20", "target": GUARD_ID, "encounter": "fixture:banishment-gate-w07", "gateId": GATE_ID, "admissionId": f"{CELL_ID}/admission/1", "spentAt": 1.2, "spentOnlyAfterSuccessfulAdmission": True})
    s["items"][TOKEN_ID]["location"] = {"cellId": CELL_ID, "carrierId": GUARD_ID}


event(f"{GATE_ID}:6", 1.2, "FORCED_MOVEMENT_AND_ADMISSION", "The automatically failed Gust save yields its complete 5-foot directly-away movement. The single Guard body crosses the full aperture, spends one claim on successful admission, then moves cell-locally; no duplicate body is instantiated.", "Gust operational effect; CONDITIONS_PLAYTEST.md:723; BODY_EQUIPMENT_PLAYTEST.md:67-76; Banishment Gate PG9-Q14-Q17; Director W07 ruling", {"originPlane": "fixture:origin", "gatePlane": "x=0", "openingY": [-5, 5], "openingZ": [0, 15], "bodyBoxStart": {"x": [-5, 0], "y": [-2.5, 2.5], "z": [0, 1]}, "bodyBoxAfterMovementBeforeAdmission": {"x": [0, 5], "y": [-2.5, 2.5], "z": [0, 1]}, "pushDirection": "+x directly away from W17", "movement": 5, "guardAbilityScoresUsed": False, "shoveCheck": False, "initialTouchTriggered": False, "unobstructedPath": True, "targetInCustody": True, "eligibleType": "Humanoid", "immunityOrSuppression": False, "claimAvailableAtStart": True, "samePhysicalBody": True}, gust_cross_admit)


def w17_end(s):
    a = s["actors"]["W17"]
    a["regularSchedule"]["ends"].append(1.9)
    a["action"] = a["bonusAction"] = a["movement"] = 0


event(f"{GATE_ID}:7", 1.9, "TURN_END", "W17 ends the ordinary turn. Forced movement did not spend W17 or Guard voluntary movement.", "COMBAT_ACTION_PLAYTEST.md", {"W17MovementSpent": 0, "GuardMovementSpent": 0}, w17_end)


def guard_death(s):
    g = s["actors"][GUARD_ID]
    g["regularSchedule"]["starts"].append(2.0)
    g["regularSchedule"]["nextStart"] = 8.0
    g["death"]["failures"] = 3
    g["death"]["status"] = "dead"
    g["death"]["saveInputs"].append({"time": 2.0, "regularStart": True, "d20": 5, "modifier": 0, "result": "oneFailure", "failuresBefore": 2, "failuresAfter": 3, "successes": 0, "stable": False, "preventionOrReplacement": [], "woundSave": "not triggered: no damage and no Maiming", "lifecycleSource": "CORE_RESOLUTION_PLAYTEST.md:54; Director approval"})
    g["corpseIdentity"] = GUARD_ID
    g["lifeState"] = "dead corporeal remains"
    g["heldItems"] = []
    s["items"][TOKEN_ID]["corpseAssociation"] = GUARD_ID


event(f"{GATE_ID}:8", 2.0, "SCHEDULED_DEATH_SAVE", "At the Guard's original regular-start marker, unmodified result 5 adds the third failure and resolves death. The same physical body remains a corpse; its genuine carried token stays with it. No Wound save is made.", "CORE_RESOLUTION_PLAYTEST.md:54; Creature lifecycle and Gate cell-extension rules", {"marker": "first scheduled Guard regular start", "d20": 5, "priorFailures": 2, "savesBeforeThisMarker": 0, "otherStartEffects": [], "deathPreventedOrReplaced": False, "damage": False, "maiming": False, "woundSave": False}, guard_death)


def close(s):
    gate = s["effects"][GATE_ID]
    cell = s["effects"][CELL_ID]
    gate["status"] = "ended"
    gate["concentrationEndedAt"] = 2.1
    gate["endReason"] = "Wizard20 voluntarily ends its still-active concentration"
    gate["closeCount"] = 1
    gate["cells"] = []
    cell["status"] = "destroyed"
    cell["closedAt"] = 2.1
    cell["closeCount"] = 1
    cell["closureReason"] = "parent Gate concentration ended before either deadline"
    g = s["actors"][GUARD_ID]
    g["plane"] = "fixture:origin"
    g["position"] = [2.5, 0, 0]
    g["bodyBoxWorld"] = {"x": [0, 5], "y": [-2.5, 2.5], "z": [0, 1]}
    g["cellLocalPosition"] = None
    g["cellLocalBodyBox"] = None
    g["returnedByClosureReceiptId"] = f"{CELL_ID}/closure/1"
    s["items"][TOKEN_ID]["location"] = {"plane": "fixture:origin", "carrierId": GUARD_ID, "sameCarrierAsBefore": True}
    w = s["actors"]["W20"]
    w["concentration"] = None
    s["closureReceipts"].append({
        "id": f"{CELL_ID}/closure/1",
        "cellId": CELL_ID,
        "parentGateId": GATE_ID,
        "closedAt": 2.1,
        "reason": "concentration end",
        "appliedOnce": True,
        "deadlineAtAdmissionPlus60": 61.2,
        "gateOriginalDeadline": 600.2,
        "sameExtantCorpseIdentityReturned": GUARD_ID,
        "fixedOriginAnchor": g["originReturnAnchor"],
        "legalSpaceAtAnchor": True,
        "originBodiesAtClosure": {"W20": {"x": [-52.5, -47.5], "y": [-2.5, 2.5]}, "W17": {"x": [-28.5, -23.5], "y": [-2.5, 2.5]}},
        "placementConflict": False,
        "tokenIdentityReturnedWithCorpse": TOKEN_ID,
        "duplicateBodyCreated": False,
        "refund": 0,
        "remainingRP": 54,
    })


event(f"{GATE_ID}:9", 2.1, "GATE_CONCENTRATION_END_AND_CELL_CLOSURE", "Wizard20 ends the Gate concentration while the cell is live. The same corpse and carried item return once at the approved fixed admission-time anchor; the cell and Gate close once, with no refund or duplicate entity.", "Banishment Gate PG9-Q15-Q17 / PG200-CELL-EXT; Director anchor confirmation", {"cellDeadline": 61.2, "gateDeadline": 600.2, "earlierValidEnding": True, "anchor": {"x": [0, 5], "y": [-2.5, 2.5], "z": [0, 1]}, "originLocationFreeAndLegal": True, "fallbackNeeded": False}, close)

case = {
    "id": "W07_GUST_CORPSE_CASE_363",
    "spellId": "banishment-gate",
    "witnessId": "W07",
    "mainCaseId": "W07_GUST_CORPSE_CASE_363",
    "kind": "TEST_ONLY_lifecycle_witness",
    "status": "SUBMITTED_FOR_DIRECTOR_REVIEW; NOT_ACCEPTED; NOT_APPLIED",
    "holdIds": ["PG200-B03", "PG200-B04"],
    "coverage": {"W07": "complete evidence submitted for Director check", "W01": "not evidenced by this packet", "W02": "not evidenced by this packet", "W03": "source gap remains open", "W04": "not evidenced by this packet", "W05": "not evidenced by this packet", "W06": "separately source-approved; witness outstanding", "W08": "not evidenced by this packet"},
    "scenarioQualification": "Owner-authorized hypothetical TEST_ONLY state; not campaign history, runtime execution, or a spell identity disposition.",
    "sourceBindings": {
        "Wizard20": {"path": w20_path, "pointer": "/Wizard20", "sha256WorkingTree": file_sha((ROOT / w20_path).read_bytes()), "id": w20["id"], "campaignExistenceVerified": False},
        "Wizard17": {"path": w17_path, "pointer": "/profiles/0", "sha256WorkingTree": file_sha((ROOT / w17_path).read_bytes()), "id": w17["id"], "campaignExistenceVerified": False},
        "Guard": {"path": guard_path, "pointer": "/326", "sha256WorkingTree": file_sha((ROOT / guard_path).read_bytes()), "id": GUARD_ID, "fixtureProfile": "Guard"},
        "Banishment Gate": {"path": catalog_path, "id": "banishment-gate"},
        "Gust": {"path": catalog_path, "id": "gust"},
    },
    "fixturePremises": owner_authority,
    "sourceAndRulings": "See SOURCE_EXTRACTS_363.json, SOURCE_BINDINGS_363.json, and W07_DIRECTOR_RULING_363.json.",
    "initial": initial,
    "events": events,
    "final": state,
    "initialSHA256": sha(initial),
    "finalSHA256": sha(state),
    "inverseRestorationOrder": [e["id"] for e in reversed(events)],
    "assertions": {
        "touchOnlyGateOpeningCreatedNoCell": True,
        "guardInitialBodyIsMediumFiveByFiveMeasuredProneHeightOne": True,
        "gustSaveAutomaticallyFailsWithoutAbilityScoreOrDie": True,
        "completeBodyCrossesAperture": True,
        "sameActorIsMovedCellLocalAfterAdmission": True,
        "singleClaimSpentOnlyUponAdmission": True,
        "deathSaveOccursAtOriginalRegularStartAndThirdFailureKills": True,
        "noWoundSaveBecauseNoDamageOrMaiming": True,
        "corpseAndGenuineCarriedItemPersist": True,
        "sameCorpseReturnsAtFixedPostCrossingAnchor": True,
        "cellDeadlineAndGateDeadlineRetained": True,
        "closureOccursExactlyOnce": True,
        "gateRemainHOLD": True,
        "w03SourceGapRemainsOpen": True,
    },
}
write_json(PACK / "W07_GUST_CORPSE_CASE_363.json", case)

validation = {
    "id": "PG327-W07-VALIDATION-363",
    "status": "PASS_LOCAL_REPLAY_AND_SOURCE_BINDINGS; DIRECTOR_REVIEW_REQUIRED",
    "caseId": case["id"],
    "sourceCommit": commit,
    "eventCount": len(events),
    "eventIds": [e["id"] for e in events],
    "forwardReplay": "PASS",
    "inverseReplay": "PASS",
    "initialSHA256": sha(initial),
    "finalSHA256": sha(state),
    "terminalLifecycle": "same corpse and token returned to fixed post-crossing anchor; Gate/cell close once",
    "admissionTime": 1.2,
    "cellDeadline": 61.2,
    "gateDeadline": 600.2,
    "closureTime": 2.1,
    "chronology": "PASS",
    "guardAbilityScoreInvented": False,
    "guardWoundSaveSkippedAsInapplicable": True,
    "campaignFactsAsserted": False,
    "spellAccepted": False,
    "spellApplied": False,
    "applicationAuthorized": False,
    "queueAuthority": "Queue361 unchanged: 828 applied / 20 pending / 0 accepted-unapplied",
    "w03": "OPEN SOURCE GAP",
}

replay = copy.deepcopy(initial)
for e in events:
    assert sha(replay) == e["beforeSHA256"]
    replay = apply_root_patch(replay, e["forward"])
    assert sha(replay) == e["afterSHA256"]
assert replay == state
for e in reversed(events):
    assert sha(replay) == e["afterSHA256"]
    replay = apply_root_patch(replay, e["inverse"])
    assert sha(replay) == e["beforeSHA256"]
assert replay == initial
assert [e["time"] for e in events] == sorted(e["time"] for e in events)
assert state["actors"][GUARD_ID]["death"]["status"] == "dead"
assert state["actors"][GUARD_ID]["plane"] == "fixture:origin"
assert state["actors"][GUARD_ID]["position"] == [2.5, 0, 0]
assert state["effects"][CELL_ID]["closeCount"] == 1
assert state["effects"][GATE_ID]["closeCount"] == 1
write_json(PACK / "VALIDATION_363.json", validation)

readme = """# Banishment Gate W07 TEST_ONLY witness 363

This packet submits only the W07 corpse lifecycle witness to the GPT Director. It does not request or imply Gate acceptance or application. Queue361 remains authoritative at 828 applied, 20 pending, and 0 accepted-unapplied. Banishment Gate remains HOLD under PG200-B03 and PG200-B04. W03 remains an open source gap.

The finite fixture uses the Director-approved Wizard20 Gate creator and Wizard17 Gust caster. The Guard opens at 0 HP, dying with two failures, Unconscious and Prone under the TEST_ONLY significant-NPC death-save classification specifically approved for this witness. Gust is resolved before the Guard's first original regular-start marker. An unmodified result 5 makes the third failure. Because that event is neither damage nor Maiming, no Wound save is triggered. The same extant body becomes a corpse; its single genuine fixture token remains carried.

Geometry is bound to the Medium five-by-five occupied footprint with measured Prone height one foot. The stationary face touch at x=0 creates no cell. Gust moves the full body five feet to x=[0,5] through the 10-by-15 opening; only then is the body admitted to its separate cell-local space. At closure, the same corpse returns to the approved fixed post-crossing origin anchor. No campaign facts, runtime execution, invented Guard scores, or new type-change source are asserted.

All events include complete before/after state, deterministic SHA-256 state hashes, test-and-replace forward patches, scoped inverse patches, and exact reverse-order restoration. The local validator replays all nine transitions forward and backward.
"""
(PACK / "README.md").write_text(readme, encoding=ENC)

# Inventory every packet member before writing the delivery and manifest.
members = sorted(p for p in PACK.rglob("*") if p.is_file() and p.name not in {"MANIFEST.json", "DELIVERY.json"})
manifest = {
    "id": "PG327-W07-MANIFEST-363",
    "packetId": "DD-RANK9-BANISHMENT-GATE-W07-GUSTCORPSE-363-TESTONLY",
    "sourceCommit": commit,
    "disposition": "W07 evidence only; not a spell acceptance/application decision",
    "metadataSidecars": "MANIFEST.json and DELIVERY.json are archive members but excluded from the member self-hash table; the external ARCHIVE_DELIVERY_363.json binds the final archive bytes and ZIP CRC validates every member.",
    "members": [{"path": p.relative_to(PACK).as_posix(), "bytes": p.stat().st_size, "sha256": file_sha(p.read_bytes()), "crc32": f"{__import__('zlib').crc32(p.read_bytes()) & 0xffffffff:08x}"} for p in members],
}
write_json(PACK / "MANIFEST.json", manifest)
delivery = {
    "id": "PG327-W07-DELIVERY-363",
    "packetId": manifest["packetId"],
    "archive": ZIP_PATH.name,
    "scope": ["banishment-gate/W07"],
    "requestedDirectorAction": "Review the attached source-bound W07 TEST_ONLY witness. Identify exact defects or seal W07 only; leave W01-W06/W08 and Gate identity disposition untouched.",
    "spellDispositionRequested": "NONE",
    "applicationRequested": False,
    "sourceGap": {"id": "W03", "status": "OPEN; no qualifying source-bound same-body mechanical creature-type change"},
    "authority": {"queue": "Queue361", "applied": 828, "pending": 20, "acceptedUnapplied": 0, "heldIds": ["banishment-gate"], "blockers": ["PG200-B03", "PG200-B04"]},
    "members": manifest["members"],
}
write_json(PACK / "DELIVERY.json", delivery)

with zipfile.ZipFile(ZIP_PATH, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
    for p in sorted(q for q in PACK.rglob("*") if q.is_file()):
        zf.write(p, p.relative_to(PACK).as_posix())

with zipfile.ZipFile(ZIP_PATH, "r") as zf:
    infos = zf.infolist()
    names = [i.filename for i in infos]
    assert len(names) == len(set(names))
    assert sorted(names) == sorted(p.relative_to(PACK).as_posix() for p in PACK.rglob("*") if p.is_file())
    bad = zf.testzip()
    assert bad is None, bad
    for record in manifest["members"]:
        b = zf.read(record["path"])
        assert len(b) == record["bytes"] and file_sha(b) == record["sha256"]

archive_bytes = ZIP_PATH.read_bytes()
delivery_out = {
    "id": "PG327-W07-ARCHIVE-DELIVERY-363",
    "archive": ZIP_PATH.name,
    "bytes": len(archive_bytes),
    "sha256": file_sha(archive_bytes),
    "crc32": f"{__import__('zlib').crc32(archive_bytes) & 0xffffffff:08x}",
    "memberCount": len(infos),
    "exactMemberSet": True,
    "allMemberHashesAndCrcsVerified": True,
    "zipTest": "PASS",
    "caseReplay": "PASS forward; PASS exact inverse restoration",
    "decision": "TEST_ONLY W07 evidence submitted; Gate remains HOLD; no application",
}
write_json(OUT / "ARCHIVE_DELIVERY_363.json", delivery_out)
print(json.dumps({"output": str(OUT), "archive": str(ZIP_PATH), "archiveBytes": len(archive_bytes), "archiveSha256": file_sha(archive_bytes), "members": len(infos), "events": len(events), "initialSha256": sha(initial), "finalSha256": sha(state)}, ensure_ascii=False, indent=2))
