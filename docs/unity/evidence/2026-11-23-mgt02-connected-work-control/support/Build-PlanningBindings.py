"""Read-only source audit; writes only this planning packet's two JSON reports."""
import hashlib
import json
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
PACKET = Path(__file__).resolve().parents[1]
BASE = "aa75ff96f3d28de8773a6792ebaf9974ee4b164c"
SOURCE_REVISION = "46a4d52728ee6956f0bebcb5d2103ffd5bc67ba4"


def git(*args):
    return subprocess.check_output(["git", "-C", str(ROOT), *args])


def sha(data):
    return hashlib.sha256(data).hexdigest()


def write(name, data):
    (PACKET / name).write_bytes((json.dumps(data, indent=2, ensure_ascii=False) + "\n").encode("utf-8"))


def main():
    assert (ROOT / "engine/AGENTS.md").is_file(), str(ROOT)
    assert git("rev-parse", "HEAD").decode().strip() == BASE, "Audit requires the declared baseline checkout."
    assert not git("diff", "--name-only", "HEAD", "--", "engine"), "Unexpected tracked runtime changes."
    tracked = git("ls-files", "engine/com.decennium.foundation").decode().splitlines()
    cs = [p for p in tracked if p.endswith(".cs")]
    inputs = []

    def pin(path, role, locator="", historical=False):
        data = (ROOT / path).read_bytes()
        blob = git("rev-parse", BASE + ":" + path).decode().strip()
        committed = git("cat-file", "blob", blob)
        row = {"path": path, "role": role, "locator": locator, "baseline": BASE,
               "gitBlob": blob, "gitBlobBytes": len(committed), "gitBlobSha256": sha(committed),
               "workingBytes": len(data), "workingSha256": sha(data),
               "workingBytesEqualGitBlob": data == committed}
        if historical:
            original = git("show", SOURCE_REVISION + ":" + path)
            row.update({"sourceReviewRevision": SOURCE_REVISION,
                        "sourceReviewBlob": git("rev-parse", SOURCE_REVISION + ":" + path).decode().strip(),
                        "sourceReviewSha256": sha(original),
                        "baselineEqualsSourceReview": original == committed})
        inputs.append(row)

    for p in ["CANON_MANIFEST.md", "docs/canon/CANON_MANIFEST.json", "docs/canon/REPOSITORY_PROMOTION.md"]:
        pin(p, "authority registry/promotion boundary; no promotion")
    mechanics = "DescentReviewChanges/ReviewBible/docs/mechanics/"
    sources = {
        "expedition/EXPEDITION_PLAYER_BOOK.md": "FL-01 through FL-05; actual workers, clock, hands and fixed60-second ordinary fill",
        "expedition/EXPEDITION_DIRECTOR_BOOK.md": "actual stock/worker/resource continuity; Director-only source not exposed in host discovery",
        "expedition/EX58_SOURCE_CONTRACTS_CORRECTED.md": "EC-02/EC-03; actual work/resource intervals, identity and custody",
        "MINING_CANDIDATE_GUIDE.md": "finite exposed-node selection, STR/WIS, hurry, source duration and outcome",
        "GATHERING_TOOL_CANDIDATE_GUIDE.md": "actual physical tools and eligible worker/site access",
        "CRAFTING_HARVEST_PLAYTEST.md": "work phases, interruption, research, ingredient aging and deliberate abandonment",
        "CRAFTING_TRADE_REFERENCE.md": "Alchemy qualification; native crafting/research procedures",
        "ALCHEMY_PUBLIC_RECIPE_CARDS.md": "recipe-4 Superior Vital Potion of Black Blood",
        "ALCHEMY_RECIPE_PLAYTEST.md": "exact native ingredient/packaging and quality behavior",
        "CORE_RESOLUTION_PLAYTEST.md": "current source check/modifier/outcome procedure",
        "EQUIPMENT_ACQUISITION_PLAYTEST.md": "actual acquisition, ownership and carrying; no fabricated stock"
    }
    for p, locator in sources.items():
        pin(mechanics + p, "review source, not production promotion", locator, historical=True)
    pin("data/crafting/Decennium_Descent_Crafting_Bible_v4.json", "exact recipe source",
        "/recipes/3, recipe-4; Alchemy5, INT DC8,4 hours, formula required, no assistants", historical=True)
    for p in ["VESSEL_FILLING_RULE_DECISIONS.md", "FORMULA_RESEARCH_RULE_DECISIONS.md", "MINING_RULE_DECISIONS.md",
              "INVENTORY_RULE_DECISIONS.md", "SHARED_WORLD_RULE_DECISIONS.md"]:
        pin("docs/unity/" + p, "adopted bounded prototype policy")
    for p in [
        "2026-11-12-mgt04-connected-recipe4-batch/IMPLEMENTATION_CONTRACT.md",
        "2026-11-12-mgt04-connected-recipe4-batch/SOURCE_API_BINDINGS.json",
        "2026-11-12-mgt04-connected-recipe4-batch/GPT_REVIEW.md",
        "2026-11-12-mgt09-connected-formula-research/IMPLEMENTATION_CONTRACT.md",
        "2026-11-12-mgt09-connected-formula-research/GPT_REVIEW.md",
        "2026-11-15-chr02-shared-rp/GPT_FINAL_REVIEW.md",
        "2026-11-13-int03-strict-restoration/GPT_FINAL_REVIEW.md",
        "2026-11-23-tac01-ordinary-magic/FINAL_ACCEPTANCE.json",
        "2026-11-23-tac01-ordinary-magic/GPT_FINAL_ACCEPTANCE.json",
        "2026-11-23-tac01-ordinary-magic/MAP_ACCEPTANCE_RECONCILIATION.json",
        "2026-11-23-tac01-ordinary-magic/UNRESOLVED_CAPABILITIES.json"]:
        pin("docs/unity/evidence/" + p, "predecessor acceptance/contract; scope retained")
    for p in ["IMPLEMENTATION_STATUS.json", "IMPLEMENTATION_MAP.md", "PRE_UNITY_COMPLETION_CONTRACT.md"]:
        pin("docs/unity/" + p, "approved dependency/completion boundary")
    names = ["OrdinaryMagicProfile.cs", "OrdinaryMagicValidation.cs", "ConsecrationRecords.cs",
             "VerifiedSharedWorldCheckpoint.cs", "ConnectedExpeditionSession.cs", "ConnectedExpeditionView.cs",
             "SharedWorldCommandQueries.cs", "SharedWorldRangedCombat.cs", "SharedMining.cs",
             "SharedFormulaResearch.cs", "SharedConnectedFormulaResearch.cs", "SharedManufacturing.cs",
             "SharedConnectedRecipe4Batch.cs", "TestOnlySharedWorldPolicy.cs", "TestOnlyFillingPolicy.cs",
             "WaterFilling.cs", "Simulation.cs", "SnapshotCodec.cs", "OrdinaryMagicCodec.cs",
             "WorkLedger.cs", "ActiveWorkProgress.cs", "WaterVesselRecords.cs", "MiningRecords.cs",
             "ManufacturingRecords.cs", "ConnectedBloodSpecimen.cs", "HarvestPreservationRecords.cs",
             "ConnectedFormulaResearchCases.cs", "ConnectedRecipe4BatchCases.cs", "MiningCases.cs"]
    for name in names:
        matches = [p for p in cs if p.endswith("/" + name)]
        assert len(matches) == 1, (name, matches)
        pin(matches[0], "existing implementation/test evidence, not independent rule authority")
    pin("engine/tools/Open-ConnectedExpedition.ps1", "existing host console seam")
    inputs.sort(key=lambda x: x["path"])
    write("SOURCE_BINDINGS.json", {"status": "PINNED_PROPOSAL_NOT_ACCEPTED", "baseline": BASE,
          "sourceReviewRevision": SOURCE_REVISION, "pins": inputs, "pinCount": len(inputs),
          "sourceAuthorityChanged": False, "runtimeChanged": False})

    identifiers = ["TEST_ONLY.work-control-v1-", "ConnectedWorkControlProfile", "StartWithConnectedWorkControl"]
    contents = {p: (ROOT / p).read_text(encoding="utf-8-sig") for p in cs}
    hits = {token: [p for p, text in contents.items() if token in text] for token in identifiers}
    assert not any(hits.values()), hits
    simulation = contents[next(p for p in cs if p.endswith("/Simulation.cs"))]
    schemas = [(name, int(value)) for name, value in re.findall(r"public const int (\w*Schema)\s*=\s*(\d+)", simulation)]
    assert max(value for _, value in schemas) == 116, schemas[-5:]
    assert len(identifiers[0]) + 64 <= 96
    status = json.loads((ROOT / "docs/unity/IMPLEMENTATION_STATUS.json").read_text(encoding="utf-8-sig"))
    checks = {"status": "SOURCE_ONLY_CHECKS_PASS", "baseline": BASE,
        "engineTree": git("rev-parse", BASE + ":engine").decode().strip(),
        "trackedCSharpFilesInspectedForIdentifiers": len(cs), "identifierHits": hits,
        "proposedFingerprintLength": len(identifiers[0]) + 64,
        "highestDeclaredSnapshotSchema": max(value for _, value in schemas),
        "newWireSchemaProposed": False, "sourcePinCount": len(inputs),
        "sourceBindingsSha256": sha((PACKET / "SOURCE_BINDINGS.json").read_bytes()),
        "historicalSourceMatches": {p["path"]: p["baselineEqualsSourceReview"] for p in inputs if "baselineEqualsSourceReview" in p},
        "nextModuleAtBaseline": status.get("nextModule"),
        "trackedRuntimeDiff": [], "buildsRun": False, "testsRun": False,
        "genuineNewProfilePathsExecuted": False, "actualGptContractAcceptance": False,
        "sourceAuthorityChanged": False, "unityAuthorized": False}
    write("PLANNING_CHECKS.json", checks)
    print(json.dumps({k: checks[k] for k in ["status", "baseline", "trackedCSharpFilesInspectedForIdentifiers", "proposedFingerprintLength", "highestDeclaredSnapshotSchema", "sourcePinCount", "sourceBindingsSha256"]}))


if __name__ == "__main__":
    main()
