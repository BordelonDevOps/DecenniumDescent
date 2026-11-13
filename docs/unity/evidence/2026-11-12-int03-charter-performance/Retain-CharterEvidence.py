"""Bind the INT-03 charter performance evidence to exact source, assemblies and regression."""

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


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("implementation")
    parser.add_argument("--headless", type=Path, required=True)
    parser.add_argument("--standalone", type=Path, required=True)
    parser.add_argument("--static", type=Path, required=True)
    parser.add_argument("--connected", type=Path, required=True)
    parser.add_argument("--timing", type=Path, required=True)
    parser.add_argument("--regression", type=Path)
    args = parser.parse_args()
    packet = Path(__file__).resolve().parent
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
        if report["status"] != "PASS":
            raise ValueError(f"Failed validation: {source}")
        for item in report["sourceHashes"]:
            name = "engine/" + item["path"].replace("\\", "/")
            if digest(archive.read(name)) != item["sha256"].lower():
                raise ValueError(f"Wrong source hash: {name}")
        retain(source, relative)
        return report

    headless = retain_compilation(args.headless / "results.json", "compile/headless.json")
    standalone = retain_compilation(args.standalone, "compile/standalone.json")
    static = retain_compilation(args.static, "compile/static.json")
    focus = headless["cases"][0]
    if focus["Name"] != "int03_verified_charter_passage_ownership_and_cutoff" or not focus["Passed"]:
        raise ValueError("The new charter ownership and cutoff control did not pass.")
    assemblies = {}
    for name in ("Core", "Persistence", "LabModel", "HeadlessTests"):
        dll = f"Decennium.Foundation.{name}.dll"
        relative = f"assemblies/{dll}"
        retain(args.headless / dll, relative)
        assemblies[dll] = artifacts[relative]
    connected = read_json(args.connected / "results.json")
    timings = read_json(args.timing / "results.json")
    baseline = read_json(packet / "baseline/results.json")
    if connected["Status"] != "PASS":
        raise ValueError("The public console continuation did not pass.")
    comparison = read_json(args.connected / "transcript-equivalence.json")
    if comparison["Status"] != "PASS" or comparison["IgnoredFields"]:
        raise ValueError("The full public response comparison did not pass.")
    retain(args.connected / "results.json", "connected/results.json")
    retain(args.connected / "transcript-equivalence.json", "connected/transcript-equivalence.json")
    retain(args.timing / "results.json", "performance/results.json")
    for profile, count in (("Default", 223), ("FishingTrap", 242)):
        result = connected["Profiles"][profile]
        timing = timings[profile]
        transcript = comparison["Profiles"][profile]
        if (transcript["comparedRows"] != result["Inputs"]
                or transcript["actualSha256"] != digest((args.connected / profile / "responses.jsonl").read_bytes())
                or transcript["referenceSha256"] != digest((packet.parent / transcript["reference"]).read_bytes())):
            raise ValueError(f"Public transcript comparison identities differ: {profile}")
        if (result["Committed"] != count or timing["Samples"] < 30 or timing["PublicMs"]["P95"] > 150
                or timing["LiveResultSha256"] != timing["ResultSha256"]
                or timing["ResultSha256"] != baseline[profile]["ResultSha256"]):
            raise ValueError(f"Connected or performance acceptance failed: {profile}")
        for name in ("samples.csv", "prefix.csv", "pre-submit.ddsave", "post-submit.ddsave", "live-submit.ddsave"):
            retain(args.timing / profile / name, f"performance/{profile}/{name}")
        for name, expected in result["Checkpoints"].items():
            filename = name + ".ddsave"
            retain(args.connected / profile / filename, f"connected/{profile}/{filename}")
            if artifacts[f"connected/{profile}/{filename}"]["sha256"] != expected:
                raise ValueError(f"Connected checkpoint changed: {profile} {name}")
        for name in ("responses.jsonl", "authentic.ddsave"):
            retain(args.connected / profile / name, f"connected/{profile}/{name}")
    for name in ("before-reject.ddsave", "after-reject.ddsave"):
        retain(args.connected / "FishingTrap" / name, "connected/FishingTrap/" + name)
    if artifacts["connected/FishingTrap/before-reject.ddsave"] != artifacts["connected/FishingTrap/after-reject.ddsave"]:
        raise ValueError("Atomic forged restore bytes differ.")

    identity = {"implementationCommit": args.implementation, "sourceArchiveSha256": digest(archive_bytes),
                "executedAssemblies": assemblies}
    regression_cases = None
    if args.regression:
        run = args.regression
        launch = read_json(run / "launch.json")
        expected_digests = {name: item["sha256"] for name, item in assemblies.items()}
        if launch["assemblies"] != expected_digests or launch["inventorySha256"] != digest((run / "all-names.txt").read_bytes()):
            raise ValueError("The run launch does not match the retained assemblies or inventory.")
        retain(run / "launch.json", "regression/launch.json")
        processes = {row["group"]: row for row in read_json(run / "processes.json")}
        retain(run / "processes.json", "regression/processes.json")
        names = lines(run / "all-names.txt")
        prior = lines(packet.parent / "2026-11-12-mgt06-connected-trap/regression/inventory.txt")
        if len(names) != 1487 or len(set(names)) != 1487 or [name for name in names if name != focus["Name"]] != prior:
            raise ValueError("The charter inventory differs from its 1,486 accepted predecessors.")
        results = {}
        for label in ("shard" + letter for letter in "ABCDEF"):
            assigned = lines(run / f"{label}-names.txt")
            journal = [json.loads(line) for line in lines(run / f"{label}.jsonl")]
            started = read_json(run / f"{label}.started.json")
            execution = read_json(run / f"{label}.execution.json")
            recorded = {name: item["sha256"] for name, item in started["assemblies"].items()}
            assignment_sha = digest((run / f"{label}-names.txt").read_bytes())
            if (recorded != expected_digests or not all(item["moduleId"] for item in started["assemblies"].values())
                    or started["runId"] != launch["runId"] or started["group"] != label
                    or started["pid"] != processes[label]["pid"] or processes[label]["cases"] != len(assigned)
                    or started["inventorySha256"] != launch["inventorySha256"]
                    or started["assignmentSha256"] != assignment_sha or launch["assignments"][label] != assignment_sha
                    or any(execution.get(key) != value for key, value in started.items())
                    or not execution["completedUtc"] or execution["cases"] != len(assigned)
                    or execution["journalSha256"] != digest((run / f"{label}.jsonl").read_bytes())):
                raise ValueError(f"The journal is not bound to the recorded launch and execution: {label}")
            if lines(run / f"{label}.done") != ["DONE"] or assigned != [row["Name"] for row in journal]:
                raise ValueError(f"Incomplete or reordered journal: {label}")
            for row in journal:
                if row["Name"] in results or not row["Passed"] or row["Error"]:
                    raise ValueError(f"Repeated or failed result: {row}")
                results[row["Name"]] = row
            for suffix in ("-names.txt", ".done", ".jsonl", ".started.json", ".execution.json"):
                retain(run / (label + suffix), "regression/" + label + suffix)
        if set(names) != results.keys() or results[focus["Name"]] != focus:
            raise ValueError("Completed journals differ from the exact inventory or focused result.")
        retain(run / "all-names.txt", "regression/inventory.txt")
        report = {"status": "PASS", **identity, "testsDiscovered": len(names), "passed": len(names),
                  "failed": 0, "cases": [results[name] for name in names], "unity": "NOT RUN"}
        result = packet / "regression/results.json"
        result.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
        payload = result.read_bytes()
        artifacts["regression/results.json"] = {"bytes": len(payload), "sha256": digest(payload)}
        regression_cases = len(names)

    binding = {**identity, "sourceApiReview": "76a47a76-0d85-4e74-82d0-98a6c2baaa25", "focusedCase": focus,
               "compiledSourceCounts": {"headless": len(headless["sourceHashes"]),
                                        "standalone": len(standalone["sourceHashes"]),
                                        "staticInputs": len(static["sourceHashes"])},
               "regressionCases": regression_cases, "profiles": connected["Profiles"],
               "artifacts": dict(sorted(artifacts.items()))}
    (packet / "BINDINGS.json").write_text(json.dumps(binding, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
