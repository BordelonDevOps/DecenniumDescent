#!/usr/bin/env python3
"""Bind the R02 target-state pointer to its rebuilt pickup transition and verify R03."""
import copy, hashlib, importlib.util, json, subprocess
from pathlib import Path

BASE = "b46452ad02962a5a3faa4d20f03cf5fd2ac72049"
R2_SHA = "c3353a7225b4e50be59f0e129a9274a5eb963712ebf4b63ea408378337cf1a70"
R2_COMMIT = BASE
P05 = "FR-EP480-INTERFACE-PROPOSAL-05"
P05_SHA = "cd492a5bdf9c966f83a2674c31ff1db02a10d2df5f3c92fe8b4680974047386d"
EXPECTED_TARGET_STATE = "23f127f668ca31f6af4939ea87605c3fad578bd125275df202f2a6a3420144ef"
T1_FINAL = "49d94d12e54fbd36d36a0cf3f69803f6de1b0f903557804c02dbd41f1a2ae7c3"
DIR = Path("docs/audit/2026-10-08/full-game/director-spell-review-129/fate_rewrite_ep480_interface_witness_2026-11-03")
R1_HELPER = DIR / "tools/build_verify_fr_ep480_p05_witnesses.py"
R2_PACKET = DIR / "FR_EP480_P05_TESTONLY_WITNESS_PACKET_R02.json"
R2_REVISE = DIR / "CODEX_TRANSCRIBED_DIRECTOR_REVIEW_REVISE_02.json"
R3_PACKET = DIR / "FR_EP480_P05_TESTONLY_WITNESS_PACKET_R03.json"
R3_REQUEST = DIR / "DIRECTOR_REVIEW_REQUEST_FR_EP480_P05_WITNESSES_R03.md"
R3_MANIFEST = DIR / "PACKET_MANIFEST_FR_EP480_P05_WITNESSES_R03.json"
R3_SCRIPT = DIR / "tools/build_verify_fr_ep480_p05_witnesses_r03.py"
STAMP = "2026-11-03T03:36:03Z"
ROOT = Path(subprocess.check_output(["git", "rev-parse", "--show-toplevel"], text=True).strip())

spec = importlib.util.spec_from_file_location("fr_p05_r01_helpers", ROOT / R1_HELPER)
H = importlib.util.module_from_spec(spec)
spec.loader.exec_module(H)

def gitshow(rev_path):
    return subprocess.check_output(["git", "show", rev_path], cwd=ROOT)

def sha(raw):
    return hashlib.sha256(raw).hexdigest()

def git_blob_sha1(raw):
    return hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()

def write_json(path, value):
    full = ROOT / path
    full.parent.mkdir(parents=True, exist_ok=True)
    full.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")

def transcribed_review():
    return {
      "schema": "CODEX_TRANSCRIBED_GPT_DIRECTOR_REVIEW_V1",
      "classification": "CODEX_TRANSCRIBED_GPT_UI_READBACK_NOT_GPT_AUTHORED",
      "conversationUrl": "https://chatgpt.com/g/g-p-67f17555a8dc8191a2b5b81e6d8adc12-dungeon-crawler/c/6adc506d-8770-83ea-b64c-0345d9b9b682",
      "transcribedAtUtc": STAMP,
      "reviewedCommit": R2_COMMIT,
      "reviewedPacketPath": R2_PACKET.as_posix(),
      "reviewedPacketSha256": R2_SHA,
      "disposition": "REVISE_ONE_INTEGRITY_ONLY_CORRECTION",
      "verified": {
        "sourceBindings": 20,
        "manifestEntries": 4,
        "proposalAndOwnerAdoptionBindingsMatch": True,
        "branchesStartAtExactT1Final": T1_FINAL,
        "transitionCount": 15,
        "forwardOperationCount": 106,
        "inverseOperationCount": 106,
        "intermediateHashesPass": True,
        "bothBranchesRestoreExactStart": True,
        "C01ReplacementAtMs": 34560012105,
        "C01SettlementAtMs": 34560012106,
        "C01OriginalHistoryAndSunkCostsPreserved": True,
        "C02PickupKnowledgeBeforeCommitmentAndTaggedMemory": True,
        "C03BothReceiptFirstRetriesIndependentlyReproduced": True,
        "retryStateCostsCustodyAndHistoryUnchanged": True,
        "conflictBranchAgeMs": 6006,
        "conflictRejectedBeforeCommitment": True
      },
      "correction": {
        "id": "FR-P05-W-R02-C01",
        "pointer": "/branches/0/targetEvent/stateAtTargetSha256",
        "oldValue": "998e86c42f400b0e82ff270a80a448f7595197890acd25dff9dbf2ac6a7de491",
        "requiredValue": EXPECTED_TARGET_STATE,
        "requiredAction": "Derive stateAtTargetSha256 from the rebuilt compatible pickup transition's afterStateSHA256; assert equality and regenerate dependent packet and manifest hashes.",
        "noSemanticTransitionChangeRequired": True
      },
      "adoptionScopeReadback": "No new adoption is required; correction is an integrity-only binding within the existing Proposal 05 adoption.",
      "queueAndHoldState": {
        "Queue481": "836/12/0",
        "TF192-B02": "OPEN",
        "TF192-B04": "OPEN",
        "EP480": "unsealed",
        "FateRewrite": "unaccepted/unapplied"
      },
      "noCanonRuntimeCampaignSealBlockerOrQueueChange": True
    }

