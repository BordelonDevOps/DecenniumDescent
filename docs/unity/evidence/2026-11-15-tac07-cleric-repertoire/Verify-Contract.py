"""Verify TAC-07 source/identity bindings only; does not compile or execute gameplay."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess

PACKET = Path(__file__).resolve().parent
ROOT = PACKET.parents[3]
BASELINE = "c4b5a0ad38974ab696ca2b2d7f66fa9de9f30aaa"
SOURCE = "46a4d52728ee6956f0bebcb5d2103ffd5bc67ba4"
RB = "DescentReviewChanges/ReviewBible/"
CATALOG = RB + "data/public/spell_playtests/catalog.json"
INDEX = RB + "data/public/spell_playtests/authored_review_index.json"
EXPECTED = [
    ("arcane-ward", 0, "InitialCantrip", 0, "Abjuration"),
    ("guidance", 781, "InitialCantrip", 0, "Universal"),
    ("spare-the-dying", 596, "InitialCantrip", 0, "Necromancy"),
    ("sanctuary", 21, "InitialRanked", 1, "Abjuration"),
    ("purify-food-and-drink", 24, "InitialRanked", 1, "Abjuration"),
    ("detect-magic", 216, "FutureCleric2RankedChoiceNotOwned", 1, "Divination"),
]
NEGATIVE = ["flare-spark", "dispel-magic-lesser", "light"]
AUTHORITY = ["CANON_MANIFEST.md", "docs/canon/CANON_MANIFEST.json", "docs/canon/REPOSITORY_PROMOTION.md",
             "docs/mechanics/CONTINUITY_SOURCE_OF_TRUTH.md"]
SOURCES = [
    RB + "docs/mechanics/CHARACTER_CREATION_PLAYTEST.md",
    RB + "docs/mechanics/CLASS_PLAYTEST_RULES.md",
    RB + "docs/mechanics/SPELL_INTEGRATION_RULES.md",
    RB + "data/playtest/character_foundation.json",
    RB + "data/public/class_playtests/cleric.json",
    RB + "docs/mechanics/classes/cleric.md",
    CATALOG, INDEX, RB + "data/public/spell_playtests/manifest.json",
    "src/data/spells.js", RB + "src/data/spells.js",
    "src/data/class-spell-progression.js", RB + "src/data/class-spell-progression.js",
    "data/public/Decennium_Descent_Core_Systems_Data_v2_Known_Descent.json",
]
DECISIONS = [
    "docs/unity/evidence/2026-11-03-rule-map/RULE_MAP.json",
    "docs/unity/evidence/2026-11-15-chr03-cleric-advancement/GPT_CONTRACT_REVIEW.md",
]
RUNTIME = ["Runtime/Core/Simulation.cs", "Runtime/Core/CharacterAdvancementRecords.cs",
           "Runtime/Core/ResonanceRecords.cs", "Runtime/Persistence/SnapshotCodec.cs",
           "Runtime/Persistence/ResonanceCodec.cs", "Laboratory/Model/SharedResonance.cs",
           "Laboratory/Model/SharedCharacterAdvancement.cs", "Laboratory/Model/ConnectedExpeditionSession.cs",
           "Laboratory/Model/ConnectedExpeditionView.cs", "Laboratory/Model/SharedWorldCommandQueries.cs"]

def git(*args):
    return subprocess.check_output(["git", *args], cwd=ROOT)

def sha(data):
    return hashlib.sha256(data).hexdigest()

def canonical(data):
    return json.dumps(data, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")

def write_json(path, value):
    path.write_bytes((json.dumps(value, indent=2, ensure_ascii=False) + "\n").encode("utf-8"))

def require(ok, message):
    if not ok:
        raise ValueError(message)

def blob(revision, path):
    identity = git("rev-parse", revision + ":" + path).decode().strip()
    return identity, git("cat-file", "blob", identity)

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--create-bindings", action="store_true")
    args = parser.parse_args()
    rows = ([(p, BASELINE, "authority") for p in AUTHORITY]
            + [(p, SOURCE, "pinned-source-preserve-own-status") for p in SOURCES]
            + [(p, BASELINE, "approved-map-or-actual-review") for p in DECISIONS]
            + [("engine/com.decennium.foundation/" + p, BASELINE, "accepted-runtime-audit") for p in RUNTIME])
    binding_path = PACKET / "SOURCE_API_BINDINGS.json"
    if args.create_bindings:
        entries = []
        for path, revision, role in rows:
            identity, data = blob(revision, path)
            entries.append({"path": path, "revision": revision, "role": role, "gitBlob": identity,
                            "sha256": sha(data), "bytes": len(data)})
        write_json(binding_path, {"baseline": BASELINE, "sourceRevision": SOURCE,
            "precedingReview": "b6c973bf-8890-57ea-b9e4-135b527b2ad9",
            "status": "SOURCE_BINDINGS_ONLY_NOT_RUNTIME_AUTHORITY", "sources": entries})
    bindings = json.loads(binding_path.read_text(encoding="utf-8"))
    require(bindings["baseline"] == BASELINE and bindings["sourceRevision"] == SOURCE, "Wrong baseline.")
    require([(x["path"], x["revision"], x["role"]) for x in bindings["sources"]] == rows, "Wrong source inventory.")
    payloads = {}
    for entry in bindings["sources"]:
        identity, data = blob(entry["revision"], entry["path"])
        require(identity == entry["gitBlob"] and sha(data) == entry["sha256"] and len(data) == entry["bytes"],
                "Changed source binding: " + entry["path"])
        payloads[entry["path"]] = data
    require(not git("diff", "--name-only", BASELINE, "--", "engine").strip(), "Engine changed during contract audit.")
    checks = []
    def check(name, ok):
        require(ok, name)
        checks.append({"name": name, "status": "PASS"})
    catalog = json.loads(payloads[CATALOG])
    index = json.loads(payloads[INDEX])
    by_id = {s["id"]: s for s in catalog["spells"]}
    by_review = {s["id"]: s for s in index["entries"]}
    check("Exactly 848 unique catalog identities retain separate placements",
          len(catalog["spells"]) == len(by_id) == len(by_review) == 848)
    check("Current authored index binds the exact normalized catalog bytes",
          index["currentSourceCatalogBinding"]["sha256"] == sha(payloads[CATALOG])
          and index["currentSourceCatalogBinding"]["bytes"] == len(payloads[CATALOG]))
    check("Main and preserved spell/progression mirrors match",
          payloads["src/data/spells.js"] == payloads[RB + "src/data/spells.js"]
          and payloads["src/data/class-spell-progression.js"] == payloads[RB + "src/data/class-spell-progression.js"])
    raw_text = payloads["src/data/spells.js"].decode("utf-8-sig")
    start = raw_text.index("{", raw_text.index("export const SPELLS"))
    raw, _ = json.JSONDecoder().raw_decode(raw_text[start:])
    check("Raw authoritative catalog has the same identities", set(raw) == set(by_id))
    manifest = json.loads(payloads[RB + "data/public/spell_playtests/manifest.json"])
    for source in manifest["sourceHashes"]:
        path = source["path"] if source["path"] in payloads else RB + source["path"]
        check("Manifest source hash: " + source["path"], sha(payloads[path]) == source["sha256"])
    progress = catalog["classProgression"]["Cleric"]
    check("Cleric first cantrip and rank1 access is level1; rank2 is level3",
          progress["mode"] == "full" and progress["learnLevels"]["0"] == 1
          and progress["learnLevels"]["1"] == 1 and progress["learnLevels"]["2"] == 3)
    js = payloads["src/data/class-spell-progression.js"].decode()
    check("Raw progression agrees with normalized first-access gates",
          re.search(r'Cleric:\s*\{\s*mode:\s*"full",\s*maxRank:\s*9,\s*learnLevels:\s*\{\s*0:\s*1,\s*1:\s*1,\s*2:\s*3', js) is not None)
    class_rules = payloads[RB + "docs/mechanics/CLASS_PLAYTEST_RULES.md"].decode()
    check("Fallback grants three initial cantrips, two first-access ranked spells, one per later class level",
          "full casters know 3 cantrips at 1" in class_rules
          and "choose 2 ranked spells at first spell access plus 1 each later class level" in class_rules)
    cleric = json.loads(payloads[RB + "data/public/class_playtests/cleric.json"])
    check("Cleric2 remains maximum rank1", cleric["maxSpellRankByClassLevel"][:2] == [1, 1])
    selected = []
    for spell_id, ordinal, origin, rank, school in EXPECTED:
        card = catalog["spells"][ordinal]
        review = by_review[spell_id]
        access = {"rank": rank, "minimumClassLevel": 1, "school": school, "baseRpCost": 0 if rank == 0 else 2}
        check("Exact operational identity/class access: " + spell_id,
              card["id"] == spell_id and card["status"] == "operational-playtest-draft"
              and card["classAccess"]["Cleric"] == access and card["additionalRpCost"] == 0
              and card["operational"]["id"] == spell_id
              and review["authoredStatus"] == "reviewed-authored-operational-playtest"
              and review["procedureFile"] == "catalog.json"
              and review["wholeCardPointer"] == "/spells/" + str(ordinal)
              and review["procedurePointer"] == "/spells/" + str(ordinal) + "/operational")
        check("Whole original catalog/class placements retained: " + spell_id,
              card["source"]["original"] == raw[spell_id]
              and card["source"]["catalogSha256"] == sha(payloads["src/data/spells.js"])
              and card["source"]["coreSha256"] == sha(payloads["data/public/Decennium_Descent_Core_Systems_Data_v2_Known_Descent.json"])
              and raw[spell_id]["classRanks"]["Cleric"] == rank
              and raw[spell_id]["classLearnLevels"]["Cleric"] == 1
              and raw[spell_id]["classSchools"]["Cleric"] == school)
        selected.append({"id": spell_id, "name": card["name"], "proposedOrigin": origin,
            "wholeCardPointer": review["wholeCardPointer"], "procedurePointer": review["procedurePointer"],
            "wholeCardSha256": sha(canonical(card)), "procedureSha256": sha(canonical(card["operational"])),
            "originalCatalogRecordSha256": sha(canonical(raw[spell_id])),
            "authoredReviewEntrySha256": sha(canonical(review)), "status": card["status"],
            "authoredStatus": review["authoredStatus"], "clericAccess": access,
            "allClassAccess": card["classAccess"], "allSourcePlacements": raw[spell_id]["placements"],
            "additionalRpCost": card["additionalRpCost"], "castingRuntime": "UNSUPPORTED"})
    check("Initial bundle has exactly three cantrips and two ranked distinct identities",
          len({x[0] for x in EXPECTED[:5]}) == 5 and [x[3] for x in EXPECTED[:5]] == [0, 0, 0, 1, 1])
    check("Detect Magic remains a distinct future earned choice, not a new rank gate",
          EXPECTED[5][0] not in {x[0] for x in EXPECTED[:5]} and EXPECTED[5][3] == 1)
    check("Duplicate school placements remain one global identity",
          len(raw["spare-the-dying"]["placements"]) == 2 and len(raw["detect-magic"]["placements"]) == 2)
    check("Negative controls preserve source class/rank/admission distinctions",
          "Cleric" not in by_id["flare-spark"]["classAccess"]
          and by_id["dispel-magic-lesser"]["classAccess"]["Cleric"]["minimumClassLevel"] == 3
          and by_id["dispel-magic-lesser"]["classAccess"]["Cleric"]["rank"] == 2
          and by_id["light"]["status"] == "blocked-pending-operational-review"
          and by_review["light"]["authoredStatus"] == "reviewed-authored-operational-playtest"
          and by_review["light"]["runtimeSelectionEnabled"] is False)
    negatives = [{"id": name, "wholeCardSha256": sha(canonical(by_id[name])),
                  "clericAccess": by_id[name]["classAccess"].get("Cleric"), "catalogStatus": by_id[name]["status"],
                  "authoredReview": by_review[name]} for name in NEGATIVE]
    spell_binding = {"sourceRevision": SOURCE, "catalogPath": CATALOG, "catalogSha256": sha(payloads[CATALOG]),
        "canonicalEntryHashEncoding": "UTF-8 JSON, sorted keys, compact separators, ensure_ascii=False",
        "initialOwnedCount": 5, "futureEarnedChoiceOwnedNow": False,
        "selected": selected, "negativeControls": negatives}
    spell_binding_path = PACKET / "SELECTED_SPELL_BINDINGS.json"
    if args.create_bindings:
        write_json(spell_binding_path, spell_binding)
    require(json.loads(spell_binding_path.read_text(encoding="utf-8")) == spell_binding, "Selected spell bindings differ.")
    rule_map = json.loads(payloads["docs/unity/evidence/2026-11-03-rule-map/RULE_MAP.json"])
    found = {}
    def walk(value):
        if isinstance(value, dict):
            if value.get("id") in ["TAC-07", "CHR-03"] and "dependencies" in value:
                found[value["id"]] = sorted(value["dependencies"])
            for child in value.values(): walk(child)
        elif isinstance(value, list):
            for child in value: walk(child)
    walk(rule_map)
    check("TAC07 and CHR03 preserve mapped prerequisite edges",
          found == {"TAC-07": ["CHR-02", "FND-05"], "CHR-03": ["CHR-02"]})
    resonance = payloads["engine/com.decennium.foundation/Runtime/Core/ResonanceRecords.cs"].decode()
    check("Accepted profile retains fixed level1 and original resource invariants",
          "character.Levels.Count != 1" in resonance and "pool.Maximum != 3" in resonance and "funding.Amount != 3" in resonance)
    names = ["README.md", "SOURCE_API_CONTRACT.md", "SOURCE_API_BINDINGS.json", "SELECTED_SPELL_BINDINGS.json", "Verify-Contract.py"]
    artifacts = {name: {"bytes": (PACKET / name).stat().st_size, "sha256": sha((PACKET / name).read_bytes())} for name in names}
    report = {"status": "PASS", "scope": "source/identity contract audit only", "baseline": BASELINE,
        "sourceEntriesVerified": len(rows), "checks": checks, "selectedIdentities": len(selected),
        "engineChanged": False, "compilation": "NOT RUN; engine unchanged", "runtimeTests": "NOT RUN; engine unchanged",
        "runtimeImplementationAuthorized": False, "reviewStatus": "PENDING ACTUAL CONTRACT REVIEW", "artifacts": artifacts}
    write_json(PACKET / "CONTRACT_VALIDATION.json", report)
    print(json.dumps({"status": "PASS", "sources": len(rows), "checks": len(checks),
                      "selected": len(selected), "engineChanged": False, "runtimeTests": "NOT RUN"}))

if __name__ == "__main__":
    main()
