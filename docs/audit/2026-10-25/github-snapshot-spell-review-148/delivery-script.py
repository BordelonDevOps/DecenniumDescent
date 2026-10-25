"""Build a preservation-based GitHub snapshot of the current spell-review state."""
from pathlib import Path
from collections import Counter
from datetime import datetime, timezone
import hashlib
import importlib.util
import io
import json
import os
import subprocess
import sys
import time
import zipfile

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("delivery_policy", HERE / "deliver_progress_2026_10_14.py")
policy = importlib.util.module_from_spec(spec)
spec.loader.exec_module(policy)

SOURCE = Path(r"C:\Github\DecenniumDescent")
DEST = Path(r"C:\Github\DecenniumDescent-review-push-134")
WORK = HERE.parent / "audit_work" / "github-push-spell-review-148-attempt02"
REPORT = "docs/audit/2026-10-25/github-snapshot-spell-review-148"
BASE = "6b96c99f63ebbd63eb0d088aa1fedfcc886fae8e"
BRANCH = "codex/ordinary-spell-review-complete"
STATUS = "SNAPSHOT_STATUS_2026-10-25_SPELL_REVIEW_148.md"
MAX_CHUNK_BYTES = 1_500_000_000
INDEX = "DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json"
HANDOFF = "docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT_HANDOFF_148.json"
PENDING = "docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT148_PENDING_IDENTITY_AUDIT_148.json"

def lp(path):
    path = Path(path)
    return Path("\\\\?\\" + str(path.resolve())) if os.name == "nt" else path

def git(*args, data=None, env=None):
    merged = os.environ.copy()
    if env:
        merged.update(env)
    return subprocess.run(
        ["git", "-c", "core.longpaths=true", "-c", "core.autocrlf=false", *args],
        cwd=DEST,
        input=data,
        capture_output=True,
        check=True,
        env=merged,
    ).stdout

def digest(raw):
    return hashlib.sha256(raw).hexdigest()

def git_blob(raw):
    return hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()

