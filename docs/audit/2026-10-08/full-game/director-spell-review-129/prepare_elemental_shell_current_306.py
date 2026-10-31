from __future__ import annotations

from pathlib import Path


HERE = Path(__file__).resolve().parent
TEMPLATE = HERE / "prepare_defenseform8_current_236.py"
source = TEMPLATE.read_text(encoding="utf-8")

# Reuse the independently audited Return218 source/case refresh builder, rebased
# to current authority and narrowed to Elemental Shell only.
for old, new in (("236", "306"), ("811", "822"), ("37", "26"), ("535", "546")):
    if old not in source:
        raise RuntimeError(f"Expected template token is absent: {old}")
    source = source.replace(old, new)

source = source.replace(
    'assert q["status"] == "RETURN235_AUDITED_HELD_822_26_0_PACKET306_PREPARATION"',
    'assert q["nextGroup"] == GROUP and q["next"]["pendingIds"] == ["elemental-shell", "timeless-form", "invulnerable-sphere"]',
)
source = source.replace('assert q["nextGroup"] == GROUP and q["next"]["pendingIds"] == TARGETS',
                        'assert q["nextGroup"] == GROUP and set(TARGETS).issubset(q["next"]["pendingIds"])')
source = source.replace('assert prior_delivery_obj["heldIds"] == TARGETS and prior_delivery_obj["authority"]["reviewedApplied"] == 808',
                        'assert set(TARGETS).issubset(prior_delivery_obj["heldIds"]) and prior_delivery_obj["authority"]["reviewedApplied"] == 808')
source = source.replace('qpath = BASE / "CURRENT_SPELL_QUEUE_306.json"', 'qpath = BASE / "CURRENT_SPELL_QUEUE_304.json"')
source = source.replace('hpath = BASE / "CURRENT_HANDOFF_306.json"', 'hpath = BASE / "CURRENT_HANDOFF_305.json"')
source = source.replace('ppath = BASE / "CURRENT26_PENDING_IDENTITY_AUDIT_306.json"', 'ppath = BASE / "CURRENT26_PENDING_IDENTITY_AUDIT_304.json"')
source = source.replace('BASE / "CURRENT_SPELL_REVIEW_SNAPSHOT_306.md"', 'BASE / "CURRENT_SPELL_REVIEW_SNAPSHOT_305.md"')
source = source.replace('TARGETS = ["elemental-shell", "timeless-form", "invulnerable-sphere"]', 'TARGETS = ["elemental-shell"]')
source = source.replace('len(focused_questions) >= 10', 'len(focused_questions) >= 6')
source = source.replace('"priorHeldIdentitiesNotReopened": ["psychic-scream", "mass-phantom-killer", "weird", "final-word"]', '"priorHeldIdentitiesNotReopened": ["final-word"]')
source = source.replace('assert p["pendingCount"] == len(p["pendingIds"]) == 26 and set(TARGETS).issubset(p["pendingIds"])',
                        'assert p["pendingCount"] == len(p["pendingIds"]) == 26 and set(TARGETS).issubset(p["pendingIds"])')

source = source.replace(
    'source_search_leads = {\n        "id": "DEFENSEFORM8-306-CURRENT-SOURCE-LEADS",',
    'source_search_leads = {\n        "id": "ELEMENTAL-SHELL-306-CURRENT-SOURCE-LEADS",',
)
start = source.index('    source_search_leads = {')
end = source.index('    request = f"""REQUEST_306', start)
leads = '''    source_search_leads = {
        "id": "ELEMENTAL-SHELL-306-CURRENT-SOURCE-LEADS",
        "authority": AUTHORITY,
        "scopeIds": ["elemental-shell"],
        "leadsAreNotFindings": True,
        "leads": [
            {"source": "catalog.json", "pointer": "/spells (id=volcanic-cage or deep-crust-spike)/operational", "lead": "Both remain blocked with operational=null. Printed descriptions are not an instantiated noncreature elemental damage packet; do not infer an owner or event."},
            {"source": "catalog.json", "pointer": "/spells (id=dominate-beast)/operational", "lead": "The owner-attached companion execution bridge does not by itself establish a legally acquired and actually instantiated proxy with body/profile, HP/defenses, equipment, native damaging attack, controller acquisition, command cost, and attached phase schedule."},
            {"source": "catalog.json", "pointer": "/spells (id=summon-spectral-steed)/operational", "lead": "The current mount has no damaging Action and cannot supply the required B02 attack witness."},
            {"source": "prior Return218/DF218-B01", "pointer": "history/Return218/BLOCKER_REASSESSMENT.json#/records/DF218-B01", "lead": "Prior hold requires a source-established quantified noncreature environmental packet and bearer occupancy/defense history; an accepted/index-bound envelope alone is insufficient."},
            {"source": "prior Return218/DF218-B02", "pointer": "history/Return218/BLOCKER_REASSESSMENT.json#/records/DF218-B02", "lead": "Prior hold requires an actually accessible companion or proxy with its full body, equipment, attack, controller acquisition, command payment, and attached phase history."},
        ],
    }

'''
source = source[:start] + leads + source[end:]

