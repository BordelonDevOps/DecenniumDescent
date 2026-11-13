"""Bind the EXP-05 gameplay evidence to exact source, assemblies and regression."""

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
    if focus["Name"] != "exp05_session_exact_local_traversal_restore" or not focus["Passed"]:
        raise ValueError("The new traversal restore control did not pass.")
    assemblies = {}
    for name in ("Core", "Persistence", "LabModel", "HeadlessTests"):
        dll = f"Decennium.Foundation.{name}.dll"
        relative = f"assemblies/{dll}"
        retain(args.headless / dll, relative)
        assemblies[dll] = artifacts[relative]
    connected = read_json(args.connected / "results.json")
    if connected["Status"] != "PASS" or connected["CSharpCommittedActions"] != connected["FinalRevision"]:
        raise ValueError("The public C# and console walkthrough did not pass.")
    for name in ("results.json", "walkthrough.jsonl", "responses.jsonl", "partial-edge.ddsave", "arrived.ddsave",
                 "away-from-site.ddsave", "travel-continued.ddsave", "authentic-observation.ddsave",
                 "replay/walkthrough.jsonl", "replay/responses.jsonl", "replay/partial-edge.ddsave",
                 "replay/travel-continued.ddsave", "csharp/partial-edge.ddsave", "csharp/travel-continued.ddsave"):
        retain(args.connected / name, "connected/" + name)
    for name in ("travel-continued.ddsave", "replay/travel-continued.ddsave", "csharp/travel-continued.ddsave"):
        if artifacts["connected/" + name]["sha256"] != connected["FinalSha256"]:
            raise ValueError(f"Public continuation differs: {name}")
    for name in ("partial-edge.ddsave", "replay/partial-edge.ddsave", "csharp/partial-edge.ddsave"):
        if artifacts["connected/" + name]["sha256"] != connected["PendingSha256"]:
            raise ValueError(f"Pending edge differs: {name}")
    if artifacts["connected/authentic-observation.ddsave"]["sha256"] != connected["AuthenticSha256"]:
        raise ValueError("The accepted predecessor changed.")

    identity = {"implementationCommit": args.implementation, "sourceArchiveSha256": digest(archive_bytes),
                "executedAssemblies": assemblies}
    regression_cases = None
    if args.regression:
        run = args.regression
        names = lines(run / "all-names.txt")
        prior = lines(packet.parent / "2026-11-12-exp04-public-observation/regression/inventory.txt")
        if len(names) != 1485 or len(set(names)) != 1485 or [name for name in names if name != focus["Name"]] != prior:
            raise ValueError("The traversal inventory differs from its 1,484 accepted predecessors.")
        results = {}
        for label in ("shard" + letter for letter in "ABCDEF"):
            assigned = lines(run / f"{label}-names.txt")
            journal = [json.loads(line) for line in lines(run / f"{label}.jsonl")]
            if lines(run / f"{label}.done") != ["DONE"] or assigned != [row["Name"] for row in journal]:
                raise ValueError(f"Incomplete or reordered journal: {label}")
            for row in journal:
                if row["Name"] in results or not row["Passed"] or row["Error"]:
                    raise ValueError(f"Repeated or failed result: {row}")
                results[row["Name"]] = row
            for suffix in ("-names.txt", ".done", ".jsonl"):
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

    binding = {**identity, "sourceApiReview": "02a9ed1a-d334-43a3-acdc-2ac91a4bb1f4", "focusedCase": focus,
               "compiledSourceCounts": {"headless": len(headless["sourceHashes"]),
                                        "standalone": len(standalone["sourceHashes"]),
                                        "staticInputs": len(static["sourceHashes"])},
               "regressionCases": regression_cases, "acceptedBaselineSha256": connected["AuthenticSha256"],
               "pendingSha256": connected["PendingSha256"], "finalSha256": connected["FinalSha256"],
               "artifacts": dict(sorted(artifacts.items()))}
    (packet / "BINDINGS.json").write_text(json.dumps(binding, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
