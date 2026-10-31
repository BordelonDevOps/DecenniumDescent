from __future__ import annotations

import json
import hashlib
import pathlib
import zipfile
import zlib

ROOT = pathlib.Path.cwd()
BASE = ROOT / "docs/audit/2026-10-08/full-game/director-spell-review-129"
TEMPLATE = BASE / "prepare_defenseform8_current_236.py"
source = TEMPLATE.read_text(encoding="utf-8")

for old, new in (("236", "310"), ("811", "822"), ("37", "26"), ("535", "546")):
    if old not in source:
        raise RuntimeError(f"Expected template token is absent: {old}")
    source = source.replace(old, new)

source = source.replace(
    'TARGETS = ["elemental-shell", "timeless-form", "invulnerable-sphere"]',
    'TARGETS = ["invulnerable-sphere"]',
)
source = source.replace('qpath = BASE / "CURRENT_SPELL_QUEUE_310.json"', 'qpath = BASE / "CURRENT_SPELL_QUEUE_309.json"')
source = source.replace('hpath = BASE / "CURRENT_HANDOFF_310.json"', 'hpath = BASE / "CURRENT_HANDOFF_309.json"')
source = source.replace('ppath = BASE / "CURRENT26_PENDING_IDENTITY_AUDIT_310.json"', 'ppath = BASE / "CURRENT26_PENDING_IDENTITY_AUDIT_308.json"')
source = source.replace('BASE / "CURRENT_SPELL_REVIEW_SNAPSHOT_310.md"', 'BASE / "CURRENT_SPELL_REVIEW_SNAPSHOT_309.md"')

source = source.replace(
    'assert q["nextGroup"] == GROUP and q["next"]["pendingIds"] == TARGETS',
    'assert q["nextGroup"] == GROUP and q["next"]["pendingIds"] == TARGETS\n    assert q["next"]["status"] == "DIRECTOR_NEXT_AFTER_TIMELESS_FORM_HOLD_308"',
)
source = source.replace(
    'assert q["status"] == "RETURN235_AUDITED_HELD_822_26_0_PACKET310_PREPARATION"',
    'assert q["currentAuthority"] == AUTHORITY and q["packetStatus"] == "RETURN308_RECEIVED_AND_INDEPENDENTLY_VERIFIED_HELD"',
)
source = source.replace(
    'assert prior_delivery_obj["heldIds"] == TARGETS and prior_delivery_obj["authority"]["reviewedApplied"] == 808',
    'assert set(TARGETS).issubset(prior_delivery_obj["heldIds"]) and prior_delivery_obj["authority"]["reviewedApplied"] == 808',
)
source = source.replace('assert len(target_cases) > 15', 'assert len(target_cases) == 14')
source = source.replace('len(target_cases) > 15', 'len(target_cases) == 14')
source = source.replace('len(focused_questions) >= 10', 'len(focused_questions) >= 5')
source = source.replace(
    '"DIRECTOR_DECISION.json", "BLOCKER_REASSESSMENT.json", "COUNTS.json", "CASE_INDEX.json",\n            "PROCEDURES.json", "INDEPENDENT_SEMANTIC_FAILURE_CHECK.json", "MEMBER_MANIFEST.json",',
    '"DIRECTOR_DECISION.json", "BLOCKER_REASSESSMENT.json", "COUNTS.json", "CASE_INDEX.json",\n            "PROCEDURES.json", "INDEPENDENT_SEMANTIC_FAILURE_CHECK.json", "MEMBER_MANIFEST.json",\n            "QUESTION_DISPOSITIONS.json", "FUTURE_OBLIGATION_DISPOSITIONS.json",',
)
source = source.replace(
    'return235_archive = BASE / "rank9_deathrecovery7_return235_received/DD_Rank9_FinalWord_Director_Return235_HELD.zip"\n'
    '    return235_delivery = BASE / "rank9_deathrecovery7_return235_received/DD_Rank9_FinalWord_Director_Return235_HELD_DELIVERY.json"\n'
    '    return235_audit = BASE / "RANK9DEATHRECOVERY7_RETURN235_INDEPENDENT_AUDIT.json"\n'
    '    return235_receipt = BASE / "RANK9DEATHRECOVERY7_RETURN235_RECEIPT.json"\n'
    '    assert read(return235_audit)["status"] == read(return235_receipt)["status"] == "PASS"',
    'return308_archive = BASE / "rank9_defenseform8_return308_received/DD_Rank9_DefenseForm8_Director_Return308_HELD.zip"\n'
    '    return308_delivery = BASE / "rank9_defenseform8_return308_received/DD_Rank9_DefenseForm8_Director_Return308_HELD_DELIVERY.json"\n'
    '    return308_audit = BASE / "TIMELESS_FORM_RETURN308_INDEPENDENT_AUDIT.json"\n'
    '    return308_receipt = BASE / "TIMELESS_FORM_HOLD_RECEIPT_308.json"\n'
    '    return308_decision = BASE / "TIMELESS_FORM_DIRECTOR_DECISION_308.json"\n'
    '    return308_hold_validation = BASE / "TIMELESS_FORM_HOLD_VALIDATION_309.json"\n'
    '    assert read(return308_audit)["status"] == read(return308_hold_validation)["status"] == "PASS"\n'
    '    assert read(return308_decision)["heldIds"] == ["timeless-form"] and read(return308_decision)["blockerIds"] == ["DF218-B03"]',
)
source = source.replace(
    '"return235Audit": file_bind(return235_audit)',
    '"return308Audit": file_bind(return308_audit), "return308Decision": file_bind(return308_decision)',
)
source = source.replace(
    '"heldIds": TARGETS, "blockerIds": {"elemental-shell": ["DF218-B01", "DF218-B02"], "timeless-form": ["DF218-B03"], "invulnerable-sphere": ["DF218-B04"]}',
    '"heldIds": ["elemental-shell", "timeless-form", "invulnerable-sphere"], "blockerIds": {"elemental-shell": ["DF218-B01", "DF218-B02"], "timeless-form": ["DF218-B03"], "invulnerable-sphere": ["DF218-B04"]}',
)
source = source.replace(
    '"priorHeldIdentitiesNotReopened": ["psychic-scream", "mass-phantom-killer", "weird", "final-word"]',
    '"priorHeldIdentitiesNotReopened": ["final-word", "elemental-shell", "timeless-form"]',
)

