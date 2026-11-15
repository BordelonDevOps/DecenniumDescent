"""Bind and verify the CHR-03 source/API audit. This does not run engine tests."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess

PACKET = Path(__file__).resolve().parent
ROOT = PACKET.parents[3]
BASELINE = "29eed15d770de93f00217a0d9977c5bb489cfca4"
SOURCE = "46a4d52728ee6956f0bebcb5d2103ffd5bc67ba4"

def git(*args):
    return subprocess.check_output(["git", *args], cwd=ROOT)

def sha(data):
    return hashlib.sha256(data).hexdigest()

def read_blob(revision, path):
    blob = git("rev-parse", revision + ":" + path).decode().strip()
    return blob, git("cat-file", "blob", blob)

def write_json(path, value):
    path.write_bytes((json.dumps(value, indent=2, ensure_ascii=False) + "\n").encode("utf-8"))

def require(condition, message):
    if not condition:
        raise ValueError(message)

SOURCE_ROWS = [
    ("CANON_MANIFEST.md", BASELINE, "authority-pointer", ["single domain registry"]),
    ("docs/canon/CANON_MANIFEST.json", BASELINE, "authority-registry", ["/domains", "/opsProtocol"]),
    ("docs/canon/REPOSITORY_PROMOTION.md", BASELINE, "promotion-authority", ["Layers", "Promotion path"]),
    ("docs/mechanics/CONTINUITY_SOURCE_OF_TRUTH.md", BASELINE, "ops-and-override-tracker", ["5. Pending owner override questions"]),
    ("DescentReviewChanges/ReviewBible/docs/mechanics/CHARACTER_CREATION_PLAYTEST.md", SOURCE, "reviewed-playtest", ["Gain a level", "One shared RP pool"]),
    ("DescentReviewChanges/ReviewBible/data/playtest/character_foundation.json", SOURCE, "reviewed-playtest", ["/classes/1"]),
    ("DescentReviewChanges/ReviewBible/docs/mechanics/CLASS_PLAYTEST_RULES.md", SOURCE, "provisional-playtest", ["Reading a class card", "Spell repertoires and acquisition"]),
    ("DescentReviewChanges/ReviewBible/data/public/class_playtests/cleric.json", SOURCE, "provisional-playtest", ["/engine/1", "/engine/8", "/engine/9", "/engine/11", "/schedule/1", "/rpByClassLevel", "/cards"]),
    ("DescentReviewChanges/ReviewBible/docs/mechanics/classes/cleric.md", SOURCE, "rendered-class-guide", ["Class engine and setup", "Invocation Attunement", "Radiance", "Conviction Pool"]),
    ("DescentReviewChanges/ReviewBible/docs/mechanics/CLASS_PLAYTEST_BUILD_EXAMPLES.md", SOURCE, "legal-example-not-mandatory-choice", ["Cleric / Saint / levels 1 and 2"]),
    ("DescentReviewChanges/ReviewBible/docs/mechanics/XP_ADVANCEMENT_CANON.md", SOURCE, "advancement-provenance", ["Official Opening advancement"]),
    ("DescentReviewChanges/ReviewBible/docs/mechanics/SPELL_INTEGRATION_RULES.md", SOURCE, "reviewed-playtest-integration", ["Select a spell"]),
    ("docs/unity/evidence/2026-11-03-rule-map/RULE_MAP.json", BASELINE, "approved-implementation-map", ["CHR-03", "TAC-07", "TAC-08", "CHR-05"]),
    ("docs/unity/CHARACTER_ADVANCEMENT_RULE_DECISIONS.md", BASELINE, "existing-prototype-policy", ["Source rules implemented", "Prototype policies adopted for this slice"]),
    ("docs/unity/evidence/2026-11-15-chr02-shared-rp/GPT_FINAL_REVIEW.md", BASELINE, "actual-predecessor-acceptance", ["84bd8644-f237-55a4-8d15-c8a18ddda017"]),
    ("docs/unity/evidence/2026-11-15-chr02-shared-rp/GPT_CONTRACT_REVIEW.md", BASELINE, "actual-predecessor-contract", ["Initial funding", "Lawful class access"]),
]
RUNTIME_PATHS = [
    "Runtime/Core/Simulation.cs",
    "Runtime/Core/CharacterAdvancementRecords.cs",
    "Runtime/Core/ResonanceRecords.cs",
    "Runtime/Persistence/SnapshotCodec.cs",
    "Runtime/Persistence/ResonanceCodec.cs",
    "Laboratory/Model/SharedCharacterAdvancement.cs",
    "Laboratory/Model/SharedResonance.cs",
    "Laboratory/Model/ConnectedExpeditionSession.cs",
    "Laboratory/Model/ConnectedExpeditionView.cs",
    "Laboratory/Model/SharedWorldCommandQueries.cs",
    "Laboratory/Model/SharedExpeditionEpisodeClose.cs",
]

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--create-bindings", action="store_true")
    args = parser.parse_args()
    rows = SOURCE_ROWS + [("engine/com.decennium.foundation/" + path, BASELINE, "accepted-runtime-audit", [])
                          for path in RUNTIME_PATHS]
    binding_path = PACKET / "SOURCE_API_BINDINGS.json"
    if args.create_bindings:
        entries = []
        for path, revision, authority, selectors in rows:
            blob, payload = read_blob(revision, path)
            entries.append({"path": path, "revision": revision, "gitBlob": blob,
                            "sha256": sha(payload), "bytes": len(payload),
                            "authority": authority, "selectors": selectors})
        write_json(binding_path, {"baseline": BASELINE, "sourceRevision": SOURCE,
            "predecessorAcceptance": "84bd8644-f237-55a4-8d15-c8a18ddda017",
            "status": "PENDING_SOURCE_API_REVIEW_NOT_RUNTIME_AUTHORITY", "sources": entries})
    bindings = json.loads(binding_path.read_text(encoding="utf-8"))
    require(bindings["baseline"] == BASELINE and bindings["sourceRevision"] == SOURCE, "Wrong baseline.")
    require([(e["path"], e["revision"], e["authority"], e["selectors"]) for e in bindings["sources"]] == rows,
            "Source inventory differs.")
    payloads = {}
    for entry in bindings["sources"]:
        blob, payload = read_blob(entry["revision"], entry["path"])
        require(blob == entry["gitBlob"] and sha(payload) == entry["sha256"] and len(payload) == entry["bytes"],
                "Binding differs: " + entry["path"])
        payloads[entry["path"]] = payload
    require(not git("diff", "--name-only", BASELINE, "--", "engine").strip(), "Engine changed during contract audit.")
    checks = []
    def check(name, condition):
        require(condition, name)
        checks.append({"name": name, "status": "PASS"})
    prefix = "DescentReviewChanges/ReviewBible/"
    foundation = json.loads(payloads[prefix + "data/playtest/character_foundation.json"])
    cleric = json.loads(payloads[prefix + "data/public/class_playtests/cleric.json"])
    chassis = foundation["classes"][1]
    check("Cleric chassis has d8, later fixed base5 and RP3-to4",
          chassis["class"] == "Cleric" and chassis["hitDie"] == 8 and chassis["fixedLaterLevelHpBase"] == 5
          and chassis["rpByClassLevel"][:2] == [3, 4] and cleric["rpByClassLevel"][:2] == [3, 4])
    row = cleric["schedule"][1]
    check("Level2 requires two Base selections, no active minimum or ASI",
          row == {"classLevel": 2, "choose": 2, "bands": ["Base"], "minimumActives": 0, "asiOrFeat": False})
    cards = {c["id"]: c for c in cleric["cards"]}
    attune = cards["cleric.base.invocation-attunement"]
    radiance = cards["cleric.base.radiance.radiance"]
    check("Attunement and Radiance are automatic level2 grants",
          attune["minimumClassLevel"] == 2 and attune["acquisition"] == "automatic"
          and radiance["minimumClassLevel"] == 2 and radiance["acquisition"] == "automatic"
          and "Once on each of your turns" in radiance["effect"]
          and "Frightened or Poisoned" in radiance["effect"])
    initial = {"cleric.base.consecrate", "cleric.base.healing-rite", "cleric.base.consecrated-ground",
               "cleric.base.fervent-ritualist"}
    selected = ["cleric.base.judging-light", "cleric.base.conviction-pool"]
    check("Candidate two selections are distinct legal unowned Base cards",
          len(set(selected)) == 2 and all(c not in initial and cards[c]["acquisition"] == "selection"
          and cards[c]["band"] == "Base" and cards[c]["minimumClassLevel"] <= 2 for c in selected))
    check("Conviction Pool increases maximum without immediate restoration",
          "Increase your Conviction maximum by 2" in cards[selected[1]]["effect"]
          and "does not immediately restore spent Conviction" in cards[selected[1]]["effect"])
    rules = payloads[prefix + "docs/mechanics/CLASS_PLAYTEST_RULES.md"].decode()
    check("Full-caster fallback includes one ranked spell at each later class level",
          "plus 1 each later class level" in rules and "does not replace a more specific" in rules)
    xp = payloads[prefix + "docs/mechanics/XP_ADVANCEMENT_CANON.md"].decode()
    check("Other Opening milestones must be preannounced",
          "other milestones announced before the Opening begins" in xp)
    creation = payloads[prefix + "docs/mechanics/CHARACTER_CREATION_PLAYTEST.md"].decode()
    check("Advancement preserves HP and spent resources",
          "Keep current HP and spent resources unchanged" in creation and "not healing or a rest" in creation)
    runtime = payloads["engine/com.decennium.foundation/Laboratory/Model/SharedCharacterAdvancement.cs"].decode()
    check("Current advancement is explicitly Soldier-scoped",
          'if(!supportedProfile)return "UnsupportedAdvancementPath"' in runtime
          and 'new CharacterLevelFact("Soldier",6)' in runtime)
    resonance = payloads["engine/com.decennium.foundation/Runtime/Core/ResonanceRecords.cs"].decode()
    check("Existing shared RP reconciliation preserves current balance and funding",
          "Math.Min(Current, maximum), InitialFunding" in resonance)
    check("Accepted Cleric envelope is fixed at level1 capacity",
          "character.Levels.Count != 1" in resonance and "life.MaximumHp != 8" in resonance and "pool.Maximum != 3" in resonance)
    rule_map = json.loads(payloads["docs/unity/evidence/2026-11-03-rule-map/RULE_MAP.json"])
    found = {}
    def walk(value):
        if isinstance(value, dict):
            if value.get("id") in ["CHR-03", "TAC-07", "TAC-08", "CHR-05"] and "dependencies" in value:
                found[value["id"]] = value["dependencies"]
            for child in value.values(): walk(child)
        elif isinstance(value, list):
            for child in value: walk(child)
    walk(rule_map)
    # A dependency list names prerequisite edges, not an execution sequence.
    check("Approved dependency branches remain separate",
          {name: sorted(edges) for name, edges in found.items()} ==
          {name: sorted(edges) for name, edges in {
              "CHR-03": ["CHR-02"], "TAC-07": ["CHR-02", "FND-05"],
              "TAC-08": ["TAC-07", "TAC-02", "TAC-05"],
              "CHR-05": ["CHR-03", "TAC-02", "TAC-05", "TAC-08"]}.items()})
    artifacts = {}
    for name in ["README.md", "SOURCE_API_CONTRACT.md", "SOURCE_API_BINDINGS.json", "Verify-Contract.py"]:
        data = (PACKET / name).read_bytes()
        artifacts[name] = {"bytes": len(data), "sha256": sha(data)}
    report = {"status": "PASS", "scope": "source and baseline contract audit only",
              "baseline": BASELINE, "sourceEntriesVerified": len(rows), "checks": checks,
              "engineChanged": False, "compilation": "NOT RUN; engine unchanged",
              "runtimeTests": "NOT RUN; engine unchanged", "runtimeImplementationAuthorized": False,
              "reviewStatus": "PENDING", "artifacts": artifacts}
    write_json(PACKET / "CONTRACT_VALIDATION.json", report)
    print(json.dumps({"status": "PASS", "sources": len(rows), "checks": len(checks),
                      "engineChanged": False, "runtimeTests": "NOT RUN"}))

if __name__ == "__main__":
    main()
