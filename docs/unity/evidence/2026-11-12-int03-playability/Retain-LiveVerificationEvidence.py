"""Bind the measured P1 candidate and exact regression to committed source and assemblies."""

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


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def binding(path):
    data = path.read_bytes()
    return {"bytes": len(data), "sha256": sha256(data)}


def write_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")


def copy_file(source, target):
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, target)
    return target


def retain_report(source, target, archive):
    report = read_json(source)
    if report["status"] != "PASS":
        raise ValueError(f"Failed validation report: {source}")
    for item in report["sourceHashes"]:
        path = "engine/" + item["path"].replace("\\", "/")
        if sha256(archive.read(path)) != item["sha256"].lower():
            raise ValueError(f"Wrong source hash for {path}")
    copy_file(source, target)
    return report


def retain_regression(run, packet, manifest, focused):
    names = lines(run / "all-names.txt")
    if len(names) != 1480 or len(set(names)) != 1480:
        raise ValueError("Unexpected exact compiled inventory.")
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
            copy_file(run / (label + suffix), packet / "regression" / (label + suffix))
    if set(results) != set(names) or any(results.get(row["Name"]) != row for row in focused):
        raise ValueError("Full execution did not match the inventory and focused cases.")
    copy_file(run / "all-names.txt", packet / "regression/inventory.txt")
    write_json(packet / "validation/results.json", {
        "status": "PASS",
        "implementationCommit": manifest["implementationCommit"],
        "sourceArchiveSha256": manifest["sourceArchiveSha256"],
        "executedAssemblies": manifest["executedAssemblies"],
        "testsDiscovered": len(names),
        "passed": len(names),
        "failed": 0,
        "cases": [results[name] for name in names],
        "unity": "NOT RUN",
    })
    manifest["unfilteredCases"] = len(names)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("implementation")
    parser.add_argument("--headless", type=Path, required=True)
    parser.add_argument("--second-focus", type=Path, required=True)
    parser.add_argument("--standalone", type=Path, required=True)
    parser.add_argument("--static", type=Path, required=True)
    parser.add_argument("--no-laboratory", type=Path, required=True)
    parser.add_argument("--archive-vector", type=Path, required=True)
    parser.add_argument("--equivalence", type=Path, required=True)
    parser.add_argument("--performance", type=Path, required=True)
    parser.add_argument("--initial-performance", type=Path, required=True)
    parser.add_argument("--cold-start", type=Path, required=True)
    parser.add_argument("--compatibility", type=Path, required=True)
    parser.add_argument("--regression", type=Path)
    args = parser.parse_args()
    packet = Path(__file__).resolve().parent
    zipped = subprocess.check_output(["git", "archive", "--format=zip", args.implementation, "engine"])
    archive = zipfile.ZipFile(io.BytesIO(zipped))
    headless = retain_report(args.headless / "results.json", packet / "focused/headless.json", archive)
    standalone = retain_report(args.standalone, packet / "compile/results.json", archive)
    static = retain_report(args.static, packet / "static/results.json", archive)
    no_lab = retain_report(args.no_laboratory, packet / "compile/no-laboratory.json", archive)
    focused = headless["cases"] + [read_json(args.second_focus)]
    expected_cases = {
        "int03_verified_prefix_owned_atomic_and_corrupt_restore_rejected",
        "int03_verified_prefix_preserves_receipt_capacity_and_duplicate",
    }
    if {row["Name"] for row in focused} != expected_cases or any(not row["Passed"] or row["Error"] for row in focused):
        raise ValueError("The exact focused cases did not both pass.")
    write_json(packet / "focused/cases.json", focused)
    assemblies = {}
    for assembly in ("Core", "Persistence", "LabModel", "HeadlessTests"):
        name = f"Decennium.Foundation.{assembly}.dll"
        path = copy_file(args.headless / name, packet / "focused/assemblies" / name)
        assemblies[name] = binding(path)
    vector = read_json(args.archive_vector)
    if vector["status"] != "PASS" or [entry["revision"] for entry in vector["prefixes"]] != list(range(166)):
        raise ValueError("The independent archived source vector is incomplete.")
    copy_file(args.archive_vector, packet / "focused/archived-vector.json")
    vector_hash = binding(args.archive_vector)["sha256"]
    reports = {}
    for category, path in (
        ("equivalence", args.equivalence / "Equivalence.json"),
        ("performance", args.performance),
        ("cold-start", args.cold_start),
        ("compatibility", args.compatibility),
    ):
        report = read_json(path)
        if report["status"] != "PASS" or report["source"]["vectorSha256"] != vector_hash:
            raise ValueError(f"Unbound candidate report: {category}")
        if report["source"]["assemblies"] != {name: entry["sha256"] for name, entry in assemblies.items()}:
            raise ValueError(f"Assembly continuity failure in {category}.")
        reports[category] = report
        copy_file(path, packet / category / "results.json")
    if [row["sha256"] for row in reports["equivalence"]["committed"]] != [row["sha256"] for row in vector["prefixes"][1:]]:
        raise ValueError("Equivalence did not cover every original transition.")
    if len(reports["compatibility"]["authenticWire95Saves"]) != 22:
        raise ValueError("The authentic predecessor inventory changed.")
    performance = reports["performance"]
    first_timing = read_json(args.initial_performance)
    if (performance["priorPerformanceSha256"] != binding(args.initial_performance)["sha256"]
            or first_timing["source"] != performance["source"] or first_timing["status"] != "FAIL"):
        raise ValueError("The first timing run must be retained against the same source inputs.")
    combined = performance["combinedResults"]
    if (len(combined) != 8 or any(row["count"] != 2 * performance["warmSamplesPerWorkload"]
                                  or not row["met"] for row in combined)):
        raise ValueError("The complete measured distribution did not meet the approved budgets.")
    copy_file(args.initial_performance, packet / "performance/initial-run.json")
    if (performance["mode"] != "VerifiedPrefix" or performance["warmSamplesPerWorkload"] < 30
            or len(performance["results"]) != 8 or any(not row["met"] for row in performance["results"])):
        raise ValueError("The measured public verified path did not meet the approved budgets.")
    for name, revision in (("verified-pending-opportunity", 113), ("verified-continued", 165)):
        save = args.equivalence / (name + ".ddsave")
        if binding(save)["sha256"] != vector["prefixes"][revision]["sha256"]:
            raise ValueError(f"Wrong exact connected save: {name}")
        copy_file(save, packet / "equivalence/saves" / save.name)

    manifest = {
        "implementationCommit": args.implementation,
        "sourceArchiveSha256": sha256(zipped),
        "sourceProposal": "17c986baefee8671fe4da912c3dc3aca18104c49",
        "gptSourceApiReview": "f5c10493-8778-4c1d-b0e7-ae0628e2253e",
        "acceptedReference": vector["source"]["acceptedImplementation"],
        "executedAssemblies": assemblies,
        "compiledSourceCounts": {
            "headless": len(headless["sourceHashes"]),
            "standalone": len(standalone["sourceHashes"]),
            "noLaboratory": len(no_lab["sourceHashes"]),
            "staticInputs": len(static["sourceHashes"]),
        },
        "focusedCases": sorted(expected_cases),
        "canonicalTransitionComparisons": 165,
        "authenticWire95Saves": 22,
        "measuredCommands": len(performance["samples"]) + len(first_timing["samples"]),
    }
    roots = ["compile", "static", "focused", "equivalence", "performance", "cold-start", "compatibility"]
    if args.regression:
        processes = read_json(args.regression / "processes.json")
        if len(processes) != 6 or any(Path(row["assemblyRoot"]).resolve() != args.headless.resolve() for row in processes):
            raise ValueError("The regression used different assemblies.")
        retain_regression(args.regression, packet, manifest, focused)
        roots += ["regression", "validation"]
    manifest["artifacts"] = {
        file.relative_to(packet).as_posix(): binding(file)
        for root in roots for file in sorted((packet / root).rglob("*")) if file.is_file()
    }
    write_json(packet / "BINDINGS.json", manifest)
    print(f"Retained {len(manifest['artifacts'])} bound artifacts.")


if __name__ == "__main__":
    main()