# Report the worktree snapshot separately from the last committed baseline.
overlay_marker = '    source_search_leads = {'
overlay_code = '''    base_index_raw = subprocess.check_output(["git", "show", f"{commit}:DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json"], cwd=ROOT)
    candidate["workingTreeOverlay"] = {
        "baseCommit": commit,
        "branch": branch,
        "baseAuthoredIndex": bind("DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json", base_index_raw),
        "workingTreeAuthoredIndex": file_bind(index_path),
        "workingTreeCatalog": file_bind(catalog_path),
        "workingTreeQueueInput": file_bind(qpath),
        "workingTreeHandoffInput": file_bind(hpath),
        "workingTreePendingAuditInput": file_bind(ppath),
        "interpretation": "All packet current/ sources bind the working-tree snapshot. The base commit is identified separately; no checkout or canonical file mutation occurs during packet preparation.",
    }
'''
source = source.replace(overlay_marker, overlay_code + overlay_marker, 1)

start = source.index("    source_search_leads = {")
end = source.index("\n    files: dict[str, bytes] = {}", start)
replacement = r'''    source_search_leads = {
        "id": "INVULNERABLE-SPHERE-310-CURRENT-SOURCE-LEADS",
        "authority": AUTHORITY,
        "scopeIds": TARGETS,
        "leadsAreNotFindings": True,
        "leads": [
            {"source": "catalog.json", "pointer": "/spells (id=faction-portal)/operational", "lead": "Faction Portal provides a possible planar route only if its exact accepted procedure and acceptance bindings, actual actor, current eligibility, canonical faction, positive reputation, known authorized headquarters, crossing settlement, and Sphere interaction are independently source-bound."},
            {"source": "catalog.json", "pointer": "/spells (id=summon-spectral-steed)/operational/planar-crossing", "lead": "Spectral Steed has a one-attempt planar route, but its lawfully acquired rider/owner, exact origin/destination, mounted whole bodies and cargo, command payment, eligibility, and terminal failure settlement must be established; a route summary alone is not a witness."},
            {"source": "catalog.json", "pointer": "/spells (id=teleport)", "lead": "The preserved Teleport witness is same-plane and does not satisfy the DF9-Q24 planar-crossing branch."},
            {"source": "Return218 and Return280", "pointer": "DF218-B04 / RANK9DEFENSEFORM8129-INVULNERABLE-SPHERE-B4-PLANAR", "lead": "Existing blocker requires a legal acquired planar attempt against the complete closed Sphere partition; the completed Crown-command witness is a separate closed gap and remains untouched."},
            {"source": "current authored index/catalog", "pointer": "/entries and /spells (id=invulnerable-sphere)", "lead": "Sphere remains pending-authored-procedure with operational=null at 822/26; this establishes no acquired actor, route, site or positive crossing encounter."},
        ],
    }
    request = """REQUEST_310 — CURRENT-SOURCE REASSESSMENT: INVULNERABLE SPHERE ONLY

Director: GPT in Calibration review part 6.
Current authority: 822 reviewed/applied, 26 pending, 0 accepted-unapplied; 546 complete standalone procedures; 173 scoped interfaces.
Scope: invulnerable-sphere / DF218-B04 only. This is a preparation packet for the next ruling, not an invitation to widen scope.

Keep DF218-B04 narrowly scoped to a lawful, otherwise-valid planar crossing attempt against the Sphere’s complete closed partition. The same-plane Teleport case and completed Crown-command witness do not supply planar permission. Do not reopen the closed Crown-command gap or unrelated holds.

Minimum closure evidence:
1. Exact accepted operational procedure and acceptance bindings establishing planar travel, eligibility, activation, costs, destination restrictions, and failure/terminal settlement. Printed access or a portal name alone is insufficient.
2. The acquired actor’s complete legal profile, acquisition and repertoire/preparation where applicable, available resources/components, and actual Action, interruption, concentration and recharge history.
3. Specific source-qualified origin and destination—or paired sites if required—with permission, availability, coordinates, occupied volumes, arrival clearance and support.
4. Identified transported body, equipment, cargo, ownership/custody, attachments and any companion permissions. Resolve every non-Sphere eligibility prerequisite.
5. Lawfully establish the Sphere, then attempt the otherwise-valid planar crossing while its partition is complete. Record actual commitment/payment, the Sphere-caused denial, and the crossing source’s exact terminal settlement. Preserve bodies, cargo, spent resources and independent clocks.

The decisive preserved obligation is RANK9DEFENSEFORM8129-INVULNERABLE-SPHERE-B4-PLANAR linked to DF9-Q24. An endpoint predicate or generic “blocked” flag is not the complete witness. Faction Portal or another lead qualifies only when its actual actor, permissions, sites and operational contract are bound.

Compact packet scope: bind the current 822/26/0 index, catalog, queue, handoff, pending audit and any working-tree overlay separately from the base commit; refresh all 87 Defense/Form sources with exact paths, byte lengths and SHA-256; preserve original source bytes and historical bindings; preserve the exact Sphere procedure and all 14 Return218 case IDs, including the actual Crown-command case, without recreating them; preserve DF9-Q01, DF9-Q23–Q26, DEF129-ADD02 and the Sphere future requirement at futureCaseRequirements[9]; add only necessary crossing procedure/source/acceptance, actor/acquisition, endpoint authorization and focused witness records; include source-linked before/after states, forward/inverse operations, hashes, full reverse traversal and clock/resource/custody checks, distinguishing preservation from new replay; bind Return308 and its independent audit as prior held context without duplicating large historical archives; preserve Core entry 101 and paragraph 9102, class files, accepted-interface registry, Transport6 predicates/settlements, and applicable casting/combat/control/body-equipment/lifecycle/cosmology records. Bind extra sources explicitly if the selected crossing route lies outside the 87-file inventory.

Keep the current Sphere procedure constraints unchanged: native Cleric/Druid/Mage/Wizard Abjuration, rank 9, class level 17, base 26 RP, Action, V/S/F, 120 feet; preserve Core entry 101, paragraph 9102 and printed “Instantaneous.” Selected concentration/60-second duration, fixed 10-foot radius and 1-inch boundary are spell-local authorship. Preserve clear establishment geometry, actual consent from every enclosed creature, no body/object cutting, crushing, displacement or hidden-roster disclosure; complete enclosure blocks specified physical, informational, magical and planar crossings; consent withdrawal, concentration loss, caster death and expiry retain selected endings; partial antimagic creates actual openings and occupied portions cannot close onto bodies; no resource refunds, clock pauses, free opportunities, invented atmosphere/suffocation rules or automatic custody changes.

Retain DF186-QH-SOURCE-ACCESS, CONTENT-PHYSICAL, RUNTIME, HUMAN-PLAY, BALANCE, COSMOLOGY, DOMAIN-CLOSURE, RELEASE, INHERITED, and DF218-Q-IMPLEMENTATION. The prior Sphere procedure has no separate conditional-qualification ID. Bind Return308 and its audit as prior held context: Timeless Form remains held under DF218-B03. Final Word and Elemental Shell remain separately held. Do not mutate the index/catalog or apply anything.

The continuing order begins with Invulnerable Sphere, then Nullification Wave, Reality Anchor, Time Stop, Fate Rewrite, Collapse Timeline, Eternal Prophecy, Faction Omniscience Supreme, Banishment Gate, Conjure Demiplane Fortress, Summon Elemental Avatar, Summon Herald of the Planes, Summon Avatar of Decay, Reverse Gravity Field, Alignment Ascension, Alignment Perfection, Faction Incarnate, Faction Perfection, Corruption Purification, Astral Projection, Imprisonment, Divine Intervention Greater, Wish. Final Word, Elemental Shell and Timeless Form remain separately held: 26 closure tasks total and zero first-review tasks.

If the current source snapshot lacks a fully qualified crossing route and encounter, retain only DF218-B04 with the exact minimum missing witness. Do not invent an actor, permission, faction, plane, site, lawful cast, or positive crossing trace. Return the sealed decision ZIP, exact DELIVERY.json, and next pending group/order. Do not accept or apply without exact source-complete evidence.
"""
'''
source = source[:start] + replacement + source[end:]