def assert_replay(branch):
    state = copy.deepcopy(branch["branchStartState"])
    assert H.digest(state) == branch["branchStartStateSHA256"], "branch start"
    fwd = inv = 0
    for i, tr in enumerate(branch["transitions"]):
        assert H.digest(state) == tr["beforeStateSHA256"], f"before hash {branch['branchId']}:{i}"
        versions = H.snapshot(state)
        assert all(versions[k] == v for k, v in tr["readSetVersions"].items()), f"read set {i}"
        H.apply(state, tr["forward"])
        fwd += len(tr["forward"])
        assert H.digest(state) == tr["afterStateSHA256"], f"after hash {branch['branchId']}:{i}"
        assert state["overlay"]["nowMs"] == tr["atMs"], f"event time {i}"
        for write in tr["writeSetVersions"]:
            exists, value = H.tryget(state, write["path"])
            assert exists == write["exists"] and (not exists or H.digest(value) == write["sha256"]), f"write version {i}"
    assert H.digest(state) == branch["finalStateSHA256"], "final hash"
    for i, tr in reversed(list(enumerate(branch["transitions"]))):
        H.apply(state, tr["inverse"])
        inv += len(tr["inverse"])
        assert H.digest(state) == tr["beforeStateSHA256"], f"inverse {branch['branchId']}:{i}"
    assert H.digest(state) == branch["branchStartStateSHA256"], "inverse to branch start"
    return fwd, inv

