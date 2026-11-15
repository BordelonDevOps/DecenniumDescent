"""Verify pinned TAC-05 source facts and baseline gaps; not runtime acceptance."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess

PACKET = Path(__file__).resolve().parent
ROOT = PACKET.parents[3]
BASELINE = "f69eebcdc2361e38d42501c1fa08a5e6dd4d8c43"
SOURCE = "46a4d52728ee6956f0bebcb5d2103ffd5bc67ba4"
RB = "DescentReviewChanges/ReviewBible/"
ENGINE = "engine/com.decennium.foundation/"
PRIOR = "docs/unity/evidence/2026-11-15-tac07-cleric-repertoire/"
ROWS = [(p, BASELINE, "authority-and-accepted-baseline") for p in [
    "CANON_MANIFEST.md", "docs/canon/CANON_MANIFEST.json", "docs/canon/REPOSITORY_PROMOTION.md",
    "docs/mechanics/CONTINUITY_SOURCE_OF_TRUTH.md", "engine/AGENTS.md",
    "docs/unity/evidence/2026-11-03-rule-map/RULE_MAP.json",
    "docs/unity/CONDITION_LIFECYCLE_RULE_DECISIONS.md", "docs/unity/SHARED_WORLD_RULE_DECISIONS.md",
    "docs/unity/evidence/2026-11-14-tac06-maximum-hp/SOURCE_API_CONTRACT.md",
    "docs/unity/evidence/2026-11-15-chr03-cleric-settlement/GPT_DEPENDENCY_REVIEW.md",
    "docs/unity/evidence/2026-11-15-chr03-cleric-settlement/GPT_CONTEXT_GUIDANCE.md",
    PRIOR + "GPT_FINAL_REVIEW.md", PRIOR + "regression/results.json", PRIOR + "regression/inventory.txt",
]] + [(RB + p, SOURCE, "pinned-gameplay-source") for p in [
    "data/public/class_playtests/warrior.json", "docs/mechanics/classes/warrior.md",
    "docs/mechanics/CLASS_PLAYTEST_RULES.md", "docs/mechanics/CONDITIONS_PLAYTEST.md",
    "data/playtest/condition_playtests.json", "docs/mechanics/CORE_RESOLUTION_PLAYTEST.md",
    "docs/mechanics/COMBAT_ACTION_PLAYTEST.md",
]] + [(ENGINE + p, BASELINE, "accepted-runtime-audit") for p in [
    "Runtime/Core/Simulation.cs", "Runtime/Core/ConditionJournal.cs",
    "Runtime/Core/CharacterAdvancementRecords.cs", "Runtime/Core/WorldScheduleRecord.cs",
    "Runtime/Core/WorldPositionResolver.cs", "Runtime/Core/LaterEncounterRecords.cs",
    "Runtime/Core/ReinforcementRecords.cs", "Runtime/Persistence/SnapshotCodec.cs",
    "Runtime/Persistence/ConditionJournalCodec.cs", "Laboratory/Model/ConditionApplications.cs",
    "Laboratory/Model/ConditionHistory.cs", "Laboratory/Model/ConditionLedger.cs",
    "Laboratory/Model/PlaytestConditions.cs", "Laboratory/Model/RangedAttackResolution.cs",
    "Laboratory/Model/TestOnlyClubAttackPolicy.cs", "Laboratory/Model/SharedWorldRangedCombat.cs",
    "Laboratory/Model/ObservationRules.cs", "Laboratory/Model/ObservationGeometry.cs",
    "Laboratory/Model/SharedObservationActions.cs", "Laboratory/Model/SharedExplorationHide.cs",
    "Laboratory/Model/SharedWorldDefinitions.cs", "Laboratory/Model/PlanarCombatGeometry.cs",
    "Laboratory/Model/SharedWorldCommandQueries.cs", "Laboratory/Model/TacticalMovementPolicy.cs",
    "Laboratory/Model/SharedLaterEncounter.cs", "Laboratory/Model/SharedReinforcement.cs",
    "Laboratory/Model/SharedCharacterAdvancement.cs", "Laboratory/Model/ConnectedExpeditionSession.cs",
    "Laboratory/Model/LaterDefenderController.cs", "Laboratory/Model/SharedSpellRepertoire.cs",
    "Laboratory/Model/RuleResolution.cs", "Laboratory/Model/TestOnlySharedWorldPolicy.cs",
]]


def git(*args):
    return subprocess.check_output(["git", *args], cwd=ROOT)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()


def write(name, value):
    (PACKET / name).write_bytes((json.dumps(value, indent=2, ensure_ascii=False) + "\n").encode())


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
        write("SOURCE_BINDINGS.json", binding)
    require(json.loads((PACKET / "SOURCE_BINDINGS.json").read_bytes()) == binding, "Source inventory differs")
    require(not git("diff", "--name-only", BASELINE, "--", "engine").strip(), "Engine changed during contract audit")
    checks = []

    def check(name, result):
        require(result, name)
        checks.append({"name": name, "status": "PASS"})

    def text(path):
        return payloads[path].decode("utf-8-sig")

    warrior = json.loads(payloads[RB + "data/public/class_playtests/warrior.json"])
    card = warrior["cards"][8]
    check("Exact selected provisional active card identity", card["id"] == "warrior.base.intimidating-presence"
          and card["designStatus"] == "provisional-playtest" and card["sourceKind"] == "active")
    check("Selection and actual Warrior2 gate", card["acquisition"] == "selection"
          and card["className"] == "Warrior" and card["band"] == "Base" and card["minimumClassLevel"] == 2)
    check("Action zero cost maximum2 rounds Recharge3", [card[k] for k in ["activation", "cost", "duration", "frequency"]]
          == ["Action", "0", "Maximum 2 rounds", "Recharge 3 rounds"])
    check("Up to3 enemies within15ft see-or-hear target predicate", card["rangeAndTarget"]
          == "Up to 3 enemies of your choice within 15 feet that can see or hear you")
    check("Actual WIS save fear-of-user and first repeat endpoint", all(x in card["effect"] for x in
          ["Each target makes a Wisdom save", "Frightened of you", "end of its next turn, then repeats the save"]))
    check("One final round and same-use immunity no forced surrender", all(x in card["effect"] for x in
          ["second failure extends the fear one final round", "immune to this use", "never forces surrender"]))
    check("DC uses chosen modifier not minimum-one M", "Warrior technique save DC = 8 + normal character proficiency bonus + chosen modifier"
          in warrior["engine"][0] and "M = max(1, chosen Warrior ability modifier)" in warrior["engine"][0])
    check("Warrior ability choice is permanent", "choose Strength or Dexterity" in warrior["engine"][0]
          and "choice is permanent" in warrior["engine"][0])
    common = text(RB + "docs/mechanics/CLASS_PLAYTEST_RULES.md")
    check("Common preflight before spending and failed legal save still pays", "before spending anything" in common
          and "failed legal attack/save attempt still pays" in common)
    check("Regular start and outside6seconds recharge no double count", all(x in common for x in
          ["Recharge N sets a counter to N", "start of the owner's regular initiative turn", "whether able to act or not",
           "Extra turns/Actions do not tick", "Outside combat tick once per 6 elapsed seconds, without double counting"]))
    conditions = json.loads(payloads[RB + "data/playtest/condition_playtests.json"])
    fear = conditions["conditions"][9]
    check("Exact generic Frightened source identity", fear["id"] == "frightened")
    check("Visible check and attack disadvantage but unconditional willing restriction", all(x in fear["effect"] for x in
          ["visible/in line of sight", "ability checks and attack rolls", "cannot willingly move closer"]))
    check("Independent fear source and source-defined endings", "records its fear source" in fear["application"]
          and "applying effect's duration and repeat-save procedure" in fear["durationAndEnding"]
          and "tracked independently" in fear["stacking"])
    check("Fear immunity prevents and forced movement may approach", "Fear immunity blocks application" in fear["immunitiesAndOverrides"]
          and "Forced movement may move the creature closer" in fear["immunitiesAndOverrides"])
    shared = text(RB + "docs/mechanics/CONDITIONS_PLAYTEST.md")
    check("Generic named cure all sources with explicit narrower exception", "A generic cure naming a condition clears its source records"
          in shared and "one-record scope" in shared)
    check("Suppression clocks continue and removing immunity never restarts", "their clocks continue" in shared
          and "restart an old duration" in shared)
    consensus = text("docs/unity/CONDITION_LIFECYCLE_RULE_DECISIONS.md")
    check("Actual consensus includes suppressed eligible cures", "present, unexpired records, including suppressed ones" in consensus)
    application = text(ENGINE + "Laboratory/Model/ConditionApplications.cs")
    enum = re.search(r"enum ConditionKind\s*\{([^}]+)\}", application)
    require(enum is not None, "Condition enum missing")
    kinds = [x.strip() for x in enum.group(1).split(",")]
    check("Baseline generic lifecycle contains14 identities without Frightened", len(kinds) == 14 and "Frightened" not in kinds)
    history = text(ENGINE + "Laboratory/Model/ConditionHistory.cs")
    check("Baseline restore enforces exact old policy and kind parser", 'TEST_ONLY.generic-conditions-v1' in history
          and "journal.PolicyId != PolicyId" in history and "Unsupported condition identity in journal" in history)
    check("Baseline structural immunity-set maximum is14", "copy.Length > 14" in text(ENGINE + "Runtime/Core/ConditionJournal.cs"))
    check("Baseline fear attack projection requires supplied visibility", "ConditionClause.Frightened)&&frightenedSourceVisible"
          in text(ENGINE + "Laboratory/Model/PlaytestConditions.cs"))
    observation = text(ENGINE + "Laboratory/Model/ObservationRules.cs")
    check("Actual observation distinguishes hidden from geometric sight", "return !HiddenTo(s, observerId, targetId)" in observation)
    positions = text(ENGINE + "Runtime/Core/WorldPositionResolver.cs")
    check("Exact position includes partial traversal and attached route", "edge.DistanceFeet.Numerator" in positions
          and "RouteTravelSpatial" in positions and "RuleQuantity.FromFraction" in positions)
    check("Existing tactical metric is Chebyshev5ft", "5*Math.Max(Math.Abs((long)to.X-from.X),Math.Abs((long)to.Y-from.Y))"
          in text(ENGINE + "Laboratory/Model/PlanarCombatGeometry.cs"))
    later = text(ENGINE + "Laboratory/Model/SharedLaterEncounter.cs")
    check("Defender has actual numericalWarrior3 and own condition target", '"TEST_ONLY.numeric-warrior3"' in later
          and "bodies.RegisterDeferredConditionTarget(LaterDefenderId)" in later and "state.Characters = state.Characters.Append" in later)
    initial = text(ENGINE + "Laboratory/Model/TestOnlySharedWorldPolicy.cs").split("public Snapshot Initial()", 1)[1]
    check("Defender is created during initial world construction before encounter entry", "InitializeLaterEncounter(s);" in initial
          and initial.index("InitializeLaterEncounter(s);") < initial.index("InitializeClericRepertoire(s);"))
    timing = text(ENGINE + "Runtime/Core/LaterEncounterRecords.cs")
    check("Actor timing retains reinforcement epoch", "phase.Epoch.Order.Contains(actor)) return phase.Epoch" in timing)
    check("Existing shared feature runtime already owns Soldier recharge", "TacticalAssessmentRechargeRemaining" in
          text(ENGINE + "Runtime/Core/CharacterAdvancementRecords.cs") and "regularStartsElapsed" in
          text(ENGINE + "Runtime/Core/CharacterAdvancementRecords.cs"))
    dependency = text("docs/unity/evidence/2026-11-15-chr03-cleric-settlement/GPT_DEPENDENCY_REVIEW.md")
    check("Actual GPT selects prerequisite and prohibits unrestricted cure", "aee19602-eb93-5f80-b5f7-90dd14d2fcee" in dependency
          and "must not expose an unrestricted public cure command" in dependency)
    found = {}

    def visit(value):
        if isinstance(value, dict):
            if value.get("id") in ["TAC-05", "CHR-03"] and "dependencies" in value:
                found[value["id"]] = sorted(value["dependencies"])
            for child in value.values():
                visit(child)
        elif isinstance(value, list):
            for child in value:
                visit(child)

    visit(json.loads(payloads["docs/unity/evidence/2026-11-03-rule-map/RULE_MAP.json"]))
    check("Direct map edges remain TAC05 and CHR03 approved dependencies",
          found == {"TAC-05": ["RUL-05", "TAC-01"], "CHR-03": ["CHR-02"]})
    results = json.loads(payloads[PRIOR + "regression/results.json"])
    inventory = text(PRIOR + "regression/inventory.txt").splitlines()
    check("Accepted1509 predecessor inventory is unique ordered and passed", results["status"] == "PASS"
          and results["passed"] == 1509 and results["failed"] == 0 and len(inventory) == len(set(inventory)) == 1509
          and [row["Name"] for row in results["cases"]] == inventory)
    selected = {"sourceRevision": SOURCE, "status": "PROPOSED_SOURCE_SELECTION_NOT_RUNTIME_APPROVAL", "records": [
        {"path": RB + "data/public/class_playtests/warrior.json", "pointer": "/cards/8", "id": card["id"],
         "canonicalSha256": sha(canonical(card)), "value": card},
        {"path": RB + "data/public/class_playtests/warrior.json", "pointer": "/engine/0",
         "canonicalSha256": sha(canonical(warrior["engine"][0])), "value": warrior["engine"][0]},
        {"path": RB + "data/playtest/condition_playtests.json", "pointer": "/conditions/9", "id": fear["id"],
         "canonicalSha256": sha(canonical(fear)), "value": fear},
    ]}
    if args.create_bindings:
        write("SELECTED_SOURCE_BINDINGS.json", selected)
    require(json.loads((PACKET / "SELECTED_SOURCE_BINDINGS.json").read_bytes()) == selected, "Selected record binding differs")
    report = {"status": "PASS", "scope": "SOURCE_AND_CAPABILITY_AUDIT_ONLY", "baseline": BASELINE,
              "sourceRevision": SOURCE, "pinnedFiles": len(entries), "checks": checks,
              "engineChanged": False, "compilation": "NOT_RUN", "runtimeTests": "NOT_RUN", "connectedScenario": "NOT_RUN",
              "predecessorCases": 1509, "contractApproval": "APPROVED_WITH_RECORDED_AMENDMENTS",
              "actualReviewResponse": "226d668a-fd32-51b3-b64c-bbd74b67e64c"}
    write("AUDIT_VALIDATION.json", report)
    print(json.dumps({"status": "PASS", "pinnedFiles": len(entries), "sourceChecks": len(checks),
                      "engineChanged": False, "runtime": "NOT_RUN"}))


if __name__ == "__main__":
    main()
