"""Record a confirmed bounded disposition; never promote whole cards/game."""
from pathlib import Path
import json
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]/'DescentReviewChanges/ReviewBible'
GAME=ROOT.parents[1]
evidence=HERE/'GPT_DEVICE_LIFECYCLE_FINAL_CLOSURE.md'
assert evidence.exists(),'Do not record closure before reading GPT final disposition'
reply=evidence.read_text(encoding='utf-8')
assert 'REVIEWED' in reply and 'VALIDATED' in reply,'Final disposition must be explicitly confirmed'
assert reply.startswith('# GPT confirmed device lifecycle closure'),'Use only a manually inspected, unconditional closure reply'
closure='docs/audit/2026-10-08/full-game/GPT_DEVICE_LIFECYCLE_FINAL_CLOSURE.md'
report_path=ROOT/'docs/mechanics/DEVICE_LIFECYCLE_PLAYTEST_VALIDATION.json'
report=json.loads(report_path.read_text(encoding='utf-8'))
assert report['result']=='PASS' and report['checkCount']==132 and report['reconfigurationStates']==1200
report['status']='REVIEWED / reference-VALIDATED; bounded74+3 lifecycle/command roles'
report['reviewClosure']=closure
report_path.write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
path=ROOT/'data/playtest/device_lifecycle_bindings.json'
data=json.loads(path.read_text(encoding='utf-8'))
data['status']='REVIEWED / reference-VALIDATED; bounded74+3 lifecycle/command roles'
data['reviewClosure']=closure
for row in data['bindings']:
    row['status']='REVIEWED / reference-VALIDATED: supplied lifecycle/command or guard/exclusion role only'
    row['reviewEvidence']=list(dict.fromkeys(row['reviewEvidence']+[
        'GPT_DEVICE_LIFECYCLE_FINAL_FINDINGS.md','GPT_DEVICE_LIFECYCLE_FINAL_CLOSURE.md']))
    row['openIssues']=['Other card components, unsupplied object-targeting content, wider companions/forms/tempHP and complete runtime remain open.']
path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
path=ROOT/'data/playtest/game_development_coverage.json'
coverage=json.loads(path.read_text(encoding='utf-8'))
for ident in ('DD-24','DD-35'):
    row=next(r for r in coverage['aspects'] if r['id']==ident)
    for field,value in (
        ('reviewEvidence',closure),
        ('sourceEvidence','docs/audit/2026-10-08/full-game/DEVICE_LIFECYCLE_SOURCE_CANDIDATES.json'),
        ('draftEvidence','DescentReviewChanges/ReviewBible/docs/mechanics/DEVICE_LIFECYCLE_PLAYTEST.md'),
        ('draftEvidence','DescentReviewChanges/ReviewBible/docs/mechanics/DEVICE_LIFECYCLE_SOURCE_BINDINGS.md'),
        ('validationEvidence','DescentReviewChanges/ReviewBible/docs/mechanics/DEVICE_LIFECYCLE_PLAYTEST_VALIDATION.json'),
        ('validationEvidence','DescentReviewChanges/ReviewBible/docs/mechanics/DEVICE_LIFECYCLE_SOURCE_VALIDATION.json')):
        if value not in row[field]:row[field].append(value)
    row['status']='selected-interfaces-closed-remainder-integrating'
    row['closure']='open'
    text='Device/Totem lifecycle and shared commands:74 source roles plus3 frozen paragraphs jointly reviewed;132 checks and1,200 reconfiguration states. Scraplings retain temporary-companion type, standard elementals retain half-PB AC, and Reaper respects death-trigger restrictions.'
    if text not in row.setdefault('completedScopes',[]):row['completedScopes'].append(text)
    row['openIssues']=[v for v in row['openIssues'] if not v.startswith(('Next device/Totem lifecycle conference','All131 remaining class passages discussed; implement'))]
    text='Remaining creature companion, form/tempHP, copy and other catalog interfaces require source review. The next prepared five-family slice contains83 original candidates plus17 semantic supplements (100 exact passages); no full-family closure.'
    if text not in row['openIssues']:row['openIssues'].append(text)
