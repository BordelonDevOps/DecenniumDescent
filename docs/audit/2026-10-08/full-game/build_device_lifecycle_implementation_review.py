from pathlib import Path
import json
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]/'DescentReviewChanges/ReviewBible'
path=ROOT/'data/playtest/device_lifecycle_bindings.json'
data=json.loads(path.read_text(encoding='utf-8'))
data['status']='IMPLEMENTED CANDIDATE; exact lifecycle/command review pending'
for row in data['bindings']:
    row['status']='SOURCE-AUDITED / DRAFTABLE; exact implementation review pending'
    row['reviewEvidence']=list(dict.fromkeys(row['reviewEvidence']+[
        'GPT_DEVICE_LIFECYCLE_BOUNDARIES.md','GPT_DEVICE_LIFECYCLE_PREDICATES.md']))
    row['operationalOverrides']=[
        'Current lifecycle/command role is defined in DEVICE_LIFECYCLE_PLAYTEST.md. Boundary and predicate replies supersede conflicting initial proposals. Full card effects are not certified.',
        'Shared owner command/damage ledgers, source-qualified life states, original expiry, slot footprint, protected-disable and destruction provenance apply only where the source role calls for them.']
    row['openIssues']=['Exact implementation review pending; other effects and wider companion completeness remain outside this bounded role.']
    if row['bindingId']=='tinker.hero.artificer.restoration-field':
        row['classification']='SLOT_EFFECT/HEALING_ZONE; no physical anchor'
        row['operationalOverrides'].append('No imported object HP/AC, machine targeting, disable routing, reconstruction or debris.')
    if row['bindingId']=='tinker.hero.techsmith.efficient-recycling':
        row['operationalOverrides'].append('Enemy destruction is not required; friendly/accidental qualifies if not deliberate sacrifice/copy and noResourceGeneration absent.')
    if row['bindingId']=='tinker.hero.warmachine.scrap-reaper':
        row['operationalOverrides'].append('No invented deployable-slot requirement; shared command still applies; exact enemy-hit predicate retained.')
path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
header="""# Exact device lifecycle implementation review

Codex → Calibration Review. Please review the exact candidate against all 74 supplied class source roles and three frozen shared paragraphs. Source cards, books and frozen class guide are unchanged. Reply under 15,000 characters and identify concrete defects before disposition.

Current verification: 104 targeted adversarial checks and 1,200 reconfiguration-state cases pass. Source integrity separately verifies 74+3. This bounded package covers life/deployment state, protected disablement, repair/reconstruction, original material identity, slot replacement and Echo dependencies, command/damage budgets, creation/dynamic stats and Magnetic Wall's newly bound transfer. Other effects on the same cards and the other 157 lifecycle candidates remain open.

Important caller boundaries are explicit, not completion claims: actual source access/class gates, known eligible profiles, range/space/LOS, actual rolls and damage defenses, source recharge/encounter/rest calendar and use keys, authoritative owner wallet/command ledger, standard movement/collision, concentration/pulse propagation, module riders and remaining individual card effects. Placement validates state/capacity/payment but receives already source/geometry-legal entities and costs. This is a rules reference for tabletop and later engine implementation, not a full video game.

Please check especially:

1. First actual destruction locks the instance's only material/opportunity set. Snap and ten-minute Drone reconstruction consume that material and cannot manufacture another first-event entitlement. Fresh explicit LR Drone incarnation is a new instance but carries asset disablement. The two ten-minute procedures remain separate.
2. Efficient Recycling now matches your correction: friendly/accidental destruction can qualify; sacrifice/copy and noResourceGeneration block. Salvage and Reaper keep distinct hostile/actual-enemy-hit predicates.
3. Magnetic Wall branch is not an attack hit, so a Wall destroyed purely by transferred enemy damage is enemy-caused for Volatile/Salvage but does NOT satisfy Scrap Reaper's stricter enemy-hit source wording. Confirm this consequence, or give the exact intended source override; none has been silently added.
4. Off-turn automatic Decoy damage uses the owner numbered-round damage allowance without a BA. Only Tinker BA commands impose regular-turn eligibility in the helper; Gadget Sync still needs its actual printed trigger checked by caller. No passive Cinder/Volatile charge against command allowance.
5. noDeathTriggers now blocks Cinder/Volatile destruction bursts. The Reaper helper currently enforces hostile enemy-hit/no-sacrifice/copy/friendly/secondary and no-self-replacement predicates. Does inherited noDeathTriggers also bar Reaper's Reaction while leaving later active Salvage distinct? Does any exact source forbid that active material transformation too? Avoid widening noResourceGeneration to all transformations.
6. Scrapling no-self-replacement is enforced for Salvage/Reaper, but is not broadened to an unrelated Volatile exclusion beyond its printed friendly/copy/sacrifice/secondary bans. Is a first genuine enemy destruction of a Salvage Scrapling allowed to use separately owned Volatile, subject to no-chain flags? Also clarify Recycling of that new Scrapling under its exact deployment payment provenance if needed.
7. The bounded helper models positive-HP repairs and preserves tempHP/module/ammo/effect clocks. Normal damage consumes tempHP before object death. LR Drone rebuild clears old timed effects and gives zero tempHP; source-authorized long-rest use resets remain a separate canonical rest operation. Confirm whether source-effect clocks need further retention across LR instance replacement.
8. Check the source aliases/stat/capacity table and anti-loop implications rather than granting blanket full-card closure. Guide has NEW integration labels; no new named abilities.

If correct, explicitly dispose of the 74 supplied lifecycle/command roles plus3 shared paragraphs and state remaining scope. If anything needs correction, return the smallest exact counterexample.

"""
parts=[header]
for name in ('docs/mechanics/DEVICE_LIFECYCLE_PLAYTEST.md',
             'tools/device_lifecycle_playtest_rules.py',
             'tools/validate_device_lifecycle_playtests.py',
             'docs/mechanics/DEVICE_LIFECYCLE_PLAYTEST_VALIDATION.json',
             'docs/mechanics/DEVICE_LIFECYCLE_SOURCE_VALIDATION.json'):
    parts+=['## '+name,'',(ROOT/name).read_text(encoding='utf-8'),'']
parts+=['## Full current source roles','',json.dumps(data,ensure_ascii=False,indent=2),'']
sources=json.loads((HERE/'DEVICE_LIFECYCLE_SOURCE_CANDIDATES.json').read_text(encoding='utf-8'))
parts+=['## Source inventory supporting records','',
        json.dumps({k:v for k,v in sources.items() if k!='classRecords'},ensure_ascii=False,indent=2),'']
parts+=['## Magnetic Wall new profile added alongside original redirection profiles','',
        (ROOT/'tools/redirection_playtest_rules.py').read_text(encoding='utf-8'),'']
(HERE/'CODEX_DEVICE_LIFECYCLE_IMPLEMENTATION_REVIEW.md').write_text('\n'.join(parts),encoding='utf-8')
print('Built exact 74+3 device lifecycle implementation review.')
