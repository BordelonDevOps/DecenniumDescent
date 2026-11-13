"""Bind the INT-03 strict restoration evidence to exact source, assemblies and regression."""

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
    parser.add_argument("--first", type=Path, required=True)
    parser.add_argument("--counts", type=Path, required=True)
    parser.add_argument("--rejections", type=Path, required=True)
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
    if focus["Name"] != "int03_strict_restore_constructs_fresh_owned_prefix" or not focus["Passed"]:
        raise ValueError("The new fresh owned restore control did not pass.")
    assemblies = {}
    for name in ("Core", "Persistence", "LabModel", "HeadlessTests"):
        dll = f"Decennium.Foundation.{name}.dll"
        relative = f"assemblies/{dll}"
        retain(args.headless / dll, relative)
        assemblies[dll] = artifacts[relative]
    connected = read_json(args.connected / "results.json")
    timings = read_json(args.timing / "results.json")["Profiles"]
    baseline = read_json(packet / "baseline/results.json")["Profiles"]
    initial = read_json(args.first / "results.json")["Profiles"]
    if connected["Status"] != "PASS":
        raise ValueError("The public console continuation did not pass.")
    retain(args.connected / "results.json", "connected/results.json")
    retain(args.timing / "results.json", "performance/results.json")
    retain(args.first / "results.json", "first-performance/results.json")
    replay_counts = {}
    for mode in ("Reference", "Candidate"):
        diagnosis = read_json(args.counts / mode / "results.json")
        if diagnosis["Status"] != "PASS":
            raise ValueError(f"Instrumentation failed: {mode}")
        replay_counts[mode] = diagnosis["Profiles"]
        retain(args.counts / mode / "results.json", f"counts/{mode}/results.json")
    rejections = read_json(args.rejections / "results.json")
    if rejections["Status"] != "PASS":
        raise ValueError("Restore and backup controls failed.")
    retain(args.rejections / "results.json", "rejections/results.json")
    for profile, count in (("Default", 223), ("FishingTrap", 242)):
        result = connected["Profiles"][profile]
        timing = timings[profile]
        reference = packet.parent / "2026-11-13-int03-active-work-performance/connected" / profile / "responses.jsonl"
        if (result["TranscriptSha256"] != digest((args.connected / profile / "responses.jsonl").read_bytes())
                or result["TranscriptSha256"] != digest(reference.read_bytes())):
            raise ValueError(f"Public transcript comparison identities differ: {profile}")
        old = replay_counts["Reference"][profile]
        new = replay_counts["Candidate"][profile]
        if (old["Outer"] != 104 or new["Outer"] != old["Outer"] or new["Nested"] != old["Nested"]
                or old["DedicatedSeal"] == 0 or new["DedicatedSeal"] != 0 or old["Sha256"] != new["Sha256"]):
            raise ValueError(f"The full validation or separate sealing count differs: {profile}")
        if (result["Committed"] != count or timing["Samples"] < 30 or timing["PublicMs"]["P95"] > 3950
                or timing["Sha256"] != baseline[profile]["Sha256"] or initial[profile]["Sha256"] != timing["Sha256"]):
            raise ValueError(f"Connected or performance acceptance failed: {profile}")
        for name in ("samples.csv", "probes.csv", "round-trip.ddsave", "control-r103.ddsave",
                     f"control-r{count}.ddsave"):
            retain(args.timing / profile / name, f"performance/{profile}/{name}")
            retain(args.first / profile / name, f"first-performance/{profile}/{name}")
        for name in ("altered.ddsave", "later-receipt.ddsave", "malformed.ddsave", "live-before.ddsave",
                     "live-after-malformed.ddsave", "live-after-wrong-profile.ddsave", "live-after-later-receipt.ddsave",
                     "live-after-altered.ddsave", "recovery.ddsave"):
            retain(args.rejections / profile / name, f"rejections/{profile}/{name}")
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
        prior = lines(packet.parent / "2026-11-13-int03-active-work-performance/regression/inventory.txt")
        if len(names) != 1489 or len(set(names)) != 1489 or [name for name in names if name != focus["Name"]] != prior:
            raise ValueError("The restore inventory differs from its 1,488 accepted predecessors.")
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

    binding = {**identity, "sourceApiReview": "7eb9c90e-b182-464e-863f-01561c9d5cf9", "focusedCase": focus,
               "compiledSourceCounts": {"headless": len(headless["sourceHashes"]),
                                        "standalone": len(standalone["sourceHashes"]),
                                        "staticInputs": len(static["sourceHashes"])},
               "regressionCases": regression_cases, "profiles": connected["Profiles"],
               "artifacts": dict(sorted(artifacts.items()))}
    (packet / "BINDINGS.json").write_text(json.dumps(binding, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