path.write_text(json.dumps(coverage,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
path=ROOT/'docs/mechanics/DEVICE_LIFECYCLE_PLAYTEST.md'
text=path.read_text(encoding='utf-8').replace(
    '**Implemented candidate; exact GPT implementation review pending.**',
    '**REVIEWED / reference-VALIDATED: 132 targeted checks and 1,200 reconfiguration states.**')
if 'GPT_DEVICE_LIFECYCLE_FINAL_CLOSURE.md)' not in text:
    text+='\n[Final notebook disposition](../../../../docs/audit/2026-10-08/full-game/GPT_DEVICE_LIFECYCLE_FINAL_CLOSURE.md) closes only this supplied 74+3 interface. Human balance and whole-game completion remain separate.\n'
path.write_text(text,encoding='utf-8')
path=ROOT/'docs/mechanics/HEALING_PULSE_PLAYTEST.md'
text=path.read_text(encoding='utf-8').replace(
    "The scheduler takes each anchor's active/coverage state from the future object lifecycle. Parent destruction does not yet authorize this package to destroy or preserve its Echo. Both anchors never supply a six-target budget.",
    "The scheduler takes each anchor's active/coverage state from the [reviewed device/Totem lifecycle](DEVICE_LIFECYCLE_PLAYTEST.md). The parent ending, including destruction, ends its dependent Echo administratively; ending Echo alone leaves the parent. Both anchors still share the original recipient/pulse budget and never supply six targets. Restoration Field is a slot effect with no fabricated HP-bearing machine anchor.")
path.write_text(text,encoding='utf-8')
path=ROOT/'docs/mechanics/DEVELOPMENT_ROADMAP.md'
text=path.read_text(encoding='utf-8').replace(
    'Zone scheduling, companion/device lifecycle and complete copy semantics remain open; the selected maximum-HP interface is closed below.',
    'Selected maximum-HP, pulse scheduling and device/Totem interfaces are closed below. Wider creature companions, forms/tempHP, copy semantics and other catalogs remain open.').replace(
    'Device/Totem lifecycle is next.','The selected device/Totem lifecycle is also closed below; broader creature companions are next.')
line='- [Devices, Totems and shared commands](DEVICE_LIFECYCLE_PLAYTEST.md):74 class roles plus3 frozen paragraphs,132 checks and1,200 reconfiguration states. [Final notebook review](../../../../docs/audit/2026-10-08/full-game/GPT_DEVICE_LIFECYCLE_FINAL_CLOSURE.md) closes this bounded interface; creature companions, forms/tempHP and wider catalogs remain open.'
if line not in text:text+='\n'+line+'\n'
path.write_text(text,encoding='utf-8')
path=ROOT/'docs/mechanics/HEALING_SOURCE_EXTENSIONS.md'
text=path.read_text(encoding='utf-8').replace(
    '3. Sustained zones and pulse scheduling: activation, paid source-turn windows, target-start and entry events, capacity and expiry.',
    '3. [Selected sustained-zone and pulse scheduling interface](HEALING_PULSE_PLAYTEST.md):100 roles plus6 supporting passages reviewed;89 checks and301 reserve partitions.').replace(
    '4. Companion/device/temp-HP lifecycle: living companions, destroyed reconstruction, Druid Buffer Reserve and nonstacking.',
    '4. [Selected device/Totem lifecycle](DEVICE_LIFECYCLE_PLAYTEST.md):74 roles plus3 shared paragraphs reviewed;132 checks and1,200 states. Broader living companions, Druid forms/Buffer Reserve and tempHP remain open.')
path.write_text(text,encoding='utf-8')
for path in (HERE/'README.md',HERE/'REVIEW_STATUS.md'):
    text=path.read_text(encoding='utf-8')
    note='\n## Device/Totem bounded closure\n\n[Exact corrected packet](CODEX_DEVICE_LIFECYCLE_CORRECTIONS_2.md) received [GPT final closure](GPT_DEVICE_LIFECYCLE_FINAL_CLOSURE.md) for74 lifecycle/command roles plus3 frozen paragraphs.132 checks and1,200 HP-conversion states pass; the earlier redirection suite retains94 checks/186 conservation states. Corrections preserve standard-elemental AC, temporary Scrapling type and inherited death-trigger restrictions. Original sources remain unchanged. Next prepared creature slice:100 passages (83 original candidates plus17 semantic supplements); whole game remains active and incomplete.\n'
    if '## Device/Totem bounded closure' not in text:text+=note
    path.write_text(text,encoding='utf-8')
path=GAME/'START_HERE.md'
text=path.read_text(encoding='utf-8')
note='\nThe selected [device, Totem and shared-command rules](DescentReviewChanges/ReviewBible/docs/mechanics/DEVICE_LIFECYCLE_PLAYTEST.md) are jointly reviewed:74 source roles plus3 shared passages,132 checks and1,200 state cases. Repair, reconstruction, disablement, slots and destruction provenance now have explicit contracts. Broader creature companions and the remaining game audit continue.\n'
if note not in text:text+=note
path.write_text(text,encoding='utf-8')
print('Recorded confirmed74+3 closure; DD24/DD35 and whole game remain open.')
