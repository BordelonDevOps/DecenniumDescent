"""Retain the focused packet or finalize the exact regression on its original assemblies."""

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


def write_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")


def digest(contents):
    return hashlib.sha256(contents).hexdigest()


def artifact(path):
    contents = path.read_bytes()
    return {"sha256": digest(contents), "bytes": len(contents)}


def copy_file(source, target):
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, target)
    return target


def copy_report(source, packet, relative, source_zip):
    report = read_json(source)
    if report["status"] != "PASS":
        raise ValueError(f"Failed validation report: {source}")
    for item in report["sourceHashes"]:
        path = "engine/" + item["path"].replace("\\", "/")
        if digest(source_zip.read(path)) != item["sha256"].lower():
            raise ValueError(f"Source binding changed: {path}")
    copy_file(source, packet / relative)
    return report


def read_lines(path):
    return path.read_text(encoding="utf-8-sig").splitlines()


def finalize_regression(run, packet, manifest):
    names = read_lines(run / "all-names.txt")
    if len(names) != 1478 or len(set(names)) != 1478:
        raise ValueError("Unexpected compiled case inventory.")
    results = {}
    for group in "ABCDEF":
        label = "shard" + group
        assigned = read_lines(run / f"{label}-names.txt")
        finished = read_lines(run / f"{label}.done")
        path = run / f"{label}.jsonl"
        rows = [json.loads(line) for line in read_lines(path)]
        if finished != ["DONE"] or assigned != [row["Name"] for row in rows]:
            raise ValueError(f"Regressions did not complete in assignment order: {label}")
        for row in rows:
            if row["Name"] in results or not row["Passed"] or row["Error"]:
                raise ValueError(f"Duplicate or failed result: {row}")
            results[row["Name"]] = row
        for suffix in ("-names.txt", ".jsonl", ".done"):
            copy_file(run / (label + suffix), packet / "regression" / (label + suffix))
    if set(results) != set(names):
        raise ValueError("Regressions did not cover the exact compiled inventory.")
    copy_file(run / "all-names.txt", packet / "regression/inventory.txt")
    write_json(packet / "validation/results.json", {
        "status": "PASS",
        "implementationCommit": manifest["implementationCommit"],
        "sourceArchiveSha256": manifest["sourceArchiveSha256"],
        "executedAssemblies": manifest["executedAssemblies"],
        "testsDiscovered": len(names),
        "passed": len(names),
        "failed": 0,
        "execution": "Six unfiltered journals on the four exact retained assemblies.",
        "unity": "NOT RUN",
        "cases": [results[name] for name in names],
    })
    manifest["unfilteredCases"] = len(names)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("commit")
    parser.add_argument("--headless", type=Path, required=True)
    parser.add_argument("--standalone", type=Path, required=True)
    parser.add_argument("--static", type=Path, required=True)
    parser.add_argument("--no-laboratory", type=Path, required=True)
    parser.add_argument("--compatibility", type=Path, required=True)
    parser.add_argument("--timeline", type=Path, required=True)
    parser.add_argument("--regression", type=Path)
    args = parser.parse_args()
    packet = Path(__file__).resolve().parent
    source_archive = subprocess.check_output(["git", "archive", "--format=zip", args.commit, "engine"])
    source_zip = zipfile.ZipFile(io.BytesIO(source_archive))
    focused = copy_report(args.headless / "results.json", packet, "focused/results.json", source_zip)
    if focused["testsDiscovered"] != 1 or focused["passed"] != 1 or focused["failed"]:
        raise ValueError("The exact focused case did not pass.")
    standalone = copy_report(args.standalone, packet, "compile/results.json", source_zip)
    static = copy_report(args.static, packet, "static/results.json", source_zip)
    no_laboratory = copy_report(args.no_laboratory, packet, "compile/no-laboratory.json", source_zip)
    files = sorted((args.headless / "saves").glob("tac10-*.ddsave"))
    if not files or not (args.headless / "saves/tac10-timings.csv").is_file():
        raise ValueError("Missing focused saves or timings.")
    for file in files:
        copy_file(file, packet / "focused/saves" / file.name)
    copy_file(args.headless / "saves/tac10-timings.csv", packet / "focused/timings.csv")
    compatibility = read_json(args.compatibility)
    timeline = read_json(args.timeline)
    if compatibility["status"] != "PASS" or len(compatibility["savedStates"]) != 22:
        raise ValueError("Authentic wire95 compatibility checks did not pass.")
    if timeline["status"] != "PASS" or len(timeline["states"]) != len(files):
        raise ValueError("Focused save timeline does not match the save inventory.")
    copy_file(args.compatibility, packet / "compatibility/results.json")
    copy_file(args.timeline, packet / "focused/timeline.json")
    manifest = {
        "implementationCommit": args.commit,
        "sourceArchiveSha256": digest(source_archive),
        "sourceProposal": "172fe189b929f5c3ac399f1de2c04f24c22bf018",
        "gptSourceApiReview": "a3ba325d-e745-4a94-a85f-08c49d907632",
        "acceptedPredecessor": "0f4d1139dd28a4c8d1051ca82fa81adc2b336dfb",
        "wire": 95,
        "baseSchema": 90,
        "compiledSourceCounts": {
            "headless": len(focused["sourceHashes"]),
            "standalone": len(standalone["sourceHashes"]),
            "withoutLaboratory": len(no_laboratory["sourceHashes"]),
            "staticInputs": len(static["sourceHashes"]),
        },
        "focusedCases": [row["Name"] for row in focused["cases"]],
        "savedStates": len(files),
        "authenticPredecessorSaves": len(compatibility["savedStates"]),
        "executedAssemblies": {},
    }
    for assembly in ("Core", "Persistence", "LabModel", "HeadlessTests"):
        name = f"Decennium.Foundation.{assembly}.dll"
        path = copy_file(args.headless / name, packet / "focused/assemblies" / name)
        manifest["executedAssemblies"][name] = artifact(path)
    if args.regression:
        processes = read_json(args.regression / "processes.json")
        if len(processes) != 6 or any(Path(row["assemblyRoot"]).resolve() != args.headless.resolve() for row in processes):
            raise ValueError("Regression assembly root differs from the focused assembly root.")
        finalize_regression(args.regression, packet, manifest)
    roots = ["focused", "compile", "static", "compatibility"]
    if args.regression:
        roots += ["regression", "validation"]
    manifest["artifacts"] = {
        path.relative_to(packet).as_posix(): artifact(path)
        for root in roots for path in sorted((packet / root).rglob("*")) if path.is_file()
    }
    write_json(packet / "BINDINGS.json", manifest)
    print(f"Retained {len(manifest['artifacts'])} artifacts for {args.commit}.")


if __name__ == "__main__":
    main()
