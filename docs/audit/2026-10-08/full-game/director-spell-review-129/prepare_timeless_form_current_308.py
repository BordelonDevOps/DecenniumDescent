from pathlib import Path
import json

HERE = Path(__file__).resolve().parent
TEMPLATE = HERE / "prepare_defenseform8_current_236.py"
BASE = HERE
source = TEMPLATE.read_text(encoding="utf-8")

# Rebase the independently audited source/case builder to 822/26 and this packet number.
for old, new in (("236", "308"), ("811", "822"), ("37", "26"), ("535", "546")):
    if old not in source:
        raise RuntimeError(f"Expected rebase token is absent: {old}")
    source = source.replace(old, new)
source = source.replace('qpath = BASE / "CURRENT_SPELL_QUEUE_308.json"', 'qpath = BASE / "CURRENT_SPELL_QUEUE_307.json"')
source = source.replace('hpath = BASE / "CURRENT_HANDOFF_308.json"', 'hpath = BASE / "CURRENT_HANDOFF_307.json"')
source = source.replace('ppath = BASE / "CURRENT26_PENDING_IDENTITY_AUDIT_308.json"', 'ppath = BASE / "CURRENT26_PENDING_IDENTITY_AUDIT_307.json"')
source = source.replace('BASE / "CURRENT_SPELL_REVIEW_SNAPSHOT_308.md"', 'BASE / "CURRENT_SPELL_REVIEW_SNAPSHOT_307.md"')
source = source.replace('TARGETS = ["elemental-shell", "timeless-form", "invulnerable-sphere"]', 'TARGETS = ["timeless-form"]')
source = source.replace(
    'assert q["nextGroup"] == GROUP and q["next"]["pendingIds"] == TARGETS',
    'assert q["nextGroup"] == GROUP and q["next"]["pendingIds"] == ["timeless-form", "invulnerable-sphere"]',
)
source = source.replace(
    'assert q["status"] == "RETURN235_AUDITED_HELD_822_26_0_PACKET308_PREPARATION"',
    'assert q["pendingCount"] == 26 and q["packetAuditStatus"] == "PASS" and q["lastReviewedBatch"]["heldIds"] == ["elemental-shell"]',
)
source = source.replace(
    'assert prior_delivery_obj["acceptedIds"] == PREVIOUS_ACCEPTED and prior_delivery_obj["applied"] is False\n    assert prior_delivery_obj["heldIds"] == TARGETS and prior_delivery_obj["authority"]["reviewedApplied"] == 808',
    'assert prior_delivery_obj["acceptedIds"] == PREVIOUS_ACCEPTED and prior_delivery_obj["applied"] is False\n    assert set(TARGETS).issubset(prior_delivery_obj["heldIds"]) and prior_delivery_obj["authority"]["reviewedApplied"] == 808',
)
source = source.replace('assert len(target_cases) > 15', 'assert len(target_cases) == 11')
source = source.replace('len(focused_questions) >= 10', 'len(focused_questions) >= 5')
source = source.replace(
    '"heldIds": TARGETS, "blockerIds": {"elemental-shell": ["DF218-B01", "DF218-B02"], "timeless-form": ["DF218-B03"], "invulnerable-sphere": ["DF218-B04"]}',
    '"heldIds": ["elemental-shell", "timeless-form", "invulnerable-sphere"], "blockerIds": {"elemental-shell": ["DF218-B01", "DF218-B02"], "timeless-form": ["DF218-B03"], "invulnerable-sphere": ["DF218-B04"]}',
)
source = source.replace(
    '"priorHeldIdentitiesNotReopened": ["psychic-scream", "mass-phantom-killer", "weird", "final-word"]',
    '"priorHeldIdentitiesNotReopened": ["final-word", "elemental-shell"]',
)
source = source.replace(
    'assert all(entries[s]["authoredStatus"] == "pending-authored-procedure" and spells[s].get("operational") is None for s in TARGETS)',
    'assert all(entries[s]["authoredStatus"] == "pending-authored-procedure" and spells[s].get("operational") is None for s in TARGETS)\n    assert entries["time-stop"]["authoredStatus"] == "pending-authored-procedure" and spells["time-stop"].get("operational") is None\n    assert "time-stop" in p["pendingIds"]',
)

