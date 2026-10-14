"""Bind the actual notebook closure to exactly the 59-method source journal."""
from pathlib import Path
import hashlib,json
audit=Path(__file__).resolve().parent;game=audit.parents[3];root=game/'DescentReviewChanges/ReviewBible'
evidence='docs/audit/2026-10-08/full-game/GPT_TEMPORAL_PARENT_HISTORY_CLOSURE.md'
reply=(game/evidence).read_text(encoding='utf-8')
assert 'I confirm this bounded checkpoint.' in reply and '59' in reply
assert 'REVIEWED / reference-VALIDATED' in reply
submission=json.loads((audit/'TEMPORAL_PARENT_HISTORY_TIME_PIN_SUBMISSION.json').read_text())
for name,h in submission['hashes'].items():assert hashlib.sha256((root/name).read_bytes()).hexdigest()==h
control=json.loads((root/'docs/mechanics/TEMPORAL_CONTROL_WORLD_REVIEW_STATUS.json').read_text())
for name,h in control['reviewedHashes'].items():assert hashlib.sha256((root/name).read_bytes()).hexdigest()==h
parent=json.loads((root/'docs/mechanics/TEMPORAL_PARENT_REVIEW_STATUS.json').read_text())
for name,h in parent['sourceCodeEvidenceHashes'].items():assert hashlib.sha256((root/name).read_bytes()).hexdigest()==h
assert hashlib.sha256((root/'docs/mechanics/CLASS_PLAYTEST_RULES.md').read_bytes()).hexdigest()=='adb2f4752b45dc70ce792a675bb30dda362aab5056588061bcde3ba31c4c8a81'

p=root/'docs/mechanics/TEMPORAL_PARENT_HISTORY_REVIEW_STATUS.json'
backup=audit/'PARENT_HISTORY_STATUS_BEFORE_CLOSURE.json';assert not backup.exists();backup.write_bytes(p.read_bytes())
status=json.loads(p.read_text());status.update({
 'status':'REVIEWED / reference-VALIDATED — actual canonical Druid/Transformation parent-operation history journal only',
 'latestActualReview':evidence,'independentEvidence':evidence,'allSixFindingsConfirmedRepaired':True,
 'reviewedHashes':submission['hashes'],'testMethods':59,
 'scopeQualification':'Historical evidence and retained identities only; no authorization to restore from them without the larger parent planner',
 'authorizationNote':'The human authorized GitHub delivery after joint whole-game flow confirmation. This bounded checkpoint does not satisfy that condition.'})
p.write_text(json.dumps(status,indent=2)+'\n',encoding='utf-8')

p=root/'docs/mechanics/TEMPORAL_PARENT_PLAYTEST.md';text=p.read_text(encoding='utf-8')
text=text.replace('**Source policies discussed; parent implementation and adversarial review pending. Full Time Loop remains unavailable.**',
 '**Source policies discussed and the 59-check operation-history layer jointly reviewed. Parent restoration remains unimplemented; full Time Loop remains unavailable.**')
text=text.replace('passes [59 checks](TEMPORAL_PARENT_HISTORY_VALIDATION.json), and is under review.',
 'passes [59 checks](TEMPORAL_PARENT_HISTORY_VALIDATION.json), and has [actual notebook closure](../../../../docs/audit/2026-10-08/full-game/GPT_TEMPORAL_PARENT_HISTORY_CLOSURE.md). All six evidence findings are confirmed repaired within this history-only scope.')
p.write_text(text,encoding='utf-8')

p=game/'START_HERE.md';text=p.read_text(encoding='utf-8')
text=text.replace('The latest jointly reviewed checkpoint is the [Time Loop control/healing-pulse interface]',
 'The previously reviewed [Time Loop control/healing-pulse interface]')
text=text.replace('Its 50 integration checks','Its 50 integration checks')
text=text.replace('has a 59-check repair under notebook review after four initial evidence findings.',
 'is now jointly reviewed with 59 checks and all six evidence findings resolved. This establishes reliable source history; it does not yet restore forms or concentration.')
p.write_text(text,encoding='utf-8')

p=audit/'REVIEW_STATUS.md';text=p.read_text(encoding='utf-8')
text=text.replace('| Latest jointly reviewed code | Bounded Time Loop control/pulse interface, with 50+76+22 checks and exact hashes in its [review manifest](../../../../DescentReviewChanges/ReviewBible/docs/mechanics/TEMPORAL_CONTROL_WORLD_REVIEW_STATUS.json) |',
 '| Latest jointly reviewed code | Parent operation-history journal: 59 checks and all six findings resolved. The earlier control/pulse checkpoint retains its separate 50+76+22 checks. |')
text=text.replace('| Current joint work | Four initial parent-history repairs confirmed; two follow-up fixes pass 59 checks and are [under notebook review](../../../../DescentReviewChanges/ReviewBible/docs/mechanics/TEMPORAL_PARENT_HISTORY_REVIEW_STATUS.json) |',
 '| Current joint work | [History checkpoint closed](../../../../DescentReviewChanges/ReviewBible/docs/mechanics/TEMPORAL_PARENT_HISTORY_REVIEW_STATUS.json); actual parent restoration is next |')
p.write_text(text,encoding='utf-8')

p=root/'data/playtest/game_development_coverage.json';packet=json.loads(p.read_text(encoding='utf-8'))
for row in packet['aspects']:
    if any('two follow-up fixes for query time/reference pins pass59 checks and await review' in v for v in row['openIssues']):
        row['openIssues']=[v.replace('Four initial parent-history repairs confirmed;two follow-up fixes for query time/reference pins pass59 checks and await review.',
            'Parent operation-history journal jointly reviewed with59 checks;all six evidence findings resolved.') for v in row['openIssues']]
        row['reviewEvidence']=list(dict.fromkeys(row['reviewEvidence']+[evidence]))
p.write_text(json.dumps(packet,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

note='''
## Parent operation-history checkpoint closed

The notebook [confirmed the exact 59-method journal](GPT_TEMPORAL_PARENT_HISTORY_CLOSURE.md), closing all four initial findings and the two follow-up findings. The [current manifest](../../../../DescentReviewChanges/ReviewBible/docs/mechanics/TEMPORAL_PARENT_HISTORY_REVIEW_STATUS.json) binds the actual closure to the helper, tests and validation report. Earlier packets and actual reviews remain preserved. Ordinary source helpers, the reviewed control/pulse files and frozen class rules are unchanged by hash comparison.

Next work is the actual parent transaction: capture the reviewed identities/history, propose complete forms/concentration and dependent state, reconcile current inventory/enrollment/geometry, stage the exact original references atomically, and exercise subsequent genuine events. The present Transaction intentionally accepts only data values, so reference staging requires its own reviewed extension. The kernel still rejects active form identities and admits only its existing control/pulse adapter. Do not remove either gate based on history-only approval.

All seven larger integration domains remain open. Full Time Loop, the remaining game content, final whole-game flow review and GitHub delivery remain unfinished. Nothing was deleted or pushed.
'''
for name in ('README.md','REVIEW_STATUS.md','TEMPORAL_PARENT_INTEGRATION_NEXT.md'):
    p=audit/name;p.write_text(p.read_text(encoding='utf-8')+note,encoding='utf-8')
print('Recorded exact59-method joint closure. Earlier reviewed code unchanged. All seven major integrations remain open.')