def main():
    r2_raw = gitshow(f"{BASE}:{R2_PACKET.as_posix()}")
    assert sha(r2_raw) == R2_SHA, "R02 packet pin"
    old = json.loads(r2_raw)
    assert old["baseMainCommit"] == "eacd076230175e3f843d14d4d9150c205b4d58d1", "original witness fork base"
    assert old["reviewedProposal"]["sha256"] == P05_SHA, "proposal pin"
    proposal_path = "docs/audit/2026-10-08/full-game/director-spell-review-129/fate_rewrite_ep480_interface_spec_2026-11-02/FATE_REWRITE_EP480_INTERFACE_PROPOSAL_05.json"
    assert sha(gitshow(f"{BASE}:{proposal_path}")) == P05_SHA, "proposal bytes"

    review = transcribed_review()
    write_json(R2_REVISE, review)
    review_raw = (ROOT / R2_REVISE).read_bytes()
    branches = copy.deepcopy(old["branches"])
    pickup_after = branches[0]["transitions"][5]["afterStateSHA256"]
    assert pickup_after == EXPECTED_TARGET_STATE, "Director-provided pickup hash differs from rebuilt transition"
    branches[0]["targetEvent"]["stateAtTargetSha256"] = pickup_after
    assert branches[0]["targetEvent"]["stateAtTargetSha256"] == branches[0]["transitions"][5]["afterStateSHA256"], "target-state binding"

    total_forward = total_inverse = 0
    for branch in branches:
        fwd, inv = assert_replay(branch)
        total_forward += fwd
        total_inverse += inv
        evidence = branch["idempotency"]["executionEvidence"]
        assert evidence["duplicateCallUsedCachedReceipt"] and evidence["retryReturnedSameReceipt"], "retry receipt"
        assert evidence["stateUnchanged"] and evidence["costCustodyAndHistoryUnchanged"], "retry invariance"
    assert total_forward == 106 and total_inverse == 106, "operation counts changed"

    sources = copy.deepcopy(old["sourceBindings"])
    for source in sources:
        raw = gitshow(f"{BASE}:{source['path']}")
        assert len(raw) == source["bytes"] and sha(raw) == source["sha256"], f"inherited source binding {source['path']}"
    sources.extend([
      {"role": "superseded_R02_witness_packet", "path": R2_PACKET.as_posix(), "bytes": len(r2_raw),
       "gitBlobSha1": subprocess.check_output(["git", "rev-parse", f"{BASE}:{R2_PACKET.as_posix()}"], cwd=ROOT, text=True).strip(), "sha256": sha(r2_raw)},
      {"role": "director_REVISE_02_transcription", "path": R2_REVISE.as_posix(), "bytes": len(review_raw),
       "gitBlobSha1": git_blob_sha1(review_raw), "sha256": sha(review_raw)}
    ])
    packet = copy.deepcopy(old)
    packet.update({
      "packetId": "FR-EP480-P05-TESTONLY-WITNESSES-R03-2026-11-03",
      "revisionBaseCommit": BASE,
      "supersedes": {"packetId": old["packetId"], "commit": BASE, "sha256": R2_SHA},
      "directorRevision": {"path": R2_REVISE.as_posix(), "sha256": sha(review_raw), "disposition": "REVISE_ONE_INTEGRITY_ONLY_CORRECTION"},
      "sourceBindings": sources,
      "branches": branches,
      "summary": {"branchCount": 2, "compatibleBranch": branches[0]["branchId"], "conflictBranch": branches[1]["branchId"],
        "transitions": 15, "forwardOperations": total_forward, "inverseOperations": total_inverse,
        "allForwardAndInverseChecksPass": True, "bothInverseToT1Final": True,
        "targetStateHashDerivedFromPickupTransition": True, "sameKeyRetriesExecutedAndVerified": True,
        "spellIdentityAcceptanceOrApplication": False, "queueState": "836/12/0"}
    })
    write_json(R3_PACKET, packet)
    packet_raw = (ROOT / R3_PACKET).read_bytes()
    packet_sha = sha(packet_raw)
    review_sha = sha(review_raw)
    request = f"""# Director evidence review — Fate Rewrite Proposal 05 witnesses, R03

R03 makes one integrity-only correction to R02 and leaves all 15 transitions semantically unchanged. The compatible target-state pointer is now derived from, and asserted equal to, the rebuilt pickup transition's post-state hash.

- Existing owner adoption: {P05}, SHA-256 {P05_SHA}; scope remains the two named TEST_ONLY branches.
- R02 Director review transcription: {R2_REVISE.as_posix()}, SHA-256 {review_sha}.
- R03 packet: {R3_PACKET.as_posix()}, SHA-256 {packet_sha}.
- R03 manifest: {R3_MANIFEST.as_posix()}.

The corrected `/branches/0/targetEvent/stateAtTargetSha256` is `{EXPECTED_TARGET_STATE}` and equals `/branches/0/transitions/5/afterStateSHA256`. The builder asserts that binding, independently replays all 15 transitions and inverses (106 operations each way), and verifies the previously passed retry evidence remains unchanged.

Please return PASS, REVISE, or HOLD bound to the exact main commit and packet hash. No new premise or owner adoption is needed. Keep Queue481 836/12/0, TF192-B02/B04 open, EP480 unsealed, and Fate Rewrite unaccepted/unapplied. No canon, runtime, campaign, seal, blocker, identity, or queue change is requested.
"""
    full_req = ROOT / R3_REQUEST
    full_req.parent.mkdir(parents=True, exist_ok=True)
    full_req.write_text(request, encoding="utf-8", newline="\n")
    manifest_files = []
    for path in (R2_REVISE, R3_PACKET, R3_REQUEST, R3_SCRIPT):
        raw = (ROOT / path).read_bytes()
        manifest_files.append({"path": path.as_posix(), "bytes": len(raw), "sha256": sha(raw)})
    manifest = {
      "schema": "DD_TESTONLY_WITNESS_PACKET_MANIFEST_V1",
      "manifestId": "FR-EP480-P05-TESTONLY-WITNESS-MANIFEST-R03",
      "classification": "TEST_ONLY_STATIC_INTERFACE_WITNESS_CONSTRUCTION",
      "proposal": {"id": P05, "sha256": P05_SHA, "readinessCommit": "08c4e0db03fb3d20db56c01c16af7865110adc85"},
      "ownerAdoptionReceipt": {"path": DIR.joinpath("OWNER_ADOPTION_RECEIPT_FR_EP480_P05.json").as_posix(),
        "sha256": "9d51c3baa42dd300e618a8dca881515d54d3b40e762ccd9eb19773d050025b49",
        "scope": ["FR-EP480-IFACE-COMPAT-01", "FR-EP480-IFACE-CONFLICT-01"]},
      "supersedes": {"packetPath": R2_PACKET.as_posix(), "commit": BASE, "sha256": R2_SHA},
      "baseMainCommit": old["baseMainCommit"], "revisionBaseCommit": BASE, "files": manifest_files,
      "queuePreservation": {"reviewedApplied": 836, "pending": 12, "acceptedUnapplied": 0,
        "nextIdentity": "fate-rewrite", "openBlockers": ["TF192-B02", "TF192-B04"]},
      "constructionStatus": "R03_ONE_HASH_BINDING_CORRECTION_AWAITING_DIRECTOR_REVIEW",
      "semanticTransitionsChanged": False, "targetStateHashDerivedAndAsserted": True,
      "noSealAcceptanceApplicationOrQueueChange": True
    }
    write_json(R3_MANIFEST, manifest)
    for entry in manifest["files"]:
        raw = (ROOT / entry["path"]).read_bytes()
        assert len(raw) == entry["bytes"] and sha(raw) == entry["sha256"], f"manifest {entry['path']}"
    disk = json.loads((ROOT / R3_PACKET).read_text(encoding="utf-8"))
    assert disk["branches"][0]["targetEvent"]["stateAtTargetSha256"] == disk["branches"][0]["transitions"][5]["afterStateSHA256"]
    for branch in disk["branches"]:
        assert_replay(branch)
    print("PASS R03 target-state hash derived from compatible pickup transition=" + EXPECTED_TARGET_STATE)
    print("PASS transitions=15 forward=106 inverse=106; both branches restore T1; retry evidence preserved")
    print("PASS packet SHA-256=" + packet_sha)

if __name__ == "__main__":
    main()