requirements = {
    "id": "TIMELESS-FORM-DF218-B03-DIRECTOR-REQUIREMENTS-308",
    "source": {"service": "ChatGPT", "conversationTitle": "Calibration review part 6", "url": "https://chatgpt.com/g/g-p-67f17555a8dc8191a2b5b81e6d8adc12-dungeon-crawler/c/6adc506d-8770-83ea-b64c-0345d9b9b682"},
    "authority": {"reviewedApplied": 822, "pending": 26, "acceptedUnapplied": 0, "completeStandaloneProcedures": 546, "scopedInterfaces": 173},
    "scopeIds": ["timeless-form"], "blockerIds": ["DF218-B03"], "accepted": False, "applied": False,
    "minimumClosureEvidence": [
        "Exact accepted operational Time Stop procedure with source and acceptance bindings; define activation, costs, eligible actors, affected/excluded entities, permitted actions, and native chronology. Printed access, immunity flag, or ‘take three turns’ wording alone is insufficient.",
        "Lawfully acquired caster and complete activation history: class/repertoire/preparation, components, resources, Action and interruption accounting, actual target/area geometry, and relevant prior effects.",
        "One complete joint encounter in which a lawfully established Timeless Form encounters that Time Stop. Demonstrate promised exclusion using Time Stop’s actual permissions and clock; preserve ordinary turns, recharge, Reaction, Ready, concentration, resources, and original deadlines without added opportunities or paused clocks."
    ],
    "exactUnresolvedRecord": {"path": "history/Return218/preserved_cases/RANK9DEFENSEFORM8129-TIMELESS-FORM-B.json", "pointer": "/events/4", "finding": "Time-Stop-access/procedure-held; not a positive interaction."},
    "preservation": {"currentSourceInventory": 87, "priorTimelessFormCases": 11, "selectedDispositions": ["DF9-Q01", "DF9-Q20", "DF9-Q21", "DF9-Q22", "DF9-Q26", "DEF129-ADD02", "DF186-FUTURE-09"], "classAccess": {"classes": ["Druid", "Mage", "Wizard"], "school": "Transmutation", "rank": 9, "minimumClassLevel": 17, "baseRpCost": 26, "castingTime": "Action", "components": "V/S/F", "nativeRangeFeet": 120}, "selectedProcedure": {"recipient": "willing", "concentration": False, "durationSeconds": 60, "preserveHasteSlowSuppression": True, "preserveEndingLiabilities": True, "preserveSpentBudget": True}, "conditionalQualification": "DF218-Q-AGING remains conditional, not a whole-spell blocker."},
    "constraints": ["No DF218 obligation revision.", "Time Stop remains pending.", "Unrelated external-provider revisions do not satisfy this named interaction.", "If no qualifying procedure exists, provide a concise dependency assessment; do not manufacture a positive trace.", "No acceptance, application, or canonical changes without exact source-complete Director decision."],
    "remainingSequence": ["timeless-form", "invulnerable-sphere", "nullification-wave", "reality-anchor", "time-stop", "fate-rewrite", "collapse-timeline", "eternal-prophecy", "faction-omniscience-supreme", "banishment-gate", "conjure-demiplane-fortress", "summon-elemental-avatar", "summon-herald-of-the-planes", "summon-avatar-of-decay", "reverse-gravity-field", "alignment-ascension", "alignment-perfection", "faction-incarnate", "faction-perfection", "corruption-purification", "astral-projection", "imprisonment", "divine-intervention-greater", "wish"],
    "pendingReconciliation": {"continuingSequenceCount": 24, "separatelyHeld": ["final-word", "elemental-shell"], "totalPending": 26, "firstReviewTasks": 0}
}
(BASE / "TIMELESS_FORM_DIRECTOR_REQUIREMENTS_308.json").write_text(json.dumps(requirements, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

request = """REQUEST_308 — CURRENT-SOURCE REASSESSMENT: TIMELESS FORM ONLY

Director: GPT in Calibration review part 6.
Current authority: 822 reviewed/applied, 26 pending, 0 accepted-unapplied; 546 complete standalone procedures; 173 scoped interfaces.
Exact adjudication scope: timeless-form only, DF218-B03. Invulnerable Sphere remains next and outside this adjudication. Final Word remains held under DR217-B01; Elemental Shell remains held under DF218-B01/B02.

Minimum closure evidence:
1. An exact accepted operational Time Stop procedure with source and acceptance bindings. It must define activation, costs, eligible actors, affected and excluded entities, permitted actions, and native chronology. Printed access, an immunity flag, or ‘take three turns’ wording alone is insufficient.
2. A lawfully acquired caster and complete activation history: class/repertoire/preparation, components, resources, Action and interruption accounting, actual target/area geometry, and relevant prior effects.
3. One complete joint encounter in which a lawfully established Timeless Form encounters that Time Stop. Demonstrate the promised exclusion using Time Stop’s actual permissions and clock. Preserve ordinary turns, recharge, Reaction, Ready, concentration, resources, and original deadlines without added opportunities or paused clocks.

The exact unresolved record is history/Return218/preserved_cases/RANK9DEFENSEFORM8129-TIMELESS-FORM-B.json#/events/4, which records Time-Stop-access/procedure-held, not a positive interaction.

Refresh the current 87-source inventory and current authority/index/catalog bindings. Preserve all 11 prior Timeless Form cases, its prior procedure and selected dispositions DF9-Q01/Q20/Q21/Q22/Q26, DEF129-ADD02, and DF186-FUTURE-09. Preserve Druid/Mage/Wizard Transmutation rank 9, minimum class level 17, base 26 RP, Action/V/S/F, and native 120-foot range. Retain the selected willing-recipient, nonconcentration 60-second procedure; existing Haste/Slow suppression, ending liabilities, and spent-budget history remain unchanged. Retain DF218-Q-AGING as a conditional qualification, not another whole-spell blocker, and preserve all source/access and downstream qualifications.

No DF218 obligation revision is made here. Time Stop itself remains pending in the supplied authority. External-provider revisions for Mind Collapse, Absolute Domination, Mass Phantom Killer, and Weird do not automatically satisfy this named Time Stop interaction. If no qualifying procedure is available, submit a concise dependency assessment; do not manufacture a positive trace.

Return the sealed decision ZIP, exact DELIVERY.json, and next pending group/order. Do not accept or apply anything unless the supplied exact source-complete evidence closes DF218-B03. Do not edit canonical files or create synthetic sources/encounters.
"""
leads = {
    "id": "TIMELESS-FORM-308-CURRENT-SOURCE-LEADS", "authority": {"reviewedApplied": 822, "pending": 26, "acceptedUnapplied": 0, "completeStandaloneProcedures": 546, "scopedInterfaces": 173}, "scopeIds": ["timeless-form"], "leadsAreNotFindings": True,
    "leads": [
        {"source": "catalog.json", "pointer": "/spells (id=time-stop)/operational", "lead": "Time Stop remains pending-authored-procedure with operational=null. Class access is not a positive operational procedure or acceptance binding."},
        {"source": "authored_review_index.json", "pointer": "/entries (id=time-stop)", "lead": "Time Stop remains pending at 822/26; no completed accepted Time Stop procedure is indicated by current authority."},
        {"source": "Return218", "pointer": "history/Return218/preserved_cases/RANK9DEFENSEFORM8129-TIMELESS-FORM-B.json#/events/4", "lead": "The exact joint interaction remains Time-Stop-access/procedure-held, not a positive interaction."},
        {"source": "Return218/PROCEDURES.json", "pointer": "/spells (id=timeless-form)", "lead": "Preserve the selected willing-recipient, nonconcentration 60-second Timeless Form procedure and its Haste/Slow, ending, and spent-budget history. It does not create a Time Stop procedure."},
        {"source": "Return218/PROCEDURES.json", "pointer": "/spells (id=timeless-form)/conditionalQualificationIds", "lead": "DF218-Q-AGING remains conditional and is not a whole-spell blocker."}
    ]
}
replacement = f"    source_search_leads = {leads!r}\n    request = {request!r}\n"
start = source.index("    source_search_leads = {")
end = source.index("\n    files: dict[str, bytes] = {}", start)
source = source[:start] + replacement + source[end:]

source = source.replace(
    '    add(files, "current/RETURN235_RECEIPT.json", return235_receipt.read_bytes())\n',
    '''    add(files, "current/RETURN235_RECEIPT.json", return235_receipt.read_bytes())
    for member, local_name in [
        ("current/TIMELESS_FORM_DIRECTOR_REQUIREMENTS_308.json", "TIMELESS_FORM_DIRECTOR_REQUIREMENTS_308.json"),
        ("current/CURRENT_HANDOFF_307.json", "CURRENT_HANDOFF_307.json"),
        ("current/CURRENT_SPELL_QUEUE_307.json", "CURRENT_SPELL_QUEUE_307.json"),
        ("current/CURRENT26_PENDING_IDENTITY_AUDIT_307.json", "CURRENT26_PENDING_IDENTITY_AUDIT_307.json"),
        ("current/FINAL_WORD_DIRECTOR_DECISION_303.json", "FINAL_WORD_DIRECTOR_DECISION_303.json"),
        ("current/FINAL_WORD_HOLD_RECEIPT_303.json", "FINAL_WORD_HOLD_RECEIPT_303.json"),
        ("current/FINAL_WORD_HOLD_VALIDATION_304.json", "FINAL_WORD_HOLD_VALIDATION_304.json"),
        ("current/ELEMENTAL_SHELL_DIRECTOR_DECISION_306.json", "ELEMENTAL_SHELL_DIRECTOR_DECISION_306.json"),
        ("current/ELEMENTAL_SHELL_HOLD_RECEIPT_306.json", "ELEMENTAL_SHELL_HOLD_RECEIPT_306.json"),
        ("current/ELEMENTAL_SHELL_HOLD_VALIDATION_307.json", "ELEMENTAL_SHELL_HOLD_VALIDATION_307.json"),
        ("current/ELEMENTAL_SHELL_PACKET_306_SUBMISSION_RECEIPT_CORRECTED_307.json", "ELEMENTAL_SHELL_PACKET_306_SUBMISSION_RECEIPT_CORRECTED_307.json"),
    ]:
        add(files, member, (BASE / local_name).read_bytes())
    q_current = read(BASE / "CURRENT_SPELL_QUEUE_307.json")
    h_current = read(BASE / "CURRENT_HANDOFF_307.json")
    p_current = read(BASE / "CURRENT26_PENDING_IDENTITY_AUDIT_307.json")
    assert q_current["currentAuthority"] == h_current["currentAuthority"] == p_current["authority"] == AUTHORITY
    assert h_current["currentPreparation"]["pendingIds"] == ["timeless-form", "invulnerable-sphere"]
    assert p_current["pendingCount"] == 26 and "timeless-form" in p_current["pendingIds"] and "time-stop" in p_current["pendingIds"]
    assert read(BASE / "FINAL_WORD_DIRECTOR_DECISION_303.json")["heldIds"] == ["final-word"]
    assert read(BASE / "ELEMENTAL_SHELL_DIRECTOR_DECISION_306.json")["heldIds"] == ["elemental-shell"]
'''
)
source = source.replace('    qpath.write_bytes(enc(q_after))\n    q_bind = file_bind(qpath)', '    q_after_path = BASE / "CURRENT_SPELL_QUEUE_308.json"\n    q_after_path.write_bytes(enc(q_after))\n    q_bind = file_bind(q_after_path)')
source = source.replace(
    '"currentPreparation": file_bind(PREP), "nextGroup": GROUP, "nextPendingIds": TARGETS',
    '"currentPreparation": next_record, "preparationArtifact": file_bind(PREP), "nextPendingGroup": next_record, "nextGroup": GROUP, "nextPendingIds": TARGETS',
)
source = source.replace('    hpath.write_bytes(enc(h_after))', '    h_after_path = BASE / "CURRENT_HANDOFF_308.json"\n    h_after_path.write_bytes(enc(h_after))')
source = source.replace('len(target_cases) > 15', 'len(target_cases) == 11')

# Sanity check all required transforms took effect before compiling the generated builder.
for required in ['TARGETS = ["timeless-form"]', 'CURRENT_SPELL_QUEUE_307.json', 'CURRENT_HANDOFF_307.json', 'CURRENT26_PENDING_IDENTITY_AUDIT_307.json', 'len(target_cases) == 11', 'TIMELESS_FORM_DIRECTOR_REQUIREMENTS_308.json', 'DF218-B03']:
    if required not in source:
        raise RuntimeError(f"Generated builder is missing: {required}")
if 'qpath.write_bytes(enc(q_after))' in source or 'hpath.write_bytes(enc(h_after))' in source:
    raise RuntimeError("Refusing to overwrite the 307 parent handoff/queue")

namespace = {"__name__": "__main__", "__file__": str(TEMPLATE)}
exec(compile(source, str(TEMPLATE), "exec"), namespace)