source = source.replace(
    '    add(files, "current/RETURN235_DELIVERY.json", return235_delivery.read_bytes())\n'
    '    add(files, "current/RETURN235_INDEPENDENT_AUDIT.json", return235_audit.read_bytes())\n'
    '    add(files, "current/RETURN235_RECEIPT.json", return235_receipt.read_bytes())',
    '    add(files, "current/RETURN308_DELIVERY.json", return308_delivery.read_bytes())\n'
    '    add(files, "current/RETURN308_INDEPENDENT_AUDIT.json", return308_audit.read_bytes())\n'
    '    add(files, "current/RETURN308_HOLD_RECEIPT.json", return308_receipt.read_bytes())\n'
    '    add(files, "current/RETURN308_DIRECTOR_DECISION.json", return308_decision.read_bytes())\n'
    '    add(files, "current/RETURN308_HOLD_VALIDATION_309.json", return308_hold_validation.read_bytes())',
)

source = source.replace(
    '    return308_hold_validation = BASE / "TIMELESS_FORM_HOLD_VALIDATION_309.json"\n'
    '    assert read(return308_audit)["status"] == read(return308_hold_validation)["status"] == "PASS"',
    '    return308_hold_validation = BASE / "TIMELESS_FORM_HOLD_VALIDATION_309.json"\n'
    '    assert read(return308_audit)["status"] == read(return308_hold_validation)["status"] == "PASS"\n'
    '    return280_archive = BASE / "rank9_defenseform8_return280_received/DD_Rank9_DefenseForm8_Director_Return280_HELD.zip"\n'
    '    return280_delivery = BASE / "rank9_defenseform8_return280_received/DD_Rank9_DefenseForm8_Director_Return280_HELD_DELIVERY.json"\n'
    '    with zipfile.ZipFile(return280_archive) as r280:\n'
    '        b04 = next(row for row in json.loads(r280.read("BLOCKERS.json"))["records"] if row["id"] == "DF218-B04")\n'
    '        d280 = json.loads(r280.read("DIRECTOR_DECISION.json"))\n'
    '        d04 = next(row for row in d280["perIdentity"] if row.get("id") == "invulnerable-sphere")\n'
    '        sphere_case_rows = [row for row in json.loads(r280.read("CASE_RESULTS.json"))["cases"] if row.get("spellId") == "invulnerable-sphere"]\n'
    '        r280_manifest = json.loads(r280.read("MEMBER_MANIFEST.json"))\n'
    '        b04_manifest_binding = next(row for row in r280_manifest["members"] if row["path"] == "BLOCKERS.json")\n'
    '    return280_context = {"archive": file_bind(return280_archive), "delivery": file_bind(return280_delivery), "blockerMemberBinding": b04_manifest_binding, "blocker": b04, "sphereDecision": d04, "sphereCaseResults": sphere_case_rows, "scopeNote": "Historical Return280 context only; current scope is invulnerable-sphere at authority 822/26."}\n'
    '    assert b04["id"] == "DF218-B04" and b04["spellId"] == "invulnerable-sphere" and d04["blockerIds"] == ["DF218-B04"]',
)

