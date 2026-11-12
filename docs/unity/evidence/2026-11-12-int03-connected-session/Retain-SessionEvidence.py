"""Bind and retain the tested session, console transcript and exact regression."""

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


def digest(data):
    return hashlib.sha256(data).hexdigest()


def file_binding(path):
    data = path.read_bytes()
    return {"bytes": len(data), "sha256": digest(data)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("implementation")
    parser.add_argument("--headless", type=Path, required=True)
    parser.add_argument("--standalone", type=Path, required=True)
    parser.add_argument("--static", type=Path, required=True)
    parser.add_argument("--connected", type=Path, required=True)
    parser.add_argument("--console", type=Path, required=True)
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
        artifacts[relative] = file_binding(target)

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
    assemblies = {}
    for name in ("Core", "Persistence", "LabModel", "HeadlessTests"):
        filename = f"Decennium.Foundation.{name}.dll"
        relative = f"assemblies/{filename}"
        retain(args.headless / filename, relative)
        assemblies[filename] = artifacts[relative]

    connected = read_json(args.connected / "results.json")
    console = read_json(args.console / "results.json")
    if (connected["WarmSamplesPerInput"] != 30 or console["Status"] != "PASS"
            or connected["RepeatedFinalSha256"] != console["FinalSha256"]
            or connected["RestoredFinalSha256"] != console["FinalSha256"]
            or connected["PendingSha256"] != console["PendingSha256"]):
        raise ValueError("The measured and console continuations must match.")
    for name in ("results.json", "samples.csv", "timeline.json"):
        retain(args.connected / name, f"connected/{name}")
    for name in ("initial.ddsave", "checkpoint-15.ddsave", "checkpoint-16.ddsave", "checkpoint-28.ddsave",
                 "checkpoint-30.ddsave", "checkpoint-84.ddsave", "checkpoint-97.ddsave", "checkpoint-105.ddsave",
                 "checkpoint-106.ddsave", "checkpoint-107.ddsave", "checkpoint-113.ddsave", "restored-pending.ddsave", "forged-history.ddsave",
                 "checkpoint-114.ddsave", "checkpoint-115.ddsave", "checkpoint-163.ddsave", "checkpoint-165.ddsave",
                 "restored-165.ddsave", "warm-final.ddsave", "authentic-predecessor.ddsave"):
        retain(args.connected / name, f"connected/saves/{name}")
    retain(args.connected / "walkthrough.jsonl", "walkthrough.jsonl")
    for name in ("results.json", "inputs.jsonl", "responses.jsonl"):
        retain(args.console / name, f"console/{name}")

    implementation = {
        "implementationCommit": args.implementation,
        "sourceArchiveSha256": digest(archive_bytes),
        "executedAssemblies": assemblies,
    }
    regression_cases = None
    if args.regression:
        run = args.regression
        names = lines(run / "all-names.txt")
        prior = lines(packet.parent / "2026-11-12-int03-playability/regression/inventory.txt")
        focus = headless["cases"][0]["Name"]
        if len(names) != 1481 or len(set(names)) != 1481 or [name for name in names if name != focus] != prior:
            raise ValueError("The exact session inventory differs from the accepted predecessor inventory.")
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
        if set(names) != results.keys() or results[focus] != headless["cases"][0]:
            raise ValueError("The executed journals differ from the inventory or the focus result.")
        retain(run / "all-names.txt", "regression/inventory.txt")
        report = {"status": "PASS", **implementation, "testsDiscovered": len(names), "passed": len(names),
                  "failed": 0, "cases": [results[name] for name in names], "unity": "NOT RUN"}
        path = packet / "regression/results.json"
        path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
        artifacts["regression/results.json"] = file_binding(path)
        regression_cases = len(names)

    binding = {
        **implementation,
        "gptGateReview": "7e7a9141-78c3-4dcb-923b-7ea779e7eab2",
        "compiledSourceCounts": {
            "headless": len(headless["sourceHashes"]),
            "standalone": len(standalone["sourceHashes"]),
            "staticInputs": len(static["sourceHashes"]),
        },
        "focusedCases": headless["cases"],
        "regressionCases": regression_cases,
        "performanceStatus": connected["Status"],
        "finalCanonicalSha256": connected["RepeatedFinalSha256"],
        "artifacts": dict(sorted(artifacts.items())),
    }
    (packet / "BINDINGS.json").write_text(json.dumps(binding, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
