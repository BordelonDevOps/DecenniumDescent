"""Verify and retain TAC-07 connected Cleric repertoire exact source, focused evidence and full regression."""

import argparse
import hashlib
import io
import json
from pathlib import Path
import shutil
import subprocess
import zipfile


def read_json(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def lines(path):
    return path.read_text(encoding="utf-8-sig").splitlines()


def digest(payload):
    return hashlib.sha256(payload).hexdigest()


def require(test, message):
    if not test:
        raise ValueError(message)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("implementation")
    for name in ("headless", "standalone", "static", "public", "compatibility", "direct", "additional", "run"):
        parser.add_argument(f"--{name}", type=Path, required=True)
    parser.add_argument("--complete", action="store_true")
    args = parser.parse_args()
    packet = Path(__file__).resolve().parent
    previous = packet.parent / "2026-11-15-chr02-shared-rp"
    archive_bytes = subprocess.check_output(["git", "archive", "--format=zip", args.implementation, "engine"])
    archive = zipfile.ZipFile(io.BytesIO(archive_bytes))
    artifacts = {}

    def retain(source, relative):
        target = packet / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
        payload = target.read_bytes()
        artifacts[relative] = {"bytes": len(payload), "sha256": digest(payload)}

    def retain_compilation(source, relative):
        report = read_json(source)
        require(report["status"] == "PASS", f"Failed report: {source}")
        for item in report["sourceHashes"]:
            name = "engine/" + item["path"].replace("\\", "/")
            require(digest(archive.read(name)) == item["sha256"].lower(), f"Wrong source hash: {name}")
        retain(source, relative)
        return report

    source_bindings = read_json(packet / "SOURCE_API_BINDINGS.json")
    for source in source_bindings["sources"]:
        blob = subprocess.check_output(
            ["git", "rev-parse", source.get("revision", source_bindings["sourceRevision"]) + ":" + source["path"]], text=True).strip()
        require(blob == source["gitBlob"], f"Wrong pinned source blob: {source['path']}")
        payload = subprocess.check_output(["git", "cat-file", "blob", blob])
        require(digest(payload) == source["sha256"], f"Wrong pinned source hash: {source['path']}")
    support_sources = {}
    for name in ("docs/unity/evidence/2026-11-12-mgt06-connected-trap/Run-ExactTrapShard.ps1",):
        payload = subprocess.check_output(["git", "show", args.implementation + ":" + name])
        require(digest(Path(name).read_bytes()) == digest(payload), "Shared worker source differs from the implementation commit.")
        relative = "support/" + Path(name).name
        retain(Path(name), relative)
        support_sources[name] = {"revision": args.implementation, "sha256": digest(payload), "retained": relative}

    headless = retain_compilation(args.headless / "results.json", "compile/headless.json")
    retain_compilation(args.standalone, "compile/standalone.json")
    retain_compilation(args.static, "compile/static.json")
    focused = [headless["cases"][0]]
    focus_names = {"tac07_cleric_initial_repertoire_source_and_detached_earned_contract", "tac07_cleric_repertoire_connected_payment_restore_and_denials", "tac07_cleric_repertoire_forgery_legacy_and_authority_boundaries"}
    require({row["Name"] for row in focused} == {"tac07_cleric_repertoire_connected_payment_restore_and_denials"} and all(row["Passed"] and not row["Error"] for row in focused),
            "The exact focused case did not pass.")
    for file in sorted((args.headless / "saves").rglob("*.ddsave")):
        retain(file, f"focused/{file.name}")
    assemblies = {}
    for name in ("Core", "Persistence", "LabModel", "HeadlessTests"):
        dll = f"Decennium.Foundation.{name}.dll"
        relative = "assemblies/" + dll
        retain(args.headless / dll, relative)
        assemblies[dll] = artifacts[relative]
    public_assemblies = {}
    for name in ("Core", "Persistence", "LabModel"):
        dll = f"Decennium.Foundation.{name}.dll"
        relative = "assemblies-public/" + dll
        retain(args.standalone.parent / dll, relative)
        public_assemblies[dll] = artifacts[relative]

    public = read_json(args.public / "results.json")
    compatibility = read_json(args.compatibility / "results.json")
    direct = read_json(args.direct / "results.json")
    additional = read_json(args.additional / "results.json")
    require(additional["Status"] == "PASS" and len(additional["BoundaryControls"]) == 7 and additional["LegacyProjectionIdentical"],
            "Additional shared-boundary/legacy controls are incomplete.")
    require(public["Status"] == compatibility["Status"] == direct["Status"] == "PASS", "Public, compatibility or typed replay failed.")
    selected = read_json(packet / "SELECTED_SPELL_BINDINGS.json")
    runtime = read_json(args.additional / "runtime-source-bindings.json")
    require(len(runtime) == 6 and digest((args.additional / "runtime-source-bindings.json").read_bytes()) == additional["RuntimeSourceSha256"],
            "Runtime source registry missing or changed.")
    for row in selected["selected"]:
        actual = next(item for item in runtime if item["Id"] == row["id"])
        require(actual["SourceRevision"] == selected["sourceRevision"] and actual["WholeCardSha256"] == row["wholeCardSha256"]
                and actual["ProcedureSha256"] == row["procedureSha256"] and actual["OriginalRecordSha256"] == row["originalCatalogRecordSha256"]
                and actual["AuthoredReviewSha256"] == row["authoredReviewEntrySha256"] and actual["WholeCardPointer"] == row["wholeCardPointer"]
                and actual["ProcedurePointer"] == row["procedurePointer"] and actual["SourceStatus"] == row["status"]
                and actual["AuthoredStatus"] == row["authoredStatus"] and not actual["CastingSupported"]
                and actual["AdditionalRpCost"] == row["additionalRpCost"], "Runtime source metadata differs.")
        access = {item["ClassName"]: {"rank": item["Rank"], "minimumClassLevel": item["MinimumClassLevel"],
                  "school": item["School"], "baseRpCost": item["BaseRpCost"]} for item in actual["ClassAccess"]}
        require(access == row["allClassAccess"], "Runtime per-class access differs.")
        require(actual["Placements"] == [{"School": item["school"], "Rank": item["level"], "Summary": item["summary"]}
                for item in row["allSourcePlacements"]], "Runtime school placements differ.")
    for point, state in public["States"].items():
        known = state["KnownSpells"]
        require(state["Wire"] == 106 and len(known) == 5
                and sorted(item["SpellId"] for item in known) == sorted(item["id"] for item in selected["selected"] if item["id"] != "detect-magic")
                and all(item["Origin"] == "InitialClassRepertoire" and item["AcquiredRevision"] == 0 for item in known),
                "Connected ownership/provenance differs at " + point)
    for control in additional["BoundaryControls"]:
        require(control["Result"]["Outcome"] == "Rejected" and not control["Query"]["Admissible"]
                and control["Result"]["Code"] == control["Query"]["Code"]
                and digest((args.additional / "before.ddsave").read_bytes()) == control["UnchangedSha256"]
                    == digest((args.additional / ("after-" + control["Kind"] + "-" + control["Spell"] + ".ddsave")).read_bytes()),
                "Shared engine query/execution denial differs.")

    original = [json.loads(line) for line in lines(packet / "walkthrough.jsonl")]
    for mode in ("Restored", "Uninterrupted"):
        actual = [json.loads(line) for line in lines(args.public / mode / "inputs.jsonl")]
        require(actual == [row for row in original if mode == "Restored" or row["op"] != "load"],
                "Retained console inputs differ from the complete authored input stream.")
        require(public["Runs"][mode]["Checkpoints"] == public["ReceiptCheckpoints"], "Console and receipt checkpoint sets differ.")
        for mark, sha in public["ReceiptCheckpoints"].items():
            require(digest((args.public / mode / mark).read_bytes()) == sha
                    == digest((args.public / ("receipt-" + mark)).read_bytes()), "Observed checkpoint digest differs.")
    require({row["Wire"] for row in compatibility["Cases"]} == set(range(95, 106)), "An authentic supported wire is missing.")
    for row in compatibility["Cases"]:
        require(row["SourceSha256"] == row["RoundtripSha256"] == row["ContinuedSha256"] and row["Commands"] > 0,
                "Authentic continued state differs.")
        require(digest((packet.parent / row["Source"]).read_bytes()) == row["SourceSha256"]
                and digest((packet.parent / row["Earlier"]).read_bytes()) == row["EarlierSha256"], "Authentic input binding differs.")
    public_branches = {"walkthrough": {"DirectCheckpoints": public["ReceiptCheckpoints"]}}
    for name, branch in public_branches.items():
        require(branch["DirectCheckpoints"] == direct["Branches"][name]["DirectCheckpoints"], "Typed and receipt checkpoint sets differ.")
        details = direct["Branches"][name]
        direct_folder = args.direct / name
        console = args.public / "Restored"
        requests = read_json(direct_folder / "requests.json")
        require(len(requests) == details["Inputs"]
                and digest((direct_folder / "requests.json").read_bytes()) == details["RequestsSha256"]
                and digest((console / "inputs.jsonl").read_bytes()) == details["InputSha256"]
                and digest((console / "responses.jsonl").read_bytes()) == details["ReferenceResponsesSha256"], "Typed request stream identity differs.")
        for row in requests:
            if "BeforeSnapshot" in row:
                require(digest((direct_folder / row["BeforeSnapshot"]).read_bytes()) == row["UnchangedSha256"]
                        == digest((direct_folder / row["AfterSnapshot"]).read_bytes()), "Denied/retried state pair differs.")
        for mark, sha in details["DirectCheckpoints"].items():
            require(digest((direct_folder / mark).read_bytes()) == sha == digest((console / mark).read_bytes()), "Typed checkpoint file differs.")
    for folder, label in ((args.public, "public"), (args.compatibility, "compatibility"), (args.direct, "direct"), (args.additional, "additional")):
        retained = set()
        if label == "direct":
            for name in direct["Branches"]:
                rows = read_json(folder / name / "requests.json")
                for row in rows:
                    for field in ("BeforeSnapshot", "AfterSnapshot"):
                        if field in row: retained.add(name + "/" + row[field])
                for mark in direct["Branches"][name]["DirectCheckpoints"]: retained.add(name + "/" + mark)
        for file in sorted(folder.rglob("*")):
            relative = file.relative_to(folder).as_posix()
            if file.is_file() and not file.name.endswith(".bak") and (label != "direct" or file.suffix == ".json" or relative in retained):
                retain(file, label + "/" + relative)

    run = args.run
    focused = []
    for group in ("shardA", "shardB", "shardC"):
        with (run / (group + ".jsonl")).open(encoding="utf-8-sig") as journal:
            row = json.loads(journal.readline())
        require(row["Name"] in focus_names and row["Passed"] and not row["Error"], "Exact new-case execution did not pass.")
        focused.append(row)
        for file in sorted((run / "saves" / row["Name"]).rglob("*.ddsave")):
            retain(file, "focused/" + row["Name"] + "/" + file.name)
    require({row["Name"] for row in focused} == focus_names, "The three new cases did not all execute.")
    names = lines(run / "all-names.txt")
    prior_names = lines(previous / "regression/inventory.txt")
    require(len(names) == len(set(names)) == 1509 and [name for name in names if name not in focus_names] == prior_names,
            "The exact inventory must preserve all 1,506 predecessors in order.")
    launch = read_json(run / "launch.json")
    expected = {name: value["sha256"] for name, value in assemblies.items()}
    require(launch["assemblies"] == expected and launch["inventorySha256"] == digest((run / "all-names.txt").read_bytes()),
            "Run launch differs from accepted bytes or exact inventory.")
    process_rows = {entry["group"]: entry for entry in read_json(run / "processes.json")}
    results = {}
    assigned_union = []
    modules = None
    group_names = ["shard" + suffix for suffix in "ABCDEF"]
    for group in group_names:
        start = read_json(run / f"{group}.started.json")
        assignment = run / f"{group}-names.txt"
        assignment_sha = digest(assignment.read_bytes())
        assigned = lines(assignment)
        assigned_union.extend(assigned)
        require(start["runId"] == launch["runId"] and start["group"] == group
                and start["pid"] == process_rows[group]["pid"] and len(assigned) == process_rows[group]["cases"]
                and start["inventorySha256"] == launch["inventorySha256"]
                and start["assignmentSha256"] == assignment_sha == launch["assignments"][group]
                and {name: item["sha256"] for name, item in start["assemblies"].items()} == expected,
                f"Invalid worker start: {group}")
        actual_modules = {name: entry["moduleId"] for name, entry in start["assemblies"].items()}
        require(modules is None or actual_modules == modules, f"Inconsistent loaded modules: {group}")
        modules = actual_modules
        for file in (assignment, run / f"{group}.started.json"):
            retain(file, "regression/" + file.name)
        if not args.complete:
            continue
        completed = read_json(run / f"{group}.execution.json")
        journal_file = run / f"{group}.jsonl"
        journal = [json.loads(line) for line in lines(journal_file)]
        require(all(completed.get(key) == value for key, value in start.items())
                and completed["journalSha256"] == digest(journal_file.read_bytes())
                and completed["cases"] == len(assigned) and lines(run / f"{group}.done") == ["DONE"]
                and [row["Name"] for row in journal] == assigned,
                f"Invalid completed execution: {group}")
        for row in journal:
            require(row["Passed"] and not row["Error"] and row["Name"] not in results, f"Failed or repeated case: {row}")
            results[row["Name"]] = row
        for suffix in (".execution.json", ".jsonl", ".done"):
            retain(run / (group + suffix), "regression/" + group + suffix)
    require(sorted(assigned_union) == sorted(names), "Assignments are not the complete exact inventory.")
    for short_name, module in direct["Assemblies"].items():
        dll = f"Decennium.Foundation.{short_name}.dll"
        require(module["sha256"] == public_assemblies[dll]["sha256"], "Typed verifier used a different standalone assembly.")

    retain(run / "launch.json", "regression/launch.json")
    retain(run / "processes.json", "regression/processes.json")
    retain(run / "all-names.txt", "regression/inventory.txt")
    identity = {"implementationCommit": args.implementation, "sourceArchiveSha256": digest(archive_bytes),
                "executedAssemblies": assemblies, "moduleIds": modules, "runId": launch["runId"],
                "standaloneAssemblies": public_assemblies, "standaloneLoadedModules": direct["Assemblies"]}
    focus_report = packet / "focused/results.json"
    focus_report.parent.mkdir(parents=True, exist_ok=True)
    focus_report.write_text(json.dumps({"status": "PASS", **identity, "cases": focused,
        "executionOrigin": "First completed case in each immutable exact-run worker shardA/shardB/shardC; not a new invocation"}, indent=2) + "\n", encoding="utf-8")
    artifacts["focused/results.json"] = {"bytes": focus_report.stat().st_size, "sha256": digest(focus_report.read_bytes())}
    if args.complete:
        require(set(results) == set(names) and all(results[row["Name"]] == row for row in focused),
                "The completed run must include the passing focused result and all predecessors.")
        report = {"status": "PASS", **identity, "testsDiscovered": len(names), "passed": len(names), "failed": 0,
                  "cases": [results[name] for name in names], "unity": "NOT RUN"}
        result = packet / "regression/results.json"
        result.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
        artifacts["regression/results.json"] = {"bytes": result.stat().st_size, "sha256": digest(result.read_bytes())}
    for pattern in ("*.ps1", "*.py", "*.jsonl", "*.md", "SOURCE_API_BINDINGS.json", "SELECTED_SPELL_BINDINGS.json", "CONTRACT_VALIDATION.json", "development/*.json"):
        for file in sorted(packet.glob(pattern)):
            relative = file.relative_to(packet).as_posix()
            artifacts[relative] = {"bytes": file.stat().st_size, "sha256": digest(file.read_bytes())}
    binding = {**identity, "sourceBindings": source_bindings, "contractReview": "f17c9e06-7464-56da-8184-a5723befea81", "newRegisteredCases": sorted(focus_names),
               "focusedCases": focused, "regressionCases": len(results) if args.complete else None,
               "public": {name: branch["DirectCheckpoints"] for name, branch in public_branches.items()}, "compatibility": compatibility,
               "additionalControls": additional, "supportSources": support_sources, "artifacts": dict(sorted(artifacts.items()))}
    (packet / "BINDINGS.json").write_text(json.dumps(binding, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