source = source.replace(
    '"return308Audit": file_bind(return308_audit), "return308Decision": file_bind(return308_decision)',
    '"return308Audit": file_bind(return308_audit), "return308Decision": file_bind(return308_decision), "return280B04Context": file_bind(BASE / "PRIOR_RETURN280_B04_CONTEXT_310.json")',
)

source = source.replace(
    '    qpath.write_bytes(enc(q_after))\n    q_bind = file_bind(qpath)',
    '    q_outpath = BASE / "CURRENT_SPELL_QUEUE_310.json"\n    q_outpath.write_bytes(enc(q_after))\n    q_bind = file_bind(q_outpath)',
)
source = source.replace(
    '    hpath.write_bytes(enc(h_after))',
    '    h_outpath = BASE / "CURRENT_HANDOFF_310.json"\n    h_outpath.write_bytes(enc(h_after))',
)

# Replace the downstream file names for the scoped Sphere packet and link the
# newly written director hold context, without overwriting its parent queue.
source = source.replace('"exact three pending targets"', '"exact pending Sphere target"')
source = source.replace('"Exact three pending targets remain non-operational and the two prior acceptances are applied/closed"', '"The exact Sphere target remains pending/non-operational and prior acceptances stay closed"')
source = source.replace('len(source_search_leads["leads"]) == 5', 'len(source_search_leads["leads"]) == 5')
source = source.replace('"All 87 historical source paths refresh to current worktree bytes"', '"All 87 Defense/Form source paths refresh to current worktree bytes"')
source = source.replace('"Fresh current-authority review of only three pending Defense/Form8 identities; GPT is director. Prior accepted identities remain closed."', '"Fresh current-authority review of Invulnerable Sphere / DF218-B04 only; GPT is Director. Prior accepted identities and separate holds remain unchanged."')