def jsraw(value):
    return (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8")

def write_new(path, raw):
    path = lp(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("xb") as f:
        f.write(raw)

def tree(ref):
    result = {}
    for row in git("ls-tree", "-r", "-z", ref).split(b"\0"):
        if row:
            meta, name = row.split(b"\t", 1)
            mode, kind, oid = meta.decode().split()
            result[name.decode("utf-8", "surrogateescape")] = {"mode": mode, "oid": oid}
    return result

def is_text(name):
    return Path(name).suffix.lower() in policy.TEXT

def zip_issue(raw, name, depth=0):
    if depth > 5:
        return "nested archive depth exceeds review limit"
    try:
        with zipfile.ZipFile(io.BytesIO(raw)) as archive:
            for item in archive.infolist():
                if item.is_dir():
                    continue
                issue = policy.reason(item.filename)
                if issue and not issue.startswith("generated"):
                    return f"archive contains locally retained material: {issue}"
                if item.file_size >= 100 * 1024 * 1024:
                    return "archive contains an oversized member"
                content = archive.read(item)
                if is_text(item.filename) and any(rx.search(content) for rx in policy.SECRET):
                    return "archive contains credential-pattern match"
                if Path(item.filename).suffix.lower() == ".zip":
                    issue = zip_issue(content, item.filename, depth + 1)
                    if issue:
                        return issue
    except (zipfile.BadZipFile, OSError, RuntimeError):
        return "archive inspection failed"
    return None

def verify_base(require_clean=True):
    if require_clean:
        assert git("status", "--porcelain=v1", "-z") == b"", "Delivery checkout must be clean."
    assert git("rev-parse", "HEAD").decode().strip() == BASE, "Unexpected delivery branch base."
    assert git("branch", "--show-current").decode().strip() == BRANCH, "Unexpected delivery branch."
    remote = git("ls-remote", "origin", "refs/heads/main").decode().split()
    assert remote and remote[0] == BASE, "GitHub main advanced; rebase the snapshot plan before pushing."
    target_branch = git("ls-remote", "origin", f"refs/heads/{BRANCH}").decode().split()
    assert not target_branch, "Snapshot branch already exists remotely; inspect it before updating."

def scan():
    verify_base()
    assert not WORK.exists(), "Keep earlier delivery evidence intact."
    WORK.mkdir(parents=True)
    baseline = tree("HEAD")
    args = ["rg", "--files", "--hidden", "--no-ignore", "-g", "!Descent assets/**"]
    for part in policy.SKIP:
        args += ["-g", f"!**/{part}/**"]
    names = subprocess.run(args, cwd=SOURCE, capture_output=True, text=True, encoding="utf-8", check=True).stdout.splitlines()
    included, excluded, alerts = [], [], []
    unchanged = 0
    for i, name in enumerate(sorted(n.replace("\\", "/") for n in names)):
        path = lp(SOURCE / name)
        assert not path.is_symlink(), name
        stat_before = path.stat()
        row = {"path": name, "bytes": stat_before.st_size}
        issue = policy.reason(name)
        if not issue and stat_before.st_size >= 100 * 1024 * 1024:
            issue = "oversized regular Git blob; preserved locally"
        if issue:
            row["reason"] = issue
            excluded.append(row)
        else:
            raw = path.read_bytes()
            assert (stat_before.st_size, stat_before.st_mtime_ns) == (path.stat().st_size, path.stat().st_mtime_ns), name
            row.update(sha256=digest(raw), gitBlob=git_blob(raw))
            if baseline.get(name, {}).get("oid") == row["gitBlob"]:
                unchanged += 1
            else:
                if Path(name).suffix.lower() == ".zip":
                    issue = zip_issue(raw, name)
                if not issue and is_text(name) and any(rx.search(raw) for rx in policy.SECRET):
                    issue = "credential-pattern review required; preserved locally"
                    alerts.append(name)
                if issue:
                    row["reason"] = issue
                    excluded.append(row)
                    if "credential-pattern" in issue:
                        alerts.append(name)
                else:
                    row["changedFromBase"] = True
                    included.append(row)
        if i and i % 5000 == 0:
            print(json.dumps({"filesInspected": i, "included": len(included), "excluded": len(excluded)}), flush=True)
    plan = {
        "createdAtUtc": datetime.now(timezone.utc).isoformat(),
        "ownerInstruction": "Push all current spell-review work to GitHub.",
        "scope": "Preservation snapshot through Return148; next Ward5 review packet is prepared and remains unaccepted.",
        "sourceRoot": str(SOURCE),
        "deliveryRoot": str(DEST),
        "baseCommit": BASE,
        "branch": BRANCH,
        "sourceFileCount": len(names),
        "unchangedSourceFileCount": unchanged,
        "included": included,
        "excluded": excluded,
        "excludedTreesPreservedLocally": ["Descent assets", *policy.SKIP],
        "credentialPatternAlerts": sorted(set(alerts)),
        "sourceInformationDeleted": 0,
        "gitHistoryRewritten": False,
    }
    write_new(WORK / "plan.json", jsraw(plan))
    changed = [row["path"] for row in included if row["changedFromBase"]]
    write_new(WORK / "changed-source-paths.json", b"\n".join(x.encode("utf-8") for x in changed) + b"\n")
    print(json.dumps({
        "includedFiles": len(included),
        "changedOrNewSourceFiles": len(changed),
        "unchangedSourceFiles": unchanged,
        "includedBytes": sum(x["bytes"] for x in included),
        "excludedFiles": len(excluded),
        "exclusionReasons": dict(Counter(x["reason"] for x in excluded)),
        "credentialPatternAlerts": sorted(set(alerts)),
        "workDirectory": str(WORK),
    }), flush=True)

def read_source_json(name):
    return json.loads(lp(SOURCE / name).read_bytes())

def assemble():
    verify_base()
    plan = json.loads((WORK / "plan.json").read_bytes())
    assert not plan["credentialPatternAlerts"], "Review credential-pattern matches before assembly."
    selected = []
    for row in plan["included"]:
        if not row["changedFromBase"]:
            continue
        raw = lp(SOURCE / row["path"]).read_bytes()
        assert digest(raw) == row["sha256"], row["path"]
        target = lp(DEST / row["path"])
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(raw)
        assert digest(target.read_bytes()) == row["sha256"], row["path"]
        selected.append(row["path"])

    index = read_source_json(INDEX)
    assert index["authoredCounts"] == {"reviewed": 700, "pending": 148}
    handoff = read_source_json(HANDOFF)
    assert handoff["currentAuthority"]["reviewedApplied"] == 700 and handoff["currentAuthority"]["pending"] == 148
    pending = read_source_json(PENDING)
    assert pending["pendingCount"] == 148

    snapshot_notice = f"> **GitHub snapshot — 25 October 2026:** Ordinary spell review is at **700 applied-reviewed / 148 pending**. Return148 was accepted and applied with retained holds. The next Ward5 packet is prepared; its review and acceptance remain pending. See [snapshot status]({STATUS}). Earlier notes below are retained history.\n\n"
    overlays = []
    for name in ["README.md", "START_HERE.md"]:
        original = lp(SOURCE / name).read_bytes()
        preserved = f"{REPORT}/source-before/{name}"
        write_new(DEST / preserved, original)
        delivered = snapshot_notice.encode("utf-8") + original
        lp(DEST / name).write_bytes(delivered)
        overlays.append({"path": name, "sourceSha256": digest(original), "deliveredSha256": digest(delivered), "preservedSource": preserved})
        selected.extend([name, preserved])

    status = f"""# Decennium Descent backup — 25 October 2026

This owner-requested snapshot preserves the current ordinary spell review state through Return148. The public GitHub branch is a saved-work backup; it does not claim whole-game completion, runtime readiness or release approval.

- The authored index records **700 applied-reviewed / 148 pending**, with **424 complete reviewed standalone procedures** and zero accepted-but-unapplied spells.
- GPT accepted and the local application verified five Return148 identities. Retained holds and all earlier completed cohorts remain intact.
- The next `rank8-ward5` packet contains Alignment Immunity, Antilife Shell, Antimagic Field, Mind Blank and Reputation Fortress. It is prepared for GPT review; no acceptance is claimed for it.
- Feat335 and completed spell cohorts remain closed. Runtime selection, implementation, human play, balance, cosmology and release approval remain separate.
- The [current handoff]({HANDOFF}), [pending identity audit]({PENDING}) and application validation at `docs/audit/2026-10-08/full-game/director-spell-review-129/RANK8_CONTROL5_APPLICATION_VALIDATION_148.json` record the current authority.

The [manifest]({REPORT}/manifest.json) lists source fingerprints and files kept local under the established privacy and archive checks. Existing tracked Git entries and history are preserved. No source information was deleted and no force-push was used.
"""
    delivery = {
        "recordedAtUtc": datetime.now(timezone.utc).isoformat(),
        "status": "Saved-work snapshot through Return148; Ward5 prepared, awaiting GPT review",
        "authoredCounts": index["authoredCounts"],
        "standaloneProcedureCount": index["representationCounts"]["completeReviewedStandaloneProcedures"],
        "acceptedUnapplied": 0,
        "closedCohortsReopened": False,
        "runtimeOrReleaseApprovalClaimed": False,
        "sourceInformationDeleted": 0,
        "baseCommit": BASE,
        "branch": BRANCH,
    }
    manifest = dict(plan)
    manifest.update({
        "assembledAtUtc": datetime.now(timezone.utc).isoformat(),
        "deliveryOverlays": overlays,
        "allSelectedSourcesReverified": True,
        "preservedExistingTrackedEntries": True,
    })
    extras = {
        STATUS: status.encode("utf-8"),
        f"{REPORT}/DELIVERY_CHECKPOINT.json": jsraw(delivery),
        f"{REPORT}/manifest.json": jsraw(manifest),
        f"{REPORT}/delivery-script.py": Path(__file__).read_bytes(),
    }
    for name, raw in extras.items():
        write_new(DEST / name, raw)
        selected.append(name)
    source_sizes = {row["path"]: row["bytes"] for row in plan["included"]}
    for name, row in zip(["README.md", "START_HERE.md"], overlays):
        source_sizes[name] = len(lp(DEST / name).read_bytes())
        source_sizes[row["preservedSource"]] = len(lp(DEST / row["preservedSource"]).read_bytes())
    for name, raw in extras.items():
        source_sizes[name] = len(raw)

    selected = sorted(set(selected))
    core_paths = []
    rest_paths = []
    for name in selected:
        low = name.lower()
        core = (
            name in {"README.md", "START_HERE.md", INDEX, HANDOFF, PENDING}
            or name.startswith(REPORT + "/")
            or "return148" in low
            or "rank8control5" in low
            or "rank8_ward_5_source_conference_02" in low
            or "rank8-ward5-source-conference-02" in low
        )
        (core_paths if core else rest_paths).append(name)

    chunks = [{"paths": sorted(core_paths), "rawBytes": sum(source_sizes[p] for p in core_paths)}]
    assert chunks[0]["rawBytes"] <= MAX_CHUNK_BYTES, "Core checkpoint exceeds safe single-push size."
    rest_paths.sort(key=lambda p: (-source_sizes[p], p))
    for name in rest_paths:
        size = source_sizes[name]
        assert size <= MAX_CHUNK_BYTES, f"Oversized file escaped screening: {name}"
        slot = next((chunk for chunk in chunks[1:] if chunk["rawBytes"] + size <= MAX_CHUNK_BYTES), None)
        if slot is None:
            slot = {"paths": [], "rawBytes": 0}
            chunks.append(slot)
        slot["paths"].append(name)
        slot["rawBytes"] += size
    for i, chunk in enumerate(chunks, 1):
        chunk["id"] = i
        chunk["pathCount"] = len(chunk["paths"])
        chunk_file = WORK / "chunks" / f"chunk-{i:02}.nul"
        write_new(chunk_file, b"\0".join(p.encode("utf-8") for p in sorted(chunk["paths"])) + b"\0")
    push_plan = {
        "reason": "GitHub enforces a 2 GiB single-push limit; raw file content is partitioned below 1.5 GB per incremental commit.",
        "maxRawBytesPerPush": MAX_CHUNK_BYTES,
        "totalSourcePaths": len(selected),
        "totalRawBytes": sum(source_sizes[p] for p in selected),
        "chunks": [{"id": c["id"], "pathCount": c["pathCount"], "rawBytes": c["rawBytes"]} for c in chunks],
        "deletions": 0,
        "forcePush": False,
    }
    validation = {
        "verifiedAtUtc": datetime.now(timezone.utc).isoformat(),
        "changedSourceFilesRehashed": len([x for x in plan["included"]]),
        "unchangedSourceFilesLeftAtBase": plan["unchangedSourceFileCount"],
        "excludedLocalFiles": len(plan["excluded"]),
        "credentialPatternAlerts": 0,
        "stagedPaths": len(selected) + 1,
        "previousGitEntriesDeleted": 0,
        "contentValidation": "all selected source SHA-256 values rechecked during copy; archive and credential screening passed",
        "pushChunkCount": len(chunks),
        "maxRawBytesPerPush": MAX_CHUNK_BYTES,
        "plannedSourceBytes": sum(source_sizes[p] for p in selected),
    }
    validation_path = f"{REPORT}/PUSH_PLAN_VALIDATION.json"
    validation_raw = jsraw(validation)
    write_new(DEST / validation_path, validation_raw)
    assert len(validation_raw) <= 4096 and chunks[0]["rawBytes"] + len(validation_raw) <= MAX_CHUNK_BYTES
    chunks[0]["paths"].append(validation_path)
    chunks[0]["rawBytes"] += len(validation_raw)
    chunks[0]["pathCount"] += 1
    chunk_file = WORK / "chunks" / "chunk-01.nul"
    chunk_file.write_bytes(b"\0".join(p.encode("utf-8") for p in sorted(chunks[0]["paths"])) + b"\0")
    push_plan["chunks"] = [{"id": c["id"], "pathCount": c["pathCount"], "rawBytes": c["rawBytes"]} for c in chunks]
    (WORK / "push-plan.json").write_bytes(jsraw(push_plan))
    paths_file = WORK / "stage-paths.nul"
    write_new(paths_file, b"\0".join(p.encode("utf-8") for p in selected + [validation_path]) + b"\0")
    print(json.dumps({"sourceFilesCopiedAndVerified": len([x for x in plan["included"]]), "pathsToStage": len(selected) + 1, "indexCounts": index["authoredCounts"], "chunkCount": len(chunks), "chunkRawBytes": [c["rawBytes"] for c in chunks], "sourceInformationDeleted": 0}), flush=True)

def publish():
    plan = json.loads((WORK / "plan.json").read_bytes())
    push_plan = json.loads((WORK / "push-plan.json").read_bytes())
    chunk_dir = WORK / "chunks"
    assert not plan["credentialPatternAlerts"], "Credential-pattern matches require inspection before push."
    assert git("rev-parse", "HEAD").decode().strip() == BASE
    assert git("branch", "--show-current").decode().strip() == BRANCH
    assert not git("ls-remote", "origin", f"refs/heads/{BRANCH}").decode().split()
    commits = []
    total_chunks = len(push_plan["chunks"])
    for i, chunk in enumerate(push_plan["chunks"], 1):
        expected_head = BASE if i == 1 else commits[-1]["commit"]
        assert git("rev-parse", "HEAD").decode().strip() == expected_head
        main_ref = git("ls-remote", "origin", "refs/heads/main").decode().split()
        assert main_ref and main_ref[0] == BASE, "GitHub main advanced during snapshot delivery."
        remote_branch = git("ls-remote", "origin", f"refs/heads/{BRANCH}").decode().split()
        if i == 1:
            assert not remote_branch, "Snapshot branch appeared during preparation."
        else:
            assert remote_branch and remote_branch[0] == expected_head, "Remote branch moved unexpectedly."
        path_file = chunk_dir / f"chunk-{i:02}.nul"
        expected_paths = {x.decode("utf-8", "surrogateescape") for x in path_file.read_bytes().split(b"\0") if x}
        git("add", f"--pathspec-from-file={path_file}", "--pathspec-file-nul")
        staged_paths = {x.decode("utf-8", "surrogateescape") for x in git("diff", "--cached", "--name-only", "-z").split(b"\0") if x}
        assert staged_paths == expected_paths, f"Chunk {i} staged paths differ from plan."
        assert not git("diff", "--cached", "--name-only", "--diff-filter=D", "-z"), "Snapshot attempted a deletion."
        baseline = tree("HEAD")
        staged_tree = tree(git("write-tree").decode().strip())
        assert all(name in staged_tree for name in baseline), "A prior tracked Git entry was deleted."
        assert all(staged_tree[name] == baseline[name] for name in baseline if name not in staged_paths), "An entry changed outside this chunk."
        future_paths = set()
        for future_index in range(i + 1, total_chunks + 1):
            future_file = chunk_dir / f"chunk-{future_index:02}.nul"
            future_paths.update(x.decode("utf-8", "surrogateescape") for x in future_file.read_bytes().split(b"\0") if x)
        unstaged_paths = {x.decode("utf-8", "surrogateescape") for x in git("diff", "--name-only", "-z").split(b"\0") if x}
        untracked_paths = {x.decode("utf-8", "surrogateescape") for x in git("ls-files", "--others", "--exclude-standard", "-z").split(b"\0") if x}
        assert unstaged_paths <= future_paths and untracked_paths <= future_paths, "Unplanned local file found in delivery checkout."
        git("commit", "-m", f"Preserve ordinary spell review checkpoint 148 ({i}/{total_chunks})")
        commit = git("rev-parse", "HEAD").decode().strip()
        assert git("rev-parse", "HEAD^").decode().strip() == expected_head
        if i > 1:
            time.sleep(11)
        if i == 1:
            git("push", "--set-upstream", "origin", f"HEAD:refs/heads/{BRANCH}")
        else:
            git("push", "origin", f"HEAD:refs/heads/{BRANCH}")
        remote = git("ls-remote", "origin", f"refs/heads/{BRANCH}").decode().split()
        assert remote and remote[0] == commit, f"GitHub branch did not advance to chunk {i}."
        commits.append({"chunk": i, "commit": commit, "paths": len(expected_paths), "rawBytes": chunk["rawBytes"], "remoteVerified": True})
        (WORK / "push-progress.json").write_bytes(jsraw({"completedChunks": commits, "totalChunks": total_chunks}))
        print(json.dumps({"pushedChunk": i, "totalChunks": total_chunks, "commit": commit, "paths": len(expected_paths), "rawBytes": chunk["rawBytes"], "remoteVerified": True}), flush=True)
    assert git("status", "--porcelain=v1", "-z") == b"", "Delivery checkout is not clean after all chunks."
    final_commit = git("rev-parse", "HEAD").decode().strip()
    remote = git("ls-remote", "origin", f"refs/heads/{BRANCH}").decode().split()
    main_ref = git("ls-remote", "origin", "refs/heads/main").decode().split()
    assert remote and remote[0] == final_commit and main_ref and main_ref[0] == BASE
    receipt = {
        "pushedAtUtc": datetime.now(timezone.utc).isoformat(),
        "branch": BRANCH,
        "remote": "https://github.com/BordelonDevOps/DecenniumDescent.git",
        "baseCommit": BASE,
        "finalCommit": final_commit,
        "commits": commits,
        "remoteVerified": True,
        "mainModified": False,
        "forcePush": False,
    }
    (WORK / "push-receipt.json").write_bytes(jsraw(receipt))
    print(json.dumps(receipt), flush=True)

if __name__ == "__main__":
    actions = {"scan": scan, "assemble": assemble, "push": publish}
    if len(sys.argv) != 2 or sys.argv[1] not in actions:
        raise SystemExit("usage: push_spell_review148.py scan|assemble|push")
    actions[sys.argv[1]]()