start = source.index('    request = f"""REQUEST_306')
end = source.index('\n"""', start) + len('\n"""')
request = '''    request = """REQUEST_306 — CURRENT-SOURCE REASSESSMENT: ELEMENTAL SHELL ONLY

Director: GPT in Calibration review part 6.
Current authority: 822 reviewed/applied, 26 pending, 0 accepted-unapplied; 546 complete standalone procedures; 173 scoped interfaces.
Exact adjudication scope: elemental-shell only, DF218-B01 and DF218-B02. Final Word remains separately held under DR217-B01. Do not adjudicate other identities.

Refresh the prior 87-source inventory, current authority records, and relevant accepted-interface bindings. Preserve the exact Druid/Mage/Wizard Transmutation rank-9 class-level-17 routes at base 26 RP, native card, current selected rules, and all 21 prior Elemental Shell case records, including both completed CH07 Null traces. Preserve the prior Return218 procedures and blocker findings byte-exact as history; do not claim replay of preserved cases.

DF218-B01 minimum closure evidence: a source-established noncreature elemental damage source with exact geometry, selected damage type, amount or roll, and timing; plus Shell bearer occupancy, defenses, paid application, and deadline. Demonstrate selected-component mitigation and Shell immunity. Where no responsible creature dealer exists, demonstrate no reflected recipient and no emitted reflection packet; do not invent an environmental owner.

DF218-B02 minimum closure evidence: one legally acquired and actually instantiated companion/proxy with complete body/profile, HP/defenses, equipment or explicit absence, native damaging attack with type/reach/range, controller acquisition, command cost, and attached-phase schedule. Trace the attack into Shell and reflection back to the actual creature dealer, never automatically to its controller. Preserve resulting damage/lifecycle, resources, custody, and phase history.

Integrated traces must preserve reflection basis after other applicable defenses but before Shell immunity; reflected amount floor(basis/2); actual dealer within 120 feet and unobstructed line of effect or else no reflection/deferred payment; separate original/reflected roots; reflector-derived Null provenance; once-only causal keys; no recursion; actual cast/interruption accounting; regular clocks; command opportunities; suppression; original deadlines; and complete reversible states.

No substantive DF218 ruling changes are authorized. Preserve DF9-Q01/Q12/Q13/Q14/Q15/Q26, DEF129-ADD01, relevant future requirements, and all qualifications. The selected 60-second nonconcentration duration remains spell-local authorship, not recovered native text. Do not synthesize a replacement source or scenario; the accepted/index-bound envelope, Dominate Beast alone, and Spectral Steed without a damaging Action remain unqualified leads unless exact source evidence closes the stated conditions.

The packet binds current queue 304, corrected handoff 305, current pending audit 304, Final Word hold 303/304, current authored index/catalog, and current accepted-interface registry/work queue. The stale Return289 pointer from handoff 304 is preserved only as history in handoff 305. If a blocker remains, retain its exact minimum under the existing DF218 ID. Do not edit canonical files or apply/accept anything. Return the sealed decision ZIP, exact DELIVERY.json, and the next pending group/order.
"""'''
source = source[:start] + request + source[end:]

marker = '    add(files, "current/RETURN235_RECEIPT.json", return235_receipt.read_bytes())\n'
extra = marker + '''    # Latest current position and authority records, bound separately from history.
    for member, local_name in [
        ("current/CURRENT_HANDOFF_305.json", "CURRENT_HANDOFF_305.json"),
        ("history/Parent304/CURRENT_HANDOFF_304.json", "CURRENT_HANDOFF_304.json"),
        ("current/CURRENT_SPELL_QUEUE_304.json", "CURRENT_SPELL_QUEUE_304.json"),
        ("current/CURRENT26_PENDING_IDENTITY_AUDIT_304.json", "CURRENT26_PENDING_IDENTITY_AUDIT_304.json"),
        ("current/ELEMENTAL_SHELL_DIRECTOR_REQUIREMENTS_305.json", "ELEMENTAL_SHELL_DIRECTOR_REQUIREMENTS_305.json"),
        ("current/ELEMENTAL_SHELL_HANDOFF_CORRECTION_VALIDATION_305.json", "ELEMENTAL_SHELL_HANDOFF_CORRECTION_VALIDATION_305.json"),
        ("current/FINAL_WORD_DIRECTOR_DECISION_303.json", "FINAL_WORD_DIRECTOR_DECISION_303.json"),
        ("current/FINAL_WORD_HOLD_RECEIPT_303.json", "FINAL_WORD_HOLD_RECEIPT_303.json"),
        ("current/FINAL_WORD_HOLD_VALIDATION_304.json", "FINAL_WORD_HOLD_VALIDATION_304.json"),
    ]:
        add(files, member, (BASE / local_name).read_bytes())
    latest_queue = read(BASE / "CURRENT_SPELL_QUEUE_304.json")
    corrected_handoff = read(BASE / "CURRENT_HANDOFF_305.json")
    current_pending = read(BASE / "CURRENT26_PENDING_IDENTITY_AUDIT_304.json")
    latest_fw = read(BASE / "FINAL_WORD_DIRECTOR_DECISION_303.json")
    assert latest_queue["currentAuthority"] == corrected_handoff["currentAuthority"] == current_pending["authority"] == AUTHORITY
    assert corrected_handoff["nextPendingGroup"]["group"] == corrected_handoff["currentPreparation"]["group"] == GROUP
    assert corrected_handoff["historicalNextPendingGroupPointer304"]["directorReturn"] == 289
    assert latest_fw["heldIds"] == ["final-word"] and latest_fw["blockerIds"] == ["DR217-B01"]
    assert latest_fw["acceptedIds"] == latest_fw["appliedIds"] == []
'''
if marker not in source:
    raise RuntimeError("Cannot locate current authority member insertion point")
source = source.replace(marker, extra, 1)

namespace = {"__name__": "__main__", "__file__": str(TEMPLATE)}
exec(compile(source, str(TEMPLATE), "exec"), namespace)