# Preserve the full historical Sphere procedure, all 14 source-bound cases,
# the selected question/future dispositions, and the compact current Return308 context.
if 'CURRENT_HANDOFF_309.json' not in source or 'CURRENT_SPELL_QUEUE_309.json' not in source:
    raise RuntimeError("Generated packet does not bind its actual current input handoff and queue")
if 'return235_' in source or 'RETURN235_' in source:
    raise RuntimeError("Generated packet still carries stale Return235 status instead of Return308")
if 'len(target_cases) == 14' not in source or 'TARGETS = ["invulnerable-sphere"]' not in source:
    raise RuntimeError("Generated packet is not restricted to the 14-case Sphere scope")

requirements = {
    "id": "INVULNERABLE-SPHERE-DF218-B04-DIRECTOR-REQUIREMENTS-310",
    "source": {"service": "ChatGPT", "conversationTitle": "Calibration review part 6", "url": "https://chatgpt.com/g/g-p-67f17555a8dc8191a2b5b81e6d8adc12-dungeon-crawler/c/6adc506d-8770-83ea-b64c-0345d9b9b682"},
    "preparationOnly": True,
    "authority": {"reviewedApplied": 822, "pending": 26, "acceptedUnapplied": 0, "completeStandaloneProcedures": 546, "scopedInterfaces": 173},
    "scopeIds": ["invulnerable-sphere"], "blockerIds": ["DF218-B04"], "acceptedIds": [], "appliedIds": [],
    "minimumClosureEvidence": [
        "Exact accepted operational procedure and acceptance bindings establishing planar travel, eligibility, activation, costs, destination restrictions, and failure/terminal settlement.",
        "Acquired actor’s complete legal profile, acquisition and repertoire/preparation where applicable, available resources/components, and actual Action, interruption, concentration and recharge history.",
        "Specific source-qualified origin and destination, or paired sites if required, with permission, availability, coordinates, occupied volumes, arrival clearance and support.",
        "Identified transported body, equipment, cargo, ownership/custody, attachments and any companion permissions; resolve every non-Sphere eligibility prerequisite.",
        "Lawfully establish Sphere, then attempt the otherwise-valid planar crossing while its partition is complete. Record actual commitment/payment, Sphere-caused denial and exact terminal settlement; preserve bodies, cargo, spent resources and independent clocks.",
    ],
    "decisivePreservedObligation": {"caseId": "RANK9DEFENSEFORM8129-INVULNERABLE-SPHERE-B4-PLANAR", "questionId": "DF9-Q24", "endpointPredicateOrGenericBlockedFlagSufficient": False},
    "preserve": {
        "currentSourceInventory": 87,
        "return218Procedure": "procedures/invulnerable-sphere.json",
        "return218CaseIds": [
            "RANK9DEFENSEFORM8129-INVULNERABLE-SPHERE-A", "RANK9DEFENSEFORM8129-INVULNERABLE-SPHERE-B",
            "RANK9DEFENSEFORM8129-INVULNERABLE-SPHERE-B1-TELEPORT", "RANK9DEFENSEFORM8129-INVULNERABLE-SPHERE-B2-CONSENT-END",
            "RANK9DEFENSEFORM8129-INVULNERABLE-SPHERE-B3-HIDDEN-OCCUPANCY", "RANK9DEFENSEFORM8129-INVULNERABLE-SPHERE-B4-PLANAR",
            "RANK9DEFENSEFORM8129-INVULNERABLE-SPHERE-B5-CONTROL", "RANK9DEFENSEFORM8129-INVULNERABLE-SPHERE-COUNTER",
            "RANK9DEFENSEFORM8129-INVULNERABLE-SPHERE-GATE-access", "RANK9DEFENSEFORM8129-INVULNERABLE-SPHERE-GATE-components",
            "RANK9DEFENSEFORM8129-INVULNERABLE-SPHERE-GATE-range", "RANK9DEFENSEFORM8129-INVULNERABLE-SPHERE-GATE-resource",
            "RANK9DEFENSEFORM8129-INVULNERABLE-SPHERE-READY-EXPIRES", "DF218-SPHERE-ACTUAL-CROWN-COMMAND",
        ],
        "selectedDispositions": ["DF9-Q01", "DF9-Q23", "DF9-Q24", "DF9-Q25", "DF9-Q26", "DEF129-ADD02"],
        "futureRequirementPointer": "futureCaseRequirements[9]",
        "nativeRoute": {"classes": ["Cleric", "Druid", "Mage", "Wizard"], "school": "Abjuration", "rank": 9, "minimumClassLevel": 17, "baseRpCost": 26, "castingTime": "Action", "components": "V/S/F", "rangeFeet": 120},
        "selectedLocalAuthorship": {"concentration": True, "durationSeconds": 60, "radiusFeet": 10, "boundaryInches": 1, "coreEntry": 101, "coreParagraph": 9102, "printedDuration": "Instantaneous"},
        "conditionalQualificationIds": [],
        "retainedQualificationIds": ["DF186-QH-SOURCE-ACCESS", "DF186-QH-CONTENT-PHYSICAL", "DF186-QH-RUNTIME", "DF186-QH-HUMAN-PLAY", "DF186-QH-BALANCE", "DF186-QH-COSMOLOGY", "DF186-QH-DOMAIN-CLOSURE", "DF186-QH-RELEASE", "DF186-QH-INHERITED", "DF218-Q-IMPLEMENTATION"],
        "priorReturn308": {"archivePath": "rank9_defenseform8_return308_received/DD_Rank9_DefenseForm8_Director_Return308_HELD.zip", "heldIds": ["timeless-form"], "blockerIds": ["DF218-B03"], "acceptedIds": [], "appliedIds": []},
    },
    "constraints": [
        "No accepted route, actor, faction, plane, site, lawful cast or positive crossing witness may be inferred from a printed name or endpoint predicate.",
        "Do not reopen the completed Crown-command witness or the same-plane Teleport case.",
        "Do not alter Sphere spell-local procedure rules or retained qualifications.",
        "Preserve Return308 as prior held context; Final Word, Elemental Shell and Timeless Form remain held.",
        "No acceptance, application, index/catalog edits, or GitHub publication from this packet.",
    ],
    "remainingOrder": ["invulnerable-sphere", "nullification-wave", "reality-anchor", "time-stop", "fate-rewrite", "collapse-timeline", "eternal-prophecy", "faction-omniscience-supreme", "banishment-gate", "conjure-demiplane-fortress", "summon-elemental-avatar", "summon-herald-of-the-planes", "summon-avatar-of-decay", "reverse-gravity-field", "alignment-ascension", "alignment-perfection", "faction-incarnate", "faction-perfection", "corruption-purification", "astral-projection", "imprisonment", "divine-intervention-greater", "wish"],
    "separatelyHeld": ["final-word", "elemental-shell", "timeless-form"],
    "pendingReconciliation": {"continuingPriorities": 23, "separatelyHeld": 3, "totalPending": 26, "firstReviewTasks": 0},
}
requirements_path = BASE / "INVULNERABLE_SPHERE_DIRECTOR_REQUIREMENTS_310.json"
requirements_path.write_text(json.dumps(requirements, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
(BASE / "REQUEST_310.txt").write_text(
    "REQUEST_310 — CURRENT-SOURCE REASSESSMENT: INVULNERABLE SPHERE ONLY\n\n"
    "Director: GPT in Calibration review part 6.\n"
    "Authority 822/26/0; 546 standalone procedures; 173 scoped interfaces. Exact scope: invulnerable-sphere / DF218-B04.\n\n"
    "Follow INVULNERABLE_SPHERE_DIRECTOR_REQUIREMENTS_310.json. DF218-B04 is limited to a lawful otherwise-valid planar crossing attempt against the Sphere’s complete closed partition. The same-plane Teleport case and completed Crown-command witness do not supply planar permission.\n\n"
    "The compact packet refreshes all 87 source bindings and current authority/index/catalog/queue/handoff/pending audit; preserves the exact Return218 Sphere procedure and 14 cases byte-exact, DF9-Q01/Q23–Q26, DEF129-ADD02, and futureCaseRequirements[9]; binds Return280’s B04 context and Return308 plus its independent audit; and includes only source-qualified current crossing leads.\n\n"
    "If no fully qualified route and integrated crossing witness exist, retain only DF218-B04 and identify the exact missing evidence. Do not invent an actor, faction, permission, plane/site, lawful cast, or positive trace. No acceptance, application or canonical changes. Return the sealed decision ZIP, exact DELIVERY.json, and next order/count.\n",
    encoding="utf-8",
)

# Build the prior Return280 context before the generated builder executes.
return280_archive = BASE / "rank9_defenseform8_return280_received/DD_Rank9_DefenseForm8_Director_Return280_HELD.zip"
return280_delivery = BASE / "rank9_defenseform8_return280_received/DD_Rank9_DefenseForm8_Director_Return280_HELD_DELIVERY.json"
with zipfile.ZipFile(return280_archive) as z:
    b04 = next(row for row in json.loads(z.read("BLOCKERS.json"))["records"] if row["id"] == "DF218-B04")
    dec = json.loads(z.read("DIRECTOR_DECISION.json"))
    sphere_decision = next(row for row in dec["perIdentity"] if row.get("id") == "invulnerable-sphere")
    case_rows = [row for row in json.loads(z.read("CASE_RESULTS.json"))["cases"] if row.get("spellId") == "invulnerable-sphere"]
    im = json.loads(z.read("MEMBER_MANIFEST.json"))
    blocker_binding = next(row for row in im["members"] if row["path"] == "BLOCKERS.json")
return280_archive_raw = return280_archive.read_bytes()
return280_delivery_raw = return280_delivery.read_bytes()
return280_context = {
    "archive": {"path": return280_archive.relative_to(ROOT).as_posix(), "bytes": len(return280_archive_raw), "sha256": hashlib.sha256(return280_archive_raw).hexdigest(), "crc32": f"{zlib.crc32(return280_archive_raw) & 0xffffffff:08x}"},
    "delivery": {"path": return280_delivery.relative_to(ROOT).as_posix(), "bytes": len(return280_delivery_raw), "sha256": hashlib.sha256(return280_delivery_raw).hexdigest(), "crc32": f"{zlib.crc32(return280_delivery_raw) & 0xffffffff:08x}"},
    "blockerMemberBinding": blocker_binding, "blocker": b04,
    "sphereDecision": sphere_decision, "sphereCaseResults": case_rows,
    "scopeNote": "Historical Return280 context only; current scope is Invulnerable Sphere at authority 822/26.",
}
(BASE / "PRIOR_RETURN280_B04_CONTEXT_310.json").write_text(json.dumps(return280_context, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

# Add compact Return280 B04 context and current Return308 held context to packet.
member_marker = '    add(files, "current/RETURN308_HOLD_VALIDATION_309.json", return308_hold_validation.read_bytes())\n'
if member_marker not in source:
    raise RuntimeError("Cannot locate Return308 packet binding insertion point")
source = source.replace(
    member_marker,
    member_marker +
    '    add(files, "current/PRIOR_RETURN280_B04_CONTEXT_310.json", (BASE / "PRIOR_RETURN280_B04_CONTEXT_310.json").read_bytes())\n'
    '    add(files, "current/INVULNERABLE_SPHERE_DIRECTOR_REQUIREMENTS_310.json", (BASE / "INVULNERABLE_SPHERE_DIRECTOR_REQUIREMENTS_310.json").read_bytes())\n'
    '    add(files, "history/Return308_DIRECTOR_RETURN.zip", return308_archive.read_bytes())\n',
)
if 'history/Return308_DIRECTOR_RETURN.zip' not in source:
    raise RuntimeError("Generated packet does not bind the prior Return308 archive")

# Update queue/handoff outputs to successor 310 while preserving queue309/handoff309 as inputs.
source = source.replace(
    '    qpath.write_bytes(enc(q_after))\n    q_bind = file_bind(qpath)',
    '    q_outpath = BASE / "CURRENT_SPELL_QUEUE_310.json"\n    q_outpath.write_bytes(enc(q_after))\n    q_bind = file_bind(q_outpath)',
)
source = source.replace(
    '    hpath.write_bytes(enc(h_after))',
    '    h_outpath = BASE / "CURRENT_HANDOFF_310.json"\n    h_outpath.write_bytes(enc(h_after))',
)

if 'return235_' in source or 'RETURN235_' in source:
    raise RuntimeError("Stale Return235 dependency remains in generated builder")
if 'qpath.write_bytes(enc(q_after))' in source or 'hpath.write_bytes(enc(h_after))' in source:
    raise RuntimeError("Refusing to overwrite the input queue/handoff")
if 'TARGETS = ["invulnerable-sphere"]' not in source or 'len(target_cases) == 14' not in source:
    raise RuntimeError("Generated builder has incorrect Sphere scope")

namespace = {"__name__": "__main__", "__file__": str(TEMPLATE), "return280_context": return280_context}
exec(compile(source, str(TEMPLATE), "exec"), namespace)

