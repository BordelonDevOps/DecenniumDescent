"""Verify and retain MGT-03 Short Rest exact source, focused evidence and full regression."""

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
    for name in ("headless", "standalone", "static", "public", "connected", "prior", "run"):
        parser.add_argument(f"--{name}", type=Path, required=True)
    parser.add_argument("--complete", action="store_true")
    args = parser.parse_args()
    packet = Path(__file__).resolve().parent
    previous = packet.parent / "2026-11-14-tac06-temporary-hp"
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

    source_bindings = read_json(packet / "SOURCE_BINDINGS.json")
    for source in source_bindings["sources"]:
        blob = subprocess.check_output(
            ["git", "rev-parse", source_bindings["sourceCommit"] + ":" + source["path"]], text=True).strip()
        require(blob == source["gitBlob"], f"Wrong pinned source blob: {source['path']}")
        payload = subprocess.check_output(["git", "cat-file", "blob", blob])
        require(digest(payload) == source["sha256"], f"Wrong pinned source hash: {source['path']}")

    headless = retain_compilation(args.headless / "results.json", "compile/headless.json")
    retain_compilation(args.standalone, "compile/standalone.json")
    retain_compilation(args.static, "compile/static.json")
    focused = [headless["cases"][0]]
    focus_names = {"mgt03_connected_short_rest_deadlines_cadence_interruption_and_restore"}
    require({row["Name"] for row in focused} == focus_names and all(row["Passed"] and not row["Error"] for row in focused),
            "The exact focused case did not pass.")
    for file in sorted((args.headless / "saves").rglob("*.ddsave")):
        retain(file, f"focused/{file.name}")
    assemblies = {}
    for name in ("Core", "Persistence", "LabModel", "HeadlessTests"):
        dll = f"Decennium.Foundation.{name}.dll"
        relative = "assemblies/" + dll
        retain(args.headless / dll, relative)
        assemblies[dll] = artifacts[relative]

    public = read_json(args.public / "results.json")
    connected = read_json(args.connected / "results.json")
    require(public["Status"] == connected["Status"] == read_json(args.prior / "results.json")["Status"] == "PASS", "Connected witnesses did not pass.")
    for folder, label in ((args.public, "public"), (args.connected, "connected"), (args.prior, "prior")):
        for file in sorted(folder.rglob("*")):
            if file.is_file() and not file.name.endswith(".bak"):
                retain(file, label + "/" + file.relative_to(folder).as_posix())

    run = args.run
    names = lines(run / "all-names.txt")
    prior_names = lines(previous / "regression/inventory.txt")
    require(len(names) == len(set(names)) == 1499 and [name for name in names if name not in focus_names] == prior_names,
            "The exact inventory must preserve all 1,498 predecessors in order.")
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
    retain(run / "launch.json", "regression/launch.json")
    retain(run / "processes.json", "regression/processes.json")
    retain(run / "all-names.txt", "regression/inventory.txt")
    identity = {"implementationCommit": args.implementation, "sourceArchiveSha256": digest(archive_bytes),
                "executedAssemblies": assemblies, "moduleIds": modules, "runId": launch["runId"]}
    if args.complete:
        require(set(results) == set(names) and all(results[row["Name"]] == row for row in focused),
                "The completed run must include the passing focused result and all predecessors.")
        report = {"status": "PASS", **identity, "testsDiscovered": len(names), "passed": len(names), "failed": 0,
                  "cases": [results[name] for name in names], "unity": "NOT RUN"}
        result = packet / "regression/results.json"
        result.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
        artifacts["regression/results.json"] = {"bytes": result.stat().st_size, "sha256": digest(result.read_bytes())}
    binding = {**identity, "sourceApiReview": "521f7485-a1fc-5771-bdda-eff382d7367d",
               "focusedCases": focused, "regressionCases": len(results) if args.complete else None,
               "public": {name: branch["DirectCheckpoints"] for name, branch in public["Branches"].items()}, "profiles": connected["Profiles"], "artifacts": dict(sorted(artifacts.items()))}
    (packet / "BINDINGS.json").write_text(json.dumps(binding, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
