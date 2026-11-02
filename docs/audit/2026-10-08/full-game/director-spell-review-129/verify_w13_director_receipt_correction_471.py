#!/usr/bin/env python3
"""Validate the narrow GPT correction to the W13-471 adopted-proposal fields."""
import hashlib
import json
from pathlib import Path

BASE = Path(__file__).resolve().parent
PKG = BASE / "fortress_w13_director_receipt_correction_471_repack01"
OLD = BASE / "fortress_w13_nested_space_witness_471/DIRECTOR_READBACK_471.json"
PROPOSAL = BASE / "fortress_w13_nested_space_owner_proposal_448/PG328_W13_NESTED_SPACE_OWNER_PROPOSAL_448_TESTONLY.json"
ADOPTION = BASE / "fortress_w13_nested_space_owner_proposal_448/OWNER_PG328_W13_ADOPTION_448_TESTONLY.json"
WITNESS = BASE / "fortress_w13_nested_space_witness_471/W13_WITNESS_471_TESTONLY.json"
TRACE = BASE / "fortress_w13_nested_space_witness_471/W13_LIFECYCLE_TRACE_471.json"
ARCHIVE = BASE / "fortress_w13_nested_space_witness_471/DD_Fortress_W13_Reversible_Witness_471_TESTONLY.zip"
QUEUE = BASE / "CURRENT_SPELL_QUEUE_476_REPACK01.json"
CORRECTION = PKG / "DIRECTOR_READBACK_471_REPACK01_CORRECTION.json"


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def main():
    old = read(OLD)
    correction = read(CORRECTION)
    queue = read(QUEUE)
    assert sha(OLD) == correction["correctsReceipt"]["sha256"] == "71237a7bc6cc94ebaa2faf06cec8c65ecfe9f4f389b5e52a46328c16aad663d9"
    assert old["reviewedPacket"]["adoptedProposalId"] == "OWNER-PG328-W13-SUPPORT-426-REPACK01-TESTONLY-PROPOSAL"
    assert old["reviewedPacket"]["adoptedProposalSha256"] == "f4dfbf3403c63f603ef188be972c4425cc627309d4fb77cc86934afecd6b8a9d"
    assert sha(PROPOSAL) == correction["correctedFields"]["/reviewedPacket/adoptedProposalSha256"]
    assert sha(ADOPTION) == correction["ownerAdoptionSha256"]
    assert sha(WITNESS) == correction["reviewedPacket"]["witnessSha256"]
    assert sha(TRACE) == correction["reviewedPacket"]["traceSha256"]
    assert sha(ARCHIVE) == correction["reviewedPacket"]["archiveSha256"]
    assert correction["correctedFields"]["/reviewedPacket/adoptedProposalId"] == "PG328-W13-NESTED-SPACE-OWNER-PROPOSAL-448"
    assert correction["remainingComponentCorrections"] == []
    assert correction["priorReplayFindingsPreserved"] == {"events": 47, "forwardOperations": 526, "inverseOperations": 526, "restoresExactS030": True}
    assert correction["decisionBoundary"] == {"sealed": False, "newIdentityDecision": False, "applicationPerformed": False, "canonicalChange": False, "queueChange": False, "campaignClaim": False}
    assert queue["currentAuthority"] == {"reviewedApplied": 831, "pending": 17, "acceptedUnapplied": 0, "completeStandaloneProcedures": 555, "scopedInterfaces": 173}
    assert correction["authority"]["receiptTimeSnapshot"]["reviewedApplied"] == 830
    assert correction["authority"]["receiptTimeSnapshot"]["pending"] == 18
    assert correction["authority"]["currentSnapshot"]["reviewedApplied"] == 831
    assert correction["authority"]["currentSnapshot"]["pending"] == 17
    assert correction["authority"]["currentSnapshot"]["queueSha256"] == sha(QUEUE)
    assert correction["authority"]["currentSnapshot"]["Fortress"] == "ACCEPTED_APPLIED_STATIC_AUTHORED_REVIEW_ONLY"
    print("PASS: original receipt preserved; exact Proposal448/adoption, witness, trace, archive, replay, scope and current queue bindings verified.")


if __name__ == "__main__":
    main()
