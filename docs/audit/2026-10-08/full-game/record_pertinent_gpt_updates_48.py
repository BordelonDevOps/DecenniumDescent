"""Preserve newly retrieved owner direction and update navigation without applying mechanics."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json

G = Path(r"C:\Github\DecenniumDescent")
A = G / "docs/audit/2026-10-08/full-game"
R = G / "DescentReviewChanges/ReviewBible"
LEDGER = A / "PERTINENT_GPT_DECISIONS_2026_10_20_01.json"
CHECKPOINT = A / "ACTIVE_AUTHORING_CHECKPOINT_GPT_OWNER_DIRECTION_48.json"
BACKUP = A / "navigation-before-gpt-owner-direction-48"


def bind(path):
    raw = path.read_bytes()
    return {"path": path.relative_to(G).as_posix(), "bytes": len(raw),
            "sha256": hashlib.sha256(raw).hexdigest()}


def save_new(path, value):
    with path.open("x", encoding="utf-8", newline="\n") as output:
        json.dump(value, output, ensure_ascii=False, indent=2)
        output.write("\n")


def main():
    assert not LEDGER.exists() and not CHECKPOINT.exists() and not BACKUP.exists()
    for path in [G / "DescentReviewChanges/AGENTS.md", R / "AGENTS.md",
                 R / "docs/AGENTS.md"]:
        assert not path.exists(), f"Read newly discovered instructions before proceeding: {path}"
    observed = datetime.now(timezone.utc).isoformat()
    native_rules = A / "GPT_PART5_PERTINENT_OWNER_CHOICES_2026_10_20_NATIVE.json"
    native_unity = A / "GPT_UNITY_DEVELOPMENT_SETUP_2026_10_20_NATIVE.json"
    rules = json.loads(native_rules.read_text(encoding="utf-8"))
    unity = json.loads(native_unity.read_text(encoding="utf-8"))
    assert rules["thread"]["title"] == "Calibration Review Part 5"
    assert unity["thread"]["title"] == "Unity Development Setup"
    all_turns = {t["id"]: t for doc in [rules, unity] for t in doc["turns"]}
    direction_turn = all_turns["374b7d9e-41fd-42a4-934e-711ad616b4b9"]
    direction_text = next(i for i in direction_turn["items"] if i["type"] == "userMessage")["content"][0]["text"]
    oversight_turn = all_turns["7c6cc02d-a5b6-4d38-822e-6565dfd8f1be"]
    oversight_text = next(i for i in oversight_turn["items"] if i["type"] == "userMessage")["content"][0]["text"]
    original_index = bind(R / "data/public/spell_playtests/authored_review_index.json")
    original_registry = bind(R / "data/director/spell_review/accepted_interface_registry_06.json")
    assert original_index["sha256"] == "6f9b86e21f6a69c7ba2469aba89d5907aa08da567226a2c4bd3ced9e09409857"
    assert original_registry["sha256"] == "a08f8040c2ad5eaff08668376d15155f926f909c4b63a30461d55449e18aa567"
    helper_paths = [R / ("tools/feat335_copy_" + suffix + ".py")
                    for suffix in ["capture", "release", "payloads", "class_release"]]
    helper_before = [bind(p) for p in helper_paths]
    confirmation = json.loads((A / "GPT_PART5_OWNER_READY_SUCCESSOR_08_NATIVE.json").read_text(encoding="utf-8"))
    assert any(t["id"] == "645d2ea1-1dd1-418f-aae2-4596255253ea" for t in confirmation["turns"])
    assert "Codex checked the owner's latest pertinent discussion" in json.dumps(confirmation)
    ledger = {
        "id": "PERTINENT-GPT-DECISIONS-2026-10-20-01",
        "recordedAtUtc": observed,
        "scope": "Owner direction and review synchronization; no mechanic or engine implementation.",
        "sources": [bind(native_rules), bind(native_unity)],
        "ownerGameDirection": {
            "sourceUserTurn": direction_turn["id"], "verbatim": direction_text,
            "status": "explicit-owner-product-direction",
            "presentation": "SNES-style CRPG",
            "modes": [
                {"id": "exploration", "direction": "Direct control inspired by Secret of Mana, with running, jumping and mapped interactions including exploration, digging, marking, doors and chests."},
                {"id": "tactical", "direction": "Deep CRPG combat; Owlcat is a depth reference, not authority to import its rules."},
                {"id": "resource-management", "direction": "Crafting, research and companion assignments such as fishing, mining and farming."}
            ],
            "scopeCaution": "The owner describes a desired format; the incidental belief that 3D is technically impossible with Codex is not adopted as a technical fact. No existing content or benefit is removed."
        },
        "ongoingAiOversight": {
            "sourceUserTurn": oversight_turn["id"], "verbatim": oversight_text,
            "status": "explicit-owner-development-expectation",
            "workingModel": "Owner directs game design. AI continues engineering assistance, interaction review, debugging, test construction and plain-language reporting. Repository evidence must support future sessions.",
            "notImplied": "No requirement for live model calls to adjudicate every gameplay turn; no guarantee of correctness from AI agreement alone."
        },
        "architectureRecommendations": {
            "status": "gpt-proposals-pending-source-reconciliation-and-implementation",
            "sourceAssistant": "bcb8181f-aad1-4d36-a25f-e3a545c922c8",
            "proposals": [
                "Unity presentation over shared C# state and rules, with exploration, combat and management command layers.",
                "Shared character, inventory, world and scheduling state; animations display resolved outcomes.",
                "Saved companion jobs continue when their presentation unloads.",
                "Validated commands and side-effect-free previews with information visibility preserved.",
                "Prove a connected exploration/combat/assignment/save-load loop using sufficiently reviewed content."
            ],
            "unsettled": [
                "Exact exploration/combat/work time conversion and menu/pause policy.",
                "Movement, jumping, party following and encounter transition policies.",
                "Turn-based-first recommendation, cooperative details and prototype roster/content are not newly owner-approved exact mechanics.",
                "No Unity project inspection, engine implementation, compile or runtime validation occurred in this synchronization."
            ]
        },
        "mechanicalDecisions": [
            {"id": "MASS-SUGGESTION-SHARED-24H", "status": "owner-confirmed-existing-review",
             "userTurn": "f2c4c555-5b8f-4ba7-8264-d4c66fa0d319", "ownerWords": "shared 24 hour",
             "decision": "One shared 24-hour maximum; nonconcentration; no new consumed reagent. Preserve existing RP, components, actual class access, tasks and early endings."},
            {"id": "TRUE-SEEING-CONSISTENT-BENEFITS", "status": "owner-confirmed-existing-review",
             "userTurn": "db7826fc-93d5-4d92-9fca-34ea05a9707f",
             "decision": "Combine the printed perception benefits consistently across legitimate acquisition routes, retaining distinct access and physical occlusion/transformation limits."},
            {"id": "COPY-READY-PREPARATION-ONLY", "status": "owner-delegated-gpt-selection-supersedes-prior-proposal-successor-pending",
             "userTurn": "db7826fc-93d5-4d92-9fca-34ea05a9707f",
             "assistant": "4a85848b-27b8-48ec-8f3a-a852f1f50a0c",
             "decision": "Spend applicable copied-feat and actually owned Mirrorsage allowances on preparation only. Delayed release spends its real Reaction without requiring or spending a second copy allowance for the release round. RP, components and capture permission are paid once; counter/abandon does not refund preparation.",
             "retainedRequirements": ["Real trigger", "Legal targets", "Maintained concentration", "Unexpired hold", "Available Reaction", "All separate action and resource requirements"],
             "scope": "Copied-feat Ready only; no ordinary Ready or unrelated Echo change. It grants no extra actions.",
             "consequence": "A held copy may release during a round with another otherwise lawful copy, including when that round's allowance is already used.",
             "supersedes": "Historical COPY-READY-ALLOWANCE-01 both-touched-round wording in proposed correction archives and affected Control15 references.",
             "historyTreatment": "Keep all original archives and examples unchanged; review exact successors before implementation."},
            {"id": "SOULBURN-GRAND-RESERVOIR", "status": "owner-delegated-gpt-confirmation-of-existing-review",
             "userTurn": "db7826fc-93d5-4d92-9fca-34ea05a9707f",
             "decision": "Retain Soulburn's intrinsic selected 0–3 RP recovery after successful resolution. Grand Reservoir consumes its actual limited use and waives eligible base RP; 20 normal HP is still paid. No general refund-chain permission."}
        ],
        "twoDefectSupplement": bind(A / "COPIED_FEAT_PART5_SUPPLEMENT_02_LOCAL_PREFLIGHT.json"),
        "readySuccessorRequest": bind(A / "GPT_PART5_OWNER_READY_SUCCESSOR_08_REQUEST.txt"),
        "readySuccessorNativeConfirmation": bind(A / "GPT_PART5_OWNER_READY_SUCCESSOR_08_NATIVE.json"),
        "ownerImplementationReservationRetained": True,
        "implementationApplied": False, "sourceInformationDeleted": 0
    }
    save_new(LEDGER, ledger)
    BACKUP.mkdir()
    navigation = [G / "START_HERE.md", R / "docs/DEVELOPMENT_DIRECTION.md"]
    preserved = []
    for path in navigation:
        raw = path.read_bytes()
        backup = BACKUP / path.name
        with backup.open("xb") as output:
            output.write(raw)
        preserved.append(bind(backup))
        prefix = "docs/audit/2026-10-08/full-game/" if path == navigation[0] else "../../../docs/audit/2026-10-08/full-game/"
        notice = (
            "\n**Latest owner direction and GPT synchronization — 20 October 2026:** "
            f"[Checkpoint48]({prefix}{CHECKPOINT.name}) and the "
            f"[source-linked decision ledger]({prefix}{LEDGER.name}) supersede older status statements below. "
            "The owner describes an SNES-style CRPG with direct-control exploration, deep tactical combat, "
            "and companion-driven crafting, research and gathering; ongoing AI engineering and rules oversight "
            "supports the owner as design authority. GPT's shared Unity/C# architecture and connected first "
            "playable loop are proposals. Mass Suggestion has one shared 24-hour maximum without an added "
            "consumed reagent; True Seeing benefits remain consistent across legitimate routes; the scoped "
            "Soulburn/Grand Reservoir recovery is retained. **Copied-feat Ready now uses preparation-round-only "
            "allowances: older both-round wording is superseded and requires an exact reviewed successor.** "
            "GPT has received that reconciliation request. The two-defect supplement is preserved with "
            "156 local integrity/source/text checks; implementation remains reserved. Applied counts remain "
            "525 reviewed/323 pending/249 standalone, with173 interfaces and39 accepted-but-unapplied spells. "
            "Queue39 and the89 ungrouped rank9 identities remain current. All history is retained.\n"
        ).encode("utf-8")
        first_line_end = raw.index(b"\n") + 1
        path.write_bytes(raw[:first_line_end] + notice + raw[first_line_end:])
        assert path.read_bytes().replace(notice, b"", 1) == raw
    assert [bind(p) for p in helper_paths] == helper_before
    assert bind(R / "data/public/spell_playtests/authored_review_index.json") == original_index
    assert bind(R / "data/director/spell_review/accepted_interface_registry_06.json") == original_registry
    checkpoint = {
        "id": "ACTIVE-AUTHORING-GPT-OWNER-DIRECTION-48", "recordedAtUtc": observed,
        "status": "Pertinent Part5 and Unity discussions preserved; owner direction recorded; supplement02 verified; exact preparation-only Ready successor requested.",
        "previousCheckpoint": bind(A / "ACTIVE_AUTHORING_CHECKPOINT_RANK9_PSYCHIC_FEAR_47.json"),
        "decisionLedger": bind(LEDGER),
        "currentWorkQueue": bind(R / "data/director/spell_review/remaining_work_queue_39.json"),
        "currentAuthoredIndex": original_index, "currentAcceptedInterfaceRegistry": original_registry,
        "authoredCounts": {"reviewed": 525, "pending": 323, "standalone": 249, "total": 848},
        "acceptedButUnapplied": 39, "preparedGroupCount": 37,
        "groupedPendingIdentities": 234, "ungroupedPendingIdentities": 89,
        "supplement02Receipt": bind(A / "COPIED_FEAT_PART5_SUPPLEMENT_02_LOCAL_PREFLIGHT.json"),
        "activeGptReviewAtLastVerifiedObservation": {
            "threadId": rules["thread"]["id"], "title": rules["thread"]["title"],
            "userTurn": "645d2ea1-1dd1-418f-aae2-4596255253ea",
            "nativeConfirmation": bind(A / "GPT_PART5_OWNER_READY_SUCCESSOR_08_NATIVE.json"),
            "scope": "Exact proposed successor for preparation-round-only copied-feat Ready.",
            "sent": True, "completedResponseReceived": False
        },
        "nextAction": "Receive and verify the narrow Ready successor; keep implementation reserved. Then continue already-delivered Rank8Damage6/Rank7IdentityCasting5 and remaining source preparation, carrying forward the owner's three-mode product direction.",
        "navigation": [bind(p) for p in navigation], "preservedNavigation": preserved,
        "canonicalHelperBaselinesUnchanged": helper_before,
        "latestPreviouslyVerifiedGitHubBackup": {"commit": "ccb9047a76e9807250feee6d72285c268957d20b", "throughCheckpoint": 46},
        "laterLocalWork": "Checkpoints47–48 and associated evidence have not been pushed in this turn.",
        "lastUsageObservation": {"usedPercent": 3, "remainingPercent": 97, "stopAtRemainingPercent": 20},
        "ownerImplementationReservationRetained": True, "implementationApplied": False,
        "downloadedCodeExecuted": False, "runtimeTestsExecuted": 0,
        "all75DomainGatesUnchanged": True, "wholeGameComplete": False,
        "sourceInformationDeleted": 0
    }
    save_new(CHECKPOINT, checkpoint)
    print(json.dumps({"checkpoint": bind(CHECKPOINT), "ledger": bind(LEDGER),
                      "navigationUpdated": len(navigation), "canonicalFilesUnchanged": 6}))


if __name__ == "__main__":
    main()
