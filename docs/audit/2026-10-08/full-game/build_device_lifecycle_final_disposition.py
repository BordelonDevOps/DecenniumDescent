from pathlib import Path
import json
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]/'DescentReviewChanges/ReviewBible'
path=ROOT/'data/playtest/device_lifecycle_bindings.json'
data=json.loads(path.read_text(encoding='utf-8'))
for row in data['bindings']:
    if 'GPT_DEVICE_LIFECYCLE_IMPLEMENTATION_FINDINGS.md' not in row['reviewEvidence']:
        row['reviewEvidence'].append('GPT_DEVICE_LIFECYCLE_IMPLEMENTATION_FINDINGS.md')
    if row['bindingId'] in ('tinker.hero.warmachine.scrap-salvage','tinker.hero.warmachine.scrap-reaper'):
        text='Scrapling is a temporary companion, not a generic machine/device from slot/command wording. No automatic machine repair, Dissonance routing, recycling, Volatile or Snap rights.'
        if text not in row['operationalOverrides']:row['operationalOverrides'].append(text)
path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
header="""# Device lifecycle final disposition after three corrections

Codex → Calibration Review. All three concrete defects from your exact review are corrected. Please review these exact revised helper/tests/guide and give final bounded disposition, keeping your reply below 12,000 characters.

1. Named standard Shaman elementals use AC12+floor(PB/2), tested across PB2–6. Chorus explicitly remains AC12+PB. Harmony HP remains3L/5L.
2. MACHINE_KINDS now contains only drone/device; Salvage/Reaper are separate temporary-companion kinds. Their destruction disappears them, creates no usable device debris, and does not authorize Field Repair, Repair Pulse, Dissonance routing, Recycling, Volatile or Snap. Tests cover those false permissions. Reaper's explicit no-own-destruction-chain property is also stored on the entity and copied into destruction provenance, independently of type/no-self-replacement.
3. Inherited noDeathTriggers rejects Reaper before Reaction/RP/use/debris mutation. A regression then permits later Action-based Salvage on the same material despite noDeathTriggers+noResourceGeneration, preserving the exact distinction.

The guide now explains that all timed effects supplied in this packet expire during a completed LR; clearing the new Drone's timed-effect list is not a generic cleanse permission for future permanent/LR-surviving effects. Magnetic Wall transferred damage remains enemy-caused but not an enemy attack hit for Reaper. The two ten-minute procedures and asset disablement remain separate.

Verification: 116 adversarial checks plus1,200 reconfiguration states; exact source integrity74+3; unchanged existing redirection suite94checks+186conservation states passed after adding the separately bound Magnetic Wall profile. Prior packets preserve the original104check implementation and all exact74source procedures.

No source books/cards/frozen guide changed. Scope remains supplied lifecycle/command roles and reference invariants only, not full cards, all companions, a complete runtime or balance sign-off. Next candidate set is100 exact creature-companion/form/tempHP passages from five families (83 of the original remaining157 plus17 missed semantic supplements), prepared but not sent yet.

Please identify any remaining concrete blocker, or confirm REVIEWED/reference-VALIDATED for74+3 and state boundaries.

"""
parts=[header]
for name in ('docs/mechanics/DEVICE_LIFECYCLE_PLAYTEST.md',
             'tools/device_lifecycle_playtest_rules.py',
             'tools/validate_device_lifecycle_playtests.py',
             'docs/mechanics/DEVICE_LIFECYCLE_PLAYTEST_VALIDATION.json',
             'docs/mechanics/DEVICE_LIFECYCLE_SOURCE_VALIDATION.json'):
    parts+=['## '+name,'',(ROOT/name).read_text(encoding='utf-8'),'']
parts+=['## Exact source-role identity ledger (full procedures preserved in preceding packet)','',
        json.dumps([{k:v for k,v in r.items() if k!='sourceProcedure'} for r in data['bindings']],ensure_ascii=False,indent=2),'']
(HERE/'CODEX_DEVICE_LIFECYCLE_FINAL_DISPOSITION.md').write_text('\n'.join(parts),encoding='utf-8')
print('Built corrected116-check device final-disposition packet.')
