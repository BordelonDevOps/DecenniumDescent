"""Verify source/baseline findings only; this is not gameplay or implementation approval."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess

PACKET = Path(__file__).resolve().parent
ROOT = PACKET.parents[3]
BASELINE = "459b8bf54ea46ecf45a0622ce99d5f18a77bd57f"
SOURCE = "46a4d52728ee6956f0bebcb5d2103ffd5bc67ba4"
RB = "DescentReviewChanges/ReviewBible/"
ENGINE = "engine/com.decennium.foundation/"
ROWS = [(name, BASELINE, "authority-or-accepted-decision") for name in [
    "CANON_MANIFEST.md", "docs/canon/CANON_MANIFEST.json", "docs/canon/REPOSITORY_PROMOTION.md",
    "docs/mechanics/CONTINUITY_SOURCE_OF_TRUTH.md", "docs/unity/evidence/2026-11-03-rule-map/RULE_MAP.json",
    "docs/unity/SHARED_WORLD_RULE_DECISIONS.md", "docs/unity/CONDITION_LIFECYCLE_RULE_DECISIONS.md",
    "docs/unity/CHARACTER_ADVANCEMENT_RULE_DECISIONS.md",
    "docs/unity/evidence/2026-11-15-chr03-cleric-advancement/SOURCE_API_CONTRACT.md",
    "docs/unity/evidence/2026-11-15-chr03-cleric-advancement/GPT_CONTRACT_REVIEW.md",
    "docs/unity/evidence/2026-11-15-tac07-cleric-repertoire/GPT_FINAL_REVIEW.md",
    "docs/unity/evidence/2026-11-15-tac07-cleric-repertoire/SELECTED_SPELL_BINDINGS.json",
    "docs/unity/evidence/2026-11-15-tac07-cleric-repertoire/regression/results.json",
    "docs/unity/evidence/2026-11-15-tac07-cleric-repertoire/regression/inventory.txt",
]] + [(RB + name, SOURCE, "pinned-gameplay-source") for name in [
    "docs/mechanics/CHARACTER_CREATION_PLAYTEST.md", "data/playtest/character_foundation.json",
    "docs/mechanics/CLASS_PLAYTEST_RULES.md", "data/public/class_playtests/cleric.json",
    "docs/mechanics/classes/cleric.md", "docs/mechanics/CLASS_PLAYTEST_BUILD_EXAMPLES.md",
    "docs/mechanics/XP_ADVANCEMENT_CANON.md", "docs/mechanics/SPELL_INTEGRATION_RULES.md",
    "docs/mechanics/COMBAT_ACTION_PLAYTEST.md", "docs/mechanics/CONDITIONS_PLAYTEST.md",
    "data/playtest/condition_playtests.json", "data/public/spell_playtests/catalog.json",
]] + [(ENGINE + name, BASELINE, "accepted-runtime-audit") for name in [
    "Runtime/Core/Simulation.cs", "Runtime/Core/CharacterAdvancementRecords.cs",
    "Runtime/Core/ResonanceRecords.cs", "Runtime/Core/SpellRepertoireRecords.cs",
    "Runtime/Core/SpellSourceCatalog.cs", "Runtime/Core/WorldScheduleRecord.cs",
    "Runtime/Core/LaterEncounterRecords.cs", "Runtime/Core/ReinforcementRecords.cs",
    "Runtime/Core/ConditionJournal.cs", "Runtime/Persistence/SnapshotCodec.cs",
    "Runtime/Persistence/SpellRepertoireCodec.cs", "Runtime/Persistence/ConditionJournalCodec.cs",
    "Laboratory/Model/SharedCharacterAdvancement.cs", "Laboratory/Model/SharedResonance.cs",
    "Laboratory/Model/SharedSpellRepertoire.cs", "Laboratory/Model/SharedLaterEncounter.cs",
    "Laboratory/Model/SharedReinforcement.cs", "Laboratory/Model/ConditionApplications.cs",
    "Laboratory/Model/ConditionLedger.cs", "Laboratory/Model/ConditionHistory.cs",
    "Laboratory/Model/PlaytestConditions.cs", "Laboratory/Model/RangedAttackResolution.cs",
    "Laboratory/Model/ConnectedExpeditionSession.cs",
]]


def git(*args):
    return subprocess.check_output(["git", *args], cwd=ROOT)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()


def write(path, value):
    path.write_bytes((json.dumps(value, indent=2, ensure_ascii=False) + "\n").encode())


def require(condition, message):
    if not condition:
        raise ValueError(message)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--create-bindings", action="store_true")
    args = parser.parse_args()
    entries, payloads = [], {}
    for path, revision, role in ROWS:
        blob = git("rev-parse", revision + ":" + path).decode().strip()
        data = git("cat-file", "blob", blob)
        entries.append({"path": path, "revision": revision, "role": role, "gitBlob": blob,
                        "sha256": sha(data), "bytes": len(data)})
        payloads[path] = data
    binding = {"baseline": BASELINE, "sourceRevision": SOURCE, "sources": entries,
               "status": "SOURCE_AND_CAPABILITY_AUDIT_ONLY_NOT_RUNTIME_AUTHORITY"}
    if args.create_bindings:
        write(PACKET / "SOURCE_BINDINGS.json", binding)
    require(json.loads((PACKET / "SOURCE_BINDINGS.json").read_bytes()) == binding, "Pinned binding inventory differs")
    require(not git("diff", "--name-only", BASELINE, "--", "engine").strip(), "Engine changed during source audit")
    checks = []

    def check(name, result):
        require(result, name)
        checks.append({"name": name, "status": "PASS"})

    cleric = json.loads(payloads[RB + "data/public/class_playtests/cleric.json"])
    foundation = json.loads(payloads[RB + "data/playtest/character_foundation.json"])["classes"][1]
    cards = {row["id"]: row for row in cleric["cards"]}
    check("Cleric2 d8/base5 and RP3-to4", foundation["class"] == "Cleric" and foundation["hitDie"] == 8
          and foundation["fixedLaterLevelHpBase"] == 5 and foundation["rpByClassLevel"][:2] == [3, 4]
          and cleric["rpByClassLevel"][:2] == [3, 4])
    check("Two Base selections with no active minimum or ASI", cleric["schedule"][1] ==
          {"classLevel": 2, "choose": 2, "bands": ["Base"], "minimumActives": 0, "asiOrFeat": False})
    check("Automatic Attunement and selected Radiance at2", all(cards[key]["acquisition"] == "automatic"
          and cards[key]["minimumClassLevel"] == 2 for key in ["cleric.base.invocation-attunement", "cleric.base.radiance.radiance"]))
    check("Selected unowned Base cards are legal", all(cards[key]["acquisition"] == "selection"
          and cards[key]["band"] == "Base" and cards[key]["minimumClassLevel"] <= 2
          for key in ["cleric.base.judging-light", "cleric.base.conviction-pool"]))
    rite, radiance = cards["cleric.base.healing-rite"], cards["cleric.base.radiance.radiance"]
    check("Healing Rite is Action2RP on living ally within30ft", rite["activation"] == "Action"
          and rite["cost"] == "2 RP" and rite["rangeAndTarget"] == "One living ally within 30 feet")
    check("Radiance requires actual own-turn healing and names both cures", all(text in radiance["effect"]
          for text in ["Once on each of your turns", "restores HP", "S additional HP", "Frightened or Poisoned"]))
    check("Pool changes maximum without funding", "Increase your Conviction maximum by 2" in cards["cleric.base.conviction-pool"]["effect"]
          and "does not immediately restore" in cards["cleric.base.conviction-pool"]["effect"])
    creation = payloads[RB + "docs/mechanics/CHARACTER_CREATION_PLAYTEST.md"].decode()
    check("Advancement is not healing or rest", "Keep current HP and spent resources unchanged" in creation and "not healing or a rest" in creation)
    check("Objective preannouncement source remains explicit", "other milestones announced before the Opening begins"
          in payloads[RB + "docs/mechanics/XP_ADVANCEMENT_CANON.md"].decode())
    prior = "docs/unity/evidence/2026-11-15-tac07-cleric-repertoire/"
    selected = json.loads(payloads[prior + "SELECTED_SPELL_BINDINGS.json"])
    detect = next(row for row in selected["selected"] if row["id"] == "detect-magic")
    catalog = json.loads(payloads[RB + "data/public/spell_playtests/catalog.json"])["spells"]
    card = catalog[int(detect["wholeCardPointer"].split("/")[-1])]
    check("Earned DetectMagic retains exact card/procedure and Cleric placement", card["id"] == "detect-magic"
          and sha(canonical(card)) == detect["wholeCardSha256"] and sha(canonical(card["operational"])) == detect["procedureSha256"]
          and card["classAccess"]["Cleric"]["rank"] == 1 and card["classAccess"]["Cleric"]["school"] == "Divination")
    earned = payloads[ENGINE + "Laboratory/Model/SharedSpellRepertoire.cs"].decode()
    check("Accepted settlement requires staged real milestone and advancement", all(text in earned for text in
          ["SettleClericEarnedRepertoire", "milestone.ConsumedRevision != advancement.Revision", "staged.CharacterAdvancements.Contains(advancement)"]))
    timing = payloads[ENGINE + "Runtime/Core/LaterEncounterRecords.cs"].decode()
    closure = payloads[ENGINE + "Laboratory/Model/SharedLaterEncounter.cs"].decode()
    check("Actor timing prioritizes retained reinforcement epoch", "phase.Epoch.Order.Contains(actor)) return phase.Epoch" in timing)
    check("Closure clears encounter and encounter timing can fall back", "state.Encounter = null" in closure
          and "public static WorldScheduleRecord ForEncounter" in timing and ": state.WorldSchedule" in timing)
    check("Reinforcement interval starts use global numbering", "admission.Phase.GlobalTurn(local)" in timing
          and "global - phase.FirstTurn" in payloads[ENGINE + "Laboratory/Model/SharedReinforcement.cs"].decode())
    application = payloads[ENGINE + "Laboratory/Model/ConditionApplications.cs"].decode()
    match = re.search(r"enum ConditionKind\s*\{([^}]+)\}", application)
    require(match is not None, "Condition lifecycle enum missing")
    kinds = [x.strip() for x in match.group(1).split(",")]
    check("Poisoned lifecycle exists and Frightened lifecycle is absent", "Poisoned" in kinds and "Frightened" not in kinds and len(kinds) == 14)
    check("Journal interpreter rejects unsupported identities", "Unsupported condition identity in journal"
          in payloads[ENGINE + "Laboratory/Model/ConditionHistory.cs"].decode())
    check("Frightened currently exists only as supplied projection in inspected calculation", "ConditionClause.Frightened)&&frightenedSourceVisible"
          in payloads[ENGINE + "Laboratory/Model/PlaytestConditions.cs"].decode())
    condition_source = payloads[RB + "docs/mechanics/CONDITIONS_PLAYTEST.md"].decode()
    fear = condition_source.split("## Frightened", 1)[1].split("## Grappled", 1)[0]
    check("Frightened source requires independent fear identity and actual behavior", all(text in fear for text in
          ["Each application records its fear source", "ability checks and attack rolls", "cannot willingly move closer",
           "Separate fear sources", "Fear immunity blocks application", "Forced movement"]))
    found = {}

    def visit(value):
        if isinstance(value, dict):
            if value.get("id") in ["CHR-03", "TAC-05", "TAC-07", "TAC-08", "CHR-05"] and "dependencies" in value:
                found[value["id"]] = sorted(value["dependencies"])
            for child in value.values():
                visit(child)
        elif isinstance(value, list):
            for child in value:
                visit(child)

    visit(json.loads(payloads["docs/unity/evidence/2026-11-03-rule-map/RULE_MAP.json"]))
    expected = {"CHR-03": ["CHR-02"], "TAC-05": ["TAC-01", "RUL-05"], "TAC-07": ["CHR-02", "FND-05"],
                "TAC-08": ["TAC-02", "TAC-05", "TAC-07"], "CHR-05": ["CHR-03", "TAC-02", "TAC-05", "TAC-08"]}
    check("Approved direct map edges are unchanged", found == {key: sorted(value) for key, value in expected.items()})
    result = json.loads(payloads[prior + "regression/results.json"])
    inventory = payloads[prior + "regression/inventory.txt"].decode("utf-8-sig").splitlines()
    check("Accepted predecessor result retains exact1509 unique cases", result["status"] == "PASS" and result["passed"] == 1509
          and result["failed"] == 0 and len(inventory) == len(set(inventory)) == 1509
          and [row["Name"] for row in result["cases"]] == inventory)
    selected_cards = {key: {"sha256": sha(canonical(cards[key])), "source": cards[key]["source"]} for key in
                      ["cleric.base.healing-rite", "cleric.base.invocation-attunement", "cleric.base.radiance.radiance",
                       "cleric.base.judging-light", "cleric.base.conviction-pool"]}
    artifacts = {path.name: {"bytes": path.stat().st_size, "sha256": sha(path.read_bytes())}
                 for path in sorted(PACKET.iterdir()) if path.is_file() and path.name != "AUDIT_VALIDATION.json"}
    report = {"status": "PASS", "scope": "source identity and concrete capability findings only", "baseline": BASELINE,
              "sourceEntriesVerified": len(entries), "checks": checks, "selectedCards": selected_cards,
              "engineChanged": False, "compilation": "NOT RUN; no engine changes", "runtimeTests": "NOT RUN; no engine changes",
              "runtimeImplementationAuthorized": False, "fullContractReview": "HELD until the selected TAC-05 Frightened prerequisite is implemented and accepted",
              "contextReview": "68898ea2-4ba8-52e5-afe9-ac081a2dbd12",
              "dependencyReview": "aee19602-eb93-5f80-b5f7-90dd14d2fcee",
              "artifacts": artifacts}
    write(PACKET / "AUDIT_VALIDATION.json", report)
    print(json.dumps({"status": "PASS", "sources": len(entries), "checks": len(checks), "engineChanged": False, "runtimeTests": "NOT RUN"}))


if __name__ == "__main__":
    main()
