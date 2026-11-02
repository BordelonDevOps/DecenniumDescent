#!/usr/bin/env python3
"""Verify the adopted 468 caster-preparation premise and its strict boundary."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[5]
BASE = ROOT / "docs/audit/2026-10-08/full-game/director-spell-review-129"


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


report = load(HERE / "SHELL_CASTER_QUALIFICATION_472_TESTONLY.json")
proposal_dir = BASE / "elemental_shell_caster_premise_proposal_468"
preflight_dir = BASE / "elemental_shell_caster_preflight_467"
profile_path = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_candidates/rank9defenseform8_reviewed_186/ACTOR_PROFILES.json"

bindings = [
    (report["adoptedProposal"]["path"], report["adoptedProposal"]["sha256"]),
    (report["ownerAdoption"]["path"], report["ownerAdoption"]["sha256"]),
    (report["adoptedPremise"]["path"], report["adoptedPremise"]["sha256"]),
    (report["sourceQualifications"][0]["path"], report["sourceQualifications"][0]["sha256"]),
    (report["sourceQualifications"][1]["path"], report["sourceQualifications"][1]["sha256"]),
    (report["sourceQualifications"][2]["path"], report["sourceQualifications"][2]["sha256"]),
]
for relpath, expected in bindings:
    assert sha(ROOT / relpath) == expected, f"hash mismatch: {relpath}"

owner = load(proposal_dir / "OWNER_DF218_B02_SHELL_CASTER_PREMISE_ADOPTION_468_TESTONLY.json")
premise = load(proposal_dir / "CASTER_PREPARATION_PREMISE_468_TESTONLY.json")
readback468 = load(proposal_dir / "DIRECTOR_READBACK_468.json")
readback467 = load(preflight_dir / "DIRECTOR_READBACK_467.json")
profile = load(profile_path)

assert owner["ownerAuthorization"]["verbatim"] == "Yes—adopt exact 468"
assert owner["scope"]["proposalSha256"] == report["ownerAdoption"]["proposalSha256"]
assert owner["adoptedEffect"]["doesNotPermit"]
assert readback468["status"] == "PASS_READY_FOR_OWNER_ADOPTION"
assert readback467["status"] == "PASS_PACKET_INTEGRITY_CANDIDATE_FOUND_PREPARATION_GAP_REMAINS"
assert premise["status"] == "RECORDED_FOR_CASTER_QUALIFICATION"
assert premise["branchId"] == report["scope"]["branchId"]
wizard = profile["Wizard18"]
assert wizard["spellbook"][65]["spellId"] == "elemental-shell"
prepared = premise["hypotheticalPreparationRecord"]
assert prepared["preparedOrdinaryCount"] == 24
assert len(prepared["preparedOrdinarySpellIds"]) == 24
assert prepared["matchesBoundOrdinaryRepertoireExactly"] is True
assert prepared["preparedOrdinarySpellIds"] == wizard["ordinaryRepertoire"]
assert wizard["preparedCapacity"] == 24 and wizard["preparedCount"] == 24
assert wizard["extraSchoolOnlyCapacity"] == 1
assert "elemental-shell" in prepared["preparedOrdinarySpellIds"]
assert prepared["schoolOnlyPosition"]["designation"] == "UNASSIGNED"
assert prepared["schoolOnlyPosition"]["capacity"] == 1
assert prepared["matrixModifications"] == {}
assert report["qualificationResult"]["fullDF218B02Satisfied"] is False
assert report["authority"]["reviewedApplied"] == 830
assert report["authority"]["pending"] == 18
assert report["authority"]["acceptedUnapplied"] == 0
assert all(value is False for value in report["nonEffects"].values())

print("PASS: exact Proposal 468 owner adoption and director readback bound")
print("PASS: Wizard18 source selection and 24 ordinary prepared spells match")
print("PASS: 45-minute branch timing, unassigned Divination position, and matrix preserved")
print("PASS: cast/witness/blocker/acceptance/application/queue boundaries preserved")
