"""Record actual source discussion without promoting missing runtime adapters."""
from pathlib import Path
import hashlib
import json

audit=Path(__file__).resolve().parent
game=audit.parents[3]
root=game/'DescentReviewChanges/ReviewBible'
conference=audit/'GPT_TEMPORAL_PARENT_BOUNDARIES.md'
clarification=audit/'GPT_TEMPORAL_PARENT_CADENCE_CLARIFICATION.md'
assert 'SOURCE-DISCUSSED / IMPLEMENTATION-READY' in conference.read_text(encoding='utf-8')
assert 'Confirmed. My parent-conference wording' in clarification.read_text(encoding='utf-8')
inventory=json.loads((audit/'TEMPORAL_PARENT_STATE_INVENTORY.json').read_text(encoding='utf-8'))
source_hashes={r['source']:r['sourceSha256'] for r in inventory['holders']}
for name,digest in source_hashes.items():
    assert hashlib.sha256((root/name).read_bytes()).hexdigest()==digest
status={
 'status':'SOURCE-DISCUSSED / IMPLEMENTATION-READY; parent code and adversarial validation pending',
 'evidence':[str(p.relative_to(game)).replace('\\','/') for p in (conference,clarification)],
 'sourceCodeEvidenceHashes':source_hashes,
 'discussedCases':10,'inventoriedHolderTypes':9,'inventoriedFields':85,'druidSourceProfiles':26,
 'sourceDecisions':['participant exact concentration closure','protected mixed-roster casts',
   'permanent True Polymorph reconciliation','paid same-instance Druid renewal receipts',
   'local permissions versus conserved global expenditures','form entry and independent Howl shields',
   'authentic recharge markers','Shapechange and repeat-save iteration windows',
   'conserved current Druid cadence','expired anatomy and current external overlays'],
 'actionBudgetClarification':'Restore snapshot Action/Bonus Action/Reaction budgets and overlay outstanding Time Loop Reaction debts. Preserve historical events and finite spending; parent retirement creates no refund or charge.',
 'recoveryQualification':'No new generic short-rest Dissonance reset; only existing source-authorized recovery events apply.',
 'parentRuntimeImplemented':False,'fullTimeLoopOperational':False,
 'remainingMajorIntegrations':7,'wholeGameClosure':False,'githubPushed':False,
 'authoredGuide':'docs/mechanics/TEMPORAL_PARENT_PLAYTEST.md'
}
p=root/'docs/mechanics/TEMPORAL_PARENT_REVIEW_STATUS.json'
assert not p.exists();p.write_text(json.dumps(status,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

p=root/'data/playtest/game_development_coverage.json'
backup=audit/'COVERAGE_BEFORE_TEMPORAL_PARENT_CONFERENCE.json'
assert not backup.exists();backup.write_bytes(p.read_bytes())
packet=json.loads(p.read_text(encoding='utf-8'))
ids=('DD-03','DD-08','DD-09','DD-16','DD-18','DD-21','DD-35','DD-63','DD-64')
for row in packet['aspects']:
    if row['id'] not in ids:continue
    row['validationEvidence']=list(dict.fromkeys(row['validationEvidence']+status['evidence']+[
      'DescentReviewChanges/ReviewBible/docs/mechanics/TEMPORAL_PARENT_REVIEW_STATUS.json',
      'DescentReviewChanges/ReviewBible/docs/mechanics/TEMPORAL_PARENT_PLAYTEST.md']))
    row['openIssues'].append('Ten form/concentration/Druid parent cases and the Action-budget clarification are source-discussed;85 actual fields and26 Druid profiles inventoried. Parent runtime and adversarial review remain pending, with all seven major temporal integrations still open.')
p.write_text(json.dumps(packet,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

note='''
## Parent source conference completed

The [actual ten-case conference](GPT_TEMPORAL_PARENT_BOUNDARIES.md) and [Action-budget/cadence clarification](GPT_TEMPORAL_PARENT_CADENCE_CLARIFICATION.md) settle source policies for participant concentration, protected mixed-roster spells, permanent True Polymorph, paid Druid renewals, local/global spending, entry shields, authentic recharge, new-iteration windows, conserved cadence and expired anatomy. Five temporal rules are explicitly labeled new/provisional in the [authored parent guide](../../../../DescentReviewChanges/ReviewBible/docs/mechanics/TEMPORAL_PARENT_PLAYTEST.md).

The Action clarification preserves the approved kernel: current turn allowances restore from the snapshot with all outstanding Time Loop Reaction debts; historical activation events and finite resource spending remain recorded. No new generic short-rest Dissonance reset was adopted from loose wording in the reply; actual source-authorized recovery still governs.

`TEMPORAL_PARENT_STATE_INVENTORY.json` accounts for85 actual fields across9 holder types, including Druid fields initialized outside the constructor, and links all26 exact form profiles. This is source/implementation preparation, not runtime validation. The new review-status manifest explicitly leaves parent code, all seven larger integrations, full Time Loop and whole-game approval unfinished. All exact previously reviewed helper hashes remain unchanged. No original content was deleted or pushed.
'''
for name in ('README.md','REVIEW_STATUS.md','TEMPORAL_ADAPTER_ENGINEERING_NOTES.md','TEMPORAL_PARENT_INTEGRATION_NEXT.md'):
    p=audit/name;p.write_text(p.read_text(encoding='utf-8')+note,encoding='utf-8')

p=root/'docs/mechanics/TEMPORAL_KERNEL_PLAYTEST.md'
text=p.read_text(encoding='utf-8')
text+='\nThe next [form/concentration parent policies](TEMPORAL_PARENT_PLAYTEST.md) are now source-discussed with the notebook, including all26 Druid profiles and explicit renewal/stabilization history. The [parent status](TEMPORAL_PARENT_REVIEW_STATUS.json) records ten cases and the corrected Action-budget wording. Runtime parent integration and its validation are still pending.\n'
p.write_text(text,encoding='utf-8')
p=game/'START_HERE.md';text=p.read_text(encoding='utf-8')
text=text.replace('Current discussion covers form/concentration parents and all 26 Druid profiles.', '[Form/concentration parent policies](DescentReviewChanges/ReviewBible/docs/mechanics/TEMPORAL_PARENT_PLAYTEST.md) are now settled for all 26 Druid profiles; their runtime integration remains next.')
p.write_text(text,encoding='utf-8')
print('Recorded10 source-policy cases and clarification. Runtime and whole-game completion remain open.')
