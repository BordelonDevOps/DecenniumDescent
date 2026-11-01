from __future__ import annotations

import hashlib
import json
import zlib
from pathlib import Path

ROOT = Path(__file__).resolve().parent
BASE = "https://github.com/BordelonDevOps/DecenniumDescent/blob/main/docs/audit/2026-10-08/full-game/director-spell-review-129"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def dump(path: Path, data: object) -> None:
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def artifact(path: str, label: str) -> str:
    return f"[{label}]({BASE}/{path})"


def main() -> None:
    queue_old_path = ROOT / "CURRENT_SPELL_QUEUE_428_REPACK02.json"
    handoff_old_path = ROOT / "CURRENT_HANDOFF_428_REPACK02.json"
    readback_md = ROOT / "DIRECTOR_READBACK_428_REPACK02.md"
    readback_json = ROOT / "DIRECTOR_READBACK_428_REPACK02.json"
    status_readback_md = ROOT / "DIRECTOR_STATUS_READBACK_451.md"
    status_readback_json = ROOT / "DIRECTOR_STATUS_READBACK_451.json"
    queue_path = ROOT / "CURRENT_SPELL_QUEUE_451_REPACK01.json"
    handoff_path = ROOT / "CURRENT_HANDOFF_451_REPACK01.json"
    packet_path = ROOT / "CURRENT_REVIEW_PACKET_451_REPACK01.md"

    ruling = """PASS for W01 overlay sufficiency and corrected W09 witness sufficiency. No remaining correction in these two components. Fortress is not yet ready for whole-identity acceptance.

Reviewed current main at c6cf8bfec83e63bafe109b389e8e2a63bf7b9c68.

Artifact integrity — PASS. All four supplied SHA-256 values match. W01 ZIP: 431,737 bytes, 22 members, all 21 manifest payload hashes and CRCs pass. W09 ZIP: 829,235 bytes, 21 members, all 20 payload hashes and CRCs pass.

Source/adoption bindings — PASS. W01’s 12 bindings and W09’s 11 bindings resolve to the supplied exact bytes. Adoption424 covers only the two W01 overlays; Adoption427 binds the exact W09 proposal for hypothetical construction only.

W01 support overlay — PASS within adopted scope. All 2,660 structural nodes reach origin-ground-face through 4,851 structural joints. The 53 leaf attachments do not support the building. The 4,904 total connections are not all structural joints.

W01 usable volume — PASS within adopted scope. All 54 routes / 1,586 positions fit the adopted z-max 46 ft. Structure and roof remain 40 ft; no new floor, platform, support edge or historical coordinate is introduced.

W09 replay and C01 — PASS. Exact replay hash 173d1decaaa2d706f4266261600aba15bbc6eb01cf90628dd2b83e124a09f48a; 146 events, 1,715 forward operations and 1,715 inverse operations, with complete reverse restoration. All seven corrected support states pass.

W09 movement/attacks — PASS. The ordered tile reposition, 100-foot movement expenditure, carry/strike sweeps and 12 attacks match the adopted terms. Independent checks found no positive-volume structural intersections in the checked sweeps.

W09 support loss/fall — PASS. At 102.1, the target reaches zero HP, exactly 18 dependent stair parts are destroyed, and A’s support clears. All 128 regular markers are preserved. A’s END at 108.9 precedes landing; support returns on tread/riser 1 after 4 feet, with zero damage and no damage-triggered Prone.

The 55-HP historical south panel, tile identity/custody and 3606.13 expiry, actor HP/RP, and unchanged parent remain preserved. This is structural-collapse settlement—not whole-Fortress closure or evacuation.

The existing W01 transport qualification also remains: its readback’s final CRLF differs from the Git LF bytes; the documented normalization reproduces the exact Git source. No correction is needed.

Whole-identity status: conjure-demiplane-fortress remains HELD under PG200-B06. These passes do not complete the outstanding W05, W10, W11, W12 and W13 integrations. Preserve W04’s completed component disposition and all other prior passes/seals; W13-446’s correction list remains outstanding.

No seal, acceptance, application, campaign occurrence, canonical change or queue mutation is issued. Authority remains 830 applied / 18 pending / 0 accepted-unapplied. Fortress remains first priority; Elemental Shell follows it."""
    readback_md.write_text("# GPT Director readback — W01 overlays 425 and W09 witness 428\n\n" + ruling + "\n", encoding="utf-8")

    packet_old = queue_old_path
    raw_old = packet_old.read_bytes()
    queue = json.loads(raw_old)
    handoff = json.loads(handoff_old_path.read_text(encoding="utf-8"))
    w05_dir = ROOT / "fortress_w05_w10_joint_witness_451"
    w11_dir = ROOT / "fortress_w11_cargo_owner_proposal_438"
    w12_dir = ROOT / "fortress_w12_reversion_owner_proposal_445"
    w13_dir = ROOT / "fortress_w13_nested_space_owner_proposal_447"

    components = [
        {
            "component": "PG328-W05 + PG328-W10",
            "witnessPath": rel(w05_dir / "W05_W10_WITNESS_451_TESTONLY.json"),
            "witnessSha256": sha(w05_dir / "W05_W10_WITNESS_451_TESTONLY.json"),
            "archivePath": rel(w05_dir / "DD_Fortress_W05_W10_Witness_451_TESTONLY.zip"),
            "archiveSha256": sha(w05_dir / "DD_Fortress_W05_W10_Witness_451_TESTONLY.zip"),
            "validationPath": rel(w05_dir / "BUILD_VALIDATION_451.json"),
            "validationSha256": sha(w05_dir / "BUILD_VALIDATION_451.json"),
        },
        {
            "component": "PG328-W11",
            "witnessPath": rel(w11_dir / "W11_WITNESS_449_TESTONLY.json"),
            "witnessSha256": sha(w11_dir / "W11_WITNESS_449_TESTONLY.json"),
            "validationPath": rel(w11_dir / "BUILD_VALIDATION_449.json"),
            "validationSha256": sha(w11_dir / "BUILD_VALIDATION_449.json"),
        },
        {
            "component": "PG328-W12",
            "witnessPath": rel(w12_dir / "W12_WITNESS_450_TESTONLY.json"),
            "witnessSha256": sha(w12_dir / "W12_WITNESS_450_TESTONLY.json"),
            "validationPath": rel(w12_dir / "BUILD_VALIDATION_450.json"),
            "validationSha256": sha(w12_dir / "BUILD_VALIDATION_450.json"),
        },
    ]
    w13 = {
        "proposalPath": rel(w13_dir / "PG328_W13_NESTED_SPACE_OWNER_PROPOSAL_447_TESTONLY.json"),
        "proposalSha256": sha(w13_dir / "PG328_W13_NESTED_SPACE_OWNER_PROPOSAL_447_TESTONLY.json"),
        "markdownPath": rel(w13_dir / "PG328_W13_NESTED_SPACE_OWNER_PROPOSAL_447_TESTONLY.md"),
        "markdownSha256": sha(w13_dir / "PG328_W13_NESTED_SPACE_OWNER_PROPOSAL_447_TESTONLY.md"),
        "validationPath": rel(w13_dir / "BUILD_VALIDATION_447.json"),
        "validationSha256": sha(w13_dir / "BUILD_VALIDATION_447.json"),
        "status": "CORRECTIONS_446_APPLIED; READY_FOR_DIRECTOR_READINESS_REVIEW; NOT_OWNER_ADOPTED",
    }
    priority_order = [
        "conjure-demiplane-fortress", "elemental-shell", "final-word", "summon-avatar-of-decay",
        "reverse-gravity-field", "eternal-prophecy", "fate-rewrite", "collapse-timeline",
        "faction-omniscience-supreme", "alignment-ascension", "alignment-perfection",
        "faction-incarnate", "faction-perfection", "corruption-purification", "astral-projection",
        "imprisonment", "divine-intervention-greater", "wish",
    ]
    status_text = """Authority remains 830 applied / 18 pending / 0 accepted-unapplied, with zero first-review tasks.

The complete continuing priority order is: conjure-demiplane-fortress, elemental-shell, final-word, summon-avatar-of-decay, reverse-gravity-field, eternal-prophecy, fate-rewrite, collapse-timeline, faction-omniscience-supreme, alignment-ascension, alignment-perfection, faction-incarnate, faction-perfection, corruption-purification, astral-projection, imprisonment, divine-intervention-greater, wish.

Next required action is the focused review of existing W05/W10 witness 451, followed by W11 witness 449 and W12 witness 450. These are built submissions awaiting disposition—not requests to reconstruct them. Their sufficiency has not been established by this message.

W13 still requires the consolidated W13-446-C01–C05 corrections and source-pointer correction, then exact owner adoption before witness construction.

Preserve W01-425 and W09-428 as PASS for component sufficiency, along with W04 and all other previously completed components. They need no repeated unchanged review. Once the remaining integrations pass, reconcile W01–W13 for a separate explicit Fortress identity decision.

Fortress remains HELD under PG200-B06. No seal, identity acceptance/application, canonical change or queue change occurs here."""
    status_readback_md.write_text("# GPT Director status readback — continuation priority\n\n" + status_text + "\n", encoding="utf-8")
    status_readback_obj = {
        "id": "DIRECTOR-STATUS-READBACK-451",
        "source": "GPT Director, Calibration review part 6",
        "firstReviewTasksRemaining": 0,
        "continuingPriorityOrder": priority_order,
        "nextRequiredComponentReviews": ["W05/W10 witness 451", "W11 witness 449", "W12 witness 450"],
        "W13": "W13-446-C01-C05 and source-pointer corrections are required, then exact owner adoption before witness construction.",
        "preservePassedComponents": ["W01-425", "W09-428", "W04"],
        "wholeFortressDisposition": "HELD_UNDER_PG200-B06",
        "queueAuthority": {"reviewedApplied": 830, "pending": 18, "acceptedUnapplied": 0},
        "identityAcceptanceOrApplication": False,
        "canonicalChanged": False,
        "queueChanged": False,
    }
    dump(status_readback_json, status_readback_obj)

    readback_obj = {
        "id": "DIRECTOR-READBACK-W01-425-W09-428-REPACK02",
        "source": "GPT Director, Calibration review part 6",
        "reviewedMainCommit": "c6cf8bfec83e63bafe109b389e8e2a63bf7b9c68",
        "reviewedPacket": {
            "path": "CURRENT_REVIEW_PACKET_428_REPACK02.md",
            "sha256": sha(ROOT / "CURRENT_REVIEW_PACKET_428_REPACK02.md"),
        },
        "readbackMarkdownPath": rel(readback_md),
        "readbackMarkdownSha256": sha(readback_md),
        "statusReadbackPath": str(status_readback_md.relative_to(ROOT).as_posix()),
        "statusReadbackSha256": sha(status_readback_md),
        "componentDisposition": {
            "W01SuccessorOverlays425": "PASS_WITHIN_ADOPTED_SCOPE",
            "W09CorrectedWitness428": "PASS_TEST_ONLY_UNSEALED",
            "FortressIdentity": "HELD_UNDER_PG200-B06",
        },
        "verified": {
            "W01SourceBindings": 12,
            "W09SourceBindings": 11,
            "W01StructuralNodes": 2660,
            "W01StructuralJoints": 4851,
            "W01LeafAttachmentsNotStructuralSupport": 53,
            "W01UsableRoutes": 54,
            "W01UsablePositions": 1586,
            "W09Events": 146,
            "W09ForwardOperations": 1715,
            "W09InverseOperations": 1715,
            "W09RegularMarkers": 128,
            "W09DestroyedDependentStairParts": 18,
        },
        "identityAcceptanceOrApplication": False,
        "witnessSealed": False,
        "canonicalChanged": False,
        "queueChanged": False,
        "queueAuthority": {"reviewedApplied": 830, "pending": 18, "acceptedUnapplied": 0},
        "nextIdentity": "conjure-demiplane-fortress",
        "followingIdentity": "elemental-shell",
        "remainingIntegrations": ["W05", "W10", "W11", "W12", "W13"],
    }
    dump(readback_json, readback_obj)

    packet_md = f"""# Director review packet — W05/W10 witness 451

GPT Director passed W01 overlays 425 and W09 witness 428. The exact readback is {artifact('DIRECTOR_READBACK_428_REPACK02.md', 'here')} and its structured receipt is {artifact('DIRECTOR_READBACK_428_REPACK02.json', 'here')}. The Director’s sequence is captured in the {artifact('DIRECTOR_STATUS_READBACK_451.md', 'status readback')}. Fortress remains held under PG200-B06; current queue authority remains **830 applied / 18 pending / 0 accepted-unapplied**.

## Focused review request

### W05 and W10 joint witness 451

- {artifact('fortress_w05_w10_joint_witness_451/W05_W10_WITNESS_451_TESTONLY.json', 'Witness JSON')} — SHA-256 `{components[0]['witnessSha256']}`.
- {artifact('fortress_w05_w10_joint_witness_451/DD_Fortress_W05_W10_Witness_451_TESTONLY.zip', 'Review ZIP')} — SHA-256 `{components[0]['archiveSha256']}`.
- {artifact('fortress_w05_w10_joint_witness_451/BUILD_VALIDATION_451.json', 'Verifier result')} — 12 build checks; see the package verifier for 17 independent checks.
- {artifact('fortress_w05_w10_joint_preflight_443/PG328_W05_W10_JOINT_PROPOSAL_443_TESTONLY.json', 'Exact adopted proposal 443')} — SHA-256 `1fd045800181958d34e141763e07fe230a2261a3879e8115869551c2a6d20b85`.
- {artifact('fortress_w05_w10_joint_preflight_443/OWNER_PG328_W05_W10_ADOPTION_443_TESTONLY.json', 'Owner adoption record')}.

Return separate W05 and W10 pass/hold dispositions. Verify the exact parent and adopted terms, bolt/wound/death sequence, 18.1 focus set-down, custody, and conditional Q27 terminal projection. The package asserts no extra resolution timestamp for the final Dispel and remains TEST_ONLY/unsealed.

## Boundaries and requested response

Please review this witness only and return precise separate W05/W10 findings plus any consolidated exact corrections. This is the next item in the Director’s stated order; W11/449 and W12/450 follow. W13-447 remains a later readiness review after the W05/W10, W11 and W12 witness dispositions. Say whether this witness passes component sufficiency; do not accept/apply the whole Fortress identity. W01/425 and W09/428 already passed and need no repeated unchanged review. Do not infer campaign events, canon changes, application or queue mutation. Preserve the existing W04 disposition and other prior passes/seals. Authority remains **830 / 18 / 0**.

The source queue and handoff are {artifact('CURRENT_SPELL_QUEUE_451_REPACK01.json', 'queue')} and {artifact('CURRENT_HANDOFF_451_REPACK01.json', 'handoff')}.
"""
    packet_path.write_text(packet_md, encoding="utf-8")

    queue["id"] = "CURRENT-SPELL-QUEUE-451-REPACK01"
    queue["supersedesQueue"] = {
        "path": queue_old_path.name,
        "bytes": len(raw_old),
        "sha256": sha(queue_old_path),
        "crc32": f"{zlib.crc32(raw_old) & 0xffffffff:08x}",
    }
    queue["currentHandoffPath"] = rel(handoff_path)
    queue["currentDirectorReadback"] = {
        "path": rel(readback_json),
        "sha256": sha(readback_json),
        "W01": "PASS_WITHIN_ADOPTED_SCOPE",
        "W09": "PASS_TEST_ONLY_UNSEALED",
        "wholeFortress": "HELD_UNDER_PG200-B06",
    }
    queue["currentDirectorStatusReadback"] = {
        "path": rel(status_readback_json),
        "sha256": sha(status_readback_json),
        "firstReviewTasksRemaining": 0,
        "nextRequiredComponentReviews": status_readback_obj["nextRequiredComponentReviews"],
    }
    queue["reviewedComponents"] = ["W01 overlays 425", "W09 corrected witness 428"]
    queue["currentReviewPacket"] = {
        "requestPath": rel(packet_path),
        "classification": "FOCUSED_TEST_ONLY_COMPONENT_REVIEW",
        "witnesses": [components[0]],
        "nextReviewOrder": ["W11 witness 449", "W12 witness 450", "W13 proposal 447 readiness"],
        "W01W09DirectorReadbackPath": rel(readback_json),
        "queueAuthority": {"reviewedApplied": 830, "pending": 18, "acceptedUnapplied": 0},
        "sealOrAcceptanceInferred": False,
    }
    dump(queue_path, queue)

    handoff["id"] = "CURRENT-HANDOFF-451-REPACK01"
    handoff["supersedes"] = rel(handoff_old_path)
    handoff["queue"] = {
        "path": rel(queue_path),
        "bytes": queue_path.stat().st_size,
        "sha256": sha(queue_path),
        "crc32": f"{zlib.crc32(queue_path.read_bytes()) & 0xffffffff:08x}",
    }
    handoff["nextStep"] = "GPT Director: focused review of adopted W05/W10 witness 451 only. If those components pass, review W11 witness 449, then W12 witness 450; next confirm W13-447 readiness for owner adoption. W01-425 and W09-428 have passed component review but do not complete whole-Fortress acceptance. Return precise pass/hold findings. Preserve queue authority 830/18/0; do not infer a seal, campaign event, canon change, identity acceptance or application. After Fortress is accepted and applied, continue with Elemental Shell, then the remaining queue priority order."
    handoff["DirectorReadbackW01W09"] = queue["currentDirectorReadback"]
    handoff["DirectorStatusReadback"] = queue["currentDirectorStatusReadback"]
    handoff["W01SuccessorOverlays"]["directorStatus"] = "PASS_WITHIN_ADOPTED_SCOPE"
    handoff["W09Witness"]["directorStatus"] = "PASS_TEST_ONLY_UNSEALED"
    handoff["componentDisposition"] = {
        "W01-425": "PASS_WITHIN_ADOPTED_SCOPE",
        "W09-428": "PASS_TEST_ONLY_UNSEALED",
        "wholeFortress": "HELD_UNDER_PG200-B06",
    }
    handoff["NextComponentReviews"] = {
        "W05W10": {"witnessPath": components[0]["witnessPath"], "witnessSha256": components[0]["witnessSha256"], "status": "TEST_ONLY_UNSEALED_PENDING_DIRECTOR_REVIEW"},
        "W11": {"witnessPath": components[1]["witnessPath"], "witnessSha256": components[1]["witnessSha256"], "status": "TEST_ONLY_UNSEALED_PENDING_DIRECTOR_REVIEW"},
        "W12": {"witnessPath": components[2]["witnessPath"], "witnessSha256": components[2]["witnessSha256"], "status": "TEST_ONLY_UNSEALED_PENDING_DIRECTOR_REVIEW"},
        "W13": {"proposalPath": w13["proposalPath"], "proposalSha256": w13["proposalSha256"], "status": w13["status"]},
    }
    handoff["repackNote"] = "Director PASS recorded for W01-425 and W09-428. Whole Fortress identity remains held under PG200-B06. This repack updates the next review pointers only; authority, identity dispositions, pending IDs and application state are unchanged."
    dump(handoff_path, handoff)
    print(json.dumps({
        "queueSha256": sha(queue_path),
        "handoffSha256": sha(handoff_path),
        "readbackSha256": sha(readback_json),
        "packetSha256": sha(packet_path),
        "authority": queue["currentAuthority"],
        "witnesses": components,
        "w13": w13,
    }, indent=2))


if __name__ == "__main__":
    main()
