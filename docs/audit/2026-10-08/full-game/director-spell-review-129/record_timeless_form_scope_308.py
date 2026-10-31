from __future__ import annotations

import datetime as dt
import hashlib
import json
import pathlib
import zlib

ROOT = pathlib.Path.cwd()
A = ROOT / "docs/audit/2026-10-08/full-game/director-spell-review-129"

def bind(path: pathlib.Path):
    b = path.read_bytes()
    return {"path": path.relative_to(ROOT).as_posix(), "bytes": len(b), "sha256": hashlib.sha256(b).hexdigest(), "crc32": f"{zlib.crc32(b) & 0xffffffff:08x}"}

def main():
    stamp = dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")
    obj = {
        "id": "TIMELESS-FORM-DIRECTOR-SCOPE-308", "recordedAtUtc": stamp,
        "source": {"service": "ChatGPT", "conversationTitle": "Calibration review part 6", "url": "https://chatgpt.com/g/g-p-67f17555a8dc8191a2b5b81e6d8adc12-dungeon-crawler/c/6adc506d-8770-83ea-b64c-0345d9b9b682"},
        "receiptCorrectionConfirmed": True,
        "correctedElementalShellReceipt": bind(A / "ELEMENTAL_SHELL_PACKET_306_SUBMISSION_RECEIPT_CORRECTED_307.json"),
        "currentAuthority": {"reviewedApplied": 822, "pending": 26, "acceptedUnapplied": 0, "completeStandaloneProcedures": 546, "scopedInterfaces": 173},
        "scope": {"ids": ["timeless-form"], "blockers": ["DF218-B03"], "acceptedIds": [], "appliedIds": []},
        "minimumClosureEvidence": [
            {"requirement": "Accepted operational Time Stop procedure", "details": "Exact procedure with source and acceptance bindings; defines activation, costs, eligible actors, affected/excluded entities, permitted actions, and native chronology. Printed access, an immunity flag, or 'take three turns' wording alone is insufficient."},
            {"requirement": "Legally acquired caster and complete activation history", "details": "Class/repertoire/preparation, components, resources, Action and interruption accounting, actual target/area geometry, and relevant prior effects."},
            {"requirement": "Complete joint encounter", "details": "A lawfully established Timeless Form encounters that Time Stop. Demonstrate promised exclusion using Time Stop's actual permissions and clock. Preserve ordinary turns, recharge, Reaction, Ready, concentration, resources, and original deadlines; invent no extra opportunities or paused clocks."}
        ],
        "unresolvedHistoricalRecord": {"path": "history/Return218/preserved_cases/RANK9DEFENSEFORM8129-TIMELESS-FORM-B.json", "pointer": "/events/4", "status": "Time-Stop-access/procedure-held; not a positive interaction"},
        "compactPacketScope": {
            "refreshSourceInventory": 87,
            "preserveCases": 11,
            "preserveRules": ["DF9-Q01", "DF9-Q20", "DF9-Q21", "DF9-Q22", "DF9-Q26", "DEF129-ADD02", "DF186-FUTURE-09"],
            "classAccess": {"classes": ["Druid", "Mage", "Wizard"], "school": "Transmutation", "rank": 9, "minimumClassLevel": 17, "baseRpCost": 26, "casting": "Action/V/S/F", "nativeRangeFeet": 120},
            "selectedProcedure": "willing recipient, nonconcentration, 60 seconds",
            "preserveHasteSlowSuppressionEndingLiabilitiesAndSpentBudgetHistory": True,
            "aging": "Retain DF218-Q-AGING as a conditional qualification, not another whole-spell blocker.",
            "retainAllSourceAccessAndDownstreamQualifications": True,
        },
        "explicitBoundaries": ["No DF218 obligation revision.", "Time Stop remains pending in supplied authority.", "External-provider revisions for Mind Collapse, Absolute Domination, Mass Phantom Killer, and Weird do not automatically satisfy this named Time Stop interaction.", "If no qualifying procedure is available, provide a concise dependency assessment; do not manufacture a positive trace."],
        "remainingSequence": ["timeless-form", "invulnerable-sphere", "nullification-wave", "reality-anchor", "time-stop", "fate-rewrite", "collapse-timeline", "eternal-prophecy", "faction-omniscience-supreme", "banishment-gate", "conjure-demiplane-fortress", "summon-elemental-avatar", "summon-herald-of-the-planes", "summon-avatar-of-decay", "reverse-gravity-field", "alignment-ascension", "alignment-perfection", "faction-incarnate", "faction-perfection", "corruption-purification", "astral-projection", "imprisonment", "divine-intervention-greater", "wish"],
        "separateHolds": ["final-word", "elemental-shell"], "pendingTotal": 26, "firstReviewTasksRemaining": 0,
        "canonicalFilesChangedByThisClarification": False,
    }
    path = A / "TIMELESS_FORM_DIRECTOR_REQUIREMENTS_308.json"
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"status": "PASS", "requirements": bind(path), "scope": obj["scope"], "pendingTotal": obj["pendingTotal"]}, indent=2))

if __name__ == "__main__":
    main()
