"""One-shot local preservation and text verification; never executes downloaded code."""
from pathlib import Path, PurePosixPath
from datetime import datetime, timezone
import ast
import hashlib
import io
import json
import stat
import zipfile

G = Path(r"C:\Github\DecenniumDescent")
A = G / "docs/audit/2026-10-08/full-game"
SOURCE = Path(r"C:\Users\cbord\Downloads\DD_Part5_Copied_Feat_Integration_Supplement_02.zip")
ARCHIVE = A / SOURCE.name
ROOT = A / "copied-feat-integration-part5-supplement-02"
RECEIPT = A / "COPIED_FEAT_PART5_SUPPLEMENT_02_LOCAL_PREFLIGHT.json"


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def binding(path):
    raw = path.read_bytes()
    return {"path": path.relative_to(G).as_posix(), "bytes": len(raw), "sha256": digest(raw)}


def main():
    assert not ARCHIVE.exists() and not ROOT.exists() and not RECEIPT.exists()
    checks = []

    def check(label, condition):
        checks.append({"check": label, "passed": bool(condition)})
        assert condition, label

    def matches(raw, metadata):
        return len(raw) == metadata["bytes"] and digest(raw) == metadata["sha256"]

    def replay(before, after, operations, label):
        current = before
        for op in operations:
            old, new = op["before"].encode(), op["after"].encode()
            check(label + " unique before " + op["id"],
                  op["kind"] == "replace-exact-text" and current.count(old) == 1)
            current = current.replace(old, new, 1)
        check(label + " complete forward bytes", current == after)
        for op in reversed(operations):
            old, new = op["before"].encode(), op["after"].encode()
            check(label + " unique after " + op["id"], current.count(new) == 1)
            current = current.replace(new, old, 1)
        check(label + " complete reverse bytes", current == before)

    raw = SOURCE.read_bytes()
    check("Exact GPT-reported supplement archive",
          len(raw) == 37269540 and digest(raw) ==
          "8ca9f7d6cca9f3353888cd1afb806d705e05e50357c809604cc2f95c54fb83d8")
    with zipfile.ZipFile(io.BytesIO(raw)) as z:
        names = z.namelist()
        check("Archive CRC", z.testzip() is None)
        check("52 unique safe regular members", len(names) == len(set(names)) == 52 and
              all(not PurePosixPath(n).is_absolute() and ".." not in PurePosixPath(n).parts
                  and "\\" not in n and ":" not in n and not n.endswith("/")
                  and not stat.S_ISLNK(z.getinfo(n).external_attr >> 16) for n in names))
        manifest = json.loads(z.read("MANIFEST.json"))
        check("Complete 51-member manifest", manifest["fileCount"] == len(manifest["files"]) == 51
              and {f["path"] for f in manifest["files"]} == set(names) - {"MANIFEST.json"})
        for f in manifest["files"]:
            check("Manifest " + f["path"], matches(z.read(f["path"]), f))
        prior_name = "DD_Part5_Copied_Feat_Integration_Review_01.zip"
        prior_raw = z.read("history/" + prior_name)
        check("Complete Return01 archive unchanged", prior_raw == (A / prior_name).read_bytes())
        with zipfile.ZipFile(io.BytesIO(prior_raw)) as prior:
            original_ops = json.loads(prior.read("CODE_OPERATIONS.json"))["operations"]
            cumulative = json.loads(z.read("CUMULATIVE_CODE_OPERATIONS_FROM_ORIGINAL.json"))
            delta = json.loads(z.read("CODE_OPERATIONS_FROM_RETURN01.json"))
            check("14 cumulative operations retain original eleven plus three",
                  cumulative["operationCount"] == len(cumulative["operations"]) == 14
                  and delta["operationCount"] == len(delta["operations"]) == 3
                  and cumulative["operations"] == original_ops + delta["operations"])
            bindings = json.loads(z.read("ARTIFACT_BINDINGS.json"))
            check("Four complete files, one supplement change",
                  bindings["fileCount"] == len(bindings["files"]) == 4
                  and bindings["changedFileCount"] == 1
                  and sum(f["changedByThisSupplement"] for f in bindings["files"]) == 1)
            for f in bindings["files"]:
                path = f["path"]
                before, proposed = prior.read("baseline/" + path), prior.read("proposed/" + path)
                successor = z.read("successor/" + path)
                check("Original and live baseline " + path,
                      before == (G / path).read_bytes() and matches(before, f["original"]))
                check("Return01 proposed binding " + path, matches(proposed, f["return01Proposal"]))
                check("Supplement successor binding " + path,
                      matches(successor, f["supplement02Successor"]))
                check("Declared changed-file state " + path,
                      (proposed != successor) == f["changedByThisSupplement"])
                replay(before, successor,
                       [o for o in cumulative["operations"] if o["path"] == path],
                       "Cumulative " + path)
                replay(proposed, successor,
                       [o for o in delta["operations"] if o["path"] == path],
                       "Incremental " + path)
                ast.parse(successor.decode("utf-8"), filename=path)
                check("Successor Python syntax parses without execution " + path, True)
            path = delta["path"]
            check("Both complete supplement baselines",
                  z.read("baseline_original/" + path) == prior.read("baseline/" + path)
                  and z.read("baseline_return01/" + path) == prior.read("proposed/" + path))
        for name in [n for n in names if n.startswith("sources/")]:
            check("Current complete source " + name, z.read(name) == (G / name[8:]).read_bytes())
        refs = json.loads(z.read("SOURCE_REFERENCES.json"))["references"]
        for ref in refs:
            source = z.read(ref["path"])
            check("Source reference binding " + ref["id"], matches(source, ref))
            check("Source reference complete excerpt " + ref["id"],
                  "\n".join(source.decode().splitlines()[ref["lineStart"]-1:ref["lineEnd"]])
                  == ref["exactText"].rstrip("\n"))
        successor = z.read("successor/" + delta["path"]).decode()
        check("Both Mend guards filter actual live next-healing records",
              successor.count("r.present and not r.suppressed and r.next_healing") == 2)
        check("Advance forwards actual expiry instructions after projection",
              "instructions=self.buffers.expire(marker);self.projection()\n        return instructions" in successor)
        check("Three new operations scoped to the two findings",
              {o["finding"] for o in delta["operations"]} == {"CFI-06", "CFI-07"}
              and {o["path"] for o in delta["operations"]} == {delta["path"]})
        # Write only after all checks pass. No canonical source or prior evidence is replaced.
        with ARCHIVE.open("xb") as output:
            output.write(raw)
        ROOT.mkdir()
        for name in names:
            target = ROOT / PurePosixPath(name)
            target.parent.mkdir(parents=True, exist_ok=True)
            with target.open("xb") as output:
                output.write(z.read(name))

    report = {
        "recordedAtUtc": datetime.now(timezone.utc).isoformat(),
        "status": "preserved-and-locally-text-verified-proposed-two-defect-correction",
        "archive": binding(ARCHIVE), "verificationScript": binding(Path(__file__)),
        "actualGptEvidence": binding(A / "GPT_PART5_PERTINENT_OWNER_CHOICES_2026_10_20_NATIVE.json"),
        "gptAssistantId": "3d85fd5e-6d8b-446b-ace4-e6d5a16c6f6c",
        "extractedRoot": ROOT.relative_to(G).as_posix(),
        "checkCount": len(checks), "failures": 0, "checks": checks,
        "localVerification": "Archive/member/source bindings, four live originals, both alternative reconstruction paths, exact reverse bytes, source excerpts and narrow textual semantics. Python syntax parsed only.",
        "gptReportedOnly": {"targetedTests": 36, "priorRegressionTests": 47,
                            "existingHelperAssertions": 456, "preservationChecks": 412},
        "downloadedCodeExecuted": False, "implementationApplied": False,
        "canonicalRuleOrIndexChanged": False, "sourceInformationDeleted": 0,
        "retainedWork": [
            "Actual active next-healing source consumption remains required.",
            "Expiry choice/removal, source-owned dispatch, receipt persistence and retry/deduplication remain required.",
            "Complete Ready, positive canonical Shaman Step and printed missing Boon/Step variants remain required.",
            "The owner's later preparation-round-only Ready choice supersedes historical both-round wording; a separate proposed successor is requested.",
            "GPT's executable results were not rerun locally; no game-engine, human-play, balance or release completion is claimed."
        ],
        "authoredCountsUnchanged": {"reviewed": 525, "pending": 323, "standalone": 249,
                                   "total": 848, "interfaces": 173, "acceptedButUnapplied": 39}
    }
    with RECEIPT.open("x", encoding="utf-8", newline="\n") as output:
        json.dump(report, output, ensure_ascii=False, indent=2)
        output.write("\n")
    print(json.dumps({"receipt": binding(RECEIPT), "checks": len(checks), "failures": 0}))


if __name__ == "__main__":
    main()
